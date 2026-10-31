---
title: "CoorDex: Coordinating Body and Hand Priors for Continuous Dexterous Humanoid Loco-Manipulation"
date: "2026-06-22"
authors: "Sikai Li; Shuning Li; Zhenyu Wei; Yunchao Yao; Chenran Li; Mingyu Ding"
url: https://arxiv.org/abs/2606.23680
pdf: https://arxiv.org/pdf/2606.23680
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.23680)** / [論文ページ](https://arxiv.org/abs/2606.23680)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CoorDex: Coordinating Body and Hand Priors for Continuous Dexterous Humanoid Loco-Manipulation** 

**Sikai Li**<sup>1</sup> **, Shuning Li**<sup>1</sup> **, Zhenyu Wei**<sup>1</sup> **, Yunchao Yao**<sup>1</sup> **, Chenran Li**<sup>2</sup> **, Mingyu Ding**<sup>1</sup> 1University of North Carolina at Chapel Hill 2University of California, Berkeley 


Figure 1: **Dexterous loco-manipulation on the move.** CoorDex enables a humanoid equipped with high-DoF dexterous hands to perform continuous loco-manipulation tasks that require simultaneous coordination between locomotion and dexterous hand control, such as walk-grasp-carry, fridge opening while stepping back, and walk-pick-turn. 

**Abstract:** Humanoid loco-manipulation is often simplified into a stop-and-go process: walking to an object, stopping to manipulate it, and then resuming locomotion. It also commonly relies on low degree-of-freedom (DoF) end effectors that behave like an open-close grasp primitive. We introduce **CoorDex** , a learning pipeline that converts high-dimensional body and dexterous hand control into coordinated latent residual control, enabling high-DoF dexterous locomanipulation on the move. Starting from simulated whole-body and hand demonstrations, CoorDex trains privileged motion tracking teachers for the humanoid body and dexterous hand, distills them into proprioception-conditioned latent priors, and uses the frozen priors as the action space for downstream residual reinforcement learning. A coordinated latent residual policy composes these priors through shared task context and separate body-hand residual heads, preserving natural whole-body motion while improving finger-level contact reliability. CoorDex enables a Unitree G1 humanoid with a 20-DoF WUJI hand to execute dexterous manipulation while in motion, including non-stop bottle grasping and carrying, fridge door opening on the move, and cube pick-andturn. Ablations on the walk-grasp-carry task show that joint-space PPO, jointspace hand control, and monolithic latent prediction all fail under the same reward budget, while the latent-prior interface and coordinated residual structure make high-dimensional contact-rich loco-manipulation trainable. Project Page: `https://skevinci.github.io/coordex/` 

**Keywords:** Dexterous Loco-manipulation, Humanoids, Body-hand Coordination 

## **1 Introduction** 

Humanoid robots equipped with high-DoF dexterous hands promise a single embodiment that can both navigate human environments and manipulate everyday objects. Realizing this promise requires more than placing an end effector near a target. The robot must maintain balance, keep the object reachable, coordinate wrist and finger poses before contact, close the hand without disturbing the object, and continue transporting the object while hand-object interactions perturb whole-body dynamics. Learning such behaviors directly over all actuated joints creates a challenging highdimensional exploration problem, where locomotion and dexterous hand control must be simultaneously coordinated throughout execution. 

Recent progress has advanced complementary parts of humanoid loco-manipulation. Whole-body tracking enables stable locomotion and expressive upper-body motion [1, 2, 3, 4, 5, 6, 7]. Physicsbased priors reduce exploration through structured latent action spaces [8, 9, 10, 11, 12]. Teleoperation, residual learning, hierarchical control, force-adaptive policies, and vision-conditioned systems further improve task-level interaction and sim-to-real transfer [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]. However, many systems still use end-effector-centric, low-dimensional, or primitive-based manipulation interfaces, leaving high-DoF multi-finger contact during continuous locomotion remains less isolated and less understood. 

This limitation is especially pronounced in on-the-move dexterous loco-manipulation. Current handcentric methods have made strong progress in grasp synthesis, hand-object representation, crossembodiment transfer, and demonstration generation [24, 25, 26, 27, 28, 29, 30, 31]. Yet they often assume that the wrist or arm trajectory is provided by teleoperation, planning, a fixed-base setup, or a stationary whole-body controller. As a result, existing humanoid loco-manipulation systems are often simplified into a stop-and-go process: walking to an object, stopping to manipulate it, and then resuming locomotion. On a walking humanoid, however, the wrist pose emerges from foot timing, root motion, torso posture, and whole-body reaching. A hand prior that must also explain 6D wrist motion therefore spends much of its capacity on body-side placement rather than on finger coordination. The key challenge is to decompose and coordinate body-side wrist placement with hand-side finger motion during continuous locomotion. 

We introduce **CoorDex** , a learning pipeline that makes high-DoF dexterous humanoid locomanipulation trainable through coordinated latent residual control. It targets dexterous manipulation on the move, where wrist placement emerges from whole-body motion, by separating whole-body wrist placement from finger coordination, modeling them with a body prior and a wrist-stabilized hand prior, and coupling them through a coordinated latent residual policy. Specifically, CoorDex first constructs separate latent priors for the humanoid body and dexterous hand. Each prior is trained from a privileged motion tracking teacher and distilled into a proprioception conditioned student prior and decoder using a variational bottleneck [11]. The body prior supports locomotion, reaching, and wrist placement, while the wrist-stabilized hand prior controls only the active finger joints and captures reusable finger coordination. This factorization replaces direct full-joint control with residual control over two compact latent spaces, separating body-side placement from hand-side dexterity while preserving their downstream coordination. 

To compose these priors, CoorDex uses a coordinated latent residual policy. At each control step, the frozen body and hand priors first encode their respective proprioception into latent means. These means, together with object-relative geometry, contact features, and the current proprioceptive state, are passed to a shared coordination trunk to produce a task-level coordination feature. Two residual heads then predict body and hand latent corrections, which are added to the corresponding prior means before decoding. The body residual adjusts stepping, torso motion, reaching, and wrist placement, whereas the hand residual refines finger preshape, closure, and contact. This design couples the two subsystems through shared task state without collapsing them into a single monolithic action head. It preserves the structural separation between whole-body motion and finger-level dexterity. 

Our contributions are threefold. **1)** We present a complete learning pipeline in Isaac Lab [32] for high-DoF dexterous humanoid loco-manipulation, including simulated whole-body and hand 

2 

demonstration collection, motion tracking policies, prior distillation, and downstream residual RL. **2)** We propose an asymmetric body-hand prior composition for high-dimensional control. Wrist placement emerges from whole-body motion from a task-aligned body prior, while a wrist-stabilized hand prior captures reusable finger skills. A coordinated latent residual policy adapts the frozen priors through shared task context and body-hand residual heads. **3)** We provide ablations on the walkgrasp-carry task showing that raw joint-space PPO, the body prior with joint-space hand control, and monolithic latent prediction all fail under the same reward budget, highlighting the importance of both latent-prior actions and structured body-hand coordination for dexterous loco-manipulation. 

## **2 Related Work** 

**Motion Imitation and Motion Priors.** Physics-based motion imitation enables high-dimensional humanoid control. DeepMimic [1] combines reference motion tracking with task rewards to produce robust simulated skills. Recent humanoid trackers scale this idea to full-body robots by improving motion retargeting, adaptive tracking, privileged training, and sim-to-real deployment, enabling expressive locomotion, whole-body teleoperation, and highly dynamic behaviors [3, 4, 5, 6, 2, 33, 7, 34, 35, 36, 37]. A related line learns latent motion priors that replace raw joint actions with more structured action spaces. AMP [8] and ASE [9] use adversarial objectives to regularize or parameterize downstream control, while CALM [10], PULSE [11], and SLMP [12] further study conditional or compact latent representations for reusable physics-based skills. Building on prior work that learns motion priors for humanoid body control, we extend the same principle to dexterous hand control by constructing a separate hand prior. CoorDex then studies how to compose the body and hand priors for downstream contact-rich loco-manipulation tasks. 

**Dexterous Hand Manipulation.** Dexterous hand research provides tools for grasp synthesis, handobject representation, and manipulation data generation. Large-scale datasets and generative methods synthesize diverse multi-finger grasps over objects and hand morphologies [24, 25, 26, 38, 39, 40]. Cross-embodiment representations such as _D_ ( _R, O_ ) Grasp [27] and OHRA [28] encode hand-object geometry or hand morphology in forms that transfer across different dexterous hands. Demonstration generation and transfer systems such as ManipTrans [29], DexMimicGen [30], and Jacta [31] use human motions, planners, or few demonstrations to bootstrap dexterous manipulation through tracking, imitation, and residual refinement. While these methods provide effective supervision for finger-level dexterity, they typically assume that wrist motion is externally provided. CoorDex targets a walking humanoid, where wrist placement emerges from whole-body motion. 

**Humanoid Loco-Manipulation.** Humanoid loco-manipulation couples locomotion, reaching, contact, and object transport. Existing approaches address this coupling from several directions. Optimization and residual-learning methods generate or refine dynamically feasible whole-body behaviors for object interaction [41, 16, 17]. Skill composition and unified whole-body controllers widen the range of reachable tasks, while force-adaptive policies make humanoids more robust to payloads and contacts [18, 20, 19]. Teleoperation systems provide high-quality humanoid demonstrations and have begun to include dexterous hands [13, 42, 15]. Vision-based systems push loco-manipulation toward large-scale sim-to-real transfer and language- or video-conditioned control [21, 22, 23]. We isolate the control problem of continuous high-DoF dexterous loco-manipulation, where grasp formation and object transport occur during ongoing walking rather than in a stationary manipulation phase. This setting is closer to finger-level humanoid dexterity than to standard mobile manipulation, where navigation and manipulation can be separated in time. 

## **3 Method** 

We present CoorDex, a modular pipeline that maps high-dimensional humanoid locomotion and dexterous hand control to coordinated latent residual control (Fig. 2). It builds separate body and hand priors and trains a downstream residual RL policy to coordinate them. Sec. 3.1 describes prior construction via teacher tracking and proprioceptive distillation; Sec. 3.2 introduces the coordinated latent residual policy; and Sec. 3.3 details residual PPO [43] training and environment design. 

3 


Figure 2: **Overview of CoorDex** . Body and hand reference motions are tracked by privileged teachers and distilled into separate proprioception-conditioned latent priors. During downstream RL, a coordinated residual policy uses task context and prior means to predict body and hand latent residuals. The frozen decoders map the corrected latents to joint-position targets for loco-manipulation. 

### **3.1 Prior Construction** 

We construct two separate motion priors, one for the humanoid body and one for the dexterous hand. The two priors are trained on different tracking tasks but share the same distillation pipeline. Let _x ∈{b, h}_ denote the body or hand subsystem. 

**Demonstration collection in simulation** We collect task reference motions in Isaac Lab through a simulated teleoperation pipeline. Lower-body locomotion is generated by an AGILE-based locomotion controller [44], while the operator provides right wrist and hand motion through Apple Vision Pro using the CloudXR-based XR teleoperation interface in Isaac Lab [32]. The tracked human wrist pose serves as the end-effector target for a Pink inverse-kinematics solver, and human hand motion is retargeted to the target dexterous hand with optimization-based dex-retargeting [45]. The resulting whole-body trajectories provide the reference motions for body tracking training. 

**Humanoid body prior.** For the body subsystem, we first train a general whole-body motion tracking teacher _πT_<sup>_b_[2].The teacher takes body proprioception</sup><sup>**s**</sup> _t_<sup>_b,p_</sup> and a reference goal **s**<sup>_b,g_</sup> _t_ as input, and outputs joint position targets **a**<sup>_b,T_</sup> _t_ for the body joints. Before training, we preprocess each reference motion on the humanoid model equipped with the corresponding dexterous hands. The resulting reference trajectories thus match the morphology and kinematic structure used in our downstream loco-manipulation tasks. 

**Dexterous hand prior.** For the hand subsystem, we train a privileged hand tracking teacher _πT_<sup>_h_in a</sup> floating-hand environment using ManipTrans-style [29] retargeted hand-object motions. The teacher observes hand proprioception **s**<sup>_h,p_</sup> _t_ and a reference goal **s**<sup>_h,g_</sup> _t_ , and outputs joint position targets **a**<sup>_h,T_</sup> _t_ for the active finger joints. During hand-prior training, the reference wrist pose and velocity are written directly into simulation, so the teacher and the learned prior control only finger motion. This wrist-stabilized design keeps the hand latent space from spending most of its capacity on 6D wrist motion, and makes the learned latent command directly useful for finger coordination. 

**Distillation.** After training the tracking teachers, we distill each teacher into a proprioception conditioned latent prior [11]. For each subsystem _x ∈{b, h}_ , the student contains an encoder _Ex_ ( **z**<sup>_x_</sup> _t_<sup>_|_</sup><sup>**s**</sup> _t_<sup>_x,g_</sup> _,_ **s**<sup>_x,p_</sup> _t_ ), a proprioceptive prior _Rx_ ( **z**<sup>_x_</sup> _t_<sup>_|_</sup><sup>**s**</sup> _t_<sup>_x,p_</sup> ), and a decoder _Dx_ ( **s**<sup>_x,p_</sup> _t ,_ **z**<sup>_x_</sup> _t_<sup>).The training</sup> objective combines teacher-action reconstruction, temporal smoothness of the encoder means, and 

4 

KL regularization between the encoder and the prior: 

_L_<sup>_x_</sup> distill<sup>=</sup><sup>_Lx_</sup> action<sup>+</sup><sup>_αxLx_</sup> regu<sup>+</sup><sup>_βxL_</sup> KL<sup>_x._</sup> (1) 

After distillation, _Rx_ and _Dx_ are frozen, and the prior mean **_µ_**<sup>_x,p_</sup> _t_ provides the default latent command for downstream residual RL. Full definitions are given in Appendix A. 

### **3.2 Coordinated Latent Residual Policy** 

Given the frozen body and hand priors, a downstream residual PPO [43] policy coordinates and adapts them for the loco-manipulation task. At each control step, we obtain the proprioception conditioned prior means from the frozen prior networks: 


The actor predicts residuals in the two latent spaces rather than joint-space targets: 

The actor first computes a shared coordination representation **c** _t_ to capture body-hand coupling, and then predicts residual commands through a specialized body head _fb_ and hand head _fh_ : 


Here **s**<sup>task</sup> _t_ contains task-level state such as object pose, goal information, projected gravity, and contact features. The hand-object state **s**<sup>hand</sup> _t_<sup>-object</sup> includes the object pose in the hand frame and fingertip-object contact features. 

The corrected latent commands are 


The final joint position targets are produced by the frozen decoders: 


The body decoder outputs targets for all humanoid body joints. The hand decoder outputs targets for the active finger joints of the selected dexterous hand. These targets are inserted into the corresponding joint slots and executed by a low-level PD controller. This architecture keeps downstream exploration low-dimensional while preserving separate control authority for locomotion and grasping. The shared coordination trunk lets the policy reason about task phase and contact state. The separate heads let the body residual adapt stepping, torso motion, reaching, and wrist placement, and let the hand residual adapt finger preshape, closure, and contact refinement. 

### **3.3 Residual RL and Environment Design** 

We train downstream policies with PPO while keeping the body and hand priors frozen. The policy observation contains body proprioception, hand proprioception, task state, object-relative geometry, fingertip contact features, the prior means, and the previous latent residual. Since the actor outputs only ∆ **z** _t_ , exploration happens in the learned body and hand latent spaces rather than in the full joint-position action space. 

All tasks use the same latent residual interface but differ in their interaction structure and exploration difficulty. The priors used by different tasks are not identical, since each task needs different coarse motion support. For shorter interaction tasks such as walk-grasp-carry and fridge door opening, we use a single-stage reward without reference state initialization. The reward combines locomotion and balance terms, palm-object reaching and alignment terms, fingertip contact and sustained contact terms, task-completion terms such as lift, carry, or door-angle progress, and regularization on latent residuals, decoded action changes, and joint velocities. For the longer-horizon walk-pick-turn task, pure reward optimization from the initial state is unreliable. We therefore use a lightweight staged reward together with demonstration-free reference state initialization (NoDemoRSI), which resets part of the episodes from states the policy itself has reached. This curriculum is task-specific and is not part of the policy architecture. More details are given in Appendix B. 

5 

Table 2: Task performance of CoorDex. Results are evaluated over 50 _,_ 000 episodes collected with 10 _,_ 000 parallel simulation environments in Isaac Lab. 

|Task|Success|Fall|Drop|Task-specific metric|
|---|---|---|---|---|
|WALKGRAB|0.55|0.00|0.40|Velocity profile, Fig.4|
|OPENFRIDGE|0.66|0.00|–|Door angle: 57.76 /60<sup>_◦_</sup>|
|WALKPICKTURN|0.89|0.01|0.10|Min heading err.: 9.98<sup>_◦_</sup>|


## **4 Experimental Results** 

We evaluate the core design components of **CoorDex** in Isaac Lab [32]. Our experiments use a 29DoF Unitree G1 humanoid [46] equipped with a 20-DoF five-finger WUJI dexterous hand [47]. We study three questions. **Q1.** Whether a unified body–hand latent residual interface supports diverse loco-manipulation skills. **Q2.** Whether latent actions improve exploration over direct joint-space control. **Q3.** Whether coordinated residual prediction improves over monolithic latent prediction. 

### **4.1 Experiment Setup** 

