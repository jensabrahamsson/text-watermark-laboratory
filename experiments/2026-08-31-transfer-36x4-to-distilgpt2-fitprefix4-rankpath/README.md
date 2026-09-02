# GPT-2 36×4 rankpath → Distil 12×4 (GPT-2 LM)

Train 24 new GPT-2 stems, score DistilGPT2 12×4. Ranks come from the
**GPT-2** unmarked LM (wrong LM for Distil’s tournament). Shared BPE.
`--fit-prefix 4 --pos-bucket 1`. `used_keys=false`.

| Method | Prompt wins | File AUC | marked>0 | unmarked≤0 | perm p |
|---|---|---|---|---|---|
| rankpath | 9/12 | 0.636 | 21/48 | 34/48 | 0.017 |
| rankuni | 5/12 | 0.475 | 18/48 | 28/48 | 0.645 |

Weak ranking, not a Distil reader. Token-identity hits on this split
is **5/12**, AUC **0.462**. Native Distil rankpath (right LM) is chance.
Do not sell 9/12 as Distil transfer.

Write-up: [../../research/key-free-rankpath.md](../../research/key-free-rankpath.md).
