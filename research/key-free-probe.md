# Stronger key-free probes (without reconstructing keys)

The 10/12 prompt-grain count-table result is real. The 29/48 isolated-file sign
was a weak test. On 2026-08-31 we re-read the same 12×4 GPT-2 twins with
scorers that still use **no keys, no `hash_iv`, no g-values**.

Raw tables: [../experiments/2026-08-31-probe-12x4/](../experiments/2026-08-31-probe-12x4/)
and [../experiments/2026-08-31-scrub-12x4/](../experiments/2026-08-31-scrub-12x4/).

## Statistics on the published hard last-4 LRs

Frozen file: `experiments/2026-08-17-indicate-holdout-12x4/holdout.json`.

| Grain | Statistic | Result |
|---|---|---|
| Prompt-mean ranking | 10/12 | binomial P(≥10) = 0.019 |
| Isolated `lr > 0` | 29/48 | binomial P(≥29) = 0.097 (not a 5% test) |
| Isolated ranking | AUC | **0.626** |
| Mean gap | permutation | p = 0.0075 |

So the original method already had a significant **ranking** gap. The headline
weakness was the threshold-0 sign, not “no signal”.

## What the new scorers do

The published `hard` last-4 LR falls straight to the unigram when a 4-gram is
new. Leave-one-prompt-out makes most content 4-grams unseen. Two hypotheses:

1. Shared function-word 4-grams across prompts carry the transferable mark
   (`hits` / `gated` / `shrinkage`).
2. Random feature-hashing of the last-4 context shares statistics the way a
   stealing attack would, without reconstructing SynthID’s secret hash
   (`hashpool`).
3. Tournament sampling only reweights top-k, so unmarked-LM rank/gap features
   should also separate (`pivot-*`), and snapping to the unmarked argmax
   should kill the official mean (`scrub`).

Hash pooling uses laboratory splitmix64 mixers. It is **not** `accumulate_hash`
and does not recover the SHA-256 IV.

## Results on the 12×4 corpus

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | perm p |
|---|---|---|---|---|---|
| unigram | **11/12** | 0.592 | 26/48 | 24/48 | 0.031 |
| hard (published last-4) | 10/12 | 0.626 | 29/48 | 23/48 | 0.0075 |
| backoff | 7/12 | 0.521 | 29/48 | 21/48 | 0.28 |
| interpolate (Witten–Bell) | 7/12 | 0.524 | 24/48 | 24/48 | 0.36 |
| **hits** (shared 4-grams) | **11/12** | **0.737** | 28/48 | 30/48 | 0.00050 |
| gated (count ≥ 2) | 10/12 | 0.717 | 27/48 | 31/48 | 0.00050 |
| shrinkage | **11/12** | 0.734 | 28/48 | 30/48 | 0.00050 |
| mix last-1+4 | 6/12 | 0.520 | 25/48 | 21/48 | 0.33 |
| **hashpool** | **11/12** | 0.716 | **35/48** | 29/48 | 0.00050 |
| pivot-lda | 10/12 | 0.599 | 17/48 | 31/48 | 0.016 |
| pivot-rank | 8/12 | 0.609 | 26/48 | 27/48 | 0.045 |

Prompt-level misses:

- hard: *station*, *office* (same as the original write-up)
- unigram: *office*
- hits / shrinkage: *night-bus*
- hashpool: *letter*

`hits` and `hashpool` fail different prompts. That is recorded; it is not a
claimed 12/12 ensemble.

## Results on 36 GPT-2 topics (one draw)

Corpus: `experiments/2026-08-17-pair-36`. The original last-1 blind was **22/36**. Hard last-4 is **20/36**, AUC 0.549.

| Method | Prompt wins | File AUC | Marked `> 0` |
|---|---|---|---|
| hard | 20/36 | 0.549 | 20/36 |
| interpolate | 29/36 | 0.796 | 26/36 |
| **hits** | **30/36** | **0.886** | 33/36 |
| gated / shrinkage | **31/36** | 0.86–0.88 | 32–33/36 |
| **hashpool** | **31/36** | 0.877 | 32/36 |

The earlier lesson that “more topics alone do not help” was a **scorer artifact**. Extra topics help once unseen 4-grams are not dumped into the unigram. `hits` at threshold 0 is too sensitive here (unmarked ≤0 only 16/36); Youden t ≈ 0.39 gives sens 0.83 / spec 0.89.

JSON: [../experiments/2026-08-31-probe-36/](../experiments/2026-08-31-probe-36/).

## Results on Qwen2-1.5B (12×1)

Published last-2 on this corpus was **10/12**. Hard last-4 is **6/12**. Hashpool is **10/12**, AUC **0.750**, isolated **11/12** marked `lr > 0`. Exact `hits` prompt-wins 8/12 but file AUC **0.417** (below chance): one draw and a large tokenizer leave almost no shared 4-grams.

JSON: [../experiments/2026-08-31-probe-qwen/](../experiments/2026-08-31-probe-qwen/).

