# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 34/36 | 0.935 | 131/144 | 132/144 | 0.0004998 | 3.3330 |
| postokhits | 34/36 | 0.912 | 122/144 | 132/144 | 0.0004998 | 3.3281 |
| postokbackoff | 34/36 | 0.910 | 122/144 | 131/144 | 0.0004998 | 3.2786 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 8/144 | 89/144 | 131/5 | 12/43 | 0.916 |
| postokhits | 19/144 | 105/144 | 122/3 | 12/27 | 0.910 |
| postokbackoff | 19/144 | 102/144 | 122/3 | 13/29 | 0.904 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| poshits | 121/144 | 132/144 | 0.0336 | 0.840 | 0.917 |
| postokhits | 121/144 | 139/144 | 0.4041 | 0.840 | 0.965 |
| postokbackoff | 121/144 | 138/144 | 0.4041 | 0.840 | 0.958 |

poshits auc=0.935 mean_pos=2.7607 mean_neg=-0.5724 diff=3.3330 pos>0=131/144 neg<=0=132/144 perm_p=0.0004998 binom_p=5.228e-26 youden_t=0.0304 youden_sens=0.910 youden_spec=0.924 J=0.833
poshits prompts_marked_above=34/36 instance=key-free-poshits used_keys=False
postokhits auc=0.912 mean_pos=2.8235 mean_neg=-0.5046 diff=3.3281 pos>0=122/144 neg<=0=132/144 perm_p=0.0004998 binom_p=2.724e-18 youden_t=0.4044 youden_sens=0.840 youden_spec=0.972 J=0.812
postokhits prompts_marked_above=34/36 instance=key-free-postokhits used_keys=False
postokbackoff auc=0.910 mean_pos=2.7778 mean_neg=-0.5007 diff=3.2786 pos>0=122/144 neg<=0=131/144 perm_p=0.0004998 binom_p=2.724e-18 youden_t=0.4044 youden_sens=0.840 youden_spec=0.965 J=0.806
postokbackoff prompts_marked_above=34/36 instance=key-free-postokbackoff used_keys=False
