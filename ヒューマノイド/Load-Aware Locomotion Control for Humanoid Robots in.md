---
title: "Load-Aware Locomotion Control for Humanoid Robots in Industrial Transportation Tasks"
date: "2026-03-15"
authors: "Lequn Fu; Yijun Zhong; Xiao Li; Yibin Liu; Zhiyuan Xu; Jian Tang"
url: https://arxiv.org/abs/2603.14308
pdf: https://arxiv.org/pdf/2603.14308
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.14308)** / [論文ページ](https://arxiv.org/abs/2603.14308)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

# Load-Aware Locomotion Control for Humanoid Robots in Industrial Transportation Tasks 

Lequn Fu, Yijun Zhong, Xiao Li, Yibin Liu, Zhiyuan Xu, Jian Tang, _Fellow, IEEE_ , and Shiqi Li 

**_Abstract_ —Humanoid robots deployed in industrial environments are required to perform load-carrying transportation tasks that tightly couple locomotion and manipulation. However, achieving stable and robust locomotion under varying payloads and upper-body motions is challenging due to dynamic coupling and partial observability. This paper presents a load-aware locomotion framework for industrial humanoids based on a decoupled yet coordinated loco-manipulation architecture. Lower-body locomotion is controlled via a reinforcement learning policy producing residual joint actions on kinematically derived nominal configurations. A kinematics-based locomotion reference with a height-conditioned joint-space offset guides learning, while a history-based state estimator infers base linear velocity and height and encodes residual load- and manipulation-induced disturbances in a compact latent representation. The framework is trained entirely in simulation and deployed on a full-size humanoid robot without finetuning. Simulation and real-world experiments demonstrate faster training, accurate height tracking, and stable locomanipulation. Project page: https://lequn-f.github.io/LALO/.** 

**_Index Terms_ —Humanoid Robots, Loco-manipulation, Reinforcement Learning, Load-carrying Locomotion, Industrial Transportation** 

## I. INTRODUCTION 

**H** UMANOIDin industrialrobotsenvironments,areenvironments,are increasinglywhere theyexpectedmusttoperformoperatemusttoperformoperateperformoperate 

in industrialrobotsenvironments,areenvironments,are where theyexpectedmusttoperformoperatemusttoperformoperateperformoperate load-carrying transportation tasks such as box handling, material transfer, and workstation-to-workstation delivery [1], [2]. Unlike locomotion-only scenarios, industrial box-handling tasks require tight coordination between locomotion and upper-body manipulation while maintaining balance and safety under varying payloads. During squatting, lifting, carrying, and walking motions, the payload mass, location, and distribution can change significantly, introducing strong dynamic coupling between the upper and lower body. These variations induce time-varying disturbances, shifts in the center of mass, and changes in ground reaction forces, posing substantial challenges to stable humanoid locomotion. 

Lequn Fu, Yijun Zhong, Xiao Li, and Yibin Liu are with the Huazhong University of Science and Technology, Wuhan 430074, China (email: fulq@hust.edu.cn; zhongyijun@hust.edu.cn; li <u>xiao@hust.edu.cn;</u> liu <u>yibin@hust.edu.cn).</u> 

Zhiyuan Xu, and Jian Tang are with the Beijing Humanoid Robot Innovation Center, Beijing 100086, China (e-mail: eric.xu@x-humanoid.com; jian.tang@x-humanoid.com). 

Shiqi Li is with the Huazhong University of Science and Technology, Wuhan 430074, China (e-mail: sqli@hust.edu.cn). 

From a control perspective, load-carrying locomotion has traditionally been addressed using model-based whole-body control and optimization-based frameworks [3]–[7]. By explicitly modeling payload effects as changes in mass distribution or external wrenches, such methods can, in principle, account for manipulation-induced dynamics [8], [9]. However, their performance is highly sensitive to modeling accuracy, contact estimation, and payload identification, and often requires careful tuning for specific task configurations. In realistic industrial settings, payload properties may be unknown, vary across tasks, or change during operation, making it difficult for purely model-based approaches to maintain robust performance. 

Recent advances in reinforcement learning (RL) have demonstrated strong potential for humanoid locomotion by directly optimizing feedback policies in high-dimensional state spaces [10]–[17]. Learning-based controllers are inherently more tolerant to modeling errors and contact uncertainties. 

Research on humanoid loco-manipulation has generally followed two primary paradigms. The first paradigm adopts a decoupled control strategy, where reinforcement learning is used to generate lower-body locomotion while upper-body motions are produced by kinematic or optimization-based controllers [18]–[21]. For example, Fu et al. [22] proposed a unified learning framework for legged manipulators but treated arm and leg control separately, which limited the consideration of manipulation-induced disturbances on locomotion stability. Murooka et al. [23] integrated imitation learning with tactile feedback for whole-body contact manipulation; however, locomotion remained model-based and retargeted, and the dynamic influence of arm motion on bipedal balance was not explicitly addressed. Xue et al. [24] presented a versatile whole-body controller supporting external upper-body interventions such as teleoperation, yet its decoupled formulation does not allow the lower-body policy to adapt online to payload variations induced by arm motion. More broadly, many decoupled approaches simplify payload effects by modeling the load as a static mass attached to the torso [25], overlooking a key characteristic of industrial box-handling tasks: payloads are carried by upper-body end-effectors and move relative to the base as the arms and torso articulate [26]. Moreover, base-height regulation in these methods is often realized through hard tracking or direct constraint enforcement, which lacks flexibility under varying payloads and may degrade contact smoothness during squatting and lifting. Although some recent works incorporate upper-body observations into locomotion policies [27], [28], they often lack precise feedback mechanisms for autonomous squatting and lifting height regulation, and frequently rely on 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

teleoperation rather than fully autonomous loco-manipulation. 

TABLE I 

OBSERVATION SPACE OF THE LOCOMOTION POLICY. 

The second paradigm directly trains whole-body motions using reinforcement learning, aiming to implicitly capture inter-limb coordination and contact-rich behaviors [29]–[35]. Zhang et al. [36] proposed the WoCoCo framework, which decomposes tasks into sequential contact stages and demonstrates impressive versatility across box loco-manipulation, dynamic dancing, and cliff climbing. However, the framework does not explicitly address payload variability or provide dedicated mechanisms for posture and height regulation under changing load conditions. Similarly, Dao et al. [37] demonstrated sim-to-real transfer of box loco-manipulation on the Digit humanoid by decomposing the task into multiple modular policies, but relied on predefined contact sequences and exhibited limited adaptability to unmodeled payload variations. Despite their expressiveness, existing whole-body RL approaches rarely model the dynamic interplay between upperbody payload motion and lower-body locomotion in an explicit or structured manner, which restricts robustness in realistic industrial scenarios. 

In contrast to existing approaches, this work addresses both dynamic upper–lower body coupling and partial observability within a unified locomotion framework. We propose a decoupled yet tightly coordinated locomotion–manipulation architecture, where reinforcement learning is applied exclusively to lower-body locomotion while upper-body box-handling motions are generated by a perception-driven kinematic controller and incorporated into the locomotion policy observations. The locomotion controller is further guided by a kinematics-based reference conditioned on commanded velocity and base height, providing structured motion priors that facilitate stable locomotion under varying payloads. To cope with partial observability, a history-based state estimator reconstructs base velocity and height while learning a compact latent representation of load- and manipulation-induced disturbances. The framework is trained entirely in simulation with domain randomization and deployed on a full-size humanoid robot without additional fine-tuning, demonstrating robust locomotion in real-world industrial box-handling tasks. 

The main contributions of this work are summarized as follows: 

- 1) A load-aware locomotion control framework for humanoid box-handling tasks that decouples lower-body locomotion learning from upper-body manipulation while maintaining dynamic coupling through observation design. 

