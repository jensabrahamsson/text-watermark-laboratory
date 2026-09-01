# Occupancy-free hashed 5-gram + prefix-4 rankpath cascade

Count channel: 60-stem prefix-5 `hashtoklen` (official 5-gram slot
only). Fallback: saved prefix-4 opening rankpath from
[../2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/](../2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/).
Rebound with `rebind_count_channel`. No new GPT-2 forwards.
`used_keys=false`. Mixed AUC is not a detector.

| Rule | marked>0 | unmarked≤0 | count decided | fallback TP |
|---|---|---|---|---|
| hashtoklen `n_used>0` | **21/48** | **45/48** | 21 marked, precision 0.875 | — |
| **coverage / positive-when** | **33/48** | **37/48** | 21 | 12/27 |

hashtoklen has no covered-negative marked files, so `--cascade-when
positive` equals coverage. Combined **70/96**. Count `postokbackoff`
on the same 60-stem prefix-4 split is **82/96**. Leftover eight stay
misses. Do not sell 33/48 as beating poshits **39/48** or replacing
**29/48**.

`--cascade hashtoklen --cascade-fallback rankpath` is the first-class
command. This directory reuses saved rank-path rows.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
