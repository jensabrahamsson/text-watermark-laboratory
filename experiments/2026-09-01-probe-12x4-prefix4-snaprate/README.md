# Table-free prefix-4 snap-rate (12×4 LOO, isolated)

`--fit-prefix 5 --methods snapleave,snapupset,snapmiss --skip-hashpool`.
Four unmarked-LM rank rows (generated tokens 1–4). `used_keys=false`.
Score is rate − 0.5 so threshold 0 is a majority.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | perm p |
|---|---|---|---|---|---|
| snapleave | 8/12 | 0.601 | 42/48 | 10/48 | 0.029 |
| **snapupset** | **6/12** | **0.501** | 25/48 | 14/48 | 0.23 |
| snapmiss | 11/12 | 0.717 | 2/48 | 46/48 | 0.0005 |

Same story as the three-row opening: `snapupset` is chance. Prefix-4
miss rates sit below 0.5, so majority-miss t=0 is 2/48. Nested Youden
on snapmiss is 27/48 vs 39/48. Not 29/48.

Write-up: [../../research/key-free-snaprate.md](../../research/key-free-snaprate.md).
