---
title: "Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation (H2O)"
date: "2024"
venue: "未確認(arXivページに記載なし)"
url: https://arxiv.org/abs/2403.04436
pdf: https://arxiv.org/pdf/2403.04436
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2403.04436)** / [論文ページ](https://arxiv.org/abs/2403.04436)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation** 

Tairan He<sup>†</sup> Zhengyi Luo<sup>†</sup> Wenli Xiao Chong Zhang Kris Kitani Changliu Liu Guanya Shi Carnegie Mellon University †Equal Contributions https://human2humanoid.com 


Fig. 1: The **humanoid robot** is teleoperated in real-time using an RGB camera by the **human teleoperator** . (a) The humanoid mimics the human teleoperator, advancing one step while delivering a punch to displace a box, followed by a victory gesture. (b) The humanoid executes a precise sidestep to align with a ball and delivers a controlled kick using its right foot. (c) The humanoid demonstrates forward walking while pushing a stroller. (d) The operator teleoperates the humanoid to catch a box, rotate its waist, and drop the box into a waste bin. **Videos:** see the website. 

**_Abstract_ — We present Human to Humanoid (H2O), a reinforcement learning (RL) based framework that enables realtime whole-body teleoperation of a full-sized humanoid robot with only an RGB camera. To create a large-scale retargeted motion dataset of human movements for humanoid robots, we propose a scalable “sim-to-data” process to filter and pick feasible motions using a privileged motion imitator. Afterwards, we train a robust real-time humanoid motion imitator in simulation using these refined motions and transfer it to the real humanoid robot in a zero-shot manner. We successfully achieve teleoperation of dynamic whole-body motions in real-world scenarios, including walking, back jumping, kicking, turning, waving, pushing, boxing,** **_etc_ . To the best of our knowledge, this is the first demonstration to achieve learning-based real-time whole-body humanoid teleoperation.** 

# I. INTRODUCTION 

We aim to enable real-time teleoperation of a full-sized humanoid robot by a human teleoperator using an RGB 

camera. Humanoid robots, with their physical form closely mirroring that of humans, present an unparalleled opportunity for real-time teleoperation. This alignment of the embodiment allows for a seamless integration of human cognitive skills with versatile humanoid capabilities [1]. Such synergy stimulated by human-to-humanoid teleoperation is crucial for complex tasks ( _e.g_ ., household chores, medical assistance, high-risk rescue operations) that are yet too challenging for a fully autonomous robot, but possible for existing hardware teleoperated by humans [2, 3]. In this paper, we transfer human motions to humanoid behaviors in a real-time fashion using an RGB camera. This system also has the potential to enable large-scale and high-quality data collection of human operations for robotics [2, 4], where human-teleoperated actions can be used for imitation learning. 

However, whole-body control of full-sized humanoids is a long-standing problem in robotics [5], and complexity 

increases when controlling the humanoid to replicate freeform human movements in real-time [1]. Existing work on whole-body humanoid teleoperation has achieved remarkable results via model-based controllers [6–9], but they all use simplified models due to the high computational cost of modeling the full dynamics of the system [10, 11], which limits the scalability to dynamic motions. Furthermore, these works are highly dependent on contact measurement [12, 13], leading to reliance on external setups such as the exoskeleton [9] and force sensors [8, 14] for teleoperation. 

Recent advances in reinforcement learning (RL) for humanoid control provide a promising alternative. First, in the graphics community, RL has been used to generate complex human movements [15, 16], perform a variety of tasks [17], and track real-time human motions captured by a webcam [18] in simulation. However, due to unrealistic state-space design and partial disregard of the hardware limit ( _e.g_ . torque / joint limit), it remains a question whether these methods can be applied to a full-sized humanoid. On the other hand, RL has achieved robust and agile biped locomotion in the real world [19–21]. To date, however, there has been no existing work on RL-based whole-body humanoid teleoperation. The most closely related effort is a concurrent study [22], which focuses on learning to replicate upper-body motions and uses root velocity tracking for the lower body, from offline human motions rather than real-time teleoperation. 

In this paper, we design a complete system for humanoid teleportation in real time. First, we identify one of the primary challenges in whole-body humanoid teleoperation as the lack of a dataset with feasible motions tailored to the humanoid, which is essential for training a controller that can track diverse motions. Although direct human-to-humanoid retargeting has been explored in previous locomotion-focused efforts [23–25], retargeting a largescale human motion dataset to the humanoid presents new challenges. That is, the significant dynamics discrepancy between humans and humanoids means that some human motions could be infeasible for the humanoid ( _e.g_ . cartwheeling, steps wider than the leg lengths of the humanoid). In light of this, we introduce an automated “sim-to-data” process to retarget and refine a large-scale human motion dataset [26] into motions that are feasible for real-world humanoid embodiment. Specifically, we first retarget the human motions to the humanoid via inverse kinematics, and train a humanoid controller with access to privileged state information [18] to imitate the unfiltered motions in simulation. Afterwards, we remove the motion sequences that the privileged imitator fails to track. By doing so, we create a large-scale humanoid-compatible motion dataset. 

After obtaining a dataset of feasible motions, we develop a scalable training process for the real-world motion imitator that incorporates extensive domain randomization to bridge the sim-to-real gap. To facilitate real-time teleoperation, we design a state space that prioritizes the inputs available in the real world using an RGB camera, such as the keypoint positions. During inference, we use an off-the-shelf human pose estimator [27] to provide global human body positions 

for the humanoid to track. 

In summary, we demonstrate the feasibility of an RL-based real-time Human-to-Humanoid (H2O) teleoperation system. Our contributions include: 

- 1) A scalable retargeting and “sim-to-data” process to obtain a large-scale motion dataset feasible for the realworld humanoid robot; 

- 2) Sim-to-real transfer of the RL-based whole-body tracking controller that scales to a large number of motions; 

- 3) A real-time teleoperation system with an RGB camera and 3D human pose estimation, demonstrating fulfillment of various whole-body motions including walking, pick-and-place, stroller pushing, boxing, handwaving, ball kicking, etc. 

II. RELATED WORKS 

# _A. Physics-Based Animation of Human Motions_ 

