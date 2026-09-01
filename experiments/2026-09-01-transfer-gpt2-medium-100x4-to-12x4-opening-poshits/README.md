# gpt2-medium 100×4 occupancy-free transfer → original 12×4

Protocol: [research/PROTOCOL-isolated-mgen.md](../../research/PROTOCOL-isolated-mgen.md).
Frozen SHA **`cc9c4ca`**. Named **`883532b`**. `--model gpt2-medium`.
`used_keys=false`.

| method | prompt wins (strict) | file auc | marked>0 | unmarked≤0 | nested Youden |
|---|---|---|---|---|---|
| poshits | **12/12** | 0.870 | **39/48** | **41/48** | **15/48 vs 48/48** |
| postokhits | **7/12** (5 ties) | 0.715 | **16/48** | **48/48** | **15/48 vs 48/48** |

Occupancy-free t=0 **16/48** equals opening coverage **16/48** and GPT-2
lock B occupancy-free **16/48**. It does not beat **25/48**. Nested 15/48
is a high train threshold. Do not sell **16/48**, **39/48**, **7/12**, or
**15/48**.
