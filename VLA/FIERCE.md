---
title: "FIERCE: From Generalist Robot Policies to Fast Specialists via Progress-Failure Feedback"
date: "2026-09-16"
authors: "Runjia Tan; Yuang Tu; Yujie Yan; Lan Yu; Xuesong Tian; Chen Lv"
url: https://arxiv.org/abs/2609.18651
pdf: https://arxiv.org/pdf/2609.18651
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.18651)** / [論文ページ](https://arxiv.org/abs/2609.18651)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **FIERCE: From Generalist Robot Policies to Fast Specialists via Progress–Failure Feedback** 

Runjia Tan<sup>1</sup> , Yuang Tu<sup>1</sup> , Yujie Yan<sup>1</sup> , Lan Yu<sup>2</sup> , Xuesong Tian<sup>2</sup> , Chen Lv<sup>1</sup> 

**_Abstract_ — Generalist robot policies offer useful initialization, but refining compact specialists through limited physical interaction requires informative learning feedback. We present FIERCE, a generalist-initialized reinforcement learning framework centered on a unified, task-adaptive progress–failure evaluator. Its architecture shares an observation–language representation between an observed-progress head and an action-conditioned latent predictor whose past and current predictions feed a causal sequence head for task-failure estimation. Joint supervision from progress and preference labels, synchronized commands and observations, and terminal outcomes trains the evaluator; target-task rollouts support adaptation and calibration. Fixed evaluator snapshots provide progress shaping and failure-risk penalties alongside independently verified terminal rewards, while evaluator and policy updates alternate as new experience is collected. Refinement requires neither continued generalist action queries nor a dedicated target-task simulator or manually annotated dense rewards. Only the compact specialist is retained at deployment. The evaluation separates feedback quality, policylearning efficiency, and deployment cost across simulation and two contact-rich real tasks. Code, model weights, and data-restoration tools are released at https://github.com/ ar-mine/FIERCE.** 

## I. INTRODUCTION 

Generalist robot policies, including vision–language–action models and action-producing world models, provide transferable behavioral priors for manipulation [1]–[3]. For repeated insertion, alignment, and placement, however, broad task coverage is only part of the deployment objective. A policy must respond to local variations while meeting task-specific latency and computational constraints; action chunking does not remove the importance of inference latency [4]. Compact, independently executable specialists provide a complementary deployment choice and can serve as individual reusable skills [5]. Generalist demonstrations can initialize such policies, but the central question is how they continue to improve from their own physical experience. 

Prior work combines imitation and reinforcement learning (RL) to acquire compact experts from generalists [6], while HIL-SERL demonstrates policy improvement through realworld interaction [7]. Our focus is therefore the learning feedback that enables refinement under a limited real-interaction budget, rather than reproducing the generalist more faithfully. Independently verified terminal outcomes establish whether an attempt succeeds, but do not directly annotate which intermediate decisions should change. RL can learn from these outcomes; the question is whether transferable progress 

> 1Nanyang Technological University. 

> 2Guangzhou Cloudbutterfly Technology Co., Ltd. 

and failure predictions can provide more effective feedback when only limited target-task experience is available. 

The difficulty is that local progress and eventual success need not agree. For example, pushing a misaligned connector toward a socket may appear to advance insertion while increasing the chance of jamming. Retracting to realign may temporarily reduce progress yet improve the chance of completing the task. Progress feedback describes how much an observed execution advances the task; prospective failure feedback estimates the risk associated with a proposed action and subsequent execution. A useful learning signal must distinguish these roles while remaining grounded in real transitions and independently verified outcomes. 

Robometer demonstrates that progress and trajectorypreference feedback can transfer across robot experience [8], while Foresight shows that action-conditioned predictive latents can support terminally supervised failure detection [9]. Motivated by these findings, we study a unified, taskadaptive progress–failure evaluator as a feedback interface for specialist learning. The central empirical question is whether learned failure scores add value to progress shaping and terminal rewards during physical refinement. Comparisons with progress-based and terminal-reward learning assess the overall pipeline; a within-architecture ablation isolates the use of the failure penalty while retaining failure-head supervision. 

We introduce FIERCE ( _Failure-Informed Efficient Reinforcement Learning for Compact Experts_ ), a generalistinitialized RL framework for refining compact robot specialists through real-world interaction (Fig. 1). Initialization supplies a compact policy; subsequent improvement uses its own rollouts without requiring further generalist action queries. The framework centers on a task-adaptive, actionconditioned progress–failure evaluator. Its shared encoder feeds an observed-progress head and a latent-prediction pathway with a causal risk readout. Multi-task post-training uses diverse trajectories and audited action-synchronized data; target-task fitting and score calibration refresh this feedback using local successes and failures. Progress increments, a failure-risk penalty, and verified terminal rewards relabel real transitions for RL policy updates. Evaluator and policy updates alternate as new experience becomes available. Targettask learning requires no dedicated simulator, manually annotated dense rewards, or separate sim-to-real policytransfer stage. At deployment, both the generalist and the large evaluator are removed, leaving a standalone specialist. Our contributions are twofold: 

- A unified progress–failure evaluator design with separate observed-progress and action-conditioned predictive 


Fig. 1. **FIERCE learning framework. (1)** Generalist demonstrations and rollouts initialize _πθ_ 0 . **(2)** Real trajectories and independently verified outcomes populate replay; the evaluator supplies progress shaping and action-conditioned failure penalties alongside terminal rewards. The dashed link denotes calibration, and scoring snapshots remain fixed during policy updates. Progress uses observed history; risk also depends on the action prefix, remaining time, and reference continuation in (1). **(3)** Only _πθK_ is deployed; the generalist and evaluator are removed while independent safeguards remain. 

pathways, trained as a refreshable feedback interface for specialist RL. 

- A physical-refinement framework for compact policies initialized from demonstrations, including generalist rollouts, with no continued generalist action queries or dedicated target-task simulator. Deployment retains only the policy; within-architecture comparisons assess failure feedback and evaluator-training stages. 

We assess progress and failure discrimination, feedbackguided policy learning, and the resulting specialists’ taskperformance and inference-cost trade-offs. Alternative-action validity is distinct from these evaluations. 

## II. RELATED WORK 

## _A. Robot Policy Adaptation and Specialization_ 

Robot policy improvement can retain the generalist or learn a separate specialist. In the former route, RECAP improves a VLA using execution experience and expert corrections [10], while RL Token trains a lightweight actor–critic on pretrained VLA representations, retaining the generalist during execution [11]. Generalists themselves also remain strong alternatives: _π_ 0 _._ 7 reports performance comparable to specialized RL policies on selected tasks [12]. Specialization therefore targets a performance–computation trade-off, rather than assuming that a smaller policy is inherently more capable. 

A complementary route uses generalist behavior to support a separate expert. RPD combines behavioral cloning with teacher-action guidance during RL exploration to refine compact task-specific policies [6], establishing that specialization can extend beyond imitation. Real-world refinement is also supported by HIL-SERL, which combines demonstrations, human corrections, and sample-efficient RL for 

precise manipulation [7]. FIERCE uses generalist trajectories for initialization but improves an independently executable specialist without continued generalist action queries. Our focus is the learning feedback needed for this refinement under a limited real-interaction budget. 

## _B. Reward and Failure Modeling for Policy Improvement_ 

Learned rewards provide a route from robot experience to transferable supervision. ReWiND and RoboReward study language-conditioned rewards for policy adaptation and evaluation [13], [14], while VLAC couples progress and completion feedback with real-world RL [15]. Closely related to our progress branch, Robometer combines intra-trajectory progress and inter-trajectory preferences across successful, suboptimal, and failed experience [8]. Its reward model evaluates observed execution without directly conditioning on a proposed action; using failed trajectories for reward learning is thus distinct from predicting candidate-action-conditioned failure risk. 

Predictive representations extend supervision to future value and action consequences. V-JEPA 2 learns action-conditioned latent dynamics for robot planning from video and interaction data [16]. ViVa uses video-generative representations for value estimation [17]. BORA explicitly conditions its critic on VLM features and action chunks for offline value guidance, then refines a frozen VLA through online residual adaptation [18]. These methods establish that forward-looking or actionconditioned guidance is not unique to failure prediction. 

Failure models address a related but different objective: identifying executions likely to fail. FAIL-Detect learns uncertainty-based signals from successful demonstrations [19], while Gauge uses video-world-model features for failure and anomaly classification [20]. SAFE uses VLA internal features 


Fig. 2. **Progress–failure evaluator and general-to-task learning. (a)** Shared history features feed a progress head and an action-conditioned predictor; its prediction history feeds the causal risk head. Dashed links denote training-only supervision, not future observations available at inference. **(b)** Multi-task post-training uses RBM progress/preference examples, audited action-synchronized data, and additional rollouts. Task adaptation and subsequent refreshes inherit the preceding parameters; fixed snapshots provide feedback for policy learning under the conditions in (1). 

for multitask detection [21], whereas Foresight combines action-conditioned predictive latents with a causal detector trained from terminal success/failure labels [9]. We instead use such predictions as training penalties. Whether a failure score ranks alternative actions or remains calibrated after a policy update is a separate empirical question. Risk-aware refinement is itself an established setting: FARL couples a worldmodel-based safety critic with a recovery policy to reduce intervention-requiring failures during online learning [22]. 

FIERCE jointly trains observed-progress and actionconditioned failure pathways as a training-time evaluator, with local adaptation and score-calibration steps. It is not a runtime alarm or recovery controller. The experiments assess progress/failure feedback within this architecture and its use in compact-policy learning. 

## III. FIERCE 

## _A. Setting and Feedback Semantics_ 

For manipulation task _g_ , let _ht_ = ( _o≤t, q≤t, a<t_ ) contain visual observations, proprioception, and executed commands. The decision context is _xt_ = ( _ht, g, bt_ ), where _bt_ = _T_ max _− t_ is the remaining task time. Modules use declared observation windows and retain time information. The command prefix _At_ = ( _at|t, . . . , at_ + _H−_ 1 _|t_ ) is selected before execution for the next replan interval; its realized length _ℓ ≤ H_ is logged. Independently verified terminal outcomes _yτ ∈{_ 0 _,_ 1 _}_ indicate success; unknown outcomes are masked. Action demonstrations _D_ 0 initialize the compact specialist _πθ_ ( _A | x_ ); in the generalist-initialized setting, these are rollouts of _πG_ . The training-time progress–failure evaluator _Mϕ_ supplies feedback for reward construction; a separate RL critic _Qω_ learns action values from the resulting rewards. Refinement uses interaction budget _B_ int, with units specified per experiment. 

Observed progress _p_ ˆ _t_ estimates task advancement from history, not success probability or unexecuted candidate actions. For collection round _k_ , risk is defined relative to 

continuation policy _πk_ = _πθk_ : 


The estimate _f_<sup>ˆ</sup> _t_ concerns eventual failure after executing _At_ and continuing with _πk_ within the remaining task time, not only the next _H_ steps; it is not 1 _− p_ ˆ _t_ . Equation (1) defines the estimation target. In the reported learning experiments, _f_<sup>ˆ</sup> _t_ is used as a risk score, not as an independently verified calibrated probability or causal action effect. FIERCE alternates evaluator adaptation and specialist improvement on real experience, exporting only the compact policy (Fig. 1). 

## _B. Progress–Failure Evaluator Architecture_ 

Our evaluator requires a shared representation for both task-progress estimation and action-conditioned predictive learning. We instantiate this representation with Cosmos 3 Edge, motivated by its development for physical-world understanding and prediction [23]. In our implementation, action conditioning is learned through an external latent predictor, while the progress branch follows Robometer’s progress and preference supervision [8]. Thus, we reuse the supervision principle rather than transferring Robometer’s Qwen-specific prediction heads. 

We instantiate the encoder with Cosmos 3 Edge observation–language representations [23] and attach an external action-conditioned latent predictor (Fig. 2). Robometer provides a supervision formulation, not transferred backbonespecific head weights. With _zt_ = _Eϕ_ ( _ht, g_ ), 


The progress branch evaluates observed state; the risk branch evaluates predicted action consequences. Prediction history contains only predictions formed at decisions no later than _t_ , not subsequently observed frames. The reference _πk_ defines the continuation distribution, not a policy-weight input. Future observations and outcomes provide training supervision only: 

no future RGB is rendered at inference and ground-truth future frames are never prediction inputs. 

## _C. General-to-Task Evaluator Learning_ 

**Data and action restoration.** RBM-1M is a multi-source 

robot-trajectory corpus for progress and preference learning [8]. Its processed video–language examples omit robot actions. We recover logged commands from audited source episodes, including heterogeneous Open X-Embodiment transitions [24], and supplement them with branching/policy rollouts. Restoration aligns parent timestamps, command frames, units, controllers, and gripper conventions. Measured displacement is not a command, and later feedbackdependent actions cannot form a chunk known at _t_ . Unknown action semantics mask action-dependent losses. Rewound or instruction-mismatched videos are preference examples, not verified physical failures. Views, subskills, and windows from one parent episode share a split. 

**General training.** Available fields enable the masked objective 


Progress/preference retain RBM supervision. Dynamics uses _L_ dyn = _∥z_ ˆ _t_ + _H −_ sg( _E_ target( _ot_ + _H_ )) _∥_ 1 with a stop-gradient target encoder. This target requires a fully executed prefix and its future observation. Failure labels separately require that the logged execution and continuation match (1); masking the dynamics loss does not by itself establish that correspondence. For valid queries _Tτ_ , terminal labels train prefix risk: 


Episode normalization limits length bias. These labels identify neither failure onset nor causal actions. Same-state simulator branches, with matched continuation policy and remaining time, supply repeated success estimates _y_ ¯ _i_ . Clearly ordered pairs add 

For a real transition of length _ℓ_ , let _dt_ denote true task termination and Φ _ϕ_ ( _ht, g_ ) = _p_ ˆ _t_ . A fixed evaluator snapshot gives 


The outcome term is zero at nonterminal transitions. The progress term has discounted potential-difference form with zero terminal potential [27]. Risk and time penalties intentionally change the objective; no policy-invariance claim is made for the full objective. Summed risks are a regularizer, not an episode failure probability or safety guarantee. The coefficient _β_ controls the strength of this penalty, including possible over-conservatism. 

**Iterative refinement.** Each round collects real rollouts, updates/calibrates _Mϕ_ , freezes a versioned snapshot, consistently relabels replay, and updates _πθ_ . Recent-policy outcomes refresh risk; older data preserve progress/dynamics knowledge rather than becoming labels for a new continuation policy. After policy changes, risk remains provisional feedback until refreshed. A SAC-style learner [28] mixes demonstration and online replay following RLPD [29] (Sec. IV-A). _Mϕ_ supplies progress and risk scores for reward construction; the RL critic _Qω_ learns return through Bellman updates with discount _γ_<sup>_ℓ_</sup> and mask _dt_ . Evaluator scoring can run asynchronously outside the control path. 

Success, the declared deadline, or predefined failure terminates a task. Task termination is distinguished from external time-limit truncation [30]. External stops/interventions do not automatically imply failure or termination; unknown outcomes are masked. Bootstrap only from valid pre-reset context when continuation is defined; otherwise exclude the Bellman transition. Independent hardware safeguards remain. 

## IV. EXPERIMENTS 

We evaluate feedback quality (Table I), specialist performance and deployment efficiency (Table II), and component contributions to learning (Table III). 

## _A. Experimental Setup_ 


where _ℓf_ is the failure logit. Unrelated states with similar progress are not counterfactual pairs. 

**Task adaptation.** Low-rank adapters [25] and heads fit local successful/failed rollouts; disjoint data fit failure-logit temperature and bias [26]. Insufficient-data settings retain the general calibrator. This is a score-calibration procedure; persistence of probability calibration across policy updates is not established by the reported tests. 

## _D. Evaluator-Guided Specialist Refinement_ 

The specialist has its own visual encoder and action head. Successful generalist trajectories or demonstrations initialize it by BC; failures inform the evaluator. Stored demonstrations may regularize later learning, without further generalist action queries. 

The evaluation spans LIBERO-90 Tasks 6, 28, 33, and 73 [31]; ManiSkill3 StackCube and PegInsertionSide [32]; and real-world _peg-in-hole_ and _cup stack_ on Franka. Real specialists learn through physical interaction; terminal success is verified independently. Reward comparisons use the compactpolicy setup below. The primary within-architecture control retains evaluator supervision and sets the failure-penalty coefficient to zero; external baselines compare complete training pipelines rather than isolate a single architectural factor. Action-free evaluator tests use only images and task text; action-aware tests match command semantics and horizons. OOD refers to documented evaluator-training exclusions, not verified exclusion from foundation pretraining. 

Simulation policies initialize from 50 successful demonstrations. The horizons shown in Fig. 4 are 100k steps for Tasks 6 and 28, 300k for Task 33, and 120k for Task 73. StackCube and PegInsertionSide use displayed horizons of 250k and 

TABLE I 

PROGRESS AND FAILURE PREDICTION. **A:** ACTION-FREE OOD PROGRESS AND TRAJECTORY-QUALITY ORDERING (VOC AND KENDALL’S _τa_ ). **B:** VLABENCH FAILURE DISCRIMINATION OVER THREE HELD-OUT TASK SPLITS; 50%-PREFIX AUROC USES THE LAST COMPLETE QUERY BLOCK BY THE MIDPOINT. HIGHER IS BETTER; THESE METRICS DO NOT MEASURE PROBABILITY CALIBRATION. _†_ : REPORTED BY ROBOMETER [8]. _‡_ : EVALUATION UNDER THIS WORK’S VLABENCH PROTOCOL, NOT SCORES QUOTED FROM THE ORIGINAL BENCHMARKS. _§_ : ARCHIVED SCORES NOT REPRODUCED IN A CPU RERUN; SEE SEC. IV-B. 

|A. OOD progress / qu|ality orde|ring|B. He|ld-out-task failure <br>Rollout AUROC|prediction<br>Prefix AUROC||
|---|---|---|---|---|---|---|
|Model|VOC _↑_|_τa ↑_|Model|_↑_|@50% _↑_|BalAcc _↑_|
|ReWiND<sup>_†_</sup>|0.51|0.01|FAIL-Detect/logpZO<sup>_‡_</sup>|0.577|0.654|0.557|
|RoboReward-4B|0.84|0.51|RND (two-head)<sup>_‡_</sup>|0.763|0.652|0.616|
|Robometer-4B|0.94|0.64|SAFE-LSTM<sup>_‡,§_</sup>|0.733|0.577|0.571|
|Cosmos-Reward (V+L)|0.95|0.47|Gauge<sup>_‡_</sup>|0.799|0.612|0.603|
|Cosmos-Reward-Cont.|0.94|0.38|Foresight-Transformer<sup>_‡_</sup>|0.807|0.645|0.637|
|FIERCE|**0.96**|**0.66**|FIERCE (full)|**0.822**|**0.693**|**0.648**|


Fig. 3. **Progress and failure feedback during peg-in-hole execution. (a)** Successful and **(b)** failed runs show selected frames with their timestamps, progress estimates (FIERCE, Robometer), and failure scores (FIERCE, Foresight). Later frames document outcomes, not prediction inputs. The 0.8 line is a displayed score reference; marked threshold crossings are offline diagnostics, not independently verified terminal failures or online recovery commands. Shared-threshold crossings alone do not establish matched false-alarm rates or calibrated detection lead times. 

300k steps. The BC-initialized RLPD-SAC actor uses a frozen DINOv2-small encoder [33], proprioception, and three 512unit hidden layers with LayerNorm; the proposed horizon is four seven-dimensional actions. Robometer is frozen, with isotonic calibration on a fixed 10-demonstration subset. All task-training conditions use seed 7, giving one training run per task and condition. The two-task LIBERO protocol uses 200 final trials per run (10 initial states, 20 repeats); this does not specify test counts for the remaining tasks or measure variation across training runs. The plotted bands have no documented aggregation unit and are not used as inferential uncertainty. Results are descriptive single-run comparisons; no training-seed significance claim is made. 

The real-task protocol uses 300 refinement rollouts per condition and evaluation every 30 rollouts. Tables II and III share final-success values where conditions overlap. The 300rollout figure specifies refinement, not the complete cost of initialization, adaptation, calibration, evaluation, resets, or interventions. It does not establish equal total target-task data use or robot operating time across methods. 

## _B. Evaluator Generalization and Failure Prediction_ 

**Protocol.** Table IA compares action-free progress and quality ordering using VOC on successful trajectories and Kendall’s _τa_ . ReWiND values are reproduced from Robometer [8]; other entries come from archived evaluation artifacts. The FIERCE checkpoint is selected on development-set failure BCE subject to reward retention. Table IB uses three fixed VLABench [34] task splits held out from detector training. Baselines include an adapted random-network-distillation detector [35]; its two-head implementation is distinct from the original exploration objective. Rollout AUROC uses each execution’s maximum score; 50%-prefix AUROC uses the last complete query block by half of its actual steps. Balanced accuracy averages conformal levels _α ∈{_ 0 _._ 15 _,_ 0 _._ 20 _,_ 0 _._ 25 _}_ within each split, then across splits. This follows a Foresightstyle protocol [9], not an exact reproduction of its datasets or calibration selection. 

**Prediction quality.** FIERCE reaches VOC/ _τa_ of 0.96/0.66 versus Robometer’s 0.94/0.64. Rollout AUROC is 0.822 versus 0.807 for Foresight-Transformer. Prefix AUROC is 


Fig. 4. **Evaluator-guided policy learning. (a–d)** LIBERO Tasks 6, 28, 33, and 73; **(e,f)** ManiSkill3 StackCube and PegInsertionSide; **(g,h)** real peg-in-hole and cup stack. Success fractions are plotted against environment steps for simulation and refinement rollouts for the real tasks; horizons are task-specific. The four conditions are full FIERCE, Robometer-guided RL, FIERCE without its failure penalty ( _β_ = 0, retaining failure supervision), and sparse terminal reward. Training uses seed 7; bands are not across-training-seed uncertainty estimates (see Sec. IV-A). 

0.693 versus the strongest baseline value of 0.654 (FAILDetect/logpZO), a difference of 0.039; the difference from Foresight-Transformer (0.645) is 0.048. Balanced accuracy is 0.648 versus 0.637 for Foresight-Transformer. These scores measure outcome discrimination, not probability calibration or alternative-action ranking. Archived scores and differing inference backends limit cross-method attribution; the flagged SAFE-LSTM entry was not reproduced by a CPU rerun. The gaps are not significance estimates. Fig. 3 illustrates the intended distinction between observed progress and prospective risk. 

## _C. Specialist Learning and Deployment_ 

The four reward conditions are sparse terminal reward, Robometer-guided RL, FIERCE without its failure penalty, and full FIERCE. The full and no-penalty conditions share the compact actor, evaluator supervision, terminal/time terms, and nominal refinement budget; the latter sets only _β_ = 0. This tests using the learned risk penalty within the same architecture, not the value of joint representation learning. Robometer is frozen in the specified simulation setup, so that comparison also changes evaluator adaptation and measures a pipeline-level difference. Progress versus sparse rewards is a sanity check; it is not a new claim that dense rewards can help RL. 

Table IIA reports success on the two real tasks. The taskadapted generalist uses successful-rollout SFT, not VLA RL. In the reported seed-7 runs, full FIERCE averages 92% success, versus 83% for Robometer-guided RL and 85% without the failure penalty. Per-checkpoint test counts and the alignment of Fig. 4 with the table summaries are not fully documented; the reported AUC and threshold costs are 

#### TABLE II 

POLICY SUCCESS AND END-TO-END LATENCY. **A:** PEG-IN-HOLE/CUP STACK SUCCESS RATES AND THEIR EQUAL-TASK MEAN. **B:** MEAN OF TASK-LEVEL P95 OBSERVATION-TO-ACTION LATENCIES (MS) ACROSS FOUR LIBERO, TWO MANISKILL3, OR TWO REAL TASKS, MEASURED ON AN INTEL CORE I9-12900K CPU AND NVIDIA RTX 5090 GPU. _†_ DENOTES THE ORIGINAL/ADAPTED MODEL-PAIR MEAN, NOT AN INDIVIDUAL MODEL’S LATENCY. 

### **A. Real-task performance** 

|**Policy / training signal**|**Su**|**ccess (%)** _↑_||
|---|---|---|---|
||Peg-in-<br>hole|Cup<br>stack|Mean|
|_Generalist policies_||||
|Original _π_0_._5|40|50|45.0|
|Task-adapted _π_0_._5|78|82|80.0|
|_Standalone compact policies_||||
|BC initialization only|30|38|34.0|
|Robometer-guided RL|80|86|83.0|
|FIERCE w/o failure penalty|82|88|85.0|
|**FIERCE (full)**|**91**|**93**|**92.0**|


|**B. Task-averaged **|**end-to-end **|**P95 (ms)** _↓_||
|---|---|---|---|
|**Policy / timing condition**|LIBERO|ManiSkill3|Real|
|Original _π_0_._5|88.684|88.023||
|Original/adapted mean<sup>_†_</sup>|||94.315|
|BC initialization only|11.678|11.855|21.743|
|Robometer-guided RL|11.715|11.232|21.343|
|**FIERCE (full)**|11.333|11.234|21.923|


TABLE III 

COMPONENT CONTRIBUTIONS TO SPECIALIST LEARNING. PEG-IN-HOLE AND CUP STACK USE THE SAME COMPACT ACTOR ARCHITECTURE AND A 300-ROLLOUT REFINEMENT BUDGET PER TASK. **A:** FEEDBACK-DESIGN ABLATIONS. **B:** EVALUATOR-TRAINING ABLATIONS. HIGHER FINAL SUCCESS AND LEARNING-CURVE AUC, AND LOWER _N_ 80, ARE PREFERRED. 

|**Variant**||**Peg-in-hole**|||**Cup stack**||
|---|---|---|---|---|---|---|
||Final success<br>(%) _↑_|Norm. AUC<br>[0_,_1] _↑_|_N_80<br>(rollouts) _↓_|Final success<br>(%) _↑_|Norm. AUC<br>[0_,_1] _↑_|_N_80<br>(rollouts) _↓_|
|**FIERCE (full)**|**91**|**0.733**|**185**|**93**|**0.786**|**147**|
|_A. Feedback design_|||||||
|w/o failure penalty (_β_ = 0)|82|0.634|270|88|0.705|206|
|w/o candidate-action conditioning|78|0.598|NR|84|0.674|NR|
|w/o action-ranking loss (_λa_ = 0)|88|0.706|186|91|0.762|152|
|_B. Evaluator training procedure_|||||||
|w/o general evaluator post-training (G)|74|0.550|NR|81|0.632|NR|
|w/o initial task adaptation (T)|77|0.581|NR|85|0.691|NR|
|Frozen task evaluator (no P refresh)|83|0.684|213|89|0.754|154|


_Notes._ AUC is trapezoidal area under the success-fraction learning curve divided by 300, not detection AUROC. _N_ 80 is the first 30-rollout evaluation checkpoint reaching 80% success, without interpolation; NR means unreached within budget. Shared final successes match Table IIA. Ablation definitions are in the text. 


Fig. 5. **Real-task success–latency comparison.** Success equally averages peg-in-hole and cup stack (Table IIA); latency averages their end-to-end P95 values on the stated hardware (Table IIB). Original and task-adapted _π_ 0 _._ 5 share the reported 94.315 ms model-pair mean on the horizontal axis; their individual latencies are not supplied. This plot does not measure task throughput. 

therefore descriptive, not independently reconstructed from the displayed traces. 

Table IIB reports task-averaged end-to-end P95 latency: four LIBERO tasks, two ManiSkill3 tasks, and peg-inhole/cup stack. Each entry averages per-task P95 values, rather than pooling queries before taking a percentile. All timings use the i9-12900K/RTX 5090. The 94.315 ms Real entry is the original/adapted _π_ 0 _._ 5 model-pair average; Fig. 5 assigns that aggregate coordinate to both markers, not individual model measurements. FIERCE’s 21.923 ms is close to BConly’s 21.743 ms and Robometer-guided RL’s 21.343 ms. Low inference cost primarily follows from the shared compact actor and removal of the evaluator at deployment; it is not evidence that failure feedback accelerates inference, evaluator 

## training, or task throughput. 

## _D. Component Ablations_ 

Table III separates feedback design from evaluator training, using the same actor and per-task budget. Final success is evaluated at 300 rollouts; normalized AUC is the trapezoidal area under the success-fraction curve divided by 300, not a detection AUROC. _N_ 80 is the first evaluated checkpoint reaching 80% success, without interpolation; NR denotes censoring, not a cost of 300. Real-task _N_ 80 counts rollout checkpoints and is not pooled with simulation environmentstep budgets. 

**Definitions.** Setting _β_ = 0 removes only the risk penalty, retaining failure-head training and terminal reward. The no-action variant retrains the evaluator without candidate commands; actor actions remain unchanged. This is an evaluator-configuration ablation: retraining can change shared features and auxiliary objectives, so its effect cannot be attributed solely to removing one risk-head input. Setting _λa_ = 0 removes ranking supervision while retaining branch data for other valid losses. Skipping G retains the foundation checkpoint and T/P; skipping initial T retains the general calibrator, local replay, and later P refreshes. The frozen variant completes T, then fixes _Mϕ_ and its calibrator while the actor and RL critic _Qω_ continue learning. These ablations compare configurations within the same nominal refinement budget, not an equalized end-to-end data or computation budget. 

For full versus _β_ = 0, final success is 91%/93% versus 82%/88%, and _N_ 80 is 180/150 versus 270/210 on peg/cup. These observations support using risk feedback in the reported runs. The no-action configuration performs worse than _β_ = 0, but the present experiments do not identify the cause of that difference. 

## V. DISCUSSION AND CONCLUSION 

FIERCE uses a unified progress–failure evaluator as a training-time interface for compact-policy refinement. Observed-progress estimation and action-conditioned latent prediction provide different learning signals; local adaptation and refreshes fit them to new execution data. The reported within-architecture ablation favors using the failure penalty on both real tasks, while deployment retains only the compact actor. These are single-seed observations, not evidence of robustness to retraining or reduced total robot operating cost. 

The study does not isolate parameter sharing from independently trained progress and failure models, and its discrimination and RL metrics do not establish policy-wise probability calibration or same-state alternative-action ranking. Risk penalties can discourage useful corrective actions; policy shift and hidden contact states remain limitations. We claim no formal safety, optimal-policy invariance, or early-recovery guarantee. The latency measurement concerns the deployed actor, not evaluator compute or successful task throughput. Data, weights, restoration tools, split manifests, and evaluation scripts will be released subject to source licenses. 

## ACKNOWLEDGMENTS 

**Generative-AI assistance.** ChatGPT (OpenAI) supported drafting and editing (Abstract, Sections I–V and captions); code development, debugging, experiment planning and analysis scripts (Sections III–IV); and initial figure/layout and illustrative-asset prototyping. The authors retain responsibility for the code, measurements and conclusions. 

## REFERENCES 

- [1] D. Ghosh, H. R. Walke, K. Pertsch _et al._ , “Octo: An open-source generalist robot policy,” in _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- [2] Physical Intelligence, K. Black, N. Brown _et al._ , “ _π_ 0 _._ 5: A visionlanguage-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [3] S. Ye, Y. Ge, K. Zheng _et al._ , “World action models are zero-shot policies,” _arXiv preprint arXiv:2602.15922_ , 2026. 

- [4] K. Black, M. Y. Galliker, and S. Levine, “Real-time execution of action chunking flow policies,” _arXiv preprint arXiv:2506.07339_ , 2025. 

- [5] R. Tan, S. Lou, Y. Zhou, and C. Lv, “Multi-modal LLM-enabled long-horizon skill learning for robotic manipulation,” in _2024 IEEE International Conference on Cybernetics and Intelligent Systems (CIS) and IEEE International Conference on Robotics, Automation and_ 

   - _Mechatronics (RAM)_ . IEEE, 2024, pp. 14–19. 

- [6] T. Jülg, W. Burgard, and F. Walter, “Refined policy distillation: From VLA generalists to RL experts,” _arXiv preprint arXiv:2503.05833_ , 2025. 

- [7] J. Luo, C. Xu, J. Wu, and S. Levine, “Precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning,” _arXiv preprint arXiv:2410.21845_ , 2024. 

- [8] A. Liang, Y. Korkmaz, J. Zhang _et al._ , “Robometer: Scaling generalpurpose robotic reward models via trajectory comparisons,” _arXiv preprint arXiv:2603.02115_ , 2026. 

- [9] H. Zhang, Y. Lu, B. Wang _et al._ , “Foresight: Failure detection for long-horizon robotic manipulation with action-conditioned world model latents,” _arXiv preprint arXiv:2606.23085_ , 2026. 

- [10] Physical Intelligence, “ _π_ 0<sup>_∗_</sup> _._ 6<sup>:AVLAthatlearnsfromexperience,”</sup> _arXiv preprint arXiv:2511.14759_ , 2025. 

- [11] C. Xu, J. T. Springenberg, M. Equi _et al._ , “RL Token: Bootstrapping online RL with vision-language-action models,” _arXiv preprint arXiv:2604.23073_ , 2026. 

- [12] Physical Intelligence, “ _π_ 0 _._ 7: A steerable generalist robotic foundation model with emergent capabilities,” _arXiv preprint arXiv:2604.15483_ , 2026. 

- [13] J. Zhang, Y. Luo, A. Anwar _et al._ , “ReWiND: Language-guided rewards teach robot policies without new demonstrations,” in _Proceedings of the 9th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, vol. 305. PMLR, 2025, pp. 460–488. 

- [14] T. Lee, A. Wagenmaker, K. Pertsch, P. Liang, S. Levine, and C. Finn, “RoboReward: General-purpose vision-language reward models for robotics,” _arXiv preprint arXiv:2601.00675_ , 2026. 

- [15] S. Zhai, Q. Zhang, T. Zhang _et al._ , “A vision-language-action-critic model for robotic real-world reinforcement learning,” _arXiv preprint arXiv:2509.15937_ , 2025. 

- [16] M. Assran, A. Bardes, D. Fan _et al._ , “V-JEPA 2: Self-supervised video models enable understanding, prediction and planning,” _arXiv preprint arXiv:2506.09985_ , 2025. 

- [17] J. Lv, H. Li, J. Li _et al._ , “ViVa: A video-generative value model for robot reinforcement learning,” _arXiv preprint arXiv:2604.08168_ , 2026. 

- [18] Z. Chen, Y. Han, Y. Shao _et al._ , “BORA: Bridging offline reinforcement learning and online residual adaptation for real-world dexterous VLA models,” _arXiv preprint arXiv:2605.30226_ , 2026. 

- [19] C. Xu, T. K. Nguyen, E. Dixon _et al._ , “Can we detect failures without failure data? uncertainty-aware runtime failure detection for imitation learning policies,” in _Proceedings of Robotics: Science and Systems_ , 2025. 

- [20] M. Ho, M. F. Ginting, I. R. Ward _et al._ , “World model failure classification and anomaly detection for autonomous inspection,” _arXiv preprint arXiv:2602.16182_ , 2026. 

- [21] Q. Gu, Y. Ju, S. Sun _et al._ , “SAFE: Multitask failure detection for vision-language-action models,” in _Advances in Neural Information Processing Systems_ , vol. 38, 2025. 

- [22] H. Li, K. Lei, S. Zang _et al._ , “Failure-aware RL: Reliable offlineto-online reinforcement learning with self-recovery for real-world manipulation,” _arXiv preprint arXiv:2601.07821_ , 2026. 

- [23] NVIDIA, “Cosmos 3: Omnimodal world models for physical AI,” _arXiv preprint arXiv:2606.02800_ , 2026. 

- [24] Open X-Embodiment Collaboration, “Open X-embodiment: Robotic learning datasets and RT-X models,” _arXiv preprint arXiv:2310.08864_ , 2023. 

- [25] E. J. Hu, Y. Shen, P. Wallis _et al._ , “LoRA: Low-rank adaptation of large language models,” _arXiv preprint arXiv:2106.09685_ , 2021. 

- [26] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, “On calibration of modern neural networks,” in _Proceedings of the 34th International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, vol. 70. PMLR, 2017, pp. 1321–1330. 

- [27] A. Y. Ng, D. Harada, and S. J. Russell, “Policy invariance under reward transformations: Theory and application to reward shaping,” in _Proceedings of the Sixteenth International Conference on Machine Learning_ . Morgan Kaufmann, 1999, pp. 278–287. 

- [28] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” in _Proceedings of the 35th International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, vol. 80. PMLR, 2018, pp. 1861–1870. 

- [29] P. J. Ball, L. Smith, I. Kostrikov, and S. Levine, “Efficient online reinforcement learning with offline data,” in _Proceedings of the 40th International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, vol. 202, 2023, pp. 1577–1594. 

- [30] F. Pardo, A. Tavakoli, V. Levdik, and P. Kormushev, “Time limits in reinforcement learning,” in _Proceedings of the 35th International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, vol. 80, 2018, pp. 4045–4054. 

- [31] B. Liu, Y. Zhu, C. Gao _et al._ , “LIBERO: Benchmarking knowledge transfer for lifelong robot learning,” _arXiv preprint arXiv:2306.03310_ , 2023. 

- [32] S. Tao, F. Xiang, A. Shukla _et al._ , “ManiSkill3: GPU parallelized robotics simulation and rendering for generalizable embodied AI,” in _Robotics: Science and Systems_ , 2025. 

- [33] M. Oquab, T. Darcet, T. Moutakanni _et al._ , “DINOv2: Learning robust visual features without supervision,” _arXiv preprint arXiv:2304.07193_ , 2023. 

- [34] S. Zhang, Z. Xu, P. Liu _et al._ , “VLABench: A large-scale benchmark for language-conditioned robotics manipulation with long-horizon reasoning tasks,” _arXiv preprint arXiv:2412.18194_ , 2024. 

- [35] Y. Burda, H. Edwards, A. Storkey, and O. Klimov, “Exploration by random network distillation,” _arXiv preprint arXiv:1810.12894_ , 2018. 

