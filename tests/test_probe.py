"""Probe CLI and published 12×4 holdout statistics."""

import json
from pathlib import Path

from text_watermark_tools.blind import load_twins
from text_watermark_tools.cli import main
from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.probe import (
    apply_overlap,
    persist_probe,
    rotate_count_methods,
    rotate_hashpool,
    rotate_score_stack,
    run_probe,
    run_transfer,
    shuffle_twin_sides,
)
from text_watermark_tools.stats import binary_eval, binomial_sf, coverage_gate

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


def test_recount_hard_last4_drops_the_opening_overcount() -> None:
    import json

    root = Path(__file__).resolve().parents[1] / "experiments"
    hard = holdout_from_json(
        root / "2026-09-01-probe-12x4-recount-hard-last4" / "hard" / "holdout.json"
    )
    assert hard.used_keys is False
    assert hard.used_hash_iv is False
    assert hard.used_g_values is False
    assert hard.n_prompts == 12
    assert hard.n_prompts_marked_above == 9
    assert hard.n_marked_positive == 25
    assert hard.n_unmarked_nonpositive == 22
    stats = binary_eval(hard.marked_lrs, hard.unmarked_lrs, n_perm=500, seed=0)
    assert 0.55 < stats.auc < 0.63
    assert stats.permutation_p < 0.05
    assert binomial_sf(9, 12, 0.5) > 0.05
    assert stats.binomial_p_above_zero > 0.05

    interpolate = holdout_from_json(
        root / "2026-09-01-probe-12x4-recount-hard-last4" / "interpolate" / "holdout.json"
    )
    assert interpolate.n_prompts_marked_above == 7

    blind = json.loads(
        (root / "2026-09-01-blind-12x4-recount-last4" / "results.json").read_text()
    )
    assert blind["n_marked_wins"] == 9
    margin = json.loads(
        (root / "2026-09-01-blind-12x4-recount-last4-margin" / "results.json").read_text()
    )
    assert margin["n_marked_wins"] == 10

    hits = holdout_from_json(
        root / "2026-09-01-probe-12x4-recount-hits" / "hits" / "holdout.json"
    )
    assert hits.n_prompts_marked_above == 10
    assert hits.n_marked_positive == 28
    hits_stats = binary_eval(hits.marked_lrs, hits.unmarked_lrs, n_perm=200, seed=0)
    assert hits_stats.auc > 0.70

    poshits = holdout_from_json(
        root
        / "2026-09-01-probe-12x4-recount-opening-poshits"
        / "poshits"
        / "holdout.json"
    )
    assert poshits.n_prompts_marked_above == 9
    assert poshits.n_marked_positive == 23

    rank = holdout_from_json(
        root
        / "2026-09-01-probe-12x4-recount-opening-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    assert rank.n_prompts_marked_above == 11
    assert rank.n_marked_positive == 41
    assert rank.n_unmarked_nonpositive == 35

    hits36 = holdout_from_json(
        root / "2026-09-01-probe-36x4-recount-hits" / "hits" / "holdout.json"
    )
    assert hits36.n_prompts == 36
    assert hits36.n_prompts_marked_above == 36
    hits36_stats = binary_eval(
        hits36.marked_lrs, hits36.unmarked_lrs, n_perm=200, seed=0
    )
    assert hits36_stats.auc > 0.92


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


def test_run_probe_hashtok_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        context_len=2,
        methods=("hashpool", "hashtok"),
        with_hashpool=True,
        with_pivot=False,
        n_hashes=4,
        n_buckets=32,
    )
    names = [m.name for m in run.methods]
    assert names == ["hashpool", "hashtok"]
    assert run.used_keys is False
    ht = next(m for m in run.methods if m.name == "hashtok")
    assert ht.holdout.instance == "key-free-hashtok"
    assert ht.holdout.score_kind == "hashtok"
    assert ht.binary.n_positive == 3


def test_run_probe_hashtokbackoff_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        context_len=2,
        methods=("hashtokbackoff", "hashtokbackoff2"),
        with_hashpool=True,
        with_pivot=False,
        n_hashes=4,
        n_buckets=16,
    )
    names = [m.name for m in run.methods]
    assert names == ["hashtokbackoff", "hashtokbackoff2"]
    assert run.used_keys is False
    hb = next(m for m in run.methods if m.name == "hashtokbackoff")
    assert hb.holdout.instance == "key-free-hashtokbackoff"
    hb2 = next(m for m in run.methods if m.name == "hashtokbackoff2")
    assert hb2.holdout.instance == "key-free-hashtokbackoff2"


def test_run_probe_hashtoklen_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        methods=("hashtoklen", "hashtoklenbackoff", "hashtoklenbackoff2"),
        with_pivot=False,
    )
    names = [m.name for m in run.methods]
    assert names == ["hashtoklen", "hashtoklenbackoff", "hashtoklenbackoff2"]
    assert run.used_keys is False
    hl = next(m for m in run.methods if m.name == "hashtoklen")
    assert hl.holdout.instance == "key-free-hashtoklen"
    hlb = next(m for m in run.methods if m.name == "hashtoklenbackoff")
    assert hlb.holdout.instance == "key-free-hashtoklenbackoff"
    hlb2 = next(m for m in run.methods if m.name == "hashtoklenbackoff2")
    assert hlb2.holdout.instance == "key-free-hashtoklenbackoff2"


def test_run_probe_hashskip_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        methods=("hashskip",),
        with_pivot=False,
    )
    names = [m.name for m in run.methods]
    assert names == ["hashskip"]
    assert run.used_keys is False
    hsk = run.methods[0]
    assert hsk.holdout.instance == "key-free-hashskip"
    assert hsk.holdout.used_keys is False


def test_run_probe_hashtok2_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        methods=("hashtok2",),
        with_pivot=False,
        n_hashes=4,
        n_buckets=16,
    )
    names = [m.name for m in run.methods]
    assert names == ["hashtok2"]
    assert run.used_keys is False
    ht2 = run.methods[0]
    assert ht2.holdout.instance == "key-free-hashtok2"
    assert ht2.holdout.used_keys is False
    assert ht2.holdout.used_hash_iv is False
    assert ht2.holdout.used_g_values is False
    from text_watermark_tools.transfer import HASH_CASCADE_READERS

    assert "hashtok2" not in HASH_CASCADE_READERS


def test_run_probe_hashtoklen2_and_hashskip2_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        methods=("hashtoklen2", "hashskip2"),
        with_pivot=False,
    )
    names = [m.name for m in run.methods]
    assert names == ["hashtoklen2", "hashskip2"]
    assert run.used_keys is False
    hl2 = next(m for m in run.methods if m.name == "hashtoklen2")
    assert hl2.holdout.instance == "key-free-hashtoklen2"
    hsk2 = next(m for m in run.methods if m.name == "hashskip2")
    assert hsk2.holdout.instance == "key-free-hashskip2"


def test_run_probe_tokhybrid_and_poshashtok_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        methods=("tokhybrid", "poshashtok"),
        with_pivot=False,
        position_bucket=2,
        n_hashes=4,
        n_buckets=16,
    )
    names = [m.name for m in run.methods]
    assert set(names) == {"tokhybrid", "poshashtok"}
    assert run.used_keys is False
    thyb = next(m for m in run.methods if m.name == "tokhybrid")
    pht = next(m for m in run.methods if m.name == "poshashtok")
    assert thyb.holdout.instance == "key-free-tokhybrid"
    assert pht.holdout.instance == "key-free-poshashtok"
    assert thyb.holdout.used_keys is False
    assert pht.holdout.used_keys is False


def test_run_probe_hashtokgap_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        methods=("hashtokgap",),
        with_pivot=False,
        n_hashes=4,
        n_buckets=16,
    )
    names = [m.name for m in run.methods]
    assert names == ["hashtokgap"]
    assert run.used_keys is False
    gap = run.methods[0]
    assert gap.holdout.instance == "key-free-hashtokgap"
    assert gap.holdout.used_keys is False
    assert gap.holdout.used_hash_iv is False
    assert gap.holdout.used_g_values is False


def test_run_probe_hashmask_on_lab_pairs() -> None:
    twins = load_twins(PAIR)
    run = run_probe(
        twins,
        pair_dir=str(PAIR),
        methods=("hashmask",),
        with_pivot=False,
    )
    names = [m.name for m in run.methods]
    assert names == ["hashmask"]
    assert run.used_keys is False
    hmk = run.methods[0]
    assert hmk.holdout.instance == "key-free-hashmask"
    assert hmk.holdout.used_keys is False


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
        methods=("hard", "hits", "hashpool", "hashtok", "hybrid", "stack"),
        overlap_mode="keep",
        n_hashes=4,
        n_buckets=16,
        nested=False,
    )
    names = [m.name for m in run.methods]
    assert names == ["hard", "hits", "hashpool", "hashtok", "hybrid", "stack"]
    assert run.used_keys is False
    assert run.n_train_prompts == 2
    assert run.n_test_prompts == 1
    assert run.thresholds
    hp = next(m for m in run.methods if m.name == "hashpool")
    assert hp.holdout.mode == "transfer"
    assert hp.holdout.instance == "key-free-hashpool"
    ht = next(m for m in run.methods if m.name == "hashtok")
    assert ht.holdout.instance == "key-free-hashtok"
    assert ht.holdout.score_kind == "hashtok"
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


def test_pair_100x4_official_splits_all_first_draws() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-pair-100x4"
            / "results.json"
        ).read_text()
    )
    assert raw["instance"] == "public-deepmind-30"
    assert raw["max_new_tokens"] == 128
    assert raw["model_name"] == "gpt2"
    assert raw["seed"] == 20260901
    assert len(raw["rows"]) == 100
    wins = sum(
        1
        for row in raw["rows"]
        if row["marked"]["mean"] > row["unmarked_gen"]["mean"]
    )
    assert wins == 100


def test_protocol_next_phase_a_locks_on_100x4() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    lock_a = holdout_from_json(
        root / "2026-09-01-probe-100x4-hard-last4" / "interpolate" / "holdout.json"
    )
    assert lock_a.used_keys is False
    assert lock_a.used_hash_iv is False
    assert lock_a.used_g_values is False
    assert lock_a.n_prompts == 100
    assert lock_a.n_prompts_marked_above == 99
    assert lock_a.n_marked_positive == 352
    lock_a_probe = json.loads(
        (root / "2026-09-01-probe-100x4-hard-last4" / "results.json").read_text()
    )
    lock_a_youden = next(
        m["nested_stem"]["nested-youden-by-stem"]
        for m in lock_a_probe["methods"]
        if m["name"] == "interpolate"
    )
    assert lock_a_youden["n_marked_above"] == 322
    assert lock_a_youden["n_unmarked_at_most"] == 338
    stats = binary_eval(lock_a.marked_lrs, lock_a.unmarked_lrs, n_perm=400, seed=0)
    assert stats.auc > 0.85
    assert stats.permutation_p < 0.01
    assert binomial_sf(99, 100, 0.5) < 0.001

    lock_b = holdout_from_json(
        root / "2026-09-01-probe-100x4-opening-poshits" / "poshits" / "holdout.json"
    )
    assert lock_b.used_keys is False
    assert lock_b.n_prompts_marked_above == 100
    lock_b_probe = json.loads(
        (root / "2026-09-01-probe-100x4-opening-poshits" / "results.json").read_text()
    )
    lock_b_youden = next(
        m["nested_stem"]["nested-youden-by-stem"]
        for m in lock_b_probe["methods"]
        if m["name"] == "poshits"
    )
    assert lock_b_youden["n_marked_above"] == 392
    assert lock_b_youden["n_unmarked_at_most"] == 382
    assert lock_b_probe["methods"][0]["coverage_gate"]["n_unmarked_zero"] == 198

    lock_c = holdout_from_json(
        root / "2026-09-01-probe-100x4-opening-rankpath" / "rankpath" / "holdout.json"
    )
    assert lock_c.used_keys is False
    assert lock_c.n_prompts_marked_above == 96

    early = holdout_from_json(
        root
        / "2026-09-01-probe-100x4-hard-windows"
        / "window-0-4"
        / "interpolate"
        / "holdout.json"
    )
    mid = holdout_from_json(
        root
        / "2026-09-01-probe-100x4-hard-windows"
        / "window-16-32"
        / "interpolate"
        / "holdout.json"
    )
    assert early.n_prompts_marked_above == 99
    assert mid.n_prompts_marked_above == 89
    early_stats = binary_eval(early.marked_lrs, early.unmarked_lrs, n_perm=200, seed=0)
    mid_stats = binary_eval(mid.marked_lrs, mid.unmarked_lrs, n_perm=200, seed=0)
    assert early_stats.auc > mid_stats.auc
    assert early.n_prompts_marked_above > mid.n_prompts_marked_above


def test_pair_distil_100x4_official_is_weaker_than_gpt2() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-pair-distil-100x4"
            / "results.json"
        ).read_text()
    )
    assert raw["instance"] == "public-deepmind-30"
    assert raw["model_name"] == "distilgpt2"
    assert raw["seed"] == 20260901
    assert len(raw["rows"]) == 100
    wins = sum(
        1
        for row in raw["rows"]
        if row["marked"]["mean"] > row["unmarked_gen"]["mean"]
    )
    assert wins == 70


