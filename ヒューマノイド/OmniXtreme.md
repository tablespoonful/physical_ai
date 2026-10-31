---
title: "OmniXtreme: Breaking the Generality Barrier in High-Dynamic Humanoid Control"
date: "2026-02-27"
authors: "Yunshen Wang; Shaohang Zhu; Peiyuan Zhi; Yuhan Li; Jiaxin Li; Yong-Lu Li"
url: https://arxiv.org/abs/2602.23843
pdf: https://arxiv.org/pdf/2602.23843
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.23843)** / [論文ページ](https://arxiv.org/abs/2602.23843)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# OmniXtreme: Breaking the Generality Barrier in High-Dynamic Humanoid Control 

Yunshen Wang<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup><sup>_,∗_</sup> , Shaohang Zhu<sup>1</sup><sup>_,_2</sup><sup>_,_4</sup><sup>_,∗_</sup> , Peiyuan Zhi<sup>1</sup><sup>_,_2</sup> , Yuhan Li<sup>1</sup><sup>_,_2</sup><sup>_,_6</sup> , Jiaxin Li<sup>1</sup><sup>_,_2</sup><sup>_,_7</sup> , Yong-Lu Li<sup>3</sup> , Yuchen Xiao<sup>5</sup> , Xingxing Wang<sup>5</sup> , Baoxiong Jia<sup>1</sup><sup>_,_2</sup><sup>_,†_</sup> , Siyuan Huang<sup>1</sup><sup>_,_2</sup><sup>_,†_</sup> 1State Key Laboratory of General Artificial Intelligence, Beijing Institute for General Artificial Intelligence (BIGAI) 

> 2Joint Laboratory of Embodied AI and Humanoid Robots, BIGAI & Unitree Robotics 

> 3Shanghai Jiao Tong University 4University of Science and Technology of China 

> 5Unitree Robotics 6Huazhong University of Science and Technology 7Beijing Institute of Technology 

> _∗_ Equal contribution. _†_ Corresponding authors. Project page: https://extreme-humanoid.github.io/ 


Fig. 1: **Extreme whole-body humanoid control from our unified policy OMNIXTREME.** (a) A quantitative comparison shows that our curated extreme motion libraries occupy substantially more challenging regimes than standard multi-motion benchmarks ( _e.g_ ., Unitree-retargeted LAFAN1). Real-world executions of our unified policy OMNIXTREME demonstrate robust and physically executable extreme behaviors drawn from this motion set, including (b) extreme balance behaviors, (c) rapid contact switching with complex support transitions, (d) high-speed motions with large angular velocities, and (e) diverse whole-body behaviors spanning qualitatively distinct motion styles. 

**_Abstract_ —High-fidelity motion tracking serves as the ultimate litmus test for generalizable, human-level motor skills. However, current policies often hit a “generality barrier”: as motion libraries scale in diversity, tracking fidelity inevitably collapses—especially for real-world deployment of high-dynamic motions. We identify this failure as the result of two compounding factors: the learning bottleneck in scaling multi-motion optimization and the physical executability constraints that arise in realworld actuation. To overcome these, we introduce OMNIXTREME, a scalable framework that decouples general motor skill learning from sim-to-real physical skill refinement. Our approach uses a flow-matching policy with high-capacity architectures to scale representation capacity without the interference-intensive multimotion RL optimization, followed by an actuation-aware refinement phase that ensures robust performance on physical hardware. Extensive experiments demonstrate that OMNIXTREME maintains high-fidelity tracking across diverse, high-difficulty datasets. On real robots, the unified policy successfully executes multiple extreme motions, effectively breaking the long-standing fidelity–scalability trade-off in high-dynamic humanoid control.** 

## I. INTRODUCTION 

We ultimately seek general-purpose humanoids with scalable, human-level whole-body motor skills. A natural and widely used way to study such capability is high-fidelity motion tracking, where a controller must reproduce reference motions accurately while remaining dynamically stable under contacts and disturbances. High-quality tracking is more than an aesthetic goal: it captures whole-body coordination and contact timing that underlie loco-manipulation, expressive interaction, and many downstream core humanoid capabilities [59, 50, 52, 1, 43, 47, 53]. 

Over the past years, learning-based motion tracking has made striking progress: with carefully designed objectives and reinforcement learning, policies can track individual motions with high precision, including highly dynamic behaviors such as dance, flips, and martial arts [57, 28, 14]. More recent work [5, 30, 9, 23, 11, 6, 12, 58, 55, 26] has taken important steps toward multi-motion controllers that cover broader behavior libraries. Yet a recurring pattern persists: when we scale to larger, more heterogeneous motion libraries spanning diverse styles, contact regimes, and timing modes, motion tracking quality tends to degrade. Controllers become conservative and “average,” break on the hardest motions, or prove brittle to the small deviations that inevitably occur in simto-real transfer. The degradation is particularly pronounced in _high-dynamic motions_ , where even small tracking errors can rapidly cascade into catastrophic failures. This long-standing fidelity–scalability trade-off has effectively capped the level of generality achievable in humanoid motor control, particularly in _high-dynamic regimes_ , suggesting a fundamental limitation rather than isolated engineering issues [11, 58, 14, 57]. 

A central question therefore arises: **why is high-fidelity motion tracking so difficult to scale, especially on real humanoid robots?** We argue that this difficulty stems from two compounding barriers that emerge at different stages of the current sim-to-real training pipeline. 

The first barrier is the **learning bottleneck** that arises even in simulation. Several recent works [58, 5, 23, 30, 55, 26, 12, 

11] have begun to explore multi-motion humanoid tracking, aiming to improve scalability beyond single-motion imitation. However, existing approaches remain constrained by both representation and optimization. On the representation side, most approaches rely on relatively simple policy parameterizations, such as MLP actors [58, 5, 23, 55, 26, 12, 11, 46]. When required to map observations to highly heterogeneous action targets arising from diverse behaviors and contact patterns, such parameterizations have been observed to exhibit limited scalability as data diversity increases [33]. On the optimization side, jointly training a unified policy across many motions using reinforcement learning exacerbates gradient interference, often leading to conservative averaging and selective failures on _high-dynamic behaviors_ [12, 11, 9, 30]. Together, these factors cause tracking fidelity to collapse as motion diversity and difficulty increase. 

The second barrier is the **physical executability bottleneck** that emerges at deployment. Even when high-fidelity tracking is achieved in simulation, transferring such behaviors to physical robots remains challenging. In prior humanoid learning pipelines [11, 58, 5, 23, 30, 55, 28, 14, 26, 49], actuation constraints during training are modeled primarily through joint position limits and simple effort bounds. Although these simplifications facilitate learning, they become insufficient in _high-dynamic motions_ , where system behavior is dominated by unmodeled actuator nonlinearities [41], such as torque– speed characteristics and velocity-dependent torque losses, as well as power-related effects, including regenerative power phenomena, leading to rapid degradation of execution stability. As a result, fidelity that appears scalable in simulation may still fail to materialize on real robots. 

Motivated by this analysis, we propose OMNIXTREME, a scalable training framework designed to explicitly address both barriers, with the goal of enabling a single policy to robustly control diverse and _high-dynamic_ humanoid behaviors. To overcome the learning bottleneck, OMNIXTREME adopts a flow matching policy and performs specialist-to-unified generative pretraining via behavior cloning from a collection of motion specialists. This design decouples representation learning from optimization, scaling expressive capacity through a high-capacity generative policy while avoiding interferenceheavy multi-motion reinforcement learning. 

To overcome the physical executability bottleneck, OMNIXTREME introduces a residual reinforcement learning posttraining refinement for execution under realistic actuation constraints, which become particularly critical in _high-dynamic motions_ . Rather than relearning motion tracking, this stage refines the pretrained policy to respect real-world actuation constraints through actuation-aware modeling, refined domain randomization, and explicit penalties on power-related effects. This targeted refinement ensures that the scaled tracking policy remains physically executable under realistic hardware dynamics. 

We validate OMNIXTREME through extensive simulation and real-robot evaluations on increasingly diverse and highdynamic motion libraries. Beyond standard multi-motion 

benchmarks, we curate a set of extreme motions characterized by high speed, frequent contact transitions, and tight timing constraints, and evaluate OMNIXTREME across this full spectrum. As shown in Fig. 1, OMNIXTREME successfully executes a wide range of extreme behaviors on a Unitree G1 humanoid robot, including flips, acrobatics, and breakdancing where even minor deviations can rapidly cascade into failure. Together, these results constitute a stringent scalability stress test and challenge the prevailing assumption that tracking fidelity must collapse as motion diversity and difficulty increase. Overall, our contributions are fourfold: 

- 1) We present OMNIXTREME, a scalable training framework for high-fidelity humanoid motion tracking that explicitly tackles the fundamental scalability challenge in _highdynamic_ humanoid control. 

- 2) We introduce a specialist-to-unified generative pretraining stage based on flow matching, enabling a unified policy to scale across heterogeneous and high-dynamic motions. 

- 3) We propose an actuation-aware residual reinforcement learning post-training stage that refines the pretrained policy under realistic actuation constraints, ensuring physical executability. 

- 4) We demonstrate through extensive simulation and realworld experiments that OMNIXTREME enables a single unified policy to robustly execute diverse and extreme motions, addressing the conventional fidelity–scalability trade-off, especially for high-dynamic motions. 

## II. RELATED WORK 

## _A. Humanoid Whole-body Control and General Tracking_ 

