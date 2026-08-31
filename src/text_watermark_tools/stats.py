"""Key-free evaluation extras: AUC, permutation, binomial, Youden.

None of this consults watermark keys, hash_iv, or g-values. It only
summarises already-computed scores.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class BinaryEval:
    n_positive: int
    n_negative: int
    auc: float
    mean_positive: float
    mean_negative: float
    mean_diff: float
    n_positive_above_zero: int
    n_negative_at_most_zero: int
    permutation_p: float
    binomial_p_above_zero: float
    youden_threshold: float
    youden_sensitivity: float
    youden_specificity: float
    youden_j: float
    n_perm: int


def _mean(xs: Sequence[float]) -> float:
    if not xs:
        return float("nan")
    return sum(xs) / len(xs)


def roc_auc(positive: Sequence[float], negative: Sequence[float]) -> float:
    """Mann–Whitney AUC: P(pos > neg) + 0.5 P(equal)."""
    n1 = len(positive)
    n2 = len(negative)
    if n1 == 0 or n2 == 0:
        return float("nan")
    hits = 0.0
    for a in positive:
        for b in negative:
            if a > b:
                hits += 1.0
            elif a == b:
                hits += 0.5
    return hits / (n1 * n2)


def binomial_sf(k: int, n: int, p: float = 0.5) -> float:
    """P(X >= k) for X ~ Binomial(n, p)."""
    if n <= 0:
        return float("nan")
    k = max(0, min(k, n + 1))
    total = 0.0
    for i in range(k, n + 1):
        total += math.comb(n, i) * (p**i) * ((1.0 - p) ** (n - i))
    return total


def permutation_mean_diff_p(
    positive: Sequence[float],
    negative: Sequence[float],
    *,
    n_perm: int = 2000,
    seed: int = 0,
) -> float:
    """One-sided P(mean_pos - mean_neg as large as observed | shuffled labels).

    Adds one to numerator and denominator (conservative).
    """
    pos = list(positive)
    neg = list(negative)
    n1 = len(pos)
    if n1 == 0 or not neg or n_perm <= 0:
        return float("nan")
    observed = _mean(pos) - _mean(neg)
    pool = pos + neg
    rng = random.Random(seed)
    count = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        diff = _mean(pool[:n1]) - _mean(pool[n1:])
        if diff >= observed:
            count += 1
    return (count + 1) / (n_perm + 1)


def youden_threshold(
    positive: Sequence[float], negative: Sequence[float]
) -> tuple[float, float, float, float]:
    """Return (threshold, sensitivity, specificity, J) maximising Youden's J.

    A score is called positive when it is strictly greater than the threshold.
    Ties in J keep the threshold closest to 0.
    """
    pos = list(positive)
    neg = list(negative)
    if not pos or not neg:
        return 0.0, float("nan"), float("nan"), float("nan")

    candidates = sorted({0.0, *pos, *neg})
    best_t = 0.0
    best_j = -2.0
    best_sens = 0.0
    best_spec = 0.0
    n_pos = len(pos)
    n_neg = len(neg)
    for t in candidates:
        tp = sum(1 for s in pos if s > t)
        tn = sum(1 for s in neg if s <= t)
        sens = tp / n_pos
        spec = tn / n_neg
        j = sens + spec - 1.0
        closer = abs(t) < abs(best_t) - 1e-15
        if j > best_j + 1e-15 or (abs(j - best_j) <= 1e-15 and closer):
            best_j = j
            best_t = t
            best_sens = sens
            best_spec = spec
    return best_t, best_sens, best_spec, best_j


def binary_eval(
    positive: Sequence[float],
    negative: Sequence[float],
    *,
    n_perm: int = 2000,
    seed: int = 0,
) -> BinaryEval:
    pos = list(positive)
    neg = list(negative)
    n_pos_above = sum(1 for s in pos if s > 0.0)
    y_t, y_sens, y_spec, y_j = youden_threshold(pos, neg)
    return BinaryEval(
        n_positive=len(pos),
        n_negative=len(neg),
        auc=roc_auc(pos, neg),
        mean_positive=_mean(pos),
        mean_negative=_mean(neg),
        mean_diff=_mean(pos) - _mean(neg),
        n_positive_above_zero=n_pos_above,
        n_negative_at_most_zero=sum(1 for s in neg if s <= 0.0),
        permutation_p=permutation_mean_diff_p(pos, neg, n_perm=n_perm, seed=seed),
        binomial_p_above_zero=binomial_sf(n_pos_above, len(pos), 0.5),
        youden_threshold=y_t,
        youden_sensitivity=y_sens,
        youden_specificity=y_spec,
        youden_j=y_j,
        n_perm=n_perm,
    )


def format_binary_eval(ev: BinaryEval, *, label: str = "") -> str:
    prefix = f"{label} " if label else ""
    return (
        f"{prefix}auc={ev.auc:.3f} "
        f"mean_pos={ev.mean_positive:.4f} mean_neg={ev.mean_negative:.4f} "
        f"diff={ev.mean_diff:.4f} "
        f"pos>0={ev.n_positive_above_zero}/{ev.n_positive} "
        f"neg<=0={ev.n_negative_at_most_zero}/{ev.n_negative} "
        f"perm_p={ev.permutation_p:.4g} "
        f"binom_p={ev.binomial_p_above_zero:.4g} "
        f"youden_t={ev.youden_threshold:.4f} "
        f"youden_sens={ev.youden_sensitivity:.3f} "
        f"youden_spec={ev.youden_specificity:.3f} "
        f"J={ev.youden_j:.3f}"
    )


def binary_eval_to_dict(ev: BinaryEval) -> dict:
    return {
        "n_positive": ev.n_positive,
        "n_negative": ev.n_negative,
        "auc": ev.auc,
        "mean_positive": ev.mean_positive,
        "mean_negative": ev.mean_negative,
        "mean_diff": ev.mean_diff,
        "n_positive_above_zero": ev.n_positive_above_zero,
        "n_negative_at_most_zero": ev.n_negative_at_most_zero,
        "permutation_p": ev.permutation_p,
        "binomial_p_above_zero": ev.binomial_p_above_zero,
        "youden_threshold": ev.youden_threshold,
        "youden_sensitivity": ev.youden_sensitivity,
        "youden_specificity": ev.youden_specificity,
        "youden_j": ev.youden_j,
        "n_perm": ev.n_perm,
    }
