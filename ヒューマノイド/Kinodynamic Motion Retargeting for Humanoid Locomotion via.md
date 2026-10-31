---
title: "Kinodynamic Motion Retargeting for Humanoid Locomotion via Multi-Contact Whole-Body Trajectory Optimization"
date: "2026-03-10"
authors: "Xiaoyu Zhang; Steven Haener; Varun Madabushi; Maegan Tucker"
url: https://arxiv.org/abs/2603.09956
pdf: https://arxiv.org/pdf/2603.09956
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.09956)** / [論文ページ](https://arxiv.org/abs/2603.09956)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Kinodynamic Motion Retargeting for Humanoid Locomotion via Multi-Contact Whole-Body Trajectory Optimization** 

Xiaoyu Zhang, Steven Haener, Varun Madabushi and Maegan Tucker 

**_Abstract_ — We present the Kinodynamic Motion Retargeting (KDMR) framework, a novel approach for humanoid locomotion that models the retargeting process as a multicontact, whole-body trajectory optimization problem. Conventional kinematics-based retargeting methods only look at kinematic feasibility, inevitably introducing physically inconsistent artifacts, such as foot sliding and ground penetration, that degrade the performance of downstream imitation learning policies. To address these inconsistencies, KDMR extends beyond pure kinematics to explicitly enforce rigid-body dynamics and scheduled contact constraints. This requires explicit contact sequences, which are estimated systematically using human ground-reaction force data. The result is dynamically feasible motions both in terms of the rigid-body dynamics and the enforced contacts. The approach also enables an operator to add additional constraints or costs such as minimizing acceleration or enforcing torque limits, improving the overall quality of the reference motion.** 

**We evaluate KDMR against the state-of-the-art baseline, GMR, across three key dimensions: 1) the dynamic feasibility and smoothness of the retargeted motions, 2) the accuracy of GRF tracking compared to raw source data, and 3) the training efficiency and final performance of downstream control policies trained via the BeyondMimic framework. Experimental results demonstrate that KDMR significantly outperforms purely kinematic methods, yielding dynamically viable reference trajectories that accelerate policy convergence and enhance overall locomotion stability. Our end-to-end pipeline will be open-sourced upon publication.** 


Fig. 1. Given a source human motion and measured ground-reaction forces (GRFs), the proposed KDMR performs contact-aware trajectory optimization to generate a contact-consistent and dynamically feasible robot reference. A downstream RL policy tracks this reference on the real humanoid robot. 

## I. INTRODUCTION 

Recent advances in humanoid locomotion have been largely driven by imitation learning and related approaches that transfer human-based motions, obtained primarily using motion capture (MoCap), to real-world humanoid robots. By incorporating human motion references into reward design, humanoid robots can reproduce agile and natural human-like behaviors. Furthermore, prior work has demonstrated that high-quality motion references can be leveraged to distilling reusable motion policies for generalizable control across a variety of downstream tasks [1], [2]. 

However, human-based motions cannot be applied to robot motion directly; bridging the gap between human and robot morphology necessitates a motion retargeting process. This process must rigorously account for discrepancies in joint limits, mass distribution, and actuation capabilities. State-ofthe-art retargeting methods only perform this mapping using kinematics, consequently introducing physical artifacts, such as foot sliding, ground penetration, and dynamically infeasible transitions [3]. If these artifacts are not explicitly 

Authors are with Georgia Institute of Technology, Atlanta, GA, USA {xzhang636,shaener3,vmadabushi3,mtucker}@gatech.edu 

resolved, they persist throughout the training process, forcing the learning agent to compensate for physically impossible references. This inherently limits the sample efficiency and ultimate performance of the downstream control policies. 

Purely kinematics-based methods struggle to eliminate these artifacts because they neither enforce system dynamics nor capture the underlying contact forces. Moreover, simplified MoCap skeletons often omit articulated toes and detailed plantar contact geometry, thereby losing important foot– ground interaction information. GRF measurements provide complementary information about weight bearing and load transfer, which is essential for identifying heel–toe contact patterns in multi-contact humanoid motion [4]. 

To address these complexities, we propose a novel method for kinodynamic motion retargeting that explicitly certifies dynamic feasibility and holonomic constraint satisfaction for any arbitrary motion, including multi-contact locomotion. Our approach formulates the retargeting procedure, leveraging human ground reaction forces as a primary physical anchor, as a whole-body trajectory optimization problem. This approach explicitly accounts for dynamic feasibility, enforces proper holonomic constraints for any contact sequence, and 

allows for additional constraints such as actuator limits. The main contributions of this work are as follows: 

- 1) A comprehensive pipeline, named Kinodynamic Motion Retargeting (KDMR), that jointly optimizes kinematics and whole-body dynamics. The result is smooth, dynamically feasible reference trajectories that bridge the morphological gap between humans and humanoid robots. 

- 2) Demonstration that dynamics-consistent references improve sample efficiency and tracking performance across two motions: forward walking and twisting. 