Recent research in humanoid whole-body control has demonstrated remarkable progress across diverse skills [62, 19, 15, 57, 36], including dance, fall recovery, and parkour. However, achieving both high-fidelity motion tracking and scalability across large and diverse motion libraries remains an open challenge. Frameworks such as ASAP [14] and BeyondMimic [28] demonstrate strong performance in highquality imitation of individual motion clips, yet extending these approaches to increasingly large motion sets introduces additional optimization complexity. On the other hand, large-scale RL-based trackers including OmniH2O [11], ExBody2 [23], and GMT [5] show promising scalability, though maintaining precise motion fidelity under extensive skill coverage remains challenging. This tension is often reflected as a fidelity–scalability trade-off in practice. To address this issue, OMNIXTREME introduces a generative action representation and a specialist-to-unified optimization framework, enabling scalable learning while maintaining strong tracking precision across high-dynamic motion datasets. 

## _B. Diffusion and Flow-based Action Modeling for Robotic Planning and Control_ 

Diffusion and flow-based models [42, 16, 34, 38, 29, 33, 45, 44, 8] have shown strong capability in robot learning, leveraging iterative refinement and stochastic sampling to enhance robustness and diversity in robotic control and planning [33]. 

While early research focused on high-level trajectory planning or low-frequency visuomotor tasks [22, 18, 8, 48, 4], DiffuseLoco [20] takes a step to apply them to high-frequency quadruped control. To further enhance expressivity and robustness, recent works like Policy Decorator [54] and ResiP [2] introduce residual policy learning on arm-based robots, coupling frozen base models with refinement layers to handle covariate shift and precision bottlenecks in long-horizon assembly. However, given the vast skill space and inherent instability that distinguish humanoids from quadrupeds and manipulators, current effort such as BeyondMimic [28] focuses on guided control interfaces rather than the scalability and high-speed agility essential for high-dynamic humanoid motion tracking. Different from previous work, OMNIXTREME introduces a comprehensive training pipeline involving DAgger-based Flow Matching pretraining and residual post-training that pushes the boundaries of low-level scalability and agility, far surpassing the motion diversity and dynamic performance of previous approaches. 

## _C. Actuation-aware Agile Robotic Control_ 

Achieving agility remains a frontier in robotics [25, 27, 13, 24, 21, 32, 56, 17, 7, 61, 62, 49]. ACRL [41] leveraged actuator-constrained RL for high-speed quadrupedal locomotion, while Closing the Reality Gap [60] utilized a currentto-torque calibration and actuator dynamics modeling for dexterous five-finger manipulation. Despite these advancements in other morphologies, learning agile and actuation-aware control policies for humanoids remains an underexplored area. OMNIXTREME addresses this gap by integrating physics-informed motor modeling and actuation regularization, pushing the boundaries of agile humanoid performance under realistic hardware constraints. 

## III. METHODOLOGY 

In this section, we present OMNIXTREME, a two-stage training framework for scalable, high-fidelity humanoid motor skill learning. The **Scalable Flow-based Pretraining** stage focuses on high-fidelity motion imitation and representation capacity acquisition. Specifically, we distill diverse expert behaviors from a collection of motion-specific expert policies into a single unified base policy using flow matching [29]. This generative pretraining stage establishes a shared tracking prior across heterogeneous motions, without relying on interferenceprone joint multi-motion reinforcement learning. 

To address the gap between simulation and real-world execution, we further introduce an **Actuation-Aware PostTraining** stage based on residual reinforcement learning. Rather than relearning motion tracking, a residual policy is trained to produce corrective actions that complement the pretrained flow matching base policy. This stage aligns the overall system with real-world actuation constraints while introducing substantially more aggressive domain randomization. Through this targeted refinement, the residual policy adapts the pretrained tracking behavior to realistic hardware 


Fig. 2: **Overview of the OMNIXTREME.** (a) Pretraining phase: A unified base policy is trained via DAgger-based Flow Matching to aggregate diverse motion priors from different motion tracking experts. (b) Post-training phase: The base policy is frozen while a residual policy is optimized under stringent motor constraints, extensive domain randomization, and power-safety regularization to bridge the sim-to-real gap. (c) Onboard deployment: The whole inference pipeline is real-time and executed entirely onboard, facilitating robust and agile control in physical environments. 

dynamics, improving physical executability and deployment robustness. 

## _A. Scalable Flow-based Policy Pretraining_ 

_1) Problem Formulation:_ During the pretraining phase, we learn a flow-matching robot policy with Dataset Aggregation (DAgger)-based distillation [39, 45]. Specifically, we consider the observation space of _o_ = _{p, c, h}_ covering: (i) robot proprioception _p_ , including joint positions, velocities, base angular velocities, and previous actions; (ii) command _c_ consisting of 6D torso orientation differences along with target joint positions and velocities from the reference motion; and (iii) history information _h_ encompassing past proprioceptive states. Given a reference motion dataset _M_ = _{mi}_<sup>_M_</sup> _i_ =1<sup>,our</sup> goal is to first learn expert policies Π<sup>_i_</sup> expert<sup>=</sup><sup>_{π_</sup> expert<sup>_i_(</sup><sup>_a|o_)</sup><sup>_}_</sup> _i_<sup>_M_</sup> =1 for each reference motion, then distilling it into a flow-based general policy _πθ_ ( _a|o_ ). 

_2) Expert Policy Learning:_ For expert policy training, we draw the reference motion dataset _M_ from a combination of Unitree-retargeted LAFAN1 (LAFAN1) dataset [10], AMASS [31], MimicKit [35], and the Reallusion motion library [37], covering both diverse behavioral patterns and high-dynamic maneuvers. All reference motions are first retargeted to the Unitree G1 humanoid robot using GMR [55, 3]. Subsequently, we train each expert policy _π_ expert<sup>_k_on the specific</sup> motion _mk_ via Proximal Policy Optimization (PPO) [40]. 

_3) Flow-matching Policy Learning:_ We learn the flowmatching robot policy with DAgger by first rolling out the current flow-based policy _πθ_ ( _a|o_ ) in the simulator and collecting a trajectory of visited states _{o_ 1 _, · · · , oN }_ given reference motion dataset _M_ . For each visited state _o_ , we obtain the expert action _a_ expert by querying the corresponding expert policy. The flow-based model then learn to recover the expert action _a_ expert from noised action by optimizing: 


where _at_ = (1 _− t_ ) _a_ expert + _tϵ_ is the noised action interpolated between expert action _a_ expert and random noise _ϵ ∼N_ (0 _, I_ ) depending on flow timestep _t ∈_ [0 _,_ 1]. This objective learns a velocity field _vθ_ ( _at, t, o_ ) to predict the target velocity _u_ = _ϵ − a_ expert, learning the denoising directions at each flow timestep [29]. During the optimization process, the timestep _t_ is sampled from a Beta distribution, _t ∼_ Beta( _α, β_ ), to focus the learning process on specific regions of the probability path, thereby enhancing convergence and trajectory refinement. With the velocity field _vθ_ , we can generate action _a_ 0 from random noise _a_ 1 _∼N_ (0 _, I_ ) by integrating _vθ_ from _t_ = 1 to _t_ = 0 via the foward Euler rule: 


where _D_ is the number of integration or denoising steps controlling the approximation accuracy. By iteratively rolling out trajectories and supervising them with expert actions using Eq. (1), we learn _πθ_ as a general policy to map the current observation to appropriate actions. The full training procedure is illustrated in Fig. 2(a) and detailed in Alg. 1. 

_4) Fidelity-Preserving Randomization and Noise:_ To maintain a high degree of motion expressivity while ensuring physical stability, we implement a conservative randomization and noise strategy, as detailed in Tab. I, during both the teacher training and pretraining phases. By utilizing moderate noise levels and domain randomization, we prevent the performance collapse often induced by excessive stochasticity. This ensures that the agent accurately captures the underlying physical dynamics, resulting in a flow matching policy that possesses foundational sim-to-real robustness and the predictive certainty necessary for real-world deployment. 

## _B. Actuation-Aware Post-training Phase_ 

_1) Residual Policy Modeling:_ While the pretrained flow matching base policy provides a robust and unified behavioral foundation, it encounters performance gaps when facing realworld physics. To better account for this gap and enable smooth sim-to-real transfer, we propose a post-training refinement stage using a lightweight MLP-based residual-corrective learning. Specifically, we learn the residual correction policy _πϕ_ on top of the frozen pretrained policy _πθ_ by generating the refined action _a_ = _a_ flow + _a_ res and supervising it with cumulative rewards via PPO, detailed in the Appendix. 

In particular, the observation space for the residual actor and critic incorporates robot proprioception, motion command, 

TABLE I: Configurations for noise, domain randomization, and termination thresholds during pre-training and post-training phases. Here _±x_ denotes [ _−x, x_ ]. 

**Algorithm 1** Flow-based Pretraining and Inference 

- 1: **Training: Distill Flow Matching Policy with DAgger** 2: **Input:** Teacher policy set _πteacher_ , Flow matching policy _πθ_ , Motion dataset _M_ , Replay buffer _D_ 

