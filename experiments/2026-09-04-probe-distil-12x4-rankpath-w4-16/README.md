# Distil native rankpath body window [4:16) on Distil 12

Frozen in [PROTOCOL-isolated-rankpath-d12body.md](../../research/PROTOCOL-isolated-rankpath-d12body.md)
(`468a66b`). `--model distilgpt2 --methods rankpath --fit-prefix 16
--pos-bucket 1 --skip-hashpool --windows 4:16`. The frozen slice is
`window-4-16/`: ranking **9/12**, isolated **25/48 vs 30/48**, nested
**33/48 vs 21/48** (negative threshold), AUC **0.630**.
`used_keys=false`. The unwindowed fit-prefix-16 file score **9/12** /
**26/48 vs 26/48** is not that slice. Equality with **25/48** is not a
win. Do not sell **25/48** or nested **33/48** as replacing **25/48**.
