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
* shrinkage — credibility-weight each token's log ratio
* mix — average last-1 and last-k log ratios
* hashpool — feature-hash the context into shared buckets
* hashvote — majority sign of per-token hashpool ratios
* hybrid — exact shared n-grams when both sides saw them, else hashpool

Hash pooling is the one extra fit. It is a stealing-style regulariser:
contexts that collide in a random hash share a next-token table, so
held-out prompts can still be scored. It does not reconstruct the
secret SynthID hash. Frozen hashpool tables can be scored later with
`indicate score` without a twin.
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
    BlindModel,
    NextTokenTable,
    Twin,
    _ctx,
    _log_prob,
    fit_blind,
    likelihood_ratio,
)

# Deterministic 64-bit constants (splitmix / golden ratio). Not watermark keys.
_GOLDEN = 0x9E3779B97F4A7C15
_MIX1 = 0xBF58476D1CE4E5B9
_MIX2 = 0x94D049BB133111EB
MASK64 = 0xFFFFFFFFFFFFFFFF


@dataclass(frozen=True)
class ScoreSpec:
    kind: str = "hard"
    min_count: int = 0
    require_both: bool = True
    shrinkage_tau: float = 0.0
    mix_orders: tuple[int, ...] = ()
    instance: str = "key-free-counts"


