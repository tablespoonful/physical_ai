---
title: "HUSKY: Humanoid Skateboarding System via Physics-Aware Whole-Body Control"
date: "2026-02-03"
authors: "Jinrui Han; Dewei Wang; Chenyun Zhang; Xinzhe Liu; Ping Luo; Chenjia Bai"
url: https://arxiv.org/abs/2602.03205
pdf: https://arxiv.org/pdf/2602.03205
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.03205)** / [論文ページ](https://arxiv.org/abs/2602.03205)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# HUSKY: Humanoid Skateboarding System via Physics-Aware Whole-Body Control 

Jinrui Han<sup>1,2*</sup> Dewei Wang<sup>1,3*</sup> Chenyun Zhang<sup>1</sup> Xinzhe Liu<sup>1,4</sup> Ping Luo<sup>2</sup> Chenjia Bai<sup>1†</sup> Xuelong Li<sup>1†</sup> 

> 1Institute of Artificial Intelligence (TeleAI), China Telecom 2The University of Hong Kong 

> 3University of Science and Technology of China 4ShanghaiTech University 

> _∗_ Equal contribution †Corresponding author 

Webpage: husky-humanoid.github.io Code: TeleHuman/humanoid_skateboarding 


**Fig. 1: Overview.** (a) Our proposed framework HUSKY enables the humanoid robot to perform complete real-world skateboarding, including pushing, steering, and phase transitions. (b) Generalization to diverse outdoor scenarios and skateboards with consistent stability and control. (c) Reliable indoor skateboarding performance. (d) Lean-to-steer behaviors achieved by exploiting robot body tilt. (e) Robustness against external disturbances. 

**_Abstract_ —While current humanoid whole-body control frameworks predominantly rely on the static environment assumptions, addressing tasks characterized by high dynamism and complex interactions presents a formidable challenge. In this paper, we address humanoid skateboarding, a highly challenging task requiring stable dynamic maneuvering on an underactuated wheeled platform. This integrated system is governed by nonholonomic constraints and tightly coupled human-object interactions. Successfully executing this task requires simultaneous mastery of hybrid contact dynamics and robust balance control on a mechanically coupled, dynamically unstable skateboard. To overcome the aforementioned challenges, we propose HUSKY, a learning-based framework that integrates humanoid-skateboard system modeling and physics-aware whole-body control. We first model the coupling relationship between board tilt and truck steering angles, enabling a principled analysis of system** 

**dynamics. Building upon this, HUSKY leverages Adversarial Motion Priors (AMP) to learn human-like pushing motions and employs a physics-guided, heading-oriented strategy for leanto-steer behaviors. Moreover, a trajectory-guided mechanism ensures smooth and stable transitions between pushing and steering. Experimental results on the Unitree G1 humanoid platform demonstrate that our framework enables stable and agile maneuvering on skateboards in real-world scenarios. More videos and code are available on our project page.** 

## I. INTRODUCTION 

Recent advancements in robotic hardware and control algorithms have enabled humanoid robots to perform a wide range of whole-body control tasks, including locomotion over complex terrains [28, 37, 20], dancing [12, 18, 41, 10], 

manipulation [4, 30, 31], and fall recovery [14, 15]. However, learning skateboarding skills for humanoid robots remains a highly challenging and largely unexplored problem. While existing approaches primarily focus on contact-rich wholebody control tasks [48, 43] and humanoid–object interaction scenarios [38, 39], humanoid skateboarding involves even more intricate contact dynamics and hybrid motion transitions. Furthermore, the shift from interacting with static objects to an underactuated wheeled platform challenges existing control frameworks, rendering them inadequate for stable humanoid skateboarding system. 

Traditional model-based approaches typically leverage simplified dynamic models for trajectory generation and Model Predictive Control (MPC) to synthesize skateboarding maneuvers for legged robots [32, 33, 42]. While these classical methodologies can generate controlled motions, the high computational cost of solving high-dimensional, non-convex optimization problems often precludes the real-time responsiveness required for dynamic skateboarding. Moreover, simplified models are insufficient to capture the complex non-holonomic and underactuated dynamics inherent to skateboarding, resulting in limited robustness to unmodeled physical effects and environmental variations. Although agile skateboarding skills can be achieved in simulation [22], they overlook physical hardware constraints and the sim-to-real gap, making direct real-world deployment highly challenging. 

Deep Reinforcement Learning (DRL) has recently emerged as a powerful alternative, leveraging large-scale parallel training to synthesize complex behaviors with minimal modeling assumptions and robust performance. Recent researches have demonstrated the effectiveness of RL in diverse tasks, from force-controlled interaction [49] and end-effector control [17] to quadrupedal skateboarding [19, 3] and humanoid roller skating [6], highlighting RL’s capacity to manage complex contact dynamics and stabilize high-speed, underactuated systems. 

However, humanoid skateboarding introduces substantially greater challenges due to the emergence of a tightly coupled, highly underactuated system. While the humanoid’s highdimensional state and action spaces already complicate wholebody control, this difficulty is compounded by the dynamic nature of the skateboard. The board’s motion, governed by intricate interactions between the wheels, ground, and the robot’s feet, creates a scenario where the robot must indirectly control its own moving support base. The inherent instability of this task becomes even more evident when compared to quadrupedal platforms. Unlike quadrupeds [19], humanoids possess significantly higher Degrees of Freedom (DoF) and an elevated Center of Mass (CoM), paired with a much smaller and more precarious support polygon. These physical constraints, combined with the need for complex leg reorientation and side-on steering maneuvers, result in highly nonlinear dynamics and severe sim-to-real discrepancies. Consequently, existing learning-based controllers that may succeed on simpler platforms struggle to maintain robust coordination here. Table I further highlights these unique structural and taskspecific difficulties. 

**TABLE I:** Comparison of Humanoid and Quadrupedal Skateboarding Tasks. 

|**Term**|**Humanoid (G1)**|**Quadruped (Go1)** [19]|
|---|---|---|
|Degrees of Freedom|23|12|
|Contact Points|1–2|2–4|
|CoM Height|0.6–0.8 _m_|0.2–0.3 _m_|
|Support Polygon|0.05–0.10 _m_<sup>2</sup>|0.10–0.15 _m_<sup>2</sup>|
|Side-on Steering|✓|_×_|
|Leg Reorientation|✓|_×_|


In this paper, we propose HUSKY, a physics-aware wholebody controller for **<u>hu</u>** <u>manoid</u> **<u>sk</u>** <u>ateboarding s</u> **<u>y</u>** <u>stem. HUSKY</u> first explicitly analyzes the coupled humanoid–skateboard system and derives an equality constraint between board tilt and truck steering angles, enabling physics-informed policy learning. The skateboarding task is formulated as a hybrid dynamical system with discrete contact phases, capturing the distinct pushing and steering behaviors inherent to skateboard locomotion. Based on this modeling, we employ DRL to train the humanoid to acquire the essential skateboarding skills, including propulsion through pushing and directional control through steering. To enhance the robustness and naturalness of pushing behaviors, HUSKY leverages Adversarial Motion Priors (AMP) [27] to guide the policy toward human-like propulsion motions. Steering is achieved through a physicsaware strategy that exploits the intrinsic coupling between humanoid body lean and skateboard truck steering. To facilitate exploration across distinct phases and ensure smooth transitions, HUSKY integrates a trajectory planning mechanism that stabilizes transitions between pushing and steering, resulting in continuous and coordinated skateboarding behaviors. 

Taken together, HUSKY enables the humanoid to achieve agile, stable skateboarding maneuvers, as validated in both simulation and real-world experiments. Our main contributions are summarized as follows: 

- We model the humanoid skateboarding system by explicitly incorporating the tilt–steering constraint and formulate the skateboarding task as a hybrid dynamical system characterized by distinct contact phases. 

- We develop a learning-based whole-body control framework that integrates AMP-based pushing, physics-guided steering, and trajectory planning for phase transitions. 

- We validate HUSKY in both simulation and real-world experiments, demonstrating agile, stable, and human-like humanoid skateboarding maneuvers. 

## II. RELATED WORK 

## _A. Learning-based Humanoid Whole-Body Control_ 

Recent advances in learning-based humanoid whole-body control have enabled robots to tackle complex control tasks, leveraging state-of-the-art algorithms and high-fidelity simulators [45, 23, 21]. Existing research primarily focuses on locomotion [28, 7], motion tracking [26, 12], and teleoperation [11, 46, 47]. These approaches have achieved robust blind locomotion over uneven terrains [8, 40], highly dynamic motion tracking [41, 10], agile parkour [50], and complex 

manipulation tasks [5]. To enhance environmental perception and reactive capabilities, many studies have incorporated exteroceptive sensors such as LiDAR and depth cameras, enabling more sophisticated terrain traversal [37, 20, 1] and object interaction [38, 39, 49]. Our work further investigates the task of humanoid skateboarding, which demands significantly higher levels of control agility and whole-body coordination. 

## _B. Legged Robots on Dynamic Platforms_ 

The interaction between legged robots and dynamic platforms poses significant challenges. Model-based approaches have enabled quadrupedal robots to perform skateboarding through offline trajectory optimization [42]. Learning-based methods further allow quadrupeds to acquire more robust skateboarding skills, including mounting [3] and maneuvering the board [19]. By simulating dynamic platform motion in virtual environments, Huang et al. [13] demonstrated effective balance control across a variety of unstable surfaces. 

Humanoid skateboarding, however, remains especially demanding for model-based frameworks [33, 32, 22], as it requires agile, real-time control and highly accurate physical modeling [36, 16]. In contrast, while RL has shown great potential for enabling robust and dexterous humanoid behaviors in other domains [2, 9], its application to skateboarding remains largely unexplored. Our framework leverages these capabilities to realize learning-based agile skateboarding skills on a humanoid robot in the real world. 

## III. HUMANOID-SKATEBOARD SYSTEM 

## _A. System Modeling_ 

We consider a humanoid robot interacting with a fully passive articulated skateboard via foot contacts, with all actuation provided by the humanoid. As illustrated in Fig. 2, the skateboard comprises three main components: the deck, trucks, and wheels. The deck supports the humanoid’s weight and transmits forces to the trucks, which connect the deck to the wheels. In real skateboards, the trucks use a kingpin-based suspension with elastic bushings, which converts deck tilting into truck steering while providing force damping. While directly modeling the full suspension in simulation is challenging due to its structural complexity and compliance. Therefore, we adopt a simplified kinematic model that preserves the key lean-to-steer behavior while remaining tractable for control and simulation. 

Under this formulation, wheel–ground contacts are modeled as non-holonomic rolling constraints that restrict lateral slip. Instead of explicitly resolving the constraint forces, we exploit the truck geometry to relate the board tilt angle _γ_ to the rotation of the truck axes. Due to the mechanical structure of the trucks, tilting the board by _γ_ induces a coordinated rotation of the truck axes, resulting in a kinematic coupling [36] described by: 


where _λ_ is the constant rake angle of the skateboard, and _σ_ is the resulting truck steering angle. Intuitively, this implies 


**Fig. 2: Skateboard Model.** We analyze the skateboard kinematic structure and derive the coupling relationships among the board tilt, truck steering, and rake angles, which form the basis of the lean-to-steer behavior. 

that the truck steering angle is determined by the board tilt angle, with larger tilts producing greater steering deflections. Detailed derivation is provided in Appendix A. 

This abstraction directly links board tilt to truck steering, capturing the essential equality constraint of humanoid-driven maneuvers while avoiding unnecessary mechanical redundancies. The resulting model is both computationally efficient and physically representative, providing a tractable foundation for subsequent control and learning of humanoid skateboarding. 

## _B. Humanoid Skateboarding Task_ 

We formulate humanoid skateboarding as a hybrid control task, comprising two periodically recurring phases, _pushing_ and _steering_ , which arise from discrete changes in the system’s contact topology. Each phase is governed by distinct dynamics and control objectives. The framework is shown in Fig. 3. 

During the pushing phase (Section IV-B), one foot of the humanoid maintains contact with the skateboard to stabilize the body, while the other intermittently contacts the ground to generate propulsion. Forward motion is produced by tangential ground reaction forces at the pushing foot, whereas the supporting foot ensures balance on the moving board. 

In the steering phase (Section IV-C), both feet of the humanoid remain on the skateboard, producing a passive gliding motion. Steering is achieved by modulating the board tilt through body leaning, which induces truck rotation and allows the humanoid to follow a desired heading. 

While transitions between pushing and steering are challenging due to the distinct dynamics and control objectives of each phase. In Section IV-D, we describe strategies to explicitly bridge these phases, enabling smooth and stable phase transitions during humanoid skateboarding. 


**Fig. 3: Framework of HUSKY.** (a) We first analyze and model the humanoid–skateboard system, deriving a physics-inspired lean-to-steer coupling mechanism. Due to the distinct contact dynamics and control objectives across skateboarding phases, we adopt a phase-wise learning strategy. (b) The learning-based whole-body control framework integrates an AMP-based pushing style for active forward propulsion, a steering strategy guided by kinematics-aware tilt references, and a trajectory-guided transition mechanism to enable stable switching between pushing and steering phases. 

## IV. METHOD 

## _A. Problem Formulation_ 

In this work, we adopt the Unitree G1 humanoid robot [35] with 23 controllable degrees of freedom (DoF), excluding the three DoFs of each wrist. We formulate the humanoid skateboarding task as a RL problem, in which the agent interacts with the environment through a policy _π_ to maximize cumulative reward. At each timestep _t_ , the policy receives the state **_s_** _t_ and outputs an action **_a_** _t ∈_ R<sup>23</sup> , which is subsequently mapped to motor torques via a PD controller. This defines the policy as _π_ ( **_a_** _t|_ **_s_** _t_ ). The environment dynamics _p_ ( **_s_** _t_ +1 _|_ **_s_** _t,_ **_a_** _t_ ) determine the next state, while a dense reward _r_ ( **_s_** _t,_ **_a_** _t_ ) evaluates skateboarding performance while providing regularization. The agent aims to maximize the expected return _J_ = E _t_ =0<sup>_βtrt_</sup> , where _β_ denotes the discount factor. �� _T −_ 1 � We utilize an asymmetric actor–critic framework for policy training, where the actor observes only proprioceptive information, while the critic has access to additional privileged information. At each timestep _t_ , the policy state **_s_** _t_ consists of a short history of proprioceptive states **_o_**<sup>prop</sup> _t−_ 4: _t_<sup>,whereeach</sup> proprioceptive state **_o_**<sup>prop</sup> _t ∈_ R<sup>78</sup> is defined as 


where **_c_** _t_ = [ _vcmd, ψ_ ] _∈_ R<sup>2</sup> contains the desired skateboard forward velocity _vcmd_ and heading target _ψ_ , **_ω_** _t ∈_ R<sup>3</sup> is the base angular velocity, **_g_** _t ∈_ R<sup>3</sup> is the base projected gravity, **_θ_** _t ∈_ R<sup>23</sup> and **_θ_**<sup>˙</sup> _t ∈_ R<sup>23</sup> are the joint angles and velocities, and **_a_** _t−_ 1 _∈_ R<sup>23</sup> is the previous action. The phase cycle is represented by a normalized variable Φ = ( _t_ mod _H_ ) _/H ∈_ [0 _,_ 1), where _H_ is the cycle duration. This periodic variable governs transitions between pushing and steering phases, serving as a temporal reference for the policy. 

To expose the skateboard state to the critic during training, we define the privileged observation **_o_**<sup>priv</sup> _t_ as 


where **_v_** _t ∈_ R<sup>3</sup> denotes the robot base linear velocity, **_p_**<sup>_b_</sup> _t_<sup>_∈_R3,</sup> **_r_** _t_<sup>_b∈_R6,</sup><sup>**_v_**</sup> _t_<sup>_b∈_R3and</sup><sup>**_ω_**</sup> _t_<sup>_b∈_R3representtheskateboardbase</sup> position, orientation, linear velocity and angular velocity in the robot’s frame, respectively. **_θ_** _t_<sup>_b∈_R3is the skateboard’s tilt and</sup> truck joint angles, while **_f_** _t_<sup>_g∈_R6and</sup><sup>**_f_**</sup><sup>_b_</sup> _t_<sup>_∈_R6representthe</sup> humanoid’s feet contact forces with ground and skateboard, respectively. To guide the humanoid toward the desired behaviors in each phase, we detail phase-specific reward functions in Appendix C. The overall reward is formulated as: 


where I<sup>push</sup> , I<sup>steer</sup> , and I<sup>trans</sup> are binary indicators denoting the current contact phase, and _rt_<sup>reg</sup> is a global regularization term. 

## _B. Adversarial Motion Prior for Pushing Style_ 

During the pushing phase, the primary objective is to achieve a target skateboard velocity _vcmd_ by generating physically plausible propulsion through intermittent foot-ground contacts. Traditional reference-tracking methods enforce strict adherence to predefined joint trajectories [26], resulting in rigid behaviors that limit adaptation to varying environments and velocity demands. To encourage more natural and robust behaviors, we build on the AMP framework, which employs a discriminator _Dϕ_ to distinguish policy rollouts from reference human pushing motions. 

The AMP observation is defined as the robot joint angles **_o_**<sup>amp</sup> _t_ = _θt ∈_ R<sup>23</sup> . To provide the discriminator with temporal context, we construct a motion window _τt_ = _{_ **_o_**<sup>amp</sup> _t−_ 3<sup>_, . . . ,_</sup><sup>**_o_**amp</sup> _t_ +1<sup>_}_</sup> spanning five timesteps. Reference transitions are sampled from a human motion dataset _M_ , while generated transitions are collected from the current policy rollouts _P_ . 

The discriminator is trained to distinguish between expert and agent motions using a least-squares loss, augmented with 

a gradient penalty to promote training stability: 


The discriminator output _d_ = _Dϕ_ ( _τt_ ) is then mapped to a bounded style reward: 


where _α_ is a scaling coefficient. The total reward for the pushing phase combines task-specific and style components: 


Here, _rt_<sup>task</sup> encourages accurate tracking of the commanded skateboard velocity, while _rt_<sup>style</sup> guides the humanoid to exhibit human-like pushing behaviors. 

## _C. Kinematics-Guided Heading-Oriented Steering_ 

In the steering phase, the humanoid receives a target heading command _ψ_ and leans its body to induce a board tilt _γ_ , which, through the truck geometry coupling in Eq. (1), produces the corresponding truck steering angle _σ_ and achieves the desired turning behavior. To exploit this physical coupling, we provide the humanoid with a kinematics-guided reference specifying the desired board tilt angle for heading regulation. 

Assuming a planar kinematic model of the skateboard, we adopt a bicycle-model approximation commonly used in vehicle dynamics [44], which captures the yaw motion of the skateboard while neglecting lateral slip and vertical dynamics. Under this formulation, the yaw rate _ψ_<sup>˙</sup> is given by: 


where _v_ is the forward velocity of the skateboard in its base frame, and _L_ is the wheelbase. Combining this with the leanto-steer relationship in Eq. (1), we obtain 


which links the board tilt angle _γ_ to the resulting yaw rate. 

Given a desired heading change ∆ _ψ_ = _ψ − ψ_ board over a steering horizon ∆ _t_ , where _ψ_ board denotes the current heading of the skateboard, we assume a constant yaw rate _ψ_<sup>˙</sup> _≈_ ∆ _ψ/_ ∆ _t_ to achieve a smooth and gradual turn. Substituting this into Eq. (9) yields the kinematics-guided tilt reference: 


where _γ_ ref represents the desired board tilt angle that minimizes the heading error. To ensure numerical stability at low speeds or large desired turns, we clip _v_ to a minimum threshold and constrain _γ_ ref within feasible lean limits. 

We define a tilt reward to guide the policy toward this physically consistent lean: 


where _σγ_ sets the tolerance. This is combined with a headingtracking reward _r_ heading = exp( _−_ (∆ _ψ_ )<sup>2</sup> _/σψ_<sup>2),ensuringthat</sup> the policy aligns the skateboard with the target direction while maintaining a physically feasible lean angle. 

To further promote balance and stable foot placement during steering, two virtual markers are defined above the skateboard trucks. These markers indicate preferred feet contact locations, and the policy is encouraged to place the feet close to them, providing auxiliary guidance for the humanoid’s stance. 

## _D. Trajectory Planning for Phase Transition_ 

Direct transitions between the pushing and steering phases are challenging due to differences in body poses, contact dynamics, and learning objectives. Policies trained without explicit transition guidance often fail to explore new contact phases, which can lead to convergence to local optima [48]. 

To address this problem, we introduce a _trajectory-guided transition_ mechanism that explicitly bridges the pushing and steering phases by generating intermediate reference states. Specifically, we select a set of key bodies, denoted by _K_ , which capture the humanoid’s essential motion during phase transitions. The positions and orientations of these key bodies relative to the skateboard are then used to plan smooth and physically consistent transition trajectories. 

At the end of the current phase, the humanoid’s key body poses ( **_p_**<sup>_K_</sup> end<sup>_,_</sup><sup>**_q_**</sup> end<sup>_K_)areobtainedonlineandserveastheinitial</sup> condition for trajectory planning. Unlike predefined motions, these terminal poses vary across episodes and policies, resulting in a state-dependent transition problem. For each phase, we also define a canonical stable pose ( **_p_**<sup>_K_</sup> ref<sup>_,_</sup><sup>**_q_**</sup> ref<sup>_K_)relativetotheskateboardframe,representingthe</sup> nominal start configuration of the subsequent phase. The transition is therefore formulated as a trajectory connecting the online terminal pose of the current phase to the fixed reference pose of the next phase. For example, the end pose of the pushing phase is planned toward the steering phase reference pose, and vice versa. 

For body translations, the planned Cartesian position at timestep _t_ is generated using an _n_ -th order B´ezier curve: 


where **_p_**<sup>_K_</sup> 0 = **_p_**<sup>_K_</sup> end<sup>and</sup><sup>**_p_**</sup> _n_<sup>_K_</sup> = **_p_**<sup>_K_</sup> ref<sup>denotetheinitialand</sup> target positions, and _{_ **_p_**<sup>_K_</sup> _i_<sup>_}n_</sup> _i_ =1<sup>_−_1areintermediatecontrolpoints</sup> shaping the trajectory. Here, _t_ 0 and _tf_ are the start and end times of the transition. 

Boy orientations are interpolated using spherical linear interpolation (slerp) between quaternions: 


where _s_ = _ttf− −tt_ <u>00</u><sup>andΩ=arccos(</sup><sup>_⟨_</sup><sup>**_q_**</sup> end<sup>_K,_</sup><sup>**_q_**</sup> ref<sup>_K⟩_)istheangular</sup> distance between the quaternions. This ensures smooth and physically consistent orientation transitions while stepping onto or off the skateboard. 

At each transitional timestep _t_ , the policy receives a tracking reward that encourages it to follow the planned trajectories ( **_p_**<sup>_K_</sup> ( _t_ ) _,_ **_q_**<sup>_K_</sup> ( _t_ )). This trajectory-guided guidance shapes the exploration space, enabling reliable phase switching while retaining sufficient flexibility for the policy to adapt to dynamic interactions. By integrating trajectory-guided transitions with phase-specific learning objectives, the humanoid achieves stable and repeatable transitions between pushing and steering, facilitating consecutive skateboarding behaviors. 

## _E. Sim-to-Real Transfer_ 

_1) Skateboard Physical Identification:_ To bridge the simto-real gap, we identify an equivalent PD model for the skateboard’s passive tilt dynamics (back view of Fig. 2) through a sequential analytical identification procedure based on its free-decay roll response [24]. Specifically, the skateboard is perturbed in roll and released, allowing the truck bushings and pivot friction to produce a naturally decaying oscillation. We first quantify energy dissipation by measuring two successive roll angle peaks, _ϕ_ ( _t_ ) and _ϕ_ ( _t_ + _T_ ). The logarithmic decrement _δ_ and the corresponding damping ratio _ζ_ are computed as 


