"""Distil ∪ SMT openings union, frozen before decode."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-dsmt.md"
DISTIL = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-distil100x4-to-12x4"
    / "coverage.json"
)
SMT = (
    ROOT
    / "experiments"
    / "2026-08-31-openings-short-medium-tails"
    / "coverage.json"
)
HOLDOUT = (
    ROOT
    / "experiments"
    / "2026-09-01-probe-12x4-recount-hard-last4"
    / "hard"
    / "holdout.json"
)
DISTIL_HOLDOUT = (
    ROOT
    / "experiments"
    / "2026-09-01-transfer-distil100x4-to-12x4-opening-poshits"
    / "postokhits"
    / "holdout.json"
)
DUMP = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-union-distil100x4-and-smt-to-12x4"
)


def test_protocol_dsmt_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-dsmt-cover" in text
    assert "H-dsmt-left" in text
    assert "H-dsmt-iso" in text
    assert "summarize_coverage_union" in text
    assert "2026-09-01-openings-distil100x4-to-12x4/coverage.json" in text
    assert "2026-08-31-openings-short-medium-tails/coverage.json" in text
    assert "2026-09-01-openings-union-distil100x4-and-smt-to-12x4" in text
    assert "thesis/" in text
    assert "Do not redefine leftover" in text
    assert "family-12" in text
    assert "leftover-15" in text
    assert "Do **not** mix grok12" in text
    assert "postokhits" in text
    assert "distil100x4" in text
    assert DISTIL.is_file()
    assert SMT.is_file()
    assert HOLDOUT.is_file()
    assert DISTIL_HOLDOUT.is_file()
    assert "*(empty until the SHA is named in LOGBOOK.md)*" in text
    assert "H-dsmt-cover **holds**" not in text
    assert not (DUMP / "union.json").exists()
