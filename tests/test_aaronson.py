"""Aaronson–Kirchner exponential-minimum is not detector_mean."""

from pathlib import Path

import torch

from text_watermark_tools.aaronson import (
    AARONSON_CONTEXT_WIDTH,
    AARONSON_HASHING_KEY,
    AARONSON_INSTANCE,
    AARONSON_Z_THRESHOLD,
    aaronson_config_dict,
    aaronson_pick,
    aaronson_score_token_ids,
    aaronson_uniform,
    format_aaronson_score,
)
from text_watermark_tools.score import OfficialScore


def test_aaronson_module_does_not_import_synthid_detector() -> None:
    src = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "text_watermark_tools"
        / "aaronson.py"
    ).read_text()
    assert "from synthid_text" not in src
    assert "import synthid_text" not in src
    assert "from synthid_text import detector_mean" not in src
    assert "WatermarkDetector" not in src
    assert "WatermarkLogitsProcessor" not in src
    assert "Do not call detector_mean" in src


def test_aaronson_config_is_frozen_public() -> None:
    cfg = aaronson_config_dict()
    assert cfg["hashing_key"] == 314159265
    assert cfg["context_width"] == 1
    assert cfg["temperature"] == 1.0
    assert cfg["top_k"] == 40
    assert cfg["z_threshold"] == 3.0
    assert cfg["prf"] == "blake2b-64"
    assert AARONSON_HASHING_KEY == 314159265
    assert AARONSON_CONTEXT_WIDTH == 1
    assert AARONSON_Z_THRESHOLD == 3.0
    assert AARONSON_INSTANCE == "aaronson-kirchner-expmin"


def test_aaronson_uniform_is_open_unit_interval_and_deterministic() -> None:
    u = aaronson_uniform(AARONSON_HASHING_KEY, (12,), 7)
    v = aaronson_uniform(AARONSON_HASHING_KEY, (12,), 7)
    w = aaronson_uniform(AARONSON_HASHING_KEY, (13,), 7)
    assert u == v
    assert u != w
    assert 0.0 < u < 1.0


def test_aaronson_pick_is_deterministic_on_peaked_logits() -> None:
    logits = torch.zeros(20)
    logits[5] = 8.0
    a = aaronson_pick(logits, (3,))
    b = aaronson_pick(logits, (3,))
    assert a == b
    assert a == 5


def test_aaronson_score_null_sequence_is_finite() -> None:
    ids = torch.arange(1, 33)
    score = aaronson_score_token_ids(ids)
    assert score.n_tokens == 32
    assert score.n_unmasked_ngrams == 32
    assert score.z_score is not None
    assert 0.0 < score.mean < 1.0
    line = format_aaronson_score("harbour-marked", score)
    assert "mean_u=" in line
    assert AARONSON_INSTANCE in line
    assert "detector_mean" not in line


def test_run_pairs_aaronson_rejects_control_keys() -> None:
    import pytest
    from text_watermark_tools.pair import run_pairs

    with pytest.raises(ValueError, match="SynthID-only"):
        run_pairs(
            [("harbour", "prompt")],
            mixin="aaronson",
            also_control_keys=True,
        )


def test_run_pairs_aaronson_rejects_ngram_len_13() -> None:
    import pytest
    from text_watermark_tools.pair import run_pairs

    with pytest.raises(ValueError, match="SynthID-only"):
        run_pairs(
            [("harbour", "prompt")],
            mixin="aaronson",
            ngram_len=13,
        )


def test_official_score_optional_fields_default_none() -> None:
    s = OfficialScore(mean=0.62, weighted_mean=0.61, n_tokens=128, n_unmasked_ngrams=116)
    assert s.z_score is None
    assert s.green_fraction is None
