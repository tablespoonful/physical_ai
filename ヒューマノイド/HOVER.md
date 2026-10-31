---
title: "HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots"
date: "2024-10-28"
authors: "Tairan He; Wenli Xiao; Toru Lin; Zhengyi Luo; Zhenjia Xu; Zhenyu Jiang"
venue: "ICRA 2025"
url: https://arxiv.org/abs/2410.21229
pdf: https://arxiv.org/pdf/2410.21229
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2410.21229)** / [論文ページ](https://arxiv.org/abs/2410.21229)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots** 

Tairan He<sup>_∗_1</sup><sup>_,_2</sup> Wenli Xiao<sup>_∗_1</sup><sup>_,_2</sup> Toru Lin<sup>1</sup><sup>_,_3</sup> Zhengyi Luo<sup>1</sup><sup>_,_2</sup> Zhenjia Xu<sup>1</sup> Zhenyu Jiang<sup>1</sup><sup>_,_4</sup> Jan Kautz<sup>1</sup> Changliu Liu<sup>2</sup> Guanya Shi<sup>2</sup> Xiaolong Wang<sup>1</sup><sup>_,_5</sup> Linxi “Jim” Fan<sup>_†_1</sup> Yuke Zhu<sup>_†_1</sup><sup>_,_4</sup> 

**_Abstract_ — Humanoid whole-body control requires adapting to diverse tasks such as navigation, loco-manipulation, and tabletop manipulation, each demanding a different mode of control. For example, navigation relies on root velocity or position tracking, while tabletop manipulation prioritizes upperbody joint angle tracking. Existing approaches typically train individual policies tailored to a specific command space, limiting their transferability across modes. We present the key insight that full-body kinematic motion imitation can serve as a common abstraction for all these tasks and provide generalpurpose motor skills for learning multiple modes of whole-body control. Building on this, we propose HOVER (Humanoid Versatile Controller), a multi-mode policy distillation framework that consolidates diverse control modes into a unified policy. HOVER enables seamless transitions between control modes while preserving the distinct advantages of each, offering a robust and scalable solution for humanoid control across a wide range of modes. By eliminating the need for policy retraining for each control mode, our approach improves efficiency and flexibility for future humanoid applications.** 

# I. INTRODUCTION 

Humanoid is a versatile form factor that supports a wide variety of robotic tasks and applications, including bimanual manipulation [1–3], bipedal locomotion [4–7], and agile whole-body control [8–14]. While showing impressive results, each of these efforts uses a different formulation for whole-body control based on the need for their specific task and scenario. Some use root velocity tracking [5, 6] to support locomotion, some choose joint angle tracking [12, 13] to enable expressive movements, and others use kinematic tracking of selected body keypoints [9, 10] to support teleoperation. Although these approaches are similar in terms of the end goal of motion tracking, they require task-specific controller interface and rewards design. This not only makes the development process repetitive and timeconsuming, but also limits the versatility of the resultant whole-body controller. For instance, a robot performing bipedal locomotion on uneven terrain using root velocity tracking [5, 6] would struggle to seamlessly switch to a task requiring precise bimanual manipulation, where joint angle or end-effector tracking [2, 12, 13] might be necessary. These task-specific dependencies limit versatility, as each controller is restricted to a single mode of control. In addition to motion tracking, many pretrained manipulation policies [15, 16] require operating in different configuration spaces, such as joint angles and end-effector positions. This variability highlights 

> *Equal Contributions, _†_ GEAR Team Leads 

> 1NVIDIA, 2CMU, 3UC Berkeley, 4UT Austin, 5UC San Diego Paper website: https://hover-versatile-humanoid.github.io 


Fig. 1: HOVER enables versatile humanoid control with a unified multi-mode command space. The versatile multi-mode command space supports **kinematic position tracking (blue)** , **local joint angle tracking (yellow)** , and **root tracking (purple)** . Highlighted boxes indicate active commands being tracked, while the masks (dashed boxes on the right) allow selective activation of different command spaces to accommodate various tasks. 

the need for a unified low-level humanoid controller capable of adapting to diverse control mode configurations. 

Since all these modes are applied to a shared hardware platform, a natural question arises: _Can we create a unified controller that supports all control modes, combining the strengths of each?_ This is a non-trivial challenge, as each mode operates within a distinct command space, making direct integration impractical. However, despite differences in control interfaces, the underlying motion objectives often align: stable, human-like motion for humanoid control. 

To this end, we present HOVER, a unified neural controller for humanoid whole-body control that supports diverse control modes as shown in Figure 1, including over 15 useful modes for real-world applications to a 19-DOF humanoid robot. This versatile command space covers most modes used in prior works [9, 10, 12, 13]. To ensure a robust foundation of motor skills that generalize well across tasks, we train an oracle motion imitator to mimic large-scale human motion data from MoCap [17], covering a wide variety 


Fig. 2: **Overview of HOVER distillation process.** The **HOVER policy** is distilled from the **Oracle policy** through proprioception and command masking. The task commands for the student are determined via _mode-specific_ and _sparsity-based_ masks, applied to both upper and lower body motions independently. These masks generate diverse task command modes, refining the student’s inputs. The distillation employs DAgger to align the student’s actions with those of the oracle, optimizing through supervised learning on the oracle’s actions. 

of movements and control objectives. This design choice leverages the inherent adaptability and natural efficiency of human movements, providing the policy with rich motor priors that can be reused across multiple control modes. By grounding the training process in human-like motion, the policy gains a deeper understanding of balance, coordination, and motion control, which are crucial for effective whole-body humanoid behavior. Through a policy distillation process, we transfer these motor skills from the oracle policy into a single “generalist policy” capable of handling multiple control modes. The resulting multi-mode policy not only supports diverse control modes but also _outperforms_ policies trained individually for each mode as shown in Figure 3. We hypothesize that this is due to the policy leveraging shared physical knowledge across modes, such as maintaining balance, human-like motion, and precise limb control. These shared skills enhance generalization, leading to better performance across all modes. In contrast, singlemode policies often overfit to specific reward structures and training environments, limiting their adaptability. Our multimode generalist policy also enables seamless transitions between modes, making it both robust and versatile. 

To summarize, our contributions are threefold: 1) we present HOVER, a unified neural controller for humanoid whole-body control supporting multiple control modes; 2) we show that, through policy distillation, HOVER effectively shares motor skills across modes and outperforms individually trained policies; and 3) experiments in both simulation and on a real humanoid robot demonstrate that HOVER achieves seamless transitions between modes and delivers superior multi-mode control compared to other baselines. 

