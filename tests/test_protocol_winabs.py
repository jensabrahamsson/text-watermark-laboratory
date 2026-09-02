"""Absolute-history OOD interpolate windows, frozen before window LRs."""

import json
from pathlib import Path

from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-windows-absolute.md"
TRAIN = ROOT / "experiments" / "2026-09-01-pair-100x4"
GROK = ROOT / "experiments" / "2026-09-01-pair-grok12x4"
ORIG = ROOT / "experiments" / "2026-08-17-pair-12x4"
REINDEXED_GROK = (
    ROOT / "experiments" / "2026-09-01-transfer-100x4-to-grok12x4-hard-windows"
)
REINDEXED_ORIG = (
    ROOT / "experiments" / "2026-09-01-transfer-100x4-to-12x4-hard-windows"
)
ABSOLUTE_GROK = (
    ROOT
    / "experiments"
    / "2026-09-02-transfer-100x4-to-grok12x4-hard-windows-absolute"
)
ABSOLUTE_ORIG = (
    ROOT
    / "experiments"
    / "2026-09-02-transfer-100x4-to-12x4-hard-windows-absolute"
)


def _windows(raw: dict) -> dict[tuple[int, int], dict]:
    return {(int(w["start"]), int(w["end"])): w for w in raw["window_scores"]}


def test_protocol_winabs_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-win-abs-open" in text
    assert "H-win-abs-mid" in text
    assert "H-win-abs-12" in text
    assert "H-win-abs-iso" in text
    assert "2026-09-01-pair-100x4" in text
    assert "2026-09-01-pair-grok12x4" in text
    assert "2026-08-17-pair-12x4" in text
    assert "2026-09-01-transfer-100x4-to-grok12x4-hard-windows" in text
    assert "2026-09-01-transfer-100x4-to-12x4-hard-windows" in text
    assert "2026-09-02-transfer-100x4-to-grok12x4-hard-windows-absolute" in text
    assert "2026-09-02-transfer-100x4-to-12x4-hard-windows-absolute" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--windows 0:4,4:16,16:32,32:64,64:128" in text
    assert "score_span" in text
    assert "Do **not** overwrite" in text or "Do not overwrite" in text
    assert "Do **not** mix grok12" in text
    assert "thesis/" in text
    assert "leftover-15" in text
    assert "PROTOCOL-isolated-windows.md" in text
    assert "PROTOCOL-h2-absolute" in text
    assert "PROTOCOL-isolated-xkey" in text
    assert "PROTOCOL-isolated-mask" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    assert "H-win-abs-open **holds**" in text
    assert "H-win-abs-mid **holds**" in text
    assert "H-win-abs-12 **holds**" in text
    assert "H-win-abs-iso **holds**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "`1504cb4`" in log
    assert "`b32ea50`" in log
    assert TRAIN.is_dir()
    assert GROK.is_dir()
    assert ORIG.is_dir()
    assert REINDEXED_GROK.is_dir()
    assert REINDEXED_ORIG.is_dir()
    assert (ABSOLUTE_GROK / "results.json").is_file()
    assert (ABSOLUTE_ORIG / "results.json").is_file()


def test_winabs_keeps_reindexed_dumps() -> None:
    text = PROTOCOL.read_text()
    assert "Do **not** overwrite" in text or "Do not overwrite" in text
    grok = json.loads((REINDEXED_GROK / "results.json").read_text())
    orig = json.loads((REINDEXED_ORIG / "results.json").read_text())
    gw = _windows(grok)
    ow = _windows(orig)
    assert grok["used_keys"] is False
    assert orig["used_keys"] is False
    assert gw[(0, 4)]["n_prompt_wins"] == 7
    assert gw[(32, 64)]["n_prompt_wins"] == 9
    assert gw[(64, 128)]["n_prompt_wins"] == 9
    assert ow[(0, 4)]["n_prompt_wins"] == 9
    assert ow[(16, 32)]["n_prompt_wins"] == 6
    assert (REINDEXED_GROK / "window-0-4" / "interpolate" / "holdout.json").is_file()
    assert (REINDEXED_ORIG / "window-16-32" / "interpolate" / "holdout.json").is_file()


