"""Key-free learned scorers: hashed logistic, token MLP, character CNN.

Count tables and `logit` (ridge on already-computed file scores) are already
learned models. These three architectures ask a narrower question: does a
more flexible function of the *same opening tokens* beat Laplace last-k
tables on the laboratory grains?

They rest on DeepMind SynthID-Text (tournament sampling leaves a next-token
footprint) and on stealing-style detectors that read that footprint without
the secret hash. This lab did not invent that theory. The experiment is
whether a tiny network trained on *this* mixin's matched twins improves
isolated-file GPT-2 indication or transfers across generators.

None of this consults keys, `hash_iv`, or g-values. A win on GPT-2 twins is
not a universal detector and not a Claude classifier.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

import numpy as np

from text_watermark_tools.blind import FIRST_TOKEN_CTX, Twin, _scored_ctx, clip_twins, clip_twins_prefix
from text_watermark_tools.indicator import CAVEAT, IndicatorHoldout
from text_watermark_tools.probe import (
    ProbeRun,
    TransferRun,
    _append_pair,
    _append_threshold,
    _empty_holdout_parts,
    _holdout_from_parts,
    _twin_prefix,
    apply_overlap,
    persist_probe,
    persist_transfer,
    print_probe,
    print_transfer,
    score_twins,
    shuffle_twin_sides,
    summarize_holdout,
)
from text_watermark_tools.stats import binary_eval, fit_ridge_logodds, score_ridge_logodds, threshold_at_fpr
from text_watermark_tools.transfer import _hash_seeds, hash_context

ScoreFn = Callable[..., float]

LEARN_ARCHS: tuple[str, ...] = ("hashlog", "tokmlp", "charcnn")
INSTANCE = {
    "hashlog": "key-free-hashlog",
    "tokmlp": "key-free-tokmlp",
    "charcnn": "key-free-charcnn",
}
PAD_TOKEN_BUCKET = 0
PAD_BYTE = 256
LEARN_NOTE = (
    "Key-free learned scorers, not detector_mean, not Claude, not key recovery. "
    "hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, "
    "not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on "
    "the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a "
    "Qwen or Distil detector."
)


@dataclass(frozen=True)
class LearnSpec:
    context_len: int = 4
    position_bucket: int = 1
    include_first: bool = False
    prompt_context: bool = False
    n_hashes: int = 4
    n_buckets: int = 64
    ridge: float = 1.0
    seed: int = 20260831
    epochs: int = 40
    lr: float = 0.05
    weight_decay: float = 0.05
    embed_buckets: int = 64
    embed_dim: int = 16
    hidden: int = 32
    tokmlp_max_len: int = 16
    charcnn_max_bytes: int = 64
    charcnn_filters: int = 32
    charcnn_kernel: int = 3


def _validate_archs(archs: Sequence[str] | None) -> tuple[str, ...]:
    names = tuple(archs) if archs else LEARN_ARCHS
    unknown = [n for n in names if n not in INSTANCE]
    if unknown:
        raise ValueError(
            f"unknown learn archs {unknown}; use {', '.join(LEARN_ARCHS)}"
        )
    return names


def hashed_ngram_vector(
    ids: Sequence[int],
    spec: LearnSpec,
    *,
    prefix: Sequence[int] = (),
) -> np.ndarray:
    """Signed hashing trick on (last-k, token). Not SynthID's secret hash."""
    dim = spec.n_hashes * spec.n_buckets
    x = np.zeros(dim, dtype=np.float64)
    if not ids:
        return x
    seeds = _hash_seeds(spec.n_hashes, spec.seed)
    for i, tok in enumerate(ids):
        if i == 0 and not spec.include_first and not prefix:
            continue
        ctx = _scored_ctx(
            ids,
            i,
            spec.context_len,
            spec.position_bucket,
            prefix=prefix,
        )
        joint = tuple(ctx) + (int(tok),)
        if joint == FIRST_TOKEN_CTX + (int(tok),) and not spec.include_first:
            continue
        for h, seed in enumerate(seeds):
            hv = hash_context(joint, seed)
            bucket = hv % spec.n_buckets
            sign = 1.0 if (hv >> 1) & 1 else -1.0
            x[h * spec.n_buckets + bucket] += sign
    return x


def ids_to_bytes(ids: Sequence[int], tokenizer=None) -> list[int]:
    """UTF-8 bytes of a decoded token prefix, or id&255 when no tokenizer."""
    if not ids:
        return []
    if tokenizer is None:
        return [int(t) & 255 for t in ids]
    text = tokenizer.decode(
        list(ids),
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )
    return list(text.encode("utf-8"))


