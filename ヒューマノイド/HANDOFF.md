---
title: "HANDOFF: Humanoid Agentic Task-Space Whole-Body Control via Distilled Complementary Teachers"
date: "2026-06-04"
authors: "Lizhi Yang; Junheng Li; Nehar Poddar; Yiling Hou; Gio Huh; Robert Griffin"
url: https://arxiv.org/abs/2606.06493
pdf: https://arxiv.org/pdf/2606.06493
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.06493)** / [論文ページ](https://arxiv.org/abs/2606.06493)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# HANDOFF: Humanoid Agentic Task-Space Whole-Body Control via Distilled Complementary Teachers 

Lizhi Yang<sup>1</sup> , Junheng Li<sup>1</sup> , Nehar Poddar<sup>2</sup> , Yiling Hou<sup>1</sup> , Gio Huh<sup>1</sup> , Robert Griffin<sup>2</sup> , Georgia Gkioxari<sup>1</sup> , and Aaron D. Ames<sup>1</sup> 

**_Abstract_ — Humanoid loco-manipulation benefits from one controller to coordinate locomotion, arm movements, and fall recovery. These behaviors are difficult to learn together from scratch because they require different skills and objectives. We present HANDOFF, a training architecture that distills motion-tracking, locomotion, and recovery teachers into one 29DoF policy, using context-conditioned KL losses over separate action slices and a soft mixture of experts. Commanded velocity continuously blends body supervision, while a binary recovery flag assigns the full action to the recovery teacher. The resulting controller takes a compact 10-D task-space command rather than a dense kinematic stream and does not switch policies at runtime. On the Unitree G1, HANDOFF matches stateof-the-art velocity tracking and obtains the largest robust manipulation workspace in a matched adapted-interface benchmark. The same controller executes natural-language-driven, multi-stage loco-manipulation tasks in simulation and hardware experiments without further data collection or fine-tuning.** 

## I. INTRODUCTION 

A humanoid robot fetching a cup of coffee for someone looks effortless in a video. The planning and control problem behind that loco-manipulation action is anything but: it has to coordinate object localization, sensing, motion planning, and whole-body control [15]. For the planner, the practical question is what to command. A person can describe sparse subgoals (“find the coffee, walk near it, reach for it, grab it”) and leave gait and balance to lower-level control. Most whole-body controllers (WBCs) instead operate in a motion-tracking regime [1]–[3] and require a dense full-body kinematic stream at the control rate. Producing this stream for a new skill requires teleoperation or motion capture, embodiment-specific retargeting, and dynamic-feasibility filtering. As a result, the planner largely replays motions from a fixed demonstration library. We seek a low-dimensional command that a human, geometric planner, or VLM can provide while leaving whole-body coordination to the controller. 

In this paper, we propose HANDOFF, a training architecture that composes complementary specialists into one taskspace whole-body controller with the command 


where _vx, vy, ωz_ are planar base velocity commands, _z_ is the commanded root height, and _p_<sup>_P_</sup> _L_<sup>_, pP_</sup> _R_<sup>arebilateralpelvis-</sup> frame wrist targets. These variables are standard planner 

> 1California Institute of Technology, Pasadena, CA, USA. _{_ lzyang, junhengl, yhou, ghuh, georgia, ames _}_ @caltech.edu 

> 2The Institute for Human & Machine Cognition, Pensacola, FL, USA. _{_ npoddar, rgriffin _}_ @ihmc.org 


Fig. 1: **HANDOFF.** Motion-tracking, locomotion, and recovery specialists are distilled into one whole-body controller. Context determines which teacher supervises each action slice, and a VLM-based planner drives the resulting 10-D interface without task-specific fine-tuning. 

outputs. Locomotion stacks produce ( _vx, vy, ωz_ ), grasp planners produce end-effector targets, and a squat or reach heuristic can set _z_ . Language-grounded planners [16], [17] also decompose long-horizon goals into task-space subgoals. VLAs [18], [19] produce end-effector actions that map to the wrist targets without retargeting or controller fine-tuning. The command also specifies coupled whole-body behavior. A low _z_ with forward wrist targets produces a squat and reach; an asymmetric wrist target during locomotion produces a onehanded moving reach. 

No single training regime learns velocity tracking, coordinated whole-body reaching, and fall recovery equally well. We therefore train one specialist for each regime and distill them into a single student. A public retargeted motion dataset supplies the whole-body motion-tracking teacher [3], [20], task rewards train the locomotion teacher [21], and adversarial motion priors train the fall-recovery teacher [22], [23]. Each teacher is a separate module that can be improved or replaced independently. We train the student with PPO [24], multi-teacher KL [25], and a soft mixture of experts [26]. Its objective blends WBC and locomotion supervision over the legs and waist according to commanded velocity, keeps the arms under the motion-tracking teacher, and uses full-action recovery supervision only during recovery. This produces one policy with all three behaviors and no runtime switching. 

Our contributions are as follows: 1) a context-conditioned, action-sliced KL objective for distilling teachers with dif- 

