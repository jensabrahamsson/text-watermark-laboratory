"""Same prompt → unmarked twin + mixin-marked twin → official score.

SynthID-Text is applied at sampling time. This does not stamp an existing
string; it generates new tokens from the prompt with and without the mixin.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import torch

from text_watermark_tools.generate import (
    Generation,
    _load_marked_model,
    _load_unmarked_model,
    generate_device,
    generate_text,
    is_gpt2_name,
)
from text_watermark_tools.score import (
    CONTROL_INSTANCE,
    PUBLIC_INSTANCE,
    OfficialScore,
    control_keys,
    format_score,
    load_tokenizer,
    official_processor,
    official_score_text,
    official_score_token_ids,
    public_ngram_len,
)


@dataclass
class PairRow:
    stem: str
    prompt: str
    prompt_score: OfficialScore
    marked_text: str
    marked_score: OfficialScore
    unmarked_text: str
    unmarked_score: OfficialScore
    alt_text: str = ""
    alt_score_public: OfficialScore | None = None
    alt_score_matching: OfficialScore | None = None
    extra_marked: list[tuple[str, OfficialScore]] = field(default_factory=list)
    extra_unmarked: list[tuple[str, OfficialScore]] = field(default_factory=list)
    extra_control: list[tuple[str, OfficialScore, OfficialScore]] = field(
        default_factory=list
    )


@dataclass
class PairRun:
    rows: list[PairRow]
    max_new_tokens: int
    seed: int
    alt_keys: list[int] | None = None
    model_name: str = "gpt2"
    ngram_len: int = 5


def collect_prompts(path: Path) -> list[tuple[str, str]]:
    """Load (stem, prompt) pairs from a .txt file or a directory of .txt files."""
    path = Path(path)
    if path.is_dir():
        files = sorted(p for p in path.glob("*.txt") if p.is_file())
        if not files:
            raise FileNotFoundError(f"no .txt files in {path}")
        return [(f.stem, f.read_text()) for f in files]
    if not path.is_file():
        raise FileNotFoundError(f"not a file or directory: {path}")
    return [(path.stem, path.read_text())]


def _score_to_dict(score: OfficialScore) -> dict:
    return {
        "mean": score.mean,
        "weighted_mean": score.weighted_mean,
        "n_tokens": score.n_tokens,
        "n_unmasked_ngrams": score.n_unmasked_ngrams,
    }


def pair_stem_files_complete(out_dir: Path, stem: str, n_samples: int) -> bool:
    """True when marked/unmarked draws for this stem are already on disk."""
    if n_samples < 1:
        return False
    out_dir = Path(out_dir)
    needed = [
        out_dir / f"{stem}-marked.txt",
        out_dir / f"{stem}-unmarked-gen.txt",
    ]
    for i in range(2, n_samples + 1):
        needed.append(out_dir / f"{stem}-marked-{i}.txt")
        needed.append(out_dir / f"{stem}-unmarked-gen-{i}.txt")
    return all(p.is_file() and p.stat().st_size > 0 for p in needed)


def persist_pair_row_texts(row: PairRow, out_dir: Path) -> None:
    """Write one stem's prompt and twin files. Does not rewrite results.json."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{row.stem}-prompt.txt").write_text(row.prompt.rstrip() + "\n")
    if row.unmarked_text:
        (out_dir / f"{row.stem}-unmarked-gen.txt").write_text(
            row.unmarked_text.strip() + "\n"
        )
    if row.marked_text:
        (out_dir / f"{row.stem}-marked.txt").write_text(row.marked_text.strip() + "\n")
    for i, (txt, _sc) in enumerate(row.extra_marked, start=2):
        (out_dir / f"{row.stem}-marked-{i}.txt").write_text(txt.strip() + "\n")
    for i, (txt, _sc) in enumerate(row.extra_unmarked, start=2):
        (out_dir / f"{row.stem}-unmarked-gen-{i}.txt").write_text(txt.strip() + "\n")
    if (
        row.alt_text
        and row.alt_score_public is not None
        and row.alt_score_matching is not None
    ):
        (out_dir / f"{row.stem}-control-gen.txt").write_text(row.alt_text.strip() + "\n")
        for i, (txt, _pub, _match) in enumerate(row.extra_control, start=2):
            (out_dir / f"{row.stem}-control-gen-{i}.txt").write_text(txt.strip() + "\n")


