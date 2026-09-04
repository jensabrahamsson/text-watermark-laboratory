"""Kirchenbauer on DistilGPT2, frozen before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-kgw-distil.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-03-pair-distil-12x4-kgw"
PROBE = ROOT / "experiments" / "2026-09-03-probe-distil-12x4-kgw-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-03-atoms-distil-12x4-kgw"


def test_protocol_kgw_distil_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-kgw-d-ctrl" in text
    assert "H-kgw-d-group" in text
    assert "H-kgw-d-iso" in text
    assert "--mixin kgw" in text
    assert "--model distilgpt2" in text
    assert "20260904" in text
    assert "2026-09-03-pair-distil-12x4-kgw" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "H-kgw-d-ctrl **holds**" in text
    assert "PROTOCOL-next-kgw.md" in text
    assert "Aaronson" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    log = LOG.read_text()
    assert "PROTOCOL-next-kgw-distil" in log
    assert "--model distilgpt2" in log
    assert "`1540d3c`" in log


def test_protocol_kgw_distil_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
            "--model",
            "distilgpt2",
            "--n-samples",
            "4",
            "--max-new-tokens",
            "128",
            "--seed",
            "20260904",
            "--mixin",
            "kgw",
            "--out-dir",
            "experiments/2026-09-03-pair-distil-12x4-kgw",
        ]
    )
    assert args.mixin == "kgw"
    assert args.model == "distilgpt2"
    assert args.seed == 20260904


def test_protocol_kgw_distil_official_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["mixin"] == "kgw"
    assert pair["model_name"] == "distilgpt2"
    assert pair["seed"] == 20260904
    assert pair["hub_revision"] is None
    assert len(pair["rows"]) == 12
    assert all(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    assert all(row["unmarked_gen"]["z_score"] <= 3.0 for row in pair["rows"])
    n_first = sum(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    pair_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if ln.startswith("| `2026-09-03-pair-distil-12x4-kgw/`")
    ]
    assert len(pair_rows) == 1
    assert f"**{n_first}/12**" in pair_rows[0]
    pair_readme = (PAIR / "README.md").read_text()
    assert f"**{n_first}/12**" in pair_readme
    assert str(pair["seed"]) in pair_readme
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["n_prompts_marked_above"] == 12
    assert hard["n_prompts_marked_above"] == 11
    assert interp["n_marked_lr_positive"] == 42
    assert interp["n_unmarked_lr_nonpositive"] == 43
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 85
    assert abs(interp["binary"]["auc"] - 0.947) < 0.001
    occ = json.loads((ATOMS / "atoms.json").read_text())
    agents_rows = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| DistilGPT2 Kirchenbauer original-12")
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
        if "2026-09-03-probe-distil-12x4-kgw-hard-last4" in ln
    ]
    assert len(exp_rows) == 1
    assert f"**{interp['n_prompts_marked_above']}/12**" in exp_rows[0]
    assert f"**{ba}/96**" in exp_rows[0]
    assert f"**{hard['n_prompts_marked_above']}/12**" in exp_rows[0]
    probe_readme = (PROBE / "README.md").read_text()
    assert f"**{interp['n_prompts_marked_above']}/12**" in probe_readme
    assert f"**{ba}/96**" in probe_readme
    atoms_readme = (ATOMS / "README.md").read_text()
    assert f"**{occ['n_seen']}**" in atoms_readme
    assert f"**{occ['n_unseen']}**" in atoms_readme
    narrative = (ROOT / "research" / "narrative.md").read_text()
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert f"**{ba}/96**" in narrative
    assert f"**{hard['n_prompts_marked_above']}/12**" in narrative
    assert f"**{occ['n_seen']}**" in narrative
    assert f"**{occ['n_unseen']}**" in narrative
    assert f"**{ba}/96**" in ledger
    assert f"**{hard['n_prompts_marked_above']}/12**" in ledger
    assert f"**{occ['n_seen']}**" in ledger
    atom_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-03-atoms-distil-12x4-kgw" in ln
    ]
    assert len(atom_rows) == 1
    assert f"**{occ['n_seen']}**" in atom_rows[0]
    assert f"**{occ['n_unseen']}**" in atom_rows[0]
    research_rows = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if ln.startswith("| [PROTOCOL-next-kgw-distil.md]")
    ]
    assert len(research_rows) == 1
    assert f"**{ba}/96**" in research_rows[0]
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 130
    assert occ["n_unseen"] == 11972
    assert "H-kgw-d-ctrl **holds**" in text
    assert "H-kgw-d-group **holds**" in text
    assert "H-kgw-d-iso **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **12/12**" in collapsed
    lo, hi = clopper_pearson(12, 12)
    assert lo > 0.5
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert iso_lo <= 0.5 <= iso_hi


PROMPTS_100 = ROOT / "experiments" / "2026-09-01-prompts-100"


def test_protocol_kgw_distil_100_named_before_generation() -> None:
    text = PROTOCOL.read_text()
    log = LOG.read_text()
    assert "H-kgw-d100-ctrl" in text
    assert "H-kgw-d100-group" in text
    assert "H-kgw-d100-iso" in text
    assert "H-kgw-d100-occ" in text
    assert "2026-09-03-pair-distil-100x4-kgw" in text
    assert "2026-09-01-prompts-100" in text
    assert "--hub-revision 2290a62682d06624634c1f46a6ad5be0f47f38aa" in text
    assert "--model distilgpt2" in text
    assert "--mixin kgw" in text
    assert "Do not look at key-free LRs" in text
    assert "25/48" in text
    assert "H-kgw-d100-ctrl" in log
    assert "`4fad227`" in log
    assert "2290a62682d06624634c1f46a6ad5be0f47f38aa" in log
    assert "2026-09-03-pair-distil-100x4-kgw" in log
    assert PROMPTS_100.is_dir()
    assert len(list(PROMPTS_100.glob("*.txt"))) == 100


def test_protocol_kgw_distil_100_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "pair",
            "experiments/2026-09-01-prompts-100",
            "--model",
            "distilgpt2",
            "--n-samples",
            "4",
            "--max-new-tokens",
            "128",
            "--seed",
            "20260904",
            "--mixin",
            "kgw",
            "--hub-revision",
            "2290a62682d06624634c1f46a6ad5be0f47f38aa",
            "--out-dir",
            "experiments/2026-09-03-pair-distil-100x4-kgw",
        ]
    )
    assert args.mixin == "kgw"
    assert args.model == "distilgpt2"
    assert args.seed == 20260904
    assert args.hub_revision == "2290a62682d06624634c1f46a6ad5be0f47f38aa"


PAIR100 = ROOT / "experiments" / "2026-09-03-pair-distil-100x4-kgw"
PROBE100 = ROOT / "experiments" / "2026-09-03-probe-distil-100x4-kgw-hard-last4"
ATOMS100 = ROOT / "experiments" / "2026-09-03-atoms-distil-100x4-kgw"


def test_protocol_kgw_distil_100_official_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR100 / "results.json").read_text())
    assert pair["mixin"] == "kgw"
    assert pair["model_name"] == "distilgpt2"
    assert pair["seed"] == 20260904
    assert pair["hub_revision"] == "2290a62682d06624634c1f46a6ad5be0f47f38aa"
    assert len(pair["rows"]) == 100
    assert all(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    n_first = sum(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    pair_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if ln.startswith("| `2026-09-03-pair-distil-100x4-kgw/`")
    ]
    assert len(pair_rows) == 1
    assert f"**{n_first}/100**" in pair_rows[0]
    pair_readme = (PAIR100 / "README.md").read_text()
    assert f"**{n_first}/100**" in pair_readme
    assert pair["hub_revision"] in pair_readme
    assert str(pair["seed"]) in pair_readme
    narrative = (ROOT / "research" / "narrative.md").read_text()
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert f"**{n_first}/100**" in narrative
    assert f"**{n_first}/100**" in ledger
    n_unmarked_above = sum(row["unmarked_gen"]["z_score"] > 3.0 for row in pair["rows"])
    assert n_unmarked_above == 16
    interp = json.loads((PROBE100 / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE100 / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["n_prompts_marked_above"] == 100
    assert hard["n_prompts_marked_above"] == 82
    assert interp["n_marked_lr_positive"] == 346
    assert interp["n_unmarked_lr_nonpositive"] == 337
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 683
    assert abs(interp["binary"]["auc"] - 0.915) < 0.001
    occ = json.loads((ATOMS100 / "atoms.json").read_text())
    agents_rows = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| DistilGPT2 Kirchenbauer 100-family")
    ]
    assert len(agents_rows) == 1
    row = agents_rows[0]
    ba = interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"]
    assert f"**{interp['n_prompts_marked_above']}/100**" in row
    assert f"**{hard['n_prompts_marked_above']}/100**" in row
    assert f"**{ba}/800**" in row
    assert f"**{occ['n_seen']}**" in row
    exp_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-03-probe-distil-100x4-kgw-hard-last4" in ln
    ]
    assert len(exp_rows) == 1
    assert f"**{interp['n_prompts_marked_above']}/100**" in exp_rows[0]
    assert f"**{ba}/800**" in exp_rows[0]
    assert f"**{hard['n_prompts_marked_above']}/100**" in exp_rows[0]
    probe_readme = (PROBE100 / "README.md").read_text()
    assert f"**{interp['n_prompts_marked_above']}/100**" in probe_readme
    assert f"**{ba}/800**" in probe_readme
    atoms_readme = (ATOMS100 / "README.md").read_text()
    assert f"**{occ['n_seen']}**" in atoms_readme
    assert f"**{occ['n_unseen']}**" in atoms_readme
    narrative = (ROOT / "research" / "narrative.md").read_text()
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert f"**{ba}/800**" in narrative
    assert f"**{hard['n_prompts_marked_above']}/100**" in narrative
    assert f"**{occ['n_seen']}**" in narrative
    assert f"**{occ['n_unseen']}**" in narrative
    assert f"**{ba}/800**" in ledger
    assert f"**{hard['n_prompts_marked_above']}/100**" in ledger
    assert f"**{occ['n_seen']}**" in ledger
    atom_rows = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-03-atoms-distil-100x4-kgw" in ln
    ]
    assert len(atom_rows) == 1
    assert f"**{occ['n_seen']}**" in atom_rows[0]
    assert f"**{occ['n_unseen']}**" in atom_rows[0]
    research_rows = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if ln.startswith("| [PROTOCOL-next-kgw-distil.md]")
    ]
    assert len(research_rows) == 1
    assert f"**{ba}/800**" in research_rows[0]
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 16170
    assert occ["n_unseen"] == 71541
    assert occ["n_marked_lr_positive"] == 346
    assert "H-kgw-d100-ctrl **holds**" in text
    assert "H-kgw-d100-group **holds**" in text
    assert "H-kgw-d100-iso **holds**" in text
    assert "H-kgw-d100-occ **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **100/100**" in collapsed
    lo, hi = clopper_pearson(100, 100)
    assert lo > 0.5
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert iso_lo <= 0.5 <= iso_hi
    ba_lo, ba_hi = clopper_pearson(683, 800)
    assert ba_lo > 0.5
