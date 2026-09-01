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

Still not keys. Still not a universal detector. Do not replace
**10/12**, **29/48**, or **36/36**. Rank-path tables that score novel
openings without token identity are in
[key-free-rankpath.md](key-free-rankpath.md).