|**Parameter Item**|**Moderate**|**Aggressive**||_πθ_, Motion dataset _M_, Replay buffer _D_|
|---|---|---|---|---|
|_Noise and Domain Rando_|_mization_||3:|**repeat**<br><br>|
|Joint Position (rad)|_±_0_._01<br>|_±_0_._01<br>|4:|_D ←∅_<br>_▷_On-policy reset: Clear buffer for the new|
|Joint Velocity (rad/s)<br>|_±_0_._5<br>|_±_0_._5<br>||iteration|
|Angular Velocity (rad/s)|_±_0_._2|_±_0_._2|5|Samlemotion_m ∼M_andselectteacher_π_<sup>_m_</sup><br>|
|Torso 6D Rotation (rad)|_±_0_._05|_±_0_._05|:<br>|p       <br>_teacher_<br>|
|Base CoM Offset (m)|_x_: _±_0_._025_, y, z_: _±_|0_._05_x_: _±_0_._025_, y, z_: _±_0_._05|6:|Rollout _πθ_ in simulator conditioned on _m_ to obtain|
|Static Friction|[0_._3_,_1_._6]<br>|[0_._3_,_1_._6]<br>||states _s_1:_T_|
|Dynamic Friction|[0_._3_,_1_._2]<br>|[0_._3_,_1_._2]<br>|7:|**for** _t_= 1 to _T_ **do**|
|Action Delay (ms)|[0_,_15]|[**5**_,_**10**]|8|_a←_<sup>_m_</sup><br><sup>(</sup><sup>_s_)</sup><br>_▷_Exertlabelin|
|Coefficient of Restitution|None|[**0**_._**0**_,_**0**_._**5**]|:|_expert,t π_<br>_teacher_<sup>_t_</sup><br>p g<br> <br>|
|Default Calib. (rad)|_±_0_._01|_±_0_._01|9:|_D ←D ∪{_(_st, m, aexpert,t_)_}_<br>_▷_Aggregate data<br>|
|Init. Pose (rad)|_±_0_._1|_±_**0**_._**15**|10:|**end for**|
|Init. Lin. Vel. (m/s)<br>|_xy_: _±_0_._5_, z_: _±_0_._2<br>|**xy** : _±_**0**_._**75**_,_**z** : _±_**0**_._**3**<br>|11:|**Flow Matching Optimization:**|
|Init. Ang. Vel. (rad/s)|_RP_: _±_0_._52_, Y_: _±_|0_._78 **RP** : _±_**0**_._**78**_,_**Y** : _±_**1**_._**17**|12:|**for**eachradientste**do**|
|Push Frequency (s)|1_._0_−_3_._0|1_._0_−_3_._0||g p <br>|
|Push Lin. Vel. (m/s)|_xy_: _±_0_._5_, z_: _±_0_._2|_xy_: _±_0_._5_, z_: _±_0_._2|13:|Sample (_s, aexpert_)_∼D_<br>|
|Push Ang. Vel. (rad/s)|_RP_: _±_0_._52_, Y_: _±_|0_._78 _RP_: _±_0_._52_, Y_: _±_0_._78|14:|Sample _t ∼_Beta(_α, β_) and _ϵ ∼N_(0_, I_)|
|Terrain Surface / Step (m)|None|[**0**_,_**0**_._**01**]_/_**0**_._**01**|15:|Construct probability path:_xt_ = (1_−t_)_aexpert_+_tϵ_|
|_Termination Thresholds_|||16:|Compute target velocity: _ut_ =_ϵ −aexpert_|
|Torso Pos. Z / Ori. Error|0_._25m / 0_._8rad|**0**_._**375m**_/_**1**_._**2rad**|17:|Update _θ_ using gradient descent on _∥vθ_(_xt, t, c_)_−_|
|End-Effector Z-Error (m)|0_._25|**0**_._**375**||<br>_ut∥_<sup>2</sup>|
||||18:|**end for**|
|and the current bas|e action _a_flow.|Within the proprioceptive|19:|**until** convergence|


and the current base action _a_ flow. Within the proprioceptive state, the residual policy observes the previous refined action, whereas the flow matching base policy remains conditioned on the previous flow-based action. 

20: **Inference: Action Sampling with Euler Integration** 21: **Input:** Trained velocity field _vθ_ , Concatenated condition _c_ , Number of steps _N_ 22: Set step size ∆ _t_ = 1 _/N_ 23: Initialize _x_ 1 _∼N_ (0 _, I_ ) _▷_ Start from Gaussian noise 24: **for** _k_ = 0 to _N −_ 1 **do** 25: _t_ = 1 _− k ·_ ∆ _t ▷_ Reverse time from 1 to 0 26: _vt ← vθ_ ( _xt, t, c_ ) 27: _xt−_ ∆ _t ← xt − vt ·_ ∆ _t ▷_ Reverse-time Euler step to obtain _x_ 0 28: **end for** 29: **return** _a_ = _x_ 0 _▷_ Execute final reconstructed action 

_2) Actuation-aware Physical Constraint Modeling:_ To explicitly account for real-world actuation effects, we train the residual policy using environments that incorporate realistic actuation-aware physical constraints and domain randomization, as shown in Fig. 2(b). The actuation-aware physical modeling is detailed as follows: 

_a) Aggressive Domain Randomization:_ We substantially increase the range for domain randomization by up to 50% on common domain randomization settings, including initial pose noise, force disturbances magnitude, angular velocity, _etc_ ., as detailed in Tab. I. We randomize the terrain by adding surface noise and placing vertical steps randomly in the scene. Crucially, we relax the termination thresholds by 1.5 _×_ from their base values ( _e.g_ ., orientation error from 0.8 to 1.2 rad). This relaxation allows the residual policy to explore and correct for large-deviation but recoverable states that would otherwise be prematurely terminated. 

braking events for each joint: 


where _Pj_ , _P_ db denotes power for joint _j_ and the deadband threshold, respectively. _K_ is a normalizing constant. In practice, this term is selectively applied to the knee joints in the context of high-dynamic motions( _e.g_ ., backflips), as these joints are particularly prone to high braking loads during impacts and recovery phases. 

_b) Power-Safe Actuation Regularization:_ In practice, highly dynamic motions can induce large transient braking loads that are not explicitly regulated in standard training pipelines. To address the issue, we introduce an explicit penalty on excessive negative joint mechanical power to mitigate aggressive motor braking that can trigger overcurrent protection or thermal stress on real robots. Specifically, we use the instantaneous mechanical power _P_ = _τ · ω_ calculated from the applied joint torque _τ_ and angular velocity _ω_ as a critical policy for actuator safety. We penalize the negative power beyond a predefined deadband to suppress large regenerative 

_c) Actuation-Aware Torque–Speed Constraints:_ A major source of sim-to-real discrepancy stems from the oversimplification of actuator modeling, whereas standard torque clipping techniques neglect velocity-dependent constraints imposed by back-electromotive force and physical power limits. This omission leads to a significant sim-to-real gap when performing 

high-dynamic motions. To bridge this gap, we integrate a realistic torque-speed operating envelope directly into the simulation, dynamically deriving torque limits based on the instantaneous alignment of torque and angular velocity: 


The admissible torque is then defined as a monotonically decreasing function of joint velocity magnitude: 


The commanded torque is finally clipped to this admissible range before being applied to the joint, which ensures that the simulator never samples torque commands that are physically unattainable for the real actuators. 

In addition to torque-speed limits, we further model actuator-level internal losses through a nonlinear friction term applied after torque clipping, 


The smoothed Coulomb component captures the transition from static to kinetic friction, while the viscous term accounts for velocity-dependent dissipation and provides additional damping. The parameters _µs_ , _v_ act, and _µd_ are constants. 

Overall, this structured refinement stage yields controllers that are simultaneously safer, more robust to large disturbances, and more faithfully aligned with real-world actuator dynamics, thereby enabling reliable deployment on robots. 

## _C. Real World Deployment_ 

The integrated real-world deployment pipeline is illustrated in Fig. 2(c). In the deployment phase, we leverage the pelvis IMU as the primary orientation source and compute the torso rotation through Forward Kinematics (FK). To ensure minimal control latency, the entire computational pipeline—including FK-based state estimation, the base flow matching policy, and the residual policy—is optimized and executed via TensorRT. This integrated pipeline achieves an end-to-end inference latency of about 10ms on the Unitree G1’s onboard Orin NX. Such optimization enables the robot to execute high-quality motion tracking at a consistent 50Hz frequency in complex physical environments. 

## IV. EXPERIMENTS 

We present extensive experiments in simulation and on physical robots to evaluate the scalability of our proposed OMNIXTREME system as motion libraries grow in diversity and difficulty. Our experiments are organized around the following key questions: 

**Q1: Scalable high-fidelity tracking.** Compared to prior multimotion baselines, can our approach maintain high-fidelity 

tracking at scale, both in simulation and on real robots, without collapsing under representation and optimization challenges? **Q2: Fidelity–scalability trade-off (OMNIXTREME v.s. from-scratch RL controllers).** As motion diversity and difficulty increase, how does tracking performance degrade for from-scratch multi-motion reinforcement learning controllers, and to what extent can our approach extend the scalability frontier? 

**Q3: Capacity scaling with flow-based (OMNIXTREME v.s. MLP-based controllers).** Does increasing model capacity improve large-scale multi-motion tracking performance, and does generative pretraining via flow matching enable stronger and more stable scaling behavior than conventional MLPbased motion tracking controllers? 

**Q4: Real-world executability and robustness.** How do aggressive domain randomization, actuation-aware modeling, and power-aware safety mechanisms individually and jointly affect sim-to-real transfer and real-world execution success? **Q5: Qualitative whole-body capability.** Beyond scalar tracking metrics, can OMNIXTREME demonstrate agile and versatile whole-body behaviors across diverse motion styles and dynamic contact patterns? 

Together, these questions probe the scalability and robustness of OMNIXTREME by disentangling the roles of generative pretraining for representation and capacity scaling, and residual post-training for real-world executability. 

## _A. Experimental Setup_ 

_1) Motion Libraries:_ We construct our motion libraries following a two-tier design. First, we use the full LAFAN1 [10], which has been widely adopted in prior multi-motion tracking work and serves as a standard benchmark for evaluating scalability under stylistic and temporal diversity. 

