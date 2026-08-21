# Key-free blind eval (leave-one-prompt-out)

Accuracy: **28/37** (0.757). context_len=1 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | 0.0997 | 0.0579 | True |
| 02-explain-how-a-municipal-library-actually | -0.0020 | -0.0092 | True |
| 03-a-short-story-about-two-neighbours | 0.0350 | 0.0747 | False |
| 04-describe-a-rainy-tuesday-commute-in | 0.0288 | -0.0484 | True |
| 05-write-600-words-on-why-people | -0.0084 | -0.0360 | True |
| 06-a-letter-from-a-retired-ferry | 0.0037 | -0.1284 | True |
| 07-explain-sourdough-as-if-you-have | 0.0507 | -0.0347 | True |
| 08-a-600-word-scene-in-a | 0.1030 | -0.0129 | True |
| 09-write-about-500-words-as-a | 0.0751 | -0.0418 | True |
| 10-describe-a-weekday-morning-in-a | 0.0329 | 0.1276 | False |
| 11-a-short-story-about-a-chess | 0.1112 | 0.0880 | True |
| 12-a-letter-from-someone-who-just | -0.0248 | -0.0367 | True |
| 13-write-about-500-words-on-a | 0.0151 | 0.0052 | True |
| 14-describe-the-last-hour-of-a | 0.0575 | -0.1067 | True |
| 15-a-500-word-scene-in-a | 0.1282 | -0.0430 | True |
| 16-explain-ice-fishing-as-if-you | -0.0199 | 0.0247 | False |
| 17-write-about-500-words-as-a | 0.0864 | 0.0046 | True |
| 18-a-short-story-about-two-people | -0.0151 | -0.0444 | True |
| 19-describe-an-allotment-garden-in-late | 0.0941 | -0.0017 | True |
| 20-a-letter-from-a-lighthouse-keeper | 0.0344 | 0.0058 | True |
| 21-write-about-500-words-on-a | 0.0875 | 0.0965 | False |
| 22-a-500-word-scene-in-a | 0.0786 | -0.0218 | True |
| 23-describe-a-night-receptionist-in-a | 0.0054 | -0.0057 | True |
| 24-explain-bicycle-repair-as-if-you | -0.0287 | -0.0130 | False |
| 25-a-short-story-about-a-community | 0.0433 | -0.0170 | True |
| 26-write-about-500-words-as-a | 0.1246 | 0.1310 | False |
| 27-a-letter-from-a-market-stall | 0.0243 | 0.0852 | False |
| 28-describe-a-hiking-hut-on-a | -0.0232 | 0.0190 | False |
| 29-a-500-word-scene-in-a | 0.1161 | -0.0217 | True |
| 30-write-about-500-words-on-an | 0.0485 | -0.0173 | True |
| 31-explain-printing-a-local-newspaper-as | 0.0398 | 0.0005 | True |
| 32-a-short-story-about-walking-other | 0.0838 | 0.0074 | True |
| 33-describe-a-fishing-village-in-january | -0.0376 | -0.0282 | False |
| 34-a-letter-from-a-night-train | -0.0030 | -0.0061 | True |
| 35-write-about-500-words-as-someone | 0.1595 | -0.0147 | True |
| 36-a-500-word-scene-in-a | 0.0924 | 0.0224 | True |
| 37-describe-a-rooftop-greenhouse-that-is | 0.0252 | -0.0477 | True |

