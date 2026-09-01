"""Leftover-18 remaining readers, frozen before leftover-18 rankpath decode."""

import json
from pathlib import Path

from text_watermark_tools.leftover import (
    leftover_keys_from_union,
    summarize_leftover_holdouts,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-leftover-18.md"
DUMP = ROOT / "experiments" / "2026-09-01-isolated-leftover-18-readers"
UNION = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4"
    / "union.json"
)


def test_protocol_leftover18_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-left18-C" in text
    assert "H-left18-A" in text
    assert "H-left18-iso" in text
    assert "summarize_leftover_holdouts" in text
    assert "summarize_leftover_interpolate_atoms" in text
    assert "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4/union.json" in text
    assert (
        "2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath/rankpath/holdout.json"
        in text
    )
    assert (
        "2026-09-01-transfer-grok36x4-to-12x4-hard-last4/interpolate/holdout.json"
        in text
    )
    assert "2026-09-01-isolated-leftover-18-readers" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "Do not redefine leftover" in text
    assert "*(empty until the SHA is named" not in text
    assert "Do **not** mix grok12" in text
    assert "dump_interpolate_atoms" in text
    assert "10/18 vs 10/18" in text
    assert "`5621544`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "H-left18-C **holds**" in text
    assert "H-left18-A **holds**" in text
    assert "H-left18-iso **holds**" in text
    assert "Do not sell leftover-18 rankpath **12/18**" in text


def test_leftover_holdouts_helper_on_synthetic(tmp_path: Path) -> None:
    holdout = {
        "used_keys": False,
        "files": [
            {"stem": "left", "sample": 1, "file": "left-1.txt", "lr": 0.2},
            {"stem": "left", "sample": 1, "file": "left-1.unmarked.txt", "lr": -0.1},
            {"stem": "left", "sample": 2, "file": "left-2.txt", "lr": -0.3},
            {"stem": "left", "sample": 2, "file": "left-2.unmarked.txt", "lr": 0.05},
            {"stem": "cov", "sample": 1, "file": "cov-1.txt", "lr": 1.0},
            {"stem": "cov", "sample": 1, "file": "cov-1.unmarked.txt", "lr": -1.0},
        ],
    }
    path = tmp_path / "holdout.json"
    path.write_text(__import__("json").dumps(holdout))
    payload = summarize_leftover_holdouts(
        {("left", 1), ("left", 2)},
        {"synthetic": path},
    )
    assert payload["used_keys"] is False
    assert payload["n_leftover"] == 2
    row = payload["leftover_signs"][0]
    assert row["label"] == "synthetic"
    assert row["marked_above_zero"] == 1
    assert row["unmarked_at_most_zero"] == 1


def test_leftover18_rankpath_is_chance_interpolate_is_backoff() -> None:
    raw = json.loads((DUMP / "readers.json").read_text())
    assert raw["used_keys"] is False
    assert raw["n_leftover"] == 18
    by = {row["label"]: row for row in raw["leftover_signs"]}
    rank = by["mixed-rankpath"]
    assert rank["marked_above_zero"] == 12
    assert rank["unmarked_at_most_zero"] == 13
    interp = by["grok36-interpolate"]
    assert interp["marked_above_zero"] == 12
    assert interp["unmarked_at_most_zero"] == 12
    hard = by["12loo-hard-last4"]
    assert hard["marked_above_zero"] == 10
    assert hard["unmarked_at_most_zero"] == 10
    atoms = raw["atoms"]
    assert atoms["used_keys"] is False
    assert atoms["n_rows"] == 36
    assert atoms["n_marked_lr_positive"] == 12
    wins = {f"{w['start']}:{w['end']}": w for w in atoms["windows"]}
    assert wins["0:4"]["n_unseen"] == 89
    assert wins["0:4"]["n_seen"] == 19
    assert wins["0:4"]["n_unseen"] > wins["0:4"]["n_seen"]
    top = wins["0:4"]["top_marked_positive_seen"]
    assert top
    assert top[0]["ctx"] == ["Cl"]
    assert top[0]["next"] == "osing"
    assert top[0]["n"] == 4
    keys = leftover_keys_from_union(UNION)
    recomputed = summarize_leftover_holdouts(
        keys,
        {
            "mixed-rankpath": ROOT
            / "experiments"
            / "2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath"
            / "rankpath"
            / "holdout.json",
            "grok36-interpolate": ROOT
            / "experiments"
            / "2026-09-01-transfer-grok36x4-to-12x4-hard-last4"
            / "interpolate"
            / "holdout.json",
            "12loo-hard-last4": ROOT
            / "experiments"
            / "2026-09-01-probe-12x4-recount-hard-last4"
            / "hard"
            / "holdout.json",
        },
    )
    by2 = {row["label"]: row for row in recomputed["leftover_signs"]}
    assert by2["mixed-rankpath"]["marked_above_zero"] == 12
    assert by2["12loo-hard-last4"]["marked_above_zero"] == 10
    text = PROTOCOL.read_text()
    assert "Garden leftover had 0 mixed rankpath TPs" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "leftover-18 remaining readers opened" in log
    assert "Do not sell leftover-18 rankpath **12/18**" in text
