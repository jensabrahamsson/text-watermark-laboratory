# In-domain hashtok OR indicate is not a detector

Saved leave-one-prompt-out holdouts only. Hard last-4 `indicate`
(`instance=key-free-counts`, **29/48**) versus occupancy-free full-file
`hashtok` (**33/48**). No new GPT-2. Still no keys.

Complementary true positives exist. OR at t=0 looks like poshits
**39/48** on the TP side only. Combined **51/96** is worse than
indicate **52/96**. Honest nested fusion throws the extra TPs away.

| Rule | marked>0 | unmarked≤0 | combined |
|---|---|---|---|
| indicate | **29/48** | 23/48 | **52/96** |
| hashtok | **33/48** | 22/48 | 55/96 |
| **OR t=0** | **39/48** | **12/48** | **51/96** |
| nested 2D Youden OR | 37/48 | 18/48 | 55/96 |
| LDA stack t=0 | 28/48 | 27/48 | 55/96 |
| LDA nested-by-stem | **21/48** | **37/48** | 58/96 |
| max nested-by-stem | 21/48 | 39/48 | 60/96 |
| postokhits then hashtok | 35/48 | 22/48 | 57/96 |
| postokhits standalone | 24/48 | **45/48** | **69/96** |

hashtok recovers 10 of 19 indicate misses (harbour d1, night-bus d1,
market d3, kitchen d3, station d1/d2, office d1, garden d2/d3/d4).
Indicate recovers 6 of 15 hashtok misses (library d1/d3/d4, market d1,
station d4, rain d1). Both miss 9 files, including letter d2/d3/d4.

Do **not** sell 39/48. Nested LDA is not leftover fill-in and does not
replace **29/48**. `rotate_score_stack` on hits+hashpool remains the
published 11/12 stack; this is not a 12/12 ensemble.

JSON: [complement.json](complement.json).
Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
