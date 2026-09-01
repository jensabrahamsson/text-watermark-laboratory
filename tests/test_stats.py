"""AUC, permutation, and binomial helpers for key-free scores."""

from text_watermark_tools.stats import (
    binary_eval,
    binomial_sf,
    counts_at_threshold,
    fit_ridge_logodds,
    nested_threshold_by_stem,
    permutation_mean_diff_p,
    roc_auc,
    score_ridge_logodds,
    threshold_at_fpr,
    youden_threshold,
)


def test_auc_is_one_when_perfectly_separated() -> None:
    assert roc_auc([1.0, 2.0, 3.0], [-2.0, -1.0, 0.0]) == 1.0


def test_auc_is_half_on_identical_lists() -> None:
    xs = [0.0, 1.0, 0.2, -0.3]
    assert roc_auc(xs, xs) == 0.5


def test_auc_handles_ties() -> None:
    # 1 vs 1 (tie), 1 vs -1 (win), 0 vs 1 (loss), 0 vs -1 (win) → 2.5/4
    assert roc_auc([1.0, 0.0], [1.0, -1.0]) == 0.625


def test_binomial_ten_of_twelve_is_below_five_percent() -> None:
    p = binomial_sf(10, 12, 0.5)
    assert 0.01 < p < 0.05
    assert binomial_sf(6, 12, 0.5) > 0.3


def test_permutation_p_is_small_when_means_differ() -> None:
    p = permutation_mean_diff_p(
        [1.0, 1.1, 0.9, 1.2],
        [0.0, -0.1, 0.05, -0.2],
        n_perm=500,
        seed=0,
    )
    assert p < 0.02


def test_permutation_p_is_large_when_labels_are_noise() -> None:
    p = permutation_mean_diff_p(
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 0.0, 1.0, 0.0],
        n_perm=400,
        seed=1,
    )
    assert p > 0.2


def test_youden_picks_a_separating_threshold() -> None:
    t, sens, spec, j = youden_threshold([1.0, 2.0, 3.0], [-1.0, 0.0, 0.5])
    assert j == 1.0
    assert sens == 1.0
    assert spec == 1.0
    assert t >= 0.5


def test_counts_at_threshold_matches_youden_zero() -> None:
    pos = [0.2, -0.1, 0.4]
    neg = [0.3, -0.2, -0.5]
    tp, tn, sens, spec = counts_at_threshold(pos, neg, 0.0)
    assert tp == 2
    assert tn == 2
    assert abs(sens - 2 / 3) < 1e-12
    assert abs(spec - 2 / 3) < 1e-12


def test_nested_youden_by_stem_classifies_without_the_held_stem() -> None:
    # One loud stem plus two quiet stems. Nested Youden must still separate
    # the quiet files using a threshold fitted without the loud stem.
    stems = ["loud", "loud", "q1", "q1", "q2", "q2"]
    marked = [10.0, 10.0, 0.2, 0.3, 0.25, 0.15]
    unmarked = [-10.0, -10.0, -0.2, -0.1, -0.15, -0.05]
    ev = nested_threshold_by_stem(stems, marked, unmarked)
    assert ev.n_stems == 3
    assert ev.n_marked_above == 6
    assert ev.n_unmarked_at_most == 6
    assert ev.source == "nested-youden-by-stem"
    assert "does not refit tables without H" in nested_threshold_by_stem.__doc__


def test_nested_threshold_by_stem_rejects_misaligned_inputs() -> None:
    try:
        nested_threshold_by_stem(["a"], [0.1, 0.2], [0.0])
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_threshold_at_fpr_ten_percent_on_ten_unmarked() -> None:
    neg = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    t = threshold_at_fpr(neg, fpr=0.10)
    fp = sum(1 for s in neg if s > t)
    assert fp <= 1
    assert t >= 0.7


def test_ridge_logodds_separates_two_features() -> None:
    pos = [[2.0, 1.0], [1.8, 1.2], [2.2, 0.9], [1.9, 1.1]]
    neg = [[0.0, 0.0], [0.2, -0.1], [-0.1, 0.1], [0.1, 0.0]]
    w, b, mu, sd = fit_ridge_logodds(pos, neg, ridge=1.0)
    assert score_ridge_logodds(pos[0], w, b, mu, sd) > 0.0
    assert score_ridge_logodds(neg[0], w, b, mu, sd) < 0.0


def test_binary_eval_at_zero_matches_sign_counts() -> None:
    ev = binary_eval([0.2, -0.1, 0.4], [0.3, -0.2, -0.5], n_perm=200, seed=0)
    assert ev.n_positive_above_zero == 2
    assert ev.n_negative_at_most_zero == 2
    assert ev.auc > 0.5
    assert ev.n_perm == 200
    assert ev.auc > 0.5
