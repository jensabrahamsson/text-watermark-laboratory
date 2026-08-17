"""Key-free surrogate: fit only from generate() token samples.

Does not read watermark keys, hash_iv, or official g-values.
Context window is a fit hyperparameter (last-k tokens), not loaded from
DEFAULT_WATERMARKING_CONFIG.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Mapping, Optional, Sequence

import torch

# Last-k tokens used as the surrogate's context. Chosen as a fit knob, not
# read from the watermark config / keys / hash_iv.
SURROGATE_CONTEXT_LEN = 4


@dataclass(frozen=True)
class QueryObservation:
    """One next-token sample from the marked generator."""

    context: tuple[int, ...]
    next_token: int


@dataclass
class Surrogate:
    """Empirical next-token preferences under the marked generator."""

    context_len: int
    counts: dict[tuple[int, ...], Counter] = field(default_factory=dict)
    n_observations: int = 0
    n_queries: int = 0
    used_keys: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False

    def preferred(self, context: Sequence[int], token: int) -> bool:
        """True if the marked generator was seen emitting `token` in this context."""
        key = _ctx(context, self.context_len)
        ctr = self.counts.get(key)
        if not ctr:
            return False
        return token in ctr

    def alternative(
        self, context: Sequence[int], token: int
    ) -> Optional[int]:
        key = _ctx(context, self.context_len)
        ctr = self.counts.get(key)
        if not ctr:
            return None
        # Prefer a rarer marked sample, not the current token.
        for cand, _ in sorted(ctr.items(), key=lambda kv: kv[1]):
            if cand != token:
                return cand
        return None


def _ctx(ids: Sequence[int], context_len: int) -> tuple[int, ...]:
    if len(ids) < context_len:
        return tuple(ids)
    return tuple(ids[-context_len:])


def observations_from_sequence(
    token_ids: Sequence[int],
    *,
    context_len: int = SURROGATE_CONTEXT_LEN,
) -> list[QueryObservation]:
    """Treat every source token as one marked-generator observation."""
    ids = list(token_ids)
    return [
        QueryObservation(context=_ctx(ids[:i], context_len), next_token=int(ids[i]))
        for i in range(max(context_len, 1), len(ids))
    ]


def observations_from_samples(
    prefix_ids: Sequence[int],
    next_tokens: Iterable[int],
    *,
    context_len: int = SURROGATE_CONTEXT_LEN,
) -> list[QueryObservation]:
    ctx = _ctx(prefix_ids, context_len)
    return [QueryObservation(context=ctx, next_token=int(t)) for t in next_tokens]


def fit_surrogate(
    observations: Sequence[QueryObservation],
    *,
    context_len: int = SURROGATE_CONTEXT_LEN,
    n_queries: Optional[int] = None,
) -> Surrogate:
    """Aggregate query observations. Must not consult keys / g-values."""
    counts: dict[tuple[int, ...], Counter] = defaultdict(Counter)
    for obs in observations:
        counts[obs.context][obs.next_token] += 1
    return Surrogate(
        context_len=context_len,
        counts=dict(counts),
        n_observations=len(observations),
        n_queries=n_queries if n_queries is not None else len(observations),
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )


def query_marked_generator(
    token_ids: torch.Tensor,
    *,
    model: torch.nn.Module,
    pad_token_id: int,
    n_positions: int,
    samples_per_position: int,
    context_len: int = SURROGATE_CONTEXT_LEN,
    temperature: float = 1.0,
    top_k: int = 40,
    seed: Optional[int] = 0,
) -> tuple[list[QueryObservation], int]:
    """Query the marked model at prefixes taken from token_ids.

    Only uses model.generate. Does not compute g-values or read keys.
    """
    from text_watermark_tools.generate import next_token_samples

    if token_ids.dim() == 2:
        ids = token_ids[0].tolist()
    else:
        ids = token_ids.tolist()
    start = max(context_len, 1)
    eligible = list(range(start, len(ids)))
    if not eligible:
        return [], 0
    if seed is not None:
        torch.manual_seed(seed)
    # n_positions < 0: every eligible token. 0: no extra queries.
    if n_positions == 0:
        return [], 0
    if n_positions < 0 or n_positions >= len(eligible):
        positions = eligible
    else:
        step = len(eligible) / n_positions
        positions = [eligible[int(i * step)] for i in range(n_positions)]

    observations: list[QueryObservation] = []
    n_queries = 0
    for pos in positions:
        prefix = torch.tensor(ids[:pos], dtype=torch.long)
        samples = next_token_samples(
            prefix,
            model=model,
            n_samples=samples_per_position,
            temperature=temperature,
            top_k=top_k,
            pad_token_id=pad_token_id,
        )
        n_queries += samples_per_position
        observations.extend(
            observations_from_samples(ids[:pos], samples, context_len=context_len)
        )
        # Also count the token that actually appeared in the source as one
        # observation of the marked generator's choice (it was sampled once).
        observations.append(
            QueryObservation(
                context=_ctx(ids[:pos], context_len),
                next_token=int(ids[pos]),
            )
        )
    return observations, n_queries


def rewrite_token_ids(
    token_ids: Sequence[int],
    surrogate: Surrogate,
    *,
    unmarked_replacements: Optional[Mapping[int, int]] = None,
) -> list[int]:
    """Replace surrogate-preferred tokens with a less-preferred alternative.

    Lookups use the *original* contexts so earlier flips do not hide later
    ones. Unmarked-decoder substitutes are preferred over other marked
    samples (those are still biased). Never uses g-values.
    """
    src = list(token_ids)
    out = list(token_ids)
    ctx_len = surrogate.context_len
    for i in range(ctx_len, len(out)):
        context = src[i - ctx_len : i]
        tok = src[i]
        if not surrogate.preferred(context, tok):
            continue
        alt = None
        if unmarked_replacements is not None:
            cand = unmarked_replacements.get(i)
            if cand is not None and cand != tok:
                alt = cand
        if alt is None:
            alt = surrogate.alternative(context, tok)
        if alt is not None and alt != tok:
            out[i] = int(alt)
    return out


def unmarked_replacements_for(
    token_ids: Sequence[int],
    surrogate: Surrogate,
    *,
    model: torch.nn.Module,
    pad_token_id: int,
    temperature: float = 1.0,
    top_k: int = 40,
) -> dict[int, int]:
    """Unmarked top alternative at every preferred source position.

    One forward pass over the source sequence (logits at each prefix).
    """
    from text_watermark_tools.generate import top_alternative_from_logits

    del pad_token_id, temperature
    ids = list(token_ids)
    if len(ids) < 2:
        return {}
    device = next(model.parameters()).device
    batch = torch.tensor([ids], dtype=torch.long, device=device)
    with torch.no_grad():
        logits = model(input_ids=batch).logits[0]
    repl: dict[int, int] = {}
    ctx_len = surrogate.context_len
    for i in range(ctx_len, len(ids)):
        context = ids[i - ctx_len : i]
        if not surrogate.preferred(context, ids[i]):
            continue
        alt = top_alternative_from_logits(logits[i - 1], ids[i], top_k=top_k)
        if alt is not None:
            repl[i] = alt
    return repl
