# Coverage-then-pivot cascade (key-free, not a universal detector)

Count tables cannot score a novel opening: `lr == 0` iff `n_used == 0`.
That is the opening-overlap bound in
[key-free-tokhits.md](key-free-tokhits.md). This note asks whether
**unmarked-LM choice geometry** can classify those zeros without keys,
`hash_iv`, or g-values.

Tournament sampling only reweights the public model's top-k. Two
implementation mistakes in the original full-file pivot hid the
front-loaded mark:

1. Generated token 0 was never scored (no context). With a prompt
   prefix it is the first tournament decision; without a prompt it
   stays unscored. Isolated `indicate score` of a lone file cannot
   reconstruct the prompt, so the isolated-file reader is generated
   tokens 1–3 of a 4-token opening.
2. Uniform means over 128 tokens dilute near-ties. Entropy weighting
   and `in_topk` are still key-free.

The cascade protocol is: **use the observed-token LR when `n_used > 0`;
otherwise the unmarked-LM score**. Signs at threshold 0 are comparable.
A single AUC on mixed magnitudes is not a detector. `indicate score`
now prints `n_used` and `decision=ABSTAIN` when coverage is zero,
instead of treating `lr=0` as unmarked.

`--cascade` count tables are the isolated-file reader (`count_prompt_context=False`)
even when `--prompt-context` is on for the pivot.

## In-domain 12×4 leave-one-prompt-out, 4 generated tokens

`--fit-prefix 4 --pos-bucket 1 --methods postokbackoff --pivot --cascade postokbackoff`.
JSON: [../experiments/2026-08-31-probe-12x4-fitprefix4-cascade-isolated/](../experiments/2026-08-31-probe-12x4-fitprefix4-cascade-isolated/)
and [../experiments/2026-08-31-probe-12x4-fitprefix4-cascade-prompt/](../experiments/2026-08-31-probe-12x4-fitprefix4-cascade-prompt/).

| Reader | Prompt | Prompt wins | File AUC | marked>0 | unmarked≤0 |
|---|---|---|---|---|---|
| Full-file pivot-lda (published) | no | 10/12 | 0.599 | 17/48 | 31/48 |
| Opening pivot-lda | no | **10/12** | **0.672** | **27/48** | 37/48 |
| Opening pivot-rank | no | **10/12** | **0.674** | **31/48** | 30/48 |
| Opening pivot-lda-entropy | no | 9/12 | 0.650 | 24/48 | 35/48 |
| postokbackoff | no | **12/12** | 0.756 | 23/48 | 47/48 |
| cascade (count then pivot-lda) | no | 11/12 | 0.798† | 36/48 | 37/48 |
| Opening pivot-lda | **yes** | 7/12 | 0.468 | 19/48 | 27/48 |
| postokbackoff | **yes** | 12/12 | 0.893 | 42/48 | 37/48 |

† Mixed-magnitude AUC. Not a detector headline.

The mark in unmarked-LM geometry is **front-loaded**, same as the count
tables. Opening-only generated tokens beat the published 128-token
pivot (27/48 vs 17/48). Entropy weighting did not beat uniform LDA
here.

Prompt-conditioned geometry is **worse than chance** under
leave-one-prompt-out. The first tournament decision is given a prompt
the LDA never saw. That is not an isolated-file protocol and it is not
a held-out-prompt detector. Prompt-context count tables also stop
being an isolated-file reader (`indicate score` already refuses them).

Cascade on this in-domain split: count covers 23/48 (23/23 TP, 1 FP);
pivot fallback 13/25 marked and 10 unmarked FPs among 43 uncovered
unmarked. Combined 36/48 is not a calibrated detector.

## Out-of-family: 24 short 36×4 stems → 12×4

Same 4-token window. Isolated generated-only geometry.

JSON: [../experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-cascade-isolated/](../experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-cascade-isolated/).

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | decided fp | precision |
|---|---|---|---|---|---|---|
| postokbackoff | **12/12** | 0.694 | **16/48** | **48/48** | 0 | **1.000** |
| pivot-lda | 4/12 | 0.422 | 15/48 | 29/48 | 19 | 0.441 |
| pivot-rank | 2/12 | 0.317 | 16/48 | 19/48 | 29 | 0.356 |
| pivot-rank-entropy | 10/12 | 0.678 | 32/48 | 26/48 | 22 | 0.593 |
| cascade | 6/12 | 0.517† | 18/48 | 31/48 | 17 | 0.514 |

