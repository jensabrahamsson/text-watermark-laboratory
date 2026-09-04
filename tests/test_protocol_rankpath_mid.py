"""GPT-2 rankpath mid-file window [16:32), locked before LRs."""

import json
from pathlib import Path

from text_watermark_tools.generate import is_gpt2_name
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-rankpath-mid.md"
LOG = ROOT / "research" / "LOGBOOK.md"
PAIR = ROOT / "experiments" / "2026-08-17-pair-12x4"
OPENING = ROOT / "experiments" / "2026-09-01-probe-12x4-recount-opening-rankpath"
BODY = (
    ROOT
    / "experiments"
    / "2026-09-04-probe-12x4-rankpath-w4-16"
    / "window-4-16"
)
PROBE = (
    ROOT
    / "experiments"
    / "2026-09-04-probe-12x4-rankpath-w16-32"
    / "window-16-32"
)


def test_protocol_rankpath_mid_locks_config_before_lrs() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-rpmid" in text
    assert "H-rpmid-iso" in text
    assert "H-rpmid **holds**" in text
    assert "H-rpmid-iso **holds**" in text
    assert "Do not sell **23/48**" in text
    assert "*(empty until the SHA is named in LOGBOOK.md" not in text
    assert "--windows 16:32" in text
    assert "--fit-prefix 32 --pos-bucket 1" in text
    assert "--methods rankpath" in text
    assert "2026-08-17-pair-12x4" in text
    assert "2026-09-04-probe-12x4-rankpath-w16-32" in text
    assert "Do **not** look at rankpath `[16:32)` LRs" in text
    assert "Do **not** leftover-slice" in text
    assert "Do **not** pass `--rankpath-full`" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert PAIR.is_dir()
    assert is_gpt2_name("gpt2") is True
    log = LOG.read_text()
    assert "PROTOCOL-isolated-rankpath-mid" in log
    assert "named before" in log
    assert "PROTOCOL-isolated-rankpath-mid" in (
        ROOT / "research" / "results-ledger.md"
    ).read_text()
    assert "PROTOCOL-isolated-rankpath-mid" in (ROOT / "HOW-TO.md").read_text()
    exp = [
        ln
        for ln in (ROOT / "experiments" / "README.md").read_text().splitlines()
        if "2026-09-04-probe-12x4-rankpath-w16-32" in ln
    ]
    assert len(exp) == 1
    research = [
        ln
        for ln in (ROOT / "research" / "README.md").read_text().splitlines()
        if "PROTOCOL-isolated-rankpath-mid.md" in ln
    ]
    assert len(research) == 1
    agents = [
        ln
        for ln in (ROOT / "AGENTS.md").read_text().splitlines()
        if ln.startswith("| gpt2 opening rankpath [16:32)")
    ]
    assert len(agents) == 1
    assert "**25/48**" in agents[0]
    assert "**23/48 vs 26/48**" in agents[0]
    lo, hi = clopper_pearson(25, 48)
    assert lo <= 0.5 <= hi


def test_protocol_rankpath_mid_cli_flag_exists() -> None:
    from text_watermark_tools.cli import build_parser

    args = build_parser().parse_args(
        [
            "probe",
            "experiments/2026-08-17-pair-12x4",
            "--skip-hashpool",
            "--fit-prefix",
            "32",
            "--pos-bucket",
            "1",
            "--methods",
            "rankpath",
            "--windows",
            "16:32",
            "--out-dir",
            "experiments/2026-09-04-probe-12x4-rankpath-w16-32",
        ]
    )
    assert args.windows == "16:32"
    assert args.fit_prefix == 32
    assert args.methods == "rankpath"


def test_protocol_rankpath_mid_opening_control_stays() -> None:
    holdout = json.loads((OPENING / "rankpath" / "holdout.json").read_text())
    assert holdout["used_keys"] is False
    assert holdout["model_name"] == "gpt2"
    assert holdout["n_prompts_marked_above"] == 11
    assert holdout["n_marked_lr_positive"] == 41
    assert holdout["n_unmarked_lr_nonpositive"] == 35


def test_protocol_rankpath_mid_body_control_stays() -> None:
    holdout = json.loads((BODY / "rankpath" / "holdout.json").read_text())
    assert holdout["used_keys"] is False
    assert holdout["model_name"] == "gpt2"
    assert holdout["n_prompts_marked_above"] == 7
    assert holdout["n_marked_lr_positive"] == 20
    assert holdout["n_unmarked_lr_nonpositive"] == 22


def test_protocol_rankpath_mid_from_dumps() -> None:
    interp = json.loads((PROBE / "rankpath" / "holdout.json").read_text())
    assert interp["used_keys"] is False
    assert interp["used_hash_iv"] is False
    assert interp["used_g_values"] is False
    assert interp["model_name"] == "gpt2"
    assert interp["n_prompts_marked_above"] == 7
    assert interp["n_marked_lr_positive"] == 23
    assert interp["n_unmarked_lr_nonpositive"] == 26
    text = PROTOCOL.read_text()
    assert "H-rpmid **holds**" in text
    marked = interp["n_marked_lr_positive"]
    unmarked = interp["n_unmarked_lr_nonpositive"]
    assert f"**{marked}/48 vs {unmarked}/48**" in text
    readme = (PROBE.parent / "README.md").read_text()
    assert f"**{marked}/48 vs {unmarked}/48**" in readme
    lo, hi = clopper_pearson(marked, 48)
    assert lo <= 0.5 <= hi
    lo25, hi25 = clopper_pearson(25, 48)
    assert lo25 <= 0.5 <= hi25
