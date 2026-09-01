# 60-stem prefix-4 exact-length hashed backoff → 12×4

Published opening (generated tokens 0–3). Same 60-stem train as
prefix-5 `hashtoklen`. `hashtoklen` with `context_len=4` needs a
4-token context, which a 4-token prefix never has (max ctx_len=3).
`used_keys=false`.

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| hashtok | 10/12 | 0.844 | **35/48** | 39/48 | **33/48 vs 45/48** | 0.795 |
| **hashtoklen** | 12/12† | 0.500 | **0/48** | 48/48 | **0/48 vs 48/48** | — |
| **hashtoklenbackoff** | 11/12 | 0.826 | **35/48** | 38/48 | **35/48 vs 40/48** | 0.778 |
| **hashtoklenbackoff2** | 9/12 | 0.732 | 30/48 | 42/48 | 30/48 vs 43/48 | 0.833 |

† All zeros. `pair_marked_wins` counts ties as prompt wins. Not a ranking.

Exact backoff on this window does **not** hurt the way mixed hashed
backoff did (31/48). Order-4 never fires; last-3/2/1 are legal n-grams.
Keep prefix-4 `hashtok` as the occupancy-free hashed opening reader.
Do not sell 35/48 as beating poshits **39/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
