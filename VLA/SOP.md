---
title: "SOP: A Scalable Online Post-Training System for Vision-Language-Action Models"
date: "2026-01-06"
authors: "Mingjie Pan; Siyuan Feng; Qinglin Zhang; Xinchen Li; Jianheng Song; Chendi Qu"
url: https://arxiv.org/abs/2601.03044
pdf: https://arxiv.org/pdf/2601.03044
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.03044)** / [論文ページ](https://arxiv.org/abs/2601.03044)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# SOP: A Scalable Online Post-Training System for Vision-Language-Action Models 

Mingjie Pan*<sup>1</sup> Siyuan Feng*<sup>1</sup> Qinglin Zhang<sup>1</sup> Xinchen Li<sup>1</sup> Jianheng Song<sup>1</sup> Chendi Qu<sup>1</sup> Yi Wang<sup>1</sup><sup>_,_2</sup> Chuankang Li<sup>1</sup> Ziyu Xiong<sup>1</sup> Zhi Chen<sup>1</sup> Yi Liu<sup>1</sup> Jianlan Luo<sup>1</sup><sup>_,_2</sup><sup>_†_</sup> 1Agibot Research. 2Shanghai Innovation Institute. 

https://www.agibot.com/research/sop 

**_Abstract_ —Vision-language-action (VLA) models achieve strong generalization through large-scale pre-training, but real-world deployment requires expert-level task proficiency in addition to broad generality. Existing post-training approaches for VLA models are typically offline, single-robot, or task-specific, limiting effective on-policy adaptation and scalable learning from realworld interaction. We introduce a Scalable Online Post-training (SOP) system that enables online, distributed, multi-task posttraining of generalist VLA models directly in the physical world. SOP tightly couples execution and learning through a closed-loop architecture in which a fleet of robots continuously streams onpolicy experience and human intervention signals to a centralized cloud learner, and asynchronously receives updated policies. This design supports prompt on-policy correction, scales experience collection through parallel deployment, and preserves generality during adaptation. SOP is agnostic to the choice of post-training algorithm; we instantiate it with both interactive imitation learning (HG-DAgger) and reinforcement learning (RECAP). Across a range of real-world manipulation tasks including cloth folding, box assembly, and grocery restocking, we show that SOP substantially improves the performance of large pretrained VLA models while maintaining a single shared policy across tasks. Effective post-training can be achieved within hours of real-world interaction, and performance scales near-linearly with the number of robots in the fleet. These results suggest that tightly coupling online learning with fleet-scale deployment is instrumental to enabling efficient, reliable, and scalable posttraining of generalist robot policies in the physical world.** 

## I. INTRODUCTION 


Fig. 1: **Scalable Online Post-training (SOP).** A fleet of robots continuously collects experience across diverse tasks, streams interaction data to a centralized cloud server, and receives updated control policies asynchronously—enabling VLA models to improve proficiency on each task while preserving generality. 

_In the long history of humankind, those who learned to collaborate and improvise most effectively have prevailed._ 

Charles Darwin, _The Descent of Man_ 

Deploying general-purpose robots at scale is becoming increasingly tractable [57, 7, 22, 17, 31]. However, generality alone does not suffice for real-world deployment. Real-world deployment demands _high-performance generalists_ —systems that not only generalize across diverse tasks, but also achieve expert-level proficiency when instantiated in any specific setting. Consider a household robot: it must fold laundry, organize shelves, and assemble furniture, while exhibiting the reliability and precision expected of a dedicated appliance. 

> _†_ Corresponding author. 

Neither generality nor proficiency in isolation meets this bar; the two capabilities must coexist within a single system. 

Vision-language-action (VLA) models represent substantial progress toward providing the generality component of this requirement [57, 50, 22, 7, 17]. By unifying visual perception, language understanding, and action generation within a single architecture, VLAs trained on Internet-scale data exhibit very strong generalization capability across tasks, objects, and embodiments [8, 57, 42]. The remaining challenge is how to endow these models with expert-level proficiency without sacrificing this carefully achieved generality. 

The answer lies in _post-training_ —adapting the pre-trained model to specific downstream deployment scenarios [43, 3, 30, 39]. In domains such as large language models (LLMs), posttraining via online reinforcement learning (RL) and human 

_∗_ Equal contribution. 

feedback has proven to be very effective [43, 12], enabling models to continuously improve through large-scale distributed training [54, 15]. Yet system-level realizations of online learning with distributed data collection remain largely unexplored for VLA post-training in the physical world. 

Despite substantial progress in algorithmic post-training methods, existing VLA approaches remain fundamentally constrained by the absence of a unified system that couples distributed robot fleets with centralized, online learning. Consequently, most prior work operates in offline, singlerobot, and task-specific regimes [11, 56, 7, 57], where data collection and policy improvement are structurally decoupled. In this setting, offline training on pre-collected demonstrations inevitably suffers from distribution shift, with small execution errors compounding over long horizons. Iterative imitation learning methods, such as DAgger, partially mitigate this issue by incorporating human corrections [44, 25, 26, 18, 16], but their batch-based update cycles introduce latency between execution and correction, limiting their effectiveness in realtime sequential decision making—even in fully online variants such as HG-DAgger [21]. This observation is consistent with theoretical results highlighting the importance of timely, onpolicy corrections for mitigating distribution shift [19, 1]. These limitations are further exacerbated by single-robot data collection, which restricts experience diversity and learning speed, and by task-specific fine-tuning, which often trades generality for gains in proficiency [11, 56, 22, 50]. Collectively, these challenges reflect limitations of the underlying learning setting rather than shortcomings of individual algorithms. Consequently, no existing VLA post-training approach simultaneously supports timely on-policy correction, scalable experience collection, and multi-task adaptation within a single generalist model. 

To address these challenges, we introduce a Scalable Online Post-training (SOP) system for post-training generalist VLA models directly in the physical world using large-scale realworld interaction. The key insight is that tightly coupling learning and execution yields a unified feedback loop that enables timely on-policy correction, scales exploration through parallel experience, and preserves generality during adaptation. SOP realizes this insight via a closed-loop architecture in which a robot fleet exchanges on-policy trajectories and human intervention signals with a centralized cloud learner. This collect–train–deploy loop enables low-latency adaptation and scales naturally with fleet size. 

While SOP is in principle agnostic to the choice of posttraining algorithm, we instantiate it with HG-DAgger [21] and RECAP [3], representing interactive imitation learning and reinforcement learning, respectively. SOP substantially improves the performance of pretrained VLA models across a diverse set of real-world manipulation tasks, including cloth folding, box assembly, and shelf restocking. Crucially, these gains do not come at the expense of generality: a single model is jointly post-trained across all tasks, with shelf restocking involving a large and diverse set of objects. 

Perhaps most surprisingly, SOP enables effective post- 

training of large VLA models directly in the real world on the order of hours, rather than extended multi-day training cycles. This efficiency arises from prompt on-policy correction that targets the deployed policy’s failure modes, amplified by distributed experience collection. Additionally, SOP exhibits near-linear scaling: increasing the number of robots reduces the wall-clock time required to reach a target performance level approximately proportionally. Across both HG-DAgger and RECAP, SOP consistently outperforms their non-SOP counterparts, often achieving 2× or greater improvements in success rate, with several tasks approaching near-perfect performance and substantially higher throughput. In longhorizon evaluations, tasks such as laundry folding and box assembly run continuously for over 36 hours without degradation, demonstrating that SOP provides systematic benefits beyond algorithmic post-training alone. 

Our primary contribution is SOP, the first framework for online, distributed, multi-task post-training of VLA models in the physical world. SOP enables a fleet of robots to continuously share real-world experience through a centralized learner, allowing models to rapidly improve task proficiency without sacrificing generality. Crucially, we show that existing post-training algorithms, when instantiated within SOP, can reliably and efficiently improve large pretrained VLA models on challenging dexterous manipulation tasks using only limited real-world interaction. 

More broadly, SOP represents a concrete step toward scalable robot learning through shared experience across robot fleets. By tightly coupling deployment and learning, SOP enables a collection of robots to jointly maintain and refine a continuously evolving VLA directly from real-world interaction. This coupling establishes a feedback loop in which scaling robot fleets not only improves the efficiency of post-training, but also increases the diversity and relevance of experience available for learning—supporting continual adaptation and robust performance in long-horizon real-world deployments. These results suggest that fleet-scale deployment can serve as an important and complementary enabler of progress in robot learning systems, alongside advances in algorithms and data. 

## II. RELATED WORKS 

SOP is a fundamentally integrative system framework: by combining online learning, distributed data collection, and multi-task training, it addresses the limitations of existing VLA post-training methods. We thus survey related works along these three axes. 

## _A. VLA Post-training_ 

VLA models achieve broad generalization through largescale pre-training on diverse multimodal data [8, 57, 22, 50, 17, 6, 51, 2, 34, 47]. To adapt these models to deployment settings, post-training methods broadly fall into two categories: supervised finetuning and reinforcement learning. Supervised finetuning adapts VLA models using task-specific demonstrations [7, 33, 22]. While stable and effective, these 


Fig. 2: SOP overview. SOP is a scalable actor–learner framework for online, multi-task post-training of generalist policies. The robot fleet streams on-policy rollouts to the cloud learner. Optional human interventions are triggered in failure or uncertain cases, providing corrected trajectories or actions that are incorporated into the streaming experience buffer. The cloud learner constructs task-balanced updates by mixing an online buffer with a static offline buffer, applies a plug-in post-training module (e.g., HG-DAgger/RECAP), and asynchronously broadcasts refreshed weights back to all actors to close a low-latency online training loop. 

methods rely on static datasets, limiting their ability to address distribution shift or to improve beyond demonstration coverage. Reinforcement learning (RL) [49] improves policies through environment interaction and feedback, encompassing both online and offline RL [24, 28]. Online RL algorithms such as PPO [45] and GRPO [46] have shown strong results in domains including robotic locomotion and LLMs, but face practical challenges in real-world robotic manipulation, including high variance and training instability [35, 32, 29, 9, 55]. Behavior-regularized RL methods can improve stability [10, 27], but often bias asymptotic performance and are typically task-specific, limiting applicability to generalist settings. Among offline RL approaches [41, 23, 52], RECAP [3] is most closely related. RECAP combines reward feedback with human interventions through iterative offline training, focusing on task-specific specialization. While effective for individual tasks, it does not directly support continuous online improvement of a single generalist policy across tasks. RLDG [53] adopts a complementary strategy by first using taskspecific RL to generate high-quality trajectories, which are subsequently distilled into a generalist policy via behavior cloning. While this distillation step helps retain generality, data generation in RLDG remains offline, single-robot, and 

requires training separate RL policies for each task, limiting scalability. In contrast, SOP directly updates a generalist policy through continuous online learning with distributed, multitask data collection, enabling performance improvement while preserving generality. 

## _B. Interactive and Online Learning_ 

Online learning addresses distribution shift by training on states encountered by the current policy, rather than relying solely on pre-collected expert data. Interactive imitation learning methods such as DAgger [44] iteratively collect states from the learned policy and query expert labels, while HGDAgger [21] shifts to real-time intervention where the expert only takes over when the policy is about to fail, reducing human burden while directly correcting on-policy mistakes. Sample-efficient online RL methods leverage demonstrations to accelerate learning: RLPD [4] mixes offline data with online experiences, SERL [36] combines demonstrations with online RL for robotic tasks, and HIL-SERL [37] further integrates human intervention, achieving expert-level performance on complex long-horizon tasks. However, these methods remain _single-robot_ (limiting data collection throughput) and _taskspecific_ (requiring separate training for each task). SOP extends online learning to distributed multi-task settings, en- 

abling parallel state-space coverage across robot fleets while preserving generality. 

## _C. Distributed and Multi-task Robot Learning_ 

Scaling beyond single-robot data collection requires distributed architectures, while multi-task learning prevents overfitting to narrow objectives. Distributed RL systems such as Gorila [5], A3C [40], and IMPALA [13] pioneered actorlearner architectures for accelerated training, but target simulation environments where reset is trivial and do not address realworld deployment with human oversight. Fleet-DAgger [14] is the closest prior work, establishing a multi-robot interactive learning system with scalable human supervision. It achieves online distributed learning, but remains simulation-only, not designed for large VLA models, and limited to single-task learning. Multi-task robot learning [48, 20, 38] demonstrates the benefits of sharing experience across tasks, but these methods do not combine online learning with distributed collection for VLA post-training. In summary, SOP is the first framework that simultaneously enables online, distributed, multi-task post-training for generalist models in the physical world. 

## III. PRELIMINARIES AND PROBLEM STATEMENT 

## _A. Preliminaries_ 

We formulate the considered robot control problem as a Markov decision process (MDP) _M_ = ( _S, A, T, r, γ_ ), where _S_ is the state space, _A_ is the action space, _T_ ( _s_<sup>_′_</sup> _|s, a_ ) and _r_ ( _s, a_ ) denote the transition dynamics and environment reward at ( _s, a_ ) and _γ ∈_ (0 _,_ 1] is the discount factor. For VLA models, the state _s_ typically comprises visual observations, language instructions, and robot proprioceptive information. A policy _πθ_ ( _a|s_ ) defines a distribution over actions given state _s_ ; at each step, the agent samples _a ∼ πθ_ ( _·|s_ ) and transitions to _s_<sup>_′_</sup> _∼ T_ ( _·|s, a_ ). 

|**Algorithm 1:** Scalable Online Post-training for VLA|
|---|
|**Input:** Initial policy _πθ_0, Offline buffer _B_off,|
|Post-training algorithm _G_, Adaptive sampler _S_|
|Initialize online buffer _B_on _←∅_;|
|Broadcast _πθ_0 to all actors;|
|**Actor** _i_ **(parallel):**<br>**while** _acting_ **do**<br>|
|Execute policy _πθ_ and collect rollouts _τ _<sup>_i_</sup><br>_π_<sup>;</sup><br>**if** _human has control_ **then**<br>Collect interventions _τ _<sup>_i_</sup><br>_H_<sup>;</sup><br>Upload _τ _<sup>_i_</sup><br>_π _<sup>_∪τ i_</sup><br>_H_ <sup>to</sup> <sup>_B_on.</sup>|
|**Cloud Learner (asynchronous):**<br>**while** _training_ **do**<br>|
|Sample a training batch _ξ ←S_(_B_on_∪B_off);<br>Update policy parameters: _θ ←G_(_θ, ξ_);<br>Stream updated policy _πθ_ to all actors;|


## IV. SCALABLE ONLINE POST-TRAINING 

We present _Scalable Online Post-training_ (SOP), a closedloop actor–learner framework for adapting a pretrained VLA policy using continual real-world interaction from a heterogeneous robot fleet. SOP consists of (i) distributed on-policy data collection by robot actors, (ii) centralized cloud optimization on mixed online and offline data, and (iii) low-latency model synchronization back to actors. Importantly, SOP is _algorithm-agnostic_ : it specifies the system-level dataflow and synchronization, while the concrete parameter update method can be replaced by any post-training algorithm. In this paper, we instantiate SOP with two existing post-training methods— HG-DAgger [21] and RECAP [3]—and show that SOP _upgrades_ them into practical on-policy, online post-training by continuously streaming fresh experience and applying frequent asynchronous model updates. 

## _B. Problem Statement_ 

Consider a distributed robot system. _N_ robots are deployed in various environments, operating different tasks. We use a domain variable _ϕ_ to model the heterogeneity, which induces a family of MDPs _M_ ( _ϕ_ ). Specifically, the _i_ -th robot’s interaction is governed by _M_<sup>_i_</sup> := _M_ ( _ϕi_ ), where _ϕi ∼ p_ ( _ϕ_ ) for _i_ = 1 _,_ 2 _, . . . , N_ . The goal of post-training is to adapt a pretrained base policy _πθ_ 0 to each deployment domain by leveraging online interaction data collected from the robot fleet. This usually involves a multi-round optimization procedure. At the _k_ -th iteration, robots execute the current policy _πθk_ and collect trajectories, including both autonomous rollouts and potential human interventions, into a dataset _Dk_ . The policy is then updated by minimizing a post-training objective defined over collected samples: 


_LP T_ denotes the post-training loss corresponding to the specific chosen post-training algorithm _G_ , which can be formulated as log-likelihood loss or diffusion/flow-based loss. 

## _A. Algorithm Framework_ 

Algorithm 1 summarizes SOP. We start from a pretrained policy _πθ_ 0 (see more details in Appendix C) and broadcast it to all _N_ robot actors. Each actor _i_ continuously executes the latest available policy _πθ_ in its local domain _M_<sup>_i_</sup> and uploads trajectories to a shared online experience buffer in parallel. Trajectories include autonomous rollouts _τπ_<sup>_i_and,</sup> when available, human interventions _τH_<sup>_i_for correction.At the</sup> same time, a centralized cloud learner continuously samples training batches from a mixture of the online buffer and static offline buffer and updates the shared parameters via a posttraining algorithm _G_ . Updated parameters are then streamed back to all actors asynchronously. 

Specifically, let _τ_<sup>_i_</sup> ( _t_ ) denote all episodes uploaded to the cloud by robot _i_ up to wall-clock time _t_ . The aggregated online experience available by time _t_ is _B_ on( _t_ ) = _∪_<sup>_N_</sup> _i_ =1<sup>_τ i_(</sup><sup>_t_). At</sup> training step _j_ (wall-clock time _tj_ ), the training batch sampled by the cloud learner is denoted as 


where _Sj_ is a designed adaptive data sampler that enables dynamic online/offline composition via configurable weighting schemes (see the design details in Sec. IV-C). _B_ off is a static offline buffer containing prior human demonstrations. With _ξj_ , the model parameter is updated by the learner through 


Then the latest model parameter _θ_ is streamed to all actors. 

## _B. System Infrastructure_ 

We develop a distributed actor–learner data infrastructure designed for real-world robot fleets, as illustrated in Figure 7. Each robot actor runs an edge-side client that buffers episodes locally and uploads them asynchronously to object storage at episode boundaries. Uploaded episodes are then appended into a cloud-hosted online buffer, which the learner consumes independently via notifications and on-demand retrieval. 

To close the loop, updated model parameters are synchronized from the cloud learner to robot actors through a lightweight publish–subscribe channel at short intervals. Actors fetch the latest checkpoints with end-to-end latencies typically on the order of seconds to tens of seconds (scaling with model size) and apply updates at safe boundaries (e.g., between episodes), preventing mid-episode policy changes from corrupting logged trajectories. This decoupling allows actors and learners to scale independently and remains robust to transient network disruptions. See more design details in Appendix B. 

## _C. Adaptive Sampling Strategy_ 

To preserve multi-task coverage while adapting quickly to newly collected on-policy data, we use a task-balanced adaptive sampling strategy _Sj_ at learner step _j_ . Assume the training data are partitioned into _M_ tasks indexed by _m ∈ {_ 1 _,_ 2 _, . . . , M }_ . At the inter-task level, we enforce uniform task weights _ω_<sup>_m_</sup> = 1 _/M_ so that each task contributes equally. At At the intra-task level, for task _m_ , we adjust the sampling ratio between the task’s online buffer _B_ on<sup>_m_andofflinebuffer</sup> _B_ off<sup>_m_basedonrecenttraininglosses.</sup> 

For each task, we maintain sliding-window estimates of online and offline losses with window size _W_ = 200: ¯ _l_ on<sup>_m_=</sup> _W_ <u>1</u> � _ji_ = _−j_ 1 _−W_<sup>_l_</sup> on<sup>_m,i_</sup> and<sup>¯</sup> _l_ off<sup>_m_=</sup> _W_ <u>1</u> � _ji_ = _−j_ 1 _−W_<sup>_l_</sup> off<sup>_m,i_.The</sup> online sampling ratio _ω_ on<sup>_m_iscomputedby:</sup> 


where _α >_ 1 is a boost factor that prioritizes online data to accelerate adaptation under distribution shift. To avoid extreme allocations, we clip _ω_ on<sup>_m_totheinterval</sup> �0 _._ 2 _,_ 0 _._ 8�. Given task _m_ , we sample from _B_ on<sup>_m_withprobability</sup><sup>_ω_</sup> on<sup>_m_andfrom</sup><sup>_B_</sup> off<sup>_m_</sup> with probability 1 _− ω_ on<sup>_m_. This sampling strategy ensures equal</sup> task coverage while enabling loss-driven adaptation of the online/offline data mixture. 

## _D. Post-training Learning Module_ 

SOP decouples the _system_ (distributed dataflow and synchronization) from the _algorithm_ (how to update _θ_ from a batch). This is captured by the post-training module _G_ in Algorithm 1. Any existing post-training method that consumes logged experience and returns updated parameters can be plugged into SOP. Below we summarize the original characteristics of HG-DAgger and RECAP, and describe how SOP turns each into an on-policy, online post-training procedure via continuous data streaming and asynchronous updates. 

_a)_ **_HG-DAgger_** _:_ HG-DAgger [21] is an interactive imitation learning method in which a human supervisor provides real-time interventions when the robot is about to fail, yielding corrective supervision on hard, on-policy states with reduced human effort compared to full teleoperation. In SOP, these intervention segments (together with autonomous rollouts and offline demonstrations) are continuously streamed into the shared buffer and consumed by the cloud learner for frequent asynchronous updates. This turns HG-DAgger into a practical, fleet-scale _on-policy online_ post-training procedure by reducing the latency between failure, correction, and model update. 

