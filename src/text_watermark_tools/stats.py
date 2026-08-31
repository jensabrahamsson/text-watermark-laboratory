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


@dataclass(frozen=True)
class NestedStemEval:
    n_marked_above: int
    n_unmarked_at_most: int
    n_marked: int
    n_unmarked: int
    sensitivity: float
    specificity: float
    mean_threshold: float
    n_stems: int
    source: str = "nested-youden-by-stem"


def nested_threshold_by_stem(
    stems: Sequence[str],
    marked_lrs: Sequence[float],
    unmarked_lrs: Sequence[float],
    *,
    fpr: float | None = None,
) -> NestedStemEval:
    """Leave-one-stem-out threshold on already-held-out file scores.

    For each stem, choose Youden (or a target FPR) on the *other* stems,
    then apply that threshold to this stem. Does not refit tables. Use this
    on leave-one-prompt-out LRs so the operating point is not chosen on the
    same prompt family being classified.
    """
    if len(stems) != len(marked_lrs) or len(stems) != len(unmarked_lrs):
        raise ValueError("stems and LRs must be aligned")
    by: dict[str, tuple[list[float], list[float]]] = {}
    for stem, marked, unmarked in zip(stems, marked_lrs, unmarked_lrs, strict=True):
        bucket = by.setdefault(stem, ([], []))
        bucket[0].append(marked)
        bucket[1].append(unmarked)
    names = list(by)
    source = (
        "nested-fpr10-by-stem" if fpr is not None else "nested-youden-by-stem"
    )
    if len(names) < 2:
        n_m = sum(len(v[0]) for v in by.values())
        n_u = sum(len(v[1]) for v in by.values())
        return NestedStemEval(
            n_marked_above=0,
            n_unmarked_at_most=0,
            n_marked=n_m,
            n_unmarked=n_u,
            sensitivity=float("nan"),
            specificity=float("nan"),
            mean_threshold=0.0,
            n_stems=len(names),
            source=source,
        )
    tp = tn = n_m = n_u = 0
    thresholds: list[float] = []
    for hold in names:
        pos: list[float] = []
        neg: list[float] = []
        for stem, (marked, unmarked) in by.items():
            if stem == hold:
                continue
            pos.extend(marked)
            neg.extend(unmarked)
        if fpr is not None:
            threshold = threshold_at_fpr(neg, fpr=fpr)
        else:
            threshold, _, _, _ = youden_threshold(pos, neg)
        thresholds.append(threshold)
        hold_m, hold_u = by[hold]
        above, at_most, _, _ = counts_at_threshold(hold_m, hold_u, threshold)
        tp += above
        tn += at_most
        n_m += len(hold_m)
        n_u += len(hold_u)
    return NestedStemEval(
        n_marked_above=tp,
        n_unmarked_at_most=tn,
        n_marked=n_m,
        n_unmarked=n_u,
        sensitivity=(tp / n_m) if n_m else float("nan"),
        specificity=(tn / n_u) if n_u else float("nan"),
        mean_threshold=(sum(thresholds) / len(thresholds)) if thresholds else 0.0,
        n_stems=len(names),
        source=source,
    )


def nested_stem_eval_to_dict(ev: NestedStemEval) -> dict:
    return {
        "n_marked_above": ev.n_marked_above,
        "n_unmarked_at_most": ev.n_unmarked_at_most,
        "n_marked": ev.n_marked,
        "n_unmarked": ev.n_unmarked,
        "sensitivity": ev.sensitivity,
        "specificity": ev.specificity,
        "mean_threshold": ev.mean_threshold,
        "n_stems": ev.n_stems,
        "source": ev.source,
    }


def counts_at_threshold(
    positive: Sequence[float],
    negative: Sequence[float],
    threshold: float,
) -> tuple[int, int, float, float]:
    """Return (n_pos > t, n_neg ≤ t, sensitivity, specificity)."""
    pos = list(positive)
    neg = list(negative)
    if not pos or not neg:
        return 0, 0, float("nan"), float("nan")
    tp = sum(1 for s in pos if s > threshold)
    tn = sum(1 for s in neg if s <= threshold)
    return tp, tn, tp / len(pos), tn / len(neg)


def threshold_at_fpr(
    negative: Sequence[float],
    *,
    fpr: float = 0.10,
) -> float:
    """Lowest threshold whose false-positive rate on `negative` is ≤ fpr.

    A score is called positive when it is strictly greater than the threshold.
    If even t = max(negative) still exceeds `fpr` (ties at the top), return that
    max. Empty input returns 0.
    """
    neg = list(negative)
    if not neg:
        return 0.0
    target_fp = fpr * len(neg)
    candidates = sorted({*neg, 0.0})
    chosen = candidates[-1]
    for t in candidates:
        fp = sum(1 for s in neg if s > t)
        if fp <= target_fp + 1e-12:
            return t
        chosen = t
    return chosen


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


def fit_ridge_logodds(
    X_pos,
    X_neg,
    *,
    ridge: float = 1.0,
    max_iter: int = 40,
):
    """Ridge logistic log-odds for marked (+) vs unmarked (−).

    Returns (weights, intercept, mean, std) so a later vector `x` scores as
    `((x - mean) / std) · weights + intercept`. Threshold 0 is a 50% logit.
    Z-scoring uses the pooled train rows. Still no keys / hash_iv / g-values.
    """
    import numpy as np

    pos = np.asarray(X_pos, dtype=np.float64)
    neg = np.asarray(X_neg, dtype=np.float64)
    if pos.ndim != 2 or neg.ndim != 2 or pos.shape[1] != neg.shape[1]:
        raise ValueError("fit_ridge_logodds needs 2-d arrays with the same width")
    if len(pos) < 1 or len(neg) < 1:
        raise ValueError("fit_ridge_logodds needs both classes")
    X = np.vstack([pos, neg])
    y = np.concatenate(
        [np.ones(len(pos), dtype=np.float64), np.zeros(len(neg), dtype=np.float64)]
    )
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    Z = (X - mu) / sd
    n, d = Z.shape
    Zb = np.column_stack([Z, np.ones(n)])
    w = np.zeros(d + 1, dtype=np.float64)
    penalty = ridge * np.eye(d + 1)
    penalty[-1, -1] = 0.0
    for _ in range(max_iter):
        logits = np.clip(Zb @ w, -40.0, 40.0)
        p = 1.0 / (1.0 + np.exp(-logits))
        weight = np.clip(p * (1.0 - p), 1e-6, None)
        hessian = Zb.T @ (weight[:, None] * Zb) + penalty
        grad = Zb.T @ (y - p) - penalty @ w
        try:
            step = np.linalg.solve(hessian, grad)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(hessian, grad, rcond=None)[0]
        w = w + step
        if float(np.max(np.abs(step))) < 1e-8:
            break
    return w[:-1], float(w[-1]), mu, sd


def score_ridge_logodds(x, weights, intercept, mean, std) -> float:
    import numpy as np

    vec = (np.asarray(x, dtype=np.float64) - mean) / std
    return float(vec @ weights + intercept)


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
