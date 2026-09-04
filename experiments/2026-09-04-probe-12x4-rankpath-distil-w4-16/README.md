# Distil-LM rankpath body window [4:16) on original 12

Frozen in [PROTOCOL-isolated-rankpath-dbody.md](../../research/PROTOCOL-isolated-rankpath-dbody.md)
(`68b0514`). `--model distilgpt2 --methods rankpath --fit-prefix 16
--pos-bucket 1 --skip-hashpool --windows 4:16`. The frozen slice is
`window-4-16/`: ranking **6/12**, isolated **24/48 vs 23/48**, nested
**32/48 vs 19/48** (negative threshold), AUC **0.447**.
`used_keys=false`. The unwindowed fit-prefix-16 file score **8/12** /
**23/48 vs 32/48** is not that slice. Do not sell **24/48** as replacing
**25/48**.
