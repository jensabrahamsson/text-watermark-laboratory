# Key-free probe

probe n_methods=5 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.737 | 28/48 | 30/48 | 0.0004998 | 1.1283 |
| hashpool | 11/12 | 0.716 | 35/48 | 29/48 | 0.0004998 | 0.0392 |
| postokhits | 12/12 | 0.763 | 24/48 | 45/48 | 0.0004998 | 1.6477 |
| hashtok | 9/12 | 0.664 | 33/48 | 22/48 | 0.001999 | 0.0715 |
| hashtoklen | 8/12 | 0.592 | 33/48 | 23/48 | 0.01849 | 0.0444 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hits | 7/48 | 8/48 | 28/13 | 18/22 | 0.609 |
| hashpool | 0/48 | 0/48 | 35/13 | 19/29 | 0.648 |
| postokhits | 24/48 | 39/48 | 24/0 | 3/6 | 0.889 |
| hashtok | 0/48 | 0/48 | 33/15 | 26/22 | 0.559 |
| hashtoklen | 0/48 | 0/48 | 33/15 | 25/23 | 0.569 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 22/48 | 39/48 | 0.2626 | 0.458 | 0.812 |
| hashpool | 23/48 | 36/48 | 0.0220 | 0.479 | 0.750 |
| postokhits | 22/48 | 45/48 | 0.8436 | 0.458 | 0.938 |
| hashtok | 22/48 | 30/48 | 0.0582 | 0.458 | 0.625 |
| hashtoklen | 30/48 | 20/48 | 0.0031 | 0.625 | 0.417 |

hits auc=0.737 mean_pos=1.0491 mean_neg=-0.0793 diff=1.1283 pos>0=28/48 neg<=0=30/48 perm_p=0.0004998 binom_p=0.1562 youden_t=0.0080 youden_sens=0.562 youden_spec=0.854 J=0.417
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
hashpool auc=0.716 mean_pos=0.0355 mean_neg=-0.0037 diff=0.0392 pos>0=35/48 neg<=0=29/48 perm_p=0.0004998 binom_p=0.001044 youden_t=0.0258 youden_sens=0.500 youden_spec=0.938 J=0.438
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
postokhits auc=0.763 mean_pos=1.5036 mean_neg=-0.1441 diff=1.6477 pos>0=24/48 neg<=0=45/48 perm_p=0.0004998 binom_p=0.5573 youden_t=1.1249 youden_sens=0.458 youden_spec=1.000 J=0.458
postokhits prompts_marked_above=12/12 instance=key-free-postokhits used_keys=False
hashtok auc=0.664 mean_pos=0.0604 mean_neg=-0.0112 diff=0.0715 pos>0=33/48 neg<=0=22/48 perm_p=0.001999 binom_p=0.006642 youden_t=0.0840 youden_sens=0.438 youden_spec=0.833 J=0.271
hashtok prompts_marked_above=9/12 instance=key-free-hashtok used_keys=False
hashtoklen auc=0.592 mean_pos=0.0409 mean_neg=-0.0034 diff=0.0444 pos>0=33/48 neg<=0=23/48 perm_p=0.01849 binom_p=0.006642 youden_t=0.0043 youden_sens=0.667 youden_spec=0.521 J=0.188
hashtoklen prompts_marked_above=8/12 instance=key-free-hashtoklen used_keys=False
