"""Control-gen files are ignored by twin loaders; instance contrast stays key-free."""

from pathlib import Path

import pytest

from text_watermark_tools.blind import Twin, load_twins
from text_watermark_tools.cli import main
from text_watermark_tools.contrast import (
    ControlDraw,
    load_control_draws,
    logodds_brier,
    persist_contrast,
    run_instance_contrast,
)
from text_watermark_tools.stats import binary_eval


def test_load_control_draws_skips_marked(tmp_path: Path) -> None:
    (tmp_path / "01-a-marked.txt").write_text("marked text here")
    (tmp_path / "01-a-unmarked-gen.txt").write_text("unmarked text here")
    (tmp_path / "01-a-control-gen.txt").write_text("control text here")
    (tmp_path / "01-a-control-gen-2.txt").write_text("control two here")
    twins = load_twins(tmp_path)
    assert twins[0].stem == "01-a"
    assert len(twins[0].marked_seqs()) == 1
    draws = load_control_draws(tmp_path)
    assert [d.sample for d in draws] == [1, 2]
    assert all(d.stem == "01-a" for d in draws)


def test_instance_contrast_on_planted_shift(tmp_path: Path) -> None:
    def twin(stem: str, marked: list[int], unmarked: list[int]) -> Twin:
        return Twin(
            stem=stem,
            marked_text="m",
            unmarked_text="u",
            marked_ids=list(marked),
            unmarked_ids=list(unmarked),
        )

    train = [
        twin("t1", [10, 11, 12, 13], [10, 21, 22, 23]),
        twin("t2", [10, 11, 14, 15], [10, 21, 24, 25]),
        twin("t3", [10, 11, 16, 17], [10, 21, 26, 27]),
        twin("t4", [10, 11, 18, 19], [10, 21, 28, 29]),
        # Overlapping test stem: drop-from-train must remove it.
        twin("x1", [10, 11, 90, 91], [10, 21, 92, 93]),
    ]
    test = [
        twin("x1", [10, 11, 50, 51], [10, 21, 60, 61]),
        twin("x2", [10, 11, 52, 53], [10, 21, 62, 63]),
        twin("x3", [10, 11, 54, 55], [10, 21, 64, 65]),
    ]
    # Control looks like unmarked (other instance ≈ mixin off for this toy).
    control = [
        ControlDraw("x1", 1, [10, 21, 70, 71], "c"),
        ControlDraw("x2", 1, [10, 21, 72, 73], "c"),
        ControlDraw("x3", 1, [10, 21, 74, 75], "c"),
    ]
    run = run_instance_contrast(
        train,
        test,
        control,
        methods=("hits", "poshits"),
        fit_prefix=4,
        position_bucket=1,
    )
    assert run.used_keys is False
    assert run.n_aligned == 3
    assert run.transfer is not None
    assert run.transfer.n_train_prompts == 4
    names = {(m.name, m.comparison) for m in run.methods}
    assert ("poshits", "public-vs-unmarked") in names
    assert ("poshits", "control-vs-unmarked") in names
    assert ("poshits", "public-vs-control") in names
    pub = next(
        m for m in run.methods if m.name == "poshits" and m.comparison == "public-vs-unmarked"
    )
    ctrl = next(
        m
        for m in run.methods
        if m.name == "poshits" and m.comparison == "control-vs-unmarked"
    )
    vs = next(
        m
        for m in run.methods
        if m.name == "poshits" and m.comparison == "public-vs-control"
    )
    pub_auc = binary_eval(pub.holdout.marked_lrs, pub.holdout.unmarked_lrs, n_perm=20, seed=0)
    ctrl_auc = binary_eval(ctrl.holdout.marked_lrs, ctrl.holdout.unmarked_lrs, n_perm=20, seed=0)
    vs_auc = binary_eval(vs.holdout.marked_lrs, vs.holdout.unmarked_lrs, n_perm=20, seed=0)
    assert pub_auc.auc > 0.8
    assert ctrl_auc.auc < 0.7
    assert vs_auc.auc > 0.8
    persist_contrast(run, tmp_path)
    assert (tmp_path / "poshits-control-vs-unmarked" / "holdout.json").is_file()
    assert logodds_brier([2.0], [-2.0]) < 0.2


def test_instance_contrast_requires_aligned_control() -> None:
    def twin(stem: str, marked: list[int], unmarked: list[int]) -> Twin:
        return Twin(
            stem=stem,
            marked_text="m",
            unmarked_text="u",
            marked_ids=list(marked),
            unmarked_ids=list(unmarked),
        )

    train = [
        twin("t1", [10, 11, 12, 13], [10, 21, 22, 23]),
        twin("t2", [10, 11, 14, 15], [10, 21, 24, 25]),
    ]
    test = [twin("x1", [10, 11, 50, 51], [10, 21, 60, 61])]
    control = [ControlDraw("other", 1, [10, 21, 70, 71], "c")]
    with pytest.raises(ValueError, match="aligned"):
        run_instance_contrast(
            train,
            test,
            control,
            methods=("hits",),
            fit_prefix=4,
            position_bucket=1,
        )


def test_cli_contrast_help_mentions_instance(capsys) -> None:
    try:
        main(["contrast", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    out = capsys.readouterr().out
    assert "control-shuffled" in out
    assert "instance-specific" in out
    assert "Claude" in out