where _T_ is the observed oscillation period. This damping ratio captures the intrinsic dissipative effects of the truck bushings and pivot interfaces. Given the identified _ζ_ , we estimate the equivalent torsional stiffness of the truck assembly by matching the observed roll oscillation frequency. The undamped natural frequency is computed as: 


where _ωd_ = 2 _π/T_ is the damped frequency. Approximating the skateboard’s roll inertia _I_ using a rigid cuboid model dominated by the deck geometry, the torsional stiffness is identified as _k_ = _Iωn_<sup>2,whichrepresentstherestorativetorque</sup> generated by the bushings under roll deformation. Finally, the velocity-dependent damping coefficient is obtained as _d_ = 2 _ζ_ _~~√~~ kI_ , modeling the dissipative torque arising from bushing hysteresis and pivot friction. Embedding the identified parameters ( _k, d_ ) into simulation yields a physically grounded tilt spring–damper model that faithfully reproduces the passive truck mechanics observed on the real skateboard. 

_2) Domain Randomization:_ To further improve policy robustness and facilitate effective sim-to-real transfer, we employ domain randomization (DR) during training. The detailed configurations are provided in Table II. 

V. EXPERIMENTS 

## _A. Experiment Setup_ 

In simulation, we use a standard 80 _cm ×_ 20 _cm ×_ 12 _cm_ skateboard model, the coupling mechanism in Eq. (1) is 