def test_protocol_next_phase_b_distil_opening_locks() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    poshits = holdout_from_json(
        root / "2026-09-01-probe-distil-100x4-opening-poshits" / "poshits" / "holdout.json"
    )
    rankpath = holdout_from_json(
        root / "2026-09-01-probe-distil-100x4-opening-rankpath" / "rankpath" / "holdout.json"
    )
    assert poshits.used_keys is False
    assert rankpath.used_keys is False
    assert poshits.n_prompts == 100
    assert poshits.n_prompts_marked_above == 89
    assert rankpath.n_prompts_marked_above == 69
    assert poshits.n_marked_positive == 216
    assert poshits.n_unmarked_nonpositive == 247
    # H3 on Distil: rankpath drops more from GPT-2 Phase A than poshits.
    assert (96 - rankpath.n_prompts_marked_above) > (100 - poshits.n_prompts_marked_above)


def test_protocol_isolated_freezes_out_of_family_transfer_commands() -> None:
    text = (
        Path(__file__).resolve().parents[1] / "research" / "PROTOCOL-isolated.md"
    ).read_text()
    assert "--methods interpolate --context-len 4" in text
    assert "--methods poshits --fit-prefix 4 --pos-bucket 1" in text
    assert "--methods rankpath --fit-prefix 4 --pos-bucket 1" in text
    assert "2026-09-01-transfer-100x4-to-12x4-hard-last4" in text
    assert "2026-09-01-transfer-100x4-to-36x4-opening-poshits" in text
    assert "**25/48**" in text
    assert "nested Youden" in text


def _transfer_threshold(results: dict, name: str, source: str) -> dict:
    return next(
        r
        for r in results["thresholds"]
        if r["name"] == name and r["source"] == source
    )


def test_protocol_isolated_100x4_to_12x4_locks() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    hard = json.loads(
        (root / "2026-09-01-transfer-100x4-to-12x4-hard-last4" / "results.json").read_text()
    )
    poshits = json.loads(
        (
            root / "2026-09-01-transfer-100x4-to-12x4-opening-poshits" / "results.json"
        ).read_text()
    )
    assert hard["used_keys"] is False
    assert poshits["used_keys"] is False
    assert hard["n_train_prompts"] == 100
    assert hard["n_test_prompts"] == 12
    assert hard["dropped_stems"] == []
    assert hard["methods"][0]["n_prompt_wins"] == 8
    assert poshits["methods"][0]["n_prompt_wins"] == 11
    # H-iso-B: opening poshits ranks the original 12 at least as high as interpolate.
    assert poshits["methods"][0]["n_prompt_wins"] >= hard["methods"][0]["n_prompt_wins"]
    nested_a = _transfer_threshold(hard, "interpolate", "nested-youden")
    nested_b = _transfer_threshold(poshits, "poshits", "nested-youden")
    assert nested_a["n_marked_above"] == 23
    assert nested_a["n_unmarked_at_most"] == 38
    assert nested_b["n_marked_above"] == 36
    assert nested_b["n_unmarked_at_most"] == 42
    assert poshits["methods"][0]["coverage_gate"]["n_unmarked_zero"] == 33
    # Isolated lock A on the original 12 does not beat recounted hard 25/48.
    assert nested_a["n_marked_above"] < 25


def test_protocol_isolated_100x4_to_36x4_locks() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    hard = json.loads(
        (root / "2026-09-01-transfer-100x4-to-36x4-hard-last4" / "results.json").read_text()
    )
    poshits = json.loads(
        (
            root / "2026-09-01-transfer-100x4-to-36x4-opening-poshits" / "results.json"
        ).read_text()
    )
    assert hard["used_keys"] is False
    assert poshits["used_keys"] is False
    assert hard["n_train_prompts"] == 100
    assert hard["n_test_prompts"] == 36
    assert hard["methods"][0]["n_prompt_wins"] == 36
    assert poshits["methods"][0]["n_prompt_wins"] == 35
    nested_a = _transfer_threshold(hard, "interpolate", "nested-youden")
    nested_b = _transfer_threshold(poshits, "poshits", "nested-youden")
    assert nested_a["n_marked_above"] == 109
    assert nested_a["n_unmarked_at_most"] == 122
    assert nested_b["n_marked_above"] == 134
    assert nested_b["n_unmarked_at_most"] == 129
    assert poshits["methods"][0]["coverage_gate"]["n_unmarked_zero"] == 75


def test_protocol_isolated_lock_b_occupancy_free_readout() -> None:
    root = Path(__file__).resolve().parents[1] / "experiments"
    orig = json.loads(
        (
            root
            / "2026-09-01-transfer-100x4-to-12x4-opening-poshits"
            / "occupancy-free.json"
        ).read_text()
    )
    pool = json.loads(
        (
            root
            / "2026-09-01-transfer-100x4-to-36x4-opening-poshits"
            / "occupancy-free.json"
        ).read_text()
    )
    assert orig["used_keys"] is False
    assert pool["used_keys"] is False
    assert orig["postokhits_t0_marked_above"] == 16
    assert orig["postokhits_t0_unmarked_at_most"] == 48
    assert orig["occupancy_marked_tp"] == 21
    # Occupancy-free isolated recall on the original 12 does not beat 25/48.
    assert orig["postokhits_t0_marked_above"] < 25
    assert pool["postokhits_t0_marked_above"] == 114
    assert pool["postokhits_t0_unmarked_at_most"] == 139
    assert pool["occupancy_marked_tp"] == 20


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


def test_opening_snapupset_is_chance() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-fitprefix4-snaprate"
        / "snapupset"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.used_hash_iv is False
    assert ev.used_g_values is False
    assert ev.n_prompts_marked_above == 7
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert 0.45 < stats.auc < 0.55
    assert stats.permutation_p > 0.2


def test_opening_snapmiss_ranks_and_is_not_isolated() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-fitprefix4-snaprate"
        / "snapmiss"
        / "holdout.json"
    )
    leave = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-fitprefix4-snaprate"
        / "snapleave"
        / "holdout.json"
    )
    prefix = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-prefix4-snaprate"
        / "snapupset"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 10
    assert ev.n_marked_positive == 21
    assert ev.n_unmarked_nonpositive == 41
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert stats.auc > 0.65
    assert stats.permutation_p < 0.01
    # Majority leave-argmax is not a detector. Prefix-4 upset stays chance.
    assert leave.n_marked_positive == 48
    assert leave.n_unmarked_nonpositive == 7
    assert prefix.n_prompts_marked_above == 6
    prefix_auc = binary_eval(prefix.marked_lrs, prefix.unmarked_lrs, n_perm=200, seed=0)
    assert 0.45 < prefix_auc.auc < 0.55


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


def test_leftover_eight_are_officially_marked_at_prefix16() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-official-prefix-leftover"
            / "results.json"
        ).read_text()
    )
    assert raw["used_keys"] is True
    leftover = [r for r in raw["rows"] if r["side"] == "marked" and r["leftover"]]
    assert len(leftover) == 8
    means16 = [r["prefixes"]["16"]["mean"] for r in leftover]
    assert all(m > 0.55 for m in means16)
    full = [r["prefixes"]["128"]["mean"] for r in leftover]
    assert min(full) > 0.59
    other = [
        r["prefixes"]["16"]["mean"]
        for r in raw["rows"]
        if r["side"] == "marked" and not r["leftover"]
    ]
    unmarked = [
        r["prefixes"]["16"]["mean"]
        for r in raw["rows"]
        if r["side"] == "unmarked"
    ]
    assert abs(sum(means16) / 8 - sum(other) / 40) < 0.02
    assert sum(unmarked) / 48 < 0.53
    letter = [
        r
        for r in leftover
        if r["stem"] == "08-letter" and r["sample"] == 2
    ][0]
    assert letter["prefixes"]["5"]["mean"] > 0.70


def test_prefix8_backoff_rescues_four_zeros_not_letter_d2() -> None:
    ev = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-rankpath"
        / "postokbackoff"
        / "holdout.json"
    )
    p4 = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4"
        / "postokbackoff"
        / "holdout.json"
    )
    rank = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    assert ev.used_keys is False
    assert ev.n_prompts_marked_above == 10
    assert ev.n_marked_positive == 38
    assert ev.n_unmarked_nonpositive == 40
    assert p4.n_marked_positive == 34
    assert p4.n_unmarked_nonpositive == 48
    by8 = {
        (s, samp): m
        for s, samp, m in zip(ev.stems, ev._samples(), ev.marked_lrs)
    }
    assert by8[("06-station", 4)] > 0
    assert by8[("08-letter", 3)] > 0
    assert by8[("10-office", 1)] > 0
    assert by8[("10-office", 3)] > 0
    assert by8[("08-letter", 2)] <= 0
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc > 0.75
    # Prefix-8 rankpath does not beat prefix-4 rankpath isolated sign.
    assert rank.n_marked_positive == 30
    assert rank.n_unmarked_nonpositive == 35


def test_letter_d2_official_5gram_is_isolated_rank_invisible() -> None:
    import json

    raw = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-letter-d2-first-ngram"
            / "results.json"
        ).read_text()
    )
    assert raw["used_keys"] is True
    d2 = raw["letter_d2"]
    assert d2["ids5"] == [3844, 287, 262, 1218, 314]
    assert d2["pieces8"][:5] == ["Now", " in", " the", " second", " I"]
    assert d2["official_isolated_prefix5_mean"] > 0.70
    assert d2["g_last_ones"] == 22
    assert d2["g_last_equal"] is True
    assert d2["isolated_fifth"]["rank_topk"] == 41
    assert d2["isolated_fifth"]["in_topk"] is False
    assert d2["isolated_fifth"]["symbol"] == 0
    assert d2["prompt_fifth"]["rank_topk"] == 11
    assert d2["prompt_fifth"]["in_topk"] is True
    assert d2["prompt_fifth"]["symbol"] == 4
    iso_misses = [
        (r["stem"], r["sample"])
        for r in raw["leftover_marked"]
        if not r["isolated_fifth"]["in_topk"]
    ]
    assert iso_misses == [("08-letter", 2), ("08-letter", 3)]
    ferry = [
        r
        for r in raw["leftover_marked"]
        if r["stem"] == "12-ferry-queue" and r["sample"] == 4
    ][0]
    assert ferry["official_prefix5_mean"] > 0.65
    assert ferry["isolated_fifth"]["rank_topk"] == 1
    assert ferry["prompt_fifth"]["rank_topk"] == 1


def test_prefix5_rankpath_does_not_beat_prefix4_or_rescue_letter_d2() -> None:
    p5 = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-fitprefix5-rankpath"
        / "rankpath"
        / "holdout.json"
    )
    p4 = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-31-probe-12x4-fitprefix4-rankpath-isolated"
        / "rankpath"
        / "holdout.json"
    )
    fifth = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-fitprefix5-rankpath"
        / "window-3-4"
        / "rankuni"
        / "holdout.json"
    )
    assert p5.used_keys is False
    assert p5.n_prompts_marked_above == 11
    assert p5.n_marked_positive == 30
    assert p5.n_unmarked_nonpositive == 36
    assert p4.n_prompts_marked_above == 12
    assert p4.n_marked_positive == 41
    by5 = {
        (s, samp): lr
        for s, samp, lr in zip(p5.stems, p5._samples(), p5.marked_lrs)
    }
    assert by5[("08-letter", 2)] < 0
    auc5 = binary_eval(p5.marked_lrs, p5.unmarked_lrs, n_perm=200, seed=0)
    auc4 = binary_eval(p4.marked_lrs, p4.unmarked_lrs, n_perm=200, seed=0)
    assert auc5.auc < auc4.auc
    assert fifth.used_keys is False
    assert fifth.n_prompts_marked_above == 4
    fifth_auc = binary_eval(fifth.marked_lrs, fifth.unmarked_lrs, n_perm=200, seed=0)
    assert fifth_auc.auc < 0.50


def test_letter_d2_ood_backoff_is_last1_not_the_5gram() -> None:
    import json

    root = Path(__file__).resolve().parents[1] / "experiments" / "2026-09-01-letter-d2-first-ngram"
    trace = json.loads((root / "backoff-trace.json").read_text())
    bins = json.loads((root / "fifth-rank-bins.json").read_text())
    assert trace["used_keys"] is False
    d2 = trace["letter_d2"]
    assert d2["n_used"] == 2
    assert d2["lr"] < 0
    assert all(a["i"] != 4 for a in d2["atoms"])
    last1 = [a for a in d2["atoms"] if a["ctx_text"] == " in" and a["piece"] == " the"]
    assert len(last1) == 1
    assert last1[0]["c_m"] == 2
    assert last1[0]["c_u"] == 8
    assert last1[0]["delta"] < 0
    gram = d2["official_5gram"]
    assert gram["scored"] is False
    assert gram["tok"] == 314
    by_order = {row["order"]: row for row in gram["orders"]}
    assert by_order[4]["n_m"] == 0 and by_order[4]["c_m"] == 0
    assert by_order[1]["n_m"] == 6 and by_order[1]["c_m"] == 0
    assert d2["postokbackoff2"]["n_used"] == 0
    d3 = trace["letter_d3"]
    assert d3["lr"] > 0
    assert any(a["piece"] == " my" and a["delta"] > 0 for a in d3["atoms"])
    marked = bins["marked_isolated"]
    unmarked = bins["unmarked_isolated"]
    assert marked["bins"]["miss"] == 9
    assert unmarked["bins"]["miss"] == 7
    assert marked["bins_official_gt_055"]["argmax"] == 10
    assert marked["bins_official_gt_055"]["miss"] == 8


