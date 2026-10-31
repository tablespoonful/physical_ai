---
title: "HWC-Loco: A Hierarchical Whole-Body Control Approach to Robust Humanoid Locomotion"
date: "2025-03-02"
authors: "Sixu Lin; Guanren Qiao; Yunxin Tai; Ang Li; Kui Jia; Guiliang Liu"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2503.00923
pdf: https://arxiv.org/pdf/2503.00923
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2503.00923)** / [論文ページ](https://arxiv.org/abs/2503.00923)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HWC-Loco: A Hierarchical Whole-Body Control Approach to Robust Humanoid Locomotion** 

**Sixu Lin**<sup>1</sup><sup>_,_2</sup> **Guanren Qiao**<sup>1</sup> **Yunxin Tai**<sup>3</sup> **Ang Li**<sup>1</sup><sup>_,_4</sup> **Kui Jia**<sup>1</sup><sup>_,_3</sup> **Guiliang Liu**<sup>1</sup><sup>_∗_</sup> 1The Chinese University of Hong Kong (Shenzhen) 2Harbin Institute of Technology 

3DexForce Technology 4Southeast University 

## **Abstract** 

Humanoid robots, capable of assuming human roles in various workplaces, have become essential to embodied intelligence. However, as robots with complex physical structures, learning a control model that can operate robustly across diverse environments remains inherently challenging, particularly under the discrepancies between training and deployment environments. In this study, we propose HWCLoco, a robust whole-body control algorithm tailored for humanoid locomotion tasks. By reformulating policy learning as a robust optimization problem, HWCLoco explicitly learns to recover from safety-critical scenarios. While prioritizing safety guarantees, overly conservative behavior can compromise the robot’s ability to complete the given tasks. To tackle this challenge, HWC-Loco leverages a hierarchical policy for robust control. This policy can dynamically resolve the trade-off between goal-tracking and safety recovery, guided by human behavior norms and dynamic constraints. To evaluate the performance of HWC-Loco, we conduct extensive comparisons against state-of-the-art humanoid control models, demonstrating HWC-Loco’s superior performance across diverse terrains, robot structures, and locomotion tasks under both simulated and real-world environments. Our project page is available at `HWC-Loco` . 

## **1 Introduction** 

Humanoid robots, with a physical structure resembling that of humans, can be seamlessly integrated into humans’ workspace and take on roles in completing different tasks [1]. This capability makes them reliable embodiments of artificial intelligence in various forms [2]. In recent years, with advancements in both hardware capabilities and control algorithms, humanoid robots have become an increasingly significant type of robot with a growing impact on practical applications across various environments, such as factories, homes, and offices [3–5]. 

~~Disturb~~ Detect ~~Stability Recover~~ 

Figure 1: An example of recovering from a Hard Kick: The humanoid robot withstands external disturbance by automatically detecting hazardous states and adjusting its motion to regain stability. 

In the development of humanoid control, classic methods commonly rely on model-based optimization [6–10]. However, these methods require precise and comprehensive modeling of the robot’s structure, kinematics, and dynamics across different environments. In practice, obtaining such data requires significant computational resources or manual effort. These limitations significantly influence the scalability of these approaches. To develop an end-to-end solution with promising generalizability, recent studies [11–15] adopted Reinforcement Learning (RL) methods by training a neural model to control based on human demonstrations and interactions with the environment. 

> _∗†_ Corresponding author. Email: `liuguiliang@cuhk.edu.cn` 

Preprint. Under review. 

While these learning-based approaches show potential for effective control policies across various tasks, they are typically trained in simulated environments, which often differ considerably from the deploying environment. To bridge the Simulation-to-Real (Sim2Real) gap, previous works often introduce additional regularization to constrain the robot’s movements or employ domain randomization to account for variations in the robot’s physical properties [16–18] . However, excessive regularization can greatly affect the efficiency of control policy, and unstructured randomization often fails to capture safety-critical patterns in real-world applications. 

To develop a reliable locomotion policy capable of generalizing from the training to the deployment environment, we propose formulating policy optimization as a robust optimization problem under misspecified environmental dynamics. However, traditional robust optimization primarily focuses on worst-case control, requiring the policy to ensure safety under the most adverse environmental dynamics within an uncertainty set. Under this context, the learned policy tends to be overly conservative, inducing sub-optimal control performance in terms of finishing the given task. 

In this paper, to learn a control policy that can dynamically solve the trade-off between task performance and maintaining safety under different deployment environments, we present **H** ierarchical **W** hole-body **C** ontrol for Robust Humanoid **Loco** motion (HWC-Loco). Figure 1 illustrates an example of HWC-Loco, where a _high-level planning policy_ detects hazardous states and seamlessly switches from the _goal-tracking policy_ to a _safety-recovery policy_ . 

The _goal-tracking policy_ is designed to follow task-specific commands (e.g., moving velocity). Additionally, we ensure that the learned policy can effectively adhere to humanoid behavioral patterns by ensuring its distributional alignment with human motions. Note that this policy primarily focuses on ensuring task completion performance, without addressing safety issues that may arise from potential mismatches with the deployment environment. 

The _safety-recovery policy_ aims at ensuring safety across various deployment environments. To address safety-critical scenarios during deployment, we construct an uncertainty set by designing an extreme-case estimation mechanism. Within these constructed scenarios, we propose a dynamic constraint guided by the Zero Moment Point (ZMP) to ensure stability under various disturbances. 

While the goal-tracking and safety-recovery policies are primarily designed to enhance task performance and safety control, respectively, they lack a coordination mechanism to effectively control the trade-off between these objectives. To address this limitation, we propose a _high-level planning policy_ that dynamically selects which policy to activate based on the scenario. 

We conduct extensive experiments to evaluate the performance of HWC-Loco from four fundamental perspectives: 1) _effectiveness_ , demonstrated across diverse terrains, 2) _robustness_ , evaluated under varying scales of disturbances, 3) _naturalness_ , exhibited in its ability to imitate human behavioral norms, 4) _scalability_ evaluated in different robot embodiment and motion tracking tasks. These validations are performed in both simulated and real-world settings, demonstrating HWC-Loco as a foundational advancement for achieving reliable humanoid locomotion in safety-critical scenarios. 

## **2 Related Work** 

**Learning-based Legged Robot Locomotion.** Various learning-based methods have been proposed for legged locomotion, such as quadrupedal locomotion [17, 19, 20, 18, 21–23] and bipedal locomotion [24–27]. Despite their success, these approaches cannot be directly applied to humanoid robots because of the complex physical structure and the higher degrees of freedom. Recent advances in hardware and learning methods (e.g., RL algorithms) have enabled humanoid robots to move through diverse and complex environments. Some humanoid control policy navigates across diverse terrains using only proprioceptive information [12, 28, 15]. Others enhance performance by incorporating additional sensors, such as vision or LiDAR, to collect detailed environmental data, enabling robots to perform complex tasks like stair climbing and parkour jumps [11, 13, 29]. While these approaches have demonstrated promising locomotion performance, they lack mechanisms to handle safety-critical scenarios that humanoid robots may encounter during real-world deployment. 

**Whole-body control for humanoid robots.** Learning effective whole-body control remains a central challenge for humanoid robotics. Prior works [30–32] have demonstrated impressive results in simulated avatars, showcasing the feasibility of learning-based control strategies. More recently, studies such as [33, 14, 34–39] have enabled realistic robots to imitate complex human-like motions, such as boxing and dancing by leveraging motion priors from human demonstrations. Additionally, previous methods employed multi-stage reward designs to accomplish complex tasks [40, 41]. 

2 

However, the success of these methods often relies on intricate reward shaping and struggles to generalize across different humanoid robots, particularly when motion priors are unavailable. 

## **3 Problem Formulation** 

**Learning Environment.** We formulate the environment of the humanoid locomotion task with a Partially Observable Markov Decision Process (POMDP) _M_ = ( _S, A, O, PT , r, µ_ 0 _, γ_ ), where: 1) Within the state space _S_ , a state _s ∈S_ records the environmental information and the robot’s internal states. 2) _A_ denotes the action space, and action _a ∈A_ denotes the target joint angles that a PD controller uses to actuate the degrees of freedom (DOF). 3) _o ∈O_ denotes an observation, which provides partial information about the state of the agent due to sensory limitations and environmental uncertainty. At a time step _t_ , **_o_** _t_ includes velocity command **_v_**<sup>_cmd_</sup> _t ∈_ R<sup>3</sup> and proprioception **_o_**<sup>_p_</sup> _t_ that records a humanoid’s internal state. Appendix A.2 introduces the details. By incorporating the temporal observations **_o_**<sup>_H_</sup> _t_ = [ **_o_** _t,_ **_o_** _t−_ 1 _, · · · ,_ **_o_** _t−H_ ], the control model can summarize a state as _st_ = [ **_o_**<sup>_H_</sup> _t_<sup>_,_P</sup><sup>_t_],where P</sup><sup>_t_is the privileged information which the robot can’t access in realistic</sup> deployment, including base velocity _vt_ , terrain height, external disturbance and ZMP features (see Section 4.3). 4) _PT ∈_ ∆<sup>_S_</sup> _S×A_<sup>denotes the transition function as a mapping from state-action pairs to</sup> a distribution of future states. 5) _r_ denotes the reward functions, which typically consist of penalty, regularization, and task rewards. These reward signals significantly influence the optimality of the control policy, for which we provide a detailed introduction in the following. 6) _µ_ 0 _∈_ ∆<sup>_S_</sup> denotes the initial state distribution. 7) _γ ∈_ (0 _,_ 1] denotes the discounting factor. The robot’s policy stops at a terminating state ˜ _s_ , and the corresponding terminating time is denoted as _T ∈_ (0 _, ∞_ ). 

Under this POMDP, our goal is to learn a policy _π ∈_ ∆<sup>_A_</sup> _S_<sup>according to the objective as follows:</sup> 


In the task of humanoid locomotion, the total rewards can be generally represented as a weighted combination of task rewards _r_ T, penalty rewards _r_ P, and regularization rewards _r_ R [14, 34, 11], where the rewards have distinct semantic meanings: 

