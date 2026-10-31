---
title: "H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model"
date: "2026-02-11"
authors: "Jinbang Huang; Wenyuan Chen; Zhiyuan Li; Oscar Pang; Xiao Hu; Lingfeng Zhang"
url: https://arxiv.org/abs/2602.11291
pdf: https://arxiv.org/pdf/2602.11291
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.11291)** / [論文ページ](https://arxiv.org/abs/2602.11291)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **H-WM: Robotic Task and Motion Planning Guided by Hierarchical World Model** 

Jinbang Huang<sup>1</sup><sup>_∗_</sup> , Wenyuan Chen<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Zhiyuan Li<sup>1</sup><sup>_,_2</sup> , Oscar Pang<sup>1</sup><sup>_,_2</sup> , Xiao Hu<sup>1</sup> , Lingfeng Zhang<sup>1</sup> , Yuanzhao Hu<sup>1</sup><sup>_,_3</sup> , Mark Coates<sup>4</sup> , Tongtong Cao<sup>1</sup> , Xingyue Quan<sup>1</sup> , Zhanguang Zhang<sup>1</sup> , Yingxue Zhang<sup>1</sup> 

**_Abstract_ — World models are becoming central to robotic planning and control by predicting future state transitions. Existing approaches mainly rely on visual, latent, or language prediction, which can be difficult to ground in executable robot actions and prone to compounding errors over long horizons. In contrast, traditional robotic task and motion planning enables structured long-horizon reasoning through compact symbolic representations of world transitions, but typically lacks synchronized visual prediction. We propose Hierarchical World Model (H-WM), which jointly predicts logical and visual state transitions by combining a high-level logical world model with a low-level visual world model. The predicted logical actions and latent visual state transitions are jointly incorporated into Vision–Language–Action (VLA) models as intermediate state guidance for long-horizon task execution. Experiments on three long-horizon benchmarks and real robots show that H-WM consistently improves VLA’s performance by stabilizing longhorizon execution and mitigating error accumulation. We also construct LIBERO-Logic, a frame-level aligned dataset that pairs visual observations and continuous robot states with logical actions and predicate-based logical states.** 

## I. INTRODUCTION 

Recent advances in VLA models have enabled robotic systems that tightly couple multi-modal perception and control via large pre-trained foundation models, achieving stronger generalization than traditional modular pipelines. However, most existing VLA methods adopt an end-to-end paradigm that maps visual observations and language instructions directly to low-level actions, resulting in degraded performance on long-horizon tasks [1]. This failure is driven by compounding execution errors, ambiguous goal specifications, limited intermediate supervision, and overfitting to taskspecific representations. 

A natural response to these limitations is to introduce richer intermediate guidance; however, existing approaches fall into three dominant paradigms, each with unsolved shortcomings. First, LLM-based hierarchical planners decompose tasks into subgoals or action sequences [2], but are fundamentally constrained by language as the intermediate interface: LLMs struggle to reason about physical constraints, and their vague, unstructured representations lead to semantic–execution misalignment [2], [3]. Second, world-model-based approaches aim to provide predictive visual guidance [4], [5], yet existing formulations suffer from long-horizon settings where compounding prediction 

> 1Huawei Noah’s Ark Lab, 2University of Toronto, 3 University of British Columbia, 4 McGill University, _∗_ Equal contribution, Correspond to: jinbang.huang.work@gmail.com, _{_ zhanguang.zhang, yingxue.zhang _}_ @huawei.com 

errors degrade planning reliability. Third, classical Task and Motion Planning (TAMP) achieves long-horizon consistency through explicit logical world models for symbolic reasoning [6], but relies on manually designed abstractions and engineered symbolic representations that are weakly aligned with raw visual observations, resulting in brittleness to perception noise and difficulty in scaling to unstructured environments [7]. Consequently, none of these paradigms delivers the informative, grounded, and long-horizon–robust guidance required for reliable VLA execution. 

In this paper, we propose a novel hierarchical world model (H-WM) that couples long-horizon symbolic reasoning with perceptually grounded visual prediction to provide intermediate guidance for VLA models. First, a logical world model predicts structured action–state transitions and searches over candidate symbolic trajectories, promoting logically consistent task progression through trajectory evaluation and explicit goal-progress scoring. Second, a latent visual world model conditions on each selected logical transition and predicts the terminal visual representation of the corresponding subtask, avoiding autoregressive visual rollouts. The predicted logical action and visual subgoal are then jointly injected into a guided VLA for continuous low-level execution. Together, H-WM bridges high-level task reasoning and lowlevel perceptual control without requiring dense pixel-level prediction over the full task horizon. To summarize, our key contributions are: **(1)** A hierarchical world-modeling framework that combines symbolic transitions with visual subgoal prediction to ground robot execution. **(2)** A logic-conditioned latent visual world model that directly predicts the visual representation of a subtask’s terminal state from the predicted logical transition. **(3)** A guided VLA architecture that jointly incorporates logical actions and predicted visual subgoals for continuous low-level execution. **(4)** LIBERO-Logic, a robot manipulation dataset providing frame-level alignment among RGB observations, continuous robot states, logical actions, and logical states. 

## II. RELATED WORK 

## _A. World Model_ 

World models are powerful paradigms for robotics. Recent work has shown their effectiveness across a range of robotic settings, including policy learning [8], [9], policy evaluation [10], [11], test-time rollout simulation [12], [13], and unified model–policy training [14]–[16]. World models 


Fig. 1. **Overview of H-WM and guided VLA execution.** H-WM jointly models logical and visual transitions at the subtask level _m_ , while the VLA performs low-level control at the higher-frequency time step _t_ . The logical world model searches and evaluates candidate transitions to predict the next logical action _am_ +1 and logical state _Xm_ +1. Conditioned on the current observation _obsm_ , robot configuration _qm_ , _am_ +1, and _Xm_ +1, the visual world model uses an understanding expert and a prediction expert to generate the latent visual subgoal _f_ pred<sup>_m_+1. During execution, the understanding expert encodes</sup> _obst_ and _am_ +1, while the goal expert processes _f_ pred<sup>_m_+1.Theactionexperttakes</sup><sup>_qt_andnoisyactiontokens,attendstobothrepresentations,andgenerates</sup> the low-level action chunk _α_ ˆ<sup>_t_</sup> _m_<sup>:</sup><sup>_t_+</sup><sup>_k_</sup> , grounding long-horizon logical guidance into visually conditioned robot execution. 

enable reliable future reasoning and can generate largescale multi-modal data [14]–[16]. Recent systems further demonstrate that world models can be directly adapted for action generation [17]. Most existing approaches focus on pixel-level world modeling, yet real-world dynamics can be captured at multiple abstraction levels. Lower-level representations offer high expressivity but suffer from poor sample efficiency and generalization [18], [19], whereas higherlevel abstractions exhibit the opposite trade-off [20], [21]. Achieving a balance across levels remains challenging [22]. 

## _B. Vision–Language–Action Models_ 

VLA models enable direct mapping from visual observations and language instructions to robotic actions and have become a dominant paradigm for general-purpose robot control [23], [24]. End-to-end VLA models directly generate low-level actions from multi-modal inputs via large-scale pretraining [25]–[28], but suffer from performance degradation on long-horizon tasks due to goal ambiguity and error accumulation [1]. Hierarchical methods mitigate this issue by introducing intermediate guidance [4]. Prior work explores various guidance such as keypoints [29], [30], language [2], and visual predictions [3], [31]. While these approaches improve robot control stability and instruction following, they remain vulnerable to error propagation over time and struggle with long-horizon tasks. 

## _C. Task and Motion Planning_ 

Task and motion planning (TAMP) integrates symbolic reasoning with motion generation to solve multi-step tasks under physical constraints [6], but often suffers from limited scalability. To address this, prior work has explored imitation learning to accelerate planning [7], [32] and reinforcement learning to enhance adaptability in dynamic environments [33], [34]. More recently, LLM-based TAMP has leveraged language priors to guide planning [35]–[37]. Another line of work attempts to learn planning domains to improve scalability [38]–[45], but primarily focuses on abstract world modeling without visual grounding. A framework that jointly captures logical and visual dynamics to enable simultaneous prediction of logical transitions and visual observations remains lacking. 

III. PRELIMINARY 

## _A. Symbolic Task Formalization_ 

We represent the logic-level structure of a robot manipulation task using a PDDL-style symbolic formulation. A symbolic domain is defined as _D_ = ( _P, A_ ) _,_ where _P_ is a finite set of predicate symbols and _A_ is a set of parameterized action schemas. Given the objects _O_ = _{o_ 1 _, . . . , on}_ in a task instance, grounding the predicates in _P_ with compatible objects produces the set of ground atoms _G_ = � _p_ ( _oi_ 1 _, . . . , oik_ ) �� _p ∈P, oij ∈O_ � _,_ where _k_ is 

the arity of predicate _p_ . A logical state is represented by the subset of ground atoms that are true, _X ⊆G._ Similarly, grounding an action schema in _A_ produces a logical action _a_ , which describes a semantic robot subtask such as picking an object, placing it into a receptacle, or closing a drawer. 

A long-horizon task is specified by an initial logical state _X_ 0 and a goal logical state _XG ⊆G_ . We decompose its execution into a sequence of _M_ symbolic transitions, _a_ 1 _a_ 2 _aM X_ 0 _−→X_ 1 _−→· · · −−→XM ,_ where _m_ indexes symbolic subtask boundaries. At boundary _m_ , _Xm_ denotes the current logical state, _am_ +1 denotes the next logical action, and _Xm_ +1 denotes the state expected after successfully completing that action. The corresponding one-step transition can therefore be written as _Xm −−−→Xam_ +1 _m_ +1 _._ A task is completed when the terminal state satisfies the goal, i.e., _XG ⊆XM ._ 

In classical PDDL planning, each action schema is associated with preconditions and add/delete effects, and the successor state is computed using a deterministic transition function. In our formulation, the transition dynamics are instead learned from annotated robot trajectories. Given the current state, task goal, and preceding symbolic trajectory, the logical world _X_ ˆ<sup>(</sup><sup>_i_)</sup> model predicts candidate pairs ( _a_<sup>(</sup> _m_<sup>_i_)</sup> +1<sup>_,_</sup> _X_<sup>ˆ</sup> _m_<sup>(</sup><sup>_i_</sup> +1<sup>)),where</sup> _m_ +1<sup>isthepredictedsuccessorstateassociatedwithcandi-</sup> date action _a_<sup>(</sup><sup>_i_)</sup> _m_ +1<sup>.Aftercandidateevaluationandselection,</sup> we use _am_ +1 and _Xm_ +1 to denote the selected logical action and predicted successor state, respectively. This convention distinguishes candidate predictions used during symbolic search from the selected transition provided to the visual world model and VLA. 

## _B. Visual Subgoal Representation_ 

The symbolic transition specifies what semantic change should occur but does not directly describe the visual and geometric configuration that the robot should reach. We therefore associate each symbolic subtask with a latent visual subgoal. At the beginning of subtask _m_ +1, the robot receives an RGB observation _obsm_ and its current configuration _qm_ . The selected logical action _am_ +1 describes the subtask to execute, while _Xm_ +1 represents its predicted resulting logical state. Together, these variables define the conditioning context _cm_ = ( _obsm, qm, am_ +1 _, Xm_ +1) _._ Let _ϕ_ : _I →F_ be a fixed visual encoder that maps an RGB image from the image space _I_ into a _d_ -dimensional latent feature space _F ⊆_ R<sup>_d_</sup> _._ For each training subtask, _obs_<sup>_m_</sup> goal<sup>+1denotestheterminal</sup> keyframe observed after the successful completion of _am_ +1. Its latent representation, _f_ goal<sup>_m_+1</sup> = _ϕ_ � _obs_<sup>_m_</sup> goal<sup>+1</sup> � _∈F,_ serves as the ground-truth visual subgoal. 

The visual world model predicts the corresponding latent visual subgoal directly from the current multimodal context, 


where _MV_ denotes the visual world model. Rather than predicting every intermediate observation within the subtask, _MV_ predicts only the latent representation of its terminal visual state. Consequently, _f_ pred<sup>_m_+1provides a fixed perceptual</sup> target for low-level control throughout the execution of 

_am_ +1. The framework therefore operates at two temporal resolutions. The subtask index _m_ is used by the logical and visual world models, which are invoked once at each symbolic transition. The control index _t_ denotes the higherfrequency VLA execution steps within the active subtask. Accordingly, _obsm_ and _qm_ refer to the observation and robot configuration at a subtask boundary, whereas _obst_ and _qt_ denote their control-step counterparts. During execution of _am_ +1, the VLA receives the fixed symbolic action and visual subgoal ( _am_ +1 _, f_ pred<sup>_m_+1)whilecontinuouslyupdatingitslow-</sup> level actions from ( _obst, qt_ ). 

## IV. METHODOLOGY 

Building on the symbolic transition and visual-subgoal formulation above, H-WM consists of a logical world model, a logic-conditioned visual world model, and a guided VLA policy. 

## _A. Logical World Model_ 

The logical world model enables long-horizon reasoning in symbolic space. Classical TAMP frameworks rely on handcrafted PDDL transition rules [6], which can become brittle when logical state estimates are incomplete or imperfect. We instead model symbolic transitions directly from data. 

We annotate robot trajectories at subtask boundaries with the current logical state _Xm_ , next logical action _am_ +1, resulting logical state _Xm_ +1, observation _obsm_ , and robot configuration _qm_ , forming the LIBERO-Logic dataset with unified transition tuples _⟨Xm, am_ +1 _, Xm_ +1 _, obsm, qm⟩_ . We initialize from a planning-enhanced language model that has been post-trained for symbolic planning through structured reasoning supervision and planning-oriented preference optimization [46]. We further fine-tune it on LIBERO-Logic to obtain the logical world model _ML_ , adapting its generic symbolic planning capability to robot manipulation. 

During inference, _ML_ is instantiated with two complementary roles, the generator _ML_<sup>search</sup> and the evaluator _ML_<sup>eval</sup> . Given the current state _Xm_ , task goal, and preceding symbolic trajectory, _ML_<sup>search</sup> predicts candidate action–state transitions _Cm_ = �� _a_<sup>(</sup> _m_<sup>_i_)</sup> +1<sup>_,_</sup> _X_<sup>ˆ</sup> _m_<sup>(</sup><sup>_i_</sup> +1<sup>)</sup> �� _Ki_ =1<sup>_,_whereeachcan-</sup> didate jointly specifies the next logical action and its predicted resulting state. The model therefore performs learned symbolic rollout rather than applying an externally specified deterministic transition function. 

To reduce error accumulation across long horizons, we perform beam-style search over the predicted transitions. At each search depth, the top- _B_ partial trajectories are retained and each is expanded with _K_ candidate transitions. For a partial trajectory _τ_ , _ML_<sup>eval</sup> predicts a trajectory-consistency score _s_ eval( _τ_ ) that reflects logical validity and compatibility with the task goal. We additionally compute explicit goal progress from the terminal predicted state, 


where _XG_ denotes the goal logical state. Candidate trajectories are ranked by _S_ ( _τ_ ) = _λ_ eval _s_ eval( _τ_ ) + _λ_ goal _s_ goal( _X_ ) _,_ 

and the top- _B_ trajectories are retained for the next expansion. Search terminates when the predicted state satisfies the goal or a maximum symbolic depth is reached. In this way, _ML_ acts jointly as a learned symbolic transition model and a structured trajectory evaluator. 

## _B. Visual World Model_ 

The visual world model provides visually grounded guidance by predicting the latent representation of the next visual subgoal, conditioned on the current observation, predicted logical state, and corresponding logical action. Unlike autoregressive visual world models, we predict only the terminal visual representation of each subtask, avoiding long visual rollouts and reducing error accumulation. 

As shown in Fig. 1, the visual world model adopts a multi-expert architecture comprising an understanding expert and a prediction expert. The understanding expert adopts the PaliGemma VLM backbone of _π_ 0 _._ 5 [28]. We freeze its visual encoder and multimodal projector to extract features from _obsm_ , while Gemma jointly processes these features and the text embeddings of _am_ +1 and _Xm_ +1. The prediction expert is a randomly initialized lightweight transformer. Through unidirectional fused self-attention, its prediction tokens attend to the understanding expert’s representations, with _qm_ , noisy subgoal features, and flow time embedded into the prediction stream. A trainable head _Rθ_ projects its output into a velocity field in PaliGemma’s projected visual feature space. 

During training, the terminal keyframe _obs_<sup>_m_</sup> goal<sup>+1is encoded</sup> as _f_ goal<sup>_m_+1=</sup><sup>_ϕ_(</sup><sup>_obsm_</sup> goal<sup>+1)</sup><sup>_,_where</sup><sup>_ϕ_includesthefrozenvisual</sup> encoder and multimodal projector. We train the prediction expert using the conditional flow-matching objective [28], [47], with terminal visual features replacing action targets. At inference, we integrate the predicted velocity field from Gaussian noise to obtain the visual subgoal _f_ pred<sup>_m_+1.</sup> 

## _C. Injecting Hierarchical World Model Guidance in VLA_ 

The guided VLA extends the _π_ 0 _._ 5 with an additional goal expert for incorporating the visual subgoal predicted by the visual world model. It retains the original understanding and action experts for multimodal state understanding and low-level action generation, while the goal expert provides explicit conditioning on the predicted future visual state. 

At control step _t_ , the understanding expert combines the current observation _obst_ and logical action _am_ +1 to produce the current-state representation _h_<sup>_u_</sup> _t_<sup>.Inparallel,thegoal</sup> expert encodes the fixed latent visual subgoal _f_ pred<sup>_m_+1intoa</sup> goal representation _h_<sup>_g_</sup> _m_<sup>.Theactionexperttakesthecurrent</sup> robot configuration _qt_ and noisy action tokens as inputs and generates an action chunk _αm_ ˆ<sup>_t_:</sup><sup>_t_+</sup><sup>_k_</sup> conditioned on both _h_<sup>_u_</sup> _t_ and _h_<sup>_g_</sup> _m_<sup>.Tointegratethethreeexperts,weextendthebase</sup> VLA’s directional expert interaction with an additional goalto-action pathway. Specifically, the action expert attends to the hidden representations of both the understanding and goal experts through asymmetric cross-attention. Information flows only from the understanding and goal experts to the action expert; reverse attention is disabled. This 

design retains the base VLA’s action-generation mechanism while incorporating both logical and visual guidance. The guided VLA is trained end-to-end using the same conditional flow-matching objective for continuous action generation as _π_ 0 _._ 5 [28]. 

## _D. Subtask Completion and Transition Prediction_ 

During execution, the VLA performs the subtask specified by _am_ +1 toward its predicted visual subgoal. To detect completion, we use a separate predictor initialized from the understanding expert of the trained guided VLA and augmented with a lightweight classification head. At each control step _t_ , a learnable [CLS] token is processed together with the observation tokens from _obst_ and the logical-action tokens from _am_ +1. Through self-attention, this token gathers information from both inputs. Its final hidden representation _h_<sup>cls</sup> _t_ is passed to the classification head to predict the completion probability, _p_<sup>done</sup> _t_ = _σ_ ( _Wh_<sup>cls</sup> _t_<sup>)</sup><sup>_,_where</sup><sup>_σ_denotesthe</sup> sigmoid function. The predictor is fine-tuned using binary cross-entropy loss and evaluated at every VLA control step. Once completion is detected, execution advances to the next symbolic transition, and the visual world model predicts the next visual subgoal. 

## V. EXPERIMENTS 

## _A. Training Dataset_ 

We train our hierarchical world model on two datasets: LIBERO-Logic, which augments the LIBERO dataset [48] with temporally aligned logical annotations at every timestep, and RoboCerebra [49]. For LIBERO-Logic, annotations are generated through a two-stage process. We first replay each episode and use predefined predicate classifiers to infer logical states, identifying logical actions from the corresponding state changes. We then manually inspect the annotations and correct labeling errors. From these frame-level annotations, we extract subtask-boundary transition tuples _⟨Xm, am_ +1 _, Xm_ +1 _, obsm, qm⟩_ , where _m_ indexes symbolic subtask boundaries. For RoboCerebra, we directly adopt the provided task decompositions and standardize the logical actions and predicates across tasks to obtain a consistent symbolic representation. 

## _B. Benchmark and Evaluation_ 

We evaluate H-WM alongside a range of VLA baselines across three long-horizon planning and control benchmarks, including LIBERO-10 [48], RoboCerebra [49], and the customized LIBERO-LoHo. We introduce **LIBERO-LoHo** , a more challenging long-horizon benchmark derived from LIBERO. It contains five tasks with extended manipulation sequences, constructed by increasing the number of manipulated objects and inter-subtask dependencies relative to the original LIBERO tasks. Specifically, **Task 1** is a five-step task that places the front butter and chocolate pudding into the top drawer of a wooden cabinet before closing it. **Task 2** requires placing alphabet soup, butter, and tomato sauce into a basket over six steps. **Task 3** is a six-step task that places alphabet soup, cream cheese, and butter into a wooden tray. **Task** 

TABLE I 

PERFORMANCE ON THE LIBERO-LOHO BENCHMARK. FOR EACH TASK, WE REPORT Q-SCORE AND SUCCESS RATE (IN %). THE BEST RESULTS ARE SHOWN IN **BOLD** , AND THE SECOND-BEST RESULTS ARE <u>UNDERLINED.</u> 

|**Methods**||**Tasks Q-**|**score / Task Succ**|**ess Rate**|||
|---|---|---|---|---|---|---|
||Task 1|Task 2|Task 3|Task 4|Task 5|**Average**|
|H-WM-_π_0_._5 (ours)|**98.0/94.0**|**86.7/60.0**|**74.0/46.0**|70.7<br>/**42.0**|**95.0/82.0**|**84.9/64.8**|
|H-WM-Stable-Diffusion-_π_0_._5|92.7/82.0|80.0/46.0|65.3/30.0|**74.0**/34.0|93.5/80.0|81.1/54.4|
|Logic-guided _π_0_._5|95.3/86.0|84.7/58.0|54.7/16.0|39.3/4.0|92.0/78.0|73.2/48.4|
|LLM-guided _π_0_._5|84.7/54.0|80.7/42.0|68.0<br>/24.0|41.3/4.0|59.5/10.0|66.8/26.8|
|_π_0_._5|66.0/4.0|73.3/24.0|54.7/4.0|44.7/0.0|38.0/0.0|55.3/6.4|
|_π_0|54.0/0.0|62.0/28.0|44.0/0.0|31.3/0.0|34.0/0.0|45.1/5.6|
|X-VLA|48.8/0.0|16.7/0.0|23.3/0.0|33.3/0.0|40.0/0.0|32.4/0.0|
|Gr00t-N1.5|0.0/0.0|30.7/0.0|34.7/0.0|2.7/0.0|0.0/0.0|13.6/0.0|
|OpenVLA-OFT|0.0/0.0|60.0/0.0|17.3/0.0|22.7/0.0|0.0/0.0|20.0/0.0|
|OpenVLA|0.0/0.0|2.7/0.0|24.0/0.0|2.7/0.0|0.0/0.0|5.9/0.0|


**4** requires placing the left black bowl, salad dressing, and chocolate pudding into a wooden tray over six steps. **Task 5** is a seven-step task that places the back butter and chocolate pudding into the top cabinet drawer, closes the drawer, and then places the black bowl on top of the cabinet. Compared with the original LIBERO benchmark, which typically contains 1–3-step tasks, LIBERO-LoHo extends the task horizon to as many as seven steps, enabling a more rigorous evaluation of long-horizon policy performance. We primarily report **Success Rate** , defined as the percentage of tasks completed successfully. For extra-long-horizon benchmarks, including LIBERO-LoHo _(up to 7 steps)_ and RoboCerebra _(up to 20 steps)_ , we additionally report **Q-Score** , defined as the fraction of completed subgoals among all required subgoals. This metric provides a more informative measure of task progress when full task completion remains difficult. 

## _C. Baselines_ 

We evaluate H-WM against two categories of baselines covering both end-to-end VLA learning and hierarchical long-horizon control. For end-to-end VLAs, we compare with _π_ 0 [27], _π_ 0 _._ 5 [28], OpenVLA [26], OpenVLAOFT [50], X-VLA [51], and GR00T [52]. For hierarchical approaches, we include LLM-guided _π_ 0 _._ 5, which uses a language model to decompose the task into natural-language subgoals [2] that are sequentially executed by _π_ 0 _._ 5, and Logic-guided _π_ 0 _._ 5, which decomposes the task into structured PDDL-style logical actions and states and sequentially conditions _π_ 0 _._ 5 on the resulting logical actions without visual-subgoal prediction. These comparisons separate the benefit of hierarchical decomposition from the additional benefit of structured logical guidance and logic-conditioned visual guidance. 

## _D. Implementation Details_ 

For LIBERO-10 and LIBERO-LoHo, all VLA models are trained on the corresponding LIBERO demonstrations. For RoboCerebra, models are trained on the provided training split and evaluated on the ideal test set. The guided VLA 

is initialized from _π_ 0 _._ 5, with the additional goal expert initialized from the Gemma backbone of its understanding expert. We follow its standard training configuration, with a learning rate of 5 _×_ 10<sup>_−_5</sup> and 256 global batch size for 60k steps in PyTorch. The subtask completion predictor is initialized from the PaliGemma backbone of the trained guided VLA, and trained for 10k steps using binary crossentropy loss with the classification head. Baseline methods use publicly released LIBERO fine-tuned checkpoints when available. 

The logical world model is initialized from the planningenhanced Qwen3-4B checkpoint released in [46] and further full-parameter fine-tuned on LIBERO-Logic for 10k optimization steps with a learning rate of 1 _×_ 10<sup>_−_5</sup> and batch size of 16. We follow the training formulation in [46], including the structured planning data format, autoregressive nexttoken objective, and optimization setup, while replacing the original planning data with LIBERO-Logic trajectories. For symbolic search, we use a beam width of _B_ = 3, generate _K_ = 2 candidate transitions per expansion, set _λ_ eval = 0 _._ 5 and _λ_ goal = 0 _._ 5, and limit the maximum search depth to 20 symbolic steps. 

For the visual world model, the visual encoder is instantiated with SigLIP [53], while the multimodal transformer is initialized from the Gemma understanding expert of _π_ 0 _._ 5. The prediction expert is a randomly initialized lightweight Transformer of approximately 300M parameters following the _π_ 0 _._ 5 expert architecture. The projection head uses two fully connected layers with dimensions 1024 _→_ 4096 _→_ 2048. The visual world model is trained for 100k steps with a learning rate of 5 _×_ 10<sup>_−_5</sup> and 256 global batch size. 

## _E. Ablation Studies_ 

To validate the contribution of visual guidance beyond logical reasoning, we use Logic-guided _π_ 0 _._ 5 as a controlled ablation in which the visual world model is removed and only logical guidance is retained. In addition, we replace latent visual prediction with pixel-level terminal-subgoal generation 


Fig. 2. (a) Evaluation results of H-WM-guided _π_ 0 _._ 5 and various VLA baselines on the LIBERO-10 benchmark. (b) Evaluation results of H-WM-guided _π_ 0 _._ 5 and baseline methods on the RoboCerebra benchmark. 

using Stable Diffusion v1.5 [54]. The diffusion model is finetuned on the same subtask-aligned training data, conditioned on the current observation and predicted logical transition, and its generated subgoal image is encoded by the same frozen visual encoder before being provided to the guided VLA for execution. This compares the effectiveness of latent versus pixel-level visual guidance. 

## _F. Real-Robot Experiment._ 

We evaluate H-WM on a UR5e robot with visual observations captured by an Intel RealSense camera. The robot performs an eight-step office-table cleaning task involving multiple sequential pick-and-place operations, which requires both spatial reasoning and consistent task progression over a long horizon. We compare _π_ 0 _._ 5, logic-guided- _π_ 0 _._ 5, and H- WM-guided _π_ 0 _._ 5 under the same setup. All methods are trained using the same 40 manually collected demonstration trajectories and executed through the UR5e control API. Each method is evaluated over 20 real-robot trials, and performance is measured using step-wise success rate to capture both partial task progress and complete longhorizon execution. Logical states are estimated from visual observations using Qwen3-VL-2B with one-shot prompting. 

## VI. RESULTS 

Our experiments aim to answer the following questions: (1) Does H-WM provide effective guidance for downstream VLAs? (2) How does the H-WM-guided VLA compare to baseline approaches and models? (3) How does each level of the world model contribute to the final performance? (4) Is the H-WM framework deployable in real-robot settings? 

**(1) Effectiveness of H-WM guidance:** The results demonstrate that H-WM provides stable and effective guidance for long-horizon tasks across three benchmarks. On LIBERO-LoHo (Table I), H-WM-guided _π_ 0 _._ 5 significantly outperforms _π_ 0 _._ 5, improving success rate by 58.4 percentage points and Q-score by 29.6 points. Similar gains are observed on RoboCerebra (Fig. 2.(b)), with improvements of 12.7 points in Q-score and 9.1 percentage points in success rate. In contrast, _π_ 0 _._ 5 attains relatively high Q-Scores but low Success Rates, often due to missing intermediate steps, ignored instructions, and incorrect action ordering, leading to partial completion but overall failure. On LIBERO-10 (Fig. 2.(a)), H-WM guidance still improves performance, 

though the margin is smaller. This is because LIBERO-10 tasks are much shorter, allowing VLAs to succeed directly. 

**(2) Comparison to Baselines:** H-WM-guided _π_ 0 _._ 5 consistently outperforms all end-to-end VLA baselines on longhorizon tasks (Table I, Fig. 2.(b)). Despite their strong lowlevel manipulation capabilities, end-to-end VLAs struggle to maintain task progress over extended horizons. Without explicit intermediate guidance, they are sensitive to prompt variations and frequently omit required subtasks, execute them in the wrong order, or terminate before satisfying the complete task goal. H-WM mitigates these failures by explicitly predicting and executing a sequence of intermediate transitions. We further compare H-WM with hierarchical methods that decompose the original instruction before VLA execution. LLM-guided _π_ 0 _._ 5 improves over raw VLAs through natural-language task decomposition, but its language subgoals remain ambiguous and do not explicitly track logical state changes. Logic-guided _π_ 0 _._ 5 introduces structured PDDL-based actions and states, improving task ordering and global consistency, but provides no perceptual description of the desired outcome of each subtask. H-WM combines the complementary strengths of both levels: logical transitions maintain globally consistent task progression, while latent visual subgoals provide perceptually grounded targets for low-level control. This joint guidance produces more reliable long-horizon execution than either end-to-end policies or language- and logic-only hierarchical methods. On the shorter-horizon LIBERO-10 benchmark (Fig. 2.(a)), intermediate guidance is less critical; consequently, H-WM shows smaller gains and ranks second overall. 

**(3) Ablation Study:** The ablation results further validate the necessity of bilevel guidance. As shown in Table I, logic-only guidance already surpasses the unguided baseline by 42.0 percentage points in success rate and 17.9 points in Q-score. Incorporating visual guidance yields a further 16.4 percentage-point improvement in success rate and 11.7 points in Q-score. This confirms that visual world modeling provides actionable grounding for symbolic plans, improving alignment between symbolic constraints and perceptual execution. The results on RoboCerebra (Fig. 2.(b)) support the same conclusion. Moreover, the results show that pixellevel image generation is less effective than latent visual features. The H-WM-Stable-Diffusion- _π_ 0 _._ 5 variant replaces 


Fig. 3. (a) Real-world experiment with UR5e robot evaluating H-WM guided _π_ 0 _._ 5 on long-horizon manipulation task. (b) Step-wise success rates in real-robot experiments. 

latent visual prediction with Stable Diffusion-based image generation, yet achieves smaller performance gains than the default H-WM, exhibiting a 10.4% drop in overall success rate. This is likely because pixel-level generation introduces unnecessary visual details and reconstruction noise, whereas latent features provide more compact guidance for VLAs. 

**(4) Real-World Experiment:** The complete real-robot task is illustrated in Fig. 3(a), and the corresponding stepwise success rates are reported in Fig. 3(b). Although _π_ 0 _._ 5 can complete early manipulation steps, its success rate declines rapidly as execution progresses. Logic-guided _π_ 0 _._ 5 improves task progression through structured subtask guidance, but its performance remains limited in later stages, suggesting that logical guidance alone is insufficient for reliable execution. H-WM complements this logical guidance with predicted visual subgoals, providing explicit perceptual targets for each pick-and-place operation. This combination helps connect the intended task progression with the physical configuration required at each stage. Consequently, H-WMguided _π_ 0 _._ 5 maintains higher success rates throughout the later steps and achieves more reliable full-task completion, demonstrating the effectiveness of hierarchical world-model guidance in real-world manipulation. 

## VII. CONCLUSION 

We propose a hierarchical world model (H-WM) that jointly models logical and visual world dynamics to provide bilevel guidance for VLA models in long-horizon robotic tasks. The logical world model captures global task structure and long-term dependencies, while the visual level grounds logical transitions into visually meaningful latent subgoals, enabling stable guidance of VLAs over extended horizons. Experimental results show that H-WM significantly improves long-horizon performance over base VLA models and hierarchical or end-to-end approaches. These findings demonstrate that hierarchical world modeling offers effective and scalable guidance for bridging symbolic reasoning and perceptual grounding in VLA systems. Although the proposed Hierarchical World Model demonstrates strong performance in guiding long-horizon manipulation tasks, several 

limitations remain. H-WM introduces additional training cost and system complexity and assumes tasks admit meaningful symbolic representations. Future work will explore selfsupervised learning to reduce logical supervision and incorporate additional sensory modalities for spatial reasoning. 

## REFERENCES 

- [1] Y. Yang, J. Sun, S. Kou, Y. Wang, and Z. Deng, “Lohovla: A unified vision-language-action model for long-horizon embodied tasks,” _arXiv preprint arXiv:2506.00411_ , 2025. 

- [2] L. X. Shi, B. Ichter, M. Equi, L. Ke, K. Pertsch, Q. Vuong, J. Tanner, A. Walling, H. Wang, N. Fusai, _et al._ , “Hi robot: Open-ended instruction following with hierarchical vision-language-action models,” _arXiv preprint arXiv:2502.19417_ , 2025. 

- [3] H. Chen, J. Guo, B. Wang, T. Zhang, X. Huang, B. Zheng, Y. Hou, C. Tie, J. Deng, and L. Shao, “Goal-vla: Image-generative vlms as object-centric world models empowering zero-shot robot manipulation,” _arXiv preprint arXiv:2506.23919_ , 2025. 

- [4] R. Shao, W. Li, L. Zhang, R. Zhang, Z. Liu, R. Chen, and L. Nie, “Large vlm-based vision-language-action models for robotic manipulation: A survey,” _arXiv preprint arXiv:2508.13073_ , 2025. 

- [5] PAN Team, Z. Liu, Y. Gu, M. Deng, G. Liu, Z. Feng, Q. Gao, Y. Hu, B. Huang, Y. Yang, K. Zhou, J. Xiang, Z. Hu, Z. Liu, and E. P. Xing, “Pan: A world model for general, actionable, and long-horizon world simulation,” _arXiv preprint arXiv:2511.09057_ , 2025. 

- [6] L. P. Kaelbling and T. Lozano-P´erez, “Hierarchical task and motion planning in the now,” in _2011 IEEE international conference on robotics and automation_ , 2011. 

- [7] T. Silver, R. Chitnis, A. Curtis, J. B. Tenenbaum, T. Lozano-P´erez, and L. P. Kaelbling, “Planning with learned object importance in large problem instances using graph neural networks,” in _Proceedings of the AAAI conference on artificial intelligence_ , 2021. 

- [8] D. Hafner, W. Yan, and T. Lillicrap, “Training agents inside of scalable world models,” _arXiv preprint arXiv:2509.24527_ , 2025. 

- [9] S. Li, Y. Gao, D. Sadigh, and S. Song, “Unified video action model,” _arXiv preprint arXiv:2503.00200_ , 2025. 

- [10] J. Quevedo, A. K. Sharma, Y. Sun, V. Suryavanshi, P. Liang, and S. Yang, “Worldgym: World model as an environment for policy evaluation,” _arXiv preprint arXiv:2506.00613_ , 2025. 

- [11] Y. Li, Y. Zhu, J. Wen, C. Shen, and Y. Xu, “Worldeval: World model as real-world robot policies evaluator,” _arXiv preprint arXiv:2505.19017_ , 2025. 

- [12] A. Bar, G. Zhou, D. Tran, T. Darrell, and Y. LeCun, “Navigation world models,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025. 

- [13] Y. Yang, J. Liu, Z. Zhang, S. Zhou, R. Tan, J. Yang, Y. Du, and C. Gan, “Mindjourney: Test-time scaling with world models for spatial reasoning,” _arXiv preprint arXiv:2507.12508_ , 2025. 

- [14] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn, _et al._ , “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025. 

- [15] H. Bi, H. Tan, S. Xie, Z. Wang, S. Huang, H. Liu, R. Zhao, Y. Feng, C. Xiang, Y. Rong, _et al._ , “Motus: A unified latent action world model,” _arXiv preprint arXiv:2512.13030_ , 2025. 

- [16] W. Zhang, H. Liu, Z. Qi, Y. Wang, X. Yu, J. Zhang, R. Dong, J. He, F. Lu, H. Wang, _et al._ , “Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge,” _arXiv preprint arXiv:2507.04447_ , 2025. 

- [17] M. J. Kim, Y. Gao, T.-Y. Lin, Y.-C. Lin, Y. Ge, G. Lam, P. Liang, S. Song, M.-Y. Liu, C. Finn, and J. Gu, “Cosmos policy: Fine-tuning video models for visuomotor control and planning,” in _The Fourteenth International Conference on Learning Representations_ , 2026. 

- [18] A. Xie, F. Ebert, S. Levine, and C. Finn, “Improvisation through physical understanding: Using novel objects as tools with visual foresight,” _arXiv preprint arXiv:1904.05538_ , 2019. 

- [19] R. Hoque, D. Seita, A. Balakrishna, A. Ganapathi, A. K. Tanwani, N. Jamali, K. Yamane, S. Iba, and K. Goldberg, “Visuospatial foresight for physical sequential fabric manipulation,” _Autonomous Robots_ , 2022. 

- [20] L. Manuelli, Y. Li, P. Florence, and R. Tedrake, “Keypoints into the future: Self-supervised correspondence in model-based reinforcement learning,” _arXiv preprint arXiv:2009.05085_ , 2020. 

- [21] D. Driess, F. Xia, M. S. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu, _et al._ , “Palm-e: An embodied multimodal language model,” _arXiv preprint arXiv:2303.03378_ , 2023. 

- [22] E. Xing, M. Deng, and J. Hou, “Critique of world model,” _arXiv preprint arXiv:2507.05169_ , 2025. 

- [23] Y. Ma, Z. Song, Y. Zhuang, J. Hao, and I. King, “A survey on vision-language-action models for embodied ai,” _arXiv preprint arXiv:2405.14093_ , 2024. 

- [24] Y. Zhong, F. Bai, S. Cai, X. Huang, Z. Chen, X. Zhang, Y. Wang, S. Guo, T. Guan, K. N. Lui, _et al._ , “A survey on vision-languageaction models: An action tokenization perspective,” _arXiv preprint arXiv:2507.01925_ , 2025. 

- [25] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ , 2023. 

- [26] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “OpenVLA: An open-source vision-language-action model,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [27] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [28] K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. R. Equi, C. Finn, N. Fusai, M. Y. Galliker, _et al._ , “ _π_ 0 _._ 5: a visionlanguage-action model with open-world generalization,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [29] Z. Wu, Y. Zhou, X. Xu, Z. Wang, and H. Yan, “Momanipvla: Transferring vision-language-action models for general mobile manipulation,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025. 

- [30] W. Yuan, J. Duan, V. Blukis, W. Pumacay, R. Krishna, A. Murali, A. Mousavian, and D. Fox, “Robopoint: A vision-language model for spatial affordance prediction for robotics,” _arXiv preprint arXiv:2406.10721_ , 2024. 

- [31] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: A 3d vision-language-action generative world model,” _arXiv preprint arXiv:2403.09631_ , 2024. 

- [32] M. Dalal, A. Mandlekar, C. Garrett, A. Handa, R. Salakhutdinov, and D. Fox, “Imitating task and motion planning with visuomotor transformers,” _arXiv preprint arXiv:2305.16309_ , 2023. 

- [33] R. Chitnis, D. Hadfield-Menell, A. Gupta, S. Srivastava, E. Groshev, C. Lin, and P. Abbeel, “Guided search for task and motion plans using learned heuristics,” in _2016 IEEE International Conference on Robotics and Automation (ICRA)_ , 2016. 

- [34] C. Paxton, V. Raman, G. D. Hager, and M. Kobilarov, “Combining neural networks and tree search for task and motion planning in challenging environments,” in _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2017. 

      - Embodied reasoning through planning with language models,” _arXiv preprint arXiv:2207.05608_ , 2022. 

   - [36] S. Wang, M. Han, Z. Jiao, Z. Zhang, Y. N. Wu, S.-C. Zhu, and H. Liu, “Llmˆ 3: Large language model-based task and motion planning with motion failure reasoning,” in _2024 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , 2024. 

   - [37] Y. Chen, J. Arkin, Y. Hao, Y. Zhang, N. Roy, and C. Fan, “Prompt optimization in multi-step tasks (promst): Integrating human feedback and heuristic-based sampling,” in _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , 2024. 

   - [38] M. Diehl, C. Paxton, and K. Ramirez-Amaro, “Automated generation of robotic planning domains from observations,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2021. 

   - [39] N. Kumar, W. McClinton, R. Chitnis, T. Silver, T. Lozano-P´erez, and L. P. Kaelbling, “Learning efficient abstract planning models that choose what to predict,” in _Conference on Robot Learning_ , 2023. 

   - [40] T. Silver, R. Chitnis, N. Kumar, W. McClinton, T. Lozano-P´erez, L. Kaelbling, and J. B. Tenenbaum, “Predicate invention for bilevel planning,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2023. 

   - [41] Y. Liang, N. Kumar, H. Tang, A. Weller, J. B. Tenenbaum, T. Silver, J. F. Henriques, and K. Ellis, “Visualpredicator: Learning abstract world models with neuro-symbolic predicates for robot planning,” _arXiv preprint arXiv:2410.23156_ , 2024. 

   - [42] J. Mao, T. Lozano-P´erez, J. B. Tenenbaum, and L. P. Kaelbling, “Learning reusable manipulation strategies,” in _Conference on Robot Learning_ , 2023. 

   - [43] J. Huang, A. Tao, R. Marco, M. Bogdanovic, J. Kelly, and F. Shkurti, “Automated planning domain inference for task and motion planning,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

   - [44] J. Huang, Y. Xiao, Z. Zhang, M. Coates, J. HAO, and Y. Zhang, “One demo is all it takes: Planning domain derivation with LLMs from a single demonstration,” in _The Fourteenth International Conference on Learning Representations_ , 2026. 

   - [45] M. Han, Y. Zhu, S.-C. Zhu, Y. N. Wu, and Y. Zhu, “Interpret: Interactive predicate learning from language feedback for generalizable task planning,” in _Robotics: Science and Systems (RSS)_ , 2024. 

   - [46] J. Huang, Z. Li, Y. Hu, Z. Zhang, M. Coates, X. Quan, and Y. Zhang, “Self-CriTeach: LLM self-teaching and self-critiquing for improving robotic planning via automated domain generation,” _arXiv preprint arXiv:2509.21543_ , 2025. 

   - [47] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _The Eleventh International Conference on Learning Representations_ , 2023. 

   - [48] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone, “Libero: Benchmarking knowledge transfer for lifelong robot learning,” _Advances in Neural Information Processing Systems_ , 2023. 

   - [49] S. Han, B. Qiu, Y. Liao, S. Huang, C. Gao, S. YAN, and S. Liu, “Robocerebra: A large-scale benchmark for long-horizon robotic manipulation evaluation,” in _The Thirty-ninth Annual Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ , 2025. 

   - [50] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: Optimizing speed and success,” _arXiv preprint arXiv:2502.19645_ , 2025. 

   - [51] J. Zheng, J. Li, Z. Wang, D. Liu, X. Kang, Y. Feng, Y. Zheng, J. Zou, Y. Chen, J. Zeng, T. Wang, Y.-Q. Zhang, J. Liu, and X. Zhan, “X-VLA: Soft-prompted transformer as scalable cross-embodiment vision-language-action model,” in _The Fourteenth International Conference on Learning Representations_ , 2026. 

   - [52] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

   - [53] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer, “Sigmoid loss for language image pre-training,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023. 

   - [54] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer, “High-resolution image synthesis with latent diffusion models,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2022. 

- [35] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng, J. Tompson, I. Mordatch, Y. Chebotar, _et al._ , “Inner monologue: 

