"""Distil 100×4 → Distil 12×4 occupancy-free, frozen before Distil→Distil decode."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-dgen.md"
TRAIN = ROOT / "experiments" / "2026-09-01-pair-distil-100x4"
TEST = ROOT / "experiments" / "2026-08-31-pair-distilgpt2-12x4"
TRAIN_PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
TEST_PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
PROBE = (
    ROOT
    / "experiments"
    / "2026-09-01-transfer-distil100x4-to-distil12x4-opening-poshits"
)
OPENINGS = (
    ROOT / "experiments" / "2026-09-01-openings-distil100x4-to-distil12x4"
)


def _prompt_texts(folder: Path) -> set[str]:
    return {
        p.read_text().strip()
        for p in folder.glob("*.txt")
        if p.name != "README.md"
    }


def test_protocol_dgen_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-dgen-cover" in text
    assert "H-dgen-B" in text
    assert "H-dgen-iso" in text
    assert "2026-09-01-pair-distil-100x4" in text
    assert "2026-08-31-pair-distilgpt2-12x4" in text
    assert "2026-09-01-transfer-distil100x4-to-distil12x4-opening-poshits" in text
    assert "2026-09-01-openings-distil100x4-to-distil12x4" in text
    assert "leftover-18 GPT-2 keys" in text
    assert "Do **not** run lock A" in text
    assert "Do **not** mix grok12" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "postokhits" in text
    assert "--model distilgpt2" in text
    assert "Do **not** leftover-slice Distil rankpath" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    assert "`6bb95a6`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "H-dgen-cover **holds**" in text
    assert "H-dgen-B **holds**" in text
    assert "H-dgen-iso **holds**" in text
    assert "Do not sell Distil→Distil **16/48**" in text
    assert TRAIN.is_dir()
    assert TEST.is_dir()


def test_dgen_train_and_test_prompts_are_disjoint() -> None:
    train = _prompt_texts(TRAIN_PROMPTS)
    test = _prompt_texts(TEST_PROMPTS)
    assert len(train) == 100
    assert len(test) == 12
    assert train.isdisjoint(test)


def test_distil_to_distil_occupancy_free_equals_opening_coverage() -> None:
    probe = json.loads((PROBE / "results.json").read_text())
    assert probe["used_keys"] is False
    methods = {m["name"]: m for m in probe["methods"]}
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] == 16
    assert methods["postokhits"]["binary"]["n_negative_at_most_zero"] == 39
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] < 25
    nested = next(
        t
        for t in probe["thresholds"]
        if t["name"] == "postokhits" and t["source"] == "nested-youden"
    )
    assert nested["train_youden"] < 0
    cov = json.loads((OPENINGS / "coverage.json").read_text())
    assert cov["used_keys"] is False
    assert cov["final"]["postokhits"]["n_covered"] == 16
    assert cov["final"]["postokhits"]["n_exact_opening"] == 9
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "Distil occupancy-free Distil-12 transfer opened" in log
    text = PROTOCOL.read_text()
    assert "H-dgen-B **holds**" in text
    assert "Do not sell Distil→Distil **16/48**" in text
