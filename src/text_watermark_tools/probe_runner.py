"""Runners for probe and transfer experiments."""

from __future__ import annotations

import inspect
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
from text_watermark_tools.probe_reporting import (
    _append_threshold,
    _cascade_json,
    _ranking_without_tp_md,
    _store_prefixes,
    _store_windows,
    format_cascade,
    nested_stem_gates,
    persist_coverage,
    persist_probe,
    persist_transfer,
    print_coverage,
    print_probe,
    print_transfer,
    summarize_holdout,
)
from text_watermark_tools.probe_eval import (
    _aligned_rows,
    _cascade_fallback_lr,
    _choice_matrix_views,
    _cov_finalize,
    _cov_observe,
    _empty_cov_bin,
    _hashed_cascade_models,
    _hashed_flag_model,
    _holdouts_as_series,
    _snaprate_holdout_from_twins,
    apply_overlap,
    combine_holdouts_logit,
    hashed_count_detail,
    hashed_count_map,
    rotate_cascade,
    rotate_count_methods,
    rotate_custom,
    rotate_hashmask,
    rotate_hashmask2,
    rotate_hashmix,
    rotate_hashpool,
    rotate_hashskip,
    rotate_hashskip2,
    rotate_hashtok,
    rotate_hashtok2,
    rotate_hashtokbackoff,
    rotate_hashtokbackoff2,
    rotate_hashtokgap,
    rotate_hashtoklen,
    rotate_hashtoklen2,
    rotate_hashtoklenbackoff,
    rotate_hashtoklenbackoff2,
    rotate_hashvote,
    rotate_hits_coverage,
    rotate_hybrid,
    rotate_pivot,
    rotate_pos_methods,
    rotate_poshashtok,
    rotate_poshitmass,
    rotate_poshits,
    rotate_postokbackoff,
    rotate_postokbackoff2,
    rotate_postokhits,
    rotate_rankpath,
    rotate_score_logit,
    rotate_score_stack,
    rotate_snaprate,
    rotate_surface,
    rotate_tokhybrid,
    score_twins,
    shuffle_twin_sides,
    swap_twin_sides,
    transfer_cascade,
    transfer_pivot,
    transfer_rankpath,
    transfer_snaprate,
)
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

