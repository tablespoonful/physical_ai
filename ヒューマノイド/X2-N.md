---
title: "X2-N: A Transformable Wheel-legged Humanoid Robot with Dual-mode Locomotion and Manipulation"
date: "2026-04-23"
authors: "Yan Ning; Xingzhou Chen; Delong Li; Hao Zhang; Hanfu Gai; Jinlei Zhao"
url: https://arxiv.org/abs/2604.21541
pdf: https://arxiv.org/pdf/2604.21541
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.21541)** / [論文ページ](https://arxiv.org/abs/2604.21541)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

## **X2-N: A Transformable Wheel-legged Humanoid Robot with Dual-mode Locomotion and Manipulation** 

Yan Ning<sup>1</sup> , Xingzhou Chen<sup>1</sup> , Delong Li<sup>2</sup> , Hao Zhang<sup>2</sup> , Hanfu Gai<sup>2</sup> , Jinlei Zhao<sup>2</sup> , Tongyuan Li<sup>2</sup> , Cheng Zhang<sup>2</sup> , Zhihui Peng<sup>2</sup> and Ling Shi<sup>1</sup> 

**_Abstract_ — Wheel-legged robots combine the efficiency of wheeled locomotion with the versatility of legged systems, enabling rapid traversal over both continuous and discrete terrains. However, conventional designs typically employ fixed wheels as feet and limited degrees of freedom (DoFs) at the hips, resulting in reduced stability and mobility during legged locomotion compared to humanoids with flat feet. In addition, most existing platforms lack a full upper body with arms, which limits their ability to perform dexterous manipulation tasks.** 

**In this letter, we present X2-N, a high-DoF transformable robot with dual-mode locomotion and manipulation. X2-N can operate in both humanoid and wheel-legged forms and transform seamlessly between them through joint reconfiguration. We further propose a reinforcement learning (RL)-based wholebody control framework tailored to this morphology, enabling control across hybrid locomotion, transformation, and manipulation. We validate X2-N in a range of challenging locomotion and manipulation tasks, including dynamic skating-like motion, stair climbing and package delivery. Results demonstrate high locomotion efficiency, strong terrain adaptability, and stable loco-manipulation performance of X2-N, highlighting its potential for real-world deployment.** 

#### I. INTRODUCTION 

In recent years, agile legged robots with high degrees of freedom (DoFs) have achieved significant progress in both research and industry. Among them, humanoid and wheellegged robots have emerged as two prominent platforms. 

Humanoid robots [1–3] exhibit impressive capabilities in robust dynamic locomotion and dexterous manipulation through a high-DoF full-body design. Their bipedal structure with flat feet also provides robust standing with minimal ground occupancy, thereby benefiting static manipulation. However, during movement, legged locomotion involves frequent impacts to the body and compromises operational stability. Moreover, on continuous and flat terrains typical in industrial or civil scenarios, legged locomotion is generally less energy efficient, slower, and less stable compared to wheel-legged systems. 

Wheel-legged robots integrate wheels into legged systems to improve locomotion efficiency and terrain adaptability [4– 6]. They can achieve stable operation during smooth wheeled 

> 1Department of Electronic and Computer Engineering, The Hong Kong University of Science and Technology, Hong Kong, China. 

> 2X-lab Department, Agibot Innovation Company, Shanghai, China. Email: _{_ yningaa, xchenfk _}_ @connect.ust.hk, lidelong@agibot.com, ahaobupt@gmail.com, gaihanfu@live.com, in ~~b~~ arrel@outlook.com, 

> _{_ zhangcheng, pengzhihui _}_ @zhiyuan-robot.com, eesling@ust.hk 


Fig. 1: Illustration of X2-N in dual locomotion modes with 4/7-DoF arms, operating on stairs and slopes. 

locomotion, but suffer from unsteady point-contact constraints during legged locomotion. Moreover, most systems are designed with limited-DoF legs and only lower bodies, restricting their capabilities in manipulation compared to humanoids. Therefore, it remains challenging for existing robotic platforms to simultaneously achieve efficient, agile locomotion together with stable, dexterous manipulation in a unified form for practical applications. 

In this paper, we present X2-N, a high-DoF transformable wheel-legged humanoid robot with dual working modes. The robot can operate in either wheel-contact or foot-contact configurations for agile and efficient locomotion, and can interchange between 4-DoF and 7-DoF arms for manipulation. X2-N can transition seamlessly between these modes for the most suitable, efficient and stable operation form with a compact size and weight. 

To control this dual-mode system, we develop a hierarchical control framework tailored to the proposed morphology. It combines a reinforcement learning (RL)-based controller with a model-based whole-body controller for hybrid locomotion, mode transformation, and loco-manipulation. We validate the effectiveness and robustness of X2-N through simulation and hardware experiments. 

Our **contributions** are summarized as follows: 

(1) We present X2-N, a novel transformable robot platform that integrates features of both wheel-legged and humanoid robots. The system is built upon customized hardware and actuators, enabling both efficient locomotion and dexterous manipulation within a unified design. 

(2) We propose a new lower-limb joint configuration and mechanism that support both wheel- and foot-contact modes without introducing redundant DoFs for transformation and steering. The legs of X2-N preserve sufficient workspace and maneuverability comparable to existing humanoid legs. 

(3) We develop a hybrid hierarchical control framework for the proposed dual-mode transformable morphology. The framework enables X2-N to switch between specific RLbased agents with a shared whole-body model-based controller for the most suitable operation form. 

(4) We will open-source parts of the robot design, hardware and software interfaces, and control framework to enable researchers to customize and further develop on this transformable robot platform. 

#### II. RELATED WORK 

#### _A. Humanoid Platforms_ 

Humanoid robots have achieved remarkable progress in dynamic locomotion and dexterous manipulation through high-DoF full-body structures and articulated limbs. Their anthropomorphic morphology provides large workspace, versatile contact capability, and effective whole-body interaction with human-oriented environments. Representative platforms such as Atlas [1], G1 [2], and Helix [3] demonstrate agile locomotion, dynamic balancing, and generalized operation for practical applications. 

However, existing humanoid robots are generally optimized for a fixed morphology, which inherently introduces a trade-off between locomotion efficiency and operational capability. Although legged locomotion provides excellent terrain adaptability and whole-body interaction ability, repeated foot-ground contacts introduce additional energy consumption and motion complexity, especially during long-distance traversal. Therefore, achieving both efficient mobility and dexterous operation remains a fundamental challenge for humanoid robot design. 

#### _B. Wheel-Legged Platforms_ 

Wheel-legged robots combine the terrain adaptability of legged systems with the efficiency of wheeled locomotion. Representative quadrupedal platforms such as ANYmal [7] and B2-W [8] demonstrate robust mobility across challenging terrains, while compact bipedal platforms including Tron 1 [5] and DIABLO [6] achieve agile locomotion in constrained environments. Compared with conventional humanoids, these platforms significantly improve locomotion efficiency on continuous and structured terrains. 

Despite their mobility advantages, most existing wheellegged robots are primarily designed with locomotion efficiency as the first priority. Their simplified limb structures and lower-body-focused configurations reduce mechanical 


Fig. 2: Overview of different classic legged robot platforms. 

complexity but limit dexterous manipulation and wholebody interaction capabilities. Although several platforms introduce lightweight manipulators for loco-manipulation [9, 10], their limited DoF and non-humanoid configurations still restrict versatile operation compared with humanoid systems. Furthermore, wheeled locomotion usually provides limited support configurations for complex manipulation tasks. 

Similar to humanoid robots, current wheel-legged platforms generally adopt fixed morphologies. A robotic platform that can combine the advantages of both morphologies remains largely unexplored. 

#### _C. Control of High-DoF Legged Robot_ 

Whole-body control of high-DoF robots has been dominated by model-based optimization methods, such as inverse dynamics, quadratic programming, and model predictive control [11]. These methods provide accurate motion tracking and force regulation but rely heavily on model accuracy and computational efficiency, limiting their robustness under highly dynamic and uncertain contact conditions. 

Reinforcement learning has recently enabled agile locomotion and loco-manipulation with improved robustness against modeling uncertainties [12, 13]. However, existing learningbased methods mainly focus on dynamic locomotion and generally lack the precise manipulation capability of modelbased controllers. 

Hybrid control frameworks have recently combined learning-based locomotion policies with model-based wholebody controllers, leveraging the advantages of both approaches [7, 10]. However, existing control frameworks mainly assume fixed robot morphologies and predefined contact configurations. For robots with multiple operating mode, the controller must have additionally coordination across different configurations, which remains underdeveloped. 

Overall, existing humanoid and wheel-legged robots represent two distinct design paradigms, where humanoids prioritize dexterous whole-body interaction while wheellegged systems emphasize efficient mobility. However, these advantages are difficult to simultaneously achieve within a fixed morphology. A transformable robotic platform that can 


Fig. 3: Illustration of X2-N’s specifications. 

dynamically switch between efficient wheeled locomotion and humanoid-level operation remains unexplored. Moreover, such a system requires a control framework capable of coordinating locomotion, transformation, and manipulation across different morphologies. These challenges motivate the development of X2-N presented in this work. 

#### III. SYSTEM DESIGN 

#### _A. Overview_ 

X2-N is a fully electric and mid-sized wheel-legged humanoid robot with both wheel-legged and foot-legged modes. It weighs approximately 30.7 kg and stands 1.3 m tall, as shown in Fig. 3. The system consists of a torso, a waist, two arms, and two legs, primarily constructed from aluminum. 

The standard configuration of X2-N has 21 DoFs in footlegged mode and 17 DoFs in wheel-legged mode to accommodate the distinct requirements of the two locomotion modes. Through a unified mechanical design, the system supports both transformation and locomotion without introducing additional actuators, thereby avoiding increased system weight and complexity. The upper body adopts a modular design with interchangeable manipulators, supporting both lightweight operation and dexterous manipulation. Detailed designs of the lower limbs, upper body, and actuation system are presented in the following sections. 

#### _B. A Two-mode Transformable Leg Design_ 

Designing a unified robot platform that integrates humanoid and wheel-legged configurations is challenging due to their mismatched kinematic structures, particularly in degrees of freedom (DoFs) and contact constraints. Moreover, enabling transformation between two modes typically requires additional dedicated actuation. To address this issue, we propose a transformable lower-limb architecture based on a joint reuse principle, to support both locomotion and transformation within a unified design. 

In foot-legged mode, the lower body consists of 13 DoFs, including a 1-DoF waist yaw joint and two 6-DoF legs. Each leg follows a conventional humanoid topology with a 3-DoF hip (pitch, roll, yaw), a 1-DoF knee (pitch), and a 2-DoF ankle (pitch, roll). Departing from standard designs, we introduce a topology-level reconfiguration by relocating 


Fig. 4: Illustration of X2-N’s structural details (linkage and locking mechanism), and joint topology in different modes. 

the yaw joint. Specifically, the traditional flat foot is replaced by a wheel integrated with a direct-drive hub motor. Such motor is further reused as the yaw joint of the leg, effectively replacing the conventional yaw joint in the hip. By shifting leg yaw joint to the end-effector, X2-N integrates wheelsteering motors while preserving humanoid-compatible kinematics. The workspace and maneuverability of the proposed topology are analyzed along with a conventional humanoid leg in Section V, demonstrating a comparable operational capability. To further improve dynamic performance and motion agility, the knee and ankle pitch actuators are relocated closer to the CoM for reducing limb inertia [14, 15]. We further design four-bar linkage mechanisms within the limbs for power and torque transmission of these joints. 

In wheel-legged mode, as the yaw motion of X2-N can be achieved through wheel-velocity differentiation, the need for an explicit leg yaw joint is eliminated. Therefore, each leg is reconfigured to a 4-DoF topology including wheel steering. To omit redundant DoFs in leg of this mode, we design a structural locking mechanism and utilize the position control of ankle roll actuator to rigidly lock the wheel mount with the calf. Specifically, the mechanism has a retaining clip structure and adopt multiple contact interfaces to stabilize the wheel twist during locomotion, as shown in Fig. 4. 

The mode transformation is achieved by reusing the ankle roll joint to actively drive the orientation of wheel motors from horizontal foot-contact to vertical wheel-contact form. Detailed transformation control process is described in the following controller section IV. Notably, during transformation, the locking mechanism can also adopt positioning and leading the ankle to the calf with a sliding slot structure. 

Through the design principle of joint reuse, topology reconfiguration and a locking mechanism, X2-N eliminates the need for additional dedicated actuators. Therefore, it achieves dual locomotion modes and transformation within 

a compact and efficient mechanical structure. 

#### _C. Upper Limb Design_ 

A key design consideration for the arms is the trade-off between manipulation dexterity and dynamic agility. To balance both demands, we adopt a modular and interchangeable upper-limb design as illustrated in Fig. 4, enabling the system to equip either configuration based on the requirements. 

In the basic configuration of X2-N, each upper limb provides 4 DoFs, including 2 DoFs in shoulder (pitch and roll), 1 DoF in upper arm (yaw), and 1 DoF in elbow (pitch). This configuration is designed for tasks such as bodybalancing and payload delivery. The forearm is implemented as a rigid link for efficient motion and load bearing. 

To enhance manipulation capability, the forearm can be replaced with a modular 3-DoF wrist unit (yaw, roll, pitch). The module can be installed at the elbow with minimal assembly effort. A linkage mechanism is employed to align the wrist joint axes to intersect in space, improving endeffector maneuverability. The arm can be equipped with a gripper or dexterous hand as end-effectors. 

_D. Actuators_ 

TABLE I: Actuator specifications 

|Actuator|R90|R57|R52|R52-U|
|---|---|---|---|---|
|Mass (g)|990|370|360|410|
|Gear ratio|16|40|36|72|
|Peak torque (Nm)|120|30|20|40|
|Peak speed (rpm)|105|110|130|65|


R90: shoulder pitch, hip pitch/roll, knee, waist; R57: shoulder roll; R52: arm yaw, ankle roll; R52-U: elbow, ankle pitch. 

To achieve high dynamic locomotion and manipulation performance, four types of customized actuators are developed, with specifications summarized in Table I. These actuators adopt quasi-direct-drive designs with planetary gear reductions, providing high torque density, low rotor inertia, and low rotational friction. Such characteristics enable a near-linear relationship between motor current and output torque, avoiding the need for extra torque sensors [16]. Hightorque actuators are assigned to load-intensive joints, including the shoulder, hip, and knee, while compact actuators are adopted for other joints to reduce the overall system weight. 

#### IV. CONTROL FRAMEWORK 

The control framework of X2-N integrates RL-based agents for locomotion and transformation, with a modelbased whole-body controller for manipulation, as illustrated in Fig. 5 

#### _A. Locomotion Controller_ 

The RL-based locomotion controller is realized through Proximal Policy Optimization (PPO) [17] with an actor–critic architecture. We design three independent agents for locomotion and the controller can switch between them based on working scenarios, which are defined as follows: 


Fig. 5: Illustration of X2-N’s control architecture. 

- **Wheel-legged mode** , which employs wheel propulsion and steering with the legs for posture adjustment. 

- **Foot-legged mode** , which relies on legged stepping and turning with flat feet for locomotion. 

- **Hybrid mode** , which combines the above behaviors to enable dynamic, skating-like motion, thereby fully exploiting the locomotion capabilities of X2-N. 

All policies are trained in the Isaac Gym simulator [18] and validated in the MuJoCo simulator [19] before real-world deployment. They share the same observation and action formulation. The observation vector consists of body pose, linear and angular velocities, joint positions, velocities, and torques. The actions are defined as desired joint position commands executed by the low-level joint controllers. 

Low-level actuation employs a torque–position–velocity hybrid controller following the MIT control policy [16]. The control bandwidth is 50 Hz for learning policy inference, and 1 kHz for state estimation and actuator-level control. 

_1)_ **_Wheel-legged Agent with Centrifugal Compensation_** _:_ Wheel-legged locomotion on X2-N presents significant challenges due to the high-DoF legs, heavy upper body, and elevated CoM, compared to conventional wheel-legged robots. These factors make it more difficult to maintain balance while achieving agile locomotion, especially during highspeed maneuvers and turning. To address this, we employ a two-stage RL training strategy. 

