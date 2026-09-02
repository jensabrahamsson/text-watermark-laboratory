# Key-free probe

probe n_methods=6 pair_dir=/workspace/experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 12/12 | 0.756 | 23/48 | 47/48 | 0.0004998 | 1.5900 |
| pivot-lda | 10/12 | 0.672 | 27/48 | 37/48 | 0.0009995 | 0.0081 |
| pivot-rank | 10/12 | 0.674 | 31/48 | 30/48 | 0.001499 | 5.2222 |
| rankpath | 12/12 | 0.797 | 41/48 | 39/48 | 0.0004998 | 1.5253 |
| rankuni | 11/12 | 0.759 | 33/48 | 32/48 | 0.0004998 | 0.2775 |
| cascade | 12/12 | 0.858 | 37/48 | 33/48 | 0.0004998 | 1.7823 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 25/48 | 43/48 | 23/0 | 1/4 | 0.958 |
| pivot-lda | 0/48 | 0/48 | 27/21 | 11/37 | 0.711 |
| pivot-rank | 0/48 | 0/48 | 31/17 | 18/30 | 0.633 |
| rankpath | 0/48 | 5/48 | 41/7 | 9/34 | 0.820 |
| rankuni | 0/48 | 0/48 | 33/15 | 16/32 | 0.673 |
| cascade | 0/48 | 0/48 | 37/11 | 15/33 | 0.712 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| postokbackoff | 23/48 | 47/48 | 0.9686 | 0.479 | 0.979 |
| pivot-lda | 27/48 | 37/48 | 0.0000 | 0.562 | 0.771 |
| pivot-rank | 25/48 | 36/48 | 2.7298 | 0.521 | 0.750 |
| rankpath | 37/48 | 39/48 | 0.0206 | 0.771 | 0.812 |
| rankuni | 29/48 | 36/48 | 0.1287 | 0.604 | 0.750 |
| cascade | 30/48 | 37/48 | 0.1541 | 0.625 | 0.771 |

Cascade: count LR when n_used>0, unmarked-LM rankuni otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff fallback=rankuni pivot_weight=uniform prompt_context=False used_keys=False
count covered marked 23/48 >0 23/23 unmarked<=0 4/5 precision=0.958
rankuni fallback marked 25/48 >0 14/25 unmarked<=0 29/43
combined marked>0 37/48 unmarked<=0 33/48
rankuni-fallback marked files:
- `02-night-bus` draw 1: The bus is a lr>0=0.3289
- `02-night-bus` draw 2: The bus is all lr>0=0.5554
- `02-night-bus` draw 3: After two and a lr<=0=-0.1073
- `02-night-bus` draw 4: The bus is all lr>0=0.5554
- `03-library` draw 1: Closing is the lr>0=0.1903
- `03-library` draw 2: Closing is the lr>0=0.1903
- `03-library` draw 3: Closing is the lr>0=0.1903
- `03-library` draw 4: Closing is the lr>0=0.1903
- `04-market` draw 1: The dog gave me lr<=0=-0.1366
- `04-market` draw 2: The dog gave me lr<=0=-0.1366
- `04-market` draw 3: The dog gave me lr<=0=-0.1366
- `04-market` draw 4: The dog gave me lr<=0=-0.1366
- `06-station` draw 4: The conductor turned and lr<=0=-0.0030
- `07-rain` draw 2: "My sister's lr>0=0.2674
- `08-letter` draw 1: The second version is lr>0=0.1810
- `08-letter` draw 2: Now in the second lr<=0=-0.5965
- `08-letter` draw 3: While working on the lr>0=0.2951
- `08-letter` draw 4: The second version is lr>0=0.1810
- `10-office` draw 1: The printer worked. lr<=0=-0.0162
- `10-office` draw 3: The printer worked. lr<=0=-0.0162
- `10-office` draw 4: The printer worked better lr>0=0.1807
- `11-garden` draw 1: Now a little after lr<=0=-0.3236
- `11-garden` draw 2: The car is really lr>0=0.5857
- `11-garden` draw 3: The car is really lr>0=0.5857
- `11-garden` draw 4: Now a little after lr<=0=-0.3236

postokbackoff auc=0.756 mean_pos=1.4069 mean_neg=-0.1830 diff=1.5900 pos>0=23/48 neg<=0=47/48 perm_p=0.0004998 binom_p=0.6673 youden_t=1.0566 youden_sens=0.479 youden_spec=1.000 J=0.479
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
pivot-lda auc=0.672 mean_pos=0.0036 mean_neg=-0.0045 diff=0.0081 pos>0=27/48 neg<=0=37/48 perm_p=0.0009995 binom_p=0.2354 youden_t=0.0000 youden_sens=0.562 youden_spec=0.771 J=0.333
pivot-lda prompts_marked_above=10/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.674 mean_pos=2.6111 mean_neg=-2.6111 diff=5.2222 pos>0=31/48 neg<=0=30/48 perm_p=0.001499 binom_p=0.02973 youden_t=2.3712 youden_sens=0.604 youden_spec=0.771 J=0.375
pivot-rank prompts_marked_above=10/12 instance=key-free-pivot-rank used_keys=False
rankpath auc=0.797 mean_pos=0.4782 mean_neg=-1.0471 diff=1.5253 pos>0=41/48 neg<=0=39/48 perm_p=0.0004998 binom_p=3.12e-07 youden_t=0.0000 youden_sens=0.854 youden_spec=0.812 J=0.667
rankpath prompts_marked_above=12/12 instance=key-free-rankpath used_keys=False
rankuni auc=0.759 mean_pos=0.1299 mean_neg=-0.1476 diff=0.2775 pos>0=33/48 neg<=0=32/48 perm_p=0.0004998 binom_p=0.006642 youden_t=0.1271 youden_sens=0.688 youden_spec=0.771 J=0.458
rankuni prompts_marked_above=11/12 instance=key-free-rankuni used_keys=False
cascade auc=0.858 mean_pos=1.4599 mean_neg=-0.3224 diff=1.7823 pos>0=37/48 neg<=0=33/48 perm_p=0.0004998 binom_p=0.0001111 youden_t=0.1271 youden_sens=0.771 youden_spec=0.792 J=0.562
cascade prompts_marked_above=12/12 instance=key-free-cascade used_keys=False
