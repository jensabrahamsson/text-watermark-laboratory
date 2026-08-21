# Key-free blind eval (leave-one-prompt-out)

Accuracy: **24/37** (0.649). context_len=4 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | 0.0032 | 0.0020 | True |
| 02-explain-how-a-municipal-library-actually | -0.0068 | -0.0489 | True |
| 03-a-short-story-about-two-neighbours | 0.0596 | 0.0401 | True |
| 04-describe-a-rainy-tuesday-commute-in | 0.0116 | 0.0057 | True |
| 05-write-600-words-on-why-people | -0.0208 | -0.0380 | True |
| 06-a-letter-from-a-retired-ferry | -0.0032 | 0.0033 | False |
| 07-explain-sourdough-as-if-you-have | -0.0315 | -0.0192 | False |
| 08-a-600-word-scene-in-a | 0.0454 | 0.0445 | True |
| 09-write-about-500-words-as-a | 0.0410 | -0.0179 | True |
| 10-describe-a-weekday-morning-in-a | 0.0224 | -0.0365 | True |
| 11-a-short-story-about-a-chess | 0.0511 | 0.0835 | False |
| 12-a-letter-from-someone-who-just | 0.0180 | 0.0191 | False |
| 13-write-about-500-words-on-a | -0.0347 | -0.0401 | True |
| 14-describe-the-last-hour-of-a | 0.0061 | -0.0511 | True |
| 15-a-500-word-scene-in-a | 0.0418 | -0.0088 | True |
| 16-explain-ice-fishing-as-if-you | 0.0317 | 0.0251 | True |
| 17-write-about-500-words-as-a | 0.0441 | 0.0154 | True |
| 18-a-short-story-about-two-people | 0.0694 | -0.0823 | True |
| 19-describe-an-allotment-garden-in-late | -0.0414 | 0.0205 | False |
| 20-a-letter-from-a-lighthouse-keeper | 0.0194 | 0.0020 | True |
| 21-write-about-500-words-on-a | -0.0141 | 0.0216 | False |
| 22-a-500-word-scene-in-a | 0.0489 | -0.0491 | True |
| 23-describe-a-night-receptionist-in-a | 0.0761 | 0.0025 | True |
| 24-explain-bicycle-repair-as-if-you | -0.0341 | -0.0112 | False |
| 25-a-short-story-about-a-community | 0.0629 | 0.0295 | True |
| 26-write-about-500-words-as-a | 0.0189 | 0.0211 | False |
| 27-a-letter-from-a-market-stall | -0.0514 | 0.0063 | False |
| 28-describe-a-hiking-hut-on-a | 0.0488 | 0.0462 | True |
| 29-a-500-word-scene-in-a | 0.0466 | 0.0316 | True |
| 30-write-about-500-words-on-an | 0.0856 | -0.0445 | True |
| 31-explain-printing-a-local-newspaper-as | 0.0248 | 0.0423 | False |
| 32-a-short-story-about-walking-other | 0.0177 | 0.0591 | False |
| 33-describe-a-fishing-village-in-january | 0.0773 | 0.0134 | True |
| 34-a-letter-from-a-night-train | 0.0448 | -0.0082 | True |
| 35-write-about-500-words-as-someone | -0.0270 | -0.0090 | False |
| 36-a-500-word-scene-in-a | 0.0422 | -0.0115 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.0189 | 0.0058 | False |

