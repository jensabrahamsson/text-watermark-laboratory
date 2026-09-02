# Key-free probe

probe n_methods=6 pair_dir=/workspace/experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 12/12 | 0.756 | 23/48 | 47/48 | 0.0004998 | 1.5900 |
| pivot-lda | 10/12 | 0.672 | 27/48 | 37/48 | 0.0009995 | 0.0081 |
| pivot-rank | 10/12 | 0.674 | 31/48 | 30/48 | 0.001499 | 5.2222 |
| pivot-lda-entropy | 9/12 | 0.650 | 24/48 | 35/48 | 0.004498 | 0.0073 |
| pivot-rank-entropy | 10/12 | 0.678 | 31/48 | 27/48 | 0.001999 | 5.0535 |
| cascade | 11/12 | 0.798 | 36/48 | 37/48 | 0.0004998 | 1.5945 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 25/48 | 43/48 | 23/0 | 1/4 | 0.958 |
| pivot-lda | 0/48 | 0/48 | 27/21 | 11/37 | 0.711 |
| pivot-rank | 0/48 | 0/48 | 31/17 | 18/30 | 0.633 |
| pivot-lda-entropy | 0/48 | 0/48 | 24/24 | 13/35 | 0.649 |
| pivot-rank-entropy | 0/48 | 0/48 | 31/17 | 21/27 | 0.596 |
| cascade | 0/48 | 0/48 | 36/12 | 11/37 | 0.766 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| postokbackoff | 23/48 | 47/48 | 0.9686 | 0.479 | 0.979 |
| pivot-lda | 27/48 | 37/48 | 0.0000 | 0.562 | 0.771 |
| pivot-rank | 25/48 | 36/48 | 2.7298 | 0.521 | 0.750 |
| pivot-lda-entropy | 19/48 | 31/48 | 0.0005 | 0.396 | 0.646 |
| pivot-rank-entropy | 22/48 | 32/48 | 3.4459 | 0.458 | 0.667 |
| cascade | 27/48 | 40/48 | 0.0068 | 0.562 | 0.833 |

Cascade: count LR when n_used>0, unmarked-LM pivot otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff pivot_weight=uniform prompt_context=False used_keys=False
count covered marked 23/48 >0 23/23 unmarked<=0 4/5 precision=0.958
pivot fallback marked 25/48 >0 13/25 unmarked<=0 33/43
combined marked>0 36/48 unmarked<=0 37/48
Pivot-fallback marked files:
- `02-night-bus` draw 1: The bus is a lr<=0=-0.0088
- `02-night-bus` draw 2: The bus is all lr>0=0.0062
- `02-night-bus` draw 3: After two and a lr<=0=-0.0064
- `02-night-bus` draw 4: The bus is all lr>0=0.0062
- `03-library` draw 1: Closing is the lr<=0=-0.0081
- `03-library` draw 2: Closing is the lr<=0=-0.0081
- `03-library` draw 3: Closing is the lr<=0=-0.0081
- `03-library` draw 4: Closing is the lr<=0=-0.0081
- `04-market` draw 1: The dog gave me lr>0=0.0022
- `04-market` draw 2: The dog gave me lr>0=0.0022
- `04-market` draw 3: The dog gave me lr>0=0.0022
- `04-market` draw 4: The dog gave me lr>0=0.0022
- `06-station` draw 4: The conductor turned and lr>0=0.0529
- `07-rain` draw 2: "My sister's lr<=0=-0.0053
- `08-letter` draw 1: The second version is lr<=0=-0.0142
- `08-letter` draw 2: Now in the second lr<=0=-0.0169
- `08-letter` draw 3: While working on the lr>0=0.0019
- `08-letter` draw 4: The second version is lr<=0=-0.0142
- `10-office` draw 1: The printer worked. lr>0=0.0213
- `10-office` draw 3: The printer worked. lr>0=0.0213
- `10-office` draw 4: The printer worked better lr>0=0.0231
- `11-garden` draw 1: Now a little after lr<=0=-0.0304
- `11-garden` draw 2: The car is really lr>0=0.0109
- `11-garden` draw 3: The car is really lr>0=0.0109
- `11-garden` draw 4: Now a little after lr<=0=-0.0304

postokbackoff auc=0.756 mean_pos=1.4069 mean_neg=-0.1830 diff=1.5900 pos>0=23/48 neg<=0=47/48 perm_p=0.0004998 binom_p=0.6673 youden_t=1.0566 youden_sens=0.479 youden_spec=1.000 J=0.479
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
pivot-lda auc=0.672 mean_pos=0.0036 mean_neg=-0.0045 diff=0.0081 pos>0=27/48 neg<=0=37/48 perm_p=0.0009995 binom_p=0.2354 youden_t=0.0000 youden_sens=0.562 youden_spec=0.771 J=0.333
pivot-lda prompts_marked_above=10/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.674 mean_pos=2.6111 mean_neg=-2.6111 diff=5.2222 pos>0=31/48 neg<=0=30/48 perm_p=0.001499 binom_p=0.02973 youden_t=2.3712 youden_sens=0.604 youden_spec=0.771 J=0.375
pivot-rank prompts_marked_above=10/12 instance=key-free-pivot-rank used_keys=False
pivot-lda-entropy auc=0.650 mean_pos=0.0033 mean_neg=-0.0039 diff=0.0073 pos>0=24/48 neg<=0=35/48 perm_p=0.004498 binom_p=0.5573 youden_t=-0.0013 youden_sens=0.562 youden_spec=0.708 J=0.271
pivot-lda-entropy prompts_marked_above=9/12 instance=key-free-pivot-lda-entropy used_keys=False
pivot-rank-entropy auc=0.678 mean_pos=2.5267 mean_neg=-2.5267 diff=5.0535 pos>0=31/48 neg<=0=27/48 perm_p=0.001999 binom_p=0.02973 youden_t=3.0729 youden_sens=0.562 youden_spec=0.771 J=0.333
pivot-rank-entropy prompts_marked_above=10/12 instance=key-free-pivot-rank-entropy used_keys=False
cascade auc=0.798 mean_pos=1.4070 mean_neg=-0.1875 diff=1.5945 pos>0=36/48 neg<=0=37/48 perm_p=0.0004998 binom_p=0.0003586 youden_t=0.0009 youden_sens=0.750 youden_spec=0.792 J=0.542
cascade prompts_marked_above=11/12 instance=key-free-cascade used_keys=False
