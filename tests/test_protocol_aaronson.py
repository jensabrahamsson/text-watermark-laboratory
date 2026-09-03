"""Aaronson–Kirchner exponential-minimum two-grain freeze, locked before generation."""

from pathlib import Path

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
    assert "H-aar-ctrl **holds**" not in text
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
