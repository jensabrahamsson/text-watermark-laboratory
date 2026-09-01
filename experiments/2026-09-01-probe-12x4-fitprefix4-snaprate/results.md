# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| snapleave | 9/12 | 0.569 | 48/48 | 7/48 | 0.05697 | 0.0764 |
| snapupset | 7/12 | 0.501 | 24/48 | 20/48 | 0.5482 | -0.0035 |
| snapmiss | 10/12 | 0.707 | 21/48 | 41/48 | 0.0004998 | 0.1806 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| snapleave | 0/48 | 0/48 | 48/0 | 41/7 | 0.539 |
| snapupset | 15/48 | 10/48 | 24/9 | 28/10 | 0.462 |
| snapmiss | 0/48 | 0/48 | 21/27 | 7/41 | 0.750 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| snapleave | 48/48 | 7/48 | 0.0000 | 1.000 | 0.146 |
| snapupset | 23/48 | 26/48 | 0.1389 | 0.479 | 0.542 |
| snapmiss | 21/48 | 31/48 | -0.1250 | 0.438 | 0.646 |

snapleave auc=0.569 mean_pos=0.3264 mean_neg=0.2500 diff=0.0764 pos>0=48/48 neg<=0=7/48 perm_p=0.05697 binom_p=3.553e-15 youden_t=0.0000 youden_sens=1.000 youden_spec=0.146 J=0.146
snapleave prompts_marked_above=9/12 instance=key-free-snapleave used_keys=False
snapupset auc=0.501 mean_pos=0.1493 mean_neg=0.1528 diff=-0.0035 pos>0=24/48 neg<=0=20/48 perm_p=0.5482 binom_p=0.5573 youden_t=0.1667 youden_sens=0.479 youden_spec=0.583 J=0.062
snapupset prompts_marked_above=7/12 instance=key-free-snapupset used_keys=False
snapmiss auc=0.707 mean_pos=-0.0417 mean_neg=-0.2222 diff=0.1806 pos>0=21/48 neg<=0=41/48 perm_p=0.0004998 binom_p=0.8438 youden_t=0.0000 youden_sens=0.438 youden_spec=0.854 J=0.292
snapmiss prompts_marked_above=10/12 instance=key-free-snapmiss used_keys=False