def _score_text(text: str, tokenizer, ngram_len: int, keys=None) -> OfficialScore:
    proc = official_processor(keys=keys, ngram_len=ngram_len)
    return official_score_text(text, tokenizer=tokenizer, processor=proc)


def _score_ids(ids, tokenizer, ngram_len: int, keys=None) -> OfficialScore:
    proc = official_processor(keys=keys, ngram_len=ngram_len)
    return official_score_token_ids(ids, tokenizer=tokenizer, processor=proc)


def load_pair_row_from_files(
    out_dir: Path,
    stem: str,
    prompt: str,
    tokenizer,
    *,
    n_samples: int,
    ngram_len: int = 5,
) -> PairRow:
    """Rebuild a row from already-written twins. Re-scores; does not regenerate."""
    out_dir = Path(out_dir)
    text = prompt if prompt.endswith("\n") else prompt + "\n"
    marked = (out_dir / f"{stem}-marked.txt").read_text()
    unmarked = (out_dir / f"{stem}-unmarked-gen.txt").read_text()
    extra_marked: list[tuple[str, OfficialScore]] = []
    extra_unmarked: list[tuple[str, OfficialScore]] = []
    for i in range(2, n_samples + 1):
        extra_m = (out_dir / f"{stem}-marked-{i}.txt").read_text()
        extra_u = (out_dir / f"{stem}-unmarked-gen-{i}.txt").read_text()
        extra_marked.append(
            (extra_m, _score_text(extra_m, tokenizer, ngram_len))
        )
        extra_unmarked.append(
            (extra_u, _score_text(extra_u, tokenizer, ngram_len))
        )
    return PairRow(
        stem=stem,
        prompt=text,
        prompt_score=_score_text(text, tokenizer, ngram_len),
        marked_text=marked,
        marked_score=_score_text(marked, tokenizer, ngram_len),
        unmarked_text=unmarked,
        unmarked_score=_score_text(unmarked, tokenizer, ngram_len),
        extra_marked=extra_marked,
        extra_unmarked=extra_unmarked,
    )