- 2) A kinematics-based locomotion reference and heightconditioned joint-space offset that enable structured residual reinforcement learning, improving training efficiency, contact quality, and height regulation performance. 

- 3) A history-based state estimation scheme that explicitly infers base linear velocity and base height while learning a compact latent representation to capture load- and manipulation-induced disturbances under partial observability. 

|**Category**|**Dimension**|**Noise Scale**|
|---|---|---|
|Phase Input|2|0|
|Projected gravity|3|_±_0_._05|
|Angular velocity|3|_±_0_._1|
|Joint positions|27|_±_0_._02|
|Joint velocities|27|_±_0_._5|
|Command|4|0|
|Last actions|12|0|
|Estimated base velocity|3|0|
|Estimated base height|1|0|
|Latent feature|32|0|


## II. PROBLEM FORMULATION 

## _A. Industrial Box-Handling Task_ 

Humanoid robots operating in industrial logistics environments must perform continuous box-handling cycles, which may include approaching a palletized or non-palletized box, executing a depalletizing motion when required that involves coordinated squatting and reaching, transporting the grasped box under a varying payload, placing it at a designated area, and returning for the next item. These operations introduce substantial variations in upper-body posture and external loading conditions, requiring the robot to maintain dynamic stability throughout. 

The robot is modeled as a floating-base articulated system with generalized coordinates _q_ = [ _qb, q_ leg _, q_ arm] _∈_ R<sup>_n_</sup> , where _qb_ denotes the 6-DoF floating base, _q_ leg corresponds to the 12 lower-limb joints, and _q_ arm to the 14 upper-body joints. When a box is grasped, the payload becomes rigidly coupled to the torso, resulting in unknown variations in mass distribution and center-of-mass (CoM) location. The resulting dynamics are described by _M_ ( _q,_ ∆ _m_ )¨ _q_ + _h_ ( _q, q,_ ˙ ∆ _m_ ) = _S_<sup>_T_</sup> _τ_ + _Jc_<sup>_Tλ_,</sup> with ∆ _m_ denoting the unknown payload parameters. These load-induced disturbances strongly affect torso stabilization and feasible foot placement, especially during squatting and stepping. In the system architecture, only the 12 lower-limb joints are driven by the locomotion controller, whereas the 14 upper-body joints follow trajectories produced by an IKbased manipulation module using target poses _T_ box _∈ SE_ (3). The induced arm motions and payload shifts must therefore be compensated implicitly via proprioceptive and IMU feedback. 

## _B. Reinforcement Learning Formulation_ 

The locomotion controller is formulated as a rein= forcement learning problem defined by the tuple _M ⟨S, A, O, T, R, γ⟩_ . Due to sensing limitations and the presence of unknown payloads and manipulation-induced disturbances, the locomotion control problem is inherently partially observable. The agent therefore receives only a partial observation _ot_ = _ψ_ ( _st_ ), which contains proprioceptive measurements such as IMU orientation, angular velocity, joint positions and velocities and locomotion commands. Table I summarizes the observation space used by the locomotion policy. 

The control action _at ∈_ R<sup>12</sup> corresponds to the desired joint targets for the 12 lower-limb actuators. Because the transition dynamics depend on both the unmodeled payload ∆ _m_ and the 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

time-varying manipulation motions, the locomotion subsystem constitutes a Partially Observable Markov Decision Process (POMDP). The objective is to learn a policy _π_ ( _at | o≤t_ ) that maximizes the expected discounted return 


where the reward function is designed to encourage stable walking, robust balance during squatting and stepping, energy efficiency, and resilience to disturbances arising from box manipulation and payload shifts. 


## _A. Overview_ 

As illustrated in Fig. 1, we propose a load-aware locomotion framework for humanoid robots performing industrial transportation tasks such as box handling and load carrying. The system adopts a decoupled yet tightly coordinated locomotion– manipulation architecture, where lower-body locomotion is controlled by a reinforcement learning policy while upperbody manipulation is executed through perception-driven kinematic control. 

At each control step _t_ , the robot receives a high-level locomotion command 


where ( _vx_<sup>_∗, v_</sup> _y_<sup>_∗_) and</sup><sup>_ω_</sup> _z_<sup>_∗_denote the desired planar linear velocity</sup> and yaw rate, and _zb_<sup>_∗_specifiesthecommandedbaseheight.</sup> The locomotion policy outputs joint-space position targets for the lower-body joints, which are tracked by joint-level PD controllers. Upper-body motions are generated independently using real-time object pose estimation and inverse kinematics. 

Although the locomotion policy does not directly command arm joints, upper-body states are included in the policy observation, allowing the controller to react to manipulation-induced disturbances and payload-dependent dynamics. 

The framework consists of four main components: (i) a kinematics-based locomotion reference generator, (ii) a history-based state estimator for partial observability, (iii) a reinforcement learning locomotion policy with structured reward design, and (iv) an upper-body curriculum strategy that gradually increases dynamic coupling during training. 

## _B. Height-Conditioned Offset Control with Kinematic Reference_ 

To improve training stability, base height tracking accuracy, and contact smoothness, we adopt a height-conditioned offset control formulation augmented with a kinematics-based locomotion reference. In this design, the joint-space offset is determined solely by the commanded base height, while the kinematic reference trajectory is generated from both velocity and height commands and is used only as a training regularizer. 

Specifically, at each control step, the commanded base height _zb_<sup>_∗_ismappedtoanominallower-bodyjointconfig-</sup> uration through inverse kinematics. This configuration defines a height-conditioned joint offset 