postokbackoff copies the known 16/48 / precision 1.0 gate. Opening LDA
**does not transfer**. Rank+entropy is the only geometry that keeps
prompt ranking (10/12) on this split; isolated sign 32/48 spends 22
unmarked FPs. Cascade fallback is 2/32 marked and wrecks the 12/12
count ranking (6/12). Do not sell 18/48 or 32/48 as beating 39/48.

Prompt-conditioned OOD geometry is also chance or worse
([cascade-prompt](../experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-cascade-prompt/)).
Cascade count tables stay isolated (16/48, precision 1.0); pivot
fallback 9/32.

## Combined short+medium+tails+neighborhood → 12×4

Sixty training stems after dropping the 12 test prompts. Isolated.

JSON: [../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-isolated/](../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-isolated/).

| Method | Prompt wins | covered | marked>0 | unmarked≤0 | decided fn | decided fp | precision |
|---|---|---|---|---|---|---|---|
| postokbackoff | 10/12 | **42/48** | **34/48** | **48/48** | 8 | 0 | **1.000** |
| pivot-lda | 10/12 | — | 33/48 | 32/48 | — | 16 | 0.673 |
| cascade | 10/12 | — | 39/48 | 33/48 | 9 | 15 | 0.722 |

Coverage is 42/48; **eight of those 42 have negative observed-token
LR**. Covering an opening is not the same as a marked-like
continuation. Openings tables quoted 42/48 covered with precision 1.0
(no unmarked FP). Quote both: 42 covered, 34 `lr>0`.

The six leftover zeros are station d4, letter d2/d3, office d1/d3/d4.
Isolated pivot-lda signs 5/6 of them, and also 15 of 42 uncovered
unmarked files. That 5/6 slice is not a test. Combined 39/48 has
precision 0.722. Do not sell 39/48 cascade as beating poshits 39/48
(The-Laplace occupancy, different FPs).

Rank-path leftover fill-in, same 60-stem count tables, not the full
file. Opening rankuni: **2/6** leftover, 15 unmarked FPs, cascade
36/48. Full-file rankpath: **4/6** leftover, 17 unmarked FPs, cascade
38/48. Unbucketed prefix-4 rankpath (`--cascade-rankpath-end 4`):
**1/6** leftover, 5 unmarked FPs, cascade **35/48 vs 43/48**. Uncovered
FPR10 on the saved opening-rankuni rows is 1/6 leftover and 3 unmarked
FPs. Quote the count channel when `n_used>0`. Do not sell 35–38/48.

Coverage cascade leaves eight **covered-negative** harbour / ferry
openings on the count channel (`The ferry was so/over/...`, last-1
`' was'` looks unmarked). `--cascade-when positive` sends those to
prefix-4 rankpath as well as the zeros. Rebound from the same saved
rows, no new GPT-2 forwards:

JSON: [../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4-when-positive/](../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4-when-positive/).

| Rule | marked>0 | unmarked≤0 |
|---|---|---|
| count `lr>0` | **34/48** | **48/48** |
| coverage cascade | 35/48 | 43/48 |
| **positive-when cascade** | **40/48** | **40/48** |

Five of eight covered-negatives sign, plus one leftover zero. Eight
unmarked FPs, all rankpath. Combined accuracy **80/96** vs count
**82/96**. Fallback FPR10 on that residual is combined **39/48 vs 44/48**.
Do not sell 40/48 or 39/48 as beating poshits **39/48**.

## Leftover eight are officially marked

The eight positive-when misses are not unmarked openings. Official
`public-deepmind-30` mean on isolated generated prefixes
([../experiments/2026-09-01-official-prefix-leftover/](../experiments/2026-09-01-official-prefix-leftover/)):

| prefix | leftover marked | other marked | unmarked |
|---|---|---|---|
| 5 (one 5-gram) | 0.637 (6/8 >0.55) | 0.633 | 0.481 |
| 16 | **0.627, 8/8 >0.55** | 0.626, 40/40 | 0.496, 3/48 |
| 128 | 0.621, 8/8 | 0.622, 40/40 | 0.500, 0/48 |

Prefix 4 is shorter than `ngram_len=5` and returns no official score.
Letter d2/d3 prefix-5 means are **0.733 / 0.767**. Office d1/d3 are
0.500 at five tokens and 0.633 at eight. In-domain opening rankpath
already signs 7/8; only letter d2 misses. The OOD miss is overlap plus
one hard 5-gram (`Now in the second I`).

