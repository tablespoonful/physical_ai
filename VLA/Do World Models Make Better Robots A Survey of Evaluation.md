---
title: "Do World Models Make Better Robots? A Survey of Evaluation Benchmarks for Predictive Embodied Intelligence"
date: "2026-08-30"
authors: "Gaytri Jena; Kapil Wanaskar; Vinija Jain; Aman Chadha; Vasu Sharma; Amitava Das"
url: https://arxiv.org/abs/2609.29669
pdf: https://arxiv.org/pdf/2609.29669
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.29669)** / [論文ページ](https://arxiv.org/abs/2609.29669)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Do World Models Make Better Robots?** 

A Survey of Evaluation Benchmarks for Predictive Embodied Intelligence 

GAYTRI JENA<sup>∗</sup> , UC Berkeley, USA KAPIL WANASKAR, San Jose State University, USA VINIJA JAIN, Meta, USA AMAN CHADHA, Apple, USA VASU SHARMA, PocketFM, USA 

AMITAVA DAS, Pragya Lab, BITS Pilani Goa, India 

Robot learning now advances along two tracks that rarely meet. On one side, direct Vision-Language-Action (VLA) policies map observations to actions and are scored by closed-loop task success. On the other, predictive and generative world models forecast future observations and are scored by open-loop prediction or generation quality. A natural question sits between them: does world modelling earn a measurable, closed-loop _advantage_ over a direct policy, and for which robotic capabilities? We argue that the field cannot yet answer this question, and that the reason is a gap in how it is measured, not in the models themselves. World-model benchmarks score prediction without ever executing it, while task-success suites host a single policy and never build a world-model versus VLA contrast. 

This survey maps the evaluation landscape around that gap. We catalogue 160 web-verified benchmarks spanning 2017 to 2026 and organise them by evaluation mode, robotic capability, and model family into four lanes: policy suites, embodied agents, world-model evaluation, and prediction-to-action bridges. Across the corpus, 138 of 160 benchmarks are model-agnostic and only 11 (7%) build an explicit VLA-versus-world-model contrast; counterfactual capability is almost entirely unmeasured, and only four benchmarks turn prediction into executed action. We contribute an operational taxonomy, a coverage comparison against the eight closest surveys (ours is the only one to cross capability with model family), an evaluation loop that isolates the advantage of prediction, and an actionable protocol of four advantage-aware metrics anchored on named testbeds. The organising claim is not that world models help or do not help, but that answering the question requires benchmarks built to ask it. 

CCS Concepts: • **Computing methodologies** → **Robotic planning** ; _Computer vision_ ; _Machine learning_ . 

Additional Key Words and Phrases: robot learning, world models, evaluation, benchmarks, vision-language-action models, embodied AI, predictive models, survey 

## **1 Introduction** 

A robot can be taught to act in two broadly different ways. The first learns a _direct policy_ : a function that maps an observation, and often a language instruction, straight to an action. Recent Vision-Language-Action (VLA) models are the prominent instance of this track, and they are judged by running them in an environment and counting task success, on suites such as LIBERO [91], CALVIN [101], RLBench [69], and ManiSkill2 [59]. The second track learns a _world model_ : a predictor of future observations that a controller can plan against. This track spans latent-dynamics predictors (DreamerV3, TD-MPC2), action-conditioned video predictors (iVideoGPT, GR-2), and large generative video models (Sora, Cosmos, Genie), and it is judged not by acting but by the quality of what it predicts or generates, on suites such as VBench [68], EvalCrafter [92], and EWMBench [67]. 

∗The authors contributed to this work independently of their roles and employment. 

> Authors’ Contact Information: Gaytri Jena, UC Berkeley, Berkeley, CA, USA; Kapil Wanaskar, San Jose State University, USA; Vinija Jain, Meta, USA; Aman Chadha, Apple, USA; Vasu Sharma, PocketFM, USA; Amitava Das, Pragya Lab, BITS Pilani Goa, India. 

1 

Jena et al. 

2 


Fig. 1. **Predict or Act?** The survey’s organising question, posed with real benchmarks. _Closed-loop_ (left): policy and embodied suites score task success by running a policy in the environment. _Open-loop_ (right): world-model and video-generation benchmarks score prediction or generation quality with no action. The centre axis is the question neither pole answers, whether prediction earns a closed-loop advantage, built explicitly by only 11 of 160 benchmarks (Table 10). Every tile is a representative figure from the benchmark’s paper and links to it; per-tile provenance is in Table 13. Images © their respective authors, reproduced for scholarly review. 

Between these two tracks sits a question that neither is built to answer: does world modelling earn a measurable, closed-loop _advantage_ over a direct policy, and for which robotic capabilities? Figure 1 poses that question with real benchmarks. On the left, closed-loop policy and embodied suites score success by executing a policy in the environment. On the right, open-loop world-model and video-generation suites score prediction or generation with no action taken. The axis down the centre, whether prediction buys a closed-loop advantage, is the one the field has not instrumented. 

The gap is methodological rather than empirical. A world-model benchmark scores a rollout for realism or physical plausibility and then stops; it never closes the loop, so it cannot report whether the prediction would have helped a robot act. A task-success suite does close the loop, but it hosts a single policy and is deliberately model-agnostic, so it never contrasts a world-model policy against a direct VLA policy under one protocol. A benchmark that could answer the question must run _both_ branches in one closed loop and report the per-capability gain (Section 4, Figure 10). Only a handful of recent “bridge” benchmarks attempt this, and none yet reports a capability-sliced VLA head-to-head. 

This survey is therefore about _evaluation_ , not about models. It maps the benchmark landscape that surrounds the question and asks which benchmarks could, in principle, establish an advantage of prediction. We catalogue 160 web-verified benchmarks spanning 2017 to 2026 and organise them by evaluation mode, robotic capability, and model family. The headline finding is stark: 138 of the 160 benchmarks are model-agnostic and only 11 (7%) build an explicit VLA-versus-world-model contrast, counterfactual capability is almost entirely unmeasured, and only four benchmarks turn prediction into executed action. 

_Contributions._ This survey offers the following. 

Do World Models Make Better Robots? 

3 

= refereed venue (CoRL, IEEE TETCI); others are preprints 

|**RL Reprod.**|[95]<br>**Eval. of Embodied AI**[66]<br>**WM for Robots**[65]<br>**Bench**|**. Constr.**[82]<br>**Ours**|
|---|---|---|
|||_time_|
||**Embodied AI: Sim.**[42]<br>**VLA Datasets**[142]<br>**Embodied WM**[125]|**WM Eval.**_(pos.)_[153]|
|**2019**|**2021**<br>**2026**||


Fig. 2. The closest benchmark/evaluation surveys as a timeline. Two predate the recent wave, an IEEE TETCI survey of embodied-AI simulators and tasks [42] and a CoRL survey of real-robot RL reproducibility [95] (amber = refereed venue); the rest are 2026 preprints on embodied evaluation, VLA data, and world models. None organises the robot-evaluation landscape by evaluation-mode × capability × model-family; the sole work reaching the advantage-of-prediction axis is a _position_ paper [153]. **Ours** ( _★_ ) fills that cell; per-axis coverage is in Table 1. 

- An **operational taxonomy** of 160 robot-evaluation benchmarks across four evaluation lanes and twelve capability areas (Figure 7), with per-benchmark detail in Tables 3 and 10 and placement rules in Table 2. 

- A **profile of the corpus** (Figures 4, 5, 6) and two galleries of the benchmarks’ own subject and results figures (Figures 8, 9), each panel provenance-tracked. 

- A **coverage comparison** against the eight closest benchmark and evaluation surveys (Table 1): ours is the only one that crosses robotic capability with model family under a single protocol. 

- A **contrast-gap analysis** (Section 4): an evaluation loop that isolates the advantage of prediction (Figure 10), a disambiguation of the overloaded term “world model” (Table 7), and a lane-by-lane account of why the contrast is missing (Table 8). 

- An **actionable protocol** for advantage-aware evaluation: four measurable quantities with named testbeds (Table 9, Figure 11). 

The organising claim is deliberately modest. We do not argue that world models help, or that they do not. We argue that the question is currently unanswerable with the benchmarks the field has built, and we specify what a benchmark that could answer it would have to do. 

## **1.1 Related surveys and the empty cell** 

Table 1 places the eight closest surveys and position papers against five axes that a survey of predictive embodied evaluation could organise around: ( _𝛼_ ) evaluation mode, open- versus closed-loop, as the _primary_ axis; ( _𝛽_ ) robotic capability, such as hidden-state, counterfactual, long-horizon, and social; ( _𝛾_ ) a capability-by-model-family crosstabulation, direct VLA against latent, action-conditioned, and generative world models under one protocol; ( _𝛿_ ) a behavioural advantage-of-prediction metric, which we _assess_ in the literature rather than adopt; and ( _𝜀_ ) a comprehensive benchmark catalogue. Existing surveys populate _𝜀_ well and touch _𝛼_ and _𝛽_ in passing, but the capability-by-family cross-tab _𝛾_ is absent everywhere, and the advantage metric _𝛿_ is reached only partially, and only by a position paper [153], never by a survey. Figure 2 places these works on a timeline: two predate the recent world-model wave, and the rest cluster in the last two years, none of them crossing capability with family. 

Jena et al. 

4 

|**Survey**|**Venue**|**Yr**|_𝛼_<br>mode|_𝛽_<br>cap.|_𝛾_<br>family|_𝛿_<br>metric|_𝜀_<br>catalog|
|---|---|---|---|---|---|---|---|
|Evaluation of Embodied AI [66]|Authorea|2026|**~**|**~**|✘|✘|✔|
|VLA Datasets & Bench. [142]|arXiv|2026|✘|✘|✘|✘|✔|
|Benchmark Construction [82]|arXiv|2026|✘|**~**|✘|✘|✔|
|RL Reproducibility [95]|CoRL|2020|✘|✘|✘|✘|✘|
|World Models for Robots [65]|arXiv|2026|**~**|✘|**~**|**~**|**~**|
|Embodied World Models [125]|preprint|2026|**~**|✘|**~**|✘|**~**|
|WM Evaluation_(pos.)_[153]|arXiv|2026|✔|**~**|✘|**~**|✘|
|Embodied AI: Simulators [42]|TETCI|2022|**~**|**~**|✘|✘|✔|
|**Ours (this survey)**|**--**|2026|✔|✔|✔|✔|✔|


Table 1. **Topical coverage of the closest benchmark/evaluation surveys versus ours.** ✔ covered as an organising axis, **~** partial or mentioned in passing, ✘ absent. Axes: _𝛼_ evaluation mode (open- vs closed-loop as the _primary_ axis); _𝛽_ capability cuts (hidden-state, counterfactual, long-horizon, social); _𝛾_ capability × model-family cross-tab (direct VLA vs latent / action-conditioned / generative world models under one protocol); _𝛿_ behavioural advantage-of-prediction metric ( _assessed, not adopted_ ; e.g. ACTION-ATLAS’s World Advantage Score); _𝜀_ comprehensive benchmark catalogue. This survey is the only work that covers _𝛾_ , and _𝛿_ is otherwise reached only _partially_ , and only by a _position_ paper [153], never by a survey. Venues: CoRL, IEEE TETCI; the remaining rows are arXiv or unrefereed preprints (Authorea, Preprints.org). 

## **2 Survey methodology and corpus** 

## **2.1 Scope, search, and verification** 

The unit of this survey is the _benchmark_ : an individually citeable evaluation artefact, a suite, a dataset paired with a scoring protocol, or an interactive environment with a task distribution, that measures robot, embodied-agent, or world-model behaviour. We deliberately exclude three neighbouring categories that a benchmark survey is often confused with: individual models and policies (the systems a benchmark scores), raw datasets with no scoring protocol, and pure simulators with no task distribution. Where a work contributes both a model and a benchmark, only its benchmark enters the corpus. 

Candidates were gathered by parallel web search over arXiv, publisher venues, and project pages, using query strings built from the cross-product of the evaluation lanes (policy, embodied, world-model, bridge) with capability terms (manipulation, navigation, long-horizon, social, counterfactual, physical reasoning, generation quality) and with the terms _benchmark_ , _evaluation_ , and _suite_ . Every candidate was then web-verified against its arXiv or venue page for exact title, first author, year, and identifier; any candidate that could not be verified was dropped rather than recorded from memory, and entries were de-duplicated by both citation key and arXiv identifier. Figure 3 records the resulting funnel in the PRISMA 2020 style [108]; stages that were not logged as counts are marked as such rather than estimated. The procedure yields 160 web-verified benchmarks drawing on 164 references. 

## **2.2 Placement, definitions, and the core-versus-appendix rule** 

Each benchmark is placed on four axes: its evaluation _lane_ (Section 3), the robotic _capability_ it primarily stresses, its evaluation _mode_ (open-loop prediction or generation quality, closed-loop task success, or a prediction-to-action bridge), 

Do World Models Make Better Robots? 

5 


Fig. 3. **Corpus construction** in the PRISMA 2020 style [108]. The left column is the web-search stream behind the landscape corpus (Table 10): five thematic sweeps, de-duplicated by name and arXiv ID, screened to drop datasets and models, and metadata-verified by parallel audit agents. The right column is the venue-targeted and snowball search behind the closest surveys (Table 1). Both streams feed the included set. Candidates whose metadata could not be verified were discarded at harvest; their count was not logged, which we state rather than estimate. 

and whether it builds a native VLA-versus-world-model _contrast_ (explicit, partial, or model-agnostic). Table 2 states the operational definition used for each placement, so that boundary cases are resolved by a written rule rather than by taste; a benchmark counts as building a contrast, for example, only if a direct-policy and a world-model policy are run under one protocol and compared. 

Because the full corpus is large, we split it. A benchmark enters the core taxonomy (Figure 7) when it is cleanly axis-placeable, distinct from its neighbours, and fully characterisable from its paper; the 86 representative benchmarks that meet all three sit in the taxonomy, and the complete set of 160 is catalogued in the landscape table (Table 10, Appendix A). Every count in the survey reconciles with that table. 

## **2.3 The corpus at a glance** 

Figures 4 and 5 profile the corpus, with all counts re-tallied directly from the catalogue rather than taken from any single paper. The 160 benchmarks divide by lane into 37 policy suites, 85 embodied-agent benchmarks, 34 worldmodel-evaluation benchmarks, and 4 prediction-to-action bridges, and by capability area into twelve clusters led by long-horizon planning (26), manipulation and dexterity (22), and generation quality (19). By evaluation mode, 113 score 

Jena et al. 

6 

|**Construct**|**Counts (a benchmark has it if and only if...)**|**Does not count**|
|---|---|---|
|**Open-loop eval (open)**|it scores prediction or generation_quality_on fixed inputs with-<br>out executing the prediction in a feedback loop: video fidelity<br>(FVD), physics or rollout consistency, or frame-level accuracy|any protocol where an action is executed and<br>the environment responds; offline scoring of a<br>policy’s success|
|**Closed-loop eval (closed)**|success is measured by running a policy_in_the environment<br>with state feedback and scoring task outcome: success rate,<br>sub-goal completion, or reward under interaction|scoring a generated video or a static predic-<br>tion; a metric computed without stepping the<br>environment|
|**Bridge (bridge)**|a prediction (imagined rollout, video, or latent plan) is_con-_<br>_verted into executed actions_and scored on the resulting task<br>success|a benchmark that stops at prediction quality;<br>one that never turns a prediction into a control<br>signal|
|**Native VLA-vs-WM con-**<br>**trast (**_𝛾_**)**|the benchmark _itself_ runs both a direct Vision-Language-<br>Action policy and a world-model policy under one protocol<br>and reports the head-to-head|a model-agnostic suite that merely_hosts_either<br>family; a suite evaluated with only one family<br>in the original paper|
|**Advantage-of-prediction**<br>**(**_𝛿_**)**|a metric quantifies the closed-loop_gain_of a predictive policy<br>over a matched direct-VLA baseline on the same tasks (as-<br>sessed, not adopted)|absolute success with no matched baseline;<br>open-loop quality scores; a ranking that never<br>isolates the predictive component|


Table 2. Operational definitions used to place each benchmark on the evaluation axes (§2). They resolve the ambiguous boundary cases: hosting a policy is not the same as _building_ a VLA-vs-world-model contrast ( _𝛾_ ), and an absolute success number is not an advantage-of-prediction measurement ( _𝛿_ ) without a matched baseline. open open-loop, closed closed-loop, bridge bridge. 


Fig. 4. **The catalogued corpus at a glance.** The survey maps 160 web-verified benchmarks across 4 evaluation lanes, spanning 2017–2026 and totalling 164 references; only 11 build an explicit Vision-Language-Action vs world-model contrast. The bars give benchmarks per capability area, with kindred clusters merged (dexterity into manipulation, vision-language navigation into navigation, theory-of-mind into hidden-state); the twelve areas sum to the 160 works of Table 10. Bars are coloured by the dominant lane of each area (teal policy, blue embodied, purple world-model). 

closed-loop task success, 43 score open-loop prediction or generation, and only 4 bridge the two. Publication years show the field’s shape clearly: a steady rise from 2 in 2017 to a peak of 36 in 2024, with the world-model-evaluation lane arriving almost entirely in the last three years (Figure 6). The single most consequential distribution is the contrast axis: 138 of 160 benchmarks are model-agnostic, 11 build a partial contrast, and 11 (7%) build one explicitly. That imbalance is the empirical core of the survey and is taken up in Section 4. 

Do World Models Make Better Robots? 

7 


Fig. 5. **Profile of the 160 catalogue benchmarks** (Table 10), re-counted directly from the catalogue. (a) publication year, showing the 2023–2024 surge; (b) evaluation lane (embodied navigation dominates, then policy suites); (c) evaluation mode (closed-loop task success dominates, open-loop prediction is second, only four bridges reach action); (d) whether the benchmark builds a native Vision-Language-Action vs world-model contrast, the survey’s organising question: **138 of 160 are model-agnostic** , and only **11 (7%)** build the contrast explicitly. Counts are the exact column tallies of Table 10. 

## **3 A taxonomy of robot-evaluation benchmarks** 

Figure 7 organises 86 representative benchmarks under a single root and four evaluation lanes. The lanes are ordered by how close their scoring sits to executed behaviour: from closed-loop policy suites (Section 3 §3.1) and embodied-agent benchmarks (§3.2), through open-loop world-model evaluation (§3.3), to the prediction-to-action bridges (§3.4) that alone turn prediction into action. Within each lane, benchmarks are grouped by the capability they stress. Table 3 gives a detailed comparison of a representative subset on year, venue, evaluation mode, and contrast, and Table 4 places one exemplar per lane against a common set of capability dimensions; neither lane’s exemplar builds the VLA-versus-world-model contrast that Section 4 isolates. 

Table 3. **Detailed comparison of a representative 31 of the 160 benchmarks** in the landscape (Table 10), grouped by evaluation lane. **Eval** : open open-loop prediction/generation quality, closed closed-loop task success, bridge prediction-to-action bridge. **VLA vs WM** : ✔ native direct-policy vs world-model contrast, **~** partial, **--** model-agnostic. Venues are web-verified; “arXiv” marks preprint-only works. 

|**Benchmark**|**Year**|**Venue**|**Eval**|**Capability**|**VLA vs WM**|
|---|---|---|---|---|---|
|**§3.1 Policy / manipulation suites**|||||closed|
|**CALVIN**[101]|2021|RA-L|closed|long-horizon language|**--**|
|**LIBERO**[91]|2023|NeurIPS D&B|closed|short-horizon + transfer|**--**|
|**Meta-World**[152]|2020|CoRL|closed|multi-task / meta-RL|**--**|


Jena et al. 

8 

_Table 3 (continued)_ 

|**Benchmark**|**Year**|**Venue**|**Eval**|**Capability**|**VLA vs WM**|
|---|---|---|---|---|---|
|**ManiSkill2**[59]|2023|ICLR|closed|generalizable skills|**--**|
|**SIMPLER**[88]|2024|CoRL|closed|generalization (real vs sim)|**--**|
|**THE COLOSSEUM**[113]|2024|RSS|closed|generalization / robustness|**--**|
|**RoboCasa**[105]|2024|RSS|closed|long-horizon (data scaling)|**--**|
|**RoboArena**[4]|2025|CoRL|closed|real-world generalization|**--**|
|**GemBench**[54]|2024|ICRA|closed|generalization levels|**--**|
|**VLABench**[160]|2025|ICCV|closed|long-horizon reasoning|**--**|
|**§3.2 Embodied navigation, p**|**lanning &**|**social**|||closed|
|**Habitat 3.0**[112]|2023|ICLR|closed|social / multi-agent|**--**|
|**BEHAVIOR-1K**[85]|2024|CoRL|closed|long-horizon household|**--**|
|**ALFRED**[128]|2019|CVPR|closed|long-horizon, partial-obs|**--**|
|**TEACh**[107]|2021|AAAI|closed|hidden-state (dialog)|**--**|
|**RoboTHOR**[38]|2020|CVPR|closed|navigation / sim-to-real|**--**|
|**SocNavBench**[14]|2021|ACM THRI|closed|social navigation|**--**|
|**LIBERO-Mem**[36]|2025|AAAI|closed|hidden-state / occlusion|✔|
|**VIMA-Bench**[75]|2023|ICML|closed|multimodal-prompt generalization|**--**|
|**§3.3 World-model & video-g**|**eneration**|**evaluation**|||open|
|**WorldModelBench**[86]|2025|arXiv|open|video-WM prediction quality|**--**|
|**Physics-IQ**[103]|2025|WACV|open|physical realism|**--**|
|**VBench-2.0**[161]|2025|arXiv|open|generation faithfulness|**--**|
|**WorldScore**[41]|2025|ICCV|open|world-gen quality|**--**|
|**EWMBench**[67]|2025|arXiv|open|scene/motion/semantic quality|**--**|
|**EVA-Bench**[33]|2024|ICML|open|embodied video anticipation|**--**|
|**WorldPrediction**[25]|2025|arXiv|open|counterfactual action recognition|**--**|
|**Physion**[12]|2021|NeurIPS D&B|open|physical prediction from vision|**--**|
|**Physion++**[138]|2023|NeurIPS D&B|open|physical prediction with online property<br>inference|**--**|
|**§3.4 Bridges (prediction to a**|**ction)**||||bridge|
|**WorldSimBench**[115]|2024|ICML|bridge|video-to-action consistency|**~**|
|**World-in-World**[157]|2025|ICLR|bridge|closed-loop task success of WMs|**~**|
|**RoboWM-Bench**[73]|2026|arXiv|bridge|prediction executability|**~**|
|**WorldArena**[124]|2026|arXiv|bridge|closed-loop WM arena|**~**|


The two galleries make the corpus concrete. Figure 8 collects the benchmarks’ own _subject_ figures, the task and scene images that show what each benchmark depicts, grouped by lane rather than by embodiment. Figure 9 collects the _results_ figures, the leaderboards, radar plots, and distributions that show what each benchmark reports. Every panel links to its source paper and is provenance-tracked (Tables 11, 12); benchmarks with no locatable figure are omitted, not fabricated. 

## **3.1 Policy suites** 

The policy lane (37 benchmarks) scores a policy by executing it and counting task success. Its sub-families run from singleand dual-arm _manipulation_ (§3.1.1: ARNOLD [56], PerAct [127], FMB [94], ManiSkill2 [59]), through _generalization_ 

Do World Models Make Better Robots? 

9 


Fig. 6. **The world-model-evaluation wave is recent.** Per-year counts of closed-loop task-success benchmarks (green) and openloop world-model / video-generation benchmarks (magenta) in the catalogue. Closed-loop suites dominate through 2024; in **2025 open-loop evaluation overtakes them** (13 vs 6) as the world-model-generation literature arrives. The four prediction-to-action bridges are newer still, all appearing in 2024 or later. Years are the benchmarks’ first-release years (2026 is partial and omitted); counts are the tallies of Table 10. 

|**Dimension**|**LIBERO**[91]<br>_policy suite_|**Habitat 3.0**[112]<br>_embodied nav_|**WorldModel-**<br>**Bench**[86]<br>_world-model eval_|**World-in-**<br>**World**[157]<br>_bridge_|
|---|---|---|---|---|
|What it scores|task success|social-nav success|video-pred. quality|closed-loop WM<br>success|
|Evaluation mode|closed|closed|open|bridge|
|Executes actions in a loop?|✔|✔|✘|✔|
|Native VLA-vs-WM contrast?|✘|✘|✘|**~**|
|Capability stressed|short-horizon +<br>transfer|social / multi-agent|physical realism|plan executability|
|Per-capability slicing?|**~**|**~**|✘|✘|
|Advantage-of-prediction metric?|✘|✘|✘|**~**|
|Real / sim / video|sim|sim|video|sim|
|Counterfactual probing?|✘|✘|✘|✘|
|Reusable leaderboard?|✔|✔|✔|**~**|


Table 4. Capability matrix, one representative benchmark per evaluation lane. No lane’s exemplar builds a native VLA-vs-world-model contrast: policy and embodied suites are model-agnostic (they _host_ any policy), world-model suites score generation quality with no action, and the bridge exemplar reaches closed-loop success but reports only a partial contrast (“visual quality is not task success”). Counterfactual probing is absent throughout. ✔ yes, **~** partial, ✘ no, **--** n/a; open open-loop, closed closed-loop, bridge bridge. 

suites that vary objects, scenes, and sim-to-real gaps (§3.1.2: LIBERO [91], THE COLOSSEUM [113], SIMPLER [88], VIMA-Bench [75]), to _dexterous_ hands (§3.1.4: Bi-DexHands [28], DexArt [9], UniDexGrasp [146]). These suites are the backbone of policy evaluation, and they are deliberately model-agnostic: they host whatever policy a user brings and are careful not to privilege one architecture. That neutrality is exactly why they cannot, on their own, answer whether 

Jena et al. 

10 


Fig. 7. **A taxonomy of robot-evaluation benchmarks for predictive embodied intelligence** (86 representative benchmarks of the 160 in Table 10). Each sub-family is one cell listing its benchmarks, each with a short statement of what it measures. Benchmarks are grouped by evaluation lane (§3.1–§3.4) and then by the capability they stress. The lanes run from closed-loop task-success suites to the _bridge_ frontier (shaded), the only lane that turns prediction into executed action, which is the survey’s novelty axis. Full per-benchmark detail: Tables 3, 10. 

Do World Models Make Better Robots? 

11 


Fig. 8. **Benchmarks across the surveyed corpus.** Representative subject figures from the catalogue, grouped by evaluation lane rather than embodiment: _closed-loop_ task-success suites, _open-loop_ world-model and video-generation evaluation, and the _prediction-to-action bridges_ . Each panel is a live hyperlink to the source paper on arXiv and is annotated with its arXiv id (per-panel figure provenance in Table 11); the figure is vector with photographs embedded at full resolution, so it can be zoomed without pixelation. Only figures that depict the benchmark’s task or scene are shown; results and leaderboard figures appear in Figure 9. Benchmarks with no locatable subject figure are omitted, not fabricated. Images © their respective authors, reproduced for scholarly review. 

Jena et al. 

12 

a world-model policy beats a direct one. Table 5 audits, capability by capability, which benchmarks come closest to building such a contrast, and finds the lane almost entirely agnostic. 

Table 5. **Capability deep-dive** : the benchmarks that probe each of the _𝛽_ capability cuts, and whether each builds a native VLA-vsworld-model contrast. Native contrasts cluster in the hidden-state, theory-of-mind and counterfactual _reasoning_ cuts (LIBERO-Mem, ComPhy, AGENT, BIB, ACRE, CoPhy, CausalWorld); the long-horizon and social _task-success_ cuts are largely model-agnostic (ALFWorld’s abstract-to-grounded transfer is the lone partial). **Eval** : open/closed. **VLA vs WM** : ✔ native contrast, **~** partial, **--** model-agnostic; each cut’s header tallies the fraction of its benchmarks that build any (native or partial) contrast. 

|**Benchmark**|**Year**|**Eval**|**What it probes**|**VLA vs WM**|
|---|---|---|---|---|
|**Hidden-state / memory / occlusion**||||_3/4_|
|**LIBERO-Mem**[36]|2025|closed|occluded object state carried across time|✔|
|**TEACh**[107]|2021|closed|partner belief and history via dialog|**--**|
|**ComPhy**[29]|2022|open|hidden mass and charge inferred from collisions|✔|
|**Bongard-HOI**[74]|2022|open|few-shot hidden-concept induction|**~**|
|**Theory-of-mind**||||_3/4_|
|**AGENT**[130]|2021|open|expectations over an agent’s goals and actions|✔|
|**BIB**[48]|2021|open|infant-style goal inference from behaviour|✔|
|**PHASE**[106]|2021|closed|social relations and goals inferred from motion|**~**|
|**SocialAI**[78]|2021|closed|language-based social interaction with agents|**--**|
|**Counterfactual / physical inference**||||_3/6_|
|**WorldPrediction**[25]|2025|open|discriminate correct vs counterfactual action|**--**|
|**Physion**[12]|2021|open|predict a physical outcome from vision|**--**|
|**Physion++**[138]|2023|open|infer latent physical properties online|**--**|
|**ACRE**[155]|2021|open|abstract causal reasoning over blicket tests|✔|
|**CoPhy**[10]|2019|open|counterfactual outcome under a changed cause|✔|
|**CausalWorld**[1]|2020|closed|causal do-interventions on task variables|✔|
|**Long-horizon / compositional**||||_1/6_|
|**CALVIN**[101]|2021|closed|chain several language subtasks in a row|**--**|
|**BEHAVIOR-1K**[85]|2024|closed|1000 long-horizon household activities|**--**|
|**ALFRED**[128]|2019|closed|instruction to action under partial view|**--**|
|**ALFWorld**[129]|2020|closed|abstract-text to grounded-task transfer|**~**|
|**EmbodiedBench**[147]|2025|closed|broad long-horizon embodied planning|**--**|
|**PARTNR**[21]|2024|closed|human-robot collaborative household tasks|**--**|
|**Social / multi-agent**||||_0/5_|
|**Habitat 3.0**[112]|2023|closed|human-robot co-habitation and hand-off|**--**|
|**SocNavBench**[14]|2021|closed|socially compliant navigation|**--**|
|**Melting Pot**[84]|2021|closed|mixed-motive multi-agent generalization|**--**|
|**SMAC**[120]|2019|closed|cooperative multi-agent micro-control|**--**|
|**CrowdNav**[24]|2018|closed|socially-aware navigation among pedestrians|**--**|


## **3.2 Embodied agents** 

The embodied-agent lane is the largest (85 benchmarks) and the most diverse. It spans _long-horizon_ household and planning tasks (§3.2.1: ALFRED [128], BEHAVIOR-1K [85], EmbodiedBench [147]), _social and multi-agent_ settings (§3.2.2: Habitat 3.0 [112], Overcooked-AI [19], Melting Pot [84]), _navigation_ (§3.2.3: Habitat [121], HM3D [117], GOATBench [77]), _autonomous driving_ (§3.2.4: CARLA [40], Bench2Drive [72], Waymax [60]), _counterfactual_ reasoning (§3.2.5: 

Do World Models Make Better Robots? 

13 

CausalWorld [1], CoPhy [10], ACRE [155]), and _locomotion_ (§3.2.6: HumanoidBench [123], Barkour [18], Isaac Gym [97]). Two observations matter for the survey’s question. First, like the policy lane, these suites are overwhelmingly modelagnostic. Second, the counterfactual sub-family, which is where predictive world modelling should most plausibly help, is the thinnest: it is populated by causal-reasoning tasks but almost never run as a closed-loop VLA-versus-world-model contrast. 

## **3.3 World-model evaluation** 

The world-model-evaluation lane (34 benchmarks) scores prediction and generation directly, with no action taken. Its sub-families are _generation quality_ (§3.3.1: VBench [68], EvalCrafter [92], EWMBench [67], EVA-Bench [33]), _physical reasoning_ (§3.3.2: IntPhys [118], PhysBench [35], PhyGenBench [102], Physics-IQ [103]), _counterfactual_ video reasoning (§3.3.3: CLEVRER [150], WorldPrediction [25]), and a driving world model (§3.3.4: Vista [52]). Table 6 is a deep-dive over all 34: it records what each scores (generation, question-answering, or prediction), the signal it uses (automatic metric, accuracy, violation-of-expectation, or human rating), and whether it touches physical grounding. The lane’s defining limitation is uniform: every benchmark scores open-loop, and none executes what it predicts, so a high generation score certifies visual quality but says nothing about task success. 

Table 6. **World-model-evaluation deep-dive** : the 34 benchmarks of the world-model-evaluation lane, by sub-type – the P3 counterpart of the skill-building branch deep-dive. **Mode** : Gen evaluates generated video, QA video question-answering, Pred physical prediction. **Signal** : Auto computed/learned metric, Acc accuracy vs ground truth, VOE violation-of-expectation, Human human study. **Physical** : targets physical-law understanding, ✔ core, **~** adjacent, ✘ general. Generation-quality suites dominate and are physics-agnostic; only the physical-reasoning and physical-commonsense sub-types test physical law, and every lane benchmark scores open-loop, never in a closed loop. 

|**Benchmark**|**Year**|**Mode**|**What it scores**|**Signal**|**Physical**|
|---|---|---|---|---|---|
|**Generation quality (multi-dimens**|**ional)**|||||
|**EvalCrafter**[92]|2023|Gen|17-metric text-to-video quality suite|Auto|✘|
|**FETV**[93]|2023|Gen|fine-grained text-to-video quality|Auto|✘|
|**VBench**[68]|2023|Gen|16 disentangled generation dimensions|Auto|✘|
|**StoryBench**[16]|2023|Gen|continuous story-visualisation quality|Auto|✘|
|**DEVIL**[89]|2024|Gen|content-dynamics quality of T2V|Auto|✘|
|**T2V-CompBench**[134]|2024|Gen|compositional text-to-video quality|Auto|✘|
|**T2VScore**[144]|2024|Gen|learned alignment + quality metric|Auto|✘|
|**TC-Bench**[44]|2024|Gen|temporal compositionality in generation|Auto|✘|
|**VideoScore**[63]|2024|Gen|learned automatic quality metric|Auto|✘|
|**EWMBench**[67]|2025|Gen|scene / motion / semantic quality|Auto|✘|
|**VBench-2.0**[161]|2025|Gen|generation faithfulness|Auto|✘|
|**Intuitive & physical reasoning**||||||
|**IntPhys**[118]|2018|Pred|intuitive physics from video|VOE|✔|
|**Physion**[12]|2021|Pred|physical outcome prediction from vision|Acc|✔|
|**GRASP**[71]|2023|QA|intuitive physics in video MLLMs|Acc|✔|
|**Physion++**[138]|2023|Pred|prediction with online property inference|Acc|✔|
|**ContPhy**[163]|2024|QA|soft-body / fluid physical reasoning|Acc|✔|
|**Physics-IQ**[103]|2025|Gen|physical realism of generated video|Auto|✔|
|**PhysBench**[35]|2025|QA|physical-world understanding for VLMs|Acc|✔|
|**PHYBench**[116]|2025|QA|physical perception and reasoning|Acc|✔|
|**IntPhys 2**[15]|2025|Pred|intuitive physics in complex scenes|VOE|✔|
|**Physical commonsense in generat**|**ed video**|||||
|**PhyGenBench**[102]|2024|Gen|physical-commonsense correctness in gen|Auto|✔|


Jena et al. 

14 

_Table 6 (continued)_ 

|**Benchmark**|**Year**|**Mode**|**What it scores**|**Signal**|**Physical**|
|---|---|---|---|---|---|
|**VideoPhy**[7]|2024|Gen|physical commonsense in generated video|Human|✔|
|**VideoPhy-2**[8]|2025|Gen|action-centric physical commonsense|Human|✔|
|**PhyWorldBench**[58]|2025|Gen|physical realism in text-to-video|Human|✔|
|**IPV-Bench**[5]|2025|Gen|impossible-video generation + understanding|Acc|✔|
|**Counterfactual / causal / temporal**||||||
|**CATER**[55]|2019|QA|compositional-action temporal reasoning|Acc|✘|
|**CLEVRER**[150]|2019|QA|causal / counterfactual video reasoning|Acc|**~**|
|**WorldPrediction**[25]|2025|QA|counterfactual action recognition|Acc|✘|
|**Video-language alignment / halluci**|**nation**|||||
|**VideoCon**[6]|2023|QA|robust video-language alignment|Auto|✘|
|**VideoHallucer**[141]|2024|QA|hallucination in video-language models|Acc|✘|
|**World-model prediction & world ge**|**neratio**|**n**||||
|**Vista**[52]|2024|Gen|driving world-model generation|Auto|**~**|
|**EVA-Bench**[33]|2024|Pred|embodied video anticipation|Auto|**~**|
|**WorldModelBench**[86]|2025|Gen|video world-model prediction quality|Human|**~**|
|**WorldScore**[41]|2025|Gen|controllable world-generation quality|Auto|✘|


## **3.4 Prediction-to-action bridges** 

The bridge lane is the frontier, and it is tiny: four benchmarks. RoboWM-Bench [73] tests whether a world model’s predictions are _executable_ ; World-in-World [157] and WorldArena [124] place world models in a closed loop and score task success rather than rollout realism; WorldSimBench [115] scores generative models both as renderers and as controllable simulators. These are the only benchmarks that carry prediction all the way into executed action, and they are the shaded frontier of Figure 7. Even so, none of the four yet reports a per-capability, head-to-head comparison between a direct VLA policy and a world-model policy under one protocol. The bridges prove the loop can be closed; they do not yet close it in a way that isolates the advantage of prediction. That is the gap Section 4 formalises. 

Do World Models Make Better Robots? 

15 


Fig. 9. **Results reported across the surveyed corpus.** Representative results figures from the catalogue, grouped by type of evidence: _leaderboard and model-comparison charts_ , _per-dimension radar and multi-metric_ plots, and _distributions and composition_ . Each panel is a live hyperlink to the source paper on arXiv and is annotated with its arXiv id (per-panel provenance in Table 12); the figure is vector with plots embedded at full resolution. Only results/leaderboard/metric figures are shown; task and scene figures appear in Figure 8. As a benchmark survey the reported evidence is dominated by rankings, radars and distributions rather than training curves, and is sparser than the subject figures, so this gallery is smaller; benchmarks that publish no results figure are omitted, not fabricated. A benchmark may appear more than once when it reports several evidence types. Images © their respective authors, reproduced for scholarly review. 

Jena et al. 

16 

## **4 Does prediction help acting? The contrast gap** 

The survey’s question can be stated precisely. Let a _direct policy_ map observations to actions, and let a _world-model policy_ first predict future observations and then plan an action against that prediction. The advantage of prediction is the closed-loop task-success _gain_ of the world-model policy over a matched direct policy, and it is only meaningful when reported per capability, since prediction should help more where hidden state, occlusion, or long horizons make foresight valuable. Figure 10 draws the evaluation loop this definition requires: a task forks into a direct-VLA branch and a world-model branch, both run in one closed loop with state feedback, both scored by the same task-success measure, and the difference read off per capability. 

Today’s benchmarks break this loop in one of two ways, visible as the two poles of Figure 1. Model-agnostic policy and embodied suites (Sections 3.1, 3.2) close the loop but run a single branch, so there is no contrast to read. Worldmodel-evaluation suites (Section 3.3) score the prediction branch open-loop and never execute it, so a high score certifies generation quality, not task success. The prediction-to-action bridges (Section 3.4) close the loop for a world-model policy but do not yet run the matched VLA branch per capability. No lane completes the diagram. 

## **4.1 “World model” is three things, none of them sufficient alone** 

Part of why the contrast is hard to build is that the term “world model” is overloaded. Table 7 separates two axes the literature routinely conflates. Along a _representation_ axis a world model may be a latent-dynamics predictor (LWM; DreamerV3, TD-MPC2), an action-conditioned future-frame predictor (WAM; iVideoGPT, GR-2), or a generative video model (WFM; Sora, Cosmos, Genie). Along a _role_ axis it may be a neural simulator that trains or evaluates a policy, or the object that a benchmark scores. The crucial fact is that no single sense is simultaneously action-conditioned, run in a closed loop, and readily comparable to a VLA policy under one protocol: latent and action-conditioned models act but are rarely scored by a standard generation metric, while generative models carry the metrics but are rarely closed into a loop. A benchmark that contrasts a world-model policy with a VLA policy therefore has to assemble properties that no existing sense of the term supplies at once. 

## **4.2 Why each lane leaves the contrast unbuilt** 

Table 8 compares the four lanes on six evaluation axes and makes the pattern lane-by-lane. Policy and embodied suites score the right quantity, closed-loop success, on the right capabilities, but hold the model family fixed and so never contrast it. World-model-evaluation suites vary the model family richly but score the wrong quantity for our question, open-loop prediction quality, and never close the loop. The bridges are the only lane that scores closed-loop success of a world model, but they are four benchmarks and none slices a VLA head-to-head by capability. The result is a coverage hole precisely where the survey’s question lives: the intersection of closed-loop scoring, per-capability slicing, and a world-model-versus-VLA family contrast. 

## **4.3 Measuring the advantage: assessed, not adopted** 

Closing the loop is necessary but not sufficient; the gain also needs an instrument. Proposals exist, including behavioural advantage-of-prediction scores such as ACTION-ATLAS’s World Advantage Score, but they are put forward in position papers [153] rather than established across a benchmark suite. We therefore _assess_ such instruments as candidates rather than adopting any one as ground truth, and Section 5 specifies how an advantage-of-prediction quantity should be reported: as a per-capability distribution or curve against a matched baseline, never as a single headline number. The 

Do World Models Make Better Robots? 

17 


Fig. 10. **The evaluation loop that isolates the advantage of prediction.** A benchmark that can answer “does world modelling help a robot act” must run a direct Vision-Language-Action policy _and_ a world-model policy (predict then plan) under one closed loop, then report the closed-loop gain ( _𝛿_ ) sliced by capability ( _𝛽_ ). Today’s suites break this loop in one of two ways: model-agnostic policy suites host a single policy and never build the contrast, while world-model suites score the prediction open-loop and never execute it (§4). 

empirical scale of the gap is worth restating: of 160 benchmarks, 138 are model-agnostic, 11 build a partial contrast, and 11 build an explicit one; counterfactual capability, where foresight should matter most, is almost entirely unmeasured; and only four benchmarks reach executed action at all. 

Jena et al. 

18 

|**Sense**<br>**of**<br>**“world**<br>**model”**|**What it is**|**Examples**|**Act. cond.**|**Loop**|**Metric**|**VLA-cmp.**|
|---|---|---|---|---|---|---|
|_As a representation (what_|_the model is)_||||||
|latent WM (LWM)|latent-dynamics predictor_𝑧𝑡_+1 =<br>_𝑓_(_𝑧𝑡,𝑎𝑡_)|DreamerV3, TD-MPC2|✔|✔|**~**|**~**|
|action-cond.<br>WM<br>(WAM)|action-conditioned<br>future-frame<br>predictor|iVideoGPT, GR-2|✔|**~**|**~**|**~**|
|generative WM (WFM)|text / image-to-video generator|Sora, Cosmos, Genie|**~**|✘|✔|✘|
|_As a role (what the model_|_is used for)_||||||
|neural simulator|learned environment for policy<br>training / eval|UniSim|✔|✔|**~**|**~**|
|evaluation target|benchmarks that_score_world mod-<br>els|WorldSimBench,<br>World-<br>ModelBench, EWMBench|**--**|**~**|✔|✘|


Table 7. The term “world model” spans two orthogonal axes the literature routinely conflates: a _representation_ axis (what the model is: latent-state dynamics, action-conditioned video, or generative video, a soft boundary since action-conditioned generators straddle WAM and WFM) and a _role_ axis (what it is used for: a neural simulator, or the object a benchmark scores). Columns record whether a sense is **act** ion- **cond** itioned, is used in a closed **loop** , carries a standard evaluation **metric** , and is readily **VLA-comp** arable under one protocol (✔ yes, **~** partial, ✘ no, **--** n/a). No single sense is action-conditioned, closed-loop, and VLA-comparable at once, which is why a benchmark that contrasts a world-model policy with a VLA policy per capability (§4) is still missing. Evaluation benchmarks score the world model as an _object_ ; they are not world models acting as judges. 

||**Policy suites**[91]|**Embodied nav / social**[112]|**World-model eval**[86]|**Bridges**[157]|
|---|---|---|---|---|
|**Loop closure**|✔closed-loop; steps the<br>environment [101]|✔closed-loop; long-horizon<br>rollouts [85]|✘open-loop; scores generation, no<br>action [103]|**~**converts a prediction into an<br>executed action [115]|
|**Task horizon**|**~**short reactive skills; long by<br>chaining [91]|✔long-horizon household and<br>dialog [107]|**~**short clips; temporal but not<br>task-level [67]|**~**a single executed rollout [73]|
|**Capability breadth**|**~**manipulation + transfer;<br>hidden-state rare [113]|✔navigation, social, some<br>hidden-state [38]|**~**physical / temporal;<br>counterfactual barely [25]|✘narrow; executability only [124]|
|**Model-family**<br>**contrast**|✘model-agnostic host of any<br>policy [4]|**~**memory-vs-Markovian in one<br>suite [36]|✘world-model-only scores [86]|**~**WM as policy substrate; no VLA<br>pole [157]|
|**Reproducibility**|**~**sim; some real-vs-sim<br>transfer [88]|**~**sim-heavy; a sim-to-real gap [38]|✔fixed offline sets; deterministic<br>scoring [161]|✘new, still-unstandardised<br>protocols [124]|
|**Structural blind spot**|hosts a world-model policy but<br>never builds the VLA contrast|capability cuts exist, but no<br>per-capability family ablation|visual quality is not task success;<br>no behavioural utility|reaches action, but omits the<br>per-capability VLA head-to-head|


Table 8. **Evaluation-lane comparison matrix** : the four benchmark lanes on six evaluation axes (loop closure, task horizon, capability breadth, model-family contrast, reproducibility, and characteristic blind spot). Marks grade each lane on the axis (✔ favourable, **~** mixed, ✘ weak), with an anchoring benchmark per cell. No lane closes the loop, slices capability, _and_ builds a native VLA-vs-worldmodel contrast at once; the bridge lane comes closest yet still omits the per-capability VLA head-to-head, which is the empty cell this survey names (§4). 

## **5 An agenda for advantage-aware evaluation** 

If the gap is that no benchmark is built to ask whether prediction helps acting, the remedy is a small, measurable protocol that any benchmark could adopt. Table 9 sets out four quantities, each with a definition, a concrete testbed, and the axis it stresses, and Figure 11 sketches how they compose. The figure shows target shapes, not measured results: it is a protocol, not a leaderboard. 

The first quantity is an _advantage-of-prediction curve_ : the closed-loop success gain of a world-model policy over a matched direct-VLA baseline, reported per capability as a curve rather than a single endpoint, instantiated over LIBERO [91] and CALVIN [101] run under one harness. The second is _counterfactual accuracy_ : task success on episodes 

Do World Models Make Better Robots? 

19 

|**Metric**|**Definition**|**Instantiation (testbed)**|**Axis stressed**|
|---|---|---|---|
|Advantage-of-prediction<br>curve|closed-loop success_gain_of a predictive policy<br>over a matched direct-VLA baseline, reported<br>per capability as a curve, not a single endpoint|a<br>capability-sliced<br>protocol<br>over<br>LIBERO [91] and CALVIN [101] that runs<br>a world-model policy and a VLA policy<br>under one harness|_𝛾_family,_𝛿_metric|
|Counterfactual accuracy|task success on episodes that require inference<br>over unobserved or hypothetical dynamics (oc-<br>clusion, object permanence, “what if”)|WorldPrediction [25] plus occlusion /<br>memory splits in the style of LIBERO-<br>Mem [36]|_𝛽_capability|
|Prediction-to-action fidelity<br>gap|the difference between a world model’s open-<br>loop generation quality and its closed-loop<br>task success (“visual quality is not task suc-<br>cess”)|bridge protocols such as WorldSim-<br>Bench [115] and World-in-World [157]|_𝛼_mode|
|Per-capability contrast cover-<br>age|the fraction of capabilities for which a bench-<br>mark actually runs a VLA-vs-world-model<br>head-to-head under a single protocol|audits of the landscape (Table 10) against<br>a declared contrast schema|_𝛾_family,_𝜀_catalog|


Table 9. **An actionable protocol for the future agenda** : four measurable quantities, their definitions, and concrete testbeds. The first anchors the advantage-of-prediction question ( _𝛿_ ) on LIBERO / CALVIN-style suites; the second targets the near-unmeasured counterfactual capability; the third quantifies the prediction-to-action gap the bridges expose; the fourth audits per-capability contrast coverage across the landscape. Each is reported as a distribution or curve, never a single headline number. 

that require reasoning over unobserved or hypothetical dynamics, built from WorldPrediction [25] together with occlusion and memory splits in the style of LIBERO-Mem [36]; this targets the capability the corpus most neglects. The third is the _prediction-to-action fidelity gap_ : the difference between a world model’s open-loop generation quality and its closed-loop task success, measured on bridge protocols such as WorldSimBench [115] and World-in-World [157], which quantifies directly the “visual quality is not task success” warning of Section 4. The fourth is _per-capability contrast coverage_ : the fraction of capabilities for which a benchmark actually runs a VLA-versus-world-model head-to-head, computed by auditing the landscape (Table 10) against a declared contrast schema. Each is reported as a distribution or a curve, never as one number, so that “prediction helps” can be replaced by “prediction helps _here_ , by _this much_ ”. 

Jena et al. 

20 


Fig. 11. **An actionable evaluation protocol for the future agenda** (Table 9). The panels are _schematic_ : they show the axes and the _target_ shape of each measurement, not measured results. (a) a world-model policy should beat a matched direct-VLA baseline in closed-loop success, and the per-capability gap is the advantage of prediction ( _𝛿_ ), on LIBERO / CALVIN-style suites run with both families; (b) counterfactual accuracy is near chance today and should rise, on WorldPrediction and occlusion splits; (c) a world model’s open-loop quality far exceeds its closed-loop task success, and that gap must be reported, on bridge suites; (d) the fraction of capabilities with a native VLA-vs-world-model contrast is far below target across the landscape. 

## **6 Limitations** 

Three limits bound the survey’s claims. First, its unit is the benchmark, not the model: the corpus maps how the field _measures_ predictive embodied intelligence and deliberately says nothing about which world models or VLA policies are strongest. A reader looking for a model ranking will not find one here, by design. Second, the contrast axis rests on an operational definition (Table 2): a benchmark counts as building a VLA-versus-world-model contrast only when both branches are run under one protocol. A more permissive reading would move some benchmarks from model-agnostic to partial, though the qualitative picture, that explicit contrasts are rare and counterfactual coverage is thin, is robust to the exact threshold. Third, coverage is biased towards recent, arXiv-indexed, English-language work reachable by web search; the funnel in Figure 3 records only logged stages, and the two galleries include only benchmarks whose figures could be located and provenance-checked, so absence from a gallery is not evidence of absence of results. Finally, the advantage-of-prediction instruments discussed in Section 4 are assessed as candidates rather than adopted; we do not rank benchmarks by any metric that the field has not yet validated. 

Do World Models Make Better Robots? 

21 

## **7 Conclusion** 

Do world models make better robots? On the evidence of the benchmarks the field has built, the honest answer is that we cannot yet tell. The question asks for a closed-loop, per-capability comparison between a world-model policy and a direct VLA policy, and our catalogue of 160 web-verified benchmarks shows that almost none is built to run it: 138 of 160 are model-agnostic, only 11 build an explicit contrast, counterfactual capability is nearly unmeasured, and only four benchmarks carry prediction into executed action. The obstacle is methodological. World-model suites score prediction without executing it, task-success suites execute a single policy without contrasting families, and the term “world model” itself names three different objects, none of which is action-conditioned, closed-loop, and VLA-comparable at once. 

This survey’s contribution is to make that gap precise and measurable. We give an operational taxonomy of the landscape across four evaluation lanes, a coverage comparison showing that no prior survey crosses capability with model family, an evaluation loop that isolates the advantage of prediction, and a four-metric protocol, anchored on named testbeds, that any benchmark could adopt to report where and by how much prediction helps. The next benchmark that matters will not be the one with the most tasks or the most realistic renders; it will be the one that runs both branches in one loop and reads off the difference. Building it is the empty cell this survey names. 

Jena et al. 

22 

## **References** 

- [1] Ossama Ahmed, Frederik Trauble, Anirudh Goyal, Alexander Neitz, Yoshua Bengio, Bernhard Scholkopf, Manuel Wuthrich, and Stefan Bauer. 2020. CausalWorld: A Robotic Manipulation Benchmark for Causal Structure and Transfer Learning. arXiv:2010.04296. 

- [2] Peter Anderson, Qi Wu, Damien Teney, Jake Bruce, Mark Johnson, Niko Sunderhauf, Ian Reid, Stephen Gould, and Anton van den Hengel. 2017. Vision-and-Language Navigation: Interpreting visually-grounded navigation instructions in real environments. arXiv:1711.07280. 

- [3] Tayfun Ates, M. Samil Atesoglu, Cagatay Yigit, Ilker Kesen, Mert Kobas, Erkut Erdem, Aykut Erdem, Tilbe Goksun, and Deniz Yuret. 2020. CRAFT: A Benchmark for Causal Reasoning About Forces and inTeractions. arXiv:2012.04293. 

- [4] Pranav Atreya, Karl Pertsch, Tony Lee, Moo Jin Kim, Arhan Jain, Artur Kuramshin, Clemens Eppner, Cyrus Neary, Edward Hu, Fabio Ramos, Jonathan Tremblay, Kanav Arora, Kirsty Ellis, Luca Macesanu, Marcel Torne Villasevil, Matthew Leonard, Meedeum Cho, Ozgur Aslan, Shivin Dass, Jie Wang, William Reger, Xingfang Yuan, Xuning Yang, Abhishek Gupta, Dinesh Jayaraman, Glen Berseth, Kostas Daniilidis, Roberto Martin-Martin, Youngwoon Lee, Percy Liang, Chelsea Finn, and Sergey Levine. 2025. RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies. arXiv:2506.18123. 

- [5] Zechen Bai, Hai Ci, and Mike Zheng Shou. 2025. Impossible Videos. arXiv:2503.14378. 

- [6] Hritik Bansal, Yonatan Bitton, Idan Szpektor, Kai-Wei Chang, and Aditya Grover. 2023. VideoCon: Robust Video-Language Alignment via Contrast Captions. arXiv:2311.10111. 

- [7] Hritik Bansal, Zongyu Lin, Tianyi Xie, Zeshun Zong, Michal Yarom, Yonatan Bitton, Chenfanfu Jiang, Yizhou Sun, Kai-Wei Chang, and Aditya Grover. 2024. VideoPhy: Evaluating Physical Commonsense for Video Generation. arXiv:2406.03520. 

- [8] Hritik Bansal, Clark Peng, Yonatan Bitton, Roman Goldenberg, Aditya Grover, and Kai-Wei Chang. 2025. VideoPhy-2: A Challenging Action-Centric Physical Commonsense Evaluation in Video Generation. arXiv:2503.06800. 

- [9] Chen Bao, Helin Xu, Yuzhe Qin, and Xiaolong Wang. 2023. DexArt: Benchmarking Generalizable Dexterous Manipulation with Articulated Objects. arXiv:2305.05706. 

- [10] Fabien Baradel, Natalia Neverova, Julien Mille, Greg Mori, and Christian Wolf. 2019. CoPhy: Counterfactual Learning of Physical Dynamics. arXiv:1909.12000. 

- [11] Dhruv Batra, Aaron Gokaslan, Aniruddha Kembhavi, Oleksandr Maksymets, Roozbeh Mottaghi, Manolis Savva, Alexander Toshev, and Erik Wijmans. 2020. ObjectNav Revisited: On Evaluation of Embodied Agents Navigating to Objects. arXiv:2006.13171. 

- [12] Daniel M. Bear, Elias Wang, Damian Mrowca, Felix J. Binder, Hsiao-Yu Fish Tung, R. T. Pramod, Cameron Holdaway, Sirui Tao, Kevin Smith, Fan-Yun Sun, Li Fei-Fei, Nancy Kanwisher, Joshua B. Tenenbaum, Daniel L. K. Yamins, and Judith E. Fan. 2021. Physion: Evaluating Physical Prediction from Vision in Humans and Machines. arXiv:2106.08261. 

- [13] Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. 2023. RoboAgent: Generalization and Efficiency in Robot Manipulation via Semantic Augmentations and Action Chunking. arXiv:2309.01918. 

- [14] Abhijat Biswas, Allan Wang, Gustavo Silvera, Aaron Steinfeld, and Henny Admoni. 2021. SocNavBench: A Grounded Simulation Testing Framework for Evaluating Social Navigation. arXiv:2103.00047. 

- [15] Florian Bordes, Quentin Garrido, Justine T Kao, Adina Williams, Michael Rabbat, and Emmanuel Dupoux. 2025. IntPhys 2: Benchmarking Intuitive Physics Understanding In Complex Synthetic Environments. arXiv:2506.09849. 

- [16] Emanuele Bugliarello, Hernan Moraldo, Ruben Villegas, Mohammad Babaeizadeh, Mohammad Taghi Saffar, Han Zhang, Dumitru Erhan, Vittorio Ferrari, Pieter-Jan Kindermans, and Paul Voigtlaender. 2023. StoryBench: A Multifaceted Benchmark for Continuous Story Visualization. arXiv:2308.11606. 

- [17] Holger Caesar, Varun Bankiti, Alex H. Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. 2019. nuScenes: A multimodal dataset for autonomous driving. arXiv:1903.11027. 

- [18] Ken Caluwaerts, Atil Iscen, J. Chase Kew, Wenhao Yu, Tingnan Zhang, Daniel Freeman, Kuang-Huei Lee, Lisa Lee, Stefano Saliceti, Vincent Zhuang, Nathan Batchelor, Steven Bohez, Federico Casarini, Jose Enrique Chen, Omar Cortes, Erwin Coumans, Adil Dostmohamed, Gabriel Dulac-Arnold, Alejandro Escontrela, Erik Frey, Roland Hafner, Deepali Jain, Bauyrjan Jyenis, Yuheng Kuang, Edward Lee, Linda Luu, Ofir Nachum, Ken Oslund, Jason Powell, Diego Reyes, Francesco Romano, Feresteh Sadeghi, Ron Sloat, Baruch Tabanpour, Daniel Zheng, Michael Neunert, Raia Hadsell, Nicolas Heess, Francesco Nori, Jeff Seto, Carolina Parada, Vikas Sindhwani, Vincent Vanhoucke, and Jie Tan. 2023. Barkour: Benchmarking Animal-level Agility with Quadruped Robots. arXiv:2305.14654. 

- [19] Micah Carroll, Rohin Shah, Mark K. Ho, Thomas L. Griffiths, Sanjit A. Seshia, Pieter Abbeel, and Anca Dragan. 2019. On the Utility of Learning about Humans for Human-AI Coordination. arXiv:1910.05789. 

- [20] Angel Chang, Angela Dai, Thomas Funkhouser, Maciej Halber, Matthias Niessner, Manolis Savva, Shuran Song, Andy Zeng, and Yinda Zhang. 2017. Matterport3D: Learning from RGB-D Data in Indoor Environments. arXiv:1709.06158. 

- [21] Matthew Chang, Gunjan Chhablani, Alexander Clegg, Mikael Dallaire Cote, Ruta Desai, Michal Hlavac, Vladimir Karashchuk, Jacob Krantz, Roozbeh Mottaghi, Priyam Parashar, Siddharth Patki, Ishita Prasad, Xavier Puig, Akshara Rai, Ram Ramrakhya, Daniel Tran, Joanne Truong, John M. Turner, Eric Undersander, and Tsung-Yen Yang. 2024. PARTNR: A Benchmark for Planning and Reasoning in Embodied Multi-agent Tasks. arXiv:2411.00081. 

- [22] Yu-Wei Chao, Chris Paxton, Yu Xiang, Wei Yang, Balakumar Sundaralingam, Tao Chen, Adithyavairavan Murali, Maya Cakmak, and Dieter Fox. 2022. HandoverSim: A Simulation Framework and Benchmark for Human-to-Robot Object Handovers. arXiv:2205.09747. 

Do World Models Make Better Robots? 

23 

- [23] Changan Chen, Unnat Jain, Carl Schissler, Sebastia Vicenc Amengual Gari, Ziad Al-Halah, Vamsi Krishna Ithapu, Philip Robinson, and Kristen Grauman. 2019. SoundSpaces: Audio-Visual Navigation in 3D Environments. arXiv:1912.11474. 

- [24] Changan Chen, Yuejiang Liu, Sven Kreiss, and Alexandre Alahi. 2018. Crowd-Robot Interaction: Crowd-aware Robot Navigation with Attentionbased Deep Reinforcement Learning. arXiv:1809.08835. 

- [25] Delong Chen, Willy Chung, Yejin Bang, Ziwei Ji, and Pascale Fung. 2025. WorldPrediction: A Benchmark for High-level World Modeling and Long-horizon Procedural Planning. arXiv:2506.04363. 

- [26] Howard Chen, Alane Suhr, Dipendra Misra, Noah Snavely, and Yoav Artzi. 2018. Touchdown: Natural Language Navigation and Spatial Reasoning in Visual Street Environments. arXiv:1811.12354. 

- [27] Yi Chen, Yuying Ge, Yixiao Ge, Mingyu Ding, Bohao Li, Rui Wang, Ruifeng Xu, Ying Shan, and Xihui Liu. 2023. EgoPlan-Bench: Benchmarking Multimodal Large Language Models for Human-Level Planning. arXiv:2312.06722. 

- [28] Yuanpei Chen, Tianhao Wu, Shengjie Wang, Xidong Feng, Jiechuang Jiang, Stephen Marcus McAleer, Yiran Geng, Hao Dong, Zongqing Lu, SongChun Zhu, and Yaodong Yang. 2022. Towards Human-Level Bimanual Dexterous Manipulation with Reinforcement Learning. arXiv:2206.08686. 

- [29] Zhenfang Chen, Kexin Yi, Yunzhu Li, Mingyu Ding, Antonio Torralba, Joshua B. Tenenbaum, and Chuang Gan. 2022. ComPhy: Compositional Physical Reasoning of Objects and Events from Videos. arXiv:2205.01089. 

- [30] Zhili Cheng, Yuge Tu, Ran Li, Shiqi Dai, Jinyi Hu, Shengding Hu, Jiahao Li, Yang Shi, Tianyu Yu, Weize Chen, Lei Shi, and Maosong Sun. 2025. EmbodiedEval: Evaluate Multimodal LLMs as Embodied Agents. arXiv:2501.11858. 

- [31] Zhili Cheng, Zhitong Wang, Jinyi Hu, Shengding Hu, An Liu, Yuge Tu, Pengkai Li, Lei Shi, Zhiyuan Liu, and Maosong Sun. 2024. LEGENT: Open Platform for Embodied Agents. arXiv:2404.18243. 

- [32] Nikita Chernyadev, Nicholas Backshall, Xiao Ma, Yunfan Lu, Younggyo Seo, and Stephen James. 2024. BiGym: A Demo-Driven Mobile Bi-Manual Manipulation Benchmark. arXiv:2407.07788. 

- [33] Xiaowei Chi, Chun-Kai Fan, Hengyuan Zhang, Xingqun Qi, Rongyu Zhang, Anthony Chen, Chi min Chan, Wei Xue, Qifeng Liu, Shanghang Zhang, and Yike Guo. 2024. EVA: An Embodied World Model for Future Video Anticipation. arXiv:2410.15461. 

- [34] Jae-Woo Choi, Youngwoo Yoon, Hyobin Ong, Jaehong Kim, and Minsu Jang. 2024. LoTa-Bench: Benchmarking Language-oriented Task Planners for Embodied Agents. arXiv:2402.08178. 

- [35] Wei Chow, Jiageng Mao, Boyi Li, Daniel Seita, Vitor Guizilini, and Yue Wang. 2025. PhysBench: Benchmarking and Enhancing Vision-Language Models for Physical World Understanding. arXiv:2501.16411. 

- [36] Nhat Chung, Taisei Hanyu, Toan Nguyen, Huy Le, Frederick Bumgarner, Duy Minh Ho Nguyen, Khoa Vo, Kashu Yamazaki, Chase Rainwater, Tung Kieu, Anh Nguyen, and Ngan Le. 2025. Rethinking Progression of Memory State in Robotic Manipulation: An Object-Centric Perspective. arXiv:2511.11478. 

- [37] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, Andreas Geiger, and Kashyap Chitta. 2024. NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking. arXiv:2406.15349. 

- [38] Matt Deitke, Winson Han, Alvaro Herrasti, Aniruddha Kembhavi, Eric Kolve, Roozbeh Mottaghi, Jordi Salvador, Dustin Schwenk, Eli VanderBilt, Matthew Wallingford, Luca Weihs, Mark Yatskar, and Ali Farhadi. 2020. RoboTHOR: An Open Simulation-to-Real Embodied AI Platform. arXiv:2004.06799. 

- [39] Matt Deitke, Eli VanderBilt, Alvaro Herrasti, Luca Weihs, Jordi Salvador, Kiana Ehsani, Winson Han, Eric Kolve, Ali Farhadi, Aniruddha Kembhavi, and Roozbeh Mottaghi. 2022. ProcTHOR: Large-Scale Embodied AI Using Procedural Generation. arXiv:2206.06994. 

- [40] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. 2017. CARLA: An Open Urban Driving Simulator. arXiv:1711.03938. 

- [41] Haoyi Duan, Hong-Xing Yu, Sirui Chen, Li Fei-Fei, and Jiajun Wu. 2025. WorldScore: A Unified Evaluation Benchmark for World Generation. arXiv:2504.00983. 

- [42] Jiafei Duan, Samson Yu, Hui Li Tan, Hongyuan Zhu, and Cheston Tan. 2022. A Survey of Embodied AI: From Simulators to Research Tasks. _IEEE Transactions on Emerging Topics in Computational Intelligence_ (2022). arXiv:2103.04918. 

- [43] Mahsa Ehsanpour, Fatemeh Saleh, Silvio Savarese, Ian Reid, and Hamid Rezatofighi. 2021. JRDB-Act: A Large-scale Dataset for Spatio-temporal Action, Social Group and Activity Detection. arXiv:2106.08827. 

- [44] Weixi Feng, Jiachen Li, Michael Saxon, Tsu jui Fu, Wenhu Chen, and William Yang Wang. 2024. TC-Bench: Benchmarking Temporal Compositionality in Text-to-Video and Image-to-Video Generation. arXiv:2406.08656. 

- [45] Aaron Foss, Chloe Evans, Sasha Mitts, Koustuv Sinha, Ammar Rizvi, and Justine T. Kao. 2025. CausalVQA: A Physically Grounded Causal Reasoning Benchmark for Video Models. arXiv:2506.09943. 

- [46] C. Daniel Freeman, Erik Frey, Anton Raichuk, Sertan Girgin, Igor Mordatch, and Olivier Bachem. 2021. Brax – A Differentiable Physics Engine for Large Scale Rigid Body Simulation. arXiv:2106.13281. 

- [47] Chuang Gan, Siyuan Zhou, Jeremy Schwartz, Seth Alter, Abhishek Bhandwaldar, Dan Gutfreund, Daniel L. K. Yamins, James J DiCarlo, Josh McDermott, Antonio Torralba, and Joshua B. Tenenbaum. 2021. The ThreeDWorld Transport Challenge: A Visually Guided Task-and-Motion Planning Benchmark for Physically Realistic Embodied AI. arXiv:2103.14025. 

- [48] Kanishk Gandhi, Gala Stojnic, Brenden M. Lake, and Moira R. Dillon. 2021. Baby Intuitions Benchmark (BIB): Discerning the goals, preferences, and actions of others. arXiv:2102.11938. 

Jena et al. 

24 

- [49] Chen Gao, Baining Zhao, Weichen Zhang, Jinzhu Mao, Jun Zhang, Zhiheng Zheng, Fanhang Man, Jianjie Fang, Zile Zhou, Jinqiang Cui, Xinlei Chen, and Yong Li. 2024. EmbodiedCity: A Benchmark Platform for Embodied Agent in Real-world City Environment. arXiv:2410.09604. 

- [50] Ning Gao, Yilun Chen, Shuai Yang, Xinyi Chen, Yang Tian, Hao Li, Haifeng Huang, Hanqing Wang, Tai Wang, and Jiangmiao Pang. 2025. GENMANIP: LLM-driven Simulation for Generalizable Instruction-Following Manipulation. arXiv:2506.10966. 

- [51] Qiaozi Gao, Govind Thattai, Suhaila Shakiah, Xiaofeng Gao, Shreyas Pansare, Vasu Sharma, Gaurav Sukhatme, Hangjie Shi, Bofei Yang, Desheng Zheng, Lucy Hu, Karthika Arumugam, Shui Hu, Matthew Wen, Dinakar Guthy, Cadence Chung, Rohan Khanna, Osman Ipek, Leslie Ball, Kate Bland, Heather Rocker, Yadunandana Rao, Michael Johnston, Reza Ghanadan, Arindam Mandal, Dilek Hakkani Tur, and Prem Natarajan. 2023. Alexa Arena: A User-Centric Interactive Platform for Embodied AI. arXiv:2303.01586. 

- [52] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. 2024. Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability. arXiv:2405.17398. 

- [53] Xiaofeng Gao, Qiaozi Gao, Ran Gong, Kaixiang Lin, Govind Thattai, and Gaurav S. Sukhatme. 2022. DialFRED: Dialogue-Enabled Agents for Embodied Instruction Following. arXiv:2202.13330. 

- [54] Ricardo Garcia, Shizhe Chen, and Cordelia Schmid. 2024. Towards Generalizable Vision-Language Robotic Manipulation: A Benchmark and LLM-guided 3D Policy. arXiv:2410.01345. 

- [55] Rohit Girdhar and Deva Ramanan. 2019. CATER: A diagnostic dataset for Compositional Actions and TEmporal Reasoning. arXiv:1910.04744. 

- [56] Ran Gong, Jiangyong Huang, Yizhou Zhao, Haoran Geng, Xiaofeng Gao, Qingyang Wu, Wensi Ai, Ziheng Zhou, Demetri Terzopoulos, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. 2023. ARNOLD: A Benchmark for Language-Grounded Task Learning With Continuous States in Realistic 3D Scenes. arXiv:2304.04321. 

- [57] Markus Grotz, Mohit Shridhar, Tamim Asfour, and Dieter Fox. 2024. PerAct2: Benchmarking and Learning for Robotic Bimanual Manipulation Tasks. arXiv:2407.00278. 

- [58] Jing Gu, Xian Liu, Yu Zeng, Ashwin Nagarajan, Fangrui Zhu, Daniel Hong, Yue Fan, Qianqi Yan, Kaiwen Zhou, Ming-Yu Liu, and Xin Eric Wang. 2025. PhyWorldBench: A Comprehensive Evaluation of Physical Realism in Text-to-Video Models. arXiv:2507.13428. 

- [59] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, Xiaodi Yuan, Pengwei Xie, Zhiao Huang, Rui Chen, and Hao Su. 2023. ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills. arXiv:2302.04659. 

- [60] Cole Gulino, Justin Fu, Wenjie Luo, George Tucker, Eli Bronstein, Yiren Lu, Jean Harb, Xinlei Pan, Yan Wang, Xiangyu Chen, John D. CoReyes, Rishabh Agarwal, Rebecca Roelofs, Yao Lu, Nico Montali, Paul Mougin, Zoey Yang, Brandyn White, Aleksandra Faust, Rowan McAllister, Dragomir Anguelov, and Benjamin Sapp. 2023. Waymax: An Accelerated, Data-Driven Simulator for Large-Scale Autonomous Driving Research. arXiv:2310.08710. 

- [61] Abhishek Gupta, Vikash Kumar, Corey Lynch, Sergey Levine, and Karol Hausman. 2019. Relay Policy Learning: Solving Long-Horizon Tasks via Imitation and Reinforcement Learning. arXiv:1910.11956. 

- [62] Agrim Gupta, Silvio Savarese, Surya Ganguli, and Li Fei-Fei. 2021. Embodied Intelligence via Learning and Evolution. arXiv:2102.02202. 

- [63] Xuan He, Dongfu Jiang, Ge Zhang, Max Ku, Achint Soni, Sherman Siu, Haonan Chen, Abhranil Chandra, Ziyan Jiang, Aaran Arulraj, Kai Wang, Quy Duc Do, Yuansheng Ni, Bohan Lyu, Yaswanth Narsupalli, Rongqi Fan, Zhiheng Lyu, Yuchen Lin, and Wenhu Chen. 2024. VideoScore: Building Automatic Metrics to Simulate Fine-grained Human Feedback for Video Generation. arXiv:2406.15252. 

- [64] Minho Heo, Youngwoon Lee, Doohyun Lee, and Joseph J. Lim. 2023. FurnitureBench: Reproducible Real-World Benchmark for Long-Horizon Complex Manipulation. arXiv:2305.12821. 

- [65] Bohan Hou, Gen Li, Jindou Jia, Tuo An, Xinying Guo, Sicong Leng, Haoran Geng, Yanjie Ze, Tatsuya Harada, Philip Torr, Oier Mees, Marc Pollefeys, Zhuang Liu, Jiajun Wu, Pieter Abbeel, Jitendra Malik, Yilun Du, and Jianfei Yang. 2026. World Model for Robot Learning: A Comprehensive Survey. arXiv:2605.00080. 

- [66] Liyu Hou, Linyuan Gao, Yuan Wu, and Yi Chang. 2026. A Survey on Evaluation of Embodied AI. Authorea preprint, DOI:10.22541/au.176851544.45077723. 

- [67] Yue Hu, Siyuan Huang, Yue Liao, Shengcong Chen, Pengfei Zhou, Liliang Chen, Maoqing Yao, and Guanghui Ren. 2025. EWMBench: Evaluating Scene, Motion, and Semantic Quality in Embodied World Models. arXiv:2505.09694. 

- [68] Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang, Chenyang Si, Yuming Jiang, Yuanhan Zhang, Tianxing Wu, Qingyang Jin, Nattapol Chanpaisit, Yaohui Wang, Xinyuan Chen, Limin Wang, Dahua Lin, Yu Qiao, and Ziwei Liu. 2023. VBench: Comprehensive Benchmark Suite for Video Generative Models. arXiv:2311.17982. 

- [69] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J. Davison. 2019. RLBench: The Robot Learning Benchmark and Learning Environment. arXiv:1909.12271. 

- [70] Steeven Janny, Fabien Baradel, Natalia Neverova, Madiha Nadri, Greg Mori, and Christian Wolf. 2022. Filtered-CoPhy: Unsupervised Learning of Counterfactual Physics in Pixel Space. arXiv:2202.00368. 

- [71] Serwan Jassim, Mario Holubar, Annika Richter, Cornelius Wolff, Xenia Ohmer, and Elia Bruni. 2023. GRASP: A novel benchmark for evaluating language GRounding And Situated Physics understanding in multimodal language models. arXiv:2311.09048. 

- [72] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. 2024. Bench2Drive: Towards Multi-Ability Benchmarking of Closed-Loop End-To-End Autonomous Driving. arXiv:2406.03877. 

- [73] Feng Jiang, Yang Chen, Kyle Xu, Yuchen Liu, Haifeng Wang, Zhenhao Shen, Jasper Lu, Shengze Huang, Yuanfei Wang, Chen Xie, and Ruihai Wu. 2026. RoboWM-Bench: A Benchmark for Evaluating World Models in Robotic Manipulation. arXiv:2604.19092. 

Do World Models Make Better Robots? 

25 

- [74] Huaizu Jiang, Xiaojian Ma, Weili Nie, Zhiding Yu, Yuke Zhu, Song-Chun Zhu, and Anima Anandkumar. 2022. Bongard-HOI: Benchmarking Few-Shot Visual Reasoning for Human-Object Interactions. arXiv:2205.13803. 

- [75] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. 2022. VIMA: General Robot Manipulation with Multimodal Prompts. arXiv:2210.03094. 

- [76] Shyam Sundar Kannan, Vishnunandan L. N. Venkatesh, and Byung-Cheol Min. 2023. SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models. arXiv:2309.10062. 

- [77] Mukul Khanna, Ram Ramrakhya, Gunjan Chhablani, Sriram Yenamandra, Theophile Gervet, Matthew Chang, Zsolt Kira, Devendra Singh Chaplot, Dhruv Batra, and Roozbeh Mottaghi. 2024. GOAT-Bench: A Benchmark for Multi-Modal Lifelong Navigation. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . arXiv:2404.06609. 

- [78] Grgur Kovac, Remy Portelas, Katja Hofmann, and Pierre-Yves Oudeyer. 2021. SocialAI: Benchmarking Socio-Cognitive Abilities in Deep Reinforcement Learning Agents. arXiv:2107.00956. 

- [79] Jacob Krantz, Erik Wijmans, Arjun Majumdar, Dhruv Batra, and Stefan Lee. 2020. Beyond the Nav-Graph: Vision-and-Language Navigation in Continuous Environments. arXiv:2004.02857. 

- [80] Alexander Ku, Peter Anderson, Roma Patel, Eugene Ie, and Jason Baldridge. 2020. Room-Across-Room: Multilingual Vision-and-Language Navigation with Dense Spatiotemporal Grounding. arXiv:2010.07954. 

- [81] Vikash Kumar, Rutav Shah, Gaoyue Zhou, Vincent Moens, Vittorio Caggiano, Jay Vakil, Abhishek Gupta, and Aravind Rajeswaran. 2023. RoboHive: A Unified Framework for Robot Learning. arXiv:2310.06828. 

- [82] Jinshan Lai, Jianwei Hu, Baoyang Jiang, Fengchun Zhang, Leyuan Wang, Haotian Li, Yida Wang, Tingxuan Huang, Xi Ren, and Qiang Ma. 2026. Intelligent Automation for Embodied Benchmark Construction: Pipelines, Embodiments, Simulators, and Trends. arXiv:2606.12207. 

- [83] Alex X. Lee, Coline Devin, Yuxiang Zhou, Thomas Lampe, Konstantinos Bousmalis, Jost Tobias Springenberg, Arunkumar Byravan, Abbas Abdolmaleki, Nimrod Gileadi, David Khosid, Claudio Fantacci, Jose Enrique Chen, Akhil Raju, Rae Jeong, Michael Neunert, Antoine Laurens, Stefano Saliceti, Federico Casarini, Martin Riedmiller, Raia Hadsell, and Francesco Nori. 2021. Beyond Pick-and-Place: Tackling Robotic Stacking of Diverse Shapes. arXiv:2110.06192. 

- [84] Joel Z. Leibo, Edgar Duenez-Guzman, Alexander Sasha Vezhnevets, John P. Agapiou, Peter Sunehag, Raphael Koster, Jayd Matyas, Charles Beattie, Igor Mordatch, and Thore Graepel. 2021. Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot. arXiv:2107.06857. 

- [85] Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto Martin-Martin, Chen Wang, Gabrael Levine, Wensi Ai, Benjamin Martinez, Hang Yin, Michael Lingelbach, Minjune Hwang, Ayano Hiranaka, Sujay Garlanka, Arman Aydin, Sharon Lee, Jiankai Sun, Mona Anvari, Manasi Sharma, Dhruva Bansal, Samuel Hunter, Kyu-Young Kim, Alan Lou, Caleb R Matthews, Ivan Villa-Renteria, Jerry Huayang Tang, Claire Tang, Fei Xia, Yunzhu Li, Silvio Savarese, Hyowon Gweon, C. Karen Liu, Jiajun Wu, and Li Fei-Fei. 2024. BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation. arXiv:2403.09227. 

- [86] Dacheng Li, Yunhao Fang, Yukang Chen, Shuo Yang, Shiyi Cao, Justin Wong, Michael Luo, Xiaolong Wang, Hongxu Yin, Joseph E. Gonzalez, Ion Stoica, Song Han, and Yao Lu. 2025. WorldModelBench: Judging Video Generation Models As World Models. arXiv:2502.20694. 

- [87] Quanyi Li, Zhenghao Peng, Lan Feng, Qihang Zhang, Zhenghai Xue, and Bolei Zhou. 2021. MetaDrive: Composing Diverse Driving Scenarios for Generalizable Reinforcement Learning. arXiv:2109.12674. 

- [88] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. 2024. Evaluating Real-World Robot Manipulation Policies in Simulation. arXiv:2405.05941. 

- [89] Mingxiang Liao, Hannan Lu, Xinyu Zhang, Fang Wan, Tianyu Wang, Yuzhong Zhao, Wangmeng Zuo, Qixiang Ye, and Jingdong Wang. 2024. Evaluation of Text-to-Video Generation Models: A Dynamics Perspective. arXiv:2407.01094. 

- [90] Xingyu Lin, Yufei Wang, Jake Olkin, and David Held. 2020. SoftGym: Benchmarking Deep Reinforcement Learning for Deformable Object Manipulation. arXiv:2011.07215. 

- [91] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. 2023. LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning. arXiv:2306.03310. 

- [92] Yaofang Liu, Xiaodong Cun, Xuebo Liu, Xintao Wang, Yong Zhang, Haoxin Chen, Yang Liu, Tieyong Zeng, Raymond Chan, and Ying Shan. 2023. EvalCrafter: Benchmarking and Evaluating Large Video Generation Models. arXiv:2310.11440. 

- [93] Yuanxin Liu, Lei Li, Shuhuai Ren, Rundong Gao, Shicheng Li, Sishuo Chen, Xu Sun, and Lu Hou. 2023. FETV: A Benchmark for Fine-Grained Evaluation of Open-Domain Text-to-Video Generation. arXiv:2311.01813. 

- [94] Jianlan Luo, Charles Xu, Fangchen Liu, Liam Tan, Zipeng Lin, Jeffrey Wu, Pieter Abbeel, and Sergey Levine. 2024. FMB: a Functional Manipulation Benchmark for Generalizable Robotic Learning. arXiv:2401.08553. 

- [95] Nicolai A. Lynnerup, Laura Nolling, Rasmus Hasle, and John Hallam. 2020. A Survey on Reproducibility by Evaluating Deep Reinforcement Learning Algorithms on Real-World Robots. In _Conference on Robot Learning (CoRL), PMLR vol. 100_ . arXiv:1909.03772. 

- [96] Arjun Majumdar, Karmesh Yadav, Sergio Arnaud, Yecheng Jason Ma, Claire Chen, Sneha Silwal, Aryan Jain, Vincent-Pierre Berges, Pieter Abbeel, Jitendra Malik, Dhruv Batra, Yixin Lin, Oleksandr Maksymets, Aravind Rajeswaran, and Franziska Meier. 2023. Where are we in the search for an Artificial Visual Cortex for Embodied Intelligence? arXiv:2303.18240. 

- [97] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, and Gavriel State. 2021. Isaac Gym: High Performance GPU-Based Physics Simulation For Robot Learning. arXiv:2108.10470. 

Jena et al. 

26 

- [98] Ajay Mandlekar, Danfei Xu, Josiah Wong, Soroush Nasiriany, Chen Wang, Rohun Kulkarni, Li Fei-Fei, Silvio Savarese, Yuke Zhu, and Roberto Martin-Martin. 2021. What Matters in Learning from Offline Human Demonstrations for Robot Manipulation. arXiv:2108.03298. 

- [99] Roberto Martin-Martin, Mihir Patel, Hamid Rezatofighi, Abhijeet Shenoi, JunYoung Gwak, Eric Frankel, Amir Sadeghian, and Silvio Savarese. 2019. JRDB: A Dataset and Benchmark of Egocentric Robot Visual Perception of Humans in Built Environments. arXiv:1910.11792. 

- [100] Daniel McDuff, Yale Song, Jiyoung Lee, Vibhav Vineet, Sai Vemprala, Nicholas Gyde, Hadi Salman, Shuang Ma, Kwanghoon Sohn, and Ashish Kapoor. 2021. CausalCity: Complex Simulations with Agency for Causal Discovery and Reasoning. arXiv:2106.13364. 

- [101] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. 2021. CALVIN: A Benchmark for Language-Conditioned Policy Learning for Long-Horizon Robot Manipulation Tasks. arXiv:2112.03227. 

- [102] Fanqing Meng, Jiaqi Liao, Xinyu Tan, Wenqi Shao, Quanfeng Lu, Kaipeng Zhang, Yu Cheng, Dianqi Li, Yu Qiao, and Ping Luo. 2024. Towards World Simulator: Crafting Physical Commonsense-Based Benchmark for Video Generation. arXiv:2410.05363. 

- [103] Saman Motamed, Laura Culp, Kevin Swersky, Priyank Jaini, and Robert Geirhos. 2025. Do generative video models understand physical principles? arXiv:2501.09038. 

- [104] Yao Mu, Tianxing Chen, Shijia Peng, Zanxin Chen, Zeyu Gao, Yude Zou, Lunkai Lin, Zhiqiang Xie, and Ping Luo. 2024. RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins. arXiv:2409.02920. 

- [105] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. 2024. RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots. arXiv:2406.02523. 

- [106] Aviv Netanyahu, Tianmin Shu, Boris Katz, Andrei Barbu, and Joshua B. Tenenbaum. 2021. PHASE: PHysically-grounded Abstract Social Events for Machine Social Perception. arXiv:2103.01933. 

- [107] Aishwarya Padmakumar, Jesse Thomason, Ayush Shrivastava, Patrick Lange, Anjali Narayan-Chen, Spandana Gella, Robinson Piramuthu, Gokhan Tur, and Dilek Hakkani-Tur. 2021. TEACh: Task-driven Embodied Agents that Chat. arXiv:2110.00534. 

- [108] Matthew J. Page, Joanne E. McKenzie, Patrick M. Bossuyt, Isabelle Boutron, Tammy C. Hoffmann, Cynthia D. Mulrow, et al. 2021. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. _BMJ_ 372 (2021), n71. doi:10.1136/bmj.n71. 

- [109] Noe Perez-Higueras, Roberto Otero, Fernando Caballero, and Luis Merino. 2023. HuNavSim: A ROS 2 Human Navigation Simulator for Benchmarking Human-Aware Robot Navigation. arXiv:2305.01303. 

- [110] Xavier Puig, Kevin Ra, Marko Boben, Jiaman Li, Tingwu Wang, Sanja Fidler, and Antonio Torralba. 2018. VirtualHome: Simulating Household Activities via Programs. arXiv:1806.07011. 

- [111] Xavier Puig, Tianmin Shu, Shuang Li, Zilin Wang, Yuan-Hong Liao, Joshua B. Tenenbaum, Sanja Fidler, and Antonio Torralba. 2020. Watch-And-Help: A Challenge for Social Perception and Human-AI Collaboration. arXiv:2010.09890. 

- [112] Xavier Puig, Eric Undersander, Andrew Szot, Mikael Dallaire Cote, Tsung-Yen Yang, Ruslan Partsey, Ruta Desai, Alexander William Clegg, Michal Hlavac, So Yeon Min, Vladimir Vondrus, Theophile Gervet, Vincent-Pierre Berges, John M. Turner, Oleksandr Maksymets, Zsolt Kira, Mrinal Kalakrishnan, Jitendra Malik, Devendra Singh Chaplot, Unnat Jain, Dhruv Batra, Akshara Rai, and Roozbeh Mottaghi. 2023. Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots. arXiv:2310.13724. 

- [113] Wilbert Pumacay, Ishika Singh, Jiafei Duan, Ranjay Krishna, Jesse Thomason, and Dieter Fox. 2024. THE COLOSSEUM: A Benchmark for Evaluating Generalization for Robotic Manipulation. arXiv:2402.08191. 

- [114] Yuankai Qi, Qi Wu, Peter Anderson, Xin Wang, William Yang Wang, Chunhua Shen, and Anton van den Hengel. 2019. REVERIE: Remote Embodied Visual Referring Expression in Real Indoor Environments. arXiv:1904.10151. 

- [115] Yiran Qin, Zhelun Shi, Jiwen Yu, Xijun Wang, Enshen Zhou, Lijun Li, Zhenfei Yin, Xihui Liu, Lu Sheng, Jing Shao, Lei Bai, Wanli Ouyang, and Ruimao Zhang. 2024. WorldSimBench: Towards Video Generation Models as World Simulators. arXiv:2410.18072. 

- [116] Shi Qiu, Shaoyang Guo, Zhuo-Yang Song, Yunbo Sun, Zeyu Cai, Jiashen Wei, Tianyu Luo, and Yixuan Yin. 2025. PHYBench: Holistic Evaluation of Physical Perception and Reasoning in Large Language Models. arXiv:2504.16074. 

- [117] Santhosh K. Ramakrishnan, Aaron Gokaslan, Erik Wijmans, Oleksandr Maksymets, Alex Clegg, John Turner, Eric Undersander, Wojciech Galuba, Andrew Westbury, Angel X. Chang, Manolis Savva, Yili Zhao, and Dhruv Batra. 2021. Habitat-Matterport 3D Dataset (HM3D): 1000 Large-scale 3D Environments for Embodied AI. arXiv:2109.08238. 

- [118] Ronan Riochet, Mario Ynocente Castro, Mathieu Bernard, Adam Lerer, Rob Fergus, Veronique Izard, and Emmanuel Dupoux. 2018. IntPhys: A Framework and Benchmark for Visual Intuitive Physics Reasoning. arXiv:1803.07616. 

- [119] Nikita Rudin, David Hoeller, Philipp Reist, and Marco Hutter. 2021. Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning. arXiv:2109.11978. 

- [120] Mikayel Samvelyan, Tabish Rashid, Christian Schroeder de Witt, Gregory Farquhar, Nantas Nardelli, Tim G. J. Rudner, Chia-Man Hung, Philip H. S. Torr, Jakob Foerster, and Shimon Whiteson. 2019. The StarCraft Multi-Agent Challenge. arXiv:1902.04043. 

- [121] Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, Vladlen Koltun, Jitendra Malik, Devi Parikh, and Dhruv Batra. 2019. Habitat: A Platform for Embodied AI Research. arXiv:1904.01201. 

- [122] Pierre Sermanet, Tianli Ding, Jeffrey Zhao, Fei Xia, Debidatta Dwibedi, Keerthana Gopalakrishnan, Christine Chan, Gabriel Dulac-Arnold, Sharath Maddineni, Nikhil J Joshi, Pete Florence, Wei Han, Robert Baruch, Yao Lu, Suvir Mirchandani, Peng Xu, Pannag Sanketi, Karol Hausman, Izhak Shafran, Brian Ichter, and Yuan Cao. 2023. RoboVQA: Multimodal Long-Horizon Reasoning for Robotics. arXiv:2311.00899. 

- [123] Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. 2024. HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation. arXiv:2403.10506. 

Do World Models Make Better Robots? 

27 

- [124] Yu Shang, Zhuohang Li, Yiding Ma, Weikang Su, Xin Jin, Ziyou Wang, Lei Jin, Xin Zhang, Yinzhou Tang, Haisheng Su, Chen Gao, Wei Wu, Xihui Liu, Dhruv Shah, Zhaoxiang Zhang, Zhibo Chen, Jun Zhu, Yonghong Tian, Wenwu Zhu, and Yong Li. 2026. WorldArena: A Unified Benchmark for Evaluating Perception and Functional Utility of Embodied World Models. arXiv:2602.08971. 

- [125] Yu Shang, Yinzhou Tang, Xin Zhang, Shengyuan Wang, Yuwei Yan, Honglin Zhang, Zhiheng Zheng, Jie Zhao, Jie Feng, Chen Gao, Jiansheng Chen, and Yong Li. 2026. A Survey of Embodied World Models. Preprint (non-arXiv). 

- [126] Bokui Shen, Fei Xia, Chengshu Li, Roberto Martin-Martin, Linxi Fan, Guanzhi Wang, Claudia Perez-DArpino, Shyamal Buch, Sanjana Srivastava, Lyne P. Tchapmi, Micael E. Tchapmi, Kent Vainio, Josiah Wong, Li Fei-Fei, and Silvio Savarese. 2020. iGibson 1.0: a Simulation Environment for Interactive Tasks in Large Realistic Scenes. arXiv:2012.02924. 

- [127] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. 2022. Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation. arXiv:2209.05451. [128] Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, and Dieter Fox. 2019. ALFRED: A Benchmark for Interpreting Grounded Instructions for Everyday Tasks. arXiv:1912.01734. 

- [129] Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Cote, Yonatan Bisk, Adam Trischler, and Matthew Hausknecht. 2020. ALFWorld: Aligning Text and Embodied Environments for Interactive Learning. arXiv:2010.03768. 

- [130] Tianmin Shu, Abhishek Bhandwaldar, Chuang Gan, Kevin A. Smith, Shari Liu, Dan Gutfreund, Elizabeth Spelke, Joshua B. Tenenbaum, and Tomer D. Ullman. 2021. AGENT: A Benchmark for Core Psychological Reasoning. arXiv:2102.12321. 

- [131] Xinshuai Song, Weixing Chen, Yang Liu, Weikai Chen, Guanbin Li, and Liang Lin. 2024. Towards Long-Horizon Vision-Language Navigation: Platform, Benchmark and Method. arXiv:2412.09082. 

- [132] Zayne Sprague, Rohan Chandra, Jarrett Holtz, and Joydeep Biswas. 2023. SocialGym 2.0: Simulator for Multi-Agent Social Robot Navigation in Shared Human Spaces. arXiv:2303.05584. 

- [133] Haisheng Su, Feixiang Song, Cong Ma, Wei Wu, and Junchi Yan. 2024. RoboSense: Large-scale Dataset and Benchmark for Egocentric Robot Perception and Navigation in Crowded and Unstructured Environments. arXiv:2408.15503. 

- [134] Kaiyue Sun, Kaiyi Huang, Xian Liu, Yue Wu, Zihan Xu, Zhenguo Li, and Xihui Liu. 2024. T2V-CompBench: A Comprehensive Benchmark for Compositional Text-to-video Generation. arXiv:2407.14505. 

- [135] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, Vijay Vasudevan, Wei Han, Jiquan Ngiam, Hang Zhao, Aleksei Timofeev, Scott Ettinger, Maxim Krivokon, Amy Gao, Aditya Joshi, Sheng Zhao, Shuyang Cheng, Yu Zhang, Jonathon Shlens, Zhifeng Chen, and Dragomir Anguelov. 2019. Scalability in Perception for Autonomous Driving: Waymo Open Dataset. arXiv:1912.04838. 

- [136] Andrew Szot, Alex Clegg, Eric Undersander, Erik Wijmans, Yili Zhao, John Turner, Noah Maestre, Mustafa Mukadam, Devendra Chaplot, Oleksandr Maksymets, Aaron Gokaslan, Vladimir Vondrus, Sameer Dharur, Franziska Meier, Wojciech Galuba, Angel Chang, Zsolt Kira, Vladlen Koltun, Jitendra Malik, Manolis Savva, and Dhruv Batra. 2021. Habitat 2.0: Training Home Assistants to Rearrange their Habitat. arXiv:2106.14405. 

- [137] Nathan Tsoi, Mohamed Hussein, Jeacy Espinoza, Xavier Ruiz, and Marynel Vazquez. 2020. SEAN: Social Environment for Autonomous Navigation. arXiv:2009.04300. 

- [138] Hsiao-Yu Tung, Mingyu Ding, Zhenfang Chen, Daniel Bear, Chuang Gan, Joshua B. Tenenbaum, Daniel L. K. Yamins, Judith E. Fan, and Kevin A. Smith. 2023. Physion++: Evaluating Physical Scene Understanding that Requires Online Inference of Different Physical Properties. arXiv:2306.15668. 

- [139] Karthik Valmeekam, Matthew Marquez, Alberto Olmo, Sarath Sreedharan, and Subbarao Kambhampati. 2022. PlanBench: An Extensible Benchmark for Evaluating Large Language Models on Planning and Reasoning about Change. arXiv:2206.10498. 

- [140] Hanqing Wang, Jiahe Chen, Wensi Huang, Qingwei Ben, Tai Wang, Boyu Mi, Tao Huang, Siheng Zhao, Yilun Chen, Sizhe Yang, Peizhou Cao, Wenye Yu, Zichao Ye, Jialun Li, Junfeng Long, Zirui Wang, Huiling Wang, Ying Zhao, Zhongying Tu, Yu Qiao, Dahua Lin, and Jiangmiao Pang. 2024. GRUtopia: Dream General Robots in a City at Scale. arXiv:2407.10943. 

- [141] Yuxuan Wang, Yueqian Wang, Dongyan Zhao, Cihang Xie, and Zilong Zheng. 2024. VideoHallucer: Evaluating Intrinsic and Extrinsic Hallucinations in Large Video-Language Models. arXiv:2406.16338. 

- [142] Ziyao Wang, Bingying Wang, Hanrong Zhang, Tingting Du, Tianyang Chen, Guoheng Sun, Yexiao He, Zheyu Shen, Wanghao Ye, and Ang Li. 2026. Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines. arXiv:2604.23001. 

- [143] Jimmy Wu, Rika Antonova, Adam Kan, Marion Lepert, Andy Zeng, Shuran Song, Jeannette Bohg, Szymon Rusinkiewicz, and Thomas Funkhouser. 2023. TidyBot: Personalized Robot Assistance with Large Language Models. arXiv:2305.05658. 

- [144] Jay Zhangjie Wu, Guian Fang, Haoning Wu, Xintao Wang, Yixiao Ge, Xiaodong Cun, David Junhao Zhang, Jia-Wei Liu, Yuchao Gu, Rui Zhao, Weisi Lin, Wynne Hsu, Ying Shan, and Mike Zheng Shou. 2024. Towards A Better Metric for Text-to-Video Generation. arXiv:2401.07781. 

- [145] Fei Xia, Amir Zamir, Zhi-Yang He, Alexander Sax, Jitendra Malik, and Silvio Savarese. 2018. Gibson Env: Real-World Perception for Embodied Agents. arXiv:1808.10654. 

- [146] Yinzhen Xu, Weikang Wan, Jialiang Zhang, Haoran Liu, Zikang Shan, Hao Shen, Ruicheng Wang, Haoran Geng, Yijia Weng, Jiayi Chen, Tengyu Liu, Li Yi, and He Wang. 2023. UniDexGrasp: Universal Robotic Dexterous Grasping via Learning Diverse Proposal Generation and Goal-Conditioned Policy. arXiv:2303.00938. 

- [147] Rui Yang, Hanyang Chen, Junyu Zhang, Mark Zhao, Cheng Qian, Kangrui Wang, Qineng Wang, Teja Venkat Koripella, Marziyeh Movahedi, Manling Li, Heng Ji, Huan Zhang, and Tong Zhang. 2025. EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents. arXiv:2502.09560. 

Jena et al. 

28 

- [148] Xuemeng Yang, Licheng Wen, Yukai Ma, Jianbiao Mei, Xin Li, Tiantian Wei, Wenjie Lei, Daocheng Fu, Pinlong Cai, Min Dou, Botian Shi, Liang He, Yong Liu, and Yu Qiao. 2024. DriveArena: A Closed-loop Generative Simulation Platform for Autonomous Driving. arXiv:2408.00415. 

- [149] Sriram Yenamandra, Arun Ramachandran, Karmesh Yadav, Austin Wang, Mukul Khanna, Theophile Gervet, Tsung-Yen Yang, Vidhi Jain, Alexander William Clegg, John Turner, Zsolt Kira, Manolis Savva, Angel Chang, Devendra Singh Chaplot, Dhruv Batra, Roozbeh Mottaghi, Yonatan Bisk, and Chris Paxton. 2023. HomeRobot: Open-Vocabulary Mobile Manipulation. arXiv:2306.11565. 

- [150] Kexin Yi, Chuang Gan, Yunzhu Li, Pushmeet Kohli, Jiajun Wu, Antonio Torralba, and Joshua B. Tenenbaum. 2019. CLEVRER: CoLlision Events for Video REpresentation and Reasoning. arXiv:1910.01442. 

- [151] Sheng Yin, Xianghe Pang, Yuanzhuo Ding, Menglan Chen, Yutong Bi, Yichen Xiong, Wenhao Huang, Zhen Xiang, Jing Shao, and Siheng Chen. 2024. SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents. arXiv:2412.13178. 

- [152] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Avnish Narayan, Hayden Shively, Adithya Bellathur, Karol Hausman, Chelsea Finn, and Sergey Levine. 2019. Meta-World: A Benchmark and Evaluation for Multi-Task and Meta Reinforcement Learning. arXiv:1910.10897. 

- [153] Yang Yu, Shiyuan Zhang, Yifei Sheng, Haoxiang Ren, and Haoxin Lin. 2026. How Should World Models Be Evaluated for Embodied Decision-Making? A Decision-Making-Centric Position. arXiv:2606.15032. 

- [154] Andy Zeng, Pete Florence, Jonathan Tompson, Stefan Welker, Jonathan Chien, Maria Attarian, Travis Armstrong, Ivan Krasin, Dan Duong, Ayzaan Wahid, Vikas Sindhwani, and Johnny Lee. 2020. Transporter Networks: Rearranging the Visual World for Robotic Manipulation. arXiv:2010.14406. 

- [155] Chi Zhang, Baoxiong Jia, Mark Edmonds, Song-Chun Zhu, and Yixin Zhu. 2021. ACRE: Abstract Causal REasoning Beyond Covariation. arXiv:2103.14232. 

- [156] Hongxin Zhang, Weihua Du, Jiaming Shan, Qinhong Zhou, Yilun Du, Joshua B. Tenenbaum, Tianmin Shu, and Chuang Gan. 2023. Building Cooperative Embodied Agents Modularly with Large Language Models. arXiv:2307.02485. 

- [157] Jiahan Zhang, Muqing Jiang, Nanru Dai, Taiming Lu, Arda Uzunoglu, Shunchi Zhang, Yana Wei, Jiahao Wang, Vishal M. Patel, Paul Pu Liang, Daniel Khashabi, Cheng Peng, Rama Chellappa, Tianmin Shu, Alan Yuille, Yilun Du, and Jieneng Chen. 2025. World-in-World: World Models in a Closed-Loop World. arXiv:2510.18135. 

- [158] Min Zhang, Xian Fu, Jianye Hao, Peilong Han, Hao Zhang, Lei Shi, Hongyao Tang, and Yan Zheng. 2024. MFE-ETP: A Comprehensive Evaluation Benchmark for Multi-modal Foundation Models on Embodied Task Planning. arXiv:2407.05047. 

- [159] Shengqiang Zhang, Philipp Wicke, Lutfi Kerem Senel, Luis Figueredo, Abdeldjallil Naceri, Sami Haddadin, Barbara Plank, and Hinrich Schutze. 2023. LoHoRavens: A Long-Horizon Language-Conditioned Benchmark for Robotic Tabletop Manipulation. arXiv:2310.12020. 

- [160] Shiduo Zhang, Zhe Xu, Peiju Liu, Xiaopeng Yu, Yuan Li, Qinghui Gao, Zhaoye Fei, Zhangyue Yin, Zuxuan Wu, Yu-Gang Jiang, and Xipeng Qiu. 2024. VLABench: A Large-Scale Benchmark for Language-Conditioned Robotics Manipulation with Long-Horizon Reasoning Tasks. arXiv:2412.18194. 

- [161] Dian Zheng, Ziqi Huang, Hongbo Liu, Kai Zou, Yinan He, Fan Zhang, Lulu Gu, Yuanhan Zhang, Jingwen He, Wei-Shi Zheng, Yu Qiao, and Ziwei Liu. 2025. VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness. arXiv:2503.21755. 

- [162] Kaizhi Zheng, Xiaotong Chen, Odest Chadwicke Jenkins, and Xin Eric Wang. 2022. VLMbench: A Compositional Benchmark for Vision-andLanguage Manipulation. arXiv:2206.08522. 

- [163] Zhicheng Zheng, Xin Yan, Zhenfang Chen, Jingzhou Wang, Qin Zhi Eddie Lim, Joshua B. Tenenbaum, and Chuang Gan. 2024. ContPhy: Continuum Physical Concept Learning and Reasoning from Videos. arXiv:2402.06119. 

- [164] Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Martin-Martin, Abhishek Joshi, Kevin Lin, Abhiram Maddukuri, Soroush Nasiriany, and Yifeng Zhu. 2020. robosuite: A Modular Simulation Framework and Benchmark for Robot Learning. arXiv:2009.12293. 

Do World Models Make Better Robots? 

29 

## **A The full benchmark landscape** 

The core taxonomy (Figure 7) shows 86 representative benchmarks, those that are cleanly axis-placeable, distinct, and fully characterisable from their papers. For completeness and reproducibility, Table 10 lists the full catalogue of 160 web-verified benchmarks, grouped by the same four evaluation lanes and sub-grouped by capability, and compared on year, capability, evaluation mode, and whether the benchmark builds a native VLA-versus-world-model contrast. Every entry is a real, individually citeable benchmark; the column tallies are the source of the counts reported throughout the survey and of the distributions in Figure 5. 

Table 10. **The robot-evaluation benchmark landscape: 160 web-verified benchmarks, compared on four axes.** Grouped into four evaluation lanes and sub-grouped by capability. Columns: **Year** ; **Capability** (what the benchmark stresses); **Eval** (evaluation mode: open-loop prediction/generation quality, closed-loop task success, or a prediction-to-action bridge); and **VLA vs WM** (does the benchmark build a native direct-policy vs world-model contrast: ✔ explicit, **~** partial, **--** model-agnostic). Every entry is a real, individually citeable benchmark. 

|**Benchmark**|**Year**|**Capability**|**Eval**|**VLA vs WM**|
|---|---|---|---|---|
|**Policy / manipulation suites**(37)|||||
|_Manipulation_|||||
|**ARNOLD**[56]|2023|language-grounded continuous-state 3D manipulation|closed|**--**|
|**BiGym**[32]|2024|mobile bimanual manipulation|closed|**--**|
|**FMB**[94]|2024|real-world functional multi-step assembly manipulation|closed|**--**|
|**Franka Kitchen**[61]|2019|multi-task kitchen manipulation|closed|**--**|
|**FurnitureBench**[64]|2023|real-world furniture assembly|closed|**--**|
|**GRUtopia**[140]|2024|city-scale embodied navigation and manipulation|closed|**--**|
|**KitchenShift**|2021|kitchen distribution-shift generalization|closed|**--**|
|**ManiSkill2**[59]|2023|generalizable skills|closed|**--**|
|**PerAct**[127]|2022|language-conditioned 6-DoF single-arm manipulation|closed|**--**|
|**PerAct2**[57]|2024|bimanual language-conditioned manipulation|closed|**--**|
|**Ravens**[154]|2020|vision-based pick-and-place rearrangement|closed|**--**|
|**RGB-Stacking**[83]|2021|vision-based stacking of diverse shapes|closed|**--**|
|**RLBench**[69]|2020|manipulation breadth|closed|**--**|
|**RoboAgent**[13]|2023|multi-task manipulation with RoboSet|closed|**--**|
|**robomimic**[98]|2021|single-arm manipulation from human demonstrations|closed|**--**|
|**robosuite**[164]|2020|modular simulated single-arm manipulation tasks|closed|**--**|
|**RoboTwin**[104]|2024|dual-arm bimanual manipulation|closed|**--**|
|**VLMbench**[162]|2022|vision-and-language compositional manipulation|closed|**--**|
|_Generalization & robustness_|||||
|**GemBench**[54]|2024|generalization levels|closed|**--**|
|**LIBERO**[91]|2023|short-horizon + transfer|closed|**--**|
|**RoboArena**[4]|2025|real-world generalization|closed|**--**|
|**SIMPLER / SimplerEnv**[88]|2024|generalization (real vs sim)|closed|**--**|
|**THE COLOSSEUM**[113]|2024|generalization / robustness|closed|**--**|
|**VIMA-Bench**[75]|2023|multimodal-prompt generalization|closed|**--**|
|_Other_|||||
|**CortexBench**[96]|2023|pretrained visual representations for embodied control|closed|**--**|
|**GenManip**[50]|2025|LLM-scene tasks|closed|**~**|
|**HandoverSim**[22]|2022|human-to-robot object handover|closed|**--**|
|**Meta-World**[152]|2020|multi-task / meta-RL|closed|**--**|
|**RoboHive**[81]|2023|unified robot-learning environments|closed|**--**|
|_Dexterous manipulation_|||||
|**Bi-DexHands**[28]|2022|bimanual dexterous manipulation|closed|**--**|
|**DeformableGym**|2023|3D deformable-object grasping|closed|**--**|
|**DexArt**[9]|2023|dexterous articulated-object manipulation|closed|**--**|
|**UniDexGrasp**[146]|2023|universal dexterous grasping|closed|**--**|


Jena et al. 

30 

### _Table 10 (continued)_ 

|**Benchmark**|**Year**|**Capability**|**Eval**<br>**VLA vs WM**|
|---|---|---|---|
|_Long-horizon & planning_||||
|**CALVIN**[101]|2021|long-horizon language|closed<br>**--**|
|**RoboCasa**[105]|2024|long-horizon (data scaling)|closed<br>**--**|
|**VLABench**[160]|2025|long-horizon reasoning|closed<br>**--**|
|_Deformable-object manipulation_||||
|**SoftGym**[90]|2020|deformable-object manipulation|closed<br>**--**|
|**Embodied navigation, planning & social**(85)||||
|_Long-horizon & planning_||||
|**Alexa Arena**[51]|2023|task-planning|closed<br>**--**|
|**ALFRED**[128]|2019|long-horizon, partial-obs|closed<br>**--**|
|**BEHAVIOR-1K**[85]|2024|long-horizon household|closed<br>**--**|
|**CoELA (C-WAH/TDW-MAT)**[156]|2023|long-horizon|closed<br>**--**|
|**DialFRED**[53]|2022|task-planning|closed<br>**--**|
|**EgoPlan-Bench**[27]|2023|task-planning|closed<br>**--**|
|**EmbodiedBench**[147]|2025|long-horizon|closed<br>**--**|
|**EmbodiedCity**[49]|2024|long-horizon|closed<br>**--**|
|**EmbodiedEval**[30]|2025|long-horizon|closed<br>**--**|
|**HomeRobot OVMM**[149]|2023|long-horizon|closed<br>**--**|
|**LEGENT**[31]|2024|long-horizon|closed<br>**--**|
|**LH-VLN**[131]|2024|long-horizon|closed<br>**--**|
|**LoHoRavens**[159]|2023|long-horizon|closed<br>**--**|
|**LoTa-Bench**[34]|2024|task-planning|closed<br>**--**|
|**MFE-ETP**[158]|2024|task-planning|closed<br>**--**|
|**PARTNR**[21]|2024|task-planning|closed<br>**--**|
|**PlanBench**[139]|2022|task-planning|closed<br>**--**|
|**SafeAgentBench**[151]|2024|task-planning|closed<br>**--**|
|**SMART-LLM**[76]|2023|task-planning|closed<br>**--**|
|**TDW-Transport**[47]|2021|task-planning|closed<br>**--**|
|**TidyBot**[143]|2023|task-planning|closed<br>**--**|
|**VirtualHome**[110]|2018|task-planning|closed<br>**--**|
|**Watch-And-Help**[111]|2020|long-horizon|closed<br>**--**|
|_Social & multi-agent_||||
|**CrowdNav**[24]|2018|social|closed<br>**--**|
|**Habitat 3.0**[112]|2023|social / multi-agent|closed<br>**--**|
|**HuNavSim**[109]|2023|social|closed<br>**--**|
|**JRDB**[99]|2019|social|closed<br>**--**|
|**JRDB-Act**[43]|2021|social|closed<br>**--**|
|**Melting Pot**[84]|2021|social|closed<br>**--**|
|**Overcooked-AI**[19]|2019|social|closed<br>**--**|
|**RoboSense**[133]|2024|social|closed<br>**--**|
|**SEAN**[137]|2020|social|closed<br>**--**|
|**SMAC**[120]|2019|social|closed<br>**--**|
|**SocialGym 2.0**[132]|2023|social|closed<br>**--**|
|**SocNavBench**[14]|2021|social navigation|closed<br>**--**|
|_Navigation_||||
|**Gibson Env**[145]|2018|navigation|closed<br>**--**|
|**GOAT-Bench**[77]|2024|multi-modal lifelong navigation|closed<br>**--**|
|**Habitat**[121]|2019|navigation|closed<br>**--**|
|<br>**Habitat 2.0**[136]|2021|rearrangement|closed<br>**--**|
|**HM3D**[117]|2021|navigation|closed<br>**--**|
|**iGibson**[126]|2020|interactive navigation|closed<br>**--**|
|**Matterport3D**[20]|2017|navigation|closed<br>**--**|
|**ObjectNav**[11]|2020|object-goal navigation|closed<br>**--**|
|<br>**ProcTHOR**[39]|2022|<br>navigation|closed<br>**--**|


Do World Models Make Better Robots? 

31 

_Table 10 (continued)_ 

|**Benchmark**|**Year**|**Capability**|**Eval**|**VLA vs WM**|
|---|---|---|---|---|
|**RoboTHOR**[38]|2020|navigation / sim-to-real|closed|**--**|
|**SoundSpaces**[23]|2020|audio-visual navigation|closed|**--**|
|_Autonomous driving_|||||
|**Bench2Drive**[72]|2024|driving|closed|**--**|
|**CARLA**[40]|2017|driving|closed|**--**|
|**DriveArena**[148]<br>|2024|driving<br>|closed<br>|✔|
|**MetaDrive**[87]|2021|driving|closed|**--**|
|**NAVSIM**[37]|2024|driving|closed|**--**|
|**nuScenes**[17]<br>|2019|driving<br>|closed<br>|**--**|
|**Waymax**[60]|2023|driving|closed|**--**|
|**Waymo Open**[135]|2019|driving|closed|**--**|
|_Counterfactual reasoning_|||||
|**ACRE**[155]|2021|counterfactual|open|✔|
|**CausalCity**[100]|2021|counterfactual|closed|**~**|
|**CausalVQA**[45]|2025|counterfactual|open|✔|
|**CausalWorld**[1]|2020|counterfactual|closed|✔|
|**CoPhy**[10]|2019|counterfactual|open|✔|
|**CRAFT**[3]|2020|counterfactual|open|✔|
|**Filtered-CoPhy**[70]|2022|counterfactual|open|✔|
|_Locomotion_|||||
|**Barkour**[18]|2023|legged locomotion|closed|**--**|
|**Brax**[46]|2021|locomotion|closed|**--**|
|**DERL**[62]|2021|locomotion|closed|**--**|
|**HumanoidBench**[123]|2024|humanoid locomotion|closed|**--**|
|**Isaac Gym**[97]|2021|locomotion|closed|**--**|
|**Legged Gym**[119]|2021|legged locomotion|closed|**--**|
|_Theory of mind_|||||
|**AGENT**[130]|2021|theory-of-mind|open|✔|
|**BIB**[48]|2021|theory-of-mind|open|✔|
|**PHASE**[106]|2021|theory-of-mind|closed|**~**|
|**SocialAI**[78]|2021|theory-of-mind|closed|**--**|
|**ToMi**|2019|theory-of-mind|closed|**~**|
|_Vision-language navigation_|||||
|**R2R**[2]|2018|VLN|closed|**--**|
|**REVERIE**[114]|2020|VLN|closed|**--**|
|**RxR**[80]|2020|VLN|closed|**--**|
|**Touchdown**[26]|2019|outdoor VLN|closed|**--**|
|**VLN-CE**[79]|2020|VLN|closed|**--**|
|_Hidden-state / object permanence_|||||
|**Bongard-HOI**[74]|2022|hidden-state|open|**~**|
|**ComPhy**[29]|2022|hidden-state|open|✔|
|**LIBERO-Mem**[36]<br>|2025|hidden-state / occlusion<br>|closed|✔|
|**TEACh**[107]|2021|hidden-state (dialog)|closed|**--**|
|_Embodied question answering_|||||
|**OpenEQA**|2024|EQA|closed|**--**|
|**RoboVQA**[122]|2023|EQA|closed|**--**|
|_Generalization & robustness_|||||
|**ALFWorld**[129]|2020|abstract-vs-grounded transfer|closed|**~**|
|_Other_|||||
|**O-PIAAGETS**|2022|object permanence|closed|**~**|
|**World-model & video-generation evaluation**(34)|||||
|_Generation quality_|||||
|**CATER**[55]|2019|compositional-action temporal reasoning|open|**--**|
|**DEVIL**[89]|2024|content-dynamics quality of T2V models|open|**--**|


Jena et al. 

32 

_Table 10 (continued)_ 

|**Benchmark**|**Year**|**Capability**|**Eval**|**VLA vs WM**|
|---|---|---|---|---|
|**EVA-Bench**[33]|2024|embodied video anticipation|open|**--**|
|**EvalCrafter**[92]|2023|generation quality (17-metric suite)|open|**--**|
|**EWMBench**[67]|2025|scene/motion/semantic quality|open|**--**|
|**FETV**[93]|2023|fine-grained text-to-video quality|open|**--**|
|**IPV-Bench**[5]|2025|impossible-video generation + understanding|open|**--**|
|**StoryBench**[16]|2023|continuous story visualization|open|**--**|
|**T2V-CompBench**[134]|2024|compositional text-to-video quality|open|**--**|
|**T2VScore**[144]|2024|text-to-video metric (alignment + quality)|open|**--**|
|**TC-Bench**[44]|2024|temporal compositionality in video generation|open|**--**|
|**VBench**[68]|2023|generation quality (16 disentangled dimensions)|open|**--**|
|**VBench-2.0**[161]|2025|generation faithfulness|open|**--**|
|**VideoCon**[6]|2023|robust video-language alignment|open|**--**|
|**VideoHallucer**[141]|2024|hallucination in video-language models|open|**--**|
|**VideoScore**[63]|2024|learned automatic quality metric|open|**--**|
|**WorldModelBench**[86]|2025|video-WM prediction quality|open|**--**|
|**WorldScore**[41]|2025|world-gen quality|open|**--**|
|_Physical reasoning_|||||
|**ContPhy**[163]|2024|continuum (soft-body/fluid) physical reasoning|open|**--**|
|**GRASP**[71]|2023|grounding + intuitive physics in video MLLMs|open|**--**|
|**IntPhys**[118]|2018|intuitive physics (violation-of-expectation)|open|**--**|
|**IntPhys 2**[15]|2025|intuitive physics in complex scenes|open|**--**|
|**PHYBench**[116]|2025|physical perception and reasoning|open|**--**|
|**PhyGenBench**[102]|2024|physical-commonsense correctness in video gen|open|**--**|
|**PhysBench**[35]|2025|physical-world understanding for VLMs|open|**--**|
|**Physics-IQ**[103]|2025|physical realism|open|**--**|
|**Physion**[12]|2021|physical prediction from vision|open|**--**|
|**Physion++**[138]|2023|physical prediction with online property inference|open|**--**|
|**PhyWorldBench**[58]|2025|physical realism in text-to-video|open|**--**|
|**VideoPhy**[7]|2024|physical commonsense in generated video|open|**--**|
|**VideoPhy-2**[8]|2025|action-centric physical commonsense|open|**--**|
|_Counterfactual reasoning_|||||
|**CLEVRER**[150]|2019|physical/causal video reasoning (counterfactual)|open|**--**|
|**WorldPrediction**[25]|2025|counterfactual action recognition|open|**--**|
|_Autonomous driving_|||||
|**Vista**[52]|2024|driving world model|open|**--**|
|**Bridges (prediction to action)**(4)|||||
|_Other_|||||
|**RoboWM-Bench**[73]|2026|prediction executability|bridge|**~**|
|**World-in-World**[157]|2025|closed-loop task success of WMs|bridge|**~**|
|**WorldArena**[124]|2026|closed-loop WM arena|bridge|**~**|
|_Generation quality_|||||
|**WorldSimBench**[115]|2024|video-to-action consistency|bridge|**~**|


## **B Provenance of the galleries and collage** 

Every panel in the subject and results galleries (Figures 8, 9) and every tile in the hero collage (Figure 1) is a real figure reproduced from the benchmark’s own paper, hyperlinked to its arXiv source. The tables below record, for each panel and tile, its source benchmark and the verified figure number within that paper; a panel whose figure could not be located was dropped rather than guessed. Table 11 covers the subject gallery, Table 12 the results gallery, and Table 13 the collage. 

Do World Models Make Better Robots? 

33 

|**Benchmark**|**arXiv**|**Panel source (subject scene)**|
|---|---|---|
|**Closed-loop task-s**|**uccess suites**||
|ALFRED|1912.01734|sim task scene (rep. figure, pp.1–3)|
|BEHAVIOR-1K|2403.09227|household sim scene (rep. figure, pp.1–3)|
|CALVIN|2112.03227|tabletop manipulation scene (rep. figure, pp.1–3)|
|GemBench|2410.01345|manipulation scene (rep. figure, pp.1–3)|
|ManiSkill2|2302.04659|multi-task sim scenes (rep. figure, pp.1–3)|
|Meta-World|1910.10897|task-suite thumbnail grid (rep. figure, pp.1–3)|
|RoboCasa|2406.02523|kitchen sim scene (rep. figure, pp.1–3)|
|LIBERO|2306.03310|manipulation task scene (embedded raster, pp.1–8)|
|VLABench|2412.18194|mahjong-tile manipulation scene (embedded raster, pp.1–8)|
|Habitat 3.0|2310.13724|human–robot collaboration scene (embedded raster, pp.1–8)|
|**Open-loop world-**|**model & video**|**-generation evaluation**|
|EVA-Bench|2410.15461|embodied-anticipation scene (rep. figure, pp.1–3)|
|EWMBench|2505.09694|generated-video sample (rep. figure, pp.1–3)|
|Physics-IQ|2501.09038|physical-realism sample (rep. figure, pp.1–3)|
|Physion|2106.08261|Fig. 1 example-scenario frames (p.3)|
|Physion++|2306.15668|physical-prediction scene (rep. figure, pp.1–3)|
|VideoPhy|2406.03520|generated-video sample (rep. figure, pp.1–3)|
|WorldModelBench|2502.20694|generated-video sample (rep. figure, pp.1–3)|
|WorldScore|2504.00983|generated world sample (rep. figure, pp.1–3)|
|VBench-2.0|2503.21755|generated-video sample (embedded raster, pp.1–8)|
|WorldPrediction|2506.04363|procedural-action video frame (embedded raster, pp.1–8)|
|**Prediction-to-actio**|**n bridges**||
|WorldSimBench|2410.18072|video-prediction filmstrip, interactive-eval figure (embedded raster, pp.1–8)|
|World-in-World|2510.18135|closed-loop manipulation scene (embedded raster, pp.1–8)|
|RoboWM-Bench|2604.19092|manipulation rollout scene (embedded raster, pp.1–8)|
|WorldArena|2602.08971|dual-arm manipulation scene (embedded raster, pp.1–8)|


Table 11. **Per-panel provenance for Figure 8.** Every panel is a real subject/scene figure cropped from the benchmark’s own arXiv paper and hyperlinked to its source. Exact figure numbers are given where verified from the paper (e.g. Physion Fig. 1); otherwise the teaser-region basis is noted (“rep. figure, pp.1–3” for tiles reused from the collage pool; “embedded raster, pp.1–8” for the nine gap tiles hand-picked from per-paper candidate contact sheets after a subject/results/neither classification pass). No figure number is invented. Images © their respective authors, reproduced for scholarly review. 

Jena et al. 

34 

|**Benchmark**|**arXiv**|**Panel source (results plot)**|
|---|---|---|
|**Leaderboard & mo**|**del-comparis**|**on charts**|
|World-in-World|2510.18135|task-success / gen-quality leaderboard (embedded raster)|
|EvalCrafter|2310.11440|overall model-ranking bar chart (embedded raster)|
|VideoScore|2406.15252|annotation score-ratio grouped bars (embedded raster)|
|WorldModelBench|2502.20694|VBench-vs-Ours win-rate comparison (embedded raster)|
|**Per-dimension rad**<br>|**ar & multi-me**|**tric**<br>|
|VBench|2311.17982|16-dimension evaluation radar (embedded raster)|
|EWMBench|2505.09694|EWMScore 5-dimension radar (embedded raster)|
|WorldArena|2602.08971|Fig. 1 (p.2): EWMScore ranking bars + evaluation radars|
|**Distributions & co**|**mposition**||
|EvalCrafter|2310.11440|prompt-length histogram (embedded raster)|
|EvalCrafter|2310.11440|meta-type composition pie chart (embedded raster)|
|VBench|2311.17982|prompt word cloud (embedded raster)|


Table 12. **Per-panel provenance for Figure 9.** Every panel is a real results/leaderboard/metric plot cropped from the benchmark’s own arXiv paper and hyperlinked to its source. Exact figure numbers are given where verified from the paper (e.g. WorldArena Fig. 1); otherwise the extraction basis is noted (“embedded raster”). Plots are contain-fitted, not cropped-to-fill, so no bars, axes or radar spokes are cut off. No figure number is invented. A benchmark appears more than once when it reports several evidence types. Images © their respective authors, reproduced for scholarly review. 

|**Benchmark**|**arXiv**|**Source**|**Benchmark**|**arXiv**|**Source**|
|---|---|---|---|---|---|
|**Closed-loop (**|**task-success s**|**uites)**|**Open-loop (world**|**-model & vid**|**eo eval)**|
|LIBERO|2306.03310|Fig. 1 (p.2)|WorldModelBench|2502.20694|rep. figure (pp.1–3)|
|CALVIN|2112.03227|rep. figure (pp.1–3)|Physics-IQ|2501.09038|rep. figure (pp.1–3)|
|Meta-World|1910.10897|rep. figure (pp.1–3)|WorldScore|2504.00983|rep. figure (pp.1–3)|
|ManiSkill2|2302.04659|rep. figure (pp.1–3)|EWMBench|2505.09694|rep. figure (pp.1–3)|
|RoboCasa|2406.02523|rep. figure (pp.1–3)|EVA-Bench|2410.15461|rep. figure (pp.1–3)|
|Habitat 3.0|2310.13724|rep. figure (pp.1–3)|VideoPhy|2406.03520|rep. figure (pp.1–3)|
|ALFRED|1912.01734|rep. figure (pp.1–3)|Physion++|2306.15668|rep. figure (pp.1–3)|
|GemBench|2410.01345|rep. figure (pp.1–3)|Physion|2106.08261|Fig. 1 (p.3)|
|VLABench|2412.18194|Fig. 1 Overview (p.1)|EvalCrafter|2310.11440|rep. figure (pp.1–3)|


Table 13. **Per-tile provenance for Figure 1.** Every tile is a representative figure cropped from the benchmark’s own arXiv paper (page/figure noted; “rep. figure” marks the paper’s teaser-region figure on pp.1–3), reproduced for scholarly review and hyperlinked to its source. Images © their respective authors. 

