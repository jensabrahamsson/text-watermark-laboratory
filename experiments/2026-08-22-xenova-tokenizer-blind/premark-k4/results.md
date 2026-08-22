# Key-free blind eval (leave-one-prompt-out)

Accuracy: **35/40** (0.875). context_len=4 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.4099 | -0.4563 | True |
| 02-explain-how-a-municipal-library-actually | -0.4576 | -0.4345 | False |
| 03-a-short-story-about-two-neighbours | -0.2751 | -0.3490 | True |
| 04-describe-a-rainy-tuesday-commute-in | -0.3934 | -0.4741 | True |
| 05-write-600-words-on-why-people | -0.5120 | -0.4813 | False |
| 06-a-letter-from-a-retired-ferry | 2.5071 | -0.4877 | True |
| 07-explain-sourdough-as-if-you-have | -0.5396 | -0.4595 | False |
| 08-a-600-word-scene-in-a | 2.3203 | -0.3792 | True |
| 09-write-about-500-words-as-a | -0.3658 | -0.5090 | True |
| 10-describe-a-weekday-morning-in-a | -0.3752 | -0.4737 | True |
| 11-a-short-story-about-a-chess | -0.1902 | -0.3715 | True |
| 12-a-letter-from-someone-who-just | 2.7274 | -0.5026 | True |
| 13-write-about-500-words-on-a | -0.3927 | -0.5102 | True |
| 14-describe-the-last-hour-of-a | -0.4012 | -0.4552 | True |
| 15-a-500-word-scene-in-a | -0.3198 | -0.4248 | True |
| 16-explain-ice-fishing-as-if-you | -0.4810 | -0.4883 | True |
| 17-write-about-500-words-as-a | -0.4094 | -0.5077 | True |
| 18-a-short-story-about-two-people | -0.2720 | -0.4064 | True |
| 19-describe-an-allotment-garden-in-late | 2.1733 | -0.3219 | True |
| 20-a-letter-from-a-lighthouse-keeper | 2.6406 | -0.4694 | True |
| 21-write-about-500-words-on-a | 2.6849 | -0.3184 | True |
| 22-a-500-word-scene-in-a | 2.3791 | -0.3393 | True |
| 23-describe-a-night-receptionist-in-a | -0.3651 | -0.4403 | True |
| 24-explain-bicycle-repair-as-if-you | -0.4552 | -0.4208 | False |
| 25-a-short-story-about-a-community | 2.2806 | -0.2982 | True |
| 26-write-about-500-words-as-a | -0.4019 | -0.4705 | True |
| 27-a-letter-from-a-market-stall | 2.4939 | -0.4068 | True |
| 28-describe-a-hiking-hut-on-a | -0.4323 | -0.4182 | False |
| 29-a-500-word-scene-in-a | 2.3814 | -0.3649 | True |
| 30-write-about-500-words-on-an | 2.5675 | -0.4457 | True |
| 31-explain-printing-a-local-newspaper-as | -0.2138 | -0.3800 | True |
| 32-a-short-story-about-walking-other | -0.3261 | -0.3567 | True |
| 33-describe-a-fishing-village-in-january | -0.3711 | -0.4379 | True |
| 34-a-letter-from-a-night-train | 2.8010 | -0.4879 | True |
| 35-write-about-500-words-as-someone | -0.3638 | -0.4660 | True |
| 36-a-500-word-scene-in-a | 2.1050 | -0.4021 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.2913 | -0.4195 | True |
| 38-a-short-story-about-neighbours-sharing | 2.5206 | -0.2779 | True |
| 39-write-about-500-words-on-a | 2.6314 | -0.3077 | True |
| 40-a-letter-from-a-retired-teacher | 2.5611 | -0.5582 | True |

