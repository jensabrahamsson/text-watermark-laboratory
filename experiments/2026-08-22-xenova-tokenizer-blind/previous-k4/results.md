# Key-free blind eval (leave-one-prompt-out)

Accuracy: **32/40** (0.800). context_len=4 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.4090 | -0.4311 | True |
| 02-explain-how-a-municipal-library-actually | -0.4365 | -0.4066 | False |
| 03-a-short-story-about-two-neighbours | -0.3319 | -0.3935 | True |
| 04-describe-a-rainy-tuesday-commute-in | -0.3783 | -0.3569 | False |
| 05-write-600-words-on-why-people | -0.4630 | -0.5181 | True |
| 06-a-letter-from-a-retired-ferry | 2.4542 | -0.4850 | True |
| 07-explain-sourdough-as-if-you-have | -0.4704 | -0.5286 | True |
| 08-a-600-word-scene-in-a | 2.2755 | -0.3578 | True |
| 09-write-about-500-words-as-a | -0.4631 | -0.5507 | True |
| 10-describe-a-weekday-morning-in-a | -0.4122 | -0.3885 | False |
| 11-a-short-story-about-a-chess | -0.2635 | -0.2964 | True |
| 12-a-letter-from-someone-who-just | 2.6039 | -0.4174 | True |
| 13-write-about-500-words-on-a | -0.4130 | -0.4370 | True |
| 14-describe-the-last-hour-of-a | -0.4116 | -0.3448 | False |
| 15-a-500-word-scene-in-a | -0.3883 | -0.4261 | True |
| 16-explain-ice-fishing-as-if-you | -0.4720 | -0.4657 | False |
| 17-write-about-500-words-as-a | -0.4223 | -0.5771 | True |
| 18-a-short-story-about-two-people | -0.2962 | -0.3813 | True |
| 19-describe-an-allotment-garden-in-late | 2.0966 | -0.4086 | True |
| 20-a-letter-from-a-lighthouse-keeper | 2.5761 | -0.4016 | True |
| 21-write-about-500-words-on-a | 2.6561 | -0.4164 | True |
| 22-a-500-word-scene-in-a | 2.3608 | -0.3137 | True |
| 23-describe-a-night-receptionist-in-a | -0.4609 | -0.4877 | True |
| 24-explain-bicycle-repair-as-if-you | -0.4739 | -0.4182 | False |
| 25-a-short-story-about-a-community | 2.2137 | -0.3199 | True |
| 26-write-about-500-words-as-a | -0.4729 | -0.4518 | False |
| 27-a-letter-from-a-market-stall | 2.3882 | -0.3451 | True |
| 28-describe-a-hiking-hut-on-a | -0.4555 | -0.4512 | False |
| 29-a-500-word-scene-in-a | 2.3630 | -0.4093 | True |
| 30-write-about-500-words-on-an | 2.4802 | -0.4395 | True |
| 31-explain-printing-a-local-newspaper-as | -0.3145 | -0.4762 | True |
| 32-a-short-story-about-walking-other | -0.3509 | -0.4343 | True |
| 33-describe-a-fishing-village-in-january | -0.3721 | -0.4747 | True |
| 34-a-letter-from-a-night-train | 2.6878 | -0.5097 | True |
| 35-write-about-500-words-as-someone | -0.3803 | -0.4267 | True |
| 36-a-500-word-scene-in-a | 2.0876 | -0.3805 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.3200 | -0.4863 | True |
| 38-a-short-story-about-neighbours-sharing | 2.4742 | -0.2677 | True |
| 39-write-about-500-words-on-a | 2.5796 | -0.5109 | True |
| 40-a-letter-from-a-retired-teacher | 2.5155 | -0.4956 | True |