- _Task rewards r_ T assess how effectively the agents achieve the goals of the current task, such as tracking velocities [11], managing contacts [41], and producing expressive motions [33]. These task rewards are closely correlated with the optimality of the current control policy, making them an appropriate _objective to maximize_ in this context. 

- _Penalty rewards r_ P are used to prevent undesirable events. For example, in locomotion tasks, these penalties are applied when the humanoid falls or when the robot violates dynamic constraints, such as torque limits and joint position limits. To mitigate these negative outcomes, recent studies [14, 34] have assigned a large weight _β_ P to these rewards. While these weights inherently function as Lagrange multipliers [42], they are predefined and not subject to optimization. Consequently, a more effective approach would be to model the control problem as a _constrained RL problem_ . 

- _Regularization rewards r_ R aligns the behavior of the humanoid with human preferences on motion styles or safe deployment. However, accurately specifying these regularizations remains challenging since they are often task-dependent, context-sensitive, and inherently rooted in human experts’ experience [43]. As a result, instead of manually specifying regularizations, we _align the robot’s motion with human preferences_ by imitating human behavior from motion datasets (e.g., AMASS dataset [44]), which contains rich signals about desirable behavior norms. 

**Constrained RL for Whole-Body Control.** Inspired by the aforementioned analysis, we formulate the whole-body control locomotion objective for humanoid robots as follows: 


where 1) we replace the hard regularization in _r_ R with a mimic learning objective _Df_ ( _ρM_<sup>_πE∥ρπ_</sup> _M_<sup>) that</sup> constrains the distributional divergence between the learned policy’s occupancy measure _ρ_<sup>_π_</sup> _M_<sup>and the</sup> expert policy’s occupancy measure _ρ_<sup>_π_</sup> _M_<sup>_E_.In this study we implement</sup><sup>_Df_by Wasserstein distance</sup> (Section 4.1). 2) Instead of relying on the penalty reward _r_ P, we use _ϕ_ to capture the feasibility of the current trajectory generated by the policy _π_ under the environment _M_ . Within the objective, only the task rewards _r_ T are subject to maximization; other desired characteristics of humanoid 

3 

robots are captured by constraints learned from human motion datasets. More importantly, this approach effectively eliminates the need for regularization on the humanoid robot’s upper or lower pose, significantly enhancing the learning of whole-body locomotion policies. 

**Robust Locomotion in Humanoid Robot.** A common approach to learning humanoid locomotion policies involves training in a simulated environment before deploying the policies in a real-world setting. Due to the complexity of real-world environments, there is often a significant discrepancy between the training and deployment environments. In this study, we characterize this discrepancy by the mismatched POMDPs defined as follows: 

**Definition 3.1.** (Mismatched POMDPs) We define a POMDP _M_ := ( _S, A, PT , O, r, µ_ 0 _, γ_ ), to be mismatched with another POMDP _M_<sup>_′_</sup> := ( _S, A, PT_<sup>_′, O, r, µ_0</sup><sup>_, γ_)iftheydifferonlyintransition</sup> functions (i.e., _PT̸_ = _PT_<sup>_′_).We define a set of mismatched POMDPs as</sup><sup>**_M_**</sup><sup>_m_=</sup><sup>_{M PT , M P ′_</sup> _T , . . . }_ , where their transition functions differ from each other. 

Note that we follow previous studies [45] and primarily focus on the mismatch in transition dynamics during learning and deployment. The uncertainty set of transition function [46] is represented as: 


where _α_ specifies the scale of mismatch, _PT_<sup>_L_denotes the transition function in the learning environ-</sup> ment and P _⊆_ ∆<sup>_S_</sup> _S×A_<sup>represents the set of all candidate transition functions. While other factors, such</sup> as divergence in state-action spaces and initial state distribution _µ_ 0, can influence the performance during deployment, we find that the majority of factors affecting Sim2Real performance in humanoid locomotion _P_ ¯ _T_ denotes a Gaussian function, the underlying sensor noise can be captured by transitions intasks can be characterized by the mismatch in transition dynamics. For example, P<sup>_L_</sup> _α_ if<sup>.</sup> Additionally, if _P_<sup>¯</sup> _T_ denotes a projection from one spatial state to another, the variations of terrains in the deploying environment can be modeled by transitions in P<sup>_L_</sup> _α_<sup>[13].</sup> 


where 1) P<sup>_L_</sup> _α_<sup>represents the set of mismatched dynamics from the learning environment dynamics</sup> _PT_<sup>_L_(defined in 3) and 2)</sup><sup>_ρ_</sup> _M_<sup>_π_(</sup><sup>_s, a_) = (1</sup><sup>_−γ_)</sup><sup>_π_(</sup><sup>_a|s_) �</sup><sup>_∞_</sup> _t_ =0<sup>_γtp_(</sup><sup>_st_=</sup><sup>_s|π, M_) defines the normalized</sup> occupancy measure of policy _π_ under the environment _M_ . Intuitively, we aim to learn a robust control policy that ensures feasibility across all mismatched transition functions _P_<sup>�</sup> _T ∈_ P<sup>_L_</sup> _α_<sup>, thereby</sup> guaranteeing the safety of policy _π_ . However, for the reward-maximizing and mimic learning objectives, we optimize the policy based on the transition dynamics in the learning environment _PT_<sup>_L_,</sup> rather than concentrating solely on worst-case guarantees. 

## **4 Hierarchical Whole-Body Control for Humanoid Robust Locomotion** 

In practice, developing an end-to-end solver for the robust locomotion problem (4) is challenging, as it involves multiple deployment environments and constraints that must be adhered to. To tackle this issue, we propose dividing the objective into two stages: goal-tracking and safety recovery. The goal-tracking policy maximizes rewards while mimicking human behaviors (see Section 4.1). When mismatched environmental dynamics pose a risk to the safety of the control policy, HWC-Loco switches to the safety recovery policy, which manages safety-critical events to ensure the feasibility of humanoid control (see Section 4.2). To dynamically identify the "sweet spot" for policy switching or activation, we introduce a high-level policy that coordinates the low-level policies based on historical observations and the robot’s current status (see Section 4.3). Figure 2 illustrates the training pipeline of our HWC-Loco. 

### **4.1 Learning Goal-Tracking Policy for Efficient Humanoid Locomotion** 

The goal-tracking policy primarily focuses on tracking the provided command within the learning environment efficiently and naturally. This is achieved by optimizing the following objective function: 

4 


Figure 2: Overview of HWC-Loco: The framework consists of two stages: (a) Training _goal-tracking policy_ to effectively enable human-like locomotion across diverse terrains (Section 4.1) and _safety recovery policy_ to recover from safety-ciritical states (i.e., extreme-case) (Section 4.2). (b) Training the _high-level planning policy_ to select between the two pre-trained low-level policies (Section 4.3), thereby ensuring locomotion stability and consistency. 


Note that compared to the complete objective (4), this goal-tracking objective focuses only on maximizing performance in the training environments’ dynamics _PT_<sup>_L_.Within this objective, the scale</sup> of the cumulative task rewards,<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtr_T reflects how effectively the policy</sup><sup>_π_tracks locomotion-</sup> related commands. Appendix A.2 specifies the configuration of our task reward. In addition to the task rewards, a crucial aspect of the goal-tracking objective (5) is evaluating the distance between the occupancy measures of the trained policy and the expert policy In the following, striving for concise representation, we represent _ρ_<sup>_π_</sup> _M_<sup>_EP L_</sup> _T_<sup>and</sup><sup>_ρπ_</sup> _M_<sup>_P L_</sup> _T_<sup>by</sup><sup>_ρπE_and</sup><sup>_ρπ_.Driven</sup> by information theory, previous works [47] primarily implement _Df_ using metrics such as KullbackLeibler (KL) divergence or Jensen-Shannon (JS) divergence. However, these metrics fail when the support of _ρ_<sup>_πE_</sup> and _ρ_<sup>_π_</sup> has limited or zero overlap. In this study, we consider implement _Df_ with Wasserstein-1 distance under the Kantorovich-Rubinstein duality [48] such that: 


where the bounded Lipschitz-norm _∥fd∥L ≤_ 1 ensure the smoothness of functions _fd_ . Inspired by adversarial imitation learning [49, 50], an effective and intuitive implementation of _fd_ is a discriminator for measuring whether _x_ is generated by human experts, such that _fd_ : _X →_ R. It can be learned by maximizing the following objective: 


where weighted by _β_ , the gradient penalty term enforces the Lipschitz continuity required by the Wasserstein distance (i.e., _∥fd∥L ≤_ 1). During training, _ρ_<sup>_πE_</sup> represents the density of expert demonstration dataset _D_<sup>_E_</sup> , which is built from the CMU MoCap dataset [51]. Additionally, we include data about humans standing, walking, and running to learn various human behaviors. We then retarget the motion data into a humanoid robot-compatible format, which we use as the training dataset. By substituting _Df_ with equation (6), the goal-tracking objective (5) can be simplified as: 


where _s_<sup>_d_</sup> records the necessary state information for the discriminator. (See details in Appendix A.5). Given that this formulation of constrained RL problem has a zero duality gap [52], we can transform it into an unconstrained objective by analyzing the Lagrange dual form of the original constrained RL problem: 

5 


where _λ_ denotes the optimal Lagrange multiplier. In practical implementation, the policy _π_ and discriminator _fd_ can intuitively represent the generator and the discriminator under the adversarial learning framework. In implementation, we utilize the proximal policy optimization algorithm [53] to update the goal-tracking policy. By alternatively updating (7) and (9), we can develop a goal-tracking policy that effectively maximizes task rewards while closely mimicking the expert’s behavior. 

### **4.2 Learning Safety Recovery Policy for Handling Safe-Critical Events** 

Our safety recovery policy primarily focuses on handling emergency events, thereby recovering the robot from safety-critical situations and preventing failures of locomotion tasks, such as loss of balance or control policy malfunctions. To learn the safety-recover policy, we mainly study the complete objective (4). Similarly, as it is introduced in Section 4.1, we implement the divergence metric _Df_ with Wasserstein-1 distance, deriving the following objective: 