Second, to evaluate and push the limit of extreme humanoid motions, we curate about 60 highly challenging motions selected from LAFAN1 [10], AMASS [31], MimicKit [35], and Reallusion [37]. These motions exhibit substantially higher dynamic intensity, frequent contact transitions, and tight timing constraints, as shown in Fig. 1(a). We collectively refer to this curated set as the XtremeMotion dataset. 

Together, LAFAN1 and XtremeMotion form a motion library that spans both standard multi-motion benchmarks and extreme behaviors that probe the limits of fidelity, robustness, and real-world executability. 

_2) Baselines:_ We compare against two families of strong baselines designed for multi-motion tracking. **(a) Specialist-to-Unified MLP Distillation.** This class of methods [58] first trains per-motion (or per-cluster) specialist policies and then distills them into a single unified MLP tracking policy. Relying on supervised distillation, they benefit from relatively stable and straightforward optimization, but are limited by the representational capacity of the MLP policy. 

**(b) From-scratch Multi-motion Reinforcement Learning.** This class [11, 5, 23, 58, 30, 28] directly trains a single unified tracking policy from scratch using reinforcement learning across all motions, but often suffers from gradient interference 

and conservative averaging as motion diversity and difficulty increase. 

## _B. Evaluation Metrics_ 

The policy is evaluated through simulated rollouts of motion tracking to extract performance metrics. The primary metric is the **success rate (Succ)** , where an episode is deemed unsuccessful if the humanoid deviates beyond a predefined threshold from the reference motion or becomes unstable. We additionally report the **root-relative mean per-joint position error (MPJPE)** (mm), as well as discrepancies in jointspace **velocity** (∆vel) and **acceleration** (∆acc), to quantify kinematic accuracy and physical fidelity. 

On physical robots, we evaluate performance using deployment-oriented metrics, including **skill-level success rates** and qualitative assessments of motion fidelity for highdynamic behaviors. 

## _C. Scalable high-fidelity tracking (Q1)_ 

In this section, we study whether high-fidelity humanoid motion tracking can be preserved by OMNIXTREME as motion libraries scale in diversity and difficulty. We compare OMNIXTREME with specialist-to-unified MLP distillation and fromscratch multi-motion reinforcement learning under matched model capacity and identical training data. All methods are trained on the same combined motion library (LAFAN1 + XtremeMotion) and evaluated on three test sets: the full motion library, the high-dynamic XtremeMotion subset, and an unseen motion set (randomly sampled from retargeted AMASS). 

**Simulation.** As summarized in Tab. II, **OMNIXTREME consistently outperforms both baselines across all simulation metrics.** The gap becomes substantially larger on XtremeMotion and unseen motions, where baseline methods exhibit reduced success rates and increased tracking errors as motion difficulty increases. This indicates that OMNIXTREME preserves tracking fidelity as motion diversity and difficulty scale, rather than degrading under increased complexity. 

**Real world.** We further deploy OMNIXTREME on a Unitree G1 humanoid robot using motions drawn from XtremeMotion. For clarity of presentation, motions are grouped into representative skill categories based on shared dynamic structure and contact patterns. A trial is considered successful if the motion is executed without manual intervention or safety-triggered termination. As shown in Tab. III, across 157 real-world trials spanning 24 distinct high-dynamic motions, **OMNIXTREME achieves consistently high success rates across diverse skill categories** , including flips, acrobatics, breakdancing, and martial-arts-style motions. These results demonstrate that the scalability gains observed in simulation translate to robust and physically executable behaviors on real hardware. 

## _D. Fidelity–scalability trade-off (Q2)_ 

To characterize the fidelity–scalability trade-off in multimotion tracking, we progressively scale motion diversity by training on an expanding set of motions drawn from XtremeMotion, and analyze how different training paradigms respond under the same evaluation protocol. 


Fig. 3: **Fidelity–scalability trade-off.** Tracking success rate as we progressively scale motion diversity and difficulty, while evaluating all policies on a fixed set of the first 10 motions. 


Fig. 4: **Capacity scaling.** Tracking fidelity and robustness as a function of model capacity. OMNIXTREME benefit more strongly from scaling, while conventional MLP controllers saturate earlier. 

Under this controlled scaling regime, **from-scratch multimotion reinforcement learning exhibits earlier and more pronounced performance degradation as scale increases, whereas OMNIXTREME maintains higher tracking robustness over a broader scaling range.** As shown in Fig. 3, from-scratch multi-motion RL [28] exhibits a characteristic degradation pattern as motion diversity increases: tracking precision deteriorates steadily, followed by a sharp loss of robustness beyond a critical scale. These results indicate that the observed fidelity–scalability trade-off is not inherent, but can be substantially alleviated by a more scalable training paradigm. 

## _E. Capacity scaling (Q3)_ 

We next examine whether increasing model capacity further improves multi-motion tracking performance, and whether our generative policy exhibits stronger scaling behavior than conventional MLP-based controllers [33]. We train a family of models with increasing capacity (e.g., width/depth or Transformer hidden size and layers) under the same data and training recipe. Fig. 4 reports tracking fidelity and robustness as a function of model capacity. We observe that **additional capacity translates more directly into improved tracking quality for our flow matching policies, whereas MLPbased policies show weaker gains.** These results suggest that representational scaling is a practical lever for extending multimotion tracking fidelity when paired with a scalable training paradigm. 

## _F. Real-world executability and robustness (Q4)_ 

We analyze the contribution of different post-training mechanisms to sim-to-real transfer by incrementally enabling them 

TABLE II: **Scalable high-fidelity motion tracking under diverse motion sets.** OMNIXTREME consistently achieves lower kinematic errors and higher success rates than baselines, particularly on high-dynamic and unseen motions. 

|Method||LaFAN1+X|tremeMot|ion||Xtrem|eMotion||Unsee|n Motions|
|---|---|---|---|---|---|---|---|---|---|---|
||MPJPE|_↓_<br>∆vel _↓_|∆acc _↓_|Succ.(%) _↑_|MPJPE _↓_|∆vel _↓_|∆acc _↓_|Succ.(%) _↑_|MPJPE _↓_|Succ.(%) _↑_|
|From-scratch RL [28]|47.95|10.03|3.27|82.95|54.19|14.04|4.04|79.45|56.87|85.29|
|Specialist_→_Unified MLP [58]|33.35|6.70|2.11|94.91|43.43|11.38|2.51|89.22|58.94|85.95|
|**OmniXtreme (Pretrain only)**|32.65|6.34|**2.04**|97.17|37.11|10.46|**2.39**|95.16|56.25|89.23|
|**OmniXtreme (Pretrain + Post-train)**|**30.93**|**6.19**|2.13|**98.54**|**36.17**|**9.94**|2.58|**95.64**|**56.05**|**89.54**|
|ABLE III: **Real-world evaluation**<br>**1.**We evaluate OMNIXTREME on<br>awn from the XtremeMotion moti<br>Skill<br>#Motions<br>A|**of OMN**<br>physical h<br>on library<br>ttempts<br>|**IXTREME **<br>ardware us<br>.<br>Success (%|**on Unit**<br>ing moti<br>)_↑_|**ree**<br>ons<br>Fli||||Acrobatic|||
|Flip<br>7<br>Handspring<br>5|55<br>35|96.36<br>88.57||Brea|kdanc|||Martial Arts|||


TABLE III: **Real-world evaluation of OMNIXTREME on Unitree G1.** We evaluate OMNIXTREME on physical hardware using motions drawn from the XtremeMotion motion library. 

|Skill|#Motions|Attempts|Success (%)_↑_|
|---|---|---|---|
|Flip|7|55|96.36|
|Handspring|5|35|88.57|
|Acrobatics|4|15|80.00|
|Breakdance|5|22|86.36|
|Martial arts|3|30|93.33|
|**Total**|**24**|**157**|**91.08**|


Fig. 5: **Qualitative results.** Representative real-world rollouts produced by OMNIXTREME, executing qualitatively distinct whole-body motions across diverse styles and contact patterns, including flips, acrobatics, breakdance, and martial-arts behaviors. The results illustrate stable and coordinated execution under rapid contact transitions and timing-sensitive phases on physical hardware. 

TABLE IV: **Ablation of post-training mechanisms.** Real-world executability of different skills under incremental post-training mechanisms. **None** : base pretrained policy only; **MC** : motor constraints; **ADR** : aggressive domain randomization; **PS** : power-safety regularization (overcurrent / regenerative protection). ✓: stable execution; _△_ : unstable or inconsistent execution; _×_ : consistent failure; ⊖: failures primarily associated with power-safety protection, such as overcurrent or excessive regenerative braking. 

motion styles and contact patterns, beyond what is captured by scalar tracking metrics. We visualize representative rollouts spanning stylistic motions from XtremeMotion. Fig. 5 highlights that OMNIXTREME can track qualitatively different motions with coherent whole-body coordination, complement the quantitative metrics in Q1-Q4 and illustrate the breadth of behaviors enabled by scalable generative pretraining and actuation-aware refinement. Please refer to the _Supp._ for additional qualitative results, including video demonstrations. 

|Skill|None|+MC|+MC+ADR|Full (+MC+ADR+PS)|
|---|---|---|---|---|
|Flip|_△_|✓|✓|✓|
|Breakdance|_△_|_△_|✓|✓|
|Acrobatics|_×_|_△_|⊖|✓|


and evaluating real-world execution at the skill level. Tab. IV summarizes the ablation results. 

