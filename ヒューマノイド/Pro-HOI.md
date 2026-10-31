---
title: "Pro-HOI: Perceptive Root-guided Humanoid-Object Interaction"
date: "2026-03-01"
authors: "Yuhang Lin; Jiyuan Shi; Dewei Wang; Jipeng Kong; Yong Liu; Chenjia Bai"
url: https://arxiv.org/abs/2603.01126
pdf: https://arxiv.org/pdf/2603.01126
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.01126)** / [論文ページ](https://arxiv.org/abs/2603.01126)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Pro-HOI** : **P** erceptive **Ro** ot-guided **H** umanoid- **O** bject **I** nteraction 

Yuhang Lin<sup>1,2</sup> Jiyuan Shi<sup>1</sup> Dewei Wang<sup>1,3</sup> Jipeng Kong<sup>1,4</sup> Yong Liu<sup>2</sup> Chenjia Bai<sup>1</sup><sup>_†_</sup> Xuelong Li<sup>1</sup><sup>_†_</sup> 

> 1Institute of Artificial Intelligence (TeleAI), China Telecom 2Zhejiang University 

> 3University of Science and Technology of China 4ShanghaiTech University 

> †Corresponding author 


**Fig. 1: Pro-HOI** enables humanoid robots to perform generalizable and robust whole-body object interaction using exclusively onboard sensing and computing resources on a Unitree G1. a) **Stylized Behaviors** : Guided by motion tracking rewards, the robot exhibits stylized skills, such as running while carrying. b) **Navigation & Obstacle Avoidance** : The root-guided interface facilitates seamless integration with high-level planners for simultaneous carrying and obstacle avoidance. c) **Autonomous Re-grasping** : The robot autonomously detects an accidental drop, utilizing a digital twin module to enable state estimation and retrieval even when the object falls out of the camera’s field of view. d) **Continuous Operation** : The robot successfully completes over 15 consecutive carrying cycles, demonstrating long-horizon robustness. 

**_Abstract_ —Executing reliable Humanoid-Object Interaction (HOI) tasks for humanoid robots is hindered by the lack of generalized control interfaces and robust closed-loop perception mechanisms. In this work, we introduce** **<u>Perceptive Root-guided Humanoid-Object Interaction,</u> Pro-HOI, a generalizable framework for robust humanoid loco-manipulation. First, we collect box-carrying motions that are suitable for real-world deployment and optimize penetration artifacts through a Signed Distance** 

**Field loss. Second, we propose a novel training framework that conditions the policy on a desired root-trajectory while utilizing reference motion exclusively as a reward. This design not only eliminates the need for intricate reward tuning but also establishes root trajectory as a universal interface for high-level planners, enabling simultaneous navigation and locomanipulation. Furthermore, to ensure operational reliability, we incorporate a persistent object estimation module. By fusing real-** 

**TABLE I:** Capability comparison across different methods 

|Method|No External<br>Devices|Whole-Body<br>Control|Generalizable<br>Interaction|Controlable|Failure<br>Recovery|
|---|---|---|---|---|---|
|OmniRetarget[43]|✓|✓|_×_|_×_|_×_|
|HDMI[37]|_×_|✓|_×_|_×_|_×_|
|DemoHLM|✓|✓|✓|_×_|_×_|
|PhysHSI[34]|✓|✓|✓|_×_|_×_|
|Falcon[47]|✓|✓|✓|✓|_×_|
|OURS|✓|✓|✓|✓|✓|


**time detection with Digital Twin, this module allows the robot to autonomously detect slippage and trigger re-grasping maneuvers. Empirical validation on a Unitree G1 robot demonstrates that Pro-HOI significantly outperforms baselines in generalization and robustness, achieving reliable long-horizon execution in complex real-world scenarios. The project page is available on project page.** 

### I. INTRODUCTION 

Humanoid robots, characterized by their high degrees of freedom (DoFs) and anthropomorphic configurations, are widely viewed as the ideal platform for general-purpose robots. While state-of-the-art methods have demonstrated remarkable capabilities for performing highly dynamic motions [16, 39, 8, 48] and traversing complex terrain [49, 18, 33], executing whole-body manipulation tasks, such as box carrying, remains a significant challenge. This difficulty arises from the rigorous demands of maintaining balance under external loads, closed-loop perception for robust interaction with objects [7], and the extensibility to integrate with high-level planners [5]. Bridging the gap from isolated locomotion primitives to integrated perception-control frameworks is essential for achieving reliable carrying capabilities and represents a critical milestone in transitioning humanoid robots from laboratory demonstrations to practical applications in human-centric environments. 

Existing works on humanoid robot carrying tasks face various limitations. Traditional model-based methods often require task-specific design of optimization objectives and are limited to precise dynamics modeling [6, 1, 17], making it difficult to generalize to unknown scenarios. Reinforcement Learning (RL) has emerged as a scalable alternative for discovering complex contact-rich behaviors [9, 41, 12]. However, end-to-end RL approaches often necessitate laborious reward engineering, requiring distinct parameter tuning for different task phases to ensure convergence [46]. Recent advancements have attempted to address naturalness and generalization by incorporating Adversarial Motion Priors (AMP) [25] and a coarse-to-fine perception scheme [34]. HDMI [37] proposes to learn interaction skills from videos and presents a unified interaction task design, yielding a unified HOI training framework. However, this method not only relies on optical motion capture systems that are difficult to migrate, but also limits the location of object interactions to the training motion. What’s more, existing approaches often lack a generalized command interface for high-level planners [40] and fail to incorporate closed-loop perception during task execution [43]. For instance, if a robot drops a box while carrying, a practical 

system should enable the robot to autonomously detect the failure and pick it up. These limitations render current methods impractical for real-world carrying tasks. 

In this work, we present **Pro-HOI** ( **P** erceptive **Ro** ot-guided **H** umanoid- **O** bject **I** nteraction), a generalizable and robust RL controller for HOI task. First, we decouple the motion tracking objective from the observation space, conditioning the policy solely on the desired root trajectory while utilizing whole-body tracking exclusively as a reward. This enables the policy to learn the dynamic correlation between root trajectory and task states, allowing for generalizable object interaction without requiring full-body reference motions. Furthermore, this design establishes the root trajectory as a universal interface, facilitating seamless integration with diverse high-level planners for executing carrying, navigation, and obstacle avoidance tasks simultaneously. Second, to address real-world uncertainties such as accidental drops, we introduce a persistent object estimation module. Combining real-time object detection with Digital Twin, this module enables the robot to detect drops and re-acquire objects autonomously, thereby substantially enhancing system reliability. Table I presents a qualitative comparison between our framework and state-of-the-art HOI methods. While early approaches like OmniRetarget [43] and HDMI [37] established the foundation for whole-body control, they are limited by either poor generalization or reliance on external devices. Recent imitation-based works, such as PhysHSI [34] and Falcon [47], have significantly improved interaction generalizability and controllability. However, a critical gap remains: none of these baselines account for execution robustness. In contrast, our method stands out as the only holistic solution that integrates controllable, generalizable interaction with a distinct failure recovery mechanism, ensuring reliable deployment without the need for external instrumentation. 

To evaluate our approach, we conducted extensive experiments on the box carrying task with various practical challenges, such as continuous multi-cycle transport of boxes with diverse locations, carrying with obstacle avoidance, and autonomous re-grasping under disturbances. The results confirm that Pro-HOI not only supports seamless high-level integration but also achieves superior robustness, enabling reliable longhorizon task execution. 

In summary, the main contributions of this work are as follows: 

- We propose a root trajectory guided RL framework for HOI task. This framework achieves generalizable humanoid HOI capabilities without requiring extensive 

reference motions or intricate reward engineering. Furthermore, the root trajectory serves as a flexible interface that seamlessly integrates with high-level planners to enable simultaneous navigation and obstacle avoidance. 

- We introduce a persistent object estimation module that combines real-time object detection with Digital Twin. This module allows autonomous re-grasping of dropped objects, which significantly enhances system robustness and practicality in real-world scenarios. 

- We deploy the complete system on a Unitree G1 robot, with all modules running on a single onboard Jetson NX. Extensive real-world experiments validate the generalization, scalability, and robustness of our approach. 

### II. RELATED WORKS 

### _A. Reinforcement Learning for Humanoid Control_ 

With large-scale simulation training and sim-to-real transfer techniques, RL empowers humanoid robots to achieve robust locomotion [27, 38, 18], highly agile maneuvers [49, 31], and recovery behaviors [11, 13]. To enable robots to perform human-like behaviors, mimic-based approaches that imitate human demonstrations [23] have been extended to highly anthropomorphic and dynamic humanoid whole-body control [10, 39, 16, 48, 8, 43]. Despite demonstrating remarkable capabilities, these methods exhibit limited generalization, particularly for real-world HOI tasks that demand extensive adaptability to diverse scenarios. Alternative paradigms like Adversarial Motion Priors (AMP) [33, 34] mitigate the need for precise tracking by learning style distributions from datasets. However, these methods typically suffer from a trade-off between style fidelity and task generalization. 

Distinguished from prior works, we propose a root-guided HOI training paradigm. By decoupling the root commands from the motion tracking rewards, the policy only exhibits anthropomorphic behaviors but also possesses high generalizability. 

### _B. Humanoid-Object Interaction_ 

Humanoid-object interaction (HOI) [20, 35] presents a compounded challenge due to the high-dimensional state space and complex contact dynamics involved, particularly in real-world deployments. Early approaches utilizing Trajectory Optimization (TO) [29, 6, 17] can generate physically feasible motions for specific tasks but often suffer from limited generalization to unseen scenarios. 

Recent RL-based approaches for HOI have demonstrated enhanced robustness and generalization capabilities [46, 37, 34, 47, 45]. Through meticulous reward and task design, RL-based controllers can acquire whole-body manipulation skills involving specific contact sequences [46]. However, such methods necessitate intricate reward engineering and, due to the absence of reference trajectories, often struggle to constrain the stylistic quality of the learned motions. A promising alternative involves learning interaction skills directly from large-scale human videos [37]. While data acquisition in this paradigm is scalable, the approach relies on external Motion 

Capture (MoCap) systems for deployment and often lacks generalization regarding object positioning. VisualMimic[45] employs a hierarchical whole-body control framework to train a humanoid robot for specific HOI tasks; however, the learned policy is limited to interactions with objects that remain within the visual field. FALCON[47] achieves force-adaptive HOI through a dual-agent learning framework and can be combined with high-level planners to perform complex tasks. However, these methods are limited to scenarios where the object remains within the robot’s field of view. Distinguished from the motion-tracking or hierarchical methods, PhysHSI [34] incorporates AMP to learn an end-to-end HOI policy and significantly enhance generalization, yet this inevitably introduces the burden of laborious task reward tuning. 

In contrast, our approach decouples the target root trajectory observation from the motion tracking reward. This design enables the robot to execute generalizable HOI tasks while preserving human-like motion styles. Furthermore, the root trajectory serves as a versatile interface compatible with highlevel planners, facilitating complex tasks such as navigation and obstacle avoidance. Additionally, by leveraging a digital twin module to enable state estimation for out-of-view objects during deployment, our system successfully completed over 15 continuous box-carrying cycles in the real world, demonstrating exceptional generalization and robustness. 

### III. METHOD 

### _A. Problem Definition_ 

We formulate humanoid-object interaction as a goalconditioned reinforcement learning problem, where the agent interacts with objects in a physical environment according to a policy _π_ to maximize cumulative reward. We adopt the Unitree G1 robot as the agent, which has 29 degrees of freedom (DoF) in total. At each timestep _t_ , the policy receives the state **_s_** _t_ and target state **_g_** _t_ , and outputs an action **_a_** _∈_ R<sup>29</sup> , which represents the target joint positions and subsequently converted into motor torques via a PD controller. State transitions are governed by the environment dynamics _p_ ( **_s_** _t_ +1 _|_ **_s_** _t,_ **_a_** _t_ ), and A dense reward function _r_ ( **_s_** _t,_ **_g_** _t,_ **_a_** _t_ ) is employed for task performance evaluation and regularization. The optimization objective is to maximize the expected discounted return: _J_ = E _t_ =0<sup>_γtrt_</sup> . �� _T −_ 1 � 

The policy is trained using Proximal Policy Optimization (PPO) [30] in an asymmetric Actor-Critic architecture [26] to ensure it is deployable on physical hardware. During training, the critic has access to privileged information (e.g., base velocity), while the actor operates on noisy observations available to the real robot. 

### _B. Data Preparation and Optimization_ 

While numerous HOI datasets exist [15, 3], their highdynamic motions (e.g., sharp bending) are often difficult for a humanoid robot to imitate, thereby increasing the risk of overheating. To improve interaction performance, we first collected a custom dataset of box-carrying human motions in the SMPL [22] format using an Xsens inertial motion 


**Fig. 2: Overview of Pro-HOI.** a) **Data Preparation** : We frist collect human motion clips using the mocap system, and augment them with object geometries in _Blender_ . Then we use SDF-based optimization to generate physically feasible reference motions. b) **Root-Guided Policy Learning** : The RL policy is trained to perform whole-body interaction skills conditioned on the desired root trajectory, while utilizing the reference motion as rewards. c) **Real-world Deployment** : We integrate FoundationPose for 6D object pose estimation and FAST-LIO2 [42] for root pose estimation, combined with the Interaction Pose Prior and a task specific planner to generate target root trajectories. The full stack executes entirely onboard a Jetson NX with a D435i camera and a Mid-360 LiDAR, achieving robust sim-to-real transfer. 

capture system. We then retargeted the SMPL motions to the humanoid robot using General Motion Retargeting (GMR) [2]. Without capturing object state, existing HOI retargeting methods [43] are inapplicable. To address this, we manually associated the object with the robot’s end-effector using the ‘Child Of’ constraint in Blender [4]. 

Precise humanoid–object alignment is crucial for mimicbased learning frameworks. We formulated a penetration loss based on SDF [21, 44] to resolve mesh penetration artifacts between the robot’s end-effector and the object. 

simplifiedSpecifically, we utilize voxel-based downsampling to obtainmeshes _M_ ˆ hand and _M_ ˆ obj, and construct a SDF Φobj( _·_ ) from the object mesh. Then, we optimize the robot’s upper-body joints position **_q_** upper over the contact phase _Tc_ = [ _ϕ_ 1 _, ϕ_ 2], which is computed by the linear velocity of objects. The penetration loss is defined as: 


where **_P_** _t_<sup>hand</sup> represents the hand vertices at timestep _t_ in the object’s coordinate frame. We minimize _L_ pen using the Adam optimizer [14] to keep the hands in contact with the object’s 

surface. 

### _C. Root-guided HOI Policy Training_ 

_1) HOI Process Encoding:_ A core challenge in mimicbased HOI is the trade-off between motion fidelity and generalization. Existing imitation approaches often include fullbody reference motions (e.g., joint positions and velocity) [16] or scalar phase variables (e.g., _ϕ ∈_ [0 _,_ 1]) [10] in the policy observation. However, directly observing high-dimensional reference motions imposes a heavy data burden for learning the intricate mapping between body poses and object locations [19]. Since interaction mechanics vary drastically with object positioning, achieving exhaustive dataset coverage is practically infeasible. Conversely, low-dimensional phase variables lack sufficient spatial context to guide complex, multi-stage tasks like box carrying. 

To bridge this gap, we propose a root-guided observation paradigm. By leveraging the desired root movement trend, we effectively encode the task’s semantic stages. In the case of carrying boxes, vertical movement means squatting or standing, while horizontal movement means locomotion or transport. Coupling this spatial trend with a binary desired contact state _ct ∈{_ 0 _,_ 1 _}_ forms a minimalist yet sufficient ob- 

servation space. Desired contact state _ct_ represents whether the robot’s end-effectors should be in contact with the object from reference motions. This design compels the policy to learn the correlations between desired movement, contact states, and distinct task phases via reward signals, rather than merely mimicking reference motions. Notably, this streamlined design exhibits high data efficiency, requiring only a limited set of HOI demonstrations for effective training. Furthermore, utilizing the root trajectory as an observation facilitates seamless integration with high-level path planners, thereby enabling the execution of complex object interaction tasks. 

Specifically, we define the above observation state as the goal **_g_** _t_ = [∆ **_p_**<sup>root</sup> _t ,_ ∆ **_r_** _t_<sup>root</sup> _, ct_ ]. The ∆ **_p_**<sup>root</sup> _t_ and ∆ **_r_** _t_<sup>root</sup> represent the deviation in root position and orientation between the current state and the expected state. 

_2) State Space:_ The critic and the actor operate on different information sets. At each timestep _t_ , the critic has access to the full state **_s_** _t_ , which comprises the proprioceptive state, the object state **_s_**<sup>o</sup> _t_<sup>,andthegoal</sup><sup>**_g_**</sup><sup>_t_:</sup> 


where **_p_**<sup>body</sup> _t ∈_ R<sup>14</sup><sup>_×_3</sup> and **_r_** _t_<sup>body</sup> _∈_ R<sup>14</sup><sup>_×_6</sup> denote the positions and rotations of the robot’s key bodies. The root state consists of projected gravity **g** ˜ _∈_ R<sup>3</sup> , linear velocity **_v_** _t ∈_ R<sup>3</sup> , and angular velocity **_ω_** _t ∈_ R<sup>3</sup> . The joint state includes positions **_q_** _t ∈_ R<sup>29</sup> , velocities **_q_** ˙ _t ∈_ R<sup>29</sup> , and the previous action **_a_** _t−_ 1 _∈_ R<sup>29</sup> . The state of an object consists of its position **_p_** _t_<sup><u>o</u></sup> <u>rel</u> _∈_ R<sup>3</sup> and rotation **_r_** _t_<sup><u>o</u></sup> <u>rel</u> _∈_ R<sup>6</sup> in the robot coordinate system. In contrast, the actor _π_ receives a partial observation **_o_** _t_ to ensure deployment feasibility. Specifically, **_o_** _t_ excludes the privileged information difficult to estimate on physical hardware—namely, the robot’s key body poses and the root linear velocity **_v_** _t_ . Thus, the observation is defined as a subset: **_o_** _t_ = **_s_** _t \{_ **_p_**<sup>body</sup> _t ,_ **_r_** _t_<sup>body</sup> _,_ **_v_** _t}_ . Furthermore, to bridge the sim-toreal gap, we inject Gaussian noise into the policy’s observations to simulate sensor uncertainty, whereas the critic operates on the noise-free state to ensure stable value estimation. 

_3) Reward Terms:_ Without task-specific reward design, we utilize simple tracking-based reward terms _R_ ( _·, ·_ ) to guide the training process. During training, for each episode, we randomly sample a reference HOI motion state **_s_**<sup>ref</sup> _t_ from the dataset. The robot and the object are initialized to the starting state of the sequence. At each timestep _t_ , we compute the total reward _rt_ as the sum of two components: 


Specifically, the tracking reward _R_ ( **_s_** _t,_ **_s_**<sup>ref</sup> _t_<sup>)minimizesde-</sup> viations in the global root pose and incentivizes the agent to replicate the reference joint kinematics, thereby implicitly guiding the necessary whole-body coordination. Regarding the object, the reward prioritizes manipulation fidelity; it encourages precise tracking of the reference trajectory and enforces consistency between the simulated and reference contact states. Finally, the penalty term _P_ reg( **_s_** _t_<sup>p</sup><sup>_,_</sup><sup>**_a_**</sup><sup>_t_)serves</sup> as a regularization component. It penalizes large temporal 

variations in actions to ensure control smoothness, discourages joint limit violations, and prevents undesired collisions. 

_4) Sim-to-Real Transfer:_ To ensure successful sim-to-real transfer, we employ Domain Randomization (DR) [24] during training to enhance policy robustness. Specifically, we randomize a set of physical parameters, including friction, restitution coefficients, joint position offsets, the agent’s center of mass (CoM), and the object’s mass. Furthermore, to simulate external disturbances, we apply random perturbations to the robot’s root linear and angular velocities. 

### _D. Real-world Deployment System_ 

A primary discrepancy between simulation and the real world lies in the inaccessibility of a precise global pose for both the robot and the object. Accurate acquisition of these states is critical for robust object interaction and precise transport. On one hand, relying on onboard sensors for perception presents significant challenges due to limited FoV, perception latency, and constrained computational resources. The difficulty is further exacerbated during occlusions or unconstrained motion (e.g., free-falling). On the other hand, training mimic-based policies typically relies on reference root trajectories from datasets. However, these trajectories often imply the location of objects, limiting the generalization ability of policy to interact with objects at random locations in real-world deployments. To address these challenges, we propose an object state estimation module (III-D1) to ensure acquisition of stable object states, and root trajectory planner (III-D2) conditioned on object initial position and waypoints of the robot to achieve generalizable interactions. 

_1) Object State Estimation Module:_ To ensure robust 6D pose tracking under partial occlusion during interaction, we leverage FoundationPose [36]. This unified foundation model enables stable tracking of novel objects given their mesh models without fine-tuning. 

Once an object falls, it often exits the limited FoV of the onboard sensors. Treating the object as a point mass under gravity is insufficient, as it neglects geometric collisions with the robot body and the ground. To address this, we propose a Digital Twin module powered by the MuJoCo simulator [32]. Leveraging continuous state estimation, we formulate a heuristic to detect manipulation failures. A drop event is identified based on the inconsistency between the contact goal and the relative object pose. Specifically, the system triggers a drop alert if the contact state remains active ( _ct_ = 1) while the deviation in the relative object position exceeds a safety threshold _δ_ pos over a sliding time window _N_ . 

This Digital Twin module runs on an external computational unit, synchronizing with the robot and object global states in real-time. Upon detecting a drop, the simulator initializes a parallel environment using the object’s last known pose and velocity. It then performs high-fidelity physics stepping to simulate collision dynamics and predict the final resting pose. Based on this prediction, the robot automatically adjusts its gaze to re-acquire the object, facilitating seamless recovery and re-grasping. 

_2) Root Trajectory Planner:_ The core observation mechanism of our policy relies on the deviation of the root pose between the current and reference states, which guides the entire interaction process. During training, the policy relies on a limited set of fixed reference trajectories. However, the reference trajectories can be flexibly defined to meet task requirements during inference, utilizing tools such as off-theshelf 2D planners or generative motion models. To ensure stable object interaction, we propose a hybrid root trajectory planning method that leverages grasping priors from the dataset to guide the policy. Specifically, the planner consists of three parts: interaction pose prior, task-specific planner, and 6Dof trajectory interpolation _ξ_ ( _t_ ), constrained by expected linear and angular velocity. 

_a) Interaction Pose Prior:_ To facilitate robust object interaction, we leverage grasping priors extracted from the training dataset. Specifically, we record the relative robotobject poses at the onset of each contact phase. During deployment, upon detecting a new object, the system retrieves the optimal interaction configuration by evaluating the similarity between the currently detected relative object pose and the stored priors. 

_b) Task-specific planner:_ Upon establishing the global interaction target, the policy can be flexibly guided by diverse trajectory planners to accommodate specific task requirements. In this work, we integrate the Timed Elastic Band (TEB) [28] local planner as an exemplar navigation module for executing long-horizon transport tasks with collision avoidance. Given a goal location and an obstacle map, the planner generates a smooth planar trajectory comprising a sequence of 2D positions and yaw angles. We then transform these planar waypoints into a 6-DoF trajectory to serve as the desired root poses. 

_c) 6Dof trajectory interpolation:_ To generate a continuous reference root trajectory for the policy, we apply 6-DoF interpolation to the constructed waypoint sequence. This process synthesizes the robot’s current state, specific interaction targets, and the planner-generated trajectory into a unified time-parameterized trajectory, while simultaneously outputting the expected contact commands based on the interaction objectives. 

### IV. EVALUATION 

In this section, we conduct a comprehensive evaluation of our proposed framework in both high-fidelity simulation and real-world environments. Our experiments aim to answer the following questions: 

- **Q1:** How does our root-guided policy perform on box carrying tasks? 

- **Q2:** How does our policy perform on tracking the reference root trajectories and contact command? 

- **Q3:** Does the system support complex, long-horizon, and dynamic tasks? 

- **Q4:** Can the policy and perception system reliably transfer to physical hardware? 

_A. How does our root-guided policy perform on box carrying tasks?_ 

**Experimental Setup:** The task is decomposed into four phases: _Approach_ , _Pick_ , _Carry_ , and _Place_ . To rigorously evaluate the robustness and generalization capability of our method, we conducted comprehensive tests categorized into two sets: _In-Distribution (ID)_ and _Out-of-Distribution (OOD)_ . The ID set utilizes the exact robot and object configurations from the training distribution. The OOD set is designed to test the policy by random sampling of the initial object position and the target placement position in the workspace. Specifically, we created a grid with a spacing of 0 _._ 2m within a trapezoidal region defined by _x ∈_ [0 _._ 4 _,_ 1 _._ 4] m and _y ∈_ [ _−x, x_ ] m. For each grid point, we evaluated object yaw orientations from _{_ 0<sup>_◦_</sup> _,_ 15<sup>_◦_</sup> _,_ 30<sup>_◦_</sup> _,_ 45<sup>_◦_</sup> _}_ . Furthermore, target placement locations were sampled along a circle with a radius of 4m centered on the robot at 10<sup>_◦_</sup> intervals. This extensive evaluation protocol yields a total of 5 _,_ 756 distinct task scenarios. 

Table II presents the evaluation of our root-guide policy’s performance by comparing it against the following baselines in the MuJoCo simulator: 

- **w/o SDF:** We trained a variant of our policy using raw retargeted motions without SDF optimization while keeping all other hyperparameters constant. 

- **w/o contact:** This baseline is trained without the contactrelated observation and reward. 

- **PhysHSI:** A state-of-the-art baseline that utilizes AMP combined with manually designed rewards for box carrying tasks. 

- **Ours w/ FR.:** A variant of our proposed framework that includes the failure recovery strategy. 

The performance is evaluated using the following metrics: 

_1)_ **_Grasp Success Rate_** _:_ Evaluates the stability of the grasp and represents it as ( _R_ succ). It is defined as the percentage of trials where the robot successfully lifts the object above a threshold height and maintains the grasp without slippage for at least 1 second. Our method demonstrates superior grasping stability, particularly in generalization scenarios. While baseline methods suffer significant performance drops in OOD settings (e.g., PhysHSI drops from 96.60% to 82.54%), our full method ( **Ours w/ FR.** ) achieves a near-perfect success lift rate of 99.93% in OOD tasks. This robust performance verifies that our root-guided policy, combined with the failure recovery mechanism, effectively handles variations in object positioning without compromising grasp stability. A detailed visualization of the grasp success rate is presented in Figure 3. 

_2)_ **_Placement Precision_** _:_ Quantifies the manipulation accuracy and represents it as _R_ prec. It is calculated as the average Euclidean distance between the object’s final resting position and the target goal center. This metric is computed only for successful episodes to exclude outliers from failed grasps. Quantitatively, our approach yields the highest placement precision. In ID settings, **Ours w/ FR.** reduces the placement error to just 6.46 cm, significantly outperforming the baselines, 

**TABLE II: Quantitative comparison** of success rates, placement precision and execution velocity in Mujoco. 

|**Method**||**In Dist**|**ribution**|||**Out Dis**|**tribution**||
|---|---|---|---|---|---|---|---|---|
||Rsucc(%_↑_)|Rprec(cm_↓_)|Rtask(%_↑_)|Vexec(m/s_↑_)|Rsucc(%_↑_)|Rprec(cm_↓_)|Rtask(%_↑_)|Vexec(m/s_↑_)|
|w/o SDF|97.90|7.54|55.76|0.29|82.52|8.44|64.26|0.436|
|w/o contact|94.99|7.86|31.13|0.29|88.43|8.28|71.65|0.41|
|PhysHSI [34]|96.60|7.62|**90.59**|**0.49**|82.54|7.25|70.17|**0.72**|
|**Ours**|97.90|6.32|73.07|0.29|91.90|**6.83**|76.15|0.42|
|**Ours w/ FR.**|**100.00**|**5.80**|73.67|0.29|**99.93**|6.84|**88.38**|0.27|


**Fig. 3: Spatial distribution of grasp success rates across the Out-of-Distribution (OOD) evaluation set.** The color scale indicates the success rate, where darker green denotes higher stability and red/yellow indicates failure. 


**Fig. 4: Statistical distribution of placement precision across different methods.** 

which hover around 9.5 cm. This trend continues in OOD scenarios, where both our base policy and the version with failure recovery maintain high accuracy. This indicates that our minimalist observation space does not sacrifice control precision; rather, by focusing on the root trajectory, the policy achieves more consistent global spatial planning. We present the box plot of placement precision with tolerance threshold _<_ 0 _._ 2m in Figure 4. 

_3)_ **_Task Success Rate_** _:_ The metric for task completion rate is represented as _R_ task. A trial is considered a task success only if the robot completes the entire pick-and-place sequence, and the final object position lies within a tolerance threshold ( _<_ 0 _._ 1m) of the target. The results highlight the generalization capability of our framework. Although PhysHSI achieves a high success rate (90.59%) in ID settings, likely due to overfitting to reference motions, its performance degrades to 70.17% in OOD tasks. In contrast, **Ours w/ FR.** demonstrates exceptional robustness, achieving the highest task success rate of 88.38% in the challenging OOD setting. This validates that our decoupled observation design enables the robot to adapt to novel object locations and complete complex multi-stage tasks that traditional motion-tracking methods fail at. 

**TABLE III:** Quantitative comparison of tracking fidelity and synchronization. Metrics are reported as **Mean** _±_ **Std** . **RPE** : Root Position Error (m), **ROE** : Root Orientation Error (rad), **MPL** : Motion Phase Lag (s), **CPL** : Contact Phase Lag (s). The best results are highlighted in **bold** . 

|**Method**|**RPE** _↓_|**ROE** _↓_|**MPL** _↓_|**CPL** _↓_|
|---|---|---|---|---|
|w/o Contact|0.23 _±_0_._03|6.39 _±_0_._53|18.37 _±_1_._54|20.50 _±_7_._00|
|w/o SDF|0.26 _±_0_._03|6.33 _±_0_._79|22.11 _±_1_._35|**14.25** _±_3_._28|
|**Ours**|**0.22** _±_0_._02|**5.77** _±_0_._41|**16.21** _±_1_._61|14.80 _±_3_._89|


_B. How does our policy perform on tracking the reference root trajectories and contact command?_ 

To rigorously quantify the policy’s ability to track the reference root pose and adhere to the contact schedule, we conducted an extensive evaluation using diverse trajectory generation methods across a range of target velocities. We recorded both the generated reference trajectories, _ξ_ ref, and the robot’s executed root trajectories, _ξ_ real. The performance is measured using the following four metrics: 

- **Root Position Error (RPE):** The average Euclidean distance between the reference and actual root positions. 

- **Root Orientation Error (ROE):** The average angular deviation between the reference and actual root orientations. 

- **Motion Phase Lag (MPL):** Defined as the temporal delay for the robot’s root to reach the spatial position specified by the reference trajectory. This metric reflects the dynamic response speed of the policy. 

- **Contact Phase Lag (CPL):** The average temporal discrepancy between the reference contact timestamp (when _ct_ switches to 1) and the actual physical contact onset. 

We benchmark our method against two ablation variants, **w/o SDF** and **w/o Contact** as described above. 

The quantitative results presented in Table III demonstrate that our full framework consistently outperforms the ablation baselines across most metrics, achieving the best balance between spatial accuracy and temporal synchronization. 

In terms of spatial tracking fidelity, ours achieves the lowest RPE and ROE. Compared to the _w/o SDF_ baseline, our method significantly reduces tracking deviations, suggesting that the SDF-based optimization effectively eliminates physics inconsistencies in the reference motion, thereby allowing the policy to learn more precise kinematic tracking. 

Regarding dynamic response, our method exhibits the lowest MPL, improving upon _w/o Contact_ and _w/o SDF_ . This indicates that including explicit contact states and high-quality motion priors enables the policy to anticipate high-dynamic transitions more effectively, thereby reducing the temporal delay between the reference and executed trajectories. 

For contact synchronization CPL, the _w/o Contact_ variant exhibits the highest lag, confirming that without explicit contact observations, the policy struggles to initiate interaction at the correct time. While _w/o SDF_ achieves a marginally lower CPL compared to **Ours** , the difference is minimal given the standard deviation. Crucially, our method maintains this competitive contact timing while delivering significantly superior spatial tracking and motion response, validating the necessity of each component in the proposed framework. 

_C. Does the system support complex, long-horizon, and dynamic tasks?_ 

To demonstrate the versatility and robustness of our integrated system, we designed four challenging task scenarios as shown in Figure 1: 

_a) Task I: Continuous Long-Horizon Transport:_ We verified the system’s ability to perform continuous re-arrangement tasks. Guided by the root trajectory planner, the robot autonomously returns to the starting point after placing the box, initiating the next transport cycle. This test confirms the cyclic stability of our state machine and planner. 

_b) Task II: Obstacle Avoidance:_ We introduced static obstacles in the transport path. Leveraging the TEB planner, our system successfully generated collision-free trajectories, modifying the robot’s yaw and path to navigate around obstacles while carrying the load. 

_c) Task III: Failure Recovery via Digital Twin:_ We simulated a scenario where the box is knocked out of the robot’s hands during transport. The Object State Estimation module detected the drop and utilized the physics-based simulator to estimate the object’s new location. The robot successfully adjusted its gaze, replanned the approach, and regrasped the object, demonstrating resilience in the face of unexpected failures. 

_d) Task IV: High-Dynamic Agility:_ To explore the upper limits of our method, we simulated a high-speed ”running and carrying” scenario. The results indicate that our root-guided policy can generalize to highly dynamic motions, suggesting potential for future high-speed humanoid manipulation. 

_D. Can the policy and perception system reliably transfer to physical hardware?_ 

We deployed our system on the Unitree G1 humanoid robot to evaluate sim-to-real transferability. 

_1) Real-World Manipulation and Dynamic Robustness:_ We deployed our system on the physical Unitree G1 robot to evaluate its robustness under varying dynamic conditions. To systematically assess the policy’s performance across different operating speeds, we categorized the guidance commands into three profiles: _Slow_ ( _v_ = 0 _._ 2 m/s, _ω_ = 0 _._ 6 rad/s), _Middle_ 

( _v_ = 0 _._ 4 m/s, _ω_ = 1 _._ 0 rad/s), and _Fast_ ( _v_ = 0 _._ 6 m/s, _ω_ = 1 _._ 3 rad/s). 

The quantitative results are summarized in Table IV. As shown, the system exhibits consistent reliability across diverse velocity profiles, maintaining a grasp success rate exceeding 60% in all scenarios. We specifically conducted an extended evaluation of 28 consecutive trials under the _Middle_ profile. Notably, this sequence included multiple instances where the object was intentionally dislodged. Despite these severe disturbances, our method successfully recovered and completed the tasks, underscoring the system’s exceptional robustness and stability on physical hardware. 

**TABLE IV:** Real-world performance under different dynamic command profiles. **GSR** : Grasp Success Rate (%), **PP** : Placement Precision (error in m). The velocities represent the maximum commanded linear ( _v_ ) and angular ( _ω_ ) limits. 

|**Profile**|**Command **|**Velocity**|**GSR** (_↑_)|**PP** (m) (_↓_)|
|---|---|---|---|---|
||_v_ (m/s)<br>|_ω_ (rad/s)|||
|**Slow**|0.2|0.6|7 / 10|0.15|
|**Middle**|0.4|1.0|21 / 28|0.16|
|**Fast**|0.6|1.3|6 / 10|0.25|


_2) Evaluation of Object State Estimation:_ To validate the efficacy of our Digital Twin drop prediction module, we established a discretized grid coordinate system centered on the robot’s base with a spatial resolution of 0 _._ 2 _×_ 0 _._ 2 m. Controlled drop experiments were conducted by releasing objects with arbitrary orientations within the robot’s FoV. The primary function of this module is to estimate a recovery pose by falling simulation in MuJoCo and reorient the robot’s gaze after the object fell. Consequently, we define the success rate for each grid cell as the Success rate with which the robot re-acquires the object in its FoV after adjusting its pose based on the drop location predicted by the MuJoCo simulation. Figure 5 visualizes the detection success rates within the original camera FoV and the adjusted FoV guided by the object estimation. The results demonstrate that this module effectively augments the original detection FoV during the interaction process, especially the circular area centered on the robot. 


