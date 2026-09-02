"""Transferable key-free scorers on top of count tables.

The baseline `likelihood_ratio` uses an exact last-k context and falls
straight to the unigram when that k-gram is new. That is brittle on a
held-out prompt: most 4-grams never appeared in training.

These scorers keep the same tables (still no keys / hash_iv / g-values)
and change only how a finished string is read:

* unigram — token identity only
* backoff — shrink the context instead of jumping to the unigram
* interpolate — Witten–Bell mix of every stored order
* gated / hits — skip positions whose exact context is too rare
* tokhits — hits that also skip an unseen next token (no occupancy Laplace)
* tokbackoff — tokhits that shrink last-k until an observed next token hits
* tokbackoff2 — tokbackoff that will not shrink below last-2
* freqhits — shared 4-grams with count ≥ 4 on both sides
* hitmass — hits log-ratio × fraction of positions that hit
* shrinkage — credibility-weight each token's log ratio
* mix — average last-1 and last-k log ratios
* hashpool — feature-hash the context into shared buckets
* hashtok — hashpool that skips a hash unless the observed next token
  appeared in that bucket (occupancy-free; tokhits analog on collisions)
* hashtok2 — hashtok that skips singleton hash collisions (min_count=2)
* hashtokbackoff — hashtok that shrinks last-k across per-order hash
  tables until an observed next token hits (tokbackoff analog)
* hashtokbackoff2 — hashtokbackoff that will not shrink below last-2
* hashtoklen — hashtok that hashes only exact last-k (no short prefix
  mixed into a longer-order table)
* hashtoklenbackoff / hashtoklenbackoff2 — per-order hashtoklen;
  order-k is used only when i >= k
* hashskip — occupancy-free hashing of exact last-k with one token
  dropped (tagged skip-grams, not last-(k-1) and not Laplace)
* hashmask — occupancy-free hashing of exact last-k with one token
  replaced by MASK_TAG (length-k templates, not skip-grams)
* hashvote — majority sign of per-token hashpool ratios
* hybrid — exact shared n-grams when both sides saw them, else hashpool
* tokhybrid — occupancy-free hybrid: tokhits when the exact context and
  next token were seen, else hashtok
* hashtokgap — hashtok only where tokhits abstains (hashed residual of
  unseen exact n-grams; occupancy-free)
* poshashtok — hashtok with a token-position namespace (pospool analog)
* surface — the same hashpool, but on UTF-8 bytes of the raw string
  (no tokenizer; the reader that can cross generators)

Hash pooling is the one extra fit. It is a stealing-style regulariser:
contexts that collide in a random hash share a next-token table, so
held-out prompts can still be scored. It does not reconstruct the
secret SynthID hash. Frozen hashpool tables can be scored later with
`indicate score` without a twin. `hashtok` is a reader on those same
tables: Laplace occupancy of empty cells cannot vote.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

from text_watermark_tools.blind import (
    DEFAULT_ALPHA,
    FIRST_TOKEN_CTX,
    BlindModel,
    NextTokenTable,
    Twin,
    _ctx,
    _log_prob,
    _scored_ctx,
    clip_ctx_order,
    fit_blind,
    likelihood_ratio,
    score_index_range,
    shorten_ctx,
)

# Deterministic 64-bit constants (splitmix / golden ratio). Not watermark keys.
_GOLDEN = 0x9E3779B97F4A7C15
_MIX1 = 0xBF58476D1CE4E5B9
_MIX2 = 0x94D049BB133111EB
MASK64 = 0xFFFFFFFFFFFFFFFF
# Drop-one skip-gram namespace. Token ids are >= 0; FIRST_TOKEN_CTX is (-1,).
SKIP_TAG = -3
# Length-k MASK replace. Distinct from SKIP_TAG; not a watermark key.
MASK_TAG = -4


@dataclass(frozen=True)
class ScoreSpec:
    kind: str = "hard"
    min_count: int = 0
    require_both: bool = True
    require_token: bool = False
    shrinkage_tau: float = 0.0
    mix_orders: tuple[int, ...] = ()
    instance: str = "key-free-counts"
    include_first: bool = False
    first_only: bool = False
    min_order: int = 1


COUNT_SPECS: dict[str, ScoreSpec] = {
    "unigram": ScoreSpec(kind="unigram", instance="key-free-unigram"),
    "hard": ScoreSpec(kind="hard", instance="key-free-counts"),
    "backoff": ScoreSpec(kind="backoff", instance="key-free-backoff"),
    "interpolate": ScoreSpec(kind="interpolate", instance="key-free-interpolate"),
    "hits": ScoreSpec(kind="gated", min_count=1, instance="key-free-hits"),
    "tokhits": ScoreSpec(
        kind="gated",
        min_count=1,
        require_token=True,
        instance="key-free-tokhits",
    ),
    "tokbackoff": ScoreSpec(
        kind="tokbackoff",
        min_count=1,
        require_token=True,
        instance="key-free-tokbackoff",
    ),
    "tokbackoff2": ScoreSpec(
        kind="tokbackoff",
        min_count=1,
        require_token=True,
        min_order=2,
        instance="key-free-tokbackoff2",
    ),
    "freqhits": ScoreSpec(kind="gated", min_count=4, instance="key-free-freqhits"),
    "hitmass": ScoreSpec(kind="hitmass", min_count=1, instance="key-free-hitmass"),
    "gated": ScoreSpec(kind="gated", min_count=2, instance="key-free-gated"),
    "shrinkage": ScoreSpec(
        kind="shrinkage", shrinkage_tau=2.0, instance="key-free-shrinkage"
    ),
    "mix": ScoreSpec(kind="mix", mix_orders=(1, 4), instance="key-free-mix"),
    "first": ScoreSpec(
        kind="gated",
        min_count=1,
        include_first=True,
        first_only=True,
        instance="key-free-first",
    ),
}


@dataclass
class ScoreDetail:
    lr: float
    n_used: int
    n_positions: int


def _count(table: NextTokenTable, ctx: tuple[int, ...]) -> int:
    bucket = table.counts.get(ctx)
    if not bucket:
        return 0
    return int(sum(bucket.values()))


def _tok_count(table: NextTokenTable, ctx: tuple[int, ...], tok: int) -> int:
    bucket = table.counts.get(ctx)
    if not bucket:
        return 0
    return int(bucket.get(int(tok), 0))


def _ctx_has_support(
    model: BlindModel, ctx: tuple[int, ...], spec: ScoreSpec
) -> bool:
    n_m = _count(model.marked, ctx)
    n_u = _count(model.unmarked, ctx)
    if spec.min_count <= 0:
        return True
    support = min(n_m, n_u) if spec.require_both else max(n_m, n_u)
    return support >= spec.min_count


def _next_token_seen(model: BlindModel, ctx: tuple[int, ...], tok: int) -> bool:
    return (
        _tok_count(model.marked, ctx, tok) + _tok_count(model.unmarked, ctx, tok)
        >= 1
    )


def _naked_tokens(ctx: tuple[int, ...], model: BlindModel) -> tuple[int, ...]:
    """Last-k token ids with the position namespace stripped.

    FIRST_TOKEN_CTX is the empty generated prefix, not a real token.
    """
    if not ctx:
        return ()
    tokens = ctx[1:] if model.position_bucket and model.position_bucket > 0 else ctx
    if tokens == FIRST_TOKEN_CTX:
        return ()
    return tokens


def _select_score_ctx(
    ids: Sequence[int],
    i: int,
    tok: int,
    model: BlindModel,
    spec: ScoreSpec,
    *,
    prefix: Sequence[int] = (),
    order: int | None = None,
) -> tuple[int, ...] | None:
    """Context used at position i, or None to abstain.

    tokbackoff tries last-k, then last-(k-1), …, last-min_order, and keeps
    the longest context that has both-side support and (if required) the
    observed next token. min_order=2 refuses generic last-1 English.
    The opening symbol with include_first uses FIRST_TOKEN_CTX instead of
    treating the empty prefix as below min_order.
    It does not reconstruct keys.
    """
    min_order = max(1, int(spec.min_order or 1))
    score_first = bool(
        prefix
        or spec.include_first
        or spec.first_only
        or model.include_first
        or model.prompt_context
    )
    if spec.kind == "tokbackoff":
        if i == 0 and score_first and not prefix:
            # FIRST_TOKEN_CTX is the opening bucket. Naked last-k is empty,
            # which is not “below min_order English”; skip the 1..k loop.
            orders: tuple[int, ...] | range = (0,)
        else:
            orders = range(int(model.context_len), min_order - 1, -1)
    else:
        orders = (model.context_len if order is None else order,)
    for length in orders:
        ctx = _scored_ctx(
            ids, i, int(length), model.position_bucket, prefix=prefix
        )
        naked = _naked_tokens(ctx, model)
        if spec.kind == "tokbackoff" and int(length) > 0 and len(naked) < min_order:
            continue
        if spec.min_count > 0 and not _ctx_has_support(model, ctx, spec):
            continue
        if spec.require_token and not _next_token_seen(model, ctx, tok):
            continue
        return ctx
    return None


def _vocab_size(model: BlindModel) -> int:
    return max(len(model.vocab), 2)


def _witten_bell_p(
    table: NextTokenTable,
    ctx: tuple[int, ...],
    tok: int,
    *,
    alpha: float,
    v: int,
    namespaced: bool = False,
) -> float:
    n_uni = max(table.n_tokens, 1)
    p_uni = (table.unigram.get(tok, 0) + alpha) / (n_uni + alpha * v)
    if not ctx:
        return p_uni
    bucket = table.counts.get(ctx)
    shorter = shorten_ctx(ctx, namespaced=namespaced)
    if not bucket:
        if shorter is None:
            return p_uni
        return _witten_bell_p(
            table, shorter, tok, alpha=alpha, v=v, namespaced=namespaced
        )
    n = int(sum(bucket.values()))
    r = len(bucket)
    c = int(bucket.get(tok, 0))
    if n <= 0:
        if shorter is None:
            return p_uni
        return _witten_bell_p(
            table, shorter, tok, alpha=alpha, v=v, namespaced=namespaced
        )
    stay = n / (n + r)
    fallback = (
        p_uni
        if shorter is None
        else _witten_bell_p(
            table, shorter, tok, alpha=alpha, v=v, namespaced=namespaced
        )
    )
    return stay * (c / n) + (1.0 - stay) * fallback


def _log_p_mode(
    table: NextTokenTable,
    ctx: tuple[int, ...],
    tok: int,
    *,
    model: BlindModel,
    kind: str,
    order: int | None = None,
) -> float:
    v = _vocab_size(model)
    namespaced = int(getattr(model, "position_bucket", 0) or 0) > 0
    if kind == "unigram":
        return _log_prob(
            table, (), tok, alpha=model.alpha, v=v, backoff=False
        )
    if kind == "interpolate":
        p = _witten_bell_p(
            table, ctx, tok, alpha=model.alpha, v=v, namespaced=namespaced
        )
        return math.log(max(p, 1e-18))
    use_ctx = ctx if order is None else clip_ctx_order(
        ctx, order, namespaced=namespaced
    )
    backoff = kind == "backoff" or model.backoff
    return _log_prob(
        table,
        use_ctx,
        tok,
        alpha=model.alpha,
        v=v,
        backoff=backoff,
        namespaced=namespaced,
    )


def _ctx_from_full(
    ctx: tuple[int, ...], order: int, *, namespaced: bool = False
) -> tuple[int, ...]:
    return clip_ctx_order(ctx, order, namespaced=namespaced)


def score_sequence_detail(
    ids: Sequence[int],
    model: BlindModel,
    spec: ScoreSpec | None = None,
    *,
    prefix: Sequence[int] = (),
    score_span: tuple[int, int] | None = None,
) -> ScoreDetail:
    spec = spec or ScoreSpec()
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("transfer scorer consulted keys / hash_iv / g-values")
    kind = spec.kind
    if kind == "hitmass":
        inner = score_sequence_detail(
            ids,
            model,
            ScoreSpec(
                kind="gated",
                min_count=max(spec.min_count, 1),
                instance=spec.instance,
                include_first=spec.include_first,
                first_only=spec.first_only,
            ),
            prefix=prefix,
            score_span=score_span,
        )
        if inner.n_positions <= 0:
            return inner
        mass = inner.n_used / inner.n_positions
        return ScoreDetail(inner.lr * mass, inner.n_used, inner.n_positions)
    if kind == "mix":
        orders = spec.mix_orders or (1, model.context_len)
        parts = [
            score_sequence_detail(
                ids,
                model,
                ScoreSpec(
                    kind="hard-order",
                    mix_orders=(order,),
                    instance=spec.instance,
                    include_first=spec.include_first,
                    first_only=spec.first_only,
                ),
                prefix=prefix,
                score_span=score_span,
            )
            for order in orders
            if 1 <= order <= model.context_len
        ]
        used = [p for p in parts if p.n_positions]
        if not used:
            return ScoreDetail(0.0, 0, 0)
        lr = sum(p.lr for p in used) / len(used)
        n_used = int(sum(p.n_used for p in used) / len(used))
        n_pos = max(p.n_positions for p in used)
        return ScoreDetail(lr, n_used, n_pos)

    order: int | None = None
    if kind == "hard-order":
        order = spec.mix_orders[0] if spec.mix_orders else model.context_len
        kind = "hard"
    log_kind = "gated" if spec.kind == "tokbackoff" else kind

    score_first = bool(
        prefix
        or spec.include_first
        or spec.first_only
        or model.include_first
        or model.prompt_context
    )
    total = 0.0
    weight_sum = 0.0
    n_used = 0
    n_positions = 0
    for i in score_index_range(len(ids), score_span):
        tok = ids[i]
        if i == 0 and not score_first:
            continue
        if spec.first_only and i > 0:
            continue
        n_positions += 1
        t = int(tok)
        ctx = _select_score_ctx(
            ids, i, t, model, spec, prefix=prefix, order=order
        )
        if ctx is None:
            continue
        n_m = _count(model.marked, ctx)
        n_u = _count(model.unmarked, ctx)
        log_m = _log_p_mode(
            model.marked, ctx, t, model=model, kind=log_kind, order=order
        )
        log_u = _log_p_mode(
            model.unmarked, ctx, t, model=model, kind=log_kind, order=order
        )
        delta = log_m - log_u
        if spec.shrinkage_tau > 0.0:
            n_obs = min(n_m, n_u)
            w = n_obs / (n_obs + spec.shrinkage_tau)
        else:
            w = 1.0
        if w <= 0.0:
            continue
        total += w * delta
        weight_sum += w
        n_used += 1
    if n_used == 0 or weight_sum == 0.0:
        return ScoreDetail(0.0, 0, n_positions)
    return ScoreDetail(total / weight_sum, n_used, n_positions)


@dataclass(frozen=True)
class HitAtom:
    """One scored last-k → next-token event. Not a watermark key."""

    i: int
    ctx: tuple[int, ...]
    tok: int
    n_m: int
    n_u: int
    c_m: int
    c_u: int
    delta: float
    unseen_next: bool


def gated_hit_trace(
    ids: Sequence[int],
    model: BlindModel,
    spec: ScoreSpec | None = None,
    *,
    prefix: Sequence[int] = (),
) -> list[HitAtom]:
    """Per-position hits atoms. tokhits drops rows with unseen_next."""
    spec = spec or ScoreSpec(kind="gated", min_count=1)
    if spec.kind not in ("gated", "hitmass", "tokbackoff"):
        raise ValueError("gated_hit_trace is for hits / tokhits / tokbackoff tables")
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("hit trace consulted keys / hash_iv / g-values")
    score_first = bool(
        prefix
        or spec.include_first
        or spec.first_only
        or model.include_first
        or model.prompt_context
    )
    out: list[HitAtom] = []
    for i, tok in enumerate(ids):
        if i == 0 and not score_first:
            continue
        if spec.first_only and i > 0:
            continue
        t = int(tok)
        ctx = _select_score_ctx(ids, i, t, model, spec, prefix=prefix)
        if ctx is None:
            continue
        n_m = _count(model.marked, ctx)
        n_u = _count(model.unmarked, ctx)
        c_m = _tok_count(model.marked, ctx, t)
        c_u = _tok_count(model.unmarked, ctx, t)
        unseen = c_m + c_u < 1
        log_m = _log_p_mode(
            model.marked, ctx, t, model=model, kind="gated"
        )
        log_u = _log_p_mode(
            model.unmarked, ctx, t, model=model, kind="gated"
        )
        out.append(
            HitAtom(
                i=i,
                ctx=ctx,
                tok=t,
                n_m=n_m,
                n_u=n_u,
                c_m=c_m,
                c_u=c_u,
                delta=float(log_m - log_u),
                unseen_next=unseen,
            )
        )
    return out


def interpolate_trace(
    ids: Sequence[int],
    model: BlindModel,
    spec: ScoreSpec | None = None,
    *,
    prefix: Sequence[int] = (),
) -> list[HitAtom]:
    """Per-position Witten–Bell interpolate atoms. Not a new scorer."""
    spec = spec or COUNT_SPECS["interpolate"]
    if spec.kind != "interpolate":
        raise ValueError("interpolate_trace is for interpolate tables")
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("interpolate trace consulted keys / hash_iv / g-values")
    score_first = bool(
        prefix
        or spec.include_first
        or spec.first_only
        or model.include_first
        or model.prompt_context
    )
    out: list[HitAtom] = []
    for i, tok in enumerate(ids):
        if i == 0 and not score_first:
            continue
        if spec.first_only and i > 0:
            continue
        t = int(tok)
        ctx = _select_score_ctx(ids, i, t, model, spec, prefix=prefix)
        if ctx is None:
            continue
        n_m = _count(model.marked, ctx)
        n_u = _count(model.unmarked, ctx)
        c_m = _tok_count(model.marked, ctx, t)
        c_u = _tok_count(model.unmarked, ctx, t)
        unseen = c_m + c_u < 1
        log_m = _log_p_mode(
            model.marked, ctx, t, model=model, kind="interpolate"
        )
        log_u = _log_p_mode(
            model.unmarked, ctx, t, model=model, kind="interpolate"
        )
        out.append(
            HitAtom(
                i=i,
                ctx=ctx,
                tok=t,
                n_m=n_m,
                n_u=n_u,
                c_m=c_m,
                c_u=c_u,
                delta=float(log_m - log_u),
                unseen_next=unseen,
            )
        )
    return out


def score_sequence(
    ids: Sequence[int],
    model: BlindModel,
    spec: ScoreSpec | None = None,
    *,
    prefix: Sequence[int] = (),
    score_span: tuple[int, int] | None = None,
) -> float:
    return score_sequence_detail(
        ids, model, spec, prefix=prefix, score_span=score_span
    ).lr


def splitmix64(x: int) -> int:
    x = (x + _GOLDEN) & MASK64
    z = x
    z = (z ^ (z >> 30)) * _MIX1 & MASK64
    z = (z ^ (z >> 27)) * _MIX2 & MASK64
    return z ^ (z >> 31)


def hash_context(ctx: tuple[int, ...], seed: int) -> int:
    h = seed & MASK64
    for tok in ctx:
        h = splitmix64(h ^ (int(tok) & MASK64))
    return splitmix64(h ^ (len(ctx) & MASK64))


def _hash_seeds(n_hashes: int, seed: int) -> tuple[int, ...]:
    out = []
    x = seed & MASK64
    for _ in range(n_hashes):
        x = splitmix64(x ^ _GOLDEN)
        out.append(x)
    return tuple(out)


@dataclass
class HashPoolModel:
    n_hashes: int
    n_buckets: int
    context_len: int
    seeds: tuple[int, ...]
    marked: list[dict[int, Counter]]
    unmarked: list[dict[int, Counter]]
    marked_unigram: Counter
    unmarked_unigram: Counter
    n_marked: int
    n_unmarked: int
    alpha: float
    vocab: set[int] = field(default_factory=set)
    alphabet: str = "tokens"
    used_keys: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False
    position_bucket: int = 0
    exact_len: bool = False
    drop_one: bool = False
    mask_one: bool = False

    @property
    def instance(self) -> str:
        return f"key-free-{hash_fit_reader(self)}"


HASH_SCORE_MODES = (
    "auto",
    "hashpool",
    "hashtok",
    "hashtok2",
    "hashtoklen",
    "hashtoklen2",
    "hashskip",
    "hashskip2",
    "hashmask",
    "hashmask2",
    "",
)


def hash_fit_reader(model: HashPoolModel) -> str:
    """Mixer encoded in the tables, not a score-time switch."""
    if model.alphabet == "bytes":
        return "surface"
    if model.drop_one:
        return "hashskip"
    if model.mask_one:
        return "hashmask"
    if model.exact_len:
        return "hashtoklen"
    if model.position_bucket > 0:
        return "pospool"
    return "hashpool"


def resolve_hash_score_mode(
    model: HashPoolModel,
    mode: str = "auto",
    *,
    stored_reader: str = "",
) -> str:
    """Pick a hash reader that matches the fitted mixer.

    ``auto`` follows drop_one / mask_one / exact_len. Occupancy hashpool
    tables stay Laplace unless the file stored a hashtok reader. Explicit
    hashtoklen on a non-exact table is refused.
    """
    raw = (mode or "auto").strip().lower()
    mixer = hash_fit_reader(model)
    allowed = (
        "hashpool",
        "hashtok",
        "hashtok2",
        "hashtoklen",
        "hashtoklen2",
        "hashskip",
        "hashskip2",
        "hashmask",
        "hashmask2",
    )
    if raw not in HASH_SCORE_MODES:
        raise ValueError(
            f"tables are hashpool; --score-mode {mode} does not apply"
        )
    if raw in ("auto", ""):
        if mixer in ("hashskip", "hashmask", "hashtoklen"):
            return mixer
        stored = (stored_reader or "").strip().lower()
        if stored in ("hashtok", "hashtok2"):
            return stored
        if mixer == "pospool":
            return "hashpool"
        return "hashpool"
    drop_one = bool(model.drop_one)
    mask_one = bool(model.mask_one)
    exact = bool(model.exact_len) or drop_one or mask_one
    if raw in ("hashskip", "hashskip2"):
        if not drop_one:
            raise ValueError(
                "these tables were not fit as drop-one skip-grams; "
                "refusing score-time hashskip on a different mixer"
            )
        return raw
    if raw in ("hashmask", "hashmask2"):
        if not mask_one:
            raise ValueError(
                "these tables were not fit as MASK-replace templates; "
                "refusing score-time hashmask on a different mixer"
            )
        return raw
    if raw in ("hashtoklen", "hashtoklen2"):
        if drop_one:
            raise ValueError(
                "these tables are drop-one skip-grams; use --score-mode "
                "hashskip or hashskip2"
            )
        if mask_one:
            raise ValueError(
                "these tables are MASK-replace templates; use --score-mode "
                "hashmask or hashmask2"
            )
        if not exact:
            raise ValueError(
                "these tables were not fit with exact_len; refusing "
                "score-time hashtoklen on a truncated-context mixer"
            )
        return raw
    if raw in ("hashtok", "hashtok2"):
        if drop_one:
            raise ValueError(
                "these tables are drop-one skip-grams; use --score-mode "
                "hashskip or hashskip2"
            )
        if mask_one:
            raise ValueError(
                "these tables are MASK-replace templates; use --score-mode "
                "hashmask or hashmask2"
            )
        if exact:
            raise ValueError(
                "these tables were fit with exact_len; use --score-mode "
                "hashtoklen, not hashtok"
            )
        return raw
    if raw == "hashpool":
        if drop_one or mask_one or bool(model.exact_len):
            raise ValueError(
                f"these tables were fit as {mixer}; refusing Laplace "
                "hashpool on a different mixer"
            )
        return raw
    if raw not in allowed:
        raise ValueError(
            f"tables are hashpool; --score-mode {mode} does not apply"
        )
    return raw


def hash_score_min_count(mode: str) -> int:
    return 2 if str(mode).endswith("2") else 1


def hash_ctx_len(ctx: tuple[int, ...], position_bucket: int = 0) -> int:
    """How many token ids were hashed, excluding a position namespace.

    Order-k tables must see length-k contexts. A shorter prefix hashed
    into a longer-order mixer is not that order's n-gram.
    """
    if not ctx:
        return 0
    tokens = ctx[1:] if int(position_bucket or 0) > 0 else ctx
    if tokens == FIRST_TOKEN_CTX:
        return 0
    return len(tokens)


def skip_views(
    ctx: tuple[int, ...],
    position_bucket: int = 0,
) -> list[tuple[int, ...]]:
    """Exact last-k with one token dropped.

    Each view is tagged `(SKIP_TAG, drop_index, *kept)` so a drop-one
    4-gram is not a last-3. Occupancy-free hashing of these views asks
    whether a coarsened official 5-gram still shares a next-token
    preference. Not SynthID's secret hash.
    """
    if int(position_bucket or 0) > 0:
        if not ctx:
            return []
        ns = (int(ctx[0]),)
        tokens = ctx[1:]
    else:
        ns = ()
        tokens = ctx
    if not tokens or tokens == FIRST_TOKEN_CTX or len(tokens) < 2:
        return []
    views: list[tuple[int, ...]] = []
    for drop_i, _tok in enumerate(tokens):
        kept = tuple(int(t) for j, t in enumerate(tokens) if j != drop_i)
        views.append(ns + (SKIP_TAG, int(drop_i)) + kept)
    return views


def mask_views(
    ctx: tuple[int, ...],
    position_bucket: int = 0,
) -> list[tuple[int, ...]]:
    """Exact last-k with one token replaced by MASK_TAG.

    Length stays k, so a masked 4-gram is not a last-3 and not a
    tagged skip-gram. Occupancy-free hashing of these templates asks
    whether a coarsened official 5-gram still shares a next-token
    preference. Not SynthID's secret hash.
    """
    if int(position_bucket or 0) > 0:
        if not ctx:
            return []
        ns = (int(ctx[0]),)
        tokens = ctx[1:]
    else:
        ns = ()
        tokens = ctx
    if not tokens or tokens == FIRST_TOKEN_CTX or len(tokens) < 2:
        return []
    views: list[tuple[int, ...]] = []
    for mask_i, _tok in enumerate(tokens):
        masked = tuple(
            MASK_TAG if j == mask_i else int(t) for j, t in enumerate(tokens)
        )
        views.append(ns + masked)
    return views


def hashed_ctx_views(
    ctx: tuple[int, ...],
    *,
    position_bucket: int = 0,
    drop_one: bool = False,
    mask_one: bool = False,
) -> list[tuple[int, ...]]:
    if drop_one and mask_one:
        raise ValueError("drop-one skip-grams and MASK replace are different mixers")
    if drop_one:
        return skip_views(ctx, position_bucket)
    if mask_one:
        return mask_views(ctx, position_bucket)
    return [ctx]


def _add_hash_seq(
    tables: list[dict[int, Counter]],
    unigram: Counter,
    ids: Sequence[int],
    *,
    context_len: int,
    seeds: Sequence[int],
    n_buckets: int,
    position_bucket: int = 0,
    exact_len: bool = False,
    drop_one: bool = False,
    mask_one: bool = False,
) -> int:
    n = 0
    for i, tok in enumerate(ids):
        t = int(tok)
        unigram[t] += 1
        n += 1
        if i == 0:
            continue
        ctx = _scored_ctx(ids, i, context_len, position_bucket)
        if exact_len and hash_ctx_len(ctx, position_bucket) != int(context_len):
            continue
        views = hashed_ctx_views(
            ctx,
            position_bucket=position_bucket,
            drop_one=bool(drop_one),
            mask_one=bool(mask_one),
        )
        if not views:
            continue
        for view in views:
            for h, seed in enumerate(seeds):
                bucket = hash_context(view, seed) % n_buckets
                tables[h].setdefault(bucket, Counter())[t] += 1
    return n


def fit_hashpool(
    marked_seqs: Iterable[Sequence[int]],
    unmarked_seqs: Iterable[Sequence[int]],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    alpha: float = DEFAULT_ALPHA,
    seed: int = 20260831,
    alphabet: str = "tokens",
    position_bucket: int = 0,
    exact_len: bool = False,
    drop_one: bool = False,
    mask_one: bool = False,
) -> HashPoolModel:
    drop_one = bool(drop_one)
    mask_one = bool(mask_one)
    if drop_one and mask_one:
        raise ValueError("drop-one skip-grams and MASK replace are different mixers")
    exact_len = bool(exact_len) or drop_one or mask_one
    seeds = _hash_seeds(n_hashes, seed)
    marked = [defaultdict(Counter) for _ in range(n_hashes)]
    unmarked = [defaultdict(Counter) for _ in range(n_hashes)]
    marked_uni: Counter = Counter()
    unmarked_uni: Counter = Counter()
    n_m = n_u = 0
    for seq in marked_seqs:
        n_m += _add_hash_seq(
            marked,
            marked_uni,
            seq,
            context_len=context_len,
            seeds=seeds,
            n_buckets=n_buckets,
            position_bucket=position_bucket,
            exact_len=bool(exact_len),
            drop_one=drop_one,
            mask_one=mask_one,
        )
    for seq in unmarked_seqs:
        n_u += _add_hash_seq(
            unmarked,
            unmarked_uni,
            seq,
            context_len=context_len,
            seeds=seeds,
            n_buckets=n_buckets,
            position_bucket=position_bucket,
            exact_len=bool(exact_len),
            drop_one=drop_one,
            mask_one=mask_one,
        )
    vocab = set(marked_uni) | set(unmarked_uni)
    if alphabet == "bytes":
        vocab = set(range(256)) | vocab
    return HashPoolModel(
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        context_len=context_len,
        seeds=seeds,
        marked=[dict(t) for t in marked],
        unmarked=[dict(t) for t in unmarked],
        marked_unigram=marked_uni,
        unmarked_unigram=unmarked_uni,
        n_marked=n_m,
        n_unmarked=n_u,
        alpha=alpha,
        vocab=vocab,
        alphabet=alphabet,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        position_bucket=int(position_bucket) if position_bucket > 0 else 0,
        exact_len=bool(exact_len),
        drop_one=drop_one,
        mask_one=mask_one,
    )


def fit_hashpool_twins(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    alpha: float = DEFAULT_ALPHA,
    seed: int = 20260831,
    position_bucket: int = 0,
    exact_len: bool = False,
    drop_one: bool = False,
    mask_one: bool = False,
) -> HashPoolModel:
    return fit_hashpool(
        [ids for t in twins for ids in t.marked_seqs()],
        [ids for t in twins for ids in t.unmarked_seqs()],
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        alpha=alpha,
        seed=seed,
        position_bucket=position_bucket,
        exact_len=bool(exact_len),
        drop_one=bool(drop_one),
        mask_one=bool(mask_one),
    )


def text_to_bytes(text: str) -> list[int]:
    """UTF-8 bytes as integer 'tokens'. Not a tokenizer and not SynthID."""
    return list(text.encode("utf-8"))


DEFAULT_SURFACE_CONTEXT = 8


def fit_surface_twins(
    twins: Sequence[Twin],
    *,
    context_len: int = DEFAULT_SURFACE_CONTEXT,
    n_hashes: int = 8,
    n_buckets: int = 256,
    alpha: float = DEFAULT_ALPHA,
    seed: int = 20260831,
) -> HashPoolModel:
    """Hash-pool last-k bytes of the raw string. Tokenizer-agnostic."""
    return fit_hashpool(
        [text_to_bytes(s) for t in twins for s in t.marked_texts()],
        [text_to_bytes(s) for t in twins for s in t.unmarked_texts()],
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        alpha=alpha,
        seed=seed,
        alphabet="bytes",
    )


def score_surface(text: str, model: HashPoolModel) -> float:
    if model.alphabet != "bytes":
        raise ValueError("score_surface needs a byte hashpool (alphabet='bytes')")
    return score_hashpool(text_to_bytes(text), model)


def _dirichlet_logp(
    bucket: Counter | None,
    tok: int,
    *,
    fallback: Counter,
    n_fallback: int,
    alpha: float,
    v: int,
) -> float:
    if bucket:
        n = int(sum(bucket.values()))
        c = int(bucket.get(tok, 0))
        return math.log((c + alpha) / (n + alpha * v))
    n = max(n_fallback, 1)
    c = int(fallback.get(tok, 0))
    return math.log((c + alpha) / (n + alpha * v))


def hashpool_token_lr(model: HashPoolModel, ctx: tuple[int, ...], tok: int) -> float:
    """Per-position hashpool log ratio. Not SynthID's secret hash."""
    v = max(len(model.vocab), 2)
    piece = 0.0
    for h, seed in enumerate(model.seeds):
        bucket = hash_context(ctx, seed) % model.n_buckets
        piece += _dirichlet_logp(
            model.marked[h].get(bucket),
            tok,
            fallback=model.marked_unigram,
            n_fallback=model.n_marked,
            alpha=model.alpha,
            v=v,
        )
        piece -= _dirichlet_logp(
            model.unmarked[h].get(bucket),
            tok,
            fallback=model.unmarked_unigram,
            n_fallback=model.n_unmarked,
            alpha=model.alpha,
            v=v,
        )
    return piece / max(model.n_hashes, 1)


