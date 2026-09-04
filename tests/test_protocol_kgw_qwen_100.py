"""Kirchenbauer on Qwen2-1.5B 100-family, locked before generation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-kgw-qwen-100.md"
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
LOG = ROOT / "research" / "LOGBOOK.md"


def test_protocol_kgw_qwen_100_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-kgw-q100-ctrl" in text
    assert "H-kgw-q100-group" in text
    assert "H-kgw-q100-iso" in text
    assert "H-kgw-q100-occ" in text
    assert "--mixin kgw" in text
    assert "Qwen/Qwen2-1.5B-Instruct" in text
    assert "20260904" in text
    assert "2026-09-04-pair-qwen-100x4-kgw" in text
    assert "2026-09-01-prompts-100" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "ba1cf1846d7df0a0591d6c00649f57e798519da8" in text
    assert "15485863" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-kgw-qwen.md" in text
    assert "100/100" in text
    assert "683/800" in text
    assert "no chat template" in text
    assert "GPT-2 tokenizer" in text
    assert "--model Qwen/Qwen2-1.5B-Instruct" in text
    assert "H-kgw-q100-ctrl **holds**" not in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 100
    log = LOG.read_text()
    assert "PROTOCOL-next-kgw-qwen-100" in log
    assert "--mixin kgw" in log
    assert "--model Qwen/Qwen2-1.5B-Instruct" in log
    assert "`ed9fb20`" in log
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert "PROTOCOL-next-kgw-qwen-100" in ledger
    assert "`ed9fb20`" in ledger


def test_protocol_kgw_qwen_100_cli_flag_exists() -> None:
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
            "20260904",
            "--mixin",
            "kgw",
            "--hub-revision",
            "ba1cf1846d7df0a0591d6c00649f57e798519da8",
            "--out-dir",
            "experiments/2026-09-04-pair-qwen-100x4-kgw",
        ]
    )
    assert args.mixin == "kgw"
    assert args.model == "Qwen/Qwen2-1.5B-Instruct"
    assert args.seed == 20260904
    assert args.hub_revision == "ba1cf1846d7df0a0591d6c00649f57e798519da8"

    probe = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-04-pair-qwen-100x4-kgw",
            "--model",
            "Qwen/Qwen2-1.5B-Instruct",
            "--methods",
            "hard,interpolate",
            "--context-len",
            "4",
            "--skip-hashpool",
            "--out-dir",
            "experiments/2026-09-04-probe-qwen-100x4-kgw-hard-last4",
        ]
    )
    assert probe.model == "Qwen/Qwen2-1.5B-Instruct"
    assert probe.skip_hashpool is True
