---
title: "HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation"
date: "2026-02-06"
authors: "Zhanxiang Cao; Liyun Yan; Yang Zhang; Sirui Chen; Jianming Ma; Tianyue Zhan"
url: https://arxiv.org/abs/2602.06341
pdf: https://arxiv.org/pdf/2602.06341
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.06341)** / [論文ページ](https://arxiv.org/abs/2602.06341)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation 

Zhanxiang Cao<sup>1</sup><sup>_,_2</sup> , Liyun Yan<sup>1</sup><sup>_,_2</sup> , Yang Zhang<sup>1</sup> , Sirui Chen<sup>1</sup> , Jianming Ma<sup>1</sup><sup>_,_2</sup> , Tianyue Zhan<sup>1</sup><sup>_,_2</sup> , Shengcheng Fu<sup>3</sup><sup>_,_2</sup> , Yufei Jia<sup>4</sup> , Cewu Lu<sup>1</sup><sup>_,_2</sup> , Yue Gao<sup>1</sup><sup>_,_2</sup><sup>_,†_</sup> 1Shanghai Jiao Tong University 2Shanghai Innovation Institute 3Tongji University 4Tsinghua University 

> _†_ Corresponding author 

**_Abstract_ —Humanoid loco-manipulation requires executing precise manipulation tasks while maintaining dynamic stability amid base motion and impacts. Existing approaches typically formulate commands in body-centric frames, fail to inherently correct cumulative world-frame drift induced by legged locomotion. We reformulate the problem as world-frame end-effector tracking and propose HiWET, a hierarchical reinforcement learning framework that decouples global reasoning from dynamic execution. The high-level policy generates subgoals that jointly optimize endeffector accuracy and base positioning in the world frame, while the low-level policy executes these commands under stability constraints. We introduce a Kinematic Manifold Prior (KMP) that embeds the manipulation manifold into the action space via residual learning, reducing exploration dimensionality and mitigating kinematically invalid behaviors. Extensive simulation and ablation studies demonstrate that HiWET achieves precise and stable end-effector tracking in long-horizon world-frame tasks. We validate zero-shot sim-to-real transfer of the low-level policy on a physical humanoid, demonstrating stable locomotion under diverse manipulation commands. These results indicate that explicit world-frame reasoning combined with hierarchical control provides an effective and scalable solution for long-horizon humanoid loco-manipulation.** 


Fig. 1. **HiWET capabilities in simulation and real-world deployment.** (a)-(c) Whole-body redundancy exploitation for diverse reaching tasks (left: simulation, right: real robot): (a) lowest and farthest, (b) highest, (c) outermost in semi-squat posture. (d) Sim-to-sim transfer to MuJoCo with world-frame trajectory tracking (red circle: target, green: actual). (e)-(f) Real-world longexposure experiments: (e) square trajectory, (f) circular trajectory, where red curves are traced by an LED attached to the end-effector. 

## I. INTRODUCTION 

Recent advances in reinforcement learning (RL) and imitation learning have driven rapid progress in humanoid whole-body motion control [28, 7, 43, 33]. Motion retargeting addresses the embodiment gap between humans and robots, enabling expressive motion imitation while maintaining dynamic balance [11, 10, 13, 5, 15, 3, 40, 12]. Recent works further leverage diffusion models, large-scale motion datasets, and visual perception for more versatile whole-body control [41, 24, 23, 42, 46, 38, 34]. These results demonstrate that learning-based methods can produce stable, expressive whole-body behaviors for humanoid robots. 

Moving beyond motion imitation, command-driven locomanipulation frameworks enable task-level control through abstract interfaces [20, 2, 44]. These methods allow operators to specify end-effector poses or joint targets via motion optimization, teleoperation, or structured planners, providing interpretable geometric control with clear task semantics. Hierarchical architectures further decouple high-level planning from low-level motor control, employing either latent skill interfaces [45, 16] or explicit trajectory-level commands [13, 35, 

29, 19]. Combined with end-effector stabilization methods [21], these developments have significantly advanced the practical deployment of humanoid loco-manipulation systems. 

Despite this progress, fundamental challenges remain. Wholebody motion imitation optimizes joint-space errors rather than task-space precision, lacking theoretical guarantees for accurate end-effector tracking [1, 17] and typically requiring costly dense reference trajectories [27]. Meanwhile, most command-driven methods operate in body-centric frames, where cumulative base drift and high-frequency oscillations can significantly degrade end-effector precision in the world frame [22]. The tight coupling between upper and lower body dynamics further compounds this challenge: aggressive arm motions can destabilize the gait, while locomotion-induced impacts propagate to the end-effectors [8]. When task trajectories extend beyond the static reachable workspace, the robot must actively transport its base to maintain reachability—a coordination that body-centric formulations do not explicitly address [31]. We argue that formulating the task as _world-frame end-effector tracking_ exposes this geometric coupling, enabling 

the controller to actively compensate for base disturbances while reshaping the operational workspace through locomotion. 

To address these challenges, we propose HiWET, a hierarchical reinforcement learning framework that enables precise world-frame end-effector tracking through explicit upper-lower body coordination. The high-level _world-frame command policy_ reasons in global coordinates, generating structured subgoals—base velocity, body height, and local endeffector targets—to guide the robot toward task objectives while maintaining reachability. The low-level _whole-body tracking policy_ operates at high frequency, translating these subgoals into joint commands while ensuring dynamic stability. This decomposition separates _where to go_ (global planning) from _how to move_ (dynamic execution), allowing each policy to specialize in its respective objective. To accelerate learning and improve tracking precision, we introduce a Kinematic Manifold Prior (KMP) that provides kinematically consistent references for upper-body control, enabling the policy to learn residual corrections rather than absolute joint targets. 

Our main contributions are as follows: 

- We propose a **world-to-body hierarchical control scheme** that coordinates upper-body manipulation with lower-body locomotion through an explicit spatial interface, enabling world-frame consistency via active base transport and height adjustment. 

- We introduce an **efficient Kinematic Manifold Prior (KMP)** integrated within a residual action space, providing high-speed kinematic references that ground the policy in valid manipulation manifolds while preserving dynamic adaptability. 

- We perform **extensive validation on a physical humanoid platform** , demonstrating 12.4 mm world-frame tracking error in simulation and robust zero-shot sim-to-real transfer across diverse limb configurations. 

## II. RELATED WORKS 

## _A. Humanoid Whole-Body Motion Control_ 

Reinforcement learning and imitation learning have enabled humanoids to achieve expressive whole-body behaviors. The seminal work DeepMimic [28] demonstrated that RL can track motion capture references with physical realism, inspiring benchmarks such as Humanoid-Gym [7] and HumanoidBench [33]. Motion retargeting methods address the embodiment gap: H2O [11] and OmniH2O [10] enable realtime teleoperation, ExBody [5, 15] extends imitation to expressive upper-body motions, and SONIC [24] scales motion tracking with large-scale datasets. Generative approaches such as BeyondMimic [23] and MaskedManipulator [35] leverage diffusion models to synthesize versatile motions from sparse goals. 

Command-driven frameworks enable task-level control: AMO [20] employs motion optimization, HOMIE [2] uses isomorphic teleoperation, and HOVER [13] consolidates locomotion, standing, and manipulation into a unified policy. Hierarchical architectures separate planning from motor control: 

R<sup>2</sup> S<sup>2</sup> [45] and WholeBodyVLA [16] encode commands as latent skill codes, while FALCON [44] and VisualMimic [41] transmit trajectory-level commands with clearer geometric semantics. 

## _B. Spatial Consistency in Humanoid Loco-Manipulation_ 

Most existing methods reference commands to the robot base, assuming a stable coordinate frame [36, 37, 31]. Wheeled mobile manipulators such as Mobile ALOHA [6] largely maintain this assumption, achieving bimanual coordination via imitation on stable bases. However, legged humanoids must contend with cumulative drift and high-frequency oscillations during dynamic locomotion [22], compounded by tight upperlower body coupling [8]. DexMan [14] explores floating-base manipulation without explicitly modeling leg-arm coupling. FALCON [44] and RAMBO [4] improve tracking through force adaptation and hybrid model-based RL, but still operate in body-centric coordinates. 

In summary, imitation-based methods optimize joint-space errors rather than task-space precision [1] and require dense references [27], while command-driven methods operate in body-centric frames that cannot maintain world-frame consistency. HiWET addresses these limitations through worldframe end-effector tracking with an explicit Cartesian interface, enabling active workspace reshaping through locomotion while ensuring dynamic stability via a modular low-level policy. 

## III. PROBLEM FORMULATION 

We propose a hierarchical reinforcement learning (HRL) framework that decouples global spatial reasoning from dynamic execution. The overall architecture is illustrated in Fig. 2. The _world-frame command policy_ functions as a task planner, interpreting global end-effector targets and generating local subgoals—specifically base velocity, body height, and baserelative hand poses. The _whole-body tracking policy_ operates at a higher frequency to translate these subgoals into joint-space targets while ensuring physical feasibility and dynamic balance. By formulating this interplay as a semi-Markov decision process (Semi-MDP), the hierarchy effectively reconciles longhorizon manipulation objectives with instantaneous stability constraints. 

We model the humanoid control problem as a hierarchical reinforcement learning process 


where _S_ is the state space, _A_<sup>_H_</sup> and _A_<sup>_L_</sup> denote the high-level and low-level action spaces, _P_ is the transition dynamics, _R_ is the reward function, and _γ ∈_ (0 _,_ 1) is the discount factor. 

The hierarchy operates on two distinct timescales: the worldframe command policy _π_<sup>_H_</sup> runs every _K_ steps to update the subgoal command, while the whole-body tracking policy _π_<sup>_L_</sup> executes actions at every control step conditioned on the static high-level command. Both policies are optimized to maximize the expected discounted return _J_ = E[<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtrt_],</sup> where rewards are designed to balance global tracking precision with local dynamic stability. 


Fig. 2. **HiWET architecture and two-stage training procedure. Stage 1: Tracker** (blue): The tracking policy learns to follow base-relative end-effector commands. Commands are sampled from a mixture of uniform random sampling and an importance-sampled dataset filtered by IK error and manipulability. A pretrained KMP provides upper-body kinematic references, which are refined by residual actions from the Actor. The History Encoder extracts temporal context, while the State Estimator reconstructs privileged information via an auxiliary estimation loss. **Stage 2: Commander** (orange): The command policy translates world-frame end-effector (EEF) targets (EEF Cmd. W.) and base pose into base-frame subgoals (Base Cmd. B. and EEF Cmd. B.). 

## IV. WHOLE-BODY TRACKING POLICY 

The whole-body tracking policy translates high-level motion commands into joint-space targets for stable whole-body execution. It operates at high frequency and interfaces directly with the PD controller. The humanoid is decomposed into an upper-body subsystem (arms and waist) and a lower-body subsystem (legs). This policy serves as a **standalone wholebody tracker** with a general-purpose command interface, capable of following arbitrary base velocity and end-effector subgoals independently of the high-level task planner. 

## _A. State and Action Representation_ 

_1) State Space:_ The whole-body tracking policy is conditioned on both the humanoid proprioceptive state _st_ and the structured command **u** _t_ received from the world-frame command policy. The observation at time _t_ is defined as 


