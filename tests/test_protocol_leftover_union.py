"""Leftover-20 union with short-medium-tails openings, frozen before decode."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-leftover-union.md"


def test_protocol_leftover_union_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-union-smt" in text
    assert "H-union-left" in text
    assert "H-union-iso" in text
    assert "summarize_coverage_union" in text
    assert "2026-09-01-openings-100plusgrok36-to-12x4/coverage.json" in text
    assert "2026-08-31-openings-short-medium-tails/coverage.json" in text
    assert "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4" in text
    assert "thesis/" in text
    assert "Do not redefine leftover" in text
    assert "family-12" in text
    assert "*(empty until the SHA is named" in text
    assert "Do **not** mix grok12" in text
    assert "postokhits" in text
