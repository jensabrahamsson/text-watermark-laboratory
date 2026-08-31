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
    assert 0 < swapped < len(twins)
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