In summary, **different classes of high-dynamic motions exhibit distinct failure modes, and each execution-oriented mechanism addresses a complementary aspect of realworld executability** . For highly impulsive motions such as flips, enforcing actuator torque-speed constraints is sufficient to enable stable execution, as respecting motor envelopes prevents immediate hardware-level violations. Contact-rich skills such as breakdance and acrobatic motions remain unstable under motor constraints alone, but benefit substantially from aggressive domain randomization, which improves robustness to timing-sensitive contact perturbations. Motions involving high-speed impact buffering, such as acrobatic landings, remain challenging even with aggressive domain randomization, power-safety regularization is critical for these skills, as it mitigates failures caused by excessive transient braking loads and unsafe energy absorption during high-impact contacts. Together, these results show that reliable real-world execution emerges from the combined effects of actuation-aware modeling, robustness-oriented randomization, and energy-aware safety constraints. 

## V. CONCLUSION 

We presented OMNIXTREME, a two-stage framework for scalable high-fidelity humanoid motion tracking in highdynamic regimes. By combining specialist-to-unified flowbased pretraining with actuation-aware residual reinforcement learning, OMNIXTREME mitigates both the learning bottleneck at scale and the physical executability bottleneck at sim-to-real deployment. Extensive simulation results show that OMNIXTREME preserves tracking fidelity substantially deeper into motion diversity than other baselines, and realrobot experiments demonstrate reliable execution of diverse extreme behaviors with a single unified policy, breaking the conventional fidelity–scalability trade-off. 

For future research, jointly scaling data diversity and model capacity will be essential for enhancing the generalization of whole-body humanoid motor skills. As learning-based controllers are pushed toward more dynamic and hardwareconstrained regimes, actuation-aware modeling becomes a critical component of the learning pipeline. By incorporating high-fidelity actuation characteristics—such as current, power, torque, and speed-dependent constraints—researchers can further bridge the sim-to-real gap, ensuring that learned behaviors translate seamlessly to physical humanoid robots. 

## _G. Qualitative results on extreme motions (Q5)_ 

Finally, we provide qualitative evidence that OMNIXTREME can exhibit agile and versatile whole-body skills across distinct 

ACKNOWLEDGMENTS 

REFERENCES 

Changliu Liu, and Guanya Shi. Agile but safe: Learning collision-free high-speed legged locomotion. In _Robotics: Science and Systems (RSS)_ , 2024. 

- [1] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 

- [2] Lars Ankile, Anthony Simeonov, Idan Shenfeld, Marcel Torne, and Pulkit Agrawal. From imitation to refinementresidual rl for precise assembly. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 01–08. IEEE, 2025. 

- [3] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [4] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained image-editing diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 

- [5] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [6] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive wholebody control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 

- [7] Xuxin Cheng, Kexin Shi, Ananye Agarwal, and Deepak Pathak. Extreme parkour with legged robots. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450. IEEE, 2024. 

- [8] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _International Journal of Robotics Research (IJRR)_ , page 02783649241273668, 2023. 

- [9] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [10] Felix G Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher J Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4), 2020. 

- [11] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [12] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning humanto-humanoid real-time whole-body teleoperation. _arXiv preprint arXiv:2403.04436_ , 2024. 

- [13] Tairan He, Chong Zhang, Wenli Xiao, Guanqi He, 

- [14] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [15] Xialin He, Runpei Dong, Zixuan Chen, and Saurabh Gupta. Learning getting-up policies for real-world humanoid robots. _arXiv preprint arXiv:2502.12152_ , 2025. 

- [16] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , 33: 6840–6851, 2020. 

- [17] David Hoeller, Nikita Rudin, Dhionis Sako, and Marco Hutter. Anymal parkour: Learning agile navigation for quadrupedal robots. _Science Robotics_ , 9(88):eadi7566, 2024. 

- [18] Siyuan Huang, Zan Wang, Puhao Li, Baoxiong Jia, Tengyu Liu, Yixin Zhu, Wei Liang, and Song-Chun Zhu. Diffusion-based generation, optimization, and planning in 3d scenes. In _Proceedings of Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 

- [19] Tao Huang, Junli Ren, Huayi Wang, Zirui Wang, Qingwei Ben, Muning Wen, Xiao Chen, Jianan Li, and Jiangmiao Pang. Learning humanoid standingup control across diverse postures. _arXiv preprint arXiv:2502.08378_ , 2025. 

- [20] Xiaoyu Huang, Yufeng Chi, Ruofeng Wang, Zhongyu Li, Xue Bin Peng, Sophia Shao, Borivoje Nikolic, and Koushil Sreenath. Diffuseloco: Real-time legged locomotion control with diffusion from offline datasets, 2024. URL https://arxiv.org/abs/2404.19264. 

- [21] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. 

- [22] Michael Janner, Yilun Du, Joshua B Tenenbaum, and Sergey Levine. Planning with diffusion for flexible behavior synthesis. _arXiv preprint arXiv:2205.09991_ , 2022. 

- [23] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- [24] Donghyun Kim, Jared Di Carlo, Benjamin Katz, Gerardo Bledt, and Sangbae Kim. Highly dynamic quadruped locomotion via whole-body impulse control and model predictive control. _arXiv preprint arXiv:1909.06586_ , 2019. 

- [25] Hyeongjun Kim, Hyunsik Oh, Jeongsoo Park, Yunho Kim, Donghoon Youm, Moonkyu Jung, Minho Lee, and Jemin Hwangbo. High-speed control and navigation for quadrupedal robots on complex and discrete terrain. 

_Science Robotics_ , 10(102):eads6192, 2025. 

- [26] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei Liang, Yixin Zhu, and Siyuan Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. In _Conference on Robot Learning (CoRL)_ , 2025. 

- [27] Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control. _International Journal of Robotics Research (IJRR)_ , 44(5):840–888, 2025. 

- [28] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [29] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _Proceedings of International Conference on Learning Representations (ICLR)_ , 2023. 

- [30] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Casta˜neda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi Fan, and Yuke Zhu. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [31] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of International Conference on Computer Vision (ICCV)_ , 2019. 

- [32] Gabriel B Margolis, Ge Yang, Kartik Paigwar, Tao Chen, and Pulkit Agrawal. Rapid locomotion via reinforcement learning. _International Journal of Robotics Research (IJRR)_ , 43(4):572–587, 2024. 

- [33] Chaoyi Pan, Giri Anantharaman, Nai-Chieh Huang, Claire Jin, Daniel Pfrommer, Chenyang Yuan, Frank Permenter, Guannan Qu, Nicholas Boffi, Guanya Shi, et al. Much ado about noising: Dispelling the myths of generative robotic control. _arXiv preprint arXiv:2512.01809_ , 2025. 

- [34] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of International Conference on Computer Vision (ICCV)_ , 2023. 

- [35] Xue Bin Peng. Mimickit: A reinforcement learning framework for motion imitation and control. _arXiv preprint arXiv:2510.13794_ , 2025. 

- [36] Ilija Radosavovic, Sarthak Kamat, Trevor Darrell, and Jitendra Malik. Learning humanoid locomotion over challenging terrain. _arXiv preprint arXiv:2410.03654_ , 2024. 

- [37] Reallusion. 3d animation and 2d cartoons made simple, 2022. http://www.reallusion.com. 

- [38] Robin Rombach, Andreas Blattmann, Dominik Lorenz, 

Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _Proceedings of Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 

- [39] St´ephane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _International Conference on Artificial Intelligence and Statistics (AISTATS)_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- [40] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [41] Young-Ha Shin, Tae-Gyu Song, Gwanghyeon Ji, and Hae-Won Park. Actuator-constrained reinforcement learning for high-speed quadrupedal locomotion. _arXiv preprint arXiv:2312.17507_ , 2023. 

- [42] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 

- [43] Zhi Su, Bike Zhang, Nima Rahmanian, Yuman Gao, Qiayuan Liao, Caitlin Regan, Koushil Sreenath, and S Shankar Sastry. Hitter: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint arXiv:2508.21043_ , 2025. 

- [44] Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, and Xue Bin Peng. Maskedmimic: Unified physics-based character control through masked motion inpainting. _ACM Transactions on Graphics (TOG)_ , 2024. 

- [45] Chen Tessler, Yifeng Jiang, Erwin Coumans, Zhengyi Luo, Gal Chechik, and Xue Bin Peng. Maskedmanipulator: Versatile whole-body manipulation. In _ACM SIGGRAPH Asia Conference Proceedings_ , 2025. 

- [46] Yuxuan Wang, Ming Yang, Ziluo Ding, Yu Zhang, Weishuai Zeng, Xinrun Xu, Haobin Jiang, and Zongqing Lu. From experts to a generalist: Toward general whole-body control for humanoid robots. _arXiv preprint arXiv:2506.12779_ , 2025. 

- [47] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [48] Zhou Xian and Nikolaos Gkanatsios. Chaineddiffuser: Unifying trajectory diffusion and keypose prediction for robotic manipulation. In _Conference on Robot Learning (CoRL)_ . Proceedings of Machine Learning Research, 2023. 

- [49] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid wholebody control for learning highly-dynamic skills. In _Proceedings of Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. URL https://openreview.net/ forum?id=LCPoXt0pzm. 

- [50] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, 

Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

_Learning (CoRL)_ , 2023. 

   - [62] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. In _Conference on Robot Learning (CoRL)_ , 2024. URL https://openreview.net/forum?id= fs7ia3FqUM. 

- [51] Brent Yi, Hongsuk Choi, Himanshu Gaurav Singh, Xiaoyu Huang, Takara E. Truong, Carmelo Sferrazza, Yi Ma, Rocky Duan, Pieter Abbeel, Guanya Shi, Karen Liu, and Angjoo Kanazawa. Flow policy gradients for robot control. _arXiv preprint arXiv:2602.02481_ , 2026. 

