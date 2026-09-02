# Key-free blind eval (leave-one-prompt-out)

Accuracy: **9/12** (0.750). context_len=4 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-harbour | 0.0057 | -0.0113 | True |
| 02-night-bus | -0.0114 | -0.0510 | True |
| 03-library | 0.0066 | -0.0438 | True |
| 04-market | 0.0602 | 0.0202 | True |
| 05-kitchen | 0.1020 | 0.0249 | True |
| 06-station | -0.0023 | 0.0255 | False |
| 07-rain | 0.0982 | 0.0023 | True |
| 08-letter | 0.0182 | -0.0282 | True |
| 09-workshop | 0.0892 | 0.0734 | True |
| 10-office | -0.0524 | 0.0192 | False |
| 11-garden | -0.0238 | -0.0474 | True |
| 12-ferry-queue | -0.0119 | -0.0067 | False |