- In **Stage A** , we first train the policy to learn fundamental wheel-based balance and velocity tracking on a flat terrain. We apply limited domain randomization and noise, and regularize joint motion to reference states. 

- In **Stage B** , the level of terrain complexity is progressively increased with uneven types, such as slopes, stairs, and low-friction surfaces to improve locomotion robustness. The reference joint states are removed to allow the policy exploiting coordinated motion of both wheels and high-DoF legs for adaptive locomotion. 

**Centrifugal effects** substantially impacts locomotion stability of X2-N with elevated CoM during high-speed turning. Therefore, we introduce a body-leaning strategy that tilts 

the CoM toward the turning center, using gravity for partial compensation. During training, we design a centrifugalforce-aware reward term _R_ cen based on a single rigid body model. The desired CoM tilt angle _θ_<sup>des</sup> and the corresponding reward can be derived as: 


where _vx_ and _ω_ yaw are the robot forward velocity and yaw angular velocity. _g_ is the gravity term, and _a_<sup>obs</sup> _y_ is the lateral-direction acceleration measured by the IMU. The constant 0.3 limits excessive body inclination for safety. This reward encourages the robot to generate appropriate body lean during turning for enhanced locomotion stability. 

_2)_ **_Foot-legged Agent with Human Gait Mimicry_** _:_ The key distinction of foot-legged locomotion on X2-N compared to humanoid robots lies in its joint topology reconfiguration, where the hub motor is repurposed as the leg’s yaw joint. To achieve more bio-inspired motion and improve walking naturalness, we incorporate human gait data from the AMASS library [20] into the controller. To achieve these capabilities, we adopt a two-stage training process. 

- In **Stage A** , the robot is trained on flat terrain to coordinate the yaw hub motor during stepping and turning, following desired commands. We apply a human-mimic reward _R_ mimic to encourage the lower limb joints of X2N to replicate human joint reference **q** ref. The reward _R_ mimic is defined as: 


- In **Stage B** , the training environment is gradually diversified with stairs, slopes, and rough terrains, promoting robustness of high-dynamic locomotion. During this stage, the mimic reward is removed to prioritize locomotion performance. Nevertheless, the learned policy implicitly retains the human-like walking style. 

_3)_ **_Hybrid Wheel-legged Agent_** _:_ Training hybrid wheellegged controller is challenging due to the unsteady bipedal single-point contacts between the arc-shaped wheel surfaces and the ground, compared to flat-foot contacts. To address such challenges, we adopt a three-stage RL curriculum. 

- In **Stage A** , we train the robot with a frequent stepping cycle (T = 0.5 s) on flat terrains, faster than normal walking. By rapidly switching support points, the narrow-contact issue can be overcome. We further define a curve trajectory for the swing-leg end-effector. 

- In **Stage B** , the stepping duration is extended longer to 1.2s in each complete leg-switch cycle. We incorporated human walking data like foot-legged controller for bioinspired gaits using the same reward _R_ mimic in footlegged agent. 

- In **Stage C** , the training task becomes purely following body velocity commands without any reference trajectories. This allows the policy to develop adaptive stepping 


Fig. 6: Illustration of X2-N’s transformation processes. The top figures show the transition from foot-legged to wheellegged; the bottom figures show the inverse mode transition. 

behaviors. We then gradually introduce rough terrains for robustness under high-speed locomotion. Notably, we penalize hub motor speed to zero at stepping contact instant to reduce jitter and vibration to the body. 

#### _B. Transformation Controller_ 

The training setup of the transformation controller is similar as the locomotion controller. The core challenge lies in maintaining balance under inherently unstable changing ground contacts during smooth and robust mode transformation. To address this, we design two distinct transformation strategies for wheel-to-foot and foot-to-wheel transitions, illustrated in Fig. 6. 

