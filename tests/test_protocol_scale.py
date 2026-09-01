"""36 Grok-length prompts frozen before pair."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-grok36"
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-scale.md"
OTHER_PROMPT_DIRS = (
    ROOT / "experiments" / "2026-08-17-grok-prompts",
    ROOT / "experiments" / "2026-08-17-more-prompts",
    ROOT / "experiments" / "2026-08-31-prompts-long12",
    ROOT / "experiments" / "2026-08-31-prompts-family12",
    ROOT / "experiments" / "2026-08-31-prompts-tails12",
    ROOT / "experiments" / "2026-09-01-prompts-100",
    ROOT / "experiments" / "2026-09-01-prompts-grok12",
)


def _prompt_files() -> list[Path]:
    return sorted(p for p in PROMPTS.glob("*.txt") if p.name != "README.md")


def test_grok36_prompts_are_thirty_six_long_scenes() -> None:
    files = _prompt_files()
    assert [p.name[:3] for p in files] == [f"{n:03d}" for n in range(201, 237)]
    counts = [len(p.read_text().split()) for p in files]
    assert len(files) == 36
    assert min(counts) >= 220
    assert max(counts) <= 330


def test_grok36_prompts_are_disjoint_from_earlier_seeds() -> None:
    new = {p.read_text().strip() for p in _prompt_files()}
    old: set[str] = set()
    for folder in OTHER_PROMPT_DIRS:
        for path in folder.glob("*.txt"):
            old.add(path.read_text().strip())
    assert new.isdisjoint(old)
    assert len(new) == 36


def test_protocol_scale_names_frozen_locks_before_pair() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "--methods interpolate --context-len 4" in text
    assert "--methods poshits --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods postokhits --fit-prefix 4 --pos-bucket 1" in text
    assert "H-scale-A" in text
    assert "H-scale-grok" in text
    assert "H-scale-B" in text
    assert "H-scale-iso" in text
    assert "20260905" in text
    assert "2026-09-01-prompts-grok36" in text
    assert "2026-09-01-pair-grok12x4" in text
    assert "Do **not** mix" in text
    assert "thesis/" in text
    assert "pair-grok36x4" in text
    assert "`e537d71`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_protocol_scale_pair_official_lamp_is_36_of_36() -> None:
    pair = ROOT / "experiments" / "2026-09-01-pair-grok36x4"
    raw = json.loads((pair / "results.json").read_text())
    assert raw["seed"] == 20260905
    assert raw["instance"] == "public-deepmind-30"
    assert raw["also_control_keys"] is False
    rows = raw["rows"]
    assert len(rows) == 36
    wins = sum(1 for r in rows if r["marked"]["mean"] > r["unmarked_gen"]["mean"])
    assert wins == 36
    assert min(r["marked"]["mean"] for r in rows) > 0.55
    assert max(r["unmarked_gen"]["mean"] for r in rows) < 0.55
    assert len(list(pair.glob("*-marked-4.txt"))) == 36
    assert len(list(pair.glob("*-unmarked-gen-4.txt"))) == 36


def test_protocol_scale_lock_a_grok12_beats_xreg_not_25() -> None:
    from text_watermark_tools.indicator import holdout_from_json

    root = ROOT / "experiments"
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-grok36x4-to-grok12x4-hard-last4"
        / "interpolate"
        / "holdout.json"
    )
    nested = json.loads(
        (
            root / "2026-09-01-transfer-grok36x4-to-grok12x4-hard-last4" / "results.json"
        ).read_text()
    )
    row = next(t for t in nested["thresholds"] if t["source"] == "nested-youden")
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 39
    assert row["n_marked_above"] == 36
    assert row["n_unmarked_at_most"] == 39
    assert row["n_marked_above"] > 22
    text = PROTOCOL.read_text()
    assert "H-scale-grok **holds**" in text
    assert "H-scale-iso **holds**" in text


def test_protocol_scale_occupancy_free_equals_opening_coverage() -> None:
    from text_watermark_tools.indicator import holdout_from_json

    root = ROOT / "experiments"
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-grok36x4-to-grok12x4-occupancy-free"
        / "postokhits"
        / "holdout.json"
    )
    cov = json.loads(
        (root / "2026-09-01-openings-grok36x4-to-grok12x4" / "coverage.json").read_text()
    )
    nested = json.loads(
        (
            root
            / "2026-09-01-transfer-grok36x4-to-grok12x4-occupancy-free"
            / "results.json"
        ).read_text()
    )
    row = next(t for t in nested["thresholds"] if t["source"] == "nested-youden")
    covered = cov["final"]["postokhits"]["n_covered"]
    assert ev.used_keys is False
    assert cov["used_keys"] is False
    assert ev.n_marked_positive == 39
    assert covered == 39
    assert row["n_marked_above"] == 39
    assert cov["final"]["postokhits"]["n_exact_opening"] == 21
    assert cov["final"]["postokhits"]["coverage_gate"]["decided_fp"] == 3


def test_protocol_scale_lock_a_original_12_beats_n12_not_25() -> None:
    from text_watermark_tools.indicator import holdout_from_json

    root = ROOT / "experiments"
    ev = holdout_from_json(
        root
        / "2026-09-01-transfer-grok36x4-to-12x4-hard-last4"
        / "interpolate"
        / "holdout.json"
    )
    nested = json.loads(
        (
            root / "2026-09-01-transfer-grok36x4-to-12x4-hard-last4" / "results.json"
        ).read_text()
    )
    row = next(t for t in nested["thresholds"] if t["source"] == "nested-youden")
    occ = holdout_from_json(
        root
        / "2026-09-01-transfer-grok36x4-to-12x4-occupancy-free"
        / "postokhits"
        / "holdout.json"
    )
    cov = json.loads(
        (root / "2026-09-01-openings-grok36x4-to-12x4" / "coverage.json").read_text()
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 10
    assert row["n_marked_above"] == 26
    assert row["n_unmarked_at_most"] == 33
    assert row["n_marked_above"] > 16
    assert occ.n_marked_positive == 10
    assert cov["final"]["postokhits"]["n_covered"] == 10
    text = PROTOCOL.read_text()
    assert "H-scale-A **holds**" in text
    assert "H-scale-B **holds**" in text
    assert "Do not sell 26/48" in text


def test_protocol_scale_atoms_explain_nested_versus_occupancy_free() -> None:
    text = PROTOCOL.read_text()
    assert "2026-09-01-atoms-grok36x4-to-12x4-interpolate" in text
    assert "2026-09-01-atoms-grok36x4-to-grok12x4-interpolate" in text
    assert "Witten–Bell" in text or "Witten-Bell" in text
    assert "unbucketed" in text
    assert "Does not replace **25/48**" in text
    orig = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-01-atoms-grok36x4-to-12x4-interpolate"
            / "atoms.json"
        ).read_text()
    )
    grok = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-01-atoms-grok36x4-to-grok12x4-interpolate"
            / "atoms.json"
        ).read_text()
    )
    assert orig["used_keys"] is False
    assert grok["used_keys"] is False
    assert orig["n_marked_lr_positive"] == 29
    assert grok["n_marked_lr_positive"] == 39
    assert orig["n_marked_lr_positive"] != 10
    assert grok["n_marked_lr_positive"] == 39
