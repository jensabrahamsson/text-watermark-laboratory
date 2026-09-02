"""Tests specifically verifying probe.py components and helpers to guarantee 100% coverage before refactoring."""

from __future__ import annotations

import json
from pathlib import Path
import pytest
import torch

from text_watermark_tools.blind import Twin
from text_watermark_tools.indicator import IndicatorHoldout
from text_watermark_tools.probe import (
    MethodSummary,
    ProbeRun,
    ThresholdRow,
    TransferRun,
    ScrubRow,
    ScrubRun,
    _parse_prefix_lens,
    _parse_windows,
    _window_dir,
    clip_seq,
    slice_seq,
    scrub_token_ids,
    print_scrub,
    persist_scrub,
    print_coverage,
    persist_coverage,
    format_cascade,
    _cascade_json,
    _ranking_without_tp_md,
    summarize_holdout,
    swap_twin_sides,
    shuffle_twin_sides,
    _empty_holdout_parts,
    _holdout_from_parts,
    _append_pair,
    print_probe,
    persist_probe,
    print_transfer,
    persist_transfer,
    combine_holdouts_logit,
)
from text_watermark_tools.stats import binary_eval


def test_parse_prefix_lens_and_windows() -> None:
    assert _parse_prefix_lens(None) == ()
    assert _parse_prefix_lens([]) == ()
    assert _parse_prefix_lens([16, 32, 64]) == (16, 32, 64)
    assert _parse_prefix_lens([16, 16, 32]) == (16, 32)
    assert _parse_prefix_lens([-1, 0, 16]) == (16,)

    assert _parse_windows(None) == ()
    assert _parse_windows([]) == ()
    assert _parse_windows(["0:16", "16:32"]) == ((0, 16), (16, 32))
    assert _parse_windows([(0, 16), (16, 32)]) == ((0, 16), (16, 32))
    # Negative / inverted windows are ignored with continue
    assert _parse_windows(["16:16", "32:16", "0:8"]) == ((0, 8),)
    with pytest.raises(ValueError, match="must look like start:end"):
        _parse_windows(["invalid"])

    assert _window_dir(0, 16) == "window-0-16"


def test_clip_seq_and_slice_seq() -> None:
    seq = [10, 20, 30, 40, 50]
    assert clip_seq(seq, 3) == [10, 20, 30]
    assert clip_seq(seq, 0) == seq
    assert clip_seq(seq, -1) == seq
    assert clip_seq(seq, 10) == seq

    assert slice_seq(seq, 1, 4) == [20, 30, 40]
    assert slice_seq(seq, 0, 2) == [10, 20]
    assert slice_seq(seq, 4, 1) == []
    assert slice_seq(seq, -1, 3) == []
    assert slice_seq("hello world", 0, 5) == "hello"


def test_scrub_token_ids_and_scrub_run(tmp_path: Path) -> None:
    # Dummy logits tensor for 3 tokens and vocab of 5 tokens
    logits = torch.tensor([
        [10.0, 5.0, 1.0, 0.0, 0.0],  # argmax 0 != 1 -> snap to 0
        [1.0, 2.0, 10.0, 0.0, 0.0],  # argmax 2 == 2 -> keep 2
        [0.0, 1.0, 2.0, 3.0, 10.0],  # argmax 4 != 3 -> snap to 4
    ], dtype=torch.float32)
    snapped, n_flips = scrub_token_ids([1, 2, 3], lm=None, logits=logits, top_k=4)
    # ids[0] stays 1; ids[1] snaps from 2 to 0; ids[2] snaps from 3 to 2
    assert snapped == [1, 0, 2]
    assert n_flips == 2

    row = ScrubRow(
        path=str(tmp_path / "test.txt"),
        n_tokens=100,
        n_flips=15,
        mean_before=0.62,
        weighted_before=0.64,
        mean_after=0.51,
        weighted_after=0.50,
        used_keys_for_snap=False,
    )
    run = ScrubRun(
        rows=[row],
        model_name="gpt2",
        instance="public-deepmind-30",
        used_keys_for_snap=False,
        used_hash_iv=False,
        used_g_values=False,
    )
    txt = print_scrub(run)
    assert "scrub n_files=1" in txt
    assert "mean official before=0.6200 after=0.5100" in txt

    out_dir = tmp_path / "scrub_out"
    persist_scrub(run, out_dir)
    assert (out_dir / "results.json").exists()
    assert (out_dir / "results.md").exists()
    data = json.loads((out_dir / "results.json").read_text())
    assert data["model_name"] == "gpt2"
    assert len(data["rows"]) == 1