def score_hashpool_detail(
    ids: Sequence[int],
    model: HashPoolModel,
    *,
    score_span: tuple[int, int] | None = None,
) -> ScoreDetail:
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("hashpool consulted keys / hash_iv / g-values")
    total = 0.0
    n_used = 0
    n_positions = 0
    for i in score_index_range(len(ids), score_span):
        tok = ids[i]
        if i == 0:
            continue
        n_positions += 1
        ctx = _scored_ctx(ids, i, model.context_len, model.position_bucket)
        total += hashpool_token_lr(model, ctx, int(tok))
        n_used += 1
    if n_used == 0:
        return ScoreDetail(0.0, 0, n_positions)
    return ScoreDetail(total / n_used, n_used, n_positions)


def score_hashpool(
    ids: Sequence[int],
    model: HashPoolModel,
    *,
    score_span: tuple[int, int] | None = None,
) -> float:
    return score_hashpool_detail(ids, model, score_span=score_span).lr


def score_hashpool_vote(
    ids: Sequence[int],
    model: HashPoolModel,
    *,
    score_span: tuple[int, int] | None = None,
) -> float:
    """Mean sign of per-token hashpool LRs. Threshold 0 is a majority vote."""
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("hashpool consulted keys / hash_iv / g-values")
    signs: list[float] = []
    for i in score_index_range(len(ids), score_span):
        tok = ids[i]
        if i == 0:
            continue
        ctx = _scored_ctx(ids, i, model.context_len, model.position_bucket)
        delta = hashpool_token_lr(model, ctx, int(tok))
        if delta > 0.0:
            signs.append(1.0)
        elif delta < 0.0:
            signs.append(-1.0)
    if not signs:
        return 0.0
    return sum(signs) / len(signs)


