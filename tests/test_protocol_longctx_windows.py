"""Hw=12 vs Hw=4 body-window remasure, locked before those LRs."""

import json
from pathlib import Path

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-longctx-windows.md"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR12 = ROOT / "experiments" / "2026-09-03-pair-100x4-ngram13"
PAIR4 = ROOT / "experiments" / "2026-09-01-pair-100x4"
HW12 = ROOT / "experiments" / "2026-09-04-probe-100x4-ngram13-windows"
PUB = ROOT / "experiments" / "2026-09-04-probe-100x4-public-w64-128"


def _named(rows: list[dict], name: str) -> dict:
    found = [row for row in rows if row["name"] == name]
    assert len(found) == 1
    return found[0]


def _window(rows: list[dict], name: str, start: int, end: int) -> dict:
    found = [
        row
        for row in rows
        if row["name"] == name and row["start"] == start and row["end"] == end
    ]
    assert len(found) == 1
    return found[0]


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
    assert "H-long-win-ctrl **holds**" in text
    assert "H-long-win-body **holds**" in text
    assert "H-long-win-open **holds**" in text
    assert "H-long-win-hits **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **50/100**" in collapsed
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
    hw12_data = json.loads((HW12 / "results.json").read_text())
    pub_data = json.loads((PUB / "results.json").read_text())
    assert hw12_data["used_keys"] is False
    assert hw12_data["used_hash_iv"] is False
    assert hw12_data["used_g_values"] is False
    assert pub_data["used_keys"] is False
    assert pub_data["used_hash_iv"] is False
    assert pub_data["used_g_values"] is False
    assert hw12_data["context_len"] == 4
    assert pub_data["context_len"] == 4
    assert hw12_data["pair_dir"] == "experiments/2026-09-03-pair-100x4-ngram13"
    assert pub_data["pair_dir"] == "experiments/2026-09-01-pair-100x4"
    assert hw12_data["windows"] == ["0:4", "4:16", "16:32", "32:64", "64:128"]
    assert pub_data["windows"] == ["64:128"]
    assert [m["name"] for m in hw12_data["methods"]] == ["interpolate", "hard", "hits"]
    assert [m["name"] for m in pub_data["methods"]] == ["interpolate"]
    hw12_full = _named(hw12_data["methods"], "interpolate")
    pub_full = _named(pub_data["methods"], "interpolate")
    hits_full = _named(hw12_data["methods"], "hits")
    assert hw12_full["n_prompt_wins"] == 76
    assert pub_full["n_prompt_wins"] == 99
    assert hits_full["n_prompt_wins"] == 91
    hw12_tail = _window(hw12_data["window_scores"], "interpolate", 64, 128)
    pub_tail = _window(pub_data["window_scores"], "interpolate", 64, 128)
    hw12_open = _window(hw12_data["window_scores"], "interpolate", 0, 4)
    hits_open = _window(hw12_data["window_scores"], "hits", 0, 4)
    hits_tail = _window(hw12_data["window_scores"], "hits", 64, 128)
    assert hw12_tail["n_prompt_wins"] == 50
    assert pub_tail["n_prompt_wins"] == 93
    assert hw12_open["n_prompt_wins"] == 86
    assert hits_open["n_prompt_wins"] == 95
    assert hits_tail["n_prompt_wins"] == 53
    assert abs(hw12_tail["binary"]["auc"] - 0.501) < 0.001
    assert abs(pub_tail["binary"]["auc"] - 0.726) < 0.001
    assert abs(hw12_open["binary"]["auc"] - 0.823) < 0.001
    assert hw12_tail["binary"]["n_positive_above_zero"] == 184
    assert hw12_tail["binary"]["n_negative_at_most_zero"] == 212
    assert pub_tail["binary"]["n_positive_above_zero"] == 259
    assert pub_tail["binary"]["n_negative_at_most_zero"] == 258
    tail_hold = json.loads(
        (HW12 / "window-64-128" / "interpolate" / "holdout.json").read_text()
    )
    pub_hold = json.loads(
        (PUB / "window-64-128" / "interpolate" / "holdout.json").read_text()
    )
    assert tail_hold["used_keys"] is False
    assert pub_hold["used_keys"] is False
    assert tail_hold["n_prompts_marked_above"] == 50
    assert pub_hold["n_prompts_marked_above"] == 93
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi


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
