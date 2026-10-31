---
title: "Constrained Whole-Body Tracking for Humanoid Robots"
date: "2026-05-29"
authors: "Daniel Morton; Pranit Mohnot; Marco Pavone"
url: https://arxiv.org/abs/2606.00374
pdf: https://arxiv.org/pdf/2606.00374
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.00374)** / [論文ページ](https://arxiv.org/abs/2606.00374)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Constrained Whole-Body Tracking for Humanoid Robots** 

**Daniel Morton**<sup>**1**</sup> **, Pranit Mohnot**<sup>**1**</sup> **, Marco Pavone**<sup>**1,2**</sup> 

1Stanford University, 2NVIDIA Research 

**Abstract:** Recent advances in reinforcement learning (RL) have demonstrated impressive whole-body agility for humanoid robots, yet ensuring safety and satisfying constraints – particularly those specified after training – remains a challenge. Towards this goal, we present ConstrainedMimic, a control framework that leverages whole-body kinematics and dynamics for real-time constraint enforcement within RL tracking policies. By integrating principles from operational space control and control barrier functions, we enable the satisfaction of arbitrary runtime constraints on both the kinematic reference motion and the underlying dynamics, with efficient computation at frequencies above 1 kHz. In whole-body motion-tracking experiments in simulation and hardware, we demonstrate collision avoidance (both with the robot body and external obstacles), joint limits, and center of mass stability constraints. By remaining consistent with the current contact mode and tracking objectives, we minimally restrict the capabilities of the policy when constraints are active. Project page: `https://stanfordasl.github.io/constrainedmimic` . 

**Keywords:** Whole-body control, Safety, Humanoids 

## **1 Introduction** 

Modern humanoid robots are becoming increasingly capable of whole-body motion tracking, locomotion, and manipulation, with reinforcement learning (RL) policies that achieve striking agility on hardware [1, 2, 3]. As these systems are deployed, especially when they must interact with novel scenes, other equipment, or humans, a framework to enforce previously unseen safety constraints becomes critical. An ideal runtime safety framework would be minimally invasive, policy-agnostic, easily configurable for arbitrary deployment-time constraints, and capable of real-time speeds ( _≥_ 50 Hz). 

Recent work has led to significant advances in humanoid whole-body control, demonstrating capable tracking across teleoperation [1, 4, 5, 6], multi-task control [2, 7], and expressive behaviors at scale [3]. Despite this diversity, these works share a common architectural paradigm: reference kinematic trajectories from retargeted motion capture systems, virtual-reality headsets, or high-level planners are passed to an RL motion tracking policy, which takes these (often dynamically infeasible) references and outputs joint commands that produce closely-tracking dynamically-feasible trajectories on the real robot. This separation provides two natural points at which safety can be considered without modifying the tracking policy: the input kinematic reference, and the output dynamics. 

With these desiderata and problem structure in mind, control barrier functions (CBFs) may be a natural choice to embed safety into humanoid whole-body control. Commonly used in optimizationbased control, CBFs enforce safety via forward-invariance of a set defined by a differentiable barrier function _h_ ( **z** ), and are typically applied as a safety filter on top of a nominal, unsafe controller [8]. While CBFs for humanoids have been explored in prior work [9, 10, 11, 12, 13, 14], safety for whole-body control remains underexplored, particularly in the context of learning-based motion tracking policies. 

Correspondence to: dmorton@stanford.edu 


Figure 1: **_Where does safety fit into a learning-based humanoid motion tracking stack?_** We approach safety at the kinematics and dynamics levels, addressing safety from both sides (input and output) of the policy. On the kinematics side, constraints can naturally fit into the IK-based retargeting between human and robot form-factors, or be applied as a safety filter on motions already mapped to the robot geometry. On the dynamics side, a potentially unsafe command from the policy can be passed through a safety filter prior to execution on the robot. 

### **1.1 Related Work** 

**Whole-Body Control of Humanoid Robots.** For years, the dominant approach to whole-body control was purely model-based, including operational space control [15, 16, 17] and broader optimization-based methods [18, 19]. More recently, RL-based whole-body control has become a leading paradigm, with systems demonstrating whole-body teleoperation [1, 4, 5, 6], operation across multiple control modes [7], diffusion-based skill composition [2], and motion tracking at foundation-model scale [3]. In this setting, reference trajectories are produced by retargeting human motion to robot kinematics via inverse kinematics (IK) and optimization [20, 21, 22, 23], in both online and offline contexts. Broadly, these recent RL-based methods take advantage of modeling structure in robot kinematics as an interface for control, while relying on the expressiveness of learning-based policies for robustness and recovery behaviors. 

**Learning-Based Humanoid Safety.** Recent works in safety for learning-based humanoid control have explored several directions. First, methods that prioritize compliance [24, 25, 26] limit risk during incidental contact with humans, the environment, or the robot itself. Also critical to safety is understanding when and how to stop the robot [27], and avoiding damage during falls [28, 29]. However, these contexts differ from state constraint enforcement, which typically seeks to avoid undesired contact or avoid exceeding other physical limits. Towards this end, recent work compiles and compares common safety methods [30], incorporates potential fields during policy training [31], and analyzes constraint infeasibility in cluttered settings [32]. 

**CBFs for Humanoid Safety.** CBFs have been applied to legged systems since early bipedalwalking demonstrations [9, 10]. For humanoids, acceleration-level CBFs have been used as constraints in optimization-based whole-body controllers, for self-collision avoidance in locomotion [11] and task-space constraints in model-based control [12]. However, both works enforce the CBF with a reduced-order double-integrator model, which fails to properly consider the true constrained dynamics of the system. For more recent work combining CBFs and RL, two works are closest to ours. SHIELD [13] learns a stochastic residual on top of a planar single-integrator nominal model and enforces CBFs for safety in expectation. CBF-RL [14] integrates CBFs into the RL training loop for lower-body locomotion, demonstrating planar obstacle avoidance and stair-stepping. Both focus on _locomotion_ , rather than whole-body tracking. 

### **1.2 Contributions** 

We make several contributions towards safe learning-based whole-body tracking. First, we identify where safety can be enforced in the motion-tracking stack (Fig. 1): at the input (kinematic 

2 

reference) and the output (low-level joint commands) of the policy, and propose three methods for constraint enforcement: _constrained retargeting_ , _kinematic filters_ , and _dynamic filters_ . For each of these methods, we construct CBFs on the full _contact-constrained_ kinematics and dynamics, with _task-consistent_ filtering objectives that respect the implicit task structure of motion tracking and loco-manipulation. Together, these form **ConstrainedMimic** : a runtime safety framework for learned whole-body motion-tracking policies which requires no retraining of the underlying policy, and is capable of running well above policy frequency even on edge compute. In both simulation and hardware, we validate performance on collision avoidance, joint limits, and stability constraints, demonstrating successful constraint enforcement even on fast-moving motions. 

## **2 Constrained Whole-Body Tracking** 

Within an RL-based motion tracking stack, constraints can be enforced at three key points, depending on the source of the reference motion: (1) in the quadratic programming (QP)-based human-torobot kinematic retargeting pipeline, whether online or offline (Sec. 2.2), (2) as a kinematic safety layer on top of an already-retargeted motion (Sec. 2.3), and (3) as a dynamic safety layer at the torque level (Sec. 2.4). In this section, we discuss each approach, and their commonalities: particularly, how the _contact-constrained_ kinematics and dynamics influence their construction, and how to design the filter objectives to be _consistent_ with typical tasks such as locomotion and manipulation. 

### **2.1 Safety Constraints** 

_Refer to the Appendix, Sec. A for derivations of the kinematics and dynamics terms used in this paper._ 

During operation, _safety_ can imply a variety of constraints to impose on the system. Most commonly, this includes collision avoidance, workspace limits, joint limits, singularity avoidance, and stability constraints. For each of these, we can define a barrier function _h_ with respect to the state **z** as a differentiable metric of the current safety of the system, and incorporate this into an optimization-based controller or safety filter through CBF constraints. Specifically, for a control-affine system **z** ˙ = _f_ ( **z** )+ _g_ ( **z** ) **u** , the CBF condition requires 


where _Lf h_ ( **z** ) = _<u>dhd</u>_ **z**<sup>(</sup><sup>**z**)</sup><sup>_f_(</sup><sup>**z**)and</sup><sup>_Lgh_(</sup><sup>**z**)=</sup> _<u>dhd</u>_ **z**<sup>(</sup><sup>**z**)</sup><sup>_g_(</sup><sup>**z**)aretheLiederivativesof</sup><sup>_h_alongthe</sup> dynamics, and _α_ is an extended class _K∞_ function. Satisfying this condition renders the safe set _{_ **z** : _h_ ( **z** ) _≥_ 0 _}_ forward-invariant [8]. Further details on CBFs can be found in the Appendix, Sec. B. In this work, we employ the following (vector-valued) barrier functions in our experiments. Note that for kinematic safety methods, the state **z** is simply the generalized coordinates **q** , whereas for dynamic safety methods, the state includes the generalized velocities, i.e., **z** =[ **q** _,_ **q** ˙ ]. 

_Joint limits_ : Defined as the joint-space distances to the positional limits, 


_Collision avoidance_ : Defined as the distance to collision between two bodies ( _i, j_ ) in a set of collision pairs _P_ with radii _ri_ , _rj_ . In this paper, we restrict our focus to sphere-sphere, sphere-plane, and sphere-cylinder collision models for simplicity, where 


_Center of mass (CoM) stability_ : Defined as the distance between the XY projection of the robot’s CoM and the edges of the feet’s support polygon. We represent the support polygon in halfspace form where **Ax** _≤_ **b** for a point **x** _∈_ R<sup>2</sup> , computed by considering the convex hull of the four contact points on each foot, where 


Constructing these CBF constraints requires differentiating through the barrier function _h_ with respect to the state variable **z** (Eq. 1). To do so, we compute all terms related to the robot kinematics and dynamics with `frax` [33], and differentiate through these with `cbfpy` [34]. 

3 

### **2.2 Whole-Body Kinematically-Constrained Retargeting** 

During retargeting, we consider the following control-affine model of the _fully-actuated_ system subject to contact constraints (Eq. 26), where **z** = **q** and **u** = ˙ **q** : 


Here, **N** _c_ is the contact null-space projection matrix, and across the following sections, the subscript _|c_ denotes a contact-constrained quantity (projected via **N** _c_ ). For each frame of interest (with an associated Jacobian **J** _i_ and positive-definite weighting matrix **W** _i_ ), we compute the task-space twist **_ν_** _i_ to reduce the error dynamics between the frame on the robot and the desired frame on the reference human kinematics. For retargeting between human frames and the Unitree G1, we use a weighted combination of _nt_ = 14 pairwise tasks with independent control over the position and orientation weighting for each. 

Given a barrier function _h_ ( **z** ) and an extended class _K∞_ function _α_ , we then construct the CBF constraint (Eq. 1) and enforce this in the following differential inverse kinematics problem: 


We also enforce box inequality constraints on the joint velocities ( ˙ **q** min _≤_ **q** ˙ _≤_ **q** ˙ max), add an _ℓ_ 1 relaxation for persistent feasibility (and _soft_ safety guarantees) (Eq. 44) [35], and add additional pre/post-processing steps for improved retargeting, elaborated in the Appendix, Sec. C.3. When the retargeter cannot be modified (e.g., for offline-retargeted motions), the analogous constraints can instead be enforced as a filter on the retargeted reference, presented next. 

### **2.3 Whole-Body Kinematic Safety Filters** 

For a motion which is already defined on the robot kinematics (e.g., post-offline-retargeting), we can still enforce safety at the kinematic level without explicitly re-solving the retargeting problem with constraints in the QP. In this case, we can construct a kinematic safety filter to compute a minimally-invasive modification to the reference motion to maintain constraint enforcement. 

For whole-body locomotion and manipulation (including teleoperation), we adopt a hierarchical objective structure, where the primary task is motion tracking in operational space for any endeffectors (hands and feet) not currently in contact, and the CoM. As a secondary task, we consider posture tracking in the null space of motion tracking, to fully define the remaining degrees of freedom (DoFs) of the system. Note that these tasks are _consistent_ with the current contact mode, projected into the null space of the contact Jacobian. Given this structure, the filtering objective is: 


Writing Eq. 7 in terms of **q** ˙ , we can then pose the CBF-QP as: 


As in Sec. 2.2, we use the same constrained control-affine kinematic model (Eq. 5) when constructing the CBF constraints, and we pair the QP with joint velocity limits and an _ℓ_ 1 relaxation. 

Both kinematic methods enforce safety only on the policy’s _input_ ; next, we consider _output_ safety. 

### **2.4 Whole-Body Dynamic Safety Filters** 

After computing the nominal (potentially unsafe) joint PD targets from the RL tracking policy, we enforce a final layer of safety before sending the command to the robot. In contrast to Secs. 2.2 and 

4 

2.3, this filtering _can not_ be applied at the kinematic level, as the joint PD targets implicitly produce a set of actuator torques, and thus we must analyze safety at a lower level. In this case, we employ the following control-affine model of the contact-constrained and underactuated system dynamics, obtained by applying the constrained dynamics (Eq. 31) and actuation model (Eq. 23): 


Here, the state **z** contains both the generalized coordinates and velocities [ **q** _,_ **q** ˙ ], the control input **u** is the actuated joint torques **Γ** body, **M** is the mass matrix, **c** and **g** are the Coriolis and gravity terms, **J** _c_ is the contact Jacobian, **_µ_** _c,J_ ˙ is the Coriolis term associated with **J**<sup>˙</sup> _c_ , and **S** is the actuator selection matrix (App. A). 

As with the kinematic filter, we consider whole-body locomotion and manipulation tasks, with a similar hierarchical objective structure. To minimally interfere with the stability of the policy, we consider the primary task to be _contact force tracking_ on any feet in contact with the ground, and then motion and posture tasks are posed as secondary and tertiary tasks. Motion and posture are also defined with respect to the task-space and joint-space _accelerations_ , rather than velocities. Given these task definitions, we can then express the objective terms of the safety filter in a weighted least-squares form for each task as 


Writing Eq. 10 in terms of **Γ** body, we can then pose the QP as 


We also enforce box inequality constraints on the joint torques ( **Γ** body, min _≤_ **Γ** body _≤_ **Γ** body, max), and as before, use an _ℓ_ 1 relaxation for persistent feasibility. 

To compute the nominal actuated torque input **Γ** body,nom, we apply the actuators’ PD control law, with gains **K** _p_ , **K** _d_ and clipping to the torque limits: 


After solving for the safe torque input **Γ**<sup>_∗_</sup> body<sup>from Eq.11, we then map this back to a safe set of PD</sup> targets and send this to the robot:<sup>1</sup> 


## **3 Experiments** 

We evaluate our methods in both simulation and hardware (Unitree G1), with unmodified TWIST2 [1] and SONIC [3] policies as the underlying whole-body controller. In our experiments, we address five questions, each motivating a successive piece of the framework: is safety already implicit in the policy (Sec. 3.1); when is dynamic filtering necessary (Sec. 3.2); how do contact constraints shape the CBF and QP objective (Sec. 3.3); where do single-step constraints fail (Sec. 3.4); and how to handle necessary contact mode changes (Sec. 3.5). Furthermore, we conclude with validating performance both computationally (Sec. 3.6) and on hardware (Sec. 3.7). 

### **3.1** **_To what extent is safety already represented in the policy?_** 

Safety specifications which can be defined purely with respect to the robot model (e.g., selfcollision, joint limits) are known at training time, and are often included in the reward function. 

> 1Direct torque commands at up to 1 kHz (as on TORO [36]) would be preferable. The PD-target mapping is a practical concession to the Unitree G1’s control interface and the current state of motion tracking policies. 

5 


Figure 2: Self-collision constraint violation from the TWIST2 policy tracking both unfiltered and filtered kinematic references. 

However, we find that motion tracking policies such as TWIST2 do not provide any inherent guarantees of satisfying these safety constraints. In a simulated whole-body online teleoperation experiment (Fig. 2), passing an unsafe “arm-crossing” reference to the policy immediately results in self-collision between the arm geometry [blue]. Additionally, while applying a self-collision CBF during the retargeting IK process can enforce safety [green], simply tracking this safe reference with the policy can still lead to constraint violation [orange]. Given this, we observe that even constraints known _a priori_ benefit from explicit safety filtering at deployment time. 

### **3.2** **_Is dynamic safety necessary if kinematic safety is enforced?_** 


Figure 3: Handling deployment-time safety at both the kinematic and dynamics levels. 

Motivated by the failure modes of purely kinematic methods in Sec. 3.1, we look at the performance of dynamic safety methods in the context of a “karate chop” collision avoidance scenario; an external safety constraint which can _not_ be defined at training time. Here, we enforce a constraint (Eq. 3) between the hand and the planar surface of a table, and we find that while constrained kinematic retargeting can lead to a safe reference motion (Fig. 3B), this is no longer safe when the policy is deployed due to overshoot (Fig. 3C). When adding the dynamic safety filter (Fig. 3D–E), we see that safety is maintained regardless of the kinematic reference being safe or unsafe, but combining both kinematics- and dynamics-based filters can lead to marginally higher conservatism (Fig. 3E). 

### **3.3** **_How do contact constraints impact the design of the safety filter?_** 


Figure 4: Ablation on the components of contact-constrained kinematic safety filters. 

Consider an _antigravity lean_ dance move [Jackson, 1988]; impossible to execute for a human or robot without specialized shoe fixtures or harnesses. The primary safety condition violated is center of mass (CoM) stability: the projection of the CoM into the XY plane departs from the interior of the feet’s support polygon, indicating that the pose is not statically stable.<sup>2</sup> 

> 2In short, the robot (referred to as Annie) would _not_ be OK if this were performed without a safety filter. 

6 

Enforcing a standard min-norm safety filter (Eq. 41) with both a CoM stability CBF (Eq. 4) and joint limits CBF (Eq. 2) on the full unconstrained kinematics of the system leads to the behavior shown in Fig. 4B. The CoM remains within the original (static) support polygon, and joint limits are respected, but integrating without considering the constrained kinematics (Eq. 26) leads to infeasible motion where the feet leave the ground. Accounting for this, in Fig. 4C, we now observe a violation of the CBF constraints, due to a mismatch between the kinematic model used in the CBF (unconstrained) and the true kinematic model (constrained). Lastly, in Fig. 4D, we see that without a task-consistent filtering objective (Fig. 4E), the filter can induce undesired motion at the boundary of safety. 

### **3.4** **_Where are the failure modes of short-horizon constraint enforcement?_** 


Figure 5: Impact of short-horizon safety constraints on dynamic feasibility across discrete modes. Consider a robot walking under a cylindrical obstacle at head-height (Fig. 5), with collision avoidance enforced via CBF constraints on a spherized model of the robot geometry (Eq. 3). Walking safely under the obstacle can take one of two modes: “limbo”; bending backward to avoid a collision, or “crouch”; bending forward. These discrete modes of approaching an obstacle have distinct consequences on the dynamic feasibility of the trajectory, with “crouch” leading to a feasible trajectory whereas “limbo” is unstable. By nature, CBFs are a _single-step_ method of enforcing safety, and some constraints (such as this) inherently require longer-horizon reasoning over discrete actions or modes. In teleoperation, we can assume that a human provides this higher-level reasoning ( _“how should the robot approach this obstacle?”_ ), whereas for full autonomy, this reasoning would require an additional layer in the stack; a target for future work. 

### **3.5** **_When is it necessary to break the current contact mode to maintain safety?_** 

Consider a humanoid standing at rest with a dynamic obstacle moving towards the robot (Fig. 6). In the contact-constrained kinematic setting, no motion of any feet currently in contact is permitted, leading to an infeasible problem where collision is inevitable. This safety condition inherently requires the ability to break the current contact mode and begin walking to maintain safety. 

In the context of whole-body motion tracking, we cannot simply command a planar twist for a locomotion policy to track. Instead, we must explicitly define a lower-body kinematic motion to track a safe velocity, typically through a footstep planner and IK solver (similar to Eq. 6), or through a learned planner [3]. 


Figure 6: Tracking lower-body kinematic plans with SONIC for dynamic collision avoidance. 

As with the “limbo” example, this requires higher-level discrete decision making ( _“when should the robot take a step?”_ ). We propose a simple heuristic to approach this: in parallel with the wholebody CBFs, enforce an obstacle-avoidance CBF on a reduced-order model of the planar locomotion dynamics<sup>3</sup> . When this constraint is active, pass the safe velocity to a lower-body kinematic planner, and enforce whole-body safety on the updated reference. This approach is practical, easy to implement, and safe in most cases, but does not give a firm guarantee of safety. Future work will explore 

> 3SHIELD’s residual-augmented single-integrator model would apply here [13]. 

7 

tighter integration of discrete high-level decision making with more continuous notions of safety, and better locomotion dynamics models. 

### **3.6 Performance Analysis** 


Figure 7: Compute frequencies for constrained whole-body tracking. 

When implementing safety filters and inverse kinematics/dynamics methods for online control, speed is critical. Higher frequencies result in tighter feedback loops with less jitter or delay, and enable control over faster dynamics. And, for a fixed time budget, more efficient methods allow for higher scalability in the number of constraints, or the ability to run onboard on edge devices. As seen in Fig. 7, all three methods in this paper run well above the policy frequency of 50 Hz on both desktop PCs and edge devices. On desktop, even with over 300 constraints, all methods achieve _≥_ 1 kHz control rates. For filtering, this unlocks the ability to enforce safety at higher rates than the policy, to constrain faster dynamics when new low-level state information is available (in general, the dynamic filter should be run as fast as possible given the compute budget). 

In Tab. 1, we also quantify the performance of the kinematic and dynamic safety methods on the self-collision and karate chop experiments. To evaluate these, we vary both parameters of the CBF constraint (e.g., table height for karate chop) and the playback speed of the reference motion (uniformly distributed between 0 _._ 5 _×_ and 2 _._ 0 _×_ the nominal rate) across 100 trials for each method and experiment. Consistently, we see that (1) the base policy is unable to maintain safety, even for conditions known at training time, (2) adding a kinematic filter significantly reduces constraint violation but does not perfectly ensure safety due to overshoot, (3) dynamic safety filters reduce constraint violation significantly due to operating at the final, lowest level of the stack, but can still have some minor violation (for reasons elaborated in the Appendix, Sec. B.1), and (4) enabling constraints on both input and output levels most reliably leads to safe operation. 

Table 1: Constraint enforcement performance on TWIST2 [orange] and SONIC [green] policies. 

||Self-Co|llision|Karate|Chop|
|---|---|---|---|---|
||Frames in violation [%]|Max violation [mm]|Frames in violation [%]|Max violation [mm]|
|Base Policy|37.6 ± 0.3/37.7 ± 0.2|97.4 ± 3.0/100.4 ± 2.7|20.6 ± 4.1/18.9 ± 7.2|424 ± 152/253 ± 143|
|Kinematic Safety|8.5 ± 1.3/7.5 ± 1.0|12.1 ± 0.6/52.9 ± 4.9|12.6 ± 8.6/7.6 ± 8.7|100.3 ± 91.3/64.6 ± 75.7|
|Dynamic Safety|0.35 ± 0.86/1.24 ± 1.26|0.50 ± 1.32/0.43 ± 0.41|0.28 ± 1.16/3.10 ± 3.57|0.09 ± 0.48/5.98 ± 8.39|
|Kin. + Dyn. Safety|0.02 ± 0.10/0.00 ± 0.00|0.03 ± 0.12/0.00 ± 0.00|0.05 ± 0.35/0.29 ± 1.10|0.02 ± 0.14/0.25 ± 1.04|


### **3.7 Hardware Validation** 

Building upon our simulation results, we recreate the karate-chop example from Section 3.2 and deploy this motion on the Unitree G1 hardware. Here, we use TWIST2 as the underlying general motion tracking policy, wrapped in a low-latency ROS2 interface to handle the low-level control, safety layers, and the original recording of the motion data from the Pico XR headset [37]. 

On hardware, we note three main differences from simulation that influence the performance of the safety filter: delays (from communication, actuators, and computation), noise (from realistic actuator measurements and state estimation), and model mismatch (unmodeled friction, imperfect inertial values). While our emphasis on speed from Section 3.6 helps to minimize the adverse effects of delays (and noise, to some extent, with some minimal smoothing), these hardware experiments primarily seek to understand how performance varies under minor dynamics model mismatch. 

8 


Figure 8: Hardware validation of the kinematic and dynamic safety filters on the “karate-chop” motion of Section 3.2. After a fast-moving initial start of the motion (1), we observe the outcomes with no filter (2a), kinematic safety only (2b), dynamic safety only (2c), and both kinematic and dynamic safety layers (2d). The plot visualizes the constraint satisfaction throughout the trajectory: _h_ ( **z** ) _≥_ 0 when safe. 

Broadly, our hardware results validate our simulation results, with one minor difference to note. Whereas in simulation (with no dynamics mismatch) the dynamic filter was the _least conservative_ approach that could maintain safety (Fig. 3D), on hardware, this led to small constraint violation, particularly when moving fast (Fig. 8, 2c and plot). Thus, this provides an even more convincing argument for why safety must be considered at _both_ the kinematics and dynamics levels: kinematics alone can fail due to lack of consideration of inertial effects and tracking error; dynamics alone can fail due to imperfect modeling; together these complement each other for strong constraint satisfaction. 

## **4 Conclusion** 

In this work, we have presented ConstrainedMimic: a framework for constraint enforcement in a learning-based whole-body control stack. With whole-body motion tracking policies emerging as “foundation models” for humanoid control, ConstrainedMimic allows for enforcing arbitrary safety constraints (unknown at training time) on top of a pre-trained policy, in a minimally-invasive manner, and without any need for re-training. This combination of RL + CBFs can handle both dynamic feasibility and large numbers of nonconvex state constraints in real time, bringing model-based assurances to learning-based control in a computationally-tractable manner. 

### **4.1 Limitations and Future Work** 

**Higher-level safety.** We focus primarily on single-step constraint enforcement, and as discussed, safety often requires higher-level logic (long-horizon or semantic reasoning) for discrete decisions. 

**Safety under disturbances.** We design our safety methods to _minimally interfere_ with recovery behaviors in the RL policy, but do not currently account for fall-inducing disturbances. 

**Uncertainty in dynamics and estimation.** Dynamic filters work well when the contact modes are well-known, but this assumes that reliable sensing or estimation is available, which is not always the case. Future work will explore integration with onboard estimation for improved generality. 

**Distribution shift.** Kinematic filters (generally) result in in-distribution motions, but dynamic filters can potentially lead to out-of-distribution situations, despite a minimally-invasive design. Future work will quantify this effect and explore how fine-tuning can reduce tradeoffs in performance for safety, and will take advantage of the differentiability and GPU-compatibility of these methods. 

**Onboard perception.** We analyze whole-body safety with strong assumptions about the state and geometry of collision bodies in the environment. While this is useful for initial experiments, we aim to make use of onboard perception data in the future. 

9 

### **Acknowledgments** 

Daniel Morton was supported by a NASA Space Technology Graduate Research Opportunity. Pranit Mohnot was supported by an NSF Graduate Research Fellowship. This work was supported in part by Generative Bionics. Thanks to Yanjie Ze and William Chong for helpful discussions throughout the project. 

## **References** 

- [1] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. Karen Liu. TWIST2: Scalable, portable, and holistic humanoid data collection system. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 15900–15907, 2026. doi: 10.1109/ICRA57385.2026.11696896. 

- [2] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. BeyondMimic: From motion tracking to versatile humanoid control via guided diffusion. _Science Robotics_ , 11(117):eadx8924, 2026. doi:10.1126/scirobotics.adx8924. URL `https://www.science. org/doi/abs/10.1126/scirobotics.adx8924` . 

- [3] Z. Luo, Y. Yuan, T. Wang, C. Li, F. Casta˜neda, S. Chen, Z.-A. Cao, J. Li, D. Minor, Q. Ben, J. Park, D. Sami, Z. Wang, X. Da, R. Ding, C. Hogg, L. Song, E. Lim, E. Jeong, T. He, H. Xue, W. Xiao, S. Yuen, J. Kautz, Y. Chang, U. Iqbal, L. Fan, and Y. Zhu. SONIC: Supersizing motion tracking for natural humanoid whole-body control. _Science Robotics_ , 11(117):eaed4592, 2026. doi:10.1126/scirobotics.aed4592. URL `https://www.science.org/doi/abs/10. 1126/scirobotics.aed4592` . 

- [4] Y. Ze, Z. Chen, J. P. Araujo, Z.-a. Cao, X. B. Peng, J. Wu, and K. Liu. TWIST: Teleoperated whole-body imitation system. In J. Lim, S. Song, and H.-W. Park, editors, _Proceedings of The 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 2143–2154. PMLR, 27–30 Sep 2025. URL `https://proceedings.mlr. press/v305/ze25a.html` . 

- [5] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. OmniH2O: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In _Conference on Robot Learning_ , 2024. URL `https://api.semanticscholar.org/CorpusID: 270440515` . 

- [6] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang. HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit. In _Proceedings of Robotics: Science and Systems_ , Los Angeles, CA, USA, June 2025. doi:10.15607/RSS.2025.XXI.070. 

- [7] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, L. J. Fan, and Y. Zhu. HOVER: Versatile neural whole-body controller for humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9989–9996, 2025. doi:10.1109/ICRA55743.2025.11128549. 

- [8] A. D. Ames, S. Coogan, M. Egerstedt, G. Notomista, K. Sreenath, and P. Tabuada. Control barrier functions: Theory and applications. In _2019 18th European Control Conference (ECC)_ , 2019. doi:10.23919/ECC.2019.8796030. 

- [9] S.-C. Hsu, X. Xu, and A. D. Ames. Control barrier function based quadratic programs with application to bipedal robotic walking. In _2015 American Control Conference (ACC)_ , pages 4542–4548, 2015. doi:10.1109/ACC.2015.7172044. 

- [10] Q. Nguyen, A. Hereid, J. W. Grizzle, A. D. Ames, and K. Sreenath. 3D dynamic walking on stepping stones with control barrier functions. In _2016 IEEE 55th Conference on Decision and Control (CDC)_ , pages 827–834, 2016. doi:10.1109/CDC.2016.7798370. 

10 

- [11] C. Khazoom, D. Gonzalez-Diaz, Y. Ding, and S. Kim. Humanoid self-collision avoidance using whole-body control with control barrier functions. In _2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids)_ , pages 558–565, 2022. doi: 10.1109/Humanoids53995.2022.10000235. 

