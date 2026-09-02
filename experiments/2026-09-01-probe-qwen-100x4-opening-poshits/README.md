# Qwen Phase B lock B — opening poshits

Native Qwen2-1.5B-Instruct, `--methods poshits --fit-prefix 4 --pos-bucket 1`.
`used_keys=false`. Prompt ranking **95/100**, AUC **0.873**, isolated
**333/400 vs 308/400**. Nested-by-stem Youden **331/400 vs 347/400**.
Drop from GPT-2 Phase A lock B (**100/100**) is **5**. Not **25/48**.

`--rankpath` extras in the sibling directory are not this lock.