TABLE I: **Planner-facing interfaces.** Recent whole-body humanoid controllers are compared by their required command references and whether they retain a single deployed policy. 

|**Method**|**Locomotion ref.**|**Height ref.**|**Arm ref.**|**No dense**<br>**streaming**|**No ext.**<br>**kin. ref.**|**Single**<br>**policy**|
|---|---|---|---|---|---|---|
|Motion-tracking WBCs [1]–[6]|kin. ref. (29D)|from kin.|full upper kin. (14D)|_×_|_×_|✓|
|ResMimic [7]|kin. ref. (29D)|from kin.|full upper kin. (14D)|_×_|_×_|_×_|
|VisualMimic [8]|keypoint stream (18D)|from kin.|keypoint stream (18D)|_×_|✓|✓|
|HOVER [9]|multi-mode kin. (_∼_80D + mask)|from kin.|from kin.|_×_|_×_|✓|
|HOMIE / FALCON [10], [11]|velocity (2–6D)|scalar _h_ (1D)|full upper kin. (14D)|✓|_×_|_×_|
|AMO [12]|velocity (3D)|torso pose (4D)|full upper kin. (14D)|✓|_×_|_×_|
|HUMI [13]|pelvis traj. (6D)|from pelvis|EE traj. (12D)|_×_|✓|✓|
|HERO [14]|velocity (6D)|scalar _h_ (1D)|upper kin. (17D) + IK residual (6D)|✓|_×_|_×_|
|**HANDOFF (Ours)**|**velocity (3D)**|**scalar** **_h_ (1D)**|**wrist target (6D)**|✓|✓|✓|


ferent action coverage into one MoE student; 2) a 29-DoF controller combining locomotion, whole-body coordination, and recovery under one 10-D command without policy switching; and 3) ablations and matched evaluations of controller interfaces, recovery, randomized tasks, and hardware deployment. We will release the full framework to facilitate future research in the field. 

## II. RELATED WORK 

**Whole-body motion tracking with dense-reference interfaces:** Motion imitation first produced diverse behavior for physics-based characters [22], [27] and now scales to humanoid robots through motion-tracking WBCs [1]–[6] and masked multi-mode policies [9]. Recent work studies residual control [7], visual hierarchies [8], motion data [28], [29], and real-time retargeting from human demonstrations [30], [31]. These controllers reproduce expressive motion, but the planner must generate the full kinematic stream, as in Table I. HANDOFF does not reproduce motion outside its teacher coverage, such as dancing, but its commands can be generated by a simple planner. 

**Task-command controllers and architectural decompositions:** Controllers with compact mid-level commands differ in how they divide control over the body. [10] uses cockpit commands for the upper body and a separate RL policy for the lower body. [11] co-trains lower-body locomotion with a force-adaptive upper-body controller, while [12] combines RL with dynamically optimized whole-body references. [32] and [9] use head-and-hand targets, but still require dense target trajectories at the controller rate. Other methods consume upper-body joint references [14], select from skill libraries [33], or train a task policy above a learned controller [13], [34]–[36]. In multi-task loco-manipulation systems [13], [34], a new behavior requires new whole-body demonstrations and a new task policy. Table I summarizes the references exposed to an upstream planner. Here, _No ext. kin. ref._ means that the planner can issue commands without using IK or retargeting to generate joint angles. HANDOFF directly admits base velocity, root height, and bilateral wristposition targets through a single policy. 

**VLA- and VLM-driven systems:** Planner-controller systems couple language models to skill libraries [16], while vision-language-action models train transformers to produce low-level actions [17]–[19]. Humanoid systems pre-train on 

egocentric video and post-train an action expert above a low-level controller [37], [38]. [39] connects a VLM to a modular RL/ACT skill library, and [40] uses a latent “verb” vocabulary instead of an explicit interface. In HANDOFF, this layer is replaceable and targets the same 10-D baseand-hand command. 

**Specialist-to-generalist distillation and expert routing:** Several humanoid systems combine control modes, locomotion behaviors, motion clusters, embodiment-specific specialists, parkour skills, or motion-tracking teachers in one student [9], [41]–[44]. [6] gates a motion MoE over clusters from one motion-tracking manifold and retains a dense kinematic reference. [45] instead keeps the experts separate and learns an inference-time gate. [46] uses DAgger to distill one dense-reference motion-tracking teacher into a partial-observation student for simulated characters, addressing a difference in input modalities. HANDOFF addresses a different mismatch. Under the fixed command [ _vx, vy, ωz, z, pL_<sup>_P, pP_</sup> _R_<sup>],thehuman-motionteacherprovides</sup> whole-body coordination but limited task coverage, while the locomotion and recovery teachers provide narrower but more reliable behaviors. 

## III. WHOLE-BODY CONTROL 

