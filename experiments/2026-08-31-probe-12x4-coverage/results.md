# Key-free probe

probe n_methods=0 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=['0:16', '16:32', '32:64', '64:128'] fit_prefix=None pos_bucket=16 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|

coverage n_prompts=12 n_files=96 context_len=4 pos_bucket=0 used_keys=False
Leave-one-prompt-out share of last-k contexts seen on both training sides. Hits can only score those positions. This is why the key-free 4-gram reader is front-loaded. Not keys.

| window | shared last-4 | n | mean support when shared |
|---|---|---|---|
| 0:16 | 0.065 (94/1440) | 1440 | 28.03 |
| 16:32 | 0.010 (15/1536) | 1536 | 3.67 |
| 32:64 | 0.011 (34/3072) | 3072 | 4.38 |
| 64:128 | 0.014 (86/6133) | 6133 | 4.74 |

