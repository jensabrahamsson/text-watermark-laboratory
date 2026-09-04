"""Kirchenbauer on Qwen2-1.5B, frozen before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-kgw-qwen.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-03-pair-qwen-12x4-kgw"
PROBE = ROOT / "experiments" / "2026-09-03-probe-qwen-12x4-kgw-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-03-atoms-qwen-12x4-kgw"


def test_protocol_kgw_qwen_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-kgw-q-ctrl" in text
    assert "H-kgw-q-group" in text
    assert "H-kgw-q-iso" in text
    assert "--mixin kgw" in text
    assert "Qwen/Qwen2-1.5B-Instruct" in text
    assert "20260904" in text
    assert "2026-09-03-pair-qwen-12x4-kgw" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "--model Qwen/Qwen2-1.5B-Instruct" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "H-kgw-q-ctrl **holds**" in text
    assert "no chat template" in text
    assert "GPT-2 `WatermarkDetector`" in text or "GPT-2 WatermarkDetector" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    log = LOG.read_text()
    assert "PROTOCOL-next-kgw-qwen" in log
    assert "`45a75c9`" in log


def test_protocol_kgw_qwen_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
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
            "--out-dir",
            "experiments/2026-09-03-pair-qwen-12x4-kgw",
        ]
    )
    assert args.mixin == "kgw"
    assert args.model == "Qwen/Qwen2-1.5B-Instruct"
    assert args.seed == 20260904


def test_protocol_kgw_qwen_official_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["mixin"] == "kgw"
    assert pair["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert pair["seed"] == 20260904
    assert pair["hub_revision"] is None
    assert len(pair["rows"]) == 12
    assert all(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    assert all(row["unmarked_gen"]["z_score"] <= 3.0 for row in pair["rows"])
    n_first = sum(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    pair_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if ln.startswith("| `2026-09-03-pair-qwen-12x4-kgw/`")
    ]
    assert len(pair_rows) == 1
    assert f"**{n_first}/12**" in pair_rows[0]
    pair_readme = (PAIR / "README.md").read_text()
    assert f"**{n_first}/12**" in pair_readme
    assert str(pair["seed"]) in pair_readme
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert interp["n_prompts_marked_above"] == 12
    assert hard["n_prompts_marked_above"] == 8
    assert interp["n_marked_lr_positive"] == 35
    assert interp["n_unmarked_lr_nonpositive"] == 33
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 68
    assert abs(interp["binary"]["auc"] - 0.814) < 0.001
    occ = json.loads((ATOMS / "atoms.json").read_text())
    agents_rows = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| Qwen2-1.5B Kirchenbauer original-12")
    ]
    assert len(agents_rows) == 1
    row = agents_rows[0]
    ba = interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"]
    assert f"**{interp['n_prompts_marked_above']}/12**" in row
    assert f"**{hard['n_prompts_marked_above']}/12**" in row
    assert f"**{ba}/96**" in row
    assert f"**{occ['n_seen']}**" in row
    exp_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-03-probe-qwen-12x4-kgw-hard-last4" in ln
    ]
    assert len(exp_rows) == 1
    assert f"**{interp['n_prompts_marked_above']}/12**" in exp_rows[0]
    assert f"**{ba}/96**" in exp_rows[0]
    assert f"**{hard['n_prompts_marked_above']}/12**" in exp_rows[0]
    probe_readme = (PROBE / "README.md").read_text()
    assert f"**{interp['n_prompts_marked_above']}/12**" in probe_readme
    assert f"**{ba}/96**" in probe_readme
    assert f"**{hard['n_prompts_marked_above']}/12**" in probe_readme
    atoms_readme = (ATOMS / "README.md").read_text()
    assert f"**{occ['n_seen']}**" in atoms_readme
    assert f"**{occ['n_unseen']}**" in atoms_readme
    atom_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-03-atoms-qwen-12x4-kgw" in ln
    ]
    assert len(atom_rows) == 1
    assert f"**{occ['n_seen']}**" in atom_rows[0]
    assert f"**{occ['n_unseen']}**" in atom_rows[0]
    research_rows = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if ln.startswith("| [PROTOCOL-next-kgw-qwen.md]")
    ]
    assert len(research_rows) == 1
    assert f"**{ba}/96**" in research_rows[0]
    assert f"**{hard['n_prompts_marked_above']}/12**" in research_rows[0]
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 84
    assert occ["n_unseen"] == 12108
    assert "H-kgw-q-ctrl **holds**" in text
    assert "H-kgw-q-group **holds**" in text
    assert "H-kgw-q-iso **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **12/12**" in collapsed
    lo, hi = clopper_pearson(8, 12)
    assert lo <= 0.5 <= hi
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert iso_lo <= 0.5 <= iso_hi