def test_coverage_reporting(tmp_path: Path) -> None:
    raw = {
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "n_prompts": 2,
        "n_files": 4,
        "context_len": 4,
        "position_bucket": 16,
        "by_window": [
            {
                "start": 0,
                "end": 16,
                "shared_frac": 0.125,
                "shared": 10,
                "n": 80,
                "mean_shared_support": 1.5,
            }
        ],
    }
    rendered = print_coverage(raw)
    assert "coverage n_prompts=2" in rendered
    assert "0:16" in rendered

    out_dir = tmp_path / "cov_out"
    persist_coverage(raw, out_dir)
    assert (out_dir / "coverage.json").exists()
    assert (out_dir / "coverage.md").exists()


def test_cascade_format_and_json() -> None:
    summary = {
        "count_method": "postokhits",
        "fallback": "rankpath",
        "cascade_when": "positive",
        "pivot_weight": 0.0,
        "prompt_context": False,
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "count_precision": 1.0,
        "n_count_marked": 16,
        "n_count_unmarked": 0,
        "n_pivot_marked": 32,
        "n_pivot_unmarked": 48,
        "prompt_accuracy": 0.9,
        "n_prompts": 12,
        "n_files": 96,
        "auc": 0.85,
        "isolated_marked_positive": 24,
        "isolated_unmarked_nonpositive": 40,
        "n_marked_wins": 10,
        "n_unmarked_wins": 2,
        "n_ties": 0,
    }
    lines = format_cascade(summary)
    assert any("Cascade: count LR" in line for line in lines)
    payload = _cascade_json(summary)
    assert payload["count_method"] == "postokhits"
    assert payload["fallback"] == "rankpath"


def test_twin_transformations() -> None:
    t = Twin(
        stem="stem1",
        marked_text="marked text",
        unmarked_text="unmarked text",
        marked_ids=[1, 2, 3],
        unmarked_ids=[4, 5, 6],
        extra_marked_ids=[[7, 8]],
        extra_unmarked_ids=[[9, 10]],
        extra_marked_text=["m2"],
        extra_unmarked_text=["u2"],
        prompt_text="prompt",
        prompt_ids=[100],
    )
    swapped = swap_twin_sides(t)
    assert swapped.marked_ids == [4, 5, 6]
    assert swapped.unmarked_ids == [1, 2, 3]
    assert swapped.extra_marked_ids == [[9, 10]]
    assert swapped.extra_unmarked_ids == [[7, 8]]

    shuffled = shuffle_twin_sides([t], seed=42)
    assert len(shuffled) == 1
    assert isinstance(shuffled[0], Twin)


def test_holdout_parts_and_helpers() -> None:
    parts = _empty_holdout_parts()
    assert "stems" in parts
    assert "marked" in parts
    _append_pair(parts, stem="s1", sample=1, marked=1.0, unmarked=-1.0)
    assert len(parts["marked"]) == 1
    assert len(parts["stems"]) == 1

    ev = _holdout_from_parts(
        parts,
        model_name="test_m",
        instance="test_inst",
        score_kind="test_kind",
        context_len=4,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )
    assert ev.n_prompts == 1
    assert ev.n_files == 2
    assert ev.n_marked_positive == 1

    s = summarize_holdout("test_meth", ev)
    assert s.name == "test_meth"
    assert s.n_prompt_wins == 1
    assert s.n_prompts == 1


def test_ranking_without_tp_md() -> None:
    ev = IndicatorHoldout(
        stems=["stem1", "stem2"],
        marked_lrs=[0.1, -0.2],
        unmarked_lrs=[-0.5, 0.4],
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        context_len=4,
        model_name="m",
        instance="i",
        score_kind="k",
    )
    s = summarize_holdout("hits", ev)
    lines = _ranking_without_tp_md([s])
    assert any("ranking wins with no isolated TP" in line for line in lines)


