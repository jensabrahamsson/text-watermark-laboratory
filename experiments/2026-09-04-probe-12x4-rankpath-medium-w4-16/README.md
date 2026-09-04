# gpt2-medium-LM rankpath body window [4:16) on original 12

Frozen in [PROTOCOL-isolated-rankpath-mbody.md](../../research/PROTOCOL-isolated-rankpath-mbody.md)
(`3ea80e4`). `--model gpt2-medium --methods rankpath --fit-prefix 16
--pos-bucket 1 --skip-hashpool --windows 4:16`. The frozen slice is
`window-4-16/`: ranking **9/12**, isolated **27/48 vs 28/48**, nested
**18/48 vs 31/48**, AUC **0.580**. `used_keys=false`. The unwindowed
fit-prefix-16 file score **11/12** / **25/48 vs 31/48** is not that
slice. Do not sell **27/48** or unwindowed **25/48** as replacing
**25/48**.
