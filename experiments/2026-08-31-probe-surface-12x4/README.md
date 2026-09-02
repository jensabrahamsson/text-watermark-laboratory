# Surface and logit on 12×4 GPT-2 leave-one-out

Same twins as `../2026-08-31-probe-12x4/`. UTF-8 byte hashpool (`surface`)
and ridge logistic (`logit`) on hits+hashpool+surface. `used_keys=false`.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hits | **11/12** | **0.737** | 28/48 | 30/48 |
| hashpool | **11/12** | 0.716 | **35/48** | 29/48 |
| surface | **10/12** | 0.602 | 12/48 | 42/48 |
| logit | 10/12 | 0.735 | 23/48 | 41/48 |

Byte pooling ranks 10/12 prompt groups without a tokenizer. Isolated sign at
0 is conservative (12/48). Token hashpool remains the stronger isolated
reader on this corpus (35/48). Logit at 0 behaves like the LDA stack: a
specificity knob, not a 12/12 ensemble.
