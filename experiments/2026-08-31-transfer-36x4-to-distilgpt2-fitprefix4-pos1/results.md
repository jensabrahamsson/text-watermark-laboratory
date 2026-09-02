# Key-free transfer

transfer n_methods=3 train=experiments/2026-08-31-pair-36x4 test=experiments/2026-08-31-pair-distilgpt2-12x4 n_train=24 n_test=12 overlap_mode=drop-from-train dropped=12 context_len=4 model=gpt2 nested=True shuffle_seed=None used_keys=False hash_iv=False g_values=False include_first=False prompt_context=False
Train on one twin directory, score the other. Shared prompt stems are dropped as overlap_mode says. In-sample Youden is optimistic. nested-youden / nested-fpr10 come from leave-one-prompt-out on training stems only, then frozen on the test files. Not detector_mean. Not Claude. Not key recovery.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hits | 7/12 | 0.551 | 15/48 | 30/48 | 0.01699 | 0.4044 |
| first | 10/12 | 0.637 | 5/48 | 43/48 | 0.004498 | 0.5281 |
| poshits | 8/12 | 0.582 | 13/48 | 38/48 | 0.001999 | 0.4517 |

| method | source | t | test marked>t | test unmarked≤t | sens | spec |
|---|---|---|---|---|---|---|
| hits | in-sample-youden | 0.1963 | 13/48 | 38/48 | 0.271 | 0.792 |
| first | in-sample-youden | 0.0000 | 5/48 | 43/48 | 0.104 | 0.896 |
| poshits | in-sample-youden | 0.1963 | 13/48 | 39/48 | 0.271 | 0.812 |
| hits | nested-youden | 0.3247 | 13/48 | 38/48 | 0.271 | 0.792 |
| hits | nested-fpr10 | 0.2967 | 13/48 | 38/48 | 0.271 | 0.792 |
| first | nested-youden | 0.0000 | 5/48 | 43/48 | 0.104 | 0.896 |
| first | nested-fpr10 | 0.9299 | 0/48 | 48/48 | 0.000 | 1.000 |
| poshits | nested-youden | 0.3114 | 13/48 | 39/48 | 0.271 | 0.812 |
| poshits | nested-fpr10 | 0.3077 | 13/48 | 39/48 | 0.271 | 0.812 |

dropped stems: 01-harbour, 02-night-bus, 03-library, 04-market, 05-kitchen, 06-station, 07-rain, 08-letter, 09-workshop, 10-office, 11-garden, 12-ferry-queue

hits auc=0.551 mean_pos=0.2880 mean_neg=-0.1164 diff=0.4044 pos>0=15/48 neg<=0=30/48 perm_p=0.01699 binom_p=0.9972 youden_t=-0.0183 youden_sens=1.000 youden_spec=0.167 J=0.167
hits prompts_marked_above=7/12 instance=key-free-hits used_keys=False
first auc=0.637 mean_pos=-0.4725 mean_neg=-1.0006 diff=0.5281 pos>0=5/48 neg<=0=43/48 perm_p=0.004498 binom_p=1 youden_t=-1.6864 youden_sens=0.771 youden_spec=0.479 J=0.250
first prompts_marked_above=10/12 instance=key-free-first used_keys=False
poshits auc=0.582 mean_pos=0.2842 mean_neg=-0.1674 diff=0.4517 pos>0=13/48 neg<=0=38/48 perm_p=0.001999 binom_p=0.9996 youden_t=0.3301 youden_sens=0.104 youden_spec=1.000 J=0.104
poshits prompts_marked_above=8/12 instance=key-free-poshits used_keys=False
