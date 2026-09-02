# Key-free transfer

transfer n_methods=4 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.820 | 39/48 | 33/48 | 0.0004998 | 1.5101 |
| tokhits | 11/12 | 0.674 | 16/48 | 45/48 | 0.0004998 | 1.3486 |
| poshits | 12/12 | 0.873 | 39/48 | 41/48 | 0.0004998 | 1.6315 |
| postokhits | 12/12 | 0.694 | 16/48 | 48/48 | 0.0004998 | 1.4705 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hits | 9/48 | 22/48 | 39/0 | 15/11 | 0.722 |
| tokhits | 32/48 | 39/48 | 16/0 | 3/6 | 0.842 |
| poshits | 9/48 | 33/48 | 39/0 | 7/8 | 0.848 |
| postokhits | 32/48 | 44/48 | 16/0 | 0/4 | 1.000 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.1963 | 39/48 | 38/48 | 0.812 | 0.792 |
| tokhits | in-sample-youden | 0.1963 | 16/48 | 45/48 | 0.333 | 0.938 |
| poshits | in-sample-youden | 0.1963 | 39/48 | 41/48 | 0.812 | 0.854 |
| postokhits | in-sample-youden | 0.1963 | 16/48 | 48/48 | 0.333 | 1.000 |
| hits | nested-youden | 0.3247 | 39/48 | 38/48 | 0.812 | 0.792 |
| hits | nested-fpr10 | 0.2967 | 39/48 | 38/48 | 0.812 | 0.792 |
| tokhits | nested-youden | 0.6481 | 16/48 | 45/48 | 0.333 | 0.938 |
| tokhits | nested-fpr10 | 0.0000 | 16/48 | 45/48 | 0.333 | 0.938 |
| poshits | nested-youden | 0.3114 | 39/48 | 41/48 | 0.812 | 0.854 |
| poshits | nested-fpr10 | 0.3077 | 39/48 | 41/48 | 0.812 | 0.854 |
| postokhits | nested-youden | 0.6481 | 16/48 | 48/48 | 0.333 | 1.000 |
| postokhits | nested-fpr10 | 0.0000 | 16/48 | 48/48 | 0.333 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.820 mean_pos=1.2994 mean_neg=-0.2107 diff=1.5101 pos>0=39/48 neg<=0=33/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0400 youden_sens=0.812 youden_spec=0.792 J=0.604
hits zeros=9/48 vs 22/48 decided_tp=39 fn=0 fp=15 tn=11 precision=0.722 decided_acc=0.769
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
tokhits auc=0.674 mean_pos=1.1351 mean_neg=-0.2135 diff=1.3486 pos>0=16/48 neg<=0=45/48 perm_p=0.0004998 binom_p=0.9934 youden_t=1.1386 youden_sens=0.333 youden_spec=0.958 J=0.292
tokhits zeros=32/48 vs 39/48 decided_tp=16 fn=0 fp=3 tn=6 precision=0.842 decided_acc=0.880
tokhits prompts_marked_above=11/12 instance=key-free-tokhits used_keys=False
poshits auc=0.873 mean_pos=1.2933 mean_neg=-0.3382 diff=1.6315 pos>0=39/48 neg<=0=41/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.854 J=0.667
poshits zeros=9/48 vs 33/48 decided_tp=39 fn=0 fp=7 tn=8 precision=0.848 decided_acc=0.870
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
postokhits auc=0.694 mean_pos=1.1351 mean_neg=-0.3353 diff=1.4705 pos>0=16/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9934 youden_t=0.0000 youden_sens=0.333 youden_spec=1.000 J=0.333
postokhits zeros=32/48 vs 44/48 decided_tp=16 fn=0 fp=0 tn=4 precision=1.000 decided_acc=1.000
postokhits prompts_marked_above=12/12 instance=key-free-postokhits used_keys=False
