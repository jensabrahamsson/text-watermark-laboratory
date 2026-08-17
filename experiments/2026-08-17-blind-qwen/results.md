# Key-free blind eval (leave-one-prompt-out)

Accuracy: **4/12** (0.333). context_len=1.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-harbour | 0.0840 | 0.0443 | True |
| 02-night-bus | -0.0515 | 0.0088 | False |
| 03-library | 0.3100 | -0.0433 | True |
| 04-market | 0.0123 | 0.0127 | False |
| 05-kitchen | -0.0059 | 0.0409 | False |
| 06-station | -0.0851 | 0.0167 | False |
| 07-rain | -0.1225 | -0.0637 | False |
| 08-letter | -0.1807 | -0.0725 | False |
| 09-workshop | 0.1045 | -0.0942 | True |
| 10-office | -0.0915 | 0.0009 | False |
| 11-garden | 0.0063 | -0.1118 | True |
| 12-ferry-queue | -0.0244 | 0.0016 | False |

