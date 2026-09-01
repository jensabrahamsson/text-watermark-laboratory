# Key-free probe

probe n_methods=15 pair_dir=experiments/2026-09-01-pair-distil-100x4 context_len=4 model=distilgpt2 max_draws=None prefix_lens=[] windows=[] fit_prefix=4 pos_bucket=1 rankpath_full=False rankpath_pos_bucket=1 cascade_rankpath_end=None cascade_when=coverage include_first=False prompt_context=False used_keys=False hash_iv=False g_values=False
Key-free scorer comparison. Not detector_mean. Not Claude. AUC is single-file ranking; prompt wins are prompt-group ranking, not per-file accuracy. nested-youden-by-stem is a threshold chosen on other prompt families' already-held-out LRs, not a global peek at the same stem. coverage.json is leave-one-out shared last-k fraction by position; it explains a front-loaded reader, not a keyed detector.
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.

| method | prompt wins | file auc | marked>0 | unmarked<=0 | perm p | mean diff |
|---|---|---|---|---|---|---|
| unigram | 82/100 | 0.683 | 210/400 | 257/400 | 0.0004998 | 0.3494 |
| hard | 84/100 | 0.683 | 211/400 | 242/400 | 0.0004998 | 0.6045 |
| backoff | 85/100 | 0.685 | 206/400 | 246/400 | 0.0004998 | 0.5412 |
| interpolate | 89/100 | 0.750 | 220/400 | 280/400 | 0.0004998 | 1.8054 |
| hits | 91/100 | 0.709 | 216/400 | 244/400 | 0.0004998 | 0.8671 |
| freqhits | 88/100 | 0.690 | 189/400 | 264/400 | 0.0004998 | 0.7683 |
| hitmass | 90/100 | 0.711 | 216/400 | 244/400 | 0.0004998 | 0.4093 |
| gated | 89/100 | 0.698 | 201/400 | 255/400 | 0.0004998 | 0.8170 |
| shrinkage | 91/100 | 0.704 | 212/400 | 244/400 | 0.0004998 | 0.8425 |
| mix | 82/100 | 0.694 | 211/400 | 247/400 | 0.0004998 | 0.5888 |
| hashpool | 91/100 | 0.740 | 218/400 | 268/400 | 0.0004998 | 0.6109 |
| rankpath | 69/100 | 0.598 | 164/400 | 270/400 | 0.0004998 | 0.0799 |
| rankuni | 39/100 | 0.431 | 114/400 | 219/400 | 1 | -0.0052 |
| stack | 93/100 | 0.746 | 195/400 | 321/400 | 0.0004998 | 0.0014 |
| logit | 92/100 | 0.746 | 200/400 | 311/400 | 0.0004998 | 1.3067 |

| method | marked zeros | unmarked zeros | decided tp/fn | decided fp/tn | precision |
|---|---|---|---|---|---|
| unigram | 108/400 | 47/400 | 210/82 | 143/210 | 0.595 |
| hard | 108/400 | 47/400 | 211/81 | 158/195 | 0.572 |
| backoff | 108/400 | 47/400 | 206/86 | 154/199 | 0.572 |
| interpolate | 108/400 | 47/400 | 220/72 | 120/233 | 0.647 |
| hits | 155/400 | 75/400 | 216/29 | 156/169 | 0.581 |
| freqhits | 181/400 | 102/400 | 189/30 | 136/162 | 0.582 |
| hitmass | 155/400 | 75/400 | 216/29 | 156/169 | 0.581 |
| gated | 168/400 | 91/400 | 201/31 | 145/164 | 0.581 |
| shrinkage | 155/400 | 75/400 | 212/33 | 156/169 | 0.576 |
| mix | 108/400 | 47/400 | 211/81 | 153/200 | 0.580 |
| hashpool | 108/400 | 47/400 | 218/74 | 132/221 | 0.623 |
| rankpath | 108/400 | 47/400 | 164/128 | 130/223 | 0.558 |
| rankuni | 108/400 | 47/400 | 114/178 | 181/172 | 0.386 |
| stack | 0/400 | 0/400 | 195/205 | 79/321 | 0.712 |
| logit | 0/400 | 0/400 | 200/200 | 89/311 | 0.692 |

| method | nested-youden-by-stem marked>t | unmarked<=t | mean t | sens | spec |
|---|---|---|---|---|---|
| unigram | 320/400 | 207/400 | -0.0180 | 0.800 | 0.517 |
| hard | 320/400 | 191/400 | -0.0355 | 0.800 | 0.477 |
| backoff | 314/400 | 195/400 | -0.0030 | 0.785 | 0.487 |
| interpolate | 330/400 | 232/400 | -0.0190 | 0.825 | 0.580 |
| hits | 371/400 | 168/400 | -0.0015 | 0.927 | 0.420 |
| freqhits | 370/400 | 161/400 | -0.0029 | 0.925 | 0.403 |
| hitmass | 371/400 | 168/400 | -0.0010 | 0.927 | 0.420 |
| gated | 369/400 | 163/400 | -0.0029 | 0.922 | 0.407 |
| shrinkage | 367/400 | 168/400 | -0.0021 | 0.917 | 0.420 |
| mix | 324/400 | 189/400 | -0.0421 | 0.810 | 0.472 |
| hashpool | 326/400 | 218/400 | -0.0002 | 0.815 | 0.545 |
| rankpath | 272/400 | 222/400 | -0.0056 | 0.680 | 0.555 |
| rankuni | 0/400 | 397/400 | 0.0628 | 0.000 | 0.993 |
| stack | 331/400 | 217/400 | -0.0002 | 0.828 | 0.542 |
| logit | 333/400 | 218/400 | -0.1396 | 0.833 | 0.545 |

