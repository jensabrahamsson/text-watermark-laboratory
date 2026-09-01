# Key-free transfer

transfer n_methods=2 train=experiments/2026-09-01-pair-gpt2-medium-100x4 test=experiments/2026-09-01-pair-gpt2-medium-12x4 n_train=100 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=gpt2-medium nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. ranking_without_isolated_tp counts prompt wins with no marked file lr>0; do not read prompt wins as isolated recall. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 11/12 | 0.836 | 39/48 | 41/48 | 0.0004998 | 0.8587 |
| postokhits | 8/12 | 0.625 | 10/48 | 48/48 | 0.0009995 | 0.7974 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| poshits | 11/12 | 0/11 | 0 |
| postokhits | 8/12 | 4/8 (03-library, 04-market, 09-workshop, 11-garden) | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 6/48 | 35/48 | 39/3 | 7/6 | 0.848 |
| postokhits | 35/48 | 42/48 | 10/3 | 0/6 | 1.000 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | 0.5488 | 10/48 | 48/48 | 0.208 | 1.000 |
| postokhits | in-sample-youden | 0.5488 | 10/48 | 48/48 | 0.208 | 1.000 |
| poshits | nested-youden | 1.1256 | 10/48 | 48/48 | 0.208 | 1.000 |
| poshits | nested-fpr10 | 0.1313 | 39/48 | 41/48 | 0.812 | 0.854 |
| postokhits | nested-youden | 1.1256 | 10/48 | 48/48 | 0.208 | 1.000 |
| postokhits | nested-fpr10 | 0.0000 | 10/48 | 48/48 | 0.208 | 1.000 |

poshits auc=0.836 mean_pos=0.6386 mean_neg=-0.2201 diff=0.8587 pos>0=39/48 neg<=0=41/48 perm_p=0.0004998 (file-level, descriptive) binom_p=7.611e-06 (file-level, descriptive) youden_t=0.0000 youden_sens=0.812 youden_spec=0.854 J=0.667
poshits zeros=6/48 vs 35/48 decided_tp=39 fn=3 fp=7 tn=6 precision=0.848 decided_acc=0.818
poshits prompts_marked_above=11/12 ranking_without_isolated_tp=0/11 ranking_losses_with_isolated_tp=0 instance=key-free-poshits used_keys=False
postokhits auc=0.625 mean_pos=0.5578 mean_neg=-0.2396 diff=0.7974 pos>0=10/48 neg<=0=48/48 perm_p=0.0009995 (file-level, descriptive) binom_p=1 (file-level, descriptive) youden_t=0.0000 youden_sens=0.208 youden_spec=1.000 J=0.208
postokhits zeros=35/48 vs 42/48 decided_tp=10 fn=3 fp=0 tn=6 precision=1.000 decided_acc=0.842
postokhits prompts_marked_above=8/12 ranking_without_isolated_tp=4/8 ranking_losses_with_isolated_tp=0 instance=key-free-postokhits used_keys=False
