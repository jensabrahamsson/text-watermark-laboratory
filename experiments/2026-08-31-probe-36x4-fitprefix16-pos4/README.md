# Matched 16-token fit with 4-token position buckets (36×4)

`--fit-prefix 16` clips every draw before fit and score. `--pos-bucket 4`
then namespaces last-4 by `i // 4`, so the 16-token window is four
position slices rather than one. Bucket 16 on a 16-token prefix is a
no-op (every token sits in bucket 0). `used_keys=false`.

Hits here reproduces
[`../2026-08-31-probe-36x4-fitprefix16/`](../2026-08-31-probe-36x4-fitprefix16/).

## Leave-one-of-36-out

| Method | Prompts marked > unmarked | Isolated marked `lr > 0` | Unmarked `lr ≤ 0` | AUC | Nested-by-stem Youden |
|---|---|---|---|---|---|
| Full 128-token hits (published) | **36/36** | 134/144 | 76/144 | 0.934 | 119/144 vs 134/144 |
| Matched 16-token hits | **34/36** | 132/144 | 112/144 | 0.929 | 121/144 vs 136/144 |
| **Matched 16-token poshits, bucket 4** | **34/36** | **133/144** | **114/144** | **0.937** | 122/144 vs 127/144 |

Finer buckets on the opening slightly beat unbucketed matched-prefix hits
on file AUC (0.937 vs 0.929) and t=0 counts (133/144 and 114/144). That
AUC sits next to full-file hits (0.934) and full-file hitmass (0.938)
while unmarked `≤ 0` is **114/144** rather than 76/144. Prompt grain
stays 34/36. Nested-by-stem Youden trades a little specificity for a
threshold near 0. Isolated overlap at a universal t=0 remains.

Do not replace 36/36 or 29/48.

See [research/key-free-probe.md](../../research/key-free-probe.md).
