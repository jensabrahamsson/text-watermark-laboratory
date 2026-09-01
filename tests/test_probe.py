"""Probe CLI and published 12×4 holdout statistics."""

from pathlib import Path

from text_watermark_tools.blind import load_twins
from text_watermark_tools.cli import main
from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.probe import (
    apply_overlap,
    persist_probe,
    rotate_count_methods,
    rotate_score_stack,
    run_probe,
    run_transfer,
    shuffle_twin_sides,
)
from text_watermark_tools.stats import binary_eval, binomial_sf

PAIR = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-17-pair"
HOLD = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "2026-08-17-indicate-holdout-12x4"
    / "holdout.json"
)


def test_published_12x4_holdout_is_ten_of_twelve_and_has_auc() -> None:
    ev = holdout_from_json(HOLD)
    assert ev.used_keys is False
    assert ev.used_hash_iv is False
    assert ev.used_g_values is False
    assert ev.n_prompts == 12
    assert ev.n_files == 96
    assert ev.n_prompts_marked_above == 10
    assert ev.n_marked_positive == 29
    assert ev.n_unmarked_nonpositive == 23
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=500, seed=0)
    assert stats.auc > 0.55
    assert binomial_sf(10, 12, 0.5) < 0.05
    # Isolated sign at 0 is not a 5% test; ranking still has a mean gap.
    assert stats.binomial_p_above_zero > 0.05
    assert stats.mean_diff > 0.0


def test_clip_seq_keeps_a_token_prefix() -> None:
    from text_watermark_tools.probe import clip_seq, slice_seq

    assert clip_seq([1, 2, 3, 4], 2) == [1, 2]
    assert clip_seq("abcd", 3) == "abc"
    assert clip_seq([1, 2], 8) == [1, 2]
    assert clip_seq([1, 2, 3], 0) == [1, 2, 3]
    assert slice_seq([1, 2, 3, 4], 1, 3) == [2, 3]
    assert slice_seq("abcd", 0, 2) == "ab"
    assert slice_seq([1, 2, 3], 2, 2) == []


def test_clip_prefix_and_poshits_on_lab_pairs_are_key_free(tmp_path) -> None:
    from text_watermark_tools.blind import clip_twins_prefix
    from text_watermark_tools.probe import persist_probe

    twins = load_twins(PAIR)
    clipped = clip_twins_prefix(twins, 4)
    assert clipped[0].marked_ids == twins[0].marked_ids[:4]
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        context_len=2,
        methods=("hits", "poshits", "poshitmass", "pospool"),
        fit_prefix=6,
        position_bucket=2,
        n_hashes=4,
        n_buckets=16,
    )
    assert run.used_keys is False
    assert run.fit_prefix == 6
    names = {m.name for m in run.methods}
    assert names == {"hits", "poshits", "poshitmass", "pospool"}
    assert all(m.holdout.used_keys is False for m in run.methods)
    poshits = next(m for m in run.methods if m.name == "poshits")
    assert poshits.holdout.instance == "key-free-poshits"
    poshitmass = next(m for m in run.methods if m.name == "poshitmass")
    assert poshitmass.holdout.instance == "key-free-poshitmass"
    persist_probe(run, tmp_path)
    assert (tmp_path / "poshits" / "holdout.json").is_file()
    assert (tmp_path / "poshitmass" / "holdout.json").is_file()
    assert (tmp_path / "pospool" / "holdout.json").is_file()
    from text_watermark_tools.probe import persist_transfer, run_transfer

    xfer = run_transfer(
        twins,
        twins[-1:],
        train_dir=str(PAIR),
        test_dir=str(PAIR),
        context_len=2,
        methods=("poshits", "poshitmass"),
        overlap_mode="keep",
        nested=True,
        position_bucket=2,
        n_hashes=4,
        n_buckets=16,
    )
    assert xfer.used_keys is False
    nested_names = {r.name for r in xfer.thresholds if r.source == "nested-youden"}
    assert nested_names == {"poshits", "poshitmass"}
    persist_transfer(xfer, tmp_path / "xfer")
    tables = tmp_path / "xfer" / "tables-poshits" / "tables.json"
    assert tables.is_file()
    from text_watermark_tools.indicator import load_indicator, score_text_from_tables
    from text_watermark_tools.score import load_tokenizer

    model, meta = load_indicator(tmp_path / "xfer" / "tables-poshits")
    assert model.used_keys is False
    assert model.position_bucket == 2
    assert meta.instance == "key-free-poshits"
    tok = load_tokenizer("gpt2")
    lr, scored, used_keys = score_text_from_tables(
        twins[0].marked_text,
        tmp_path / "xfer" / "tables-poshits",
        tokenizer=tok,
        score_mode="auto",
    )
    assert used_keys is False
    assert scored.score_kind == "poshits"
    assert isinstance(lr, float)
    mass_lr, mass_meta, mass_keys = score_text_from_tables(
        twins[0].marked_text,
        tmp_path / "xfer" / "tables-poshits",
        tokenizer=tok,
        score_mode="poshitmass",
    )
    assert mass_keys is False
    assert mass_meta.score_kind == "poshitmass"
    assert isinstance(mass_lr, float)


def test_include_first_and_prompt_context_on_lab_pairs_are_key_free() -> None:
    twins = load_twins(PAIR)
    assert twins[0].prompt_ids
    base = run_probe(
        twins,
        pair_dir=str(PAIR),
        context_len=2,
        methods=("hits", "first"),
        fit_prefix=4,
        position_bucket=1,
        n_hashes=4,
        n_buckets=16,
    )
    with_first = run_probe(
        twins,
        pair_dir=str(PAIR),
        context_len=2,
        methods=("hits", "first"),
        fit_prefix=4,
        position_bucket=1,
        include_first=True,
        n_hashes=4,
        n_buckets=16,
    )
    with_prompt = run_probe(
        twins,
        pair_dir=str(PAIR),
        context_len=2,
        methods=("hits",),
        fit_prefix=4,
        position_bucket=1,
        prompt_context=True,
        n_hashes=4,
        n_buckets=16,
    )
    assert base.used_keys is False
    assert with_first.include_first is True
    assert with_prompt.prompt_context is True
    assert all(m.holdout.used_keys is False for m in with_first.methods)
    assert all(m.holdout.used_keys is False for m in with_prompt.methods)
    first = next(m for m in with_first.methods if m.name == "first")
    assert first.holdout.instance == "key-free-first"
    base_hits = next(m for m in base.methods if m.name == "hits")
    first_hits = next(m for m in with_first.methods if m.name == "hits")
    assert base_hits.holdout.marked_lrs != first_hits.holdout.marked_lrs


def test_prefix_probe_on_lab_pairs_is_key_free(tmp_path) -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        context_len=2,
        methods=("hard", "hits", "hashpool"),
        prefix_lens=(2, 4),
        windows=((0, 2), (2, 4)),
        n_hashes=4,
        n_buckets=16,
    )
    assert run.used_keys is False
    assert run.prefix_lens == (2, 4)
    assert run.windows == ((0, 2), (2, 4))
    assert set(run.prefixes) == {2, 4}
    assert set(run.window_results) == {(0, 2), (2, 4)}
    names = {m.name for m in run.prefixes[2]}
    assert "hard" in names
    assert "hits" in names
    assert "hashpool" in names
    win_names = {m.name for m in run.window_results[(0, 2)]}
    assert "hits" in win_names
    persist_probe(run, tmp_path)
    assert (tmp_path / "prefix-2" / "hits" / "holdout.json").is_file()
    assert (tmp_path / "window-0-2" / "hits" / "holdout.json").is_file()
    twins = load_twins(PAIR)
    out = rotate_count_methods(
        twins, methods=("unigram", "hard", "interpolate"), context_len=2
    )
    assert set(out) == {"unigram", "hard", "interpolate"}
    for ev in out.values():
        assert ev.used_keys is False
        assert ev.n_prompts == 3
        assert ev.n_files == 6


def test_cli_probe_small_pair_dir_is_key_free(tmp_path, capsys) -> None:
    out = tmp_path / "probe"
    rc = main(
        [
            "probe",
            str(PAIR),
            "--context-len",
            "2",
            "--methods",
            "unigram,hard",
            "--skip-hashpool",
            "--out-dir",
            str(out),
        ]
    )
    assert rc == 0
    printed = capsys.readouterr().out
    assert "used_keys=False" in printed
    assert "auc=" in printed
    assert "unigram" in printed
    assert "hard" in printed
    assert (out / "results.json").is_file()
    assert (out / "hard" / "holdout.json").is_file()


def test_hashpool_12x4_isolated_sign_is_thirty_five_of_forty_eight() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-12x4"
        / "hashpool"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 11
    assert ev.n_marked_positive == 35
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=400, seed=0)
    assert stats.auc > 0.70
    assert binomial_sf(35, 48, 0.5) < 0.01


def test_hits_12x4_auc_beats_hard_counts() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-31-probe-12x4"
    hits = holdout_from_json(root / "hits" / "holdout.json")
    hard = holdout_from_json(root / "hard" / "holdout.json")
    assert hits.n_prompts_marked_above == 11
    assert hard.n_prompts_marked_above == 10
    assert hits.used_keys is False
    h = binary_eval(hits.marked_lrs, hits.unmarked_lrs, n_perm=200, seed=0)
    d = binary_eval(hard.marked_lrs, hard.unmarked_lrs, n_perm=200, seed=0)
    assert h.auc > d.auc
    assert h.auc > 0.72


def test_scrub_12x4_official_mean_falls_to_chance() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-scrub-12x4"
            / "results.json"
        ).read_text()
    )
    assert raw["used_keys_for_snap"] is False
    rows = raw["rows"]
    assert len(rows) == 48
    before = sum(r["mean_before"] for r in rows) / len(rows)
    after = sum(r["mean_after"] for r in rows) / len(rows)
    assert before > 0.60
    assert abs(after - 0.5) < 0.02
    assert all(r["used_keys_for_snap"] is False for r in rows)


def test_hashpool_36_topics_is_thirty_one_of_thirty_six() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36"
        / "hashpool"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts == 36
    assert ev.n_prompts_marked_above == 31
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc > 0.85


def test_hashpool_qwen_is_ten_of_twelve() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-qwen"
        / "hashpool"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 10
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc > 0.70


def test_run_probe_hashpool_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        context_len=2,
        methods=("hard", "hashpool"),
        with_hashpool=True,
        with_pivot=False,
        n_hashes=4,
        n_buckets=32,
    )
    names = [m.name for m in run.methods]
    assert "hard" in names
    assert "hashpool" in names
    assert run.used_keys is False
    hp = next(m for m in run.methods if m.name == "hashpool")
    assert hp.holdout.instance == "key-free-hashpool"
    assert hp.binary.n_positive == 3


def test_apply_overlap_drops_shared_stems_from_train_or_test() -> None:
    twins = load_twins(PAIR)
    train, test, dropped = apply_overlap(twins, twins[:1], mode="drop-from-train")
    assert dropped == [twins[0].stem]
    assert all(t.stem != twins[0].stem for t in train)
    assert test[0].stem == twins[0].stem
    train2, test2, dropped2 = apply_overlap(
        twins[:1], twins, mode="drop-from-test"
    )
    assert dropped2 == [twins[0].stem]
    assert len(train2) == 1
    assert all(t.stem != twins[0].stem for t in test2)


def test_run_transfer_on_lab_pairs_is_key_free() -> None:
    twins = load_twins(PAIR)
    run = run_transfer(
        twins[:2],
        twins[2:],
        train_dir=str(PAIR),
        test_dir=str(PAIR),
        context_len=2,
        methods=("hard", "hits", "hashpool", "hybrid", "stack"),
        overlap_mode="keep",
        n_hashes=4,
        n_buckets=16,
        nested=False,
    )
    names = [m.name for m in run.methods]
    assert names == ["hard", "hits", "hashpool", "hybrid", "stack"]
    assert run.used_keys is False
    assert run.n_train_prompts == 2
    assert run.n_test_prompts == 1
    assert run.thresholds
    hp = next(m for m in run.methods if m.name == "hashpool")
    assert hp.holdout.mode == "transfer"
    assert hp.holdout.instance == "key-free-hashpool"
    assert run.nested is False
    assert all(row.source == "in-sample-youden" for row in run.thresholds)


def test_shuffle_twin_sides_is_a_per_stem_coin_flip() -> None:
    twins = load_twins(PAIR)
    shuffled = shuffle_twin_sides(twins, seed=0)
    assert len(shuffled) == len(twins)
    swapped = sum(
        a.marked_ids == b.unmarked_ids for a, b in zip(twins, shuffled, strict=True)
    )
    assert swapped == len(twins) // 2
    assert all(t.stem == s.stem for t, s in zip(twins, shuffled, strict=True))


def test_stack_12x4_hits_and_hashpool_stays_key_free() -> None:
    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-12x4"
    )
    hits = holdout_from_json(root / "hits" / "holdout.json")
    hashed = holdout_from_json(root / "hashpool" / "holdout.json")
    stacked = rotate_score_stack([hits, hashed], model_name="gpt2")
    assert stacked.used_keys is False
    assert stacked.used_hash_iv is False
    assert stacked.used_g_values is False
    assert stacked.n_prompts == 12
    assert stacked.n_files == 96
    stats = binary_eval(stacked.marked_lrs, stacked.unmarked_lrs, n_perm=400, seed=0)
    assert stats.auc > 0.65
    assert stacked.n_prompts_marked_above >= 10


def test_transfer_36_to_12x4_hits_isolated_is_thirty_nine_of_forty_eight() -> None:
    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36-to-12x4"
    )
    hits = holdout_from_json(root / "hits" / "holdout.json")
    hashed = holdout_from_json(root / "hashpool" / "holdout.json")
    assert hits.used_keys is False
    assert hashed.used_keys is False
    assert hits.mode == "transfer"
    assert hits.n_prompts == 12
    assert hits.n_marked_positive == 39
    assert hashed.n_prompts_marked_above == 11
    stats = binary_eval(hits.marked_lrs, hits.unmarked_lrs, n_perm=400, seed=0)
    assert stats.auc > 0.75
    assert binomial_sf(39, 48, 0.5) < 1e-5


def test_transfer_12x4_to_36_hits_ranks_all_new_topics() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-12x4-to-36"
        / "hits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts == 24
    assert ev.n_prompts_marked_above == 24
    assert ev.n_marked_positive == 24
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=400, seed=0)
    assert stats.auc > 0.95


def test_ood_hashpool_tables_score_one_file_without_keys() -> None:
    from text_watermark_tools.indicator import score_text_from_tables
    from text_watermark_tools.score import load_tokenizer

    tables = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36-to-12x4"
        / "tables-hashpool"
    )
    text = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-17-pair-12x4"
        / "01-harbour-marked.txt"
    ).read_text()
    tok = load_tokenizer("gpt2")
    lr, meta, used = score_text_from_tables(text, tables, tokenizer=tok)
    assert used is False
    assert meta.instance == "key-free-hashpool"
    assert meta.score_kind == "hashpool"
    assert isinstance(lr, float)


def test_nested_36_to_12x4_hashpool_youden_is_balanced() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-transfer-nested-36-to-12x4"
            / "results.json"
        ).read_text()
    )
    assert raw["used_keys"] is False
    row = next(
        r
        for r in raw["thresholds"]
        if r["name"] == "hashpool" and r["source"] == "nested-youden"
    )
    assert row["n_marked_above"] == 33
    assert row["n_unmarked_at_most"] == 34
    hitmass = next(m for m in raw["methods"] if m["name"] == "hitmass")
    assert hitmass["n_prompt_wins"] == 10


def test_nested_12x4_to_36_freqhits_is_twenty_three_of_twenty_four() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-transfer-nested-12x4-to-36"
            / "results.json"
        ).read_text()
    )
    assert raw["used_keys"] is False
    row = next(
        r
        for r in raw["thresholds"]
        if r["name"] == "freqhits" and r["source"] == "nested-youden"
    )
    assert row["n_marked_above"] == 23
    assert row["n_unmarked_at_most"] == 23


def test_shuffle_36_to_12x4_isolated_falls_toward_chance() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-shuffle-36-to-12x4"
    )
    raw = json.loads((root / "results.json").read_text())
    assert raw["used_keys"] is False
    assert raw["shuffle_seed"] == 0
    assert not (root / "tables-hashpool").exists()
    hits = next(m for m in raw["methods"] if m["name"] == "hits")
    hashed = next(m for m in raw["methods"] if m["name"] == "hashpool")
    assert hits["binary"]["n_positive_above_zero"] == 19
    assert hashed["binary"]["n_positive_above_zero"] == 20
    assert hits["binary"]["auc"] < 0.65
    assert hashed["n_prompt_wins"] == 9


def test_run_transfer_surface_and_logit_on_lab_pairs_is_key_free() -> None:
    twins = load_twins(PAIR)
    run = run_transfer(
        twins[:2],
        twins[2:],
        train_dir=str(PAIR),
        test_dir=str(PAIR),
        context_len=2,
        methods=("hits", "hashpool", "surface", "logit"),
        overlap_mode="keep",
        n_hashes=4,
        n_buckets=16,
        nested=False,
        surface_context_len=4,
    )
    names = [m.name for m in run.methods]
    assert names == ["hits", "hashpool", "surface", "logit"]
    assert run.used_keys is False
    surf = next(m for m in run.methods if m.name == "surface")
    assert surf.holdout.instance == "key-free-surface"
    logit = next(m for m in run.methods if m.name == "logit")
    assert logit.holdout.instance == "key-free-logit"


def test_shuffle_transfer_does_not_persist_tables(tmp_path) -> None:
    twins = load_twins(PAIR)
    run = run_transfer(
        twins[:2],
        twins[2:],
        train_dir=str(PAIR),
        test_dir=str(PAIR),
        context_len=2,
        methods=("hits", "hashpool"),
        overlap_mode="keep",
        n_hashes=4,
        n_buckets=16,
        nested=False,
        shuffle_labels=True,
        shuffle_seed=0,
    )
    from text_watermark_tools.probe import persist_transfer

    persist_transfer(run, tmp_path)
    assert run.shuffle_seed == 0
    assert not (tmp_path / "tables-hashpool").exists()
    assert not (tmp_path / "tables-counts").exists()
    assert not (tmp_path / "tables-poshits").exists()
    assert (tmp_path / "results.json").is_file()


def test_surface_12x4_loo_is_ten_of_twelve() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-surface-12x4"
        / "surface"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.instance == "key-free-surface"
    assert ev.n_prompts_marked_above == 10
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc > 0.55
    assert stats.permutation_p < 0.05


def test_gpt2_to_qwen_same_topic_hits_ranks_eleven_of_twelve() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-gpt2-to-qwen"
        / "hits"
        / "holdout.json"
    )
    hashed = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-gpt2-to-qwen"
        / "hashpool"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 11
    assert ev.n_marked_positive == 1
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc > 0.70
    # Token hashpool does not follow the probe-BPE hits ranking across generators.
    assert hashed.n_prompts_marked_above == 7
    hash_stats = binary_eval(hashed.marked_lrs, hashed.unmarked_lrs, n_perm=200, seed=0)
    assert hash_stats.auc < 0.60


def test_new_topics_gpt2_to_qwen_is_chance() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36-to-qwen"
        / "hits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 6
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc < 0.60


def test_qwen_in_domain_surface_is_nine_of_twelve() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-surface-qwen"
        / "surface"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 9
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc > 0.60


def test_pair_36x4_official_splits_all_first_draws() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-pair-36x4"
            / "results.json"
        ).read_text()
    )
    assert raw["instance"] == "public-deepmind-30"
    assert raw["max_new_tokens"] == 128
    assert raw["model_name"] == "gpt2"
    assert len(raw["rows"]) == 36
    wins = sum(
        1
        for row in raw["rows"]
        if row["marked"]["mean"] > row["unmarked_gen"]["mean"]
    )
    assert wins == 36


def test_probe_36x4_hits_ranks_all_prompts_and_nested_gate_is_balanced() -> None:
    from text_watermark_tools.stats import nested_threshold_by_stem

    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36x4"
        / "hits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts == 36
    assert ev.n_files == 288
    assert ev.n_prompts_marked_above == 36
    assert ev.n_marked_positive == 134
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=400, seed=0)
    assert stats.auc > 0.92
    nested = nested_threshold_by_stem(ev.stems, ev.marked_lrs, ev.unmarked_lrs)
    assert nested.n_marked_above == 119
    assert nested.n_unmarked_at_most == 134
    assert nested.sensitivity > 0.80
    assert nested.specificity > 0.90


def test_transfer_36x4_to_12x4_hits_is_twelve_of_twelve() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4"
    )
    hits = holdout_from_json(root / "hits" / "holdout.json")
    logit = holdout_from_json(root / "logit" / "holdout.json")
    assert hits.used_keys is False
    assert hits.mode == "transfer"
    assert hits.n_prompts_marked_above == 12
    assert hits.n_marked_positive == 42
    stats = binary_eval(hits.marked_lrs, hits.unmarked_lrs, n_perm=400, seed=0)
    assert stats.auc > 0.78
    assert logit.n_prompts_marked_above == 12
    logit_stats = binary_eval(
        logit.marked_lrs, logit.unmarked_lrs, n_perm=200, seed=0
    )
    assert logit_stats.auc > 0.80
    raw = json.loads((root / "results.json").read_text())
    assert raw["used_keys"] is False
    nested = next(
        r
        for r in raw["thresholds"]
        if r["name"] == "hits" and r["source"] == "nested-youden"
    )
    assert nested["n_marked_above"] == 26
    assert nested["n_unmarked_at_most"] == 44


def test_probe_36x4_draw_ablation_lifts_hits_with_extra_draws() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    one = holdout_from_json(root / "2026-08-31-probe-36x4-draws1" / "hits" / "holdout.json")
    two = holdout_from_json(root / "2026-08-31-probe-36x4-draws2" / "hits" / "holdout.json")
    four = holdout_from_json(root / "2026-08-31-probe-36x4" / "hits" / "holdout.json")
    assert one.used_keys is False
    assert one.n_prompts_marked_above == 30
    assert two.n_prompts_marked_above == 33
    assert four.n_prompts_marked_above == 36
    assert one.n_files == 72
    assert two.n_files == 144
    assert four.n_files == 288
    one_auc = binary_eval(one.marked_lrs, one.unmarked_lrs, n_perm=200, seed=0).auc
    four_auc = binary_eval(four.marked_lrs, four.unmarked_lrs, n_perm=200, seed=0).auc
    assert one_auc > 0.82
    assert four_auc > one_auc


def test_transfer_12x4_to_36x4_nested_hits_fpr10_is_balanced() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-12x4-to-36x4"
    )
    hits = holdout_from_json(root / "hits" / "holdout.json")
    assert hits.used_keys is False
    assert hits.n_prompts == 24
    assert hits.n_prompts_marked_above == 24
    assert hits.n_files == 192
    stats = binary_eval(hits.marked_lrs, hits.unmarked_lrs, n_perm=400, seed=0)
    assert stats.auc > 0.90
    raw = json.loads((root / "results.json").read_text())
    assert raw["used_keys"] is False
    nested = next(
        r
        for r in raw["thresholds"]
        if r["name"] == "hits" and r["source"] == "nested-fpr10"
    )
    assert nested["n_marked_above"] == 83
    assert nested["n_unmarked_at_most"] == 85


def test_qwen_12x4_official_splits_all_first_draws() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-pair-qwen-12x4"
            / "results.json"
        ).read_text()
    )
    assert raw["model_name"] == "Qwen/Qwen2-1.5B-Instruct"
    assert len(raw["rows"]) == 12
    wins = sum(
        1
        for row in raw["rows"]
        if row["marked"]["mean"] > row["unmarked_gen"]["mean"]
    )
    assert wins == 12


def test_qwen_12x4_hits_does_not_match_gpt2_extra_draw_lift() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-qwen-12x4"
        / "hits"
        / "holdout.json"
    )
    hashed = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-qwen-12x4"
        / "hashpool"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 8
    assert hashed.n_prompts_marked_above == 7
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert 0.55 < stats.auc < 0.70


def test_gpt2_to_new_qwen_sample_does_not_replicate_eleven_of_twelve() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-gpt2-to-qwen-12x4"
        / "hits"
        / "holdout.json"
    )
    one = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-gpt2-to-qwen-12x4-draws1"
        / "hits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 5
    assert one.n_prompts_marked_above == 6
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc < 0.45


def test_prefix16_36x4_hits_is_front_loaded_and_key_free() -> None:
    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36x4-prefixes"
    )
    early = holdout_from_json(root / "prefix-16" / "hits" / "holdout.json")
    full = holdout_from_json(root / "prefix-128" / "hits" / "holdout.json")
    published = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36x4"
        / "hits"
        / "holdout.json"
    )
    assert early.used_keys is False
    assert early.n_prompts_marked_above == 34
    assert early.n_marked_positive == 129
    early_auc = binary_eval(early.marked_lrs, early.unmarked_lrs, n_perm=200, seed=0)
    assert early_auc.auc > 0.90
    assert full.n_prompts_marked_above == 36
    assert full.n_marked_positive == 134
    assert published.n_prompts_marked_above == 36
    assert published.n_marked_positive == 134
    from text_watermark_tools.stats import nested_threshold_by_stem

    nested = nested_threshold_by_stem(full.stems, full.marked_lrs, full.unmarked_lrs)
    assert nested.n_marked_above == 119
    assert nested.n_unmarked_at_most == 134


def test_ood_prefix16_hits_ranks_eleven_of_twelve() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-prefixes"
        / "prefix-16"
        / "hits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 11
    assert ev.n_marked_positive == 40
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc > 0.70
    from text_watermark_tools.stats import nested_threshold_by_stem

    nested = nested_threshold_by_stem(ev.stems, ev.marked_lrs, ev.unmarked_lrs)
    assert nested.n_marked_above == 25
    assert nested.n_unmarked_at_most == 29


def test_context_len_5_on_36x4_does_not_beat_last_four() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    k5 = holdout_from_json(root / "2026-08-31-probe-36x4-k5" / "hits" / "holdout.json")
    k4 = holdout_from_json(root / "2026-08-31-probe-36x4" / "hits" / "holdout.json")
    assert k5.used_keys is False
    assert k5.context_len == 5
    assert k5.n_prompts_marked_above == 35
    k5_auc = binary_eval(k5.marked_lrs, k5.unmarked_lrs, n_perm=200, seed=0).auc
    k4_auc = binary_eval(k4.marked_lrs, k4.unmarked_lrs, n_perm=200, seed=0).auc
    assert k5_auc < k4_auc
    assert k5_auc > 0.88


def test_gpt2_36x4_to_new_qwen_is_chance() -> None:
    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-qwen-12x4"
    )
    hits = holdout_from_json(root / "hits" / "holdout.json")
    hashed = holdout_from_json(root / "hashpool" / "holdout.json")
    surface = holdout_from_json(root / "surface" / "holdout.json")
    assert hits.used_keys is False
    assert hashed.used_keys is False
    assert surface.used_keys is False
    assert hits.n_prompts_marked_above == 6
    assert hashed.n_prompts_marked_above == 3
    assert surface.n_prompts_marked_above == 6
    hits_auc = binary_eval(hits.marked_lrs, hits.unmarked_lrs, n_perm=200, seed=0).auc
    assert hits_auc < 0.55


def test_gpt2_surface_to_new_qwen_is_chance() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-gpt2-surface-to-qwen-12x4"
        / "surface"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 7
    assert ev.n_marked_positive == 5
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc < 0.60


def test_window_0_16_matches_prefix_and_mid_window_is_weak() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    early = holdout_from_json(
        root / "2026-08-31-probe-36x4-windows" / "window-0-16" / "hits" / "holdout.json"
    )
    mid = holdout_from_json(
        root / "2026-08-31-probe-36x4-windows" / "window-16-32" / "hits" / "holdout.json"
    )
    tail = holdout_from_json(
        root / "2026-08-31-probe-36x4-windows" / "window-64-128" / "hits" / "holdout.json"
    )
    prefix = holdout_from_json(
        root / "2026-08-31-probe-36x4-prefixes" / "prefix-16" / "hits" / "holdout.json"
    )
    assert early.used_keys is False
    assert mid.used_keys is False
    assert early.n_prompts_marked_above == 34
    assert early.n_marked_positive == 129
    assert prefix.n_prompts_marked_above == 34
    early_auc = binary_eval(early.marked_lrs, early.unmarked_lrs, n_perm=200, seed=0)
    mid_auc = binary_eval(mid.marked_lrs, mid.unmarked_lrs, n_perm=200, seed=0)
    tail_auc = binary_eval(tail.marked_lrs, tail.unmarked_lrs, n_perm=200, seed=0)
    prefix_auc = binary_eval(prefix.marked_lrs, prefix.unmarked_lrs, n_perm=200, seed=0)
    assert abs(early_auc.auc - prefix_auc.auc) < 1e-9
    assert early_auc.auc > 0.90
    assert mid.n_prompts_marked_above == 22
    assert mid_auc.auc < 0.60
    assert tail.n_prompts_marked_above == 29
    assert tail_auc.auc > 0.65


def test_poshits_36x4_keeps_recall_and_lifts_specificity() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    hits = holdout_from_json(
        root / "2026-08-31-probe-36x4-posbucket" / "hits" / "holdout.json"
    )
    poshits = holdout_from_json(
        root / "2026-08-31-probe-36x4-posbucket" / "poshits" / "holdout.json"
    )
    fit16 = holdout_from_json(
        root / "2026-08-31-probe-36x4-fitprefix16" / "hits" / "holdout.json"
    )
    loo12 = holdout_from_json(
        root / "2026-08-31-probe-12x4-posbucket" / "poshits" / "holdout.json"
    )
    assert hits.used_keys is False
    assert poshits.used_keys is False
    assert fit16.used_keys is False
    assert loo12.used_keys is False
    assert hits.n_prompts_marked_above == 36
    assert poshits.n_prompts_marked_above == 34
    assert poshits.n_marked_positive == 134
    assert poshits.n_unmarked_nonpositive == 97
    assert poshits.n_unmarked_nonpositive > hits.n_unmarked_nonpositive
    pos_auc = binary_eval(poshits.marked_lrs, poshits.unmarked_lrs, n_perm=200, seed=0)
    assert pos_auc.auc > 0.90
    assert fit16.n_prompts_marked_above == 34
    assert fit16.n_marked_positive == 132
    assert fit16.n_unmarked_nonpositive == 112
    fit_auc = binary_eval(fit16.marked_lrs, fit16.unmarked_lrs, n_perm=200, seed=0)
    assert fit_auc.auc > 0.92
    assert loo12.n_prompts_marked_above == 10
    assert loo12.n_marked_positive == 24
    from text_watermark_tools.stats import nested_threshold_by_stem

    nested = nested_threshold_by_stem(
        poshits.stems, poshits.marked_lrs, poshits.unmarked_lrs
    )
    assert nested.n_marked_above == 119
    assert nested.n_unmarked_at_most == 129
    nested16 = nested_threshold_by_stem(fit16.stems, fit16.marked_lrs, fit16.unmarked_lrs)
    assert nested16.n_marked_above == 121
    assert nested16.n_unmarked_at_most == 136


def test_ood_poshits_and_fit_prefix_raise_file_auc() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    hits = holdout_from_json(
        root / "2026-08-31-transfer-36x4-to-12x4-posbucket" / "hits" / "holdout.json"
    )
    poshits = holdout_from_json(
        root / "2026-08-31-transfer-36x4-to-12x4-posbucket" / "poshits" / "holdout.json"
    )
    fit16 = holdout_from_json(
        root / "2026-08-31-transfer-36x4-to-12x4-fitprefix16" / "hits" / "holdout.json"
    )
    assert hits.used_keys is False
    assert poshits.used_keys is False
    assert fit16.used_keys is False
    assert hits.n_prompts_marked_above == 12
    assert poshits.n_prompts_marked_above == 10
    assert poshits.n_marked_positive == 39
    assert poshits.n_unmarked_nonpositive == 31
    pos_auc = binary_eval(poshits.marked_lrs, poshits.unmarked_lrs, n_perm=200, seed=0)
    hits_auc = binary_eval(hits.marked_lrs, hits.unmarked_lrs, n_perm=200, seed=0)
    assert pos_auc.auc > 0.80
    assert pos_auc.auc > hits_auc.auc
    assert fit16.n_prompts_marked_above == 11
    assert fit16.n_unmarked_nonpositive == 31
    fit_auc = binary_eval(fit16.marked_lrs, fit16.unmarked_lrs, n_perm=200, seed=0)
    assert fit_auc.auc > 0.80
    assert fit_auc.auc > hits_auc.auc
    from text_watermark_tools.stats import nested_threshold_by_stem

    nested_pos = nested_threshold_by_stem(
        poshits.stems, poshits.marked_lrs, poshits.unmarked_lrs
    )
    assert nested_pos.n_marked_above == 37
    assert nested_pos.n_unmarked_at_most == 35
    nested16 = nested_threshold_by_stem(fit16.stems, fit16.marked_lrs, fit16.unmarked_lrs)
    assert nested16.n_marked_above == 39
    assert nested16.n_unmarked_at_most == 36


def test_fit_prefix_poshits_bucket4_beats_unbucketed_matched_prefix() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    pos = holdout_from_json(
        root / "2026-08-31-probe-36x4-fitprefix16-pos4" / "poshits" / "holdout.json"
    )
    hits = holdout_from_json(
        root / "2026-08-31-probe-36x4-fitprefix16" / "hits" / "holdout.json"
    )
    ood = holdout_from_json(
        root
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos4"
        / "poshits"
        / "holdout.json"
    )
    assert pos.used_keys is False
    assert ood.used_keys is False
    assert pos.n_prompts_marked_above == 34
    assert pos.n_marked_positive == 133
    assert pos.n_unmarked_nonpositive == 114
    pos_auc = binary_eval(pos.marked_lrs, pos.unmarked_lrs, n_perm=200, seed=0)
    hits_auc = binary_eval(hits.marked_lrs, hits.unmarked_lrs, n_perm=200, seed=0)
    assert pos_auc.auc > 0.93
    assert pos_auc.auc > hits_auc.auc
    assert ood.n_prompts_marked_above == 11
    assert ood.n_unmarked_nonpositive == 33
    ood_auc = binary_eval(ood.marked_lrs, ood.unmarked_lrs, n_perm=200, seed=0)
    assert ood_auc.auc > 0.80
    from text_watermark_tools.stats import nested_threshold_by_stem

    nested = nested_threshold_by_stem(ood.stems, ood.marked_lrs, ood.unmarked_lrs)
    assert nested.n_marked_above == 39
    assert nested.n_unmarked_at_most == 38


def test_ood_window_16_32_hits_is_near_chance() -> None:
    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-windows"
    )
    early = holdout_from_json(root / "window-0-16" / "hits" / "holdout.json")
    mid = holdout_from_json(root / "window-16-32" / "hits" / "holdout.json")
    assert early.used_keys is False
    assert early.n_prompts_marked_above == 11
    assert mid.n_prompts_marked_above == 8
    early_auc = binary_eval(early.marked_lrs, early.unmarked_lrs, n_perm=200, seed=0)
    mid_auc = binary_eval(mid.marked_lrs, mid.unmarked_lrs, n_perm=200, seed=0)
    assert early_auc.auc > 0.70
    assert mid_auc.auc < 0.60


def test_hits_coverage_on_lab_pairs_is_front_loaded(tmp_path) -> None:
    from text_watermark_tools.probe import persist_probe, rotate_hits_coverage

    twins = load_twins(PAIR)
    cov = rotate_hits_coverage(
        twins,
        context_len=2,
        windows=((0, 16), (16, 32), (32, 64)),
        max_index=64,
    )
    assert cov["used_keys"] is False
    assert cov["used_hash_iv"] is False
    assert cov["used_g_values"] is False
    by_win = {(row["start"], row["end"]): row for row in cov["by_window"]}
    early = by_win[(0, 16)]
    mid = by_win[(16, 32)]
    assert early["n"] > 0
    assert mid["n"] > 0
    assert early["shared_frac"] > mid["shared_frac"]
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        context_len=2,
        methods=(),
        with_coverage=True,
        windows=((0, 16), (16, 32)),
    )
    assert run.methods == []
    assert run.coverage is not None
    assert run.coverage["used_keys"] is False
    persist_probe(run, tmp_path)
    assert (tmp_path / "coverage.json").is_file()
    assert (tmp_path / "coverage.md").is_file()


def test_coverage_36x4_opening_has_more_shared_last4() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-probe-36x4-coverage"
            / "coverage.json"
        ).read_text()
    )
    assert raw["used_keys"] is False
    by_win = {(row["start"], row["end"]): row for row in raw["by_window"]}
    early = by_win[(0, 16)]
    mid = by_win[(16, 32)]
    assert early["shared"] == 592
    assert early["n"] == 4320
    assert mid["shared"] == 181
    assert mid["n"] == 4608
    assert early["shared_frac"] > 0.12
    assert mid["shared_frac"] < 0.05
    assert early["mean_shared_support"] > 80
    assert mid["mean_shared_support"] < 20
    by_i = {row["start"]: row for row in raw["by_index"]}
    assert by_i[1]["shared_frac"] > 0.90
    four_to_sixteen = sum(by_i[i]["shared"] for i in range(4, 16))
    four_to_sixteen_n = sum(by_i[i]["n"] for i in range(4, 16))
    assert four_to_sixteen / four_to_sixteen_n < 0.05


def test_poshitmass_matched_prefix_beats_poshits_auc() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    mass = holdout_from_json(
        root
        / "2026-08-31-probe-36x4-fitprefix16-poshitmass"
        / "poshitmass"
        / "holdout.json"
    )
    pos = holdout_from_json(
        root / "2026-08-31-probe-36x4-fitprefix16-poshitmass" / "poshits" / "holdout.json"
    )
    assert mass.used_keys is False
    assert mass.n_prompts_marked_above == 34
    assert mass.n_marked_positive == 133
    assert mass.n_unmarked_nonpositive == 114
    mass_auc = binary_eval(mass.marked_lrs, mass.unmarked_lrs, n_perm=200, seed=0)
    pos_auc = binary_eval(pos.marked_lrs, pos.unmarked_lrs, n_perm=200, seed=0)
    assert mass_auc.auc > 0.94
    assert mass_auc.auc > pos_auc.auc


def test_finest_bucket_balances_in_domain_t0() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36x4-fitprefix16-pos-sweep"
    )
    b1 = holdout_from_json(root / "bucket-1" / "poshits" / "holdout.json")
    b2 = holdout_from_json(root / "bucket-2" / "poshits" / "holdout.json")
    assert b1.used_keys is False
    assert b1.n_prompts_marked_above == 34
    assert b1.n_marked_positive == 132
    assert b1.n_unmarked_nonpositive == 132
    auc = binary_eval(b1.marked_lrs, b1.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc > 0.93
    assert b1.marked_lrs == b2.marked_lrs
    assert b1.unmarked_lrs == b2.unmarked_lrs
    summary = json.loads((root / "results.json").read_text())
    assert summary["used_keys"] is False
    by_b = {row["bucket"]: row for row in summary["buckets"]}
    assert by_b[4]["binary"]["n_positive_above_zero"] == 133
    assert by_b[4]["binary"]["n_negative_at_most_zero"] == 114


def test_ood_bucket1_poshits_is_twelve_of_twelve_and_balanced() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos1"
    )
    ev = holdout_from_json(root / "poshits" / "holdout.json")
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 39
    assert ev.n_unmarked_nonpositive == 41
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc > 0.85
    from text_watermark_tools.stats import nested_threshold_by_stem

    nested = nested_threshold_by_stem(ev.stems, ev.marked_lrs, ev.unmarked_lrs)
    assert nested.n_marked_above == 39
    assert nested.n_unmarked_at_most == 41
    table = json.loads((root / "results.json").read_text())
    fpr10 = next(
        r
        for r in table["thresholds"]
        if r["name"] == "poshits" and r["source"] == "nested-fpr10"
    )
    assert fpr10["n_marked_above"] == 39
    assert fpr10["n_unmarked_at_most"] == 41
    youden = next(
        r
        for r in table["thresholds"]
        if r["name"] == "poshits" and r["source"] == "nested-youden"
    )
    assert youden["n_marked_above"] == 16
    assert youden["n_unmarked_at_most"] == 48


def test_ood_poshitmass_nested_fpr10_matches_nested_stem() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix16-poshitmass"
    )
    ev = holdout_from_json(root / "poshitmass" / "holdout.json")
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 11
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc > 0.82
    table = json.loads((root / "results.json").read_text())
    fpr10 = next(
        r
        for r in table["thresholds"]
        if r["name"] == "poshitmass" and r["source"] == "nested-fpr10"
    )
    assert fpr10["n_marked_above"] == 39
    assert fpr10["n_unmarked_at_most"] == 38


def test_12x4_matched_prefix_bucket1_is_not_the_hard_isolated_gate() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-12x4-fitprefix16-pos1"
        / "poshits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 9
    assert ev.n_marked_positive == 23
    assert ev.n_unmarked_nonpositive == 48
    # Leave-one-of-12-out is not the published 29/48 hard sign.
    assert ev.n_marked_positive < 29


def test_qwen_matched_prefix_poshits_bucket1_is_chance() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-qwen-fitprefix16-pos1"
        / "poshits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 8
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc < 0.60


def test_opening_four_tokens_match_sixteen_token_prefix_ranking() -> None:
    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36x4-windows-opening"
    )
    early = holdout_from_json(root / "window-0-4" / "hits" / "holdout.json")
    prefix = holdout_from_json(root / "window-0-16" / "hits" / "holdout.json")
    mid = holdout_from_json(root / "window-4-16" / "hits" / "holdout.json")
    late = holdout_from_json(root / "window-16-32" / "hits" / "holdout.json")
    assert early.used_keys is False
    assert early.n_prompts_marked_above == 34
    assert prefix.n_prompts_marked_above == 34
    assert mid.n_prompts_marked_above == 29
    assert late.n_prompts_marked_above == 22
    early_auc = binary_eval(early.marked_lrs, early.unmarked_lrs, n_perm=200, seed=0)
    prefix_auc = binary_eval(prefix.marked_lrs, prefix.unmarked_lrs, n_perm=200, seed=0)
    mid_auc = binary_eval(mid.marked_lrs, mid.unmarked_lrs, n_perm=200, seed=0)
    late_auc = binary_eval(late.marked_lrs, late.unmarked_lrs, n_perm=200, seed=0)
    assert early_auc.auc > 0.90
    assert abs(early_auc.auc - prefix_auc.auc) < 0.01
    assert 0.65 < mid_auc.auc < 0.80
    assert late_auc.auc < 0.60


def test_matched_four_token_poshits_ood_nested_youden_matches_t0() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix4-pos1"
    )
    ev = holdout_from_json(root / "poshits" / "holdout.json")
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 39
    assert ev.n_unmarked_nonpositive == 41
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc > 0.85
    table = json.loads((root / "results.json").read_text())
    youden = next(
        r
        for r in table["thresholds"]
        if r["name"] == "poshits" and r["source"] == "nested-youden"
    )
    assert youden["n_marked_above"] == 39
    assert youden["n_unmarked_at_most"] == 41
    in_domain = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36x4-fitprefix4-pos1"
        / "poshits"
        / "holdout.json"
    )
    assert in_domain.n_prompts_marked_above == 34
    assert in_domain.n_marked_positive == 131
    assert in_domain.n_unmarked_nonpositive == 132


def test_last1_four_token_ood_matches_last4_poshits_gate() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix4-k1-pos1"
        / "poshits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 39
    assert ev.n_unmarked_nonpositive == 41
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc > 0.85
    first = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix4-k1-pos1"
        / "first"
        / "holdout.json"
    )
    assert first.n_prompts_marked_above == 6


def test_include_first_hurts_the_four_token_ood_gate() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix4-include-first"
        / "poshits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 9
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc < 0.80
    in_domain = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-36x4-fitprefix4-include-first"
        / "poshits"
        / "holdout.json"
    )
    assert in_domain.n_prompts_marked_above == 35


def test_prompt_context_ood_ranks_without_isolated_recall() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-fitprefix4-prompt-context"
        / "poshits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert ev.n_marked_positive == 13
    assert ev.n_unmarked_nonpositive == 48


def test_qwen_first_token_opening_is_twelve_of_twelve() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-qwen-12x4-fitprefix4-pos1"
        / "first"
        / "holdout.json"
    )
    hits = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-qwen-12x4-fitprefix4-pos1"
        / "hits"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 12
    assert hits.n_prompts_marked_above == 7
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc > 0.85
    xfer = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-qwen-fitprefix4-include-first"
        / "poshits"
        / "holdout.json"
    )
    assert xfer.n_prompts_marked_above == 8
    xfer_auc = binary_eval(xfer.marked_lrs, xfer.unmarked_lrs, n_perm=200, seed=0)
    assert xfer_auc.auc < 0.65


def test_distilgpt2_official_splits_and_gpt2_hits_do_not_transfer() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-31-pair-distilgpt2-12x4"
            / "results.json"
        ).read_text()
    )
    assert raw["model_name"] == "distilgpt2"
    wins = sum(
        1
        for row in raw["rows"]
        if row["marked"]["mean"] > row["unmarked_gen"]["mean"]
    )
    assert wins == 12
    in_domain = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-distilgpt2-12x4"
        / "hits"
        / "holdout.json"
    )
    assert in_domain.used_keys is False
    assert in_domain.n_prompts_marked_above == 9
    xfer = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-distilgpt2-12x4"
        / "hits"
        / "holdout.json"
    )
    assert xfer.n_prompts_marked_above == 5
    auc = binary_eval(xfer.marked_lrs, xfer.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc < 0.55


def test_distilgpt2_native_rankpath_is_chance() -> None:
    opening = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    prefix = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-distilgpt2-12x4-prefix4-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    uni = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath"
        / "rankuni"
        / "holdout.json"
    )
    assert opening.used_keys is False
    assert prefix.used_keys is False
    assert opening.n_prompts_marked_above == 8
    assert opening.n_marked_positive == 28
    assert opening.n_unmarked_nonpositive == 32
    assert prefix.n_prompts_marked_above == 7
    assert prefix.n_marked_positive == 23
    assert uni.n_prompts_marked_above == 5
    opening_auc = binary_eval(opening.marked_lrs, opening.unmarked_lrs, n_perm=200, seed=0)
    prefix_auc = binary_eval(prefix.marked_lrs, prefix.unmarked_lrs, n_perm=200, seed=0)
    assert opening_auc.auc < 0.65
    assert prefix_auc.auc < 0.65


def test_gpt2_rankpath_on_distil_tokens_is_not_a_distil_reader() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-distilgpt2-fitprefix4-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 9
    assert ev.n_marked_positive == 21
    assert ev.n_unmarked_nonpositive == 34
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert 0.58 < auc.auc < 0.70


def test_stem60_prefix4_rankpath_matches_short_combined_accuracy() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-short-medium-tails-family-to-12x4-prefix4-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    uni = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-short-medium-tails-family-to-12x4-prefix4-rankpath"
        / "rankuni"
        / "holdout.json"
    )
    short = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-36x4-to-12x4-rankpath-full-isolated"
        / "prefix-4"
        / "rankpath"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 10
    assert ev.n_marked_positive == 28
    assert ev.n_unmarked_nonpositive == 40
    assert uni.n_prompts_marked_above == 11
    assert uni.n_marked_positive == 39
    assert uni.n_unmarked_nonpositive == 32
    assert short.n_marked_positive == 25
    assert short.n_unmarked_nonpositive == 43
    assert ev.n_marked_positive + ev.n_unmarked_nonpositive == 68
    assert short.n_marked_positive + short.n_unmarked_nonpositive == 68
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc > 0.72


def test_qwen_native_opening_rankpath_does_not_match_first_token() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-qwen-12x4-fitprefix4-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    first = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-qwen-12x4-fitprefix4-pos1"
        / "first"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 8
    assert ev.n_marked_positive == 24
    assert ev.n_unmarked_nonpositive == 32
    assert first.n_prompts_marked_above == 12
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    first_auc = binary_eval(first.marked_lrs, first.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc < 0.70
    assert first_auc.auc > 0.85
    prefix = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-qwen-12x4-prefix4-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    assert prefix.used_keys is False
    assert prefix.n_prompts_marked_above == 9
    assert prefix.n_marked_positive == 25
    assert prefix.n_unmarked_nonpositive == 33
    prefix_auc = binary_eval(prefix.marked_lrs, prefix.unmarked_lrs, n_perm=200, seed=0)
    assert 0.60 < prefix_auc.auc < 0.75


def _snap_twin(stem: str) -> object:
    from text_watermark_tools.blind import Twin

    return Twin(
        stem=stem,
        marked_text="m",
        unmarked_text="u",
        marked_ids=[0, 1],
        unmarked_ids=[0, 1],
        extra_marked_ids=[[0, 2]],
        extra_unmarked_ids=[[0, 2]],
    )


def test_rotate_snaprate_needs_no_tables_or_keys() -> None:
    import numpy as np

    from text_watermark_tools.probe import rotate_snaprate, transfer_snaprate
    from text_watermark_tools.stats import roc_auc

    def _row(rank: float, in_topk: float) -> list[float]:
        return [0.0, rank, rank, in_topk, 0.0, 1.0]

    twins = [_snap_twin("a"), _snap_twin("b")]
    mats = {}
    for stem in ("a", "b"):
        mats[(stem, 1, "marked")] = np.array([_row(2, 1.0), _row(3, 1.0)])
        mats[(stem, 1, "unmarked")] = np.array([_row(1, 1.0), _row(1, 1.0)])
        mats[(stem, 2, "marked")] = np.array([_row(41, 0.0), _row(42, 0.0)])
        mats[(stem, 2, "unmarked")] = np.array([_row(1, 1.0), _row(1, 1.0)])
    out = rotate_snaprate(twins, methods=("snapleave", "snapupset", "snapmiss"), mats=mats)
    assert set(out) == {"snapleave", "snapupset", "snapmiss"}
    leave = out["snapleave"]
    assert leave.used_keys is False
    assert leave.used_hash_iv is False
    assert leave.used_g_values is False
    assert leave.n_prompts_marked_above == 2
    assert min(leave.marked_lrs) > max(leave.unmarked_lrs)
    assert roc_auc(leave.marked_lrs, leave.unmarked_lrs) == 1.0
    # Unmarked twins stay greedy. Only the all-miss marked draw signs on snapmiss.
    assert out["snapmiss"].n_marked_positive == 2
    assert out["snapmiss"].n_unmarked_nonpositive == 4
    test_out, train_out = transfer_snaprate(
        twins[:1],
        twins[1:],
        methods=("snapleave",),
        train_mats=mats,
        test_mats=mats,
    )
    assert train_out["snapleave"].mode == "train"
    assert test_out["snapleave"].mode == "transfer"
    assert test_out["snapleave"].used_keys is False
    assert test_out["snapleave"].n_prompts_marked_above == 1