# II. METHOD 

# _A. Goal-Conditioned RL for Humanoid Control_ 

We formulate our problem as a goal-conditioned reinforcement learning (RL) task, where the policy _π_ is trained to track real-time human motion. The state **_s_** _t_ comprises both the agent’s proprioception **_s_**<sup>p</sup> _t_<sup>andthetargetgoalstate</sup> **_s_**<sup>g</sup> _t_<sup>.Thegoalstate</sup><sup>**_s_**g</sup> _t_<sup>providesaunifiedrepresentationof</sup> the target motion goal, which we will describe in detail in Section II-B. Using the agent’s proprioception **_s_**<sup>p</sup> _t_<sup>andthe</sup> goal state **_s_**<sup>g</sup> _t_<sup>, we define the reward</sup><sup>_rt_=</sup><sup>_R_</sup> � **_s_**<sup>p</sup> _t_<sup>_,_</sup><sup>**_s_**g</sup> _t_ � for policy optimization. The action **_a_** _t ∈_ R<sup>19</sup> represents the target joint 


Fig. 3: Comparison between **prior work specialists (blue)** and our **generalist policy (green)** under corresponding modes. The metrics used are: upper/lower joint error (rad), global/local body position error (mm), root velocity error (m/s), and root rotation error (rad). These metrics evaluate how accurately each policy tracks reference motions and joint configurations across different control modes. The modes being tracked (activated) by each mode are colored **blue** . 

positions, which are fed into the PD controller to actuate the robot’s degrees of freedom. We employ the proximal policy optimization (PPO) algorithm [18] to maximize the cumulative discounted reward E _t_ =1<sup>_γt−_1</sup><sup>_rt_</sup> . This setup �� _T_ � is framed as a command-tracking task, where the humanoid learns to follow the target commands at each timestep. 

# _B. Command Space Design for Humanoid Control_ 

In legged locomotion, root velocity [19] or position tracking [20] is a commonly employed command space. However, focusing solely on root tracking imposes limitations on the full capabilities of humanoid robots, especially for wholebody loco-manipulation tasks. We observe that while prior works [9, 10, 12, 13] have introduced control modes with varying advantages and disadvantages, each is typically tailored to specific subsets of tasks, thus lacking the flexibility required for general-purpose humanoid control. In contrast, our goal is to design a comprehensive control framework that 

TABLE I: Command space for priors works on whole-body humanoid control. HOVER covers all the command designs designed by prior works with a unified command space and supports multi-mode control by tracking arbitrary subsets of the command elements. 

|Controller|Multi-Mode Control|Uppe|r-Body Command|Lower-Body|Command||
|---|---|---|---|---|---|---|
|||Kinematic|Position<br>Joint Angle|Kinematic Position|Joint Angl|e<br>Root|
|ExBody [12]|✗|✗|✓|✗|✗|✓|
|H2O [10]|✗|✓|✗|✓|✗|✗|
|OmniH2O [9]|✗|✓|✗|✗|✗|✗|
|HumanPlus [13]|✗|✗|✓|✗|✓|✓|
|MHC [21]|✓|✗|✓|✗|✓|✓|
|HOVER (ours)|✓|✓|✓|✓|✓|✓|


accommodates a wide range of scenarios and is adaptable to various humanoid tasks. To achieve this, the command space must be constructed to satisfy the following key criteria: 

- **Generality** : The command space should encompass most existing configurations, allowing a generalpurpose controller to replace task-specific controllers without sacrificing performance or versatility. And the space should be sufficiently expressive to interface with real-world control devices, including joysticks, keyboards, motion capture systems, exoskeletons, and virtual reality (VR) headsets as shown in Figure 1. 

- **Atomicity** : The command space should be composed of independent dimensions, enabling arbitrary combinations of control options to support various modes. 

Based on these criteria, we define a unified command space for humanoid whole-body control. This space consists of two primary control regions—upper-body and lower-body control—and incorporates three distinct control modes: 

- **Kinematic Position Tracking** : target 3D positions of key rigid body points on the robot. 

- **Local Joint Angle Tracking** : target joint angles for each robot motor. 

- **Root Tracking** : target root velocity, height, and orientation, specified by roll, pitch, and yaw angles. 

In our framework, as shown in Figure 1, a one-hot masking vector is introduced to specify which components of the command space are activated for tracking. Recent work on learning-based humanoid whole-body control [9, 10, 12, 13], as shown in Table I can be viewed as subsets of our unified command space, each representing specific configurations. 

# _C. Motion Retargeting_ 

Recent works have shown the advantage of learning robust whole-body control for humanoid robots from large motion datasets [9, 10, 12, 13]. The retargeting procedure from human motion dataset [17] to humanoid motion dataset has three steps: **Step-1** : We first compute the keypoints positions of the humanoid using forward kinematics, mapping its joint configurations to workspace coordinates. **Step-2** : Next, we fit the SMPL model to match the humanoid’s kinematics by optimizing the SMPL parameters to align with the computed keypoints from forward kinematics. **Step-3** : Finally, the AMASS dataset is retargeted by matching corresponding keypoints between the fitted SMPL model and the humanoid with gradient descent. We follow the same motion retargeting 

TABLE II: Reward designs for the oracle policy. 

|Term|Weight|Term|Weight|
|---|---|---|---|
|||Penalty||
|Torque limits<br>Termination|_−_2<br>_−_2_._5_e_<sup>2</sup>|DoF position limits<br>DoF velocity limits|_−_1_._25_e_<sup>2</sup><br>_−_5_e_<sup>1</sup>|
||Re|gularization||
|DoF acceleration|_−_1_._1_e_<sup>_−_5</sup>|DoF velocity|_−_4_e_<sup>_−_3</sup>|
|Lower Action rate|_−_3|Upper Action rate|_−_6_._25_e_<sup>_−_1</sup>|
|Torque|_−_1_e_<sup>_−_4</sup>|Feet orientation|_−_6_._25_e_<sup>1</sup>|
|Feet air time|1_e_<sup>3</sup>|Feet contact force|_−_7_._5_e_<sup>_−_1</sup>|
|Stumble|_−_1_._25_e_<sup>3</sup>|Slippage|_−_7_._5_e_<sup>1</sup>|
|In the air|_−_2_e_<sup>2</sup>|Max feet height per step|_−_3_e_<sup>3</sup>|
||Ta|sk Reward||
|DoF position|3_._2_e_<sup>1</sup>|DoF velocity|1_._6_e_<sup>1</sup>|
|Body position|8_e_<sup>1</sup>|Body rotation|2_e_<sup>1</sup>|
|Body velocity|8|Body angular velocity|8|
|Root velocity|1_e_<sup>2</sup>|Root rotation|2_e_<sup>1</sup>|


and “sim-to-data” procedure with [10] to convert the largescale human motion dataset [17] to dataset _Q_<sup>ˆ</sup> that only contains feasible motions for humanoids. 

_D. Oracle Policy Training from Large-Scale Human Motions_ 

**State Space Design** . We train an oracle motion imitator _π_<sup>oracle</sup> ( _at|s_<sup>p-oracle</sup> _t , s_<sup>g-oracle</sup> _t_ ). The proprioception is defined as _s_<sup>p-oracle</sup> _t_ ≜ [ **_p_** _t,_ **_θ_** _t, p_ ˙ _t,_ **_ω_** _t,_ **_a_** _t−_ 1], which contains the humanoid rigid-body position **_p_** _t_ , orientation **_θ_** _t_ , linear velocity _p_ ˙ _t_ , angular velocity **_ω_** _t_ , and the previous action **_a_** _t−_ 1. The goal state is defined as _s_<sup>g-oracle</sup> _t_ ≜ [ **_θ_**<sup>**ˆ**</sup> _t_ +1 _⊖_ **_θ_** _t,_ **ˆ** **_p_** _t_ +1 _−_ **_p_** _t,_ **ˆ** **_v_** _t_ +1 _−_ **_v_** _t,_ **ˆ** **_ω_** _t_ +1 _−_ **_ω_** _t,_ **_θ_**<sup>**ˆ**</sup> **_t_** _,_ **ˆ** **_pt_** ], which contains the reference pose ( **_θ_**<sup>**ˆ**</sup> _t,_ **ˆ** **_p_** _t_ ) and one-frame difference between the reference and current state for all rigid bodies of the humanoid. We use the same policy network structure with [9], a three-layer MLP with layer dimensions of [512 _,_ 256 _,_ 128]. 

**Reward Design and Domain Randomizations** . We formulate the reward _rt_ as the sum of three components: 1) penalty, 2) regularization, and 3) task rewards, detailed in Table II. We follow the same domain randomization in [9] to randomize the physical parameters of the simulated environment and humanoids for successful sim-to-real transfer. 

_E. Multi-Mode Versatile Controller via Distillation_ 

**Proprioception** . For the student policy _π_<sup>student</sup> ( _s_<sup>p-student</sup> _t , s_<sup>g-student</sup> _t_ ) distilled from the oracle teacher _π_<sup>oracle</sup> , the proprioception is defined as _s_<sup>p-student</sup> _t_ ≜ [ _q, q, ω_ ˙<sup>base</sup> _, g_ ] _t−_ 25: _t ∪_ [ _at−_ 25: _t−_ 1], where _q_ is the joint position, _q_ ˙ is the joint velocity, _ω_<sup>base</sup> is the base angular velocity, _g_ is the gravity vector, and _a_ is the action history. Following [9], we stack these terms over the last 25 steps to represent the student’s proprioceptive input. 

