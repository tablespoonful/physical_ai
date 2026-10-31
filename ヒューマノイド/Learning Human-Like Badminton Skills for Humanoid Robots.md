---
title: "Learning Human-Like Badminton Skills for Humanoid Robots"
date: "2026-02-09"
authors: "Yeke Chen; Shihao Dong; Xiaoyu Ji; Jingkai Sun; Zeren Luo; Liu Zhao"
url: https://arxiv.org/abs/2602.08370
pdf: https://arxiv.org/pdf/2602.08370
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.08370)** / [論文ページ](https://arxiv.org/abs/2602.08370)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Learning Human-Like Badminton Skills for Humanoid Robots** 

Yeke Chen<sup>_∗_1</sup> , Shihao Dong<sup>_∗_1</sup> , Xiaoyu Ji<sup>_∗_1</sup> , Jingkai Sun<sup>_∗_1</sup> , Zeren Luo<sup>1</sup> , Liu Zhao<sup>1</sup> , Jiahui Zhang<sup>1</sup> , Wanyue Li<sup>1</sup> , Ji Ma<sup>1</sup> , Bowen Xu<sup>1</sup> , Yimin Han<sup>1</sup> , Xuanyi Li<sup>2</sup> , Yudong Zhao<sup>2</sup> , Liyun Li<sup>2</sup> , Peng Lu<sup>_†_1</sup> 


Fig. 1: **Real-world Deployment of the System.** We present a learning-based framework that enables a humanoid to perform agile shuttlecock interceptions using a racket. The snapshots demonstrate the zero-shot Sim-to-Real transfer of two fundamental skills: **(a, b) Forehand Lifts** and **(c, d) Backhand Lifts** . The blue circles highlight the successful contact moments between the racket and the shuttlecock. Despite the complexity of the motions, our policy maintains robust balance and tracking accuracy on physical hardware. 

**_Abstract_ — Realizing versatile and human-like performance in high-demand sports like badminton remains a formidable challenge for humanoid robotics. Unlike standard locomotion or static manipulation, this task demands a seamless integration of explosive whole-body coordination and precise, timing-critical interception. While recent advances have achieved lifelike motion mimicry, bridging the gap between kinematic imitation and functional, physics-aware striking without compromising stylistic naturalness is non-trivial. To address this, we propose** **_Imitation-to-Interaction_ , a progressive reinforcement learning framework designed to evolve a robot from a “mimic” to a capable “striker.” Our approach establishes a robust motor prior from human data, distills it into a compact, model-based state representation, and stabilizes dynamics via adversarial priors. Crucially, to overcome the sparsity of expert demonstrations, we introduce a manifold expansion strategy that generalizes discrete strike points into a dense interaction volume. We validate our framework through the mastery of diverse skills, including lifts and drop shots, in simulation. Furthermore, we demonstrate the first zero-shot sim-to-real transfer of anthropomorphic badminton skills to a humanoid robot, successfully replicating the kinetic elegance and functional precision of** 

> _∗_ Equal contribution. _†_ Corresponding author. 

> 1 Authors are with the Adaptive Robotic Controls Lab (ArcLab), Department of Mechanical Engineering, The University of Hong Kong, Hong Kong SAR, China (Email: chen-yeke@connect.hku.hk, lupeng@hku.hk). 

> 2 X. Li, Y. Zhao, and L. Li are with EngineAI Robotics Technology Co., Ltd., Shenzhen, China. 

## **human athletes in the physical world.** 

# I. INTRODUCTION 

Badminton stands as one of the most demanding racket sports, requiring a unique combination of speed, precision, and motor diversity. A proficient human player commands a rich repertoire of strokes—from lightning-fast overhead smashes that overwhelm opponents, to delicate drop shots that barely clear the net. Each stroke involves sophisticated whole-body coordination: power originates from the legs, flows through the rotating trunk, and is ultimately delivered via a precisely timed wrist snap, forming a kinetic chain that exemplifies the elegance of human motor control. 

Beyond raw performance, human badminton motions exhibit a distinctive naturalness and fluency—smooth trajectories, rhythmic timing, and biomechanically efficient postures that are immediately recognizable yet challenging to replicate. Moreover, players continuously adapt to the shuttlecock’s variable trajectory, making split-second decisions on stroke selection and execution. This seamless integration of perception, decision-making, and multi-skill motor execution represents a pinnacle of human sensorimotor intelligence— and sets an ambitious target for robotic systems aspiring to achieve human-like athletic performance. 

While human players seamlessly switch between thundering smashes and feathery drop shots with whole-body coordination, significant breakthroughs have been made in legged robot research, but challenges remain. Among these, [1] [2] [3] [4] [5] [6] [7] [8] have achieved humanoid-like motions, yet lack precise interaction with tiny objects. [9] [10] demonstrates successful interaction but falls short of agile, whole-body coordination. Several works have explored ball-related sports; however, some only validate their methods in simulation without real robotic system testing [11] [12] [13] [14] [15], others fail to fully realize humanoid characteristics [16] [17] [18] [19]. Some have learned agile human-like motions [20] [21] — yet realizing versatile and human-like performance in high-demand sports like badminton, which require precise timing, accuracy, and agility, remains a formidable challenge. These limitations highlight the gap that this work aims to address. 

To bridge the gap between kinematic mimicry and dynamic interaction, we propose a progressive “Imitationto-Interaction” framework. Our method decouples wholebody coordination from precise striking through a fourstage pipeline: (1) learning a robust motor prior via motion tracking; (2) performing goal-conditioned distillation to initialize a student policy with a model-based state representation (incorporating _Time-to-Hit_ , _Target Hit State_ and _Target Recovery State_ ) and forward-compatible critics; (3) stabilizing motion execution through reinforcement learning (RL) with Adversarial Motion Priors (AMP) [22] [23]; and (4) conducting interaction-driven refinement in a physicsinteractive environment. This final stage generalizes the policy from sparse dataset samples to a dense interaction manifold, transforming the agent from a “mimic” to a functional “striker.” We validate our approach through extensive experiments and successfully demonstrate agile, human-like badminton striking on a physical humanoid robot. 

In summary, our main contributions are as follows: 

- We propose a progressive learning framework that bridges the gap between kinematic imitation and dynamic interaction. This enables the synthesis of agile, high-velocity sports movements that are distinctively **human-like** in coordination and style. 

- We introduce a specialized state representation that **preserves** the motion priors inherent in human data. This design ensures stable transitions from kinematic tracking to physics-aware striking, maintaining natural behavioral fidelity even during aggressive maneuvers. 

- We achieve the first zero-shot sim-to-real transfer of whole-body badminton skills to a humanoid robot with **anthropomorphic** agility, demonstrating robust striking capabilities and stylistic realism in the physical world. 

# II. RELATED WORKS 

# _A. Humanoid Whole-Body Control_ 

Achieving stable yet agile whole-body control is a fundamental challenge in humanoid robotics. Early approaches predominantly relied on model-based trajectory optimization 

[24] [25] [26] [27]. While theoretically sound, these methods rely heavily on accurate dynamics modeling and often result in stiff behaviors that struggle to adapt to the unpredictable contact dynamics of real-world environments. 

The rapid development of RL has enabled robots to learn robust controllers directly through trial-and-error [28] [29] [30] [31]. To synthesize naturalistic behaviors, imitation techniques [32] have been widely adopted. Seminal works like [3] [1] [2] [33] utilize tracking-based rewards to replicate complex kinematic skills with high fidelity. Parallel to tracking, AMP [22] provides an alternative paradigm, enabling robots to learn versatile interaction tasks while implicitly maintaining a human-like style [8]. 

However, a disconnect remains between mimicking motion and functional interaction. While methods like [7] [6] [5] [4] [8] have explored object interaction, they are often limited to large, static targets. Other works [10] [9] have achieved precise manipulation of small objects via teleoperation and imitation, yet these typically focus on upper-limb dexterity, lacking the explosive, whole-body coordination required for athletic sports. Our work builds upon these foundations but ventures into a more challenging domain: leveraging human motion priors to interact with tiny, high-velocity objects in sparse-reward settings, where the demand for both precision and agility is significantly amplified. 

# _B. Dynamic Ball Sports in Legged Robotics_ 

Ball sports serve as a comprehensive benchmark for testing integrated locomotion, precision control, and rapid decisionmaking. Significant progress has been made in groundbased tasks, such as robot soccer [5] [34], where legged agents learn robust object interaction. However, these tasks are predominantly confined to the 2D ground plane, which simplifies the interception problem compared to aerial sports. 

In the realm of aerial sports, systems have been developed for badminton and table tennis using fixed robotic arms as well as quadrupedal and humanoid platforms [16] [17] [18] [35]. While these works demonstrate impressive task success rates, they often prioritize functional engineering— adopting distinct, non-human strategies—over biomechanical realism. Concurrently, other studies have explored agile, human-like aerial ball sports [12] [13] [14] [15] [11] [36]; however, these represent simulated avatars rather than physical machines, lacking validation on robotic morphologies or transfer to real-world hardware. Recently, several works have successfully learned agile human-like motions [20] [21], enabling robots to perform dynamic maneuvers ranging from rapid table tennis strokes to agile goalkeeping actions. Nevertheless, realizing versatile and human-like performance in high-demand sports like badminton, which require precise timing, accuracy, and agility, remains a formidable challenge. This work aims to bridge this gap, synthesizing a policy that achieves high-performance striking without sacrificing the natural elegance and efficiency of the human kinetic chain. 


Fig. 2: **Overview of the Framework.** The pipeline progressively transforms a kinematic imitator into a dynamic striker through four stages: **(Stage 1) Imitation:** A teacher policy learns to robustly track human motions from MoCap data using proprioceptive (blue) and imitation goal (green) observations. **(Stage 2) Distillation:** The teacher’s capabilities are distilled into a student policy via DAgger. The student operates on a reduced observation space consisting of proprioception, task goals (yellow: target hit/recovery states), and time-to-hit (red), removing dependency on future motion trajectories. **(Stage 3) Stabilization:** The student policy is fine-tuned using RL with an AMP discriminator to enforce stylistic plausibility (Style Reward) while minimizing tracking errors, stabilizing the motion against drift. **(Stage 4) Interaction:** In the final physics-interactive environment, the policy undergoes refinement with simulated shuttlecock dynamics, generalizing to a dense spatio-temporal manifold to achieve precise, agile striking. 

# _C. Goal-Conditioned Reinforcement Learning_ 

Learning agile motor skills to reach dynamic targets can be formulated as a Goal-Conditioned Reinforcement Learning (GCRL) [37] problem. A fundamental challenge in this domain, particularly for high-dimensional legged robot control, is the sparsity of reward signals, which significantly complicates the exploration process [38] [39]. 

To mitigate the exploration burden, hierarchical approaches [40] [41] [42] decouple the problem by using a high-level planner to direct a low-level locomotion controller. However, this decoupling often imposes a performance ceiling: the system’s overall agility is bottlenecked by the constraints of the frozen low-level controller, limiting the emergence of coherent whole-body behaviors. 

Alternatively, techniques such as Reference State Initialization (RSI) [32] [43] leverage expert data to accelerate exploration by initializing the agent in valid states along reference trajectories. While RSI effectively provides highquality starting points, it does not actively govern the transition dynamics _post-initialization_ . The agent still requires explicit guidance—such as tracking rewards or adversarial priors—to maintain physically plausible behavior throughout the episode. 

Our work presents a novel perspective on GCRL by employing a progressive multi-stage framework. By first distilling a robust motor prior to anchoring the policy near the expert manifold and subsequently enabling interactiondriven refinement, we effectively structure the exploration process. This approach allows the agent to retain the stylistic 

quality of expert movements while autonomously exploiting the physics simulation to maximize task performance. 

# III. METHOD 

# _A. Overview_ 

Our framework is designed to enable a humanoid robot to master high-dynamic badminton skills by progressively bridging the gap between kinematic imitation and physicsbased interaction. As illustrated in Fig. 2, the pipeline consists of four stages: (1) **Motion Retargeting and Teacher Training** , where a privileged teacher learns to robustly track human motions; (2) **Goal-Conditioned Distillation** , where a student policy learns to execute these motions based on a hybrid state representation comprising _Time-to-Hit_ , _Target Hit State_ and _Target Recovery State_ ; (3) **Motion Stabilization** , utilizing RL with AMP to refine the student’s tracking stability; and (4) **Interaction-Driven Refinement** , where the policy is fine-tuned in a physics-interactive environment to master ball interception and recovery. 

# _B. Motion Data Processing & Retargeting_ 

We collected a dataset of expert badminton motions using a motion capture system, recording the 6-DoF pose of the racket and body markers. To bridge the morphological gap between the human subject and the robot, we employ a parallel optimization-based retargeting scheme similar to [44]. The retargeting objective minimizes a weighted sum 

of costs: 


where _J_ global aligns key point positions, _J_ local preserves relative positions and angles between key points, _J_ ee, rotation ensures the alignment of racket and feet orientation, _J_ collision prevents collisions to avoid interpenetration and unnatural poses, _J_ limit enforces joint limits to maintain physically plausible postures, and _J_ smooth encourages motion smoothness for natural transitions. Crucially, we jointly optimize the root pose and joint angles to compensate for the robot’s lack of spinal flexibility, ensuring a natural whole-body posture. Additionally, we simultaneously optimize the overall scale and the local scale between keypoints to reduce morphological discrepancies. Finally, the retargeted motions are vertically translated to align the feet with the ground plane, and contact sequences are extracted based on foot height thresholds. The hitting moments and the opponent’s hitting moments (which correspond to the agent’s recovery moments) are manually annotated. 

# _C. Stage 1: Kinematic Motor Prior Learning (Teacher)_ 

The teacher observation at timestep _t_ includes three components: proprioceptive observation, privileged observation, and tracking observation. Formally, it is defined as 


Here, **q** _t_ and **q** ˙ _t_ represent the joint positions and velocities at timestep _t_ ; **v** _t_<sup>base</sup> and **_ω_**<sup>base</sup> _t_ denote the base linear and angular velocities; **g** _t_<sup>proj</sup> represents the gravity vector projected onto the base frame; **a** _t−_ 1 is the policy output at timestep _t −_ 1; _h_<sup>base</sup> _t_ is the base height; **c**<sup>feet</sup> _t_ indicates binary foot contact states; ∆ **s** _t_ : _t_ + _H_ and ∆ **q** _t_ : _t_ + _H_ represent the differences between current and future root states (position, rotation, linear and angular velocity) and joint angles over the horizon _H_ , respectively, all expressed in the base frame. The reward function at timestep _t_ consists of tracking and regularization terms: 


where the regularization reward _rt_<sup>reg</sup> includes common terms such as energy consumption penalties and joint limit constraints, as described in [45]. The term _rt_<sup>term</sup> corresponds to penalties or early termination conditions applied when the agent’s state violates safety or performance constraints, such as base height dropping below a threshold, excessive base rotation, or large deviation from the reference motion. The tracking reward, following a similar format as in [32], can be separated into four components 


with _r_ track, root encourages accurate tracking of the root state, while _r_ track, joint promotes precise tracking of joint angles. The term _r_ track, ee encourages alignment of the end-effector poses, including those of the hands, racket, and feet, and _r_ track, contact fosters rhythmic and clear footwork by faithfully reproducing the ground contact schedule. Note that the tracking rewards for the racket and the root are computed in the world coordinate frame, whereas other components, such as the hand and foot tracking, are defined in the base frame of the robot. 

To improve robustness during distillation, the teacher policy is trained with heavy domain randomization and random external force perturbations. After the initial training, the teacher policy is rolled out to generate physically feasible reference trajectories. The teacher is then further finetuned on these rollouts to improve the precision of the trajectories, providing more accurate targets for the student policy to imitate during distillation. 

# _D. Stage 2: Goal-Conditioned Distillation (Student)_ 

This stage transitions the control strategy from pure tracking to task-oriented execution. We distill the teacher’s knowledge into a student policy _πS_ using DAgger [46], while simultaneously employing the same critic architecture used in subsequent stages, paired with a standard RL loss to facilitate effective policy improvement. 

_1) Goal-Conditioned State Representation:_ We formulate the hitting task as a _goal-conditioned_ task, where the goal is represented using a model-based approach. Due to the rhythmic nature of badminton, the goal naturally divides into two phases: _Preparation_ (before impact) and _Recovery_ (after impact). The student observation **o** student includes proprioceptive information **o**<sup>prop</sup> _t_ and goal components: 

