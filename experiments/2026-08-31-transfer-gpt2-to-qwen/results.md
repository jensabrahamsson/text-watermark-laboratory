# Key-free transfer

transfer n_methods=5 train=experiments/2026-08-17-pair-12x4 test=experiments/2026-08-17-pair-qwen n_train=12 n_test=12 overlap_mode=keep dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.740 | 1/12 | 11/12 | 0.3918 | 0.0490 |
| hitmass | 11/12 | 0.747 | 1/12 | 11/12 | 0.3908 | 0.0005 |
| hashpool | 7/12 | 0.521 | 4/12 | 8/12 | 0.3388 | 0.0028 |
| surface | 8/12 | 0.646 | 2/12 | 11/12 | 0.1399 | 0.0067 |
| logit | 9/12 | 0.708 | 0/12 | 11/12 | 0.3783 | 0.0744 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | -0.2541 | 12/12 | 2/12 | 1.000 | 0.167 |
| hitmass | in-sample-youden | -0.0086 | 12/12 | 1/12 | 1.000 | 0.083 |
| hashpool | in-sample-youden | 0.0000 | 4/12 | 8/12 | 0.333 | 0.667 |
| surface | in-sample-youden | 0.0000 | 2/12 | 11/12 | 0.167 | 0.917 |
| logit | in-sample-youden | 0.0000 | 0/12 | 11/12 | 0.000 | 0.917 |
| hits | nested-youden | 0.0080 | 1/12 | 11/12 | 0.083 | 0.917 |
| hits | nested-fpr10 | 0.5048 | 0/12 | 11/12 | 0.000 | 0.917 |
| hitmass | nested-youden | 0.0089 | 0/12 | 11/12 | 0.000 | 0.917 |
| hitmass | nested-fpr10 | 0.0088 | 0/12 | 11/12 | 0.000 | 0.917 |
| hashpool | nested-youden | 0.0258 | 1/12 | 12/12 | 0.083 | 1.000 |
| hashpool | nested-fpr10 | 0.0251 | 1/12 | 12/12 | 0.083 | 1.000 |
| surface | nested-youden | -0.0044 | 2/12 | 11/12 | 0.167 | 0.917 |
| surface | nested-fpr10 | 0.0024 | 2/12 | 11/12 | 0.167 | 0.917 |
| logit | nested-youden | 0.7394 | 0/12 | 11/12 | 0.000 | 0.917 |
| logit | nested-fpr10 | 0.5464 | 0/12 | 11/12 | 0.000 | 0.917 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.740 mean_pos=-0.0040 mean_neg=-0.0530 diff=0.0490 pos>0=1/12 neg<=0=11/12 perm_p=0.3918 binom_p=0.9998 youden_t=-0.0009 youden_sens=0.833 youden_spec=0.667 J=0.500
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
hitmass auc=0.747 mean_pos=-0.0000 mean_neg=-0.0005 diff=0.0005 pos>0=1/12 neg<=0=11/12 perm_p=0.3908 binom_p=0.9998 youden_t=-0.0000 youden_sens=0.917 youden_spec=0.667 J=0.583
hitmass prompts_marked_above=11/12 instance=key-free-hitmass used_keys=False
hashpool auc=0.521 mean_pos=-0.0044 mean_neg=-0.0073 diff=0.0028 pos>0=4/12 neg<=0=8/12 perm_p=0.3388 binom_p=0.927 youden_t=0.0038 youden_sens=0.250 youden_spec=0.917 J=0.167
hashpool prompts_marked_above=7/12 instance=key-free-hashpool used_keys=False
surface auc=0.646 mean_pos=-0.0140 mean_neg=-0.0206 diff=0.0067 pos>0=2/12 neg<=0=11/12 perm_p=0.1399 binom_p=0.9968 youden_t=-0.0159 youden_sens=0.583 youden_spec=0.750 J=0.333
surface prompts_marked_above=8/12 instance=key-free-surface used_keys=False
logit auc=0.708 mean_pos=-0.3350 mean_neg=-0.4094 diff=0.0744 pos>0=0/12 neg<=0=11/12 perm_p=0.3783 binom_p=1 youden_t=-0.3417 youden_sens=0.583 youden_spec=0.833 J=0.417
logit prompts_marked_above=9/12 instance=key-free-logit used_keys=False