def test_prefix8_backoff_extra_tps_are_last1_not_5grams() -> None:
    import json

    orders = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-letter-d2-first-ngram"
            / "prefix8-backoff-orders.json"
        ).read_text()
    )
    b2 = holdout_from_json(
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-backoff2"
        / "postokbackoff2"
        / "holdout.json"
    )
    assert orders["used_keys"] is False
    assert orders["tp_n"] == 38
    assert orders["tp_only_last1"] == 20
    rescued = {
        (r["stem"], r["sample"]): r for r in orders["rescued_prefix4_zeros"]
    }
    assert set(rescued) == {
        ("06-station", 4),
        ("08-letter", 3),
        ("10-office", 1),
        ("10-office", 3),
    }
    assert all(r["only_last1"] for r in rescued.values())
    assert all(r["backoff2_n_used"] == 0 for r in rescued.values())
    assert orders["letter_d2"]["backoff2_n_used"] == 0
    assert b2.used_keys is False
    assert b2.n_prompts_marked_above == 12
    assert b2.n_marked_positive == 18
    assert b2.n_unmarked_nonpositive == 46
    gate = coverage_gate(b2.marked_lrs, b2.unmarked_lrs)
    assert gate.n_marked_zero == 30
    assert abs(gate.precision - 0.9) < 1e-9


def test_prefix5_hashtok_letter_d2_is_occupancy_not_observed() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtok"
    )
    hp = holdout_from_json(root / "hashpool" / "holdout.json")
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    tok = holdout_from_json(root / "postokhits" / "holdout.json")
    trace = json.loads((root / "occupancy-trace.json").read_text())
    assert hp.used_keys is False
    assert ht.used_keys is False
    assert hp.n_prompts_marked_above == 11
    assert hp.n_marked_positive == 34
    assert hp.n_unmarked_nonpositive == 34
    assert ht.n_prompts_marked_above == 9
    assert ht.n_marked_positive == 30
    assert ht.n_unmarked_nonpositive == 36
    assert tok.n_marked_positive == 30
    hp_pos = {
        (s, samp)
        for s, samp, m in zip(hp.stems, hp._samples(), hp.marked_lrs)
        if m > 0
    }
    ht_pos = {
        (s, samp)
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
        if m > 0
    }
    tok_pos = {
        (s, samp)
        for s, samp, m in zip(tok.stems, tok._samples(), tok.marked_lrs)
        if m > 0
    }
    assert ht_pos == tok_pos
    assert hp_pos - ht_pos == {
        ("01-harbour", 2),
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("08-letter", 2),
    }
    by_hp = {
        (s, samp): m
        for s, samp, m in zip(hp.stems, hp._samples(), hp.marked_lrs)
    }
    by_ht = {
        (s, samp): m
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
    }
    assert by_hp[("08-letter", 2)] > 0
    assert by_ht[("08-letter", 2)] == 0
    assert trace["used_keys"] is False
    assert trace["letter_d2"]["hashtok"]["n_used"] == 0
    fifth = trace["letter_d2"]["fifth_token"]
    assert fifth["n_hashes_seen"] == 0
    assert fifth["hashtok_delta"] is None
    assert fifth["hashpool_delta"] > 0
    assert all(row["n_hashes_seen"] == 0 for row in trace["letter_d2"]["trace"])
    assert trace["marked_tp_sets"]["hashtok_equals_postokhits"] is True


def _nested_youden(results: dict, name: str) -> tuple[int, int]:
    rows = [
        row
        for row in results["thresholds"]
        if row["name"] == name and row["source"] == "nested-youden"
    ]
    assert len(rows) == 1
    return int(rows[0]["n_marked_above"]), int(rows[0]["n_unmarked_at_most"])


def test_prefix5_hashtokbackoff_letter_d2_fifth_is_last1_unmarked() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtokbackoff"
    )
    atoms = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-letter-d2-first-ngram"
        / "hashtokbackoff-trace.json"
    )
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    hb = holdout_from_json(root / "hashtokbackoff" / "holdout.json")
    hb2 = holdout_from_json(root / "hashtokbackoff2" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    trace = json.loads((root / "backoff-order-trace.json").read_text())
    atoms_trace = json.loads(atoms.read_text())
    assert ht.used_keys is False
    assert hb.used_keys is False
    assert hb2.used_keys is False
    assert trace["used_keys"] is False
    assert atoms_trace["used_keys"] is False
    assert ht.n_marked_positive == 30
    assert ht.n_unmarked_nonpositive == 36
    assert hb.n_prompts_marked_above == 10
    assert hb.n_marked_positive == 38
    assert hb.n_unmarked_nonpositive == 35
    assert hb2.n_marked_positive == 36
    assert hb2.n_unmarked_nonpositive == 34
    # t=0 38/48 is not a calibrated detector and does not beat poshits 39/48.
    assert hb.n_marked_positive < 39
    assert hb2.n_marked_positive < 39
    nested_hb = _nested_youden(results, "hashtokbackoff")
    nested_hb2 = _nested_youden(results, "hashtokbackoff2")
    assert nested_hb == (30, 40)
    assert nested_hb2 == (30, 42)
    extras = {tuple(row) for row in trace["backoff_extras_vs_hashtok"]}
    extras2 = {tuple(row) for row in trace["backoff2_extras_vs_hashtok"]}
    assert extras == {
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("03-library", 1),
        ("03-library", 2),
        ("03-library", 3),
        ("03-library", 4),
        ("08-letter", 2),
        ("08-letter", 3),
        ("10-office", 4),
    }
    assert extras2 == extras - {("01-harbour", 3), ("01-harbour", 4)}
    d2 = trace["letter_d2"]
    assert d2["ids"] == atoms_trace["letter_d2"]["ids"] == [3844, 287, 262, 1218, 314]
    assert d2["hashtokbackoff"]["n_used"] == 3
    assert d2["hashtokbackoff2"]["n_used"] == 2
    assert d2["holdout"]["hashtok"] == 0.0
    assert d2["holdout"]["hashtokbackoff"] > 0
    assert d2["holdout"]["hashtokbackoff2"] > 0
    assert d2["holdout"]["hashtokbackoff"] < d2["holdout"]["hashtokbackoff2"]
    by_ht = {
        (s, samp): m
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
    }
    by_hb = {
        (s, samp): m
        for s, samp, m in zip(hb.stems, hb._samples(), hb.marked_lrs)
    }
    by_hb2 = {
        (s, samp): m
        for s, samp, m in zip(hb2.stems, hb2._samples(), hb2.marked_lrs)
    }
    assert by_ht[("08-letter", 2)] == 0
    assert abs(by_hb[("08-letter", 2)] - d2["holdout"]["hashtokbackoff"]) < 1e-9
    assert abs(by_hb2[("08-letter", 2)] - d2["holdout"]["hashtokbackoff2"]) < 1e-9
    first, second, third, fifth = d2["trace"]
    # i=1 "order 3" hashes a 1-token prefix into the order-3 table, not a 3-gram.
    assert first["i"] == 1
    assert first["order"] == 3
    assert first["piece"] == " in"
    assert second["i"] == 2
    assert second["order"] == 4
    assert third["i"] == 3
    assert third["order"] is None
    assert fifth["i"] == 4
    assert fifth["piece"] == " I"
    assert fifth["order"] == 1
    assert fifth["delta"] < 0
    assert d2["fifth_order"] == 1
    by_order = {row["order"]: row for row in fifth["tried"]}
    assert by_order[4]["n_hashes_seen"] == 0
    assert by_order[3]["n_hashes_seen"] == 0
    assert by_order[2]["n_hashes_seen"] == 0
    assert by_order[1]["n_hashes_seen"] == 2
    assert by_order[1]["c_m"] == 0
    assert by_order[1]["c_u"] == 2
    library = [
        row
        for row in trace["traced_files"]
        if row["stem"] == "03-library" and row["in_backoff2_extras"]
    ]
    assert len(library) == 4
    assert all(row["orders"] == [4] for row in library)
    for row in library:
        hits = [p for p in row["positions"] if p["order"] is not None]
        assert hits
        assert all(p["order"] > p["i"] for p in hits)
    d3 = next(
        row
        for row in trace["traced_files"]
        if row["stem"] == "08-letter" and row["sample"] == 3
    )
    d3_hits = [p for p in d3["positions"] if p["order"] is not None]
    assert d3_hits
    assert all(p["order"] > p["i"] for p in d3_hits)


def test_prefix4_hashtok_beats_hashed_backoff_on_opening() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtokbackoff"
    )
    hp = holdout_from_json(root / "hashpool" / "holdout.json")
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    hb = holdout_from_json(root / "hashtokbackoff" / "holdout.json")
    hb2 = holdout_from_json(root / "hashtokbackoff2" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    assert hp.used_keys is False
    assert ht.used_keys is False
    assert hb.used_keys is False
    assert results["fit_prefix"] == 4
    assert hp.n_prompts_marked_above == 10
    assert hp.n_marked_positive == 38
    assert hp.n_unmarked_nonpositive == 37
    assert ht.n_prompts_marked_above == 10
    assert ht.n_marked_positive == 35
    assert ht.n_unmarked_nonpositive == 39
    assert hb.n_prompts_marked_above == 10
    assert hb.n_marked_positive == 31
    assert hb.n_unmarked_nonpositive == 33
    assert hb2.n_marked_positive == 31
    assert hb2.n_unmarked_nonpositive == 33
    assert hb.n_marked_positive < ht.n_marked_positive
    assert ht.n_marked_positive < hp.n_marked_positive
    assert hp.n_marked_positive < 39
    assert ht.n_marked_positive < 39
    assert _nested_youden(results, "hashtok") == (33, 45)
    assert _nested_youden(results, "hashtokbackoff") == (31, 42)
    assert _nested_youden(results, "hashpool") == (35, 46)


def test_prefix5_hashtoklen_drops_short_prefix_collisions() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen"
    )
    atoms = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-letter-d2-first-ngram"
        / "hashtoklen-trace.json"
    )
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    hl = holdout_from_json(root / "hashtoklen" / "holdout.json")
    hb = holdout_from_json(root / "hashtoklenbackoff" / "holdout.json")
    hb2 = holdout_from_json(root / "hashtoklenbackoff2" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    trace = json.loads((root / "exact-order-trace.json").read_text())
    atoms_trace = json.loads(atoms.read_text())
    assert ht.used_keys is False
    assert hl.used_keys is False
    assert hb.used_keys is False
    assert trace["exact_len"] is True
    assert atoms_trace["exact_len"] is True
    assert ht.n_marked_positive == 30
    assert hl.n_prompts_marked_above == 12
    assert hl.n_marked_positive == 21
    assert hl.n_unmarked_nonpositive == 45
    assert hb.n_prompts_marked_above == 11
    assert hb.n_marked_positive == 36
    assert hb.n_unmarked_nonpositive == 34
    assert hb2.n_marked_positive == 36
    assert hb2.n_unmarked_nonpositive == 35
    assert hl.n_marked_positive < ht.n_marked_positive
    assert hb.n_marked_positive < 39
    assert _nested_youden(results, "hashtoklen") == (21, 45)
    assert _nested_youden(results, "hashtoklenbackoff") == (33, 42)
    assert _nested_youden(results, "hashtoklenbackoff2") == (28, 43)
    ht_pos = {
        (s, samp)
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
        if m > 0
    }
    hb_pos = {
        (s, samp)
        for s, samp, m in zip(hb.stems, hb._samples(), hb.marked_lrs)
        if m > 0
    }
    hb2_pos = {
        (s, samp)
        for s, samp, m in zip(hb2.stems, hb2._samples(), hb2.marked_lrs)
        if m > 0
    }
    extras = hb_pos - ht_pos
    assert extras == {
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("03-library", 1),
        ("03-library", 2),
        ("03-library", 3),
        ("03-library", 4),
        ("10-office", 4),
    }
    assert ("08-letter", 2) not in extras
    assert ("08-letter", 3) not in extras
    assert ("08-letter", 2) in hb2_pos
    by_hl = {
        (s, samp): m
        for s, samp, m in zip(hl.stems, hl._samples(), hl.marked_lrs)
    }
    by_hb = {
        (s, samp): m
        for s, samp, m in zip(hb.stems, hb._samples(), hb.marked_lrs)
    }
    by_hb2 = {
        (s, samp): m
        for s, samp, m in zip(hb2.stems, hb2._samples(), hb2.marked_lrs)
    }
    assert by_hl[("08-letter", 2)] == 0
    assert by_hb[("08-letter", 2)] < 0
    assert by_hb2[("08-letter", 2)] > 0
    d2 = atoms_trace["letter_d2"]
    assert d2["ids"] == [3844, 287, 262, 1218, 314]
    assert d2["hashtoklen"]["n_used"] == 0
    assert d2["hashtoklenbackoff2"]["n_used"] == 1
    wins = d2["winning"]
    assert all(order <= i for i, order, _piece, _delta in wins)
    assert wins[0][0] == 2 and wins[0][1] == 2 and wins[0][2] == " the"
    assert wins[1][0] == 4 and wins[1][1] == 1 and wins[1][2] == " I"
    assert wins[1][3] < 0
    lib = atoms_trace["library_d1"]
    assert lib["winning"][0][0] == 3
    assert lib["winning"][0][1] == 3
    assert lib["winning"][0][2] == " the"
    for row in d2["trace"]:
        if row["order"] is None:
            continue
        tried = {t["order"]: t for t in row["tried"]}
        assert tried[row["order"]]["exact_ok"] is True
        assert tried[row["order"]]["ctx_len"] == row["order"]


def test_prefix5_hashtoklen_recovers_one_postokhits_miss_by_collision() -> None:
    """Official-grain hashing is not a denser last-4 table.

    20 of 21 hashtoklen TPs are exact postokhits. Harbour d2 is the
    unique occupancy-free collision: exact last-4 of `The ferry was over`
    → `,` is unmarked-like; hashed last-4 of the comma is marked-like.
    Letter d2's official 5-gram still abstains. Do not sell 21/48.
    """
    import json

    p5 = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen"
    )
    p5h = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtok"
    )
    hl = holdout_from_json(p5 / "hashtoklen" / "holdout.json")
    ph = holdout_from_json(p5h / "postokhits" / "holdout.json")
    ht = holdout_from_json(p5 / "hashtok" / "holdout.json")
    hl_pos = {
        (s, samp)
        for s, samp, m in zip(hl.stems, hl._samples(), hl.marked_lrs)
        if m > 0
    }
    ph_pos = {
        (s, samp)
        for s, samp, m in zip(ph.stems, ph._samples(), ph.marked_lrs)
        if m > 0
    }
    ht_pos = {
        (s, samp)
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
        if m > 0
    }
    assert hl.n_marked_positive == 21
    assert ph.n_marked_positive == 30
    assert hl_pos - ph_pos == {("01-harbour", 2)}
    assert ht_pos == ph_pos
    by_hl = {
        (s, samp): m
        for s, samp, m in zip(hl.stems, hl._samples(), hl.marked_lrs)
    }
    by_ph = {
        (s, samp): m
        for s, samp, m in zip(ph.stems, ph._samples(), ph.marked_lrs)
    }
    assert by_hl[("01-harbour", 2)] > 0
    assert by_ph[("01-harbour", 2)] < 0
    assert by_hl[("08-letter", 2)] == 0
    atoms = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-letter-d2-first-ngram"
            / "harbour-d2-hashtoklen-trace.json"
        ).read_text()
    )
    assert atoms["used_keys"] is False
    assert atoms["exact_len"] is True
    assert atoms["ids"] == [464, 26450, 373, 625, 11]
    assert atoms["pieces"] == ["The", " ferry", " was", " over", ","]
    assert atoms["postokhits"]["lr"] < 0
    assert atoms["postokhits"]["n_used"] == 1
    assert atoms["hashtoklen"]["n_used"] == 1
    assert atoms["hashtoklen"]["lr"] == by_hl[("01-harbour", 2)]
    slot = atoms["official_slot"]
    assert slot["i"] == 4
    assert slot["tok"] == 11
    assert slot["n_hashes_seen"] == 1
    assert slot["c_m"] == 11
    assert slot["c_u"] == 0
    cas = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen-cascade-rankpath"
            / "results.json"
        ).read_text()
    )
    assert cas["used_keys"] is False
    assert cas["count_method"] == "hashtoklen"
    assert cas["coverage"]["combined_marked_above_zero"] == 33
    assert cas["coverage"]["combined_unmarked_at_most_zero"] == 37
    assert cas["coverage"]["combined_marked_above_zero"] < 39
    assert cas["positive"]["combined_marked_above_zero"] == 33


