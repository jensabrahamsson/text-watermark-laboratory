"""Opening-overlap bound for isolated-file key-free indication.

Isolated postokhits / postokbackoff recall equals the fraction of test
files that share at least one observed-token atom with the training
tables: ``lr == 0`` iff ``n_used == 0``. Exact 4-token opening copy is a
stricter lower bound. Covering a miss means putting that opening in
train, not recovering keys, ``hash_iv``, or g-values.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from text_watermark_tools.atoms import _pretty_ctx, decode_token
from text_watermark_tools.blind import Twin, _scored_ctx, clip_twins_prefix, load_twins
from text_watermark_tools.indicator import CAVEAT
from text_watermark_tools.probe import POS_SPECS
from text_watermark_tools.score import load_tokenizer
from text_watermark_tools.stats import coverage_gate, coverage_gate_to_dict
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    ScoreSpec,
    _count,
    _ctx_has_support,
    _naked_tokens,
    _next_token_seen,
    _tok_count,
    fit_count_model,
    gated_hit_trace,
    score_sequence_detail,
)

BUCKETED_NAMES = frozenset(POS_SPECS)


@dataclass(frozen=True)
class TrainGroup:
    name: str
    twins: list[Twin]


def resolve_spec(name: str) -> ScoreSpec:
    if name in POS_SPECS:
        return POS_SPECS[name]
    if name in COUNT_SPECS:
        return COUNT_SPECS[name]
    known = sorted(set(POS_SPECS) | set(COUNT_SPECS))
    raise ValueError(f"unknown openings method {name!r}; choose one of {known}")


def opening_tuple(seq: Sequence[int], n: int = 4) -> tuple[int, ...]:
    return tuple(int(t) for t in seq[:n])


def distinct_openings(twins: Sequence[Twin], n: int = 4) -> set[tuple[int, ...]]:
    out: set[tuple[int, ...]] = set()
    for twin in twins:
        for seq in twin.marked_seqs():
            if seq:
                out.add(opening_tuple(seq, n))
    return out


def _fit(
    twins: Sequence[Twin],
    *,
    name: str,
    context_len: int,
    position_bucket: int,
    include_first: bool,
):
    bucket = int(position_bucket) if name in BUCKETED_NAMES else 0
    if bucket < 0:
        bucket = 0
    model = fit_count_model(
        twins,
        context_len=context_len,
        position_bucket=bucket,
        include_first=include_first,
    )
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("openings fit consulted keys / hash_iv / g-values")
    model.include_first = bool(include_first)
    return model


def candidate_rows(
    seq: Sequence[int],
    model,
    spec: ScoreSpec,
    *,
    decode: Callable[[int], str],
) -> list[dict]:
    """Every (position, order) lookup. Used to explain zeros. Not keys."""
    score_first = bool(spec.include_first or spec.first_only or model.include_first)
    min_order = max(1, int(spec.min_order or 1))
    rows = []
    seen: set[tuple] = set()
    bucket = int(model.position_bucket or 0)
    for i, tok in enumerate(seq):
        if i == 0 and not score_first:
            continue
        if spec.first_only and i > 0:
            continue
        t = int(tok)
        for length in range(int(model.context_len), 0, -1):
            ctx = _scored_ctx(seq, i, int(length), bucket)
            naked = _naked_tokens(ctx, model)
            if spec.kind == "tokbackoff" and len(naked) < min_order:
                continue
            key = (i, len(naked), ctx, t)
            if key in seen:
                continue
            seen.add(key)
            support = _ctx_has_support(model, ctx, spec) if spec.min_count > 0 else True
            seen_next = _next_token_seen(model, ctx, t)
            rows.append(
                {
                    "i": i,
                    "order": len(naked),
                    "ctx": _pretty_ctx(ctx, position_bucket=bucket, decode=decode),
                    "next": decode(t),
                    "n_m": _count(model.marked, ctx),
                    "n_u": _count(model.unmarked, ctx),
                    "c_m": _tok_count(model.marked, ctx, t),
                    "c_u": _tok_count(model.unmarked, ctx, t),
                    "support": bool(support),
                    "seen_next": bool(seen_next),
                    "would_hit": bool(support and (seen_next if spec.require_token else True)),
                }
            )
    return rows


def _file_row(
    stem: str,
    sample: int,
    side: str,
    seq: Sequence[int],
    model,
    spec: ScoreSpec,
    *,
    decode: Callable[[int], str],
    train_openings: set[tuple[int, ...]],
    prefix_n: int,
) -> dict:
    detail = score_sequence_detail(seq, model, spec)
    hits = gated_hit_trace(seq, model, spec)
    opening = [decode(t) for t in seq]
    exact = opening_tuple(seq, prefix_n) in train_openings
    row = {
        "stem": stem,
        "sample": sample,
        "side": side,
        "opening": opening,
        "opening_text": "".join(opening).strip(),
        "lr": detail.lr,
        "n_used": detail.n_used,
        "n_positions": detail.n_positions,
        "covered": detail.n_used > 0,
        "exact_opening": bool(exact),
        "hit_orders": [len(_naked_tokens(a.ctx, model)) for a in hits],
        "hits": [
            {
                "i": a.i,
                "order": len(_naked_tokens(a.ctx, model)),
                "ctx": _pretty_ctx(
                    a.ctx,
                    position_bucket=int(model.position_bucket or 0),
                    decode=decode,
                ),
                "next": decode(a.tok),
                "n_m": a.n_m,
                "n_u": a.n_u,
                "c_m": a.c_m,
                "c_u": a.c_u,
                "delta": a.delta,
                "unseen_next": a.unseen_next,
            }
            for a in hits
        ],
    }
    if detail.n_used == 0:
        cands = candidate_rows(seq, model, spec, decode=decode)
        row["needed"] = [
            c
            for c in cands
            if c["order"] >= max(1, int(spec.min_order or 1))
        ]
        row["nearest"] = [
            c for c in cands if c["support"] or c["seen_next"] or c["n_m"] or c["n_u"]
        ]
    return row


def score_split(
    train: Sequence[Twin],
    test: Sequence[Twin],
    spec: ScoreSpec,
    *,
    name: str,
    context_len: int,
    position_bucket: int,
    include_first: bool,
    decode: Callable[[int], str],
    prefix_n: int,
) -> dict:
    model = _fit(
        train,
        name=name,
        context_len=context_len,
        position_bucket=position_bucket,
        include_first=include_first,
    )
    train_openings = distinct_openings(train, prefix_n)
    rows = []
    marked_lrs: list[float] = []
    unmarked_lrs: list[float] = []
    for twin in test:
        for sample, seq in enumerate(twin.marked_seqs(), start=1):
            row = _file_row(
                twin.stem,
                sample,
                "marked",
                seq,
                model,
                spec,
                decode=decode,
                train_openings=train_openings,
                prefix_n=prefix_n,
            )
            rows.append(row)
            marked_lrs.append(row["lr"])
        for sample, seq in enumerate(twin.unmarked_seqs(), start=1):
            row = _file_row(
                twin.stem,
                sample,
                "unmarked",
                seq,
                model,
                spec,
                decode=decode,
                train_openings=train_openings,
                prefix_n=prefix_n,
            )
            rows.append(row)
            unmarked_lrs.append(row["lr"])
    gate = coverage_gate(marked_lrs, unmarked_lrs)
    marked_rows = [r for r in rows if r["side"] == "marked"]
    n_exact = sum(1 for r in marked_rows if r["exact_opening"])
    n_covered = sum(1 for r in marked_rows if r["covered"])
    zeros = [
        {
            "stem": r["stem"],
            "sample": r["sample"],
            "opening_text": r["opening_text"],
            "nearest": r.get("nearest", []),
        }
        for r in marked_rows
        if not r["covered"]
    ]
    last1_hits = 0
    last1_later = 0
    for r in marked_rows:
        if not r["covered"] or not r["hit_orders"]:
            continue
        if max(r["hit_orders"]) == 1:
            last1_hits += 1
            hit_is = [h["i"] for h in r["hits"]]
            if hit_is and min(hit_is) > 1:
                last1_later += 1
    return {
        "method": name,
        "instance": spec.instance,
        "used_keys": False,
        "n_train_stems": len(train),
        "n_train_openings": len(train_openings),
        "n_marked": len(marked_rows),
        "n_exact_opening": n_exact,
        "n_covered": n_covered,
        "n_last1_only": last1_hits,
        "n_last1_later": last1_later,
        "coverage_gate": coverage_gate_to_dict(gate),
        "zeros": zeros,
        "rows": rows,
    }


def stem_curve(
    train: Sequence[Twin],
    test: Sequence[Twin],
    spec: ScoreSpec,
    *,
    name: str,
    context_len: int,
    position_bucket: int,
    include_first: bool,
    prefix_n: int,
) -> list[dict]:
    """Add train stems in sorted order. Recall is monotonic in coverage."""
    ordered = sorted(train, key=lambda t: t.stem)
    points = []
    so_far: list[Twin] = []
    for twin in ordered:
        so_far.append(twin)
        model = _fit(
            so_far,
            name=name,
            context_len=context_len,
            position_bucket=position_bucket,
            include_first=include_first,
        )
        n_open = len(distinct_openings(so_far, prefix_n))
        covered = 0
        n_test = 0
        for held in test:
            for seq in held.marked_seqs():
                n_test += 1
                if score_sequence_detail(seq, model, spec).n_used > 0:
                    covered += 1
        points.append(
            {
                "n_stems": len(so_far),
                "last_stem": twin.stem,
                "n_train_openings": n_open,
                "n_covered": covered,
                "n_test": n_test,
                "recall": covered / n_test if n_test else 0.0,
            }
        )
    return points


def run_openings(
    groups: Sequence[TrainGroup],
    test: Sequence[Twin],
    *,
    methods: Sequence[str],
    fit_prefix: int = 4,
    position_bucket: int = 1,
    include_first: bool = False,
    context_len: int = 4,
    model_name: str = "gpt2",
    with_stem_curve: bool = True,
    curve_method: str = "postokbackoff",
) -> dict:
    tokenizer = load_tokenizer(model_name)
    decode = lambda t, tok=tokenizer: decode_token(tok, t)
    prefix_n = int(fit_prefix) if fit_prefix and fit_prefix > 0 else 4
    grouped = [
        TrainGroup(
            g.name,
            clip_twins_prefix(g.twins, prefix_n) if fit_prefix and fit_prefix > 0 else list(g.twins),
        )
        for g in groups
    ]
    held = clip_twins_prefix(list(test), prefix_n) if fit_prefix and fit_prefix > 0 else list(test)
    names = [m.strip() for m in methods if str(m).strip()]
    if not names:
        names = ["postokhits", "postokbackoff", "postokbackoff2"]
    cumul: list[Twin] = []
    curve = []
    last_by_method: dict[str, dict] = {}
    for group in grouped:
        cumul.extend(group.twins)
        point = {
            "upto": group.name,
            "n_train_stems": len(cumul),
            "n_train_openings": len(distinct_openings(cumul, prefix_n)),
            "methods": {},
        }
        for name in names:
            spec = resolve_spec(name)
            split = score_split(
                cumul,
                held,
                spec,
                name=name,
                context_len=context_len,
                position_bucket=position_bucket,
                include_first=include_first,
                decode=decode,
                prefix_n=prefix_n,
            )
            last_by_method[name] = split
            point["methods"][name] = {
                "n_covered": split["n_covered"],
                "n_exact_opening": split["n_exact_opening"],
                "n_last1_only": split["n_last1_only"],
                "n_last1_later": split["n_last1_later"],
                "n_train_openings": split["n_train_openings"],
                "coverage_gate": split["coverage_gate"],
                "zero_openings": [
                    f"{z['stem']}-{z['sample']}: {z['opening_text']}"
                    for z in split["zeros"]
                ],
            }
        curve.append(point)
    stem_points = []
    if with_stem_curve and curve_method in names and cumul:
        stem_points = stem_curve(
            cumul,
            held,
            resolve_spec(curve_method),
            name=curve_method,
            context_len=context_len,
            position_bucket=position_bucket,
            include_first=include_first,
            prefix_n=prefix_n,
        )
    return {
        "note": (
            "Isolated-file observed-token recall equals opening-atom "
            "overlap with train. Exact 4-token copy is a lower bound. "
            "Not keys, not hash_iv, not g-values, not a universal detector."
        ),
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "model_name": model_name,
        "fit_prefix": prefix_n,
        "position_bucket": int(position_bucket),
        "include_first": bool(include_first),
        "context_len": int(context_len),
        "groups": [g.name for g in grouped],
        "n_test_stems": len(held),
        "methods": names,
        "curve": curve,
        "stem_curve": stem_points,
        "final": {
            name: {
                "n_covered": split["n_covered"],
                "n_exact_opening": split["n_exact_opening"],
                "n_last1_only": split["n_last1_only"],
                "n_last1_later": split["n_last1_later"],
                "n_train_openings": split["n_train_openings"],
                "coverage_gate": split["coverage_gate"],
                "zeros": split["zeros"],
            }
            for name, split in last_by_method.items()
        },
        "caveat": CAVEAT,
    }


def print_openings(payload: dict) -> str:
    lines = [
        "# Opening-overlap bound",
        "",
        payload["note"],
        "",
        (
            f"fit_prefix={payload['fit_prefix']} "
            f"pos_bucket={payload['position_bucket']} "
            f"include_first={payload['include_first']} "
            f"used_keys={payload['used_keys']}"
        ),
        "",
        "| upto | stems | distinct openings | method | covered | exact 4-token | last-1 only | last-1 later | decided fp | precision |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for point in payload.get("curve") or []:
        for name, row in point["methods"].items():
            g = row["coverage_gate"]
            prec = g.get("precision")
            prec_s = f"{prec:.3f}" if isinstance(prec, float) and prec == prec else "nan"
            lines.append(
                f"| {point['upto']} | {point['n_train_stems']} | "
                f"{point['n_train_openings']} | {name} | "
                f"{row['n_covered']}/{g['n_marked']} | "
                f"{row['n_exact_opening']}/{g['n_marked']} | "
                f"{row['n_last1_only']} | {row.get('n_last1_later', 0)} | "
                f"{g['decided_fp']} | {prec_s} |"
            )
    lines.append("")
    lines.append("Zeros on the full combined train:")
    for name, block in (payload.get("final") or {}).items():
        lines.append("")
        lines.append(f"### {name} ({len(block['zeros'])} marked zeros)")
        for z in block["zeros"]:
            lines.append(f"- `{z['stem']}` draw {z['sample']}: {z['opening_text']}")
    lines.append("")
    lines.append(payload.get("caveat") or CAVEAT)
    return "\n".join(lines)


def persist_openings(payload: dict, out_dir: Path) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "coverage.json").write_text(json.dumps(payload, indent=2) + "\n")
    (out_dir / "results.md").write_text(print_openings(payload) + "\n")
    return out_dir / "coverage.json"


def load_group(path: Path, tokenizer, name: str | None = None) -> TrainGroup:
    twins = load_twins(path, tokenizer=tokenizer)
    return TrainGroup(name or path.name, twins)
