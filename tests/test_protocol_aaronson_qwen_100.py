"""Aaronson–Kirchner on Qwen2-1.5B 100-family, locked before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-aaronson-qwen-100.md"
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-04-pair-qwen-100x4-aaronson"
PROBE = ROOT / "experiments" / "2026-09-04-probe-qwen-100x4-aaronson-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-04-atoms-qwen-100x4-aaronson"


def test_protocol_aaronson_qwen_100_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-aar-q100-ctrl" in text
    assert "H-aar-q100-group" in text
    assert "H-aar-q100-iso" in text
    assert "H-aar-q100-occ" in text
    assert "--mixin aaronson" in text
    assert "Qwen/Qwen2-1.5B-Instruct" in text
    assert "20260905" in text
    assert "2026-09-04-pair-qwen-100x4-aaronson" in text
    assert "2026-09-01-prompts-100" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "ba1cf1846d7df0a0591d6c00649f57e798519da8" in text
    assert "314159265" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-aaronson-qwen.md" in text
    assert "100/100" in text
    assert "96/100" in text
    assert "no chat template" in text
    assert "GPT-2 tokenizer" in text
    assert "--model Qwen/Qwen2-1.5B-Instruct" in text
    assert "H-aar-q100-ctrl **fails**" in text
    assert "H-aar-q100-group **holds**" in text
    assert "H-aar-q100-iso **holds**" in text
    assert "H-aar-q100-occ **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **100/100**" in collapsed
    assert text.count("## Results") == 1
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 100
    log = LOG.read_text()
    assert "PROTOCOL-next-aaronson-qwen-100" in log
    assert "--mixin aaronson" in log
    assert "--model Qwen/Qwen2-1.5B-Instruct" in log
    assert "`a761a7d`" in log
    assert "**100/100**" in log
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert "PROTOCOL-next-aaronson-qwen-100" in ledger
    assert "`a761a7d`" in ledger
    assert "**616/800**" in ledger


def test_protocol_aaronson_qwen_100_cli_flag_exists() -> None:
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
            "20260905",
            "--mixin",
            "aaronson",
            "--hub-revision",
            "ba1cf1846d7df0a0591d6c00649f57e798519da8",
            "--out-dir",
            "experiments/2026-09-04-pair-qwen-100x4-aaronson",
        ]
    )
    assert args.mixin == "aaronson"
    assert args.model == "Qwen/Qwen2-1.5B-Instruct"
    assert args.seed == 20260905
    assert args.hub_revision == "ba1cf1846d7df0a0591d6c00649f57e798519da8"

    probe = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-04-pair-qwen-100x4-aaronson",
            "--model",
            "Qwen/Qwen2-1.5B-Instruct",
            "--methods",
            "hard,interpolate",
            "--context-len",
            "4",
            "--skip-hashpool",
            "--out-dir",
            "experiments/2026-09-04-probe-qwen-100x4-aaronson-hard-last4",
        ]
    )
    assert probe.model == "Qwen/Qwen2-1.5B-Instruct"
    assert probe.skip_hashpool is True


def test_protocol_aaronson_qwen_100_official_and_keyfree_from_dumps() -> None:
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["mixin"] == "aaronson"
    assert pair["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert pair["seed"] == 20260905
    assert pair["hub_revision"] == "ba1cf1846d7df0a0591d6c00649f57e798519da8"
    assert pair["aaronson"]["hashing_key"] == 314159265
    assert pair["aaronson"]["context_width"] == 1
    assert len(pair["rows"]) == 100
    n_first = sum(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    assert n_first == 99
    assert all(row["unmarked_gen"]["z_score"] <= 3.0 for row in pair["rows"])
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert interp["n_prompts_marked_above"] == 100
    assert hard["n_prompts_marked_above"] == 97
    assert interp["n_marked_lr_positive"] == 216
    assert interp["n_unmarked_lr_nonpositive"] == 400
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 616
    occ = json.loads((ATOMS / "atoms.json").read_text())
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 8750
    assert occ["n_unseen"] == 92842
    assert occ["n_marked_lr_positive"] == 216
    ledger = " ".join((ROOT / "research" / "results-ledger.md").read_text().split())
    w0 = next(w for w in occ["windows"] if w["start"] == 0 and w["end"] == 4)
    assert f"**{occ['n_seen']}** seen vs **{occ['n_unseen']}** unseen" in ledger
    assert f"**{w0['n_seen']}** vs **{w0['n_unseen']}**" in ledger
    research = (ROOT / "research" / "README.md").read_text()
    row = next(
        ln
        for ln in research.splitlines()
        if "PROTOCOL-next-aaronson-qwen-100.md" in ln
    )
    assert f"**{occ['n_seen']}** vs **{occ['n_unseen']}**" in row
    assert (
        f"**{interp['n_marked_lr_positive']}/400 vs {interp['n_unmarked_lr_nonpositive']}/400**"
        in ledger
    )
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi
    lo_iso, hi_iso = clopper_pearson(216, 400)
    assert lo_iso <= 0.5 <= hi_iso