which varies continuously with the height command and provides a physically consistent vertical posture for the robot. The offset does not encode stepping or gait patterns and is independent of velocity commands. 

On top of this offset, the locomotion policy outputs jointspace residual actions ∆ _qleg_ ( _t_ ), which are added to form the final joint position commands tracked by low-level PD controllers, 


This formulation allows the policy to focus on local corrections around a height-consistent nominal posture, rather than learning absolute joint targets across varying height conditions. 

In parallel, a kinematics-based locomotion reference trajectory is generated from the commanded planar velocity ( _vx_<sup>_∗, v_</sup> _y_<sup>_∗_),yawrate</sup><sup>_ω_</sup> _z_<sup>_∗_,andbaseheight</sup><sup>_z_</sup> _b_<sup>_∗_.Anormalizedgait</sup> phase is defined as 


where _Tc_ denotes the gait cycle duration and _φ_ 0 is a random phase offset. Based on the gait phase and velocity commands, foot-end trajectories are generated for each leg. During the swing phase, the vertical foot motion is parameterized by a smooth cubic polynomial over normalized swing time _τ ∈_ [0 _,_ 1], 


which satisfies zero position and velocity boundary conditions at lift-off and touch-down. The peak swing clearance is modulated by a task-dependent height parameter, ensuring smooth ground contact and reduced impact forces. During the stance phase, the foot height remains consistent with the commanded base height _zb_<sup>_∗_.</sup> 

The resulting reference joint trajectories _qleg_<sup>_ref_(</sup><sup>_t_),obtained</sup> via inverse kinematics from the foot-end trajectories, are _not_ tracked by the controller. Instead, they are incorporated only through auxiliary reward terms on joint motion and foot-end kinematics during training. At deployment, the controller relies solely on the height-conditioned offset and the learned residual policy. By separating height regulation (offset), locomotion structure (reference), and disturbance compensation (residual policy), this formulation improves convergence speed, enhances base height tracking under varying commands, and leads to smoother foot–ground contacts without restricting policy expressiveness. 

## _C. History-Based State Estimation_ 

Industrial transportation tasks exhibit partial observability due to unmodeled payload dynamics and manipulationinduced disturbances. Because such effects cannot be reliably inferred from single-step proprioceptive measurements, we introduce a history-based state estimator that leverages shortterm temporal context. 

At each control step, a fixed-length window of raw observations is stacked as 


IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 


Fig. 1. Overview of the proposed load-aware humanoid loco-manipulation framework. Upper-body manipulation is generated by perception-driven kinematic control using 6D object pose estimation, while lower-body locomotion is governed by a residual reinforcement learning policy with heightconditioned offsets and history-based state estimation. Historical proprioceptive observations are encoded by a history-based state estimator to infer base velocity, base height, and a compact latent state capturing load- and manipulation-induced disturbances. 

and processed by a lightweight neural encoder. The estimator predicts the base linear velocity ˆ _vb,t_ , the base height _z_ ˆ _b,t_ , and a compact latent representation _zt_ that captures residual dynamic variations caused by payload changes and upper-body motion. The latent feature _zt ∈_ R<sup>_D_</sup> is _ℓ_ 2-normalized to ensure bounded representations, 


The inferred states are incorporated into the policy observation as [ˆ _vb,t,_ ˆ _zb,t, zt_ ], enabling the locomotion controller to reason about unobserved dynamics under varying load conditions. 

During training, the estimator is supervised using privileged simulation information through regression losses on base linear velocity and base height, 


where _vb,t_ and _zb,t_ denote the ground-truth base linear velocity and base height, respectively. To encourage informative latent representations, we additionally employ a prototypebased swap prediction objective with Sinkhorn-normalized assignments. The overall estimator objective is 

### TABLE II 

REWARD TERMS AND WEIGHTS USED FOR TRAINING. 

|**Reward term**|**Formulation**|**Weight** (_µi_)|
|---|---|---|
|Linear velocity tracking|exp<br>�<br>_−_4_∥_[_vx, vy_]_−_[_v_<sup>_∗_</sup><br>_x_<sup>_, v∗_</sup><br>_y_<sup>]</sup><sup>_∥_2�</sup><br>|1_._2|
|Angular velocity tracking|exp<br>�<br>_−_4(_ωz −ω_<sup>_∗_</sup><br>_z_<sup>)2�</sup>|1_._1|
|Base height tracking|exp(_−_50_|hb,rel −h_<sup>_∗_</sup><br>_b,rel_<sup>_|_)</sup>|2_._0|
|Low-speed consistency|_r_ls(_vx, v_<sup>_∗_</sup><br>_x_<sup>)</sup><sup>_·_ I(</sup><sup>_|v∗_</sup><br>_x_<sup>_| >_ 0</sup><sup>_._1)</sup>|0_._2|
|Orientation stabilization|exp(_−_10_∥gproj,xy∥_)|1_._0|
|Velocity mismatch|0_._5(exp(_−_10_v_<sup>2</sup><br>_z_<sup>) + exp(</sup><sup>_−_5</sup><sup>_∥ω_</sup>_x,y_<sup>_∥_))</sup>|0_._5|
|Base acceleration|exp(_−∥_∆_v_root_∥_)|0_._2|
|Feet contact consistency|0_._5<sup>�</sup><br>_f∈{L,R}_<sup>(I[</sup><sup>_cf_ =</sup><sup>_sf_]</sup><sup>_−_0</sup><sup>_._5 I[</sup><sup>_cf̸_ =</sup><sup>_sf_])</sup><br>|1_._2|
|Joint imitation|exp(_−_2_∥qleg −q_<sup>_ref_</sup><br>_leg _<sup>_∥_)</sup><br>|1_._0|
|Foot height tracking|�<br>_f∈{L,R}_ <sup>I(</sup><sup>_href_</sup><br>_f_<br>_−hf <_0_._008)|1_._0|
|Foot slip|�<br>_f∈{L,R} _<sup>_∥_</sup><sup>**v**</sup><sup>_xy_</sup><br>_foot,f_<sup>_∥·_ I[</sup><sup>_Fz,f >_ 1]</sup>|_−_0_._25|
|Foot stumble|I(_∃f_ : _∥Fxy,f∥>_3_|Fz,f|_)|_−_1_._5|
|Contact force|�<br>_f∈{L,R}_<br>�<br>_∥Ff∥−F_max<br>�<br>+|_−_0_._005|
|Contact momentum|�<br>_f∈{L,R}_ <sup>min(</sup><sup>_vz,f,_ 0)</sup><sup>_·_ max(</sup><sup>_Fz,f −_50</sup><sup>_,_ 0)</sup>|_−_0_._005|
|Hip-joint deviation|exp(_−_50_δhip_)_−_0_._01_∥qleg −q_<sup>0</sup><br>_leg_<sup>_∥_</sup>|0_._5|
|Action smoothness|_∥at −at−_1_∥_<sup>2 </sup>+_∥at_+_at−_2_−_2_at−_1_∥_<sup>2</sup>|_−_0_._02|
|Torque penalty|_∥τ∥_<sup>2</sup>|_−_10<sup>_−_5</sup>|
|Joint velocity|_∥_˙_q∥_<sup>2</sup>|_−_10<sup>_−_4</sup>|
|Joint acceleration|_∥_( ˙_qt −_˙_qt−_1)_/_∆_t∥_<sup>2</sup>|_−_10<sup>_−_7</sup>|
|Velocity limit penalty|�<br>_j_<br>�<br>_|_˙_qj| −κv_ ˙_q_<sup>max</sup><br>_j_<br>�<br>+|_−_0_._1|
|Torque limit penalty|�<br>_j_<br>�<br>_|τj| −κτ τ_ <sup>max</sup><br>_j_<br>�<br>+|_−_0_._1|
|Position limit penalty|�<br>_j_<br>�<br>(_qj −q_<sup>max</sup><br>_j_<br>)++ (_q_<sup>min</sup><br>_j_<br>_−qj_)+<br>�|_−_2_._0|
|Stand-still|�<br>_j_<br>��_qj −q_stand<br>_j_<br>��+I<br>�<br>_|z −h_<sup>_cmd_</sup>_| <_0_._01<br>�|_−_3_._0|
|Collision penalty|�I[undesired contact]|_−_1|