_1)_ **_From foot-legged mode to wheel-legged mode_** _:_ We apply a direct ankle twisting control to reorient the wheels from horizontal to vertical transitioning mode from foot to wheel. This approach follows the potential-energy-descent principle due to the CoM depression in wheel-legged mode. The mechanical components assistant with a rapid and precise ankle locking during the process. 

_2)_ **_From wheel-legged mode to foot-legged mode_** _:_ We implement two distinct stepping motions while rotating the ankle and wheel during the air time of each step, transitioning wheel to foot. Since single-point contact is inherently unstable, the transformation duration is gradually refined to achieve smooth transformation and balance. 

During training of each process, offline joint trajectories for each transformation process are precomputed using forward kinematics. We assign each mode a fixed phase signal, and formulate the joint trajectories as a function of this signal and the transforming duration. The robot is then trained to maintain locomotion balance during transformation while following pre-defined joint trajectories. We specially define a balance reward _R_ balance during the process: 


to stabilize the body CoM and pose, where _k_ 1 to _k_ 4 are term weights, _θ_ roll _, θ_ pitch _, ω_ roll _, ω_ pitch are the pose angles and velocities in roll and pitch orientations, and _σθ, σω_ are the scale parameters to control decay rate. 

#### _C. Whole-body Controller_ 

The whole-body controller is developed for task-oriented loco-manipulation, while the RL controller provides dynamic locomotion policies for balance stabilization and contact adaptation. The estimated robot states are shared with the RL agents as observations, and the whole-body controller generates commands in complement to RL-based actions. 

For task-driven target poses, we define end-effector trajectories with pose, velocity, and force vectors in Cartesian space. The desired joint positions **q** and velocities **˙q** are then computed via inverse kinematics and the endeffector Jacobian matrices **J** ee. Furthermore, the required joint torques _τ_ can be derived from external forces **F** ext using the Newton–Euler dynamic equations: 


where **M** ( **q** ) _,_ **C** ( **q** _,_ **˙q** ) _,_ **g** ( **q** ) represents the mass-inertia matrix, Coriolis, centrifugal and gravity terms. The derived joint positions, velocities, and torques are executed on the actuators via a low-level PD controller, following the MIT control policy [16]. 


The locomotion and operational capabilities of X2-N were validated through both simulation and experiments across diverse scenarios, demonstrating the effectiveness of the hybrid novel form and the robustness of the platform. 

#### _A. Workspace analysis_ 

To evaluate the impact of the proposed joint reconfiguration in foot-legged mode, we compare the kinematic workspace and maneuverability of the X2-N’s leg with that of a conventional humanoid leg. For a fair comparison, both configurations share identical thigh and calf lengths, and the illustration is shown in Fig. 7. The corresponding Denavit–Hartenberg (DH) parameters and transformation matrices are derived to formulate the forward kinematics from the floating base (waist) to the end-effector (foot). 


Fig. 7: Leg-joint configuration comparison of workspace and manipulability between X2-N and conventional humanoid. 

construct workspace mesh surfaces, and the volume is evaluated using both convex hull coverage [22] and voxel grid occupancy [23] methods. 

To further assess kinematic performance, we evaluate Yoshikawa’s manipulability index _w_ [24] for both configurations. For a consistent comparison, matched sampling points with the same spatial coordinates of both configurations are identified, and the mean manipulability _w_ ¯ is computed as: 


where _N_ is the number of matched samples, and **J** ee( **q** _k_ ) denotes the Jacobian matrix at _k_ -th joint configuration **q** _k_ . The results show that the proposed topology achieves a workspace volume and mean manipulability comparable to those of a conventional humanoid leg (see Table II). Although a slight reduction in workspace is observed, the difference has minimal impact on foot placement in typical locomotion scenarios. These results indicate that the proposed joint reconfiguration preserves high locomotion capability while enabling additional functionality for transformation and wheel integration. 

TABLE II: Workspace and maneuverability comparison 

#### _B. Locomotion Performance and Energy Evaluation_ 

|Configuration|X2-N leg|Normal leg|Ratio|
|---|---|---|---|
|Volume (voxel)|0.603|0.743|81.16%|
|Volume (convex hull)|1.440|1.640|87.80%|
|Mean manipulability|0.0140|0.0154|90.91%|
|Max manipulability|0.0302|0.0359|84.12%|


Considering joint limits, the reachable workspace of each configuration is sampled using a Monte Carlo method [21], as illustrated in Fig. 7. The sampled points are used to 

Real-world locomotion performance was evaluated in wheel-legged, foot-legged, and hybrid modes, as illustrated in Figs. 8 and 9. In wheel-legged mode, we tested X2N to traverse small ramps, perform in-place rotations on slopes, descend steps on stairs, and recover from external pushes. The legs act as an active suspension system, allowing traversal of highly uneven terrains. In foot-legged mode, X2-N behaves as a mid-size humanoid robot, performing anthropomorphic walking, stair and slope climbing, and push recovery. Moreover, we evaluated the hybrid wheel-legged 


Fig. 8: Three different locomotion modes of X2-N and average cost of transport. 

TABLE III: Power and energy evaluation. 

|Velocity|Mode|_P_ <sup>avg</sup><br>mech<br>(W)|_P_ <sup>avg</sup><br>elec<br>(W)|CoTmech|CoTelec|
|---|---|---|---|---|---|
||walk|38.44|133.29|0.498|1.723|
|0.4 m/s|wheel<br>hybrid|**10.73**<br>–|**94.17**<br>–|**0.077**<br>–|**0.672**<br>–|
||walk|35.33|127.63|0.276|0.998|
|0.6 m/s|wheel|**15.80**|**99.15**|**0.080**|**0.501**|
||hybrid|61.65|110.94|0.366|0.659|
||walk|94.09|173.12|0.895|1.650|
|1.0 m/s|wheel|**32.28**|**110.76**|**0.094**|**0.322**|
||hybrid|65.43|112.65|0.309|0.533|


locomotion mode, enabling agile and robust “skating” and “space-walking” behaviors. 

Energy consumption was analyzed across different locomotion modes by calculating both mechanical and electrical power during locomotion cycles. The total energy consumption and cost of transport (CoT) formulas are as follows: 


where _τi_ ( _k_ ) and _q_ ˙ _i_ ( _k_ ) denote the torque and angular velocity of joint _i_ at time step _k_ , _Vk_ , _Ik_ are the discrete voltage and current obtained from the battery management system, _d_ is the total travel distance. 

As illustrated in Table III, legged locomotion experiences substantial impact power during each gait cycle, which can lead to structural fatigue and increased thermal load in the joints. In contrast, wheel-legged rolling can reduce joint peak load and energy consumption at equivalent forward speeds, 


Fig. 9: Experiments of X2-N on different scenarios. 

demonstrating superior stability, efficiency, and robustness, and highlighting its practical advantages for diverse realworld constructed scenarios. 

#### _C. Transformation and locking system Performance_ 

Transformation performance and repeatability were evaluated on constrained flat terrain, including both wheel-to-foot and foot-to-wheel transitions. The locking mechanism was further validated through mechanical analysis and hardware experiments with total 180 transformation cycles: 150 noload cycles and 30 full-load cycles. We analyzed the transformation time _T_ trans, body position and orientation deviation _e_ CoM _, e_ ori, and the success rate. 

From the results in Table IV, each transformation was completed within approximately 2 seconds. During the transformation process, the robot maintained stable body posture with minor pose deviations. However, a small number of failure cases were observed, mainly attributed to mechanical component degradation after repeated operation. 

TABLE IV: Transformation performance evaluation. 

|Motion|_T_trans|_e_CoM|_e_ori|Success|rate (%)|
|---|---|---|---|---|---|
||(s)|(m)|(deg)|No-load|Full-load|
|Wheel to foot|2.53|0.309|28.48|100|90.0|
|Foot to wheel|1.85|0.183|4.58|100|100|


#### _D. Ablation Study of Rewards in RL-agents_ 

We further analyzed the contributions of the core reward components used in the RL agents. The ablation experiments demonstrate that the centrifugal-force compensation reward _R_ cen improves turning agility and stability; the mimic reward _R_ mimic reduces joint position errors with respect to 

REFERENCES 


Fig. 10: Ablation experiments results for key agent rewards. 

the reference trajectories; and the balance reward _R_ balance enables faster stabilization during the transformation process. Detailed experimental results are summarized in Fig. 10 and the supplementary materials. 

#### _E. Operation Performance_ 

We further assessed X2-N’s operational capabilities under both locomotion modes across diverse scenarios. Illustrations of different tests are shown in Fig. 9. Leveraging its highDoF upper limbs and grippers, X2-N can perform package carrying and object manipulation, while stationary and during locomotion, including operation on stairs and slopes. 

In stationary conditions, the foot-legged mode provides superior resistance to external forces and heavy payloads, maintaining steadier body and end-effector states. Conversely, during movement, the wheel-legged mode effectively mitigates oscillations induced by high-frequency ground impacts during legged walking, enabling smoother and more stable loco-manipulation performance. 

#### VI. CONCLUSION AND FUTURE WORK 

In this work, we presented X2-N, a novel transformable wheel-legged humanoid robot capable of dual-mode locomotion and manipulation. The proposed lower-limb joint topology reconfiguration and transformation mechanism enable seamless switching between wheel-legged and footlegged modes without introducing redundant actuators. The workspace of X2-N’s leg is preserved to be comparable to conventional humanoid legs. Moreover, the interchangeable arm design further enhances operational versatility. 

A RL-based whole-body control framework was developed and tailored to this morphology. It integrates multiple hybrid locomotion with manipulation behaviors and allows the robot to transform for the most suitable operation mode under different tasks. Extensive simulation and real-world experiments validate the advantages of X2-N with transformable design, demonstrating agility, efficiency and adaptability in locomotion as well as reliability in operation. 

