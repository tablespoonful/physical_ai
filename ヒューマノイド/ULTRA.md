---
title: "ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation"
date: "2026-03-03"
authors: "Xialin He; Sirui Xu; Xinyao Li; Runpei Dong; Liuyu Bian; Yu-Xiong Wang"
url: https://arxiv.org/abs/2603.03279
pdf: https://arxiv.org/pdf/2603.03279
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.03279)** / [論文ページ](https://arxiv.org/abs/2603.03279)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation** 

Xialin He<sup>_†_</sup> Sirui Xu<sup>_†_</sup> Xinyao Li Runpei Dong Liuyu Bian Yu-Xiong Wang<sup>_‡_</sup> Liang-Yan Gui<sup>_‡_</sup> 

University of Illinois Urbana-Champaign 

> _†_ Equal Contribution _‡_ Equal Advising https://ultrahumanoid.github.io/ 


Fig. 1: ULTRA is an **all-in-one** controller for humanoid loco-manipulation that supports: **Top:** dense motion tracking from different references; **Middle:** _fine-grained control_ from operator commands; **Bottom:** _long-horizon goal_ following with _egocentric perception_ . It demonstrates autonomous whole-body behavior without relying on test-time motion references under real sensing. We provide additional examples in our project webpage. 

**_Abstract_ — Achieving autonomous and versatile whole-body loco-manipulation remains a central barrier to making humanoids practically useful. Yet existing approaches are fundamentally constrained: retargeted data are often scarce or low-quality; methods struggle to scale to large skill repertoires; and, most importantly, they rely on tracking predefined motion references rather than generating behavior from perception and high-level task specifications. To address these limitations, we propose ULTRA, a unified framework with two key components. First, we introduce a physics-driven neural retargeting algorithm that translates large-scale motion capture to humanoid embodiments while preserving physical plausibility for contact-rich interactions. Second, we learn a unified multimodal** 

**controller that supports both dense references and sparse task specifications, under sensing ranging from accurate motioncapture state to noisy egocentric visual inputs. We distill a universal tracking policy into this controller, compress motor skills into a compact latent space, and apply reinforcement learning finetuning to expand coverage and improve robustness under out-of-distribution scenarios. This enables coordinated whole-body behavior from sparse intent without test-time reference motions. We evaluate ULTRA in simulation and on a real Unitree G1 humanoid. Results show that ULTRA generalizes to autonomous, goal-conditioned whole-body locomanipulation from egocentric perception, consistently outperforming tracking-only baselines with limited skills.** 

## I. INTRODUCTION 

Real-world loco-manipulation requires autonomy beyond replaying fixed reference motions: a humanoid must span a continuum from dense motion references to sparse task goals, and from accurate state estimation to onboard sensing. Yet many controllers treat these as separate regimes and focus mainly on reference tracking [1], [2], creating a precision-flexibility trade-off: dense-tracking policies break down when references are missing or infeasible, while purely goal-conditioned ones lack fine-grained coordination. We seek a unified controller that smoothly transitions between dense plans and sparse intent as information changes. 

Despite progress in co-tracking humanoid and object dynamics [3], two bottlenecks hinder unified autonomy. First, kinematic retargeting can yield physically inconsistent demonstrations that fail in contact-rich tasks. Second, existing architectures typically assume a fixed conditioning structure tailored to one input type, and cannot interpret diverse or partial supervision within a consistent framework. Under shifting observability and goals at deployment, this rigidity leads to systemic instability. 

To overcome the demonstration bottleneck, we introduce a physics-driven, _neural_ retargeting algorithm that transfers large-scale motion capture (MoCap) to humanoid embodiments at scale. Unlike kinematic retargeting [2], [4], [5], which struggles to maintain physical consistency in contactrich tasks, our retargeting is dynamics- and contact-aware by construction. We cast retargeting as simulation-constrained optimization with kinematic, dynamic, and contact constraints, and solve it with reinforcement learning (RL) at scale. Once trained, the policy generates large-scale physically feasible trajectories and generalizes to arbitrary data, enabling augmentation by scaling both objects and motions. 

Building on this expanded corpus, we learn a _U_ nified mu _LT_ imodal cont _R_ oller for _A_ utonomous humanoid control (ULTRA) that shifts from reference replay to perceptiondriven, goal-conditioned control. We first train a privileged universal tracker, then distill it into a student that follows diverse goal specifications, from dense references to sparse long-horizon targets (Fig. 1). This is enabled by ( **i** ) unified tokenization with availability masking [6], which keeps a single policy stable when references or modalities are missing; and ( **ii** ) a variational skill bottleneck plus RL finetuning [7] geared toward deployment with realistic perception and sensor noise. The bottleneck resolves ambiguity under sparse goals by maintaining coherent motion, while RL finetuning shifts control from reference-conditioned tracking to closed-loop goal stabilization under partial observability and distribution shift. Together, ULTRA yields one policy that tracks references when available and executes from egocentric perception and sparse intent when they are not. 

In summary, ULTRA presents a unified system for practical whole-body loco-manipulation with three components: ( **1** ) a physics-driven neural retargeting framework that scales MoCap to humanoid embodiments and supports zero-shot augmentation; ( **ii** ) a versatile _multimodal_ controller distilled 

from a privileged tracker that supports reference tracking and goal following across sensing modalities, including blind, MoCap-based, and depth-perception settings; and ( **iii** ) simulation and real-world evaluation on Unitree G1, showing that a unified model can outperform tracking baselines when references exist while enabling goal-conditioned behaviors. 

## II. RELATED WORK 

## _A. Motion Retargeting_ 

Retargeting transfers motion across embodiments with different morphologies. It originated in animation, where inverse-kinematics optimization adapted motions under kinematic constraints [8], and later evolved into learning-based mappings that amortized transfer for better generalization [9]. Humanoid retargeting requires stronger constraints because executability is contact-dependent and subject to joint limits and dynamics. As a result, existing robot retargeting methods trade off efficiency and physical fidelity: kinematic approaches are fast but often under-model dynamics and degrade in contact-rich settings [2], [4]–[6], [10], while physics-based retargeting enforces dynamics for physically plausible motions, but relies on expensive optimization, typically per-trajectory RL [11] or costly samplingbased methods [12]. We target the missing regime: _physicsdriven yet scalable_ retargeting that preserves interaction semantics without per-trajectory RL. We perform large-scale retargeting with a single unified policy, and enable zero-shot augmentation to expand coverage. 

## _B. Humanoid Whole-Body Locomotion_ 

Leveraging human motion data to teach humanoid robots complex skills has been widely studied. Early methods often used model-based control ( _e.g._ , trajectory optimization and model predictive control) to bridge embodiment and dynamics, while recent learning-based systems achieve precise tracking and agile motion replay [1], [13]–[19]. Beyond pure tracking, recent work moves toward foundation-style control by distilling large motion corpora into reusable priors, where a single model tracks diverse motions and supports multiple control modes [20]–[23]. Others shape latent priors with adversarial RL [24]–[27], but have not shown reliable scaling to large, heterogeneous loco-manipulation corpora. ULTRA follows the scalable teacher-student distillation paradigm but addresses a key bottleneck: offline distillation is limited by the state coverage of teacher rollouts. While less severe for humanoid-only control with more structured spaces, it becomes acute in high-dimensional robot-object interaction. To address this, we draw inspiration from animation practice [7] and use a two-stage framework: large-scale distillation followed by RL finetuning that _expands_ interactionstate coverage and improves robustness to out-of-distribution (OOD) goals and executions. 

## _C. Humanoid Whole-Body Loco-Manipulation_ 

Most humanoid motion tracking emphasizes reproducing human motion on the robot and treats environmental dynamics as secondary [13], [28]–[30], which is brittle for contact- 

IV. METHOD 

rich loco-manipulation. Recent work couples humanoid motion and object interaction via co-tracking and shows strong agility [1], [2], [31], [32], but often assumes limited data replay or relies on external object state estimation ( _e.g._ , motion capture), limiting autonomy under onboard egocentric sensing. Other approaches use hierarchical designs that generate trajectories/keypoints and track them with a universal controller [17], [33]; however, stacking a highlevel planner on a low-level controller can accumulate error and violate physical constraints. Adversarial motion priors broaden coverage but are typically task-specific, requiring careful objective engineering and scaling poorly to large, heterogeneous loco-manipulation corpora [34]. ULTRA addresses these issues by learning a goal-conditioned policy that unifies dense tracking and sparse task specifications in a _shared_ latent space, and by using RL finetuning to induce _closed-loop_ behaviors that expand interaction-state coverage. This yields a _versatile_ single-policy controller under realworld perception with a _scalable_ paradigm that leverages broad motion corpora. 

## III. PROBLEM FORMULATION AND PRELIMINARIES 

## _A. Task Interface_ 

We study whole-body loco-manipulation tasks where a humanoid interacts with a manipulated object, specified by a _goal_ signal **_c_** _∈C_ that defines the task objective. A rollout succeeds if the terminal outcome satisfies **_c_** , _e.g._ , the humanoid root and/or the object reaches target transformations within a tolerance. At each time step _t_ , the policy receives ( **i** ) an observation **_o_** _t ∈O_ and ( **ii** ) task conditioning **_c_** _t_ , and outputs an action **_a_** _t ∈A_ . Here **_a_** _t_ specifies target joint positions executed by a PD controller. 

**Goal specification.** We consider two forms of **_c_** : ( **i** ) _dense reference conditioning_ , which provides a time-indexed motion reference and thus specifies intermediate motions; and ( **ii** ) _sparse goal conditioning_ , which specifies long-horizon target transformations for the humanoid root and/or object while leaving intermediate motions underdetermined. **Perception.** Beyond proprioception, we consider two regimes for object sensing: ( **i** ) _MoCap-based sensing_ , where **_o_** _t_ includes accurate object pose ( _e.g.,_ from motion capture); and ( **ii** ) _egocentric depth perception_ , where **_o_** _t_ includes an egocentric point cloud from a depth sensor ( _e.g.,_ headmounted), from which object state must be inferred. 

## _B. Preliminaries_ 

Since the controller may rely on partial onboard sensing, we model loco-manipulation as a goal-conditioned _Partially Observable Markov Decision Process_ (POMDP). Let **_s_** _t ∈ S_ be the underlying system state (humanoid and scene, including the object), with dynamics **_s_** _t_ +1 _∼T_ ( **_s_** _t,_ **_a_** _t_ ). The policy acts from **_o_** _t_ = Ω( **_s_** _t_ ) and conditioning **_c_** _t_ , producing **_a_** _t ∈A_ . We optimize _π_ ( **_a_** _t |_ **_o_** _t,_ **_c_** _t_ ) to maximize expected discounted return: max _π_ E�� _t≥_ 0<sup>_γt r_(</sup><sup>**_s_**</sup><sup>_t,_</sup><sup>**_a_**</sup><sup>_t,_</sup><sup>**_c_**</sup><sup>_t_)</sup> � _._ The following sections describe how we use PPO [35] and imitation to learn policies, including the observation/reward design and key techniques for our tasks. 

As shown in Fig. 2, ULTRA follows a four-stage training paradigm that couples physics-driven motion retargeting with teacher-student learning. In Stage 1, we learn a _retargeting policy_ that maps human MoCap motions to physically feasible humanoid loco-manipulation rollouts. In Stage 2, we train a privileged _teacher policy_ , leveraging full state and dense reference trajectories from the retargeted rollouts. In Stage 3, we distill the teacher into a _multimodal student_ that operates under perception and sparse goal specifications. Finally, we deploy the student with a separated control mode. 

## _A. General Motion Tracking for Neural Retargeting_ 

Given a human-object demonstration represented by an SMPL-X [36] motion sequence and an object pose trajectory, our goal is to generate a physically feasible rollout on the target humanoid ( _e.g.,_ Unitree G1) that preserves the overall motion and intended interaction (Fig. 3). Traditional retargeting solves inverse kinematics under kinematic constraints. We instead cast retargeting as RL-based trajectory optimization: rewards encode tracking, while simulator transitions enforce kinematics, dynamics, and contacts. Following [3], this is well suited for contact-rich loco-manipulation, where contacts are hard to express as kinematic constraints. As preprocessing, we scale the human-object trajectory to match G1 and define a fixed correspondence from human key links to humanoid counterparts. We then train a _unified_ retargeting policy across all motions, producing physically consistent rollouts without per-motion optimization or retraining. Dense, full-body tracking is brittle under embodiment mismatch and becomes especially fragile during object interaction, where exact link-wise targets may be infeasible and contact often requires deliberate deviations. Our key insight is to combine ( **i** ) relaxed tracking that prioritizes end effectors critical for loco-manipulation with ( **ii** ) interaction and contact rewards that correct mismatch-induced errors. 

**Reward.** We define _r_ track = _rp · rr · r_ obj _· r_ int _· r_ ct _· r_ eng _,_ with all terms computed in a heading-aligned humanoid frame. Let _F_ include only feet and palms. _rp_ tracks endeffector positions as sparse anchors; _rr_ matches normalized link directions over a fixed key edge set; and _r_ eng regularizes joint effort and foot placement. To reduce ambiguity, _r_ obj tracks object pose/velocities and _r_ int matches palm-to-surface offsets over sampled object points. We also align contact events by mapping contacts on human links to corresponding humanoid links, yielding _r_ ct. 

**Observation.** The policy uses a privileged, reference-aware observation containing simulator state and its deviation from the SMPL-X reference. Since preprocessing establishes a fixed correspondence after scaling/alignment, residuals are well-defined: **_o_** _t_ = � **_o_**<sup>sim</sup> _t_<sup>_,_</sup><sup>**_o_**ref</sup> _t_<sup>_,_</sup><sup>**_o_**∆</sup> _t_ � _._ **_o_**<sup>sim</sup> _t_ includes proprioception and contact signals; **_o_**<sup>ref</sup> _t_ provides selected correspondence-defined reference quantities (including object state); and **_o_**<sup>∆</sup> _t_ encodes heading-aligned simulationreference differences. All quantities are expressed in a heading-aligned frame to remove global yaw. 


Fig. 2: ULTRA follows four stages: ( **i** ) **Neural Retargeting:** an RL policy converts MoCap data into physically feasible G1 rollouts with augmentation; ( **ii** ) **Tracking:** a privileged teacher tracks these rollouts using full state and references; ( **iii** ) **Distillation:** we distill the teacher into a multimodal student for realistic sensing and sparse goals, with additional RL finetuning; ( **iv** ) **Deployment:** the student runs under real sensing, supporting depth input or MoCap-based state estimation. 

**State initialization and early termination.** Because we cannot reliably initialize the humanoid from an SMPL-X pose, we do not use reference-state initialization [37]. Each episode starts from a default standing pose, initially tracking the first reference frame to stabilize the humanoid before transitioning to full tracking with smoothly varying weights. We terminate on falls, excessive deviation, or contact mismatch for 20 frames [3] to improve sample efficiency. **Simplified actuation.** Since retargeting is used only to _generate reference rollouts_ , we prioritize motion quality and throughput over hardware-faithful control. We use an _idealized_ low-level controller in simulation, _e.g._ , with control frequency equal to simulation frequency, enabling stronger, more responsive tracking than onboard PD control. We train without domain randomization or perturbations, and address robustness later in Sec. IV-B. 

**Trajectory and object augmentation.** RL-based retargeting also enables _flexible augmentation_ (Fig. 4). Since preprocessing already scales positions, we can ( **i** ) apply anisotropic scaling along coordinate axes and ( **ii** ) scale the manipulated object with different coefficients, while interaction/contact rewards correct imperfections and the simulator enforces physical feasibility. Crucially, these augmentations are handled by a _single retargeting policy without retraining_ . 

## _B. Dense Motion Tracking for Teacher Policy_ 

Sec. IV-A converts human-object demonstrations into physically feasible G1 rollouts. For downstream imitation, 

we train a separate privileged teacher _π_ teacher to track these rollouts. The teacher uses the deployment control interface and actuation limits, but trains with privileged state and dense reference residuals to accelerate learning. We randomize physics and inject perturbations to broaden state visitation and teach recovery, producing stable behaviors that provide high-quality supervision for the student. 

**Observation.** The teacher uses the same reference-aware observation as retargeting, but does not require crossembodiment correspondence since the reference is already in the humanoid embodiment. 

**Dense tracking objective.** The teacher uses the same reward template, but replaces sparse anchoring with _full_ link tracking, together with object, interaction, and contact reward. **Reference initialization and robustness training.** We initialize from randomly sampled reference frames and include occasional stand still episodes that track standing references, reflecting deployment from a stable standing pose. To improve robustness, we randomize humanoid/object physical properties and inject perturbations, with a short grace period to allow recovery. We use the same early-termination criteria as retargeting and add no observation noise at this stage. 

## _C. Multimodal Student Policy_ 

We distill the privileged teacher into a multimodal student policy _π_ student. Unlike the teacher, the student observes only partial state and conditions on whatever modalities are available at test time via an availability mask randomly sampled 

during training. This retains teacher behavior as a prior while enabling goal-reaching under missing observations. **Multimodal observation with availability mask.** The student consumes heterogeneous inputs: **_o_**<sup>student</sup> _t_ = � **_o_**<sup>proprio</sup> _t ,_ **_o_**<sup>goal</sup> _t ,_ **_o_**<sup>object</sup> _t ,_ **_o_**<sup>pcd</sup> _t_<sup>_,_</sup> **_m_** _t_ � _._ **_o_**<sup>proprio</sup> _t_ contains proprioception ( _e.g.,_ joint states, IMU), **_o_**<sup>object</sup> _t_ provides object state ( _e.g.,_ MoCap), and **_o_**<sup>pcd</sup> _t_ is an egocentric point cloud ( _e.g.,_ egocentric camera). **_o_**<sup>goal</sup> _t_ encodes task objectives and commands, including ( **i** ) long-horizon object transforms, ( **ii** ) long-horizon humanoid root transforms, and ( **iii** ) next-frame humanoid local state changes for tracking. We also include discretized commands ( _e.g_ ., stand still) for deployment. **_m_** _t_ indicates which modalities are present. **Distillation.** We collect data with a DAgger-style loop [38]: we roll out with the teacher initially, gradually shift to the student, and query the teacher on visited states to obtain **_a_**<sup>teacher</sup> _t_ . During training, an encoder _qϕ_ ( **_z_** _t_<sup>res</sup> _|_ **_o_**<sup>student</sup> _t ,_ **_o_**<sup>teacher</sup> _t_ ) infers a latent residual [6] using privileged teacher inputs, while a prior _pθ_ ( **_z_**<sup>prior</sup> _t | m_ ( **_o_**<sup>student</sup> _t_ )) predicts a latent from masked student observations ( _m_ ( _·_ ) applies **_m_** _t_ ). We combine them as **_z_** _t_ = **_z_**<sup>prior</sup> _t_ + **_z_**<sup>res</sup> _t_ and sample actions **_a_**<sup>student</sup> _t ∼ π_ student( **_a_** _t |_ **_o_**<sup>student</sup> _t ,_ **_z_** _t_ ). We implement _π_ student with a transformer-based encoder [39] that projects each modality into shared tokens; **_m_** _t_ gates tokens and modulates crossmodal attention to ignore missing inputs. At deployment, we sample **_z_** _t_ from the prior only. **Training objective.** We match teacher actions while aligning the prior with the privileged posterior: 


_L_ aux uses reconstruction heads (recovering masked modalities) to encourage **_z_** _t_ to retain task-relevant information. **Curriculum learning.** Beyond DAgger, we use two curricula to keep the prior effective under partial observability: we progressively increase modality-masking probability, and anneal _λ_ KL and auxiliary weights to avoid posterior collapse while preserving latent skill diversity. 

**Shortcut for tracking.** For local-goal tracking, behavior is largely deterministic, so a stochastic latent helps less. We add a residual shortcut (with the mask) from the full-body goal directly to the decoder, preserving low-level reference information and stabilizing decoding (Fig. 2). 

**RL finetuning.** We perform RL finetuning on top of the distilled student by switching a subset of parallel environments to a goal-reaching objective while continuing distillation updates. Following [7], we partition simulators into ( **i** ) distillation environments replaying reference motions with imitation losses, and ( **ii** ) RL environments optimizing task success under state/goal perturbations. We sample random offsets for the object goal, humanoid root goal, and their initializations, and inject simulated point-cloud noise (jitter, dropout, occlusion) for alleviating sim-to-real gap. 

**Deployment versatility.** At test time, the student receives only **_o_**<sup>student</sup> _t_ and samples **_z_** _t_ from the prior. With the same parameters, modality masking enables: ( **i** ) high-fidelity track- 


Fig. 3: Qualitative comparison of our retargeting and OmniRetarget [2] at the same frame/sequence. **Top:** final frame; the baseline shows undesired standing foot placement. **Bottom:** a contact frame; ours yields more stable contacts. 

ing by unmasking local reference (Fig. 1 **Top** ), ( **ii** ) goalconditioned control by masking local reference and unmasking long-horizon goals (Fig. 1 **Middle** ), and ( **iii** ) visionbased manipulation by masking MoCap object state while unmasking point clouds (Fig. 1 **Bottom** ). 

V. EXPERIMENTAL RESULTS 

We evaluate ULTRA end-to-end for autonomous wholebody loco-manipulation, from data generation to real-world transfer. We ask: ( **i** ) Can we retarget human-object MoCap into physically consistent rollouts with stable contacts and minimal sliding/penetration? ( **ii** ) Under dense references, can the student match a privileged teacher and specialized trackers? ( **iii** ) Under sparse goals, does RL finetuning improve robustness and yield a semantically organized latent skill space? ( **iv** ) Can one policy transfer to a real humanoid without test-time references? We evaluate four axes: retargeting, tracking, goal execution, and real deployment on Unitree G1. 

## _A. Experimental Setup_ 

**Simulation.** We train in IsaacGym [40] with GPU-parallel environments and validate key results in MuJoCo [41]. Real trials use a physical Unitree G1 [42]. 

**Dataset.** We use OMOMO [43] human-object MoCap, with the corrected subset from [3] for a fair comparison with [2]. We focus on four box-like objects compatible with rigid hands. We retarget all sequences with our RL-based strategy (Sec. IV-A) and augment via anisotropic trajectory scaling and object resizing, yielding a _∼_ 6 _×_ larger corpus (Fig. 4). We adopt the same train/test split for **ID** evaluation and define **OOD** by held-out motions and novel object scales. 

## _B. Motion Retargeting_ 

**Baselines.** We compare against: ( **i** ) PHC [4] (human-only), ( **ii** ) GMR [5] (human-only), and ( **iii** ) OmniRetarget [2] (human-object interaction). All retarget from the same OMOMO subset processed by [3]. 

**Metrics.** We measure: ( **i** ) _penetration_ (duration, max depth) between humanoid/object/environment [2]; ( **ii** ) _foot skating_ (sliding duration, max tangential stance velocity), with stance defined geometrically (foot within 2 cm of ground) to avoid 

TABLE I: Motion-tracking evaluation in IsaacGym. All methods are trained/evaluated on our data unless noted. **Green** highlights our primary tracking controller. 

||**In-Distribution (ID)**||**Out-of-Distribution (OOD)**||
|---|---|---|---|---|
|Succ_↑_<br>Succ_↑_|Humanoid<br>O|bject<br>Succ_↑_|Succ_↑_<br>Humanoid|Object|
|**Method**<br>(Humanoid)<br>(+Object|)<br>_E_g-mpjpe _↓_<br>_E_mpjpe _↓_<br>_E_jitter _↓_<br>_E_pos _↓_|_E_rot _↓_<br>(Humanoid)|(+Object)<br>_E_g-mpjpe _↓_<br>_E_mpjpe _↓_<br>_E_jitter _↓_|_E_pos _↓_<br>_E_rot _↓_|
||**(a) Unified M**<br><br><br>|**ultimodal Controller**<br>|||
|ULTRA (**Ours**)<br>67.30_±_0.12 57.44_±_0.4|0 13.49_±_0.14<br>5.89_±_0.02<br>6.27_±_0.00 53.42_±_0.2|1 65.44_±_0.37 70.57_±_0.54|52.00_±_0.44 35.55_±_0.23 14.67_±_0.08<br>6.81_±_0.01|56.52_±_0.35 67.60_±_0.58|
||**(b) Privi**|**leged Teacher**|||
|_ULTRA Teacher_<br>_97.57±0.05_<br>_89.79±0.1_|_1_<br>_12.98±0.30_<br>_5.64±0.05_<br>_14.81±0.08_<br>_17.15±0.0_|_3_<br>_23.28±0.33_<br>_97.12±0.43_|_81.33±0.78_<br>_19.14±0.48_<br>_7.94±0.11_<br>_15.91±0.08_|_25.57±0.28_<br>_33.49±0.37_|
||**(c) General **|**Motion Tracking**|||
|ULTRA (RL)<br>54.47_±_0.43 41.78_±_0.3<br>ULTRA (Distillation)<br>**85.03**_±_**3.00**<br>**77.15**_±_**0.5**|1 49.30_±_0.32 16.23_±_0.11 20.04_±_0.15 47.48_±_0.3<br>**7**<br>**15.45**_±_**0.08**<br>**6.84**_±_**0.04**<br>**8.12**_±_**0.01**<br>**25.48**_±_**0.4**|1 60.53_±_0.09 53.38_±_0.98 <br>**8**<br>**33.97**_±_**0.58**<br>**86.63**_±_**0.50**|23.54_±_0.24 68.11_±_0.26 22.22_±_0.01 17.46_±_0.09 <br>**52.74**_±_**0.04**<br>**35.01**_±_**0.31**<br>**13.48**_±_**0.10**<br>**9.35**_±_**0.01**|66.17_±_0.54 59.44_±_0.73<br>**36.18**_±_**0.30**<br>**38.18**_±_**0.29**|
|HDMI [1]<br>13.07_±_0.20<br>9.94_±_0.3<br>OmniRetarget<sup>_†_ </sup>[2]<br>41.27_±_1.17 21.90_±_0.2<br>OmniRetarget [2]<br>51.34_±_0.67 20.91_±_0.5|8 92.77_±_0.56 26.90_±_0.10 26.13_±_0.60 78.93_±_0.4<br>9 62.96_±_1.43 15.37_±_0.17 39.35_±_0.57 77.94_±_3.5<br>2 67.12_±_0.86<br>7.43_±_0.07 39.92_±_1.44 60.67_±_0.5|2 70.23_±_0.62 13.92_±_0.78 <br>2 66.47_±_1.15 33.36_±_0.39 <br>4 67.03_±_0.19 46.71_±_0.74|12.95_±_0.30 87.07_±_0.44 27.54_±_0.06 29.19_±_0.38 <br> 20.78_±_0.13 74.80_±_0.34 16.23_±_0.15 49.52_±_0.52 <br> 25.82_±_0.52 68.34_±_0.82<br>8.98_±_0.19 40.08_±_1.77|77.33_±_2.27 71.16_±_0.48<br> 55.11_±_2.32 62.44_±_0.77<br> 58.57_±_2.37 66.70_±_0.84|
|_†_ Trained/evaluated on original OmniRetarget|dataset.||||
|||w/o finetuning|||
|||w/ finetuning|||
|Motion Augmentation|Object Augmentation|Fig. 6: Sim-to-<br>Blue/green: p<br>goal. **Top:** wit<br>OmniRetarget <br>HDMI1d|sim comparison for egocentric<br>oint cloud without/with noise;<br>hout finetuning. **Bottom:** with<br> retrained on our augmented<br>diWl|goal following<br> yellow: objec<br> finetuning.<br> set, and (**iii**<br>ULTR|


Fig. 6: Sim-to-sim comparison for egocentric goal following. Blue/green: point cloud without/with noise; yellow: object goal. **Top:** without finetuning. **Bottom:** with finetuning. 

OmniRetarget retrained on our augmented set, and ( **iii** ) HDMI [1] adapted to our setting. We also report ULTRA ablations: ( **i** ) direct RL under student observations (tracking only), ( **ii** ) tracking-only distillation, and ( **iii** ) all-task unified training. The privileged teacher is an upper bound. **Metrics.** We report success (Succ): no fall and per-frame _E_ g-mpjpe _<_ 0 _._ 3 m and _E_ pos _<_ 0 _._ 3 m; we also report humanoid-only success. Tracking errors include _E_ g-mpjpe, _E_ mpjpe, _E_ jitter, and object errors _E_ pos, _E_ rot. 

Fig. 4: Zero-shot augmentation with the retargeting policy. **Left:** trajectory scaling. **Right:** object scaling. Motions remain plausible, enabling scalable data augmentation. 

noisy MoCap stance labels; and ( **iii** ) _contact floating_ , the duration of lost hand-object contact during transport, detected via MuJoCo contact queries. 

**Quantitative evaluation.** Table II shows ULTRA outperforms baselines across nearly all metrics/categories: lowest foot-skating duration/velocity and much less contact floating (near-zero on Largebox/Suitcase), while also reducing penetration. We attribute this to physics-aware retargeting that enforces contact/dynamics, keeping stance feet planted and preserving hand-object contact when lifting. **Qualitative evaluation.** Fig. 3 shows more accurate hand/foot placement than OmniRetarget, whose kinematic formulation often breaks contact consistency and yields unnatural configurations relative to the object and ground. **Effectiveness of data augmentation.** Our augmentation diversifies motions without retraining the retargeter and applies along the full trajectory (not only the initial frame), producing temporally consistent variations (Fig. 4). This improves downstream generalization: in Table I, OmniRetarget retrained on our augmented data attains substantially higher OOD tracking success than when trained on its original dataset, confirming broader state/skill coverage. 

**Results.** Table I shows ULTRA strongly outperforms baselines for humanoid-object tracking, especially under OOD motions/object scales. HDMI often becomes unstable at our scale and fails to converge. OmniRetarget trains smoothly but frequently fails manipulation: humanoid success is reasonable, but drops when object tracking is required, likely due to missing explicit object observations and a defaultto-locomotion failure mode. ULTRA closes this gap via a privileged teacher with object/contact signals and distillation that preserves closed-loop tracking under partial observability. The residual teacher-student gap (97.57% vs. 67.30% ID) reflects this unification rather than under-fitting, as a tracking-only student already reaches 85.03%. 

**Distillation vs. direct RL.** Direct RL under partial observations must learn stabilization and sustained contact jointly, so early failures dominate and training can collapse. Distillation transfers contact-aware corrections learned with privileged state and dense references, yielding higher success. 

## _D. Goal-Conditioned Following_ 

## _C. General Motion Tracking_ 

**Metric.** Success (Succ): no fall and terminal state within 0 _._ 3 m of the goal. 

**Baselines.** We evaluate dense tracking (full reference provided) against: ( **i** ) OmniRetarget<sup>_†_</sup> (original data), ( **ii** ) 


TABLE II: Physical interaction quality for retargeting. Ours is better. 

|**Method**|**Pene**|**tration**|**Foot **|**Skating**|**Contact Floating**|
|---|---|---|---|---|---|
||Duration _↓_|Max Depth (cm) _↓_|Duration _↓_|Max Vel. (cm/s) _↓_|Duration _↓_|
|**Largebox**||||||
|PHC [4]|0.908 _±_ 0.125|0.073 _±_ 0.048|0.303 _±_ 0.145|0.032 _±_ 0.022|0.025 _±_ 0.054|
|GMR [5]|0.522 _±_ 0.259|0.086 _±_ 0.053|0.366 _±_ 0.317|0.029 _±_ 0.020|0.111 _±_ 0.171|
|OmniRetarget [2]|**0.000** _±_ **0.002**|0.013 _±_ 0.002|0.205 _±_ 0.106|0.035 _±_ 0.019|0.231 _±_ 0.224|
|ULTRA (**Ours**)|0.008 _±_ 0.030|**0.012** _±_ **0.002**|**0.061** _±_ **0.031**|**0.018** _±_ **0.010**|**0.015** _±_ **0.063**|
|**Suitcase**||||||
|PHC [4]|0.914 _±_ 0.119|0.077 _±_ 0.051|0.286 _±_ 0.147|0.035 _±_ 0.024|0.032 _±_ 0.065|
|GMR [5]|0.571 _±_ 0.265|0.105 _±_ 0.050|0.399 _±_ 0.368|0.028 _±_ 0.018|0.142 _±_ 0.175|
|OmniRetarget [2]|0.003 _±_ 0.016|**0.012** _±_ **0.002**|0.264 _±_ 0.141|0.040 _±_ 0.021|0.404 _±_ 0.279|
|ULTRA (**Ours**)|**0.002** _±_ **0.013**|0.017 _±_ 0.019|**0.062** _±_ **0.045**|**0.017** _±_ **0.008**|**0.008** _±_ **0.040**|


Fig. 5: **Left:** embeddings under different modalities; aside from tracking, embeddings largely mix, indicating a shared latent space. **Right:** latents cluster by text labels (C0–C4), showing semantic structure. 

TABLE III: Sim-to-sim success rate on Mujoco across goal types with in-distributional (ID) goals from training and out-of-distribution (OOD) goals with random offsets, and across perception with egocentric point clouds or object position with no shape. Policies are trained in IsaacGym and evaluated in MuJoCo with 20 selected motion per setting. 

**Comparisons.** Tracking-only baselines ( _e.g.,_ HDMI [1], OmniRetarget [2]) require dense references and are inapplicable; we compare ULTRA to ablations. 

**Tasks.** We test two perception regimes: ( **i** ) _MoCap_ object pose and ( **ii** ) _egocentric vision_ from a noisy depth point cloud. In both, we provide only long-horizon object target. **RL finetuning expands OOD coverage.** Table III and Fig. 6 show finetuning yields modest ID gains but large OOD gains under random goal offsets (nearly doubling under point clouds and tripling under position-only). This suggests finetuning expands interaction-state coverage and reinforces closed-loop recovery beyond the demonstration manifold. **Latent structure.** Fig. 5 shows the latent separates tracking vs. goal following across modalities while remaining on a shared manifold. Tracking stays distinct because we bypass the stochastic latent via a residual shortcut when local tracking goals are provided (Sec. IV-C), leaving the latent to capture multimodality under sparse goals. The latent also aligns with text-derived semantic clusters (MiniLM [44] + K- Means), indicating organization by control regime and intent. 

|**RL finetuning**|**ID **|**Goals**|**OOD**|**Goals**|
|---|---|---|---|---|
||**Points**|**Position**|**Points**|**Position**|
|✗|16 / 20|14 / 20|5 / 20|4 / 20|
|✓|19 / 20|16 / 20|**9 / 20**|**12 / 20**|
|∆(RL gain)|+18.8%|+14.3%|**+80.0%**|**+200.0%**|


TABLE IV: Real-world success rates on the OMOMO subset using a Unitree G1 humanoid. Each task is evaluated over two trials. MoCap provides object pose tracking for nonegocentric control modes, while the egocentric setting relies only on onboard sensing. MoCap is used for success evaluation in all settings. Dense reference tracking is directionagnostic and thus reported as a single success rate. 

|**Setting**|**Vertical**|**Lat**|**eral**|
|---|---|---|---|
|Dense Reference Tracking|**73%**|(19/26)||
|Sparse Goal Following (MoCap)|**80%** (8/10)|**90%**|(9/10)|
|Sparse Goal Following (Egocentric)|**50%** (5/10)|**60%**|(6/10)|


## _E. Real-World Deployment_ 

**Tasks.** We deploy ULTRA on a physical Unitree G1. The student runs onboard at the control frequency with proprioception and, when available, OptiTrack object pose. For dense tracking, we test OMOMO subsets (bimanual box lift/carry, suitcase transport) with household objects. For goal-conditioned control, we provide no motion references and specify future object transforms via keyboard commands. Beyond picking, our real-robot evaluation also covers locomotion with other contact pattern, including kicking boxes. **Point cloud extraction.** For egocentric perception, we extract object point clouds from depth only: back-project depth pixels using calibrated intrinsics, crop a forward ROI, remove the ground plane, take the dominant cluster as the box, and downsample to a fixed size for policy input. 

## VI. CONCLUSION 

ULTRA is a unified framework for practical humanoid whole-body loco-manipulation that moves beyond reference replay toward perception- and goal-driven autonomy. It combines an RL-formulated, physics-driven retargeting policy that scales human-object MoCap into physically consistent humanoid rollouts with a distilled multimodal controller that unifies dense tracking and sparse goal specification. Experiments show improved interaction fidelity from retargeting, a student that matches tracking performance while remaining robust under distribution shift, and RL finetuning that boosts success on out-of-distribution goals. We further validate simto-real transfer on Unitree G1, demonstrating reliable dense tracking and sparse goal following. Overall, ULTRA points to a scalable path for versatile loco-manipulation that adapts online from realistic sensing without test-time references. **Limitations.** Future work may extend our approach to dexterous hands for interacting with non-box-shaped objects and enable more dynamic locomotion, and incorporate pretrained perception models instead of training them from scratch. 

**Quantitative evaluation.** Table IV reports success rates: the policy reliably grasps/transports on hardware and achieves reasonable sparse-goal success under out-of-distribution operator commands, including composed motions. 

**Failure analysis.** Failures mainly arise from ( **i** ) friction gaps causing occasional grasp slip, ( **ii** ) depth noise/occlusion breaking point-cloud extraction, and ( **iii** ) disturbances beyond the recovery margin learned with domain randomization, motivating future tactile integration. 

**Acknowledgments.** This work was supported in part by NSF Grants 2106825 and 2519216, the DARPA Young Faculty Award, ONR Grant N00014-26-1-2099, NIFA Award 2020-67021-32799, Toyota Research Institute, and Amazon. This work used computational resources provided through the ACCESS program and the NAIRR Pilot. We thank the Coordinated Science Laboratory and the Center for Autonomy for access to the experimental space and the G1 humanoid robot, and John M. Hart for his assistance with the robot. 

## REFERENCES 

- [1] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi, “HDMI: Learning interactive humanoid whole-body control from human videos,” _arXiv preprint arXiv:2509.16757_ , 2025. 2, 3, 6, 7 

- [2] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “OmniRetarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” in _ICRA_ , 2026. 2, 3, 5, 6, 7 

- [3] S. Xu, H. Y. Ling, Y.-X. Wang, and L.-Y. Gui, “InterMimic: Towards universal whole-body control for physics-based human-object interactions,” in _CVPR_ , 2025. 2, 3, 4, 5 

- [4] Z. Luo, J. Cao, K. Kitani, W. Xu, _et al._ , “Perpetual humanoid control for real-time simulated avatars,” in _ICCV_ , 2023. 2, 5, 7 

- [5] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” in _ICRA_ , 2026. 2, 5, 7 

- [6] C. Tessler, Y. Guo, O. Nabati, G. Chechik, and X. B. Peng, “MaskedMimic: Unified physics-based character control through masked motion inpainting,” _ACM Trans. Graph._ , 2024. 2, 5 

- [7] S. Xu, S. Schulter, M. Ziyadi, X. He, X. Fei, Y.-X. Wang, and L.-Y. Gui, “InterPrior: Scaling generative control for physics-based humanobject interactions,” in _CVPR_ , 2026. 2, 5 

- [8] J. Lee and S. Y. Shin, “A hierarchical approach to interactive motion editing for human-like figures,” in _SIGGRAPH_ , 1999. 2 

- [9] R. Villegas, J. Yang, D. Ceylan, and H. Lee, “Neural kinematic networks for unsupervised motion retargetting,” in _CVPR_ , 2018. 2 

- [10] S. Park, H. Bharadhwaj, and S. Tulsiani, “DemoDiffusion: One-shot human imitation using pre-trained diffusion policy,” _arXiv preprint arXiv:2506.20668_ , 2025. 2 

- [11] S. Xu, Y.-W. Chao, L. Bian, A. Mousavian, Y.-X. Wang, L.-Y. Gui, and W. Yang, “DexPlore: Scalable neural control for dexterous manipulation from reference-scoped exploration,” in _CoRL_ , 2025. 2 

- [12] C. Pan, C. Wang, H. Qi, Z. Liu, H. Bharadhwaj, A. Sharma, T. Wu, G. Shi, J. Malik, and F. Hogan, “SPIDER: Scalable physics-informed dexterous retargeting,” _arXiv preprint arXiv:2511.09484_ , 2025. 2 

- [13] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “OmniH2O: Universal and dexterous human-to-humanoid whole-body teleoperation and learning,” in _CoRL_ , 2024. 2 

- [14] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “ExBody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 2 

- [15] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, _et al._ , “ASAP: Aligning simulation and realworld physics for learning agile humanoid whole-body skills,” in _RSS_ , 2025. 2 

- [16] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, _et al._ , “HOVER: Versatile neural whole-body controller for humanoid robots,” in _ICRA_ , 2025. 2 

- [17] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu, “VisualMimic: Visual humanoid loco-manipulation via motion tracking and generation,” _arXiv preprint arXiv:2509.20322_ , 2025. 2, 3 

- [18] Y. Ze, Z. Chen, J. P. Ara´ujo, Z.-a. Cao, X. B. Peng, J. Wu, and C. K. Liu, “TWIST: Teleoperated whole-body imitation system,” in _CoRL_ , 2025. 2 

- [19] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang, “GMT: General motion tracking for humanoid whole-body control,” _arXiv preprint arXiv:2506.14770_ , 2025. 2 

- [20] K. Yin, W. Zeng, K. Fan, M. Dai, Z. Wang, Q. Zhang, Z. Tian, J. Wang, J. Pang, and W. Zhang, “UniTracker: Learning universal whole-body motion tracker for humanoid robots,” _RAL_ , 2026. 2 

- [21] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Casta˜neda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, _et al._ , “SONIC: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 2 

- [22] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “BeyondMimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 2 

- [23] W. Zeng, S. Lu, K. Yin, X. Niu, M. Dai, J. Wang, and J. Pang, “Behavior foundation model for humanoid robots,” _arXiv preprint arXiv:2509.13780_ , 2025. 2 

- [24] H. Xue, X. Huang, D. Niu, Q. Liao, T. Kragerud, J. T. Gravdahl, X. B. Peng, G. Shi, T. Darrell, K. Sreenath, _et al._ , “LeVERB: Humanoid whole-body control with latent vision-language instruction,” _arXiv preprint arXiv:2506.13751_ , 2025. 2 

- [25] L. Ma, Z. Meng, T. Liu, Y. Li, R. Song, W. Zhang, and S. Huang, “StyleLoco: Generative adversarial distillation for natural humanoid robot locomotion,” _arXiv preprint arXiv:2503.15082_ , 2025. 2 

- [26] J. Shi, X. Liu, D. Wang, O. Lu, S. Schwertfeger, C. Zhang, F. Sun, C. Bai, and X. Li, “Adversarial locomotion and motion imitation for humanoid policy learning,” in _NeurIPS_ , 2025. 2 

- [27] Y. Li, Z. Luo, T. Zhang, C. Dai, A. Kanervisto, A. Tirinzoni, H. Weng, K. Kitani, M. Guzek, A. Touati, _et al._ , “BFM-Zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning,” in _ICLR_ , 2026. 2 

- [28] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “HOMIE: Humanoid loco-manipulation with isomorphic exoskeleton cockpit,” in _RSS_ , 2025. 2 

- [29] W. Sun, L. Feng, B. Cao, Y. Liu, Y. Jin, and Z. Xie, “ULC: A unified and fine-grained controller for humanoid loco-manipulation,” _arXiv preprint arXiv:2507.06905_ , 2025. 2 

- [30] J. Li, Y. Zhu, Y. Xie, Z. Jiang, M. Seo, G. Pavlakos, and Y. Zhu, “OKAMI: Teaching humanoid robots manipulation skills through single video imitation,” in _CoRL_ , 2024. 2 

- [31] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan, “ResMimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning,” _arXiv preprint arXiv:2510.05070_ , 2025. 3 

- [32] Y. Fu, F. Xie, C. Xu, J. Xiong, H. Yuan, and Z. Lu, “DemoHLM: From one demonstration to generalizable humanoid loco-manipulation,” _arXiv preprint arXiv:2510.11258_ , 2025. 3 

- [33] D. Kalaria, S. S. Harithas, P. Katara, S. Kwak, S. Bhagat, S. Sastry, S. Sridhar, S. Vemprala, A. Kapoor, and J. C.-K. Huang, “DreamControl: Human-inspired whole-body humanoid control for scene interaction via guided diffusion,” _arXiv preprint arXiv:2509.14353_ , 2025. 3 

- [34] H. Wang, W. Zhang, R. Yu, T. Huang, J. Ren, F. Jia, Z. Wang, X. Niu, X. Chen, J. Chen, _et al._ , “PhysHSI: Towards a real-world generalizable and natural humanoid-scene interaction system,” _arXiv preprint arXiv:2510.11072_ , 2025. 3 

- [35] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 3 

- [36] G. Pavlakos, V. Choutas, N. Ghorbani, T. Bolkart, A. A. A. Osman, D. Tzionas, and M. J. Black, “Expressive body capture: 3D hands, face, and body from a single image,” in _CVPR_ , 2019. 3 

- [37] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “DeepMimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Trans. Graph._ , 2018. 4 

- [38] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _AISTATS_ , 2011. 5 

- [39] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. u. Kaiser, and I. Polosukhin, “Attention is all you need,” in _NeurIPS_ , 2017. 5 

- [40] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, _et al._ , “Isaac Gym: High performance GPU-based physics simulation for robot learning,” in _NeurIPS_ , 2021. 5 

- [41] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _IROS_ , 2012. 5 

- [42] Unitree, “Unitree g1 humanoid agent ai avatar,” https://www.unitree. com/g1/. 5 

- [43] J. Li, J. Wu, and C. K. Liu, “Object motion guided human motion synthesis,” _ACM Trans. Graph._ , 2023. 5 

- [44] W. Wang, F. Wei, L. Dong, H. Bao, N. Yang, and M. Zhou, “MiniLM: Deep self-attention distillation for task-agnostic compression of pretrained transformers,” in _NeurIPS_ , 2020. 7 

APPENDIX 

In this appendix, we provide additional details of our ULTRA: 

- 1) Sec. A describes the organization of the supplementary demo video. 

- 2) Sec. B provides additional details on retargeting and the teacher policy, including the observation and reward design. 

