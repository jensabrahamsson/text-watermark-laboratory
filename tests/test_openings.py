"""Opening-overlap bound: isolated recall equals train atom coverage."""

from text_watermark_tools.blind import Twin, clip_twins_prefix
from text_watermark_tools.openings import (
    TrainGroup,
    distinct_openings,
    run_openings,
    score_split,
    stem_curve,
)
from text_watermark_tools.probe import POSTOKBACKOFF2_SPEC, POSTOKHITS_SPEC
from text_watermark_tools.transfer import fit_count_model, score_sequence_detail


def _twin(stem: str, marked: list[int], unmarked: list[int]) -> Twin:
    return Twin(
        stem=stem,
        marked_text="m",
        unmarked_text="u",
        marked_ids=list(marked),
        unmarked_ids=list(unmarked),
    )


def _toy_train() -> list[Twin]:
    return clip_twins_prefix(
        [
            _twin("a", [10, 11, 12, 13], [10, 21, 22, 23]),
            _twin("b", [10, 11, 14, 15], [10, 21, 24, 25]),
            _twin("c", [30, 31, 32, 33], [30, 31, 32, 34]),
            _twin("d", [35, 36, 37, 38], [35, 36, 37, 39]),
        ],
        4,
    )


def test_covered_iff_n_used() -> None:
    train = _toy_train()
    test = clip_twins_prefix(
        [
            _twin("held-hit", [10, 11, 12, 13], [10, 21, 22, 23]),
            _twin("held-miss", [90, 91, 92, 93], [90, 91, 92, 94]),
        ],
        4,
    )
    split = score_split(
        train,
        test,
        POSTOKHITS_SPEC,
        name="postokhits",
        context_len=4,
        position_bucket=1,
        include_first=False,
        decode=lambda t: str(t),
        prefix_n=4,
    )
    assert split["used_keys"] is False
    by = {(r["stem"], r["side"], r["sample"]): r for r in split["rows"]}
    hit = by[("held-hit", "marked", 1)]
    miss = by[("held-miss", "marked", 1)]
    assert hit["covered"] is True
    assert hit["n_used"] > 0
    assert hit["exact_opening"] is True
    assert miss["covered"] is False
    assert miss["n_used"] == 0
    assert miss["exact_opening"] is False
    assert split["n_covered"] == 1
    assert split["n_exact_opening"] == 1


def test_stem_curve_is_monotonic_in_recall_and_openings() -> None:
    train = _toy_train()
    test = clip_twins_prefix(
        [_twin("held", [10, 11, 12, 13], [10, 21, 22, 23])],
        4,
    )
    points = stem_curve(
        train,
        test,
        POSTOKHITS_SPEC,
        name="postokhits",
        context_len=4,
        position_bucket=1,
        include_first=False,
        prefix_n=4,
    )
    recalls = [p["recall"] for p in points]
    openings = [p["n_train_openings"] for p in points]
    assert recalls == sorted(recalls)
    assert openings == sorted(openings)
    assert points[-1]["n_covered"] == 1
    assert points[0]["n_stems"] == 1


def test_distinct_openings_count_marked_prefixes() -> None:
    train = _toy_train()
    assert len(distinct_openings(train, 4)) == 4


def test_run_openings_curve_adds_groups() -> None:
    a = clip_twins_prefix([_twin("a", [10, 11, 12, 13], [10, 21, 22, 23])], 4)
    b = clip_twins_prefix([_twin("b", [40, 41, 42, 43], [40, 41, 42, 44])], 4)
    test = clip_twins_prefix(
        [_twin("held", [40, 41, 42, 43], [40, 41, 42, 44])],
        4,
    )
    payload = run_openings(
        [TrainGroup("first", a), TrainGroup("second", b)],
        test,
        methods=["postokhits", "postokbackoff", "postokbackoff2"],
        fit_prefix=4,
        position_bucket=1,
        include_first=False,
        with_stem_curve=False,
    )
    assert payload["used_keys"] is False
    first = payload["curve"][0]["methods"]["postokhits"]["n_covered"]
    second = payload["curve"][1]["methods"]["postokhits"]["n_covered"]
    assert first == 0
    assert second == 1
    assert payload["final"]["postokhits"]["n_covered"] == 1
    assert payload["final"]["postokbackoff"]["n_covered"] == 1
    assert payload["final"]["postokbackoff2"]["n_covered"] == 1


def test_pos_bucket_zero_is_unbucketed_tokhits() -> None:
    train = _toy_train()
    model = fit_count_model(train, context_len=4, position_bucket=0)
    held = [10, 11, 12, 13]
    pos = fit_count_model(train, context_len=4, position_bucket=1)
    u = score_sequence_detail(held, model, POSTOKHITS_SPEC)
    b = score_sequence_detail(held, pos, POSTOKHITS_SPEC)
    assert model.position_bucket in (0, None) or model.position_bucket == 0
    assert u.n_used > 0
    assert b.n_used > 0
    assert model.used_keys is False