**Command Mask** . As illustrated in Figure 2, the task command input for the student policy is defined using modebased and sparsity-based masking. Specifically, the student’s 

TABLE III: Simulation motion imitation evaluation of HOVER and baselines on dataset _Q_<sup>ˆ</sup> . Metrics that are tracked by different modes are highlighted in corresponding colors. Results that are statistically significant are highlighted in bold across 5 random seeds. 

|||**Kine**|**matic Positi**|**on**|**Joint Angle**|||**Root**|||
|---|---|---|---|---|---|---|---|---|---|---|
|Method|Survive_↑_|_E_g-mpjpe _↓_|_E_mpjpe _↓_|Eacc _↓_<br>Evel _↓_|_E_upper-j _↓_<br>_E_lower-j _↓_|_E_root-vel _↓_|_E_root-h _↓_|_E_root-r _↓_|_E_root-p _↓_|_E_root-y _↓_|
|Oracle policy|99.3%_±_0.203|119_±_0.442|59.4_±_0.234|2.63_±_0.008 5.43_±_0.024|0.153_±_0.001 0.206_±_0.001|0.456_±_0.002|0.066_±_0.001|0.065_±_0.001|0.083_±_0.001|0.282_±_0.002|
|**ExBody Mode** - Upper:|joint angle tra|cking, Low|er: root trac|king|||||||
|ExBody (Specialist)<br>HOVER (Ours)|99.1%_±_0.212<br>99.1%_±_0.220|275_±_1.650<br>**185**_±_**1.110**|83.1_±_0.499 <br>**63.9**_±_**0.384**|**2.63**_±_**0.007** 6.31_±_0.034<br> 3.01_±_0.009 **6.06**_±_**0.033**|0.166_±_0.002 0.243_±_0.003<br>**0.148**_±_**0.002 0.210**_±_**0.004**|**0.428**_±_**0.007**<br>0.452_±_0.006|0.074_±_0.001<br>**0.063**_±_**0.001**|0.070_±_0.001<br>0.068_±_0.001|0.147_±_0.002<br>**0.091**_±_**0.001**|0.276_±_0.003<br>0.279_±_0.002|
|**HumanPlus Mode**- Upp|er: joint angle|tracking, L|ower: joint|angle tracking, root tra|cking||||||
|HumanPlus (Specialist)<br>HOVER (Ours)|98.4%_±_0.259<br>98.9%_±_0.285|266_±_1.597<br>**182**_±_**1.093**|80.1_±_0.481 <br>**64.5**_±_**0.387**|**2.53**_±_**0.007** 6.16_±_0.033<br> 2.85_±_0.008 **5.91**_±_**0.032**|0.177_±_0.002<br>0.222_±_0.002<br>**0.145**_±_**0.001**<br>**0.211**_±_**0.002**|**0.422**_±_**0.006**<br>0.455_±_0.007|**0.061**_±_**0.001**<br>0.067_±_0.001|0.080_±_0.001<br>**0.069**_±_**0.001**|0.124_±_0.001<br>**0.104**_±_**0.001**|0.228_±_0.002<br>0.237_±_0.002|
|**H2O Mode** - Upper: kin|ematic positio|n tracking (|left/right ha|nd, left/right shoulder,|left/right elbow), Lower:|kinematic po|sition trackin|g (left/right|ankle)||
|H2O (Specialist)<br>HOVER (Ours)|99.2%_±_0.233<br>98.9%_±_0.276|137_±_0.827<br>**121**_±_**0.726**|66.3_±_0.398<br>**60.6**_±_**0.361**|**2.63**_±_**0.008**<br>5.75_±_0.028 <br>2.73_±_0.008<br>**5.49**_±_**0.028 **|0.177_±_0.003 0.221_±_0.002 <br> **0.158**_±_**0.002 0.207**_±_**0.002**|0.457_±_0.004 <br> 0.456_±_0.005|0.078_±_0.001 <br> **0.065**_±_**0.001**|0.067_±_0.001 <br> 0.067_±_0.001|0.095_±_0.001<br> **0.086**_±_**0.001**|0.415_±_0.003<br>**0.365**_±_**0.003**|
|**OmniH2O Mode** - Upp|er: kinematic p|osition trac|king (head,|left/right hand), Lower|: N/A||||||
|OmniH2O (Specialist)<br>HOVER (Ours)|99.0%_±_0.301<br>99.0%_±_0.297|149_±_0.897<br>**128**_±_**0.768**|76.4_±_0.459<br>**62.5**_±_**0.368**|2.69_±_0.007<br>6.18_±_0.037 <br>2.69_±_0.008<br>**5.65**_±_**0.032 **|0.199_±_0.002 0.232_±_0.003 <br> **0.162**_±_**0.002 0.213**_±_**0.002**|0.456_±_0.002 <br> 0.457_±_0.004|0.071_±_0.001 <br> **0.065**_±_**0.001**|0.070_±_0.001 <br> 0.068_±_0.001|0.125_±_0.002<br> **0.089**_±_**0.001**|**0.306**_±_**0.002**<br>0.310_±_0.002|


