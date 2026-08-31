"""Drive the real CLI entry on shipped lab files."""

from pathlib import Path

from text_watermark_tools.cli import build_parser, main

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "experiments" / "2026-08-15-gpt2-sonnet5"
GROK_PROMPTS = ROOT / "experiments" / "2026-08-17-grok-prompts"


def _mean_on_line(line: str) -> float:
    return float(line.split("mean=")[1].split()[0])


def _official_line(out: str, needle: str | None = None) -> str:
    for line in out.splitlines():
        if "instance=public-deepmind-30" not in line:
            continue
        if needle is None or needle in line:
            return line
    raise AssertionError(f"no official-instance row for {needle!r} in:\n{out}")


def _control_line(out: str, needle: str | None = None) -> str:
    for line in out.splitlines():
        if "instance=control-shuffled-30" not in line:
            continue
        if needle is None or needle in line:
            return line
    raise AssertionError(f"no control-instance row for {needle!r} in:\n{out}")


def test_cli_score_marked_prints_counts(capsys) -> None:
    rc = main(["score", str(LAB / "t_high_temp.txt")])
    assert rc == 0
    out = capsys.readouterr().out
    assert "mean=" in out
    assert "weighted_mean=" in out
    assert "n_tokens=" in out
    assert "n_unmasked_ngrams=" in out
    assert "instance=public-deepmind-30" in out
    assert "ngram_len=5" in out
    mean = float(out.split("mean=")[1].split()[0])
    assert mean > 0.55


def test_cli_score_grok_prompt_near_half(capsys) -> None:
    rc = main(["score", str(GROK_PROMPTS / "01-harbour.txt")])
    assert rc == 0
    out = capsys.readouterr().out
    mean = float(out.split("mean=")[1].split()[0])
    assert "instance=public-deepmind-30" in out
    assert abs(mean - 0.5) < 0.05


def test_cli_score_rewrite_near_half(capsys) -> None:
    rc = main(["score", str(LAB / "t_prime_sonnet5.txt")])
    assert rc == 0
    out = capsys.readouterr().out
    assert "instance=public-deepmind-30" in out
    assert "ngram_len=5" in out
    mean = float(out.split("mean=")[1].split()[0])
    assert abs(mean - 0.5) < 0.03


def test_cli_score_control_contrasts_same_marked_file(capsys) -> None:
    marked = str(LAB / "t_high_temp.txt")
    rc = main(["score", marked, "--control-shuffled-keys"])
    assert rc == 0
    out = capsys.readouterr().out
    official = _mean_on_line(_official_line(out, "t_high_temp.txt"))
    control = _mean_on_line(_control_line(out, "t_high_temp.txt"))
    assert official > 0.55
    assert abs(control - 0.5) < 0.05


def test_cli_iterate_without_deepseek_key_exits_2(
    tmp_path, capsys, monkeypatch
) -> None:
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("TEXT_WATERMARK_KEY_DIR", str(tmp_path))
    rc = main(["iterate", str(LAB / "t_high_temp.txt")])
    assert rc == 2
    err = capsys.readouterr().err
    assert "DEEPSEEK_API_KEY" in err
    assert "DEEPSEEK-KEY.conf" in err


def test_cli_iterate_help_mentions_polish_and_indicate_stop(capsys) -> None:
    try:
        build_parser().parse_args(["iterate", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected --help SystemExit")
    out = capsys.readouterr().out
    flat = " ".join(out.split())
    assert "polish" in out
    assert "sounds better" in flat
    assert "--stop-on" in out
    assert "indicate" in out
    assert "not official score" in flat
    assert "not a remover" in flat.lower()


def test_cli_probe_help_mentions_auc_grain(capsys) -> None:
    try:
        build_parser().parse_args(["probe", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected --help SystemExit")
    out = capsys.readouterr().out
    assert "key-free" in out.lower()
    assert "Not detector_mean" in out
    assert "--pivot" in out
    try:
        build_parser().parse_args(["indicate", "holdout", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("expected --help SystemExit")
    out = capsys.readouterr().out
    assert "leave-one-out" in out.lower()
    assert "--rotate" in out


def test_cli_iterate_indicate_stop_without_tables_exits_2(
    tmp_path, capsys, monkeypatch
) -> None:
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("TEXT_WATERMARK_KEY_DIR", str(tmp_path))
    rc = main(
        [
            "iterate",
            str(LAB / "t_high_temp.txt"),
            "--stop-on",
            "indicate",
        ]
    )
    assert rc == 2
    err = capsys.readouterr().err
    assert "--tables" in err
    assert "not official score" in err


def test_cli_iterate_qwen_without_key_exits_2(tmp_path, capsys, monkeypatch) -> None:
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.setenv("TEXT_WATERMARK_KEY_DIR", str(tmp_path))
    rc = main(["iterate", str(LAB / "t_high_temp.txt"), "--backend", "qwen"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "DASHSCOPE_API_KEY" in err
    assert "DASHSCOPE-KEY.conf" in err


def test_cli_pair_same_prompt_prints_both_twins(tmp_path, capsys) -> None:
    prompt = tmp_path / "harbour.txt"
    prompt.write_text("The harbour lights flickered over wet cobblestones. ")
    out_dir = tmp_path / "pair-out"
    rc = main(
        [
            "pair",
            str(prompt),
            "--max-new-tokens",
            "64",
            "--seed",
            "2",
            "--out-dir",
            str(out_dir),
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    marked = _mean_on_line(_official_line(out, "harbour-marked"))
    unmarked = _mean_on_line(_official_line(out, "harbour-unmarked-gen"))
    assert marked > 0.5
    assert marked > unmarked
    assert (out_dir / "harbour-marked.txt").is_file()


def test_cli_score_directory_prints_one_row_per_txt(capsys) -> None:
    rc = main(["score", str(LAB)])
    assert rc == 0
    out = capsys.readouterr().out
    rows = [line for line in out.splitlines() if "mean=" in line]
    assert len(rows) >= 2
    marked = _mean_on_line(_official_line(out, "t_high_temp.txt"))
    rewritten = _mean_on_line(_official_line(out, "t_prime_sonnet5.txt"))
    assert marked > 0.55
    assert abs(rewritten - 0.5) < 0.03
    assert "instance=public-deepmind-30" in _official_line(out, "t_high_temp.txt")
    assert "ngram_len=5" in _official_line(out, "t_prime_sonnet5.txt")