During deployment, the estimator operates solely on onboard sensory inputs and serves as a preprocessing module for the locomotion policy. 

## _D. End-to-End Deep Reinforcement Learning_ 

The lower-body locomotion controller is trained in an endto-end manner. At each control step, the policy outputs jointspace action commands as position offsets with respect to a 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

nominal configuration. 

_1) Reward Design:_ The reward function is designed to balance command tracking accuracy, dynamic stability, contact quality, and motion regularity. At time step _t_ , the total reward is defined as 


where _ri_ denotes an individual reward term and _µi_ is its corresponding weight. we employ exponentially shaped rewards to emphasize small residual errors while maintaining smooth and well-conditioned gradients. The shaping coefficients are selected individually according to the sensitivity of each task. 

Table II summarizes all reward terms used for training. In the table, _vx_ and _vy_ denote the planar base linear velocities, _ωz_ denotes the yaw angular velocity, and ( _·_ )<sup>_∗_</sup> represents commanded values. The base height _hb,rel_ is measured relative to the supporting feet. Kinematics-based reference terms, including joint imitation and foot height tracking, are incorporated only during training as soft constraints to guide exploration and improve convergence, while remaining inactive during deployment. Contact-related penalties suppress excessive impact forces, foot slip, unstable contacts, and undesired collisions, thereby improving contact smoothness and robustness. Additional regularization terms on action variation, joint motion, and actuation effort are included to promote smooth and energy-efficient behaviors. 

_2) Upper-Body Curriculum:_ Although the locomotion policy directly controls only the lower-body joints, upper-body motions can significantly affect whole-body dynamics through inertial coupling, especially during load-carrying tasks. Injecting strong upper-body disturbances from the early training stage often leads to unstable learning and degraded convergence. To mitigate this issue, we adopt an upper-body curriculum strategy. 

During training, random upper-body joint motions are applied as external disturbances with bounded magnitude and smooth temporal interpolation. The disturbance intensity is governed by a scalar ratio _ρ ∈_ [0 _,_ 1], which is progressively increased as the policy achieves stable locomotion performance. This curriculum sampling scheme follows the strategy introduced in [27], allowing the policy to first acquire robust lower-body locomotion and then gradually adapt to stronger whole-body perturbations. During deployment, the curriculum randomization is disabled. 

_3) Domain Randomization:_ To reduce the sim-to-real gap, we apply domain randomization during training so that the locomotion policy is exposed to a broad range of uncertainties that commonly arise in real deployment. The randomized factors include variations in contact and environment properties, robot inertial parameters, actuation imperfections, and control timing. In addition, intermittent external pushes are applied to improve disturbance rejection. This combination encourages the policy to rely on robust feedback strategies rather than exploiting simulator-specific dynamics. Concretely, we randomize ground friction and restitution to cover diverse contact conditions. To model variations caused by loads and modeling errors, we perturb payload masses and apply centerof-mass (CoM) offsets, together with link-mass scaling. To 

### TABLE III 

OVERVIEW OF DOMAIN RANDOMIZATION 

|**Parameter**|**Unit**|**Range**|**Operator**|
|---|---|---|---|
|Ground Friction|–|[0.1, 3.0]|–|
|Restitution Coefficient|–|[0.0, 1]|–|
|External Push Velocity (XY)|m/s|[-0.5, 0.5]|additive|
|External Push Angular Velocity|rad/s|[0, 0.6]|additive|
|Base Mass Offset|kg|[-5.0, 10.0]|additive|
|Hand Mass Offset|kg|[-0.1, 0.3]|additive|
|Base CoM Offset|m|[-0.03, 0.03]|additive|
|Link Mass Scaling|–|[0.8, 1.0]|scaling|
|Joint Position Offset|rad|[-0.05, 0.05]|additive|
|Joint Friction|–|[0.01, 1.15]|–|
|Joint Armature|–|[0.008, 0.06]|–|
|PD Factors|–|[0.9, 1.1]|scaling|
|Torque Output Scaling|–|[0.8, 1.2]|scaling|
|Action Latency|ms|[10, 50]|–|
|Motor/IMU Observation Latency|ms|[10, 50]|–|


account for hardware inconsistencies, we randomize PD gains and inject additive actuation offsets and torque perturbations. Finally, we introduce stochastic action execution delay to emulate control-level latency. The domain randomization settings are summarized in Table III. 

## _E. Upper-Body Control and Deployment_ 

In real-world deployment, upper-body manipulation is executed independently of the locomotion policy through a perception-driven kinematic control pipeline. To handle scenarios with multiple identical boxes in the workspace, we integrate instance segmentation with a 6D pose estimation framework to enable multi-object detection and target selection. As shown in Fig. 2, a YOLO-based [38] segmentation network is first applied to the RGB image to obtain pixel-wise masks of all visible boxes. According to task requirements, a target box is selected from the segmented instances (e.g., the nearest box or the leftmost/rightmost instance). The corresponding bounding region in the RGB image is then cropped and fed into a FoundationPose-based [39] 6D pose estimator, which outputs the object pose relative to the camera frame. When object configurations change due to environmental interactions, the detection and pose estimates are updated in real time to maintain tracking consistency. Given the estimated 6D pose, a predefined grasp or pre-grasp pose is generated, and inverse kinematics is used to compute the corresponding arm joint trajectories. The resulting joint commands are executed by position-based controllers to accomplish grasping, lifting, and placement motions. 

