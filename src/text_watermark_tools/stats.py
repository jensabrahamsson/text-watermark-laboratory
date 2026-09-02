"""Key-free evaluation extras: AUC, permutation, binomial, Youden.

None of this consults watermark keys, hash_iv, or g-values. It only
summarises already-computed scores.
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Mapping, Sequence


FILE_LEVEL_INFERENCE_NOTE = (
    "File-level permutation_p and binomial_p_above_zero shuffle or test "
    "individual files. Draws are paired and clustered by prompt family; "
    "score 0 is not a calibrated null. Those p-values are descriptive, "
    "not valid clustered inference. Use permutation_prompt_sign_p on "
    "prompt-mean differences."
)

CLUSTERED_INFERENCE_NOTE = (
    "Prompt family is the intended independent unit. Leave-one-prompt-out "
    "tables share training mass across families, so the families are weakly "
    "dependent. permutation_prompt_sign_p, exact McNemar on discordant "
    "prompt signs, and Clopper–Pearson intervals on prompt-win counts are "
    "clustered descriptions of already-computed scores. They are not a "
    "second freeze, not a new scorer, and not a theorem. File-level "
    "binomial_p_above_zero remains descriptive. Independent binomial "
    "intervals on two paired windows are not a test of those windows."
)


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


def _binomial_sf_invert(k: int, n: int, target: float, *, iters: int = 80) -> float:
    """Invert binomial_sf(k, n, p) = target by bisection on p in [0, 1].

    binomial_sf increases in p. No scipy.
    """
    lo = 0.0
    hi = 1.0
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if binomial_sf(k, n, mid) > target:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def clopper_pearson(
    k: int, n: int, *, confidence: float = 0.95
) -> tuple[float, float]:
    """Exact Clopper–Pearson interval for a binomial proportion.

    Inverts binomial_sf. Lower solves P(X >= k | n, p) = α/2; upper
    solves P(X <= k | n, p) = α/2. k=0 pins lower at 0; k=n pins
    upper at 1. Not a theorem about watermarks. Cite Clopper and
    Pearson (1934).
    """
    if n <= 0:
        raise ValueError("n must be positive")
    k = int(k)
    n = int(n)
    if k < 0 or k > n:
        raise ValueError("k must satisfy 0 <= k <= n")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be in (0, 1)")
    alpha = 1.0 - confidence
    lo = 0.0 if k == 0 else _binomial_sf_invert(k, n, alpha / 2.0)
    hi = 1.0 if k == n else _binomial_sf_invert(k + 1, n, 1.0 - alpha / 2.0)
    return lo, hi


def mcnemar_exact_p(n_only_a: int, n_only_b: int) -> tuple[float, float]:
    """Exact binomial McNemar on discordant paired binary outcomes.

    one_sided is P(X >= n_only_a | Bin(n_only_a+n_only_b, 1/2)): the
    directed test that A wins more of the disagreements. two_sided is
    P(|X - n/2| >= |n_only_a - n/2|). Zero discordant pairs return
    (1, 1). Cite McNemar (1947).
    """
    b = int(n_only_a)
    c = int(n_only_b)
    if b < 0 or c < 0:
        raise ValueError("discordant counts must be non-negative")
    n = b + c
    if n == 0:
        return 1.0, 1.0
    one_sided = binomial_sf(b, n, 0.5)
    thresh = abs(b - n / 2.0)
    two_sided = 0.0
    half_n = 0.5**n
    for i in range(n + 1):
        if abs(i - n / 2.0) + 1e-15 >= thresh:
            two_sided += math.comb(n, i) * half_n
    return one_sided, min(1.0, two_sided)


def _sign_flip_mean_p(
    deltas: Sequence[float], *, n_perm: int, seed: int
) -> float:
    """One-sided sign-flip p on mean(deltas). Conservative +1/(n_perm+1)."""
    values = [float(x) for x in deltas]
    if not values or n_perm <= 0:
        return float("nan")
    observed = _mean(values)
    rng = random.Random(seed)
    count = 0
    n = len(values)
    for _ in range(n_perm):
        flipped = 0.0
        for delta in values:
            flipped += delta if rng.random() < 0.5 else -delta
        if flipped / n >= observed:
            count += 1
    return (count + 1) / (n_perm + 1)


def permutation_mean_diff_p(
    positive: Sequence[float],
    negative: Sequence[float],
    *,
    n_perm: int = 2000,
    seed: int = 0,
) -> float:
    """One-sided P(mean_pos - mean_neg as large as observed | shuffled labels).

    Adds one to numerator and denominator (conservative). This is a
    file-level label shuffle. It is **not** valid inference when files are
    paired by prompt or clustered in families of four draws. See
    permutation_prompt_sign_p.
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


