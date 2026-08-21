# Key-free blind eval (leave-one-prompt-out)

Accuracy: **31/40** (0.775). context_len=1 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.1784 | -0.1694 | False |
| 02-explain-how-a-municipal-library-actually | -0.1846 | -0.2574 | True |
| 03-a-short-story-about-two-neighbours | -0.1744 | -0.2400 | True |
| 04-describe-a-rainy-tuesday-commute-in | -0.1059 | -0.1881 | True |
| 05-write-600-words-on-why-people | -0.2533 | -0.1752 | False |
| 06-a-letter-from-a-retired-ferry | 1.9828 | -0.3257 | True |
| 07-explain-sourdough-as-if-you-have | -0.2583 | -0.2147 | False |
| 08-a-600-word-scene-in-a | 1.8238 | -0.1768 | True |
| 09-write-about-500-words-as-a | -0.0917 | -0.2092 | True |
| 10-describe-a-weekday-morning-in-a | -0.1834 | -0.2126 | True |
| 11-a-short-story-about-a-chess | -0.0369 | -0.0514 | True |
| 12-a-letter-from-someone-who-just | 2.1060 | -0.2470 | True |
| 13-write-about-500-words-on-a | -0.0978 | -0.1158 | True |
| 14-describe-the-last-hour-of-a | -0.1672 | -0.1352 | False |
| 15-a-500-word-scene-in-a | -0.1943 | -0.2540 | True |
| 16-explain-ice-fishing-as-if-you | -0.2493 | -0.1912 | False |
| 17-write-about-500-words-as-a | -0.1623 | -0.2290 | True |
| 18-a-short-story-about-two-people | -0.1185 | -0.0446 | False |
| 19-describe-an-allotment-garden-in-late | 1.6705 | -0.2574 | True |
| 20-a-letter-from-a-lighthouse-keeper | 2.0203 | -0.1405 | True |
| 21-write-about-500-words-on-a | 2.1236 | -0.1433 | True |
| 22-a-500-word-scene-in-a | 1.9200 | -0.2397 | True |
| 23-describe-a-night-receptionist-in-a | -0.2278 | -0.1350 | False |
| 24-explain-bicycle-repair-as-if-you | -0.2047 | -0.1710 | False |
| 25-a-short-story-about-a-community | 1.8403 | -0.0927 | True |
| 26-write-about-500-words-as-a | -0.2071 | -0.2352 | True |
| 27-a-letter-from-a-market-stall | 1.8771 | -0.2605 | True |
| 28-describe-a-hiking-hut-on-a | -0.0957 | -0.2515 | True |
| 29-a-500-word-scene-in-a | 1.9264 | -0.2394 | True |
| 30-write-about-500-words-on-an | 1.9637 | -0.2330 | True |
| 31-explain-printing-a-local-newspaper-as | -0.1480 | -0.2264 | True |
| 32-a-short-story-about-walking-other | -0.1533 | -0.2255 | True |
| 33-describe-a-fishing-village-in-january | -0.1910 | -0.2199 | True |
| 34-a-letter-from-a-night-train | 2.1984 | -0.3530 | True |
| 35-write-about-500-words-as-someone | -0.2243 | -0.2036 | False |
| 36-a-500-word-scene-in-a | 1.7470 | -0.2300 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.0918 | -0.1883 | True |
| 38-a-short-story-about-neighbours-sharing | 1.8383 | -0.1051 | True |
| 39-write-about-500-words-on-a | 2.0284 | -0.2052 | True |
| 40-a-letter-from-a-retired-teacher | 2.0188 | -0.3078 | True |

