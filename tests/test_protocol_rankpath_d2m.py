"""Distil LM opening rankpath on gpt2-medium 12, locked before LRs."""

import json
from pathlib import Path

import pytest

from text_watermark_tools.generate import is_gpt2_name
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-rankpath-d2m.md"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-12x4"
PROBE = ROOT / "experiments" / "2026-09-04-probe-medium-12x4-rankpath-distil-lm"


def test_protocol_rankpath_d2m_locks_config_before_lrs() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-rpd2m" in text
    assert "H-rpd2m-iso" in text
    assert "H-rpd2m **fails**" in text
    assert "H-rpd2m-iso **holds**" in text
    assert "Do not sell **30/48**" in text
    assert "*(empty until the SHA is named in LOGBOOK.md" not in text
    assert "--model distilgpt2" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "2026-09-04-probe-medium-12x4-rankpath-distil-lm" in text
    assert "Do **not** look at Distil-on-medium rankpath LRs" in text
    assert "Do **not** leftover-slice" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert PAIR.is_dir()
    assert is_gpt2_name("distilgpt2") is True
    log = LOG.read_text()
    assert "PROTOCOL-isolated-rankpath-d2m" in log
    assert "named before" in log
    assert "PROTOCOL-isolated-rankpath-d2m" in (ROOT / "research" / "results-ledger.md").read_text()
    assert "PROTOCOL-isolated-rankpath-d2m" in (ROOT / "HOW-TO.md").read_text()
    exp = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-04-probe-medium-12x4-rankpath-distil-lm" in ln
    ]
    assert len(exp) == 1
    research = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if "PROTOCOL-isolated-rankpath-d2m" in ln
    ]
    assert len(research) == 1
    agents = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| Distil LM on gpt2-medium 12")
    ]
    assert len(agents) == 1
    assert "**25/48**" in agents[0]
    assert "**30/48 vs 31/48**" in agents[0]
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi


def test_protocol_rankpath_d2m_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-01-pair-gpt2-medium-12x4",
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
            "experiments/2026-09-04-probe-medium-12x4-rankpath-distil-lm",
        ]
    )
    assert args.model == "distilgpt2"
    assert args.methods == "rankpath"


def test_protocol_rankpath_d2m_from_dumps() -> None:
    interp = json.loads((PROBE / "rankpath" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["used_hash_iv"] is False
    assert interp["used_g_values"] is False
    assert interp["model_name"] == "distilgpt2"
    assert interp["n_prompts_marked_above"] == 11
    assert interp["n_marked_lr_positive"] == 30
    assert interp["n_unmarked_lr_nonpositive"] == 31
    text = PROTOCOL.read_text()
    assert "H-rpd2m **fails**" in text
    marked = interp["n_marked_lr_positive"]
    unmarked = interp["n_unmarked_lr_nonpositive"]
    assert f"**{marked}/48 vs {unmarked}/48**" in text
    readme = (PROBE / "README.md").read_text()
    assert f"**{marked}/48 vs {unmarked}/48**" in readme
    lo, hi = clopper_pearson(marked, 48)
    assert lo <= 0.5 <= hi
    lo25, hi25 = clopper_pearson(25, 48)
    assert lo25 <= 0.5 <= hi25