def run_pairs(
    prompts: list[tuple[str, str]],
    *,
    max_new_tokens: int = 128,
    seed: int = 0,
    tokenizer=None,
    marked_model=None,
    unmarked_model=None,
    alt_model=None,
    also_control_keys: bool = False,
    model_name: str | None = None,
    n_samples: int = 1,
    resume_dir: Path | None = None,
    persist_dir: Path | None = None,
    ngram_len: int | None = None,
) -> PairRun:
    """For each prompt: score the prompt, then generate unmarked and marked twins.

    When `also_control_keys` is set, a third twin is sampled with
    `control_keys()` (not a `-marked.txt` name — `blind` must not pick it up).
    Score uses the same tokenizer as the generator.
    When `resume_dir` has complete stem files, those stems are re-scored
    instead of regenerated. When `persist_dir` is set, each stem's texts
    are written as soon as the row exists.
    """
    if n_samples < 1:
        raise ValueError("n_samples must be >= 1")
    name = model_name or "gpt2"
    nlen = public_ngram_len() if ngram_len is None else int(ngram_len)
    tok = tokenizer or load_tokenizer(name)
    device = torch.device("cpu") if is_gpt2_name(name) else generate_device()
    resume = Path(resume_dir) if resume_dir is not None else None
    persist = Path(persist_dir) if persist_dir is not None else None
    if persist is not None:
        persist.mkdir(parents=True, exist_ok=True)
    remaining = [
        (stem, prompt)
        for stem, prompt in prompts
        if resume is None or not pair_stem_files_complete(resume, stem, n_samples)
    ]
    if remaining:
        if marked_model is None:
            marked_model = _load_marked_model(
                device, model_name=name, ngram_len=nlen
            )
        if unmarked_model is None:
            unmarked_model = _load_unmarked_model(device, model_name=name)
    alt_key_list = control_keys() if also_control_keys else None
    if also_control_keys and alt_model is None:
        alt_model = _load_marked_model(
            device, keys=alt_key_list, model_name=name, ngram_len=nlen
        )

    rows: list[PairRow] = []
    for offset, (stem, prompt) in enumerate(prompts):
        text = prompt if prompt.endswith("\n") else prompt + "\n"
        if resume is not None and pair_stem_files_complete(resume, stem, n_samples):
            row = load_pair_row_from_files(
                resume, stem, text, tok, n_samples=n_samples, ngram_len=nlen
            )
            rows.append(row)
            if persist is not None:
                persist_pair_row_texts(row, persist)
            continue
        prompt_score = _score_text(text, tok, nlen)
        stride = 2 * n_samples + 2
        marked_gen: Generation = generate_text(
            text,
            marked=True,
            max_new_tokens=max_new_tokens,
            seed=seed + stride * offset,
            device=device,
            tokenizer=tok,
            model=marked_model,
            ngram_len=nlen,
        )
        unmarked_gen: Generation = generate_text(
            text,
            marked=False,
            max_new_tokens=max_new_tokens,
            seed=seed + stride * offset + 1,
            device=device,
            tokenizer=tok,
            model=unmarked_model,
        )
        extra_marked: list[tuple[str, OfficialScore]] = []
        extra_unmarked: list[tuple[str, OfficialScore]] = []
        for s_i in range(1, n_samples):
            mg = generate_text(
                text,
                marked=True,
                max_new_tokens=max_new_tokens,
                seed=seed + stride * offset + 2 * s_i,
                device=device,
                tokenizer=tok,
                model=marked_model,
                ngram_len=nlen,
            )
            ug = generate_text(
                text,
                marked=False,
                max_new_tokens=max_new_tokens,
                seed=seed + stride * offset + 2 * s_i + 1,
                device=device,
                tokenizer=tok,
                model=unmarked_model,
            )
            extra_marked.append(
                (mg.text, _score_ids(mg.token_ids, tok, nlen))
            )
            extra_unmarked.append(
                (ug.text, _score_ids(ug.token_ids, tok, nlen))
            )
        alt_text = ""
        alt_pub = None
        alt_match = None
        if alt_model is not None and alt_key_list is not None:
            alt_gen: Generation = generate_text(
                text,
                marked=True,
                max_new_tokens=max_new_tokens,
                seed=seed + 3 * offset + 2,
                device=device,
                tokenizer=tok,
                model=alt_model,
                ngram_len=nlen,
            )
            alt_text = alt_gen.text
            alt_pub = _score_ids(alt_gen.token_ids, tok, nlen)
            alt_match = _score_ids(
                alt_gen.token_ids, tok, nlen, keys=alt_key_list
            )
        rows.append(
            PairRow(
                stem=stem,
                prompt=text,
                prompt_score=prompt_score,
                marked_text=marked_gen.text,
                marked_score=_score_ids(marked_gen.token_ids, tok, nlen),
                unmarked_text=unmarked_gen.text,
                unmarked_score=_score_ids(unmarked_gen.token_ids, tok, nlen),
                alt_text=alt_text,
                alt_score_public=alt_pub,
                alt_score_matching=alt_match,
                extra_marked=extra_marked,
                extra_unmarked=extra_unmarked,
            )
        )
        if persist is not None:
            persist_pair_row_texts(rows[-1], persist)
    return PairRun(
        rows=rows,
        max_new_tokens=max_new_tokens,
        seed=seed,
        alt_keys=alt_key_list,
        model_name=name,
        ngram_len=nlen,
    )


