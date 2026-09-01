# Rank-path tables (key-free, not a universal detector)

Token count tables cannot score a novel opening: `lr == 0` iff
`n_used == 0`. That is an overlap bound on **token identity**. Tournament
sampling does not need the same tokens. It biases which rank within the
unmarked top-k is chosen.

This reader discretizes that rank into five symbols and fits the same
observed-token tables on the symbol sequence:

| Symbol | Meaning |
|---|---|
| 0 | missed the unmarked top-k |
| 1 | unmarked argmax (rank 1) |
| 2 | ranks 2–3 (tight near-tie) |
| 3 | ranks 4–10 |
| 4 | ranks 11–k |

Still no keys, `hash_iv`, or g-values. Isolated `indicate score` still
needs the public unmarked LM (same as pivot) and still cannot reconstruct
a prompt. The first generated token has no unmarked-LM context without a
prompt, so the isolated-file path scores generated tokens 1… The first
*symbol* is therefore a real tournament decision (`include_first` on the
symbol sequence).

`--rankpath` reports `rankpath` (tokbackoff on symbols) and `rankuni`
(rank-symbol unigram). `--cascade-fallback rankuni` uses the unigram when
count tables abstain.

JSON: [../experiments/2026-08-31-probe-12x4-fitprefix4-rankpath-isolated/](../experiments/2026-08-31-probe-12x4-fitprefix4-rankpath-isolated/),
[../experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-rankpath-isolated/](../experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-rankpath-isolated/),
[../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-rankpath-isolated/](../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-rankpath-isolated/).

`--fit-prefix 4 --pos-bucket 1`. Isolated generated-only geometry.
`used_keys=false`.

## In-domain 12×4 leave-one-prompt-out

| Reader | Prompt wins | File AUC | marked>0 | unmarked≤0 | precision |
|---|---|---|---|---|---|
| postokbackoff | **12/12** | 0.756 | 23/48 | 47/48 | 0.958 |
| Opening pivot-lda | 10/12 | 0.672 | 27/48 | 37/48 | 0.711 |
| **rankpath** | **12/12** | **0.797** | **41/48** | **39/48** | 0.820 |
| rankuni | 11/12 | 0.759 | 33/48 | 32/48 | 0.673 |
| cascade (count then rankuni) | 12/12 | 0.858† | 37/48 | 33/48 | 0.712 |

† Mixed-magnitude AUC. Not a detector headline.

Rank-path tokbackoff on the five-symbol alphabet is a real in-domain
isolated-file signal: **41/48** at threshold 0 with 9 unmarked FPs. That
is stronger than opening LDA (**27/48**) and stronger than the published
full-file pivot (**17/48**). It is **not** the 29/48 last-4 hard-holdout
headline (different protocol, 128-token files). Nested-by-stem Youden is
**37/48 vs 39/48**.

## Out-of-family: 24 short 36×4 stems → 12×4

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | precision |
|---|---|---|---|---|---|
| postokbackoff | **12/12** | 0.694 | **16/48** | **48/48** | **1.000** |
| pivot-lda | 4/12 | 0.422 | 15/48 | 29/48 | 0.441 |
| **rankpath** | **10/12** | **0.683** | **28/48** | **33/48** | 0.651 |
| rankuni | 8/12 | 0.628 | 29/48 | 25/48 | 0.558 |
| cascade | 8/12 | 0.719† | 32/48 | 25/48 | 0.582 |

Opening LDA **does not transfer**. Rank-path **does**, as prompt ranking
(**10/12**) and as an isolated sign (**28/48**) that still spends 15
unmarked FPs. Do not sell 28/48 or cascade 32/48 as beating 39/48. Count
tables on this gate remain the high-precision channel (16/48, precision
1.0 among decided). Cascade fallback is 16/32 and drops ranking to 8/12.

## Combined short+medium+tails+neighborhood → 12×4

Sixty training stems after dropping the 12 test prompts.

| Method | Prompt wins | covered | marked>0 | unmarked≤0 | precision |
|---|---|---|---|---|---|
| postokbackoff | 10/12 | **42/48** | **34/48** | **48/48** | **1.000** |
| rankpath | **12/12** | — | 30/48 | 32/48 | 0.652 |
| rankuni | 10/12 | — | 37/48 | 31/48 | 0.685 |
| cascade | 10/12 | — | 36/48 | 33/48 | 0.706 |