**Tasks.** We consider three dexterous humanoid loco-manipulation Table 1: Actuated degrees of tasks with different interaction structures. In WALKGRAB, the freedom and latent dimensions. humanoid must grasp and lift a bottle from a side table while Subsystem DoF Latent dim. continuously walking forward. In OPENFRIDGE, it must grasp G1 body 29 16 a fridge handle and open the door while stepping backward to WUJI hand 20 12 create workspace. In WALKPICKTURN, it must approach a table, pick up a cube, and complete a 180<sup>_◦_</sup> turn while retaining the object. The three tasks respectively stress dynamic grasping during locomotion, sustained articulated-object interaction, and long-horizon skill composition. Fig. 1 visualizes the three tasks. Table 1 summarizes the action dimensions. 

**Evaluation metrics.** Unless stated otherwise, all metrics are computed over 50 _,_ 000 evaluation episodes collected with 10 _,_ 000 parallel simulation environments. We report task success, fall rate, drop rate when applicable, and task-specific progress metrics. A rollout counts as successful only if the task-specific completion condition is satisfied and the robot stays balanced. WALKGRAB requires lifting and carrying the bottle beyond a target displacement, OPENFRIDGE requires the maximum door angle to exceed the success threshold, and WALKPICKTURN requires grasping, lifting, and retaining the cube while completing a 180<sup>_◦_</sup> turn. Exact thresholds are provided in Appendix B.4. We additionally report diagnostic metrics, including door angle, heading error, and action rate. 

**Controlled variants on WALKGRAB.** We use WALKGRAB as the main controlled ablation task because it is the cleanest test of grasping during locomotion. It uses a single-stage reward, does not use reference state initialization, and directly couples root motion, wrist placement, and finger closure. We compare CoorDex with three variants under the same environment and task-level reward. _All Joint Space_ removes both latent priors and predicts joint targets directly. _Body Prior + Hand Joint Space_ keeps the body prior but controls the hand in joint space. _Monolithic Latent Residual_ keeps both priors but predicts one concatenated residual vector with a single MLP. Since the action parameterizations differ, we compare task-level metrics rather than raw return. 

### **4.2 Task Performance Across Skills** 

Table 2 shows that the same CoorDex interface can be instantiated across all three tasks, answering **Q1** . WALKGRAB is the most challenging because grasping must happen under continuous wholebody motion, whereas OPENFRIDGE permits the robot to slow down and reposition during manipulation. WALKPICKTURN is longer-horizon, but NoDemoRSI provides additional exploration support by resetting later stages from states discovered by the policy itself, without any expert states or action labels. Implementation details are given in Appendix B. 

6 

Table 3: Action-space variants on WALKGRAB under the same PPO budget. Reach, grasp, stop, and fall are rates over evaluation episodes. 

|Method|Succ|ess<br>Reach<br>Grasp|Stop<br>Fall|
|---|---|---|---|
|All Joint Spa<br>Body Prior +<br>**CoorDex**|ce<br>0<br>Hand Joint Space<br>0<br>0.5|1.00<br>0.00<br>0.96<br>0.01<br>5<br>1.00<br>0.55|0.86<br>0.04<br>0.90<br>0.04<br>0.00<br>0.00|
|All Joint Space|Body Prior + Hand Joint Space|Monolithic Latent Residual|**CoorDex (Ours)**|
|Approach|Approach|Approach|Approach|
|Pre-grasp|Pre-grasp|Pre-grasp|Pre-grasp|
|Grasp fail|Grasp fail|Grasp fail|Grasp|
|Bottle fall|Bottle fall|Bottle fall|Carry|


Figure 3: **Qualitative comparison on WALKGRAB.** Each column shows sequential key frames from one rollout of the corresponding method. All Joint Space produces unstable whole-body motion. Body Prior + Hand Joint Space reaches the bottle but fails to learn a reliable grasp. Monolithic Latent Residual reaches the interaction region but produces less natural body motion and fails to complete the task. **CoorDex** completes the full sequence of approach, grasp, lift, and carry. 

### **4.3 Action-Space Variants on WALKGRAB** 

We next study whether the latent-prior action interface is necessary for WALKGRAB, answering **Q2** . This task directly tests the definition of non-stop dexterous loco-manipulation: the robot must grasp an object while it keeps moving forward. Table 3 compares the action-space variants under the same environment and task reward. 

**Metrics.** Reach measures whether the palm enters a predefined distance threshold from the bottle. Grasp measures whether the bottle is lifted above the task threshold. Stop measures whether the humanoid slows below a velocity threshold near the bottle. Fall measures robot-fall termination. 

The two failed variants reveal different failure modes, also visible in Fig. 3. All Joint Space removes both learned priors and must explore the full body and hand joint space. The policy often twists the whole body into unnatural postures to avoid falling, and it never grasps the bottle. 

Body Prior + Hand Joint Space isolates the hand-side difficulty. With the body prior, the humanoid can walk toward the bottle and place the wrist near the interaction region. However, the policy still has to discover high-DoF finger coordination directly in joint space. In practice, it often learns to slow down or stop near the bottle and tries to solve the problem as a stationary grasping task. This behavior shows that the body prior alone is not enough for non-stop dexterous loco-manipulation. The hand prior is also needed to make finger coordination learnable under residual RL. 

For WALKGRAB, we also analyze non-stop behavior with a velocity profile. For each rollout, we compute the body-frame forward velocity _vx,t_<sup>body</sup> and the relative forward po- 

7 

sition _dt_ = _x_<sup>robot</sup> _t − x_<sup>bottle</sup> _t_ . We bin samples by _dt_ with bin width 0 _._ 05 m over the range [ _−_ 3 _._ 0 _,_ 0 _._ 5] m, and plot the mean and standard deviation of _vx,t_<sup>body</sup> in each bin. As shown in Fig. 4, CoorDex slows down slightly near the bottle but still keeps a forward velocity around 0 _._ 25 m _/_ s near _dt_ = 0. This indicates that the policy does not solve the task by stopping before grasping. 

### **4.4 Coordinated Residual Prediction** 

We finally test whether the actor structure matters once both priors are available, answering **Q3** . Monolithic Latent Residual and CoorDex 

Figure 4: Non-stop locomotion on WALKGRAB. 

use the same frozen body and hand priors, the same latent dimensions, and the same RL environment and reward. The only difference is the policy architecture. Monolithic Latent Residual uses one MLP to predict the full latent residual and then splits it into body and hand parts. CoorDex uses a shared coordination trunk with separate body and hand residual heads. 

**Metrics.** Action rate measures the average change of decoded body joint targets between consecutive control steps. A lower action rate indicates smoother and more natural body motion. 

|Table 4 and Fig. 3 show that the coordi-<br>nated actor matters even when both priors|Table 4: Coordination analysis on|WALKGR|AB.|
|---|---|---|---|
|are present. The monolithic actor can of-|Method<br>Success|Action rate|Fall|
|ten follow the task direction and approach<br>the bottle, but its body motion is less nat-<br> l|Monolithic Latent Residual<br>0.00<br>**CoorDex**<br>**0.55**|0.40<br>**0.22**|0.02<br>0.00|
|ural and more jittery. This is reflected in||||


the higher action rate in Table 4 and the unstable torso motion visible in Fig. 3. The hand failure is harder to see because the fingers are small, but the zero success rate shows that monolithic latent prediction does not produce reliable grasping under the same reward budget. CoorDex performs better because the shared trunk lets the policy reason about the same task state, while the separate heads keep body adaptation and finger adaptation from being forced through a single output pathway. 

## **5 Discussion and Limitations** 

We present CoorDex, a modular pipeline for dexterous loco-manipulation. Rather than treating locomotion and manipulation as two separate phases, CoorDex exposes a structured latent action space for the humanoid body and the dexterous hand. Within this space, downstream RL can jointly adapt stepping, wrist placement, and finger-level contact. Across bottle grasping and carrying, fridge door opening, and cube pick-and-turn, the results indicate that dexterous humanoid skills benefit from priors that provide task-relevant motion support, and from policies that preserve the structure of body-hand coordination. This points to a practical direction for future loco-manipulation systems. Reusable motion priors should be paired with task-aware latent coordination, treating whole-body mobility and dexterous contact as coupled behaviors rather than stitched-together modules. 

**Limitations and Future Work.** Although CoorDex demonstrates continuous high-DoF dexterous loco-manipulation across multiple simulated tasks, our results are still an early step toward general humanoid dexterity. The current policies use privileged state observations, including object poses and contact signals, and do not yet address perception or visual sim-to-real transfer. The experiments also focus on a fixed G1 platform with a WUJI hand, and broader deployment will require evaluation across more objects, hands, and hardware configurations. Finally, longer-horizon tasks such as WALKPICKTURN still rely on task-specific exploration support such as NoDemoRSI. Future work should combine the proposed latent residual interface with perception, automatic curricula, and broader task-conditioned priors. 

8 

# **Appendix** 

## **A Motion Prior Implementation Details** 