Physics-based simulation has been used to generate realistic and natural motions for avatars [15–18, 28–33]. With motion capture as the main source of human motion data [26], RL is often used to learn avatar controllers that can mimic these motions, offering distinctive styles [15, 31], scalability [16, 18, 34], and reusability [17, 32]. 

However, realistic animation in physics-based simulators does not guarantee real-world applicability, especially for humanoids. Simulated humanoid avatars typically have high degrees of freedom and large joint torques [35], and sometimes need non-physical assistive external forces [36]. In this work, we demonstrate that, with carefully designed sim-to-real training, approaches in the humanoid animation community can be applied to a real-world humanoid robot. 

# _B. Transferring Human Motions to Real-World Humanoids_ 

Before the emergence of RL-based humanoid controllers, traditional methods typically employ model-based optimization to track retargeted motions while maintaining stability [1]. To this end, these methods minimize tracking errors under the constraints of stability and contacts, requiring predefined contact states [6, 10, 12, 13, 37–40] or estimated contacts from sensors [7, 9, 14, 41, 42], hindering largescale deployment outside the laboratory. Zhang _et al._ [11] use contact-implicit model predictive control (MPC) to track motions extracted from videos, but trajectories must first be optimized offline to ensure dynamic feasibility. Furthermore, the model used in MPC needs to be simplified due to computational burden [6, 11, 14], which limits the capability of trackable motions. 

RL-based controllers may provide an alternative that does not require explicit contact information. Some works [43, 44] use imitation learning to transfer human-style motions to the controller, but do not accurately track human motions. Cheng _et al._ [22] train whole-body humanoid controllers that can replicate upper body movements from offline human motions, but the lower body relies on root velocity tracking and does not track precise lower body movements. In comparison, our work achieves real-time whole-body tracking of human motions. 

# _C. Teleoperation of Humanoids_ 

Teleoperation of humanoids can be categorized into three types: 1) task-space teleoperation [45, 46], 2) upper-bodyretargeted teleoperation [47, 48], and 3) whole-body teleoperation [6, 7, 13, 42, 49]. For the first and second types, the shared morphology between humans and humanoids is not fully utilized, and whole-body control must be solved in a task-specified way. This also raises the concern that, if tracking lower body movement is not necessary, the robot could opt for designs with better stability, such as a quadruped [50] or wheeled configuration [51]. 

Our work belongs to the third type and is the first to achieve learning-based whole-body teleoperation. Moreover, our approach does not require capture markers or force sensors on the human teleoperator, as we directly employ an RGB camera to capture human motions for tracking, potentially paving the way for collecting large-scale humanoid data for training autonomous agents. 

# III. PRELIMINARIES 

The whole-body real-time humanoid teleoperation we are tackling is formulated as a goal-conditioned RL problem, which tracks versatile human motion with a single RL control policy. In Section III-A, we set up the preliminary for our control framework. Section III-B describes the human model and dataset we use in the RL policy training. As a notation convention, we use � _·_ to represent kinematic quantities (without physics simulation) from pose estimator/keypoint detectors, � _·_ to denote ground truth quantities from Motion Capture (MoCap), and normal symbols without accents for values from the physics simulation. 

# _A. Goal-conditioned RL for Humanoid Control_ 

We formulate our problem as goal-conditioned RL where _π_ is trained to track real-time human motions. We formulate the learning task as a Markov Decision Process (MDP) defined by the tuple _M_ = _⟨S, A, T , R, γ⟩_ of state **_s_** _t ∈S_ , action **_a_** _t ∈A_ , transition dynamics _T_ , reward function _R_ , and discount factor _γ_ . The state **_s_** _t_ contains the proprioception **_s_**<sup>p</sup> _t_<sup>andthegoalstate</sup><sup>**_s_**g</sup> _t_<sup>.Thegoalstate</sup> **_s_**<sup>g</sup> _t_<sup>isaunifiedrepresentationofthewhole-bodymotionof</sup> the human teleoperator, which we will discuss in detail in Section V-A. Based on proprioception **_s_**<sup>p</sup> _t_<sup>andgoalstate</sup> **_s_**<sup>g</sup> _t_<sup>,wedefinethereward</sup><sup>_rt_=</sup><sup>_R_</sup> � **_s_**<sup>p</sup> _t_<sup>_,_</sup><sup>**_s_**g</sup> _t_ � for the policy training. The action **_a_** _t ∈_ R<sup>19</sup> specifies the joint target positions that the PD controller will use to actuate the degrees of freedom. We apply the proximal policy gradient (PPO) [52] to maximize the cumulative discounted reward E _t_ =1<sup>_γt−_1</sup><sup>_rt_</sup> . We formulate the teleoperation task as the �� _T_ � motion imitation/tracking/mimicking task, where we train the humanoid to track the reference motion at every frame. 

# _B. Parametric Human Model and Human Motion Dataset_ 

Popular in the vision and graphics community, parametric human models such as SMPL [53] are easy to work with representations of human shapes and motions. SMPL represents the human body as body shape parameters **_β_** _∈R_<sup>10</sup> , pose 


Fig. 2: Fitting the SMPL body to the H1 humanoid. (a) Visualization of the humanoid keypoints (red dots) (b) Humanoid keypoints vs SMPL keypoints (green dots and mesh) before and after fitted SMPL shape **_β_**<sup>_′_</sup> . (c) Corresponding 12 joint position before and after fitting. 


Fig. 3: Effect of using a fitted SMPL shape **_β_**<sup>_′_</sup> instead of mean body shape on position-based retargeting. (a) Retargting without using **_β_**<sup>_′_</sup> , which results in unstable “in-toed” humanoid motion. (b) Retargeting using **_β_**<sup>_′_</sup> , which result in balanced humanoid motion. 

parameters **_θ_** _∈R_<sup>24</sup><sup>_×_3</sup> , and root translation **_p_** _∈R_<sup>24</sup><sup>_×_3</sup> . Given **_β_** , **_θ_** and **_p_** , _S_ denotes the SMPL function, where _S_ ( **_β_** _,_ **_θ_** _,_ **_p_** ) : **_β_** _,_ **_θ_** _,_ **_p_** _→R_<sup>6890</sup><sup>_×_3</sup> maps the parameters to the position of the vertices of a triangular human mesh of 6890 vertices. The AMASS [26] dataset contains 40 hours of motion capture expressed in the SMPL parameters. 