This loop runs concurrently with the learned locomotion controller. By decoupling upper-body planning from lowerbody learning, the system ensures precise and predictable manipulation behavior, while the locomotion policy adapts online to manipulation-induced dynamic effects through its observation inputs, enabling stable load-carrying locomotion in industrial environments. 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 


Fig. 2. Multi-box detection and target 6D pose estimation. Blue boxes denote instances detected by YOLO-seg, the red box indicates the selected target, and the green wireframe shows the 6D pose estimated by FoundationPose. 

## IV. EXPERIMENTS 

## _A. System Overview and Implementation Details_ 

All simulation and real-world experiments are conducted on Tiangong 2.0 Pro, a full-size humanoid robot developed by the Beijing Humanoid Robot Innovation Center. The robot is 1 _._ 73 m tall, weighs 74 kg, and is fully electrically actuated with 42 degrees of freedom (DoFs), including legs, arms, waist, head, and dexterous hands. 

For locomotion and loco-manipulation experiments, a subset of 27 DoFs is activated, consisting of 6 DoFs per leg, 7 upper-body DoFs, and 1 waist DoF. Head joints are fixed, and the original hands are replaced with a custom endeffector designed for robust box handling. All active joints are controlled by position-based PD controllers at 500 Hz, while the reinforcement learning policy runs at 100 Hz. Upper-body manipulation is executed independently using a perception-driven kinematic controller. Object perception is provided by a head-mounted depth camera for box localization and pose estimation. All policies are trained in simulation using Proximal Policy Optimization (PPO) [40] with extensive domain randomization and are deployed on the real robot without additional fine-tuning. Training is performed in Isaac Gym with 4096 parallel environments on a single NVIDIA RTX 4090 GPU. The hyperparameters are listed in Table IV. 

TABLE IV 

PPO TRAINING HYPERPARAMETERS 

|Parameter Name|Value|
|---|---|
|Value loss coefficient|1.0|
|Number of Epochs|5|
|Clipping|0.2|
|Entropy Coefficient|0.003|
|Discount Factor|0.99|
|GAE Discount Factor|0.95|
|Desired KL-Divergence|0.01|
|Learning Rate|1e-3 (adaptive)|
|Actor hidden layers|[512, 256, 256]|
|Source Encoder hidden layers|[256, 256]|
|Target Encoder hidden layers|[256, 256]|
|Number of History Observation|6|


## _B. Effect of Kinematic Reference with Residual Control_ 

To evaluate the effectiveness of the proposed heightconditioned offset and kinematics-based locomotion reference, we conduct an ablation study comparing three locomotion 


Fig. 3. Training convergence comparison of different offset and reference formulations. (a) Episode reward for tracking base height versus environment steps. (b) Mean episode length versus environment steps. 

controllers. All methods share the same policy architecture, training procedure, and domain randomization settings, and differ only in the formulation of the joint offset and the use of kinematics-based reference trajectories. The reward structure is kept consistent across methods, while the weight of the baseheight tracking term is adjusted when necessary to ensure that each controller can successfully follow the commanded height, such that all methods are evaluated on the same task. For each method, policies are trained with three different random seeds. Evaluation is carried out in 2000 parallel environments, each running for 20 s under randomly sampled velocity and base height commands. Reported results are obtained by averaging across the three trained policies, with the standard deviation indicating performance variation. 

Specifically, we consider three methods. 

_a) Fixed Offset w/o Reference:_ serves as the baseline, where a fixed nominal joint configuration is used as the offset and no kinematics-based reference is provided, resulting in a purely learning-based controller with unstructured exploration. _b) Ours Fixed Offset:_ augments the baseline with kinematics-based reference trajectories generated from the commanded velocity and base height, which are incorporated only through auxiliary reward terms during training, while keeping the joint offset fixed. 

_c) Ours:_ further replaces the fixed offset with a heightconditioned joint-space offset computed via inverse kinematics from the commanded base height, on top of which the policy outputs residual joint actions; the same kinematics-based reference rewards are retained. 

As shown in Fig. 3, incorporating kinematics priors consistently improves training efficiency and stability compared to the purely learning-based baseline (Fixed Offset w/o Reference). In Fig. 3(a), the baseline converges slowly with large reward fluctuations, indicating unstructured exploration and difficulty in satisfying the base-height tracking objective. Intro- 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 


Fig. 4. Distribution of joint residual actions during steady-state walking. 

ducing kinematics-based reference rewards accelerates reward growth and reduces variance, demonstrating their effectiveness in guiding early-stage learning. Replacing the fixed nominal offset with a height-conditioned joint-space offset further improves training dynamics, leading to the fastest and most stable convergence. By providing a physically plausible nominal configuration, this formulation allows the policy to focus on learning residual joint corrections rather than discovering postures from scratch, thereby improving sample efficiency and robustness. A consistent trend is observed in Fig. 3(b). Both the reference-based and proposed methods achieve longer and more stable episode lengths than the baseline, indicating fewer premature terminations during training. The proposed method attains the longest and most consistent episodes, confirming that reference shaping and height-conditioned offsets provide complementary benefits for robust locomotion learning. 

Fig. 4 compares the action distributions of left-leg joints under different offset and reference formulations. The baseline controller exhibits wide and irregular action distributions across multiple joints, reflecting unstructured exploration and a strong reliance on policy outputs to compensate for posture and height variations. Introducing kinematics-based reference rewards slightly regularizes the action distributions, but the overall spread remains comparable, indicating that reference shaping alone does not fundamentally change the underlying action parameterization. 

In contrast, the proposed method produces more structured and joint-dependent action distributions. Notably, actions concentrate around joint-specific operating regions with reduced bias and improved symmetry across the kinematic chain. This behavior suggests that the height-conditioned inversekinematics offset absorbs most posture- and height-related variations, allowing the policy to focus on learning residual corrections rather than compensating for global configuration changes. As a result, the learned actions exhibit improved regularity and coordination, which is consistent with the observed gains in training stability, height tracking accuracy, and contact behavior. 


Fig. 5. Prediction performance of the history-based state estimator. Comparison between commanded, ground-truth, and estimated states for (a) base velocity _vx_ , (b) base velocity _vy_ , and (c) base height. The estimator achieves low mean squared error under dynamic motion conditions. 