This section describes the implementation for building the body and hand priors that are later composed by the downstream residual policy. The body tracker extends the motion tracking design used by BeyondMimic [2]. References are represented as joint trajectories and Cartesian body targets, the policy tracks them through normalized joint-position setpoints, and the critic receives additional privileged tracking information. The hand tracker is trained with PPO to track MANO keypoints retargeted to robot hand bodies [29]. The distillation stage learns an encoder–decoder latent skill space together with a proprioception-conditioned prior [11]. 

### **A.1 Humanoid Body Tracking Teacher** 

The robot is a Unitree G1 [46] with fixed WUJI hands [47]. Only the 29 body joints are actuated for training efficiency. The reference bodies used by the tracking objective include the pelvis, leg links, torso, arm links, and wrist links; finger bodies are excluded from the body prior. Actions are normalized joint position setpoints with joint-specific scales derived from actuator effort and stiffness. The simulation uses decimation 4 and a physics step of 1 _/_ (60 _·_ 4) seconds, giving a 60 Hz control rate and 10 second episodes. 

The no-state-estimator body teacher removes anchor translation and base linear velocity from the actor and teacher observations for real-world deployment. Per frame, the deployable proprioceptive suffix is 

[ _ω_ base _, q, q, a_ ˙ _t−_ 1] _∈_ R<sup>90</sup> _,_ 

where _q, q, a_ ˙ _t−_ 1 each have 29 body-joint dimensions. The actor also receives the current motion command and relative anchor orientation during teacher training, with a five-frame history. The critic is asymmetric and additionally observes privileged reference body pose and velocity errors. 

Rewards are exponential tracking rewards plus minimal regularization. The main positive terms track anchor position and orientation, relative body position and orientation, body linear and angular velocity, and palm keypoints. Penalties discourage action rate jitter, joint limit violations, and undesired contacts. Episodes terminate on timeout, excessive anchor height or orientation error, or excessive end-effector height error at the ankles and wrist yaw links. Domain randomization includes friction, joint default offsets, torso center-of-mass perturbation, and random base pushes. 

The teacher is trained with PPO using 24 rollout steps per environment, five learning epochs, four minibatches, _γ_ = 0 _._ 99, _λ_ = 0 _._ 95, adaptive learning rate with target KL 0.01, learning rate 10<sup>_−_3</sup> , entropy coefficient 0.005, and gradient clipping at 1.0. Actor and critic MLPs use ELU activations and hidden dimensions [1024 _,_ 512 _,_ 256]. 

### **A.2 Dexterous Hand Tracking Teacher** 

Our hand motion loader reads ManipTrans-style annotations [29], evaluates SMPL-X to obtain MANO wrist and finger keypoints, converts from the MuJoCo frame to the Isaac Lab frame, and downsamples 120 Hz annotations to 60 Hz. 

For the current WUJI hand prior, the tracked hand bodies are the palm and the five finger links and tips. The environment writes the reference wrist root pose and velocity into simulation both at command resampling and during every command update, so the wrist is kinematically driven by the dataset. The policy therefore controls only the twenty active finger joints for WUJI hand. This fingers-only action space avoids spending latent capacity on high-variance wrist motion and matches the downstream residual interface, where the humanoid body prior determines the wrist motion. 

The policy observation concatenates a target command, hand proprioception, and the previous action. The target command contains flattened MANO keypoint positions and velocities, plus the reference wrist pose expressed relative to the simulated wrist. Proprioception contains wrist linear 

9 

and angular velocity in the wrist frame, and active joint position and velocity relative to default joint states. The critic receives the same target and proprioception plus privileged per-body keypoint position and velocity deltas. 

The remaining rewards track MANO keypoints with fingertip-heavy weights, track keypoint velocities, penalize joint power through an exponential power reward, and penalize action rate. Tracking failure terminates an episode if keypoint errors exceed group-specific thresholds after a short warmup. An additional unstable state termination catches unrealistic wrist, body, or joint velocities. PPO hyperparameters match the body teacher: 24 rollout steps, five epochs, four minibatches, ELU MLPs with [1024 _,_ 512 _,_ 256] hidden units, learning rate 10<sup>_−_3</sup> , adaptive KL target 0.01, and 4096 environments. 

### **A.3 VAE Distillation** 

The student contains three trainable networks: 


The encoder predicts the posterior diagonal Gaussian from the full student observation. The prior predicts a diagonal Gaussian from the deployable proprioceptive slice. And the decoder maps proprioception plus a latent sample to the teacher action. During training, _zt_ is sampled from the encoder with the reparameterization trick. At inference and downstream residual RL time, the default latent is the prior mean. 

The distillation loss is 

_L_ = _λa∥a_ ˆ _t − a_<sup>_T_</sup> _t_<sup>_∥_</sup> 2<sup>2+</sup><sup>_λs∥µq_</sup> _t_<sup>_−µq_</sup> _t−_ 1<sup>_∥_</sup> 2<sup>2+</sup><sup>_λ_KL</sup><sup>_D_KL</sup> � _qϕ_ ( _zt | st_<sup>full</sup> ) _∥ pψ_ ( _zt | st_<sup>prop</sup> )� _,_ 

where the smoothness term is evaluated only across valid consecutive samples in the same environment. This mirrors the PULSE [11] motivation. The decoder learns the teacher’s motor actions. The prior makes the latent usable from proprioception alone. And the temporal regularizer keeps nearby states from mapping to discontinuous latent codes. 

For the body prior, the latent dimension is 16. The proprioceptive prior input is the five-frame suffix 


dimensions. Encoder, decoder, and prior networks are MLPs with [512 _,_ 256 _,_ 128]. The body distillation optimizer uses learning rate 2 _·_ 10<sup>_−_4</sup> , action coefficient 1.0, smoothness coefficient 0.005, and a KL coefficient annealed from 10<sup>_−_3</sup> to 10<sup>_−_4</sup> between 15000 and 20000 updates. 

For the active WUJI hand prior, the latent dimension is 12. The prior input is 66 dimensions: 


The decoder outputs twenty fingers-only actions. The hand distillation optimizer uses learning rate 5 _·_ 10<sup>_−_4</sup> , action coefficient 1.0, smoothness coefficient 0.005, and a KL coefficient annealed from 10<sup>_−_2</sup> to 10<sup>_−_3</sup> between 15000 and 25000 updates. Both distillation runners use 24 rollout steps, five learning epochs, gradient accumulation length 16, gradient clipping at 1.0, empirical observation normalization, and up to 30000 iterations. 

### **A.4 Downstream Residual Composition** 

Downstream loco-manipulation tasks use the frozen priors. The action term loads only the distilled prior and decoder weights, plus the observation normalizer. At each control step it constructs a body-prior observation from the current G1 proprioceptive history and a hand-prior observation from wrist-frame hand velocity, finger joint state, and the previous decoded hand action. 

The downstream PPO actor outputs a residual latent 


For each prior, the action term computes the prior mean and decodes the shifted latent: 


10 

Table 5: Observation terms for the three downstream tasks. Policy and critic share the same layout. 

|WALKGRAB||WALKPICKTUR|N|OPENFRIDGE||
|---|---|---|---|---|---|
|**State term**|**Dim.**|**State term**|**Dim.**|**State term**|**Dim.**|
|Stage one-hot|1|Stage one-hot|3|Stage one-hot|1|
|Projected gravity|3|Projected gravity|3|Projected gravity|3|
|Body prior proprio history|450|Body prior proprio history|450|Body prior proprio history|450|
|Right-hand prior proprio|66|Right-hand prior proprio|66|Right-hand prior proprio|66|
|Last latent action|28|Last latent action|28|Last latent action|28|
|Fingertip forces on bottle|15|Fingertip forces on object|15|Fingertip forces on handle|15|
|Bottle pose, root|9|Object pose, root|9|Fridge pose, root|9|
|Source-table pose, root|9|Source-table pose, root|9|Handle-point pose, root|9|
|Bottle pose, hand|9|Object pose, hand|9|Door pose, root|9|
|Body prior latent mean|16|Body prior latent mean|16|Handle-point pose, hand|9|
|Hand prior latent mean|12|Hand prior latent mean|12|Door joint state<br>|2<br>|
|Total|618|Total|620|Body prior latent mean<br>Hand prior latent mean|16<br>12|
|||||Total|629|


The decoded body actions are inserted into the 29 body-joint slots. The decoded hand actions are converted through the configured joint-action scale and offset into finger targets. An EMA with coefficient 0.4 is applied to the hand targets. The combined joint position action is then sent to the underlying Isaac Lab joint position action term. 

The body prior is a 16-dimensional no-base-linear-velocity G1 prior and the hand prior is the 12dimensional kinematic-wrist WUJI hand prior, yielding a 28-dimensional residual action space. 

## **B Training Details** 

