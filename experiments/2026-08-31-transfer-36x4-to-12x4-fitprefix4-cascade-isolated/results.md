# Key-free transfer

transfer n_methods=6 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 12/12 | 0.694 | 16/48 | 48/48 | 0.0004998 | 1.4476 |
| pivot-lda | 4/12 | 0.422 | 15/48 | 29/48 | 0.9575 | -0.0041 |
| pivot-rank | 2/12 | 0.317 | 16/48 | 19/48 | 0.999 | -5.2222 |
| pivot-lda-entropy | 4/12 | 0.421 | 15/48 | 31/48 | 0.954 | -0.0040 |
| pivot-rank-entropy | 10/12 | 0.678 | 32/48 | 26/48 | 0.001999 | 5.0535 |
| cascade | 6/12 | 0.517 | 18/48 | 31/48 | 0.0004998 | 1.4414 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 32/48 | 44/48 | 16/0 | 0/4 | 1.000 |
| pivot-lda | 0/48 | 0/48 | 15/33 | 19/29 | 0.441 |
| pivot-rank | 0/48 | 0/48 | 16/32 | 29/19 | 0.356 |
| pivot-lda-entropy | 0/48 | 0/48 | 15/33 | 17/31 | 0.469 |
| pivot-rank-entropy | 0/48 | 0/48 | 32/16 | 22/26 | 0.593 |
| cascade | 0/48 | 0/48 | 18/30 | 17/31 | 0.514 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff | in-sample-youden | 0.0000 | 16/48 | 48/48 | 0.333 | 1.000 |
| pivot-lda | in-sample-youden | 0.0037 | 15/48 | 42/48 | 0.312 | 0.875 |
| pivot-rank | in-sample-youden | 2.1458 | 14/48 | 26/48 | 0.292 | 0.542 |
| pivot-lda-entropy | in-sample-youden | 0.0027 | 15/48 | 37/48 | 0.312 | 0.771 |
| pivot-rank-entropy | in-sample-youden | 9.7142 | 5/48 | 44/48 | 0.104 | 0.917 |
| cascade | in-sample-youden | 0.0059 | 17/48 | 45/48 | 0.354 | 0.938 |
| postokbackoff | nested-youden | 0.6481 | 16/48 | 48/48 | 0.333 | 1.000 |
| postokbackoff | nested-fpr10 | 0.0000 | 16/48 | 48/48 | 0.333 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

Cascade: count LR when n_used>0, unmarked-LM pivot otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff pivot_weight=uniform prompt_context=False used_keys=False
count covered marked 16/48 >0 16/16 unmarked<=0 4/4 precision=1.000
pivot fallback marked 32/48 >0 2/32 unmarked<=0 27/44
combined marked>0 18/48 unmarked<=0 31/48
Pivot-fallback marked files:
- `01-harbour` draw 1: The ferry was so lr<=0=-0.0269
- `01-harbour` draw 2: The ferry was over lr<=0=-0.0272
- `01-harbour` draw 3: The ferry was in lr<=0=-0.0337
- `01-harbour` draw 4: The ferry was in lr<=0=-0.0337
- `02-night-bus` draw 1: The bus is a lr<=0=-0.0194
- `02-night-bus` draw 2: The bus is all lr<=0=-0.0147
- `02-night-bus` draw 3: After two and a lr>0=0.0049
- `02-night-bus` draw 4: The bus is all lr<=0=-0.0147
- `03-library` draw 1: Closing is the lr<=0=-0.0097
- `03-library` draw 2: Closing is the lr<=0=-0.0097
- `03-library` draw 3: Closing is the lr<=0=-0.0097
- `03-library` draw 4: Closing is the lr<=0=-0.0097
- `04-market` draw 1: The dog gave me lr<=0=-0.0104
- `04-market` draw 2: The dog gave me lr<=0=-0.0104
- `04-market` draw 3: The dog gave me lr<=0=-0.0104
- `04-market` draw 4: The dog gave me lr<=0=-0.0104
- `06-station` draw 4: The conductor turned and lr<=0=-0.0140
- `08-letter` draw 1: The second version is lr<=0=-0.0165
- `08-letter` draw 2: Now in the second lr<=0=-0.0047
- `08-letter` draw 3: While working on the lr>0=0.0101
- `08-letter` draw 4: The second version is lr<=0=-0.0165
- `10-office` draw 1: The printer worked. lr<=0=-0.0171
- `10-office` draw 3: The printer worked. lr<=0=-0.0171
- `10-office` draw 4: The printer worked better lr<=0=-0.0203
- `11-garden` draw 1: Now a little after lr<=0=-0.0113
- `11-garden` draw 2: The car is really lr<=0=-0.0089
- `11-garden` draw 3: The car is really lr<=0=-0.0089
- `11-garden` draw 4: Now a little after lr<=0=-0.0113
- `12-ferry-queue` draw 1: The ferry was so lr<=0=-0.0269
- `12-ferry-queue` draw 2: The ferry was so lr<=0=-0.0269
- `12-ferry-queue` draw 3: The ferry was so lr<=0=-0.0269
- `12-ferry-queue` draw 4: The ferry was waiting lr<=0=-0.0274