def run_control_only(
    prompts: list[tuple[str, str]],
    *,
    max_new_tokens: int = 128,
    seed: int = 0,
    n_samples: int = 1,
    model_name: str | None = None,
    tokenizer=None,
) -> PairRun:
    """Sample only control-shuffled-30 twins. Does not write *-marked.txt.

    Official public scores on these files should sit near chance. Matching
    control-key scores should sit with a known mark. blind ignores them.
    """
    if n_samples < 1:
        raise ValueError("n_samples must be >= 1")
    name = model_name or "gpt2"
    tok = tokenizer or load_tokenizer(name)
    device = torch.device("cpu") if is_gpt2_name(name) else generate_device()
    alt_key_list = control_keys()
    alt_model = _load_marked_model(device, keys=alt_key_list, model_name=name)
    rows: list[PairRow] = []
    for offset, (stem, prompt) in enumerate(prompts):
        text = prompt if prompt.endswith("\n") else prompt + "\n"
        prompt_score = official_score_text(text, tokenizer=tok)
        extra_control: list[tuple[str, OfficialScore, OfficialScore]] = []
        first_text = ""
        first_pub = None
        first_match = None
        for s_i in range(n_samples):
            gen = generate_text(
                text,
                marked=True,
                max_new_tokens=max_new_tokens,
                seed=seed + n_samples * offset + s_i,
                device=device,
                tokenizer=tok,
                model=alt_model,
            )
            pub = official_score_token_ids(gen.token_ids, tokenizer=tok)
            match = official_score_token_ids(
                gen.token_ids, tokenizer=tok, keys=alt_key_list
            )
            if s_i == 0:
                first_text = gen.text
                first_pub = pub
                first_match = match
            else:
                extra_control.append((gen.text, pub, match))
        rows.append(
            PairRow(
                stem=stem,
                prompt=text,
                prompt_score=prompt_score,
                marked_text="",
                marked_score=prompt_score,
                unmarked_text="",
                unmarked_score=prompt_score,
                alt_text=first_text,
                alt_score_public=first_pub,
                alt_score_matching=first_match,
                extra_control=extra_control,
            )
        )
    return PairRun(
        rows=rows,
        max_new_tokens=max_new_tokens,
        seed=seed,
        alt_keys=alt_key_list,
        model_name=name,
    )


def print_pair_run(run: PairRun) -> str:
    chunks: list[str] = []
    for row in run.rows:
        nlen = run.ngram_len
        chunks.append(
            format_score(f"{row.stem}-prompt", row.prompt_score, ngram_len=nlen)
        )
        if row.unmarked_text:
            chunks.append(
                format_score(
                    f"{row.stem}-unmarked-gen", row.unmarked_score, ngram_len=nlen
                )
            )
        if row.marked_text:
            chunks.append(
                format_score(f"{row.stem}-marked", row.marked_score, ngram_len=nlen)
            )
        if row.alt_score_public is not None and row.alt_score_matching is not None:
            chunks.append(
                format_score(
                    f"{row.stem}-control-gen",
                    row.alt_score_public,
                    instance=PUBLIC_INSTANCE,
                    ngram_len=nlen,
                )
            )
            chunks.append(
                format_score(
                    f"{row.stem}-control-gen",
                    row.alt_score_matching,
                    instance=CONTROL_INSTANCE,
                    ngram_len=nlen,
                )
            )
            for i, (_txt, pub, match) in enumerate(row.extra_control, start=2):
                chunks.append(
                    format_score(
                        f"{row.stem}-control-gen-{i}",
                        pub,
                        instance=PUBLIC_INSTANCE,
                        ngram_len=nlen,
                    )
                )
                chunks.append(
                    format_score(
                        f"{row.stem}-control-gen-{i}",
                        match,
                        instance=CONTROL_INSTANCE,
                        ngram_len=nlen,
                    )
                )
    return "\n".join(chunks)