def test_prefix4_hashtoklen_never_fires_on_a_four_token_prefix() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix4-hashtoklen"
    )
    hl = holdout_from_json(root / "hashtoklen" / "holdout.json")
    hb = holdout_from_json(root / "hashtoklenbackoff" / "holdout.json")
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    assert hl.used_keys is False
    assert hl.n_marked_positive == 0
    assert hl.n_unmarked_nonpositive == 48
    assert hl.n_prompts_marked_above == 12
    hl_bin = next(m for m in results["methods"] if m["name"] == "hashtoklen")["binary"]
    ht_bin = next(m for m in results["methods"] if m["name"] == "hashtok")["binary"]
    assert hl_bin["auc"] == 0.5
    assert hl_bin["permutation_p"] == 1.0
    assert hb.n_marked_positive == 35
    assert hb.n_unmarked_nonpositive == 38
    assert ht.n_marked_positive == 35
    assert ht_bin["auc"] > 0.80
    assert _nested_youden(results, "hashtoklen") == (0, 48)
    assert _nested_youden(results, "hashtoklenbackoff") == (35, 40)
    assert _nested_youden(results, "hashtok") == (33, 45)


def test_in_domain_gpt2_prefix5_hashtoklen_is_seven_of_forty_eight() -> None:
    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-fitprefix5-hashtoklen"
    )
    hl = holdout_from_json(root / "hashtoklen" / "holdout.json")
    assert hl.used_keys is False
    assert hl.n_marked_positive == 7
    assert hl.n_unmarked_nonpositive == 48
    letter = [
        m
        for s, samp, m in zip(hl.stems, hl._samples(), hl.marked_lrs)
        if s == "08-letter" and samp == 2
    ]
    harbour = [
        m
        for s, samp, m in zip(hl.stems, hl._samples(), hl.marked_lrs)
        if s == "01-harbour" and samp == 2
    ]
    assert letter[0] == 0
    assert harbour[0] > 0


def test_in_domain_distil_prefix5_hashtoklen_is_seven_of_forty_eight() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-distilgpt2-12x4-fitprefix5-hashtoklen"
    )
    hl = holdout_from_json(root / "hashtoklen" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    assert hl.used_keys is False
    assert hl.n_marked_positive == 7
    assert hl.n_unmarked_nonpositive == 48
    hl_bin = next(m for m in results["methods"] if m["name"] == "hashtoklen")["binary"]
    assert hl_bin["auc"] > 0.56
    assert hl_bin["permutation_p"] < 0.03


def test_sixty_stem_hashtoklen_does_not_become_a_distil_detector() -> None:
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-distil-prefix5-hashtoklen"
    )
    hl = holdout_from_json(root / "hashtoklen" / "holdout.json")
    hb = holdout_from_json(root / "hashtoklenbackoff" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    assert hl.used_keys is False
    assert hl.n_marked_positive == 10
    assert hl.n_unmarked_nonpositive == 43
    hl_bin = next(m for m in results["methods"] if m["name"] == "hashtoklen")["binary"]
    hb_bin = next(
        m for m in results["methods"] if m["name"] == "hashtoklenbackoff"
    )["binary"]
    assert abs(hl_bin["auc"] - 0.571) < 0.002
    assert hl_bin["permutation_p"] < 0.05
    assert hb_bin["auc"] < 0.50
    assert hb_bin["permutation_p"] > 0.70
    assert _nested_youden(results, "hashtoklen") == (10, 43)


def test_prefix5_hashskip_is_denser_at_zero_and_worse_nested() -> None:
    """Drop-one skip-grams are not a leftover rescue.

    t=0 25/48 spends 13 unmarked FPs. Nested Youden 16/48 vs 41/48.
    Letter d2's official I is seen unmarked-only. Do not sell 25/48.
    """
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashskip"
    )
    hl = holdout_from_json(root / "hashtoklen" / "holdout.json")
    hs = holdout_from_json(root / "hashskip" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    tables = json.loads((root / "tables-hashskip" / "tables.json").read_text())
    atoms = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-letter-d2-first-ngram"
            / "letter-d2-hashskip-trace.json"
        ).read_text()
    )
    assert hl.used_keys is False
    assert hs.used_keys is False
    assert tables["drop_one"] is True
    assert tables["exact_len"] is True
    assert tables["used_keys"] is False
    assert hs.n_prompts_marked_above == 8
    assert hs.n_marked_positive == 25
    assert hs.n_unmarked_nonpositive == 35
    assert hl.n_marked_positive == 21
    assert hs.n_marked_positive < 39
    assert _nested_youden(results, "hashskip") == (16, 41)
    assert _nested_youden(results, "hashtoklen") == (21, 45)
    hl_pos = {
        (s, samp)
        for s, samp, m in zip(hl.stems, hl._samples(), hl.marked_lrs)
        if m > 0
    }
    hs_pos = {
        (s, samp)
        for s, samp, m in zip(hs.stems, hs._samples(), hs.marked_lrs)
        if m > 0
    }
    assert hs_pos - hl_pos == {
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("02-night-bus", 2),
        ("02-night-bus", 4),
        ("09-workshop", 4),
    }
    by_hs = {
        (s, samp): m
        for s, samp, m in zip(hs.stems, hs._samples(), hs.marked_lrs)
    }
    leftover = {
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("06-station", 4),
        ("08-letter", 2),
        ("08-letter", 3),
        ("10-office", 1),
        ("10-office", 3),
        ("12-ferry-queue", 4),
    }
    leftover_tp = {k for k in leftover if by_hs[k] > 0}
    assert leftover_tp == {("01-harbour", 3), ("01-harbour", 4)}
    assert by_hs[("08-letter", 2)] < 0
    assert atoms["used_keys"] is False
    assert atoms["drop_one"] is True
    assert atoms["ids"] == [3844, 287, 262, 1218, 314]
    assert atoms["hashskip"]["n_used"] == 1
    assert atoms["hashskip"]["lr"] == by_hs[("08-letter", 2)]
    views = {v["drop_i"]: v for v in atoms["official_slot"]["skip_views"]}
    assert views[2]["c_m"] == 0 and views[2]["c_u"] == 1
    assert views[3]["c_m"] == 0 and views[3]["c_u"] == 1
    assert views[2]["delta"] < 0
    assert views[3]["delta"] < 0