We instantiate three downstream loco-manipulation tasks on the same Unitree G1 humanoid equipped with a WUJI five-finger right hand: **WALKGRAB** , **OPENFRIDGE** , and **WALKPICKTURN** . All three share the same control stack. The policy runs at 60 Hz (physics step 1 _/_ 240 s, decimation 4) over 4096 parallel environments, and emits a 28-dim latent residual (16 body + 12 hand) on top of two frozen priors mentioned above. WALKGRAB and OPENFRIDGE are single-stage reformulations whose phase structure is realized through predicate gating inside the reward terms, whereas WALKPICKTURN keeps an explicit three stage schedule with a stage weighted reward. 

### **B.1 Observation Details** 

For every task the actor and critic observe the same terms. The only difference is that observation noise is enabled for the actor and disabled for the critic. Each observation concatenates the proprioceptive prior stack ( `humanoid` ~~`p`~~ `rior` , a 5-step history of the 90-dim body proprio frame [ _v_ ang<sup>base(3)</sup><sup>_,q_(29)</sup><sup>_,q_˙(29)</sup><sup>_,at−_1(29) ];</sup><sup>`right`</sup> ~~`h`~~ `and` ~~`p`~~ `rior` , the 66-dim hand proprio frame; and the last emitted latent), the frozen prior latent means, contact forces, and task-specific object poses. Object poses are expressed as a 3-D position plus the first two columns of the rotation matrix (6-D), i.e. 9 dims each. Table 5 lists the per-task layouts. 

### **B.2 Reward Details** 

**WALKGRAB and OPENFRIDGE (single-stage).** Both tasks use a single “continuous” stage, so the per-step reward is a flat weighted sum of shaping terms, 


where phase structure is induced by predicate gating _inside_ the terms: a grasp predicate 1[grasped] turns approach terms off and manipulation terms on, and a contact predicate gates the door-opening / lifting rewards so the robot cannot exploit them without touching the object. Tables 6 and 7 list the active terms. 

11 

Table 6: WALKGRAB reward components, expressions, and weights. _d_ denotes a mean distance over the listed bodies; _grasped_ requires mean fingertip–bottle distance _<_ 0 _._ 10 m and at least two fingertip contact sensors above 1 N, including thumb contact. 

|**Term**|**Expression**|**Weight**|
|---|---|---|
|_Task / object-centric rewards_|||
|Hand–bottle distance|1<br>2<br>�<br>exp(_−_8_._5<br>_d_palm+tips)|50_._0|
|Grasp by finger dir|_θ_thumb,others_/π_|40_._0|
|Fingertip contact|mean_i_1[_∥Fi∥>_1]|15_._0|
|Grasp force|clip<br>�<br>mean_i_<br>�_∥Fi∥,_ 0_,_2<br>�<br><br>|15_._0|
|Palm facing object|exp<br>�<br>_−_((cos∠_xy −_0_._47)_/_0_._25)<sup>2�</sup>|15_._0|
|Thumb opposition|�<br>_i _<sup>_wi_ exp(</sup><sup>_−|qi −q∗_</sup><br>_i _<sup>_|_) (4 thumb joints)</sup>|20_._0|
|Others open (penalty)|[1_−_exp(_−_3<br>dev)] + 5 clip(∆err_,_0_,_0_._02)|_−_5_._0|
|Bottle lift height|(min(_ℓ,_0_._05)_/_0_._05) exp(_−_2_v_<sup>2</sup><br>_z_<sup>), grasp-gated</sup>|100_._0|
|Hold bottle|1[grasped]|100_._0|
|Sustained grasp|clip(secs(grasped_∧ℓ>_0_._01)_/_1_._5_,_0_,_1)|100_._0|
|Forward progress|clip(_v_<sup>bottle</sup><br>_x_<br>_/_1_,_0_,_1)1[grasped_∧ℓ>_0_._01]|100_._0|
|_Locomotion / posture shaping_|||
|Forward target|exp<br>�<br>_−_[(_x −_2)<sup>2 </sup>+_y_<sup>2</sup>]<br>�|25_._0|
|Heading forward|exp(_−_(∆_ψ_)<sup>2</sup>_/_0_._3<sup>2</sup>)|10_._0|
|Upright orientation|exp(_−∥gxy∥_<sup>2</sup>_/_0_._2<sup>2</sup>)|5_._0|
|_y_below zero (penalty)|clip(_−y,_0_,_0_._5)|_−_10_._0|
|_Termination / generic penalties_|||
|Success bonus|1[success]|500_._0|
|Action rate|_∥at −at−_1_∥_<sup>2</sup>|_−_0_._01|
|Undesired table contact|�1[contact_>_5N]|_−_20_._0|
|Passed without grasp|1[passed-without-grasp]|_−_20_._0|
|<br>Time-out|1[time-out]|_−_20_._0|
|Robot fall|1[fall]|_−_10_._0|
|Bottle dropped|1[dropped](scaled_×_5once lifted)|_−_1_._0|


**WALKPICKTURN (multi-stage).** A WALKPICKTURN episode is decomposed into stages. Table 8 instantiates _r_<sup>(</sup><sup>_s_)</sup> with the stage-dependent shaping terms. More details can be found in B.5 


### **B.3 Hyperparameter Details** 

All three tasks are trained with PPO under the same actor–critic architecture and optimizer. Only the task-dependent settings (episode length, number of stages, and initial action noise) differ. The actor is a coordinated residual network with a shared coordination trunk that feeds body and hand heads that each output a latent residual on the corresponding frozen prior. The shared PPO settings are listed in Table 9 and the per-task differences in Table 10. 

12 

Table 7: OPENFRIDGE reward components, expressions, and weights. ∆ _θ_ is the door open angle, _c ∈_ _<u>{</u>_ 0 _<u>,</u>_ 1 _<u>}</u>_ the fingertip-contact predicate; the success angle is 60<sup>_◦_</sup> and the held-open angle 35<sup>_◦_</sup> . 

|**Term**|**Expression**|**Weight**|
|---|---|---|
|_Task / object-centric rewards_|||
|Hand–handle distance|exp(_−_10<br>_d_)over_{_5 tips+palm_}_|30_._0|
|Door open amount|clip(∆_θ/_60<sup>_◦_</sup>_,_0_,_1)_· c_<br><sup>˙</sup>|30_._0|
|Door open progress|clip(max(_θ,_0)_/_0_._02_,_0_,_1)_· c_|20_._0|
|Door held open|clip(secs(∆_θ ≥_35<sup>_◦_</sup>_∧c_)_/_1_,_0_,_1)<br>|100_._0|
|Door close regression|clip(max(_−_<sup>˙</sup>_θ,_0)_/_0_._02_,_0_,_1)|_−_20_._0|
|Backward progress|clip(_v_back_/_0_._10_,_0_,_1)_· c_<br>|20_._0|
|Fingertip contact|mean_i_1[_fi >_1] + 0_._25( <sup>max(</sup><sup>_nc−_2</sup><sup>_,_0)</sup><br>3<br>)<sup>2</sup>|15_._0|
|Thumb contact|1[_f_thumb _>_1]|10_._0|
|_Termination / generic penalties_|||
|Success bonus|1[success]|1000_._0|
|Action rate|clip(_∥at −at−_1_∥_<sup>2</sup>_, ≤_100)<br>|_−_0_._01|
|Joint action rate|clip(<sup>�</sup>(_ut −ut−_1)<sup>2</sup>_, ≤_50)|_−_0_._01|
|DoF velocity|clip(<sup>�</sup><br>_j_ <sup>˙</sup><sup>_q_2</sup><br>_j _<sup>_, ≤_200)</sup>|_−_0_._01|
|Feet slip|<br><br>clip(<sup>�</sup><br>feet <sup>1[</sup><sup>_F >_ 5]</sup><sup>_∥vxy∥, ≤_2)</sup>|_−_5_._0|
|Large linear_vx_|<br>min(max(_|vx| −_0_._8_,_0)_,_2)|_−_8_._0|
|Large linear_vy_|min(max(_|vy| −_0_._35_,_0)_,_2)|_−_10_._0|
|Large angular_ω_|min(max(_|ωz| −_0_._6_,_0)_,_5)|_−_10_._0|
|Hand far from handle|1[hand far]|_−_20_._0|
|Time-out|1[time-out]|_−_20_._0|
|Robot fall|1[fall]|_−_10_._0|


### **B.4 Task-specific success conditions and auxiliary metrics.** 

|Task|Success condition|Auxiliary metrics|
|---|---|---|
|WALKGRAB|Root forward displacement_>_2_._0m, bottle<br>lift_>_0_._02m, and grasp is true.|Root_x_progress, fingertip–bottle<br>distance, contact/grasp rate, bot-<br>tle lift, carry-forward distance,<br>bottle drop, pass-without-grasp,<br>robot fall.|
|OPENFRIDGE|Door angle_≥_60<sup>_◦_</sup>, held-open counter_≥_30<br>control steps. The held-open counter incre-<br>ments only while door angle_≥_35<sup>_◦_</sup>and at<br>least one fingertip contact sensor is above<br>1 N.|Final/max<br>door<br>angle,<br>held-<br>open seconds, hand–handle dis-<br>tance, fingertip contact, back-<br>ward distance, hand-far termina-<br>tion, robot/joint/fridge blow-up.|
|WALKPICKTUR|NGrasp the cube with minimum fingertip–<br>cube distance _<_ 0_._08 m and at least one<br>fingertip contact_>_1N, lifting the cube by<br>_>_ 0_._10 m, and completing the turn with<br>heading error_<_0_._4rad.|Max<br>stage<br>reached,<br>stage-<br>transition rates, fingertip–cube<br>distance, fingertip contact, cube<br>lift, heading error, cube drop.|