postokbackoff auc=0.694 mean_pos=1.1122 mean_neg=-0.3353 diff=1.4476 pos>0=16/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9934 youden_t=0.0000 youden_sens=0.333 youden_spec=1.000 J=0.333
postokbackoff zeros=32/48 vs 44/48 decided_tp=16 fn=0 fp=0 tn=4 precision=1.000 decided_acc=1.000
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
pivot-lda auc=0.422 mean_pos=-0.0081 mean_neg=-0.0041 diff=-0.0041 pos>0=15/48 neg<=0=29/48 perm_p=0.9575 binom_p=0.9972 youden_t=0.0070 youden_sens=0.271 youden_spec=0.979 J=0.250
pivot-lda zeros=0/48 vs 0/48 decided_tp=15 fn=33 fp=19 tn=29 precision=0.441 decided_acc=0.458
pivot-lda prompts_marked_above=4/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.317 mean_pos=-3.7708 mean_neg=1.4514 diff=-5.2222 pos>0=16/48 neg<=0=19/48 perm_p=0.999 binom_p=0.9934 youden_t=-11.1875 youden_sens=0.979 youden_spec=0.062 J=0.042
pivot-rank zeros=0/48 vs 0/48 decided_tp=16 fn=32 fp=29 tn=19 precision=0.356 decided_acc=0.365
pivot-rank prompts_marked_above=2/12 instance=key-free-pivot-rank used_keys=False
pivot-lda-entropy auc=0.421 mean_pos=-0.0081 mean_neg=-0.0041 diff=-0.0040 pos>0=15/48 neg<=0=31/48 perm_p=0.954 binom_p=0.9972 youden_t=0.0051 youden_sens=0.312 youden_spec=0.938 J=0.250
pivot-lda-entropy zeros=0/48 vs 0/48 decided_tp=15 fn=33 fp=17 tn=31 precision=0.469 decided_acc=0.479
pivot-lda-entropy prompts_marked_above=4/12 instance=key-free-pivot-lda-entropy used_keys=False
pivot-rank-entropy auc=0.678 mean_pos=3.2716 mean_neg=-1.7819 diff=5.0535 pos>0=32/48 neg<=0=26/48 perm_p=0.001999 binom_p=0.01465 youden_t=3.9511 youden_sens=0.562 youden_spec=0.771 J=0.333
pivot-rank-entropy zeros=0/48 vs 0/48 decided_tp=32 fn=16 fp=22 tn=26 precision=0.593 decided_acc=0.604
pivot-rank-entropy prompts_marked_above=10/12 instance=key-free-pivot-rank-entropy used_keys=False
cascade auc=0.517 mean_pos=1.1020 mean_neg=-0.3394 diff=1.4414 pos>0=18/48 neg<=0=31/48 perm_p=0.0004998 binom_p=0.9703 youden_t=0.0094 youden_sens=0.354 youden_spec=1.000 J=0.354
cascade zeros=0/48 vs 0/48 decided_tp=18 fn=30 fp=17 tn=31 precision=0.514 decided_acc=0.510
cascade prompts_marked_above=6/12 instance=key-free-cascade used_keys=False
