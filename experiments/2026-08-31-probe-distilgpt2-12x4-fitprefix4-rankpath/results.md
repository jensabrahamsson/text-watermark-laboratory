# Key-free probe

probe n_methods=2 pair_dir=/workspace/experiments/2026-08-31-pair-distilgpt2-12x4 context_len=4 model=distilgpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 8/12 | 0.579 | 28/48 | 32/48 | 0.1319 | 0.1947 |
| rankuni | 5/12 | 0.451 | 25/48 | 25/48 | 0.8761 | -0.0276 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 1/48 | 28/20 | 16/31 | 0.636 |
| rankuni | 0/48 | 0/48 | 25/23 | 23/25 | 0.521 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| rankpath | 26/48 | 32/48 | 0.0878 | 0.542 | 0.667 |
| rankuni | 20/48 | 28/48 | 0.0298 | 0.417 | 0.583 |

rankpath auc=0.579 mean_pos=0.1085 mean_neg=-0.0862 diff=0.1947 pos>0=28/48 neg<=0=32/48 perm_p=0.1319 binom_p=0.1562 youden_t=0.1196 youden_sens=0.542 youden_spec=0.729 J=0.271
rankpath prompts_marked_above=8/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.451 mean_pos=-0.0139 mean_neg=0.0136 diff=-0.0276 pos>0=25/48 neg<=0=25/48 perm_p=0.8761 binom_p=0.4427 youden_t=0.0336 youden_sens=0.417 youden_spec=0.688 J=0.104
rankuni prompts_marked_above=5/12 instance=key-free-rankuni used_keys=False