That 5-gram is generated token 4. Isolated `--fit-prefix 4` rankpath
never scores it (three symbols = tokens 1–3). Isolated unmarked GPT-2
ranks `I` given `Now in the second` at **41** (miss top-k). The same
token with the prompt in context is rank **11**. Official g-values on
the isolated 5-gram match the last n-gram of `prompt + generated[:5]`
(22/30). Isolated rankpath is the right tokens and the wrong LM
context; generation-time rank 11 is not the near-tie bin.

In-domain `--fit-prefix 5` rankpath
([../experiments/2026-09-01-probe-12x4-fitprefix5-rankpath/](../experiments/2026-09-01-probe-12x4-fitprefix5-rankpath/))
is **11/12**, **30/48 vs 36/48**. Prefix-4 stays **12/12 / 41/48**.
Letter d2 stays `lr<0` (−1.208). Window `3:4` rankuni (token 4 alone)
is **4/12**, AUC **0.406**. Letter d3's 5-gram is also an isolated
miss (rank 41, official 0.767); prefix-4 already signs it from tokens
1–3. Ferry-queue d4 is officially marked (0.700) on the **argmax**.
Keep prefix-4. Do not sell 30/48.

Among 45 marked files with official prefix-5 >0.55, isolated token-4
rank is **10 argmax** and **8 miss**. Unmarked isolated miss is **7/48**
vs marked **9/48**. Fifth-token rank is not a detector.

JSON: [../experiments/2026-09-01-letter-d2-first-ngram/](../experiments/2026-09-01-letter-d2-first-ngram/).

60-stem `--fit-prefix 8` postokbackoff
([../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-rankpath/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-rankpath/))
covers 4 of 6 prefix-4 zeros (station d4, letter d3, office d1/d3):
**38/48 vs 40/48**, precision 0.826, AUC **0.818**. Combined **78/96**
vs prefix-4 count **82/96**. Nested FPR10 38/48 vs 42/48. Letter d2
stays `lr<0`. That negative is last-1 `' in' → ' the'` (c_m=2, c_u=8),
not the official 5-gram. The 5-gram is unseen at last-4/3/2; last-1
`' second'` never continues with `' I'`. `postokbackoff2` abstains
(`n_used=0`). Letter d3's prefix-8 rescue is last-1 `',' → ' my'`,
not `While working on the key`. All four extra TPs are last-1
punctuation; **20 of 38** TPs are last-1 only. Prefix-8
`postokbackoff2` is **18/48 vs 46/48**, precision 0.900 among decided
([../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-backoff2/](../experiments/2026-09-01-transfer-short-medium-tails-family-to-12x4-prefix8-backoff2/)).
Prefix-8 rankpath is 30/48 vs 35/48 and does not beat prefix-4
rankpath. Do not sell 38/48 or 18/48 as beating poshits **39/48**.

## What to use

- Isolated-file observed-token reader: `postokhits` / `postokbackoff`
  with `n_used` and **ABSTAIN** at coverage 0. Precision 1.0 among
  decided files on the 24-short OOD gate; recall is the overlap bound.
- In-domain opening geometry (generated-only, 4 tokens) is a real
  key-free ranking signal and is stronger than the published full-file
  pivot. It is not a transferred isolated-file detector.
- Prompt-conditioned geometry is not an isolated-file protocol and
  fails leave-one-prompt-out.
- Cascade is an honest two-channel report, not a single score.
  Rank-path fallback uses the opening path (or prefix-N), never the
  full file. `--cascade-when coverage` (default) substitutes only at
  `n_used=0`. `--cascade-when positive` also substitutes covered
  negatives; on the 60-stem prefix-4 gate that is **40/48 vs 40/48**.
  Quote the count channel when it is positive. Uncovered-only 10% FPR
  is reported beside t=0. Prefix-8 backoff on the same 60-stem train is
  **38/48 vs 40/48** (4 extra zeros, 8 FPs). Those extras are last-1
  punctuation, not official 5-grams. Prefix-8 `postokbackoff2` is
  **18/48 vs 46/48**. Keep prefix-4 when the high-precision last-1
  reader is the point. Isolated prefix-5 rankpath is **11/12**,
  **30/48 vs 36/48** and still misses letter d2's official 5-gram
  (isolated rank 41, prompt rank 11). Keep prefix-4.

Still not keys. Still not a universal detector. Do not replace
**10/12**, **29/48**, or **36/36**. Rank-path tables that score novel
openings without token identity are in
[key-free-rankpath.md](key-free-rankpath.md).