TRANSFER_DEFAULTS: tuple[str, ...] = (
    "hard",
    "hits",
    "freqhits",
    "hitmass",
    "hashpool",
    "hashmix",
    "hybrid",
    "stack",
    "surface",
    "logit",
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
    pivot_weights: Sequence[str] = ("uniform",),
    cascade: str = "",
    with_rankpath: bool = False,
    with_snaprate: bool = False,
    cascade_fallback: str = "pivot",
    n_hashes: int = 8,
    n_buckets: int = 256,
    surface_context_len: int = DEFAULT_SURFACE_CONTEXT,
    max_draws: int | None = None,
    prefix_lens: Sequence[int] = (),
    windows: Sequence[str | tuple[int, int]] = (),
    fit_prefix: int | None = None,
    position_bucket: int = DEFAULT_POS_BUCKET,
    with_coverage: bool = False,
    include_first: bool = False,
    prompt_context: bool = False,
    rankpath_full: bool = False,
    rankpath_pos_bucket: int | None = None,
    cascade_rankpath_end: int | None = None,
    cascade_when: str = "coverage",
    lm=None,
) -> ProbeRun:
    requested = (
        list(methods)
        if methods is not None
        else [k for k in COUNT_SPECS if k not in ("first", "tokhits", "tokbackoff", "tokbackoff2")]
    )
    count_names = [m for m in requested if m in COUNT_SPECS]
    extras = {m for m in requested if m not in COUNT_SPECS}
    pos_names = [m for m in requested if m in POS_SPECS]
    from text_watermark_tools.pivot import SNAPRATE_METHODS
    from text_watermark_tools.rankpath import RANKPATH_SPECS, parse_cascade_fallback

    rank_names = [m for m in requested if m in RANKPATH_SPECS]
    fallback = parse_cascade_fallback(cascade_fallback)
    if with_rankpath and not rank_names:
        rank_names = ["rankpath", "rankuni"]
    snap_names = [m for m in requested if m in SNAPRATE_METHODS]
    if with_snaprate and not snap_names:
        snap_names = list(SNAPRATE_METHODS)
    raw_twins = twins
    if fit_prefix and fit_prefix > 0:
        twins = clip_twins_prefix(
            twins, int(fit_prefix), model_name=model_name
        )
    lenses = _parse_prefix_lens(prefix_lens)
    spans = _parse_windows(windows)
    prefix_out: dict[int, dict[str, IndicatorHoldout]] = {}
    window_out: dict[tuple[int, int], dict[str, IndicatorHoldout]] = {}
    pos_bucket = int(position_bucket) if position_bucket and position_bucket > 0 else 0
    rank_full = bool(rankpath_full)
    if rankpath_pos_bucket is None:
        rank_bucket = pos_bucket
    else:
        rank_bucket = int(rankpath_pos_bucket) if rankpath_pos_bucket > 0 else 0
    run = ProbeRun(
        pair_dir=pair_dir,
        model_name=model_name,
        context_len=context_len,
        max_draws=max_draws,
        prefix_lens=lenses,
        windows=spans,
        fit_prefix=int(fit_prefix) if fit_prefix and fit_prefix > 0 else None,
        position_bucket=pos_bucket,
        include_first=bool(include_first),
        prompt_context=bool(prompt_context),
        pivot_weights=tuple(pivot_weights) if with_pivot or cascade or rank_names or snap_names else (),
        rankpath_full=rank_full,
        rankpath_pos_bucket=(
            rank_bucket if rank_names or fallback in RANKPATH_SPECS else None
        ),
        cascade_rankpath_end=(
            int(cascade_rankpath_end)
            if cascade_rankpath_end and int(cascade_rankpath_end) > 0
            else None
        ),
        cascade_when=cascade_when,
    )
    if count_names:
        counted = rotate_count_methods(
            twins,
            methods=count_names,
            context_len=context_len,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
            include_first=include_first,
            prompt_context=prompt_context,
        )
        for name in count_names:
            run.methods.append(summarize_holdout(name, counted[name]))
    want_hash = with_hashpool and (
        methods is None or "hashpool" in requested or "hashvote" in extras
        or "hybrid" in extras or "tokhybrid" in extras or "hashtokgap" in extras
        or "hashtok" in extras or "hashtok2" in extras
        or "hashtoklen" in extras
        or "hashtoklen2" in extras or "hashskip" in extras or "hashskip2" in extras
        or "hashmask" in extras or "hashmask2" in extras
        or "poshashtok" in extras
    )
    if want_hash and (methods is None or "hashpool" in requested):
        hp = rotate_hashpool(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
        )
        run.methods.append(summarize_holdout("hashpool", hp))
    if pos_names:
        counted_pos = rotate_pos_methods(
            twins,
            methods=tuple(pos_names),
            context_len=context_len,
            position_bucket=pos_bucket,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
            include_first=include_first,
            prompt_context=prompt_context,
        )
        for name in pos_names:
            run.methods.append(summarize_holdout(name, counted_pos[name]))
    if "pospool" in extras:
        pp = rotate_hashpool(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
            position_bucket=pos_bucket,
            method_name="pospool",
        )
        run.methods.append(summarize_holdout("pospool", pp))
    if with_hashpool and "poshashtok" in extras:
        pht = rotate_poshashtok(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
            position_bucket=pos_bucket,
        )
        run.methods.append(summarize_holdout("poshashtok", pht))
    if with_hashpool and "hashvote" in extras:
        vote = rotate_hashvote(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hashvote", vote))
    if with_hashpool and "hashtok" in extras:
        ht = rotate_hashtok(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
        )
        run.methods.append(summarize_holdout("hashtok", ht))
    if with_hashpool and "hashtok2" in extras:
        ht2 = rotate_hashtok2(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
        )
        run.methods.append(summarize_holdout("hashtok2", ht2))
    if with_hashpool and "hashtoklen" in extras:
        htl = rotate_hashtoklen(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
        )
        run.methods.append(summarize_holdout("hashtoklen", htl))
    if with_hashpool and "hashskip" in extras:
        hsk = rotate_hashskip(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
        )
        run.methods.append(summarize_holdout("hashskip", hsk))
    if with_hashpool and "hashtoklen2" in extras:
        htl2 = rotate_hashtoklen2(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
        )
        run.methods.append(summarize_holdout("hashtoklen2", htl2))
    if with_hashpool and "hashskip2" in extras:
        hsk2 = rotate_hashskip2(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
        )
        run.methods.append(summarize_holdout("hashskip2", hsk2))
    if with_hashpool and "hashmask" in extras:
        hmk = rotate_hashmask(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
        )
        run.methods.append(summarize_holdout("hashmask", hmk))
    if with_hashpool and "hashmask2" in extras:
        hmk2 = rotate_hashmask2(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=prefix_out if lenses else None,
            windows=spans,
            window_out=window_out if spans else None,
        )
        run.methods.append(summarize_holdout("hashmask2", hmk2))
    if "hybrid" in extras:
        hyb = rotate_hybrid(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hybrid", hyb))
    if "tokhybrid" in extras:
        thyb = rotate_tokhybrid(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("tokhybrid", thyb))
    if "hashtokgap" in extras:
        hgap = rotate_hashtokgap(
            twins,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hashtokgap", hgap))
    if "hashmix" in extras:
        mix = rotate_hashmix(
            twins,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hashmix", mix))
    if "hashtokbackoff" in extras:
        hb = rotate_hashtokbackoff(
            twins,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hashtokbackoff", hb))
    if "hashtokbackoff2" in extras:
        hb2 = rotate_hashtokbackoff2(
            twins,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hashtokbackoff2", hb2))
    if "hashtoklenbackoff" in extras:
        hlb = rotate_hashtoklenbackoff(
            twins,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hashtoklenbackoff", hlb))
    if "hashtoklenbackoff2" in extras:
        hlb2 = rotate_hashtoklenbackoff2(
            twins,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("hashtoklenbackoff2", hlb2))
    if "surface" in extras:
        one: dict[int, IndicatorHoldout] = {}
        one_win: dict[tuple[int, int], IndicatorHoldout] = {}
        surf = rotate_surface(
            twins,
            context_len=surface_context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            model_name=model_name,
            prefix_lens=lenses,
            prefix_out=one if lenses else None,
            windows=spans,
            window_out=one_win if spans else None,
        )
        run.methods.append(summarize_holdout("surface", surf))
        if one:
            _store_prefixes(prefix_out, {n: {"surface": ev} for n, ev in one.items()})
        if one_win:
            _store_windows(
                window_out, {win: {"surface": ev} for win, ev in one_win.items()}
            )
    if with_pivot or cascade or rank_names or snap_names:
        from text_watermark_tools.generate import _load_unmarked_model, generate_device
        from text_watermark_tools.pivot import (
            parse_pivot_weights,
            summarize_cascade,
        )

        if lm is None:
            lm = _load_unmarked_model(generate_device(), model_name=model_name)
        weight_names = parse_pivot_weights(pivot_weights)
        run.pivot_weights = weight_names
        from text_watermark_tools.rankpath import (
            RANKPATH_SPECS as _RANK_SPECS,
            cascade_fallback_matrices,
        )

        cas_end = (
            int(cascade_rankpath_end)
            if cascade_rankpath_end and int(cascade_rankpath_end) > 0
            and fallback in _RANK_SPECS
            else None
        )
        full_mats, opening_mats, rank_mats = _choice_matrix_views(
            twins,
            raw_twins,
            lm,
            fit_prefix=run.fit_prefix,
            prompt_context=prompt_context,
            rankpath_full=rank_full,
            want_spans=bool(rank_names and (lenses or spans)),
            cascade_end=cas_end,
            model_name=model_name,
        )
        if with_pivot:
            pivots = rotate_pivot(
                twins,
                model_name=model_name,
                lm=lm,
                prompt_context=prompt_context,
                weights=weight_names,
                mats=opening_mats,
            )
            for name, ev in pivots.items():
                run.methods.append(summarize_holdout(name, ev))
        if snap_names:
            snapped = rotate_snaprate(
                twins,
                model_name=model_name,
                lm=lm,
                prompt_context=prompt_context,
                methods=snap_names,
                mats=opening_mats,
            )
            for name in snap_names:
                run.methods.append(summarize_holdout(name, snapped[name]))
        if rank_names:
            ranked = rotate_rankpath(
                twins,
                model_name=model_name,
                lm=lm,
                prompt_context=prompt_context,
                position_bucket=rank_bucket,
                context_len=min(int(context_len), 3),
                methods=rank_names,
                mats=rank_mats,
                span_mats=full_mats if (lenses or spans) else None,
                prefix_lens=lenses,
                prefix_out=prefix_out if lenses else None,
                windows=spans,
                window_out=window_out if spans else None,
            )
            for name, ev in ranked.items():
                run.methods.append(summarize_holdout(name, ev))
        cascade_name = str(cascade or "").strip()
        if cascade_name:
            hashed = cascade_name if cascade_name in HASH_CASCADE_READERS else ""
            spec = None if hashed else (
                POS_SPECS.get(cascade_name) or COUNT_SPECS.get(cascade_name)
            )
            if spec is None and not hashed:
                raise ValueError(
                    f"unknown --cascade {cascade_name}; choose postokbackoff, "
                    f"postokhits, a count spec, or occupancy-free "
                    + ", ".join(HASH_CASCADE_READERS)
                )
            cascade_mats = (
                cascade_fallback_matrices(
                    opening_mats, full_mats, end=cas_end
                )
                if fallback in _RANK_SPECS
                else opening_mats
            )
            ev, rows = rotate_cascade(
                twins,
                spec=spec,
                position_bucket=pos_bucket if cascade_name in POS_SPECS else 0,
                context_len=context_len,
                include_first=include_first,
                model_name=model_name,
                lm=lm,
                prompt_context=prompt_context,
                pivot_weight=weight_names[0],
                count_prompt_context=False,
                fallback=fallback,
                mats=cascade_mats,
                rankpath_pos_bucket=rank_bucket if fallback in _RANK_SPECS else None,
                cascade_when=cascade_when,
                hashed_reader=hashed,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
            )
            run.methods.append(summarize_holdout("cascade", ev))
            run.cascade = summarize_cascade(rows, when=cascade_when)
            run.cascade["count_method"] = cascade_name
            run.cascade["pivot_weight"] = weight_names[0]
            run.cascade["fallback"] = fallback
            run.cascade["prompt_context"] = bool(prompt_context)
            run.cascade["rankpath_end"] = cas_end
            run.cascade["rows"] = rows
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
    logit_feats = [by_name[n] for n in LOGIT_FEATURE_ORDER if n in by_name]
    want_logit = len(logit_feats) >= 2 and (methods is None or "logit" in extras)
    if want_logit:
        logit = rotate_score_logit(logit_feats, model_name=model_name)
        run.methods.append(summarize_holdout("logit", logit))
    run.used_keys = any(m.holdout.used_keys for m in run.methods)
    run.used_hash_iv = any(m.holdout.used_hash_iv for m in run.methods)
    run.used_g_values = any(m.holdout.used_g_values for m in run.methods)
    _store_prefixes(run.prefixes, prefix_out)
    _store_windows(run.window_results, window_out)
    if with_coverage:
        if len(raw_twins) < 3:
            raise ValueError("coverage rotate needs at least three prompts")
        run.coverage = rotate_hits_coverage(
            raw_twins,
            context_len=context_len,
            position_bucket=0,
            windows=spans or DEFAULT_COVERAGE_WINDOWS,
        )
    return run


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
    nested: bool = True,
    shuffle_labels: bool = False,
    shuffle_seed: int = 0,
    surface_context_len: int = DEFAULT_SURFACE_CONTEXT,
    prefix_lens: Sequence[int] = (),
    windows: Sequence[str | tuple[int, int]] = (),
    fit_prefix: int | None = None,
    position_bucket: int = DEFAULT_POS_BUCKET,
    include_first: bool = False,
    prompt_context: bool = False,
    with_pivot: bool = False,
    pivot_weights: Sequence[str] = ("uniform",),
    cascade: str = "",
    with_rankpath: bool = False,
    with_snaprate: bool = False,
    cascade_fallback: str = "pivot",
    rankpath_full: bool = False,
    rankpath_pos_bucket: int | None = None,
    cascade_rankpath_end: int | None = None,
    cascade_when: str = "coverage",
    lm=None,
    hash_seed: int = 20260831,
) -> TransferRun:
    """Fit on train twins, score every test file. No test prompt enters the fit."""
    train, test, overlap = apply_overlap(
        train_twins, test_twins, mode=overlap_mode
    )
    if shuffle_labels:
        train = shuffle_twin_sides(train, seed=shuffle_seed)
    raw_train, raw_test = train, test
    if fit_prefix and fit_prefix > 0:
        train = clip_twins_prefix(
            train, int(fit_prefix), model_name=model_name
        )
        test = clip_twins_prefix(
            test, int(fit_prefix), model_name=model_name
        )
    if len(train) < 1:
        raise ValueError("transfer left no training prompts")
    if len(test) < 1:
        raise ValueError("transfer left no test prompts")
    names = list(methods or TRANSFER_DEFAULTS)
    count_names = [n for n in names if n in COUNT_SPECS]
    extras = [n for n in names if n not in COUNT_SPECS]
    from text_watermark_tools.pivot import SNAPRATE_METHODS
    from text_watermark_tools.rankpath import RANKPATH_SPECS, parse_cascade_fallback

    rank_names = [n for n in names if n in RANKPATH_SPECS]
    fallback = parse_cascade_fallback(cascade_fallback)
    if with_rankpath and not rank_names:
        rank_names = ["rankpath", "rankuni"]
    snap_names = [n for n in names if n in SNAPRATE_METHODS]
    if with_snaprate and not snap_names:
        snap_names = list(SNAPRATE_METHODS)
    if "logit" in extras:
        logit_ready = [n for n in LOGIT_FEATURE_ORDER if n in names]
        if len(logit_ready) < 2:
            raise ValueError(
                "logit needs at least two of hits, poshits, hashpool, "
                "surface, hitmass, poshitmass, first"
            )
    need_counts = bool(count_names) or any(
        n in extras for n in ("hybrid", "tokhybrid", "hashtokgap", "stack")
    )
    need_hash = any(
        n in extras
        for n in (
            "hashpool",
            "hashvote",
            "hybrid",
            "tokhybrid",
            "hashtokgap",
            "stack",
            "hashmix",
            "hashtok",
            "hashtok2",
            "hashtoklen",
            "hashtoklen2",
            "hashskip",
            "hashskip2",
            "hashmask",
            "hashmask2",
            "hashtokbackoff",
            "hashtokbackoff2",
            "hashtoklenbackoff",
            "hashtoklenbackoff2",
            "poshashtok",
        )
    )
    need_surface = "surface" in extras
    store_first = include_first or "first" in count_names
    count_model = (
        fit_count_model(
            train,
            context_len=context_len,
            include_first=store_first,
            prompt_context=prompt_context,
        )
        if need_counts
        else None
    )
    if count_model is not None:
        count_model.include_first = bool(include_first)
    hash_model = (
        fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            seed=hash_seed,
        )
        if need_hash and any(
            n in extras
            for n in (
                "hashpool",
                "hashvote",
                "hybrid",
                "tokhybrid",
                "hashtokgap",
                "stack",
                "hashtok",
                "hashtok2",
            )
        )
        else None
    )
    hash_len_model = (
        fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            exact_len=True,
        )
        if need_hash and any(n in extras for n in ("hashtoklen", "hashtoklen2"))
        else None
    )
    hash_skip_model = (
        fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            exact_len=True,
            drop_one=True,
        )
        if need_hash and any(n in extras for n in ("hashskip", "hashskip2"))
        else None
    )
    hash_mask_model = (
        fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            exact_len=True,
            mask_one=True,
        )
        if need_hash and any(n in extras for n in ("hashmask", "hashmask2"))
        else None
    )
    mix_model = (
        fit_hashmix_twins(
            train,
            orders=(
                HASHBACKOFF_ORDERS
                if any(
                    n in extras for n in ("hashtokbackoff", "hashtokbackoff2")
                )
                else (1, 2, 4)
            ),
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
        if any(
            n in extras for n in ("hashmix", "hashtokbackoff", "hashtokbackoff2")
        )
        else None
    )
    mix_len_model = (
        fit_hashmix_twins(
            train,
            orders=HASHBACKOFF_ORDERS,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            exact_len=True,
        )
        if any(
            n in extras for n in ("hashtoklenbackoff", "hashtoklenbackoff2")
        )
        else None
    )
    surface_model = (
        fit_surface_twins(
            train,
            context_len=surface_context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
        )
        if need_surface
        else None
    )
    pos_bucket = (
        int(position_bucket) if position_bucket and position_bucket > 0 else 0
    )
    rank_full = bool(rankpath_full)
    if rankpath_pos_bucket is None:
        rank_bucket = pos_bucket
    else:
        rank_bucket = int(rankpath_pos_bucket) if rankpath_pos_bucket > 0 else 0
    pos_names = [n for n in extras if n in POS_SPECS]
    pos_model = (
        fit_count_model(
            train,
            context_len=context_len,
            position_bucket=pos_bucket,
            include_first=store_first,
            prompt_context=prompt_context,
        )
        if pos_names
        else None
    )
    if pos_model is not None:
        pos_model.include_first = bool(include_first)
    pos_hash = (
        fit_hashpool_twins(
            train,
            context_len=context_len,
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            position_bucket=pos_bucket,
        )
        if "pospool" in extras or "poshashtok" in extras
        else None
    )
    used_keys = False
    used_hash = False
    used_g = False
    for model in (
        count_model,
        hash_model,
        hash_len_model,
        hash_skip_model,
        hash_mask_model,
        mix_model,
        mix_len_model,
        surface_model,
        pos_model,
        pos_hash,
    ):
        if model is None:
            continue
        used_keys = used_keys or model.used_keys
        used_hash = used_hash or model.used_hash_iv
        used_g = used_g or model.used_g_values

    scorers: dict[str, tuple[ScoreFn, str, str, str]] = {}
    for name in count_names:
        spec = COUNT_SPECS[name]
        assert count_model is not None
        scorers[name] = (
            _bound_ids_scorer(score_sequence, count_model, spec),
            spec.instance,
            name,
            "ids",
        )
    if "hashpool" in extras:
        assert hash_model is not None
        scorers["hashpool"] = (
            _bound_ids_scorer(score_hashpool, hash_model),
            "key-free-hashpool",
            "hashpool",
            "ids",
        )
    if "hashvote" in extras:
        assert hash_model is not None
        scorers["hashvote"] = (
            _bound_ids_scorer(score_hashpool_vote, hash_model),
            "key-free-hashvote",
            "hashvote",
            "ids",
        )
    if "hashtok" in extras:
        assert hash_model is not None
        scorers["hashtok"] = (
            _bound_ids_scorer(score_hashtok, hash_model),
            "key-free-hashtok",
            "hashtok",
            "ids",
        )
    if "hashtok2" in extras:
        assert hash_model is not None
        scorers["hashtok2"] = (
            _bound_ids_scorer(score_hashtok, hash_model, min_count=2),
            "key-free-hashtok2",
            "hashtok2",
            "ids",
        )
    if "hashtoklen" in extras:
        assert hash_len_model is not None
        scorers["hashtoklen"] = (
            _bound_ids_scorer(score_hashtok, hash_len_model),
            "key-free-hashtoklen",
            "hashtoklen",
            "ids",
        )
    if "hashtoklen2" in extras:
        assert hash_len_model is not None
        scorers["hashtoklen2"] = (
            _bound_ids_scorer(score_hashtok, hash_len_model, min_count=2),
            "key-free-hashtoklen2",
            "hashtoklen2",
            "ids",
        )
    if "hashskip" in extras:
        assert hash_skip_model is not None
        scorers["hashskip"] = (
            _bound_ids_scorer(score_hashskip, hash_skip_model),
            "key-free-hashskip",
            "hashskip",
            "ids",
        )
    if "hashskip2" in extras:
        assert hash_skip_model is not None
        scorers["hashskip2"] = (
            _bound_ids_scorer(score_hashskip, hash_skip_model, min_count=2),
            "key-free-hashskip2",
            "hashskip2",
            "ids",
        )
    if "hashmask" in extras:
        assert hash_mask_model is not None
        scorers["hashmask"] = (
            _bound_ids_scorer(score_hashmask, hash_mask_model),
            "key-free-hashmask",
            "hashmask",
            "ids",
        )
    if "hashmask2" in extras:
        assert hash_mask_model is not None
        scorers["hashmask2"] = (
            _bound_ids_scorer(score_hashmask, hash_mask_model, min_count=2),
            "key-free-hashmask2",
            "hashmask2",
            "ids",
        )
    if "hybrid" in extras:
        assert count_model is not None and hash_model is not None
        scorers["hybrid"] = (
            _bound_ids_scorer(score_hybrid, count_model, hash_model),
            "key-free-hybrid",
            "hybrid",
            "ids",
        )
    if "tokhybrid" in extras:
        assert count_model is not None and hash_model is not None
        scorers["tokhybrid"] = (
            _bound_ids_scorer(score_tokhybrid, count_model, hash_model),
            "key-free-tokhybrid",
            "tokhybrid",
            "ids",
        )
    if "hashtokgap" in extras:
        assert count_model is not None and hash_model is not None
        scorers["hashtokgap"] = (
            _bound_ids_scorer(score_hashtokgap, count_model, hash_model),
            "key-free-hashtokgap",
            "hashtokgap",
            "ids",
        )
    if "hashmix" in extras:
        assert mix_model is not None
        scorers["hashmix"] = (
            _bound_ids_scorer(score_hashmix, mix_model),
            "key-free-hashmix",
            "hashmix",
            "ids",
        )
    if "hashtokbackoff" in extras:
        assert mix_model is not None
        scorers["hashtokbackoff"] = (
            _bound_ids_scorer(score_hashtokbackoff, mix_model, min_order=1),
            "key-free-hashtokbackoff",
            "hashtokbackoff",
            "ids",
        )
    if "hashtokbackoff2" in extras:
        assert mix_model is not None
        scorers["hashtokbackoff2"] = (
            _bound_ids_scorer(score_hashtokbackoff, mix_model, min_order=2),
            "key-free-hashtokbackoff2",
            "hashtokbackoff2",
            "ids",
        )
    if "hashtoklenbackoff" in extras:
        assert mix_len_model is not None
        scorers["hashtoklenbackoff"] = (
            _bound_ids_scorer(score_hashtokbackoff, mix_len_model, min_order=1),
            "key-free-hashtoklenbackoff",
            "hashtoklenbackoff",
            "ids",
        )
    if "hashtoklenbackoff2" in extras:
        assert mix_len_model is not None
        scorers["hashtoklenbackoff2"] = (
            _bound_ids_scorer(score_hashtokbackoff, mix_len_model, min_order=2),
            "key-free-hashtoklenbackoff2",
            "hashtoklenbackoff2",
            "ids",
        )
    if "surface" in extras:
        assert surface_model is not None
        scorers["surface"] = (
            (lambda text, m=surface_model: score_surface(text, m)),
            "key-free-surface",
            "surface",
            "text",
        )

    for name in pos_names:
        if name == "pospool":
            continue
        spec = POS_SPECS[name]
        assert pos_model is not None
        scorers[name] = (
            _bound_ids_scorer(score_sequence, pos_model, spec),
            spec.instance,
            name,
            "ids",
        )
    if "pospool" in extras:
        assert pos_hash is not None
        scorers["pospool"] = (
            _bound_ids_scorer(score_hashpool, pos_hash),
            "key-free-pospool",
            "pospool",
            "ids",
        )
    if "poshashtok" in extras:
        assert pos_hash is not None
        scorers["poshashtok"] = (
            _bound_ids_scorer(score_hashtok, pos_hash),
            "key-free-poshashtok",
            "poshashtok",
            "ids",
        )

    note = (
        "Train on one twin directory, score the other. Shared prompt stems "
        "are dropped as overlap_mode says. In-sample Youden is optimistic. "
        "nested-youden / nested-fpr10 come from leave-one-prompt-out on "
        "training stems only, then frozen on the test files. "
        "ranking_without_isolated_tp counts prompt wins with no marked "
        "file lr>0; do not read prompt wins as isolated recall. "
        "Not detector_mean. Not Claude. Not key recovery."
    )
    if shuffle_labels:
        note = (
            "NEGATIVE CONTROL: training marked/unmarked labels were shuffled "
            "per stem. Test labels are real. AUC should collapse toward 0.5. "
        ) + note

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
        count_model=count_model,
        hash_model=hash_model,
        hash_len_model=hash_len_model,
        hash_skip_model=hash_skip_model,
        hash_mask_model=hash_mask_model,
        surface_model=surface_model,
        pos_model=pos_model,
        pos_hash=pos_hash,
        nested=bool(nested and len(train) >= 3),
        shuffle_seed=shuffle_seed if shuffle_labels else None,
        surface_context_len=surface_context_len,
        prefix_lens=_parse_prefix_lens(prefix_lens),
        windows=_parse_windows(windows),
        fit_prefix=int(fit_prefix) if fit_prefix and fit_prefix > 0 else None,
        position_bucket=pos_bucket,
        include_first=bool(include_first),
        prompt_context=bool(prompt_context),
        rankpath_full=rank_full,
        rankpath_pos_bucket=(
            rank_bucket if rank_names or fallback in RANKPATH_SPECS else None
        ),
        cascade_rankpath_end=(
            int(cascade_rankpath_end)
            if cascade_rankpath_end and int(cascade_rankpath_end) > 0
            else None
        ),
        cascade_when=cascade_when,
        note=note,
    )
    train_holdouts: dict[str, IndicatorHoldout] = {}
    test_holdouts: dict[str, IndicatorHoldout] = {}
    for name, (scorer, instance, kind, seq_mode) in scorers.items():
        train_ev = score_twins(
            train,
            scorer,
            context_len=context_len if seq_mode == "ids" else surface_context_len,
            model_name=model_name,
            instance=instance,
            score_kind=kind,
            used_keys=used_keys,
            used_hash_iv=used_hash,
            used_g_values=used_g,
            mode="train",
            seq_mode=seq_mode,
            prompt_context=prompt_context,
        )
        pref: dict[int, IndicatorHoldout] = {}
        win: dict[tuple[int, int], IndicatorHoldout] = {}
        test_ev = score_twins(
            test,
            scorer,
            context_len=context_len if seq_mode == "ids" else surface_context_len,
            model_name=model_name,
            instance=instance,
            score_kind=kind,
            used_keys=used_keys,
            used_hash_iv=used_hash,
            used_g_values=used_g,
            mode="transfer",
            seq_mode=seq_mode,
            prefix_lens=run.prefix_lens,
            prefix_out=pref if run.prefix_lens else None,
            windows=run.windows,
            window_out=win if run.windows else None,
            prompt_context=prompt_context,
        )
        if pref:
            _store_prefixes(run.prefixes, {n: {name: ev} for n, ev in pref.items()})
        if win:
            _store_windows(
                run.window_results, {span: {name: ev} for span, ev in win.items()}
            )
        train_holdouts[name] = train_ev
        test_holdouts[name] = test_ev
        run.methods.append(summarize_holdout(name, test_ev))
        train_bin = binary_eval(train_ev.marked_lrs, train_ev.unmarked_lrs)
        _append_threshold(
            run,
            name=name,
            source="in-sample-youden",
            threshold=train_bin.youden_threshold,
            test_ev=test_ev,
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
        _append_threshold(
            run,
            name="stack",
            source="in-sample-youden",
            threshold=train_bin.youden_threshold,
            test_ev=stack_ev,
        )
        test_holdouts["stack"] = stack_ev

    logit_names = [n for n in LOGIT_FEATURE_ORDER if n in test_holdouts]
    if "logit" in extras and len(logit_names) >= 2:
        train_logit, test_logit = combine_holdouts_logit(
            [train_holdouts[n] for n in logit_names],
            [test_holdouts[n] for n in logit_names],
            model_name=model_name,
        )
        run.methods.append(summarize_holdout("logit", test_logit))
        train_bin = binary_eval(train_logit.marked_lrs, train_logit.unmarked_lrs)
        _append_threshold(
            run,
            name="logit",
            source="in-sample-youden",
            threshold=train_bin.youden_threshold,
            test_ev=test_logit,
        )
        test_holdouts["logit"] = test_logit
        train_holdouts["logit"] = train_logit

    if with_pivot or cascade or rank_names or snap_names:
        from text_watermark_tools.generate import _load_unmarked_model, generate_device
        from text_watermark_tools.pivot import (
            parse_pivot_weights,
            summarize_cascade,
        )

        if lm is None:
            lm = _load_unmarked_model(generate_device(), model_name=model_name)
        weight_names = parse_pivot_weights(pivot_weights)
        run.pivot_weights = weight_names
        run.cascade_fallback = fallback
        from text_watermark_tools.rankpath import (
            RANKPATH_SPECS as _RANK_SPECS,
            cascade_fallback_matrices,
        )

        cas_end = (
            int(cascade_rankpath_end)
            if cascade_rankpath_end and int(cascade_rankpath_end) > 0
            and fallback in _RANK_SPECS
            else None
        )
        want_spans = bool(rank_names and (run.prefix_lens or run.windows))
        train_full, train_opening, train_rank_mats = _choice_matrix_views(
            train,
            raw_train,
            lm,
            fit_prefix=run.fit_prefix,
            prompt_context=prompt_context,
            rankpath_full=rank_full,
            want_spans=want_spans,
            cascade_end=cas_end,
            model_name=model_name,
        )
        test_full, test_opening, test_rank_mats = _choice_matrix_views(
            test,
            raw_test,
            lm,
            fit_prefix=run.fit_prefix,
            prompt_context=prompt_context,
            rankpath_full=rank_full,
            want_spans=want_spans,
            cascade_end=cas_end,
            model_name=model_name,
        )
        train_mats = train_rank_mats
        test_mats = test_rank_mats
        if with_pivot:
            test_pivots, train_pivots, fits = transfer_pivot(
                train,
                test,
                model_name=model_name,
                lm=lm,
                prompt_context=prompt_context,
                weights=weight_names,
                train_mats=train_opening,
                test_mats=test_opening,
            )
            run.pivot_fits = fits
            run.pivot_fit = fits.get("uniform") or next(iter(fits.values()), None)
            used_keys = used_keys or any(ev.used_keys for ev in test_pivots.values())
            used_hash = used_hash or any(
                ev.used_hash_iv for ev in test_pivots.values()
            )
            used_g = used_g or any(ev.used_g_values for ev in test_pivots.values())
            for name, ev in test_pivots.items():
                run.methods.append(summarize_holdout(name, ev))
                train_bin = binary_eval(
                    train_pivots[name].marked_lrs, train_pivots[name].unmarked_lrs
                )
                _append_threshold(
                    run,
                    name=name,
                    source="in-sample-youden",
                    threshold=train_bin.youden_threshold,
                    test_ev=ev,
                )
                test_holdouts[name] = ev
                train_holdouts[name] = train_pivots[name]
        if snap_names:
            test_snaps, train_snaps = transfer_snaprate(
                train,
                test,
                model_name=model_name,
                lm=lm,
                prompt_context=prompt_context,
                methods=snap_names,
                train_mats=train_opening,
                test_mats=test_opening,
            )
            used_keys = used_keys or any(ev.used_keys for ev in test_snaps.values())
            used_hash = used_hash or any(
                ev.used_hash_iv for ev in test_snaps.values()
            )
            used_g = used_g or any(ev.used_g_values for ev in test_snaps.values())
            for name in snap_names:
                ev = test_snaps[name]
                run.methods.append(summarize_holdout(name, ev))
                train_bin = binary_eval(
                    train_snaps[name].marked_lrs, train_snaps[name].unmarked_lrs
                )
                _append_threshold(
                    run,
                    name=name,
                    source="in-sample-youden",
                    threshold=train_bin.youden_threshold,
                    test_ev=ev,
                )
                test_holdouts[name] = ev
                train_holdouts[name] = train_snaps[name]
        rank_model = None
        if rank_names:
            rank_pref: dict[int, dict[str, IndicatorHoldout]] = {}
            rank_win: dict[tuple[int, int], dict[str, IndicatorHoldout]] = {}
            test_rank, train_rank, rank_model, _syms = transfer_rankpath(
                train,
                test,
                model_name=model_name,
                lm=lm,
                prompt_context=prompt_context,
                position_bucket=rank_bucket,
                context_len=min(int(context_len), 3),
                methods=rank_names,
                train_mats=train_rank_mats,
                test_mats=test_rank_mats,
                span_train_mats=train_full if want_spans else None,
                span_test_mats=test_full if want_spans else None,
                prefix_lens=run.prefix_lens,
                prefix_out=rank_pref if run.prefix_lens else None,
                windows=run.windows,
                window_out=rank_win if run.windows else None,
            )
            run.rankpath_model = rank_model
            if rank_pref:
                _store_prefixes(run.prefixes, rank_pref)
            if rank_win:
                _store_windows(run.window_results, rank_win)
            used_keys = used_keys or rank_model.used_keys
            used_hash = used_hash or rank_model.used_hash_iv
            used_g = used_g or rank_model.used_g_values
            for name, ev in test_rank.items():
                run.methods.append(summarize_holdout(name, ev))
                train_bin = binary_eval(
                    train_rank[name].marked_lrs, train_rank[name].unmarked_lrs
                )
                _append_threshold(
                    run,
                    name=name,
                    source="in-sample-youden",
                    threshold=train_bin.youden_threshold,
                    test_ev=ev,
                )
                test_holdouts[name] = ev
                train_holdouts[name] = train_rank[name]
        cascade_name = str(cascade or "").strip()
        if cascade_name:
            hashed = cascade_name if cascade_name in HASH_CASCADE_READERS else ""
            spec = None if hashed else (
                POS_SPECS.get(cascade_name) or COUNT_SPECS.get(cascade_name)
            )
            if spec is None and not hashed:
                raise ValueError(
                    f"unknown --cascade {cascade_name}; choose postokbackoff, "
                    f"postokhits, a count spec, or occupancy-free "
                    + ", ".join(HASH_CASCADE_READERS)
                )
            cascade_pos = None if hashed else (
                pos_model if cascade_name in POS_SPECS else None
            )
            if fallback in _RANK_SPECS:
                cas_train = cascade_fallback_matrices(
                    train_opening, train_full, end=cas_end
                )
                cas_test = cascade_fallback_matrices(
                    test_opening, test_full, end=cas_end
                )
            else:
                cas_train, cas_test = train_opening, test_opening
            reuse_rank = (
                fallback in RANKPATH_SPECS
                and rank_model is not None
                and not rank_full
                and cas_end is None
            )
            hashed_models = None
            count_detail = None
            flag_model = None
            if hashed:
                hashed_models = _hashed_cascade_models(
                    train,
                    hashed,
                    context_len=context_len,
                    n_hashes=n_hashes,
                    n_buckets=n_buckets,
                )
                count_detail = hashed_count_detail(hashed, hashed_models)
                flag_model = _hashed_flag_model(hashed_models)
            test_cas, train_cas, rows = transfer_cascade(
                train,
                test,
                spec=spec,
                position_bucket=pos_bucket if cascade_name in POS_SPECS else 0,
                context_len=context_len,
                include_first=include_first,
                model_name=model_name,
                lm=lm,
                prompt_context=prompt_context,
                pivot_weight=weight_names[0],
                count_prompt_context=False,
                pos_model=cascade_pos,
                fallback=fallback,
                train_mats=cas_train,
                test_mats=cas_test,
                rank_model=rank_model if reuse_rank else None,
                rankpath_pos_bucket=rank_bucket if fallback in _RANK_SPECS else None,
                cascade_when=cascade_when,
                hashed_reader="" if count_detail is not None else hashed,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                count_detail=count_detail,
                flag_model=flag_model,
            )
            run.methods.append(summarize_holdout("cascade", test_cas))
            train_bin = binary_eval(train_cas.marked_lrs, train_cas.unmarked_lrs)
            _append_threshold(
                run,
                name="cascade",
                source="in-sample-youden",
                threshold=train_bin.youden_threshold,
                test_ev=test_cas,
            )
            test_holdouts["cascade"] = test_cas
            train_holdouts["cascade"] = train_cas
            run.cascade = summarize_cascade(rows, when=cascade_when)
            run.cascade["count_method"] = cascade_name
            run.cascade["pivot_weight"] = weight_names[0]
            run.cascade["fallback"] = fallback
            run.cascade["prompt_context"] = bool(prompt_context)
            run.cascade["rankpath_end"] = cas_end
            run.cascade["rows"] = rows
            used_keys = used_keys or test_cas.used_keys
            used_hash = used_hash or test_cas.used_hash_iv
            used_g = used_g or test_cas.used_g_values
        run.used_keys = used_keys
        run.used_hash_iv = used_hash
        run.used_g_values = used_g

    if run.nested:
        nested_holdouts: dict[str, IndicatorHoldout] = {}
        if count_names:
            loo_counts = rotate_count_methods(
                train,
                methods=count_names,
                context_len=context_len,
                model_name=model_name,
                include_first=include_first,
                prompt_context=prompt_context,
            )
            nested_holdouts.update(loo_counts)
        if "hashpool" in extras:
            nested_holdouts["hashpool"] = rotate_hashpool(
                train,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashtok" in extras:
            nested_holdouts["hashtok"] = rotate_hashtok(
                train,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
                seed=hash_seed,
            )
        if "hashtok2" in extras:
            nested_holdouts["hashtok2"] = rotate_hashtok2(
                train,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashtoklen" in extras:
            nested_holdouts["hashtoklen"] = rotate_hashtoklen(
                train,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashtoklen2" in extras:
            nested_holdouts["hashtoklen2"] = rotate_hashtoklen2(
                train,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashskip" in extras:
            nested_holdouts["hashskip"] = rotate_hashskip(
                train,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashskip2" in extras:
            nested_holdouts["hashskip2"] = rotate_hashskip2(
                train,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashmask" in extras:
            nested_holdouts["hashmask"] = rotate_hashmask(
                train,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashmask2" in extras:
            nested_holdouts["hashmask2"] = rotate_hashmask2(
                train,
                context_len=context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashtokbackoff" in extras:
            nested_holdouts["hashtokbackoff"] = rotate_hashtokbackoff(
                train,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashtokbackoff2" in extras:
            nested_holdouts["hashtokbackoff2"] = rotate_hashtokbackoff2(
                train,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashtoklenbackoff" in extras:
            nested_holdouts["hashtoklenbackoff"] = rotate_hashtoklenbackoff(
                train,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "hashtoklenbackoff2" in extras:
            nested_holdouts["hashtoklenbackoff2"] = rotate_hashtoklenbackoff2(
                train,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if "surface" in extras:
            nested_holdouts["surface"] = rotate_surface(
                train,
                context_len=surface_context_len,
                n_hashes=n_hashes,
                n_buckets=n_buckets,
                model_name=model_name,
            )
        if pos_names:
            nested_holdouts.update(
                rotate_pos_methods(
                    train,
                    methods=tuple(pos_names),
                    context_len=context_len,
                    position_bucket=pos_bucket,
                    model_name=model_name,
                    include_first=include_first,
                    prompt_context=prompt_context,
                )
            )
        if rank_names:
            nested_holdouts.update(
                rotate_rankpath(
                    train,
                    model_name=model_name,
                    prompt_context=prompt_context,
                    position_bucket=rank_bucket,
                    context_len=min(int(context_len), 3),
                    methods=rank_names,
                    mats=train_mats,
                )
            )
        if snap_names:
            nested_holdouts.update(
                {n: train_holdouts[n] for n in snap_names if n in train_holdouts}
            )
        if (
            "stack" in extras
            and "hits" in nested_holdouts
            and "hashpool" in nested_holdouts
        ):
            nested_holdouts["stack"] = rotate_score_stack(
                [nested_holdouts["hits"], nested_holdouts["hashpool"]],
                model_name=model_name,
            )
        nested_logit_names = [n for n in LOGIT_FEATURE_ORDER if n in nested_holdouts]
        if "logit" in extras and len(nested_logit_names) >= 2:
            nested_holdouts["logit"] = rotate_score_logit(
                [nested_holdouts[n] for n in nested_logit_names],
                model_name=model_name,
            )
        for name, loo_ev in nested_holdouts.items():
            test_ev = test_holdouts.get(name)
            if test_ev is None:
                continue
            loo_bin = binary_eval(loo_ev.marked_lrs, loo_ev.unmarked_lrs)
            _append_threshold(
                run,
                name=name,
                source="nested-youden",
                threshold=loo_bin.youden_threshold,
                test_ev=test_ev,
            )
            _append_threshold(
                run,
                name=name,
                source="nested-fpr10",
                threshold=threshold_at_fpr(loo_ev.unmarked_lrs, fpr=0.10),
                test_ev=test_ev,
            )
    return run