- **Time-to-Hit (TTH)** : A scalar indicating the remaining time until impact. When _TTH >_ 0, the system is in the Preparation phase; when _TTH <_ 0, it is in the Recovery phase. 

- **Target Hit/Recovery State** : The relative difference between the current state and the target state (racket or root pose) at the moment of impact ( _TTH_ = 0) or at recovery. 

To mitigate out-of-distribution (OOD) issues arising from the large combinatorial state space, we implement several parallel design strategies. First, we simplify the input representation by omitting the explicit time-to-recovery variable, as it is rarely observable in practice. Second, to bound the temporal horizon, the TTH variable is explicitly clipped to the range [ _−_ 2 _,_ 2] seconds. Finally, a **phase-dependent masking** strategy is employed to further reduce ambiguity: when TTH _>_ 0 (approach phase), recovery targets are masked to zero; conversely, when TTH _<_ 0 (recovery phase), hit targets are masked. 

_2) Reward Design:_ While the other rewards remain consistent with the previous stage, the tracking reward is tailored for the new task, with distinct objectives in each phase. During the hitting phase ( _TTH >_ 0), the reward encourages accurate tracking of the racket trajectory rather than full-body 

imitation, weighted by an exponential decay on the absolute time-to-hit to emphasize states near impact. In the recovery phase ( _TTH <_ 0), the focus shifts to tracking the root pose without temporal decay, as the policy cannot reliably infer recovery timing from _TTH_ . Formally, the rewards are defined as 