- [1] Boston Dynamics, “All new atlas,” YouTube, Apr. 2024. [Online]. Available: https://www.youtube.com/watch?v=29ECwExc- ~~M~~ 

- [2] Unitree Robotics, “Unitree g1: Humanoid agent ai avatar,” Unitree Robotics Official Website, 2025. [Online]. Available: https://www. unitree.com/g1/ 

- [3] Figure, “Helix 02 living room tidy,” YouTube, Mar. 2026. [Online]. Available: https://www.youtube.com/watch?v=CAdTjePDBfc 

- [4] M. Bjelonic, P. K. Sankar, C. D. Bellicoso, H. Vallery, and M. Hutter, “Rolling in the deep – hybrid locomotion for wheeled-legged robots using online trajectory optimization,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 3626–3633, 2020. 

- [5] LimX Dynamics, “Tron 1,” LimX Dynamics Official Website, 2024. [Online]. Available: https://www.limxdynamics.com/zh/products/tron1 

- [6] D. Liu, F. Yang, X. Liao, and X. Lyu, “DIABLO: A 6-DoF wheeled bipedal robot composed entirely of direct-drive joints,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 3605–3612. 

- [7] J. Lee, M. Bjelonic, A. Reske, L. Wellhausen, T. Miki, and M. Hutter, “Learning robust autonomous navigation and locomotion for wheeledlegged robots,” _Science Robotics_ , vol. 9, no. 89, p. eadi9641, 2024. 

- [8] Unitree Robotics, “Unitree B2-W,” 2026. [Online]. Available: https://www.unitree.com/mobile/b2-w/ 

- [9] J. Cheng, D. Kang, G. Fadini, G. Shi, and S. Coros, “Rambo: Rlaugmented model-based whole-body control for loco-manipulation,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 10, pp. 9462– 9469, 2025. 

- [10] Y. Ma, A. Cramariuc, F. Farshidian, and M. Hutter, “Learning coordinated badminton skills for legged manipulators,” _Science Robotics_ , vol. 10, no. 102, p. eadu3922, 2025. 

- [11] Y. Ding, C. Khazoom, M. Chignoli, and S. Kim, “Orientationaware model predictive control with footstep adaptation for dynamic humanoid walking,” in _IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids)_ , 2022, pp. 299–305. 

- [12] Z. Li, X. Cheng, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for robust parameterized locomotion control of bipedal robots,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 2811–2817. 

- [13] Y. Zhang, Y. Yuan, P. Gurunath, T. He, S. Omidshafiei, A.-a. Aghamohammadi, M. Vazquez-Chanlatte, L. Pedersen, and G. Shi, “Falcon: Learning force-adaptive humanoid loco-manipulation,” _arXiv preprint arXiv:2505.06776_ , 2025. 

- [14] D. E. Orin, A. Goswami, and S.-H. Lee, “Centroidal dynamics of a humanoid robot,” in _13th IEEE-RAS International Conference on Humanoid Robots (Humanoids)_ , 2013, pp. 161–167. 

- [15] Y. Sim and J. Ramos, “Tello leg: The study of design principles and metrics for dynamic humanoid robots,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 4, pp. 9318–9325, 2022. 

- [16] P. M. Wensing, A. Wang, S. Seok, D. Otten, J. Lang, and S. Kim, “Proprioceptive actuator design in the mit cheetah: Impact mitigation and high-bandwidth physical interaction for dynamic legged robots,” _IEEE Transactions on Robotics_ , vol. 33, no. 3, pp. 509–522, 2017. 

- [17] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [18] NVIDIA Corporation, “Isaac gym - preview release,” 2021. [Online]. Available: https://developer.nvidia.com/isaac-gym 

- [19] G. DeepMind, “Mujoco physics simulator,” 2023. [Online]. Available: https://github.com/google-deepmind/mujoco 

- [20] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “Amass: Archive of motion capture as surface shapes,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 5442–5451. 

- [21] N. Metropolis and S. Ulam, “The monte carlo method,” _Journal of the American Statistical Association_ , vol. 44, no. 247, pp. 335–341, 1949. 

- [22] A. Skuric, V. Padois, and D. Daney, “Approximating robot reachable space using convex polytopes,” Nov. 2022. 

- [23] P. Anderson-Sprecher and R. G. Simmons, “Voxel-based motion bounding and workspace estimation for robotic manipulators,” in _Proc. IEEE Int. Conf. Robotics and Automation (ICRA)_ , St. Paul, MN, USA, May 2012, pp. 2141–2146. 

- [24] T. Yoshikawa, “Manipulability of robotic mechanisms,” _The International Journal of Robotics Research_ , vol. 4, no. 2, pp. 3–9, 1985. 

# **Supplementary Experimental Evaluation** 

Supporting Material for the RA-L Manuscript: 

- _“X2-N: A Transformable Wheel-Legged Humanoid Robot with Dual-Mode Locomotion and Manipulation”_ 

Related manuscript: arXiv:2604.21541 


**Figure 1:** Overview of the X2-N platform with dual locomotion modes and different arm configurations. 

### **1 Overview** 

This supplementary document provides additional experimental evaluations to characterize the performance of the proposed X2-N transformable wheel-legged humanoid robot. Beyond the demonstrations presented in the main manuscript, these experiments provide more detailed quantitative metrics and assessments of its functional capabilities. 

Furthermore, these evaluations address the major concerns raised by the reviewers regarding the core functionalities. The newly added experiments provide further quantitative evidence and supplementary analysis to strengthen the validation of the proposed system under the available experimental conditions. Some long-term engineering evaluations and additional test scenarios may be further explored in future work. 

Five experiments are conducted, covering locomotion efficiency, transformation capability, locking system reliability, control performance, and workspace analysis, as summarized in Table 1. Detailed experimental setups, evaluation metrics, and results are presented in the following sections. 

**Table 1:** Organization of the supplementary experiments. 

|**Exp.**|**Title**|**Sec.**|
|---|---|---|
|Exp. 1|Energy efficiency evaluation under different locomotion modes.|3|
|Exp. 2|Repeatability and stability evaluation of bidirectional transformation.|4|
|Exp. 3|Engineering validation of the locking mechanism.|5|
|Exp. 4|Ablation studies of the reinforcement learning reward components.|6|
|Exp. 5|Comparison evaluation of 4-DoF and 7-DoF interchangeable arms|7|


1 

### **2 Fundamental Experimental Setup** 

#### **2.1 X2-N Robot Specification** 

The hardware specification of X2-N prototype is shown below as Table 2. 

**Table 2:** Robot specifications of the X2-N prototype. 

|**Item**|**Specification**|
|---|---|
|Dimensions (H×L×W)|1_._30×0_._47×0_._23 m|
|Mass|30.7 kg|
|Degrees of Freedom (DoF)|21 (Foot-legged Mode) / 17 (Wheel-legged|
||Mode)|
|Nominal Battery Voltage|48 V|
|Wheel Diameter|180 mm|
|Command Frequency|50 Hz|
|Joint Control Frequency|1000 Hz|


#### **2.2 Environment Setup** 

Both simulation and hardware environments were established for comprehensive performance evaluation. 


**Figure 2:** Overview of the simulation and hardware experimental environments. 

**Table 3:** Simulation and hardware experimental setups. 

|**Item**|**Simulation**|**Hardware**|
|---|---|---|
|Platform|Isaac Gym (RL Training)<br>MuJoCo (Sim-to-Sim Evaluation)|Indoor laboratory<br>(15 m×7 m)|
|Ground surface|Flat ground|Flat indoor PVC floor|
|Safety protection|–|Overhead crane|
|Computing platform|Desktop PC<br>(NVIDIA RTX 4090 GPU)|Onboard computer|
|Operating system|Ubuntu 22.|04|


2 

#### **2.3 Basic Data Acquisition** 

During each experiment, the robot states and sensor measurements of X2-N were recorded for subsequent analysis, as summarized in Table 4. For hardware experiments, the robot velocity and displacement were estimated from the measurements of the body-mounted IMU without external motion capture systems. The battery voltage and current were directly obtained from the battery management system (BMS). 

**Table 4:** Recorded robot states during the experiments. 

|**Item**|**Recorded Signals**|**Sim.**|**Hw.**|
|---|---|---|---|
|Joint|Position, velocity, torque|✓|✓|
|IMU|Acceleration, angular velocity, orientation|✓|✓|
|Body (CoM) States|Position, velocity, orientation|✓|–|
|Battery States|Voltage, current|–|✓|
|Contact Forces|Normal force, lateral force|✓|–|


### **3 Experiment 1: Energy Efficiency Evaluation under Different Locomotion Modes** 

To investigate the energy efficiency of different locomotion modes, additional simulation and hardware experiments were conducted on the proposed X2-N robot. The experiments quantitatively analyze the mechanical power, electrical power, total energy consumption, and Cost of Transport (CoT) of different locomotion configurations. 

#### **3.1 Evaluation Metrics** 

The evaluation metrics and corresponding formulas are summarized in Table 5. Since battery measurements are unavailable in the simulator, the electrical power cannot be estimated for simulation experiments. 

**Table 5:** Evaluation metrics used throughout the energy experiments. 

|**Metric**|**Formula (Unit)**|**Notes**|
|---|---|---|
|Total|_𝑁_|_𝜏𝑖_: torque;_𝜔𝑖_:|
|Mechanical<br>Power|_𝑃_mech =<br><br>∑<br>_𝑖_=1<br>|_𝜏𝑖𝜔𝑖_| (W)|angular velocity;_𝑁_:<br>actuators.|
|Electrical<br>Power|_𝑃_elec =_𝑉𝐼_(W)|_𝑉_: voltage;_𝐼_: BMS<br>current.|
|Energy<br>Consumption|_𝐸_=<br>_𝐾_<br>∑<br>_𝑘_=1<br>_𝑃𝑘_Δ_𝑡_(J)|_𝑃𝑘_: sampled power;<br>Δ_𝑡_: interval.|
|Cost of|_𝐶𝑇_<br>_𝐸_|_𝑚_: mass;_𝑔_: gravity;|
|Transport|_𝑜_=<br>_𝑚𝑔𝑑_|_𝑑_: distance.|


