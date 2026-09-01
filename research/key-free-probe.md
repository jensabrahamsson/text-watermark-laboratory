# Stronger key-free probes (without reconstructing keys)

The published 10/12 / 29/48 last-4 count-table result overcounted truncated
openings. After storing each real suffix once, hard last-4 is **9/12** /
**25/48** (`experiments/2026-09-01-probe-12x4-recount-hard-last4/`). Isolated
sign at 0 remains a weak test. On 2026-08-31 we re-read the same 12×4 GPT-2
twins with scorers that still use **no keys, no `hash_iv`, no g-values**.

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

## Truncated-context recount (2026-09-01)

`_add_sequence` used to store every order `1..k` even when fewer tokens
existed, so `fit_table([[10,20]], context_len=4)` counted `(10,)→20` four
times. After storing each real suffix once:

| Grain | Statistic | Result |
|---|---|---|
| Prompt-mean ranking | 9/12 | binomial P(≥9) = 0.073 (not a 5% test) |
| Isolated `lr > 0` | 25/48 | binomial P(≥25) = 0.443 (not a 5% test) |
| Isolated ranking | AUC | **0.590** |
| Mean gap | permutation | p = 0.040 |

Prompt ranking survives (**9/12**, or **10/12** with margin 0.02). Isolated
sign at 0 is chance-like. Rechecked `hits` is **10/12**, AUC **0.718**.
In-domain 36×4 hits is still **36/36**, AUC **0.930**. JSON:
`experiments/2026-09-01-blind-12x4-recount-last4/`,
`experiments/2026-09-01-probe-12x4-recount-hard-last4/`,
`experiments/2026-09-01-probe-12x4-recount-hits/`,
`experiments/2026-09-01-probe-36x4-recount-hits/`. The 2026-08-17 holdout
files stay as collected. `probe` / `indicate holdout` / `blind` now report
`ranking_without_isolated_tp`: prompt-group wins whose marked files are
all `lr<=0`. Those stems are not isolated-file true positives. Historical
`blind` JSON stays stem-mean only.

## What the new scorers do

The published `hard` last-4 LR falls straight to the unigram when a 4-gram is
new. Leave-one-prompt-out makes most content 4-grams unseen. Two hypotheses:

1. Shared function-word 4-grams across prompts carry the transferable mark
   (`hits` / `gated` / `shrinkage`).
2. Random feature-hashing of the last-4 context shares statistics across
   prompts (`hashpool`). That mixer is a laboratory splitmix of token ids,
   not SynthID’s secret hash, and it is not the stealing attack of
   Jovanović et al. (2024).
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
| opening pivot-lda (`--fit-prefix 4`, no prompt) | **10/12** | **0.672** | **27/48** | 37/48 | 0.0010 |
| opening pivot-rank | **10/12** | **0.674** | **31/48** | 30/48 | 0.0015 |

The unpublished full-file pivot averaged 128 tokens. The mark in
unmarked-LM geometry is front-loaded: a 4-token generated-only opening
beats that 17/48 isolated sign. Prompt-conditioned opening LDA is
worse than chance under leave-one-prompt-out (7/12, AUC 0.468). It
does not transfer as a calibrated OOD isolated-file reader. See
[key-free-cascade.md](key-free-cascade.md).

Prompt-level misses:

- hard: *station*, *office* (same as the original write-up)
- unigram: *office*
- hits / shrinkage: *night-bus*
- hashpool: *letter*