**Fig. 5:** The percentages quantify the likelihood of successfully detecting an object dropped within each respective region. (a) The detection probability distribution simulated via the object estimate module. (b) The baseline detection probability distribution relying exclusively on the onboard camera. 

### V. CONCLUSION 

In this work, we presented Pro-HOI (Perceptive Rootguided Humanoid-Object Interaction), a generalizable and robust framework for humanoid-object interaction. By proposing a low-dimensional representation that encodes the interaction process through root trajectories and contact information, our approach overcomes the inherent generalization limitations of traditional imitation based learning method while make the HOI process controllable. Extensive experiments demonstrate that Pro-HOI achieves superior task success rates in out-ofdistribution scenarios, enhanced manipulation precision, and reliable sim-to-real transferability compared to state-of-the-art baselines. 

### ACKNOWLEDGMENTS 

This work is supported by the National Natural Science Foundation of China (Grant No.62306242), the Young Elite Scientists Sponsorship Program by CAST (Grant No. 2024QNRC001), and the Yangfan Project of the Shanghai (Grant No.23YF11462200). 

### REFERENCES 

- [1] Alphonsus Adu-Bredu, Grant Gibson, and Jessy Grizzle. Exploring kinodynamic fabrics for reactive whole-body control of underactuated humanoid robots. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 10397–10404. IEEE, 2023. 

- [2] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [3] Bharat Lal Bhatnagar, Xianghui Xie, Ilya Petrov, Cristian Sminchisescu, Christian Theobalt, and Gerard PonsMoll. Behave: Dataset and method for tracking human object interactions. In _IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, jun 2022. 

- [4] Blender Foundation. Blender, 2024. URL https://www. blender.org. Version 4.0. 

- [5] Pengxiang Ding, Han Zhao, Wenjie Zhang, Wenxuan Song, Min Zhang, Siteng Huang, Ningxi Yang, and Donglin Wang. Quar-vla: Vision-language-action model for quadruped robots. In _European Conference on Computer Vision_ , pages 352–367. Springer, 2024. 

- [6] Nadia Figueroa, Salman Faraji, Mikhail Koptev, and Aude Billard. A dynamical system approach for adaptive grasping, navigation and co-manipulation with humanoid robots. In _2020 IEEE International conference on robotics and automation (ICRA)_ , pages 7676–7682. IEEE, 2020. 

- [7] Zhaoyuan Gu, Junheng Li, Wenlan Shen, Wenhao Yu, Zhaoming Xie, Stephen McCrory, Xianyi Cheng, Abdulaziz Shamsah, Robert Griffin, C Karen Liu, et al. Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. _IEEEASME transactions on mechatronics_ , 2025. 

- [8] Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv preprint arXiv:2509.16638_ , 2025. 

- [9] Mohamed Hassan, Yunrong Guo, Tingwu Wang, Michael Black, Sanja Fidler, and Xue Bin Peng. Synthesizing physical character-scene interactions. In _ACM SIGGRAPH 2023 Conference Proceedings_ , pages 1–9, 2023. 

- [10] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [11] Xialin He, Runpei Dong, Zixuan Chen, and Saurabh Gupta. Learning getting-up policies for real-world humanoid robots. _arXiv preprint arXiv:2502.12152_ , 2025. 

- [12] Dianyong Hou, Chengrui Zhu, Zhen Zhang, Zhibin Li, Chuang Guo, and Yong Liu. Efficient learning of a unified policy for whole-body manipulation and locomotion skills. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 5455–5461. IEEE, 2025. 

- [13] Tao Huang, Junli Ren, Huayi Wang, Zirui Wang, Qingwei Ben, Muning Wen, Xiao Chen, Jianan Li, and Jiangmiao Pang. Learning humanoid standingup control across diverse postures. _arXiv preprint arXiv:2502.08378_ , 2025. 

- [14] Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In _International Conference on Learning Representations_ , 2015. 

- [15] Jiaman Li, Jiajun Wu, and C Karen Liu. Object motion guided human motion synthesis. _ACM Trans. Graph._ , 42 (6), 2023. 

- [16] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [17] Fukang Liu, Zhaoyuan Gu, Yilin Cai, Ziyi Zhou, Hyunyoung Jung, Jaehwi Jang, Shijie Zhao, Sehoon Ha, Yue Chen, Danfei Xu, et al. Opt2skill: Imitating dynamicallyfeasible whole-body trajectories for versatile humanoid loco-manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [18] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao Huang, Ping Luo, and Jiangmiao Pang. Learning humanoid locomotion with perceptive internal model. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9997–10003. IEEE, 2025. 

- [19] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Casta˜neda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi Fan, and Yuke Zhu. 

Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [20] Liang Pan, Zeshi Yang, Zhiyang Dou, Wenjia Wang, Buzhen Huang, Bo Dai, Taku Komura, and Jingbo Wang. Tokenhsi: Unified synthesis of physical human-scene interactions through task tokenization. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 5379–5391, 2025. 

- [21] Jeong Joon Park, Peter Florence, Julian Straub, Richard Newcombe, and Steven Lovegrove. Deepsdf: Learning continuous signed distance functions for shape representation. In _CVPR_ , 2019. 

- [22] Georgios Pavlakos, Vasileios Choutas, Nima Ghorbani, Timo Bolkart, Ahmed A. A. Osman, Dimitrios Tzionas, and Michael J. Black. Expressive body capture: 3D hands, face, and body from a single image. In _Proceedings IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , pages 10975–10985, 2019. 

- [23] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [24] Xue Bin Peng, Marcin Andrychowicz, Wojciech Zaremba, and Pieter Abbeel. Sim-to-real transfer of robotic control with dynamics randomization. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 3803–3810. IEEE, 2018. 

- [25] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [26] Lerrel Pinto, Marcin Andrychowicz, Peter Welinder, Wojciech Zaremba, and Pieter Abbeel. Asymmetric actor critic for image-based robot learning. _arXiv:1710.06542_ , 2017. URL https://arxiv.org/abs/1710.06542. arXiv preprint. 

- [27] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

- [28] Christian R¨osmann, Felix Hoffmann, and Torsten Bertram. Integrated online trajectory planning and optimization in distinctive topologies. _Robotics and Autonomous Systems_ , 88:142–153, 2017. 

- [29] Francesco Ruscelli, Matteo Parigi Polverini, Arturo Laurenzi, Enrico Mingo Hoffman, and Nikos G Tsagarakis. A multi-contact motion planning and control strategy for physical interaction tasks using a humanoid robot. In _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3869–3876. IEEE, 2020. 

- [30] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [31] Ruiyu Tan, Xueai Li, Fenglei Ni, Dong Zhou, Yi Ji, and Xiangyu Shao. Versatile jumping of humanoid robots via curriculum-assisted reinforcement learning. In _2024 China Automation Congress (CAC)_ , pages 2502–2508. IEEE, 2024. 

- [32] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

