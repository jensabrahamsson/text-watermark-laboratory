"""Qwen2-1.5B ngram_len=13 100-family freeze, locked before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-longctx-qwen-100.md"
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-04-pair-qwen-100x4-ngram13"
PROBE = ROOT / "experiments" / "2026-09-04-probe-qwen-100x4-ngram13-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-04-atoms-qwen-100x4-ngram13"


def test_protocol_longctx_qwen_100_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-long-q100-ctrl" in text
    assert "H-long-q100-group" in text
    assert "H-long-q100-iso" in text
    assert "H-long-q100-occ" in text
    assert "--ngram-len 13" in text
    assert "Qwen/Qwen2-1.5B-Instruct" in text
    assert "20260903" in text
    assert "2026-09-04-pair-qwen-100x4-ngram13" in text
    assert "2026-09-01-prompts-100" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "ba1cf1846d7df0a0591d6c00649f57e798519da8" in text
    assert "detector_mean" in text
    assert "ngram_len=5" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-longctx-qwen.md" in text
    assert "76/100" in text
    assert "88/100" in text
    assert "4/12" in text
    assert "no chat template" in text
    assert "GPT-2 tokenizer" in text
    assert "--model Qwen/Qwen2-1.5B-Instruct" in text
    assert "H-long-q100-ctrl **fails**" in text
    assert "H-long-q100-group **holds**" in text
    assert "H-long-q100-iso **holds**" in text
    assert "H-long-q100-occ **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **76/100**" in collapsed
    assert text.count("## Results") == 1
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 100
    log = LOG.read_text()
    assert "PROTOCOL-next-longctx-qwen-100" in log
    assert "--model Qwen/Qwen2-1.5B-Instruct" in log
    assert "--ngram-len 13" in log
    assert "`636765c`" in log
    assert "**76/100**" in log
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert "PROTOCOL-next-longctx-qwen-100" in ledger
    assert "`636765c`" in ledger
    assert "**474/800**" in ledger


def test_protocol_longctx_qwen_100_cli_flag_exists() -> None:
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
            "20260903",
            "--ngram-len",
            "13",
            "--hub-revision",
            "ba1cf1846d7df0a0591d6c00649f57e798519da8",
            "--out-dir",
            "experiments/2026-09-04-pair-qwen-100x4-ngram13",
        ]
    )
    assert args.model == "Qwen/Qwen2-1.5B-Instruct"
    assert args.ngram_len == 13
    assert args.seed == 20260903
    assert args.hub_revision == "ba1cf1846d7df0a0591d6c00649f57e798519da8"

    probe = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-04-pair-qwen-100x4-ngram13",
            "--model",
            "Qwen/Qwen2-1.5B-Instruct",
            "--methods",
            "hard,interpolate",
            "--context-len",
            "4",
            "--skip-hashpool",
            "--out-dir",
            "experiments/2026-09-04-probe-qwen-100x4-ngram13-hard-last4",
        ]
    )
    assert probe.model == "Qwen/Qwen2-1.5B-Instruct"
    assert probe.skip_hashpool is True


def test_protocol_longctx_qwen_100_official_and_keyfree_from_dumps() -> None:
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["ngram_len"] == 13
    assert pair["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert pair["seed"] == 20260903
    assert pair["hub_revision"] == "ba1cf1846d7df0a0591d6c00649f57e798519da8"
    assert pair["instance"] == "public-deepmind-30"
    assert len(pair["rows"]) == 100
    n_first = sum(row["marked"]["mean"] > 0.55 for row in pair["rows"])
    assert n_first == 91
    assert all(row["unmarked_gen"]["mean"] <= 0.55 for row in pair["rows"])
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert interp["n_prompts_marked_above"] == 76
    assert hard["n_prompts_marked_above"] == 74
    assert interp["n_marked_lr_positive"] == 273
    assert interp["n_unmarked_lr_nonpositive"] == 201
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 474
    occ = json.loads((ATOMS / "atoms.json").read_text())
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 3535
    assert occ["n_unseen"] == 98064
    assert occ["n_marked_lr_positive"] == 273
    ledger = " ".join((ROOT / "research" / "results-ledger.md").read_text().split())
    w0 = next(w for w in occ["windows"] if w["start"] == 0 and w["end"] == 4)
    assert f"**{occ['n_seen']}** seen vs **{occ['n_unseen']}** unseen" in ledger
    assert f"**{w0['n_seen']}** vs **{w0['n_unseen']}**" in ledger
    research = (ROOT / "research" / "README.md").read_text()
    row = next(
        ln
        for ln in research.splitlines()
        if "PROTOCOL-next-longctx-qwen-100.md" in ln
    )
    assert f"**{occ['n_seen']}** vs **{occ['n_unseen']}**" in row
    assert (
        f"**{interp['n_marked_lr_positive']}/400 vs {interp['n_unmarked_lr_nonpositive']}/400**"
        in ledger
    )
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi
