# Key-free probe

probe n_methods=3 pair_dir=/workspace/experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=['3:4'] fit_prefix=5 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 12/12 | 0.756 | 23/48 | 47/48 | 0.0004998 | 1.6046 |
| rankpath | 11/12 | 0.767 | 30/48 | 36/48 | 0.0004998 | 0.8214 |
| rankuni | 11/12 | 0.738 | 34/48 | 32/48 | 0.0004998 | 0.1598 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 25/48 | 43/48 | 23/0 | 1/4 | 0.958 |
| rankpath | 0/48 | 1/48 | 30/18 | 12/35 | 0.714 |
| rankuni | 0/48 | 0/48 | 34/14 | 16/32 | 0.680 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| postokbackoff | 23/48 | 47/48 | 0.9768 | 0.479 | 0.979 |
| rankpath | 37/48 | 29/48 | -0.4219 | 0.771 | 0.604 |
| rankuni | 34/48 | 28/48 | -0.0322 | 0.708 | 0.583 |

| window tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 3:4 | postokbackoff | 12/12 | 0.500 | 0/48 | 48/48 |
| 3:4 | rankpath | 12/12 | 0.500 | 0/48 | 48/48 |
| 3:4 | rankuni | 4/12 | 0.406 | 8/48 | 34/48 |

postokbackoff auc=0.756 mean_pos=1.4251 mean_neg=-0.1795 diff=1.6046 pos>0=23/48 neg<=0=47/48 perm_p=0.0004998 binom_p=0.6673 youden_t=1.0656 youden_sens=0.479 youden_spec=1.000 J=0.479
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
rankpath auc=0.767 mean_pos=0.1850 mean_neg=-0.6364 diff=0.8214 pos>0=30/48 neg<=0=36/48 perm_p=0.0004998 binom_p=0.0557 youden_t=-0.4284 youden_sens=0.854 youden_spec=0.646 J=0.500
rankpath prompts_marked_above=11/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.738 mean_pos=0.0738 mean_neg=-0.0860 diff=0.1598 pos>0=34/48 neg<=0=32/48 perm_p=0.0004998 binom_p=0.002758 youden_t=-0.0164 youden_sens=0.771 youden_spec=0.667 J=0.438
rankuni prompts_marked_above=11/12 instance=key-free-rankuni used_keys=False
