"""Key-free blind detector: counts only, no keys."""

import json
from pathlib import Path

from text_watermark_tools.blind import (
    BlindEval,
    BlindFold,
    Twin,
    FIRST_TOKEN_CTX,
    _scored_ctx,
    clip_twins,
    fit_blind,
    leave_one_prompt_out,
    likelihood_ratio,
    load_twins,
    pair_marked_wins,
    pair_outcome,
    persist_blind_eval,
    print_blind_eval,
)
from text_watermark_tools.cli import main
from text_watermark_tools.indicator import holdout_from_json

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


def test_pair_outcome_treats_equality_as_a_tie() -> None:
    assert pair_outcome(0.0, 0.0) == "tie"
    assert pair_marked_wins(0.0, 0.0) is False
    assert pair_outcome(0.1, 0.0) == "win"
    assert pair_outcome(0.0, 0.1) == "loss"
    assert pair_outcome(0.01, 0.03, margin=0.02) == "tie"


def test_score_span_keeps_absolute_history() -> None:
    # Marked history (10,11,12)→99; unmarked likes a sliced (99,)→88.
    marked = [[10, 11, 12, 99, 88]]
    unmarked = [[99, 88, 88, 88, 88]]
    model = fit_blind(marked * 8, unmarked * 8, context_len=3)
    ids = marked[0]
    assert _scored_ctx(ids, 3, 3, 0) == (10, 11, 12)
    assert _scored_ctx(ids[3:5], 1, 3, 0) == (99,)
    with_history = likelihood_ratio(ids, model, score_span=(3, 5))
    reindexed = likelihood_ratio(ids[3:5], model)
    assert with_history != reindexed
    # A one-token window is scored at its absolute index; a sliced
    # singleton is skipped as generated token 0.
    assert likelihood_ratio(ids, model, score_span=(3, 4)) != 0.0
    assert likelihood_ratio(ids[3:4], model) == 0.0


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


def test_fit_table_does_not_recount_truncated_openings() -> None:
    from text_watermark_tools.blind import fit_table

    table = fit_table([[10, 20]], context_len=4)
    assert table.counts[(10,)][20] == 1
    assert table.unigram[10] == 1
    assert table.unigram[20] == 1
    long = fit_table([[1, 2, 3, 4, 5]], context_len=4)
    assert long.counts[(1,)][2] == 1
    assert long.counts[(4,)][5] == 1
    assert long.counts[(3, 4)][5] == 1
    assert long.counts[(2, 3, 4)][5] == 1
    assert long.counts[(1, 2, 3, 4)][5] == 1
    prefixed = fit_table([[20]], context_len=4, prefixes=[[10]])
    assert prefixed.counts[(10,)][20] == 1
    first = fit_table([[9, 8]], context_len=4, include_first=True)
    assert first.counts[FIRST_TOKEN_CTX][9] == 1
    assert first.counts[(9,)][8] == 1


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
    for fold in ev.folds:
        assert len(fold.marked_file_lrs) == 1
        assert len(fold.unmarked_file_lrs) == 1
        assert fold.marked_lr == fold.marked_file_lrs[0]
        assert fold.unmarked_lr == fold.unmarked_file_lrs[0]
    assert ev.ranking_without_isolated_tp == []
    assert ev.ranking_losses_with_isolated_tp == []


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


def test_load_twins_rejects_asymmetric_extra_draws(tmp_path: Path) -> None:
    (tmp_path / "harbour-marked.txt").write_text("alpha marked")
    (tmp_path / "harbour-unmarked-gen.txt").write_text("alpha unmarked")
    (tmp_path / "harbour-marked-2.txt").write_text("beta marked")
    (tmp_path / "harbour-unmarked-gen-3.txt").write_text("gamma unmarked")
    try:
        load_twins(tmp_path)
    except ValueError as exc:
        msg = str(exc)
        assert "asymmetric" in msg
        assert "harbour" in msg
    else:
        raise AssertionError("missing unmarked-gen-2 must not silently pair draw 2 with 3")


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
    assert "ranking_without_isolated_tp=" in out
    assert "ranking_losses_with_isolated_tp=" in out
    assert "marked_lr_positive=" in out


