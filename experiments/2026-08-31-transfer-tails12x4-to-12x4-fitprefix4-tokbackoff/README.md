# Tail-transplant train → original 12×4

Train 12 tails12 stems, score original 12×4.
`--fit-prefix 4 --pos-bucket 1`. `used_keys=false`.
Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

This is **not** new-topic OOD. The train prompts reuse last paragraphs
from night-bus / library / letter / garden.

`postokhits` **12/12**, isolated **10/48**, precision **1.000**. That
covers night-bus `After two and a` and both garden `Now a little after`
files. Library `Closing is the` and both letter zeros stay zero.

`postokbackoff` **12/12**, isolated **23/48**, precision **1.000**. The
extra files include all four library draws via last-1 `' is' → ' the'`,
not via a Closing opening. Letter `Now in the second` / `While working
on the` stay zero. Do not sell 23/48 as beating 39/48.

| Method | Prompt wins | File AUC | marked `lr>0` | unmarked `lr≤0` | zeros M/U | decided tp | precision |
|---|---|---|---|---|---|---|---|
| poshits | 8/12 | 0.495 | 10/48 | **48/48** | 22/41 | 10 | 1.000 |
| postokhits | **12/12** | 0.604 | **10/48** | **48/48** | 38/48 | **10** | **1.000** |
| **postokbackoff** | **12/12** | 0.740 | **23/48** | **48/48** | 25/48 | **23** | **1.000** |
