"""Absolute-history H2 remasure, frozen before window LRs."""

import json
from pathlib import Path

from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.stats import (
    clopper_pearson,
    mcnemar_exact_p,
    paired_prompt_sign_table,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-h2-absolute.md"
PAIR = ROOT / "experiments" / "2026-09-01-pair-100x4"
REINDEXED = ROOT / "experiments" / "2026-09-01-probe-100x4-hard-windows"
ABSOLUTE = ROOT / "experiments" / "2026-09-01-probe-100x4-hard-windows-absolute"
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"


def _windows(raw: dict) -> dict[tuple[int, int], dict]:
    return {(int(w["start"]), int(w["end"])): w for w in raw["window_scores"]}


def test_protocol_h2abs_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H2-abs" in text
    assert "H2-abs-acc" in text
    assert "H2-abs-iso" in text
    assert "2026-09-01-pair-100x4" in text
    assert "2026-09-01-probe-100x4-hard-windows" in text
    assert "2026-09-01-probe-100x4-hard-windows-absolute" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--windows 0:4,4:16,16:32,32:64" in text
    assert "score_span" in text
    assert "Do **not** overwrite" in text or "Do not overwrite" in text
    assert "Do **not** mix grok12" in text
    assert "thesis/" in text
    assert "leftover-15" in text
    assert "PROTOCOL-isolated-xkey" in text
    assert "PROTOCOL-isolated-windows-absolute" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    assert "H2-abs **holds**" in text
    assert "H2-abs-acc **holds**" in text
    assert "H2-abs-iso **holds**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "`89cb62d`" in log
    assert "`450658c`" in log
    assert PAIR.is_dir()
    assert REINDEXED.is_dir()
    assert ABSOLUTE.is_dir()
    assert PROMPTS.is_dir()


def test_h2abs_keeps_reindexed_dump() -> None:
    text = PROTOCOL.read_text()
    assert "Do **not** overwrite" in text or "Do not overwrite the reindexed" in text
    assert (REINDEXED / "results.json").is_file()
    reindexed = json.loads((REINDEXED / "results.json").read_text())
    wins = _windows(reindexed)
    assert reindexed["used_keys"] is False
    assert wins[(0, 4)]["n_prompt_wins"] == 99
    assert wins[(16, 32)]["n_prompt_wins"] == 89
    assert abs(wins[(0, 4)]["binary"]["auc"] - 0.885) < 0.001
    assert abs(wins[(16, 32)]["binary"]["auc"] - 0.689) < 0.001
    assert (REINDEXED / "window-0-4" / "interpolate" / "holdout.json").is_file()
    assert (REINDEXED / "window-16-32" / "interpolate" / "holdout.json").is_file()


def test_h2abs_absolute_opening_outranks_midfile() -> None:
    raw = json.loads((ABSOLUTE / "results.json").read_text())
    wins = _windows(raw)
    assert raw["used_keys"] is False
    assert raw["used_hash_iv"] is False
    assert raw["used_g_values"] is False
    assert raw["pair_dir"] == "experiments/2026-09-01-pair-100x4"
    assert raw["windows"] == ["0:4", "4:16", "16:32", "32:64"]
    assert wins[(0, 4)]["n_prompt_wins"] == 99
    assert wins[(0, 4)]["n_prompt_ties"] == 0
    assert wins[(16, 32)]["n_prompt_wins"] == 87
    assert wins[(16, 32)]["n_prompt_ties"] == 0
    assert wins[(0, 4)]["n_prompt_wins"] > wins[(16, 32)]["n_prompt_wins"]
    assert abs(wins[(0, 4)]["binary"]["auc"] - 0.885) < 0.001
    assert abs(wins[(16, 32)]["binary"]["auc"] - 0.695) < 0.001
    assert wins[(0, 4)]["binary"]["n_positive_above_zero"] == 372
    assert wins[(0, 4)]["binary"]["n_negative_at_most_zero"] == 272
    assert wins[(16, 32)]["binary"]["n_positive_above_zero"] == 267
    assert wins[(16, 32)]["binary"]["n_negative_at_most_zero"] == 240
    nested0 = wins[(0, 4)]["nested_stem"]["nested-youden-by-stem"]
    nested16 = wins[(16, 32)]["nested_stem"]["nested-youden-by-stem"]
    assert nested0["n_marked_above"] == 361
    assert nested0["n_unmarked_at_most"] == 311
    assert nested16["n_marked_above"] == 215
    assert nested16["n_unmarked_at_most"] == 313
    early = holdout_from_json(ABSOLUTE / "window-0-4" / "interpolate" / "holdout.json")
    mid = holdout_from_json(ABSOLUTE / "window-16-32" / "interpolate" / "holdout.json")
    assert early.used_keys is False
    assert mid.used_keys is False
    assert early.n_prompts_marked_above == 99
    assert mid.n_prompts_marked_above == 87
    assert early.n_prompts_marked_above > mid.n_prompts_marked_above
    text = PROTOCOL.read_text()
    assert "H2-abs **holds**" in text
    assert "Do not sell absolute 0:4 **99/100**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "absolute-history H2 remasure opened" in log


def test_h2abs_midfile_did_not_rise_versus_reindexed() -> None:
    absolute = _windows(json.loads((ABSOLUTE / "results.json").read_text()))
    reindexed = _windows(json.loads((REINDEXED / "results.json").read_text()))
    assert absolute[(16, 32)]["n_prompt_wins"] == 87
    assert reindexed[(16, 32)]["n_prompt_wins"] == 89
    assert absolute[(16, 32)]["n_prompt_wins"] < reindexed[(16, 32)]["n_prompt_wins"]
    assert absolute[(16, 32)]["n_prompt_wins"] > 50
    assert absolute[(0, 4)]["n_prompt_wins"] == reindexed[(0, 4)]["n_prompt_wins"]
    assert absolute[(0, 4)]["binary"]["n_positive_above_zero"] == 372
    assert reindexed[(0, 4)]["binary"]["n_positive_above_zero"] == 372
    text = PROTOCOL.read_text()
    assert "H2-abs-acc **holds**" in text
    assert "did **not** rise versus reindexed **89/100**" in text
    assert "H2-abs-iso **holds**" in text


def test_h2abs_paired_prompt_family_mcnemar_from_holdouts() -> None:
    early = holdout_from_json(ABSOLUTE / "window-0-4" / "interpolate" / "holdout.json")
    mid = holdout_from_json(ABSOLUTE / "window-16-32" / "interpolate" / "holdout.json")
    table = paired_prompt_sign_table(
        early.stems,
        early.marked_lrs,
        early.unmarked_lrs,
        mid.stems,
        mid.marked_lrs,
        mid.unmarked_lrs,
        n_perm=50,
        seed=0,
    )
    assert table.n_stems == 100
    assert table.both_win == 86
    assert table.only_a == 13
    assert table.only_b == 1
    assert table.both_lose == 0
    assert table.n_discordant == 14
    one, two = mcnemar_exact_p(13, 1)
    assert table.mcnemar_one_sided_p == one
    assert table.mcnemar_two_sided_p == two
    assert table.n_a_gap_larger == 93
    assert table.n_b_gap_larger == 7
    assert table.n_gap_ties == 0
    assert abs(table.mean_gap_diff - 1.6875446420769182) < 1e-9
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert iso_lo <= 0.5 <= iso_hi
    nine_lo, nine_hi = clopper_pearson(9, 12)
    assert nine_lo <= 0.5 <= nine_hi
    abs99_lo, _abs99_hi = clopper_pearson(99, 100)
    mid_lo, _mid_hi = clopper_pearson(87, 100)
    assert abs99_lo > 0.5
    assert mid_lo > 0.5
    text = PROTOCOL.read_text()
    assert "not a second freeze" in text
    assert "**86**" in text
    assert "**13**" in text
    assert "McNemar" in text
    assert "Clopper–Pearson" in text
    assert "[0.372, 0.667]" in text
    assert "Do not sell" in text
    assert "McNemar **0.00092**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "paired prompt-family H2 readout" in log
