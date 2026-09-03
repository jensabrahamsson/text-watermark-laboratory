"""Longer-context two-grain replication, frozen before generation."""

import json
from pathlib import Path

from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-longctx.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
PAIR = ROOT / "experiments" / "2026-09-03-pair-12x4-ngram13"
PROBE = ROOT / "experiments" / "2026-09-03-probe-12x4-ngram13-hard-last4"


def test_protocol_longctx_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-long-ctrl" in text
    assert "H-long-group" in text
    assert "H-long-hard" in text
    assert "H-long-iso" in text
    assert "H-long-occ" in text
    assert "--ngram-len 13" in text
    assert "ngram_len` | **13**" in text or "`ngram_len` | **13**" in text
    assert "20260903" in text
    assert "2026-08-17-grok-prompts" in text
    assert "2026-09-03-pair-12x4-ngram13" in text
    assert "2026-09-03-probe-12x4-ngram13-hard-last4" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "--skip-hashpool" in text
    assert "--n-samples 4" in text
    assert "leave-one-family-out" in text
    assert "confusion matrix" in text
    assert "thesis/" in text
    assert "synthid-text" in text
    assert "Do **not** look at key-free LRs" in text or "Do not look at key-free LRs" in text
    assert PROMPTS.is_dir()
    n_prompts = len(list(PROMPTS.glob("*.txt")))
    assert n_prompts == 12
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "PROTOCOL-next-longctx" in log
    assert "ngram_len=13" in log or "`ngram_len=13`" in log
    assert "`b70986d`" in log


def test_protocol_longctx_cli_flag_exists() -> None:
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
            "20260903",
            "--ngram-len",
            "13",
            "--out-dir",
            "experiments/2026-09-03-pair-12x4-ngram13",
        ]
    )
    assert args.ngram_len == 13
    assert args.n_samples == 4
    assert args.seed == 20260903


def test_protocol_longctx_official_control_and_keyfree_from_dumps() -> None:
    text = PROTOCOL.read_text()
    pair = json.loads((PAIR / "results.json").read_text())
    probe = json.loads((PROBE / "results.json").read_text())
    assert pair["ngram_len"] == 13
    assert pair["seed"] == 20260903
    assert pair["max_new_tokens"] == 128
    assert len(pair["rows"]) == 12
    for row in pair["rows"]:
        assert row["marked"]["mean"] > 0.55
        assert abs(row["unmarked_gen"]["mean"] - 0.5) < 0.08
        assert row["marked"]["n_tokens"] == 128
    assert probe["used_keys"] is False
    assert probe["include_first"] is False
    hard = holdout_from_json(PROBE / "hard" / "holdout.json")
    interp = holdout_from_json(PROBE / "interpolate" / "holdout.json")
    assert hard.used_keys is False
    assert interp.used_keys is False
    assert hard.n_prompts_marked_above == 6
    assert interp.n_prompts_marked_above == 6
    hard_raw = json.loads((PROBE / "hard" / "holdout.json").read_text())
    interp_raw = json.loads((PROBE / "interpolate" / "holdout.json").read_text())
    assert hard_raw["n_marked_lr_positive"] == 22
    assert hard_raw["n_unmarked_lr_nonpositive"] == 30
    assert interp_raw["n_marked_lr_positive"] == 20
    assert interp_raw["n_unmarked_lr_nonpositive"] == 31
    assert abs(hard_raw["binary"]["auc"] - 0.544) < 0.001
    lo, hi = clopper_pearson(6, 12)
    assert lo <= 0.5 <= hi
    iso_lo, iso_hi = clopper_pearson(25, 48)
    assert iso_lo <= 0.5 <= iso_hi
    assert "H-long-ctrl **holds**" in text
    assert "H-long-group **holds**" in text
    assert "H-long-hard **holds**" in text
    assert "H-long-iso **holds**" in text
    assert "H-long-occ is **not opened**" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    collapsed = " ".join(text.split())
    assert "Do not sell **6/12**" in collapsed
    assert not (PROBE / "tables-counts").exists()
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "`b70986d`" in log
