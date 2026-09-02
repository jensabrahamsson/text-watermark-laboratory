# Key-free transfer

transfer n_methods=2 train=experiments/2026-09-01-pair-distil-100x4 test=experiments/2026-09-01-pair-gpt2-medium-12x4 n_train=100 n_test=12 overlap_mode=drop-from-train dropped=0 context_len=4 model=distilgpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False rankpath_full=False rankpath_pos_bucket=None cascade_rankpath_end=None cascade_when=coverage
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. ranking_without_isolated_tp counts prompt wins with no marked file lr>0; do not read prompt wins as isolated recall. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| poshits | 11/12 | 0.869 | 42/48 | 26/48 | 0.0004998 | 0.5532 |
| postokhits | 11/12 | 0.755 | 20/48 | 48/48 | 0.0004998 | 0.6000 |

| method | prompt wins | ranking wins with no isolated TP | ranking losses with isolated TP |
|---|---|---|---|
| poshits | 11/12 | 0/11 | 1 (11-garden) |
| postokhits | 11/12 | 4/11 (01-harbour, 02-night-bus, 08-letter, 12-ferry-queue) | 0 |

Ranking wins with no isolated TP are prompt groups whose marked mean LR beats unmarked while every marked file has lr<=0. Ranking losses with isolated TP still have marked files above 0 but lose the prompt-mean comparison. Neither column is a detector.

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| poshits | 4/48 | 12/48 | 42/2 | 22/14 | 0.656 |
| postokhits | 26/48 | 37/48 | 20/2 | 0/11 | 1.000 |

Zeros are lr==0: no shared last-k, or (tokhits/postokhits/tokbackoff/postokbackoff/tokbackoff2/postokbackoff2/hashtok/hashtoklen/hashtokbackoff/hashtokbackoff2/hashtoklenbackoff/hashtoklenbackoff2/hashskip/hashtoklen2/hashskip2/hashmask/hashmask2/tokhybrid/hashtokgap/poshashtok/hashtok2) no observed next token under that context (or colliding hash). They are abstentions, not sign errors. poshits and hashpool can still score an *unseen* next token via Laplace; that occupancy artifact is not a token preference. tokbackoff / hashtokbackoff shrink last-k until an observed next token hits; tokbackoff2 / hashtokbackoff2 stop at last-2. hashtoklen / hashtoklenbackoff hash only exact last-k (short prefixes are not mixed into a longer-order table). hashskip hashes exact last-k with one token dropped (tagged skip-grams, not last-(k-1)). hashmask replaces one last-k token with MASK_TAG (length-k templates). hashtoklen2 / hashskip2 / hashmask2 / hashtok2 skip singleton hash collisions (min_count=2). hashtok is the hashpool analog of tokhits. tokhybrid prefers tokhits then hashtok; hashtokgap is the opposite residual (hashtok only where tokhits abstains). None of these is key recovery.

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| poshits | in-sample-youden | -0.0591 | 46/48 | 11/48 | 0.958 | 0.229 |
| postokhits | in-sample-youden | -0.0591 | 46/48 | 11/48 | 0.958 | 0.229 |
| poshits | nested-youden | -0.0015 | 46/48 | 14/48 | 0.958 | 0.292 |
| poshits | nested-fpr10 | 0.1513 | 20/48 | 48/48 | 0.417 | 1.000 |
| postokhits | nested-youden | -0.0026 | 46/48 | 11/48 | 0.958 | 0.229 |
| postokhits | nested-fpr10 | 0.3034 | 20/48 | 48/48 | 0.417 | 1.000 |

poshits auc=0.869 mean_pos=0.2776 mean_neg=-0.2755 diff=0.5532 pos>0=42/48 neg<=0=26/48 perm_p=0.0004998 (file-level, descriptive) binom_p=5.044e-08 (file-level, descriptive) youden_t=0.0211 youden_sens=0.854 youden_spec=0.833 J=0.688
poshits zeros=4/48 vs 12/48 decided_tp=42 fn=2 fp=22 tn=14 precision=0.656 decided_acc=0.700
poshits prompts_marked_above=11/12 ranking_without_isolated_tp=0/11 ranking_losses_with_isolated_tp=1 instance=key-free-poshits used_keys=False
postokhits auc=0.755 mean_pos=0.3059 mean_neg=-0.2941 diff=0.6000 pos>0=20/48 neg<=0=48/48 perm_p=0.0004998 (file-level, descriptive) binom_p=0.9033 (file-level, descriptive) youden_t=0.0000 youden_sens=0.417 youden_spec=1.000 J=0.417
postokhits zeros=26/48 vs 37/48 decided_tp=20 fn=2 fp=0 tn=11 precision=1.000 decided_acc=0.939
postokhits prompts_marked_above=11/12 ranking_without_isolated_tp=4/11 ranking_losses_with_isolated_tp=0 instance=key-free-postokhits used_keys=False
