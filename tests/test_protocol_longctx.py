"""Longer-context two-grain replication, frozen before generation."""

from pathlib import Path

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


def test_protocol_longctx_results_wait_for_generation() -> None:
    text = PROTOCOL.read_text()
    opened = PAIR.exists() and (PAIR / "results.json").is_file()
    if not opened:
        assert "*(empty until the SHA is named in LOGBOOK.md)*" in text
        assert "H-long-group **holds**" not in text
        assert "H-long-group **fails**" not in text
        assert not PROBE.exists() or not (PROBE / "results.json").is_file()
        return
    import json

    raw = json.loads((PAIR / "results.json").read_text())
    assert raw["ngram_len"] == 13
    assert raw["seed"] == 20260903
    assert "does not replace **25/48**" in text
