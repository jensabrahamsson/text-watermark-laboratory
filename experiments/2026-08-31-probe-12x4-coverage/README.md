# Last-4 coverage by token window (12×4)

Same `--coverage` protocol as
[`../2026-08-31-probe-36x4-coverage/`](../2026-08-31-probe-36x4-coverage/).
`used_keys=false`.

| Window | Shared last-k | n | Mean support when shared |
|---|---|---|---|
| 0:16 (includes last-1/2) | **0.065** (94/1440) | 1440 | **28.0** |
| 16:32 | 0.010 (15/1536) | 1536 | 3.7 |
| 32:64 | 0.011 (34/3072) | 3072 | 4.4 |
| 64:128 | 0.014 (86/6133) | 6133 | 4.7 |

Same shape as 36×4 at lower mass. The 0:16 average is pulled up by
short contexts at the start, not by extra full 4-grams. Leave-one-of-12-out
still has little shared last-4 after those opening tokens, which is why
12×4 `hits` is a ranking method rather than a 29/48 isolated-file detector.
