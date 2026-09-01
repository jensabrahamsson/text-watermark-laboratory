"""Single-text key-free indicator: fit, persist, load, score one file."""

from pathlib import Path

from text_watermark_tools.cli import main
from text_watermark_tools.indicator import (
    CAVEAT,
    INDICATOR_INSTANCE,
    IndicatorHoldout,
    fit_indicator,
    format_indicator,
    holdout_from_json,
    holdout_single_text,
    load_indicator,
    persist_holdout,
    persist_indicator,
    rotate_holdout,
    score_text,
    score_text_from_tables,
)
from text_watermark_tools.blind import load_twins
from text_watermark_tools.score import load_tokenizer

PAIR = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-17-pair"
PREMARK = (
    Path(__file__).resolve().parents[1] / "experiments" / "claude-premark-2026-08"
)


def test_load_twins_does_not_treat_claude_premark_as_pairs() -> None:
    try:
        load_twins(PREMARK)
    except FileNotFoundError as exc:
        msg = str(exc).lower()
        assert "twin" in msg or "marked" in msg
    else:
        raise AssertionError("pre-mark pile must not load as marked/unmarked twins")


def test_persist_load_same_lr_on_lab_twin(tmp_path: Path) -> None:
    twins = load_twins(PAIR)
    model = fit_indicator(twins, context_len=2)
    assert model.used_keys is False
    persist_indicator(model, tmp_path, model_name="gpt2", n_train_prompts=len(twins))
    loaded, meta = load_indicator(tmp_path)
    assert loaded.used_keys is False
    assert meta.model_name == "gpt2"
    tok = load_tokenizer("gpt2")
    text = twins[0].marked_text
    a = score_text(text, model, tokenizer=tok)
    b = score_text(text, loaded, tokenizer=tok)
    assert a == b


def test_cli_indicate_score_is_stable_and_key_free(tmp_path, capsys) -> None:
    tables = tmp_path / "tables"
    rc = main(
        [
            "indicate",
            "fit",
            str(PAIR),
            "--out-dir",
            str(tables),
            "--context-len",
            "2",
        ]
    )
    assert rc == 0
    fit_out = capsys.readouterr().out
    assert INDICATOR_INSTANCE in fit_out
    assert "used_keys=False" in fit_out
    assert "Not detector_mean" in fit_out
    assert "Not Claude" in fit_out

    held = PAIR / "03-library-marked.txt"
    rc = main(["indicate", "score", str(held), "--tables", str(tables)])
    assert rc == 0
    first = capsys.readouterr().out
    rc = main(["indicate", "score", str(held), "--tables", str(tables)])
    assert rc == 0
    second = capsys.readouterr().out
    assert first == second
    line = first.splitlines()[0]
    assert "lr=" in line
    assert "instance=key-free-counts" in line
    assert "used_keys=False" in line
    assert "not_detector_mean=true" in line
    assert "n_used=" in line
    assert CAVEAT in first


def test_cli_indicate_holdout_scores_each_file_alone(tmp_path, capsys) -> None:
    out = tmp_path / "hold"
    rc = main(
        [
            "indicate",
            "holdout",
            str(PAIR),
            "--hold",
            "01-harbour",
            "02-night-bus",
            "--context-len",
            "2",
            "--out-dir",
            str(out),
        ]
    )
    assert rc == 0
    printed = capsys.readouterr().out
    assert "n_files=4" in printed
    assert "marked_above_unmarked=" in printed
    assert "used_keys=False" in printed
    assert printed.count("instance=key-free-counts") >= 4
    ev = holdout_single_text(
        load_twins(PAIR),
        ["01-harbour", "02-night-bus"],
        context_len=2,
    )
    assert ev.n_files == 4
    assert ev.used_keys is False
    assert len(ev.marked_lrs) == 2
    assert len(ev.unmarked_lrs) == 2
    assert (out / "holdout.json").is_file()


