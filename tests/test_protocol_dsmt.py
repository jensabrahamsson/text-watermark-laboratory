"""Distil ∪ SMT openings union, frozen before decode."""

import json
from pathlib import Path

from text_watermark_tools.openings import summarize_coverage_union

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-dsmt.md"
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
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    assert "`b1f0c7d`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "H-dsmt-cover **holds**" in text
    assert "H-dsmt-left **holds**" in text
    assert "H-dsmt-iso **holds**" in text
    assert "Do not sell union **33/48**" in text


def test_dsmt_union_is_33_leftover_is_15() -> None:
    raw = json.loads((DUMP / "union.json").read_text())
    assert raw["used_keys"] is False
    assert raw["used_hash_iv"] is False
    assert raw["used_g_values"] is False
    assert raw["n_covered_a"] == 23
    assert raw["n_covered_b"] == 30
    assert raw["n_union"] == 33
    assert raw["n_intersection"] == 20
    assert raw["n_leftover"] == 15
    a_only = {(r["stem"], r["sample"]) for r in raw["covered_a_only"]}
    assert a_only == {("10-office", 1), ("10-office", 3), ("10-office", 4)}
    leftover = {(r["stem"], r["sample"]) for r in raw["leftover"]}
    assert leftover == {
        ("01-harbour", 1),
        ("01-harbour", 2),
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("03-library", 1),
        ("03-library", 2),
        ("03-library", 3),
        ("03-library", 4),
        ("06-station", 4),
        ("08-letter", 2),
        ("08-letter", 3),
        ("12-ferry-queue", 1),
        ("12-ferry-queue", 2),
        ("12-ferry-queue", 3),
        ("12-ferry-queue", 4),
    }
    assert ("10-office", 1) not in leftover
    assert ("10-office", 3) not in leftover
    assert ("10-office", 4) not in leftover
    by = {row["label"]: row for row in raw["leftover_signs"]}
    hard = by["12loo-hard-last4"]
    assert hard["n"] == 15
    assert hard["marked_above_zero"] == 9
    assert hard["unmarked_at_most_zero"] == 8
    distil = by["distil-postokhits"]
    assert distil["marked_above_zero"] == 0
    assert distil["unmarked_at_most_zero"] == 14
    recomputed = summarize_coverage_union(
        ROOT
        / "experiments"
        / "2026-09-01-openings-distil100x4-to-12x4"
        / "coverage.json",
        ROOT
        / "experiments"
        / "2026-08-31-openings-short-medium-tails"
        / "coverage.json",
        ROOT
        / "experiments"
        / "2026-09-01-probe-12x4-recount-hard-last4"
        / "hard"
        / "holdout.json",
        leftover_holdouts={
            "12loo-hard-last4": ROOT
            / "experiments"
            / "2026-09-01-probe-12x4-recount-hard-last4"
            / "hard"
            / "holdout.json",
            "distil-postokhits": ROOT
            / "experiments"
            / "2026-09-01-transfer-distil100x4-to-12x4-opening-poshits"
            / "postokhits"
            / "holdout.json",
        },
        label_a="distil100x4",
        label_b="smt",
    )
    assert recomputed["n_union"] == 33
    assert recomputed["n_leftover"] == 15
    assert recomputed["n_union"] != 25
    text = PROTOCOL.read_text()
    assert "Leftover after Distil ∪ SMT is **15**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "Distil ∪ SMT openings union opened" in log
    assert "Do not sell union **33/48**" in text