where **_ω_** _t ∈_ R<sup>3</sup> is the base angular velocity, **g** _t ∈_ R<sup>3</sup> is the gravity projection in the base frame, **q** _t_ and **q** ˙ _t_ denote joint positions and velocities, and **a**<sup>_L_</sup> _t−_ 1<sup>isthepreviousaction.</sup> 

The command **u** _t_ transmits high-level spatial objectives to the low-level policy: 


where **v** _b_<sup>_des_</sup> = ( _vx, vy, ωz_ ) is the desired base velocity, _h_<sup>_des_</sup> is the target body height,<sup>_b_</sup> **T**<sup>_des_</sup> _{·}_<sup>denotethedesiredend-effector</sup> poses, and _αt_ is the waist regularization weight (uniformly sampled from [0 _._ 1 _,_ 10] during training). We use the superscript _{·}_<sup>_des_</sup> to distinguish these local subgoals from global worldframe targets. 

_2) Hybrid Action Space:_ Given the proprioceptive observation _st_ and the command **u** _t_ , the policy outputs joint position targets for all actuated joints: 


where **q**<sup>_des_</sup> _t,up_<sup>denotesthedesiredjointpositionsoftheupper</sup> body and **q**<sup>_des_</sup> _t,low_<sup>denotesthoseofthelowerbody.</sup> 

