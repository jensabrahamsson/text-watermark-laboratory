"""Leftover-opening rankpath protocol frozen before mixed LRs."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-leftover.md"
COVERAGE = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-100plusgrok36-to-12x4"
    / "coverage.json"
)


def test_protocol_leftover_names_frozen_rankpath_before_probe() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "--extra-train experiments/2026-09-01-pair-grok36x4" in text
    assert "H-left-C" in text
    assert "H-left-full" in text
    assert "H-left-iso" in text
    assert "thesis/" in text
    assert "Do **not** mix grok12" in text
    assert "2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath" in text
    assert "`7afd049`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_leftover_membership_is_the_mixed_postokhits_zeros() -> None:
    import json

    raw = json.loads(COVERAGE.read_text())
    zeros = raw["final"]["postokhits"]["zeros"]
    keys = {(z["stem"], int(z["sample"])) for z in zeros}
    assert len(keys) == 20
    stems = {s for s, _ in keys}
    assert "01-harbour" in stems
    assert "03-library" in stems
    assert "12-ferry-queue" in stems
    text = PROTOCOL.read_text()
    assert "Closing is the" in text
    assert "The ferry" in text
    assert "Do not redefine leftover" in text


def test_protocol_leftover_mixed_rankpath_is_not_25() -> None:
    import json
    from text_watermark_tools.indicator import holdout_from_json

    root = ROOT / "experiments"
    leftover = json.loads(
        (
            root
            / "2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath"
            / "leftover.json"
        ).read_text()
    )
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    nested = json.loads(
        (
            root
            / "2026-09-01-transfer-100plusgrok36-to-12x4-opening-rankpath"
            / "results.json"
        ).read_text()
    )
    row = next(t for t in nested["thresholds"] if t["source"] == "nested-youden")
    assert leftover["used_keys"] is False
    assert ev.used_keys is False
    assert leftover["leftover"]["n"] == 20
    assert leftover["leftover"]["marked_above_zero"] == 12
    assert leftover["leftover"]["unmarked_at_most_zero"] == 14
    assert leftover["leftover"]["marked_above_zero"] != 25
    assert ev.n_marked_positive == 35
    assert row["n_marked_above"] == 35
    text = PROTOCOL.read_text()
    assert "H-left-C **holds**" in text
    assert "H-left-iso **holds**" in text
    assert "Do not sell **35/48**" in text
    assert "12/20 is not **25/48**" in text
