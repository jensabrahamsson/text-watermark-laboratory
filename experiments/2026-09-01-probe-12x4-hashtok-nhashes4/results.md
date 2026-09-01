# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashtok | 11/12 | 0.733 | 36/48 | 30/48 | 0.0004998 | 0.1150 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashtok | 0/48 | 0/48 | 36/12 | 18/30 | 0.667 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hashtok | 35/48 | 30/48 | -0.0030 | 0.729 | 0.625 |

hashtok auc=0.733 mean_pos=0.0871 mean_neg=-0.0279 diff=0.1150 pos>0=36/48 neg<=0=30/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=-0.0059 youden_sens=0.771 youden_spec=0.625 J=0.396
hashtok prompts_marked_above=11/12 instance=key-free-hashtok used_keys=False
