# Transfer hashtok seed sweep: n=8 win is not stable

24 new 36×4 stems → original 12×4 files. Occupancy-free `hashtok`,
last-4, full files, `drop-from-train`. Nested Youden / 10% FPR from
leave-one-prompt-out on the 24 training stems. Feature-hash `seed` is
not SynthID `hash_iv`. Default mixer seed **20260831** is the locked
n=8 transfer: **11/12**, **29/48 vs 35/48**, nested **17/48 vs 46/48**.

This sweep asks whether that n=8 win is a width law or a lucky mixer,
the same question as the in-domain n=2 seed sweep.

| n_hashes | seed | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | nested FPR10 |
|---|---|---|---|---|---|---|---|
| 8 | **20260831** | **11/12** | 0.707 | 29/48 | 35/48 | 17/48 vs 46/48 | 17/48 vs 46/48 |
| 8 | 0 | 10/12 | 0.709 | 27/48 | 36/48 | 14/48 vs 46/48 | 14/48 vs 46/48 |
| 8 | 7 | 10/12 | 0.705 | 25/48 | **37/48** | 16/48 vs 45/48 | 16/48 vs 45/48 |
| 2 | **20260831** | 10/12 | 0.704 | 29/48 | 32/48 | 17/48 vs 44/48 | 13/48 vs 46/48 |
| 2 | 0 | 9/12 | 0.669 | 29/48 | 29/48 | 15/48 vs 41/48 | 13/48 vs 45/48 |
| 2 | 7 | 9/12 | **0.740** | 29/48 | 36/48 | **19/48 vs 47/48** | 16/48 vs 47/48 |

Default seed 20260831 is the best n=8 prompt ranking here (**11/12**).
Other n=8 seeds drop t=0 marked recall to 27 and 25. n=2 seed 7 nested
**19/48 vs 47/48** beats the advertised n=8 default on nested recall
and spec, with worse prompt ranking (9/12). Letter d2 flips at seed 0
for both widths.

The 24→12 “n=8 wins” table is seed-confounded, as was in-domain n=2.
Keep the published protocol frozen (`n_hashes=8`, seed `20260831`).
Do **not** fish a seed. Do **not** sell 19/48, 17/48, or 14/48 as
beating poshits **39/48** or replacing **29/48**. Transfer t=0 29/48
is not the headline hard last-4 **29/48**.

`run_transfer(..., hash_seed=)` / `rotate_hashtok(..., seed=)`.
Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
