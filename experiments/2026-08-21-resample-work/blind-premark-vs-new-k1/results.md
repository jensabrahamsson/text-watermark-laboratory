# Key-free blind eval (leave-one-prompt-out)

Accuracy: **33/40** (0.825). context_len=1 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.1109 | -0.1157 | True |
| 02-explain-how-a-municipal-library-actually | -0.1952 | -0.1578 | False |
| 03-a-short-story-about-two-neighbours | -0.1131 | -0.1980 | True |
| 04-describe-a-rainy-tuesday-commute-in | -0.1512 | -0.1384 | False |
| 05-write-600-words-on-why-people | -0.2868 | -0.1593 | False |
| 06-a-letter-from-a-retired-ferry | 2.3266 | -0.3255 | True |
| 07-explain-sourdough-as-if-you-have | -0.2793 | -0.2209 | False |
| 08-a-600-word-scene-in-a | 2.0892 | -0.2384 | True |
| 09-write-about-500-words-as-a | -0.0185 | -0.2480 | True |
| 10-describe-a-weekday-morning-in-a | -0.1249 | -0.1496 | True |
| 11-a-short-story-about-a-chess | 0.0070 | -0.1520 | True |
| 12-a-letter-from-someone-who-just | 2.5289 | -0.2704 | True |
| 13-write-about-500-words-on-a | -0.0501 | -0.2149 | True |
| 14-describe-the-last-hour-of-a | -0.1311 | -0.1820 | True |
| 15-a-500-word-scene-in-a | -0.0688 | -0.2603 | True |
| 16-explain-ice-fishing-as-if-you | -0.2502 | -0.1151 | False |
| 17-write-about-500-words-as-a | -0.0371 | -0.2659 | True |
| 18-a-short-story-about-two-people | -0.1307 | -0.1812 | True |
| 19-describe-an-allotment-garden-in-late | 2.0474 | -0.1984 | True |
| 20-a-letter-from-a-lighthouse-keeper | 2.3644 | -0.1469 | True |
| 21-write-about-500-words-on-a | 2.4278 | -0.1663 | True |
| 22-a-500-word-scene-in-a | 2.2197 | -0.2897 | True |
| 23-describe-a-night-receptionist-in-a | -0.1172 | -0.2510 | True |
| 24-explain-bicycle-repair-as-if-you | -0.2118 | -0.1767 | False |
| 25-a-short-story-about-a-community | 2.0747 | -0.1553 | True |
| 26-write-about-500-words-as-a | -0.1491 | -0.1407 | False |
| 27-a-letter-from-a-market-stall | 2.1916 | -0.2198 | True |
| 28-describe-a-hiking-hut-on-a | -0.0163 | -0.1118 | True |
| 29-a-500-word-scene-in-a | 2.2165 | -0.2200 | True |
| 30-write-about-500-words-on-an | 2.4059 | -0.2195 | True |
| 31-explain-printing-a-local-newspaper-as | -0.0667 | -0.1430 | True |
| 32-a-short-story-about-walking-other | -0.0462 | -0.1882 | True |
| 33-describe-a-fishing-village-in-january | -0.0808 | -0.2317 | True |
| 34-a-letter-from-a-night-train | 2.6140 | -0.2990 | True |
| 35-write-about-500-words-as-someone | -0.1341 | -0.2237 | True |
| 36-a-500-word-scene-in-a | 1.9683 | -0.2041 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.0481 | -0.2915 | True |
| 38-a-short-story-about-neighbours-sharing | 2.1167 | 0.0225 | True |
| 39-write-about-500-words-on-a | 2.3848 | -0.1526 | True |
| 40-a-letter-from-a-retired-teacher | 2.3615 | -0.2598 | True |

