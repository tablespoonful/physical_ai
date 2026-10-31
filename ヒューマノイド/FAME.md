---
title: "FAME: Force-Adaptive RL for Expanding the Manipulation Envelope of a Full-Scale Humanoid"
date: "2026-03-09"
authors: "Niraj Pudasaini; Yutong Zhang; Jensen Lavering; Max Conway; Alessandro Roncone; Nikolaus Correll"
url: https://arxiv.org/abs/2603.08961
pdf: https://arxiv.org/pdf/2603.08961
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.08961)** / [論文ページ](https://arxiv.org/abs/2603.08961)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**FAME:** 

# **Force-Adaptive RL for Expanding the Manipulation Envelope of a Full-Scale Humanoid** 

Niraj Pudasaini<sup>1</sup> , Yutong Zhang<sup>2</sup> , Jensen Lavering<sup>2</sup> , Max Conway<sup>2</sup> , Alessandro Roncone<sup>2</sup> , and Nikolaus Correll<sup>1</sup> 


Fig. 1: FAME overview. **Left:** a standing policy conditioned on an upper-body context encoder mapping arm and torso configuration _∈_ R<sup>15</sup> and hand forces [ _F_<sup>_L_</sup> _, F_<sup>_R_</sup> ] _∈_ R<sup>6</sup> to a latent context _zt_ . At deployment the forces are reconstructed from joint torques. The H1-2 stands under a 30 N load. **Right:** the policy in the GOLEM simulation [1] on bowl pick-and-place (top) and refrigerator door opening (bottom), where the forces arise from the task. Arrows mark the force on the hand. 

**_Abstract_ — Maintaining balance under external hand forces is critical for humanoid bimanual manipulation, where interaction forces propagate through the kinematic chain and constrain the feasible manipulation envelope. We propose FAME, a forceadaptive reinforcement learning framework that conditions a standing policy on a learned latent context encoding upperbody joint configuration and bimanual interaction forces** **_jointly_ , since the base moment a load induces depends on the arm configuration through which it acts. Training applies isotropically sampled 3D forces at each hand under an upper-body pose curriculum, exposing the policy to manipulation-induced perturbations across continuously varying arm configurations. At deployment the interaction force is not measured but reconstructed online from joint torques and states through rigid-body inverse dynamics, requiring no wrist force/torque sensing. We evaluate over** 100 **upper-body configurations under swept hand forces, scoring each trial by a task-level criterion that requires the robot both to remain upright and to hold its hands near where the task placed them; all such results run with the estimated force in the loop. At a** 150 **mm tolerance FAME reaches** 38 _._ 9% **task success, against** 16 _._ 6% **for a policy given the same force without encoding,** 4 _._ 3% **for a poseconditioned curriculum policy, and** 24 _._ 7% **for an adversarially trained locomotion policy, which stays upright but recovers by stepping and so relocates the hands. We further demonstrate transfer to task-generated interaction forces in a MuJoCo kitchen environment, and to asymmetric and bimanual loading on a full-scale Unitree H1-2. Code and videos are available on the project website.** 

> 1Department of Aerospace and Mechanical Engineering, University of Notre Dame, Notre Dame, IN 46556, USA. 

> 2Department of Computer Science, University of Colorado Boulder, Boulder, CO 80309, USA. Corresponding author: Niraj Pudasaini, npudasai@nd.edu. 

## I. INTRODUCTION 

Humanoid robots are designed to operate in humancentered environments, where interaction with tools, objects, and existing infrastructure requires coordinated upper-body bimanual manipulation with stable lower-body control. During bimanual manipulation, external forces applied at the hands propagate through the kinematic chain and directly disturb the lower-body balance. Unless actively mitigated, these interaction forces constrain the feasible manipulation envelope of the robot and couple upper-body tasks with stance stability. We define the manipulation envelope as the region of admissible external hand forces and arm configurations under which the robot can maintain stable standing. Enabling humanoids to maintain stable standing under varying and uncertain hand loads remains a fundamental challenge. 

Traditional model-based methods [2], [3] (LIPM [4], SLIP [5], MPC, trajectory optimization) for humanoid balance struggle under highly dynamic conditions with significant external disturbances. Deep reinforcement learning (DRL) has emerged as a promising alternative [6], [7], [8], yet training policies that maintain stability under varying and uncertain hand forces during manipulation remains challenging. The core difficulty lies in the high-dimensional, coupled nature of the disturbance: interaction forces at the hands depend on both the magnitude and direction of applied loads as well as the geometric configuration of the arms, creating a state space that is difficult to explore during training. 

Latent context adaptation supplies the right machinery, though not for the usual reason. Rapid Motor Adaptation (RMA) [9], [10] compresses environment parameters such 


Fig. 2: Overview of the proposed standing framework. During training (top), an upper-body dynamics encoder processes upper-body joint states and sampled hand forces to produce a latent context variable that conditions the base standing policy in simulation. During deployment (bottom), the same encoder operates on measured upper-body joints and estimated hand forces to infer the latent context online, enabling rapid adaptation to upper-body-induced disturbances. 

as terrain, mass distribution and contact dynamics into a latent, and because those parameters cannot be measured on hardware, regresses that latent from proprioceptive history in a second stage. Domain randomization [11] forgoes the latent and buys robustness by exposure alone. Hand forces are not of that kind. The robot neither commands the load nor can predict it from its own action history, yet the load is recoverable at run time from the rigid-body model, so the latent need not stand in for an unmeasurable quantity and no second-stage regression is required. Recent humanoid work either exposes the policy to disturbance without representing it, through upper-body pose curricula [12] and force-aware training [13], or obtains it explicitly, through co-trained estimators of a base-applied force fed directly to the policy [14] and wrist-mounted force/torque sensing [15]. Each route either requires dedicated force sensing at deployment or conditions on a disturbance whose effect on the base is fixed by a known application point. Forces applied at the hands are different: the induced base moment depends jointly on the force and on the arm configuration through which it acts, so neither quantity alone determines the disturbance and the two must be represented together. 

inverse dynamics, requiring no wrist force/torque sensing, no force supervision, and no base-wrench measurement. The estimator itself is standard; what we show is that the policy’s advantage survives substituting the estimate for the applied force. 

- 3) We evaluate over 100 upper-body configurations sampled from the training pose distribution under swept hand forces, scoring each trial by a **task-level criterion** that requires the hands to stay near their commanded pose. Against a policy given the same estimated force without the joint encoding, task success rises from 16 _._ 6% to 38 _._ 9%, attributing the gain to the encoding rather than to the availability of the force signal. We further benchmark against **HOMIE** -style posecurriculum training [12] and **ALMI** [16], an adversarially trained whole-body controller. 

