"""Pooled opening-coverage union is not a mixed detector."""

import json
from pathlib import Path

from text_watermark_tools.openings import summarize_coverage_union

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-pool.md"
UNION = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-union-100-and-grok36-to-12x4"
    / "union.json"
)


def test_protocol_pool_names_frozen_mix_before_probe() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "--extra-train experiments/2026-09-01-pair-grok36x4" in text
    assert "--methods postokhits --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods interpolate --context-len 4" in text
    assert "H-pool-B" in text
    assert "H-pool-A" in text
    assert "H-pool-iso" in text
    assert "**28/48**" in text
    assert "thesis/" in text
    assert "Do **not** mix grok12" in text
    assert "`244d23a`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_published_zero_union_is_disjoint_28() -> None:
    raw = json.loads(UNION.read_text())
    assert raw["used_keys"] is False
    assert raw["n_covered_a"] == 18
    assert raw["n_covered_b"] == 10
    assert raw["n_union"] == 28
    assert raw["n_intersection"] == 0
    assert raw["n_leftover"] == 20
    by = {row["label"]: row for row in raw["leftover_signs"]}
    grok = by["grok36 interpolate"]
    assert grok["marked_above_zero"] == 13
    assert grok["unmarked_at_most_zero"] == 14
    recomputed = summarize_coverage_union(
        ROOT / "experiments/2026-09-01-openings-100x4-to-12x4/coverage.json",
        ROOT / "experiments/2026-09-01-openings-grok36x4-to-12x4/coverage.json",
        ROOT
        / "experiments/2026-09-01-transfer-grok36x4-to-12x4-hard-last4"
        / "interpolate"
        / "holdout.json",
        label_a="100-one-liners",
        label_b="grok36",
    )
    assert recomputed["n_union"] == 28
    assert recomputed["n_intersection"] == 0
    text = PROTOCOL.read_text()
    assert "replacing **25/48**" in text
    assert "Do not sell 28/48" in text or "Do **not** sell **28/48**" in text
