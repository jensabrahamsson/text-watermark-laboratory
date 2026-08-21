# Key-free blind eval (leave-one-prompt-out)

Accuracy: **24/40** (0.600). context_len=1 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | 0.0016 | 0.0613 | False |
| 02-explain-how-a-municipal-library-actually | 0.0210 | -0.0379 | True |
| 03-a-short-story-about-two-neighbours | 0.0669 | 0.0046 | True |
| 04-describe-a-rainy-tuesday-commute-in | 0.0134 | 0.0024 | True |
| 05-write-600-words-on-why-people | -0.0650 | 0.0480 | False |
| 06-a-letter-from-a-retired-ferry | 0.0817 | 0.0076 | True |
| 07-explain-sourdough-as-if-you-have | -0.0261 | -0.0219 | False |
| 08-a-600-word-scene-in-a | 0.0784 | -0.0731 | True |
| 09-write-about-500-words-as-a | 0.1486 | -0.0395 | True |
| 10-describe-a-weekday-morning-in-a | 0.0209 | 0.0644 | False |
| 11-a-short-story-about-a-chess | -0.0286 | 0.0808 | False |
| 12-a-letter-from-someone-who-just | 0.0951 | -0.0151 | True |
| 13-write-about-500-words-on-a | -0.0402 | -0.0169 | False |
| 14-describe-the-last-hour-of-a | 0.0267 | -0.0011 | True |
| 15-a-500-word-scene-in-a | 0.1014 | -0.0220 | True |
| 16-explain-ice-fishing-as-if-you | 0.0013 | -0.0189 | True |
| 17-write-about-500-words-as-a | 0.0289 | -0.0296 | True |
| 18-a-short-story-about-two-people | 0.0704 | -0.0089 | True |
| 19-describe-an-allotment-garden-in-late | 0.0580 | 0.0487 | True |
| 20-a-letter-from-a-lighthouse-keeper | 0.0048 | 0.0206 | False |
| 21-write-about-500-words-on-a | 0.0771 | -0.0167 | True |
| 22-a-500-word-scene-in-a | 0.1271 | -0.0853 | True |
| 23-describe-a-night-receptionist-in-a | 0.0284 | -0.0213 | True |
| 24-explain-bicycle-repair-as-if-you | -0.1085 | 0.0212 | False |
| 25-a-short-story-about-a-community | 0.1199 | -0.0103 | True |
| 26-write-about-500-words-as-a | -0.0016 | 0.0951 | False |
| 27-a-letter-from-a-market-stall | -0.0281 | 0.0149 | False |
| 28-describe-a-hiking-hut-on-a | 0.0189 | 0.0774 | False |
| 29-a-500-word-scene-in-a | 0.0725 | 0.0329 | True |
| 30-write-about-500-words-on-an | 0.0254 | 0.0219 | True |
| 31-explain-printing-a-local-newspaper-as | 0.0061 | 0.0214 | False |
| 32-a-short-story-about-walking-other | 0.0125 | 0.0208 | False |
| 33-describe-a-fishing-village-in-january | -0.0679 | 0.0099 | False |
| 34-a-letter-from-a-night-train | 0.0236 | -0.0408 | True |
| 35-write-about-500-words-as-someone | 0.0409 | 0.0313 | True |
| 36-a-500-word-scene-in-a | 0.0106 | 0.0363 | False |
| 37-describe-a-rooftop-greenhouse-that-is | 0.0405 | 0.0036 | True |
| 38-a-short-story-about-neighbours-sharing | 0.1007 | 0.0863 | True |
| 39-write-about-500-words-on-a | 0.0543 | 0.0129 | True |
| 40-a-letter-from-a-retired-teacher | -0.0449 | -0.0205 | False |