where _ϵϕ_ is a hyperparameter. By comparing this objective with the goal-tracking objective (9), while both consider task rewards and human mimicking performance, their key differences lie in the incorporation of uncertainty in environmental dynamics and feasibility constraints in policy updates. These additions necessitate the construction of an extreme-case uncertainty set and the modeling of safety constraints by learning the feasibility function _ϕ_ ( _·_ ). 

**Extreme-case Uncertainty Set.** Real-world deployment has complex terrains, external disturbances, hardware malfunctions, and sensor noise. Those factors may lead to extreme cases like falling or unexpected behaviors. To model them in the simulation (i.e., modelling _P_<sup>�</sup> _T_ s), We: 1) apply multi-scale external forces and torques to the humanoid body, 2) introduce random, high-intensity noise to the proprioceptive information and PD gains, 3) resample velocity commands to simulate malicious velocity inputs [54] within the goal-tracking policy, and 4) apply domain randomization to the training environment. Together, these dynamic variations construct the uncertainty set P<sup>_L_</sup> _α_<sup>, under</sup> which we learn the safety-recover policy. Appendix A.7 shows our implementation details. 

**Zero-Moment Point (ZMP) Constraint.** A bipedal robot can be generally modeled by a linear inverted pendulum [55, 56], where ZMP refers to the point where the ground reaction force has no horizontal moment. If the ZMP exits the support polygon (typically the foot’s contact area), the robot will quickly lose balance [57–60]. Stability is governed by gravity and the Center of Mass (CoM) accelerations, which also account for disturbances like obstacles and slippery surfaces. Under this assumption, we implement the feasibility indicator in the safety recovery objective (10) as follows: 


where 1) the vector **p** CoM denotes the _x_ and _y_ -coordinates of CoM position. 2) _z_ CoM is the height of the CoM. 3) _g_ represents the acceleration due to gravity. 4) **p** ¨CoM indicates the accelerations of the CoM in the _x_ and _y_ -directions. 5) **p** ac represents the center of the support polygon (specific to each robot and known in advance). Intuitively, _ϕ_ provides real-time insights into the robot’s stability and varies in its representation depending on the current support phase. Therefore, the humanoid robot can assess its stability in real time and use whole-body coordination to satisfy the ZMP constraint. 

### **4.3 High-Level Planning for Policy Transition** 

While the low-level policies can achieve varying levels of optimality, a fundamental challenge is coordinating these policies to ensure that a humanoid robot can efficiently complete tasks while adhering to safety and robustness requirements. We introduce a high-level planning policy that dynamically determines which policy to activate based on the specific state of humanoid robots. The task of policy selection has a discrete action space, and we learn this 


6 

high-level policy _π_ 0 based on the following objective: 


where 1) the policy selection action _a_ ¯ _t ∈{_ 0 _,_ 1 _}_<sup>2</sup> denotes a one-hot vector featuring whether the goal-tracking policy _π_ 1 and safety-recovery policy _π_ 2, 2) 1(¯ _at−_ 1 _̸_ = _a_ ¯t) denotes the continuality identifier for discouraging the over-frequent switch of policies, and 3) 1( _st_ ) denotes the termination identifier for preventing the failing of locomotion tasks. (2) and (3) are both _r_ P defined in Section 3. More importantly, within this objective, by adjusting _α_ , practitioners can adjust the trade-off safety guarantee and task completion. Training and algorithmic details can be found in Appendix A.2. 

We evaluate the average activation proportion of the goal-tracking policy during training. As shown in Figure 3, when _α_ = 0, 20, or 50, the goal-tracking policy _π_ 1 is predominantly selected, with the recovery policy _π_ 2 triggered only in rare dangerous cases. In contrast, when _α_ = 200, the sparsity of termination rewards induces training instability, resulting in overly conservative behavior. 

**Practical Deployment.** The training of humanoid control policy commonly relies on the privileged information P _t_ , such as external disturbances, terrain dynamics, etc. We follow [18] and infer P _t_ by training a VAE-based estimator _P_ ( _et, zt|o_<sup>_H_</sup> _t_<sup>) where</sup><sup>_zt_captures the contextual embedding of the</sup> P _t_ , and _et_ consists of body velocity and ZMP features. To enhance the representation of _ϕ_ ( _·_ ), we introduce frequency encoding, similar to the approach in [61], to capture the subtle variations in _ϕ_ ( _·_ ) for the policy. Additionally, instead of the zero-mean Gaussian prior, we introduce a learnable prior similar to [62]. Moreover, we include a certain degree of domain randomization in the learning of HWC-Loco policies. The details of domain randomization are in Appendix A.7. 

## **5 Experiment** 

**Experiment Settings.** To conduct a comprehensive evaluation, we quantify the control performance of HWC-Loco in simulated (Issac Gym [63]) and realistic environments from the following perspectives: 1) _Effectiveness_ : How effectively does HWC-Loco navigate across diverse terrains? 2) _Robustness_ : How well can HWC-Loco stabilize the humanoid robot under varying levels of disturbance? 3) _Naturalness_ : How well does HWC-Loco imitate human-like movement norms? 4) _Scalability_ : How effectively does HWC-Loco generalize to diverse embodiments and tasks? 

Our evaluation metric includes a) _Success Rate_ : The proportion of successful traverse across different scenarios. [64] b) _Goal Tracking_ performance: The ability to accurately follow velocity commands by maximizing task rewards _r_ T detailed in Appendix A.2 [43]. c) _Human-Like_ behavior: Measured as the Wasserstein-1 distance between the robot’s and sampled human motions. 

**Comparison Methods.** To evaluate the effectiveness of different components in HWC-Loco, we design a comparison method using an ablation approach as follows: 1) _HWC-Loco-l_ sets _α_ to a lower value, thereby reducing the sensitivity of the high-level policy to failure events. 2) _Goal-Tracking Policy_ removes the safety recovery mechanism and relies solely on the goal-tracking policy _π_ 1 (Section 4.1). 3) _DreamWaQ-Humanoid_ further removes the human imitation objective _Df_ from objective (5), effectively reducing our method to an adaptation of DreamWaQ [18] for humanoid control. 4) To highlight the benefits of our hierarchical policy, we compare a recent advancement of DreamWaQ, called _AHL_ [64], which employs two-phase training for updating the locomotion policy. All policies are trained using three random seeds and evaluated in 1000 distinct environments. 

### **5.1 Effectiveness: Locomotion across Diverse Terrains** 

**Effectiveness in Simulated Environments.** We evaluate the policies on challenging terrains, specifically slopes and stairs. To enable a comprehensive comparison, evaluations are performed under both low-speed and high-speed command conditions. Low-speed commands are sampled as _v_ x<sup>_c∼_[0</sup><sup>_._0</sup><sup>_,_1</sup><sup>_._0],</sup><sup>_v_</sup> y<sup>_c∼_[</sup><sup>_−_0</sup><sup>_._3</sup><sup>_,_0</sup><sup>_._3],and</sup><sup>_w_</sup> z<sup>_c∼_[</sup><sup>_−_0</sup><sup>_._5</sup><sup>_,_0</sup><sup>_._5],whilehigh-speedcommandsfollow</sup> _v_ x<sup>_c∼_[1</sup><sup>_._0</sup><sup>_,_2</sup><sup>_._0],</sup><sup>_v_</sup> y<sup>_c∼_[</sup><sup>_−_0</sup><sup>_._6</sup><sup>_,_0</sup><sup>_._6],and</sup><sup>_w_</sup> z<sup>_c∼_[</sup><sup>_−_1</sup><sup>_._0</sup><sup>_,_1</sup><sup>_._0].Here,</sup><sup>_v_</sup> x<sup>_c_and</sup><sup>_v_</sup> y<sup>_c_denote the commanded</sup> linear velocities along the x- and y-axes, respectively, and _w_ z<sup>_c_denotesthecommandedangular</sup> velocity around the z-axis. Table 1 shows that our HWC-Loco achieves the highest success rate across all evaluated scenarios, while maintaining promising goal tracking and human mimic performance. Notably, in the high-speed stair terrain setting, HWC-Loco has a significantly higher success rate than all other policies, although its goal-tracking ability slightly decreases. This indicates that the policy prioritizes stability over aggressive goal pursuit. For example, when given a high-speed command, 

7 

HWC-Loco enables the policy to adapt dynamically in safety-critical situations (e.g., navigating stairs mid-air) rather than rigidly maintaining high velocity. Comparably, when downplaying the sensitivity to safety-critical events and removing the safety-recovery policy, the success data drops significantly from nearly 85% to around 60% in the testing environment with stairs and high-speed commands. 

**Effectiveness in Realistic Environments.** Figure 10 (see Appendix B.1) demonstrates the robot’s ability to climb 15 cm stairs and 20° slopes. When faced with challenging terrain, the robot prioritizes safety by activating the recovery policy. After regaining stability, it smoothly transitions back to goal tracking, showcasing its adaptive control in dynamic and uncertain environments. Figure 11 (see Appendix B.1) further illustrates the robot’s effectiveness in real-world outdoor settings, where it successfully navigates across diverse terrains, including flat ground, grassy surfaces, and slopes. 

Table 1: Locomotion performance in simulated environments. Each evaluation runs for 1200 steps, which is equivalent to 12 seconds of real clock time. 

