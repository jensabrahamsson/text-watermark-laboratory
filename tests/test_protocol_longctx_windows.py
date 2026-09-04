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
    assert "`8283d1f`" in log
    assert "**50/100**" in log
    assert "**93/100**" in log


def test_protocol_longctx_windows_dumps_match_freeze() -> None:
    import json

    hw12 = ROOT / "experiments" / "2026-09-04-probe-100x4-ngram13-windows" / "results.json"
    pub = ROOT / "experiments" / "2026-09-04-probe-100x4-public-w64-128" / "results.json"
    assert hw12.is_file()
    assert pub.is_file()
    hw12_data = json.loads(hw12.read_text())
    pub_data = json.loads(pub.read_text())
    assert hw12_data["used_keys"] is False
    assert pub_data["used_keys"] is False
    hw12_full = {m["name"]: m["n_prompt_wins"] for m in hw12_data["methods"]}
    assert hw12_full["interpolate"] == 76
    pub_full = {m["name"]: m["n_prompt_wins"] for m in pub_data["methods"]}
    assert pub_full["interpolate"] == 99
    hw12_tail = [
        w
        for w in hw12_data["window_scores"]
        if w["start"] == 64 and w["end"] == 128 and w["name"] == "interpolate"
    ]
    pub_tail = [
        w
        for w in pub_data["window_scores"]
        if w["start"] == 64 and w["end"] == 128 and w["name"] == "interpolate"
    ]
    assert hw12_tail and hw12_tail[0]["n_prompt_wins"] == 50
    assert pub_tail and pub_tail[0]["n_prompt_wins"] == 93
    hw12_open = [
        w
        for w in hw12_data["window_scores"]
        if w["start"] == 0 and w["end"] == 4 and w["name"] == "interpolate"
    ]
    assert hw12_open and hw12_open[0]["n_prompt_wins"] == 86


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