## _C. History-Based State Estimation Analysis_ 

We evaluate the proposed history-based estimator in simulation, where ground-truth base states are available for quantitative comparison. The estimator predicts the base linear velocity and base height from a short horizon of proprioceptive observations, without direct access to privileged state information. 

Fig. 5 presents representative time-series results under dynamically varying velocity commands. The estimated velocities closely track the ground-truth signals in both magnitude and phase, with no observable drift or delayed convergence during command transitions. The mean squared errors are 2 _._ 15 _×_ 10<sup>_−_3</sup> for _vx_ and 8 _._ 86 _×_ 10<sup>_−_4</sup> for _vy_ , indicating accurate reconstruction of planar motion despite contact-induced disturbances. 

For base height estimation, the error remains on the order of 10<sup>_−_6</sup> , demonstrating near-perfect alignment with ground truth. Such high precision is particularly critical for heightconditioned locomotion, where small vertical deviations may significantly affect contact stability and squatting performance. 

Overall, the results confirm that the history-based estimator effectively compensates for partial observability and provides stable, low-variance state feedback for policy execution under dynamic payload conditions. 

## _D. Real-World Loco-Manipulation Experiments_ 

We evaluate the proposed framework on real-world industrial box transportation tasks that require tight coordination between locomotion and manipulation. The experiments are conducted in a one-to-one reconstructed factory environment that replicates an industrial logistics scenario used in the World Humanoid Robot Games. The robot is required to transport 5 kg boxes between designated locations, with and without 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 


Fig. 6. Real-world loco-manipulation experiments in an industrial box transportation scenario. (a–c) Box transportation without depalletizing: the robot transitions from unloaded walking to load-carrying locomotion, squats to a target height, places the box onto a rack while maintaining a crouched posture, and then stands up. (d–f) Transportation with depalletizing: the robot performs box depalletizing, walks while carrying a 5 kg payload, places the box at the designated location, and continues unloaded walking for the next task. The environment is a one-to-one reconstruction of an industrial factory setting and corresponds to the task scenario of the World Humanoid Robot Games. 

depalletizing, while maintaining stable locomotion under significant load variations and upper-body motion disturbances. 

Upper-body manipulation is generated independently using a vision-based pipeline that estimates the 6D pose of the box from a head-mounted depth camera, followed by inverse kinematics for arm control. The lower-body locomotion policy receives no direct manipulation commands and relies solely on proprioceptive feedback and estimated states to compensate for manipulation-induced disturbances. 

Fig. 6 illustrates two representative task sequences. In the first scenario (Fig. 6(a–c)), the robot performs a transportation task without depalletizing, transitioning from unloaded walking to load-carrying locomotion, squatting to a commanded height, placing the box onto a rack while maintaining a crouched posture, and then standing up. In the second scenario (Fig. 6(d–f)), the robot executes a full depalletizing pipeline, including box removal from a stacked pallet, load-carrying walking, object placement at a target location, and subsequent unloaded locomotion for the next task. 

All policies are trained entirely in simulation and deployed on the real robot without additional fine-tuning. Despite the decoupled control architecture, the robot consistently maintains stable walking, smooth foot ground contact, and accurate height regulation across different task phases. These results demonstrate that the proposed kinematics-based reference with height-conditioned residual control and history-based state estimation enables robust sim-to-real transfer for humanoid loco-manipulation in realistic industrial environments. 

## V. CONCLUSION AND DISCUSSION 

This paper presented a load-aware locomotion framework for humanoid robots performing industrial transportation tasks. By adopting a decoupled yet tightly coordinated locomotion– manipulation architecture, the approach combines learningbased lower-body locomotion with perception-driven kinematic manipulation, enabling stable walking under varying payloads and upper-body motions. A kinematics-based locomotion reference conditioned on commanded base height and foot-end trajectories is integrated with residual reinforcement learning control, which accelerates training convergence, improves ground contact behavior, and enhances height tracking compared to purely reward-driven policies. In addition, a history-based state estimator augments the policy with inferred base motion states and a compact latent representation, improving robustness to payload variations and manipulationinduced disturbances. 

The proposed framework is validated through simulation and real-robot experiments in industrial box-handling scenarios, where policies trained entirely in simulation are deployed without additional fine-tuning. Future work will investigate adaptive reference generation and tighter whole-body integration to further improve versatility in complex environments. 

## REFERENCES 

- [1] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu, A. Kheddar, X. B. Peng, Y. Zhu, G. Shi, Q. Nguyen, G. Cheng, H. Gao, and Y. Zhao, “Humanoid 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _arXiv preprint arXiv:2501.02116_ , DOI 10.48550/arXiv.2501.02116, 2025. 

- [2] Q. Sheng, Z. Zhou, J. Li, X. Mi, P. Xiang, Z. Chen, H. Xu, S. Jia, X. Wu, Y. Cui, S. Ye, J. Yu, Y. Du, S. Zhai, K. Xu, Y. Yang, Z. Lou, Z. Song, Z. Yin, Y. Sun, R. Xiong, J. Zou, and H. Yang, “A comprehensive review of humanoid robots,” _SmartBot_ , vol. 1, DOI 10.1002/smb2.12008, no. 1, p. e12008, 2025. 

- [3] A. Rigo, M. Hu, S. K. Gupta, and Q. Nguyen, “Hierarchical optimization-based control for whole-body loco-manipulation of heavy objects,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , DOI 10.1109/ICRA57147.2024.10611656, pp. 15 322– 15 328, 2024. 

- [4] H. Qi, Z. Yu, X. Chen, Q. Li, Y. Liu, C. Yi, C. Dong, F. Meng, and Q. Huang, “A 3-step optimization framework with hybrid models for a humanoid robot’s jump motion,” _IEEE Transactions on Automation Science and Engineering_ , 2025. 

- [5] Z. He, J. Wu, J. Zhang, S. Zhang, Y. Shi, H. Liu, L. Sun, Y. Su, and X. Leng, “Cdm-mpc: An integrated dynamic planning and control framework for bipedal robots jumping,” _IEEE Robotics and Automation Letters_ , vol. PP, DOI 10.1109/LRA.2024.3408487, 05 2024. 

- [6] K. Yamamoto, T. Kamioka, and T. Sugihara, “Survey on model-based biped motion control for humanoid robots,” _Advanced Robotics_ , vol. 34, DOI 10.1080/01691864.2020.1837670, no. 21-22, pp. 1353–1369, 2020. 