|**Method**||**Slopes**|||**Stairs**||
|---|---|---|---|---|---|---|
||**Success Rate(%)**_↑_|**Goal Tracking**_↑_|**Human - like**_↓_|**Success Rate(%)**_↑_|**Goal Tracking**_↑_|**Human - like**_↓_|
|**(a) Low Speed**|||||||
|DreamWaQ|92_._31_±_0_._40|1_._19_±_0_._02|3_._52_±_0_._05|74_._32_±_1_._30|1_._19_±_0_._03|3_._53_±_0_._02|
|AHL|98_._83_±_0_._15|1_._21_±_0_._01|3_._41_±_0_._04|93_._73_±_0_._70|1_._21_±_0_._04|3_._44_±_0_._01|
|Goal-tracking Policy|99_._90_±_0_._04|**1****_._31****_±_ 0****_._00**|**3****_._30****_±_ 0****_._05**|96_._60_±_0_._14|**1****_._31****_±_ 0****_._00**|**3****_._31****_±_ 0****_._01**|
|HWC-Loco-l|**100****_._00****_±_ 0****_._00**|1_._23_±_0_._02|3_._32_±_0_._03|99_._80_±_0_._08|1_._21_±_0_._02|3_._31_±_0_._06|
|HWC-Loco|**100****_._00****_±_ 0****_._00**|1_._22_±_0_._02|3_._32_±_0_._05|**99****_._98****_±_ 0****_._01**|1_._19_±_0_._03|3_._34_±_0_._03|
|**(b) High Speed**|||||||
|DreamWaQ|90_._46_±_0_._43|1_._05_±_0_._01|3_._63_±_0_._04|60_._58_±_0_._64|1_._06_±_0_._01|3_._66_±_0_._02|
|AHL|97_._36_±_0_._23|1_._12_±_0_._01|3_._76_±_0_._02|67_._48_±_0_._77|1_._09_±_0_._01|3_._68_±_0_._04|
|Goal-tracking Policy|98_._51_±_0_._45|**1****_._13****_±_ 0****_._00**|3_._52_±_0_._03|72_._60_±_0_._97|**1****_._11****_±_ 0****_._00**|3_._43_±_0_._02|
|HWC-Loco-l|99_._95_±_0_._02|1_._12_±_0_._02|**3****_._43****_±_ 0****_._04**|78_._92_±_0_._45|1_._10_±_0_._01|**3****_._39****_±_ 0****_._05**|
|HWC-Loco|**100****_._0****_±_ 0****_._00**|1_._12_±_0_._02|3_._44_±_0_._09|**84****_._34****_±_ 0****_._43**|1_._07_±_0_._03|3_._46_±_0_._03|


### **5.2 Robustness: Stable Control under Disturbances** 

**Robustness under Simulated Disturbances.** To demonstrate the robustness of HWC-Loco, we conduct extensive disturbance tests in simulation. The robots are commanded to follow randomly sampled velocities within the training distribution while navigating a uniformly mixed terrain comprising flat ground, obstacles, slopes, and stairs. Under these general locomotion settings, we design three types of disturbances as follows: 1) External force/torque disturbances, where random forces and torques (up to 200 N and 200 N _·_ m) are applied to each robot link, either at a low frequency of 1 Hz or as constant perturbations lasting 0.5 seconds, following prior setups [65, 66]. 2) Impulse disturbances on the CoM, implemented by directly altering the robot’s CoM velocity [65, 28]. We simulate both low-impulse and high-impulse scenarios, with linear velocity perturbations of 0–1 m/s or 1–2 m/s, and angular velocity perturbations of 0–0.5 rad/s or 0.5–1.0 rad/s, respectively. 3) Payload disturbances, where an additional mass uniformly sampled from either 0 to 5 kg or 0 to 10 kg is added to upper-body links [21, 12], along with internal perturbations from sensor and actuator noise (see Table 11 in Appendix A.7), to simulate unmodeled dynamics and varying mass distribution scenarios. 

As shown in Table 2, HWC-Loco consistently achieves the highest success rates across all types of disturbances. Specifically, under constant disturbances, HWC-Loco demonstrates superior performance with a success rate of 75.95%, which is nearly 25% higher than that of DreamWaQ. It validates the effectiveness of HWC-Loco’s recovery mechanism in resisting strong and persistent forces. Under low-impulse disturbances, all methods maintain relatively high success rates, with HWC-Loco again achieving the best performance at 94.84%. When facing more challenging high-impulse disturbances, the performance gap becomes more pronounced. HWC-Loco reaches a success rate of 81.27%, outperforming all baselines by a significant margin. This result indicates that the recovery mechanism effectively mitigates the impact of sudden impulses by enabling the robot to quickly lower its body and wave its arms to regain stability. In the payload test, HWC-Loco also demonstrates the best performance. Although it s not explicitly trained on scenarios such as adding 10 kg to the hands, it maintains a high success rate. This highlights the robustness of HWC-Loco to unseen disturbances. 

Table 2: Robustness of Locomotion across Various Terrains under Different Disturbances 

|**Policy**|**External Force/T**|**orque Disturbances**|**Impulse Distur**|**bances on CoM**|**Payload on**|**Upper Body**|
|---|---|---|---|---|---|---|
||**Low-freq.** _↑_|**Constant**_↑_|**Low-imp.** _↑_|**High-imp.** _↑_|**Low Payload**_↑_|**High Payload**_↑_|
|DreamWaQ|85_._92_±_1_._64|51_._31_±_0_._97|85_._24_±_0_._37|45_._34_±_0_._41|67_._63_±_3_._10|55_._04_±_2_._82|
|AHL|87_._15_±_2_._86|60_._72_±_0_._36|85_._87_±_1_._47|62_._94_±_1_._29|79_._29_±_0_._65|59_._16_±_1_._60|
|Goal-tracking Policy|90_._00_±_2_._20|61_._20_±_0_._61|88_._90_±_0_._60|58_._13_±_0_._78|78_._34_±_1_._23|61_._44_±_1_._00|
|HWC-Loco-l|92_._69_±_0_._56|68_._60_±_0_._28|92_._79_±_1_._75|77_._09_±_0_._79|84_._11_±_2_._66|63_._96_±_0_._09|
|HWC-Loco|**95****_._88****_±_ 0****_._37**|**75****_._95****_±_ 0****_._66**|**94****_._84****_±_ 0****_._54**|**81****_._27****_±_ 0****_._80**|**87****_._43****_±_ 0****_._92**|**69****_._86****_±_ 1****_._00**|


8 

**Robustness in Realistic Deployment.** We deploy HWC-Loco on a real humanoid robot and evaluate its performance under various external force disturbances. Figure 12 (see Appendix B.1) shows policy switching and associated changes in roll and pitch angles under continuous perturbations, including pushes, pulls, and kicks. Upon encountering disturbances, the robot promptly switches to the recovery policy, adjusting its posture and gait to regain stability. Importantly, the controller does not rely solely on recovery mode but dynamically switches between goal-tracking and recovery policies, thereby adapting the action distribution to environmental changes. Figure 13 (see Appendix B.1) further demonstrates the robot’s robustness to disturbances in outdoor settings. 

### **5.3 Naturalness: Imitating Human-like Movements** 

This experiment assesses the robot’s ability to imitate human-like locomotion under varying velocity commands. As shown in Figure 4, the robot remains stationary at 0 m/s, and exhibits natural walking behavior at 1.0 m/s, characterized by straight elbows and coordinated arm swings. At 2.5 m/s, it transitions to running, with longer strides and increasingly bent elbows, closely resembling human running. As the velocity increases, both stride length and step frequency adjust dynamically, mimicking typical human locomotion. In contrast, prior approaches [28, 67, 64, 68] often maintain a fixed step frequency regardless of the commanded velocity. Some even exhibit in-place stepping at 0,m/s [68, 64], resulting in unnatural behavior for tasks requiring a steady stance, such as manipulation. 

### **5.4 Scalability: Extending HWC-Loco to New Tasks** 

**Cross Embodiment Validation.** We deploy HWC-Loco on the Unitree G1 humanoid robot to evaluate its generalization capability under the same locomotion settings. As shown in Table 3, G1 outperforms H1 across all metrics. A detailed analysis is provided in Appendix A.2. 

Table 3: Comparison of Embodiments 

|**(a) Stationary**||**Success Rate**_↑_|**Goal Tracking**|_↑_<br>**Human-like**_↓_|
|---|---|---|---|---|
||**Unitree H1**<br>**Unitree G1**|97_._13_±_0_._43<br>**98****_._14****_±_ 0****_._35**|1_._10_±_0_._00<br>**1****_._12****_±_ 0****_._01**|3_._18_±_0_._01<br>**3****_._11****_±_ 0****_._03**|
|**(b) Walking**|Table 4:|Motion Trac|kingunder D|isturbances|
|**(c) Running**||**Punching**_↑_|**Dancing**_↑_<br>|**Expressive Walking**_↑_|
||**HWC-Loco**<br>**Motion-tracking**|**94****_._01****_±_ 0****_._49**<br><br>90_._85_±_0_._74|**86****_._44****_±_ 0****_._60**<br>81_._64_±_0_._64|**94****_._53****_±_ 0****_._23**<br>89_._63_±_0_._27|


Figure 4: Human-like behavior. 

**Expressive Motion Tracking** We follow the approach of ExBody[33, 69] and set expressive motion as the goal for HWC-Loco. We train the model following the same pipeline as locomotion tasks. A domain-randomized motion tracking policy serves as the baseline. We evaluate both policies on three representative motions under impulse disturbances. The success rates are reported in Table 4. 

## **6 Limitation** 

Our approach has three main limitations. First, policy transitions are governed by a learned discrete decision module, while the low-level controllers remain fixed. A jointly optimized hierarchical framework may enable smoother and more adaptive transitions. Second, the humanoid robot used in real-world deployment has only 19 degrees of freedom, which limits whole-body coordination and constrains the expression of complex recovery behaviors. Third, the recovery policy is trained in simulated dynamic scenarios that may not fully reflect the diversity and complexity of real-world disturbances. Incorporating more realistic perturbations, such as those generated by adversarial policies, could further improve recovery ability. 

## **7 Conclusion** 

We introduce HWC-Loco, a hierarchical control framework for humanoid robots that incorporates an embedded safety recovery mechanism. This framework has been validated across various tasks and scenarios, demonstrating exceptional effectiveness, robustness, naturalness, and scalability. Notably, the safety mechanism in HWC-Loco extends beyond locomotion, enabling reliable performance in complex tasks through a dynamic task-safety balance. This ensures robust operation in real-world deployments, positioning HWC-Loco as a foundational solution for safety-critical applications such as industrial automation and assistive robotics. A promising direction for future research is integrating HWC-Loco with loco-manipulation skills, enabling safety-critical control across a broader range of tasks involving different objects. 

