# Key-free transfer

transfer n_methods=6 train=36x4+long12+tails12+family12 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 10/12 | 0.797 | 34/48 | 48/48 | 0.0004998 | 2.4092 |
| pivot-lda | 10/12 | 0.743 | 33/48 | 32/48 | 0.0004998 | 0.0015 |
| pivot-rank | 10/12 | 0.683 | 31/48 | 30/48 | 0.001499 | 5.2222 |
| pivot-lda-entropy | 10/12 | 0.744 | 35/48 | 32/48 | 0.0004998 | 0.0016 |
| pivot-rank-entropy | 10/12 | 0.678 | 31/48 | 27/48 | 0.001999 | 5.0535 |
| cascade | 10/12 | 0.828 | 39/48 | 33/48 | 0.0004998 | 2.4098 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 6/48 | 42/48 | 34/8 | 0/6 | 1.000 |
| pivot-lda | 0/48 | 0/48 | 33/15 | 16/32 | 0.673 |
| pivot-rank | 0/48 | 0/48 | 31/17 | 18/30 | 0.633 |
| pivot-lda-entropy | 0/48 | 0/48 | 35/13 | 16/32 | 0.686 |
| pivot-rank-entropy | 0/48 | 0/48 | 31/17 | 21/27 | 0.596 |
| cascade | 0/48 | 0/48 | 39/9 | 15/33 | 0.722 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff | in-sample-youden | 0.0000 | 34/48 | 48/48 | 0.708 | 1.000 |
| pivot-lda | in-sample-youden | 0.0000 | 33/48 | 33/48 | 0.688 | 0.688 |
| pivot-rank | in-sample-youden | 6.1750 | 22/48 | 40/48 | 0.458 | 0.833 |
| pivot-lda-entropy | in-sample-youden | 0.0002 | 27/48 | 35/48 | 0.562 | 0.729 |
| pivot-rank-entropy | in-sample-youden | 8.2137 | 7/48 | 44/48 | 0.146 | 0.917 |
| cascade | in-sample-youden | 0.0041 | 34/48 | 48/48 | 0.708 | 1.000 |
| postokbackoff | nested-youden | 0.5388 | 34/48 | 48/48 | 0.708 | 1.000 |
| postokbackoff | nested-fpr10 | 0.0000 | 34/48 | 48/48 | 0.708 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

Cascade: count LR when n_used>0, unmarked-LM pivot otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff pivot_weight=uniform prompt_context=False used_keys=False
count covered marked 42/48 >0 34/42 unmarked<=0 6/6 precision=1.000
pivot fallback marked 6/48 >0 5/6 unmarked<=0 27/42
combined marked>0 39/48 unmarked<=0 33/48
Pivot-fallback marked files:
- `06-station` draw 4: The conductor turned and lr>0=0.0033
- `08-letter` draw 2: Now in the second lr<=0=-0.0019
- `08-letter` draw 3: While working on the lr>0=0.0006
- `10-office` draw 1: The printer worked. lr>0=0.0021
- `10-office` draw 3: The printer worked. lr>0=0.0021
- `10-office` draw 4: The printer worked better lr>0=0.0017

postokbackoff auc=0.797 mean_pos=1.9355 mean_neg=-0.4737 diff=2.4092 pos>0=34/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.0000 youden_sens=0.708 youden_spec=1.000 J=0.708
postokbackoff zeros=6/48 vs 42/48 decided_tp=34 fn=8 fp=0 tn=6 precision=1.000 decided_acc=0.833
postokbackoff prompts_marked_above=10/12 instance=key-free-postokbackoff used_keys=False
pivot-lda auc=0.743 mean_pos=0.0010 mean_neg=-0.0005 diff=0.0015 pos>0=33/48 neg<=0=32/48 perm_p=0.0004998 binom_p=0.006642 youden_t=0.0002 youden_sens=0.688 youden_spec=0.729 J=0.417
pivot-lda zeros=0/48 vs 0/48 decided_tp=33 fn=15 fp=16 tn=32 precision=0.673 decided_acc=0.677
pivot-lda prompts_marked_above=10/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.683 mean_pos=2.4250 mean_neg=-2.7972 diff=5.2222 pos>0=31/48 neg<=0=30/48 perm_p=0.001499 binom_p=0.02973 youden_t=2.1750 youden_sens=0.604 youden_spec=0.771 J=0.375
pivot-rank zeros=0/48 vs 0/48 decided_tp=31 fn=17 fp=18 tn=30 precision=0.633 decided_acc=0.635
pivot-rank prompts_marked_above=10/12 instance=key-free-pivot-rank used_keys=False
pivot-lda-entropy auc=0.744 mean_pos=0.0009 mean_neg=-0.0007 diff=0.0016 pos>0=35/48 neg<=0=32/48 perm_p=0.0004998 binom_p=0.001044 youden_t=-0.0001 youden_sens=0.771 youden_spec=0.667 J=0.438
pivot-lda-entropy zeros=0/48 vs 0/48 decided_tp=35 fn=13 fp=16 tn=32 precision=0.686 decided_acc=0.698
pivot-lda-entropy prompts_marked_above=10/12 instance=key-free-pivot-lda-entropy used_keys=False
pivot-rank-entropy auc=0.678 mean_pos=2.1093 mean_neg=-2.9442 diff=5.0535 pos>0=31/48 neg<=0=27/48 perm_p=0.001999 binom_p=0.02973 youden_t=2.7888 youden_sens=0.562 youden_spec=0.771 J=0.333
pivot-rank-entropy zeros=0/48 vs 0/48 decided_tp=31 fn=17 fp=21 tn=27 precision=0.596 decided_acc=0.604
pivot-rank-entropy prompts_marked_above=10/12 instance=key-free-pivot-rank-entropy used_keys=False
cascade auc=0.828 mean_pos=1.9357 mean_neg=-0.4741 diff=2.4098 pos>0=39/48 neg<=0=33/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0030 youden_sens=0.729 youden_spec=1.000 J=0.729
cascade zeros=0/48 vs 0/48 decided_tp=39 fn=9 fp=15 tn=33 precision=0.722 decided_acc=0.750
cascade prompts_marked_above=10/12 instance=key-free-cascade used_keys=False