`hits` and `hashpool` fail different prompts. That is recorded; it is not a
claimed 12/12 ensemble. `hashtok` is occupancy-free hashpool (tokhits on
collisions). On 60-stem prefix-5 it copies postokhits' 30 true positives;
hashpool's extra four, including letter d2's official 5-gram, are Laplace.
`hashtokbackoff` fits per-order hash tables; prefix-5 nested Youden stays
**30/48**, and letter d2's fifth token is last-1 unmarked. Those tables
also hash short prefixes into longer-order mixers. `hashtoklenbackoff`
requires exact last-k; nested Youden **33/48**. Prefix-4 hashed
backoff hurts versus hashtok. `hashskip` (tagged drop-one last-k)
is denser at t=0 (**25/48**) and nested Youden **16/48**; letter d2's
official `I` is seen unmarked-only. `hashtoklen2` skips singleton
collisions: **10/48 vs 48/48**, precision 1.0; 11 of 21 hashtoklen TPs
were singletons; harbour d2 survives. Count-weighting those hashes
keeps 21/48 (no singleton+dense mix). `hashtoklen2` + prefix-4 rankpath cascade
is **28/48 vs 40/48** (same as standalone rankpath). `hashmask`
(length-k MASK replace) is **21/48 vs 42/48** at t=0 and nested
Youden **19/48 vs 45/48**, worse than hashtoklen; letter d2's official
slot is two opposing singletons (lr=+0.240), thrown out nested.
In-domain full-file `hashtok` is **33/48 vs 22/48**, nested-by-stem
**22/48 vs 30/48** (hashpool stays **35/48 vs 29/48**). `--n-hashes 2`
on that mixer is **34/48 vs 31/48**, nested **28/48 vs 37/48**, AUC
**0.764**; `--n-hashes 4` is **36/48 vs 30/48**, nested **35/48 vs
30/48**; `--n-hashes 16` copies 36/48 with nested spec **24/48**;
`--n-hashes 32` hurts (**30/48**, nested **21/48 vs 38/48**). Default
n=8 is not the best in-domain width **at seed 20260831**; that n=2 win
is seed-confounded (n=2 spec **21–31/48**). 24→12 nested Youden prefers
n=8 (**17/48 vs 46/48**) at seed 20260831; that win is also
seed-confounded (n=2 seed 7 nested **19/48 vs 47/48**). Occupancy-free
last-k at that frozen mixer: in-domain last-1 is chance (**5/12**);
last-3 prompt **11/12** has t=0 **24/48** (below recounted hard **25/48**). 24→12
last-4 still wins prompt ranking and nested FPR10 (**17/48 vs 46/48**);
last-2 file AUC **0.738** is ranking (nested **15/48**); last-1 nested
**18/48** has prompt **7/12**. Keep `--context-len 4`. Do not fish a
seed. Do not sell 36/48, 31/48, 24/48, or 18/48. OR with hard
last-4 indicate is **39/48 vs 12/48**, combined **51/96** (worse than
indicate **52/96**); nested LDA **21/48 vs 37/48**. Complementary TPs
exist; the unmarked OR cost destroys the combined gate. Do not sell
33/48 or 39/48 as replacing **25/48**. `tokhybrid` (tokhits, then
hashtok) copies that isolated 33/48 and lifts prompt ranking to 11/12;
`poshashtok` nested **14/48 vs 38/48** is a specificity knob.
`hashtokgap` (hashtok only where tokhits abstains) is **27/48 vs 21/48**,
nested **17/48 vs 31/48**, a strict subset of hashtok's 33 TPs.
`hashtok2` (unbucketed min_count=2) is **34/48 vs 21/48**, nested
**19/48 vs 35/48**: a sign reshuffle, not a singleton core.
In-domain `--fit-prefix 4` occupancy-free hashing copies tokhits
density, not opening rankpath **41/48**: tokhits **23/48 vs 48/48**
(prompt **12/12**); hashtok **24/48 vs 47/48** (nested **23/48 vs
47/48**, extra TP letter d3 only); hashtok2 **22/48 vs 48/48**. Letter
d2 is zero at that grain. Marked isolated recall **24/48** is below
hard last-4 **25/48**. Do not sell 24/48 as replacing **25/48**.
See [key-free-hashtok.md](key-free-hashtok.md).

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

## Results on 36 GPT-2 topics × 4 draws (128 tokens)

Corpus: [../experiments/2026-08-31-pair-36x4/](../experiments/2026-08-31-pair-36x4/).
Official first-draw lamp **36/36**. Length-matched to 12×4, not the historical
256-token 36×1 run. Leave-one-out JSON:
[../experiments/2026-08-31-probe-36x4/](../experiments/2026-08-31-probe-36x4/).

| Method | Prompt wins | File AUC | Marked `> 0` | Nested-by-stem Youden |
|---|---|---|---|---|
| **hits** | **36/36** | **0.934** | 134/144 | **119/144 vs 134/144** |
| hitmass | **36/36** | **0.938** | 134/144 | 116/144 vs 134/144 |
| hashpool | **36/36** | 0.909 | 128/144 | 111/144 vs 128/144 |

**36/36 is in-domain ranking**, same generator. Nested-by-stem Youden chooses
the threshold on other prompts' already-held-out LRs. It is the honest
in-domain isolated-file gate here; it is not a detector of a new model.

Draw-count ablation (`--max-draws` on the same files):

| Draws | hits wins | hits AUC | Nested-by-stem hits |
|---|---|---|---|
| 1 | 30/36 | 0.845 | 29/36 vs 31/36 |
| 2 | 33/36 | 0.875 | 52/72 vs 64/72 |
| 4 | **36/36** | **0.934** | **119/144 vs 134/144** |

