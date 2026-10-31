---
title: "APEX: Learning Adaptive High-Platform Traversal for Humanoid Robots"
date: "2026-02-11"
authors: "Yikai Wang; Tingxuan Leng; Changyi Lin; Shiqi Liu; Shir Simon; Bingqing Chen"
url: https://arxiv.org/abs/2602.11143
pdf: https://arxiv.org/pdf/2602.11143
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.11143)** / [論文ページ](https://arxiv.org/abs/2602.11143)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# APEX: Learning Adaptive High-Platform Traversal for Humanoid Robots 

Yikai Wang<sup>*1</sup> , Tingxuan Leng<sup>*1</sup> , Changyi Lin<sup>*1</sup> , Shiqi Liu<sup>1</sup> , Shir Simon<sup>2</sup> , Bingqing Chen<sup>2</sup> , Jonathan Francis<sup>1,2</sup> , Ding Zhao<sup>1</sup> 

> 1Carnegie Mellon University 2Bosch Center for Artificial Intelligence 


Fig. 1: The robot adaptively traverses high platforms of up to 0 _._ 8 m ( _≈_ 114% of leg length) by leveraging diverse full-body behaviors, including climb-up, climb-down, stand-up, lie-down. Enabled by LiDAR-based elevation mapping, the policy exhibits context-aware whole-body coordination, allowing continuous and robust traversal across challenging terrain (project webpage). 

**_Abstract_ —Humanoid locomotion has advanced rapidly with deep reinforcement learning (DRL), enabling robust feet-based traversal over uneven terrain. Yet platforms beyond leg length remain largely out of reach because current RL training paradigms often converge to jumping-like solutions that are high-impact, torque-limited, and unsafe for real-world deployment. To address this gap, we propose** **_APEX_ , a system for perceptive, climbingbased high-platform traversal that composes terrain-conditioned behaviors: climb-up and climb-down at vertical edges, walking or crawling on the platform, and stand-up and lie-down for posture reconfiguration. Central to our approach is a generalized ratchet progress reward for learning contact-rich, goal-reaching maneuvers. It tracks best-so-far task progress and penalizes non-improving steps, which provides dense yet velocity-free supervision, enabling efficient exploration under strong safety regularization. Based on it, we train LiDAR-based full-body maneuver policies and reduce the sim-to-real perception gap via a dual strategy: training-time modeling of mapping artifacts and deployment-time filtering and inpainting of elevation maps. Finally, we distill all six skills into a single policy that au-** 

**tonomously selects behaviors and transitions from local geometry and commands. Experiments on a 29-DoF Unitree G1 humanoid demonstrate zero-shot sim-to-real traversal of** 0 _._ 8 **m platforms (** _≈_ 114% **of leg length), with robust adaptation to platform height and initial pose and smooth, stable multi-skill transitions.** 

## I. INTRODUCTION 

Locomotion is a fundamental capability for humanoid robots, yet has long remained challenging. Recent advances in deep reinforcement learning (DRL) have enabled robust, feet-based locomotion over uneven terrains [1, 2]. To further expand traversable terrain, prior systems have also learned whole-body jumping to get onto and off elevated structures [3, 4, 5]. However, jumping-based solutions typically achieve limited height (often below 63% of leg length). Directly scaling them to substantially higher platforms (e.g., ledges or tables exceeding 100% of leg length) requires large impulsive torques and induces high-impact dynamics, which can exceed actuator limits and pose unacceptable risk in real-world deployment. 

*Equal contribution 

For such extreme heights, a more reliable alternative is fullbody climbing, which coordinates arms, torso, and legs to create distributed supports to ascend or descend in a controlled manner. Building on climbing, complete high-platform traversal involves multiple behaviors: climb-up and climb-down at vertical edges, walking or crawling on the platform, standup and lie-down for posture reconfiguration between prone and upright configurations. Despite its promise, learning and executing high-platform traversal presents two key challenges. 

First, the four full-body maneuvers (climb-up, climb-down, stand-up, and lie-down) are difficult to learn with DRL. In contrast to cyclic, command-conditioned locomotion (e.g., walking, running, or crawling), where tracking objectives such as base velocity and periodic contacts provide dense supervision, these maneuvers are contact-rich and goal-reaching. Success is defined by satisfying terminal conditions through staged contact transitions and whole-body reconfiguration (e.g., moving the lower body and center of mass above the platform during climb-up). Their contact patterns and motion velocities vary across phases and depend on perceived geometry, making such dense locomotion-style tracking rewards ill-defined. 

Second, complete high-platform traversal is a long-horizon sequential problem that requires autonomous skill selection and seamless switching. A unified end-to-end policy must (i) acquire a diverse repertoire of skills, (ii) infer the appropriate behavior from local terrain observations and high-level user commands, and (iii) trigger smooth transitions at the correct moments while maintaining robot stability. These requirements couple perception, high-level decision-making, and low-level control across extended, multi-contact interaction phases, substantially increasing the difficulty of learning. 

To address these challenges, we propose _APEX_ , a system for learning _adaptive high-platform traversal_ based on a twostage framework. First, we train a library of six skills via DRL: the four goal-reaching full-body maneuvers and two cyclic locomotion skills. To make the goal-reaching maneuvers learnable and deployable, we introduce a generalized _ratchet progress_ reward that maintains a self-updating bestso-far task state and penalizes the agent unless it strictly surpasses this state. This yields dense, task-aligned supervision while remaining velocity-free, enabling efficient exploration under strong safety regularization and preventing “retrace” exploitation. For perception, we leverage a LiDAR-based elevation mapping pipeline and bridge the sim-to-real gap with a dual strategy: training-time modeling of mapping artifacts and deployment-time filtering and inpainting of raw maps. To make the learned skills ready for seamless transitions, we improve distribution matching between the predecessor’s terminal states and the successor’s initial states with strategies on reward design and data sampling. We then distill the six teacher policies into a unified student policy, training on a mixture of skill-focused and transition-focused environments. With these design choices, our unified policy achieves complete traversal of a 0 _._ 8 m platform ( _≈_ 114% of leg length) with zero-shot sim-to-real transfer on a 29-DoF Unitree G1 humanoid robot, and remains robust under variations in platform height and 

initial robot pose. We further conduct extensive comparisons showing that the proposed ratchet progress reward is critical for learning adaptive contact-rich maneuvers. 

In summary, our contributions are: 

- A two-stage learning framework for adaptive highplatform traversal that integrates contact-rich full-body maneuvers and cyclic locomotion into a single controller. 

- A generalized ratchet progress reward that provides dense, velocity-free supervision for learning deployable contact-rich, goal-reaching maneuvers. 

- The first humanoid traversal policy that achieves realworld traversal over platforms exceeding 114% of leg length, demonstrating robust adaptation, autonomous skill selection, and smooth transitions. 

## II. RELATED WORK 

We review prior works in three aspects most relevant to our system, and summarize key distinctions in Tab. I. 

TABLE I: Comparison with existing methods on humanoid full-body maneuver capabilities. Extreme height is defined as platforms exceeding 100% of leg length. 

|Methods|Parkour<br>[3, 4, 5]|Stand-Up<br>[6, 7, 8]|Trajectory<br>Tracking<br>[9]|Motion<br>Generation<br>[10]|**APEX**<br>**(Ours)**|
|---|---|---|---|---|---|
|Extreme height|✗|✗|✓|✓|✓|
|Full-body contact|✗|✓|✓|✗|✓|
|Terrain perception|✓|✗|✗|✓|✓|
|Terrain/pose-adaptive|✓|✓|✗|✓|✓|
|Reference-free|✓|✓|✗|✗|✓|
|Real robot|✓|✓|✓|✗|✓|
|Unified multi-skill|✓|✗|✗|✗|✓|


## _A. Learning Feet-Based Locomotion_ 

Deep reinforcement learning (DRL) has substantially improved the robustness and agility of legged locomotion, with early successes on quadrupeds [11, 12, 13, 14] and recent progress on humanoids. Humanoids with learned controllers can walk and run in uneven terrain [15, 16, 2], traverse sparse footholds [17, 18, 19], and step or jump into elevated structures [3, 4, 5]. However, these methods primarily rely on _feet-only_ contacts, which requires large impulsive torques to reach high platforms, resulting in limited height (typically below 63% of leg length). In contrast, our system exploits whole-body, multi-contact coordination to distribute load and traverse platforms exceeding 114% of leg length. 

## _B. Learning Humanoid Full-Body Maneuvers_ 

Recent work has started to learn individual full-body maneuvers such as stand-up [6, 7, 8]. However, these methods often use task rewards that conflict with safety regularization and therefore require multi-stage pipelines or rely on heavy task-specific engineering (e.g., virtual-force shaping and carefully tuned curriculum for regularization and action rescaling), which has largely limited progress to relatively simple behaviors. In contrast, our generalized _ratchet progress_ 


Fig. 2: **Learning pipeline for high-platform traversal:** Teacher Training uses RL with the Ratchet Progress Reward, where a ”best-so-far” task-space reference ensures genuine advancement by only rewarding states that strictly surpass historical progress. These skills are unified into a single context-aware policy through Distillation, using a “divide-and-conquer” Data Sampling Rule across distributed environments to cover the full distribution of maneuvers and transitions. In Deployment, the humanoid robot performs end-to-end traversal using LiDAR-based elevation mapping for terrain adaptation. 

reward supports single-stage RL training for multiple contactrich, goal-reaching maneuvers, while jointly optimizing task completion and safety regularization. 

A complementary line of work learns human-like behaviors (e.g., dancing, walking, crawling, and jumping) by training policies to track human motions [20, 21, 22, 23, 24, 25, 26] using dense imitation rewards [27]. Building on these foundations, OmniRetarget [9] enables full-body climbing by preserving robot-scene contact relationships during retargeting. However, motion-tracking approaches fundamentally rely on prerecorded trajectories and therefore require close alignment between the reference motion, the environment geometry, and the robot’s initial state. This strongly limits adaptation to unseen terrain and initial conditions common in real deployment. Motion generation models [28, 29, 30] could in principle provide adaptive references, but generated motions are often physics-infeasible and do not explicitly reason about multicontact feasibility and deployment constraints (e.g. torque limit, contact force, generation speed, perception gap) ; consequently, they are typically validated only in simulation [10]. In contrast, our policy is perceptive, reference-free, and deployable: it learns terrain-conditioned strategies that generalize across platform heights and initial poses, enabling autonomous traversal in diverse real-world environments. 

## _C. Policy Distillation for Legged Robots_ 

Teacher-student distillation is widely used to train deployable policies for legged robots [31, 32, 33, 34, 35, 36]. A common paradigm trains a teacher with privileged simulation information and distills it into a student that relies only on onboard observations (e.g., depth images or tactile signals) for deployment. More recently, multi-expert distillation has 

been used to integrate terrain-conditioned skills into a single quadrupedal policy [37, 38], typically using DAgger-style [39] data aggregation, which we also adopt. However, existing multi-skill distillation has largely focused on quadrupeds, where skills share similar feet-contact modes and transitions occur near a nominal walking posture. In contrast, our teacher set spans heterogeneous humanoid behaviors, including fullbody maneuvers and locomotion skills with substantially different state and action distributions (e.g., climbing, walking, crawling, and posture transitions). This substantially increases the difficulty of both RL and distillation training: the teacher skills must be trained with compatible terminal-state distributions to enable safe and smooth concatenation, and appropriate teacher actions should be provided conditioned not only on terrain geometry and user commands, but also on the robot state and transition progress. 

## III. HIGH-PLATFORM TRAVERSAL POLICY LEARNING 

Our goal is to learn a perceptive humanoid policy that can robustly traverse extremely high platforms in the real world. As introduced in Sec. I, such traversal requires multiple terrain-conditioned behaviors: four full-body maneuvers ( _climb-up, climb-down, stand-up, lie-down_ ) and two standard locomotion skills (walking, crawling). To handle this diversity, we adopt a two-stage learning pipeline [35, 36] as shown in Fig. 2. First, we develop a unified RL training framework to learn the four full-body maneuver policies with LiDAR perception (Sec. III-B). To enable efficient learning of these contact-rich goal-reaching tasks, we introduce a generalized _ratchet progress_ reward that provides dense supervision while supporting exploration under strong safety regularization (Sec. III-A). Second, we distill all six policies 

into a unified single policy that autonomously selects and transitions between behaviors based on perception, enabling end-to-end high-platform traversal (Sec. III-C). 

## _A. Ratchet Progress Reward for Humanoid Maneuvers_ 

## _1) Task Definition:_ 

We model the full-body, contact-rich humanoid maneuver as a goal-reaching task, where success is defined by satisfying a terminal condition rather than tracking a reference trajectory. Let _st_ denote the robot state at timestep _t_ . We define a _task state xt_ = _ϕ_ ( _st_ ), where _ϕ_ ( _·_ ) extracts a minimal set of variables needed to evaluate task completion. For each maneuver, we specify a target task state _x_<sup>_g_</sup> and declare success when _xt ≥ x_<sup>_g_</sup> , where _≥_ denotes the ordering induced by the task metric. 

To instantiate the four maneuver objectives (Tab. II), we use the following notation. _pCoM_ , _phead_ , and _pLB_ denote the positions of the full-body center of mass, head, and lower body, respectively. We use _h_ and _x_ to denote environment- and pose-dependent thresholds, such as the platform edge height _hedge_ or the nominal standing head height _hhead_<sup>_stand_. For standing</sup> stability, we define a balance margin _dbal_ = _∥pCoM − p_ ¯ _feet∥_ where _p_ ¯ _feet_ is the geometric center of the feet. These definitions yield concise, task-specific terminal conditions while keeping _xt_ low-dimensional and easy to compute online. 

TABLE II: Task Definition of Four Goal-Reaching Maneuvers 

|**Task**|**Task State (**_xt_**)**|**Target Task State (**_x_<sup>_g_</sup>**)**|
|---|---|---|
|**Climb-up**|_pCoM, pLB_|_p_<sup>(</sup><sup>_z_)</sup><br>_LB _<sup>_> hedge ∧p_(</sup><sup>_x_)</sup><br>_CoM _<sup>_> xedge_</sup>|
|**Climb-down**|_pCoM, pLB_|_p_<sup>(</sup><sup>_z_)</sup><br>_LB _<sup>_< hstand_</sup><br>_LB_<br>_∧p_<sup>(</sup><sup>_x_)</sup><br>_CoM _<sup>_< xedge_</sup>|
|**Stand-up**|_p_<sup>(</sup><sup>_z_)</sup><br>_head_<sup>_, dbal_</sup>|_p_<sup>(</sup><sup>_z_)</sup><br>_head _<sup>_> hstand_</sup><br>_head _<sup>_∧dbal < δ_</sup>|
|**Lie-down**|_pCoM, phead_|_p_<sup>(</sup><sup>_z_)</sup><br>_CoM _<sup>_< hprone_</sup><br>_CoM _<sup>_∧p_(</sup><sup>_z_)</sup><br>_head _<sup>_< hprone_</sup><br>_head_|


## _2) Ratchet Progress Reward:_ 

These goal-reaching maneuvers do not admit a phaseinvariant predefined reference, such as a consistent velocity or contact pattern for command-conditioned locomotion. To provide a meaningful reference at every timestep without prescribing a motion template, we introduce a _self-updating task-space reference_ that records the best progress achieved so far along the trajectory. This best-so-far task state at timestep _t_ is defined as: 


which can be updated online via _x_<sup>_∗_</sup> _t_<sup>= max(</sup><sup>_x∗_</sup> _t−_ 1<sup>_, xt−_1),with</sup> _x_<sup>_∗_</sup> 0<sup>=</sup><sup>_x_0.Intuitively,</sup><sup>_x_</sup> _t_<sup>_∗_tracksthecurrentfrontieroftask-</sup> space progress demonstrated by the agent. 

Based on the best-so-far task-space reference, we define a binary _ratchet progress_ task reward: 


That is, the agent receives no penalty only when it _strictly surpasses_ its historical best, and is penalized otherwise. Although 

simple, the above construction is tailored to contact-rich, goalreaching maneuvers, with three key properties. 

• **Dense task-aligned supervision.** The reward is evaluated at every timestep to penalize any failure to exceed the best-so-far progress. This provides a dense signal that keeps exploration within task-relevant behaviors, which is essential for contactrich maneuvers where terminal-only rewards are too sparse to discover feasible contact sequences. 

• **Velocity-free progress enables exploration and deployment.** Because the reward depends only on _whether_ progress improves but not _how much_ , it does not encourage rushing in task space. This supports (i) _patient, contact-aware exploration_ , allowing the robot to hold intermediate supports until necessary contacts become stable (e.g., during climbup, keep one leg grounded until the other stably lands on the platform; during stand-up, hold torso ascent until limbs become load-bearing), and (ii) _effective regularization_ of impact/torque/force can enforce safe motions without having to counteract a velocity-driven task incentive. 

• **History dependence prevents retracing exploits.** Incremental criteria such as ( _xt > xt−_ 1) can be gamed by oscillating backward and forward. In contrast, our historical best criteria ( _xt > x_<sup>_∗_</sup> _t_<sup>)ensuresoptimizationwithgenuine</sup> advancement toward the goal. 

## _B. Learning Perceptive Full-Body Maneuvers_ 

In this section, we present our RL framework for learning the four full-body maneuver skills. For brevity, we omit the training details of the two standard locomotion skills, as they follow a conventional velocity-tracking formulation. 

## _1) RL Training Environment:_ 

**State, Observation, and Action.** We train each maneuver as a single-skill policy in a Markov Decision Process (MDP). The observation space includes robot proprioception _s_<sup>proprio</sup> _t ∈_ R<sup>64</sup> (gravity vector, base angular velocity, and joint positions/velocities), the previous action _at−_ 1 _∈_ R<sup>29</sup> , the task state _xt_ , and optionally a local elevation map _mt ∈_ R<sup>441</sup> at 0 _._ 05 m resolution covering a 1 _×_ 1 m<sup>2</sup> area. All policies take a 5-step history of ( _s_<sup>proprio</sup> _t , at−_ 1) to capture short-term dynamics. Because the climbing skills must perceive the platform geometry, the _climb-up_ and _climb-down_ policies additionally take _mt_ as input. All policies output target joint positions _at ∈_ R<sup>29</sup> , which are tracked by a low-level PD controller. Our task reward depends on the best-so-far task state _x_<sup>_∗_</sup> _t_<sup>,</sup> which evolves over time and is not included in the instantaneous robot state. This creates history dependence that can impair value estimation if the critic observes only _st_ . To address this, we provide _x_<sup>_∗_</sup> _t_<sup>asadditionalinputtothecritic.</sup> 

**Simulation Environment.** To learn adaptive behaviors, we extensively randomize the terrain configuration and initial conditions. The platform height is sampled from [0 _._ 55 m _,_ 0 _._ 85 m]. For _climb-up_ , the initial distance from the robot base to the vertical surface and the initial yaw angle are sampled from [0 _._ 15 m _,_ 0 _._ 35 m] and [ _−_ 60<sup>_◦_</sup> _,_ 60<sup>_◦_</sup> ]; for _climb-down_ , they are sampled from [0 _._ 30 m _,_ 0 _._ 45 m] and [ _−_ 75<sup>_◦_</sup> _,_ 75<sup>_◦_</sup> ]. To improve sim-to-real transfer, we apply a comprehensive suite of domain 

randomization following [26]. We further apply symmetric augmentation [40] to reduce handedness bias and improve generalization across approach angles. 

**Initial Posture Sampling.** Since single-skill policies are executed sequentially during distillation, their initial-state distributions must encompass the terminal states generated by preceding skills. As illustrated in Fig. 2, transitions predominantly occur around two canonical postures: standing (start of walking, climb-up, and lie-down; end of walking, climb-down, and stand-up) and prone (start of crawling, climb-down, and stand-up; end of crawling, climb-up, and lie-down). We define nominal joint configurations for these postures as _q_ stand and _q_ prone, respectively. 

For each skill, initial joint angles are sampled by perturbing the corresponding nominal starting posture, ensuring that training begins from physically plausible states that are compatible with upstream transitions. To enable seamless switch-out between skills, we additionally shape the terminal behavior of full-body maneuvers toward the nominal ending posture using a terminal-pose reward (Sec. III-B2). If the reachable terminal-state distribution of a skill is not fully contained within the initial-state distribution of its successor, we subsequently retrain the successor skill while augmenting its initial-state distribution to cover all possible terminal configurations produced by its predecessors. 

_2) Reward Design:_ 

