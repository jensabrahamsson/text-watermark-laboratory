# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-09-01-pair-100x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| interpolate | 99/100 | 0.898 | 352/400 | 290/400 | 0.0004998 | 0.5201 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| interpolate | 0/400 | 0/400 | 352/48 | 110/290 | 0.762 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| interpolate | 322/400 | 338/400 | 0.0876 | 0.805 | 0.845 |

interpolate auc=0.898 mean_pos=0.4027 mean_neg=-0.1174 diff=0.5201 pos>0=352/400 neg<=0=290/400 perm_p=0.0004998 binom_p=1.513e-58 youden_t=0.0889 youden_sens=0.815 youden_spec=0.865 J=0.680
interpolate prompts_marked_above=99/100 instance=key-free-interpolate used_keys=False
