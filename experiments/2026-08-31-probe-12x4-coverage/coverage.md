# Key-free last-4 coverage by position

coverage n_prompts=12 n_files=96 context_len=4 pos_bucket=0 used_keys=False
Leave-one-prompt-out share of last-k contexts seen on both training sides. Hits can only score those positions. This is why the key-free 4-gram reader is front-loaded. Not keys.

| window | shared last-4 | n | mean support when shared |
|---|---|---|---|
| 0:16 | 0.065 (94/1440) | 1440 | 28.03 |
| 16:32 | 0.010 (15/1536) | 1536 | 3.67 |
| 32:64 | 0.011 (34/3072) | 3072 | 4.38 |
| 64:128 | 0.014 (86/6133) | 6133 | 4.74 |
