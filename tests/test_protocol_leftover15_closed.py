"""Occupancy-free leftover-15 closed after Distil ∪ SMT; no new trains."""

import json
from pathlib import Path

from text_watermark_tools.leftover import (
    leftover_keys_from_union,
    summarize_official_on_keys,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-leftover-15-closed.md"
UNION15 = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-union-distil100x4-and-smt-to-12x4"
    / "union.json"
)
UNION18 = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4"
    / "union.json"
)
OFFICIAL = (
    ROOT
    / "experiments"
    / "2026-09-01-official-prefix-leftover"
    / "results.json"
)


def test_protocol_leftover15_closed_refuses_targeting() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-l15-left" in text
    assert "H-l15-lamp" in text
    assert "H-l15-iso" in text
    assert "leftover_keys_from_union" in text
    assert "summarize_official_on_keys" in text
    assert "2026-09-01-openings-union-distil100x4-and-smt-to-12x4/union.json" in text
    assert "2026-09-01-official-prefix-leftover/results.json" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "leftover-15" in text
    assert "Do not redefine leftover" in text
    assert "Do **not** mix grok12" in text
    assert "There is no decode command" in text
    assert "H-l15-left **holds**" in text
    assert "H-l15-lamp **holds**" in text
    assert "H-l15-iso **holds**" in text
    assert "Do not sell leftover official **15/15**" in text
    assert "Do not target leftover-15" in text
    assert "PROTOCOL-isolated-mgen" in text
    assert "PROTOCOL-isolated-m12" in text
    assert "PROTOCOL-isolated-xsize" in text
    assert "PROTOCOL-h2-absolute" in text
    assert "PROTOCOL-isolated-xkey" in text
    assert "PROTOCOL-isolated-windows-absolute" in text
    assert "PROTOCOL-isolated-mask" in text
    assert "PROTOCOL-isolated-rankpath-lm" in text
    assert "PROTOCOL-isolated-rankpath-m12" in text
    assert "PROTOCOL-isolated-rankpath-g2m" in text
    assert "PROTOCOL-isolated-rankpath-d2m" in text
    assert "PROTOCOL-isolated-rankpath-g2d" in text
    assert "PROTOCOL-isolated-rankpath-m2d" in text
    assert "PROTOCOL-isolated-rankpath-body" in text
    assert "PROTOCOL-isolated-rankpath-dbody" in text
    assert "H-xkey-iso **fails**" in text
    assert "`570a5c6`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_leftover15_official_is_15_of_15() -> None:
    keys15 = leftover_keys_from_union(UNION15)
    keys18 = leftover_keys_from_union(UNION18)
    assert len(keys15) == 15
    assert len(keys18) == 18
    assert keys15 < keys18
    assert keys18 - keys15 == {
        ("10-office", 1),
        ("10-office", 3),
        ("10-office", 4),
    }
    assert ("10-office", 1) not in keys15
    payload = summarize_official_on_keys(keys15, OFFICIAL)
    assert payload["used_keys"] is True
    assert payload["n_leftover"] == 15
    assert payload["prefixes"]["128"]["leftover_marked"]["n_above_055"] == 15
    assert payload["prefixes"]["16"]["leftover_marked"]["n_above_055"] == 15
    assert payload["prefixes"]["5"]["leftover_marked"]["n_above_055"] == 15
    union = json.loads(UNION15.read_text())
    by = {row["label"]: row for row in union["leftover_signs"]}
    hard = by["12loo-hard-last4"]
    assert hard["n"] == 15
    assert hard["marked_above_zero"] == 9
    assert hard["unmarked_at_most_zero"] == 8
    distil = by["distil-postokhits"]
    assert distil["marked_above_zero"] == 0
    text = PROTOCOL.read_text()
    assert "leftover-15 official is **15/15**" in text or (
        "Leftover-15 official is **15/15**" in text
    )
    assert "leftover last-4 is **9/15 vs 8/15**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "leftover-15 occupancy-free closed" in log
