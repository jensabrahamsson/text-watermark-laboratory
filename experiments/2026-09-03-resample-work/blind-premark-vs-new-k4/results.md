# Key-free blind eval (leave-one-prompt-out)

Accuracy: **35/40** (0.875). context_len=4 backoff=False margin=0.

Ranking wins with no isolated TP: **3/35** (18-a-short-story-about-two-people, 31-explain-printing-a-local-newspaper-as, 38-a-short-story-about-neighbours-sharing). Ranking losses with isolated TP: **0**. Isolated marked `lr>0`: **32**. Prompt ranking is not per-file accuracy.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |
|---|---|---|---|---|
| 01-write-a-600-word-travel-essay | 3.2505 | -1.4809 | True | 1/1 |
| 02-explain-how-a-municipal-library-actually | -1.4510 | -1.3220 | False | 0/1 |
| 03-a-short-story-about-two-neighbours | 2.9195 | -1.0717 | True | 1/1 |
| 04-describe-a-rainy-tuesday-commute-in | 3.0944 | -1.3893 | True | 1/1 |
| 05-write-600-words-on-why-people | -1.4770 | -1.3591 | False | 0/1 |
| 06-a-letter-from-a-retired-ferry | 3.2098 | -1.3623 | True | 1/1 |
| 07-explain-sourdough-as-if-you-have | -1.3502 | -1.3283 | False | 0/1 |
| 08-a-600-word-scene-in-a | 2.8570 | -1.1817 | True | 1/1 |
| 09-write-about-500-words-as-a | 3.2682 | -1.4868 | True | 1/1 |
| 10-describe-a-weekday-morning-in-a | 3.2575 | -1.3727 | True | 1/1 |
| 11-a-short-story-about-a-chess | 2.9171 | -1.2291 | True | 1/1 |
| 12-a-letter-from-someone-who-just | 3.2593 | -1.3385 | True | 1/1 |
| 13-write-about-500-words-on-a | 3.1962 | -1.2804 | True | 1/1 |
| 14-describe-the-last-hour-of-a | 3.0170 | -1.3487 | True | 1/1 |
| 15-a-500-word-scene-in-a | 2.7025 | -1.0242 | True | 1/1 |
| 16-explain-ice-fishing-as-if-you | -1.4762 | -1.3723 | False | 0/1 |
| 17-write-about-500-words-as-a | 3.1857 | -1.4490 | True | 1/1 |
| 18-a-short-story-about-two-people | -1.2082 | -1.3192 | True | 0/1 |
| 19-describe-an-allotment-garden-in-late | 3.2320 | -1.2440 | True | 1/1 |
| 20-a-letter-from-a-lighthouse-keeper | 3.2281 | -1.3733 | True | 1/1 |
| 21-write-about-500-words-on-a | 3.2693 | -1.1943 | True | 1/1 |
| 22-a-500-word-scene-in-a | 2.9390 | -1.0979 | True | 1/1 |
| 23-describe-a-night-receptionist-in-a | 3.0853 | -1.3372 | True | 1/1 |
| 24-explain-bicycle-repair-as-if-you | -1.3150 | -1.1960 | False | 0/1 |
| 25-a-short-story-about-a-community | 2.8023 | -1.0621 | True | 1/1 |
| 26-write-about-500-words-as-a | 3.0759 | -1.2097 | True | 1/1 |
| 27-a-letter-from-a-market-stall | 3.1279 | -1.3267 | True | 1/1 |
| 28-describe-a-hiking-hut-on-a | 3.1312 | -1.3133 | True | 1/1 |
| 29-a-500-word-scene-in-a | 2.7772 | -1.0853 | True | 1/1 |
| 30-write-about-500-words-on-an | 3.2349 | -1.3181 | True | 1/1 |
| 31-explain-printing-a-local-newspaper-as | -1.2495 | -1.2833 | True | 0/1 |
| 32-a-short-story-about-walking-other | 3.0578 | -1.2108 | True | 1/1 |
| 33-describe-a-fishing-village-in-january | 3.0990 | -1.3941 | True | 1/1 |
| 34-a-letter-from-a-night-train | 3.2122 | -1.3860 | True | 1/1 |
| 35-write-about-500-words-as-someone | 3.1855 | -1.3170 | True | 1/1 |
| 36-a-500-word-scene-in-a | 2.6405 | -1.1817 | True | 1/1 |
| 37-describe-a-rooftop-greenhouse-that-is | 3.2732 | -1.2360 | True | 1/1 |
| 38-a-short-story-about-neighbours-sharing | -1.1882 | -1.3224 | True | 0/1 |
| 39-write-about-500-words-on-a | 2.9461 | -1.3665 | True | 1/1 |
| 40-a-letter-from-a-retired-teacher | 3.1165 | -1.4611 | True | 1/1 |

