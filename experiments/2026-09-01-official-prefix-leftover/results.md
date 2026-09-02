# Official prefix scores on leftover isolated files

Reference check with `public-deepmind-30`. Uses keys / g-values.
Not a key-free reader. Prefix 4 is shorter than `ngram_len=5` and
cannot be scored. leftover = eight positive-when cascade misses.

| prefix | leftover marked mean | >0.55 | other marked mean | >0.55 | unmarked mean | >0.55 |
|---|---|---|---|---|---|---|
| 5 | 0.637 | 6/8 | 0.633 | 39/40 | 0.481 | 14/48 |
| 8 | 0.625 | 7/8 | 0.621 | 34/40 | 0.490 | 5/48 |
| 16 | 0.627 | 8/8 | 0.626 | 40/40 | 0.496 | 3/48 |
| 32 | 0.633 | 8/8 | 0.627 | 40/40 | 0.500 | 0/48 |
| 64 | 0.626 | 8/8 | 0.623 | 40/40 | 0.501 | 0/48 |
| 128 | 0.621 | 8/8 | 0.622 | 40/40 | 0.500 | 0/48 |

Leftover files are officially marked at the same strength as the
other 40. Isolated key-free misses are not unmarked openings.
Letter d2/d3 prefix-5 means are 0.733 / 0.767 (one 5-gram).
Office d1/d3 prefix-5 is 0.500; prefix-8 is 0.633.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).

