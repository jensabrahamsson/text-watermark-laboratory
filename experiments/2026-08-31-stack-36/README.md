# Leave-one-prompt LDA stack of hits + hashpool (36 topics)

Same construction as `../2026-08-31-stack-12x4/`, on the 36-topic probe
scores.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| hits (source) | 30/36 | 0.886 | 33/36 | 16/36 |
| hashpool (source) | 31/36 | 0.877 | 32/36 | 22/36 |
| **stack** | **32/36** | **0.890** | 27/36 | **34/36** |

Prompt grain and AUC tick up. Isolated recall at 0 drops; specificity
rises. Still key-free.
