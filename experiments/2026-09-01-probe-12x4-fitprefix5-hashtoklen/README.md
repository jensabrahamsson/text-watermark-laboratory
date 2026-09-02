# In-domain 12×4 LOO exact hashed 5-grams

Leave-one-prompt-out on the published 12×4 twins. `--fit-prefix 5`.
`used_keys=false`. Eleven other prompts, not the 60-stem train.

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| postokhits | 12/12 | 0.772 | **23/48** | **48/48** | 23/48 vs 48/48 | 1.000 |
| hashtok | 10/12 | 0.737 | 24/48 | 42/48 | 22/48 vs 44/48 | 0.800 |
| **hashtoklen** | 12/12† | 0.573 | **7/48** | **48/48** | **7/48 vs 48/48** | 1.000 |
| hashtoklenbackoff | 10/12 | 0.716 | 28/48 | 37/48 | 23/48 vs 41/48 | 0.718 |

† Ranking of 41 marked zeros plus 7 decided files. Not isolated-file density.

Letter d2 (`Now in the second I`) still `lr=0`. Harbour d2
(`The ferry was over ,`) is already a TP here: the comma collision
does not need the 60 extra stems. Unique openings stay unseen.
Do not sell 7/48 as beating **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