def test_prefix5_hashtoklen2_is_the_robust_collision_core() -> None:
    """11 of 21 hashtoklen TPs are singleton hash collisions.

    min_count=2 is 10/48 vs 48/48, nested matching t=0, precision 1.0.
    Harbour d2 survives (c_m=11). Letter d2 still abstains. Do not sell 10/48.
    """
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2"
    )
    hl = holdout_from_json(root / "hashtoklen" / "holdout.json")
    hl2 = holdout_from_json(root / "hashtoklen2" / "holdout.json")
    hs = holdout_from_json(root / "hashskip" / "holdout.json")
    hs2 = holdout_from_json(root / "hashskip2" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    tables = json.loads((root / "tables-hashtoklen" / "tables.json").read_text())
    skip_tables = json.loads((root / "tables-hashskip" / "tables.json").read_text())
    assert not (root / "tables-hashpool").exists()
    assert hl.used_keys is False
    assert hl2.used_keys is False
    assert hs2.used_keys is False
    assert hl2.instance == "key-free-hashtoklen2"
    assert hs2.instance == "key-free-hashskip2"
    assert tables["exact_len"] is True
    assert tables["drop_one"] is False
    assert tables["used_keys"] is False
    assert skip_tables["drop_one"] is True
    assert hl.n_marked_positive == 21
    assert hl.n_unmarked_nonpositive == 45
    assert hl2.n_marked_positive == 10
    assert hl2.n_unmarked_nonpositive == 48
    assert hl2.n_marked_positive < 21
    assert hl2.n_marked_positive < 29
    assert hs2.n_marked_positive == 22
    assert hs2.n_unmarked_nonpositive == 39
    assert _nested_youden(results, "hashtoklen") == (21, 45)
    assert _nested_youden(results, "hashtoklen2") == (10, 48)
    assert _nested_youden(results, "hashskip") == (16, 41)
    assert _nested_youden(results, "hashskip2") == (15, 41)
    hl_pos = {
        (s, samp)
        for s, samp, m in zip(hl.stems, hl._samples(), hl.marked_lrs)
        if m > 0
    }
    hl2_pos = {
        (s, samp)
        for s, samp, m in zip(hl2.stems, hl2._samples(), hl2.marked_lrs)
        if m > 0
    }
    assert hl2_pos == {
        ("01-harbour", 2),
        ("05-kitchen", 1),
        ("05-kitchen", 3),
        ("07-rain", 1),
        ("07-rain", 4),
        ("08-letter", 1),
        ("08-letter", 4),
        ("09-workshop", 1),
        ("09-workshop", 2),
        ("09-workshop", 3),
    }
    assert hl_pos - hl2_pos == {
        ("02-night-bus", 3),
        ("04-market", 1),
        ("04-market", 2),
        ("04-market", 3),
        ("04-market", 4),
        ("05-kitchen", 2),
        ("06-station", 1),
        ("06-station", 3),
        ("07-rain", 2),
        ("11-garden", 1),
        ("11-garden", 4),
    }
    by_hl = {
        (s, samp): m
        for s, samp, m in zip(hl.stems, hl._samples(), hl.marked_lrs)
    }
    by_hl2 = {
        (s, samp): m
        for s, samp, m in zip(hl2.stems, hl2._samples(), hl2.marked_lrs)
    }
    by_hs = {
        (s, samp): m
        for s, samp, m in zip(hs.stems, hs._samples(), hs.marked_lrs)
    }
    by_hs2 = {
        (s, samp): m
        for s, samp, m in zip(hs2.stems, hs2._samples(), hs2.marked_lrs)
    }
    leftover = {
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("06-station", 4),
        ("08-letter", 2),
        ("08-letter", 3),
        ("10-office", 1),
        ("10-office", 3),
        ("12-ferry-queue", 4),
    }
    assert by_hl[("01-harbour", 2)] == by_hl2[("01-harbour", 2)]
    assert by_hl2[("01-harbour", 2)] > 0
    assert by_hl2[("08-letter", 2)] == 0.0
    assert all(by_hl2[k] == 0.0 for k in leftover)
    leftover_hs2 = {k for k in leftover if by_hs2[k] > 0}
    assert leftover_hs2 == {("01-harbour", 3), ("01-harbour", 4)}
    assert by_hs[("08-letter", 2)] < 0
    assert by_hs2[("08-letter", 2)] == 0.0
    hs2_nested_t = next(
        row["train_youden"]
        for row in results["thresholds"]
        if row["name"] == "hashskip2" and row["source"] == "nested-youden"
    )
    leftover_hs2_nested = {k for k in leftover if by_hs2[k] > hs2_nested_t}
    assert leftover_hs2_nested == set()


def test_prefix5_hashmask_is_not_a_nested_leftover_rescue() -> None:
    """MASK replace is denser coverage and worse nested than hashtoklen.

    t=0 21/48 vs 42/48 spends 6 unmarked FPs. Nested Youden 19/48 vs 45/48.
    Letter d2's file LR is the official slot: two opposing singletons.
    Do not sell 21/48 or 19/48.
    """
    import json

    from text_watermark_tools.transfer import HASH_CASCADE_READERS, MASK_TAG

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashmask"
    )
    hl = holdout_from_json(root / "hashtoklen" / "holdout.json")
    hm = holdout_from_json(root / "hashmask" / "holdout.json")
    hm2 = holdout_from_json(root / "hashmask2" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    tables = json.loads((root / "tables-hashmask" / "tables.json").read_text())
    atoms = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-letter-d2-first-ngram"
            / "letter-d2-hashmask-trace.json"
        ).read_text()
    )
    assert hl.used_keys is False
    assert hm.used_keys is False
    assert hm2.used_keys is False
    assert tables["mask_one"] is True
    assert tables["drop_one"] is False
    assert tables["exact_len"] is True
    assert tables["used_keys"] is False
    assert hm.instance == "key-free-hashmask"
    assert hm2.instance == "key-free-hashmask2"
    assert hm.n_prompts_marked_above == 11
    assert hm.n_marked_positive == 21
    assert hm.n_unmarked_nonpositive == 42
    assert hl.n_marked_positive == 21
    assert hm.n_marked_positive < 39
    assert hm2.n_marked_positive == 15
    assert hm2.n_unmarked_nonpositive == 44
    assert _nested_youden(results, "hashtoklen") == (21, 45)
    assert _nested_youden(results, "hashmask") == (19, 45)
    assert _nested_youden(results, "hashmask2") == (11, 45)
    assert "hashmask" not in HASH_CASCADE_READERS
    hl_pos = {
        (s, samp)
        for s, samp, m in zip(hl.stems, hl._samples(), hl.marked_lrs)
        if m > 0
    }
    hm_pos = {
        (s, samp)
        for s, samp, m in zip(hm.stems, hm._samples(), hm.marked_lrs)
        if m > 0
    }
    assert hm_pos - hl_pos == {
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("08-letter", 2),
        ("09-workshop", 4),
    }
    assert hl_pos - hm_pos == {
        ("04-market", 1),
        ("04-market", 2),
        ("04-market", 3),
        ("04-market", 4),
    }
    by_hm = {
        (s, samp): m
        for s, samp, m in zip(hm.stems, hm._samples(), hm.marked_lrs)
    }
    by_hm2 = {
        (s, samp): m
        for s, samp, m in zip(hm2.stems, hm2._samples(), hm2.marked_lrs)
    }
    leftover = {
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("06-station", 4),
        ("08-letter", 2),
        ("08-letter", 3),
        ("10-office", 1),
        ("10-office", 3),
        ("12-ferry-queue", 4),
    }
    leftover_tp = {k for k in leftover if by_hm[k] > 0}
    assert leftover_tp == {
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("08-letter", 2),
    }
    assert by_hm[("08-letter", 2)] > 0
    hm_nested_t = next(
        row["train_youden"]
        for row in results["thresholds"]
        if row["name"] == "hashmask" and row["source"] == "nested-youden"
    )
    leftover_nested = {k for k in leftover if by_hm[k] > hm_nested_t}
    assert leftover_nested == {("01-harbour", 3), ("01-harbour", 4)}
    assert by_hm[("08-letter", 2)] < hm_nested_t
    leftover_hm2 = {k for k in leftover if by_hm2[k] > 0}
    assert leftover_hm2 == set()
    assert atoms["used_keys"] is False
    assert atoms["mask_one"] is True
    assert atoms["drop_one"] is False
    assert atoms["mask_tag"] == MASK_TAG
    assert atoms["ids"] == [3844, 287, 262, 1218, 314]
    assert atoms["hashmask"]["n_used"] == 1
    assert atoms["hashmask"]["lr"] == by_hm[("08-letter", 2)]
    assert atoms["holdout_lr"] == by_hm[("08-letter", 2)]
    assert atoms["hashmask2"]["n_used"] == 0
    slot = atoms["official_slot"]
    assert slot["i"] == 4
    assert slot["tok"] == 314
    assert slot["delta"] == by_hm[("08-letter", 2)]
    views = {v["mask_i"]: v for v in slot["mask_views"]}
    assert views[0]["n_hashes_seen"] == 0
    assert views[1]["n_hashes_seen"] == 0
    assert views[2]["n_hashes_seen"] == 0
    assert views[3]["n_hashes_seen"] == 2
    assert views[3]["c_m"] == 1 and views[3]["c_u"] == 1
    hashes = {(h["c_m"], h["c_u"]) for h in views[3]["hashes"]}
    assert hashes == {(1, 0), (0, 1)}


def test_prefix5_hashtoklen2_rankpath_cascade_copies_rankpath() -> None:
    """Robust 5-gram TPs are already prefix-4 rankpath TPs.

    Coverage cascade 28/48 vs 40/48. Leftover fill-in 0/8. Do not sell 28/48.
    """
    import json

    from text_watermark_tools.transfer import HASH_CASCADE_READERS

    cas = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2-cascade-rankpath"
            / "cascade.json"
        ).read_text()
    )
    assert cas["used_keys"] is False
    assert cas["count_method"] == "hashtoklen2"
    assert cas["fallback"] == "rankpath"
    assert cas["combined_marked_above_zero"] == 28
    assert cas["combined_unmarked_at_most_zero"] == 40
    assert cas["count_marked_above_zero"] == 10
    assert cas["count_unmarked_at_most_zero"] == 0
    assert cas["fallback_marked_above_zero"] == 18
    assert cas["combined_marked_above_zero"] < 39
    assert cas["leftover_marked_above_zero"] == 0
    assert cas["leftover_tps"] == []
    assert cas["hashtoklen2_tps_subset_of_rankpath"] is True
    assert "hashtoklen2" not in HASH_CASCADE_READERS
    leftover = {
        ("01-harbour", 3),
        ("01-harbour", 4),
        ("06-station", 4),
        ("08-letter", 2),
        ("08-letter", 3),
        ("10-office", 1),
        ("10-office", 3),
        ("12-ferry-queue", 4),
    }
    leftover_tp = {
        (row["stem"], row["sample"])
        for row in cas["rows"]
        if row["side"] == "marked"
        and (row["stem"], row["sample"]) in leftover
        and row["score"] > 0
    }
    assert leftover_tp == set()
    hl2 = {
        (row["stem"], row["sample"])
        for row in cas["rows"]
        if row["side"] == "marked" and row["count_lr"] > 0
    }
    rank = {
        (row["stem"], row["sample"])
        for row in cas["rows"]
        if row["side"] == "marked" and row["pivot_lr"] > 0
    }
    assert len(hl2) == 10
    assert len(rank) == 28
    assert hl2 <= rank


def test_prefix5_hashtoklen_count_weighting_copies_uniform() -> None:
    """Weighting hashes by count does not flip signs at official 5-gram grain.

    No file mixes a singleton with a dense hash. Rain d1 mixes n=7 with
    n=8; that does not change 21/48 vs 45/48. excess n-1 copies min_count=2.
    Not a product scorer.
    """
    import math

    from text_watermark_tools.blind import clip_twins_prefix, load_twins
    from text_watermark_tools.transfer import (
        _dirichlet_logp,
        _hash_bucket_tok_count,
        _scored_ctx,
        hash_context,
        hash_ctx_len,
        load_hashpool,
        score_hashtok,
        score_hashtok_detail,
    )

    tables = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2"
        / "tables-hashtoklen"
    )
    hold_root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen2"
    )
    hl = holdout_from_json(hold_root / "hashtoklen" / "holdout.json")
    hl2 = holdout_from_json(hold_root / "hashtoklen2" / "holdout.json")
    model = load_hashpool(tables)
    assert model.used_keys is False
    assert model.exact_len is True
    assert model.drop_one is False
    twins = clip_twins_prefix(
        load_twins(
            Path(__file__).resolve().parents[1]
            / "experiments"
            / "2026-08-17-pair-12x4"
        ),
        5,
    )

    def weighted(ids: list[int], scheme: str) -> float:
        v = max(len(model.vocab), 2)
        pos: list[float] = []
        for i, tok in enumerate(ids):
            if i == 0:
                continue
            ctx = _scored_ctx(ids, i, model.context_len, model.position_bucket)
            if hash_ctx_len(ctx, model.position_bucket) != int(model.context_len):
                continue
            pieces: list[tuple[int, float]] = []
            t = int(tok)
            for h, seed in enumerate(model.seeds):
                bucket = hash_context(ctx, seed) % model.n_buckets
                c_m = _hash_bucket_tok_count(model.marked[h], bucket, t)
                c_u = _hash_bucket_tok_count(model.unmarked[h], bucket, t)
                n = c_m + c_u
                if n < 1:
                    continue
                lr = _dirichlet_logp(
                    model.marked[h].get(bucket),
                    t,
                    fallback=model.marked_unigram,
                    n_fallback=model.n_marked,
                    alpha=model.alpha,
                    v=v,
                ) - _dirichlet_logp(
                    model.unmarked[h].get(bucket),
                    t,
                    fallback=model.unmarked_unigram,
                    n_fallback=model.n_unmarked,
                    alpha=model.alpha,
                    v=v,
                )
                pieces.append((n, lr))
            if not pieces:
                continue
            ns = {n for n, _ in pieces}
            if 1 in ns and any(n >= 2 for n in ns):
                mixed_singleton_dense.append((ids, ns))
            if scheme == "uniform":
                pos.append(sum(p for _, p in pieces) / len(pieces))
            elif scheme == "count":
                w = sum(n for n, _ in pieces)
                pos.append(sum(n * p for n, p in pieces) / w)
            elif scheme == "log":
                w = sum(math.log(1 + n) for n, _ in pieces)
                pos.append(sum(math.log(1 + n) * p for n, p in pieces) / w)
            elif scheme == "excess":
                kept = [(n - 1, p) for n, p in pieces if n >= 2]
                if not kept:
                    continue
                w = sum(n for n, _ in kept)
                pos.append(sum(n * p for n, p in kept) / w)
            else:
                raise ValueError(scheme)
        if not pos:
            return 0.0
        return pos[0] if len(pos) == 1 else sum(pos) / len(pos)

    mixed_singleton_dense: list = []
    marked_uniform = []
    unmarked_uniform = []
    count_sign_flips = 0
    log_sign_flips = 0
    for twin in twins:
        for seq in twin.marked_seqs():
            u = weighted(seq, "uniform")
            c = weighted(seq, "count")
            lg = weighted(seq, "log")
            assert abs(u - score_hashtok(seq, model)) < 1e-12
            if (u > 0) != (c > 0):
                count_sign_flips += 1
            if (u > 0) != (lg > 0):
                log_sign_flips += 1
            marked_uniform.append(u)
        for seq in twin.unmarked_seqs():
            u = weighted(seq, "uniform")
            c = weighted(seq, "count")
            lg = weighted(seq, "log")
            assert abs(u - score_hashtok(seq, model)) < 1e-12
            if (u > 0) != (c > 0):
                count_sign_flips += 1
            if (u > 0) != (lg > 0):
                log_sign_flips += 1
            unmarked_uniform.append(u)
    assert mixed_singleton_dense == []
    assert count_sign_flips == 0
    assert log_sign_flips == 0
    assert sum(x > 0 for x in marked_uniform) == hl.n_marked_positive == 21
    assert sum(x <= 0 for x in unmarked_uniform) == hl.n_unmarked_nonpositive == 45
    marked_ex = [
        weighted(seq, "excess") for twin in twins for seq in twin.marked_seqs()
    ]
    unmarked_ex = [
        weighted(seq, "excess") for twin in twins for seq in twin.unmarked_seqs()
    ]
    assert sum(x > 0 for x in marked_ex) == hl2.n_marked_positive == 10
    assert sum(x <= 0 for x in unmarked_ex) == hl2.n_unmarked_nonpositive == 48
    harbour = next(t for t in twins if t.stem == "01-harbour")
    assert abs(
        score_hashtok_detail(harbour.marked_seqs()[1], model).lr
        - score_hashtok_detail(harbour.marked_seqs()[1], model, min_count=2).lr
    ) < 1e-12