# IV. RETARGETING HUMAN MOTIONS FOR HUMANOID 

To enable humanoid motion imitation for unscripted human motion, we require a large amount of whole-body motion to train a robust motion imitation policy. Since humans and humanoids also have a nontrivial difference in body structure, shape, and dynamics, naively retargeted motion from a human motion dataset can result in a large number of motions impossible for our humanoid to perform. These imfeasible motion sequences can hinder imitation training as observed in prior work [32]. To resolve these issues, we design a “sim-to-data” approach to complement traditional retargeting to convert a large-scale human motion dataset to feasible motions for humanoids. 

# _A. Motion Retargeting_ 

As there is a non-trivial difference between the SMPL kinematic structure and the humanoid kinematic tree, we perform a two-step process for the initial retargeting. First, since the SMPL body model can represent different body 


Fig. 4: Overview of H2O: (a) **Retargeting** (Section IV): H2O first aligns the SMPL body model to a humanoid’s structure by optimizing shape parameters. Then H2O retargets and removes the infeasible motions using a trained privileged imitation policy, producing a clean motion dataset. (b) **Sim-to-Real Training** : (Section V) An imitation policy is trained to track motion goals sampled from a cleaned dataset. (c) **Real-time Teleoperation Deployment** (Section VI-B): The real-time teleoperation deployment captures human motion through an RGB camera and a pose estimator, which is then mimicked by a humanoid robot using the trained sim-to-real imitation policy. 

proportions, we first find a body shape **_β_**<sup>_′_</sup> closest to the humanoid structure. We choose 12 joints that have a correspondence between humans and humanoids, as shown in Fig.2 and perform gradient descents on the shape parameter **_s_** to minimize the joint distances using a common rest pose. After finding the optimal **_β_**<sup>_′_</sup> , given a sequence of motions expressed in SMPL parameters, we use the original translation **_p_** and pose **_θ_** , but the fitted shape **_β_**<sup>_′_</sup> to obtain the set of body keypoint positions. Then we retarget motion from human to humanoid by minimizing the 12 joint position differences using Adam optimizer [54]. Notice that our retargeting process try to match the end effectors of the human to the humanoid ( _e.g_ . ankles, elbows, wrists) to preserve the overall motion pattern. Another approach is direct copying the local joint angles from human to humanoid, but that approach can lead to large differences in end-effector positions due to the large difference in kinematic trees. During this process, we also add some heuristic-based filtering to remove unsafe sequences, such as sitting on the ground. The motivation to find **_β_**<sup>_′_</sup> before retargeting is that in the rest pose, our humanoid has a large gap between its feet. If naively trying to match the foot movement between the human and the humanoid, the humanoid motion can have an in-toed artifact. Using **_β_**<sup>_′_</sup> , we can find a human body structure has a large gap between its rest pose (as shown in Fig.2). Using **_β_**<sup>_′_</sup> during fitting can effectively create motion that is more feasible for 

the **_Q_ ˆ** that contains 13k motion sequences, this process computeshumanoid, as shown in Fig.3. From the AMASS dataset 10k retargted motion sequences **_Q_**<sup>**ˆ**retarget</sup> . 

# _B. Simulation-based Data Cleaning_ 

As shown in Figure 4 _,_ **_Q_**<sup>**ˆ**retarget</sup> contain a large number of implausible motions for the humanoid due to the significant gap between the capabilities of a human and a motor-actuated humanoid. Manually finding these data sequences from a large-scale dataset can be a rather cumbersome process. Thus, we propose a “sim-to-data” procedure, where we train a motion imitator _π_ privileged (similar to PHC [18]) with access to privileged information and no domain randomization to imitate all uncleaned data **_Q_**<sup>**ˆ**retarget</sup> . Without domain randomization, _π_ privileged can perform well in motion imitation, but is not suitable for transfer to the real humanoid. However, _π_ privileged represents the upper bound of motion imitation performance, and sequences which _π_ privileged fails to imitate represent implausible ones. Specifically, we train _π_ privileged following the same state space, control parameters, and hardnegative mining procedure proposed in PULSE [32], and train a single imitation policy to imitate the entire retargeted dataset. After training, _∼_ 8.5k out of 10k motion sequences from AMASS turn out to be plausible for the H1 humanoid, and we denote the obtained clean dataset as **_Q_**<sup>**ˆ**clean</sup> . 

**Privileged Motion Imitation Policy** . To train _π_ privileged, we follow PULSE [32] and train a motion imitator with access 

to the full rigid body state of the humanoid. Specifically, for the privileged policy _π_ privileged, its proprioception is defined as **_s_**<sup>p-privileged</sup> _t_ ≜ [ **_p_** _t,_ **_θ_** _t,_ **_v_** _t,_ **_ω_** _t_ ], which contains the global 3D rigid body position **_p_** _t_ , orientation **_θ_** _t_ , linear velocity **_v_** _t_ , and angular velocity **_ω_** _t_ of all rigid bodies in the humanoid. The goal state is defined as **_s_**<sup>g-privileged</sup> _t_ ≜ [ **_θ_**<sup>**ˆ**</sup> _t_ +1 _⊖_ **_θ_** _t,_ **ˆ** **_p_** _t_ +1 _−_ **_p_** _t,_ **ˆ** **_v_** _t_ +1 _−_ **_v_** _t,_ **ˆ** **_ω_** _t −_ **_ω_** _t,_ **_θ_**<sup>**ˆ**</sup> _t_ +1 _,_ **ˆ** **_p_** _t_ +1], which contains the one-frame difference between the reference and current simulation result for all rigid bodies on the humanoid. It also contains the next frame’s reference rigid body orientation and position. All values are normalized to the humanoid’s coordinate system. Notice that all values are global, and values such as global rigidbody linear velocity **_v_** _t_ and angular velocity **_ω_** _t_ are hard to obtain accurately in the real world. 

# V. WHOLE-BODY TELEOPERATION POLICY TRAINING 

# _A. State Space_ 

To achieve real-time teleoperation of humanoid robots, the state space of RL policy must contain only quantities available in the real world. This differs from the simulationonly approaches, where all the physics information ( _e.g_ ., foot contact force) is available. For example, in the real world, we have no access to each joint’s precise global angular velocity due to the lack of IMUs, but the privileged policy _π_ privileged requires them. 

