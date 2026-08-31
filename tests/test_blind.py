"""Key-free blind detector: counts only, no keys."""

from pathlib import Path

from text_watermark_tools.blind import (
    Twin,
    FIRST_TOKEN_CTX,
    _scored_ctx,
    clip_twins,
    fit_blind,
    leave_one_prompt_out,
    likelihood_ratio,
    load_twins,
    pair_marked_wins,
)
from text_watermark_tools.cli import main

PAIR = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-17-pair"


def test_position_bucket_namespaces_the_same_last_k() -> None:
    ids = [10, 20, 30, 40, 50, 60]
    assert _scored_ctx(ids, 4, 4, 0) == (10, 20, 30, 40)
    assert _scored_ctx(ids, 4, 4, 16) == (0, 10, 20, 30, 40)
    later = list(range(25))
    assert _scored_ctx(later, 20, 4, 16)[0] == 20 // 16
    assert _scored_ctx(later, 20, 4, 16)[1:] == _scored_ctx(later, 20, 4, 0)
    assert _scored_ctx(ids, 0, 4, 0) == FIRST_TOKEN_CTX
    assert _scored_ctx(ids, 1, 4, 0) == (10,)
    prompt = (7, 8, 9, 1)
    assert _scored_ctx(ids, 0, 4, 0, prefix=prompt) == prompt
    assert _scored_ctx(ids, 1, 4, 0, prefix=prompt) == (8, 9, 1, 10)
    assert _scored_ctx(ids, 0, 4, 1, prefix=prompt)[0] == 0


def test_margin_turns_a_close_miss_into_a_hit() -> None:
    assert pair_marked_wins(0.01, 0.02, margin=0.0) is False
    assert pair_marked_wins(0.01, 0.02, margin=0.015) is True
    assert pair_marked_wins(-0.05, 0.02, margin=0.015) is False


def test_clip_twins_keeps_the_first_n_draws() -> None:
    twin = Twin(
        stem="x",
        marked_text="a",
        unmarked_text="b",
        marked_ids=[1],
        unmarked_ids=[2],
        extra_marked_ids=[[3], [4], [5]],
        extra_unmarked_ids=[[6], [7], [8]],
        extra_marked_text=["c", "d", "e"],
        extra_unmarked_text=["f", "g", "h"],
    )
    one = clip_twins([twin], 1)[0]
    assert one.extra_marked_ids == []
    assert one.extra_unmarked_text == []
    assert len(one.marked_seqs()) == 1
    two = clip_twins([twin], 2)[0]
    assert two.extra_marked_ids == [[3]]
    assert two.extra_unmarked_ids == [[6]]
    assert len(two.marked_seqs()) == 2
    four = clip_twins([twin], 4)[0]
    assert len(four.marked_seqs()) == 4


def test_clip_twins_rejects_zero_draws() -> None:
    twin = Twin(
        stem="x",
        marked_text="a",
        unmarked_text="b",
        marked_ids=[1],
        unmarked_ids=[2],
    )
    try:
        clip_twins([twin], 0)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_blind_separates_synthetic_alternating_tokens() -> None:
    marked = [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2, 0, 2]]
    model = fit_blind(marked, unmarked, context_len=1, alpha=0.5)
    assert model.used_keys is False
    assert model.used_hash_iv is False
    assert model.used_g_values is False
    held_marked = [0, 1, 0, 1, 0, 1]
    held_unmarked = [0, 2, 0, 2, 0, 2]
    assert likelihood_ratio(held_marked, model) > likelihood_ratio(
        held_unmarked, model
    )


def test_include_first_scores_token_zero_as_a_unigram() -> None:
    from text_watermark_tools.transfer import COUNT_SPECS, score_sequence

    marked = [[1, 9, 9, 9], [1, 8, 8, 8], [1, 7, 7, 7]]
    unmarked = [[2, 9, 9, 9], [2, 8, 8, 8], [2, 7, 7, 7]]
    skipped = fit_blind(marked, unmarked, context_len=1)
    first = fit_blind(marked, unmarked, context_len=1, include_first=True)
    held_m = [1]
    held_u = [2]
    assert skipped.include_first is False
    assert first.include_first is True
    assert likelihood_ratio(held_m, skipped) == 0.0
    assert likelihood_ratio(held_u, skipped) == 0.0
    assert likelihood_ratio(held_m, first) > likelihood_ratio(held_u, first)
    spec = COUNT_SPECS["first"]
    assert score_sequence(held_m, first, spec) > score_sequence(held_u, first, spec)
    assert score_sequence(held_m, skipped, COUNT_SPECS["hits"]) == 0.0