_b)_ **_RECAP_** _:_ RECAP [3] is an offline RL method for post-training large VLA policies, designed to improve a policy from experience (including autonomous rollouts and optional human corrections). In its standard usage, RECAP is applied in an iterative offline loop (collect experience, train offline, redeploy). SOP makes this workflow _online_ by continuously incorporating freshly collected trajectories from the latest deployed policy into the buffer and running RECAPstyle updates asynchronously on the evolving dataset. This reduces policy–data staleness and enables continual, on-policy improvement while keeping RECAP itself unchanged. 

## V. EXPERIMENTAL EVALUATION 

We evaluate SOP by instantiating it with two representative post-training algorithms: HG-DAgger [21] and RECAP [3]. Experiments are conducted on a fleet of 10 dual-arm manipulators across three challenging manipulation task families as in Fig. 3, designed to stress both fine-grained dexterity and semantic generalization. Our experiments focus on three questions: 

- 1) How effectively does SOP improve pretrained VLA performance on real-world manipulation, and how does it compare to offline alternatives? 

- 2) How does performance scale with fleet size? 

- 3) Does SOP provide consistent gains across pretrained models of varying initial quality? 

We organize results accordingly into multi-task post-training, fleet scaling, and pre-training quality/data efficiency. 

## _A. Experiment Tasks_ 

We evaluate on three task families that require both dexterous manipulation and semantic understanding: Grocery Restocking, Laundry Folding, and Box Assembly. The illustration of tasks can be seen in Fig. 3. We summarize detailed task setups and evaluation protocol below. 


Fig. 3: Illustrations of the three task categories. (A) Grocery Restocking scenarios: (A-1) flat-shelf restocking; (A-2) correcting misplaced items; (A-3) freezer restocking involving door manipulation; and (A-4) open-cooler restocking with carton handling. (B) Laundry Folding: a bimanual sequence where the robot flattens and folds a garment. (C) Box Assembly: a sequence showing two robot arms coordinating to fold a flattened cardboard sheet into a 3D box structure. 

**Grocery Restocking.** This task evaluates policy generalization in a cluttered retail environment, requiring semantic understanding across a large catalog of store items and diverse shelf configurations. During pre-training, the robot is trained to execute diverse operations including restocking, picking, hanging, and item rearrangement. The pretraining corpus covers 500+ distinct objects in this task family. For evaluation, we uniformly sample a fixed set of 40 objects from this pool and keep it unchanged across all experiments; each of the four variants: (1) flat-shelf restocking, (2) correction for misplaced items, (3) freezer restocking with door operation, and (4) opencooler restocking with carton handling—is tested on 10 objects drawn from this evaluation set, with 5 trials per object. During post-training, objects are sampled from the full object pool; consequently, a typical post-training session overlaps with roughly two-thirds ( _∼_ 70%) of the evaluation objects, while still preserving object diversity beyond the evaluation subset. Success requires both instruction compliance (selecting the correct item from a cluttered set) and task completion (placing it at the target location within the time limit). 

