# Key-free transfer

transfer n_methods=6 train=/workspace/experiments/2026-08-31-pair-36x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=False shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 12/12 | 0.694 | 16/48 | 48/48 | 0.0004998 | 1.4476 |
| pivot-lda | 4/12 | 0.422 | 15/48 | 29/48 | 0.9575 | -0.0041 |
| pivot-rank | 2/12 | 0.317 | 16/48 | 19/48 | 0.999 | -5.2222 |
| rankpath | 10/12 | 0.683 | 28/48 | 33/48 | 0.001999 | 0.6346 |
| rankuni | 8/12 | 0.628 | 29/48 | 25/48 | 0.01899 | 0.1228 |
| cascade | 8/12 | 0.719 | 32/48 | 25/48 | 0.0004998 | 1.4739 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 32/48 | 44/48 | 16/0 | 0/4 | 1.000 |
| pivot-lda | 0/48 | 0/48 | 15/33 | 19/29 | 0.441 |
| pivot-rank | 0/48 | 0/48 | 16/32 | 29/19 | 0.356 |
| rankpath | 0/48 | 0/48 | 28/20 | 15/33 | 0.651 |
| rankuni | 0/48 | 0/48 | 29/19 | 23/25 | 0.558 |
| cascade | 0/48 | 0/48 | 32/16 | 23/25 | 0.582 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff | in-sample-youden | 0.0000 | 16/48 | 48/48 | 0.333 | 1.000 |
| pivot-lda | in-sample-youden | 0.0037 | 15/48 | 42/48 | 0.312 | 0.875 |
| pivot-rank | in-sample-youden | 2.1458 | 14/48 | 26/48 | 0.292 | 0.542 |
| rankpath | in-sample-youden | 0.0817 | 28/48 | 34/48 | 0.583 | 0.708 |
| rankuni | in-sample-youden | 0.0000 | 29/48 | 25/48 | 0.604 | 0.521 |
| cascade | in-sample-youden | 0.5330 | 16/48 | 47/48 | 0.333 | 0.979 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

Cascade: count LR when n_used>0, unmarked-LM rankuni otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff fallback=rankuni pivot_weight=uniform prompt_context=False used_keys=False
count covered marked 16/48 >0 16/16 unmarked<=0 4/4 precision=1.000
rankuni fallback marked 32/48 >0 16/32 unmarked<=0 21/44
combined marked>0 32/48 unmarked<=0 25/48
rankuni-fallback marked files:
- `01-harbour` draw 1: The ferry was so lr>0=0.3787
- `01-harbour` draw 2: The ferry was over lr>0=0.3787
- `01-harbour` draw 3: The ferry was in lr>0=0.1676
- `01-harbour` draw 4: The ferry was in lr>0=0.1676
- `02-night-bus` draw 1: The bus is a lr>0=0.2753
- `02-night-bus` draw 2: The bus is all lr>0=0.1210
- `02-night-bus` draw 3: After two and a lr>0=0.1676
- `02-night-bus` draw 4: The bus is all lr>0=0.1210
- `03-library` draw 1: Closing is the lr<=0=-0.0901
- `03-library` draw 2: Closing is the lr<=0=-0.0901
- `03-library` draw 3: Closing is the lr<=0=-0.0901
- `03-library` draw 4: Closing is the lr<=0=-0.0901
- `04-market` draw 1: The dog gave me lr<=0=-0.1487
- `04-market` draw 2: The dog gave me lr<=0=-0.1487
- `04-market` draw 3: The dog gave me lr<=0=-0.1487
- `04-market` draw 4: The dog gave me lr<=0=-0.1487
- `06-station` draw 4: The conductor turned and lr<=0=-0.1487
- `08-letter` draw 1: The second version is lr<=0=-0.0901
- `08-letter` draw 2: Now in the second lr<=0=-0.2055
- `08-letter` draw 3: While working on the lr>0=0.2753
- `08-letter` draw 4: The second version is lr<=0=-0.0901
- `10-office` draw 1: The printer worked. lr<=0=-0.1487
- `10-office` draw 3: The printer worked. lr<=0=-0.1487
- `10-office` draw 4: The printer worked better lr>0=0.0133
- `11-garden` draw 1: Now a little after lr<=0=-0.4631
- `11-garden` draw 2: The car is really lr>0=0.1210
- `11-garden` draw 3: The car is really lr>0=0.1210
- `11-garden` draw 4: Now a little after lr<=0=-0.4631
- `12-ferry-queue` draw 1: The ferry was so lr>0=0.3787
- `12-ferry-queue` draw 2: The ferry was so lr>0=0.3787
- `12-ferry-queue` draw 3: The ferry was so lr>0=0.3787
- `12-ferry-queue` draw 4: The ferry was waiting lr>0=0.3787

postokbackoff auc=0.694 mean_pos=1.1122 mean_neg=-0.3353 diff=1.4476 pos>0=16/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.9934 youden_t=0.0000 youden_sens=0.333 youden_spec=1.000 J=0.333
postokbackoff zeros=32/48 vs 44/48 decided_tp=16 fn=0 fp=0 tn=4 precision=1.000 decided_acc=1.000
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
pivot-lda auc=0.422 mean_pos=-0.0081 mean_neg=-0.0041 diff=-0.0041 pos>0=15/48 neg<=0=29/48 perm_p=0.9575 binom_p=0.9972 youden_t=0.0070 youden_sens=0.271 youden_spec=0.979 J=0.250
pivot-lda zeros=0/48 vs 0/48 decided_tp=15 fn=33 fp=19 tn=29 precision=0.441 decided_acc=0.458
pivot-lda prompts_marked_above=4/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.317 mean_pos=-3.7708 mean_neg=1.4514 diff=-5.2222 pos>0=16/48 neg<=0=19/48 perm_p=0.999 binom_p=0.9934 youden_t=-11.1875 youden_sens=0.979 youden_spec=0.062 J=0.042
pivot-rank zeros=0/48 vs 0/48 decided_tp=16 fn=32 fp=29 tn=19 precision=0.356 decided_acc=0.365
pivot-rank prompts_marked_above=2/12 instance=key-free-pivot-rank used_keys=False
rankpath auc=0.683 mean_pos=-0.0881 mean_neg=-0.7227 diff=0.6346 pos>0=28/48 neg<=0=33/48 perm_p=0.001999 binom_p=0.1562 youden_t=-0.8521 youden_sens=0.854 youden_spec=0.500 J=0.354
rankpath zeros=0/48 vs 0/48 decided_tp=28 fn=20 fp=15 tn=33 precision=0.651 decided_acc=0.635
rankpath prompts_marked_above=10/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.628 mean_pos=0.0907 mean_neg=-0.0321 diff=0.1228 pos>0=29/48 neg<=0=25/48 perm_p=0.01899 binom_p=0.09671 youden_t=0.0642 youden_sens=0.583 youden_spec=0.708 J=0.292
rankuni zeros=0/48 vs 0/48 decided_tp=29 fn=19 fp=23 tn=25 precision=0.558 decided_acc=0.562
rankuni prompts_marked_above=8/12 instance=key-free-rankuni used_keys=False
cascade auc=0.719 mean_pos=1.1354 mean_neg=-0.3385 diff=1.4739 pos>0=32/48 neg<=0=25/48 perm_p=0.0004998 binom_p=0.01465 youden_t=0.0642 youden_sens=0.646 youden_spec=0.708 J=0.354
cascade zeros=0/48 vs 0/48 decided_tp=32 fn=16 fp=23 tn=25 precision=0.582 decided_acc=0.594
cascade prompts_marked_above=8/12 instance=key-free-cascade used_keys=False
