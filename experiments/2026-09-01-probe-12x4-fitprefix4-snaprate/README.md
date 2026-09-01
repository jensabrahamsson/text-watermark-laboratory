# Table-free opening snap-rate (12×4 LOO, isolated)

`--fit-prefix 4 --methods snapleave,snapupset,snapmiss --skip-hashpool`.
Three unmarked-LM rank rows (generated tokens 1–3). `used_keys=false`.
Score is rate − 0.5 so threshold 0 is a majority.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | perm p |
|---|---|---|---|---|---|
| snapleave | 9/12 | 0.569 | 48/48 | 7/48 | 0.057 |
| **snapupset** | **7/12** | **0.501** | 24/48 | 20/48 | **0.55** |
| snapmiss | **10/12** | **0.707** | **21/48** | **41/48** | 0.0005 |

`snapupset` is chance: marked and unmarked leave the in-topk argmax at
the same rate (0.649 vs 0.653). `snapleave` majority vote is not a
detector. `snapmiss` ranks (off-mode continuation, not the tournament)
and is not 29/48. Nested FPR10 on snapleave / snapmiss is 0/48.

Write-up: [../../research/key-free-snaprate.md](../../research/key-free-snaprate.md).