def permutation_prompt_sign_p(
    stems: Sequence[str],
    marked: Sequence[float],
    unmarked: Sequence[float],
    *,
    n_perm: int = 2000,
    seed: int = 0,
) -> float:
    """One-sided sign-flip p-value on prompt-mean(marked − unmarked).

    The independent unit is the prompt family. For each stem, delta is
    mean(marked files) − mean(unmarked files). The statistic is the mean
    of those deltas. Under the null, randomly flip each stem's sign.
    Conservative +1 / (n_perm+1). Empty input returns nan.
    """
    if len(stems) != len(marked) or len(stems) != len(unmarked):
        raise ValueError("stems and LRs must be aligned")
    by: dict[str, tuple[list[float], list[float]]] = {}
    for stem, m, u in zip(stems, marked, unmarked, strict=True):
        bucket = by.setdefault(str(stem), ([], []))
        bucket[0].append(float(m))
        bucket[1].append(float(u))
    if not by or n_perm <= 0:
        return float("nan")
    deltas = [_mean(ms) - _mean(us) for ms, us in by.values()]
    return _sign_flip_mean_p(deltas, n_perm=n_perm, seed=seed)


def _prompt_family_win_delta(
    stems: Sequence[str],
    marked: Sequence[float],
    unmarked: Sequence[float],
) -> dict[str, tuple[bool, float]]:
    if len(stems) != len(marked) or len(stems) != len(unmarked):
        raise ValueError("stems and LRs must be aligned")
    by: dict[str, tuple[list[float], list[float]]] = {}
    for stem, m, u in zip(stems, marked, unmarked, strict=True):
        bucket = by.setdefault(str(stem), ([], []))
        bucket[0].append(float(m))
        bucket[1].append(float(u))
    out: dict[str, tuple[bool, float]] = {}
    for stem, (ms, us) in by.items():
        if not ms or not us:
            raise ValueError(f"stem {stem!r} is missing a marked or unmarked side")
        delta = _mean(ms) - _mean(us)
        out[stem] = (delta > 0.0, delta)
    return out


@dataclass(frozen=True)
class PairedPromptSignTable:
    n_stems: int
    both_win: int
    only_a: int
    only_b: int
    both_lose: int
    n_discordant: int
    mcnemar_one_sided_p: float
    mcnemar_two_sided_p: float
    n_a_gap_larger: int
    n_b_gap_larger: int
    n_gap_ties: int
    mean_gap_diff: float
    gap_sign_p: float
    note: str


