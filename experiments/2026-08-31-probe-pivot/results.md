# Key-free probe

probe n_methods=3 pair_dir=experiments/2026-08-17-pair-12x4 context_len=4 model=gpt2 used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are the 10/12 grain.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| unigram | 11/12 | 0.592 | 26/48 | 24/48 | 0.03148 | 0.0243 |
| pivot-lda | 10/12 | 0.599 | 17/48 | 31/48 | 0.01649 | 0.0050 |
| pivot-rank | 8/12 | 0.609 | 26/48 | 27/48 | 0.04498 | 0.3657 |

unigram auc=0.592 mean_pos=0.0153 mean_neg=-0.0090 diff=0.0243 pos>0=26/48 neg<=0=24/48 perm_p=0.03148 binom_p=0.3327 youden_t=-0.0297 youden_sens=0.792 youden_spec=0.458 J=0.250
unigram prompts_marked_above=11/12 instance=key-free-unigram used_keys=False
pivot-lda auc=0.599 mean_pos=0.0019 mean_neg=-0.0031 diff=0.0050 pos>0=17/48 neg<=0=31/48 perm_p=0.01649 binom_p=0.9853 youden_t=-0.0045 youden_sens=0.750 youden_spec=0.521 J=0.271
pivot-lda prompts_marked_above=10/12 instance=key-free-pivot-lda used_keys=False
pivot-rank auc=0.609 mean_pos=0.1829 mean_neg=-0.1829 diff=0.3657 pos>0=26/48 neg<=0=27/48 perm_p=0.04498 binom_p=0.3327 youden_t=-0.6632 youden_sens=0.812 youden_spec=0.417 J=0.229
pivot-rank prompts_marked_above=8/12 instance=key-free-pivot-rank used_keys=False
