# Key-free blind eval (leave-one-prompt-out)

Accuracy: **10/12** (0.833). context_len=2 backoff=False.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-harbour | 0.0014 | -0.1678 | True |
| 02-night-bus | 0.0090 | -0.1214 | True |
| 03-library | 0.2060 | -0.1907 | True |
| 04-market | -0.0564 | -0.1313 | True |
| 05-kitchen | -0.1100 | -0.0159 | False |
| 06-station | -0.1110 | -0.1173 | True |
| 07-rain | -0.0246 | -0.1211 | True |
| 08-letter | -0.1760 | -0.1595 | False |
| 09-workshop | 0.0796 | -0.0232 | True |
| 10-office | -0.0561 | -0.0945 | True |
| 11-garden | 0.0107 | -0.0942 | True |
| 12-ferry-queue | -0.0526 | -0.1192 | True |

