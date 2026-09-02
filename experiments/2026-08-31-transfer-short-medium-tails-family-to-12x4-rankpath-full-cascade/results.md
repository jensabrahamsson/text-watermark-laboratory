# Key-free transfer

transfer n_methods=4 train=/workspace/experiments/2026-08-31-pair-36x4+/workspace/experiments/2026-08-31-pair-long12x4+/workspace/experiments/2026-08-31-pair-tails12x4+/workspace/experiments/2026-08-31-pair-family12x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=True rankpath_pos_bucket=0
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 10/12 | 0.797 | 34/48 | 48/48 | 0.0004998 | 2.4092 |
| rankpath | 7/12 | 0.538 | 24/48 | 28/48 | 0.3198 | 0.0020 |
| rankuni | 7/12 | 0.569 | 34/48 | 21/48 | 0.1009 | 0.0008 |
| cascade | 10/12 | 0.822 | 38/48 | 31/48 | 0.0004998 | 2.4139 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 6/48 | 42/48 | 34/8 | 0/6 | 1.000 |
| rankpath | 0/48 | 0/48 | 24/24 | 20/28 | 0.545 |
| rankuni | 0/48 | 0/48 | 34/14 | 27/21 | 0.557 |
| cascade | 0/48 | 0/48 | 38/10 | 17/31 | 0.691 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff | in-sample-youden | 0.0000 | 34/48 | 48/48 | 0.708 | 1.000 |
| rankpath | in-sample-youden | -0.0008 | 25/48 | 27/48 | 0.521 | 0.562 |
| rankuni | in-sample-youden | 0.0013 | 23/48 | 28/48 | 0.479 | 0.583 |
| cascade | in-sample-youden | 0.0414 | 34/48 | 48/48 | 0.708 | 1.000 |
| postokbackoff | nested-youden | 0.5388 | 34/48 | 48/48 | 0.708 | 1.000 |
| postokbackoff | nested-fpr10 | 0.0000 | 34/48 | 48/48 | 0.708 | 1.000 |
| rankpath | nested-youden | 0.0051 | 21/48 | 30/48 | 0.438 | 0.625 |
| rankpath | nested-fpr10 | 0.0195 | 8/48 | 41/48 | 0.167 | 0.854 |
| rankuni | nested-youden | 0.0014 | 21/48 | 29/48 | 0.438 | 0.604 |
| rankuni | nested-fpr10 | 0.0034 | 10/48 | 38/48 | 0.208 | 0.792 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

Cascade: count LR when n_used>0, unmarked-LM rankpath otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff fallback=rankpath pivot_weight=uniform prompt_context=False used_keys=False
count covered marked 42/48 >0 34/42 unmarked<=0 6/6 precision=1.000
rankpath fallback marked 6/48 >0 4/6 unmarked<=0 25/42
combined marked>0 38/48 unmarked<=0 31/48
rankpath-fallback marked files:
- `06-station` draw 4: The conductor turned and lr>0=0.0049
- `08-letter` draw 2: Now in the second lr<=0=-0.0035
- `08-letter` draw 3: While working on the lr<=0=-0.0007
- `10-office` draw 1: The printer worked. lr>0=0.0218
- `10-office` draw 3: The printer worked. lr>0=0.0173
- `10-office` draw 4: The printer worked better lr>0=0.0231

postokbackoff auc=0.797 mean_pos=1.9355 mean_neg=-0.4737 diff=2.4092 pos>0=34/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.0000 youden_sens=0.708 youden_spec=1.000 J=0.708
postokbackoff zeros=6/48 vs 42/48 decided_tp=34 fn=8 fp=0 tn=6 precision=1.000 decided_acc=0.833
postokbackoff prompts_marked_above=10/12 instance=key-free-postokbackoff used_keys=False
rankpath auc=0.538 mean_pos=-0.0001 mean_neg=-0.0021 diff=0.0020 pos>0=24/48 neg<=0=28/48 perm_p=0.3198 binom_p=0.5573 youden_t=0.0035 youden_sens=0.500 youden_spec=0.625 J=0.125
rankpath zeros=0/48 vs 0/48 decided_tp=24 fn=24 fp=20 tn=28 precision=0.545 decided_acc=0.542
rankpath prompts_marked_above=7/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.569 mean_pos=0.0012 mean_neg=0.0004 diff=0.0008 pos>0=34/48 neg<=0=21/48 perm_p=0.1009 binom_p=0.002758 youden_t=-0.0010 youden_sens=0.812 youden_spec=0.396 J=0.208
rankuni zeros=0/48 vs 0/48 decided_tp=34 fn=14 fp=27 tn=21 precision=0.557 decided_acc=0.573
rankuni prompts_marked_above=7/12 instance=key-free-rankuni used_keys=False
cascade auc=0.822 mean_pos=1.9368 mean_neg=-0.4771 diff=2.4139 pos>0=38/48 neg<=0=31/48 perm_p=0.0004998 binom_p=3.085e-05 youden_t=0.0260 youden_sens=0.708 youden_spec=1.000 J=0.708
cascade zeros=0/48 vs 0/48 decided_tp=38 fn=10 fp=17 tn=31 precision=0.691 decided_acc=0.719
cascade prompts_marked_above=10/12 instance=key-free-cascade used_keys=False
