"""Official score path on real texts. Calls shipped official_score_text."""

from pathlib import Path

import pytest

from text_watermark_tools.score import (
    control_keys,
    format_score,
    official_processor,
    official_score_text,
    public_keys,
)

LAB = Path(__file__).resolve().parents[1] / "experiments" / "2026-08-15-gpt2-sonnet5"


@pytest.fixture(scope="module")
def marked_text() -> str:
    return (LAB / "t_high_temp.txt").read_text()


@pytest.fixture(scope="module")
def rewritten_text() -> str:
    return (LAB / "t_prime_sonnet5.txt").read_text()


def test_marked_lab_text_scores_above_half(marked_text: str) -> None:
    score = official_score_text(marked_text)
    assert score.n_unmasked_ngrams > 100
    assert score.n_tokens > 100
    assert score.mean > 0.55
    assert score.weighted_mean > 0.55


def test_rewritten_lab_text_near_half(rewritten_text: str) -> None:
    score = official_score_text(rewritten_text)
    assert score.n_unmasked_ngrams > 100
    assert abs(score.mean - 0.5) < 0.03
    assert abs(score.weighted_mean - 0.5) < 0.03


def test_wrong_key_on_marked_text_near_half(marked_text: str) -> None:
    cfg_keys = list(official_processor().keys.cpu().tolist())
    wrong = [int(k) + 1 for k in cfg_keys]
    score = official_score_text(marked_text, keys=wrong)
    assert score.n_unmasked_ngrams > 100
    assert abs(score.mean - 0.5) < 0.05


def test_score_reports_counts(marked_text: str) -> None:
    score = official_score_text(marked_text)
    assert score.n_tokens == len(
        __import__("transformers")
        .AutoTokenizer.from_pretrained("gpt2")(marked_text)["input_ids"]
    )
    assert 0 < score.n_unmasked_ngrams <= score.n_tokens


def test_official_processor_ngram_len_override() -> None:
    default = official_processor()
    longer = official_processor(ngram_len=13)
    assert int(default.ngram_len) == 5
    assert int(longer.ngram_len) == 13


def test_format_score_names_public_instance(marked_text: str) -> None:
    line = format_score("lab", official_score_text(marked_text))
    assert "instance=public-deepmind-30" in line
    assert "ngram_len=5" in line
    assert "mean=" in line


def test_control_keys_are_dummy_not_a_permutation() -> None:
    public = public_keys()
    dummy = control_keys()
    assert dummy == control_keys()
    assert dummy != public
    assert sorted(dummy) != sorted(public)


def test_control_keys_on_marked_text_near_half(marked_text: str) -> None:
    score = official_score_text(marked_text, keys=control_keys())
    assert score.n_unmasked_ngrams > 100
    assert abs(score.mean - 0.5) < 0.05
