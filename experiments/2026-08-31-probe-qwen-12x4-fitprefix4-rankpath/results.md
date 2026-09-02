# Key-free probe

probe n_methods=2 pair_dir=/workspace/experiments/2026-08-31-pair-qwen-12x4 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 8/12 | 0.590 | 24/48 | 32/48 | 0.02949 | 0.4006 |
| rankuni | 8/12 | 0.597 | 26/48 | 33/48 | 0.2459 | 0.0413 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 24/24 | 16/32 | 0.600 |
| rankuni | 0/48 | 0/48 | 26/22 | 15/33 | 0.634 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| rankpath | 21/48 | 32/48 | 0.3734 | 0.438 | 0.667 |
| rankuni | 26/48 | 34/48 | 0.0290 | 0.542 | 0.708 |

rankpath auc=0.590 mean_pos=0.0007 mean_neg=-0.3998 diff=0.4006 pos>0=24/48 neg<=0=32/48 perm_p=0.02949 binom_p=0.5573 youden_t=0.5465 youden_sens=0.479 youden_spec=0.771 J=0.250
rankpath prompts_marked_above=8/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.597 mean_pos=-0.0196 mean_neg=-0.0609 diff=0.0413 pos>0=26/48 neg<=0=33/48 perm_p=0.2459 binom_p=0.3327 youden_t=0.0308 youden_sens=0.542 youden_spec=0.729 J=0.271
rankuni prompts_marked_above=8/12 instance=key-free-rankuni used_keys=False
