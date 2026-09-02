"""Threat-model freeze: key-free is not reference-free."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THREAT = ROOT / "research" / "threat-model.md"
RELATED = ROOT / "research" / "related-work.md"
ABSTRACT = ROOT / "research" / "abstract.md"
NARRATIVE = ROOT / "research" / "narrative.md"


def test_threat_model_locks_auditor_access_and_two_grains() -> None:
    text = THREAT.read_text()
    assert "key-free" in text
    assert "not reference-free" in text
    assert "not fully blind" in text
    assert "population" in text
    assert "**25/48**" in text
    assert "**99/100**" in text
    assert "Gloaguen et al. (2025)" in text
    assert "Wang et al. (2026)" in text
    assert "thesis/" in text
    assert "Do not write `thesis/`" in text or "not `thesis/`" in text
    assert "not field-defining" in text
    assert "not a finished conference paper" in text
    assert "workshop, artifact, or focused empirical report" in text


def test_related_work_does_not_claim_field_defining_novelty() -> None:
    text = RELATED.read_text()
    assert "Gloaguen et al. (2025)" in text
    assert "Wang et al. (2026)" in text
    assert "SRI Lab" in text
    assert "not a priority claim" in text.lower() or "not a priority claim" in text
    assert "finished-string paired-reference analog" in text
    assert "not a finished conference paper" in text


def test_abstract_says_key_free_is_not_reference_free() -> None:
    window = ABSTRACT.read_text().split("## Shop window", 1)[1].split(
        "## Not in the window", 1
    )[0]
    assert "not reference-free" in window
    assert "population" in window
    assert "**25/48**" in window
    assert "finished-string paired-reference analog" in window
    assert "22/48" not in window
    assert "field-defining" not in window


def test_narrative_points_at_manuscript_position() -> None:
    text = NARRATIVE.read_text()
    assert "not field-defining" in text
    assert "not a finished conference paper" in text
    assert "threat-model.md" in text
    assert "Distil lock B **88/100** (1 tie)" in text