where _i_ and _j_ index state components for hitting and recovery phases, respectively. The manifold-aware error is 


representing the difference between the reference _s_<sup>ref</sup> _ℓ_ and current state _sℓ_ . The squared norm sums over the state dimension: 


# _E. Stage 3: Motion Stabilization with RL_ 

While the distillation stage initializes the general policy behavior, the supervised DAgger loss inherently prioritizes global pose imitation, forcing a trade-off that often yields suboptimal racket tracking precision. To bridge this gap, this stage utilizes pure trial-and-error optimization to shift the focus towards high-precision racket tracking. This enables the robot to enhance its physical stability and minimize interception errors. 

Essentially, in this stage, the student policy is fine-tuned with Adversarial Motion Priors (AMP) [22]. To enforce stylistic plausibility, we introduce a discriminator network _D_ trained to distinguish between the agent’s generated transitions and ground-truth motions. The discriminator operates on a specific observation space **o**<sup>amp</sup> _t_ , which aggregates a history of _HAMP_ = 5 frames to capture temporal motion characteristics: 


The single-frame feature vector **x** _t_ consists of kinematic states expressed in the robot’s local base frame: 


Here, **p**<sup>ee</sup> _t_ and **v** _t_<sup>ee</sup> correspond to the positions and linear velocities of the key end-effectors (ankles and hands) in the base frame. 

