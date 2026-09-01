"""gpt2-medium 100×4 → gpt2-medium 12×4 occupancy-free, frozen before decode."""

from pathlib import Path

from text_watermark_tools.generate import is_gpt2_name

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-m12.md"
TRAIN = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-100x4"
TRAIN_PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
TEST_PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"


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
    assert "*(empty until the SHA is named in LOGBOOK.md)*" in text
    assert "H-m12-cover **holds**" not in text
    assert "`5be70f3`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert TRAIN.is_dir()
    assert TRAIN_PROMPTS.is_dir()
    assert TEST_PROMPTS.is_dir()
    assert is_gpt2_name("gpt2-medium") is True


def test_m12_train_and_test_prompts_are_disjoint() -> None:
    train = _prompt_texts(TRAIN_PROMPTS)
    test = _prompt_texts(TEST_PROMPTS)
    assert len(train) == 100
    assert len(test) == 12
    assert train.isdisjoint(test)