### **B.5 Demonstration-Free Reference State Initialization** 

Long-horizon loco-manipulation suffers from a sparse exploration bottleneck. A policy that starts every episode from a default standing pose almost never discovers the later phases of the task by chance, because reaching them requires first solving every earlier phase. A common remedy is reference state initialization (RSI) in VIRAL [21], which resets a fraction of the environments to states drawn from a demonstration so that later phases receive gradient signal from the outset. WALKPICKTURN has no such demonstrations available. We therefore use a _demonstration-free_ variant (NoDe- 

13 

Table 8: WALKPICKTURN reward components, expressions, weights, and the stage(s) (0–2) where each term is applied. Stages: (0) approach & hand-prep, (1) grasp & lift, (2) turn. 

|**Term**|**Expression**|**Weight**|**Stage(s)**|
|---|---|---|---|
|_Termination / generic pena_|_lties_|||
|Success bonus|1[success]|1000_._0|—|
|Robot fall|1[fall]<br>|_−_10_._0|—|
|Action rate|_∥at −at−_1_∥_<sup>2</sup>|_−_0_._01|0–2|
|Joint action rate|�(_ut −ut−_1)2|_−_0_._01|0–2|
|Left-arm DoF velocity|�˙_q_2<br>l-arm|_−_0_._01|0–2|
|DoF velocity|�<br>_j_ <sup>˙</sup><sup>_q_2</sup><br>_j_|_−_0_._01|0–2|
|Large linear_vx_|clip(_|vx| −_0_._5_,_0_,_5)|_−_10_._0|0–2|
|Large linear_vy_|clip(_|vy| −_0_._5_,_0_,_5)|_−_10_._0|0–2|
|<br>Large angular_ω_|<br>clip(_|ωz| −_0_._5_,_0_,_5)|_−_5_._0|0–2|
|<br>Feet slip|<br>�<br>feet <sup>1[contact]</sup><sup>_∥vxy∥_</sup>|_−_5_._0|0–2|
|<br>Undesired table contact|<br>�1[contact_>_5N]|_−_10_._0|0–2|
|Upright orientation|exp(_−∥gxy∥_<sup>2</sup>_/_0_._2<sup>2</sup>)|5_._0|0–2|
|_Heading / command shapin_|_g_|||
|Stage-progress bonus|1[_st > st−_1]|500_._0|0–2|
|<br>Turn alignment|_−|_∆_ψ_region_|_|15_._0|2|
|<br>Heading to object|(∆_ψ_obj_/π_)<sup>2</sup>|_−_10_._0|0|
|_Task / object-centric rewar_|_ds_|||
|Robot–object distance|exp(_−_4(_d −_0_._5)<sup>2</sup>)|15_._0|0–2|
|<br>Right-hand target pose|exp(_−_25_∥_¯_p_hand_−p_<sup>_∗_</sup>_∥_<sup>2</sup>)|30_._0|0|
|<br>Hand prep-region penalty|1_−_exp(_−_(60_e_<sup>2</sup><br>_xy_ <sup>+ 20</sup><sup>_e_2</sup><br>_z_<sup>))</sup>|_−_10_._0|0|
|Hand flat (stage 0)|<br><br>1_−_exp(_−_(_α/_0_._8)<sup>2</sup>)|_−_5_._0|0|
|Keep hand open|exp(_−_6<br>_∥q −q_open_∥_) + 5prog|20_._0|0|
|Hand–object distance|exp(_−_10<br>_d_)over_{_5 tips+palm_}_|20_._0|1–2|
|<br>Fingertip contact|<br>contact ratio+count bonus, lift-gated|10_._0|1–2|
|Grasp force|tanh<br>��_∥F∥_clip_/_2<br>�<br>, lift-gated|10_._0|1–2|
|<br>Object lift height|<br>min(_ℓ,_0_._12)_/_0_._12|50_._0|1–2|
|<br>Hold object|1[grasped]_,_1[_ℓ> ℓ_0]|20_._0|1–2|
|Object not lifted (pen.)|1_−_clip(_ℓ/_0_._1_,_0_,_1)|_−_10_._0|1–2|


moRSI) that bootstraps its own reset distribution from states the policy visits during training, rather than from an external dataset. 

- **Stage Decomposition for WALKPICKTURN** We decompose a WALKPICKTURN episode into three stages, indexed 0 to 2, and treat _completing stage 2 as task success_ . The policy controls the G1 humanoid at 60 Hz over episodes of 10 s (600 control steps), and a per-environment stage index advances monotonically as the corresponding sub-goal is met. **Stage 0 (approach and reach).** The robot walks toward the object and brings its open right hand above it. The stage completes when the mean height of the palm and fingertips is within 0 _._ 3 m above the object, the mean hand-to-object horizontal distance is below 0 _._ 1 m, the right hand is open, both feet are in a stable stance (foot stagger below 0 _._ 4 m), and no table collision is detected. 

- **Stage 1 (grasp and lift).** The robot closes the hand on the object and lifts it. The stage completes when the object is grasped, defined as a minimum fingertip-to-object distance below 0 _._ 08 m together with a positive fingertip contact, and the object is raised more than 0 _._ 1 m above its initial height. 

- **Stage 2 (turn).** While holding the object, the robot rotates its base to face the target heading. The stage completes when the heading error to the target falls below 0 _._ 4 rad. 

14 

Table 9: Shared training hyperparameters (identical across all three tasks). 

|**Hyperparameter**|**Value**|
|---|---|
|Parallel environments|4096|
|Steps per environment per rollout|24|
|Batch size (env_×_steps)|98304|
|Mini-batches|4|
|Learning epochs per update|5|
|Discount_γ_|0.99|
|GAE_λ_|0.95|
|Clip parameter|0.2|
|Entropy coefficient|0.005|
|Value loss coefficient|1.0<br>|
|Learning rate (adaptive, KL target)|1_×_10<sup>_−_3</sup>|
|Desired KL|0.01|
|Max gradient norm|1.0|
|Empirical observation normalization|enabled|
|Actor / critic hidden dims|[1024, 512, 256]|
|Activation|ELU|
|Coord. trunk hidden dims|[512, 256]|
|Body / hand head hidden dims|[256, 128]|
|Body / hand residual scale|1.0|
|Body / hand prior latent dim|16 / 12|


Table 10: Task-dependent settings. 

|**Setting**|**WALKGRAB**|**OPENFRIDGE**|**WALKPICKTURN**|
|---|---|---|---|
|Episode length (s)|15.0|7.0|10.0|
|Control steps|900|420|600|
|Number of stages|1|1|3|
|<br>Action dim (latent)|28|28|28|
|Observation dim|618|629|620|
|Init. action noise_σ_|0.22|0.22|0.22|


The transition criteria are one-way. An environment that satisfies the gate for stage _k → k_ +1 has its stage index incremented and never decreases it within an episode. This monotone structure is what lets NoDemoRSI treat the entry state of each stage as a reusable initialization point. 

**Self-Populating Snapshot Buffer** NoDemoRSI maintains one fixed-capacity ring buffer per noninitial stage. Each entry is a _snapshot_ of the full simulator state needed to resume an episode from a stage boundary. It includes the robot root state (position, orientation quaternion, and linear and angular velocities), the positions and velocities of all actuated joints, the object root state, the stage index, and the object’s initial height. Each buffer holds up to 512 snapshots. Once full, new snapshots overwrite the oldest in first-in-first-out order, so the buffer tracks the policy’s current behaviour rather than its early, low-quality behaviour. 

Snapshots are collected on the fly. When an environment first transitions into a stage _k ≥_ 1, a deferred capture is queued for that environment. On the following control step, provided the environment is still in stage _k_ , the current state is captured and inserted into buffer _k_ , but only if it passes a set of quality filters that reject states unsuitable as reset points. A snapshot is stored only when the robot has not fallen (root height at least 0 _._ 5 m), the environment has spent a minimum dwell time in the stage (12 steps for stage 1, 6 steps for stages 2), and the motion is settled rather than mid-transient: root linear velocity below 0 _._ 4 m/s, root angular velocity below 0 _._ 75 rad/s, joint velocity norm below 10 rad/s, and object linear and angular velocities below 1 _._ 0 in their respective units. 

15 

Table 11: NoDemoRSI configuration for the WALKPICKTURN run. Per-stage entries are listed for stages 0–2; stage 0 has no buffer and is always reset to the default pose. 

