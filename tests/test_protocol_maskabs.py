"""Absolute-history 12-LOO mask-k, frozen before window LRs."""

import json
from pathlib import Path

from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.stats import clopper_pearson

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
    text = PROTOCOL.read_text()
    assert "Do **not** overwrite" in text or "Do not overwrite" in text
    raw = json.loads((REINDEXED / "results.json").read_text())
    assert raw["used_keys"] is False
    assert raw["include_first"] is False
    hard04 = json.loads((REINDEXED / "window-0-4" / "hard" / "holdout.json").read_text())
    hard4128 = json.loads((REINDEXED / "window-4-128" / "hard" / "holdout.json").read_text())
    hard8128 = json.loads((REINDEXED / "window-8-128" / "hard" / "holdout.json").read_text())
    interp8128 = json.loads(
        (REINDEXED / "window-8-128" / "interpolate" / "holdout.json").read_text()
    )
    assert hard04["n_prompts_marked_above"] == 5
    assert hard4128["n_prompts_marked_above"] == 9
    assert hard8128["n_prompts_marked_above"] == 9
    assert interp8128["n_prompts_marked_above"] == 3


def test_protocol_maskabs_prefixes_equal_reindexed_hard_tails_stay() -> None:
    raw = json.loads((ABSOLUTE / "results.json").read_text())
    assert raw["used_keys"] is False
    assert raw["include_first"] is False
    assert raw["windows"] == ["0:2", "0:4", "0:8", "2:128", "4:128", "8:128"]
    wins = {
        (int(w["start"]), int(w["end"]), w["name"]): w
        for w in raw["window_scores"]
    }
    hard04 = holdout_from_json(ABSOLUTE / "window-0-4" / "hard" / "holdout.json")
    hard4128 = holdout_from_json(ABSOLUTE / "window-4-128" / "hard" / "holdout.json")
    interp8128 = holdout_from_json(
        ABSOLUTE / "window-8-128" / "interpolate" / "holdout.json"
    )
    re_hard04 = json.loads((REINDEXED / "window-0-4" / "hard" / "holdout.json").read_text())
    re_hard4128 = json.loads(
        (REINDEXED / "window-4-128" / "hard" / "holdout.json").read_text()
    )
    re_interp8128 = json.loads(
        (REINDEXED / "window-8-128" / "interpolate" / "holdout.json").read_text()
    )
    assert hard04.used_keys is False
    assert hard04.n_prompts_marked_above == 5
    assert hard04.n_prompts_marked_above == re_hard04["n_prompts_marked_above"]
    assert hard4128.n_prompts_marked_above == 9
    assert hard4128.n_prompts_marked_above == re_hard4128["n_prompts_marked_above"]
    assert interp8128.n_prompts_marked_above == 4
    assert interp8128.n_prompts_marked_above > re_interp8128["n_prompts_marked_above"]
    assert wins[(0, 2, "hard")]["n_prompt_wins"] == 10
    assert wins[(0, 8, "hard")]["n_prompt_wins"] == 6
    assert wins[(8, 128, "hard")]["n_prompt_wins"] == 9
    text = PROTOCOL.read_text()
    assert "H-mask-abs-open **holds**" in text
    assert "H-mask-abs-tail **holds" in text
    assert "H-mask-abs-2 **holds**" in text
    assert "H-mask-abs-iso **holds**" in text
    assert "rose" in text
    assert "Do **not** sell tail **9/12**" in text or "Do not sell tail **9/12**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "`b70986d`" in log
    assert not (ABSOLUTE / "tables-counts").exists()


def test_protocol_maskabs_isolated_grain_stays_chance() -> None:
    five_lo, five_hi = clopper_pearson(5, 12)
    nine_lo, nine_hi = clopper_pearson(9, 12)
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert five_lo <= 0.5 <= five_hi
    assert nine_lo <= 0.5 <= nine_hi
    assert iso_lo <= 0.5 <= iso_hi
    assert abs(iso_lo - 0.372) < 0.001
    assert abs(iso_hi - 0.667) < 0.001
    hard04 = json.loads((ABSOLUTE / "window-0-4" / "hard" / "holdout.json").read_text())
    assert hard04["n_marked_lr_positive"] == 29
    assert hard04["n_unmarked_lr_nonpositive"] == 26
    text = PROTOCOL.read_text()
    assert "H-mask-abs-iso **holds**" in text
    assert "[0.372, 0.667]" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