One 128-token draw reproduces the old 36×1 hits ranking (30/36). Extra
*draws* lift it to 36/36. Hashpool on the short 1-draw slice is only 23/36
(the 256-token 36×1 hashpool was 31/36).

Train those 24 new stems × 4 draws, score the original 12×4 files
([../experiments/2026-08-31-transfer-36x4-to-12x4/](../experiments/2026-08-31-transfer-36x4-to-12x4/)):
hits **12/12**, AUC **0.793**, isolated **42/48** at t=0. Nested hits Youden
is conservative: **26/48** vs **44/48**. Reverse — train 12×4, score 96
new-topic 36×4 files
([../experiments/2026-08-31-transfer-12x4-to-36x4/](../experiments/2026-08-31-transfer-12x4-to-36x4/)):
hits **24/24**, AUC 0.924; nested hits 10% FPR **83/96** vs **85/96**.

## Prefix length and mixin `ngram_len=5`

Prefixes are cumulative token clips (`--prefix-lens`). They ask how early
the key-free footprint is visible. They are not disjoint windows.

In-domain 36×4
([../experiments/2026-08-31-probe-36x4-prefixes/](../experiments/2026-08-31-probe-36x4-prefixes/)):

| Prefix tokens | hits wins | Isolated `lr>0` | AUC | Nested-by-stem Youden |
|---|---|---|---|---|
| 16 | **34/36** | 129/144 | **0.916** | 118/144 vs 127/144 |
| 64 | **36/36** | 130/144 | 0.919 | 125/144 vs 130/144 |
| 128 | **36/36** | 134/144 | **0.934** | 119/144 vs 134/144 |

The 128-token prefix matches the published full-file 36×4 result. Sixteen
tokens already rank almost every prompt. Isolated overlap at `t = 0`
remains. `--fit-prefix 16` is a different protocol: it trains on those
16 tokens instead of scoring a prefix of a full-file table. See below.

New-topic 24×4 → 12×4
([../experiments/2026-08-31-transfer-36x4-to-12x4-prefixes/](../experiments/2026-08-31-transfer-36x4-to-12x4-prefixes/)):
16-token hits **11/12**, AUC **0.752**, isolated 40/48; nested-by-stem
**25/48** vs **29/48**. Full length recovers 12/12 / 0.793 / 42/48. Ranking
appears early; the nested isolated-file gate on short prefixes stays weak.

`--context-len 5` on the same 36×4 twins
([../experiments/2026-08-31-probe-36x4-k5/](../experiments/2026-08-31-probe-36x4-k5/))
matches the mixin's `ngram_len=5` and does **not** beat last-4: hits
**35/36**, AUC **0.912** versus last-4 **36/36** / **0.934**. Keep
`context_len=4`.

## Disjoint windows (not prefixes)

`--windows 0:16,16:32,32:64,64:128` scores each slice without earlier
tokens. Window `0:16` matches the 16-token prefix.

In-domain 36×4 hits
([../experiments/2026-08-31-probe-36x4-windows/](../experiments/2026-08-31-probe-36x4-windows/)):

| Window | wins | Isolated `lr>0` | AUC |
|---|---|---|---|
| 0:16 | **34/36** | 129/144 | **0.916** |
| 16:32 | 22/36 | 74/144 | 0.549 |
| 32:64 | 28/36 | 92/144 | 0.651 |
| 64:128 | 29/36 | 108/144 | 0.723 |

The keyed mixin marks every position. The key-free 4-gram reader does not:
tokens 16–32 are near chance. The tail still ranks above chance but does
not match the opening. New-topic transfer
([../experiments/2026-08-31-transfer-36x4-to-12x4-windows/](../experiments/2026-08-31-transfer-36x4-to-12x4-windows/))
is sharper: 0:16 hits **11/12** AUC **0.752**; 16:32 is chance (8/12,
AUC 0.512).

GPT-2 36×4 → new Qwen 12×4, overlapping stems dropped
([../experiments/2026-08-31-transfer-36x4-to-qwen-12x4/](../experiments/2026-08-31-transfer-36x4-to-qwen-12x4/)):
hits **6/12** AUC 0.445, hashpool **3/12**, surface **6/12**. Chance.
Same-topic GPT-2 surface → that Qwen sample: **7/12**, AUC 0.525,
isolated 5/48. Extra GPT-2 draws and a byte table do not create a Qwen
detector. Do not overwrite the published original-corpus Qwen hashpool
**10/12**.

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

