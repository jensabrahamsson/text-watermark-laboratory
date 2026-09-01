"""Qwen 100×4 → Qwen 12×4 occupancy-free, frozen before Qwen→Qwen decode."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-qgen.md"
TRAIN = ROOT / "experiments" / "2026-09-01-pair-qwen-100x4"
TEST = ROOT / "experiments" / "2026-08-31-pair-qwen-12x4"
TRAIN_PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
TEST_PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"


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
    assert "*(empty until the SHA is named in LOGBOOK.md)*" in text
    assert "`3c0a5c9`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert TRAIN.is_dir()
    assert TEST.is_dir()


def test_qgen_train_and_test_prompts_are_disjoint() -> None:
    train = _prompt_texts(TRAIN_PROMPTS)
    test = _prompt_texts(TEST_PROMPTS)
    assert len(train) == 100
    assert len(test) == 12
    assert train.isdisjoint(test)
