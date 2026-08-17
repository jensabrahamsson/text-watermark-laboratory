# 2026-08-17 — indicate rotate hold-out (12×4, last-4)

Single-text key-free indicator. Leave one *prompt* out, fit last-4 count tables
on the other eleven, score every held file alone. Extra samples of the held
prompt never enter the fit.

Twins: [`../2026-08-17-pair-12x4/`](../2026-08-17-pair-12x4/).
`used_keys=false`. Not `detector_mean`. Not Claude.

```bash
python -m text_watermark_tools indicate holdout experiments/2026-08-17-pair-12x4 \
  --rotate --context-len 4 --out-dir experiments/2026-08-17-indicate-holdout-12x4
```

## Result

| Grain | Count |
|---|---|
| Prompts (mean of 4 samples) | **10/12** marked mean LR > unmarked |
| Sample pairs | **30/48** marked file > its unmarked twin |
| One marked file, `lr>0` | **29/48** |
| One unmarked file, `lr≤0` | **23/48** |
| Both signs right on a pair | **15/48** |

Misses at prompt grain: **station**, **office**. Same two as
[`../2026-08-17-blind-12x4-k4/`](../2026-08-17-blind-12x4-k4/).

Mean LR across 48 marked files: **+0.033** (min −0.121, max +0.259).
Mean LR across 48 unmarked files: **−0.003** (min −0.110, max +0.173).

The tournament still works when you average a prompt. One new file against
frozen tables is a weak tilt around zero. Not a lamp you point at one
paragraph. `experiments/indicator-gpt2/` is fit on *all* 12 prompts — do not
read an in-sample `indicate score` on these twins as this hold-out.

## Per prompt (mean of 4 samples)

| Stem | Marked LR | Unmarked LR | Marked higher | marked `lr>0` | unmarked `lr≤0` |
|---|---|---|---|---|---|
| 01-harbour | +0.025 | −0.011 | yes | 3/4 | 2/4 |
| 02-night-bus | −0.012 | −0.051 | yes | 1/4 | 3/4 |
| 03-library | +0.007 | −0.047 | yes | 3/4 | 3/4 |
| 04-market | +0.060 | +0.018 | yes | 3/4 | 1/4 |
| 05-kitchen | +0.121 | +0.019 | yes | 3/4 | 2/4 |
| 06-station | +0.015 | +0.025 | no | 2/4 | 1/4 |
| 07-rain | +0.112 | −0.000 | yes | 4/4 | 2/4 |
| 08-letter | +0.018 | −0.031 | yes | 1/4 | 2/4 |
| 09-workshop | +0.110 | +0.073 | yes | 4/4 | 0/4 |
| 10-office | −0.047 | +0.019 | no | 2/4 | 2/4 |
| 11-garden | −0.024 | −0.047 | yes | 0/4 | 3/4 |
| 12-ferry-queue | +0.009 | −0.007 | yes | 3/4 | 2/4 |