**TABLE II:** Domain Randomization Parameters. 

|**DR terms**|**Range**|Unit|
|---|---|---|
|Robot Center of Mass|_U_(_−_2_._5_,_ 2_._5)|_cm_|
|Skateboard Center of Mass|_U_(_−_2_._5_,_ 2_._5)|_cm_|
|Default Root Position|_U_(_−_2_._0_,_ 2_._0)|_cm_|
|Default Joint Position|_U_(_−_0_._01_,_ 0_._01)|_rad_|
|Push Robot Base|_U_(_−_0_._5_,_ 0_._5)|_m/s_|
|Robot Body Friction|_U_(0_._3_,_ 1_._6)|-|
|Skateboard Deck Friction|_U_(0_._8_,_ 2_._0)|-|


embedded into the simulator as an equivalent constraint. The details of skateboard model are provided in Appendix B. All trainings and evaluations are implemented in mjlab [45], which integrates MuJoCo physics [34] with the IsaacLab API [23]. Humanoid skateboarding policies are trained using the PPO [29] algorithm across 4,096 parallel environments, with each episode lasting 20 seconds. For each experiment, we evaluate 1,000 rollout episodes in simulation and report results over five random seeds. Additional training details are given in Appendix D. In real-world experiments, the policy is deployed on a Unitree G1 humanoid robot at 50 Hz, with joint positions tracked by a 500 Hz PD controller. 

