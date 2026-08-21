# Key-free blind eval (leave-one-prompt-out)

Accuracy: **35/40** (0.875). context_len=4 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.4846 | -0.5160 | True |
| 02-explain-how-a-municipal-library-actually | -0.5346 | -0.4832 | False |
| 03-a-short-story-about-two-neighbours | -0.4384 | -0.5085 | True |
| 04-describe-a-rainy-tuesday-commute-in | -0.4410 | -0.4912 | True |
| 05-write-600-words-on-why-people | -0.5347 | -0.5836 | True |
| 06-a-letter-from-a-retired-ferry | 2.5284 | -0.5485 | True |
| 07-explain-sourdough-as-if-you-have | -0.5663 | -0.5872 | True |
| 08-a-600-word-scene-in-a | 2.3349 | -0.4238 | True |
| 09-write-about-500-words-as-a | -0.5405 | -0.6244 | True |
| 10-describe-a-weekday-morning-in-a | -0.4732 | -0.4815 | True |
| 11-a-short-story-about-a-chess | -0.3051 | -0.4140 | True |
| 12-a-letter-from-someone-who-just | 2.6558 | -0.5210 | True |
| 13-write-about-500-words-on-a | -0.4747 | -0.5143 | True |
| 14-describe-the-last-hour-of-a | -0.5168 | -0.4162 | False |
| 15-a-500-word-scene-in-a | -0.4137 | -0.5023 | True |
| 16-explain-ice-fishing-as-if-you | -0.5605 | -0.5501 | False |
| 17-write-about-500-words-as-a | -0.4845 | -0.6612 | True |
| 18-a-short-story-about-two-people | -0.3755 | -0.4311 | True |
| 19-describe-an-allotment-garden-in-late | 2.2983 | -0.4747 | True |
| 20-a-letter-from-a-lighthouse-keeper | 2.7115 | -0.4472 | True |
| 21-write-about-500-words-on-a | 2.7292 | -0.4940 | True |
| 22-a-500-word-scene-in-a | 2.3867 | -0.4078 | True |
| 23-describe-a-night-receptionist-in-a | -0.5134 | -0.5670 | True |
| 24-explain-bicycle-repair-as-if-you | -0.5645 | -0.5165 | False |
| 25-a-short-story-about-a-community | 2.3657 | -0.2858 | True |
| 26-write-about-500-words-as-a | -0.5626 | -0.5191 | False |
| 27-a-letter-from-a-market-stall | 2.4705 | -0.4121 | True |
| 28-describe-a-hiking-hut-on-a | -0.5133 | -0.5486 | True |
| 29-a-500-word-scene-in-a | 2.4228 | -0.4865 | True |
| 30-write-about-500-words-on-an | 2.5413 | -0.5141 | True |
| 31-explain-printing-a-local-newspaper-as | -0.3801 | -0.5356 | True |
| 32-a-short-story-about-walking-other | -0.4171 | -0.5079 | True |
| 33-describe-a-fishing-village-in-january | -0.4627 | -0.5482 | True |
| 34-a-letter-from-a-night-train | 2.6621 | -0.5910 | True |
| 35-write-about-500-words-as-someone | -0.4277 | -0.5110 | True |
| 36-a-500-word-scene-in-a | 2.2886 | -0.4639 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.3652 | -0.5608 | True |
| 38-a-short-story-about-neighbours-sharing | 2.6757 | -0.3185 | True |
| 39-write-about-500-words-on-a | 2.6705 | -0.5844 | True |
| 40-a-letter-from-a-retired-teacher | 2.6124 | -0.5538 | True |