- 4) We validate FAME on the **Unitree H1-2** full-scale humanoid under representative load-interaction scenarios, including asymmetric single-arm pulling (RE1) and symmetric bimanual load augmentation (RE2), and evaluate on manipulation tasks in kitchen environments where the interaction forces arise from the task itself. 

The contributions of this paper are: 

- 1) We propose **FAME** , a force-adaptive standing framework that conditions a lower-body policy on a latent context encoding upper-body configuration and bimanual interaction force _jointly_ , rather than supplying the policy with two independent signals. 

- 2) We **deploy without force sensing** . The interaction force is not privileged but reconstructed online from measured joint torques and states through rigid-body 

## II. RELATED WORK 

## _A. Force-adaptive humanoid control_ 

Recent whole-body control research addresses stability under external interaction forces. FALCON [13] trains a dualagent policy with a torque-limit-aware 3D force curriculum for forceful tasks such as heavy lifting and cart-pulling. HAFO [17] models disturbances using virtual spring-damper 

2 

systems, Thor [18] introduces force-adaptive torso-tilt rewards to maximize peak interaction strength, and Heterogeneous Meta-Control [19] stitches position, impedance, and hybrid force-position modalities within a shared torque-space interface. These frameworks optimize how much force the robot can _apply_ during loco-manipulation. FAME targets the complementary quantity: the region of external hand loads and arm configurations under which stance remains stable, which bounds what manipulation can be attempted at all. 

## _B. Obtaining interaction forces at deployment_ 

Conditioning a policy on interaction force requires that force to be available at run time, and prior work takes two routes. Sensor-based methods instrument the contact: H2COMPACT [15] reads wrist-mounted force/torque sensors to infer human intent during human–humanoid co-manipulation and adapt contact trajectories online, at the cost of dedicated force sensing on the robot. Learning-based methods infer force from proprioception: RL-Force [14] co-trains an MLP estimator with the policy to regress a base-applied force vector and its point of application from a short proprioceptive history, feeding the estimate directly into the policy. The authors report two failure modes of this design. Transplanting the estimator into a separately trained policy destabilized both, indicating that it had learned a mapping valid only for the specific closed-loop dynamics it was trained inside. Further, the estimated force tracked the robot’s torso pitch closely enough to be largely predictable from it, suggesting that the estimator had learned to read the postural deflection the force produces rather than the force itself, which holds only while the policy responds to disturbances like training. 

FAME takes a third route, recovering the external force at each hand from the difference between modelled and measured joint torques through the wrist Jacobian, with the model evaluated by full inverse dynamics rather than a static approximation. This requires no wrist sensing, no force supervision, and no co-training, and because the mapping follows from the robot model rather than from data collected under a particular controller, the estimator is independent of the policy it serves. It is also independent of contact: formed from the rows of the equation of motion belonging to a single arm, it drops the unknown ground reaction identically rather than modelling or measuring it, and it needs no base-wrench measurement, which a physical robot does not have. Both properties are derived in Sec. III-C. 

## _C. Conditioning on disturbance context_ 

Rapid Motor Adaptation [9] learns a latent encoder of environment parameters in simulation and, because those parameters cannot be measured on hardware, trains a secondstage module to regress the latent from proprioceptive history; the paradigm has been extended to bipedal locomotion [10] and to manipulators [20]. A separate line forgoes explicit conditioning and relies on randomized exposure, with humanoid controllers training under continuously varying arm configurations via upper-body pose curricula [12], or adversarially, as in ALMI [16], which trains a locomotion 

policy against upper-body motions ordered by how much they destabilize the current policy. Both follow broader use of curricula for command ranges, terrain difficulty, and perturbation magnitude in legged locomotion [21], [22]. 

The two lines differ from our setting in what the policy can know. RMA needs a second stage because terrain and body parameters cannot be observed on hardware, whereas an external hand load is recoverable from the rigid-body model at run time, so its latent is built from a measured quantity rather than a regressed surrogate. Pose curricula and adversarial upper bodies perturb the stance with motion the robot itself generates and can therefore predict from its own action history; an external load is neither commanded nor anticipated. The same load produces a different base moment depending on the arm configuration it acts through, which motivates encoding the two jointly rather than as independent channels. Sec. IV-A.2 measures what that encoding contributes over supplying the same force unencoded. 

