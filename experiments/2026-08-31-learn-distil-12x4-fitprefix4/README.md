# Key-free learned scorers

Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.

Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

probe n_methods=3 pair_dir=experiments/2026-08-31-pair-distilgpt2-12x4 context_len=4 model=distilgpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free learned scorers, not detector_mean, not Claude, not key recovery. hashlog is ridge logistic on hashed last-k n-grams (laboratory splitmix64, not SynthID). tokmlp is a tiny token MLP. charcnn is a tiny UTF-8 CNN on the decoded prefix. Nested Youden is train-only. A GPT-2 win is not a Qwen or Distil detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| hashlog | 7/12 | 0.569 | 23/48 | 29/48 | 0.09695 | 0.8525 |
| tokmlp | 8/12 | 0.617 | 25/48 | 34/48 | 0.1344 | 0.0562 |
| charcnn | 9/12 | 0.710 | 28/48 | 34/48 | 0.0004998 | 0.4404 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| hashlog | 17/48 | 40/48 | 0.9413 | 0.354 | 0.833 |
| tokmlp | 24/48 | 38/48 | 0.0163 | 0.500 | 0.792 |
| charcnn | 28/48 | 25/48 | -0.1525 | 0.583 | 0.521 |

hashlog auc=0.569 mean_pos=-0.0510 mean_neg=-0.9034 diff=0.8525 pos>0=23/48 neg<=0=29/48 perm_p=0.09695 binom_p=0.6673 youden_t=0.7753 youden_sens=0.479 youden_spec=0.792 J=0.271
hashlog prompts_marked_above=7/12 instance=key-free-hashlog used_keys=False
tokmlp auc=0.617 mean_pos=0.0355 mean_neg=-0.0207 diff=0.0562 pos>0=25/48 neg<=0=34/48 perm_p=0.1344 binom_p=0.4427 youden_t=0.0163 youden_sens=0.500 youden_spec=0.812 J=0.312
tokmlp prompts_marked_above=8/12 instance=key-free-tokmlp used_keys=False
charcnn auc=0.710 mean_pos=0.1857 mean_neg=-0.2547 diff=0.4404 pos>0=28/48 neg<=0=34/48 perm_p=0.0004998 binom_p=0.1562 youden_t=0.1087 youden_sens=0.562 youden_spec=0.771 J=0.333
charcnn prompts_marked_above=9/12 instance=key-free-charcnn used_keys=False
