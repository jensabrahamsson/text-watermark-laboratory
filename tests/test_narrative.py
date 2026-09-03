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
    assert "PROTOCOL-isolated-leftover-bound" in text
    assert "PROTOCOL-isolated-leftover-union" in text
    assert "leftover **11/20 vs 11/20**" in text or "leftover is **11/20 vs 11/20**" in text
    assert "union **30/48**" in text
    assert "leftover **10/18**" in text
    assert "PROTOCOL-isolated-occupancy-closed" in text
    assert "Leftover-18 official is **18/18**" in text
    assert "PROTOCOL-isolated-leftover-18" in text
    assert "leftover-18 mixed rankpath **12/18 vs 13/18**" in text
    assert "PROTOCOL-isolated-leftover-18-closed" in text
    assert "PROTOCOL-isolated-xgen" in text
    assert "Distil occupancy-free t=0 **22/48 vs 43/48**" in text
    assert "PROTOCOL-isolated-dsmt" in text
    assert "union **33/48**" in text
    assert "leftover **9/15**" in text
    assert "PROTOCOL-isolated-leftover-15-closed" in text
    assert "PROTOCOL-isolated-mgen" in text
    assert "PROTOCOL-isolated-m12" in text
    assert "PROTOCOL-isolated-xsize" in text
    assert "PROTOCOL-h2-absolute" in text
    assert "PROTOCOL-isolated-xkey" in text
    assert "PROTOCOL-isolated-windows-absolute" in text
    assert "PROTOCOL-isolated-mask-absolute" in text
    assert "PROTOCOL-next-longctx" in text
    assert "H-xkey-iso **fails**" in text
    assert "Leftover-15 official is **15/15**" in text
    assert "Master of Science" in text
    assert "Do not write `thesis/`" in text or "Do **not** write `thesis/`" in text
    assert "`004397c`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_narrative_tables_do_not_replace_25() -> None:
    text = NARRATIVE.read_text()
    assert "None of those occupancy-free or nested counts replace **25/48**" in text
    assert "GPT-2 36×4" in text
    assert "DistilGPT2" in text
    assert "Qwen2-1.5B" in text
    assert "`'The'→' car'`" in text