def test_leave_one_out_stores_per_file_lrs_on_extra_draws() -> None:
    twins = [
        Twin(
            "a",
            "a",
            "a",
            [0, 1, 0, 1, 0, 1, 0, 1],
            [0, 2, 0, 2, 0, 2, 0, 2],
            extra_marked_ids=[[0, 1, 0, 1, 0, 1]],
            extra_unmarked_ids=[[0, 2, 0, 2, 0, 2]],
        ),
        Twin("b", "b", "b", [0, 1, 0, 1, 0, 1, 0, 1], [0, 2, 0, 2, 0, 2, 0, 2]),
        Twin("c", "c", "c", [0, 1, 0, 1, 0, 1, 0, 1], [0, 2, 0, 2, 0, 2, 0, 2]),
    ]
    ev = leave_one_prompt_out(twins, context_len=1)
    held = next(f for f in ev.folds if f.stem == "a")
    assert len(held.marked_file_lrs) == 2
    assert len(held.unmarked_file_lrs) == 2
    assert held.marked_lr == sum(held.marked_file_lrs) / 2
    assert held.unmarked_lr == sum(held.unmarked_file_lrs) / 2
    assert ev.n_marked_wins == 3


def test_blind_eval_ranking_without_isolated_tp_is_prompt_win_with_no_sign() -> None:
    ev = BlindEval(
        folds=[
            BlindFold(
                stem="bus",
                marked_lr=-0.15,
                unmarked_lr=-0.45,
                marked_wins=True,
                marked_file_lrs=[-0.1, -0.2],
                unmarked_file_lrs=[-0.4, -0.5],
            ),
            BlindFold(
                stem="ferry",
                marked_lr=0.45,
                unmarked_lr=-0.15,
                marked_wins=True,
                marked_file_lrs=[0.4, 0.5],
                unmarked_file_lrs=[-0.2, -0.1],
            ),
            BlindFold(
                stem="station",
                marked_lr=-0.05,
                unmarked_lr=0.10,
                marked_wins=False,
                marked_file_lrs=[0.1, -0.2],
                unmarked_file_lrs=[0.2, 0.0],
            ),
        ],
        context_len=4,
        alpha=0.5,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )
    assert ev.n_marked_wins == 2
    assert ev.n_marked_positive == 3
    assert ev.ranking_without_isolated_tp == ["bus"]
    assert ev.n_prompt_wins_without_isolated_tp == 1
    assert ev.ranking_losses_with_isolated_tp == ["station"]
    assert ev.n_marked_positive_on_ranking_losses == 1
    text = print_blind_eval(ev)
    assert "ranking_without_isolated_tp=1/2" in text
    assert "ranking_losses_with_isolated_tp=1" in text
    assert "ranking wins with no isolated TP: bus" in text
    assert "ranking losses with isolated TP: station" in text
    assert "marked_files_gt0=0/2" in text


def test_blind_eval_isolated_sign_stays_hard_when_margin_is_nonzero() -> None:
    ev = BlindEval(
        folds=[
            BlindFold(
                stem="garden",
                marked_lr=-0.02,
                unmarked_lr=-0.05,
                marked_wins=True,
                marked_file_lrs=[-0.01, -0.03],
                unmarked_file_lrs=[-0.04, -0.06],
            )
        ],
        context_len=4,
        alpha=0.5,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        margin=0.02,
    )
    assert ev.n_marked_wins == 1
    assert ev.n_marked_positive == 0
    assert ev.ranking_without_isolated_tp == ["garden"]


