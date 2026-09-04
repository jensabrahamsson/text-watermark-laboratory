# Key-free blind eval (leave-one-prompt-out)

Accuracy: **19/40** (0.475). context_len=4 backoff=False margin=0.

Ranking wins with no isolated TP: **3/19** (05-write-600-words-on-why-people, 24-explain-bicycle-repair-as-if-you, 35-write-about-500-words-as-someone). Ranking losses with isolated TP: **4** (13-write-about-500-words-on-a, 15-a-500-word-scene-in-a, 17-write-about-500-words-as-a, 38-a-short-story-about-neighbours-sharing). Isolated marked `lr>0`: **20**. Prompt ranking is not per-file accuracy.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |
|---|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.1323 | 0.0105 | False | 0/1 |
| 02-explain-how-a-municipal-library-actually | -0.0334 | 0.0234 | False | 0/1 |
| 03-a-short-story-about-two-neighbours | -0.0495 | 0.0361 | False | 0/1 |
| 04-describe-a-rainy-tuesday-commute-in | -0.0712 | 0.0196 | False | 0/1 |
| 05-write-600-words-on-why-people | -0.0218 | -0.0377 | True | 0/1 |
| 06-a-letter-from-a-retired-ferry | 0.0296 | -0.0212 | True | 1/1 |
| 07-explain-sourdough-as-if-you-have | 0.0275 | 0.0268 | True | 1/1 |
| 08-a-600-word-scene-in-a | 0.0294 | -0.0157 | True | 1/1 |
| 09-write-about-500-words-as-a | -0.0083 | 0.0093 | False | 0/1 |
| 10-describe-a-weekday-morning-in-a | -0.0564 | -0.0250 | False | 0/1 |
| 11-a-short-story-about-a-chess | -0.0200 | 0.0353 | False | 0/1 |
| 12-a-letter-from-someone-who-just | -0.0191 | 0.0075 | False | 0/1 |
| 13-write-about-500-words-on-a | 0.0092 | 0.0130 | False | 1/1 |
| 14-describe-the-last-hour-of-a | -0.0380 | 0.0496 | False | 0/1 |
| 15-a-500-word-scene-in-a | 0.0543 | 0.0581 | False | 1/1 |
| 16-explain-ice-fishing-as-if-you | 0.0525 | -0.0266 | True | 1/1 |
| 17-write-about-500-words-as-a | 0.0370 | 0.0479 | False | 1/1 |
| 18-a-short-story-about-two-people | 0.0092 | -0.0410 | True | 1/1 |
| 19-describe-an-allotment-garden-in-late | -0.0188 | -0.0093 | False | 0/1 |
| 20-a-letter-from-a-lighthouse-keeper | -0.0034 | 0.0315 | False | 0/1 |
| 21-write-about-500-words-on-a | 0.0338 | 0.0165 | True | 1/1 |
| 22-a-500-word-scene-in-a | 0.0349 | 0.0275 | True | 1/1 |
| 23-describe-a-night-receptionist-in-a | 0.1047 | 0.0473 | True | 1/1 |
| 24-explain-bicycle-repair-as-if-you | -0.0038 | -0.0090 | True | 0/1 |
| 25-a-short-story-about-a-community | -0.1140 | -0.0024 | False | 0/1 |
| 26-write-about-500-words-as-a | 0.0288 | 0.0276 | True | 1/1 |
| 27-a-letter-from-a-market-stall | -0.0146 | 0.0383 | False | 0/1 |
| 28-describe-a-hiking-hut-on-a | 0.0630 | 0.0156 | True | 1/1 |
| 29-a-500-word-scene-in-a | -0.0195 | -0.0060 | False | 0/1 |
| 30-write-about-500-words-on-an | 0.0013 | -0.0617 | True | 1/1 |
| 31-explain-printing-a-local-newspaper-as | -0.0321 | 0.0035 | False | 0/1 |
| 32-a-short-story-about-walking-other | 0.0146 | -0.0321 | True | 1/1 |
| 33-describe-a-fishing-village-in-january | -0.0192 | 0.0233 | False | 0/1 |
| 34-a-letter-from-a-night-train | 0.0290 | 0.0122 | True | 1/1 |
| 35-write-about-500-words-as-someone | -0.0287 | -0.0955 | True | 0/1 |
| 36-a-500-word-scene-in-a | 0.0817 | -0.0341 | True | 1/1 |
| 37-describe-a-rooftop-greenhouse-that-is | 0.0081 | -0.0111 | True | 1/1 |
| 38-a-short-story-about-neighbours-sharing | 0.0472 | 0.0898 | False | 1/1 |
| 39-write-about-500-words-on-a | 0.0552 | 0.0352 | True | 1/1 |
| 40-a-letter-from-a-retired-teacher | -0.0193 | 0.0039 | False | 0/1 |

