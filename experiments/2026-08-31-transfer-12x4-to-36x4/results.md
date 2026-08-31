# Key-free transfer

transfer n_methods=5 train=experiments/2026-08-17-pair-12x4 test=experiments/2026-08-31-pair-36x4 n_train=12 n_test=24 overlap_mode=drop-from-test dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 24/24 | 0.924 | 90/96 | 59/96 | 0.0004998 | 1.2945 |
| freqhits | 24/24 | 0.896 | 89/96 | 69/96 | 0.0004998 | 1.5778 |
| hitmass | 24/24 | 0.936 | 90/96 | 59/96 | 0.0004998 | 0.0521 |
| hashpool | 24/24 | 0.888 | 85/96 | 48/96 | 0.0004998 | 0.0661 |
| logit | 24/24 | 0.931 | 89/96 | 71/96 | 0.0004998 | 2.0867 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | -0.2541 | 96/96 | 19/96 | 1.000 | 0.198 |
| freqhits | in-sample-youden | 0.0000 | 89/96 | 69/96 | 0.927 | 0.719 |
| hitmass | in-sample-youden | -0.0086 | 95/96 | 19/96 | 0.990 | 0.198 |
| hashpool | in-sample-youden | 0.0000 | 85/96 | 48/96 | 0.885 | 0.500 |
| logit | in-sample-youden | 0.0000 | 89/96 | 71/96 | 0.927 | 0.740 |
| hits | nested-youden | 0.0080 | 90/96 | 63/96 | 0.938 | 0.656 |
| hits | nested-fpr10 | 0.5048 | 83/96 | 85/96 | 0.865 | 0.885 |
| freqhits | nested-youden | 0.5224 | 86/96 | 79/96 | 0.896 | 0.823 |
| freqhits | nested-fpr10 | 0.5224 | 86/96 | 79/96 | 0.896 | 0.823 |
| hitmass | nested-youden | 0.0089 | 88/96 | 75/96 | 0.917 | 0.781 |
| hitmass | nested-fpr10 | 0.0088 | 88/96 | 75/96 | 0.917 | 0.781 |
| hashpool | nested-youden | 0.0258 | 76/96 | 90/96 | 0.792 | 0.938 |
| hashpool | nested-fpr10 | 0.0251 | 77/96 | 89/96 | 0.802 | 0.927 |
| logit | nested-youden | 0.7935 | 75/96 | 95/96 | 0.781 | 0.990 |
| logit | nested-fpr10 | 0.3785 | 85/96 | 83/96 | 0.885 | 0.865 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.924 mean_pos=1.3084 mean_neg=0.0139 diff=1.2945 pos>0=90/96 neg<=0=59/96 perm_p=0.0004998 binom_p=1.252e-20 youden_t=0.7155 youden_sens=0.823 youden_spec=0.938 J=0.760
hits prompts_marked_above=24/24 instance=key-free-hits used_keys=False
freqhits auc=0.896 mean_pos=1.5598 mean_neg=-0.0180 diff=1.5778 pos>0=89/96 neg<=0=69/96 perm_p=0.0004998 binom_p=1.63e-19 youden_t=0.7619 youden_sens=0.865 youden_spec=0.885 J=0.750
freqhits prompts_marked_above=24/24 instance=key-free-freqhits used_keys=False
hitmass auc=0.936 mean_pos=0.0533 mean_neg=0.0012 diff=0.0521 pos>0=90/96 neg<=0=59/96 perm_p=0.0004998 binom_p=1.252e-20 youden_t=0.0170 youden_sens=0.854 youden_spec=0.906 J=0.760
hitmass prompts_marked_above=24/24 instance=key-free-hitmass used_keys=False
hashpool auc=0.888 mean_pos=0.0617 mean_neg=-0.0044 diff=0.0661 pos>0=85/96 neg<=0=48/96 perm_p=0.0004998 binom_p=1.274e-15 youden_t=0.0245 youden_sens=0.812 youden_spec=0.927 J=0.740
hashpool prompts_marked_above=24/24 instance=key-free-hashpool used_keys=False
logit auc=0.931 mean_pos=1.7750 mean_neg=-0.3117 diff=2.0867 pos>0=89/96 neg<=0=71/96 perm_p=0.0004998 binom_p=1.63e-19 youden_t=0.6728 youden_sens=0.823 youden_spec=0.948 J=0.771
logit prompts_marked_above=24/24 instance=key-free-logit used_keys=False
