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
    assert "H-kgw-q100-win-ctrl **holds**" not in text
    assert PAIR.is_dir()
    assert (PAIR / "results.json").is_file()
    assert (FULL / "interpolate" / "holdout.json").is_file()
    log = LOG.read_text()
    assert "PROTOCOL-next-kgw-qwen-100-windows" in log


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
    if "H-kgw-q100-win-ctrl **holds**" not in text:
        pytest.skip("window counts not folded yet")
    data = json.loads((WINDOWS / "results.json").read_text())
    assert data["used_keys"] is False
    assert data["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    full = json.loads((FULL / "interpolate" / "holdout.json").read_text())
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi
    assert f"**{full['n_prompts_marked_above']}/100**" in text
