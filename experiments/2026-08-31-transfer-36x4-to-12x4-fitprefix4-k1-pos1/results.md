# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-17-pair-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=1 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 11/12 | 0.846 | 39/48 | 38/48 | 0.0004998 | 1.1678 |
| first | 6/12 | 0.555 | 16/48 | 40/48 | 0.1784 | 0.2256 |
| poshits | 12/12 | 0.873 | 39/48 | 41/48 | 0.0004998 | 1.2285 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.0611 | 39/48 | 38/48 | 0.812 | 0.792 |
| first | in-sample-youden | 0.0000 | 16/48 | 40/48 | 0.333 | 0.833 |
| poshits | in-sample-youden | 0.2162 | 16/48 | 48/48 | 0.333 | 1.000 |
| hits | nested-youden | 0.4092 | 16/48 | 45/48 | 0.333 | 0.938 |
| hits | nested-fpr10 | 0.1097 | 31/48 | 40/48 | 0.646 | 0.833 |
| first | nested-youden | 0.0000 | 16/48 | 40/48 | 0.333 | 0.833 |
| first | nested-fpr10 | 0.9299 | 0/48 | 48/48 | 0.000 | 1.000 |
| poshits | nested-youden | 0.3916 | 16/48 | 48/48 | 0.333 | 1.000 |
| poshits | nested-fpr10 | 0.0922 | 31/48 | 43/48 | 0.646 | 0.896 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.846 mean_pos=1.0204 mean_neg=-0.1474 diff=1.1678 pos>0=39/48 neg<=0=38/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.792 J=0.604
hits prompts_marked_above=11/12 instance=key-free-hits used_keys=False
first auc=0.555 mean_pos=-0.5173 mean_neg=-0.7429 diff=0.2256 pos>0=16/48 neg<=0=40/48 perm_p=0.1784 binom_p=0.9934 youden_t=-2.1972 youden_sens=1.000 youden_spec=0.188 J=0.188
first prompts_marked_above=6/12 instance=key-free-first used_keys=False
poshits auc=0.873 mean_pos=1.0099 mean_neg=-0.2186 diff=1.2285 pos>0=39/48 neg<=0=41/48 perm_p=0.0004998 binom_p=7.611e-06 youden_t=0.0000 youden_sens=0.812 youden_spec=0.854 J=0.667
poshits prompts_marked_above=12/12 instance=key-free-poshits used_keys=False