9 

## **References** 

- [1] Saeed Saeedvand, Masoumeh Jafari, Hadi S. Aghdasi, and Jacky Baltes. A comprehensive survey on humanoid robot development. _Knowledge Engineering Review_ , 34:e20, 2019. 

- [2] Giuseppe Paolo, Jonas Gonzalez-Billandon, and Balázs Kégl. Position: A call for embodied AI. In _Forty-first International Conference on Machine Learning, ICML_ , 2024. 

- [3] Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _arXiv preprint arXiv:2403.10506_ , 2024. 

- [4] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ , 2024. 

- [5] Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse-kai Chan, et al. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. _arXiv preprint arXiv:2410.00425_ , 2024. 

- [6] Yoshiaki Sakagami, Ryujin Watanabe, Chiaki Aoyama, Shinichi Matsunaga, Nobuo Higaki, and Kikuo Fujimura. The intelligent ASIMO: system overview and integration. In _IEEE/RSJ International Conference on Intelligent Robots and Systems, IROS_ , pages 2478–2483. IEEE, 2002. 

- [7] Luis Sentis and Oussama Khatib. A whole-body control framework for humanoids operating in human environments. In _IEEE International Conference on Robotics and Automation, ICRA_ , pages 2641–2648. IEEE, 2006. 

- [8] David Gouaillier, Vincent Hugel, Pierre Blazevic, Chris Kilner, Jérôme Monceaux, Pascal Lafourcade, Brice Marnier, Julien Serre, and Bruno Maisonnier. Mechatronic design of NAO humanoid. In _IEEE International Conference on Robotics and Automation, ICRA_ , pages 769–774, 2009. 

- [9] Nicolaus A. Radford, Philip Strawser, Kimberly A. Hambuchen, Joshua S. Mehling, William K. Verdeyen, A. Stuart Donnan, James Holley, Jairo Sanchez, Vienny Nguyen, Lyndon B. Bridgwater, Reginald Berka, Robert O. Ambrose, Mason Myles Markee, N. J. Fraser-Chanpong, Christopher McQuin, John D. Yamokoski, Stephen Hart, Raymond Guo, Adam Parsons, Brian Wightman, Paul Dinh, Barrett Ames, Charles Blakely, Courtney Edmondson, Brett Sommers, Rochelle Rea, Chad Tobler, Heather Bibby, Brice Howard, Lei Niu, Andrew Lee, Michael Conover, Lily Truong, Ryan Reed, David Chesney, Robert Platt Jr., Gwendolyn Johnson, ChienLiang Fok, Nicholas Paine, Luis Sentis, Eric A. Cousineau, Ryan W. Sinnet, Jordan Lack, Matthew J. Powell, Benjamin Morris, Aaron D. Ames, and Jide Akinyode. Valkyrie: Nasa’s first bipedal humanoid robot. _Journal of Field Robotics_ , 32(3):397–419, 2015. 

- [10] Matthew Chignoli, Donghyun Kim, Elijah Stanger-Jones, and Sangbae Kim. The mit humanoid robot: Design, motion planning, and control for acrobatic behaviors. In _2020 IEEE-RAS 20th International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2021. 

- [11] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. In _8th Annual Conference on Robot Learning_ , 2024. 

- [12] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89): eadi9579, 2024. 

- [13] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao Huang, Ping Luo, and Jiangmiao Pang. Learning humanoid locomotion with perceptive internal model. _arXiv preprint arXiv:2411.14386_ , 2024. 

- [14] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning human-to-humanoid real-time whole-body teleoperation. _arXiv preprint arXiv:2403.04436_ , 2024. 

10 

- [15] Xinyang Gu, Yen-Jen Wang, Xiang Zhu, Chengming Shi, Yanjiang Guo, Yichen Liu, and Jianyu Chen. Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning. _arXiv preprint arXiv:2408.14472_ , 2024. 

- [16] Hang Lai, Weinan Zhang, Xialin He, Chen Yu, Zheng Tian, Yong Yu, and Jun Wang. Sim-toreal transfer for quadrupedal locomotion via terrain transformer. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5141–5147. IEEE, 2023. 

- [17] Nikita Rudin, David Hoeller, Philipp Reist, and Marco Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In _Conference on Robot Learning_ , pages 91–100. PMLR, 2022. 

- [18] I Made Aswin Nahrendra, Byeongho Yu, and Hyun Myung. Dreamwaq: Learning robust quadrupedal locomotion with implicit terrain imagination via deep reinforcement learning. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5078–5084. IEEE, 2023. 

- [19] Haojie Shi, Bo Zhou, Hongsheng Zeng, Fan Wang, Yueqiang Dong, Jiangyong Li, Kang Wang, Hao Tian, and Max Q-H Meng. Reinforcement learning with evolutionary trajectory generator: A general approach for quadrupedal locomotion. _IEEE Robotics and Automation Letters_ , 7(2): 3085–3092, 2022. 

- [20] Shuxiao Chen, Bike Zhang, Mark W Mueller, Akshara Rai, and Koushil Sreenath. Learning torque control for quadrupedal locomotion. In _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2023. 

- [21] Gabriel B Margolis and Pulkit Agrawal. Walk these ways: Tuning robot control for generalization with multiplicity of behavior. In _Conference on Robot Learning_ , pages 22–31. PMLR, 2023. 

- [22] Ziwen Zhuang, Zipeng Fu, Jianren Wang, Christopher Atkeson, Soeren Schwertfeger, Chelsea Finn, and Hang Zhao. Robot parkour learning. _arXiv preprint arXiv:2309.05665_ , 2023. 

- [23] Tairan He, Chong Zhang, Wenli Xiao, Guanqi He, Changliu Liu, and Guanya Shi. Agile but safe: Learning collision-free high-speed legged locomotion. _arXiv preprint arXiv:2401.17583_ , 2024. 

- [24] Zhongyu Li, Xuxin Cheng, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Reinforcement learning for robust parameterized locomotion control of bipedal robots. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2811–2817. IEEE, 2021. 

- [25] Ashish Kumar, Zhongyu Li, Jun Zeng, Deepak Pathak, Koushil Sreenath, and Jitendra Malik. Adapting rapid motor adaptation for bipedal robots. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1161–1168. IEEE, 2022. 

- [26] Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Robust and versatile bipedal jumping control through reinforcement learning. _arXiv preprint arXiv:2302.09450_ , 2023. 

- [27] Helei Duan, Bikram Pandit, Mohitvishnu S Gadde, Bart Van Marum, Jeremy Dao, Chanho Kim, and Alan Fern. Learning vision-based bipedal locomotion for challenging terrain. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 56–62. IEEE, 2024. 

- [28] Xinyang Gu, Yen-Jen Wang, and Jianyu Chen. Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer. _arXiv preprint arXiv:2404.05695_ , 2024. 

- [29] Wandong Sun, Baoshi Cao, Long Chen, Yongbo Su, Yang Liu, Zongwu Xie, and Hong Liu. Learning perceptive humanoid locomotion over challenging terrain. _arXiv preprint arXiv:2503.00692_ , 2025. 

- [30] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

11 

- [31] Zhengyi Luo, Jinkun Cao, Rawal Khirodkar, Alexander Winkler, Kris Kitani, and Weipeng Xu. Real-time simulated avatar from head-mounted sensors. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 571–581, 2024. 

- [32] Zhengyi Luo, Jiashun Wang, Kangni Liu, Haotian Zhang, Chen Tessler, Jingbo Wang, Ye Yuan, Jinkun Cao, Zihui Lin, Fengyi Wang, et al. Smplolympics: Sports environments for physically simulated humanoids. _arXiv preprint arXiv:2407.00187_ , 2024. 

- [33] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive whole-body control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 

- [34] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [35] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. In _8th Annual Conference on Robot Learning_ , 2024. 

- [36] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, Linxi Fan, and Yuke Zhu. HOVER: versatile neural wholebody controller for humanoid robots. _arXiv preprint arXiv:2410.21229_ , 2024. 

- [37] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [38] Yanjie Ze, Zixuan Chen, JoÃG,<sup>oPedroAraÃšjo,Zi-angCao,XueBinPeng,JiajunWu,</sup> and C Karen Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

- [39] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Ri-Zhao Qiu, and Xiaolong Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _arXiv preprint arXiv:2505.03738_ , 2025. 

- [40] Dohyeong Kim, Hyeokjin Kwon, Junseok Kim, Gunmin Lee, and Songhwai Oh. Stage-wise reward shaping for acrobatic robots: A constrained multi-objective reinforcement learning approach. _arXiv preprint arXiv:2409.15755_ , 2024. 

- [41] Chong Zhang, Wenli Xiao, Tairan He, and Guanya Shi. Wococo: Learning whole-body humanoid control with sequential contacts. In _Annual Conference on Robot Learning_ , 2024. 

- [42] Shangding Gu, Long Yang, Yali Du, Guang Chen, Florian Walter, Jun Wang, and Alois Knoll. A review of safe reinforcement learning: Methods, theories, and applications. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 46(12):11216–11235, 2024. 

- [43] Zixuan Chen, Xialin He, Yen-Jen Wang, Qiayuan Liao, Yanjie Ze, Zhongyu Li, S Shankar Sastry, Jiajun Wu, Koushil Sreenath, Saurabh Gupta, et al. Learning smooth humanoid locomotion through lipschitz-constrained policies. _arXiv preprint arXiv:2410.11825_ , 2024. 

- [44] Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. AMASS: archive of motion capture as surface shapes. In _IEEE/CVF International Conference on Computer Vision, ICCV_ , pages 5441–5450. IEEE, 2019. 

- [45] Janosch Moos, Kay Hansel, Hany Abdulsamad, Svenja Stark, Debora Clever, and Jan Peters. Robust reinforcement learning: A review of foundations and recent advances. _Machine Learning and Knowledge Extraction_ , pages 276–315, 2022. 

