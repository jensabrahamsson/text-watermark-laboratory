# Key-free transfer

transfer n_methods=2 train=experiments/2026-09-01-pair-qwen-100x4 test=experiments/2026-08-31-pair-qwen-12x4 n_train=100 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=Qwen/Qwen2-1.5B-Instruct nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. ranking_without_isolated_tp counts prompt wins with no marked file lr>0; do not read prompt wins as isolated recall. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 11/12 | 0.770 | 33/48 | 37/48 | 0.0004998 | 1.9264 |
| postokhits | 11/12 | 0.809 | 31/48 | 48/48 | 0.0004998 | 2.1070 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| poshits | 11/12 | 2/11 (01-harbour, 06-station) | 0 |
| postokhits | 11/12 | 2/11 (01-harbour, 06-station) | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 4/48 | 24/48 | 33/11 | 11/13 | 0.750 |
| postokhits | 11/48 | 36/48 | 31/6 | 0/12 | 1.000 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | 0.3838 | 31/48 | 48/48 | 0.646 | 1.000 |
| postokhits | in-sample-youden | 0.3838 | 31/48 | 48/48 | 0.646 | 1.000 |
| poshits | nested-youden | 0.0192 | 33/48 | 38/48 | 0.688 | 0.792 |
| poshits | nested-fpr10 | 0.0276 | 31/48 | 45/48 | 0.646 | 0.938 |
| postokhits | nested-youden | 0.0219 | 31/48 | 48/48 | 0.646 | 1.000 |
| postokhits | nested-fpr10 | 0.0000 | 31/48 | 48/48 | 0.646 | 1.000 |

poshits auc=0.770 mean_pos=1.6667 mean_neg=-0.2597 diff=1.9264 pos>0=33/48 neg<=0=37/48 perm_p=0.0004998 binom_p=0.006642 youden_t=0.2238 youden_sens=0.646 youden_spec=1.000 J=0.646
poshits zeros=4/48 vs 24/48 decided_tp=33 fn=11 fp=11 tn=13 precision=0.750 decided_acc=0.676
poshits prompts_marked_above=11/12 ranking_without_isolated_tp=2/11 ranking_losses_with_isolated_tp=0 instance=key-free-poshits used_keys=False
postokhits auc=0.809 mean_pos=1.8093 mean_neg=-0.2976 diff=2.1070 pos>0=31/48 neg<=0=48/48 perm_p=0.0004998 binom_p=0.02973 youden_t=0.0000 youden_sens=0.646 youden_spec=1.000 J=0.646
postokhits zeros=11/48 vs 36/48 decided_tp=31 fn=6 fp=0 tn=12 precision=1.000 decided_acc=0.878
postokhits prompts_marked_above=11/12 ranking_without_isolated_tp=2/11 ranking_losses_with_isolated_tp=0 instance=key-free-postokhits used_keys=False