The optimization objective follows the Least-Squares GAN (LSGAN) formulation with a gradient penalty [47]. The total reward _rt_ is a weighted combination of the task reward and the style reward: 


where _rt_<sup>task</sup> adopts the formulation in Eq (5). 


Fig. 3: **Manifold Expansion of Strike Targets.** The scattered points represent the discrete strike locations from the original MoCap dataset, colorcoded by the time-to-hit (blue for shorter, red for longer durations) relative to the robot’s initial pose. The semi-transparent cyan volume illustrates the expanded, continuous striking manifold achieved by our interaction-driven refinement stage. Our method empowers the robot to generalize from these sparse human demonstrations to a dense, volumetric region of reachable targets across varying temporal horizons. 

The discriminator minimizes the following loss: 


where _M_ represents the reference motion dataset and the last term is the gradient penalty regularizer applied to referenced data samples **o**<sup>D</sup> _t_<sup>.</sup> 

# _F. Stage 4: Interaction-Driven Refinement_ 

In the final stage, we introduce the physics of the shuttlecock. The policy interacts with a physically simulated ball, allowing it to refine its control based on realistic feedback and improve return effectiveness. 

_1) Manifold Expansion:_ Due to the sparsity of strike points in the original Mocap dataset, we expand these discrete points into a denser, near-continuous manifold of reachable strike targets, as shown in Fig. 3. Concretely, we pre-generate a large number of shuttlecock trajectories with varying interception heights and times, then select strike points around the original dataset samples. During training, the policy is tasked with generalizing motor primitives to this enriched target space. 

_2) Reward Design:_ We maintain the tracking rewards from the previous stage for both the hitting and recovery phases. However, the time-decay weighting in the hitting tracking reward is replaced by a sparse indicator function around the exact strike moment: 


where _ϵ >_ 0 is a small threshold defining a narrow time window near impact. This change reflects the fact that only the strike point is known precisely, while racket trajectories immediately before and after are uncertain. Consequently, the policy learns to focus on achieving accurate motion at the strike instant. For the recovery phase, the tracking reward remains unchanged. 

Additionally, we introduce a physics-informed reward based on the ball’s post-hit behavior: 


where _rt_<sup>dir</sup> encourages the ball to land within the opponent’s court, and _rt_<sup>speed</sup> penalizes weak returns to promote effective strikes. 

_3) Physics Simulation of the Ball:_ The shuttlecock’s flight is simulated by applying aerodynamic forces, including air drag and damping torques, to capture its overall flight behavior. In contrast, the contact simulation models the shuttlecock as two distinct parts—the head and the feather skirt—each assigned different material properties. This separation allows for more accurate and physically plausible collision responses with the racket and environment, enabling the policy to learn refined hitting strategies that account for both aerodynamic and contact dynamics. 

_4) Temporal Rhythm Randomization:_ To enhance the policy’s adaptability to variable rhythmic patterns, we implement a stochastic serving and reset mechanism. Specifically, the time interval between a hitting event and the subsequent serve is randomized uniformly within the range of [1 _,_ 6] seconds. This design exposes the robot to a diverse set of temporal states during training. The longer intervals compel the robot to maintain stable idling behaviors in the absence of immediate targets, ensuring energy efficiency and balance. Conversely, the shorter intervals simulate continuous rallies, requiring the robot to intercept incoming shots even when it has not yet fully recovered to a neutral stance, thereby enforcing robustness against suboptimal initial states. 

By integrating manifold expansion, physics-based ball simulation, temporal rhythm randomization, and refined rewards, Stage 4 enables the policy to transition from purely kinematic tracking to interaction-aware control. 

# IV. EXPERIMENTAL RESULTS 

# _A. Implementation Details_ 

_a) Simulation and Training Framework.:_ We develop our training environment using NVIDIA Isaac Sim, leveraging the Isaac Lab to facilitate high-throughput parallel reinforcement learning. The physics engine operates at a frequency of 200 Hz, while the policy runs at 50 Hz. Within this simulation, we successfully train the humanoid to master a diverse repertoire of badminton skills without modifying the core pipeline, specifically including forehand and backhand lifts and drop shots, as visualized in Fig. 4. 

_b) Hardware and Perception Setup.:_ We conduct realworld evaluations using the EngineAI PM01 humanoid robot. To obtain precise ground truth states for the experiments, we utilize an FZMotion optical motion capture system. This system tracks the 6-DoF pose of the robot’s base link as well as the real-time 3D position of the badminton ball. To handle sensor noise and latency, we implement an Extended Kalman Filter (EKF) that estimates the ball’s full state (position and velocity) from the raw motion capture observations, which is also employed to predict the future trajectory and the optimal 

hitting point, enabling the robot to plan interception motions proactively. 