## II. RELATED WORK 

## _A. Imitation Learning for Humanoid Locomotion_ 

Imitation Learning (IL) is a common approach for producing natural, smooth motion tracking policies by imitating human data. DeepMimic [5] introduced a reinforcement learning (RL) approach to learn to reproduce motion references for different characters in a simulated environment using a goal-oriented reward function. Adversarial Motion Prior (AMP) [1] employs an adversarial discriminator to model motion style as a distributional prior, enabling better generalization beyond individual reference trajectories. 

Building upon these prior efforts, several works [6], [7], [8] demonstrated quadrupedal locomotion by leveraging animal motion capture (MoCap) data. More recently, to enable human-like motion generation, methods such as ASAP [9], KungFuBot [10], Hub [11], OmniH2O [12], UniTracker [13], TWIST [14], and BeyondMimic [2] have adopted imitation learning frameworks to achieve humanoid locomotion skills. Although these approaches demonstrate agile and natural movements using retargeted kinematic trajectories, handling dynamic inconsistencies and retargeting artifacts during training remains challenging, critically impacts sample efficiency, learning stability, and performance [3]. In this paper, we mitigate retargeting artifacts and improve dynamic feasibility by casting the problem as a whole-body trajectory optimization problem. 

## _B. Kinematic Motion Retargeting_ 

Motion retargeting originally aimed to transfer human motions to character animations in computer graphics [15], [16]. When extending this process to humanoid robots, additional challenges emerge due to morphological differences and dynamic inconsistencies, such as variations in degrees of freedom (DoFs), link lengths, inertial properties, and actuator limits. Consequently, directly mapping joint values from human data to humanoid robots is insufficient [17], [18], often leading to non-physical artifacts such as base floating, foot penetration, foot sliding, and non-smooth motions. 

Recent works such as PHC [19] and its subsequent extensions [12], [9], [20], aim to mitigate these morphological challenges. They formulate retargeting as an inverse kinematics (IK) problem solved via gradient descent through forward kinematics. However, the resulting motions may be dynamically infeasible and still exhibit noticeable artifacts. GMR 

[3] improves upon this paradigm by incorporating a nonuniform local scaling strategy combined with a two-stage IK formulation to improve geometric consistency. While they perform well in common human skeleton models, differences in skeleton structure (e.g., additional intermediate foot joints) can introduce systematic height and grounding offsets, since ground alignment is often computed from specific joint positions rather than true contact geometry. Despite these improvements, GMR still suffers from similar limitations, as ensuring dynamic feasibility and eliminating artifacts across the entire motion reference trajectories remain unresolved. 

## _C. Dynamics-Informed Motion Retargeting_ 

The artifacts arising from purely kinematic motion retargeting are closely coupled with violations of dynamic feasibility [21], [22], as system dynamics and contact complementarity constraints are typically not enforced. Consequently, incorporating system dynamics into the retargeting process can substantially improve the physical plausibility of the generated motions and facilitate their transfer to real robots beyond visually convincing animations. 

Several works have attempted to address this issue by refining kinematic reference trajectories through dynamicsaware optimization. For example, [23] enables robust transfer of complex animal motions to quadruped robots by jointly aligning spatial kinematics and temporal dynamics. Similarly, SPARK [24] also refines kinematically retargeted motions through full-order kinodynamic trajectory optimization. It progressively solves kinematic trajectory optimization, inverse dynamics, and full kinodynamic optimization, assuming that foot-level contact labels are provided with the source motion. In contrast, our work focuses on transferring fine-grained foot–ground interaction by inferring a pointlevel heel–toe contact schedule from synchronized GRF and contact-point velocities. Therefore, SPARK and KDMR address different aspects of dynamics-aware retargeting: progressive optimization and skeleton calibration in SPARK, and GRF-informed multi-point contact transfer in KDMR. 

Other work uses ground-reaction-force measurement as an alternative source of contact information [25], [26], [27], [28]; KDMR leverages human GRF to systematically detect contact phase and as an optional force-initialization signal. KDMR also computes an explicit, reproducible per-point contact schedule from measured marker velocity and models each foot’s heel and toe as independently-active contact candidates, merging them into a single line-contact wrench only when both are planted. This enables changing contact modes, unlike SPARK’s single rigid-foot contact wrench. 

A complementary line of work enforces physical consistency through simulator rollouts. DynaRetarget [29] refines kinematic references using sampling-based trajectory optimization in MuJoCo [30], whereas Direct Dynamic Retargeting [31] directly optimizes task-space tracking through sampling-based MPC. Both resolve contacts implicitly through simulation and depend on sampling objectives and initialization. NMR [32] distills trajectories generated by simulated RL experts into a neural retargeter, enabling 


Fig. 2. Overview of KDMR. Human pose trajectories and GRF measurements are used to infer the contact schedule and initialize the robot motion. The initial trajectory is then refined through contact- and dynamics-constrained whole-body optimization to produce a dynamically feasible robot reference. 

