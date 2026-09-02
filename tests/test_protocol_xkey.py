"""Second-key in-domain lock A, frozen before control-as-marked LRs."""

import json
from pathlib import Path

from text_watermark_tools.blind import load_twins
from text_watermark_tools.contrast import (
    CONTROL_RE,
    control_gen_to_marked_name,
    materialize_control_as_marked,
)
from text_watermark_tools.stats import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-xkey.md"
CONTROL = ROOT / "experiments" / "2026-08-31-pair-12x4-controlkeys"
UNMARKED = ROOT / "experiments" / "2026-08-17-pair-12x4"
PAIR = ROOT / "experiments" / "2026-09-02-pair-12x4-control-as-marked"
PROBE = (
    ROOT / "experiments" / "2026-09-02-probe-12x4-control-as-marked-hard-last4"
)


def test_protocol_xkey_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-xkey-A" in text
    assert "H-xkey-iso" in text
    assert "H-xkey-seed" in text
    assert "2026-08-31-pair-12x4-controlkeys" in text
    assert "2026-08-17-pair-12x4" in text
    assert "2026-09-02-pair-12x4-control-as-marked" in text
    assert "2026-09-02-probe-12x4-control-as-marked-hard-last4" in text
    assert "--methods interpolate --context-len 4" in text
    assert "materialize_control_as_marked" in text
    assert "20260931" in text
    assert "seed **0**" in text
    assert "matched `pair()`" in text
    assert "Do **not** mix grok12" in text
    assert "thesis/" in text
    assert "leftover-15" in text
    assert "Distil ∪ gpt2-medium" in text
    assert "key-free-contrast.md" in text
    assert "PROTOCOL-isolated-windows-absolute" in text
    assert "*(empty until the SHA is named in LOGBOOK.md)*" not in text
    assert "H-xkey-A **holds**" in text
    assert "H-xkey-iso **fails**" in text
    assert "H-xkey-seed **holds**" in text
    assert "Do not sell **30/48**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "`d25e495`" in log
    assert "`9ec3b0c`" in log
    assert CONTROL.is_dir()
    assert UNMARKED.is_dir()
    assert PAIR.is_dir()
    assert (PROBE / "results.json").is_file()


def test_control_gen_maps_onto_marked_names() -> None:
    assert control_gen_to_marked_name("01-harbour-control-gen.txt") == (
        "01-harbour-marked.txt"
    )
    assert control_gen_to_marked_name("01-harbour-control-gen-2.txt") == (
        "01-harbour-marked-2.txt"
    )
    assert control_gen_to_marked_name("12-ferry-queue-control-gen-4.txt") == (
        "12-ferry-queue-marked-4.txt"
    )
    assert control_gen_to_marked_name("01-harbour-marked.txt") is None
    n = 0
    for path in CONTROL.glob("*-control-gen*.txt"):
        mapped = control_gen_to_marked_name(path.name)
        assert mapped is not None
        n += 1
    assert n == 48


def test_control_as_marked_pair_loads_twelve_by_four() -> None:
    twins = load_twins(PAIR)
    assert len(twins) == 12
    n_marked = sum(len(t.marked_seqs()) for t in twins)
    n_unmarked = sum(len(t.unmarked_seqs()) for t in twins)
    assert n_marked == 48
    assert n_unmarked == 48
    control_stems = {
        CONTROL_RE.fullmatch(p.name).group(1)
        for p in CONTROL.glob("*-control-gen.txt")
    }
    assert {t.stem for t in twins} == control_stems
    text = (PAIR / "README.md").read_text()
    assert "20260931" in text or "seed" in text.lower()
    assert "PROTOCOL-isolated-xkey" in text


def test_materialize_control_as_marked_is_idempotent(tmp_path) -> None:
    out = tmp_path / "pair"
    first = materialize_control_as_marked(CONTROL, UNMARKED, out)
    second = materialize_control_as_marked(CONTROL, UNMARKED, out)
    assert first["n_marked"] == 48
    assert second["n_unmarked"] == 48
    assert first["used_keys"] is False
    twins = load_twins(out)
    assert len(twins) == 12
    harbour = next(t for t in twins if t.stem == "01-harbour")
    src = (CONTROL / "01-harbour-control-gen.txt").read_text()
    assert harbour.marked_text == src
    unmarked = (UNMARKED / "01-harbour-unmarked-gen.txt").read_text()
    assert harbour.unmarked_text == unmarked


def test_xkey_interpolate_last4_from_holdout() -> None:
    raw = json.loads((PROBE / "results.json").read_text())
    assert raw["used_keys"] is False
    assert raw["used_hash_iv"] is False
    assert raw["used_g_values"] is False
    assert raw["pair_dir"] == "experiments/2026-09-02-pair-12x4-control-as-marked"
    methods = {m["name"]: m for m in raw["methods"]}
    row = methods["interpolate"]
    assert row["n_prompt_wins"] == 7
    assert row["n_prompts"] == 12
    assert row["n_prompt_ties"] == 0
    assert row["binary"]["n_positive_above_zero"] == 30
    assert row["binary"]["n_negative_at_most_zero"] == 25
    assert abs(row["binary"]["auc"] - 0.590) < 0.001
    assert row["ranking_without_isolated_tp"] == ["11-garden"]
    nested = row["nested_stem"]["nested-youden-by-stem"]
    assert nested["n_marked_above"] == 33
    assert nested["n_unmarked_at_most"] == 20
    lo, hi = clopper_pearson(30, 48)
    assert lo < 0.5 < hi
    plo, phi = clopper_pearson(7, 12)
    assert plo < 0.5 < phi
    text = PROTOCOL.read_text()
    assert "H-xkey-A **holds**" in text
    assert "H-xkey-iso **fails**" in text
    assert "H-xkey-seed **holds**" in text
    assert "Do not sell **30/48**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "second-key in-domain lock A opened" in log
    assert "`9ec3b0c`" in log
