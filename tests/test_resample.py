"""Shipped Claude resample: analyze existing twins and append-only logbook."""

from pathlib import Path

from text_watermark_tools.resample import analyze_and_append

ROOT = Path(__file__).resolve().parents[1]
COLLECT = ROOT / "scripts" / "collect_claude_premark.py"
FIRST_PROMPT = (
    "Write a 600-word travel essay about arriving in a small harbour town at dusk. "
    "Everyday words, no lists, no title."
)
LAST_PROMPT = (
    "A letter from a retired teacher to a former pupil who wrote first. About 500 words."
)


def test_prompts_strings_untouched() -> None:
    src = COLLECT.read_text()
    assert FIRST_PROMPT in src
    assert LAST_PROMPT in src
    # Order: first prompt still precedes last; no silent rewrite of the list.
    assert src.index(FIRST_PROMPT) < src.index(LAST_PROMPT)


def test_analyze_and_append_existing_twins_appends_logbook(tmp_path: Path) -> None:
    original = (ROOT / "research" / "LOGBOOK.md").read_text()
    log = tmp_path / "LOGBOOK.md"
    log.write_text(original)
    report = analyze_and_append(
        new_dir=ROOT / "experiments" / "claude-sample-2026-08-19b",
        premark_dir=ROOT / "experiments" / "claude-premark-2026-08",
        previous_dir=ROOT / "experiments" / "claude-mark-2026-08-19",
        logbook=log,
        experiments=tmp_path / "exp",
        date="2026-08-20",
        collected=False,
    )
    assert report.contrasts, "expected premark-vs-new and previous-vs-new"
    assert all(c.used_keys is False for c in report.contrasts)
    assert all(c.n_pairs >= 2 for c in report.contrasts)
    text = log.read_text()
    assert "## 2026-08-15" in text
    assert original in text
    assert text.index("## 2026-08-15") < text.index("## 2026-08-20 resample")
    suffix = text[len(original) :]
    assert "## 2026-08-20 resample" in suffix
    assert "last-1" in suffix and "last-4" in suffix
    for c in report.contrasts:
        assert f"{c.last1_wins}/{c.n_pairs}" in suffix
        assert f"{c.last4_wins}/{c.n_pairs}" in suffix
        results = (
            tmp_path
            / "exp"
            / "2026-08-20-resample-work"
            / f"blind-{c.name}-k1"
            / "results.json"
        )
        assert results.is_file()
        payload = results.read_text()
        assert f'"n_marked_wins": {c.last1_wins}' in payload
        k4 = results.with_name("results.json")
        k4 = (
            tmp_path
            / "exp"
            / "2026-08-20-resample-work"
            / f"blind-{c.name}-k4"
            / "results.json"
        )
        assert f'"n_marked_wins": {c.last4_wins}' in k4.read_text()
    # Older headings survive verbatim as a block.
    assert "## 2026-08-17" in text
    assert original.split("## 2026-08-15")[0] in text