- [46] Luca Viano, Yu-Ting Huang, Parameswaran Kamalaruban, Craig Innes, Subramanian Ramamoorthy, and Adrian Weller. Robust learning from observation with model misspecification. In _International Conference on Autonomous Agents and Multiagent Systems_ , pages 1337–1345, 2022. 

12 

- [47] Ahmed Hussein, Mohamed Medhat Gaber, Eyad Elyan, and Chrisina Jayne. Imitation learning: A survey of learning methods. _ACM Computing Surveys_ , 50(2):21:1–21:35, 2017. 

- [48] Cédric Villani et al. _Optimal transport: old and new_ , volume 338. Springer, 2009. 

- [49] Jonathan Ho and Stefano Ermon. Generative adversarial imitation learning. In Daniel D. Lee, Masashi Sugiyama, Ulrike von Luxburg, Isabelle Guyon, and Roman Garnett, editors, _Advances in Neural Information Processing Systems, NeurIPS_ , pages 4565–4573, 2016. 

- [50] Xin Zhang, Yanhua Li, Ziming Zhang, and Zhi-Li Zhang. f-gail: Learning f-divergence for generative adversarial imitation learning. In _Advances in Neural Information Processing Systems, NeurIPS_ , 2020. 

- [51] CMU, Cmu graphics lab motion capture database, `http://mocap.cs.cmu.edu/` . 

- [52] Santiago Paternain, Luiz F. O. Chamon, Miguel Calvo-Fullana, and Alejandro Ribeiro. Constrained reinforcement learning has zero duality gap. In _Advances in Neural Information Processing Systems, NeurIPS_ , pages 7553–7563, 2019. 

- [53] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [54] Fan Shi, Chong Zhang, Takahiro Miki, Joonho Lee, Marco Hutter, and Stelian Coros. Rethinking robustness assessment: Adversarial attacks on learning-based quadrupedal locomotion controllers. _arXiv preprint arXiv:2405.12424_ , 2024. 

- [55] Mitsuharu Morisawa, Kensuke Harada, Shuuji Kajita, Kenji Kaneko, Fumio Kanehiro, Kiyoshi Fujiwara, Shinichiro Nakaoka, and Hirohisa Hirukawa. A biped pattern generation allowing immediate modification of foot placement in real-time. In _2006 6th IEEE-RAS International Conference on Humanoid Robots_ , pages 581–586. IEEE, 2006. 

- [56] Kensuke Harada, Shuuji Kajita, Kenji Kaneko, and Hirohisa Hirukawa. An analytical method for real-time gait planning for humanoid robots. _International Journal of Humanoid Robotics_ , 3 (01):1–19, 2006. 

- [57] Pierre-Brice Wieber. Trajectory free linear model predictive control for stable walking in the presence of strong perturbations. In _2006 6th IEEE-RAS International Conference on Humanoid Robots_ , pages 137–142. IEEE, 2006. 

- [58] Siyuan Feng, X Xinjilefu, Christopher G Atkeson, and Joohyung Kim. Robust dynamic walking using online foot step optimization. In _2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 5373–5378. IEEE, 2016. 

- [59] Nicola Scianca, Daniele De Simone, Leonardo Lanari, and Giuseppe Oriolo. Mpc for humanoid gait generation: Stability and feasibility. _IEEE Transactions on Robotics_ , 36(4):1171–1188, 2020. 

- [60] Weiji Xie, Chenjia Bai, Jiyuan Shi, Junkai Yang, Yunfei Ge, Weinan Zhang, and Xuelong Li. Humanoid whole-body locomotion on narrow terrain via dynamic balance and reinforcement learning. _arXiv preprint arXiv:2502.17219_ , 2025. 

- [61] Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. _Communications of the ACM_ , 65(1):99–106, 2021. 

- [62] Zhengyi Luo, Jinkun Cao, Josh Merel, Alexander Winkler, Jing Huang, Kris Kitani, and Weipeng Xu. Universal humanoid motion representations for physics-based control. _arXiv preprint arXiv:2310.04582_ , 2023. 

- [63] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

13 

- [64] Wenhao Cui, Shengtao Li, Huaxing Huang, Bangyu Qin, Tianchu Zhang, Liang Zheng, Ziyang Tang, Chenxu Hu, NING Yan, Jiahao Chen, et al. Adapting humanoid locomotion over challenging terrain via two-phase training. In _8th Annual Conference on Robot Learning_ , 2024. 

- [65] Bowen Weng, Guillermo A Castillo, Wei Zhang, and Ayonga Hereid. On the comparability and optimal aggressiveness of the adversarial scenario-based safety testing of robots. _IEEE Transactions on Robotics_ , 39(4):3299–3318, 2023. 

- [66] Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning quadrupedal locomotion over challenging terrain. _Science robotics_ , 5(47):eabc5986, 2020. 

- [67] Xinyang Gu, Yen-Jen Wang, Xiang Zhu, Chengming Shi, Yanjiang Guo, Yichen Liu, and Jianyu Chen. Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning. _arXiv preprint arXiv:2408.14472_ , 2024. 

- [68] Qiang Zhang, Peter Cui, David Yan, Jingkai Sun, Yiqun Duan, Gang Han, Wen Zhao, Weining Zhang, Yijie Guo, Arthur Zhang, et al. Whole-body humanoid robot locomotion with human reference. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11225–11231. IEEE, 2024. 

- [69] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- [70] Zhicheng Wang, Wandi Wei, Ruiqi Yu, Jun Wu, and Qiuguo Zhu. Toward understanding key estimation in learning robust humanoid locomotion. _arXiv preprint arXiv:2403.05868_ , 2024. 

14 

## **A Addtional Details of HWC-Loco** 

### **A.1 Motion Retargeting** 

Our motion data is derived from the CMU Mocap dataset [51], which exclusively encompasses human locomotion data, featuring a diverse array of walking, jogging, and running styles. In aggregate, we have loaded 318 motion sequences, totaling 3729.18 seconds in duration. Our motion retargeting methodology closely follows the approach outlined in [33]. We have meticulously aligned the humanoid robot’s skeleton with that of humans, incorporating adjustments such as rotation, translation, and scaling. Additionally, we map human joints onto the humanoid robot’s structure. Specifically, the human motion data is adapted to the humanoid robot’s framework by mapping local information. Both the Unitree H1 and G1 robots possess shoulder and hip joints that are functionally equivalent to spherical joints. During the retargeting process, the three hip and shoulder joints are treated as a single spherical joint, corresponding to the human’s spherical joint. For one-dimensional joints such as the elbow and torso, the rotation angle is projected onto the corresponding rotation axis of the joint angles. 

Table 5: Double-DQN Parameters 

|Parameter|Value|||
|---|---|---|---|
|Batch Size|128|Table 6:|DQN Network Structure|
|Learning Rate|1e-4|Layer|Details|
|Gamma|0.99|L 1|idi 256|
|Max Grad Norm|1.0|ayer<br>L 2|[nput_m, ]<br>AtitiRLU|
|Replay Buffer Capacity<br>Switch Penalty Coefficient|2000000<br>0.001|ayer<br>Layer 3<br>Laer 4|cvaon: e<br>Regularization: Dropout<br>[256 128]|
|Target Update Frequency<br>Optimizer<br>Loss Function<br>Initial Epsilon|50<br>Adam<br>MSELoss<br>0.1|y<br>Layer 5<br>Layer 6<br>Layer 7|,<br>[128, 64]<br>Activation: ReLU<br>[64, output_dim]|
|Minimum Epsilon|0.001|||
|Epsilon Decay Rate|0.999|||


### **A.2 Implementation Details** 

**Proprioception:** For the Unitree H1, proprioception **_o_**<sup>_p_</sup> _t_<sup>_∈_R65, which denotes the internal state of the</sup> robot, including the base angular velocity **_w_** _t ∈_ R<sup>3</sup> , base roll **_r_** _t ∈_ R<sup>1</sup> , base pitch **_p_** _t ∈_ R<sup>1</sup> , degrees of freedom (DOF) positions **_q_** _t ∈_ R<sup>19</sup> , DOF velocities **_q_** ˙ _t ∈_ R<sup>19</sup> , previous actions **_a_** _t−_ 1 _∈_ R<sup>19</sup> , and projected gravity **_g_** _t ∈_ R<sup>3</sup> . The projected gravity refers to the component of gravity expressed in the robot’s local coordinate system. For the Unitree G1, proprioception **_o_**<sup>_p_</sup> _t_<sup>_∈_R77, includes base</sup> angular velocity **_w_** _t ∈_ R<sup>3</sup> , base roll **_r_** _t ∈_ R<sup>1</sup> , base pitch **_p_** _t ∈_ R<sup>1</sup> , DOF positions **_q_** _t ∈_ R<sup>23</sup> , DOF velocities **_q_** ˙ _t ∈_ R<sup>23</sup> , previous actions **_a_** _t−_ 1 _∈_ R<sup>23</sup> , and projected gravity **_g_** _t ∈_ R<sup>3</sup> . As with the H1, the projected gravity denotes the component of gravity in the robot’s local coordinate system. 

**Action Space:** The policy outputs continuous actions **a** _t ∈_ R<sup>_n_</sup> , which are utilized as target positions for a PD controller to compute joint torques. The actions correspond to the robot’s actuated degrees of freedom: specifically, **a** _t ∈_ R<sup>19</sup> (19 DoF) for the Unitree H1 and **a** _t ∈_ R<sup>23</sup> (23 DoF) for the Unitree G1. 

**Terrain details:** Terrains in the training environment simulated by Isaac Gym [63] include flats, obstacles, slopes, and stairs. An example of these terrains is shown in Figure 5. 

**Low-level Policy Training:** For all the low-level policies training, the commands are sampled from ranges: _v_ x<sup>_c∼_[</sup><sup>_−_0</sup><sup>_._6</sup><sup>_,_2</sup><sup>_._5],</sup><sup>_v_</sup> y<sup>_c∼_[</sup><sup>_−_0</sup><sup>_._6</sup><sup>_,_0</sup><sup>_._6] and</sup><sup>_w_</sup> z<sup>_c∼_[</sup><sup>_−_1</sup><sup>_._0</sup><sup>_,_1</sup><sup>_._0].During the initial training of the</sup> humanoid robot on uneven terrain, the robot often remains stationary due to the high difficulty of navigating complex surfaces. To address this, we introduce a terrain curriculum method [63]. The training terrain consists of various types, including flat planes, rough surfaces, steps, and slopes. As the robot achieves a goal-tracking performance of 70% of the commanded velocity, the terrain difficulty increases. Conversely, if the goal-tracking performance drops below 40% of the commanded velocity, the terrain becomes easier. 