## III. METHODOLOGY 

FAME conditions a base standing policy on a learned latent representation of upper-body context. As illustrated in Fig. 2, the system has three components: an upper-body context encoder, which maps joint states and hand interaction forces to a latent vector describing the disturbance bimanual manipulation induces; a base standing policy, which that latent conditions; and a model-based estimator, which supplies the hand forces at deployment. Training exposes the policy to diverse disturbances by sampling external forces at the hands (Sec. III-B) and randomizing upper-body targets through a pose curriculum that expands as standing quality improves (Sec. III-A). Training supplies the hand force exactly, whereas a deployed robot has no such signal; we close that gap with a rigid-body estimator (Sec. III-C) that requires no wrist sensing and no supervision, and every result we report runs with the estimate in the loop. 

## _A. Upper-Body Pose Curriculum_ 

To train the standing controller under continuously varying upper-body configurations, we employ the pose curriculum of HOMIE [12] unchanged, which progressively widens the range of randomized target poses as standing quality improves. We maintain a scalar _upper-body action ratio ρa ∈_ [0 _,_ 1], initialized to 0 and increased by ∆ _ρ_ whenever the height-tracking reward exceeds a threshold. At each resampling event we draw an auxiliary ratio _ρ_<sup>_′_</sup> _a_<sup>_∈_[0</sup><sup>_,_1]that</sup> concentrates near zero early in training and broadens as _ρa_ grows, 


where _u ∼U_ (0 _,_ 1) and _κ_ = 20 controls sharpness. Let _q_ ub _∈_ R<sup>15</sup> denote the torso and arm joint positions. For each joint _j_ we sample _aj ∼U_ (0 _, ρa_<sup>_′_) and a target angle in a curriculum-</sup> scaled interval around the default posture _q_ ub<sup>0,</sup> 


3 

resampled every _T_ ub = 1 s. The evaluation poses of Sec. IVA are drawn from this same distribution, so the reported results measure behaviour inside the trained envelope rather than extrapolation beyond it. 

## _D. Base policy_ 

We formulate the base-policy training problem as a Partially Observable Markov Decision Process (POMDP) 


## _B. Upper-Body Context Encoder_ 

The disturbance a manipulation task imposes on stance is not determined by the hand force alone: the same force produces a different base moment depending on the arm configuration through which it acts. We therefore encode the two jointly rather than presenting either in isolation. The encoder _µθ_ , a multi-layer perceptron, maps the torso and arm joint positions _q_ ub _∈_ R<sup>15</sup> together with the two hand forces **F** _L,_ **F** _R ∈_ R<sup>3</sup> to a latent context vector 


It is trained end-to-end with the policy, with no force labels or auxiliary regression loss, and the policy receives the _Hz_ = 3 most recent latents appended to its proprioceptive history. During training the applied force is drawn isotropically, **F** = _r_ **_ξ_** _/∥_ **_ξ_** _∥_ 2 with **_ξ_** _∼N_ ( **0** _,_ **I** 3) and magnitude _r ∼ U_ ( _r_ min _, r_ max), giving unbiased coverage of the 3D force space. 

## _C. Estimating Hand Force at Deployment_ 

At deployment, the hand force is not given, and recovering it from the full-body dynamics is obstructed by the ground reaction, which is unknown and discontinuous at contact events. We remove it structurally. Let _A_ index the seven degrees of freedom of one arm; restricted to those rows, the equation of motion reads 


where **J** _h_ is the Jacobian of the loaded point on the hand and **J** _c_ that of a foot contact carrying the unknown reaction **f** _c_ . Moving an arm joint does not displace either foot, so the columns of every **J** _c_ at the rows _A_ are identically zero and the contact sum vanishes: the ground reaction leaves the problem without being measured or modelled. The same argument decouples the two arms. Evaluating the left-hand side rigid-body inverse dynamics with the recursive Newton– Euler algorithm and accounting for the actuator-side rotor inertia **B** and joint damping **D** gives 


For the 7-DoF arm, this gives seven scalar equations for the three components of the hand force. We therefore estimate **F**<sup>ˆ</sup> by solving the resulting overdetermined system in the leastsquares sense and pass the result to the encoder. Both **J** _h_ and the RNEA term are evaluated online with Pinocchio [23]. 

and utilize Proximal Policy Optimization (PPO) [6] to learn a parameterized policy _πθ_ ( _at | ot_ ) that maximizes the expected return 


The policy observation concatenates a three-step proprioceptive history with the latent context of Sec. III-B, 


where **p** _t_ collects base angular velocity, projected gravity, command, joint positions, joint velocities and the previous action; the state space is detailed in Sec. A. We implement PPO from the RSL-RL library [24]. Table I summarizes the rewards used to train the policy for the Unitree H1-2. 