Figure 2 summarizes the training pipeline. Wholebody coordination, command-conditioned locomotion, and ground-to-upright recovery rely on different references, rewards, and state distributions. We train one PPO teacher for each regime, then distill them into a single student to avoid runtime policy switching. Action-sliced, context-conditioned supervision and a soft MoE preserve the specialists’ roles within one deployed controller. 

## _A. Whole-Body Control Teacher_ 

The 29-DoF motion-tracking teacher follows recent controllers [2]–[5] and uses asymmetric actor-critic PPO [47]. Training uses a retargeted human motion dataset<sup>1</sup> [20]. Its actor receives an 11-frame proprioceptive history and the full 29-D reference joint angles from the current clip frame. The critic also receives measured base linear velocity, reference root pose, key-body positions, and domain-randomization parameters, none of which are available to the deployed actor. This teacher learns posture, reaching, squatting, and bilateral 

> 1Motion Data by Bones Studio - https://bones.studio/ 


Fig. 2: **Training architecture.** Separate whole-body motion-tracking, locomotion, and fall-recovery teachers supervise a context-routed MoE student that maps the 10-D command to 29-DoF actions. 


Fig. 3: **CoP filtering.** Filtered squat reference remains inside the support polygon; the original reference drifts. 

coordination. However, its locomotion is tied to the motion data and does not reliably track arbitrary velocity commands, as shown in Table IIa. The retargeted data also contains squat frames that are dynamically infeasible for the real robot. Before training, we correct them with a closed-form CBF projection on the static center-of-pressure (CoP) margin. For quasi-static squat frames (root height below 0 _._ 65 m and planar speed below 0 _._ 2 m/s), let _h_ ( _q_ ) be the signed CoM distance to the foot-contact box shrunk by _δ_ = 0 _._ 10 m. When _h < h_ tgt = 0 _._ 04 m, we project in a 7-D correction subspace of bilateral hip pitch, ankle pitch/roll, and waist pitch: 


where _Jc,xy_<sup>ccisthecontact-consistentCoMJacobianunder</sup> rigid double support. We iterate this projection with backtracking, re-anchor the base at the mid-feet pose, and blend each corrected segment over 10 frames. Figure 3 shows one corrected squat clip. 

## _B. Locomotion Teacher_ 

The locomotion teacher controls the 15-DoF legs-andwaist slice on flat terrain. Curriculum-blended motion samples drive the arms during training, exposing the policy to the corresponding CoM shifts before distillation. The actor observes commanded velocity, projected gravity, base angular velocity, joint state, last action, and a 4-D gait- 

phase block. The critic also receives the measured base linear velocity. The rewards combine velocity tracking with gait and stance terms. Linear and angular velocity tracking use exponential errors with ranges of 1 m/s and approximately _π_ rad/s. A phase-contact term uses a 0 _._ 6 stance ratio, while swing-foot clearance, flat-foot contact, foot-slip, and actionrate terms regularize the resulting gait. 

## _C. Fall-recovery Teacher_ 

A full-body 29-DoF Adversarial Motion Prior (AMP) teacher learns fall recovery [22], [23]. Episodes start from random frames of retargeted motion, including ground poses from one fall-and-get-up clip. The discriminator data contains this clip together with 17 walking, jogging, and turning clips. The teacher does not copy the get-up motion frame by frame. Under the style prior, RL learns recovery from fallen initializations, and a small torso-anchor reward encourages command tracking after the robot stands. The PPO reward is 0 _._ 25 _r_ disc + 0 _._ 75 _r_ task. Up to 40% of environments use delayed fallen resets to retain ground-to-upright transitions in the training distribution. 

## _D. Context-Conditioned Behavior Composition_ 

The teachers provide complementary supervision at different levels: WBC and AMP cover the full action space in their respective regimes, while locomotion specializes in the body slice under velocity commands. We combine their targets according to both action coverage and control regime. Action slices determine which joints a teacher supervises, and context weights determine when its target is active. We query them with a shared simulator state while preserving their native inputs: a dense motion reference for WBC, twist and gait phase for locomotion, and four-frame proprioception for AMP. Pelvis-frame forward kinematics converts each WBC reference into the sparse commands _z, p_<sup>_P_</sup> _L_<sup>_, pP_</sup> _R_<sup>; velocity</sup> commands are sampled independently in [ _−_ 1 _,_ 1] and resampled every 3–8 s, with 10% of environments standing. The student receives only the resulting 10-D command and its proprioceptive history. 

Let _B_ = _a_ 0:15 and _A_ = _a_ 15:29 denote the body and arm slices, and let _Dj_<sup>_S_</sup> = _D_ KL( _πθ_<sup>_S∥π_</sup> _j_<sup>_S_)betheKLaveraged</sup> over slice _S_ . We use context **x** _t_ = ( _∥c_<sup>vel</sup> _t_<sup>_∥, rt_),where</sup> 