def test_in_domain_full_file_hashtok_is_denser_and_noisier() -> None:
    """Occupancy-free full-file hashing is 33/48 vs 22/48.

    Hashpool stays 35/48 vs 29/48. Nested-by-stem hashtok 22/48 vs 30/48
    is worse spec than hits 22/48 vs 39/48. Letter d2 stays negative.
    Do not sell 33/48 as replacing 29/48.
    """
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-hashtok"
    )
    hp = holdout_from_json(root / "hashpool" / "holdout.json")
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    hl = holdout_from_json(root / "hashtoklen" / "holdout.json")
    hits = holdout_from_json(root / "hits" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    assert results["used_keys"] is False
    assert hp.used_keys is False
    assert ht.used_keys is False
    assert hp.instance == "key-free-hashpool"
    assert ht.instance == "key-free-hashtok"
    assert hp.n_marked_positive == 35
    assert hp.n_unmarked_nonpositive == 29
    assert ht.n_marked_positive == 33
    assert ht.n_unmarked_nonpositive == 22
    assert hl.n_marked_positive == 33
    assert hl.n_unmarked_nonpositive == 23
    assert ht.n_prompts_marked_above == 9
    assert hl.n_prompts_marked_above == 8
    assert ht.n_marked_positive < 39
    assert hits.n_marked_positive == 28

    def nested_stem(name: str) -> tuple[int, int]:
        method = next(m for m in results["methods"] if m["name"] == name)
        row = method["nested_stem"]["nested-youden-by-stem"]
        return int(row["n_marked_above"]), int(row["n_unmarked_at_most"])

    assert nested_stem("hits") == (22, 39)
    assert nested_stem("hashpool") == (23, 36)
    assert nested_stem("hashtok") == (22, 30)
    hp_pos = {
        (s, samp)
        for s, samp, m in zip(hp.stems, hp._samples(), hp.marked_lrs)
        if m > 0
    }
    ht_pos = {
        (s, samp)
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
        if m > 0
    }
    assert hp_pos - ht_pos == {
        ("02-night-bus", 3),
        ("03-library", 2),
        ("04-market", 1),
        ("12-ferry-queue", 4),
    }
    assert ht_pos - hp_pos == {("02-night-bus", 4), ("04-market", 3)}
    by_ht = {
        (s, samp): m
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
    }
    by_hp = {
        (s, samp): m
        for s, samp, m in zip(hp.stems, hp._samples(), hp.marked_lrs)
    }
    assert by_ht[("08-letter", 2)] < 0
    assert by_hp[("08-letter", 2)] < 0


def test_in_domain_hashtok_or_indicate_is_not_a_detector() -> None:
    """OR at t=0 is 39/48 vs 12/48; combined 51/96 worse than indicate.

    Complementary TPs exist. Honest nested LDA/max throw them away.
    Do not sell 39/48 as beating poshits 39/48 or replacing 29/48.
    """
    import json

    from text_watermark_tools.stats import nested_threshold_by_stem

    indicate = holdout_from_json(HOLD)
    probe = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-hashtok"
    )
    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-hashtok-indicate-or"
    )
    hashtok = holdout_from_json(probe / "hashtok" / "holdout.json")
    hits = holdout_from_json(probe / "hits" / "holdout.json")
    postokhits = holdout_from_json(probe / "postokhits" / "holdout.json")
    raw = json.loads((root / "complement.json").read_text())
    stacked = rotate_score_stack([indicate, hashtok], model_name="gpt2")
    saved_stack = holdout_from_json(root / "lda-stack" / "holdout.json")

    assert raw["used_keys"] is False
    assert indicate.used_keys is False
    assert hashtok.used_keys is False
    assert stacked.used_keys is False
    assert indicate.instance == "key-free-counts"
    assert hashtok.instance == "key-free-hashtok"
    assert list(zip(indicate.stems, indicate._samples())) == list(
        zip(hashtok.stems, hashtok._samples())
    )
    assert indicate.n_marked_positive == 29
    assert indicate.n_unmarked_nonpositive == 23
    assert hashtok.n_marked_positive == 33
    or_m = sum(
        a > 0 or b > 0
        for a, b in zip(indicate.marked_lrs, hashtok.marked_lrs, strict=True)
    )
    or_u = sum(
        not (a > 0 or b > 0)
        for a, b in zip(indicate.unmarked_lrs, hashtok.unmarked_lrs, strict=True)
    )
    assert or_m == 39
    assert or_u == 12
    assert or_m + or_u == 51
    assert or_m + or_u < indicate.n_marked_positive + indicate.n_unmarked_nonpositive
    assert raw["headline"]["or_indicate_hashtok_marked"] == 39
    assert raw["headline"]["or_combined"] == 51
    assert raw["headline"]["indicate_combined"] == 52

    ind_tp = {
        (s, samp)
        for s, samp, m in zip(indicate.stems, indicate._samples(), indicate.marked_lrs)
        if m > 0
    }
    ht_tp = {
        (s, samp)
        for s, samp, m in zip(hashtok.stems, hashtok._samples(), hashtok.marked_lrs)
        if m > 0
    }
    marked = set(zip(indicate.stems, indicate._samples(), strict=True))
    recovers = (marked - ind_tp) & ht_tp
    assert recovers == {
        ("01-harbour", 1),
        ("02-night-bus", 1),
        ("04-market", 3),
        ("05-kitchen", 3),
        ("06-station", 1),
        ("06-station", 2),
        ("10-office", 1),
        ("11-garden", 2),
        ("11-garden", 3),
        ("11-garden", 4),
    }
    assert (marked - ht_tp) & ind_tp == {
        ("03-library", 1),
        ("03-library", 3),
        ("03-library", 4),
        ("04-market", 1),
        ("07-rain", 1),
        ("06-station", 4),
    }
    both_miss = marked - ind_tp - ht_tp
    assert ("08-letter", 2) in both_miss
    assert ("08-letter", 3) in both_miss
    assert ("08-letter", 4) in both_miss
    assert len(both_miss) == 9
    by_ind = {
        (s, samp): m
        for s, samp, m in zip(indicate.stems, indicate._samples(), indicate.marked_lrs)
    }
    by_ht = {
        (s, samp): m
        for s, samp, m in zip(hashtok.stems, hashtok._samples(), hashtok.marked_lrs)
    }
    assert by_ind[("08-letter", 2)] < 0
    assert by_ht[("08-letter", 2)] < 0

    def coverage(primary, fallback) -> tuple[int, int]:
        ms = [
            p if p != 0.0 else f
            for p, f in zip(primary.marked_lrs, fallback.marked_lrs, strict=True)
        ]
        us = [
            p if p != 0.0 else f
            for p, f in zip(primary.unmarked_lrs, fallback.unmarked_lrs, strict=True)
        ]
        return sum(s > 0 for s in ms), sum(s <= 0 for s in us)

    cov_m, cov_u = coverage(postokhits, hashtok)
    assert (cov_m, cov_u) == (35, 22)
    assert cov_m + cov_u < postokhits.n_marked_positive + postokhits.n_unmarked_nonpositive
    assert postokhits.n_marked_positive + postokhits.n_unmarked_nonpositive == 69
    hits_m, hits_u = coverage(hits, hashtok)
    assert (hits_m, hits_u) == (29, 25)

    assert stacked.n_marked_positive == saved_stack.n_marked_positive == 28
    assert stacked.n_unmarked_nonpositive == saved_stack.n_unmarked_nonpositive == 27
    nested = nested_threshold_by_stem(
        stacked.stems, stacked.marked_lrs, stacked.unmarked_lrs
    )
    assert (nested.n_marked_above, nested.n_unmarked_at_most) == (21, 37)
    assert raw["headline"]["lda_nested_marked"] == 21
    assert raw["nested_2d_youden"]["indicate_or_hashtok"]["n_marked_positive"] == 37
    assert raw["nested_2d_youden"]["indicate_or_hashtok"][
        "n_unmarked_nonpositive"
    ] == 18
    assert or_m < 40
    assert stacked.n_prompts_marked_above == 10


def test_in_domain_tokhybrid_copies_hashtok_isolated() -> None:
    """Token-level occupancy-free hybrid copies hashtok 33/48 vs 22/48.

    Prompt ranking rises to 11/12. poshashtok nested 14/48 vs 38/48 is a
    specificity knob. Hybrid occupancy extras are the same four files as
    hashpool vs hashtok. Letter d2 stays negative. Do not sell 33/48.
    """
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-tokhybrid-poshashtok"
    )
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    th = holdout_from_json(root / "tokhybrid" / "holdout.json")
    hy = holdout_from_json(root / "hybrid" / "holdout.json")
    ph = holdout_from_json(root / "poshashtok" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    assert results["used_keys"] is False
    assert th.used_keys is False
    assert ph.used_keys is False
    assert th.instance == "key-free-tokhybrid"
    assert ph.instance == "key-free-poshashtok"
    assert ht.n_marked_positive == th.n_marked_positive == 33
    assert ht.n_unmarked_nonpositive == th.n_unmarked_nonpositive == 22
    assert th.n_prompts_marked_above == 11
    assert ht.n_prompts_marked_above == 9
    assert ph.n_marked_positive == 28
    assert ph.n_unmarked_nonpositive == 25
    assert hy.n_marked_positive == 35
    assert th.n_marked_positive < 39

    def nested_stem(name: str) -> tuple[int, int]:
        method = next(m for m in results["methods"] if m["name"] == name)
        row = method["nested_stem"]["nested-youden-by-stem"]
        return int(row["n_marked_above"]), int(row["n_unmarked_at_most"])

    assert nested_stem("tokhybrid") == (23, 35)
    assert nested_stem("poshashtok") == (14, 38)
    assert nested_stem("hashtok") == (22, 30)
    ht_pos = {
        (s, samp)
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
        if m > 0
    }
    th_pos = {
        (s, samp)
        for s, samp, m in zip(th.stems, th._samples(), th.marked_lrs)
        if m > 0
    }
    hy_pos = {
        (s, samp)
        for s, samp, m in zip(hy.stems, hy._samples(), hy.marked_lrs)
        if m > 0
    }
    assert ht_pos == th_pos
    assert hy_pos - th_pos == {
        ("02-night-bus", 3),
        ("03-library", 2),
        ("04-market", 1),
        ("12-ferry-queue", 4),
    }
    by_th = {
        (s, samp): m
        for s, samp, m in zip(th.stems, th._samples(), th.marked_lrs)
    }
    by_ph = {
        (s, samp): m
        for s, samp, m in zip(ph.stems, ph._samples(), ph.marked_lrs)
    }
    assert by_th[("08-letter", 2)] < 0
    assert by_ph[("08-letter", 2)] < 0


def test_in_domain_hashtokgap_is_weaker_than_hashtok() -> None:
    """Hashtok residual of unseen n-grams is a strict subset of hashtok 33/48.

    27/48 vs 21/48; nested 17/48 vs 31/48. Loses harbour d2, kitchen d1,
    station d1/d2/d3, rain d3; gains none. Letter d2 stays negative. Do
    not sell 27/48 as replacing 29/48.
    """
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-hashtokgap"
    )
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    th = holdout_from_json(root / "tokhybrid" / "holdout.json")
    gap = holdout_from_json(root / "hashtokgap" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    assert results["used_keys"] is False
    assert gap.used_keys is False
    assert gap.used_hash_iv is False
    assert gap.used_g_values is False
    assert gap.instance == "key-free-hashtokgap"
    assert ht.n_marked_positive == th.n_marked_positive == 33
    assert ht.n_unmarked_nonpositive == th.n_unmarked_nonpositive == 22
    assert gap.n_marked_positive == 27
    assert gap.n_unmarked_nonpositive == 21
    assert gap.n_prompts_marked_above == 8
    assert ht.n_prompts_marked_above == 9
    assert th.n_prompts_marked_above == 11
    assert gap.n_marked_positive < 29
    assert gap.n_marked_positive + gap.n_unmarked_nonpositive == 48

    def nested_stem(name: str) -> tuple[int, int]:
        method = next(m for m in results["methods"] if m["name"] == name)
        row = method["nested_stem"]["nested-youden-by-stem"]
        return int(row["n_marked_above"]), int(row["n_unmarked_at_most"])

    assert nested_stem("hashtokgap") == (17, 31)
    assert nested_stem("hashtok") == (22, 30)
    assert nested_stem("tokhybrid") == (23, 35)

    def pos(holdout) -> set[tuple[str, int]]:
        return {
            (s, samp)
            for s, samp, m in zip(holdout.stems, holdout._samples(), holdout.marked_lrs)
            if m > 0
        }

    ht_pos = pos(ht)
    gap_pos = pos(gap)
    assert gap_pos < ht_pos
    assert ht_pos - gap_pos == {
        ("01-harbour", 2),
        ("05-kitchen", 1),
        ("06-station", 1),
        ("06-station", 2),
        ("06-station", 3),
        ("07-rain", 3),
    }
    by_gap = {
        (s, samp): m
        for s, samp, m in zip(gap.stems, gap._samples(), gap.marked_lrs)
    }
    by_ht = {
        (s, samp): m
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
    }
    assert by_gap[("08-letter", 2)] < 0
    assert by_ht[("08-letter", 2)] < 0
    assert by_gap[("08-letter", 2)] == by_ht[("08-letter", 2)]


def test_in_domain_hashtok2_reshuffles_hashtok_not_a_singleton_core() -> None:
    """Full-file min_count=2 is 34/48 vs 21/48, not prefix-5's 10/48 core.

    Lost harbour d2, night-bus d4, station d1; gained night-bus d3,
    library d1/d2, ferry-queue d4. Nested 19/48 vs 35/48. Letter d2
    stays negative. Do not sell 34/48 as replacing 29/48.
    """
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-hashtok2"
    )
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    ht2 = holdout_from_json(root / "hashtok2" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    assert results["used_keys"] is False
    assert ht2.used_keys is False
    assert ht2.used_hash_iv is False
    assert ht2.used_g_values is False
    assert ht2.instance == "key-free-hashtok2"
    assert ht.n_marked_positive == 33
    assert ht.n_unmarked_nonpositive == 22
    assert ht2.n_marked_positive == 34
    assert ht2.n_unmarked_nonpositive == 21
    assert ht2.n_prompts_marked_above == 8
    assert ht.n_prompts_marked_above == 9
    assert ht2.n_marked_positive < 39
    assert ht2.n_marked_positive + ht2.n_unmarked_nonpositive == 55

    def nested_stem(name: str) -> tuple[int, int]:
        method = next(m for m in results["methods"] if m["name"] == name)
        row = method["nested_stem"]["nested-youden-by-stem"]
        return int(row["n_marked_above"]), int(row["n_unmarked_at_most"])

    assert nested_stem("hashtok2") == (19, 35)
    assert nested_stem("hashtok") == (22, 30)

    def pos(holdout) -> set[tuple[str, int]]:
        return {
            (s, samp)
            for s, samp, m in zip(holdout.stems, holdout._samples(), holdout.marked_lrs)
            if m > 0
        }

    ht_pos = pos(ht)
    ht2_pos = pos(ht2)
    assert ht2_pos - ht_pos == {
        ("02-night-bus", 3),
        ("03-library", 1),
        ("03-library", 2),
        ("12-ferry-queue", 4),
    }
    assert ht_pos - ht2_pos == {
        ("01-harbour", 2),
        ("02-night-bus", 4),
        ("06-station", 1),
    }
    by_ht2 = {
        (s, samp): m
        for s, samp, m in zip(ht2.stems, ht2._samples(), ht2.marked_lrs)
    }
    by_ht = {
        (s, samp): m
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
    }
    assert by_ht2[("08-letter", 2)] < 0
    assert by_ht[("08-letter", 2)] < 0
    assert by_ht2[("08-letter", 2)] < by_ht[("08-letter", 2)]


def test_opening_grain_hashtok_copies_tokhits_density() -> None:
    """Matched prefix-4 occupancy-free hashing is sparse like tokhits.

    tokhits 23/48 vs 48/48 (prompt 12/12); hashtok 24/48 vs 47/48 with
    extra TP letter d3 only; hashtok2 22/48 vs 48/48. Letter d2 is zero.
    Nested hashtok 23/48 vs 47/48. Not opening rankpath 41/48. Marked
    recall 24/48 is below hard last-4 29/48. Do not sell 24/48 as
    replacing 29/48.
    """
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-fitprefix4-hashtok"
    )
    hits = holdout_from_json(root / "hits" / "holdout.json")
    tok = holdout_from_json(root / "tokhits" / "holdout.json")
    ht = holdout_from_json(root / "hashtok" / "holdout.json")
    ht2 = holdout_from_json(root / "hashtok2" / "holdout.json")
    results = json.loads((root / "results.json").read_text())
    assert results["used_keys"] is False
    assert results["fit_prefix"] == 4
    assert ht.used_keys is False
    assert ht.used_hash_iv is False
    assert ht.used_g_values is False
    assert ht.instance == "key-free-hashtok"
    assert ht2.instance == "key-free-hashtok2"
    assert tok.instance == "key-free-tokhits"
    assert hits.n_prompts_marked_above == 9
    assert tok.n_prompts_marked_above == 12
    assert ht.n_prompts_marked_above == 12
    assert ht2.n_prompts_marked_above == 12
    assert hits.n_marked_positive == 23
    assert hits.n_unmarked_nonpositive == 48
    assert tok.n_marked_positive == 23
    assert tok.n_unmarked_nonpositive == 48
    assert ht.n_marked_positive == 24
    assert ht.n_unmarked_nonpositive == 47
    assert ht2.n_marked_positive == 22
    assert ht2.n_unmarked_nonpositive == 48
    assert ht.n_marked_positive < 29

    def nested_stem(name: str) -> tuple[int, int]:
        method = next(m for m in results["methods"] if m["name"] == name)
        row = method["nested_stem"]["nested-youden-by-stem"]
        return int(row["n_marked_above"]), int(row["n_unmarked_at_most"])

    assert nested_stem("hits") == (23, 48)
    assert nested_stem("tokhits") == (23, 48)
    assert nested_stem("hashtok") == (23, 47)
    assert nested_stem("hashtok2") == (22, 48)

    def pos(holdout) -> set[tuple[str, int]]:
        return {
            (s, samp)
            for s, samp, m in zip(holdout.stems, holdout._samples(), holdout.marked_lrs)
            if m > 0
        }

    tok_pos = pos(tok)
    ht_pos = pos(ht)
    ht2_pos = pos(ht2)
    assert tok_pos < ht_pos
    assert ht_pos - tok_pos == {("08-letter", 3)}
    assert ht2_pos - tok_pos == {("08-letter", 3)}
    assert tok_pos - ht2_pos == {("05-kitchen", 4), ("07-rain", 1)}

    by_hits = {
        (s, samp): m
        for s, samp, m in zip(hits.stems, hits._samples(), hits.marked_lrs)
    }
    by_tok = {
        (s, samp): m
        for s, samp, m in zip(tok.stems, tok._samples(), tok.marked_lrs)
    }
    by_ht = {
        (s, samp): m
        for s, samp, m in zip(ht.stems, ht._samples(), ht.marked_lrs)
    }
    by_ht2 = {
        (s, samp): m
        for s, samp, m in zip(ht2.stems, ht2._samples(), ht2.marked_lrs)
    }
    assert by_hits[("08-letter", 2)] == 0
    assert by_tok[("08-letter", 2)] == 0
    assert by_ht[("08-letter", 2)] == 0
    assert by_ht2[("08-letter", 2)] == 0
    assert by_ht[("08-letter", 3)] > 0
    assert by_tok[("08-letter", 3)] == 0

    unmarked_fp = {
        (s, samp)
        for s, samp, u in zip(ht.stems, ht._samples(), ht.unmarked_lrs)
        if u > 0
    }
    assert unmarked_fp == {("05-kitchen", 4)}


