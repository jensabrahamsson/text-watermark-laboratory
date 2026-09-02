# Key-free transfer

transfer n_methods=2 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.820 | 39/48 | 33/48 | 0.0004998 | 1.5101 |
| poshits | 12/12 | 0.873 | 39/48 | 41/48 | 0.0004998 | 1.6315 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.1963 | 39/48 | 38/48 | 0.812 | 0.792 |
| poshits | in-sample-youden | 0.1963 | 39/48 | 41/48 | 0.812 | 0.854 |
| hits | nested-youden | 0.3247 | 39/48 | 38/48 | 0.812 | 0.792 |
| hits | nested-fpr10 | 0.2967 | 39/48 | 38/48 | 0.812 | 0.792 |
| poshits | nested-youden | 0.3114 | 39/48 | 41/48 | 0.812 | 0.854 |
| poshits | nested-fpr10 | 0.3077 | 39/48 | 41/48 | 0.812 | 0.854 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.820 mean_pos=1.2994 mean_neg=-0.2107 diff=1.5101 pos>0=39/48 neg<=0=33/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0400 youden_sens=0.812 youden_spec=0.792 J=0.604
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
poshits auc=0.873 mean_pos=1.2933 mean_neg=-0.3382 diff=1.6315 pos>0=39/48 neg<=0=41/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.854 J=0.667
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