_1) Evaluation Metrics:_ We adopt the following metrics to evaluate the humanoid skateboarding performance: 

   - **Task success rate** ( _E_ succ): Defined as the percentage of episodes completed without termination. 

   - **Velocity tracking error** ( _E_ vel): Measured as the mean absolute error between the commanded velocity _v_ cmd and the actual skateboard forward velocity _v_ board during the pushing phase: _E_ vel = E [ _|v_ cmd _− v_ board _|_ ]. 

   - **Heading tracking error** ( _E_ yaw): Quantifies the accuracy of heading control during steering phase using the heading error: _E_ yaw = E [ _|ψ − ψ_ board _|_ ]. 

   - **Motion smoothness** ( _E_ smth): Evaluated by aggregating joint angle variations across consecutive control steps, promoting temporally smooth and plausible behaviors. 

   - **Contact error** ( _E_ contact): Defined as the per-step violation of the foot–board contact pattern, i.e., single-foot contact during pushing and double-foot contact during steering. 

- _2) Baselines:_ To evaluate the effectiveness of HUSKY, we 

- compare it with the following ablated baseline variants: 

   - **Pushing style** : We consider two baselines: (i) a **_Trackingbased_** variant [26] that directly tracks reference skateboarding motions from _M_ , and (ii) a **_Gait-based_** variant [25] in which the humanoid’s pushing follows a fixed gait schedule. 

   - **Steering strategy** : We compare our steering design with a **_w/o Tilt Guidance_** baseline, where the policy implicitly learn board tilt angles for steering without physics-guided tilt reference. 

   - **Transition mechanism** : We evaluate three variants: (i) **_AMP Transition_** , which uses phase-specific reference motions, including stepping onto and off the skateboard, and relies on style rewards to guide transitions, (ii) **_Translation-only_** , which guides only translational motion while ignoring orientation, underscoring the importance 

**TABLE III:** Simulation Results. 

|**Method**|_E_succ_↑_|_E_vel_↓_|_E_yaw_↓_|_E_smth_↓_|_E_contact_↓_|
|---|---|---|---|---|---|
|**Ablation on Pushing Style**||||||
|HUSKY-Tracking-Based|11_._12_±_3_._86|0_._435_±_0_._101|0_._568_±_0_._092|0_._044_±_0_._025|0_._015_±_0_._010|
|HUSKY-Gait-Based|82_._38_±_7_._25|0_._102_±_0_._035|0_._302_±_0_._041|0_._043_±_0_._011|0_._130_±_0_._072|
|HUSKY (ours)|**100.00**_±_0_._00|**0.056**_±_0_._013|**0.208**_±_0_._014|**0.033**_±_0_._005|**0.001**_±_0_._001|
|**Ablation on Steering Strategy**||||||
|HUSKY-w/o-Tilt Guidance|96_._72_±_2_._10|0_._071_±_0_._010|0_._233_±_0_._027|0_._035_±_0_._017|0_._002_±_0_._002|
|HUSKY (ours)|**100.00**_±_0_._00|**0.056**_±_0_._013|**0.208**_±_0_._014|**0.033**_±_0_._005|**0.001**_±_0_._001|
|**Ablation on Transition Mech**|**anism**|||||
|HUSKY-AMP Transition|85_._12_±_4_._11|**0.053**_±_0_._025|0_._265_±_0_._050|0_._040_±_0_._007|0_._394_±_0_._015|
|HUSKY-Translation-only|89_._55_±_2_._30|0_._064_±_0_._020|0_._294_±_0_._075|0_._039_±_0_._012|0_._038_±_0_._012|
|HUSKY-Mixed Initialization|86_._03_±_1_._70|0_._067_±_0_._024|0_._278_±_0_._092|0_._037_±_0_._015|0_._371_±_0_._025|
|HUSKY (ours)|**100.00**_±_0_._00|0_._056_±_0_._013|**0.208**_±_0_._014|**0.033**_±_0_._005|**0.001**_±_0_._001|


of jointly controlling both position and rotation during phase transitions, and (iii) **_Mixed Initialization_** [19] utilizes a balanced 50/50 mixture of pushing and steering phases during reset to facilitate comprehensive phase exploration. 

## _B. Main Results_ 

Table III summarizes the overall performance of HUSKY compared to the baselines across metrics. These results demonstrate that HUSKY enables robust humanoid skateboarding with stable, accurate, smooth motions and continuous, reliable phase transitions. The contributions of the key design choices are summarized as follows: 

**AMP enables flexible and natural pushing.** For pushing, the _Tracking-based_ baseline strictly follows reference motions, limiting its adaptability to varying contact timings and velocities and leading to the lowest success rate. The _Gait-based_ baseline, lacking human motion priors, produces less smooth motions and higher contact errors, reflecting its difficulty in generating coordinated, human-like pushing behaviors. 

**Physics-guided steering enhances heading control.** For steering, the _w/o Tilt Guidance_ baseline learns board tilt angles implicitly, which reduces heading accuracy and highlights the importance of explicitly incorporating the lean-to-steer coupling for precise directional control. 

**Trajectory guidance is essential for phase transitions.** For phase transitions, the _AMP Transition_ baseline, which relies solely on full reference motions, achieves moderate success rates but incurs significant contact errors, as the robot fails to explore proper phase switching. The _Translation-only_ baseline, which guides translation while omitting orientation alignment, exhibits poor heading tracking, causing the robot to align with the board direction rather than adopt a side-on posture and making steering control difficult. 

## _C. More Analysis_ 

**Skateboard Modeling (Fig. 4).** We validate the effect of skateboard modeling and visualize the resulting steering trajectories in Fig. 4 (a). Similar to prior simplified models [19], omitting the equality constraint in Eq. (1) prevents board tilting 


**Fig. 4: Steering Trajectories Visualizations.** (a) Omitting lean-to-steer coupling prevents effective steering. (b) Incorporating physics-guided tilt guidance substantially increases the reachable heading range and precision. 

from inducing truck steering, leaving the skateboard able only to glide straight forward with negligible turning capability. 

Fig. 4 (b) compares policies trained without tilt guidance under identical steering commands by measuring the range of reachable headings. Without tilt guidance, the achievable heading range is narrow. In contrast, incorporating tilt guidance produces smooth turning trajectories and enables the humanoid to reach a substantially wider range of headings with higher precision. These results demonstrate that tilt guidance is essential for effective and precise turning control. 

**Phase Exploration (Fig. 5).** To further analyze the necessity of transition guidance, we train policies without it under two settings: (i) all episodes are initialized to start in the pushing phase, matching our setup, and (ii) a 50/50 mixture of pushing and steering phases, as used in prior work [19] to promote phase exploration. We measure episode length and a steering contact reward, which encourages double-foot board contact and penalizes ground contact during steering. 

In both settings, episode length increases rapidly during early training, yet the steering contact reward remains low, indicating persistent incorrect foot–board contact patterns. This suggests that policies trained without transition guidance fail to learn phase transitions, collapsing to a trivial pushingonly behavior and failing to properly execute the steering phase, even under mixed initialization. In contrast, HUSKY discovers correct contact patterns by mid-training, successfully learns foot-mounting transitions, and achieves higher rewards, demonstrating that trajectory-guided transitions are essential 


**Fig. 5: Training Performance Comparison.** Episode length (left) and steering contact reward (right). Without transition guidance, the policy fails to maintain correct foot–board contacts. In contrast, the policy discovers correct contact patterns early in training and establishes stable phase transitions. 