We define the total reward as the sum of five components: 


The first three terms _r_ alive, _r_ reg, and _r_ force, are shared across all maneuvers. _r_ alive is a constant survival bonus that discourages early termination. _r_ reg aggregates standard regularization penalties that promote smooth and energy-efficient motions. 

Because full-body maneuvers involve frequent terrain contacts beyond the feet, limiting impact is critical for safe deployment. We therefore include a contact-force penalty _r_ force that grows rapidly once contact forces exceed a safe threshold: 


where _Ft_ is the maximum contact force at timestep _t_ , _Flimit_ is a safety threshold, and _α >_ 0 controls the penalty scale. Specially, we set _Flimit_ = 0 for the head link, since even light head contact can destabilize the head-mounted LiDAR and severely degrade perception. 

The remaining two terms, _r_ task and _r_ tp, are task-specific but require only minimal specification. _r_ task is the ratchet progress reward introduced in Sec. III-A, which drives goal completion. _r_ tp encourages a desired terminal posture to facilitate reliable behavior transitions. It is activated _only_ after the goal is reached and within the final second of an episode: 


where I is the indicator function, _H_ is the episode duration, _qt_ and _qtar_ denote the current and desired terminal joint angles of the robot, and _β >_ 0 is a scale parameter. 


Fig. 3: The sim-to-real gap in LiDAR mapping is addressed through a dual approach that combines artifact modeling in simulation with real-world post-processing. 

