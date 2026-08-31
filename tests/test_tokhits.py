"""tokhits skips Laplace unseen-token scores after a shared context."""

from text_watermark_tools.blind import Twin, clip_twins_prefix
from text_watermark_tools.probe import POSHITS_SPEC, POSTOKHITS_SPEC
from text_watermark_tools.stats import coverage_gate
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    fit_count_model,
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