task command input, _s_<sup>g-student</sup> _t_ , is represented as _s_<sup>g-student</sup> _t_ ≜ _M_ sparsity _⊙ M_ mode _⊙ s_<sup>g-upper</sup> _t , M_ mode _⊙ s_<sup>g-lower</sup> _t_ . The mode � � mask, _M_ mode, selects a specific task command mode for the upper and lower body independently. For instance, the upper body may track kinematic positions, while the lower body focuses on joint angle and root tracking, as shown in Figure 2. After the mode-specific masking, the sparsity mask, _M_ sparsity, is applied. For example, in some scenarios, the upper body may track only the kinematic positions of the hands, while the lower body tracks only the joint angles of the torso. Every bit of the mode and sparsity binary mask is from a Bernoulli distribution _B_ (0 _._ 5). Mode and sparsity masks are randomized at the episode beginning and remain fixed until the episode ends 

**Policy Distillation** . We perform policy distillation using the DAgger framework [22]. For each episode, we roll out the student policy _π_<sup>student</sup> ( **a** _t|s_<sup>p-student</sup> _t , s_<sup>g-student</sup> _t_ ) in simulation to obtain trajectories of ( _s_<sup>p-student</sup> _t , s_<sup>g-student</sup> _t_ ). At each timestep, we also compute the corresponding oracle states ( _s_<sup>p-oracle</sup> _t , s_<sup>g-oracle</sup> _t_ ). Using these oracle states, we query the oracle teacher policy _π_<sup>oracle</sup> (ˆ **a** _t|s_<sup>p-oracle</sup> _t , s_<sup>g-oracle</sup> _t_ ) to obtain the reference action ˆ **a** _t_ . The student policy _π_<sup>student</sup> is then updated by minimizing the loss function: _L_ = _∥_ **a** ˆ _t −_ **a** _t∥_ 2<sup>2</sup><sup>_,_where</sup><sup>**a**ˆ</sup><sup>_t_</sup> is the reference action from the oracle, and **a** _t_ is the action taken by the student policy. 

# III. EXPERIMENT 

In this section, we present extensive experimental results in both IsaacGym [23] and the real-world Unitree H1 [24] robot to address the following questions: 

- **Q1** : Can HOVER as a generalist policy outperform policies trained for a specific command configuration? 

- **Q2** : Can HOVER outperform other methods of training a multi-mode humanoid controller? 

- **Q3** : Can HOVER transfer to real-world hardware and execute versatile multi-mode control? 

**Experiment Setup** . To answer these questions, we evaluate 

HOVER on motion tracking in both simulation (Section III-A and Section III-B) and real-world settings (Section III-C). In simulation, we evaluate using the retargeted AMASS dataset _Q_ ˆ. In the real world, we test 20 standing motion sequences focusing on quantitative tracking and locomotion tasks for qualitative multi-mode control. Our real robot employs a 19DOF Unitree H1 platform [24] with a total mass of around 51.5kg and a height of around 1.8m. 

**Baselines** . To address **Q1** and **Q3** , we compare HOVER with several specialists. As shown in Table I, ExBody [12] focuses on tracking upper body joint angles and root velocity, HumanPlus [13] tracks whole-body joints and root velocity, H2O [10] tracks the kinematic positions of eight keypoints (shoulders, elbows, hands, ankles), and OmniH2O [9] tracks the kinematic positions of the head and both hands. We also compare other useful tracking modes (e.g., left-hand mode, right-hand mode, two-hand mode, head mode). For each control mode, we provide only the relevant observation input to the controller and train the specialist baseline with RL. For instance, in left-hand-only mode, only reference motion of the left hand is provided. To address **Q2** , we compare with another multi-mode RL policy, which follows the same masking process on the goal commands, but trains the baseline with RL objective from scratch. During the multi-mode RL baseline training, mode and sparsity are randomized at the beginning of each episode and remain fixed until the episode ends, which is the same as the randomized masking process during distillation. 

**Metrics** . We report survival rate, where the episode terminates if the humanoid hits the ground, not by feet. We calculate tracking error in terms of kinematic pose, joint angles, and root twist and rotations. The mean values of the metrics are computed across all motion sequences from dataset _Q_<sup>ˆ</sup> . We evaluate policy’s ability to imitate the reference motion by compare the tracking error of the global body position _Eg−_ mpjpe (mm), the root-relative mean perjoint (MPJPE) _E_ mpjpe (mm), joint tracking error _Ej_ (rad), 

TABLE IV: Comparison between HOVER and specialists. We only report tracking metrics that are tracked by this mode. 

|Method|_E_g-mpjpe-mode _↓_|_E_mpjpe-mode _↓_|_E_acc-mode _↓_|_E_vel-mode _↓_|
|---|---|---|---|---|
|**Left Hand Mod**|**e** - Upper: kine|matic position|tracking (left ha|nd), Lower: N/A|
|Specialist|189_±_1.526|**147**_±_**1.324**|5.82_±_0.029|11.2_±_0.089|
|HOVER (Ours)|**138**_±_**1.025**|151_±_0.934|**5.45**_±_**0.031**|**10.3**_±_**0.104**|
|**Right Hand Mo**|**de** - Upper: kin|ematic position|tracking (right|hand), Lower: N/A|
|Specialist<br>HOVER (Ours)|220_±_1.345<br>**128**_±_**0.774**|216_±_1.451<br>**141**_±_**0.821**|6.77_±_0.051<br>**5.83**_±_**0.049**|12.5_±_0.152<br>**10.8**_±_**0.129**|
|**2 Hands Mode**|- Upper: kinem|atic position tra|cking (left-right|hands), Lower: N/A|
|Specialist|137_±_0.998|145_±_1.010|5.72_±_0.037|11.2_±_0.004|
|HOVER (Ours)|**120**_±_**0.901**|**119**_±_**0.827**|**5.60**_±_**0.045**|**10.1**_±_**0.134**|
|**Head Mode** - U|pper: kinematic|position tracki|ng (robot head),|Lower: N/A|
|Specialist|186_±_1.149|104_±_0.814|**2.22**_±_**0.008**|6.63_±_0.065|
|HOVER (Ours)|**133**_±_**0.849**|**80.0**_±_**0.711**|2.31_±_0.011|**6.40**_±_**0.029**|


