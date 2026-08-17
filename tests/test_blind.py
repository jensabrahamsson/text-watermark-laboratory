"""Key-free blind detector: counts only, no keys."""

from pathlib import Path

from text_watermark_tools.blind import (
    Twin,
    fit_blind,
    leave_one_prompt_out,
    likelihood_ratio,
    load_twins,
    pair_marked_wins,
)
from text_watermark_tools.cli import main

PAIR = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-17-pair"


def test_margin_turns_a_close_miss_into_a_hit() -> None:
    assert pair_marked_wins(0.01, 0.02, margin=0.0) is False
    assert pair_marked_wins(0.01, 0.02, margin=0.015) is True
    assert pair_marked_wins(-0.05, 0.02, margin=0.015) is False


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
