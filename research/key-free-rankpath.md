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

After the truncated-context recount and first-symbol fix
(`experiments/2026-09-01-probe-12x4-recount-opening-rankpath/`), in-domain
opening rankpath is **11/12**, isolated still **41/48 vs 35/48**. That isolated
sign survived; prompt ranking dropped by one group. It is discovery, not a
headline, and it does not replace recounted hard **25/48**. Pre-fix JSON in
the directories above stays as collected.

Rank-path tokbackoff on the five-symbol alphabet is a real in-domain
isolated-file signal: **41/48** at threshold 0 with 9 unmarked FPs (pre-fix
JSON). That
is stronger than opening LDA (**27/48**) and stronger than the published
full-file pivot (**17/48**). It is **not** the 25/48 last-4 hard-holdout
headline (different protocol, 128-token files). Nested-by-stem Youden is
**37/48 vs 41/48**. Isolated `--fit-prefix 5` (four symbols, last row =
the first official 5-gram) is **11/12**, **30/48 vs 36/48** and still
misses letter d2. Keep prefix-4. See
[key-free-cascade.md](key-free-cascade.md). DistilGPT2 and gpt2-medium
unmarked-LM opening rankpath 12-LOO on the original GPT-2 twins is
named before those LRs
([PROTOCOL-isolated-rankpath-lm.md](PROTOCOL-isolated-rankpath-lm.md)).
Distil-LM isolated is **32/48 vs 31/48** (ranking **10/12**).
gpt2-medium-LM isolated is **31/48 vs 32/48**. Do not sell **32/48** or
**31/48**. Do not leftover-slice. That freeze does not replace **25/48**.

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

## Instance contrast (not key recovery)

Fit public 36×4 rank-path tables. Score the 12×4 public twins and the
matching `control-shuffled-30` pile. Same three comparisons as
[key-free-contrast.md](key-free-contrast.md). `used_keys=false`.

JSON: [../experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4-rankpath/](../experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4-rankpath/),
[../experiments/2026-08-31-contrast-36x4-to-12x4-prefix4-rankpath/](../experiments/2026-08-31-contrast-36x4-to-12x4-prefix4-rankpath/).

Opening (`--fit-prefix 4 --pos-bucket 1`):

| Method | Comparison | Prompt wins | File AUC | pos `lr>0` | neg `lr≤0` | perm p |
|---|---|---|---|---|---|---|
| **rankpath** | public-vs-unmarked | **10/12** | **0.683** | **28/48** | 33/48 | 0.002 |
| **rankpath** | control-vs-unmarked | 8/12 | **0.498** | 17/48 | 33/48 | 0.42 |
| **rankpath** | public-vs-control | 9/12 | **0.694** | 28/48 | 31/48 | 0.001 |
| rankuni | public-vs-unmarked | 8/12 | 0.628 | 29/48 | 25/48 | 0.019 |
| rankuni | control-vs-unmarked | 9/12 | **0.613** | **30/48** | 25/48 | 0.025 |
| rankuni | public-vs-control | 5/12 | **0.502** | 29/48 | 18/48 | 0.49 |

Unbucketed prefix-4 (`--fit-prefix 5 --pos-bucket 0`):

| Method | Comparison | Prompt wins | File AUC | pos `lr>0` | neg `lr≤0` | perm p |
|---|---|---|---|---|---|---|
| **rankpath** | public-vs-unmarked | **11/12** | **0.759** | **25/48** | **43/48** | 0.00050 |
| **rankpath** | control-vs-unmarked | 6/12 | **0.511** | **6/48** | 43/48 | 0.27 |
| **rankpath** | public-vs-control | 9/12 | **0.752** | 25/48 | 42/48 | 0.00050 |
| rankuni | public-vs-unmarked | 10/12 | 0.653 | 31/48 | 27/48 | 0.005 |
| rankuni | control-vs-unmarked | 7/12 | 0.557 | 22/48 | 27/48 | 0.17 |
| rankuni | public-vs-control | 7/12 | 0.594 | 31/48 | 26/48 | 0.034 |

**rankpath tokbackoff** ranks the other instance with unmarked (opening
AUC 0.498; prefix-4 AUC 0.511). Public vs control matches public vs
unmarked. Isolated control `lr>0` is **not** the poshits **0/48**:
opening 17/48, prefix-4 **6/48** (the same 5–6 false-positive rate as
unmarked). Prefix-4 is the cleaner instance check.

**rankuni** on the opening sees tournament sampling in general
(control **30/48**, public vs control chance). Do not headline the
unigram as instance-specific.

