# Distil LM rankpath body window [4:16) on gpt2-medium 12

Frozen in [PROTOCOL-isolated-rankpath-d2mbody.md](../../research/PROTOCOL-isolated-rankpath-d2mbody.md)
(`1b4c541`). `--model distilgpt2 --methods rankpath --fit-prefix 16
--pos-bucket 1 --skip-hashpool --windows 4:16`. The frozen slice is
`window-4-16/`: ranking **11/12**, isolated **25/48 vs 33/48**, nested
**36/48 vs 16/48** (negative threshold), AUC **0.646**.
`used_keys=false`. The unwindowed fit-prefix-16 file score **11/12** /
**33/48 vs 33/48** is not that slice. Equality with **25/48** is not a
win. Do not sell **25/48** as replacing **25/48**.