root velocity _E_ root-vel (m/s), and root orientation tracking error _E_ root-rpy (rad). To show physical realism, we report average joint acceleration _E_ acc (mm/frame<sup>2</sup> ), and velocity _E_ vel (mm/frame) error. To better show the correspondence between control modes and metrics, we highlight the metrics that are actively tracked by each mode with corresponding colors in Table III, Table IV and Table V. For instance, in Table III, upper joint and root metrics are colored with corresponding mode for ExBody mode. 

# _A. Comparison with Specialists_ 

**Comparison with Specialists of Prior Work’s Control Mode** . To address **Q1** ( _Can HOVER as a generalist policy outperform policies trained for a specific command configuration?_ ), we compare the performance of the same HOVER policy across different control modes against the corresponding specialist policies. For example, the performance of HOVER under ExBody mode is evaluated with a fixed mask to match ExBody mode across the entire dataset _Q_<sup>ˆ</sup> . As shown in Table III and Figure 3, HOVER consistently demonstrates superior generalization. In every command mode, HOVER outperforms prior work specialist controllers in at least 7 out of the 12 metrics, as highlighted by the bold values in Table III. This consistent advantage across various control modes underscores the versatility of HOVER. Furthermore, this means that even when focusing on a single control mode without considering multi-mode versatility, distilling from an oracle policy still surpasses RL-trained specialists. 

**Comparison with Other Specialists of Other Useful Con-** 

**trol Mode** . In addition to the aforementioned baselines, we also evaluate four additional modes: left-hand mode, righthand mode, two-hand mode, and head mode. We train four RL specialists to track these modes individually. The results in Table IV show that HOVER consistently outperforms specialists in terms of tracking metrics that are trained for specific command configurations. 

# _B. Comparison with Other Generalist Training Methods._ 

To address **Q2** ( _does HOVER outperform other methods of training a multi-mode humanoid controller?_ ), we compare HOVER with a multi-mode RL baseline that follows the 


Fig. 4: We assess the tracking accuracy of two multi-mode control policies— **HOVER (green)** and **Multi-Mode RL (purple)** —across eight distinct humanoid control modes. The comparison is visualized across four key performance metrics in the radar charts. 

same masking process on the commands but trains with RL objective from scratch. In Figure 4, we assess tracking error across four metrics: root orientation, upper joint angle, and local and global body positions, measured in eight different modes. We scale the tracking error via _E_<sup>_<u>E</u>_maxmax</sup> _−_<sup>_−_</sup> _E_<sup>_<u>E</u>_min(</sup><sup>_._)for</sup> visualization, where larger radar webs indicate better tracking performance. The results show that HOVER achieves consistently lower tracking error across 32/32 metrics and modes. This performance boost underscores the importance of distilling from an oracle policy that tracks full-body kinematics for learning a generalist whole-body controller. 

# _C. Real-World Evaluation_ 

To address **Q3** ( _does HOVER transfer to real-world hardware and execute versatile multi-mode control?_ ), we conduct quantitative tracking experiments and locomotion tests for qualitative multi-mode control. 

**Standing Motion Evaluations** . We evaluate HOVER’s performance in the real world by tracking 20 different standing motions in _Q_<sup>ˆ</sup> . Among these, two motions are visually illustrated in Figure 5 (left). The quantitative metrics presented in Table V demonstrate HOVER outperforms specialist policies in 11 out of 12 metrics. Moreover, we demonstrate successful tracking of root pitch motion, as shown in the middle of Figure 5, and full-body kinematic tracking, as shown on the right of Figure 5, where the robot is capable of tracking highly dynamic running motions. 

**Multi-Mode Evaluations** . We also evaluate HOVER’s generalization to locomotion in Figure 6, where we abruptly switch command modes during operation to simulate reallife scenarios. HOVER successfully transitions from ExBody mode to H2O mode during forward walking in Figure 6(a), and from HumanPlus mode to OmniH2O mode while performing turning and backward walking, in Figure 6(b). 

TABLE V: Real-world tracking evaluation on 20 standing motions between prior works specialists and our method. Results that are statistically significant are highlighted in bold across 5 tests. 


Fig. 5: Real-World Evaluations on different control modes. 

Additionally, we conduct a real-test teleoperation demo with Vision Pro, randomly masking out the positions of the head and hands. For example, in the middle of Figure 6(c), the humanoid tracks only the human’s head position, ignoring the waving hands in _head mode_ . The results demonstrate that HOVER can smoothly track motions across different modes, showcasing its robustness for real-world scenarios (e.g., when there are occlusions in the reference motions). 

# IV. RELATED WORK 