def test_blind_eval_ranking_matches_hard_last4_holdout() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    hold = holdout_from_json(
        root / "2026-09-01-probe-12x4-recount-hard-last4" / "hard" / "holdout.json"
    )
    folds: list[BlindFold] = []
    for stem, pairs in sorted(hold._stem_pairs().items()):
        marked = [m for m, _ in pairs]
        unmarked = [u for _, u in pairs]
        marked_mean = sum(marked) / len(marked)
        unmarked_mean = sum(unmarked) / len(unmarked)
        folds.append(
            BlindFold(
                stem=stem,
                marked_lr=marked_mean,
                unmarked_lr=unmarked_mean,
                marked_wins=pair_marked_wins(marked_mean, unmarked_mean),
                marked_file_lrs=marked,
                unmarked_file_lrs=unmarked,
            )
        )
    ev = BlindEval(
        folds=folds,
        context_len=4,
        alpha=0.5,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )
    assert ev.used_keys is False
    assert ev.n_marked_wins == 9
    assert ev.n_marked_positive == 25
    assert ev.ranking_without_isolated_tp == ["11-garden"]
    assert ev.ranking_losses_with_isolated_tp == [
        "06-station",
        "10-office",
        "12-ferry-queue",
    ]
    assert ev.n_marked_positive_on_ranking_losses == 5
    payload = ev.ranking_payload()
    assert payload["ranking_without_isolated_tp"] == ["11-garden"]
    assert payload["n_marked_lr_positive"] == 25


def test_persist_blind_eval_writes_ranking_honesty(tmp_path: Path) -> None:
    ev = BlindEval(
        folds=[
            BlindFold(
                stem="garden",
                marked_lr=-0.02,
                unmarked_lr=-0.05,
                marked_wins=True,
                marked_file_lrs=[-0.01, -0.03],
                unmarked_file_lrs=[-0.04, -0.06],
            ),
            BlindFold(
                stem="ferry",
                marked_lr=-0.01,
                unmarked_lr=0.02,
                marked_wins=False,
                marked_file_lrs=[0.1, -0.12],
                unmarked_file_lrs=[0.01, 0.03],
            ),
        ],
        context_len=4,
        alpha=0.5,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )
    persist_blind_eval(ev, tmp_path)
    raw = json.loads((tmp_path / "results.json").read_text())
    assert raw["n_marked_wins"] == 1
    assert raw["ranking_without_isolated_tp"] == ["garden"]
    assert raw["ranking_losses_with_isolated_tp"] == ["ferry"]
    assert raw["n_marked_lr_positive"] == 1
    assert raw["folds"][0]["marked_file_lrs"] == [-0.01, -0.03]
    md = (tmp_path / "results.md").read_text()
    assert "Ranking wins with no isolated TP: **1/1** (garden)" in md
    assert "Ranking losses with isolated TP: **1** (ferry)" in md
    historical = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-blind-12x4-recount-last4"
            / "results.json"
        ).read_text()
    )
    assert historical["n_marked_wins"] == 9
    assert "ranking_without_isolated_tp" not in historical
    assert "marked_file_lrs" not in historical["folds"][0]


def test_blind_12x4_ranking_honesty_json_matches_headline() -> None:
    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-blind-12x4-ranking-honesty"
            / "results.json"
        ).read_text()
    )
    assert raw["used_keys"] is False
    assert raw["n_marked_wins"] == 9
    assert raw["n_marked_lr_positive"] == 25
    assert raw["ranking_without_isolated_tp"] == ["11-garden"]
    assert raw["ranking_losses_with_isolated_tp"] == [
        "06-station",
        "10-office",
        "12-ferry-queue",
    ]
    assert raw["n_marked_positive_on_ranking_losses"] == 5
    garden = next(f for f in raw["folds"] if f["stem"] == "11-garden")
    assert garden["marked_wins"] is True
    assert garden["n_marked_positive"] == 0
    assert all(m <= 0.0 for m in garden["marked_file_lrs"])
    ferry = next(f for f in raw["folds"] if f["stem"] == "12-ferry-queue")
    assert ferry["marked_wins"] is False
    assert ferry["n_marked_positive"] == 3

