# Distil 100×4 occupancy-free transfer → original 12×4

Protocol: [research/PROTOCOL-isolated-xgen.md](../../research/PROTOCOL-isolated-xgen.md).
Frozen SHA **`8e33445`**. `--model distilgpt2`. `used_keys=false`.

| method | prompt wins | file auc | marked>0 | unmarked≤0 | nested Youden |
|---|---|---|---|---|---|
| poshits | **11/12** | 0.760 | **39/48** | **24/48** | **47/48 vs 11/48** (negative t) |
| postokhits | **10/12** | 0.717 | **22/48** | **43/48** | **47/48 vs 7/48** (negative t) |

Occupancy-free t=0 **22/48** beats GPT-2 lock B occupancy-free **16/48**
and does not beat **25/48**. Nested 47/48 is a negative train threshold.
Do not sell **22/48**, **39/48**, or **47/48**.