Nested Youden / 10% FPR from leave-one-prompt-out on the *training* stems,
then frozen on the test files, is the honest isolated-file gate. In-sample
Youden on files that entered the fit is optimistic (hard collapsed to
always-marked). JSON: [../experiments/2026-08-31-transfer-nested-36-to-12x4/](../experiments/2026-08-31-transfer-nested-36-to-12x4/)
and [../experiments/2026-08-31-transfer-nested-12x4-to-36/](../experiments/2026-08-31-transfer-nested-12x4-to-36/).

Train 24 new stems, test 12×4 files, nested operating points:

| Method | Nested t | Test marked>t | Test unmarked≤t | sens | spec |
|---|---|---|---|---|---|
| hits Youden / FPR10 | 0.368 | 22/48 | 40/48 | 0.46 | 0.83 |
| **hashpool Youden** | **0.005** | **33/48** | **34/48** | **0.69** | **0.71** |
| hashpool FPR10 | 0.016 | 26/48 | 41/48 | 0.54 | 0.85 |
| hitmass Youden | 0.013 | 17/48 | 44/48 | 0.35 | 0.92 |

Coverage-weighted hits (`hitmass`) recovers the OOD prompt grain that plain
hits lost (8/12 → **10/12**) without hurting file AUC (0.771).

Train 12×4, test stems 13–36, nested:

| Method | Nested t | Test marked>t | Test unmarked≤t | sens | spec |
|---|---|---|---|---|---|
| hits FPR10 | 0.505 | 20/24 | 24/24 | 0.83 | 1.00 |
| **freqhits Youden / FPR10** | **0.522** | **23/24** | **23/24** | **0.96** | **0.96** |

Four draws per training prompt give shared 4-grams enough support that a
count ≥ 4 gate plus a nested threshold is an almost balanced isolated-file
rule on *new* GPT-2 topics. It is still not a universal detector.

A 50% train-label shuffle on the 36→12×4 split
([../experiments/2026-08-31-transfer-shuffle-36-to-12x4/](../experiments/2026-08-31-transfer-shuffle-36-to-12x4/))
drops isolated sign at 0 to chance (hits 19/48, hashpool 20/48). File AUC
falls from ~0.77 to ~0.61–0.64. Residual ranking is not zero: half the
training labels are still correct. Prompt-grain wins on n=12 under shuffle
are noise (hitmass 11/12 there is **not** a detection result). Frozen shuffle
tables are omitted so they cannot be used as a detector.

`surface` is a UTF-8 byte hashpool of the raw string: same laboratory mixer,
no tokenizer, so a GPT-2 fit can score Qwen text. On 12×4 GPT-2 leave-one-out
it is **10/12**, AUC 0.602, isolated 12/48 (conservative). On 24 new topics
→ 12×4 it is **9/12**, AUC 0.648; nested Youden 15/48 vs 40/48 does **not**
beat token hashpool (33/48 vs 34/48). On Qwen 12×1 leave-one-out, surface is
**9/12** (AUC 0.674) versus Qwen-tokenizer hashpool **10/12**.

`logit` is ridge logistic on z-scored file scores (hits / hashpool / surface /
hitmass) with nested Youden on the log-odds. On 12×4 LOO it is a specificity
knob (23/48 marked, 41/48 unmarked, AUC 0.735), not a 12/12 ensemble.

**Same-topic GPT-2 tables → Qwen text.** Train 12×4 GPT-2, score Qwen 12×1
with overlap kept. Hits through GPT-2 BPE of the Qwen string ranks **11/12**
(AUC 0.740) but isolated `lr > 0` is **1/12**: the LR scale shifts. Token
hashpool does not transfer (7/12, AUC 0.521). Mean-gap permutation on n=12
files is noisy (p ≈ 0.39); quote the paired 11/12, not a detector. Different
topics *and* Qwen is chance (hits 6/12, hashpool AUC 0.500).

A leave-one-prompt LDA **stack** of hits+hashpool on the original 12×4 LOO
scores is **11/12**, AUC 0.732, isolated 23/48 with unmarked ≤0 **44/48**.
It trades recall for specificity. Complementary probe misses are not a 12/12
ensemble.

`indicate fit --method hashpool` writes frozen buckets. `indicate fit
--method surface` writes byte buckets and `indicate score` reads them
without a tokenizer. Nested 36→12×4 hashpool tables with
`decision_threshold` ≈ 0.005 live at
`experiments/2026-08-31-transfer-nested-36-to-12x4/tables-hashpool/`.

## How to read this

**Coverage gating was the missing ablation on 12×4 and 36-topic GPT-2.** Scoring *only* 4-grams seen on both training sides raises 12×4 AUC from 0.626 to 0.737 (11/12) and 36-topic ranking from 20/36 to 30–31/36 (AUC 0.89). The unigram fallback in `hard` was adding topic noise. The old “more topics do not help” lesson was a scorer artifact.

