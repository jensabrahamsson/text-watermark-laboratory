"""Leftover vs covered on mask-k windows, frozen before decode."""

import json
from pathlib import Path

from text_watermark_tools.openings import summarize_isolated_coverage_split

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-mask-split.md"
COVERAGE = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-100plusgrok36-to-12x4"
    / "coverage.json"
)
WIN = ROOT / "experiments" / "2026-09-01-probe-12x4-headline-windows"
DUMP = (
    ROOT / "experiments" / "2026-09-01-isolated-split-windows-leftover-vs-covered"
)


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
    assert "Do **not** mix grok12" in text
    assert "`3e30e70`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "H-wsplit-tail **holds**" in text
    assert "H-wsplit-open **holds**" in text
    assert "H-wsplit-iso **holds**" in text
    assert "Do not sell leftover **11/20**" in text
    assert "*(empty until the SHA is named" not in text


def test_protocol_mask_split_hard_tail_leftover_is_chance() -> None:
    raw = json.loads((DUMP / "split.json").read_text())
    assert raw["used_keys"] is False
    assert raw["n_leftover"] == 20
    assert raw["n_covered"] == 28
    left = raw["primary"]["leftover"]
    cov = raw["primary"]["covered"]
    assert raw["primary"]["n_marked_above_zero"] == 27
    assert left["marked_above_zero"] == 11
    assert left["unmarked_at_most_zero"] == 11
    assert cov["marked_above_zero"] == 16
    assert cov["unmarked_at_most_zero"] == 11
    assert left["marked_above_zero"] + cov["marked_above_zero"] == 27
    assert left["marked_above_zero"] != 25
    recomputed = summarize_isolated_coverage_split(
        COVERAGE,
        WIN / "window-4-128" / "hard" / "holdout.json",
        extra_holdouts={
            "hard-8:128": WIN / "window-8-128" / "hard" / "holdout.json",
            "hard-0:4": WIN / "window-0-4" / "hard" / "holdout.json",
            "interpolate-4:128": WIN / "window-4-128" / "interpolate" / "holdout.json",
        },
    )
    assert recomputed["primary"]["leftover"]["marked_above_zero"] == 11
    assert recomputed["primary"]["covered"]["marked_above_zero"] == 16
    extra = {row["label"]: row for row in raw["extra"]}
    hard8 = extra["hard-8:128"]
    assert hard8["leftover"]["marked_above_zero"] == 12
    assert hard8["leftover"]["unmarked_at_most_zero"] == 12
    assert hard8["covered"]["marked_above_zero"] == 17
    hard04 = extra["hard-0:4"]
    assert hard04["n_marked_above_zero"] == 29
    assert hard04["leftover"]["marked_above_zero"] == 12
    assert hard04["covered"]["marked_above_zero"] == 17
    interp = extra["interpolate-4:128"]
    assert interp["n_marked_above_zero"] == 20
    assert interp["leftover"]["marked_above_zero"] == 7
    assert interp["covered"]["marked_above_zero"] == 13
    leftover_tps = {(r["stem"], r["sample"]) for r in left["tp"]}
    leftover_fns = {(r["stem"], r["sample"]) for r in left["fn"]}
    assert {("06-station", 4), ("10-office", 4), ("12-ferry-queue", 1), ("12-ferry-queue", 2)} <= leftover_tps
    assert ("12-ferry-queue", 3) in leftover_fns
    assert {("11-garden", 1), ("11-garden", 4), ("08-letter", 2)} <= leftover_tps
    text = PROTOCOL.read_text()
    assert "Leftover tail is chance" in text
    assert "Tail prompt **9/12** is occupancy-covered" in text
    assert "Do not sell leftover **11/20**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "leftover-versus-covered mask-k window split opened" in log
    assert "**11/20**" in log
