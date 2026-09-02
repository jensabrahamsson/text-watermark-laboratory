# Key-free last-4 coverage by position

coverage n_prompts=36 n_files=288 context_len=4 pos_bucket=0 used_keys=False
Leave-one-prompt-out share of last-k contexts seen on both training sides. Hits can only score those positions. This is why the key-free 4-gram reader is front-loaded. Not keys.

| window | shared last-4 | n | mean support when shared |
|---|---|---|---|
| 0:16 | 0.137 (592/4320) | 4320 | 97.44 |
| 16:32 | 0.039 (181/4608) | 4608 | 12.20 |
| 32:64 | 0.035 (319/9216) | 9216 | 13.13 |
| 64:128 | 0.039 (722/18396) | 18396 | 13.57 |
