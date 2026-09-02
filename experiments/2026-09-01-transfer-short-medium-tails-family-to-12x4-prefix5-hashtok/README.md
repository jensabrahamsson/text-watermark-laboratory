# 60-stem prefix-5 hashpool vs hashtok → 12×4

Official 5-gram grain (`--fit-prefix 5`, last-4 context). Train is the
60-stem mix (36×4 + long + tails + family); overlap `drop-from-train`.
`used_keys=false`. `hashtok` is hashpool that skips a hash unless the
observed next token appeared in that bucket.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | precision |
|---|---|---|---|---|---|
| hashpool (occupancy) | **11/12** | 0.841 | **34/48** | **34/48** | 0.708 |
| **hashtok** | 9/12 | 0.761 | **30/48** | **36/48** | 0.714 |
| hybrid | 9/12 | 0.808 | 31/48 | 33/48 | 0.674 |
| postokhits | **10/12** | 0.762 | **30/48** | **45/48** | **0.909** |
| postokbackoff2 | **12/12** | 0.642 | 15/48 | 46/48 | 0.882 |

Hashpool never abstains (0/48 zeros). Its four extra marked signs
versus hashtok are harbour d2/d3/d4 and **letter d2**. Those four
hashtok scores are ≤0. Letter d2 is occupancy on every prefix-5
position, including the official 5-gram `Now in the second I`
(8/8 hashes unseen; `n_used=0`). hybrid copies hashpool there.

hashtok's 30 true positives are **exactly** postokhits' 30. Feature
hashing did not recover an observed continuation that exact last-k
missed. It did add unmarked false positives (12 vs 3).

Do not sell 34/48 or 30/48 as beating poshits **39/48** or replacing
**29/48**. Nested hashtok Youden is **26/48 vs 42/48**.

JSON: `occupancy-trace.json` (`used_keys=false`). Frozen buckets:
`tables-hashpool/` (`indicate score --score-mode hashtok`).
Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
