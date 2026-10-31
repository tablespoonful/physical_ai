---
title: "Tree Learning: A Multi-Skill Continual Learning Framework for Humanoid Robots"
date: "2026-04-14"
authors: "Yifei Yan; Linqi Ye"
url: https://arxiv.org/abs/2604.12909
pdf: https://arxiv.org/pdf/2604.12909
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.12909)** / [論文ページ](https://arxiv.org/abs/2604.12909)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Tree Learning: A Multi-Skill Continual Learning Framework for Humanoid Robots 

Yifei Yan<sup>_a_</sup> , Linqi Ye<sup>_a_,∗</sup> 

_aSchool of Future Technology, Shanghai University, No. 99 Shangda Road, Baoshan District, Shanghai, 200444, Shanghai, China_ 

|A R T I C L E I N F O|A B S T R A C T|
|---|---|
|_Keywords_:<br>Tree Learning|As reinforcement learning for humanoid robots evolves from single-task to multi-skill paradigms,<br>efficiently expanding new skills while avoiding catastrophic forgetting has become a key challenge in|
|Reinforcement learning<br>Continual learning<br>Humanoid robot<br>Embodied intelligence|embodied intelligence. Existing approaches either rely on complex topology adjustments in Mixture-<br>of-Experts (MoE) models or require training extremely large-scale models, making lightweight<br>deployment difficult. To address this, we propose Tree Learning, a multi-skill continual learning<br>framework for humanoid robots. The framework adopts a root-branch hierarchical parameter inheri-<br>tance mechanism, providing motion priors for branch skills through parameter reuse to fundamentally<br>prevent catastrophic forgetting. A multi-modal feedforward adaptation mechanism combining phase<br>modulation and interpolation is designed to support both periodic and aperiodic motions. A task-<br>level reward shaping strategy is also proposed to accelerate skill convergence. Unity-based simulation<br>experiments show that, in contrast to simultaneous multi-task training, Tree Learning achieves higher<br>rewards across various representative locomotion skills while maintaining a 100% skill retention rate,<br>enabling seamless multi-skill switching and real-time interactive control. We further validate the<br>performance and generalization capability of Tree Learning on two distinct Unity-simulated tasks:<br>a Super Mario-inspired interactive scenario and autonomous navigation in a classical Chinese garden<br>environment.|


# **1. Introduction** 

The rapid development of embodied intelligence is driving autonomous robot technology from controlled laboratory environments toward general-purpose real-world scenarios [1, 2, 3]. As a typical representative of embodied intelligence, humanoid robots possess significant advantages in navigating unstructured environments—such as roads, staircases, and debris—due to their human-like gait and body structure [4, 5]. In recent years, reinforcement learning (RL)based motion control methods [6, 7, 8, 9] have been evolving from single-task adaptation toward multi-skill incremental expansion, posing significant challenges in terms of generalization capability, continual learning efficiency, and system scalability. 

In the domain of humanoid robots acquiring diverse skills, several recent advances have been achieved. BeyondMimic [10] realized flexible cross-task trajectory synthesis through a guided diffusion model. The KungfuBot series [11, 12] leveraged orthogonal mixture-of-experts (OMoE) models and bilevel optimization algorithms, enabling robots to imitate highly dynamic behaviors such as martial arts and dance. Any2Track [13] proposed a two-stage framework that substantially enhanced motion tracking robustness under multi-source disturbances. 

However, three major technical gaps remain with respect to the core demand for continual incremental expansion. First, existing MoE-based approaches [14, 15, 16, 17] often require network topology adjustments when introducing new skills, while approaches represented by SONIC [18] tend 

> Project page: https://yyf-prog.github.io/Tree-learning/ 

> ∗Corresponding author. 


> yyf20041019@shu.edu.cn (Y. Yan); yelinqi@shu.edu.cn (L. Ye) 

to train extremely large-scale models, leading to computational costs that grow rapidly with the number of skills and making edge-side lightweight deployment difficult. Second, motion imitation-based methods [19, 20, 21] typically require full policy retraining when learning new motions, which readily leads to degradation of existing fundamental capabilities—the well-known catastrophic forgetting problem. Third, existing robust control strategies [22, 23, 24] are largely limited to parameter adaptation for basic gaits and cannot achieve cross-modal motion generalization at low training cost. 


**Figure 1:** Tree Learning diagram. 

Page 1 of 11 

: _Preprint submitted to Elsevier_ 

Inspired by the mechanisms of prior inheritance and specialized evolution observed in biological evolution, this paper proposes Tree Learning (Figure 1)—a multi-skill continual learning framework based on hierarchical inheritance. The framework defines a pre-trained flat-ground basic gait as the root skill, while other skills inherit root skill parameters in a tree-structured manner layer by layer, referred to as branch skills. Through parameter inheritance and reward shaping, branch skills achieve rapid evolution. The main contributions of this paper are as follows: 

(1) A tree-structured parameter inheritance architecture for continual learning is proposed. Through physically isolated sub-network clusters, catastrophic forgetting is fundamentally eliminated, enabling lossless incremental expansion of multiple skills. 

(2) A low-cost skill iteration pipeline is designed, supporting incremental fine-tuning of specific branches and significantly reducing computational and time costs. 

(3) Simulation validation is conducted on the Unitree G1 humanoid robot, achieving efficient expansion and seamless switching of 11 types of highly dynamic skills with real-time interactive control. 

# **2. System Overview** 

As shown in Figure 2, the Tree Learning architecture defines flat-ground walking as the root skill and extends branch skills layer by layer based on a hierarchical inheritance mechanism. Continuing training from the root skill yields first-level branch skills: one-leg standing, stair climbing, lying prone, running, and squatting. From one-legged standing, a second-level branch skill—ball kicking—is derived through further training. From squatting, a secondlevel branch skill—two-footed jumping—is obtained. From the lying prone action, second-level branch skills including push-ups, crawling, and standing up are developed. 


**Figure 2:** Tree Learning for Unitree G1. 

The Tree Learning framework enforces consistency of the global state space and action representation by design. 

Since the root skill and all branch sub-networks share identical sensor input interfaces and joint control output dimensions, and network switching is only performed between skills with overlapping action sequences and state spaces, the system maintains high consistency in motion continuity during dynamic model loading and skill switching. This consistency fundamentally avoids action discontinuities at the moment of neural network switching, thereby effectively preventing abrupt posture changes of the robot and enabling seamless, smooth transitions between heterogeneous locomotion modes. 

In complex terrain or task scenarios requiring finegrained control, the Tree Learning framework supports user intervention in skill switching and action adjustment through a lightweight input interface. For example, users can select target skill models via numeric keys 0/1/2/3 (e.g., 0 for flat-ground walking, 1 for running) and dynamically adjust action commands via W/S/A/D/Q/E letter keys (e.g., W/S for forward/backward, A/D for left/right turning, Q/E for lateral movement). Upon receiving user commands, the system combines state assessment to load the corresponding model and output action commands, forming a closed-loop interaction of user input–model execution–state feedback. This human-robot collaborative mode significantly enhances system adaptability in dynamic scenarios. 


**Figure 3:** Interactive multi-skill control. 

# **3. Methodology** 

## **3.1. Feedforward Action Design** 

For each skill, motion prior is used as a feedforward action to achieve a specific motion style. Different actions are realized through simple feedforward signals. For periodic and aperiodic actions, phase-based and interpolation-based methods are employed, respectively. 

### **_3.1.1. Phase modulation method_** 

For periodic locomotion skills such as walking, running, stair climbing, and jumping, a cosine phase modulation method is used to design the feedforward action trajectory. The core mechanism employs gait phase activation factors _𝑢_ 1 and _𝑢_ 2 to schedule alternating motion of the left and right legs of the humanoid robot, providing a baseline action reference for reinforcement learning and reducing exploration cost. 

Page 2 of 11 

: _Preprint submitted to Elsevier_ 

The factors _𝑢_ 1 and _𝑢_ 2 represent the gait phase activation factors for the robot’s left and right legs, respectively. Their computation relies on the gait cycle counter _𝑡𝑝_ and the gait cycle period _𝑇_ 1. 

The core formulas are given as follows: 


In Eq. (1), the gait time step counter _𝑡𝑝_ auto-increments at each fixed time step (0.01 s) and resets to 0 upon reaching 2 _𝑇_ 1, enabling cyclic gait periodicity. A sub-counter _𝑡𝑝_ 0 is used for single-leg phase cycle calculation. The cosine function maps the [0 _,_ 2 _𝜋_ ] cosine period to [0 _,_ 2], which is then divided by 2 to yield a [0 _,_ 1] phase activation factor, ensuring smooth action scheduling. 

The factors _𝑢_ 1 and _𝑢_ 2 implement left-right leg support phase separation through an alternating activation mechanism. By combining _𝑢_ 1 and _𝑢_ 2 with joint angle coefficients (where _𝑑ℎ_ denotes a dynamic adjustment coefficient and _𝑑_ 0 denotes a base angle offset), feedforward angle commands for the core lower-limb joints (hip, knee, and ankle) are generated. 


In Eq. (2), where _𝑢𝑓_ represents _𝑢_ 1 or _𝑢_ 2, idx is the index mapping array of lower limb joints, and sign(idx[ _𝑖_ ]) is used to control the joint movement direction. Finally, the periodic gait feedforward control of the robot is realized. Different branch skills adapt their characteristics by adjusting _𝑇_ 1, _𝑑ℎ_ , _𝑑_ 0, and the activation logic of _𝑢_ 1 and _𝑢_ 2. 

### **_3.1.2. Interpolation method_** 

For aperiodic actions (e.g., squatting), a linear interpolation method is employed to generate reference joint angles. This method supports continuously adjustable action depth (e.g., linear mapping of squat amplitude between 0–100%). The feedforward commands provide the RL network with baseline trajectory boundaries that carry strong physical meaning, while the policy network is responsible for optimizing action along the feedforward signal, thereby substantially improving the learning efficiency of diverse motion skills. 

**Table 1** 

Basic reward components 

|No.|Reward Term|Mathematical Expression|
|---|---|---|
|1|Velocity tracking|_𝑟_vel = 1 −2|_𝑣𝑥_−_𝑣_<sup>cmd</sup><br>_𝑥_<br>|<br>−2|_𝑣𝑧_−_𝑣_<sup>cmd</sup><br>_𝑧_<br>||
|2|Angular velocity tracking|_𝑟_wel = 1 −2|_𝑤𝑦_−_𝑤_<sup>cmd</sup><br>_𝑦_<br>||
|3|Center of mass height|_𝑟_height = 2(_ℎ_−_ℎ_target)|
|4|Orientation constraint|_𝑟_ori = −0_._1|_𝜃_roll|−0_._1|_𝜃_pitch||
|5|Survival reward|_𝑟_live = 1|
|6|Action energy penalty|_𝑟_penalty = −0_._2 <sup>∑</sup><br>_𝑖_∈_𝐽_<sup>|</sup><sup>_𝑢_</sup>_𝑖_<sup>|</sup>|


## **3.2. Parameter Inheritance** 

Parameter inheritance is primarily embodied in the training phase. The root skill (flat-ground walking) is first trained to completion, equipping the robot with stable basic locomotion capability. All branch skills are initialized from their parent skill network parameters, thus avoiding the efficiency loss associated with training from scratch. 

Branch networks fully inherit the weights of the parent network as their initialization parameter value. This not only preserves the state-perception features and physical dynamics representations extracted in the hidden layers, but also avoids the random exploration inherent in training from scratch. During inference, to satisfy the memory constraints of edge devices and to fundamentally eliminate gradient interference from multi-task joint optimization, the framework employs physically isolated sub-network clusters. By sharing the same state space and similar distribution manifolds, the system ensures continuity of action commands during neural network model switching (models are in ONNX format), thereby achieving incremental expansion of multiple skills. 

## **3.3. Reward Shaping** 

To accelerate skill convergence and improve execution stability, a set of basic reward components is first designed, as shown in Table 1. 

In Table 1, _𝑣𝑥_ is the robot’s lateral velocity; _𝑣_<sup>cmd</sup> _𝑥_ is the robot’s target lateral velocity; _𝑣𝑧_ is the robot’s forward velocity; _𝑣_<sup>cmd</sup> _𝑧_ is the robot’s target forward velocity; _𝑤𝑦_ is the robot’s torso yaw angular velocity about the Y-axis; _𝑤_<sup>cmd</sup> _𝑦_ is the preset target yaw angular velocity about the Y-axis of the robot’s torso; _ℎ_ target is the robot’s torso target height; _𝜃_ roll is the body roll angle; _𝜃_ pitch is the body pitch angle; _𝑢𝑖_ represents the output amplitude of the control command for the corresponding joint. To control redundant movements of non-essential joints, the set of penalty joints is defined as _𝐽_ = {1 _,_ 2 _,_ 5 _,_ 7 _,_ 8 _,_ 11}. 

Since different skills have distinct requirements and preferences, the basic reward components can be recombined or supplemented with preference-specific reward terms to accommodate different skills. 

Page 3 of 11 

: _Preprint submitted to Elsevier_ 

**Table 2** 

Core hyperparameter configuration of PPO 

|No.|Parameter Name|Value|
|---|---|---|
|1|Time steps per update|1000|
|2|Batch size|2048|
|3|Replay buffer size|20480|
|4|Number of epochs|3|
|5|Reward scale|1.0|
|6|Discount factor _𝛾_|0.995|
|7|GAE coefficient _𝜆_|0.95|
|8|Learning rate|3 × 10<sup>−4</sup>|
|9|Clipping parameter _𝜖_|0.2|
|10|Entropy coefficient _𝛽_|5 × 10<sup>−3</sup>|


## **3.4. Training Configuration** 

### **_3.4.1. Network Architecture and RL Algorithm_** 

This study is based on the Unity ML-Agents framework, employing the Proximal Policy Optimization (PPO [25]) algorithm for reinforcement learning training. For the network architecture, the actor policy network adopts a 3-layer fully connected multilayer perceptron (MLP) with 512 hidden units per layer and normalization of input state features. The policy output is set as a Gaussian distribution to ensure nondeterministic exploration. The critic value network uses a 2-layer fully connected structure (hidden layer dimension of 128) without state normalization. During training, model weights are saved every 4×10<sup>5</sup> steps to monitor convergence trends. 

# **4. Comparison with Multi-Task Baseline** 

This section selects 6 representative skills from the 11 skill types for quantitative comparison between Tree Learning and simultaneous multi-task training (Multi-task). In the experiment, the multi-task baseline uses a single policy network to train all 6 skills simultaneously, whereas Tree Learning trains each skill independently. To ensure comparable computational budgets, both experimental groups are set to a total of 10<sup>7</sup> environment steps. 

The experimental results are presented in Figures 4–9. As observed, Tree Learning achieves higher final rewards than the multi-task baseline across all 6 selected skills. Specifically, for the highly dynamic skills Jump and Run, Tree Learning attains stable rewards of 990 and 6138, respectively, while the multi-task baseline achieves only 99 and 609. Figure 10 presents a radar chart of stable converged reward distributions across the 6 skills, clearly showing that the final reward of the Run skill under Tree Learning is substantially higher than that of the multi-task baseline. 

These results indicate that simultaneous multi-task training suffers from significant gradient conflicts: the substantial differences among reward functions for different skills lead to negative transfer during optimization, rendering some highly dynamic skills (e.g., Jump) virtually unable to converge effectively. In contrast, Tree Learning fundamentally avoids gradient interference through physically isolated independent sub-networks, allowing each skill to fully leverage the neural network weights from the root skill to achieve efficient and stable convergence. 

### **_3.4.2. Reinforcement Learning Hyperparameters_** 

The total training steps for different skills are adaptively adjusted according to their convergence difficulty. The core hyperparameters of the PPO algorithm employ a linear decay strategy to balance exploration in the early stages and exploitation in the later stages. The detailed configuration is presented in Table 2. 

### **_3.4.3. Progressive Curriculum Learning_** 

For complex skills with strong terrain constraints, such as stair climbing, direct training in the target staircase environment is prone to becoming trapped in local optima. To address this, an environment-variable-driven curriculum learning mechanism is introduced. Specifically, staircase step height is designated as the curriculum difficulty metric and divided into four progressive stages (Lesson 1 through Lesson 4, with heights set to 0.01 m, 0.05 m, 0.10 m, and 0.15 m, respectively). During training, when the robot’s smoothed cumulative reward at the current stage reaches a preset threshold, the environment automatically advances to the next difficulty level. This mechanism effectively alleviates the sparse reward problem on unstructured terrain, enabling smooth transition and efficient convergence of the robot’s obstacle-crossing capabilities. 


**Figure 4:** Reward comparison of walk skill. 

Page 4 of 11 

: _Preprint submitted to Elsevier_ 


**Figure 8:** Reward comparison of crawl skill. 

**Figure 5:** Reward comparison of run skill. 


**Figure 6:** Reward comparison of squat skill. 


**Figure 7:** Reward comparison of jump skill. 


**Figure 9:** Reward comparison of one-leg stand skill. 


**Figure 10:** Final reward comparison. 

Page 5 of 11 

: _Preprint submitted to Elsevier_ 


**Figure 11:** Super Mario simulation scene. The robot sequentially performed (a) walking, (b) running to escape a ghost, (c) climbing up and down stairs, (d) lying prone, (e) crawling through a tunnel, (f) standing up, and (g) jumping to hit boxes to collect coins or gifts along the way. Finally, (h) the robot kicks a ball into the goal and wins. (i) is the global view. 

# **5. Super Mario Scenario Experiment** 

## **5.1. Simulation Environment and Task Setup** 

The simulation environment was built using Unity 2022. 3.62f3 LTS. The Unitree G1 humanoid robot (23-DoF version) was selected as the experimental platform, configured with 12 lower-limb joints, 1 waist joint, and 10 upper-limb joints. Multi-skill expansion was achieved through coordinated control of lower-limb joint motion and optimization of upper-limb joint motion. To increase the interestingness of the experiment and verify the comprehensive performance of multi-skill capabilities in continuous complex tasks, the experimental scenario was designed in the style of a Super Mario game, as shown in Figure 11. To prevent the robot from deviating laterally, two transparent walls were added to constrain movement to the forward-backward direction. 

## **5.2. Manual Switching Control** 

The Super Mario test scene contains multiple interactive constraints including pursuers, coins, and complex terrain, posing high demands on the temporal sequencing of the humanoid robot’s actions. Experimental observations revealed that the robot must complete multiple action transitions within extremely narrow action windows. Through manual switching control via keyboard, a typical full-process task sequence was successfully executed, validating the physical feasibility of the Tree Learning framework in handling highly dynamic and tightly coupled tasks. See Supplementary Video 1 for details. 

## **5.3. Automatic Switching Control** 

For convenience, we also developed a method to enable the robot to automatically switch from walking to running 

and subsequent complex action sequences based on environmental cues. To quantitatively assess switching continuity, center-of-mass (CoM) height and forward velocity curves were extracted during the automatic switching process. 


**Figure 12:** Ghost chasing scene. 

As shown in Figure 12, when the robot detects a ghost pursuit and triggers an acceleration command, the CoM velocity curve exhibits notable continuity, smoothly transitioning from 0.8 m/s to 2.0 m/s without any step-like jumps or acceleration spikes throughout the switching interval. This smooth locomotion performance physically validates the effectiveness of the state space consistency design proposed in Section 2—namely, that physical quantities from different skill models can naturally align at the moment of switching. The entire automatic task flow demonstrates that the framework possesses high kinematic coherence when handling heterogeneous skill sequences. See Supplementary Video 2 for more details. 

Page 6 of 11 

: _Preprint submitted to Elsevier_ 

# **6. Autonomous Navigation Experiment** 

To further validate the robustness and control quality of the Tree Learning framework under a prolonged continuous task, an autonomous navigation task was designed in a classical Chinese garden scenario. Unlike the manual and automatic switching experiments in previous section, which focused on verifying switching feasibility, this experiment concentrates on a comprehensive evaluation of the robot during nearly 240 seconds of continuous locomotion, encompassing path planning, velocity control, gait switching, posture balancing, and forward-turn exchange. The results are given in Supplementary Video 3. The sampling rate was set to 50 Hz, resulting in about 12,000 recorded frames. 

The navigation test scenario includes buildings, streets, and bridges, as shown in Figure 13. Based on the skills learned by Tree Learning, we adopted a navigation workflow as shown in Figure 14. Figure 13 shows the top-view trajectory of the robot. Starting from the starting point (green dot), the robot follows the path from the planner to sequentially approach multiple operator-specified target points and finally reach the end point (red square). The trajectory covers an area of approximately 30 m × 30 m. Multiple turns and obstacle avoidance behaviors are observed along the path, indicating that the navigation system can effectively plan feasible paths in complex scenarios with various terrains. 

During the experiment, the operator clicks random target points in the scenario in real time. After the robot reaches the current target, the next target point is clicked immediately. During the task, the robot sequentially experiences three motion modes within 240 seconds: walking (Walk), running (Run), and stair climbing (Stair). The gait mode switching is automatically performed by the navigation system according to environmental conditions: when the target distance is far, the system automatically switches to Run mode to improve locomotion efficiency; when stairs are detected ahead, the system automatically switches to Stair mode; in other cases, Walk mode is used by default. 


**Figure 13:** Autonomous navigation task. The left shows snapshots during the task. The right shows the top-down trajectory of the robot. 


**Figure 14:** Autonomous navigation workflow. 

## **6.1. Navigation Performance Analysis** 

Figure 15 presents the position curves of the robot’s center of mass on the three coordinate axes over time. The X-axis position continuously rises from 0 to approximately 27 m after 120 s, corresponding to the robot’s long-distance navigation phase toward a far target. The Z-axis position exhibits reciprocating fluctuations, reflecting the robot’s path between multiple target points. Of particular interest is the Y- axis (height) data: during the flat-ground phase from 0 to 160 s, the center-of-mass height remains stable at approximately 0.78 m with minimal fluctuations. In the interval from 170 to 190 s, the center-of-mass height rises sharply from 0.78 m to approximately 1.78 m and then stabilizes at the top of the stairs, proving that the robot successfully climbed a stair of about 1 m in height. The time interval of this height jump matches exactly with the Stair mode activation interval in Figure 16, verifying the physical effectiveness of gait switching from the spatial position dimension. At the end of the experiment (around 235 s), the Y-axis shows a slight rise again, corresponding to the second short stair climbing. 

Figure 16 quantitatively presents the navigation performance metric over time. The upper figure shows the target distance curve, which exhibits a typical “sawtooth” descending pattern: whenever the distance approaches zero, the system determines that the current target has been reached, the operator specifies a new target immediately, and the distance jumps accordingly. The green vertical lines mark the events of reaching each target. During the entire experiment, the robot successfully reached 22 target points with only one stuck recovery, demonstrating extremely high navigation reliability. Notably, a long-distance navigation segment (with 

Page 7 of 11 

: _Preprint submitted to Elsevier_ 

a distance peak close to 20 m) appears around 120 s, which is a typical scenario where the system automatically switches to Run mode based on the target distance. The lower figure shows the obstacle factor curve, which reflects the degree to which obstacles in front suppress the robot’s speed: a value of 1.0 indicates no obstacles ahead, while values close to 0 indicate detection of close-range obstacles. In the early half of the experiment (0–120 s), the obstacle factor remains at 1.0, indicating that this area is dominated by flat ground or open corridors. In the intervals of 140–170 s and 200–240 s, the obstacle factor drops multiple times, corresponding to the robot entering stairwells or narrow passages and performing obstacle avoidance deceleration. 

Figure 17 presents the statistic of the navigation experiment in three forms: pie chart, bar chart, and histogram. The gait distribution pie chart shows that Walk mode accounts for 87.8%, Stair mode for 10.1%, and Run mode for 2.0%, which is consistent with the expected design of mainly normal walking, automatic acceleration for long-distance targets, and stair climbing. The navigation bar chart visually compares the completion of 22 target points with only one stuck recovery, verifying the high reliability of the system in multiterrain environments. The forward velocity histogram shows a bimodal distribution, with the main peak near 0.0 m/s (corresponding to standing or deceleration phases) and the secondary peak in the range of 0.8–1.0 m/s (corresponding to steady-state forward movement). This distribution is highly consistent with the designed auto-steering control logic. 


**Figure 15:** Robot CoM position curve. 


**Figure 16:** Autonomous navigation metric. 


**Figure 17:** Autonomous navigation statistic. 

## **6.2. Motion Control Analysis** 

Figure 18 shows the time series of control commands _𝑣𝑟_ (forward velocity), _𝑤𝑟_ (turning angular velocity). The _𝑣𝑟_ curve exhibits a distinct "step-pulse" alternating pattern: _𝑣𝑟_ stabilizes at 0.8–1.0 m/s during straight segments and drops rapidly to near zero during turning segments. Correspondingly, the _𝑤𝑟_ curve fluctuates significantly during turning segments (peak value ±1.0 rad/s) and remains small during straight segments. Notably, _𝑣𝑟_ shows a peak of 1.5 m/s at around 120 s, corresponding to the high-speed forward phase when Run mode is activated. The inverse coupling relationship between _𝑣𝑟_ and _𝑤𝑟_ visually verifies the primary auto-steering control logic of forward and turning in the navigation system: the forward velocity is preferentially reduced during turning to ensure steering accuracy, while the forward efficiency is maximized during straight-line movement. 


**Figure 18:** Control commands(vr/wr). 

To further reveal the inherent structure of the forwardturn mutual exclusion relationship, Figure 19 plots the _𝑣𝑟_ - _𝑤𝑟_ phase diagram with target angle as the color mapping. The gray dashed line in the figure represents the speed-turn interlock boundary, which is determined by the parameters in the controller. Two distinct regions can be clearly observed in the figure: when the target angle is large (warm color, angle > 60°), the data points are concentrated in the region of low _𝑣𝑟_ and high | _𝑤𝑟_ | (marked as “Turn-dominant” in the figure), indicating that the robot prioritizes turning to align with the target direction; when the target angle is small (cool color, angle < 30°), the data points are concentrated in the high _𝑣𝑟_ and low | _𝑤𝑟_ | region (marked as “Forward-dominant” in the figure), indicating that the robot has basically aligned with the target and accelerates forward. The entire data distribution is enclosed by the interlock boundary, and the control commands are always within the physical safety envelope regardless of the gait mode. 

Page 8 of 11 

: _Preprint submitted to Elsevier_ 


**Figure 20:** Gait mode distribution along path. 


**Figure 21:** Torso orientation curve. 

**Figure 19:** vr-wr phase portrait. 

# **7. Discussion** 

## **6.3. Gait Switching and Posture Stability** 

Figure 20 shows the temporal switching of gait modes during the 240-second experiment in the form of a color band diagram. The robot remained in Walk mode throughout the 0–120 s period, conducting stable locomotion in the flat environment. Then, at approximately 120 s, as the operator specified a farther target point, the system automatically switched to Run mode (lasting about 5 s) for acceleration, and then returned to Walk mode. In the 160–180 s interval, the robot reached the stair area, and the system automatically switched to Stair mode to adapt to the step terrain, returning to Walk mode after passing the stairs. At the end of the experiment (around 235 s), the robot encountered stairs again and briefly entered Stair mode. The gait switching sequence throughout the experiment was highly consistent with terrain changes and target distances, and all switching was completed automatically by the navigation system, indicating that the multi-skill switching logic under the Tree Learning framework has good environmental adaptability in autonomous navigation scenarios. 

Figure 21 presents the posture stability data of the robot’s torso. The upper figure shows the time curves of roll and pitch angles. During the flat-ground walking phase, both roll and pitch angles were controlled within about ±2.5°, demonstrating high posture stability. In the stair interval (160–180 s), the Roll angle fluctuations increased to approximately ±(5–7)°, caused by periodic disturbances from the stair steps, but remained within a safe range without falls or severe instability. This further verifies the design concept of a unified state space shared by all skill models in the Tree Learning framework: different branch networks can achieve continuous transition of action commands at the moment of switching, ensuring posture robustness throughout autonomous navigation. 

## **7.1. Mechanism Effectiveness Analysis** 

The Tree Learning framework achieves both enhanced multi-skill expansion efficiency and high motion stability, primarily owing to the synergistic effect of its underlying design components. First, the parameter inheritance mechanism reuses the neural network weights embedded in the root skill (e.g., flat-ground walking). This approach of learning by building upon established foundations substantially reduces the blind exploration range in the high-dimensional state-action space, significantly lowering the exploration cost and sample complexity for new skills. Second, the feedforward action and reward shaping strategy provides targeted dense guidance for different branch skills, not only accelerating network convergence but also ensuring action reasonableness under physical constraints. Third, the multimodal action adaptation mechanism combining phase modulation and trajectory interpolation enables the framework to accommodate both periodic gaits and aperiodic large-range motions, substantially extending the system’s applicability boundary. 

## **7.2. Summary of Core Advantages** 

Compared with conventional reinforcement learningbased motion control approaches, the Tree Learning framework proposed in this paper demonstrates advantages as follows: 

(1) High training efficiency: Owing to hierarchical parameter reuse, the converged rewards of Tree Learning consistently surpass those of the multi-task baseline when expanding new skills. 

(2) Avoidance of catastrophic forgetting: Through the physically isolated tree-structured network storage topology, the system achieves decoupling of old and new skills, with a retention rate of 100% for existing fundamental skills, resolving the negative transfer problem in single-network multi-task learning. 

Page 9 of 11 

: _Preprint submitted to Elsevier_ 

(3) Broad scenario adaptability: The framework successfully covers a wide skill spectrum ranging from simple flatground locomotion to complex environments (e.g., stairs, tunnel) and highly dynamic interactive motion (e.g., ball kicking, jumping). 

(4) Practical interactivity: Through a lightweight global clock and state relay logic, the system supports smooth, ultra-low-latency dynamic skill switching under user commands, with no posture transients or fall instabilities observed. 

## **7.3. Limitations and Future Directions** 

Despite the promising results achieved in simulation, this study has certain limitations that point to directions for future work. On one hand, the current framework has been validated only in the Unity simulation environment, without fully accounting for the complexities of real motor dynamics, sensor noise, and contact friction—constituting an objective Sim-to-Real gap. In future work, we plan to add domain randomization and implicit state estimation techniques to pursue zero-shot transfer deployment to physical humanoid robots. On the other hand, long-period complex motions (e.g., dance) have not yet been addressed. The next step will involve developing automated motion retargeting and keyframe auto-extraction algorithms based on human video demonstrations, to further improve the construction efficiency of complex skills. 

# **CRediT authorship contribution statement** 

**Yifei Yan:** Methodology, Software, Writing - original draft, Visualization. **Linqi Ye:** Conceptualization, Supervision, Project administration, Funding acquisition, Writing - review & editing. 

# **Declaration of competing interest** 

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. 

# **References** 

- [1] Wu, J., Xin, G., Qi, C., Xue, Y., 2023. Learning robust and agile legged locomotion using adversarial motion priors. IEEE Robotics and Automation Letters 8, 4975–4982. doi:10.1109/LRA.2023.3290509. 

- [2] Zhu, S., Huang, R., Mou, L., et al., 2024. Robust robot walker: Learning agile locomotion over tiny traps. arXiv preprint arXiv:2409.07409 . 

- [3] Lee, J., Hwangbo, J., Wellhausen, L., et al., 2020. Learning quadrupedal locomotion over challenging terrain. Science Robotics 5, eabc5986. 

- [4] Ha, S., Lee, J., van de Panne, M., et al., 2025. Learning-based legged locomotion: State of the art and future perspectives. The International Journal of Robotics Research 44, 1396–1427. 

- [5] Liu, L.M., Tian, Y.T., Li, J.F., et al., 2011. Switch control of passive walking robot under variable road conditions. Control and Decision 26, 1203–1208. 

- [6] Xie, B., Chen, Y.L., Liu, X.L., et al., 2025. Overview of the intelligent robot training platform. Space Electronic Technology 22, 1–9. 

# **8. Conclusion** 

This paper addresses the prevalent pain points of low training efficiency and susceptibility to catastrophic forgetting in multi-skill learning for humanoid robots by proposing Tree Learning, a multi-skill continual learning framework. The framework innovatively adopts a root-branch hierarchical network architecture, achieving efficient expansion of 11 diverse motor skills for humanoid robots through prior parameter inheritance, task-level reward shaping, and multimodal action feedforward adaptation. Simulation experiments demonstrate that, compared with the simultaneous multi-task training baseline, Tree Learning not only improves the converged rewards for new skills but also achieves seamless human-robot interactive switching of cross-terrain, cross-modal action commands. This work fundamentally avoids the gradient conflicts arising from complex skill accumulation from a mechanistic perspective, providing an efficient system-level solution for continual learning of embodied intelligent agents. 

# **Acknowledgements** 

This work was supported by the Science and Technology Commission of Shanghai Municipality (24511103304). 

- [7] Gou, G.Z., Guo, M., 2025. Review of domestic humanoid robot development in 2024. Robot Technique and Application 9, 5–13. doi:10.3969/j.issn.1004-6437.2025.02.007. 

- [8] Liu, W.L., Li, B., Hou, L.D., et al., 2022. Review of quadruped robot research based on deep reinforcement learning. Journal of Qilu University of Technology 32, 67–74. 

- [9] Zhang, W.Y., Xia, D.W., Chang, G.Y., et al., 2025. A dual visionguided mobile robot control approach for multi-target path planning and intelligent pickup. Robotics and Autonomous Systems 190, 104993. 

- [10] Liao, Q., Truong, T.E., Huang, X., et al., 2025. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. arXiv preprint arXiv:2508.08241 . 

- [11] Xie, W., Han, J., Zheng, J., et al., 2025. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. arXiv preprint arXiv:2506.12851 . 

- [12] Han, J., Xie, W., Zheng, J., et al., 2025. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. arXiv preprint arXiv:2509.16638 . 

- [13] Zhang, Z., Guo, J., Chen, C., et al., 2025. Track any motions under any disturbances. arXiv preprint arXiv:2509.13833 . 

- [14] Obando-Ceron, J., Sokar, G., Willi, T., et al., 2024. Mixtures of experts unlock parameter scaling for deep rl. arXiv preprint arXiv:2402.08609 . 

- [15] Yang, C., Yuan, K., Zhu, Q., et al., 2020. Multi-expert learning of adaptive legged locomotion. Science Robotics 5, eabb2174. 

- [16] Huang, R., Zhu, S., Du, Y., et al., 2025. Moe-loco: Mixture of experts for multitask locomotion, in: 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 14218– 14225. 

- [17] Cheng, G., Dong, L., Cai, W., et al., 2023. Multi-task reinforcement learning with attention-based mixture of experts. IEEE Robotics and Automation Letters 8, 3812–3819. 

Page 10 of 11 

: _Preprint submitted to Elsevier_ 

- [18] Luo, Z., Yuan, Y., Wang, T., et al., 2025. Sonic: Supersizing motion tracking for natural humanoid whole-body control. arXiv preprint arXiv:2511.07820 . 

- [19] Peng, X.B., Abbeel, P., Levine, S., et al., 2018. Deepmimic: Exampleguided deep reinforcement learning of physics-based character skills. ACM Transactions on Graphics 37, 1–14. 

- [20] Li, Z., Peng, X.B., Abbeel, P., Levine, S., Berseth, G., Sreenath, K., 2024. Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control. arXiv preprint arXiv:2401.16889 . 

- [21] Zhang, L.J., Tang, L., Liu, L., 2025. Whole-body motion strategy intelligent generation method for multi-skilled humanoid robots. Aerospace Control and Application 51, 28–40. 

- [22] Zhang, X., Xiao, Z., Zhang, Q., et al., 2024. Synloco: Synthesizing central pattern generator and reinforcement learning for quadruped locomotion, in: 2024 IEEE 63rd Conference on Decision and Control (CDC), pp. 2640–2645. 

- [23] Bellegarda, G., Shafiee, M., Ijspeert, A.J., 2024. Visual cpg-rl: Learning central pattern generators for visually-guided quadruped locomotion, in: 2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 1420–1427. 

- [24] Chen, L., Cui, R., Yan, W., et al., 2024. Terrain-adaptive locomotion control for an underwater hexapod robot: Sensing leg-terrain interaction with proprioceptive sensors. IEEE Robotics & Automation Magazine 31, 41–52. 

- [25] Schulman, J., Wolski, F., Dhariwal, P., et al., 2017. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347 . 

Page 11 of 11 

: _Preprint submitted to Elsevier_ 

