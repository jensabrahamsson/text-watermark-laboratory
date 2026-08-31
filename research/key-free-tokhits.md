# Observed-token hits vs Laplace occupancy

The 4-token new-topic isolated-file gate
(`experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-pos1/`,
`--pos-bucket 1`, skip generated token 0) is **12/12** prompt ranking
and **39/48** marked files with `lr > 0`. That 39/48 is **not** 39
independent next-token preferences. Nine of the twelve missed marked
files are **zeros**, not wrong-sign scores. Among files with a non-zero
LR, marked is **39/39** positive on this gate.

`tokhits` / `postokhits` skip a context that never produced the observed
next token on either side of the training tables
(`n_m[token] + n_u[token] < 1`). They keep the same Laplace log-ratio
when the token **was** seen at least once. They do not reconstruct keys.

## Protocol

```bash
python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --fit-prefix 4 --pos-bucket 1 \
  --methods poshits,postokhits,hits,tokhits \
  --out-dir experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits

python -m text_watermark_tools probe experiments/2026-08-31-pair-36x4 \
  --fit-prefix 4 --pos-bucket 1 --methods poshits,postokhits \
  --out-dir experiments/2026-08-31-probe-36x4-fitprefix4-postokhits

python -m text_watermark_tools contrast experiments/2026-08-31-pair-36x4 \
  --test-dir experiments/2026-08-17-pair-12x4 \
  --control-dir experiments/2026-08-31-pair-12x4-controlkeys \
  --fit-prefix 4 --pos-bucket 1 \
  --methods hits,tokhits,poshits,postokhits \
  --out-dir experiments/2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokhits
```

Fit 24 other 36×4 stems. Score 12×4 files, first 4 generated tokens.
Position bucket 1 prepends `i`. Skip token 0.

Rebuild the atom dump from the persisted poshits tables (no keys):

```python
from pathlib import Path
from text_watermark_tools.atoms import dump_opening_atoms

dump_opening_atoms(
    Path("experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits/tables-poshits"),
    Path("experiments/2026-08-17-pair-12x4"),
    Path("experiments/2026-08-31-transfer-36x4-to-12x4-fitprefix4-tokhits/atoms.json"),
)
```

## Laplace occupancy on shared "The"

At generated index 1 the previous token is often `'The'`. On this
training split the context occupancy is **8 marked vs 52 unmarked**.
Hits still fire when the **context** is shared, even if the next token
never appeared. Unequal occupancy then gives every novel continuation
the same δ:

```
log(α / (8 + αV)) − log(α / (52 + αV)) = 0.330103
```

That one family of atoms accounts for **23 of 39** marked true positives
(The ferry / bus / dog / printer / car / …) **and all 7** unmarked false
positives (The weather / passengers / cat / day / green / line /
drivers). The effect is **anti-occupancy**: marked used “The” *less* in
the training openings, so unseen-after-The looks marked. It is not a
preference for ferry versus weather.

The remaining true positives are observed-token atoms, mainly dialogue
openings actually seen in train: `'"' → 'This'` (δ 3.22) then
`'"This' → ' is'` (δ 4.78), n=9; also `'Oh'`, `'Who'`, `'My'`.

The nine marked zeros are openings with **no** overlapping context at
indices 1–3: `After two and a`, `Closing is the` (all four library
draws), `Now in the second`, `While working on the`,
`Now a little after`. Zeros are abstentions, not sign errors.

Atom counts on this gate: **26** distinct (ctx, next) types; unseen-next
mass **34**, seen-next mass **33**. JSON: `atoms.json` in the transfer
directory.

## Frozen result (24 other 36×4 stems → 12×4)

| Method | Prompt wins | File AUC | marked `lr>0` | unmarked `lr≤0` | zeros M/U | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|---|---|---|
| poshits | **12/12** | **0.873** | **39/48** | **41/48** | 9/33 | 39/0 | 7/8 | 0.848 |
| **postokhits** | **12/12** | 0.694 | **16/48** | **48/48** | 32/44 | **16/0** | **0/4** | **1.000** |
| hits | 11/12 | 0.820 | 39/48 | 33/48 | 9/22 | 39/0 | 15/11 | 0.722 |
| tokhits | 11/12 | 0.674 | 16/48 | 45/48 | 32/39 | 16/0 | 3/6 | 0.842 |

`postokhits` among decided files is **perfect** on this gate
(16 TP, 0 FN, 0 FP, 4 TN). Prompt ranking stays **12/12**. Isolated
`lr>0` drops to **16/48** because The-Laplace true positives become
zeros. Nested Youden: 16/48 vs 48/48, spec **1.000**.

Do **not** sell 16/48 as beating 39/48. Quote both: 39/48 includes
occupancy Laplace; 16/48 is observed next-token only, precision 1.0 on
this gate. The 29/48 last-4 isolated-file headline is unchanged.

## In-domain 36×4 LOO

`--fit-prefix 4 --pos-bucket 1`, 36×4 leave-one-file-out, same opening
window:

| Method | Prompt wins | File AUC | marked `lr>0` | unmarked `lr≤0` | zeros M/U | decided tp/fn | decided fp |
|---|---|---|---|---|---|---|---|
| poshits | 34/36 | 0.935 | **131/144** | **132/144** | 8/89 | 131/5 | 12 |
| postokhits | 34/36 | 0.912 | **122/144** | **132/144** | 19/105 | 122/3 | 12 |

Only **9 of 131** in-domain poshits true positives were occupancy
Laplace. The extra true positives versus the OOD 16/48 are observed
continuations of repeated 36×4 topics, not The-ferry. The 12 unmarked
false positives stay after tokhits: they are observed-token errors, not
occupancy. Nested-by-stem Youden: poshits 121/144 vs 132/144;
postokhits 121/144 vs 139/144.

## Instance contrast

Same 4-token tables, `control-shuffled-30` openings
([key-free-contrast.md](key-free-contrast.md)):

| Method | control `lr>0` | public vs control |
|---|---|---|
| poshits | **0/48** | **12/12**, AUC **0.906** |
| postokhits | **0/48** | **12/12**, AUC 0.667 |

The 16 observed-token true positives are still this public instance.
Control files never get `lr > 0`. Public-vs-control AUC drops because
32 marked zeros tie with control zeros; quote **0/48**, not the 12/12
control-vs-unmarked prompt-mean artifact (zeros beating negative
unmarked LRs).

## What this is not

- Not a universal calibrated detector.
- Not key recovery. Tokhits only gates Laplace on next-token occupancy.
- Not a claim that 16/48 isolated-file is the headline. 39/48 remains
  the poshits number; tokhits explains it.
- Not a replacement of **10/12**, **29/48**, or **36/36**.
