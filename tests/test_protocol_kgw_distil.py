"""Kirchenbauer on DistilGPT2, frozen before generation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-kgw-distil.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"


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
    assert "Not opened" in text
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


def test_protocol_kgw_distil_has_no_pair_dump_yet() -> None:
    pair = ROOT / "experiments" / "2026-09-03-pair-distil-12x4-kgw"
    probe = ROOT / "experiments" / "2026-09-03-probe-distil-12x4-kgw-hard-last4"
    assert not (pair / "results.json").is_file()
    assert not (probe / "hard" / "holdout.json").is_file()
