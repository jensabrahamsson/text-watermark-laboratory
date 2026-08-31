"""Probe CLI and published 12×4 holdout statistics."""

from pathlib import Path

from text_watermark_tools.blind import load_twins
from text_watermark_tools.cli import main
from text_watermark_tools.indicator import holdout_from_json
from text_watermark_tools.probe import rotate_count_methods, run_probe
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