In our state space design, proprioception is defined by **_s_**<sup>p</sup> _t_<sup>≜[</sup><sup>**_q_**</sup> _t_<sup>_,_</sup><sup>**_q_˙**</sup><sup>_t,_</sup><sup>**_v_**</sup><sup>_t,_</sup><sup>**_ω_**</sup><sup>_t,_</sup><sup>**_g_**</sup><sup>_t,_</sup><sup>**_a_**</sup><sup>_t−_1],withjointposition</sup><sup>**_q_**</sup> _t_<sup>_∈_R19</sup> (DoF position), joint velocity **_q_ ˙** _t ∈_ R<sup>19</sup> (DoF velocity), root linear velocity **_v_** _t ∈_ R<sup>3</sup> , root angular velocity **_ω_** _t ∈_ R<sup>3</sup> , root projected gravity **_g_** _t ∈_ R<sup>3</sup> , and last action **_a_** _t−_ 1 _∈_ R<sup>19</sup> . kp The goal state is **_s_**<sup>g</sup> _t_<sup>≜[</sup><sup>**_p_ˆ**kp</sup> _t_<sup>_,_</sup><sup>**ˆ**</sup><sup>**_p_**kp</sup> _t_<sup>_−_</sup><sup>**_p_**</sup> _t_ kp _,_ **ˆ˙** **_p_** _t_<sup>].</sup><sup>**_p_ˆ**</sup> _t_<sup>kp</sup> _∈_ R<sup>8</sup><sup>_×_3</sup> is the position of eight selected reference body positions (shoulders, elbows, hands, ankles); **_p_ ˆ**<sup>kp</sup> _t_<sup>_−_</sup><sup>**_p_**</sup> _t_ kp is the position difference between the reference joints and humanoid’s own joints; **_p_**<sup>**ˆ**</sup> **˙** kp _t_ is the linear velocity of the reference joints. All values are normalized to the humanoid’s own coordinate system. As a comparison, we also consider a reduced goal state **_s_**<sup>g-reduced</sup> _t_ ≜ ( **_p_ ˆ**<sup>kp</sup> _t_<sup>),whereonlythereferenceposition</sup> **_p_ ˆ**<sup>kp</sup> _t_ but not the position difference. The action space of the agile policy consists of 19-dim joint targets. A PD controller tracks these joint targets by converting them to joint torques: _τ_ = _Kp_ ( **_a_** _t −_ **_q_** _t_ ) _− Kd_ **˙** **_q_** _t_ . 

# _B. Reward Design_ 

We formulate the reward function _rt_ with the summation of three terms: 1) penalty; 2) regularization; and 3) task rewards, which are summarized in detail in Table I. Note that while we only have eight selected body positions **_p_ ˆ**<sup>kp</sup> _t_ in our state space, we provide six _full-body_ reward terms for all joints (DoF position, DoF velocity, body position, body rotation, body velocity, body angular velocity) for the imitation task. These expressive rewards give more dense reward signals for efficient RL training. 

# _C. Domain Randomization_ 

Domain randomization has been shown to be the key source of robustness and generalization to achieve successful 

TABLE I: Reward components and weights: penalty rewards for preventing undesired behaviors for sim-to-real transfer, regularization to refine motion, and task reward to achieve successful whole-body tracking in real-time. 

|Term|Expression|Weight|
|---|---|---|
||Penalty||
|Torque limits|1(**_τ_**_t /∈_[**_τ_**min_,_**_τ_**max])|_−_2_e_<sup>_−_1</sup><br>|
|DoF position limits<br>Termination|1(**_q_**_t /∈_[**_q_**min_,_**_q_**max])<br>1termination|_−_1_e_<sup>2</sup><br>_−_2_e_<sup>2</sup>|
||Regularization||
|DoF acceleration|_∥_**¨****_q_**_t∥_<sup>2</sup><br>2|_−_8_._4_e_<sup>_−_6</sup>|
|DoF velocity|_∥_**˙****_q_**_t∥_<sup>2</sup><br>2|_−_3_e_<sup>_−_3</sup>|
|Action rate|_∥_**_a_**_t −_**_a_**_t−_1_∥_<sup>2</sup><br>2|_−_9_e_<sup>_−_1</sup>|
|Torque|_∥_**_τ_**_t∥_|_−_9_e_<sup>_−_5</sup>|
|Feet air time|_T_air_−_0_._25 [55]|8_e_<sup>2</sup>|
|Feet contact force|_∥F_feet_∥_<sup>2</sup><br>2|_−_1_e_<sup>_−_1</sup>|
|Stumble|1(_F _<sup>_xy_</sup><br>feet <sup>_>_ 5</sup><sup>_× F z_</sup><br>feet<sup>)</sup>|_−_1_e_<sup>3</sup>|
|Slippage|<br><br>_∥_**_v_**_t_<sup>feet</sup>_∥_<sup>2</sup><br>2 <sup>_×_ 1(</sup><sup>_F_feet</sup> <sup>_≥_1)</sup>|_−_3_e_<sup>1</sup>|
||Task Reward||
|DoF position|exp(_−_0_._25_∥_**ˆ****_qt_**_−_**_q_**_t∥_2)<br>|2_._4_e_<sup>1</sup>|
|DoF velocity|exp(_−_0_._25_∥_<sup>**ˆ**</sup>**˙****_q_**_t −_**˙****_q_**_t∥_<sup>2</sup><br>2<sup>)</sup>|2_._4_e_<sup>1</sup>|
|Body position|exp(_−_0_._5_∥_**_p_**_t −_**ˆ****_p_**_t∥_<sup>2</sup><br>2<sup>)</sup>|4_e_<sup>1</sup>|
|Body rotation|exp(_−_0_._1_∥_**_θ_**_t ⊖_<sup>**ˆ**</sup>**_θ_**_t∥_)|1_._6_e_<sup>1</sup>|
|Body velocity|exp(_−_10_._0_∥_**_v_**_t −_**ˆ****_v_**_t∥_2)|6_e_<sup>1</sup>|
|Body angular velocity|exp(_−_0_._01_∥_**_ω_**_t −_**ˆ****_ω_**_t∥_2)|6_e_<sup>1</sup>|


