# Key-free blind eval (leave-one-prompt-out)

Accuracy: **19/38** (0.500). context_len=1 backoff=False margin=0.

No key. No `detector_mean`. Ground truth is how the file was *created* (mixin vs not), not the official score.

| Stem | Marked LR | Unmarked LR | Marked higher |
|---|---|---|---|
| 01-write-a-600-word-travel-essay | -0.0315 | 0.0238 | False |
| 02-explain-how-a-municipal-library-actually | 0.0454 | 0.0296 | True |
| 03-a-short-story-about-two-neighbours | 0.0466 | 0.0735 | False |
| 04-describe-a-rainy-tuesday-commute-in | -0.0026 | -0.0360 | True |
| 05-write-600-words-on-why-people | 0.0072 | 0.0323 | False |
| 06-a-letter-from-a-retired-ferry | 0.0028 | 0.0102 | False |
| 07-explain-sourdough-as-if-you-have | -0.0096 | -0.0562 | True |
| 08-a-600-word-scene-in-a | -0.0309 | -0.0328 | True |
| 09-write-about-500-words-as-a | -0.0212 | 0.0380 | False |
| 10-describe-a-weekday-morning-in-a | -0.0323 | 0.0147 | False |
| 11-a-short-story-about-a-chess | -0.0752 | -0.1035 | True |
| 12-a-letter-from-someone-who-just | 0.0472 | -0.0085 | True |
| 13-write-about-500-words-on-a | -0.0749 | -0.0040 | False |
| 14-describe-the-last-hour-of-a | 0.0363 | 0.0183 | True |
| 15-a-500-word-scene-in-a | 0.0048 | -0.0226 | True |
| 16-explain-ice-fishing-as-if-you | 0.0204 | 0.0333 | False |
| 17-write-about-500-words-as-a | -0.0198 | -0.0794 | True |
| 18-a-short-story-about-two-people | -0.0127 | -0.0519 | True |
| 19-describe-an-allotment-garden-in-late | 0.0494 | -0.0575 | True |
| 20-a-letter-from-a-lighthouse-keeper | -0.0621 | 0.0020 | False |
| 21-write-about-500-words-on-a | -0.0031 | -0.0724 | True |
| 22-a-500-word-scene-in-a | 0.0266 | 0.0289 | False |
| 23-describe-a-night-receptionist-in-a | -0.0108 | 0.0262 | False |
| 24-explain-bicycle-repair-as-if-you | -0.0301 | -0.0000 | False |
| 25-a-short-story-about-a-community | 0.0443 | 0.0284 | True |
| 26-write-about-500-words-as-a | -0.0317 | -0.0252 | False |
| 27-a-letter-from-a-market-stall | -0.0839 | -0.0558 | False |
| 28-describe-a-hiking-hut-on-a | 0.0021 | 0.0216 | False |
| 29-a-500-word-scene-in-a | -0.0345 | -0.0043 | False |
| 30-write-about-500-words-on-an | 0.1195 | 0.0583 | True |
| 31-explain-printing-a-local-newspaper-as | -0.0173 | -0.0416 | True |
| 32-a-short-story-about-walking-other | 0.0182 | -0.0046 | True |
| 33-describe-a-fishing-village-in-january | 0.0209 | 0.0454 | False |
| 34-a-letter-from-a-night-train | -0.0023 | -0.0210 | True |
| 35-write-about-500-words-as-someone | -0.0434 | -0.0664 | True |
| 36-a-500-word-scene-in-a | -0.0810 | -0.0164 | False |
| 37-describe-a-rooftop-greenhouse-that-is | -0.0080 | -0.0592 | True |
| 38-a-short-story-about-neighbours-sharing | -0.0264 | -0.0030 | False |