**The 29/48 isolated sign was partly a protocol artifact.** Training on 24 *other* topics and scoring the 12×4 files, hits marks **39/48** (AUC 0.769). Nested hashpool Youden on that split is the honest yes/no: **33/48** marked and **34/48** unmarked. Four training draws lift OOD ranking to **12/12** and **42/48** at t=0; nested hits Youden then sits at **26/48** vs **44/48**. Training on 12×4 and scoring 24 new topics, hits ranks **24/24** (AUC **0.986** on 1-draw 256-token stems; AUC **0.924** on 96 files from 36×4). Nested hits 10% FPR on those 96 files is **83/96** vs **85/96**. Leave-one-of-36-out with four draws is **36/36** (AUC **0.934**); nested-by-stem hits **119/144** vs **134/144**. Leave-one-of-12-out hard last-4 remains 29/48.

**Hash pooling is the method that generalizes across generators.** Isolated 35/48 on 12×4 GPT-2 (p ≈ 0.001), 32/36 on 36 topics, 11/12 on Qwen 12×1 (AUC 0.750), and 11/12 prompt grain when those hash buckets are trained on other GPT-2 topics. Exact `hits` fails on Qwen 12×1 (AUC 0.417) because the 4-grams do not overlap.

**Shorter-context interpolation is corpus-dependent.** On 12×4 it hurt (7/12). On 36 topics it helped (29/36). Do not treat Witten–Bell as a default win.

**Choice geometry is real but weaker.** Unmarked-LM rank/LDA separates above chance on 12×4 (perm p 0.016–0.045) and stays key-free. It does not beat `hits` or `hashpool` there.

**A 50% train-label shuffle collapses isolated sign at 0 to chance** (19–20/48) and drops AUC from ~0.77 to ~0.61–0.64. Residual ranking is expected: half the training labels remain correct.

**Surface (UTF-8 byte) hashpool is a tokenizer-agnostic reader, not the best isolated-file rule.** In-domain: GPT-2 10/12 (AUC 0.602), Qwen 9/12 (AUC 0.674). OOD GPT-2 topics: 9/12 (AUC 0.648). Nested Youden 15/48 vs 40/48 loses to nested token hashpool 33/48 vs 34/48.

**Same-topic GPT-2 hits can rank Qwen twins 11/12 through a probe tokenizer.** Isolated sign at 0 fails (1/12). Token hashpool does not transfer (AUC 0.521). New topics plus Qwen is chance. Paired ranking is not a single-file detector. A **new Qwen 12×4 sample of the same prompts** does not reproduce that 11/12 (hits 5/12, AUC 0.355; first-draw 6/12). Extra Qwen draws also fail to lift in-domain hits (8/12, AUC 0.602) the way extra GPT-2 draws lift 30/36 to 36/36. The published Qwen 12×1 hashpool **10/12** stays tied to that corpus.

**A hits+hashpool LDA stack is a specificity knob, not a 12/12 detector.** On 12×4 LOO it keeps 11/12 and AUC 0.732 while unmarked ≤0 rises to 44/48.

**Four extra draws at matched length, not extra topics, lift in-domain GPT-2 hits to 36/36.** One 128-token draw is still 30/36. Nested-by-stem Youden on the 4-draw LRs is 119/144 vs 134/144. Out-of-family, 4-draw train → 12×4 is 12/12 ranking (42/48 at t=0) with a conservative nested Youden (26/48 vs 44/48). The reverse nested hits 10% FPR on 96 new-topic files is 83/96 vs 85/96. The same extra-draw protocol on Qwen does **not** produce a comparable isolated-file gate.

**The in-domain mark is front-loaded, and disjoint windows show where.** A
16-token prefix of the 36×4 twins already ranks 34/36 (AUC 0.916). Tokens
16–32 scored alone are near chance (22/36, AUC 0.549). The tail (64–128)
still ranks 29/36 (AUC 0.723) but does not match the opening. New-topic
ranking also appears by 16 tokens (11/12, AUC 0.752); the next 16 tokens
are chance (AUC 0.512). Matching mixin `ngram_len=5` (`context_len=5`)
does not beat last-4. This is a statement about the count-table indicator,
not that later tokens are unmarked under official `score`.

**Matching the train window to those first 16 tokens is stricter than
scoring a prefix of a full-file table.** `--fit-prefix 16` clips every
draw before fit *and* score. In-domain hits then ranks **34/36** (AUC
**0.929**) with unmarked ≤0 **112/144**, versus 76/144 on the full
128-token reader and 93/144 on fit-full/score-prefix 16. Out of family,
matched 16-token hits is **11/12**, AUC **0.818**, nested-by-stem
**39/48** vs **36/48** — better file AUC than full-file hits (0.793)
with one fewer prompt win. JSON:
[../experiments/2026-08-31-probe-36x4-fitprefix16/](../experiments/2026-08-31-probe-36x4-fitprefix16/),
[../experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix16/](../experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix16/).

