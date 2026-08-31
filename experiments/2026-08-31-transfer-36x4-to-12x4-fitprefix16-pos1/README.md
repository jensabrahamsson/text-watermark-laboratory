# New-topic matched 16-token poshits, bucket 1

Finest position namespace (`i // 1`) on the first 16 tokens. Train 24
new 36×4 stems, score the original 12×4 files. Nested Youden / 10% FPR
from training-stem leave-one-out, then frozen on test. `used_keys=false`.
The prepended position is not a watermark key.

On this 16-token prefix, bucket 2 produced identical LRs (see
[`../2026-08-31-probe-36x4-fitprefix16-pos-sweep/`](../2026-08-31-probe-36x4-fitprefix16-pos-sweep/)).

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| Full-file hits (published) | **12/12** | 0.793 | **42/48** | 24/48 |
| Matched 16-token hits | 11/12 | 0.818 | 39/48 | 31/48 |
| Matched 16-token poshits, bucket 4 | 11/12 | 0.820 | 39/48 | 33/48 |
| **Matched 16-token poshits, bucket 1** | **12/12** | **0.873** | 39/48 | **41/48** |

| Gate | Test marked>t | Test unmarked≤t |
|---|---|---|
| Nested-by-stem Youden | **39/48** | **41/48** |
| Nested FPR10 (train-LOO) | **39/48** | **41/48** |
| Nested Youden (train-LOO) | 16/48 | 48/48 |

t=0 is already the balanced isolated-file rule here. Nested Youden on
the training stems is conservative (high in-domain threshold). Nested
FPR10 matches t=0.

This is still GPT-2 laboratory text, new topics, same generator. It is
not a universal detector. A matched **4-token** clip with the same
namespace copies this operating point and makes nested Youden match t=0:
[`../2026-08-31-transfer-36x4-to-12x4-fitprefix4-pos1/`](../2026-08-31-transfer-36x4-to-12x4-fitprefix4-pos1/).
Leave-one-of-12-out on the original 12 prompts alone does **not** copy
this gate
([`../2026-08-31-probe-12x4-fitprefix16-pos1/`](../2026-08-31-probe-12x4-fitprefix16-pos1/)).
GPT-2 → Qwen with the 16-token reader is chance
([`../2026-08-31-transfer-36x4-to-qwen-fitprefix16-pos1/`](../2026-08-31-transfer-36x4-to-qwen-fitprefix16-pos1/)).

Do not replace 10/12, 29/48, or 36/36.
