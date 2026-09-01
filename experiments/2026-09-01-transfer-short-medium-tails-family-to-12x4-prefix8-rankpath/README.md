# 60-stem prefix-8 rankpath / postokbackoff → 12×4

Train pair-36x4 + long12x4 + tails12x4 + family12x4 (60 stems after
dropping the 12 test prompts). Score `2026-08-17-pair-12x4`.
`--fit-prefix 8 --pos-bucket 0`. `used_keys=false`.

Not leftover-only cascade. Eight generated tokens, so the first official
5-gram exists. Prefix-4 is shorter than `ngram_len=5`.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | precision |
|---|---|---|---|---|---|
| **postokbackoff** | **10/12** | **0.818** | **38/48** | **40/48** | 0.826 |
| rankpath | 9/12 | 0.674 | 30/48 | 35/48 | 0.698 |
| rankuni | 9/12 | 0.563 | 28/48 | 25/48 | 0.549 |

Prefix-4 postokbackoff on this train was **34/48 vs 48/48**, precision
1.0, combined **82/96**. Prefix-8 adds 4 true positives (station d4,
letter d3, office d1/d3) and 8 unmarked FPs. Combined **78/96**. Nested
FPR10 is 38/48 vs 42/48. Do not sell 38/48 as beating poshits **39/48**
or replacing **29/48**.

Letter d2 (`Now in the second I'm just getting ready for bed.`) stays
`lr<0` despite official prefix-5 mean **0.733**. Harbour covered-negatives
stay negative. Prefix-8 rankpath does not beat prefix-4 rankpath.

Write-up: [../../research/key-free-cascade.md](../../research/key-free-cascade.md).
