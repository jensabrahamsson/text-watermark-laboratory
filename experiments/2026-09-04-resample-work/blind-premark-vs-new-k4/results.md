# Key-free blind eval (leave-one-prompt-out)

Accuracy: **37/40** (0.925). context_len=4 backoff=False margin=0.

Ranking wins with no isolated TP: **5/37** (01-write-a-600-word-travel-essay, 03-a-short-story-about-two-neighbours, 07-explain-sourdough-as-if-you-have, 18-a-short-story-about-two-people, 25-a-short-story-about-a-community). Ranking losses with isolated TP: **0**. Isolated marked `lr>0`: **32**. Prompt ranking is not per-file accuracy.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |
|---|---|---|---|---|
| 01-write-a-600-word-travel-essay | -1.4991 | -1.6166 | True | 0/1 |
| 02-explain-how-a-municipal-library-actually | 3.1447 | -1.2917 | True | 1/1 |
| 03-a-short-story-about-two-neighbours | -1.1903 | -1.1959 | True | 0/1 |
| 04-describe-a-rainy-tuesday-commute-in | 3.0497 | -1.4202 | True | 1/1 |
| 05-write-600-words-on-why-people | -1.4393 | -1.4064 | False | 0/1 |
| 06-a-letter-from-a-retired-ferry | 3.2687 | -1.4184 | True | 1/1 |
| 07-explain-sourdough-as-if-you-have | -1.3475 | -1.3493 | True | 0/1 |
| 08-a-600-word-scene-in-a | 2.8770 | -1.2356 | True | 1/1 |
| 09-write-about-500-words-as-a | 3.2053 | -1.4984 | True | 1/1 |
| 10-describe-a-weekday-morning-in-a | 3.1101 | -1.4538 | True | 1/1 |
| 11-a-short-story-about-a-chess | 2.9354 | -1.2598 | True | 1/1 |
| 12-a-letter-from-someone-who-just | 3.1824 | -1.3816 | True | 1/1 |
| 13-write-about-500-words-on-a | 3.1037 | -1.4013 | True | 1/1 |
| 14-describe-the-last-hour-of-a | 3.0512 | -1.4084 | True | 1/1 |
| 15-a-500-word-scene-in-a | 2.9437 | -1.0243 | True | 1/1 |
| 16-explain-ice-fishing-as-if-you | -1.4430 | -1.3702 | False | 0/1 |
| 17-write-about-500-words-as-a | 3.1897 | -1.5149 | True | 1/1 |
| 18-a-short-story-about-two-people | -1.1651 | -1.3351 | True | 0/1 |
| 19-describe-an-allotment-garden-in-late | 3.0558 | -1.2021 | True | 1/1 |
| 20-a-letter-from-a-lighthouse-keeper | 3.2170 | -1.3804 | True | 1/1 |
| 21-write-about-500-words-on-a | 3.2290 | -1.3062 | True | 1/1 |
| 22-a-500-word-scene-in-a | 2.8901 | -1.1101 | True | 1/1 |
| 23-describe-a-night-receptionist-in-a | 3.3745 | -1.3468 | True | 1/1 |
| 24-explain-bicycle-repair-as-if-you | -1.3188 | -1.2364 | False | 0/1 |
| 25-a-short-story-about-a-community | -1.0920 | -1.1534 | True | 0/1 |
| 26-write-about-500-words-as-a | 3.1139 | -1.2499 | True | 1/1 |
| 27-a-letter-from-a-market-stall | 3.1321 | -1.3478 | True | 1/1 |
| 28-describe-a-hiking-hut-on-a | 3.2274 | -1.3292 | True | 1/1 |
| 29-a-500-word-scene-in-a | 2.6611 | -1.1319 | True | 1/1 |
| 30-write-about-500-words-on-an | 3.2507 | -1.3273 | True | 1/1 |
| 31-explain-printing-a-local-newspaper-as | 3.0988 | -1.2103 | True | 1/1 |
| 32-a-short-story-about-walking-other | 3.1680 | -1.2453 | True | 1/1 |
| 33-describe-a-fishing-village-in-january | 3.0551 | -1.3481 | True | 1/1 |
| 34-a-letter-from-a-night-train | 3.2070 | -1.4495 | True | 1/1 |
| 35-write-about-500-words-as-someone | 3.1493 | -1.3756 | True | 1/1 |
| 36-a-500-word-scene-in-a | 2.6607 | -1.2218 | True | 1/1 |
| 37-describe-a-rooftop-greenhouse-that-is | 3.1813 | -1.2853 | True | 1/1 |
| 38-a-short-story-about-neighbours-sharing | 3.2396 | -1.2502 | True | 1/1 |
| 39-write-about-500-words-on-a | 3.1465 | -1.3126 | True | 1/1 |
| 40-a-letter-from-a-retired-teacher | 3.2567 | -1.4782 | True | 1/1 |

