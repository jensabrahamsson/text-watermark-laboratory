# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-09-01-pair-distil-100x4 context_len=4 model=distilgpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 89/100 | 0.713 | 216/400 | 247/400 | 0.0004998 | 0.8627 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 160/400 | 82/400 | 216/24 | 153/165 | 0.585 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| poshits | 376/400 | 164/400 | -0.0015 | 0.940 | 0.410 |

poshits auc=0.713 mean_pos=0.4502 mean_neg=-0.4125 diff=0.8627 pos>0=216/400 neg<=0=247/400 perm_p=0.0004998 binom_p=0.06052 youden_t=-0.0015 youden_sens=0.940 youden_spec=0.412 J=0.353
poshits prompts_marked_above=89/100 instance=key-free-poshits used_keys=False
