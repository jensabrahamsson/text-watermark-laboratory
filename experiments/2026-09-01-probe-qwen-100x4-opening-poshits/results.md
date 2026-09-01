# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-09-01-pair-qwen-100x4 context_len=4 model=Qwen/Qwen2-1.5B-Instruct max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 95/100 | 0.874 | 333/400 | 308/400 | 0.0004998 | 2.2917 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 14/400 | 142/400 | 333/53 | 92/166 | 0.784 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| poshits | 331/400 | 347/400 | 0.0192 | 0.828 | 0.868 |

poshits auc=0.874 mean_pos=1.9200 mean_neg=-0.3717 diff=2.2917 pos>0=333/400 neg<=0=308/400 perm_p=0.0004998 binom_p=8.221e-44 youden_t=0.0192 youden_sens=0.828 youden_spec=0.868 J=0.695
poshits prompts_marked_above=95/100 instance=key-free-poshits used_keys=False
