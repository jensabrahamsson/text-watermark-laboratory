"""GPT-2-small LM opening rankpath on Distil 12, locked before LRs."""

import json
from pathlib import Path

import pytest

from text_watermark_tools.generate import is_gpt2_name
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-rankpath-g2d.md"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-08-31-pair-distilgpt2-12x4"
NATIVE = ROOT / "experiments" / "2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath"
PROBE = ROOT / "experiments" / "2026-09-04-probe-distil-12x4-rankpath-gpt2-lm"


def test_protocol_rankpath_g2d_locks_config_before_lrs() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-rpg2d" in text
    assert "H-rpg2d-iso" in text
    assert "--model gpt2" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "2026-08-31-pair-distilgpt2-12x4" in text
    assert "2026-09-04-probe-distil-12x4-rankpath-gpt2-lm" in text
    assert "Do **not** look at GPT-2-small-on-Distil rankpath LRs" in text
    assert "Do **not** leftover-slice" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert PAIR.is_dir()
    assert is_gpt2_name("gpt2") is True
    log = LOG.read_text()
    assert "PROTOCOL-isolated-rankpath-g2d" in log
    assert "named before" in log
    assert "PROTOCOL-isolated-rankpath-g2d" in (ROOT / "research" / "results-ledger.md").read_text()
    assert "PROTOCOL-isolated-rankpath-g2d" in (ROOT / "HOW-TO.md").read_text()
    exp = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-04-probe-distil-12x4-rankpath-gpt2-lm" in ln
    ]
    assert len(exp) == 1
    research = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if "PROTOCOL-isolated-rankpath-g2d" in ln
    ]
    assert len(research) == 1
    agents = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| GPT-2-small LM on Distil 12")
    ]
    assert len(agents) == 1
    assert "**25/48**" in agents[0]
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi


def test_protocol_rankpath_g2d_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-08-31-pair-distilgpt2-12x4",
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
            "experiments/2026-09-04-probe-distil-12x4-rankpath-gpt2-lm",
        ]
    )
    assert args.model == "gpt2"
    assert args.methods == "rankpath"


def test_protocol_rankpath_g2d_distil_native_control_stays() -> None:
    holdout = json.loads((NATIVE / "rankpath" / "holdout.json").read_text())
    assert holdout["used_keys"] is False
    assert holdout["model_name"] == "distilgpt2"
    assert holdout["n_marked_lr_positive"] == 28
    assert holdout["n_unmarked_lr_nonpositive"] == 32


@pytest.mark.skipif(
    not (PROBE / "rankpath" / "holdout.json").is_file(),
    reason="GPT-2-on-Distil rankpath not run",
)
def test_protocol_rankpath_g2d_from_dumps() -> None:
    interp = json.loads((PROBE / "rankpath" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["model_name"] == "gpt2"
    text = PROTOCOL.read_text()
    if "H-rpg2d **holds**" not in text and "H-rpg2d **fails**" not in text:
        pytest.skip("not folded yet")
    marked = interp["n_marked_lr_positive"]
    unmarked = interp["n_unmarked_lr_nonpositive"]
    assert f"**{marked}/48 vs {unmarked}/48**" in text
    lo25, hi25 = clopper_pearson(25, 48)
    assert lo25 <= 0.5 <= hi25
