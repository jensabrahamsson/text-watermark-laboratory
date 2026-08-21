# Key-free blind eval (leave-one-prompt-out)

Accuracy: **19/38** (0.500). context_len=4 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | 0.0067 | -0.0014 | True |
| 02-explain-how-a-municipal-library-actually | -0.0449 | -0.0208 | False |
| 03-a-short-story-about-two-neighbours | -0.0408 | 0.0677 | False |
| 04-describe-a-rainy-tuesday-commute-in | 0.0195 | 0.0102 | True |
| 05-write-600-words-on-why-people | -0.0039 | -0.0227 | True |
| 06-a-letter-from-a-retired-ferry | -0.0056 | -0.0131 | True |
| 07-explain-sourdough-as-if-you-have | 0.0353 | 0.0182 | True |
| 08-a-600-word-scene-in-a | 0.0040 | 0.0264 | False |
| 09-write-about-500-words-as-a | 0.0084 | -0.0273 | True |
| 10-describe-a-weekday-morning-in-a | 0.0319 | 0.0361 | False |
| 11-a-short-story-about-a-chess | -0.0184 | -0.0659 | True |
| 12-a-letter-from-someone-who-just | -0.0039 | -0.0623 | True |
| 13-write-about-500-words-on-a | -0.0103 | -0.0010 | False |
| 14-describe-the-last-hour-of-a | -0.0129 | 0.0267 | False |
| 15-a-500-word-scene-in-a | 0.0136 | -0.0645 | True |
| 16-explain-ice-fishing-as-if-you | -0.0397 | -0.0117 | False |
| 17-write-about-500-words-as-a | 0.0521 | -0.0328 | True |
| 18-a-short-story-about-two-people | 0.0190 | -0.0403 | True |
| 19-describe-an-allotment-garden-in-late | 0.0264 | 0.0289 | False |
| 20-a-letter-from-a-lighthouse-keeper | -0.0686 | -0.0278 | False |
| 21-write-about-500-words-on-a | 0.0623 | 0.0614 | True |
| 22-a-500-word-scene-in-a | 0.0559 | -0.0170 | True |
| 23-describe-a-night-receptionist-in-a | 0.0211 | 0.0392 | False |
| 24-explain-bicycle-repair-as-if-you | 0.0133 | 0.0207 | False |
| 25-a-short-story-about-a-community | 0.0651 | -0.0381 | True |
| 26-write-about-500-words-as-a | -0.0265 | 0.0025 | False |
| 27-a-letter-from-a-market-stall | -0.0083 | 0.0539 | False |
| 28-describe-a-hiking-hut-on-a | -0.0208 | 0.0398 | False |
| 29-a-500-word-scene-in-a | 0.0078 | 0.0267 | False |
| 30-write-about-500-words-on-an | -0.0394 | -0.0398 | True |
| 31-explain-printing-a-local-newspaper-as | 0.0456 | -0.0008 | True |
| 32-a-short-story-about-walking-other | 0.0127 | -0.0147 | True |
| 33-describe-a-fishing-village-in-january | 0.0804 | -0.0338 | True |
| 34-a-letter-from-a-night-train | -0.0021 | -0.0696 | True |
| 35-write-about-500-words-as-someone | -0.0597 | -0.0102 | False |
| 36-a-500-word-scene-in-a | 0.0481 | 0.0579 | False |
| 37-describe-a-rooftop-greenhouse-that-is | -0.0181 | 0.0184 | False |
| 38-a-short-story-about-neighbours-sharing | -0.0654 | -0.0067 | False |

