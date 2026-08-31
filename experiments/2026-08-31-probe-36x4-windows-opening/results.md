# Key-free probe

probe n_methods=1 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=['0:4', '4:16', '0:16', '16:32'] fit_prefix=None pos_bucket=16 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 36/36 | 0.934 | 134/144 | 76/144 | 0.0004998 | 1.4896 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 119/144 | 134/144 | 0.7593 | 0.826 | 0.931 |

| window tokens | method | prompt wins | file auc | nested-by-stem marked | unmarked |
|---|---|---|---|---|---|
| 0:4 | hits | 34/36 | 0.917 | 117/144 | 126/144 |
| 0:16 | hits | 34/36 | 0.916 | 118/144 | 127/144 |
| 4:16 | hits | 29/36 | 0.712 | 80/144 | 123/144 |
| 16:32 | hits | 22/36 | 0.549 | 32/144 | 119/144 |

hits auc=0.934 mean_pos=1.4598 mean_neg=-0.0298 diff=1.4896 pos>0=134/144 neg<=0=76/144 perm_p=0.0004998 binom_p=3.714e-29 youden_t=0.7950 youden_sens=0.826 youden_spec=0.965 J=0.792
hits prompts_marked_above=36/36 instance=key-free-hits used_keys=False
