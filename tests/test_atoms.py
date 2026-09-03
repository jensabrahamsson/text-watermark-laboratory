"""Interpolate atom dump: not a new scorer."""

import json
from pathlib import Path

from text_watermark_tools.atoms import window_atom_summary
from text_watermark_tools.blind import Twin
from text_watermark_tools.cli import main
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    fit_count_model,
    interpolate_trace,
    score_sequence,
)

ROOT = Path(__file__).resolve().parents[1]
ATOMS = (
    ROOT
    / "experiments"
    / "2026-09-01-atoms-100x4-to-grok12x4-interpolate"
    / "atoms.json"
)
PROTOCOL_WINDOWS = ROOT / "research" / "PROTOCOL-isolated-windows.md"
ATOMS_GROK36_TO_12 = (
    ROOT
    / "experiments"
    / "2026-09-01-atoms-grok36x4-to-12x4-interpolate"
    / "atoms.json"
)
ATOMS_GROK36_TO_GROK12 = (
    ROOT
    / "experiments"
    / "2026-09-01-atoms-grok36x4-to-grok12x4-interpolate"
    / "atoms.json"
)
PROTOCOL_SCALE = ROOT / "research" / "PROTOCOL-isolated-scale.md"


def _twin(stem: str, marked: list[int], unmarked: list[int]) -> Twin:
    return Twin(
        stem=stem,
        marked_text="m",
        unmarked_text="u",
        marked_ids=list(marked),
        unmarked_ids=list(unmarked),
    )


def test_interpolate_trace_skips_first_and_matches_lr() -> None:
    twins = [
        _twin("a", [1, 2, 3, 4, 5], [1, 9, 9, 9, 9]),
        _twin("b", [1, 2, 3, 4, 6], [1, 8, 8, 8, 8]),
        _twin("c", [1, 2, 3, 4, 5], [1, 7, 7, 7, 7]),
    ]
    model = fit_count_model(twins, context_len=4)
    assert model.used_keys is False
    spec = COUNT_SPECS["interpolate"]
    seq = [1, 2, 3, 4, 5]
    hits = interpolate_trace(seq, model, spec)
    assert [h.i for h in hits] == [1, 2, 3, 4]
    lr = score_sequence(seq, model, spec)
    mean = sum(h.delta for h in hits) / len(hits)
    assert abs(mean - lr) < 1e-9


def test_window_summary_separates_head_and_tail() -> None:
    rows = [
        {
            "side": "marked",
            "hits": [
                {
                    "i": 2,
                    "ctx": {"tokens": ["The"]},
                    "next": " car",
                    "delta": 0.5,
                    "unseen_next": False,
                },
                {
                    "i": 40,
                    "ctx": {"tokens": [" the"]},
                    "next": " night",
                    "delta": 0.4,
                    "unseen_next": False,
                },
            ],
        },
        {
            "side": "unmarked",
            "hits": [
                {
                    "i": 40,
                    "ctx": {"tokens": [" the"]},
                    "next": " night",
                    "delta": -0.2,
                    "unseen_next": False,
                }
            ],
        },
    ]
    wins = window_atom_summary(rows, windows=((0, 4), (32, 64)), top_k=5)
    by = {(w["start"], w["end"]): w for w in wins}
    assert by[(0, 4)]["n_marked"] == 1
    assert by[(32, 64)]["n_marked"] == 1
    assert by[(32, 64)]["mean_marked_delta"] > by[(32, 64)]["mean_unmarked_delta"]
    top = by[(32, 64)]["top_marked_positive_seen"]
    assert top[0]["next"] == " night"
    assert top[0]["n"] == 1


def test_loo_interpolate_atoms_does_not_pool_the_held_out_family() -> None:
    twins = [
        _twin("a", [1, 2, 3, 4, 5], [1, 9, 9, 9, 9]),
        _twin("b", [1, 2, 3, 4, 6], [1, 8, 8, 8, 8]),
        _twin("c", [1, 2, 3, 4, 5], [1, 7, 7, 7, 7]),
    ]
    from text_watermark_tools.atoms import (
        _interpolate_atom_rows,
        _interpolate_atoms_payload,
        decode_token,
    )
    from text_watermark_tools.score import load_tokenizer
    from text_watermark_tools.transfer import COUNT_SPECS, fit_count_model

    spec = COUNT_SPECS["interpolate"]
    tok = load_tokenizer("gpt2")
    decode = lambda t, tokenizer=tok: decode_token(tokenizer, t)
    rows = []
    for held in twins:
        train = [t for t in twins if t.stem != held.stem]
        model = fit_count_model(train, context_len=4)
        assert model.used_keys is False
        rows.extend(_interpolate_atom_rows([held], model, decode=decode, spec=spec))
    payload = _interpolate_atoms_payload(
        rows,
        ((0, 4), (4, 16)),
        top_k=5,
        store_rows=False,
        note="test",
        mode="leave-one-family-out",
    )
    assert payload["mode"] == "leave-one-family-out"
    assert payload["used_keys"] is False
    assert payload["n_rows"] == 6
    assert "rows" not in payload
    assert len(payload["files"]) == 6
    pooled = fit_count_model(twins, context_len=4)
    pooled_rows = _interpolate_atom_rows(twins, pooled, decode=decode, spec=spec)
    loo_lrs = [r["lr"] for r in rows]
    pooled_lrs = [r["lr"] for r in pooled_rows]
    assert loo_lrs != pooled_lrs


