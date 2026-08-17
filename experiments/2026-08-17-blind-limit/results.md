# Key-free blind eval (leave-one-prompt-out)

Accuracy: **6/12** (0.500). context_len=1.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-harbour | 0.0169 | 0.0128 | True |
| 02-night-bus | 0.0515 | 0.0338 | True |
| 03-library | 0.0215 | -0.0207 | True |
| 04-market | 0.1357 | 0.0484 | True |
| 05-kitchen | 0.0250 | -0.0066 | True |
| 06-station | 0.1117 | 0.0317 | True |
| 07-rain | 0.0275 | 0.0375 | False |
| 08-letter | -0.0467 | -0.0243 | False |
| 09-workshop | 0.0631 | 0.0653 | False |
| 10-office | -0.0259 | 0.0142 | False |
| 11-garden | 0.0463 | 0.0556 | False |
| 12-ferry-queue | -0.0397 | -0.0217 | False |

