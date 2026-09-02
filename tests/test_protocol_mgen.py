"""gpt2-medium occupancy-free leftover-15, frozen before medium→12 decode."""

import json
from pathlib import Path

from text_watermark_tools.generate import is_gpt2_name
from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.leftover import (
    leftover_keys_from_union,
    persist_mgen_leftover,
    print_mgen_leftover,
    summarize_mgen_leftover,
)
from text_watermark_tools.pair import (
    PairRow,
    pair_stem_files_complete,
    persist_pair_row_texts,
)
from text_watermark_tools.score import OfficialScore

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research" / "PROTOCOL-isolated-mgen.md"
TRAIN_PROMPTS = ROOT / "experiments" / "2026-09-01-prompts-100"
TEST_PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"
TEST = ROOT / "experiments" / "2026-08-17-pair-12x4"
UNION15 = (
    ROOT
    / "experiments"
    / "2026-09-01-openings-union-distil100x4-and-smt-to-12x4"
    / "union.json"
)


def _prompt_texts(folder: Path) -> set[str]:
    return {
        p.read_text().strip()
        for p in folder.glob("*.txt")
        if p.name != "README.md"
    }


def test_protocol_mgen_names_frozen_sources_before_decode() -> None:
    text = PROTOCOL.read_text()
    assert "25/48" in text
    assert "H-mgen-cover" in text
    assert "H-mgen-B" in text
    assert "H-mgen-iso" in text
    assert "leftover_keys_from_union" in text
    assert "summarize_mgen_leftover" in text
    assert "2026-09-01-prompts-100" in text
    assert "2026-09-01-pair-gpt2-medium-100x4" in text
    assert "2026-08-17-pair-12x4" in text
    assert "2026-09-01-openings-union-distil100x4-and-smt-to-12x4/union.json" in text
    assert "2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits" in text
    assert "2026-09-01-openings-gpt2-medium-100x4-to-12x4" in text
    assert "2026-09-01-isolated-mgen-leftover-15" in text
    assert "thesis/" in text
    assert "family-12" in text
    assert "Do not redefine leftover" in text
    assert "Do **not** mix grok12" in text
    assert "postokhits" in text
    assert "--model gpt2-medium" in text
    assert "Do **not** leftover-slice gpt2-medium rankpath" in text
    assert "Do **not** run lock A interpolate" in text
    assert "Do **not** target leftover-15" in text
    assert "openings after peeking" in text
    assert 'not "more GPT-2 scenes"' in text
    assert "*(empty until the SHA is named" not in text
    assert "H-mgen-cover **holds**" in text
    assert "H-mgen-B **holds**" in text
    assert "H-mgen-iso **holds**" in text
    assert "`cc9c4ca`" in (ROOT / "research" / "LOGBOOK.md").read_text()
    assert TEST.is_dir()
    assert UNION15.is_file()
    assert TRAIN_PROMPTS.is_dir()
    assert is_gpt2_name("gpt2-medium") is True


def test_mgen_train_and_test_prompts_are_disjoint() -> None:
    train = _prompt_texts(TRAIN_PROMPTS)
    test = _prompt_texts(TEST_PROMPTS)
    assert len(train) == 100
    assert len(test) == 12
    assert train.isdisjoint(test)


def test_mgen_leftover15_keys_are_the_dsmt_union() -> None:
    keys = leftover_keys_from_union(UNION15)
    assert len(keys) == 15
    union = json.loads(UNION15.read_text())
    assert union.get("used_keys") is False


def test_summarize_mgen_leftover_on_synthetic(tmp_path: Path) -> None:
    holdout = {
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "files": [
            {"stem": "left", "sample": 1, "file": "left-marked.txt", "lr": 0.2},
            {"stem": "left", "sample": 1, "file": "left-unmarked-gen.txt", "lr": -0.1},
            {"stem": "cov", "sample": 1, "file": "cov-marked.txt", "lr": -0.4},
            {"stem": "cov", "sample": 1, "file": "cov-unmarked-gen.txt", "lr": 0.1},
        ],
    }
    hold_path = tmp_path / "holdout.json"
    hold_path.write_text(json.dumps(holdout))
    openings = {
        "used_keys": False,
        "final": {
            "postokhits": {
                "n_covered": 1,
                "n_train_openings": 3,
                "zeros": [{"stem": "left", "sample": 1}],
            }
        },
    }
    cov_path = tmp_path / "coverage.json"
    cov_path.write_text(json.dumps(openings))
    payload = summarize_mgen_leftover(
        {("left", 1), ("cov", 1)},
        holdouts={"medium-postokhits": hold_path},
        openings=cov_path,
    )
    assert payload["used_keys"] is False
    assert payload["n_leftover"] == 2
    by = {row["label"]: row for row in payload["leftover_signs"]}
    assert by["medium-postokhits"]["marked_above_zero"] == 1
    assert by["medium-postokhits"]["unmarked_at_most_zero"] == 1
    assert payload["openings"]["n_covered"] == 1
    assert payload["openings"]["n_uncovered"] == 1
    rendered = print_mgen_leftover(payload)
    assert "leftover-15" in rendered
    assert "Does not replace 25/48" in rendered
    persist_mgen_leftover(payload, tmp_path / "out")
    assert (tmp_path / "out" / "mgen.json").is_file()


