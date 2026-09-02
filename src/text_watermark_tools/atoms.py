"""Decode hits atoms from count tables. Not keys, not g-values."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Sequence

from text_watermark_tools.blind import BlindModel, Twin, clip_twins_prefix, load_twins
from text_watermark_tools.indicator import load_indicator
from text_watermark_tools.score import load_tokenizer
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    HitAtom,
    ScoreSpec,
    gated_hit_trace,
    interpolate_trace,
    score_sequence_detail,
)

POSHITS_SPEC = ScoreSpec(kind="gated", min_count=1, instance="key-free-poshits")
POSTOKHITS_SPEC = ScoreSpec(
    kind="gated",
    min_count=1,
    require_token=True,
    instance="key-free-postokhits",
)


def decode_token(tokenizer, tok: int) -> str:
    n = int(tok)
    if n < 0:
        return "<first>"
    return tokenizer.decode([n])


def _pretty_ctx(
    ctx: tuple[int, ...],
    *,
    position_bucket: int,
    decode: Callable[[int], str],
) -> dict:
    if position_bucket > 0 and ctx:
        return {
            "i": int(ctx[0]),
            "tokens": [decode(t) for t in ctx[1:]],
        }
    return {"i": None, "tokens": [decode(t) for t in ctx]}


def atom_to_dict(
    atom: HitAtom,
    *,
    position_bucket: int,
    decode: Callable[[int], str],
) -> dict:
    pretty = _pretty_ctx(
        atom.ctx, position_bucket=position_bucket, decode=decode
    )
    return {
        "i": atom.i,
        "ctx": pretty,
        "next": decode(atom.tok),
        "n_m": atom.n_m,
        "n_u": atom.n_u,
        "c_m": atom.c_m,
        "c_u": atom.c_u,
        "delta": atom.delta,
        "unseen_next": atom.unseen_next,
    }


def summarize_atom_counts(rows: Sequence[dict]) -> list[dict]:
    grouped: dict[tuple, dict] = {}
    for row in rows:
        for hit in row.get("hits", []):
            tokens = tuple(hit["ctx"]["tokens"])
            key = (tokens, hit["next"], bool(hit["unseen_next"]))
            bucket = grouped.setdefault(
                key,
                {
                    "ctx": list(tokens),
                    "next": hit["next"],
                    "unseen_next": bool(hit["unseen_next"]),
                    "delta": float(hit["delta"]),
                    "n": 0,
                },
            )
            bucket["n"] += 1
    return sorted(grouped.values(), key=lambda r: (-r["n"], r["ctx"], r["next"]))


def explain_twin_files(
    twins: Sequence[Twin],
    model: BlindModel,
    spec: ScoreSpec,
    *,
    decode: Callable[[int], str],
    tokhits_spec: ScoreSpec | None = None,
) -> list[dict]:
    skip = tokhits_spec or COUNT_SPECS["tokhits"]
    if spec.require_token:
        skip = spec
    rows = []
    bucket = int(model.position_bucket or 0)
    for twin in twins:
        for sample, seq in enumerate(twin.marked_seqs(), start=1):
            hits = gated_hit_trace(seq, model, spec)
            pos = score_sequence_detail(seq, model, spec)
            tok = score_sequence_detail(seq, model, skip)
            rows.append(
                {
                    "stem": twin.stem,
                    "sample": sample,
                    "side": "marked",
                    "opening": [decode(t) for t in seq],
                    "poshits_lr": pos.lr,
                    "postokhits_lr": tok.lr,
                    "poshits_n_used": pos.n_used,
                    "postokhits_n_used": tok.n_used,
                    "hits": [
                        atom_to_dict(a, position_bucket=bucket, decode=decode)
                        for a in hits
                    ],
                }
            )
        for sample, seq in enumerate(twin.unmarked_seqs(), start=1):
            hits = gated_hit_trace(seq, model, spec)
            pos = score_sequence_detail(seq, model, spec)
            tok = score_sequence_detail(seq, model, skip)
            rows.append(
                {
                    "stem": twin.stem,
                    "sample": sample,
                    "side": "unmarked",
                    "opening": [decode(t) for t in seq],
                    "poshits_lr": pos.lr,
                    "postokhits_lr": tok.lr,
                    "poshits_n_used": pos.n_used,
                    "postokhits_n_used": tok.n_used,
                    "hits": [
                        atom_to_dict(a, position_bucket=bucket, decode=decode)
                        for a in hits
                    ],
                }
            )
    return rows


def dump_opening_atoms(
    tables_dir: Path,
    test_dir: Path,
    out_path: Path | None = None,
    *,
    fit_prefix: int = 4,
    model_name: str = "gpt2",
) -> dict:
    """Rebuild the 4-token poshits atom dump from persisted tables. No keys."""
    model, _meta = load_indicator(tables_dir)
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("atom dump consulted keys / hash_iv / g-values")
    tokenizer = load_tokenizer(model_name)
    twins = clip_twins_prefix(
        load_twins(test_dir, tokenizer=tokenizer),
        int(fit_prefix),
        tokenizer=tokenizer,
    )
    spec = POSHITS_SPEC if model.position_bucket else COUNT_SPECS["hits"]
    skip = POSTOKHITS_SPEC if model.position_bucket else COUNT_SPECS["tokhits"]
    decode = lambda t, tok=tokenizer: decode_token(tok, t)
    rows = explain_twin_files(twins, model, spec, decode=decode, tokhits_spec=skip)
    atom_counts = summarize_atom_counts(rows)
    unseen_n = sum(a["n"] for a in atom_counts if a["unseen_next"])
    seen_n = sum(a["n"] for a in atom_counts if not a["unseen_next"])
    payload = {
        "note": (
            "4-token poshits atoms. Unseen_next is the Laplace occupancy "
            "artifact: shared context, never-seen next token. Not keys."
        ),
        "used_keys": False,
        "n_rows": len(rows),
        "atom_counts": atom_counts,
        "unseen_next_n": unseen_n,
        "seen_next_n": seen_n,
        "rows": rows,
    }
    if out_path is not None:
        Path(out_path).write_text(json.dumps(payload, indent=2) + "\n")
    return payload


DEFAULT_ATOM_WINDOWS: tuple[tuple[int, int], ...] = (
    (0, 4),
    (4, 16),
    (16, 32),
    (32, 64),
    (64, 128),
)


def _in_window(i: int, start: int, end: int) -> bool:
    return int(start) <= int(i) < int(end)


def window_atom_summary(
    rows: Sequence[dict],
    windows: Sequence[tuple[int, int]] = DEFAULT_ATOM_WINDOWS,
    *,
    top_k: int = 20,
) -> list[dict]:
    """Per-window mean delta and top observed-token atoms. Not a detector."""
    out = []
    for start, end in windows:
        marked_d: list[float] = []
        unmarked_d: list[float] = []
        n_unseen = 0
        n_seen = 0
        grouped: dict[tuple, dict] = {}
        for row in rows:
            side = str(row["side"])
            for hit in row.get("hits", []):
                i = int(hit["i"])
                if not _in_window(i, start, end):
                    continue
                delta = float(hit["delta"])
                unseen = bool(hit["unseen_next"])
                if side == "marked":
                    marked_d.append(delta)
                else:
                    unmarked_d.append(delta)
                if unseen:
                    n_unseen += 1
                else:
                    n_seen += 1
                if unseen or side != "marked" or delta <= 0.0:
                    continue
                tokens = tuple(hit["ctx"]["tokens"])
                key = (tokens, hit["next"])
                bucket = grouped.setdefault(
                    key,
                    {
                        "ctx": list(tokens),
                        "next": hit["next"],
                        "delta": 0.0,
                        "n": 0,
                    },
                )
                bucket["n"] += 1
                bucket["delta"] += delta
        top = sorted(grouped.values(), key=lambda r: (-r["n"], r["ctx"], r["next"]))
        for item in top:
            item["mean_delta"] = item["delta"] / max(item["n"], 1)
            del item["delta"]
        out.append(
            {
                "start": start,
                "end": end,
                "n_marked": len(marked_d),
                "n_unmarked": len(unmarked_d),
                "mean_marked_delta": (
                    sum(marked_d) / len(marked_d) if marked_d else 0.0
                ),
                "mean_unmarked_delta": (
                    sum(unmarked_d) / len(unmarked_d) if unmarked_d else 0.0
                ),
                "n_seen": n_seen,
                "n_unseen": n_unseen,
                "top_marked_positive_seen": top[: int(top_k)],
            }
        )
    return out


def dump_interpolate_atoms(
    tables_dir: Path,
    test_dir: Path,
    out_path: Path | None = None,
    *,
    model_name: str = "gpt2",
    windows: Sequence[tuple[int, int]] = DEFAULT_ATOM_WINDOWS,
    top_k: int = 20,
    store_rows: bool = False,
) -> dict:
    """Decode interpolate last-4 atoms from persisted tables. No keys."""
    model, _meta = load_indicator(tables_dir)
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("atom dump consulted keys / hash_iv / g-values")
    tokenizer = load_tokenizer(model_name)
    twins = load_twins(test_dir, tokenizer=tokenizer)
    spec = COUNT_SPECS["interpolate"]
    decode = lambda t, tok=tokenizer: decode_token(tok, t)
    bucket = int(model.position_bucket or 0)
    rows: list[dict] = []
    for twin in twins:
        for sample, seq in enumerate(twin.marked_seqs(), start=1):
            hits = interpolate_trace(seq, model, spec)
            detail = score_sequence_detail(seq, model, spec)
            rows.append(
                {
                    "stem": twin.stem,
                    "sample": sample,
                    "side": "marked",
                    "lr": detail.lr,
                    "n_used": detail.n_used,
                    "hits": [
                        atom_to_dict(a, position_bucket=bucket, decode=decode)
                        for a in hits
                    ],
                }
            )
        for sample, seq in enumerate(twin.unmarked_seqs(), start=1):
            hits = interpolate_trace(seq, model, spec)
            detail = score_sequence_detail(seq, model, spec)
            rows.append(
                {
                    "stem": twin.stem,
                    "sample": sample,
                    "side": "unmarked",
                    "lr": detail.lr,
                    "n_used": detail.n_used,
                    "hits": [
                        atom_to_dict(a, position_bucket=bucket, decode=decode)
                        for a in hits
                    ],
                }
            )
    windows_out = window_atom_summary(rows, windows, top_k=top_k)
    payload = {
        "note": (
            "Interpolate last-4 atoms from frozen count tables. "
            "unseen_next means the observed next token is absent from both "
            "marked and unmarked buckets (Witten–Bell backoff). Not keys, "
            "not a new probe method, not a universal detector."
        ),
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "n_rows": len(rows),
        "windows": windows_out,
        "n_marked_lr_positive": sum(
            1 for r in rows if r["side"] == "marked" and float(r["lr"]) > 0.0
        ),
    }
    if store_rows:
        payload["rows"] = rows
    if out_path is not None:
        Path(out_path).write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def print_interpolate_atoms(payload: dict) -> str:
    lines = [
        "# Interpolate atoms",
        "",
        str(payload.get("note") or ""),
        "",
        f"used_keys={payload.get('used_keys')} n_rows={payload.get('n_rows')} "
        f"marked_lr>0={payload.get('n_marked_lr_positive')}",
        "",
        "| window | mean marked Δ | mean unmarked Δ | seen | unseen |",
        "|---|---|---|---|---|",
    ]
    for win in payload.get("windows") or []:
        lines.append(
            f"| {win['start']}:{win['end']} | "
            f"{win['mean_marked_delta']:.4f} | "
            f"{win['mean_unmarked_delta']:.4f} | "
            f"{win['n_seen']} | {win['n_unseen']} |"
        )
    lines.extend(["", "Top observed-token marked Δ>0 atoms by window:", ""])
    for win in payload.get("windows") or []:
        top = win.get("top_marked_positive_seen") or []
        if not top:
            continue
        lines.append(f"### {win['start']}:{win['end']}")
        for atom in top[:8]:
            ctx = " ".join(repr(t) for t in atom["ctx"])
            lines.append(
                f"- n={atom['n']} meanΔ={atom['mean_delta']:.3f} "
                f"{ctx} → {atom['next']!r}"
            )
        lines.append("")
    lines.append(
        "Not detector_mean. Not Claude. Not a new probe method. "
        "Does not replace 25/48."
    )
    return "\n".join(lines) + "\n"


def persist_interpolate_atoms(payload: dict, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "atoms.json").write_text(json.dumps(payload, indent=2) + "\n")
    (out_dir / "results.md").write_text(print_interpolate_atoms(payload))
