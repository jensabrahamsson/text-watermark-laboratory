"""Data models, specs, and sequence helpers for probe and transfer."""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Sequence

from text_watermark_tools.blind import Twin
from text_watermark_tools.indicator import IndicatorHoldout
from text_watermark_tools.transfer import DEFAULT_SURFACE_CONTEXT, ScoreSpec

ScoreFn = Callable[[Sequence[int] | str], float]

LOGIT_FEATURE_ORDER: tuple[str, ...] = (
    "hits",
    "poshits",
    "hashpool",
    "surface",
    "hitmass",
    "poshitmass",
    "first",
)
DEFAULT_POS_BUCKET = 16
DEFAULT_COVERAGE_WINDOWS: tuple[tuple[int, int], ...] = (
    (0, 16),
    (16, 32),
    (32, 64),
    (64, 128),
)

POSHITS_SPEC = ScoreSpec(kind="gated", min_count=1, instance="key-free-poshits")
POSTOKHITS_SPEC = ScoreSpec(
    kind="gated",
    min_count=1,
    require_token=True,
    instance="key-free-postokhits",
)
POSTOKBACKOFF_SPEC = ScoreSpec(
    kind="tokbackoff",
    min_count=1,
    require_token=True,
    instance="key-free-postokbackoff",
)
POSTOKBACKOFF2_SPEC = ScoreSpec(
    kind="tokbackoff",
    min_count=1,
    require_token=True,
    min_order=2,
    instance="key-free-postokbackoff2",
)
POSHITMASS_SPEC = ScoreSpec(
    kind="hitmass", min_count=1, instance="key-free-poshitmass"
)
POS_SPECS: dict[str, ScoreSpec] = {
    "poshits": POSHITS_SPEC,
    "postokhits": POSTOKHITS_SPEC,
    "postokbackoff": POSTOKBACKOFF_SPEC,
    "postokbackoff2": POSTOKBACKOFF2_SPEC,
    "poshitmass": POSHITMASS_SPEC,
}


def clip_seq(seq, n: int):
    """Prefix of token ids or of a string. n<=0 leaves the sequence unchanged."""
    if n <= 0:
        return seq
    return seq[:n]


def slice_seq(seq, start: int, end: int):
    """Half-open token or character window [start:end]."""
    if end <= start or start < 0:
        return seq[0:0]
    return seq[start:end]


def _parse_prefix_lens(prefix_lens: Sequence[int] | None) -> tuple[int, ...]:
    if not prefix_lens:
        return ()
    out = []
    seen: set[int] = set()
    for raw in prefix_lens:
        n = int(raw)
        if n <= 0 or n in seen:
            continue
        seen.add(n)
        out.append(n)
    return tuple(out)


def _parse_windows(
    windows: Sequence[str | tuple[int, int]] | None,
) -> tuple[tuple[int, int], ...]:
    if not windows:
        return ()
    out: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for raw in windows:
        if isinstance(raw, str):
            if ":" not in raw:
                raise ValueError(f"window {raw!r} must look like start:end")
            left, right = raw.split(":", 1)
            start, end = int(left.strip()), int(right.strip())
        else:
            start, end = int(raw[0]), int(raw[1])
        if start < 0 or end <= start:
            continue
        key = (start, end)
        if key in seen:
            continue
        seen.add(key)
        out.append(key)
    return tuple(out)


def _window_dir(start: int, end: int) -> str:
    return f"window-{start}-{end}"


def _twin_prefix(twin: Twin, prompt_context: bool) -> tuple[int, ...]:
    if not prompt_context:
        return ()
    if not twin.prompt_ids:
        raise ValueError(
            f"prompt-context needs prompt token ids on stem {twin.stem!r}"
        )
    return tuple(int(x) for x in twin.prompt_ids)


def _call_scorer(
    scorer: ScoreFn,
    seq,
    *,
    prefix: Sequence[int] = (),
    score_span: tuple[int, int] | None = None,
):
    """Call a scorer with optional prefix and absolute score_span.

    Inspects the callable. Does not catch TypeError from inside the scorer.
    Refuses to reindex a window as a new sequence if score_span is missing.
    """
    try:
        params = inspect.signature(scorer).parameters
    except (TypeError, ValueError):
        params = {}
    has_var = any(
        p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()
    )
    kwargs = {}
    if prefix:
        if has_var or "prefix" in params:
            kwargs["prefix"] = prefix
        else:
            raise TypeError(
                "scorer does not accept prefix=; prompt-context was requested"
            )
    if score_span is not None:
        if has_var or "score_span" in params:
            kwargs["score_span"] = score_span
        else:
            raise TypeError(
                "scorer does not accept score_span=; refusing to reindex "
                "the window as a new sequence"
            )
    if kwargs:
        return scorer(seq, **kwargs)
    return scorer(seq)