unigram auc=0.683 mean_pos=0.2203 mean_neg=-0.1291 diff=0.3494 pos>0=210/400 neg<=0=257/400 perm_p=0.0004998 binom_p=0.1711 youden_t=-0.0184 youden_sens=0.807 youden_spec=0.520 J=0.328
unigram prompts_marked_above=82/100 instance=key-free-unigram used_keys=False
hard auc=0.683 mean_pos=0.4291 mean_neg=-0.1754 diff=0.6045 pos>0=211/400 neg<=0=242/400 perm_p=0.0004998 binom_p=0.1469 youden_t=-0.0368 youden_sens=0.810 youden_spec=0.480 J=0.290
hard prompts_marked_above=84/100 instance=key-free-counts used_keys=False
backoff auc=0.685 mean_pos=0.3899 mean_neg=-0.1513 diff=0.5412 pos>0=206/400 neg<=0=246/400 perm_p=0.0004998 binom_p=0.2912 youden_t=-0.0026 youden_sens=0.790 youden_spec=0.495 J=0.285
backoff prompts_marked_above=85/100 instance=key-free-backoff used_keys=False
interpolate auc=0.750 mean_pos=1.2263 mean_neg=-0.5791 diff=1.8054 pos>0=220/400 neg<=0=280/400 perm_p=0.0004998 binom_p=0.02552 youden_t=-0.0189 youden_sens=0.825 youden_spec=0.583 J=0.407
interpolate prompts_marked_above=89/100 instance=key-free-interpolate used_keys=False
hits auc=0.709 mean_pos=0.4361 mean_neg=-0.4310 diff=0.8671 pos>0=216/400 neg<=0=244/400 perm_p=0.0004998 binom_p=0.06052 youden_t=-0.0015 youden_sens=0.927 youden_spec=0.422 J=0.350
hits prompts_marked_above=91/100 instance=key-free-hits used_keys=False
freqhits auc=0.690 mean_pos=0.3497 mean_neg=-0.4186 diff=0.7683 pos>0=189/400 neg<=0=264/400 perm_p=0.0004998 binom_p=0.8749 youden_t=-0.0029 youden_sens=0.925 youden_spec=0.405 J=0.330
freqhits prompts_marked_above=88/100 instance=key-free-freqhits used_keys=False
hitmass auc=0.711 mean_pos=0.2448 mean_neg=-0.1645 diff=0.4093 pos>0=216/400 neg<=0=244/400 perm_p=0.0004998 binom_p=0.06052 youden_t=-0.0010 youden_sens=0.927 youden_spec=0.422 J=0.350
hitmass prompts_marked_above=90/100 instance=key-free-hitmass used_keys=False
gated auc=0.698 mean_pos=0.3859 mean_neg=-0.4311 diff=0.8170 pos>0=201/400 neg<=0=255/400 perm_p=0.0004998 binom_p=0.4801 youden_t=-0.0029 youden_sens=0.922 youden_spec=0.410 J=0.333
gated prompts_marked_above=89/100 instance=key-free-gated used_keys=False
shrinkage auc=0.704 mean_pos=0.4138 mean_neg=-0.4287 diff=0.8425 pos>0=212/400 neg<=0=244/400 perm_p=0.0004998 binom_p=0.1251 youden_t=-0.0021 youden_sens=0.917 youden_spec=0.422 J=0.340
shrinkage prompts_marked_above=91/100 instance=key-free-shrinkage used_keys=False
mix auc=0.694 mean_pos=0.4067 mean_neg=-0.1821 diff=0.5888 pos>0=211/400 neg<=0=247/400 perm_p=0.0004998 binom_p=0.1469 youden_t=-0.0433 youden_sens=0.828 youden_spec=0.475 J=0.302
mix prompts_marked_above=82/100 instance=key-free-mix used_keys=False
hashpool auc=0.740 mean_pos=0.4432 mean_neg=-0.1676 diff=0.6109 pos>0=218/400 neg<=0=268/400 perm_p=0.0004998 binom_p=0.03999 youden_t=-0.0000 youden_sens=0.815 youden_spec=0.552 J=0.367
hashpool prompts_marked_above=91/100 instance=key-free-hashpool used_keys=False
rankpath auc=0.598 mean_pos=0.0415 mean_neg=-0.0384 diff=0.0799 pos>0=164/400 neg<=0=270/400 perm_p=0.0004998 binom_p=0.9999 youden_t=-0.0056 youden_sens=0.680 youden_spec=0.557 J=0.238
rankpath prompts_marked_above=69/100 instance=key-free-rankpath used_keys=False
rankuni auc=0.431 mean_pos=-0.0033 mean_neg=0.0019 diff=-0.0052 pos>0=114/400 neg<=0=219/400 perm_p=1 binom_p=1 youden_t=0.0631 youden_sens=0.000 youden_spec=1.000 J=0.000
rankuni prompts_marked_above=39/100 instance=key-free-rankuni used_keys=False
stack auc=0.746 mean_pos=0.0007 mean_neg=-0.0007 diff=0.0014 pos>0=195/400 neg<=0=321/400 perm_p=0.0004998 binom_p=0.7088 youden_t=-0.0002 youden_sens=0.835 youden_spec=0.542 J=0.377
stack prompts_marked_above=93/100 instance=key-free-stack used_keys=False
logit auc=0.746 mean_pos=0.7183 mean_neg=-0.5884 diff=1.3067 pos>0=200/400 neg<=0=311/400 perm_p=0.0004998 binom_p=0.5199 youden_t=-0.1396 youden_sens=0.833 youden_spec=0.547 J=0.380
logit prompts_marked_above=92/100 instance=key-free-logit used_keys=False
