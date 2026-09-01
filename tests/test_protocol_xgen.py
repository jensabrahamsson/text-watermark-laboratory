"""Distil occupancy-free leftover-18, frozen before Distil→12 decode."""

import json
from pathlib import Path

from text_watermark_tools.leftover import leftover_openings_coverage

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-xgen.md"
DISTIL = ROOT / "experiments" / "2026-09-01-pair-distil-100x4"
TEST = ROOT / "experiments" / "2026-08-17-pair-12x4"
UNION = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4"
    / "union.json"
)


def test_protocol_xgen_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-xgen-cover" in text
    assert "H-xgen-B" in text
    assert "H-xgen-iso" in text
    assert "leftover_openings_coverage" in text
    assert "summarize_xgen_leftover" in text
    assert "2026-09-01-pair-distil-100x4" in text
    assert "2026-08-17-pair-12x4" in text
    assert "2026-09-01-openings-union-100plusgrok36-and-smt-to-12x4/union.json" in text
    assert "2026-09-01-transfer-distil100x4-to-12x4-opening-poshits" in text
    assert "2026-09-01-openings-distil100x4-to-12x4" in text
    assert "2026-09-01-isolated-xgen-leftover-18" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "Do not redefine leftover" in text
    assert "Do **not** mix grok12" in text
    assert "postokhits" in text
    assert "--model distilgpt2" in text
    assert "Do **not** leftover-slice Distil rankpath" in text
    assert "*(empty until the SHA is named" not in text
    assert "`8e33445`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "H-xgen-cover **holds**" in text
    assert "H-xgen-B **fails**" in text
    assert "H-xgen-iso **holds**" in text
    assert "Do not sell Distil occupancy-free **22/48**" in text
    assert DISTIL.is_dir()
    assert TEST.is_dir()
    assert UNION.is_file()


def test_leftover_openings_coverage_on_synthetic(tmp_path: Path) -> None:
    openings = {
        "used_keys": False,
        "final": {
            "postokhits": {
                "n_covered": 1,
                "n_train_openings": 3,
                "zeros": [
                    {"stem": "left", "sample": 1},
                    {"stem": "left", "sample": 2},
                ],
            }
        },
    }
    path = tmp_path / "coverage.json"
    path.write_text(json.dumps(openings))
    payload = leftover_openings_coverage(
        {("left", 1), ("left", 2), ("cov", 1)},
        path,
    )
    assert payload["used_keys"] is False
    assert payload["n_leftover"] == 3
    assert payload["n_covered"] == 1
    assert payload["n_uncovered"] == 2
    assert payload["covered"] == [{"stem": "cov", "sample": 1}]


def test_distil_occupancy_free_leftover18_is_office_three() -> None:
    dump = ROOT / "experiments" / "2026-09-01-isolated-xgen-leftover-18"
    raw = json.loads((dump / "xgen.json").read_text())
    assert raw["used_keys"] is False
    assert raw["n_leftover"] == 18
    by = {row["label"]: row for row in raw["leftover_signs"]}
    assert by["distil-postokhits"]["marked_above_zero"] == 3
    assert by["distil-postokhits"]["unmarked_at_most_zero"] == 16
    cov = raw["openings"]
    assert cov["n_covered"] == 3
    assert cov["n_uncovered"] == 15
    assert cov["n_marked_covered"] == 23
    covered = {(r["stem"], r["sample"]) for r in cov["covered"]}
    assert covered == {("10-office", 1), ("10-office", 3), ("10-office", 4)}
    probe = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-01-transfer-distil100x4-to-12x4-opening-poshits"
            / "results.json"
        ).read_text()
    )
    assert probe["used_keys"] is False
    methods = {m["name"]: m for m in probe["methods"]}
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] == 22
    assert methods["postokhits"]["binary"]["n_negative_at_most_zero"] == 43
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] > 16
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] < 25
    text = PROTOCOL.read_text()
    assert "H-xgen-B **fails**" in text
    assert "office 1/3/4" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "Distil occupancy-free leftover-18 opened" in log
    assert "Do not sell Distil occupancy-free **22/48**" in text