## Cross-corpus transfer (new prompt families)

Leave-one-of-12-out still shares the 12-prompt topic pool. The harder isolated-file
question is: train on **other** prompt families, score the 12×4 files (and the
reverse). Shared stems are dropped. Tables: [../experiments/2026-08-31-transfer-36-to-12x4/](../experiments/2026-08-31-transfer-36-to-12x4/)
and [../experiments/2026-08-31-transfer-12x4-to-36/](../experiments/2026-08-31-transfer-12x4-to-36/).

Train 24 new 36-topic stems, test all 12×4 files:

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hard | 10/12 | 0.640 | 32/48 | 27/48 |
| **hits** | 8/12 | **0.769** | **39/48** | 28/48 |
| **hashpool** | **11/12** | 0.766 | 34/48 | 30/48 |
| hybrid | 10/12 | 0.757 | 34/48 | 31/48 |

Train 12×4, test stems 13–36 (24 new topics):

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hard | 14/24 | 0.606 | 16/24 | 12/24 |
| **hits** | **24/24** | **0.986** | **24/24** | 14/24 |
| **hashpool** | **23/24** | 0.924 | 21/24 | 20/24 |
| **hybrid** | **23/24** | **0.946** | 22/24 | 20/24 |

Hits on new topics is an almost-perfect *ranking* of marked vs unmarked files
(AUC 0.986) and every marked file is positive at 0. It is not a calibrated
yes/no: ten unmarked twins are also positive. Hashpool/hybrid keep higher
specificity at threshold 0.

A leave-one-prompt LDA **stack** of hits+hashpool on the original 12×4 LOO
scores is **11/12**, AUC 0.732, isolated 23/48 with unmarked ≤0 **44/48**.
It trades recall for specificity. Complementary probe misses are not a 12/12
ensemble.

`indicate fit --method hashpool` writes frozen buckets. `indicate score`
reads them. The 36→12×4 hashpool tables live at
`experiments/2026-08-31-transfer-36-to-12x4/tables-hashpool/`.

## How to read this

**Coverage gating was the missing ablation on 12×4 and 36-topic GPT-2.** Scoring *only* 4-grams seen on both training sides raises 12×4 AUC from 0.626 to 0.737 (11/12) and 36-topic ranking from 20/36 to 30–31/36 (AUC 0.89). The unigram fallback in `hard` was adding topic noise. The old “more topics do not help” lesson was a scorer artifact.

**The 29/48 isolated sign was partly a protocol artifact.** Training on 24 *other* topics and scoring the 12×4 files, hits marks **39/48** (AUC 0.769). Training on 12×4 and scoring 24 new topics, hits ranks **24/24** (AUC **0.986**). Leave-one-of-12-out hard last-4 remains 29/48.

**Hash pooling is the method that generalizes across generators.** Isolated 35/48 on 12×4 GPT-2 (p ≈ 0.001), 32/36 on 36 topics, 11/12 on Qwen 12×1 (AUC 0.750), and 11/12 prompt grain when those hash buckets are trained on other GPT-2 topics. Exact `hits` fails on Qwen 12×1 (AUC 0.417) because the 4-grams do not overlap.

**Shorter-context interpolation is corpus-dependent.** On 12×4 it hurt (7/12). On 36 topics it helped (29/36). Do not treat Witten–Bell as a default win.

**Choice geometry is real but weaker.** Unmarked-LM rank/LDA separates above chance on 12×4 (perm p 0.016–0.045) and stays key-free. It does not beat `hits` or `hashpool` there.

**A hits+hashpool LDA stack is a specificity knob, not a 12/12 detector.** On 12×4 LOO it keeps 11/12 and AUC 0.732 while unmarked ≤0 rises to 44/48.

**Argmax snap removes the public mark without keys.** On all 48 marked 12×4 files, official mean **0.6216 → 0.4994**. An unmarked control stays near 0.50 (0.508 → 0.487). About 60–90 of 128 tokens flip, so this is a statistical scrub, not a fluent rewrite. It needs the unmarked generator, not the keys.

## What this is not

- Not key recovery and not an inverse of SHA-256.
- Not a Claude detector.
- Not a claim that every isolated paragraph is classifiable.
- Not a quality-preserving remover. For fluent rewrite see `iterate`.

## Commands

```bash
python -m text_watermark_tools indicate holdout \
  experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4 --score-mode hits

python -m text_watermark_tools probe \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/2026-08-31-probe-12x4

python -m text_watermark_tools probe experiments/2026-08-17-pair-36 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --overlap drop-from-train \
  --out-dir experiments/2026-08-31-transfer-36-to-12x4

python -m text_watermark_tools indicate fit experiments/2026-08-17-pair-12x4 \
  --method hashpool --out-dir experiments/indicator-gpt2-hashpool

python -m text_watermark_tools indicate score FILE.txt \
  --tables experiments/2026-08-31-transfer-36-to-12x4/tables-hashpool

python -m text_watermark_tools scrub \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/2026-08-31-scrub-12x4
```
