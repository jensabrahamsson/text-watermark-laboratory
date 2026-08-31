# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=4 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 36/36 | 0.934 | 134/144 | 76/144 | 0.0004998 | 1.4896 |
| freqhits | 35/36 | 0.916 | 131/144 | 81/144 | 0.0004998 | 1.7003 |
| hitmass | 36/36 | 0.938 | 134/144 | 76/144 | 0.0004998 | 0.0838 |
| hashpool | 36/36 | 0.909 | 128/144 | 96/144 | 0.0004998 | 0.1298 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 119/144 | 134/144 | 0.7593 | 0.826 | 0.931 |
| freqhits | 122/144 | 130/144 | 0.7216 | 0.847 | 0.903 |
| hitmass | 116/144 | 134/144 | 0.0284 | 0.806 | 0.931 |
| hashpool | 111/144 | 128/144 | 0.0266 | 0.771 | 0.889 |

hits auc=0.934 mean_pos=1.4598 mean_neg=-0.0298 diff=1.4896 pos>0=134/144 neg<=0=76/144 perm_p=0.0004998 binom_p=3.714e-29 youden_t=0.7950 youden_sens=0.826 youden_spec=0.965 J=0.792
hits prompts_marked_above=36/36 instance=key-free-hits used_keys=False
freqhits auc=0.916 mean_pos=1.6134 mean_neg=-0.0869 diff=1.7003 pos>0=131/144 neg<=0=81/144 perm_p=0.0004998 binom_p=5.228e-26 youden_t=0.7230 youden_sens=0.847 youden_spec=0.910 J=0.757
freqhits prompts_marked_above=35/36 instance=key-free-freqhits used_keys=False
hitmass auc=0.938 mean_pos=0.0834 mean_neg=-0.0004 diff=0.0838 pos>0=134/144 neg<=0=76/144 perm_p=0.0004998 binom_p=3.714e-29 youden_t=0.0289 youden_sens=0.826 youden_spec=0.965 J=0.792
hitmass prompts_marked_above=36/36 instance=key-free-hitmass used_keys=False
hashpool auc=0.909 mean_pos=0.1208 mean_neg=-0.0090 diff=0.1298 pos>0=128/144 neg<=0=96/144 perm_p=0.0004998 binom_p=3.517e-23 youden_t=0.0255 youden_sens=0.819 youden_spec=0.910 J=0.729
hashpool prompts_marked_above=36/36 instance=key-free-hashpool used_keys=False
