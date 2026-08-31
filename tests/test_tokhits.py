"""tokhits skips Laplace unseen-token scores after a shared context."""

from text_watermark_tools.blind import Twin, clip_twins_prefix
from text_watermark_tools.probe import (
    POSHITS_SPEC,
    POSTOKBACKOFF_SPEC,
    POSTOKHITS_SPEC,
)
from text_watermark_tools.stats import coverage_gate
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    fit_count_model,
    gated_hit_trace,
    score_sequence_detail,
)


def _twin(stem: str, marked: list[int], unmarked: list[int]) -> Twin:
    return Twin(
        stem=stem,
        marked_text="m",
        unmarked_text="u",
        marked_ids=list(marked),
        unmarked_ids=list(unmarked),
    )


def test_tokhits_skips_unseen_next_token_after_shared_the() -> None:
    train = [
        _twin("t1", [10, 11, 12, 13], [10, 21, 22, 23]),
        _twin("t2", [10, 11, 14, 15], [10, 21, 24, 25]),
        # Marked uses 10 less often, so Laplace unseen-after-10 is positive.
        _twin("t3", [30, 31, 32, 33], [10, 21, 26, 27]),
        _twin("t4", [30, 34, 35, 36], [10, 21, 28, 29]),
    ]
    train = clip_twins_prefix(train, 4)
    counts = fit_count_model(train, context_len=4)
    pos = fit_count_model(train, context_len=4, position_bucket=1)
    unseen = [10, 99, 50, 51]
    hits = score_sequence_detail(unseen, counts, COUNT_SPECS["hits"])
    tokhits = score_sequence_detail(unseen, counts, COUNT_SPECS["tokhits"])
    poshits = score_sequence_detail(unseen, pos, POSHITS_SPEC)
    postok = score_sequence_detail(unseen, pos, POSTOKHITS_SPEC)
    assert hits.n_used > 0
    assert poshits.n_used > 0
    assert hits.lr > 0.0
    assert poshits.lr > 0.0
    assert tokhits.n_used == 0
    assert tokhits.lr == 0.0
    assert postok.n_used == 0
    assert postok.lr == 0.0
    seen = [10, 11, 50, 51]
    seen_tok = score_sequence_detail(seen, pos, POSTOKHITS_SPEC)
    assert seen_tok.n_used > 0
    assert seen_tok.lr != 0.0
    assert counts.used_keys is False
    assert pos.used_keys is False
    trace = gated_hit_trace(unseen, pos, POSHITS_SPEC)
    assert trace
    assert all(a.unseen_next for a in trace)
    assert all(a.delta > 0.0 for a in trace)
    skipped = gated_hit_trace(unseen, pos, POSTOKHITS_SPEC)
    assert skipped == []


def test_tokbackoff_uses_shorter_context_when_full_ngram_unseen_token() -> None:
    train = clip_twins_prefix(
        [
            _twin("t1", [10, 11, 12, 13], [10, 11, 12, 23]),
            _twin("t2", [40, 41, 12, 99], [40, 41, 12, 51]),
            _twin("t3", [30, 31, 32, 33], [30, 31, 32, 34]),
            _twin("t4", [35, 36, 37, 38], [35, 36, 37, 39]),
        ],
        4,
    )
    pos = fit_count_model(train, context_len=4, position_bucket=1)
    held = [90, 91, 12, 99]
    postok = score_sequence_detail(held, pos, POSTOKHITS_SPEC)
    backoff = score_sequence_detail(held, pos, COUNT_SPECS["tokbackoff"])
    pos_back = score_sequence_detail(held, pos, POSTOKBACKOFF_SPEC)
    assert postok.n_used == 0
    assert postok.lr == 0.0
    assert backoff.n_used > 0
    assert backoff.lr > 0.0
    assert pos_back.n_used > 0
    assert pos_back.lr > 0.0
    assert pos.used_keys is False
    trace = gated_hit_trace(held, pos, POSTOKBACKOFF_SPEC)
    assert trace
    assert all(not a.unseen_next for a in trace)


