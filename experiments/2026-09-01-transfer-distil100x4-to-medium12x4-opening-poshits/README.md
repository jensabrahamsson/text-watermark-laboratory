# Distil 100×4 → gpt2-medium 12×4 occupancy-free

Protocol: [research/PROTOCOL-isolated-xsize.md](../../research/PROTOCOL-isolated-xsize.md).

Train: `../2026-09-01-pair-distil-100x4/`. Test:
`../2026-09-01-pair-gpt2-medium-12x4/`. Same BPE. Disjoint prompts.
Not leftover-15. `used_keys=false`.

postokhits t=0 **20/48 vs 48/48**. poshits t=0 **42/48 vs 26/48**
(occupancy). Nested Youden postokhits **46/48 vs 11/48** at a negative
train threshold; do not sell 46/48. Prompt ranking postokhits **11/12**
strict with **1 tie**. Do not sell **20/48**, **42/48**, **11/12**, or
nested **46/48** as replacing **25/48**.