_3) Robust Perception via Elevation Mapping:_ We implement a LiDAR-based elevation mapping pipeline following prior humanoid locomotion work [1]. However, dynamic maneuvers introduce perceptual degradation: rapid accelerations and contact-induced disturbances accumulate localization drift; self-occlusion from the robot’s limbs produces spurious point clusters; extreme body configurations limit field of view; and probabilistic elevation fusion yields uncertain or missing measurements. To mitigate the sim-to-real perception gap induced by these, we adopt a dual strategy (Fig. 3): 

- **Simulation Artifact Modeling:** During training, we explicitly inject three classes of perceptual artifacts to improve robustness: per-cell Gaussian noise to emulate mapping uncertainty and self-scanning effects, spatial offsets to simulate localization drift, and synthetic outlier clusters to reproduce spurious obstacle artifacts. 

- **Real-World Post-Processing:** We apply a spatial outlier filter to suppress high-variance noise clusters and an inpainting algorithm [41] to reconstruct missing elevation regions, providing the policy with a structurally coherent terrain representation. 

## _C. Policy Distillation for Skill Integration_ 

To obtain a unified, context-aware controller from our diverse skill library, we adopt a distillation pipeline inspired by [36]. Specifically, we first leverage Behavior Cloning (BC) [42] to pretrain a student policy, and then refine it using DAgger [39] to improve robustness and distributional coverage. We dynamically select the appropriate teacher based on the robot’s state and and commanded velocity, optimizing the policy using the Mean Squared Error (MSE) between the student and teacher actions. 

_1) Construction of Data Distribution:_ A standard sequential sampling strategy [37] is unsuitable for high-platform traversal distillation, which involves multiple substantially different behaviors. Rollouts starting from the traversal initial state produce highly imbalanced data. For example, predom- 


Fig. 4: The robot regains balance and climbs up the high platform after being heavily kicked. 

inantly walking data in early stages, or no climb-down data until a successful climb-up occurs. To obtain a more balanced dataset across all teacher policies while covering possible skill transitions, we introduce a “divide-and-conquer” strategy: each training environment is assigned either to a single core skill or to a combination of two consecutive skills. More detail for the environment definition is provided in the Appendix. 

_2) Data Augmentation Strategy:_ We incorporate the full suite of configurations utilized during teacher training, including domain randomization, physical perturbations, and perception artifacts. The first skill in each sub-environment is initialized from a broader range of states to maximize statespace coverage for the student policy. Additionally, we apply action noise and symmetry augmentation during the distillation process to improve the robustness of the unified policy. 

## IV. EXPERIMENTS 

In this section, we present a series of qualitative and quantitative evaluations to address the following questions: 

TABLE III: Comparative Success Rates of Single Skill in Sim and Real. SR: Success Rate; S/T: Success / Trials; M.C.F.: Max Contact Force; _H_ (m): platform height; _A_ (<sup>_◦_</sup> ): approach angle relative to the platform-edge normal. 

||**Sim**<br>|**ulation**<br>||**Re**<br>|**al Wo**<br>|**rld**<br>||
|---|---|---|---|---|---|---|---|
|**Task**|**S.R. (%) **|**M.C.F. (N)**|_H_ **(m)**|_A_ **(**|<sup>_◦_</sup>**)**|**S/T **|**S.R. (%)**|
||||0.6|[_−_45_, _<br>|_−_15]<br>|5/5||
||||0.6|[_−_15_,_ <br>|+15]<br>|5/5||
||||0.6|[+15_,_|+45]|5/5||
|Climb-up|98.8|638<br>_±_479|0.7<br>0.7|[_−_45_, _<br>[_−_15_,_|_−_15]<br>+15]|4/5<br>5/5|97.8|
||||0.7|[+15_,_|+45]|5/5||
||||0.8|[_−_45_, _|_−_15]|5/5||
||||0.8|[_−_15_,_|+15]|5/5||
||||0.8|[+15_,_|+45]|5/5||
|Climb-down|99.9|754<br>_±_241|0.8|[_−_45_,_|+45]|5/5|100.0|
|Stand-up|99.5|632<br>_±_222|–|–||5/5|100.0|
|Lie-down|100.0|576<br>_±_125|–|–||5/5|100.0|