- [7] A. W. Winkler, C. D. Bellicoso, M. Hutter, and J. Buchli, “Gait and trajectory optimization for legged systems through phase-based end-effector parameterization,” _IEEE Robotics and Automation Letters_ , vol. 3, DOI 10.1109/LRA.2018.2798285, no. 3, pp. 1560–1567, 2018. 

- [8] M. Chignoli, D. Kim, E. Stanger-Jones, and S. Kim, “The mit humanoid robot: Design, motion planning, and control for acrobatic behaviors,” in _2020 IEEE-RAS 20th International Conference on Humanoid Robots (Humanoids)_ , DOI 10.1109/HUMANOIDS47582.2021.9555782, pp. 1– 8. Munich, Germany: IEEE, 2021. 

- [9] D. Calvert, L. Penco, D. Anderson, T. Bialek, A. Chatterjee, B. Mishra, G. Clark, S. Bertrand, and R. J. Griffin, “A behavior architecture for fast humanoid robot door traversals,” _Robotics Auton. Syst._ , vol. 195, DOI 10.1016/J.ROBOT.2025.105217, p. 105217, 2026. 

- [10] S. Gangapurwala, M. Geisert, R. Orsolino, M. Fallon, and I. Havoutis, “Rloc: Terrain-aware legged locomotion using reinforcement learning and optimal control,” _IEEE Transactions on Robotics_ , vol. 38, DOI 10.1109/TRO.2022.3172469, no. 5, pp. 2908–2927, 2022. 

- [11] Y. Kim, H. Oh, J. Lee, J. Choi, G. Ji, M. Jung, D. Youm, and J. Hwangbo, “Not only rewards but also constraints: Applications on legged robot locomotion,” _IEEE Transactions on Robotics_ , vol. 40, DOI 10.1109/TRO.2024.3400935, pp. 2984–3003, 2024. 

- [12] H. Zhang, C. Hua, J. Chen, X. Luo, and J. Wei, “Chaos-augmented reinforcement learning with diffusion models for robust legged robot locomotion,” _IEEE Transactions on Industrial Electronics_ , DOI 10.1109/TIE.2025.3603082, pp. 1–10, 2025. 

- [13] L. Bao, J. Humphreys, T. Peng, and C. Zhou, “Deep reinforcement learning for robotic bipedal locomotion: A brief survey,” _Artificial Intelligence Review_ , vol. 59, DOI 10.1007/s10462-025-11451-z, no. 1, p. 38, 2025. 

- [14] F. Jenelten, J. He, F. Farshidian, and M. Hutter, “Dtc: Deep tracking control,” _Science Robotics_ , vol. 9, DOI 10.1126/scirobotics.adh5401, no. 86, p. eadh5401, 2024. 

- [15] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _The International Journal of Robotics Research_ , vol. 44, DOI 10.1177/02783649241285161, no. 5, pp. 840–888, 2025. 

- [16] B. V. Marum, A. Shrestha, H. Duan, P. Dugar, J. Dao, and A. Fern, “Revisiting reward design and evaluation for robust humanoid standing and walking,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , DOI 10.1109/IROS58592.2024.10802680, pp. 11 256–11 263. Abu Dhabi, United Arab Emirates: IEEE, 2024. 

- [17] Y. Zhou, J. Qiu, S. Jia, F. Ni, and W. Zhang, “Curriculum-enhanced reinforcement learning for robust humanoid locomotion,” _IEEE Transactions on Automation Science and Engineering_ , 2026. 

- [18] S. Ji, Z. Chen, C. Zhang, J. Gao, and H. Qiao, “A unified reinforcement learning framework for payload-aware humanoid control with integrated inertial and state estimation,” _IEEE/ASME Transactions on Mechatronics_ , DOI 10.1109/TMECH.2025.3648874, pp. 1–11, 2026. 

- [19] G. Li, Q. Shi, Y. Hu, J. Hu, Z. Wang, X. Wang, and S. Luo, “Thor: Towards human-level whole-body reactions for intense contact-rich environments,” _arXiv preprint arXiv:2510.26280_ , DOI 10.48550/arXiv.2510.26280, 2025. 

- [20] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” in _Robotics: Science and Systems XX, Delft, The Netherlands, July 15-19, 2024_ , D. Kulic, G. Venture, K. E. Bekris, and E. Coronado, Eds., DOI 10.15607/RSS.2024.XX.107. Robotics: Science and Systems Foundation, 2024. 

- [21] C. Lu, X. Cheng, J. Li, S. Yang, M. Ji, C. Yuan, G. Yang, S. Yi, and X. Wang, “Mobile-television: Predictive motion priors for humanoid whole-body control,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 5364–5371. IEEE, 2025. 

- [22] Z. Fu, X. Cheng, and D. Pathak, “Deep whole-body control: Learning a unified policy for manipulation and locomotion,” in _Conference on Robot Learning, CoRL 2022, 14-18 December 2022, Auckland, New Zealand_ , ser. Proceedings of Machine Learning Research, K. Liu, D. Kulic, and J. Ichnowski, Eds., vol. 205, pp. 138–149. PMLR, 2022. 

- [23] M. Murooka, T. Hoshi, K. Fukumitsu, S. Masuda, M. Hamze, T. Sasaki, M. Morisawa, and E. Yoshida, “Tact: Humanoid whole-body contact manipulation through deep imitation learning with tactile modality,” _IEEE Robotics and Automation Letters_ , DOI 10.1109/LRA.2025.3580329, pp. 1–8, 2025. 

- [24] Y. Xue, W. Dong, M. Liu, W. Zhang, and J. Pang, “A unified and general humanoid whole-body controller for versatile locomotion,” _arXiv preprint arXiv:2502.03206_ , DOI 10.48550/arXiv.2502.03206, 2025. 

- [25] L. Fu, X. Li, Y. Liu, X. Zeng, Y. Peng, Y. Xiong, and S. Li, “Human-inspired adaptive gait learning for humanoids locomotion,” _IEEE Robotics and Automation Letters_ , vol. 11, DOI 10.1109/LRA.2026.3653300, no. 3, pp. 2458–2465, 2026. 

- [26] K. Chappellet, M. Murooka, G. Caron, F. Kanehiro, and A. Kheddar, “Humanoid loco-manipulations using combined fast dense 3d tracking and slam with wide-angle depth-images,” _IEEE Transactions on Automation Science and Engineering_ , vol. 21, DOI 10.1109/TASE.2023.3283497, no. 3, pp. 3691–3704, 2024. 

- [27] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit,” _arXiv preprint arXiv:2502.13013_ , DOI 10.48550/arXiv.2502.13013, 2025. 

- [28] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Aghamohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi, “Falcon: Learning force-adaptive humanoid loco-manipulation,” _arXiv preprint arXiv:2505.06776_ , DOI 10.48550/arXiv.2505.06776, 2025. 

