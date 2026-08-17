"""Same-prompt twins: mixin-marked generation scores above the unmarked twin."""

from pathlib import Path

from text_watermark_tools.pair import collect_prompts, persist_pair_run, run_pairs

PROMPT = "The harbour lights flickered over wet cobblestones. "


def test_collect_prompts_from_file(tmp_path: Path) -> None:
    p = tmp_path / "harbour.txt"
    p.write_text(PROMPT)
    got = collect_prompts(p)
    assert got == [("harbour", PROMPT)]


def test_collect_prompts_from_directory(tmp_path: Path) -> None:
    (tmp_path / "a.txt").write_text("one")
    (tmp_path / "b.txt").write_text("two")
    (tmp_path / "notes.md").write_text("ignore")
    got = collect_prompts(tmp_path)
    assert [stem for stem, _ in got] == ["a", "b"]


def test_pair_marked_twin_scores_above_unmarked(tmp_path: Path) -> None:
    run = run_pairs([("harbour", PROMPT)], max_new_tokens=64, seed=2)
    assert len(run.rows) == 1
    row = run.rows[0]
    assert row.marked_score.n_tokens == 64
    assert row.unmarked_score.n_tokens == 64
    assert row.marked_score.n_unmasked_ngrams >= 50
    assert row.marked_score.mean > 0.5
    assert row.marked_score.mean > row.unmarked_score.mean
    persist_pair_run(run, tmp_path)
    assert (tmp_path / "harbour-marked.txt").is_file()
    assert (tmp_path / "harbour-unmarked-gen.txt").is_file()
    assert not (tmp_path / "harbour-control-gen.txt").is_file()
    results = (tmp_path / "results.json").read_text()
    assert "public-deepmind-30" in results
    assert "not stamped" in results


def test_pair_control_gen_is_other_instance_not_a_marked_file(tmp_path: Path) -> None:
    run = run_pairs(
        [("harbour", PROMPT)],
        max_new_tokens=64,
        seed=2,
        also_control_keys=True,
    )
    row = run.rows[0]
    assert row.alt_score_public is not None
    assert row.alt_score_matching is not None
    assert row.alt_score_matching.mean > row.alt_score_public.mean
    persist_pair_run(run, tmp_path)
    assert (tmp_path / "harbour-control-gen.txt").is_file()
    marked = sorted(p.name for p in tmp_path.glob("*-marked.txt"))
    assert marked == ["harbour-marked.txt"]