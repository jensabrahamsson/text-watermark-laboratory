"""Distil ↔ gpt2-medium occupancy-free, frozen before decode."""

import json
from pathlib import Path

from text_watermark_tools.generate import is_gpt2_name
from text_watermark_tools.indicator import holdout_from_json

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-xsize.md"
DISTIL_TRAIN = ROOT / "experiments" / "2026-09-01-pair-distil-100x4"
MEDIUM_TRAIN = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-100x4"
DISTIL_TEST = ROOT / "experiments" / "2026-08-31-pair-distilgpt2-12x4"
MEDIUM_TEST = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-12x4"
TRAIN_PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
TEST_PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
DISTIL_TO_MEDIUM_PROBE = (
    ROOT
    / "experiments"
    / "2026-09-01-transfer-distil100x4-to-medium12x4-opening-poshits"
)
DISTIL_TO_MEDIUM_OPENINGS = (
    ROOT / "experiments" / "2026-09-01-openings-distil100x4-to-medium12x4"
)
MEDIUM_TO_DISTIL_PROBE = (
    ROOT
    / "experiments"
    / "2026-09-01-transfer-gpt2-medium-100x4-to-distil12x4-opening-poshits"
)
MEDIUM_TO_DISTIL_OPENINGS = (
    ROOT / "experiments" / "2026-09-01-openings-gpt2-medium-100x4-to-distil12x4"
)


def _prompt_texts(folder: Path) -> set[str]:
    return {
        p.read_text().strip()
        for p in folder.glob("*.txt")
        if p.name != "README.md"
    }


def test_protocol_xsize_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-xsize-cover" in text
    assert "H-xsize-B" in text
    assert "H-xsize-iso" in text
    assert "2026-09-01-pair-distil-100x4" in text
    assert "2026-09-01-pair-gpt2-medium-100x4" in text
    assert "2026-08-31-pair-distilgpt2-12x4" in text
    assert "2026-09-01-pair-gpt2-medium-12x4" in text
    assert "2026-09-01-transfer-distil100x4-to-medium12x4-opening-poshits" in text
    assert "2026-09-01-openings-distil100x4-to-medium12x4" in text
    assert "2026-09-01-transfer-gpt2-medium-100x4-to-distil12x4-opening-poshits" in text
    assert "2026-09-01-openings-gpt2-medium-100x4-to-distil12x4" in text
    assert "leftover-15" in text
    assert "leftover-18" in text
    assert "Do **not** run lock A interpolate" in text
    assert "Do **not** mix grok12" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "postokhits" in text
    assert "--model distilgpt2" in text
    assert "--model gpt2-medium" in text
    assert "Do **not** leftover-slice Distil or gpt2-medium rankpath" in text
    assert "Do **not** apply leftover-15 or leftover-18" in text
    assert "Do **not** target leftover-15" in text
    assert "Distil ∪ gpt2-medium" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    assert "H-xsize-cover **holds**" in text
    assert "H-xsize-B **holds**" in text
    assert "H-xsize-iso **holds**" in text
    assert "`3bb8430`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert DISTIL_TRAIN.is_dir()
    assert MEDIUM_TRAIN.is_dir()
    assert DISTIL_TEST.is_dir()
    assert MEDIUM_TEST.is_dir()
    assert TRAIN_PROMPTS.is_dir()
    assert TEST_PROMPTS.is_dir()
    assert is_gpt2_name("distilgpt2") is True
    assert is_gpt2_name("gpt2-medium") is True


def test_xsize_train_and_test_prompts_are_disjoint() -> None:
    train = _prompt_texts(TRAIN_PROMPTS)
    test = _prompt_texts(TEST_PROMPTS)
    assert len(train) == 100
    assert len(test) == 12
    assert train.isdisjoint(test)


def test_distil_to_medium_occupancy_free_does_not_beat_25() -> None:
    probe = json.loads((DISTIL_TO_MEDIUM_PROBE / "results.json").read_text())
    assert probe["used_keys"] is False
    methods = {m["name"]: m for m in probe["methods"]}
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] == 20
    assert methods["postokhits"]["binary"]["n_negative_at_most_zero"] == 48
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] < 25
    nested = next(
        t
        for t in probe["thresholds"]
        if t["name"] == "postokhits" and t["source"] == "nested-youden"
    )
    assert nested["n_marked_above"] == 46
    assert nested["n_unmarked_at_most"] == 11
    assert nested["train_youden"] < 0
    cov = json.loads((DISTIL_TO_MEDIUM_OPENINGS / "coverage.json").read_text())
    assert cov["used_keys"] is False
    post = cov["final"]["postokhits"]
    assert post["n_covered"] == 22
    assert post["n_exact_opening"] == 4
    assert post["coverage_gate"]["decided_fp"] == 0
    assert post["n_covered"] != 48
    ev = holdout_from_json(DISTIL_TO_MEDIUM_PROBE / "postokhits" / "holdout.json")
    assert ev.n_prompts_marked_above == 11
    assert ev.n_prompt_ties == 1
    assert ev.n_prompts_marked_ge == 12
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "Distil occupancy-free gpt2-medium transfer opened" in log
    text = PROTOCOL.read_text()
    assert "H-xsize-B **holds**" in text
    assert "Do not sell Distil→gpt2-medium **20/48**" in text


def test_medium_to_distil_occupancy_free_does_not_beat_25() -> None:
    probe = json.loads((MEDIUM_TO_DISTIL_PROBE / "results.json").read_text())
    assert probe["used_keys"] is False
    methods = {m["name"]: m for m in probe["methods"]}
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] == 3
    assert methods["postokhits"]["binary"]["n_negative_at_most_zero"] == 47
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] < 25
    nested = next(
        t
        for t in probe["thresholds"]
        if t["name"] == "postokhits" and t["source"] == "nested-youden"
    )
    assert nested["n_marked_above"] == 3
    assert nested["n_unmarked_at_most"] == 48
    cov = json.loads((MEDIUM_TO_DISTIL_OPENINGS / "coverage.json").read_text())
    assert cov["used_keys"] is False
    post = cov["final"]["postokhits"]
    assert post["n_covered"] == 5
    assert post["n_exact_opening"] == 2
    assert post["coverage_gate"]["decided_fp"] == 1
    assert post["n_covered"] != 48
    ev = holdout_from_json(MEDIUM_TO_DISTIL_PROBE / "postokhits" / "holdout.json")
    assert ev.n_prompts_marked_above == 6
    assert ev.n_prompt_ties == 6
    assert ev.n_prompts_marked_ge == 12
    text = PROTOCOL.read_text()
    assert "H-xsize-iso **holds**" in text
    assert "Do not sell Distil→gpt2-medium **20/48**" in text
    assert "gpt2-medium→Distil **3/48**" in text