Neither outcome recovers keys.

## Prefix-4 cascade fallback (60-stem train)

JSON: [../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/](../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/).

Count tables stay `--fit-prefix 4 --pos-bucket 1`. Fallback is
unbucketed first-four rank symbols (`--cascade-rankpath-end 4`), not
the full file.

| Channel | marked>0 | unmarked≤0 |
|---|---|---|
| postokbackoff (covered 42/48) | **34/48** | **48/48** |
| prefix-4 rankpath on leftover zeros | **1/6** | 37/42 |
| combined t=0 | **35/48** | **43/48** |
| combined at uncovered FPR10 | 35/48 | 44/48 |

One leftover zero signs (`The printer worked better`). Five unmarked
FPs at t=0. That is higher precision than opening rankuni (2/6 leftover,
15 unmarked FPs) and than full-file rankpath (4/6 leftover, 17 unmarked
FPs). Do not sell 35/48 as beating poshits 39/48.

Recomputing Youden / 10% FPR on *already saved* opening-rankuni leftover
rows: FPR10 t=0.154 signs 1/6 leftover and 3 unmarked FPs (combined
35/48 vs 45/48). Full-file leftover FPR10 signs 2/6 with 4 unmarked FPs.
The high-precision fill-in is a threshold on the uncovered channel, not
a mixed-magnitude AUC.

## DistilGPT2 and Qwen: not a universal tournament detector

A working mixin is not enough. Rank-path uses the **generator's own**
unmarked LM. DistilGPT2 12×4 is officially **12/12**; in-domain token
hits is **9/12**, AUC 0.705. Native Distil unmarked-LM rankpath is
chance.

JSON: [../experiments/2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath/](../experiments/2026-08-31-probe-distilgpt2-12x4-fitprefix4-rankpath/),
[../experiments/2026-08-31-probe-distilgpt2-12x4-prefix4-rankpath/](../experiments/2026-08-31-probe-distilgpt2-12x4-prefix4-rankpath/),
[../experiments/2026-08-31-transfer-36x4-to-distilgpt2-fitprefix4-rankpath/](../experiments/2026-08-31-transfer-36x4-to-distilgpt2-fitprefix4-rankpath/),
[../experiments/2026-08-31-probe-qwen-12x4-fitprefix4-rankpath/](../experiments/2026-08-31-probe-qwen-12x4-fitprefix4-rankpath/),
[../experiments/2026-08-31-probe-qwen-12x4-prefix4-rankpath/](../experiments/2026-08-31-probe-qwen-12x4-prefix4-rankpath/).

| Protocol | Prompt wins | File AUC | marked>0 | unmarked≤0 | perm p |
|---|---|---|---|---|---|
| Distil opening rankpath | **8/12** | **0.579** | 28/48 | 32/48 | 0.132 |
| Distil prefix-4 rankpath | **7/12** | **0.563** | 23/48 | 26/48 | 0.099 |
| GPT-2 36×4 rankpath → Distil (GPT-2 LM) | 9/12 | 0.636 | 21/48 | 34/48 | 0.017 |
| Qwen opening rankpath | **8/12** | **0.590** | 24/48 | 32/48 | 0.029 |
| Qwen prefix-4 rankpath | **9/12** | **0.662** | 25/48 | 33/48 | 0.0035 |

Distil rankuni is worse than chance (opening 5/12, AUC 0.451). GPT-2
ranks of Distil tokens are the **wrong LM** for Distil’s tournament:
weak ranking, isolated **21/48**, not a Distil reader. Token-identity
hits on that split is **5/12**, AUC **0.462**. Native Distil (right LM)
is the fairer test, and that is chance.

Qwen’s in-domain opening **is generated token 0** (`first` **12/12**,
AUC **0.901**). Rankpath scores generated tokens 1… and does not recover
that. Opening rankpath is 8/12 (isolated 24/48). Prefix-4 file AUC is
weakly above chance (**9/12**, AUC **0.662**, perm p=0.0035, isolated
25/48) and is still not the first-token gate. Do not score Qwen ids with
GPT-2 tables.

Rank-path is GPT-2-geometry-specific on the piles we have. It is not a
universal tournament detector.

## 60-stem prefix-4 as a standalone isolated-file reader

Not leftover-only cascade. Train 60 stems (36×4 + long + tails +
family, overlapping 12×4 prompts dropped). Score the original 12×4.
`--fit-prefix 5 --pos-bucket 0`. `used_keys=false`.