- [33] Dewei Wang, Xinmiao Wang, Xinzhe Liu, Jiyuan Shi, Yingnan Zhao, Chenjia Bai, and Xuelong Li. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains. _arXiv preprint arXiv:2506.08840_ , 2025. 

- [34] Huayi Wang, Wentao Zhang, Runyi Yu, Tao Huang, Junli Ren, Feiyu Jia, Zirui Wang, Xiaojie Niu, Xiao Chen, Jiahe Chen, et al. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system. _arXiv preprint arXiv:2510.11072_ , 2025. 

- [35] Wenjia Wang, Liang Pan, Zhiyang Dou, Jidong Mei, Zhouyingcheng Liao, Yuke Lou, Yifan Wu, Lei Yang, Jingbo Wang, and Taku Komura. Sims: Simulating stylized human-scene interactions with retrieval-augmented script generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 14117– 14127, 2025. 

- [36] Bowen Wen, Wei Yang, Jan Kautz, and Stan Birchfield. Foundationpose: Unified 6d pose estimation and tracking of novel objects. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17868–17879, 2024. 

- [37] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [38] Weiji Xie, Chenjia Bai, Jiyuan Shi, Junkai Yang, Yunfei Ge, Weinan Zhang, and Xuelong Li. Humanoid wholebody locomotion on narrow terrain via dynamic balance and reinforcement learning. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025. 

- [39] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid wholebody control for learning highly-dynamic skills. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [40] Zhanteng Xie and Philip Dames. Drl-vo: Learning to navigate through crowded dynamic scenes using velocity obstacles. _IEEE Transactions on Robotics_ , 39(4):2700– 2719, 2023. 

- [41] Sirui Xu, Hung Yu Ling, Yu-Xiong Wang, and Liang-Yan Gui. Intermimic: Towards universal whole-body control for physics-based human-object interactions. In _Proceedings of the Computer Vision and Pattern Recognition_ 

_Conference_ , pages 12266–12277, 2025. 

- [42] Wei Xu, Yixi Cai, Dongjiao He, Jiarong Lin, and Fu Zhang. Fast-lio2: Fast direct lidar-inertial odometry. _IEEE Transactions on Robotics_ , 38(4):2053–2073, 2022. 

- [43] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [44] Jianglong Ye, Keyi Wang, Chengjing Yuan, Ruihan Yang, Yiquan Li, Jiyue Zhu, Yuzhe Qin, Xueyan Zou, and Xiaolong Wang. Dex1b: Learning with 1b demonstrations for dexterous manipulation. In _Robotics: Science and Systems (RSS)_ , 2025. 

- [45] Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C. Karen Liu, and Jiajun Wu. Visualmimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [46] Chong Zhang, Wenli Xiao, Tairan He, and Guanya Shi. Wococo: Learning whole-body humanoid control with sequential contacts. In _Conference on Robot Learning_ , pages 455–472. PMLR, 2025. 

- [47] Yuanhang Zhang, Yifu Yuan, Prajwal Gurunath, Ishita Gupta, Shayegan Omidshafiei, Ali-akbar Agha-mohammadi, Marcell Vazquez-Chanlatte, Liam Pedersen, Tairan He, and Guanya Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 

- [48] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- [49] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. In _Conference on Robot Learning_ , pages 1975–1991. PMLR, 2025. 

## **Supplementary Appendix** 

VI. DETAIL OF IMPLEMENTATION 

### _A. Training and Simulation Setup_ 

We utilized NVIDIA Isaac Lab as the reinforcement learning simulation environment. The policy training was conducted on a high-performance computing platform equipped with eight NVIDIA RTX 3090 GPUs and dual AMD CPUs. For simulation-based validation experiments in MuJoCo, we utilized an Apple MacBook Pro powered by the M3 silicon chip. 

### _B. Perception Detail_ 

The FastLIO2 robot state estimator, FoundationPose object pose estimator, and the robot controller are fully deployed on the robot’s onboard NVIDIA Jetson Orin NX module. For realtime perception, we used the isaac-ros framework to interface the foundationpose model and trained the YOLOv8 model for the object. The YOLO results are converted to a mask, which is supplied to FoundationPose at the initial time. The object model is constructed by iPhone14 Pro using AR code Object Capture and converted to OBJ format with online tools. An external desktop workstation receives real-time estimates of the robot’s state for visualization and logging. Communication between the high-level motion controller and the Unitree low-level control interface is facilitated via the Lightweight Communications and Marshalling (LCM) protocol. Ultimately, we obtained object perception at approximately 40 Hz, robot state estimation at 200 Hz, and robot control at 50 Hz. 

### _C. Detail of Object State Estimation Module_ 

The drop detection logic relies on a spatial safety threshold _δ_ pos and a temporal window _N_ . Specifically, we define the safety region as a rectangular prism in the robot’s base frame, with dimensions of 0 _._ 4 _×_ 0 _._ 2 _×_ 0 _._ 4 m (length _×_ width _×_ height) and centered at _x_ = 0 _._ 35 m along the robot’s forward axis. The sliding window size for consistent state monitoring is set to _N_ = 10. The Digital Twin simulation is hosted on an external desktop workstation within the same local area network. It receives the robot’s object state stream via the ZeroMQ protocol. The module computes the object’s 

velocity in real time; upon triggering a drop event, the initial velocity for the physics simulation is derived by averaging the velocities from the last 3 frames to mitigate noise. Once the simulator predicts the final resting position, the module calculates the required gaze-adjustment pose and transmits it to the robot for recovery. 

### _D. Detail of Root Trajectory Planner_ 

In this appendix, we provide the detailed mathematical formulation for the hybrid root trajectory planner described in Section III-D2. This includes the quantitative retrieval metric for interaction priors, the explicit transformation from 2D navigation paths to 6-DoF root references, and the interpolation sequence construction. 

