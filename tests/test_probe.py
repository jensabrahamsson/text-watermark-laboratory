"""Probe CLI and published 12×4 holdout statistics."""

from pathlib import Path

from text_watermark_tools.blind import load_twins
from text_watermark_tools.cli import main
from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.probe import (
    apply_overlap,
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


def test_probe_count_methods_on_lab_pairs_are_key_free() -> None:
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