TABLE II: The range of dynamics randomization. Describing simulated dynamics randomization, external perturbation, and randomized terrain, which are important for sim-to-real transfer and boost robustness and generalizability. 

|Term<br>Value<br>|
|---|
|**Dynamics Randomization**|
|Friction<br>_U_(0_._2_,_1_._1)|
|Base CoM offset<br>_U_(_−_0_._1_,_0_._1)m|
|Link mass<br>_U_(0_._7_,_1_._3)_×_default kg|
|P Gain<br>_U_(0_._75_,_1_._25)_×_default|
|D Gain<br>_U_(0_._75_,_1_._25)_×_default|
|Torque RFI [56]<br>0_._1_×_torque limit N_·_m<br>Control delay<br>_U_(20_,_60)ms|
|**External Perturbation**<br><br>|
|Push robot<br>interval= 5_s_, _vxy_ = 0_._5m/s|
|**Randomized Terrain**<br><br>l|
|Terrain type<br>flat, rough, low obstacles [57]|


sim-to-real transfers [19, 58]. All the domain randomization we use in H2O are listed in Table II, including ground friction coefficient, link mass, Centor-of-Mass (CoM) position of the torso link, PD gains of the PD controller, torque noise on the actually applied torques on each joint, control delay, terrain types. The link mass and PD gains are independently randomized for each link and joint, and the rest are episodic randomized. These domain randomization together can effectively facilitate the sim-to-real transfer for the real-world dynamics and hardware gaps. 

# _D. Early Termination Conditions_ 

We introduce three early termination conditions to make the RL training process more sample-efficient: 1) low height: the base height is lower than 0.3m; 2) orientation: the projected gravity on x or y axis exceeds 0.7; 3) teleoperation tolerance: the average link distance between the robot and reference motions is further than 0.5m. 

TABLE III: Quantitative motion imtiation results the uncleaned retargeted AMASS dataset **_Q_**<sup>**ˆ**retarget</sup> . 

|||||All|sequences|||S|uccessful se|quences||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Method|State Dimension|Sim2Real|Succ_↑_|_E_g-mpjpe _↓_|_E_mpjpe _↓_|Eacc _↓_|Evel _↓_|_E_g-mpjpe _↓_|_E_mpjpe _↓_|Eacc _↓_|Evel _↓_|
|Privileged policy|_S ⊂R_<sup>778</sup>|✗|85.5%|50.0|43.6|6.9|7.8|46.0|40.9|5.2|6.2|
|H2O-reduced|_S ⊂R_<sup>90</sup>|✓|53.2%|200.2|115.8|11.2|13.8|182.5|111.0|3.0|8.1|
|H2O-w/o-sim2data|_S ⊂R_<sup>138</sup>|✓|67.9%|176.6|95.0|10.2|12.2|163.1|93.8|3.0|7.5|
|H2O|_S ⊂R_<sup>138</sup>|✓|**72.5%**|**166.7**|**91.7**|**8.9**|**11.0**|**151.0**|**88.8**|**2.9**|**7.0**|


# VI. EXPERIMENTAL RESULTS 

# _A. Simulation Experiments_ 

**Baselines** . To reveal the effect of different retargeting, state space designs, and sim-to-real training techniques on wholebody teleoperation performance, we consider four baselines: 

- 1) Privileged policy _π_ privileged: The privileged policy (trained without any sim-to-real regularizations or domain randomizations) is used to filter the dataset to find infeasible motion. It has no sim-to-real capability and has a much higher input dimension. 

- 2) H2O-w/o-sim2data: H2O without the “sim-to-data” retargeting, trained on the **_Q_**<sup>**ˆ**retarget</sup> ; 

- 3) H2O-reduced: H2O with a state space of goal state consisting only of selected body positions **_s_**<sup>g-reduced</sup> _t_ . 

- 4) H2O: Our full H2O system, with all the retargeting process introduced in Section IV and the state space design introduced in Section V-A, trained on **_Q_**<sup>**ˆ**clean</sup> ; 

**Metrics** . We evaluate these baselines in simulation on the uncleaned retargeted AMASS dataset (10k sequences **_Q_**<sup>**ˆ**retarget</sup> ). The metrics are as follows: 

- 1) Success rate: the success rate (Succ) as in PHC [18], deeming imitation unsuccessful when, at any point during imitation, the average difference in body distance is on average further than 0.5m. Succ measures whether the humanoid can track the reference motion without losing balance or significantly lag behind. 

- 2) _E_ mpjpe and _Eg−_ mpjpe: the global MPJPE _Eg−_ mpjpe and the root-relative mean per-joint position error (MPJPE) _E_ mpjpe (in mm), measuring our imitator’s ability to imitate the reference motion both globally and locally (root-relative). 

- 3) _E_ acc and _E_ vel: To show physical realism, we also compare acceleration _E_ acc (mm/frame<sup>2</sup> and velocity _E_ vel (mm/frame) difference. 

**Results** . The experimental results are summarized in Table III, where H2O significantly outperforms H2O-w/osim2data and H2O-reduced by a large margin, demonstrating the importance of the “sim-to-data” process and the statespace design of motion goals for RL. Note that the privileged policy and H2O-w/o-sim2data are trained on the entire retargeted AMASS dataset **_Q_**<sup>**ˆ**retarget</sup> while H2O and H2O-reduced are trained on the filtered dataset **_Q_**<sup>**ˆ**clean</sup> . The success rate gap between H2O and the privileged policy comes from two factors: 1) H2O uses a much more practical and less informative observation space compared to the privileged 

TABLE IV: Quantitative results of H2O on different sizes of motion dataset for training, evaluated on the uncleaned retargeted AMASS dataset **_Q_**<sup>**ˆ**retarget</sup> . 

|||All|sequences|||
|---|---|---|---|---|---|
|Dataset Size|Succ_↑_|_E_g-mpjpe _↓_|_E_mpjpe _↓_|Eacc _↓_|Evel|
|0_._1% of <sup>**ˆ**</sup><br>**_Q_**<sup>clean</sup>|52.0%|198.0|107.9|12.4|13.7|
|1% of <sup>**ˆ**</sup><br>**_Q_**<sup>clean</sup>|58.8%|183.8|96.4|10.7|12.0|
|10% of <sup>**ˆ**</sup><br>**_Q_**<sup>clean</sup>|61.3%|174.3|92.3|10.8|12.1|
|100% of <sup>**ˆ**</sup><br>**_Q_**<sup>clean</sup>|**72.5%**|**166.7**|**91.7**|**8.9**|**11.0**|