Fig. 4: **Expert routing.** Recovery dominates get-up; upright experts alternate in walking and share standing motions. _rt_ = recover _t_ , _mt_ = 1 _−rt_ , and _α_ = _σ_ (( _∥c_<sup>vel</sup> _t_<sup>_∥−_0</sup><sup>_._1)</sup><sup>_/_0</sup><sup>_._02).</sup> capture-point term. This approximation is exact in double The four HANDOFF routes form one distillation loss: stance and avoids convex-hull construction during 

capture-point term. This approximation is exact in double stance and avoids convex-hull construction during batched training. For recovery states, active hand contacts extend the support region used by the CoM term. If a wall or table contact supports the body, the capture-point term receives full reward rather than penalizing a point outside the feetonly polygon. The same balance objective therefore covers foot-supported and braced whole-body recovery. Penalties on changes in whole-body linear and angular momentum suppress abrupt corrections. These terms shape upright balance, while AMP remains responsible for ground-to-upright recovery. 


For upright states, _α_ shifts body supervision from WBC to locomotion as commanded velocity increases, while WBC continues to supervise the arms. In recovery states, AMP replaces both routes and supervises the full action. For diagonal-Gaussian teachers, overlapping routes produce a precision-weighted geometric mean on each supervised action dimension. 

To retain capacity for the three regimes within one controller, the student uses a soft MoE. On non-recovery samples, a standard load-balancing loss _L_ LB [26] balances the renormalized WBC and locomotion weights. When recovery is active, _L_ R pins one expert to recovery without labeling the two upright experts. Figure 4 visualizes the learned routing weights across recovery, locomotion, and standing upperbody commands. The complete student objective is 

## _F. Training setup_ 

All policies use asymmetric actor-critic PPO in mjlab with Rsl-rl. One iteration collects 24 steps from 4,096 parallel environments ( _≈_ 98K transitions), followed by five Adam epochs over four mini-batches. We use learning rate 10<sup>_−_3</sup> , PPO clip 0 _._ 2, entropy coefficient 0 _._ 005, _γ_ = 0 _._ 99, GAE _λ_ = 0 _._ 95, and gradient-norm clip 1 _._ 0. The teacher actors and critics are [512 _,_ 256 _,_ 128] ELU MLPs. The student uses a [512 _,_ 512 _,_ 256 _,_ 128] backbone with Swish, LayerNorm, and the 64-D temporal latent used by the MoE. The MoE gate is a [128 _,_ 64] MLP over this latent, and each [256 _,_ 128] expert predicts a 29-D action mean. At every step, the gate blends all outputs under a shared log-standard-deviation. Only recovery is explicitly pinned; the other experts divide upright behavior without labels. Soft routing avoids hard top- _k_ discontinuities and retains one deployed controller. During distillation, ( _λB, λA, λ_ AMP) are cosine-annealed from (0 _._ 4 _,_ 0 _._ 1 _,_ 0 _._ 4) to (0 _._ 2 _,_ 0 _._ 05 _,_ 0 _._ 2), with _β_ LB = 0 _._ 01 and _β_ R = 0 _._ 5. The smaller arm weight reduces interference with locomotion stability. The WBC teacher and student train for up to 30K updates, the locomotion teacher for 20K, and AMP for 100K. We evaluate the final checkpoints. Domain randomization covers base mass, foot friction, PD gains, motor strength, encoder bias, hand forces, and actuation delay. These parameters are hidden from the actor. 


## _E. Whole-Body Stability Shaping_ 

We add shared balance rewards [48] to WBC, locomotion, and the student; AMP retains its recovery objective. The rewards use the mass-weighted whole-body CoM and active-foot contacts. CoM and capture-point terms reward stayingCoM˙ _xy/_ inside ~~�~~ _g/h_ theCoMsupport. An ankle-hip-stepregion, wheretermCPrewards= CoMankle _xy_ + torque opposing CoM drift, hip motion once ankle authority saturates, and swing-foot motion toward the capture point once both saturate. Actuator torques are normalized by their joint limits, and CoP saturation against a _µ_ = 0 _._ 7 friction cone determines when ankle and hip authority are exhausted. During training, we approximate the support polygon by the axis-aligned bounding box of active foot contacts, using force thresholds of 20 N for the CoM term and 50 N for the 


Fig. 5: **Agentic deployment pipeline.** Perception and planning produce the 10-D command consumed by HANDOFF. 

## _G. Agentic planner_ 

Any planner that emits the 10-D command can drive the controller. For the hardware experiments, we use the locomanipulation stack in Fig. 5. A high-level reasoner divides a natural-language instruction into atomic tasks through regex parsing, with an LLM fallback when no pattern matches. A VLM projects predicted 2D points and bounding boxes into the RGB-D point cloud. A waypoint tracker then converts the pelvis-frame waypoints into ( _vx, vy, ωz_ ). Near the target, a skill selector produces root height _z_ and bilateral wrist targets _p_<sup>_P_</sup> _L_<sup>_, pP_</sup> _R_<sup>.Akinematiccorrectionalignseachgripper</sup> horizontally with the grasping surface. The reasoner runs at 0.001 Hz, the VLM at 0.1 Hz, and the skill selector at 1– 50 Hz. HANDOFF runs at 50 Hz, and its 29-DoF actions are tracked on hardware at 500 Hz. 