- [12] V. C. Paredes and A. Hereid. Safe whole-body task space control for humanoid robots. In _2024 American Control Conference (ACC)_ , pages 949–956, 2024. doi:10.23919/ACC60939.2024. 10644227. 

- [13] L. Yang, B. Werner, R. K. Cosner, D. Fridovich-Keil, P. Culbertson, and A. D. Ames. SHIELD: Safety on humanoids via CBFs in expectation on learned dynamics. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 203–210, 2025. doi: 10.1109/IROS60139.2025.11247065. 

- [14] L. Yang, B. Werner, M. de Sa, and A. D. Ames. CBF-RL: Safety filtering reinforcement learning in training with control barrier functions. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 17825–17832, 2026. doi:10.1109/ICRA57385.2026. 11695808. 

- [15] J. Park and O. Khatib. Contact consistent control framework for humanoid robots. In _2006 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 1963–1969, 2006. doi:10.1109/ROBOT.2006.1641993. 

- [16] O. Khatib, M. Jorda, J. Park, L. Sentis, and S.-Y. Chung. Constraint-consistent taskoriented whole-body robot formulation: Task, posture, constraints, multiple contacts, and balance. _The International Journal of Robotics Research_ , 41(13-14):1079–1098, 2022. doi: 10.1177/02783649221120029. URL `https://doi.org/10.1177/02783649221120029` . 