**Fig. 6: Transition trajectories analysis.** Representative trajectories during phase transitions. The humanoid maintains smooth, coordinated whole-body motions, with seamless transitions between pushing and steering. 

for enabling phase switching and avoiding local optima. 

**Trajectories Analysis (Fig. 6).** We further examine the humanoid’s skateboarding transitions by analyzing collected trajectory sequences. As shown in Fig. 6, the robot maintains smooth, coordinated whole-body motions with seamless transitions between pushing and steering. The trajectories display consistent foot placement and gradual body pose adjustments, reflecting strong temporal coherence and physical plausibility enabled by our trajectory-guided transitions. 

## _D. Real-World Experiments_ 

_1) Overall Performance:_ Overall, Fig. 1 and the supplementary videos demonstrate that HUSKY achieves robust real-world skateboarding across diverse conditions. The system executes complete skateboarding behaviors including pushing, steering, and phase transitions, generalizes to different skateboard platforms, and performs reliably in both indoor and outdoor environments. Lean-to-steer control emerges naturally through body tilting, enabling heading regulation. The humanoid maintains smooth and coordinated foot placements during transitions, withstands external disturbances, and sustains multiple continuous skateboarding cycles. 


**Fig. 7: Details of feet motions during transitions.** The humanoid pushes off the ground, mounts the skateboard, and adjusts orientation on the board. 


**Fig. 8: Effect of Skateboard Physical Identification.** (a) Applying the compliant board parameters to the stiff board prevents mounting, as the real stiff board does not tilt under the robot’s step. (b) Applying the stiff board parameters to the compliant board causes over-leaning and loss of stability during steering. 

_2) Transition Details:_ We analyze the transitions from pushing to steering, focusing on detailed humanoid feet motion. In Fig. 7, the transition begins with the foot pushing against the ground to generate propulsion, followed by lifting and placing the foot onto the skateboard. Once on the board, the humanoid performs in-place adjustments, rotating the body to align the torso perpendicular to the skateboard deck, thereby facilitating stable steering. These motions closely match human behaviors and are consistent with our simulation data. 

To account for the high friction of real skateboard decks, we apply DR during training, varying friction parameters to improve sim-to-real transfer of foot-mounting and bodyalignment behaviors. 

_3) Role of System Identification:_ We evaluate the importance of skateboard system identification by focusing on the board’s tilt compliance, which determines how readily the board responds to humanoid leaning. Experiments are conducted using two skateboards with distinct tilt stiffness: one stiffer (black) and one more compliant (pink). As shown in Fig. 1 (a) and (b), when using the identified parameters corresponding to each physical board, the robot successfully performs push-and-steer maneuvers and achieves smooth board mounting and dismounting. 

Cross-applying the identified parameters reveals the limitations of mismatched system models. In Fig. 8 (a), when using parameters identified from the compliant board on the stiffer board, the robot fails to mount. In simulation, the board 

tilts under the robot’s stepping motion, allowing the policy to exploit this compliance for mounting, whereas the real stiff board remains nearly flat, breaking this assumption and preventing successful mounting. Conversely, in Fig. 8 (b), applying the stiff-board parameters to the compliant board causes excessive leaning and loss of stability during steering, since the policy is not trained for such compliant dynamics. These results highlight that accurate identification of board tilt compliance is critical for sim-to-real transfer of humanoid skateboarding policies. 

## VI. CONCLUSION AND FUTURE WORK 

In this work, we present HUSKY, a physics-aware learning framework that enables humanoid robots to perform agile skateboarding with active propulsion and lean-to-steer control. By modeling the coupled humanoid–skateboard dynamics and explicitly capturing the relationship between board tilt and truck steering, we decompose the task into pushing, steering, and transition phases and develop phase-specific learning strategies. We further introduce a trajectory-guided transition mechanism to enable smooth and reliable phase switching, which is critical for long-horizon stability. Extensive simulation and real-world experiments demonstrate that HUSKY enables continuous and robust skateboarding behaviors on the Unitree G1 humanoid robot platform. 

We emphasize that HUSKY is a principled paradigm with utility beyond skateboarding. Its core mechanisms—kinematic coupling for underactuated tools and transitions between contact topologies—extend to broader tasks. Despite strong simulation and real-world performance, several limitations remain and warrant future investigation. 

**Perception Integration.** The limited camera field of view prevents reliable observation of the board and wheel–ground interactions, restricting perception-driven feedback in the control loop. Incorporating visual state estimation is important for enabling perception-aware skateboarding control. 

**Complex Terrains.** Current experiments are conducted on relatively simple terrains, whereas human skateboarders routinely perform in complex environments such as skateparks while executing acrobatic maneuvers. Extending our framework to such scenarios will require richer motion priors and terrain-adaptive control strategies. 

## ACKNOWLEDGMENTS 

Our training pipeline builds on mjlab [45], we gratefully acknowledge the open-source communities and contributors behind the frameworks, and thank Unitree Robotics [35] for their support of the humanoid hardware used in this work. 

## REFERENCES 

- [1] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. In _Proceedings of The Conference on Robot_ 

_Learning_ , Proceedings of Machine Learning Research, 2025. 

- [2] Hongjun An, Wenhan Hu, Sida Huang, Siqi Huang, Ruanjun Li, Yuanzhi Liang, Jiawei Shao, Yiliang Song, Zihan Wang, Cheng Yuan, et al. Ai flow: Perspectives, scenarios, and approaches. _Vicinagearth_ , 3(1):1, 2026. 

- [3] Danil Belov, Artem Erkhov, Elizaveta Pestova, Ilya Osokin, Dzmitry Tsetserukou, and Pavel Osinenko. Quadrupedal robot skateboard mounting via reverse curriculum learning. _arXiv preprint arXiv:2505.06561_ , 2025. 

- [4] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid locomanipulation with isomorphic exoskeleton cockpit. In _Robotics: Science and Systems_ , 2025. 

- [5] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. Humanplus: Humanoid shadowing and imitation from humans. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [6] Junchi Gu, Feiyang Yuan, Weize Shi, Tianchen Huang, Haopeng Zhang, Xiaohu Zhang, Yu Wang, Wei Gao, and Shiwu Zhang. Skater: Synthesized kinematics for advanced traversing efficiency on a humanoid robot via roller skate swizzles. _arXiv preprint arXiv:2601.04948_ , 2026. 

- [7] Xinyang Gu, Yen-Jen Wang, and Jianyu Chen. Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer. _arXiv preprint arXiv:2404.05695_ , 2024. 

- [8] Xinyang Gu, Yen-Jen Wang, Xiang Zhu, Chengming Shi, Yanjiang Guo, Yichen Liu, and Jianyu Chen. Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning. In _Robotics: Science and Systems_ , 2024. 

- [9] Zhaoyuan Gu, Junheng Li, Wenlan Shen, Wenhao Yu, Zhaoming Xie, Stephen McCrory, Xianyi Cheng, Abdulaziz Shamsah, Robert Griffin, C Karen Liu, et al. Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. _IEEE/ASME Transactions on Mechatronics_ , 31(2):2300– 2330, 2026. 

- [10] Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. Kungfubot2: Learning versatile motion skills for humanoid wholebody control. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2026. 

- [11] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris M. Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. In _8th Annual Conference on Robot Learning_ , 2024. 

- [12] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbabu, Chaoyi Pan, Zeji Yi, Guannan Qu, Kris Kitani, Jessica Hodgins, Linxi ”Jim” Fan, Yuke Zhu, Changliu Liu, and Guanya Shi. Asap: Aligning simula- 

tion and real-world physics for learning agile humanoid whole-body skills. _Robotics: Science and Systems_ , 2025. 

- [13] Kaihui Huang, Heming Feng, Wei Meng, Tianqi Wei, and Tianjiang Hu. Learning-based quadruped robot framework for locomotion on dynamic rigid platforms. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 17746–17753. IEEE, 2025. 

- [14] Tao Huang, Junli Ren, Huayi Wang, Zirui Wang, Qingwei Ben, Muning Wen, Xiao Chen, Jianan Li, and Jiangmiao Pang. Learning humanoid standingup control across diverse postures. _arXiv preprint arXiv:2502.08378_ , 2025. 

- [15] Heejin Jeong and Daniel D Lee. Efficient learning of stand-up motion for humanoid robots with bilateral symmetry. In _2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1544– 1549. IEEE, 2016. 

- [16] Alexander S Kuleshov. Mathematical model of the skateboard. In _ISBS-Conference Proceedings Archive_ , 2006. 