def paired_prompt_sign_table(
    stems_a: Sequence[str],
    marked_a: Sequence[float],
    unmarked_a: Sequence[float],
    stems_b: Sequence[str],
    marked_b: Sequence[float],
    unmarked_b: Sequence[float],
    *,
    n_perm: int = 2000,
    seed: int = 0,
) -> PairedPromptSignTable:
    """Paired prompt-family 2×2 of ranking wins, plus delta-gap signs.

    Win is mean(marked) > mean(unmarked), the frozen strict-`>` ranking
    endpoint. McNemar is exact binomial on the discordant cells, directed
    at A. gap_sign_p is a sign-flip on mean(delta_a − delta_b), the same
    conservative +1/(n_perm+1) as permutation_prompt_sign_p. Leave-one-
    prompt-out tables induce weak dependence; see CLUSTERED_INFERENCE_NOTE.
    """
    left = _prompt_family_win_delta(stems_a, marked_a, unmarked_a)
    right = _prompt_family_win_delta(stems_b, marked_b, unmarked_b)
    if set(left) != set(right):
        raise ValueError("paired tables must cover the same prompt families")
    both_win = only_a = only_b = both_lose = 0
    n_a_gap = n_b_gap = n_gap_ties = 0
    gap_diffs: list[float] = []
    for stem in sorted(left):
        win_a, delta_a = left[stem]
        win_b, delta_b = right[stem]
        if win_a and win_b:
            both_win += 1
        elif win_a and not win_b:
            only_a += 1
        elif (not win_a) and win_b:
            only_b += 1
        else:
            both_lose += 1
        gap = delta_a - delta_b
        gap_diffs.append(gap)
        if gap > 0.0:
            n_a_gap += 1
        elif gap < 0.0:
            n_b_gap += 1
        else:
            n_gap_ties += 1
    one_sided, two_sided = mcnemar_exact_p(only_a, only_b)
    return PairedPromptSignTable(
        n_stems=len(left),
        both_win=both_win,
        only_a=only_a,
        only_b=only_b,
        both_lose=both_lose,
        n_discordant=only_a + only_b,
        mcnemar_one_sided_p=one_sided,
        mcnemar_two_sided_p=two_sided,
        n_a_gap_larger=n_a_gap,
        n_b_gap_larger=n_b_gap,
        n_gap_ties=n_gap_ties,
        mean_gap_diff=_mean(gap_diffs),
        gap_sign_p=_sign_flip_mean_p(gap_diffs, n_perm=n_perm, seed=seed),
        note=CLUSTERED_INFERENCE_NOTE,
    )


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

    For each stem H, choose Youden (or a target FPR) on the *other* stems'
    already-OOF LRs, then apply that threshold to H. This is nested on the
    operating point only. It does not refit tables without H: those other
    OOF scores were still produced by models that trained on H. True nested
    CV would refit when choosing H's threshold. t=0, AUC, and prompt
    ranking do not use this helper.
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
        f"perm_p={ev.permutation_p:.4g} (file-level, descriptive) "
        f"binom_p={ev.binomial_p_above_zero:.4g} (file-level, descriptive) "
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


@dataclass(frozen=True)
class CoverageGate:
    """Treat lr==0 as abstain (no shared last-k, or no observed next token).

    Hits/poshits can still assign a non-zero LR to an *unseen* next token
    after a shared context (Laplace occupancy). tokhits skips those.
    tokbackoff shrinks last-k until an observed next token hits. Zeros
    are not counted as sign errors.
    """

    n_marked: int
    n_unmarked: int
    n_marked_zero: int
    n_unmarked_zero: int
    n_marked_decided: int
    n_unmarked_decided: int
    decided_tp: int
    decided_fn: int
    decided_fp: int
    decided_tn: int
    precision: float
    decided_accuracy: float
    recall_including_zeros: float


def coverage_gate(
    marked: Sequence[float],
    unmarked: Sequence[float],
    *,
    eps: float = 1e-15,
    marked_used: Sequence[int] | None = None,
    unmarked_used: Sequence[int] | None = None,
) -> CoverageGate:
    def is_zero(i: int, x: float, used: Sequence[int] | None) -> bool:
        if used is not None:
            return int(used[i]) == 0
        return abs(float(x)) <= eps

    marked_l = [float(x) for x in marked]
    unmarked_l = [float(x) for x in unmarked]
    mz = sum(1 for i, x in enumerate(marked_l) if is_zero(i, x, marked_used))
    uz = sum(1 for i, x in enumerate(unmarked_l) if is_zero(i, x, unmarked_used))
    m_dec = [x for i, x in enumerate(marked_l) if not is_zero(i, x, marked_used)]
    u_dec = [x for i, x in enumerate(unmarked_l) if not is_zero(i, x, unmarked_used)]
    tp = sum(1 for x in m_dec if x > 0)
    fn = sum(1 for x in m_dec if x <= 0)
    fp = sum(1 for x in u_dec if x > 0)
    tn = sum(1 for x in u_dec if x <= 0)
    decided = tp + fn + fp + tn
    prec = (tp / (tp + fp)) if (tp + fp) else float("nan")
    acc = ((tp + tn) / decided) if decided else float("nan")
    rec = (tp / len(marked_l)) if marked_l else float("nan")
    return CoverageGate(
        n_marked=len(marked_l),
        n_unmarked=len(unmarked_l),
        n_marked_zero=mz,
        n_unmarked_zero=uz,
        n_marked_decided=len(m_dec),
        n_unmarked_decided=len(u_dec),
        decided_tp=tp,
        decided_fn=fn,
        decided_fp=fp,
        decided_tn=tn,
        precision=prec,
        decided_accuracy=acc,
        recall_including_zeros=rec,
    )


