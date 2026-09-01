# Official prefix scores on leftover isolated files

Reference check with `public-deepmind-30`. This path uses detector keys
and g-values. **Not a key-free reader.** Prefix 4 is shorter than
`ngram_len=5` and cannot be scored. leftover = the eight
`--cascade-when positive` misses (count nonpositive and prefix-4
rankpath ≤ 0).

| prefix | leftover marked mean | >0.55 | other marked mean | >0.55 | unmarked mean | >0.55 |
|---|---|---|---|---|---|---|
| 5 | 0.637 | 6/8 | 0.633 | 39/40 | 0.481 | 14/48 |
| 8 | 0.625 | 7/8 | 0.621 | 34/40 | 0.490 | 5/48 |
| 16 | 0.627 | **8/8** | 0.626 | **40/40** | 0.496 | 3/48 |
| 32 | 0.633 | 8/8 | 0.627 | 40/40 | 0.500 | 0/48 |
| 128 | 0.621 | 8/8 | 0.622 | 40/40 | 0.500 | 0/48 |

The leftover eight are officially marked at the same strength as the
other 40. Isolated key-free misses are not unmarked openings.

Letter d2/d3 (`Now in the second`, `While working on the`) prefix-5
means are **0.733 / 0.767** (one 5-gram). Office d1/d3
(`The printer worked.`) prefix-5 is 0.500; prefix-8 is 0.633. In-domain
opening rankpath already signs 7/8 of these files; only letter d2
misses. The OOD 60-stem prefix-4 reader misses all eight.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).
