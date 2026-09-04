"""Kirchenbauer green-list two-grain freeze, locked before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-kgw.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-03-pair-12x4-kgw"
PROBE = ROOT / "experiments" / "2026-09-03-probe-12x4-kgw-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-03-atoms-12x4-kgw"
PAIR100 = ROOT / "experiments" / "2026-09-03-pair-100x4-kgw"
PROBE100 = ROOT / "experiments" / "2026-09-03-probe-100x4-kgw-hard-last4"
ATOMS100 = ROOT / "experiments" / "2026-09-03-atoms-100x4-kgw"


def test_protocol_kgw_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-kgw-ctrl" in text
    assert "H-kgw-group" in text
    assert "H-kgw-hard" in text
    assert "H-kgw-iso" in text
    assert "H-kgw-occ" in text
    assert "--mixin kgw" in text
    assert "20260904" in text
    assert "2026-08-17-grok-prompts" in text
    assert "2026-09-03-pair-12x4-kgw" in text
    assert "2026-09-03-probe-12x4-kgw-hard-last4" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "--skip-hashpool" in text
    assert "--n-samples 4" in text
    assert "leave-one-family-out" in text
    assert "greenlist_ratio" in text
    assert "**0.25**" in text
    assert "**2.0**" in text
    assert "**15485863**" in text
    assert "lefthash" in text
    assert "context_width" in text
    assert "z_threshold" in text
    assert "607a30d783dfa663caf39e06633721c8d4cfcd7e" in text
    assert "detector_mean" in text
    assert "synthid-text" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "Named here before generation" in text
    assert "Aaronson" in text
    assert "PROTOCOL-next-longctx" in text
    assert "not unique to tournament" in text or "not unique to tournament sampling" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    log = LOG.read_text()
    assert "PROTOCOL-next-kgw" in log
    assert "--mixin kgw" in log
    assert "`8371406`" in log


def test_protocol_kgw_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
            "--n-samples",
            "4",
            "--max-new-tokens",
            "128",
            "--seed",
            "20260904",
            "--mixin",
            "kgw",
            "--hub-revision",
            "607a30d783dfa663caf39e06633721c8d4cfcd7e",
            "--out-dir",
            "experiments/2026-09-03-pair-12x4-kgw",
        ]
    )
    assert args.mixin == "kgw"
    assert args.n_samples == 4
    assert args.seed == 20260904
    assert args.hub_revision == "607a30d783dfa663caf39e06633721c8d4cfcd7e"
    assert args.ngram_len == 5


def test_protocol_kgw_refuses_synthid_only_flags() -> None:
    from text_watermark_tools.cli import build_parser, cmd_pair

    parser = build_parser()
    ngram = parser.parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
            "--mixin",
            "kgw",
            "--ngram-len",
            "13",
        ]
    )
    assert cmd_pair(ngram) == 2
    ctrl = parser.parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
            "--mixin",
            "kgw",
            "--control-only",
        ]
    )
    assert cmd_pair(ctrl) == 2


def test_protocol_kgw_official_control_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    probe = json.loads((PROBE / "results.json").read_text())
    assert pair["mixin"] == "kgw"
    assert pair["instance"] == "kirchenbauer-hf-default"
    assert pair["seed"] == 20260904
    assert pair["hub_revision"] == "607a30d783dfa663caf39e06633721c8d4cfcd7e"
    assert pair["kgw"]["greenlist_ratio"] == 0.25
    assert pair["kgw"]["bias"] == 2.0
    assert pair["kgw"]["hashing_key"] == 15485863
    assert pair["kgw"]["seeding_scheme"] == "lefthash"
    assert pair["kgw"]["context_width"] == 1
    assert pair["kgw"]["z_threshold"] == 3.0
    assert len(pair["rows"]) == 12
    for row in pair["rows"]:
        assert row["marked"]["z_score"] > 3.0
        assert row["unmarked_gen"]["z_score"] <= 3.0
        assert row["marked"]["n_tokens"] == 128
    assert min(row["marked"]["z_score"] for row in pair["rows"]) > 8.4
    assert max(row["unmarked_gen"]["z_score"] for row in pair["rows"]) < 2.2
    assert probe["used_keys"] is False
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    assert hard["used_keys"] is False
    assert interp["used_keys"] is False
    assert hard["n_prompts_marked_above"] == 12
    assert interp["n_prompts_marked_above"] == 12
    assert hard["n_prompt_ties"] == 0
    assert interp["n_prompt_ties"] == 0
    assert interp["n_marked_lr_positive"] == 44
    assert interp["n_unmarked_lr_nonpositive"] == 41
    assert hard["n_marked_lr_positive"] == 35
    assert hard["n_unmarked_lr_nonpositive"] == 25
    assert abs(interp["binary"]["auc"] - 0.947) < 0.001
    assert abs(hard["binary"]["auc"] - 0.703) < 0.001
    assert abs(interp["binary"]["mean_diff"] - 0.437) < 0.001
    assert abs(hard["binary"]["mean_diff"] - 0.070) < 0.001
    lo, hi = clopper_pearson(12, 12)
    assert lo > 0.5
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert iso_lo <= 0.5 <= iso_hi
    ba_lo, ba_hi = clopper_pearson(85, 96)
    assert ba_lo > 0.5
    occ = json.loads((ATOMS / "atoms.json").read_text())
    agents_rows = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| GPT-2 Kirchenbauer original-12")
    ]
    assert len(agents_rows) == 1
    row = agents_rows[0]
    ba = interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"]
    assert f"**{interp['n_prompts_marked_above']}/12**" in row
    assert f"**{hard['n_prompts_marked_above']}/12**" in row
    assert f"**{ba}/96**" in row
    assert f"**{occ['n_seen']}**" in row
    assert "H-kgw-ctrl **holds**" in text
    assert "H-kgw-group **holds**" in text
    assert "H-kgw-hard **holds**" in text
    assert "H-kgw-iso **holds**" in text
    assert "H-kgw-occ **holds**" in text
    assert "**12/12**" in text
    assert "**85/96**" in text
    assert "**114**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **12/12**" in collapsed
    assert "Not opened. Do not fill this section" not in text
    occ = json.loads((ATOMS / "atoms.json").read_text())
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 114
    assert occ["n_unseen"] == 12071
    assert occ["n_marked_lr_positive"] == 44
    assert occ["windows"][0]["n_seen"] == 40
    assert occ["windows"][0]["n_unseen"] == 248
    log = LOG.read_text()
    assert "`8371406`" in log
    assert "09e40d4" in log
    assert "2026-09-03-pair-100x4-kgw" in log
    assert "H-kgw-B-ctrl" in log
    assert "H-kgw-B-group" in log
    assert "H-kgw-B-iso" in log


def test_protocol_kgw_100_family_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR100 / "results.json").read_text())
    assert pair["mixin"] == "kgw"
    assert pair["seed"] == 20260904
    assert pair["hub_revision"] == "607a30d783dfa663caf39e06633721c8d4cfcd7e"
    assert len(pair["rows"]) == 100
    assert all(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    assert sum(row["unmarked_gen"]["z_score"] > 3.0 for row in pair["rows"]) == 1
    interp = json.loads((PROBE100 / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE100 / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["n_prompts_marked_above"] == 100
    assert hard["n_prompts_marked_above"] == 62
    assert interp["n_marked_lr_positive"] == 376
    assert interp["n_unmarked_lr_nonpositive"] == 371
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 747
    assert abs(interp["binary"]["auc"] - 0.982) < 0.001
    assert abs(interp["binary"]["mean_diff"] - 0.745) < 0.001
    occ = json.loads((ATOMS100 / "atoms.json").read_text())
    agents = (ROOT / "AGENTS.md").read_text()
    assert f"**{interp['n_prompts_marked_above']}/100**" in agents
    assert f"**{hard['n_prompts_marked_above']}/100**" in agents
    assert (
        f"**{interp['n_marked_lr_positive'] + interp['n_unmarked_lr_nonpositive']}/800**"
        in agents
    )
    assert f"**{occ['n_seen']}**" in agents
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 4557
    assert occ["n_unseen"] == 96991
    assert occ["windows"][0]["n_seen"] == 1044
    assert "H-kgw-B-ctrl **holds**" in text
    assert "H-kgw-B-group **holds**" in text
    assert "H-kgw-B-iso **holds**" in text
    assert "**100/100**" in text
    assert "**747/800**" in text
    assert "**4557**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **100/100**" in collapsed
    lo, hi = clopper_pearson(100, 100)
    assert lo > 0.5


def test_protocol_kgw_pair_does_not_store_synthid_means() -> None:
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["instance"] != "public-deepmind-30"
    assert "detector_mean" in pair["note"]
    for row in pair["rows"]:
        assert "z_score" in row["marked"]
        assert "green_fraction" in row["marked"]
