"""Window readout of 100-family interpolate tables: freeze before LRs."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-windows.md"


def test_protocol_windows_names_frozen_flags() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--windows 0:4,4:16,16:32,32:64,64:128" in text
    assert "H-win-open" in text
    assert "H-win-mid" in text
    assert "H-win-12" in text
    assert "H-win-iso" in text
    assert "2026-09-01-pair-grok12x4" in text
    assert "2026-08-17-pair-12x4" in text
    assert "thesis/" in text
    assert "## Results" not in text
