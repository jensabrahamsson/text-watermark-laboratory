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
    assert "Masking *k*=1 is" in text
    assert "2026-09-01-probe-12x4-headline-windows" in text
    assert "`004397c`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "H-mask-open **fails**" in text
    assert "H-mask-iso **holds**" in text


def test_protocol_mask_hard_tail_keeps_nine_open_is_five() -> None:
    import json

    root = ROOT / "experiments" / "2026-09-01-probe-12x4-headline-windows"
    raw = json.loads((root / "results.json").read_text())
    assert raw["used_keys"] is False
    assert raw["include_first"] is False
    hard04 = json.loads((root / "window-0-4" / "hard" / "holdout.json").read_text())
    hard4128 = json.loads((root / "window-4-128" / "hard" / "holdout.json").read_text())
    hard8128 = json.loads((root / "window-8-128" / "hard" / "holdout.json").read_text())
    interp8128 = json.loads(
        (root / "window-8-128" / "interpolate" / "holdout.json").read_text()
    )
    assert hard04["n_prompts_marked_above"] == 5
    assert hard4128["n_prompts_marked_above"] == 9
    assert hard8128["n_prompts_marked_above"] == 9
    assert interp8128["n_prompts_marked_above"] == 3
    assert hard04["n_marked_lr_positive"] != 25 or hard04["n_prompts_marked_above"] != 9
    text = PROTOCOL.read_text()
    assert "Do not sell prefix" in text
    assert "hard** 9/12 is not an opening-only" in text or "hard 9/12 is not an opening-only" in text
