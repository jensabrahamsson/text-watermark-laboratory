# Key-free blind eval (leave-one-prompt-out)

Accuracy: **20/38** (0.526). context_len=4 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.0011 | -0.0022 | True |
| 02-explain-how-a-municipal-library-actually | -0.0402 | -0.0196 | False |
| 03-a-short-story-about-two-neighbours | -0.0458 | 0.0898 | False |
| 04-describe-a-rainy-tuesday-commute-in | -0.0123 | 0.0052 | False |
| 05-write-600-words-on-why-people | 0.0024 | -0.0108 | True |
| 06-a-letter-from-a-retired-ferry | -0.0086 | -0.0181 | True |
| 07-explain-sourdough-as-if-you-have | 0.0309 | 0.0006 | True |
| 08-a-600-word-scene-in-a | 0.0109 | 0.0277 | False |
| 09-write-about-500-words-as-a | -0.0067 | -0.0295 | True |
| 10-describe-a-weekday-morning-in-a | 0.0256 | 0.0446 | False |
| 11-a-short-story-about-a-chess | -0.0217 | -0.0618 | True |
| 12-a-letter-from-someone-who-just | -0.0261 | -0.0547 | True |
| 13-write-about-500-words-on-a | -0.0152 | -0.0043 | False |
| 14-describe-the-last-hour-of-a | -0.0039 | 0.0094 | False |
| 15-a-500-word-scene-in-a | 0.0081 | -0.0704 | True |
| 16-explain-ice-fishing-as-if-you | -0.0455 | -0.0160 | False |
| 17-write-about-500-words-as-a | 0.0444 | -0.0362 | True |
| 18-a-short-story-about-two-people | 0.0092 | -0.0394 | True |
| 19-describe-an-allotment-garden-in-late | 0.0530 | 0.0309 | True |
| 20-a-letter-from-a-lighthouse-keeper | -0.0659 | -0.0230 | False |
| 21-write-about-500-words-on-a | 0.0611 | 0.0624 | False |
| 22-a-500-word-scene-in-a | 0.0361 | -0.0484 | True |
| 23-describe-a-night-receptionist-in-a | 0.0504 | 0.0397 | True |
| 24-explain-bicycle-repair-as-if-you | 0.0205 | 0.0244 | False |
| 25-a-short-story-about-a-community | 0.0705 | -0.0395 | True |
| 26-write-about-500-words-as-a | -0.0247 | 0.0128 | False |
| 27-a-letter-from-a-market-stall | 0.0087 | 0.0540 | False |
| 28-describe-a-hiking-hut-on-a | -0.0328 | 0.0456 | False |
| 29-a-500-word-scene-in-a | 0.0051 | 0.0366 | False |
| 30-write-about-500-words-on-an | -0.0385 | -0.0518 | True |
| 31-explain-printing-a-local-newspaper-as | 0.0401 | -0.0069 | True |
| 32-a-short-story-about-walking-other | 0.0334 | -0.0206 | True |
| 33-describe-a-fishing-village-in-january | 0.0904 | -0.0232 | True |
| 34-a-letter-from-a-night-train | 0.0179 | -0.0643 | True |
| 35-write-about-500-words-as-someone | -0.0668 | -0.0113 | False |
| 36-a-500-word-scene-in-a | 0.0380 | 0.0272 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.0147 | 0.0337 | False |
| 38-a-short-story-about-neighbours-sharing | -0.0604 | 0.0211 | False |