- 3) Sec. C provides additional details on the student policy, covering both the distillation stage and the RL finetuning stage. 

- 4) Sec. D provides additional experimental details and setups for both simulation and real-world experiments. 

## CONTENTS 

- A Demo Videos . . . . . . . . . . . . . . . . . 9 B Additional Details on Retargeting and Teacher Policy . . . . . . . . . . . . . . . . 9 

- C Additional Details on Student Policy . . . . 9 D Additional Experimental Details. . . . . . . 11 

## _A. Demo Videos_ 

In our webpage, we highlight the following capabilities: ( **I** ) our retargeting pipeline learns a single policy from all data and performs zero-shot retargeting to unseen, rescaled trajectories and objects; ( **II** ) our teacher policy transfers reliably across simulators; ( **III** ) the all-in-one ULTRA model faithfully tracks reference motions for object interactions; ( **IV** ) ULTRA supports sparse object-goal commands and fine-grained, keyboard-based control, demonstrating strong generalization; and ( **V** ) ULTRA completes long-horizon, object-centric goals using only egocentric perception. 

## _B. Additional Details on Retargeting and Teacher Policy_ 

We provide additional details on retargeting and teacher policy training. Both follow the same general procedure. The key difference is that the retargeting policy tracks reference motions from a different embodiment, which requires a predefined keyjoint mapping when constructing rewards and observations. In this appendix, we focus on the teacher policy reward and observation; This can be easily extended to the retargeting policy, which uses the same formulations, with the additional cross-embodiment link alignment applied (Table A). 