def persist_pair_run(run: PairRun, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    table: dict = {
        "max_new_tokens": run.max_new_tokens,
        "seed": run.seed,
        "instance": PUBLIC_INSTANCE,
        "model_name": run.model_name,
        "ngram_len": run.ngram_len,
        "also_control_keys": run.alt_keys is not None,
        "control_only": bool(run.alt_keys is not None)
        and all(not row.marked_text for row in run.rows),
        "note": (
            "Marked and unmarked-gen are newly sampled tokens from the prompt. "
            "The prompt string itself is not stamped. "
            "*-control-gen.txt (if present) used control-shuffled-30 at sampling; "
            "not a *-marked.txt so blind ignore it."
        ),
        "rows": [],
    }
    md = [
        "# Same-prompt marked / unmarked twins",
        "",
        "The mark is applied at sampling time. The prompt is not stamped. "
        "`score` on `*-marked.txt` asks about *our* public key set.",
        "",
        "| Stem | Prompt mean | Unmarked-gen mean | Marked mean | "
        "Control-gen public | Control-gen matching | Gen n-grams |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in run.rows:
        persist_pair_row_texts(row, out_dir)
        rec: dict = {
            "stem": row.stem,
            "prompt": _score_to_dict(row.prompt_score),
            "unmarked_gen": _score_to_dict(row.unmarked_score),
            "marked": _score_to_dict(row.marked_score),
        }
        pub_s = ""
        match_s = ""
        if (
            row.alt_text
            and row.alt_score_public is not None
            and row.alt_score_matching is not None
        ):
            rec["control_gen_public"] = _score_to_dict(row.alt_score_public)
            rec["control_gen_matching"] = _score_to_dict(row.alt_score_matching)
            pub_s = f"{row.alt_score_public.mean:.6f}"
            match_s = f"{row.alt_score_matching.mean:.6f}"
            for i, (_txt, pub, match) in enumerate(row.extra_control, start=2):
                rec.setdefault("extra_control", []).append(
                    {
                        "sample": i,
                        "public": _score_to_dict(pub),
                        "matching": _score_to_dict(match),
                    }
                )
        table["rows"].append(rec)
        um = f"{row.unmarked_score.mean:.6f}" if row.unmarked_text else ""
        mk = f"{row.marked_score.mean:.6f}" if row.marked_text else ""
        md.append(
            f"| {row.stem} | {row.prompt_score.mean:.6f} | "
            f"{um} | {mk} | "
            f"{pub_s} | {match_s} | "
            f"{(row.marked_score.n_unmasked_ngrams if row.marked_text else row.alt_score_matching.n_unmasked_ngrams) if row.alt_score_matching is not None else 0} |"
        )
    md.append("")
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    (out_dir / "results.md").write_text("\n".join(md) + "\n")
    extra = ""
    control_only = bool(run.alt_keys is not None) and all(
        not row.marked_text for row in run.rows
    )
    if control_only:
        extra = (
            "`*-control-gen.txt` used `control-shuffled-30` at sampling. "
            "There is no `*-marked.txt`. `blind` does not load these files. "
            "Official public scores should sit near chance; matching control "
            "keys should sit with a known mark.\n\n"
        )
        title = "# Control-shuffled-30 twins (not public DeepMind 30)"
        body = (
            "Each `*-prompt.txt` is the seed. `*-control-gen.txt` is **new** "
            "text from GPT-2 + mixin with `control_keys()`. Not a public-key "
            "marked file."
        )
    else:
        if run.alt_keys is not None:
            extra = (
                "`*-control-gen.txt` is a third twin sampled with "
                "`control-shuffled-30`. `blind` does not load those files.\n\n"
            )
        title = "# Same-prompt twins (public DeepMind 30)"
        body = (
            "Each `*-prompt.txt` is the seed. `*-marked.txt` is **new** "
            "text from GPT-2 + mixin. `*-unmarked-gen.txt` is new text from "
            "the same prompt without the mixin."
        )
    (out_dir / "README.md").write_text(
        "\n".join(
            [
                title,
                "",
                body,
                "",
                extra,
                "Not a stamp on the same string. Not Claude. Not a remover.",
                "",
                "```bash",
                "python -m text_watermark_tools score .",
                "```",
                "",
            ]
        )
    )