|**Setting**|**Value**|
|---|---|
|Buffer capacity per stage|512|
|Min. snapshots to unlock a stage|128 (stages 1–2)|
|Min. dwell steps before storing|(–, 12, 6)|
|Snapshot root-height gate|_≥_0_._5m|
|Max. root linear / angular velocity|0_._4m/s /0_._75rad/s|
|Max. joint velocity norm|10rad/s|
|Max. object linear / angular velocity|1_._0/1_._0|
|Adaptive stage sampling|enabled|
|Success-rate EMA decay|0.98|
|Success-rate prior (weight @ 0.5)|4.0|
|Difficulty floor / power|0.1 / 1.0|
|Consolidation enter / exit|0.80 / 0.75|
|Consolidation stage-0 share|0.85|
|Non-adaptive stage-0 share|0.30|
|Non-adaptive stage weights|(–, 2, 1)|
|Warmup unlock mode|previous-stage success|
|Previous-stage success threshold|0.70|
|Ramp initial share / attempts|0.05 / 1000|


**Reset Sampling and Progressive Stage Unlocking** At every reset, NoDemoRSI assigns each resetting environment a target stage. An environment assigned to stage 0 is reset to the default standing pose, while an environment assigned to a later stage is reset by sampling a snapshot from that stage’s buffer and writing it back into the simulator, so training resumes from a state the policy itself previously reached. If a later stage is selected but its buffer is empty, the reset falls back to stage 0. 

The per-stage sampling probabilities are computed adaptively. Each stage receives a weight proportional to its difficulty times its availability. Difficulty is max(1 _−_ SR _k, ϵ_ )<sup>_p_</sup> with floor _ϵ_ = 0 _._ 1 and power _p_ = 1, where SR _k_ is a smoothed success rate for resets at stage _k_ . A reset counts as a success if the resulting episode advances to the next stage (or, for the final stage, reaches the task success heading condition). The success rate is tracked as an exponential moving average with decay 0 _._ 98 and a Beta-style prior of weight 4 centred at 0 _._ 5, which keeps the estimate stable when a stage has few recent attempts. Availability is a log-compressed function of the buffer occupancy, so a stage with more stored snapshots is sampled more readily without dominating the difficulty term. When all tracked stages reach a success rate of 0 _._ 80, the sampler enters a consolidation mode that spends 85% of resets on stage 0 to rehearse the full chain end to end, and exits when any stage falls back below 0 _._ 75. In the non-adaptive fallback, stage 0 instead receives a fixed share of 0 _._ 3 and the remaining mass is split across later stages by the weights (2 _,_ 1) for stages 1 through 2. 

Two mechanisms govern when the sampler may reset into a later stage, which is essential to avoid initializing a stage before the policy can make use of it. First, a stage must have accumulated at least 128 snapshots in its buffer before it is eligible. Second, a progressive warmup unlocks stages in order of their success. A stage becomes available only after the preceding stage is itself available, the preceding stage’s success rate exceeds 0 _._ 70, and the stage’s buffer satisfies the minimum-sample requirement. Immediately after a stage unlocks, its sampling probability is capped and ramped from an initial share of 0 _._ 05 up to its full adaptive value over the first 1000 cumulative attempts at that stage. The cap prevents a newly unlocked stage from abruptly absorbing the reset budget and starving the stages the policy has not yet consolidated. Together these rules induce a curriculum that begins almost entirely from the default pose, admits stage 1 resets once the policy reliably reaches and grasps the object, and only later admits turn-stage resets, all without any external demonstration. 

16 


Figure 5: WALKPICKTURN real-world demo. 


Figure 6: WALKGRAB real-world demo. 

## **C Real-World Demos** 

This section provides additional qualitative hardware visualizations and clarifies the hardware variant used for real-robot replay. The quantitative simulation experiments in the main paper are conducted on a Unitree G1 humanoid equipped with a 20-DoF WUJI dexterous hand. In contrast, the physical robot available for our hardware visualization uses a Unitree G1 humanoid equipped with a Dex3-1 [48] dexterous hand. The hardware results in this section should therefore be interpreted as a qualitative trajectory replay on a G1+Dex3-1 platform, rather than as the same G1+WUJI configuration used for the reported simulation success rates. 

CoorDex supports such hand variants through its factorized body-hand prior design. The body prior is responsible for whole-body locomotion, reaching, and wrist placement, while the hand prior is 

17 


Figure 7: OPENFRIDGE real-world demo. Due to facility constraints, we use a simplified mockup instead of a full refrigerator door, focusing on the core behavior of maintaining a grasp while stepping backward to pull the object open. 

specific to the dexterous hand morphology. When replacing the hand, the same pipeline can be instantiated by training a hand specific tracking teacher and distilling it into a hand-specific latent prior and decoder. In our implementation, we train an additional Dex3-1 hand tracking teacher and distill it into a Dex3-1 hand prior using the same procedure as the WUJI hand prior. The downstream residual interface remains structurally unchanged. 

For the hardware visualization, we replay recorded joint position trajectories on the physical G1+Dex3-1 robot using the low level joint-position control interface. These trajectories are used to visualize whether the generated body-hand motions are kinematically compatible with the real hardware configuration. We include qualitative snapshots for each task, including WALKGRAB, OPENFRIDGE, and WALKPICKTURN. 

## **References** 

- [1] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne. Deepmimic: example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions on Graphics_ , 37 (4):1–14, 2018. ISSN 1557-7368. doi:10.1145/3197517.3201311. URL `http://dx.doi. org/10.1145/3197517.3201311` . 

- [2] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion, 2025. URL `https: //arxiv.org/abs/2508.08241` . 

- [3] Z. Luo, Y. Yuan, T. Wang, C. Li, F. Casta˜neda, S. Chen, Z.-A. Cao, J. Li, D. Minor, Q. Ben, J. Park, D. Sami, Z. Wang, X. Da, R. Ding, C. Hogg, L. Song, E. Lim, E. Jeong, T. He, H. Xue, W. Xiao, S. Yuen, J. Kautz, Y. Chang, U. Iqbal, L. J. Fan, and Y. Zhu. Sonic: Supersizing motion tracking for natural humanoid whole-body control, 2026. URL `https://arxiv.org/ abs/2511.07820` . 

- [4] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi. Learning human-to-humanoid real-time whole-body teleoperation, 2024. URL `https://arxiv.org/abs/2403.04436` . 

- [5] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang. Expressive whole-body control for humanoid robots, 2024. URL `https://arxiv.org/abs/2402.16796` . 

- [6] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang. Exbody2: Advanced expressive humanoid whole-body control, 2025. URL `https://arxiv.org/abs/2412.13196` . 

- [7] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, L. Fan, and Y. Zhu. Hover: Versatile neural whole-body controller for humanoid robots, 2025. URL `https://arxiv.org/abs/2410.21229` . 

18 

- [8] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. Amp: adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics_ , 40(4):1–20, 2021. ISSN 1557-7368. doi:10.1145/3450626.3459670. URL `http://dx.doi.org/10. 1145/3450626.3459670` . 

- [9] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler. Ase: large-scale reusable adversarial skill embeddings for physically simulated characters. _ACM Transactions on Graphics_ , 41(4): 1–17, 2022. ISSN 1557-7368. doi:10.1145/3528223.3530110. URL `http://dx.doi.org/ 10.1145/3528223.3530110` . 

- [10] C. Tessler, Y. Kasten, Y. Guo, S. Mannor, G. Chechik, and X. B. Peng. Calm: Conditional adversarial latent models for directable virtual characters. _ACM Transactions on Graphics_ , 2023. 

- [11] Z. Luo, J. Cao, J. Merel, A. Winkler, J. Huang, K. Kitani, and W. Xu. Universal humanoid motion representations for physics-based control. In _International Conference on Learning Representations_ , 2024. 

- [12] J. Tan, W. Xu, X. Jiang, J. Zhang, K. Yang, K. Wu, J. Xiong, S. Chen, Y. Li, Y. Feng, Y. Fang, Y. Zou, Y. Song, and R. Xu. Spherical latent motion prior for physics-based simulated humanoid control, 2026. URL `https://arxiv.org/abs/2603.01294` . 

- [13] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning, 2024. URL `https://arxiv.org/abs/2406.08858` . 

- [14] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans, 2024. URL `https://arxiv.org/abs/2406.10454` . 

- [15] L. Heng, Y. Tang, J. Xu, H. Bao, D. Huang, and Y. Wang. Humdex: Humanoid dexterous manipulation made easy, 2026. 

- [16] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning, 2025. 

- [17] Y. Fu, F. Xie, C. Xu, J. Xiong, H. Yuan, and Z. Lu. Demohlm: From one demonstration to generalizable humanoid loco-manipulation, 2025. URL `https://arxiv.org/abs/2510. 11258` . 

