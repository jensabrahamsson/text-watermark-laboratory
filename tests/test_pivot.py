"""Unmarked-LM choice geometry and argmax snap, without watermark keys."""

import numpy as np
import torch

from text_watermark_tools.pivot import (
    choice_matrix_from_logits,
    fit_pivot,
    score_pivot_lda,
    snap_to_unmarked_argmax,
)
from text_watermark_tools.stats import roc_auc


def test_choice_matrix_ranks_the_argmax_first() -> None:
    logits = torch.tensor([[0.0, 5.0, 1.0, -1.0], [2.0, 0.0, 3.0, 0.0]])
    # tokens: prefix 0, then 1 (row0 argmax), then 2 (row1 argmax)
    mat = choice_matrix_from_logits(logits, [0, 1, 2], top_k=3)
    assert mat.shape == (2, 6)
    assert mat[0, 1] == 1.0  # full rank
    assert mat[0, 2] == 1.0  # rank in top-k
    assert mat[0, 3] == 1.0  # in top-k
    assert mat[0, 4] == 0.0  # gap to argmax


def test_lda_separates_shifted_gaussians_without_keys() -> None:
    rng = np.random.default_rng(0)
    x_pos = rng.normal(1.0, 0.15, size=(50, 6))
    x_neg = rng.normal(-1.0, 0.15, size=(50, 6))
    fit = fit_pivot(x_pos, x_neg)
    assert fit.used_keys is False
    assert fit.used_hash_iv is False
    assert fit.used_g_values is False
    pos = [score_pivot_lda(x, fit) for x in x_pos]
    neg = [score_pivot_lda(x, fit) for x in x_neg]
    assert roc_auc(pos, neg) == 1.0
    assert min(pos) > max(neg)


def test_snap_replaces_non_argmax_inside_top_k() -> None:
    logits = torch.zeros(2, 8)
    logits[0, 3] = 5.0
    logits[0, 1] = 1.0
    logits[1, 2] = 5.0
    ids, n_flips = snap_to_unmarked_argmax([0, 1, 2], logits, top_k=4)
    assert ids[0] == 0
    assert ids[1] == 3
    assert ids[2] == 2
    assert n_flips == 1
