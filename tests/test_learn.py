"""Key-free learned scorers stay key-free and separate a planted shift."""

from pathlib import Path

from text_watermark_tools.blind import Twin
from text_watermark_tools.cli import main
from text_watermark_tools.learn import (
    LearnSpec,
    hashed_ngram_vector,
    persist_learn,
    persist_learn_transfer,
    run_learn,
    run_learn_transfer,
)
from text_watermark_tools.stats import binary_eval


def _twin(stem: str, marked: list[int], unmarked: list[int], extra: int = 0) -> Twin:
    extra_m = []
    extra_u = []
    extra_mt = []
    extra_ut = []
    for i in range(extra):
        extra_m.append([t + i + 1 for t in marked])
        extra_u.append([t + i + 1 for t in unmarked])
        extra_mt.append("m")
        extra_ut.append("u")
    return Twin(
        stem=stem,
        marked_text="m",
        unmarked_text="u",
        marked_ids=list(marked),
        unmarked_ids=list(unmarked),
        extra_marked_ids=extra_m,
        extra_unmarked_ids=extra_u,
        extra_marked_text=extra_mt,
        extra_unmarked_text=extra_ut,
    )


def _planted(n_stems: int = 4, extra: int = 1) -> list[Twin]:
    twins = []
    for i in range(n_stems):
        marked = [10, 11, 30 + i, 31 + i]
        unmarked = [20, 21, 40 + i, 41 + i]
        twins.append(_twin(f"s{i:02d}", marked, unmarked, extra=extra))
    return twins


def test_hashed_ngram_vector_skips_token_zero_by_default() -> None:
    spec = LearnSpec(context_len=2, position_bucket=1, n_hashes=2, n_buckets=8)
    skipped = hashed_ngram_vector([7, 8, 9], spec)
    included = hashed_ngram_vector(
        [7, 8, 9], LearnSpec(context_len=2, position_bucket=1, n_hashes=2, n_buckets=8, include_first=True)
    )
    assert skipped.shape == (16,)
    assert float(skipped.sum()) != 0.0
    assert float(abs(included - skipped).sum()) > 0.0


def test_learn_loo_on_planted_shift_is_key_free(tmp_path: Path) -> None:
    spec = LearnSpec(
        context_len=2,
        position_bucket=1,
        n_hashes=2,
        n_buckets=16,
        epochs=12,
        seed=1,
    )
    twins = _planted()
    run = run_learn(
        twins,
        pair_dir="planted",
        archs=("hashlog", "tokmlp", "charcnn"),
        spec=spec,
        fit_prefix=4,
    )
    assert run.used_keys is False
    assert run.used_hash_iv is False
    assert run.used_g_values is False
    names = {m.name for m in run.methods}
    assert names == {"hashlog", "tokmlp", "charcnn"}
    for method in run.methods:
        assert method.holdout.used_keys is False
        assert method.holdout.used_hash_iv is False
        assert method.holdout.used_g_values is False
        assert method.holdout.instance.startswith("key-free-")
        stats = binary_eval(method.holdout.marked_lrs, method.holdout.unmarked_lrs, n_perm=50, seed=0)
        assert stats.auc > 0.9
        assert method.n_prompt_wins == method.n_prompts
    persist_learn(run, tmp_path)
    assert (tmp_path / "hashlog" / "holdout.json").is_file()
    assert (tmp_path / "tokmlp" / "holdout.json").is_file()
    assert (tmp_path / "charcnn" / "holdout.json").is_file()
    readme = (tmp_path / "README.md").read_text()
    assert "detector_mean" in readme
    assert "used_keys=False" in readme


def test_learn_transfer_nested_stays_key_free(tmp_path: Path) -> None:
    spec = LearnSpec(
        context_len=2,
        position_bucket=1,
        n_hashes=2,
        n_buckets=16,
        epochs=8,
        seed=2,
    )
    train = _planted(n_stems=4, extra=1)
    test = _planted(n_stems=3, extra=1)
    for twin in test:
        twin.stem = "t" + twin.stem[1:]
    xfer = run_learn_transfer(
        train,
        test,
        train_dir="train",
        test_dir="test",
        archs=("hashlog", "tokmlp"),
        spec=spec,
        fit_prefix=4,
        overlap_mode="keep",
        nested=True,
    )
    assert xfer.used_keys is False
    assert {m.name for m in xfer.methods} == {"hashlog", "tokmlp"}
    nested = {row.source for row in xfer.thresholds}
    assert "nested-youden" in nested
    assert "in-sample-youden" in nested
    persist_learn_transfer(xfer, tmp_path / "xfer")
    assert (tmp_path / "xfer" / "hashlog" / "holdout.json").is_file()