def test_coverage_gate_treats_zeros_as_abstain_not_sign_errors() -> None:
    g = coverage_gate(
        [0.33, 0.0, 4.0, 0.0],
        [0.33, 0.0, -0.6, 0.0],
    )
    assert g.n_marked_zero == 2
    assert g.n_unmarked_zero == 2
    assert g.decided_tp == 2
    assert g.decided_fn == 0
    assert g.decided_fp == 1
    assert g.decided_tn == 1
    assert g.precision == 2 / 3


def test_poshits_ood_zeros_are_the_isolated_file_misses() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix4-pos1"
        / "poshits"
        / "holdout.json"
    )
    g = coverage_gate(ev.marked_lrs, ev.unmarked_lrs)
    assert ev.n_marked_positive == 39
    assert g.n_marked_zero == 9
    assert g.decided_fn == 0
    assert g.decided_tp == 39
    assert g.decided_fp == 7
    assert g.n_unmarked_zero == 33


def test_postokhits_ood_is_observed_token_only() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits"
    )
    ev = holdout_from_json(root / "postokhits" / "holdout.json")
    g = coverage_gate(ev.marked_lrs, ev.unmarked_lrs)
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 16
    assert ev.n_unmarked_nonpositive == 48
    assert g.n_marked_zero == 32
    assert g.n_unmarked_zero == 44
    assert g.decided_tp == 16
    assert g.decided_fn == 0
    assert g.decided_fp == 0
    assert g.decided_tn == 4
    assert g.precision == 1.0
    pos = holdout_from_json(root / "poshits" / "holdout.json")
    assert pos.n_prompts_marked_above == 12
    assert pos.n_marked_positive == 39


def test_postokhits_36x4_loo_keeps_most_in_domain_hits() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36x4-fitprefix4-postokhits"
    )
    pos = holdout_from_json(root / "poshits" / "holdout.json")
    tok = holdout_from_json(root / "postokhits" / "holdout.json")
    assert pos.used_keys is False
    assert tok.used_keys is False
    assert pos.n_prompts_marked_above == 34
    assert tok.n_prompts_marked_above == 34
    assert pos.n_marked_positive == 131
    assert tok.n_marked_positive == 122
    assert pos.n_unmarked_nonpositive == 132
    assert tok.n_unmarked_nonpositive == 132
    g = coverage_gate(tok.marked_lrs, tok.unmarked_lrs)
    assert g.n_marked_zero == 19
    assert g.decided_fp == 12


def test_the_laplace_atom_is_occupancy_not_token_preference() -> None:
    import json
    from pathlib import Path

    payload = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits"
            / "atoms.json"
        ).read_text()
    )
    assert payload["used_keys"] is False
    the = [
        a
        for a in payload["atom_counts"]
        if a["ctx"] == ["The"] and a["unseen_next"]
    ]
    assert the
    assert all(abs(a["delta"] - 0.330103) < 1e-5 for a in the)
    unseen_n = sum(a["n"] for a in payload["atom_counts"] if a["unseen_next"])
    seen_n = sum(a["n"] for a in payload["atom_counts"] if not a["unseen_next"])
    assert unseen_n >= 20
    assert seen_n >= 20
    zeros = [
        r
        for r in payload["rows"]
        if r["side"] == "marked" and abs(r["poshits_lr"]) <= 1e-15
    ]
    openings = ["".join(r["opening"]).strip() for r in zeros]
    assert any(s.startswith("After") for s in openings)
    assert any(s.startswith("Cl") for s in openings)
    assert any(s.startswith("Now") for s in openings)
    assert any(s.startswith("While") for s in openings)


def test_long12_pair_official_lamp_is_twelve_of_twelve() -> None:
    import json
    from pathlib import Path

    payload = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-pair-long12x4"
            / "results.json"
        ).read_text()
    )
    assert payload["instance"] == "public-deepmind-30"
    rows = payload["rows"]
    assert len(rows) == 12
    assert all(
        float(r["marked"]["mean"]) > float(r["unmarked_gen"]["mean"]) for r in rows
    )
    assert min(float(r["marked"]["mean"]) for r in rows) > 0.57
    assert max(float(r["unmarked_gen"]["mean"]) for r in rows) < 0.52


