# Experiments

This directory contains the runs behind the results in the root [README](../README.md).

The central sequence is:

```text
known public mark
      ↓
verify with official score
      ↓
generate matched marked/unmarked twins
      ↓
throw the keys away
      ↓
fit key-free token/context statistics
      ↓
evaluate held-out prompts
```

That progression produced the repository's key result: a **key-free indicator for watermark presence**, reaching **10/12** held-out prompts on the 12×4 GPT-2 corpus and **11/12** under the documented 0.02 comparison margin.

## Main runs

| Directory | Experiment | Result |
|---|---|---|
| `2026-08-15-gpt2-sonnet5/` | Known public mark before/after Sonnet edits | marked 0.617/0.638; proofread 0.605/0.625; rewrite 0.502/0.502 |
| `2026-08-15-known-mark-v2/` | Key-free rewrite surrogate, then official measurement | ~0.62 → ~0.50 |
| `claude-premark-2026-08/` | Control corpus collected before announced marking condition | 40 A/B texts plus auxiliary files |
| `2026-08-17-grok-prompts/` | Seed prompts | reference input |
| `2026-08-17-blind-pairs/` | 12 GPT-2 marked/unmarked prompt pairs | official detector: **12/12** |
| `2026-08-17-blind/` | First key-free leave-one-out run | **8/12** |
| `2026-08-17-blind-limit/` | Same seeds, longer generations | **6/12** |
| `2026-08-17-pair-qwen/` | Qwen2-1.5B matched twins | official **12/12** |
| `2026-08-17-blind-qwen-k2/` | Key-free Qwen, last-2 | **10/12** |
| `2026-08-17-pair-36/` | More topics | official 36/36; blind 22/36 |
| `2026-08-17-pair-12x4/` | 12 prompts × 4 GPT-2 samples | corpus for higher-context indicator |
| `2026-08-17-blind-12x4-k4/` | Key-free last-4 | **10/12** |
| `2026-08-17-indicate-holdout-12x4/` | Rotate, fit 11 prompts, score held-out files | prompt grain **10/12**, single marked file **29/48** |
| `2026-08-17-indicate-holdout-12x4-margin02/` | Same LRs, 0.02 comparison margin | prompt grain **11/12** |

## What changed across the runs

The early 8/12 result showed that token-level structure was present.

The later runs clarified what strengthens it:

- simply making generations longer did not help;
- simply adding more topics did not help much;
- **repeated draws from the same prompts did help**, because they create reusable higher-order contexts;
- the effect also appears with a different local generator (Qwen2-1.5B).

This is why the current result should be described as a working experimental indicator rather than merely a "promising idea".

## Reference score

```bash
source .venv/bin/activate
python -m text_watermark_tools score \
  experiments/2026-08-15-gpt2-sonnet5/t_high_temp.txt
```

## Generate twins

```bash
python -m text_watermark_tools pair \
  experiments/2026-08-17-grok-prompts \
  --out-dir experiments/2026-08-17-pair \
  --max-new-tokens 128
```

## Run the key-free indicator experiment

```bash
python -m text_watermark_tools indicate holdout \
  experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4
```

For interpretation and methodology, see [research/key-free-twins.md](../research/key-free-twins.md).

`results.md` files inside individual run directories are experiment artifacts. They should be treated as recorded output, not editorial documentation.
