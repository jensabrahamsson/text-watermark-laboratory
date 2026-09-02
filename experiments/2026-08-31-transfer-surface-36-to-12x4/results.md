# Key-free transfer

transfer n_methods=5 train=experiments/2026-08-17-pair-36 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 8/12 | 0.769 | 39/48 | 28/48 | 0.0004998 | 0.6630 |
| hitmass | 10/12 | 0.771 | 39/48 | 28/48 | 0.0004998 | 0.0298 |
| hashpool | 11/12 | 0.766 | 34/48 | 30/48 | 0.0004998 | 0.0483 |
| surface | 9/12 | 0.648 | 36/48 | 19/48 | 0.0009995 | 0.0123 |
| logit | 8/12 | 0.760 | 22/48 | 39/48 | 0.0004998 | 0.9928 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0000 | 39/48 | 28/48 | 0.812 | 0.583 |
| hitmass | in-sample-youden | 0.0000 | 39/48 | 28/48 | 0.812 | 0.583 |
| hashpool | in-sample-youden | 0.0000 | 34/48 | 30/48 | 0.708 | 0.625 |
| surface | in-sample-youden | 0.0000 | 36/48 | 19/48 | 0.750 | 0.396 |
| logit | in-sample-youden | 0.0000 | 22/48 | 39/48 | 0.458 | 0.812 |
| hits | nested-youden | 0.3676 | 22/48 | 40/48 | 0.458 | 0.833 |
| hits | nested-fpr10 | 0.3676 | 22/48 | 40/48 | 0.458 | 0.833 |
| hitmass | nested-youden | 0.0130 | 17/48 | 44/48 | 0.354 | 0.917 |
| hitmass | nested-fpr10 | 0.0120 | 19/48 | 43/48 | 0.396 | 0.896 |
| hashpool | nested-youden | 0.0053 | 33/48 | 34/48 | 0.688 | 0.708 |
| hashpool | nested-fpr10 | 0.0155 | 26/48 | 41/48 | 0.542 | 0.854 |
| surface | nested-youden | 0.0215 | 15/48 | 40/48 | 0.312 | 0.833 |
| surface | nested-fpr10 | 0.0211 | 15/48 | 40/48 | 0.312 | 0.833 |
| logit | nested-youden | 0.1275 | 22/48 | 40/48 | 0.458 | 0.833 |
| logit | nested-fpr10 | -0.5854 | 45/48 | 14/48 | 0.938 | 0.292 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.769 mean_pos=0.6757 mean_neg=0.0127 diff=0.6630 pos>0=39/48 neg<=0=28/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0009 youden_sens=0.812 youden_spec=0.667 J=0.479
hits prompts_marked_above=8/12 instance=key-free-hits used_keys=False
hitmass auc=0.771 mean_pos=0.0291 mean_neg=-0.0007 diff=0.0298 pos>0=39/48 neg<=0=28/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.792 youden_spec=0.667 J=0.458
hitmass prompts_marked_above=10/12 instance=key-free-hitmass used_keys=False
hashpool auc=0.766 mean_pos=0.0412 mean_neg=-0.0071 diff=0.0483 pos>0=34/48 neg<=0=30/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.0143 youden_sens=0.562 youden_spec=0.854 J=0.417
hashpool prompts_marked_above=11/12 instance=key-free-hashpool used_keys=False
surface auc=0.648 mean_pos=0.0170 mean_neg=0.0047 diff=0.0123 pos>0=36/48 neg<=0=19/48 perm_p=0.0009995 binom_p=0.0003586 youden_t=0.0064 youden_sens=0.625 youden_spec=0.625 J=0.250
surface prompts_marked_above=9/12 instance=key-free-surface used_keys=False
logit auc=0.760 mean_pos=0.6436 mean_neg=-0.3492 diff=0.9928 pos>0=22/48 neg<=0=39/48 perm_p=0.0004998 binom_p=0.7646 youden_t=-0.3611 youden_sens=0.812 youden_spec=0.646 J=0.458
logit prompts_marked_above=8/12 instance=key-free-logit used_keys=False