- [17] L. Sentis. _Synthesis and Control of Whole-Body Behaviors in Humanoid Systems_ . PhD thesis, Stanford University, Stanford, CA, July 2007. 

- [18] S. Kuindersma, R. Deits, M. Fallon, A. Valenzuela, H. Dai, F. Permenter, T. Koolen, P. Marion, and R. Tedrake. Optimization-based locomotion planning, estimation, and control design for the Atlas humanoid robot. _Autonomous robots_ , 40(3):429–455, 2016. 

- [19] P. M. Wensing, M. Posa, Y. Hu, A. Escande, N. Mansard, and A. D. Prete. Optimizationbased control for dynamic legged robots. _IEEE Transactions on Robotics_ , 40:43–63, 2024. doi:10.1109/TRO.2023.3324580. 

- [20] J. P. Ara´ujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6097–6104, 2026. doi:10.1109/ICRA57385.2026.11697263. 

- [21] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11691–11698, 2026. doi:10.1109/ICRA57385.2026.11696487. 

- [22] C. M. Kim, B. Yi, H. Choi, Y. Ma, K. Goldberg, and A. Kanazawa. PyRoki: A modular toolkit for robot kinematic optimization. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025. URL `https://arxiv.org/abs/2505.03728` . 

- [23] K. Zakka. Mink: Python inverse kinematics based on MuJoCo, Feb. 2026. URL `https: //github.com/kevinzakka/mink` . 

