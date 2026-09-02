"""Leftover-20 union with short-medium-tails openings, frozen before decode."""

import json
from pathlib import Path

from text_watermark_tools.openings import summarize_coverage_union

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-leftover-union.md"
DUMP = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4"
)


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
    assert "*(empty until the SHA is named" not in text
    assert "Do **not** mix grok12" in text
    assert "`e5a5f6b`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "postokhits" in text
    assert "H-union-smt **holds**" in text
    assert "H-union-left **holds**" in text
    assert "H-union-iso **holds**" in text
    assert "Do not sell union **30/48**" in text


def test_leftover_union_equals_smt_coverage_leftover_is_18() -> None:
    raw = json.loads((DUMP / "union.json").read_text())
    assert raw["used_keys"] is False
    assert raw["used_hash_iv"] is False
    assert raw["used_g_values"] is False
    assert raw["n_covered_a"] == 28
    assert raw["n_covered_b"] == 30
    assert raw["n_union"] == 30
    assert raw["n_intersection"] == 28
    assert raw["n_leftover"] == 18
    assert raw["covered_a_only"] == []
    b_only = {(r["stem"], r["sample"]) for r in raw["covered_b_only"]}
    assert b_only == {("11-garden", 1), ("11-garden", 4)}
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
        ("10-office", 1),
        ("10-office", 3),
        ("10-office", 4),
        ("12-ferry-queue", 1),
        ("12-ferry-queue", 2),
        ("12-ferry-queue", 3),
        ("12-ferry-queue", 4),
    }
    assert ("11-garden", 1) not in leftover
    assert ("11-garden", 4) not in leftover
    by = {row["label"]: row for row in raw["leftover_signs"]}
    hard = by["12loo-hard-last4"]
    assert hard["n"] == 18
    assert hard["marked_above_zero"] == 10
    assert hard["unmarked_at_most_zero"] == 10
    mixed = by["mixed-postokhits"]
    assert mixed["marked_above_zero"] == 0
    assert mixed["unmarked_at_most_zero"] == 18
    recomputed = summarize_coverage_union(
        ROOT
        / "experiments"
        / "2026-09-01-openings-100plusgrok36-to-12x4"
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
            "mixed-postokhits": ROOT
            / "experiments"
            / "2026-09-01-transfer-100plusgrok36-to-12x4-occupancy-free"
            / "postokhits"
            / "holdout.json",
        },
        label_a="100plusgrok36",
        label_b="smt",
    )
    assert recomputed["n_union"] == 30
    assert recomputed["n_leftover"] == 18
    assert recomputed["n_union"] != 25
    text = PROTOCOL.read_text()
    assert "added no unique occupancy-free openings over SMT" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "leftover-20 ∪ short-medium-tails openings opened" in log
    assert "Do not sell union **30/48**" in text