def test_hashtok_nhashes_width_ablation_default_is_not_best() -> None:
    """In-domain hashtok n=2/4 beat default n=8; n=32 hurts.

    n=2: 11/12, 34/48 vs 31/48, nested 28/48 vs 37/48, AUC 0.764.
    n=4: 11/12, 36/48 vs 30/48, nested 35/48 vs 30/48.
    n=8: 9/12, 33/48 vs 22/48, nested 22/48 vs 30/48.
    n=16: 11/12, 36/48 vs 22/48, nested 29/48 vs 24/48.
    n=32: 10/12, 30/48 vs 26/48, nested 21/48 vs 38/48.
    Letter d2 stays negative except n=16; that prompt still loses.
    Do not sell 36/48, 35/48, or 34/48 as replacing 29/48.
    """
    import json

    root = Path(__file__).resolve().parents[1] / "experiments"

    def load(name: str):
        d = root / name
        holdout = holdout_from_json(d / "hashtok" / "holdout.json")
        results = json.loads((d / "results.json").read_text())
        method = next(m for m in results["methods"] if m["name"] == "hashtok")
        nested = method["nested_stem"]["nested-youden-by-stem"]
        letter = next(
            m
            for s, samp, m in zip(
                holdout.stems, holdout._samples(), holdout.marked_lrs
            )
            if s == "08-letter" and samp == 2
        )
        return holdout, nested, letter, results

    n2, nest2, letter2, res2 = load("2026-09-01-probe-12x4-hashtok-nhashes2")
    n4, nest4, letter4, res4 = load("2026-09-01-probe-12x4-hashtok-nhashes4")
    n8, nest8, letter8, res8 = load("2026-09-01-probe-12x4-hashtok")
    n16, nest16, letter16, res16 = load("2026-09-01-probe-12x4-hashtok-nhashes16")
    n32, nest32, letter32, res32 = load("2026-09-01-probe-12x4-hashtok-nhashes32")

    for holdout, results in (
        (n2, res2),
        (n4, res4),
        (n8, res8),
        (n16, res16),
        (n32, res32),
    ):
        assert results["used_keys"] is False
        assert holdout.used_keys is False
        assert holdout.used_hash_iv is False
        assert holdout.used_g_values is False
        assert holdout.instance == "key-free-hashtok"

    assert n2.n_prompts_marked_above == 11
    assert n2.n_marked_positive == 34
    assert n2.n_unmarked_nonpositive == 31
    assert (nest2["n_marked_above"], nest2["n_unmarked_at_most"]) == (28, 37)
    assert res2["methods"][0]["binary"]["auc"] > 0.76

    assert n4.n_prompts_marked_above == 11
    assert n4.n_marked_positive == 36
    assert n4.n_unmarked_nonpositive == 30
    assert (nest4["n_marked_above"], nest4["n_unmarked_at_most"]) == (35, 30)

    ht8 = next(m for m in res8["methods"] if m["name"] == "hashtok")
    assert n8.n_prompts_marked_above == 9
    assert n8.n_marked_positive == 33
    assert n8.n_unmarked_nonpositive == 22
    assert (nest8["n_marked_above"], nest8["n_unmarked_at_most"]) == (22, 30)
    assert ht8["binary"]["auc"] < res2["methods"][0]["binary"]["auc"]

    assert n16.n_prompts_marked_above == 11
    assert n16.n_marked_positive == 36
    assert n16.n_unmarked_nonpositive == 22
    assert (nest16["n_marked_above"], nest16["n_unmarked_at_most"]) == (29, 24)

    assert n32.n_prompts_marked_above == 10
    assert n32.n_marked_positive == 30
    assert n32.n_unmarked_nonpositive == 26
    assert (nest32["n_marked_above"], nest32["n_unmarked_at_most"]) == (21, 38)
    assert n32.n_marked_positive < n8.n_marked_positive

    assert n2.n_marked_positive < 39
    assert n4.n_marked_positive < 39
    assert n4.n_marked_positive > 29
    assert nest2["n_unmarked_at_most"] < 39
    assert nest2["n_unmarked_at_most"] > nest8["n_unmarked_at_most"]
    assert nest2["n_marked_above"] > nest8["n_marked_above"]

    assert letter2 < 0
    assert letter4 < 0
    assert letter8 < 0
    assert letter16 > 0
    assert letter32 < 0
    assert n16.n_prompts_marked_above == 11
    letter_prompt_n16 = [
        m for s, m in zip(n16.stems, n16.marked_lrs) if s == "08-letter"
    ]
    unmarked_letter_n16 = [
        u for s, u in zip(n16.stems, n16.unmarked_lrs) if s == "08-letter"
    ]
    assert len(letter_prompt_n16) == 4
    assert sum(letter_prompt_n16) / 4 < sum(unmarked_letter_n16) / 4


def test_hashtok_nhashes_width_does_not_transfer() -> None:
    """24→12 nested Youden prefers default n=8 over in-domain n=2/4.

    n=8: 11/12, 29/48 vs 35/48, nested Youden 17/48 vs 46/48.
    n=2: 10/12, 29/48 vs 32/48, nested 17/48 vs 44/48.
    n=4: 9/12, 31/48 vs 30/48, nested 19/48 vs 41/48.
    Keep the CLI default at 8. t=0 29/48 is not headline 29/48.
    Do not sell 31/48, 19/48, or 17/48 as replacing 29/48.
    """
    import json

    root = Path(__file__).resolve().parents[1] / "experiments"

    def load(name: str):
        d = root / name
        holdout = holdout_from_json(d / "hashtok" / "holdout.json")
        results = json.loads((d / "results.json").read_text())
        return holdout, results

    n2, r2 = load("2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes2")
    n4, r4 = load("2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes4")
    n8, r8 = load("2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8")

    for holdout, results in ((n2, r2), (n4, r4), (n8, r8)):
        assert results["used_keys"] is False
        assert results["used_hash_iv"] is False
        assert results["used_g_values"] is False
        assert results["n_train_prompts"] == 24
        assert results["n_test_prompts"] == 12
        assert results["overlap_mode"] == "drop-from-train"
        assert holdout.used_keys is False
        assert holdout.instance == "key-free-hashtok"

    assert n2.n_prompts_marked_above == 10
    assert n2.n_marked_positive == 29
    assert n2.n_unmarked_nonpositive == 32
    assert _nested_youden(r2, "hashtok") == (17, 44)

    assert n4.n_prompts_marked_above == 9
    assert n4.n_marked_positive == 31
    assert n4.n_unmarked_nonpositive == 30
    assert _nested_youden(r4, "hashtok") == (19, 41)

    assert n8.n_prompts_marked_above == 11
    assert n8.n_marked_positive == 29
    assert n8.n_unmarked_nonpositive == 35
    assert _nested_youden(r8, "hashtok") == (17, 46)

    assert n8.n_prompts_marked_above > n2.n_prompts_marked_above
    assert n8.n_prompts_marked_above > n4.n_prompts_marked_above
    assert n8.n_unmarked_nonpositive > n2.n_unmarked_nonpositive
    assert n8.n_unmarked_nonpositive > n4.n_unmarked_nonpositive
    nest8 = _nested_youden(r8, "hashtok")
    nest2 = _nested_youden(r2, "hashtok")
    nest4 = _nested_youden(r4, "hashtok")
    assert nest8[1] > nest2[1]
    assert nest8[1] > nest4[1]
    assert n4.n_marked_positive < 39
    assert nest8[0] < 29
    letter8 = next(
        m
        for s, samp, m in zip(n8.stems, n8._samples(), n8.marked_lrs)
        if s == "08-letter" and samp == 2
    )
    letter2 = next(
        m
        for s, samp, m in zip(n2.stems, n2._samples(), n2.marked_lrs)
        if s == "08-letter" and samp == 2
    )
    letter4 = next(
        m
        for s, samp, m in zip(n4.stems, n4._samples(), n4.marked_lrs)
        if s == "08-letter" and samp == 2
    )
    assert letter8 < 0
    assert letter2 < 0
    assert letter4 < 0