JSON: [../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-prefix4-rankpath/](../experiments/2026-08-31-transfer-short-medium-tails-family-to-12x4-prefix4-rankpath/).

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | precision |
|---|---|---|---|---|---|
| **rankpath** | **10/12** | **0.770** | **28/48** | **40/48** | 0.778 |
| rankuni | 11/12 | 0.761 | 39/48 | 32/48 | 0.709 |

24-short unbucketed prefix-4 was **11/12**, **25/48 vs 43/48**. Combined
accuracy is the same **68/96**. Extra stems add 3 TPs and 3 FPs.
Nested FPR10 is 11/48 vs 47/48. Do not sell 28/48 as beating **29/48**
or rankuni 39/48 as beating poshits **39/48** (16 unmarked FPs).

## 100-family tables → original 12 (PROTOCOL-isolated lock C)

Not a new scorer. Frozen `--methods rankpath --fit-prefix 4 --pos-bucket 1`
on the 100 GPT-2 families, scored on the original 12×4 files.

Prompt ranking **10/12**. Nested Youden **24/48 vs 41/48**. Isolated t=0
**24/48 vs 40/48**. Does not beat recounted hard **25/48**.

Prompt losses: **letter**, **garden**. Garden is also the 12-LOO
opening-rankpath miss on these files. Letter is lock B's only miss.
Lock C recovers harbour and ferry-queue (`The ferry` openings) that
lock A interpolate missed (4/4 marked t=0). Three ranking wins have
**0/4** marked files above 0: night-bus, library, market. Those stems
rank because unmarked LRs are more negative — the rankpath analog of
occupancy, not isolated-file recall. Do not sell a union of locks A/B/C
(t=0 **42/48**, nested **40/48**). On the 36-topic pool the only prompt
loss is library (Closing, different draws, still 0/4 marked t=0).

JSON: [../experiments/2026-09-01-transfer-100x4-to-12x4-opening-rankpath/](../experiments/2026-09-01-transfer-100x4-to-12x4-opening-rankpath/),
[../experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4/stems.json](../experiments/2026-09-01-transfer-100x4-to-12x4-hard-last4/stems.json).

## What to use

- Isolated-file observed-token reader: `postokhits` / `postokbackoff` with
  `n_used` and **ABSTAIN** at coverage 0. Precision 1.0 among decided files
  on the 24-short OOD gate; recall is the overlap bound.
- Isolated-file **rank path** is a second channel that does not need token
  overlap. On **GPT-2** use the **opening** reader (`--fit-prefix 4
  --pos-bucket 1`): in-domain 12/12, 41/48; OOD 10/12, 28/48 with unmarked
  FPs. Unbucketed first-four rank symbols transfer as ranking **11/12**
  with isolated **25/48 vs 43/48** (5 unmarked FPs). 60-stem prefix-4 as a
  standalone reader is **10/12**, **28/48 vs 40/48** (same 68/96 combined
  as 24-short). Prefix-5 (four symbols) is weaker (**11/12**, 30/48) and
  still misses letter d2's official 5-gram. Full-file rank-path is chance.
  Native Distil opening rankpath is chance (**8/12**, AUC **0.579**)
  despite official 12/12. Native Qwen opening rankpath is **8/12** against
  first-token **12/12**. Rank-path is not a universal tournament detector.
  An officially marked 5-gram can sit at isolated rank 41 or at the
  argmax; neither is the near-tie bin.
- Table-free snap-rate is **not** a substitute. Opening `snapupset`
  (in-topk not argmax) is chance (**7/12**, AUC **0.501**). `snapmiss`
  ranking is already inside opening LDA. See
  [key-free-snaprate.md](key-free-snaprate.md).
- Cascade remains an honest two-channel report. Quote the high-precision
  count channel when `n_used>0`. When it abstains, use the **opening**
  rank-path reader, not the full file. Unbucketed prefix-4 is the
  higher-precision leftover fill-in on the 60-stem gate (1/6 leftover,
  5 unmarked FPs). Uncovered-only 10% FPR is reported beside t=0.
  `--cascade-when positive` also sends covered-negative count files to
  that leftover reader: **40/48 vs 40/48** on the 60-stem prefix-4 gate
  (5 of 8 ferry covered-negatives plus 1 leftover zero; 8 unmarked FPs).
  Combined 80/96 vs count 82/96. Mixed AUC is not a detector.

Still not keys. Still not a universal detector. Do not replace
recounted **9/12**, **25/48**, or **36/36**.
