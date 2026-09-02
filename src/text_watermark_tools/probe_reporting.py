"""Reporting, formatting, and persistence of probe and transfer results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from text_watermark_tools.indicator import (
    CAVEAT,
    IndicatorHoldout,
    persist_holdout,
    persist_indicator,
)
from text_watermark_tools.probe_models import (
    MethodSummary,
    ProbeRun,
    ThresholdRow,
    TransferRun,
    _window_dir,
)
from text_watermark_tools.stats import (
    binary_eval,
    binary_eval_to_dict,
    coverage_gate,
    coverage_gate_to_dict,
    counts_at_threshold,
    format_binary_eval,
    format_coverage_gate,
    nested_stem_eval_to_dict,
    nested_threshold_by_stem,
)
from text_watermark_tools.transfer import persist_hashpool


def print_coverage(cov: dict) -> str:
    lines = [
        (
            f"coverage n_prompts={cov['n_prompts']} n_files={cov['n_files']} "
            f"context_len={cov['context_len']} pos_bucket={cov['position_bucket']} "
            f"used_keys={cov['used_keys']}"
        ),
        cov.get("note", ""),
        "",
        "| window | shared last-4 | n | mean support when shared |",
        "|---|---|---|---|",
    ]
    for row in cov.get("by_window") or []:
        lines.append(
            f"| {row['start']}:{row['end']} | {row['shared_frac']:.3f} "
            f"({row['shared']}/{row['n']}) | {row['n']} | "
            f"{row['mean_shared_support']:.2f} |"
        )
    return "\n".join(lines)


def persist_coverage(cov: dict, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "coverage.json").write_text(json.dumps(cov, indent=2) + "\n")
    (out_dir / "coverage.md").write_text(
        "# Key-free last-4 coverage by position\n\n"
        + print_coverage(cov)
        + "\n"
    )


def summarize_holdout(name: str, ev: IndicatorHoldout) -> MethodSummary:
    binary = binary_eval(ev.marked_lrs, ev.unmarked_lrs)
    return MethodSummary(
        name=name,
        holdout=ev,
        binary=binary,
        n_prompt_wins=ev.n_prompts_marked_above,
        n_prompts=ev.n_prompts,
    )


def _ranking_without_tp_md(methods: Sequence[MethodSummary]) -> list[str]:
    lines = [
        "",
        (
            "| method | prompt wins | ranking wins with no isolated TP | "
            "ranking losses with isolated TP |"
        ),
        "|---|---|---|---|",
    ]
    for m in methods:
        hide = m.holdout.ranking_without_isolated_tp
        loss = m.holdout.ranking_losses_with_isolated_tp
        hide_cell = f"{len(hide)}/{m.n_prompt_wins}"
        if 0 < len(hide) <= 6:
            hide_cell += f" ({', '.join(hide)})"
        loss_cell = str(len(loss))
        if 0 < len(loss) <= 6:
            loss_cell += f" ({', '.join(loss)})"
        lines.append(
            f"| {m.name} | {m.n_prompt_wins}/{m.n_prompts} | "
            f"{hide_cell} | {loss_cell} |"
        )
    lines.append("")
    lines.append(
        "Ranking wins with no isolated TP are prompt groups whose marked "
        "mean LR beats unmarked while every marked file has lr<=0. Ranking "
        "losses with isolated TP still have marked files above 0 but lose "
        "the prompt-mean comparison. Neither column is a detector."
    )
    return lines


def nested_stem_gates(ev: IndicatorHoldout) -> dict:
    """Youden and 10% FPR leave-one-stem thresholds on held-out LRs."""
    youden = nested_threshold_by_stem(ev.stems, ev.marked_lrs, ev.unmarked_lrs)
    fpr10 = nested_threshold_by_stem(
        ev.stems, ev.marked_lrs, ev.unmarked_lrs, fpr=0.10
    )
    return {
        "nested-youden-by-stem": nested_stem_eval_to_dict(youden),
        "nested-fpr10-by-stem": nested_stem_eval_to_dict(fpr10),
    }


def _store_prefixes(
    dest: dict[int, list[MethodSummary]],
    src: dict[int, dict[str, IndicatorHoldout]],
) -> None:
    for plen, by_name in src.items():
        bucket = dest.setdefault(int(plen), [])
        seen = {m.name for m in bucket}
        for name, ev in by_name.items():
            if name in seen:
                continue
            bucket.append(summarize_holdout(name, ev))
            seen.add(name)


def _store_windows(
    dest: dict[tuple[int, int], list[MethodSummary]],
    src: dict[tuple[int, int], dict[str, IndicatorHoldout]],
) -> None:
    for win, by_name in src.items():
        bucket = dest.setdefault(win, [])
        seen = {m.name for m in bucket}
        for name, ev in by_name.items():
            if name in seen:
                continue
            bucket.append(summarize_holdout(name, ev))
            seen.add(name)


def _append_threshold(
    run: TransferRun,
    *,
    name: str,
    source: str,
    threshold: float,
    test_ev: IndicatorHoldout,
) -> None:
    tp, tn, sens, spec = counts_at_threshold(
        test_ev.marked_lrs, test_ev.unmarked_lrs, threshold
    )
    run.thresholds.append(
        ThresholdRow(
            name=name,
            train_youden=threshold,
            n_marked_above=tp,
            n_unmarked_at_most=tn,
            n_marked=len(test_ev.marked_lrs),
            n_unmarked=len(test_ev.unmarked_lrs),
            sensitivity=sens,
            specificity=spec,
            source=source,
        )
    )


def format_cascade(payload: dict) -> list[str]:
    """Human lines for the count-then-fallback isolated-file protocol."""
    prec = payload.get("count_precision")
    prec_s = f"{prec:.3f}" if isinstance(prec, float) and prec == prec else "nan"
    n_pm = max(int(payload.get("n_pivot_marked") or 0), 1)
    n_pu = max(int(payload.get("n_pivot_unmarked") or 0), 1)
    n_cm = max(int(payload.get("n_count_marked") or 0), 1)
    n_cu = max(int(payload.get("n_count_unmarked") or 0), 1)
    fallback = str(payload.get("fallback") or "pivot")
    when = str(payload.get("cascade_when") or "coverage")
    if when == "positive":
        rule = (
            f"Cascade: count LR when lr>0, unmarked-LM {fallback} when count "
            "is nonpositive (zeros and covered negatives). "
        )
    else:
        rule = (
            f"Cascade: count LR when n_used>0, unmarked-LM {fallback} otherwise. "
        )
    lines = [
        (
            rule
            + "Signs at 0 are comparable. Mixed AUC is not a detector. "
            "Not keys, not a universal detector."
        ),
        (
            f"count_method={payload.get('count_method')} "
            f"fallback={fallback} "
            f"cascade_when={when} "
            f"pivot_weight={payload.get('pivot_weight')} "
            f"prompt_context={payload.get('prompt_context')} "
            f"used_keys={payload.get('used_keys')}"
        ),
        (
            f"count covered marked {payload.get('n_count_marked')}/"
            f"{payload.get('n_marked')} >0 "
            f"{payload.get('count_marked_above_zero')}/{n_cm} unmarked<=0 "
            f"{payload.get('count_unmarked_at_most_zero')}/{n_cu} "
            f"precision={prec_s}"
        ),
        (
            f"{fallback} fallback marked {payload.get('n_pivot_marked')}/"
            f"{payload.get('n_marked')} >0 "
            f"{payload.get('pivot_marked_above_zero')}/{n_pm} unmarked<=0 "
            f"{payload.get('pivot_unmarked_at_most_zero')}/{n_pu}"
        ),
        (
            f"combined marked>0 {payload.get('combined_marked_above_zero')}/"
            f"{payload.get('n_marked')} unmarked<=0 "
            f"{payload.get('combined_unmarked_at_most_zero')}/"
            f"{payload.get('n_unmarked')}"
        ),
    ]
    if payload.get("rankpath_end"):
        lines.append(
            f"cascade rankpath_end={payload.get('rankpath_end')} "
            "(opening prefix-N, not the full file)"
        )
    fb10 = payload.get("fallback_fpr10") or {}
    comb10 = payload.get("combined_at_fallback_fpr10") or {}
    if fb10:
        lines.append(
            f"{fallback} uncovered FPR10 t={float(fb10.get('threshold') or 0):.4f} "
            f"marked>t {fb10.get('marked_above')}/{fb10.get('n_marked')} "
            f"unmarked<=t {fb10.get('unmarked_at_most')}/{fb10.get('n_unmarked')}"
        )
    if comb10:
        lines.append(
            f"combined at fallback FPR10 marked>t "
            f"{comb10.get('marked_above')}/{comb10.get('n_marked')} "
            f"unmarked<=t {comb10.get('unmarked_at_most')}/{comb10.get('n_unmarked')}. "
            "Count stays at 0; mixed AUC is still not a detector."
        )
    marked_fallback = payload.get("pivot_fallback_marked") or []
    if marked_fallback:
        lines.append(f"{fallback}-fallback marked files:")
        for row in marked_fallback:
            score = float(row.get("score") or 0.0)
            sign = "lr>0" if score > 0.0 else "lr<=0"
            lines.append(
                f"- `{row.get('stem')}` draw {row.get('sample')}: "
                f"{row.get('opening_text', '')} {sign}={score:.4f}"
            )
    return lines


def _cascade_json(payload: dict | None) -> dict | None:
    import math

    if not payload:
        return None

    def conv(x):
        if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
            return None
        if isinstance(x, dict):
            return {k: conv(v) for k, v in x.items()}
        if isinstance(x, list):
            return [conv(v) for v in x]
        return x

    return conv(payload)


def print_probe(run: ProbeRun) -> str:
    lines = [
        (
            f"probe n_methods={len(run.methods)} pair_dir={run.pair_dir} "
            f"context_len={run.context_len} model={run.model_name} "
            f"max_draws={run.max_draws} prefix_lens={list(run.prefix_lens)} "
            f"windows={[f'{a}:{b}' for a, b in run.windows]} "
            f"fit_prefix={run.fit_prefix} pos_bucket={run.position_bucket} "
            f"rankpath_full={getattr(run, 'rankpath_full', False)} "
            f"rankpath_pos_bucket={getattr(run, 'rankpath_pos_bucket', None)} "
            f"cascade_rankpath_end={getattr(run, 'cascade_rankpath_end', None)} "
            f"cascade_when={getattr(run, 'cascade_when', 'coverage')} "
            f"include_first={run.include_first} prompt_context={run.prompt_context} "
            f"used_keys={run.used_keys} hash_iv={run.used_hash_iv} "
            f"g_values={run.used_g_values}"
        ),
        run.note,
        CAVEAT,
        "",
        (
            "| method | prompt wins | file auc | marked>0 | unmarked<=0 "
            "| perm p | mean diff |"
        ),
        "|---|---|---|---|---|---|---|",
    ]
    for m in run.methods:
        b = m.binary
        lines.append(
            f"| {m.name} | {m.n_prompt_wins}/{m.n_prompts} | {b.auc:.3f} | "
            f"{b.n_positive_above_zero}/{b.n_positive} | "
            f"{b.n_negative_at_most_zero}/{b.n_negative} | "
            f"{b.permutation_p:.4g} | {b.mean_diff:.4f} |"
        )
    lines.extend(_ranking_without_tp_md(run.methods))
    lines.append("")
    lines.append(
        "| method | marked zeros | unmarked zeros | decided tp/fn | "
        "decided fp/tn | precision |"
    )
    lines.append("|---|---|---|---|---|---|")
    for m in run.methods:
        g = coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs)
        prec = f"{g.precision:.3f}" if g.precision == g.precision else "nan"
        lines.append(
            f"| {m.name} | {g.n_marked_zero}/{g.n_marked} | "
            f"{g.n_unmarked_zero}/{g.n_unmarked} | "
            f"{g.decided_tp}/{g.decided_fn} | {g.decided_fp}/{g.decided_tn} | "
            f"{prec} |"
        )
    lines.append("")
    lines.append(
        "| method | nested-youden-by-stem marked>t | unmarked<=t | "
        "mean t | sens | spec |"
    )
    lines.append("|---|---|---|---|---|---|")
    for m in run.methods:
        gate = nested_stem_gates(m.holdout)["nested-youden-by-stem"]
        lines.append(
            f"| {m.name} | {gate['n_marked_above']}/{gate['n_marked']} | "
            f"{gate['n_unmarked_at_most']}/{gate['n_unmarked']} | "
            f"{gate['mean_threshold']:.4f} | {gate['sensitivity']:.3f} | "
            f"{gate['specificity']:.3f} |"
        )
    if run.prefixes:
        lines.append("")
        lines.append(
            "| prefix tokens | method | prompt wins | file auc | "
            "nested-by-stem marked | unmarked |"
        )
        lines.append("|---|---|---|---|---|---|")
        for plen in sorted(run.prefixes):
            for m in run.prefixes[plen]:
                gate = nested_stem_gates(m.holdout)["nested-youden-by-stem"]
                lines.append(
                    f"| {plen} | {m.name} | {m.n_prompt_wins}/{m.n_prompts} | "
                    f"{m.binary.auc:.3f} | "
                    f"{gate['n_marked_above']}/{gate['n_marked']} | "
                    f"{gate['n_unmarked_at_most']}/{gate['n_unmarked']} |"
                )
    if run.window_results:
        lines.append("")
        lines.append(
            "| window tokens | method | prompt wins | file auc | "
            "nested-by-stem marked | unmarked |"
        )
        lines.append("|---|---|---|---|---|---|")
        for start, end in sorted(run.window_results):
            for m in run.window_results[(start, end)]:
                gate = nested_stem_gates(m.holdout)["nested-youden-by-stem"]
                lines.append(
                    f"| {start}:{end} | {m.name} | "
                    f"{m.n_prompt_wins}/{m.n_prompts} | "
                    f"{m.binary.auc:.3f} | "
                    f"{gate['n_marked_above']}/{gate['n_marked']} | "
                    f"{gate['n_unmarked_at_most']}/{gate['n_unmarked']} |"
                )
    if run.cascade:
        lines.extend(["", *format_cascade(run.cascade)])
    if run.coverage:
        lines.append("")
        lines.append(print_coverage(run.coverage))
    lines.append("")
    for m in run.methods:
        lines.append(format_binary_eval(m.binary, label=m.name))
        lines.append(
            f"{m.name} prompts_marked_above={m.n_prompt_wins}/{m.n_prompts} "
            f"ranking_without_isolated_tp="
            f"{m.holdout.n_prompt_wins_without_isolated_tp}/"
            f"{m.n_prompt_wins} "
            f"ranking_losses_with_isolated_tp="
            f"{len(m.holdout.ranking_losses_with_isolated_tp)} "
            f"instance={m.holdout.instance} used_keys={m.holdout.used_keys}"
        )
    return "\n".join(lines)


def persist_probe(run: ProbeRun, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    table = {
        "pair_dir": run.pair_dir,
        "model_name": run.model_name,
        "context_len": run.context_len,
        "used_keys": run.used_keys,
        "used_hash_iv": run.used_hash_iv,
        "used_g_values": run.used_g_values,
        "max_draws": run.max_draws,
        "prefix_lens": list(run.prefix_lens),
        "windows": [f"{a}:{b}" for a, b in run.windows],
        "fit_prefix": run.fit_prefix,
        "position_bucket": run.position_bucket,
        "include_first": run.include_first,
        "prompt_context": run.prompt_context,
        "pivot_weights": list(run.pivot_weights),
        "rankpath_full": bool(getattr(run, "rankpath_full", False)),
        "rankpath_pos_bucket": getattr(run, "rankpath_pos_bucket", None),
        "cascade_rankpath_end": getattr(run, "cascade_rankpath_end", None),
        "cascade_when": getattr(run, "cascade_when", "coverage"),
        "note": run.note,
        "caveat": CAVEAT,
        "methods": [],
    }
    for m in run.methods:
        row = {
            "name": m.name,
            "instance": m.holdout.instance,
            "score_kind": m.holdout.score_kind,
            "n_prompt_wins": m.n_prompt_wins,
            "n_prompts": m.n_prompts,
            "n_marked_above_unmarked": m.holdout.n_marked_above_unmarked,
            **m.holdout.ranking_payload(),
            "used_keys": m.holdout.used_keys,
            "used_hash_iv": m.holdout.used_hash_iv,
            "used_g_values": m.holdout.used_g_values,
            "binary": binary_eval_to_dict(m.binary),
            "nested_stem": nested_stem_gates(m.holdout),
            "coverage_gate": coverage_gate_to_dict(
                coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs)
            ),
        }
        table["methods"].append(row)
        persist_holdout(m.holdout, out_dir / m.name)
    table["prefixes"] = []
    for plen in sorted(run.prefixes):
        for m in run.prefixes[plen]:
            table["prefixes"].append(
                {
                    "prefix_tokens": plen,
                    "name": m.name,
                    "n_prompt_wins": m.n_prompt_wins,
                    "n_prompts": m.n_prompts,
                    **m.holdout.ranking_payload(),
                    "binary": binary_eval_to_dict(m.binary),
                    "nested_stem": nested_stem_gates(m.holdout),
                    "used_keys": m.holdout.used_keys,
                }
            )
            persist_holdout(m.holdout, out_dir / f"prefix-{plen}" / m.name)
    table["window_scores"] = []
    for start, end in sorted(run.window_results):
        for m in run.window_results[(start, end)]:
            table["window_scores"].append(
                {
                    "start": start,
                    "end": end,
                    "name": m.name,
                    "n_prompt_wins": m.n_prompt_wins,
                    "n_prompts": m.n_prompts,
                    **m.holdout.ranking_payload(),
                    "binary": binary_eval_to_dict(m.binary),
                    "nested_stem": nested_stem_gates(m.holdout),
                    "used_keys": m.holdout.used_keys,
                }
            )
            persist_holdout(
                m.holdout, out_dir / _window_dir(start, end) / m.name
            )
    table["has_coverage"] = run.coverage is not None
    if run.coverage is not None:
        persist_coverage(run.coverage, out_dir)
    if run.cascade:
        (out_dir / "cascade.json").write_text(
            json.dumps(_cascade_json(run.cascade), indent=2) + "\n"
        )
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    (out_dir / "results.md").write_text(
        "# Key-free probe\n\n" + print_probe(run) + "\n"
    )


def print_transfer(run: TransferRun) -> str:
    lines = [
        (
            f"transfer n_methods={len(run.methods)} train={run.train_dir} "
            f"test={run.test_dir} n_train={run.n_train_prompts} "
            f"n_test={run.n_test_prompts} overlap_mode={run.overlap_mode} "
            f"dropped={len(run.dropped_stems)} context_len={run.context_len} "
            f"model={run.model_name} nested={getattr(run, 'nested', None)} "
            f"shuffle_seed={getattr(run, 'shuffle_seed', None)} used_keys={run.used_keys} "
            f"hash_iv={run.used_hash_iv} g_values={run.used_g_values} "
            f"include_first={run.include_first} prompt_context={run.prompt_context} "
            f"rankpath_full={getattr(run, 'rankpath_full', False)} "
            f"rankpath_pos_bucket={getattr(run, 'rankpath_pos_bucket', None)} "
            f"cascade_rankpath_end={getattr(run, 'cascade_rankpath_end', None)} "
            f"cascade_when={getattr(run, 'cascade_when', 'coverage')}"
        ),
        run.note,
        CAVEAT,
        "",
        (
            "| method | prompt wins | file auc | marked>0 | unmarked<=0 "
            "| perm p | mean diff |"
        ),
        "|---|---|---|---|---|---|---|",
    ]
    for m in run.methods:
        b = m.binary
        lines.append(
            f"| {m.name} | {m.n_prompt_wins}/{m.n_prompts} | {b.auc:.3f} | "
            f"{b.n_positive_above_zero}/{b.n_positive} | "
            f"{b.n_negative_at_most_zero}/{b.n_negative} | "
            f"{b.permutation_p:.4g} | {b.mean_diff:.4f} |"
        )
    lines.extend(_ranking_without_tp_md(run.methods))
    lines.append("")
    lines.append(
        "| method | marked zeros | unmarked zeros | decided tp/fn | "
        "decided fp/tn | precision |"
    )
    lines.append("|---|---|---|---|---|---|")
    for m in run.methods:
        g = coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs)
        prec = f"{g.precision:.3f}" if g.precision == g.precision else "nan"
        lines.append(
            f"| {m.name} | {g.n_marked_zero}/{g.n_marked} | "
            f"{g.n_unmarked_zero}/{g.n_unmarked} | "
            f"{g.decided_tp}/{g.decided_fn} | {g.decided_fp}/{g.decided_tn} | "
            f"{prec} |"
        )
    lines.append("")
    lines.append(
        "Zeros are lr==0: no shared last-k, or (tokhits/postokhits/"
        "tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/"
        "hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/"
        "hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/"
        "tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that "
        "context (or colliding hash). They are abstentions, not sign "
        "errors. poshits and hashpool can still score an *unseen* next "
        "token via Laplace; that occupancy artifact is not a token "
        "preference. tokbackoff / hashtokbackoff shrink last-k until an "
        "observed next token hits; tokbackoff2 / hashtokbackoff2 stop at "
        "last-2. hashtoklen / hashtoklenbackoff hash only exact last-k "
        "(short prefixes are not mixed into a longer-order table). "
        "hashskip hashes exact last-k with one token dropped (tagged "
        "skip-grams, not last-(k-1)). hashmask replaces one last-k token "
        "with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / "
        "hashmask2 / hashtok2 skip "
        "singleton hash collisions (min_count=2). hashtok is the hashpool analog of "
        "tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the "
        "opposite residual (hashtok only where tokhits abstains). "
        "None of these is key recovery."
    )
    lines.append("")
    lines.append(
        "| method | source | t | test marked>t | test unmarked≤t "
        "| sens | spec |"
    )
    lines.append("|---|---|---|---|---|---|---|")
    for row in run.thresholds:
        lines.append(
            f"| {row.name} | {row.source} | {row.train_youden:.4f} | "
            f"{row.n_marked_above}/{row.n_marked} | "
            f"{row.n_unmarked_at_most}/{row.n_unmarked} | "
            f"{row.sensitivity:.3f} | {row.specificity:.3f} |"
        )
    if run.dropped_stems:
        lines.append("")
        lines.append("dropped stems: " + ", ".join(run.dropped_stems))
    if run.prefixes:
        lines.append("")
        lines.append(
            "| prefix tokens | method | prompt wins | file auc | "
            "marked>0 | unmarked<=0 |"
        )
        lines.append("|---|---|---|---|---|---|")
        for plen in sorted(run.prefixes):
            for m in run.prefixes[plen]:
                b = m.binary
                lines.append(
                    f"| {plen} | {m.name} | {m.n_prompt_wins}/{m.n_prompts} | "
                    f"{b.auc:.3f} | {b.n_positive_above_zero}/{b.n_positive} | "
                    f"{b.n_negative_at_most_zero}/{b.n_negative} |"
                )
    if run.window_results:
        lines.append("")
        lines.append(
            "| window tokens | method | prompt wins | file auc | "
            "marked>0 | unmarked<=0 |"
        )
        lines.append("|---|---|---|---|---|---|")
        for start, end in sorted(run.window_results):
            for m in run.window_results[(start, end)]:
                b = m.binary
                lines.append(
                    f"| {start}:{end} | {m.name} | "
                    f"{m.n_prompt_wins}/{m.n_prompts} | "
                    f"{b.auc:.3f} | {b.n_positive_above_zero}/{b.n_positive} | "
                    f"{b.n_negative_at_most_zero}/{b.n_negative} |"
                )
    if run.cascade:
        lines.extend(["", *format_cascade(run.cascade)])
    lines.append("")
    for m in run.methods:
        lines.append(format_binary_eval(m.binary, label=m.name))
        lines.append(
            format_coverage_gate(
                coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs),
                label=m.name,
            )
        )
        lines.append(
            f"{m.name} prompts_marked_above={m.n_prompt_wins}/{m.n_prompts} "
            f"ranking_without_isolated_tp="
            f"{m.holdout.n_prompt_wins_without_isolated_tp}/"
            f"{m.n_prompt_wins} "
            f"ranking_losses_with_isolated_tp="
            f"{len(m.holdout.ranking_losses_with_isolated_tp)} "
            f"instance={m.holdout.instance} used_keys={m.holdout.used_keys}"
        )
    return "\n".join(lines)


def persist_transfer(run: TransferRun, out_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    table = {
        "train_dir": run.train_dir,
        "test_dir": run.test_dir,
        "n_train_prompts": run.n_train_prompts,
        "n_test_prompts": run.n_test_prompts,
        "dropped_stems": run.dropped_stems,
        "overlap_mode": run.overlap_mode,
        "model_name": run.model_name,
        "context_len": run.context_len,
        "used_keys": run.used_keys,
        "used_hash_iv": run.used_hash_iv,
        "used_g_values": run.used_g_values,
        "nested": getattr(run, "nested", None),
        "shuffle_seed": getattr(run, "shuffle_seed", None),
        "surface_context_len": getattr(run, "surface_context_len", None),
        "prefix_lens": list(run.prefix_lens),
        "windows": [f"{a}:{b}" for a, b in run.windows],
        "fit_prefix": run.fit_prefix,
        "position_bucket": run.position_bucket,
        "include_first": run.include_first,
        "prompt_context": run.prompt_context,
        "pivot_weights": list(getattr(run, "pivot_weights", ())),
        "rankpath_full": bool(getattr(run, "rankpath_full", False)),
        "rankpath_pos_bucket": getattr(run, "rankpath_pos_bucket", None),
        "cascade_fallback": getattr(run, "cascade_fallback", "pivot"),
        "cascade_rankpath_end": getattr(run, "cascade_rankpath_end", None),
        "cascade_when": getattr(run, "cascade_when", "coverage"),
        "note": run.note,
        "caveat": CAVEAT,
        "methods": [],
        "thresholds": [row.__dict__ for row in run.thresholds],
    }

    def _t(name: str, source: str) -> float | None:
        for row in run.thresholds:
            if row.name == name and row.source == source:
                return row.train_youden
        return None

    for m in run.methods:
        row = {
            "name": m.name,
            "instance": m.holdout.instance,
            "score_kind": m.holdout.score_kind,
            "n_prompt_wins": m.n_prompt_wins,
            "n_prompts": m.n_prompts,
            "n_marked_above_unmarked": m.holdout.n_marked_above_unmarked,
            **m.holdout.ranking_payload(),
            "used_keys": m.holdout.used_keys,
            "used_hash_iv": m.holdout.used_hash_iv,
            "used_g_values": m.holdout.used_g_values,
            "binary": binary_eval_to_dict(m.binary),
            "coverage_gate": coverage_gate_to_dict(
                coverage_gate(m.holdout.marked_lrs, m.holdout.unmarked_lrs)
            ),
        }
        table["methods"].append(row)
        persist_holdout(m.holdout, out_dir / m.name)
    persist_tables = getattr(run, "shuffle_seed", None) is None
    fit_n = int(run.fit_prefix or 0)
    present = {m.name for m in run.methods}

    def _present(*names: str) -> str | None:
        for name in names:
            if name in present:
                return name
        return None

    def _t_first(*pairs: tuple[str, str]) -> float | None:
        for name, source in pairs:
            val = _t(name, source)
            if val is not None:
                return val
        return None

    if persist_tables and getattr(run, "hash_model", None) is not None:
        nested_t = _t_first(
            ("hashpool", "nested-youden"),
            ("hashtok", "nested-youden"),
            ("hashtok2", "nested-youden"),
        )
        in_t = _t_first(
            ("hashpool", "in-sample-youden"),
            ("hashtok", "in-sample-youden"),
            ("hashtok2", "in-sample-youden"),
        )
        persist_hashpool(
            run.hash_model,
            out_dir / "tables-hashpool",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden" if nested_t is not None else "in-sample-youden"
            ),
            fit_prefix=fit_n,
            score_kind=_present("hashpool", "hashtok", "hashtok2") or "hashpool",
        )
    if persist_tables and getattr(run, "hash_len_model", None) is not None:
        nested_t = _t_first(
            ("hashtoklen", "nested-youden"),
            ("hashtoklen2", "nested-youden"),
        )
        in_t = _t_first(
            ("hashtoklen", "in-sample-youden"),
            ("hashtoklen2", "in-sample-youden"),
        )
        persist_hashpool(
            run.hash_len_model,
            out_dir / "tables-hashtoklen",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-hashtoklen"
                if nested_t is not None
                else "in-sample-youden-hashtoklen"
            ),
            fit_prefix=fit_n,
            score_kind=_present("hashtoklen", "hashtoklen2") or "hashtoklen",
        )
    if persist_tables and getattr(run, "hash_skip_model", None) is not None:
        nested_t = _t_first(
            ("hashskip", "nested-youden"),
            ("hashskip2", "nested-youden"),
        )
        in_t = _t_first(
            ("hashskip", "in-sample-youden"),
            ("hashskip2", "in-sample-youden"),
        )
        persist_hashpool(
            run.hash_skip_model,
            out_dir / "tables-hashskip",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-hashskip"
                if nested_t is not None
                else "in-sample-youden-hashskip"
            ),
            fit_prefix=fit_n,
            score_kind=_present("hashskip", "hashskip2") or "hashskip",
        )
    if persist_tables and getattr(run, "hash_mask_model", None) is not None:
        nested_t = _t_first(
            ("hashmask", "nested-youden"),
            ("hashmask2", "nested-youden"),
        )
        in_t = _t_first(
            ("hashmask", "in-sample-youden"),
            ("hashmask2", "in-sample-youden"),
        )
        persist_hashpool(
            run.hash_mask_model,
            out_dir / "tables-hashmask",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-hashmask"
                if nested_t is not None
                else "in-sample-youden-hashmask"
            ),
            fit_prefix=fit_n,
            score_kind=_present("hashmask", "hashmask2") or "hashmask",
        )
    if persist_tables and getattr(run, "surface_model", None) is not None:
        nested_t = _t("surface", "nested-youden")
        in_t = _t("surface", "in-sample-youden")
        persist_hashpool(
            run.surface_model,
            out_dir / "tables-surface",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-surface"
                if nested_t is not None
                else "in-sample-youden-surface"
            ),
            fit_prefix=fit_n,
        )
    if persist_tables and getattr(run, "count_model", None) is not None:
        nested_t = _t("hits", "nested-youden")
        in_t = _t("hits", "in-sample-youden")
        persist_indicator(
            run.count_model,
            out_dir / "tables-counts",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-hits" if nested_t is not None else "in-sample-youden-hits"
            ),
            fit_prefix=fit_n,
            score_kind="hits",
        )
    if persist_tables and getattr(run, "pos_model", None) is not None:
        nested_t = _t_first(
            ("poshits", "nested-youden"),
            ("poshitmass", "nested-youden"),
        )
        in_t = _t_first(
            ("poshits", "in-sample-youden"),
            ("poshitmass", "in-sample-youden"),
        )
        persist_indicator(
            run.pos_model,
            out_dir / "tables-poshits",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-poshits"
                if nested_t is not None
                else "in-sample-youden-poshits"
            ),
            fit_prefix=fit_n,
            score_kind="poshits",
        )
    if persist_tables and getattr(run, "pos_hash", None) is not None:
        nested_t = _t("pospool", "nested-youden")
        in_t = _t("pospool", "in-sample-youden")
        persist_hashpool(
            run.pos_hash,
            out_dir / "tables-pospool",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-pospool"
                if nested_t is not None
                else "in-sample-youden-pospool"
            ),
            fit_prefix=fit_n,
            score_kind="hashpool",
        )
    table["prefixes"] = []
    for plen in sorted(run.prefixes):
        for m in run.prefixes[plen]:
            table["prefixes"].append(
                {
                    "prefix_tokens": plen,
                    "name": m.name,
                    "n_prompt_wins": m.n_prompt_wins,
                    "n_prompts": m.n_prompts,
                    **m.holdout.ranking_payload(),
                    "binary": binary_eval_to_dict(m.binary),
                    "nested_stem": nested_stem_gates(m.holdout),
                    "used_keys": m.holdout.used_keys,
                }
            )
            persist_holdout(m.holdout, out_dir / f"prefix-{plen}" / m.name)
    table["window_scores"] = []
    for start, end in sorted(run.window_results):
        for m in run.window_results[(start, end)]:
            table["window_scores"].append(
                {
                    "start": start,
                    "end": end,
                    "name": m.name,
                    "n_prompt_wins": m.n_prompt_wins,
                    "n_prompts": m.n_prompts,
                    **m.holdout.ranking_payload(),
                    "binary": binary_eval_to_dict(m.binary),
                    "nested_stem": nested_stem_gates(m.holdout),
                    "used_keys": m.holdout.used_keys,
                }
            )
            persist_holdout(
                m.holdout, out_dir / _window_dir(start, end) / m.name
            )
    if persist_tables and getattr(run, "pivot_fits", None):
        from text_watermark_tools.pivot import persist_pivot

        for weight, fit in run.pivot_fits.items():
            nested_t = _t(f"pivot-lda{'' if weight == 'uniform' else '-' + ('intopk' if weight == 'in_topk' else weight)}", "nested-youden")
            in_t = _t(
                f"pivot-lda{'' if weight == 'uniform' else '-' + ('intopk' if weight == 'in_topk' else weight)}",
                "in-sample-youden",
            )
            persist_pivot(
                fit,
                out_dir / f"tables-pivot-{weight}",
                model_name=run.model_name,
                pair_dir=run.train_dir,
                n_train_prompts=run.n_train_prompts,
                weight=weight,
                prompt_context=bool(run.prompt_context),
                decision_threshold=nested_t if nested_t is not None else in_t,
                decision_source=(
                    f"nested-youden-pivot-{weight}"
                    if nested_t is not None
                    else f"in-sample-youden-pivot-{weight}"
                ),
            )
        canonical = run.pivot_fits.get("uniform") or next(iter(run.pivot_fits.values()))
        canonical_weight = (
            "uniform" if "uniform" in run.pivot_fits else next(iter(run.pivot_fits))
        )
        nested_t = _t("pivot-lda", "nested-youden")
        in_t = _t("pivot-lda", "in-sample-youden")
        persist_pivot(
            canonical,
            out_dir / "tables-pivot",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            weight=canonical_weight,
            prompt_context=bool(run.prompt_context),
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-pivot" if nested_t is not None else "in-sample-youden-pivot"
            ),
        )
    elif persist_tables and getattr(run, "pivot_fit", None) is not None:
        from text_watermark_tools.pivot import persist_pivot

        nested_t = _t("pivot-lda", "nested-youden")
        in_t = _t("pivot-lda", "in-sample-youden")
        weight = run.pivot_weights[0] if getattr(run, "pivot_weights", ()) else "uniform"
        persist_pivot(
            run.pivot_fit,
            out_dir / "tables-pivot",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            weight=weight,
            prompt_context=bool(run.prompt_context),
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-pivot" if nested_t is not None else "in-sample-youden-pivot"
            ),
        )
    if persist_tables and getattr(run, "rankpath_model", None) is not None:
        from text_watermark_tools.rankpath import persist_rankpath

        nested_t = _t("rankpath", "nested-youden")
        in_t = _t("rankpath", "in-sample-youden")
        persist_rankpath(
            run.rankpath_model,
            out_dir / "tables-rankpath",
            model_name=run.model_name,
            pair_dir=run.train_dir,
            n_train_prompts=run.n_train_prompts,
            prompt_context=bool(run.prompt_context),
            spec_name="rankpath",
            decision_threshold=nested_t if nested_t is not None else in_t,
            decision_source=(
                "nested-youden-rankpath"
                if nested_t is not None
                else "in-sample-youden-rankpath"
            ),
            fit_prefix=fit_n,
        )
    if run.cascade:
        (out_dir / "cascade.json").write_text(
            json.dumps(_cascade_json(run.cascade), indent=2) + "\n"
        )
    (out_dir / "results.json").write_text(json.dumps(table, indent=2) + "\n")
    (out_dir / "results.md").write_text(
        "# Key-free transfer\n\n" + print_transfer(run) + "\n"
    )
