# Stronger key-free probes (without reconstructing keys)

The 10/12 prompt-grain result is real. The 29/48 isolated-file sign is weak.
This note records the next attack surface: **better ways to read the same
paired evidence**, plus a key-free scrub, without touching keys, `hash_iv`,
or g-values.

Official `score` is used only as a reference check after a scrub.

## Why the baseline stalls on one file

`indicate` fits last-4 next-token tables and scores a held-out string with
mean log P_marked − log P_unmarked. With `--backoff` off (the published
run), an unseen 4-gram falls **straight to the unigram**. Leave-one-prompt-out
makes most content 4-grams unseen. So the isolated-file LR is a noisy mix of:

- rare exact 4-gram hits that happen to overlap across prompts;
- unigram fallback that can be topic, not watermark.

That is why repeated draws of the *same* prompt help the 10/12 ranking
(more chance of shared function-word 4-grams) while one file’s sign at 0
does not clear a binomial 5% bar. See the frozen
`experiments/2026-08-17-indicate-holdout-12x4/holdout.json`:

| Grain | Statistic | Result |
|---|---|---|
| Prompt-mean ranking | 10/12 | binomial P(≥10) ≈ 0.019 |
| Isolated `lr > 0` | 29/48 | binomial P(≥29) ≈ 0.16 (not a 5% test) |
| Isolated ranking | AUC of the same 48+48 LRs | computed in `probe` / `indicate holdout` |

The scientific job is therefore not “quote a higher 29/48”. It is to
**raise transferable signal** and **report ranking tests**, not only a
threshold of 0.

## Methods (all key-free)

| Method | Idea |
|---|---|
| `unigram` | Token identity only. Lower bound on transfer. |
| `hard` | Published last-k table, unigram fallback. |
| `backoff` | Shrink the context instead of jumping to the unigram. |
| `interpolate` | Witten–Bell mix of every stored order. |
| `hits` | Score only exact contexts seen at least once on **both** sides. |
| `gated` | Same, with a count ≥ 2. If this collapses, the 4-gram table is not transferring. |
| `shrinkage` | Credibility-weight each token LR by n/(n+τ). |
| `mix` | Average last-1 and last-k LRs. |
| `hashpool` | Feature-hash the last-k context into shared buckets (stealing-style regulariser; **not** the secret SynthID hash). |
| `pivot-rank` | Mean rank of the chosen token inside the unmarked LM’s top-k. Tournament sampling only reweights top-k. |
| `pivot-lda` | Fisher LDA on six choice-geometry features from the unmarked LM. |
| `scrub` | Snap each token to the unmarked top-k argmax of the *original* prefix; then official-score the result as a reference. |

None of these invert the SHA-256 IV. Hash pooling is explicit about that:
random 64-bit mixers with laboratory seeds, not `accumulate_hash`.

`hits` / `gated` are the ablation that answers whether last-4 is actually
using reused 4-grams or mostly unigram fallback. That is the interesting
negative-or-positive result.

Choice geometry is the original detection idea: a finished string is scored
from **how** the unmarked model would have ranked the observed tokens, not
from sparse 4-gram identity. It needs the public GPT-2 weights, not the
watermark keys.

## Commands

```bash
python -m text_watermark_tools indicate holdout \
  experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4 --score-mode interpolate

python -m text_watermark_tools probe \
  experiments/2026-08-17-pair-12x4 \
  --pivot \
  --out-dir experiments/2026-08-31-probe-12x4

python -m text_watermark_tools scrub \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/2026-08-31-scrub-12x4
```

`indicate holdout` now prints `auc` and a permutation p-value on the same
LRs it always computed.

## What would count as a better crack

Keep the 10/12 claim as-is unless a method beats it **on this corpus**
without keys.

A real single-file improvement is:

- higher AUC than the published count LR, with permutation p still small;
- and/or a threshold-0 sign that finally beats a binomial 5% bar
  without wrecking specificity.

A real removal is:

- official mean on snapped **marked** files falling toward 0.50;
- snap itself still `used_keys=False`.

If a method is worse, say so. Negative ablations (especially `gated`) are
part of the result.

Headline numbers from a dated `probe` / `scrub` run belong in
[key-free-twins.md](key-free-twins.md) and the root README only after the
JSON is checked in.