_c) Domain Randomization.:_ To facilitate robust Sim-toReal transfer and ensure the policy remains effective under real-world uncertainties, we apply extensive domain randomization during the training phase. The specific randomization ranges for these critical parameters are detailed in Table I. 

|**Parameters**|**Range**|**Unit**|
|---|---|---|
|_Robot Dynamics & Payload_|||
|Base Mass Variation|[_−_3_._0_,_5_._0]|kg|
|Hand Mass Variation|[_−_0_._05_,_0_._15]|kg|
|Racket Mass Variation<br><br>|[_−_0_._005_,_0_._005]<br>|kg|
|CoM Offset (_x, y_)<br>|[_−_0_._05_,_0_._05]<br>|m|
|CoM Offset (_z_)|[_−_0_._03_,_0_._03]<br>|m|
|PD Gain Scale|[0_._9_,_1_._1]<br>|-|
|Control Latency|[5_,_30]|ms|
|_Environment & Interaction_|||
|Ground Friction|[0_._5_,_1_._0]<br>|-|
|Restitution Coeff.|[0_._0_,_0_._2]|-|
|Base Velocity Perturbation|[_−_0_._4_,_0_._4]<br>|m/s|
|Terrain Height Noise|[0_,_0_._05]|m|


TABLE I: **Domain Randomization Parameters.** We randomize dynamic and environmental parameters to bridge the sim-to-real gap. 

# _B. Simulation Experiments_ 

To comprehensively evaluate the efficacy of our proposed framework, we conduct extensive experiments in simulation. The primary goal is to verify the contribution of each stage in our pipeline and to demonstrate its superiority over representative end-to-end and hierarchical baselines. 

_a) Task and Environment Setup:_ We focus on the Lift task, evaluated in a specialized environment designed to test the robot’s interception capabilities. We classify the evaluation scenarios into two difficulty levels based on the spatial extent of the required coverage. Both modes define a total effective striking volume that encompasses both _forehand_ and _backhand_ areas relative to the robot’s base: 

- **Easy Mode:** The shuttlecock targets are sampled within a moderate volume of 2 _._ 0 _×_ 0 _._ 4 _×_ 0 _._ 3 m<sup>3</sup> . 

- **Hard Mode:** The target volume is expanded to 4 _._ 0 _×_ 1 _._ 0 _×_ 0 _._ 3 m<sup>3</sup> , necessitating agile bi-directional locomotion and versatile whole-body coordination to cover the substantial lateral range. 

Statistical results are aggregated over 4 _,_ 096 parallel environments, with each episode lasting 4 _,_ 000 steps (80 seconds). 

- _b) Baselines and Ablations:_ We compare our full 

- method ( **Ours** ) against the following ablations and baselines: _•_ **w/o Stab.:** Removes the motion stabilization stage (Stage 3). The policy distilled from the teacher (Stage 2) is directly fine-tuned in the interaction environment. 

- **E2E-AMP:** Removes the imitation stages (Stages 1-3). The policy learns from scratch using AMP and task rewards directly in the physics environment. 

- **w/o Interact.:** Removes the final interaction-driven refinement (Stage 4). We evaluate the policy immediately after the motion stabilization stage. 


Fig. 4: **Diverse Badminton Skills Learned via the Proposed Framework.** Time-lapse sequences demonstrating the humanoid’s mastery of distinct striking techniques. **(a) Backhand Lift:** The robot rotates its torso to generate “whipping” power for a cross-body return. **(b) Forehand Lift:** The robot executes an extended lunge to reach a distant target and quickly recovers balance. **(c) Drop Shot:** The robot performs an overhead strike with a natural inertial follow-through. Pink dots visualize the historical trajectory of the shuttlecock. 

|Method|S|R_↑_|MS|E_↓_|IB|R_↑_|
|---|---|---|---|---|---|---|
||easy|hard|easy|hard|easy|hard|
|Ours|**0.9516** _±_ **0.0005**|**0.9153** _±_ **0.0007**|**0.0062** _±_ **0.0003**|**0.0108** _±_ **0.0003**|0.1999 _±_ 0.0037|**0.1575** _±_ **0.0042**|
|w/o Stab.|0.9501 _±_ 0.0011|0.9147 _±_ 0.0016|0.0094 _±_ 0.0001|0.0162 _±_ 0.0003|0.1363 _±_ 0.0039|0.1148 _±_ 0.0031|
|E2E-AMP|0.8586 _±_ 0.0016|0.7391 _±_ 0.0016|0.2109 _±_ 0.0024|0.6004 _±_ 0.0006|**0.2383** _±_ **0.0061**|0.0990 _±_ 0.0002|
|w/o Interact.|0.3787 _±_ 0.0017|0.3583 _±_ 0.0014|0.3419 _±_ 0.0068|0.3569 _±_ 0.0013|-0.0210 _±_ 0.0006|-0.0230 _±_ 0.0008|
|ASE-Based|0.0037 _±_ 0.0006|0.0034 _±_ 0.0000|4.2742 _±_ 0.0422|4.3395 _±_ 0.0000|-0.2671 _±_ 0.0003|-0.2682 _±_ 0.0000|
|VQ-Based|0.0042 _±_ 0.0003|0.0041 _±_ 0.0003|3.3111 _±_ 0.0329|3.3766 _±_ 0.0172|-0.2770 _±_ 0.0009|-0.2753 _±_ 0.0032|


TABLE II: **Quantitative Comparison in Simulation.** We report the performance of our method against baselines on the Lift task. Best results are highlighted in **bold** . 

- **ASE-Based:** A hierarchical approach based on Adversarial Skill Embeddings (ASE) [48], utilizing a latent space to drive low-level control, like [36]. 

- **VQ-Based:** A hierarchical approach utilizing a VQVAE-based latent space [49] for action generation. 

- _c) Evaluation Metrics:_ We quantify the performance 

- using three key indicators: 

- **Success Rate (SR):** The percentage of episodes where the robot successfully intercepts and contacts the shuttlecock, measuring the fundamental reliability of the policy. 

- **Tracking Error (MSE):** The mean squared Euclidean 

