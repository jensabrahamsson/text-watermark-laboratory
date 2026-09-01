"""Leftover-18 remaining readers, frozen before leftover-18 rankpath decode."""

from pathlib import Path

from text_watermark_tools.leftover import summarize_leftover_holdouts

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-leftover-18.md"


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
    assert "*(empty until the SHA is named" in text
    assert "Do **not** mix grok12" in text
    assert "dump_interpolate_atoms" in text
    assert "10/18 vs 10/18" in text
    assert "`5621544`" in (ROOT / "research" / "LOGBOOK.md").read_text()


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
