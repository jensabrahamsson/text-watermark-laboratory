# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashtok | 9/12 | 0.664 | 33/48 | 22/48 | 0.001999 | 0.0715 |
| hashtok2 | 8/12 | 0.602 | 34/48 | 21/48 | 0.03148 | 0.0579 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashtok | 0/48 | 0/48 | 33/15 | 26/22 | 0.559 |
| hashtok2 | 0/48 | 0/48 | 34/14 | 27/21 | 0.557 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hashtok | 22/48 | 30/48 | 0.0582 | 0.458 | 0.625 |
| hashtok2 | 19/48 | 35/48 | 0.1426 | 0.396 | 0.729 |

hashtok auc=0.664 mean_pos=0.0604 mean_neg=-0.0112 diff=0.0715 pos>0=33/48 neg<=0=22/48 perm_p=0.001999 binom_p=0.006642 youden_t=0.0840 youden_sens=0.438 youden_spec=0.833 J=0.271
hashtok prompts_marked_above=9/12 instance=key-free-hashtok used_keys=False
hashtok2 auc=0.602 mean_pos=0.0887 mean_neg=0.0308 diff=0.0579 pos>0=34/48 neg<=0=21/48 perm_p=0.03148 binom_p=0.002758 youden_t=0.1064 youden_sens=0.479 youden_spec=0.771 J=0.250
hashtok2 prompts_marked_above=8/12 instance=key-free-hashtok2 used_keys=False
