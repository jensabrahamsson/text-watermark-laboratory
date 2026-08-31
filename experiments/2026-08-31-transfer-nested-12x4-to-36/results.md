# Key-free transfer

transfer n_methods=7 train=experiments/2026-08-17-pair-12x4 test=experiments/2026-08-17-pair-36 n_train=12 n_test=24 overlap_mode=drop-from-test dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hard | 14/24 | 0.606 | 16/24 | 12/24 | 0.05447 | 0.0290 |
| hits | 24/24 | 0.986 | 24/24 | 14/24 | 0.0004998 | 1.1854 |
| freqhits | 24/24 | 0.984 | 24/24 | 13/24 | 0.0004998 | 1.6835 |
| hitmass | 23/24 | 0.977 | 24/24 | 14/24 | 0.0004998 | 0.0338 |
| hashpool | 23/24 | 0.924 | 21/24 | 20/24 | 0.0004998 | 0.0506 |
| hybrid | 23/24 | 0.946 | 22/24 | 20/24 | 0.0004998 | 0.0569 |
| stack | 21/24 | 0.880 | 12/24 | 24/24 | 0.0004998 | 0.9841 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hard | in-sample-youden | 0.6101 | 0/24 | 24/24 | 0.000 | 1.000 |
| hits | in-sample-youden | -0.2541 | 24/24 | 6/24 | 1.000 | 0.250 |
| freqhits | in-sample-youden | 0.0000 | 24/24 | 13/24 | 1.000 | 0.542 |
| hitmass | in-sample-youden | -0.0086 | 24/24 | 6/24 | 1.000 | 0.250 |
| hashpool | in-sample-youden | 0.0000 | 21/24 | 20/24 | 0.875 | 0.833 |
| hybrid | in-sample-youden | 0.0000 | 22/24 | 20/24 | 0.917 | 0.833 |
| stack | in-sample-youden | 0.0000 | 12/24 | 24/24 | 0.500 | 1.000 |
| hard | nested-youden | -0.0308 | 19/24 | 9/24 | 0.792 | 0.375 |
| hard | nested-fpr10 | 0.0819 | 3/24 | 24/24 | 0.125 | 1.000 |
| hits | nested-youden | 0.0080 | 24/24 | 16/24 | 1.000 | 0.667 |
| hits | nested-fpr10 | 0.5048 | 20/24 | 24/24 | 0.833 | 1.000 |
| freqhits | nested-youden | 0.5224 | 23/24 | 23/24 | 0.958 | 0.958 |
| freqhits | nested-fpr10 | 0.5224 | 23/24 | 23/24 | 0.958 | 0.958 |
| hitmass | nested-youden | 0.0089 | 21/24 | 23/24 | 0.875 | 0.958 |
| hitmass | nested-fpr10 | 0.0088 | 21/24 | 23/24 | 0.875 | 0.958 |
| hashpool | nested-youden | 0.0258 | 12/24 | 24/24 | 0.500 | 1.000 |
| hashpool | nested-fpr10 | 0.0251 | 12/24 | 24/24 | 0.500 | 1.000 |
| stack | nested-youden | 0.0087 | 12/24 | 24/24 | 0.500 | 1.000 |
| stack | nested-fpr10 | -0.0008 | 12/24 | 24/24 | 0.500 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hard auc=0.606 mean_pos=0.0254 mean_neg=-0.0036 diff=0.0290 pos>0=16/24 neg<=0=12/24 perm_p=0.05447 binom_p=0.07579 youden_t=0.0630 youden_sens=0.250 youden_spec=1.000 J=0.250
hard prompts_marked_above=14/24 instance=key-free-counts used_keys=False
hits auc=0.986 mean_pos=1.0386 mean_neg=-0.1468 diff=1.1854 pos>0=24/24 neg<=0=14/24 perm_p=0.0004998 binom_p=5.96e-08 youden_t=0.3485 youden_sens=0.917 youden_spec=1.000 J=0.917
hits prompts_marked_above=24/24 instance=key-free-hits used_keys=False
freqhits auc=0.984 mean_pos=1.5043 mean_neg=-0.1792 diff=1.6835 pos>0=24/24 neg<=0=13/24 perm_p=0.0004998 binom_p=5.96e-08 youden_t=0.4884 youden_sens=0.958 youden_spec=0.958 J=0.917
freqhits prompts_marked_above=24/24 instance=key-free-freqhits used_keys=False
hitmass auc=0.977 mean_pos=0.0314 mean_neg=-0.0024 diff=0.0338 pos>0=24/24 neg<=0=14/24 perm_p=0.0004998 binom_p=5.96e-08 youden_t=0.0023 youden_sens=1.000 youden_spec=0.833 J=0.833
hitmass prompts_marked_above=23/24 instance=key-free-hitmass used_keys=False
hashpool auc=0.924 mean_pos=0.0343 mean_neg=-0.0163 diff=0.0506 pos>0=21/24 neg<=0=20/24 perm_p=0.0004998 binom_p=0.0001386 youden_t=-0.0034 youden_sens=0.917 youden_spec=0.833 J=0.750
hashpool prompts_marked_above=23/24 instance=key-free-hashpool used_keys=False
hybrid auc=0.946 mean_pos=0.0394 mean_neg=-0.0175 diff=0.0569 pos>0=22/24 neg<=0=20/24 perm_p=0.0004998 binom_p=1.794e-05 youden_t=0.0039 youden_sens=0.917 youden_spec=0.875 J=0.792
hybrid prompts_marked_above=23/24 instance=key-free-hybrid used_keys=False
stack auc=0.880 mean_pos=0.1896 mean_neg=-0.7945 diff=0.9841 pos>0=12/24 neg<=0=24/24 perm_p=0.0004998 binom_p=0.5806 youden_t=-0.2553 youden_sens=0.708 youden_spec=0.958 J=0.667
stack prompts_marked_above=21/24 instance=key-free-stack used_keys=False