def test_cli_learn_help_mentions_key_free(capsys) -> None:
    try:
        main(["learn", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    out = capsys.readouterr().out
    assert "hashlog" in out
    assert "tokmlp" in out
    assert "charcnn" in out


def _hold(name: str, method: str):
    from text_watermark_tools.indicator import holdout_from_json

    root = Path(__file__).resolve().parents[1] / "experiments" / name
    return holdout_from_json(root / method / "holdout.json")


def test_learned_ood_gate_does_not_beat_poshits() -> None:
    hashlog = _hold("2026-08-31-learn-36x4-to-12x4-fitprefix4", "hashlog")
    tokmlp = _hold("2026-08-31-learn-36x4-to-12x4-fitprefix4", "tokmlp")
    charcnn = _hold("2026-08-31-learn-36x4-to-12x4-fitprefix4", "charcnn")
    poshits = _hold("2026-08-31-transfer-36x4-to-12x4-fitprefix4-pos1", "poshits")
    assert hashlog.used_keys is False
    assert tokmlp.used_keys is False
    assert charcnn.used_keys is False
    assert hashlog.n_prompts_marked_ge == 7
    assert tokmlp.n_prompts_marked_ge == 8
    assert charcnn.n_prompts_marked_ge == 7
    assert poshits.n_prompts_marked_ge == 12
    h_auc = binary_eval(hashlog.marked_lrs, hashlog.unmarked_lrs, n_perm=200, seed=0)
    t_auc = binary_eval(tokmlp.marked_lrs, tokmlp.unmarked_lrs, n_perm=200, seed=0)
    c_auc = binary_eval(charcnn.marked_lrs, charcnn.unmarked_lrs, n_perm=200, seed=0)
    p_auc = binary_eval(poshits.marked_lrs, poshits.unmarked_lrs, n_perm=200, seed=0)
    assert h_auc.auc < 0.65
    assert 0.65 < t_auc.auc < 0.80
    assert c_auc.auc < 0.65
    assert p_auc.auc > 0.85
    assert t_auc.auc < p_auc.auc


def test_learned_cross_generator_is_chance() -> None:
    distil = _hold("2026-08-31-learn-36x4-to-distil-fitprefix4", "tokmlp")
    qwen = _hold("2026-08-31-learn-36x4-to-qwen-fitprefix4", "charcnn")
    assert distil.used_keys is False
    assert qwen.used_keys is False
    d_auc = binary_eval(distil.marked_lrs, distil.unmarked_lrs, n_perm=200, seed=0)
    q_auc = binary_eval(qwen.marked_lrs, qwen.unmarked_lrs, n_perm=200, seed=0)
    assert d_auc.auc < 0.65
    assert q_auc.auc < 0.55
    hashlog_q = _hold("2026-08-31-learn-36x4-to-qwen-fitprefix4", "hashlog")
    assert binary_eval(hashlog_q.marked_lrs, hashlog_q.unmarked_lrs, n_perm=200, seed=0).auc < 0.55


def test_hashlog_twelve_prompt_loo_is_not_the_ood_gate() -> None:
    loo = _hold("2026-08-31-learn-12x4-fitprefix4", "hashlog")
    ood = _hold("2026-08-31-learn-36x4-to-12x4-fitprefix4", "hashlog")
    poshits = _hold("2026-08-31-probe-12x4-fitprefix4-pos1", "poshits")
    assert loo.n_prompts_marked_ge == 11
    assert ood.n_prompts_marked_ge == 7
    assert poshits.n_prompts_marked_ge == 9
    assert poshits.n_marked_positive == 23
    assert poshits.n_unmarked_nonpositive == 48


def test_qwen_include_first_hashlog_ranks_but_is_not_first_token_table() -> None:
    learned = _hold("2026-08-31-learn-qwen-12x4-fitprefix4-include-first", "hashlog")
    first = _hold("2026-08-31-probe-qwen-12x4-fitprefix4-pos1", "first")
    assert learned.used_keys is False
    assert learned.n_prompts_marked_ge == 12
    assert first.n_prompts_marked_ge == 12
    learned_auc = binary_eval(learned.marked_lrs, learned.unmarked_lrs, n_perm=200, seed=0)
    first_auc = binary_eval(first.marked_lrs, first.unmarked_lrs, n_perm=200, seed=0)
    assert learned_auc.auc > 0.75
    assert first_auc.auc > learned_auc.auc


def test_tokmlp_shuffle_collapses() -> None:
    ev = _hold("2026-08-31-learn-36x4-to-12x4-shuffle", "tokmlp")
    assert ev.used_keys is False
    assert ev.n_prompts_marked_ge == 5
    auc = binary_eval(ev.marked_lrs, ev.unmarked_lrs, n_perm=200, seed=0)
    assert auc.auc < 0.55
