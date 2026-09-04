"""Narrative freeze: two grains, not a failure paper."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NARRATIVE = ROOT / "research" / "narrative.md"
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-mask.md"


def test_narrative_rejects_failure_title_and_keeps_headlines() -> None:
    text = NARRATIVE.read_text()
    assert "Why Key-Free Watermark Detection Fails" in text
    assert "wrong for this laboratory" in text
    assert "**9/12**" in text
    assert "**25/48**" in text
    assert "**36/36**" in text
    assert "10/12" in text
    assert "29/48" in text
    assert "thesis/" in text
    assert "Two grains" in text
    assert "leftover **10/20 vs 11/20**" in text
    assert "PROTOCOL-next **H3**" in text
    assert "PROTOCOL-isolated-mask-split" in text
    assert "PROTOCOL-isolated-leftover-bound" in text
    assert "PROTOCOL-isolated-leftover-union" in text
    assert "leftover **11/20 vs 11/20**" in text or "leftover is **11/20 vs 11/20**" in text
    assert "union **30/48**" in text
    assert "leftover **10/18**" in text
    assert "PROTOCOL-isolated-occupancy-closed" in text
    assert "Leftover-18 official is **18/18**" in text
    assert "PROTOCOL-isolated-leftover-18" in text
    assert "leftover-18 mixed rankpath **12/18 vs 13/18**" in text
    assert "PROTOCOL-isolated-leftover-18-closed" in text
    assert "PROTOCOL-isolated-xgen" in text
    assert "Distil occupancy-free t=0 **22/48 vs 43/48**" in text
    assert "PROTOCOL-isolated-dsmt" in text
    assert "union **33/48**" in text
    assert "leftover **9/15**" in text
    assert "PROTOCOL-isolated-leftover-15-closed" in text
    assert "PROTOCOL-isolated-mgen" in text
    assert "PROTOCOL-isolated-m12" in text
    assert "PROTOCOL-isolated-xsize" in text
    assert "PROTOCOL-h2-absolute" in text
    assert "PROTOCOL-isolated-xkey" in text
    assert "PROTOCOL-isolated-windows-absolute" in text
    assert "PROTOCOL-isolated-mask-absolute" in text
    assert "PROTOCOL-isolated-rankpath-lm" in text
    assert "PROTOCOL-isolated-rankpath-m12" in text
    assert "PROTOCOL-next-longctx" in text
    assert "PROTOCOL-next-kgw" in text
    assert "--mixin kgw" in text
    assert "**85/96**" in text
    assert "**114**" in text
    assert "**100/100**" in text
    assert "**747/800**" in text
    assert "**4557**" in text
    assert "**6/12**" in text
    assert "**76/100**" in text
    assert "PROTOCOL-next-longctx-distil" in text
    assert "**49/96**" in text
    assert "PROTOCOL-next-longctx-qwen" in text
    assert "**41/96**" in text
    assert "PROTOCOL-next-aaronson-distil" in text
    assert "**0/48**" in text
    assert "PROTOCOL-next-aaronson-qwen" in text
    assert "**60/96**" in text
    assert "PROTOCOL-next-longctx-distil-100" in text
    assert "**557/800**" in text
    assert "PROTOCOL-next-longctx-qwen-100" in text
    assert "636765c" in text
    assert "**474/800**" in text
    assert "PROTOCOL-next-longctx-windows" in text
    assert "8283d1f" in text
    assert "**50/100**" in text
    assert "**93/100**" in text
    assert "**86/100**" in text
    assert "PROTOCOL-next-aaronson-distil-100" in text
    assert "**601/800**" in text
    assert "PROTOCOL-next-aaronson-qwen-100" in text
    assert "**616/800**" in text
    assert "PROTOCOL-next-kgw-qwen-100" in text
    assert "`ed9fb20`" in text
    assert "**96/100**" in text
    assert "**620/800**" in text
    assert "PROTOCOL-next-kgw-qwen-100-windows" in text
    assert "`e270546`" in text
    assert "**683/800**" in text
    assert "**68/96**" in text
    assert "**82/100**" in text
    assert "**8/12**" in text
    assert "**16170**" in text
    assert "**84**" in text
    assert "**12108**" in text
    assert "**71541**" in text
    assert "**11972**" in text
    assert "**11/12**" in text
    assert "**160**" in text
    assert "**269**" in text
    assert "**5878**" in text
    assert "**10158**" in text
    assert "H-xkey-iso **fails**" in text
    assert "Leftover-15 official is **15/15**" in text
    assert "Master of Science" in text
    assert "Do not write `thesis/`" in text or "Do **not** write `thesis/`" in text
    assert "`004397c`" in (ROOT / "research" / "LOGBOOK.md").read_text()


def test_narrative_mixin_occupancy_from_atoms() -> None:
    text = re.sub(r"\s+", " ", NARRATIVE.read_text())
    dumps = (
        "experiments/2026-09-04-atoms-distil-12x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-qwen-12x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-distil-12x4-aaronson/atoms.json",
        "experiments/2026-09-04-atoms-qwen-12x4-aaronson/atoms.json",
        "experiments/2026-09-04-atoms-distil-100x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-qwen-100x4-ngram13/atoms.json",
        "experiments/2026-09-04-atoms-distil-100x4-aaronson/atoms.json",
        "experiments/2026-09-04-atoms-qwen-100x4-aaronson/atoms.json",
    )
    for rel in dumps:
        occ = json.loads((ROOT / rel).read_text())
        assert occ["used_keys"] is False
        w0 = next(w for w in occ["windows"] if w["start"] == 0 and w["end"] == 4)
        assert f"**{occ['n_seen']}** seen vs **{occ['n_unseen']}** unseen" in text
        assert f"**{w0['n_seen']}** vs **{w0['n_unseen']}**" in text
    distil_aar12 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-distil-12x4-aaronson"
            / "results.json"
        ).read_text()
    )
    distil_aar100 = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-04-pair-distil-100x4-aaronson"
            / "results.json"
        ).read_text()
    )
    n12 = sum(row["unmarked_gen"]["z_score"] > 3.0 for row in distil_aar12["rows"])
    n100 = sum(
        row["unmarked_gen"]["z_score"] > 3.0 for row in distil_aar100["rows"]
    )
    assert f"z>3 **{n12}/12**" in text
    assert f"z>3 **{n100}/100**" in text
    assert "`ed9fb20`" in text
    assert "named before generation" in text


def test_narrative_tables_do_not_replace_25() -> None:
    text = NARRATIVE.read_text()
    assert "None of those occupancy-free or nested counts replace **25/48**" in text
    assert "GPT-2 36×4" in text
    assert "DistilGPT2" in text
    assert "Qwen2-1.5B" in text
    assert "`'The'→' car'`" in text
