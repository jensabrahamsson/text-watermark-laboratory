# 36×4 LOO postokbackoff, matched 4-token opening

`--fit-prefix 4 --pos-bucket 1`. `used_keys=false`.
Write-up: [../../research/key-free-tokhits.md](../../research/key-free-tokhits.md).

In-domain, shrinking last-k does **not** add marked detections versus
`postokhits` (**122/144** both). It adds one unmarked false positive
(unmarked ≤0 **131/144** vs **132/144**). Nested-by-stem Youden stays
**121/144** marked.

| Method | Prompt wins | File AUC | marked `lr>0` | unmarked `lr≤0` |
|---|---|---|---|---|
| poshits | 34/36 | 0.935 | **131/144** | **132/144** |
| postokhits | 34/36 | 0.912 | **122/144** | **132/144** |
| postokbackoff | 34/36 | 0.910 | **122/144** | **131/144** |