- [18] Y. Kuang, H. Geng, A. Elhafsi, T.-D. Do, P. Abbeel, J. Malik, M. Pavone, and Y. Wang. Skillblender: Towards versatile humanoid whole-body loco-manipulation via skill blending, 2025. URL `https://arxiv.org/abs/2506.09366` . 

- [19] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A. akbar Agha-mohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi. Falcon: Learning force-adaptive humanoid loco-manipulation, 2025. URL `https://arxiv.org/abs/2505.06776` . 

- [20] W. Sun, L. Feng, Y. Liu, B. Cao, Y. Jin, and Z. Xie. Ulc: A unified and fine-grained controller for humanoid loco-manipulation, 2025. 

- [21] T. He, Z. Wang, H. Xue, Q. Ben, Z. Luo, W. Xiao, Y. Yuan, X. Da, F. Castaneda, S. Sastry, C. Liu, G. Shi, L. Fan, and Y. Zhu. Viral: Visual sim-to-real at scale for humanoid locomanipulation. _arXiv preprint arXiv:2511.15200_ , 2025. 

- [22] H. Xue, T. He, Z. Wang, Q. Ben, W. Xiao, Z. Luo, X. Da, F. Casta˜neda, G. Shi, S. Sastry, L. J. Fan, and Y. Zhu. Opening the sim-to-real door for humanoid pixel-to-action policy transfer, 2025. URL `https://arxiv.org/abs/2512.01061` . 

19 

- [23] H. Jiang, J. Chen, Q. Bu, L. Chen, M. Shi, Y. Zhang, D. Li, C. Suo, C. Wang, Z. Peng, and H. Li. Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control, 2025. URL `https://arxiv.org/abs/2512.11047` . 

- [24] R. Wang, J. Zhang, J. Chen, Y. Xu, P. Li, T. Liu, and H. Wang. Dexgraspnet: A large-scale robotic dexterous grasp dataset for general objects based on simulation, 2023. URL `https: //arxiv.org/abs/2210.02697` . 

- [25] P. Li, T. Liu, Y. Li, Y. Geng, Y. Zhu, Y. Yang, and S. Huang. Gendexgrasp: Generalizable dexterous grasping, 2023. URL `https://arxiv.org/abs/2210.00722` . 

- [26] X. Zhan, L. Yang, Y. Zhao, K. Mao, H. Xu, Z. Lin, K. Li, and C. Lu. Oakink2: A dataset of bimanual hands-object manipulation in complex task completion, 2024. URL `https:// arxiv.org/abs/2403.19417` . 

- [27] Z. Wei, Z. Xu, J. Guo, Y. Hou, C. Gao, Z. Cai, J. Luo, and L. Shao. _D_ ( _R, O_ ) grasp: A unified representation of robot and object interaction for cross-embodiment dexterous grasping, 2025. URL `https://arxiv.org/abs/2410.01702` . 

- [28] Z. Wei, Y. Yao, and M. Ding. One hand to rule them all: Canonical representations for unified dexterous manipulation, 2026. URL `https://arxiv.org/abs/2602.16712` . 

- [29] K. Li, P. Li, T. Liu, Y. Li, and S. Huang. Maniptrans: Efficient dexterous bimanual manipulation transfer via residual learning, 2025. URL `https://arxiv.org/abs/2503.21860` . 

- [30] Z. Jiang, Y. Xie, K. Lin, Z. Xu, W. Wan, A. Mandlekar, L. Fan, and Y. Zhu. Dexmimicgen: Automated data generation for bimanual dexterous manipulation via imitation learning, 2025. URL `https://arxiv.org/abs/2410.24185` . 

- [31] J. Br¨udigam, A.-A. Abbas, M. Sorokin, K. Fang, B. Hung, M. Guru, S. Sosnowski, J. Wang, S. Hirche, and S. L. Cleac’h. Jacta: A versatile planner for learning dexterous and whole-body manipulation, 2024. URL `https://arxiv.org/abs/2408.01258` . 

- [32] M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. Serrano-Mu˜noz, X. Yao, R. Zurbr¨ugg, N. Rudin, L. Wawrzyniak, M. Rakhsha, A. Denzler, E. Heiden, A. Borovicka, O. Ahmed, I. Akinola, A. Anwar, M. T. Carlson, J. Y. Feng, A. Garg, R. Gasoto, L. Gulich, Y. Guo, M. Gussert, A. Hansen, M. Kulkarni, C. Li, W. Liu, V. Makoviychuk, G. Malczyk, H. Mazhar, M. Moghani, A. Murali, M. Noseworthy, A. Poddubny, N. Ratliff, W. Rehberg, C. Schwarke, R. Singh, J. L. Smith, B. Tang, R. Thaker, M. Trepte, K. V. Wyk, F. Yu, A. Millane, V. Ramasamy, R. Steiner, S. Subramanian, C. Volk, C. Chen, N. Jawale, A. V. Kuruttukulam, M. A. Lin, A. Mandlekar, K. Patzwaldt, J. Welsh, H. Zhao, F. Anes, J.-F. Lafleche, N. Mo¨enne-Loccoz, S. Park, R. Stepinski, D. V. Gelder, C. Amevor, J. Carius, J. Chang, A. H. Chen, P. de Heras Ciechomski, G. Daviet, M. Mohajerani, J. von Muralt, V. Reutskyy, M. Sauter, S. Schirm, E. L. Shi, P. Terdiman, K. Vilella, T. Widmer, G. Yeoman, T. Chen, S. Grizan, C. Li, L. Li, C. Smith, R. Wiltz, K. Alexis, Y. Chang, D. Chu, L. J. Fan, F. Farshidian, A. Handa, S. Huang, M. Hutter, Y. Narang, S. Pouya, S. Sheng, Y. Zhu, M. Macklin, A. Moravanszky, P. Reist, Y. Guo, D. Hoeller, and G. State. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. URL `https://arxiv.org/abs/2511.04831` . 

- [33] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills, 2025. URL `https://arxiv.org/abs/2506.12851` . 

- [34] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu. Twist2: Scalable, portable, and holistic humanoid data collection system, 2025. URL `https: //arxiv.org/abs/2511.02832` . 

20 

- [35] Y. Ze, Z. Chen, J. P. Ara´ujo, Z. ang Cao, X. B. Peng, J. Wu, and C. K. Liu. Twist: Teleoperated whole-body imitation system, 2025. URL `https://arxiv.org/abs/2505.02833` . 

- [36] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control, 2025. URL `https://arxiv.org/ abs/2505.03738` . 

- [37] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang. Gmt: General motion tracking for humanoid whole-body control, 2025. URL `https://arxiv.org/abs/2506.14770` . 

- [38] S. Zhao, X. Zhu, Y. Chen, C. Li, Y. Xie, X. Zhang, M. Ding, and M. Tomizuka. Dexh2r: Task-oriented dexterous manipulation from human to robots. _IEEE/ASME Transactions on Mechatronics_ , 2025. 

- [39] G. Zhang, Q. Xu, H. Zhang, J. Ma, L. He, Y. Bao, Z. Ping, Z. Yuan, C. Lu, C. Yuan, et al. Unidex: A robot foundation suite for universal dexterous hand control from egocentric human videos. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1841–1852, 2026. 

- [40] Z. Liang, Y. Mu, Y. Wang, T. Chen, W. Shao, W. Zhan, M. Tomizuka, P. Luo, and M. Ding. Dexhanddiff: Interaction-aware diffusion planning for adaptive dexterous manipulation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1745–1755, 2025. 

- [41] F. Liu, Z. Gu, Y. Cai, Z. Zhou, H. Jung, J. Jang, S. Zhao, S. Ha, Y. Chen, D. Xu, and Y. Zhao. Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid locomanipulation, 2025. URL `https://arxiv.org/abs/2409.20514` . 

- [42] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang. Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [43] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms, 2017. URL `https://arxiv.org/abs/1707.06347` . 

- [44] H. Zhao, R. Cathomen, L. Gulich, W. Liu, E. A. Ongan, M. Lin, S. Jain, S. Pouya, and Y. Chang. Agile: A comprehensive workflow for humanoid loco-manipulation learning, 2026. URL `https://arxiv.org/abs/2603.20147` . 

- [45] Y. Qin, W. Yang, B. Huang, K. Van Wyk, H. Su, X. Wang, Y.-W. Chao, and D. Fox. Anyteleop: A general vision-based dexterous robot arm-hand teleoperation system. In _Robotics: Science and Systems_ , 2023. 

- [46] Unitree Robotics. Unitree g1 humanoid robot. `https://www.unitree.com/g1` , 2026. Accessed: 2026-05-27. 

- [47] WUJI TECH. Wuji hand product introduction. `https://docs.wuji.tech/docs/en/ wuji-hand/latest/overview/` , 2026. Accessed: 2026-05-27. 

- [48] Unitree Robotics. Unitree dex3-1 dexterous hand. `https://www.unitree.com/Dex3-1` , 2026. Accessed: 2026-05-27. 

21 

