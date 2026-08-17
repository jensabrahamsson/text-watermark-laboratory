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
    official_score_text,
    official_score_token_ids,
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


@dataclass
class PairRun:
    rows: list[PairRow]
    max_new_tokens: int
    seed: int
    alt_keys: list[int] | None = None
    model_name: str = "gpt2"


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
) -> PairRun:
    """For each prompt: score the prompt, then generate unmarked and marked twins.

    When `also_control_keys` is set, a third twin is sampled with
    `control_keys()` (not a `-marked.txt` name — `blind` must not pick it up).
    Score uses the same tokenizer as the generator.
    """
    if n_samples < 1:
        raise ValueError("n_samples must be >= 1")
    name = model_name or "gpt2"
    tok = tokenizer or load_tokenizer(name)
    device = torch.device("cpu") if is_gpt2_name(name) else generate_device()
    if marked_model is None:
        marked_model = _load_marked_model(device, model_name=name)
    if unmarked_model is None:
        unmarked_model = _load_unmarked_model(device, model_name=name)
    alt_key_list = control_keys() if also_control_keys else None
    if also_control_keys and alt_model is None:
        alt_model = _load_marked_model(device, keys=alt_key_list, model_name=name)

    rows: list[PairRow] = []
    for offset, (stem, prompt) in enumerate(prompts):
        text = prompt if prompt.endswith("\n") else prompt + "\n"
        prompt_score = official_score_text(text, tokenizer=tok)
        stride = 2 * n_samples + 2
        marked_gen: Generation = generate_text(
            text,
            marked=True,
            max_new_tokens=max_new_tokens,
            seed=seed + stride * offset,
            device=device,
            tokenizer=tok,
            model=marked_model,
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
                (mg.text, official_score_token_ids(mg.token_ids, tokenizer=tok))
            )
            extra_unmarked.append(
                (ug.text, official_score_token_ids(ug.token_ids, tokenizer=tok))
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
            )
            alt_text = alt_gen.text
            alt_pub = official_score_token_ids(alt_gen.token_ids, tokenizer=tok)
            alt_match = official_score_token_ids(
                alt_gen.token_ids, tokenizer=tok, keys=alt_key_list
            )
        rows.append(
            PairRow(
                stem=stem,
                prompt=text,
                prompt_score=prompt_score,
                marked_text=marked_gen.text,
                marked_score=official_score_token_ids(
                    marked_gen.token_ids, tokenizer=tok
                ),
                unmarked_text=unmarked_gen.text,
                unmarked_score=official_score_token_ids(
                    unmarked_gen.token_ids, tokenizer=tok
                ),
                alt_text=alt_text,
                alt_score_public=alt_pub,
                alt_score_matching=alt_match,
                extra_marked=extra_marked,
                extra_unmarked=extra_unmarked,
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
        chunks.append(format_score(f"{row.stem}-prompt", row.prompt_score))
        chunks.append(format_score(f"{row.stem}-unmarked-gen", row.unmarked_score))
        chunks.append(format_score(f"{row.stem}-marked", row.marked_score))
        if row.alt_score_public is not None and row.alt_score_matching is not None:
            chunks.append(
                format_score(
                    f"{row.stem}-control-gen",
                    row.alt_score_public,
                    instance=PUBLIC_INSTANCE,
                )
            )
            chunks.append(
                format_score(
                    f"{row.stem}-control-gen",
                    row.alt_score_matching,
                    instance=CONTROL_INSTANCE,
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
        "ngram_len": 5,
        "also_control_keys": run.alt_keys is not None,
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
        (out_dir / f"{row.stem}-prompt.txt").write_text(row.prompt.rstrip() + "\n")
        (out_dir / f"{row.stem}-unmarked-gen.txt").write_text(
            row.unmarked_text.strip() + "\n"
        )
        (out_dir / f"{row.stem}-marked.txt").write_text(row.marked_text.strip() + "\n")
        for i, (txt, _sc) in enumerate(row.extra_marked, start=2):
            (out_dir / f"{row.stem}-marked-{i}.txt").write_text(txt.strip() + "\n")
        for i, (txt, _sc) in enumerate(row.extra_unmarked, start=2):
            (out_dir / f"{row.stem}-unmarked-gen-{i}.txt").write_text(
                txt.strip() + "\n"
            )
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
            (out_dir / f"{row.stem}-control-gen.txt").write_text(
                row.alt_text.strip() + "\n"
            )
            rec["control_gen_public"] = _score_to_dict(row.alt_score_public)
            rec["control_gen_matching"] = _score_to_dict(row.alt_score_matching)
            pub_s = f"{row.alt_score_public.mean:.6f}"
            match_s = f"{row.alt_score_matching.mean:.6f}"
        table["rows"].append(rec)
        md.append(
            f"| {row.stem} | {row.prompt_score.mean:.6f} | "
            f"{row.unmarked_score.mean:.6f} | {row.marked_score.mean:.6f} | "
            f"{pub_s} | {match_s} | "
            f"{row.marked_score.n_unmasked_ngrams} |"
        )
    md.append("")
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    (out_dir / "results.md").write_text("\n".join(md) + "\n")
    extra = ""
    if run.alt_keys is not None:
        extra = (
            "`*-control-gen.txt` is a third twin sampled with "
            "`control-shuffled-30`. `blind` does not load those files.\n\n"
        )
    (out_dir / "README.md").write_text(
        "\n".join(
            [
                "# Same-prompt twins (public DeepMind 30)",
                "",
                "Each `*-prompt.txt` is the seed. `*-marked.txt` is **new** "
                "text from GPT-2 + mixin. `*-unmarked-gen.txt` is new text from "
                "the same prompt without the mixin.",
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
