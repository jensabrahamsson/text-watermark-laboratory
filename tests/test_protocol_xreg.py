"""100 one-liners → Grok-register isolated protocol."""

import json
from pathlib import Path

from text_watermark_tools.indicator import holdout_from_json

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-xreg.md"
TRAIN = ROOT / "experiments" / "2026-09-01-pair-100x4"
TEST = ROOT / "experiments" / "2026-09-01-pair-grok12x4"


def test_protocol_xreg_names_frozen_locks_and_dirs() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--methods poshits --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods postokhits --fit-prefix 4 --pos-bucket 1" in text
    assert "H-xreg-A **holds**" in text
    assert "H-xreg-hard **holds**" in text
    assert "H-xreg-iso **holds**" in text
    assert "H-xreg-B **holds**" in text
    assert "2026-09-01-pair-100x4" in text
    assert "2026-09-01-pair-grok12x4" in text
    assert "transfer-100x4-to-grok12x4-hard-last4" in text
    assert "thesis/" in text
    assert "22/48 vs 41/48" in text
    assert "`1ef7330`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_protocol_xreg_pair_dirs_exist() -> None:
    assert (TRAIN / "results.json").is_file()
    assert (TEST / "results.json").is_file()


def test_protocol_xreg_lock_a_nested_beats_grok_train_not_25() -> None:
    root = ROOT / "experiments"
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-100x4-to-grok12x4-hard-last4"
        / "interpolate"
        / "holdout.json"
    )
    nested = json.loads(
        (root / "2026-09-01-transfer-100x4-to-grok12x4-hard-last4" / "results.json").read_text()
    )
    row = next(t for t in nested["thresholds"] if t["source"] == "nested-youden")
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 11
    assert ev.n_marked_positive == 27
    assert row["n_marked_above"] == 22
    assert row["n_unmarked_at_most"] == 41
    assert row["n_marked_above"] > 16
    assert row["n_marked_above"] <= 24
    assert row["n_marked_above"] < 25
    assert ev.ranking_without_isolated_tp == []
    assert ev.ranking_losses_with_isolated_tp == ["112-taxi-rank"]


def test_protocol_xreg_occupancy_free_is_bounded_by_coverage() -> None:
    root = ROOT / "experiments"
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-100x4-to-grok12x4-occupancy-free"
        / "postokhits"
        / "holdout.json"
    )
    cov = json.loads(
        (root / "2026-09-01-openings-100x4-to-grok12x4" / "coverage.json").read_text()
    )
    nested = json.loads(
        (
            root / "2026-09-01-transfer-100x4-to-grok12x4-occupancy-free" / "results.json"
        ).read_text()
    )
    row = next(t for t in nested["thresholds"] if t["source"] == "nested-youden")
    covered = cov["final"]["postokhits"]["n_covered"]
    assert ev.used_keys is False
    assert cov["used_keys"] is False
    assert ev.n_marked_positive == 0
    assert covered == 5
    assert cov["final"]["postokhits"]["n_exact_opening"] == 0
    assert ev.n_marked_positive <= covered
    assert row["n_marked_above"] == 0
    assert ev.n_prompt_wins_without_isolated_tp == 10
    assert ev.n_prompts_marked_above == 10


def test_protocol_xreg_rankpath_nested_is_not_a_detector() -> None:
    root = ROOT / "experiments"
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-100x4-to-grok12x4-opening-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    nested = json.loads(
        (
            root / "2026-09-01-transfer-100x4-to-grok12x4-opening-rankpath" / "results.json"
        ).read_text()
    )
    row = next(t for t in nested["thresholds"] if t["source"] == "nested-youden")
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 8
    assert ev.n_marked_positive == 10
    assert ev.n_marked_positive < 25
    assert row["n_marked_above"] == 10
    assert row["n_unmarked_at_most"] == 41
    assert ev.ranking_without_isolated_tp == [
        "104-hospital-corridor",
        "110-chip-shop",
    ]
