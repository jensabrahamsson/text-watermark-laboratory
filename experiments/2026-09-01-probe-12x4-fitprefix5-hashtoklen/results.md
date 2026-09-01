# Key-free probe

probe n_methods=5 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=5 pos_bucket=0 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokhits | 12/12 | 0.772 | 23/48 | 48/48 | 0.0004998 | 1.7879 |
| hashtok | 10/12 | 0.737 | 24/48 | 42/48 | 0.0004998 | 0.8532 |
| hashtoklen | 12/12 | 0.573 | 7/48 | 48/48 | 0.008496 | 0.2674 |
| hashtoklenbackoff | 10/12 | 0.716 | 28/48 | 37/48 | 0.0004998 | 0.8304 |
| hashtoklenbackoff2 | 10/12 | 0.694 | 26/48 | 40/48 | 0.0004998 | 0.6587 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokhits | 25/48 | 42/48 | 23/0 | 0/6 | 1.000 |
| hashtok | 21/48 | 32/48 | 24/3 | 6/10 | 0.800 |
| hashtoklen | 41/48 | 48/48 | 7/0 | 0/0 | 1.000 |
| hashtoklenbackoff | 10/48 | 23/48 | 28/10 | 11/14 | 0.718 |
| hashtoklenbackoff2 | 14/48 | 33/48 | 26/8 | 8/7 | 0.765 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| postokhits | 23/48 | 48/48 | 0.0000 | 0.479 | 1.000 |
| hashtok | 22/48 | 44/48 | 0.7484 | 0.458 | 0.917 |
| hashtoklen | 7/48 | 48/48 | 0.0000 | 0.146 | 1.000 |
| hashtoklenbackoff | 23/48 | 41/48 | 0.5906 | 0.479 | 0.854 |
| hashtoklenbackoff2 | 23/48 | 46/48 | 0.8603 | 0.479 | 0.958 |

postokhits auc=0.772 mean_pos=1.5577 mean_neg=-0.2302 diff=1.7879 pos>0=23/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=1.000 J=0.479
postokhits prompts_marked_above=12/12 instance=key-free-postokhits used_keys=False
hashtok auc=0.737 mean_pos=0.7816 mean_neg=-0.0716 diff=0.8532 pos>0=24/48 neg<=0=42/48 perm_p=0.0004998 binom_p=0.5573 youden_t=0.7241 youden_sens=0.479 youden_spec=0.938 J=0.417
hashtok prompts_marked_above=10/12 instance=key-free-hashtok used_keys=False
hashtoklen auc=0.573 mean_pos=0.2674 mean_neg=0.0000 diff=0.2674 pos>0=7/48 neg<=0=48/48 perm_p=0.008496 binom_p=1 youden_t=0.0000 youden_sens=0.146 youden_spec=1.000 J=0.146
hashtoklen prompts_marked_above=12/12 instance=key-free-hashtoklen used_keys=False
hashtoklenbackoff auc=0.716 mean_pos=0.7124 mean_neg=-0.1181 diff=0.8304 pos>0=28/48 neg<=0=37/48 perm_p=0.0004998 binom_p=0.1562 youden_t=0.4924 youden_sens=0.583 youden_spec=0.833 J=0.417
hashtoklenbackoff prompts_marked_above=10/12 instance=key-free-hashtoklenbackoff used_keys=False
hashtoklenbackoff2 auc=0.694 mean_pos=0.5820 mean_neg=-0.0767 diff=0.6587 pos>0=26/48 neg<=0=40/48 perm_p=0.0004998 binom_p=0.3327 youden_t=0.8667 youden_sens=0.479 youden_spec=0.979 J=0.458
hashtoklenbackoff2 prompts_marked_above=10/12 instance=key-free-hashtoklenbackoff2 used_keys=False