Instead of learning a monolithic policy, we adopt a hybrid action space that leverages kinematic structure. For the upper body, the policy predicts a residual correction ∆ **q** _t,up_ which is added to the KMP reference **q** ˆ _t,up_ to form the final command: 


This residual formulation enables the controller to make subtle dynamic adjustments for end-effector stability and accuracy while remaining within the valid manipulation manifold. Conversely, the lower body is controlled via absolute joint targets **q**<sup>_des_</sup> _t,low_<sup>tomaintaindirectauthorityovergaitgeneration</sup> and base propulsion. 

## _B. Network Architecture Overview_ 

The whole-body tracking policy employs a modular network architecture comprising three key components designed to address the challenges of partial observability and kinematic consistency (see Stage 1: Tracker in Fig. 2). 

To ensure accurate end-effector tracking during motion and to provide a strong reference for learning, we introduce the Kinematic Manifold Prior (KMP) for the upper body. The KMP predicts a kinematically consistent joint configuration given desired end-effector poses and a waist motion preference. The input to the KMP is defined as 


where<sup>_b_</sup> **T**<sup>_des_</sup> _{·}_<sup>arethecommandedend-effectorposes,and</sup> _αt ∈_ [0 _._ 1 _,_ 10] is a scalar waist regularization weight (the fixed weight for other upper-body joints is 0 _._ 2). This parameter serves as a hierarchical interface that modulates torso engagement. Since humanoid stability is highly sensitive to the Center of Mass (CoM) position, explicitly allowing the global planner to control waist motion enables the framework to trade off between reachability and balance; lower values of _αt_ encourage the KMP to utilize waist redundancy to extend the effective workspace, while larger values prioritize a stable CoM to maintain dynamic balance during locomotion. The KMP produces a reference joint configuration for the upper body, 


where _fKMP_ is a neural approximation of the kinematic mapping for the arms and the waist. The KMP is pretrained offline and frozen during policy optimization, enabling the policy to learn residual corrections rather than absolute joint targets. 

_1) History Encoder:_ To improve robustness under partial observability, we construct a history buffer of length _H_ = 5 containing tuples ( _st,_ **u** _t_ ). The History Encoder (a CNN) processes this buffer _Ht_ = _{_ ( _st−i,_ **u** _t−i_ ) _}_<sup>_H_</sup> _i_ =0<sup>_−_1</sup> and outputs a latent representation **e** _t_ encoding temporal dependencies. _2) State Estimator:_ The State Estimator (also a CNN) infers privileged state variables from the observation history. It predicts base linear velocity and end-effector poses _b_ **T** _L, b_ **T** _R_ —quantities essential for accurate tracking but not directly accessible from onboard sensors during deployment. The estimator is trained jointly with the policy using a mean squared error loss. 

_3) Actor and Critic Inputs:_ The final input to the actor network is formed by concatenating the raw observation, the command, the privileged estimates from the State Estimator, the latent embedding from the History Encoder, and the kinematic reference from the frozen KMP: 


The critic is trained with access to full privileged information to reduce variance in value estimation. Its input is defined as 


where **p** _t_ includes the true base linear velocity and end-effector poses<sup>_b_</sup> **T** _L,_<sup>_b_</sup> **T** _R_ , and **h** _t_ denotes terrain elevation measurements from the height map sensor. Both actor and critic are optimized using Proximal Policy Optimization (PPO) [32, 30]. 

To ensure that the policy focuses on functionally relevant and reachable configurations, we construct a prioritized endeffector command dataset. Two metrics are used to curate this dataset. First, the inverse kinematics reconstruction error is employed to prune unreachable poses for which the solver fails to converge. Second, the manipulability index is used to weight sampling probability, favoring comfortable configurations that enable high-dexterity motion. 

To preserve coverage of the full command space, the actual command fed into the policy during training is drawn from a mixture distribution, 


where _β ∈_ [0 _,_ 1] is the mixing weight, _puniform_ samples uniformly from the full Cartesian volume, and _pprior_ samples from the curated dataset with added small perturbations. This mixture ensures that the policy observes both realistic commands and boundary cases, improving robustness without sacrificing feasibility. 

## _D. Kinematic Manifold Prior Learning_ 

_1) Dataset Generation:_ Training data for the KMP are generated by solving constrained optimization-based inverse kinematics problems using PyRoki [18]. For each sampled end-effector command, an optimization problem is constructed to minimize Cartesian pose errors subject to joint limits and a regularization term on waist motion weighted by _α_ , which is uniformly sampled from [0 _._ 1 _,_ 10]. This enables the prior to capture a spectrum of limb configurations ranging from rigid-torso reaching to whole-body lunges. Approximately ten million samples are generated. 

