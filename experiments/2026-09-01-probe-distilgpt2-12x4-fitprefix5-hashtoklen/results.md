# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-31-pair-distilgpt2-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=5 pos_bucket=0 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokhits | 10/12 | 0.633 | 18/48 | 46/48 | 0.0004998 | 1.3150 |
| hashtok | 8/12 | 0.655 | 18/48 | 42/48 | 0.0004998 | 1.0034 |
| hashtoklen | 12/12 | 0.573 | 7/48 | 48/48 | 0.009495 | 0.4827 |
| hashtoklenbackoff | 8/12 | 0.592 | 22/48 | 35/48 | 0.001999 | 0.8042 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokhits | 26/48 | 46/48 | 18/4 | 2/0 | 0.900 |
| hashtok | 23/48 | 32/48 | 18/7 | 6/10 | 0.750 |
| hashtoklen | 41/48 | 48/48 | 7/0 | 0/0 | 1.000 |
| hashtoklenbackoff | 12/48 | 24/48 | 22/14 | 13/11 | 0.629 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| postokhits | 16/48 | 46/48 | 0.4217 | 0.333 | 0.958 |
| hashtok | 18/48 | 46/48 | 0.9068 | 0.375 | 0.958 |
| hashtoklen | 7/48 | 48/48 | 0.0000 | 0.146 | 1.000 |
| hashtoklenbackoff | 17/48 | 42/48 | 1.1970 | 0.354 | 0.875 |

postokhits auc=0.633 mean_pos=1.4204 mean_neg=0.1054 diff=1.3150 pos>0=18/48 neg<=0=46/48 perm_p=0.0004998 binom_p=0.9703 youden_t=0.0000 youden_sens=0.375 youden_spec=0.958 J=0.333
postokhits prompts_marked_above=10/12 instance=key-free-postokhits used_keys=False
hashtok auc=0.655 mean_pos=0.9063 mean_neg=-0.0971 diff=1.0034 pos>0=18/48 neg<=0=42/48 perm_p=0.0004998 binom_p=0.9703 youden_t=0.9078 youden_sens=0.375 youden_spec=0.979 J=0.354
hashtok prompts_marked_above=8/12 instance=key-free-hashtok used_keys=False
hashtoklen auc=0.573 mean_pos=0.4827 mean_neg=0.0000 diff=0.4827 pos>0=7/48 neg<=0=48/48 perm_p=0.009495 binom_p=1 youden_t=0.0000 youden_sens=0.146 youden_spec=1.000 J=0.146
hashtoklen prompts_marked_above=12/12 instance=key-free-hashtoklen used_keys=False
hashtoklenbackoff auc=0.592 mean_pos=0.8254 mean_neg=0.0212 diff=0.8042 pos>0=22/48 neg<=0=35/48 perm_p=0.001999 binom_p=0.7646 youden_t=1.0885 youden_sens=0.438 youden_spec=0.896 J=0.333
hashtoklenbackoff prompts_marked_above=8/12 instance=key-free-hashtoklenbackoff used_keys=False
