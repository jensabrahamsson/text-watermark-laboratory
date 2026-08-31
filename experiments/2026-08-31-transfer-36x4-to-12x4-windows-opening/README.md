# New-topic opening windows: 0:4 vs 4:16

Train 24 new 36×4 stems, score 12×4. `--windows` on a full-file hits
table (not `--fit-prefix`). Nested skipped. Full-file tables omitted
(duplicate of the published 36×4→12×4 counts). `used_keys=false`.

| Window | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| **0:4** | **11/12** | **0.752** | 40/48 | 23/48 |
| 0:16 | **11/12** | **0.752** | 40/48 | 23/48 |
| 4:16 | 9/12 | 0.617 | 26/48 | 30/48 |
| 16:32 | 8/12 | 0.512 | 27/48 | 22/48 |

Same identity as in-domain: the 16-token prefix ranking is the first
four tokens. Isolated t=0 spec stays weak (23/48) because this is
fit-full / score-slice, not a matched 4-token fit.