fast inference at the cost of morphology-specific training and implicit, distribution-dependent physical feasibility. In contrast, KDMR requires no learned retargeter and explicitly optimizes robot dynamics, contact forces, and scheduled contact constraints. 

## III. METHOD 

Our method, KDMR, summarized in Fig. 2, consists of two main components: contact force decomposition and kinodynamic motion retargeting. We first decompose the foot-level ground reaction force into contact-point forces and infer the corresponding contact sequence, as described in Sec. III-B. Given this contact sequence and an initial kinematic retargeting trajectory described in Sec. III-C, we then solve a multi-contact trajectory optimization problem to generate the final dynamically feasible motion reference, as described in Sec. III-D. 

_A. Problem Statement_ 

The input human biomechanics data consist of synchronized motion and ground reaction force (GRF) measurements over _T_ + 1 frames, indexed by _t_ = 0 _, . . . , T_ . The motion is reconstructed from three-dimensional marker trajectories and fitted in OpenSim [33] to a human skeletal model with _Nh_ degrees of freedom, yielding the generalized coordinates **_q_** _t_<sup>h</sup><sup>_∈_R</sup><sup>_Nh_and velocities</sup><sup>**_q_**˙</sup> _t_<sup>h. The fitted motion is represented</sup> by a collection of human body poses _X_<sup>target</sup> = _{x_<sup>target</sup> _t,ℓ_<sup>h</sup> _∈ SE_ (3) _| ℓ_<sup>h</sup> _∈L_<sup>h</sup> _, t_ = 0 _, . . . , T }_ , where _L_<sup>h</sup> is the set of selected human bodies and _x_<sup>target</sup> denotes the world-frame _t,ℓ_<sup>h</sup> pose of human body _ℓ_<sup>h</sup> at frame _t_ . The synchronized GRF measurements provide the net force acting on each foot, denoted by **_λ_**<sup>h</sup> _t_<sup>=</sup><sup>_{_</sup><sup>**_λ_**h</sup> _t,L_<sup>_,_</sup><sup>**_λ_**</sup> _t,R_<sup>h</sup><sup>_}_.</sup> 

The humanoid robot generally has a different kinematic structure, mass distribution, and foot geometry from the human subject. We model the robot as a floating-base system with configuration **_q_** _t_ = ( **_q_** _t,b,_ **_q_** _t,l_ ) _∈Q_ = _SE_ (3) _× Q_<sup>_l_</sup> , where **_q_** _t,b ∈ SE_ (3) denotes the pelvis-attached floatingbase pose and **_q_** _t,l ∈Q_<sup>_l_</sup> _⊆_ R<sup>_Nl_</sup> contains the _Nl_ actuated 

joint coordinates. The corresponding generalized velocity and acceleration are denoted by **_q_** ˙ _t_ and **_q_** ¨ _t_ , respectively. 

To transfer the human motion to the robot, we define a set of corresponding rigid-body links _M_ = _{_ ( _ℓ_<sup>h</sup> _m_<sup>_, ℓ_r</sup> _m_<sup>)</sup><sup>_}N_</sup> _m_<sup>_M_</sup> =1<sup>,</sup> where _ℓ_<sup>h</sup> _m_<sup>and</sup><sup>_ℓ_r</sup> _m_<sup>denote the corresponding human and robot</sup> links, respectively. The human-link poses _Xt,m_<sup>target</sup> serve as task-space tracking targets for the corresponding robot links. Given _X_<sup>target</sup> , **_λ_**<sup>h</sup> , _M_ , and the robot model, our objective is to generate a dynamically feasible robot reference trajectory. Let _Z_ = _{_ **_q_** _t,_ **_q_** ˙ _t,_ **_q_** ¨ _t,_ **_τ_** _t,_ **_λ_** _t}_<sup>_T_</sup> _t_ =0<sup>collecttherobot</sup> configurations, velocities, accelerations, actuator torques, and contact forces. The retargeting problem is formulated abstractly as 


where **_I_** denotes the contact schedule constructed from the human motion and GRF measurements. The optimized trajectory should preserve the target human motion while satisfying the robot dynamics, scheduled contact constraints, and physical limits. The construction of **_I_** and the initialization of **_λ_** _t_ are described in Sec. III-B, followed by the detailed trajectory optimization formulation. 

## _B. Contact Sequence Detection_ 

The GRF measurements introduced in Sec. III-A represent the resultant force acting on each entire human foot, whereas the robot dynamics model applies forces at four discrete contact points. We therefore infer a point-level binary contact schedule over _C_ = _{_ LH _,_ LT _,_ RH _,_ RT _}_ , where _c ∈C_ indexes an individual contact point. Let _F_ = _{_ L _,_ R _}_ denote the set of feet, with _C_ L = _{_ LH _,_ LT _}_ and _C_ R = _{_ RH _,_ RT _}_ denoting the contact points associated with each foot. 

