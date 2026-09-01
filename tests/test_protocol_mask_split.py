"""Leftover vs covered on mask-k windows, frozen before decode."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-mask-split.md"


def test_protocol_mask_split_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-wsplit-tail" in text
    assert "H-wsplit-open" in text
    assert "H-wsplit-iso" in text
    assert "summarize_isolated_coverage_split" in text
    assert "window-4-128/hard/holdout.json" in text
    assert "window-8-128/hard/holdout.json" in text
    assert "window-0-4/hard/holdout.json" in text
    assert "2026-09-01-isolated-split-windows-leftover-vs-covered" in text
    assert "thesis/" in text
    assert "Do not redefine leftover" in text
    assert "*(empty until the SHA is named" in text
    assert "Do **not** mix grok12" in text
