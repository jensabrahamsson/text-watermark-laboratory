# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 36/36 | 0.930 | 136/144 | 72/144 | 0.0004998 | 1.2683 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hits | 0/144 | 3/144 | 136/8 | 72/69 | 0.654 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 118/144 | 132/144 | 0.5424 | 0.819 | 0.917 |

hits auc=0.930 mean_pos=1.2937 mean_neg=0.0253 diff=1.2683 pos>0=136/144 neg<=0=72/144 perm_p=0.0004998 binom_p=1.791e-31 youden_t=0.5368 youden_sens=0.833 youden_spec=0.938 J=0.771
hits prompts_marked_above=36/36 instance=key-free-hits used_keys=False
