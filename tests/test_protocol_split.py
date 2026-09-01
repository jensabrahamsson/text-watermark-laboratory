"""In-domain 25/48 leftover-vs-covered split frozen before decode."""

import json
from pathlib import Path

from text_watermark_tools.openings import summarize_isolated_coverage_split

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-split.md"
COVERAGE = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-100plusgrok36-to-12x4"
    / "coverage.json"
)
HOLDOUT = (
    ROOT
    / "experiments"
    / "2026-09-01-probe-12x4-recount-hard-last4"
    / "hard"
    / "holdout.json"
)


def test_protocol_split_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-split-left" in text
    assert "H-split-cov" in text
    assert "H-split-iso" in text
    assert "summarize_isolated_coverage_split" in text
    assert "2026-09-01-openings-100plusgrok36-to-12x4" in text
    assert "2026-09-01-probe-12x4-recount-hard-last4/hard/holdout.json" in text
    assert "2026-09-01-isolated-split-25-leftover-vs-covered" in text
    assert "thesis/" in text
    assert "Do **not** mix grok12" in text
    assert "Do not redefine leftover" in text
    assert "`f09d0e2`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_leftover_membership_stays_twenty_mixed_zeros() -> None:
    raw = json.loads(COVERAGE.read_text())
    zeros = raw["final"]["postokhits"]["zeros"]
    keys = {(z["stem"], int(z["sample"])) for z in zeros}
    assert len(keys) == 20
    hold = json.loads(HOLDOUT.read_text())
    assert hold["used_keys"] is False
    assert hold["n_marked_lr_positive"] == 25
    text = PROTOCOL.read_text()
    assert "The two slices add to 25" in text
    assert "Do not sell leftover-TP count" in text


def test_isolated_coverage_split_helper_on_synthetic_holdout(
    tmp_path: Path,
) -> None:
    coverage = {
        "used_keys": False,
        "final": {
            "postokhits": {
                "zeros": [
                    {"stem": "left", "sample": 1},
                    {"stem": "left", "sample": 2},
                ]
            }
        },
    }
    holdout = {
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "score_kind": "hard",
        "files": [
            {"file": "left-marked.txt", "lr": 0.2, "stem": "left", "sample": 1},
            {
                "file": "left-unmarked-gen.txt",
                "lr": -0.1,
                "stem": "left",
                "sample": 1,
            },
            {"file": "left-marked-2.txt", "lr": -0.3, "stem": "left", "sample": 2},
            {
                "file": "left-unmarked-gen-2.txt",
                "lr": 0.4,
                "stem": "left",
                "sample": 2,
            },
            {"file": "cov-marked.txt", "lr": 0.5, "stem": "cov", "sample": 1},
            {
                "file": "cov-unmarked-gen.txt",
                "lr": -0.2,
                "stem": "cov",
                "sample": 1,
            },
            {"file": "cov-marked-2.txt", "lr": 0.1, "stem": "cov", "sample": 2},
            {
                "file": "cov-unmarked-gen-2.txt",
                "lr": -0.05,
                "stem": "cov",
                "sample": 2,
            },
        ],
    }
    cov_path = tmp_path / "coverage.json"
    hol_path = tmp_path / "holdout.json"
    cov_path.write_text(json.dumps(coverage))
    hol_path.write_text(json.dumps(holdout))
    payload = summarize_isolated_coverage_split(cov_path, hol_path)
    assert payload["used_keys"] is False
    assert payload["n_leftover"] == 2
    assert payload["n_covered"] == 2
    assert payload["primary"]["n_marked_above_zero"] == 3
    assert payload["primary"]["leftover"]["marked_above_zero"] == 1
    assert payload["primary"]["leftover"]["unmarked_at_most_zero"] == 1
    assert payload["primary"]["covered"]["marked_above_zero"] == 2
    assert payload["primary"]["covered"]["unmarked_at_most_zero"] == 2
    assert payload["primary"]["leftover"]["tp"] == [{"stem": "left", "sample": 1}]