_1) Interaction Pose Prior:_ To retrieve the optimal grasping prior, we first formalize the spatial poses using rigid transformation matrices **T** _∈ SE_ (3), where each **T** encapsulates a rotation **R** _∈ SO_ (3) and a translation **p** _∈_ R<sup>3</sup> . Let _P_ = _{_ ( **T**<sup>(</sup> obj<sup>_i_)</sup><sup>_,_</sup><sup>**T**</sup> int<sup>(</sup><sup>_i_))</sup><sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>denotethelibraryofpriorposesextracted</sup> from the training dataset. These represent the object pose **T**<sup>(</sup> obj<sup>_i_)</sup> and the corresponding robot interaction pose **T**<sup>(</sup> int<sup>_i_)(relativeto</sup> the initial frame’s robot coordinate system) recorded at the onset of the contact phase. Given a newly detected relative object pose **T**<sup>cur</sup> obj<sup>,wedefineaweightederrorfunction</sup><sup>_Si_to</sup> quantify the similarity between the current state and the stored priors: 


where Φ( _·_ ) calculates the angular distance, and _wT , wR_ are weighting coefficients for translation and rotation errors, respectively. The system identifies the optimal prior index via _k_ = argmin _i Si_ . Subsequently, the target interaction pose is computed by compensating for the deviation between the current and prior object locations: 


This target is then transformed into the world frame based on the robot’s current root state to guide the policy. 


**Fig. 6:** The example of trajectory generation with contact information and simulated tracking contact. 

**TABLE V:** Hyperparameters related to PPO. 

**TABLE VI:** Reward terms and weights. 

|Hyperparameter|Value|
|---|---|
|Optimizer|Adam|
|Batch size|4096|
|Mini Batches|4|
|Learning epoches|5|
|Entropy coefficient|0.01|
|Value loss coefficient|1.0|
|Clip param|0.2|
|Max grad norm|1.0|
|Init noise std|1.0|
|Learning rate|1e-3|
|Desired KL|0.01|
|GAE _λ_|0.95|
|GAE _γ_|0.99|
|Actor MLP|[512,256,128]|
|Critic MLP|[512,256,128]|
|Activation|ELU|


|Term|Expression|Weight|
|---|---|---|
||Task||
|Global robot position|exp(_−∥_**_p_**_t −_ˆ**_p_**_t∥_<sup>2</sup>_/σ_rpos)<br>|0.5|
|Global robot orientation|exp(_−∥_**_r_**_t −_ˆ**_r_**_t∥_<sup>2</sup>_/σ_rrot)<br><br>|0.5|
|Global body position|exp(_−∥_**_p_**<sup>_b_</sup><br>_t _<sup>_−_ˆ</sup><sup>**_p_**</sup><sup>_b_</sup><br>_t_<sup>_∥_2</sup><sup>_/σ_bpos)</sup><br><br>|1.0|
|Global body orientation|exp(_−∥_**_r_**<sup>_b_</sup><br>_t _<sup>_−_ˆ</sup><sup>**_r_**</sup><sup>_b_</sup><br>_t_<sup>_∥_2</sup><sup>_/σ_brot)</sup><br><br>|1.0|
|Body linear velocity|exp(_−∥_**_v_**<sup>_b_</sup><br>_t _<sup>_−_ˆ</sup><sup>**_v_**</sup><sup>_b_</sup><br>_t _<sup>_∥_2</sup><sup>_/σ_bvel)</sup>|1.0|
|Body angular velocity|exp(_−∥_**_ω_**<sup>_b_</sup><br>_t _<sup>_−_ˆ</sup><sup>**_ω_**</sup><sup>_b_</sup><br>_t _<sup>_∥_2</sup><sup>_/σ_bang)</sup><br>|1.0|
|Object position|exp(_−∥_**_p_**<sup>_o_</sup><br>_t _<sup>_−_ˆ</sup><sup>**_p_**</sup><sup>_o_</sup><br>_t _<sup>_∥_2</sup><sup>_/σ_opos)</sup>|1.0|
||Regularization||
|Joint limits|I(**_q_** _/∈_[**_q_**min_,_**_q_**max])|-10.0|
|Undesired contacts|�I(_∥_**F**_∥>_1_._0)<br>|-0.1|
|Action rate|_∥_**_a_**_t −_**_a_**_t−_1_∥_<sup>2</sup>|-0.3|


_2) 2D-to-3D Waypoint Lifting:_ For long-horizon navigation, the TEB local planner generates a planar trajectory _T_ 2D = _{_ ( _xi, yi, ψi_ ) _}_<sup>_M_</sup> _i_ =1<sup>,where(</sup><sup>_xi, yi_)denotesthe2Dpositionand</sup> _ψi_ the yaw angle. To adapt this for our whole-body controller, we lift these 2D waypoints into a 6-DoF reference trajectory _T_ waypoints = _{_ **T** ref<sup>(</sup><sup>_i_)</sup><sup>_}_</sup> _i_<sup>_M_</sup> =1<sup>usingthefollowingformulation:</sup> 


Here, _h_ stand represents the robot’s default standing height, and **R** _z_ ( _ψi_ ) is the rotation matrix corresponding to the yaw angle _ψi_ , assuming zero roll and pitch to maintain stable locomotion. 

_3) Trajectory Interpolation Sequence:_ To ensure smooth transitions between navigation and manipulation phases, we construct a continuous time-parameterized trajectory _ξ_ ( _t_ ) using 6-DoF interpolation. The interpolation sequence explicitly includes intermediate ”via-points” adjusted to the standing height ( **T**<sup>up</sup> ) to prevent collision during approach and transport: 


The contact information _ct_ is manually set to 1 during the interval [ **T** target _,_ **T** end], and 0 otherwise. The example is shown in Figure 6. This sequence ensures the robot lifts its root to a safe height before and after interacting with the target **T** target or the final goal **T** end. 

### VII. SUPPLEMENTARY TABLES 

This section presents four tables detailing the implementation of our Pro-HOI framework. These tables specify the weights of the reward terms, the dimensions of the observation space, the domain randomization settings, and the hyperparameters used for training. 

### _A. Reward Terms and Weights_ 

All reward functions are detailed in Table VI. The overall reward design is divided into two categories: tracking rewards and regularization rewards. The _undesired contacts_ term is employed to penalize self-collisions between the robot’s links. Specifically, the set _B_ includes all robot bodies, with the exception of the ankles and wrists. The relative body includes the pelvis, hip, knee, ankle, shoulder, elbow, wrist, and torso links. 

### _B. Observation_ 

The specific observation items and dimensions for the Actor and Critic are detailed in Table VII. 

**TABLE VII:** Actor and critic observation state space. 

|State term|Actor Dim|Critic Dim|
|---|---|---|
|Global root position|3|3|
|Global root orientation|6|6|
|Relative object position|3|3|
|Relative object orientation|6|6|
|Contact information|1|1|
|Root projected gravity|3|3|
|Root angular velocity|3|3|
|Joint position|29|29|
|Joint velocity|29|29|
|Actions|29|29|
|Root linear velocity|–|3|
|Relative Body position|–|45|
|Relative Body orientation|–|90|
|**Total dim**|112|250|


### _C. Domain Randomization_ 

Since the physical characteristics of the simulator cannot accurately represent the real situation, we incorporate domain randomization during training to improve the transferability of trained polices to real-world or other simulations settings. The specific settings are given in Table VIII. 

### _D. PPO Hyperparameter_ 

The detailed PPO hyperparameters are shown in Table V. 

|**Domain Randomization**|**Sampling Distribution**|
|---|---|
|_Physical parameters_||
|Static friction coefficients|_µs ∼U_[0_._3_,_1_._6]|
|Dynamic friction coefficients|_µd ∼U_[0_._3_,_1_._2]|
|Restitution coefficient|_e ∼U_[0_,_0_._5]|
|Default joint positions|**_q_**0 _∼_**_q_**0+_U_[_−_0_._01_,_0_._01]|
|Base COM offset (x, y, z)|∆_x ∼U_[_−_0_._025_,_0_._025]_,_ ∆_y ∼U_[_−_0_._05_,_0_._05]_,_ ∆_z ∼U_[_−_0_._05_,_0_._05]|
|_Root velocity perturbations (exter_|_nal pushes)_|
|Root linear vel (x, y, z)|_vx ∼U_[_−_0_._5_,_0_._5]_, vy ∼U_[_−_0_._5_,_0_._5]_, vz ∼U_[_−_0_._2_,_0_._2]<br>|
|Push duration|∆_t ∼U_[1_,_3]s|
|Root angular vel|_ω_roll _∼U_[_−_0_._52_,_0_._52]_, ω_pitch _∼U_[_−_0_._52_,_0_._52]_, ω_yaw _∼U_[_−_0_._78_,_0_._78]|
|_Task related_||
|Object mass|scale_o ∼U_[0_._5_,_2_._0]|


**TABLE VIII:** Domain randomization parameters applied during training. _U_ [ _·_ ]: uniform distribution. 