- [17] Yitang Li, Yuanhang Zhang, Wenli Xiao, Chaoyi Pan, Haoyang Weng, Guanqi He, Tairan He, and Guanya Shi. Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control, 2025. URL https: //arxiv.org/abs/2505.24198. 

- [18] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [19] Hang Liu, Sangli Teng, Ben Liu, Wei Zhang, and Maani Ghaffari. Discrete-time hybrid automata learning: Legged locomotion meets skateboarding. _arXiv preprint arXiv:2503.01842_ , 2025. 

- [20] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao Huang, Ping Luo, and Jiangmiao Pang. Learning humanoid locomotion with perceptive internal model. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9997–10003. IEEE, 2025. 

- [21] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [22] Elias Mikkola. Online planning and control of physics-based skateboarding animation. Master’s thesis, Aalto University, School of Science, 2023. URL https://aaltodoc.aalto.fi/items/ 3d76eb38-cedf-473b-b19f-e6e9d604215b. 

- [23] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Mu˜noz, Xinjie Yao, Ren´e Zurbr¨ugg, Nikita Rudin, et al. Isaac lab: A gpu-accelerated simulation framework for multimodal robot learning. _arXiv preprint arXiv:2511.04831_ , 

2025. 

- [24] Katsuhiko Ogata. _Modern control engineering_ . Prentice hall, 2010. 

- [25] Open-X-Humanoid. Tienkung-lab: An open-source research platform for humanoid robots. https://github.com/ Open-X-Humanoid/TienKung-Lab, 2024. 

- [26] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [27] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [28] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

- [29] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [30] Jiyuan Shi, Xinzhe Liu, Dewei Wang, S¨oren Schwertfeger, Chi Zhang, Fuchun Sun, Chenjia Bai, Xuelong Li, et al. Adversarial locomotion and motion imitation for humanoid policy learning. _Advances in Neural Information Processing Systems_ , 38:73918–73949, 2026. 

- [31] Haoming Song, Delin Qu, Yuanqi Yao, Qizhi Chen, Qi Lv, Yiwen Tang, Modi Shi, Guanghui Ren, Maoqing Yao, Bin Zhao, et al. Hume: Introducing system-2 thinking in visual-language-action model. _arXiv preprint arXiv:2505.21432_ , 2025. 

- [32] Noriaki Takasugi, Kunio Kojima, Shu nichi Nozawa, Yohei Kakiuchi, Kei Okada, and Masayuk i Inaba. Realtime skating motion control of humanoid robots for acceleration and balancing. In _2016 IEEE/RSJ International Conference on Intell igent Robots and Systems (IROS)_ , pages 1356–1363. IEEE, 2016. 

- [33] Noriaki Takasugi, Kunio Kojima, Shu nichi Nozawa, Fumihito Sugai, Kakiuchi Yohei, Kei Okada, and Masayuki Inaba. Extended three-dimensional walking and skating motion generation for multiple noncoplanar contacts with anisotropic friction: Application to walk and skateboard and roller skate. _IEEE Robotics and Automation Letters_ , 4(1):9–16, 2018. 

- [34] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033. IEEE, 2012. doi: 10.1109/IROS.2012.6386109. 

- [35] Unitree Robotics. Humanoid robot G1 <u>Humanoid Robot</u> Functions <u>Humanoid</u> Robot Price — Unitree Robotics, 2025. URL https://www.unitree.com/g1/. https://www. unitree.com/g1/. 

- [36] Balazs Varszegi, Denes Takacs, and Gabo r Stepan. Skateboard: a human controlled non-holonomic syste 

m. In _International Design Engineering Technical Confe rences and Computers and Information in Engineering Conferenc e_ , volume 57168, page V006T10A066. American Society of Mechanical Engineers, 2015. 

- [37] Dewei Wang, Xinmiao Wang, Xinzhe Liu, Jiyuan Shi, Yingnan Zhao, Chenjia Bai, and Xuelong Li. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains. _arXiv preprint arXiv:2506.08840_ , 2025. 

- [38] Huayi Wang, Wentao Zhang, Runyi Yu, Tao Huang, Junli Ren, Feiyu Jia, Zirui Wang, Xiaojie Niu, Xiao Chen, Jiahe Chen, et al. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system. _arXiv preprint arXiv:2510.11072_ , 2025. 

- [39] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

and holistic humanoid data collection system, 2025. URL https://arxiv.org/abs/2511.02832. 

   - [48] Chong Zhang, Wenli Xiao, Tairan He, and Guanya Shi. Wococo: Learning whole-body humanoid control with sequential contacts, 2024. URL https://arxiv.org/abs/ 2406.06005. 

   - [49] Yuanhang Zhang, Yifu Yuan, Prajwal Gurunath, Ishita Gupta, Shayegan Omidshafiei, Ali-akbar Agha-mohammadi, Marcell Vazquez-Chanlatte, Liam Pedersen, Tairan He, and Guanya Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 

   - [50] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. _arXiv preprint arXiv:2406.10759_ , 2024. 

- [40] Weiji Xie, Chenjia Bai, Jiyuan Shi, Junkai Yang, Yunfei Ge, Weinan Zhang, and Xuelong Li. Humanoid whole-body locomotion on narrow terrain via dynamic balance and reinforcement learning. _arXiv preprint arXiv:2502.17219_ , 2025. 

- [41] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid wholebody control for learning highly-dynamic skills. _Advances in Neural Information Processing Systems_ , 38: 62406–62433, 2026. 

- [42] Zhe Xu, Mohamed Al-Khulaqui, Hanxin Ma, Jiajun Wang, Quanbin Xin, Yangwei You, Mingliang Zhou, Diyun Xiang, and Shiwu Zhang. Optimization based dynamic skateboarding of quadrupedal robot. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8058–8064. IEEE, 2024. 

- [43] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [44] Shaopu Yang, Yongjie Lu, and Shaohua Li. An overview on vehicle dynamics. _International Journal of Dynamics and Control_ , 1(4):385–395, 2013. 

- [45] Kevin Zakka, Qiayuan Liao, Brent Yi, Louis Le Lay, Koushil Sreenath, and Pieter Abbeel. mjlab: A lightweight framework for gpu-accelerated robot learning, 2026. URL https://arxiv.org/abs/2601.22074. 

- [46] Yanjie Ze, Zixuan Chen, Jo˜ao Pedro Ara´ujo, Zi ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

- [47] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C. Karen Liu. Twist2: Scalable, portable, 

## APPENDIX 

## _A. Derivation of Skateboard Equality Constraint_ 

This appendix derives the kinematic relationship between the deck tilt angle _γ_ and the wheel axle steering angle _σ_ for a skateboard truck with fixed rake angle _λ_ . The derivation follows a two-stage rotation sequence constrained by the wheel-ground contact condition [36]. In Fig. 9 (a), place the origin at the deck center projection _M_ = (0 _,_ 0 _,_ 0) with the _xy_ -plane coinciding with the ground plane. Define: 

- Truck pivot center: _C_ = (0 _,_ 0 _, h_ ) where _h_ is the truck height 

- Initial wheel positions: _E_ = (0 _, w, h_ ), _F_ = (0 _, −w, h_ ) where 2 _w_ is the truck width 

- Kingpin axis _BC_ lies in the horizontal plane at fixed angle _λ_ relative to the _x_ -axis 

- _η_ **-rotation about kingpin axis** _BC_ **.** Transforms wheel 

positions to: 


_γ_ **-rotation about** _x_ **-axis.** The board tilt corresponds to a rotation by angle _γ_ about the _x_ -axis. To rigorously derive the coordinate transformation, we introduce auxiliary points that exploit the geometry of rotation about a coordinate axis (Fig. 9 (b)). For wheel _E_<sup>_′_</sup> , we define: 

- _ME′_ = ( _xE′,_ 0 _,_ 0): orthogonal projection of _E_<sup>_′_</sup> onto the _X_ -axis 

- The segment _ME′_ - _E_<sup>_′_</sup> lies in the plane _x_ = _xE′_ , perpendicular to the rotation axis 

- Rotation about the _x_ -axis preserves _x_ -coordinates and moves _E_<sup>_′_</sup> along a circular arc centered at _ME′_ with radius _rE_ = _∥ME′_ - _E_<sup>_′_</sup> _∥_ 

Let _αE_ denote the angle between segment _ME′_ - _E_<sup>_′_</sup> and the positive _z_ -axis. By construction: 


After rotation by _γ_ , the angle between _ME′_ - _E_<sup>_′′_</sup> and the _z_ -axis becomes _αE − γ_ . Applying trigonometric addition formulas: 


