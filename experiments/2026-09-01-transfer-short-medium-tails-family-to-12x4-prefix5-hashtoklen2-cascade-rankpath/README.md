# Robust hashed 5-gram + prefix-4 rankpath is not complementary

Count channel: 60-stem prefix-5 `hashtoklen2` (`min_count=2` on the
same exact-length tables as `hashtoklen`; precision 1.0 among
decided). Fallback: saved prefix-4 opening rankpath from
[../2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/](../2026-08-31-transfer-short-medium-tails-family-to-12x4-fitprefix4-cascade-rankpath-prefix4/).
Rebound with `rebind_count_channel`. No new GPT-2 forwards.
`used_keys=false`. Mixed AUC is not a detector.

| Rule | marked>0 | unmarked≤0 | count decided | fallback TP |
|---|---|---|---|---|
| hashtoklen2 `n_used>0` | **10/48** | **48/48** | 10 marked, precision 1.0 | — |
| **coverage** | **28/48** | **40/48** | 10 | 18/38 |

Coverage cascade **28/48 vs 40/48** copies standalone 60-stem prefix-4
rankpath. All 10 hashtoklen2 true positives are already rankpath true
positives. Combined **68/96** vs hashtoklen cascade **70/96** vs
prefix-4 count **82/96**. Leftover eight stay misses (0/8). Do not
sell 28/48.

`hashtoklen2` is **not** in `HASH_CASCADE_READERS`. Do not add it as a
cascade count channel on this number. `--cascade hashtoklen` remains
the occupancy-free hashed 5-gram count channel
(**33/48 vs 37/48**), and even that is not leftover fill-in.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