we select each adapted baseline on a separate validation set and evaluate it with 600 discovery and 250 accuracy targets per mirrored or independent mode. All controller variants use the same command sweeps and paired target sets. 

## _A. Ablation studies_ 

Table IIa starts with direct distillation of the motiontracking teacher and adds one specialist or composition mechanism at a time. Each row is one policy with the same 10-D interface. The locomotion teacher gives the largest initial velocity gain. Randomized commands then close the lateral-velocity gap, and action-sliced KL with a soft MoE closes the remaining _vx_ gap. Two-teacher ablations use two experts. The recovery variants add a third pinned expert and recovery KL term, while the stability variants change rewards but not the teacher-student architecture. Gate 

## IV. EXPERIMENTS 

We run all experiments on a 29-DoF Unitree G1 with an external payload (Jetson Thor + Dex1-1 grippers) in mjlab/MuJoCo [49], and train every policy with Rsl-rl [50]. We measure velocity tracking, manipulation workspace, fall recovery, and task resumption. The experiments also isolate the components of the training architecture, compare controllers adapted to the same command interface, and test complete loco-manipulation tasks through the 10-D command. 

For velocity tracking, we sweep per-axis commands along [ _−_ 1 _,_ 1] and report _|_ ∆ _v·|_ = E _t_ [ _|v·_<sup>cmd</sup> ( _t_ ) _− v·_<sup>base</sup> ( _t_ ) _|_ ]. For manipulation, we sample bilateral wrist targets uniformly inside [ _−_ 0 _._ 6 _,_ 0 _._ 6]<sup>3</sup> m in the pelvis frame, with a 1 s warm-up, 2 s settle, and 4 s measurement window. We define _feasibility_ as the fraction of trials with no fall and less than 25 cm pelvis drift. _Robust WS_ is the convex-hull volume of targets tracked within 15 cm, multiplied by feasibility, in the task-relevant forward half-space _x ≥_ 0. Each velocity sweep uses 20 commands per axis. Table IIa uses 2,000 discovery and 400 accuracy targets per controller. For the matched comparison, 

TABLE II: **Controller evaluation.** Panel (a) isolates the stages of behavior composition; panel (b) compares controllers under the matched adapted contract. 

(a) Progressive behavior composition. 

|**Ablation**|_|_∆_vx|_<br>(|_|_∆_vy|_<br>m/s, rad/s)|_|_∆_ωz|_<br>_↓_|**Robust WS**<br>(m<sup>3</sup>) _↑_|
|---|---|---|---|---|
|Direct|0.29|0.43|0.08|0.20|
|+ Dual teacher|0.14|0.25|0.09|**0.31**|
|+ RandCmd|0.14|**0.13**|0.05|0.29|
|**+ Split KL + MoE (Ours)**|**0.07**|0.14|**0.04**|0.27|
|**+ AMP recovery (Ours + Rec.)**|**0.07**|0.15|0.05|0.26|
|**+ Stability (Ours + Stab.)**|**0.07**|0.18|**0.04**|**0.31**|
|**+ Stab. + Rec. (Ours + Stab. + Rec.)**|**0.06**|0.18|0.06|0.277|


### (b) Matched adapted-contract comparison. 

|**Method**|_|_∆_vx|_|_|_∆_vy|_|_|_∆_ωz|_|**Feas.**|**Robust WS**<br>|
|---|---|---|---|---|---|
||(|m/s, rad/s)|_↓_|(%) _↑_|(m<sup>3</sup>) _↑_|
|FALCON [11]|0.07|**0.10**|0.07|26.1|0.033|
|OpenHomie [10]|0.06|0.12|0.10|72.3|0.098|
|AMO [12]|0.06|0.19|**0.01**|84.7|0.215|
|SONIC [1]|**0.03**|0.15|0.02|**96.2**|0.265|
|**Ours + Stab. + Rec.**|0.06|0.18|0.06|93.0|**0.277**|


Fig. 6: **Hardware and simulated deployments.** The same 10-D controller executes six VLM-commanded task sequences without task-specific fine-tuning. 

probes on deployed observation streams show the learned specialization. The recovery expert receives 92% of the gate mass during get-up and 5% during walking, while upright motion mixes the two non-recovery experts with weights of 0.40–0.49 each. Adding recovery expands the hull toward more extreme targets but reduces pointwise feasibility. 

## _B. Comparison with whole-body controllers_ 

Table IIb uses a common _adapted contract_ because the prior controllers accept different arm interfaces. The same differential-IK bridge [51] maps bilateral wrist targets to each baseline’s native arm commands, while its controller remains responsible for walking and balance. Figure 7 visualizes the workspace hulls combined across mirrored and independent modes. HANDOFF covers 0 _._ 297 m<sup>3</sup> , giving 0 _._ 277 m<sup>3</sup> Robust WS; SONIC has higher feasibility at 96.2% but a smaller 0 _._ 275 m<sup>3</sup> hull and 0 _._ 265 m<sup>3</sup> Robust WS. Conditioning on targets where the IK bridge converges below a 2 cm residual, AMO, OpenHomie, and SONIC execute 87– 92%, while FALCON executes 63%. 

