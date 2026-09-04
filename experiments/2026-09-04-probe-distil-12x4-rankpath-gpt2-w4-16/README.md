# GPT-2-small LM rankpath body window [4:16) on Distil 12

Frozen in [PROTOCOL-isolated-rankpath-g2dbody.md](../../research/PROTOCOL-isolated-rankpath-g2dbody.md)
(`08b89ee`). `--model gpt2 --methods rankpath --fit-prefix 16
--pos-bucket 1 --skip-hashpool --windows 4:16`. The frozen slice is
`window-4-16/`: ranking **4/12**, isolated **26/48 vs 21/48**, nested
**22/48 vs 17/48** (negative threshold), AUC **0.495**.
`used_keys=false`. The unwindowed fit-prefix-16 file score **5/12** /
**28/48 vs 21/48** is not that slice. Do not sell **26/48** or **28/48**
as replacing **25/48**.