- [52] Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C Karen Liu, and Jiajun Wu. Visualmimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [53] Runyi Yu, Yinhuai Wang, Qihan Zhao, Hok Wai Tsui, Jingbo Wang, Ping Tan, and Qifeng Chen. Skillmimicv2: Learning robust and generalizable interaction skills from sparse and noisy demonstrations. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , pages 1–11, 2025. 

- [54] Xiu Yuan, Tongzhou Mu, Stone Tao, Yunhao Fang, Mengke Zhang, and Hao Su. Policy decorator: Modelagnostic online refinement for large policy model. _arXiv preprint arXiv:2412.13630_ , 2024. 

- [55] Yanjie Ze, Zixuan Chen, Joao Pedro Ara´ujo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and C Karen Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

- [56] Chong Zhang, Nikita Rudin, David Hoeller, and Marco Hutter. Learning agile locomotion on risky terrains. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11864–11871. IEEE, 2024. 

- [57] Tong Zhang, Boyuan Zheng, Ruiqian Nai, Yingdong Hu, Yen-Jen Wang, Geng Chen, Fanqi Lin, Jiongye Li, Chuye Hong, Koushil Sreenath, et al. Hub: Learning extreme humanoid balance. _arXiv preprint arXiv:2505.07294_ , 2025. 

- [58] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- [59] Siheng Zhao, Yanjie Ze, Yue Wang, C Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [60] Zhe Zhao, Haoyu Dong, Zhengmao He, Yang Li, Xinyu Yi, and Zhibin Li. Closing the reality gap: Zero-shot simto-real deployment for dexterous force-based grasping and manipulation. _arXiv e-prints_ , pages arXiv–2601, 2026. 

- [61] Ziwen Zhuang, Zipeng Fu, Jianren Wang, Christopher Atkeson, S¨oren Schwertfeger, Chelsea Finn, and Hang Zhao. Robot parkour learning. In _Conference on Robot_ 

## APPENDIX 

## _A. XtremeMotion Motion Library_ 

The challenging motions selected from the AMASS dataset, Reallsusion, MimicKit, and LAFAN1 are detailed in Tab. V. 

## _B. Motion Complexity Metrics_ 

Given a motion sequence with frame index _t ∈{_ 0 _, . . . , T −_ 1 _}_ , frame time-step ∆ _t_ , joint positions _qt ∈_ R<sup>_J_</sup> , joint velocities _q_ ˙ _t ∈_ R<sup>_J_</sup> , root/body positions _xt ∈_ R<sup>_B×_3</sup> and velocities _vt ∈_ R<sup>_B×_3</sup> , we compute a set of scalar metrics that summarize its kinematic and contact complexity. 

_a) Joint/base kinematics.:_ From joint or base kinematics we extract: 


where _q_ ¨ _t_ and<sup>...</sup> _q t_ are obtained by finite differencing, e.g., _q_ ¨ _t ≈_ ( ˙ _qt_ +1 _− q_ ˙ _t_ ) _/_ ∆ _t_ and<sup>...</sup> _q t ≈_ (¨ _qt_ +1 _− q_ ¨ _t_ ) _/_ ∆ _t_ . We use base (torso) linear and angular kinematics to define the same three scalars (maximum linear velocity, linear acceleration and angular velocity). 

_b) Center-of-mass vertical velocity.:_ Let _zt_<sup>CoM</sup> be the center-of-mass height and _z_ ˙ _t_<sup>CoM</sup> its vertical velocity. We measure the peak vertical CoM speed 


This captures the dynamic “liveliness” of the motion (e.g., jumps). 

_c) Airborne ratio.:_ Given a set of foot body indices _F_ , a frame is considered _airborne_ if all feet are above a small height threshold _h_ air above the ground. The airborne ratio is the fraction of airborne frames 


where _zt_<sup>(</sup><sup>_b_)</sup> denotes the vertical position of body _b_ at time _t_ . _d) Contact switch frequency.:_ Independently, we obtain a binary contact state _ct ∈{_ 0 _,_ 1 _}_<sup>_K_</sup> for _K_ end-effectors and define the contact switch frequency as the number of contact state flips per second: 


In the radar plots, the _contact switch_ axis corresponds to a normalized version of this scalar, _s_ sw = min( _f_ switch _/_ 10 _,_ 1). 

_e) Difficulty scores.:_ For comparability across metrics with different physical units we map the main scalar metrics to [0 _,_ 1] “difficulty” scores using simple clamping and linear scaling, mirroring the implementation used in our analysis code. Let 


where clip( _x,_ 0 _,_ 1) = max(0 _,_ min( _x,_ 1)). The resulting 6-D score vector 


is what we use in the radar plots to summarize and compare motion complexity across datasets. 

## _C. Teacher Training_ 

The teacher policy is trained using BeyondMimic [28]——a RL motion tracking algorithm within the IsaacLab simulator, with the specific reward constituents detailed in Tab. VII. Regarding the robot configuration, a full-mesh representation is employed for the collision geometry to ensure high-fidelity physical interactions. System parameters—including armature, _kp_ , _kd_ , and action scale—are kept consistent with the BeyondMimic framework, which is specifically tailored to the motor specifications of each joint. 

The Teacher Policy employs an MLP architecture with hidden dimensions of [512, 256, 128] for both actor and critic. The actor observation is defined by 


including reference motion joint positions and velocities **_ψ_** = [ **_q_**<sup>ref</sup> _,_ **_q_** ˙<sup>ref</sup> ], **e** torso which includes torso position difference and torso orientation difference from reference represented by the 6D orientation from _R_ torso<sup>ref</sup><sup>_R_</sup> torso<sup>_⊤_,baselinearandangular</sup> velocities _V_ imu _∈_ R<sup>6</sup> , relative joint positions **_q_** _−_ **_q_**<sup>0</sup> computed by joint position **_q_** subtract default joint position **_q_**<sup>0</sup> and joint velocities **_q_** ˙, and the previous action **a** last, all of which are subject to noise described in Tab. I to enhance robustness. In contrast, the critic observation includes these same elements in their ground-truth form, supplemented by privileged information such as the robot’s precise body position and orientation, providing a comprehensive and noise-free state representation to facilitate stable value function estimation during training. 

The detailed training parameters are shown in Tab. VI. To speed up training, early termination is introduced when tracking errors is larger than a threshold. Tracking errors are defined as **e** _p,b_ = **p**<sup>ref</sup> _b −_ **p** _b_ for position and **e** _R,b_ = log( _Rb_<sup>ref</sup><sup>_R_</sup> _b_<sup>_⊤_)for</sup> 

TABLE V: Motion information summary. 

|Motion ID|Motion Source|Motion Description|
|---|---|---|
|1|CMU-85-05|Handstand walk.|
|2|CMU-85-10|Handstand spin.|
|3<br>|CMU-88-09<br>|Back Handspring with a full twist.<br>|
|4|CMU-88-08|Back Handspring with a half twist.|
|5|CMU-90-08|Aerial Cartwheel|
|6<br>|CMU-85-14<br>|B-boying with a rapid-fire string of back handsprings.<br>l|
|7|CMU-85-13|Skip back, pivot through a hand-to-headstand, drop, flip, and bounce back.|
|8|CMU-90-06|l<br>Fly kick.|
|9|CMU-90-34|Forward roll.|
|10|CMU-90-01|Backward roll.|
|11|CMU-90-28|Backspin.|
|12|CMU-85-08|Thomas Flare.|
|13|CMU-85-12|Long breaking dance.|
|14|CMU-85-04|Another long breaking dance.|
|15|CMU-85-01|Bicycle kick flip.|
|16<br>|CMU-85-02<br>|Another bicycle kick flip.<br>l|
|17|CMU-88-06|Butterfly kick.|
|18|CMU-85-06|l<br>Webster flip.|
|19<br>|CMU-49-08<br>|Two consecutive cartwheels.<br>|
|20|CMU-90-30|Alternating pistol squats.|
|21|CMU-90-29|Acrobatic gymnastics with cartwheel and back handsprings.|
|22|CMU-90-19|Crawl forward and backflip.|
|23|GeneralA11-MilitaryCrawlForward|Stay low and crawl forward.|
|24|IconicHeroMotion-SwordJudgment|Spinning slash.|
|25|IconicHeroMotion-SwordHeroic|Another style of spinning slash.|
|26|HandtoHandCombat-B3AttackReverseTurningKick|Reverse turning kick.|
|27|HandtoHandCombat-D2AttackPunchSweepKick|Punch and sweep kick.|
|28|HandtoHandCombat-D4AttackReverseFrontSnapKick|Reverse and front snap kick.|
|29|HandtoHandCombat-D4DodgeRollBack|Two consecutive rolls in different styles.|
|30|HandtoHandCombat-G1GetupKipUp|Kip up.|
|31|HandtoHandCombat-G2GetupHandstandKipUp|Handstand kip.|
|32|HandtoHandCombat-KO2FalltoGroundAxelDown|Execute a downward Axel into a ground fall.|
|33|LadyAgent-AgentElbowStrikeSweepKick|Elbow strike and sweep kick.|
|34|LadyAgent-AgentHandspring|Front handspring.|
|35|LadyAgent-AgentRollForward|Shoulder roll.|
|36|LadyAgent-AgentShootSidewardRoll|Quick side roll.|
|37|LadyAgent-AgentSnapKick|Snapkick.|
|38|Mimickit-g1spinkick|Spinkick.|
|39<br>|LAFAN1-dance1subject2 [82.8,106.9]s<br>|Constantly spin in full circles.<br>|
|40|LAFAN1-dance1subject2 [145.3,161.3]s|Play guitar while hopping on one leg.|
|41|LAFAN1-dance2subject3 [160.2,224.3]s|Flutter arms and hands.|
|42<br>|LAFAN1-fightandsports1subject1 [167.0,176.9]s<br>i|Continuous long jumps.<br>|
|43|LAFAN1-fightandsports1subject1 [0.0,17.0]s|Balance on one leg.|
|44|i<br>LAFAN1-dance1subject1 [104.6,119.1]s|Cartwheel twice.|
|45|LAFAN1-jump1subject1 [70.3,87.6]s|Play hopscotch.|
|46|LAFAN1-jump1subject1 [89.1,138.4]s|Hop on one foot.|
|47|LAFAN1-jump1subject1 [0.0,72.0]s|Successive leaps.|
|48|LAFAN1-fightandsports1subject4 [154.4,219.8]s|Vigorously swing the baseball bat.|
|49|i<br>LAFAN1-fightandsports1subject4 [61.1,85.9]s|Lash the golf club.|
|50|i<br>LAFAN1-fightandsports1subject4 [28.2,61.9]s|Diverse kicking movements.|
|51|i<br>LAFAN1-run1subject2 [20.4,101.0]s|Shuttle run.|
|52<br>|LAFAN1-run1subject2 [92.0,130.6]s<br>|Run rapidly.<br>|
|53|LAFAN1-fallandgetup2subject3 [33.8,56.1]s|Kip up twice.|
|54|LAFAN1-fightandsports1subject1 [17.3,27.2]s|Roundhouse kick.|
|55|LAFAN1-jump1subject2 [187.9,196.2]s|Push up.|
|56|LAFAN1-jump1subject2[196.0205.8]s|Lateralroll.|
|57|,<br>LAFAN1-jump1subject2 [205.6,244.4]s|<br>Lateral roll and kip up.|