**Humanoid Whole-Body Controller** . Performing wholebody control on humanoid hardware is a long-standing challenge in robotics due to the complex structure of humanoid robots. Before the rise in popularity of learning-based controllers, classical humanoid controllers [25–34] often use a hierarchical model-based optimization to solve for the low-level torque or position commands sent to hardware motors, where actuator-level dynamics on single joints are abstracted to multi-joint [27] or whole-body [28] controllers. Learning-based controllers follow the same design pattern in spirit, where high-level inputs are translated into lowlevel motor commands via neural networks. The design of controller abstraction and task specification varies by user needs and applications [35–37]. Recent works on learningbased humanoid whole-body control [9, 10, 12, 13, 38] generally have three design patterns for humanoid wholebody controller: kinematic motion tracking [9, 10, 38], local joint angle tracking [1, 13], and root velocity tracking [5, 6]. Kinematic motion tracking means tracking the full-body kinematic motion for each rigid body of the humanoid, and is heavily inspired by the motion imitation in the graphics community [39–42]. Local joint angle tracking tracks the local joint angles of the humanoid, which can be considered a specialized case of kinematic motion imitation where global position information is discarded. Root velocity tracking only 


Fig. 6: HOVER shows robustness under control mode switches during locomotion and real-time teleoperation tests. 

serves for locomotion ability, and is used for navigation and terrain traversal of humanoids [5, 6]. One can also combine different control modes for upper and lower body: for instance, the upper body can be controlled with local joint angle tracking and the lower body with velocity tracking [12]. Even within the same kinematic tracking pattern, the sparsity design varies depending on the selected keypoints [9, 10]. So far, each of these control modes is independently developed and are not compatible with each other. In this work, we aim to unify all of these control modes. 

**Unified Neural Whole-Body Controller for Humanoid** . MHC [21, 43] learns multi-mode humanoid controller using RL from retargeted motion, but does not support arbitrary subset of chosen modes and is limited to local joint angles and root tracking. In computer graphics, MaskedMimic [44] enables multi-mode control with flexible kinematic tracking constraint by distillation. Other graphics works leverage reusable motion latent space for downstream flexible control modes [45–47]. However, additional policies need to be trained. In this work, we aim to learn a unified control policy that can be directly used to control real humanoids using different control modes. 

# V. CONCLUSIONS 

In this work, we introduced HOVER, a unified neural controller for humanoid whole-body control that supports diverse control modes. Through the use of a kinematic motion imitator and policy distillation, HOVER consolidates motor skills across multiple control modes into a unified policy that outperforms specialized controllers. Our evaluations collectively illustrate HOVER’s ability to handle diverse real-world control modes, offering and superior performance compared to specialist policies. Future work will explore further developing an automated mode-switching module for real-world applications. 

# ACKNOWLEDGEMENT 

We appreciate Unitree Robotics and Fourier Intelligence for supporting hardware experiments and thank Xue Bin Peng, Chen Tessler, Scott Reed, Viktor Makoviychuk, Yuqi Xie, Avnish Narayan, Zu Wang, Xuxin Cheng, Chong Zhang, Zixuan Chen, and Ziqiao Ma for the insightful discussions. 

# REFERENCES 

- [1] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang, “Open-television: Teleoperation with immersive active visual feedback,” _arXiv preprint arXiv:2407.01512_ , 2024. 

- [2] T. Lin _et al._ , “Learning visuotactile skills with two multifingered hands,” _arXiv preprint arXiv:2404.16823_ , 2024. 

- [3] J. Li _et al._ , “Okami: Teaching humanoid robots manipulation skills through single video imitation,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [4] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, eadi9579, 2024. 

- [5] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _arXiv preprint arXiv:2401.16889_ , 2024. 

- [6] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” _arXiv preprint arXiv:2406.10759_ , 2024. 

- [7] Q. Liao, B. Zhang, X. Huang, X. Huang, Z. Li, and K. Sreenath, “Berkeley humanoid: A research platform for learning-based control,” _arXiv preprint arXiv:2407.21781_ , 2024. 

- [8] Boston Dynamics, _Atlas — partners in parkour_ , https : / / www . youtube . com / watch ? v = tF4DML7FIWk, 2021. 

- [9] T. He _et al._ , “Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning,” _arXiv preprint arXiv:2406.08858_ , 2024. 

- [10] T. He _et al._ , “Learning human-to-humanoid realtime whole-body teleoperation,” _arXiv preprint arXiv:2403.04436_ , 2024. 

- [11] H. Xue, C. Pan, Z. Yi, G. Qu, and G. Shi, “Fullorder sampling-based mpc for torque-level locomotion control via diffusion-style annealing,” _arXiv preprint arXiv:2409.15610_ , 2024. 

- [12] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [13] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

- [14] C. Zhang, W. Xiao, T. He, and G. Shi, “Wococo: Learning whole-body humanoid control with sequential contacts,” _arXiv preprint arXiv:2406.06005_ , 2024. 

- [15] A. Padalkar _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models,” _arXiv preprint arXiv:2310.08864_ , 2023. 

- [16] M. J. Kim _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [17] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “Amass: Archive of motion capture as surface shapes,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 5442–5451. 

- [18] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [19] G. B. Margolis, G. Yang, K. Paigwar, T. Chen, and P. Agrawal, “Rapid locomotion via reinforcement learning,” _The International Journal of Robotics Research_ , vol. 43, no. 4, pp. 572–587, 2024. 

- [20] T. He, C. Zhang, W. Xiao, G. He, C. Liu, and G. Shi, “Agile but safe: Learning collision-free high-speed legged locomotion,” _arXiv preprint arXiv:2401.17583_ , 2024. 

- [21] P. Dugar, A. Shrestha, F. Yu, B. van Marum, and A. Fern, “Learning multi-modal whole-body control for real-world humanoid robots,” _arXiv preprint arXiv:2408.07295_ , 2024. 

