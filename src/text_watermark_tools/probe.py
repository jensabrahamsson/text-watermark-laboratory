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
    score_sequence,
    score_surface,
)

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


def _twin_prefix(twin: Twin, prompt_context: bool) -> tuple[int, ...]:
    if not prompt_context:
        return ()
    if not twin.prompt_ids:
        raise ValueError(
            f"prompt-context needs prompt token ids on stem {twin.stem!r}"
        )
    return tuple(int(x) for x in twin.prompt_ids)


def _call_scorer(scorer: ScoreFn, seq, *, prefix: Sequence[int] = ()):
    if not prefix:
        return scorer(seq)
    try:
        return scorer(seq, prefix=prefix)
    except TypeError:
        return scorer(seq)


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


def print_coverage(cov: dict) -> str:
    lines = [
        (
            f"coverage n_prompts={cov['n_prompts']} n_files={cov['n_files']} "
            f"context_len={cov['context_len']} pos_bucket={cov['position_bucket']} "
            f"used_keys={cov['used_keys']}"
        ),
        cov.get("note", ""),
        "",
        "| window | shared last-4 | n | mean support when shared |",
        "|---|---|---|---|",
    ]
    for row in cov.get("by_window") or []:
        lines.append(
            f"| {row['start']}:{row['end']} | {row['shared_frac']:.3f} "
            f"({row['shared']}/{row['n']}) | {row['n']} | "
            f"{row['mean_shared_support']:.2f} |"
        )
    return "\n".join(lines)


