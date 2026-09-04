"""Aaronson–Kirchner on DistilGPT2 100-family, locked before generation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-aaronson-distil-100.md"
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
LOG = ROOT / "research" / "LOGBOOK.md"


def test_protocol_aaronson_distil_100_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-aar-d100-ctrl" in text
    assert "H-aar-d100-group" in text
    assert "H-aar-d100-iso" in text
    assert "H-aar-d100-occ" in text
    assert "--mixin aaronson" in text
    assert "--model distilgpt2" in text
    assert "20260905" in text
    assert "2026-09-04-pair-distil-100x4-aaronson" in text
    assert "2026-09-01-prompts-100" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "2290a62682d06624634c1f46a6ad5be0f47f38aa" in text
    assert "314159265" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-aaronson-distil.md" in text
    assert "100/100" in text
    assert "H-aar-d100-ctrl **holds**" not in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 100
    log = LOG.read_text()
    assert "PROTOCOL-next-aaronson-distil-100" in log
    assert "--mixin aaronson" in log
    assert "--model distilgpt2" in log
    assert "`bf05759`" in log


def test_protocol_aaronson_distil_100_cli_flag_exists() -> None:
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
            "20260905",
            "--mixin",
            "aaronson",
            "--hub-revision",
            "2290a62682d06624634c1f46a6ad5be0f47f38aa",
            "--out-dir",
            "experiments/2026-09-04-pair-distil-100x4-aaronson",
        ]
    )
    assert args.mixin == "aaronson"
    assert args.model == "distilgpt2"
    assert args.seed == 20260905
    assert args.hub_revision == "2290a62682d06624634c1f46a6ad5be0f47f38aa"
