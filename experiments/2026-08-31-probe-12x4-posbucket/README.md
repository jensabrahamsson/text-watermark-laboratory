# Position-bucketed last-4 on the original 12×4 GPT-2 twins

Same 12-prompt × 4-draw corpus as
[`../2026-08-31-probe-12x4/`](../2026-08-31-probe-12x4/).
`poshits` / `pospool` prepend `i // 16` to the last-4 context so a 4-gram
in the opening does not share a count bucket with the same tokens later
in the string. That namespace is laboratory bookkeeping, **not** a
watermark key. `used_keys=false`.

Hits and hashpool here reproduce the published 12×4 leave-one-out
readers. They are not bucketed.

## Leave-one-of-12-out

| Method | Prompts marked > unmarked | Isolated marked `lr > 0` | Unmarked `lr ≤ 0` | AUC | Nested-by-stem Youden marked>t / unmarked≤t |
|---|---|---|---|---|---|
| hits | **11/12** | 28/48 | 30/48 | **0.737** | 22/48 vs 39/48 |
| hashpool | **11/12** | **35/48** | 29/48 | 0.716 | 23/48 vs 36/48 |
| poshits | 10/12 | 24/48 | **37/48** | 0.666 | **24/48 vs 45/48** |
| pospool | 9/12 | 28/48 | 24/48 | 0.669 | 24/48 vs 43/48 |

On this small leave-one-out, poshits is a **specificity knob**, not a
better t=0 detector. Isolated marked `lr > 0` falls from 28/48 (hits) to
24/48. Nested-by-stem Youden then holds unmarked files to 45/48 at the
cost of that same 24/48 recall. Do not replace the published hard last-4
**10/12** / **29/48**, and do not replace hits **11/12**.

See [research/key-free-probe.md](../../research/key-free-probe.md).
