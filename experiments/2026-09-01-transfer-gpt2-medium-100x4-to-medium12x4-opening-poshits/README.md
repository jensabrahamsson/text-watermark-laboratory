# gpt2-medium 100×4 → gpt2-medium 12×4 occupancy-free

Protocol: [research/PROTOCOL-isolated-m12.md](../../research/PROTOCOL-isolated-m12.md).

Train: `../2026-09-01-pair-gpt2-medium-100x4/`. Test:
`../2026-09-01-pair-gpt2-medium-12x4/`. Same BPE. Disjoint prompts.
Not leftover-15. `used_keys=false`.

postokhits t=0 **10/48 vs 48/48**. poshits t=0 **39/48 vs 41/48**
(occupancy). Nested Youden postokhits **10/48 vs 48/48**. Prompt ranking
postokhits **8/12** strict with **3 ties**. Do not sell **10/48**,
**39/48**, **8/12**, or nested **10/48** as replacing **25/48**.
