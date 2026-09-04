# Key-free blind eval (leave-one-prompt-out)

Accuracy: **36/40** (0.900). context_len=1 backoff=False margin=0.

Ranking wins with no isolated TP: **4/36** (03-a-short-story-about-two-neighbours, 07-explain-sourdough-as-if-you-have, 18-a-short-story-about-two-people, 25-a-short-story-about-a-community). Ranking losses with isolated TP: **0**. Isolated marked `lr>0`: **32**. Prompt ranking is not per-file accuracy.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |
|---|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.5943 | -0.5712 | False | 0/1 |
| 02-explain-how-a-municipal-library-actually | 2.7693 | -0.4783 | True | 1/1 |
| 03-a-short-story-about-two-neighbours | -0.3798 | -0.4590 | True | 0/1 |
| 04-describe-a-rainy-tuesday-commute-in | 2.6627 | -0.4713 | True | 1/1 |
| 05-write-600-words-on-why-people | -0.5161 | -0.4229 | False | 0/1 |
| 06-a-letter-from-a-retired-ferry | 2.8868 | -0.5093 | True | 1/1 |
| 07-explain-sourdough-as-if-you-have | -0.4957 | -0.5548 | True | 0/1 |
| 08-a-600-word-scene-in-a | 2.6300 | -0.4524 | True | 1/1 |
| 09-write-about-500-words-as-a | 3.1498 | -0.6343 | True | 1/1 |
| 10-describe-a-weekday-morning-in-a | 2.8667 | -0.4210 | True | 1/1 |
| 11-a-short-story-about-a-chess | 2.5617 | -0.4261 | True | 1/1 |
| 12-a-letter-from-someone-who-just | 2.8105 | -0.4678 | True | 1/1 |
| 13-write-about-500-words-on-a | 2.8158 | -0.5615 | True | 1/1 |
| 14-describe-the-last-hour-of-a | 2.7838 | -0.5364 | True | 1/1 |
| 15-a-500-word-scene-in-a | 2.6946 | -0.4176 | True | 1/1 |
| 16-explain-ice-fishing-as-if-you | -0.4991 | -0.4805 | False | 0/1 |
| 17-write-about-500-words-as-a | 2.8693 | -0.5277 | True | 1/1 |
| 18-a-short-story-about-two-people | -0.3618 | -0.4144 | True | 0/1 |
| 19-describe-an-allotment-garden-in-late | 2.6041 | -0.4364 | True | 1/1 |
| 20-a-letter-from-a-lighthouse-keeper | 2.8110 | -0.4150 | True | 1/1 |
| 21-write-about-500-words-on-a | 2.8471 | -0.4827 | True | 1/1 |
| 22-a-500-word-scene-in-a | 2.5876 | -0.4732 | True | 1/1 |
| 23-describe-a-night-receptionist-in-a | 3.0067 | -0.4802 | True | 1/1 |
| 24-explain-bicycle-repair-as-if-you | -0.5075 | -0.4076 | False | 0/1 |
| 25-a-short-story-about-a-community | -0.4139 | -0.4949 | True | 0/1 |
| 26-write-about-500-words-as-a | 2.7919 | -0.4860 | True | 1/1 |
| 27-a-letter-from-a-market-stall | 2.5849 | -0.4748 | True | 1/1 |
| 28-describe-a-hiking-hut-on-a | 2.6355 | -0.4897 | True | 1/1 |
| 29-a-500-word-scene-in-a | 2.5286 | -0.5227 | True | 1/1 |
| 30-write-about-500-words-on-an | 2.8524 | -0.6168 | True | 1/1 |
| 31-explain-printing-a-local-newspaper-as | 2.7476 | -0.4025 | True | 1/1 |
| 32-a-short-story-about-walking-other | 2.7792 | -0.5049 | True | 1/1 |
| 33-describe-a-fishing-village-in-january | 2.7028 | -0.5692 | True | 1/1 |
| 34-a-letter-from-a-night-train | 2.8823 | -0.5638 | True | 1/1 |
| 35-write-about-500-words-as-someone | 2.7713 | -0.5072 | True | 1/1 |
| 36-a-500-word-scene-in-a | 2.3759 | -0.3981 | True | 1/1 |
| 37-describe-a-rooftop-greenhouse-that-is | 2.7583 | -0.6174 | True | 1/1 |
| 38-a-short-story-about-neighbours-sharing | 2.8329 | -0.3569 | True | 1/1 |
| 39-write-about-500-words-on-a | 2.6781 | -0.5006 | True | 1/1 |
| 40-a-letter-from-a-retired-teacher | 2.7166 | -0.5567 | True | 1/1 |

