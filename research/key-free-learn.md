# Key-free learned scorers (not a universal detector)

Count tables are already a learned model: Laplace-smoothed next-token
likelihoods on last-k contexts. `logit` is already a learned combiner of
those file scores. This note asks a different question:

> If we replace the n-gram likelihood with a tiny neural net (or a hashed
> logistic on the same n-grams), do we get a better **key-free** indicator
> on the grains this lab already reports?

The theory this rests on is not original to this repository.

- **DeepMind SynthID-Text** (tournament sampling) is the watermark. The
  official detector needs keys. See [how-synthid-works.md](how-synthid-works.md).
- **Stealing-style readers** estimate a generator's context-dependent
  token preference from many samples, without reconstructing the secret
  hash or SHA-256 IV. Hash pooling in this lab is already that idea with
  a laboratory splitmix64 mixer. See [invertibility.md](invertibility.md).
- **This lab's contribution** is the matched-twin protocol on the public
  mixin, the grains (prompt ranking vs isolated file vs nested threshold),
  and the measurement of whether extra flexibility helps.

A neural net trained here is still key-free (`used_keys` / `used_hash_iv` /
`used_g_values` stay false). It is **not** `score`. It is **not** a Claude
classifier. Do not train it on the pre-mark corpus alone.

## Architectures

All three read the same clipped token prefix as the matched 4-token
count-table gate (`--fit-prefix 4`). They skip generated token 0 unless
`--include-first`, matching the published last-k tables.

| Name | What it learns | What it is not |
|---|---|---|
| `hashlog` | Ridge logistic on a hashing-trick bag of last-k n-grams (laboratory splitmix64) | Not SynthID's `accumulate_hash` |
| `tokmlp` | Tiny MLP on hashed token embeddings, mean-pooled | Not a language model and not g-values |
| `charcnn` | Tiny CNN on UTF-8 bytes of the decoded prefix | Not a tokenizer-matched 4-gram table |

`hashlog` is the tight comparison: same n-gram features as hashpool, a
learned scoring function instead of two Laplace tables and an LR.
`tokmlp` asks whether token composition beats independent n-grams.
`charcnn` asks whether a tokenizer-free net transfers when GPT-2 4-gram
tables do not (DistilGPT2, Qwen).

## Protocol

Same splits as the count-table work:

```bash
python -m text_watermark_tools learn experiments/2026-08-31-pair-36x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-learn-36x4-fitprefix4

python -m text_watermark_tools learn experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-learn-36x4-to-12x4-fitprefix4

python -m text_watermark_tools learn experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-31-pair-distilgpt2-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-learn-36x4-to-distil-fitprefix4

python -m text_watermark_tools learn experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-31-pair-qwen-12x4 \
  --test-model Qwen/Qwen2-1.5B-Instruct \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-learn-36x4-to-qwen-fitprefix4
```

Quote **t=0** and **nested Youden** (train-only) separately. Nested-by-stem
on already-held-out LRs is a different gate. A 50% train-label shuffle
must collapse isolated sign toward chance.

## What would count as a result

- **Better isolated-file GPT-2 indication** than matched 4-token poshits
  (**12/12**, AUC **0.873**, t=0 **39/48 vs 41/48**) on the same 24×4 → 12×4
  split, without peeking at the test Youden.
- **Transfer** to DistilGPT2 or Qwen above chance, after count tables
  failed (hits **5/12** Distil, **6/12** Qwen). That would be news.
- **A net that matches the tables and still fails to transfer** is also a
  result: extra flexibility was not the bottleneck; the footprint is
  generator-weight specific.

Do not replace the published headlines **10/12**, **29/48**, or **36/36**.
Do not call any of these a universal detector.
