# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-09-01-pair-100x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 100/100 | 0.980 | 393/400 | 344/400 | 0.0004998 | 3.7804 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 0/400 | 198/400 | 393/7 | 56/146 | 0.875 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| poshits | 392/400 | 382/400 | 0.1474 | 0.980 | 0.955 |

poshits auc=0.980 mean_pos=3.0917 mean_neg=-0.6887 diff=3.7804 pos>0=393/400 neg<=0=344/400 perm_p=0.0004998 binom_p=1.216e-106 youden_t=0.1474 youden_sens=0.980 youden_spec=0.955 J=0.935
poshits prompts_marked_above=100/100 instance=key-free-poshits used_keys=False