#### **3.2 Experimental Design** 

The experimental design for energy evaluation is described as follows. First, a static standing test is conducted to characterize the baseline energy consumption of the robot system, including the onboard computer, communication modules, electrical drive boards, and other auxiliary components. Then, X2-N is commanded to perform constant-speed straight-line locomotion under different locomotion modes to evaluate their energy efficiency. Detailed experimental settings are summarized in Table 6. 

3 


**Figure 3:** Four configurations in simulation setup. 


**Figure 4:** Four configurations in hardware setup. 

**Table 6:** Experimental settings for power and energy evaluation. 

|**Item**|**Sub-item**|**Simulation**|**Hardware Experiment**|
|---|---|---|---|
|Still standing|–|10 s|5 mins|
||||8 m straight path|
||Travel distance|16 m straight path|10 round trips|
|Linear motion|||160 m in total|
||Speed|0.5 m/s, 1 m/s, 1.5|0.4 m/s, 0.6 m/s, 1.0 m/s|
||commands|m/s||
||Loco. Mode|Foot-legged, Wheel-l|egged, Wheel-legged*, Hybrid|


In addition, although the robot primarily relies on wheel locomotion in this mode, the bent knee posture introduces additional joint actuation and energy consumption. Therefore, the wheel-legged mode was further evaluated with a straightened-knee configuration (wheel-legged*). This additional case was conducted to analyze the potential energy consumption characteristics of the wheel-legged locomotion mode. 

Furthermore, since the state estimation relies solely on onboard proprioceptive information (IMU), achieving accurate velocity tracking during experiments remains challenging. The actual velocity is influenced by multiple factors, including ground friction conditions, motion direction, sim-to-real gaps, joint temperature variations, and power supply stability. Therefore, the reported average velocities are determined based on practical hardware measured velocities. 

4 

#### **3.3 Results** 

#### **3.3.1 Simulation** 

Simulation results are shown in Fig. 5, Fig. 6 and Table 7. Due to joint torque limitations, the foot-legged mode cannot achieve a locomotion speed of 1.5 m/s, while the hybrid mode failed after 7 s of operation. 


**Figure 5:** Mechanical power and CoT comparison in simulation experiments. 


**Figure 6:** Real-time mechanical power in simulation experiments. 

#### **3.3.2 Hardware Experiment** 

The hardware experiment statistics are provided below. It should be noted that the hybrid locomotion mode cannot maintain stable balance at low-speed conditions. Therefore, the 0.4 m/s experimental data are unavailable for this mode. 

5 

**Table 7:** Power and energy evaluation in simulation experiments. 

|Motion|Velocity<br>(m s<sup>−1</sup>)|Loco. Mode|_𝑃_<sup>avg</sup><br>mech<br>(W)|_𝑃_<sup>max</sup><br>mech<br>(W)|_𝐸_mech_,_16m<br>(J)|CoTmech|
|---|---|---|---|---|---|---|
|Still standing|0.0|–|0.12±0.10|0.90|–|–|
|||foot|42.46±1.73|153.24|1923.1±77.7|0.390±0.016|
||05|wheel|18.21±0.22|19.78|402.3±31.6|0.082±0.006|
||.|wheel<sup>∗</sup>|**7.50**±**0.17**|**11.24**|**238.8**±**7.9**|**0.048**±**0.002**|
|||hybrid|42.76±4.24|113.18|975.0±89.6|0.198±0.018|
|||foot|113.00±3.56|595.06|1958.3±66.4|0.397±0.013|
|Linear motion|1|wheel|41.52±0.75|44.65|598.4±46.2|0.121±0.009|
||.0|wheel<sup>∗</sup>|**33.31**±**1.07**|**37.56**|**490.7**±**38.2**|**0.099**±**0.008**|
|||hybrid|74.71±4.09|177.35|838.3±106.8|0.170±0.022|
|||foot|–|–|–|–|
|||wheel|62.37±1.92|63.46|731.7±52.0|0.148±0.011|
||1.5|wheel<sup>∗</sup>|**38.33**±**2.93**|**43.90**|**535.8**±**56.5**|**0.109**±**0.011**|
|||hybrid|220.50±266.65|937.75|2710.6±1782.7|0.549±0.361|


**Table 8:** Power and energy evaluation in hardware experiments. 

|Motion|Velocity<br>(m/s)|Loco. Mode|_𝑃_<sup>avg</sup><br>mech<br>(W)|_𝑃_<sup>avg</sup><br>elec<br>(W)|_𝑃_<sup>max</sup><br>mech<br>(W)|_𝑃_<sup>max</sup><br>elec<br>(W)|_𝐸_elec_,_16m<br>(J)|CoTmech|CoTelec|_𝜂_<br>(%)|
|---|---|---|---|---|---|---|---|---|---|---|
|Still standing|0|–|0_._42±0_._10|74_._04±0_._86|0.88|76.84|740.4|–|–|0.57|
|||foot|38_._44±2_._61|133_._29±13_._76|409.40|1019.39|8504_._6±1687_._8|0_._498±0_._093|1_._723±0_._342|28_._9±2_._9|
||04|wheel|19_._94±7_._32|111_._33±17_._90|35.08|156.70|4479_._8±720_._4|0_._163±0_._060|0_._908±0_._146|17_._9±6_._8|
||.|wheel<sup>∗</sup><br>|**10**_._**73**±**0**_._**53**|**94**_._**17**±**2**_._**90**|42.81|**108**_._**01**|**3317**_._**5**±**131**_._**0**|**0**_._**077**±**0**_._**004**|**0**_._**672**±**0**_._**027**|11_._4±0_._5|
|||hybrid|–|–|–|–|–|–|–|–|
|||foot|35_._33±–|127_._63±–|155.87|195.06|4925_._8±–|0_._276±–|0_._998±–|27_._7±–|
|Linear motion|06|wheel|16_._31±0_._91|117_._26±2_._96|50.49|156.72|3073_._8±98_._8|0_._087±0_._005|0_._623±0_._020|13_._9±0_._6|
||.|wheel<sup>∗</sup>|**15**_._**80**±**1**_._**03**|**99**_._**15**±**4**_._**18**|57.88|**121**_._**22**|**2471**_._**7**±**146**_._**3**|**0**_._**080**±**0**_._**003**|**0**_._**501**±**0**_._**030**|15_._9±0_._9|
|||hybrid|61_._65±5_._75|110_._94±18_._83|484.45|402.60|3254_._7±582_._5|0_._366±0_._037|0_._659±0_._118|55_._5±10_._9|
|||foot|94_._09±12_._08|173_._12±18_._10|191.45|467.02|8141_._9±2231_._6|0_._895±0_._244|1_._650±0_._452|54_._2±6_._7|
||10|wheel|33_._06±1_._98|122_._76±3_._63|93.38|151.87|1740_._9±63_._6|0_._095±0_._004|0_._353±0_._013|26_._9±1_._3|
||.|wheel<sup>∗</sup>|**32**_._**28**±**1**_._**35**|**110**_._**76**±**2**_._**67**|**91**_._**21**|**139**_._**91**|**1589**_._**7**±**79**_._**0**|**0**_._**094**±**0**_._**003**|**0**_._**322**±**0**_._**016**|29_._1±1_._5|
|||hybrid|65_._43±5_._08|112_._65±11_._22|349.71|240.26|2629_._3±315_._1|0_._309±0_._026|0_._533±0_._064|58_._0±7_._4|


**Figure 7:** Mechanical power and CoT in hardware experiments. 

6 


**Figure 8:** Electrical power and CoT in hardware experiments. 

#### **3.4 Discussion and Summary** 

From the experimental results, wheel-legged locomotion achieves the lowest energy consumption under the same velocity conditions. This is mainly because the robot relies on continuous wheel rolling, which reduces the required joint actuation compared with foot-legged locomotion. 

In contrast, foot-legged locomotion requires continuous joint actuation for gait generation, including leg swing motion, body stabilization, and periodic foot-ground interactions, resulting in higher mechanical and electrical power consumption. Hybrid locomotion exhibits intermediate energy consumption, as it retains the efficiency of wheel rolling while requiring additional leg joint actuation for posture regulation and motion coordination. 

Furthermore, the **straightened-knee** wheel-legged configuration further reduces energy consumption compared with the bent-knee configuration. This is because the straightened-knee posture improves structural load support and reduces the required joint torque, whereas the bent-knee configuration requires continuous actuator effort to maintain the posture. 

And we found a **large sim2real gap** between the simulation and hardware experiments. The torque and velocity tracking errors are mainly because of sensing noise, ground friction conditions, motion direction, joint heat variations, and power supply stability. 

Overall, the results validate the energy efficiency advantage of the transformable wheel-legged design. By switching to wheel-based locomotion when appropriate, X2-N significantly reduces actuator effort and achieves more efficient mobility. 

### **4 Experiment 2: Repeatability and Stability Evaluation of Bidirectional Transformation** 

To further validate the engineering robustness of the proposed transformable mechanism, additional experiments were conducted to evaluate the repeatability, stability, and reliability of transformation between the wheel-legged and foot-legged configurations. 

#### **4.1 Evaluation Metrics** 

The following metrics are adopted throughout this section. 

7 

**Table 9:** Evaluation metrics for bidirectional transformation experiments. 

