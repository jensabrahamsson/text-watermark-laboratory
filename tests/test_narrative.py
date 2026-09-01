"""Narrative freeze: two grains, not a failure paper."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NARRATIVE = ROOT / "research" / "narrative.md"
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-mask.md"


def test_narrative_rejects_failure_title_and_keeps_headlines() -> None:
    text = NARRATIVE.read_text()
    assert "Why Key-Free Watermark Detection Fails" in text
    assert "wrong for this laboratory" in text
    assert "**9/12**" in text
    assert "**25/48**" in text
    assert "**36/36**" in text
    assert "10/12" in text
    assert "29/48" in text
    assert "thesis/" in text
    assert "Two grains" in text
    assert "leftover **10/20 vs 11/20**" in text
    assert "PROTOCOL-next **H3**" in text
    assert "PROTOCOL-isolated-mask-split" in text
    assert "leftover **11/20 vs 11/20**" in text or "leftover is **11/20 vs 11/20**" in text
    assert "Do not write `thesis/`" in text or "Do **not** write `thesis/`" in text
    assert "`004397c`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_narrative_tables_do_not_replace_25() -> None:
    text = NARRATIVE.read_text()
    assert "None of those occupancy-free or nested counts replace **25/48**" in text
    assert "GPT-2 36×4" in text
    assert "DistilGPT2" in text
    assert "Qwen2-1.5B" in text
    assert "`'The'→' car'`" in text
