# Key-free blind eval (leave-one-prompt-out)

Accuracy: **29/40** (0.725). context_len=4 backoff=False margin=0.

Ranking wins with no isolated TP: **5/29** (05-write-600-words-on-why-people, 07-explain-sourdough-as-if-you-have, 18-a-short-story-about-two-people, 24-explain-bicycle-repair-as-if-you, 31-explain-printing-a-local-newspaper-as). Ranking losses with isolated TP: **8** (08-a-600-word-scene-in-a, 20-a-letter-from-a-lighthouse-keeper, 21-write-about-500-words-on-a, 25-a-short-story-about-a-community, 34-a-letter-from-a-night-train, 36-a-500-word-scene-in-a, 39-write-about-500-words-on-a, 40-a-letter-from-a-retired-teacher). Isolated marked `lr>0`: **32**. Prompt ranking is not per-file accuracy.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |
|---|---|---|---|---|
| 01-write-a-600-word-travel-essay | 0.1893 | -0.8679 | True | 1/1 |
| 02-explain-how-a-municipal-library-actually | -0.8608 | -0.8280 | False | 0/1 |
| 03-a-short-story-about-two-neighbours | 0.1702 | -0.6776 | True | 1/1 |
| 04-describe-a-rainy-tuesday-commute-in | 0.2411 | -0.8274 | True | 1/1 |
| 05-write-600-words-on-why-people | -0.8383 | -0.9167 | True | 0/1 |
| 06-a-letter-from-a-retired-ferry | 0.2703 | 0.2677 | True | 1/1 |
| 07-explain-sourdough-as-if-you-have | -0.7362 | -0.8194 | True | 0/1 |
| 08-a-600-word-scene-in-a | 0.1597 | 0.2363 | False | 1/1 |
| 09-write-about-500-words-as-a | 0.2158 | -0.9414 | True | 1/1 |
| 10-describe-a-weekday-morning-in-a | 0.2166 | -0.7844 | True | 1/1 |
| 11-a-short-story-about-a-chess | 0.1482 | -0.7573 | True | 1/1 |
| 12-a-letter-from-someone-who-just | 0.2513 | 0.2002 | True | 1/1 |
| 13-write-about-500-words-on-a | 0.2559 | -0.7429 | True | 1/1 |
| 14-describe-the-last-hour-of-a | 0.1889 | -0.8698 | True | 1/1 |
| 15-a-500-word-scene-in-a | 0.1583 | -0.6868 | True | 1/1 |
| 16-explain-ice-fishing-as-if-you | -0.8580 | -0.8407 | False | 0/1 |
| 17-write-about-500-words-as-a | 0.1542 | -0.8972 | True | 1/1 |
| 18-a-short-story-about-two-people | -0.7994 | -0.8637 | True | 0/1 |
| 19-describe-an-allotment-garden-in-late | 0.2977 | 0.2484 | True | 1/1 |
| 20-a-letter-from-a-lighthouse-keeper | 0.2783 | 0.3076 | False | 1/1 |
| 21-write-about-500-words-on-a | 0.2960 | 0.3036 | False | 1/1 |
| 22-a-500-word-scene-in-a | 0.2989 | 0.2065 | True | 1/1 |
| 23-describe-a-night-receptionist-in-a | 0.1927 | -0.8357 | True | 1/1 |
| 24-explain-bicycle-repair-as-if-you | -0.7443 | -0.7545 | True | 0/1 |
| 25-a-short-story-about-a-community | 0.1909 | 0.2087 | False | 1/1 |
| 26-write-about-500-words-as-a | 0.1915 | -0.7642 | True | 1/1 |
| 27-a-letter-from-a-market-stall | 0.1961 | 0.1941 | True | 1/1 |
| 28-describe-a-hiking-hut-on-a | 0.1881 | -0.9018 | True | 1/1 |
| 29-a-500-word-scene-in-a | 0.2662 | 0.1956 | True | 1/1 |
| 30-write-about-500-words-on-an | 0.2331 | 0.1954 | True | 1/1 |
| 31-explain-printing-a-local-newspaper-as | -0.8013 | -0.8897 | True | 0/1 |
| 32-a-short-story-about-walking-other | 0.2555 | -0.8421 | True | 1/1 |
| 33-describe-a-fishing-village-in-january | 0.1463 | -0.8793 | True | 1/1 |
| 34-a-letter-from-a-night-train | 0.2573 | 0.2714 | False | 1/1 |
| 35-write-about-500-words-as-someone | 0.2193 | -0.8969 | True | 1/1 |
| 36-a-500-word-scene-in-a | 0.2004 | 0.2006 | False | 1/1 |
| 37-describe-a-rooftop-greenhouse-that-is | 0.2418 | -0.7111 | True | 1/1 |
| 38-a-short-story-about-neighbours-sharing | -0.8787 | 0.2488 | False | 0/1 |
| 39-write-about-500-words-on-a | 0.1651 | 0.2017 | False | 1/1 |
| 40-a-letter-from-a-retired-teacher | 0.2528 | 0.2943 | False | 1/1 |