**Position-bucketed last-4 (`poshits`, bucket 16) stops early 4-grams
sharing counts with the tail.** The prepended `i // 16` is not a
watermark key. In-domain on 36×4 it keeps hits' **134/144** marked t=0
detections while unmarked ≤0 rises from 76 to **97/144** (34/36, AUC
0.925). Out of family it beats full-file hits on file AUC (**0.811** vs
0.793) and nested-by-stem balance (**37/48** vs **35/48** vs hits 27/48
vs 40/48) while dropping prompt grain to 10/12. On 12×4 leave-one-out
it is a specificity knob (24/48 marked, 37/48 unmarked), not a better
t=0 detector. Combining `--fit-prefix 16` with bucket 16 is a no-op:
every token sits in bucket 0. Bucket 4 on that same 16-token window is
not: in-domain poshits then ranks **34/36** with file AUC **0.937**
(unmarked ≤0 **114/144**), a small lift over unbucketed matched-prefix
hits (0.929 / 112/144). Out of family it is **11/12**, AUC **0.820**,
nested-by-stem **39/48** vs **38/48**. JSON:
[../experiments/2026-08-31-probe-36x4-posbucket/](../experiments/2026-08-31-probe-36x4-posbucket/),
[../experiments/2026-08-31-transfer-36x4-to-12x4-posbucket/](../experiments/2026-08-31-transfer-36x4-to-12x4-posbucket/),
[../experiments/2026-08-31-probe-12x4-posbucket/](../experiments/2026-08-31-probe-12x4-posbucket/),
[../experiments/2026-08-31-probe-36x4-fitprefix16-pos4/](../experiments/2026-08-31-probe-36x4-fitprefix16-pos4/),
[../experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos4/](../experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix16-pos4/).

**Coverage is the mechanism, and it is short-context at the start.**
`--coverage` asks, leave-one-prompt-out, what share of last-k contexts
were seen on both training sides. On 36×4, window 0:16 shares **13.7%**
versus **3.9%** on 16:32, but that gap is last-1/last-2 at i=1–2 (i=1 is
**96.9%** shared). Full last-4 from i=4 is ~3–4% everywhere. Scoring
only tokens **0:4** already ranks **34/36** (AUC **0.917**), matching
0:16; tokens 4:16 are 29/36 (AUC 0.712); 16:32 is chance. Out of family,
0:4 matches 0:16 at **11/12** / 0.752.

**A matched 4-token fit plus position namespace is the tight isolated-file
reader.** `--fit-prefix 4 --pos-bucket 1` in-domain: **34/36**, AUC
**0.935**, t=0 **131/144 vs 132/144**. Trained on 24 other topics:
**12/12**, AUC **0.873**, t=0 **39/48 vs 41/48**, and nested Youden
matches t=0. Last-1 on those four tokens copies that OOD gate, so
last-4 at the opening was already truncated. Mixing generated token 0
into hits (`--include-first`) **hurts** OOD (9/12, AUC 0.719).
`--prompt-context` is mixin-aligned and does not transfer isolated-file
recall (OOD 12/12 ranking, 13/48 at t=0). `indicate score` of a lone
file cannot reconstruct the prompt.

**That 39/48 is not 39 independent token preferences.** Nine marked
misses are zeros. Hits still scores an *unseen* next token after a
shared context via Laplace. On this split, `'The'` at index 1 is 8
marked vs 52 unmarked in train, so every novel continuation gets
δ = 0.330103. That occupancy atom is 23 of 39 marked TPs and all 7
unmarked FPs. `postokhits` skips those: **12/12**, isolated **16/48**,
precision **1.000** among decided files. In-domain, only 9 of 131
poshits TPs were occupancy (`postokhits` **122/144**). Control-shuffled-30
stays **0/48** `lr>0` under both readers. Details:
[key-free-tokhits.md](key-free-tokhits.md). Do not sell 16/48 as beating
39/48. Do not replace 10/12, 29/48, or 36/36.

