# 60-stem prefix-4 hashed backoff → 12×4

Published opening window (generated tokens 0–3). Same 60-stem train.
`used_keys=false`.

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashpool | 10/12 | 0.887 | **38/48** | 37/48 | **35/48 vs 46/48** | 0.776 |
| **hashtok** | 10/12 | 0.844 | **35/48** | 39/48 | **33/48 vs 45/48** | 0.795 |
| hashtokbackoff | 10/12 | 0.780 | 31/48 | 33/48 | 31/48 vs 42/48 | 0.674 |
| hashtokbackoff2 | 10/12 | 0.760 | 31/48 | 33/48 | 31/48 vs 42/48 | 0.674 |
| postokbackoff | 10/12 | 0.800 | 34/48 | 43/48 | 34/48 vs 45/48 | 0.872 |
| postokbackoff2 | 12/12 | 0.642 | 15/48 | 46/48 | 15/48 vs 46/48 | 0.882 |

Hashpool's three extra TPs versus hashtok are occupancy. Shrinking
last-k across hashed orders **hurts** this window (31/48, 15 FPs)
relative to plain hashtok. Keep prefix-4 `hashtok` when the hashed
reader should skip empty cells; keep `postokbackoff` when exact
overlap precision is the point. Do not sell 38/48 or 35/48 as beating
poshits **39/48** (that 39/48 is `--pos-bucket 1` occupancy) or
replacing **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
