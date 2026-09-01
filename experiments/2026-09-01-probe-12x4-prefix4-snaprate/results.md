# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=5 pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| snapleave | 8/12 | 0.601 | 42/48 | 10/48 | 0.02949 | 0.0781 |
| snapupset | 6/12 | 0.501 | 25/48 | 14/48 | 0.2309 | 0.0399 |
| snapmiss | 11/12 | 0.717 | 2/48 | 46/48 | 0.0004998 | 0.1458 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| snapleave | 6/48 | 8/48 | 42/0 | 38/2 | 0.525 |
| snapupset | 17/48 | 7/48 | 25/6 | 34/7 | 0.424 |
| snapmiss | 25/48 | 7/48 | 2/21 | 2/39 | 0.500 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| snapleave | 19/48 | 37/48 | 0.2500 | 0.396 | 0.771 |
| snapupset | 19/48 | 37/48 | 0.2500 | 0.396 | 0.771 |
| snapmiss | 27/48 | 39/48 | -0.2500 | 0.562 | 0.812 |

snapleave auc=0.601 mean_pos=0.3177 mean_neg=0.2396 diff=0.0781 pos>0=42/48 neg<=0=10/48 perm_p=0.02949 binom_p=5.044e-08 youden_t=0.2500 youden_sens=0.396 youden_spec=0.771 J=0.167
snapleave prompts_marked_above=8/12 instance=key-free-snapleave used_keys=False
snapupset auc=0.501 mean_pos=0.1910 mean_neg=0.1510 diff=0.0399 pos>0=25/48 neg<=0=14/48 perm_p=0.2309 binom_p=0.4427 youden_t=0.2500 youden_sens=0.396 youden_spec=0.771 J=0.167
snapupset prompts_marked_above=6/12 instance=key-free-snapupset used_keys=False
snapmiss auc=0.717 mean_pos=-0.1094 mean_neg=-0.2552 diff=0.1458 pos>0=2/48 neg<=0=46/48 perm_p=0.0004998 binom_p=1 youden_t=-0.2500 youden_sens=0.562 youden_spec=0.812 J=0.375
snapmiss prompts_marked_above=11/12 instance=key-free-snapmiss used_keys=False
