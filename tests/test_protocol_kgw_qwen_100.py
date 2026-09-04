"""Kirchenbauer on Qwen2-1.5B 100-family, locked before generation."""

import json
from pathlib import Path

import pytest

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-kgw-qwen-100.md"
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-04-pair-qwen-100x4-kgw"
PROBE = ROOT / "experiments" / "2026-09-04-probe-qwen-100x4-kgw-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-04-atoms-qwen-100x4-kgw"


def test_protocol_kgw_qwen_100_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-kgw-q100-ctrl" in text
    assert "H-kgw-q100-group" in text
    assert "H-kgw-q100-iso" in text
    assert "H-kgw-q100-occ" in text
    assert "--mixin kgw" in text
    assert "Qwen/Qwen2-1.5B-Instruct" in text
    assert "20260904" in text
    assert "2026-09-04-pair-qwen-100x4-kgw" in text
    assert "2026-09-01-prompts-100" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "ba1cf1846d7df0a0591d6c00649f57e798519da8" in text
    assert "15485863" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-kgw-qwen.md" in text
    assert "100/100" in text
    assert "683/800" in text
    assert "no chat template" in text
    assert "GPT-2 tokenizer" in text
    assert "--model Qwen/Qwen2-1.5B-Instruct" in text
    assert "H-kgw-q100-ctrl **holds**" not in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 100
    log = LOG.read_text()
    assert "PROTOCOL-next-kgw-qwen-100" in log
    assert "--mixin kgw" in log
    assert "--model Qwen/Qwen2-1.5B-Instruct" in log
    assert "`ed9fb20`" in log
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert "PROTOCOL-next-kgw-qwen-100" in ledger
    assert "`ed9fb20`" in ledger
    assert "named before generation" in ledger
    narrative = (ROOT / "research" / "narrative.md").read_text()
    assert "PROTOCOL-next-kgw-qwen-100" in narrative
    assert "`ed9fb20`" in narrative
    assert "named before generation" in narrative
    agents_rows = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| Qwen2-1.5B Kirchenbauer 100-family")
    ]
    assert len(agents_rows) == 1
    row = agents_rows[0]
    assert "`ed9fb20`" in row
    assert "named before generation" in row
    assert "**25/48**" in row
    assert "100/100" not in row
    assert "/800" not in row
    howto = (ROOT / "HOW-TO.md").read_text()
    assert "PROTOCOL-next-kgw-qwen-100" in howto
    assert "`ed9fb20`" in howto
    assert "Do not invent those scores" in howto
    exp_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-04-pair-qwen-100x4-kgw" in ln
    ]
    assert len(exp_rows) == 1
    assert "`ed9fb20`" in exp_rows[0]
    assert "named before generation" in exp_rows[0]
    assert "100/100" not in exp_rows[0]
    research_rows = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if "PROTOCOL-next-kgw-qwen-100" in ln
    ]
    assert len(research_rows) == 1
    assert "`ed9fb20`" in research_rows[0]
    assert "named before generation" in research_rows[0]
    assert "100/100" not in research_rows[0]


def test_protocol_kgw_qwen_100_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "pair",
            "experiments/2026-09-01-prompts-100",
            "--model",
            "Qwen/Qwen2-1.5B-Instruct",
            "--n-samples",
            "4",
            "--max-new-tokens",
            "128",
            "--seed",
            "20260904",
            "--mixin",
            "kgw",
            "--hub-revision",
            "ba1cf1846d7df0a0591d6c00649f57e798519da8",
            "--out-dir",
            "experiments/2026-09-04-pair-qwen-100x4-kgw",
        ]
    )
    assert args.mixin == "kgw"
    assert args.model == "Qwen/Qwen2-1.5B-Instruct"
    assert args.seed == 20260904
    assert args.hub_revision == "ba1cf1846d7df0a0591d6c00649f57e798519da8"

    probe = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-04-pair-qwen-100x4-kgw",
            "--model",
            "Qwen/Qwen2-1.5B-Instruct",
            "--methods",
            "hard,interpolate",
            "--context-len",
            "4",
            "--skip-hashpool",
            "--out-dir",
            "experiments/2026-09-04-probe-qwen-100x4-kgw-hard-last4",
        ]
    )
    assert probe.model == "Qwen/Qwen2-1.5B-Instruct"
    assert probe.skip_hashpool is True


@pytest.mark.skipif(
    not (PAIR / "results.json").is_file(),
    reason="Qwen Kirchenbauer 100-family pair still generating",
)
def test_protocol_kgw_qwen_100_official_from_dumps() -> None:
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["mixin"] == "kgw"
    assert pair["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert pair["seed"] == 20260904
    assert pair["hub_revision"] == "ba1cf1846d7df0a0591d6c00649f57e798519da8"
    assert pair["kgw"]["hashing_key"] == 15485863
    assert pair["kgw"]["greenlist_ratio"] == 0.25
    assert pair["kgw"]["bias"] == 2.0
    assert pair["kgw"]["seeding_scheme"] == "lefthash"
    assert pair["kgw"]["context_width"] == 1
    assert pair["kgw"]["z_threshold"] == 3.0
    assert len(pair["rows"]) == 100
    n_first = sum(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    n_unmarked = sum(row["unmarked_gen"]["z_score"] > 3.0 for row in pair["rows"])
    text = PROTOCOL.read_text()
    log = LOG.read_text()
    if "H-kgw-q100-ctrl **holds**" not in text:
        pytest.skip("official first-draw not folded yet")
    assert f"**{n_first}/100**" in text
    assert f"**{n_first}/100**" in log
    assert n_unmarked < 100


@pytest.mark.skipif(
    not (PROBE / "interpolate" / "holdout.json").is_file(),
    reason="frozen probe not run",
)
def test_protocol_kgw_qwen_100_keyfree_from_dumps() -> None:
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert hard["used_keys"] is False
    assert interp["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    text = PROTOCOL.read_text()
    if "H-kgw-q100-group **holds**" not in text:
        pytest.skip("key-free two-grain counts not folded yet")
    wins = interp["n_prompts_marked_above"]
    hard_wins = hard["n_prompts_marked_above"]
    marked = interp["n_marked_lr_positive"]
    unmarked = interp["n_unmarked_lr_nonpositive"]
    ba = marked + unmarked
    assert f"**{wins}/100**" in text
    assert f"**{hard_wins}/100**" in text
    assert f"**{ba}/800**" in text
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi
    if (ATOMS / "atoms.json").is_file():
        occ = json.loads((ATOMS / "atoms.json").read_text())
        assert occ["used_keys"] is False
        assert occ["n_marked_lr_positive"] == marked