- 1) Does the proposed system enable context-aware traversal via coordinated skill execution (Sec. IV-A)? 

- 2) Do the learned policies demonstrate robustness and adaptability to environmental variations (Sec. IV-B)? 

- 3) How does the proposed ratchet progress reward facilitate the acquisition of full-body maneuvers (Sec. IV-C)? 

Experiments are conducted on a 29-DoF Unitree G1 humanoid robot in both simulation and real-world settings. 

## _A. Performance of Context-Aware Continuous Traversal_ 

**The system enables continuous traversal via coordinated skills.** To evaluate context-aware traversal across high platforms, we design three challenging simulation courses requiring long-horizon execution without resets (Fig. 1). These courses— _Continuous Traversing_ , _Ascending_ , and _Descending_ —combine acyclic maneuvers (e.g., climbing, standing up, lying down) with periodic gaits (e.g., walking) into cohesive traversal sequences. Successful completion requires the policy to autonomously determine skill transitions based on terrain context. The robot is commanded via velocity inputs, while standing up and lying down are triggered by the user. 

To assess system-level robustness, we introduce environmental perturbations and perception artifacts during evaluation, including LiDAR degradation and state-estimation drift. Despite these disturbances, the robot maintains stable traversal across varying terrain geometries. Over 1,000 trials with predefined command sequences, the policy achieves a 95.4% success rate. 

**Zero-shot transfer to long-sequence real-world deployment.** As shown in Fig. 1, we validate the learned policy 

on hardware via zero-shot sim-to-real transfer. The robot autonomously coordinates walking, climb-up, stand-up, liedown, and climb-down skills to traverse a 0.8 m platform in a continuous full-loop sequence. Additional results involving consecutive full-loop traversals are provided in the Appendix. During deployment, the robot exhibits context-aware motor strategies: it switches to climb-up when approaching the platform and selects different lead legs depending on the approach angle, while the descending phase follows a similar adaptive pattern. These behaviors demonstrate the policy’s ability to modulate skill execution based on the surrounding physical context. 

**Robust skill transitions under severe perturbations.** Beyond nominal traversal, the system remains effective under strong external disturbances. As shown in Fig. 4, the robot is heavily kicked from behind while approaching the platform, causing a stumble and unintended contact. Despite being pushed into a near-failure state, it rapidly adapts by adjusting its gait and switching the pivoting leg to stabilize and initiate climbing. This behavior demonstrates that the distilled policy executes skill transitions even from near-failure states, leveraging environmental contact to regain balance. These results indicate that distillation transfers teacher robustness into a unified policy capable of context-dependent modulation. 

## _B. Robustness and Adaptability to Environmental Variations_ 

**Robustness evaluation of individual full-body maneuvers.** To quantify the robustness of each full-body maneuver, 


Fig. 5: Real-world adaptation of the climb-up policy to varying platform heights (0.6–0.8,m) and approach angles ( _θ ∈_ [ _−_ 65<sup>_◦_</sup> _,_ 65<sup>_◦_</sup> ]). The policy exhibits coordinated whole-body behaviors and reliable zero-shot sim-to-real transfer, even in extreme out-of-distribution cases. 

we first evaluate the specialized teacher policies across a diverse set of challenging scenarios in simulation. Each task is assessed over 1,000 independent trials, while maintaining identical terrain distributions, domain randomizations, and pose initializations as those used during training. We adopt Success Rate (SR) as the primary performance metric, and additionally report the maximum contact force (M.C.F.) to assess safety. As summarized in Tab. III, all teacher policies achieve near-perfect success rates in simulation, while maintaining contact forces within safe limits. These results validate the effectiveness of the proposed contact-force regularization across varied terrain geometries and initial conditions. 

**Generalization across real-world configurations.** We further evaluate the robustness and adaptability of the learned policies on hardware across multiple real-world configurations. For the climb-up task, we vary the platform height from 0.6 m to 0.8 m and the approach angle from _−_ 45<sup>_◦_</sup> to 45<sup>_◦_</sup> , as summarized in Tab. III. Across these in-distribution configurations, the policy consistently achieves high success rates, 

including at a platform height of 0.8 m, which corresponds to approximately 114% of the robot’s leg length. 

In addition to these settings, we evaluate the policy under more extreme approach angles of up to _±_ 65<sup>_◦_</sup> , which lie outside the training distribution. As illustrated in Fig. 5, both in-distribution and out-of-distribution cases are shown. In these cases, the robot demonstrates strong adaptability by modifying its whole-body strategy according to the approach geometry, reorienting its torso toward the platform and leveraging fullbody motion to initiate the climb rather than executing a fixed or naive forward reach. 

Beyond climb-up, we also evaluate other full-body maneuvers, including climb-down, stand-up, and lie-down, on hardware. As reported in Tab. III, all evaluated skills achieve a 5/5 success rate, indicating that the robustness and adaptability of the learned behaviors extend beyond a single maneuver. 

**Robustness to Varying Contact Properties.** We evaluate the climbing policy under out-of-distribution contact conditions by placing a soft vinyl–foam mat on the target platform (see Appendix). This introduces unseen compliance and friction properties compared to the rigid training surfaces. The robot successfully climbs onto the soft surface while maintaining stability consistent with behavior observed on rigid platforms. 

**Symmetry augmentation facilitates balanced behaviors.** With symmetry augmentation, the policy converges to a balanced strategy rather than a biased handedness. During climbup, the lead leg is selected dynamically based on the robot’s relative heading to the platform. Such balance is critical in practice, as asymmetric biases restrict the feasible workspace and degrade climbing performance. 

## _C. Skill Acquisition via Progress Rewards_ 

To evaluate the efficacy of progress-based rewards in learning adaptive full-body maneuvers, we benchmark the training of the Climb-up skill against several baseline formulations. In each baseline, the progress-based reward is replaced by alternative task rewards while maintaining identical weights and hyperparameters. 

- 1) Velocity: Employs a standard velocity-tracking objective aimed at matching a torso velocity command[43, 1, 19]. This command is defined in the world frame and oriented forward toward the platform. 

- 2) RND (Random Network Distillation [44]): Utilizes intrinsic rewards generated via RND to incentivize exploration, combined with a sparse task reward upon task completion. [45, 46]. 

- 3) Distance: Penalizes the distance to the target, encouraging the agent to minimize this gap at every timestep. 

- 4) Distance (less Reg.): Follows the same distanceminimization objective as above but with significantly lower regularization penalties. 

- 5) Direction: Rewards any base velocity in the direction towards the goal, while penalizing small velocity to prevent stalling [47, 48]. 


- 6) Increment: Rewards the difference between the previous and the current distance of the system state from the goal state [49]. 

Fig. 7: Comparison against the baseline. (a)(b) Keyframes of policy trained separately with distance-based reward / our proposed reward. The actual contact points at each timestep are visualized with the green sphere. (c) Max contact force over body parts w.r.t. time. (d) Mean joint torque w.r.t time. 

The details of the baseline training configurations are shown in Appendix. We report the learning curves for task rewards, alongside the success rates and maximum contact forces for each formulation. To ensure statistical significance and assess robustness, each policy is evaluated over 1,000 independent trials across randomized environment configurations. These results are summarized in Fig 6. 

aggressive “full-body jumping” behaviors characterized by impulsive contacts and excessive joint torques (Fig. 7). Such solutions are physically infeasible for real-world deployment. In contrast, the proposed ratchet progress-based reward yields sustained whole-body coordination with significantly reduced peak forces. 

Baseline 1 fails to complete climb-up and remains stuck at the platform edge. The velocity-tracking objective overconstrains motion to a fixed forward speed, preventing the discovery of adaptive velocity modulation required to negotiate the edge. Although the reward is partially optimized, task completion remains unsuccessful. 

Baselines 5 and 6 converge to a local optimum at the platform edge, where the agent exhibits a repetitive ”backand-forth” motion—abruptly retreating only to slowly advance again. Because these rewards depend only on instantaneous velocity direction, forward progress can be accumulated without committing to the full maneuver. The agent therefore learns to cyclically reset its position to maximize reward accumulation rather than execute the climb. 

Baseline 2 fails due to the absence of structured guidance for precise multi-stage coordination. Although curiosity-driven exploration encourages diverse behaviors, it lacks a directional gradient toward task completion, often resulting in exploration of physically irrelevant states. Without a dense shaping signal such as ratchet progress reward , the probability of discovering the specific maneuver sequence required to trigger sparse success within the training budget is negligible. 

