# Key-free transfer

transfer n_methods=2 train=/workspace/experiments/2026-08-31-pair-36x4+/workspace/experiments/2026-08-31-pair-long12x4+/workspace/experiments/2026-08-31-pair-tails12x4+/workspace/experiments/2026-08-31-pair-family12x4 test=/workspace/experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=0 cascade_rankpath_end=4
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 10/12 | 0.797 | 34/48 | 48/48 | 0.0004998 | 2.4092 |
| cascade | 10/12 | 0.825 | 35/48 | 43/48 | 0.0004998 | 2.7781 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 6/48 | 42/48 | 34/8 | 0/6 | 1.000 |
| cascade | 0/48 | 0/48 | 35/13 | 5/43 | 0.875 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2) no observed next token under that context. They are abstentions, not sign errors. poshits can still score an *unseen* next token after a shared context via Laplace; that occupancy artifact is not a token preference. tokbackoff shrinks last-k until an observed next token hits; tokbackoff2 stops at last-2. Neither is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| postokbackoff | in-sample-youden | 0.0000 | 34/48 | 48/48 | 0.708 | 1.000 |
| cascade | in-sample-youden | 0.4728 | 35/48 | 46/48 | 0.729 | 0.958 |
| postokbackoff | nested-youden | 0.5388 | 34/48 | 48/48 | 0.708 | 1.000 |
| postokbackoff | nested-fpr10 | 0.0000 | 34/48 | 48/48 | 0.708 | 1.000 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

Cascade: count LR when n_used>0, unmarked-LM rankpath otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff fallback=rankpath pivot_weight=uniform prompt_context=False used_keys=False
count covered marked 42/48 >0 34/42 unmarked<=0 6/6 precision=1.000
rankpath fallback marked 6/48 >0 1/6 unmarked<=0 37/42
combined marked>0 35/48 unmarked<=0 43/48
cascade rankpath_end=4 (opening prefix-N, not the full file)
rankpath uncovered FPR10 t=0.1098 marked>t 1/6 unmarked<=t 38/42
combined at fallback FPR10 marked>t 35/48 unmarked<=t 44/48. Count stays at 0; mixed AUC is still not a detector.
rankpath-fallback marked files:
- `06-station` draw 4: The conductor turned and lr<=0=-0.5998
- `08-letter` draw 2: Now in the second lr<=0=-0.9578
- `08-letter` draw 3: While working on the lr<=0=-0.4075
- `10-office` draw 1: The printer worked. lr<=0=-0.3458
- `10-office` draw 3: The printer worked. lr<=0=-0.3458
- `10-office` draw 4: The printer worked better lr>0=0.5175

postokbackoff auc=0.797 mean_pos=1.9355 mean_neg=-0.4737 diff=2.4092 pos>0=34/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.002758 youden_t=0.0000 youden_sens=0.708 youden_spec=1.000 J=0.708
postokbackoff zeros=6/48 vs 42/48 decided_tp=34 fn=8 fp=0 tn=6 precision=1.000 decided_acc=0.833
postokbackoff prompts_marked_above=10/12 instance=key-free-postokbackoff used_keys=False
cascade auc=0.825 mean_pos=1.8909 mean_neg=-0.8872 diff=2.7781 pos>0=35/48 neg<=0=43/48 perm_p=0.0004998 binom_p=0.001044 youden_t=0.5955 youden_sens=0.708 youden_spec=1.000 J=0.708
cascade zeros=0/48 vs 0/48 decided_tp=35 fn=13 fp=5 tn=43 precision=0.875 decided_acc=0.812
cascade prompts_marked_above=10/12 instance=key-free-cascade used_keys=False