def test_prompt_context_uses_prompt_last_k_at_token_zero() -> None:
    from text_watermark_tools.transfer import COUNT_SPECS, fit_count_model, score_sequence

    twins = [
        Twin(
            "a",
            "a",
            "a",
            [3, 9],
            [4, 9],
            prompt_ids=[10, 11, 12, 13],
        ),
        Twin(
            "b",
            "b",
            "b",
            [3, 8],
            [4, 8],
            prompt_ids=[10, 11, 12, 13],
        ),
        Twin(
            "c",
            "c",
            "c",
            [3, 7],
            [4, 7],
            prompt_ids=[10, 11, 12, 13],
        ),
    ]
    model = fit_count_model(
        twins[:2], context_len=4, prompt_context=True, include_first=True
    )
    assert model.prompt_context is True
    prefix = tuple(twins[2].prompt_ids)
    marked = score_sequence(
        twins[2].marked_ids, model, COUNT_SPECS["hits"], prefix=prefix
    )
    unmarked = score_sequence(
        twins[2].unmarked_ids, model, COUNT_SPECS["hits"], prefix=prefix
    )
    assert marked > unmarked


def test_load_twins_reads_prompt_ids() -> None:
    twins = load_twins(PAIR)
    assert twins[0].prompt_ids
    assert twins[0].prompt_text


def test_backoff_uses_shorter_context_when_full_ngram_is_new() -> None:
    """Train last-3 on 9,8,1; hold out 3,8,1. Exact 3-gram is new; last-2 is not."""
    marked = [[9, 8, 1, 9, 8, 1, 9, 8, 1, 9, 8, 1]]
    unmarked = [[9, 8, 2, 9, 8, 2, 9, 8, 2, 9, 8, 2]]
    held_m = [3, 8, 1, 3, 8, 1, 3, 8, 1]
    held_u = [3, 8, 2, 3, 8, 2, 3, 8, 2]
    hard = fit_blind(marked, unmarked, context_len=3, backoff=False)
    soft = fit_blind(marked, unmarked, context_len=3, backoff=True)
    assert hard.used_keys is False and soft.used_keys is False
    # Without backoff the unseen 3-gram falls to unigram and the two LRs collapse.
    # With backoff, last-2 (8 → 1 vs 2) still separates.
    assert likelihood_ratio(held_m, soft) > likelihood_ratio(held_u, soft)
    assert (likelihood_ratio(held_m, soft) - likelihood_ratio(held_u, soft)) > (
        likelihood_ratio(held_m, hard) - likelihood_ratio(held_u, hard)
    )


def test_leave_one_out_prefers_matching_pile() -> None:
    twins = [
        Twin("a", "a", "a", [0, 1, 0, 1, 0, 1, 0, 1], [0, 2, 0, 2, 0, 2, 0, 2]),
        Twin("b", "b", "b", [0, 1, 0, 1, 0, 1, 0, 1], [0, 2, 0, 2, 0, 2, 0, 2]),
        Twin("c", "c", "c", [0, 1, 0, 1, 0, 1, 0, 1], [0, 2, 0, 2, 0, 2, 0, 2]),
    ]
    ev = leave_one_prompt_out(twins, context_len=1)
    assert ev.used_keys is False
    assert ev.n_marked_wins == 3
    assert ev.accuracy == 1.0


def test_load_twins_groups_extra_marked_samples(tmp_path: Path) -> None:
    (tmp_path / "harbour-marked.txt").write_text("alpha marked")
    (tmp_path / "harbour-unmarked-gen.txt").write_text("alpha unmarked")
    (tmp_path / "harbour-marked-2.txt").write_text("beta marked")
    (tmp_path / "harbour-unmarked-gen-2.txt").write_text("beta unmarked")
    twins = load_twins(tmp_path)
    assert len(twins) == 1
    assert twins[0].stem == "harbour"
    assert len(twins[0].marked_seqs()) == 2
    assert len(twins[0].unmarked_seqs()) == 2


def test_load_twins_from_lab_pair_dir() -> None:
    twins = load_twins(PAIR)
    assert len(twins) >= 3
    stems = {t.stem for t in twins}
    assert "01-harbour" in stems
    assert twins[0].marked_ids
    assert twins[0].unmarked_ids


def test_cli_blind_on_lab_pairs_is_key_free(capsys) -> None:
    rc = main(["blind", str(PAIR)])
    assert rc in (0, 3)
    out = capsys.readouterr().out
    assert "used_keys=False" in out
    assert "hash_iv=False" in out
    assert "g_values=False" in out
    assert "accuracy=" in out