|**Metric**|**Formula (Unit)**|**Notes**|
|---|---|---|
|Transformation<br>Time|_𝑇_trans =_𝑡𝑒_−_𝑡𝑠_(s)|_𝑡𝑠_: start;_𝑡𝑒_: end.|
|Body CoM<br>Displacement|_𝑒_CoM =<br>��_𝑝𝑒_<br>CoM <sup>−</sup><sup>_𝑝𝑠_</sup><br>CoM<br>��<br>2 <sup>(m)</sup>|CoM displacement<br>between start and end.|
|Body Orientation<br>Deviation|_𝑒_ori =cos<sup>−1</sup><br>�tr(_𝑅𝑇_<br>_𝑠_<sup>_𝑅𝑒_) −1</sup><br>2<br>�<br>(rad)|_𝑅𝑠_,_𝑅𝑒_: initial and<br>final orientations.|
|Transformation<br>Energy|_𝐸_trans =<br>_𝑒_<br>∑<br>_𝑘_=_𝑠_<br>_𝑃𝑘_Δ_𝑡_(J)|_𝑃𝑘_: measured power;<br>Δ_𝑡_: interval.|
|Success Rate|_𝑅_success = <sup>_𝑁𝑠_</sup><br>_𝑁𝑎_<br>×100% (%)|_𝑁𝑠_: successful trials;<br>_𝑁𝑎_: total trials.|


#### **4.2 Experimental Setup** 

The transformation process consists of two operating modes: wheel-legged to foot-legged transformation and foot-legged to wheel-legged transformation. During each trial, the robot remains stationary while executing the transformation motion. The transformation completion time was determined based on the IMU measurements. When the body orientation signals reached a stable state after the transformation motion, the corresponding time was recorded as the transformation completion time. 

To further evaluate the transformation robustness, hardware experiments were conducted under practical operating conditions. For the no-load condition, the robot was suspended and the ankle-driven transformation mechanism was activated to verify the basic transformation capability. For the full-body-load condition, a square region with predefined dimensions of 70 cm × 70 cm was marked on a flat floor to quantitatively evaluate transformation stability. 

A successful transformation was defined as completing the mode transition without falling while keeping the robot body within the marked region. Otherwise, the trial was recorded as a failure. The corresponding experimental setup is illustrated in Fig. 10. 

**Table 10:** Experimental settings for transformation repeatability evaluation. 

|**Item**|**No-load Transformation **|**Full-body-load Transformation**|
|---|---|---|
|Number of cycles|150|30|


8 


**Figure 9:** Transformation experiment setup. 

#### **4.3 Representative Results** 

The recorded transformation data are summarized in Table 11, Table 12 and Table 17 including the transformation time, CoM displacement, body orientation deviation, energy consumption, and transformation success rate. 

**Table 11:** Real-robot transformation metrics under full action execution. 

|Motion|_𝑇_trans (s)|_𝑒_CoM (m)|_𝑒_ori (deg)|_𝑒_roll (deg)|_𝑒_pitch (deg)|_𝑒_yaw (deg)|
|---|---|---|---|---|---|---|
|Wheel to foot|2_._53±0_._25|0_._309±0_._076|28_._48±10_._64|0_._680±0_._696|−4_._387±1_._075|−27_._909±11_._292|
|Foot to wheel|1_._85±0_._50|0_._183±0_._083|4_._58±1_._39|0_._416±0_._450|3_._952±1_._489|−1_._801±1_._247|


**Table 12:** Real-robot transformation power and energy evaluation. 

|Motion|_𝐸_mech (J)|_𝑃_mech (W)|_𝐸_elec|(J)<br>_𝑃_elec (W)|
|---|---|---|---|---|
|Wheel-to-foot|219_._90±19_._72|87_._14±6_._84|539_._09±|110_._38<br>214_._67±47_._55|
|Foot-to-wheel|128_._24±16_._70|72_._62±16_._23|210_._21±|101_._16<br>115_._41±45_._72|


**Table 13:** Success rate evaluation of bidirectional transformation under different loading conditions. 

|Condition|Motion|_𝑁𝑠_|_𝑁𝑎_|_𝑅_success (%)|
|---|---|---|---|---|
|No-load|Wheel to foot<br>Foot to wheel|150<br>150|150<br>150|100<br>100|
|Full-body-load|Wheel to foot<br>Foot to wheel|27<br>30|30<br>30|90<br>100|


#### **4.4 Discussion** 

Across all no-load transformation trials, the transformation controller and locking mechanism operated reliably without any jamming or structural damage. During the full-body-load transformation experiments, the robot maintained dynamic balance through continuous body posture regulation by the transformation controller. 

The proposed transformation and locking mechanisms achieved several repeated transformation cycles, demonstrating their practical reliability. The body displacement and orientation deviations remain within a relatively small range, especially during the foot-legged to wheel-legged transformation. 

However, several unexpected behaviors and failure cases were also observed during these experiments. 

9 

**Yaw-axis Deviation** A noticeable yaw-axis deviation is observed during the wheel-legged to foot-legged transformation. This deviation occurs when the robot reaches the final stationary state and is mainly attributed to the current agent switching strategy in the control policy. As a result, the robot exhibits a consistent yaw rotation tendency toward the right side during this transformation direction. This issue will be further addressed through future controller optimization. 

**Failure Cases** Several failure cases were observed during the experiments, mainly caused by mechanical component degradation, joint overheating, operation errors, insufficient battery power, and unexpected embedded-system issues. 

The **mechanical degradation** was mainly caused by loosened screws during repeated operation, which resulted in partial separation of the mechanical component from the bearing support. Consequently, the bearing lost its intended support function, and the reduced ankle structural stiffness introduced additional vibration, affecting the balance stability during transformation. 


**Figure 10:** Mechanical degradation during transformation tests. 

Furthermore, continuous transformation requires sufficient **thermal management** and **battery power support** for the ankle actuators. Insufficient cooling and power stability reduced the achievable joint torque, leading to degraded posture control capability and occasional transformation failures. 

#### **4.5 Summary** 

The repeated transformation experiments validate the reliability and repeatability of the proposed transformation mechanism under practical conditions. The system maintains stable bidirectional transformation performance under different loading conditions, while the observed failure cases provide insights for further improvements in mechanical durability and controller robustness. 

### **5 Experiment 3: Engineering Validation of the Locking Mechanism** 

The following experiments aim to evaluate the engineering performance of the proposed locking mechanism, including its structural strength, locking reliability, and operational stability under repeated transformations and external loading conditions. 

10 

#### **5.1 Detailed View of the Locking Mechanism** 


**Figure 11:** 3D model and explosion view of the locking mechanism. 

#### **5.2 Evaluation Metrics** 

The locking mechanism is evaluated using the following criteria. 

**Table 14:** Evaluation metrics for locking mechanism validation. 

|**Metric**|**Formula (Unit)**|**Notes**|
|---|---|---|
|Maximum Impact<br>Load|_𝐹_impact_,_max (N)|Maximum impact force<br>during locking engagement.|
|Maximum Impact<br>Torque|_𝜏_impact_,_max (Nm)|Maximum joint torque<br>during locking engagement.|
|||Displacement caused by|
|Locking Backlash|Δ_𝜃_(arcmin)|mechanical clearance after<br>locking.|
|Wear Degradation|Δ_𝐷_(mm)|Clearance increase after<br>repeated locking cycles.|
|Success Rate|_𝑅_success = <sup>_𝑁𝑠_</sup><br>_𝑁𝑎_<br>×100%<br>(%)|_𝑁𝑠_: successful operations;<br>_𝑁𝑎_: total attempts.|


#### **5.3 Experiment Setup** 

The structural stiffness of the locking mechanism was evaluated using finite element analysis (FEA) in SolidWorks. The maximum loading condition of the ankle joint during transformation was first determined, and the corresponding load with an applied safety factor was then introduced into the simulation to assess the structural response and reliability of the locking mechanism. 

11 

**Table 15:** Validation setups for the locking mechanism. 

|**Item**|**Simulation**|**Har**|**dware**|
|---|---|---|---|
|Condition|SolidWorks Analysis|No Load|Full Robot Load|
|Evaluation|Finite Element<br>Analysis|Ankle-level<br>Transformation|Whole Robot<br>Transformation|
|Number of|–|150|30|
|Trials||||


**Table 16:** Maximum loading conditions of the locking mechanism. 

|**Item**|**Max. Impact Normal Force**|**Max. Impact Lateral Force**|**Max. Rotation Torque**|
|---|---|---|---|
|Condition|Hybrid mode<br>stepping|High-speed<br>turning|High-speed<br>rolling acceleration|
|Value|900 N|100 N|20 Nm|


#### **5.4 Results and Discussion** 

#### **5.4.1 Finite Element Analysis** 

By assigning the material properties in the simulation model, the FEA results were obtained as shown below. The von Mises stress distribution was analyzed, where the red regions indicate the areas experiencing the highest stress. 

The maximum simulated stress and deformation remain below the yield strength and allowable deformation limits of the aluminum 7075-T6 alloy material (approximately 500 MPa). Therefore, the locking components are expected to maintain sufficient structural reliability and robustness under the applied loading conditions. 


**Figure 12:** Modeling, mesh and real parts of the locking mechanism. 


**Figure 13:** Stiffness analysis results of the locking mechanism. 

12 

#### **5.4.2 Backlash Analysis** 


**Figure 14:** Pitch and roll view of the ankle of X2-N. 

We further analyzed the pitch and roll joint backlash based on the mechanical design and manufacturing tolerances. 

For the **pitch rotation** , the joint is constrained by the mating surfaces of the locking components. Therefore, the dominant backlash source is the manufacturing tolerance. According to the 2D mechanical drawings, the machining tolerance of the metal CNC components is specified as 0–0.02 mm. With a rotation radius of approximately 30 mm, the maximum angular backlash caused by the clearance can be estimated as: 


For the **roll rotation** , the ankle joint is locked by the roll actuator. Therefore, the main backlash originates from the gearbox transmission. The R52 actuator adopts a planetary gearbox with an average backlash of approximately _𝜃_ roll _,_ max = **5 arcmin** , corresponding to about **0.083**<sup>◦</sup> . 

It should be noted that the backlash is not constant during the entire lifetime of the mechanism. With prolonged operation, mechanical wear and clearance accumulation can gradually increase the backlash. After extended usage, the backlash of the roll joint increased to approximately **50 arcmin** . The corresponding components will be replaced with newly manufactured parts during maintenance. 

