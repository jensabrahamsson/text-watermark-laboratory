"""Argmax snap scrub: verifiable watermark scrubbing on token ids and files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from text_watermark_tools.probe_models import ScrubRow, ScrubRun


def scrub_token_ids(
    token_ids: Sequence[int],
    lm,
    *,
    top_k: int = 40,
    only_if_in_topk: bool = True,
    logits=None,
) -> tuple[list[int], int]:
    from text_watermark_tools.pivot import (
        snap_to_unmarked_argmax,
        unmarked_logits_for_sequence,
    )

    rows = logits if logits is not None else unmarked_logits_for_sequence(
        token_ids, lm
    )
    return snap_to_unmarked_argmax(
        token_ids, rows, top_k=top_k, only_if_in_topk=only_if_in_topk
    )


def run_scrub_files(
    files: Sequence[Path],
    *,
    model_name: str = "gpt2",
    top_k: int = 40,
    lm=None,
    tokenizer=None,
) -> ScrubRun:
    from text_watermark_tools.generate import _load_unmarked_model, generate_device
    from text_watermark_tools.score import (
        PUBLIC_INSTANCE,
        load_tokenizer,
        official_score_token_ids,
    )
    import torch

    tok = tokenizer or load_tokenizer(model_name)
    if lm is None:
        lm = _load_unmarked_model(generate_device(), model_name=model_name)
    rows: list[ScrubRow] = []
    for path in files:
        text = Path(path).read_text()
        ids = tok(text)["input_ids"]
        snapped, n_flips = scrub_token_ids(ids, lm, top_k=top_k)
        before = official_score_token_ids(
            torch.tensor([ids], dtype=torch.long), tokenizer=tok
        )
        after = official_score_token_ids(
            torch.tensor([snapped], dtype=torch.long), tokenizer=tok
        )
        rows.append(
            ScrubRow(
                path=str(path),
                n_tokens=len(ids),
                n_flips=n_flips,
                mean_before=before.mean,
                weighted_before=before.weighted_mean,
                mean_after=after.mean,
                weighted_after=after.weighted_mean,
                used_keys_for_snap=False,
            )
        )
    return ScrubRun(
        rows=rows,
        model_name=model_name,
        instance=PUBLIC_INSTANCE,
        used_keys_for_snap=False,
        used_hash_iv=False,
        used_g_values=False,
    )


def print_scrub(run: ScrubRun) -> str:
    lines = [
        (
            f"scrub n_files={len(run.rows)} model={run.model_name} "
            f"snap_used_keys={run.used_keys_for_snap} "
            f"reference_instance={run.instance} "
            f"hash_iv={run.used_hash_iv} g_values={run.used_g_values}"
        ),
        "Argmax snap does not use watermark keys. Official scores are a reference check.",
        "",
        "| file | flips | mean before | mean after |",
        "|---|---|---|---|",
    ]
    for row in run.rows:
        name = Path(row.path).name
        lines.append(
            f"| {name} | {row.n_flips}/{row.n_tokens} | "
            f"{row.mean_before:.4f} | {row.mean_after:.4f} |"
        )
    if run.rows:
        mb = sum(r.mean_before for r in run.rows) / len(run.rows)
        ma = sum(r.mean_after for r in run.rows) / len(run.rows)
        lines.append("")
        lines.append(f"mean official before={mb:.4f} after={ma:.4f}")
    return "\n".join(lines)


def persist_scrub(run: ScrubRun, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "model_name": run.model_name,
        "instance": run.instance,
        "used_keys_for_snap": run.used_keys_for_snap,
        "used_hash_iv": run.used_hash_iv,
        "used_g_values": run.used_g_values,
        "rows": [row.__dict__ for row in run.rows],
    }
    (out_dir / "results.json").write_text(json.dumps(payload, indent=2) + "\n")
    (out_dir / "results.md").write_text("# Argmax snap scrub\n\n" + print_scrub(run) + "\n")