def test_cli_atoms_help_is_not_a_new_scorer(capsys) -> None:
    try:
        main(["atoms", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    out = capsys.readouterr().out
    assert "not a new scorer" in out.lower()
    assert "detector_mean" in out
    assert "--leave-one-out" in out


def test_cli_atoms_leave_one_out_rejects_pooled_tables(capsys) -> None:
    code = main(
        [
            "atoms",
            "experiments/tables-counts",
            "--leave-one-out",
            "--test-dir",
            "experiments/pair",
        ]
    )
    assert code == 2
    err = capsys.readouterr().err
    assert "leaks" in err.lower()


def test_live_grok12_atoms_are_backoff_not_a_detector() -> None:
    raw = json.loads(ATOMS.read_text())
    assert raw["used_keys"] is False
    assert raw["used_hash_iv"] is False
    assert raw["used_g_values"] is False
    assert "rows" not in raw
    assert raw["n_rows"] == 96
    assert raw["n_marked_lr_positive"] == 27
    by = {(int(w["start"]), int(w["end"])): w for w in raw["windows"]}
    head = by[(0, 4)]
    mid = by[(16, 32)]
    tail = by[(64, 128)]
    assert head["n_unseen"] > head["n_seen"]
    assert mid["n_unseen"] > 10 * max(mid["n_seen"], 1)
    assert tail["n_unseen"] > 10 * max(tail["n_seen"], 1)
    assert tail["n_unseen"] == 5924
    assert tail["n_seen"] == 214
    # Opening ranking is unmarked more negative, not occupancy-free TPs.
    assert head["mean_unmarked_delta"] < head["mean_marked_delta"]
    assert head["mean_unmarked_delta"] < -0.3
    top = head["top_marked_positive_seen"]
    assert top[0]["next"] == " car"
    assert top[0]["ctx"] == ["The"]
    assert top[0]["n"] == 19
    text = PROTOCOL_WINDOWS.read_text()
    assert "2026-09-01-atoms-100x4-to-grok12x4-interpolate" in text
    assert "Witten–Bell" in text or "Witten-Bell" in text
    assert "Does not replace **25/48**" in text or "does not replace **25/48**" in text.lower()


def _by_window(raw: dict) -> dict[tuple[int, int], dict]:
    return {(int(w["start"]), int(w["end"])): w for w in raw["windows"]}


def test_live_grok36_to_12_atoms_are_not_occupancy_free_26() -> None:
    raw = json.loads(ATOMS_GROK36_TO_12.read_text())
    assert raw["used_keys"] is False
    assert raw["used_hash_iv"] is False
    assert raw["used_g_values"] is False
    assert "rows" not in raw
    assert raw["n_rows"] == 96
    assert raw["n_marked_lr_positive"] == 29
    by = _by_window(raw)
    head = by[(0, 4)]
    tail = by[(64, 128)]
    assert head["n_unseen"] > head["n_seen"]
    assert head["n_seen"] == 69
    assert head["n_unseen"] == 219
    assert tail["n_unseen"] == 5996
    assert tail["n_seen"] == 137
    assert tail["n_unseen"] > 10 * max(tail["n_seen"], 1)
    assert head["mean_unmarked_delta"] < 0.0
    assert head["mean_marked_delta"] > head["mean_unmarked_delta"]
    top = head["top_marked_positive_seen"]
    assert top[0]["ctx"] == ["Cl"]
    assert top[0]["next"] == "osing"
    assert top[0]["n"] == 4
    cov = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-01-openings-grok36x4-to-12x4"
            / "coverage.json"
        ).read_text()
    )
    zeros = " ".join(
        z["opening_text"] for z in cov["final"]["postokhits"]["zeros"]
    )
    assert "Closing is the" in zeros
    assert cov["final"]["postokhits"]["n_covered"] == 10
    text = PROTOCOL_SCALE.read_text()
    assert "2026-09-01-atoms-grok36x4-to-12x4-interpolate" in text
    assert "unbucketed" in text
    assert "Does not replace **25/48**" in text


def test_live_grok36_to_grok12_atoms_track_opening_overlap() -> None:
    raw = json.loads(ATOMS_GROK36_TO_GROK12.read_text())
    assert raw["used_keys"] is False
    assert "rows" not in raw
    assert raw["n_rows"] == 96
    assert raw["n_marked_lr_positive"] == 39
    by = _by_window(raw)
    head = by[(0, 4)]
    tail = by[(64, 128)]
    assert head["n_seen"] == 119
    assert head["n_unseen"] == 169
    assert head["mean_marked_delta"] > 2.0
    assert head["mean_marked_delta"] > head["mean_unmarked_delta"]
    top = head["top_marked_positive_seen"]
    assert top[0]["ctx"] == ["The"]
    assert top[0]["next"] == " car"
    assert top[0]["n"] == 19
    assert tail["n_unseen"] == 5955
    assert tail["n_seen"] == 183
    assert tail["n_unseen"] > 10 * max(tail["n_seen"], 1)
    cov = json.loads(
        (
            ROOT
            / "experiments"
            / "2026-09-01-openings-grok36x4-to-grok12x4"
            / "coverage.json"
        ).read_text()
    )
    assert cov["final"]["postokhits"]["n_covered"] == 39
    text = PROTOCOL_SCALE.read_text()
    assert "2026-09-01-atoms-grok36x4-to-grok12x4-interpolate" in text
    assert "The car" in text
    assert "Does not replace **25/48**" in text