**Matched seed length does not cover those zeros.** Twelve new ~40-word
scene topics (`experiments/2026-08-31-pair-long12x4/`, official lamp
**12/12**) still open with only `"` and `The`. Train that pile, score
original 12×4: `postokhits` **12/12**, isolated **19/48**, precision
**1.000** among decided (all four *market* draws via `'The' → ' dog'`).
Combined with the 24 short one-liners: **20/48**. The same nine zeros
remain (night-bus `After`, all four library `Closing`, letter `Now` /
`While`, garden `Now`). Library is a prompt echo of “Closing time is
announced twice”, not a generic temporal class. On this medium-seed
train, unseen-after-The Laplace **flips** (δ ≈ −0.365); poshits is then
**8/12** with 20 marked wrong-sign files. 39/48 poshits is occupancy-
specific. Do not sell 19/48 or 20/48 as beating 39/48.

**tokbackoff shrinks last-k until an observed next token hits.** On the
short one-liner train it **copies** postokhits **16/48**. On the medium
train it adds harbour draws 3 and 4 (`The ferry was in`: last-1
`' was' → ' in'`), **21/48**, still precision **1.000**. Combined
**22/48**. The nine zeros remain. In-domain it adds one unmarked FP.
Control stays **0/48**. Do not sell 21/48 or 22/48 as beating 39/48.

**Prompt-tail transplant is not new-topic OOD.** Reusing last paragraphs
from the zero-producing 12×4 seeds, combined with short+medium train,
lifts postokhits to **30/48** and postokbackoff to **36/48** (AUC
**0.888**), precision **1.000** among decided. Library `Closing is the`
never appears in that train; backoff scores those four files via last-1
`' is' → ' the'`. Letter stays zero. Do not sell 30/48 or 36/48 as
beating 39/48.

**Qwen's in-domain opening signal is generated token 0.** `--methods first`
on a 4-token prefix ranks **12/12** (AUC **0.901**). Hits that skip
token 0 is 7/12. Full-file Qwen hits stays **8/12**. GPT-2 tables still
do not read Qwen (8/12, AUC 0.584).

**Same tokenizer is not a transferable 4-gram detector.** DistilGPT2
12×4 is officially **12/12**. In-domain hits **9/12**, AUC 0.705. GPT-2
36×4 → Distil (shared BPE, same public keys) hits **5/12**, AUC **0.462**.
The 4-gram footprint is generator-weight specific. Native Distil
unmarked-LM rankpath is chance (**8/12**, AUC **0.579**). Rank-path is
not a universal tournament detector.

**Qwen native rankpath does not copy first-token 12/12.** Opening
rankpath is **8/12**, AUC **0.590**, isolated 24/48. Qwen's in-domain
opening remains generated token 0.

**A tiny neural net does not beat those tables.** On the same 4-token
new-topic gate, tokmlp is 8/12 (AUC 0.714) against poshits **12/12**
(AUC **0.873**). A character CNN trained on GPT-2 openings does not
transfer to Distil or Qwen. Details: [key-free-learn.md](key-free-learn.md).

**Extra GPT-2 training draws do not create a Qwen detector.** 36×4 GPT-2 → new Qwen 12×4 is chance (hits 6/12, AUC 0.445). Same-topic surface on that sample is 7/12 (AUC 0.525). The published original-corpus Qwen hashpool 10/12 stays tied to that corpus.

**Argmax snap removes the public mark without keys.** On all 48 marked 12×4 files, official mean **0.6216 → 0.4994**. An unmarked control stays near 0.50 (0.508 → 0.487). About 60–90 of 128 tokens flip, so this is a statistical scrub, not a fluent rewrite. It needs the unmarked generator, not the keys.

**Binary snap-rate is not a tournament detector.** Table-free `snapupset` (in-topk not argmax) on 12×4 openings is chance: **7/12**, AUC **0.501**, perm p=0.55. Marked and unmarked leave the greedy top-k token at the same rate (0.649 vs 0.653). `snapleave` majority vote marks 48/48 and 41 unmarked files. `snapmiss` ranks (**10/12**, AUC **0.707**) because marked openings sit off-mode more often (46% vs 28% miss); isolated t=0 is **21/48 vs 41/48**, correlation 0.87 with opening pivot-rank, 0.23 with rankpath. Rank-symbol tables are not a dressed-up upset bit. Details: [key-free-snaprate.md](key-free-snaprate.md).

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