**Rewards.** The teacher policy reward combines tracking terms with smoothness and regularization penalties to facilitate sim-to-real transfer for the distilled student policy. The total reward is defined as 


Table B lists all tracking reward terms, and Table C summarizes all smoothness and regularization terms. **Observation.** At time step _t_ , the teacher policy receives an observation vector 


where the four blocks correspond to simulated state, reference targets, simulation–reference residuals, and interaction-graph features, respectively. Table D details the observation components and variable definitions. 

**Architecture.** The teacher policy uses a three-layer MLP with hidden dimensions 1024, 1024, and 512, and ReLU activations. It follows a separate actor–critic design, producing a 29-dimensional action output. The action mean is output with no activation ( _i.e.,_ a linear head), while the action standard deviation is fixed rather than learned and is initialized to _−_ 2 _._ 9. All weights use the default Xavier initialization. 

**Training.** We summarize PPO hyperparameters in Table E. 

|**Unitree G1 Link**|**SMPL-X Index**|**SMPL-X Body Part**|
|---|---|---|
|left<br>~~h~~ip<br>~~y~~aw<br>~~l~~ink|1|Left hip|
|left<br>~~k~~nee<br>~~l~~ink|2|Left knee|
|left<br>~~a~~nkle<br>~~r~~oll<br>~~l~~ink|3|Left ankle|
|right<br>~~h~~ip<br>~~y~~aw<br>~~l~~ink|5|Right hip|
|right<br>~~k~~nee<br>~~l~~ink|6|Right knee|
|right<br>~~a~~nkle<br>~~r~~oll<br>~~l~~ink|7|Right ankle|
|torso<br>~~l~~ink|9|Pelvis / lower torso|
|mid360<br>~~l~~ink|13|Upper torso / spine|
|left<br>~~s~~houlder<br>~~y~~aw<br>~~l~~ink|15|Left shoulder|
|left<br>~~e~~lbow<br>~~l~~ink|16|Left elbow|
|left<br>~~w~~rist<br>~~y~~aw<br>~~l~~ink|17|Left wrist|
|right<br>~~s~~houlder<br>~~y~~aw<br>~~l~~ink|34|Right shoulder|
|right<br>~~e~~lbow<br>~~l~~ink|35|Right elbow|
|right<br>~~w~~rist<br>~~y~~aw<br>~~l~~ink|36|Right wrist|


TABLE A: Correspondence between Unitree G1 key links and SMPL-X body indices (52-body model) used for motion retargeting. 

TABLE B: **Tracking reward components for the teacher policy. p** _l,_ **q** _,_ **p** ˙ _l,_ **q** ˙ denote the simulated body joint positions, joint rotation, and their velocities; **p** ˆ _l,_ ˆ **q** _,_ **p**<sup>ˆ</sup> ˙ _l,_ **q**<sup>ˆ</sup> ˙ are the corresponding reference quantities. **p** _o,_ **q** _o,_ **p** ˙ _o_ denote the simulated object position, rotation (quaternion), and linear velocity; **p** ˆ _o,_ ˆ **q** _o,_ **p**<sup>ˆ</sup> ˙ _o_ are the corresponding references. ∠( **q** _o,_ ˆ **q** _o_ ) is the relative rotation angle and huber( _·_ ) is the Huber loss. **_δ_** _ij_ denotes the palm-to-surface distance between palm point _i_ and object surface sample _j_ , with weights _wij_ ; hats denote reference values. _cl ∈{_ 0 _,_ 1 _}_ is a binary contact indicator for link _l_ . The scalars _k·_ are temperature coefficients. All reward terms are multiplied together. 

|**Term**|**Expression**|**Weight**|
|---|---|---|
|_Body Tracking:_|||
|Joint position|exp<br>�<br>_−kp ·_mean(_∥_**p**_l −_ˆ**p**_l∥_<sup>2</sup><br>2<sup>)</sup><br>�<br><br><br>|_kp_ = 10_._0|
|Joint rotation|exp<br>�<br>_−kr ·_mean(_∥_**q**_−_ˆ**q**_∥_<sup>2</sup><br>2<sup>)</sup><br>�<br><br>|_kr_ = 5_._0|
|Body velocity|exp<br>�<br>_−kpv ·_mean(_∥_˙**p**_l −_<sup>ˆ</sup>˙**p**_l∥_<sup>2</sup><br>2<sup>)</sup><br>�<br><br>|_kpv_ = 0_._1|
|Joint velocity|exp<br>�<br>_−krv ·_mean(_∥_˙**q**_−_<sup>ˆ</sup>˙**q**_∥_<sup>2</sup><br>2<sup>)</sup><br>�|_krv_ = 0_._001|
|_Object Tracking:_|||
|Object position|exp<br>�<br>_−kop ·_mean(_∥_**p**_o −_ˆ**p**_o∥_<sup>2</sup><br>2<sup>)</sup><br>�|_kop_ = 5_._0|
|Object rotation|exp (_−kor ·_huber(∠(**q**_o,_ˆ**q**_o_)))<br><br>|_kor_ = 0_._5|
|Object linear velocity|exp<br>�<br>_−kopv ·_mean(_∥_˙**p**_o −_<sup>ˆ</sup>˙**p**_o∥_<sup>2</sup><br>2<sup>)</sup><br>�|_kopv_ = 0_._1|
|_Interaction:_|||
|Palm-to-surface|exp<br>�<br>_−k_int_·_ <sup>�</sup><br>_i,j _<sup>_wij∥_</sup><sup>**_δ_**</sup><sup>_ij −_ˆ</sup><sup>**_δ_**</sup><sup>_ij∥_2</sup><br>2<br>�|_k_int = 20_._0|
|Contact matching|exp (_−k_ct_·_mean(_|cl −_ˆ_cl|_))|_k_ct = 5_._0|


## _C. Additional Details on Student Policy_ 

**Student Policy Observation.** The student policy observation extends the student observation with multimodal inputs including object point clouds and goal phase information. The observation is structured as **_o_**<sup>student</sup> _t_ = [ **_o_**<sup>global</sup> _,_ **_o_**<sup>cmd</sup> _,_ **_o_**<sup>local</sup> _,_ **_o_**<sup>proprio</sup> _,_ **_o_**<sup>task</sup> _,_ **_m_** ]. We summarize all components in Table H. 

**Student Policy Architecture.** ULTRA enables learning a latent representation that captures task-relevant information while maintaining robustness to noise and missing modalities. 

Specifically, the student is a latent-variable policy with a 64dimensional latent _z_ and a modality-fusion transformer. Each input modality, as summarized in Table H, is first encoded into a 256dimensional token; point-cloud perception uses a PointNet over 64 

TABLE C: **Smoothness and regularization rewards for the teacher policy.** All terms are penalties with negative weights _wi <_ 0. **v** base and **_ω_** base are the base linear and angular velocities. **a** _t_ is the action at time _t_ ; **q** ˙ _t_ is the joint velocity at time _t_ ; and **_ω_** _t_ is the base angular velocity at time _t_ . **_τ_** denotes joint torques and _⊙_ is elementwise multiplication. **q** lim and **_τ_** lim are per-joint position and torque limits. 1contact is an indicator for foot contact; **f** _xy_ and **f** _z_ are the horizontal and vertical components of the contact force. _d_ feet and _d_ knee are the distances between the two feet and the two knees, and clamp( _·_ ) clips the distance to the specified interval. **g** _⊥_<sup>feet</sup> measures foot tilt relative to gravity. ref ~~s~~ tand and sim ~~s~~ tand indicate standing phases in the reference and simulation. _h_ term is a swing-foot height term, _c_ is a clearance/contactrelated term, and _g_ swing gates the swing penalty, which is active only during reference indicating swing. 

|**Term**<br>**Expression**|**Weight**|
|---|---|
|_Velocity Penalties:_<br>||
|Base linear velocity<br>_∥_**v**base_∥_2<br>|_−_0_._1|
|Base angular velocity<br>_∥_**_ω_**base_∥_<sup>2</sup><br>2<br>|_−_0_._01|
|Joint velocity<br>_∥_˙**q**_∥_<sup>2</sup><br>2|_−_0_._0004|
|_Smoothness Penalties:_||
|Action rate<br>_∥_**a**_t −_**a**_t−_1_∥_2<br>|_−_0_._1<br>|
|Joint velocity change<br>_∥_˙**q**_t −_˙**q**_t−_1_∥_<sup>2</sup><br>2<br>|_−_2_×_10<sup>_−_5</sup><br>|
|Angular velocity change<br>_∥_**_ω_**_t −_**_ω_**_t−_1_∥_<sup>2</sup><br>2|_−_5_×_10<sup>_−_4</sup>|
|_Torque & Energy Penalties:_||
|Torque magnitude<br>_∥_**_τ_**_∥_2|_−_0_._001|
|Energy consumption<br>_∥_**_τ_** _⊙_˙**q**_∥_2|_−_0_._0001|
|Joint position limits<br>�max(0_, |_**q**_| −_**q**lim)|_−_5_._0|
|Joint torque limits<br>�max(0_, |_**_τ_**_|/_**_τ_**lim_−_0_._95)|_−_1_._0|
|_Foot & Stability Penalties:_||
|Feet orientation<br>_∥_**g**<sup>feet</sup><br>_⊥_<sup>_∥_2</sup><br>|_−_0_._35|
|Foot slip<br>~~�~~<br>_∥_**v**foot_∥_2_·_1contact|_−_0_._1|
|Feet stumble<br>1(_∥_**f**_xy∥>_4_|_**f**_z|_)|_−_10_._0|
|Feet distance<br>clamp(_d_feet_−_[0_._25_,_0_._65])|_−_0_._1|
|Knee distance<br>clamp(_d_knee_−_[0_._25_,_0_._65])|_−_0_._1|
|Stand on feet<br>1(ref<br>~~s~~tand_∧¬_sim<br>~~s~~tand)|_−_1_._0|
|Swing clearance<br>(_wh · h_term+_wc · c_)_· g_swing|_−_0_._6|
|Termination<br>1terminated|_−_50_._0|


3D points that outputs a 256-dimensional feature via a point MLP and global pooling/statistics, while all other modalities are embedded with MLP encoders into the same token space. These modality tokens are fused by a lightweight transformer with token dimension 256, two layers, four attention heads, and a 1024-dimensional feedforward network, using GELU activations, sinusoidal positional encoding, and zero dropout. 

For the latent model, a prior network predicts the Gaussian parameters of _z_ from the transformer context token using two MLP heads, each mapping 256 to 128 to 64 with ReLU. During training, a privileged encoder takes the teacher observation together with additional observations and privileged signals, processes them with an MLP of widths 2048, 1024, 512, and 256, and outputs the posterior with the same 256 to 128 to 64 heads. An auxiliary latent decoder maps _z_ through a small MLP from 64 to 256 to 16 for reconstruction or regularization. Finally, _z_ conditions the policy via FiLM by predicting per-layer scale and shift parameters with a linear projection, and the FiLM modulation is scaled by 0.1. **Distillation Training.** ULTRA is first pretrained via a distillation loop that combines on-policy rollouts with teacher supervision. We apply a DAgger mixing schedule to transition from teacher-driven 

TABLE D: **Teacher policy observation space.** At time _t_ , **_o_** _t_ = [ **_o_**<sup>sim</sup> _t_<sup>_,_</sup><sup>**_o_**ref</sup> _t_<sup>_,_</sup><sup>**_o_**∆</sup> _t_<sup>_,_</sup><sup>**_o_**</sup> _t_<sup>ig].</sup><sup>**_o_**sim</sup> _t_ contains simulated quantities: root height; per-body local positions **p** , rotations **R** in 6D tan-norm, linear velocities **p** ˙ , angular velocities **_ω_** , contact flags _c ∈{_ 0 _,_ 1 _}_ ; and joint states (positions **q** , velocities **q** ˙ , actions **a** , torques **_τ_** , and history). **_o_**<sup>ref</sup> _t_ contains corresponding reference targets (hats), _e.g.,_ body pose (ˆ **p** _,_ **R**<sup>ˆ</sup> ) and object pose/velocity (ˆ **x** _o,_ ˆ **q** _o,_ ˆ **v** _o,_ ˆ **_ω_** _o_ ). **_o_**<sup>∆</sup> _t_<sup>stores residuals</sup> between simulation and reference ( _e.g.,_ **p** _−_ **p** ˆ and velocity errors), and **_o_**<sup>ig</sup> _t_<sup>storesinteraction-graphfeaturesbasedon</sup> SDF distances between body points and the object surface and their residuals. Two observations based on next 1-frame and next 16-frame reference are concatenated, yielding total dimension 4052. 

|**Category**|**Feature**<br>|**Dimension**|**Description**|
|---|---|---|---|
||Root height|1|Root height above ground|
||Local body positions **p**|114|39 bodies _×_ 3 (root removed)|
||Local body rotations **R**|234|39 bodies _×_ 6 (tan-norm)|
|**_o_**<sup>sim</sup>|Local body velocities ˙**p**|117|39 bodies _×_ 3|
||Local body angular vel. **_ω_**<br>Contact indicators _c_|117<br>39|39 bodies _×_ 3<br>Binary contact flags|
||Joint states (**q**_,_ ˙**q**_,_**a**_,_**_τ_**)|145|Proprioception + short history|
|**_o_**<sup>ref</sup>|Body reference (ˆ**p**_,_ <sup>ˆ</sup>**R**)<br>Object reference|351<br>13|Positions (117) + rotations (234)<br>Pose (ˆ**x**_o,_ˆ**q**_o_) (7) + vel. (ˆ**v**_o,_ ˆ**_ω_**_o_) (6)|
|**_o_**<sup>∆</sup>|Body residuals<br>Object residuals|585<br>21|Pose/velocity residuals vs. reference<br>Object pose/velocity residuals vs. reference|
|**_o_**<sup>ig</sup>|Interaction graph|234|39 _×_ 3 SDF distances + residuals|
|**Total**||4052|Concatenate 2 frames (current + future)|


TABLE E: PPO hyperparameters. 

|**Hyperparameter**|**Value**|
|---|---|
|Learning rate<br>|2_×_10<sup>_−_5</sup><br>|
|Clip ratio _ϵ_|0.2|
|GAE _λ_ (tau)|0.95|
|Discount _γ_|0.99|
|Horizon length|32|
|Mini-batch size|16384|
|Mini epochs per update|6|
|Entropy coefficient|0.0|
|Critic loss coefficient|5.0|
|Bounds loss coefficient|10.0|
|Max gradient norm|1.0|
|Number of parallel envs|4096|
|Normalize input|True|
|Normalize value|False|
|Normalize advantage|True|


rollouts to student-driven rollouts. Specifically, we use full teacher rollout below 500 epoch, then linearly anneal to over epochs 1500 epoch for full student rollout. We use 4096 parallel environments with horizon length 8, mini-batch size 4096, and 2 mini-epochs per update, which updates more frequently compared to PPO setup in Table E, given that supervised distillation is much more stable. The learning rate follows a warmup-and-decay schedule: it starts at 2 _×_ 10<sup>_−_4</sup> , ends warmup at epoch 500, and decays to 5 _×_ 10<sup>_−_5</sup> by epoch 5500. The latent dimension is 64. 

**Distillation Loss.** In the distillation stage, the optimization uses supervised and latent-regularization objectives. The PPO actor-critic terms are disabled in the provided implementation, so the total loss is a weighted sum of ( **I** ) expert supervision on the action mean, ( **II** ) KL alignment between the privileged posterior and the student prior, ( **III** ) a temporal smoothness penalty on the latent mean, ( **IV** ) auxiliary masked-prediction losses, and ( **V** ) a prior-only 

TABLE F: **Distillation-stage loss terms.** **_µ_** is the student action mean from the full model forward pass, and **_µ_**<sup>prior</sup> is the action mean from a prior-only forward pass (encoder disabled). **_a_**<sup>exp</sup> denotes the expert action mean (teacher target) used for supervision. The prior and privileged encoder output diagonal Gaussians over the latent _z_ , denoted by _pθ_ ( _z |_ **_o_** ) = _N_ ( **_µ_** _p,_ **_σ_**<sup>2</sup> _p_<sup>)</sup> and _qϕ_ ( _z |_ **_o_** _,_ **_o_**<sup>priv</sup> ) = _N_ ( **_µ_** _e,_ **_σ_** _e_<sup>2). Let ep be the epoch index and</sup><sup>_s_= clip</sup> <u>�</u> ep3000 _−_ 500<sup>_,_0</sup><sup>_,_1</sup> <u>�. The cosine ramp is</u> _g_ ( _s_ ) =<sup>1</sup><sup>_−_cos</sup> 2<sup><u>(</u></sup><sup>_πs_</sup><sup><u>)</u></sup> . 

|**Term**|**Definition**|**Weight / schedule**|
|---|---|---|
|Total loss<br>_L_|=_λELE_ +_λ_KL_L_KL+_λSLS_ +_λALA_+_λGLG_+_λP LP_|see below|
|Expert imitation|_LE_ =<br>��**_µ_**_−_**_a_**exp��2<br>2|_λE_ = 1_._0|
|Latent KL alignment|_L_KL =_D_KL(_qϕ_(_z_) _∥pθ_(_z_))|_λ_KL = 0_._001 + (0_._1_−_0_._001)_g_(_s_)|
|Latent smoothness|_LS_ =<br>���<br>**_µ_**_p_+**_µ_**_e_<br>�<br>_t _<sup>_−_</sup><br>�<br>**_µ_**_p_+**_µ_**_e_<br>�<br>_t−_1<br>��2<br>2|_λS_ = 0_._0001 + (0_._001_−_0_._0001)_g_(_s_)|
|Auxiliary prediction|_LA_ = MSE<br>�ˆ**_y_**aux_,_**_y_**aux<br>�<br>with mask-weighting|_λA_ = 1_._0|
|Local-goal prediction|_LG_ = MSE<br>�ˆ**_g_**local_,_**_g_**local<br>�<br>with mask-weighting|_λG_ = 1_._0|


TABLE G: **RL finetuning reward components** . We mask-gate goal-related terms: if a target is unobserved, we set its reward to zero and exclude it from success checks. 

|Term|Active when|Description|
|---|---|---|
|Goal-reaching<br>Progress|target visible<br>target visible|Reward proximity to the sampled goal (dense).<br>Reward step-to-step improvement toward the goal (clipped).|
|Terminal bonus|success on visible targets|Add a bonus when all visible thresholds are met.|
|Termination|always|Same as in Table C.|
|Smoothness|always|Mostly same as in Table C without reference related terms|


TABLE H: Student policy observation space. 

|**Category**|**Feature**<br>**D**|**imension**|**Description**|
|---|---|---|---|
|**_o_**<sup>global</sup>|Root position residual (xy)<br>Heading residual (yaw)|2<br>1|Horizontal position error<br>Yaw angle error|
|**_o_**<sup>cmd</sup>|End-of-episode flag<br>Approaching flag<br>Leaving flag<br>Time-to-go|1<br>1<br>1<br>1|Near episode end indicator<br>Moving toward object<br>Moving away from object<br>Normalized remaining time|
|**_o_**<sup>local</sup>|IMU residual (roll, pitch)<br>Joint position residual|2<br>29|Local orientation error<br>Joint angle error to local target|
||Root angular velocity<br>IMU (roll, pitch)|3<br>2|Base angular velocity<br>Current orientation|
|**_o_**<sup>proprio</sup>|Joint positions|29|Current joint angles|
||Joint velocities|29|Scaled by 0.05|
||Previous action|29|Last action command|
|**_o_**<sup>history</sup>|Proprioceptive history|920|92 dims _×_ 10 steps|
|_Object Obs_|_ervations:_|||
||Object position residual|3|Local frame position error|
|<sup>task</sup>|Object rotation residual|6|Tan-norm rotation error|
|**_o_**|Object position|3|Local frame position|
||Point cloud (PCA sampled)|192|64 points _×_ 3 in head frame|
|_Observatio_|_n Masks:_|||
|**_m_**|Global goal mask<br>Local goal mask<br>Object masks<br>Goal mask|3<br>31<br>204<br>4|Keep probability for global goal<br>Keep probability for local goal<br>Trans(3) + rot(6) + pos(3) + pcd(192)<br>Keep probability for command|
|**Total**||1496||


action matching loss computed from an additional forward pass that disables the privileged encoder. We set the expert loss coefficient, auxiliary loss coefficient, and local goal prediction coefficient to 1.0. To stabilize training and encourage a useful prior, the KL coefficient increases from 0.001 to 0.1 with a cosine schedule. More details are presented in Table F. 

**RL Finetuning Training.** We finetune the distilled student with PPO. Importantly, PPO is applied to the _deployable_ student policy, _i.e.,_ the prior-only policy that does not use privileged encoder inputs. And to keep the prior, we preserve 1 _/_ 4 of environment still for distillation update. The PPO objective follows the standard loss. To keep finetuning stable, we use a conservative update regime. First, we scale the overall PPO contribution by a small constant rel- 

TABLE I: Domain randomization ranges. 

|**Category**|**Parameter**|**Range**|
|---|---|---|
|Humanoid|Added base mass (kg)<br>CoM offset (m)<br>Motor strength scale|[_−_3_._0_,_3_._0]<br>[_−_0_._05_,_0_._05]<br>[0_._8_,_1_._2]|
|Environment|Ground friction<br>Gravity perturbation (m/s<sup>2</sup>)<br>Gravity randomization interval|[0_._5_,_2_._0]<br>[_−_0_._1_,_0_._1]<br>4 s|
|Perturbations|Max push velocity (m/s)<br>Push interval|1.0<br>4 s|
|Action|Action delay buffer length|8 steps|


ative to the distillation objectives. Second, we apply a short warmup schedule for the critic: the policy-gradient term is gradually enabled over an initial window of 100 training epochs, while the critic loss remains active throughout. This warm-up reduces abrupt distribution shift from the distilled policy and improves optimization stability in the early finetuning phase. 

**RL Finetuning Reward.** At each step, we define the total reward as the sum of a dense goal-reaching term, a progress term, and auxiliary regularizers: the dense term encourages matching the object and root goals via an exponentially decayed function of their current distances, while the progress term rewards step-tostep reduction in those distances, which is clipped to prevent large spikes; importantly, both goal-related terms are visibility-gated by binary masks so that if the object or root goal is hidden by the observation mask, the corresponding reward contribution is set to zero, and we add a terminal success bonus when all visible goal constraints fall below preset thresholds. More details are discussed in Table G. 

## _D. Additional Experimental Details._ 

**Simulation Configuration.** We summarize the simulation hyperparameters in Table M. 

TABLE J: Object domain randomization ranges. 

|**Parameter**|**Range**|
|---|---|
|Object mass (kg)|[0_._15_,_1_._5]|
|Object mass rare (kg)|[0_._05_,_0_._15] (every 10 episodes)|
|Object CoM offset (m)|[_−_0_._05_,_0_._05]|
|Object inertia scale|[0_._5_,_2_._0]|
|Object friction|[0_._2_,_1_._2]|
|Object restitution|[0_._0_,_0_._3]|
|Object rolling friction|[0_._0_,_0_._05]|
|Object torsion friction|[0_._0_,_0_._05]|


TABLE K: Point cloud domain randomization. 

|**Parameter**|**Value**|
|---|---|
|Gaussian noise std (m)|0.02|
|Point dropout probability|0.15|
|Outlier probability|0.05|
|Outlier max distance (m)|0.5|
|Depth noise scale|0.01|
|Density range|[0.5, 1.0]|
|Cluster noise std (m)|0.005|
|Scale range|[0.95, 1.05]|
|Translation noise (m)|0.02|
|Occlusion probability|0.1|
|Camera rotation noise (rad)|0.05|
|Camera position noise (m)|0.02|


TABLE L: Observation noise scales. 


Fig. A: ( **I** ) The _OptiTrack_ camera setup used to support ULTRA control in MoCap mode. ( **II** ) Markers attached to the humanoid root (front and back). 


Fig. B: We visualize the objects used in our real-world deployment. 

**Limitations.** Our method still has several limitations. It can fail under out-of-distribution conditions, such as severe point-cloud occlusion that removes critical geometric cues. In real-world experiments, MoCap-driven control is sensitive to marker occlusions, which can introduce jitter and drift in the estimated object pose and cascade into unstable tracking. Performance can also degrade when a human operator specifies overly aggressive or inconsistent goals ( _e.g._ , large, discontinuous target jumps or goals that are physically infeasible given the current contacts). 

|**Observation**|**Noise Scale**|
|---|---|
|Joint positions (rad)|0.01|
|Joint velocities (rad/s)|0.1|
|Angular velocity (rad/s)|0.05|
|IMU|0.05|
|Root position (m)|0.05|


TABLE M: Simulation configuration. 

|**Simulation**|**Parameter**|**Value**|
|---|---|---|
||Simulation substeps<br>Control frequency inverse<br>Number of parallel envs|1<br>17 (_≈_59 Hz)<br>4096|
|Physics|PhysX solver type<br>Position iterations|1 (TGS)<br>4|
||Velocity iterations|1|
||Contact offset (m)|0.02|
||Rest offset (m)|0.0|
||Bounce threshold vel. (m/s)|0.2|
||Max depenetration vel. (m/s)|1.0|
|Ground Plane|Static friction<br>Dynamic friction|1.0<br>1.0|
||Restitution|0.0|


**Domain Randomization and Observation Noise.** We summarize the domain randomization settings for the humanoid and the object in Tables I and J, respectively. Observation noise is summarized in Table L. We additionally apply domain randomization and noise to egocentric perception, summarized in Table K. **Real-World Deployment.** Figure A illustrates the motion-capture system used to support MoCap-driven control, and Figure B shows the objects used in our real-world experiments. 

