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

### How to read this

**Coverage gating was the missing ablation.** Scoring *only* 4-grams seen on
both the marked and unmarked training sides raises AUC from 0.626 to 0.737
and prompt-grain wins from 10/12 to 11/12. The unigram fallback in `hard` was
adding topic noise. Shared 4-grams *do* transfer across held-out prompts.

**Hash pooling is the first isolated-file sign that clears 5%.** 35/48 marked
files have `lr > 0` (binomial p ≈ 0.001). Unmarked specificity is still 29/48.
This is a better indicator, not a verdict machine.

**Shorter-context interpolation hurt.** Backoff, Witten–Bell, and mixing last-1
with last-4 all fall to chance-like AUCs. The watermark footprint that
transfers is the *exact* (or hashed) 4-gram, matching SynthID’s H = 4, not a
smoothed language model.

**Choice geometry is real but weaker.** Unmarked-LM rank/LDA separates above
chance (perm p 0.016–0.045) and stays key-free. It does not beat `hits` or
`hashpool` on this corpus.

**Argmax snap removes the public mark without keys.** On all 48 marked 12×4
files, official mean **0.6216 → 0.4994**. An unmarked control stays near 0.50
(0.508 → 0.487). About 60–90 of 128 tokens flip, so this is a statistical
scrub, not a fluent rewrite. It needs the unmarked generator, not the keys.

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

python -m text_watermark_tools scrub \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/2026-08-31-scrub-12x4
```