def test_medium_length_postokhits_ood_is_nineteen_with_perfect_precision() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokhits"
    )
    ev = holdout_from_json(root / "postokhits" / "holdout.json")
    g = coverage_gate(ev.marked_lrs, ev.unmarked_lrs)
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 19
    assert ev.n_unmarked_nonpositive == 48
    assert g.n_marked_zero == 29
    assert g.decided_tp == 19
    assert g.decided_fn == 0
    assert g.decided_fp == 0
    assert g.precision == 1.0
    pos = holdout_from_json(root / "poshits" / "holdout.json")
    pg = coverage_gate(pos.marked_lrs, pos.unmarked_lrs)
    assert pos.n_prompts_marked_above == 8
    assert pg.n_marked_zero == 9
    assert pg.decided_fn == 20


def test_combined_short_plus_medium_postokhits_is_twenty() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-short24-plus-long12-to-12x4-fitprefix4-tokhits"
    )
    ev = holdout_from_json(root / "postokhits" / "holdout.json")
    g = coverage_gate(ev.marked_lrs, ev.unmarked_lrs)
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 20
    assert ev.n_unmarked_nonpositive == 48
    assert g.n_marked_zero == 28
    assert g.decided_tp == 20
    assert g.decided_fn == 0
    assert g.decided_fp == 0
    assert g.precision == 1.0


def test_medium_the_laplace_flips_sign_and_zeros_stay() -> None:
    import json
    from pathlib import Path

    payload = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokhits"
            / "atoms.json"
        ).read_text()
    )
    assert payload["used_keys"] is False
    the = [
        a
        for a in payload["atom_counts"]
        if a["ctx"] == ["The"] and a["unseen_next"]
    ]
    assert the
    assert all(a["delta"] < -0.3 for a in the)
    assert all(abs(a["delta"] + 0.364898) < 1e-4 for a in the)
    zeros = [
        r
        for r in payload["rows"]
        if r["side"] == "marked" and abs(r["poshits_lr"]) <= 1e-15
    ]
    openings = ["".join(r["opening"]).strip() for r in zeros]
    assert any(s.startswith("After") for s in openings)
    assert any(s.startswith("Cl") for s in openings)
    assert any(s.startswith("Now") for s in openings)
    assert any(s.startswith("While") for s in openings)
    stems = {r["stem"] for r in zeros}
    assert stems == {"02-night-bus", "03-library", "08-letter", "11-garden"}


def test_postokbackoff_copies_postokhits_on_short_train_ood() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokbackoff"
    )
    ev = holdout_from_json(root / "postokbackoff" / "holdout.json")
    tok = holdout_from_json(root / "postokhits" / "holdout.json")
    g = coverage_gate(ev.marked_lrs, ev.unmarked_lrs)
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 16
    assert tok.n_marked_positive == 16
    assert ev.n_unmarked_nonpositive == 48
    assert g.decided_tp == 16
    assert g.decided_fp == 0
    assert g.precision == 1.0


def test_medium_postokbackoff_adds_two_harbour_files() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokbackoff"
    )
    back = holdout_from_json(root / "postokbackoff" / "holdout.json")
    tok = holdout_from_json(root / "postokhits" / "holdout.json")
    g = coverage_gate(back.marked_lrs, back.unmarked_lrs)
    assert back.used_keys is False
    assert back.n_prompts_marked_above == 12
    assert tok.n_marked_positive == 19
    assert back.n_marked_positive == 21
    assert back.n_unmarked_nonpositive == 48
    assert g.decided_tp == 21
    assert g.decided_fp == 0
    assert g.precision == 1.0
    new = [
        (s, i)
        for s, i, m, t in zip(
            back.stems, back.samples, back.marked_lrs, tok.marked_lrs
        )
        if m > 0 and abs(t) <= 1e-15
    ]
    assert new == [("01-harbour", 3), ("01-harbour", 4)]


def test_combined_postokbackoff_is_twenty_two() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-short24-plus-long12-to-12x4-fitprefix4-tokbackoff"
    )
    ev = holdout_from_json(root / "postokbackoff" / "holdout.json")
    g = coverage_gate(ev.marked_lrs, ev.unmarked_lrs)
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 22
    assert g.decided_fp == 0
    assert g.precision == 1.0


