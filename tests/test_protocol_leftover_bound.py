"""Occupancy leftover-20 official+atoms bound, frozen before decode."""

from pathlib import Path

from text_watermark_tools.leftover import (
    summarize_leftover_interpolate_atoms,
    summarize_occupancy_leftover_official,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-leftover-bound.md"


def test_protocol_leftover_bound_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-bound-lamp" in text
    assert "H-bound-open" in text
    assert "H-bound-atom" in text
    assert "H-bound-iso" in text
    assert "summarize_occupancy_leftover_official" in text
    assert "summarize_leftover_interpolate_atoms" in text
    assert "2026-09-01-official-prefix-leftover/results.json" in text
    assert "2026-09-01-transfer-grok36x4-to-12x4-hard-last4/tables-counts" in text
    assert "2026-09-01-isolated-leftover-bound" in text
    assert "thesis/" in text
    assert "Do not redefine leftover" in text
    assert "*(empty until the SHA is named" in text
    assert "cascade leftover" in text
    assert "Do **not** mix grok12" in text


def test_occupancy_leftover_official_helper_on_synthetic(tmp_path: Path) -> None:
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
    official = {
        "used_keys": True,
        "used_hash_iv": True,
        "used_g_values": True,
        "rows": [
            {
                "stem": "left",
                "sample": 1,
                "side": "marked",
                "prefixes": {"128": {"mean": 0.62}},
            },
            {
                "stem": "left",
                "sample": 1,
                "side": "unmarked",
                "prefixes": {"128": {"mean": 0.50}},
            },
            {
                "stem": "left",
                "sample": 2,
                "side": "marked",
                "prefixes": {"128": {"mean": 0.64}},
            },
            {
                "stem": "left",
                "sample": 2,
                "side": "unmarked",
                "prefixes": {"128": {"mean": 0.49}},
            },
            {
                "stem": "cov",
                "sample": 1,
                "side": "marked",
                "prefixes": {"128": {"mean": 0.63}},
            },
            {
                "stem": "cov",
                "sample": 1,
                "side": "unmarked",
                "prefixes": {"128": {"mean": 0.48}},
            },
        ],
    }
    cov_path = tmp_path / "coverage.json"
    off_path = tmp_path / "official.json"
    cov_path.write_text(__import__("json").dumps(coverage))
    off_path.write_text(__import__("json").dumps(official))
    payload = summarize_occupancy_leftover_official(
        cov_path, off_path, prefixes=("128",)
    )
    assert payload["used_keys"] is True
    assert payload["n_leftover"] == 2
    assert payload["n_covered"] == 1
    left = payload["prefixes"]["128"]["leftover_marked"]
    cov = payload["prefixes"]["128"]["covered_marked"]
    um = payload["prefixes"]["128"]["unmarked"]
    assert left["n"] == 2
    assert abs(left["mean"] - 0.63) < 1e-12
    assert left["n_above_055"] == 2
    assert cov["n"] == 1
    assert cov["mean"] == 0.63
    assert um["n"] == 3


def test_leftover_atoms_helper_on_synthetic() -> None:
    leftover = {("left", 1)}
    atoms = {
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "rows": [
            {
                "stem": "left",
                "sample": 1,
                "side": "marked",
                "lr": 0.2,
                "hits": [
                    {
                        "i": 1,
                        "ctx": {"tokens": ["The"]},
                        "next": " ferry",
                        "delta": 0.4,
                        "unseen_next": True,
                    },
                    {
                        "i": 8,
                        "ctx": {"tokens": ["Cl"]},
                        "next": "osing",
                        "delta": 2.0,
                        "unseen_next": False,
                    },
                ],
            },
            {
                "stem": "left",
                "sample": 1,
                "side": "unmarked",
                "lr": -0.1,
                "hits": [
                    {
                        "i": 1,
                        "ctx": {"tokens": ["The"]},
                        "next": " old",
                        "delta": -0.2,
                        "unseen_next": True,
                    }
                ],
            },
            {
                "stem": "cov",
                "sample": 1,
                "side": "marked",
                "lr": 1.0,
                "hits": [
                    {
                        "i": 1,
                        "ctx": {"tokens": ["The"]},
                        "next": " car",
                        "delta": 5.0,
                        "unseen_next": False,
                    }
                ],
            },
        ],
    }
    payload = summarize_leftover_interpolate_atoms(
        atoms, leftover, windows=((0, 4), (4, 16))
    )
    assert payload["used_keys"] is False
    assert payload["n_rows"] == 2
    assert payload["n_marked_lr_positive"] == 1
    wins = {f"{w['start']}:{w['end']}": w for w in payload["windows"]}
    assert wins["0:4"]["n_unseen"] == 2
    assert wins["0:4"]["n_seen"] == 0
    assert wins["4:16"]["n_seen"] == 1
    assert wins["4:16"]["n_unseen"] == 0