def test_cli_indicate_fit_score_hashpool_is_key_free(tmp_path, capsys) -> None:
    tables = tmp_path / "hashpool"
    rc = main(
        [
            "indicate",
            "fit",
            str(PAIR),
            "--out-dir",
            str(tables),
            "--method",
            "hashpool",
            "--context-len",
            "2",
            "--n-hashes",
            "4",
            "--n-buckets",
            "32",
        ]
    )
    assert rc == 0
    fit_out = capsys.readouterr().out
    assert "instance=key-free-hashpool" in fit_out
    assert "used_keys=False" in fit_out
    held = PAIR / "03-library-marked.txt"
    rc = main(["indicate", "score", str(held), "--tables", str(tables)])
    assert rc == 0
    first = capsys.readouterr().out
    rc = main(["indicate", "score", str(held), "--tables", str(tables)])
    assert rc == 0
    second = capsys.readouterr().out
    assert first == second
    line = first.splitlines()[0]
    assert "lr=" in line
    assert "instance=key-free-hashpool" in line
    assert "score_kind=hashpool" in line
    assert "used_keys=False" in line
    tok = load_tokenizer("gpt2")
    lr, meta, used = score_text_from_tables(
        held.read_text(), tables, tokenizer=tok, score_mode="auto"
    )
    assert used is False
    assert meta.instance == "key-free-hashpool"
    assert "lr=" + f"{lr:.6f}" in line
    rc = main(
        [
            "indicate",
            "score",
            str(held),
            "--tables",
            str(tables),
            "--score-mode",
            "hashtok",
        ]
    )
    assert rc == 0
    tok_line = capsys.readouterr().out.splitlines()[0]
    assert "instance=key-free-hashtok" in tok_line
    assert "score_kind=hashtok" in tok_line
    assert "used_keys=False" in tok_line
    tok_lr, tok_meta, tok_used = score_text_from_tables(
        held.read_text(), tables, tokenizer=tok, score_mode="hashtok"
    )
    assert tok_used is False
    assert tok_meta.instance == "key-free-hashtok"
    assert tok_meta.score_kind == "hashtok"
    assert "lr=" + f"{tok_lr:.6f}" in tok_line


def test_cli_indicate_fit_score_surface_needs_no_tokenizer(tmp_path, capsys) -> None:
    tables = tmp_path / "surface"
    rc = main(
        [
            "indicate",
            "fit",
            str(PAIR),
            "--out-dir",
            str(tables),
            "--method",
            "surface",
            "--surface-context-len",
            "4",
            "--n-hashes",
            "4",
            "--n-buckets",
            "32",
        ]
    )
    assert rc == 0
    fit_out = capsys.readouterr().out
    assert "instance=key-free-surface" in fit_out
    assert "alphabet=bytes" in fit_out
    held = PAIR / "03-library-marked.txt"
    rc = main(["indicate", "score", str(held), "--tables", str(tables)])
    assert rc == 0
    line = capsys.readouterr().out.splitlines()[0]
    assert "instance=key-free-surface" in line
    assert "score_kind=surface" in line
    assert "used_keys=False" in line
    lr, meta, used = score_text_from_tables(held.read_text(), tables)
    assert used is False
    assert meta.instance == "key-free-surface"
    assert meta.score_kind == "surface"
    assert "lr=" + f"{lr:.6f}" in line


def test_cli_indicate_rotate_scores_each_prompt_file_alone(capsys) -> None:
    rc = main(
        [
            "indicate",
            "holdout",
            str(PAIR),
            "--rotate",
            "--context-len",
            "2",
        ]
    )
    assert rc == 0
    printed = capsys.readouterr().out
    assert "mode=rotate" in printed
    assert "n_prompts=3" in printed
    assert "n_files=6" in printed
    assert "used_keys=False" in printed
    ev = rotate_holdout(load_twins(PAIR), context_len=2)
    assert ev.mode == "rotate"
    assert ev.n_files == 6
    assert ev.n_prompts == 3
    assert ev.used_keys is False
    assert len(ev.stems) == 3


def test_holdout_margin_counts_a_close_miss() -> None:
    kwargs = dict(
        stems=["close", "wide"],
        marked_lrs=[0.01, 0.10],
        unmarked_lrs=[0.02, 0.00],
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        context_len=4,
        model_name="gpt2",
        mode="rotate",
    )
    strict = IndicatorHoldout(**kwargs, margin=0.0)
    soft = IndicatorHoldout(**kwargs, margin=0.015)
    assert strict.n_marked_above_unmarked == 1
    assert soft.n_marked_above_unmarked == 2
    assert strict.n_marked_positive == 2
    # 0.01 is > 0, still two; a slightly negative marked file:
    bar = IndicatorHoldout(
        **{**kwargs, "marked_lrs": [-0.01, 0.10], "unmarked_lrs": [0.02, 0.00]},
        margin=0.015,
    )
    assert bar.n_marked_positive == 2
    assert IndicatorHoldout(
        **{**kwargs, "marked_lrs": [-0.01, 0.10], "unmarked_lrs": [0.02, 0.00]},
        margin=0.0,
    ).n_marked_positive == 1


def test_holdout_from_json_can_retune_margin(tmp_path: Path) -> None:
    ev = IndicatorHoldout(
        stems=["close", "wide"],
        marked_lrs=[0.01, 0.10],
        unmarked_lrs=[0.02, 0.00],
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        context_len=4,
        model_name="gpt2",
        samples=[1, 1],
        mode="rotate",
        margin=0.0,
    )
    persist_holdout(ev, tmp_path)
    same = holdout_from_json(tmp_path / "holdout.json")
    assert same.n_marked_above_unmarked == 1
    soft = holdout_from_json(tmp_path / "holdout.json", margin=0.015)
    assert soft.n_marked_above_unmarked == 2
    assert soft.margin == 0.015