Collectively, these results expose a fundamental limitation of instantaneous or goal-distance-based objectives: they either induce unsafe velocity bias or admit degenerate local optima. In contrast, the history-dependent ratchet progress reward produces sustained whole-body coordination, modulating contact locations and force distribution to achieve stable climb-up behaviors with substantially reduced peak forces suitable for hardware deployment. 

The distance-minimization objective induces a strong velocity bias, encouraging rapid target approach to maximize cumulative returns. This conflicts with contact-force regularization, preventing Baseline 3 from achieving a balance between task success and physical safety. Reducing regularization in Baseline 4 enables goal reaching but produces 

REFERENCES 

## V. CONCLUSION 

We presented APEX, a learning system for adaptive high-platform traversal on humanoid robots, targeting extreme ledges where jumping becomes unsafe and actuatorlimited. Our approach trains six terrain-conditioned skills (four contact-rich maneuvers and two cyclic locomotion skills) and distills them into a single perceptive policy that autonomously selects behaviors and transitions from LiDAR-based elevation maps. Central to our method is a generalized ratchet progress reward for goal-reaching maneuvers. By tracking best-so-far task progress and penalizing non-improving steps, it provides dense, velocity-free supervision that enables efficient learning under strong safety regularization and avoids retracing failure modes. Experiments on a 29-DoF Unitree G1 humanoid demonstrate zero-shot sim-to-real traversal of 0 _._ 8 m platforms ( _≈_ 114% of leg length), with robust adaptation to platform height and initial pose and smooth multi-skill transitions. 

## ACKNOWLEDGMENT 

This work was partially supported by the National Science Foundation under Grant CAREER CNS-2047454. The authors would also like to thank Yuxiang Yang from Google DeepMind for valuable advice and discussions, and Boda Huo and Mingyang Yu from the CMU SafeAI Lab for their assistance with the experiments. 

- [1] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9997–10 003. 

- [2] Y. Xue, W. Dong, M. Liu, W. Zhang, and J. Pang, “A unified and general humanoid whole-body controller for fine-grained locomotion,” _arXiv e-prints_ , pp. arXiv–2502, 2025. 

- [3] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” _arXiv preprint arXiv:2406.10759_ , 2024. 

- [4] Q. Zhang, P. Cui, D. Yan, J. Sun, Y. Duan, G. Han, W. Zhao, W. Zhang, Y. Guo, A. Zhang _et al._ , “Wholebody humanoid robot locomotion with human reference,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 225–11 231. 

- [5] Q. Ben, B. Xu, K. Li, F. Jia, W. Zhang, J. Wang, J. Wang, D. Lin, and J. Pang, “Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains,” _arXiv preprint arXiv:2511.14625_ , 2025. 

- [6] P. Chen, Y. Wang, C. Luo, W. Cai, and M. Zhao, “Hifar: Multi-stage curriculum learning for high-dynamics humanoid fall recovery,” _arXiv preprint arXiv:2502.20061_ , 2025. 

- [7] X. He, R. Dong, Z. Chen, and S. Gupta, “Learning getting-up policies for real-world humanoid robots,” _arXiv preprint arXiv:2502.12152_ , 2025. 

- [8] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning humanoid standing-up control across diverse postures,” _arXiv preprint arXiv:2502.08378_ , 2025. 

- [9] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” _arXiv preprint arXiv:2509.26633_ , 2025. 

- [10] M. Xu, Y. Shi, K. Yin, and X. B. Peng, “Parc: Physicsbased augmentation with reinforcement learning for character controllers,” in _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , 2025, pp. 1–11. 

- [11] J. Tan, T. Zhang, E. Coumans, A. Iscen, Y. Bai, D. Hafner, S. Bohez, and V. Vanhoucke, “Sim-to-real: Learning agile locomotion for quadruped robots,” _arXiv preprint arXiv:1804.10332_ , 2018. 

- [12] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter, “Learning agile and dynamic motor skills for legged robots,” _Science Robotics_ , vol. 4, no. 26, p. eaau5872, 2019. 

- [13] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

- [14] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on robot learning_ . PMLR, 2022, pp. 91–100. 

- [15] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, p. eadi9579, 2024. 

- [16] X. Gu, Y.-J. Wang, X. Zhu, C. Shi, Y. Guo, Y. Liu, and J. Chen, “Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning,” _arXiv preprint arXiv:2408.14472_ , 2024. 

- [17] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv preprint arXiv:2502.10363_ , 2025. 

- [18] J. Ren, T. Huang, H. Wang, Z. Wang, Q. Ben, J. Long, Y. Yang, J. Pang, and P. Luo, “Vb-com: Learning visionblind composite humanoid locomotion against deficient perception,” _arXiv preprint arXiv:2502.14814_ , 2025. 

- [19] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter, “Attention-based map encoding for learning generalized legged locomotion,” _Science Robotics_ , vol. 10, no. 105, p. eadv3604, 2025. 

- [20] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [21] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [22] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

- [23] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang _et al._ , “Hover: Versatile neural whole-body controller for humanoid robots,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9989–9996. 

- [24] Y. Ze, Z. Chen, J. P. Ara´ujo, Z.-a. Cao, X. B. Peng, J. Wu, and C. K. Liu, “Twist: Teleoperated whole-body imitation system,” _arXiv preprint arXiv:2505.02833_ , 2025. 

- [25] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang, “Gmt: General motion tracking for humanoid whole-body control,” _arXiv preprint arXiv:2506.14770_ , 2025. 

- [26] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [27] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [28] G. Tevet, S. Raab, B. Gordon, Y. Shafir, D. Cohen-Or, and A. H. Bermano, “Human motion diffusion model,” 

   - _arXiv preprint arXiv:2209.14916_ , 2022. 

- [29] Z. Jiang, Y. Xie, J. Li, Y. Yuan, Y. Zhu, and Y. Zhu, “Harmon: Whole-body motion generation of humanoid robots from language descriptions,” _arXiv preprint arXiv:2410.12773_ , 2024. 

- [30] J. Li, J. Cao, H. Zhang, D. Rempe, J. Kautz, U. Iqbal, and Y. Yuan, “Genmo: A generalist model for human motion,” _arXiv preprint arXiv:2505.01425_ , 2025. 

- [31] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “Rma: Rapid motor adaptation for legged robots,” _arXiv preprint arXiv:2107.04034_ , 2021. 

- [32] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning robust perceptive locomotion for quadrupedal robots in the wild,” _Science robotics_ , vol. 7, no. 62, p. eabk2822, 2022. 

- [33] Z. Fu, X. Cheng, and D. Pathak, “Deep whole-body control: learning a unified policy for manipulation and locomotion,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 138–149. 

- [34] X. Cheng, K. Shi, A. Agarwal, and D. Pathak, “Extreme parkour with legged robots,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 11 443–11 450. 

- [35] Y. Yang, G. Shi, C. Lin, X. Meng, R. Scalise, M. G. Castro, W. Yu, T. Zhang, D. Zhao, J. Tan _et al._ , “Agile continuous jumping in discontinuous terrains,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 10 245–10 252. 

- [36] C. Lin, Y. R. Song, B. Huo, M. Yu, Y. Wang, S. Liu, Y. Yang, W. Yu, T. Zhang, J. Tan _et al._ , “Locotouch: Learning dexterous quadrupedal transport with tactile sensing,” _arXiv preprint arXiv:2505.23175_ , 2025. 

- [37] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao, “Robot parkour learning,” _arXiv preprint arXiv:2309.05665_ , 2023. 

- [38] N. Rudin, J. He, J. Aurand, and M. Hutter, “Parkour in the wild: Learning a general and extensible agile locomotion policy using multi-expert distillation and rl fine-tuning,” _arXiv preprint arXiv:2505.11164_ , 2025. 

- [39] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 

- [40] M. Mittal, N. Rudin, V. Klemm, A. Allshire, and M. Hutter, “Symmetry considerations for learning task symmetric robot policies,” 2024. [Online]. Available: https://arxiv.org/abs/2403.04359 

- [41] G. Bradski and A. Kaehler, _Learning OpenCV: Computer vision with the OpenCV library_ . ” O’Reilly Media, Inc.”, 2008. 

- [42] F. Torabi, G. Warnell, and P. Stone, “Behavioral cloning from observation,” _arXiv preprint arXiv:1805.01954_ , 2018. 

- [43] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour 

learning,” 2024. [Online]. Available: https://arxiv.org/ abs/2406.10759 

- [44] Y. Burda, H. Edwards, A. Storkey, and O. Klimov, “Exploration by random network distillation,” 2018. [Online]. Available: https://arxiv.org/abs/1810.12894 

