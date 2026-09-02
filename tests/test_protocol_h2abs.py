"""Absolute-history H2 remasure, frozen before window LRs."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-h2-absolute.md"
PAIR = ROOT / "experiments" / "2026-09-01-pair-100x4"
REINDEXED = ROOT / "experiments" / "2026-09-01-probe-100x4-hard-windows"
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"


def test_protocol_h2abs_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H2-abs" in text
    assert "H2-abs-acc" in text
    assert "H2-abs-iso" in text
    assert "2026-09-01-pair-100x4" in text
    assert "2026-09-01-probe-100x4-hard-windows" in text
    assert "2026-09-01-probe-100x4-hard-windows-absolute" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--windows 0:4,4:16,16:32,32:64" in text
    assert "score_span" in text
    assert "Do **not** overwrite" in text or "Do not overwrite" in text
    assert "Do **not** mix grok12" in text
    assert "thesis/" in text
    assert "leftover-15" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" in text
    assert "H2-abs **holds**" not in text
    assert "`89cb62d`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert PAIR.is_dir()
    assert REINDEXED.is_dir()
    assert PROMPTS.is_dir()


def test_h2abs_keeps_reindexed_dump() -> None:
    text = PROTOCOL.read_text()
    assert "Do **not** overwrite" in text or "Do not overwrite the reindexed" in text
    assert (REINDEXED / "results.json").is_file()
    assert (REINDEXED / "window-0-4" / "interpolate" / "holdout.json").is_file()
    assert (REINDEXED / "window-16-32" / "interpolate" / "holdout.json").is_file()
