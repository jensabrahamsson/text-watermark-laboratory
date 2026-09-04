"""Qwen Kirchenbauer 100-family windows, locked before those LRs."""

import json
from pathlib import Path

import pytest

from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-next-kgw-qwen-100-windows.md"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-09-04-pair-qwen-100x4-kgw"
FULL = ROOT / "experiments" / "2026-09-04-probe-qwen-100x4-kgw-hard-last4"
WINDOWS = ROOT / "experiments" / "2026-09-04-probe-qwen-100x4-kgw-windows"


def test_protocol_kgw_qwen_100_windows_locks_config_before_lrs() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-kgw-q100-win-ctrl" in text
    assert "H-kgw-q100-win-open" in text
    assert "H-kgw-q100-win-body" in text
    assert "H-kgw-q100-win-iso" in text
    assert "2026-09-04-pair-qwen-100x4-kgw" in text
    assert "2026-09-04-probe-qwen-100x4-kgw-windows" in text
    assert "--windows 0:4,4:16,16:32,32:64,64:128" in text
    assert "--methods interpolate,hard --context-len 4" in text
    assert "--model Qwen/Qwen2-1.5B-Instruct" in text
    assert "Do **not** look at window LRs" in text
    assert "96/100" in text
    assert "620/800" in text
    assert "detector_mean" in text
    assert "thesis/" in text
    assert "PROTOCOL-next-kgw-qwen-100.md" in text
    assert "H-kgw-q100-win-ctrl **holds**" in text
    assert "H-kgw-q100-win-open **holds**" in text
    assert "H-kgw-q100-win-body **holds**" in text
    assert "H-kgw-q100-win-iso **holds**" in text
    collapsed = " ".join(text.split())
    assert "Do not sell **97/100**" in collapsed
    assert text.count("## Results") == 1
    assert PAIR.is_dir()
    assert (PAIR / "results.json").is_file()
    assert (FULL / "interpolate" / "holdout.json").is_file()
    log = LOG.read_text()
    assert "PROTOCOL-next-kgw-qwen-100-windows" in log
    assert "`e270546`" in log
    assert "**97/100**" in log


def test_protocol_kgw_qwen_100_windows_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-09-04-pair-qwen-100x4-kgw",
            "--model",
            "Qwen/Qwen2-1.5B-Instruct",
            "--methods",
            "interpolate,hard",
            "--context-len",
            "4",
            "--skip-hashpool",
            "--windows",
            "0:4,4:16,16:32,32:64,64:128",
            "--out-dir",
            "experiments/2026-09-04-probe-qwen-100x4-kgw-windows",
        ]
    )
    assert args.model == "Qwen/Qwen2-1.5B-Instruct"
    assert args.skip_hashpool is True
    assert args.windows == "0:4,4:16,16:32,32:64,64:128"


@pytest.mark.skipif(
    not (WINDOWS / "results.json").is_file(),
    reason="Qwen Kirchenbauer 100-family windows not dumped",
)
def test_protocol_kgw_qwen_100_windows_from_dumps() -> None:
    text = PROTOCOL.read_text()
    data = json.loads((WINDOWS / "results.json").read_text())
    assert data["used_keys"] is False
    assert data["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    full = json.loads((FULL / "interpolate" / "holdout.json").read_text())
    assert full["n_prompts_marked_above"] == 96
    interp_full = next(m for m in data["methods"] if m["name"] == "interpolate")
    assert interp_full["n_prompt_wins"] == 96
    open_ = next(
        r
        for r in data["window_scores"]
        if r["name"] == "interpolate" and r["start"] == 0 and r["end"] == 4
    )
    tail = next(
        r
        for r in data["window_scores"]
        if r["name"] == "interpolate" and r["start"] == 64 and r["end"] == 128
    )
    assert open_["n_prompt_wins"] == 84
    assert tail["n_prompt_wins"] == 97
    assert f"**{open_['n_prompt_wins']}/100**" in text
    assert f"**{tail['n_prompt_wins']}/100**" in text
    assert f"**{full['n_prompts_marked_above']}/100**" in text
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi
    ba_lo, ba_hi = clopper_pearson(50, 100)
    assert ba_lo <= 0.5 <= ba_hi