15 


Figure 5: Visualization of different terrains. From left to right, the terrains are flats, obstacles, slopes, and stairs 

**Learning for Policy Transition:** High-level planning policy is utilized to switch between low-level policies, ensuring compliance with robustness constraints. For the High-level policy, the input is the same set of observations as used by the low-level policies, with the output being a two-dimensional Q-value. During training, two trained low-level policies are loaded and rolled out to generate training data for optimizing the high-level policy. We train this high-level policy in the simulation environment mentioned detailed in Section 4.2, focusing on locomotion goals as the primary task. The objective is to enable the robot to track goal commands across a variety of terrains. The details of the training process is in Algorithm 1 

**Algorithm 1** Training for High-level Policy using Double-DQN 

**Input:** Environment _env_ , Selector network _S_ , Target network _S_ target, Goal-tracking policy _L_ , Recovery policy _R_ Initialize: Learning rate _α_ , Discount factor _γ_ , Exploration rate _ϵ_ , Replay buffer _B_ , Target update frequency _f_ target, Switch penalty _λ_ switch, Exploration decay _ϵ_ decay, Minimum exploration _ϵ_ min _S_ target _← S_ {Initialize target network} **repeat** Observe initial state _s_ from _env_ Reset cumulative reward _R_ total, step count _n_ , previous action _a_ prev _←_ None **while** not done **do** Compute _Q_ ( _s, ·_ ) _← S_ ( _s_ ), select action _a_ with _ϵ_ -greedy Compute switch penalty: _r_ penalty _← λ_ switch _·_ **1** [ _a̸_ = _a_ prev] Execute _a_ , observe reward _r_ , next state _s_<sup>_′_</sup> , and done signal _d_ Store ( _s, a, r_ + _r_ penalty _, s_<sup>_′_</sup> _, d_ ) in _B_ Update _s ← s_<sup>_′_</sup> , _a_ prev _← a R_ total _← R_ total + _r_ , _n ← n_ + 1 **if** _B_ .size() _≥_ batch size **then** Sample ( _s, a, r, s_<sup>_′_</sup> _, d_ ) from _B a_<sup>_′_</sup> _←_ arg max _a′ S_ ( _s_<sup>_′_</sup> _, a_<sup>_′_</sup> ) {Online network selects action} _Q_<sup>target</sup> ( _s_<sup>_′_</sup> _, a_<sup>_′_</sup> ) _← S_ target( _s_<sup>_′_</sup> _, a_<sup>_′_</sup> ) {Target network evaluates} Compute target: _Q_<sup>target</sup> ( _s, a_ ) _← r_ + _γ_ (1 _− d_ ) _Q_<sup>target</sup> ( _s_<sup>_′_</sup> _, a_<sup>_′_</sup> ) Update _S_ by minimizing: _L_ = ( _S_ ( _s, a_ ) _− Q_<sup>target</sup> ( _s, a_ ))<sup>2</sup> **end if if** _n_ mod _f_ target = 0 **then** _S_ target _← S_ {Sync target network} **end if end while** Decay exploration rate: _ϵ ←_ max( _ϵ · ϵ_ decay _, ϵ_ min) **until** convergence criteria met **Output:** Trained Selector Network _S_ 

**Reward Details:** To better facilitate efficient humanoid locomotion, our task reward is defined as [28, 67]: 


where 1) _v_ xy<sup>_c_denotesthecommandedlinearvelocityalongthe</sup><sup>_x_and</sup><sup>_y_axes,while</sup><sup>_w_</sup> z<sup>_c_isthe</sup> commanded yaw velocity. 2) _v_ xy and _w_ z represent the corresponding base velocities of the humanoid 

16 

robot. 3) _α_ 1 and _α_ 2 indicate the hyperparameters that are utilized to adjust the importance of the different velocity terms. 4) _σ_ lin<sup>2and</sup><sup>_σ_</sup> ang<sup>2control the precision of the expected command tracking.</sup> Smaller values of _σ_ lin<sup>2and</sup><sup>_σ_</sup> ang<sup>2enhance the precision of command tracking for humanoid robots.</sup> However, they may hinder reward acquisition during the initial stages of training. 

The recovery policy shares the same task reward formulation as the goal-tracking policy. However, it uses larger values of the _σ_ lin<sup>2and</sup><sup>_σ_</sup> ang<sup>2, which implies a greater tolerance for velocity tracking errors.</sup> As a result, this reward term serves as a back-tracking reward for the safety recovery mechanism, encouraging it to return to a stable goal-tracking state. To further promote stable posture restoration and enable smooth transitions back to the goal-tracking policy, we introduce an additional stand reward, defined as: 


where **q** default represents a default standing pose. 

For safety realistic deployment, we add some energy and safety reward for the low-level policies training. These rewards are shown in Table. 

Table 7: Safety & Energy Reward 

|Term|Expression|Weight|
|---|---|---|
|DoF position limits|**1**(**q**_t /∈_[**q**min_,_**q**max])<br>|_−_1_e_<sup>2</sup><br>|
|DoF acceleration|_∥_¨**q**_t∥_<sup>2</sup><br>2<br>|_−_1_e_<sup>_−_7</sup><br>|
|DoF velocity|_∥_˙**q**_t∥_<sup>2</sup><br>2|_−_5_e_<sup>_−_4</sup>|
|Action rate|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup><br>2<br>|_−_2_e_<sup>_−_3</sup><br>|
|Torque|_∥τt∥_|_−_1_e_<sup>_−_5</sup>|
|Collision|�<br>_i∈_contact <sup>**1**</sup><sup>_{∥Fi∥>_ 1</sup><sup>_._0</sup><sup>_}_</sup>|_−_10|


### **A.3 PPO** 

In order to enhance the understanding of historical observation information, we have made some improvements to the Actor-network. We first process this information using an encoder network to preliminarily extract the features of the observation values at each time step, and then use a merger network to integrate the observation values at different time steps. Finally, we obtain fixeddimensional feature information, which is then input into the Actor backbone network together with other information. 

Table 8: PPO hyperparameters 

|Hyperparameter|Value|
|---|---|
|Actor Layer|[512, 256, 128]|
|Critic Layer|[512, 256, 128]|
|Activation Function|ELU|
|Discount Factor|0.99|
|GAE Parameter|0.95|
|Epochs per Rollout|5|
|Minibatch|4|
|Entropy Coefficient|0.005|
|Value Loss Coefficient (_α_1)|1.0|
|Clip Range|0.2|
|Learning Rate|2.e-4|
|Environment Steps per Rollout|24|


### **A.4 VAE** 

The VAE Network consists of an encoder and a decoder. The encoder takes historical observations as input and outputs latent representation and estimation of priviledged information. The decoder takes 

17 

latent as input and outputs the reconstruction of the next observation. The structure of VAE is shown in Figure 6 


Table 9: VAE hyperparameters 

|Hyperparameter|Value|
|---|---|
|Encoder Layer|[256, 128]|
|Decoder Layer|[256, 128, 64]|
|Activation Function|ELU|
|KL Coefficient|1.0|
|Learning Rate|1.e-4|


Figure 6: VAE Structure 

### **A.5 Discriminator** 

The input to the discriminator _s_<sup>_d_</sup> is defined as [ _q, v, w, r, p, k_ ], where _k_ represents the local positions of key points. Specifically, we define 12 key points, including the hips, shoulders, hands, ankles, knees, and elbows. For the Unitree H1, the total input dimension is 63, while for the Unitree G1, it is 67. 

The discriminator’s hyperparameters are shown in Table. 10. 

Table 10: Discriminator hyperparameters 

|Hyperparameter|Value|
|---|---|
|Discriminator Hidden Layer Dim|[1024,512]|
|Replay Buffer Size|500000|
|Expert Buffer Size|200000|
|Expert Fetch Size|512|
|Learning Batch Size|4096|
|Learning Rate|2e-5|
|Gradient Penalty Coefficient|1.0|
|lamda|1.0|


### **A.6 Saliency Analysis of Observations** 

We adopt an integrated gradients method similar to [70] to assess the importance of different parts of the observation to the policy, as shown in Fig.7. 

For the recovery policy, the Zero Moment Point (ZMP) encoding proves to be the most critical factor, followed by the estimated velocity. The robot’s current and historical proprioceptive states also contribute substantially to the policy’s decision-making process. In contrast, the environmental latent representation exhibits only a marginal effect. This hierarchy of importance reflects the necessity of strictly adhering to ZMP constraints to maintain dynamic stability and ensure the safety of the robot during recovery. 

For the high-level policy, the Zero Moment Point (ZMP) encoding remains the most influential component, indicating that it provides critical information for decision-making and substantially enhances the policy’s awareness of the robot’s stability. This observation implies that the high-level policy prioritizes stability-relevant features over task-irrelevant ones, which is advantageous for promoting generalization across diverse scenarios. Moreover, the environmental latent variable exhibits greater importance compared to that in the recovery policy, suggesting that high-level decisions are more sensitive to environmental factors such as terrain variations. 

18 


Figure 7: Importance of Observations 

### **A.7 Extreme Initialization** 

To simulate extreme scenarios that may occur in real-world deployment, we identify three primary causes of such cases: external disturbances, hardware malfunctions, and malicious commands. Additionally, we retain domain randomization to enhance the generalization of physical dynamics within the simulation environment. The specific details are outlined as follows: 

To enhance robustness and generalization in simulation, we simulate both extreme deployment scenarios and apply domain randomization. The extreme scenarios include external disturbances, sensor and actuator failures, and adversarial commands, while domain randomization targets physical variability in the environment. 