def coverage_gate_to_dict(ev: CoverageGate) -> dict:
    return {
        "n_marked": ev.n_marked,
        "n_unmarked": ev.n_unmarked,
        "n_marked_zero": ev.n_marked_zero,
        "n_unmarked_zero": ev.n_unmarked_zero,
        "n_marked_decided": ev.n_marked_decided,
        "n_unmarked_decided": ev.n_unmarked_decided,
        "decided_tp": ev.decided_tp,
        "decided_fn": ev.decided_fn,
        "decided_fp": ev.decided_fp,
        "decided_tn": ev.decided_tn,
        "precision": ev.precision,
        "decided_accuracy": ev.decided_accuracy,
        "recall_including_zeros": ev.recall_including_zeros,
    }


def format_coverage_gate(ev: CoverageGate, *, label: str = "") -> str:
    prefix = f"{label} " if label else ""
    return (
        f"{prefix}zeros={ev.n_marked_zero}/{ev.n_marked} vs "
        f"{ev.n_unmarked_zero}/{ev.n_unmarked} "
        f"decided_tp={ev.decided_tp} fn={ev.decided_fn} "
        f"fp={ev.decided_fp} tn={ev.decided_tn} "
        f"precision={ev.precision:.3f} decided_acc={ev.decided_accuracy:.3f}"
    )


def stem_transfer_rows(
    files: Sequence[Mapping[str, object]],
    nested_threshold: float,
) -> list[dict]:
    """Group already-saved holdout file LRs by stem.

    Prompt win is mean marked LR > mean unmarked LR. ``marked_t0`` is
    hard ``lr > 0``. ``marked_nested`` uses the train-LOO Youden
    threshold passed in. Not a new scorer. Does not consult keys.
    """
    by: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: {"marked": [], "unmarked": []}
    )
    for row in files:
        stem = str(row["stem"])
        lr = float(row["lr"])
        name = str(row["file"])
        side = "unmarked" if "unmarked" in name else "marked"
        by[stem][side].append(lr)
    rows: list[dict] = []
    for stem in sorted(by):
        marked = by[stem]["marked"]
        unmarked = by[stem]["unmarked"]
        if not marked or not unmarked:
            raise ValueError(f"stem {stem!r} is missing a marked or unmarked side")
        mean_marked = _mean(marked)
        mean_unmarked = _mean(unmarked)
        rows.append(
            {
                "stem": stem,
                "prompt_win": mean_marked > mean_unmarked,
                "mean_marked": mean_marked,
                "mean_unmarked": mean_unmarked,
                "mean_diff": mean_marked - mean_unmarked,
                "marked_t0": sum(1 for x in marked if x > 0.0),
                "marked_nested": sum(1 for x in marked if x > nested_threshold),
                "n": len(marked),
            }
        )
    return rows


def stem_prompt_losses(rows: Sequence[Mapping[str, object]]) -> list[str]:
    """Stems whose marked mean LR does not beat unmarked mean LR."""
    return [str(r["stem"]) for r in rows if not r["prompt_win"]]


def stem_ranking_without_isolated_tp(
    rows: Sequence[Mapping[str, object]],
) -> list[str]:
    """Prompt-ranking wins with no marked file above 0.

    Those stems rank because unmarked LRs are more negative, not because
    any isolated marked file signs. Do not read prompt wins as isolated
    recall.
    """
    return [
        str(r["stem"])
        for r in rows
        if r["prompt_win"] and int(r["marked_t0"]) == 0
    ]


def stem_ranking_losses_with_isolated_tp(
    rows: Sequence[Mapping[str, object]],
) -> list[str]:
    """Prompt-ranking losses that still have a marked file above 0."""
    return [
        str(r["stem"])
        for r in rows
        if (not r["prompt_win"]) and int(r["marked_t0"]) > 0
    ]


def stem_marked_positive_on_ranking_losses(
    rows: Sequence[Mapping[str, object]],
) -> int:
    """Isolated ``lr>0`` count sitting on prompt-ranking losses."""
    return sum(int(r["marked_t0"]) for r in rows if not r["prompt_win"])


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
        "permutation_p_note": FILE_LEVEL_INFERENCE_NOTE,
        "binomial_p_note": FILE_LEVEL_INFERENCE_NOTE,
        "youden_threshold": ev.youden_threshold,
        "youden_sensitivity": ev.youden_sensitivity,
        "youden_specificity": ev.youden_specificity,
        "youden_j": ev.youden_j,
        "n_perm": ev.n_perm,
    }
