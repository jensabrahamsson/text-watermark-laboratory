# Qwen 100×4 occupancy-free transfer → Qwen 12×4

Protocol: [research/PROTOCOL-isolated-qgen.md](../../research/PROTOCOL-isolated-qgen.md).
Frozen SHA **`3c0a5c9`**. `--model Qwen/Qwen2-1.5B-Instruct`.
`used_keys=false`. Local Hugging Face, not Dashscope.

| method | prompt wins | file auc | marked>0 | unmarked≤0 | nested Youden |
|---|---|---|---|---|---|
| poshits | **11/12** | 0.770 | **33/48** | **37/48** | **33/48 vs 38/48** |
| postokhits | **11/12** | 0.809 | **31/48** | **48/48** | **31/48 vs 48/48** (t≈0.022) |

Occupancy-free t=0 **31/48** is below openings coverage **37/48**.
Unmarked t=0 is **48/48**. Cross-corpus **31/48** > **25/48** does not
replace original-12 GPT-2 isolated sign. Do not sell **31/48**.