The initial end-effector command space is defined inside two symmetric Cartesian volumes around the torso center with full orientation coverage over the _SO_ (3) manifold. However, not all commands in this space are kinematically feasible. To curate the dataset, we apply importance sampling based on two metrics: the inverse kinematics reconstruction error, which prunes unreachable poses, and the manipulability index, which favors configurations that admit dexterous motion. Specifically, fivefold oversampling is performed and filtered according to these criteria as detailed in the appendix. 

_2) Network Architecture:_ The KMP adopts a symmetric encoder-decoder architecture with residual connections. It is based on a ResNet backbone [9] and incorporates layer normalization, dropout, and GELU activations to ensure stable training and generalization. 

## _C. Command Importance Sampling for Policy Learning_ 

Uniform sampling in the Cartesian command space of the end-effectors leads to a significant proportion of kinematically infeasible or ill-conditioned targets, which typically lie near workspace boundaries and suffer from poor manipulability. Training directly on such distributions degrades learning efficiency and stability. To mitigate this, we curate a dataset using importance sampling (see top-left of Fig. 2). 

## _E. Reward Formulation_ 

The reward function is designed to encourage accurate command tracking, stable locomotion, and precise manipulation, while preserving smooth and physically consistent motions. In addition to standard tracking terms for base linear velocity, angular velocity, body height, and end-effector poses, several task-specific shaping rewards are introduced. 

_1) KMP Reference Tracking:_ To exploit the kinematic prior provided by the KMP, we include a reward that encourages the executed upper-body configuration to stay close to the reference. Let **q** ˆ _t,up_ denote the reference joint configuration from the KMP and **q** _t,up_ denote the current upper-body joint positions. The tracking error is defined as 


where _σkmp_ controls the sensitivity. A time-dependent scaling factor is applied after command resampling to avoid overly constraining early transient responses. 

_2) Base Height Tracking with Knee Awareness:_ To stabilize standing and squatting, we introduce a base height tracking term with asymmetric knee-aware weighting. Let _ht_ be the measured base height and _h_<sup>_des_</sup> _t_ the commanded height. The height error is weighted by knee joint margins: when above target, by flexion margin; when below, by extension margin: 


where _w_ ¯ _knee_<sup>_flex_and</sup><sup>_w_¯</sup> _knee_<sup>_ext_aretheaveragemarginsforknee</sup> flexion and extension, respectively. This term is activated only under zero velocity conditions to avoid interference with dynamic locomotion. 

Additional regularization terms penalize excessive joint velocity, action rate, and torque variation to ensure smooth and hardware-friendly motions. The complete reward formulation and weighting is provided in the appendix. 

## V. WORLD-FRAME COMMAND POLICY 

The world-frame command policy _π_<sup>_H_</sup> functions as a global task planner, translating world-frame end-effector targets into dynamically feasible whole-body commands (see Stage 2: Commander in Fig. 2). It reasons over the coupled nature of locomotion and manipulation, effectively enlarging the robot’s operational workspace through active base transport. During this training stage, the whole-body tracking policy from Stage 1 is frozen. 

## _A. State and Command Representation_ 

_1) Observation and Task Command:_ The world-frame command policy observes the proprioceptive state alongside global information and the task-level command **c** _t_ . The observation is defined as 


where<sup>_w_</sup> **T**<sup>_t_</sup> _b_<sup>_∈SE_(3)denotesthebaseposeintheworldframe.</sup> The task command **c** _t_ is defined as 


where<sup>_w_</sup> **T**<sup>_∗_</sup> _{·}_<sup>_∈SE_(3)specifythedesiredend-effectorposes</sup> in the absolute world frame, and **m** _t ∈{_ [1 _,_ 0] _,_ [0 _,_ 1] _,_ [1 _,_ 1] _}_ is a binary mask that indicates which end-effector targets are 

active, enabling compatibility with both unilateral and bilateral manipulation tasks. 

We employ an asymmetric actor-critic architecture: while the actor observes the above state, the critic is augmented with privileged information: 


where **v** _b_<sup>_w_isthebaselinearvelocityand</sup><sup>_w_</sup><sup>**T**</sup><sup>_t_</sup> _{·}_<sup>arethecurrent</sup> end-effector poses in the world frame. The policy is optimized using PPO [32, 30]. 

_2) Action Space:_ The world-frame command policy outputs a structured motion command that serves as the input to the whole-body tracking policy: 


This abstraction allows the policy to focus on geometric consistency and reachability while delegating dynamic stability and contact management to the whole-body tracking policy. The inclusion of _αt_ in the action space enables the high-level policy to actively regulate the robot’s posture and CoM stability based on the global task context and locomotion state. 

## _B. Spatial Curriculum Strategy_ 

Training the world-frame command policy directly on large workspace ranges is challenging, as distant targets require long-horizon locomotion that complicates credit assignment. We adopt a curriculum learning strategy that progressively expands the world-frame command range based on tracking performance. 

Initially, world-frame targets<sup>_w_</sup> **T**<sup>_∗_</sup> _{·}_<sup>aresampledwithina</sup> small neighborhood around the robot’s current base position. As training progresses, we monitor the end-effector tracking error _eee_ = _∥_<sup>_w_</sup> **T** _{·} −_<sup>_w_</sup> **T**<sup>_∗_</sup> _{·}_<sup>_∥_andexpandthesamplingrange</sup> when the error falls below a threshold. Specifically, the planar command range _R_ is updated as: 


where ∆ _R_ is the range increment and _ϵth_ is the error threshold. This curriculum ensures that the policy masters local coordination before tackling long-range workspace transport. 

## _C. Reward Formulation_ 

The high-level reward function is designed to reconcile absolute tracking precision with optimal base positioning. 

