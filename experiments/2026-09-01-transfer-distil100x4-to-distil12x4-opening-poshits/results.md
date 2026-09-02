# Key-free transfer

transfer n_methods=2 train=experiments/2026-09-01-pair-distil-100x4 test=experiments/2026-08-31-pair-distilgpt2-12x4 n_train=100 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=distilgpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. ranking_without_isolated_tp counts prompt wins with no marked file lr>0; do not read prompt wins as isolated recall. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 9/12 | 0.639 | 25/48 | 25/48 | 0.0009995 | 0.5656 |
| postokhits | 9/12 | 0.660 | 16/48 | 39/48 | 0.001999 | 0.5678 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| poshits | 9/12 | 1/9 (02-night-bus) | 1 (09-workshop) |
| postokhits | 9/12 | 2/9 (02-night-bus, 08-letter) | 1 (09-workshop) |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 22/48 | 11/48 | 25/1 | 23/14 | 0.521 |
| postokhits | 32/48 | 27/48 | 16/0 | 9/12 | 0.640 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | -0.0591 | 48/48 | 12/48 | 1.000 | 0.250 |
| postokhits | in-sample-youden | -0.0591 | 48/48 | 12/48 | 1.000 | 0.250 |
| poshits | nested-youden | -0.0015 | 47/48 | 14/48 | 0.979 | 0.292 |
| poshits | nested-fpr10 | 0.1513 | 16/48 | 40/48 | 0.333 | 0.833 |
| postokhits | nested-youden | -0.0026 | 48/48 | 12/48 | 1.000 | 0.250 |
| postokhits | nested-fpr10 | 0.3034 | 14/48 | 40/48 | 0.292 | 0.833 |

poshits auc=0.639 mean_pos=0.3687 mean_neg=-0.1969 diff=0.5656 pos>0=25/48 neg<=0=25/48 perm_p=0.0009995 binom_p=0.4427 youden_t=-0.0031 youden_sens=0.979 youden_spec=0.292 J=0.271
poshits zeros=22/48 vs 11/48 decided_tp=25 fn=1 fp=23 tn=14 precision=0.521 decided_acc=0.619
poshits prompts_marked_above=9/12 ranking_without_isolated_tp=1/9 ranking_losses_with_isolated_tp=1 instance=key-free-poshits used_keys=False
postokhits auc=0.660 mean_pos=0.3926 mean_neg=-0.1752 diff=0.5678 pos>0=16/48 neg<=0=39/48 perm_p=0.001999 binom_p=0.9934 youden_t=-0.5108 youden_sens=1.000 youden_spec=0.250 J=0.250
postokhits zeros=32/48 vs 27/48 decided_tp=16 fn=0 fp=9 tn=12 precision=0.640 decided_acc=0.757
postokhits prompts_marked_above=9/12 ranking_without_isolated_tp=2/9 ranking_losses_with_isolated_tp=1 instance=key-free-postokhits used_keys=False