We first determine the foot-level stance state _st,cf ∈{_ 0 _,_ 1 _}_ for _cf ∈{L, R}_ by thresholding the measured vertical GRF, such that _st,cf_ = 1 when _λ_<sup>h</sup> _t,c_<sup>_,z_</sup> _f_<sup>_>ϵ_force.ThisGRFgate</sup> prevents false-positive contacts when an airborne foot has a small instantaneous velocity, for example near the apex of its swing trajectory. 

Within each detected stance phase, we use the velocities of the corresponding human heel and toe sites to determine which contacts participate. A rigid point in non-slipping contact with static ground should have approximately zero world-frame velocity. Motivated by this property and contactcandidate velocity representations such as CoCo-InEKF [34], we compute the velocity of contact _c ∈C_ directly from the fitted OpenSim human model: 


where **_J_** _c_<sup>his the world-frame translational Jacobian of human</sup> heel or toe site _c_ . The binary contact state is defined as 


We use the full three-dimensional velocity norm and the same threshold for both cyclic and non-cyclic motions. The resulting contact schedule is **_I_** = _{_ I _t,c | t_ = 0 _, . . . , T, c ∈ C}_ . The current implementation uses binary GRF and velocity gates and does not employ foot-height cues, learned contact confidence, or contact covariance estimation. 

The contact schedule determines which point-force variables may be active. For each foot _f ∈F_ , let 


denote its active contact points at frame _t_ . The measured foot-level GRF is mass-scaled and equally distributed among the active contact points to initialize the nonlinear program (NLP): 


This equal split provides only an initial guess; the final point forces are independently optimized subject to the robot dynamics and contact constraints. 

## _C. Kinematics-Based Initialization_ 

Our method is initialized using the IK-based retargeting approach. This stage serves only as an initial guess and tracking prior for the dynamics-based retargeting stage described in Sec. III-D. Given the target poses _X_<sup>target</sup> and body correspondences _M_ introduced in Sec. III-A, we compute the initial robot configuration at each frame _t_ as 


where **_q_** _t_<sup>ldenotesthelocaljointconfigurationand</sup><sup>**_W_**</sup><sup>_m⪰_0</sup> weights the task-space components of correspondence _m_ . Let FK _ℓ_ r _m_ ( **_q_** _t_ ) = ( **_p_**<sup>r</sup> _t,m_<sup>_,_</sup><sup>**_R_**</sup> _t,m_<sup>r)and</sup><sup>_X_target</sup> _t,m_ = ( **_p_**<sup>target</sup> _t,m ,_ **_R_** _t,m_<sup>target</sup> ). The pose residual is defined as 


The resulting sequence _{_ **_q_** _t_<sup>kin</sup> _}_<sup>_T_</sup> _t_ =0<sup>matchestheselected</sup> human-link poses under the robot morphology and joint limits. Because the configurations are obtained without enforcing temporal dynamics, contact consistency, friction constraints, or torque limits, the resulting motion may exhibit foot sliding, ground penetration, temporal discontinuities, or dynamically infeasible transitions. The subsequent dynamicsbased retargeting stage reduces these artifacts by enforcing trajectory-level dynamics and contact constraints, using _{_ **_q_** _t_<sup>kin</sup> _}_<sup>_T_</sup> _t_ =0<sup>as both the configuration initial guess and the task-</sup> space tracking prior. 

## _D. Kinodynamic Motion Refinement_ 

The kinematic trajectory _{_ **_q_** _t_<sup>kin</sup> _}_<sup>_T_</sup> _t_ =0<sup>obtained from Sec. III-</sup> C provides a morphology-consistent warm start, but it does not enforce rigid-body dynamics, scheduled contact constraints, friction constraints, or actuator limits. Therefore, it may contain non-physical artifacts such as foot slip, ground penetration, and high-acceleration motions. We use **_q_** _t_<sup>kin</sup> as the tracking prior and initialization for the following dynamics-based retargeting problem. 

_1) Dynamics:_ The robot’s rigid-body dynamics follow the Euler-Lagrange equations of motion [35], 


where **_D_** _∈_ R<sup>(</sup><sup>_Nl_+6)</sup><sup>_×_(</sup><sup>_Nl_+6)</sup> is the generalized inertia matrix, **_H_** collects the Coriolis, centrifugal, and gravity terms, and **_B_** maps the actuator torques **_τ_** _t_ to the generalized coordinates, and _At ⊆C_ is the active contact set from Sec. III-B. Each active contact _c_ enters the dynamics through its Jacobian **_J_** _c_ ( **_q_** _t_ ), which maps generalized velocity to the world-frame velocity components conjugate to the contact wrench **_λ_** _t,c_ , and is applied as a generalized force via **_J_** _c_<sup>T</sup><sup>**_λ_**</sup><sup>_t,c_.Every</sup> wrench not in _At_ is fixed to zero, **_λ_** _t,c_ = **0** , rather than left unconstrained, so an inactive contact cannot inject a physically ungrounded force into the dynamics. The contact-force variables are warm-started from the mass-scaled, equallysplit measured GRF of Sec. III-B (Eq. (5)); this is an initialization only; **_λ_** _t,c_ is subsequently optimized jointly with **_q_** _t,_ **_q_** ˙ _t,_ **_q_** ¨ _t,_ **_τ_** _t_ subject to the constraints below. 

