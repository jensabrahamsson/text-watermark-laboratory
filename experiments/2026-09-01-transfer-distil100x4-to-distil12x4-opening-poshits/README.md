# Distil 100×4 occupancy-free transfer → Distil 12×4

Protocol: [research/PROTOCOL-isolated-dgen.md](../../research/PROTOCOL-isolated-dgen.md).
Frozen SHA **`6bb95a6`**. `--model distilgpt2`. `used_keys=false`.

| method | prompt wins | file auc | marked>0 | unmarked≤0 | nested Youden |
|---|---|---|---|---|---|
| poshits | **9/12** | 0.639 | **25/48** | **25/48** | **47/48 vs 14/48** (negative t) |
| postokhits | **9/12** | 0.660 | **16/48** | **39/48** | **48/48 vs 12/48** (negative t) |

Occupancy-free t=0 **16/48** equals opening coverage **16/48**. It does
not beat **25/48**. Distil→GPT-2 occupancy-free **22/48** used different
test files. Nested 48/48 is a negative train threshold. Do not sell
**16/48**, **25/48**, or **48/48**.