def test_pair_stem_files_complete_and_persist_row_texts(tmp_path: Path) -> None:
    dummy = OfficialScore(mean=0.5, weighted_mean=0.5, n_tokens=8, n_unmasked_ngrams=4)
    row = PairRow(
        stem="harbour",
        prompt="The harbour lights.\n",
        prompt_score=dummy,
        marked_text="marked one",
        marked_score=dummy,
        unmarked_text="unmarked one",
        unmarked_score=dummy,
        extra_marked=[("marked two", dummy)],
        extra_unmarked=[("unmarked two", dummy)],
    )
    persist_pair_row_texts(row, tmp_path)
    assert pair_stem_files_complete(tmp_path, "harbour", 2)
    assert not pair_stem_files_complete(tmp_path, "harbour", 3)
    assert (tmp_path / "harbour-marked-2.txt").read_text() == "marked two\n"
    assert not pair_stem_files_complete(tmp_path, "missing", 1)


def test_gpt2_medium_occupancy_free_leftover15_is_zero() -> None:
    dump = ROOT / "experiments" / "2026-09-01-isolated-mgen-leftover-15"
    raw = json.loads((dump / "mgen.json").read_text())
    assert raw["used_keys"] is False
    assert raw["n_leftover"] == 15
    by = {row["label"]: row for row in raw["leftover_signs"]}
    assert by["medium-postokhits"]["marked_above_zero"] == 0
    assert by["medium-postokhits"]["unmarked_at_most_zero"] == 15
    cov = raw["openings"]
    assert cov["n_covered"] == 0
    assert cov["n_uncovered"] == 15
    assert cov["n_marked_covered"] == 16
    assert cov["covered"] == []
    probe = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits"
            / "results.json"
        ).read_text()
    )
    assert probe["used_keys"] is False
    methods = {m["name"]: m for m in probe["methods"]}
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] == 16
    assert methods["postokhits"]["binary"]["n_negative_at_most_zero"] == 48
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] == 16
    assert methods["postokhits"]["binary"]["n_positive_above_zero"] < 25
    openings = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-01-openings-gpt2-medium-100x4-to-12x4"
            / "coverage.json"
        ).read_text()
    )
    assert openings["used_keys"] is False
    post = openings["final"]["postokhits"]
    assert post["n_covered"] == 16
    assert post["n_exact_opening"] == 14
    assert post["coverage_gate"]["decided_fp"] == 0
    ev = holdout_from_json(
        ROOT
        / "experiments"
        / "2026-09-01-transfer-gpt2-medium-100x4-to-12x4-opening-poshits"
        / "postokhits"
        / "holdout.json"
    )
    assert ev.n_prompts_marked_above == 7
    assert ev.n_prompt_ties == 5
    assert ev.n_prompts_marked_ge == 12
    pair = json.loads(
        (ROOT / "experiments" / "2026-09-01-pair-gpt2-medium-100x4" / "results.json").read_text()
    )
    wins = sum(
        1
        for row in pair["rows"]
        if row["marked"]["mean"] > row["unmarked_gen"]["mean"]
    )
    assert pair["model_name"] == "gpt2-medium"
    assert pair["seed"] == 20260901
    assert wins == 100
    text = PROTOCOL.read_text()
    assert "H-mgen-cover **holds**" in text
    assert "H-mgen-B **holds**" in text
    assert "H-mgen-iso **holds**" in text
    assert "sell leftover official **15/15**" in text
    log = (ROOT / "research" / "LOGBOOK.md").read_text()
    assert "gpt2-medium occupancy-free leftover-15 opened" in log