def test_decode_token_maps_first_token_sentinel() -> None:
    from text_watermark_tools.atoms import decode_token
    from text_watermark_tools.score import load_tokenizer

    tok = load_tokenizer("gpt2")
    assert decode_token(tok, -1) == "<first>"
    assert isinstance(decode_token(tok, 220), str)


def test_combined_openings_backoff2_core_is_thirteen() -> None:
    import json
    from pathlib import Path

    payload = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-openings-short-medium-tails"
            / "coverage.json"
        ).read_text()
    )
    assert payload["used_keys"] is False
    hits = payload["final"]["postokhits"]
    back = payload["final"]["postokbackoff"]
    core = payload["final"]["postokbackoff2"]
    assert hits["n_covered"] == 30
    assert back["n_covered"] == 36
    assert core["n_covered"] == 13
    assert back["n_last1_later"] == 6
    assert hits["coverage_gate"]["decided_fp"] == 0
    assert back["coverage_gate"]["decided_fp"] == 0
    assert core["coverage_gate"]["decided_fp"] == 0
    assert hits["coverage_gate"]["precision"] == 1.0
    curve = payload["curve"]
    assert curve[0]["methods"]["postokbackoff2"]["n_covered"] == 13
    assert curve[1]["methods"]["postokbackoff2"]["n_covered"] == 13
    assert curve[2]["methods"]["postokbackoff2"]["n_covered"] == 13
    zeros = {z["opening_text"] for z in back["zeros"]}
    assert "Now in the second" in zeros
    assert "While working on the" in zeros
    assert any(s.startswith("The ferry was so") for s in zeros)
    last = payload["stem_curve"][-1]
    assert last["n_covered"] == 36
    assert last["n_train_openings"] == 63


def test_family12_pair_official_lamp_and_no_leftover_openings() -> None:
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-31-pair-family12x4"
    payload = json.loads((root / "results.json").read_text())
    assert payload["instance"] == "public-deepmind-30"
    rows = payload["rows"]
    assert len(rows) == 12
    assert all(
        float(r["marked"]["mean"]) > float(r["unmarked_gen"]["mean"]) for r in rows
    )
    assert min(float(r["marked"]["mean"]) for r in rows) > 0.57
    assert max(float(r["unmarked_gen"]["mean"]) for r in rows) < 0.52
    banned = ("Closing", "Now", "While", "After")
    for path in root.glob("*-marked*.txt"):
        if "unmarked" in path.name:
            continue
        text = path.read_text()
        assert not text.startswith(banned)
        assert not text.startswith("The ferry")
        assert not text.startswith("The printer")


def test_neighborhood_family_covers_ferry_last1_not_letter() -> None:
    import json
    from pathlib import Path

    payload = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-openings-short-medium-tails-family"
            / "coverage.json"
        ).read_text()
    )
    assert payload["used_keys"] is False
    hits = payload["final"]["postokhits"]
    back = payload["final"]["postokbackoff"]
    core = payload["final"]["postokbackoff2"]
    assert hits["n_covered"] == 38
    assert back["n_covered"] == 42
    assert core["n_covered"] == 15
    assert back["coverage_gate"]["decided_fp"] == 0
    assert back["coverage_gate"]["precision"] == 1.0
    zeros = {(z["stem"], z["sample"], z["opening_text"]) for z in back["zeros"]}
    assert ("08-letter", 2, "Now in the second") in zeros
    assert ("08-letter", 3, "While working on the") in zeros
    assert ("10-office", 1, "The printer worked.") in zeros
    assert not any(z[2].startswith("The ferry") for z in zeros)
    assert hits["n_exact_opening"] == 19


def test_unbucketed_tokbackoff_copies_recall_and_adds_fps() -> None:
    import json
    from pathlib import Path

    payload = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-openings-short-medium-tails-unbucketed"
            / "coverage.json"
        ).read_text()
    )
    assert payload["used_keys"] is False
    assert payload["position_bucket"] == 0
    back = payload["final"]["tokbackoff"]
    core = payload["final"]["tokbackoff2"]
    assert back["n_covered"] == 36
    assert core["n_covered"] == 13
    assert back["coverage_gate"]["decided_fp"] == 3
    assert core["coverage_gate"]["decided_fp"] == 2
    assert back["coverage_gate"]["precision"] < 1.0


def test_include_first_postokhits_is_first_token_unigram() -> None:
    import json
    from pathlib import Path

    payload = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-openings-short-medium-tails-includefirst"
            / "coverage.json"
        ).read_text()
    )
    assert payload["used_keys"] is False
    assert payload["include_first"] is True
    hits = payload["final"]["postokhits"]
    back = payload["final"]["postokbackoff"]
    assert hits["n_covered"] == 43
    assert hits["coverage_gate"]["decided_fp"] == 10
    assert back["n_covered"] == 36
    assert back["coverage_gate"]["decided_fp"] == 0
    zeros = {z["opening_text"] for z in hits["zeros"]}
    assert "Closing is the" in zeros
    assert "While working on the" in zeros
