# gpt2-medium LM rankpath body window [4:16) on Distil 12

Frozen in [PROTOCOL-isolated-rankpath-m2dbody.md](../../research/PROTOCOL-isolated-rankpath-m2dbody.md)
(`a550cb6`). `--model gpt2-medium --methods rankpath --fit-prefix 16
--pos-bucket 1 --skip-hashpool --windows 4:16`. The frozen slice is
`window-4-16/`: ranking **9/12**, isolated **32/48 vs 25/48**, nested
**21/48 vs 31/48**, AUC **0.626**. `used_keys=false`. The unwindowed
fit-prefix-16 file score **9/12** / **28/48 vs 31/48** is not that
slice. Do not sell **32/48** or unwindowed **28/48** as replacing
**25/48**.
