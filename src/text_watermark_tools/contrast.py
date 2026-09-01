"""Key-free instance contrast: public-key twins vs control-shuffled sampling.

Fit marked/unmarked tables on the public DeepMind instance only. Score a
third pile sampled with `control_keys()` (same tournament mixin, different
keys). The official detector is instance-specific. This asks whether the
*key-free* reader is too, without reconstructing those keys.

Control files are `*-control-gen.txt`. They are never a `*-marked.txt`, so
`blind` / `indicate fit` do not train on them.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

from text_watermark_tools.blind import Twin, clip_twins_prefix, load_twins
from text_watermark_tools.indicator import CAVEAT, IndicatorHoldout
from text_watermark_tools.probe import (
    POS_SPECS,
    TransferRun,
    _append_pair,
    _empty_holdout_parts,
    _holdout_from_parts,
    apply_overlap,
    persist_transfer,
    print_transfer,
    score_twins,
    summarize_holdout,
)
from text_watermark_tools.rankpath import RANKPATH_SPECS
from text_watermark_tools.score import load_tokenizer
from text_watermark_tools.stats import binary_eval, binary_eval_to_dict, format_binary_eval
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    fit_count_model,
    fit_hashpool_twins,
    score_hashpool,
    score_sequence,
)

CONTROL_RE = re.compile(r"^(.+)-control-gen(?:-(\d+))?\.txt$")
CONTRAST_NOTE = (
    "Tables fit on public-key marked vs unmarked only. Control-gen used "
    "control-shuffled-30 at sampling. If control ranks with unmarked, the "
    "key-free reader is instance-specific without keys. If it ranks with "
    "marked, the reader is detecting tournament sampling, not this instance. "
    "Not key recovery. Not Claude."
)


@dataclass
class ControlDraw:
    stem: str
    sample: int
    ids: list[int]
    text: str


def load_control_draws(pair_dir: Path, *, tokenizer=None) -> list[ControlDraw]:
    """Load *-control-gen.txt draws. Not marked files; blind ignores them."""
    pair_dir = Path(pair_dir)
    tok = tokenizer or load_tokenizer()
    grouped: dict[str, dict[int, Path]] = {}
    for path in pair_dir.glob("*-control-gen*.txt"):
        m = CONTROL_RE.fullmatch(path.name)
        if not m:
            continue
        stem, idx = m.group(1), int(m.group(2) or 1)
        grouped.setdefault(stem, {})[idx] = path
    out: list[ControlDraw] = []
    for stem in sorted(grouped):
        for idx in sorted(grouped[stem]):
            text = grouped[stem][idx].read_text()
            out.append(
                ControlDraw(
                    stem=stem,
                    sample=idx,
                    ids=tok(text)["input_ids"],
                    text=text,
                )
            )
    return out


def collect_control_matrices(
    draws: Sequence[ControlDraw],
    model,
    *,
    top_k: int = 40,
    prompt_ids_by_stem: dict[str, Sequence[int]] | None = None,
    prompt_context: bool = False,
):
    """Unmarked-LM choice matrices for *-control-gen.txt. No watermark keys."""
    from text_watermark_tools.pivot import extract_choice_matrix

    out = {}
    for draw in draws:
        prefix: Sequence[int] = ()
        if prompt_context:
            if not prompt_ids_by_stem or draw.stem not in prompt_ids_by_stem:
                raise ValueError(
                    f"prompt-context contrast needs prompt token ids on stem {draw.stem!r}"
                )
            prefix = tuple(int(x) for x in prompt_ids_by_stem[draw.stem])
        out[(draw.stem, draw.sample, "control")] = extract_choice_matrix(
            draw.ids, model, top_k=top_k, prefix=prefix
        )
    return out


def clip_control_draws(draws: Sequence[ControlDraw], n: int) -> list[ControlDraw]:
    if n <= 0:
        return list(draws)
    return [
        ControlDraw(d.stem, d.sample, list(d.ids[:n]), d.text) for d in draws
    ]


def _holdout_from_scores(
    rows: list[tuple[str, int, float, float]],
    *,
    context_len: int,
    model_name: str,
    instance: str,
    score_kind: str,
) -> IndicatorHoldout:
    parts = _empty_holdout_parts()
    for stem, sample, pos, neg in rows:
        _append_pair(parts, stem, sample, pos, neg)
    return _holdout_from_parts(
        parts,
        context_len=context_len,
        model_name=model_name,
        instance=instance,
        score_kind=score_kind,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        mode="contrast",
    )


def _index_unmarked(twins: Sequence[Twin]) -> dict[tuple[str, int], list[int]]:
    out: dict[tuple[str, int], list[int]] = {}
    for twin in twins:
        for i, seq in enumerate(twin.unmarked_seqs()):
            out[(twin.stem, i + 1)] = list(seq)
    return out


def _index_marked(twins: Sequence[Twin]) -> dict[tuple[str, int], list[int]]:
    out: dict[tuple[str, int], list[int]] = {}
    for twin in twins:
        for i, seq in enumerate(twin.marked_seqs()):
            out[(twin.stem, i + 1)] = list(seq)
    return out


def logodds_brier(positive: Sequence[float], negative: Sequence[float]) -> float:
    """Brier score treating each value as a log-odds for P(marked)."""
    import math

    def p(s: float) -> float:
        x = max(min(float(s), 40.0), -40.0)
        return 1.0 / (1.0 + math.exp(-x))

    total = 0.0
    n = 0
    for s in positive:
        total += (p(s) - 1.0) ** 2
        n += 1
    for s in negative:
        total += (p(s) - 0.0) ** 2
        n += 1
    if n == 0:
        return float("nan")
    return total / n


@dataclass
class ContrastPair:
    name: str
    comparison: str
    holdout: IndicatorHoldout
    brier: float


@dataclass
class ContrastRun:
    methods: list[ContrastPair] = field(default_factory=list)
    transfer: TransferRun | None = None
    train_dir: str = ""
    test_dir: str = ""
    control_dir: str = ""
    n_control: int = 0
    n_aligned: int = 0
    used_keys: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False
    fit_prefix: int | None = None
    rankpath_pos_bucket: int | None = None
    rankpath_end: int | None = None
    rankpath_model: object | None = None
    note: str = CONTRAST_NOTE


def run_instance_contrast(
    train_twins: Sequence[Twin],
    test_twins: Sequence[Twin],
    control_draws: Sequence[ControlDraw],
    *,
    train_dir: str = "",
    test_dir: str = "",
    control_dir: str = "",
    model_name: str = "gpt2",
    context_len: int = 4,
    fit_prefix: int | None = None,
    position_bucket: int = 1,
    methods: Sequence[str] = ("hits", "poshits", "hashpool"),
    rankpath_pos_bucket: int | None = None,
    rankpath_end: int | None = None,
    prompt_context: bool = False,
    lm=None,
    rankpath_symbols: dict | None = None,
) -> ContrastRun:
    """Fit on public twins; score public test and control-gen. No keys in the fit."""
    train, test, _overlap = apply_overlap(
        train_twins, test_twins, mode="drop-from-train"
    )
    prefix_n = int(fit_prefix) if fit_prefix and fit_prefix > 0 else 0
    if prefix_n:
        train = clip_twins_prefix(train, prefix_n)
        test = clip_twins_prefix(test, prefix_n)
        control_draws = clip_control_draws(control_draws, prefix_n)
    if len(train) < 1:
        raise ValueError("instance contrast left no training prompts")
    if len(test) < 1:
        raise ValueError("instance contrast left no test prompts")
    if not control_draws:
        raise ValueError("instance contrast needs *-control-gen.txt draws")
    names = list(methods)
    pos_bucket = int(position_bucket) if position_bucket and position_bucket > 0 else 0
    count_names = [n for n in names if n in COUNT_SPECS]
    pos_names = [n for n in names if n in POS_SPECS]
    rank_names = [n for n in names if n in RANKPATH_SPECS]
    count_model = None
    pos_model = None
    hash_model = None
    rank_model = None
    if count_names:
        count_model = fit_count_model(train, context_len=context_len)
    if pos_names:
        pos_model = fit_count_model(
            train, context_len=context_len, position_bucket=pos_bucket
        )
    if "hashpool" in names:
        hash_model = fit_hashpool_twins(train, context_len=context_len)
    for model in (count_model, pos_model, hash_model):
        if model is not None and (
            model.used_keys or model.used_hash_iv or model.used_g_values
        ):
            raise RuntimeError("instance contrast consulted keys / hash_iv / g-values")

    if rankpath_pos_bucket is None:
        rank_bucket = pos_bucket
    else:
        rank_bucket = int(rankpath_pos_bucket) if rankpath_pos_bucket > 0 else 0
    rank_end = int(rankpath_end) if rankpath_end and int(rankpath_end) > 0 else None
    symbols: dict = {}
    if rank_names:
        from text_watermark_tools.rankpath import (
            fit_rankpath_from_symbols,
            slice_symbols,
            symbols_from_matrices,
        )

        if rankpath_symbols is not None:
            symbols = dict(rankpath_symbols)
        else:
            from text_watermark_tools.generate import (
                _load_unmarked_model,
                generate_device,
            )
            from text_watermark_tools.pivot import collect_choice_matrices

            if lm is None:
                lm = _load_unmarked_model(generate_device(), model_name=model_name)
            train_mats = collect_choice_matrices(
                train, lm, prompt_context=prompt_context
            )
            test_mats = collect_choice_matrices(
                test, lm, prompt_context=prompt_context
            )
            prompt_ids = {t.stem: t.prompt_ids for t in test}
            control_mats = collect_control_matrices(
                control_draws,
                lm,
                prompt_ids_by_stem=prompt_ids,
                prompt_context=prompt_context,
            )
            symbols = {
                **symbols_from_matrices(train_mats),
                **symbols_from_matrices(test_mats),
                **symbols_from_matrices(control_mats),
            }
        if rank_end is not None:
            symbols = slice_symbols(symbols, 0, rank_end)
        train_stems = [t.stem for t in train]
        train_sym = {
            key: ids
            for key, ids in symbols.items()
            if key[0] in train_stems and key[2] in ("marked", "unmarked")
        }
        rank_model = fit_rankpath_from_symbols(
            train_sym,
            train_stems,
            context_len=min(int(context_len), 3),
            position_bucket=rank_bucket,
        )
        if rank_model.used_keys or rank_model.used_hash_iv or rank_model.used_g_values:
            raise RuntimeError("instance contrast consulted keys / hash_iv / g-values")

    scorers = {}
    for name in count_names:
        spec = COUNT_SPECS[name]
        assert count_model is not None
        scorers[name] = (
            lambda ids, m=count_model, s=spec: score_sequence(ids, m, s),
            spec.instance,
        )
    for name in pos_names:
        spec = POS_SPECS[name]
        assert pos_model is not None
        scorers[name] = (
            lambda ids, m=pos_model, s=spec: score_sequence(ids, m, s),
            spec.instance,
        )
    if "hashpool" in names and hash_model is not None:
        scorers["hashpool"] = (
            lambda ids, m=hash_model: score_hashpool(ids, m),
            "key-free-hashpool",
        )
    unknown = [
        n
        for n in names
        if n not in scorers and n not in RANKPATH_SPECS
    ]
    if unknown:
        raise ValueError(
            "unknown contrast methods: "
            + ", ".join(unknown)
            + "; choose hits, tokhits, tokbackoff, tokbackoff2, poshits, "
            "postokhits, postokbackoff, postokbackoff2, hashpool, "
            "rankpath, rankuni, rankhits, "
            f"or one of {sorted(COUNT_SPECS) + sorted(POS_SPECS)}"
        )
    if not scorers and not rank_names:
        raise ValueError("instance contrast needs at least one scorer")

    unmarked = _index_unmarked(test)
    marked = _index_marked(test)
    n_aligned = sum(1 for d in control_draws if (d.stem, d.sample) in unmarked)
    if n_aligned < 1:
        raise ValueError(
            "no control-gen draws aligned with test unmarked (stem, sample). "
            "Check *-control-gen.txt names against *-unmarked-gen.txt."
        )
    run = ContrastRun(
        train_dir=train_dir,
        test_dir=test_dir,
        control_dir=control_dir,
        n_control=len(control_draws),
        n_aligned=n_aligned,
        fit_prefix=prefix_n or None,
        rankpath_pos_bucket=rank_bucket if rank_names else None,
        rankpath_end=rank_end,
        rankpath_model=rank_model,
    )
    transfer = TransferRun(
        train_dir=train_dir,
        test_dir=test_dir,
        n_train_prompts=len(train),
        n_test_prompts=len(test),
        overlap_mode="drop-from-train",
        model_name=model_name,
        context_len=context_len,
        fit_prefix=prefix_n or None,
        position_bucket=pos_bucket,
        rankpath_pos_bucket=rank_bucket if rank_names else None,
        note=CONTRAST_NOTE,
    )
    for name, (scorer, instance) in scorers.items():
        public = score_twins(
            test,
            scorer,
            context_len=context_len,
            model_name=model_name,
            instance=instance,
            score_kind=name,
            seq_mode="ids",
        )
        transfer.methods.append(summarize_holdout(name, public))
        cu_rows: list[tuple[str, int, float, float]] = []
        pc_rows: list[tuple[str, int, float, float]] = []
        for draw in control_draws:
            key = (draw.stem, draw.sample)
            if key not in unmarked:
                continue
            c_lr = float(scorer(draw.ids))
            u_lr = float(scorer(unmarked[key]))
            cu_rows.append((draw.stem, draw.sample, c_lr, u_lr))
            if key in marked:
                pc_rows.append(
                    (draw.stem, draw.sample, float(scorer(marked[key])), c_lr)
                )
        if cu_rows:
            cu = _holdout_from_scores(
                cu_rows,
                context_len=context_len,
                model_name=model_name,
                instance=instance,
                score_kind=f"{name}-control-vs-unmarked",
            )
            run.methods.append(
                ContrastPair(
                    name=name,
                    comparison="control-vs-unmarked",
                    holdout=cu,
                    brier=logodds_brier(cu.marked_lrs, cu.unmarked_lrs),
                )
            )
        if pc_rows:
            pc = _holdout_from_scores(
                pc_rows,
                context_len=context_len,
                model_name=model_name,
                instance=instance,
                score_kind=f"{name}-public-vs-control",
            )
            run.methods.append(
                ContrastPair(
                    name=name,
                    comparison="public-vs-control",
                    holdout=pc,
                    brier=logodds_brier(pc.marked_lrs, pc.unmarked_lrs),
                )
            )
        run.methods.append(
            ContrastPair(
                name=name,
                comparison="public-vs-unmarked",
                holdout=public,
                brier=logodds_brier(public.marked_lrs, public.unmarked_lrs),
            )
        )
    if rank_names:
        from text_watermark_tools.rankpath import score_rankpath

        assert rank_model is not None
        for name in rank_names:
            spec = RANKPATH_SPECS[name]
            instance = spec.instance

            def _lr(stem: str, sample: int, side: str, m=rank_model, s=spec) -> float:
                return float(
                    score_rankpath(symbols.get((stem, sample, side), []), m, spec=s)
                )

            pub_rows: list[tuple[str, int, float, float]] = []
            for twin in test:
                n = min(len(twin.marked_seqs()), len(twin.unmarked_seqs()))
                for i in range(n):
                    sample = i + 1
                    pub_rows.append(
                        (
                            twin.stem,
                            sample,
                            _lr(twin.stem, sample, "marked"),
                            _lr(twin.stem, sample, "unmarked"),
                        )
                    )
            public = _holdout_from_scores(
                pub_rows,
                context_len=min(int(context_len), 3),
                model_name=model_name,
                instance=instance,
                score_kind=name,
            )
            transfer.methods.append(summarize_holdout(name, public))
            cu_rows = []
            pc_rows = []
            for draw in control_draws:
                key = (draw.stem, draw.sample)
                if key not in unmarked:
                    continue
                c_lr = _lr(draw.stem, draw.sample, "control")
                u_lr = _lr(draw.stem, draw.sample, "unmarked")
                cu_rows.append((draw.stem, draw.sample, c_lr, u_lr))
                if key in marked:
                    pc_rows.append(
                        (draw.stem, draw.sample, _lr(draw.stem, draw.sample, "marked"), c_lr)
                    )
            if cu_rows:
                cu = _holdout_from_scores(
                    cu_rows,
                    context_len=min(int(context_len), 3),
                    model_name=model_name,
                    instance=instance,
                    score_kind=f"{name}-control-vs-unmarked",
                )
                run.methods.append(
                    ContrastPair(
                        name=name,
                        comparison="control-vs-unmarked",
                        holdout=cu,
                        brier=logodds_brier(cu.marked_lrs, cu.unmarked_lrs),
                    )
                )
            if pc_rows:
                pc = _holdout_from_scores(
                    pc_rows,
                    context_len=min(int(context_len), 3),
                    model_name=model_name,
                    instance=instance,
                    score_kind=f"{name}-public-vs-control",
                )
                run.methods.append(
                    ContrastPair(
                        name=name,
                        comparison="public-vs-control",
                        holdout=pc,
                        brier=logodds_brier(pc.marked_lrs, pc.unmarked_lrs),
                    )
                )
            run.methods.append(
                ContrastPair(
                    name=name,
                    comparison="public-vs-unmarked",
                    holdout=public,
                    brier=logodds_brier(public.marked_lrs, public.unmarked_lrs),
                )
            )
    run.transfer = transfer
    run.used_keys = any(m.holdout.used_keys for m in run.methods)
    run.used_hash_iv = any(m.holdout.used_hash_iv for m in run.methods)
    run.used_g_values = any(m.holdout.used_g_values for m in run.methods)
    return run


def print_contrast(run: ContrastRun) -> str:
    lines = [
        (
            f"instance-contrast n_rows={len(run.methods)} train={run.train_dir} "
            f"test={run.test_dir} control={run.control_dir} "
            f"n_control={run.n_control} n_aligned={run.n_aligned} "
            f"fit_prefix={run.fit_prefix} "
            f"rankpath_pos_bucket={run.rankpath_pos_bucket} "
            f"rankpath_end={run.rankpath_end} used_keys={run.used_keys}"
        ),
        run.note,
        CAVEAT,
        "",
        (
            "| method | comparison | prompt wins | file auc | pos>0 | "
            "neg<=0 | perm p | brier |"
        ),
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in run.methods:
        b = binary_eval(row.holdout.marked_lrs, row.holdout.unmarked_lrs)
        lines.append(
            f"| {row.name} | {row.comparison} | "
            f"{row.holdout.n_prompts_marked_above}/{row.holdout.n_prompts} | "
            f"{b.auc:.3f} | {b.n_positive_above_zero}/{b.n_positive} | "
            f"{b.n_negative_at_most_zero}/{b.n_negative} | "
            f"{b.permutation_p:.4g} | {row.brier:.4f} |"
        )
    lines.append("")
    lines.append(
        "public-vs-unmarked: can the key-free reader still see the public mark. "
        "control-vs-unmarked: does a *different* key instance look marked. "
        "public-vs-control: can it tell the two instances apart. "
        "pos is the first class in each name (control, public, public)."
    )
    lines.append("")
    for row in run.methods:
        lines.append(
            format_binary_eval(
                binary_eval(row.holdout.marked_lrs, row.holdout.unmarked_lrs),
                label=f"{row.name} {row.comparison}",
            )
            + f" brier={row.brier:.4f} "
            f"prompts={row.holdout.n_prompts_marked_above}/{row.holdout.n_prompts}"
        )
    if run.transfer is not None:
        lines.append("")
        lines.append(print_transfer(run.transfer))
    return "\n".join(lines)


def persist_contrast(run: ContrastRun, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    table = {
        "train_dir": run.train_dir,
        "test_dir": run.test_dir,
        "control_dir": run.control_dir,
        "n_control": run.n_control,
        "n_aligned": run.n_aligned,
        "fit_prefix": run.fit_prefix,
        "rankpath_pos_bucket": run.rankpath_pos_bucket,
        "rankpath_end": run.rankpath_end,
        "used_keys": run.used_keys,
        "used_hash_iv": run.used_hash_iv,
        "used_g_values": run.used_g_values,
        "note": run.note,
        "caveat": CAVEAT,
        "methods": [],
    }
    from text_watermark_tools.indicator import persist_holdout

    for row in run.methods:
        slug = f"{row.name}-{row.comparison}"
        persist_holdout(row.holdout, out_dir / slug)
        table["methods"].append(
            {
                "name": row.name,
                "comparison": row.comparison,
                "n_prompt_wins": row.holdout.n_prompts_marked_above,
                "n_prompts": row.holdout.n_prompts,
                "brier": row.brier,
                "binary": binary_eval_to_dict(
                    binary_eval(row.holdout.marked_lrs, row.holdout.unmarked_lrs)
                ),
                "used_keys": row.holdout.used_keys,
            }
        )
    if run.transfer is not None:
        persist_transfer(run.transfer, out_dir / "public-transfer")
    if run.rankpath_model is not None:
        from text_watermark_tools.rankpath import persist_rankpath

        persist_rankpath(
            run.rankpath_model,
            out_dir / "tables-rankpath",
            model_name=run.transfer.model_name if run.transfer is not None else "gpt2",
            pair_dir=run.train_dir,
            n_train_prompts=run.transfer.n_train_prompts if run.transfer is not None else 0,
            spec_name="rankpath",
        )
    body = "# Key-free instance contrast\n\n" + print_contrast(run) + "\n"
    (out_dir / "README.md").write_text(body)
    (out_dir / "results.md").write_text(body)
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
