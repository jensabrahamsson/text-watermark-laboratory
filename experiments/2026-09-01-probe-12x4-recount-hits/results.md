# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 10/12 | 0.718 | 28/48 | 31/48 | 0.0004998 | 0.7646 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hits | 7/48 | 8/48 | 28/13 | 17/23 | 0.622 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 24/48 | 41/48 | 0.3768 | 0.500 | 0.854 |

hits auc=0.718 mean_pos=0.7473 mean_neg=-0.0172 diff=0.7646 pos>0=28/48 neg<=0=31/48 perm_p=0.0004998 binom_p=0.1562 youden_t=0.4997 youden_sens=0.500 youden_spec=0.917 J=0.417
hits prompts_marked_above=10/12 instance=key-free-hits used_keys=False