|**Term**|**Expression**<br>**Weight**|**Remarks**|
|---|---|---|
||**Base Stability & Uprightness**||
|Base height tracking<br>Vertical velocity|exp(_−_4_|h_base_−h_cmd_|_)<br>3_._0<br>_v_<sup>2</sup><br>_z_<br>_−_5_._0<br>|_h_cmd = 1_._0<br>Penalize bouncing|
|Angular velocity (xy)|_∥_**_ω_**_xy∥_<sup>2</sup><br>2<br>_−_0_._1<br>|Suppress roll/pitch motion|
|Orientation|_∥_**_g_**_xy∥_<sup>2</sup><br>2<br>_−_3_._0|Projected gravity error|
|Stand still (zero command)|1(motion at zero cmd)<br>_−_0_._8|Encourage static stability|
||**Posture & Joint Deviation**<br><br>||
|Hip deviation|_∥_**_q_**hip_−_**_q_**<sup>0</sup><br>hip<sup>_∥_2</sup><br>2<br>_−_0_._2<br><br>||
|Ankle deviation|_∥_**_q_**ankle_−_**_q_**<sup>0</sup><br>ankle<sup>_∥_2</sup><br>2<br>_−_0_._5<br>||
|Knee deviation|_|_(_d_knee_−_0_._5)_·_(_h_base_−h_cmd)_|_<br>_−_1_._5<br>|Height-coupled shaping|
|Joint tracking error|_∥_**_q_**target_−_**_q_**_∥_<sup>2</sup><br>2<br>_−_0_._1<br><br>||
|DoF acceleration|_∥_¨**_q_**_∥_<sup>2</sup><br>2<br>_−_2_._5_×_10<sup>_−_5</sup>||
||**Feet Contact & Grounding**||
|Feet lateral distance|clamp(_d_feet)<br>0_._5|Maintain stance width|
|Knee lateral distance|clamp(_d_knee)<br>1_._0||
|Feet parallel|Var(_d_feet)<br>_−_2_._5|Symmetry constraint|
|Feet ground parallel|Var(_h_feet)<br>_−_2_._0||
|Feet slip|_∥_**_v_**feet_,xy∥_2<br>_−_1_._0||
|Feet stumble|1(_F _<sup>_xy _</sup>_>_3_F _<sup>_z_</sup>)<br>_−_1_._5<br>||
|Feet contact forces|max(_∥F∥−_900_,_0)<br>_−_2_._5_×_10<sup>_−_4</sup><br>||
|Contact momentum|_v_<sup>_−_</sup><br>_z _<sup>_·_ (</sup><sup>_F_</sup>_z _<sup>_−_50)</sup><br>2_._5_×_10<sup>_−_4</sup>|Encourage soft landing|
|No-fly (single contact)|1(single foot contact)<br>0_._75||
||**Control Smoothness & Energy**<br>||
|Action rate|_∥_**_a_**_t −_**_a_**_t−_1_∥_<sup>2</sup><br>2<br>_−_0_._02<br>||
|Second-order smoothness|_∥_**_a_**_t −_2**_a_**_t−_1+**_a_**_t−_2_∥_<sup>2</sup><br>2<br>_−_0_._1<br>||
|Joint power|�_|_˙_qiτi|_<br>_−_2_×_10<sup>_−_5</sup><br><br>||
|Torque penalty|_∥_**_τ_**_∥_<sup>2</sup><br>2<br>_−_2_._5_×_10<sup>_−_6</sup>||
|Action vanish|action saturation error<br>_−_1_._0||
||**Safety & Limits**||
|DoF position limits<br>DoF velocity|limit violation<br>_−_2_._0<br>_∥_˙**_q_**_∥_<sup>2</sup><br>2<br>_−_5_×_10<sup>_−_3</sup><br>|Soft limit = 0.975|
|DoF velocity limits|soft vel violation<br>_−_2_×_10<sup>_−_3</sup>||
|Torque limits|soft torque violation<br>_−_0_._1|Soft limit = 0.95|


TABLE I: Standing reward components and weights, adjusted from [12] for Unitree H1-2. 

The policy outputs a 12D action **_a_** _t ∈_ R<sup>12</sup> , corresponding to target joint position offsets for the lower-body joints (6 per leg). We compute target joint positions as 


where **_q_** lb<sup>0isthedefaultlower-bodypostureand</sup><sup>_sa_isan</sup> action scaling factor. Targets are tracked by a joint-space PD controller running at 50 Hz: 


4 

|||**Inform**|**ation availab**|**le**|**Task suc**|**cess** (%)|**Deviation**|
|---|---|---|---|---|---|---|---|
|**Variant**|Pose<br>curr.|Force to<br>policy|Arm cfg.<br>in encoder|Latent<br>encoding|_T_=150mm|_T_=250mm|∆EE (mm)|
|**FAME-pose** (HOMIE-style [12])|✓|—|✓|✓|4.3|5.6|242.4|
|**+Curr+F**raw|✓|✓|—|—|16.6|21.7|220.3|
|ALMI [16]|_adver_|_sarial motio_|_n imitation; n_|_o force input_|24.7|39.3|202.3|
|**FAME**|✓|✓|✓|✓|**38.9**|**48.5**|**179.6**|


TABLE II: Standing under swept hand-force disturbances over 100 upper-body configurations sampled from the training pose distribution (protocol in Sec. IV-A). A trial succeeds if the robot stays upright _and_ peak end-effector deviation remains below _T_ ; poses a policy cannot hold count as failures rather than exclusions. ∆EE is the force-induced hand displacement at _T_ =250 mm, differenced against the same trial run without force. ALMI is a separately trained locomotion policy, whose lower body is optimized against upper-body motion its own arms generate. All controlled variants receive the full 27-joint proprioceptive history. 

## _E. Training Variants_ 

We train three variants that differ only in what upperbody context reaches the policy. **FAME-pose** encodes the arm configuration alone, _zt_ = _µ_ ( _q_ ub); **F** raw concatenates the two hand forces into the observation without encoding; **FAME** encodes both jointly, _zt_ = _µ_ ([ _q_ ub _, F_<sup>_L_</sup> _, F_<sup>_R_</sup> ]). **FAMEpose** against **FAME** isolates the force channel, since both compress upper-body context to a latent of the same width and differ only in whether force is part of it; **F** raw against **FAME** isolates the representation, since both receive the force and differ only in whether it is concatenated directly or compressed jointly with the arm configuration. All three share the pose curriculum, reward function, force sampling, domain randomization, network widths, optimizer settings, and step budget, and the concatenated variant is given the same history depth _Hz_ = 3 as the latent, so that each comparison isolates the representation rather than the temporal context available to the policy. 

## IV. EXPERIMENTS 

Our evaluation addresses three questions. **Q1:** does conditioning on force configuration context expand the range of hand loads under which the robot can keep standing and hold its hands where the task put them? **Q2:** is the latent encoding responsible for that gain, or is the availability of force information sufficient on its own? **Q3:** does the result transfer beyond the environment in which it was trained to a different simulator and task set, and to hardware, where the force the policy conditions on is no longer exact? 

## _A. Simulation Protocol_ 

We sample 100 upper-body configurations from the training pose distribution of Sec. III-A at full curriculum. Each configuration is held fixed for the trial while the lower body stands, and receives 25 force draws: a per-hand horizontal magnitude _r ∼U_ (0 _,_ 20) N shared by both hands, an independent uniform horizontal direction at each hand, and an independent vertical component _Fz ∼U_ ( _−_ 30 _,_ 30) N. Spreading trials along the force axis rather than repeating one magnitude is deliberate: the between-configuration term dominates the standard error and does not shrink with trials 

per configuration. This gives 2500 loaded trials per policy over a 10 s, with the first 2 s discarded as settling. The hand force supplied to the encoder is the estimate of Sec. III-C. 

_a) Task-level error:_ Standing is a means, not the task. A controller that stays upright but lets the hands drift has still failed the manipulation it was standing for. We therefore run each trial twice, once with the force, once without, from the same initial state, and difference the two hand trajectories pointwise. 


Everything that is not the disturbance cancels: the commanded height, the baseline drift, the settling transient. What remains is what the load did to the hand. The pairing also makes policies with different command interfaces directly comparable, since any term common to both runs vanishes. 

_b) Success criterion:_ A trial succeeds if the robot remains upright _and_ the peak ∆EE over the horizon stays below a task tolerance _T_ ; we report _T_ = 150 mm and _T_ = 250 mm, spanning the placement accuracy a bimanual carry or door-opening task would demand. A fall is a task failure, not a missing measurement, so falls are censored at _T_ rather than excluded. A policy that fails often is penalised rather than scored only on the trials it survived. Because the task is standing, a policy that recovers by walking out from under the load has also failed it: trials displacing either foot by more than 0 _._ 15 m are counted as failures. Q1 and Q2 share this protocol and are reported together in Table II. 

_1) Q1: Envelope Expansion:_ **FAME-pose** and **FAME** differ only in whether the interaction force enters the encoded context, so the contrast isolates the force channel. 

**Results and Discussion.** Force conditioning raises task success from 4 _._ 3% to 38 _._ 9% at _T_ =150 mm and from 5 _._ 6% to 48 _._ 5% at _T_ =250 mm, close to a ninefold gain at both tolerances. Deviation moves with it: peak displacement falls from 242 _._ 4 to 179 _._ 6 mm, so the trials FAME does not convert into successes it still loses by a smaller margin. The pose curriculum alone therefore leaves most of the admissible envelope unreached, which shows what the policy needs is not further exposure to arm configurations but knowledge of the load acting through them. 

5 


Fig. 3: **Real-robot qualitative results.** Snapshot sequence from our real-robot evaluation on the Unitree H1-2 under representative load-interaction disturbances (RE1–RE2). For each experiment, we report the joint trajectories and torques of the hip pitch, ankle pitch, and elbow joints. With FAME, the robot remains stable under external loads and the joint positions stay close to their nominal standing configuration (marked in green). With FAME-pose, the joint positions drift away from the stable configuration, ultimately causing the robot to lose balance and fall (marked in red). 

_2) Q2: Encoding versus Raw Force Input:_ Sec. IV-A.1 establishes that a force-conditioned policy outperforms one without force information, but not whether the latent encoding contributes beyond the availability of that information. **+Curr+F** raw versus **FAME** resolves this: both receive the interaction force and differ only in whether it is concatenated into the observation or compressed jointly with the arm configuration into a latent of fixed width. Both are given the same history depth, so the comparison is of representation rather than of temporal context. 

**Results and Discussion.** Availability of force is not sufficient. +Curr+Fraw reaches 16 _._ 6% and 21 _._ 7%, well ahead of FAME-pose’s 4 _._ 3% and 5 _._ 6%. The force signal plainly carries usable information, but under half of FAME’s 38 _._ 9% and 48 _._ 5%. Its deviation, 220 _._ 3 mm, sits nearer FAME-pose’s 242 _._ 4 than FAME’s 179 _._ 6. These results indicate that much of the gain arises from jointly representing force and arm configuration rather than simply providing the force signal. The result also reflects on the co-trained estimate design of [14], the gain we measure comes from the representation of the force, not merely from having obtained one. 

**Comparison with adversarially trained locomotion ALMI [16]** : It acquires robustness without representing the disturbance. Its lower body is trained against upperbody motion that its own arms generate, and its observation carries no force channel, so the comparison tests whether robustness to endogenous disturbance transfers to sustained exogenous hand loading. It transfers partially. ALMI reaches 24 _._ 7% task success at _T_ =150 mm and 39 _._ 3% at _T_ =250 mm, ahead of every variant that lacks the joint encoding but behind FAME’s 38 _._ 9% and 48 _._ 5%, and its deviation of 202 _._ 3 mm exceeds FAME’s 179 _._ 6 mm. The gap narrows as the tolerance widens: ALMI gains 14 _._ 6 points between the 

two tolerances where FAME gains 9 _._ 6, indicating that its failures are concentrated as near-misses in that band. It keeps the robot upright without keeping the hands still. This behavior is suitable for locomotion recovery but violates the fixed-stance requirement of the manipulation setting. 

_3) Q3: Transfer Beyond the Training Environment:_ **Simto-sim: task-level manipulation** Forces produced by a task are neither isotropic nor independent of the robot’s own motion, unlike the sampled disturbances of Sec. IV-A. We therefore repeat the comparison on the GOLEM platform [1], which exposes FAME and ALMI behind a common velocitycommand interface in a MuJoCo kitchen twin, with the upper body driven by a shared inverse-kinematics stack so that the comparison isolates lower-body behaviour. The task, a single-arm pick of a 3 kg object from the counter, is shown in Fig. 4; we run 10 seeds varying the object and its spawn pose, both policies on every seed. Additional kitchen interaction in a different environment, the opening of the refrigerator door (Fig 1, bottom row), is qualitatively demonstrated. 

**Results and Discussion.** Both policies hold the stance while the arm reaches and closes on the object. FAME then falls on 1 of 10 seeds against ALMI’s 5, with median peak pelvis displacement of 0 _._ 065 m against 0 _._ 641 m and median peak tilt of 7 _._ 1<sup>_◦_</sup> against 30 _._ 5<sup>_◦_</sup> . ALMI yields to the load and repositions its feet, correct for a locomotion controller and wrong when the feet are where the task placed them. The seed FAME fails is one ALMI fails too. 

**Sim-to-real: hardware deployment.** We deploy on the Unitree H1-2, which has 27 degrees of freedom: two 7-DoF arms, two 6-DoF legs, and a 1-DoF waist. Base orientation and angular velocity come from the onboard IMU, joint angles and velocities from the joint encoders; no wrist force/torque sensor is used. The base policy runs in real 

6 


Fig. 4: Task-level comparison in the GOLEM kitchen twin. Both policies perform the same single-arm pick of a loaded object, with the upper body driven by a shared inverse-kinematics stack so that the lower body is the only variable. Left: one seed; FAME holds its stance, ALMI steps out from under the load and falls. Right: pelvis drift over 10 seeds. 

time at 50 Hz. We evaluate two scenarios: **RE1: Asymmetric Single-Arm Load** applies a load through one arm, producing an unbalanced moment about the stance. **RE2: Symmetric bimanual** load distributes the weight across both arms. 

**Results and Discussion.** As shown in Fig. 3, FAME held its stance in 3/3 trials of both RE1 and RE2, while FAMEpose lost balance and fell in 3/3 of each. The difference is clearest in the hip-pitch and ankle-pitch trajectories: FAME regulates joint torque to hold these joints near the nominal standing posture, whereas FAME-pose does not account for the external load and the joint positions drift until the balanced pose is lost. 

## V. CONCLUSION 

We presented FAME, a force-adaptive RL framework that expands the manipulation envelope of a full-scale humanoid by conditioning standing control on a latent context encoding upper-body configuration and bimanual interaction force jointly, with the force reconstructed online from joint torques rather than measured. Over 100 arm configurations sampled from the training pose distribution and scored by loadinduced displacement, FAME reaches 38 _._ 9% task success at a 150 mm tolerance, against 16 _._ 6% for a policy given the same estimated force without the encoding, 4 _._ 3% for a poseconditioned curriculum policy, and 24 _._ 7% for an adversarially trained locomotion policy. The first contrast holds the force input fixed and varies only its representation, attributing the gain to the joint encoding. The same estimator runs unchanged on kitchen manipulation tasks and on the Unitree H1-2, where the advantage persists despite a noisier estimate. Extending the joint encoding to load-carrying locomotion, where the feet may move but the hands must still arrive, is the natural next step. 

## ACKNOWLEDGMENT 

This work has been supported by ARPA-E contract DEAR0001966. We are grateful for this support. We leverage generative AI tools (Opus-5) for structural and grammatical proofreading in all sections and for assistance in generating 

code for plots in this manuscript. N. Correll is CEO of Realtime Manufacturing, Inc., which is working on humanoids for manufacturing applications. 

## REFERENCES 

- [1] M. Conway, W. Xie, A. Devaraj, Y. Zhang, N. Pudasaini, M. Feit, A. Abid, Z. Allen, C. Liu, X. Tan, J. Lavering, J. Chen, L. Antieau, A. V. Pischke, A. Roncone, Z. Sunberg, and N. Correll, “Golem: Modular humanoid autonomy towards electric vehicle battery disassembly,” 2026. 

- [2] S. Gupta and A. Kumar, “A brief review of dynamics and control of underactuated biped robots,” _Advanced Robotics_ , vol. 31, no. 12, pp. 607–623, 2017. 

- [3] J. Reher and A. D. Ames, “Dynamic walking: Toward agile and efficient bipedal robots,” 2020. 

- [4] S. Kajita, F. Kanehiro, K. Kaneko, K. Yokoi, and H. Hirukawa, “The 3D linear inverted pendulum mode: A simple modeling for a biped walking pattern generation,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , vol. 1, pp. 239–246, 2001. 

- [5] P. M. Wensing and D. E. Orin, “High-speed humanoid running through control with a 3d-slip model,” in _2013 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 5134–5140, 2013. 

- [6] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” 2017. 

- [7] X. Gu, Y.-J. Wang, and J. Chen, “Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer,” _arXiv preprint arXiv:2404.05695_ , 2024. 

- [8] N. Heess, D. TB, S. Sriram, J. Lemmon, J. Merel, G. Wayne, Y. Tassa, T. Erez, Z. Wang, S. M. A. Eslami, M. Riedmiller, and D. Silver, “Emergence of locomotion behaviours in rich environments,” 2017. 

- [9] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “Rapid motor adaptation for legged robots,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2021. 

- [10] A. Kumar, Z. Li, J. Zeng, D. Pathak, K. Sreenath, and J. Malik, “Adapting rapid motor adaptation for bipedal robots,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 1161–1168, 2022. 

- [11] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel, “Domain randomization for transferring deep neural networks from simulation to the real world,” in _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 23–30, 2017. 

- [12] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit,” in _Proceedings of Robotics: Science and Systems_ , (LosAngeles, CA, USA), June 2025. 

- [13] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Aghamohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi, “Falcon: Learning force-adaptive humanoid loco-manipulation,” _arXiv preprint arXiv:2505.06776_ , 2025. 

7 

- [14] W. Lin, L. Qian, S. Wang, J. Qiang, P. Sun, and X. Luo, “Rlforce: Reinforcement learning with force estimation for humanoid locomotion subject to continuous external disturbances,” in _Intelligent Robotics and Applications_ (T. Matsuno, H. Liu, L. Liu, Z. Yin, X. Zhu, W. Ren, Z. Wang, and Y. Sheng, eds.), (Singapore), pp. 52–64, Springer Nature Singapore, 2026. 

- [15] G. C. R. Bethala, H. Huang, N. Pudasaini, A. M. Ali, S. Yuan, C. Wen, A. Tzes, and Y. Fang, “H2-compact: Human-humanoid co-manipulation via adaptive contact trajectory policies,” in _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pp. 1004–1011, 2025. 

- [16] J. Shi, X. Liu, D. Wang, O. Lu, S. Schwertfeger, F. Sun, C. Bai, and X. Li, “Adversarial locomotion and motion imitation for humanoid policy learning,” in _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [17] C. Dong, H. Xu, W. Feng, Z. Wang, Y. Zhou, Y. Zhao, and B. He, “Hafo: A force-adaptive control framework for humanoid robots in intense interaction environments,” _Control Engineering Practice_ , vol. 173, p. 106978, 2026. 

- [18] G. Li, Q. Shi, Y. Hu, J. Hu, Z. Wang, X. Wang, and S. Luo, “Thor: Towards human-level whole-body reactions for intense contact-rich environments,” _ArXiv_ , vol. abs/2510.26280, 2025. 

- [19] L. Wei, X. Peng, R.-Z. Qiu, T. Huang, X. Cheng, and X. Wang, “Hmc: Learning heterogeneous meta-control for contact-rich locomanipulation,” 2025. 

- [20] Y. Liang, K. Ellis, and J. Henriques, “Rapid motor adaptation for robotic manipulator arms,” in _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 16404–16413, 2024. 

- [21] J. Hwangbo, J. Lee, A. Dosovitskiy, D. Bellicoso, V. Tsounis, V. Koltun, and M. Hutter, “Learning agile and dynamic motor skills for legged robots,” _Science Robotics_ , vol. 4, Jan. 2019. 

- [22] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _5th Annual Conference on Robot Learning_ , 2021. 

- [23] J. Carpentier, G. Saurel, G. Buondonno, J. Mirabel, F. Lamiraux, O. Stasse, and N. Mansard, “The pinocchio c++ library – a fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives,” in _IEEE International Symposium on System Integrations (SII)_ , 2019. 

- [24] C. Schwarke, M. Mittal, N. Rudin, D. Hoeller, and M. Hutter, “Rsl-rl: A learning library for robotics research,” _arXiv preprint arXiv:2509.10771_ , 2025. 

- [25] J. Long, Z. Wang, Q. Li, L. Cao, J. Gao, and J. Pang, “Hybrid internal model: Learning agile legged locomotion with simulated robot response,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

## APPENDIX 

## _A. State Space Design_ 

**Actor (policy) observations.** The actor observation at = time _t_ is a stacked history of length _Ha_ = 3: **_o_**<sup>_π_</sup> _t_ [ **_o_** _t,_ **_o_** _t−_ 1 _,_ **_o_** _t−_ 2] _,_ where each one-step vector **_o_** _t ∈_ R<sup>_do_</sup> is defined in Table III. 

|**Actor observation term (one-step)**<br>**Symbol**|**Dim**|
|---|---|
|Command (scaled)<br>**_c_**_t_<br>|3|
|Commanded base height<br>_h_<sup>cmd</sup><br>_t_|1|
|IMU angular velocity (body frame)<br>**_ω_**_t_|3|
|Projected gravity (body frame)<br>**_g_**_t_|3|
|Joint position error (scaled)<br>˜**_q_**_t_<br>˜|_N_dof|
|Joint velocity (scaled)<br>˙**_q_**_t_|_N_dof|
|Previous action<br>**_a_**_t−_1|_N_act|
|_do_ = 3+1+3+3+2_N_dof+_N_act = 76 (_N_dof=27, _N_act=<br><br>|12)<br>|
|dim(**_o_**<sup>_π_</sup><br>_t_ <sup>) =</sup><sup>_Hado_ +</sup><sup>_Hz ·_ 8 = 228+ 24 = 252 (</sup><sup>_Ha_=</sup>|<sup>_Hz_=3)</sup>|


## TABLE III: Actor (policy) observation space. 

**Critic (value) observations.** The critic uses a privileged one-step vector **_o_**<sup>_V_</sup> _t_<sup>_∈_R</sup><sup>_dv_thataugments</sup><sup>**_o_**</sup><sup>_t_withthebase</sup> linear velocity (available in simulation). We use a history length _Hc_ = 1, i.e., **_o_**<sup>_V_</sup> _t_<sup>only,assummarizedinTableIV.</sup> 

|**Critic observation term**|**Symbol**|**Dim**|
|---|---|---|
|All actor one-step terms|**_o_**_t_|76|
|Latent context (from encoder)|**_z_**_t_<br>|8|
|Base linear velocity (privileged, scaled)|**_v_**<sup>base</sup><br>_t_|3|
|**One-step critic obs:** _dv_ =_do_+ 8 + 3<br>|= 87||
|**History stacking:** _Hc_ = 1_⇒_dim(**_o_**<sup>_V_</sup><br>_t_ <sup>)</sup>|<sup>= 87</sup>||


TABLE IV: Critic observation design. The critic is additionally provided latent context **_z_** _t_ and privileged base linear velocity in simulation during training. 

## _B. Domain Randomization_ 

Table V summarizes the domain randomization strategies that we used. 

|**Term**|**Value**|
|---|---|
||**External Disturbances**<br>|
|Push robot<br>Upper-body|interval= 4 s, _v_xy _∼U_(0_,_0_._5) m_/_s<br>_ρa ←_0_._0 initially; increased with standing|
|disturbance<br>curriculum|quality, interval = 1 s|
|**Ac**|**tuation & Observation Noise**<br>|
|Joint injection noise|_q ←q_+_ϵ_, _ϵ ∼U_(_−_0_._05_,_0_._05)|
|Actuation offset<br>Control delay|_a ←a_+_δ_, _δ ∼U_(_−_0_._05_,_0_._05)<br>enabled|
|**Inertial **<br>|**& Body Parameter Randomization**<br>|
|Payload mass|_m_payload _∼U_(_−_3_,_5) kg|
|Hand payload mass|_m_hand = 0 (disabled)<br>|
|Body displacement|∆**_p_**body _∼U_(_−_0_._1_,_0_._1) m<br>|
|Link mass scaling|_m_link _←s m_default, _s ∼U_(0_._8_,_1_._2)|
||**Contact Randomization**<br>|
|Friction coefficient|_µ ∼U_(0_._1_,_3_._0)|
|Restitution|_e ∼U_(0_._0_,_1_._0)|
||**Controller Randomization**<br>|
|Proportional gain|_kp ←s kp,_default, _s ∼U_(0_._9_,_1_._1)|
|Derivative gain|_kd ←s kd,_default, _s ∼U_(0_._9_,_1_._1)|
|Initial joint position|_q_0 _←s q_0_,_default, _s ∼U_(0_._8_,_1_._2); then<br>_q_0 _←q_0+∆_q_, ∆_q ∼U_(_−_0_._1_,_0_._1)|


TABLE V: Domain randomizations used for training the standing policy. _U_ ( _·_ ) denotes a uniform distribution. 

## _C. Upper-Body Context Encoder_ ( _µ_ ) _and Base Policy_ ( _π_ ) _Architectures_ 

In our framework, for the upper-body context encoder _µ_ , we use an MLP that maps upper-body pose and bimanual interaction forces to a latent context _zt_ , which conditions the actor for force-adaptive standing. For the actor-critic, we use HIM-style [25], [12], where the actor consists of an estimator network _E_ and a follow-up policy network _N_ , and the critic is a separate value network _C_ . 

## _D. Hyperparameters_ 

Table VI presents the hyperparameters used for training. 

|**Hyperparameter**|**Value**|**Hyperparameter**|**Value**|
|---|---|---|---|
|Optimizer|Adam<br>|Discount factor _γ_|0.99|
|Learning rate|1_×_10<sup>_−_3</sup>|GAE _λ_|0.95|
|Schedule|adaptive|Clip param _ϵ_|0.2|
|Learning epochs|5|Value loss coef|1.0|
|Mini-batches|4|Clipped value loss|True|
|Max grad norm|1.0|Entropy coef|0.01|
|Init noise std|1.0|Desired KL|0.01|
|Actor / critic MLP|[512, 256, 256]|Symmetry scale|1.0|
|Activation|ELU|||


TABLE VI: PPO hyperparameters used for training. 

8 