def _bound_ids_scorer(fn, *bound, **fixed):
    """Wrap fn(ids, *bound, **fixed) so windows keep absolute score_span."""
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        params = {}
    has_var = any(
        p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()
    )

    def score(ids, prefix=(), score_span=None):
        kwargs = dict(fixed)
        if "prefix" in params or has_var:
            kwargs["prefix"] = prefix
        elif prefix:
            raise TypeError(
                "scorer does not accept prefix=; prompt-context was requested"
            )
        if score_span is not None:
            if "score_span" in params or has_var:
                kwargs["score_span"] = score_span
            else:
                raise TypeError(
                    "scorer does not accept score_span=; refusing to reindex "
                    "the window as a new sequence"
                )
        return fn(ids, *bound, **kwargs)

    return score


def _twin_sides(twin: Twin, seq_mode: str) -> tuple[list, list]:
    if seq_mode == "text":
        return twin.marked_texts(), twin.unmarked_texts()
    return twin.marked_seqs(), twin.unmarked_seqs()


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
    max_draws: int | None = None
    prefix_lens: tuple[int, ...] = ()
    prefixes: dict[int, list[MethodSummary]] = field(default_factory=dict)
    windows: tuple[tuple[int, int], ...] = ()
    window_results: dict[tuple[int, int], list[MethodSummary]] = field(
        default_factory=dict
    )
    fit_prefix: int | None = None
    position_bucket: int = 0
    include_first: bool = False
    prompt_context: bool = False
    pivot_weights: tuple[str, ...] = ()
    rankpath_full: bool = False
    rankpath_pos_bucket: int | None = None
    cascade: dict | None = None
    cascade_rankpath_end: int | None = None
    cascade_when: str = "coverage"
    coverage: dict | None = None
    note: str = (
        "Key-free scorer comparison. Not detector_mean. Not Claude. "
        "AUC is single-file ranking; prompt wins are prompt-group ranking, "
        "not per-file accuracy. ranking_without_isolated_tp counts prompt "
        "wins with no marked file lr>0 — those stems rank because unmarked "
        "is more negative, not because any isolated file signs. "
        "nested-youden-by-stem is a threshold chosen on other prompt "
        "families' already-held-out LRs, not a global peek at the same stem. "
        "coverage.json is leave-one-out shared last-k fraction by position; "
        "it explains a front-loaded reader, not a keyed detector."
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
    source: str = "in-sample-youden"


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
    count_model: object | None = None
    hash_model: object | None = None
    hash_len_model: object | None = None
    hash_skip_model: object | None = None
    hash_mask_model: object | None = None
    surface_model: object | None = None
    pos_model: object | None = None
    pos_hash: object | None = None
    nested: bool = False
    shuffle_seed: int | None = None
    surface_context_len: int = DEFAULT_SURFACE_CONTEXT
    prefix_lens: tuple[int, ...] = ()
    prefixes: dict[int, list[MethodSummary]] = field(default_factory=dict)
    windows: tuple[tuple[int, int], ...] = ()
    window_results: dict[tuple[int, int], list[MethodSummary]] = field(
        default_factory=dict
    )
    fit_prefix: int | None = None
    position_bucket: int = 0
    include_first: bool = False
    prompt_context: bool = False
    pivot_weights: tuple[str, ...] = ()
    pivot_fit: object | None = None
    pivot_fits: dict = field(default_factory=dict)
    rankpath_model: object | None = None
    rankpath_full: bool = False
    rankpath_pos_bucket: int | None = None
    cascade_fallback: str = "pivot"
    cascade_rankpath_end: int | None = None
    cascade_when: str = "coverage"
    cascade: dict | None = None
    note: str = (
        "Train on one twin directory, score the other. Shared prompt stems "
        "are dropped as overlap_mode says. Thresholds are Youden on the "
        "training files (in-sample), then frozen on the test files. "
        "ranking_without_isolated_tp counts prompt wins with no marked "
        "file lr>0; do not read prompt wins as isolated recall. "
        "Not detector_mean. Not Claude. Not key recovery."
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
