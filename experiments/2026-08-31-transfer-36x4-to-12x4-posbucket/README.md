# New-topic position-bucketed last-4 (24×4 GPT-2 → original 12×4)

Same overlap as
[`../2026-08-31-transfer-36x4-to-12x4/`](../2026-08-31-transfer-36x4-to-12x4/):
train on the 24 new 36-prompt stems × 4 draws, test on the original
12×4. `--methods hits,poshits,pospool --pos-bucket 16 --skip-nested`.
Hits is the published unbucketed reader. Unbucketed count tables are
not copied here; they are the same 24-stem fit as that earlier
transfer. `used_keys=false`.

`--skip-nested` skipped the expensive train-LOO Youden. Nested-by-stem
Youden below is computed on the frozen test LRs
(`nested_threshold_by_stem` in `stats.py`). That is not the same
protocol as the published train-LOO nested hits Youden (**26/48** vs
**44/48** on full files). In-sample Youden on files that entered the
fit is optimistic; poshits in-sample Youden is conservative here
(17/48 vs 42/48 at t=0.1445).

## Hits last-4 (new topics)

| Method | Prompts marked > unmarked | Isolated marked `lr > 0` | Unmarked `lr ≤ 0` | AUC | Nested-by-stem Youden marked>t / unmarked≤t |
|---|---|---|---|---|---|
| hits | **12/12** | **42/48** | 24/48 | 0.793 | 27/48 vs 40/48 |
| poshits | 10/12 | 39/48 | **31/48** | **0.811** | **37/48 vs 35/48** |
| pospool | 9/12 | 26/48 | 29/48 | 0.642 | 16/48 vs 44/48 |

Poshits **beats hits on file AUC** (0.811 vs 0.793) and in-sample Youden
J (0.562 vs 0.479). Nested-by-stem on the test LRs is almost balanced
(37/48 vs 35/48) where unbucketed hits stays conservative (27/48 vs
40/48). Prompt-grain ranking loses two stems (10/12 vs 12/12).

This is still GPT-2 laboratory English. It is not a Qwen detector and
not a universal isolated-file yes/no.

See [research/key-free-probe.md](../../research/key-free-probe.md).
