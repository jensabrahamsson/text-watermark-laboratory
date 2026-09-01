# Key-free probe

probe n_methods=2 pair_dir=/workspace/experiments/2026-08-31-pair-qwen-12x4 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=5 pos_bucket=0 rankpath_full=False rankpath_pos_bucket=0 cascade_rankpath_end=None include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 9/12 | 0.662 | 25/48 | 33/48 | 0.003498 | 0.3970 |
| rankuni | 8/12 | 0.561 | 25/48 | 24/48 | 0.3313 | 0.0170 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 25/23 | 15/33 | 0.625 |
| rankuni | 0/48 | 0/48 | 25/23 | 24/24 | 0.510 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| rankpath | 33/48 | 20/48 | -0.4682 | 0.688 | 0.417 |
| rankuni | 24/48 | 21/48 | -0.0294 | 0.500 | 0.438 |

rankpath auc=0.662 mean_pos=0.0749 mean_neg=-0.3221 diff=0.3970 pos>0=25/48 neg<=0=33/48 perm_p=0.003498 binom_p=0.4427 youden_t=-0.6327 youden_sens=0.938 youden_spec=0.396 J=0.333
rankpath prompts_marked_above=9/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.561 mean_pos=-0.0216 mean_neg=-0.0386 diff=0.0170 pos>0=25/48 neg<=0=24/48 perm_p=0.3313 binom_p=0.4427 youden_t=-0.0319 youden_sens=0.708 youden_spec=0.458 J=0.167
rankuni prompts_marked_above=8/12 instance=key-free-rankuni used_keys=False