_2) Holonomic Constraints:_ The dimension of **_λ_** _t,c_ and its associated no-slip constraint depend on which contact points are active on a given foot. For each foot, if only one contact point is active, the active contact point is modeled as a line contact and assigned a 5D wrench constraint **_λ_** _t,c_ = [ _Fx, Fy, Fz, Mx, Mz_ ] _∈_ R<sup>5</sup> . When the foot has both heel and toe planted, we merge merge the heel and toe line contacts into a single 6D wrench at the foot’s midpoint 

frame, **_λ_**<sup>mid</sup> _t,f_<sup>=[</sup><sup>_Fx, Fy, Fz, Mx, My, Mz_]</sup><sup>_∈_R6,andfixthe</sup> individual point wrenches to zero. In this way, we handle the sixteen possible combinations of contact modes without introducing redundant constraints into the dynamic trajectory optimization problem. 

For every active contact, the corresponding point (or midpoint) linear velocity is constrained to zero: 


This velocity-level no-slip constraint, together with the trapezoidal integration of Sec. III-D.4, implicitly keeps the contact acceleration small whenever a contact remains active across consecutive frames. For an inactive contact, the force is constrained by **_λ_** _t,c_ = **0** for _c ∈A/ t_ . 

Each active wrench satisfies a linearized friction pyramid on its linear components, 


with _µ_ being the friction coefficient and _λ_<sup>_x_</sup> _t,c_<sup>_, λ_</sup> _t,c_<sup>_y, λz_</sup> _t,c_<sup>be-</sup> ing the forward, lateral, and vertical force components of **_λ_** _t,c_ . Additionally, zero moment point (ZMP) constraints are imposed: 


with the foot’s physical half-width _w_ and half-length _ℓ_ . Note that the second ZMP constraint (on _M_<sup>_y_</sup> is only applied for 6D wrenches. The yaw moment _M_<sup>_z_</sup> is left unconstrained in both cases. 

_3) Objective:_ For _t_ = 0 _, . . . , T −_ 1, the stage cost tracks the kinematic reference, regularizes acceleration, torque, and contact-force magnitude and smoothness, and penalizes the height of each active contact: 


Here **_p_** _t,_ **_ξ_**<sup>ˆ</sup> _t_ are the base position and orientation quaternion, and **_q_** _t,l_ the actuated joint coordinates. 

_4) NLP Implementation:_ Configurations, velocities, and accelerations obey trapezoidal integration for _t_ = 0 _, . . . , T −_ 1: 


The dynamics-based retargeting problem is then the following NLP: 


Here **_λ_** _t_ = _{_ **_λ_** _t,c}c∈C_ collects all four contact forces at frame _t_ , and _τ_ max and ( **_q_** min _,_ **_q_** max) denote the actuator-torque and configuration limits, respectively. 

## IV. RESULTS 

We evaluate KDMR by retargeting walking and wholebody twisting motions from an open-source biomechanics dataset [25] to the Unitree G1 humanoid. We compare KDMR with GMR [3], a kinematic retargeting baseline. We first describe the experimental setup in Sec. IV-A. We then evaluate the retargeted motion, contact behavior, and downstream policy performance in Secs. IV-B–IV-C. Finally, we present the real-robot deployment results in Sec. IV-D 

## _A. Implementation Details_ 

We implement our optimization framework using CasADi [36] to formulate and solve the nonlinear programming (NLP) problem, alongside Pinocchio [37] for efficiently computing the rigid-body kinematics and dynamics. This implementation makes introducing a new target robot straightforward. Specific cost function weights and other implementation details can be found on our repository<sup>1</sup> . For the downstream evaluation, the motion tracking policies are trained using the default BeyondMimic pipeline [2], implemented by the MJLab framework [38]. To ensure a fair comparison, we carefully tuned GMR and applied the minimum-height correction described in the original paper to reduce floating and ground-penetration artifacts. 

## _B. Dynamic Feasibility and Motion Smoothness_ 

We first evaluate whether KDMR improves the dynamic feasibility and temporal smoothness of the retargeted motion while preserving its principal kinematic characteristics. We use the treadmill walking sequence for this comparison because its repeated gait cycles make contact violations and trajectory discontinuities particularly visible. 

As shown in Fig. 3, KDMR produces the same overall motion pattern as GMR, while introducing localized corrections to the base and lower-limb trajectories. The largest differences occur around the ankle joints, whose configurations directly affect the heel and toe positions. These deviations are necessary for satisfying the robot dynamics and holonomic constraints for the prescribed contact schedule. 

1https://anonymous.4open.science/r/KDMR 


