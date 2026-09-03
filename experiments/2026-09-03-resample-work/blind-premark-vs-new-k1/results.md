# Key-free blind eval (leave-one-prompt-out)

Accuracy: **37/40** (0.925). context_len=1 backoff=False margin=0.

Ranking wins with no isolated TP: **5/37** (07-explain-sourdough-as-if-you-have, 18-a-short-story-about-two-people, 24-explain-bicycle-repair-as-if-you, 31-explain-printing-a-local-newspaper-as, 38-a-short-story-about-neighbours-sharing). Ranking losses with isolated TP: **0**. Isolated marked `lr>0`: **32**. Prompt ranking is not per-file accuracy.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher | Marked files >0 |
|---|---|---|---|---|
| 01-write-a-600-word-travel-essay | 2.9925 | -0.5002 | True | 1/1 |
| 02-explain-how-a-municipal-library-actually | -0.5082 | -0.4957 | False | 0/1 |
| 03-a-short-story-about-two-neighbours | 2.6245 | -0.4009 | True | 1/1 |
| 04-describe-a-rainy-tuesday-commute-in | 2.6776 | -0.4333 | True | 1/1 |
| 05-write-600-words-on-why-people | -0.5555 | -0.4788 | False | 0/1 |
| 06-a-letter-from-a-retired-ferry | 2.7309 | -0.5356 | True | 1/1 |
| 07-explain-sourdough-as-if-you-have | -0.4433 | -0.4707 | True | 0/1 |
| 08-a-600-word-scene-in-a | 2.6618 | -0.5324 | True | 1/1 |
| 09-write-about-500-words-as-a | 3.0587 | -0.6668 | True | 1/1 |
| 10-describe-a-weekday-morning-in-a | 2.8225 | -0.4027 | True | 1/1 |
| 11-a-short-story-about-a-chess | 2.5937 | -0.4059 | True | 1/1 |
| 12-a-letter-from-someone-who-just | 2.9569 | -0.4602 | True | 1/1 |
| 13-write-about-500-words-on-a | 2.8047 | -0.5377 | True | 1/1 |
| 14-describe-the-last-hour-of-a | 2.8760 | -0.5907 | True | 1/1 |
| 15-a-500-word-scene-in-a | 2.3798 | -0.4316 | True | 1/1 |
| 16-explain-ice-fishing-as-if-you | -0.5023 | -0.4894 | False | 0/1 |
| 17-write-about-500-words-as-a | 2.9532 | -0.5468 | True | 1/1 |
| 18-a-short-story-about-two-people | -0.5612 | -0.5710 | True | 0/1 |
| 19-describe-an-allotment-garden-in-late | 2.6348 | -0.3834 | True | 1/1 |
| 20-a-letter-from-a-lighthouse-keeper | 2.8882 | -0.4353 | True | 1/1 |
| 21-write-about-500-words-on-a | 2.9357 | -0.4923 | True | 1/1 |
| 22-a-500-word-scene-in-a | 2.4794 | -0.4814 | True | 1/1 |
| 23-describe-a-night-receptionist-in-a | 2.8840 | -0.4757 | True | 1/1 |
| 24-explain-bicycle-repair-as-if-you | -0.4120 | -0.4229 | True | 0/1 |
| 25-a-short-story-about-a-community | 2.4758 | -0.4498 | True | 1/1 |
| 26-write-about-500-words-as-a | 2.8395 | -0.4262 | True | 1/1 |
| 27-a-letter-from-a-market-stall | 2.7162 | -0.4504 | True | 1/1 |
| 28-describe-a-hiking-hut-on-a | 2.7147 | -0.4892 | True | 1/1 |
| 29-a-500-word-scene-in-a | 2.4735 | -0.4833 | True | 1/1 |
| 30-write-about-500-words-on-an | 3.0218 | -0.5628 | True | 1/1 |
| 31-explain-printing-a-local-newspaper-as | -0.4177 | -0.4363 | True | 0/1 |
| 32-a-short-story-about-walking-other | 2.7509 | -0.4873 | True | 1/1 |
| 33-describe-a-fishing-village-in-january | 2.7868 | -0.5617 | True | 1/1 |
| 34-a-letter-from-a-night-train | 3.0963 | -0.5705 | True | 1/1 |
| 35-write-about-500-words-as-someone | 2.9455 | -0.5665 | True | 1/1 |
| 36-a-500-word-scene-in-a | 2.3474 | -0.4557 | True | 1/1 |
| 37-describe-a-rooftop-greenhouse-that-is | 2.8001 | -0.6299 | True | 1/1 |
| 38-a-short-story-about-neighbours-sharing | -0.3010 | -0.3701 | True | 0/1 |
| 39-write-about-500-words-on-a | 2.6343 | -0.6022 | True | 1/1 |
| 40-a-letter-from-a-retired-teacher | 2.8086 | -0.5622 | True | 1/1 |