def _hash_token(tok: int, n_buckets: int, seed: int) -> int:
    return (hash_context((int(tok),), seed) % n_buckets) + 1


def _tokmlp_indices(
    ids: Sequence[int],
    spec: LearnSpec,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    start = 0 if spec.include_first else 1
    used = [int(t) for t in ids[start : spec.tokmlp_max_len]]
    length = spec.tokmlp_max_len
    tok_idx = np.zeros(length, dtype=np.int64)
    pos_idx = np.arange(length, dtype=np.int64)
    mask = np.zeros(length, dtype=np.float32)
    for j, tok in enumerate(used):
        tok_idx[j] = _hash_token(tok, spec.embed_buckets, spec.seed)
        mask[j] = 1.0
    return tok_idx, pos_idx, mask


def _byte_indices(raw: Sequence[int], spec: LearnSpec) -> tuple[np.ndarray, np.ndarray]:
    used = [min(max(int(b), 0), 255) for b in raw[: spec.charcnn_max_bytes]]
    length = spec.charcnn_max_bytes
    idx = np.full(length, PAD_BYTE, dtype=np.int64)
    mask = np.zeros(length, dtype=np.float32)
    for j, b in enumerate(used):
        idx[j] = b
        mask[j] = 1.0
    return idx, mask


def _draws(twins: Sequence[Twin]):
    for twin in twins:
        marked = twin.marked_seqs()
        unmarked = twin.unmarked_seqs()
        n = min(len(marked), len(unmarked))
        prefix = _twin_prefix(twin, True) if twin.prompt_ids else ()
        for i in range(n):
            yield twin.stem, i + 1, marked[i], unmarked[i], prefix


def _seed_torch(seed: int) -> None:
    import torch

    torch.manual_seed(seed)


def fit_hashlog(
    twins: Sequence[Twin],
    spec: LearnSpec,
) -> ScoreFn:
    pos_rows = []
    neg_rows = []
    for _stem, _sample, marked, unmarked, prefix in _draws(twins):
        use_prefix = prefix if spec.prompt_context else ()
        pos_rows.append(hashed_ngram_vector(marked, spec, prefix=use_prefix))
        neg_rows.append(hashed_ngram_vector(unmarked, spec, prefix=use_prefix))
    if not pos_rows or not neg_rows:
        raise ValueError("hashlog needs marked and unmarked draws")
    weights, intercept, mu, sd = fit_ridge_logodds(
        np.stack(pos_rows),
        np.stack(neg_rows),
        ridge=spec.ridge,
    )

    def score(seq, prefix: Sequence[int] = ()) -> float:
        use_prefix = prefix if spec.prompt_context else ()
        return score_ridge_logodds(
            hashed_ngram_vector(seq, spec, prefix=use_prefix),
            weights,
            intercept,
            mu,
            sd,
        )

    return score


class _TokMLP:
    def __init__(self, spec: LearnSpec):
        import torch
        from torch import nn

        self.spec = spec
        self.torch = torch
        n_tok = spec.embed_buckets + 1
        self.tok = nn.Embedding(n_tok, spec.embed_dim, padding_idx=PAD_TOKEN_BUCKET)
        self.pos = nn.Embedding(spec.tokmlp_max_len, spec.embed_dim)
        self.fc1 = nn.Linear(spec.embed_dim, spec.hidden)
        self.fc2 = nn.Linear(spec.hidden, 1)
        self.params = nn.ModuleList([self.tok, self.pos, self.fc1, self.fc2])

    def logits(self, tok_idx, pos_idx, mask):
        torch = self.torch
        h = self.tok(tok_idx) + self.pos(pos_idx)
        h = h * mask.unsqueeze(-1)
        denom = mask.sum(dim=1, keepdim=True).clamp(min=1.0)
        pooled = h.sum(dim=1) / denom
        return self.fc2(torch.relu(self.fc1(pooled))).squeeze(-1)


class _CharCNN:
    def __init__(self, spec: LearnSpec):
        import torch
        from torch import nn

        self.spec = spec
        self.torch = torch
        self.emb = nn.Embedding(257, spec.embed_dim, padding_idx=PAD_BYTE)
        pad = spec.charcnn_kernel // 2
        self.conv = nn.Conv1d(
            spec.embed_dim,
            spec.charcnn_filters,
            spec.charcnn_kernel,
            padding=pad,
        )
        self.fc = nn.Linear(spec.charcnn_filters, 1)
        self.params = nn.ModuleList([self.emb, self.conv, self.fc])

    def logits(self, byte_idx, mask):
        torch = self.torch
        x = self.emb(byte_idx).transpose(1, 2)
        h = torch.relu(self.conv(x))
        fill = torch.finfo(h.dtype).min
        h = h.masked_fill(~mask.unsqueeze(1).bool(), fill)
        pooled = h.max(dim=2).values
        return self.fc(pooled).squeeze(-1)


def _fit_torch(module, x_pack, y, spec: LearnSpec) -> None:
    import torch
    from torch.nn.functional import binary_cross_entropy_with_logits

    _seed_torch(spec.seed)
    opt = torch.optim.Adam(
        module.params.parameters(),
        lr=spec.lr,
        weight_decay=spec.weight_decay,
    )
    y_t = torch.tensor(y, dtype=torch.float32)
    tensors = [torch.tensor(a) for a in x_pack]
    n = y_t.shape[0]
    g = torch.Generator()
    g.manual_seed(spec.seed)
    for _ in range(spec.epochs):
        order = torch.randperm(n, generator=g)
        logits = module.logits(*[t[order] for t in tensors])
        loss = binary_cross_entropy_with_logits(logits, y_t[order])
        opt.zero_grad()
        loss.backward()
        opt.step()


def fit_tokmlp(twins: Sequence[Twin], spec: LearnSpec) -> ScoreFn:
    import torch

    tok_rows = []
    pos_rows = []
    mask_rows = []
    labels = []
    for _stem, _sample, marked, unmarked, _prefix in _draws(twins):
        for seq, label in ((marked, 1.0), (unmarked, 0.0)):
            tok_idx, pos_idx, mask = _tokmlp_indices(seq, spec)
            tok_rows.append(tok_idx)
            pos_rows.append(pos_idx)
            mask_rows.append(mask)
            labels.append(label)
    if len(set(labels)) < 2:
        raise ValueError("tokmlp needs both classes")
    net = _TokMLP(spec)
    _fit_torch(
        net,
        (np.stack(tok_rows), np.stack(pos_rows), np.stack(mask_rows)),
        np.asarray(labels, dtype=np.float32),
        spec,
    )
    net.params.eval()

    def score(seq, prefix: Sequence[int] = ()) -> float:
        del prefix
        tok_idx, pos_idx, mask = _tokmlp_indices(seq, spec)
        with torch.no_grad():
            logit = net.logits(
                torch.tensor(tok_idx).unsqueeze(0),
                torch.tensor(pos_idx).unsqueeze(0),
                torch.tensor(mask).unsqueeze(0),
            )
        return float(logit.item())

    return score


def fit_charcnn(
    twins: Sequence[Twin],
    spec: LearnSpec,
    *,
    tokenizer=None,
    score_tokenizer=None,
) -> ScoreFn:
    import torch

    decode_train = tokenizer
    decode_score = score_tokenizer if score_tokenizer is not None else tokenizer
    byte_rows = []
    mask_rows = []
    labels = []
    start = 0 if spec.include_first else 1
    for _stem, _sample, marked, unmarked, _prefix in _draws(twins):
        for seq, label in ((marked, 1.0), (unmarked, 0.0)):
            raw = ids_to_bytes(seq[start:], decode_train)
            idx, mask = _byte_indices(raw, spec)
            byte_rows.append(idx)
            mask_rows.append(mask)
            labels.append(label)
    if len(set(labels)) < 2:
        raise ValueError("charcnn needs both classes")
    net = _CharCNN(spec)
    _fit_torch(
        net,
        (np.stack(byte_rows), np.stack(mask_rows)),
        np.asarray(labels, dtype=np.float32),
        spec,
    )
    net.params.eval()

    def score(seq, prefix: Sequence[int] = ()) -> float:
        del prefix
        raw = ids_to_bytes(seq[start:], decode_score)
        idx, mask = _byte_indices(raw, spec)
        with torch.no_grad():
            logit = net.logits(
                torch.tensor(idx).unsqueeze(0),
                torch.tensor(mask).unsqueeze(0),
            )
        return float(logit.item())

    return score


def fit_scorer(
    twins: Sequence[Twin],
    arch: str,
    spec: LearnSpec,
    *,
    tokenizer=None,
    score_tokenizer=None,
) -> ScoreFn:
    if arch == "hashlog":
        return fit_hashlog(twins, spec)
    if arch == "tokmlp":
        return fit_tokmlp(twins, spec)
    if arch == "charcnn":
        return fit_charcnn(
            twins,
            spec,
            tokenizer=tokenizer,
            score_tokenizer=score_tokenizer,
        )
    raise ValueError(f"unknown learn arch {arch!r}")


def rotate_learn(
    twins: Sequence[Twin],
    *,
    arch: str,
    spec: LearnSpec,
    model_name: str,
    tokenizer=None,
    score_tokenizer=None,
) -> IndicatorHoldout:
    if len(twins) < 3:
        raise ValueError("learn rotate needs at least three prompts")
    parts = _empty_holdout_parts()
    decode = score_tokenizer if score_tokenizer is not None else tokenizer
    for held in twins:
        train = [t for t in twins if t.stem != held.stem]
        scorer = fit_scorer(
            train,
            arch,
            spec,
            tokenizer=tokenizer,
            score_tokenizer=decode,
        )
        held_prefix = _twin_prefix(held, spec.prompt_context)
        marked = held.marked_seqs()
        unmarked = held.unmarked_seqs()
        n = min(len(marked), len(unmarked))
        for i in range(n):
            _append_pair(
                parts,
                held.stem,
                i + 1,
                scorer(marked[i], prefix=held_prefix),
                scorer(unmarked[i], prefix=held_prefix),
            )
    return _holdout_from_parts(
        parts,
        context_len=spec.context_len,
        model_name=model_name,
        instance=INSTANCE[arch],
        score_kind=arch,
        used_keys=False,
        used_hash_iv=False,
        used_g_values=False,
        mode="rotate",
    )


def _clip(twins: Sequence[Twin], fit_prefix: int | None) -> list[Twin]:
    if fit_prefix and fit_prefix > 0:
        return clip_twins_prefix(list(twins), int(fit_prefix))
    return list(twins)


def run_learn(
    twins: Sequence[Twin],
    *,
    pair_dir: str = "",
    model_name: str = "gpt2",
    archs: Sequence[str] | None = None,
    spec: LearnSpec | None = None,
    fit_prefix: int | None = None,
    max_draws: int | None = None,
    tokenizer=None,
) -> ProbeRun:
    spec = spec or LearnSpec()
    names = _validate_archs(archs)
    work = list(twins)
    if max_draws and max_draws > 0:
        work = clip_twins(work, int(max_draws))
    work = _clip(work, fit_prefix)
    run = ProbeRun(
        pair_dir=pair_dir,
        model_name=model_name,
        context_len=spec.context_len,
        max_draws=max_draws,
        fit_prefix=int(fit_prefix) if fit_prefix and fit_prefix > 0 else None,
        position_bucket=spec.position_bucket,
        include_first=spec.include_first,
        prompt_context=spec.prompt_context,
        note=LEARN_NOTE,
    )
    for arch in names:
        ev = rotate_learn(
            work,
            arch=arch,
            spec=spec,
            model_name=model_name,
            tokenizer=tokenizer,
        )
        run.methods.append(summarize_holdout(arch, ev))
    run.used_keys = any(m.holdout.used_keys for m in run.methods)
    run.used_hash_iv = any(m.holdout.used_hash_iv for m in run.methods)
    run.used_g_values = any(m.holdout.used_g_values for m in run.methods)
    return run


def run_learn_transfer(
    train_twins: Sequence[Twin],
    test_twins: Sequence[Twin],
    *,
    train_dir: str = "",
    test_dir: str = "",
    model_name: str = "gpt2",
    archs: Sequence[str] | None = None,
    spec: LearnSpec | None = None,
    fit_prefix: int | None = None,
    overlap_mode: str = "drop-from-train",
    nested: bool = True,
    shuffle_labels: bool = False,
    shuffle_seed: int = 0,
    tokenizer=None,
    score_tokenizer=None,
) -> TransferRun:
    spec = spec or LearnSpec()
    names = _validate_archs(archs)
    train, test, overlap = apply_overlap(
        train_twins, test_twins, mode=overlap_mode
    )
    train = _clip(train, fit_prefix)
    test = _clip(test, fit_prefix)
    if shuffle_labels:
        train = shuffle_twin_sides(train, seed=shuffle_seed)
    if len(train) < 1:
        raise ValueError("learn transfer left no training prompts")
    if len(test) < 1:
        raise ValueError("learn transfer left no test prompts")
    run = TransferRun(
        train_dir=train_dir,
        test_dir=test_dir,
        n_train_prompts=len(train),
        n_test_prompts=len(test),
        dropped_stems=list(overlap),
        overlap_mode=overlap_mode,
        model_name=model_name,
        context_len=spec.context_len,
        nested=nested,
        shuffle_seed=shuffle_seed if shuffle_labels else None,
        fit_prefix=int(fit_prefix) if fit_prefix and fit_prefix > 0 else None,
        position_bucket=spec.position_bucket,
        include_first=spec.include_first,
        prompt_context=spec.prompt_context,
        note=LEARN_NOTE,
    )
    test_holdouts: dict[str, IndicatorHoldout] = {}
    for arch in names:
        scorer = fit_scorer(
            train,
            arch,
            spec,
            tokenizer=tokenizer,
            score_tokenizer=score_tokenizer,
        )
        ev = score_twins(
            test,
            scorer,
            context_len=spec.context_len,
            model_name=model_name,
            instance=INSTANCE[arch],
            score_kind=arch,
            seq_mode="ids",
            prompt_context=spec.prompt_context and arch == "hashlog",
        )
        run.methods.append(summarize_holdout(arch, ev))
        train_ev = score_twins(
            train,
            scorer,
            context_len=spec.context_len,
            model_name=model_name,
            instance=INSTANCE[arch],
            score_kind=arch,
            seq_mode="ids",
            prompt_context=spec.prompt_context and arch == "hashlog",
        )
        train_bin = binary_eval(train_ev.marked_lrs, train_ev.unmarked_lrs)
        _append_threshold(
            run,
            name=arch,
            source="in-sample-youden",
            threshold=train_bin.youden_threshold,
            test_ev=ev,
        )
        test_holdouts[arch] = ev
    if nested and len(train) >= 3:
        for arch in names:
            loo = rotate_learn(
                train,
                arch=arch,
                spec=spec,
                model_name=model_name,
                tokenizer=tokenizer,
            )
            test_ev = test_holdouts[arch]
            loo_bin = binary_eval(loo.marked_lrs, loo.unmarked_lrs)
            _append_threshold(
                run,
                name=arch,
                source="nested-youden",
                threshold=loo_bin.youden_threshold,
                test_ev=test_ev,
            )
            _append_threshold(
                run,
                name=arch,
                source="nested-fpr10",
                threshold=threshold_at_fpr(loo.unmarked_lrs, fpr=0.10),
                test_ev=test_ev,
            )
    run.used_keys = any(m.holdout.used_keys for m in run.methods)
    run.used_hash_iv = any(m.holdout.used_hash_iv for m in run.methods)
    run.used_g_values = any(m.holdout.used_g_values for m in run.methods)
    return run


def spec_from_args(
    *,
    context_len: int = 4,
    pos_bucket: int = 1,
    include_first: bool = False,
    prompt_context: bool = False,
    n_hashes: int = 4,
    n_buckets: int = 64,
    seed: int = 20260831,
    epochs: int = 40,
) -> LearnSpec:
    return LearnSpec(
        context_len=int(context_len),
        position_bucket=int(pos_bucket) if pos_bucket and pos_bucket > 0 else 0,
        include_first=bool(include_first),
        prompt_context=bool(prompt_context),
        n_hashes=int(n_hashes),
        n_buckets=int(n_buckets),
        seed=int(seed),
        epochs=int(epochs),
    )


def print_learn(run: ProbeRun) -> str:
    return print_probe(run)


def print_learn_transfer(run: TransferRun) -> str:
    return print_transfer(run)


def persist_learn(run: ProbeRun, out_dir: Path) -> None:
    persist_probe(run, out_dir)
    out_dir = Path(out_dir)
    body = (
        "# Key-free learned scorers\n\n"
        + LEARN_NOTE
        + "\n\n"
        + CAVEAT
        + "\n\n"
        + print_learn(run)
        + "\n"
    )
    (out_dir / "README.md").write_text(body)
    (out_dir / "results.md").write_text(body)


def persist_learn_transfer(run: TransferRun, out_dir: Path) -> None:
    persist_transfer(run, out_dir)
    out_dir = Path(out_dir)
    body = (
        "# Key-free learned transfer\n\n"
        + LEARN_NOTE
        + "\n\n"
        + CAVEAT
        + "\n\n"
        + print_learn_transfer(run)
        + "\n"
    )
    (out_dir / "README.md").write_text(body)
    (out_dir / "results.md").write_text(body)