Fig. 3. Comparison of retargeted trajectories produced by KDMR and GMR over a time segment (20–27 s) of the full motion sequence. (a) Robot base configuration **_q_** _b_ , consisting of three translational and three rotational coordinates. (b) Corresponding base velocity **_q_** ˙ _b_ . (c) Joint configuration **_q_** leg of one leg, ordered from the hip-pitch joint to the ankle-roll joint. (d) Corresponding joint velocity **_q_** ˙leg. Here, _qb,i_ and _q_ ˙ _b,i_ denote the _i_ -th base coordinate and its velocity, while _q_ leg _,i_ and _q_ ˙leg _,i_ denote the position and velocity of the _i_ -th leg joint, respectively, for _i_ = 0 _, . . . ,_ 5. 

TABLE I 

COMPARISON OF KDMR AND GMR ACROSS MEAN ERRORS: GLOBAL BODY POSITION ERROR ( _Eg−bpe_ ), BODY POSITION ERROR ( _Ebpe_ ), AND JOINT POSITION ERROR ( _Ejpe_ ). EACH ERROR IS COMPUTED OVER 100 ROLLOUTS WITH DIFFERENT SEEDS. 

||||_E_g-bpe|(mm)|||_E_bpe (|mm)|||_E_jpe (m|rad)||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Motion|Method|Mean|Median|Min.|Max.|Mean|Median|Min.|Max.|Mean|Median|Min.|Max.|
|Walk|GMR|14.7|14.6|12.9|17.9|12.8|12.7|10.8|16.0|40.6|40.8|38.5|42.7|
||KDMR|**9.1**|**9.1**|**7.5**|**12.9**|**8.3**|**8.2**|**6.6**|**12.3**|**29.4**|**29.4**|**27.7**|**31.7**|
|Tit|GMR|22_._35|21_._88|19_._25|27_._32|18_._22|17_._99|15_._47|23_._49|46_._31|46_._21|43_._31|51_._62|
|wser|KDMR|**11.9**|**11.7**|**9.8**|**14.04**|**10.8**|**10.5**|**8.4**|**14.8**|**33.6**|**33.5**|**31.8**|**36.3**|


The foot-height comparison in Fig. 4 further illustrates this distinction. During each stance phase, KDMR constrains the active heel or toe contact points to remain on the ground surface. In contrast, GMR does not explicitly impose stancephase contact constraints and therefore frequently produces foot-floating artifacts. Moreover, even when a GMR contact point is geometrically close to the ground, physical contact is not guaranteed because its contact force and consistency 

with the whole-body dynamics are not enforced. KDMR instead jointly enforces the active contact heights, feasible contact forces, and whole-body equations of motion. The foot-height result therefore provides geometric evidence of the improved contact feasibility, while the dynamics and contact-force constraints establish its dynamic consistency. 

The velocity profiles in Figs. 3b and 3d show a corresponding improvement in motion smoothness. GMR exhibits 


Fig. 4. The height of heel and toe with contact window. 


Fig. 5. Mean episode rewards over three independent training runs. Solid lines show the mean, and shaded regions show one standard deviation. 

TABLE II 

abrupt variations and high-magnitude velocity spikes, particularly in the lower-limb joints around contact transitions. KDMR substantially reduces these fluctuations and produces more regular, temporally continuous velocity profiles. 

Overall, these results show that KDMR preserves the gait style while producing smoother trajectories and more physically consistent stance contacts than the kinematic baseline. 

## _C. Downstream Policy Tracking Performance_ 

Next, we evaluate whether the improved contact and dynamic consistency of KDMR benefits downstream policy learning. For each motion, we train separate policies to track the references generated by GMR and KDMR. The two methods use identical observations, actions, reward terms, network architectures, PPO hyperparameters, training budgets, and simulation settings. The only difference is the retargeted reference motion used for training. Figure 5 shows that policies trained with KDMR references achieve higher rewards with fewer environment samples and converge earlier than those trained with GMR references. 

After training, each policy is evaluated against its corresponding training reference over 100 rollouts with different random seeds. Table I reports the body-position and jointposition tracking errors. KDMR achieves lower errors across all three metrics for both motions. For walking, KDMR reduces the mean global body position error ( _E_ g-bpe), body position error ( _E_ bpe), and joint position error ( _E_ jpe) by 38 _._ 1%, 35 _._ 2%, and 27 _._ 6%, respectively. For the twisting motion, the reductions are 46 _._ 8%, 40 _._ 7%, and 27 _._ 4%. 

Together, the training curves and rollout results show that KDMR references are learned with better sampling efficiency and reproduced more accurately under the same policylearning setup. Combined with the contact-consistency and smoothness results in Sec. IV-B, these findings suggest that removing dynamically inconsistent artifacts, such as stancephase foot floating and abrupt trajectory variations, provides a more learnable reference and reduces the compensatory behavior required from the tracking policy. 