- [45] C. Schwarke, V. Klemm, M. v. d. Boon, M. Bjelonic, and M. Hutter, “Curiosity-driven learning of joint locomotion and manipulation tasks,” in _Proceedings of The 7th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, J. Tan, M. Toussaint, and K. Darvish, Eds., vol. 229. PMLR, 06–09 Nov 2023, pp. 2594–2610. [Online]. Available: https://proceedings.mlr.press/v229/schwarke23a.html 

- [46] C. Zhang, W. Xiao, T. He, and G. Shi, “Wococo: Learning whole-body humanoid control with sequential contacts,” 2024. [Online]. Available: https://arxiv.org/ abs/2406.06005 

- [47] D. Hoeller, N. Rudin, D. Sako, and M. Hutter, “Anymal parkour: Learning agile navigation for quadrupedal robots,” _Science Robotics_ , vol. 9, no. 88, p. eadi7566, 2024. 

- [48] X. Cheng, K. Shi, A. Agarwal, and D. Pathak, “Extreme parkour with legged robots,” 2023. [Online]. Available: https://arxiv.org/abs/2309.14341 

- [49] OpenAI, I. Akkaya, M. Andrychowicz, M. Chociej, M. Litwin, B. McGrew, A. Petron, A. Paino, M. Plappert, G. Powell, R. Ribas, J. Schneider, N. Tezak, J. Tworek, P. Welinder, L. Weng, Q. Yuan, W. Zaremba, and L. Zhang, “Solving rubik’s cube with a robot hand,” 2019. [Online]. Available: https://arxiv.org/abs/1910. 07113 

## VI. APPENDIX 

## _A. Effectiveness of Ratchet Progress Reward_ 

We deploy our policy on hardware and record the torso horizontal displacement ( _x_ -direction) using a motion capture system (MoCap). We do not deploy the baseline policy due to the high risk associated with its excessive contact forces and impulsive movements. As illustrated in Fig. 8, the measured trajectory reveals two characteristic properties of functional climb-up behavior: monotone task progress with contactinduced holds. After the initial approach and hand placement (0–0 _._ 7 _,_ s), the trajectory exhibits a pronounced plateau centered around _t ≈_ 1 _._ 0 _,_ s. This stagnation phase is functionally necessary: the torso remains near the platform edge while the robot lifts and securely places the lead leg. Once this contact is established, the torso resumes forward progression ( _t >_ 1 _._ 2 _,_ s), driven by coordinated forces from the hands and the newly established foothold. The emergence of this deliberate pause highlights the event-driven nature of contactrich maneuvers and indicates that our reward formulation learns to prioritize kinematic feasibility and stability, rather than simply minimizing distance to the goal. 


Fig. 8: Trajectory of the robot’s torso relative to the platform edge. The top plot shows the horizontal displacement _x_ ( _t_ ) over time, while the bottom sequence illustrates the corresponding climbing up motion at key timestamps. 

## _B. Extended Experiments on Context-Aware Traversal_ 

As shown in Fig. 9, we additionally demonstrate two new routes for high-platform traversal in the real world to further validate the context-aware capability of our proposed system. In both routes, the robot autonomously transitions between full-body maneuvers by perceiving the environmental geometry. For instance, when the robot is commanded to walk towards the platform, it perceives the obstacle and automatically triggers the climb-up skill to ascend. Similarly, when commanded to move towards the edge, the system perceives the drop and autonomously initiates the climb-down sequence to descend and reach a stable standing posture on the ground. 

Route (a) includes the sequential execution of all six fullbody maneuvers in the following order: walk (on the ground), climb-up, crawl, stand-up, walk (on the platform), lie-down, 

crawl, climb-down, and walk (on the ground). Our system achieves two full cycles of traversal consecutively, demonstrating the reliability of this context-aware gait switching. 

Route (b) consists of a complete side-to-side traversal of the high platform with the following sequence: walk, climb-up, crawl, climb-down, and walk. Besides the successful execution of full-body skills, it also highlights the robustness of our perception pipeline in accurately identifying environmental contexts during dynamic maneuvers. 


Fig. 9: Experimental validation of the unified policy. The distilled system demonstrates real-world robustness by successfully completing diverse routes requiring complex fullbody coordination. 

## _C. Extended Experiments on Robustness_ 

The adaptability and robustness of our policy is showcased in three extreme cases: (i) large external perturbation; (ii) significant perception artifacts; (iii) soft high platform; 

_1) Robustness to Perception Artifacts:_ Fig. 10 illustrates a typical elevation map observed by the robot and the robot’s corresponding climbing maneuver. The map contains a significant batch of “ghost points”, which form a fake obstacle behind the robot of a scale comparable to the target platform. Despite these substantial perceptual artifacts, the robot successfully climbs up the platform with nominal movement, demonstrating the policy’s perceptual robustness. This resilience is obtained from the noises injected during the training process, especially the outlier clusters, which showcases the necessity of rigorous perception and noise modeling for reliable real-world deployment. 

To isolate the impact of the perception pipeline, we conduct an ablation study by selectively removing individual mapping pipeline components. As reported in Tab. IV, the full system achieves nearly 100% success, whereas disabling real-time filtering and inpainting reduces the success rate to 60%. Moreover, a policy trained without simulated sensor drift and outlier corruption fails entirely on hardware. We observe that, 


Fig. 10: A typical artifacted elevation map with significant outlier cluster. The red circle denotes the outliers while the blue circle denotes the target platform. The map is aligned with the platform edge for a clearer view. 

TABLE IV: Comparative success rates of the climb-up skill on hardware. **SR** : success rate; **S/T** : successes/trials; **M.C.F.** : maximum contact force; _H_ **(m)** : platform height; _A_ **(**<sup>_◦_</sup> **)** : approach angle relative to the platform-edge normal. 

|**Task**|_H_ **(m)**|_A_ **(**<sup>_◦_</sup>**)**|**S/T**|**SR (%)**|
|---|---|---|---|---|
|Climb-up (full system)|0.8|[_−_45_,_45]|15/15|100|
|Climb-up (w/o drift & outlier)<br>(w/ post-processing)|0.8|[_−_45_,_45]|0/5|0.0|
|Climb-up (w/ drift & outlier)<br>(w/o post-processing)|0.8|[_−_45_,_45]|3/5|60.0|


in some scenarios, large regions of mapping artifacts remain in the elevation map (Fig. 11), often caused by outdated spatial measurements near the robot that are not updated in time. Despite these severe artifacts, the robust policy still executes the intended maneuver correctly and successfully completes the task. These results demonstrate that modeling sensor artifacts during training is essential for tolerating mapping uncertainty and mitigating out-of-distribution (OOD) failures by expanding the effective training distribution. In addition, real-time map reconstruction is critical to prevent the policy from encountering severely corrupted inputs, such as outlier clusters or NaN holes, which can otherwise lead to catastrophic failures. 

_2) Robustness to Varying Contact Property:_ We further evaluate the policy’s climbing capabilities by placing a soft mat, made of vinyl and foam, on top of the target platform (Fig. 12). This setup challenges the robot to climb up an unseen material with significantly different compliance and friction properties compared to the rigid training environments. The robot successfully climbs the soft mat in the first trial, maintaining the same levels of stability and efficiency observed when climbing rigid platforms. 

The stability of the climbing skill originates from the policy’s quasi-static and contact-rich moving patterns. Unlike dynamic jumping or lunging behaviors, our policy does not rely on impulsive supporting forces provided by rigid surfaces, nor does it depend on a limited number of contact points to maintain equilibrium. Instead, the policy learns to distribute loads across multiple contact points, ensuring balance through 


Fig. 11: The red dashed region indicates severe mapping artifacts caused by outdated spatial measurements, while the blue dashed region denotes the target platform. 


Fig. 12: The robot successfully and stably climbs up the platform with a black soft mat on top. 

consistent interaction with the platform. These results further demonstrate the adaptability of our policy to varying contact properties and highlight the advantages of our proposed reward formulation in learning safe, robust humanoid behaviors. 

## _D. Effectiveness of Multi-Teacher Distillation_ 

To evaluate our distillation pipeline, we compare the teacher and the distilled student across the four contact-rich fullbody maneuvers in simulation. We report success rate and maximum contact force (Tab. V), evaluated over 1,000 parallel environments with the same randomization ranges used during training. As expected, the specialized teacher policies achieve the strongest performance on their respective tasks. Nevertheless, the distilled student attains comparable success rates across all maneuvers, while maintaining statistically similar maximum contact forces within a safe range. Overall, these results indicate that the unified student policy faithfully captures the behaviors of diverse experts and retains nearteacher-level performance in simulation. 

TABLE V: Comparison of Teacher and Student Performance. **SR:** Success Rate; **M.C.F.:** Max Contact Force. 

||**Teacher **|**Policy**|**Student **|**Policy**|
|---|---|---|---|---|
|**Skill**|**SR (%)**|**M.C.F. (N)**|**SR (%)**|**M.C.F. (N)**|
|Climb-up|98.8|638_±_479|98.6|657_±_324|
|Climb-down|99.9|754_±_241|99.0|762_±_539|
|Stand-up|99.5|632_±_222|99.1|680_±_237|
|Lie-down|100.0|576_±_125|100.0|637_±_124|


## _E. Details for Baseline Training_ 

We summarize the task reward formulations used by baseline methods in Tab. VI. 

TABLE VI: Formulations of the baseline task rewards. 

|**Baseline**|**Reward**|**Formulation**<br>**Weight**|
|---|---|---|
|Velocity|Lin. Vel. Tracking<br>Ang. Vel. Tracking|exp<br>�<br>_−∥v_<sup>(</sup><sup>_xy_)</sup><br>_base,t _<sup>_−v_(</sup><sup>_xy_)</sup><br>_cmd_<sup>_∥_2</sup><sup>_/_0</sup><sup>_._52�</sup><br>4<br>exp<br>�<br>_−_(_ω_<sup>(</sup><sup>_z_)</sup><br>_base,t _<sup>_−ω_(</sup><sup>_z_)</sup><br>_cmd_<sup>)2</sup><sup>_/_0</sup><sup>_._52�</sup><br>4|
|RND|Sparse Success|**1**_{p_(_z_)<br>_LB,t_<sup>_>hedge∧p_(</sup><sup>_x_)</sup><br>_CoM,t_<sup>_>xedge}_</sup><br>8|
|Distance|L2 Tracking|(1 +_∥p_<sup>(</sup><sup>_xy_)</sup><br>_base,t _<sup>_−p_(</sup><sup>_xy_)</sup><br>_goal_<sup>_∥_2)</sup><sup>_−_1</sup><br>8|
|Direction|Cosine Sim.|cos<br>�<br>_θ_(_vbase,t, pgoal −pbase,t_)<br>�<br>8|
|Increment|Height Incr.<br>Forward Incr.|**1**_{p_(_z_)<br>_LB,t_<sup>_>p_(</sup><sup>_z_)</sup><br>_LB,t−_1<sup>_}·_</sup><sup>**1**</sup><sup>_{xt /∈xg}_</sup><br>4<br>**1**_{p_(_x_)<br>_CoM,t_<sup>_>p_(</sup><sup>_x_)</sup><br>_CoM,t−_1<sup>_}·_</sup><sup>**1**</sup><sup>_{xt /∈xg}_</sup><br>4|


For the Velocity baseline, the commanded linear velocity satisfies _v_ cmd _∈_ [0 _._ 5 _,_ 1 _._ 0] m/s in the world frame, and the goal position _p_ goal is defined 0.5 m inside the platform along the robot’s initial heading. Distance (less Reg.) shares the same task reward as Distance but uses contact-force regularization weights reduced by a factor of 10. 

TABLE VIII: Perturbations and Domain Randomization Ranges. 

|**Perturbed Terms**|**Perturbed Range**|
|---|---|
|Torso CoM Position (m)<br>Torso Mass (kg)|_x, y_ : [_−_0_._05_,_0_._05]<br>_z_ : [_−_0_._02_,_0_._02]<br>_m_: [_−_1_._0_,_1_._0]|
|Static Friction<br>Dynamic Friction<br>Restitution|_µs_ : [0_._3_,_1_._6]<br>_µd_ : [0_._3_,_1_._2]<br>_e_: [0_._0_,_0_._5]|
|Joint Default Position (rad)<br>Joint Initial Position (rad)|_q_ : [_−_0_._01_,_0_._01]<br>˙_q_ : [_−_0_._15_,_0_._15]|
|External Push (m/s) (rad/s)|_vx, vy_ : [_−_0_._5_,_0_._5]<br>_vz_ : [_−_0_._2_,_0_._2]<br>_ωr, ωp_ : [_−_0_._5_,_0_._5]<br>_ωy_ : [_−_0_._78_,_0_._78]<br>Interval (s): [1_,_3]|
|Elevation Map Noise (m)|Gaussian: [_−_0_._15_,_0_._15]<br>Drift _dx, dy_ : [_−_0_._05_,_0_._05]<br>Drift _dz_ : [_−_0_._1_,_0_._05]<br>Outliers: 20%|


TABLE IX: Hyperparameter of Teacher Policy 

## _F. Details for Teacher Policy Training_ 

_1) Environment Configuration:_ We train the teacher policy in IsaacLab using 4096 parallel environments for each single skill. While the six skills share basic observations, climbing skills are additionally based on height scan dots, and walking skill additionally utilize a phase signal to lead the gait pattern. The full list of observations is in Tab. VII. We also introduce perturbations and domain randomization, including previously discussed perception artifacts, to improve robustness (Tab. VIII). 

TABLE VII: Observations and Noise for Teacher Training. 

|**Skill**|**Observation**|**Noise Range**|
|---|---|---|
|All Skills|Root angular velocity (rad/s)<br>Projected gravity<br>Joint position (rad)<br>Joint velocity (rad/s)<br>Last action|[_−_0_._2_,_0_._2]<br>[_−_0_._05_,_0_._05]<br>[_−_0_._1_,_0_._1]<br>[_−_1_._5_,_1_._5]<br>—|
|Climb-up/down|Elevation Map (m)|refer to Tab. VIII|
|Walk / Crawl|Phase signal<br>Velocity Commands (m/s)|—<br>—|


The six skills are categorized into two groups: (i) Nonperiodic full-body maneuvers: climb-up, climb-down, standup, lie-down; (ii) Periodic locomotion skills: walk, crawl; Each group widely shares common rewards with several task-related reward terms. The full list of rewards is defined in Tab. XII. 

_2) Algorithm Design and Network Architecture:_ We use Proximal Policy Optimization (PPO) to optimize the actor and the critic during the teacher policy training stage. The network architecture and hyperparameter are listed in Tab. IX. _G. Details for Multi-Teacher Distillation_ 

_1) Algorithm Design and Network Architecture:_ The network architecture and hyperparameter are in the Tab. XI. 

|**Environment and **|**Architecture**|
|---|---|
|Num. of Environments|4096|
|Episode Length|350 / 1000|
|Network Type|MLP|
|Activation|ELU|
|Actor Network|[512, 256, 128]|
|Critic Network|[512, 256, 128]|
|**PPO Optimization **|**Parameters**|
|Num. Epochs|5|
|Num. Mini Batches|4|
|Num. Steps per Batch|24|
|Num. Steps per Env|24|
|Normalization|Observation|
|Learning Rate _lr_|1.0e-3|
|Clip Parameter|0.2|
|Entropy Coefficient|0.01|
|Gamma _γ_|0.99|
|Lambda _λ_|0.95|
|Desired KL value|0.01|
|Max Gradient Norm|1.0|


We conduct all experiments with a 29-DoF Unitree G1 humanoid robot in both simulation and on hardware. Simulation environments are implemented in NVIDIA Isaac Sim. For realworld deployment, terrain perception is handled by an Intel Core i7 CPU, which processes data from a Livox MID-360 LiDAR to generate real-time elevation maps. 

## _H. Demonstration of Individual Skills_ 

Beyond climb-up, Fig. 13 presents the motion sequences of the remaining three full-body maneuvers. 


TABLE X: Environment Distribution for Distillation. 

|**Skills**<br>**E**|**nv. Prop.**|**Terrains**|**Vel. Cmd. (**_m/s_**)**|
|---|---|---|---|
|Walk|0.17|Rough + Plane|Omni.|
|Crawl|0.08|Plane|Omni.|
|Stand-up + Walk|0.07|Plane|Zero + Omni.|
|Walk + Climb-up|0.16|Platform|Forward|
|Climb-up + Crawl|0.12|Platform|Forward + Lateral|
|Crawl + Climb-down|0.20|Platform|Lateral|
|Climb-down + Walk|0.15|Platform<br>|Lateral + Backward|
|Lie-down + Crawl|0.05|Plane|Zero + Omni.|


TABLE XI: Hyperparameter for Distillation 

|**Environment and Architecture**|
|---|
|Num. of Environments<br>1000|
|Episode Length<br>400|
|Activation<br>ELU|
|Network Type<br>MLP|
|Student Network<br>[2048, 1024, 512, 256]|
|**Optimization Parameters**|
|BC Iterations<br>4|
|DAgger Iterations<br>16|
|Num. Epochs<br>1500|
|Num. Steps per Batch<br>20000|
|Num. Steps per Env<br>400|
|Normalization<br>Observation|
|Learning Rate _lr_<br>3.0e-4|
|Action Noise Std<br>0.1|
|Gradient Length<br>1.0|
|Max Gradient Norm<br>1.0|


Fig. 13: Three full-body maneuvers deployed on hardware: climb-down, stand-up, and lie-down. 

TABLE XII: Reward Formulations for Teacher Policy Training. 

|||**Non-periodic full-body maneuvers**||
|---|---|---|---|
|**Skill**|**Reward**|**Formulation**|**Weight**|
|All Skills|Survival|**1**_{¬term}_|15|
||Termination|**1**_{term¬timeout}_|-800|
||Force Penalty<br>|_,_<br>exp(0_._01_·_max(0_, ∥F∥−_500))_−_1<br>|-1<br>|
||Head Safety<br>|exp(0_._1_· ∥Fhead∥_)_−_1<br>|-1<br>|
||Joint Limits|_∥_max(0_, |qt| −qsoft_)_∥_1|-10|
||Hip Deviation|**1**_{|qhip,yaw|>_1_._5_∨|qhip,roll|>_1_._4_}_|-1|
||Waist Deviation|**1**_{|qwaist_<br>_yaw_<sup>_|>_1</sup><sup>_._4</sup><sup>_}_</sup>|-6|
||Joint Velocity|_∥_˙_qt∥_<sup>2</sup><br>|-0.001|
||Joint Accel.|_∥_¨_qt∥_<sup>2</sup><br>|-2e-8|
||Action Rate|_∥at −at−_1_∥_<sup>2</sup>|-0.2|
||Torque|_∥τt∥_<sup>2</sup>|1.5e-5|
||Power|�_|τt ·_ ˙_qt|_<br>|-1e-5|
||Body Slip|�<br>_i∈C _<sup>_∥v_(</sup><sup>_xy_)</sup><br>_i,t _<sup>_∥_</sup><br>|-0.1|
||Base Ang. Vel.|_∥ω_<sup>(</sup><sup>_xy_)</sup><br>_base,t_<sup>_∥_2</sup>|-0.005|
||Base Accel.|_∥_¨_pbase,t∥_<sup>2 </sup>+ 0_._02_∥_˙_ωbase,t∥_<sup>2</sup>|-0.0001|
||Body Accel.|�<br>_i _<sup>_∥_¨</sup><sup>_pi,t∥_</sup>|-0.0002|
|Climb-up|Upward Progress|**1**_{p_(_z_)<br><sup>_≥p_(</sup><sup>_z_)</sup><br><sup>_} ·_</sup><sup>**1**</sup><sup>_{xt /∈xg}_</sup>|-4|
||Edge Approach|_LB,max_<br>_LB,t_<br>**1**_{p_(_x_)<br>_CM_<sup>_≥p_(</sup><sup>_x_)</sup><br>_CMt_<sup>_} ·_</sup><sup>**1**</sup><sup>_{xt /∈xg}_</sup>|-4|
||Terminal Posture|_o,max_<br>_o,_<br>**1**_{t>H−_1_s} ·_**1**_{xt∈xg} ·_exp(_−_0_._1_· ∥qt −qprone∥_)|7|
|Climb-down|Descent Progress|**1**_{p_(_z_)<br>_LBi_<sup>_≤p_(</sup><sup>_z_)</sup><br>_LBt_<sup>_} ·_</sup><sup>**1**</sup><sup>_{xt /∈xg}_</sup>|-4|
||EdCl|_,mn_<br>_,_<br>**1**<br><br><sup>_·_</sup><sup>**1**</sup>|4|
||ge earance|_{p_(_x_)<br>_CMi_<sup>_≤p_(</sup><sup>_x_)</sup><br>_CMt_<sup>_} _</sup> <sup>_{xt /∈xg}_</sup>|-|
||Terminal Posture|_o,mn_<br>_o,_<br>**1**_{t>H−_1_s} ·_**1**_{xt∈xg} ·_exp(_−_0_._1_· ∥qt −qstanding∥_)|7|
|Stand-up|Height Progress|**1**_{p_(_z_)<br>_headmax_<sup>_≥p_(</sup><sup>_z_)</sup><br>_headt_<sup>_} ·_</sup><sup>**1**</sup><sup>_{xt /∈xg}_</sup>|-4|
||BalanceProgress|_,_<br>_,_<br>**1**_·_**1**|-4|
||<br>Terminal Posture|_{dbal,min≤dbal,t} _ _{xt /∈xg}_<br>**1**_{t>H−_1_s} ·_**1**_{xt∈xg} ·_exp(_−_0_._1_· ∥qt −qstanding∥_)|7|
|Lie-down|Descent Progress|**1**_{p_(_z_)<br><sup>_≤p_(</sup><sup>_z_)</sup><br><sup>_} ·_</sup><sup>**1**</sup><sup>_{xt /∈xg}_</sup>|-4|
||HdPlt|_CoM,min_<br>_CoM,t_<br>**1**<br><br> <sup>**1**</sup>|4|
||ea acemen|_{p_(_z_)<br><sup>_≤p_(</sup><sup>_z_)</sup><br><sup>_} ·_</sup> <sup>_{xt /∈xg}_</sup>|-|
||Terminal Posture|_head,min_<br>_head,t_<br>**1**_{t>H−_1_s} ·_**1**_{xt∈xg} ·_exp(_−_0_._1_·∥qt −qprone∥_)|7|
|||**Periodic locomotion skills**||
|**Skill**|**Reward**|**Formulation**|**Weight**|
|All Skills|Track lin. Velocity|exp(_−∥v_<sup>(</sup><sup>_x,y_)</sup> _−vcmd∥_<sup>2</sup>_/_0_._5<sup>2</sup>)|1.3|
||Track Ang. Velocity|exp(_−∥ω_<sup>(</sup><sup>_z_)</sup> _−ωcmd∥_<sup>2</sup>_/_1_._0<sup>2</sup>)<br>|1.3|
||Vertical Lin. Velocity|_∥v_<sup>(</sup><sup>_z_)</sup>_∥_<sup>2</sup>|-2|
||Horizontal Ang. Velocity|_∥ω_<sup>(</sup><sup>_x,y_)</sup>_∥_<sup>2</sup>|-0.15 / -0.05|
||Height Penalty|(_p_<sup>(</sup><sup>_z_)</sup><br>_root _<sup>_−hdes_)2</sup>|-10|
||Joint Acc. Penalty|�<br>_j∈A_ <sup>¨</sup><sup>_q_2</sup><br>_j,t_<br>|_−_2_._5_e −_7|
||Joint Vel. Penalty|�<br>_A_ <sup>˙</sup><sup>_q_2</sup><br>_jt_|_−_1_._5_e −_3|
||Action Rate|_j∈_ <br>_,_<br>_∥at −at−_1_∥_<sup>2</sup>|-0.1|
||Joint Limits<br>|�(max(0_, qmin −q_) + max(0_, q −qmax_))<br>|-5<br>|
||Survival|**1**_{¬terminated}_|0.2 / 10|
||Torque Penalty|_∥τt∥_<sup>2</sup>|_−_1_._0_e −_5|
||Undesired Contact|�<br>_b∈B_ <sup>**1**</sup><sup>_{∥F_</sup>_contact,b_<sup>_∥>_0</sup><sup>_._1</sup><sup>_}_</sup>|-1|
|Walk|Base Orientation|_∥g_<sup>(</sup><sup>_x,y_)</sup><br>_b_<br>_∥_<sup>2</sup>|-1.0|
||HiDiti|<sup>2</sup>|10|
||p evaon|_∥qt −qdefault∥_<br><br>|-.|
||Contact Slip|�<br><br> <sup>**1**</sup><sup>_{∥F∥>_1</sup><sup>_} · ∥vb∥_2</sup>|-0.2|
||Feet Swing Height|_b∈_ankle<br>roll _c,b_ <br>�<br>_f∈_ankle<br>roll <sup>**1**</sup><sup>_swing ·_ (0</sup><sup>_._08</sup><sup>_−hf_)2</sup>|-20|
||Gait Phase|<br>�<br>_i_ <sup>**1**</sup><sup>_{C_</sup>_i_<sup>=</sup><sup>_C_</sup>_target_<sup>(</sup><sup>_ϕ_</sup>_t_<sup>)</sup><sup>_}_</sup>|0.18|
||Feet Air Time|�<br>_f∈_ankle<br>roll<sup>(</sup><sup>_τair,f −_0</sup><sup>_._5)</sup><sup>_·_</sup><sup>**1**</sup><sup>_contact ·_</sup><sup>**1**</sup><sup>_move_</sup>|0.1|
|Crawl|Termination|**1**_terminated_<br>|-100|
||Lying Deviation<br>Contact Force Penalty|_∥qt −qlying∥_<sup>2</sup><br>�<br>_b_ <sup>max(0</sup><sup>_, ∥Fb∥−_500)</sup>|-1.0<br>-0.01|