- [22] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to noregret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 

- [23] V. Makoviychuk _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [24] Unitree, _Unitree’s first universal humanoid robot_ , 2023. 

- [25] R. Brooks, “A robust layered control system for a mobile robot,” _IEEE journal on robotics and automation_ , vol. 2, no. 1, pp. 14–23, 1986. 

- [26] D. Gouaillier _et al._ , “Mechatronic design of nao humanoid,” in _2009 IEEE international conference on robotics and automation_ , IEEE, 2009, pp. 769–774. 

- [27] N. A. Radford _et al._ , “Valkyrie: Nasa’s first bipedal humanoid robot,” _Journal of Field Robotics_ , vol. 32, no. 3, pp. 397–419, 2015. 

- [28] Y. Sakagami, R. Watanabe, C. Aoyama, S. Matsunaga, N. Higaki, and K. Fujimura, “The intelligent asimo: System overview and integration,” in _IEEE/RSJ international conference on intelligent robots and systems_ , IEEE, vol. 3, 2002, pp. 2478–2483. 

- [29] L. Sentis and O. Khatib, “A whole-body control framework for humanoids operating in human environments,” in _Proceedings 2006 IEEE International Conference on Robotics and Automation, 2006. ICRA 2006._ , IEEE, 2006, pp. 2641–2648. 

- [30] Y. Ishiguro _et al._ , “Bilateral humanoid teleoperation system using whole-body exoskeleton cockpit tablis,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 6419–6426, 2020. 

- [31] S. Dafarra _et al._ , “Icub3 avatar system: Enabling remote fully immersive embodiment of humanoid robots,” _Science Robotics_ , vol. 9, no. 86, eadh3834, 2024. 

- [32] M. Chignoli, D. Kim, E. Stanger-Jones, and S. Kim, “The mit humanoid robot: Design, motion planning, and control for acrobatic behaviors,” in _2020 IEEERAS 20th International Conference on Humanoid Robots (Humanoids)_ , IEEE, 2021, pp. 1–8. 

- [33] K. Okada, T. Ogura, A. Haneda, J. Fujimoto, F. Gravot, and M. Inaba, “Humanoid motion generation system on hrp2-jsk for daily life environment,” in _IEEE International Conference Mechatronics and Automation, 2005_ , IEEE, vol. 4, 2005, pp. 1772–1777. 

   - [44] C. Tessler, Y. Guo, O. Nabati, G. Chechik, and X. B. Peng, “Maskedmimic: Unified physics-based character control through masked motion,” in _ACM Transactions On Graphics (TOG)_ , ACM New York, NY, USA, 2024. 

   - [45] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler, “Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters,” _arXiv preprint arXiv:2205.01906_ , 2022. 

   - [46] C. Tessler, Y. Kasten, Y. Guo, S. Mannor, G. Chechik, and X. B. Peng, “Calm: Conditional adversarial latent models for directable virtual characters,” in _ACM SIGGRAPH 2023 Conference Proceedings_ , ser. SIGGRAPH ’23, Los Angeles, CA, USA: Association for Computing Machinery, 2023. 

   - [47] Z. Luo _et al._ , “Universal humanoid motion representations for physics-based control,” _arXiv preprint arXiv:2310.04582_ , 2023. 

- [34] S. Kuindersma _et al._ , “Optimization-based locomotion planning, estimation, and control design for the atlas humanoid robot,” _Autonomous robots_ , vol. 40, pp. 429–455, 2016. 

- [35] K. Darvish _et al._ , “Teleoperation of humanoid robots: A survey,” _IEEE Transactions on Robotics_ , vol. 39, no. 3, pp. 1706–1727, 2023. 

- [36] K. Hauser _et al._ , “Analysis and perspectives on the ana avatar xprize competition,” _International Journal of Social Robotics_ , pp. 1–32, 2024. 

- [37] M. Wonsick and T. Padır, “Human-humanoid robot interaction through virtual reality interfaces,” in _2021 IEEE Aerospace Conference (50100)_ , IEEE, 2021, pp. 1–7. 

- [38] A. Serifi, R. Grandia, E. Knoop, M. Gross, and M. B¨acher, “Vmp: Versatile motion priors for robustly tracking motion on physical characters,” 2024. 

- [39] Z. Luo, J. Cao, A. W. Winkler, K. Kitani, and W. Xu, “Perpetual humanoid control for real-time simulated avatars,” in _International Conference on Computer Vision (ICCV)_ , 2023. 

- [40] J. Won, D. Gopinath, and J. Hodgins, “A scalable approach to control diverse behaviors for physically simulated characters,” _ACM Trans. Graph._ , vol. 39, 4 2020. 

- [41] N. Chentanez, M. M¨uller, M. Macklin, V. Makoviychuk, and S. Jeschke, “Physics-based motion capture imitation with deep reinforcement learning,” _Proceedings - MIG 2018: ACM SIGGRAPH Conference on Motion, Interaction, and Games_ , 2018. 

- [42] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Trans. Graph._ , vol. 37, no. 4, 143:1–143:14, Jul. 2018. 

- [43] A. Shrestha, P. Liu, G. Ros, K. Yuan, and A. Fern, “Generating physically realistic and directable human motions from multi-modal inputs,” in _European Conference on Computer Vision_ , Springer, 2024, pp. 1–17. 