RUNTIME COMPARISON OF GMR AND KDMR FOR GENERATING RETARGETED REFERENCE TRAJECTORIES OF _800_ FRAMES 

|Method|Motion|Runtime [s]|
|---|---|---|
|GMR|Walking<br>Twist|_7_<br>_10_|
|KDMR|Walking<br>Twist|_88.6_<br>_282.4_|


## _D. Real-World Transfer_ 

We deploy the policies _π_ GMR and _π_ KDMR for both motions on the real Unitree G1 robot, with the performance best shown in the supplemental video. Both policies can be transferred without real-world fine-tuning. For the twisting motion, however, _π_ GMR exhibits more fragile behavior and is more susceptible to falling during abrupt whole-body transitions, whereas _π_ KDMR produces more stable executions. This qualitative observation suggests that smoother and dynamically consistent references can facilitate real-world transfer for motions involving rapid whole-body transitions. 

## V. LIMITATION 

A primary limitation of KDMR is its computational cost. As shown in Table II, KDMR is slower than the purely kinematic GMR baseline because it solves a constrained trajectory optimization problem involving whole-body dynamics and contact forces. Nevertheless, KDMR is designed as an offline motion-retargeting method, and real-time computation is not its objective. Each reference trajectory is generated only once and can then be reused throughout policy training and deployment. As the training curves and rollout results show, this one-time preprocessing cost is a favorable tradeoff for the improved sample efficiency and tracking quality it yields downstream. 

We also note that kinodynamic retargeting may not be necessary for every type of motion. We expect its benefits to be most pronounced for motions with complex contact sequences, where enforcing dynamic feasibility improves the smoothness and success rate of the downstream tracking policy. 

## VI. CONCLUSION 

In this work, we introduce a kinodynamic motion retargeting pipeline for humanoid whole-body locomotion tasks, formulated through a multi-contact dynamic model. Our experiments demonstrate that the proposed method significantly outperforms purely kinematic baselines in mitigating physical artifacts arising from dynamic inconsistencies. Extending beyond generating visually plausible kinematics, our framework successfully recovers accurate foot contact events and the corresponding ground reaction force magnitudes directly from human source data. 

## REFERENCES 

- [1] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “AMP: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , 2021. 

- [2] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [3] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” _arXiv preprint arXiv:2510.02252_ , 2025. 

- [4] T. K. Uchida and S. L. Delp, _Biomechanics of movement: the science of sports, robotics, and rehabilitation_ . Mit Press, 2021. 

- [5] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [6] X. B. Peng, E. Coumans, T. Zhang, T.-W. E. Lee, J. Tan, and S. Levine, “Learning agile robotic locomotion skills by imitating animals,” in _Robotics: Science and Systems_ , 07 2020. 

- [7] C. Li, M. Vlastelica, S. Blaes, J. Frey, F. Grimminger, and G. Martius, “Learning agile skills via adversarial imitation of rough partial demonstrations,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 342–352. 

- [8] E. Vollenweider, M. Bjelonic, V. Klemm, N. Rudin, J. Lee, and M. Hutter, “Advanced skills through multiple adversarial motion priors in reinforcement learning,” _arXiv preprint arXiv:2203.14912_ , 2022. 

- [9] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [10] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li, “Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills,” _arXiv preprint arXiv:2506.12851_ , 2025. 

- [11] T. Zhang, B. Zheng, R. Nai, Y. Hu, Y.-J. Wang, G. Chen, F. Lin, J. Li, C. Hong, K. Sreenath _et al._ , “Hub: Learning extreme humanoid balance,” _arXiv preprint arXiv:2505.07294_ , 2025. 

- [12] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning,” _arXiv preprint arXiv:2406.08858_ , 2024. 

- [13] K. Yin, W. Zeng, K. Fan, M. Dai, Z. Wang, Q. Zhang, Z. Tian, J. Wang, J. Pang, and W. Zhang, “Unitracker: Learning universal whole-body motion tracker for humanoid robots,” _arXiv preprint arXiv:2507.07356_ , 2025. 

- [14] Y. Ze, Z. Chen, J. P. Araújo, Z.-a. Cao, X. B. Peng, J. Wu, and C. K. Liu, “Twist: Teleoperated whole-body imitation system,” _arXiv preprint arXiv:2505.02833_ , 2025. 

- [15] Z. Popovi´c and A. Witkin, “Physically based motion transformation,” in _Proceedings of the 26th annual conference on Computer graphics and interactive techniques_ , 1999, pp. 11–20. 

- [16] S. Tak and H.-S. Ko, “A physically-based motion retargeting filter,” _ACM Transactions on Graphics (ToG)_ , vol. 24, no. 1, pp. 98–117, 2005. 

- [17] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [18] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

- [19] Z. Luo, J. Cao, A. W. Winkler, K. Kitani, and W. Xu, “Perpetual humanoid control for real-time simulated avatars,” in _International Conference on Computer Vision (ICCV)_ , 2023. 