- [24] Q. Lu, Y. Feng, B. Shi, M. Piseno, Z. Bao, and C. K. Liu. GentleHumanoid: Learning upper-body compliance for contact-rich human and object interaction. _arXiv preprint arXiv:2511.04679_ , 2025. 

11 

- [25] S. Chen, Z.-A. Cao, Z. Luo, F. Casta˜neda, C. Li, T. Wang, Y. Yuan, L. Fan, C. K. Liu, and Y. Zhu. CHIP: Learning adaptive compliance for humanoid control through hindsight perturbation. _arXiv preprint arXiv:2512.14689_ , 2025. 

- [26] G. B. Margolis, M. Wang, N. Fey, and P. Agrawal. SoftMimic: Learning compliant whole-body control from examples. _arXiv preprint arXiv:2510.17792_ , 2025. 

- [27] Y. Sun, Y. Pan, S. Li, C. Ding, T. Cui, L. Wang, and C. Liu. Learning safe-stoppability monitors for humanoid robots. _arXiv preprint arXiv:2603.22703_ , 2026. 

- [28] Z. Meng, T. Liu, L. Ma, Y. Wu, R. Song, W. Zhang, and S. Huang. SafeFall: Learning protective control for humanoid robots. _arXiv preprint arXiv:2511.18509_ , 2026. 

