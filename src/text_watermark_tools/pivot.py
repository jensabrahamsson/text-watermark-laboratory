"""Unmarked-LM choice geometry: a key-free probe of tournament sampling.

SynthID-Text only reweights the language model's top-k. A finished string
therefore carries a second footprint besides token/context counts: *which*
near-tied candidate was chosen.

This module reads that footprint with the public unmarked model (GPT-2 by
default). It never computes g-values, never reads watermark keys, and never
calls detector_mean.

Two uses:

1. Detection. Per-token features (log-prob, rank, gap to argmax, top-k
   entropy) are aggregated and scored with a leave-one-prompt-out linear
   discriminant. A one-feature rank baseline is reported beside it.

2. Removal. Snapping each token to the unmarked argmax of the *original*
   prefix (no re-decoding) is a key-free scrub. The official scorer is
   then used only as a reference measurement of whether the public mark
   died — the snap itself does not consult it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import torch

from text_watermark_tools.score import TOP_K

FEATURE_NAMES: tuple[str, ...] = (
    "mean_logp",
    "mean_rank",
    "mean_rank_topk",
    "frac_in_topk",
    "mean_gap",
    "mean_entropy_topk",
)

RANK_TOPK_INDEX = FEATURE_NAMES.index("mean_rank_topk")
IN_TOPK_INDEX = FEATURE_NAMES.index("frac_in_topk")
ENTROPY_INDEX = FEATURE_NAMES.index("mean_entropy_topk")
PIVOT_KIND = "key-free-pivot"
PIVOT_TABLES = "tables.json"
PIVOT_WEIGHTS = ("uniform", "entropy", "in_topk")


@dataclass(frozen=True)
class PivotFit:
    weights: np.ndarray
    midpoint: np.ndarray
    rank_sign: float
    rank_center: float
    used_keys: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False


def unmarked_logits_for_sequence(
    token_ids: Sequence[int],
    model: torch.nn.Module,
) -> torch.Tensor:
    """Logits[i] predicts token_ids[i+1]. One forward pass. No keys."""
    ids = list(int(t) for t in token_ids)
    if len(ids) < 2:
        vocab = int(getattr(model.config, "vocab_size", 2))
        return torch.zeros((0, vocab))
    device = next(model.parameters()).device
    batch = torch.tensor([ids], dtype=torch.long, device=device)
    with torch.no_grad():
        logits = model(input_ids=batch).logits[0, :-1].detach().cpu()
    return logits


def choice_rows_from_logits(
    logits: torch.Tensor,
    chosen: Sequence[int],
    *,
    top_k: int = TOP_K,
) -> np.ndarray:
    """Per-token feature rows. ``logits[i]`` predicts ``chosen[i]``. Shape [T, 6]."""
    ids = [int(t) for t in chosen]
    n = min(int(logits.shape[0]), len(ids))
    if n <= 0:
        return np.zeros((0, len(FEATURE_NAMES)), dtype=np.float64)
    rows = logits[:n]
    chosen_t = torch.tensor(ids[:n], dtype=torch.long)
    tok_logit = rows.gather(1, chosen_t.unsqueeze(1)).squeeze(1)
    log_probs = torch.log_softmax(rows, dim=-1)
    tok_logp = log_probs.gather(1, chosen_t.unsqueeze(1)).squeeze(1)
    ranks = (rows > tok_logit.unsqueeze(1)).sum(dim=-1) + 1
    k = min(max(int(top_k), 1), int(rows.shape[-1]))
    top_vals, top_idx = torch.topk(rows, k, dim=-1)
    in_topk = (top_idx == chosen_t.unsqueeze(1)).any(dim=-1).to(dtype=torch.float32)
    # Rank within top-k; k+1 if the chosen token missed the truncated set.
    within = (top_idx == chosen_t.unsqueeze(1)).float().argmax(dim=-1) + 1
    rank_topk = torch.where(in_topk.bool(), within, torch.full_like(within, k + 1))
    max_logit = top_vals[:, 0]
    gap = max_logit - tok_logit
    top_logp = torch.log_softmax(top_vals, dim=-1)
    entropy = -(top_logp.exp() * top_logp).sum(dim=-1)
    mat = torch.stack(
        [
            tok_logp,
            ranks.to(dtype=torch.float32),
            rank_topk.to(dtype=torch.float32),
            in_topk,
            gap,
            entropy,
        ],
        dim=1,
    )
    return mat.numpy().astype(np.float64)


def choice_matrix_from_logits(
    logits: torch.Tensor,
    token_ids: Sequence[int],
    *,
    top_k: int = TOP_K,
) -> np.ndarray:
    """Per-token feature rows aligned with token_ids[1:]. Shape [T-1, 6]."""
    ids = [int(t) for t in token_ids]
    n = min(int(logits.shape[0]), max(len(ids) - 1, 0))
    if n <= 0:
        return np.zeros((0, len(FEATURE_NAMES)), dtype=np.float64)
    return choice_rows_from_logits(logits[:n], ids[1 : n + 1], top_k=top_k)


def generated_logits(
    token_ids: Sequence[int],
    model: torch.nn.Module,
    *,
    prefix: Sequence[int] = (),
) -> tuple[torch.Tensor, list[int]]:
    """Logits aligned with generated tokens that the unmarked LM can predict.

    With a prompt prefix, every generated token is predicted, including token 0
    (the first tournament decision). Without a prefix, token 0 has no context
    and is skipped — the legacy generated-only reader.
    """
    generated = [int(t) for t in token_ids]
    pref = [int(t) for t in prefix]
    vocab = int(getattr(model.config, "vocab_size", 2))
    if pref:
        full = pref + generated
        if len(full) < 2 or not generated:
            return torch.zeros((0, vocab)), []
        rows = unmarked_logits_for_sequence(full, model)
        start = len(pref) - 1
        n = min(int(rows.shape[0]) - start, len(generated))
        if n <= 0:
            return torch.zeros((0, vocab)), []
        return rows[start : start + n], generated[:n]
    if len(generated) < 2:
        return torch.zeros((0, vocab)), []
    rows = unmarked_logits_for_sequence(generated, model)
    chosen = generated[1:]
    n = min(int(rows.shape[0]), len(chosen))
    return rows[:n], chosen[:n]


def parse_pivot_weights(raw: str | Sequence[str] | None) -> tuple[str, ...]:
    if raw is None or raw == "":
        return ("uniform",)
    if isinstance(raw, str):
        parts = [p.strip().lower() for p in raw.split(",") if p.strip()]
    else:
        parts = [str(p).strip().lower() for p in raw if str(p).strip()]
    if not parts:
        return ("uniform",)
    unknown = [p for p in parts if p not in PIVOT_WEIGHTS]
    if unknown:
        raise ValueError(
            f"unknown pivot weight {unknown[0]!r}; choose {', '.join(PIVOT_WEIGHTS)}"
        )
    seen: list[str] = []
    for p in parts:
        if p not in seen:
            seen.append(p)
    return tuple(seen)


def pivot_method_name(kind: str, weight: str) -> str:
    if weight == "uniform":
        return f"pivot-{kind}"
    slug = "intopk" if weight == "in_topk" else weight
    return f"pivot-{kind}-{slug}"


def aggregate_choice_matrix(
    mat: np.ndarray,
    *,
    weight: str = "uniform",
) -> np.ndarray:
    """Mean feature vector. ``entropy`` weights tokens the mixin can reweight.

    Tournament sampling only changes the draw when top-k candidates compete.
    Uniform averaging over a long file dilutes those near-ties. Entropy
    weighting (and ``in_topk``) is still key-free: it uses the unmarked LM.
    """
    if mat.size == 0:
        return np.zeros(len(FEATURE_NAMES), dtype=np.float64)
    name = (weight or "uniform").strip().lower()
    if name == "uniform":
        return mat.mean(axis=0)
    if name == "in_topk":
        mask = mat[:, IN_TOPK_INDEX] >= 0.5
        if not bool(mask.any()):
            return mat.mean(axis=0)
        return mat[mask].mean(axis=0)
    if name == "entropy":
        w = np.clip(mat[:, ENTROPY_INDEX], 0.0, None)
        total = float(w.sum())
        if total <= 0.0:
            return mat.mean(axis=0)
        return (mat * (w / total)[:, None]).sum(axis=0)
    raise ValueError(
        f"unknown pivot weight {weight!r}; choose {', '.join(PIVOT_WEIGHTS)}"
    )


def extract_choice_matrix(
    token_ids: Sequence[int],
    model: torch.nn.Module,
    *,
    top_k: int = TOP_K,
    prefix: Sequence[int] = (),
    logits: Optional[torch.Tensor] = None,
) -> np.ndarray:
    if logits is not None and not prefix:
        return choice_matrix_from_logits(logits, token_ids, top_k=top_k)
    rows, chosen = generated_logits(token_ids, model, prefix=prefix)
    return choice_rows_from_logits(rows, chosen, top_k=top_k)


def extract_choice_vector(
    token_ids: Sequence[int],
    model: torch.nn.Module,
    *,
    top_k: int = TOP_K,
    logits: Optional[torch.Tensor] = None,
    prefix: Sequence[int] = (),
    weight: str = "uniform",
) -> np.ndarray:
    return aggregate_choice_matrix(
        extract_choice_matrix(
            token_ids, model, top_k=top_k, prefix=prefix, logits=logits
        ),
        weight=weight,
    )


def cascade_source(n_used: int, fallback: str = "pivot") -> str:
    """Count tables when they have coverage; fallback reader otherwise."""
    return "count" if int(n_used) > 0 else str(fallback or "pivot")


def cascade_score(count_lr: float, n_used: int, fallback_lr: float) -> float:
    """Threshold-0 sign is comparable; mixed magnitudes are not an AUC."""
    if int(n_used) > 0:
        return float(count_lr)
    return float(fallback_lr)


def _combined_at_fallback_threshold(rows: Sequence[dict], threshold: float) -> dict:
    """Count stays at t=0; fallback files use ``score > threshold``."""
    t = float(threshold)
    n_m = n_u = m_pos = u_nonpos = 0
    for row in rows:
        side = row.get("side")
        source = row.get("source")
        score = float(row.get("score") or 0.0)
        if side == "marked":
            n_m += 1
            if source == "count":
                if score > 0.0:
                    m_pos += 1
            elif score > t:
                m_pos += 1
        elif side == "unmarked":
            n_u += 1
            if source == "count":
                if score <= 0.0:
                    u_nonpos += 1
            elif score <= t:
                u_nonpos += 1
    return {
        "threshold": t,
        "marked_above": m_pos,
        "n_marked": n_m,
        "unmarked_at_most": u_nonpos,
        "n_unmarked": n_u,
    }


def _fallback_operating_points(
    rows: Sequence[dict],
    fallback_m: Sequence[dict],
    fallback_u: Sequence[dict],
) -> dict:
    """Youden / 10% FPR on uncovered files only. Not a mixed-magnitude AUC."""
    from text_watermark_tools.stats import (
        binary_eval,
        binary_eval_to_dict,
        threshold_at_fpr,
    )

    fb_pos = [float(r["score"]) for r in fallback_m]
    fb_neg = [float(r["score"]) for r in fallback_u]
    if not fb_pos or not fb_neg:
        return {
            "fallback_binary": None,
            "fallback_fpr10": None,
            "combined_at_fallback_youden": None,
            "combined_at_fallback_fpr10": None,
        }
    ev = binary_eval(fb_pos, fb_neg, n_perm=200)
    t10 = threshold_at_fpr(fb_neg, fpr=0.10)
    return {
        "fallback_binary": binary_eval_to_dict(ev),
        "fallback_fpr10": {
            "threshold": t10,
            "marked_above": sum(1 for s in fb_pos if s > t10),
            "unmarked_at_most": sum(1 for s in fb_neg if s <= t10),
            "n_marked": len(fb_pos),
            "n_unmarked": len(fb_neg),
        },
        "combined_at_fallback_youden": _combined_at_fallback_threshold(
            rows, ev.youden_threshold
        ),
        "combined_at_fallback_fpr10": _combined_at_fallback_threshold(rows, t10),
    }


def summarize_cascade(rows: Sequence[dict]) -> dict:
    """Per-file count/pivot split. Mixed scores are not one ranking."""
    marked = [r for r in rows if r.get("side") == "marked"]
    unmarked = [r for r in rows if r.get("side") == "unmarked"]

    def _subset(items: Sequence[dict], source: str) -> list[dict]:
        return [r for r in items if r.get("source") == source]

    def _pos(items: Sequence[dict]) -> int:
        return sum(1 for r in items if float(r["score"]) > 0.0)

    def _nonpos(items: Sequence[dict]) -> int:
        return sum(1 for r in items if float(r["score"]) <= 0.0)

    count_m = _subset(marked, "count")
    count_u = _subset(unmarked, "count")
    fallback_m = [r for r in marked if r.get("source") != "count"]
    fallback_u = [r for r in unmarked if r.get("source") != "count"]
    fallback = "pivot"
    for row in list(fallback_m) + list(fallback_u) + list(rows):
        src = str(row.get("source") or "")
        if src and src != "count":
            fallback = src
            break
    return {
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "fallback": fallback,
        "note": (
            "Count LR when n_used>0 (coverage); unmarked-LM fallback "
            f"({fallback}) otherwise. Signs at threshold 0 are comparable. "
            "A single AUC on mixed magnitudes is not a detector. "
            "Not keys, not a universal detector."
        ),
        "n_marked": len(marked),
        "n_unmarked": len(unmarked),
        "n_count_marked": len(count_m),
        "n_count_unmarked": len(count_u),
        "n_pivot_marked": len(fallback_m),
        "n_pivot_unmarked": len(fallback_u),
        "n_fallback_marked": len(fallback_m),
        "n_fallback_unmarked": len(fallback_u),
        "count_marked_above_zero": _pos(count_m),
        "count_unmarked_at_most_zero": _nonpos(count_u),
        "pivot_marked_above_zero": _pos(fallback_m),
        "pivot_unmarked_at_most_zero": _nonpos(fallback_u),
        "fallback_marked_above_zero": _pos(fallback_m),
        "fallback_unmarked_at_most_zero": _nonpos(fallback_u),
        "combined_marked_above_zero": _pos(marked),
        "combined_unmarked_at_most_zero": _nonpos(unmarked),
        "count_precision": (
            _pos(count_m) / (_pos(count_m) + (len(count_u) - _nonpos(count_u)))
            if (_pos(count_m) + (len(count_u) - _nonpos(count_u))) > 0
            else float("nan")
        ),
        "pivot_fallback_marked": [
            {
                "stem": r.get("stem"),
                "sample": r.get("sample"),
                "score": r.get("score"),
                "opening_text": r.get("opening_text", ""),
                "source": r.get("source"),
            }
            for r in fallback_m
        ],
        **_fallback_operating_points(rows, fallback_m, fallback_u),
    }


def fisher_lda(
    X_pos: np.ndarray,
    X_neg: np.ndarray,
    *,
    ridge: float = 1e-3,
) -> tuple[np.ndarray, np.ndarray]:
    """Weights and class-midpoint so (x - midpoint) @ w is the score."""
    if X_pos.ndim != 2 or X_neg.ndim != 2:
        raise ValueError("LDA inputs must be 2-D")
    mu_p = X_pos.mean(axis=0)
    mu_n = X_neg.mean(axis=0)
    d_p = X_pos - mu_p
    d_n = X_neg - mu_n
    sw = d_p.T @ d_p + d_n.T @ d_n
    dim = sw.shape[0]
    sw = sw + ridge * np.eye(dim)
    weights = np.linalg.pinv(sw) @ (mu_p - mu_n)
    midpoint = 0.5 * (mu_p + mu_n)
    return weights, midpoint


def lda_score(x: np.ndarray, weights: np.ndarray, midpoint: np.ndarray) -> float:
    return float((x - midpoint) @ weights)


def fit_pivot(X_marked: np.ndarray, X_unmarked: np.ndarray) -> PivotFit:
    if X_marked.size == 0 or X_unmarked.size == 0:
        dim = len(FEATURE_NAMES)
        return PivotFit(
            weights=np.zeros(dim),
            midpoint=np.zeros(dim),
            rank_sign=1.0,
            rank_center=0.0,
        )
    weights, midpoint = fisher_lda(X_marked, X_unmarked)
    rank_m = float(X_marked[:, RANK_TOPK_INDEX].mean())
    rank_u = float(X_unmarked[:, RANK_TOPK_INDEX].mean())
    rank_sign = 1.0 if rank_m >= rank_u else -1.0
    rank_center = 0.5 * (rank_m + rank_u)
    return PivotFit(
        weights=weights,
        midpoint=midpoint,
        rank_sign=rank_sign,
        rank_center=rank_center,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )


def score_pivot_lda(vec: np.ndarray, fit: PivotFit) -> float:
    if fit.used_keys or fit.used_hash_iv or fit.used_g_values:
        raise RuntimeError("pivot consulted keys / hash_iv / g-values")
    return lda_score(vec, fit.weights, fit.midpoint)


def score_pivot_rank(vec: np.ndarray, fit: PivotFit) -> float:
    if fit.used_keys or fit.used_hash_iv or fit.used_g_values:
        raise RuntimeError("pivot consulted keys / hash_iv / g-values")
    return float(fit.rank_sign * (vec[RANK_TOPK_INDEX] - fit.rank_center))


def snap_to_unmarked_argmax(
    token_ids: Sequence[int],
    logits: torch.Tensor,
    *,
    top_k: int = TOP_K,
    only_if_in_topk: bool = True,
) -> tuple[list[int], int]:
    """Replace chosen tokens with the unmarked top-k argmax of each original prefix.

    Lookups use the original sequence, so earlier flips do not change later
    contexts. That is a scrub, not a fluent rewrite.
    """
    ids = [int(t) for t in token_ids]
    n = min(int(logits.shape[0]), max(len(ids) - 1, 0))
    if n <= 0:
        return ids, 0
    k = min(max(int(top_k), 1), int(logits.shape[-1]))
    top_idx = torch.topk(logits[:n], k, dim=-1).indices
    n_flips = 0
    for i in range(n):
        pos = i + 1
        argmax = int(top_idx[i, 0].item())
        current = ids[pos]
        if current == argmax:
            continue
        if only_if_in_topk and current not in set(int(x) for x in top_idx[i].tolist()):
            continue
        ids[pos] = argmax
        n_flips += 1
    return ids, n_flips


def persist_pivot(
    fit: PivotFit,
    out_dir: Path,
    *,
    model_name: str = "gpt2",
    pair_dir: str = "",
    n_train_prompts: int = 0,
    weight: str = "uniform",
    prompt_context: bool = False,
    top_k: int = TOP_K,
    decision_threshold: float | None = None,
    decision_source: str = "",
) -> Path:
    """Write a frozen unmarked-LM geometry reader. Not keys. Not detector_mean."""
    if fit.used_keys or fit.used_hash_iv or fit.used_g_values:
        raise RuntimeError("refusing to persist a pivot that used keys")
    import json

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": PIVOT_KIND,
        "instance": "key-free-pivot-lda",
        "model_name": model_name,
        "pair_dir": pair_dir,
        "n_train_prompts": n_train_prompts,
        "weight": str(weight),
        "prompt_context": bool(prompt_context),
        "top_k": int(top_k),
        "weights": [float(x) for x in np.asarray(fit.weights).ravel()],
        "midpoint": [float(x) for x in np.asarray(fit.midpoint).ravel()],
        "rank_sign": float(fit.rank_sign),
        "rank_center": float(fit.rank_center),
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "caveat": (
            "Not detector_mean. Not Claude. Not Anthropic. "
            "Unmarked-LM choice geometry, not watermark keys. "
            "prompt_context=true cannot score a lone file without the prompt. "
            "A stored decision_threshold is a frozen operating point, "
            "not a universal detector."
        ),
    }
    if decision_threshold is not None:
        payload["decision_threshold"] = float(decision_threshold)
        payload["decision_source"] = str(decision_source or "unspecified")
    path = out_dir / PIVOT_TABLES
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def pivot_from_payload(raw: dict) -> PivotFit:
    if str(raw.get("kind") or "") != PIVOT_KIND:
        raise ValueError("not a key-free pivot table")
    if raw.get("used_keys") or raw.get("used_hash_iv") or raw.get("used_g_values"):
        raise RuntimeError("pivot file claims it used keys / hash_iv / g")
    weights = np.asarray(raw.get("weights") or [], dtype=np.float64)
    midpoint = np.asarray(raw.get("midpoint") or [], dtype=np.float64)
    if weights.size != len(FEATURE_NAMES) or midpoint.size != len(FEATURE_NAMES):
        raise ValueError("pivot weights/midpoint must have 6 unmarked-LM features")
    return PivotFit(
        weights=weights,
        midpoint=midpoint,
        rank_sign=float(raw.get("rank_sign", 1.0)),
        rank_center=float(raw.get("rank_center", 0.0)),
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )


def load_pivot(tables_dir: Path) -> tuple[PivotFit, dict]:
    import json

    path = Path(tables_dir)
    if path.is_dir():
        path = path / PIVOT_TABLES
    raw = json.loads(path.read_text())
    return pivot_from_payload(raw), raw


def collect_choice_matrices(
    twins,
    model: torch.nn.Module,
    *,
    top_k: int = TOP_K,
    prompt_context: bool = False,
) -> dict[tuple[str, int, str], np.ndarray]:
    """One unmarked-LM forward per draw. Keys: (stem, sample, marked|unmarked)."""
    out: dict[tuple[str, int, str], np.ndarray] = {}
    for twin in twins:
        prefix: Sequence[int] = ()
        if prompt_context:
            prefix = tuple(int(x) for x in twin.prompt_ids)
            if not prefix:
                raise ValueError(
                    f"prompt-context pivot needs prompt token ids on stem {twin.stem!r}"
                )
        for i, ids in enumerate(twin.marked_seqs()):
            out[(twin.stem, i + 1, "marked")] = extract_choice_matrix(
                ids, model, top_k=top_k, prefix=prefix
            )
        for i, ids in enumerate(twin.unmarked_seqs()):
            out[(twin.stem, i + 1, "unmarked")] = extract_choice_matrix(
                ids, model, top_k=top_k, prefix=prefix
            )
    return out


def vectors_from_matrices(
    mats: dict[tuple[str, int, str], np.ndarray],
    *,
    weight: str = "uniform",
) -> dict[tuple[str, int, str], np.ndarray]:
    return {key: aggregate_choice_matrix(mat, weight=weight) for key, mat in mats.items()}


def fit_pivot_from_vectors(
    vecs: dict[tuple[str, int, str], np.ndarray],
    train_stems: Sequence[str],
) -> PivotFit:
    hold = set(train_stems)
    marked = [
        vecs[key]
        for key in vecs
        if key[0] in hold and key[2] == "marked"
    ]
    unmarked = [
        vecs[key]
        for key in vecs
        if key[0] in hold and key[2] == "unmarked"
    ]
    if not marked or not unmarked:
        dim = len(FEATURE_NAMES)
        return PivotFit(
            weights=np.zeros(dim),
            midpoint=np.zeros(dim),
            rank_sign=1.0,
            rank_center=0.0,
        )
    return fit_pivot(np.stack(marked), np.stack(unmarked))