distance between the racket’s sweet spot and the ball’s position at the moment of impact. This metric evaluates the fine-grained spatial precision of the control. 

- **In-Bounds Reward (IBR):** A continuous cumulative metric reflecting the overall quality of the return shot. Unlike a binary success count, IBR aggregates weighted rewards for valid landings within court boundaries while penalizing out-of-bounds or net collisions. 

_Importance of Progressive Stages:_ **Ours** achieves the best overall performance across both difficulty levels, particularly in SR and MSE. Comparing **Ours** with **E2E-AMP** , we observe a significant performance drop in the latter. This indicates that the teacher mimicry and distillation stages (Stages 1 & 2) are critical for establishing a valid motor prior; without them, the RL agent struggles to explore all effective striking poses. Interestingly, **E2E-AMP** achieves a higher IBR than **Ours** in the _Easy_ setting. This is a case of survivorship bias: the E2E policy has a lower Success Rate and only intercepts the most accessible balls (those easy to return in-bounds), whereas **Ours** aggressively attempts to return difficult shots, occasionally leading to out-of-bounds penalties. 

_Role of Stabilization and Refinement:_ **w/o Stab.** achieves performance metrics comparable to the full method, indicating that the motion stabilization stage is not the primary determinant of the final performance. However, its contribution is critical for the development efficiency. In practice, a significant portion of the workflow is dedicated to tuning the interaction environment and reward functions. By providing a robust policy initialization, Stage 3 drastically reduces the convergence time required for each tuning iteration, thereby streamlining the overall experimentation and debugging process. Conversely, **w/o Interact.** exhibits poor performance, even yielding negative IBR in some cases. This highlights a critical gap between kinematic fidelity and functional success: merely mimicking human poses does not guarantee physically valid shuttlecock trajectories (e.g., ensuring the ball clears the net). Furthermore, the substantially low success rate without Stage 4 underscores that the sparse MoCap data is insufficient for generalization across dynamic interception scenarios. 

_Comparison with Hierarchical Baselines:_ Both **ASEBased** and **VQ-Based** methods struggle significantly in this task. The ASE-based approach suffers from mode collapse; faced with the strict hardware constraints of the humanoid (limited torque, heavy limbs) and domain randomization, the low-level controller conservatively converges to a narrow set of stable poses, failing to execute the dynamic reaches required for badminton. Similarly, the VQ-Based method fails to achieve precise control, likely because the compressed discrete latent space lacks the high-frequency granularity needed for fine-grained interception tasks. 

_d) Qualitative Analysis of Learned Behaviors:_ Beyond quantitative metrics, we observe that the learned policy exhibits sophisticated, non-conservative movement patterns that align with professional badminton biomechanics. As 

visualized in Fig. 4, the robot does not treat the racket as a static paddle; instead, it learns to execute complex **slicing motions** where the racket’s velocity vector is intentionally non-orthogonal to the racket face. This allows for precise control over the shuttlecock’s trajectory, rather than simple elastic collisions. 

Specific emergent behaviors highlight the policy’s mastery of whole-body dynamics: 

- **Whole-Body Torque Generation (Fig. 4a):** In the backhand lift, the robot initiates a distinct torso rotation away from the net. During the strike, it rapidly “uncoils” its trunk, transferring angular momentum from the core to the arm. This whipping motion allows the robot to generate sufficient return force to “twist” the shuttlecock back to the opponent’s court, compensating for the limited range of motion in the robot’s wrist. 

- **Dynamic Lunge and Recovery (Fig. 4b):** Faced with a distant forehand target, the robot performs an aggressive lunge, shifting its Center of Mass (CoM) significantly forward to extend its reach. Crucially, immediately after the strike, the policy utilizes ground reaction forces to push back, rapidly recovering to a neutral stance. This “attack-and-return” pattern demonstrates the policy’s foresight in managing stability for subsequent shots. 

- **Inertial Follow-Through (Fig. 4c):** During the drop shot, the robot adopts a high preparatory posture (“cocking” phase) before accelerating the racket for a highvelocity overhead strike. Notably, the arm does not stop abruptly at the impact point; instead, the policy exhibits a natural follow-through, allowing the arm to swing downward, dissipating the kinetic energy. This smooth deceleration mimics human motor control strategies to reduce joint stress and maintain fluid motion. 

# _C. Real-World Experiments_ 

We conduct real-world deployment to validate the feasibility of our zero-shot Sim-to-Real transfer. Specifically, we deploy both the learned lift policy directly onto the EngineAI PM01 humanoid robot without any fine-tuning on the physical hardware. 

_a) Qualitative Analysis: Whole-Body Coordination.:_ As illustrated in Fig. 1, for both forehand and backhand lift skills, the robot faithfully reproduces the temporal structure of a professional stroke. Specifically, in the **Backhand Lift** (Fig. 1c-d), we observe a pronounced trunk rotation: the robot turns its back partially towards the net to clear space for the arm to cross the body, generating torque through sudden uncoiling. In the **Forehand Lift** (Fig. 1a-b), the robot executes a deep lunge to extend its reach. Notably, despite the high velocity of the swing, the robot maintains stability through the follow-through phase, dissipating the arm’s kinetic energy while actively adjusting its foot placement to recover a neutral stance. 

A critical hardware constraint of the PM01 robot is that its arms possess only **5 Degrees of Freedom (DoF)** , lacking the full wrist dexterity used by humans. To overcome this, our policy successfully exploits whole-body coordination. By 

coupling the arm motion with torso yaw and precise base orientation, the robot aligns its entire body to compensate for the missing arm DoFs, ensuring the racket face strikes the shuttlecock at the correct angle to propel it forward. 

_b) Sim-to-Real Gap Analysis.:_ While the robot successfully performs the tasks, we observe distinct behavioral shifts compared to simulation due to the inevitable reality gap. Unlike the smooth, single-motion lunges in simulation, the physical robot exhibits high-frequency footwork adjustments (i.e., rapid shuffling steps) during the approach and recovery phases. We attribute this primarily to the system latencies and unmodeled joint friction, which cause slight tracking delays. The policy detects these discrepancies and reacts by generating rapid corrective steps to maintain the CoM within the support polygon. Crucially, despite these oscillations and the lack of a perfectly stable visual appearance, the robot does not fall and successfully intercepts the ball. This highlights the policy’s robustness: rather than overfitting to an ideal physics model, it adapts to dynamic uncertainties by prioritizing balance recovery over kinematic smoothness. 

