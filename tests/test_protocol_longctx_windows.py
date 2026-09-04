"""Hw=12 vs Hw=4 body-window remasure, locked before those LRs."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-longctx-windows.md"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR12 = ROOT / "experiments" / "2026-09-03-pair-100x4-ngram13"
PAIR4 = ROOT / "experiments" / "2026-09-01-pair-100x4"


def test_protocol_longctx_windows_locks_config_before_lrs() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-long-win-ctrl" in text
    assert "H-long-win-body" in text
    assert "H-long-win-open" in text
    assert "H-long-win-hits" in text
    assert "2026-09-03-pair-100x4-ngram13" in text
    assert "2026-09-01-pair-100x4" in text
    assert "2026-09-04-probe-100x4-ngram13-windows" in text
    assert "2026-09-04-probe-100x4-public-w64-128" in text
    assert "--windows 0:4,4:16,16:32,32:64,64:128" in text
    assert "--windows 64:128" in text
    assert "--methods interpolate,hard,hits --context-len 4" in text
    assert "Do **not** look at window LRs" in text
    assert "76/100" in text
    assert "99/100" in text
    assert "thesis/" in text
    assert "H-long-win-body **holds**" not in text
    assert PAIR12.is_dir()
    assert PAIR4.is_dir()
    assert (PAIR12 / "results.json").is_file()
    assert (PAIR4 / "results.json").is_file()
    log = LOG.read_text()
    assert "PROTOCOL-next-longctx-windows" in log


def test_protocol_longctx_windows_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-03-pair-100x4-ngram13",
            "--methods",
            "interpolate,hard,hits",
            "--context-len",
            "4",
            "--skip-hashpool",
            "--windows",
            "0:4,4:16,16:32,32:64,64:128",
            "--out-dir",
            "experiments/2026-09-04-probe-100x4-ngram13-windows",
        ]
    )
    assert args.skip_hashpool is True
    assert args.windows == "0:4,4:16,16:32,32:64,64:128"
    pub = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-01-pair-100x4",
            "--methods",
            "interpolate",
            "--context-len",
            "4",
            "--skip-hashpool",
            "--windows",
            "64:128",
            "--out-dir",
            "experiments/2026-09-04-probe-100x4-public-w64-128",
        ]
    )
    assert pub.windows == "64:128"