_zE′′_ = _rE_ cos( _αE − γ_ ) = _zE′_ cos _γ_ + _yE′_ sin _γ_ (20) 

with _xE′′_ = _xE′_ preserved by the rotation symmetry. Analogous definitions for _F_<sup>_′_</sup> yield: 


Substituting the expressions for _E_<sup>_′_</sup> and _F_<sup>_′_</sup> gives the complete transformed coordinates. 

**Wheel-Ground Contact Constraint.** For both wheels to maintain ground contact simultaneously, their _z_ -coordinates must be equal ( _zE′′_ = _zF ′′_ ): 


**Fig. 9: Kinematic geometry of a skateboard truck.** (a) Rotating about the truck pivot axis. (b) Geometric construction for _γ_ -rotation. (c) Definition of steering angle _σ_ from top view. 

Simplifying yields the fundamental constraint: 


**Steering Angle Definition.** In Fig. 9 (c), the steering angle _σ_ is defined geometrically from the projection of _E_<sup>_′′_</sup> onto the _xy_ -plane relative to the rotated truck center _C_<sup>_′′_</sup> = (0 _, −h_ sin _γ, h_ cos _γ_ ): 


which simplifies to: 

tan _σ_ (cos _η_ cos _γ_ + sin _η_ cos _λ_ sin _γ_ ) = sin _η_ sin _λ_ (28) 

Substituting Eq. (26) into Eq. (28): 


Finally it yields the exact kinematic relationship, as illustrated in Eq (1): 


We embed this equivalent relationship into simulation using two implementations: (i) enforcing the constraint via MuJoCo equality constraints [34], and (ii) directly setting the corresponding steer angle as a function of the tilt angle within the simulation environment. Both implementations produce similar kinematic behaviors in practice. 

## _B. Skateboard Model_ 

The key components of our simplified skateboard model in MuJoCo are summarized in Table IV and Table V. In simulation, the wheel–ground contact is modeled with six dimensions 

**TABLE IV:** Skateboard Bodies 

|Name|Position|Type|Size|
|---|---|---|---|
|Skateboard deck|0 0 0|Box|0.8 0.2 0.02|
|Front truck|0 0 -0.09|Box|0.1 0.02 0.02|
|Front left wheel|0 0.07 0|Cylinder|0.03 0.02|
|Front right wheel|0 -0.07 0|Cylinder|0.03 0.02|
|Rear truck|0 0 -0.09|Box|0.1 0.02 0.02|
|Rear left wheel|0 0.07 0|Cylinder|0.03 0.02|
|Rear right wheel|0 -0.07 0|Cylinder|0.03 0.02|


**TABLE V:** Skateboard Joints 

|Name|Type|Joint Axis|Range|
|---|---|---|---|
|Board tilt joint|Hinge|-1 0 0|(-0.2, 0.2)|
|Front truck joint|Hinge|0 0 1|(-0.1, 0.1)|
|Rear truck joint|Hinge|0 0 -1|(-0.1, 0.1)|
|Wheel joints|Hinge|0 1 0|Continuous|


( _condim_ = 6), including two tangential, one torsional, and two rolling directions, to realistically capture wheel–ground interactions. The rolling friction coefficient is set to 0.001 to reflect low-resistance wheel motion. As shown in Fig. 10, two virtual markers are positioned above the trucks to guide stable foot contacts, as illustrated by the blue and red spheres. 


**Fig. 10: Skateboard Model in Training.** Red and blue markers indicate stabel foot placement points, while thelight green areas denote collision zones used for foot-board collision detection. 


**Fig. 11: Key body reference poses.** (a) Default pose used for policy training. (b) Reference pose for the pushing phase. (c) Reference pose for the steering phase. All poses are annotated from the human motion dataset _M_ to ensure realistic humanoid posture configuration. 

## _C. Reward Functions_ 

The reward terms, corresponding to pushing, steering, transitions, and regularization, are summarized in Table VI. 

## _D. Training Details_ 

We define a skateboarding cycle of 6 seconds with a hybrid phase structure, including a pushing phase (40%), a footmounting transition phase (10%), a steering phase (45%), and a dismounting transition phase (5%). The phase variable Φ _∈_ [0 _,_ 1) is divided into Pushing [0 _,_ 0 _._ 4], Mounting [0 _._ 4 _,_ 0 _._ 5], Steering [0 _._ 5 _,_ 0 _._ 95], and Dismounting [0 _._ 95 _,_ 1 _._ 0). All parallel envs initialize from Pushing, with rewards computed according to the active phase. The RL policies are trained on an NVIDIA RTX 5080 server, with each iteration taking approximately 2–3 seconds. The tracking-based baseline follows DeepMimic [26] style, while the gait-based uses a periodic gait clock [25]. Training a policy for real-world deployment requires roughly 20 hours in total. The PPO hyperparameters used are summarized in Table VII. 

## _E. Foot Contact Detection_ 

To accurately detect foot contacts with the ground and skateboard, we employ separate contact sensors for each foot–surface pair: left foot–ground, right foot–ground, left foot–board, and right foot–board. These sensors filter the corresponding contact interactions to provide reliable feedback. 

In addition, to prevent foot penetration during training, small contact collision regions are placed on the skateboard at the designated foot placement locations. These regions ensure that only intended foot–board contacts are registered, preventing the policy from exploiting unintended collisions with other parts of the skateboard to obtain contact rewards. As shown 

in Fig. 10, the active collision regions are highlighted as light green shaded areas on the board. 

## _F. Reference Pose_ 

The initial pose used at the start of training is shown in Fig. 11 (a), while the canonical reference poses for the pushing and steering phases are shown in Fig. 11 (b) and Fig. 11 (c). All these poses are annotated from the human motion dataset _M_ to ensure realistic posture and limb configurations. 

The key bodies used to define these poses include the pelvis, torso, left and right hips, knees, and ankles, as well as the left and right shoulders, elbows, and wrists. Representing the humanoid with these key bodies provides a compact yet expressive description of its configuration, facilitating smooth and effective transitions between phases. 

## _G. Evaluations on More Terrains_ 

While our experiments were conducted on flat ground, the real-world indoor and outdoor testing environments already contained tile gaps and varying frictions. Our heavy DR strategy ensures that the policy manages these unmodeled surface irregularities. We evaluated HUSKY on inclined slopes (5<sup>_◦_</sup> – 10<sup>_◦_</sup> ) and steps (3 _−_ 6 _cm_ ) (Fig. 12), with results in Table VIII confirming its adaptability to uneven terrains. We acknowledge that extreme scenarios, such as vertical ramps or bowl parks, pose significant risks for humanoids and require vision-based planning beyond the current scope. 

## _H. Results of Skateboard Identification_ 

The gains of the PD controller were determined via system identification for two skateboards. The moment of inertia 

**TABLE VI:** Task Reward terms and weights. 

