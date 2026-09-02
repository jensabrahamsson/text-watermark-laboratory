# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=None pos_bucket=16 rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshashtok | 11/12 | 0.621 | 28/48 | 25/48 | 0.003498 | 0.0556 |
| hashtok | 9/12 | 0.664 | 33/48 | 22/48 | 0.001999 | 0.0715 |
| hybrid | 11/12 | 0.725 | 35/48 | 28/48 | 0.0004998 | 0.0449 |
| tokhybrid | 11/12 | 0.683 | 33/48 | 22/48 | 0.0004998 | 0.0804 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshashtok | 0/48 | 0/48 | 28/20 | 23/25 | 0.549 |
| hashtok | 0/48 | 0/48 | 33/15 | 26/22 | 0.559 |
| hybrid | 0/48 | 0/48 | 35/13 | 20/28 | 0.636 |
| tokhybrid | 0/48 | 0/48 | 33/15 | 26/22 | 0.559 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| poshashtok | 14/48 | 38/48 | 0.0920 | 0.292 | 0.792 |
| hashtok | 22/48 | 30/48 | 0.0582 | 0.458 | 0.625 |
| hybrid | 24/48 | 41/48 | 0.0270 | 0.500 | 0.854 |
| tokhybrid | 23/48 | 35/48 | 0.0668 | 0.479 | 0.729 |

poshashtok auc=0.621 mean_pos=0.0402 mean_neg=-0.0154 diff=0.0556 pos>0=28/48 neg<=0=25/48 perm_p=0.003498 binom_p=0.1562 youden_t=0.1192 youden_sens=0.271 youden_spec=0.979 J=0.250
poshashtok prompts_marked_above=11/12 instance=key-free-poshashtok used_keys=False
hashtok auc=0.664 mean_pos=0.0604 mean_neg=-0.0112 diff=0.0715 pos>0=33/48 neg<=0=22/48 perm_p=0.001999 binom_p=0.006642 youden_t=0.0840 youden_sens=0.438 youden_spec=0.833 J=0.271
hashtok prompts_marked_above=9/12 instance=key-free-hashtok used_keys=False
hybrid auc=0.725 mean_pos=0.0400 mean_neg=-0.0049 diff=0.0449 pos>0=35/48 neg<=0=28/48 perm_p=0.0004998 binom_p=0.001044 youden_t=0.0291 youden_sens=0.500 youden_spec=0.958 J=0.458
hybrid prompts_marked_above=11/12 instance=key-free-hybrid used_keys=False
tokhybrid auc=0.683 mean_pos=0.0680 mean_neg=-0.0124 diff=0.0804 pos>0=33/48 neg<=0=22/48 perm_p=0.0004998 binom_p=0.006642 youden_t=0.0849 youden_sens=0.479 youden_spec=0.854 J=0.333
tokhybrid prompts_marked_above=11/12 instance=key-free-tokhybrid used_keys=False
