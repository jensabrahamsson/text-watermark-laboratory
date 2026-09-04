"""Aaronson–Kirchner on DistilGPT2 100-family, locked before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-aaronson-distil-100.md"
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
LOG = ROOT / "research" / "LOGBOOK.md"


def test_protocol_aaronson_distil_100_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-aar-d100-ctrl" in text
    assert "H-aar-d100-group" in text
    assert "H-aar-d100-iso" in text
    assert "H-aar-d100-occ" in text
    assert "--mixin aaronson" in text
    assert "--model distilgpt2" in text
    assert "20260905" in text
    assert "2026-09-04-pair-distil-100x4-aaronson" in text
    assert "2026-09-01-prompts-100" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "2290a62682d06624634c1f46a6ad5be0f47f38aa" in text
    assert "314159265" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-aaronson-distil.md" in text
    assert "100/100" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 100
    log = LOG.read_text()
    assert "PROTOCOL-next-aaronson-distil-100" in log
    assert "--mixin aaronson" in log
    assert "--model distilgpt2" in log
    assert "`bf05759`" in log


def test_protocol_aaronson_distil_100_cli_flag_exists() -> None:
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
            "20260905",
            "--mixin",
            "aaronson",
            "--hub-revision",
            "2290a62682d06624634c1f46a6ad5be0f47f38aa",
            "--out-dir",
            "experiments/2026-09-04-pair-distil-100x4-aaronson",
        ]
    )
    assert args.mixin == "aaronson"
    assert args.model == "distilgpt2"
    assert args.seed == 20260905
    assert args.hub_revision == "2290a62682d06624634c1f46a6ad5be0f47f38aa"


PAIR = ROOT / "experiments" / "2026-09-04-pair-distil-100x4-aaronson"
PROBE = ROOT / "experiments" / "2026-09-04-probe-distil-100x4-aaronson-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-04-atoms-distil-100x4-aaronson"


def test_protocol_aaronson_distil_100_official_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["mixin"] == "aaronson"
    assert pair["model_name"] == "distilgpt2"
    assert pair["seed"] == 20260905
    assert pair["hub_revision"] == "2290a62682d06624634c1f46a6ad5be0f47f38aa"
    assert len(pair["rows"]) == 100
    n_first = sum(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    assert n_first == 71
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["n_prompts_marked_above"] == 96
    assert hard["n_prompts_marked_above"] == 91
    assert interp["n_marked_lr_positive"] == 252
    assert interp["n_unmarked_lr_nonpositive"] == 349
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 601
    occ = json.loads((ATOMS / "atoms.json").read_text())
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 28824
    assert occ["n_unseen"] == 61305
    ledger = " ".join((ROOT / "research" / "results-ledger.md").read_text().split())
    w0 = next(w for w in occ["windows"] if w["start"] == 0 and w["end"] == 4)
    assert f"**{occ['n_seen']}** seen vs **{occ['n_unseen']}** unseen" in ledger
    assert f"**{w0['n_seen']}** vs **{w0['n_unseen']}**" in ledger
    n_unmarked = sum(row["unmarked_gen"]["z_score"] > 3.0 for row in pair["rows"])
    assert f"z>3 **{n_unmarked}/100**" in ledger
    assert "H-aar-d100-ctrl **fails**" in text
    assert "H-aar-d100-group **holds**" in text
    assert "H-aar-d100-iso **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **96/100**" in collapsed
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi
