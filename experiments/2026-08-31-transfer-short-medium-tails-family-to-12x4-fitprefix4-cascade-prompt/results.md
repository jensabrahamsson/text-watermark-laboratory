# Key-free transfer

transfer n_methods=6 train=36x4+long12+tails12+family12 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=True
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 12/12 | 0.929 | 41/48 | 39/48 | 0.0004998 | 3.0176 |
| pivot-lda | 9/12 | 0.569 | 30/48 | 25/48 | 0.5942 | -0.0002 |
| pivot-rank | 6/12 | 0.517 | 20/48 | 24/48 | 0.4168 | 0.3229 |
| pivot-lda-entropy | 8/12 | 0.543 | 30/48 | 17/48 | 0.1289 | 0.0002 |
| pivot-rank-entropy | 4/12 | 0.466 | 31/48 | 15/48 | 0.5357 | -0.0323 |
| cascade | 10/12 | 0.839 | 39/48 | 27/48 | 0.0004998 | 2.0845 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 1/48 | 3/48 | 41/6 | 9/36 | 0.820 |
| pivot-lda | 0/48 | 0/48 | 30/18 | 23/25 | 0.566 |
| pivot-rank | 0/48 | 0/48 | 20/28 | 24/24 | 0.455 |
| pivot-lda-entropy | 0/48 | 0/48 | 30/18 | 31/17 | 0.492 |
| pivot-rank-entropy | 0/48 | 0/48 | 31/17 | 33/15 | 0.484 |
| cascade | 0/48 | 0/48 | 39/9 | 21/27 | 0.650 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff | in-sample-youden | 0.5914 | 39/48 | 39/48 | 0.812 | 0.812 |
| pivot-lda | in-sample-youden | -0.0007 | 32/48 | 18/48 | 0.667 | 0.375 |
| pivot-rank | in-sample-youden | 1.5417 | 18/48 | 27/48 | 0.375 | 0.562 |
| pivot-lda-entropy | in-sample-youden | -0.0006 | 43/48 | 5/48 | 0.896 | 0.104 |
| pivot-rank-entropy | in-sample-youden | 2.9741 | 22/48 | 20/48 | 0.458 | 0.417 |
| cascade | in-sample-youden | 0.3636 | 34/48 | 48/48 | 0.708 | 1.000 |
| postokbackoff | nested-youden | 0.3708 | 41/48 | 39/48 | 0.854 | 0.812 |
| postokbackoff | nested-fpr10 | 0.9600 | 32/48 | 48/48 | 0.667 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

Cascade: count LR when n_used>0, unmarked-LM pivot otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff pivot_weight=uniform prompt_context=True used_keys=False
count covered marked 42/48 >0 36/42 unmarked<=0 6/6 precision=1.000
pivot fallback marked 6/48 >0 3/6 unmarked<=0 21/42
combined marked>0 39/48 unmarked<=0 27/48
Pivot-fallback marked files:
- `06-station` draw 4: The conductor turned and lr>0=0.0008
- `08-letter` draw 2: Now in the second lr<=0=-0.0002
- `08-letter` draw 3: While working on the lr<=0=-0.0037
- `10-office` draw 1: The printer worked. lr>0=0.0008
- `10-office` draw 3: The printer worked. lr>0=0.0008
- `10-office` draw 4: The printer worked better lr<=0=-0.0000

postokbackoff auc=0.929 mean_pos=1.7480 mean_neg=-1.2696 diff=3.0176 pos>0=41/48 neg<=0=39/48 perm_p=0.0004998 binom_p=3.12e-07 youden_t=-0.7647 youden_sens=1.000 youden_spec=0.688 J=0.688
postokbackoff zeros=1/48 vs 3/48 decided_tp=41 fn=6 fp=9 tn=36 precision=0.820 decided_acc=0.837
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
pivot-lda auc=0.569 mean_pos=-0.0022 mean_neg=-0.0020 diff=-0.0002 pos>0=30/48 neg<=0=25/48 perm_p=0.5942 binom_p=0.0557 youden_t=0.0003 youden_sens=0.583 youden_spec=0.625 J=0.208
pivot-lda zeros=0/48 vs 0/48 decided_tp=30 fn=18 fp=23 tn=25 precision=0.566 decided_acc=0.573
pivot-lda prompts_marked_above=9/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.517 mean_pos=-0.6563 mean_neg=-0.9792 diff=0.3229 pos>0=20/48 neg<=0=24/48 perm_p=0.4168 binom_p=0.9033 youden_t=4.2917 youden_sens=0.292 youden_spec=0.875 J=0.167
pivot-rank zeros=0/48 vs 0/48 decided_tp=20 fn=28 fp=24 tn=24 precision=0.455 decided_acc=0.458
pivot-rank prompts_marked_above=6/12 instance=key-free-pivot-rank used_keys=False
pivot-lda-entropy auc=0.543 mean_pos=0.0001 mean_neg=-0.0000 diff=0.0002 pos>0=30/48 neg<=0=17/48 perm_p=0.1289 binom_p=0.0557 youden_t=0.0003 youden_sens=0.542 youden_spec=0.604 J=0.146
pivot-lda-entropy zeros=0/48 vs 0/48 decided_tp=30 fn=18 fp=31 tn=17 precision=0.492 decided_acc=0.490
pivot-lda-entropy prompts_marked_above=8/12 instance=key-free-pivot-lda-entropy used_keys=False
pivot-rank-entropy auc=0.466 mean_pos=1.7021 mean_neg=1.7345 diff=-0.0323 pos>0=31/48 neg<=0=15/48 perm_p=0.5357 binom_p=0.02973 youden_t=-3.8666 youden_sens=0.875 youden_spec=0.188 J=0.062
pivot-rank-entropy zeros=0/48 vs 0/48 decided_tp=31 fn=17 fp=33 tn=15 precision=0.484 decided_acc=0.479
pivot-rank-entropy prompts_marked_above=4/12 instance=key-free-pivot-rank-entropy used_keys=False
cascade auc=0.839 mean_pos=1.8026 mean_neg=-0.2819 diff=2.0845 pos>0=39/48 neg<=0=27/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0031 youden_sens=0.750 youden_spec=1.000 J=0.750
cascade zeros=0/48 vs 0/48 decided_tp=39 fn=9 fp=21 tn=27 precision=0.650 decided_acc=0.688
cascade prompts_marked_above=10/12 instance=key-free-cascade used_keys=False
