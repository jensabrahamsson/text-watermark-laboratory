"""100 one-liners → Grok-register isolated protocol: freeze before LRs."""

from pathlib import Path

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
    assert "H-xreg-A" in text
    assert "H-xreg-hard" in text
    assert "H-xreg-iso" in text
    assert "H-xreg-B" in text
    assert "2026-09-01-pair-100x4" in text
    assert "2026-09-01-pair-grok12x4" in text
    assert "transfer-100x4-to-grok12x4-hard-last4" in text
    assert "thesis/" in text
    assert "## Results" not in text
    assert "`1ef7330`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_protocol_xreg_pair_dirs_exist() -> None:
    assert (TRAIN / "results.json").is_file()
    assert (TEST / "results.json").is_file()