def test_postokbackoff_36x4_loo_does_not_add_marked_hits() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36x4-fitprefix4-postokbackoff"
    )
    tok = holdout_from_json(root / "postokhits" / "holdout.json")
    back = holdout_from_json(root / "postokbackoff" / "holdout.json")
    assert tok.n_marked_positive == 122
    assert back.n_marked_positive == 122
    assert tok.n_unmarked_nonpositive == 132
    assert back.n_unmarked_nonpositive == 131
    assert back.n_prompts_marked_above == 34


def test_postokbackoff_contrast_control_never_positive() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokbackoff"
        / "postokbackoff-control-vs-unmarked"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_marked_positive == 0
    vs = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokbackoff"
        / "postokbackoff-public-vs-control"
        / "holdout.json"
    )
    assert vs.n_prompts_marked_above == 12


def test_tails12_pair_official_lamp_and_after_opening() -> None:
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-31-pair-tails12x4"
    payload = json.loads((root / "results.json").read_text())
    assert payload["instance"] == "public-deepmind-30"
    rows = payload["rows"]
    assert len(rows) == 12
    assert all(
        float(r["marked"]["mean"]) > float(r["unmarked_gen"]["mean"]) for r in rows
    )
    after = (root / "54-bakery-depot-marked-3.txt").read_text()
    assert after.startswith("After two and a")
    now = (root / "55-bakery-letter-marked.txt").read_text()
    assert now.startswith("Now a little after")
    closings = []
    for path in root.glob("*-marked*.txt"):
        if "unmarked" in path.name:
            continue
        if path.read_text().startswith("Closing"):
            closings.append(path.name)
    assert closings == []


def test_tail_transplant_postokhits_covers_night_bus_and_garden() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-tails12x4-to-12x4-fitprefix4-tokbackoff"
    )
    tok = holdout_from_json(root / "postokhits" / "holdout.json")
    back = holdout_from_json(root / "postokbackoff" / "holdout.json")
    g = coverage_gate(tok.marked_lrs, tok.unmarked_lrs)
    gb = coverage_gate(back.marked_lrs, back.unmarked_lrs)
    assert tok.used_keys is False
    assert tok.n_prompts_marked_above == 12
    assert tok.n_marked_positive == 10
    assert back.n_marked_positive == 23
    assert g.decided_fp == 0
    assert gb.decided_fp == 0
    assert g.precision == 1.0
    assert gb.precision == 1.0
    by = {(s, i): m for s, i, m in zip(tok.stems, tok.samples, tok.marked_lrs)}
    bb = {(s, i): m for s, i, m in zip(back.stems, back.samples, back.marked_lrs)}
    assert by[("02-night-bus", 3)] > 0
    assert by[("11-garden", 1)] > 0
    assert by[("11-garden", 4)] > 0
    assert abs(by[("03-library", 1)]) <= 1e-15
    assert bb[("03-library", 1)] > 0
    assert abs(by[("08-letter", 2)]) <= 1e-15
    assert abs(bb[("08-letter", 2)]) <= 1e-15


def test_combined_tails_postokbackoff_is_thirty_six() -> None:
    from pathlib import Path

    from text_watermark_tools.indicator import holdout_from_json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-short-medium-tails-to-12x4-fitprefix4-tokbackoff"
    )
    tok = holdout_from_json(root / "postokhits" / "holdout.json")
    back = holdout_from_json(root / "postokbackoff" / "holdout.json")
    g = coverage_gate(back.marked_lrs, back.unmarked_lrs)
    assert tok.n_prompts_marked_above == 12
    assert back.n_prompts_marked_above == 12
    assert tok.n_marked_positive == 30
    assert back.n_marked_positive == 36
    assert back.n_unmarked_nonpositive == 48
    assert g.decided_tp == 36
    assert g.decided_fp == 0
    assert g.precision == 1.0
    by = {(s, i): m for s, i, m in zip(tok.stems, tok.samples, tok.marked_lrs)}
    bb = {(s, i): m for s, i, m in zip(back.stems, back.samples, back.marked_lrs)}
    assert abs(by[("08-letter", 3)]) <= 1e-15
    assert abs(bb[("08-letter", 3)]) <= 1e-15
    assert abs(by[("03-library", 2)]) <= 1e-15
    assert bb[("03-library", 2)] > 0
