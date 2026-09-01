"""Headline 12-LOO mask-k windows frozen before probe."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-mask.md"


def test_protocol_mask_names_frozen_windows_before_probe() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "--windows 0:2,0:4,0:8,2:128,4:128,8:128" in text
    assert "--skip-hashpool" in text
    assert "H-mask-open" in text
    assert "H-mask-tail" in text
    assert "H-mask-2" in text
    assert "H-mask-iso" in text
    assert "thesis/" in text
    assert "no `--include-first`" in text
    assert "2026-09-01-probe-12x4-headline-windows" in text
    assert "*(empty until the SHA is named" in text
    assert "Masking *k*=1 is" in text