def test_format_indicator_abstains_when_coverage_is_zero() -> None:
    line = format_indicator(
        "file.txt",
        0.0,
        n_tokens=4,
        used_keys=False,
        n_used=0,
        n_positions=3,
        threshold=0.0,
        decision_source="nested-youden-poshits",
    )
    assert "n_used=0" in line
    assert "n_positions=3" in line
    assert "decision=ABSTAIN" in line
    assert "decision=unmarked" not in line
    assert "used_keys=False" in line
    covered = format_indicator(
        "file.txt",
        0.2,
        n_tokens=4,
        used_keys=False,
        n_used=2,
        n_positions=3,
        threshold=0.0,
    )
    assert "decision=marked" in covered
    assert "decision=ABSTAIN" not in covered


def test_format_indicator_abstains_on_occupancy_only() -> None:
    line = format_indicator(
        "file.txt",
        0.149,
        n_tokens=4,
        used_keys=False,
        score_kind="poshits",
        n_used=1,
        n_positions=3,
        n_observed=0,
        threshold=0.0,
    )
    assert "n_used=1" in line
    assert "n_observed=0" in line
    assert "occupancy_only=true" in line
    assert "decision=ABSTAIN" in line
    assert "decision=marked" not in line


def test_indicate_score_lock_b_tables_abstain_on_the_ferry_occupancy() -> None:
    tables = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-100x4-to-12x4-opening-poshits"
        / "tables-poshits"
    )
    pair = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-08-17-pair-12x4"
    )
    tok = load_tokenizer("gpt2")
    ferry = (pair / "01-harbour-marked.txt").read_text()
    lr, meta, used = score_text_from_tables(
        ferry, tables, tokenizer=tok, score_mode="auto"
    )
    assert used is False
    assert meta.score_kind == "poshits"
    assert meta.n_used == 1
    assert meta.n_observed == 0
    line = format_indicator(
        "01-harbour-marked.txt",
        lr,
        n_tokens=4,
        used_keys=used,
        instance=meta.instance,
        score_kind=meta.score_kind,
        n_used=meta.n_used,
        n_positions=meta.n_positions,
        n_observed=meta.n_observed,
        threshold=0.0,
    )
    assert "occupancy_only=true" in line
    assert "decision=ABSTAIN" in line
    tok_lr, tok_meta, tok_used = score_text_from_tables(
        ferry, tables, tokenizer=tok, score_mode="postokhits"
    )
    assert tok_used is False
    assert tok_meta.n_used == 0
    assert tok_lr == 0.0
    rain = (pair / "07-rain-marked.txt").read_text()
    rain_lr, rain_meta, rain_used = score_text_from_tables(
        rain, tables, tokenizer=tok, score_mode="auto"
    )
    assert rain_used is False
    assert rain_meta.n_observed is not None
    assert rain_meta.n_observed > 0
    rain_line = format_indicator(
        "07-rain-marked.txt",
        rain_lr,
        n_tokens=4,
        used_keys=rain_used,
        instance=rain_meta.instance,
        score_kind=rain_meta.score_kind,
        n_used=rain_meta.n_used,
        n_positions=rain_meta.n_positions,
        n_observed=rain_meta.n_observed,
        threshold=0.0,
    )
    assert "occupancy_only=true" not in rain_line
    assert "decision=ABSTAIN" not in rain_line


def test_indicate_score_auto_on_hashtoklen_tables_matches_explicit() -> None:
    tables = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix5-hashtoklen"
        / "tables-hashtoklen"
    )
    occupancy = (
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
    auto_lr, auto_meta, auto_used = score_text_from_tables(
        text, tables, tokenizer=tok, score_mode="auto"
    )
    explicit_lr, explicit_meta, explicit_used = score_text_from_tables(
        text, tables, tokenizer=tok, score_mode="hashtoklen"
    )
    assert auto_used is False
    assert explicit_used is False
    assert auto_meta.score_kind == "hashtoklen"
    assert explicit_meta.score_kind == "hashtoklen"
    assert auto_meta.instance == "key-free-hashtoklen"
    assert auto_lr == explicit_lr
    try:
        score_text_from_tables(
            text, tables, tokenizer=tok, score_mode="hashpool"
        )
    except ValueError as exc:
        assert "hashtoklen" in str(exc) or "Laplace" in str(exc)
    else:
        raise AssertionError("expected ValueError")
    try:
        score_text_from_tables(
            text, occupancy, tokenizer=tok, score_mode="hashtoklen"
        )
    except ValueError as exc:
        assert "exact_len" in str(exc)
    else:
        raise AssertionError("expected ValueError")

