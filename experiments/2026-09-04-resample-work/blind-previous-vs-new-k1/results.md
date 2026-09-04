# Key-free blind eval (leave-one-prompt-out)

Accuracy: **20/40** (0.500). context_len=1 backoff=False margin=0.

Ranking wins with no isolated TP: **9/20** (06-a-letter-from-a-retired-ferry, 09-write-about-500-words-as-a, 12-a-letter-from-someone-who-just, 20-a-letter-from-a-lighthouse-keeper, 23-describe-a-night-receptionist-in-a, 27-a-letter-from-a-market-stall, 36-a-500-word-scene-in-a, 37-describe-a-rooftop-greenhouse-that-is, 40-a-letter-from-a-retired-teacher). Ranking losses with isolated TP: **3** (10-describe-a-weekday-morning-in-a, 18-a-short-story-about-two-people, 39-write-about-500-words-on-a). Isolated marked `lr>0`: **14**. Prompt ranking is not per-file accuracy.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |
|---|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.0890 | 0.0379 | False | 0/1 |
| 02-explain-how-a-municipal-library-actually | -0.0281 | -0.0136 | False | 0/1 |
| 03-a-short-story-about-two-neighbours | 0.0213 | 0.0008 | True | 1/1 |
| 04-describe-a-rainy-tuesday-commute-in | 0.0146 | -0.0194 | True | 1/1 |
| 05-write-600-words-on-why-people | -0.0145 | -0.0118 | False | 0/1 |
| 06-a-letter-from-a-retired-ferry | -0.0097 | -0.0153 | True | 0/1 |
| 07-explain-sourdough-as-if-you-have | 0.0159 | -0.0118 | True | 1/1 |
| 08-a-600-word-scene-in-a | 0.0039 | -0.0186 | True | 1/1 |
| 09-write-about-500-words-as-a | -0.0022 | -0.0045 | True | 0/1 |
| 10-describe-a-weekday-morning-in-a | 0.0358 | 0.0491 | False | 1/1 |
| 11-a-short-story-about-a-chess | 0.0193 | -0.0061 | True | 1/1 |
| 12-a-letter-from-someone-who-just | -0.0003 | -0.0116 | True | 0/1 |
| 13-write-about-500-words-on-a | 0.0419 | -0.0153 | True | 1/1 |
| 14-describe-the-last-hour-of-a | 0.0392 | -0.0337 | True | 1/1 |
| 15-a-500-word-scene-in-a | -0.0742 | -0.0277 | False | 0/1 |
| 16-explain-ice-fishing-as-if-you | -0.0538 | -0.0218 | False | 0/1 |
| 17-write-about-500-words-as-a | 0.0101 | -0.0112 | True | 1/1 |
| 18-a-short-story-about-two-people | 0.0354 | 0.0567 | False | 1/1 |
| 19-describe-an-allotment-garden-in-late | 0.0211 | 0.0043 | True | 1/1 |
| 20-a-letter-from-a-lighthouse-keeper | -0.0124 | -0.0505 | True | 0/1 |
| 21-write-about-500-words-on-a | -0.0277 | -0.0018 | False | 0/1 |
| 22-a-500-word-scene-in-a | -0.0168 | 0.0346 | False | 0/1 |
| 23-describe-a-night-receptionist-in-a | -0.0464 | -0.0467 | True | 0/1 |
| 24-explain-bicycle-repair-as-if-you | 0.0466 | 0.0173 | True | 1/1 |
| 25-a-short-story-about-a-community | -0.0008 | 0.0066 | False | 0/1 |
| 26-write-about-500-words-as-a | -0.0227 | -0.0166 | False | 0/1 |
| 27-a-letter-from-a-market-stall | -0.0132 | -0.0171 | True | 0/1 |
| 28-describe-a-hiking-hut-on-a | 0.0138 | 0.0076 | True | 1/1 |
| 29-a-500-word-scene-in-a | -0.0805 | -0.0703 | False | 0/1 |
| 30-write-about-500-words-on-an | -0.0293 | 0.0111 | False | 0/1 |
| 31-explain-printing-a-local-newspaper-as | -0.0492 | 0.0566 | False | 0/1 |
| 32-a-short-story-about-walking-other | -0.0205 | -0.0019 | False | 0/1 |
| 33-describe-a-fishing-village-in-january | -0.0445 | -0.0118 | False | 0/1 |
| 34-a-letter-from-a-night-train | -0.0295 | -0.0135 | False | 0/1 |
| 35-write-about-500-words-as-someone | -0.0251 | -0.0247 | False | 0/1 |
| 36-a-500-word-scene-in-a | -0.0367 | -0.0398 | True | 0/1 |
| 37-describe-a-rooftop-greenhouse-that-is | -0.0350 | -0.0428 | True | 0/1 |
| 38-a-short-story-about-neighbours-sharing | -0.0235 | 0.0126 | False | 0/1 |
| 39-write-about-500-words-on-a | 0.0675 | 0.0971 | False | 1/1 |
| 40-a-letter-from-a-retired-teacher | -0.0036 | -0.0636 | True | 0/1 |

