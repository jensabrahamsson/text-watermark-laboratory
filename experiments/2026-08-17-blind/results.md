# Key-free blind eval (leave-one-prompt-out)

Accuracy: **8/12** (0.667). context_len=1.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-harbour | -0.1134 | -0.0357 | False |
| 02-night-bus | -0.0401 | -0.0726 | True |
| 03-library | -0.0185 | -0.0327 | True |
| 04-market | 0.1324 | -0.0121 | True |
| 05-kitchen | 0.0430 | -0.0258 | True |
| 06-station | 0.0268 | -0.0302 | True |
| 07-rain | 0.1098 | -0.0185 | True |
| 08-letter | 0.1525 | 0.0583 | True |
| 09-workshop | 0.0565 | -0.0902 | True |
| 10-office | 0.0450 | 0.0688 | False |
| 11-garden | -0.1829 | -0.0783 | False |
| 12-ferry-queue | -0.0999 | 0.1183 | False |

