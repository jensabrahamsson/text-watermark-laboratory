"""Absolute-history 12-LOO mask-k, frozen before window LRs."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-mask-absolute.md"
REINDEXED = ROOT / "experiments" / "2026-09-01-probe-12x4-headline-windows"
PAIR = ROOT / "experiments" / "2026-08-17-pair-12x4"
ABSOLUTE = ROOT / "experiments" / "2026-09-03-probe-12x4-headline-windows-absolute"


def test_protocol_maskabs_names_frozen_flags_before_probe() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-mask-abs-open" in text
    assert "H-mask-abs-tail" in text
    assert "H-mask-abs-2" in text
    assert "H-mask-abs-iso" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "--windows 0:2,0:4,0:8,2:128,4:128,8:128" in text
    assert "--skip-hashpool" in text
    assert "2026-08-17-pair-12x4" in text
    assert "2026-09-01-probe-12x4-headline-windows" in text
    assert "2026-09-03-probe-12x4-headline-windows-absolute" in text
    assert "score_span" in text
    assert "Do **not** overwrite" in text or "Do not overwrite" in text
    assert "PROTOCOL-isolated-mask.md" in text
    assert "PROTOCOL-next-longctx.md" in text
    assert "thesis/" in text
    assert "no `--include-first`" in text or "no `--include-first`" in text.replace("**", "")
    assert PAIR.is_dir()
    assert REINDEXED.is_dir()
    assert (REINDEXED / "results.json").is_file()
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "PROTOCOL-isolated-mask-absolute" in log
    assert "PROTOCOL-next-longctx" in log
    assert "`b70986d`" in log


def test_protocol_maskabs_keeps_reindexed_dump() -> None:
    import json

    text = PROTOCOL.read_text()
    assert "Do **not** overwrite" in text or "Do not overwrite" in text
    raw = json.loads((REINDEXED / "results.json").read_text())
    assert raw["used_keys"] is False
    assert raw["include_first"] is False
    hard04 = json.loads((REINDEXED / "window-0-4" / "hard" / "holdout.json").read_text())
    hard4128 = json.loads((REINDEXED / "window-4-128" / "hard" / "holdout.json").read_text())
    hard8128 = json.loads((REINDEXED / "window-8-128" / "hard" / "holdout.json").read_text())
    assert hard04["n_prompts_marked_above"] == 5
    assert hard4128["n_prompts_marked_above"] == 9
    assert hard8128["n_prompts_marked_above"] == 9
    assert not ABSOLUTE.exists() or "H-mask-abs-open **holds**" in text or "H-mask-abs-open **fails**" in text


def test_protocol_maskabs_results_wait_for_logbook_or_match_dump() -> None:
    text = PROTOCOL.read_text()
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    opened = ABSOLUTE.exists() and (ABSOLUTE / "results.json").is_file()
    if not opened:
        assert "*(empty until the SHA is named in LOGBOOK.md)*" in text
        assert "H-mask-abs-open **holds**" not in text
        assert "H-mask-abs-open **fails**" not in text
        return
    import json

    raw = json.loads((ABSOLUTE / "results.json").read_text())
    assert raw["used_keys"] is False
    assert raw["include_first"] is False
    assert "H-mask-abs-iso **holds**" in text
    assert "absolute-history 12-LOO mask" in log.lower() or "mask-*k* absolute" in log
    assert "Do not sell" in text or "Do **not** sell" in text