|Term|Expression|Weight|Meaning|
|---|---|---|---|
|**Pushing Phase** _r_<sup>push</sup><br>_t_||||
|Linear velocity tracking<br>Yaw alignment<br>Feet air time<br>Ankle parallel [14]<br>AMP style reward|exp(_−|v_board_−v_cmd_|_<sup>2</sup>_/σ_<sup>2</sup><br>_v_<sup>)</sup><br>exp(_−|ψ_robot_−ψ_board_|_<sup>2</sup>_/σ_<sup>2</sup><br>yaw<sup>)</sup><br>I(_T_ <sup>left</sup><br>foot<br>air<br>_∈_[_T_ <sup>min</sup><br>air<br>_, T_ <sup>max</sup><br>air<br>])_·_I(_v_cmd _> v_th)<br>I(Var(_z_left<br>ankle<sup>)</sup><sup>_<_ 0</sup><sup>_._05 )</sup><sup>_·_ I(left foot on ground))</sup><br>_α ·_max<br>�<br>0_,_ 1_−_1_/_4(_d −_1)<sup>2�</sup>|3.0<br>1.0<br>3.0<br>0.5<br>5.0|Track commanded forward velocity<br>Align robot yaw with skateboard during pushing<br>Encourage proper left-foot lift timing during pushing<br>Encourage left foot to remain parallel during pushing<br>Encourage human-like natural pushing behavior|
|**Steering Phase** _r_<sup>steer</sup><br>_t_||||
|Steer feet contact<br>Joint position deviation<br>Heading tracking|2_∗_I(both feet on board)_−_I(left foot on ground)<br>exp(_−∥_**_θ_**_t −_<sup>ˆ</sup>**_θ_**_t∥_<sup>2</sup><br>2<sup>_/σ_2</sup><br>jpos<sup>)</sup><br>exp(_−_(_ψ_board_−ψ_)<sup>2</sup>_/σ_<sup>2</sup><br>_ψ_<sup>)</sup>|3.0<br>1.5<br>5.0|Encourage both feet on board and avoid ground contact<br>Maintain nominal humanoid steering pose<br>Track desired board direction|
|Board tilt tracking<br>Feet marker distance|exp(_−_(_γ −γ_ref)<sup>2</sup>_/σ_<sup>2</sup><br>_γ_<sup>)</sup><br>exp(_−∥_**_p_**foot_−_**_p_**marker_∥_<sup>2</sup><br>2<sup>_/σ_2</sup><br>_m_<sup>)</sup>|4.0<br>1.0|Align board lean with physics-guided reference<br>Encourage feet near preferred foot markers|
|**Transition** _r_<sup>trans</sup><br>_t_||||
|Keybody position tracking<br>Keybody orientation tracking|exp(_−∥_**_p_**<sup>_K_</sup><br>_t _<sup>_−_ˆ</sup><sup>**_p_**</sup><sup>_K_</sup><br>_t _<sup>_∥_2</sup><br>2<sup>_/σ_2</sup><br>pos<sup>)</sup><br>exp(_−∥_**_q_**<sup>_K_</sup><br>_t _<sup>_⊖_</sup><sup>**_q_**</sup><sup>_K_</sup><br>_t _<sup>_∥_2</sup><br>2<sup>_/σ_2</sup><br>rot<sup>)</sup>|10.0<br>10.0|Follow trajectory-planned keybody positions<br>Follow trajectory-planned keybody orientations|
|**Regularization** _r_<sup>reg</sup><br>_t_||||
|Skateboard wheel contact<br>Joint position limits<br>Joint velocity<br>Joint acceleration<br>Joint torque|I<br>��4<br>_i_=1 <sup>_ci_ = 4</sup><br>�<br>I(**_q_**_t /∈_[**_q_**min_,_**_q_**max])<br>_∥_˙**_q_**_t∥_<sup>2</sup><br>2<br>_∥_¨**_q_**_t∥_<sup>2</sup><br>2<br>_∥_**_τ_**_t∥_<sup>2</sup><br>2|0.5<br>-5.0<br>-1e-3<br>-2.5e-7<br>-1e-6|Reward full wheel contact, avoid unrealistic detachment<br>Keep joints within safe limits<br>Penalize high joint speeds<br>Penalize abrupt joint accelerations<br>Penalize excessive torque|
|Action rate|_∥_**_a_**_t −_**_a_**_t−_1_∥_<sup>2</sup><br>2|-0.1|Encourage smooth actions|
|Action smoothness|_∥_**_a_**_t −_2**_a_**_t−_1+**_a_**_t−_2_∥_<sup>2</sup><br>2|-0.1|Reduce oscillations in control commands|
|Collision|Icollision|-10.0|Penalize self-collisions|


**TABLE VII:** Hyperparameters related to PPO. 

|Hyperparameter|Value|
|---|---|
|Optimizer<br>|Adam<br>|
|Batch size|4096|
|Mini Batches|4<br>|
|Learning epoches<br>i|5<br>|
|Entropy coefficient|0.005|
|Value loss coefficient<br>|1.0<br>|
|Clip param<br>|0.2<br>|
|Max grad norm|1.0|
|Init noise std<br>|1.0|
|Learning rate<br>|1e-3<br>|
|Desired KL|0.01|
|GAE decay factor(_λ_)|0.95|
|GAE discount factor(_γ_)|0.99|
|Actor MLP size|[512, 256, 128]|
|Critic MLP size|[512, 256, 128]|
|MLP Activation|ELU|


### **TABLE VIII:** Evaluations on More Terrains 

|**Terrain Settings**|_E_succ_↑_|_E_smth_↓_|_E_contact_↓_|
|---|---|---|---|
|HUSKY-Slope|95_._02_±_0_._14|0_._038_±_0_._006|0_._001_±_0_._001|
|HUSKY-Steps|89_._21_±_0_._25|0_._042_±_0_._009|0_._003_±_0_._002|
|HUSKY-Flat Ground|100_._00_±_0_._00|0_._033_±_0_._005|0_._001_±_0_._001|


( _I_ ) of each plant was calculated using the formula for a rectangular prism, resulting in _I_ = 7 _._ 15 _×_ 10<sup>_−_3</sup> kg _·_ m<sup>2</sup> for the first skateboard and _I_ = 8 _._ 70 _×_ 10<sup>_−_3</sup> kg _·_ m<sup>2</sup> for the second. 

Analysis of the experimental decaying oscillation responses confirmed that both systems exhibited underdamped secondorder dynamics. For the first skateboard, an oscillation period 


**Fig. 12: Visualizations on more terrains.** HUSKY maintains robust zeroshot performance on unseen terrains including slopes and steps. 

of _T_ = 0 _._ 107 s was observed, with successive peak amplitudes of _θ_ ( _t_ ) = 0 _._ 614 and _θ_ ( _t_ + _T_ ) = 0 _._ 0108. This yielded controller gains of _Kp_ = 34 _._ 835 and _Kd_ = 0 _._ 540. The second skateboard demonstrated a period of _T_ = 0 _._ 185 s, with peak amplitudes of _θ_ ( _t_ ) = 0 _._ 583 and _θ_ ( _t_ + _T_ ) = 0 _._ 0081, which resulted in gains of _Kp_ = 14 _._ 677 and _Kd_ = 0 _._ 402. 

We model skateboard suspension via a lean-to-steer coupling using an equivalent spring–damper model. While abstracting detailed bushing deformation, it captures the dominant kinematic relationship within a 15<sup>_◦_</sup> roll range, which is critical for steering. We provide two-fold evidence to support physics fidelity. (1) A board-tilt response (Fig. 13 (a)) during mounting validates transient dynamics. A free-decay roll response (Fig. 13 (b)) shows close alignment between hardware and the identified model in decaying oscillation; (2) We clarify although a flat deck is used, spatial guidance and foot markers ensure contact remains within the stable central region, avoiding unmodeled kicktails. And DR of CoM offsets and surface friction mitigates sensitivity to simplified 


**Fig. 13: Board-tilt response between sim and real.** The board-tilt response curves during mounting and the board-tilt decaying results demonstrate the physics fidelity of our skateboard modeling approach. 


**Fig. 15: Humanoid Skateboarding on Diverse Boards.** HUSKY enables the humanoid to perform skateboarding behaviors across multiple skateboard platforms, demonstrating the generality and robustness of our method. 

## geometry. 

## _I. Effects of Transition Design_ 

Our key insight is leveraging _explicit guidance_ as a minimal prior to prune the search space, not as a hard-coded constraint. In Table IX, HUSKY maintains high performance even under Canonical Pose Perturbation ( _±_ 5 _cm_ ), Transition Duration Scaling ( _±_ 20%), and Interpolation Variants (Spline), showing that the policy is not overfitted to specific trajectories. Under external forces, the agent prioritizes stability over following trajectories (Fig. 14). This ability to deviate from the heuristics proves the policy mastered the underlying balancing physics, offering a scalable approach for multi-phase tasks. 

engine provides a more accurate representation of the nonlinear friction and contact dynamics crucial for skating. 

**TABLE IX:** Sensitivity Analysis of Transition 

|**Transition Settings**|_E_succ_↑_|_E_smth_↓_|_E_contact_↓_|
|---|---|---|---|
|Pose-Perturbed|99_._63_±_0_._12|0_._037_±_0_._007|0_._002_±_0_._001|
|Time-Scaled|100_._00_±_0_._00|0_._035_±_0_._003|0_._001_±_0_._002|
|Path-Varied|98_._54_±_0_._93|0_._033_±_0_._004|0_._002_±_0_._002|
|HUSKY|100_._00_±_0_._00|0_._033_±_0_._005|0_._001_±_0_._001|


**Fig. 14: Humanoids explore beyond heuristic transition.** Humanoid deviates from the planned trajectories proves the policy mastered the underlying balancing physics instead of rigidly following heuristics. 

## _J. More Skateboards_ 

We further evaluate HUSKY on a variety of skateboard platforms. Results show that the humanoid successfully performs skateboarding behaviors, including pushing, steering, and phase transitions. As shown in Fig. 15, these results confirm the generality and effectiveness of our approach. 

## _K. More Findings_ 

We conducted comparative experiments across different simulation frameworks. While IsaacLab [23] offers superior parallelization, policies trained within this environment frequently failed during sim-to-sim validation due to excessive foot-skateboard slippage. These issues were resolved upon integrating mjlab [45] for fine-grained simulation. The success of mjlab deployment suggests that its underlying physics 

