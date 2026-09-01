"""Rank-path tables: key-free next-symbol LR on unmarked-LM tournament ranks.

Token count tables cannot score a novel opening: ``lr == 0`` iff
``n_used == 0``. That is an overlap bound on *token identity*. Tournament
sampling does not need the same tokens. It biases which rank within the
unmarked top-k is chosen.

This module discretizes that rank into a five-symbol alphabet and fits the
same observed-token tables on the symbol sequence. Isolated ``indicate score``
still needs the public unmarked LM (same as pivot) and still cannot
reconstruct a prompt. It never computes g-values, never reads watermark
keys, and never calls detector_mean.

Symbols (``top_k`` default 40):

* 0 — chosen token missed the unmarked top-k
* 1 — unmarked argmax (rank 1)
* 2 — ranks 2–3 (tight near-tie; where a tournament can flip the draw)
* 3 — ranks 4–10
* 4 — ranks 11–k

The first generated token has no unmarked-LM context without a prompt, so
the isolated-file path scores generated tokens 1… (choice-matrix rows).
The first *symbol* is therefore a real tournament decision and is scored
(``include_first=True`` on the symbol sequence). ``--rankpath-full`` keeps
those rows from the unclipped file when count tables use ``--fit-prefix``.
Matched ``--prefix-lens`` / ``--windows`` slice the same rows (not token
identity). Unbucketed full-file tables want ``--rankpath-pos-bucket 0``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

import numpy as np

from text_watermark_tools.blind import BlindModel, fit_blind
from text_watermark_tools.indicator import _dump_table, _load_table
from text_watermark_tools.pivot import (
    IN_TOPK_INDEX,
    RANK_TOPK_INDEX,
    extract_choice_matrix,
)
from text_watermark_tools.score import TOP_K
from text_watermark_tools.transfer import ScoreSpec, score_sequence_detail

RANK_PATH_KIND = "key-free-rankpath"
RANK_PATH_ALPHABET = 5
RANK_PATH_TABLES = "tables.json"
RANK_PATH_CAVEAT = (
    "Not detector_mean. Not Claude. Not Anthropic. "
    "Unmarked-LM rank symbols, not watermark keys and not token identity. "
    "prompt_context=true cannot score a lone file without the prompt. "
    "Not a universal detector."
)

# tokbackoff on rank symbols. include_first: symbol 0 is generated token 1.
RANKPATH_SPEC = ScoreSpec(
    kind="tokbackoff",
    min_count=1,
    require_token=True,
    include_first=True,
    instance="key-free-rankpath",
)
RANKUNI_SPEC = ScoreSpec(
    kind="unigram",
    include_first=True,
    instance="key-free-rankuni",
)
RANKHITS_SPEC = ScoreSpec(
    kind="gated",
    min_count=1,
    require_token=True,
    include_first=True,
    instance="key-free-rankhits",
)
RANKPATH_SPECS: dict[str, ScoreSpec] = {
    "rankpath": RANKPATH_SPEC,
    "rankuni": RANKUNI_SPEC,
    "rankhits": RANKHITS_SPEC,
}
CASCADE_FALLBACKS = ("pivot", "rankpath", "rankuni")


def rank_path_symbol(
    rank_topk: float,
    in_topk: float,
    *,
    top_k: int = TOP_K,
) -> int:
    """Map one unmarked-LM choice row to the five-symbol alphabet."""
    k = max(int(top_k), 1)
    if float(in_topk) < 0.5:
        return 0
    rank = int(round(float(rank_topk)))
    if rank <= 1:
        return 1
    if rank <= 3:
        return 2
    if rank <= 10:
        return 3
    if rank <= k:
        return 4
    return 0


def symbols_from_matrix(mat: np.ndarray, *, top_k: int = TOP_K) -> list[int]:
    """One symbol per choice-matrix row. Empty matrix → empty path."""
    if mat.size == 0:
        return []
    rows = np.asarray(mat, dtype=np.float64)
    if rows.ndim != 2 or rows.shape[1] < 4:
        raise ValueError("choice matrix must be [T, 6] unmarked-LM features")
    out: list[int] = []
    for row in rows:
        out.append(
            rank_path_symbol(
                row[RANK_TOPK_INDEX],
                row[IN_TOPK_INDEX],
                top_k=top_k,
            )
        )
    return out


def symbols_from_matrices(
    mats: dict[tuple[str, int, str], np.ndarray],
    *,
    top_k: int = TOP_K,
) -> dict[tuple[str, int, str], list[int]]:
    return {key: symbols_from_matrix(mat, top_k=top_k) for key, mat in mats.items()}


def opening_matrix_end(fit_prefix: int | None, prompt_context: bool) -> int | None:
    """Choice-matrix rows that match a clipped generated file.

    Isolated generated-only skips token 0, so ``--fit-prefix 4`` is three
    rank symbols. Prompt context scores every generated token.
    """
    if not fit_prefix or int(fit_prefix) <= 0:
        return None
    n = int(fit_prefix)
    if prompt_context:
        return n
    return max(n - 1, 0)


def generated_tokens_for_rank_symbols(n_symbols: int, prompt_context: bool) -> int:
    """How many generated tokens yield ``n_symbols`` choice-matrix rows."""
    n = max(int(n_symbols), 0)
    if prompt_context:
        return n
    return n + 1


def slice_matrices(
    mats: dict[tuple[str, int, str], np.ndarray],
    start: int = 0,
    end: int | None = None,
) -> dict[tuple[str, int, str], np.ndarray]:
    """Half-open row slice. Rows are unmarked-LM decisions, not token ids."""
    s = max(int(start), 0)
    out: dict[tuple[str, int, str], np.ndarray] = {}
    for key, mat in mats.items():
        rows = np.asarray(mat, dtype=np.float64)
        if rows.ndim != 2:
            rows = np.zeros((0, 6), dtype=np.float64)
        e = int(rows.shape[0] if end is None else end)
        out[key] = rows[s:e]
    return out


def slice_symbols(
    symbols: dict[tuple[str, int, str], list[int]],
    start: int = 0,
    end: int | None = None,
) -> dict[tuple[str, int, str], list[int]]:
    s = max(int(start), 0)
    out: dict[tuple[str, int, str], list[int]] = {}
    for key, ids in symbols.items():
        seq = list(ids)
        e = len(seq) if end is None else int(end)
        out[key] = seq[s:e]
    return out


def cascade_fallback_matrices(
    opening: dict[tuple[str, int, str], np.ndarray],
    full: dict[tuple[str, int, str], np.ndarray] | None = None,
    *,
    end: int | None = None,
) -> dict[tuple[str, int, str], np.ndarray]:
    """Rank-path cascade fallback is the opening path, never the full file.

    ``end`` slices a longer collected view to the first N rank symbols
    (unbucketed prefix-N). ``None`` keeps the ``--fit-prefix`` opening.
    ``rankpath-full`` must not change this default: averaging 128 rank
    symbols dilutes the opening the way the published pivot did.
    """
    if end is None or int(end) <= 0:
        return opening
    source = full if full is not None else opening
    return slice_matrices(source, 0, int(end))


def parse_cascade_fallback(raw: str | None) -> str:
    name = str(raw or "pivot").strip().lower()
    if name not in CASCADE_FALLBACKS:
        raise ValueError(
            f"unknown cascade fallback {name!r}; choose {', '.join(CASCADE_FALLBACKS)}"
        )
    return name


def rankpath_spec(name: str) -> ScoreSpec:
    spec = RANKPATH_SPECS.get(str(name).strip().lower())
    if spec is None:
        raise ValueError(
            f"unknown rankpath method {name!r}; choose {', '.join(RANKPATH_SPECS)}"
        )
    return spec


def fit_rankpath_from_symbols(
    symbols: dict[tuple[str, int, str], list[int]],
    train_stems: Sequence[str],
    *,
    context_len: int = 3,
    position_bucket: int = 1,
    alpha: float = 0.5,
) -> BlindModel:
    """Fit next-symbol tables. Vocab is the five rank symbols, not GPT-2 ids."""
    hold = set(train_stems)
    marked: list[list[int]] = []
    unmarked: list[list[int]] = []
    for (stem, _sample, side), ids in symbols.items():
        if stem not in hold:
            continue
        if not ids:
            continue
        if side == "marked":
            marked.append(list(ids))
        elif side == "unmarked":
            unmarked.append(list(ids))
    if not marked or not unmarked:
        empty = fit_blind(
            [[1], [2]],
            [[1], [2]],
            context_len=context_len,
            alpha=alpha,
            position_bucket=position_bucket,
            include_first=True,
        )
        empty.vocab = set(range(RANK_PATH_ALPHABET))
        return empty
    model = fit_blind(
        marked,
        unmarked,
        context_len=max(int(context_len), 1),
        alpha=alpha,
        position_bucket=int(position_bucket) if position_bucket and position_bucket > 0 else 0,
        include_first=True,
    )
    model.vocab = set(range(RANK_PATH_ALPHABET)) | set(model.vocab)
    return model


def score_rankpath_detail(
    ids: Sequence[int],
    model: BlindModel,
    *,
    spec: ScoreSpec | None = None,
):
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("rankpath consulted keys / hash_iv / g-values")
    return score_sequence_detail(ids, model, spec or RANKPATH_SPEC)


def score_rankpath(
    ids: Sequence[int],
    model: BlindModel,
    *,
    spec: ScoreSpec | None = None,
) -> float:
    return float(score_rankpath_detail(ids, model, spec=spec).lr)


def persist_rankpath(
    model: BlindModel,
    out_dir: Path,
    *,
    model_name: str = "gpt2",
    pair_dir: str = "",
    n_train_prompts: int = 0,
    top_k: int = TOP_K,
    prompt_context: bool = False,
    spec_name: str = "rankpath",
    decision_threshold: float | None = None,
    decision_source: str = "",
) -> Path:
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("refusing to persist a rankpath table that used keys")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    spec = rankpath_spec(spec_name) if spec_name in RANKPATH_SPECS else RANKPATH_SPEC
    payload = {
        "kind": RANK_PATH_KIND,
        "instance": spec.instance,
        "model_name": model_name,
        "pair_dir": pair_dir,
        "n_train_prompts": n_train_prompts,
        "context_len": model.context_len,
        "alpha": model.alpha,
        "backoff": model.backoff,
        "position_bucket": int(getattr(model, "position_bucket", 0) or 0),
        "include_first": True,
        "prompt_context": bool(prompt_context),
        "top_k": int(top_k),
        "alphabet": RANK_PATH_ALPHABET,
        "spec_name": spec_name if spec_name in RANKPATH_SPECS else "rankpath",
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "vocab": sorted(int(t) for t in model.vocab),
        "marked": _dump_table(model.marked),
        "unmarked": _dump_table(model.unmarked),
        "caveat": RANK_PATH_CAVEAT,
    }
    if decision_threshold is not None:
        payload["decision_threshold"] = float(decision_threshold)
        payload["decision_source"] = str(decision_source or "unspecified")
    path = out_dir / RANK_PATH_TABLES
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def rankpath_from_payload(raw: dict) -> BlindModel:
    if str(raw.get("kind") or "") != RANK_PATH_KIND:
        raise ValueError("not a key-free rankpath table")
    if raw.get("used_keys") or raw.get("used_hash_iv") or raw.get("used_g_values"):
        raise RuntimeError("rankpath file claims it used keys / hash_iv / g")
    return BlindModel(
        marked=_load_table(raw["marked"]),
        unmarked=_load_table(raw["unmarked"]),
        context_len=int(raw["context_len"]),
        alpha=float(raw["alpha"]),
        vocab=set(int(t) for t in raw["vocab"]),
        backoff=bool(raw.get("backoff", False)),
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        position_bucket=int(raw.get("position_bucket") or 0),
        include_first=True,
        prompt_context=bool(raw.get("prompt_context", False)),
    )


def load_rankpath(tables_dir: Path) -> tuple[BlindModel, dict]:
    path = Path(tables_dir)
    if path.is_dir():
        path = path / RANK_PATH_TABLES
    raw = json.loads(path.read_text())
    return rankpath_from_payload(raw), raw


def symbols_from_token_ids(
    token_ids: Sequence[int],
    model,
    *,
    top_k: int = TOP_K,
    prefix: Sequence[int] = (),
) -> list[int]:
    """Choice matrix → rank path. Needs the unmarked LM, not watermark keys."""
    mat = extract_choice_matrix(
        token_ids, model, top_k=top_k, prefix=prefix
    )
    return symbols_from_matrix(mat, top_k=top_k)
