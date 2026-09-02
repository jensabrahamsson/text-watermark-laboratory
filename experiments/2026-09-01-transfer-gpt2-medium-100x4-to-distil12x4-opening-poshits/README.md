# gpt2-medium 100×4 → Distil 12×4 occupancy-free

Protocol: [research/PROTOCOL-isolated-xsize.md](../../research/PROTOCOL-isolated-xsize.md).

Train: `../2026-09-01-pair-gpt2-medium-100x4/`. Test:
`../2026-08-31-pair-distilgpt2-12x4/`. Same BPE. Disjoint prompts.
Not leftover-15. `used_keys=false`.

postokhits t=0 **3/48 vs 47/48**. poshits t=0 **11/48 vs 39/48**
(occupancy). Nested Youden postokhits **3/48 vs 48/48**. Prompt ranking
postokhits **6/12** strict with **6 ties**. Do not sell **3/48**,
**11/48**, **6/12**, or nested **3/48** as replacing **25/48**.
