---
title: "SPARK: Skeleton-Parameter Aligned Retargeting on Humanoid Robots with Kinodynamic Trajectory Optimization"
date: "2026-03-12"
authors: "Hanwen Wang; Qiayuan Liao; Bike Zhang; Kunzhao Ren; Koushil Sreenath; Xiaobin Xiong"
url: https://arxiv.org/abs/2603.11480
pdf: https://arxiv.org/pdf/2603.11480
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.11480)** / [論文ページ](https://arxiv.org/abs/2603.11480)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SPARK: Skeleton-Parameter Aligned Retargeting on Humanoid Robots with Kinodynamic Trajectory Optimization** 

Hanwen Wang<sup>1</sup> , Qiayuan Liao<sup>2</sup> , Bike Zhang<sup>2</sup> , Kunzhao Ren<sup>1</sup> , Koushil Sreenath<sup>2</sup> , Xiaobin Xiong<sup>1</sup><sup>_,_3</sup> 

**_Abstract_ — Human motion provides rich priors for training general-purpose humanoid control policies, but raw demonstrations are often incompatible with a robot’s kinematics and dynamics, limiting their direct use. We present a two-stage pipeline for generating natural and dynamically feasible motion references from task-space human data. First, we convert human motion into a unified robot description format (URDF)based skeleton representation and calibrate it to the target humanoid’s dimensions. By aligning the underlying skeleton structure rather than heuristically modifying task-space targets, this step significantly reduces inverse kinematics error and tuning effort. Second, we refine the retargeted trajectories through progressive kinodynamic trajectory optimization (TO), solved in three stages: kinematic TO, inverse dynamics, and full kinodynamic TO, each warm-started from the previous solution. The final result yields dynamically consistent state trajectories and joint torque profiles, providing high-quality references for learning-based controllers. Together, skeleton calibration and kinodynamic TO enable the generation of natural, physically consistent motion references across diverse humanoid platforms.** 

## I. INTRODUCTION 

Humanoid robots promise to operate in human-centered environments, performing tasks that require rich wholebody coordination, dexterous contact interaction, and agile locomotion. Human motion datasets [1] provide a rich source of coordinated behaviors that can serve as motion priors for training humanoid control policies. Recent retargeting methods [2], [3] have shown that human demonstrations can be converted into natural-looking humanoid motions by mapping human keyframes to robot inverse kinematics (IK) targets, which can then be robustly tracked by controllers trained with reinforcement learning (RL) [4], [5], [6]. However, most existing retargeting tools model humanrobot morphology mismatch using root-link-centered taskspace scalings and per-keyframe local offsets [3] that ignore skeletal structure, often requiring substantial IK objective tuning. Moreover, most retargeting pipelines are purely kinematic [2], [3], [7], producing dynamically infeasible references that entangle motion tracking with dynamics feasibility recovery in RL. 

To address these challenges, we propose a two-stage pipeline that improves both kinematic and dynamic fidelity. First, instead of root-to-keyframe scaling and keyframe local 

> 1Hanwen Wang and Kunzhao Ren are with the University of Wisconsin-Madison.<sup>2</sup> Qiayuan Liao, Bike Zhang, and Koushil Sreenath are with the University of California, Berkeley. 3Xiaobin Xiong was with the University of Wisconsin-Madison, and now with the Shanghai Innovation Institute (SII). Corresponding to Koushil Sreenath: koushils@berkeley.edu. Corresponding to Xiaobin Xiong: xiaobin.xiong@sii.edu.cn. 


Fig. 1: Experimental results of highly dynamic side flip tracking on Unitree G1. 

offsets, we generate a human skeletal URDF from task-space motion and calibrate it to the target robot dimensions. Unlike prior human skeleton calibration strategies [2] which are often limited to SMPL [8], our URDF calibration applies to any human motion format with an implicit skeleton, improving IK quality while reducing tuning efforts. 

Second, we formulate a kinodynamic TO problem to recover dynamically feasible motion references from the calibrated kinematic sequence. Rather than solving this highly nonlinear and nonconvex kinodynamic TO problem [9] in one shot, we tackle it progressively in three stages: kinematic TO, inverse dynamics, and full kinodynamic TO. Each stage uses the optimal solution of the previous stage as an initial guess, gradually introducing kinematic and dynamic consistency. The resulting trajectories provide not only dynamically valid state trajectories but also corresponding torque profiles, which serve as strong supervision for downstream RL-based tracking policies. This is especially beneficial when training highly dynamic motions like the side flip in Fig. 1. 

Our approach bridges human demonstration, model-based TO, and learning-based control. By disentangling kinematic alignment, dynamic feasibility recovery, and robust control policy learning, we improve both motion quality and training efficiency. In summary, our main contributions are as follows. 

- A general algorithm that generates and calibrates a human URDF from task-space motion, enabling physically interpretable human-to-robot geometric alignment and improved IK retargeting quality. 

- A progressive kinodynamic TO framework that gradually refines retargeted motions into kinematically and dynamically feasible humanoid trajectories. 

- An integrated pipeline that produces high-quality motion and torque references for RL training, bridging 

kinematic retargeting, dynamics enforcement through TO, and motion tracking controller training through RL. 

## II. RELATED WORK 

## _A. Human Motion Retargeting_ 

Retargeting human motions to humanoid robots is essential for leveraging human motion datasets in robot learning and control. A central challenge arises from the morphological differences between humans and robots, including discrepancies in link lengths and kinematic structures. 

One line of work addresses this issue through simplified task space modifications that are incompatible with the underlying skeleton structure. GMR [3], for example, applies root-to-keyframe scalings and per-keyframe local offsets to human motion before using it as IK targets. While effective within a limited range of configurations, the correction is inherently local: a taller and wider shoulder and a shorter arm should be corrected by lengthening spine and shoulder links and shortening arm links. With root-to-arm scaling, however, the optimal scaling factor depends on joint configurations, making it hard to calibrate. GMR mitigates this issue by adding keyframe orientation tracking when the position references are off, which introduces nontrivial human-to-robot orientation offset calibration and additional IK tuning. 

An alternative strategy is to calibrate the underlying human skeletal model to better match the robot dimensions. PHC [2] optimizes the shape parameters of the human model SMPL to align it with the dimensions of the robot, thus producing task-space references that are more consistent with the target robot. However, the SMPL [8] shape parameters are derived from principal component analysis (PCA) on the shapes of human bodies. Although they are well-suited for representing realistic human body variations, calibrating them to robot dimensions, which are often outside the human distribution, can introduce undesirable artifacts, such as asymmetric limb proportions, spine distortions, or inconsistent foot geometry. 

In contrast, our method directly calibrates the human URDF generated from task space human motion, which are not only more physically interpretable and accurate but also more generalizable to diverse human motion formats with an implicit skeleton structure other than SMPL. 

## _B. Model-Based Trajectory Optimization for Humanoids_ 

Model-based trajectory optimization (TO) serves as a cornerstone for generating dynamically feasible motions in highdimensional humanoid systems. These methods formulate motion generation as a constrained optimization problem, enforcing physically grounded dynamics constraints ranging from simplified centroidal dynamics [10] to full order Lagrangain dynamics [9]. With careful engineering, such optimization problems can be used to control humanoid robots in real time using solving methods such as Differential Dynamic Programming [11], [12] and Sequential Quadratic Programming [9], [13]. 

Despite their success, classical model-based TO pipelines typically rely on carefully hand-crafted reference trajectories. These references include but are not limited to predefined 

base link pose and velocity trajectories [9] and foot swing trajectories and contact schedules [12]. Designing such references is non-trivial in that it requires substantial domain expertise, manual tuning for each robot morphology, and often task-specific adjustments. Moreover, because these references are hard coded rather than optimized, the resulting motions may appear overly regularized or conservative, lacking the variability, expressiveness, and subtle coordination patterns observed in natural human movements. As a result, even when dynamically feasible, the generated behaviors can be perceptually unnatural. 

In contrast, our work starts from natural human motion references and refines them through model-based kinodynamic TO. We treat human demonstrations as rich priors and use TO to enforce robot-specific dynamics, contact feasibility, and actuation limits. This shifts the role of trajectory optimization from motion design to motion refinement, enabling dynamically consistent humanoid behaviors that retain the structure and naturalness of human movement while satisfying the physical constraints. 

## _C. Reinforcement Learning for Robust Motion Tracking_ 

Reinforcement learning (RL) has become a dominant paradigm for humanoid control due to its ability to learn feedback policies that are robust to modeling errors, disturbances, and contact uncertainties. However, RL-based control faces two persistent challenges: policies trained purely from task rewards may converge to unnatural motions, and training high-dimensional humanoid policies typically requires large amounts of data and computation [4]. 

To improve training efficiency and motion quality, prior works commonly adopt one of the following two strategies. A first approach uses model-based TO to synthesize dynamically feasible reference trajectories, and subsequently trains RL policies to track them [14], [15]. Although this reduces exploration difficulty and accelerates convergence, the reference motions remain shaped by handcrafted objectives, contact schedules, and heuristic design choices, inheriting the same naturalness limitations as pure TO methods. A second approach directly feeds kinematically retargeted human motions into RL as tracking references [16], [17], [18]. This significantly enhances motion naturalness by leveraging human demonstrations, but because kinematic retargeting does not enforce dynamics constraints, the RL policy must implicitly correct dynamics infeasibility. Consequently, motion correction and policy learning become entangled, increasing the difficulty of training. 

In contrast, our approach bridges these paradigms. We first retarget natural human motion to the robot kinematics and then refine it through kinodynamic TO to enforce dynamics consistency. The optimized motions are subsequently used as references for RL training. This preserves the structural naturalness of human demonstrations while ensuring physical plausibility prior to policy learning. Moreover, our kinodynamic TO provides joint torque references that are unavailable in purely kinematic retargeting pipelines, offering richer supervision and further reducing learning complexity. 


Fig. 2: Retargeting framework. 

## III. INVERSE KINEMATICS WITH URDF CALIBRATION 

Fig. 2 provides an overview of our Skeleton-Parameter Aligned Retargeting framework with Kinodynamic trajectory optimization (SPARK), which consists of an upstream inverse-kinematics (IK) stage and a downstream trajectoryoptimization (TO) stage. In the IK stage, we convert task space human motion into a human URDF and a human generalized coordinate trajectory (Sec. III-A). We then calibrate the human URDF to the target robot dimensions (Sec. III-B), and replay the generalized coordinates on the calibrated URDF to generate task space references for IK (Sec. III-C), producing a robot motion reference in robot generalized coordinates. In the TO stage, we refine this trajectory by removing kinematic artifacts via kinematic TO (KTO; Sec. IV-B) and dynamic artifacts via inverse dynamics (ID; Sec. IV-C) and kinodynamic TO (KDTO; Sec. IV-D). 

## _A. Human URDF and Generalized Coordinates Generation_ 

**Human URDF Generation** : Human skeletons and humanoid robots typically differ in both the number of links and their dimensions. To enable reliable retargeting, we first convert a human skeleton motion sequence into a human URDF and a generalized-coordinate trajectory, and then calibrate the human URDF to match the target robot dimensions. Replaying the generalized coordinates on the calibrated URDF yields high-quality task-space references (Sec. III-C) that are consistent with the robot morphology. 

The conversion workflow is illustrated in Fig. 3. A human skeleton motion sequence provides the pose of each bone frame _Bi_ ( _i ∈{_ 1 _, . . . , N_ frame _}_ ) with respect to the world frame _W_ . In the URDF, we create one link _Li_ per bone _Bi_ and construct the model from a rest pose specified by the motion file. The rest pose is typically a standing configuration with vertical legs and an upright torso; arm configurations may vary but should remain left–right symmetric. If a suitable rest pose is missing, we define one prior to URDF construction. 

The coordinate-frame-related notations in this paper are as follows: For any three frames _A, B, C_ ,<sup>_C_</sup> **p** _AB_ denotes the position vector from the origin of frame _A_ to the origin of frame _B_ , expressed in frame _C_ . **R** _AB_ denotes the rotation matrix that takes in a vector **v** expressed in _B_ and returns 


Fig. 3: Coordinate frame definitions of human skeleton and the corresponding human URDF in rest pose. While the human bone frames _Bi_ are often aligned to the specific bones, we align the URDF link frames _Li_ to a user-defined aligned frame _A_ with the same orientation as the robot URDF root link to facilitate URDF calibration. 

the same vector expressed in _A_ , i.e.<sup>_A_</sup> **v** = **R** _AB_<sup>_B_</sup> **v** . It is also the relative rotation of frame _B_ with respect to frame _A_ . **_ξ_** _AB_ denotes the quaternion corresponding to **R** _AB_ . 

In the rest pose _r_ , we set each link origin to match the corresponding bone origin, i.e., **p** _WLi_ [ _r_ ] = **p** _WBi_ [ _r_ ]. We then rotate each link frame to coincide with the orientation of a user-defined aligned frame _A_ , which has the same orientation as the robot URDF root link to facilitate the URDF calibration in Sec. III-B. This alignment simplifies both URDF generation and calibration: the local restpose relative translations<sup>_Li_</sup> **p** _LiLj_ [ _r_ ] become identical to the global relative translations expressed in _A_ , i.e.,<sup>_Li_</sup> **p** _LiLj_ [ _r_ ] = _A_ **p** _LiLj_ [ _r_ ]. Consequently, constructing the URDF reduces to computing these relative translations from the world-frame rest-pose bone positions<sup>_W_</sup> **p** _WBi_ [ _r_ ] using 


**Human Generalized Coordinate Generation** : We define the generalized coordinates of the human URDF at timestep _k_ as **q** human[ _k_ ] = � _W_ **p** _WL_ 1[ _k_ ]; **_ξ_** _WL_ 1[ _k_ ]; **_ϕ_** 1[ _k_ ]; _. . ._ ; **_ϕ_** _Nj_ [ _k_ ]�, where<sup>_W_</sup> **p** _WL_ 1 is the root-link position, **_ξ_** _WL_ 1 is the root-link quaternion, and **_ϕ_** _n_ ( _n ∈{_ 1 _, . . . , Nj}_ ) are the Euler angles of the _n_ -th spherical joint. These quantities are computed as 


where _s_ root is the root position scaling factor to be calibrated in Sec. III-B, quat( _·_ ) converts rotation matrix to quaternion, and euler( _·_ ) converts rotation matrix to euler angles. **R** _BiLi_ 


Fig. 4: Rest pose key frame calibration of human URDF to humanoid robot dimensions. We match the link lengths for arms regardless of their absolute positions, and the absolute positions for the remaining key frames. We also calibrate the orientation offsets for end effectors if the robot has enough degree of freedom to track end effector orientations. 

is the relative rotation of the _i_ -th link frame with respect to the corresponding bone frame, which can be computed under rest pose as 


## _B. Human URDF Calibration_ 

We calibrate the human URDF to the target humanoid dimensions by matching keyframes in the respective rest poses. Fig. 4 shows an example of the rest pose configurations and key frame definitions when calibrating human URDF to Unitree G1. The robot rest pose (typically the neutral configuration with zero joint angles) should be a standing pose compatible with the human-URDF rest pose convention. The arm configuration may differ, since we only calibrate arm lengths. We decompose calibration into five groups: **End Effector Calibration** : We calibrate the local position and orientation offsets of end effectors such as wrists and ankles from the human URDF to the robot URDF so that their absolute poses can be tracked. If the robot wrist has fewer than three rotational degrees of freedom, its orientation cannot be tracked exactly; in this case, we omit the wristorientation calibration. In our IK formulation, end effectors are the only frames with orientation targets, since orientation offsets for intermediate links are generally ambiguous. **Arm Calibration** : We select three keyframes on each arm (shoulder, elbow, and wrist) and calibrate the shoulder–elbow and elbow–wrist link lengths. Because human and robot rest poses can differ substantially in arm configuration, we do not calibrate the full 3D relative translations. Instead, we estimate a scalar length scaling factor _s_ length for each segment through the following 


where _∥_ **p** robot _∥_ 2 is the arm length of the robot and _∥_ **p** human _∥_ 2 is the arm length of the human. 

**Leg Calibration** : We choose three keyframes on each leg (hip, knee, and ankle) and calibrate the absolute hip–knee 

and knee–ankle translations in the human URDF to match the robot URDF. 

**Main Body Calibration** : We select five keyframes on the main body (one waist frame, two shoulder frames, and two hip frames). Because the torso contains additional intermediate links, we correct their dimensions using an affine transformation. In the Unitree G1 example shown in Fig. 4, where the robot URDF root frame and all human URDF frames have their x axes pointing forward and z axes pointing upward in the rest pose, this affine transformation includes an _xz_ shear and independent scalings along _y_ and _z_ . The orientation synchronization was done by the aligned frame _A_ introduced in Sec. III-A. To calibrate the rest pose transformations of all links between _Li_ and _Lj_ in the human URDF, we find their corresponding links _Ri, Rj_ in the robot URDF, and calibrate the affine transformation **A** using 


where _kx_ is the xz shear factor and _sy, sz_ are the scaling factors along the y and z directions. We then apply the calibrated transform to any intermediate link relative translation **p** _LmLn_ , where _Lm_ and _Ln_ are links between _Li_ and _Lj_ , using 


Setting _Li_ to the waist frame and _Lj_ to a shoulder frame calibrates all links between waist and shoulders. Likewise, setting _Li_ to the waist frame and _Lj_ to a hip frame calibrates links between waist and hips. 

**Root Position Scale Calibration** : After calibrating leg and main body dimensions, we need to calibrate the root position scaling factor _s_ root in (2a) so that stance legs are still sticking on ground after leg dimensions have changed. The calibration can be done using 


where **p**<sup>corrected</sup> _L_ root _L_ ankle<sup>and</sup><sup>**p**</sup><sup>_L_</sup> root<sup>_L_</sup> ankle<sup>are the corrected and original</sup> root-to-ankle vector respectively. 

## _C. Inverse Kinematics (IK)_ 

After URDF calibration (Sec. III-B), we replay the human generalized-coordinate trajectory in (2) on the calibrated human URDF to obtain task-space references for all keyframes. Because calibration aligns the reference geometry with the target robot morphology, these task-space references can be tracked reliably. We solve IK for the generalized coordiantes **q** of the humanoid robot at each timestep via 


where _∥_ **e** _∥_<sup>2</sup> **W**<sup>:=</sup><sup>**e**</sup><sup>_T_</sup><sup>**We**denotesa</sup><sup>**W**-weightedsquared</sup> _ℓ_ 2 norm. The objective minimizes position errors _δ_ **p** over all _N_ frame keyframes and orientation errors _δ_ **R** only over the _N_ EE end effectors. We omit orientation targets for intermediate links, since their orientations are determined by the connected keyframe positions. This avoids calibrating ambiguous intermediate-link orientation offsets. If a robot wrist has fewer than three rotational degrees of freedom, we also drop wrist-orientation tracking. Finally, we enforce joint position and velocity limits and regularize towards the previous solution **q** prev to reduce jitter near singularities. 

_δ_ **v** _i, δ_ **_ω_** _i_ for all _N_ frame keyframes used in IK, with targets computed from the IK solution **q**<sup>_∗_</sup> IK<sup>and</sup><sup>**v**</sup> IK<sup>_∗_.Theregular-</sup> ization term _l_ reg<sup>KTO</sup> penalizes generalized accelerations **a** to smooth the trajectory. 


## IV. PROGRESSIVE KINODYNAMIC TO 

## _A. General TO Formulation_ 

Given the IK retargeting result **q**<sup>_∗_</sup> IK<sup>andthecontactlabels</sup> from the human motion, we further apply kinodynamic trajectory optimization (KDTO) to obtain humanoid motions that are feasible both kinematically and dynamically. Directly solving KDTO is difficult due to the problem’s high dimensionality and nonlinearity, so we adopt a progressive pipeline with three stages: (i) kinematic TO (KTO; Sec. IVB) to correct contact kinematics and self-collisions, (ii) pertimestep inverse dynamics (ID; Sec. IV-C) to produce a good initialization for second-order dynamic quantities, and (iii) a final KDTO stage (Sec. IV-D) that jointly optimizes kinematics and dynamics. Both KTO and KDTO can be written in the following general form: 


The exact definitions of the decision variables, costs and constraints differ between KTO (Sec. IV-B) and KDTO (Sec. IV-D), and are defined in the corresponding subsections. In general, the decision variables are the system states **x** and inputs **u** . The objective consists of a motiontracking term _l_ track( **x** [0 : _N_ ]) and a smoothing regularizer _l_ reg( **x** [0 : _N_ ] _,_ **u** [0 : _N −_ 1]). The constraints include the system dynamics (9a), general inequality constraints (9b), and box constraints (9c) on states and inputs. Constraints involving time index _k_ +1 apply for all _k ∈{_ 0 _, . . . , N −_ 1 _}_ ; all others apply for _k ∈{_ 0 _, . . . , N }_ . 

## _B. Kinematic TO (KTO)_ 

**Decision Variables** : For KTO, the system state is **x** = [ **q** ; **v** ], comprising the robot generalized coordinates **q** and generalized velocities **v** , and the system input is the generalized acceleration **u** = **a** . We initialize KTO using the IK solution: **q** guess = **q**<sup>_∗_</sup> IK<sup>.Wethenobtain</sup><sup>**v**guessand</sup><sup>**a**guessviafinite</sup> differences. **Cost Function** : The KTO tracking cost _l_ track<sup>KTOpenalizestask-</sup> space pose errors _δ_ **p** _i, δ_ **R** _i_ and task-space velocity errors 

**Double-Integrator Dynamics Constraint** : The KTO dynamics use a semi-implicit double integrator that maps generalized accelerations **a** to states ( **q** _,_ **v** ): 


where _⊕_ denotes the additive group operation (to handle configuration manifolds). 

**Kinematic Contact Constraints** : A key role of KTO is to enforce consistent contact kinematics. We impose three sets of constraints: 


The swing-foot-above-ground constraint (12a) enforces a nonnegative swing-foot height _p_ swing _,z_ . The first-contact-onground constraint (12b) sets the contact-foot height to zero at the first contact timestep and approximately aligns the foot with the ground by constraining _R_ first contact _,zz_ = 1 _−ϵ_ , where _ϵ_ is a small slack to avoid numerical infeasibility (we use _ϵ_ = 10<sup>_−_4</sup> ). Finally, the holonomic contact constraint (12c) enforces zero linear and angular velocities **v** contact _,_ **_ω_** contact at the contact foot. Together, these constraints keep the swing foot above the ground and establish holonomic surface contact for the stance foot. 

**Self Collision Avoidance Constraint** : We formulate selfcollision avoidance constraints on a point-to-point basis. At any timestep _k_ , for each collision pair ( **p** _i,_ **p** _j_ ) _∈C_ (with _i, j_ denoting collision-point indices), we enforce that the distance between **p** _i_ and **p** _j_ exceeds a minimum separation _d_ ( _i,j_ ) _,_ min: 


This formulation extends naturally to sphere-to-sphere constraints by increasing _d_ ( _i,j_ ) _,_ min by the sum of radii. **Joint Position and Velocity Limits** : The KTO box constraints include joint-position limits and joint-velocity limits: 


## _C. Inverse Dynamics (ID)_ 

At each timestep, we fix the generalized coordinates and velocities to the KTO optimum ( **q**<sup>_∗_</sup> KTO<sup>_,_</sup><sup>**v**</sup> KTO<sup>_∗_)andsolve</sup> inverse dynamics (ID) as a single-timestep quadratic program (QP). 

**Decision Variable** : ID optimizes the generalized acceleration **a** , joint torques **_τ_** _j_ , and contact wrenches **w** . The KTOoptimal acceleration **a**<sup>_∗_</sup> KTO<sup>servesasboththetrackingref-</sup> erence and the initialization for **a** . 

**Cost Function** : The ID objective tracks the KTO-optimal acceleration **a**<sup>_∗_</sup> KTO<sup>whileminimizingjointtorques</sup><sup>**_τ_**</sup><sup>_j_and</sup> contact wrenches **w** : 


**Lagrangian Dynamics Constraint** : The ID dynamics constraint uses the full-order Lagrangian rigid body dynamics of a floating-base system: 


and initialize accelerations, torques, and contact wrenches with ID: **a** guess = **a**<sup>_∗_</sup> ID<sup>,</sup><sup>**_τ_**</sup><sup>_j,_guess=</sup><sup>**_τ_**</sup> _j,_<sup>_∗_</sup> ID<sup>,and</sup><sup>**w**guess=</sup><sup>**w**</sup> ID<sup>_∗_.</sup> **Cost Function** : The KDTO costs share the same tracking term as KTO ( _l_ track<sup>KDTO</sup> = _l_ track<sup>KTO),witharegularizationterm</sup> 


The regularization term encourages generalized accelerations **a** , joint torques **_τ_** _j_ , and contact wrenches **w** to stay close to the ID solutions **a**<sup>_∗_</sup> ID<sup>,</sup><sup>**_τ_**</sup> _j,_<sup>_∗_</sup> ID<sup>,and</sup><sup>**w**</sup> ID<sup>_∗_.</sup> 

**Constraints** : The KDTO constraints combine the KTO constraints with the ID constraints. For dynamics, we enforce both the discrete-time double-integrator constraint (11) and the rigid-body dynamics constraint (16) at each timestep. For contact, we include the kinematic contact constraints (12), the zero-wrench constraint for swing foot, and the CWC constraint (17) for stance foot. Self-collision avoidance follows (13). Finally, we impose joint position and velocity limits (14) and joint-torque limits (20). 

## V. RESULTS AND ANALYSES 

**Contact Wrench Constraints** : When a foot is in swing phase, its contact wrench must vanish, i.e. **w** swing = **0** . When a foot is in contact phase, the 6D wrench of a foot **w** = [ _fx_ ; _fy_ ; _fz_ ; _τx_ ; _τy_ ; _τz_ ] satisfies the Contact Wrench Cone (CWC) constraint [19], which can be written as: 


where _X_ and _Y_ are the length and width of the foot supportbox, and _µ_ is the friction coefficient. 

**Contact Foot Zero Acceleration Constraint** : In (12), the contact-foot velocity is constrained to zero, which implies zero contact-foot acceleration. However, because ID treats generalized acceleration **a** as a decision variable and does not explicitly include (12), the resulting solution **a**<sup>_∗_</sup> ID<sup>may</sup> violate this zero-acceleration condition. We therefore enforce it explicitly as: 


**Torque Limits** : The ID is subjected to joint torque limits: 


## _D. Kinodynamic TO (KDTO)_ 

**Decision Variable** : The KDTO state is **x** = [ **q** ; **v** ; **a** ], which includes generalized coordinates, velocities, and accelerations, and the input is **u** = [ **_τ_** _j_ ; **w** ], which includes joint torques and contact wrenches. Since KDTO is highly nonlinear and nonconvex, we warm-start it using the KTO and ID solutions. Specifically, we initialize generalized coordinates and velocities with KTO: **q** guess = **q**<sup>_∗_</sup> KTO<sup>and</sup><sup>**v**guess=</sup><sup>**v**</sup> KTO<sup>_∗_,</sup> 

This section evaluates the key components of our pipeline through three sets of experiments. First, we quantify how URDF calibration improves IK retargeting accuracy on multiple humanoid platforms in Sec. V-A. Next, we study motion editing in Sec. V-B, using forward jumping as a case study, and compare KDTO against raw edits and KTO. Finally, we demonstrate the advantage of KDTO for highly dynamic motions such as the side flip shown in Fig. 1 in Sec. V-C, where recovering dynamic feasibility and optionally providing torque references accelerates the RL training process. 

## _A. Effect of URDF Calibration on IK_ 

As discussed in Sec. II-A, prior retargeting methods such as GMR [3] model human–robot morphology differences using task-space root-to-keyframe scalings and per-keyframe local offsets that are not consistent with the underlying skeletal structure. Calibrating these scaling and offset parameters is therefore intertwined with tuning the IK cost, which makes the approach difficult to generalize across large variations in source human body shape and motion. When applied to datasets with substantial diversity in human shapes and motions, such as AMASS [1], it can fail in corner cases such as Fig. 5, where the reference matches along one axis (width) but is incorrect along another (height). 

Our calibration of URDF resolves this issue by correcting the dimensions of the actual human skeleton. Once the target robot and the human-motion format are fixed, the same calibration logic can be applied to large datasets containing human skeletons of various dimensions. Because the calibrated task space targets are structurally consistent with the robot, we do not need to impose orientation tracking on intermediate links, and the IK position and orientation tracking weights can be set uniformly to one. This substantially reduces the IK tuning effort. We benchmark the IK mean per-body position error _E_ mpbpe on the AMASS ACCAD 


Fig. 5: IK Comparison between GMR (left) and URDF Calibration (right). 

TABLE I: IK _E_ mpbpe [cm] Comparison between GMR and Our URDF Calibration on AMASS ACCAD Dataset over Multiple Robots. 

|Retarget Method|G1|H1|T1|PM01|Kuavo 4Pro|
|---|---|---|---|---|---|
|GMR|9.37|12.53|6.59|9.51|19.50|
|URDF Calibration|**1.60**|**4.40**|**1.85**|**2.47**|**4.71**|


dataset [1] when retargeting to Unitree G1 [20], H1 [21], Booster T1 [22], EngineAI PM01 [23], and Kuavo 4Pro [24]. Table I shows that URDF calibration yields significantly lower _E_ mpbpe than GMR, with improvements of 82 _._ 9% on G1, 64 _._ 9% on H1, 71 _._ 9% on T1, 74 _._ 0% on PM01, and 75 _._ 8% on Kuavo 4Pro. 

## _B. Motion Editing_ 

Collecting human demonstrations is costly, so editing existing motions is an appealing way to synthesize additional training data and broaden hardware coverage. However, naive edits can introduce kinematic discontinuities and dynamic infeasibility, making the resulting references difficult to track. TO can mitigate these artifacts and improve reference quality. Here we use forward jumping as a case study. We apply two kinds of edits to it: (i) increasing the jump height shown in Fig. 6, (ii) connecting it with an initial and terminal standing phase for safe hardware deployment. Fig. 7 reports RL learning curves of the mean per-body position tracking error _E_ mpbpe when using references from the raw edit, KTO, and KDTO. We train motion-tracking policies following BeyondMimic [18] in IsaacLab [4] on Unitree G1 [20]. 

**Jump Higher** : Simply scaling the vertical position to obtain a higher jump is insufficient, because a larger apex height also requires a longer flight time under the same gravity. We therefore scale the foot _z_ -height by 4 _×_ and adjust the time discretization ∆ _t_ based on the resulting change in centerof-mass height. We measured that this height edit increases the maximum center-of-mass height by 1 _._ 4 _×_ , so we scale the time by _~~√~~_ 1 _._ 4. Instead of directly scaling ∆ _t_ , which degrades the accuracy of TO integration, we interpolate the reference to _~~√~~_ 1 _._ 4 times the original frequency while keeping ∆ _t_ unchanged. The right subfigure of Fig. 7 shows that 


Fig. 6: Unitree G1 performing a forward jump. The left case is the baseline, and the right one is edited to jump higher. 

Fig. 7: Comparison of RL _E_ mpbpe learning curves of jumping motion editing when the reference motions are provided by raw edit, KTO, and KDTO. 

KDTO achieves a substantially lower final tracking error than KTO and the raw edit. This highlights that when edits affect dynamics-relevant quantities such as gravitational acceleration, recovering a dynamically feasible trajectory with KDTO is important for high-quality tracking. 

**Connect Motions** : The jumping motions cannot be deployed directly on hardware because they start and end with nonzero velocities. A simple workaround is to repeat the first and last frames so that the reference is static at the beginning and end of the execution. This edit introduces velocity discontinuities at the transitions between standing and jumping, which TO can smooth out. We apply this edit to all hardware experiments. The left subfigure of Fig. 7 shows the learning curves for this edit applied to the baseline case where the jump segment itself remains unmodified. KTO improves the convergence speed, and the gap between KTO and KDTO is small. All three variants reach similar final tracking errors, suggesting that this edit introduces only minor dynamic artifacts in our setting. 

## _C. Highly Dynamic Motion Tracking_ 

The advantage of recovering dynamically feasible trajectories with KDTO is most pronounced for highly dynamic motions, such as the side flip motion shown in Fig. 1. Beyond producing a kinematically consistent trajectory, KDTO also yields joint torque references that can accelerate policy learning. In Fig. 8 we compare _E_ mpbpe learning curves for side-flip tracking under three reference variants. The KTO 


Fig. 8: Comparison of RL _E_ mpbpe learning curves of side flip tracking when the reference motions are provided by KTO, KDTO, KDTO+T. 

and KDTO runs use the standard BeyondMimic [18] reward, while KDTO+T adds an exponential joint torque tracking term _r_ **_τ_** _j_ tracking the optimal KDTO joint torques **_τ_** _j,_<sup>_∗_</sup> KDTO<sup>,</sup> which is defined as 


This term encourages joint torques **_τ_** _j_ to track KDTOoptimized torques **_τ_** _j,_ KDTO. Here, _τj,_ MSE is the mean-squared normalized torque error, with _./_ denoting element-wise division. _Nj_ is the number of joints and **_τ_** _j,_ max is the torque limit. As shown in Fig. 8, the KTO learning curve plateaus for roughly 500 iterations before converging, as training struggles near the most challenging flip timestep when the robot is inverted. In this regime, KTO must simultaneously learn to track the difficult motion while correcting dynamics infeasibility. By contrast, KDTO exhibits a much shorter plateau because the reference motion is already dynamically feasible, and KDTO+T converges even faster thanks to the additional guidance from the torque-tracking reward. 

## VI. CONCLUSION 

In this paper, we presented a pipeline for transferring task space human motion to humanoid robots with no per-motion tuning. We first introduced a URDF calibration procedure that aligns human skeletal dimensions with the target robot prior to reference generation, producing task-space targets that are kinematically consistent with the robot morphology. This structural alignment substantially reduces the need for manual IK weight adjustment and orientation-offset tuning. 

We then investigated the role of dynamics consistency in tracking edited and highly dynamic motions and demonstrated that KDTO recovers dynamically feasible trajectories and provides additional joint torque references, which improve both learning efficiency and tracking performance. 

## REFERENCES 

- [1] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “AMASS: Archive of motion capture as surface shapes,” in _International Conference on Computer Vision_ , Oct. 2019, pp. 5442– 5451. 

- [2] Z. Luo, J. Cao, K. Kitani, W. Xu _et al._ , “Perpetual humanoid control for real-time simulated avatars,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 10 895– 10 904. 

- [3] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” _arXiv preprint arXiv:2510.02252_ , 2025. 

- [4] M. Mittal, P. Roth, J. Tigue, A. Richard, O. Zhang, P. Du, A. SerranoMunoz, X. Yao, R. Zurbr¨ugg, N. Rudin _et al._ , “Isaac lab: A gpuaccelerated simulation framework for multi-modal robot learning,” _arXiv preprint arXiv:2511.04831_ , 2025. 

- [5] K. Zakka, B. Tabanpour, Q. Liao, M. Haiderbhai, S. Holt, J. Y. Luo, A. Allshire, E. Frey, K. Sreenath, L. A. Kahrs _et al._ , “Mujoco playground,” _arXiv preprint arXiv:2502.08844_ , 2025. 

- [6] K. Zakka, Q. Liao, B. Yi, L. L. Lay, K. Sreenath, and P. Abbeel, “mjlab: A lightweight framework for gpu-accelerated robot learning,” _arXiv preprint arXiv:2601.22074_ , 2026. 

- [7] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” _arXiv preprint arXiv:2509.26633_ , 2025. 

- [8] M. Loper, N. Mahmood, J. Romero, G. Pons-Moll, and M. J. Black, “Smpl: A skinned multi-person linear model,” in _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ , 2023, pp. 851–866. 

- [9] C. Khazoom, S. Hong, M. Chignoli, E. Stanger-Jones, and S. Kim, “Tailoring solution accuracy for fast whole-body model predictive control of legged robots,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 12, pp. 11 074–11 081, 2024. 

- [10] H. Dai, A. Valenzuela, and R. Tedrake, “Whole-body motion planning with centroidal dynamics and full kinematics,” in _2014 IEEE-RAS International Conference on Humanoid Robots_ . IEEE, 2014, pp. 295–302. 

- [11] D. Mayne, “A second-order gradient method for determining optimal trajectories of non-linear discrete-time systems,” _International Journal of Control_ , vol. 3, no. 1, pp. 85–95, 1966. 

- [12] F. Farshidian _et al._ , “OCS2: An open source library for optimal control of switched systems,” [Online]. Available: https://github.com/ leggedrobotics/ocs2. 

- [13] J. Nocedal and S. J. Wright, _Numerical optimization_ . Springer, 2006. [14] J. Wu, G. Xin, C. Qi, and Y. Xue, “Learning robust and agile legged locomotion using adversarial motion priors,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 8, pp. 4975–4982, 2023. 

- [15] F. Liu, Z. Gu, Y. Cai, Z. Zhou, H. Jung, J. Jang, S. Zhao, S. Ha, Y. Chen, D. Xu _et al._ , “Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid loco-manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [16] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [17] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [18] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [19] S. Caron, Q.-C. Pham, and Y. Nakamura, “Stability of surface contacts for humanoid robots: Closed-form formulae of the contact wrench cone for rectangular support areas,” in _2015 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2015, pp. 5107–5112. 

- [20] Unitree G1: https://www.unitree.com/g1. 

- [21] Unitree H1: https://www.unitree.com/h1. 

- [22] Booster T1: https://www.booster.tech/booster-t1. 

- [23] EngineAI PM01: https://en.engineai.com.cn/product-pm01.html. 

- [24] Kuavo 4Pro: https://www.lejurobot.cn/zh/application/kuavo-my. 

