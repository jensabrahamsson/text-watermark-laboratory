# Key-free blind eval (leave-one-prompt-out)

Accuracy: **35/40** (0.875). context_len=1 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.1084 | -0.1105 | True |
| 02-explain-how-a-municipal-library-actually | -0.1512 | -0.1256 | False |
| 03-a-short-story-about-two-neighbours | -0.1651 | -0.2028 | True |
| 04-describe-a-rainy-tuesday-commute-in | -0.1266 | -0.1322 | True |
| 05-write-600-words-on-why-people | -0.2660 | -0.1609 | False |
| 06-a-letter-from-a-retired-ferry | 1.5773 | -0.2974 | True |
| 07-explain-sourdough-as-if-you-have | -0.2700 | -0.2171 | False |
| 08-a-600-word-scene-in-a | 1.4909 | -0.2105 | True |
| 09-write-about-500-words-as-a | -0.0480 | -0.2261 | True |
| 10-describe-a-weekday-morning-in-a | -0.1222 | -0.1294 | True |
| 11-a-short-story-about-a-chess | -0.0207 | -0.1286 | True |
| 12-a-letter-from-someone-who-just | 1.8076 | -0.2409 | True |
| 13-write-about-500-words-on-a | -0.0525 | -0.1964 | True |
| 14-describe-the-last-hour-of-a | -0.1407 | -0.1885 | True |
| 15-a-500-word-scene-in-a | -0.0938 | -0.2390 | True |
| 16-explain-ice-fishing-as-if-you | -0.2232 | -0.1018 | False |
| 17-write-about-500-words-as-a | -0.0892 | -0.2507 | True |
| 18-a-short-story-about-two-people | -0.1447 | -0.1695 | True |
| 19-describe-an-allotment-garden-in-late | 1.3422 | -0.1833 | True |
| 20-a-letter-from-a-lighthouse-keeper | 1.7372 | -0.1113 | True |
| 21-write-about-500-words-on-a | 1.7731 | -0.1068 | True |
| 22-a-500-word-scene-in-a | 1.6358 | -0.2561 | True |
| 23-describe-a-night-receptionist-in-a | -0.1323 | -0.2486 | True |
| 24-explain-bicycle-repair-as-if-you | -0.1923 | -0.1371 | False |
| 25-a-short-story-about-a-community | 1.5469 | -0.1711 | True |
| 26-write-about-500-words-as-a | -0.1228 | -0.1355 | True |
| 27-a-letter-from-a-market-stall | 1.5876 | -0.2000 | True |
| 28-describe-a-hiking-hut-on-a | -0.0184 | -0.1012 | True |
| 29-a-500-word-scene-in-a | 1.6502 | -0.2159 | True |
| 30-write-about-500-words-on-an | 1.5700 | -0.2190 | True |
| 31-explain-printing-a-local-newspaper-as | -0.0834 | -0.1380 | True |
| 32-a-short-story-about-walking-other | -0.0596 | -0.1656 | True |
| 33-describe-a-fishing-village-in-january | -0.0657 | -0.2240 | True |
| 34-a-letter-from-a-night-train | 1.8754 | -0.2738 | True |
| 35-write-about-500-words-as-someone | -0.1114 | -0.2085 | True |
| 36-a-500-word-scene-in-a | 1.4368 | -0.1833 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.0952 | -0.2676 | True |
| 38-a-short-story-about-neighbours-sharing | 1.4869 | -0.0008 | True |
| 39-write-about-500-words-on-a | 1.7846 | -0.1071 | True |
| 40-a-letter-from-a-retired-teacher | 1.7123 | -0.2413 | True |

