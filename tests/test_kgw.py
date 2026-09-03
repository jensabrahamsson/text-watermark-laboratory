"""Kirchenbauer official scores use WatermarkDetector, not detector_mean."""

from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

from text_watermark_tools.kgw import (
    KGW_HASHING_KEY,
    KGW_INSTANCE,
    KGW_Z_THRESHOLD,
    format_kgw_score,
    kgw_config,
    kgw_score_token_ids,
)
from text_watermark_tools.score import OfficialScore


def test_kgw_module_does_not_import_synthid_detector() -> None:
    src = (Path(__file__).resolve().parents[1] / "src" / "text_watermark_tools" / "kgw.py").read_text()
    assert "from synthid_text" not in src
    assert "import synthid_text" not in src
    assert "from synthid_text import detector_mean" not in src
    assert "SynthIDLogitsProcessor" not in src


def test_kgw_config_is_huggingface_default() -> None:
    cfg = kgw_config()
    assert cfg.greenlist_ratio == 0.25
    assert cfg.bias == 2.0
    assert cfg.hashing_key == KGW_HASHING_KEY
    assert cfg.seeding_scheme == "lefthash"
    assert cfg.context_width == 1


def test_kgw_score_token_ids_uses_watermark_detector(monkeypatch) -> None:
    called = {"detector_mean": False, "detector": False}

    def boom(*_a, **_k):
        called["detector_mean"] = True
        raise AssertionError("detector_mean must not score kgw twins")

    monkeypatch.setattr("text_watermark_tools.score.detector_mean.mean_score", boom)

    class FakeDet:
        def __call__(self, input_ids, z_threshold=3.0, return_dict=False):
            called["detector"] = True
            assert z_threshold == KGW_Z_THRESHOLD
            assert return_dict is True
            n = int(input_ids.shape[1])
            return SimpleNamespace(
                z_score=np.array([4.2]),
                green_fraction=np.array([0.41]),
                num_tokens_scored=np.array([n - 1]),
            )

    score = kgw_score_token_ids(torch.tensor([[1, 2, 3, 4]]), detector=FakeDet())
    assert called["detector"] is True
    assert called["detector_mean"] is False
    assert score.z_score == 4.2
    assert score.green_fraction == 0.41
    assert score.mean == 0.41
    assert score.n_tokens == 4
    assert score.n_unmasked_ngrams == 3
    line = format_kgw_score("harbour-marked", score)
    assert "z_score=4.200000" in line
    assert KGW_INSTANCE in line
    assert "detector_mean" not in line


def test_run_pairs_kgw_rejects_control_keys() -> None:
    import pytest
    from text_watermark_tools.pair import run_pairs

    with pytest.raises(ValueError, match="SynthID-only"):
        run_pairs(
            [("harbour", "prompt")],
            mixin="kgw",
            also_control_keys=True,
        )


def test_run_pairs_kgw_rejects_ngram_len_13() -> None:
    import pytest
    from text_watermark_tools.pair import run_pairs

    with pytest.raises(ValueError, match="SynthID-only"):
        run_pairs(
            [("harbour", "prompt")],
            mixin="kgw",
            ngram_len=13,
        )


def test_official_score_optional_kgw_fields_default_none() -> None:
    s = OfficialScore(mean=0.62, weighted_mean=0.61, n_tokens=128, n_unmasked_ngrams=116)
    assert s.z_score is None
    assert s.green_fraction is None