policy; 2) H2O is trained with all sim-to-real regularizations and domain randomization. These two factors will both lead to degradation in simulation performance. This shows that while the RL-based avatar control frameworks have achieved impressive results in simulation, transferring them to the real world requires more robustness and stability. With the carefully chosen dataset and the state space, we could make H2O achieve a higher success rate compared to H2O-w/osim2data and H2O-reduced. By comparing H2O with H2Ow/o-sim2data, we can see that our “sim-to-data” process is effective in obtaining higher success rate, even when the RL policy is trained on _less_ data. Intuitively, an implausible motion may cause the policy to waste resources trying to achieve them, and filtering them out can lead to better overall performance, as also observed in PULSE [32]. Comparing H2O with H2O-reduced, the only difference is the design of the state space of the goal, which indicates that including more informative physical information about motions helps RL to generalize to large-scale motion imitation. 

**Ablation on Motion Dataset Size** . To show how motion tracking performance scales with the size of the motion dataset, we test H2O with different size of **_Q_**<sup>**ˆ**clean</sup> by randomly selecting 1%, 10% of **_Q_**<sup>**ˆ**clean</sup> . The results are summarized in Table IV, where policies trained larger motion datasets continue to improve the tracking performance. Notice that a policy trained on only 0.1% of the data can achieve a surprisingly high success rate, most likely due to the ample domain randomization applied to the humanoid, such as push robot significantly widens the state the humanoid has encountered, improving its generalization capability. 

# _B. Real-world Demonstrations_ 

**Deployment Details** . For real-world deployment tests, we use a standard 1080P webcam as the RGB camera, and use HybrIK [27] as the 3D human pose estimator running at 30Hz. For the linear velocity estimation of the robot, we 

leverage the motion capture system (50Hz), and all the other proprioception is obtained from built-in sensors (200Hz) of Unitree H1 humanoid. Linear velocity state estimation could be replaced by onboard visual/LiDAR odometry methods, though we opt in to MoCap for this work due to its simplicity. **Real-world Teleoperation Results** . For real-time teleoperation, the 3D pose estimation from the RGB camera is noisy and can suffer from perspective bias, but our H2O policy shows a strong generalization ability to real-world estimated motion goals in real-time. The real-world teleoperation is shown in Figure 1, Figure 5 and Figure 6, where H2O enables precise real-time teleoperation of humanoids to do wholebody dynamic motions like ball kicking, walking, and back jumping. More demonstrations can be found on our website. 


Fig. 5: The humanoid robot is able to track the precise lowerbody movements of the human teleoperator. 


Fig. 6: The humanoid robot is able to track walking motions of human-style pace and imitate continuous back jumping. 

**Robustness** . Our H2O system can keep balance under external force disturbances, as shown in Figure 7. These tests demonstrate the robustness of our system. 

VII. DISCUSSIONS, LIMITATIONS, AND FUTURE WORK 

**Towards Universal Humanoid Teleoperation** . Our ultimate goal is to enable the humanoid to follow as many humandemonstrated motions as possible. We emphasize three key factors that can be improved in the future. 1) Closing the representation gap: as shown in Section VI-A, the state representation of the motion goals critically affects the scalability of RL training with more diverse motions, leading to a tradeoff. While incorporating more expressive motion representations into the state space can accommodate finer-grained and more diverse motions, the expanded dimensionality will lead to a curse of sample efficiency in scalable RL. 2) Closing the embodiment gap: as evident in Section VI-A and prior 


Fig. 7: Robustness Tests of our H2O system under powerful kicking. The policy is able to maintain balance for both stable and dynamic teleoperated motions. 

work [32], training on infeasible or damaged motions might largely harm performance. The feasibility of motions varies from robot to robot due to hardware constraints, and we lack systematic algorithms to identify feasible motions. We need more efforts to close this embodiment gap: on one end, more human-like humanoids would help; on the other, more teleoperation research is expected to improve the learnability of human motions. 3) Closing the sim-to-real gap: to achieve a successful sim-to-real transfer, regularization (e.g., reward regularization) and domain randomization are needed. However, over-regularization and over-randomization will also hinder the policy from learning the motions. It remains unknown how to strike the best trade-off between motion imitation leaning and sim-to-real transfer into a universal humanoid control policy. 

**Towards Real-time Humanoid Teleoperation** . In this work, we leverage RGB and 3D pose estimator to transform the motions of human teleoperators into humanoid robots. The latency and error from RGB cameras and pose estimation also lead to an inevitable trade-off between efficiency and precision in teleoperation. Also, in this work, the human teleoperator receives feedback from the humanoid only in the form of visual perception. More research is needed on human-robot interaction to study this emerging multimodal interaction (e.g., force feedback [59], verbal and conversational feedback [60]), which could further enhance the capability of humanoid teleoperation. 

**Towards Whole-body Humanoid Teleoperation** . One may wonder if lower-body tracking is necessary, as the major embodiment gap between humans and humanoids is the lower-body capability. A large proportion of skillful motions of humans (e.g., sports, dancing) need diverse agile lowerbody movements. We emphasize the scenarios where legged robots hold an advantage over wheeled robots, in which lower-body tracking is necessary to follow human lowerbody movements, including stepping stones, kicking, spread legs, etc. In the future, a teleoperated humanoid system that learns to switch between robust locomotion and skillful lower-body tracking would be a promising research direction. 

# VIII. CONCLUSIONS 

In this study, we introduced Human to Humanoid (H2O), a scalable learning-based framework that enables real-time whole-body humanoid robot teleoperation using just an RGB camera. Our approach, leveraging reinforcement learning and a novel “sim-to-data” process, addresses the complex challenge of translating human motion into actions a humanoid robot can perform. Through comprehensive simulation and real-world tests, H2O demonstrated its capability to perform a wide range of dynamic tasks with high fidelity and minimal hardware requirements. 

# ACKNOWLEDGMENT 