## _C. Recovery and task resumption_ 

All variants receive random base-velocity impulses every 1–3 s, up to 0.5 m/s per horizontal axis. They remain upright at four times this magnitude; Upright@6 _×_ extends 


Fig. 7: **Bilateral wrist workspace.** Feasible target hulls are shown in the pelvis frame under the validation-selected protocol. 

the disturbance-rejection test. Table IIIb instead starts each policy from 500 paired, physics-generated fallen states. The stability rewards improve both recovery and the six-timespush result. Every successful recovery resumes a commanded 0.4 m/s walk with at most 0.05 m/s error. The benchmark re- 

TABLE III: **Task-level success and recovery.** Values are percentages except mean recovery time. 

(a) Cumulative task-stage success. 

|Task<br>|Approach|Grasp|Carry|Place/HO|Success|
|---|---|---|---|---|---|
|Pick–place|100|100|—|99.8|99.8|
|Bilateral pick–place|100|100|—|100|**100**|
|Bimanual handover|100|77.6|77.6|77.6|77.6|
|Squat pick|99.8|95.6|71.0|67.2|67.2|
|Pick–transport–place|99.8|99.8|72.4|72.2|72.2|
|(b) Fallen-state|recovery|and str|ong-p|ush robustn|ess.|
|Variant|Recovery|¯_t_rec (s|)<br>R|esume<br>Up|right@6_×_|
|Ours|0|—||—|41|
|Ours + Stab.|0|—||—|55|
|Ours + Rec.|49.8|1.5||100|74|
|Ours + Stab. + Rec.|**89.6**|3.2||**100**|**95**|
|StrongPush|0|—||—|66|


ports standing and command resumption as separate metrics, with recovery time computed over successful trials. Paired initial states and disturbance sequences keep the comparison across variants fixed. StrongPush is trained directly with fallinducing impulses at six times the training magnitude. It records no recoveries in 500 trials, along with 47% shorter episodes and 14% higher velocity error. Falls terminate these episodes, so its training data do not contain ground-to-upright transitions. The AMP teacher supplies these transitions as a separate recovery regime. 

## _D. Task-level contract and hardware deployment_ 

Our VLM+depth stack estimates goals in the robot frame and re-queries at close range without a global scene map. Deterministic tools provide waypoint tracking, path planning, skill selection, model-based wrist-orientation correction, and discrete gripper control on top of the controller’s 3-D wristposition commands. The VLM grounds targets to 1.2–1.6 cm error after re-query. We inject that measured error into 500 paired, randomized object/goal placements for each of five tasks while retaining the deployed downstream tools and 10-D controller contract; grasps are kinematic within the gripper’s 12 cm jaw width. In Table IIIa, Place/HO denotes the terminal placement or handover stage. Across 2,500 trials, the approach stage succeeds in at least 99.8%, no trial falls, and total task success ranges from 67.2% to 100% (Table IIIa). Because the entries are cumulative, each column includes all preceding stages. Bilateral pick-andplace remains at 100% through placement, while bimanual trials that complete grasp retain the same success rate through carry and handover. 

We deploy the same controller on a real Unitree G1 with a ZED-M RGB-D camera and Jetson Thor, using both local VLM and ChatGPT APIs. Figure 6 shows pick-andplace, pick-transport-place, squat-pick, bimanual handover, bilateral pick-and-place, and task continuation after recovery; Table IIIa reports aggregate task statistics from simulation. In these hardware runs, one unchanged low-level policy executes all six command sequences through the full planning stack. The high-level stack changes only the 10-D command and does not select among low-level controllers. Hardware 

operation uses command clipping, wrist-target workspace bounds, CoP filtering, and an operator e-stop. 

## V. CONCLUSION 

In this paper, we introduced HANDOFF, which distills specialists with different objectives and action coverage into one humanoid whole-body controller. Its contextconditioned, action-sliced objective blends motion-tracking and locomotion supervision over the body, keeps the arms under whole-body motion supervision, and assigns the full action to the recovery teacher only during recovery. A soft mixture of experts combines these regimes without switching controllers at deployment. The policy matches state-of-theart velocity tracking, obtains the largest robust workspace in a matched adapted-interface comparison, and recovers from the ground before resuming its commanded walk. The recovery ablation also separates disturbance rejection from recovery: only the teacher that observes ground-to-upright transitions learns to stand again. All behaviors use one 10-D command, allowing the controller to operate below different planning systems. We evaluate this interface with randomized task trials and VLM-driven hardware experiments. Future work will extend this composition scheme to additional specialists and test whether they can be added without changing the 10-D command or degrading behaviors already in the controller. 

