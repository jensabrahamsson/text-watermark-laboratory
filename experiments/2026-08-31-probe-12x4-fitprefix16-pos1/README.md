# 12×4 leave-one-out, matched 16-token poshits bucket 1

Same reader as the 24-topic OOD gate, trained only on the original 12
prompt families. `--fit-prefix 16 --pos-bucket 1`. `used_keys=false`.

| Method | Prompt wins | File AUC | Marked `> 0` | Unmarked `≤ 0` |
|---|---|---|---|---|
| Hard last-4, full file (published) | **10/12** | 0.626 | **29/48** | 23/48 |
| Hits last-4, full file (published) | **11/12** | **0.737** | 28/48 | 30/48 |
| Hits, matched 16-token | 10/12 | 0.678 | 23/48 | 41/48 |
| Poshits / poshitmass, matched 16-token bucket 1 | 9/12 | 0.673 | 23/48 | **48/48** |

Finest buckets on 11 training prompts over-fragment. The reader becomes
a specificity knob (unmarked ≤0 is 48/48) and loses prompt grain. The
**39/48 vs 41/48** OOD gate needs the 24 extra topics. This run is the
negative control for “just namespace by position on 12×4”.

Do not replace 10/12 or 29/48.