The six leftover count zeros are station d4, letter d2/d3, office d1/d3/d4.
Rankuni signs **2/6** of them (`While working on the`, `The printer worked better`)
and 15 of 42 uncovered unmarked files. Combined cascade 36/48 is not a
calibrated detector. Do not sell rankuni 37/48 or cascade 36/48 as beating
poshits 39/48.

## Full file: the rank path is front-loaded

`--rankpath-full` with `--rankpath-pos-bucket 0` scores the unclipped
choice-matrix rows (generated tokens 1…). Matched `--prefix-lens` and
`--windows` slice those rows. `used_keys=false`.

JSON: [../experiments/2026-08-31-probe-12x4-rankpath-full-isolated/](../experiments/2026-08-31-probe-12x4-rankpath-full-isolated/),
[../experiments/2026-08-31-transfer-36x4-to-12x4-rankpath-full-isolated/](../experiments/2026-08-31-transfer-36x4-to-12x4-rankpath-full-isolated/),
[../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-rankpath-full-cascade/](../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-rankpath-full-cascade/).

In-domain 12×4 LOO, unbucketed:

| Slice | Prompt wins | File AUC | marked>0 | unmarked≤0 |
|---|---|---|---|---|
| prefix 4 rank symbols | **10/12** | **0.718** | 30/48 | 35/48 |
| prefix / window 0:16 | 9/12 | 0.620 | — | — |
| window 16:32 | 6/12 | 0.506 | 23/48 | 24/48 |
| full 128 (≈127 symbols) | 8/12 | 0.559 | 27/48 | 28/48 |

Permutation p on the full file is 0.145. Tokens 16–32 are chance, the
same place token-identity hits go to chance. Averaging a 128-token rank
path dilutes the opening the way the published full-file pivot did
(17/48).

Out of family, 24 short 36×4 stems → 12×4, same unbucketed slices:

| Slice | Prompt wins | File AUC | marked>0 | unmarked≤0 | precision |
|---|---|---|---|---|---|
| **prefix 4** | **11/12** | **0.759** | **25/48** | **43/48** | **0.833** |
| window 16:32 | 5/12 | 0.471 | 21/48 | 25/48 | 0.457 |
| full 128 | 6/12 | 0.534 | 24/48 | 26/48 | 0.522 |

Prefix-4 here is four choice-matrix rows (generated tokens 1–4),
unbucketed. The opening protocol above is three rows with `--pos-bucket 1`
(10/12, 28/48, 15 unmarked FPs). Unbucketed prefix-4 transfers as ranking
**11/12** with only **5** unmarked FPs. It does not beat poshits 39/48
and is not 29/48. Full-file rankuni 41/48 on this gate spends 31 unmarked
FPs (precision 0.569): a sign count, not a detector.

60-stem train, `--fit-prefix 4` count tables plus `--rankpath-full`
fallback: postokbackoff still **42 covered / 34 `lr>0`**, precision 1.0
among decided. Full-file rankpath fallback signs **4/6** leftover zeros
and 17 of 42 uncovered unmarked files. Combined cascade **38/48**,
precision 0.691. Mixed AUC 0.822 is not a detector. Do not sell 38/48.

## What to use

- Isolated-file observed-token reader: `postokhits` / `postokbackoff` with
  `n_used` and **ABSTAIN** at coverage 0. Precision 1.0 among decided files
  on the 24-short OOD gate; recall is the overlap bound.
- Isolated-file **rank path** is a second channel that does not need token
  overlap. Use the **opening** reader (`--fit-prefix 4 --pos-bucket 1`):
  in-domain 12/12, 41/48; OOD 10/12, 28/48 with unmarked FPs. Unbucketed
  first-four rank symbols transfer as ranking **11/12** with isolated
  **25/48 vs 43/48** (5 unmarked FPs). Full-file rank-path is chance.
  It is not a universal detector.
- Cascade remains an honest two-channel report. On these OOD gates the
  high-precision count channel is still the one to quote when coverage
  exists. Full-file rankpath fallback is not a calibrated fill-in.

Still not keys. Still not a universal detector. Do not replace
**10/12**, **29/48**, or **36/36**.
