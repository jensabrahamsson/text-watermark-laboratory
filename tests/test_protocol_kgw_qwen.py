"""Kirchenbauer on Qwen2-1.5B, frozen before generation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-kgw-qwen.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"


def test_protocol_kgw_qwen_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-kgw-q-ctrl" in text
    assert "H-kgw-q-group" in text
    assert "H-kgw-q-iso" in text
    assert "--mixin kgw" in text
    assert "Qwen/Qwen2-1.5B-Instruct" in text
    assert "20260904" in text
    assert "2026-09-03-pair-qwen-12x4-kgw" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "--model Qwen/Qwen2-1.5B-Instruct" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "Not opened" in text
    assert "no chat template" in text
    assert "GPT-2 `WatermarkDetector`" in text or "GPT-2 WatermarkDetector" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    log = LOG.read_text()
    assert "PROTOCOL-next-kgw-qwen" in log


def test_protocol_kgw_qwen_cli_flag_exists() -> None:
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
            "20260904",
            "--mixin",
            "kgw",
            "--out-dir",
            "experiments/2026-09-03-pair-qwen-12x4-kgw",
        ]
    )
    assert args.mixin == "kgw"
    assert args.model == "Qwen/Qwen2-1.5B-Instruct"
    assert args.seed == 20260904


def test_protocol_kgw_qwen_has_no_pair_dump_yet() -> None:
    pair = ROOT / "experiments" / "2026-09-03-pair-qwen-12x4-kgw"
    probe = ROOT / "experiments" / "2026-09-03-probe-qwen-12x4-kgw-hard-last4"
    assert not (pair / "results.json").is_file()
    assert not (probe / "hard" / "holdout.json").is_file()
