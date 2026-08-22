# Key-free blind eval (leave-one-prompt-out)

Accuracy: **30/40** (0.750). context_len=1 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.1711 | -0.1470 | False |
| 02-explain-how-a-municipal-library-actually | -0.1574 | -0.2407 | True |
| 03-a-short-story-about-two-neighbours | -0.1989 | -0.2687 | True |
| 04-describe-a-rainy-tuesday-commute-in | -0.0774 | -0.2293 | True |
| 05-write-600-words-on-why-people | -0.2352 | -0.1727 | False |
| 06-a-letter-from-a-retired-ferry | 1.5730 | -0.3181 | True |
| 07-explain-sourdough-as-if-you-have | -0.2404 | -0.1869 | False |
| 08-a-600-word-scene-in-a | 1.5206 | -0.1885 | True |
| 09-write-about-500-words-as-a | -0.1256 | -0.1864 | True |
| 10-describe-a-weekday-morning-in-a | -0.1880 | -0.1817 | False |
| 11-a-short-story-about-a-chess | -0.0567 | -0.0699 | True |
| 12-a-letter-from-someone-who-just | 1.6658 | -0.1926 | True |
| 13-write-about-500-words-on-a | -0.0988 | -0.1146 | True |
| 14-describe-the-last-hour-of-a | -0.1682 | -0.1364 | False |
| 15-a-500-word-scene-in-a | -0.2155 | -0.2571 | True |
| 16-explain-ice-fishing-as-if-you | -0.2039 | -0.1735 | False |
| 17-write-about-500-words-as-a | -0.1977 | -0.2334 | True |
| 18-a-short-story-about-two-people | -0.1356 | -0.0694 | False |
| 19-describe-an-allotment-garden-in-late | 1.2724 | -0.2732 | True |
| 20-a-letter-from-a-lighthouse-keeper | 1.6752 | -0.1668 | True |
| 21-write-about-500-words-on-a | 1.8023 | -0.1218 | True |
| 22-a-500-word-scene-in-a | 1.5760 | -0.2118 | True |
| 23-describe-a-night-receptionist-in-a | -0.2219 | -0.1385 | False |
| 24-explain-bicycle-repair-as-if-you | -0.2197 | -0.1511 | False |
| 25-a-short-story-about-a-community | 1.5099 | -0.1538 | True |
| 26-write-about-500-words-as-a | -0.1608 | -0.2594 | True |
| 27-a-letter-from-a-market-stall | 1.5549 | -0.2651 | True |
| 28-describe-a-hiking-hut-on-a | -0.1215 | -0.2370 | True |
| 29-a-500-word-scene-in-a | 1.6987 | -0.2114 | True |
| 30-write-about-500-words-on-an | 1.5855 | -0.2454 | True |
| 31-explain-printing-a-local-newspaper-as | -0.1384 | -0.2126 | True |
| 32-a-short-story-about-walking-other | -0.1734 | -0.2312 | True |
| 33-describe-a-fishing-village-in-january | -0.1858 | -0.2134 | True |
| 34-a-letter-from-a-night-train | 1.7489 | -0.3404 | True |
| 35-write-about-500-words-as-someone | -0.2257 | -0.2056 | False |
| 36-a-500-word-scene-in-a | 1.4254 | -0.2210 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.1616 | -0.1701 | True |
| 38-a-short-story-about-neighbours-sharing | 1.4839 | -0.1133 | True |
| 39-write-about-500-words-on-a | 1.6932 | -0.2153 | True |
| 40-a-letter-from-a-retired-teacher | 1.7135 | -0.2817 | True |

