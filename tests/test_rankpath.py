"""Rank-path tables: unmarked-LM rank symbols, no token identity, no keys."""

import numpy as np

from text_watermark_tools.pivot import (
    cascade_score,
    cascade_source,
    fit_pivot,
    load_pivot,
    summarize_cascade,
)
from text_watermark_tools.probe import TransferRun, persist_transfer
from text_watermark_tools.rankpath import (
    RANK_PATH_KIND,
    RANKUNI_SPEC,
    fit_rankpath_from_symbols,
    load_rankpath,
    parse_cascade_fallback,
    persist_rankpath,
    rank_path_symbol,
    score_rankpath,
    symbols_from_matrix,
)


def test_rank_path_symbol_bins_near_ties() -> None:
    assert rank_path_symbol(1, 1.0, top_k=40) == 1
    assert rank_path_symbol(2, 1.0, top_k=40) == 2
    assert rank_path_symbol(3, 1.0, top_k=40) == 2
    assert rank_path_symbol(8, 1.0, top_k=40) == 3
    assert rank_path_symbol(20, 1.0, top_k=40) == 4
    assert rank_path_symbol(41, 0.0, top_k=40) == 0


def test_symbols_from_matrix_uses_rank_topk_column() -> None:
    # FEATURE_NAMES: logp, rank, rank_topk, in_topk, gap, entropy
    mat = np.array(
        [
            [0.0, 5.0, 1.0, 1.0, 0.0, 1.0],
            [0.0, 9.0, 2.0, 1.0, 0.5, 2.0],
            [0.0, 80.0, 41.0, 0.0, 3.0, 0.2],
        ],
        dtype=np.float64,
    )
    assert symbols_from_matrix(mat, top_k=40) == [1, 2, 0]


def test_rankuni_separates_near_tie_vs_argmax_without_keys() -> None:
    symbols = {
        ("p1", 1, "marked"): [2, 2, 2],
        ("p1", 1, "unmarked"): [1, 1, 1],
        ("p2", 1, "marked"): [2, 3, 2],
        ("p2", 1, "unmarked"): [1, 1, 1],
        ("p3", 1, "marked"): [2, 2, 3],
        ("p3", 1, "unmarked"): [1, 4, 1],
    }
    model = fit_rankpath_from_symbols(symbols, ["p1", "p2", "p3"], position_bucket=1)
    assert model.used_keys is False
    assert model.used_hash_iv is False
    assert model.used_g_values is False
    marked = score_rankpath([2, 2, 2], model, spec=RANKUNI_SPEC)
    unmarked = score_rankpath([1, 1, 1], model, spec=RANKUNI_SPEC)
    assert marked > 0.0
    assert unmarked < 0.0


def test_persist_load_rankpath_is_key_free(tmp_path) -> None:
    symbols = {
        ("p1", 1, "marked"): [2, 2],
        ("p1", 1, "unmarked"): [1, 1],
        ("p2", 1, "marked"): [2, 3],
        ("p2", 1, "unmarked"): [1, 1],
    }
    model = fit_rankpath_from_symbols(symbols, ["p1", "p2"])
    path = persist_rankpath(model, tmp_path, spec_name="rankuni")
    loaded, raw = load_rankpath(tmp_path)
    assert path.name == "tables.json"
    assert raw["kind"] == RANK_PATH_KIND
    assert raw["used_keys"] is False
    assert raw["alphabet"] == 5
    assert loaded.used_keys is False
    assert score_rankpath([2, 2], loaded, spec=RANKUNI_SPEC) == score_rankpath(
        [2, 2], model, spec=RANKUNI_SPEC
    )


def test_cascade_fallback_name_is_rankuni() -> None:
    assert cascade_source(2, "rankuni") == "count"
    assert cascade_source(0, "rankuni") == "rankuni"
    assert cascade_score(1.5, 0, -0.2) == -0.2
    assert parse_cascade_fallback("rankpath") == "rankpath"
    summary = summarize_cascade(
        [
            {"side": "marked", "source": "count", "score": 1.0, "stem": "a", "sample": 1},
            {
                "side": "marked",
                "source": "rankuni",
                "score": 0.4,
                "stem": "b",
                "sample": 1,
                "opening_text": "Now in the second",
            },
            {"side": "unmarked", "source": "count", "score": -1.0},
            {"side": "unmarked", "source": "rankuni", "score": -0.1},
        ]
    )
    assert summary["fallback"] == "rankuni"
    assert summary["n_fallback_marked"] == 1
    assert summary["n_pivot_marked"] == 1
    assert summary["combined_marked_above_zero"] == 2


def test_persist_transfer_writes_each_pivot_weight(tmp_path) -> None:
    rng = np.random.default_rng(2)
    fit_u = fit_pivot(rng.normal(1.0, 0.2, (20, 6)), rng.normal(-1.0, 0.2, (20, 6)))
    fit_e = fit_pivot(rng.normal(0.5, 0.2, (20, 6)), rng.normal(-0.5, 0.2, (20, 6)))
    run = TransferRun(
        pivot_weights=("uniform", "entropy"),
        pivot_fit=fit_e,
        pivot_fits={"uniform": fit_u, "entropy": fit_e},
        n_train_prompts=2,
        train_dir="train",
        test_dir="test",
    )
    persist_transfer(run, tmp_path)
    loaded_u, raw_u = load_pivot(tmp_path / "tables-pivot")
    loaded_named, raw_named = load_pivot(tmp_path / "tables-pivot-uniform")
    loaded_e, raw_e = load_pivot(tmp_path / "tables-pivot-entropy")
    assert raw_u["weight"] == "uniform"
    assert raw_named["weight"] == "uniform"
    assert raw_e["weight"] == "entropy"
    assert np.allclose(loaded_named.weights, fit_u.weights)
    assert np.allclose(loaded_u.weights, fit_u.weights)
    assert np.allclose(loaded_e.weights, fit_e.weights)
    assert not np.allclose(fit_u.weights, fit_e.weights)
