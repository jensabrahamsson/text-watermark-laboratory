# New-topic 4-token include-first (negative for isolated-file)

Train 24 new stems, score 12×4. `--include-first` on the matched
4-token last-4 reader. `used_keys=false`.

| Method | Prompt wins | File AUC | t=0 |
|---|---|---|---|
| hits | 9/12 | 0.702 | 16/48 vs 42/48 |
| poshits | 9/12 | 0.719 | 16/48 vs 44/48 |
| first | 6/12 | 0.555 | 16/48 vs 40/48 |

Mixing token 0 into hits **hurts** the 12/12 / 0.873 gate. First-token
unigram does not transfer across GPT-2 topics. Keep `--include-first`
off for that isolated-file protocol.
