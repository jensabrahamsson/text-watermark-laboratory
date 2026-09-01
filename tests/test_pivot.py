"""Unmarked-LM choice geometry and argmax snap, without watermark keys."""

import numpy as np
import torch

from text_watermark_tools.pivot import (
    aggregate_choice_matrix,
    cascade_score,
    cascade_source,
    choice_matrix_from_logits,
    fit_pivot,
    generated_logits,
    load_pivot,
    parse_pivot_weights,
    persist_pivot,
    pivot_method_name,
    rebind_cascade_rows,
    score_pivot_lda,
    snap_to_unmarked_argmax,
    summarize_cascade,
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


class _TinyLM(torch.nn.Module):
    def __init__(self, vocab: int = 4) -> None:
        super().__init__()
        self.config = type("C", (), {"vocab_size": vocab})()
        self._p = torch.nn.Parameter(torch.zeros(1))

    def forward(self, input_ids):
        b, t = input_ids.shape
        logits = torch.zeros(b, t, int(self.config.vocab_size))
        logits[:, :, 2] = 5.0
        return type("O", (), {"logits": logits})()


def test_prompt_prefix_scores_generated_token_zero() -> None:
    model = _TinyLM()
    rows, chosen = generated_logits([3], model, prefix=[0, 1])
    assert chosen == [3]
    assert rows.shape[0] == 1
    skipped, rest = generated_logits([3, 2], model, prefix=())
    assert rest == [2]
    assert skipped.shape[0] == 1


def test_entropy_weighting_prefers_uncertain_rows() -> None:
    mat = np.array(
        [
            [1.0, 0.0, 0.0, 1.0, 0.0, 0.1],
            [9.0, 0.0, 0.0, 1.0, 0.0, 10.0],
        ],
        dtype=np.float64,
    )
    uniform = aggregate_choice_matrix(mat, weight="uniform")
    entropy = aggregate_choice_matrix(mat, weight="entropy")
    assert abs(uniform[0] - 5.0) < 1e-12
    assert entropy[0] > 8.0
    masked = np.array(
        [
            [1.0, 0.0, 0.0, 0.0, 0.0, 4.0],
            [3.0, 0.0, 0.0, 1.0, 0.0, 4.0],
        ],
        dtype=np.float64,
    )
    assert aggregate_choice_matrix(masked, weight="in_topk")[0] == 3.0


def test_cascade_uses_count_only_when_covered() -> None:
    assert cascade_source(2) == "count"
    assert cascade_source(0) == "pivot"
    assert cascade_score(1.5, 2, -9.0) == 1.5
    assert cascade_score(1.5, 0, -9.0) == -9.0
    assert cascade_source(1, "rankpath", count_lr=-2.7, when="positive") == "rankpath"
    assert cascade_score(-2.7, 1, 0.4, when="positive") == 0.4
    assert cascade_score(1.2, 1, 0.4, when="positive") == 1.2
    summary = summarize_cascade(
        [
            {
                "side": "marked",
                "source": "count",
                "score": 1.0,
                "stem": "a",
                "sample": 1,
            },
            {
                "side": "marked",
                "source": "pivot",
                "score": -0.2,
                "stem": "b",
                "sample": 1,
                "opening_text": "Now in the second",
            },
            {"side": "unmarked", "source": "count", "score": -1.0},
            {"side": "unmarked", "source": "pivot", "score": 0.4},
        ]
    )
    assert summary["used_keys"] is False
    assert summary["n_count_marked"] == 1
    assert summary["n_pivot_marked"] == 1
    assert summary["combined_marked_above_zero"] == 1
    assert summary["pivot_marked_above_zero"] == 0
    assert summary["pivot_fallback_marked"][0]["opening_text"] == "Now in the second"
    assert summary["fallback_fpr10"] is not None
    assert summary["combined_at_fallback_fpr10"]["n_marked"] == 2
    assert summary["combined_at_fallback_youden"]["n_unmarked"] == 2


def test_rebind_cascade_rows_switches_covered_negatives_to_fallback() -> None:
    rows = [
        {
            "side": "marked",
            "n_used": 1,
            "count_lr": -2.0,
            "pivot_lr": 0.5,
            "source": "count",
            "score": -2.0,
            "stem": "harbour",
            "sample": 1,
            "opening_text": "The ferry was so",
        },
        {
            "side": "unmarked",
            "n_used": 1,
            "count_lr": -1.0,
            "pivot_lr": -0.2,
            "source": "count",
            "score": -1.0,
        },
    ]
    rebound = rebind_cascade_rows(rows, when="positive", fallback="rankpath")
    assert rebound[0]["source"] == "rankpath"
    assert rebound[0]["score"] == 0.5
    summary = summarize_cascade(rebound, when="positive")
    assert summary["combined_marked_above_zero"] == 1
    assert summary["n_count_marked"] == 0


def test_format_cascade_does_not_dump_raw_rows() -> None:
    from text_watermark_tools.probe import format_cascade

    lines = format_cascade(
        {
            "fallback": "rankuni",
            "count_method": "postokbackoff",
            "pivot_weight": "uniform",
            "prompt_context": False,
            "used_keys": False,
            "n_marked": 2,
            "n_unmarked": 2,
            "n_count_marked": 1,
            "n_count_unmarked": 1,
            "n_pivot_marked": 1,
            "n_pivot_unmarked": 1,
            "count_marked_above_zero": 1,
            "count_unmarked_at_most_zero": 1,
            "pivot_marked_above_zero": 1,
            "pivot_unmarked_at_most_zero": 1,
            "combined_marked_above_zero": 2,
            "combined_unmarked_at_most_zero": 2,
            "count_precision": 1.0,
            "pivot_fallback_marked": [
                {
                    "stem": "b",
                    "sample": 1,
                    "score": 0.4,
                    "opening_text": "Now in the second",
                }
            ],
        }
    )
    joined = "\n".join(lines)
    assert "rankuni-fallback marked files:" in joined
    assert "[{'stem'" not in joined
    assert "`b` draw 1: Now in the second lr>0=0.4000" in joined


def test_persist_load_pivot_is_key_free(tmp_path) -> None:
    rng = np.random.default_rng(1)
    fit = fit_pivot(rng.normal(1.0, 0.2, (20, 6)), rng.normal(-1.0, 0.2, (20, 6)))
    path = persist_pivot(fit, tmp_path, weight="entropy", prompt_context=False)
    loaded, raw = load_pivot(tmp_path)
    assert path.name == "tables.json"
    assert raw["kind"] == "key-free-pivot"
    assert raw["used_keys"] is False
    assert raw["weight"] == "entropy"
    assert loaded.used_keys is False
    assert np.allclose(loaded.weights, fit.weights)
    assert parse_pivot_weights("entropy,uniform") == ("entropy", "uniform")
    assert pivot_method_name("lda", "entropy") == "pivot-lda-entropy"
    assert pivot_method_name("lda", "uniform") == "pivot-lda"
