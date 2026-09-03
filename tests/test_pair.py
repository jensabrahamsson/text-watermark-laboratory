"""Same-prompt twins: mixin-marked generation scores above the unmarked twin."""

from pathlib import Path

from text_watermark_tools.pair import (
    PairRow,
    PairRun,
    collect_prompts,
    persist_pair_run,
    run_pairs,
)
import json
from text_watermark_tools.score import OfficialScore

PROMPT = "The harbour lights flickered over wet cobblestones. "


def test_persist_pair_run_records_hub_revision(tmp_path: Path) -> None:
    run = PairRun(
        rows=[],
        max_new_tokens=128,
        seed=0,
        hub_revision="607a30d783dfa663caf39e06633721c8d4cfcd7e",
    )
    persist_pair_run(run, tmp_path)
    data = json.loads((tmp_path / "results.json").read_text())
    assert data["hub_revision"] == "607a30d783dfa663caf39e06633721c8d4cfcd7e"
    assert data["ngram_len"] == 5


def test_persist_pair_run_records_unset_hub_revision_as_null(tmp_path: Path) -> None:
    run = PairRun(rows=[], max_new_tokens=128, seed=0)
    persist_pair_run(run, tmp_path)
    data = json.loads((tmp_path / "results.json").read_text())
    assert "hub_revision" in data
    assert data["hub_revision"] is None
    assert "unpinned default" in data["note"]


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


def test_persist_pair_run_writes_ngram_len(tmp_path: Path) -> None:
    dummy = OfficialScore(mean=0.50, weighted_mean=0.50, n_tokens=8, n_unmasked_ngrams=4)
    run = PairRun(
        rows=[
            PairRow(
                stem="harbour",
                prompt="The harbour lights.\n",
                prompt_score=dummy,
                marked_text="marked",
                marked_score=dummy,
                unmarked_text="unmarked",
                unmarked_score=dummy,
            )
        ],
        max_new_tokens=128,
        seed=20260903,
        ngram_len=13,
    )
    persist_pair_run(run, tmp_path)
    results = (tmp_path / "results.json").read_text()
    assert '"ngram_len": 13' in results
    assert (tmp_path / "harbour-marked.txt").is_file()


def test_persist_control_only_writes_extra_draws_not_marked(tmp_path: Path) -> None:
    dummy = OfficialScore(mean=0.50, weighted_mean=0.50, n_tokens=8, n_unmasked_ngrams=4)
    match = OfficialScore(mean=0.62, weighted_mean=0.62, n_tokens=8, n_unmasked_ngrams=4)
    run = PairRun(
        rows=[
            PairRow(
                stem="harbour",
                prompt="The harbour lights.\n",
                prompt_score=dummy,
                marked_text="",
                marked_score=dummy,
                unmarked_text="",
                unmarked_score=dummy,
                alt_text="control one",
                alt_score_public=dummy,
                alt_score_matching=match,
                extra_control=[("control two", dummy, match)],
            )
        ],
        max_new_tokens=8,
        seed=0,
        alt_keys=[1, 2, 3],
    )
    persist_pair_run(run, tmp_path)
    assert (tmp_path / "harbour-control-gen.txt").is_file()
    assert (tmp_path / "harbour-control-gen-2.txt").is_file()
    assert not (tmp_path / "harbour-marked.txt").is_file()
    assert not (tmp_path / "harbour-unmarked-gen.txt").is_file()
    results = (tmp_path / "results.json").read_text()
    assert '"control_only": true' in results
    readme = (tmp_path / "README.md").read_text()
    assert "Control-shuffled-30" in readme
    assert "not public DeepMind 30" in readme