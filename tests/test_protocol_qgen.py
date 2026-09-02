"""Qwen 100×4 → Qwen 12×4 occupancy-free, frozen before Qwen→Qwen decode."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-qgen.md"
TRAIN = ROOT / "experiments" / "2026-09-01-pair-qwen-100x4"
TEST = ROOT / "experiments" / "2026-08-31-pair-qwen-12x4"
TRAIN_PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
TEST_PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
PROBE = (
    ROOT
    / "experiments"
    / "2026-09-01-transfer-qwen100x4-to-qwen12x4-opening-poshits"
)
OPENINGS = ROOT / "experiments" / "2026-09-01-openings-qwen100x4-to-qwen12x4"


def _prompt_texts(folder: Path) -> set[str]:
    return {
        p.read_text().strip()
        for p in folder.glob("*.txt")
        if p.name != "README.md"
    }


def test_protocol_qgen_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-qgen-cover" in text
    assert "H-qgen-B" in text
    assert "H-qgen-iso" in text
    assert "2026-09-01-pair-qwen-100x4" in text
    assert "2026-08-31-pair-qwen-12x4" in text
    assert "2026-09-01-transfer-qwen100x4-to-qwen12x4-opening-poshits" in text
    assert "2026-09-01-openings-qwen100x4-to-qwen12x4" in text
    assert "leftover-18 GPT-2 keys" in text
    assert "Do **not** run lock A" in text
    assert "Do **not** mix grok12" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "postokhits" in text
    assert "Qwen/Qwen2-1.5B-Instruct" in text
    assert "Do **not** use `--include-first`" in text
    assert "Dashscope" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    assert "`3c0a5c9`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "H-qgen-cover **holds**" in text
    assert "H-qgen-B **fails**" in text
    assert "H-qgen-iso **holds**" in text
    assert "Do not sell Qwen→Qwen **31/48**" in text
    assert TRAIN.is_dir()
    assert TEST.is_dir()


def test_qgen_train_and_test_prompts_are_disjoint() -> None:
    train = _prompt_texts(TRAIN_PROMPTS)
    test = _prompt_texts(TEST_PROMPTS)
    assert len(train) == 100
    assert len(test) == 12
    assert train.isdisjoint(test)


def test_qwen_to_qwen_occupancy_free_is_below_opening_coverage() -> None:
    probe = json.loads((PROBE / "results.json").read_text())
    assert probe["used_keys"] is False
    assert probe["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    methods = {m["name"]: m for m in probe["methods"]}
    marked = methods["postokhits"]["binary"]["n_positive_above_zero"]
    unmarked = methods["postokhits"]["binary"]["n_negative_at_most_zero"]
    assert marked == 31
    assert unmarked == 48
    nested = next(
        t
        for t in probe["thresholds"]
        if t["name"] == "postokhits" and t["source"] == "nested-youden"
    )
    assert nested["train_youden"] > 0
    assert nested["n_marked_above"] == 31
    assert nested["n_unmarked_at_most"] == 48
    cov = json.loads((OPENINGS / "coverage.json").read_text())
    assert cov["used_keys"] is False
    covered = cov["final"]["postokhits"]["n_covered"]
    assert covered == 37
    assert marked < covered
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "Qwen occupancy-free Qwen-12 transfer opened" in log
    text = PROTOCOL.read_text()
    assert "H-qgen-B **fails**" in text
    assert "Do not sell Qwen→Qwen **31/48**" in text