_c) Quantitative Results.:_ We evaluated the skills in a controlled test set of 10 trials each. The policy achieved a success rate of 90% for forehand lifts and 70% for backhand lifts. These results confirm that our framework effectively synthesizes dynamic motion primitives that are robust enough for real-world deployment despite hardware limitations. 

# V. CONCLUSION 

In this work, we presented _Imitation-to-Interaction_ , a progressive reinforcement learning framework enabling humanoid robots to master dynamic badminton skills. By bridging the gap between kinematic human demonstrations and physics-based interactions, we successfully demonstrated diverse skills in simulation and validated the feasibility of zero-shot transfer on a physical humanoid robot. 

However, a primary limitation remains in the delicate trade-off between **motion naturalness, dynamic stability, and task precision** . We observe that these objectives often compete directly against one another: pursuing human-like aesthetics (e.g., deep lunges and torso rotations) introduces instability, particularly under real-world latencies; prioritizing pure interception accuracy can lead to physiologically implausible (“twisted”) postures; while excessive stability constraints result in conservative behaviors that degrade agility. Currently, balancing these conflicting objectives requires meticulous tuning. Additionally, our current system focuses on intercepting single shots within a localized area. Achieving continuous **human-robot rallies** and scaling the locomotion to support **full-court coverage** remain open challenges. 

Future work will aim to address the stability-agility conflict through more adaptive control frameworks and extend the robot’s capabilities to enable sustained, full-court gameplay against human opponents. 

# VI. ACKNOWLEDGMENT 

This work was conducted during the author’s internship at EngineAI. The authors would like to thank EngineAI for the support and resources provided. We also extend our gratitude to Yinghui Li, Erdong Xiao, Guanda Li and Zhilin Xiong for their insightful discussions and valuable feedback throughout this project. 

# REFERENCES 

- [1] Q. Liao, T. E. Truong, X. Huang, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [2] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li, “Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills,” _arXiv preprint arXiv:2506.12851_ , 2025. 

- [3] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [4] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi, “Hdmi: Learning interactive humanoid whole-body control from human videos,” _arXiv preprint arXiv:2509.16757_ , 2025. 

- [5] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu, “Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation,” _arXiv preprint arXiv:2509.20322_ , 2025. 

- [6] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa, “Visual imitation enables contextual humanoid control,” _arXiv preprint arXiv:2505.03729_ , 2025. 

- [7] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” _arXiv preprint arXiv:2509.26633_ , 2025. 

- [8] H. Wang, W. Zhang, R. Yu, T. Huang, J. Ren, F. Jia, Z. Wang, X. Niu, X. Chen, J. Chen, _et al._ , “Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system,” _arXiv preprint arXiv:2510.11072_ , 2025. 

- [9] T. He, Z. Wang, H. Xue, Q. Ben, Z. Luo, W. Xiao, Y. Yuan, X. Da, F. Casta˜neda, S. Sastry, _et al._ , “Viral: Visual sim-to-real at scale for humanoid loco-manipulation,” _arXiv preprint arXiv:2511.15200_ , 2025. 

- [10] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit,” _arXiv preprint arXiv:2502.13013_ , 2025. 

- [11] Z. Luo, J. Wang, K. Liu, H. Zhang, C. Tessler, J. Wang, Y. Yuan, J. Cao, Z. Lin, F. Wang, _et al._ , “Smplolympics: Sports environments for physically simulated humanoids,” _arXiv preprint arXiv:2407.00187_ , 2024. 

- [12] P. Xu, Z. Wu, R. Wang, V. Sarukkai, K. Fatahalian, I. Karamouzas, V. Zordan, and C. K. Liu, “Learning to ball: Composing policies for long-horizon basketball moves,” _arXiv preprint arXiv:2509.22442_ , 2025. 

- [13] R. Yu, Y. Wang, Q. Zhao, H. W. Tsui, J. Wang, P. Tan, and Q. Chen, “Skillmimic-v2: Learning robust and generalizable interaction skills from sparse and noisy demonstrations,” in _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , 2025, pp. 1–11. 

- [14] Y. Wang, Q. Zhao, R. Yu, H. W. Tsui, A. Zeng, J. Lin, Z. Luo, J. Yu, X. Li, Q. Chen, _et al._ , “Skillmimic: Learning basketball interaction skills from demonstrations,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 17 540–17 549. 

- [15] H. Zhang, Y. Yuan, V. Makoviychuk, Y. Guo, S. Fidler, X. B. Peng, and K. Fatahalian, “Learning physically simulated tennis skills from broadcast videos,” _ACM Transactions on Graphics (TOG)_ , vol. 42, no. 4, pp. 1–14, 2023. 

- [16] Y. Ma, A. Cramariuc, F. Farshidian, and M. Hutter, “Learning coordinated badminton skills for legged manipulators,” _Science Robotics_ , vol. 10, no. 102, p. eadu3922, 2025. 

- [17] C. Liu, L. Jiang, Y. Wang, K. Yao, J. Fu, and X. Ren, “Humanoid whole-body badminton via multi-stage reinforcement learning,” _arXiv preprint arXiv:2511.11218_ , 2025. 

- [18] M. Hu, W. Chen, W. Li, F. Mandali, Z. He, R. Zhang, P. Krisna, K. Christian, L. Benaharon, D. Ma, _et al._ , “Towards versatile humanoid table tennis: Unified reinforcement learning with prediction augmentation,” _arXiv preprint arXiv:2509.21690_ , 2025. 

- [19] D. Nguyen, Z. Zaidi, K. Karol, J. Hodgins, and Z. Xie, “Whole body model predictive control for spin-aware quadrupedal table tennis,” _arXiv preprint arXiv:2510.08754_ , 2025. 

