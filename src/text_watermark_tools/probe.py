"""Compare key-free scorers on matched twins, plus an argmax-snap scrub.

`probe` is a laboratory comparison, not a production detector. Every method
sets used_keys / used_hash_iv / used_g_values to false. The official
`score` path is used only afterwards, as a reference check that a scrub
moved a known public mark toward chance.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence

from text_watermark_tools.blind import Twin
from text_watermark_tools.indicator import (
    CAVEAT,
    IndicatorHoldout,
    persist_holdout,
)
from text_watermark_tools.stats import (
    binary_eval,
    binary_eval_to_dict,
    counts_at_threshold,
    format_binary_eval,
)
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    fit_count_model,
    fit_hashpool_twins,
    score_hashpool,
    score_hashpool_vote,
    score_hybrid,
    score_sequence,
)

ScoreFn = Callable[[Sequence[int]], float]


def _empty_holdout_parts() -> dict:
    return {"stems": [], "samples": [], "marked": [], "unmarked": []}


def _holdout_from_parts(
    parts: dict,
    *,
    context_len: int,
    model_name: str,
    instance: str,
    score_kind: str,
    used_keys: bool = False,
    used_hash_iv: bool = False,
    used_g_values: bool = False,
    margin: float = 0.0,
    mode: str = "rotate",
) -> IndicatorHoldout:
    return IndicatorHoldout(
        stems=parts["stems"],
        marked_lrs=parts["marked"],
        unmarked_lrs=parts["unmarked"],
        used_keys=used_keys,
        used_hash_iv=used_hash_iv,
        used_g_values=used_g_values,
        context_len=context_len,
        model_name=model_name,
        samples=parts["samples"],
        mode=mode,
        margin=margin,
        instance=instance,
        score_kind=score_kind,
    )


def _append_pair(parts: dict, stem: str, sample: int, marked: float, unmarked: float) -> None:
    parts["stems"].append(stem)
    parts["samples"].append(sample)
    parts["marked"].append(marked)
    parts["unmarked"].append(unmarked)


def rotate_custom(
    twins: Sequence[Twin],
    make_scorer: Callable[[Sequence[Twin]], tuple[ScoreFn, bool, bool, bool]],
    *,
    context_len: int,
    model_name: str,
    instance: str,
    score_kind: str,
    margin: float = 0.0,
) -> IndicatorHoldout:
    if len(twins) < 3:
        raise ValueError("rotate probe needs at least three prompts")
    parts = _empty_holdout_parts()
    used_keys = used_hash = used_g = False
    for held in twins:
        train = [t for t in twins if t.stem != held.stem]
        scorer, k, h, g = make_scorer(train)
        used_keys = used_keys or k
        used_hash = used_hash or h
        used_g = used_g or g
        marked_seqs = held.marked_seqs()
        unmarked_seqs = held.unmarked_seqs()
        n = min(len(marked_seqs), len(unmarked_seqs))
        for i in range(n):
            _append_pair(
                parts,
                held.stem,
                i + 1,
                scorer(marked_seqs[i]),
                scorer(unmarked_seqs[i]),
            )
    return _holdout_from_parts(
        parts,
        context_len=context_len,
        model_name=model_name,
        instance=instance,
        score_kind=score_kind,
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
        margin=margin,
    )


def rotate_count_methods(
    twins: Sequence[Twin],
    *,
    methods: Sequence[str] | None = None,
    context_len: int = 4,
    model_name: str = "gpt2",
    margin: float = 0.0,
) -> dict[str, IndicatorHoldout]:
    names = list(methods or COUNT_SPECS.keys())
    unknown = [n for n in names if n not in COUNT_SPECS]
    if unknown:
        raise ValueError(f"unknown count methods: {unknown}")
    buckets = {name: _empty_holdout_parts() for name in names}
    used = {name: (False, False, False) for name in names}
    for held in twins:
        train = [t for t in twins if t.stem != held.stem]
        model = fit_count_model(train, context_len=context_len)
        flags = (model.used_keys, model.used_hash_iv, model.used_g_values)
        marked_seqs = held.marked_seqs()
        unmarked_seqs = held.unmarked_seqs()
        n = min(len(marked_seqs), len(unmarked_seqs))
        for name in names:
            spec = COUNT_SPECS[name]
            used[name] = tuple(a or b for a, b in zip(used[name], flags, strict=True))
            for i in range(n):
                _append_pair(
                    buckets[name],
                    held.stem,
                    i + 1,
                    score_sequence(marked_seqs[i], model, spec),
                    score_sequence(unmarked_seqs[i], model, spec),
                )
    out: dict[str, IndicatorHoldout] = {}
    for name in names:
        spec = COUNT_SPECS[name]
        k, h, g = used[name]
        out[name] = _holdout_from_parts(
            buckets[name],
            context_len=context_len,
            model_name=model_name,
            instance=spec.instance,
            score_kind=name,
            used_keys=k,
            used_hash_iv=h,
            used_g_values=g,
            margin=margin,
        )
    return out


def rotate_hashpool(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
) -> IndicatorHoldout:
    def make(train: Sequence[Twin]):
        model = fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
        return (
            lambda ids, m=model: score_hashpool(ids, m),
            model.used_keys,
            model.used_hash_iv,
            model.used_g_values,
        )

    return rotate_custom(
        twins,
        make,
        context_len=context_len,
        model_name=model_name,
        instance="key-free-hashpool",
        score_kind="hashpool",
        margin=margin,
    )


def rotate_hashvote(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
) -> IndicatorHoldout:
    def make(train: Sequence[Twin]):
        model = fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
        return (
            lambda ids, m=model: score_hashpool_vote(ids, m),
            model.used_keys,
            model.used_hash_iv,
            model.used_g_values,
        )

    return rotate_custom(
        twins,
        make,
        context_len=context_len,
        model_name=model_name,
        instance="key-free-hashvote",
        score_kind="hashvote",
        margin=margin,
    )


def rotate_hybrid(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
) -> IndicatorHoldout:
    def make(train: Sequence[Twin]):
        counts = fit_count_model(train, context_len=context_len)
        hashed = fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
        used = (
            counts.used_keys or hashed.used_keys,
            counts.used_hash_iv or hashed.used_hash_iv,
            counts.used_g_values or hashed.used_g_values,
        )
        return (
            lambda ids, c=counts, h=hashed: score_hybrid(ids, c, h),
            used[0],
            used[1],
            used[2],
        )

    return rotate_custom(
        twins,
        make,
        context_len=context_len,
        model_name=model_name,
        instance="key-free-hybrid",
        score_kind="hybrid",
        margin=margin,
    )


def _aligned_rows(ev: IndicatorHoldout) -> list[tuple[str, int, float, float]]:
    return sorted(
        zip(ev.stems, ev._samples(), ev.marked_lrs, ev.unmarked_lrs, strict=True),
        key=lambda row: (row[0], row[1]),
    )


def rotate_score_stack(
    holdouts: Sequence[IndicatorHoldout],
    *,
    model_name: str = "gpt2",
    score_kind: str = "stack",
    instance: str = "key-free-stack",
) -> IndicatorHoldout:
    """Leave-one-prompt-out Fisher LDA on already-computed file scores.

    Each holdout must cover the same (stem, sample) pairs. Weights are fit
    without the held prompt. Still no keys / hash_iv / g-values.
    """
    if len(holdouts) < 2:
        raise ValueError("score stack needs at least two methods")
    series = [_aligned_rows(ev) for ev in holdouts]
    n = len(series[0])
    if n == 0 or any(len(s) != n for s in series):
        raise ValueError("stacked holdouts have different lengths")
    keys = [(row[0], row[1]) for row in series[0]]
    for other in series[1:]:
        if [(row[0], row[1]) for row in other] != keys:
            raise ValueError("stacked holdouts are not aligned")
    import numpy as np
    from text_watermark_tools.pivot import fisher_lda, lda_score

    stems_unique: list[str] = []
    seen: set[str] = set()
    for stem, _sample, _m, _u in series[0]:
        if stem not in seen:
            seen.add(stem)
            stems_unique.append(stem)
    parts = _empty_holdout_parts()
    for held in stems_unique:
        train_m: list[list[float]] = []
        train_u: list[list[float]] = []
        held_idx: list[int] = []
        for i, (stem, _sample, _m, _u) in enumerate(series[0]):
            vec_m = [s[i][2] for s in series]
            vec_u = [s[i][3] for s in series]
            if stem == held:
                held_idx.append(i)
            else:
                train_m.append(vec_m)
                train_u.append(vec_u)
        if len(train_m) < 2 or not held_idx:
            continue
        weights, midpoint = fisher_lda(
            np.asarray(train_m, dtype=np.float64),
            np.asarray(train_u, dtype=np.float64),
        )
        for i in held_idx:
            stem, sample, _m, _u = series[0][i]
            vm = np.asarray([s[i][2] for s in series], dtype=np.float64)
            vu = np.asarray([s[i][3] for s in series], dtype=np.float64)
            _append_pair(
                parts,
                stem,
                sample,
                lda_score(vm, weights, midpoint),
                lda_score(vu, weights, midpoint),
            )
    used_keys = any(ev.used_keys for ev in holdouts)
    used_hash = any(ev.used_hash_iv for ev in holdouts)
    used_g = any(ev.used_g_values for ev in holdouts)
    return _holdout_from_parts(
        parts,
        context_len=0,
        model_name=model_name,
        instance=instance,
        score_kind=score_kind,
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
        mode="rotate",
    )


def apply_overlap(
    train: Sequence[Twin],
    test: Sequence[Twin],
    mode: str = "drop-from-train",
) -> tuple[list[Twin], list[Twin], list[str]]:
    """Remove shared prompt stems so a transfer test is out of family.

    drop-from-train: keep the test set, strip those stems from training.
    drop-from-test: keep training, strip those stems from the test set.
    """
    train_stems = {t.stem for t in train}
    test_stems = {t.stem for t in test}
    overlap = sorted(train_stems & test_stems)
    if mode == "drop-from-train":
        kept_train = [t for t in train if t.stem not in test_stems]
        return kept_train, list(test), overlap
    if mode == "drop-from-test":
        kept_test = [t for t in test if t.stem not in train_stems]
        return list(train), kept_test, overlap
    if mode == "keep":
        return list(train), list(test), overlap
    raise ValueError(
        f"unknown overlap mode {mode!r}; "
        "use drop-from-train, drop-from-test, or keep"
    )


def score_twins(
    twins: Sequence[Twin],
    scorer: ScoreFn,
    *,
    context_len: int,
    model_name: str,
    instance: str,
    score_kind: str,
    used_keys: bool = False,
    used_hash_iv: bool = False,
    used_g_values: bool = False,
    mode: str = "transfer",
) -> IndicatorHoldout:
    parts = _empty_holdout_parts()
    for twin in twins:
        marked_seqs = twin.marked_seqs()
        unmarked_seqs = twin.unmarked_seqs()
        n = min(len(marked_seqs), len(unmarked_seqs))
        for i in range(n):
            _append_pair(
                parts,
                twin.stem,
                i + 1,
                scorer(marked_seqs[i]),
                scorer(unmarked_seqs[i]),
            )
    return _holdout_from_parts(
        parts,
        context_len=context_len,
        model_name=model_name,
        instance=instance,
        score_kind=score_kind,
        used_keys=used_keys,
        used_hash_iv=used_hash_iv,
        used_g_values=used_g_values,
        mode=mode,
    )


def rotate_pivot(
    twins: Sequence[Twin],
    *,
    model_name: str = "gpt2",
    top_k: int = 40,
    margin: float = 0.0,
    lm: object | None = None,
) -> dict[str, IndicatorHoldout]:
    """Leave-one-prompt-out LDA and rank baseline on unmarked-LM features."""
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.pivot import (
        extract_choice_vector,
        fit_pivot,
        score_pivot_lda,
        score_pivot_rank,
    )

    if lm is None:
        lm = _load_unmarked_model(generate_device(), model_name=model_name)

    marked_vecs: dict[tuple[str, int], object] = {}
    unmarked_vecs: dict[tuple[str, int], object] = {}
    for twin in twins:
        for i, ids in enumerate(twin.marked_seqs()):
            marked_vecs[(twin.stem, i + 1)] = extract_choice_vector(
                ids, lm, top_k=top_k
            )
        for i, ids in enumerate(twin.unmarked_seqs()):
            unmarked_vecs[(twin.stem, i + 1)] = extract_choice_vector(
                ids, lm, top_k=top_k
            )

    lda_parts = _empty_holdout_parts()
    rank_parts = _empty_holdout_parts()
    used_keys = used_hash = used_g = False
    import numpy as np

    for held in twins:
        train_m = []
        train_u = []
        for twin in twins:
            if twin.stem == held.stem:
                continue
            n = min(len(twin.marked_seqs()), len(twin.unmarked_seqs()))
            for i in range(n):
                train_m.append(marked_vecs[(twin.stem, i + 1)])
                train_u.append(unmarked_vecs[(twin.stem, i + 1)])
        fit = fit_pivot(np.stack(train_m), np.stack(train_u))
        used_keys = used_keys or fit.used_keys
        used_hash = used_hash or fit.used_hash_iv
        used_g = used_g or fit.used_g_values
        n = min(len(held.marked_seqs()), len(held.unmarked_seqs()))
        for i in range(n):
            sample = i + 1
            vm = marked_vecs[(held.stem, sample)]
            vu = unmarked_vecs[(held.stem, sample)]
            _append_pair(
                lda_parts,
                held.stem,
                sample,
                score_pivot_lda(vm, fit),
                score_pivot_lda(vu, fit),
            )
            _append_pair(
                rank_parts,
                held.stem,
                sample,
                score_pivot_rank(vm, fit),
                score_pivot_rank(vu, fit),
            )
    ctx = 0
    flags = dict(
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
        margin=margin,
        model_name=model_name,
        context_len=ctx,
    )
    return {
        "pivot-lda": _holdout_from_parts(
            lda_parts,
            instance="key-free-pivot-lda",
            score_kind="pivot-lda",
            **flags,
        ),
        "pivot-rank": _holdout_from_parts(
            rank_parts,
            instance="key-free-pivot-rank",
            score_kind="pivot-rank",
            **flags,
        ),
    }


@dataclass
class MethodSummary:
    name: str
    holdout: IndicatorHoldout
    binary: object
    n_prompt_wins: int
    n_prompts: int


@dataclass
class ProbeRun:
    methods: list[MethodSummary] = field(default_factory=list)
    pair_dir: str = ""
    model_name: str = "gpt2"
    context_len: int = 4
    used_keys: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False
    note: str = (
        "Key-free scorer comparison. Not detector_mean. Not Claude. "
        "AUC is single-file ranking; prompt wins are the 10/12 grain."
    )


@dataclass
class ThresholdRow:
    name: str
    train_youden: float
    n_marked_above: int
    n_unmarked_at_most: int
    n_marked: int
    n_unmarked: int
    sensitivity: float
    specificity: float


@dataclass
class TransferRun:
    methods: list[MethodSummary] = field(default_factory=list)
    thresholds: list[ThresholdRow] = field(default_factory=list)
    train_dir: str = ""
    test_dir: str = ""
    n_train_prompts: int = 0
    n_test_prompts: int = 0
    dropped_stems: list[str] = field(default_factory=list)
    overlap_mode: str = "drop-from-train"
    model_name: str = "gpt2"
    context_len: int = 4
    used_keys: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False
    note: str = (
        "Train on one twin directory, score the other. Shared prompt stems "
        "are dropped as overlap_mode says. Thresholds are Youden on the "
        "training files (in-sample), then frozen on the test files. "
        "Not detector_mean. Not Claude. Not key recovery."
    )


def summarize_holdout(name: str, ev: IndicatorHoldout) -> MethodSummary:
    binary = binary_eval(ev.marked_lrs, ev.unmarked_lrs)
    return MethodSummary(
        name=name,
        holdout=ev,
        binary=binary,
        n_prompt_wins=ev.n_prompts_marked_above,
        n_prompts=ev.n_prompts,
    )


def run_probe(
    twins: Sequence[Twin],
    *,
    pair_dir: str = "",
    model_name: str = "gpt2",
    context_len: int = 4,
    methods: Sequence[str] | None = None,
    with_hashpool: bool = True,
    with_pivot: bool = False,
    n_hashes: int = 8,
    n_buckets: int = 256,
    lm=None,
) -> ProbeRun:
    requested = list(methods) if methods is not None else list(COUNT_SPECS)
    count_names = [m for m in requested if m in COUNT_SPECS]
    extras = {m for m in requested if m not in COUNT_SPECS}
    run = ProbeRun(
        pair_dir=pair_dir,
        model_name=model_name,
        context_len=context_len,
    )
    if count_names:
        counted = rotate_count_methods(
            twins,
            methods=count_names,
            context_len=context_len,
            model_name=model_name,
        )
        for name in count_names:
            run.methods.append(summarize_holdout(name, counted[name]))
    want_hash = with_hashpool and (
        methods is None or "hashpool" in requested or "hashvote" in extras
        or "hybrid" in extras
    )
    if want_hash and (methods is None or "hashpool" in requested):
        hp = rotate_hashpool(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hashpool", hp))
    if with_hashpool and "hashvote" in extras:
        vote = rotate_hashvote(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hashvote", vote))
    if "hybrid" in extras:
        hyb = rotate_hybrid(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hybrid", hyb))
    if with_pivot:
        pivots = rotate_pivot(twins, model_name=model_name, lm=lm)
        for name, ev in pivots.items():
            run.methods.append(summarize_holdout(name, ev))
    by_name = {m.name: m.holdout for m in run.methods}
    want_stack = "hits" in by_name and "hashpool" in by_name and (
        methods is None or "stack" in extras
    )
    if want_stack:
        stacked = rotate_score_stack(
            [by_name["hits"], by_name["hashpool"]],
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("stack", stacked))
    run.used_keys = any(m.holdout.used_keys for m in run.methods)
    run.used_hash_iv = any(m.holdout.used_hash_iv for m in run.methods)
    run.used_g_values = any(m.holdout.used_g_values for m in run.methods)
    return run


def print_probe(run: ProbeRun) -> str:
    lines = [
        (
            f"probe n_methods={len(run.methods)} pair_dir={run.pair_dir} "
            f"context_len={run.context_len} model={run.model_name} "
            f"used_keys={run.used_keys} hash_iv={run.used_hash_iv} "
            f"g_values={run.used_g_values}"
        ),
        run.note,
        CAVEAT,
        "",
        (
            "| method | prompt wins | file auc | marked>0 | unmarked<=0 "
            "| perm p | mean diff |"
        ),
        "|---|---|---|---|---|---|---|",
    ]
    for m in run.methods:
        b = m.binary
        lines.append(
            f"| {m.name} | {m.n_prompt_wins}/{m.n_prompts} | {b.auc:.3f} | "
            f"{b.n_positive_above_zero}/{b.n_positive} | "
            f"{b.n_negative_at_most_zero}/{b.n_negative} | "
            f"{b.permutation_p:.4g} | {b.mean_diff:.4f} |"
        )
    lines.append("")
    for m in run.methods:
        lines.append(format_binary_eval(m.binary, label=m.name))
        lines.append(
            f"{m.name} prompts_marked_above={m.n_prompt_wins}/{m.n_prompts} "
            f"instance={m.holdout.instance} used_keys={m.holdout.used_keys}"
        )
    return "\n".join(lines)


def persist_probe(run: ProbeRun, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    table = {
        "pair_dir": run.pair_dir,
        "model_name": run.model_name,
        "context_len": run.context_len,
        "used_keys": run.used_keys,
        "used_hash_iv": run.used_hash_iv,
        "used_g_values": run.used_g_values,
        "note": run.note,
        "caveat": CAVEAT,
        "methods": [],
    }
    for m in run.methods:
        row = {
            "name": m.name,
            "instance": m.holdout.instance,
            "score_kind": m.holdout.score_kind,
            "n_prompt_wins": m.n_prompt_wins,
            "n_prompts": m.n_prompts,
            "n_marked_above_unmarked": m.holdout.n_marked_above_unmarked,
            "used_keys": m.holdout.used_keys,
            "used_hash_iv": m.holdout.used_hash_iv,
            "used_g_values": m.holdout.used_g_values,
            "binary": binary_eval_to_dict(m.binary),
        }
        table["methods"].append(row)
        persist_holdout(m.holdout, out_dir / m.name)
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    (out_dir / "results.md").write_text(
        "# Key-free probe\n\n" + print_probe(run) + "\n"
    )


TRANSFER_DEFAULTS: tuple[str, ...] = (
    "hard",
    "hits",
    "hashpool",
    "hashvote",
    "hybrid",
    "stack",
)


def run_transfer(
    train_twins: Sequence[Twin],
    test_twins: Sequence[Twin],
    *,
    train_dir: str = "",
    test_dir: str = "",
    model_name: str = "gpt2",
    context_len: int = 4,
    methods: Sequence[str] | None = None,
    overlap_mode: str = "drop-from-train",
    n_hashes: int = 8,
    n_buckets: int = 256,
) -> TransferRun:
    """Fit on train twins, score every test file. No test prompt enters the fit."""
    train, test, overlap = apply_overlap(
        train_twins, test_twins, mode=overlap_mode
    )
    if len(train) < 1:
        raise ValueError("transfer left no training prompts")
    if len(test) < 1:
        raise ValueError("transfer left no test prompts")
    names = list(methods or TRANSFER_DEFAULTS)
    count_names = [n for n in names if n in COUNT_SPECS]
    extras = [n for n in names if n not in COUNT_SPECS]
    need_counts = bool(count_names) or any(
        n in extras for n in ("hybrid", "stack")
    )
    need_hash = any(
        n in extras for n in ("hashpool", "hashvote", "hybrid", "stack")
    )
    count_model = (
        fit_count_model(train, context_len=context_len) if need_counts else None
    )
    hash_model = (
        fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
        if need_hash
        else None
    )
    used_keys = False
    used_hash = False
    used_g = False
    if count_model is not None:
        used_keys = used_keys or count_model.used_keys
        used_hash = used_hash or count_model.used_hash_iv
        used_g = used_g or count_model.used_g_values
    if hash_model is not None:
        used_keys = used_keys or hash_model.used_keys
        used_hash = used_hash or hash_model.used_hash_iv
        used_g = used_g or hash_model.used_g_values

    scorers: dict[str, tuple[ScoreFn, str, str]] = {}
    for name in count_names:
        spec = COUNT_SPECS[name]
        assert count_model is not None
        scorers[name] = (
            (lambda ids, m=count_model, s=spec: score_sequence(ids, m, s)),
            spec.instance,
            name,
        )
    if "hashpool" in extras:
        assert hash_model is not None
        scorers["hashpool"] = (
            (lambda ids, m=hash_model: score_hashpool(ids, m)),
            "key-free-hashpool",
            "hashpool",
        )
    if "hashvote" in extras:
        assert hash_model is not None
        scorers["hashvote"] = (
            (lambda ids, m=hash_model: score_hashpool_vote(ids, m)),
            "key-free-hashvote",
            "hashvote",
        )
    if "hybrid" in extras:
        assert count_model is not None and hash_model is not None
        scorers["hybrid"] = (
            (lambda ids, c=count_model, h=hash_model: score_hybrid(ids, c, h)),
            "key-free-hybrid",
            "hybrid",
        )

    run = TransferRun(
        train_dir=train_dir,
        test_dir=test_dir,
        n_train_prompts=len(train),
        n_test_prompts=len(test),
        dropped_stems=list(overlap),
        overlap_mode=overlap_mode,
        model_name=model_name,
        context_len=context_len,
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
    )
    train_holdouts: dict[str, IndicatorHoldout] = {}
    test_holdouts: dict[str, IndicatorHoldout] = {}
    for name, (scorer, instance, kind) in scorers.items():
        train_ev = score_twins(
            train,
            scorer,
            context_len=context_len,
            model_name=model_name,
            instance=instance,
            score_kind=kind,
            used_keys=used_keys,
            used_hash_iv=used_hash,
            used_g_values=used_g,
            mode="train",
        )
        test_ev = score_twins(
            test,
            scorer,
            context_len=context_len,
            model_name=model_name,
            instance=instance,
            score_kind=kind,
            used_keys=used_keys,
            used_hash_iv=used_hash,
            used_g_values=used_g,
            mode="transfer",
        )
        train_holdouts[name] = train_ev
        test_holdouts[name] = test_ev
        run.methods.append(summarize_holdout(name, test_ev))
        train_bin = binary_eval(train_ev.marked_lrs, train_ev.unmarked_lrs)
        tp, tn, sens, spec = counts_at_threshold(
            test_ev.marked_lrs,
            test_ev.unmarked_lrs,
            train_bin.youden_threshold,
        )
        run.thresholds.append(
            ThresholdRow(
                name=name,
                train_youden=train_bin.youden_threshold,
                n_marked_above=tp,
                n_unmarked_at_most=tn,
                n_marked=len(test_ev.marked_lrs),
                n_unmarked=len(test_ev.unmarked_lrs),
                sensitivity=sens,
                specificity=spec,
            )
        )

    if "stack" in extras and "hits" in test_holdouts and "hashpool" in test_holdouts:
        import numpy as np
        from text_watermark_tools.pivot import fisher_lda, lda_score

        tr_h = _aligned_rows(train_holdouts["hits"])
        tr_p = _aligned_rows(train_holdouts["hashpool"])
        te_h = _aligned_rows(test_holdouts["hits"])
        te_p = _aligned_rows(test_holdouts["hashpool"])
        if [r[:2] for r in tr_h] != [r[:2] for r in tr_p]:
            raise ValueError("train hits/hashpool rows are not aligned")
        if [r[:2] for r in te_h] != [r[:2] for r in te_p]:
            raise ValueError("test hits/hashpool rows are not aligned")
        train_m = np.asarray([[a[2], b[2]] for a, b in zip(tr_h, tr_p)], dtype=np.float64)
        train_u = np.asarray([[a[3], b[3]] for a, b in zip(tr_h, tr_p)], dtype=np.float64)
        weights, midpoint = fisher_lda(train_m, train_u)
        parts = _empty_holdout_parts()
        train_parts = _empty_holdout_parts()
        for a, b in zip(tr_h, tr_p):
            vm = np.asarray([a[2], b[2]], dtype=np.float64)
            vu = np.asarray([a[3], b[3]], dtype=np.float64)
            _append_pair(
                train_parts,
                a[0],
                a[1],
                lda_score(vm, weights, midpoint),
                lda_score(vu, weights, midpoint),
            )
        for a, b in zip(te_h, te_p):
            vm = np.asarray([a[2], b[2]], dtype=np.float64)
            vu = np.asarray([a[3], b[3]], dtype=np.float64)
            _append_pair(
                parts,
                a[0],
                a[1],
                lda_score(vm, weights, midpoint),
                lda_score(vu, weights, midpoint),
            )
        stack_ev = _holdout_from_parts(
            parts,
            context_len=0,
            model_name=model_name,
            instance="key-free-stack",
            score_kind="stack",
            used_keys=used_keys,
            used_hash_iv=used_hash,
            used_g_values=used_g,
            mode="transfer",
        )
        train_stack = _holdout_from_parts(
            train_parts,
            context_len=0,
            model_name=model_name,
            instance="key-free-stack",
            score_kind="stack",
            used_keys=used_keys,
            used_hash_iv=used_hash,
            used_g_values=used_g,
            mode="train",
        )
        run.methods.append(summarize_holdout("stack", stack_ev))
        train_bin = binary_eval(train_stack.marked_lrs, train_stack.unmarked_lrs)
        tp, tn, sens, spec = counts_at_threshold(
            stack_ev.marked_lrs,
            stack_ev.unmarked_lrs,
            train_bin.youden_threshold,
        )
        run.thresholds.append(
            ThresholdRow(
                name="stack",
                train_youden=train_bin.youden_threshold,
                n_marked_above=tp,
                n_unmarked_at_most=tn,
                n_marked=len(stack_ev.marked_lrs),
                n_unmarked=len(stack_ev.unmarked_lrs),
                sensitivity=sens,
                specificity=spec,
            )
        )
    return run


def print_transfer(run: TransferRun) -> str:
    lines = [
        (
            f"transfer n_methods={len(run.methods)} train={run.train_dir} "
            f"test={run.test_dir} n_train={run.n_train_prompts} "
            f"n_test={run.n_test_prompts} overlap_mode={run.overlap_mode} "
            f"dropped={len(run.dropped_stems)} context_len={run.context_len} "
            f"model={run.model_name} used_keys={run.used_keys} "
            f"hash_iv={run.used_hash_iv} g_values={run.used_g_values}"
        ),
        run.note,
        CAVEAT,
        "",
        (
            "| method | prompt wins | file auc | marked>0 | unmarked<=0 "
            "| perm p | mean diff |"
        ),
        "|---|---|---|---|---|---|---|",
    ]
    for m in run.methods:
        b = m.binary
        lines.append(
            f"| {m.name} | {m.n_prompt_wins}/{m.n_prompts} | {b.auc:.3f} | "
            f"{b.n_positive_above_zero}/{b.n_positive} | "
            f"{b.n_negative_at_most_zero}/{b.n_negative} | "
            f"{b.permutation_p:.4g} | {b.mean_diff:.4f} |"
        )
    lines.append("")
    lines.append(
        "| method | train Youden t | test marked>t | test unmarked≤t "
        "| sens | spec |"
    )
    lines.append("|---|---|---|---|---|---|")
    for row in run.thresholds:
        lines.append(
            f"| {row.name} | {row.train_youden:.4f} | "
            f"{row.n_marked_above}/{row.n_marked} | "
            f"{row.n_unmarked_at_most}/{row.n_unmarked} | "
            f"{row.sensitivity:.3f} | {row.specificity:.3f} |"
        )
    if run.dropped_stems:
        lines.append("")
        lines.append("dropped stems: " + ", ".join(run.dropped_stems))
    lines.append("")
    for m in run.methods:
        lines.append(format_binary_eval(m.binary, label=m.name))
        lines.append(
            f"{m.name} prompts_marked_above={m.n_prompt_wins}/{m.n_prompts} "
            f"instance={m.holdout.instance} used_keys={m.holdout.used_keys}"
        )
    return "\n".join(lines)


def persist_transfer(run: TransferRun, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    table = {
        "train_dir": run.train_dir,
        "test_dir": run.test_dir,
        "n_train_prompts": run.n_train_prompts,
        "n_test_prompts": run.n_test_prompts,
        "dropped_stems": run.dropped_stems,
        "overlap_mode": run.overlap_mode,
        "model_name": run.model_name,
        "context_len": run.context_len,
        "used_keys": run.used_keys,
        "used_hash_iv": run.used_hash_iv,
        "used_g_values": run.used_g_values,
        "note": run.note,
        "caveat": CAVEAT,
        "methods": [],
        "thresholds": [row.__dict__ for row in run.thresholds],
    }
    for m in run.methods:
        row = {
            "name": m.name,
            "instance": m.holdout.instance,
            "score_kind": m.holdout.score_kind,
            "n_prompt_wins": m.n_prompt_wins,
            "n_prompts": m.n_prompts,
            "n_marked_above_unmarked": m.holdout.n_marked_above_unmarked,
            "used_keys": m.holdout.used_keys,
            "used_hash_iv": m.holdout.used_hash_iv,
            "used_g_values": m.holdout.used_g_values,
            "binary": binary_eval_to_dict(m.binary),
        }
        table["methods"].append(row)
        persist_holdout(m.holdout, out_dir / m.name)
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    (out_dir / "results.md").write_text(
        "# Key-free transfer\n\n" + print_transfer(run) + "\n"
    )


def scrub_token_ids(
    token_ids: Sequence[int],
    lm,
    *,
    top_k: int = 40,
    only_if_in_topk: bool = True,
    logits=None,
) -> tuple[list[int], int]:
    from text_watermark_tools.pivot import (
        snap_to_unmarked_argmax,
        unmarked_logits_for_sequence,
    )

    rows = logits if logits is not None else unmarked_logits_for_sequence(
        token_ids, lm
    )
    return snap_to_unmarked_argmax(
        token_ids, rows, top_k=top_k, only_if_in_topk=only_if_in_topk
    )


@dataclass
class ScrubRow:
    path: str
    n_tokens: int
    n_flips: int
    mean_before: float
    weighted_before: float
    mean_after: float
    weighted_after: float
    used_keys_for_snap: bool = False


@dataclass
class ScrubRun:
    rows: list[ScrubRow]
    model_name: str
    instance: str
    used_keys_for_snap: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False


def run_scrub_files(
    files: Sequence[Path],
    *,
    model_name: str = "gpt2",
    top_k: int = 40,
    lm=None,
    tokenizer=None,
) -> ScrubRun:
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.score import PUBLIC_INSTANCE, load_tokenizer, official_score_token_ids
    import torch

    tok = tokenizer or load_tokenizer(model_name)
    if lm is None:
        lm = _load_unmarked_model(generate_device(), model_name=model_name)
    rows: list[ScrubRow] = []
    for path in files:
        text = Path(path).read_text()
        ids = tok(text)["input_ids"]
        snapped, n_flips = scrub_token_ids(ids, lm, top_k=top_k)
        before = official_score_token_ids(
            torch.tensor([ids], dtype=torch.long), tokenizer=tok
        )
        after = official_score_token_ids(
            torch.tensor([snapped], dtype=torch.long), tokenizer=tok
        )
        rows.append(
            ScrubRow(
                path=str(path),
                n_tokens=len(ids),
                n_flips=n_flips,
                mean_before=before.mean,
                weighted_before=before.weighted_mean,
                mean_after=after.mean,
                weighted_after=after.weighted_mean,
                used_keys_for_snap=False,
            )
        )
    return ScrubRun(
        rows=rows,
        model_name=model_name,
        instance=PUBLIC_INSTANCE,
        used_keys_for_snap=False,
        used_hash_iv=False,
        used_g_values=False,
    )


def print_scrub(run: ScrubRun) -> str:
    lines = [
        (
            f"scrub n_files={len(run.rows)} model={run.model_name} "
            f"snap_used_keys={run.used_keys_for_snap} "
            f"reference_instance={run.instance} "
            f"hash_iv={run.used_hash_iv} g_values={run.used_g_values}"
        ),
        "Argmax snap does not use watermark keys. Official scores are a reference check.",
        "",
        "| file | flips | mean before | mean after |",
        "|---|---|---|---|",
    ]
    for row in run.rows:
        name = Path(row.path).name
        lines.append(
            f"| {name} | {row.n_flips}/{row.n_tokens} | "
            f"{row.mean_before:.4f} | {row.mean_after:.4f} |"
        )
    if run.rows:
        mb = sum(r.mean_before for r in run.rows) / len(run.rows)
        ma = sum(r.mean_after for r in run.rows) / len(run.rows)
        lines.append("")
        lines.append(f"mean official before={mb:.4f} after={ma:.4f}")
    return "\n".join(lines)


def persist_scrub(run: ScrubRun, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "model_name": run.model_name,
        "instance": run.instance,
        "used_keys_for_snap": run.used_keys_for_snap,
        "used_hash_iv": run.used_hash_iv,
        "used_g_values": run.used_g_values,
        "rows": [row.__dict__ for row in run.rows],
    }
    (out_dir / "results.json").write_text(json.dumps(payload, indent=2) + "\n")
    (out_dir / "results.md").write_text("# Argmax snap scrub\n\n" + print_scrub(run) + "\n")
