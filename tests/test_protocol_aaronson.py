"""Aaronson–Kirchner exponential-minimum two-grain freeze, locked before generation."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-aaronson.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"
CODE = ROOT / "src" / "text_watermark_tools" / "aaronson.py"


def test_protocol_aaronson_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-aar-ctrl" in text
    assert "H-aar-group" in text
    assert "H-aar-hard" in text
    assert "H-aar-iso" in text
    assert "H-aar-occ" in text
    assert "--mixin aaronson" in text
    assert "20260905" in text
    assert "2026-08-17-grok-prompts" in text
    assert "2026-09-04-pair-12x4-aaronson" in text
    assert "2026-09-04-probe-12x4-aaronson-hard-last4" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "--skip-hashpool" in text
    assert "--n-samples 4" in text
    assert "leave-one-family-out" in text
    assert "**314159265**" in text
    assert "context_width" in text
    assert "z_threshold" in text
    assert "607a30d783dfa663caf39e06633721c8d4cfcd7e" in text
    assert "detector_mean" in text
    assert "WatermarkDetector" in text
    assert "synthid-text" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "Named here before generation" in text
    assert "exponential-minimum" in text
    assert "PROTOCOL-next-kgw" in text
    assert "4.57.6" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    log = LOG.read_text()
    assert "PROTOCOL-next-aaronson" in log
    assert "--mixin aaronson" in log
    assert "`747f3cd`" in log
    code = CODE.read_text()
    assert "314159265" in code
    assert "from synthid_text" not in code


def test_protocol_aaronson_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
            "--n-samples",
            "4",
            "--max-new-tokens",
            "128",
            "--seed",
            "20260905",
            "--mixin",
            "aaronson",
            "--hub-revision",
            "607a30d783dfa663caf39e06633721c8d4cfcd7e",
            "--out-dir",
            "experiments/2026-09-04-pair-12x4-aaronson",
        ]
    )
    assert args.mixin == "aaronson"
    assert args.seed == 20260905
    assert args.hub_revision == "607a30d783dfa663caf39e06633721c8d4cfcd7e"


PAIR = ROOT / "experiments" / "2026-09-04-pair-12x4-aaronson"
PROBE = ROOT / "experiments" / "2026-09-04-probe-12x4-aaronson-hard-last4"
ATOMS = ROOT / "experiments" / "2026-09-04-atoms-12x4-aaronson"


def test_protocol_aaronson_official_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    assert pair["mixin"] == "aaronson"
    assert pair["seed"] == 20260905
    assert pair["hub_revision"] == "607a30d783dfa663caf39e06633721c8d4cfcd7e"
    assert pair["aaronson"]["hashing_key"] == 314159265
    assert pair["aaronson"]["context_width"] == 1
    assert len(pair["rows"]) == 12
    assert all(row["marked"]["z_score"] > 3.0 for row in pair["rows"])
    assert all(row["unmarked_gen"]["z_score"] <= 3.0 for row in pair["rows"])
    interp = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    hard = json.loads((PROBE / "hard" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["n_prompts_marked_above"] == 11
    assert hard["n_prompts_marked_above"] == 12
    assert interp["n_marked_lr_positive"] == 8
    assert interp["n_unmarked_lr_nonpositive"] == 48
    assert interp["n_marked_lr_positive"] + interp["n_unmarked_lr_nonpositive"] == 56
    assert abs(interp["binary"]["auc"] - 0.955) < 0.001
    occ = json.loads((ATOMS / "atoms.json").read_text())
    assert occ["used_keys"] is False
    assert occ["n_seen"] == 573
    assert occ["n_unseen"] == 11618
    assert occ["n_marked_lr_positive"] == 8
    assert "H-aar-ctrl **holds**" in text
    assert "H-aar-group **holds**" in text
    assert "H-aar-iso **holds**" in text
    assert "H-aar-occ **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **11/12**" in collapsed
    lo, hi = clopper_pearson(11, 12)
    assert lo > 0.5
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert iso_lo <= 0.5 <= iso_hi
    ba_lo, ba_hi = clopper_pearson(56, 96)
    assert ba_lo <= 0.5 <= ba_hi
