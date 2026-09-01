"""Leftover-18 published key-free readers are exhausted."""

import json
from pathlib import Path

from text_watermark_tools.leftover import (
    leftover_keys_from_union,
    summarize_official_on_keys,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-leftover-18-closed.md"
READERS = (
    ROOT
    / "experiments"
    / "2026-09-01-isolated-leftover-18-readers"
    / "readers.json"
)
UNION = (
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


def test_protocol_leftover18_closed_refuses_more_holdout_reslices() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-rclosed-C" in text
    assert "H-rclosed-A" in text
    assert "H-rclosed-iso" in text
    assert "2026-09-01-isolated-leftover-18-readers/readers.json" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "Do not redefine leftover" in text
    assert "Do **not** mix grok12" in text
    assert "*(empty until the SHA is named" not in text
    assert "H-rclosed-C **holds**" in text
    assert "H-rclosed-A **holds**" in text
    assert "H-rclosed-iso **holds**" in text
    assert "Do not sell leftover-18 rankpath **12/18**" in text
    assert "leftover-18 mask-*k*" in text
    assert "There is no decode command" in text
    assert "`cdccae5`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_leftover18_published_readers_are_not_leftover_file_detectors() -> None:
    keys = leftover_keys_from_union(UNION)
    raw = json.loads(READERS.read_text())
    assert raw["used_keys"] is False
    assert set((r["stem"], r["sample"]) for r in raw["leftover"]) == keys
    by = {row["label"]: row for row in raw["leftover_signs"]}
    assert by["mixed-rankpath"]["marked_above_zero"] == 12
    assert by["mixed-rankpath"]["unmarked_at_most_zero"] == 13
    assert by["grok36-interpolate"]["marked_above_zero"] == 12
    assert by["grok36-interpolate"]["unmarked_at_most_zero"] == 12
    assert by["12loo-hard-last4"]["marked_above_zero"] == 10
    assert by["12loo-hard-last4"]["unmarked_at_most_zero"] == 10
    atoms = raw["atoms"]
    assert atoms["n_marked_lr_positive"] == 12
    wins = {f"{w['start']}:{w['end']}": w for w in atoms["windows"]}
    assert wins["0:4"]["n_unseen"] == 89
    assert wins["0:4"]["n_seen"] == 19
    official = summarize_official_on_keys(keys, OFFICIAL)
    assert official["used_keys"] is True
    assert official["prefixes"]["128"]["leftover_marked"]["n_above_055"] == 18
    text = PROTOCOL.read_text()
    assert "Leftover-18 published key-free readers are" in text
    assert "exhausted" in text
    assert "Isolated-file remains open" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "leftover-18 published key-free readers closed" in log