**Laundry Folding.** This task requires dexterous bimanual manipulation of deformable objects. During training, robots learn to pick, fold, and stack garments from a basket. For evaluation, we present a single disordered T-shirt; success requires folding it correctly and placing it on a designated stack within 500 s. 

**Box Assembly.** This task evaluates precise multi-step procedural execution. The robot must transform a flat cardboard sheet into a 3D box through a sequence of folds. Success requires completing the assembly within 300 s with no folding errors. 

For Laundry Folding and Box Assembly, our data collection and deployment can involve _full-cycle_ continuous operation (e.g., fetching a garment from a basket and repositioning it before folding; or preparing the cardboard before assembly). In quantitative evaluation, we focus on the core longhorizon manipulation skill (folding/assembly) and therefore do not include upstream fetching/stacking/preparation steps in the trial definition. Each trial begins from a randomized, disordered initial state where the garment/cardboard is placed within the robot workspace (with natural variability in pose and configuration) and ends upon success, failure, or timeout. 

**Metrics.** We report _success rate_ (fraction of successful episodes) and _throughput_ (completed episodes per hour). An episode is considered _completed_ when it terminates due to success, failure, or timeout. Throughput therefore captures both execution speed and reliability under a fixed time budget (500 s for Laundry Folding and 300 s for Box Assembly; Grocery Restocking uses a task-dependent time limit). Importantly, throughput is measured as _policy-side throughput_ and does not include human operator time for environment reset or scene setup between trials; this exclusion is consistent across 

all compared methods. 

## _B. Experiment Setup_ 

We evaluate SOP with a fleet of Agibot G1 dual-arm manipulators across three task families (Grocery Restocking, Laundry Folding, and Box Assembly). In the main multi-task setting, we train a single shared learner while partitioning the 10-robot actor fleet across tasks: 4 robots collect on-policy experience for Grocery Restocking, 3 for Laundry Folding, and 3 for Box Assembly; experience from all actors is aggregated for joint SOP training. All post-training experiments start from a pretrained base policy _πθ_ 0, which is initialized by _π_ 0 _._ 5 [17]. Details are provided in the Appendix C. SOP improves it through continual on-policy interaction. Unless otherwise specified, we allocate a wall-clock budget of 3 hours (180 minutes) per experiment, and choose SOP+HGDAgger as the post-training algorithm. In our experiments, we train the learner on NVIDIA H100 GPUs. In 10-actor experiment setup, we provide 8 GPUs to accommodate the higher data throughput, while in other experiments we use 4 GPUs. This reflects our experimental allocation rather than a fixed requirement of SOP. In additional ablation experiments, we focus on Grocery Restocking only and use a smaller actor fleet of 4 robots, varying the number of active actors ( _N ∈{_ 1 _,_ 2 _,_ 4 _}_ ). Implementation details of the pretrained base policy and SOP post-training are provided in Appendix C. 

## _C. Multi-task Post-training_ 

As shown in Fig. 4, we report success rate and throughput for post-trained models with and without SOP. For Laundry Folding and Box Assembly, each reported number is evaluated over 50 trials. For Grocery Restocking, each of the four variants is evaluated over 50 trials (10 objects _×_ 5 trials), for a total of 200 trials across the task family. 

For RECAP, the original implementation is not designed for multi-task post-training. We therefore condition both the policy and value function on the task language prompt, resulting in a multi-task variant of RECAP. To verify that this modification does not degrade performance, we additionally train single-task RECAP models on two representative grocery restocking variants: open-front cooler replenishment and freezer replenishment. Single-task RECAP achieves success rates of 0.86 and 0.75, respectively, while multi-task RECAP achieves 0.80 and 0.75 (50 trials each). These results indicate that multi-task conditioning does not significantly degrade RECAP performance, ensuring a fair comparison. Implementation details of SOP + RECAP are provided in the Appendix. 