- [20] Z. Su, B. Zhang, N. Rahmanian, Y. Gao, Q. Liao, C. Regan, K. Sreenath, and S. S. Sastry, “Hitter: A humanoid table tennis robot via hierarchical planning and learning,” _arXiv preprint arXiv:2508.21043_ , 2025. 

- [21] J. Ren, J. Long, T. Huang, H. Wang, Z. Wang, F. Jia, W. Zhang, J. Wang, P. Luo, and J. Pang, “Humanoid goalkeeper: Learning from position conditioned task-motion constraints,” _arXiv preprint arXiv:2510.18002_ , 2025. 

- [22] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [23] Z. Luo, J. Zhang, Y. Han, J. Ma, M. Lu, I. Havoutis, and P. Lu, “Learning highly dynamic skills transition for quadruped jumping through constrained space,” _Advanced Robotics Research_ , p. e202500032, 2025. 

- [24] A. Dallard, M. Benallegue, F. Kanehiro, and A. Kheddar, “Synchronized human-humanoid motion imitation,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 7, pp. 4155–4162, 2023. 

- [25] B. Dariush, M. Gienger, B. Jian, C. Goerick, and K. Fujimura, “Whole body humanoid control from human motion descriptors,” in _2008 IEEE International Conference on Robotics and Automation_ . IEEE, 2008, pp. 2677–2684. 

- [26] J. Ramos and S. Kim, “Dynamic locomotion synchronization of bipedal robot and human operator via bilateral feedback teleoperation,” _Science Robotics_ , vol. 4, no. 35, p. eaav4282, 2019. 

- [27] M. Chignoli, D. Kim, E. Stanger-Jones, and S. Kim, “The mit humanoid robot: Design, motion planning, and control for acrobatic behaviors,” in _2020 IEEE-RAS 20th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2021, pp. 1–8. 

- [28] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 91–100. 

- [29] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao, “Robot parkour learning,” _arXiv preprint arXiv:2309.05665_ , 2023. 

learning,” _arXiv preprint arXiv:2302.09450_ , 2023. 

   - [39] N. Rudin, D. Hoeller, M. Bjelonic, and M. Hutter, “Advanced skills by learning locomotion and local navigation end-to-end,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 2497–2503. 

   - [40] K. Caluwaerts, A. Iscen, J. C. Kew, W. Yu, T. Zhang, D. Freeman, K.-H. Lee, L. Lee, S. Saliceti, V. Zhuang, _et al._ , “Barkour: Benchmarking animal-level agility with quadruped robots,” _arXiv preprint arXiv:2305.14654_ , 2023. 

   - [41] T. Miki, J. Lee, L. Wellhausen, and M. Hutter, “Learning to walk in confined spaces using 3d representation,” _arXiv preprint arXiv:2403.00187_ , 2024. 

   - [42] D. Hoeller, N. Rudin, D. Sako, and M. Hutter, “Anymal parkour: Learning agile navigation for quadrupedal robots,” _Science Robotics_ , vol. 9, no. 88, p. eadi7566, 2024. 

   - [43] T. Wu, Y. Chen, T. Chen, G. Zhao, and F. Gao, “Whole-body control through narrow gaps from pixels to action,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 11 317–11 324. 

   - [44] C. M. Kim, B. Yi, H. Choi, Y. Ma, K. Goldberg, and A. Kanazawa, “Pyroki: A modular toolkit for robot kinematic optimization,” _arXiv preprint arXiv:2505.03728_ , 2025. 

   - [45] G. B. Margolis and P. Agrawal, “Walk these ways: Tuning robot control for generalization with multiplicity of behavior,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 22–31. 

   - [46] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 

   - [47] A. Escontrela, X. B. Peng, W. Yu, T. Zhang, A. Iscen, K. Goldberg, and P. Abbeel, “Adversarial motion priors make good substitutes for complex reward functions,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 25–32. 

   - [48] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler, “Ase: Largescale reusable adversarial skill embeddings for physically simulated characters,” _ACM Transactions On Graphics (TOG)_ , vol. 41, no. 4, pp. 1–17, 2022. 

   - [49] Q. Zhu, H. Zhang, M. Lan, and L. Han, “Neural categorical priors for physics-based character control,” _ACM Transactions on Graphics (TOG)_ , vol. 42, no. 6, pp. 1–16, 2023. 

- [30] Y. Chen, J. Ma, Z. Luo, Y. Han, Y. Dong, B. Xu, and P. Lu, “Learning autonomous and safe quadruped traversal of complex terrains using multi-layer elevation maps,” _IEEE Robotics and Automation Letters_ , 2025. 

- [31] Z. Luo, J. Zhang, Z. Xu, W. Li, X. Li, X. Chen, Z. Yu, A. Tang, and P. Lu, “Mild: Tractable terrain modeling for learning improved bipedal locomotion on deformable surfaces,” _IEEE Robotics and Automation Letters_ , vol. 11, no. 2, pp. 1922–1929, 2025. 

- [32] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [33] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu, _et al._ , “Track any motions under any disturbances,” _arXiv preprint arXiv:2509.13833_ , 2025. 

- [34] X. Huang, Z. Li, Y. Xiang, Y. Ni, Y. Chi, Y. Li, L. Yang, X. B. Peng, and K. Sreenath, “Creating a dynamic quadrupedal robotic goalkeeper with reinforcement learning,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023, pp. 2715–2722. 

- [35] D. B¨uchler, S. Guist, R. Calandra, V. Berenz, B. Sch¨olkopf, and J. Peters, “Learning to play table tennis from scratch using muscular robots,” _IEEE Transactions on Robotics_ , vol. 38, no. 6, pp. 3850–3860, 2022. 

- [36] J. Wang, J. Hodgins, and J. Won, “Strategy and skill learning for physics-based table tennis animation,” in _ACM SIGGRAPH 2024 Conference Papers_ , 2024, pp. 1–11. 

- [37] M. Liu, M. Zhu, and W. Zhang, “Goal-conditioned reinforcement learning: Problems and solutions,” _arXiv preprint arXiv:2201.08299_ , 2022. 

- [38] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Robust and versatile bipedal jumping control through reinforcement 

