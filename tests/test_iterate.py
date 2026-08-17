"""Iterate-until-chance uses the official scorer; rewrite is injected."""

from pathlib import Path

from text_watermark_tools.iterate import (
    DASHSCOPE_KEY_FILE,
    DEEPSEEK_KEY_FILE,
    OperatorError,
    at_chance,
    chat_complete,
    dashscope_api_key,
    deepseek_api_key,
    persist_iterate_run,
    print_iterate_run,
    read_key_conf,
    rewrite_once,
    run_iterate,
)
from text_watermark_tools.score import official_score_text

LAB = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-15-gpt2-sonnet5"


def test_read_key_conf_skips_comments_and_placeholders(tmp_path: Path) -> None:
    p = tmp_path / DEEPSEEK_KEY_FILE
    p.write_text("# comment\nDEEPSEEK_API_KEY=\n# still empty\n")
    assert read_key_conf(p) is None
    p.write_text("# comment\nDEEPSEEK_API_KEY=sk-test-from-file\n")
    assert read_key_conf(p) == "sk-test-from-file"
    p.write_text("sk-bare-key\n")
    assert read_key_conf(p) == "sk-bare-key"


def test_deepseek_and_dashscope_keys_from_conf_files(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.setenv("TEXT_WATERMARK_KEY_DIR", str(tmp_path))
    (tmp_path / DEEPSEEK_KEY_FILE).write_text("DEEPSEEK_API_KEY=sk-ds-file\n")
    (tmp_path / DASHSCOPE_KEY_FILE).write_text("DASHSCOPE_API_KEY=sk-qw-file\n")
    assert deepseek_api_key() == "sk-ds-file"
    assert dashscope_api_key() == "sk-qw-file"
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-ds-env")
    assert deepseek_api_key() == "sk-ds-env"


def test_rewrite_once_paraphrase_and_zh_roundtrip() -> None:
    seen: list[str] = []

    def chat(prompt: str) -> str:
        seen.append(prompt)
        if "Simplified Chinese" in prompt:
            return "港口在黄昏"
        if "to English" in prompt:
            return "The harbour at dusk."
        return "A fully reworded harbour paragraph."

    assert rewrite_once("hello harbour", via="paraphrase", chat=chat).startswith("A fully")
    assert "substantially different wording" in seen[0]
    out = rewrite_once("hello harbour", via="zh", chat=chat)
    assert out == "The harbour at dusk."
    assert any("Simplified Chinese" in p for p in seen)
    assert any("to English" in p for p in seen)


def test_chat_complete_refuses_non_http() -> None:
    try:
        chat_complete("x", api_key="sk-test", base_url="file:///tmp")
    except OperatorError as exc:
        assert "non-http" in str(exc)
    else:
        raise AssertionError("expected OperatorError")


def test_at_chance_needs_enough_ngrams() -> None:
    marked = official_score_text((LAB / "t_high_temp.txt").read_text())
    assert not at_chance(marked)
    rewrite = official_score_text((LAB / "t_prime_sonnet5.txt").read_text())
    assert at_chance(rewrite)


def test_iterate_stops_when_official_score_hits_chance(tmp_path: Path) -> None:
    marked = (LAB / "t_high_temp.txt").read_text()
    unmarked = (LAB / "t_prime_sonnet5.txt").read_text()
    calls: list[int] = []

    def rewrite(_text: str) -> str:
        calls.append(1)
        return unmarked

    run = run_iterate(
        marked,
        rewrite=rewrite,
        operator="fixture",
        model="t_prime_sonnet5",
        max_passes=4,
    )
    assert len(calls) == 1
    assert run.source.score.mean > 0.55
    assert run.final.at_chance
    assert run.stopped_at_chance
    assert abs(run.final.score.mean - 0.5) < 0.03
    report = print_iterate_run(run)
    assert "instance=public-deepmind-30" in report
    assert "stopped_at_chance=True" in report
    persist_iterate_run(run, tmp_path)
    assert (tmp_path / "final.txt").read_text().strip() == unmarked.strip()
    assert "Not a remover" in (tmp_path / "results.json").read_text()


def test_iterate_stops_at_max_passes() -> None:
    marked = (LAB / "t_high_temp.txt").read_text()

    def rewrite(text: str) -> str:
        return text

    run = run_iterate(
        marked,
        rewrite=rewrite,
        operator="identity",
        model="none",
        max_passes=2,
    )
    assert len(run.passes) == 3  # source + 2
    assert run.stopped_at_chance is False
    assert run.final.score.mean > 0.55
