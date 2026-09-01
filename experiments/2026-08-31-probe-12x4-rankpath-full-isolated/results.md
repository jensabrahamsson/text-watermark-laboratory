# Key-free probe

probe n_methods=2 pair_dir=/workspace/experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[4, 16, 32, 64, 128] windows=['0:16', '16:32', '32:64', '64:128'] fit_prefix=None pos_bucket=0 rankpath_full=True rankpath_pos_bucket=0 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 8/12 | 0.559 | 27/48 | 28/48 | 0.1449 | 0.0091 |
| rankuni | 7/12 | 0.553 | 23/48 | 29/48 | 0.2489 | 0.0006 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 27/21 | 20/28 | 0.574 |
| rankuni | 0/48 | 0/48 | 23/25 | 19/29 | 0.548 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| rankpath | 25/48 | 31/48 | 0.0086 | 0.521 | 0.646 |
| rankuni | 31/48 | 22/48 | -0.0013 | 0.646 | 0.458 |

| prefix tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 4 | rankpath | 10/12 | 0.718 | 32/48 | 31/48 |
| 4 | rankuni | 11/12 | 0.738 | 34/48 | 28/48 |
| 16 | rankpath | 9/12 | 0.620 | 27/48 | 25/48 |
| 16 | rankuni | 2/12 | 0.380 | 40/48 | 5/48 |
| 32 | rankpath | 8/12 | 0.554 | 39/48 | 12/48 |
| 32 | rankuni | 6/12 | 0.509 | 25/48 | 22/48 |
| 64 | rankpath | 9/12 | 0.639 | 35/48 | 24/48 |
| 64 | rankuni | 8/12 | 0.602 | 22/48 | 26/48 |
| 128 | rankpath | 8/12 | 0.559 | 25/48 | 31/48 |
| 128 | rankuni | 7/12 | 0.553 | 31/48 | 22/48 |

| window tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 0:16 | rankpath | 9/12 | 0.620 | 27/48 | 25/48 |
| 0:16 | rankuni | 2/12 | 0.380 | 40/48 | 5/48 |
| 16:32 | rankpath | 6/12 | 0.506 | 40/48 | 10/48 |
| 16:32 | rankuni | 5/12 | 0.442 | 12/48 | 37/48 |
| 32:64 | rankpath | 9/12 | 0.595 | 19/48 | 39/48 |
| 32:64 | rankuni | 10/12 | 0.589 | 24/48 | 34/48 |
| 64:128 | rankpath | 4/12 | 0.466 | 27/48 | 15/48 |
| 64:128 | rankuni | 5/12 | 0.445 | 16/48 | 33/48 |

rankpath auc=0.559 mean_pos=0.0056 mean_neg=-0.0035 diff=0.0091 pos>0=27/48 neg<=0=28/48 perm_p=0.1449 binom_p=0.2354 youden_t=0.0087 youden_sens=0.521 youden_spec=0.667 J=0.188
rankpath prompts_marked_above=8/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.553 mean_pos=0.0001 mean_neg=-0.0006 diff=0.0006 pos>0=23/48 neg<=0=29/48 perm_p=0.2489 binom_p=0.6673 youden_t=-0.0013 youden_sens=0.667 youden_spec=0.500 J=0.167
rankuni prompts_marked_above=7/12 instance=key-free-rankuni used_keys=False
