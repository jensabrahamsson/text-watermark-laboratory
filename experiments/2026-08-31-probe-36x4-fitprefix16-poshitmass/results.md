# Key-free probe

probe n_methods=2 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=16 pos_bucket=4 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 34/36 | 0.937 | 133/144 | 114/144 | 0.0004998 | 3.5504 |
| poshitmass | 34/36 | 0.943 | 133/144 | 114/144 | 0.0004998 | 0.4043 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| poshits | 122/144 | 127/144 | 0.0276 | 0.847 | 0.882 |
| poshitmass | 121/144 | 130/144 | 0.0592 | 0.840 | 0.903 |

poshits auc=0.937 mean_pos=2.9561 mean_neg=-0.5942 diff=3.5504 pos>0=133/144 neg<=0=114/144 perm_p=0.0004998 binom_p=4.564e-28 youden_t=0.0035 youden_sens=0.917 youden_spec=0.889 J=0.806
poshits prompts_marked_above=34/36 instance=key-free-poshits used_keys=False
poshitmass auc=0.943 mean_pos=0.3648 mean_neg=-0.0396 diff=0.4043 pos>0=133/144 neg<=0=114/144 perm_p=0.0004998 binom_p=4.564e-28 youden_t=0.0774 youden_sens=0.840 youden_spec=0.972 J=0.812
poshitmass prompts_marked_above=34/36 instance=key-free-poshitmass used_keys=False