Across all tasks, post-trained models consistently outperform the pretrained baseline. Moreover, combining either HGDAgger (or RECAP) with SOP yields substantially higher performance than their non-SOP counterparts. SOP + HG-DAgger achieves the strongest result—success rates of 0.94, 0.96, and 0.98 across the three task families. In grocery restocking, the performance gap between SOP + HG-DAgger and SOP + RECAP is the largest, which is expected given the strong semantic generalization required by this task. In such settings, 

learning an accurate value function with sufficiently broad coverage remains challenging, whereas interactive imitation benefits more directly from corrective supervision. In terms of throughput, SOP substantially improves performance across all pretrained models, typically by approximately 2×. This gain arises from prompt on-policy correction that directly targets the failure modes of the deployed policy. For example, in laundry folding, a common failure mode is repeated missed grasps; SOP rapidly corrects this behavior through on-policy feedback, leading to significantly reduced cycle time. 

Overall, these results demonstrate that SOP provides a simple yet effective system-level mechanism for post-training generalist VLA models through scalable robot deployment. 

## _D. Scaling robot deployments_ 

A natural question is how post-training efficiency scales with fleet size. We study how post-training efficiency scales with the size of the robot fleet by varying the number of active robot actors ( _N ∈_ 1 _,_ 2 _,_ 4) and evaluating both final performance and time-to-target. All experiments are capped at 180 minutes. We report the final success rate at the end of training as well as the wall-clock time required to first reach a target success level (set to 0.8 in our experiments), which we refer to as time-to-target and use as a measure of training efficiency. As summarized in Table I, increasing the number of robot actors consistently improves both the achievable performance and the rate of learning. Expanding the fleet from one to four actors raises the final success rate at 180 minutes from 0.805 to 0.925. This improvement suggests that parallel data collection across multiple robots provides more diverse on-policy experience, reducing overfitting to station-specific noise and idiosyncrasies that arise in single-robot settings. In addition to improving the performance ceiling, fleet scaling substantially accelerates learning. As summarized in Table I, time-to-target decreases from 173.6 minutes with a single actor to 126.5 minutes with two actors (1.4 _×_ faster) and to 71.7 minutes with four actors (2.4 _×_ faster). Within the tested regime ( _N ∈{_ 1 _,_ 2 _,_ 4 _}_ ), this suggests approximately linear wall-clock speedups, indicating that SOP largely translates robot parallelism into faster on-policy post-training rather than being bottlenecked by centralized learning or communication overhead. 

Overall, these results demonstrate that SOP enables posttraining efficiency to scale favorably with fleet size, improving both data efficiency and wall-clock training time. They further suggest that, for real-world VLA post-training, scaling robot deployments can be as impactful as algorithmic refinements in accelerating learning. 

## _E. Analysis of Pre-training Quality and Data Efficiency_ 

To examine how the initial capacity of the base policy affects online adaptation, we evaluate SOP starting from three pretrained variants: Base-1/8, Base-1/2, and Base-Full. These models share the same architecture but are pretrained on 1/8, 1/2, and the full set of diverse multi-task pretraining data, respectively, where the full dataset comprises approximately 


Fig. 4: Comparison of Success Rate and Throughput across three manipulation domains. Across all domains, our approach demonstrates superior efficiency and reliability. SOP w/ HG-DAgger consistently achieves 2-4x higher throughput and significantly reduces failure rates compared to offline methods under our evaluation protocol (policy-side throughput excluding human reset/setup time). 

TABLE I: Scalability Analysis with actor count. Comparison of final success rates and training efficiency scaling with different actor counts ( _N_ ). Performance gains and speedups are reported relative to the single-actor baseline. Time-to-target denotes the wall-clock time to first reach the target success level (0.8). 

|**Actor Number**|**Success Rate @180min**|**Time-to-target (min)**|
|---|---|---|
|1|0.805|173.6|
|2|0.887 (+0.082)|126.5 (1_._4_×_ faster)|
|4|**0.925** (**+0.12**)|**71.7** (**2.4**_×_ **faster**)|


a modest improvement in success rate, from 0.576 to 0.612. In comparison, applying SOP yields a substantially larger improvement—from 0.571 to 0.800—using only 3 hours of on-policy interaction. This gap reflects the diminishing returns of static expert demonstrations, which cannot anticipate the specific error distributions induced by a deployed policy. By directly collecting and learning from policy-generated failures, SOP allocates learning capacity to the most relevant regions of the state–action space, exhibiting a markedly more favorable scaling behavior for closing the final performance gap. 

## VI. DISCUSSION AND FUTURE WORK 

160 hours of data across all tasks. Results are summarized in Fig. 5. 

Across all settings, SOP consistently improves performance relative to the pretrained baseline. However, the final performance achieved after post-training remains strongly coupled to the scale of pretraining. Models initialized from larger pretraining datasets not only start from higher baselines but also converge to higher asymptotic performance. This suggests that large-scale pretraining provides essential representational priors that SOP builds upon, and that online post-training primarily refines and specializes existing knowledge rather than replacing the need for broad pretraining. 

The contrast between offline data scaling and on-policy experience further highlights this effect. For the Base-1/2 model, augmenting the offline demonstration dataset with an additional 80 hours of human-collected data results in only 

Our results suggest that the system-level coupling between execution and learning is as critical to post-training success as the underlying algorithm. By enabling robot fleets to continuously stream on-policy experience and receive updated policies in return, SOP transforms episodic fine-tuning into scalable, closed-loop learning. The observation that on-policy correction yields substantially greater marginal utility than additional offline data echoes a recurrent theme: static datasets cannot fully anticipate the state distribution induced by a deployed policy [44]. SOP operationalizes this insight at system scale. 

Despite its effectiveness, SOP currently relies on human interventions or task-specific rewards; reducing this supervisory burden through learned reward models or foundationmodel-based success detection remains an important direction. Whether near-linear scaling extends to significantly larger fleets, and how to support continual acquisition of new skills 


Fig. 5: Effect of pretraining data scale on SOP. Larger pretraining datasets yield higher initial success and higher final performance after online post-training. 

without catastrophic forgetting, are open questions. 

Looking forward, we envision fleets of robots jointly maintaining a shared, ever-improving policy through deployment experience. In this view, scaling robot deployments becomes a form of scaling compute for learning—each additional robot accelerates policy improvement. Realizing this vision will require advances across systems, algorithms, and human-robot interaction, but the results here suggest that the foundations are within reach. 

## REFERENCES 

- [1] Alekh Agarwal, Yuda Song, Wen Sun, Kaiwen Wang, Mengdi Wang, and Xuezhou Zhang. On the theory of reinforcement learning with once-per-episode feedback. _Advances in Neural Information Processing Systems_ , 35, 2022. 

- [2] AgiBot-World-Contributors, Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, Shu Jiang, Yuxin Jiang, Cheng Jing, Hongyang Li, Jialu Li, Chiming Liu, Yi Liu, Yuxiang Lu, Jianlan Luo, Ping Luo, Yao Mu, Yuehan Niu, Yixuan Pan, Jiangmiao Pang, Yu Qiao, Guanghui Ren, Cheng Ruan, Jiaqi Shan, Yongjian Shen, Chengshi Shi, Mingkang Shi, Modi Shi, Chonghao Sima, Jianheng Song, Huijie Wang, Wenhao Wang, Dafeng Wei, Chengen Xie, Guo Xu, Junchi Yan, Cunbiao Yang, Lei Yang, Shukai Yang, Maoqing Yao, Jia Zeng, Chi Zhang, Qinglin Zhang, Bin Zhao, Chengyue Zhao, Jiaqi Zhao, and Jianchao Zhu. Agibot world colosseo: A largescale manipulation platform for scalable and intelligent embodied systems, 2025. URL https://arxiv.org/abs/2503. 06669. 