def test_rotate_hashpool_seed_is_not_hash_iv() -> None:
    """Feature-hash seed is not SynthID hash_iv. Different seeds mix differently."""
    twins = load_twins(PAIR)
    a = rotate_hashpool(
        twins,
        context_len=2,
        n_hashes=2,
        n_buckets=16,
        method_name="hashtok",
        seed=1,
    )
    b = rotate_hashpool(
        twins,
        context_len=2,
        n_hashes=2,
        n_buckets=16,
        method_name="hashtok",
        seed=2,
    )
    assert a.used_keys is False
    assert a.used_hash_iv is False
    assert a.used_g_values is False
    assert a.instance == "key-free-hashtok"
    assert b.used_hash_iv is False
    assert (tuple(a.marked_lrs), tuple(a.unmarked_lrs)) != (
        tuple(b.marked_lrs),
        tuple(b.unmarked_lrs),
    )


def test_hashtok_nhashes2_seed_win_is_not_a_width_law() -> None:
    """Default n=2 seed 20260831 is a lucky mixer, not a typical n=2.

    n=2 spec ranges 21–31/48 unmarked and 25–37/48 nested. Seed 0 keeps
    34 TPs and collapses spec to 21/48. n=8 seed 7 nested 28/37 matches
    the advertised n=2 default. Letter d2 flips at seeds 0 and 12345.
    Do not sell 34/48 as a width law or as replacing 29/48.
    """
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-probe-12x4-hashtok-nhashes2-seeds"
    )
    payload = json.loads((root / "results.json").read_text())
    assert payload["used_keys"] is False
    assert payload["used_hash_iv"] is False
    assert payload["used_g_values"] is False
    by = {(int(r["n_hashes"]), int(r["seed"])): r for r in payload["rows"]}
    d = by[(2, 20260831)]
    assert d["n_prompt_wins"] == 11
    assert d["n_marked_positive"] == 34
    assert d["n_unmarked_nonpositive"] == 31
    assert d["nested_marked"] == 28
    assert d["nested_unmarked"] == 37
    assert d["letter_d2"] < 0
    locked = holdout_from_json(root / "n2-seed20260831" / "hashtok" / "holdout.json")
    assert locked.n_marked_positive == 34
    assert locked.used_hash_iv is False

    s0 = by[(2, 0)]
    assert s0["n_marked_positive"] == 34
    assert s0["n_unmarked_nonpositive"] == 21
    assert s0["letter_d2"] > 0

    s42 = by[(2, 42)]
    assert s42["nested_marked"] == 34
    assert s42["nested_unmarked"] == 25

    s12345 = by[(2, 12345)]
    assert s12345["letter_d2"] > 0

    n8s7 = by[(8, 7)]
    assert n8s7["n_prompt_wins"] == 11
    assert n8s7["nested_marked"] == 28
    assert n8s7["nested_unmarked"] == 37

    n2_specs = [by[(2, s)]["n_unmarked_nonpositive"] for s in (20260831, 0, 1, 7, 42, 12345)]
    assert min(n2_specs) == 21
    assert max(n2_specs) == 31
    n2_nested_spec = [by[(2, s)]["nested_unmarked"] for s in (20260831, 0, 1, 7, 42, 12345)]
    assert min(n2_nested_spec) == 25
    assert max(n2_nested_spec) == 37
    n2_prompts = [by[(2, s)]["n_prompt_wins"] for s in (20260831, 0, 1, 7, 42, 12345)]
    assert min(n2_prompts) == 9
    assert max(n2_prompts) == 11


def test_hashtok_transfer_seed_win_is_not_a_width_law() -> None:
    """24→12 n=8 default seed is a lucky mixer, not a typical n=8.

    Other n=8 seeds: prompt 10/12, t=0 marked 25–27. n=2 seed 7 nested
    19/48 vs 47/48 beats that default nested. Letter d2 flips at seed 0.
    Keep n_hashes=8 / seed 20260831. Do not sell 19/48 as replacing 29/48.
    """
    import json

    root = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-36x4-to-12x4-hashtok-seeds"
    )
    payload = json.loads((root / "results.json").read_text())
    assert payload["used_keys"] is False
    assert payload["used_hash_iv"] is False
    by = {(int(r["n_hashes"]), int(r["seed"])): r for r in payload["rows"]}
    d8 = by[(8, 20260831)]
    assert d8["n_prompt_wins"] == 11
    assert d8["n_marked_positive"] == 29
    assert d8["n_unmarked_nonpositive"] == 35
    assert d8["nested_marked"] == 17
    assert d8["nested_unmarked"] == 46
    s0 = by[(8, 0)]
    assert s0["n_prompt_wins"] == 10
    assert s0["n_marked_positive"] == 27
    assert s0["letter_d2"] > 0
    s7 = by[(8, 7)]
    assert s7["n_prompt_wins"] == 10
    assert s7["n_marked_positive"] == 25
    n2s7 = by[(2, 7)]
    assert n2s7["nested_marked"] == 19
    assert n2s7["nested_unmarked"] == 47
    assert n2s7["n_prompt_wins"] == 9
    n2s0 = by[(2, 0)]
    assert n2s0["letter_d2"] > 0
    assert n2s7["nested_marked"] < 39
    hold = holdout_from_json(root / "n2-seed7" / "hashtok" / "holdout.json")
    assert hold.used_hash_iv is False
    assert hold.n_prompts_marked_above == 9


def _letter_d2(holdout) -> float:
    return next(
        m
        for s, samp, m in zip(holdout.stems, holdout._samples(), holdout.marked_lrs)
        if s == "08-letter" and samp == 2
    )


def _nested_fpr10(results: dict, name: str) -> tuple[int, int]:
    rows = [
        row
        for row in results["thresholds"]
        if row["name"] == name and row["source"] == "nested-fpr10"
    ]
    assert len(rows) == 1
    return int(rows[0]["n_marked_above"]), int(rows[0]["n_unmarked_at_most"])


def test_hashtok_lastk_in_domain_is_not_an_order_law() -> None:
    """In-domain hashtok last-1 is chance; last-3 11/12 is a sparse knob.

    Frozen mixer n_hashes=8, seed 20260831. last-3 t=0 24/48 is below
    hard last-4 29/48. Keep context_len=4. Do not sell 24/48.
    """
    import json

    root = Path(__file__).resolve().parents[1] / "experiments"

    def load(name: str):
        d = root / name
        holdout = holdout_from_json(d / "hashtok" / "holdout.json")
        results = json.loads((d / "results.json").read_text())
        method = next(m for m in results["methods"] if m["name"] == "hashtok")
        nested = method["nested_stem"]["nested-youden-by-stem"]
        return holdout, nested, results

    k1, nest1, r1 = load("2026-09-01-probe-12x4-hashtok-k1")
    k2, nest2, r2 = load("2026-09-01-probe-12x4-hashtok-k2")
    k3, nest3, r3 = load("2026-09-01-probe-12x4-hashtok-k3")
    k4, nest4, r4 = load("2026-09-01-probe-12x4-hashtok")

    for holdout, results in ((k1, r1), (k2, r2), (k3, r3), (k4, r4)):
        assert results["used_keys"] is False
        assert holdout.used_keys is False
        assert holdout.used_hash_iv is False
        assert holdout.used_g_values is False
        assert holdout.instance == "key-free-hashtok"

    assert r1["context_len"] == 1
    assert r2["context_len"] == 2
    assert r3["context_len"] == 3
    assert r4["context_len"] == 4

    assert k1.n_prompts_marked_above == 5
    assert k1.n_marked_positive == 22
    assert k1.n_unmarked_nonpositive == 22
    assert (nest1["n_marked_above"], nest1["n_unmarked_at_most"]) == (9, 42)
    assert r1["methods"][0]["binary"]["auc"] < 0.52

    assert k2.n_prompts_marked_above == 9
    assert k2.n_marked_positive == 27
    assert k2.n_unmarked_nonpositive == 28
    assert (nest2["n_marked_above"], nest2["n_unmarked_at_most"]) == (19, 32)

    assert k3.n_prompts_marked_above == 11
    assert k3.n_marked_positive == 24
    assert k3.n_unmarked_nonpositive == 36
    assert (nest3["n_marked_above"], nest3["n_unmarked_at_most"]) == (22, 40)

    assert k4.n_prompts_marked_above == 9
    assert k4.n_marked_positive == 33
    assert k4.n_unmarked_nonpositive == 22
    assert (nest4["n_marked_above"], nest4["n_unmarked_at_most"]) == (22, 30)

    assert k3.n_marked_positive < 29
    assert k3.n_marked_positive < k4.n_marked_positive
    assert nest3["n_unmarked_at_most"] > nest4["n_unmarked_at_most"]
    assert nest3["n_marked_above"] == nest4["n_marked_above"]
    assert k1.n_prompts_marked_above < k4.n_prompts_marked_above
    assert k3.n_prompts_marked_above > k4.n_prompts_marked_above
    assert k3.n_marked_positive < 39
    assert nest3["n_marked_above"] < 39

    assert _letter_d2(k1) < 0
    assert _letter_d2(k2) < 0
    assert _letter_d2(k3) > 0
    assert _letter_d2(k4) < 0


def test_hashtok_lastk_does_not_transfer_as_an_order_law() -> None:
    """24→12 last-4 still wins prompt ranking and nested FPR10 recall.

    last-2 file AUC 0.738 is ranking, not isolated classification
    (nested Youden 15/48 vs last-4 17/48). last-1 nested 18/48 has
    prompt 7/12 and FPR10 8/48. last-3 nested 11/48 is sparse.
    Keep context_len=4. Do not sell 18/48 or 0.738 as replacing 29/48.
    """
    import json

    root = Path(__file__).resolve().parents[1] / "experiments"

    def load(name: str):
        d = root / name
        holdout = holdout_from_json(d / "hashtok" / "holdout.json")
        results = json.loads((d / "results.json").read_text())
        return holdout, results

    k1, r1 = load("2026-09-01-transfer-36x4-to-12x4-hashtok-k1")
    k2, r2 = load("2026-09-01-transfer-36x4-to-12x4-hashtok-k2")
    k3, r3 = load("2026-09-01-transfer-36x4-to-12x4-hashtok-k3")
    k4, r4 = load("2026-09-01-transfer-36x4-to-12x4-hashtok-nhashes8")

    for holdout, results in ((k1, r1), (k2, r2), (k3, r3), (k4, r4)):
        assert results["used_keys"] is False
        assert results["used_hash_iv"] is False
        assert results["used_g_values"] is False
        assert results["n_train_prompts"] == 24
        assert results["n_test_prompts"] == 12
        assert results["overlap_mode"] == "drop-from-train"
        assert holdout.used_keys is False
        assert holdout.instance == "key-free-hashtok"

    assert r1["context_len"] == 1
    assert r2["context_len"] == 2
    assert r3["context_len"] == 3
    assert r4["context_len"] == 4

    assert k1.n_prompts_marked_above == 7
    assert k1.n_marked_positive == 25
    assert k1.n_unmarked_nonpositive == 35
    assert _nested_youden(r1, "hashtok") == (18, 45)
    assert _nested_fpr10(r1, "hashtok") == (8, 46)

    assert k2.n_prompts_marked_above == 10
    assert k2.n_marked_positive == 29
    assert k2.n_unmarked_nonpositive == 36
    assert _nested_youden(r2, "hashtok") == (15, 45)
    assert r2["methods"][0]["binary"]["auc"] > 0.73

    assert k3.n_prompts_marked_above == 10
    assert k3.n_marked_positive == 25
    assert k3.n_unmarked_nonpositive == 34
    assert _nested_youden(r3, "hashtok") == (11, 47)

    assert k4.n_prompts_marked_above == 11
    assert k4.n_marked_positive == 29
    assert k4.n_unmarked_nonpositive == 35
    assert _nested_youden(r4, "hashtok") == (17, 46)
    assert _nested_fpr10(r4, "hashtok") == (17, 46)

    assert k4.n_prompts_marked_above > k2.n_prompts_marked_above
    assert k4.n_prompts_marked_above > k1.n_prompts_marked_above
    nest4 = _nested_youden(r4, "hashtok")
    nest2 = _nested_youden(r2, "hashtok")
    nest3 = _nested_youden(r3, "hashtok")
    nest1 = _nested_youden(r1, "hashtok")
    assert nest2[0] < nest4[0]
    assert nest3[0] < nest4[0]
    assert nest1[0] < 29
    assert nest4[0] < 29
    assert k2.n_marked_positive < 39
    auc2 = r2["methods"][0]["binary"]["auc"]
    auc4 = r4["methods"][0]["binary"]["auc"]
    assert auc2 > auc4
    assert _letter_d2(k1) < 0
    assert _letter_d2(k2) < 0
    assert _letter_d2(k3) < 0
    assert _letter_d2(k4) < 0


def test_confirmatory_100_prompts_are_preregistered_and_disjoint() -> None:
    """100 new one-liners exist before pair; no overlap with the 36 seeds."""
    root = Path(__file__).resolve().parents[1] / "experiments"
    new = root / "2026-09-01-prompts-100"
    old = root / "2026-08-17-prompts-36"
    files = sorted(p for p in new.glob("*.txt") if p.stem.isdigit())
    assert len(files) == 100
    texts = [p.read_text().strip() for p in files]
    assert all(texts)
    assert len(set(texts)) == 100
    old_texts = {p.read_text().strip() for p in old.glob("*.txt")}
    assert not (set(texts) & old_texts)
    protocol = Path(__file__).resolve().parents[1] / "research" / "PROTOCOL-next.md"
    body = protocol.read_text()
    assert "2026-09-01-prompts-100" in body
    assert "--methods interpolate --context-len 4" in body
    assert "--methods poshits --fit-prefix 4 --pos-bucket 1" in body
    assert "--rankpath --fit-prefix 4 --pos-bucket 1" in body
    assert "Primary endpoint" in body

