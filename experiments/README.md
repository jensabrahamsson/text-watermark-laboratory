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
| `claude-mark-2026-08-19/` | Same prompts on claude.ai after a rumored live mark | **37/40**; usage limit; `assumed_watermark=rumored` |
| `2026-08-19-claude-rumor-twins/` | Premark vs 19a, 37 prompts | last-1 **28/37**; last-4 **24/37** |
| `claude-sample-2026-08-19b/` | Same-day second pass | **40/40** |
| `2026-08-19-claude-sameday-twins/` | 19a vs 19b | last-1 **19/38**; last-4 **19/38** |
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
| `2026-08-31-probe-12x4/` | Key-free scorer comparison on the same 12×4 twins | `hits` **11/12** AUC **0.737**; hashpool **11/12** isolated **35/48** |
| `2026-08-31-probe-36/` | Same scorers on 36 GPT-2 topics × 1 | hashpool **31/36** AUC **0.877**; hard last-4 **20/36** |
| `2026-08-31-probe-qwen/` | Qwen2-1.5B 12×1, Qwen tokenizer | hashpool **10/12** AUC **0.750**; hits AUC **0.417** |
| `2026-08-31-scrub-12x4/` | Key-free argmax snap, official `score` as reference | **0.622 → 0.499** on 48 marked files |
| `2026-08-31-transfer-36-to-12x4/` | Train 24 new topics, score 12×4 files | hits isolated **39/48** AUC **0.769**; hashpool **11/12** |
| `2026-08-31-transfer-12x4-to-36/` | Train 12×4, score stems 13–36 | hits **24/24** AUC **0.986**; hashpool **23/24** |
| `2026-08-31-stack-12x4/` | LOO LDA of hits+hashpool file scores | **11/12**, AUC 0.732, unmarked ≤0 **44/48** |

## What changed across the runs

The early 8/12 result showed that token-level structure was present.

The later runs clarified what strengthens it:

- simply making generations longer did not help the hard scorer;
- simply adding more topics did not help the **hard** last-1/last-4 scorer (22/36, 20/36);
- **repeated draws from the same prompts did help** that scorer, because they create reusable higher-order contexts;
- coverage-gated and hash-pool readers later showed that extra topics *do* help once unseen 4-grams are not scored as unigrams (30–31/36);
- the effect also appears with a different local generator (Qwen2-1.5B), where hashpool matches the published **10/12**.
- training on **other** prompt families is a fairer isolated-file test than leave-one-of-12-out: hits then marks **39/48** of the 12×4 files, and ranks **24/24** new 36-topic stems (specificity at 0 is still incomplete).

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
