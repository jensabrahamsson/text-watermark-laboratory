"""Single-text key-free indicator: frozen count tables, no twin at inference.

Fit on marked vs unmarked token counts. Persist. Load. Score one file.
Not detector_mean. Not Claude. Not Anthropic.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from text_watermark_tools.blind import (
    DEFAULT_ALPHA,
    DEFAULT_CONTEXT_LEN,
    BlindModel,
    NextTokenTable,
    Twin,
    fit_blind,
    likelihood_ratio,
    load_twins,
    pair_marked_wins,
)
from text_watermark_tools.score import load_tokenizer
from text_watermark_tools.stats import binary_eval, binary_eval_to_dict, format_binary_eval
from text_watermark_tools.transfer import (
    COUNT_SPECS,
    HASHPOOL_KIND,
    SURFACE_KIND,
    peek_tables_kind,
    score_hashtok_detail,
    score_hashpool_detail,
    score_sequence_detail,
    score_surface,
)

INDICATOR_INSTANCE = "key-free-counts"
TABLES_NAME = "tables.json"
CAVEAT = (
    "Not detector_mean. Not Claude. Not Anthropic. "
    "≈0 is not “human” and not “Claude has no mark”."
)


@dataclass
class IndicatorMeta:
    model_name: str
    pair_dir: str
    n_train_prompts: int
    kind: str = "key-free-indicator"
    instance: str = INDICATOR_INSTANCE
    score_kind: str = "hard"
    decision_threshold: float | None = None
    decision_source: str = ""
    n_used: int | None = None
    n_positions: int | None = None


def _twin_file(stem: str, kind: str, sample: int) -> str:
    if sample <= 1:
        return f"{stem}-marked.txt" if kind == "marked" else f"{stem}-unmarked-gen.txt"
    if kind == "marked":
        return f"{stem}-marked-{sample}.txt"
    return f"{stem}-unmarked-gen-{sample}.txt"


@dataclass
class IndicatorHoldout:
    stems: list[str]
    marked_lrs: list[float]
    unmarked_lrs: list[float]
    used_keys: bool
    used_hash_iv: bool
    used_g_values: bool
    context_len: int
    model_name: str
    samples: list[int] | None = None
    mode: str = "hold"
    margin: float = 0.0
    instance: str = INDICATOR_INSTANCE
    score_kind: str = "hard"

    def _samples(self) -> list[int]:
        if self.samples is None:
            return [1] * len(self.stems)
        return self.samples

    @property
    def n_prompts(self) -> int:
        return len(set(self.stems))

    @property
    def n_files(self) -> int:
        return 2 * len(self.stems)

    @property
    def n_marked_above_unmarked(self) -> int:
        return sum(
            pair_marked_wins(m, u, margin=self.margin)
            for m, u in zip(self.marked_lrs, self.unmarked_lrs, strict=True)
        )

    @property
    def n_marked_positive(self) -> int:
        # Soft bar: lr > -margin. margin=0 is the old lr>0 count.
        return sum(m > -self.margin for m in self.marked_lrs)

    @property
    def n_unmarked_nonpositive(self) -> int:
        return sum(u <= self.margin for u in self.unmarked_lrs)

    @property
    def n_prompts_marked_above(self) -> int:
        """Mean LR per prompt, then marked (+margin) ≥ unmarked. Same grain as blind."""
        buckets: dict[str, list[tuple[float, float]]] = {}
        for stem, m, u in zip(self.stems, self.marked_lrs, self.unmarked_lrs, strict=True):
            buckets.setdefault(stem, []).append((m, u))
        n = 0
        for pairs in buckets.values():
            marked_mean = sum(m for m, _ in pairs) / len(pairs)
            unmarked_mean = sum(u for _, u in pairs) / len(pairs)
            if pair_marked_wins(marked_mean, unmarked_mean, margin=self.margin):
                n += 1
        return n


def _dump_table(table: NextTokenTable) -> dict:
    counts = []
    for ctx in sorted(table.counts, key=lambda c: (len(c), c)):
        nxt = table.counts[ctx]
        counts.append(
            {
                "ctx": [int(x) for x in ctx],
                "next": {str(int(k)): int(v) for k, v in sorted(nxt.items())},
            }
        )
    return {
        "context_len": table.context_len,
        "n_tokens": table.n_tokens,
        "unigram": {str(int(k)): int(v) for k, v in sorted(table.unigram.items())},
        "counts": counts,
    }


def _load_table(raw: dict) -> NextTokenTable:
    table = NextTokenTable(context_len=int(raw["context_len"]))
    table.n_tokens = int(raw["n_tokens"])
    table.unigram = Counter({int(k): int(v) for k, v in raw["unigram"].items()})
    for row in raw["counts"]:
        ctx = tuple(int(x) for x in row["ctx"])
        table.counts[ctx] = Counter(
            {int(k): int(v) for k, v in row["next"].items()}
        )
    return table


def fit_indicator(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    alpha: float = DEFAULT_ALPHA,
    backoff: bool = False,
    position_bucket: int = 0,
    include_first: bool = False,
    prompt_context: bool = False,
) -> BlindModel:
    if not twins:
        raise ValueError("need at least one twin prompt to fit the indicator")
    from text_watermark_tools.transfer import fit_count_model

    if prompt_context or include_first:
        model = fit_count_model(
            twins,
            context_len=context_len,
            alpha=alpha,
            position_bucket=position_bucket,
            include_first=include_first,
            prompt_context=prompt_context,
        )
        model.backoff = backoff
        return model
    return fit_blind(
        [ids for t in twins for ids in t.marked_seqs()],
        [ids for t in twins for ids in t.unmarked_seqs()],
        context_len=context_len,
        alpha=alpha,
        backoff=backoff,
        position_bucket=position_bucket,
        include_first=include_first,
        prompt_context=prompt_context,
    )


def persist_indicator(
    model: BlindModel,
    out_dir: Path,
    *,
    model_name: str = "gpt2",
    pair_dir: str = "",
    n_train_prompts: int = 0,
    decision_threshold: float | None = None,
    decision_source: str = "",
) -> Path:
    if model.used_keys or model.used_hash_iv or model.used_g_values:
        raise RuntimeError("refusing to persist an indicator that used keys")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    bucket = int(getattr(model, "position_bucket", 0) or 0)
    payload = {
        "kind": "key-free-indicator",
        "instance": "key-free-poshits" if bucket > 0 else INDICATOR_INSTANCE,
        "model_name": model_name,
        "pair_dir": pair_dir,
        "n_train_prompts": n_train_prompts,
        "context_len": model.context_len,
        "alpha": model.alpha,
        "backoff": model.backoff,
        "position_bucket": bucket,
        "include_first": bool(getattr(model, "include_first", False)),
        "prompt_context": bool(getattr(model, "prompt_context", False)),
        "used_keys": False,
        "used_hash_iv": False,
        "used_g_values": False,
        "vocab": sorted(int(t) for t in model.vocab),
        "marked": _dump_table(model.marked),
        "unmarked": _dump_table(model.unmarked),
        "caveat": CAVEAT,
    }
    if decision_threshold is not None:
        payload["decision_threshold"] = float(decision_threshold)
        payload["decision_source"] = str(decision_source or "unspecified")
    path = out_dir / TABLES_NAME
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def load_indicator(tables_dir: Path) -> tuple[BlindModel, IndicatorMeta]:
    path = Path(tables_dir)
    if path.is_dir():
        path = path / TABLES_NAME
    raw = json.loads(path.read_text())
    if raw.get("kind") != "key-free-indicator":
        raise ValueError(f"not a key-free indicator table: {path}")
    if raw.get("used_keys") or raw.get("used_hash_iv") or raw.get("used_g_values"):
        raise RuntimeError("indicator file claims it used keys / hash_iv / g")
    model = BlindModel(
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
        include_first=bool(raw.get("include_first", False)),
        prompt_context=bool(raw.get("prompt_context", False)),
    )
    meta = IndicatorMeta(
        model_name=str(raw.get("model_name") or "gpt2"),
        pair_dir=str(raw.get("pair_dir") or ""),
        n_train_prompts=int(raw.get("n_train_prompts") or 0),
        kind=str(raw.get("kind") or "key-free-indicator"),
        instance=str(raw.get("instance") or INDICATOR_INSTANCE),
        score_kind="hard",
        decision_threshold=(
            float(raw["decision_threshold"])
            if raw.get("decision_threshold") is not None
            else None
        ),
        decision_source=str(raw.get("decision_source") or ""),
    )
    return model, meta


def load_tables_meta(tables_dir: Path) -> IndicatorMeta:
    path = Path(tables_dir)
    if path.is_dir():
        path = path / TABLES_NAME
    raw = json.loads(path.read_text())
    kind = str(raw.get("kind") or "")
    instance = str(raw.get("instance") or INDICATOR_INSTANCE)
    if kind == HASHPOOL_KIND:
        score_kind = "hashpool"
    elif kind == SURFACE_KIND:
        score_kind = "surface"
    elif kind == "key-free-pivot":
        score_kind = "pivot-lda"
    elif kind == "key-free-rankpath":
        score_kind = "rankpath"
    else:
        score_kind = "hard"
    threshold = raw.get("decision_threshold")
    return IndicatorMeta(
        model_name=str(raw.get("model_name") or "gpt2"),
        pair_dir=str(raw.get("pair_dir") or ""),
        n_train_prompts=int(raw.get("n_train_prompts") or 0),
        kind=kind,
        instance=instance,
        score_kind=score_kind,
        decision_threshold=float(threshold) if threshold is not None else None,
        decision_source=str(raw.get("decision_source") or ""),
    )


def score_text(text: str, model: BlindModel, *, tokenizer) -> float:
    """Key-free LR of one string. No twin. Positive ⇒ more like the marked pile."""
    ids = tokenizer(text)["input_ids"]
    return likelihood_ratio(ids, model)


def score_text_from_tables(
    text: str,
    tables_dir: Path,
    *,
    tokenizer=None,
    score_mode: str = "auto",
) -> tuple[float, IndicatorMeta, bool]:
    """Score one string from frozen count, hashpool, or surface tables.

    Returns (lr, meta, used_keys). Hashpool/surface tables ignore count modes.
    Surface tables do not need a tokenizer.
    """
    path = Path(tables_dir)
    kind = peek_tables_kind(path)
    mode = (score_mode or "auto").strip().lower()
    if kind == SURFACE_KIND:
        if mode not in ("auto", "surface", ""):
            raise ValueError(
                f"tables are surface; --score-mode {score_mode} does not apply"
            )
        from text_watermark_tools.transfer import load_hashpool

        model = load_hashpool(path)
        lr = score_surface(text, model)
        meta = load_tables_meta(path)
        meta.score_kind = "surface"
        meta.instance = model.instance
        return lr, meta, bool(model.used_keys)
    if kind == "key-free-pivot":
        from text_watermark_tools.generate import _load_unmarked_model, generate_device
        from text_watermark_tools.pivot import (
            extract_choice_vector,
            load_pivot,
            score_pivot_lda,
        )

        fit, raw = load_pivot(path)
        if bool(raw.get("prompt_context")):
            raise ValueError(
                "these pivot tables were fit with prompt context; indicate "
                "score of a lone file cannot reconstruct the prompt. Score "
                "pair twins with probe --pivot --prompt-context instead."
            )
        if tokenizer is None:
            raise ValueError("pivot tables need a tokenizer")
        name = str(raw.get("model_name") or "gpt2")
        lm = _load_unmarked_model(generate_device(), model_name=name)
        ids = tokenizer(text)["input_ids"]
        vec = extract_choice_vector(
            ids,
            lm,
            top_k=int(raw.get("top_k") or 40),
            weight=str(raw.get("weight") or "uniform"),
        )
        lr = score_pivot_lda(vec, fit)
        meta = load_tables_meta(path)
        meta.score_kind = "pivot-lda"
        meta.instance = str(raw.get("instance") or "key-free-pivot-lda")
        meta.n_used = int(vec.size > 0)
        meta.n_positions = None
        return lr, meta, bool(fit.used_keys)
    if kind == "key-free-rankpath":
        from text_watermark_tools.generate import _load_unmarked_model, generate_device
        from text_watermark_tools.rankpath import (
            RANKPATH_SPECS,
            load_rankpath,
            score_rankpath_detail,
            symbols_from_token_ids,
        )

        model, raw = load_rankpath(path)
        if bool(raw.get("prompt_context")):
            raise ValueError(
                "these rankpath tables were fit with prompt context; indicate "
                "score of a lone file cannot reconstruct the prompt."
            )
        if tokenizer is None:
            raise ValueError("rankpath tables need a tokenizer")
        name = str(raw.get("model_name") or "gpt2")
        lm = _load_unmarked_model(generate_device(), model_name=name)
        ids = tokenizer(text)["input_ids"]
        symbols = symbols_from_token_ids(
            ids, lm, top_k=int(raw.get("top_k") or 40)
        )
        spec_name = str(raw.get("spec_name") or "rankpath")
        spec = RANKPATH_SPECS.get(spec_name, RANKPATH_SPECS["rankpath"])
        if mode in RANKPATH_SPECS:
            spec = RANKPATH_SPECS[mode]
        detail = score_rankpath_detail(symbols, model, spec=spec)
        meta = load_tables_meta(path)
        meta.score_kind = spec_name if mode in ("auto", "", spec_name) else mode
        meta.instance = spec.instance
        meta.n_used = detail.n_used
        meta.n_positions = detail.n_positions
        return detail.lr, meta, bool(model.used_keys)
    if kind == HASHPOOL_KIND:
        if mode not in (
            "auto",
            "hashpool",
            "hashtok",
            "hashtoklen",
            "hashtoklen2",
            "hashskip",
            "hashskip2",
            "",
        ):
            raise ValueError(
                f"tables are hashpool; --score-mode {score_mode} does not apply"
            )
        from text_watermark_tools.transfer import load_hashpool

        if tokenizer is None:
            raise ValueError("hashpool tables need a tokenizer")
        model = load_hashpool(path)
        ids = tokenizer(text)["input_ids"]
        if mode in (
            "hashtok",
            "hashtoklen",
            "hashtoklen2",
            "hashskip",
            "hashskip2",
        ):
            drop_one = bool(getattr(model, "drop_one", False))
            if mode in ("hashskip", "hashskip2") and not drop_one:
                raise ValueError(
                    "these tables were not fit as drop-one skip-grams; "
                    "refusing score-time hashskip on a different mixer"
                )
            if mode in ("hashtoklen", "hashtoklen2") and drop_one:
                raise ValueError(
                    "these tables are drop-one skip-grams; use --score-mode "
                    "hashskip or hashskip2"
                )
            detail = score_hashtok_detail(
                ids,
                model,
                exact_len=True
                if mode in ("hashtoklen", "hashtoklen2", "hashskip", "hashskip2")
                else None,
                min_count=2 if mode in ("hashtoklen2", "hashskip2") else 1,
            )
            meta = load_tables_meta(path)
            meta.score_kind = mode
            meta.instance = f"key-free-{mode}"
        else:
            detail = score_hashpool_detail(ids, model)
            meta = load_tables_meta(path)
            meta.score_kind = "hashpool"
            meta.instance = model.instance
        meta.n_used = detail.n_used
        meta.n_positions = detail.n_positions
        return detail.lr, meta, bool(model.used_keys)
    if kind != "key-free-indicator":
        raise ValueError(f"unknown indicator tables kind {kind!r} in {path}")
    if tokenizer is None:
        raise ValueError("count tables need a tokenizer")
    model, meta = load_indicator(path)
    if bool(getattr(model, "prompt_context", False)):
        raise ValueError(
            "these tables were fit with prompt context; indicate score of a "
            "lone file cannot reconstruct the prompt. Score pair twins with "
            "probe --prompt-context instead."
        )
    ids = tokenizer(text)["input_ids"]
    bucketed = int(getattr(model, "position_bucket", 0) or 0) > 0

    def _return_detail(spec, score_kind: str, instance: str):
        detail = score_sequence_detail(ids, model, spec)
        meta.score_kind = score_kind
        meta.instance = instance
        meta.n_used = detail.n_used
        meta.n_positions = detail.n_positions
        return detail.lr, meta, bool(model.used_keys)

    if mode == "poshits" or (mode in ("auto", "") and bucketed):
        return _return_detail(COUNT_SPECS["hits"], "poshits", "key-free-poshits")
    if mode == "poshitmass":
        return _return_detail(COUNT_SPECS["hitmass"], "poshitmass", "key-free-poshitmass")
    if mode == "postokhits":
        return _return_detail(COUNT_SPECS["tokhits"], "postokhits", "key-free-postokhits")
    if mode == "postokbackoff":
        return _return_detail(
            COUNT_SPECS["tokbackoff"], "postokbackoff", "key-free-postokbackoff"
        )
    if mode == "postokbackoff2":
        return _return_detail(
            COUNT_SPECS["tokbackoff2"], "postokbackoff2", "key-free-postokbackoff2"
        )
    if mode in ("auto", "hard", ""):
        detail = score_sequence_detail(ids, model, COUNT_SPECS["hard"])
        meta.score_kind = "hard"
        meta.instance = INDICATOR_INSTANCE
        meta.n_used = detail.n_used
        meta.n_positions = detail.n_positions
        return detail.lr, meta, bool(model.used_keys)
    if mode not in COUNT_SPECS:
        raise ValueError(
            f"unknown --score-mode {score_mode}; "
            f"choose auto, hard, poshits, postokhits, postokbackoff, "
            f"postokbackoff2, poshitmass, hashpool, hashtok, hashtoklen, "
            f"hashtoklen2, hashskip, hashskip2, or one of "
            f"{sorted(COUNT_SPECS)}"
        )
    spec = COUNT_SPECS[mode]
    return _return_detail(spec, mode, spec.instance)


def format_indicator(
    label: str,
    lr: float,
    *,
    n_tokens: int,
    used_keys: bool,
    instance: str = INDICATOR_INSTANCE,
    score_kind: str = "hard",
    threshold: float | None = None,
    decision_source: str = "",
    n_used: int | None = None,
    n_positions: int | None = None,
) -> str:
    extra = ""
    if n_used is not None:
        extra += f" n_used={int(n_used)}"
        if n_positions is not None:
            extra += f" n_positions={int(n_positions)}"
    if threshold is not None:
        if n_used is not None and int(n_used) == 0:
            decision = "ABSTAIN"
        else:
            decision = "marked" if lr > threshold else "unmarked"
        src = f" source={decision_source}" if decision_source else ""
        extra += (
            f" threshold={threshold:.6f} decision={decision}{src} "
            f"not_a_universal_detector=true"
        )
    elif n_used is not None and int(n_used) == 0:
        extra += " decision=ABSTAIN not_a_universal_detector=true"
    return (
        f"{label}: lr={lr:.6f} n_tokens={n_tokens} "
        f"instance={instance} score_kind={score_kind} used_keys={used_keys} "
        f"not_detector_mean=true{extra} {CAVEAT}"
    )


def holdout_single_text(
    twins: Sequence[Twin],
    hold_stems: Sequence[str],
    *,
    context_len: int = 4,
    alpha: float = DEFAULT_ALPHA,
    backoff: bool = False,
    model_name: str = "gpt2",
    margin: float = 0.0,
) -> IndicatorHoldout:
    hold = set(hold_stems)
    if len(hold) < 2:
        raise ValueError("hold-out needs at least two prompt stems")
    train = [t for t in twins if t.stem not in hold]
    held = [t for t in twins if t.stem in hold]
    if len(held) != len(hold):
        missing = hold - {t.stem for t in held}
        raise FileNotFoundError(f"hold-out stems not in corpus: {sorted(missing)}")
    if not train:
        raise ValueError("hold-out left no training prompts")
    model = fit_indicator(
        train, context_len=context_len, alpha=alpha, backoff=backoff
    )
    tok = load_tokenizer(model_name)
    marked_lrs: list[float] = []
    unmarked_lrs: list[float] = []
    stems: list[str] = []
    for t in held:
        # Score the primary files only, one string at a time.
        marked_lrs.append(score_text(t.marked_text, model, tokenizer=tok))
        unmarked_lrs.append(score_text(t.unmarked_text, model, tokenizer=tok))
        stems.append(t.stem)
    return IndicatorHoldout(
        stems=stems,
        marked_lrs=marked_lrs,
        unmarked_lrs=unmarked_lrs,
        used_keys=model.used_keys,
        used_hash_iv=model.used_hash_iv,
        used_g_values=model.used_g_values,
        context_len=context_len,
        model_name=model_name,
        samples=[1] * len(stems),
        mode="hold",
        margin=margin,
    )


def rotate_holdout(
    twins: Sequence[Twin],
    *,
    context_len: int = 4,
    alpha: float = DEFAULT_ALPHA,
    backoff: bool = False,
    model_name: str = "gpt2",
    margin: float = 0.0,
    score_fn=None,
    instance: str = INDICATOR_INSTANCE,
    score_kind: str = "hard",
) -> IndicatorHoldout:
    """Leave one prompt out: fit the rest, score each held file alone.

    Extra samples of the held prompt are scored as their own files. They
    never enter the fit. That is the single-text product question.
    """
    if len(twins) < 3:
        raise ValueError("rotate hold-out needs at least three prompts")
    stems: list[str] = []
    samples: list[int] = []
    marked_lrs: list[float] = []
    unmarked_lrs: list[float] = []
    used_keys = used_hash = used_g = False
    for held in twins:
        train = [t for t in twins if t.stem != held.stem]
        model = fit_indicator(
            train, context_len=context_len, alpha=alpha, backoff=backoff
        )
        used_keys = used_keys or model.used_keys
        used_hash = used_hash or model.used_hash_iv
        used_g = used_g or model.used_g_values
        marked_seqs = held.marked_seqs()
        unmarked_seqs = held.unmarked_seqs()
        n = min(len(marked_seqs), len(unmarked_seqs))
        scorer = score_fn or likelihood_ratio
        for i in range(n):
            marked_lrs.append(scorer(marked_seqs[i], model))
            unmarked_lrs.append(scorer(unmarked_seqs[i], model))
            stems.append(held.stem)
            samples.append(i + 1)
    return IndicatorHoldout(
        stems=stems,
        marked_lrs=marked_lrs,
        unmarked_lrs=unmarked_lrs,
        used_keys=used_keys,
        used_hash_iv=used_hash,
        used_g_values=used_g,
        context_len=context_len,
        model_name=model_name,
        samples=samples,
        mode="rotate",
        margin=margin,
        instance=instance,
        score_kind=score_kind,
    )


def print_holdout(ev: IndicatorHoldout) -> str:
    stats = binary_eval(ev.marked_lrs, ev.unmarked_lrs)
    instance = ev.instance or INDICATOR_INSTANCE
    lines = [
        (
            f"indicate holdout mode={ev.mode} n_prompts={ev.n_prompts} "
            f"n_files={ev.n_files} "
            f"marked_above_unmarked={ev.n_marked_above_unmarked} "
            f"prompts_marked_above={ev.n_prompts_marked_above} "
            f"marked_lr_positive={ev.n_marked_positive} "
            f"unmarked_lr_nonpositive={ev.n_unmarked_nonpositive} "
            f"margin={ev.margin:g} context_len={ev.context_len} "
            f"score_kind={ev.score_kind} "
            f"auc={stats.auc:.3f} perm_p={stats.permutation_p:.4g} "
            f"used_keys={ev.used_keys} hash_iv={ev.used_hash_iv} "
            f"g_values={ev.used_g_values} instance={instance}"
        ),
        format_binary_eval(stats, label="single-file"),
        CAVEAT,
    ]
    for stem, sample, m, u in zip(
        ev.stems, ev._samples(), ev.marked_lrs, ev.unmarked_lrs, strict=True
    ):
        flag = (
            "marked_higher"
            if pair_marked_wins(m, u, margin=ev.margin)
            else "unmarked_higher"
        )
        marked_name = _twin_file(stem, "marked", sample)
        unmarked_name = _twin_file(stem, "unmarked", sample)
        lines.append(f"{marked_name}: lr={m:.6f} instance={instance}")
        lines.append(f"{unmarked_name}: lr={u:.6f} instance={instance}")
        lines.append(f"{stem}#{sample}: {flag}")
    return "\n".join(lines)


def holdout_from_json(path: Path, *, margin: float | None = None) -> IndicatorHoldout:
    """Reload a persist_holdout table. Optional new margin, same LRs."""
    raw = json.loads(Path(path).read_text())
    stems: list[str] = []
    samples: list[int] = []
    marked_lrs: list[float] = []
    unmarked_lrs: list[float] = []
    pending: dict[tuple[str, int], dict[str, float]] = {}
    for row in raw["files"]:
        key = (str(row["stem"]), int(row["sample"]))
        bucket = pending.setdefault(key, {})
        if "unmarked" in row["file"]:
            bucket["u"] = float(row["lr"])
        else:
            bucket["m"] = float(row["lr"])
    for stem, sample in sorted(pending, key=lambda k: (k[0], k[1])):
        bucket = pending[(stem, sample)]
        stems.append(stem)
        samples.append(sample)
        marked_lrs.append(bucket["m"])
        unmarked_lrs.append(bucket["u"])
    applied = float(raw.get("margin", 0.0) if margin is None else margin)
    return IndicatorHoldout(
        stems=stems,
        marked_lrs=marked_lrs,
        unmarked_lrs=unmarked_lrs,
        used_keys=bool(raw.get("used_keys", False)),
        used_hash_iv=bool(raw.get("used_hash_iv", False)),
        used_g_values=bool(raw.get("used_g_values", False)),
        context_len=int(raw.get("context_len", 4)),
        model_name=str(raw.get("model_name") or "gpt2"),
        samples=samples,
        mode=str(raw.get("mode") or "hold"),
        margin=applied,
        instance=str(raw.get("instance") or INDICATOR_INSTANCE),
        score_kind=str(raw.get("score_kind") or "hard"),
    )


def persist_holdout(ev: IndicatorHoldout, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    table = {
        "mode": ev.mode,
        "n_prompts": ev.n_prompts,
        "n_files": ev.n_files,
        "n_marked_above_unmarked": ev.n_marked_above_unmarked,
        "n_prompts_marked_above": ev.n_prompts_marked_above,
        "n_marked_lr_positive": ev.n_marked_positive,
        "n_unmarked_lr_nonpositive": ev.n_unmarked_nonpositive,
        "margin": ev.margin,
        "used_keys": ev.used_keys,
        "used_hash_iv": ev.used_hash_iv,
        "used_g_values": ev.used_g_values,
        "context_len": ev.context_len,
        "model_name": ev.model_name,
        "instance": ev.instance or INDICATOR_INSTANCE,
        "score_kind": ev.score_kind,
        "binary": binary_eval_to_dict(binary_eval(ev.marked_lrs, ev.unmarked_lrs)),
        "caveat": CAVEAT,
        "files": [],
    }
    for stem, sample, m, u in zip(
        ev.stems, ev._samples(), ev.marked_lrs, ev.unmarked_lrs, strict=True
    ):
        table["files"].append(
            {"file": _twin_file(stem, "marked", sample), "lr": m, "stem": stem, "sample": sample}
        )
        table["files"].append(
            {
                "file": _twin_file(stem, "unmarked", sample),
                "lr": u,
                "stem": stem,
                "sample": sample,
            }
        )
    (out_dir / "holdout.json").write_text(json.dumps(table, indent=2) + "\n")
    (out_dir / "holdout.md").write_text(print_holdout(ev) + "\n")
