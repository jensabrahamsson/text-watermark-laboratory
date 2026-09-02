"""Absolute-history OOD interpolate windows, frozen before window LRs."""

import json
from pathlib import Path

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
    assert "*(empty until the SHA is named in LOGBOOK.md)*" in text
    assert "H-win-abs-open **holds**" not in text
    assert TRAIN.is_dir()
    assert GROK.is_dir()
    assert ORIG.is_dir()
    assert REINDEXED_GROK.is_dir()
    assert REINDEXED_ORIG.is_dir()
    assert not (ABSOLUTE_GROK / "results.json").is_file()
    assert not (ABSOLUTE_ORIG / "results.json").is_file()


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
