# GPT-2 60-stem hashed 5-grams → DistilGPT2 12×4

Same tokenizer as GPT-2. Train 60 GPT-2 stems, drop the 12 test
prompts, score Distil 12×4 prefix-5. `used_keys=false`.

Earlier GPT-2 36×4 **hits** on this Distil sample is **5/12**, AUC
**0.462**. Official Distil lamp is **12/12**. Native Distil rankpath
is chance.

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | perm p |
|---|---|---|---|---|---|---|
| hashtok | 7/12 | 0.615 | 24/48 | 37/48 | 11/48 vs 41/48 | 0.085 |
| **hashtoklen** | 9/12 | **0.571** | **10/48** | 43/48 | **10/48 vs 43/48** | 0.041 |
| hashtoklenbackoff | 4/12 | **0.470** | 17/48 | 26/48 | 9/48 vs 37/48 | 0.794 |
| postokhits | 9/12 | 0.591 | 10/48 | 42/48 | 10/48 vs 43/48 | 0.017 |

Occupancy-free official-grain hashing does **not** become a Distil
detector when the tables were fit on GPT-2 watermarked openings.
hashtoklenbackoff is chance. Same tokenizer is not the same generator
footprint. Do not sell 10/48 as beating **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
