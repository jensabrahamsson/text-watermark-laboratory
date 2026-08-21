# Key-free blind eval (leave-one-prompt-out)

Accuracy: **29/40** (0.725). context_len=4 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | 0.0142 | -0.0023 | True |
| 02-explain-how-a-municipal-library-actually | -0.0521 | -0.0046 | False |
| 03-a-short-story-about-two-neighbours | -0.0011 | 0.1141 | False |
| 04-describe-a-rainy-tuesday-commute-in | 0.0279 | -0.0195 | True |
| 05-write-600-words-on-why-people | -0.0436 | -0.0128 | False |
| 06-a-letter-from-a-retired-ferry | 0.0176 | -0.0188 | True |
| 07-explain-sourdough-as-if-you-have | -0.0150 | 0.0152 | False |
| 08-a-600-word-scene-in-a | 0.0334 | -0.0058 | True |
| 09-write-about-500-words-as-a | 0.0086 | -0.0175 | True |
| 10-describe-a-weekday-morning-in-a | 0.0253 | -0.0103 | True |
| 11-a-short-story-about-a-chess | 0.0928 | 0.0546 | True |
| 12-a-letter-from-someone-who-just | -0.0051 | 0.0382 | False |
| 13-write-about-500-words-on-a | -0.0323 | -0.0941 | True |
| 14-describe-the-last-hour-of-a | -0.0312 | -0.0948 | True |
| 15-a-500-word-scene-in-a | 0.0421 | -0.0072 | True |
| 16-explain-ice-fishing-as-if-you | 0.0378 | -0.0316 | True |
| 17-write-about-500-words-as-a | 0.0212 | -0.0264 | True |
| 18-a-short-story-about-two-people | 0.1482 | -0.0093 | True |
| 19-describe-an-allotment-garden-in-late | 0.0520 | -0.0181 | True |
| 20-a-letter-from-a-lighthouse-keeper | -0.0072 | -0.0124 | True |
| 21-write-about-500-words-on-a | 0.0472 | 0.0308 | True |
| 22-a-500-word-scene-in-a | 0.0263 | 0.0023 | True |
| 23-describe-a-night-receptionist-in-a | 0.0689 | 0.0519 | True |
| 24-explain-bicycle-repair-as-if-you | -0.0370 | -0.0215 | False |
| 25-a-short-story-about-a-community | 0.1224 | 0.0664 | True |
| 26-write-about-500-words-as-a | -0.0145 | 0.0065 | False |
| 27-a-letter-from-a-market-stall | -0.0022 | -0.0054 | True |
| 28-describe-a-hiking-hut-on-a | 0.0264 | 0.0009 | True |
| 29-a-500-word-scene-in-a | 0.0651 | 0.0464 | True |
| 30-write-about-500-words-on-an | 0.0160 | -0.0456 | True |
| 31-explain-printing-a-local-newspaper-as | 0.0875 | 0.0523 | True |
| 32-a-short-story-about-walking-other | 0.0142 | -0.0290 | True |
| 33-describe-a-fishing-village-in-january | 0.0613 | 0.0080 | True |
| 34-a-letter-from-a-night-train | 0.0019 | 0.0115 | False |
| 35-write-about-500-words-as-someone | -0.0289 | -0.0109 | False |
| 36-a-500-word-scene-in-a | 0.0310 | 0.0251 | True |
| 37-describe-a-rooftop-greenhouse-that-is | 0.0005 | 0.0288 | False |
| 38-a-short-story-about-neighbours-sharing | 0.0359 | 0.0074 | True |
| 39-write-about-500-words-on-a | 0.0534 | 0.0890 | False |
| 40-a-letter-from-a-retired-teacher | -0.0323 | -0.0704 | True |