python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/2026-08-31-probe-12x4

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --max-draws 1 --methods hits,hashpool \
  --out-dir experiments/2026-08-31-probe-36x4-draws1

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --methods hits,hashpool \
  --prefix-lens 16,32,64,96,128 \
  --windows 0:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-08-31-probe-36x4-prefixes

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --fit-prefix 16 --methods hits,hashpool \
  --out-dir experiments/2026-08-31-probe-36x4-fitprefix16

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --methods hits,poshits,pospool --pos-bucket 16 \
  --out-dir experiments/2026-08-31-probe-36x4-posbucket

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --coverage --windows 0:16,16:32,32:64,64:128 \
  --out-dir experiments/2026-08-31-probe-36x4-coverage

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --fit-prefix 4 --methods hits,poshits --pos-bucket 1 \
  --out-dir experiments/2026-08-31-probe-36x4-fitprefix4-pos1

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits,hits,tokhits \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --fit-prefix 4 --context-len 1 --methods hits,poshits --pos-bucket 1 \
  --out-dir experiments/2026-08-31-probe-36x4-fitprefix4-k1-pos1

python -m text_watermark_tools probe experiments/2026-08-31-pair-qwen-12x4 \
  --model Qwen/Qwen2-1.5B-Instruct \
  --fit-prefix 4 --methods first,hits --pos-bucket 1 \
  --out-dir experiments/2026-08-31-probe-qwen-12x4-fitprefix4-pos1

python -m text_watermark_tools pair experiments/2026-08-17-grok-prompts \
  --model distilgpt2 --n-samples 4 --max-new-tokens 128 --seed 20260831 \
  --out-dir experiments/2026-08-31-pair-distilgpt2-12x4

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --overlap drop-from-train \
  --fit-prefix 16 --methods poshits,poshitmass --pos-bucket 4 \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix16-poshitmass

python -m text_watermark_tools probe experiments/2026-08-17-pair-36 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --overlap drop-from-train \
  --out-dir experiments/2026-08-31-transfer-36-to-12x4

python -m text_watermark_tools probe experiments/2026-08-17-pair-36 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --overlap drop-from-train \
  --shuffle-labels --skip-nested \
  --out-dir experiments/transfer-shuffle

python -m text_watermark_tools indicate fit experiments/2026-08-17-pair-12x4 \
  --method hashpool --out-dir experiments/indicator-gpt2-hashpool

python -m text_watermark_tools indicate score FILE.txt \
  --tables experiments/indicator-gpt2-hashpool --score-mode hashtok

python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --test-dir experiments/2026-08-17-pair-qwen \
  --overlap keep \
  --methods hits,hashpool,surface,logit \
  --out-dir experiments/2026-08-31-transfer-gpt2-to-qwen

python -m text_watermark_tools indicate score FILE.txt \
  --tables experiments/2026-08-31-transfer-nested-36-to-12x4/tables-hashpool

python -m text_watermark_tools scrub \
  experiments/2026-08-17-pair-12x4 \
  --out-dir experiments/2026-08-31-scrub-12x4

python -m text_watermark_tools probe experiments/2026-08-17-pair-12x4 \
  --methods snapleave,snapupset,snapmiss --skip-hashpool --fit-prefix 4 \
  --out-dir experiments/2026-09-01-probe-12x4-fitprefix4-snaprate

python -m text_watermark_tools learn experiments/2026-08-31-pair-36x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-learn-36x4-fitprefix4

python -m text_watermark_tools learn experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-learn-36x4-to-12x4-fitprefix4
```

Learned scorers: [key-free-learn.md](key-free-learn.md).

Occupancy vs observed next tokens: [key-free-tokhits.md](key-free-tokhits.md).
Opening geometry and ABSTAIN: [key-free-cascade.md](key-free-cascade.md).
Rank-path (no token identity): GPT-2 opening **12/12 / 41/48**, OOD **10/12 / 28/48**; full file is chance. Distil native opening is chance (**8/12**, AUC **0.579**). Qwen opening rankpath is **8/12** against first-token **12/12**. [key-free-rankpath.md](key-free-rankpath.md).
Table-free snap-rate: opening `snapupset` chance **7/12**; `snapmiss` **10/12** / **21/48**. [key-free-snaprate.md](key-free-snaprate.md).

```bash
python -m text_watermark_tools pair experiments/2026-08-31-prompts-long12 \
  --n-samples 4 --max-new-tokens 128 --seed 20260901 \
  --out-dir experiments/2026-08-31-pair-long12x4

python -m text_watermark_tools probe experiments/2026-08-31-pair-long12x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 --methods poshits,postokhits \
  --out-dir experiments/2026-08-31-transfer-long12x4-to-12x4-fitprefix4-tokhits

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits,postokbackoff \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokbackoff
```

Instance contrast (public vs `control-shuffled-30`, not key recovery):
[key-free-contrast.md](key-free-contrast.md).

```bash
python -m text_watermark_tools contrast experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --control-dir experiments/2026-08-31-pair-12x4-controlkeys \
  --fit-prefix 4 --pos-bucket 1 \
  --out-dir experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4
```
