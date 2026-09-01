# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashtok | 10/12 | 0.622 | 30/48 | 26/48 | 0.005497 | 0.0385 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashtok | 0/48 | 0/48 | 30/18 | 22/26 | 0.577 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hashtok | 21/48 | 38/48 | 0.0434 | 0.438 | 0.792 |

hashtok auc=0.622 mean_pos=0.0373 mean_neg=-0.0011 diff=0.0385 pos>0=30/48 neg<=0=26/48 perm_p=0.005497 binom_p=0.0557 youden_t=0.0385 youden_sens=0.521 youden_spec=0.792 J=0.312
hashtok prompts_marked_above=10/12 instance=key-free-hashtok used_keys=False
