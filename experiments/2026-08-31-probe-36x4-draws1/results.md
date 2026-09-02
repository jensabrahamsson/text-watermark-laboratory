# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=1 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 30/36 | 0.845 | 32/36 | 19/36 | 0.0004998 | 1.2510 |
| freqhits | 29/36 | 0.828 | 32/36 | 24/36 | 0.0004998 | 1.5484 |
| hitmass | 32/36 | 0.855 | 32/36 | 19/36 | 0.0004998 | 0.0358 |
| hashpool | 23/36 | 0.753 | 27/36 | 19/36 | 0.0004998 | 0.0454 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 29/36 | 31/36 | 0.4287 | 0.806 | 0.861 |
| freqhits | 27/36 | 26/36 | 0.5035 | 0.750 | 0.722 |
| hitmass | 26/36 | 33/36 | 0.0247 | 0.722 | 0.917 |
| hashpool | 23/36 | 31/36 | 0.0289 | 0.639 | 0.861 |

hits auc=0.845 mean_pos=1.3044 mean_neg=0.0535 diff=1.2510 pos>0=32/36 neg<=0=19/36 perm_p=0.0004998 binom_p=9.708e-07 youden_t=0.4292 youden_sens=0.806 youden_spec=0.889 J=0.694
hits prompts_marked_above=30/36 instance=key-free-hits used_keys=False
freqhits auc=0.828 mean_pos=1.7111 mean_neg=0.1627 diff=1.5484 pos>0=32/36 neg<=0=24/36 perm_p=0.0004998 binom_p=9.708e-07 youden_t=0.5443 youden_sens=0.778 youden_spec=0.806 J=0.583
freqhits prompts_marked_above=29/36 instance=key-free-freqhits used_keys=False
hitmass auc=0.855 mean_pos=0.0392 mean_neg=0.0035 diff=0.0358 pos>0=32/36 neg<=0=19/36 perm_p=0.0004998 binom_p=9.708e-07 youden_t=0.0248 youden_sens=0.722 youden_spec=0.944 J=0.667
hitmass prompts_marked_above=32/36 instance=key-free-hitmass used_keys=False
hashpool auc=0.753 mean_pos=0.0471 mean_neg=0.0018 diff=0.0454 pos>0=27/36 neg<=0=19/36 perm_p=0.0004998 binom_p=0.001967 youden_t=0.0289 youden_sens=0.639 youden_spec=0.889 J=0.528
hashpool prompts_marked_above=23/36 instance=key-free-hashpool used_keys=False
