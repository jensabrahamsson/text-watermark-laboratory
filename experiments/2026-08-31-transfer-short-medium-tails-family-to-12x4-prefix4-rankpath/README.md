# 60-stem prefix-4 rankpath, standalone isolated-file reader

Train pair-36x4 + long12x4 + tails12x4 + family12x4 (60 stems after
dropping the 12 test prompts). Score `2026-08-17-pair-12x4`.
`--fit-prefix 5 --pos-bucket 0`. Four unbucketed rank symbols.
Not leftover-only cascade. `used_keys=false`.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | precision |
|---|---|---|---|---|---|
| rankpath | **10/12** | **0.770** | **28/48** | **40/48** | 0.778 |
| rankuni | 11/12 | 0.761 | 39/48 | 32/48 | 0.709 |

24-short prefix-4 was **11/12**, **25/48 vs 43/48**. Combined accuracy
here is **68/96**, the same 25+43. Extra stems add 3 TPs and 3 FPs.
Nested FPR10 is 11/48 vs 47/48. Do not sell 28/48 as beating **29/48**
or rankuni 39/48 as beating poshits **39/48** (16 unmarked FPs).

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