def test_winabs_grok_opening_equals_reindexed_and_tail_still_ranks() -> None:
    raw = json.loads((ABSOLUTE_GROK / "results.json").read_text())
    wins = _windows(raw)
    reindexed = _windows(json.loads((REINDEXED_GROK / "results.json").read_text()))
    assert raw["used_keys"] is False
    assert raw["used_hash_iv"] is False
    assert raw["used_g_values"] is False
    assert raw["train_dir"] == "experiments/2026-09-01-pair-100x4"
    assert raw["test_dir"] == "experiments/2026-09-01-pair-grok12x4"
    assert raw["windows"] == ["0:4", "4:16", "16:32", "32:64", "64:128"]
    assert wins[(0, 4)]["n_prompt_wins"] == 7
    assert wins[(0, 4)]["n_prompt_ties"] == 0
    assert wins[(0, 4)]["n_prompt_wins"] == reindexed[(0, 4)]["n_prompt_wins"]
    assert wins[(0, 4)]["n_prompt_wins"] < 11
    assert wins[(32, 64)]["n_prompt_wins"] == 10
    assert wins[(32, 64)]["n_prompt_wins"] > reindexed[(32, 64)]["n_prompt_wins"]
    assert wins[(64, 128)]["n_prompt_wins"] == 9
    assert wins[(64, 128)]["n_prompt_wins"] == reindexed[(64, 128)]["n_prompt_wins"]
    assert wins[(16, 32)]["n_prompt_wins"] == 7
    assert wins[(16, 32)]["n_prompt_wins"] < reindexed[(16, 32)]["n_prompt_wins"]
    assert wins[(32, 64)]["n_prompt_wins"] > 6
    assert abs(wins[(0, 4)]["binary"]["auc"] - 0.619) < 0.001
    assert abs(wins[(32, 64)]["binary"]["auc"] - 0.658) < 0.001
    assert wins[(0, 4)]["binary"]["n_positive_above_zero"] == 23
    assert wins[(0, 4)]["binary"]["n_negative_at_most_zero"] == 31
    early = holdout_from_json(ABSOLUTE_GROK / "window-0-4" / "interpolate" / "holdout.json")
    mid = holdout_from_json(ABSOLUTE_GROK / "window-32-64" / "interpolate" / "holdout.json")
    assert early.used_keys is False
    assert mid.used_keys is False
    assert early.n_prompts_marked_above == 7
    assert mid.n_prompts_marked_above == 10
    text = PROTOCOL.read_text()
    assert "H-win-abs-open **holds**" in text
    assert "H-win-abs-mid **holds**" in text
    assert "rose" in text
    assert "Do **not** sell tail **10/12**" in text or "Do not sell tail **10/12**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "absolute-history OOD windows remasure opened" in log


def test_winabs_original_12_opening_outranks_midfile() -> None:
    raw = json.loads((ABSOLUTE_ORIG / "results.json").read_text())
    wins = _windows(raw)
    reindexed = _windows(json.loads((REINDEXED_ORIG / "results.json").read_text()))
    assert raw["used_keys"] is False
    assert raw["test_dir"] == "experiments/2026-08-17-pair-12x4"
    assert wins[(0, 4)]["n_prompt_wins"] == 9
    assert wins[(0, 4)]["n_prompt_ties"] == 0
    assert wins[(0, 4)]["n_prompt_wins"] == reindexed[(0, 4)]["n_prompt_wins"]
    assert wins[(16, 32)]["n_prompt_wins"] == 6
    assert wins[(0, 4)]["n_prompt_wins"] >= wins[(16, 32)]["n_prompt_wins"]
    assert wins[(64, 128)]["n_prompt_wins"] == 6
    assert wins[(64, 128)]["n_prompt_wins"] < reindexed[(64, 128)]["n_prompt_wins"]
    assert abs(wins[(0, 4)]["binary"]["auc"] - 0.636) < 0.001
    assert abs(wins[(16, 32)]["binary"]["auc"] - 0.576) < 0.001
    assert wins[(0, 4)]["binary"]["n_positive_above_zero"] == 25
    assert wins[(0, 4)]["binary"]["n_negative_at_most_zero"] == 31
    early = holdout_from_json(ABSOLUTE_ORIG / "window-0-4" / "interpolate" / "holdout.json")
    mid = holdout_from_json(ABSOLUTE_ORIG / "window-16-32" / "interpolate" / "holdout.json")
    assert early.n_prompts_marked_above == 9
    assert mid.n_prompts_marked_above == 6
    text = PROTOCOL.read_text()
    assert "H-win-abs-12 **holds**" in text
    assert "H-win-abs-iso **holds**" in text
    assert "Do not sell absolute 32:64 **10/12**" in text


def test_winabs_isolated_grain_stays_chance() -> None:
    grok_lo, grok_hi = clopper_pearson(7, 12)
    ten_lo, ten_hi = clopper_pearson(10, 12)
    nine_lo, nine_hi = clopper_pearson(9, 12)
    iso_lo, iso_hi = clopper_pearson(25, 48)
    t0_lo, t0_hi = clopper_pearson(23, 48)
    assert grok_lo <= 0.5 <= grok_hi
    assert ten_lo > 0.5
    assert not (ten_lo <= 0.5 <= ten_hi)
    assert nine_lo <= 0.5 <= nine_hi
    assert iso_lo <= 0.5 <= iso_hi
    assert t0_lo <= 0.5 <= t0_hi
    assert abs(iso_lo - 0.372) < 0.001
    assert abs(iso_hi - 0.667) < 0.001
    text = PROTOCOL.read_text()
    assert "H-win-abs-iso **holds**" in text
    assert "[0.372, 0.667]" in text
    assert "[0.516, 0.979]" in text
    assert "PROTOCOL-isolated-mask" in text
    assert not (ABSOLUTE_GROK / "tables-counts").exists()
    assert not (ABSOLUTE_ORIG / "tables-counts").exists()
