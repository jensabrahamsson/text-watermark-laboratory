# GPT-2 36×4 → new Qwen 12×4, matched 16-token poshits bucket 1

Same `--fit-prefix 16 --pos-bucket 1` reader as the GPT-2 OOD 12/12
gate. Overlapping stems dropped. `used_keys=false`. Frozen GPT-2 tables
are omitted so this negative cannot be used as a detector.

| Method | Prompt wins | File AUC | Marked `> 0` | perm p |
|---|---|---|---|---|
| Full-file hits, same split (published) | 6/12 | 0.445 | — | — |
| **Matched 16-token poshits, bucket 1** | 8/12 | **0.516** | 10/48 | 0.15 |

Chance. Extra GPT-2 draws, a matched 16-token window, and position
namespacing do not create a Qwen detector. Keep the published original
Qwen 12×1 hashpool **10/12** tied to that corpus.