The authors express their gratitude to Jessica Hodgins for providing assistance in conducting hardware experiments. Special thanks are extended to Ziqiao Ma, Zhongyu Li, Yiyu Chen, Xuxin Cheng, and Unitree for their valuable help on graphics design and hardware debugging. Furthermore, we acknowledge the significance of CMU Wean Hall room 1334, formerly utilized as the recording location for the CMU MoCap dataset. In the present study, this dataset is used for real-world humanoid teleoperation within the same room. 

# REFERENCES 

- [1] K. Darvish _et al._ , “Teleoperation of humanoid robots: A survey,” _IEEE Transactions on Robotics_ , 2023. 

- [2] Z. Fu, T. Z. Zhao, and C. Finn, “Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation,” _arXiv preprint arXiv:2401.02117_ , 2024. 

- [3] C. Chi _et al._ , “Universal manipulation interface: Inthe-wild robot teaching without in-the-wild robots,” _arXiv preprint arXiv:2402.10329_ , 2024. 

- [4] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” _arXiv preprint arXiv:2304.13705_ , 2023. 

- [5] D. Kuli´c, G. Venture, K. Yamane, E. Demircan, I. Mizuuchi, and K. Mombaur, “Anthropomorphic movement analysis and synthesis: A survey of methods and applications,” _IEEE Transactions on Robotics_ , vol. 32, no. 4, pp. 776–795, 2016. 

- [6] F.-J. Montecillo-Puente, M. Sreenivasa, and J.-P. Laumond, “On real-time whole-body human to humanoid motion transfer,” 2010. 

- [7] Y. Ishiguro _et al._ , “High speed whole body dynamic motion experiment with real time master-slave humanoid robot system,” in _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , IEEE, 2018, pp. 5835–5841. 

- [8] J. Ramos and S. Kim, “Humanoid dynamic synchronization through whole-body bilateral feedback teleoperation,” _IEEE Transactions on Robotics_ , vol. 34, no. 4, pp. 953–965, 2018. 

- [9] Y. Ishiguro _et al._ , “Bilateral humanoid teleoperation system using whole-body exoskeleton cockpit tablis,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 6419–6426, 2020. 

- [10] K. Yamane, S. O. Anderson, and J. K. Hodgins, “Controlling humanoid robots with human motion data: Experimental validation,” in _2010 10th IEEERAS International Conference on Humanoid Robots_ , IEEE, 2010, pp. 504–510. 

- [11] J. Z. Zhang _et al._ , “Slomo: A general system for legged robot motion imitation from casual videos,” _IEEE Robotics and Automation Letters_ , 2023. 

- [12] A. Di Fava, K. Bouyarmane, K. Chappellet, E. Ruffaldi, and A. Kheddar, “Multi-contact motion retargeting from human to humanoid robot,” in _2016 IEEE-RAS 16th international conference on humanoid robots (humanoids)_ , IEEE, 2016, pp. 1081–1086. 

- [13] K. Otani and K. Bouyarmane, “Adaptive whole-body manipulation in human-to-humanoid multi-contact motion retargeting,” in _2017 IEEE-RAS 17th International Conference on Humanoid Robotics (Humanoids)_ , IEEE, 2017, pp. 446–453. 

- [14] J. Ramos and S. Kim, “Dynamic locomotion synchronization of bipedal robot and human operator via bilateral feedback teleoperation,” _Science Robotics_ , vol. 4, no. 35, eaav4282, 2019. 

- [15] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [16] J. Won, D. Gopinath, and J. Hodgins, “A scalable approach to control diverse behaviors for physically simulated characters,” _ACM Transactions on Graphics (TOG)_ , vol. 39, no. 4, pp. 33–1, 2020. 

- [17] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler, “Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters,” _ACM Transactions On Graphics (TOG)_ , vol. 41, no. 4, pp. 1–17, 2022. 

- [18] Z. Luo, J. Cao, AlexanderWinkler, K. Kitani, and W. Xu, “Perpetual humanoid control for real-time simulated avatars,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , Oct. 2023, pp. 10 895–10 904. 

- [19] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _arXiv preprint arXiv:2401.16889_ , 2024. 

- [20] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Learning humanoid locomotion with transformers,” _arXiv preprint arXiv:2303.03381_ , 2023. 

- [21] J. Siekmann, K. Green, J. Warila, A. Fern, and J. Hurst, “Blind bipedal stair traversal via sim-to-real reinforcement learning,” _arXiv preprint arXiv:2105.08328_ , 2021. 

- [22] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [23] K. Darvish _et al._ , “Whole-body geometric retargeting for humanoid robots,” in _2019 IEEE-RAS 19th International Conference on Humanoid Robots (Humanoids)_ , IEEE, 2019, pp. 679–686. 

- [24] R. Cisneros-Lim´on _et al._ , “A cybernetic avatar system to embody human telepresence for connectivity, exploration, and skill transfer,” _International Journal of Social Robotics_ , pp. 1–28, 2024. 

- [25] I. Radosavovic _et al._ , “Humanoid locomotion as next token prediction,” _arXiv preprint arXiv:2402.19469_ , 2024. 

- [26] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “Amass: Archive of motion capture as surface shapes,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 5442–5451. 

- [27] J. Li, C. Xu, Z. Chen, S. Bian, L. Yang, and C. Lu, “Hybrik: A hybrid analytical-neural inverse kinematics solution for 3d human pose and shape estimation,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2021, pp. 3383–3393. 

- [28] X. B. Peng, G. Berseth, K. Yin, and M. Van De Panne, “Deeploco: Dynamic locomotion skills using hierarchical deep reinforcement learning,” _ACM Transactions on Graphics (TOG)_ , vol. 36, no. 4, pp. 1–13, 2017. 

- [29] T. Wang, Y. Guo, M. Shugrina, and S. Fidler, “Unicon: Universal neural controller for physics-based character motion,” _arXiv preprint arXiv:2011.15119_ , 2020. 

- [30] L. Fussell, K. Bergamin, and D. Holden, “Supertrack: Motion tracking for physically simulated characters using supervised learning,” _ACM Transactions on Graphics (TOG)_ , vol. 40, no. 6, pp. 1–13, 2021. 