- **Workspace Optimization** : To maintain high manipulability, we penalize the planar distance between the robot base and the active end-effector targets. We further reward the alignment of both the base heading and the commanded velocity vector **v** _b_<sup>_des_</sup> with the vector pointing toward the target center, ensuring the policy actively “steers” the body to reshape the available workspace. 

- **Precise End-effector Tracking** : Direct rewards are applied to minimize the pose error between<sup>_w_</sup> **T** _{·}_ and _w_ **T** _∗{·}_<sup>toenforceglobalspatialconsistency.</sup> 

- **Stability and Regularization** : To ensure hardware compatibility, we penalize action rates and high-frequency endeffector jitter. Additionally, when an arm is inactive (as indicated by **m** _t_ ), the policy is penalized for commanding deviations from a default neutral pose to prevent taskirrelevant limb drift. 

A detailed description of reward components and weighting is provided in the appendix. Through this hierarchical formulation, the world-frame command policy learns to coordinate locomotion and manipulation in the world frame, while delegating joint-space realization to the whole-body tracking policy. 

## VI. EXPERIMENTS AND RESULTS 

The experiments aim to answer the following key questions. 

- 1) How do the constituent components of the whole-body tracking policy—kinematic prior, privileged estimation, and importance sampling—contribute to command tracking precision and stability? 

- 2) How does the world-frame command policy achieve spatial consistency and base positioning accuracy in longhorizon trajectory tracking tasks? 

- 3) How does the proposed KMP compare to optimizationbased inverse kinematics solvers in terms of inference efficiency and reconstruction accuracy? 

- 4) Can the whole-body tracking policy successfully transfer to real hardware without additional fine-tuning? 

## _A. Experimental Setup_ 

Our experimental platform is the Unitree G1 humanoid robot with 29 degrees of freedom (12 for legs, 14 for dual arms, and 3 for waist). All policies are trained in Isaac Lab [26] and deployed via zero-shot sim-to-real transfer. Further details are provided in the Appendix. 

TABLE I 

COMMAND TRACKING PERFORMANCE COMPARISON 

|Method|Lin. Vel. Error<br>(m/s)|Ang. Vel. Error<br>(rad/s)|Height Error<br>(m)|EE Pos. Error<br>(mm)|
|---|---|---|---|---|
|HiWET|0.157 _±_ 0.003|0.461 _±_ 0.006|0.018 _±_ 0.012|12.4 _±_ 2.4|
|HiWET w/o IS|0.165 _±_ 0.005|0.472 _±_ 0.006|0.018 _±_ 0.014|16.1 _±_ 5.3|
|HiWET w/o State Est.|0.169 _±_ 0.003|0.459 _±_ 0.004|0.018 _±_ 0.016|23.0 _±_ 7.2|
|HiWET w/o KMP|0.149 _±_ 0.004|0.423 _±_ 0.005|0.015 _±_ 0.010|25.2 _±_ 12.8|
|HOMIE [2]|0.194 _±_ 0.003|0.451 _±_ 0.006|0.022 _±_ 0.019|-|


_1) Comparison with Baselines:_ HiWET outperforms the HOMIE baseline, reducing base linear velocity RMSE by _∼_ 20%. Note that HOMIE receives joint position commands rather than end-effector poses, precluding direct end-effector comparison. Our hierarchical formulation exposes locomotionmanipulation coupling, enabling more effective coordination while maintaining superior height consistency. 

_2) Ablation Studies and Precision Improvements:_ The ablation results highlight the critical contribution of each constituent component to the precision and robustness of bimanual tracking: 

- **HiWET w/o KMP** : Removing the KMP reference causes the most significant drop—hand error doubles (25.2 mm) with 5 _×_ higher variance—confirming that learning Cartesian tasks without kinematic guidance is significantly more challenging. 

- **HiWET w/o State Est.** : Without the state estimator, tracking degrades by nearly 10 mm, indicating that accurate end-effector feedback is essential for compensating locomotion-induced oscillations. 

- **HiWET w/o IS** : Comparison with uniform sampling shows that focusing training on functional workspace regions yields more consistent bimanual coordination. 

Additional ablation studies on reward components, including the knee-aware height tracking term, are provided in the Appendix. Overall, the full HiWET framework achieves the highest precision (12.4 mm hand error) while maintaining the lowest variance, demonstrating its robustness as a general-purpose loco-manipulation tracker. 


Fig. 3. **Tracking success rate and mean position error across diverse geometric trajectories.** HiWET demonstrates improved performance and consistency compared to its ablated versions (w/ Fixed _α_ , w/o State Est., w/o KMP), particularly in complex tasks like tracing stars and hearts. 

## _B. Low-Level Tracking Performance_ 

We evaluate the tracking performance of the low-level policy across various whole-body commands, measuring _base linear velocity error_ , _angular velocity error_ , _body height error_ , and _hand Cartesian error_ . Commands are uniformly sampled within: linear velocity _v ∈_ [ _−_ 1 _,_ 1] m/s, angular velocity _ωz ∈_ [ _−_ 3 _,_ 3] rad/s, body height _h ∈_ [0 _._ 3 _,_ 0 _._ 78] m, and end-effector poses within the maximal reachable Cartesian volume. We compare against the state-of-the-art framework HOMIE [2] and several ablation variants. The quantitative results are summarized in Table I. 

## _C. World-Frame Navigation and Long-Horizon Tracking_ 

_1) Trajectory Tracking Evaluation:_ We evaluate the capability of the high-level policy to perform spatially extended loco-manipulation tasks defined in absolute world coordinates, measuring _tracking success rate_ and _mean end-effector position error_ . Geometric trajectories serve as standardized benchmarks to evaluate the controller’s geometric precision and robustness across diverse motion profiles (e.g., sharp turns, velocity changes, symmetric/asymmetric movements). Five distinct geometric trajectories—star, heart, circle, spiral, and 