orientation. Termination is triggered if the vertical position error _|_ **e** _p,z,b|_ of the torso or any end-effector ( _B_ ee) exceeds 0 _._ 25m, or if the local gravity vector discrepancy caused by torso’s orientation error _∥_ **e** _R,_ torso _∥_ exceeds 0 _._ 8. 

TABLE VI: **Motion tracking hyperparameters for teacher training** [28]. 

|Hyperparameter|Value|
|---|---|
|Architecture||
|Actor MLP hidden dimensions|[512, 256, 128]|
|Critic MLP hidden dimensions|[512, 256, 128]|
|Activation function|ELU|
|Training||
|Steps per environment|24|
|Clip parameter|0.2|
|Entropy coefficient|0.005|
|Value loss coefficient|1.0|
|Discount factor (_γ_)|0.99|
|GAE _λ_|0.95|
|Desired KL|0.01|
|Learning epochs|5|
|Mini-batches|4|


## _D. Flow matching policy training_ 

The inputs robot proprioception _p_ and motion command _c_ are each mapped to a single token, while the 15-step history _h_ is mapped to 15 individual tokens, resulting in a concatenated sequence of 17 tokens. Each mapping is performed by a dedicated MLP preprocessing unit consisting of two 256-unit layers with ReLU activations. This sequence is then processed by a Transformer encoder, followed by global average pooling and a linear projection to produce a 1024-dimensional embedding. 

Simultaneously, the action _at_ is projected through a linear layer to a 1024-dimensional space, while the time step _t_ is transformed into a 1024-dimensional embedding using sinusoidal encoding. These three components—the state embedding, action embedding, and time embedding—are concatenated and fed into a deep MLP with hidden dimensions of [2048 _,_ 2048 _,_ 2048] to predict the velocity _vt_ at time _t_ . 

## _E. Residual policy training_ 

The Residual Policy is implemented as an MLP with hidden layer sizes of [1024, 512, 256, 128, 64], with the corresponding reward functions detailed in Tab. VIII. 

The residual learning framework employs an asymmetric actor-critic architecture, as well. In this setup, the residual actor’s observation space is restricted to proprioceptive data, relative motion torso orientation, motion command joint pos and joint velocity, the previous step’s total action, and the base action out by the flow matching policy. To enhance sim-to-real robustness, uniform noise is injected into these observations, and the noise is aligned with the flow matching base policy noise. 

Conversely, the residual critic utilizes privileged information available only during simulation. The critic’s observation space encompasses the full ground-truth state, including noise-free 

TABLE VII: Reward function terms and expressions for Teacher Policy training [28]. 

|**Reward Term**|**Weight**|**Expression**|
|---|---|---|
|Global Torso Position|0.5|exp(_−∥perr∥_<sup>2</sup>_/_0_._3<sup>2</sup>)<br>|
|Global Torso Orientation|0.5|exp(_−∥θerr∥_<sup>2</sup>_/_0_._4<sup>2</sup>)<br>|
|Relative Body Position|1.0|exp(_−∥prel_<br>_err_<sup>_∥_2</sup><sup>_/_0</sup><sup>_._32)</sup><br>|
|Relative Body Orientation|1.0|exp(_−∥θrel_<br>_err_<sup>_∥_2</sup><sup>_/_0</sup><sup>_._42)</sup><br>|
|Body Linear Velocity|1.0|exp(_−∥verr∥_<sup>2</sup>_/_1_._0<sup>2</sup>)<br>|
|Body Angular Velocity|1.0|exp(_−∥ωerr∥_<sup>2</sup>_/_3_._14<sup>2</sup>)<br>|
|Action Rate|-0.1|_∥at −at−_1_∥_<sup>2</sup>|
|Joint Limit|-10.0|�max(0_, q −qlimit_)<br>|
|Undesired Contacts|-0.1|�1(_Fcontact >_1_._0)|


TABLE VIII: Reward function terms and expressions for Residual Policy training. Refer to Sec. V-K for further details regarding power safety regularization. 

|**Reward Term**|**Weight**|**Expression**|
|---|---|---|
|Global Torso Position|0.5|exp(_−∥perr∥_<sup>2</sup>_/_0_._3<sup>2</sup>)<br>|
|Global Torso Orientation|0.5|exp(_−∥_(_θerr∥_<sup>2</sup>_/_0_._4<sup>2</sup>)<br>|
|Relative Body Position|1.0|exp(_−∥prel_<br>_err_<sup>_∥_2</sup><sup>_/_0</sup><sup>_._32)</sup><br>|
|Relative Body Orientation|1.0|exp(_−∥θrel_<br>_err_<sup>_∥_2</sup><sup>_/_0</sup><sup>_._42)</sup><br>|
|Body Linear Velocity|1.0|exp(_−∥verr∥_<sup>2</sup>_/_1_._0<sup>2</sup>)<br>|
|Body Angular Velocity|1.0|exp(_−∥ωerr∥_<sup>2</sup>_/_3_._14<sup>2</sup>)<br>|
|Action Rate|-0.1|_∥at −at−_1_∥_<sup>2</sup><br>|
|Joint Limit|-10.0|�max(0_, q −qlimit_)<br>|
|Undesired Contacts<br>Power Safety Regularization|-0.1<br>-10.0|�1(_Fcontact >_1_._0)<br>�<sup>�</sup><br>max<br>�<br>0_, −τ_ ˙_q−_150<br>�<br>500<br>�2|


versions of the actor’s inputs, as well as critical state variables hidden from the actor, such as the robot’s global body position and orientation, base linear velocity, and the precise position of the motion torso. 

## _F. Actuator Modeling_ 

The physical parameters of the actuators, including armature inertia _I_ , torque-speed characteristics, and friction coefficients, are summarized in Tab. IX. 

TABLE IX: **Actuator modeling parameters.** 

|Actuator|_τy_1|_τy_2|_vx_1|_vx_2|_µs_|_vact_|_µd_|_I_|
|---|---|---|---|---|---|---|---|---|
|5020-16|24.8|31.9|30.86|40.13|0.6|0.01|0.06|3.610e-03|
|7520-14.3|71.0|83.3|22.63|35.52|1.6|0.01|0.16|1.018e-02|
|7520-22.5|111.0|131.0|14.5|22.7|2.4|0.01|0.24|2.510e-02|
|4010-25|4.8|8.6|15.3|24.76|0.6|0.01|0.06|4.250e-03|


## _G. PD control_ 

Following the methodology of BeyondMimic, we calculate the PD gains, _kp_ and _kd_ , based on the natural frequency ( _ω_ ), damping ratio ( _ζ_ ), and the armature inertia ( _I_ ) of the motors: _k_ p _,j_ = _Ijω_<sup>2</sup> _, k_ d _,j_ = 2 _Ijζω_ 

For the configuration addressed here, the parameters consist of a 10 Hz natural frequency and a damping ratio of 2. To determine the action scale, we still utilize the maximum torque 

TABLE X: Unitree G1 Joint-to-Motor Mapping. 

|**Joint Name**|**Motor Model**|
|---|---|
|Hip Pitch Joint|7520-22.5|
|Hip Roll Joint|7520-22.5|
|Knee Joint|7520-22.5|
|Hip Yaw Joint|7520-14.3|
|Ankle Pitch Joint|5020|
|Ankle Roll Joint|5020|
|Waist Roll Joint|5020|
|Waist Pitch Joint|5020|
|Waist Yaw Joint|7520-14.3|
|Shoulder Pitch Joint|5020|
|Shoulder Roll Joint|5020|
|Shoulder Yaw Joint|5020|
|Elbow Joint|5020|
|Wrist Roll Joint|5020|
|Wrist Pitch Joint|4010|
|Wrist Yaw Joint|4010|


values ( **_τ_** max) originally defined in the URDF, scaled by a factor of 0.25[28]: 


Notably, due to differences in the G1 robot variants, we utilize 7520-22.5 motors for the hip pitch actuators(Tab. X), rather than the 7520-14.3 models used in the original BeyondMimic. 

The PD setpoints (target positions) are computed using the following relationship: 


where **_q_**<sup>0</sup> represents the default joint positions, and **a** is the action output by the policy. The pre-clipped control torque is then calculated using the standard PD control law: 


In this expression, **q** and **q** ˙ denote the current joint positions and velocities, respectively. 

idealized noise-free tracking. Each motion clip is evaluated over **10 independent rollouts** , and metrics are averaged across these trials. 

_c) Unseen motion set.:_ In addition to test motions drawn from the training distributions, we evaluate generalization on an unseen motion set. This set is constructed by uniformly sampling **1000** motion clips (10 seconds each) from retargeted AMASS CMU and KIT mocap sequences, explicitly excluding all motions used in training or selected as extreme motions. The unseen set primarily consists of locomotion, turning, and simple dance-like behaviors, and is used to assess generalization beyond the curated extreme motion library. 

