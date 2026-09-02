"""Grok-register isolated protocol: prompts frozen before pair."""

import json
from pathlib import Path

from text_watermark_tools.indicator import holdout_from_json

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-grok12"
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-register.md"
OTHER_PROMPT_DIRS = (
    ROOT / "experiments" / "2026-08-17-grok-prompts",
    ROOT / "experiments" / "2026-08-17-more-prompts",
    ROOT / "experiments" / "2026-08-31-prompts-long12",
    ROOT / "experiments" / "2026-08-31-prompts-family12",
    ROOT / "experiments" / "2026-08-31-prompts-tails12",
    ROOT / "experiments" / "2026-09-01-prompts-100",
)


def _prompt_files() -> list[Path]:
    return sorted(p for p in PROMPTS.glob("*.txt") if p.name != "README.md")


def test_grok12_prompts_are_twelve_long_scenes() -> None:
    files = _prompt_files()
    assert [p.name[:3] for p in files] == [f"{n:03d}" for n in range(101, 113)]
    counts = [len(p.read_text().split()) for p in files]
    assert len(files) == 12
    assert min(counts) >= 220
    assert max(counts) <= 360


def test_grok12_prompts_are_disjoint_from_earlier_seeds() -> None:
    new = {p.read_text().strip() for p in _prompt_files()}
    old: set[str] = set()
    for folder in OTHER_PROMPT_DIRS:
        for path in folder.glob("*.txt"):
            if path.name == "README.md":
                continue
            old.add(path.read_text().strip())
    assert new.isdisjoint(old)
    assert len(new) == 12


def test_protocol_register_lock_a_nested_does_not_beat_one_liner_or_25() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-grok12x4-to-12x4-hard-last4"
        / "interpolate"
        / "holdout.json"
    )
    nested = json.loads(
        (root / "2026-09-01-transfer-grok12x4-to-12x4-hard-last4" / "results.json").read_text()
    )
    row = next(
        t
        for t in nested["thresholds"]
        if t["source"] == "nested-youden"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 5
    assert ev.n_marked_positive == 23
    assert row["n_marked_above"] == 16
    assert row["n_unmarked_at_most"] == 41
    assert row["n_marked_above"] < 23
    assert row["n_marked_above"] < 25
    assert ev.ranking_without_isolated_tp == []


def test_protocol_register_occupancy_free_equals_opening_coverage() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-grok12x4-to-12x4-occupancy-free"
        / "postokhits"
        / "holdout.json"
    )
    cov = json.loads(
        (root / "2026-09-01-openings-grok12x4-to-12x4" / "coverage.json").read_text()
    )
    nested = json.loads(
        (
            root / "2026-09-01-transfer-grok12x4-to-12x4-occupancy-free" / "results.json"
        ).read_text()
    )
    row = next(
        t
        for t in nested["thresholds"]
        if t["source"] == "nested-youden"
    )
    covered = cov["final"]["postokhits"]["n_covered"]
    assert ev.used_keys is False
    assert cov["used_keys"] is False
    assert ev.n_marked_positive == 5
    assert covered == 5
    assert cov["final"]["postokhits"]["n_exact_opening"] == 0
    assert row["n_marked_above"] == 5
    assert ev.n_prompt_wins_without_isolated_tp == 9
    assert ev.n_prompts_marked_above == 11


def test_protocol_register_rankpath_nested_is_not_a_detector() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-grok12x4-to-12x4-opening-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    nested = json.loads(
        (
            root
            / "2026-09-01-transfer-grok12x4-to-12x4-opening-rankpath"
            / "results.json"
        ).read_text()
    )
    row = next(
        t
        for t in nested["thresholds"]
        if t["source"] == "nested-youden"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 10
    assert ev.n_marked_positive == 22
    assert ev.n_marked_positive < 25
    assert row["n_marked_above"] == 45
    assert row["n_unmarked_at_most"] == 22
    assert row["train_youden"] < 0
    assert ev.ranking_without_isolated_tp == ["01-harbour", "12-ferry-queue"]


def test_protocol_isolated_register_still_names_frozen_locks() -> None:
    text = PROTOCOL.read_text()
    agents = (ROOT / "AGENTS.md").read_text()
    ledger = (ROOT / "research" / "results-ledger.md").read_text()
    assert "25/48" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--methods poshits --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "H-reg-iso" in text
    assert "H-reg-A **fails**" in text
    assert "20260904" in text
    assert "thesis/" in text
    assert "16/48 vs 41/48" in agents
    assert "H-reg-A fails" in agents
    assert "Do not sell 45/48" in ledger
    assert "H-reg-A fails" in ledger
