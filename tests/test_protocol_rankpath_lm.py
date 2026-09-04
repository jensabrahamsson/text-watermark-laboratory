"""Distil / gpt2-medium unmarked-LM opening rankpath, locked before LRs."""

import json
from pathlib import Path

import pytest

from text_watermark_tools.generate import is_gpt2_name
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-rankpath-lm.md"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-08-17-pair-12x4"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
CONTROL = ROOT / "experiments" / "2026-09-01-probe-12x4-recount-opening-rankpath"
DISTIL = ROOT / "experiments" / "2026-09-04-probe-12x4-rankpath-distil-lm"
MEDIUM = ROOT / "experiments" / "2026-09-04-probe-12x4-rankpath-medium-lm"


def test_protocol_rankpath_lm_locks_config_before_lrs() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-rplm-d" in text
    assert "H-rplm-m" in text
    assert "H-rplm-iso" in text
    assert "H-rplm-d **holds**" not in text
    assert "H-rplm-m **holds**" not in text
    assert "*(empty until the SHA is named in LOGBOOK.md" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "--model distilgpt2" in text
    assert "--model gpt2-medium" in text
    assert "--skip-hashpool" in text
    assert "2026-08-17-pair-12x4" in text
    assert "2026-09-04-probe-12x4-rankpath-distil-lm" in text
    assert "2026-09-04-probe-12x4-rankpath-medium-lm" in text
    assert "2026-09-01-probe-12x4-recount-opening-rankpath" in text
    assert "Do **not** look at Distil-LM or gpt2-medium-LM rankpath LRs" in text
    assert "Do **not** leftover-slice" in text
    assert "Do **not** merge GitHub PR **#9**" in text
    assert "Do **not** pass `--rankpath`" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "leftover-15" in text
    assert "41/48" in text
    assert "8/12" in text
    assert "PROTOCOL-isolated-leftover-15-closed.md" in text
    assert "PROTOCOL-isolated-mask-absolute.md" in text
    assert PAIR.is_dir()
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    assert CONTROL.is_dir()
    assert is_gpt2_name("distilgpt2") is True
    assert is_gpt2_name("gpt2-medium") is True
    log = LOG.read_text()
    assert "PROTOCOL-isolated-rankpath-lm" in log
    assert "named before" in log
    assert "--model distilgpt2" in log
    assert "--model gpt2-medium" in log
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert "PROTOCOL-isolated-rankpath-lm" in ledger
    assert "named before" in ledger
    narrative = (ROOT / "research" / "narrative.md").read_text()
    assert "PROTOCOL-isolated-rankpath-lm" in narrative
    assert "named before" in narrative
    agents_rows = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| Distil / gpt2-medium unmarked-LM opening rankpath")
    ]
    assert len(agents_rows) == 1
    assert "named before" in agents_rows[0]
    assert "**25/48**" in agents_rows[0]
    assert "41/48" not in agents_rows[0]
    howto = (ROOT / "HOW-TO.md").read_text()
    assert "PROTOCOL-isolated-rankpath-lm" in howto
    assert "Do not invent those scores" in howto
    for stem in (
        "2026-09-04-probe-12x4-rankpath-distil-lm",
        "2026-09-04-probe-12x4-rankpath-medium-lm",
    ):
        exp_rows = [
            ln
            for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
            if stem in ln
        ]
        assert len(exp_rows) == 1
        assert "named before" in exp_rows[0]
        assert "41/48" not in exp_rows[0]
    research_rows = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if "PROTOCOL-isolated-rankpath-lm" in ln
    ]
    assert len(research_rows) == 1
    assert "named before" in research_rows[0]
    rankpath_note = (ROOT / "research" / "key-free-rankpath.md").read_text()
    assert "PROTOCOL-isolated-rankpath-lm" in rankpath_note
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi


def test_protocol_rankpath_lm_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    distil = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-08-17-pair-12x4",
            "--model",
            "distilgpt2",
            "--skip-hashpool",
            "--fit-prefix",
            "4",
            "--pos-bucket",
            "1",
            "--methods",
            "rankpath",
            "--out-dir",
            "experiments/2026-09-04-probe-12x4-rankpath-distil-lm",
        ]
    )
    assert distil.model == "distilgpt2"
    assert distil.skip_hashpool is True
    assert distil.fit_prefix == 4
    assert distil.methods == "rankpath"

    medium = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-08-17-pair-12x4",
            "--model",
            "gpt2-medium",
            "--skip-hashpool",
            "--fit-prefix",
            "4",
            "--pos-bucket",
            "1",
            "--methods",
            "rankpath",
            "--out-dir",
            "experiments/2026-09-04-probe-12x4-rankpath-medium-lm",
        ]
    )
    assert medium.model == "gpt2-medium"
    assert medium.skip_hashpool is True
    assert medium.methods == "rankpath"


def test_protocol_rankpath_lm_same_lm_control_stays() -> None:
    holdout = json.loads((CONTROL / "rankpath" / "holdout.json").read_text())
    assert holdout["used_keys"] is False
    assert holdout["model_name"] == "gpt2"
    assert holdout["n_marked_lr_positive"] == 41
    assert holdout["n_unmarked_lr_nonpositive"] == 35
    assert holdout["n_prompts_marked_above"] == 11


@pytest.mark.skipif(
    not (DISTIL / "rankpath" / "holdout.json").is_file(),
    reason="Distil-LM opening rankpath not run",
)
def test_protocol_rankpath_lm_distil_from_dumps() -> None:
    interp = json.loads((DISTIL / "rankpath" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["model_name"] == "distilgpt2"
    text = PROTOCOL.read_text()
    if "H-rplm-d **holds**" not in text:
        pytest.skip("Distil-LM rankpath not folded yet")
    marked = interp["n_marked_lr_positive"]
    unmarked = interp["n_unmarked_lr_nonpositive"]
    assert f"**{marked}/48" in text
    assert f"**{unmarked}/48" in text
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi


@pytest.mark.skipif(
    not (MEDIUM / "rankpath" / "holdout.json").is_file(),
    reason="gpt2-medium-LM opening rankpath not run",
)
def test_protocol_rankpath_lm_medium_from_dumps() -> None:
    interp = json.loads((MEDIUM / "rankpath" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["model_name"] == "gpt2-medium"
    text = PROTOCOL.read_text()
    if "H-rplm-m **holds**" not in text:
        pytest.skip("medium-LM rankpath not folded yet")
    marked = interp["n_marked_lr_positive"]
    unmarked = interp["n_unmarked_lr_nonpositive"]
    assert f"**{marked}/48" in text
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi
