---
title: "SteadyTray: Learning Object Balancing Tasks in Humanoid Tray Transport via Residual Reinforcement Learning"
date: "2026-03-11"
authors: "Anlun Huang; Zhenyu Wu; Soofiyan Atar; Yuheng Zhi; Michael Yip"
url: https://arxiv.org/abs/2603.10306
pdf: https://arxiv.org/pdf/2603.10306
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.10306)** / [論文ページ](https://arxiv.org/abs/2603.10306)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SteadyTray: Learning Object Balancing Tasks in Humanoid Tray Transport via Residual Reinforcement Learning** 

Anlun Huang<sup>_∗_</sup> , Zhenyu Wu<sup>_∗_</sup> , Soofiyan Atar<sup>_†_</sup> , Yuheng Zhi<sup>_†_</sup> , Michael Yip UC San Diego _∗†_ Equal Contribution Website: https://steadytray.github.io 


Fig. 1: **ReST-RL** enables a Unitree G1 humanoid to perform the **SteadyTray** task in a real-world setting, with a fluid-filled wine glass as one of the payload. The robot keeps the tray level to prevent fluid sloshing, glass tipping, and payload falling during transport. 

**_Abstract_ — Stabilizing unsecured payloads against the inherent oscillations of dynamic bipedal locomotion remains a critical engineering bottleneck for humanoids in unstructured environments. To solve this, we introduce ReST-RL, a hierarchical reinforcement learning architecture that explicitly decouples locomotion from payload stabilization, evaluated via the SteadyTray benchmark. Rather than relying on monolithic end-to-end learning, our framework integrates a robust base locomotion policy with a dynamic residual module engineered to actively cancel gait-induced perturbations at the end-effector. This architectural separation ensures steady tray transport without degrading the underlying bipedal stability. In simulation, the residual design significantly outperforms end-toend baselines in gait smoothness and orientation accuracy, achieving a 96.9% success rate in variable velocity tracking and 74.5% robustness against external force disturbances. Successfully deployed on the Unitree G1 humanoid hardware, this modular approach demonstrates highly reliable zero-shot sim-to-real generalization across various objects and external force disturbances.** 

## I. INTRODUCTION 

In December 2025, U.S. employers reported 1.25 million job openings in health care and social assistance and 0.81 million in accommodation and food services [1]. The need is pressing to ease labor shortages by automating routine 

delivery and service tasks [2]. Practical service tasks such as spill-free meal delivery, sterile instrument transport in operating rooms, and assistance in elder-care facilities require robots to move and carry objects with human-level reliability in dynamic environments. These human-centered environments are cluttered and designed for humans, often with equipment, cables, and narrow passages that constrain wheeled or quadrupedal platforms. Wheeled platforms cannot generate _active_ stabilizing maneuvers when experiencing large external disturbances. With the rapid progress in humanoid locomotion, humanoid robots may arguably be better suited to navigate such spaces considering their small planar footprint and active stabilization capabilities. 

To maximize transport efficiency and facilitate seamless post-delivery interaction, these scenarios require humanoid robots to walk while balancing unsecured, unstable payloads on trays. It remains unsolved despite substantial recent progress in bipedal locomotion [3] and loco-manipulation [4]. Foot impacts during locomotion are a primary source of torso and base oscillations, and these disturbances propagate through the robot’s kinematic chain. Thus, both the upper body and the gait must adapt to cancel them while maintain- 

ing balance. The most relevant approaches are end-effector stabilization methods such as SoFTA [5], which can reduce oscillation of one object hung or attached to the robot’s hand during walking to some extent. However, to the best of our knowledge, no methods have demonstrated success in balancing unsecured objects on a tray, such as liquid-filled glasses or fragile instruments, during common maneuvers such as turning, accelerating, decelerating, or withstanding external pushes. 

To address this challenge, we formulate _transporting unsecured objects on a tray with a bipedal humanoid robot_ ( **SteadyTray** ) as a bimanual loco-manipulation problem representative of the workforce scenarios above. The key technical difficulty is that the tray introduces a nonrigid intermediate coupling between the robot and payload: the end-effectors regulate tray motion, while objects are only passively constrained and therefore susceptible to slip, tilt, and toppling under dynamic maneuvers. This coupling induces an objective conflict between locomotion and stabilization, since the controller must generate agile whole-body gaits while maintaining near-level end-effector orientation to stabilize tray and payload [5]. We address this with **Residual Student-Teacher Reinforcement Learning (ReST-RL)** , which augments a pre-trained locomotion base policy with a residual module comprising (i) an encoder over privileged robot and payload related observations and (ii) an adapter that outputs corrective residual actions. By freezing the base policy and optimizing only the residual module, **ReST-RL** explicitly separates the two objectives, preserving nominal gait performance while concentrating learning capacity on payload stabilization. Then through policy distillation, the encoder is converted from taking privileged observations to taking deployable ones, while the adapter remains fixed. 

This paper provides the following technical contributions: 

- We propose **ReST-RL** for **SteadyTray** , a residual student–teacher RL framework that augments a pretrained locomotion policy with a payload-stabilization residual adapter for steady tray transport during dynamic walking. 

- We identify key training design choices, including adding observation delay, control latency, and other domain randomizations, that are critical for robustness to disturbance and sim-to-real transfer. 

- We evaluate the approach in simulation and real-world deployment on a Unitree G1 humanoid, demonstrating robust transport of diverse unsecured payloads under external disturbances. 

## II. RELATED WORK 

## _A. Humanoid Loco-Manipulation_ 

Loco-manipulation tasks require humanoids to achieve locomotion and manipulation objectives simultaneously, coupling gait stability with contact-rich object interaction under shared dynamical constraints [2]. Recent sim-to-real reinforcement learning approaches have demonstrated autonomous pick and place [6], door opening [7], package 

carrying and placement [8]–[10], and collaborative transport [11]. 

Prior works can be viewed through how they inject supervision to reduce the exploration burden of contactrich whole-body learning, including human-guided imitation (e.g., teleoperation, mocap, or human videos) [8], [12], interaction-preserving retargeting or trajectory optimization [13], [14], and privileged teacher–student distillation [6], [7]. While these methods improve robustness and generalization, stable transport of _unsecured_ payloads during walking remains underexplored due to non-stationary contact and disturbance-sensitive object dynamics. 

## _B. Humanoid Policy Architectures_ 

Humanoid whole-body control (WBC) policies are typically implemented either as monolithic end-to-end RL controllers [15], [16] or as structured multi-agent designs that decouple locomotion and upper-body control [17], [18]. Training commonly relies on teacher–student distillation and PPO-style actor–critic optimization [19], [20]. 

Residual reinforcement learning augments pretrained locomotion policies with corrective modules to improve robustness under modeling errors and disturbances. Prior works apply residual adaptation for sim-to-real transfer [21], robust teleoperation and motion tracking [22], [23], precise interaction and collaborative carrying [8], [11]. In contrast, we adopt residual RL on stabilization of **SteadyTray** , where object-level dynamics must be regulated without degrading gait stability. 

## _C. Stability Control in Mobile Manipulation_ 

Stability control during transport has been studied for wheeled and aerial manipulators using model-based coordination [24], [25]. On legged systems, quadrupedal payload transport has been explored using tactile feedback [26]. For humanoids, SoFTA [5] demonstrates end-effector stabilization during walking. However, steady transport of _unsecured_ objects requires coordinated whole-body adaptation beyond upper-body compensation alone. Our work addresses this gap through residual whole-body stabilization. 

## III. METHODOLOGY 

## _A. Problem Statement_ 

This work aims to achieve stable dual-arm load transport during humanoid robot locomotion by maintaining the tray level and resisting object tipping under disturbances. The problem is formulated as a goal-conditioned reinforcement learning problem with policy _π_ : _G × S →A_ , where _G_ , _S_ , and _A_ denote the goal, observation, and action spaces, respectively. _A ⊆_ R<sup>_n_</sup> is target joint positions for all humanoid joints. At time _t_ , the goal is denoted **g** _t_ = [ **ˆv** _t_<sup>_rx,_</sup><sup>**ˆv**</sup> _t_<sup>_ry,_</sup><sup>**ˆ**</sup><sup>**_ω_**</sup><sup>_r_</sup> _t_<sup>yaw</sup> ] _∈ G_ which consists of desired robot linear and angular velocity. The observation is **s** _t_ = ( **s**<sup>prop</sup> _t ,_ **s**<sup>obj</sup> _t_<sup>)</sup><sup>_∈S_,including</sup> proprioceptive data and object data. The proprioceptive data **s**<sup>prop</sup> _t_ = [ **q** _t−H_ : _t,_ **˙q** _t−H_ : _t,_ **_ω_**<sup>r</sup> _t−H_ : _t_<sup>_,_</sup><sup>**g**</sup> _t_<sup>r</sup> _−H_ : _t_<sup>_,_</sup><sup>**a**</sup><sup>_t−H_:</sup><sup>_t−_1]</sup><sup>_∈SP_</sup> contains _H_ -step histories of joint positions **q** _t ∈_ R<sup>_n_</sup> , joint velocities **˙q** _t ∈_ R<sup>_n_</sup> , robot angular velocity **_ω_**<sup>r</sup> _t_<sup>_∈_R3,robot</sup> 


Fig. 2: Overview of the **ReST-RL** framework. **Base Policy Training:** A locomotion policy is first trained to carry a tray while maintaining a stable gait. **Residual Module Training:** using privileged observations, a residual module learns whole-body corrective adjustments on top of the frozen base policy to stabilize the payload under disturbances. Two residual designs are considered: (a) **Residual Action Adapter** , which adds corrective residual actions to the base action, and (b) **Residual FiLM Adapter** , which modulates intermediate activations of the frozen base policy via layer-wise FiLM residuals. The student encoder distillation process is shown in Fig. 3. 

projected gravity **g** _t_<sup>r</sup><sup>_∈_R3,andaction</sup><sup>**a**</sup><sup>_t∈_R</sup><sup>_n_.Theobject</sup> data **s**<sup>obj</sup> _t_ = [ **p**<sup>_c_</sup> _t−H_ : _t_<sup>_,_</sup><sup>**q**</sup><sup>_c_</sup> _t−H_ : _t_<sup>]representstheobjectposein</sup> the camera frame _c_ , where **p**<sup>_c_</sup> _t_<sup>=(</sup><sup>_xc_</sup> _t_<sup>_, y_</sup> _t_<sup>_c, z_</sup> _t_<sup>_c_)</sup><sup>_∈_R3isthe</sup> position and **q**<sup>_c_</sup> _t_<sup>_∈_R4isthequaternionorientation.</sup> 

## _B. Base Policy Training_ 

As shown in Fig. 2, **ReST-RL** framework starts by training a base policy _π_<sup>base</sup> : _G × S_<sup>_P_</sup> _→A_ to perform robust locomotion while maintaining a level tray. The base policy takes the _H_ = 5 steps observation **s**<sup>prop</sup> _t_ and outputs the base action _at_ , optimized with the goal-conditioned objective _rt_<sup>base</sup> = _R_<sup>base</sup> ( **g** _t,_ **s**<sup>prop</sup> _t_ ). The policy is updated via PPO [20] to maximize the cumulative discounted reward: E _t_ =1<sup>_γt−_1</sup><sup>_r_</sup> _t_<sup>base</sup> . �� _T_ � 

## _C. Residual Module Learning_ 

As shown in Fig. 2, after obtaining the base policy _π_<sup>base</sup> , we train an encoder–adapter residual module that encodes observations and applies corrective updates to the frozen base policy in _A_ for robust object stabilization. The residual module is first trained with privileged observations and then distilled to one without the privileged information for realworld deployment. This approach draws inspiration from previous work on rapid motor adaptation with privileged information [27]. 

Privileged observations are defined as **s**<sup>priv</sup> _t_ = [ **v** _t_<sup>r</sup> _−H_ : _t_<sup>_,_</sup><sup>**p**tray</sup> _t−H_ : _t_<sup>_,_</sup><sup>**g**</sup> _t_<sup>tray</sup> _−H_ : _t_<sup>_,_</sup><sup>**p**obj</sup> _t−H_ : _t_<sup>_,_</sup><sup>**v**</sup> _t_<sup>obj</sup> _−H_ : _t_<sup>_,_</sup><sup>**_ω_**obj</sup> _t−H_ : _t_<sup>_,_</sup><sup>**g**</sup> _t_<sup>obj</sup> _−H_ : _t_<sup>],</sup> which contain the robot linear velocity, tray position and 

projected gravity, and the object position, linear and angular velocities, and projected gravity, all lying in R<sup>3</sup> . We concatenate the proprioceptive history **s**<sup>prop</sup> _t_ , the goal **g** _t_ , and the privileged observations **s**<sup>priv</sup> _t_ as the encoder input to provide robot-state context and task intent. A longer temporal window ( _H_ = 32) is used for all observations ( **s**<sup>prop</sup> _t ,_ **s**<sup>priv</sup> _t_ ) to capture gradual destabilization trends that are not evident from short-horizon observations. The encoder outputs a 64-dim feature vector **z** ˆ _t_ = _ϕ_ ( **s**<sup>priv</sup> _t ,_ **s**<sup>prop</sup> _t ,_ **g** _t_ ) _∈Z,_ where _Z_ denotes the latent feature space. 

As shown in Fig. 2, two representative integration mechanisms are adopted here to explore residual refinement under different structural configurations. 

_1)_ **_Residual Action Adapter_** _:_ The action adapter is defined as _π_<sup>adapter</sup> : _S_<sup>ˆ</sup> _→A_ , where _S_<sup>ˆ</sup> := _Z × S_<sup>_P_</sup> _× G_ . At time _t_ , the input is ˆ **s** _t_ = [ˆ **z** _t_ ; **s**<sup>prop</sup> _t_ ; **g** _t_ ] _∈ S_<sup>ˆ</sup> , and the action adapter produces a corrective action **a** ˜ _t_ = _π_<sup>adapter</sup> (ˆ **s** _t_ ) _∈A_ , which is applied on top of the base action **a** _t_ from the pretrained base policy. The final refined action sent to the low-level controller is 


where _α_ base is the action scale for base action, _α_ residual is the action scale for residual action, and _q_ default is the default robot joint position. 

_2)_ **_Residual FiLM Adapter_** _:_ We use FiLM adapters [28] to modulate frozen layers of the base policy through affine, feature-wise conditioning from the latent feature **z** ˆ _t_ . For a 


Fig. 3: **Residual module distillation.** The teacher encoder uses privileged observations, whereas the student encoder uses object-centric inputs; both feed into a frozen residual adapter for latent alignment. 

frozen linear layer _f_ ( _·_ ) in _π_<sup>base</sup> with output **y** = _f_ ( **x** ), an adapter predicts ( **_γ_** _t,_ **_β_** _t_ ) = FiLM(ˆ **z** _t_ ) and computes 


where _d_ is the output dimensionality of the modulated layer. Each modulated base policy layer is paired with one FiLM adapter. 

In both instantiations of the residual module, the adapter is initialized to output zero correction at the start of training, so the initial behavior matches the pre-trained base policy and preserves its locomotion skill. As training progresses, the residual modules gradually introduce taskspecific refinements. PPO jointly optimizes adapter parameters _θ_ adapter and encoder parameters _θ_ encoder to maximize E _t_ =1<sup>_γt−_1</sup><sup>_r_</sup> _t_<sup>residual</sup> . The reward _rt_<sup>residual</sup> is defined in Sec�� _T_ � tion III-F. 

## _D. Residual Module Distillation_ 

The privileged information taken by the encoder of the residual module is not directly observable in the real world. Therefore, a non-privileged state encoder is distilled from the privileged state encoder using DAgger [29] for real-world deployment. 

As shown in Fig 3, the distillation process focuses exclusively on the encoder, while the adapter remains frozen. The student encoder receives only object-centric observations **s**<sup>obj</sup> _t_ (with a 32-step history) and outputs **z** _t_ = _ϕ_<sup>_′_</sup> ( **s**<sup>obj</sup> _t_<sup>_,_</sup><sup>**s**prop</sup> _t ,_ **g** _t_ ). The frozen adapter maps **z** _t_ to refined student actions ˆ **a**<sup>student</sup> _t_ . These trajectories are collected and stored during rollout. The teacher encoder, trained with privileged observations **s**<sup>priv</sup> _t_ , outputs latent features ˆ **z** _t_ = _ϕ_ ( **s**<sup>priv</sup> _t ,_ **s**<sup>prop</sup> _t ,_ **g** _t_ ), which are passed through the same frozen adapter to produce refined teacher actions **a** ˆ<sup>teacher</sup> _t_ . The student encoder is then trained with a joint loss that aligns both latent features and refined actions: 


## _E. Domain Randomization and Environment_ 

Robot, tray, and object physical parameters are randomized during training, including mass, friction, restitution, and the robot torso center of mass. This exposes the policy 

TABLE I: Key Rewards Functions 

|Term|Equation|
|---|---|
|Object Upright|exp(_−λ_upright<br>��**P**_xy_<br>�<br>**g**<sup>obj</sup><br>_t_ <sup>)</sup><br>��2<br>2<sup>)</sup>|
|Object-tray Contact|**1**_{_object<br>~~t~~ray<br>~~c~~ontact_}_|
|Linear XY Vel Tracking|exp(_−λvxy_<br>��**v**_rx,y_<br>_t_<br>_−_**ˆv**<sup>_rx,y_</sup><br>_t_<br>��2<br>2<sup>)</sup><br>|
|Angular Vel Tracking|exp(_−λ_**_ω_**_z_<br>��**_ω_**<br>_r_yaw<br>_t_<br>_−_**ˆ****_ω_**<br>_r_yaw<br>_t_<br>��2<br>2<sup>)</sup><br>|
|Torso Vertical Vel|exp(_−λvv_<sup>_rz_ 2</sup><br>_t_<br>)|
|Torso Angular Vel|exp(_−λω_<br>��**_ω_**_rx,y_<br>_t_<br>��2<br>2<sup>)</sup><br>|
|Feet Impact|exp(_−λvz_<br>���**v**feet<br>_z,t _<sup>_−_</sup><sup>**v**feet</sup><br>_z,t−_1<br>���<br>2<br>2<sup>)</sup><br>|
|Tray Upright|exp(_−λ_upright<br>��**P**_xy_<br>�<br>**g**<sup>tray</sup><br>_t_<br>)<br>��2<br>2<sup>)</sup>|
|Tray-EE Contact|**1**_{_tray<br>~~e~~e<br>~~c~~ontact_}_|
|Tray-EE Quat Error|exp(_−λ_quat∆_θ_<sup>2</sup><br>_t_ <sup>)</sup>|


to diverse contact dynamics and inertial variations. Control delay is also introduced to account for actuation and communication latency. 

Cylindrical objects with diverse scales are sampled during training and initialized near the tray center with randomized horizontal offsets and yaw rotation to avoid overfitting to a fixed initial configuration. To ensure a stable initialization phase, velocity commands are set to zero within the initial second of each episode [26]. Random push perturbations are applied to the object during training to improve robustness and encourage the residual module to learn recovery behaviors under external disturbances. 

Observation noise is injected into all observation terms during both training and distillation. To model perception latency, an observation delay is introduced for object-related observations ( **s**<sup>obj</sup> _t_<sup>_,_</sup><sup>**s**priv</sup> _t_ ). At time _t_ , a delay _ℓt_ is sampled such that the residual module receives measurements from _t − ℓt_ , and the sampled delay is maintained for multiple steps to mimic temporally correlated latency. This delay is applied only to object observations, as object perception typically incurs higher latency than proprioceptive sensing. 

## _F. Reward Design_ 

Several base-locomotion reward terms are adapted from prior open-source works [30], [31], and augmented with object-stabilization terms. We define a base reward _rt_<sup>base</sup> and a stabilization reward _rt_<sup>obj.Thebasepolicyisoptimized</sup> with _rt_<sup>base</sup> , while the residual module is optimized with the combined objective _rt_<sup>residual</sup> = _rt_<sup>base</sup> + _rt_<sup>obj,where</sup><sup>_r_</sup> _t_<sup>obj</sup> promotes payload stability during locomotion. TABLE I summarizes the key reward components used in **ReST-RL** . The base reward _rt_<sup>base</sup> primarily consists of standard locomotion objectives, with regularization terms (e.g., joint limits and action rate penalties) to prevent aggressive motions. Torso stabilization terms reward low vertical torso velocity and low roll/pitch angular velocity, promoting smooth upperbody motion during locomotion. Waist-joint deviation is only lightly penalized, since overly strict waist constraints reduce the policy’s ability to compensate for disturbances through active upper-body adjustment. A foot impact term rewards small changes in vertical foot velocity, reducing landing forces propagated to the tray. The base reward also 

|**Simulation R**|**esults (Isaac Lab)**|**TrackLin**|**Err (m/s)** _↓_|**TrackAn**|**gErr (rad/s)** _↓_|**Grav-**|**XY** _↓_|**Success Rate (%)** _↑_|
|---|---|---|---|---|---|---|---|---|
|**Task**|**Method**|**mean**|**std**|**mean**|**std**|**mean**|**std**||
||Base Policy (WB)|0.110|0.107|**0.078**|0.065|0.179|0.064|47.4|
||End2End|0.116|0.111|0.096|0.078|0.046|0.029|89.1|
|Command Track|**ReST-RL** (Action WB)|**0.093**|0.100|0.081|0.070|**0.029**|0.022|95.9|
||**ReST-RL** (Action JT)|0.160|0.102|0.135|0.106|0.031|0.019|96.7|
||**ReST-RL (FiLM WB)**|0.106|0.098|0.069|0.058|0.046|0.023|**96.9**|
||Base Policy (WB)|0.162|0.222|0.110|0.156|0.190|0.089|9.1|
||End2End|0.170|0.215|0.123|0.155|0.055|0.051|44.0|
|Push Robot|**ReST-RL** (Action WB)|0.146|0.204|0.110|0.142|0.039|0.044|73.4|
||**ReST-RL** (Action JT)|0.190|0.168|0.176|0.213|**0.038**|0.040|72.5|
||**ReST-RL (FiLM WB)**|**0.142**|0.168|**0.094**|0.123|0.043|0.032|**84.6**|
||Base Policy (WB)|0.110|0.111|0.079|0.066|0.186|0.072|25.2|
||End2End|0.117|0.114|0.099|0.080|0.049|0.043|50.2|
|Push Object|**ReST-RL** (Action WB)|**0.096**|0.103|0.084|0.076|**0.023**|0.039|71.3|
||**ReST-RL** (Action JT)|0.161|0.104|0.141|0.118|0.033|0.039|70.7|
||**ReST-RL (FiLM WB)**|0.107|0.100|**0.073**|0.068|0.040|0.034|**74.6**|


TABLE II: Simulation results in Isaac Lab. Object stability of baselines and instantiations of **ReST-RL** with different Residual Module architectures is evaluated across various scenarios. In all three tasks, the target locomotion commands are identical. 

includes tray-related terms. In particular, a tray–end-effector orientation term rewards maintaining a predefined holding configuration, ensuring consistent contact between the tray and both end-effectors. 

For the object reward _rt_<sup>obj,weuseasparseformulation</sup> which includes two object-related terms: an upright term that encourages alignment between the object’s vertical axis and gravity, and a contact term that rewards object-tray contact. Without explicit position or velocity targets, this design allows adapter to discover emergent recovery strategies under perturbations. 


Fig. 4: Training reward comparison between End2End and **ReST-RL** . 

## IV. EXPERIMENTS 

This section assesses **ReST-RL** ’s performance through simulation studies and real-world deployment on a Unitree G1 humanoid robot (29 DoF). In particular, evaluation focus on answering following questions: 

**Q1:** How do key components (action adapter, FiLM adapter, and observation delay) affect performance on **SteadyTray** task? 

**Q2:** How robust is **ReST-RL** to disturbances of different types and magnitudes, and how well does it generalize across objects with diverse scales? 

**Q3:** Does **ReST-RL** demonstrate reliable sim-to-real transfer? 

## _A. Experiment Setup_ 

All experiments are conducted on Unitree G1 robots with specially designed end effectors for tray holding. The endeffectors support the tray and partially constrain its motion, but the tray is not rigidly attached to either end-effector. In real-world deployment, we place an AprilTag on the object and use the Unitree G1’s head-mounted RealSense D435 camera to estimate the object’s pose. 

_1)_ **_Tasks_** _:_ We evaluate three simulation tasks: (i) Command Track, which tracks velocity commands while carrying a payload, with targets resampled every 10s; (ii) Push Robot, which applies random forces to the robot torso during 

locomotion for _tr_ seconds per event; and (iii) Push Object, which applies random forces to the object during locomotion for _to_ seconds per event. All three tasks share the same goal-tracking locomotion commands. Each episode lasts 20s, and pushes are triggered every 5s. Physical properties and randomization settings match training, and object body scales are randomized. 

_2)_ **_Baselines_** _:_ Two pre-training base policies are considered: Joint-Training (JT) and Whole-Body (WB). Both follow a two-stage curriculum: (i) a locomotion stage trains a stable gait with observation ( **s**<sup>prop</sup> _t ,_ **g** _t_ ), then (ii) tray-stability rewards are added while continuing optimization. JT decouples the action space into an upper-body policy (arm/wrist joints) and a lower-body policy (leg joints), while WB uses a single policy controlling all joints. We also consider an Endto-End (End2End) baseline, where a single policy is trained from scratch on both locomotion and stabilization rewards, taking the full observation ( **s**<sup>prop</sup> _t ,_ **s**<sup>obj</sup> _t_<sup>_,_</sup><sup>**g**</sup><sup>_t_)asinput.</sup> 

_3)_ **_Metrics_** _:_ Success rate is the fraction of trials in which the on-tray object remains upright and stays on the tray for the entire horizon (i.e., no tilt or drop). Linear and angular tracking errors are the absolute differences between the commanded and measured torso linear speed in the horizontal plane and torso yaw rate about the vertical axis, respectively. Object Projected Gravity XY Tilt measures 


Fig. 5: Success rate of **ReST-RL** trained with and without observation delay under increasing perception latency in Push Robot task. 


Fig. 6: Velocity tracking and disturbance recovery of **ReSTRL** . Torso and object velocities closely follow the commanded velocity under command changes and external pushes. 

object tilt as the _L_ 2 norm of the _x, y_ component of the unit gravity vector projected into the object’s local frame. A value of 0 indicates a perfectly upright object, while a value approaching 1 indicates that the object is nearly horizontal. All simulation metrics are computed over _N_ independent trials. 

## _B. Ablation Study_ 

TABLE II reports baselines and **ReST-RL** results across three simulation tasks, addressing **Q1** . To isolate design effects, we evaluate: **ReST-RL** (FiLM), which employs a FiLM adapter in the residual module; **ReST-RL** (Action WB) and **ReST-RL** (Action JT), which use action adapters built on WB and JT bases. 

All **ReST-RL** instantiations substantially improve success rates and reduce projected gravity compared to the base policy, while command tracking error remains comparable. This shows the proposed design enhanced object stability without substantially sacrificing command-following performance. Performance across FiLM WB, Action WB, and Action JT is broadly similar, suggesting that the improvement primarily stems from structured residual adaptation conditioned on object-related features rather than a specific architectural choice. 


Fig. 7: Success rate of **ReST-RL** in ( **a** ) Push Robot task and ( **b** ) Push Object task under varying push directions and magnitudes. 


Fig. 8: Success rate of **ReST-RL** across different object body scales in Push Robot task. 

Although the End2End policy achieves reasonable performance in the Command Track task, its robustness under Push Robot and Push Object is significantly lower than that of **ReST-RL** . To better understand this gap, Fig. 4 decomposes the reward components during training. While End2End attains a comparable mean total reward, much of this reward stems from locomotion-related terms. In contrast, its object upright reward remains noticeably lower than that of **ReSTRL** . This gap suggests that directly optimizing both locomotion and object-stability objectives is non-trivial, whereas structured residual adaptation provides a more reliable route to robust stabilization. 

In addition to structured residual adaptation, we further analyze the effect of delayed observation. Fig. 5 evaluates the success rate of **ReST-RL** trained with and without observation delay under increasing perception latency. Across all delay settings, the **ReST-RL** trained with delayed observations consistently achieves higher success rates, including the zero-latency case. Although observation delay is primarily introduced to improve sim-to-real transfer by accounting for sensing latency, these results indicate that it also enhances overall stabilization performance. 

## _C. Simulation Result_ 

To answer **Q2** , we evaluate **ReST-RL** in simulation under disturbances of varying types and magnitudes, and across objects with diverse scales. 


Fig. 9: **ReST-RL** deployed on a Unitree G1 humanoid demonstrating payload stabilization capabilities. ( **a** ) Stabilizing the payload when the robot is kicked; ( **b** ) stabilizing the payload when the object is pushed; ( **c** , **d** ) stably transporting various payloads. 

Fig. 6 demonstrates the velocity tracking and disturbance recovery behavior of **ReST-RL** under command switches and external pushes. The torso velocity closely tracks the commanded value while the object velocity remains tightly coupled to it. Under both robot-level pushes (10s, 13s) and object-level perturbation (around 16s), deviations are quickly corrected without sustained oscillation, demonstrating robust recovery. 

In Fig. 7a and 7b, both plots illustrate **ReST-RL** maintains consistently high success rates across a wide range of push directions and magnitudes for both robot pushes and object pushes. As shown in Fig. 7, **ReST-RL** maintains high success rates across diverse push directions and magnitudes for both robot and object pushes (74.4% and 73.9% respectively), with only moderate degradation under extreme forces, demonstrating robustness to both body-level and payload-level perturbations. 

Fig. 8 evaluates **ReST-RL** across varying cylinder radiusto-height ratios. Success rates remain consistently high across a broad range of aspect ratios, with only a modest drop for extremely slender objects (e.g., ratio 0.1), demonstrating robustness to diverse payload geometries. 

## _D. Real-World Results_ 

As shown in Fig. 9, **ReST-RL** is deployed on a Unitree G1 humanoid robot to evaluate its payload stabilization capability under external disturbances and object variations in real-world environments. 

Fig. 9(a) and (b) show experiments where external disturbances are applied to the robot and the payload, respectively. In both cases, **ReST-RL** demonstrates timely whole-body recovery behaviors by coordinating upper and lower-body joints to re-stabilize the tray and prevent payload tipping under external disturbances. Recovery is achieved without abrupt corrective motions, demonstrating the robustness of the learned control strategy. Fig. 9(c) and (d) demonstrate generalization to objects with diverse geometries and physical properties, including a standard coffee cup, a waterfilled wine glass, medical and surgical tools, and a sealed food container. Despite their varying mass distributions, geometries, and contact properties, **ReST-RL** generalizes across all objects without retraining or fine-tuning. These results indicate strong sim-to-real transfer and robustness to real-world perception and dynamics. 

## V. DISCUSSION AND CONCLUSION 

This paper formulates a new bimanual loco-manipulation problem, transporting unsecured objects on a tray with a bipedal humanoid robot under external disturbances, namely **SteadyTray** . This paper also proses **ReST-RL** , a residual student–teacher reinforcement learning framework for solving **SteadyTray** . By decoupling locomotion from payload stabilization, the residual module resolves these competing objectives while preserving both gait quality and object stability. Our training strategy further incorporates delayed object observations, control-latency, and domain randomization 

over physical and sensing parameters. Together, these design choices reduce reliance on instantaneous measurements and promote temporally consistent control, improving sim-toreal transfer and robustness in real-world conditions. Beyond the **SteadyTray** problem, **ReST-RL** may be extended to broader loco-manipulation skills that require task-specific sensing beyond standard proprioception, such as contact-rich manipulation during walking (e.g., door opening and cart pushing) and whole-body adaptation using vision or tactile feedback while preserving a robust pretrained gait. 

Although potentially extensible, the current object encoding is limited to a single object and does not yet capture fine geometric or physical properties. Future work could integrate foundation pose-estimation models or vision-based RL to improve object representation. Hardware constraints also limit perception: the fixed head-mounted camera has a narrow field of view. This restricted viewpoint makes it difficult to transport objects in alternative holding poses, which are often needed in cluttered scenes to avoid collisions. More broadly, pure sim-to-real RL often requires extensive reward shaping and careful simulator refinement, which becomes impractical for complex contact-rich loco-manipulation tasks. 

## REFERENCES 

- [1] U.S. Bureau of Labor Statistics, “Job openings and labor turnover – december 2025,” News Release USDL-26-0167, Feb. 2026. [Online]. Available: https://www.bls.gov/news.release/archives/jolts ~~0~~ 2052026. 

htm 1 

- [2] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _arXiv preprint arXiv:2501.02116_ , 2025. 1, 2 

- [3] Z. Wu, X. Huang, L. Yang, Y. Zhang, K. Sreenath, X. Chen, P. Abbeel, R. Duan, A. Kanazawa, C. Sferrazza _et al._ , “Perceptive humanoid parkour: Chaining dynamic human skills via motion matching,” _arXiv preprint arXiv:2602.15827_ , 2026. 1 

- [4] R.-Z. Qiu, S. Yang, X. Cheng, C. Chawla, J. Li, T. He, G. Yan, D. J. Yoon, R. Hoque, L. Paulsen _et al._ , “Humanoid policy˜ human policy,” _arXiv preprint arXiv:2503.13441_ , 2025. 1 

- [5] Y. Li, Y. Zhang, W. Xiao, C. Pan, H. Weng, G. He, T. He, and G. Shi, “Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control,” in _RSS 2025 Workshop on Wholebody Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ , 2025. 2 

- [6] T. He, Z. Wang, H. Xue, Q. Ben, Z. Luo, W. Xiao, Y. Yuan, X. Da, F. Casta˜neda, S. Sastry _et al._ , “Viral: Visual sim-to-real at scale for humanoid loco-manipulation,” _arXiv preprint arXiv:2511.15200_ , 2025. 2 

- [7] H. Xue, T. He, Z. Wang, Q. Ben, W. Xiao, Z. Luo, X. Da, F. Casta˜neda, G. Shi, S. Sastry _et al._ , “Opening the sim-to-real door for humanoid pixel-to-action policy transfer,” _arXiv preprint arXiv:2512.01061_ , 2025. 2 

- [8] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan, “Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning,” _arXiv preprint arXiv:2510.05070_ , 2025. 2 

- [9] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi, “Hdmi: Learning interactive humanoid whole-body control from human videos,” _arXiv preprint arXiv:2509.16757_ , 2025. 2 

   - [13] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” _arXiv preprint arXiv:2509.26633_ , 2025. 2 

   - [14] F. Liu, Z. Gu, Y. Cai, Z. Zhou, H. Jung, J. Jang, S. Zhao, S. Ha, Y. Chen, D. Xu _et al._ , “Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid loco-manipulation,” _arXiv preprint arXiv:2409.20514_ , 2024. 2 

   - [15] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 8944–8951. 2 

   - [16] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 2 

   - [17] Y. Zhang, Y. Yuan, P. Gurunath, T. He, S. Omidshafiei, A. akbar Agha-mohammadi, M. Vazquez-Chanlatte, L. Pedersen, and G. Shi, “Falcon: Learning force-adaptive humanoid loco-manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2505.06776 2 

   - [18] C. Lu, X. Cheng, J. Li, S. Yang, M. Ji, C. Yuan, G. Yang, S. Yi, and X. Wang, “Mobile-television: Predictive motion priors for humanoid whole-body control,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 5364–5371. 2 

   - [19] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” _arXiv preprint arXiv:1503.02531_ , 2015. 2 

   - [20] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” 2017. [Online]. Available: https://arxiv.org/abs/1707.06347 2, 3 

   - [21] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 2 

   - [22] Z. Sun, B.-S. Huang, Y. Peng, X. Li, J. Ma, Y. Sun, Z. Li, H. Jiang, B. Gao, Z. Bing _et al._ , “Mosaic: Bridging the sim-to-real gap in generalist humanoid motion tracking and teleoperation with rapid residual adaptation,” _arXiv preprint arXiv:2602.08594_ , 2026. 2 

   - [23] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu _et al._ , “Track any motions under any disturbances,” _arXiv preprint arXiv:2509.13833_ , 2025. 2 

   - [24] J. Pankert and M. Hutter, “Perceptive model predictive control for continuous mobile manipulation,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 6177–6184, 2020. 2 

   - [25] G. He, X. Guo, L. Tang, Y. Zhang, M. Mousaei, J. Xu, J. Geng, S. Scherer, and G. Shi, “Flying hand: End-effector-centric framework for versatile aerial manipulation teleoperation and policy learning,” _arXiv preprint arXiv:2504.10334_ , 2025. 2 

   - [26] C. Lin, Y. R. Song, B. Huo, M. Yu, Y. Wang, S. Liu, Y. Yang, W. Yu, T. Zhang, J. Tan _et al._ , “Locotouch: Learning dexterous quadrupedal transport with tactile sensing,” _arXiv preprint arXiv:2505.23175_ , 2025. 

      - 2, 4 

   - [27] H. Qi, B. Yi, S. Suresh, M. Lambeta, Y. Ma, R. Calandra, and J. Malik, “General in-hand object rotation with vision and touch,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2549–2564. 3 

   - [28] E. Perez, F. Strub, H. de Vries, V. Dumoulin, and A. C. Courville, “Film: Visual reasoning with a general conditioning layer,” _CoRR_ , vol. abs/1709.07871, 2017. [Online]. Available: http://arxiv.org/abs/1709.07871 3 

   - [29] S. Ross, G. J. Gordon, and J. A. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” 2011. [Online]. Available: https://arxiv.org/abs/1011.0686 4 

   - [30] Unitree Robotics, “Unitree RL Lab,” GitHub repository, Oct. 2025. [Online]. Available: https://github.com/unitreerobotics/unitree ~~r~~ l ~~l~~ ab 4 

   - [31] D. M¨uller, E. Knoop, D. Mylonopoulos, A. Serifi, M. A. Hopkins, R. Grandia, and M. B¨acher, “Olaf: Bringing an animated character to life in the physical world,” 2025. [Online]. Available: https://arxiv.org/abs/2512.16705 4 

- [10] Y. Fu, F. Xie, C. Xu, J. Xiong, H. Yuan, and Z. Lu, “Demohlm: From one demonstration to generalizable humanoid loco-manipulation,” _arXiv preprint arXiv:2510.11258_ , 2025. 2 

- [11] Y. Du, Y. Li, B. Jia, Y. Lin, P. Zhou, W. Liang, Y. Yang, and S. Huang, “Learning human-humanoid coordination for collaborative object carrying,” _arXiv preprint arXiv:2510.14293_ , 2025. 2 

- [12] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu, “Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation,” _arXiv preprint arXiv:2509.20322_ , 2025. 2 

APPENDIX 

## _D. Training Hyperparameter_ 

## _A. Observation Details_ 

TABLE III: Observation Terms 

||Term|Dim|
|---|---|---|
|Proprioception (_s_<sup>prop</sup>)|Joint position|R<sup>29</sup>|
||Joint velocity<br>Last action<br>Base angular velocity<br>Base projected gravity|R<sup>29</sup><br>R<sup>29</sup><br>R<sup>3</sup><br>R<sup>3</sup>|
|Object (_s_<sup>obj</sup>)|Object position (camera frame)<br>Object quaternion (camera frame)|R<sup>3</sup><br>R<sup>4</sup>|
|Privilege (_s_<sup>priv</sup>)|Base linear velocity|R<sup>3</sup>|
||Tray position (robot frame)|R<sup>3</sup>|
||Tray projected gravity<br>Object position (tray frame)|R<sup>3</sup><br>R<sup>3</sup>|
||Object angular velocity (tray frame)<br>Object linear velocity (tray frame)<br>Object projected gravity|R<sup>3</sup><br>R<sup>3</sup><br>R<sup>3</sup>|
|Goal (_g_)|Velocity command|R<sup>3</sup>|


## _B. Reward and Termination Details_ 

All reward and termination terms used throughout training are summarized in TABLE IV. The training procedure is divided into three stages. **Stage 1** (Pre-train Locomotion) trains a base locomotion policy with velocity tracking, body stability, and gait regularization rewards. **Stage 2** (Tray Holding Fine-tune) builds upon the **Stage 1** policy by introducing tray-specific rewards, including orientation, contact, and holder alignment, to learn stable tray transport. **Stage 3** (Residual Object Stabilization) trains the residual module with object-related rewards for keeping an object upright on the tray. Each subsequent stage inherits all terms from the previous stage, modifying or disabling specific terms as needed. 

For task-specific failure conditions such as the tray or object dropping, we employ a _delayed-timeout_ mechanism rather than immediate episode termination (marked with<sup>_†_</sup> in TABLE IV), where episodes are truncated when a tracked condition remains violated for a configured duration (1.0 s in our setup). This design serves two purposes. First, it improves sampling efficiency as continued simulation yields minimal task-relevant learning signal once the object or tray is unrecoverable. Second, the delay window allows the policy to observe post-failure states and learn to maintain stable locomotion, which is critical for safe real-world deployment where unseen object states may trigger erratic behavior. In addition, the value function bootstrap is preserved in truncated episodes and the critic does not incorrectly learn to associate post-failure states with zero future return. 

TABLE VI and TABLE VII summarize the training hyperparameters for the residual teacher and encoder distillation stages, respectively. We experiment with two residual designs: residual FiLM and residual action, both of which share the same Transformer-based history encoder. The encoder distillation stage inherits the full teacher architecture and trains a student encoder to replicate the teacher’s embeddings from proprioceptive and object observations. All experiments are conducted on two NVIDIA RTX A6000 GPUs with 4 096 parallel environments per GPU. 

## _E. Training Strategy_ 

In this section, we detail an additional strategy applied during Stage 1 (pre-training locomotion) to accelerate policy training. 

In whole-body policy training, the large action space can significantly slow convergence, as the optimizer simultaneously explores locomotion gaits and upper-body movements. To address this, we introduce an auxiliary _upper-body curriculum_ loss during Stage 1 that effectively freezes the upperbody joints, allowing the policy to focus exclusively on learning stable lower-body locomotion. 

Concretely, we add a regularization term to the PPO loss that penalizes both the mean and standard deviation of the policy’s action distribution on specified upper-body joint indices _J_ upper: 


where _µb,j_ and _σb,j_ are the mean and standard deviation of the policy’s action distribution for joint _j_ in sample _b_ , _B_ denotes the mini-batch, and _α_ is a coefficient that can be decayed over training via a curriculum schedule. 

The L2 penalty on _µ_ drives the upper-body actions toward zero (i.e., the default pose), while the penalty on _σ_ suppresses exploration on these joints, preventing the optimizer from wasting gradient updates on uninformative upper-body movements during early locomotion learning. This regularizer is applied only in Stage 1 and removed in subsequent stages, where the upper-body joints are freed to learn tray-holding and object-stabilization behaviors. In practice, this strategy reduces Stage 1 training time substantially by suppressing exploration on upper-body joints and focusing gradient updates on the lower-body joints relevant for locomotion. 

## _C. Domain Randomization_ 

All domain randomization terms used throughout training are summarized in TABLE V. 

TABLE IV: Reward and termination terms across three training stages. Terms marked with<sup>_†_</sup> are _delayed-timeout_ termination conditions: they do not immediately reset the episode, but will trigger a timeout (truncation) after the configured delay has elapsed. Terms marked with<sup>_‡_</sup> indicate a change from the previous stage. 

|**Training Stage**|**Term**|**Expression**|**Weight**|
|---|---|---|---|
||_Locomotion tracking rewards_|||
||Track linear vel|exp<br>�<br>_−_<br>��**v**_rx,y_<br>_t_<br>_−_**ˆv**<sup>_rx,y_</sup><br>_t_<br>��2<br>2<sup>_/σ_2�</sup><br>, _σ_=<br>_~~√~~_<br>0_._25<br>|1.0|
||Track angular vel|exp<br>�<br>_−_<br>��**_ω_**<br>_r_yaw<br>_t_<br>_−_**ˆ****_ω_**<br>_r_yaw<br>_t_<br>��2<br>2<sup>_/σ_2�</sup><br>, _σ_=<br>_~~√~~_<br>0_._25|1.5|
||_Survival & body stability rewards_|||
||Robot Alive bonus|**1**[alive]<br>|1.0|
||Torso vertical lin vel|exp<br>�<br>_−λ v_<sup>_rz_ 2</sup><br>_t_<br>�<br>, _λ_=2<br>|0.2|
||Torso roll/pitch ang vel|exp<br>�<br>_−λ_<br>��**_ω_**_rx,y_<br>_t_<br>��2<br>2<br>�<br>, _λ_=1<br><br><br>2|0.2|
||Upright torso<br>|exp(_−λ_<br>��**P**_xy_<br>�<br>**g**<sup>r</sup><br>_t_<sup>)</sup><br>��<br>2<sup>),</sup> <sup>_λ_=4</sup><br><br> <br><br>|0.25<br>|
|**Stae1:**|Torso height|exp<br>�<br>_−λ |h_torso_−h_target_|_<br>�<br>, _λ_=10, _h_target=0_._82|0.5|
|**g **<br>Pre-train|_Regularization penalties_|||
|Locomotion|Joint velocity|�<br>_i_ <sup>˙</sup><sup>_q_2</sup><br>_i,t_|_−_0.001|
||Joint acceleration|�<br>_i_ <sup>¨</sup><sup>_q_2</sup><br>_i,t_|_−_2_._5_×_10<sup>_−_7</sup>|
||Action rate|�<br>_i_<sup>(</sup><sup>_ai,t −ai,t−_1)2</sup>|_−_0.05|
||Joint position limits<br>|�<br>_i_<br>�<br>max(0_, qi,t−q_<sup>_u_</sup><br>_i,t_<sup>) + max(0</sup><sup>_, ql_</sup><br>_i,t_<sup>_−qi,t_)</sup><br>�<br><br>|_−_5.0<br>|
||Energy consumption|�<br>_i _<sup>_|_ ˙</sup><sup>_qi,t| |τi,t|_</sup>|_−_2_×_10<sup>_−_5</sup>|
||Arm joint deviation (L1)|<br>�<br>_i∈_arms <sup>_|qi,t −q_default</sup><br>_i,t_<br>_|_|_−_0.5|
||Waist yaw joint deviation|_|q_waist<br>~~y~~aw_,t _<sup>_−q_default</sup><br>waist<br>~~y~~aw_,t_<sup>_|_</sup>|_−_1.0|
||_Feet rewards & penalties_|||
||Feet slide|�<br>_k_<sup>_∥_</sup><sup>**v**</sup><sup>_xy_</sup><br>foot_k,t_<sup>_∥·_</sup><sup>**1**[foot</sup>_k_<br>~~c~~ontact]|_−_0.2|
||Foot clearance|exp<br>�<br>_−_<sup>1</sup><br>_σ_<br>�<br>_k_<sup>(</sup><sup>_z_foot</sup>_k_<sup>_,t −_0</sup><sup>_._1)2</sup><sup>_·_ tanh(2</sup><sup>_∥_</sup><sup>**v**</sup><sup>_xy_</sup><br>foot_k,t_<sup>_∥_)</sup><br>�<br>, _σ_=0_._05<br><br><br>|1.0|
||Feet impact|exp<br>�<br>_−λ_<br>���**v**feet<br>_z,t _<sup>_−_</sup><sup>**v**feet</sup><br>_z,t−_1<br>���<br>2<br>2<br>�<br>, _λ_=5|0.5|
||Undesired contacts|**1**[undesired<br>~~b~~ody<br>~~c~~ontact]|_−_1.0|
||_Termination conditions_|||
||Time out|Episode length exceeded (_T_=20s)|—|
||Robot Base height|**1**[_zr_<br>_t _<sup>_<_0</sup><sup>_._4] (terminated)</sup>|—|
||Robot Bad orientation|<br>**1**[tilttorso_>_0_._7 rad] (terminated)|—|
||_Inherits all Stage 1 terms, with the _<br>|_following changes and additions:_||
||_Modified terms from Stage 1_<sup>_‡_</sup>|||
||_i_<br>Arm joint deviation (exp)<sup>_‡_</sup>|exp<br>�<br>_−λ_ <sup>�</sup><br>_i∈_arms <sup>_|qi,t −q_default</sup><br>_i,t_<br>_|_<br>�<br>, _λ_=0_._3|0.5|
||_Tray stability rewards (new)_|||
||Tray upright|exp(_−λ_<br>��**P**_xy_<br>�<br>**g**<sup>tray</sup><br>_t_<br>)<br>��2<br>2<sup>),</sup> <sup>_λ_=4</sup>|0.25|
|**Stage 2:**<br>Pre-train|Tray vertical lin vel|exp<br>�<br>_−λ v_<sup>tray 2</sup><br>_z,t_<br>�<br>, _λ_=2<br><br>|0.2|
|Tray Holding|Tray roll/pitch ang vel|exp<br>�<br>_−λ_<br>��**_ω_**<br>tray_x,y_<br>_t_<br>��2<br>2<br>�<br>, _λ_=1|0.2|
|Fine-tune|Tray-EE contact|**1**[tray<br>~~e~~e<br>~~c~~ontact]<br>|0.01|
||Tray-EE contact force|exp<br>�<br>_−λ_<br>��**_F_**tray<br>~~e~~e<br>_t_<br>��<br>2<br>�<br>, _λ_=0_._005<br><br>|0.2|
||Tray–Left-EE quat alignment|exp<br>�<br>_−λ ·_2 arccos(_|_**q**<sup>tray</sup><br>_t_<br>_·_**q**<sup>left</sup><br>~~e~~e<br>_t_<br>_|_)<sup>2�</sup><br>, _λ_=2<br><br>|0.5|
||Tray–Left-EE quat alignment|exp<br>�<br>_−λ ·_2 arccos(_|_**q**<sup>tray</sup><br>_t_<br>_·_**q**<sup>right</sup><br>~~e~~e<br>_t_<br>_|_)<sup>2�</sup><br>, _λ_=2|0.5|
||Joint torque penalty|<br><br> <br><br><br><br>�<br>_i _<sup>_τ_ 2</sup><br>_it_|_−_2_×_10<sup>_−_5</sup>|
||_Termination conditions (new)_|_,_||
||Tray fallen<sup>_†_</sup>|**1**[_z_tray_<_0_._7] (timeout after 1_._0s)|—|
||_Inherits all Stage 2 terms, with the _|_following changes and additions:_||
||_Disabled terms from Stage 2_<sup>_‡_</sup><br>|||
||Tray vertical lin vel<sup>_‡_</sup>|(disabled)|—|
|**S3**|Tray roll/pitch ang vel<sup>_‡_</sup>|(disabled)|—|
|**tage :**<br>ResidualObject|_Object stability rewards (new)_|||
|<br>Stabilization|Object-tray contact|**1**_{_object<br>~~t~~ray<br>~~c~~ontact_}_|0.05|
||Object upright|exp(_−λ_<br>��**P**_xy_<br>�<br>**g**<sup>obj</sup><br>_t_ <sup>)</sup><br>��2<br>2<sup>),</sup> <sup>_λ_=4</sup>|1.0|
||_Termination conditions (new)_|||
||Object fallen<sup>_†_</sup>|**1**[_z_obj_<_0_._7] (timeout after 1_._0s)|—|
||Object bad orientation<sup>_†_</sup>|**1**[tiltobj_>_0_._7 rad] (timeout after 1_._0s)|—|


TABLE V: Domain randomization parameters 

|**Parameter**|**Range / Value**|
|---|---|
|Robot static friction|[0_._3_,_1_._0]|
|Robot dynamic friction|[0_._3_,_1_._0]|
|End-effector static friction|[2_._0_,_3_._0]|
|End-effector dynamic friction|[1_._5_,_2_._5]|
|End-effector restitution|[0_._0_,_0_._05]|
|End-effector mass|[0_._05_,_0_._3]kg|
|Torso added mass|[_−_2_._0_,_3_._0]kg|
|Torso CoM offset|_x∈_[_±_0_._025], _y∈_[_±_0_._05], _z∈_[_±_0_._05]m|
|Tray static friction|[1_._2_,_2_._0]|
|Tray dynamic friction|[1_._0_,_1_._8]|
|Tray restitution|[0_._0_,_0_._05]|
|Tray mass|[0_._3_,_0_._7]kg|
|Object radius scale|[0_._7_,_1_._5]_×_0.03m|
|Object height scale|[0_._75_,_2_._0]_×_0.1m|
|Object static friction|[0_._5_,_1_._0]|
|Object dynamic friction|[0_._4_,_0_._9]|
|Object restitution|[0_._0_,_0_._5]|
|Object mass|[0_._05_,_1_._0]kg|
|Object CoM offset|_x∈_[_±_0_._01], _y∈_[_±_0_._01], _z∈_[_±_0_._02]m|
|Joint velocity reset|[_−_1_._0_,_1_._0]rad/s|
|External push on robot|every [3_,_5]s, _vxy∈_[_±_0_._5]m/s|
|External push on object|every [2_,_4]s,<br>_vxy∈_[_±_0_._3]m/s, _ωxy∈_[_±_0_._3]rad/s|


TABLE VI: Hyperparameters for residual teacher policy (PPO). Both adapter variants share the same base MLP, encoder, and PPO configuration. 

|**Hyperparameters**|**Values**|
|---|---|
|_Runner_||
|Number of environments|8 192 (4 096 _×_ 2 GPUs)|
|Number of steps per environment|24|
|_Base policy_||
|MLP size (actor & critic)|[512, 256, 128]|
|_Transformer encoder_||
|Context dimension (_d_ctx)|64|
|Encoder layers|2|
|Attention heads|4|
|_Residual FiLM adapter_||
|FiLM hidden dim|128|
|_γ_ clamp|_±_3_._0|
|_Residual action adapter_||
|Residual MLP size|[512, 256, 128]|
|_Algorithm (PPO)_||
|LR schedule|Adaptive|
|Discount factor (_γ_)|0.99|
|GAE _λ_|0.95|
|Clip parameter (_ϵ_)|0.2|
|Value loss coefficient|1.0|
|Entropy coefficient|0.01|
|Desired KL|0.01|
|Num learning epochs|5|
|Num mini-batches|4|
|Max gradient norm|1.0|


TABLE VII: Hyperparameters for encoder distillation. 

|**Hyperparameters**|**Values**|
|---|---|
|_Runner_||
|Number of environments|8 192 (4 096 _×_ 2 GPUs)|
|Number of steps per environment|24|
|_Algorithm (Distillation)_||
|Learning rate|5_×_10<sup>_−_5</sup>|
|Num learning epochs|1|
|Max gradient norm|0.5|
|Loss type|MSE|


