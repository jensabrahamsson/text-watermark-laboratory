"""Distil ↔ gpt2-medium occupancy-free, frozen before decode."""

from pathlib import Path

from text_watermark_tools.generate import is_gpt2_name

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-xsize.md"
DISTIL_TRAIN = ROOT / "experiments" / "2026-09-01-pair-distil-100x4"
MEDIUM_TRAIN = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-100x4"
DISTIL_TEST = ROOT / "experiments" / "2026-08-31-pair-distilgpt2-12x4"
MEDIUM_TEST = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-12x4"
TRAIN_PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
TEST_PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"


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
    assert "*(empty until the SHA is named in LOGBOOK.md)*" in text
    assert "H-xsize-cover **holds**" not in text
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