def _hash_bucket_tok_count(
    layer: dict[int, Counter], bucket: int, tok: int
) -> int:
    table = layer.get(int(bucket))
    if not table:
        return 0
    return int(table.get(int(tok), 0))


def hashtok_hash_seen(
    model: HashPoolModel,
    h: int,
    bucket: int,
    tok: int,
    *,
    min_count: int = 1,
) -> bool:
    """True if this hash bucket produced tok at least min_count times.

    Occupancy-free default is 1: Laplace of an empty cell cannot vote.
    min_count=2 also skips singleton collisions. Not a watermark key.
    """
    c_m = _hash_bucket_tok_count(model.marked[h], bucket, tok)
    c_u = _hash_bucket_tok_count(model.unmarked[h], bucket, tok)
    return c_m + c_u >= max(int(min_count), 1)


def hashtok_token_lr(
    model: HashPoolModel,
    ctx: tuple[int, ...],
    tok: int,
    *,
    min_count: int = 1,
) -> float | None:
    """Mean hashpool LR over hashes whose bucket saw tok. None if none did.

    Occupancy-free: a hash that never produced this next token is skipped,
    so Dirichlet/Laplace on empty cells cannot vote. Same laboratory mixer
    as hashpool. Not SynthID's secret hash.
    """
    v = max(len(model.vocab), 2)
    pieces: list[float] = []
    floor = max(int(min_count), 1)
    for h, seed in enumerate(model.seeds):
        bucket = hash_context(ctx, seed) % model.n_buckets
        if not hashtok_hash_seen(model, h, bucket, tok, min_count=floor):
            continue
        piece = _dirichlet_logp(
            model.marked[h].get(bucket),
            tok,
            fallback=model.marked_unigram,
            n_fallback=model.n_marked,
            alpha=model.alpha,
            v=v,
        )
        piece -= _dirichlet_logp(
            model.unmarked[h].get(bucket),
            tok,
            fallback=model.unmarked_unigram,
            n_fallback=model.n_unmarked,
            alpha=model.alpha,
            v=v,
        )
        pieces.append(piece)
    if not pieces:
        return None
    return pieces[0] if len(pieces) == 1 else sum(pieces) / len(pieces)