- [29] P. Strauch, D. M¨uller, S. Christen, A. Serifi, R. Grandia, E. Knoop, and M. B¨acher. Robot crash course: Learning soft and stylized falling. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 1727–1734, 2026. doi:10.1109/ICRA57385.2026.11696325. 

- [30] Y. Sun, R. Chen, K. S. Yun, Y. Fang, S. Jung, F. Li, B. Li, W. Zhao, and C. Liu. SPARK: Safe protective and assistive robot kit. In _IFAC Symposium on Robotics_ , 2025. URL `https: //intelligent-control-lab.github.io/spark/` . 

- [31] H. Xue, S. Liang, Z. Zhang, Z. Zeng, Y. Liu, Y. Lian, J. Wang, Q. Liu, X. Shi, and L. Yi. Collision-free humanoid traversal in cluttered indoor scenes. _IEEE Robotics and Automation Letters_ , 11(8):9183–9190, 2026. doi:10.1109/LRA.2026.3703590. 

- [32] R. Chen, Y. Sun, and C. Liu. Dexterous safe control for humanoids in cluttered environments via projected safe set algorithm. _arXiv preprint arXiv:2502.02858_ , 2025. 

- [33] D. Morton and M. Pavone. frax: Fast robot kinematics and dynamics in JAX. _arXiv preprint arXiv:2604.04310_ , 2026. ICRA 2026 Workshop on Frontiers of Optimization for Robotics. 

