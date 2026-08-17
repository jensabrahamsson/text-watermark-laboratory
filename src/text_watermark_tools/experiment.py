"""Known-mark experiment: generate → query-fit → rewrite → official score."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

import torch

from text_watermark_tools.generate import (
    DEFAULT_PROMPT,
    Generation,
    _load_marked_model,
    _load_unmarked_model,
    generate_text,
)
from text_watermark_tools.score import (
    OfficialScore,
    format_score,
    load_tokenizer,
    official_score_text,
    official_score_token_ids,
)
from text_watermark_tools.surrogate import (
    SURROGATE_CONTEXT_LEN,
    Surrogate,
    fit_surrogate,
    observations_from_sequence,
    query_marked_generator,
    rewrite_token_ids,
    unmarked_replacements_for,
)


@dataclass
class ExperimentResult:
    source_text: str
    rewrite_text: str
    source: OfficialScore
    rewrite: OfficialScore
    n_queries: int
    n_observations: int
    n_replacements: int
    fit_used_keys: bool
    fit_used_hash_iv: bool
    fit_used_g_values: bool
    source_mean_above_half: bool
    rewrite_closer_to_half: bool


def run_known_mark_experiment(
    *,
    prompt: str = DEFAULT_PROMPT,
    max_new_tokens: int = 320,
    n_positions: int = 0,
    samples_per_position: int = 1,
    seed: int = 0,
    tokenizer=None,
    marked_model=None,
    unmarked_model=None,
) -> ExperimentResult:
    tok = tokenizer or load_tokenizer()
    device = torch.device("cpu")
    if marked_model is None:
        marked_model = _load_marked_model(device)
    if unmarked_model is None:
        unmarked_model = _load_unmarked_model(device)

    gen: Generation = generate_text(
        prompt,
        marked=True,
        max_new_tokens=max_new_tokens,
        seed=seed,
        device=device,
        tokenizer=tok,
        model=marked_model,
    )
    source_score = official_score_token_ids(gen.token_ids, tokenizer=tok)

    src_ids = gen.token_ids[0].tolist()
    # Every source token is a marked generate() observation. Extra queries
    # are optional (n_positions==0 → none).
    observations = observations_from_sequence(
        src_ids, context_len=SURROGATE_CONTEXT_LEN
    )
    extra, n_queries = query_marked_generator(
        gen.token_ids,
        model=marked_model,
        pad_token_id=tok.eos_token_id,
        n_positions=n_positions,
        samples_per_position=samples_per_position,
        context_len=SURROGATE_CONTEXT_LEN,
        seed=seed + 1,
    )
    observations.extend(extra)
    n_queries += len(src_ids)  # source tokens themselves came from generate()
    surrogate: Surrogate = fit_surrogate(observations, n_queries=n_queries)
    if surrogate.used_keys or surrogate.used_hash_iv or surrogate.used_g_values:
        raise RuntimeError("surrogate fit consulted keys / hash_iv / g-values")

    replacements = unmarked_replacements_for(
        src_ids,
        surrogate,
        model=unmarked_model,
        pad_token_id=tok.eos_token_id,
    )
    new_ids = rewrite_token_ids(src_ids, surrogate, unmarked_replacements=replacements)
    n_replacements = sum(int(a != b) for a, b in zip(src_ids, new_ids))
    rewrite_text = tok.decode(new_ids, skip_special_tokens=True)
    rewrite_score = official_score_token_ids(
        torch.tensor([new_ids], dtype=torch.long), tokenizer=tok
    )

    return ExperimentResult(
        source_text=gen.text,
        rewrite_text=rewrite_text,
        source=source_score,
        rewrite=rewrite_score,
        n_queries=n_queries,
        n_observations=surrogate.n_observations,
        n_replacements=n_replacements,
        fit_used_keys=surrogate.used_keys,
        fit_used_hash_iv=surrogate.used_hash_iv,
        fit_used_g_values=surrogate.used_g_values,
        source_mean_above_half=source_score.mean > 0.5,
        rewrite_closer_to_half=rewrite_score.closer_to_half_than(source_score),
    )


def persist_result(result: ExperimentResult, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "source.txt").write_text(result.source_text.strip() + "\n")
    (out_dir / "rewrite.txt").write_text(result.rewrite_text.strip() + "\n")
    table = {
        "source": {
            "mean": result.source.mean,
            "weighted_mean": result.source.weighted_mean,
            "n_tokens": result.source.n_tokens,
            "n_unmasked_ngrams": result.source.n_unmasked_ngrams,
        },
        "rewrite": {
            "mean": result.rewrite.mean,
            "weighted_mean": result.rewrite.weighted_mean,
            "n_tokens": result.rewrite.n_tokens,
            "n_unmasked_ngrams": result.rewrite.n_unmasked_ngrams,
        },
        "n_queries": result.n_queries,
        "n_observations": result.n_observations,
        "n_replacements": result.n_replacements,
        "fit_used_keys": result.fit_used_keys,
        "fit_used_hash_iv": result.fit_used_hash_iv,
        "fit_used_g_values": result.fit_used_g_values,
        "source_mean_above_half": result.source_mean_above_half,
        "rewrite_closer_to_half": result.rewrite_closer_to_half,
        "rewrite_mean_closer": abs(result.rewrite.mean - 0.5)
        < abs(result.source.mean - 0.5),
        "rewrite_weighted_closer": abs(result.rewrite.weighted_mean - 0.5)
        < abs(result.source.weighted_mean - 0.5),
    }
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    lines = [
        "# Known-mark mixin experiment",
        "",
        "| | Mean | Weighted mean | Tokens | Unmasked n-grams |",
        "|---|---|---|---|---|",
        (
            f"| source | {result.source.mean:.6f} | {result.source.weighted_mean:.6f} "
            f"| {result.source.n_tokens} | {result.source.n_unmasked_ngrams} |"
        ),
        (
            f"| rewrite | {result.rewrite.mean:.6f} | {result.rewrite.weighted_mean:.6f} "
            f"| {result.rewrite.n_tokens} | {result.rewrite.n_unmasked_ngrams} |"
        ),
        "",
        f"Queries: {result.n_queries}. Observations: {result.n_observations}. "
        f"Replacements: {result.n_replacements}.",
        f"Fit consulted keys: {result.fit_used_keys}. "
        f"hash_iv: {result.fit_used_hash_iv}. g-values: {result.fit_used_g_values}.",
        "",
    ]
    (out_dir / "results.md").write_text("\n".join(lines))


def print_result(result: ExperimentResult) -> str:
    chunks = [
        format_score("source", result.source),
        format_score("rewrite", result.rewrite),
        (
            f"queries={result.n_queries} observations={result.n_observations} "
            f"replacements={result.n_replacements}"
        ),
        (
            "fit consulted keys=False hash_iv=False g-values=False "
            f"(flags keys={result.fit_used_keys} "
            f"hash_iv={result.fit_used_hash_iv} "
            f"g_values={result.fit_used_g_values})"
        ),
        f"source_mean_above_half={result.source_mean_above_half}",
        f"rewrite_closer_to_half={result.rewrite_closer_to_half}",
    ]
    return "\n".join(chunks)
