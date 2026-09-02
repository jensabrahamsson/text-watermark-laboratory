# Key-free blind eval (leave-one-prompt-out)

Accuracy: **9/12** (0.750). context_len=4 backoff=False margin=0.

Ranking wins with no isolated TP: **1/9** (11-garden). Ranking losses with isolated TP: **3** (06-station, 10-office, 12-ferry-queue). Isolated marked `lr>0`: **25**. Prompt ranking is not per-file accuracy.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |
|---|---|---|---|---|
| 01-harbour | 0.0057 | -0.0113 | True | 2/4 |
| 02-night-bus | -0.0114 | -0.0510 | True | 1/4 |
| 03-library | 0.0066 | -0.0438 | True | 3/4 |
| 04-market | 0.0602 | 0.0202 | True | 3/4 |
| 05-kitchen | 0.1020 | 0.0249 | True | 3/4 |
| 06-station | -0.0023 | 0.0255 | False | 1/4 |
| 07-rain | 0.0982 | 0.0023 | True | 3/4 |
| 08-letter | 0.0182 | -0.0282 | True | 1/4 |
| 09-workshop | 0.0892 | 0.0734 | True | 4/4 |
| 10-office | -0.0524 | 0.0192 | False | 1/4 |
| 11-garden | -0.0238 | -0.0474 | True | 0/4 |
| 12-ferry-queue | -0.0119 | -0.0067 | False | 3/4 |