#### **5.4.3 Hardware Validation** 

**Experiments** The hardware validation of the locking mechanism was performed through repeated transformation experiments. As mentioned in the previous section, we conducted 150 no-load transformation trials and 30 full-body-load transformation trials. The proposed locking mechanism achieved a high success rate throughout these experiments, demonstrating reliable locking performance under repeated transformation operations. 

**Table 17:** Success rate evaluation of bidirectional transformation under different loading conditions. 

|Condition|Motion|_𝑁𝑠_|_𝑁𝑎_|_𝑅_success (%)|
|---|---|---|---|---|
|No-load|Wheel to foot<br>Foot to wheel|150<br>150|150<br>150|100<br>100|
|Full-body-load|Wheel to foot<br>Foot to wheel|27<br>30|30<br>30|90<br>100|


**Wear Analysis** After the initial assembly, the surface condition of the locking mechanism was smooth and intact, with an additional oxidation coating applied for surface protection. During subsequent controller validation and reliability testing, the robot underwent more than 80 full-body-load transformation cycles. During these repeated operations, 

13 

different levels of mechanical wear were observed. 

Compared with the titanium alloy components, the aluminum alloy components experienced more noticeable wear. The main wear region was located at the entrance area of the mating interface, which was mainly caused by repeated impact during the locking process and occasional failed transformations. The maximum observed wear depth was approximately Δ _𝐷_ = 0 _._ 5 _𝑚𝑚_ . 


**Figure 15:** Wear cases of ankle parts. 

#### **5.5 Summary** 

The locking mechanism was validated through repeated transformation trials under different loading conditions. The results demonstrate reliable locking performance during mode switching, while the observed wear mainly originated from repeated impacts at the mating interfaces. These findings verify the effectiveness of the proposed locking design and provide guidance for further durability improvements. 

### **6 Experiment 4: Ablation Studies of Reinforcement Learning Reward Components** 

Based on the reward function used in the locomotion and transformation agents in the RL controller, we did three ablation research experiments to find the function of those rewards. 

The sub experiments are listed below, as shown in Table 18 

**Table 18:** Organization of the supplementary experiments. 

|**Exp.**|**RL Agent Type**|**Title**|**Key Reward**|
|---|---|---|---|
|Exp. 4.1|Wheel-legged Agent|Centrifugal Compensation Reward Ablation|_𝑅_cen|
|Exp. 4.2|Foot-legged Agent|Foot-legged Walking Mimic Reward Ablation|_𝑅_mimic|
|Exp. 4.3|Transformation Agent|Transformation Balance Reward Ablation|_𝑅_balance|


14 

#### **6.1 Centrifugal-force Compensation Reward Ablation** 

#### **6.1.1 Reward Definition** 

The centrifugal-force compensation reward encourages the robot to adopt an appropriate body-leaning strategy during turning. By exploiting the gravitational component generated by body inclination, the required centripetal force can be partially compensated, thereby improving turning stability. The corresponding mathematical formulation is given as follows: 


where _𝑣 𝑥_ and _𝜔_ yaw are the robot forward velocity and yaw angular velocity. _𝑔_ is the gravity term, and _𝑎_<sup>obs</sup> _𝑦_ is the lateral-direction acceleration measured by the IMU. The constant 0.3 limits excessive body inclination for safety. This reward encourages the robot to generate appropriate body lean during turning for enhanced locomotion stability. 

#### **6.1.2 Evaluation Metrics** 

To capture the turning performance, we setup the follow evaluation metrics, shown in Table 19. 

**Table 19:** Evaluation metrics for anti-centrifugal force reward ablation. 

|**Metric**|**Formula (Unit)**|**Notes**|
|---|---|---|
|Roll Tilt Angle|_𝜃_roll = |_𝜙_|(deg)|_𝜙_: measured body roll angle; represents<br>lateral inclination.|
|Velocity Tracking<br>Error|_𝑒𝑣_= <sup>1</sup><br>_𝑇_<br>∫_𝑇_<br>0<br>|_𝑣_−_𝑣𝑑_|_𝑑𝑡_(m/s)|_𝑣_: measured velocity;_𝑣𝑑_: commanded<br>velocity.|
|Turning<br>Radius<br>Error|_𝑒𝑟_= |_𝑟_−_𝑟𝑑_|(m)|_𝑟_: measured turning radius;_𝑟𝑑_: desired<br>turning radius.|
|Centripetal Force|_𝐹𝑐_= <sup>_𝑚𝑣_2</sup><br>_𝑟_<br>(N)|_𝑚_: robot mass; _𝑣_: velocity;_𝑟_: turning<br>radius.|
|Centripetal Force<br>Error|_𝑒𝑐_= |_𝐹_<sup>_𝑎_</sup><br>_𝑐_<sup>−</sup><sup>_𝐹𝑑_</sup><br>_𝑐_<sup>| (N)</sup>|_𝐹_<sup>_𝑎_</sup><br>_𝑐_<sup>: actual centripetal force;</sup> <sup>_𝐹𝑑_</sup><br>_𝑐_<sup>: re-</sup><br>quired force from commanded velocity<br>and reference radius.|
|Turning<br>Radius<br>Error|_𝑒𝑟_= <sup>|</sup><sup>_𝑟_−</sup><sup>_𝑟𝑑_|</sup><br>_𝑟𝑑_<br>(Unitless)|_𝑟_: measured turning radius;_𝑟𝑑_: desired<br>turning radius.|


#### **6.1.3 Experimental Setup** 

To evaluate the turning performance, X2-N was tested under circular motion with constant linear and angular velocities. An ablation study was conducted by removing the centrifugal-force compensation reward while keeping all other reward terms. 

15 

**Table 20:** Simulation settings for circular motion evaluation. 

|**Item**|**Simulation**|
|---|---|
|Motion|Circular motion with constant diameter (4 m)|
|Linear Velocity|0.5 m/s, 1 m/s, 1.2 m/s|
|Angular Velocity|0.25 rad/s, 0.5 rad/s, 0.5 rad/s|


#### **6.1.4 Results and Discussion** 


**Figure 16:** Circle trajectory of ablation studies. 

**Table 21:** Ablation results of the anti-centrifugal reward during circular motion. 

|_𝑣𝑥_||_𝜔𝑧_||_𝑟𝑑_|Method|_𝑟_|_𝑒𝑟_||_𝜙_||_𝑒𝑣_|_𝐹𝑐_|_𝑒𝑐_|
|---|---|---|---|---|---|---|---|---|---|
|(m/s)|(rad/s)|(m)||(m)||(deg)|(m/s)|(N)|(N)|
|0.5|0.25|2.0|<sup>w/o reward </sup><br>w/ reward|<sup>1.693 </sup><br>**1.643 **|<sup>0.1535 </sup><br> **0.1785 **|<sup>1.931 </sup><br> **2.210 **|<sup>0.0113</sup><br> **0.0038**|4.437<br>**4.709**|**0.508**<br>0.786|
|1.0|0.50|2.0|<sup>w/o reward </sup><br>w/ reward|<sup>2.567 </sup><br>**2.055 **|<sup>0.2835 </sup><br> **0.0275 **|<sup>0.923 </sup><br> **5.462 **|<sup>0.0522 </sup><br> **0.0386 **|<sup>10.992 </sup><br> **16.420 **|<sup>4.719</sup><br> **0.785**|
|1.2|0.50|2.4|<sup>w/o reward </sup><br>w/ reward|<sup>3.570 </sup><br>**2.321 **|<sup>0.4875 </sup><br> **0.0329 **|<sup>0.329 </sup><br> **5.863 **|<sup>0.0731 </sup><br> **0.0419 **|<sup>11.204 </sup><br> **18.054 **|<sup>7.681</sup><br> **0.696**|


**Figure 17:** Comparison results of ablation studies. 

16 

The ablation study demonstrates that the centrifugal-force compensation reward substantially improves circular-motion stability, particularly under demanding high-speed turning conditions. With the reward enabled, the robot maintains the commanded turning radius more accurately and exhibits improved velocity and centripetal-force tracking. The learned policy also develops a more pronounced body-leaning response, which helps preserve the intended turning behavior as the lateral demand increases. 

At low speed, the benefit is less evident, and the reward does not consistently reduce roll-angle error. A modest increase in lateral slip is also observed in some conditions, suggesting a trade-off between geometric trajectory tracking and lateral motion regulation. Overall, the results indicate that the centrifugal compensation reward is most effective for maintaining stable and accurate turning at higher speeds, while further refinement is required to improve low-speed behavior and reduce residual lateral slip. 

#### **6.1.5 Summary** 

Through different speed experiments, it can be observed that removing the centrifugal-force compensation reward increases body roll and trajectory tracking error, especially during high-speed turning. The proposed reward effectively improves turning stability while reducing lateral slip, and help with wheel-legged locomotion stability. 

#### **6.2 Foot-legged Walking Mimic Reward Ablation** 

#### **6.2.1 Reward Definition** 

We apply a human-mimic reward _𝑅_ mimic to encourage the lower limb joints of X2-N to replicate reference joint trajectory **q** ref. The reward _𝑅_ mimic is defined as: 


#### **6.2.2 Experimental Setup** 

**Table 22:** Experimental settings for mimic reward evaluation. 

|**Item**|**Configuration**|
|---|---|
|Motion|Straight-line walking|
|Velocity|0.4 m/s, 0.7 m/s, 1.0 m/s|
|Reference Trajectory|Predefined Joint Trajectory|


The humanoid locomotion reward was removed while keeping all remaining reward terms unchanged. The controller was retrained using the same training environment. Simulation experiments were performed under constant-speed walking. 

#### **6.2.3 Evaluation Metrics** 

**Table 23:** Evaluation metrics for mimic reward ablation. 

|**Metric**|**Formula (Unit)**||**Notes**|
|---|---|---|---|
|Joint Position Error|_𝑒𝑞𝑖_= |_𝑞𝑖_−_𝑞_<sup>_𝑟𝑒𝑓_</sup><br>_𝑖_<br>||(deg)|_𝑞𝑖_: measured joint position;_𝑞_<sup>_𝑟𝑒𝑓_</sup><br>_𝑖_<br>: reference|
||||joint position.|