## REFERENCES 

- [1] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, _et al._ , “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 

- [2] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [3] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu, “Twist2: Scalable, portable, and holistic humanoid data collection system,” _arXiv preprint arXiv:2511.02832_ , 

2025. 

- [4] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 2828–2844. 

- [5] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [6] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang, “Gmt: General motion tracking for humanoid whole-body control,” _arXiv preprint arXiv:2506.14770_ , 2025. 

- [7] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan, “Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning,” _arXiv preprint arXiv:2510.05070_ , 2025. 

- [8] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu, “Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation,” _arXiv preprint arXiv:2509.20322_ , 2025. 

- [9] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, _et al._ , “Hover: Versatile neural whole-body controller for humanoid robots,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9989–9996. 

- [10] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit,” in _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [11] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Aghamohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi, “Falcon: Learning force-adaptive humanoid loco-manipulation,” _arXiv preprint arXiv:2505.06776_ , 2025. 

- [12] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang, “AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid Whole-Body Control,” in _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [13] R. Nai, B. Zheng, J. Zhao, H. Zhu, S. Dai, Z. Chen, Y. Hu, Y. Hu, T. Zhang, C. Wen, _et al._ , “Humanoid manipulation interface: Humanoid whole-body manipulation from robot-free demonstrations,” _arXiv preprint arXiv:2602.06643_ , 2026. 

- [14] R. Dong, Z. Li, X. He, and S. Gupta, “Learning humanoid end-effector control for open-vocabulary visual loco-manipulation,” _arXiv preprint arXiv:2602.16705_ , 2026. 

- [15] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu, _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _IEEE/ASME Transactions on Mechatronics_ , vol. 31, no. 2, pp. 2300–2330, 2026. 

- [16] B. Ichter, A. Brohan, Y. Chebotar, C. Finn, K. Hausman, A. Herzog, D. Ho, J. Ibarz, A. Irpan, E. Jang, _et al._ , “Do as i can, not as i say: Grounding language in robotic affordances,” in _Proceedings of The 6th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, K. Liu, D. Kulic, and J. Ichnowski, Eds., vol. 205. PMLR, 2023, pp. 287–318. 

- [17] D. Driess, F. Xia, M. S. M. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu, _et al._ , “PaLMe: An embodied multimodal language model,” in _Proceedings of the 40th International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, A. Krause, E. Brunskill, K. Cho, B. Engelhardt, S. Sabato, and J. Scarlett, Eds., vol. 202. PMLR, 23–29 Jul 2023, pp. 8469–8488. 

- [18] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Proceedings of The 7th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, J. Tan, M. Toussaint, and K. Darvish, Eds., vol. 229. PMLR, 2023, pp. 2165–2183. 

- [19] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, _et al._ , “Openvla: An open-source vision-language-action model,” in _Proceedings of The 8th Conference on Robot Learning_ , ser. Proceedings of Machine Learning Research, P. Agrawal, O. Kroemer, and W. Burgard, Eds., vol. 270. PMLR, 06–09 Nov 2025, pp. 2679–2713. 

- [20] Bones Studio, “BONES-SEED: Skeletal everyday embodiment dataset,” https://bones.studio/datasets/seed, 2026. 

- [21] L. Yang, B. Werner, M. de Sa, and A. D. Ames, “Cbf-rl: Safety filtering reinforcement learning in training with control barrier functions,” _arXiv preprint arXiv:2510.14959_ , 2025. 

- [22] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [23] ccrpRepo, “AMP ~~m~~ jlab: G1 AMP motion control on mjlab + rsl ~~r~~ l,” https://github.com/ccrpRepo/AMP ~~m~~ jlab, 2025. 

- [24] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [25] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural network,” _stat_ , vol. 1050, p. 9, 2015. 

- [26] N. Shazeer, A. Mirhoseini, K. Maziarz, A. Davis, Q. Le, G. Hinton, and J. Dean, “Outrageously large neural networks: The sparsely-gated mixture-of-experts layer,” _arXiv preprint arXiv:1701.06538_ , 2017. 

- [27] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [28] F. Liu, Z. Gu, Y. Cai, Z. Zhou, H. Jung, J. Jang, S. Zhao, S. Ha, Y. Chen, D. Xu, _et al._ , “Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid loco-manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [29] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” _arXiv preprint arXiv:2509.26633_ , 2025. 

- [30] L. Penco, B. Cl´ement, V. Modugno, E. M. Hoffman, G. Nava, D. Pucci, N. G. Tsagarakis, J.-B. Mouret, and S. Ivaldi, “Robust real-time wholebody motion retargeting from human to humanoid,” in _2018 IEEE-RAS_ 

_18th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2018, pp. 425–432. 

- [31] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” _arXiv preprint arXiv:2510.02252_ , 2025. 

- [32] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. M. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous human-tohumanoid whole-body teleoperation and learning,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 1516–1540. 

