"""gpt2-medium 100×4 → gpt2-medium 12×4 occupancy-free, frozen before decode."""

import json
from pathlib import Path

from text_watermark_tools.generate import is_gpt2_name
from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.pair import pair_stem_files_complete

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-m12.md"
TRAIN = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-100x4"
TEST = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-12x4"
TRAIN_PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
TEST_PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
PROBE = (
    ROOT
    / "experiments"
    / "2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits"
)
OPENINGS = (
    ROOT / "experiments" / "2026-09-01-openings-gpt2-medium-100x4-to-medium12x4"
)


def _prompt_texts(folder: Path) -> set[str]:
    return {
        p.read_text().strip()
        for p in folder.glob("*.txt")
        if p.name != "README.md"
    }


def test_protocol_m12_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-m12-cover" in text
    assert "H-m12-B" in text
    assert "H-m12-iso" in text
    assert "2026-09-01-pair-gpt2-medium-100x4" in text
    assert "2026-08-17-grok-prompts" in text
    assert "2026-09-01-pair-gpt2-medium-12x4" in text
    assert "2026-09-01-transfer-gpt2-medium-100x4-to-medium12x4-opening-poshits" in text
    assert "2026-09-01-openings-gpt2-medium-100x4-to-medium12x4" in text
    assert "leftover-15 GPT-2 keys" in text
    assert "Do **not** run lock A interpolate" in text
    assert "Do **not** mix grok12" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "postokhits" in text
    assert "--model gpt2-medium" in text
    assert "Do **not** leftover-slice gpt2-medium rankpath" in text
    assert "Do **not** apply leftover-15 GPT-2 keys" in text
    assert "Do **not** target leftover-15" in text
    assert "Mixing the new gpt2-medium 12×4 twins into the 100×4 train" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    assert "H-m12-cover **holds**" in text
    assert "H-m12-B **holds**" in text
    assert "H-m12-iso **holds**" in text
    assert "`5be70f3`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert TRAIN.is_dir()
    assert TEST.is_dir()
    assert TRAIN_PROMPTS.is_dir()
    assert TEST_PROMPTS.is_dir()
    assert is_gpt2_name("gpt2-medium") is True


def test_m12_train_and_test_prompts_are_disjoint() -> None:
    train = _prompt_texts(TRAIN_PROMPTS)
    test = _prompt_texts(TEST_PROMPTS)
    assert len(train) == 100
    assert len(test) == 12
    assert train.isdisjoint(test)


def test_medium_to_medium_occupancy_free_does_not_beat_25() -> None:
    probe = json.loads((PROBE / "results.json").read_text())
    assert probe["used_keys"] is False
    methods = {m["name"]: m for m in probe["methods"]}
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] == 10
    assert methods["postokhits"]["binary"]["n_negative_at_most_zero"] == 48
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] < 25
    nested = next(
        t
        for t in probe["thresholds"]
        if t["name"] == "postokhits" and t["source"] == "nested-youden"
    )
    assert nested["n_marked_above"] == 10
    assert nested["n_unmarked_at_most"] == 48
    cov = json.loads((OPENINGS / "coverage.json").read_text())
    assert cov["used_keys"] is False
    post = cov["final"]["postokhits"]
    assert post["n_covered"] == 13
    assert post["n_exact_opening"] == 10
    assert post["coverage_gate"]["decided_fp"] == 0
    assert post["n_covered"] != 48
    ev = holdout_from_json(PROBE / "postokhits" / "holdout.json")
    assert ev.n_prompts_marked_above == 8
    assert ev.n_prompt_ties == 3
    assert ev.n_prompts_marked_ge == 11
    pair = json.loads((TEST / "results.json").read_text())
    wins = sum(
        1
        for row in pair["rows"]
        if row["marked"]["mean"] > row["unmarked_gen"]["mean"]
    )
    assert pair["model_name"] == "gpt2-medium"
    assert pair["seed"] == 20260901
    assert wins == 12
    assert len(pair["rows"]) == 12
    for row in pair["rows"]:
        assert pair_stem_files_complete(TEST, row["stem"], 4)
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "gpt2-medium occupancy-free medium-12 transfer opened" in log
    text = PROTOCOL.read_text()
    assert "H-m12-B **holds**" in text
    assert "Do not sell gpt2-medium→gpt2-medium **10/48**" in text
