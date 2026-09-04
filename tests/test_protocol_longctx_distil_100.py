"""DistilGPT2 ngram_len=13 100-family freeze, locked before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-longctx-distil-100.md"
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
LOG = ROOT / "research" / "LOGBOOK.md"


def test_protocol_longctx_distil_100_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-long-d100-ctrl" in text
    assert "H-long-d100-group" in text
    assert "H-long-d100-iso" in text
    assert "H-long-d100-occ" in text
    assert "--ngram-len 13" in text
    assert "--model distilgpt2" in text
    assert "20260903" in text
    assert "2026-09-04-pair-distil-100x4-ngram13" in text
    assert "2026-09-01-prompts-100" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "2290a62682d06624634c1f46a6ad5be0f47f38aa" in text
    assert "detector_mean" in text
    assert "ngram_len=5" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-longctx-distil.md" in text
    assert "76/100" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 100
    log = LOG.read_text()
    assert "PROTOCOL-next-longctx-distil-100" in log
    assert "--model distilgpt2" in log
    assert "--ngram-len 13" in log
    assert "`d891622`" in log


def test_protocol_longctx_distil_100_cli_flag_exists() -> None:
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
            "20260903",
            "--ngram-len",
            "13",
            "--hub-revision",
            "2290a62682d06624634c1f46a6ad5be0f47f38aa",
            "--out-dir",
            "experiments/2026-09-04-pair-distil-100x4-ngram13",
        ]
    )
    assert args.model == "distilgpt2"
    assert args.ngram_len == 13
    assert args.seed == 20260903
    assert args.hub_revision == "2290a62682d06624634c1f46a6ad5be0f47f38aa"


PAIR = ROOT / "experiments" / "2026-09-04-pair-distil-100x4-ngram13"
PROBE = ROOT / "experiments" / "2026-09-04-probe-distil-100x4-ngram13-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-04-atoms-distil-100x4-ngram13"


def test_protocol_longctx_distil_100_official_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["ngram_len"] == 13
    assert pair["model_name"] == "distilgpt2"
    assert pair["seed"] == 20260903
    assert pair["hub_revision"] == "2290a62682d06624634c1f46a6ad5be0f47f38aa"
    assert len(pair["rows"]) == 100
    n_first = sum(row["marked"]["mean"] > 0.55 for row in pair["rows"])
    assert n_first == 98
    assert all(row["unmarked_gen"]["mean"] <= 0.55 for row in pair["rows"])
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["n_prompts_marked_above"] == 88
    assert hard["n_prompts_marked_above"] == 89
    assert interp["n_marked_lr_positive"] == 325
    assert interp["n_unmarked_lr_nonpositive"] == 232
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 557
    occ = json.loads((ATOMS / "atoms.json").read_text())
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 11182
    assert occ["n_unseen"] == 85493
    assert "H-long-d100-ctrl **fails**" in text
    assert "H-long-d100-group **holds**" in text
    assert "H-long-d100-iso **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **88/100**" in collapsed
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi
