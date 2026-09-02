# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 9/12 | 0.590 | 25/48 | 22/48 | 0.04048 | 0.0251 |
| interpolate | 7/12 | 0.525 | 24/48 | 24/48 | 0.3708 | 0.0129 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hard | 0/48 | 0/48 | 25/23 | 26/22 | 0.490 |
| interpolate | 0/48 | 0/48 | 24/24 | 24/24 | 0.500 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hard | 39/48 | 21/48 | -0.0311 | 0.812 | 0.438 |
| interpolate | 20/48 | 35/48 | 0.0674 | 0.417 | 0.729 |

hard auc=0.590 mean_pos=0.0232 mean_neg=-0.0019 diff=0.0251 pos>0=25/48 neg<=0=22/48 perm_p=0.04048 binom_p=0.4427 youden_t=-0.0305 youden_sens=0.812 youden_spec=0.458 J=0.271
hard prompts_marked_above=9/12 instance=key-free-counts used_keys=False
interpolate auc=0.525 mean_pos=0.0037 mean_neg=-0.0092 diff=0.0129 pos>0=24/48 neg<=0=24/48 perm_p=0.3708 binom_p=0.5573 youden_t=0.0676 youden_sens=0.417 youden_spec=0.750 J=0.167
interpolate prompts_marked_above=7/12 instance=key-free-interpolate used_keys=False
