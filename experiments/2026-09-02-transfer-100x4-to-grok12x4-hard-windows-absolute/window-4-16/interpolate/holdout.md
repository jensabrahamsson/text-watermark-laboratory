indicate holdout mode=transfer n_prompts=12 n_files=96 marked_above_unmarked=21 prompts_marked_above=4 prompts_marked_ge=4 prompt_ties=0 prompt_losses=8 ranking_without_isolated_tp=0/4 ranking_losses_with_isolated_tp=7 marked_lr_positive=20 unmarked_lr_nonpositive=24 margin=0 context_len=4 score_kind=interpolate@w4-16 auc=0.461 perm_p=0.7626 (file-level, descriptive) prompt_sign_p=0.8586 used_keys=False hash_iv=False g_values=False instance=key-free-interpolate
single-file auc=0.461 mean_pos=-0.0962 mean_neg=0.0032 diff=-0.0994 pos>0=20/48 neg<=0=24/48 perm_p=0.7626 (file-level, descriptive) binom_p=0.9033 (file-level, descriptive) youden_t=-0.3714 youden_sens=0.667 youden_spec=0.375 J=0.042
Not detector_mean. Not Claude. Not Anthropic. ≈0 is not “human” and not “Claude has no mark”.
101-service-station-marked.txt: lr=-0.329441 instance=key-free-interpolate
101-service-station-unmarked-gen.txt: lr=-0.445729 instance=key-free-interpolate
101-service-station#1: marked_higher
101-service-station-marked-2.txt: lr=-0.631229 instance=key-free-interpolate
101-service-station-unmarked-gen-2.txt: lr=0.156398 instance=key-free-interpolate
101-service-station#2: unmarked_higher
101-service-station-marked-3.txt: lr=0.285284 instance=key-free-interpolate
101-service-station-unmarked-gen-3.txt: lr=-0.381623 instance=key-free-interpolate
101-service-station#3: marked_higher
101-service-station-marked-4.txt: lr=0.468425 instance=key-free-interpolate
101-service-station-unmarked-gen-4.txt: lr=-0.063554 instance=key-free-interpolate
101-service-station#4: marked_higher
102-car-boot-marked.txt: lr=0.192217 instance=key-free-interpolate
102-car-boot-unmarked-gen.txt: lr=-0.468214 instance=key-free-interpolate
102-car-boot#1: marked_higher
102-car-boot-marked-2.txt: lr=-0.584961 instance=key-free-interpolate
102-car-boot-unmarked-gen-2.txt: lr=-0.611508 instance=key-free-interpolate
102-car-boot#2: marked_higher
102-car-boot-marked-3.txt: lr=-0.521674 instance=key-free-interpolate
102-car-boot-unmarked-gen-3.txt: lr=0.145734 instance=key-free-interpolate
102-car-boot#3: unmarked_higher
102-car-boot-marked-4.txt: lr=0.300769 instance=key-free-interpolate
102-car-boot-unmarked-gen-4.txt: lr=-0.621609 instance=key-free-interpolate
102-car-boot#4: marked_higher
103-bowling-alley-marked.txt: lr=-0.106134 instance=key-free-interpolate
103-bowling-alley-unmarked-gen.txt: lr=0.226071 instance=key-free-interpolate
103-bowling-alley#1: unmarked_higher
103-bowling-alley-marked-2.txt: lr=0.424970 instance=key-free-interpolate
103-bowling-alley-unmarked-gen-2.txt: lr=-0.371445 instance=key-free-interpolate
103-bowling-alley#2: marked_higher
103-bowling-alley-marked-3.txt: lr=0.323410 instance=key-free-interpolate
103-bowling-alley-unmarked-gen-3.txt: lr=0.407175 instance=key-free-interpolate
103-bowling-alley#3: unmarked_higher
103-bowling-alley-marked-4.txt: lr=-0.463216 instance=key-free-interpolate
103-bowling-alley-unmarked-gen-4.txt: lr=0.212292 instance=key-free-interpolate
103-bowling-alley#4: unmarked_higher
104-hospital-corridor-marked.txt: lr=-0.755422 instance=key-free-interpolate
104-hospital-corridor-unmarked-gen.txt: lr=-0.304034 instance=key-free-interpolate
104-hospital-corridor#1: unmarked_higher
104-hospital-corridor-marked-2.txt: lr=-1.805612 instance=key-free-interpolate
104-hospital-corridor-unmarked-gen-2.txt: lr=0.848725 instance=key-free-interpolate
104-hospital-corridor#2: unmarked_higher
104-hospital-corridor-marked-3.txt: lr=-0.394340 instance=key-free-interpolate
104-hospital-corridor-unmarked-gen-3.txt: lr=0.049689 instance=key-free-interpolate
104-hospital-corridor#3: unmarked_higher
104-hospital-corridor-marked-4.txt: lr=-0.073674 instance=key-free-interpolate
104-hospital-corridor-unmarked-gen-4.txt: lr=-0.533746 instance=key-free-interpolate
104-hospital-corridor#4: marked_higher
105-charity-shop-marked.txt: lr=0.803090 instance=key-free-interpolate
105-charity-shop-unmarked-gen.txt: lr=0.292823 instance=key-free-interpolate
105-charity-shop#1: marked_higher
105-charity-shop-marked-2.txt: lr=0.747494 instance=key-free-interpolate
105-charity-shop-unmarked-gen-2.txt: lr=1.099720 instance=key-free-interpolate
105-charity-shop#2: unmarked_higher
105-charity-shop-marked-3.txt: lr=-0.064441 instance=key-free-interpolate
105-charity-shop-unmarked-gen-3.txt: lr=0.038152 instance=key-free-interpolate
105-charity-shop#3: unmarked_higher
105-charity-shop-marked-4.txt: lr=2.275427 instance=key-free-interpolate
105-charity-shop-unmarked-gen-4.txt: lr=0.957907 instance=key-free-interpolate
105-charity-shop#4: marked_higher
106-boxing-gym-marked.txt: lr=0.245322 instance=key-free-interpolate
106-boxing-gym-unmarked-gen.txt: lr=-0.374661 instance=key-free-interpolate
106-boxing-gym#1: marked_higher
106-boxing-gym-marked-2.txt: lr=-0.126087 instance=key-free-interpolate
106-boxing-gym-unmarked-gen-2.txt: lr=0.339170 instance=key-free-interpolate
106-boxing-gym#2: unmarked_higher
106-boxing-gym-marked-3.txt: lr=-0.084304 instance=key-free-interpolate
106-boxing-gym-unmarked-gen-3.txt: lr=-0.080087 instance=key-free-interpolate
106-boxing-gym#3: unmarked_higher
106-boxing-gym-marked-4.txt: lr=0.242896 instance=key-free-interpolate
106-boxing-gym-unmarked-gen-4.txt: lr=0.468995 instance=key-free-interpolate
106-boxing-gym#4: unmarked_higher
107-campsite-marked.txt: lr=-0.845163 instance=key-free-interpolate
107-campsite-unmarked-gen.txt: lr=0.264121 instance=key-free-interpolate
107-campsite#1: unmarked_higher
107-campsite-marked-2.txt: lr=-0.243431 instance=key-free-interpolate
107-campsite-unmarked-gen-2.txt: lr=-0.558702 instance=key-free-interpolate
107-campsite#2: marked_higher
107-campsite-marked-3.txt: lr=-1.046200 instance=key-free-interpolate
107-campsite-unmarked-gen-3.txt: lr=-0.438460 instance=key-free-interpolate
107-campsite#3: unmarked_higher
107-campsite-marked-4.txt: lr=0.118688 instance=key-free-interpolate
107-campsite-unmarked-gen-4.txt: lr=-0.102677 instance=key-free-interpolate
107-campsite#4: marked_higher
108-registry-office-marked.txt: lr=-1.234188 instance=key-free-interpolate
108-registry-office-unmarked-gen.txt: lr=0.135022 instance=key-free-interpolate
108-registry-office#1: unmarked_higher
108-registry-office-marked-2.txt: lr=0.111653 instance=key-free-interpolate
108-registry-office-unmarked-gen-2.txt: lr=0.120714 instance=key-free-interpolate
108-registry-office#2: unmarked_higher
108-registry-office-marked-3.txt: lr=-0.209706 instance=key-free-interpolate
108-registry-office-unmarked-gen-3.txt: lr=-0.754410 instance=key-free-interpolate
108-registry-office#3: marked_higher
108-registry-office-marked-4.txt: lr=-0.014531 instance=key-free-interpolate
108-registry-office-unmarked-gen-4.txt: lr=0.027899 instance=key-free-interpolate
108-registry-office#4: unmarked_higher
109-scrapyard-marked.txt: lr=-0.419905 instance=key-free-interpolate
109-scrapyard-unmarked-gen.txt: lr=0.256844 instance=key-free-interpolate
109-scrapyard#1: unmarked_higher
109-scrapyard-marked-2.txt: lr=0.645873 instance=key-free-interpolate
109-scrapyard-unmarked-gen-2.txt: lr=-0.991080 instance=key-free-interpolate
109-scrapyard#2: marked_higher
109-scrapyard-marked-3.txt: lr=-0.605094 instance=key-free-interpolate
109-scrapyard-unmarked-gen-3.txt: lr=-0.974710 instance=key-free-interpolate
109-scrapyard#3: marked_higher
109-scrapyard-marked-4.txt: lr=-0.339102 instance=key-free-interpolate
109-scrapyard-unmarked-gen-4.txt: lr=0.872755 instance=key-free-interpolate
109-scrapyard#4: unmarked_higher
110-chip-shop-marked.txt: lr=0.094201 instance=key-free-interpolate
110-chip-shop-unmarked-gen.txt: lr=-0.502107 instance=key-free-interpolate
110-chip-shop#1: marked_higher
110-chip-shop-marked-2.txt: lr=-0.232377 instance=key-free-interpolate
110-chip-shop-unmarked-gen-2.txt: lr=0.898547 instance=key-free-interpolate
110-chip-shop#2: unmarked_higher
110-chip-shop-marked-3.txt: lr=0.360066 instance=key-free-interpolate
110-chip-shop-unmarked-gen-3.txt: lr=-0.246807 instance=key-free-interpolate
110-chip-shop#3: marked_higher
110-chip-shop-marked-4.txt: lr=-0.772934 instance=key-free-interpolate
110-chip-shop-unmarked-gen-4.txt: lr=0.361010 instance=key-free-interpolate
110-chip-shop#4: unmarked_higher
111-fire-station-marked.txt: lr=0.108169 instance=key-free-interpolate
111-fire-station-unmarked-gen.txt: lr=-0.703521 instance=key-free-interpolate
111-fire-station#1: marked_higher
111-fire-station-marked-2.txt: lr=-0.737950 instance=key-free-interpolate
111-fire-station-unmarked-gen-2.txt: lr=-0.425262 instance=key-free-interpolate
111-fire-station#2: unmarked_higher
111-fire-station-marked-3.txt: lr=0.384828 instance=key-free-interpolate
111-fire-station-unmarked-gen-3.txt: lr=0.958529 instance=key-free-interpolate
111-fire-station#3: unmarked_higher
111-fire-station-marked-4.txt: lr=-0.737950 instance=key-free-interpolate
111-fire-station-unmarked-gen-4.txt: lr=-0.606075 instance=key-free-interpolate
111-fire-station#4: unmarked_higher
112-taxi-rank-marked.txt: lr=-0.262638 instance=key-free-interpolate
112-taxi-rank-unmarked-gen.txt: lr=2.248005 instance=key-free-interpolate
112-taxi-rank#1: unmarked_higher
112-taxi-rank-marked-2.txt: lr=0.778554 instance=key-free-interpolate
112-taxi-rank-unmarked-gen-2.txt: lr=-0.978201 instance=key-free-interpolate
112-taxi-rank#2: marked_higher
112-taxi-rank-marked-3.txt: lr=0.806383 instance=key-free-interpolate
112-taxi-rank-unmarked-gen-3.txt: lr=-0.031789 instance=key-free-interpolate
112-taxi-rank#3: marked_higher
112-taxi-rank-marked-4.txt: lr=-0.695737 instance=key-free-interpolate
112-taxi-rank-unmarked-gen-4.txt: lr=0.336657 instance=key-free-interpolate
112-taxi-rank#4: unmarked_higher
