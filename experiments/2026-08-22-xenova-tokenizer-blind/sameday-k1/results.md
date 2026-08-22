# Key-free blind eval (leave-one-prompt-out)

Accuracy: **21/38** (0.553). context_len=1 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.0441 | 0.0314 | False |
| 02-explain-how-a-municipal-library-actually | 0.0518 | 0.0242 | True |
| 03-a-short-story-about-two-neighbours | 0.0731 | 0.0566 | True |
| 04-describe-a-rainy-tuesday-commute-in | 0.0673 | -0.0126 | True |
| 05-write-600-words-on-why-people | 0.0007 | 0.0224 | False |
| 06-a-letter-from-a-retired-ferry | 0.0050 | 0.0149 | False |
| 07-explain-sourdough-as-if-you-have | -0.0328 | -0.0995 | True |
| 08-a-600-word-scene-in-a | -0.0126 | -0.0452 | True |
| 09-write-about-500-words-as-a | -0.0219 | 0.0306 | False |
| 10-describe-a-weekday-morning-in-a | -0.0505 | 0.0083 | False |
| 11-a-short-story-about-a-chess | -0.0273 | -0.0794 | True |
| 12-a-letter-from-someone-who-just | 0.0055 | 0.0041 | True |
| 13-write-about-500-words-on-a | -0.0692 | -0.0004 | False |
| 14-describe-the-last-hour-of-a | 0.0479 | 0.0016 | True |
| 15-a-500-word-scene-in-a | 0.0096 | -0.0157 | True |
| 16-explain-ice-fishing-as-if-you | 0.0187 | 0.0391 | False |
| 17-write-about-500-words-as-a | -0.0245 | -0.0870 | True |
| 18-a-short-story-about-two-people | -0.0068 | -0.0461 | True |
| 19-describe-an-allotment-garden-in-late | 0.0713 | -0.0688 | True |
| 20-a-letter-from-a-lighthouse-keeper | -0.0556 | -0.0124 | False |
| 21-write-about-500-words-on-a | 0.0055 | -0.0533 | True |
| 22-a-500-word-scene-in-a | 0.0147 | 0.0083 | True |
| 23-describe-a-night-receptionist-in-a | 0.0126 | 0.0089 | True |
| 24-explain-bicycle-repair-as-if-you | -0.0351 | 0.0047 | False |
| 25-a-short-story-about-a-community | 0.0320 | 0.0202 | True |
| 26-write-about-500-words-as-a | -0.0244 | 0.0119 | False |
| 27-a-letter-from-a-market-stall | -0.0884 | -0.0784 | False |
| 28-describe-a-hiking-hut-on-a | 0.0069 | 0.0467 | False |
| 29-a-500-word-scene-in-a | -0.0340 | 0.0009 | False |
| 30-write-about-500-words-on-an | 0.1217 | 0.0678 | True |
| 31-explain-printing-a-local-newspaper-as | -0.0030 | 0.0036 | False |
| 32-a-short-story-about-walking-other | 0.0303 | 0.0103 | True |
| 33-describe-a-fishing-village-in-january | 0.0168 | 0.0362 | False |
| 34-a-letter-from-a-night-train | 0.0093 | -0.0177 | True |
| 35-write-about-500-words-as-someone | -0.0093 | -0.0748 | True |
| 36-a-500-word-scene-in-a | -0.0496 | -0.0082 | False |
| 37-describe-a-rooftop-greenhouse-that-is | -0.0183 | -0.0244 | True |
| 38-a-short-story-about-neighbours-sharing | 0.0020 | 0.0439 | False |

