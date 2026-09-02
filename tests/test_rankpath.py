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


def test_opening_matrix_end_skips_generated_token_zero() -> None:
    from text_watermark_tools.rankpath import opening_matrix_end

    assert opening_matrix_end(None, False) is None
    assert opening_matrix_end(4, False) == 3
    assert opening_matrix_end(4, True) == 4
    assert opening_matrix_end(1, False) == 0


def test_slice_matrices_is_half_open_rows() -> None:
    from text_watermark_tools.rankpath import slice_matrices, slice_symbols

    mat = np.arange(24, dtype=np.float64).reshape(4, 6)
    sliced = slice_matrices({("a", 1, "marked"): mat}, 1, 3)
    assert sliced[("a", 1, "marked")].shape == (2, 6)
    assert sliced[("a", 1, "marked")][0, 0] == 6.0
    assert slice_symbols({("a", 1, "marked"): [1, 2, 3, 4]}, 1, 3)[("a", 1, "marked")] == [
        2,
        3,
    ]


def _choice_row(rank_topk: int, in_topk: float = 1.0) -> list[float]:
    return [0.0, float(rank_topk), float(rank_topk), float(in_topk), 0.0, 1.0]


def test_rotate_rankpath_matched_window_finds_late_signal() -> None:
    from text_watermark_tools.blind import Twin
    from text_watermark_tools.probe import rotate_rankpath

    early = [_choice_row(1)] * 16
    late_m = [_choice_row(2)] * 8
    late_u = [_choice_row(1)] * 8
    mat_m = np.array(early + late_m, dtype=np.float64)
    mat_u = np.array(early + late_u, dtype=np.float64)
    mats = {}
    twins = []
    for stem in ("a", "b", "c"):
        twins.append(Twin(stem, "m", "u", [0, 1], [0, 1]))
        mats[(stem, 1, "marked")] = mat_m.copy()
        mats[(stem, 1, "unmarked")] = mat_u.copy()
    prefix_out: dict = {}
    window_out: dict = {}
    rotate_rankpath(
        twins,
        methods=("rankuni",),
        mats=mats,
        position_bucket=0,
        prefix_lens=(4,),
        prefix_out=prefix_out,
        windows=((16, 24),),
        window_out=window_out,
    )
    pref = prefix_out[4]["rankuni"]
    win = window_out[(16, 24)]["rankuni"]
    assert pref.used_keys is False
    assert win.n_prompts_marked_above == 3
    assert pref.n_prompts_marked_above <= win.n_prompts_marked_above
    assert min(win.marked_lrs) > max(win.unmarked_lrs)
