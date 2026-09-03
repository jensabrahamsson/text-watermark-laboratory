"""DistilGPT2 ngram_len=13 two-grain freeze, locked before generation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-longctx-distil.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"


def test_protocol_longctx_distil_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-long-d-ctrl" in text
    assert "H-long-d-group" in text
    assert "H-long-d-iso" in text
    assert "H-long-d-occ" in text
    assert "--ngram-len 13" in text
    assert "--model distilgpt2" in text
    assert "20260903" in text
    assert "2026-09-04-pair-distil-12x4-ngram13" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "2290a62682d06624634c1f46a6ad5be0f47f38aa" in text
    assert "detector_mean" in text
    assert "ngram_len=5" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "PROTOCOL-next-longctx.md" in text
    assert "H-long-d-ctrl **holds**" not in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    log = LOG.read_text()
    assert "PROTOCOL-next-longctx-distil" in log
    assert "--model distilgpt2" in log
    assert "--ngram-len 13" in log


def test_protocol_longctx_distil_cli_flag_exists() -> None:
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
            "20260903",
            "--ngram-len",
            "13",
            "--hub-revision",
            "2290a62682d06624634c1f46a6ad5be0f47f38aa",
            "--out-dir",
            "experiments/2026-09-04-pair-distil-12x4-ngram13",
        ]
    )
    assert args.model == "distilgpt2"
    assert args.ngram_len == 13
    assert args.seed == 20260903
    assert args.hub_revision == "2290a62682d06624634c1f46a6ad5be0f47f38aa"
