# GPT-2-small LM rankpath body window [4:16) on gpt2-medium 12

Frozen in [PROTOCOL-isolated-rankpath-g2mbody.md](../../research/PROTOCOL-isolated-rankpath-g2mbody.md)
(`e677a6c`). `--model gpt2 --methods rankpath --fit-prefix 16
--pos-bucket 1 --skip-hashpool --windows 4:16`. The frozen slice is
`window-4-16/`: ranking **8/12**, isolated **28/48 vs 30/48**, nested
**25/48 vs 28/48**, AUC **0.624**. `used_keys=false`. The unwindowed
fit-prefix-16 file score **8/12** / **25/48 vs 31/48** is not that
slice. Do not sell **28/48** or unwindowed **25/48** as replacing
**25/48**.
