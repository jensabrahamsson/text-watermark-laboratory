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
    assert "*(empty until the SHA is named" in text
    assert "`8e33445`" in (ROOT / "research" / "LOGBOOK.md").read_text()
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
