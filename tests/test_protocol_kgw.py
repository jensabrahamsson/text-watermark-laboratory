"""Kirchenbauer green-list two-grain freeze, locked before generation."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-kgw.md"
PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
LOG = ROOT / "research" / "LOGBOOK.md"


def test_protocol_kgw_locks_config_before_generation() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-kgw-ctrl" in text
    assert "H-kgw-group" in text
    assert "H-kgw-hard" in text
    assert "H-kgw-iso" in text
    assert "H-kgw-occ" in text
    assert "--mixin kgw" in text
    assert "20260904" in text
    assert "2026-08-17-grok-prompts" in text
    assert "2026-09-03-pair-12x4-kgw" in text
    assert "2026-09-03-probe-12x4-kgw-hard-last4" in text
    assert "--methods hard,interpolate --context-len 4" in text
    assert "--skip-hashpool" in text
    assert "--n-samples 4" in text
    assert "leave-one-family-out" in text
    assert "greenlist_ratio" in text
    assert "**0.25**" in text
    assert "**2.0**" in text
    assert "**15485863**" in text
    assert "lefthash" in text
    assert "context_width" in text
    assert "z_threshold" in text
    assert "607a30d783dfa663caf39e06633721c8d4cfcd7e" in text
    assert "detector_mean" in text
    assert "synthid-text" in text
    assert "thesis/" in text
    assert "Do **not** look at key-free LRs" in text
    assert "Not opened" in text
    assert "Aaronson" in text
    assert "PROTOCOL-next-longctx" in text
    assert "not unique to tournament" in text or "not unique to tournament sampling" in text
    assert PROMPTS.is_dir()
    assert len(list(PROMPTS.glob("*.txt"))) == 12
    log = LOG.read_text()
    assert "PROTOCOL-next-kgw" in log
    assert "--mixin kgw" in log


def test_protocol_kgw_cli_flag_exists() -> None:
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
            "20260904",
            "--mixin",
            "kgw",
            "--hub-revision",
            "607a30d783dfa663caf39e06633721c8d4cfcd7e",
            "--out-dir",
            "experiments/2026-09-03-pair-12x4-kgw",
        ]
    )
    assert args.mixin == "kgw"
    assert args.n_samples == 4
    assert args.seed == 20260904
    assert args.hub_revision == "607a30d783dfa663caf39e06633721c8d4cfcd7e"
    assert args.ngram_len == 5


def test_protocol_kgw_refuses_synthid_only_flags() -> None:
    from text_watermark_tools.cli import build_parser, cmd_pair

    parser = build_parser()
    ngram = parser.parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
            "--mixin",
            "kgw",
            "--ngram-len",
            "13",
        ]
    )
    assert cmd_pair(ngram) == 2
    ctrl = parser.parse_args(
        [
            "pair",
            "experiments/2026-08-17-grok-prompts",
            "--mixin",
            "kgw",
            "--control-only",
        ]
    )
    assert cmd_pair(ctrl) == 2


def test_protocol_kgw_has_no_pair_dump_yet() -> None:
    pair = ROOT / "experiments" / "2026-09-03-pair-12x4-kgw"
    probe = ROOT / "experiments" / "2026-09-03-probe-12x4-kgw-hard-last4"
    assert not (pair / "results.json").is_file()
    assert not (probe / "hard" / "holdout.json").is_file()
