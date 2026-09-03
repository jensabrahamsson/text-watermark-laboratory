"""Kirchenbauer green-list official scores via Hugging Face WatermarkDetector.

This is not SynthID. Do not call detector_mean on these twins.
Defaults match transformers==4.57.6 WatermarkingConfig.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import torch
import transformers
from transformers import WatermarkDetector, WatermarkingConfig
from transformers.generation.watermarking import WatermarkDetectorOutput

from text_watermark_tools.score import OfficialScore, hf_load_kwargs, load_tokenizer

KGW_INSTANCE = "kirchenbauer-hf-default"
KGW_GREENLIST_RATIO = 0.25
KGW_BIAS = 2.0
KGW_HASHING_KEY = 15485863
KGW_SEEDING_SCHEME = "lefthash"
KGW_CONTEXT_WIDTH = 1
KGW_Z_THRESHOLD = 3.0
KGW_HUB_REVISION = "607a30d783dfa663caf39e06633721c8d4cfcd7e"


def kgw_config() -> WatermarkingConfig:
    """Frozen Hugging Face Kirchenbauer defaults. Do not fish after peeking."""
    return WatermarkingConfig(
        greenlist_ratio=KGW_GREENLIST_RATIO,
        bias=KGW_BIAS,
        hashing_key=KGW_HASHING_KEY,
        seeding_scheme=KGW_SEEDING_SCHEME,
        context_width=KGW_CONTEXT_WIDTH,
    )


def kgw_config_dict() -> dict:
    return {
        "greenlist_ratio": KGW_GREENLIST_RATIO,
        "bias": KGW_BIAS,
        "hashing_key": KGW_HASHING_KEY,
        "seeding_scheme": KGW_SEEDING_SCHEME,
        "context_width": KGW_CONTEXT_WIDTH,
        "z_threshold": KGW_Z_THRESHOLD,
    }


def kgw_detector(
    *,
    model_name: str = "gpt2",
    revision: Optional[str] = None,
    device: str = "cpu",
) -> WatermarkDetector:
    cfg = transformers.AutoConfig.from_pretrained(
        model_name, **hf_load_kwargs(revision=revision)
    )
    return WatermarkDetector(
        model_config=cfg,
        device=device,
        watermarking_config=kgw_config(),
    )


def kgw_score_token_ids(
    input_ids: torch.Tensor,
    *,
    model_name: str = "gpt2",
    revision: Optional[str] = None,
    detector: Optional[WatermarkDetector] = None,
) -> OfficialScore:
    """Matching Kirchenbauer z-test. Not detector_mean."""
    if input_ids.dim() == 1:
        input_ids = input_ids.unsqueeze(0)
    det = detector or kgw_detector(model_name=model_name, revision=revision)
    out: WatermarkDetectorOutput = det(
        input_ids, z_threshold=KGW_Z_THRESHOLD, return_dict=True
    )
    z = float(np.asarray(out.z_score)[0])
    gf = float(np.asarray(out.green_fraction)[0])
    n_scored = int(np.asarray(out.num_tokens_scored)[0])
    return OfficialScore(
        mean=gf,
        weighted_mean=gf,
        n_tokens=int(input_ids.shape[1]),
        n_unmasked_ngrams=n_scored,
        z_score=z,
        green_fraction=gf,
    )


def kgw_score_text(
    text: str,
    *,
    tokenizer: Optional[transformers.PreTrainedTokenizer] = None,
    model_name: str = "gpt2",
    revision: Optional[str] = None,
    detector: Optional[WatermarkDetector] = None,
) -> OfficialScore:
    tok = tokenizer or load_tokenizer(model_name, revision=revision)
    ids = tok(text, return_tensors="pt")["input_ids"]
    return kgw_score_token_ids(
        ids,
        model_name=model_name,
        revision=revision,
        detector=detector,
    )


def format_kgw_score(label: str, score: OfficialScore) -> str:
    z = float("nan") if score.z_score is None else score.z_score
    gf = float("nan") if score.green_fraction is None else score.green_fraction
    return (
        f"{label}: green_fraction={gf:.6f} z_score={z:.6f} "
        f"n_tokens={score.n_tokens} n_scored={score.n_unmasked_ngrams} "
        f"instance={KGW_INSTANCE} z_threshold={KGW_Z_THRESHOLD}"
    )
