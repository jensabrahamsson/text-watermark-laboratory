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


def _contrast_hold(name: str, slug: str):
    from text_watermark_tools.indicator import holdout_from_json

    root = Path(__file__).resolve().parents[1] / "experiments" / name
    return holdout_from_json(root / slug / "holdout.json")


def test_poshits_four_token_contrast_is_instance_specific() -> None:
    pub = _contrast_hold(
        "2026-08-31-contrast-36x4-to-12x4-fitprefix4",
        "poshits-public-vs-unmarked",
    )
    ctrl = _contrast_hold(
        "2026-08-31-contrast-36x4-to-12x4-fitprefix4",
        "poshits-control-vs-unmarked",
    )
    vs = _contrast_hold(
        "2026-08-31-contrast-36x4-to-12x4-fitprefix4",
        "poshits-public-vs-control",
    )
    hits_ctrl = _contrast_hold(
        "2026-08-31-contrast-36x4-to-12x4-fitprefix4",
        "hits-control-vs-unmarked",
    )
    hashed = _contrast_hold(
        "2026-08-31-contrast-36x4-to-12x4-fitprefix4",
        "hashpool-control-vs-unmarked",
    )
    assert pub.used_keys is False
    assert ctrl.used_keys is False
    assert vs.used_keys is False
    assert pub.n_prompts_marked_above == 12
    assert pub.n_marked_positive == 39
    assert pub.n_unmarked_nonpositive == 41
    assert ctrl.n_marked_positive == 0
    assert hits_ctrl.n_marked_positive == 0
    assert hashed.n_marked_positive == 6
    assert vs.n_prompts_marked_above == 12
    assert vs.n_unmarked_nonpositive == 48
    pub_auc = binary_eval(pub.marked_lrs, pub.unmarked_lrs, n_perm=200, seed=0)
    ctrl_auc = binary_eval(ctrl.marked_lrs, ctrl.unmarked_lrs, n_perm=200, seed=0)
    vs_auc = binary_eval(vs.marked_lrs, vs.unmarked_lrs, n_perm=200, seed=0)
    assert pub_auc.auc > 0.85
    assert 0.45 < ctrl_auc.auc < 0.58
    assert vs_auc.auc > 0.85


def test_unbucketed_hits_on_full_files_is_not_the_instance_sign() -> None:
    pos = _contrast_hold(
        "2026-08-31-contrast-36x4-to-12x4-full",
        "poshits-control-vs-unmarked",
    )
    hits = _contrast_hold(
        "2026-08-31-contrast-36x4-to-12x4-full",
        "hits-control-vs-unmarked",
    )
    vs = _contrast_hold(
        "2026-08-31-contrast-36x4-to-12x4-full",
        "hits-public-vs-control",
    )
    assert pos.n_marked_positive == 0
    assert hits.n_marked_positive == 29
    hits_auc = binary_eval(hits.marked_lrs, hits.unmarked_lrs, n_perm=200, seed=0)
    vs_auc = binary_eval(vs.marked_lrs, vs.unmarked_lrs, n_perm=200, seed=0)
    assert 0.40 < hits_auc.auc < 0.55
    assert vs_auc.auc > 0.80


def test_pair_limit_hits_separates_instances_on_full_files() -> None:
    vs = _contrast_hold(
        "2026-08-31-contrast-36x4-to-limit-full",
        "hits-public-vs-control",
    )
    ctrl = _contrast_hold(
        "2026-08-31-contrast-36x4-to-limit-full",
        "hits-control-vs-unmarked",
    )
    pos = _contrast_hold(
        "2026-08-31-contrast-36x4-to-limit-fitprefix4",
        "poshits-control-vs-unmarked",
    )
    assert vs.used_keys is False
    assert vs.n_prompts_marked_above == 12
    vs_auc = binary_eval(vs.marked_lrs, vs.unmarked_lrs, n_perm=200, seed=0)
    ctrl_auc = binary_eval(ctrl.marked_lrs, ctrl.unmarked_lrs, n_perm=200, seed=0)
    assert vs_auc.auc >= 0.999
    assert 0.45 < ctrl_auc.auc < 0.65
    assert pos.n_marked_positive == 0


def test_controlkeys_official_lamp_is_other_instance() -> None:
    import json

    root = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-31-pair-12x4-controlkeys"
    data = json.loads((root / "results.json").read_text())
    assert data["control_only"] is True
    pubs: list[float] = []
    matches: list[float] = []
    for row in data["rows"]:
        pubs.append(row["control_gen_public"]["mean"])
        matches.append(row["control_gen_matching"]["mean"])
        for extra in row.get("extra_control", []):
            pubs.append(extra["public"]["mean"])
            matches.append(extra["matching"]["mean"])
    assert len(pubs) == 48
    assert all(abs(x - 0.5) < 0.04 for x in pubs)
    assert all(m > 0.58 for m in matches)
    assert all(m > p for m, p in zip(matches, pubs, strict=True))