- [29] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [30] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. M. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous human-tohumanoid whole-body teleoperation and learning,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [31] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , DOI 10.1109/IROS58592.2024.10801984, pp. 8944– 8951. Abu Dhabi, United Arab Emirates: IEEE, 2024. 

- [32] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , DOI 10.48550/arXiv.2412.13196, 2025. 

- [33] M. Elobaid, G. Romualdi, G. Nava, L. Rapetti, H. A. O. Mohamed, and D. Pucci, “Online non-linear centroidal mpc for humanoid robots payload carrying with contact-stable force parametrization,” in _2023 IEEE INTERNATIONAL CONFERENCE ON ROBOTICS AND AUTOMATION (ICRA 2023)_ , ser. IEEE International Conference on Robotics and Automation ICRA, DOI 10.1109/ICRA48891.2023.10161086, pp. 12 233–12 239. IEEE; IEEE Robot & Automat Soc, 2023. 

- [34] Y. Kuang, H. Geng, A. Elhafsi, T.-D. Do, P. Abbeel, J. Malik, M. Pavone, and Y. Wang, “Skillblender: Towards versatile humanoid whole-body loco-manipulation via skill blending,” _arXiv preprint arXiv:2506.09366_ , DOI 10.48550/arXiv.2506.09366, 2025. 

- [35] C. Tessler, Y. Jiang, E. Coumans, Z. Luo, X. B. Peng, and G. Chechik, “Maskedmanipulator: Versatile whole-body control for locomanipulation,” in _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ , DOI 10.1145/3757377.3763934, pp. 1–11. Hong Kong Hong Kong: ACM, 2025. 

- [36] C. Zhang, W. Xiao, T. He, and G. Shi, “Wococo: Learning whole-body humanoid control with sequential contacts,” in _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , ser. Proceedings of Machine Learning Research, P. Agrawal, O. Kroemer, and W. Burgard, Eds., vol. 270, pp. 455–472. PMLR, 2024. 

- [37] J. Dao, H. Duan, and A. Fern, “Sim-to-real learning for humanoid box loco-manipulation,” in _2024 IEEE International Conference on Robotics_ 

IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS 

_and Automation (ICRA)_ , DOI 10.1109/ICRA57147.2024.10610977, pp. 16 930–16 936. IEEE, 2024. 

- [38] A. Wang, H. Chen, L. Liu, K. Chen, Z. Lin, J. Han, and G. Ding, “Yolov10: real-time end-to-end object detection,” in _Proceedings of the 38th International Conference on Neural Information Processing Systems_ , ser. NIPS ’24. Red Hook, NY, USA: Curran Associates Inc., 2024. 

- [39] B. Wen, W. Yang, J. Kautz, and S. Birchfield, “Foundationpose: Unified 6d pose estimation and tracking of novel objects,” in _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , DOI 10.1109/CVPR52733.2024.01692, pp. 17 868–17 879, 2024. 


**Zhiyuan Xu** received his Ph.D. degree in computer information science and engineering from Syracuse University, Syracuse, NY, USA, in 2021, and his B.E. degree in the School of Computer Science and Engineering from the University of Electronic Science and Technology of China, Chengdu, China, in 2015. 

He is now with Beijing Innovation Center of Humanoid Robotics. His research interests include Deep Learning, Deep Reinforcement Learning, and Robot Learning, Embodied AI. 

- [40] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

**Lequn Fu** received the B.E. degree in mechanical engineering from Wuhan University of Technology, Wuhan, China. He is currently pursuing the Ph.D. degree in mechanical engineering at Huazhong University of Science and Technology, Wuhan, China. 


His research interests include motion control and learning-based control of legged robots, with particular emphasis on humanoid locomotion, and robust whole-body control for realworld deployment. 

**Yijun Zhong** received the B.E. degree in industrial engineering from Hunan University, Changsha, China, in 2024. He is currently pursuing the M.E. degree in mechanical engineering at Huazhong University of Science and Technology, Wuhan, China. 

His research interests focus on optimizationbased motion control for legged robots, particularly motion strategies and gait planning for humanoid robots in complex terrains, as well as control methods to enhance adaptability and stability in unstructured environments. 

**Xiao Li** received the M.S. degree from Huazhong University of Science and Technology, Wuhan, China, in 2022. He is currently pursuing the Ph.D. degree in mechanical engineering at Huazhong University of Science and Technology. 


His research interests include whole-body coordination control and dexterous manipulation of humanoid robots. 

**Yibin Liu** received the B.E. degree from Hefei University of Technology, Hefei, China, in 2020. He is currently pursuing the Ph.D. degree at Huazhong University of Science and Technology, Wuhan, China. 


His research interests include robotic visual SLAM, multi-sensor fusion localization, and reinforcement learning-based visual navigation. 

**Jian Tang (Fellow, IEEE)** received his Ph.D. degree in Computer Science from Arizona State University in 2006. He is an IEEE Fellow and an ACM Distinguished Member. He is with Beijing Innovation Center of Humanoid Robotics. 


His research interests lie in the areas of AI, IoT, Wireless Networking, Mobile Computing and Big Data Systems. He received an NSF CAREER award in 2009. He also received several best paper awards, including the 2019 William R. Bennett Prize and the 2019 TCBD (Technical 

Committee on Big Data), Best Journal Paper Award from IEEE Communications Society (ComSoc), the 2016 Best Vehicular Electronics Paper Award from IEEE Vehicular Technology Society (VTS), and Best Paper Awards from the 2014 IEEE International Conference on Communications (ICC) and the 2015 IEEE Global Communications Conference (Globecom) respectively. He has served as an editor for several IEEE journals, including IEEE Transactions on Big Data, IEEE Transactions on Mobile Computing, etc. In addition, he served as a TPC co-chair for a few international conferences, including the IEEE/ACM IWQoS’2019, MobiQuitous’2018, IEEE iThings’2015. etc.; as the TPC vice chair for the INFOCOM’2019; and as an area TPC chair for INFOCOM 2017- 2018. He is also an IEEE VTS Distinguished Lecturer, and the Chair of the Communications Switching and Routing Committee of IEEE ComSoc 2020-2021. 

**Shiqi Li** received the B.E., M.E., and Ph.D. degrees in engineering from Huazhong University of Science and Technology, Wuhan, China, in 1986, 1989, and 1992, respectively. He is currently a Professor with the School of Mechanical Science and Engineering, Huazhong University of Science and Technology, Wuhan, China. His research interests include humanoid robots and embodied intelligence. 


Prof. Li has been actively involved in research 

and development of advanced robotic systems and intelligent control technologies. 