- [31] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [32] Z. Luo _et al._ , “Universal humanoid motion representations for physics-based control,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [33] A. Winkler, J. Won, and Y. Ye, “Questsim: Human motion tracking from sparse sensors with simulated avatars,” in _SIGGRAPH Asia 2022 Conference Papers_ , 2022, pp. 1–8. 

- [34] Z. Luo, R. Hachiuma, Y. Yuan, and K. Kitani, “Dynamics-regulated kinematic policy for egocentric pose estimation,” _Advances in Neural Information Processing Systems_ , vol. 34, pp. 25 019–25 032, 2021. 

- [35] Bullet Physics, _Humanoid urdf in bullet3_ , Accessed: 2024-03-01, 2023. 

- [36] Y. Yuan and K. Kitani, “Residual force control for agile human behavior imitation and extended motion synthesis,” _Advances in Neural Information Processing Systems_ , vol. 33, pp. 21 763–21 774, 2020. 

- [37] L. Penco _et al._ , “Robust real-time whole-body motion retargeting from human to humanoid,” in _2018 IEEERAS 18th International Conference on Humanoid Robots (Humanoids)_ , IEEE, 2018, pp. 425–432. 

- [38] J. Koenemann, F. Burget, and M. Bennewitz, “Realtime imitation of human whole-body motions by humanoids,” in _2014 IEEE International Conference on Robotics and Automation (ICRA)_ , IEEE, 2014, pp. 2806–2812. 

- [39] O. E. Ramos, N. Mansard, O. Stasse, C. Benazeth, S. Hak, and L. Saab, “Dancing humanoid robots: Systematic use of osid to compute dynamically consistent movements following a motion capture pattern,” _IEEE Robotics & Automation Magazine_ , vol. 22, no. 4, pp. 16–26, 2015. 

- [40] L. Penco _et al._ , “Mixed reality teleoperation assistance for direct control of humanoids,” _IEEE Robotics and Automation Letters_ , 2024. 

- [41] K. Ayusawa and E. Yoshida, “Motion retargeting for humanoid robots based on simultaneous morphing parameter identification and motion optimization,” _IEEE Transactions on Robotics_ , vol. 33, no. 6, pp. 1343– 1357, 2017. 

- [42] K. Hu, C. Ott, and D. Lee, “Online human walking imitation in task and joint space based on quadratic programming,” in _2014 IEEE International Conference on Robotics and Automation (ICRA)_ , IEEE, 2014, pp. 3458–3464. 

- [43] S. Bohez _et al._ , “Imitate and repurpose: Learning reusable robot movement skills from human and animal behaviors,” _arXiv preprint arXiv:2203.17138_ , 2022. 

- [44] A. Tang _et al._ , “Humanmimic: Learning natural locomotion and transitions for humanoid robot via wasserstein adversarial imitation,” _arXiv preprint arXiv:2309.14225_ , 2023. 

- [45] M. Seo _et al._ , “Deep imitation learning for humanoid loco-manipulation through human teleoperation,” in _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , IEEE, 2023, pp. 1–8. 

- [46] S. Dafarra _et al._ , “Icub3 avatar system: Enabling remote fully immersive embodiment of humanoid robots,” _Science Robotics_ , vol. 9, no. 86, eadh3834, 2024. 

- [47] J. Chagas Vaz, D. Wallace, and P. Y. Oh, “Humanoid loco-manipulation of pushed carts utilizing virtual reality teleoperation,” in _ASME International Mechanical Engineering Congress and Exposition_ , American Society of Mechanical Engineers, vol. 85628, 2021, V07BT07A027. 

- [48] M. Elobaid, Y. Hu, G. Romualdi, S. Dafarra, J. Babic, and D. Pucci, “Telexistence and teleoperation for walking humanoid robots,” in _Intelligent Systems and Applications: Proceedings of the 2019 Intelligent Systems Conference (IntelliSys) Volume 2_ , Springer, 2020, pp. 1106–1121. 

- [49] S. Tachi, Y. Inoue, and F. Kato, “Telesar vi: Telexistence surrogate anthropomorphic robot vi,” _International Journal of Humanoid Robotics_ , vol. 17, no. 05, p. 2 050 019, 2020. 

- [50] C. D. Bellicoso _et al._ , “Alma-articulated locomotion and manipulation for a torque-controllable robot,” in _2019 International conference on robotics and automation (ICRA)_ , IEEE, 2019, pp. 8477–8483. 

- [51] C. Lenz _et al._ , “Nimbro wins ana avatar xprize immersive telepresence competition: Human-centric evaluation and lessons learned,” _International Journal of Social Robotics_ , pp. 1–25, 2023. 

- [52] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _CoRR_ , vol. abs/1707.06347, 2017. arXiv: 1707.06347. 

- [53] M. Loper, N. Mahmood, J. Romero, G. Pons-Moll, and M. J. Black, “SMPL: A skinned multi-person linear model,” _ACM Trans. Graphics (Proc. SIGGRAPH Asia)_ , vol. 34, no. 6, 248:1–248:16, Oct. 2015. 

- [54] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” _arXiv preprint arXiv:1412.6980_ , 2014. 

- [55] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, _Learning to walk in minutes using massively parallel deep reinforcement learning_ , 2022. arXiv: 2109.11978 [cs.RO]. 

- [56] L. Campanaro, S. Gangapurwala, W. Merkt, and I. Havoutis, _Learning and deploying robust locomotion policies with minimal dynamics randomization_ , 2023. arXiv: 2209.12878 [cs.RO]. 

- [57] T. He, C. Zhang, W. Xiao, G. He, C. Liu, and G. Shi, _Agile but safe: Learning collision-free highspeed legged locomotion_ , 2024. arXiv: 2401.17583 [cs.RO]. 

- [58] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Sim-to-real transfer of robotic control with dynamics randomization,” in _2018 IEEE international conference on robotics and automation (ICRA)_ , IEEE, 2018, pp. 3803–3810. 

- [59] F. Yang, C. Ma, J. Zhang, J. Zhu, W. Yuan, and A. Owens, “Touch and go: Learning from human-collected vision and touch,” _arXiv preprint arXiv:2211.12498_ , 2022. 

- [60] J. Y. Chai, Q. Gao, L. She, S. Yang, S. Saba-Sadiya, and G. Xu, “Language to action: Towards interactive task learning with physical agents.,” in _IJCAI_ , 2018, pp. 2–9. 

