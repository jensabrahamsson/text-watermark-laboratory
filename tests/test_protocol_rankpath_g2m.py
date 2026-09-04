"""GPT-2-small LM opening rankpath on gpt2-medium 12, locked before LRs."""

import json
from pathlib import Path

import pytest

from text_watermark_tools.generate import is_gpt2_name
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-rankpath-g2m.md"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-12x4"
NATIVE = ROOT / "experiments" / "2026-09-04-probe-medium-12x4-rankpath-native"
PROBE = ROOT / "experiments" / "2026-09-04-probe-medium-12x4-rankpath-gpt2-lm"


def test_protocol_rankpath_g2m_locks_config_before_lrs() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-rpg2m" in text
    assert "H-rpg2m-iso" in text
    assert "H-rpg2m **holds**" in text
    assert "H-rpg2m-iso **holds**" in text
    assert "Do not sell **20/48**" in text
    assert "*(empty until the SHA is named in LOGBOOK.md" not in text
    assert "--model gpt2" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "2026-09-01-pair-gpt2-medium-12x4" in text
    assert "2026-09-04-probe-medium-12x4-rankpath-gpt2-lm" in text
    assert "Do **not** look at GPT-2-small-on-medium rankpath LRs" in text
    assert "Do **not** leftover-slice" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "PROTOCOL-isolated-rankpath-m12.md" in text
    assert PAIR.is_dir()
    assert is_gpt2_name("gpt2") is True
    log = LOG.read_text()
    assert "PROTOCOL-isolated-rankpath-g2m" in log
    assert "named before" in log
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert "PROTOCOL-isolated-rankpath-g2m" in ledger
    howto = (ROOT / "HOW-TO.md").read_text()
    assert "PROTOCOL-isolated-rankpath-g2m" in howto
    exp_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-04-probe-medium-12x4-rankpath-gpt2-lm" in ln
    ]
    assert len(exp_rows) == 1
    research_rows = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if "PROTOCOL-isolated-rankpath-g2m" in ln
    ]
    assert len(research_rows) == 1
    agents_rows = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| GPT-2-small LM on gpt2-medium 12")
    ]
    assert len(agents_rows) == 1
    assert "**25/48**" in agents_rows[0]
    assert "**20/48 vs 32/48**" in agents_rows[0]
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi


def test_protocol_rankpath_g2m_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-01-pair-gpt2-medium-12x4",
            "--model",
            "gpt2",
            "--skip-hashpool",
            "--fit-prefix",
            "4",
            "--pos-bucket",
            "1",
            "--methods",
            "rankpath",
            "--out-dir",
            "experiments/2026-09-04-probe-medium-12x4-rankpath-gpt2-lm",
        ]
    )
    assert args.model == "gpt2"
    assert args.methods == "rankpath"


def test_protocol_rankpath_g2m_medium_native_control_stays() -> None:
    holdout = json.loads((NATIVE / "rankpath" / "holdout.json").read_text())
    assert holdout["used_keys"] is False
    assert holdout["model_name"] == "gpt2-medium"
    assert holdout["n_marked_lr_positive"] == 22
    assert holdout["n_unmarked_lr_nonpositive"] == 30


def test_protocol_rankpath_g2m_from_dumps() -> None:
    interp = json.loads((PROBE / "rankpath" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["used_hash_iv"] is False
    assert interp["used_g_values"] is False
    assert interp["model_name"] == "gpt2"
    assert interp["n_prompts_marked_above"] == 8
    assert interp["n_marked_lr_positive"] == 20
    assert interp["n_unmarked_lr_nonpositive"] == 32
    text = PROTOCOL.read_text()
    assert "H-rpg2m **holds**" in text
    marked = interp["n_marked_lr_positive"]
    unmarked = interp["n_unmarked_lr_nonpositive"]
    assert f"**{marked}/48 vs {unmarked}/48**" in text
    readme = (PROBE / "README.md").read_text()
    assert f"**{marked}/48 vs {unmarked}/48**" in readme
    lo, hi = clopper_pearson(marked, 48)
    assert lo <= 0.5 <= hi
    lo25, hi25 = clopper_pearson(25, 48)
    assert lo25 <= 0.5 <= hi25