17 

#### **6.2.4 Results and Discussion** 

**Table 24:** Mimic reward ablation results. 

|Velocity|Method|_𝑒𝑞𝑖_(deg)|Δ_𝑒𝑞_(%)|
|---|---|---|---|
|04 m/s|w/o_𝑅_mimic|13.23|–|
|.|w/_𝑅_mimic|4.22|+68.1%|
|0.7 m/s|w/o_𝑅_mimic<br>w/_𝑅_mimic|20.50<br>6.23|–<br>+69.6%|
|10 m/s|w/o_𝑅_mimic|25.01|–|
|.|w/_𝑅_mimic|8.27|+66.9%|


**Figure 18:** Joint position following errors of the ablation studies. 


**Figure 19:** Comparison results of ablation studies. 

The mimic reward substantially improves joint-level motion tracking across all evaluated velocities, reducing the joint position error. The improvement is particularly pronounced for the ankle yaw and hip roll joints, while the improvement of knee joints is less significant at low walking speeds. However, improved joint trajectory imitation does not consistently translate into better whole-body stability. 

At higher walking speeds (0.7 and 1.0 m/s), the body orientation error increases, accompanied by larger yaw deviations. 

18 

These results indicate that the mimic reward effectively enhances local joint-level imitation but introduces a trade-off between trajectory tracking accuracy and global body stability. 

#### **6.3 Transformation Balance Reward Ablation** 

#### **6.3.1 Reward Definition** 

To maintain locomotion balance during transformation while following pre-defined joint trajectories, we specially define a balance reward _𝑅_ balance during the process: 


to stabilize the body CoM and pose, where _𝑘_ 1 to _𝑘_ 4 are term weights, _𝜃_ roll _, 𝜃_ pitch _, 𝜔_ roll _, 𝜔_ pitch are the pose angles and velocities in roll and pitch orientations, and _𝜎𝜃 , 𝜎𝜔_ are the scale parameters to control decay rate. 

#### **6.3.2 Experimental Setup** 

**Table 25:** Experimental settings for balance reward evaluation. 

|**Item**|**Configuration**|
|---|---|
|Motion|In-place transformation|
|Ground friction|0.3, 0.5, 0.7, 1.0|


The balance reward was removed while all remaining reward terms were retained. The controller was retrained using identical training settings. 

#### **6.3.3 Evaluation Metrics** 

**Table 26:** Metrics in the balance reward ablation tests. 

|**Metric**|**Formula (Unit)**|**Notes**|
|---|---|---|
|Transformation Time|_𝑇_trans =_𝑡_end−_𝑡_start (s)|_𝑡_start: start time;_𝑡_end: first stable state<br>maintained for 0.5 s.|
|Maximum Tilt Angle|_𝜃_max =max<br>_𝑡_<br>∥_𝜽_(_𝑡_)∥2 (deg)|Maximum roll–pitch inclination dur-<br>ing transformation.|
|CoM Position Error|_𝑒_CoM = ∥**p**<sup>_𝑒_</sup><br>CoM <sup>−</sup><sup>**p**</sup><sup>_𝑠_</sup><br>CoM<sup>∥2</sup>|CoM displacement between transfor-|
||(m)|mation start and end.|


19 

#### **6.3.4 Results and Discussion** 


**Figure 20:** Comparison results of ablation studies. 

**Table 27:** Ablation results of the balance reward under different ground friction coefficients. 

|Friction|Method|_𝑇_trans|_𝜃_max (deg)|_𝑒_CoM|_𝑅_success|
|---|---|---|---|---|---|
|03|w/o_𝑅_balance|2.324|**12.55**|0.447|100%|
|.|w/_𝑅_balance|**1.349**|18.79|**0.232**|100%|
|05|w/o_𝑅_balance|2.392|**11.57**|0.403|100%|
|.|w/_𝑅_balance|**1.579**|20.34|**0.138**|100%|
|07|w/o_𝑅_balance|2.444|**11.69**|0.438|100%|
|.|w/_𝑅_balance|**2.026**|20.46|**0.154**|100%|
|10|w/o_𝑅_balance|2.440|**11.74**|0.446|100%|
|.|w/_𝑅_balance|**1.430**|20.57|**0.129**|100%|


Across all tested ground friction conditions, the balance reward consistently improved transformation efficiency and positional stability while maintaining reliable task completion. It enabled faster transformations and reduced CoM displacement. Meanwhile, a larger maximum body tilt angle was observed, indicating that the controller actively exploited body inclination to regulate the CoM and maintain balance during dynamic transformation. 

These results demonstrate that the balance reward encourages a more dynamic balance strategy. Without the balance reward, the transformation controller tends to maintain a conservative upright posture but suffers from slower convergence and larger CoM deviation. With the proposed reward, the robot allows transient body attitude variations to achieve more effective balance regulation and robust transformation performance. 

#### **6.3.5 Summary** 

The ablation study verifies that the balance reward improves transformation stability by accelerating convergence and reducing body CoM deviation under different friction conditions. The results demonstrate its effectiveness in maintaining dynamic balance during morphology transformation. 

20 

### **7 Experiment 5: Comparison Evaluation of 4-DoF and 7-DoF Interchangeable Arms** 

#### **7.1 Overview** 

To evaluate the practical benefits of the interchangeable arm design, we conducted a comparative analysis between the 4-DoF and 7-DoF arm configurations. The 4-DoF arm provides a lightweight and compact solution for basic manipulation tasks, while the 7-DoF arm introduces additional wrist degrees of freedom to improve end-effector orientation flexibility and dexterity. 

The two arm configurations share the same mounting interface and upper-arm structure, enabling rapid replacement according to different application requirements. In this experiment, we quantitatively compare their reachable workspace and manipulation capability to analyze the contribution of the additional degrees of freedom. The corresponding arm configurations are illustrated in Fig. 21. 


**Figure 21:** URDF modeling of the 4-DoF and 7-DoF arms. 

#### **7.2 Comparison Results and Discussion** 

#### **7.2.1 Workspace and Manipulability** 

**Table 28:** Workspace comparison between the 4-DoF and 7-DoF interchangeable arm configurations. 

|**Workspace metric**|**4-DoF**|**7-DoF**|**Improvement**|
|---|---|---|---|
|X-axis span|0.9589 m|**1.2176 m**|+26_._98%|
|Y-axis span|0.8580 m|**1.1063 m**|+28_._94%|
|Z-axis span|0.9588 m|**1.2186 m**|+27_._10%|
|Maximum shoulder-referenced reach|0.5465 m|**0.6785 m**|+24_._15%|
|Workspace volume|0.28990 m<sup>3</sup>|**0.64828 m**<sup>3</sup>|+123_._62%|
|Mean translational manipulability|0.010580 m<sup>3</sup>|**0.022035 m**<sup>3</sup>|+108_._27%|
|Mean reduced 4-D manipulability|0.166356|**0.177072**|+6_._44%|


The workspace is calculated for both arm configurations under identical base mounting conditions and joint limits. Since the forearm of the 7-DoF arm is longer than that of the 4-DoF arm, the maximum reachable workspace is naturally extended. Furthermore, the additional wrist degrees of freedom provide higher end-effector orientation flexibility. 

For the 4-DoF arm, the Jacobian matrix cannot achieve full rank in the 6D Cartesian space, limiting independent control of the complete end-effector pose. Therefore, its dexterity is constrained in complex manipulation tasks requiring precise 

21 

orientation adjustment. In contrast, the 7-DoF arm provides full 6D pose control with additional redundancy, enabling better singularity avoidance and joint configuration optimization, which improves manipulation flexibility and whole-body capability. 

As for manipulability, the reduced 4-D manipulability is defined as _𝑤_ 4 = ~~√~~ det( _𝐽_<sup>T</sup> _𝐽_ ). For the 7-DoF arm, J5–J7 were fixed at zero and only the J1–J4 Jacobian columns were retained. 

#### **7.2.2 End-effector Payload** 

**Table 29:** Comparison of arm self-weight and static payload capacity. 

|**Metric**|**X2-N 4-DoF**|**X2-T2 7-DoF**|**Change**|
|---|---|---|---|
|Arm self-weight|1.739 kg|**2.686 kg**|+54_._5%|
|Worst-case static payload|**2.844 kg**|1.255 kg|−55_._9%|
|Worst-case pose|Horizontal side reach|Forward bent-elbow reach|–|
|Payload at max. horizontal<br>reach|**2.999 kg**|1.422 kg|−52_._6%|


#### **7.3 Summary** 

The results verify the complementary advantages of the two arm configurations. The 7-DoF arm improves workspace and dexterity, while the 4-DoF arm provides higher payload efficiency and a lighter mechanical structure. The interchangeable design therefore enables flexible adaptation between dexterous manipulation and efficient operation requirements. 

### **8 Conclusions** 

This supplementary experimental evaluation provides additional quantitative analysis and engineering assessments of the proposed X2-N transformable wheel-legged humanoid robot. 

The energy evaluation results demonstrate the potential efficiency advantages of wheel-based locomotion, while the transformation experiments verify the repeatability and stability of the proposed morphology transition process under practical hardware conditions. The locking mechanism evaluation provides preliminary validation of the structural robustness during repeated transformation operations. The reinforcement learning ablation studies further reveal the contributions of different reward components to locomotion stability, trajectory tracking, and transformation performance. In addition, the comparison between different arm configurations analyzes the trade-off between manipulation capability and system complexity. 

Overall, these experiments provide further evidence that the proposed transformable architecture enables flexible adaptation between efficient locomotion and multifunctional operation. Nevertheless, the current evaluations are conducted under limited experimental conditions, and more extensive experiments with larger trial numbers, longer-term operation, and diverse environments are still required to further improve and validate the robustness, durability, and reliability of the system. 

22 

