"""Occupancy-free leftover-18 closed; no new occupancy-free trains."""

import json
from pathlib import Path

from text_watermark_tools.leftover import (
    leftover_keys_from_coverage,
    leftover_keys_from_union,
    summarize_official_on_keys,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-occupancy-closed.md"
UNION = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4"
    / "union.json"
)
COVERAGE20 = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-100plusgrok36-to-12x4"
    / "coverage.json"
)
OFFICIAL = (
    ROOT
    / "experiments"
    / "2026-09-01-official-prefix-leftover"
    / "results.json"
)
BOUND = (
    ROOT / "experiments" / "2026-09-01-isolated-leftover-bound" / "official.json"
)


def test_protocol_occupancy_closed_refuses_family12_and_new_trains() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-closed-left" in text
    assert "H-closed-lamp" in text
    assert "H-closed-iso" in text
    assert "leftover_keys_from_union" in text
    assert "summarize_official_on_keys" in text
    assert "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4/union.json" in text
    assert "2026-09-01-official-prefix-leftover/results.json" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "Do not redefine leftover" in text
    assert "Do **not** mix grok12" in text
    assert "*(empty until the SHA is named" not in text
    assert "H-closed-left **holds**" in text
    assert "H-closed-lamp **holds**" in text
    assert "H-closed-iso **holds**" in text
    assert "Do not sell leftover official **18/18**" in text
    assert "There is no decode command" in text
    assert "`afb7668`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_leftover18_official_is_18_of_18_by_subset() -> None:
    keys18 = leftover_keys_from_union(UNION)
    keys20 = leftover_keys_from_coverage(COVERAGE20)
    assert len(keys18) == 18
    assert keys18 < keys20
    assert len(keys20) == 20
    assert ("11-garden", 1) in keys20
    assert ("11-garden", 1) not in keys18
    assert ("11-garden", 4) not in keys18
    bound = json.loads(BOUND.read_text())
    keys20_bound = {(r["stem"], int(r["sample"])) for r in bound["leftover"]}
    assert keys20_bound == keys20
    payload = summarize_official_on_keys(keys18, OFFICIAL)
    assert payload["used_keys"] is True
    assert payload["n_leftover"] == 18
    assert payload["prefixes"]["128"]["leftover_marked"]["n_above_055"] == 18
    assert payload["prefixes"]["5"]["leftover_marked"]["n_above_055"] == 16
    assert payload["prefixes"]["16"]["leftover_marked"]["n_above_055"] == 18
    text = PROTOCOL.read_text()
    assert "leftover-18 official is **18/18**" in text
    assert "leftover-18 prefix-5 is **16/18**" in text
    assert "occupancy-free coverage from more unrelated GPT-2" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "occupancy-free leftover-18 closed" in log