def persist_coverage(cov: dict, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "coverage.json").write_text(json.dumps(cov, indent=2) + "\n")
    (out_dir / "coverage.md").write_text(
        "# Key-free last-4 coverage by position\n\n"
        + print_coverage(cov)
        + "\n"
    )


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
                _append_pair(
                    window_parts[(start, end)],
                    held.stem,
                    i + 1,
                    scorer(slice_seq(marked, start, end)),
                    scorer(slice_seq(unmarked, start, end)),
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
                            slice_seq(marked, start, end),
                            model,
                            spec,
                            prefix=held_prefix,
                        ),
                        score_sequence(
                            slice_seq(unmarked, start, end),
                            model,
                            spec,
                            prefix=held_prefix,
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
) -> IndicatorHoldout:
    reader = str(method_name or "hashpool")
    drop_one = reader in ("hashskip", "hashskip2")
    mask_one = reader in ("hashmask", "hashmask2")
    min_count = 2 if reader in ("hashtoklen2", "hashskip2", "hashmask2") else 1
    if reader in (
        "hashtok",
        "hashtoklen",
        "hashtoklen2",
        "hashskip",
        "hashskip2",
        "hashmask",
        "hashmask2",
    ):
        kind = reader
        instance = f"key-free-{reader}"
        if drop_one:
            score_fn = lambda ids, m, k=min_count: score_hashskip(ids, m, min_count=k)
        elif mask_one:
            score_fn = lambda ids, m, k=min_count: score_hashmask(ids, m, min_count=k)
        else:
            score_fn = lambda ids, m, k=min_count: score_hashtok(ids, m, min_count=k)
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
        )
        return (
            lambda ids, m=model, s=score_fn: s(ids, m),
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
            lambda ids, m=model: score_hashmix(ids, m),
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
            lambda ids, m=model, mo=floor: score_hashtokbackoff(
                ids, m, min_order=mo
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
                        scorer, slice_seq(marked, start, end), prefix=held_prefix
                    ),
                    _call_scorer(
                        scorer, slice_seq(unmarked, start, end), prefix=held_prefix
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
        "AUC is single-file ranking; prompt wins are the 10/12 grain. "
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
        "Not detector_mean. Not Claude. Not key recovery."
    )


def _store_prefixes(
    dest: dict[int, list[MethodSummary]],
    src: dict[int, dict[str, IndicatorHoldout]],
) -> None:
    for plen, by_name in src.items():
        bucket = dest.setdefault(int(plen), [])
        seen = {m.name for m in bucket}
        for name, ev in by_name.items():
            if name in seen:
                continue
            bucket.append(summarize_holdout(name, ev))
            seen.add(name)


def _store_windows(
    dest: dict[tuple[int, int], list[MethodSummary]],
    src: dict[tuple[int, int], dict[str, IndicatorHoldout]],
) -> None:
    for win, by_name in src.items():
        bucket = dest.setdefault(win, [])
        seen = {m.name for m in bucket}
        for name, ev in by_name.items():
            if name in seen:
                continue
            bucket.append(summarize_holdout(name, ev))
            seen.add(name)


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
                source = clip_twins_prefix(raw, need_tokens)
    full = collect_choice_matrices(source, lm, prompt_context=prompt_context)
    if open_end is None:
        opening = full
    else:
        opening = slice_matrices(full, 0, open_end)
    main = full if rankpath_full else opening
    return full, opening, main


def nested_stem_gates(ev: IndicatorHoldout) -> dict:
    """Youden and 10% FPR leave-one-stem thresholds on held-out LRs."""
    youden = nested_threshold_by_stem(ev.stems, ev.marked_lrs, ev.unmarked_lrs)
    fpr10 = nested_threshold_by_stem(
        ev.stems, ev.marked_lrs, ev.unmarked_lrs, fpr=0.10
    )
    return {
        "nested-youden-by-stem": nested_stem_eval_to_dict(youden),
        "nested-fpr10-by-stem": nested_stem_eval_to_dict(fpr10),
    }


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
        twins = clip_twins_prefix(twins, int(fit_prefix))
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
        or "hybrid" in extras or "hashtok" in extras or "hashtoklen" in extras
        or "hashtoklen2" in extras or "hashskip" in extras or "hashskip2" in extras
        or "hashmask" in extras or "hashmask2" in extras
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


def format_cascade(payload: dict) -> list[str]:
    """Human lines for the count-then-fallback isolated-file protocol."""
    prec = payload.get("count_precision")
    prec_s = f"{prec:.3f}" if isinstance(prec, float) and prec == prec else "nan"
    n_pm = max(int(payload.get("n_pivot_marked") or 0), 1)
    n_pu = max(int(payload.get("n_pivot_unmarked") or 0), 1)
    n_cm = max(int(payload.get("n_count_marked") or 0), 1)
    n_cu = max(int(payload.get("n_count_unmarked") or 0), 1)
    fallback = str(payload.get("fallback") or "pivot")
    when = str(payload.get("cascade_when") or "coverage")
    if when == "positive":
        rule = (
            f"Cascade: count LR when lr>0, unmarked-LM {fallback} when count "
            "is nonpositive (zeros and covered negatives). "
        )
    else:
        rule = (
            f"Cascade: count LR when n_used>0, unmarked-LM {fallback} otherwise. "
        )
    lines = [
        (
            rule
            + "Signs at 0 are comparable. Mixed AUC is not a detector. "
            "Not keys, not a universal detector."
        ),
        (
            f"count_method={payload.get('count_method')} "
            f"fallback={fallback} "
            f"cascade_when={when} "
            f"pivot_weight={payload.get('pivot_weight')} "
            f"prompt_context={payload.get('prompt_context')} "
            f"used_keys={payload.get('used_keys')}"
        ),
        (
            f"count covered marked {payload.get('n_count_marked')}/"
            f"{payload.get('n_marked')} >0 "
            f"{payload.get('count_marked_above_zero')}/{n_cm} unmarked<=0 "
            f"{payload.get('count_unmarked_at_most_zero')}/{n_cu} "
            f"precision={prec_s}"
        ),
        (
            f"{fallback} fallback marked {payload.get('n_pivot_marked')}/"
            f"{payload.get('n_marked')} >0 "
            f"{payload.get('pivot_marked_above_zero')}/{n_pm} unmarked<=0 "
            f"{payload.get('pivot_unmarked_at_most_zero')}/{n_pu}"
        ),
        (
            f"combined marked>0 {payload.get('combined_marked_above_zero')}/"
            f"{payload.get('n_marked')} unmarked<=0 "
            f"{payload.get('combined_unmarked_at_most_zero')}/"
            f"{payload.get('n_unmarked')}"
        ),
    ]
    if payload.get("rankpath_end"):
        lines.append(
            f"cascade rankpath_end={payload.get('rankpath_end')} "
            "(opening prefix-N, not the full file)"
        )
    fb10 = payload.get("fallback_fpr10") or {}
    comb10 = payload.get("combined_at_fallback_fpr10") or {}
    if fb10:
        lines.append(
            f"{fallback} uncovered FPR10 t={float(fb10.get('threshold') or 0):.4f} "
            f"marked>t {fb10.get('marked_above')}/{fb10.get('n_marked')} "
            f"unmarked<=t {fb10.get('unmarked_at_most')}/{fb10.get('n_unmarked')}"
        )
    if comb10:
        lines.append(
            f"combined at fallback FPR10 marked>t "
            f"{comb10.get('marked_above')}/{comb10.get('n_marked')} "
            f"unmarked<=t {comb10.get('unmarked_at_most')}/{comb10.get('n_unmarked')}. "
            "Count stays at 0; mixed AUC is still not a detector."
        )
    marked_fallback = payload.get("pivot_fallback_marked") or []
    if marked_fallback:
        lines.append(f"{fallback}-fallback marked files:")
        for row in marked_fallback:
            score = float(row.get("score") or 0.0)
            sign = "lr>0" if score > 0.0 else "lr<=0"
            lines.append(
                f"- `{row.get('stem')}` draw {row.get('sample')}: "
                f"{row.get('opening_text', '')} {sign}={score:.4f}"
            )
    return lines


def _cascade_json(payload: dict | None) -> dict | None:
    import math

    if not payload:
        return None

    def conv(x):
        if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
            return None
        if isinstance(x, dict):
            return {k: conv(v) for k, v in x.items()}
        if isinstance(x, list):
            return [conv(v) for v in x]
        return x

    return conv(payload)


def print_probe(run: ProbeRun) -> str:
    lines = [
        (
            f"probe n_methods={len(run.methods)} pair_dir={run.pair_dir} "
            f"context_len={run.context_len} model={run.model_name} "
            f"max_draws={run.max_draws} prefix_lens={list(run.prefix_lens)} "
            f"windows={[f'{a}:{b}' for a, b in run.windows]} "
            f"fit_prefix={run.fit_prefix} pos_bucket={run.position_bucket} "
            f"rankpath_full={getattr(run, 'rankpath_full', False)} "
            f"rankpath_pos_bucket={getattr(run, 'rankpath_pos_bucket', None)} "
            f"cascade_rankpath_end={getattr(run, 'cascade_rankpath_end', None)} "
            f"cascade_when={getattr(run, 'cascade_when', 'coverage')} "
            f"include_first={run.include_first} prompt_context={run.prompt_context} "
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
    lines.append(
        "| method | marked zeros | unmarked zeros | decided tp/fn | "
        "decided fp/tn | precision |"
    )
    lines.append("|---|---|---|---|---|---|")
    for m in run.methods:
        g = coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs)
        prec = f"{g.precision:.3f}" if g.precision == g.precision else "nan"
        lines.append(
            f"| {m.name} | {g.n_marked_zero}/{g.n_marked} | "
            f"{g.n_unmarked_zero}/{g.n_unmarked} | "
            f"{g.decided_tp}/{g.decided_fn} | {g.decided_fp}/{g.decided_tn} | "
            f"{prec} |"
        )
    lines.append("")
    lines.append(
        "| method | nested-youden-by-stem marked>t | unmarked<=t | "
        "mean t | sens | spec |"
    )
    lines.append("|---|---|---|---|---|---|")
    for m in run.methods:
        gate = nested_stem_gates(m.holdout)["nested-youden-by-stem"]
        lines.append(
            f"| {m.name} | {gate['n_marked_above']}/{gate['n_marked']} | "
            f"{gate['n_unmarked_at_most']}/{gate['n_unmarked']} | "
            f"{gate['mean_threshold']:.4f} | {gate['sensitivity']:.3f} | "
            f"{gate['specificity']:.3f} |"
        )
    if run.prefixes:
        lines.append("")
        lines.append(
            "| prefix tokens | method | prompt wins | file auc | "
            "nested-by-stem marked | unmarked |"
        )
        lines.append("|---|---|---|---|---|---|")
        for plen in sorted(run.prefixes):
            for m in run.prefixes[plen]:
                gate = nested_stem_gates(m.holdout)["nested-youden-by-stem"]
                lines.append(
                    f"| {plen} | {m.name} | {m.n_prompt_wins}/{m.n_prompts} | "
                    f"{m.binary.auc:.3f} | "
                    f"{gate['n_marked_above']}/{gate['n_marked']} | "
                    f"{gate['n_unmarked_at_most']}/{gate['n_unmarked']} |"
                )
    if run.window_results:
        lines.append("")
        lines.append(
            "| window tokens | method | prompt wins | file auc | "
            "nested-by-stem marked | unmarked |"
        )
        lines.append("|---|---|---|---|---|---|")
        for start, end in sorted(run.window_results):
            for m in run.window_results[(start, end)]:
                gate = nested_stem_gates(m.holdout)["nested-youden-by-stem"]
                lines.append(
                    f"| {start}:{end} | {m.name} | "
                    f"{m.n_prompt_wins}/{m.n_prompts} | "
                    f"{m.binary.auc:.3f} | "
                    f"{gate['n_marked_above']}/{gate['n_marked']} | "
                    f"{gate['n_unmarked_at_most']}/{gate['n_unmarked']} |"
                )
    if run.cascade:
        lines.extend(["", *format_cascade(run.cascade)])
    if run.coverage:
        lines.append("")
        lines.append(print_coverage(run.coverage))
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
        "max_draws": run.max_draws,
        "prefix_lens": list(run.prefix_lens),
        "windows": [f"{a}:{b}" for a, b in run.windows],
        "fit_prefix": run.fit_prefix,
        "position_bucket": run.position_bucket,
        "include_first": run.include_first,
        "prompt_context": run.prompt_context,
        "pivot_weights": list(run.pivot_weights),
        "rankpath_full": bool(getattr(run, "rankpath_full", False)),
        "rankpath_pos_bucket": getattr(run, "rankpath_pos_bucket", None),
        "cascade_rankpath_end": getattr(run, "cascade_rankpath_end", None),
        "cascade_when": getattr(run, "cascade_when", "coverage"),
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
            "nested_stem": nested_stem_gates(m.holdout),
            "coverage_gate": coverage_gate_to_dict(
                coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs)
            ),
        }
        table["methods"].append(row)
        persist_holdout(m.holdout, out_dir / m.name)
    table["prefixes"] = []
    for plen in sorted(run.prefixes):
        for m in run.prefixes[plen]:
            table["prefixes"].append(
                {
                    "prefix_tokens": plen,
                    "name": m.name,
                    "n_prompt_wins": m.n_prompt_wins,
                    "n_prompts": m.n_prompts,
                    "binary": binary_eval_to_dict(m.binary),
                    "nested_stem": nested_stem_gates(m.holdout),
                    "used_keys": m.holdout.used_keys,
                }
            )
            persist_holdout(m.holdout, out_dir / f"prefix-{plen}" / m.name)
    table["window_scores"] = []
    for start, end in sorted(run.window_results):
        for m in run.window_results[(start, end)]:
            table["window_scores"].append(
                {
                    "start": start,
                    "end": end,
                    "name": m.name,
                    "n_prompt_wins": m.n_prompt_wins,
                    "n_prompts": m.n_prompts,
                    "binary": binary_eval_to_dict(m.binary),
                    "nested_stem": nested_stem_gates(m.holdout),
                    "used_keys": m.holdout.used_keys,
                }
            )
            persist_holdout(
                m.holdout, out_dir / _window_dir(start, end) / m.name
            )
    table["has_coverage"] = run.coverage is not None
    if run.coverage is not None:
        persist_coverage(run.coverage, out_dir)
    if run.cascade:
        (out_dir / "cascade.json").write_text(
            json.dumps(_cascade_json(run.cascade), indent=2) + "\n"
        )
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    (out_dir / "results.md").write_text(
        "# Key-free probe\n\n" + print_probe(run) + "\n"
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


def _append_threshold(
    run: TransferRun,
    *,
    name: str,
    source: str,
    threshold: float,
    test_ev: IndicatorHoldout,
) -> None:
    tp, tn, sens, spec = counts_at_threshold(
        test_ev.marked_lrs, test_ev.unmarked_lrs, threshold
    )
    run.thresholds.append(
        ThresholdRow(
            name=name,
            train_youden=threshold,
            n_marked_above=tp,
            n_unmarked_at_most=tn,
            n_marked=len(test_ev.marked_lrs),
            n_unmarked=len(test_ev.unmarked_lrs),
            sensitivity=sens,
            specificity=spec,
            source=source,
        )
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
) -> TransferRun:
    """Fit on train twins, score every test file. No test prompt enters the fit."""
    train, test, overlap = apply_overlap(
        train_twins, test_twins, mode=overlap_mode
    )
    if shuffle_labels:
        train = shuffle_twin_sides(train, seed=shuffle_seed)
    raw_train, raw_test = train, test
    if fit_prefix and fit_prefix > 0:
        train = clip_twins_prefix(train, int(fit_prefix))
        test = clip_twins_prefix(test, int(fit_prefix))
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
        n in extras for n in ("hybrid", "stack")
    )
    need_hash = any(
        n in extras
        for n in (
            "hashpool",
            "hashvote",
            "hybrid",
            "stack",
            "hashmix",
            "hashtok",
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
        )
        if need_hash and any(
            n in extras for n in ("hashpool", "hashvote", "hybrid", "stack", "hashtok")
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
        if "pospool" in extras
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
            (lambda ids, prefix=(), m=count_model, s=spec: score_sequence(
                ids, m, s, prefix=prefix
            )),
            spec.instance,
            name,
            "ids",
        )
    if "hashpool" in extras:
        assert hash_model is not None
        scorers["hashpool"] = (
            (lambda ids, m=hash_model: score_hashpool(ids, m)),
            "key-free-hashpool",
            "hashpool",
            "ids",
        )
    if "hashvote" in extras:
        assert hash_model is not None
        scorers["hashvote"] = (
            (lambda ids, m=hash_model: score_hashpool_vote(ids, m)),
            "key-free-hashvote",
            "hashvote",
            "ids",
        )
    if "hashtok" in extras:
        assert hash_model is not None
        scorers["hashtok"] = (
            (lambda ids, m=hash_model: score_hashtok(ids, m)),
            "key-free-hashtok",
            "hashtok",
            "ids",
        )
    if "hashtoklen" in extras:
        assert hash_len_model is not None
        scorers["hashtoklen"] = (
            (lambda ids, m=hash_len_model: score_hashtok(ids, m)),
            "key-free-hashtoklen",
            "hashtoklen",
            "ids",
        )
    if "hashtoklen2" in extras:
        assert hash_len_model is not None
        scorers["hashtoklen2"] = (
            (lambda ids, m=hash_len_model: score_hashtok(ids, m, min_count=2)),
            "key-free-hashtoklen2",
            "hashtoklen2",
            "ids",
        )
    if "hashskip" in extras:
        assert hash_skip_model is not None
        scorers["hashskip"] = (
            (lambda ids, m=hash_skip_model: score_hashskip(ids, m)),
            "key-free-hashskip",
            "hashskip",
            "ids",
        )
    if "hashskip2" in extras:
        assert hash_skip_model is not None
        scorers["hashskip2"] = (
            (lambda ids, m=hash_skip_model: score_hashskip(ids, m, min_count=2)),
            "key-free-hashskip2",
            "hashskip2",
            "ids",
        )
    if "hashmask" in extras:
        assert hash_mask_model is not None
        scorers["hashmask"] = (
            (lambda ids, m=hash_mask_model: score_hashmask(ids, m)),
            "key-free-hashmask",
            "hashmask",
            "ids",
        )
    if "hashmask2" in extras:
        assert hash_mask_model is not None
        scorers["hashmask2"] = (
            (lambda ids, m=hash_mask_model: score_hashmask(ids, m, min_count=2)),
            "key-free-hashmask2",
            "hashmask2",
            "ids",
        )
    if "hybrid" in extras:
        assert count_model is not None and hash_model is not None
        scorers["hybrid"] = (
            (lambda ids, c=count_model, h=hash_model: score_hybrid(ids, c, h)),
            "key-free-hybrid",
            "hybrid",
            "ids",
        )
    if "hashmix" in extras:
        assert mix_model is not None
        scorers["hashmix"] = (
            (lambda ids, m=mix_model: score_hashmix(ids, m)),
            "key-free-hashmix",
            "hashmix",
            "ids",
        )
    if "hashtokbackoff" in extras:
        assert mix_model is not None
        scorers["hashtokbackoff"] = (
            (
                lambda ids, m=mix_model: score_hashtokbackoff(
                    ids, m, min_order=1
                )
            ),
            "key-free-hashtokbackoff",
            "hashtokbackoff",
            "ids",
        )
    if "hashtokbackoff2" in extras:
        assert mix_model is not None
        scorers["hashtokbackoff2"] = (
            (
                lambda ids, m=mix_model: score_hashtokbackoff(
                    ids, m, min_order=2
                )
            ),
            "key-free-hashtokbackoff2",
            "hashtokbackoff2",
            "ids",
        )
    if "hashtoklenbackoff" in extras:
        assert mix_len_model is not None
        scorers["hashtoklenbackoff"] = (
            (
                lambda ids, m=mix_len_model: score_hashtokbackoff(
                    ids, m, min_order=1
                )
            ),
            "key-free-hashtoklenbackoff",
            "hashtoklenbackoff",
            "ids",
        )
    if "hashtoklenbackoff2" in extras:
        assert mix_len_model is not None
        scorers["hashtoklenbackoff2"] = (
            (
                lambda ids, m=mix_len_model: score_hashtokbackoff(
                    ids, m, min_order=2
                )
            ),
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
            (
                lambda ids, prefix=(), m=pos_model, s=spec: score_sequence(
                    ids, m, s, prefix=prefix
                )
            ),
            spec.instance,
            name,
            "ids",
        )
    if "pospool" in extras:
        assert pos_hash is not None
        scorers["pospool"] = (
            (lambda ids, m=pos_hash: score_hashpool(ids, m)),
            "key-free-pospool",
            "pospool",
            "ids",
        )

    note = (
        "Train on one twin directory, score the other. Shared prompt stems "
        "are dropped as overlap_mode says. In-sample Youden is optimistic. "
        "nested-youden / nested-fpr10 come from leave-one-prompt-out on "
        "training stems only, then frozen on the test files. "
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


def print_transfer(run: TransferRun) -> str:
    lines = [
        (
            f"transfer n_methods={len(run.methods)} train={run.train_dir} "
            f"test={run.test_dir} n_train={run.n_train_prompts} "
            f"n_test={run.n_test_prompts} overlap_mode={run.overlap_mode} "
            f"dropped={len(run.dropped_stems)} context_len={run.context_len} "
            f"model={run.model_name} nested={run.nested} "
            f"shuffle_seed={run.shuffle_seed} used_keys={run.used_keys} "
            f"hash_iv={run.used_hash_iv} g_values={run.used_g_values} "
            f"include_first={run.include_first} prompt_context={run.prompt_context} "
            f"rankpath_full={getattr(run, 'rankpath_full', False)} "
            f"rankpath_pos_bucket={getattr(run, 'rankpath_pos_bucket', None)} "
            f"cascade_rankpath_end={getattr(run, 'cascade_rankpath_end', None)} "
            f"cascade_when={getattr(run, 'cascade_when', 'coverage')}"
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
        "| method | marked zeros | unmarked zeros | decided tp/fn | "
        "decided fp/tn | precision |"
    )
    lines.append("|---|---|---|---|---|---|")
    for m in run.methods:
        g = coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs)
        prec = f"{g.precision:.3f}" if g.precision == g.precision else "nan"
        lines.append(
            f"| {m.name} | {g.n_marked_zero}/{g.n_marked} | "
            f"{g.n_unmarked_zero}/{g.n_unmarked} | "
            f"{g.decided_tp}/{g.decided_fn} | {g.decided_fp}/{g.decided_tn} | "
            f"{prec} |"
        )
    lines.append("")
    lines.append(
        "Zeros are lr==0: no shared last-k, or (tokhits/postokhits/"
        "tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/"
        "hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/"
        "hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2) no observed next token under that "
        "context (or colliding hash). They are abstentions, not sign "
        "errors. poshits and hashpool can still score an *unseen* next "
        "token via Laplace; that occupancy artifact is not a token "
        "preference. tokbackoff / hashtokbackoff shrink last-k until an "
        "observed next token hits; tokbackoff2 / hashtokbackoff2 stop at "
        "last-2. hashtoklen / hashtoklenbackoff hash only exact last-k "
        "(short prefixes are not mixed into a longer-order table). "
        "hashskip hashes exact last-k with one token dropped (tagged "
        "skip-grams, not last-(k-1)). hashmask replaces one last-k token "
        "with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / "
        "hashmask2 skip "
        "singleton hash collisions (min_count=2). hashtok is the hashpool analog of "
        "tokhits. None of these is key recovery."
    )
    lines.append("")
    lines.append(
        "| method | source | t | test marked>t | test unmarked≤t "
        "| sens | spec |"
    )
    lines.append("|---|---|---|---|---|---|---|")
    for row in run.thresholds:
        lines.append(
            f"| {row.name} | {row.source} | {row.train_youden:.4f} | "
            f"{row.n_marked_above}/{row.n_marked} | "
            f"{row.n_unmarked_at_most}/{row.n_unmarked} | "
            f"{row.sensitivity:.3f} | {row.specificity:.3f} |"
        )
    if run.dropped_stems:
        lines.append("")
        lines.append("dropped stems: " + ", ".join(run.dropped_stems))
    if run.prefixes:
        lines.append("")
        lines.append(
            "| prefix tokens | method | prompt wins | file auc | "
            "marked>0 | unmarked<=0 |"
        )
        lines.append("|---|---|---|---|---|---|")
        for plen in sorted(run.prefixes):
            for m in run.prefixes[plen]:
                b = m.binary
                lines.append(
                    f"| {plen} | {m.name} | {m.n_prompt_wins}/{m.n_prompts} | "
                    f"{b.auc:.3f} | {b.n_positive_above_zero}/{b.n_positive} | "
                    f"{b.n_negative_at_most_zero}/{b.n_negative} |"
                )
    if run.window_results:
        lines.append("")
        lines.append(
            "| window tokens | method | prompt wins | file auc | "
            "marked>0 | unmarked<=0 |"
        )
        lines.append("|---|---|---|---|---|---|")
        for start, end in sorted(run.window_results):
            for m in run.window_results[(start, end)]:
                b = m.binary
                lines.append(
                    f"| {start}:{end} | {m.name} | "
                    f"{m.n_prompt_wins}/{m.n_prompts} | "
                    f"{b.auc:.3f} | {b.n_positive_above_zero}/{b.n_positive} | "
                    f"{b.n_negative_at_most_zero}/{b.n_negative} |"
                )
    if run.cascade:
        lines.extend(["", *format_cascade(run.cascade)])
    lines.append("")
    for m in run.methods:
        lines.append(format_binary_eval(m.binary, label=m.name))
        lines.append(
            format_coverage_gate(
                coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs),
                label=m.name,
            )
        )
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
        "nested": run.nested,
        "shuffle_seed": run.shuffle_seed,
        "surface_context_len": run.surface_context_len,
        "prefix_lens": list(run.prefix_lens),
        "windows": [f"{a}:{b}" for a, b in run.windows],
        "fit_prefix": run.fit_prefix,
        "position_bucket": run.position_bucket,
        "include_first": run.include_first,
        "prompt_context": run.prompt_context,
        "pivot_weights": list(run.pivot_weights),
        "rankpath_full": bool(getattr(run, "rankpath_full", False)),
        "rankpath_pos_bucket": getattr(run, "rankpath_pos_bucket", None),
        "cascade_fallback": getattr(run, "cascade_fallback", "pivot"),
        "cascade_rankpath_end": getattr(run, "cascade_rankpath_end", None),
        "cascade_when": getattr(run, "cascade_when", "coverage"),
        "note": run.note,
        "caveat": CAVEAT,
        "methods": [],
        "thresholds": [row.__dict__ for row in run.thresholds],
    }
    def _t(name: str, source: str) -> float | None:
        for row in run.thresholds:
            if row.name == name and row.source == source:
                return row.train_youden
        return None

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
            "coverage_gate": coverage_gate_to_dict(
                coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs)
            ),
        }
        table["methods"].append(row)
        persist_holdout(m.holdout, out_dir / m.name)
    persist_tables = run.shuffle_seed is None
    if persist_tables and run.hash_model is not None:
        nested_t = _t("hashpool", "nested-youden") or _t("hashtok", "nested-youden")
        in_t = _t("hashpool", "in-sample-youden") or _t("hashtok", "in-sample-youden")
        persist_hashpool(
            run.hash_model,
            out_dir / "tables-hashpool",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden" if nested_t is not None else "in-sample-youden"
            ),
        )
    if persist_tables and getattr(run, "hash_len_model", None) is not None:
        nested_t = _t("hashtoklen", "nested-youden") or _t(
            "hashtoklen2", "nested-youden"
        )
        in_t = _t("hashtoklen", "in-sample-youden") or _t(
            "hashtoklen2", "in-sample-youden"
        )
        persist_hashpool(
            run.hash_len_model,
            out_dir / "tables-hashtoklen",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-hashtoklen"
                if nested_t is not None
                else "in-sample-youden-hashtoklen"
            ),
        )
        if run.hash_model is None and getattr(run, "hash_skip_model", None) is None and getattr(run, "hash_mask_model", None) is None:
            persist_hashpool(
                run.hash_len_model,
                out_dir / "tables-hashpool",
                model_name=run.model_name,
                pair_dir=run.train_dir,
                n_train_prompts=run.n_train_prompts,
                decision_threshold=nested_t if nested_t is not None else in_t,
                decision_source=(
                    "nested-youden-hashtoklen"
                    if nested_t is not None
                    else "in-sample-youden-hashtoklen"
                ),
            )
    if persist_tables and getattr(run, "hash_skip_model", None) is not None:
        nested_t = _t("hashskip", "nested-youden") or _t(
            "hashskip2", "nested-youden"
        )
        in_t = _t("hashskip", "in-sample-youden") or _t(
            "hashskip2", "in-sample-youden"
        )
        persist_hashpool(
            run.hash_skip_model,
            out_dir / "tables-hashskip",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-hashskip"
                if nested_t is not None
                else "in-sample-youden-hashskip"
            ),
        )
    if persist_tables and getattr(run, "hash_mask_model", None) is not None:
        nested_t = _t("hashmask", "nested-youden") or _t(
            "hashmask2", "nested-youden"
        )
        in_t = _t("hashmask", "in-sample-youden") or _t(
            "hashmask2", "in-sample-youden"
        )
        persist_hashpool(
            run.hash_mask_model,
            out_dir / "tables-hashmask",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-hashmask"
                if nested_t is not None
                else "in-sample-youden-hashmask"
            ),
        )
    if persist_tables and run.surface_model is not None:
        nested_t = _t("surface", "nested-youden")
        in_t = _t("surface", "in-sample-youden")
        persist_hashpool(
            run.surface_model,
            out_dir / "tables-surface",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-surface"
                if nested_t is not None
                else "in-sample-youden-surface"
            ),
        )
    if persist_tables and run.count_model is not None:
        nested_t = _t("hits", "nested-youden")
        in_t = _t("hits", "in-sample-youden")
        persist_indicator(
            run.count_model,
            out_dir / "tables-counts",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-hits" if nested_t is not None else "in-sample-youden-hits"
            ),
        )
    if persist_tables and run.pos_model is not None:
        nested_t = _t("poshits", "nested-youden") or _t("poshitmass", "nested-youden")
        in_t = _t("poshits", "in-sample-youden") or _t("poshitmass", "in-sample-youden")
        persist_indicator(
            run.pos_model,
            out_dir / "tables-poshits",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-poshits"
                if nested_t is not None
                else "in-sample-youden-poshits"
            ),
        )
    if persist_tables and run.pos_hash is not None:
        nested_t = _t("pospool", "nested-youden")
        in_t = _t("pospool", "in-sample-youden")
        persist_hashpool(
            run.pos_hash,
            out_dir / "tables-pospool",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-pospool"
                if nested_t is not None
                else "in-sample-youden-pospool"
            ),
        )
    table["prefixes"] = []
    for plen in sorted(run.prefixes):
        for m in run.prefixes[plen]:
            table["prefixes"].append(
                {
                    "prefix_tokens": plen,
                    "name": m.name,
                    "n_prompt_wins": m.n_prompt_wins,
                    "n_prompts": m.n_prompts,
                    "binary": binary_eval_to_dict(m.binary),
                    "nested_stem": nested_stem_gates(m.holdout),
                    "used_keys": m.holdout.used_keys,
                }
            )
            persist_holdout(m.holdout, out_dir / f"prefix-{plen}" / m.name)
    table["window_scores"] = []
    for start, end in sorted(run.window_results):
        for m in run.window_results[(start, end)]:
            table["window_scores"].append(
                {
                    "start": start,
                    "end": end,
                    "name": m.name,
                    "n_prompt_wins": m.n_prompt_wins,
                    "n_prompts": m.n_prompts,
                    "binary": binary_eval_to_dict(m.binary),
                    "nested_stem": nested_stem_gates(m.holdout),
                    "used_keys": m.holdout.used_keys,
                }
            )
            persist_holdout(
                m.holdout, out_dir / _window_dir(start, end) / m.name
            )
    if persist_tables and run.pivot_fits:
        from text_watermark_tools.pivot import persist_pivot

        for weight, fit in run.pivot_fits.items():
            nested_t = _t(f"pivot-lda{'' if weight == 'uniform' else '-' + ('intopk' if weight == 'in_topk' else weight)}", "nested-youden")
            in_t = _t(
                f"pivot-lda{'' if weight == 'uniform' else '-' + ('intopk' if weight == 'in_topk' else weight)}",
                "in-sample-youden",
            )
            persist_pivot(
                fit,
                out_dir / f"tables-pivot-{weight}",
                model_name=run.model_name,
                pair_dir=run.train_dir,
                n_train_prompts=run.n_train_prompts,
                weight=weight,
                prompt_context=bool(run.prompt_context),
                decision_threshold=nested_t if nested_t is not None else in_t,
                decision_source=(
                    f"nested-youden-pivot-{weight}"
                    if nested_t is not None
                    else f"in-sample-youden-pivot-{weight}"
                ),
            )
        canonical = run.pivot_fits.get("uniform") or next(iter(run.pivot_fits.values()))
        canonical_weight = (
            "uniform" if "uniform" in run.pivot_fits else next(iter(run.pivot_fits))
        )
        nested_t = _t("pivot-lda", "nested-youden")
        in_t = _t("pivot-lda", "in-sample-youden")
        persist_pivot(
            canonical,
            out_dir / "tables-pivot",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            weight=canonical_weight,
            prompt_context=bool(run.prompt_context),
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-pivot" if nested_t is not None else "in-sample-youden-pivot"
            ),
        )
    elif persist_tables and run.pivot_fit is not None:
        from text_watermark_tools.pivot import persist_pivot

        nested_t = _t("pivot-lda", "nested-youden")
        in_t = _t("pivot-lda", "in-sample-youden")
        weight = run.pivot_weights[0] if run.pivot_weights else "uniform"
        persist_pivot(
            run.pivot_fit,
            out_dir / "tables-pivot",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            weight=weight,
            prompt_context=bool(run.prompt_context),
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-pivot" if nested_t is not None else "in-sample-youden-pivot"
            ),
        )
    if persist_tables and run.rankpath_model is not None:
        from text_watermark_tools.rankpath import persist_rankpath

        nested_t = _t("rankpath", "nested-youden")
        in_t = _t("rankpath", "in-sample-youden")
        persist_rankpath(
            run.rankpath_model,
            out_dir / "tables-rankpath",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            prompt_context=bool(run.prompt_context),
            spec_name="rankpath",
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-rankpath"
                if nested_t is not None
                else "in-sample-youden-rankpath"
            ),
        )
    if run.cascade:
        (out_dir / "cascade.json").write_text(
            json.dumps(_cascade_json(run.cascade), indent=2) + "\n"
        )
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
