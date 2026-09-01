# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 9/12 | 0.691 | 23/48 | 48/48 | 0.0004998 | 1.7190 |
| tokhits | 12/12 | 0.772 | 23/48 | 48/48 | 0.0004998 | 1.7697 |
| hashtok | 12/12 | 0.796 | 24/48 | 47/48 | 0.0004998 | 1.0636 |
| hashtok2 | 12/12 | 0.729 | 22/48 | 48/48 | 0.0004998 | 0.8477 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hits | 9/48 | 31/48 | 23/16 | 0/17 | 1.000 |
| tokhits | 25/48 | 42/48 | 23/0 | 0/6 | 1.000 |
| hashtok | 24/48 | 37/48 | 24/0 | 1/10 | 0.960 |
| hashtok2 | 26/48 | 48/48 | 22/0 | 0/0 | 1.000 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 23/48 | 48/48 | 0.0000 | 0.479 | 1.000 |
| tokhits | 23/48 | 48/48 | 0.0000 | 0.479 | 1.000 |
| hashtok | 23/48 | 47/48 | 0.0653 | 0.479 | 0.979 |
| hashtok2 | 22/48 | 48/48 | 0.0000 | 0.458 | 1.000 |

hits auc=0.691 mean_pos=1.3906 mean_neg=-0.3285 diff=1.7190 pos>0=23/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=1.000 J=0.479
hits prompts_marked_above=9/12 instance=key-free-hits used_keys=False
tokhits auc=0.772 mean_pos=1.5358 mean_neg=-0.2339 diff=1.7697 pos>0=23/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.6673 youden_t=0.0000 youden_sens=0.479 youden_spec=1.000 J=0.479
tokhits prompts_marked_above=12/12 instance=key-free-tokhits used_keys=False
hashtok auc=0.796 mean_pos=0.8702 mean_neg=-0.1935 diff=1.0636 pos>0=24/48 neg<=0=47/48 perm_p=0.0004998 binom_p=0.5573 youden_t=0.0000 youden_sens=0.500 youden_spec=0.979 J=0.479
hashtok prompts_marked_above=12/12 instance=key-free-hashtok used_keys=False
hashtok2 auc=0.729 mean_pos=0.8477 mean_neg=0.0000 diff=0.8477 pos>0=22/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.7646 youden_t=0.0000 youden_sens=0.458 youden_spec=1.000 J=0.458
hashtok2 prompts_marked_above=12/12 instance=key-free-hashtok2 used_keys=False