COUNT_SPECS: dict[str, ScoreSpec] = {
    "unigram": ScoreSpec(kind="unigram", instance="key-free-unigram"),
    "hard": ScoreSpec(kind="hard", instance="key-free-counts"),
    "backoff": ScoreSpec(kind="backoff", instance="key-free-backoff"),
    "interpolate": ScoreSpec(kind="interpolate", instance="key-free-interpolate"),
    "hits": ScoreSpec(kind="gated", min_count=1, instance="key-free-hits"),
    "gated": ScoreSpec(kind="gated", min_count=2, instance="key-free-gated"),
    "shrinkage": ScoreSpec(
        kind="shrinkage", shrinkage_tau=2.0, instance="key-free-shrinkage"
    ),
    "mix": ScoreSpec(kind="mix", mix_orders=(1, 4), instance="key-free-mix"),
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


def _vocab_size(model: BlindModel) -> int:
    return max(len(model.vocab), 2)


def _witten_bell_p(
    table: NextTokenTable,
    ctx: tuple[int, ...],
    tok: int,
    *,
    alpha: float,
    v: int,
) -> float:
    n_uni = max(table.n_tokens, 1)
    p_uni = (table.unigram.get(tok, 0) + alpha) / (n_uni + alpha * v)
    if not ctx:
        return p_uni
    bucket = table.counts.get(ctx)
    if not bucket:
        return _witten_bell_p(table, ctx[1:], tok, alpha=alpha, v=v)
    n = int(sum(bucket.values()))
    r = len(bucket)
    c = int(bucket.get(tok, 0))
    if n <= 0:
        return _witten_bell_p(table, ctx[1:], tok, alpha=alpha, v=v)
    stay = n / (n + r)
    return stay * (c / n) + (1.0 - stay) * _witten_bell_p(
        table, ctx[1:], tok, alpha=alpha, v=v
    )


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
    if kind == "unigram":
        return _log_prob(
            table, (), tok, alpha=model.alpha, v=v, backoff=False
        )
    if kind == "interpolate":
        p = _witten_bell_p(table, ctx, tok, alpha=model.alpha, v=v)
        return math.log(max(p, 1e-18))
    use_ctx = ctx if order is None else _ctx_from_full(ctx, order)
    backoff = kind == "backoff" or model.backoff
    return _log_prob(
        table, use_ctx, tok, alpha=model.alpha, v=v, backoff=backoff
    )


def _ctx_from_full(ctx: tuple[int, ...], order: int) -> tuple[int, ...]:
    if order <= 0:
        return ()
    if len(ctx) <= order:
        return ctx
    return ctx[-order:]


def score_sequence_detail(
    ids: Sequence[int],
    model: BlindModel,
    spec: ScoreSpec | None = None,
) -> ScoreDetail:
    spec = spec or ScoreSpec()
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("transfer scorer consulted keys / hash_iv / g-values")
    kind = spec.kind
    if kind == "mix":
        orders = spec.mix_orders or (1, model.context_len)
        parts = [
            score_sequence_detail(
                ids,
                model,
                ScoreSpec(kind="hard-order", mix_orders=(order,), instance=spec.instance),
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

    total = 0.0
    weight_sum = 0.0
    n_used = 0
    n_positions = 0
    for i, tok in enumerate(ids):
        if i == 0:
            continue
        n_positions += 1
        t = int(tok)
        full_ctx = _ctx(ids, i, model.context_len)
        ctx = full_ctx if order is None else _ctx(ids, i, order)
        n_m = _count(model.marked, ctx)
        n_u = _count(model.unmarked, ctx)
        if spec.min_count > 0:
            support = min(n_m, n_u) if spec.require_both else max(n_m, n_u)
            if support < spec.min_count:
                continue
        log_m = _log_p_mode(
            model.marked, ctx, t, model=model, kind=kind, order=order
        )
        log_u = _log_p_mode(
            model.unmarked, ctx, t, model=model, kind=kind, order=order
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


def score_sequence(
    ids: Sequence[int],
    model: BlindModel,
    spec: ScoreSpec | None = None,
) -> float:
    return score_sequence_detail(ids, model, spec).lr


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
    used_keys: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False

    @property
    def instance(self) -> str:
        return "key-free-hashpool"


def _add_hash_seq(
    tables: list[dict[int, Counter]],
    unigram: Counter,
    ids: Sequence[int],
    *,
    context_len: int,
    seeds: Sequence[int],
    n_buckets: int,
) -> int:
    n = 0
    for i, tok in enumerate(ids):
        t = int(tok)
        unigram[t] += 1
        n += 1
        if i == 0:
            continue
        ctx = _ctx(ids, i, context_len)
        for h, seed in enumerate(seeds):
            bucket = hash_context(ctx, seed) % n_buckets
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
) -> HashPoolModel:
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
        )
    for seq in unmarked_seqs:
        n_u += _add_hash_seq(
            unmarked,
            unmarked_uni,
            seq,
            context_len=context_len,
            seeds=seeds,
            n_buckets=n_buckets,
        )
    vocab = set(marked_uni) | set(unmarked_uni)
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
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )


def fit_hashpool_twins(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    n_hashes: int = 8,
    n_buckets: int = 256,
    alpha: float = DEFAULT_ALPHA,
    seed: int = 20260831,
) -> HashPoolModel:
    return fit_hashpool(
        [ids for t in twins for ids in t.marked_seqs()],
        [ids for t in twins for ids in t.unmarked_seqs()],
        context_len=context_len,
        n_hashes=n_hashes,
        n_buckets=n_buckets,
        alpha=alpha,
        seed=seed,
    )


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


def score_hashpool_detail(ids: Sequence[int], model: HashPoolModel) -> ScoreDetail:
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("hashpool consulted keys / hash_iv / g-values")
    total = 0.0
    n_used = 0
    n_positions = 0
    for i, tok in enumerate(ids):
        if i == 0:
            continue
        n_positions += 1
        ctx = _ctx(ids, i, model.context_len)
        total += hashpool_token_lr(model, ctx, int(tok))
        n_used += 1
    if n_used == 0:
        return ScoreDetail(0.0, 0, n_positions)
    return ScoreDetail(total / n_used, n_used, n_positions)


def score_hashpool(ids: Sequence[int], model: HashPoolModel) -> float:
    return score_hashpool_detail(ids, model).lr


def score_hashpool_vote(ids: Sequence[int], model: HashPoolModel) -> float:
    """Mean sign of per-token hashpool LRs. Threshold 0 is a majority vote."""
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("hashpool consulted keys / hash_iv / g-values")
    signs: list[float] = []
    for i, tok in enumerate(ids):
        if i == 0:
            continue
        ctx = _ctx(ids, i, model.context_len)
        delta = hashpool_token_lr(model, ctx, int(tok))
        if delta > 0.0:
            signs.append(1.0)
        elif delta < 0.0:
            signs.append(-1.0)
    if not signs:
        return 0.0
    return sum(signs) / len(signs)


def score_hybrid_detail(
    ids: Sequence[int],
    count_model: BlindModel,
    hash_model: HashPoolModel,
    *,
    min_count: int = 1,
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
    for i, tok in enumerate(ids):
        if i == 0:
            continue
        n_positions += 1
        t = int(tok)
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
) -> float:
    return score_hybrid_detail(
        ids, count_model, hash_model, min_count=min_count
    ).lr


HASHPOOL_KIND = "key-free-hashpool"
HASHPOOL_TABLES = "tables.json"


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
) -> Path:
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("refusing to persist a hashpool that used keys")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": HASHPOOL_KIND,
        "instance": model.instance,
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
            "Random context hash, not the secret SynthID hash."
        ),
    }
    path = out_dir / HASHPOOL_TABLES
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def hashpool_from_payload(raw: dict) -> HashPoolModel:
    if raw.get("kind") != HASHPOOL_KIND:
        raise ValueError("not a key-free hashpool table")
    if raw.get("used_keys") or raw.get("used_hash_iv") or raw.get("used_g_values"):
        raise RuntimeError("hashpool file claims it used keys / hash_iv / g")
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
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
    )


def load_hashpool(tables_dir: Path) -> HashPoolModel:
    path = Path(tables_dir)
    if path.is_dir():
        path = path / HASHPOOL_TABLES
    raw = json.loads(path.read_text())
    if raw.get("kind") != HASHPOOL_KIND:
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
) -> BlindModel:
    return fit_blind(
        [ids for t in twins for ids in t.marked_seqs()],
        [ids for t in twins for ids in t.unmarked_seqs()],
        context_len=context_len,
        alpha=alpha,
        backoff=False,
    )


def count_scorer(model: BlindModel, spec: ScoreSpec):
    def _score(ids: Sequence[int]) -> float:
        if spec.kind == "hard" and spec.min_count <= 0 and spec.shrinkage_tau <= 0:
            return likelihood_ratio(ids, model)
        return score_sequence(ids, model, spec)

    return _score
