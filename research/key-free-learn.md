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

## Results (2026-08-31)

All runs below are `--fit-prefix 4 --pos-bucket 1`, skip generated token 0
unless noted, seed `20260831`, 40 Adam epochs. Nested Youden is train-only.
JSON under `experiments/2026-08-31-learn-*`.

**This lab did not get a better isolated-file GPT-2 reader, and did not
get a cross-generator detector.** Laplace last-k count tables remain the
strongest key-free scorer on the published gate. A neural net is still a
possible tool with more data or another architecture. This experiment
does not license claiming we have one.

### New-topic GPT-2 gate (24×4 → 12×4)

Count-table baseline on the same split: poshits **12/12**, AUC **0.873**,
t=0 **39/48 vs 41/48**.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` | Nested Youden |
|---|---|---|---|---|---|
| poshits (count table) | **12/12** | **0.873** | **39/48** | **41/48** | 39/48 vs 41/48 |
| tokmlp | 8/12 | 0.714 | 28/48 | 38/48 | 30/48 vs 37/48 |
| hashlog | 7/12 | 0.606 | 14/48 | 47/48 | 15/48 vs 45/48 |
| charcnn | 7/12 | 0.557 | 16/48 | 41/48 | 16/48 vs 41/48 |

tokmlp has a real ranking gap (perm p ≈ 0.0005). It does not beat the
count table. `--include-first` on this split does not rescue them
(tokmlp 8/12, AUC 0.647).

### In-domain GPT-2 (36×4 leave-one-out)

poshits on this grain: **34/36**, AUC **0.935**, t=0 **131/144 vs 132/144**.

| Method | Prompt wins | File AUC | t=0 marked / unmarked |
|---|---|---|---|
| hashlog | 34/36 | 0.864 | 113/144 vs 129/144 |
| charcnn | 34/36 | 0.834 | 97/144 vs 130/144 |
| tokmlp | 32/36 | 0.835 | 89/144 vs 118/144 |

Prompt grain can match. Isolated-file AUC does not.

### Leave-one-of-12-out (in-family, not the OOD gate)

poshits 4-token: **9/12**, AUC 0.673, t=0 **23/48 vs 48/48**.
hashlog: **11/12**, AUC 0.894, t=0 **35/48 vs 45/48**.

That 11/12 is **not** a replacement of the published 10/12, and it is
**not** a better isolated-file detector. The same hashlog reader is 7/12
on new topics. It overfits the 12-prompt family. Quote the OOD gate.

### Shuffle control (50% train-stem label flips, same 24×4 → 12×4)

| Method | Prompt wins | File AUC | Marked `> 0` |
|---|---|---|---|
| tokmlp | 5/12 | 0.471 | 6/48 |
| hashlog | 10/12 | 0.678 | 44/48 |
| charcnn | 10/12 | 0.745 | 27/48 |

tokmlp collapsed. hashlog and charcnn did not. Count-table shuffle on
this lab previously dropped isolated sign to 19–20/48. Do not treat
hashlog/charcnn OOD rankings as watermark detection; they can latch onto
sparse artifacts that survive 50% stem flips.

### Cross-generator

| Split | hashlog | tokmlp | charcnn |
|---|---|---|---|
| GPT-2 36×4 → DistilGPT2 12×4 | 7/12, AUC 0.535 | 8/12, AUC 0.559 | 2/12, AUC 0.421 |
| GPT-2 36×4 → Qwen 12×4 | 7/12, AUC 0.456 | 5/12, AUC 0.500 | 6/12, AUC 0.496 |

The character CNN was the tokenizer-free transfer hypothesis. It failed.
Distil in-domain 4-token charcnn is 9/12, AUC 0.710 (hits on Distil last-4
was 9/12, AUC 0.705) — a generator can have its own opening reader; GPT-2
tables and GPT-2 nets do not become that reader.

### Qwen in-domain, token 0

Qwen's count-table opening signal **is token 0** (`first` **12/12**, AUC
**0.901**). Learned scorers that skip token 0 (the GPT-2 default) are
weak (tokmlp 6/12, charcnn 7/12). With `--include-first`, hashlog ranks
**12/12**, AUC 0.826, isolated 25/48 — still below the first-token count
table, and still not a single-file detector.

## What this proves and what it does not

Proves, on this public mixin and these twins:

1. Extra flexibility (MLP / CNN / hashed logistic) is not the bottleneck
   on the GPT-2 isolated-file gate. Shared-context Laplace LRs were
   already the better inductive bias.
2. A tokenizer-free character net trained on GPT-2 openings does not
   transfer to DistilGPT2 or Qwen. That matches the count-table transfer
   failures. The footprint is generator-weight specific.
3. In-family 12-prompt LOO can flatter a hashed logistic (11/12) that
   then fails the new-topic gate (7/12). Extra topics are required for
   an honest isolated-file claim.

Does not prove: that no neural net can ever beat these tables; that the
lab has a universal detector; that Claude is marked.

Do not replace the recounted headlines **9/12**, **25/48**, or **36/36**.
Do not call any of these a universal detector.

The next original question after this negative net result is instance
contrast: [key-free-contrast.md](key-free-contrast.md).

