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
        load_twins(test_dir, tokenizer=tokenizer), int(fit_prefix)
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
