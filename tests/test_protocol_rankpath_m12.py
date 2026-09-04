"""gpt2-medium native opening rankpath 12-LOO, locked before LRs."""

import json
from pathlib import Path

import pytest

from text_watermark_tools.generate import is_gpt2_name
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-rankpath-m12.md"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-12x4"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
DISTIL_NATIVE = (
    ROOT / "experiments" / "2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath"
)
PROBE = ROOT / "experiments" / "2026-09-04-probe-medium-12x4-rankpath-native"


def test_protocol_rankpath_m12_locks_config_before_lrs() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-rpm12" in text
    assert "H-rpm12-iso" in text
    assert "H-rpm12 **holds**" in text
    assert "H-rpm12-iso **holds**" in text
    assert "Do not sell **22/48**" in text
    assert "*(empty until the SHA is named in LOGBOOK.md" not in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "--model gpt2-medium" in text
    assert "--skip-hashpool" in text
    assert "2026-09-01-pair-gpt2-medium-12x4" in text
    assert "2026-09-04-probe-medium-12x4-rankpath-native" in text
    assert "Do **not** look at gpt2-medium native rankpath LRs" in text
    assert "Do **not** leftover-slice" in text
    assert "Do **not** merge GitHub PR **#9**" in text
    assert "Do **not** pass `--rankpath`" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "leftover-15" in text
    assert "PROTOCOL-isolated-m12.md" in text
    assert "PROTOCOL-isolated-rankpath-lm.md" in text
    assert PAIR.is_dir()
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    assert DISTIL_NATIVE.is_dir()
    assert is_gpt2_name("gpt2-medium") is True
    log = LOG.read_text()
    assert "PROTOCOL-isolated-rankpath-m12" in log
    assert "named before" in log
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert "PROTOCOL-isolated-rankpath-m12" in ledger
    assert "named before" in ledger
    narrative = (ROOT / "research" / "narrative.md").read_text()
    assert "PROTOCOL-isolated-rankpath-m12" in narrative
    agents_rows = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| gpt2-medium native opening rankpath")
    ]
    assert len(agents_rows) == 1
    assert "**25/48**" in agents_rows[0]
    assert "**22/48 vs 30/48**" in agents_rows[0]
    howto = (ROOT / "HOW-TO.md").read_text()
    assert "PROTOCOL-isolated-rankpath-m12" in howto
    exp_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-04-probe-medium-12x4-rankpath-native" in ln
    ]
    assert len(exp_rows) == 1
    assert "**22/48 vs 30/48**" in exp_rows[0]
    research_rows = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if "PROTOCOL-isolated-rankpath-m12.md" in ln
        and "m12body" not in ln
    ]
    assert len(research_rows) == 1
    assert "**22/48 vs 30/48**" in research_rows[0]
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi


def test_protocol_rankpath_m12_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-01-pair-gpt2-medium-12x4",
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
            "experiments/2026-09-04-probe-medium-12x4-rankpath-native",
        ]
    )
    assert args.model == "gpt2-medium"
    assert args.skip_hashpool is True
    assert args.fit_prefix == 4
    assert args.methods == "rankpath"


def test_protocol_rankpath_m12_distil_native_control_stays() -> None:
    holdout = json.loads((DISTIL_NATIVE / "rankpath" / "holdout.json").read_text())
    assert holdout["used_keys"] is False
    assert holdout["model_name"] == "distilgpt2"
    assert holdout["n_prompts_marked_above"] == 8
    assert holdout["n_marked_lr_positive"] == 28
    assert holdout["n_unmarked_lr_nonpositive"] == 32


def test_protocol_rankpath_m12_from_dumps() -> None:
    interp = json.loads((PROBE / "rankpath" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["used_hash_iv"] is False
    assert interp["used_g_values"] is False
    assert interp["model_name"] == "gpt2-medium"
    assert interp["n_prompts_marked_above"] == 6
    assert interp["n_marked_lr_positive"] == 22
    assert interp["n_unmarked_lr_nonpositive"] == 30
    text = PROTOCOL.read_text()
    assert "H-rpm12 **holds**" in text
    marked = interp["n_marked_lr_positive"]
    unmarked = interp["n_unmarked_lr_nonpositive"]
    assert f"**{marked}/48 vs {unmarked}/48**" in text
    readme = (PROBE / "README.md").read_text()
    assert f"**{marked}/48 vs {unmarked}/48**" in readme
    lo, hi = clopper_pearson(marked, 48)
    assert lo <= 0.5 <= hi
    lo25, hi25 = clopper_pearson(25, 48)
    assert lo25 <= 0.5 <= hi25
