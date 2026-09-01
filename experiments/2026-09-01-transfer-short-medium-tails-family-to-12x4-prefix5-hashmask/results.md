# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4+experiments/2026-08-31-pair-long12x4+experiments/2026-08-31-pair-tails12x4+experiments/2026-08-31-pair-family12x4 test=experiments/2026-08-17-pair-12x4 n_train=60 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashtoklen | 12/12 | 0.701 | 21/48 | 45/48 | 0.0004998 | 0.7758 |
| hashmask | 11/12 | 0.704 | 21/48 | 42/48 | 0.0004998 | 0.7907 |
| hashmask2 | 10/12 | 0.642 | 15/48 | 44/48 | 0.0004998 | 0.5592 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| hashtoklen | 27/48 | 44/48 | 21/0 | 3/1 | 0.875 |
| hashmask | 24/48 | 32/48 | 21/3 | 6/10 | 0.778 |
| hashmask2 | 33/48 | 41/48 | 15/0 | 4/3 | 0.789 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hashtoklen | in-sample-youden | 0.3881 | 21/48 | 45/48 | 0.438 | 0.938 |
| hashmask | in-sample-youden | 0.1186 | 21/48 | 43/48 | 0.438 | 0.896 |
| hashmask2 | in-sample-youden | 0.4044 | 14/48 | 45/48 | 0.292 | 0.938 |
| hashtoklen | nested-youden | 0.1962 | 21/48 | 45/48 | 0.438 | 0.938 |
| hashtoklen | nested-fpr10 | 0.0000 | 21/48 | 45/48 | 0.438 | 0.938 |
| hashmask | nested-youden | 0.7776 | 19/48 | 45/48 | 0.396 | 0.938 |
| hashmask | nested-fpr10 | 0.6030 | 19/48 | 45/48 | 0.396 | 0.938 |
| hashmask2 | nested-youden | 0.7972 | 11/48 | 45/48 | 0.229 | 0.938 |
| hashmask2 | nested-fpr10 | 0.6702 | 12/48 | 45/48 | 0.250 | 0.938 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hashtoklen auc=0.701 mean_pos=0.8070 mean_neg=0.0312 diff=0.7758 pos>0=21/48 neg<=0=45/48 perm_p=0.0004998 binom_p=0.8438 youden_t=0.0000 youden_sens=0.438 youden_spec=0.938 J=0.375
hashtoklen zeros=27/48 vs 44/48 decided_tp=21 fn=0 fp=3 tn=1 precision=0.875 decided_acc=0.880
hashtoklen prompts_marked_above=12/12 instance=key-free-hashtoklen used_keys=False
hashmask auc=0.704 mean_pos=0.6777 mean_neg=-0.1130 diff=0.7907 pos>0=21/48 neg<=0=42/48 perm_p=0.0004998 binom_p=0.8438 youden_t=0.4203 youden_sens=0.417 youden_spec=0.938 J=0.354
hashmask zeros=24/48 vs 32/48 decided_tp=21 fn=3 fp=6 tn=10 precision=0.778 decided_acc=0.775
hashmask prompts_marked_above=11/12 instance=key-free-hashmask used_keys=False
hashmask2 auc=0.642 mean_pos=0.5994 mean_neg=0.0402 diff=0.5592 pos>0=15/48 neg<=0=44/48 perm_p=0.0004998 binom_p=0.9972 youden_t=0.0000 youden_sens=0.312 youden_spec=0.917 J=0.229
hashmask2 zeros=33/48 vs 41/48 decided_tp=15 fn=0 fp=4 tn=3 precision=0.789 decided_acc=0.818
hashmask2 prompts_marked_above=10/12 instance=key-free-hashmask2 used_keys=False
