# Key-free probe

probe n_methods=4 pair_dir=experiments/2026-08-31-pair-36x4 context_len=4 model=gpt2 max_draws=2 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 33/36 | 0.875 | 60/72 | 36/72 | 0.0004998 | 1.3033 |
| freqhits | 33/36 | 0.873 | 60/72 | 42/72 | 0.0004998 | 1.6809 |
| hitmass | 34/36 | 0.878 | 60/72 | 36/72 | 0.0004998 | 0.0484 |
| hashpool | 31/36 | 0.840 | 59/72 | 45/72 | 0.0004998 | 0.0875 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hits | 52/72 | 64/72 | 0.5552 | 0.722 | 0.889 |
| freqhits | 56/72 | 64/72 | 0.5878 | 0.778 | 0.889 |
| hitmass | 52/72 | 69/72 | 0.0211 | 0.722 | 0.958 |
| hashpool | 52/72 | 67/72 | 0.0346 | 0.722 | 0.931 |

hits auc=0.875 mean_pos=1.2768 mean_neg=-0.0265 diff=1.3033 pos>0=60/72 neg<=0=36/72 perm_p=0.0004998 binom_p=4.028e-09 youden_t=0.5345 youden_sens=0.778 youden_spec=0.917 J=0.694
hits prompts_marked_above=33/36 instance=key-free-hits used_keys=False
freqhits auc=0.873 mean_pos=1.6884 mean_neg=0.0075 diff=1.6809 pos>0=60/72 neg<=0=42/72 perm_p=0.0004998 binom_p=4.028e-09 youden_t=0.5798 youden_sens=0.806 youden_spec=0.903 J=0.708
freqhits prompts_marked_above=33/36 instance=key-free-freqhits used_keys=False
hitmass auc=0.878 mean_pos=0.0483 mean_neg=-0.0001 diff=0.0484 pos>0=60/72 neg<=0=36/72 perm_p=0.0004998 binom_p=4.028e-09 youden_t=0.0209 youden_sens=0.750 youden_spec=0.972 J=0.722
hitmass prompts_marked_above=34/36 instance=key-free-hitmass used_keys=False
hashpool auc=0.840 mean_pos=0.0862 mean_neg=-0.0014 diff=0.0875 pos>0=59/72 neg<=0=45/72 perm_p=0.0004998 binom_p=1.904e-08 youden_t=0.0347 youden_sens=0.722 youden_spec=0.944 J=0.667
hashpool prompts_marked_above=31/36 instance=key-free-hashpool used_keys=False
