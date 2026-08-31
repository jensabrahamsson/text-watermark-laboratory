# GPT-2 36×4 → DistilGPT2, matched 4-token poshits

`--fit-prefix 4 --pos-bucket 1`. Same tokenizer. `used_keys=false`.

| Method | Prompt wins | File AUC | t=0 |
|---|---|---|---|
| hits | 7/12 | 0.551 | 15/48 vs 30/48 |
| poshits | 8/12 | 0.582 | 13/48 vs 38/48 |
| first | 10/12 | 0.637 | 5/48 vs 43/48 |

The GPT-2 4-token 12/12 / 0.873 gate does not copy to Distil. First
ranks 10/12 with almost no isolated recall.
