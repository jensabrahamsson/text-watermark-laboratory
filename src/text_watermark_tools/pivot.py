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
    rows = logits[:n]
    chosen = torch.tensor(ids[1 : n + 1], dtype=torch.long)
    tok_logit = rows.gather(1, chosen.unsqueeze(1)).squeeze(1)
    log_probs = torch.log_softmax(rows, dim=-1)
    tok_logp = log_probs.gather(1, chosen.unsqueeze(1)).squeeze(1)
    ranks = (rows > tok_logit.unsqueeze(1)).sum(dim=-1) + 1
    k = min(max(int(top_k), 1), int(rows.shape[-1]))
    top_vals, top_idx = torch.topk(rows, k, dim=-1)
    in_topk = (top_idx == chosen.unsqueeze(1)).any(dim=-1).to(dtype=torch.float32)
    # Rank within top-k; k+1 if the chosen token missed the truncated set.
    within = (top_idx == chosen.unsqueeze(1)).float().argmax(dim=-1) + 1
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


def aggregate_choice_matrix(mat: np.ndarray) -> np.ndarray:
    if mat.size == 0:
        return np.zeros(len(FEATURE_NAMES), dtype=np.float64)
    return mat.mean(axis=0)


def extract_choice_vector(
    token_ids: Sequence[int],
    model: torch.nn.Module,
    *,
    top_k: int = TOP_K,
    logits: Optional[torch.Tensor] = None,
) -> np.ndarray:
    rows = logits if logits is not None else unmarked_logits_for_sequence(
        token_ids, model
    )
    return aggregate_choice_matrix(
        choice_matrix_from_logits(rows, token_ids, top_k=top_k)
    )


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