- [3] Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Kevin Black, Ken Conley, Grace Connors, James Darpinian, Karan Dhabalia, Jared DiCarlo, Danny Driess, et al. _π_ 0<sup>_∗_</sup> _._ 6<sup>:avlathatlearnsfromexperience.</sup><sup>_arXivpreprint_</sup> _arXiv:2511.14759_ , 2025. 

- [4] Philip J Ball, Laura Smith, Ilya Kostrikov, and Sergey Levine. Efficient online reinforcement learning with offline data. In _International Conference on Machine Learning_ , pages 1577–1594. PMLR, 2023. 

- [5] Gabriel Barth-Maron, Matthew W. Hoffman, David Budden, Will Dabney, Dan Horgan, Dhruva TB, Alistair Muldal, Nicolas Heess, and Timothy Lillicrap. Distributed distributional deterministic policy gradients, 2018. URL https://arxiv.org/abs/1804.08617. 

- [6] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A visionlanguage-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [9] Kang Chen, Zhihao Liu, Tonghe Zhang, Zhen Guo, Si Xu, Hao Lin, Hongzhi Zang, Quanlu Zhang, Zhaofei Yu, Guoliang Fan, et al. _πRL_ : Online rl fine-tuning for flow-based vision-language-action models. _arXiv preprint arXiv:2510.25889_ , 2025. 

- [10] Yuhui Chen, Shuai Tian, Shugao Liu, Yingting Zhou, Haoran Li, and Dongbin Zhao. Conrft: A reinforced fine-tuning method for vla models via consistency policy. _arXiv preprint arXiv:2502.05450_ , 2025. 

- [11] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Robotics: Science and Systems_ , 2023. 

- [12] DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue, Bingxuan Wang, Bochao Wu, Bei Feng, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, Damai Dai, Deli Chen, Dongjie Ji, Erhang Li, Fangyun Lin, Fucong Dai, Fuli Luo, Guangbo Hao, Guanting Chen, Guowei Li, H. Zhang, Han Bao, Hanwei Xu, Haocheng Wang, Honghui Ding, Huajian Xin, Huazuo Gao, Hui Qu, Hui Li, Jianzhong Guo, Jiashi Li, Jiawei Wang, Jingchang Chen, Jingyang Yuan, Junjie Qiu, Junlong Li, J. L. Cai, Jiaqi Ni, Jian Liang, Jin Chen, Kai Dong, Kai Hu, Kaige Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean Wang, Lecong Zhang, Liang Zhao, Litong Wang, Liyue Zhang, Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang, Minghui Tang, Meng Li, Miaojun Wang, Mingming Li, Ning Tian, Pan- 

pan Huang, Peng Zhang, Qiancheng Wang, Qinyu Chen, Qiushi Du, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen, R. L. Jin, Ruyi Chen, Shanghao Lu, Shangyan Zhou, Shanhuang Chen, Shengfeng Ye, Shiyu Wang, Shuiping Yu, Shunfeng Zhou, Shuting Pan, S. S. Li, Shuang Zhou, Shaoqing Wu, Shengfeng Ye, Tao Yun, Tian Pei, Tianyu Sun, T. Wang, Wangding Zeng, Wanjia Zhao, Wen Liu, Wenfeng Liang, Wenjun Gao, Wenqin Yu, Wentao Zhang, W. L. Xiao, Wei An, Xiaodong Liu, Xiaohan Wang, Xiaokang Chen, Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie, Xingchao Liu, Xinyu Yang, Xinyuan Li, Xuecheng Su, Xuheng Lin, X. Q. Li, Xiangyue Jin, Xiaojin Shen, Xiaosha Chen, Xiaowen Sun, Xiaoxiang Wang, Xinnan Song, Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Yang Zhang, Yanhong Xu, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Wang, Yi Yu, Yichao Zhang, Yifan Shi, Yiliang Xiong, Ying He, Yishi Piao, Yisong Wang, Yixuan Tan, Yiyang Ma, Yiyuan Liu, Yongqiang Guo, Yuan Ou, Yuduan Wang, Yue Gong, Yuheng Zou, Yujia He, Yunfan Xiong, Yuxiang Luo, Yuxiang You, Yuxuan Liu, Yuyang Zhou, Y. X. Zhu, Yanhong Xu, Yanping Huang, Yaohui Li, Yi Zheng, Yuchen Zhu, Yunxian Ma, Ying Tang, Yukun Zha, Yuting Yan, Z. Z. Ren, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu, Zhenda Xie, Zhengyan Zhang, Zhewen Hao, Zhicheng Ma, Zhigang Yan, Zhiyu Wu, Zihui Gu, Zijia Zhu, Zijun Liu, Zilin Li, Ziwei Xie, Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu Zhang, and Zhen Zhang. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning, 2025. URL https://arxiv.org/abs/2501.12948. 

- [13] Lasse Espeholt, Hubert Soyer, Remi Munos, Karen Simonyan, Vlad Mnih, Tom Ward, Yotam Doron, Vlad Firoiu, Tim Harley, Iain Dunning, et al. Impala: Scalable distributed deep-rl with importance weighted actorlearner architectures. In _International conference on machine learning_ , pages 1407–1416. PMLR, 2018. 

- [14] Ryan Hoque, Lawrence Yunliang Chen, Satvik Sharma, Karthik Dharmarajan, Brijen Thananjeyan, Pieter Abbeel, and Ken Goldberg. Fleet-dagger: Interactive robot fleet learning with scalable human supervision. In _Conference on Robot Learning_ , pages 368–380. PMLR, 2023. 

- [15] Jian Hu, Xibin Wu, Zilin Zhu, Weixun Wang, Dehao Zhang, Yu Cao, et al. Openrlhf: An easy-to-use, scalable and high-performance rlhf framework. _arXiv preprint arXiv:2405.11143_ , 2024. 

- [16] Zheyuan Hu, Robyn Wu, Naveen Enock, Jasmine Li, Riya Kadakia, Zackory Erickson, and Aviral Kumar. Rac: Robot learning for long-horizon tasks by scaling recovery and correction. _arXiv preprint arXiv:2509.07953_ , 2025. 

- [17] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [18] Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991–1002. PMLR, 2022. 

- [19] Sham Kakade and John Langford. Approximately optimal approximate reinforcement learning. _Proceedings of the Nineteenth International Conference on Machine Learning_ , pages 267–274, 2002. 

- [20] Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, Benjamin Swanson, Rico Jonschkowski, Chelsea Finn, Sergey Levine, and Karol Hausman. Mt-opt: Continuous multi-task robotic reinforcement learning at scale. _arXiv preprint arXiv:2104.08212_ , 2021. 

