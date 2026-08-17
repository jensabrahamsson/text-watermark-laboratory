# Key-free blind eval (leave-one-prompt-out)

Accuracy: **11/12** (0.917). context_len=4 backoff=False margin=0.015.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-harbour | 0.0248 | -0.0114 | True |
| 02-night-bus | -0.0116 | -0.0510 | True |
| 03-library | 0.0066 | -0.0470 | True |
| 04-market | 0.0599 | 0.0180 | True |
| 05-kitchen | 0.1210 | 0.0185 | True |
| 06-station | 0.0149 | 0.0254 | True |
| 07-rain | 0.1118 | -0.0000 | True |
| 08-letter | 0.0180 | -0.0314 | True |
| 09-workshop | 0.1104 | 0.0733 | True |
| 10-office | -0.0468 | 0.0192 | False |
| 11-garden | -0.0240 | -0.0475 | True |
| 12-ferry-queue | 0.0090 | -0.0068 | True |

