"""Compare key-free scorers on matched twins, plus an argmax-snap scrub.

`probe` is a laboratory comparison, not a production detector. Every method
sets used_keys / used_hash_iv / used_g_values to false. The official
`score` path is used only afterwards, as a reference check that a scrub
moved a known public mark toward chance.

This module is broken up into modular subcomponents:
- `probe_models`: data models, specs, and slicing/window helpers
- `probe_scrub`: argmax snap scrub algorithms and file scrubbing
- `probe_reporting`: coverage printing, cascade formatting, persist/print logic
- `probe_eval`: rotation, transfer evaluations, and choice matrix logic
- `probe_runner`: top-level orchestrators (`run_probe`, `run_transfer`)

All public APIs, functions, classes, and constants are re-exported here for
complete backward compatibility.
"""

from __future__ import annotations

# Re-export common dependencies that were previously imported in probe.py
from text_watermark_tools.blind import Twin, _scored_ctx, clip_twins_prefix
from text_watermark_tools.indicator import (
    CAVEAT,
    IndicatorHoldout,
    persist_holdout,
    persist_indicator,
)
from text_watermark_tools.stats import (
    binary_eval,
    binary_eval_to_dict,
    coverage_gate,
    coverage_gate_to_dict,
    counts_at_threshold,
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
    HASHBACKOFF_ORDERS,
    HASH_CASCADE_READERS,
    ScoreSpec,
    fit_count_model,
    fit_hashmix_twins,
    fit_hashpool_twins,
    fit_surface_twins,
    _count,
    persist_hashpool,
    score_hashed_reader_detail,
    score_hashmix,
    score_hashtok,
    score_hashskip,
    score_hashmask,
    score_hashtokbackoff,
    score_hashpool,
    score_hashpool_vote,
    score_hybrid,
    score_tokhybrid,
    score_hashtokgap,
    score_sequence,
    score_surface,
)

# Re-export probe_models
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
    ScrubRow,
    ScrubRun,
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

# Re-export probe_scrub
from text_watermark_tools.probe_scrub import (
    persist_scrub,
    print_scrub,
    run_scrub_files,
    scrub_token_ids,
)

# Re-export probe_reporting
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

# Re-export probe_eval
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

# Re-export probe_runner
from text_watermark_tools.probe_runner import (
    TRANSFER_DEFAULTS,
    run_probe,
    run_transfer,
)