def test_probe_and_transfer_persistence(tmp_path: Path) -> None:
    ev = IndicatorHoldout(
        stems=["stem1"],
        marked_lrs=[0.8],
        unmarked_lrs=[-0.4],
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        context_len=4,
        model_name="gpt2",
        instance="i",
        score_kind="k",
    )
    s = summarize_holdout("hits", ev)
    probe_run = ProbeRun(
        pair_dir=str(tmp_path / "pair"),
        model_name="gpt2",
        context_len=4,
        methods=[s],
    )
    text = print_probe(probe_run)
    assert "probe" in text
    assert "hits" in text

    persist_probe(probe_run, tmp_path / "probe_out")
    assert (tmp_path / "probe_out" / "results.json").exists()
    assert (tmp_path / "probe_out" / "results.md").exists()
    assert (tmp_path / "probe_out" / "hits" / "holdout.json").exists()

    transfer_run = TransferRun(
        train_dir=str(tmp_path / "train"),
        test_dir=str(tmp_path / "test"),
        model_name="gpt2",
        context_len=4,
        methods=[s],
    )
    transfer_text = print_transfer(transfer_run)
    assert "transfer" in transfer_text
    persist_transfer(transfer_run, tmp_path / "transfer_out")
    assert (tmp_path / "transfer_out" / "results.json").exists()
    assert (tmp_path / "transfer_out" / "results.md").exists()


def test_combine_holdouts_logit() -> None:
    ev1 = IndicatorHoldout(
        stems=["s1", "s2"],
        marked_lrs=[0.5, 0.2],
        unmarked_lrs=[-0.2, -0.4],
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        context_len=4,
        model_name="gpt2",
        instance="i",
        score_kind="k",
    )
    ev2 = IndicatorHoldout(
        stems=["s1", "s2"],
        marked_lrs=[0.8, 0.4],
        unmarked_lrs=[-0.5, -0.6],
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        context_len=4,
        model_name="gpt2",
        instance="i",
        score_kind="k",
    )
    tr_comb, te_comb = combine_holdouts_logit(
        train_holdouts=[ev1, ev2],
        test_holdouts=[ev1, ev2],
        model_name="gpt2",
    )
    assert tr_comb.n_prompts == 2
    assert tr_comb.used_keys is False
    assert tr_comb.score_kind == "logit"
    assert te_comb.score_kind == "logit"


def test_scorer_calling_and_prefix_helpers() -> None:
    from text_watermark_tools.probe import _twin_prefix, _call_scorer, _bound_ids_scorer

    twin = Twin(
        stem="stem1",
        marked_text="m",
        unmarked_text="u",
        marked_ids=[1, 2],
        unmarked_ids=[3, 4],
        prompt_text="p",
        prompt_ids=[10, 20],
    )
    assert _twin_prefix(twin, False) == ()
    assert _twin_prefix(twin, True) == (10, 20)

    # Scorer accepting prefix and score_span
    def custom_scorer(seq, *, prefix=(), score_span=None):
        val = sum(seq) + sum(prefix)
        if score_span:
            val += score_span[0] + score_span[1]
        return float(val)

    assert _call_scorer(custom_scorer, [1, 2], prefix=[10], score_span=(0, 2)) == 15.0

    def custom_multiplier(seq, multiplier, *, prefix=(), score_span=None):
        val = (sum(seq) + sum(prefix)) * multiplier
        if score_span:
            val += score_span[0] + score_span[1]
        return float(val)

    bound = _bound_ids_scorer(custom_multiplier, 2)
    assert bound([2, 3], prefix=[5]) == 20.0
    assert bound([2, 3]) == 10.0


def test_store_prefixes_and_windows_and_thresholds() -> None:
    from text_watermark_tools.probe import (
        _store_prefixes,
        _store_windows,
        _append_threshold,
        nested_stem_gates,
    )

    ev = IndicatorHoldout(
        stems=["s1", "s2"],
        marked_lrs=[0.5, -0.1],
        unmarked_lrs=[-0.4, 0.2],
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        context_len=4,
        model_name="gpt2",
    )
    pref_dest: dict[int, list[MethodSummary]] = {}
    _store_prefixes(pref_dest, {16: {"hits": ev}})
    assert 16 in pref_dest
    assert pref_dest[16][0].name == "hits"

    win_dest: dict[tuple[int, int], list[MethodSummary]] = {}
    _store_windows(win_dest, {(0, 16): {"hits": ev}})
    assert (0, 16) in win_dest
    assert win_dest[(0, 16)][0].name == "hits"

    gates = nested_stem_gates(ev)
    assert "nested-youden-by-stem" in gates
    assert "nested-fpr10-by-stem" in gates

    tr_run = TransferRun()
    _append_threshold(tr_run, name="hits", source="in-sample-youden", threshold=0.0, test_ev=ev)
    assert len(tr_run.thresholds) == 1
    assert tr_run.thresholds[0].name == "hits"