rectangle—are randomly initialized at global positions within a range of _±_ 5 m in both _x_ and _y_ axes relative to the robot’s starting location. This requires the robot to first navigate to the target region and then execute precise end-effector tracking while maintaining dynamic stability. 

A trial is considered successful if the average end-effector tracking error remains below 20 mm throughout the trajectory execution. This criterion evaluates both the nav-manipulation coordination of the high-level policy and the disturbance rejection of the low-level policy. 


Fig. 4. **Qualitative comparison of 3D world-frame trajectory tracking for heart and star shapes.** The color gradient indicates the instantaneous Cartesian position error (blue: _<_ 2 mm, red: _>_ 20 mm). HiWET (first column) maintains high spatial consistency, while fixing _α_ = 1 _._ 0 ( _w/ Fixed α_ ), removing privileged estimation ( _w/o State Est._ ), or removing the kinematic prior ( _w/o KMP_ ) leads to varying degrees of deviation and oscillatory patterns. Additional geometric trajectories (circle, spiral, rectangle) are provided in the Appendix. 

As illustrated in Fig. 3, HiWET achieves high success rates and low tracking errors across all geometric patterns. The qualitative comparison in Fig. 4 highlights heart and star trajectories, which require sharp changes in direction and coordinated end-effector movement. HiWET (left column) consistently maintains errors below 5 mm, while the ablated variants exhibit significant performance degradation. Specifically, the variant without the kinematic prior ( _w/o KMP_ ) shows severe trajectory distortions, as the high-level commands often drive the arms into kinematically ill-conditioned regions. The removal of the privileged estimator ( _w/o State Est._ ) leads to increased oscillations and tracking errors, highlighting the necessity of absolute state feedback for long-horizon spatial consistency. The variant with fixed _α_ = 1 _._ 0 ( _w/ Fixed α_ ) exhibits degraded performance in tasks requiring large reaching motions, as the policy cannot exploit waist redundancy to control the CoM, thereby lacking the ability to dynamically trade off between reachability and stability. Results for additional geometric trajectories (circle, spiral, rectangle) are provided in the Appendix. 

_2) Base Mobility Assessment:_ To isolate the robot’s navigation performance, we evaluate its ability to reposition its support base in response to task-space requirements. We initialize targets in eight cardinal and ordinal directions around the robot at a distance of 5 m. Figure 5 (left) illustrates the top- 


Fig. 5. **Analysis of base mobility and positioning precision.** (Left) Top-view trajectories for 8-directional base repositioning tasks. (Right) Evaluation of final base positioning error in the _xy_ -plane at the target location. HiWET provides the most stable trajectories and the highest positioning accuracy among all variants (w/ Fixed _α_ , w/o State Est., w/o KMP). 

view trajectories of the robot base for HiWET and its ablated variants. 

HiWET exhibits the most direct and stable paths toward the targets, demonstrating efficient whole-body coordination where locomotion is actively guided by the global task objective. In contrast, variants lacking high-fidelity feedback ( _w/o State Est._ ), kinematic priors ( _w/o KMP_ ), or adaptive _α_ modulation ( _w/ Fixed α_ ) show oscillations or “weaving” behaviors, as the high-level policy struggles to reconcile conflicting base and arm objectives. 

We further quantify the positioning precision by measuring the final distance between the robot base and the target starting point in the _xy_ -plane upon task completion. As shown in Fig. 5 (right), HiWET achieves the lowest mean error (0.101 m) and significantly less variance than other methods. This high positioning accuracy is a direct consequence of our active whole-body coordination strategy, which enables the policy to treat the base as an active degree of freedom for workspace optimization rather than an independent mobile platform. 

## _D. Kinematic Manifold Prior Benchmarking_ 

To evaluate the proposed kinematic prior, we benchmark the performance of the KMP against an optimization-based solver, PyRoki [18], across two primary metrics: _inference latency_ for efficiency and _Cartesian position/orientation error_ for reconstruction accuracy. We investigate two architectural variants: **KMP-S** , a lightweight 4-layer ResNet with smaller hidden dimensions, and **KMP-L** , a deeper 5-layer ResNet with larger hidden dimensions. Furthermore, we examine the impact of training distributions by comparing models trained on our importance-sampled (IS) dataset against those trained on a uniform Cartesian cube (w/o IS) with an equivalent number of samples. 

_1) Inference Efficiency:_ As shown in Fig. 6(a)-(b), the KMP variants achieve significant computational speedups. Compared to the PyRoki solver configured with 5 maximum iterations, KMP-L exhibits over 5 _×_ speedup at a single-sample inference level. This performance gap widens drastically under parallelized execution; at a batch size of 4000, KMP-L maintains 


Fig. 6. **Performance comparison between the proposed KMP variants and the optimization-based PyRoki solver.** (a)-(b) show that KMP variants achieve orders of magnitude speedup in inference latency, which is critical for real-time hierarchical control. (c)-(d) demonstrate that while optimizationbased methods are near-exact, our KMP-L model trained with importance sampling (IS) provides sufficiently high precision for dual-arm coordination, serving as an efficient kinematic prior. 

millisecond-level latency. This efficiency enables seamless integration into the reinforcement learning loop, providing highfrequency kinematic references without imposing a bottleneck on training throughput. 

_2) Reconstruction Accuracy:_ We evaluate the precision of the kinematic mapping using a test set derived from AMASS motion capture data [25] retargeted to the G1 humanoid, which captures the natural spatial distribution of human end-effector usage. Figures 6(c) and (d) summarize the Cartesian position and orientation errors. While PyRoki remains the most precise due to its iterative nature, KMP-L achieves a median position error below 15 mm and orientation error below 5 degrees. Notably, the KMP-L models trained with importance sampling (IS) significantly outperform their uniform counterparts (KMPL w/o IS), demonstrating that focusing on functional and manipulable regions of the workspace is essential for highfidelity bimanual coordination. These results validate that KMPL provides a sufficiently accurate and highly efficient kinematic prior for whole-body control. 

