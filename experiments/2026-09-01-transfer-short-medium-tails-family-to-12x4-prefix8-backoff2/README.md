# 60-stem prefix-8 postokbackoff2 → 12×4

Same train as prefix-8 `postokbackoff`, but `min_order=2` (no last-1
English). `used_keys=false`.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | precision |
|---|---|---|---|---|---|
| postokbackoff (last-1 allowed) | 10/12 | 0.818 | **38/48** | **40/48** | 0.826 |
| **postokbackoff2** | **12/12** | 0.674 | **18/48** | **46/48** | 0.900 |

**20 of 38** prefix-8 backoff true positives are last-1 only. The four
prefix-4 zeros that prefix-8 backoff signs (station d4, letter d3,
office d1/d3) are all last-1 punctuation (`',' → ' "'`, `',' → ' my'`,
`'.' → ' The'`). They are not official 5-grams. `postokbackoff2`
abstains on all four and on letter d2.

Do not sell 18/48 as beating **29/48** or poshits **39/48**. Keep
prefix-4 `postokbackoff` when the high-precision last-1 channel is the
point (**34/48 vs 48/48**). Last-2+ is the honest overlap floor.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).