- [21] Michael Kelly, Chelsea Sidrane, Katherine DriggsCampbell, and Mykel J Kochenderfer. Hg-dagger: Interactive imitation learning with human experts. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 8077–8083. IEEE, 2019. 

- [22] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [23] Ilya Kostrikov, Ashvin Nair, and Sergey Levine. Offline reinforcement learning with implicit q-learning. _arXiv preprint arXiv:2110.06169_ , 2021. 

- [24] Sascha Lange, Thomas Gabel, and Martin Riedmiller. Batch reinforcement learning. In _Reinforcement learning: State-of-the-art_ , pages 45–73. Springer, 2012. 

- [25] Michael Laskey, Sam Staszak, Wesley Yu-Shu Hsieh, Jeffrey Mahler, Florian T Pokorny, Anca D Dragan, and Ken Goldberg. Shiv: Reducing supervisor burden in dagger using support vectors for efficient learning from demonstrations in high dimensional state spaces. In _2016 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 462–469. IEEE, 2016. 

- [26] Michael Laskey, Jonathan Lee, Roy Fox, Anca Dragan, and Ken Goldberg. Dart: Noise injection for robust imitation learning. In _Conference on robot learning_ , pages 143–156. PMLR, 2017. 

- [27] Kun Lei, Huanyu Li, Dongjie Yu, Zhenyu Wei, Lingxiao Guo, Zhennan Jiang, Ziyu Wang, Shiyu Liang, and Huazhe Xu. Rl-100: Performant robotic manipulation with real-world reinforcement learning. _arXiv preprint arXiv:2510.14830_ , 2025. 

- [28] Sergey Levine, Aviral Kumar, George Tucker, and Justin Fu. Offline reinforcement learning: Tutorial, review, and perspectives on open problems. _arXiv preprint arXiv:2005.01643_ , 2020. 

- [29] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 

- [30] Yunfei Li, Xiao Ma, Jiafeng Xu, Yu Cui, Zhongren Cui, 

Zhigang Han, Liqun Huang, Tao Kong, Yuxiao Liu, Hao Niu, et al. Gr-rl: Going dexterous and precise for long-horizon robotic manipulation. _arXiv preprint arXiv:2512.01801_ , 2025. 

- [31] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-languageaction model. _arXiv preprint arXiv:2503.10631_ , 2025. 

- [32] Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qingmin Liao, Yi Wu, Chao Yu, and Yu Wang. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025. 

- [33] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- [34] Yi Liu, Sukai Wang, Dafeng Wei, Xiaowei Cai, Linqing Zhong, Jiange Yang, Guanghui Ren, Jinyu Zhang, Maoqing Yao, Chuankang Li, et al. Unified embodied vlm reasoning with robotic action via autoregressive discretized pre-training. _arXiv preprint arXiv:2512.24125_ , 2025. 

- [35] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 

- [36] Jianlan Luo, Zheyuan Hu, Charles Xu, You Liang Tan, Jacob Berg, Archit Sharma, Stefan Schaal, Chelsea Finn, Abhishek Gupta, and Sergey Levine. Serl: A software suite for sample-efficient robotic reinforcement learning. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 16961–16969. IEEE, 2024. 

- [37] Jianlan Luo, Charles Xu, Jeffrey Wu, and Sergey Levine. Precise and dexterous robotic manipulation via humanin-the-loop reinforcement learning. _Science Robotics_ , 10 (105):eads5033, 2025. 

- [38] Zhao Mandi, Homanga Bharadhwaj, Vincent Moens, Shuran Song, Aravind Rajeswaran, and Vikash Kumar. Cacti: A framework for scalable multi-task multi-scene visual imitation learning. _arXiv preprint arXiv:2212.05711_ , 2022. 

- [39] HKU MMLab. A live-stream robotic teamwork for clothing manipulation from zero to hero. _HKU MMLab Research Blog_ , 2025. https://mmlab.hk/research/kai0. 

- [40] Volodymyr Mnih, Adria Puigdomenech Badia, Mehdi Mirza, Alex Graves, Timothy Lillicrap, Tim Harley, David Silver, and Koray Kavukcuoglu. Asynchronous methods for deep reinforcement learning. In _International conference on machine learning_ , pages 1928– 1937. PmLR, 2016. 

- [41] Ashvin Nair, Abhishek Gupta, Murtaza Dalal, and Sergey Levine. Awac: Accelerating online reinforcement learning with offline datasets. _arXiv preprint arXiv:2006.09359_ , 2020. 

- [42] NVIDIA, :, Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi ”Jim” Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith Llontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. URL https://arxiv.org/abs/2503.14734. 

- [43] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ , 35:27730–27744, 2022. 

- [44] St´ephane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- [45] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [46] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. Deepseekmath: Pushing the limits of mathematical reasoning in open language models, 2024. URL https://arxiv.org/abs/2402. 03300. 

- [47] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- [48] Avi Singh, Eric Jang, Alexander Irpan, Daniel Kappler, Murtaza Dalal, Sergey Levine, Mohi Khansari, and Chelsea Finn. Scalable multi-task imitation learning with autonomous improvement. In _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2167–2173. IEEE, 2020. 

- [49] Richard S Sutton and Andrew G Barto. Reinforcement learning: An introduction, mit press. _Cambridge, MA_ , 22447(10), 1998. 

- [50] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [51] TRI LBM Team, Jose Barreiros, Andrew Beaulieu, Aditya Bhat, Rick Cory, Eric Cousineau, Hongkai Dai, Ching-Hsin Fang, Kunimatsu Hashimoto, Muhammad Zubair Irshad, Masha Itkina, Naveen Kuppuswamy, Kuan-Hui Lee, Katherine Liu, Dale McConachie, Ian McMahon, Haruki Nishimura, Calder Phillips-Grafflin, Charles Richter, Paarth Shah, Krishnan Srinivasan, Blake Wulfe, Chen Xu, Mengchao Zhang, Alex Alspach, Maya Angeles, Kushal Arora, Vitor Campagnolo Guizilini, Alejandro Castro, Dian Chen, Ting-Sheng Chu, Sam Creasey, Sean Curtis, Richard Denitto, Emma Dixon, Eric Dusel, Matthew Ferreira, Aimee Goncalves, Grant Gould, Damrong Guoy, Swati Gupta, Xuchen Han, Kyle Hatch, Brendan Hathaway, Allison Henry, Hillel Hochsztein, Phoebe Horgan, Shun Iwase, Donovon Jackson, Siddharth Karamcheti, Sedrick Keh, Joseph Masterjohn, Jean Mercat, Patrick Miller, Paul Mitiguy, Tony Nguyen, Jeremy Nimmer, Yuki Noguchi, Reko Ong, Aykut Onol, Owen Pfannenstiehl, Richard Poyner, Leticia Priebe Mendes Rocha, Gordon Richardson, Christopher Rodriguez, Derick Seale, Michael Sherman, Mariah Smith-Jones, David Tago, Pavel Tokmakov, Matthew Tran, Basile Van Hoorick, Igor Vasiljevic, Sergey Zakharov, Mark Zolotas, Rares Ambrus, Kerri FetzerBorelli, Benjamin Burchfiel, Hadas Kress-Gazit, Siyuan Feng, Stacie Ford, and Russ Tedrake. A careful examination of large behavior models for multitask dexterous manipulation, 2025. URL https://arxiv.org/abs/2507.05331. 