1) **External disturbances:** We apply external disturbances to every component of the robot. The external forces and torques are applied along the x, y, and z axes, with each direction sampled from the range of -200 N to 200 N for forces and -200 Nm to 200 Nm for torques. These disturbance forces and torques are updated at a frequency of 1 Hz. 

2) **Hardward magnification :** Random, high-intensity noise is introduced to the proprioceptive information and PD gains. The noise added to the proprioceptive data simulates sensor errors that may occur during real-world deployment. The noise applied to the PD gains simulates fluctuations in motor strength, reflecting potential issues in the robot’s actuators. The parameters for this noise are detailed in Table 11. 

3) **Malicious velocity:** Velocity commands are resampled from the command range, with updates occurring at a frequency of 5 Hz. Notably, this resampling mechanism is activated once the terrain curriculum exceeds half of its total progression. 

4) **Domain randomization (for environment variability):** Domain randomization is applied to all the training environments. This technique introduces variability in the environment’s parameters, such as friction and gravity. The specifics of the domain randomization are provided in Table 12. 

To improve the generalization of recovery ability, we utilize random initialization with extreme case initialization. The parameters are shown in Table 13 

Table 11: Intense Noise Parameters 

|Parameter|Range|Operator|
|---|---|---|
|DOF Position Noise|0.04|additive|
|DOF Velocity Noise|0.30|additive|
|Angular Velocity Noise|1.00|additive|
|IMU Noise|0.40|additive|
|Gravity Noise|0.10|additive|
|PD Gains|0.20|additive|


**Extreme-Case Analysis:** We record nearly 60000 normal state data with randomly sampled commands in diverse terrain settings in 8. We record nearly 10000 extreme cases in the P<sup>_L_</sup> _α_<sup>.Some of</sup> the terminal states are visualized in Fig. 9. For the extreme states, the distribution of velocity is close to the command ranges. Roll pitch and their velocity are in a common range, which is near zeros. For the normal states, the distribution of linear velocity overlaps with the command velocity 

19 

Table 13: Random Initialization Parameters 

Table 12: Domain Randomization Parameters 

|e : oman|anomzaton|arameters|Parameter|Range|
|---|---|---|---|---|
|Parameter|Range|Operator|Linear Velocity (x)|[_−_1_._0_,_2_._5]|
|Friction|[0.6, 2.0]|additive|Linear Velocity (y)|[_−_1_._0_,_1_._0]|
|Base Mass|[-1.0, 5.0]|additive|Linear Velocity (z)|[_−_0_._4_,_0_._4]|
|Base CoM|[-0.07, 0.07]|additive|Angular Velocity|[_−_1_._0_,_1_._0]<br>|
|Motor Strength|[0.8, 1.2]|scaling|DOF Position|[0_._2_×_default_,_1_._8_×_default]|
|Action Delay|[0, 5]|-|DOF Velocity|[_−_0_._2_,_0_._2]<br>|
|Link Mass|[0.7, 1.3]|scaling|Pitch Angle|[_−_0_._25_,_0_._25]<br>|
|Gravity|[-0.1, 0.1]|additive|Yaw Angle<br>Position|[_−_0_._4_,_0_._4]<br>[_−_2_,_2]|


range, with a dense cluster around the high-velocity value of 2 m/s. Regarding yaw velocity, most values fall within the commanded range. However, there are instances of high speed, with some even approaching 10 m/s. This may be due to the robot’s extreme behaviors when encountering unseen situations influenced by external forces and random noise. Regarding the roll-pitch velocity, the pitch velocity shows a higher degree of fluctuation. Similarly, in the roll pitch distribution, for pitch, there is a concentrated distribution at a pitch of 1 m/s, which is one of the terminal conditions. These two figures suggest that the robot is tripped by obstacles during its motion and thus terminates, for instance, when it hits steps or gravel during high-speed motion. 


Figure 8: Normal State: Policy rollout’s state distribution in the original learning environment 


Figure 9: Extreme State: Policy’s state distribution in the extreme cases 

### **A.8 History Length Experiments** 

We investigate the impact of observation history length on HWC-Loco’s performance. Setting _H_ = 10 achieves the best overall trade-off across the three metrics. While increasing _H_ beyond 10 slightly improves the success rate, it leads to a noticeable decline in goal-tracking accuracy and human-likeness. This suggests that excessively long history may hinder the effective use of privileged information, resulting in more conservative and less adaptive behaviors. 

Table 14: Performance comparison with different history lengths ( _H_ <u>)</u> 

|**History Length**|**Success Rate**_↑_|**Goal-tracking**_↑_|**Human-like**_↓_|
|---|---|---|---|
|1|95_._13_±_0_._51|1_._07_±_0_._00|3_._26_±_0_._06|
|10|96_._73_±_0_._40|**1**_._**10**_±_**0**_._**00**|**3**_._**18**_±_**0**_._**01**|
|20|96_._53_±_0_._40|1_._08_±_0_._00|3_._18_±_0_._02|
|40|**97**_._**38**_±_**0**_._**33**|1_._02_±_0_._00|3_._21_±_0_._02|


20 

### **A.9 Training Cost** 

All policies are trained on an NVIDIA RTX 4090 GPU with 4,096 parallel environments. Our framework involves training three policies. The goal-tracking policy converges within approximately 10000 iterations (nearly 10 hours), while the recovery policy requires around 8000 iterations to converge (nearly 8 hours). The high-level policy demonstrates faster convergence, requiring approximately 6000 iterations (under 6 hours). 

### **A.10 Deployment Details** 

We utilize the Unitree H1 humanoid robot as our deployment platform. This full-sized humanoid robot weighs 47 kg, stands approximately 1.8 meters tall, and features 19 degrees of freedom. The control frequency is set to 100 Hz for both simulation and real-world deployment. The PD gains, characterized by stiffness and damping values, used in the real-world deployment are detailed in Table 15. 

During deployment, inference operates through a hierarchical structure involving both high-level and low-level policies. To meet the strict latency and resource constraints of onboard systems, the policies are optimized for lightweight designs and exported JIT format. The high-level policy model size is below 2MB, and the low-level policies remain under 3MB. Those designs ensures that real-time inference at 100 Hz is feasible on the onboard computer of the Unitree H1 robot. 

Table 15: Stiffness, Damping and Torque Limit 

|Joint Names|Stiffness [N*m/rad]|Damping [N*m*s/rad]|Torque Limit (Nm)|
|---|---|---|---|
|hip yaw|200|5|170|
|hip roll|200|5|170|
|hip pitch|200|5|170|
|knee|300|6|255|
|ankle|40|2|34|
|torso|200|5|170|
|shoulder|30|1|34|
|elbow|30|1|18|


## **B Experiment** 

### **B.1 H1 Experiments** 

**Effectiveness Tests in the Real World.** Figure 10 demonstrates the robot’s ability to traverse a multi-terrain course consisting of 15 cm steps, 20° slopes, and wooden boards at a speed of 0.3 m/s. Figure 11 shows the ability to stability in real-world outdoor locomotion, including flat ground, grassy surfaces, and slopes. 


Figure 10: Climb Stairs Test. The blue segments indicate the activation of the goal-tracking policy, while the orange segments correspond to the safety recovery policy. 

**Robustness Tests in the Real World.** As shown in Figure 12, we apply various disturbances to Unitree H1 lasting for one minute. Four representative disturbance segments were selected for 

21 


Figure 11: Outdoor Deployment across Diverse Terrains: (a) flat ground, (b) grassy surface, (c) upward slope, and (d) downward slope. 

22 

analysis. The time is measured in control cycles, with each cycle lasting 0.01 seconds. Furthermore, we conduct an outdoor disturbance test by applying pushes, pulls, and kicks to the robot, as shown in Figure 13. The robot waves its arms and adjusts its gaits to maintain balance. Notably, the high control frequency (100 Hz) ensures smooth transitions between policies, and isolated activations of the recovery policy have minimal impact on overall stability. 


Figure 12: Disturbances in Realistic Deployment: Policy Switching value of 0 corresponds to the goal-tracking policy, while a value of 1 denotes the safety recovery policy. 


Figure 13: Robustness in Outdoor Settings: The robot responds to external disturbances in an outdoor environment by waving its arms and adjusting its gaits to maintain balance. 

**Case Study on Motion Tracking.** We visualize the robot’s performance in tracking a punching motion. During the execution, the robot experiences an impulse impact. In response, it dynamically activates the recovery policy, switching to more conservative and safer actions. Specifically, it lowers its body, adjusts its gait, and stabilizes itself to satisfy ZMP constraints, rather than strictly following 

23 

the original target motion. As a result, it generates a backtracking motion to maintain balance and ensure robustness. 


Figure 14: Robustness in Motion Tracking: The green dots represent the target keypoints, the blue dots indicate the keypoints corresponding to the DoFs, and the red dot denotes the ZMP. 

### **B.2 G1 Experiments** 

Table 16: Comparison of Humanoid Configurations 

|Parameter|H1|G1|
|---|---|---|
|Height|178 cm|127 cm|
|Mass|47 kg|35 kg|
|DoFs|19|23|


G1 outperforms H1 across all three metrics (success rate, goal-tracking accuracy, and human-likeness) primarily due to the following factors: 

- **Size and Mass:** As shown in Table 16, G1’s smaller size and lighter mass contribute to lower inertial loads and reduced torque demands. This facilitates greater stability, especially during dynamic motions, and enables faster corrective actions in response to disturbances. 

- **Degrees of Freedom (DoFs):** With 23 DoFs compared to H1’s 19, G1 offers enhanced joint-level flexibility. The additional DoFs, particularly in the upper body and feet, allow for better wholebody coordination. This increased redundancy leads to improved disturbance rejection and more human-like behavior during complex locomotion tasks. 

Notably, as illustrated in Figure 15, G1 is capable of achieving straight-knee walking, which remains a significant challenge for H1 due to its larger size and reduced agility. The additional DoFs in G1 enable finer control of limb trajectories, which is critical for maintaining balance during such biomechanically demanding gaits. 


Figure 15: G1 walk with straight knees 

24 