## _E. Real-world Hardware Experiments_ 

_1) Whole-body Tracking Policy:_ To evaluate the transferability and robustness of the proposed framework, we deploy the low-level tracking policy on the physical Unitree G1 robot. The policy is trained entirely in simulation and deployed via zero-shot transfer to the robot’s onboard computer, operating at 50 Hz. 

As illustrated in Fig. 7, the robot demonstrates stable locomotion under varying and asymmetric limb configurations. In Fig. 7(a), the robot maintains a steady walking gait while the right arm is commanded to a high reaching pose. In Fig. 7(b), the robot successfully navigates while the right hand dynamically traces a circular trajectory, showcasing the 


Fig. 7. **Snapshots of real-world deployment on the Unitree G1 robot.** The low-level policy maintains stable locomotion while tracking diverse arm motions: (a) unilateral right-arm reaching, and (b) dynamic upper-body motion with the right hand tracing a circular trajectory (magenta curve indicates the right end-effector path). The system successfully rejects dynamic disturbances caused by rapid limb movements. 

policy’s ability to handle rapid upper-body motions that induce significant center of mass (CoM) shifts and dynamic coupling between the limbs. These experiments confirm that the low-level policy effectively manages the trade-off between task-space tracking and dynamic balance in real-world scenarios. 

TABLE II 

### **REAL-WORLD END-EFFECTOR TRACKING ERRORS FOR CIRCLE AND SQUARE TRAJECTORY TASKS.** 

|Method||Circle RMSE (m)|Square RMSE (m)|
|---|---|---|---|
|HiWET||0.012 _±_ 0.005|0.015 _±_ 0.007|
|HiWET|w/ Fixed _α_|0.018 _±_ 0.008|0.019 _±_ 0.009|
|HiWET|w/o State Est.|0.024 _±_ 0.011|0.028 _±_ 0.011|
|HiWET|w/o KMP|0.032 _±_ 0.013|0.039 _±_ 0.015|


_2) World-Frame Command Policy:_ To enable world-frame tracking, global pose is estimated using a head-mounted Livox Mid-360 LiDAR and IMU via Fast-LIO2 [39], with base position updated at 10 Hz through forward kinematics. In the circle and square trajectory tasks (Fig. 1(e,f)), we compare HiWET against ablated variants over 10 repetitions. As shown in Table II, HiWET achieves the lowest tracking errors (12 mm for circles, 15 mm for squares). The fixed _α_ = 1 _._ 0 variant shows moderate degradation due to its inability to modulate torso engagement, while removing the state estimator or KMP leads to significantly larger errors. 

## VII. CONCLUSION AND LIMITATIONS 

We presented HiWET, a hierarchical reinforcement learning framework for whole-body loco-manipulation. By decoupling global task reasoning from dynamic execution, our approach effectively resolves the spatial and dynamic coupling between legged locomotion and precise manipulation. The high-level planner operates in a world coordinate frame to ensure longhorizon consistency, while the low-level policy augmented by 

an efficient KMP provides the necessary dynamic stabilization. Extensive simulation and real-world experiments validate the effectiveness of the proposed framework, achieving 12.4 mm mean tracking error in simulation and robust zero-shot sim-toreal transfer. 

The current framework has **limitations** : (1) world-frame tracking precision is bounded by LiDAR-based localization accuracy; (2) evaluated trajectories are relatively small in scale; (3) bimanual global tracking depends on target feasibility, and high-level experiments involve only single-arm tracking; (4) contact-rich manipulation (e.g., grasping) remains unexplored. Future work will integrate visual perception and force control for dexterous, contact-aware manipulation. 

## REFERENCES 

- [1] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [2] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid locomanipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [3] Zhanxiang Cao, Yang Zhang, Buqing Nie, Huangxuan Lin, Haoyang Li, and Yue Gao. Learning motion skills with adaptive assistive curriculum force in humanoid robots. _arXiv preprint arXiv:2506.23125_ , 2025. 

- [4] Jin Cheng, Dongho Kang, Gabriele Fadini, Guanya Shi, and Stelian Coros. Rambo: Rl-augmented model-based whole-body control for loco-manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [5] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive wholebody control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 

- [6] Zipeng Fu, Tony Z Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. 

- [7] Xinyang Gu, Yen-Jen Wang, and Jianyu Chen. Humanoidgym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer. _arXiv preprint arXiv:2404.05695_ , 2024. 

- [8] Zhaoyuan Gu, Junheng Li, Wenlan Shen, Wenhao Yu, Zhaoming Xie, Stephen McCrory, Xianyi Cheng, Abdulaziz Shamsah, Robert Griffin, C Karen Liu, et al. Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. _arXiv preprint arXiv:2501.02116_ , 2025. 

- [9] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 770–778, 2016. 

- [10] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to- 

humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [11] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning humanto-humanoid real-time whole-body teleoperation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8944–8951. IEEE, 2024. 

- [12] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid wholebody skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [13] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, et al. Hover: Versatile neural wholebody controller for humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9989–9996. IEEE, 2025. 

- [14] Jhen Hsieh, Kuan-Hsun Tu, Kuo-Han Hung, and TsungWei Ke. Dexman: Learning bimanual dexterous manipulation from human and generated videos. _arXiv preprint arXiv:2510.08475_ , 2025. 

- [15] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- [16] Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, Chuang Wang, Zhihui Peng, et al. Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control. _arXiv preprint arXiv:2512.11047_ , 2025. 