- [34] D. Morton and M. Pavone. Safe, task-consistent manipulation with operational space control barrier functions. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 187–194, 2025. doi:10.1109/IROS60139.2025.11246389. 

- [35] D. Morton, J. Arrizabalaga, Z. Manchester, and M. Pavone. ElastiQP: An always-feasible QP solver for constrained robot control. _arXiv preprint arXiv:2609.19080_ , 2026. 

- [36] J. Englsberger, A. Werner, C. Ott, B. Henze, M. A. Roa, G. Garofalo, R. Burger, A. Beyer, O. Eiberger, K. Schmid, and A. Albu-Sch¨affer. Overview of the torque-controlled humanoid robot toro. In _2014 IEEE-RAS International Conference on Humanoid Robots_ , pages 916–923, 2014. doi:10.1109/HUMANOIDS.2014.7041473. 

- [37] PICO Immersive Pte. Ltd. PICO 4 Ultra: An All-New Mixed Reality Experience. `https: //www.picoxr.com/global/products/pico4-ultra` , 2023. 

- [38] W. Xiao and C. Belta. High-order control barrier functions. _IEEE Transactions on Automatic Control_ , 67(7), 2022. doi:10.1109/TAC.2021.3105491. 

- [39] K. Tracy and Z. Manchester. On the differentiability of the primal-dual interior-point method. _arXiv preprint arXiv:2406.11749_ , 2024. 

- [40] J. Arrizabalaga, K. Tracy, and Z. Manchester. A differentiable interior-point method in single precision, 2026. URL `https://arxiv.org/abs/2605.17913` . 

- [41] A. Agrawal and K. Sreenath. Discrete control barrier functions for safety-critical control of discrete systems with application to bipedal robot navigation. In _Proceedings of Robotics: Science and Systems_ , Cambridge, Massachusetts, July 2017. doi:10.15607/RSS.2017.XIII. 073. 

12 

- [42] D. R. Agrawal and D. Panagou. Safe control synthesis via input constrained control barrier functions. In _2021 60th IEEE Conference on Decision and Control (CDC)_ , pages 6113–6118, 2021. doi:10.1109/CDC45484.2021.9682938. 

- [43] T. Flayols, A. Del Prete, P. Wensing, A. Mifsud, M. Benallegue, and O. Stasse. Experimental evaluation of simple estimators for humanoid robots. In _2017 IEEE-RAS 17th International Conference on Humanoid Robotics (Humanoids)_ , pages 889–895, 2017. doi: 10.1109/HUMANOIDS.2017.8246977. 

- [44] M. Baumgartner, D. M¨uller, A. Serifi, R. Grandia, E. Knoop, M. Gross, and M. B¨acher. CoCoInEKF: State estimation with learned contact covariances in dynamic, contact-rich scenarios. In _Proceedings of Robotics: Science and Systems_ , 2026. doi:10.48550/arXiv.2605.15122. 

- [45] Z. Zhao, L. Yu, K. Jing, and N. Yang. XRoboToolkit: A cross-platform framework for robot teleoperation. _2026 IEEE/SICE International Symposium on System Integration (SII)_ , pages 15–20, 2026. URL `https://api.semanticscholar.org/CorpusID:280417135` . 

13 

## **Appendix** 

|**A **|**Bac**|**kground: Humanoid Kinematics and Dynamics**|**15**|
|---|---|---|---|
||A.1|Kinematics<br>. . . . . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>15|
||A.2|Contact Kinematics . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>15|
||A.3|Joint Space Dynamics . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>15|
||A.4|Contact Space Dynamics . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>15|
||A.5|Actuation Modeling . . . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>16|
||A.6|Constrained Kinematics . . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>16|
||A.7|Constrained Dynamics<br>. . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>16|
||A.8|Constrained Operational Space Dynamics . . . . . . . . . . . . .|. . . . . . . . .<br>16|
|**B**|**Bac**|**kground: Control Barrier Functions**|**17**|
||B.1|Comments on Practical CBF Implementation<br>. . . . . . . . . . .|. . . . . . . . .<br>18|
|**C **|**Add**|**itional Implementation Details**|**18**|
||C.1|Timing and Performance . . . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>18|
||C.2|Contact Modes and Estimation . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>18|
||C.3|Constrained Retargeting Pipeline . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>19|
|**D **|**Alte**|**rnate Models for Humanoid Safety**|**20**|
||D.1|Humanoids on Mobile Bases . . . . . . . . . . . . . . . . . . . .|. . . . . . . . .<br>20|


14 

## **A Background: Humanoid Kinematics and Dynamics** 

_Notation for this section follows from [15, 16, 17], and all terms are computed with_ _`frax` [33]. For brevity, after a term is introduced, we drop the dependence on_ **q** _or_ **q** ˙ _in further expressions._ 

### **A.1 Kinematics** 

