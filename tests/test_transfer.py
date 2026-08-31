"""Transfer scorers stay key-free and improve on unseen exact n-grams."""

from text_watermark_tools.blind import fit_blind, likelihood_ratio
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    fit_hashpool,
    hash_context,
    load_hashpool,
    persist_hashpool,
    score_hashpool,
    score_hashpool_vote,
    score_hybrid,
    score_hybrid_detail,
    score_sequence,
    score_sequence_detail,
    splitmix64,
)


def test_splitmix_and_context_hash_are_stable() -> None:
    assert splitmix64(1) == splitmix64(1)
    assert hash_context((10, 20, 30), 99) == hash_context((10, 20, 30), 99)
    assert hash_context((10, 20, 30), 99) != hash_context((10, 20, 31), 99)


def test_interpolate_uses_shorter_context_when_full_ngram_is_new() -> None:
    marked = [[9, 8, 1, 9, 8, 1, 9, 8, 1, 9, 8, 1]]
    unmarked = [[9, 8, 2, 9, 8, 2, 9, 8, 2, 9, 8, 2]]
    held_m = [3, 8, 1, 3, 8, 1, 3, 8, 1]
    held_u = [3, 8, 2, 3, 8, 2, 3, 8, 2]
    model = fit_blind(marked, unmarked, context_len=3, backoff=False)
    spec = COUNT_SPECS["interpolate"]
    gap_i = score_sequence(held_m, model, spec) - score_sequence(held_u, model, spec)
    gap_h = likelihood_ratio(held_m, model) - likelihood_ratio(held_u, model)
    assert model.used_keys is False
    assert gap_i > gap_h
    assert score_sequence(held_m, model, spec) > score_sequence(held_u, model, spec)


def test_gated_returns_zero_on_unseen_context() -> None:
    marked = [[0, 1, 0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2]]
    model = fit_blind(marked, unmarked, context_len=1)
    held = [9, 1, 9, 1, 9, 1]
    hard = likelihood_ratio(held, model)
    gated = score_sequence_detail(held, model, COUNT_SPECS["hits"])
    assert gated.n_used == 0
    assert gated.lr == 0.0
    assert abs(hard) > 0.0


def test_unigram_still_separates_synthetic_tokens() -> None:
    marked = [[0, 1, 0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2]]
    model = fit_blind(marked, unmarked, context_len=4)
    spec = COUNT_SPECS["unigram"]
    assert score_sequence([0, 1, 0, 1, 0, 1], model, spec) > score_sequence(
        [0, 2, 0, 2, 0, 2], model, spec
    )


def test_hashpool_persist_load_same_lr(tmp_path) -> None:
    marked = [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2, 0, 2]]
    model = fit_hashpool(
        marked, unmarked, context_len=1, n_hashes=4, n_buckets=8, seed=7
    )
    persist_hashpool(model, tmp_path, model_name="gpt2", n_train_prompts=1)
    loaded = load_hashpool(tmp_path)
    held_m = [0, 1, 0, 1, 0, 1]
    held_u = [0, 2, 0, 2, 0, 2]
    assert loaded.used_keys is False
    assert loaded.instance == "key-free-hashpool"
    assert score_hashpool(held_m, loaded) == score_hashpool(held_m, model)
    assert score_hashpool(held_u, loaded) == score_hashpool(held_u, model)


def test_hybrid_uses_exact_hits_then_falls_back_to_hashpool() -> None:
    marked = [[0, 1, 0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2]]
    counts = fit_blind(marked, unmarked, context_len=1, backoff=False)
    hashed = fit_hashpool(
        marked, unmarked, context_len=1, n_hashes=4, n_buckets=8, seed=7
    )
    unseen = [9, 1, 9, 1, 9, 1]
    gated = score_sequence_detail(unseen, counts, COUNT_SPECS["hits"])
    assert gated.n_used == 0
    hybrid = score_hybrid_detail(unseen, counts, hashed)
    assert hybrid.n_used == gated.n_positions
    assert counts.used_keys is False
    assert hashed.used_keys is False
    seen_m = [0, 1, 0, 1]
    seen_u = [0, 2, 0, 2]
    assert score_hybrid(seen_m, counts, hashed) > score_hybrid(seen_u, counts, hashed)


def test_hashvote_majority_is_key_free() -> None:
    marked = [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2, 0, 2]]
    model = fit_hashpool(
        marked, unmarked, context_len=1, n_hashes=4, n_buckets=8, seed=7
    )
    assert score_hashpool_vote([0, 1, 0, 1, 0, 1], model) > 0.0
    assert score_hashpool_vote([0, 2, 0, 2, 0, 2], model) < 0.0
    assert model.used_keys is False


def test_shrinkage_scores_rare_and_common_contexts_without_keys() -> None:
    marked = [[0, 1, 0, 1, 0, 1, 7, 3]]
    unmarked = [[0, 2, 0, 2, 0, 2, 7, 4]]
    model = fit_blind(marked, unmarked, context_len=1)
    detail = score_sequence_detail([0, 1, 7, 3], model, COUNT_SPECS["shrinkage"])
    assert model.used_keys is False
    assert detail.n_used == 2
    assert detail.n_positions == 3