- [17] Xisheng Jiang, Baolei Wu, Simin Li, Yongtong Zhu, Guoxiang Liang, Ye Yuan, Qingdu Li, and Jianwei Zhang. Multi-humanoid robot arm motion imitation and collaboration based on improved retargeting. _Biomimetics_ , 10(3):190, 2025. 

- [18] Chung Min Kim, Brent Yi, Hongsuk Choi, Yi Ma, Ken Goldberg, and Angjoo Kanazawa. Pyroki: A modular toolkit for robot kinematic optimization. _arXiv preprint arXiv:2505.03728_ , 2025. 

- [19] Yuxuan Kuang, Haoran Geng, Amine Elhafsi, Tan-Dzung Do, Pieter Abbeel, Jitendra Malik, Marco Pavone, and Yue Wang. Skillblender: Towards versatile humanoid whole-body loco-manipulation via skill blending. _arXiv preprint arXiv:2506.09366_ , 2025. 

- [20] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Ri-Zhao Qiu, and Xiaolong Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _arXiv preprint arXiv:2505.03738_ , 2025. 

- [21] Yitang Li, Yuanhang Zhang, Wenli Xiao, Chaoyi Pan, Haoyang Weng, Guanqi He, Tairan He, and Guanya Shi. Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control. In _RSS 2025 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ , 2025. 

- [22] Yixuan Li, Yutang Lin, Jieming Cui, Tengyu Liu, Wei 

Liang, Yixin Zhu, and Siyuan Huang. Clone: Closedloop whole-body humanoid teleoperation for long-horizon tasks. _arXiv preprint arXiv:2506.08931_ , 2025. 

- [23] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [24] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castaneda, Zi-Ang Cao, Jiefeng Li, David˜ Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [25] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [26] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Munoz,˜ Xinjie Yao, Rene´ Zurbrugg,¨ Nikita Rudin, et al. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

- [27] Chaoyi Pan, Changhao Wang, Haozhi Qi, Zixi Liu, Homanga Bharadhwaj, Akash Sharma, Tingfan Wu, Guanya Shi, Jitendra Malik, and Francois Hogan. Spider: Scalable physics-informed dexterous retargeting. _arXiv preprint arXiv:2511.09484_ , 2025. 

- [28] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [29] Tifanny Portela, Andrei Cramariuc, Mayank Mittal, and Marco Hutter. Whole-body end-effector pose tracking. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11205–11211. IEEE, 2025. 

- [30] Nikita Rudin, David Hoeller, Philipp Reist, and Marco Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In _Conference on robot learning_ , pages 91–100. PMLR, 2022. 

- [31] Thushara Sandakalum and Marcelo H Ang Jr. Motion planning for mobile manipulators—a systematic review. _Machines_ , 10(2):97, 2022. 

- [32] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [33] Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _arXiv preprint arXiv:2403.10506_ , 2024. 

- [34] Yiyang Shao, Xiaoyu Huang, Bike Zhang, Qiayuan Liao, Yuman Gao, Yufeng Chi, Zhongyu Li, Sophia Shao, and Koushil Sreenath. Langwbc: Language-directed humanoid whole-body control via end-to-end learning. _arXiv preprint arXiv:2504.21738_ , 2025. 

- [35] Chen Tessler, Yifeng Jiang, Erwin Coumans, Zhengyi Luo, 

Xue Bin Peng, and Gal Chechik. Maskedmanipulator: Versatile whole-body control for loco-manipulation. In _Proceedings of the SIGGRAPH Asia 2025 Conference Papers_ , pages 1–11, 2025. 

- [36] Chenzheng Wang, Qiang Huang, Xuechao Chen, Zeyu Zhang, and Jing Shi. Robust visuomotor control for humanoid loco-manipulation using hybrid reinforcement learning. _Biomimetics_ , 10(7):469, 2025. 

- [37] Zifan Wang, Yufei Jia, Lu Shi, Haoyu Wang, Haizhou Zhao, Xueyang Li, Jinni Zhou, Jun Ma, and Guyue Zhou. Arm-constrained curriculum learning for locomanipulation of a wheel-legged robot. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 10770–10776. IEEE, 2024. 

- [38] Zifan Wang, Teli Ma, Yufei Jia, Xun Yang, Jiaming Zhou, Wenlong Ouyang, Qiang Zhang, and Junwei Liang. Omniperception: Omnidirectional collision avoidance for legged locomotion in dynamic environments. _arXiv preprint arXiv:2505.19214_ , 2025. 

- [39] Wei Xu, Yixi Cai, Dongjiao He, Jiarong Lin, and Fu Zhang. Fast-lio2: Fast direct lidar-inertial odometry. _IEEE Transactions on Robotics_ , 38(4):2053–2073, 2022. 

- [40] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [41] Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C Karen Liu, and Jiajun Wu. Visualmimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [42] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [43] Yang Zhang, Zhanxiang Cao, Buqing Nie, Haoyang Li, Zhong Jiangwei, Qiao Sun, Xiaoyi Hu, Xiaokang Yang, and Yue Gao. Keep on going: Learning robust humanoid motion skills via selective adversarial training. _arXiv preprint arXiv:2507.08303_ , 2025. 

- [44] Yuanhang Zhang, Yifu Yuan, Prajwal Gurunath, Ishita Gupta, Shayegan Omidshafiei, Ali-akbar Aghamohammadi, Marcell Vazquez-Chanlatte, Liam Pedersen, Tairan He, and Guanya Shi. Falcon: Learning forceadaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 

- [45] Zhikai Zhang, Chao Chen, Han Xue, Jilong Wang, Sikai Liang, Yun Liu, Zongzhang Zhang, He Wang, and Li Yi. Unleashing humanoid reaching potential via real-worldready skill space. _arXiv preprint arXiv:2505.10918_ , 2025. 

- [46] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

