# New-topic prompt-as-context (ranking without isolated-file)

Train 24 new stems, score 12×4 with `--prompt-context`. `used_keys=false`.

| Method | Prompt wins | File AUC | t=0 |
|---|---|---|---|
| hits / poshits | **12/12** | 0.635 | 13/48 vs 48/48 |

Prompt last-4 does not transfer. When a hit fires it is marked, so
prompt-grain ranking is 12/12 with unmarked LR = 0. Isolated-file
recall is 13/48. Not an `indicate score` protocol.