def score_hashtok_detail(
    ids: Sequence[int],
    model: HashPoolModel,
    *,
    exact_len: bool | None = None,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> ScoreDetail:
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("hashtok consulted keys / hash_iv / g-values")
    exact = bool(model.exact_len if exact_len is None else exact_len) or bool(
        model.drop_one
    ) or bool(model.mask_one)
    floor = max(int(min_count), 1)
    total = 0.0
    n_used = 0
    n_positions = 0
    for i in score_index_range(len(ids), score_span):
        tok = ids[i]
        if i == 0:
            continue
        n_positions += 1
        ctx = _scored_ctx(ids, i, model.context_len, model.position_bucket)
        if exact and hash_ctx_len(ctx, model.position_bucket) != int(model.context_len):
            continue
        views = hashed_ctx_views(
            ctx,
            position_bucket=model.position_bucket,
            drop_one=bool(model.drop_one),
            mask_one=bool(model.mask_one),
        )
        pieces: list[float] = []
        for view in views:
            delta = hashtok_token_lr(
                model, view, int(tok), min_count=floor
            )
            if delta is not None:
                pieces.append(delta)
        if not pieces:
            continue
        total += pieces[0] if len(pieces) == 1 else sum(pieces) / len(pieces)
        n_used += 1
    if n_used == 0:
        return ScoreDetail(0.0, 0, n_positions)
    return ScoreDetail(total / n_used, n_used, n_positions)


def score_hashtok(
    ids: Sequence[int],
    model: HashPoolModel,
    *,
    exact_len: bool | None = None,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> float:
    """Hashpool LR using only hashes that saw the observed next token."""
    return score_hashtok_detail(
        ids,
        model,
        exact_len=exact_len,
        min_count=min_count,
        score_span=score_span,
    ).lr


def score_hashskip(
    ids: Sequence[int],
    model: HashPoolModel,
    *,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> float:
    """Occupancy-free drop-one skip-grams of exact last-k. Still no keys."""
    if not model.drop_one:
        raise ValueError("score_hashskip needs a drop-one hashpool")
    return score_hashtok_detail(
        ids, model, min_count=min_count, score_span=score_span
    ).lr


def score_hashmask(
    ids: Sequence[int],
    model: HashPoolModel,
    *,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> float:
    """Occupancy-free MASK replace of exact last-k. Still no keys."""
    if not model.mask_one:
        raise ValueError("score_hashmask needs a MASK-replace hashpool")
    if model.drop_one:
        raise ValueError("score_hashmask cannot read drop-one skip tables")
    return score_hashtok_detail(
        ids, model, min_count=min_count, score_span=score_span
    ).lr


def hashtok_trace(
    ids: Sequence[int],
    model: HashPoolModel,
    *,
    min_count: int = 1,
) -> list[dict]:
    """Per-position observed-token hash collisions. Still no keys."""
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("hashtok trace consulted keys / hash_iv / g-values")
    floor = max(int(min_count), 1)
    rows: list[dict] = []
    for i, tok in enumerate(ids):
        if i == 0:
            continue
        t = int(tok)
        ctx = _scored_ctx(ids, i, model.context_len, model.position_bucket)
        ctx_n = hash_ctx_len(ctx, model.position_bucket)
        exact = bool(model.exact_len) or bool(model.drop_one) or bool(model.mask_one)
        if exact and ctx_n != int(model.context_len):
            rows.append(
                {
                    "i": int(i),
                    "tok": t,
                    "ctx": [int(x) for x in ctx],
                    "ctx_len": ctx_n,
                    "exact_ok": False,
                    "drop_one": bool(model.drop_one),
                    "mask_one": bool(model.mask_one),
                    "n_hashes_seen": 0,
                    "n_hashes": int(model.n_hashes),
                    "c_m": 0,
                    "c_u": 0,
                    "delta": None,
                    "hashpool_delta": 0.0,
                    "hashes": [],
                    "skip_views": [],
                }
            )
            continue
        views = hashed_ctx_views(
            ctx,
            position_bucket=model.position_bucket,
            drop_one=bool(model.drop_one),
            mask_one=bool(model.mask_one),
        )
        skip_rows: list[dict] = []
        pieces: list[float] = []
        hashes: list[dict] = []
        c_m_sum = 0
        c_u_sum = 0
        n_seen = 0
        multi_view = bool(model.drop_one) or bool(model.mask_one)
        for drop_i, view in enumerate(views):
            view_hashes: list[dict] = []
            view_seen = 0
            view_cm = 0
            view_cu = 0
            for h, seed in enumerate(model.seeds):
                bucket = hash_context(view, seed) % model.n_buckets
                c_m = _hash_bucket_tok_count(model.marked[h], bucket, t)
                c_u = _hash_bucket_tok_count(model.unmarked[h], bucket, t)
                seen = c_m + c_u >= floor
                if seen:
                    view_seen += 1
                    view_cm += c_m
                    view_cu += c_u
                    n_seen += 1
                    c_m_sum += c_m
                    c_u_sum += c_u
                rec = {
                    "h": int(h),
                    "bucket": int(bucket),
                    "c_m": c_m,
                    "c_u": c_u,
                    "seen": seen,
                }
                view_hashes.append(rec)
                if not multi_view:
                    hashes.append(rec)
            view_delta = hashtok_token_lr(model, view, t, min_count=floor)
            if view_delta is not None:
                pieces.append(view_delta)
            if multi_view:
                view_row = {
                    "drop_i": int(drop_i),
                    "view": [int(x) for x in view],
                    "n_hashes_seen": view_seen,
                    "c_m": view_cm,
                    "c_u": view_cu,
                    "delta": None if view_delta is None else float(view_delta),
                    "hashes": view_hashes,
                }
                if model.mask_one:
                    view_row["mask_i"] = int(drop_i)
                skip_rows.append(view_row)
        if not multi_view:
            delta = hashtok_token_lr(model, ctx, t, min_count=floor)
            pool = hashpool_token_lr(model, ctx, t)
        else:
            delta = None if not pieces else (
                pieces[0] if len(pieces) == 1 else sum(pieces) / len(pieces)
            )
            pool = 0.0
        rows.append(
            {
                "i": int(i),
                "tok": t,
                "ctx": [int(x) for x in ctx],
                "ctx_len": ctx_n,
                "exact_ok": ctx_n == int(model.context_len),
                "drop_one": bool(model.drop_one),
                "mask_one": bool(model.mask_one),
                "n_hashes_seen": n_seen,
                "n_hashes": int(model.n_hashes),
                "c_m": c_m_sum,
                "c_u": c_u_sum,
                "delta": None if delta is None else float(delta),
                "hashpool_delta": float(pool),
                "hashes": hashes,
                "skip_views": skip_rows,
            }
        )
    return rows


def score_hybrid_detail(
    ids: Sequence[int],
    count_model: BlindModel,
    hash_model: HashPoolModel,
    *,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> ScoreDetail:
    """Exact shared n-grams when both sides saw them; hashpool otherwise.

    Still no keys / hash_iv / g-values. The hash is the laboratory mixer.
    """
    if (
        count_model.used_keys
        or count_model.used_hash_iv
        or count_model.used_g_values
        or hash_model.used_keys
        or hash_model.used_hash_iv
        or hash_model.used_g_values
    ):
        raise RuntimeError("hybrid consulted keys / hash_iv / g-values")
    total = 0.0
    n_used = 0
    n_positions = 0
    for i in score_index_range(len(ids), score_span):
        if i == 0:
            continue
        n_positions += 1
        t = int(ids[i])
        ctx = _ctx(ids, i, count_model.context_len)
        n_m = _count(count_model.marked, ctx)
        n_u = _count(count_model.unmarked, ctx)
        if min(n_m, n_u) >= min_count:
            log_m = _log_p_mode(
                count_model.marked, ctx, t, model=count_model, kind="hard"
            )
            log_u = _log_p_mode(
                count_model.unmarked, ctx, t, model=count_model, kind="hard"
            )
            delta = log_m - log_u
        else:
            hctx = _ctx(ids, i, hash_model.context_len)
            delta = hashpool_token_lr(hash_model, hctx, t)
        total += delta
        n_used += 1
    if n_used == 0:
        return ScoreDetail(0.0, 0, n_positions)
    return ScoreDetail(total / n_used, n_used, n_positions)


def score_hybrid(
    ids: Sequence[int],
    count_model: BlindModel,
    hash_model: HashPoolModel,
    *,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> float:
    return score_hybrid_detail(
        ids, count_model, hash_model, min_count=min_count, score_span=score_span
    ).lr


def score_tokhybrid_detail(
    ids: Sequence[int],
    count_model: BlindModel,
    hash_model: HashPoolModel,
    *,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> ScoreDetail:
    """Exact tokhits when both sides saw the n-gram and next token; else hashtok.

    Occupancy-free analog of hybrid. Laplace on an unseen next token cannot
    vote, on either the exact table or a colliding hash. Still no keys.
    """
    if (
        count_model.used_keys
        or count_model.used_hash_iv
        or count_model.used_g_values
        or hash_model.used_keys
        or hash_model.used_hash_iv
        or hash_model.used_g_values
    ):
        raise RuntimeError("tokhybrid consulted keys / hash_iv / g-values")
    spec = COUNT_SPECS["tokhits"]
    floor = max(int(min_count), 1)
    total = 0.0
    n_used = 0
    n_positions = 0
    for i in score_index_range(len(ids), score_span):
        if i == 0:
            continue
        n_positions += 1
        t = int(ids[i])
        ctx = _select_score_ctx(ids, i, t, count_model, spec)
        if ctx is not None:
            log_m = _log_p_mode(
                count_model.marked, ctx, t, model=count_model, kind="gated"
            )
            log_u = _log_p_mode(
                count_model.unmarked, ctx, t, model=count_model, kind="gated"
            )
            delta = log_m - log_u
        else:
            hctx = _scored_ctx(
                ids, i, hash_model.context_len, hash_model.position_bucket
            )
            hashed = hashtok_token_lr(hash_model, hctx, t, min_count=floor)
            if hashed is None:
                continue
            delta = hashed
        total += delta
        n_used += 1
    if n_used == 0:
        return ScoreDetail(0.0, 0, n_positions)
    return ScoreDetail(total / n_used, n_used, n_positions)


def score_tokhybrid(
    ids: Sequence[int],
    count_model: BlindModel,
    hash_model: HashPoolModel,
    *,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> float:
    return score_tokhybrid_detail(
        ids, count_model, hash_model, min_count=min_count, score_span=score_span
    ).lr


def score_hashtokgap_detail(
    ids: Sequence[int],
    count_model: BlindModel,
    hash_model: HashPoolModel,
    *,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> ScoreDetail:
    """Hashtok only where exact tokhits abstains. Occupancy-free residual.

    Positions whose exact last-k and next token were seen on both training
    sides are skipped. Remaining positions use colliding hashes that saw
    the next token. Laplace cannot vote. Still no keys.
    """
    if (
        count_model.used_keys
        or count_model.used_hash_iv
        or count_model.used_g_values
        or hash_model.used_keys
        or hash_model.used_hash_iv
        or hash_model.used_g_values
    ):
        raise RuntimeError("hashtokgap consulted keys / hash_iv / g-values")
    spec = COUNT_SPECS["tokhits"]
    floor = max(int(min_count), 1)
    total = 0.0
    n_used = 0
    n_positions = 0
    for i in score_index_range(len(ids), score_span):
        if i == 0:
            continue
        n_positions += 1
        t = int(ids[i])
        if _select_score_ctx(ids, i, t, count_model, spec) is not None:
            continue
        hctx = _scored_ctx(
            ids, i, hash_model.context_len, hash_model.position_bucket
        )
        hashed = hashtok_token_lr(hash_model, hctx, t, min_count=floor)
        if hashed is None:
            continue
        total += hashed
        n_used += 1
    if n_used == 0:
        return ScoreDetail(0.0, 0, n_positions)
    return ScoreDetail(total / n_used, n_used, n_positions)


def score_hashtokgap(
    ids: Sequence[int],
    count_model: BlindModel,
    hash_model: HashPoolModel,
    *,
    min_count: int = 1,
    score_span: tuple[int, int] | None = None,
) -> float:
    return score_hashtokgap_detail(
        ids, count_model, hash_model, min_count=min_count, score_span=score_span
    ).lr


@dataclass
class HashMixModel:
    orders: tuple[int, ...]
    models: dict[int, HashPoolModel]
    used_keys: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False
    exact_len: bool = False

    @property
    def instance(self) -> str:
        return "key-free-hashtoklenbackoff" if self.exact_len else "key-free-hashmix"


def fit_hashmix_twins(
    twins: Sequence[Twin],
    *,
    orders: Sequence[int] = (1, 2, 4),
    n_hashes: int = 8,
    n_buckets: int = 256,
    alpha: float = DEFAULT_ALPHA,
    seed: int = 20260831,
    exact_len: bool = False,
) -> HashMixModel:
    models: dict[int, HashPoolModel] = {}
    used_keys = used_hash = used_g = False
    for order in orders:
        models[int(order)] = fit_hashpool_twins(
            twins,
            context_len=int(order),
            n_hashes=n_hashes,
            n_buckets=n_buckets,
            alpha=alpha,
            seed=seed + int(order),
            exact_len=bool(exact_len),
        )
        m = models[int(order)]
        used_keys = used_keys or m.used_keys
        used_hash = used_hash or m.used_hash_iv
        used_g = used_g or m.used_g_values
    return HashMixModel(
        orders=tuple(int(o) for o in orders),
        models=models,
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
        exact_len=bool(exact_len),
    )


def score_hashmix(
    ids: Sequence[int],
    model: HashMixModel,
    *,
    score_span: tuple[int, int] | None = None,
) -> float:
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("hashmix consulted keys / hash_iv / g-values")
    if not model.orders:
        return 0.0
    total = 0.0
    for order in model.orders:
        total += score_hashpool(ids, model.models[order], score_span=score_span)
    return total / len(model.orders)


HASHBACKOFF_ORDERS: tuple[int, ...] = (1, 2, 3, 4)
HASH_CASCADE_READERS: tuple[str, ...] = (
    "hashtok",
    "hashtoklen",
    "hashtokbackoff",
    "hashtokbackoff2",
    "hashtoklenbackoff",
    "hashtoklenbackoff2",
)


def score_hashed_reader_detail(
    ids: Sequence[int],
    reader: str,
    *,
    hash_model: HashPoolModel | None = None,
    hash_len_model: HashPoolModel | None = None,
    mix_model: HashMixModel | None = None,
    mix_len_model: HashMixModel | None = None,
) -> ScoreDetail:
    """Occupancy-free hashed ScoreDetail for cascade count channels.

    Still no keys, hash_iv, or g-values. Not detector_mean.
    """
    name = str(reader or "").strip()
    if name == "hashtok":
        if hash_model is None:
            raise ValueError("hashtok needs a hashpool model")
        return score_hashtok_detail(ids, hash_model)
    if name == "hashtoklen":
        model = hash_len_model if hash_len_model is not None else hash_model
        if model is None:
            raise ValueError("hashtoklen needs an exact-length hashpool")
        return score_hashtok_detail(ids, model, exact_len=True)
    if name == "hashtokbackoff":
        if mix_model is None:
            raise ValueError("hashtokbackoff needs per-order hash tables")
        return score_hashtokbackoff_detail(ids, mix_model, min_order=1)
    if name == "hashtokbackoff2":
        if mix_model is None:
            raise ValueError("hashtokbackoff2 needs per-order hash tables")
        return score_hashtokbackoff_detail(ids, mix_model, min_order=2)
    if name == "hashtoklenbackoff":
        if mix_len_model is None:
            raise ValueError("hashtoklenbackoff needs exact-length mix tables")
        return score_hashtokbackoff_detail(
            ids, mix_len_model, min_order=1, exact_len=True
        )
    if name == "hashtoklenbackoff2":
        if mix_len_model is None:
            raise ValueError("hashtoklenbackoff2 needs exact-length mix tables")
        return score_hashtokbackoff_detail(
            ids, mix_len_model, min_order=2, exact_len=True
        )
    raise ValueError(
        f"unknown hashed reader {reader!r}; choose "
        + ", ".join(HASH_CASCADE_READERS)
    )


def score_hashtokbackoff_detail(
    ids: Sequence[int],
    model: HashMixModel,
    *,
    min_order: int = 1,
    exact_len: bool | None = None,
    score_span: tuple[int, int] | None = None,
) -> ScoreDetail:
    """Longest per-order hashtok hit. Not occupancy hashpool, not SynthID.

    Each order has its own hash tables (same as hashmix). Last-k shrinks
    only across those fitted orders. min_order=2 refuses generic last-1.
    exact_len (default: model.exact_len) skips an order unless the hashed
    context has that many tokens. Short prefixes in a longer-order mixer
    are not that order's n-gram.
    """
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("hashtokbackoff consulted keys / hash_iv / g-values")
    floor = max(1, int(min_order or 1))
    exact = bool(model.exact_len if exact_len is None else exact_len)
    orders = sorted(
        (int(o) for o in model.orders if int(o) >= floor), reverse=True
    )
    total = 0.0
    n_used = 0
    n_positions = 0
    for i in score_index_range(len(ids), score_span):
        if i == 0:
            continue
        n_positions += 1
        t = int(ids[i])
        hit: float | None = None
        for order in orders:
            pool = model.models[int(order)]
            ctx = _scored_ctx(ids, i, pool.context_len, pool.position_bucket)
            if exact and hash_ctx_len(ctx, pool.position_bucket) != int(order):
                continue
            delta = hashtok_token_lr(pool, ctx, t)
            if delta is None:
                continue
            hit = delta
            break
        if hit is None:
            continue
        total += hit
        n_used += 1
    if n_used == 0:
        return ScoreDetail(0.0, 0, n_positions)
    return ScoreDetail(total / n_used, n_used, n_positions)


def score_hashtokbackoff(
    ids: Sequence[int],
    model: HashMixModel,
    *,
    min_order: int = 1,
    exact_len: bool | None = None,
    score_span: tuple[int, int] | None = None,
) -> float:
    return score_hashtokbackoff_detail(
        ids, model, min_order=min_order, exact_len=exact_len, score_span=score_span
    ).lr


def hashtokbackoff_trace(
    ids: Sequence[int],
    model: HashMixModel,
    *,
    min_order: int = 1,
    exact_len: bool | None = None,
) -> list[dict]:
    """Per-position longest hashed order that saw tok. Still no keys."""
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError(
            "hashtokbackoff trace consulted keys / hash_iv / g-values"
        )
    floor = max(1, int(min_order or 1))
    exact = bool(model.exact_len if exact_len is None else exact_len)
    orders = sorted(
        (int(o) for o in model.orders if int(o) >= floor), reverse=True
    )
    rows: list[dict] = []
    for i, tok in enumerate(ids):
        if i == 0:
            continue
        t = int(tok)
        tried: list[dict] = []
        chosen: int | None = None
        chosen_delta: float | None = None
        for order in orders:
            pool = model.models[int(order)]
            ctx = _scored_ctx(ids, i, pool.context_len, pool.position_bucket)
            ctx_n = hash_ctx_len(ctx, pool.position_bucket)
            exact_ok = ctx_n == int(order)
            delta = None
            n_seen = 0
            c_m = c_u = 0
            if not exact or exact_ok:
                delta = hashtok_token_lr(pool, ctx, t)
                for h, seed in enumerate(pool.seeds):
                    bucket = hash_context(ctx, seed) % pool.n_buckets
                    cm = _hash_bucket_tok_count(pool.marked[h], bucket, t)
                    cu = _hash_bucket_tok_count(pool.unmarked[h], bucket, t)
                    if cm + cu >= 1:
                        n_seen += 1
                        c_m += cm
                        c_u += cu
            tried.append(
                {
                    "order": int(order),
                    "ctx_len": ctx_n,
                    "exact_ok": exact_ok,
                    "n_hashes_seen": n_seen,
                    "c_m": c_m,
                    "c_u": c_u,
                    "delta": None if delta is None else float(delta),
                }
            )
            if chosen is None and delta is not None:
                chosen = int(order)
                chosen_delta = float(delta)
        rows.append(
            {
                "i": int(i),
                "tok": t,
                "order": chosen,
                "delta": chosen_delta,
                "tried": tried,
            }
        )
    return rows


HASHPOOL_KIND = "key-free-hashpool"
SURFACE_KIND = "key-free-surface"
HASHPOOL_TABLES = "tables.json"
POOL_KINDS = (HASHPOOL_KIND, SURFACE_KIND)


def _dump_hash_layers(layers: list[dict[int, Counter]]) -> list:
    dumped = []
    for layer in layers:
        rows = []
        for bucket in sorted(layer):
            nxt = layer[bucket]
            rows.append(
                {
                    "bucket": int(bucket),
                    "next": {str(int(k)): int(v) for k, v in sorted(nxt.items())},
                }
            )
        dumped.append(rows)
    return dumped


def _load_hash_layers(raw: list) -> list[dict[int, Counter]]:
    layers: list[dict[int, Counter]] = []
    for rows in raw:
        layer: dict[int, Counter] = {}
        for row in rows:
            layer[int(row["bucket"])] = Counter(
                {int(k): int(v) for k, v in row["next"].items()}
            )
        layers.append(layer)
    return layers


def persist_hashpool(
    model: HashPoolModel,
    out_dir: Path,
    *,
    model_name: str = "gpt2",
    pair_dir: str = "",
    n_train_prompts: int = 0,
    decision_threshold: float | None = None,
    decision_source: str = "",
    fit_prefix: int = 0,
    score_kind: str | None = None,
) -> Path:
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("refusing to persist a hashpool that used keys")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    kind = SURFACE_KIND if model.alphabet == "bytes" else HASHPOOL_KIND
    reader = hash_fit_reader(model)
    stored = str(score_kind or reader)
    payload = {
        "kind": kind,
        "alphabet": model.alphabet,
        "instance": model.instance,
        "fit_reader": reader,
        "score_kind": stored,
        "model_name": model_name,
        "pair_dir": pair_dir,
        "n_train_prompts": n_train_prompts,
        "context_len": model.context_len,
        "n_hashes": model.n_hashes,
        "n_buckets": model.n_buckets,
        "seeds": [int(s) for s in model.seeds],
        "alpha": model.alpha,
        "n_marked": model.n_marked,
        "n_unmarked": model.n_unmarked,
        "position_bucket": int(model.position_bucket),
        "exact_len": bool(model.exact_len),
        "drop_one": bool(model.drop_one),
        "mask_one": bool(model.mask_one),
        "fit_prefix": int(fit_prefix or 0),
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "vocab": sorted(int(t) for t in model.vocab),
        "marked_unigram": {
            str(int(k)): int(v) for k, v in sorted(model.marked_unigram.items())
        },
        "unmarked_unigram": {
            str(int(k)): int(v) for k, v in sorted(model.unmarked_unigram.items())
        },
        "marked": _dump_hash_layers(model.marked),
        "unmarked": _dump_hash_layers(model.unmarked),
        "caveat": (
            "Not detector_mean. Not Claude. Not Anthropic. "
            "Random context hash, not the secret SynthID hash. "
            "alphabet=bytes is UTF-8 surface pooling, not a tokenizer. "
            "A stored decision_threshold is a frozen operating point, "
            "not a universal detector."
        ),
    }
    if decision_threshold is not None:
        payload["decision_threshold"] = float(decision_threshold)
        payload["decision_source"] = str(decision_source or "unspecified")
    path = out_dir / HASHPOOL_TABLES
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def hashpool_from_payload(raw: dict) -> HashPoolModel:
    kind = str(raw.get("kind") or "")
    if kind not in POOL_KINDS:
        raise ValueError("not a key-free hashpool table")
    if raw.get("used_keys") or raw.get("used_hash_iv") or raw.get("used_g_values"):
        raise RuntimeError("hashpool file claims it used keys / hash_iv / g")
    alphabet = str(raw.get("alphabet") or ("bytes" if kind == SURFACE_KIND else "tokens"))
    return HashPoolModel(
        n_hashes=int(raw["n_hashes"]),
        n_buckets=int(raw["n_buckets"]),
        context_len=int(raw["context_len"]),
        seeds=tuple(int(s) for s in raw["seeds"]),
        marked=_load_hash_layers(raw["marked"]),
        unmarked=_load_hash_layers(raw["unmarked"]),
        marked_unigram=Counter(
            {int(k): int(v) for k, v in raw["marked_unigram"].items()}
        ),
        unmarked_unigram=Counter(
            {int(k): int(v) for k, v in raw["unmarked_unigram"].items()}
        ),
        n_marked=int(raw["n_marked"]),
        n_unmarked=int(raw["n_unmarked"]),
        alpha=float(raw["alpha"]),
        vocab=set(int(t) for t in raw["vocab"]),
        alphabet=alphabet,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        position_bucket=int(raw.get("position_bucket") or 0),
        exact_len=bool(raw.get("exact_len") or False),
        drop_one=bool(raw.get("drop_one") or False),
        mask_one=bool(raw.get("mask_one") or False),
    )


def load_hashpool(tables_dir: Path) -> HashPoolModel:
    path = Path(tables_dir)
    if path.is_dir():
        path = path / HASHPOOL_TABLES
    raw = json.loads(path.read_text())
    if raw.get("kind") not in POOL_KINDS:
        raise ValueError(f"not a key-free hashpool table: {path}")
    return hashpool_from_payload(raw)


def peek_tables_kind(tables_dir: Path) -> str:
    path = Path(tables_dir)
    if path.is_dir():
        path = path / HASHPOOL_TABLES
        if not path.is_file():
            path = Path(tables_dir) / "tables.json"
    raw = json.loads(path.read_text())
    return str(raw.get("kind") or "")


def fit_count_model(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    alpha: float = DEFAULT_ALPHA,
    position_bucket: int = 0,
    include_first: bool = False,
    prompt_context: bool = False,
) -> BlindModel:
    marked: list[Sequence[int]] = []
    unmarked: list[Sequence[int]] = []
    marked_prefixes: list[Sequence[int]] = []
    unmarked_prefixes: list[Sequence[int]] = []
    for twin in twins:
        prefix = tuple(int(x) for x in twin.prompt_ids) if prompt_context else ()
        if prompt_context and not prefix:
            raise ValueError(
                f"prompt-context fit needs prompt token ids on stem {twin.stem!r}"
            )
        for ids in twin.marked_seqs():
            marked.append(ids)
            marked_prefixes.append(prefix)
        for ids in twin.unmarked_seqs():
            unmarked.append(ids)
            unmarked_prefixes.append(prefix)
    return fit_blind(
        marked,
        unmarked,
        context_len=context_len,
        alpha=alpha,
        backoff=False,
        position_bucket=position_bucket,
        include_first=include_first,
        prompt_context=prompt_context,
        marked_prefixes=marked_prefixes,
        unmarked_prefixes=unmarked_prefixes,
    )


def count_scorer(model: BlindModel, spec: ScoreSpec):
    def _score(ids: Sequence[int], *, prefix: Sequence[int] = ()) -> float:
        if (
            spec.kind == "hard"
            and spec.min_count <= 0
            and spec.shrinkage_tau <= 0
            and not spec.first_only
        ):
            return likelihood_ratio(ids, model, prefix=prefix)
        return score_sequence(ids, model, spec, prefix=prefix)

    return _score
