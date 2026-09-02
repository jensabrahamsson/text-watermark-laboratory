# Key-free probe

probe n_methods=6 pair_dir=/workspace/experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=True used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| postokbackoff | 12/12 | 0.893 | 42/48 | 37/48 | 0.0004998 | 1.5137 |
| pivot-lda | 7/12 | 0.468 | 19/48 | 27/48 | 0.6997 | -0.0012 |
| pivot-rank | 5/12 | 0.461 | 23/48 | 22/48 | 0.6637 | -0.3438 |
| pivot-lda-entropy | 6/12 | 0.452 | 19/48 | 25/48 | 0.7446 | -0.0009 |
| pivot-rank-entropy | 1/12 | 0.382 | 15/48 | 24/48 | 0.9915 | -2.3610 |
| cascade | 10/12 | 0.707 | 30/48 | 29/48 | 0.0004998 | 1.5886 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| postokbackoff | 6/48 | 14/48 | 42/0 | 11/23 | 0.792 |
| pivot-lda | 0/48 | 0/48 | 19/29 | 21/27 | 0.475 |
| pivot-rank | 0/48 | 0/48 | 23/25 | 26/22 | 0.469 |
| pivot-lda-entropy | 0/48 | 0/48 | 19/29 | 23/25 | 0.452 |
| pivot-rank-entropy | 0/48 | 0/48 | 15/33 | 24/24 | 0.385 |
| cascade | 0/48 | 0/48 | 30/18 | 19/29 | 0.612 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| postokbackoff | 41/48 | 40/48 | 0.7144 | 0.854 | 0.833 |
| pivot-lda | 10/48 | 35/48 | 0.0048 | 0.208 | 0.729 |
| pivot-rank | 8/48 | 38/48 | 5.0578 | 0.167 | 0.792 |
| pivot-lda-entropy | 10/48 | 35/48 | 0.0035 | 0.208 | 0.729 |
| pivot-rank-entropy | 38/48 | 2/48 | -7.9191 | 0.792 | 0.042 |
| cascade | 23/48 | 47/48 | 0.9704 | 0.479 | 0.979 |

Cascade: count LR when n_used>0, unmarked-LM pivot otherwise. Signs at 0 are comparable. Mixed AUC is not a detector. Not keys, not a universal detector.
count_method=postokbackoff pivot_weight=uniform prompt_context=True used_keys=False
count covered marked 23/48 >0 23/23 unmarked<=0 4/5 precision=0.958
pivot fallback marked 25/48 >0 7/25 unmarked<=0 25/43
combined marked>0 30/48 unmarked<=0 29/48
Pivot-fallback marked files:
- `02-night-bus` draw 1: The bus is a lr<=0=-0.0111
- `02-night-bus` draw 2: The bus is all lr<=0=-0.0145
- `02-night-bus` draw 3: After two and a lr<=0=-0.0174
- `02-night-bus` draw 4: The bus is all lr<=0=-0.0145
- `03-library` draw 1: Closing is the lr<=0=-0.0201
- `03-library` draw 2: Closing is the lr<=0=-0.0201
- `03-library` draw 3: Closing is the lr<=0=-0.0201
- `03-library` draw 4: Closing is the lr<=0=-0.0201
- `04-market` draw 1: The dog gave me lr<=0=-0.0001
- `04-market` draw 2: The dog gave me lr<=0=-0.0001
- `04-market` draw 3: The dog gave me lr<=0=-0.0001
- `04-market` draw 4: The dog gave me lr<=0=-0.0001
- `06-station` draw 4: The conductor turned and lr>0=0.0000
- `07-rain` draw 2: "My sister's lr>0=0.0155
- `08-letter` draw 1: The second version is lr<=0=-0.0112
- `08-letter` draw 2: Now in the second lr<=0=-0.0107
- `08-letter` draw 3: While working on the lr<=0=-0.0233
- `08-letter` draw 4: The second version is lr<=0=-0.0112
- `10-office` draw 1: The printer worked. lr>0=0.0052
- `10-office` draw 3: The printer worked. lr>0=0.0052
- `10-office` draw 4: The printer worked better lr>0=0.0030
- `11-garden` draw 1: Now a little after lr<=0=-0.0016
- `11-garden` draw 2: The car is really lr>0=0.0057
- `11-garden` draw 3: The car is really lr>0=0.0057
- `11-garden` draw 4: Now a little after lr<=0=-0.0016

postokbackoff auc=0.893 mean_pos=1.1118 mean_neg=-0.4019 diff=1.5137 pos>0=42/48 neg<=0=37/48 perm_p=0.0004998 binom_p=5.044e-08 youden_t=0.7259 youden_sens=0.854 youden_spec=0.854 J=0.708
postokbackoff prompts_marked_above=12/12 instance=key-free-postokbackoff used_keys=False
pivot-lda auc=0.468 mean_pos=-0.0027 mean_neg=-0.0016 diff=-0.0012 pos>0=19/48 neg<=0=27/48 perm_p=0.6997 binom_p=0.9443 youden_t=0.0049 youden_sens=0.333 youden_spec=0.771 J=0.104
pivot-lda prompts_marked_above=7/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.461 mean_pos=-0.7827 mean_neg=-0.4389 diff=-0.3438 pos>0=23/48 neg<=0=22/48 perm_p=0.6637 binom_p=0.6673 youden_t=5.4233 youden_sens=0.229 youden_spec=0.875 J=0.104
pivot-rank prompts_marked_above=5/12 instance=key-free-pivot-rank used_keys=False
pivot-lda-entropy auc=0.452 mean_pos=-0.0010 mean_neg=-0.0001 diff=-0.0009 pos>0=19/48 neg<=0=25/48 perm_p=0.7446 binom_p=0.9443 youden_t=0.0047 youden_sens=0.208 youden_spec=0.854 J=0.062
pivot-lda-entropy prompts_marked_above=6/12 instance=key-free-pivot-lda-entropy used_keys=False
pivot-rank-entropy auc=0.382 mean_pos=-1.8847 mean_neg=0.4763 diff=-2.3610 pos>0=15/48 neg<=0=24/48 perm_p=0.9915 binom_p=0.9972 youden_t=-10.5225 youden_sens=1.000 youden_spec=0.021 J=0.021
pivot-rank-entropy prompts_marked_above=1/12 instance=key-free-pivot-rank-entropy used_keys=False
cascade auc=0.707 mean_pos=1.4036 mean_neg=-0.1849 diff=1.5886 pos>0=30/48 neg<=0=29/48 perm_p=0.0004998 binom_p=0.0557 youden_t=1.0566 youden_sens=0.479 youden_spec=1.000 J=0.479
cascade prompts_marked_above=10/12 instance=key-free-cascade used_keys=False