- [52] Ziyu Wang, Alexander Novikov, Konrad Zolna, Josh S Merel, Jost Tobias Springenberg, Scott E Reed, Bobak Shahriari, Noah Siegel, Caglar Gulcehre, Nicolas Heess, et al. Critic regularized regression. _Advances in Neural Information Processing Systems_ , 33:7768–7778, 2020. 

- [53] Charles Xu, Qiyang Li, Jianlan Luo, and Sergey Levine. Rldg: Robotic generalist policy distillation via reinforcement learning. _arXiv preprint arXiv:2412.09858_ , 2024. 

- [54] Zhewei Yao, Reza Yazdani Aminabadi, Olatunji Ruwase, Samyam Rajbhandari, Xiaoxia Wu, Ammar Ahmad Awan, Jeff Rasley, Minjia Zhang, Conglong Li, Connor Holmes, et al. Deepspeed-chat: Easy, fast and affordable rlhf training of chatgpt-like models at all scales. _arXiv preprint arXiv:2308.01320_ , 2023. 

- [55] Shaopeng Zhai, Qi Zhang, Tianyi Zhang, Fuxian Huang, Haoran Zhang, Ming Zhou, Shengzhe Zhang, Litao Liu, Sixu Lin, and Jiangmiao Pang. A vision-languageaction-critic model for robotic real-world reinforcement learning, 2025. URL https://arxiv.org/abs/2509.15937. 

- [56] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- [57] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. 

PMLR, 2023. 

## APPENDIX 

## _A. Robot Platform Setup_ 

Our robot platform for experiments and evaluations is Agibot G1 dual-arm manipulator. Each G1 robot has two 7- DoF arms with parallel-jaw grippers and three RGB cameras (one base view mounted on the top head of the G1 robot and two wrist views mounted above the grippers), as illustrated in Figure 6. Our policy executes joint position control at 30 Hz. 


Fig. 6: Robot platform setup in our experiments. 

_B. Data Infrastructure Details_ 


Fig. 7: Distributed data infrastructure architecture. Robot actors upload episodes to object storage and publish event notifications to a message queue. The cloud learner consumes notifications, retrieves episode data, and streams updated model parameters back to all actors via the publish–subscribe channel. 

_1) System Architecture:_ Our distributed data infrastructure implements a closed-loop actor–learner architecture comprising five core components, as illustrated in Figure 7. 

On the actor side, each robot runs an _edge client_ responsible for buffering frame-level observations locally and assembling them into complete episodes. Upon episode termination, the client serializes the episode data and uploads it to a _distributed object storage_ layer (compatible with S3-like interfaces), while simultaneously publishing an event notification to a _message queue_ . 

On the learner side, a _data consumption service_ subscribes to the message queue, retrieves newly uploaded episodes from object storage, and expands them into frame-level metadata entries in an in-memory index. A _training dataloader_ then 

samples from this index according to configurable strategies and fetches the corresponding payload data on demand. 

To complete the feedback loop, the learner broadcasts updated model parameters back to all actors through a publish– subscribe channel, enabling actors to refresh their local policies at episode boundaries without interrupting ongoing data collection. 

This architecture cleanly separates the data production pipeline (actors) from the data consumption pipeline (learner), allowing each to scale independently. The message queue serves as the decoupling layer that absorbs transient load imbalances and network disruptions. 

_2) Design Advantages:_ The above architecture provides three key advantages for large-scale online post-training. 

**Elastic Horizontal Scaling.** A key design principle is zero-configuration scalability. New robot actors can join the data collection fleet by simply connecting to the message queue—no code modifications or system reconfiguration required. The cloud learner automatically discovers and consumes data from all active actors through consumer groups that provide native load balancing. This enables seamless scaling from single-robot experiments to fleets of hundreds of robots without architectural changes. 

**Persistent and Fault-Tolerant Data Management.** All episode data are durably persisted to distributed object storage with atomic write semantics—either an entire episode is successfully stored, or the operation is rolled back entirely. The message queue provides guaranteed delivery with automatic retry mechanisms, ensuring no data loss even under network partitions or node failures. This reliability is critical for long-running training campaigns where data integrity directly impacts model quality. 

**Separation of Metadata and Payload.** To support millionscale episode sampling efficiently, we decouple lightweight metadata (episode identifiers, frame counts, sampling weights) from heavy payload data (images, sensor readings). Metadata resides in memory to enable high-frequency sampling decisions, while actual frame data are lazily loaded from object storage only when selected for training. This design reduces memory footprint by over two orders of magnitude compared to full data loading, making it feasible to maintain replay buffers spanning millions of frames on commodity hardware. 

latest published checkpoint. During post-training, we freeze the LLM backbone and train the vision components and action experts. To keep deployment practical, we only distribute the necessary updated weights; the transmitted checkpoint artifact is about 780 MB. 

_3) RECAP Implementation Details:_ To achieve a generalist policy, we implement RECAP in a multi-task post-training recipe rather than as a task-specific fine-tuning method. The policy improvements of RECAP follows 


where _π_ ref is the behavior policy from the collected dataset and _I_ = **1** ( _A_<sup>_π_ref</sup> ( _st, at_ ) _> ϵ_ ) is the advantage condition approximated by value function. In our multi-task setting, different advantage thresholds _ϵ_ are imposed since the episode lengths varies across different tasks. 

For the SOP-RECAP experiment, online training is following the training setup as mentioned in C2 where only the vision components and action expert are updated. Value function is pretrained offline and is not being updated along policy training. Applying SOP with RECAP, the policy executed by actor ends in Algorithm 1 accords to (4), and the policy parameters is updated according to the training objective in RECAP. For the RECAP-alone experiment, we execute 2 iterations, achieve a performance improvement on the multi-task setting, as presented in Fig. 4. The parameter _β_ during rollout data collection phase and online inference phase is set to 1.0; in the evaluation phase, moderate settings _β ∈_ [1 _._ 5 _,_ 2 _._ 5] are adopted. 

To validate the effectiveness of our RECAP implementation across multi-tasks, ablation studies are made for 2 single tasks (freezer restocking and open-cooler restocking) in the Grocery Restocking category. On the freezer restocking task, the success rate of single-task RECAP vs multi-task RECAP is 0.75 vs 0.75; on the open-cooler restocking task, the success rate is 0.86 vs 0.8. 

## _C. Implementation Details_ 

_1) Pre-trained Base Policy:_ All SOP post-training experiments initialize from a pretrained vision-language-action (VLA) base policy, denoted as _πθ_ 0. Here, _πθ_ 0 is obtained by tuning _π_ 0 _._ 5 model on our multi-task robot dataset (about 160 hours in total: 100 hours for Grocery Restocking, 30 hours for Laundry Folding, and 30 hours for Box Assembly). Unless otherwise specified, we use **Base-Full** ( _πθ_ 0 pretrained on our full dataset) as the initialization for the main experiments. 

_2) SOP Training Details:_ Post-training is run with a centralized cloud learner using 8 NVIDIA H100 GPUs. The learner publishes updated model parameters every 25 training steps, and robot actors refresh their local policies using the 

