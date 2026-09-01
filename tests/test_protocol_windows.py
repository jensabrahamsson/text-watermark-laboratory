"""Window readout of 100-family interpolate tables."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-windows.md"
GROK = (
    ROOT
    / "experiments"
    / "2026-09-01-transfer-100x4-to-grok12x4-hard-windows"
    / "results.json"
)
ORIG = (
    ROOT
    / "experiments"
    / "2026-09-01-transfer-100x4-to-12x4-hard-windows"
    / "results.json"
)


def _windows(raw: dict) -> dict[tuple[int, int], dict]:
    return {(int(w["start"]), int(w["end"])): w for w in raw["window_scores"]}


def test_protocol_windows_names_frozen_flags() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--windows 0:4,4:16,16:32,32:64,64:128" in text
    assert "H-win-open **holds**" in text
    assert "H-win-mid **holds**" in text
    assert "H-win-12 **holds**" in text
    assert "H-win-iso **holds**" in text
    assert "2026-09-01-atoms-100x4-to-grok12x4-interpolate" in text
    assert "thesis/" in text
    assert "`7d8759a`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_protocol_windows_grok_rank_is_not_front_loaded() -> None:
    raw = json.loads(GROK.read_text())
    wins = _windows(raw)
    assert raw["used_keys"] is False
    assert wins[(0, 4)]["n_prompt_wins"] == 7
    assert wins[(4, 16)]["n_prompt_wins"] == 4
    assert wins[(32, 64)]["n_prompt_wins"] == 9
    assert wins[(64, 128)]["n_prompt_wins"] == 9
    assert wins[(0, 4)]["n_prompt_wins"] < 11
    assert wins[(32, 64)]["n_prompt_wins"] > 6
    assert wins[(0, 4)]["binary"]["n_positive_above_zero"] == 23
    assert wins[(0, 4)]["binary"]["n_positive_above_zero"] < 25


def test_protocol_windows_original_12_is_front_loaded() -> None:
    raw = json.loads(ORIG.read_text())
    wins = _windows(raw)
    assert raw["used_keys"] is False
    assert wins[(0, 4)]["n_prompt_wins"] == 9
    assert wins[(16, 32)]["n_prompt_wins"] == 6
    assert wins[(0, 4)]["n_prompt_wins"] >= wins[(16, 32)]["n_prompt_wins"]
    assert wins[(0, 4)]["binary"]["n_negative_at_most_zero"] == 31
    assert wins[(0, 4)]["binary"]["n_negative_at_most_zero"] != 22
