"""Rotators and transfer evaluators for count, hashed, positional, and pivot models."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from text_watermark_tools.blind import Twin, _scored_ctx, clip_twins_prefix
from text_watermark_tools.indicator import (
    CAVEAT,
    IndicatorHoldout,
    persist_holdout,
    persist_indicator,
)
from text_watermark_tools.probe_models import (
    DEFAULT_COVERAGE_WINDOWS,
    DEFAULT_POS_BUCKET,
    LOGIT_FEATURE_ORDER,
    POS_SPECS,
    POSHITMASS_SPEC,
    POSHITS_SPEC,
    POSTOKBACKOFF2_SPEC,
    POSTOKBACKOFF_SPEC,
    POSTOKHITS_SPEC,
    MethodSummary,
    ProbeRun,
    ScoreFn,
    ThresholdRow,
    TransferRun,
    _append_pair,
    _bound_ids_scorer,
    _call_scorer,
    _empty_holdout_parts,
    _holdout_from_parts,
    _parse_prefix_lens,
    _parse_windows,
    _twin_prefix,
    _twin_sides,
    _window_dir,
    clip_seq,
    slice_seq,
)
from text_watermark_tools.probe_reporting import summarize_holdout
from text_watermark_tools.stats import (
    binary_eval,
    binary_eval_to_dict,
    counts_at_threshold,
    coverage_gate,
    coverage_gate_to_dict,
    fit_ridge_logodds,
    format_binary_eval,
    format_coverage_gate,
    nested_stem_eval_to_dict,
    nested_threshold_by_stem,
    score_ridge_logodds,
    threshold_at_fpr,
)
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    DEFAULT_SURFACE_CONTEXT,
    HASH_CASCADE_READERS,
    HASHBACKOFF_ORDERS,
    ScoreSpec,
    _count,
    fit_count_model,
    fit_hashmix_twins,
    fit_hashpool_twins,
    fit_surface_twins,
    persist_hashpool,
    score_hashed_reader_detail,
    score_hashmask,
    score_hashmix,
    score_hashpool,
    score_hashpool_vote,
    score_hashskip,
    score_hashtok,
    score_hashtokbackoff,
    score_hashtokgap,
    score_hybrid,
    score_sequence,
    score_surface,
    score_tokhybrid,
)

def _hashed_cascade_models(
    twins: Sequence[Twin],
    reader: str,
    *,
    context_len: int,
    n_hashes: int,
    n_buckets: int,
) -> dict:
    """Fit occupancy-free hashed tables for a cascade count channel."""
    name = str(reader)
    models: dict = {
        "hash_model": None,
        "hash_len_model": None,
        "mix_model": None,
        "mix_len_model": None,
    }
    if name == "hashtok":
        models["hash_model"] = fit_hashpool_twins(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
    elif name == "hashtoklen":
        models["hash_len_model"] = fit_hashpool_twins(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            exact_len=True,
        )
    elif name in ("hashtokbackoff", "hashtokbackoff2"):
        models["mix_model"] = fit_hashmix_twins(
            twins,
            orders=HASHBACKOFF_ORDERS,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
    elif name in ("hashtoklenbackoff", "hashtoklenbackoff2"):
        models["mix_len_model"] = fit_hashmix_twins(
            twins,
            orders=HASHBACKOFF_ORDERS,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            exact_len=True,
        )
    else:
        raise ValueError(
            f"unknown hashed cascade {reader!r}; choose "
            + ", ".join(HASH_CASCADE_READERS)
        )
    return models


def hashed_count_detail(reader: str, models: dict):
    """ScoreDetail callable for an occupancy-free hashed cascade channel."""

    def _detail(ids, prefix=()):
        del prefix
        return score_hashed_reader_detail(ids, reader, **models)

    return _detail


def hashed_count_map(
    twins: Sequence[Twin],
    reader: str,
    models: dict,
) -> dict[tuple[str, int, str], dict]:
    """Per-file hashed count_lr / n_used for rebind_count_channel."""
    detail = hashed_count_detail(reader, models)
    out: dict[tuple[str, int, str], dict] = {}
    for twin in twins:
        n = min(len(twin.marked_seqs()), len(twin.unmarked_seqs()))
        for i in range(n):
            sample = i + 1
            for side, ids in (
                ("marked", twin.marked_seqs()[i]),
                ("unmarked", twin.unmarked_seqs()[i]),
            ):
                rec = detail(ids)
                out[(twin.stem, sample, side)] = {
                    "count_lr": rec.lr,
                    "n_used": rec.n_used,
                    "n_positions": rec.n_positions,
                    "count_method": reader,
                }
    return out


def _hashed_flag_model(models: dict):
    for key in ("hash_len_model", "hash_model", "mix_len_model", "mix_model"):
        model = models.get(key)
        if model is not None:
            return model
    return None

def _empty_cov_bin() -> dict[str, float]:
    return {
        "n": 0,
        "shared": 0,
        "marked_only": 0,
        "unmarked_only": 0,
        "unseen": 0,
        "support_sum": 0,
    }


def _cov_observe(bin_: dict[str, float], n_m: int, n_u: int) -> None:
    bin_["n"] += 1
    if n_m >= 1 and n_u >= 1:
        bin_["shared"] += 1
        bin_["support_sum"] += min(n_m, n_u)
    elif n_m >= 1:
        bin_["marked_only"] += 1
    elif n_u >= 1:
        bin_["unmarked_only"] += 1
    else:
        bin_["unseen"] += 1


def _cov_finalize(bin_: dict[str, float], *, start: int | None = None, end: int | None = None) -> dict:
    n = int(bin_["n"])
    shared = int(bin_["shared"])
    row = {
        "n": n,
        "shared": shared,
        "shared_frac": (shared / n) if n else 0.0,
        "marked_only": int(bin_["marked_only"]),
        "unmarked_only": int(bin_["unmarked_only"]),
        "unseen": int(bin_["unseen"]),
        "mean_shared_support": (
            bin_["support_sum"] / shared if shared else 0.0
        ),
    }
    if start is not None:
        row["start"] = int(start)
        row["end"] = int(end or start)
    return row


def rotate_hits_coverage(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    position_bucket: int = 0,
    windows: Sequence[str | tuple[int, int]] = DEFAULT_COVERAGE_WINDOWS,
    max_index: int = 128,
) -> dict:
    """Leave-one-out share of last-k contexts seen on both training sides.

    Hits can only fire on shared contexts. This curve locates where those
    contexts exist. It does not use keys, hash_iv, or g-values.
    """
    if len(twins) < 3:
        raise ValueError("coverage rotate needs at least three prompts")
    spans = _parse_windows(windows) or DEFAULT_COVERAGE_WINDOWS
    by_index = [_empty_cov_bin() for _ in range(max_index)]
    by_window = {win: _empty_cov_bin() for win in spans}
    used_keys = False
    n_files = 0
    for held in twins:
        train = [t for t in twins if t.stem != held.stem]
        model = fit_count_model(
            train, context_len=context_len, position_bucket=position_bucket
        )
        used_keys = used_keys or model.used_keys
        seqs = [*held.marked_seqs(), *held.unmarked_seqs()]
        n_files += min(len(held.marked_seqs()), len(held.unmarked_seqs())) * 2
        for seq in seqs:
            for i in range(1, len(seq)):
                ctx = _scored_ctx(seq, i, context_len, position_bucket)
                n_m = _count(model.marked, ctx)
                n_u = _count(model.unmarked, ctx)
                if i < max_index:
                    _cov_observe(by_index[i], n_m, n_u)
                for start, end in spans:
                    if start <= i < end:
                        _cov_observe(by_window[(start, end)], n_m, n_u)
    if used_keys:
        raise RuntimeError("coverage consulted keys")
    return {
        "context_len": int(context_len),
        "position_bucket": int(position_bucket) if position_bucket else 0,
        "n_prompts": len(twins),
        "n_files": n_files,
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "note": (
            "Leave-one-prompt-out share of last-k contexts seen on both "
            "training sides. Hits can only score those positions. This is "
            "why the key-free 4-gram reader is front-loaded. Not keys."
        ),
        "by_index": [
            _cov_finalize(bin_, start=i, end=i + 1)
            for i, bin_ in enumerate(by_index)
            if bin_["n"]
        ],
        "by_window": [
            _cov_finalize(by_window[win], start=win[0], end=win[1])
            for win in spans
        ],
    }



def rotate_custom(
    twins: Sequence[Twin],
    make_scorer: Callable[[Sequence[Twin]], tuple[ScoreFn, bool, bool, bool]],
    *,
    context_len: int,
    model_name: str,
    instance: str,
    score_kind: str,
    margin: float = 0.0,
    seq_mode: str = "ids",
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, IndicatorHoldout] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], IndicatorHoldout] | None = None,
) -> IndicatorHoldout:
    if len(twins) < 3:
        raise ValueError("rotate probe needs at least three prompts")
    parts = _empty_holdout_parts()
    lenses = _parse_prefix_lens(prefix_lens)
    spans = _parse_windows(windows)
    prefix_parts = {n: _empty_holdout_parts() for n in lenses}
    window_parts = {win: _empty_holdout_parts() for win in spans}
    used_keys = used_hash = used_g = False
    for held in twins:
        train = [t for t in twins if t.stem != held.stem]
        scorer, k, h, g = make_scorer(train)
        used_keys = used_keys or k
        used_hash = used_hash or h
        used_g = used_g or g
        marked_seqs, unmarked_seqs = _twin_sides(held, seq_mode)
        n = min(len(marked_seqs), len(unmarked_seqs))
        for i in range(n):
            marked = marked_seqs[i]
            unmarked = unmarked_seqs[i]
            _append_pair(
                parts,
                held.stem,
                i + 1,
                scorer(marked),
                scorer(unmarked),
            )
            for plen in lenses:
                _append_pair(
                    prefix_parts[plen],
                    held.stem,
                    i + 1,
                    scorer(clip_seq(marked, plen)),
                    scorer(clip_seq(unmarked, plen)),
                )
            for start, end in spans:
                if seq_mode == "text":
                    marked_w = scorer(slice_seq(marked, start, end))
                    unmarked_w = scorer(slice_seq(unmarked, start, end))
                else:
                    marked_w = _call_scorer(
                        scorer, marked, score_span=(start, end)
                    )
                    unmarked_w = _call_scorer(
                        scorer, unmarked, score_span=(start, end)
                    )
                _append_pair(
                    window_parts[(start, end)],
                    held.stem,
                    i + 1,
                    marked_w,
                    unmarked_w,
                )
    flags = dict(
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
        margin=margin,
    )
    if prefix_out is not None:
        for plen in lenses:
            prefix_out[plen] = _holdout_from_parts(
                prefix_parts[plen],
                context_len=context_len,
                model_name=model_name,
                instance=instance,
                score_kind=f"{score_kind}@p{plen}",
                **flags,
            )
    if window_out is not None:
        for start, end in spans:
            window_out[(start, end)] = _holdout_from_parts(
                window_parts[(start, end)],
                context_len=context_len,
                model_name=model_name,
                instance=instance,
                score_kind=f"{score_kind}@w{start}-{end}",
                **flags,
            )
    return _holdout_from_parts(
        parts,
        context_len=context_len,
        model_name=model_name,
        instance=instance,
        score_kind=score_kind,
        **flags,
    )


def rotate_count_methods(
    twins: Sequence[Twin],
    *,
    methods: Sequence[str] | None = None,
    context_len: int = 4,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
    extra_specs: dict[str, ScoreSpec] | None = None,
    include_first: bool = False,
    prompt_context: bool = False,
) -> dict[str, IndicatorHoldout]:
    extra_specs = extra_specs or {}
    names = list(COUNT_SPECS.keys()) if methods is None else list(methods)
    for name in extra_specs:
        if name not in names:
            names.append(name)
    unknown = [n for n in names if n not in COUNT_SPECS and n not in extra_specs]
    if unknown:
        raise ValueError(f"unknown count methods: {unknown}")

    def _spec(name: str) -> ScoreSpec:
        return extra_specs[name] if name in extra_specs else COUNT_SPECS[name]

    buckets = {name: _empty_holdout_parts() for name in names}
    used = {name: (False, False, False) for name in names}
    lenses = _parse_prefix_lens(prefix_lens)
    spans = _parse_windows(windows)
    prefix_buckets = {
        plen: {name: _empty_holdout_parts() for name in names} for plen in lenses
    }
    window_buckets = {
        win: {name: _empty_holdout_parts() for name in names} for win in spans
    }
    for held in twins:
        train = [t for t in twins if t.stem != held.stem]
        store_first = include_first or any(
            _spec(n).include_first or _spec(n).first_only for n in names
        )
        model = fit_count_model(
            train,
            context_len=context_len,
            position_bucket=position_bucket,
            include_first=store_first,
            prompt_context=prompt_context,
        )
        model.include_first = bool(include_first)
        flags = (model.used_keys, model.used_hash_iv, model.used_g_values)
        marked_seqs = held.marked_seqs()
        unmarked_seqs = held.unmarked_seqs()
        held_prefix = _twin_prefix(held, prompt_context)
        n = min(len(marked_seqs), len(unmarked_seqs))
        for name in names:
            spec = _spec(name)
            used[name] = tuple(a or b for a, b in zip(used[name], flags, strict=True))
            for i in range(n):
                marked = marked_seqs[i]
                unmarked = unmarked_seqs[i]
                _append_pair(
                    buckets[name],
                    held.stem,
                    i + 1,
                    score_sequence(marked, model, spec, prefix=held_prefix),
                    score_sequence(unmarked, model, spec, prefix=held_prefix),
                )
                for plen in lenses:
                    _append_pair(
                        prefix_buckets[plen][name],
                        held.stem,
                        i + 1,
                        score_sequence(
                            clip_seq(marked, plen), model, spec, prefix=held_prefix
                        ),
                        score_sequence(
                            clip_seq(unmarked, plen), model, spec, prefix=held_prefix
                        ),
                    )
                for start, end in spans:
                    _append_pair(
                        window_buckets[(start, end)][name],
                        held.stem,
                        i + 1,
                        score_sequence(
                            marked,
                            model,
                            spec,
                            prefix=held_prefix,
                            score_span=(start, end),
                        ),
                        score_sequence(
                            unmarked,
                            model,
                            spec,
                            prefix=held_prefix,
                            score_span=(start, end),
                        ),
                    )
    out: dict[str, IndicatorHoldout] = {}
    for name in names:
        spec = _spec(name)
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
        if prefix_out is not None:
            for plen in lenses:
                prefix_out.setdefault(plen, {})[name] = _holdout_from_parts(
                    prefix_buckets[plen][name],
                    context_len=context_len,
                    model_name=model_name,
                    instance=spec.instance,
                    score_kind=f"{name}@p{plen}",
                    used_keys=k,
                    used_hash_iv=h,
                    used_g_values=g,
                    margin=margin,
                )
        if window_out is not None:
            for start, end in spans:
                window_out.setdefault((start, end), {})[name] = _holdout_from_parts(
                    window_buckets[(start, end)][name],
                    context_len=context_len,
                    model_name=model_name,
                    instance=spec.instance,
                    score_kind=f"{name}@w{start}-{end}",
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
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
    method_name: str = "hashpool",
    exact_len: bool = False,
    seed: int = 20260831,
) -> IndicatorHoldout:
    reader = str(method_name or "hashpool")
    drop_one = reader in ("hashskip", "hashskip2")
    mask_one = reader in ("hashmask", "hashmask2")
    min_count = 2 if reader in (
        "hashtok2",
        "hashtoklen2",
        "hashskip2",
        "hashmask2",
    ) else 1
    if reader in (
        "hashtok",
        "hashtok2",
        "hashtoklen",
        "hashtoklen2",
        "hashskip",
        "hashskip2",
        "hashmask",
        "hashmask2",
        "poshashtok",
    ):
        kind = reader
        instance = f"key-free-{reader}"
        if drop_one:
            score_fn = lambda ids, m, k=min_count, score_span=None: score_hashskip(
                ids, m, min_count=k, score_span=score_span
            )
        elif mask_one:
            score_fn = lambda ids, m, k=min_count, score_span=None: score_hashmask(
                ids, m, min_count=k, score_span=score_span
            )
        else:
            score_fn = lambda ids, m, k=min_count, score_span=None: score_hashtok(
                ids, m, min_count=k, score_span=score_span
            )
        exact_len = bool(exact_len) or reader in (
            "hashtoklen",
            "hashtoklen2",
            "hashskip",
            "hashskip2",
            "hashmask",
            "hashmask2",
        )
    else:
        kind = "pospool" if position_bucket > 0 else "hashpool"
        instance = "key-free-pospool" if position_bucket > 0 else "key-free-hashpool"
        score_fn = score_hashpool

    def make(train: Sequence[Twin]):
        model = fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            position_bucket=position_bucket,
            exact_len=bool(exact_len),
            drop_one=drop_one,
            mask_one=mask_one,
            seed=seed,
        )
        return (
            lambda ids, prefix=(), score_span=None, m=model, s=score_fn: s(
                ids, m, score_span=score_span
            ),
            model.used_keys,
            model.used_hash_iv,
            model.used_g_values,
        )
    store_name = method_name or kind
    one: dict[int, IndicatorHoldout] = {}
    one_win: dict[tuple[int, int], IndicatorHoldout] = {}
    ev = rotate_custom(
        twins,
        make,
        context_len=context_len,
        model_name=model_name,
        instance=instance,
        score_kind=kind,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=one if prefix_lens else None,
        windows=windows,
        window_out=one_win if windows else None,
    )
    if prefix_out is not None:
        for plen, hold in one.items():
            prefix_out.setdefault(plen, {})[store_name] = hold
    if window_out is not None:
        for win, hold in one_win.items():
            window_out.setdefault(win, {})[store_name] = hold
    return ev


def rotate_hashtok(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
    exact_len: bool = False,
    method_name: str = "",
    seed: int = 20260831,
) -> IndicatorHoldout:
    """Hashpool reader that skips unseen next tokens (no occupancy Laplace)."""
    reader = str(method_name or ("hashtoklen" if exact_len else "hashtok"))
    return rotate_hashpool(
        twins,
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=position_bucket,
        method_name=reader,
        exact_len=bool(exact_len) or reader == "hashtoklen",
        seed=seed,
    )


def rotate_hashtok2(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
) -> IndicatorHoldout:
    """Unbucketed hashtok that skips singleton hash collisions. Still no keys."""
    return rotate_hashpool(
        twins,
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=position_bucket,
        method_name="hashtok2",
        exact_len=False,
    )


def rotate_hashskip(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
) -> IndicatorHoldout:
    """Occupancy-free drop-one skip-grams of exact last-k. Still no keys."""
    return rotate_hashpool(
        twins,
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=position_bucket,
        method_name="hashskip",
        exact_len=True,
    )


def rotate_hashtoklen2(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
) -> IndicatorHoldout:
    """Exact last-k hashtok that skips singleton hash collisions."""
    return rotate_hashpool(
        twins,
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=position_bucket,
        method_name="hashtoklen2",
        exact_len=True,
    )


def rotate_hashskip2(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
) -> IndicatorHoldout:
    """Drop-one skip-grams that skip singleton hash collisions."""
    return rotate_hashpool(
        twins,
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=position_bucket,
        method_name="hashskip2",
        exact_len=True,
    )


def rotate_hashmask(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
) -> IndicatorHoldout:
    """Occupancy-free MASK replace of exact last-k. Still no keys."""
    return rotate_hashpool(
        twins,
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=position_bucket,
        method_name="hashmask",
        exact_len=True,
    )


def rotate_hashmask2(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
) -> IndicatorHoldout:
    """MASK replace that skips singleton hash collisions."""
    return rotate_hashpool(
        twins,
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=position_bucket,
        method_name="hashmask2",
        exact_len=True,
    )


def rotate_hashtoklen(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = 0,
) -> IndicatorHoldout:
    return rotate_hashtok(
        twins,
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=position_bucket,
        exact_len=True,
        method_name="hashtoklen",
    )


def rotate_pos_methods(
    twins: Sequence[Twin],
    *,
    methods: Sequence[str] = ("poshits",),
    context_len: int = 4,
    position_bucket: int = DEFAULT_POS_BUCKET,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    include_first: bool = False,
    prompt_context: bool = False,
) -> dict[str, IndicatorHoldout]:
    extra = {}
    for name in methods:
        if name not in POS_SPECS:
            raise ValueError(f"unknown position-bucketed method: {name}")
        extra[name] = POS_SPECS[name]
    return rotate_count_methods(
        twins,
        methods=(),
        extra_specs=extra,
        context_len=context_len,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=position_bucket,
        include_first=include_first,
        prompt_context=prompt_context,
    )


def rotate_poshits(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    position_bucket: int = DEFAULT_POS_BUCKET,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
) -> IndicatorHoldout:
    return rotate_pos_methods(
        twins,
        methods=("poshits",),
        context_len=context_len,
        position_bucket=position_bucket,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
    )["poshits"]


def rotate_postokhits(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    position_bucket: int = DEFAULT_POS_BUCKET,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
) -> IndicatorHoldout:
    return rotate_pos_methods(
        twins,
        methods=("postokhits",),
        context_len=context_len,
        position_bucket=position_bucket,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
    )["postokhits"]


def rotate_postokbackoff(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    position_bucket: int = DEFAULT_POS_BUCKET,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
) -> IndicatorHoldout:
    return rotate_pos_methods(
        twins,
        methods=("postokbackoff",),
        context_len=context_len,
        position_bucket=position_bucket,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
    )["postokbackoff"]


def rotate_postokbackoff2(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    position_bucket: int = DEFAULT_POS_BUCKET,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
) -> IndicatorHoldout:
    return rotate_pos_methods(
        twins,
        methods=("postokbackoff2",),
        context_len=context_len,
        position_bucket=position_bucket,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
    )["postokbackoff2"]


def rotate_poshitmass(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    position_bucket: int = DEFAULT_POS_BUCKET,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
) -> IndicatorHoldout:
    return rotate_pos_methods(
        twins,
        methods=("poshitmass",),
        context_len=context_len,
        position_bucket=position_bucket,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
    )["poshitmass"]


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
            lambda ids, score_span=None, m=model: score_hashpool_vote(
                ids, m, score_span=score_span
            ),
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
            lambda ids, score_span=None, c=counts, h=hashed: score_hybrid(
                ids, c, h, score_span=score_span
            ),
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


def rotate_tokhybrid(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
) -> IndicatorHoldout:
    """Occupancy-free hybrid: tokhits, then hashtok. Still no keys."""

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
            lambda ids, score_span=None, c=counts, h=hashed: score_tokhybrid(
                ids, c, h, score_span=score_span
            ),
            used[0],
            used[1],
            used[2],
        )

    return rotate_custom(
        twins,
        make,
        context_len=context_len,
        model_name=model_name,
        instance="key-free-tokhybrid",
        score_kind="tokhybrid",
        margin=margin,
    )


def rotate_hashtokgap(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
) -> IndicatorHoldout:
    """Hashtok residual where exact tokhits abstains. Still no keys."""

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
            lambda ids, score_span=None, c=counts, h=hashed: score_hashtokgap(
                ids, c, h, score_span=score_span
            ),
            used[0],
            used[1],
            used[2],
        )

    return rotate_custom(
        twins,
        make,
        context_len=context_len,
        model_name=model_name,
        instance="key-free-hashtokgap",
        score_kind="hashtokgap",
        margin=margin,
    )


def rotate_poshashtok(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
    position_bucket: int = DEFAULT_POS_BUCKET,
) -> IndicatorHoldout:
    """Occupancy-free hashing with a token-position namespace. Not a key."""
    bucket = int(position_bucket) if position_bucket and position_bucket > 0 else 0
    return rotate_hashtok(
        twins,
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
        position_bucket=bucket,
        method_name="poshashtok",
    )


def rotate_hashmix(
    twins: Sequence[Twin],
    *,
    orders: Sequence[int] = (1, 2, 4),
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    context_len: int = 4,
) -> IndicatorHoldout:
    def make(train: Sequence[Twin]):
        model = fit_hashmix_twins(
            train,
            orders=orders,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
        return (
            lambda ids, score_span=None, m=model: score_hashmix(
                ids, m, score_span=score_span
            ),
            model.used_keys,
            model.used_hash_iv,
            model.used_g_values,
        )

    ctx = max(int(o) for o in orders) if orders else int(context_len)
    return rotate_custom(
        twins,
        make,
        context_len=ctx,
        model_name=model_name,
        instance="key-free-hashmix",
        score_kind="hashmix",
        margin=margin,
    )


def rotate_hashtokbackoff(
    twins: Sequence[Twin],
    *,
    orders: Sequence[int] = HASHBACKOFF_ORDERS,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    context_len: int = 4,
    min_order: int = 1,
    method_name: str = "",
    exact_len: bool = False,
) -> IndicatorHoldout:
    """Hashtok that shrinks last-k across per-order hash tables."""
    floor = max(1, int(min_order or 1))
    if method_name:
        name = str(method_name)
    elif exact_len:
        name = "hashtoklenbackoff2" if floor >= 2 else "hashtoklenbackoff"
    else:
        name = "hashtokbackoff2" if floor >= 2 else "hashtokbackoff"
    instance = f"key-free-{name}"

    def make(train: Sequence[Twin]):
        model = fit_hashmix_twins(
            train,
            orders=orders,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            exact_len=bool(exact_len),
        )
        return (
            lambda ids, score_span=None, m=model, mo=floor: score_hashtokbackoff(
                ids, m, min_order=mo, score_span=score_span
            ),
            model.used_keys,
            model.used_hash_iv,
            model.used_g_values,
        )

    ctx = max(int(o) for o in orders) if orders else int(context_len)
    return rotate_custom(
        twins,
        make,
        context_len=ctx,
        model_name=model_name,
        instance=instance,
        score_kind=name,
        margin=margin,
    )


def rotate_hashtokbackoff2(
    twins: Sequence[Twin],
    *,
    orders: Sequence[int] = HASHBACKOFF_ORDERS,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    context_len: int = 4,
) -> IndicatorHoldout:
    return rotate_hashtokbackoff(
        twins,
        orders=orders,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        context_len=context_len,
        min_order=2,
        method_name="hashtokbackoff2",
    )


def rotate_hashtoklenbackoff(
    twins: Sequence[Twin],
    *,
    orders: Sequence[int] = HASHBACKOFF_ORDERS,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    context_len: int = 4,
) -> IndicatorHoldout:
    return rotate_hashtokbackoff(
        twins,
        orders=orders,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        context_len=context_len,
        min_order=1,
        method_name="hashtoklenbackoff",
        exact_len=True,
    )


def rotate_hashtoklenbackoff2(
    twins: Sequence[Twin],
    *,
    orders: Sequence[int] = HASHBACKOFF_ORDERS,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    context_len: int = 4,
) -> IndicatorHoldout:
    return rotate_hashtokbackoff(
        twins,
        orders=orders,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        model_name=model_name,
        margin=margin,
        context_len=context_len,
        min_order=2,
        method_name="hashtoklenbackoff2",
        exact_len=True,
    )


def rotate_surface(
    twins: Sequence[Twin],
    *,
    context_len: int = DEFAULT_SURFACE_CONTEXT,
    n_hashes: int = 8,
    n_buckets: int = 256,
    model_name: str = "gpt2",
    margin: float = 0.0,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, IndicatorHoldout] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], IndicatorHoldout] | None = None,
) -> IndicatorHoldout:
    def make(train: Sequence[Twin]):
        model = fit_surface_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
        return (
            lambda text, m=model: score_surface(text, m),
            model.used_keys,
            model.used_hash_iv,
            model.used_g_values,
        )

    return rotate_custom(
        twins,
        make,
        context_len=context_len,
        model_name=model_name,
        instance="key-free-surface",
        score_kind="surface",
        margin=margin,
        seq_mode="text",
        prefix_lens=prefix_lens,
        prefix_out=prefix_out,
        windows=windows,
        window_out=window_out,
    )

def swap_twin_sides(twin: Twin) -> Twin:
    return Twin(
        stem=twin.stem,
        marked_text=twin.unmarked_text,
        unmarked_text=twin.marked_text,
        marked_ids=list(twin.unmarked_ids),
        unmarked_ids=list(twin.marked_ids),
        extra_marked_ids=[list(x) for x in twin.extra_unmarked_ids],
        extra_unmarked_ids=[list(x) for x in twin.extra_marked_ids],
        extra_marked_text=list(twin.extra_unmarked_text),
        extra_unmarked_text=list(twin.extra_marked_text),
        prompt_text=twin.prompt_text,
        prompt_ids=list(twin.prompt_ids),
    )


def shuffle_twin_sides(twins: Sequence[Twin], *, seed: int = 0) -> list[Twin]:
    """Swap marked/unmarked on a seeded half of the stems. A negative control."""
    import random

    rng = random.Random(seed)
    order = list(range(len(twins)))
    rng.shuffle(order)
    swap = set(order[: len(twins) // 2])
    out: list[Twin] = []
    for i, twin in enumerate(twins):
        if i in swap:
            out.append(swap_twin_sides(twin))
        else:
            out.append(twin)
    return out


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


def _holdouts_as_series(
    holdouts: Sequence[IndicatorHoldout],
) -> list[list[tuple[str, int, float, float]]]:
    series = [_aligned_rows(ev) for ev in holdouts]
    n = len(series[0])
    if n == 0 or any(len(s) != n for s in series):
        raise ValueError("stacked holdouts have different lengths")
    keys = [(row[0], row[1]) for row in series[0]]
    for other in series[1:]:
        if [(row[0], row[1]) for row in other] != keys:
            raise ValueError("stacked holdouts are not aligned")
    return series


def rotate_score_logit(
    holdouts: Sequence[IndicatorHoldout],
    *,
    model_name: str = "gpt2",
    score_kind: str = "logit",
    instance: str = "key-free-logit",
    ridge: float = 1.0,
) -> IndicatorHoldout:
    """Leave-one-prompt-out ridge logistic on already-computed file scores.

    Features are z-scored on the training prompts of each fold. Threshold 0
    is a 50% log-odds. Still no keys / hash_iv / g-values.
    """
    if len(holdouts) < 2:
        raise ValueError("logit stack needs at least two methods")
    series = _holdouts_as_series(holdouts)
    import numpy as np

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
        weights, intercept, mu, sd = fit_ridge_logodds(
            np.asarray(train_m, dtype=np.float64),
            np.asarray(train_u, dtype=np.float64),
            ridge=ridge,
        )
        for i in held_idx:
            stem, sample, _m, _u = series[0][i]
            vm = [s[i][2] for s in series]
            vu = [s[i][3] for s in series]
            _append_pair(
                parts,
                stem,
                sample,
                score_ridge_logodds(vm, weights, intercept, mu, sd),
                score_ridge_logodds(vu, weights, intercept, mu, sd),
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


def combine_holdouts_logit(
    train_holdouts: Sequence[IndicatorHoldout],
    test_holdouts: Sequence[IndicatorHoldout],
    *,
    model_name: str = "gpt2",
    ridge: float = 1.0,
) -> tuple[IndicatorHoldout, IndicatorHoldout]:
    """Fit ridge logistic on train file scores; apply to train and test."""
    if len(train_holdouts) < 2 or len(train_holdouts) != len(test_holdouts):
        raise ValueError("logit combine needs matching train/test holdout lists")
    import numpy as np

    tr = _holdouts_as_series(train_holdouts)
    te = _holdouts_as_series(test_holdouts)
    train_m = np.asarray([[s[i][2] for s in tr] for i in range(len(tr[0]))], dtype=np.float64)
    train_u = np.asarray([[s[i][3] for s in tr] for i in range(len(tr[0]))], dtype=np.float64)
    weights, intercept, mu, sd = fit_ridge_logodds(train_m, train_u, ridge=ridge)
    flags = dict(
        context_len=0,
        model_name=model_name,
        instance="key-free-logit",
        score_kind="logit",
        used_keys=any(ev.used_keys for ev in train_holdouts),
        used_hash_iv=any(ev.used_hash_iv for ev in train_holdouts),
        used_g_values=any(ev.used_g_values for ev in train_holdouts),
    )
    train_parts = _empty_holdout_parts()
    test_parts = _empty_holdout_parts()
    for i, (stem, sample, _m, _u) in enumerate(tr[0]):
        vm = [s[i][2] for s in tr]
        vu = [s[i][3] for s in tr]
        _append_pair(
            train_parts,
            stem,
            sample,
            score_ridge_logodds(vm, weights, intercept, mu, sd),
            score_ridge_logodds(vu, weights, intercept, mu, sd),
        )
    for i, (stem, sample, _m, _u) in enumerate(te[0]):
        vm = [s[i][2] for s in te]
        vu = [s[i][3] for s in te]
        _append_pair(
            test_parts,
            stem,
            sample,
            score_ridge_logodds(vm, weights, intercept, mu, sd),
            score_ridge_logodds(vu, weights, intercept, mu, sd),
        )
    return (
        _holdout_from_parts(train_parts, mode="train", **flags),
        _holdout_from_parts(test_parts, mode="transfer", **flags),
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
    seq_mode: str = "ids",
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, IndicatorHoldout] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], IndicatorHoldout] | None = None,
    prompt_context: bool = False,
) -> IndicatorHoldout:
    parts = _empty_holdout_parts()
    lenses = _parse_prefix_lens(prefix_lens)
    spans = _parse_windows(windows)
    prefix_parts = {n: _empty_holdout_parts() for n in lenses}
    window_parts = {win: _empty_holdout_parts() for win in spans}
    for twin in twins:
        marked_seqs, unmarked_seqs = _twin_sides(twin, seq_mode)
        held_prefix = _twin_prefix(twin, prompt_context) if seq_mode == "ids" else ()
        n = min(len(marked_seqs), len(unmarked_seqs))
        for i in range(n):
            marked = marked_seqs[i]
            unmarked = unmarked_seqs[i]
            _append_pair(
                parts,
                twin.stem,
                i + 1,
                _call_scorer(scorer, marked, prefix=held_prefix),
                _call_scorer(scorer, unmarked, prefix=held_prefix),
            )
            for plen in lenses:
                _append_pair(
                    prefix_parts[plen],
                    twin.stem,
                    i + 1,
                    _call_scorer(scorer, clip_seq(marked, plen), prefix=held_prefix),
                    _call_scorer(scorer, clip_seq(unmarked, plen), prefix=held_prefix),
                )
            for start, end in spans:
                _append_pair(
                    window_parts[(start, end)],
                    twin.stem,
                    i + 1,
                    _call_scorer(
                        scorer,
                        marked if seq_mode != "text" else slice_seq(marked, start, end),
                        prefix=held_prefix if seq_mode != "text" else (),
                        score_span=(start, end) if seq_mode != "text" else None,
                    ),
                    _call_scorer(
                        scorer,
                        unmarked if seq_mode != "text" else slice_seq(unmarked, start, end),
                        prefix=held_prefix if seq_mode != "text" else (),
                        score_span=(start, end) if seq_mode != "text" else None,
                    ),
                )
    flags = dict(
        used_keys=used_keys,
        used_hash_iv=used_hash_iv,
        used_g_values=used_g_values,
        mode=mode,
    )
    if prefix_out is not None:
        for plen in lenses:
            prefix_out[plen] = _holdout_from_parts(
                prefix_parts[plen],
                context_len=context_len,
                model_name=model_name,
                instance=instance,
                score_kind=f"{score_kind}@p{plen}",
                **flags,
            )
    if window_out is not None:
        for start, end in spans:
            window_out[(start, end)] = _holdout_from_parts(
                window_parts[(start, end)],
                context_len=context_len,
                model_name=model_name,
                instance=instance,
                score_kind=f"{score_kind}@w{start}-{end}",
                **flags,
            )
    return _holdout_from_parts(
        parts,
        context_len=context_len,
        model_name=model_name,
        instance=instance,
        score_kind=score_kind,
        **flags,
    )



def rotate_pivot(
    twins: Sequence[Twin],
    *,
    model_name: str = "gpt2",
    top_k: int = 40,
    margin: float = 0.0,
    lm: object | None = None,
    prompt_context: bool = False,
    weights: Sequence[str] = ("uniform",),
    mats=None,
) -> dict[str, IndicatorHoldout]:
    """Leave-one-prompt-out LDA and rank baseline on unmarked-LM features."""
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.pivot import (
        collect_choice_matrices,
        fit_pivot_from_vectors,
        parse_pivot_weights,
        pivot_method_name,
        score_pivot_lda,
        score_pivot_rank,
        vectors_from_matrices,
    )

    if mats is None:
        if lm is None:
            lm = _load_unmarked_model(generate_device(), model_name=model_name)
        mats = collect_choice_matrices(
            twins, lm, top_k=top_k, prompt_context=prompt_context
        )
    weight_names = parse_pivot_weights(weights)
    used_keys = used_hash = used_g = False
    out: dict[str, IndicatorHoldout] = {}
    ctx = 0
    flags = dict(
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
        margin=margin,
        model_name=model_name,
        context_len=ctx,
    )
    for weight in weight_names:
        vecs = vectors_from_matrices(mats, weight=weight)
        lda_parts = _empty_holdout_parts()
        rank_parts = _empty_holdout_parts()
        for held in twins:
            train_stems = [t.stem for t in twins if t.stem != held.stem]
            fit = fit_pivot_from_vectors(vecs, train_stems)
            used_keys = used_keys or fit.used_keys
            used_hash = used_hash or fit.used_hash_iv
            used_g = used_g or fit.used_g_values
            n = min(len(held.marked_seqs()), len(held.unmarked_seqs()))
            for i in range(n):
                sample = i + 1
                vm = vecs[(held.stem, sample, "marked")]
                vu = vecs[(held.stem, sample, "unmarked")]
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
        flags = dict(
            used_keys=used_keys,
            used_hash_iv=used_hash,
            used_g_values=used_g,
            margin=margin,
            model_name=model_name,
            context_len=ctx,
        )
        out[pivot_method_name("lda", weight)] = _holdout_from_parts(
            lda_parts,
            instance=f"key-free-{pivot_method_name('lda', weight)}",
            score_kind=pivot_method_name("lda", weight),
            **flags,
        )
        out[pivot_method_name("rank", weight)] = _holdout_from_parts(
            rank_parts,
            instance=f"key-free-{pivot_method_name('rank', weight)}",
            score_kind=pivot_method_name("rank", weight),
            **flags,
        )
    return out


def transfer_pivot(
    train: Sequence[Twin],
    test: Sequence[Twin],
    *,
    model_name: str = "gpt2",
    top_k: int = 40,
    lm: object | None = None,
    prompt_context: bool = False,
    weights: Sequence[str] = ("uniform",),
    train_mats=None,
    test_mats=None,
) -> tuple[dict[str, IndicatorHoldout], dict[str, IndicatorHoldout], dict]:
    """Fit unmarked-LM geometry on train twins, score test twins. No keys."""
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.pivot import (
        collect_choice_matrices,
        fit_pivot_from_vectors,
        parse_pivot_weights,
        pivot_method_name,
        score_pivot_lda,
        score_pivot_rank,
        vectors_from_matrices,
    )

    if train_mats is None or test_mats is None:
        if lm is None:
            lm = _load_unmarked_model(generate_device(), model_name=model_name)
        if train_mats is None:
            train_mats = collect_choice_matrices(
                train, lm, top_k=top_k, prompt_context=prompt_context
            )
        if test_mats is None:
            test_mats = collect_choice_matrices(
                test, lm, top_k=top_k, prompt_context=prompt_context
            )
    weight_names = parse_pivot_weights(weights)
    train_stems = [t.stem for t in train]
    train_out: dict[str, IndicatorHoldout] = {}
    test_out: dict[str, IndicatorHoldout] = {}
    fits: dict[str, object] = {}
    for weight in weight_names:
        train_vecs = vectors_from_matrices(train_mats, weight=weight)
        test_vecs = vectors_from_matrices(test_mats, weight=weight)
        fit = fit_pivot_from_vectors(train_vecs, train_stems)
        fits[weight] = fit
        train_lda = _empty_holdout_parts()
        train_rank = _empty_holdout_parts()
        test_lda = _empty_holdout_parts()
        test_rank = _empty_holdout_parts()
        for twin in train:
            n = min(len(twin.marked_seqs()), len(twin.unmarked_seqs()))
            for i in range(n):
                sample = i + 1
                vm = train_vecs[(twin.stem, sample, "marked")]
                vu = train_vecs[(twin.stem, sample, "unmarked")]
                _append_pair(
                    train_lda,
                    twin.stem,
                    sample,
                    score_pivot_lda(vm, fit),
                    score_pivot_lda(vu, fit),
                )
                _append_pair(
                    train_rank,
                    twin.stem,
                    sample,
                    score_pivot_rank(vm, fit),
                    score_pivot_rank(vu, fit),
                )
        for twin in test:
            n = min(len(twin.marked_seqs()), len(twin.unmarked_seqs()))
            for i in range(n):
                sample = i + 1
                vm = test_vecs[(twin.stem, sample, "marked")]
                vu = test_vecs[(twin.stem, sample, "unmarked")]
                _append_pair(
                    test_lda,
                    twin.stem,
                    sample,
                    score_pivot_lda(vm, fit),
                    score_pivot_lda(vu, fit),
                )
                _append_pair(
                    test_rank,
                    twin.stem,
                    sample,
                    score_pivot_rank(vm, fit),
                    score_pivot_rank(vu, fit),
                )
        flags = dict(
            used_keys=fit.used_keys,
            used_hash_iv=fit.used_hash_iv,
            used_g_values=fit.used_g_values,
            model_name=model_name,
            context_len=0,
        )
        lda_name = pivot_method_name("lda", weight)
        rank_name = pivot_method_name("rank", weight)
        train_out[lda_name] = _holdout_from_parts(
            train_lda,
            instance=f"key-free-{lda_name}",
            score_kind=lda_name,
            mode="train",
            **flags,
        )
        train_out[rank_name] = _holdout_from_parts(
            train_rank,
            instance=f"key-free-{rank_name}",
            score_kind=rank_name,
            mode="train",
            **flags,
        )
        test_out[lda_name] = _holdout_from_parts(
            test_lda,
            instance=f"key-free-{lda_name}",
            score_kind=lda_name,
            mode="transfer",
            **flags,
        )
        test_out[rank_name] = _holdout_from_parts(
            test_rank,
            instance=f"key-free-{rank_name}",
            score_kind=rank_name,
            mode="transfer",
            **flags,
        )
    return test_out, train_out, fits



def _snaprate_holdout_from_twins(
    twins: Sequence[Twin],
    mats: dict,
    *,
    kind: str,
    model_name: str,
    score_kind: str,
    mode: str,
) -> IndicatorHoldout:
    from text_watermark_tools.pivot import snap_score_from_matrix

    parts = _empty_holdout_parts()
    empty = None
    for twin in twins:
        n = min(len(twin.marked_seqs()), len(twin.unmarked_seqs()))
        for i in range(n):
            sample = i + 1
            marked = mats.get((twin.stem, sample, "marked"), empty)
            unmarked = mats.get((twin.stem, sample, "unmarked"), empty)
            _append_pair(
                parts,
                twin.stem,
                sample,
                snap_score_from_matrix(marked, kind),
                snap_score_from_matrix(unmarked, kind),
            )
    return _holdout_from_parts(
        parts,
        context_len=0,
        model_name=model_name,
        instance=f"key-free-{score_kind}",
        score_kind=score_kind,
        mode=mode,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )


def rotate_snaprate(
    twins: Sequence[Twin],
    *,
    model_name: str = "gpt2",
    top_k: int = 40,
    lm: object | None = None,
    prompt_context: bool = False,
    methods: Sequence[str] = ("snapleave", "snapupset", "snapmiss"),
    mats=None,
) -> dict[str, IndicatorHoldout]:
    """Table-free unmarked-LM snap rates. No twin tables, no leave-one-out fit."""
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.pivot import (
        SNAPRATE_METHODS,
        collect_choice_matrices,
        parse_snaprate_methods,
    )

    names = parse_snaprate_methods(methods)
    if mats is None:
        if lm is None:
            lm = _load_unmarked_model(generate_device(), model_name=model_name)
        mats = collect_choice_matrices(
            twins, lm, top_k=top_k, prompt_context=prompt_context
        )
    return {
        name: _snaprate_holdout_from_twins(
            twins,
            mats,
            kind=SNAPRATE_METHODS[name],
            model_name=model_name,
            score_kind=name,
            mode="rotate",
        )
        for name in names
    }


def transfer_snaprate(
    train: Sequence[Twin],
    test: Sequence[Twin],
    *,
    model_name: str = "gpt2",
    top_k: int = 40,
    lm: object | None = None,
    prompt_context: bool = False,
    methods: Sequence[str] = ("snapleave", "snapupset", "snapmiss"),
    train_mats=None,
    test_mats=None,
) -> tuple[dict[str, IndicatorHoldout], dict[str, IndicatorHoldout]]:
    """Score train and test with the same table-free snap rates. No fit."""
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.pivot import (
        SNAPRATE_METHODS,
        collect_choice_matrices,
        parse_snaprate_methods,
    )

    names = parse_snaprate_methods(methods)
    if train_mats is None or test_mats is None:
        if lm is None:
            lm = _load_unmarked_model(generate_device(), model_name=model_name)
        if train_mats is None:
            train_mats = collect_choice_matrices(
                train, lm, top_k=top_k, prompt_context=prompt_context
            )
        if test_mats is None:
            test_mats = collect_choice_matrices(
                test, lm, top_k=top_k, prompt_context=prompt_context
            )
    train_out: dict[str, IndicatorHoldout] = {}
    test_out: dict[str, IndicatorHoldout] = {}
    for name in names:
        kind = SNAPRATE_METHODS[name]
        train_out[name] = _snaprate_holdout_from_twins(
            train,
            train_mats,
            kind=kind,
            model_name=model_name,
            score_kind=name,
            mode="train",
        )
        test_out[name] = _snaprate_holdout_from_twins(
            test,
            test_mats,
            kind=kind,
            model_name=model_name,
            score_kind=name,
            mode="transfer",
        )
    return test_out, train_out



def rotate_rankpath(
    twins: Sequence[Twin],
    *,
    model_name: str = "gpt2",
    top_k: int = 40,
    context_len: int = 3,
    position_bucket: int = 1,
    lm: object | None = None,
    prompt_context: bool = False,
    methods: Sequence[str] = ("rankpath", "rankuni"),
    mats=None,
    span_mats=None,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
) -> dict[str, IndicatorHoldout]:
    """Leave-one-prompt-out next-symbol LR on unmarked-LM rank paths."""
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.pivot import collect_choice_matrices
    from text_watermark_tools.rankpath import (
        RANKPATH_SPECS,
        fit_rankpath_from_symbols,
        score_rankpath,
        slice_symbols,
        symbols_from_matrices,
    )

    names = [n for n in methods if n in RANKPATH_SPECS]
    if not names:
        raise ValueError("rotate_rankpath needs rankpath, rankuni, or rankhits")
    if mats is None:
        if lm is None:
            lm = _load_unmarked_model(generate_device(), model_name=model_name)
        mats = collect_choice_matrices(
            twins, lm, top_k=top_k, prompt_context=prompt_context
        )
    symbols = symbols_from_matrices(mats, top_k=top_k)
    span_symbols = (
        symbols_from_matrices(span_mats, top_k=top_k)
        if span_mats is not None
        else symbols
    )
    lenses = _parse_prefix_lens(prefix_lens)
    spans = _parse_windows(windows)
    bucket = int(position_bucket) if position_bucket and position_bucket > 0 else 0

    def _loo(sym_dict, *, score_kind_suffix: str = "") -> dict[str, IndicatorHoldout]:
        parts = {name: _empty_holdout_parts() for name in names}
        used_keys = used_hash = used_g = False
        for held in twins:
            train_stems = [t.stem for t in twins if t.stem != held.stem]
            model = fit_rankpath_from_symbols(
                sym_dict,
                train_stems,
                context_len=context_len,
                position_bucket=bucket,
            )
            used_keys = used_keys or model.used_keys
            used_hash = used_hash or model.used_hash_iv
            used_g = used_g or model.used_g_values
            n = min(len(held.marked_seqs()), len(held.unmarked_seqs()))
            for i in range(n):
                sample = i + 1
                ids_m = sym_dict.get((held.stem, sample, "marked"), [])
                ids_u = sym_dict.get((held.stem, sample, "unmarked"), [])
                for name in names:
                    spec = RANKPATH_SPECS[name]
                    _append_pair(
                        parts[name],
                        held.stem,
                        sample,
                        score_rankpath(ids_m, model, spec=spec),
                        score_rankpath(ids_u, model, spec=spec),
                    )
        flags = dict(
            used_keys=used_keys,
            used_hash_iv=used_hash,
            used_g_values=used_g,
            model_name=model_name,
            context_len=context_len,
        )
        return {
            name: _holdout_from_parts(
                parts[name],
                instance=RANKPATH_SPECS[name].instance,
                score_kind=name + score_kind_suffix,
                **flags,
            )
            for name in names
        }

    out = _loo(symbols)
    if prefix_out is not None:
        for plen in lenses:
            sliced = _loo(slice_symbols(span_symbols, 0, plen), score_kind_suffix=f"@p{plen}")
            prefix_out.setdefault(plen, {}).update(sliced)
    if window_out is not None:
        for start, end in spans:
            sliced = _loo(
                slice_symbols(span_symbols, start, end),
                score_kind_suffix=f"@{start}:{end}",
            )
            window_out.setdefault((start, end), {}).update(sliced)
    return out


def transfer_rankpath(
    train: Sequence[Twin],
    test: Sequence[Twin],
    *,
    model_name: str = "gpt2",
    top_k: int = 40,
    context_len: int = 3,
    position_bucket: int = 1,
    lm: object | None = None,
    prompt_context: bool = False,
    methods: Sequence[str] = ("rankpath", "rankuni"),
    train_mats=None,
    test_mats=None,
    span_train_mats=None,
    span_test_mats=None,
    prefix_lens: Sequence[int] = (),
    prefix_out: dict[int, dict[str, IndicatorHoldout]] | None = None,
    windows: Sequence[str | tuple[int, int]] = (),
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] | None = None,
):
    """Fit rank-path tables on train twins, score test. Isolated-file protocol."""
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.pivot import collect_choice_matrices
    from text_watermark_tools.rankpath import (
        RANKPATH_SPECS,
        fit_rankpath_from_symbols,
        score_rankpath,
        slice_symbols,
        symbols_from_matrices,
    )

    names = [n for n in methods if n in RANKPATH_SPECS]
    if not names:
        raise ValueError("transfer_rankpath needs rankpath, rankuni, or rankhits")
    if lm is None and (train_mats is None or test_mats is None):
        lm = _load_unmarked_model(generate_device(), model_name=model_name)
    if train_mats is None:
        train_mats = collect_choice_matrices(
            train, lm, top_k=top_k, prompt_context=prompt_context
        )
    if test_mats is None:
        test_mats = collect_choice_matrices(
            test, lm, top_k=top_k, prompt_context=prompt_context
        )
    train_sym = symbols_from_matrices(train_mats, top_k=top_k)
    test_sym = symbols_from_matrices(test_mats, top_k=top_k)
    span_train = (
        symbols_from_matrices(span_train_mats, top_k=top_k)
        if span_train_mats is not None
        else train_sym
    )
    span_test = (
        symbols_from_matrices(span_test_mats, top_k=top_k)
        if span_test_mats is not None
        else test_sym
    )
    all_sym = {**train_sym, **test_sym}
    bucket = int(position_bucket) if position_bucket and position_bucket > 0 else 0
    model = fit_rankpath_from_symbols(
        train_sym,
        [t.stem for t in train],
        context_len=context_len,
        position_bucket=bucket,
    )
    lenses = _parse_prefix_lens(prefix_lens)
    spans = _parse_windows(windows)

    def _side(twins, symbols, mode: str, fit) -> dict[str, IndicatorHoldout]:
        parts = {name: _empty_holdout_parts() for name in names}
        for twin in twins:
            n = min(len(twin.marked_seqs()), len(twin.unmarked_seqs()))
            for i in range(n):
                sample = i + 1
                ids_m = symbols.get((twin.stem, sample, "marked"), [])
                ids_u = symbols.get((twin.stem, sample, "unmarked"), [])
                for name in names:
                    spec = RANKPATH_SPECS[name]
                    _append_pair(
                        parts[name],
                        twin.stem,
                        sample,
                        score_rankpath(ids_m, fit, spec=spec),
                        score_rankpath(ids_u, fit, spec=spec),
                    )
        flags = dict(
            used_keys=fit.used_keys,
            used_hash_iv=fit.used_hash_iv,
            used_g_values=fit.used_g_values,
            model_name=model_name,
            context_len=context_len,
            mode=mode,
        )
        return {
            name: _holdout_from_parts(
                parts[name],
                instance=RANKPATH_SPECS[name].instance,
                score_kind=name,
                **flags,
            )
            for name in names
        }

    test_out = _side(test, test_sym, "transfer", model)
    train_out = _side(train, train_sym, "train", model)
    if prefix_out is not None:
        for plen in lenses:
            sliced_train = slice_symbols(span_train, 0, plen)
            sliced_test = slice_symbols(span_test, 0, plen)
            fit = fit_rankpath_from_symbols(
                sliced_train,
                [t.stem for t in train],
                context_len=context_len,
                position_bucket=bucket,
            )
            prefix_out.setdefault(plen, {}).update(
                _side(test, sliced_test, "transfer", fit)
            )
    if window_out is not None:
        for start, end in spans:
            sliced_train = slice_symbols(span_train, start, end)
            sliced_test = slice_symbols(span_test, start, end)
            fit = fit_rankpath_from_symbols(
                sliced_train,
                [t.stem for t in train],
                context_len=context_len,
                position_bucket=bucket,
            )
            window_out.setdefault((start, end), {}).update(
                _side(test, sliced_test, "transfer", fit)
            )
    return test_out, train_out, model, all_sym



def rotate_cascade(
    twins: Sequence[Twin],
    *,
    spec: ScoreSpec | None = None,
    position_bucket: int = 1,
    context_len: int = 4,
    include_first: bool = False,
    model_name: str = "gpt2",
    top_k: int = 40,
    lm: object | None = None,
    prompt_context: bool = False,
    pivot_weight: str = "entropy",
    count_prompt_context: bool = False,
    fallback: str = "pivot",
    mats=None,
    rankpath_pos_bucket: int | None = None,
    cascade_when: str = "coverage",
    hashed_reader: str = "",
    n_hashes: int = 8,
    n_buckets: int = 256,
) -> tuple[IndicatorHoldout, list[dict]]:
    """LOO: count LR when the cascade-when rule fires, else unmarked-LM fallback."""
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.pivot import (
        cascade_score,
        cascade_source,
        collect_choice_matrices,
        fit_pivot_from_vectors,
        parse_cascade_when,
        vectors_from_matrices,
    )
    from text_watermark_tools.rankpath import (
        RANKPATH_SPECS,
        fit_rankpath_from_symbols,
        parse_cascade_fallback,
        symbols_from_matrices,
    )
    from text_watermark_tools.score import load_tokenizer
    from text_watermark_tools.atoms import decode_token
    from text_watermark_tools.transfer import fit_count_model, score_sequence_detail

    fallback = parse_cascade_fallback(fallback)
    when = parse_cascade_when(cascade_when)
    if mats is None:
        if lm is None:
            lm = _load_unmarked_model(generate_device(), model_name=model_name)
        mats = collect_choice_matrices(
            twins, lm, top_k=top_k, prompt_context=prompt_context
        )
    tok = load_tokenizer(model_name)
    vecs = vectors_from_matrices(mats, weight=pivot_weight)
    symbols = symbols_from_matrices(mats, top_k=top_k) if fallback != "pivot" else {}
    rank_spec = RANKPATH_SPECS.get(fallback)
    parts = _empty_holdout_parts()
    rows: list[dict] = []
    used_keys = used_hash = used_g = False
    bucket = int(position_bucket) if position_bucket and position_bucket > 0 else 0
    if rankpath_pos_bucket is None:
        rank_bucket = bucket
    else:
        rank_bucket = int(rankpath_pos_bucket) if rankpath_pos_bucket > 0 else 0
    for held in twins:
        train = [t for t in twins if t.stem != held.stem]
        hashed = str(hashed_reader or "").strip()
        count_detail = None
        model = None
        if hashed:
            models = _hashed_cascade_models(
                train,
                hashed,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
            )
            count_detail = hashed_count_detail(hashed, models)
            model = _hashed_flag_model(models)
        else:
            if spec is None:
                raise ValueError("count cascade needs a ScoreSpec")
            model = fit_count_model(
                train,
                context_len=context_len,
                position_bucket=bucket,
                include_first=include_first,
                prompt_context=count_prompt_context,
            )
            model.include_first = bool(include_first)
        used_keys = used_keys or bool(getattr(model, "used_keys", False))
        used_hash = used_hash or bool(getattr(model, "used_hash_iv", False))
        used_g = used_g or bool(getattr(model, "used_g_values", False))
        fit = None
        rank_model = None
        if fallback == "pivot":
            fit = fit_pivot_from_vectors(vecs, [t.stem for t in train])
            used_keys = used_keys or fit.used_keys
            used_hash = used_hash or fit.used_hash_iv
            used_g = used_g or fit.used_g_values
        else:
            rank_model = fit_rankpath_from_symbols(
                symbols,
                [t.stem for t in train],
                context_len=min(context_len, 3),
                position_bucket=rank_bucket,
            )
            used_keys = used_keys or rank_model.used_keys
            used_hash = used_hash or rank_model.used_hash_iv
            used_g = used_g or rank_model.used_g_values
        count_prefix = _twin_prefix(held, count_prompt_context)
        n = min(len(held.marked_seqs()), len(held.unmarked_seqs()))
        for i in range(n):
            sample = i + 1
            ids_m = held.marked_seqs()[i]
            ids_u = held.unmarked_seqs()[i]
            if count_detail is not None:
                dm = count_detail(ids_m)
                du = count_detail(ids_u)
            else:
                dm = score_sequence_detail(ids_m, model, spec, prefix=count_prefix)
                du = score_sequence_detail(ids_u, model, spec, prefix=count_prefix)
            pm = _cascade_fallback_lr(
                fallback,
                stem=held.stem,
                sample=sample,
                side="marked",
                vecs=vecs,
                pivot_fit=fit,
                symbols=symbols,
                rank_model=rank_model,
                rank_spec=rank_spec,
            )
            pu = _cascade_fallback_lr(
                fallback,
                stem=held.stem,
                sample=sample,
                side="unmarked",
                vecs=vecs,
                pivot_fit=fit,
                symbols=symbols,
                rank_model=rank_model,
                rank_spec=rank_spec,
            )
            sm = cascade_score(dm.lr, dm.n_used, pm, when=when)
            su = cascade_score(du.lr, du.n_used, pu, when=when)
            _append_pair(parts, held.stem, sample, sm, su)
            opening = "".join(decode_token(tok, t) for t in ids_m[:4]).strip()
            rows.append(
                {
                    "stem": held.stem,
                    "sample": sample,
                    "side": "marked",
                    "n_used": dm.n_used,
                    "count_lr": dm.lr,
                    "pivot_lr": pm,
                    "source": cascade_source(
                        dm.n_used, fallback, count_lr=dm.lr, when=when
                    ),
                    "score": sm,
                    "opening_text": opening,
                    "cascade_when": when,
                }
            )
            rows.append(
                {
                    "stem": held.stem,
                    "sample": sample,
                    "side": "unmarked",
                    "n_used": du.n_used,
                    "count_lr": du.lr,
                    "pivot_lr": pu,
                    "source": cascade_source(
                        du.n_used, fallback, count_lr=du.lr, when=when
                    ),
                    "score": su,
                    "opening_text": "",
                    "cascade_when": when,
                }
            )
    ev = _holdout_from_parts(
        parts,
        context_len=context_len,
        model_name=model_name,
        instance="key-free-cascade",
        score_kind="cascade",
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
    )
    return ev, rows


def transfer_cascade(
    train: Sequence[Twin],
    test: Sequence[Twin],
    *,
    spec: ScoreSpec | None = None,
    position_bucket: int = 1,
    context_len: int = 4,
    include_first: bool = False,
    model_name: str = "gpt2",
    top_k: int = 40,
    lm: object | None = None,
    prompt_context: bool = False,
    pivot_weight: str = "entropy",
    count_prompt_context: bool = False,
    pos_model=None,
    fallback: str = "pivot",
    train_mats=None,
    test_mats=None,
    rank_model=None,
    rankpath_pos_bucket: int | None = None,
    cascade_when: str = "coverage",
    hashed_reader: str = "",
    n_hashes: int = 8,
    n_buckets: int = 256,
    count_detail=None,
    flag_model=None,
) -> tuple[IndicatorHoldout, IndicatorHoldout, list[dict]]:
    """Train count+fallback on one corpus, score the other. Isolated-file cascade."""
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.pivot import (
        cascade_score,
        cascade_source,
        collect_choice_matrices,
        fit_pivot_from_vectors,
        parse_cascade_when,
        vectors_from_matrices,
    )
    from text_watermark_tools.rankpath import (
        RANKPATH_SPECS,
        fit_rankpath_from_symbols,
        parse_cascade_fallback,
        symbols_from_matrices,
    )
    from text_watermark_tools.score import load_tokenizer
    from text_watermark_tools.atoms import decode_token
    from text_watermark_tools.transfer import fit_count_model, score_sequence_detail

    fallback = parse_cascade_fallback(fallback)
    when = parse_cascade_when(cascade_when)
    if lm is None and (train_mats is None or test_mats is None):
        lm = _load_unmarked_model(generate_device(), model_name=model_name)
    tok = load_tokenizer(model_name)
    bucket = int(position_bucket) if position_bucket and position_bucket > 0 else 0
    if rankpath_pos_bucket is None:
        rank_bucket = bucket
    else:
        rank_bucket = int(rankpath_pos_bucket) if rankpath_pos_bucket > 0 else 0
    hashed = str(hashed_reader or "").strip()
    if count_detail is None and hashed:
        models = _hashed_cascade_models(
            train,
            hashed,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
        count_detail = hashed_count_detail(hashed, models)
        flag_model = _hashed_flag_model(models)
    if count_detail is None:
        if spec is None:
            raise ValueError("count cascade needs a ScoreSpec")
        model = pos_model or fit_count_model(
            train,
            context_len=context_len,
            position_bucket=bucket,
            include_first=include_first,
            prompt_context=count_prompt_context,
        )
        model.include_first = bool(include_first)
    else:
        model = flag_model
    if train_mats is None:
        train_mats = collect_choice_matrices(
            train, lm, top_k=top_k, prompt_context=prompt_context
        )
    if test_mats is None:
        test_mats = collect_choice_matrices(
            test, lm, top_k=top_k, prompt_context=prompt_context
        )
    train_vecs = vectors_from_matrices(train_mats, weight=pivot_weight)
    test_vecs = vectors_from_matrices(test_mats, weight=pivot_weight)
    fit = None
    symbols: dict = {}
    rank_spec = RANKPATH_SPECS.get(fallback)
    if fallback == "pivot":
        fit = fit_pivot_from_vectors(train_vecs, [t.stem for t in train])
    else:
        train_sym = symbols_from_matrices(train_mats, top_k=top_k)
        test_sym = symbols_from_matrices(test_mats, top_k=top_k)
        symbols = {**train_sym, **test_sym}
        if rank_model is None:
            rank_model = fit_rankpath_from_symbols(
                train_sym,
                [t.stem for t in train],
                context_len=min(context_len, 3),
                position_bucket=rank_bucket,
            )

    def _score_side(twins, vecs, mode: str) -> tuple[dict, list[dict]]:
        parts = _empty_holdout_parts()
        rows: list[dict] = []
        for twin in twins:
            prefix = _twin_prefix(twin, count_prompt_context)
            n = min(len(twin.marked_seqs()), len(twin.unmarked_seqs()))
            for i in range(n):
                sample = i + 1
                ids_m = twin.marked_seqs()[i]
                ids_u = twin.unmarked_seqs()[i]
                if count_detail is not None:
                    dm = count_detail(ids_m)
                    du = count_detail(ids_u)
                else:
                    dm = score_sequence_detail(ids_m, model, spec, prefix=prefix)
                    du = score_sequence_detail(ids_u, model, spec, prefix=prefix)
                pm = _cascade_fallback_lr(
                    fallback,
                    stem=twin.stem,
                    sample=sample,
                    side="marked",
                    vecs=vecs,
                    pivot_fit=fit,
                    symbols=symbols,
                    rank_model=rank_model,
                    rank_spec=rank_spec,
                )
                pu = _cascade_fallback_lr(
                    fallback,
                    stem=twin.stem,
                    sample=sample,
                    side="unmarked",
                    vecs=vecs,
                    pivot_fit=fit,
                    symbols=symbols,
                    rank_model=rank_model,
                    rank_spec=rank_spec,
                )
                sm = cascade_score(dm.lr, dm.n_used, pm, when=when)
                su = cascade_score(du.lr, du.n_used, pu, when=when)
                _append_pair(parts, twin.stem, sample, sm, su)
                opening = "".join(decode_token(tok, t) for t in ids_m[:4]).strip()
                rows.append(
                    {
                        "stem": twin.stem,
                        "sample": sample,
                        "side": "marked",
                        "n_used": dm.n_used,
                        "count_lr": dm.lr,
                        "pivot_lr": pm,
                        "source": cascade_source(
                            dm.n_used, fallback, count_lr=dm.lr, when=when
                        ),
                        "score": sm,
                        "opening_text": opening,
                        "cascade_when": when,
                    }
                )
                rows.append(
                    {
                        "stem": twin.stem,
                        "sample": sample,
                        "side": "unmarked",
                        "n_used": du.n_used,
                        "count_lr": du.lr,
                        "pivot_lr": pu,
                        "source": cascade_source(
                            du.n_used, fallback, count_lr=du.lr, when=when
                        ),
                        "score": su,
                        "opening_text": "",
                        "cascade_when": when,
                    }
                )
        fb = fit if fallback == "pivot" else rank_model
        ev = _holdout_from_parts(
            parts,
            context_len=context_len,
            model_name=model_name,
            instance="key-free-cascade",
            score_kind="cascade",
            used_keys=bool(
                getattr(model, "used_keys", False)
                or (fb.used_keys if fb is not None else False)
            ),
            used_hash_iv=bool(
                getattr(model, "used_hash_iv", False)
                or (fb.used_hash_iv if fb is not None else False)
            ),
            used_g_values=bool(
                getattr(model, "used_g_values", False)
                or (fb.used_g_values if fb is not None else False)
            ),
            mode=mode,
        )
        return ev, rows

    train_ev, _ = _score_side(train, train_vecs, "train")
    test_ev, rows = _score_side(test, test_vecs, "transfer")
    return test_ev, train_ev, rows


def _cascade_fallback_lr(
    fallback: str,
    *,
    stem: str,
    sample: int,
    side: str,
    vecs,
    pivot_fit,
    symbols,
    rank_model,
    rank_spec,
) -> float:
    from text_watermark_tools.pivot import score_pivot_lda
    from text_watermark_tools.rankpath import score_rankpath

    if fallback == "pivot":
        return score_pivot_lda(vecs[(stem, sample, side)], pivot_fit)
    ids = symbols.get((stem, sample, side), [])
    return score_rankpath(ids, rank_model, spec=rank_spec)


def _choice_matrix_views(
    clipped,
    raw,
    lm,
    *,
    fit_prefix: int | None,
    prompt_context: bool,
    rankpath_full: bool,
    want_spans: bool,
    cascade_end: int | None = None,
    model_name: str = "gpt2",
):
    """Collect unmarked-LM ranks once. Opening view matches --fit-prefix.

    Cascade rank-path fallback never uses the full file. ``cascade_end``
    may collect a few extra opening rows (prefix-N) without 128-token
    forwards.
    """
    from text_watermark_tools.blind import clip_twins_prefix
    from text_watermark_tools.pivot import collect_choice_matrices
    from text_watermark_tools.rankpath import (
        generated_tokens_for_rank_symbols,
        opening_matrix_end,
        slice_matrices,
    )

    open_end = opening_matrix_end(fit_prefix, prompt_context)
    cas_end = int(cascade_end) if cascade_end and int(cascade_end) > 0 else None
    if rankpath_full or want_spans:
        source = raw
    else:
        need_rows = max(open_end or 0, cas_end or 0)
        if need_rows <= 0:
            source = clipped
        else:
            need_tokens = generated_tokens_for_rank_symbols(
                need_rows, prompt_context
            )
            if fit_prefix and int(fit_prefix) >= need_tokens:
                source = clipped
            else:
                source = clip_twins_prefix(
                    raw, need_tokens, model_name=model_name
                )
    full = collect_choice_matrices(source, lm, prompt_context=prompt_context)
    if open_end is None:
        opening = full
    else:
        opening = slice_matrices(full, 0, open_end)
    main = full if rankpath_full else opening
    return full, opening, main


