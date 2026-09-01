"""Key-free marked vs unmarked likelihood on same-prompt twins.

Fits two next-token tables from token counts only. No keys, hash_iv, or
g-values. Official detector_mean is not consulted.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

from text_watermark_tools.score import load_tokenizer

# Fit knob, not ngram_len from the watermark config.
# last-1 overlaps across prompts; last-2+ is too sparse on ~12×128 tokens.
DEFAULT_CONTEXT_LEN = 1
DEFAULT_ALPHA = 0.5
# Sentinel last-k for generated token 0 when the prompt is not used as
# context. Token ids are >= 0, so -1 cannot collide. Not a watermark key.
FIRST_TOKEN_CTX = (-1,)


@dataclass
class NextTokenTable:
    context_len: int
    counts: dict[tuple[int, ...], Counter] = field(default_factory=dict)
    unigram: Counter = field(default_factory=Counter)
    n_tokens: int = 0


@dataclass
class BlindModel:
    marked: NextTokenTable
    unmarked: NextTokenTable
    context_len: int
    alpha: float
    vocab: set[int] = field(default_factory=set)
    backoff: bool = False
    used_keys: bool = False
    used_hash_iv: bool = False
    used_g_values: bool = False
    position_bucket: int = 0
    include_first: bool = False
    prompt_context: bool = False


@dataclass
class Twin:
    stem: str
    marked_text: str
    unmarked_text: str
    marked_ids: list[int]
    unmarked_ids: list[int]
    extra_marked_ids: list[list[int]] = field(default_factory=list)
    extra_unmarked_ids: list[list[int]] = field(default_factory=list)
    extra_marked_text: list[str] = field(default_factory=list)
    extra_unmarked_text: list[str] = field(default_factory=list)
    prompt_text: str = ""
    prompt_ids: list[int] = field(default_factory=list)

    def marked_seqs(self) -> list[list[int]]:
        return [self.marked_ids, *self.extra_marked_ids]

    def unmarked_seqs(self) -> list[list[int]]:
        return [self.unmarked_ids, *self.extra_unmarked_ids]

    def marked_texts(self) -> list[str]:
        return [self.marked_text, *self.extra_marked_text]

    def unmarked_texts(self) -> list[str]:
        return [self.unmarked_text, *self.extra_unmarked_text]

    def clip_draws(self, max_draws: int) -> Twin:
        """Keep the first N marked/unmarked draws (draw 1 plus N-1 extras)."""
        if max_draws < 1:
            raise ValueError("max_draws must be >= 1")
        keep = max_draws - 1
        return Twin(
            stem=self.stem,
            marked_text=self.marked_text,
            unmarked_text=self.unmarked_text,
            marked_ids=list(self.marked_ids),
            unmarked_ids=list(self.unmarked_ids),
            extra_marked_ids=[list(x) for x in self.extra_marked_ids[:keep]],
            extra_unmarked_ids=[list(x) for x in self.extra_unmarked_ids[:keep]],
            extra_marked_text=list(self.extra_marked_text[:keep]),
            extra_unmarked_text=list(self.extra_unmarked_text[:keep]),
            prompt_text=self.prompt_text,
            prompt_ids=list(self.prompt_ids),
        )

    def clip_prefix(self, n: int) -> Twin:
        """Keep the first n tokens of every draw. n<=0 leaves ids unchanged."""
        if n <= 0:
            return self
        return Twin(
            stem=self.stem,
            marked_text=self.marked_text,
            unmarked_text=self.unmarked_text,
            marked_ids=list(self.marked_ids[:n]),
            unmarked_ids=list(self.unmarked_ids[:n]),
            extra_marked_ids=[list(x[:n]) for x in self.extra_marked_ids],
            extra_unmarked_ids=[list(x[:n]) for x in self.extra_unmarked_ids],
            extra_marked_text=list(self.extra_marked_text),
            extra_unmarked_text=list(self.extra_unmarked_text),
            prompt_text=self.prompt_text,
            prompt_ids=list(self.prompt_ids),
        )


@dataclass
class BlindFold:
    stem: str
    marked_lr: float
    unmarked_lr: float
    marked_wins: bool
    marked_file_lrs: list[float] = field(default_factory=list)
    unmarked_file_lrs: list[float] = field(default_factory=list)


@dataclass
class BlindEval:
    folds: list[BlindFold]
    context_len: int
    alpha: float
    used_keys: bool
    used_hash_iv: bool
    used_g_values: bool
    backoff: bool = False
    margin: float = 0.0

    @property
    def n_pairs(self) -> int:
        return len(self.folds)

    @property
    def n_marked_wins(self) -> int:
        return sum(1 for f in self.folds if f.marked_wins)

    @property
    def n_prompt_ties(self) -> int:
        return sum(
            1
            for f in self.folds
            if pair_outcome(f.marked_lr, f.unmarked_lr, margin=self.margin) == "tie"
        )

    @property
    def n_prompt_losses(self) -> int:
        return sum(
            1
            for f in self.folds
            if pair_outcome(f.marked_lr, f.unmarked_lr, margin=self.margin) == "loss"
        )

    @property
    def n_prompts_marked_ge(self) -> int:
        """Historical ranking used ``marked >= unmarked`` (ties counted as wins)."""
        return self.n_marked_wins + self.n_prompt_ties

    @property
    def accuracy(self) -> float:
        if not self.folds:
            return float("nan")
        return self.n_marked_wins / len(self.folds)

    def _sorted_folds(self) -> list[BlindFold]:
        return sorted(self.folds, key=lambda f: f.stem)

    @property
    def n_marked_positive(self) -> int:
        """Isolated hard sign: marked files with ``lr > 0``.

        Independent of ``margin``. Empty ``marked_file_lrs`` counts as
        no isolated true positives.
        """
        return sum(1 for f in self.folds for m in f.marked_file_lrs if m > 0.0)

    def _stem_rank_isolated(self) -> list[tuple[str, str, int]]:
        rows: list[tuple[str, str, int]] = []
        for fold in self._sorted_folds():
            n_tp = sum(1 for m in fold.marked_file_lrs if m > 0.0)
            outcome = pair_outcome(
                fold.marked_lr, fold.unmarked_lr, margin=self.margin
            )
            rows.append((fold.stem, outcome, n_tp))
        return rows

    @property
    def ranking_without_isolated_tp(self) -> list[str]:
        """Prompt-ranking wins with no marked file ``lr > 0``.

        Isolated sign stays hard ``lr > 0`` even when ``margin`` is nonzero.
        Those stems rank because unmarked LRs are more negative, not because
        any isolated marked file signs. Do not read prompt wins as isolated
        recall.
        """
        return [
            stem
            for stem, outcome, n_tp in self._stem_rank_isolated()
            if outcome == "win" and n_tp == 0
        ]

    @property
    def n_prompt_wins_without_isolated_tp(self) -> int:
        return len(self.ranking_without_isolated_tp)

    @property
    def ranking_ties_without_isolated_tp(self) -> list[str]:
        """Prompt-ranking ties with no marked file ``lr > 0``."""
        return [
            stem
            for stem, outcome, n_tp in self._stem_rank_isolated()
            if outcome == "tie" and n_tp == 0
        ]

    @property
    def ranking_losses_with_isolated_tp(self) -> list[str]:
        """Prompt-ranking losses that still have a marked file ``lr > 0``.

        Isolated TPs on a ranking loss do not make the prompt-group
        comparison. Ferry-queue on 12-LOO hard last-4 is the type case.
        """
        return [
            stem
            for stem, outcome, n_tp in self._stem_rank_isolated()
            if outcome == "loss" and n_tp > 0
        ]

    @property
    def n_marked_positive_on_ranking_losses(self) -> int:
        return sum(
            n_tp
            for _stem, outcome, n_tp in self._stem_rank_isolated()
            if outcome == "loss"
        )

    def ranking_payload(self) -> dict:
        hide = self.ranking_without_isolated_tp
        ties_hide = self.ranking_ties_without_isolated_tp
        loss_tp = self.ranking_losses_with_isolated_tp
        return {
            "n_prompt_wins": self.n_marked_wins,
            "n_prompt_wins_ge": self.n_prompts_marked_ge,
            "n_prompt_ties": self.n_prompt_ties,
            "n_prompt_losses": self.n_prompt_losses,
            "n_prompt_wins_without_isolated_tp": len(hide),
            "ranking_without_isolated_tp": hide,
            "ranking_ties_without_isolated_tp": ties_hide,
            "n_ranking_losses_with_isolated_tp": len(loss_tp),
            "ranking_losses_with_isolated_tp": loss_tp,
            "n_marked_positive_on_ranking_losses": (
                self.n_marked_positive_on_ranking_losses
            ),
            "n_marked_lr_positive": self.n_marked_positive,
        }


def _ctx(ids: Sequence[int], i: int, context_len: int) -> tuple[int, ...]:
    start = max(0, i - context_len)
    return tuple(ids[start:i])


def _scored_ctx(
    ids: Sequence[int],
    i: int,
    context_len: int,
    position_bucket: int = 0,
    prefix: Sequence[int] = (),
) -> tuple[int, ...]:
    """Last-k tokens, optionally namespaced by i // position_bucket.

    Bucket 0 is the published last-k table. A positive bucket keeps early
    4-grams from sharing counts with the same tokens later in the string.
    It is not a watermark key.

    `prefix` is prompt token ids used as context only (not scored). Empty
    last-k (generated token 0 with no prefix) maps to FIRST_TOKEN_CTX so
    `_log_prob` can look it up; the empty tuple is skipped as a backoff
    rest stop and must not become a first-token bucket.
    """
    if prefix:
        available = tuple(int(x) for x in prefix) + tuple(int(x) for x in ids[:i])
        if context_len <= 0:
            ctx = FIRST_TOKEN_CTX
        else:
            ctx = available[-context_len:] if available else FIRST_TOKEN_CTX
            if not ctx:
                ctx = FIRST_TOKEN_CTX
    else:
        ctx = _ctx(ids, i, context_len)
        if not ctx:
            ctx = FIRST_TOKEN_CTX
    if position_bucket <= 0:
        return ctx
    return (i // int(position_bucket),) + ctx


def _add_sequence(
    table: NextTokenTable,
    ids: Sequence[int],
    *,
    position_bucket: int = 0,
    include_first: bool = False,
    prefix: Sequence[int] = (),
) -> None:
    for i, tok in enumerate(ids):
        t = int(tok)
        table.unigram[t] += 1
        table.n_tokens += 1
        available = len(prefix) + i
        if i == 0 and not prefix:
            if include_first:
                ctx = _scored_ctx(ids, i, 0, position_bucket, prefix=())
                table.counts.setdefault(ctx, Counter())[t] += 1
            continue
        # Store every *real* suffix length 1..min(k, available) once.
        # Looping 1..k when fewer tokens exist collapses to the same
        # truncated context and overweights the opening.
        max_len = min(int(table.context_len), available)
        for length in range(1, max_len + 1):
            ctx = _scored_ctx(
                ids, i, length, position_bucket, prefix=prefix
            )
            table.counts.setdefault(ctx, Counter())[t] += 1


def fit_table(
    sequences: Iterable[Sequence[int]],
    *,
    context_len: int,
    position_bucket: int = 0,
    include_first: bool = False,
    prefixes: Iterable[Sequence[int]] | None = None,
) -> NextTokenTable:
    seqs = list(sequences)
    if prefixes is None:
        prefs: list[Sequence[int]] = [() for _ in seqs]
    else:
        prefs = list(prefixes)
        if len(prefs) != len(seqs):
            raise ValueError("prefixes must match sequences")
    table = NextTokenTable(context_len=context_len)
    for seq, prefix in zip(seqs, prefs, strict=True):
        _add_sequence(
            table,
            seq,
            position_bucket=position_bucket,
            include_first=include_first,
            prefix=prefix,
        )
    return table


def fit_blind(
    marked_seqs: Iterable[Sequence[int]],
    unmarked_seqs: Iterable[Sequence[int]],
    *,
    context_len: int = DEFAULT_CONTEXT_LEN,
    alpha: float = DEFAULT_ALPHA,
    backoff: bool = False,
    position_bucket: int = 0,
    include_first: bool = False,
    prompt_context: bool = False,
    marked_prefixes: Iterable[Sequence[int]] | None = None,
    unmarked_prefixes: Iterable[Sequence[int]] | None = None,
) -> BlindModel:
    marked = fit_table(
        marked_seqs,
        context_len=context_len,
        position_bucket=position_bucket,
        include_first=include_first,
        prefixes=marked_prefixes,
    )
    unmarked = fit_table(
        unmarked_seqs,
        context_len=context_len,
        position_bucket=position_bucket,
        include_first=include_first,
        prefixes=unmarked_prefixes,
    )
    vocab = set(marked.unigram) | set(unmarked.unigram)
    return BlindModel(
        marked=marked,
        unmarked=unmarked,
        context_len=context_len,
        alpha=alpha,
        vocab=vocab,
        backoff=backoff,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        position_bucket=int(position_bucket) if position_bucket > 0 else 0,
        include_first=bool(include_first),
        prompt_context=bool(prompt_context),
    )


def _bucket_log_prob(bucket: Counter, tok: int, *, alpha: float, v: int) -> float:
    n = sum(bucket.values())
    c = bucket.get(tok, 0)
    return math.log((c + alpha) / (n + alpha * v))


def score_index_range(
    n: int, score_span: tuple[int, int] | None = None
) -> range:
    """Absolute generated-token indices to score. None scores the whole sequence."""
    if score_span is None:
        return range(n)
    start, end = int(score_span[0]), int(score_span[1])
    start = max(0, start)
    end = min(int(n), end)
    if end <= start:
        return range(0)
    return range(start, end)


def backoff_contexts(
    ctx: tuple[int, ...], *, namespaced: bool
) -> list[tuple[int, ...]]:
    """Shorten token history; keep a leading position namespace if present."""
    keys = [ctx]
    if not ctx:
        return keys
    if namespaced:
        ns, hist = ctx[0], ctx[1:]
        for i in range(1, len(hist) + 1):
            keys.append((ns,) + hist[i:])
        return keys
    keys.extend(ctx[i:] for i in range(1, len(ctx)))
    return keys


def shorten_ctx(
    ctx: tuple[int, ...], *, namespaced: bool
) -> tuple[int, ...] | None:
    """Drop the oldest history token, keeping a leading position namespace."""
    if namespaced:
        if len(ctx) <= 1:
            return None
        return (ctx[0],) + ctx[2:]
    if not ctx:
        return None
    return ctx[1:]


def clip_ctx_order(
    ctx: tuple[int, ...], order: int, *, namespaced: bool
) -> tuple[int, ...]:
    """Keep the last ``order`` history tokens; preserve a leading namespace."""
    if order <= 0:
        return (ctx[0],) if namespaced and ctx else ()
    if namespaced:
        if not ctx:
            return ()
        return (ctx[0],) + ctx[1:][-order:]
    if len(ctx) <= order:
        return ctx
    return ctx[-order:]


def _log_prob(
    table: NextTokenTable,
    ctx: tuple[int, ...],
    tok: int,
    *,
    alpha: float,
    v: int,
    backoff: bool,
    namespaced: bool = False,
) -> float:
    """P(tok | ctx). Optional stupid backoff: drop oldest history tokens first."""
    candidates = backoff_contexts(ctx, namespaced=namespaced) if backoff else [ctx]
    for key in candidates:
        if not key:
            continue
        bucket = table.counts.get(key)
        if bucket:
            return _bucket_log_prob(bucket, tok, alpha=alpha, v=v)
    n = max(table.n_tokens, 1)
    c = table.unigram.get(tok, 0)
    return math.log((c + alpha) / (n + alpha * v))


def likelihood_ratio(
    ids: Sequence[int],
    model: BlindModel,
    *,
    prefix: Sequence[int] = (),
    score_span: tuple[int, int] | None = None,
) -> float:
    """Mean log P_marked − log P_unmarked. Positive ⇒ more like the marked pile.

    ``score_span`` scores only those absolute generated indices, keeping the
    original preceding tokens and position as context. It is not a reindexed
    substring.
    """
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("blind model consulted keys / hash_iv / g-values")
    v = max(len(model.vocab), 2)
    total = 0.0
    n = 0
    score_first = bool(prefix) or model.include_first or model.prompt_context
    namespaced = int(getattr(model, "position_bucket", 0) or 0) > 0
    for i in score_index_range(len(ids), score_span):
        if i == 0 and not score_first:
            continue
        tok = ids[i]
        ctx = _scored_ctx(
            ids, i, model.context_len, model.position_bucket, prefix=prefix
        )
        t = int(tok)
        total += _log_prob(
            model.marked,
            ctx,
            t,
            alpha=model.alpha,
            v=v,
            backoff=model.backoff,
            namespaced=namespaced,
        )
        total -= _log_prob(
            model.unmarked,
            ctx,
            t,
            alpha=model.alpha,
            v=v,
            backoff=model.backoff,
            namespaced=namespaced,
        )
        n += 1
    if n == 0:
        return 0.0
    return total / n


def _prompt_stem_from_marked(name: str) -> tuple[str, int] | None:
    """'01-harbour-marked.txt' → (01-harbour, 1); '01-harbour-marked-2.txt' → (…, 2)."""
    m = re.fullmatch(r"(.+)-marked(?:-(\d+))?\.txt", name)
    if not m:
        return None
    return m.group(1), int(m.group(2) or 1)


def _prompt_stem_from_unmarked(name: str) -> tuple[str, int] | None:
    """'01-harbour-unmarked-gen.txt' → (…, 1); '01-harbour-unmarked-gen-2.txt' → (…, 2)."""
    m = re.fullmatch(r"(.+)-unmarked-gen(?:-(\d+))?\.txt", name)
    if not m:
        return None
    return m.group(1), int(m.group(2) or 1)


def _index_pair_files(pair_dir: Path) -> tuple[dict[str, dict[int, Path]], dict[str, dict[int, Path]]]:
    marked: dict[str, dict[int, Path]] = {}
    unmarked: dict[str, dict[int, Path]] = {}
    for path in pair_dir.glob("*-marked*.txt"):
        parsed = _prompt_stem_from_marked(path.name)
        if parsed is None:
            continue
        stem, idx = parsed
        marked.setdefault(stem, {})[idx] = path
    for path in pair_dir.glob("*-unmarked-gen*.txt"):
        parsed = _prompt_stem_from_unmarked(path.name)
        if parsed is None:
            continue
        stem, idx = parsed
        unmarked.setdefault(stem, {})[idx] = path
    return marked, unmarked


def load_twins(pair_dir: Path, *, tokenizer=None) -> list[Twin]:
    """Load marked/unmarked twins indexed by exact sample id.

    Missing a matching unmarked (or marked) draw is an error, not a silent
    shift of later extras. Draw 1 is ``{stem}-marked.txt`` /
    ``{stem}-unmarked-gen.txt``.
    """
    pair_dir = Path(pair_dir)
    tok = tokenizer or load_tokenizer()
    marked_files, unmarked_files = _index_pair_files(pair_dir)
    stems = sorted(set(marked_files) | set(unmarked_files))
    if not stems:
        raise FileNotFoundError(
            f"no *-marked.txt / *-unmarked-gen.txt twins in {pair_dir}"
        )
    twins: list[Twin] = []
    for stem in stems:
        m_ids = marked_files.get(stem, {})
        u_ids = unmarked_files.get(stem, {})
        if set(m_ids) != set(u_ids):
            missing_u = sorted(set(m_ids) - set(u_ids))
            missing_m = sorted(set(u_ids) - set(m_ids))
            raise ValueError(
                f"asymmetric pair files for stem {stem!r}: "
                f"marked samples {sorted(m_ids)}, unmarked samples {sorted(u_ids)}"
                + (f"; missing unmarked {missing_u}" if missing_u else "")
                + (f"; missing marked {missing_m}" if missing_m else "")
            )
        if 1 not in m_ids:
            raise ValueError(
                f"stem {stem!r} has extra draws {sorted(m_ids)} but no draw 1"
            )
        extras = sorted(k for k in m_ids if k != 1)
        marked_text = m_ids[1].read_text()
        unmarked_text = u_ids[1].read_text()
        extra_m: list[list[int]] = []
        extra_u: list[list[int]] = []
        extra_m_text: list[str] = []
        extra_u_text: list[str] = []
        for idx in extras:
            mtxt = m_ids[idx].read_text()
            utxt = u_ids[idx].read_text()
            extra_m_text.append(mtxt)
            extra_u_text.append(utxt)
            extra_m.append(tok(mtxt)["input_ids"])
            extra_u.append(tok(utxt)["input_ids"])
        prompt_path = pair_dir / f"{stem}-prompt.txt"
        prompt_text = prompt_path.read_text() if prompt_path.is_file() else ""
        prompt_ids = tok(prompt_text)["input_ids"] if prompt_text else []
        twins.append(
            Twin(
                stem=stem,
                marked_text=marked_text,
                unmarked_text=unmarked_text,
                marked_ids=tok(marked_text)["input_ids"],
                unmarked_ids=tok(unmarked_text)["input_ids"],
                extra_marked_ids=extra_m,
                extra_unmarked_ids=extra_u,
                extra_marked_text=extra_m_text,
                extra_unmarked_text=extra_u_text,
                prompt_text=prompt_text,
                prompt_ids=prompt_ids,
            )
        )
    return twins


def clip_twins(twins: Sequence[Twin], max_draws: int) -> list[Twin]:
    """Keep the first N draws per stem. Draw 1 is the primary marked/unmarked pair."""
    return [twin.clip_draws(max_draws) for twin in twins]


def clip_twins_prefix(twins: Sequence[Twin], n: int) -> list[Twin]:
    """Keep the first n tokens of every draw. Matched fit/score prefix."""
    return [twin.clip_prefix(n) for twin in twins]


def pair_outcome(
    marked_lr: float, unmarked_lr: float, *, margin: float = 0.0
) -> str:
    """Win / loss / tie for a paired comparison.

    Frozen endpoint: marked mean *exceeds* unmarked mean (strict ``>`` after
    adding ``margin``). Equality is a tie, not a win.
    """
    left = marked_lr + margin
    if left > unmarked_lr:
        return "win"
    if left < unmarked_lr:
        return "loss"
    return "tie"


def pair_marked_wins(marked_lr: float, unmarked_lr: float, *, margin: float = 0.0) -> bool:
    """True iff the marked twin strictly exceeds the unmarked twin.

    ``margin=0`` is the frozen strict comparison. ``margin>0`` is a named
    robustness endpoint: win iff ``marked_lr + margin > unmarked_lr``.
    """
    return pair_outcome(marked_lr, unmarked_lr, margin=margin) == "win"


def leave_one_prompt_out(
    twins: Sequence[Twin],
    *,
    context_len: int = DEFAULT_CONTEXT_LEN,
    alpha: float = DEFAULT_ALPHA,
    backoff: bool = False,
    margin: float = 0.0,
) -> BlindEval:
    if len(twins) < 2:
        raise ValueError("need at least two prompt twins for leave-one-out")
    folds: list[BlindFold] = []
    used_keys = used_hash = used_g = False
    for i, held in enumerate(twins):
        train = [t for j, t in enumerate(twins) if j != i]
        model = fit_blind(
            [ids for t in train for ids in t.marked_seqs()],
            [ids for t in train for ids in t.unmarked_seqs()],
            context_len=context_len,
            alpha=alpha,
            backoff=backoff,
        )
        used_keys = used_keys or model.used_keys
        used_hash = used_hash or model.used_hash_iv
        used_g = used_g or model.used_g_values
        marked_file_lrs = [likelihood_ratio(s, model) for s in held.marked_seqs()]
        unmarked_file_lrs = [
            likelihood_ratio(s, model) for s in held.unmarked_seqs()
        ]
        marked_lr = sum(marked_file_lrs) / len(marked_file_lrs)
        unmarked_lr = sum(unmarked_file_lrs) / len(unmarked_file_lrs)
        folds.append(
            BlindFold(
                stem=held.stem,
                marked_lr=marked_lr,
                unmarked_lr=unmarked_lr,
                marked_wins=pair_marked_wins(
                    marked_lr, unmarked_lr, margin=margin
                ),
                marked_file_lrs=marked_file_lrs,
                unmarked_file_lrs=unmarked_file_lrs,
            )
        )
    return BlindEval(
        folds=folds,
        context_len=context_len,
        alpha=alpha,
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
        backoff=backoff,
        margin=margin,
    )


def print_blind_eval(ev: BlindEval) -> str:
    lines = [
        (
            f"blind leave-one-prompt-out n_pairs={ev.n_pairs} "
            f"marked_wins={ev.n_marked_wins} ties={ev.n_prompt_ties} "
            f"accuracy={ev.accuracy:.3f} "
            f"ranking_without_isolated_tp="
            f"{ev.n_prompt_wins_without_isolated_tp}/{ev.n_marked_wins} "
            f"ranking_losses_with_isolated_tp="
            f"{len(ev.ranking_losses_with_isolated_tp)} "
            f"marked_lr_positive={ev.n_marked_positive} "
            f"context_len={ev.context_len} backoff={ev.backoff} "
            f"margin={ev.margin:g} "
            f"used_keys={ev.used_keys} hash_iv={ev.used_hash_iv} "
            f"g_values={ev.used_g_values}"
        )
    ]
    hide = ev.ranking_without_isolated_tp
    loss = ev.ranking_losses_with_isolated_tp
    if hide:
        lines.append(
            "ranking wins with no isolated TP: " + ", ".join(hide)
        )
    if loss:
        lines.append(
            "ranking losses with isolated TP: " + ", ".join(loss)
        )
    for fold in ev.folds:
        outcome = pair_outcome(
            fold.marked_lr, fold.unmarked_lr, margin=ev.margin
        )
        flag = {
            "win": "marked_higher",
            "loss": "unmarked_higher",
            "tie": "tie",
        }[outcome]
        n_tp = sum(1 for m in fold.marked_file_lrs if m > 0.0)
        n_files = len(fold.marked_file_lrs)
        files = f" marked_files_gt0={n_tp}/{n_files}" if n_files else ""
        lines.append(
            f"{fold.stem}: marked_lr={fold.marked_lr:.4f} "
            f"unmarked_lr={fold.unmarked_lr:.4f} {flag}{files}"
        )
    return "\n".join(lines)


def persist_blind_eval(ev: BlindEval, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    table = {
        "n_pairs": ev.n_pairs,
        "n_marked_wins": ev.n_marked_wins,
        "n_prompt_ties": ev.n_prompt_ties,
        "n_prompt_losses": ev.n_prompt_losses,
        "accuracy": ev.accuracy,
        **ev.ranking_payload(),
        "context_len": ev.context_len,
        "backoff": ev.backoff,
        "margin": ev.margin,
        "alpha": ev.alpha,
        "used_keys": ev.used_keys,
        "used_hash_iv": ev.used_hash_iv,
        "used_g_values": ev.used_g_values,
        "note": (
            "Likelihood ratio from token counts only. Positive marked_lr "
            "means the held-out text looks more like the marked train pile. "
            "n_marked_wins is prompt-mean ranking, not per-file accuracy. "
            "ranking_without_isolated_tp lists ranking wins with no marked "
            "file lr>0. Isolated sign is hard lr>0 even when margin is "
            "nonzero. No keys / hash_iv / g-values."
        ),
        "folds": [
            {
                "stem": f.stem,
                "marked_lr": f.marked_lr,
                "unmarked_lr": f.unmarked_lr,
                "marked_wins": f.marked_wins,
                "marked_file_lrs": list(f.marked_file_lrs),
                "unmarked_file_lrs": list(f.unmarked_file_lrs),
                "n_marked_positive": sum(1 for m in f.marked_file_lrs if m > 0.0),
            }
            for f in ev.folds
        ],
    }
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    hide = ev.ranking_without_isolated_tp
    loss = ev.ranking_losses_with_isolated_tp
    md = [
        "# Key-free blind eval (leave-one-prompt-out)",
        "",
        f"Accuracy: **{ev.n_marked_wins}/{ev.n_pairs}** ({ev.accuracy:.3f}). "
        f"context_len={ev.context_len} backoff={ev.backoff} "
        f"margin={ev.margin:g}.",
        "",
        f"Ranking wins with no isolated TP: **{len(hide)}/{ev.n_marked_wins}**"
        + (f" ({', '.join(hide)})" if hide else "")
        + ". "
        f"Ranking losses with isolated TP: **{len(loss)}**"
        + (f" ({', '.join(loss)})" if loss else "")
        + f". Isolated marked `lr>0`: **{ev.n_marked_positive}**. "
        "Prompt ranking is not per-file accuracy.",
        "",
        "No key. No `detector_mean`. Ground truth is how the file was *created* "
        "(mixin vs not), not the official score.",
        "",
        "| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |",
        "|---|---|---|---|---|",
    ]
    for f in ev.folds:
        n_tp = sum(1 for m in f.marked_file_lrs if m > 0.0)
        n_files = len(f.marked_file_lrs)
        files = f"{n_tp}/{n_files}" if n_files else "—"
        md.append(
            f"| {f.stem} | {f.marked_lr:.4f} | {f.unmarked_lr:.4f} | "
            f"{f.marked_wins} | {files} |"
        )
    md.append("")
    (out_dir / "results.md").write_text("\n".join(md) + "\n")