We consider a bipedal humanoid robot modeled as a kinematic tree with generalized coordinates **q** . These coordinates fully define the state of the robot with respect to an inertial reference frame, including both the configuration of the free-floating base **q** base, and all actuated DoFs on the robot body **q** body. In this paper, we model the free-floating base with six virtual joints (three prismatic and 


A Jacobian **J** ( **q** ) defines the relationship between an operational space velocity **_ν_** and the joint velocities **q** ˙ via **_ν_** = **J** ˙ **q** . Typically, when referring to a task _ti_ for a humanoid robot, we will consider **_ν_** _i_ to be a twist _∈_ R<sup>6</sup> for end-effector pose tracking (hands, and any feet not in contact), or a velocity _∈_ R<sup>3</sup> for center-of-mass tracking. We also denote _any_ inverse of a Jacobian **J** as **J**<sup>#</sup> . Later, we will refer to _dynamically-consistent_ inverses via the notation **J** , the _pseudoinverse_ as **J**<sup>_†_</sup> , and note that in the non-redundant full-rank case, **J**<sup>#</sup> = **J**<sup>_−_1</sup> . 

### **A.2 Contact Kinematics** 

For any feet in contact with the world, we can define a contact Jacobian: **J** _c_ ( **q** ) and its time derivative **J** ˙ _c_ ( **q** _,_ ˙ **q** ), defining the velocity **_ν_** _c_ and acceleration **_ν_** ˙ _c_ at the contact point. In this paper, we assume a planar contact model with a known flat ground plane, where 


### **A.3 Joint Space Dynamics** 

We consider a humanoid robot with the following dynamics, 


where **M** ( **q** ) is the joint-space mass matrix, **c** ( **q** _,_ ˙ **q** ) is the vector of centrifugal and Coriolis forces, **g** ( **q** ) is the gravity vector, **f** _c_ is the vector of contact forces and torques, and **Γ** is the vector of generalized joint torques. 

### **A.4 Contact Space Dynamics** 

At the point of contact, the projected dynamics of the system can be expressed as 


where **Λ** _c_ ( **q** ) is the contact-space inertia matrix, **_µ_** _c_ ( **q** _,_ **q** ˙ ) and **p** _c_ ( **q** ) are the projections of the centrifugal/Coriolis forces and gravity vector into contact space, and **J**<sup>¯</sup> _c_ ( **q** ) is the dynamicallyconsistent generalized inverse of **J** _c_ . The components of the joint-space and contact-space dynamic models are related via the following: 


For convenience, we define an auxiliary term **_µ_** _c,J_ ˙ in Eq. 19 to describe the component of **_µ_** _c_ associated with **J**<sup>˙</sup> , where 


15 

### **A.5 Actuation Modeling** 

The generalized torque vector **Γ** includes components associated with both the virtual joints for the free-floating base, and the _k_ actuated joints of the robot, i.e., **Γ** = � **Γ**<sup>_T_</sup> base **Γ**<sup>_T_</sup> body� _T_ . To account for only the actuated component, we define a selection matrix **S** such that 


### **A.6 Constrained Kinematics** 

We define the contact null space projection matrix as 


such that for an arbitrary input velocity vector **q** ˙ 0, the resultant **q** ˙ consistent with the contact constraints is 


Note that we use **J** _c_ as the inverse when constructing **N** _c_ , as opposed to the pseudoinverse. 

Incorporating the actuation model (Eq. 23), the resultant velocity of the actuated joints **q** ˙ body is the projection 


We can then express **q** ˙ as a function of the actuated component **q** ˙ body 


where the dynamically consistent inverse of **SN** _c_ is 


Here, we apply the pseudoinverse as **SN** _c_ is not necessarily full rank (which only occurs during a single-foot contact mode). In general, this implies that **q** ˙ can not take on arbitrary values in all cases. 

### **A.7 Constrained Dynamics** 

Given our assumption of a fixed contact model (Eqs. 14, 15), the dynamics in contact space (Eq. 17) simplify, allowing us to solve for **f** _c_ in terms of the generalized torques: 


Substituting **f** _c_ back into Eq. 16, we can express the constrained dynamics of the system as 


Eq. 31 can equivalently be posed as a function of the actuated torques only by applying Eq. 23 and replacing **Γ** with **S**<sup>_T_</sup> **Γ** body. 

### **A.8 Constrained Operational Space Dynamics** 

For a Jacobian **J** _t_ defining a generalized velocity **_ν_** _t_ = **J** _t_ ˙ **q** in task space, the constrained operational space dynamics take on the following form, 


where **Λ** _t|c_ ( **q** ) is the constrained operational space inertia matrix, **_µ_** _t|c_ ( **q** _,_ ˙ **q** ) and **p** _t|c_ ( **q** ) are the constrained projections of the centrifugal/Coriolis forces and gravity vector, and **_F_** is an operational space wrench. 

16 

We also define a constrained task Jacobian **J** _t|c_ , 


which projects an arbitrary **q** ˙ 0 into the task space while remaining in the null space of the contact constraints. Analogous to Eq. 25, we can also define a null space projection for the task, consistent with the contact constraints 


The components of the constrained operational-space dynamics are related to the joint-space and contact-space dynamics via the following: 


## **B Background: Control Barrier Functions** 

Consider a continuous-time dynamical system in control-affine form: 


with state **z** _∈Z ⊆_ R<sup>_n_</sup> , input **u** _∈U ⊆_ R<sup>_m_</sup> , and locally Lipschitz continuous dynamics functions _f_ : R<sup>_n_</sup> _→_ R<sup>_n_</sup> and _g_ : R<sup>_n_</sup> _→_ R<sup>_n×m_</sup> . 

Safety can be posed through the lens of set invariance. For a safe subset of the state space, _C ⊂Z_ , if we can define a control barrier function _h_ ( **z** ): R<sup>_n_</sup> _→_ R where _C_ is the zero-superlevel set of _h_ , then a controller satisfying 


for **u** _∈U_ and extended class _K∞_ function _α_ will render _C_ forward-invariant [8]. 

This condition (Eq. 40) can be integrated into a convex quadratic program (QP), paired with a min-norm objective to operate as a safety filter on a nominal (unsafe) controller: 


where _Lf h_ ( **z** )=<sup>_<u>dh</u>_</sup> _d_ **z**<sup>(</sup><sup>**z**)</sup><sup>_f_(</sup><sup>**z**) and</sup><sup>_Lgh_(</sup><sup>**z**)=</sup><sup>_<u>dh</u>_</sup> _d_ **z**<sup>(</sup><sup>**z**)</sup><sup>_g_(</sup><sup>**z**) are the Lie derivatives of</sup><sup>_h_along the dynam-</sup> ics, and _h_<sup>˙</sup> ( **z** _,_ **u** )= _Lf h_ ( **z** )+ _Lgh_ ( **z** ) **u** . 

The _relative degree_ of a CBF refers to the number of differentiations along the dynamics required before the control input **u** explicitly appears. CBFs require a relative degree of 1 (RD1), but with mechanical systems, CBFs are often of relative degree 2 (RD2). This high relative degree implies that _Lgh_ ( **z** ) = 0, and thus, we must differentiate along the dynamics again. The second timederivative of _h_ ( **z** ) can be expressed as 


where _LgLf h_ ( **z** ) _̸_ =0 for a RD2 CBF. 

Given this, we can construct a High-Order CBF (HOCBF) [38] for these RD2 constraints. Let _h_ 2( **z** )= _Lf h_ ( **z** )+ _α_ ( _h_ ( **z** )). Then, we modify the constraint in Eq. 41 to 


for an additional class _K∞_ function _α_ 2. 

17 

### **B.1 Comments on Practical CBF Implementation** 

When implementing CBFs on real robots, some assumptions and conditions are typically loosened with respect to the theory. Many of these violate any formal guarantees, but despite this, CBFs can still be extremely useful tools for _softer_ notions of safety. Below, we note a few common conditions seen in practice: 

- When enforcing a large number of CBFs, particularly with input constraints, these will sometimes be in conflict, resulting in an infeasible QP. In practice, relaxing the QP results in a reasonable solution that enforces (but does not guarantee) safety in most cases. Given this, we can update the QP (Eq. 41) by introducing a slack variable,<sup>4</sup> **t** , to handle the constraint violation with a large penalty, _ρ_ : 


- The set invariance condition of CBFs is defined for continuous-time systems, but the QP is solved in discrete-time. At high sampling rates ( _≈_ 1000 Hz) this difference is negligible, but towards lower sampling rates ( _≈_ 50 Hz) this can lead to noticeable violation and/or chatter near the boundary of the safe set. For further discussion, refer to discrete-time CBFs [41]. 

- It is often assumed that the control input for the CBF constraint is unbounded, i.e. _U_ = R<sup>_m_</sup> , but this does not hold in practice with actuator limits at the velocity and torque levels. Adding input constraints to the QP in combination with the CBF often works well in practice, but does not guarantee forward invariance of the safe set. For further discussion, see input-constrained CBFs [42] or the comparisons between torque-control and velocitycontrol CBFs with torque limits in [34]. 

- Model mismatch, including imperfect actuators, miscalibrated inertial values, or unreliable contact mode estimation, can reduce the performance of the CBF when deployed on hardware. 

## **C Additional Implementation Details** 

### **C.1 Timing and Performance** 

Desktop timing values were recorded on a PC with an i9-14900KF CPU, 64 GB RAM, and an RTX 4090 GPU. Edge device timing values were recorded on a Jetson Orin Nano with an Arm Cortex-A78AE CPU, 8 GB RAM, and an integrated Ampere GPU. The Orin was run at the standard (non-Super) power mode of 15 W. _All methods in this paper were run on CPU_ . As per [33], we evaluated performance with `time.perf` ~~`c`~~ `ounter` over 10,000 iterations, with `jax.block` ~~`u`~~ `ntil` ~~`r`~~ `eady()` called on all functions to avoid timing the asynchronous dispatch. We use JAX version 0.11.2 and the following flags: `JAX` ~~`E`~~ `NABLE` ~~`X`~~ `64=1` and `XLA` ~~`F`~~ `LAGS="--xla` ~~`c`~~ `pu` ~~`m`~~ `ulti` ~~`t`~~ `hread` ~~`e`~~ `igen=false"` . Running single-threaded was found to give both good performance and good resource management in a ROS2 stack with many nodes. 

### **C.2 Contact Modes and Estimation** 

As mentioned in Sec. A.2, we assume a planar contact model on the feet. For a bipedal humanoid, this yields four discrete contact modes: 0 (no contact), 1 (left foot), 2 (right foot), and 3 (both feet). All methods incorporate the current contact mode into the kinematics and dynamics models. 

> 4Note: solvers such as ElastiQP [35] or `qpax` [39, 40] can solve this problem structure without explicit materialization of the slacks **t** for improved performance. 

18 

Regarding contact estimation, we find that at the kinematics/input level, simple heuristics can lead to fairly reliable near-ground-truth desired contact modes under minor assumptions about the motion (such as planar contact and typical walking motions). In short, we look at the relative heights and velocities of the two feet, and determine contact based on which feet are near the ground and not moving (defined by threshold parameters on the height and planar/normal velocity). These heuristics implicitly assume that mode 0 (no contact) does not occur; a reasonable assumption for typical locomotion and manipulation tasks. 

For contact estimation at the dynamics/output level, currently, we evaluate the dynamic filter under well-known double-support (mode 3) contact. However, we aim to explore further integration with state estimation, such as model/optimization-based approaches [18, 43] or more recent work [44]. 

### **C.3 Constrained Retargeting Pipeline** 

The full pipeline for computing the constrained retargeting solution is as follows. Note that some components are loosely based on [20], for instance, the selection of the frame correspondence between the G1 and human reference. 

_Pre-processing (Before the QP solve)_ 

1. Record human reference data. We use a PICO 4 Ultra [37], similar to [1], with a custom C++ ROS2 interface for the XRoboToolkit SDK [45]. For teleoperation, high-frequency and smooth input data is critical to downstream performance, and this interface was designed to minimize latency and jitter. 

2. Adjust the desired orientations of the feet to be parallel with the floor, to better suit our planar contact model. 

3. Compute the velocity and position of the feet and incorporate this into a simple contact estimation heuristic (described in Sec. C.2). 

4. Rescale the positional data to approximately reflect the size difference between the human and Unitree G1. 

5. Update the heights of all bodies to put the lowest point on the feet at _z_ =0. As previously mentioned, this assumes that mode 0 (no contact) is not considered. 

_Constructing and solving the QP_ 

1. Compute the error dynamics for the frame correspondences between the (pre-processed) human data and the current robot state. 

2. Compute the Jacobians for all frames on the robot body with `frax` [33] 

3. Compute the CBF terms with `cbfpy` [34] 

4. Construct the QP matrices and solve the problem with `elastiqp.jax`<sup>5</sup> [35]. 

_Post-processing (After the QP solve)_ 

1. Integrate the optimal **q** ˙ according to the constrained kinematics 

2. Apply an exponential moving average filter to the free-floating base velocities to ensure a smooth observation 

On initialization, the first human pose in the reference motion may be quite different from the default standing pose of the robot. To align the internal state of the solver with this initial pose, we iterate until convergence in a sequential quadratic programming (SQP) fashion. Here, we perform the preprocessing step once, and then the QP solve and integration steps are executed repeatedly. Note that during this initialization phase, we integrate on the unconstrained kinematics, to allow for the 

> 5Note: `qpax` [39, 40] can also be used to solve the QP; while `qpax` is slower for online deployment, it is fully compatible with GPU and TPU. 

19 

necessary updates to the solver state. With a simple adaptive stepsize scheme, the SQP tends to converge in about 10 iterations. 

Following convergence, we can then begin online operation, taking only a single differential IK step per timestep, and employing the constrained kinematics. We limit this to a single step, because if multiple or a variable number of differential IK steps are performed per timestep during online control (as done in some retargeters such as [20]), adding a CBF constraint to this problem would misrepresent the _h_<sup>˙</sup> ( **z** ) term. 

## **D Alternate Models for Humanoid Safety** 

### **D.1 Humanoids on Mobile Bases** 

While traditionally _humanoid_ implies a bipedal system, often this is also used to describe upper-torso systems on a holonomic mobile base (for instance, the Galaxea R1 robot). In this case, the mobile base and any additional elevator/torso joints can be represented as a kinematic chain of prismatic and revolute joints, attached to the upper body. This yields three main benefits over a bipedal system, in the context of modeling and constraint enforcement: (1) the model is a pure kinematic tree, with no loop closures due to contacts with the ground, (2) there are no underactuated degrees of freedom from a floating base, and (3) the system is statically stable at rest. 

In this case, it generally makes more sense to use a model-based low-level controller (either inverse kinematics or dynamics), as opposed to RL. This low-level controller can easily be used in conjunction with, e.g., a learned vision-language-action model which outputs task-space commands, with the CBF enforcing safety. In this case, the _task-consistent_ CBF objective will reflect a hierarchy of tasks suited to the bimanual system: for instance, prioritizing tracking of the end-effectors (left and right hands) and possibly a head-mounted camera, while imposing a desired posture in the null space of the primary tasks. The QP form for the safety filter and low-level controller for this case can be found in [34]. 

20 

