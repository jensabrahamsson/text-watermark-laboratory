# postokbackoff vs control-shuffled-30, 4-token OOD gate

Same split as [../2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokhits/](../2026-08-31-contrast-36x4-to-12x4-fitprefix4-tokhits/).
`used_keys=false`. Not key recovery.

`postokbackoff` copies `postokhits` on this short-train gate: control
`lr>0` **0/48**; public vs control **12/12**, AUC 0.667.

| Method | control `lr>0` | public vs control |
|---|---|---|
| poshits | **0/48** | **12/12**, AUC **0.906** |
| postokhits | **0/48** | **12/12**, AUC 0.667 |
| postokbackoff | **0/48** | **12/12**, AUC 0.667 |
