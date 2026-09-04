"""Aaronson–Kirchner on Qwen2-1.5B, locked before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-aaronson-qwen.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"


def test_protocol_aaronson_qwen_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-aar-q-ctrl" in text
    assert "H-aar-q-group" in text
    assert "H-aar-q-iso" in text
    assert "H-aar-q-occ" in text
    assert "--mixin aaronson" in text
    assert "Qwen/Qwen2-1.5B-Instruct" in text
    assert "20260905" in text
    assert "2026-09-04-pair-qwen-12x4-aaronson" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "ba1cf1846d7df0a0591d6c00649f57e798519da8" in text
    assert "314159265" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-aaronson.md" in text
    assert "no chat template" in text
    assert "GPT-2 tokenizer" in text
    assert "--model Qwen/Qwen2-1.5B-Instruct" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    log = LOG.read_text()
    assert "PROTOCOL-next-aaronson-qwen" in log
    assert "--mixin aaronson" in log
    assert "--model Qwen/Qwen2-1.5B-Instruct" in log
    assert "`1171d5c`" in log


def test_protocol_aaronson_qwen_cli_flag_exists() -> None:
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
            "20260905",
            "--mixin",
            "aaronson",
            "--hub-revision",
            "ba1cf1846d7df0a0591d6c00649f57e798519da8",
            "--out-dir",
            "experiments/2026-09-04-pair-qwen-12x4-aaronson",
        ]
    )
    assert args.mixin == "aaronson"
    assert args.model == "Qwen/Qwen2-1.5B-Instruct"
    assert args.seed == 20260905
    assert args.hub_revision == "ba1cf1846d7df0a0591d6c00649f57e798519da8"

    probe = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-04-pair-qwen-12x4-aaronson",
            "--model",
            "Qwen/Qwen2-1.5B-Instruct",
            "--methods",
            "hard,interpolate",
            "--context-len",
            "4",
            "--skip-hashpool",
            "--out-dir",
            "experiments/2026-09-04-probe-qwen-12x4-aaronson-hard-last4",
        ]
    )
    assert probe.model == "Qwen/Qwen2-1.5B-Instruct"
    assert probe.skip_hashpool is True


PAIR = ROOT / "experiments" / "2026-09-04-pair-qwen-12x4-aaronson"
PROBE = ROOT / "experiments" / "2026-09-04-probe-qwen-12x4-aaronson-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-04-atoms-qwen-12x4-aaronson"


def test_protocol_aaronson_qwen_official_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["mixin"] == "aaronson"
    assert pair["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert pair["seed"] == 20260905
    assert pair["hub_revision"] == "ba1cf1846d7df0a0591d6c00649f57e798519da8"
    assert len(pair["rows"]) == 12
    assert all(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    assert all(row["unmarked_gen"]["z_score"] <= 3.0 for row in pair["rows"])
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert interp["n_prompts_marked_above"] == 12
    assert hard["n_prompts_marked_above"] == 12
    assert interp["n_marked_lr_positive"] == 12
    assert interp["n_unmarked_lr_nonpositive"] == 48
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 60
    occ = json.loads((ATOMS / "atoms.json").read_text())
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 457
    assert occ["n_unseen"] == 11735
    ledger = " ".join((ROOT / "research" / "results-ledger.md").read_text().split())
    w0 = next(w for w in occ["windows"] if w["start"] == 0 and w["end"] == 4)
    assert f"**{occ['n_seen']}** seen vs **{occ['n_unseen']}** unseen" in ledger
    assert f"**{w0['n_seen']}** vs **{w0['n_unseen']}**" in ledger
    n_unmarked = sum(r["unmarked_gen"]["z_score"] > 3.0 for r in pair["rows"])
    pair_readme = (PAIR / "README.md").read_text()
    assert f"Unmarked first-draw is **{n_unmarked}/12**" in pair_readme
    research = (ROOT / "research" / "README.md").read_text()
    row = next(
        ln
        for ln in research.splitlines()
        if "PROTOCOL-next-aaronson-qwen.md" in ln
        and "qwen-100" not in ln
    )
    assert f"**{occ['n_seen']}** vs **{occ['n_unseen']}**" in row
    assert "H-aar-q-ctrl **holds**" in text
    assert "H-aar-q-group **holds**" in text
    assert "H-aar-q-iso **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **12/12**" in collapsed
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi
