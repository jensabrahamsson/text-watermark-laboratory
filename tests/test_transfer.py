"""Transfer scorers stay key-free and improve on unseen exact n-grams."""

from text_watermark_tools.blind import fit_blind, likelihood_ratio
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    fit_hashmix_twins,
    fit_hashpool,
    hash_context,
    load_hashpool,
    persist_hashpool,
    score_hashmix,
    score_hashtok,
    score_hashtok_detail,
    score_hashpool,
    score_hashpool_detail,
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


def test_tokhybrid_skips_occupancy_then_uses_hashtok() -> None:
    from text_watermark_tools.transfer import score_tokhybrid, score_tokhybrid_detail

    marked = [[0, 1, 0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2]]
    counts = fit_blind(marked, unmarked, context_len=1, backoff=False)
    hashed = fit_hashpool(
        marked, unmarked, context_len=1, n_hashes=4, n_buckets=8, seed=7
    )
    novel = [0, 9]
    tokhits = score_sequence_detail(novel, counts, COUNT_SPECS["tokhits"])
    assert tokhits.n_used == 0
    hybrid = score_hybrid_detail(novel, counts, hashed)
    assert hybrid.n_used == 1
    tokhybrid = score_tokhybrid_detail(novel, counts, hashed)
    assert tokhybrid.n_used == 0
    assert counts.used_keys is False
    assert hashed.used_keys is False
    seen_m = [0, 1, 0, 1]
    seen_u = [0, 2, 0, 2]
    assert score_tokhybrid(seen_m, counts, hashed) > score_tokhybrid(
        seen_u, counts, hashed
    )


def test_hashvote_majority_is_key_free() -> None:
    marked = [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2, 0, 2]]
    model = fit_hashpool(
        marked, unmarked, context_len=1, n_hashes=4, n_buckets=8, seed=7
    )
    assert score_hashpool_vote([0, 1, 0, 1, 0, 1], model) > 0.0
    assert score_hashpool_vote([0, 2, 0, 2, 0, 2], model) < 0.0
    assert model.used_keys is False


def test_hashtokbackoff_shrinks_to_last1_not_occupancy() -> None:
    from text_watermark_tools.blind import Twin
    from text_watermark_tools.transfer import (
        fit_hashmix_twins,
        hashtok_token_lr,
        hashtokbackoff_trace,
        score_hashtok_detail,
        score_hashtokbackoff_detail,
        _scored_ctx,
    )

    twins = [
        Twin(
            stem="a",
            marked_text="m",
            unmarked_text="u",
            marked_ids=[0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            unmarked_ids=[0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
        )
    ]
    mix = fit_hashmix_twins(
        twins, orders=(1, 2, 3), n_hashes=4, n_buckets=256, seed=7
    )
    held_m = [100, 101, 0, 1]
    held_u = [100, 101, 0, 2]
    assert mix.used_keys is False
    ctx3 = _scored_ctx(held_m, 3, 3, 0)
    assert hashtok_token_lr(mix.models[3], ctx3, 1) is None
    long = score_hashtok_detail(held_m, mix.models[3])
    back = score_hashtokbackoff_detail(held_m, mix, min_order=1)
    back2 = score_hashtokbackoff_detail(held_m, mix, min_order=2)
    assert back.n_used > long.n_used
    assert back.lr > score_hashtokbackoff_detail(held_u, mix, min_order=1).lr
    last = hashtokbackoff_trace(held_m, mix, min_order=1)[-1]
    assert last["i"] == 3
    assert last["order"] == 1
    assert last["delta"] is not None
    last2 = hashtokbackoff_trace(held_m, mix, min_order=2)[-1]
    assert last2["order"] is None
    assert last2["delta"] is None
    assert back2.n_used == 0 or back2.n_used < back.n_used


def test_hashtoklen_refuses_short_prefix_in_longer_order() -> None:
    from text_watermark_tools.blind import Twin
    from text_watermark_tools.transfer import (
        fit_hashmix_twins,
        hash_ctx_len,
        hashtokbackoff_trace,
        score_hashtok_detail,
        score_hashtokbackoff_detail,
        _scored_ctx,
    )

    twins = [
        Twin(
            stem="a",
            marked_text="m",
            unmarked_text="u",
            marked_ids=[0, 1, 0, 1, 0, 1, 0, 1],
            unmarked_ids=[0, 2, 0, 2, 0, 2, 0, 2],
        )
    ]
    mixed = fit_hashmix_twins(
        twins, orders=(1, 2, 3), n_hashes=4, n_buckets=256, seed=7
    )
    exact = fit_hashmix_twins(
        twins,
        orders=(1, 2, 3),
        n_hashes=4,
        n_buckets=256,
        seed=7,
        exact_len=True,
    )
    held = [0, 1]
    assert mixed.used_keys is False
    assert exact.used_keys is False
    assert exact.exact_len is True
    ctx1 = _scored_ctx(held, 1, 3, 0)
    assert hash_ctx_len(ctx1, 0) == 1
    mixed_i1 = hashtokbackoff_trace(held, mixed, min_order=1)[0]
    exact_i1 = hashtokbackoff_trace(held, exact, min_order=1)[0]
    assert mixed_i1["i"] == exact_i1["i"] == 1
    assert mixed_i1["order"] == 3
    assert exact_i1["order"] != 3
    assert exact_i1["order"] in (1, None)
    order3 = next(row for row in exact_i1["tried"] if row["order"] == 3)
    assert order3["exact_ok"] is False
    assert order3["delta"] is None
    short_mixed = score_hashtok_detail(held, mixed.models[3])
    short_exact = score_hashtok_detail(held, exact.models[3])
    assert short_mixed.n_used == 1
    assert short_exact.n_used == 0
    long_exact = score_hashtokbackoff_detail([0, 1, 0, 1], exact, min_order=2)
    assert long_exact.n_used >= 1
    assert long_exact.lr > score_hashtokbackoff_detail(
        [0, 2, 0, 2], exact, min_order=2
    ).lr


def test_score_hashed_reader_detail_matches_hashtoklen_and_backoff() -> None:
    from text_watermark_tools.blind import Twin
    from text_watermark_tools.transfer import (
        fit_hashmix_twins,
        fit_hashpool,
        score_hashed_reader_detail,
        score_hashtok_detail,
        score_hashtokbackoff_detail,
    )

    marked = [[0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2]]
    pool = fit_hashpool(
        marked, unmarked, context_len=1, n_hashes=4, n_buckets=8, seed=7, exact_len=True
    )
    direct = score_hashtok_detail([0, 1, 0, 1], pool, exact_len=True)
    via = score_hashed_reader_detail(
        [0, 1, 0, 1], "hashtoklen", hash_len_model=pool
    )
    assert via.n_used == direct.n_used
    assert abs(via.lr - direct.lr) < 1e-12
    twins = [
        Twin(
            stem="a",
            marked_text="m",
            unmarked_text="u",
            marked_ids=[0, 1, 0, 1, 0, 1, 0, 1],
            unmarked_ids=[0, 2, 0, 2, 0, 2, 0, 2],
        )
    ]
    mix = fit_hashmix_twins(
        twins, orders=(1, 2), n_hashes=4, n_buckets=32, seed=7, exact_len=True
    )
    back = score_hashtokbackoff_detail([0, 1, 0, 1], mix, min_order=1, exact_len=True)
    via_b = score_hashed_reader_detail(
        [0, 1, 0, 1], "hashtoklenbackoff", mix_len_model=mix
    )
    assert via_b.n_used == back.n_used
    assert abs(via_b.lr - back.lr) < 1e-12


def test_hashskip_is_tagged_drop_one_not_last_k_minus_one() -> None:
    from text_watermark_tools.transfer import (
        SKIP_TAG,
        fit_hashpool,
        hash_context,
        score_hashtok_detail,
        score_hashskip,
        skip_views,
    )

    ctx = (10, 20, 30, 40)
    views = skip_views(ctx)
    assert len(views) == 4
    assert views[0][0] == SKIP_TAG
    assert views[0][1] == 0
    assert views[0][2:] == (20, 30, 40)
    # Tagged skip-grams must not hash as the remaining last-3.
    assert hash_context(views[0], 7) != hash_context((20, 30, 40), 7)
    marked = [[9, 1, 2, 3, 4], [8, 1, 2, 3, 4]]
    unmarked = [[9, 1, 2, 3, 5], [8, 1, 2, 3, 5]]
    skip = fit_hashpool(
        marked,
        unmarked,
        context_len=4,
        n_hashes=4,
        n_buckets=256,
        seed=7,
        drop_one=True,
    )
    exact = fit_hashpool(
        marked,
        unmarked,
        context_len=4,
        n_hashes=4,
        n_buckets=256,
        seed=7,
        exact_len=True,
    )
    held = [0, 1, 2, 3, 4]
    assert skip.used_keys is False
    assert skip.drop_one is True
    assert skip.exact_len is True
    skip_d = score_hashtok_detail(held, skip)
    exact_d = score_hashtok_detail(held, exact)
    assert exact_d.n_used == 0
    assert skip_d.n_used == 1
    assert skip_d.lr > 0
    assert score_hashskip(held, skip) > score_hashskip([0, 1, 2, 3, 5], skip)
    unseen = score_hashtok_detail([0, 1, 2, 3, 99], skip)
    assert unseen.n_used == 0
    assert unseen.lr == 0.0


def test_hashmask_is_length_k_replace_not_skip() -> None:
    from text_watermark_tools.transfer import (
        MASK_TAG,
        SKIP_TAG,
        fit_hashpool,
        hash_context,
        mask_views,
        score_hashmask,
        score_hashtok_detail,
        skip_views,
    )

    ctx = (10, 20, 30, 40)
    views = mask_views(ctx)
    assert len(views) == 4
    assert views[0][0] == MASK_TAG
    assert views[0][1:] == (20, 30, 40)
    assert len(views[0]) == 4
    assert views[0] != skip_views(ctx)[0]
    assert MASK_TAG != SKIP_TAG
    assert hash_context(views[0], 7) != hash_context((20, 30, 40), 7)
    marked = [[9, 1, 2, 3, 4], [8, 1, 2, 3, 4]]
    unmarked = [[9, 1, 2, 3, 5], [8, 1, 2, 3, 5]]
    mask = fit_hashpool(
        marked,
        unmarked,
        context_len=4,
        n_hashes=4,
        n_buckets=256,
        seed=7,
        mask_one=True,
    )
    skip = fit_hashpool(
        marked,
        unmarked,
        context_len=4,
        n_hashes=4,
        n_buckets=256,
        seed=7,
        drop_one=True,
    )
    exact = fit_hashpool(
        marked,
        unmarked,
        context_len=4,
        n_hashes=4,
        n_buckets=256,
        seed=7,
        exact_len=True,
    )
    held = [0, 1, 2, 3, 4]
    assert mask.used_keys is False
    assert mask.mask_one is True
    assert mask.drop_one is False
    assert mask.exact_len is True
    mask_d = score_hashtok_detail(held, mask)
    exact_d = score_hashtok_detail(held, exact)
    skip_d = score_hashtok_detail(held, skip)
    assert exact_d.n_used == 0
    assert mask_d.n_used == 1
    assert skip_d.n_used == 1
    assert mask_d.lr > 0
    assert score_hashmask(held, mask) > score_hashmask([0, 1, 2, 3, 5], mask)
    unseen = score_hashtok_detail([0, 1, 2, 3, 99], mask)
    assert unseen.n_used == 0
    assert unseen.lr == 0.0
    from text_watermark_tools.transfer import hashtok_trace

    trace = hashtok_trace(held, mask)
    slot = next(row for row in trace if row["i"] == 4)
    assert slot["mask_one"] is True
    assert slot["drop_one"] is False
    assert slot["skip_views"]
    assert all("mask_i" in view for view in slot["skip_views"])
    assert slot["delta"] == score_hashmask(held, mask)
    short = next(row for row in trace if row["i"] == 2)
    assert short["exact_ok"] is False
    assert short["skip_views"] == []
    assert short["delta"] is None


def test_hashtok_skips_unseen_next_token_occupancy() -> None:
    marked = [[0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2]]
    model = fit_hashpool(
        marked, unmarked, context_len=1, n_hashes=4, n_buckets=8, seed=7
    )
    assert model.used_keys is False
    seen_m = score_hashtok_detail([0, 1, 0, 1], model)
    pooled_m = score_hashpool_detail([0, 1, 0, 1], model)
    assert seen_m.n_used == seen_m.n_positions == pooled_m.n_used
    assert abs(seen_m.lr - pooled_m.lr) < 1e-12
    assert score_hashtok([0, 1, 0, 1], model) > score_hashtok([0, 2, 0, 2], model)
    occupancy = score_hashpool_detail([0, 99], model)
    unseen = score_hashtok_detail([0, 99], model)
    assert occupancy.n_used == 1
    assert occupancy.n_positions == 1
    assert abs(occupancy.lr) > 0.0
    assert unseen.n_used == 0
    assert unseen.n_positions == 1
    assert unseen.lr == 0.0
    assert score_hashtok([0, 99], model) == 0.0


def test_hashtok_min_count_skips_singleton_hash_collisions() -> None:
    from text_watermark_tools.transfer import score_hashskip

    marked = [[0, 1]]
    unmarked = [[0, 2], [0, 2], [0, 2], [0, 2]]
    model = fit_hashpool(
        marked, unmarked, context_len=1, n_hashes=4, n_buckets=8, seed=7
    )
    one = score_hashtok_detail([0, 1], model, min_count=1)
    two = score_hashtok_detail([0, 1], model, min_count=2)
    assert model.used_keys is False
    assert one.n_used == 1
    assert one.lr > 0
    assert two.n_used == 0
    assert two.lr == 0.0
    repeated = fit_hashpool(
        [[0, 1], [0, 1]],
        unmarked,
        context_len=1,
        n_hashes=4,
        n_buckets=8,
        seed=7,
    )
    kept = score_hashtok_detail([0, 1], repeated, min_count=2)
    assert kept.n_used == 1
    assert kept.lr > 0
    skip = fit_hashpool(
        [[9, 8, 1]],
        [[9, 8, 2], [9, 8, 2], [9, 8, 2], [9, 8, 2]],
        context_len=2,
        n_hashes=8,
        n_buckets=256,
        seed=7,
        drop_one=True,
    )
    skip_one = score_hashtok_detail([9, 8, 1], skip, min_count=1)
    skip_two = score_hashtok_detail([9, 8, 1], skip, min_count=2)
    assert skip.drop_one is True
    assert skip_one.n_used == 1
    assert skip_two.n_used == 0
    assert score_hashskip([9, 8, 1], skip, min_count=2) == 0.0


def test_shrinkage_scores_rare_and_common_contexts_without_keys() -> None:
    marked = [[0, 1, 0, 1, 0, 1, 7, 3]]
    unmarked = [[0, 2, 0, 2, 0, 2, 7, 4]]
    model = fit_blind(marked, unmarked, context_len=1)
    detail = score_sequence_detail([0, 1, 7, 3], model, COUNT_SPECS["shrinkage"])
    assert model.used_keys is False
    assert detail.n_used == 2
    assert detail.n_positions == 3


def test_hitmass_is_hits_times_coverage() -> None:
    marked = [[0, 1, 0, 1, 0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2, 0, 2, 0, 2]]
    model = fit_blind(marked, unmarked, context_len=1, backoff=False)
    unseen = score_sequence_detail([9, 1, 9, 1], model, COUNT_SPECS["hitmass"])
    assert unseen.lr == 0.0
    hits = score_sequence_detail([0, 1, 0, 1], model, COUNT_SPECS["hits"])
    mass = score_sequence_detail([0, 1, 0, 1], model, COUNT_SPECS["hitmass"])
    assert mass.n_used == hits.n_used
    assert abs(mass.lr - hits.lr * (hits.n_used / hits.n_positions)) < 1e-12
    assert model.used_keys is False


def test_freqhits_skips_rare_shared_contexts() -> None:
    marked = [[0, 1, 0, 1]]
    unmarked = [[0, 2, 0, 2]]
    model = fit_blind(marked, unmarked, context_len=1, backoff=False)
    detail = score_sequence_detail([0, 1, 0, 1], model, COUNT_SPECS["freqhits"])
    assert detail.n_used == 0
    assert detail.lr == 0.0


def test_hashmix_separates_synthetic_tokens() -> None:
    from text_watermark_tools.blind import Twin

    twins = [
        Twin(
            stem="a",
            marked_text="m",
            unmarked_text="u",
            marked_ids=[0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            unmarked_ids=[0, 2, 0, 2, 0, 2, 0, 2, 0, 2],
        )
    ]
    model = fit_hashmix_twins(twins, orders=(1, 2), n_hashes=4, n_buckets=8)
    assert model.used_keys is False
    assert score_hashmix([0, 1, 0, 1, 0, 1], model) > score_hashmix(
        [0, 2, 0, 2, 0, 2], model
    )


def test_surface_hashpool_is_tokenizer_free_and_key_free() -> None:
    from text_watermark_tools.blind import Twin
    from text_watermark_tools.transfer import (
        fit_surface_twins,
        load_hashpool,
        persist_hashpool,
        score_surface,
        text_to_bytes,
    )

    twins = [
        Twin(
            stem="a",
            marked_text="aaa aaa aaa aaa aaa",
            unmarked_text="zzz zzz zzz zzz zzz",
            marked_ids=[1],
            unmarked_ids=[2],
        )
    ]
    model = fit_surface_twins(twins, context_len=2, n_hashes=4, n_buckets=16)
    assert model.used_keys is False
    assert model.alphabet == "bytes"
    assert model.instance == "key-free-surface"
    assert score_surface("aaa aaa", model) > score_surface("zzz zzz", model)
    assert text_to_bytes("ab") == [97, 98]


def test_surface_persist_load_same_lr(tmp_path) -> None:
    from text_watermark_tools.blind import Twin
    from text_watermark_tools.transfer import (
        SURFACE_KIND,
        fit_surface_twins,
        load_hashpool,
        persist_hashpool,
        score_surface,
    )

    twins = [
        Twin(
            stem="a",
            marked_text="hello hello hello hello",
            unmarked_text="world world world world",
            marked_ids=[1],
            unmarked_ids=[2],
        )
    ]
    model = fit_surface_twins(twins, context_len=3, n_hashes=4, n_buckets=16, seed=3)
    persist_hashpool(model, tmp_path, model_name="none", n_train_prompts=1)
    loaded = load_hashpool(tmp_path)
    assert loaded.alphabet == "bytes"
    assert loaded.instance == "key-free-surface"
    text = "hello hello"
    assert score_surface(text, loaded) == score_surface(text, model)
    raw = (tmp_path / "tables.json").read_text()
    assert SURFACE_KIND in raw
    assert '"used_keys": false' in raw