- [20] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, C. Liu, G. Shi, X. Wang, L. Fan, and Y. Zhu, “HOVER: Versatile neural whole-body controller for humanoid robots,” _arXiv:2410.21229_ , 2024. 

- [21] J. W. Grizzle, C. Chevallereau, R. W. Sinnet, and A. D. Ames, “Models, feedback control, and open problems of 3d bipedal robotic walking,” _Automatica_ , vol. 50, no. 8, pp. 1955–1988, 2014. 

- [22] J. P. Reher, A. Hereid, S. Kolathaya, C. M. Hubicki, and A. D. Ames, “Algorithmic foundations of realizing multi-contact locomotion on the humanoid robot durus,” in _Algorithmic Foundations of Robotics XII: Proceedings of the Twelfth Workshop on the Algorithmic Foundations of Robotics_ . Springer, 2020, pp. 400–415. 

- [23] T. Yoon, D. Kang, S. Kim, J. Cheng, M. Ahn, S. Coros, and S. Choi, “Spatio-temporal motion retargeting for quadruped robots,” _IEEE Transactions on Robotics_ , 2025. 

- [24] H. Wang, Q. Liao, B. Zhang, K. Ren, K. Sreenath, and X. Xiong, “SPARK: Skeleton-parameter aligned retargeting on humanoid robots with kinodynamic trajectory optimization,” _arXiv preprint arXiv:2603.11480_ , 2026. 

- [25] K. Scherpereel, D. Molinaro, O. Inan, M. Shepherd, and A. Young, “A human lower-limb biomechanics and wearable sensors dataset during cyclic and non-cyclic activities,” _Scientific Data_ , vol. 10, no. 1, p. 924, 2023. 

- [26] X. Han, B. Senderling, S. To, D. Kumar, E. Whiting, and J. Saito, “Groundlink: A dataset unifying human body movement and ground reaction dynamics,” in _SIGGRAPH Asia 2023 Conference Papers_ , 2023, pp. 1–10. 

- [27] S. Ren, Y. Lu, J. Huang, J. Zhao, H. Zhang, T. Yu, Q. Shen, and X. Cao, “Motionpro: exploring the role of pressure in human mocap and beyond,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 27 760–27 770. 

- [28] C. Le, H.-P. Le, D. Le, M.-T. Duong, V.-B. Nguyen, and M.-H. Le, “Physics-informed ground reaction dynamics from human motion capture,” in _2025 17th International Conference on Human System Interaction (HSI)_ . IEEE, 2025, pp. 1–6. 

- [29] V. Dhedin, I. Taouil, S. Omar, D. Yu, K. Tao, A. Dai, and M. Khadiv, “Dynaretarget: Dynamically-feasible retargeting using sampling-based trajectory optimization,” _arXiv preprint arXiv:2602.06827_ , 2026. 

- [30] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2012, pp. 5026–5033. 

- [31] C. Roux, L. De Matteïs, A. Jordana, V. Guillet, N. Mansard, O. Stasse, and P. Souères, “Direct dynamic retargeting for humanoid imitation learning from videos,” _arXiv preprint arXiv:2605.23762_ , 2026. 

- [32] Q. Zhao, K. Yang, X. Wang, S. Zhao, Y. Lu, X. Zhang, Q. Shen, X.X. Long, and X. Cao, “Make tracking easy: Neural motion retargeting for humanoid whole-body control,” _arXiv preprint arXiv:2603.22201_ , 2026. 

- [33] S. L. Delp, F. C. Anderson, A. S. Arnold, P. Loan, A. Habib, C. T. John, E. Guendelman, and D. G. Thelen, “Opensim: open-source software to create and analyze dynamic simulations of movement,” _IEEE transactions on biomedical engineering_ , vol. 54, no. 11, pp. 1940–1950, 2007. 

- [34] M. Baumgartner, D. Müller, A. Serifi, R. Grandia, E. Knoop, M. Gross, and M. Bächer, “Coco-inekf: State estimation with learned contact covariances in dynamic, contact-rich scenarios,” _arXiv preprint arXiv:2605.15122_ , 2026. 

- [35] R. Featherstone, _Rigid body dynamics algorithms_ . Springer, 2008. [36] J. A. E. Andersson, J. Gillis, G. Horn, J. B. Rawlings, and M. Diehl, “CasADi – A software framework for nonlinear optimization and optimal control,” _Mathematical Programming Computation_ , vol. 11, no. 1, pp. 1–36, 2019. 

- [37] J. Carpentier, G. Saurel, G. Buondonno, J. Mirabel, F. Lamiraux, O. Stasse, and N. Mansard, “The pinocchio c++ library – a fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives,” in _IEEE International Symposium on System Integrations (SII)_ , 2019. 

- [38] K. Zakka, Q. Liao, B. Yi, L. L. Lay, K. Sreenath, and P. Abbeel, “mjlab: A lightweight framework for gpu-accelerated robot learning,” _arXiv preprint arXiv:2601.22074_ , 2026. 

