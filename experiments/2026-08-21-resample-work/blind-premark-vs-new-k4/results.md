# Key-free blind eval (leave-one-prompt-out)

Accuracy: **34/40** (0.850). context_len=4 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.4929 | -0.5464 | True |
| 02-explain-how-a-municipal-library-actually | -0.5504 | -0.5285 | False |
| 03-a-short-story-about-two-neighbours | -0.3623 | -0.4215 | True |
| 04-describe-a-rainy-tuesday-commute-in | -0.4618 | -0.5514 | True |
| 05-write-600-words-on-why-people | -0.5797 | -0.5425 | False |
| 06-a-letter-from-a-retired-ferry | 2.8413 | -0.5673 | True |
| 07-explain-sourdough-as-if-you-have | -0.6257 | -0.5532 | False |
| 08-a-600-word-scene-in-a | 2.6162 | -0.4376 | True |
| 09-write-about-500-words-as-a | -0.4474 | -0.5866 | True |
| 10-describe-a-weekday-morning-in-a | -0.4250 | -0.5556 | True |
| 11-a-short-story-about-a-chess | -0.2124 | -0.4659 | True |
| 12-a-letter-from-someone-who-just | 3.0476 | -0.5637 | True |
| 13-write-about-500-words-on-a | -0.4542 | -0.5814 | True |
| 14-describe-the-last-hour-of-a | -0.5209 | -0.5193 | False |
| 15-a-500-word-scene-in-a | -0.3445 | -0.4742 | True |
| 16-explain-ice-fishing-as-if-you | -0.5610 | -0.5598 | False |
| 17-write-about-500-words-as-a | -0.4694 | -0.5799 | True |
| 18-a-short-story-about-two-people | -0.3304 | -0.4964 | True |
| 19-describe-an-allotment-garden-in-late | 2.6511 | -0.4115 | True |
| 20-a-letter-from-a-lighthouse-keeper | 3.0246 | -0.5629 | True |
| 21-write-about-500-words-on-a | 3.0124 | -0.3807 | True |
| 22-a-500-word-scene-in-a | 2.6460 | -0.4083 | True |
| 23-describe-a-night-receptionist-in-a | -0.4155 | -0.5145 | True |
| 24-explain-bicycle-repair-as-if-you | -0.5547 | -0.5217 | False |
| 25-a-short-story-about-a-community | 2.6200 | -0.3213 | True |
| 26-write-about-500-words-as-a | -0.4883 | -0.5148 | True |
| 27-a-letter-from-a-market-stall | 2.7738 | -0.4624 | True |
| 28-describe-a-hiking-hut-on-a | -0.4545 | -0.5026 | True |
| 29-a-500-word-scene-in-a | 2.7090 | -0.4303 | True |
| 30-write-about-500-words-on-an | 2.9602 | -0.5062 | True |
| 31-explain-printing-a-local-newspaper-as | -0.2434 | -0.4538 | True |
| 32-a-short-story-about-walking-other | -0.3712 | -0.4347 | True |
| 33-describe-a-fishing-village-in-january | -0.4568 | -0.5444 | True |
| 34-a-letter-from-a-night-train | 3.0454 | -0.5680 | True |
| 35-write-about-500-words-as-someone | -0.4343 | -0.5408 | True |
| 36-a-500-word-scene-in-a | 2.4489 | -0.4815 | True |
| 37-describe-a-rooftop-greenhouse-that-is | -0.3259 | -0.4822 | True |
| 38-a-short-story-about-neighbours-sharing | 2.9187 | -0.3747 | True |
| 39-write-about-500-words-on-a | 2.9941 | -0.4280 | True |
| 40-a-letter-from-a-retired-teacher | 2.9498 | -0.6387 | True |

