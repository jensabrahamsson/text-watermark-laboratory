"""Aaronson–Kirchner exponential-minimum sampling and matching score.

transformers==4.57.6 has no Aaronson logits processor. This module is
the laboratory's frozen public instance of the talk construction
(Aaronson & Kirchner, 2023): at each step, keyed uniforms r_v and
model probabilities p_v pick v* = argmax_v r_v**(1/p_v) after the same
temperature-1 / top-K 40 filter as the SynthID path.

This is not SynthID. Do not call detector_mean on these twins.
This is not Kirchenbauer green-list. context_width=1 is shorter than
public Hw=4. Do not sell it as Hw=12.
"""

from __future__ import annotations

import hashlib
import math
from typing import Optional, Sequence

import torch
import transformers
from transformers import LogitsProcessor

from text_watermark_tools.score import OfficialScore, TEMPERATURE, TOP_K, load_tokenizer

AARONSON_INSTANCE = "aaronson-kirchner-expmin"
# Public digits of π. Not a laboratory secret. Not fished against last-4.
AARONSON_HASHING_KEY = 314159265
AARONSON_CONTEXT_WIDTH = 1
AARONSON_Z_THRESHOLD = 3.0
AARONSON_HUB_REVISION = "607a30d783dfa663caf39e06633721c8d4cfcd7e"


def aaronson_config_dict() -> dict:
    return {
        "hashing_key": AARONSON_HASHING_KEY,
        "context_width": AARONSON_CONTEXT_WIDTH,
        "temperature": TEMPERATURE,
        "top_k": TOP_K,
        "z_threshold": AARONSON_Z_THRESHOLD,
        "prf": "blake2b-64",
        "rule": "argmax r**(1/p) after temperature/top-k",
    }


def aaronson_uniform(
    hashing_key: int, context: Sequence[int], vocab_id: int
) -> float:
    """Keyed Uniform(0,1) for one vocabulary id. Open interval via (x+1/2)/2^64."""
    h = hashlib.blake2b(digest_size=8)
    h.update(int(hashing_key).to_bytes(8, "little", signed=False))
    h.update(len(context).to_bytes(4, "little"))
    for tok in context:
        h.update(int(tok).to_bytes(8, "little", signed=False))
    h.update(int(vocab_id).to_bytes(8, "little", signed=False))
    x = int.from_bytes(h.digest(), "little")
    return (x + 0.5) / float(1 << 64)


def _context_tuple(ids: Sequence[int], position: int, width: int) -> tuple[int, ...]:
    if width <= 0 or position <= 0:
        return ()
    start = max(0, position - width)
    return tuple(int(t) for t in ids[start:position])


def aaronson_pick(
    logits: torch.Tensor,
    context: Sequence[int],
    *,
    hashing_key: int = AARONSON_HASHING_KEY,
    temperature: float = TEMPERATURE,
    top_k: int = TOP_K,
) -> int:
    """Exponential-minimum pick on one logit row. Deterministic given logits+context."""
    if logits.dim() != 1:
        raise ValueError("aaronson_pick expects a 1-d logit vector")
    scaled = logits / max(float(temperature), 1e-6)
    k = min(int(top_k), scaled.numel()) if top_k else scaled.numel()
    top_vals, top_idx = torch.topk(scaled, k)
    probs = torch.softmax(top_vals, dim=-1)
    best_s = float("-inf")
    best_id = int(top_idx[0].item())
    ctx = tuple(int(t) for t in context)
    for j in range(k):
        p = float(probs[j].item())
        if p <= 0.0:
            continue
        vid = int(top_idx[j].item())
        u = aaronson_uniform(hashing_key, ctx, vid)
        score = math.log(u) / p
        if score > best_s:
            best_s = score
            best_id = vid
    return best_id


class AaronsonLogitsProcessor(LogitsProcessor):
    """Force the exponential-minimum token so HF generate can stay on the KV cache."""

    def __init__(
        self,
        *,
        hashing_key: int = AARONSON_HASHING_KEY,
        context_width: int = AARONSON_CONTEXT_WIDTH,
        temperature: float = TEMPERATURE,
        top_k: int = TOP_K,
    ) -> None:
        self.hashing_key = int(hashing_key)
        self.context_width = int(context_width)
        self.temperature = float(temperature)
        self.top_k = int(top_k)

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor
    ) -> torch.FloatTensor:
        out = torch.full_like(scores, float("-inf"))
        for b in range(input_ids.size(0)):
            ids = input_ids[b].tolist()
            ctx = _context_tuple(ids, len(ids), self.context_width)
            pick = aaronson_pick(
                scores[b],
                ctx,
                hashing_key=self.hashing_key,
                temperature=self.temperature,
                top_k=self.top_k,
            )
            out[b, pick] = 0.0
        return out


def aaronson_processor() -> AaronsonLogitsProcessor:
    return AaronsonLogitsProcessor(
        hashing_key=AARONSON_HASHING_KEY,
        context_width=AARONSON_CONTEXT_WIDTH,
        temperature=TEMPERATURE,
        top_k=TOP_K,
    )


def aaronson_score_token_ids(input_ids: torch.Tensor) -> OfficialScore:
    """Matching mean-r z-test vs Uniform(0,1). Not detector_mean. Not KGW z."""
    if input_ids.dim() == 1:
        input_ids = input_ids.unsqueeze(0)
    ids = [int(t) for t in input_ids[0].tolist()]
    us: list[float] = []
    for i, vid in enumerate(ids):
        ctx = _context_tuple(ids, i, AARONSON_CONTEXT_WIDTH)
        us.append(aaronson_uniform(AARONSON_HASHING_KEY, ctx, vid))
    n = len(us)
    if n == 0:
        return OfficialScore(
            mean=0.5,
            weighted_mean=0.5,
            n_tokens=0,
            n_unmasked_ngrams=0,
            z_score=0.0,
        )
    mean_u = float(sum(us) / n)
    z = (mean_u - 0.5) / math.sqrt((1.0 / 12.0) / n)
    return OfficialScore(
        mean=mean_u,
        weighted_mean=mean_u,
        n_tokens=n,
        n_unmasked_ngrams=n,
        z_score=float(z),
    )


def aaronson_score_text(
    text: str,
    *,
    tokenizer: Optional[transformers.PreTrainedTokenizer] = None,
    model_name: str = "gpt2",
    revision: Optional[str] = None,
) -> OfficialScore:
    tok = tokenizer or load_tokenizer(model_name, revision=revision)
    ids = tok(text, return_tensors="pt")["input_ids"]
    return aaronson_score_token_ids(ids)


def format_aaronson_score(label: str, score: OfficialScore) -> str:
    z = float("nan") if score.z_score is None else score.z_score
    return (
        f"{label}: mean_u={score.mean:.6f} z_score={z:.6f} "
        f"n_tokens={score.n_tokens} n_scored={score.n_unmasked_ngrams} "
        f"instance={AARONSON_INSTANCE} z_threshold={AARONSON_Z_THRESHOLD}"
    )
