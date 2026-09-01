# DistilGPT2 in-domain prefix-5 occupancy-free hashed LOO

Same 12 Grok seeds, Distil generator, GPT-2 tokenizer. Official
`score` on this pile is **12/12**. Native Distil opening rankpath is
chance (**8/12**, AUC 0.579). `--fit-prefix 5`. `used_keys=false`.
Tokenizer is GPT-2 (shared).

| Method | Prompt | File AUC | marked>0 | unmarked≤0 | nested Youden | precision |
|---|---|---|---|---|---|---|
| postokhits | 10/12 | 0.633 | 18/48 | 46/48 | 16/48 vs 46/48 | 0.900 |
| hashtok | 8/12 | 0.655 | 18/48 | 42/48 | 18/48 vs 46/48 | 0.750 |
| **hashtoklen** | 12/12† | 0.573 | **7/48** | **48/48** | **7/48 vs 48/48** | 1.000 |
| hashtoklenbackoff | 8/12 | 0.592 | 22/48 | 35/48 | 17/48 vs 42/48 | 0.629 |

† Same zeros-and-ties grain as GPT-2 in-domain hashtoklen.

Sparse official-grain hashing on Distil's own twins matches GPT-2
in-domain density (**7/48**, precision 1.0 among decided). It is not
the official 12/12 lamp and not a Distil rankpath substitute.
Do not sell 7/48 as beating **29/48**.

Write-up: [../../research/key-free-hashtok.md](../../research/key-free-hashtok.md).
