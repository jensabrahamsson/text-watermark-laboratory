# Key-free transfer

transfer n_methods=5 train=experiments/2026-08-17-pair-36 test=experiments/2026-08-17-pair-qwen n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 6/12 | 0.524 | 4/12 | 6/12 | 0.2874 | 0.1173 |
| hitmass | 6/12 | 0.524 | 4/12 | 6/12 | 0.2739 | 0.0013 |
| hashpool | 8/12 | 0.500 | 7/12 | 5/12 | 0.3753 | 0.0021 |
| surface | 8/12 | 0.514 | 9/12 | 5/12 | 0.5482 | -0.0011 |
| logit | 8/12 | 0.542 | 0/12 | 11/12 | 0.3043 | 0.1077 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0000 | 4/12 | 6/12 | 0.333 | 0.500 |
| hitmass | in-sample-youden | 0.0000 | 4/12 | 6/12 | 0.333 | 0.500 |
| hashpool | in-sample-youden | 0.0000 | 7/12 | 5/12 | 0.583 | 0.417 |
| surface | in-sample-youden | 0.0000 | 9/12 | 5/12 | 0.750 | 0.417 |
| logit | in-sample-youden | 0.0000 | 0/12 | 11/12 | 0.000 | 0.917 |
| hits | nested-youden | 0.3676 | 0/12 | 11/12 | 0.000 | 0.917 |
| hits | nested-fpr10 | 0.3676 | 0/12 | 11/12 | 0.000 | 0.917 |
| hitmass | nested-youden | 0.0130 | 0/12 | 12/12 | 0.000 | 1.000 |
| hitmass | nested-fpr10 | 0.0120 | 0/12 | 11/12 | 0.000 | 0.917 |
| hashpool | nested-youden | 0.0053 | 6/12 | 6/12 | 0.500 | 0.500 |
| hashpool | nested-fpr10 | 0.0155 | 1/12 | 9/12 | 0.083 | 0.750 |
| surface | nested-youden | 0.0215 | 1/12 | 9/12 | 0.083 | 0.750 |
| surface | nested-fpr10 | 0.0211 | 1/12 | 9/12 | 0.083 | 0.750 |
| logit | nested-youden | 0.1275 | 0/12 | 11/12 | 0.000 | 0.917 |
| logit | nested-fpr10 | -0.5854 | 12/12 | 3/12 | 1.000 | 0.250 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.524 mean_pos=0.0014 mean_neg=-0.1159 diff=0.1173 pos>0=4/12 neg<=0=6/12 perm_p=0.2874 binom_p=0.927 youden_t=-0.0019 youden_sens=1.000 youden_spec=0.417 J=0.417
hits prompts_marked_above=6/12 instance=key-free-hits used_keys=False
hitmass auc=0.524 mean_pos=0.0000 mean_neg=-0.0013 diff=0.0013 pos>0=4/12 neg<=0=6/12 perm_p=0.2739 binom_p=0.927 youden_t=-0.0000 youden_sens=1.000 youden_spec=0.417 J=0.417
hitmass prompts_marked_above=6/12 instance=key-free-hitmass used_keys=False
hashpool auc=0.500 mean_pos=0.0031 mean_neg=0.0011 diff=0.0021 pos>0=7/12 neg<=0=5/12 perm_p=0.3753 binom_p=0.3872 youden_t=-0.0090 youden_sens=0.917 youden_spec=0.333 J=0.250
hashpool prompts_marked_above=8/12 instance=key-free-hashpool used_keys=False
surface auc=0.514 mean_pos=0.0056 mean_neg=0.0067 diff=-0.0011 pos>0=9/12 neg<=0=5/12 perm_p=0.5482 binom_p=0.073 youden_t=0.0003 youden_sens=0.750 youden_spec=0.500 J=0.250
surface prompts_marked_above=8/12 instance=key-free-surface used_keys=False
logit auc=0.542 mean_pos=-0.3351 mean_neg=-0.4428 diff=0.1077 pos>0=0/12 neg<=0=11/12 perm_p=0.3043 binom_p=1 youden_t=-0.4108 youden_sens=0.917 youden_spec=0.417 J=0.333
logit prompts_marked_above=8/12 instance=key-free-logit used_keys=False