_d) Evaluation metrics.:_ We employ a set of pose-based and physics-aware metrics commonly used in humanoid motion tracking. All metrics are computed per episode and then averaged across episodes. 

Let _t_ = 1 _, . . . , T_ index control steps in an episode with step time ∆ _t_ (seconds), and let _i_ = 1 _, . . . , N_ index tracked bodies. All per-body errors are computed over the same tracked-body subset. 

_e) Root-relative body positions.:_ Reference motions are aligned to the robot using the torso pose. We denote the aligned reference body position as **p**<sup>ref</sup> _t,i_<sup>andtherobotbodypositionas</sup> **p**<sup>rob</sup> _t,i_<sup>.</sup> 

_f) MPJPE (mm).:_ 


_g)_ ∆ _vel (mm/frame).:_ Let **v** _t,i_<sup>refand</sup><sup>**v**</sup> _t,i_<sup>robdenotelinear</sup> velocities (in m/s). 


_h)_ ∆ _acc (mm/frame_<sup>2</sup> _).:_ Acceleration is computed by finite differences on velocity: 

## _H. Evaluation Protocol and Metrics_ 

This subsection details the evaluation protocol and metrics used throughout the paper. Our goal is to assess tracking fidelity, robustness, and generalization under controlled conditions that are consistent with training and reflective of simto-real performance. 

_a) Motion segmentation and episode length.:_ To avoid bias introduced by varying motion durations, all reference motions are segmented into fixed-length clips of **10 seconds** (corresponding to **500 control steps** ), which matches the episode length used during training. Motions shorter than 10 seconds are evaluated without further segmentation. All reported metrics in simulation and real world are computed at the clip level. 

_b) Simulation evaluation settings.:_ During simulation evaluation, we retain the same sensor noise and base domain randomization used during training, including center-of-mass offsets and default joint position offsets. This ensures that evaluation reflects basic sim-to-real robustness rather than 


The per-step acceleration error is: 


We exclude the step immediately following an environment reset. The reported acceleration error is: 


_i) Success rate.:_ An episode is considered successful if it terminates due to time-out (i.e., runs for its full allotted duration) rather than early termination. **The termination criteria used during evaluation are identical to those used during training** , including violation of safety thresholds. Success rate is defined as the fraction of successful episodes. 

TABLE XI: **Skill-level grouping of real-world evaluation motions.** Each skill category groups multiple motion instances with similar semantic meaning and dynamic structure. Motion IDs correspond to retargeted motions used during hardware evaluation. 

|Skill category|Motion IDs|
|---|---|
|Flip|5, 9, 10, 15, 16, 18, 22|
|Handspring|2, 3, 4, 19, 23|
|Acrobatics|1, 6, 7, 20, 21|
|Breakdance|11, 12, 13, 14|
|Martial arts|8, 17, 38|


_j) Aggregation.:_ MPJPE, ∆ _v_ , and ∆ _a_ are first averaged over control steps within each episode. Final reported metrics are obtained by averaging over all evaluated episodes (and over motion clips when evaluating multiple motions). 

## _I. Skill-level Grouping for Real-world Evaluation_ 

For real-world evaluation, we organize individual motions into a set of _extreme skill categories_ . Each skill groups multiple motion instances that share similar semantic intent and high-level dynamic structure. This grouping is used _only for reporting and analysis_ , and does not affect training or policy execution. 

The classification is based on human semantic understanding of the motions, taking into account characteristic body coordination patterns, contact configurations, and dominant dynamic features (e.g., aerial phases, rapid contact switching, or impulsive landing). We emphasize that this grouping is not obtained through automated clustering or learned representations, but serves as a transparent and interpretable abstraction for summarizing real-world performance. 

Tab. XI lists the correspondence between skill categories and the underlying motion instances used in hardware evaluation. 

## _J. Motion Subsets Used in Fidelity–Scalability Analysis_ 

In the fidelity–scalability analysis Sec. IV-D, we evaluate how tracking performance degrades as the size of the motion library increases. To ensure a controlled and interpretable comparison, we explicitly specify the motion subsets used at each scale. 

We begin with a curated set of extreme motions that exhibit high angular velocities, rapid contact switching, and challenging balance conditions. These motions represent a diverse yet highly demanding subset of the full motion library. All quantitative evaluations in Q2 are conducted on the same **first 10 motions** of this set, which include fast flips, contactrich acrobatics, and extreme balance behaviors. By fixing the evaluation set, we isolate the effect of training-scale growth from changes in evaluation difficulty. 

To study scalability, we progressively expand the training motion library to include 10, 20, and all extreme motions. The additional motions are drawn from the same extreme motion pool and increase diversity in contact patterns and dynamic regimes, while preserving a consistent difficulty level. This 

TABLE XII: **Motion subsets used in Q2 fidelity–scalability analysis.** All evaluations are performed on the same first 10 extreme motions. Larger training sets (20 and all motions) extend this core set with additional diverse extreme motions. 

|Training motions|Motion IDs|
|---|---|
|10|3–10, 13, 14|
|20|2–10, 13-22|
|50|All|


design yields a controlled yet representative benchmark for analyzing the fidelity–scalability trade-off under increasingly diverse extreme motions. Tab. XII summarizes the motion IDs used at each scale. 

## _K. Knee negative power penalty._ 

For each knee joint _j_ with torque _τj_ and joint velocity _q_ ˙ _j_ , we define the instantaneous mechanical power _Pj_ = _τj_ ˙ _qj_ and penalize excessive _negative_ power (large braking torques) beyond a deadband threshold. Concretely, for knee joints selected via the regex ".*_knee_joint" we compute 


where the deadband is 150 (in the same units as power, e.g., W). The normalized per-step penalty is 


where 500 is the normalization constant power_norm. In the reward function this term is added with weight _w_ = _−_ 10, i.e., _r_ knee = _w c_ knee, so that large negative joint power at the knees is strongly discouraged. 

## _L. TensorRT-Accelerated Deployment_ 

For deployment on the real G1 robot we run the model as an ONNX graph, executed by ONNX Runtime with TensorRT acceleration. At run time the deploy node continuously receives joint states and IMU signals from the robot, builds a compact observation vector, and feeds it to the ONNX base policy. The base policy outputs a 29-dimensional whole-body action, and, the residual policy produces a small corrective action in the same space; the two are added to obtain the final command. This command is interpreted as desired joint positions, which are tracked by a PD controller with safety envelopes on torques and velocities, and converted into low-level motor commands at a control period of 20 ms. 

When a GPU with TensorRT is available, ONNX Runtime delegates the forward pass of these ONNX models to TensorRT, giving a lower-latency implementation of the same controller. In our implementation, we use **5 ODE integration steps** (often informally referred to as denoising steps), which strike a favorable balance between action quality and computational cost. All inference is executed on the onboard **NVIDIA Jetson Orin NX** of the Unitree G1 humanoid robot. With TensorRT acceleration, the end-to-end policy inference latency, including the full ODE integration procedure, is approximately 

**10 ms** per control step. This latency comfortably satisfies realtime control requirements and enables closed-loop execution of high-dynamic whole-body motions entirely on the onboard compute, without reliance on offboard processing. 

## _M. Failure Cases and Discussion_ 

While OMNIXTREME achieves strong sim-to-real performance overall, we observe a small number of failure cases during real-world deployment. These failures predominantly occur during highly impulsive landing phases of certain extreme motions, where large transient braking loads trigger hardware protection mechanisms, including motor overcurrent, power limits, or battery undervoltage events. 

Notably, these motions can be executed reliably in simulation and sim-to-sim transfer, indicating that failures are not caused by degraded tracking accuracy or loss of balance. Instead, they expose residual discrepancies between simulated actuation models and the true hardware capability envelope under extreme dynamic conditions. These observations suggest that further improving robustness for extreme motions will require more comprehensive modeling of real actuator and power-system limits, including the coupled effects of torque, speed, current, power flow, and battery voltage dynamics, which remain challenging to capture accurately in simulation. 

In the current work, post-training is performed via a lightweight residual policy that refines a frozen flow-based base controller. While this design offers stability and sample efficiency, it may also limit the extent to which the full representational capacity of the large flow-based model can be further adapted to hardware-specific constraints. Future research may explore more native post-training strategies [51] that directly fine-tune or adapt the full base policy under actuation-aware objectives. Such approaches could potentially unlock greater expressivity and hardware alignment from large generative control models, enabling more principled integration between flow-based policy learning and real-world physical constraints. 