- [33] Z. Zhang, C. Chen, H. Xue, J. Wang, S. Liang, Y. Liu, Z. Zhang, H. Wang, and L. Yi, “Unleashing humanoid reaching potential via real-world-ready skill space,” _IEEE Robotics and Automation Letters_ , vol. 11, no. 2, pp. 2082–2089, 2025. 

- [34] Y. Fu, F. Xie, C. Xu, J. Xiong, H. Yuan, and Z. Lu, “Demohlm: From one demonstration to generalizable humanoid loco-manipulation,” _arXiv preprint arXiv:2510.11258_ , 2025. 

- [35] Z. Su, B. Zhang, N. Rahmanian, Y. Gao, Q. Liao, C. Regan, K. Sreenath, and S. S. Sastry, “Hitter: A humanoid table tennis robot via hierarchical planning and learning,” _arXiv preprint arXiv:2508.21043_ , 2025. 

- [36] J. Dao, H. Duan, and A. Fern, “Sim-to-real learning for humanoid box loco-manipulation,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 16 930–16 936. 

- [37] H. Jiang, J. Chen, Q. Bu, L. Chen, M. Shi, Y. Zhang, D. Li, C. Suo, C. Wang, Z. Peng, _et al._ , “Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control,” _arXiv preprint arXiv:2512.11047_ , 2025. 

- [38] S. Wei, H. Jing, B. Li, Z. Zhao, J. Mao, Z. Ni, S. He, J. Liu, X. Liu, K. Kang, _et al._ , “Ψ0: An open foundation model towards universal humanoid loco-manipulation,” _arXiv preprint arXiv:2603.12263_ , 2026. 

- [39] H. Yuan, Y. Bai, Y. Fu, B. Zhou, Y. Feng, X. Xu, Y. Zhan, B. F. Karlsson, and Z. Lu, “Being-0: A humanoid robotic agent with vision-language models and modular skills,” _arXiv preprint arXiv:2503.12533_ , 2025. 

- [40] H. Xue, X. Huang, D. Niu, Q. Liao, T. Kragerud, J. T. Gravdahl, X. B. Peng, G. Shi, T. Darrell, K. Sreenath, _et al._ , “Leverb: Humanoid whole-body control with latent vision-language instruction,” _arXiv preprint arXiv:2506.13751_ , 2025. 

- [41] Y. Zhao, X. Wang, D. Wang, X. Liu, D. Lu, Q. Han, P. Liu, and C. Bai, “Towards adaptive humanoid control via multi-behavior distillation and reinforced fine-tuning,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 40, no. 22, 2026, pp. 18 818–18 826. 

- [42] Y. Wang, M. Yang, G. Ding, Y. Zhang, W. Zeng, X. Xu, H. Jiang, and Z. Lu, “From experts to a generalist: Toward general wholebody control for humanoid robots,” _Advances in Neural Information Processing Systems_ , vol. 38, pp. 147 748–147 772, 2026. 

- [43] Q. Peng, Y. Lin, Y. Xue, J. Pang, and W. Zhang, “Embodimentaware generalist specialist distillation for unified humanoid wholebody control,” _arXiv preprint arXiv:2602.02960_ , 2026. 

- [44] Z. Wu, X. Huang, L. Yang, Y. Zhang, K. Sreenath, X. Chen, P. Abbeel, R. Duan, A. Kanazawa, C. Sferrazza, _et al._ , “Perceptive humanoid parkour: Chaining dynamic human skills via motion matching,” _arXiv preprint arXiv:2602.15827_ , 2026. 

- [45] J. Li, B. Tang, and F. Wu, “Telegate: Whole-body humanoid teleoperation via gated expert selection with motion prior,” _arXiv preprint arXiv:2602.09628_ , 2026. 

- [46] C. Tessler, Y. Guo, O. Nabati, G. Chechik, and X. B. Peng, “Maskedmimic: Unified physics-based character control through masked motion inpainting,” _ACM Transactions On Graphics (TOG)_ , vol. 43, no. 6, pp. 1–21, 2024. 

- [47] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel, “Asymmetric actor critic for image-based robot learning,” _Robotics: Science and Systems XIV_ , 2018. 

- [48] N. Poddar, S. McCrory, L. Penco, G. Clark, H. E. Svil, and R. Griffin, “Embedding classical balance control principles in reinforcement learning for humanoid recovery,” _arXiv preprint arXiv:2603.08619_ , 2026. 

- [49] K. Zakka, Q. Liao, B. Yi, L. L. Lay, K. Sreenath, and P. Abbeel, “mjlab: A lightweight framework for gpu-accelerated robot learning,” _arXiv preprint arXiv:2601.22074_ , 2026. 

- [50] C. Schwarke, M. Mittal, N. Rudin, D. Hoeller, and M. Hutter, “Rsl-rl: A learning library for robotics research,” _arXiv preprint arXiv:2509.10771_ , 2025. 

- [51] K. Zakka, “mink: Python inverse kinematics based on MuJoCo,” https: //github.com/kevinzakka/mink, 2024. 

