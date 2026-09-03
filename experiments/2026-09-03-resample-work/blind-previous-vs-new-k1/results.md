# Key-free blind eval (leave-one-prompt-out)

Accuracy: **33/40** (0.825). context_len=1 backoff=False margin=0.

Ranking wins with no isolated TP: **6/33** (02-explain-how-a-municipal-library-actually, 05-write-600-words-on-why-people, 07-explain-sourdough-as-if-you-have, 16-explain-ice-fishing-as-if-you, 24-explain-bicycle-repair-as-if-you, 31-explain-printing-a-local-newspaper-as). Ranking losses with isolated TP: **5** (12-a-letter-from-someone-who-just, 22-a-500-word-scene-in-a, 27-a-letter-from-a-market-stall, 39-write-about-500-words-on-a, 40-a-letter-from-a-retired-teacher). Isolated marked `lr>0`: **32**. Prompt ranking is not per-file accuracy.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |
|---|---|---|---|---|
| 01-write-a-600-word-travel-essay | 0.5117 | -0.3433 | True | 1/1 |
| 02-explain-how-a-municipal-library-actually | -0.3172 | -0.3798 | True | 0/1 |
| 03-a-short-story-about-two-neighbours | 0.3286 | -0.4170 | True | 1/1 |
| 04-describe-a-rainy-tuesday-commute-in | 0.5752 | -0.3930 | True | 1/1 |
| 05-write-600-words-on-why-people | -0.2797 | -0.3747 | True | 0/1 |
| 06-a-letter-from-a-retired-ferry | 0.4513 | 0.3833 | True | 1/1 |
| 07-explain-sourdough-as-if-you-have | -0.1720 | -0.3522 | True | 0/1 |
| 08-a-600-word-scene-in-a | 0.6126 | 0.4729 | True | 1/1 |
| 09-write-about-500-words-as-a | 0.5309 | -0.4249 | True | 1/1 |
| 10-describe-a-weekday-morning-in-a | 0.4848 | -0.3598 | True | 1/1 |
| 11-a-short-story-about-a-chess | 0.4469 | -0.3356 | True | 1/1 |
| 12-a-letter-from-someone-who-just | 0.3739 | 0.4187 | False | 1/1 |
| 13-write-about-500-words-on-a | 0.4795 | -0.3192 | True | 1/1 |
| 14-describe-the-last-hour-of-a | 0.5152 | -0.3453 | True | 1/1 |
| 15-a-500-word-scene-in-a | 0.5157 | -0.3199 | True | 1/1 |
| 16-explain-ice-fishing-as-if-you | -0.2759 | -0.3150 | True | 0/1 |
| 17-write-about-500-words-as-a | 0.5300 | -0.3705 | True | 1/1 |
| 18-a-short-story-about-two-people | -0.3979 | -0.3237 | False | 0/1 |
| 19-describe-an-allotment-garden-in-late | 0.5266 | 0.4709 | True | 1/1 |
| 20-a-letter-from-a-lighthouse-keeper | 0.4653 | 0.3962 | True | 1/1 |
| 21-write-about-500-words-on-a | 0.5098 | 0.3676 | True | 1/1 |
| 22-a-500-word-scene-in-a | 0.3793 | 0.4094 | False | 1/1 |
| 23-describe-a-night-receptionist-in-a | 0.5933 | -0.3131 | True | 1/1 |
| 24-explain-bicycle-repair-as-if-you | -0.2316 | -0.2437 | True | 0/1 |
| 25-a-short-story-about-a-community | 0.5148 | 0.3700 | True | 1/1 |
| 26-write-about-500-words-as-a | 0.5325 | -0.3181 | True | 1/1 |
| 27-a-letter-from-a-market-stall | 0.4626 | 0.4632 | False | 1/1 |
| 28-describe-a-hiking-hut-on-a | 0.5233 | -0.4334 | True | 1/1 |
| 29-a-500-word-scene-in-a | 0.5112 | 0.3921 | True | 1/1 |
| 30-write-about-500-words-on-an | 0.5287 | 0.5158 | True | 1/1 |
| 31-explain-printing-a-local-newspaper-as | -0.2756 | -0.4029 | True | 0/1 |
| 32-a-short-story-about-walking-other | 0.5185 | -0.3710 | True | 1/1 |
| 33-describe-a-fishing-village-in-january | 0.5850 | -0.3682 | True | 1/1 |
| 34-a-letter-from-a-night-train | 0.4653 | 0.4499 | True | 1/1 |
| 35-write-about-500-words-as-someone | 0.4713 | -0.3351 | True | 1/1 |
| 36-a-500-word-scene-in-a | 0.4005 | 0.3361 | True | 1/1 |
| 37-describe-a-rooftop-greenhouse-that-is | 0.4130 | -0.2906 | True | 1/1 |
| 38-a-short-story-about-neighbours-sharing | -0.1849 | 0.4080 | False | 0/1 |
| 39-write-about-500-words-on-a | 0.3996 | 0.4623 | False | 1/1 |
| 40-a-letter-from-a-retired-teacher | 0.3777 | 0.4322 | False | 1/1 |

