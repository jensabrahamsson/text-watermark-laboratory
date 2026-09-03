"""Official Mean / Weighted Mean via DeepMind detector_mean."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

import jax.numpy as jnp
import numpy as np
import torch
import transformers
from synthid_text import detector_mean
from synthid_text import logits_processing
from synthid_text import synthid_mixin

MODEL_NAME = "gpt2"
TEMPERATURE = 1.0
TOP_K = 40

# Printed on every score line so ~0.50 is not read as "unmarked / human / Claude".
PUBLIC_INSTANCE = "public-deepmind-30"
CONTROL_INSTANCE = "control-shuffled-30"


def public_watermarking_config() -> dict:
    return dict(synthid_mixin.DEFAULT_WATERMARKING_CONFIG)


def public_keys() -> list[int]:
    return list(public_watermarking_config()["keys"])


def public_ngram_len() -> int:
    return int(public_watermarking_config()["ngram_len"])


def control_keys(keys: Optional[list[int]] = None) -> list[int]:
    """Dummy keyset for a same-tokens contrast.

    A permutation of the public 30 keys leaves the unweighted mean unchanged
    (same layer set, different order). Offset each key, then shuffle with a
    fixed seed so the control is deterministic and not the official instance.
    """
    src = list(keys) if keys is not None else public_keys()
    dummy = [int(k) + 1 for k in src]
    rng = random.Random(0)
    rng.shuffle(dummy)
    return dummy


def _device() -> torch.device:
    return torch.device("cpu")


def official_processor(
    *,
    keys: Optional[list[int]] = None,
    device: Optional[torch.device] = None,
    ngram_len: Optional[int] = None,
) -> logits_processing.SynthIDLogitsProcessor:
    """Build the DeepMind processor for the public reference config.

    `ngram_len` overrides the public hash window. Matching generation must
    use the same value. Default is the public instance (`ngram_len=5`).
    """
    cfg = public_watermarking_config()
    dev = device or _device()
    nlen = int(ngram_len) if ngram_len is not None else int(cfg["ngram_len"])
    return logits_processing.SynthIDLogitsProcessor(
        ngram_len=nlen,
        keys=list(keys) if keys is not None else list(cfg["keys"]),
        context_history_size=cfg["context_history_size"],
        device=dev,
        top_k=TOP_K,
        temperature=TEMPERATURE,
    )


def hf_load_kwargs(*, revision: Optional[str] = None) -> dict:
    """Hugging Face from_pretrained kwargs. Empty when revision is unset."""
    return {"revision": str(revision)} if revision else {}


def load_tokenizer(
    model_name: Optional[str] = None,
    *,
    revision: Optional[str] = None,
) -> transformers.PreTrainedTokenizer:
    """Tokenizer for the generator that produced the tokens. Default: GPT-2."""
    name = model_name or MODEL_NAME
    tokenizer = transformers.AutoTokenizer.from_pretrained(
        name, **hf_load_kwargs(revision=revision)
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


@dataclass(frozen=True)
class OfficialScore:
    mean: float
    weighted_mean: float
    n_tokens: int
    n_unmasked_ngrams: int
    z_score: Optional[float] = None
    green_fraction: Optional[float] = None

    def closer_to_half_than(self, other: "OfficialScore") -> bool:
        return abs(self.mean - 0.5) < abs(other.mean - 0.5) and abs(
            self.weighted_mean - 0.5
        ) < abs(other.weighted_mean - 0.5)


def official_score_token_ids(
    input_ids: torch.Tensor,
    *,
    tokenizer: Optional[transformers.PreTrainedTokenizer] = None,
    processor: Optional[logits_processing.SynthIDLogitsProcessor] = None,
    keys: Optional[list[int]] = None,
    ngram_len: Optional[int] = None,
) -> OfficialScore:
    """Score token ids with DeepMind mean / weighted_mean (not a local reimplementation)."""
    if input_ids.dim() == 1:
        input_ids = input_ids.unsqueeze(0)
    tok = tokenizer or load_tokenizer()
    proc = processor or official_processor(keys=keys, ngram_len=ngram_len)
    ngram_len = proc.ngram_len
    if input_ids.shape[1] < ngram_len:
        return OfficialScore(
            mean=float("nan"),
            weighted_mean=float("nan"),
            n_tokens=int(input_ids.shape[1]),
            n_unmasked_ngrams=0,
        )

    eos = proc.compute_eos_token_mask(
        input_ids=input_ids, eos_token_id=tok.eos_token_id
    )[:, ngram_len - 1 :]
    rep = proc.compute_context_repetition_mask(input_ids=input_ids)
    mask_t = (rep * eos).to(dtype=torch.float32)
    g_t = proc.compute_g_values(input_ids=input_ids).to(dtype=torch.float32)

    mask = jnp.asarray(mask_t.detach().cpu().numpy())
    g_values = jnp.asarray(g_t.detach().cpu().numpy())
    mean = detector_mean.mean_score(g_values, mask)
    # weighted_mean_score multiplies g_values in place; pass a fresh array.
    weighted = detector_mean.weighted_mean_score(
        jnp.asarray(g_t.detach().cpu().numpy()), mask
    )
    n_unmasked = int(np.asarray(mask.sum(axis=1))[0])
    return OfficialScore(
        mean=float(np.asarray(mean)[0]),
        weighted_mean=float(np.asarray(weighted)[0]),
        n_tokens=int(input_ids.shape[1]),
        n_unmasked_ngrams=n_unmasked,
    )


def official_score_text(
    text: str,
    *,
    tokenizer: Optional[transformers.PreTrainedTokenizer] = None,
    processor: Optional[logits_processing.SynthIDLogitsProcessor] = None,
    keys: Optional[list[int]] = None,
    ngram_len: Optional[int] = None,
) -> OfficialScore:
    tok = tokenizer or load_tokenizer()
    ids = tok(text, return_tensors="pt")["input_ids"]
    return official_score_token_ids(
        ids,
        tokenizer=tok,
        processor=processor,
        keys=keys,
        ngram_len=ngram_len,
    )


def format_score(
    label: str,
    score: OfficialScore,
    *,
    instance: str = PUBLIC_INSTANCE,
    ngram_len: Optional[int] = None,
) -> str:
    nlen = public_ngram_len() if ngram_len is None else int(ngram_len)
    return (
        f"{label}: mean={score.mean:.6f} weighted_mean={score.weighted_mean:.6f} "
        f"n_tokens={score.n_tokens} n_unmasked_ngrams={score.n_unmasked_ngrams} "
        f"instance={instance} ngram_len={nlen}"
    )
