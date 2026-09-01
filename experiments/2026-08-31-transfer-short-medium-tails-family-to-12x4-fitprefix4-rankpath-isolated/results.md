# Key-free transfer

transfer n_methods=6 train=/workspace/experiments/2026-08-31-pair-36x4+/workspace/experiments/2026-08-31-pair-long12x4+/workspace/experiments/2026-08-31-pair-tails12x4+/workspace/experiments/2026-08-31-pair-family12x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 10/12 | 0.797 | 34/48 | 48/48 | 0.0004998 | 2.4092 |
| pivot-lda | 10/12 | 0.743 | 33/48 | 32/48 | 0.0004998 | 0.0015 |
| pivot-rank | 10/12 | 0.683 | 31/48 | 30/48 | 0.001499 | 5.2222 |
| rankpath | 12/12 | 0.739 | 30/48 | 32/48 | 0.0004998 | 0.7156 |
| rankuni | 10/12 | 0.785 | 37/48 | 31/48 | 0.0004998 | 0.2192 |
| cascade | 10/12 | 0.811 | 36/48 | 33/48 | 0.0004998 | 2.5001 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 6/48 | 42/48 | 34/8 | 0/6 | 1.000 |
| pivot-lda | 0/48 | 0/48 | 33/15 | 16/32 | 0.673 |
| pivot-rank | 0/48 | 0/48 | 31/17 | 18/30 | 0.633 |
| rankpath | 0/48 | 0/48 | 30/18 | 16/32 | 0.652 |
| rankuni | 0/48 | 1/48 | 37/11 | 17/30 | 0.685 |
| cascade | 0/48 | 1/48 | 36/12 | 15/32 | 0.706 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff | in-sample-youden | 0.0000 | 34/48 | 48/48 | 0.708 | 1.000 |
| pivot-lda | in-sample-youden | 0.0000 | 33/48 | 33/48 | 0.688 | 0.688 |
| pivot-rank | in-sample-youden | 6.1750 | 22/48 | 40/48 | 0.458 | 0.833 |
| rankpath | in-sample-youden | -0.1280 | 31/48 | 29/48 | 0.646 | 0.604 |
| rankuni | in-sample-youden | 0.0000 | 37/48 | 31/48 | 0.771 | 0.646 |
| cascade | in-sample-youden | 0.3663 | 34/48 | 48/48 | 0.708 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

Cascade: count LR when n_used>0, unmarked-LM rankuni otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff fallback=rankuni pivot_weight=uniform prompt_context=False used_keys=False
count covered marked 42/48 >0 34/42 unmarked<=0 6/6 precision=1.000
rankuni fallback marked 6/48 >0 2/6 unmarked<=0 27/42
combined marked>0 36/48 unmarked<=0 33/48
rankuni-fallback marked files:
- `06-station` draw 4: The conductor turned and lr<=0=-0.0593
- `08-letter` draw 2: Now in the second lr<=0=-0.3933
- `08-letter` draw 3: While working on the lr>0=0.1861
- `10-office` draw 1: The printer worked. lr<=0=-0.0593
- `10-office` draw 3: The printer worked. lr<=0=-0.0593
- `10-office` draw 4: The printer worked better lr>0=0.1544

postokbackoff auc=0.797 mean_pos=1.9355 mean_neg=-0.4737 diff=2.4092 pos>0=34/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.0000 youden_sens=0.708 youden_spec=1.000 J=0.708
postokbackoff zeros=6/48 vs 42/48 decided_tp=34 fn=8 fp=0 tn=6 precision=1.000 decided_acc=0.833
postokbackoff prompts_marked_above=10/12 instance=key-free-postokbackoff used_keys=False
pivot-lda auc=0.743 mean_pos=0.0010 mean_neg=-0.0005 diff=0.0015 pos>0=33/48 neg<=0=32/48 perm_p=0.0004998 binom_p=0.006642 youden_t=0.0002 youden_sens=0.688 youden_spec=0.729 J=0.417
pivot-lda zeros=0/48 vs 0/48 decided_tp=33 fn=15 fp=16 tn=32 precision=0.673 decided_acc=0.677
pivot-lda prompts_marked_above=10/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.683 mean_pos=2.4250 mean_neg=-2.7972 diff=5.2222 pos>0=31/48 neg<=0=30/48 perm_p=0.001499 binom_p=0.02973 youden_t=2.1750 youden_sens=0.604 youden_spec=0.771 J=0.375
pivot-rank zeros=0/48 vs 0/48 decided_tp=31 fn=17 fp=18 tn=30 precision=0.633 decided_acc=0.635
pivot-rank prompts_marked_above=10/12 instance=key-free-pivot-rank used_keys=False
rankpath auc=0.739 mean_pos=0.2185 mean_neg=-0.4972 diff=0.7156 pos>0=30/48 neg<=0=32/48 perm_p=0.0004998 binom_p=0.0557 youden_t=-0.6724 youden_sens=0.979 youden_spec=0.438 J=0.417
rankpath zeros=0/48 vs 0/48 decided_tp=30 fn=18 fp=16 tn=32 precision=0.652 decided_acc=0.646
rankpath prompts_marked_above=12/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.785 mean_pos=0.0999 mean_neg=-0.1193 diff=0.2192 pos>0=37/48 neg<=0=31/48 perm_p=0.0004998 binom_p=0.0001111 youden_t=-0.0898 youden_sens=0.917 youden_spec=0.542 J=0.458
rankuni zeros=0/48 vs 1/48 decided_tp=37 fn=11 fp=17 tn=30 precision=0.685 decided_acc=0.705
rankuni prompts_marked_above=10/12 instance=key-free-rankuni used_keys=False
cascade auc=0.811 mean_pos=1.9307 mean_neg=-0.5694 diff=2.5001 pos>0=36/48 neg<=0=33/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=0.2442 youden_sens=0.708 youden_spec=1.000 J=0.708
cascade zeros=0/48 vs 1/48 decided_tp=36 fn=12 fp=15 tn=32 precision=0.706 decided_acc=0.716
cascade prompts_marked_above=10/12 instance=key-free-cascade used_keys=False
