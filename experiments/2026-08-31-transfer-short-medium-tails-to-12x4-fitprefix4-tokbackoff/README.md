# 24 short + 12 medium + 12 tail-transplant → 12×4

`--fit-prefix 4 --pos-bucket 1`. `used_keys=false`.
Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

Train includes transplanted last paragraphs from the zero-producing
12×4 seeds. Not a new-topic detector.

`postokhits` **12/12**, isolated **30/48**, precision **1.000** among
decided. `postokbackoff` **12/12**, isolated **36/48**, precision
**1.000**, AUC **0.888**. Of the original nine zeros: night-bus and
both garden files are exact-context hits; all four library files score
only under backoff last-1 `' is' → ' the'`; both letter zeros remain.
Do not sell 30/48 or 36/48 as beating 39/48 occupancy, and do not
replace 10/12, 29/48, or 36/36.

| Method | Prompt wins | File AUC | marked `lr>0` | unmarked `lr≤0` | zeros M/U | decided tp | precision |
|---|---|---|---|---|---|---|---|
| poshits | 11/12 | 0.770 | 30/48 | **48/48** | 6/33 | 30 | 1.000 |
| postokhits | **12/12** | 0.832 | **30/48** | **48/48** | 18/43 | **30** | **1.000** |
| **postokbackoff** | **12/12** | **0.888** | **36/48** | **48/48** | 12/43 | **36** | **1.000** |
