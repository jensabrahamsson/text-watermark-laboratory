# Key-free probe

probe n_methods=2 pair_dir=/workspace/experiments/2026-08-31-pair-distilgpt2-12x4 context_len=4 model=distilgpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=5 pos_bucket=0 rankpath_full=False rankpath_pos_bucket=0 cascade_rankpath_end=None include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| rankpath | 7/12 | 0.563 | 23/48 | 26/48 | 0.09895 | 0.1661 |
| rankuni | 4/12 | 0.431 | 21/48 | 21/48 | 0.8851 | -0.0206 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| rankpath | 0/48 | 0/48 | 23/25 | 22/26 | 0.511 |
| rankuni | 0/48 | 0/48 | 21/27 | 27/21 | 0.438 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| rankpath | 13/48 | 41/48 | 0.5819 | 0.271 | 0.854 |
| rankuni | 36/48 | 2/48 | -0.1192 | 0.750 | 0.042 |

rankpath auc=0.563 mean_pos=0.0713 mean_neg=-0.0948 diff=0.1661 pos>0=23/48 neg<=0=26/48 perm_p=0.09895 binom_p=0.6673 youden_t=0.6961 youden_sens=0.271 youden_spec=0.958 J=0.229
rankpath prompts_marked_above=7/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.431 mean_pos=-0.0154 mean_neg=0.0053 diff=-0.0206 pos>0=21/48 neg<=0=21/48 perm_p=0.8851 binom_p=0.8438 youden_t=-0.1901 youden_sens=1.000 youden_spec=0.021 J=0.021
rankuni prompts_marked_above=4/12 instance=key-free-rankuni used_keys=False
