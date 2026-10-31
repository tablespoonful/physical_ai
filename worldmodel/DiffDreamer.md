---
title: "DiffDreamer: Coupling World Models with Differentiable Simulation for Agile Quadrotor Control"
date: "2026-10-22"
authors: "Fanxing Li; Yuxiang Huang; Shengyang Wang; Fangyu Sun; Shuyu Wu; Tianbao Zhang"
url: https://arxiv.org/abs/2610.31617
pdf: https://arxiv.org/pdf/2610.31617
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2610.31617)** / [論文ページ](https://arxiv.org/abs/2610.31617)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE ROBOTICS AND AUTOMATION LETTERS 

1 

# DiffDreamer: Coupling World Models with Differentiable Simulation for Agile Quadrotor Control 

Fanxing Li, Yuxiang Huang, Shengyang Wang, Fangyu Sun, Shuyu Wu, Tianbao Zhang, Dexin Zuo, Yan Yufei, Danping Zou, Wenxian Yu 

**_Abstract_ —Tasks such as quadrotor dynamic-gate racing require agents to anticipate external motion while maintaining precise high-frequency control. World-model-based reinforcement learning (RL) provides a natural solution by learning latent dynamics for future imagination, yet it often entangles environmental evolution and the robot’s own dynamics in a single learned rollout, where model bias can affect policy optimization efficiency. We propose DiffDreamer, a differentiable reinforcement learning framework that tightly couples a learned world model with differentiable simulation for actor optimization. In one optimization step, the learned world model propagates latent states that capture external dynamics and history-dependent features, while the differentiable simulator propagates the robot’s explicit physical state. We further decompose the actor objective into a critic-driven pathway for non-differentiable task rewards and a simulator-driven pathway for differentiable motion rewards. Experiments on aggressive tracking and dynamic-gate racing show that DiffDreamer improves training convergence over the model-free, model-based, and differentiable-RL baselines, and final performance over these baselines and classical planning and control methods. Additional experiments assess reward decomposition and the odometry-conditioned relative-state representation through ablations. We also provide proof-of-concept real-world flight experiments for validation.** 

### **_Index Terms_ —Differentiable Simulation, Reinforcement Learning, World Model.** 

## I. INTRODUCTION 

Many robotic tasks require agents to anticipate external environmental evolution to achieve precise control. This structure is particularly prominent in agile aerial robotics. A representative example is dynamic-gate racing with quadrotors [1]– [3], where the robot must predict the future motion of moving gates and generate accurate control commands to pass through narrow openings at high speed. Existing solutions [2] often address this challenge through modular pipelines that decouple prediction, planning, and control. Although such designs are interpretable and effective, they usually rely on task-specific engineering and optimize each module separately. 

World-model-based reinforcement learning [4], [5] provides an integrated alternative. By learning compact latent dynamics from interaction, methods such as Dreamer [4] can imagine future trajectories and optimize policies in latent space. However, in agile robotic control, a learned world model often has to capture both the evolution of the external environment and the robot’s high-frequency rigid-body dynamics within the same learned rollout. This entangles two sources of dynamics with different structures: the external dynamics are partially 

observable and history-dependent, whereas the robot’s internal dynamics are often smooth and available through physical modeling. As a result, policy optimization through purely learned rollouts may suffer from model bias and less accurate gradients for precise physical control. This motivates using differentiable simulation for the robot’s physical motion, so that the learned world model can focus on latent external dynamics. 

Differentiable reinforcement learning (DiffRL) [6], [7] offers a complementary direction. By backpropagating through a differentiable physical model, it can provide low-variance first-order gradients for policy optimization and be particularly effective for smooth robotic systems. However, differentiable RL alone typically assumes that the transition and reward structures are differentiable and explicitly available. This makes it difficult to handle partially observable external dynamics, moving targets with unknown future motion, and non-differentiable task events such as gate-crossing rewards. 

To address this problem, we propose DiffDreamer, which structurally separates robot dynamics from external environment dynamics and couples their rollouts for policy optimization. DiffDreamer synchronizes latent world-model imagination with differentiable physical rollouts: under the same action, the world model updates an implicit state representing external time-varying features, while the simulator propagates the explicit robot state. The actor receives both states as input, and its objective is decomposed into a critic-driven pathway for non-differentiable task rewards and a simulator-driven pathway for differentiable motion rewards. We compare DiffDreamer with RL, trajectory planning, and model predictive control (MPC) baselines on aggressive tracking and dynamic-gate racing, and demonstrate its effectiveness through transfer to real quadrotor flight. 

Our contributions are summarized as follows: 

- We propose a dual-pathway policy optimization framework that synchronizes latent imagination with differentiable physical rollouts to improve optimization accuracy and reduce the burden of learning high-frequency robot dynamics within the world model. 

- We conduct comprehensive experiments on two quadrotor tasks with dynamic external environments to validate the advantages of the proposed method in terms of control accuracy and predictive capabilities. 

- We conduct ablation studies on reward decomposition and odometry-conditioned relative-state representation to 

IEEE ROBOTICS AND AUTOMATION LETTERS 

2 


Fig. 1. A schematic overview of DiffDreamer for dynamic-gate racing. The quadrotor must predict the future motion of dynamic gates while executing precise flight control. DiffDreamer trains the actor through a tightly coupled dual-pathway process: a learned world model imagines future environmental states (e.g., target motion), while a differentiable simulation predicts the quadrotor’s physical dynamics and provides analytical gradients. The policy takes both implicit latent states and explicit physical states as input to generate control commands. The quadrotor is digitally reconstructed and calibrated through system identification for zero-shot transfer to the real world. 

assess their contributions. 

- We provide proof-of-concept validation of aggressive tracking and dynamic-gate racing in real-world scenarios. 

## II. RELATED WORK 

## _A. Agile Quadrotor Flight and Modular Pipelines_ 

Agile quadrotor flight, including autonomous racing, typically relies on modular pipelines for perception, state estimation, trajectory planning, and low-level control under tight real-time constraints [8]. In dynamic environments with moving targets or gates, these pipelines often use motionprediction modules to support downstream planning and control. Representative approaches combine learned gate perception with trajectory generation and tracking [1], learned data abstraction with nonlinear filtering and time-optimal planning [9], or model-predictive and time-optimal control for aggressive waypoint or gate traversal [10]–[12]. Policy search can also tune model-predictive controllers for agile flight [2]. Elastic Tracker combines target-motion prediction with visibility-aware spatio-temporal trajectory optimization for aerial tracking [13]. These modular pipelines are effective and interpretable, especially when the environment structure and task objectives are well specified. However, their modules are usually designed and optimized separately, so prediction or planning errors may propagate to downstream control. 

Despite their sample efficiency, model-based methods remain sensitive to model fidelity, especially in high-accuracy and high-frequency robotic control [23]. In agile quadrotor tasks, a single learned rollout must often capture both partially observable external motion and fast rigid-body dynamics, which introduces distinct learning challenges. 

## III. METHODOLOGY 

## _A. Preliminaries_ 

We formulate robotic control as a partially observable Markov decision process (POMDP), _M_ = ( _S, A, p, r, c_ ). In state _st ∈S_ , the agent executes an action _at ∈A_ , receives a reward _rt ∼ r_ ( _st, at_ ) and an episode continuation signal _ct_ , and transitions to _st_ +1 _∼ p_ ( _st_ +1 _| st, at_ ). Here, _p_ and _r_ denote the transition dynamics and reward function. Actions are sampled from a stochastic policy parameterized by _θ_ : 


where _ot_ is a noisy or partial measurement of the true state _st_ . The actor-critic framework is widely used in reinforcement learning (RL) for such problems. The critic _Vψ_ ( _ot_ ) (or _Qψ_ ( _ot, at_ )), parameterized by _ψ_ , estimates the expected longterm return and can provide a low-variance gradient signal for actor optimization. The actor aims to infer optimal actions from partial observations. 

## _B. Model-based Reinforcement Learning_ 

Model-based reinforcement learning uses learned or known dynamics models for planning and policy optimization, supporting sample-efficient end-to-end policy learning. Modelfree methods learn directly from interaction with the environment and typically require more data [14], [15]. Classical and modern approaches have explored probabilistic dynamics and uncertainty-aware planning, such as PILCO and PETS [16], [17], short model-generated rollouts for value/policy learning, such as MBPO [18], and latent dynamics for planning or imagination-based actor-critic learning, such as MuZero, Dreamer, and TD-MPC [4], [5], [19]–[22]. 

## _B. Model-based RL from a World Model_ 

Unlike model-free RL, model-based RL explicitly learns environmental dynamics and imagines future trajectories to estimate long-term returns, which can provide a richer policy optimization signal. As a representative framework, DreamerV3 [20] uses a recurrent state-space model (RSSM) as its world model to model environment dynamics. The RSSM represents environmental states and transitions in a compact latent space comprising a deterministic hidden state _ht_ and a stochastic latent feature _zt_ . An encoder _qϕ_ maps the highdimensional observation _ot_ to a posterior stochastic representation _zt_ . The recurrent dynamics module advances from 

IEEE ROBOTICS AND AUTOMATION LETTERS 

3 

In differentiable simulation, the agent collects trajectories by unrolling the dynamics with its current stochastic policy. The resulting complete computational graph links each timestep’s reward to the actor parameters across time, allowing the cumulative return to be differentiated with respect to these parameters by backpropagating through the simulator: 

the previous state using the executed action _at_ to predict the temporal prior (ˆ _zt, ht_ ). The model uses the concatenated latent state to predict expected rewards and episode continuation flags and reconstruct the original observations. 

**Training the Actor-Critic.** DreamerV3 trains its actor and critic entirely on abstract trajectories imagined by the learned = world model. Starting from initialized latent states _s_<sup>_imp_</sup> _t {zt, ht}_ , it unrolls the recurrent dynamics using successive actions from the current actor policy to generate future latent states and predicted rewards. Both networks operate directly on the implicit latent state _s_<sup>_imp_</sup> _t_ rather than explicit states: 


Since each timestep’s reward is continuously differentiable with respect to all preceding actions, the policy can be optimized by applying the chain rule through the dynamics. The actor gradient in Eq. (5) thus expands as: 


The actor is trained to maximize expected cumulative returns along imagined trajectories. We express its objective as loss minimization, using a simplified gradient form that emphasizes gradient flow through imagined latent trajectories: 

_T j_ =� _it_ +1 (6) _∇θL_ ( _θ_ ) = _−_ � _γ_<sup>_t_</sup> _∇θV_<sup>ˆ</sup> _t_ (3) _t_ =0 The reward derivatives, _∂R/∂at_ and _∂R/∂s_<sup>exp</sup> _t_ , follow directly from the known analytical reward formulation. The is the discount factor balancing immediate and future differentiable physics engine provides the state transition is the imagination horizon. The critic reJacobian, _∂s_<sup>exp</sup> _j /∂s_<sup>exp</sup> _j−_ 1<sup>.Forthecontinuous-timedynamics</sup> gresses its value predictions toward expected returns computed _d_ ( _s_<sup>exp</sup> _t , at_ ), the simulator typically uses a time-discretized rewards. To robustly estimate the target return ordinary differential equation (ODE) integration scheme: 

where _γ_ is the discount factor balancing immediate and future rewards, and _T_ is the imagination horizon. The critic regresses its value predictions toward expected returns computed from imagined rewards. To robustly estimate the target return _R_ ˆ<sup>_λ_</sup> _t_<sup>whilemitigatingtruncationbiasbeyondtheimagination</sup> horizon, bootstrapped _λ_ -returns smoothly interpolate between _N_ -step predicted rewards and learned value estimates [24]. The critic evaluates the return distribution by minimizing the negative log-likelihood: 


Using these first-order gradients through the differentiable physical model, DiffRL can improve sample efficiency in smooth robotic control problems, as empirically validated in complex domains including quadrupedal locomotion [25] and vision-based navigation for aerial robots [26]. 


For the quadrotor, the continuous-time dynamics _d_ govern the world-frame position **p** _W_ and velocity **v** _W_ , attitude quaternion **q** , and body angular velocity **Ω** : 

Here _ct_ denotes episode continuation, and _λ_ controls the mixture of bootstrapped values and longer-horizon returns. 


## _C. Differentiable Reinforcement Learning_ 

Although traditional RL has achieved remarkable success across diverse fields, actor-critic performance can be sensitive to errors in approximating long-term returns. In discrete domains such as Go or Atari games, parameterized critics are commonly used for value estimation. Smooth robotic control can exploit differentiable models of Newtonian dynamics together with suitably defined differentiable rewards. 

Here, **R** _W B_ maps body-frame vectors to the world frame, _m_ is the vehicle mass, **J** the inertia matrix, **g** gravity, **d** _W_ the external disturbance force, and **_η_** the body torque. The operator _⊗_ denotes quaternion multiplication. The quadrotor’s bodyframe thrust force is **f** _B_ = [0 _,_ 0 _, f_ ]<sup>_T_</sup> , where _f_ is the collective thrust. 

Like MPC, differentiable RL directly optimizes the policy by backpropagating reward gradients through a differentiable physical model. This reduces reliance on a learned critic for dense motion optimization and provides low-variance firstorder gradients when dynamics and reward terms are smooth and accurately modeled. We define the robot’s explicit state as _s_<sup>exp</sup> _t_ (e.g., position, velocity, joint angles) and assume a deterministic transition _d_ ( _s_<sup>exp</sup> _t , at_ ) rather than a stochastic process. The reward _R_ ( _s_<sup>exp</sup> _t , at_ ) is likewise a deterministic function of the explicit state and action. 

_D. DiffDreamer: Learning Behaviors from Imagination and Prediction_ 

Differentiable RL has shown strong sample efficiency in smooth robotic control but requires differentiable dynamics and rewards within the optimization graph. In many dynamic robotic tasks, a calibrated differentiable simulator can model or approximate ego dynamics, while separate prediction or 

IEEE ROBOTICS AND AUTOMATION LETTERS 

4 


Fig. 2. Coupling external-motion prediction with internal control. **Left:** Catching a ball requires imagining its trajectory and planning body motion. **Right:** DiffDreamer combines latent world-model features with explicit physical states for policy optimization. It imagines future external motion through a learned world model and propagates the robot’s physical state through differentiable simulation. 

estimation modules typically handle external dynamics such as moving targets or gates. These external models are feasible and often effective, but are usually optimized independently of the control policy, which can contribute to prediction-control mismatch and error propagation at high speeds. 

This separation is consistent with the intuitive process of predicting how the external world may evolve while planning body motion using an internal physical model. For example, humans catching an incoming ball anticipate its trajectory while coordinating their body motion, as illustrated in Fig. 2. 

Based on this separation, we introduce **DiffDreamer** , a unified framework coupling predictive latent imagination with differentiable physical prediction. The implicit pathway uses a learned world model to encode history-dependent external dynamics and predict future latent states. The explicit pathway propagates the robot’s physical state under the same action through a differentiable simulator, providing gradients for differentiable motion rewards. Actor training through these synchronized pathways combines the latent imagination of world-model-based RL with DiffRL’s physical precision. 

**Joint State Actor and Critic** . Like standard model-based RL, DiffDreamer stores interaction experiences in a replay buffer to continually train the world model. The actor and critic use a joint state _st_ formed by concatenating the implicit latent state _s_<sup>_imp_</sup> _t_ and explicit physical state _s_<sup>_exp_</sup> _t_ : 


= The RSSM produces and updates the implicit state _s_<sup>_imp_</sup> _t_ ( _ht, zt_ ), which encodes history-dependent external dynamics and time-varying features, such as target or gate motion patterns. The differentiable simulator propagates the explicit state _s_<sup>_exp_</sup> _t_ , comprising position, velocity, attitude, and angular velocity. The stop-gradient operator sg preserves the actor’s latent input features while blocking gradients through that input. At each rollout step, the same actor-sampled action updates both states through the RSSM and simulator, keeping them temporally synchronized. 

**Decomposed Value Estimation** . DiffDreamer decomposes rewards into a discrete (or non-differentiable) component _rt_<sup>_disc_</sup> = _Rdisc_ ( _s_<sup>_exp_</sup> _t , at_ ) and a differentiable component 

_rt_<sup>_diff_</sup> = _Rdiff_ ( _st_<sup>_exp_</sup> _, at_ ). Differentiable rewards tightly regulate continuous physical motion, while discrete rewards govern high-level behaviors or task milestones. Rather than approximate the entire expected return, the critic estimates returns from the non-differentiable component; differentiable rewards are optimized by direct backpropagation through the simulator. The critic’s surrogate objective in Eq. (4) becomes: 


Unlike the return in Eq. (4), this return uses only _rt_<sup>_disc_</sup> . 

**Dual-Pathway Policy Optimization** . The actor’s surrogate loss similarly combines a critic-driven value objective with a simulator-driven analytical objective: 


During actor optimization, the world-model and critic parameters are kept fixed. The latent input is detached at each actor evaluation, blocking backpropagation into the imagined latent rollout through this input. The explicit-state input remains differentiable, allowing motion-reward gradients to flow through the physical rollout and the actor. The critic supplies the valuebased term for non-differentiable task rewards. Both forward rollouts remain synchronized by the shared action sequence. 

DiffDreamer can benefit both paradigms. For model-based RL, separating rigid-body dynamics from latent imagination can reduce the world model’s learning burden. For differentiable RL, augmenting physical rollouts with learned latent states extends first-order policy optimization to partially observable dynamic environments and non-differentiable task events. The world model provides latent predictions of external dynamics, while the differentiable simulator supplies gradients for controllable robot dynamics. 

## IV. EXPERIMENTS 

Quadrotors’ smooth, complex dynamics make them an ideal real-world platform for evaluating algorithms that integrate 

5 

IEEE ROBOTICS AND AUTOMATION LETTERS 


Fig. 3. Real-world experiments using DiffDreamer for aggressive tracking and dynamic-gate racing. **Left:** flight trajectories and selected consecutive frames showing tight target tracking. **Right:** dynamic-gate racing, where the quadrotor anticipates the future positions of moving gates. 

differentiable physics. We design aggressive tracking and dynamic-gate racing as end-to-end benchmarks to evaluate DiffDreamer’s perception of dynamic environments and control performance. 

## _A. Experimental Setup_ 

We implement both benchmarks in VisFly [27], a highfidelity quadrotor simulator with explicit differentiable physics written in PyTorch. **Aggressive Tracking** requires the quadrotor to continuously track a high-speed target, keeping it centered in the field of view (FOV) at a stable relative distance. **Dynamic-gate Racing** requires the quadrotor to traverse moving gates sequentially in the shortest possible time. 

The quadrotor’s explicit state _s_<sup>_exp_</sup> = _{_ **p** _,_ **v** _,_ **q** _,_ **Ω** _}_ comprises position, velocity, orientation, and angular velocity. We use the full nonlinear rigid-body dynamics in Eq. (8), rather than a point-mass model driven by position commands. The policy outputs end-to-end collective thrust and body rate (CTBR) commands _at_ = [ _ft_<sup>_d,_Ω</sup><sup>_d_</sup> _t_<sup>],whereΩ</sup><sup>_d_</sup> _t_<sup>=[</sup><sup>_ω_</sup> _x_<sup>_d, ω_</sup> _y_<sup>_d, ω_</sup> _z_<sup>_d_],</sup> providing the control authority needed for aggressive maneuvers. Detailed task definitions, observations, and reward formulations are given in Section IV-B. Target and gate trajectories are cubic curves with randomly sampled control points. For external-motion prediction, we compare the world model with a three-dimensional constant-acceleration extended Kalman filter (EKF). 

## _B. Task Definition_ 

Observations come from the simulator or, in real-world validation, motion capture, as described in Section IV-F. DreamerV3 encodes observations into its RSSM state; DiffDreamer combines learned latent features with explicit physical states. 

_1) Aggressive Tracking:_ The tracking task assumes a monocular camera rigidly mounted on the quadrotor and aligned with the body _x_ -axis. The objective is to track a flying target moving agilely and unpredictably in 3D while keeping it centered in the camera field of view (FOV) and maintaining a prescribed constant distance. The observation in this camerabased task combines relative target position with quadrotor odometry: 


where **p**<sup>_tar_</sup> _H_ denotes the relative position of the target in the heading frame _H_ . 

We use the StableTracker reward [28] in VisFly. It combines a distance penalty for deviations from the desired relative distance, a perception reward for facing the target and keeping it centered in the FOV, and a control penalty for aggressive and unstable actions: 


where _k_ 0 _, k_ 1 _, k_ 2 _, k_ 3 _, k_ 4 weight the reward terms and _d_ is the desired distance between the quadrotor and target. The subscript _W_ denotes the world frame. The body-frame _x_ -axis vector **x** _B_ coincides with the camera viewing direction. _2) Dynamic-gate racing:_ Drone racing is a standard benchmark for aerial robots, typically requiring gate traversal as quickly as possible. In our setting, gates move in 3D, requiring the quadrotor to perceive environmental changes and adapt its decisions. Since gates must be traversed sequentially, we include only the nearest two gates in the observation: 


where **p**<sup>_gate_</sup> _W_<sup>1</sup> _−_ **p** _W_ and **p**<sup>_gate_</sup> _W_<sup>2</sup> _−_ **p** _W_ are the relative positions of the nearest two gates in the world frame. 

The reward combines a discrete component for successful gate passage with a differentiable component that encourages motion toward the gate, penalizes motion away from it, and penalizes aggressive and unstable control actions: 


where **v** approach and **v** away are the velocity components toward and away from the gate, respectively. The coefficients _k_ 0 _, k_ 1 _, k_ 2 weight the differentiable reward terms; _k_ 3 is a large positive constant encouraging successful gate passage. 

6 

IEEE ROBOTICS AND AUTOMATION LETTERS 


Fig. 4. The experimental results. **(A)** The predicted trajectory of the target over a 2-second horizon in aggressive tracking. The scattered points denote imagined trajectory samples. **(B)** Heatmaps illustrating the spatial distribution of the target within the quadrotor’s body frame. More intense colors correspond to higher spatial density. The region bounded by the blue rays represents the camera’s actual field of view (FOV). **(C)** The predicted trajectories of the next two gates over a 2-second horizon in dynamic-gate racing. **(D)** The average number of successfully passed gates during dynamic-gate racing. 

## _C. Training Results_ 

On both benchmarks, we train DiffDreamer, DreamerV3, proximal policy optimization (PPO), and backpropagation through time (BPTT), evaluating each across five random seeds to account for statistical variance. Fig. 5 shows the training reward curves. All methods share the same observations, rewards, and uniform randomization of target trajectories, speeds, and initial states, with fixed identified physics parameters. Baselines are tuned individually, while methods in the same methodological family share core hyperparameters, including prediction horizons for differentiable methods. 

The baselines and DiffDreamer share a similar training architecture: DreamerV3 learns the full latent rollout through its world model from these observations; BPTT uses the differentiable quadrotor simulator and differentiable reward terms without a learned latent-imagination pathway; DiffDreamer combines both pathways, using the world model to predict external dynamics and the differentiable simulator to propagate the quadrotor’s physical state. DiffDreamer converges faster and achieves higher final rewards than the baselines in both tasks, with larger gains in dynamic-gate racing. This suggests that coupled latent imagination and differentiable rollouts particularly benefit tasks requiring both future prediction and precise optimization of robot motion. 

## _D. Experimental Performance_ 

We select Elastic Tracker [13] for tracking and the policysearch method [2] for racing as classical planning and control baselines. 

**External-motion Prediction.** The world model and EKF observe the first half of each trajectory and forecast the 


Fig. 5. Training reward curves for aggressive tracking (top) and dynamicgate racing (bottom). Solid lines and shaded regions represent the mean and standard deviation across five independent random seeds, respectively. 

remainder open loop. Fig. 4A and C show that DiffDreamer predicts more precise trajectories than the EKF for agile target motion in both tasks. Without measurement updates, the EKF’s fixed-motion model cannot anticipate subsequent acceleration or maneuver changes, so its errors grow rapidly during agile maneuvers. 

**Aggressive Tracking.** We evaluate trained policies in ten randomized scenarios with aggressive target maneuvers along diverse, unpredictable trajectories. Fig. 4B shows heatmaps of the target’s spatial density in the quadrotor’s body frame 

IEEE ROBOTICS AND AUTOMATION LETTERS 

7 


Fig. 6. Ablation studies. **Left and center:** Odometry/representation ablation: reconstruction-error densities and target distributions in the quadrotor’s XY/XZ planes. Relative and absolute world models are compared with Elastic Tracker (labeled [1]) [13]; blue rays bound the camera field of view. **Right:** Reward ablation: gates passed within 512 steps versus maximum gate speed (m/s), using the full reward or removing the discrete gate-passing or differentiable motion component. 

over entire flights. Concentration around the desired relative position indicates that the policy maintains a stable standoff distance and keeps the target within the camera FOV. DiffDreamer’s distribution is more compact than those of the baselines, especially in the XZ plane, suggesting greater robustness to abrupt vertical target motion. 

DiffDreamer achieves the lowest mean errors on all three tracking metrics in Table I: its mean distance error is 0 _._ 381 m versus 0 _._ 793 m for Elastic Tracker, 0 _._ 835 m for BPTT, and 1 _._ 003 m for DreamerV3. Fig. 6 also shows Elastic Tracker’s target distribution. 

**Dynamic-gate Racing.** We evaluate racing in five randomized environments, each with a sequence of four gates moving along varying trajectories. Three difficulty tiers test robustness at maximum gate translation speeds of 1.0, 1.5, and 2.0 m/s. Fig. 4D reports the primary metric: the average number of gates passed within 512 simulation steps. 

DiffDreamer outperforms all baselines across gate speeds. In Table II, its mean gate counts are 16, 12, and 8 at the three speeds, versus 12, 4, and 1 for MPC. This smaller decline relative to MPC suggests greater robustness to faster gate motion. BPTT’s performance degrades with gate speed, which may be related to its lack of future motion prediction; DreamerV3’s limited performance may reflect the combined complexity of learned physical transitions and sparse gatepassing rewards. 

## _E. Ablations_ 

_1) Odometry and relative-state representation:_ The relative-state formulation combines quadrotor odometry with target-relative observations. The ablated world model removes odometry and reconstructs the target’s absolute position. In Fig. 6, the absolute-position variant has a broader reconstruction-error distribution and a more dispersed target distribution in the quadrotor frame during tracking. 

_2) Reward decomposition:_ We remove each reward component in turn while evaluating dynamic-gate racing at maximum 

TABLE I AGGRESSIVE TRACKING ERRORS. 

||Horizontal|Vertical|Distance|
|---|---|---|---|
|Method|_|eh|_|_|ev|_|_|ed|_ (m)|
|DreamerV3|0_._318_±_0_._275|0_._314_±_0_._307|1_._003_±_0_._556|
|BPTT|0_._198_±_0_._227|0_._235_±_0_._219|0_._835_±_0_._532|
|Elastic Tracker|0_._333_±_0_._306|0_._382_±_0_._305|0_._793_±_0_._404|
|DiffDreamer|**0**_._**168**_±_0_._163|**0**_._**215**_±_0_._177|**0**_._**381**_±_0_._282|


_Notes:_ Values are reported as the mean _±_ standard deviation over random trajectories and time steps. _|eh|_ and _|ev|_ are the normalized horizontal and vertical distances, respectively, from the target’s projection to the image center on the image plane; both are dimensionless. _|ed|_ is the distance error in meters. Lower values are better; bold indicates the best result. Elastic Tracker is the aerial trajectory planner of Ji et al. [13]. 

TABLE II 

DYNAMIC-GATE RACING PERFORMANCE. 

|Method|_v_ = 1_._0|_v_ = 1_._5|_v_ = 2_._0|
|---|---|---|---|
|DreamerV3|3_._0_±_0_._9|1_._0_±_0_._9|0_._0_±_0_._0|
|BPTT|6_._0_±_3_._4|0_._0_±_0_._5|0_._0_±_0_._0|
|PPO|14_._0_±_2_._1|8_._0_±_2_._3|3_._0_±_1_._2|
|MPC|12_._0_±_0_._9|4_._0_±_0_._9|1_._0_±_0_._9|
|DiffDreamer|**16**_._**0**_±_1_._0|**12**_._**0**_±_0_._5|**8**_._**0**_±_1_._4|


_Notes:_ Entries report the number of gates passed within 512 simulation steps as the mean _±_ standard deviation over random trajectories and time steps; _v_ is the maximum gate speed in m/s. Higher values are better; bold indicates the best result. MPC uses the approach of Song and Scaramuzza [2]. 

gate speeds of 1.0, 1.5, and 2.0 m/s. In Fig. 6, the full objective yields gate counts of 16, 12, and 8. Removing the discrete gatepassing reward reduces these counts to 2, 2, and 0. Removing the differentiable motion reward yields 7, 4, and 2. Removing either component reduces the number of gates passed at all three speeds. 

## _F. Real-World Experiments_ 

We evaluate the sim-to-real performance of DiffDreamer policies for both tasks on a custom-built quadrotor with 3.5inch propellers, an NVIDIA Jetson Orin NX onboard computer, and a Betaflight flight controller. The trained policies run onboard at over 100 Hz, sending collective thrust and 

IEEE ROBOTICS AND AUTOMATION LETTERS 

8 

body rate (CTBR) commands to the flight controller. An external motion-capture system provides odometry for the quadrotor and moving targets/gates, allowing us to evaluate DiffDreamer’s control and planning with external state feedback. We carefully identify the quadrotor’s physical parameters and incorporate them into the differentiable simulator to reduce the sim-to-real gap. All experiments use bounded thrust commands for safety in a controlled indoor environment. The successful trajectories in Fig. 3 provide proof-of-concept evidence of transfer to physical flight under calibrated dynamics and motion-capture state feedback. 

## V. CONCLUSION 

We presented DiffDreamer, a differentiable reinforcement learning framework for agile quadrotor tasks that require both external-motion prediction and precise physical control. During actor optimization, DiffDreamer couples two rollouts: the learned world model propagates latent states capturing external dynamics and history-dependent features, while the differentiable simulator propagates the robot’s explicit physical state. This separation reduces the burden of learning highfrequency robot dynamics within the world model. The actor objective is decomposed into a critic-driven pathway for nondifferentiable task rewards and a simulator-driven pathway for differentiable motion rewards. Experiments on aggressive tracking and dynamic-gate racing show improved training convergence over model-free, model-based, and differentiable-RL baselines, and higher final performance than these baselines and classical planning and control methods. Ablation studies assess the contributions of reward decomposition and the odometry-conditioned relative-state representation. Real-world flight experiments further provide proof-of-concept validation. 

## VI. LIMITATIONS AND DISCUSSION 

DiffDreamer has been evaluated only on quadrotors. Extending its coupled latent/physical rollouts and reward decomposition to other embodiments requires suitable differentiable models and additional task-specific engineering. Contacts, discontinuities, actuator limits, and perception modules can complicate differentiation [29]. In addition, real-world validation relies on motion-capture feedback for both the vehicle and external objects. Fully onboard perception and robustness to perception noise remain untested. 

## REFERENCES 

- [1] E. Kaufmann, A. Loquercio, R. Ranftl, A. Dosovitskiy, V. Koltun, and D. Scaramuzza, “Deep drone racing: Learning agile flight in dynamic environments,” in _Conference on Robot Learning_ . PMLR, 2018, pp. 133–145. 

- [2] Y. Song and D. Scaramuzza, “Policy search for model predictive control with application to agile drone flight,” _IEEE Transactions on Robotics_ , vol. 38, no. 4, pp. 2114–2130, 2022. 

- [3] R. Römer, T. Emmert, and A. P. Schoellig, “Flying through moving gates without full state estimation,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9906–9912. 

- [4] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” _arXiv preprint arXiv:1912.01603_ , 2019. 

   - [6] J. Xu, V. Makoviychuk, Y. Narang, F. Ramos, W. Matusik, A. Garg, and M. Macklin, “Accelerated Policy Learning with Parallel Differentiable Simulation,” Apr. 2022, arXiv:2204.07137. [Online]. Available: http://arxiv.org/abs/2204.07137 

   - [7] M. A. Z. Mora, M. Peychev, S. Ha, M. Vechev, and S. Coros, “Pods: Policy optimization via differentiable simulation,” in _International Conference on Machine Learning_ . PMLR, 2021, pp. 7805–7817. 

   - [8] D. Hanover, A. Loquercio, L. Bauersfeld, A. Romero, R. Penicka, Y. Song, G. Cioffi, E. Kaufmann, and D. Scaramuzza, “Autonomous drone racing: A survey,” _IEEE Transactions on Robotics_ , vol. 40, pp. 3044–3067, 2024. 

   - [9] P. Foehn, D. Brescianini, E. Kaufmann, T. Cieslewski, M. Gehrig, M. Muglikar, and D. Scaramuzza, “Alphapilot: Autonomous drone racing,” _Autonomous Robots_ , vol. 46, no. 1, pp. 307–320, 2022. 

   - [10] P. Foehn, A. Romero, and D. Scaramuzza, “Time-optimal planning for quadrotor waypoint flight,” _Science robotics_ , vol. 6, no. 56, p. eabh1221, 2021. 

   - [11] A. Romero, S. Sun, P. Foehn, and D. Scaramuzza, “Model predictive contouring control for time-optimal quadrotor flight,” _IEEE Transactions on Robotics_ , vol. 38, no. 6, pp. 3340–3356, 2022. 

   - [12] M. Krinner, A. Romero, L. Bauersfeld, M. Zeilinger, A. Carron, and D. Scaramuzza, “Mpcc++: Model predictive contouring control for timeoptimal flight with safety constraints,” _arXiv preprint arXiv:2403.17551_ , 2024. 

   - [13] J. Ji, N. Pan, C. Xu, and F. Gao, “Elastic Tracker: A spatio-temporal trajectory planner for flexible aerial tracking,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 47–53. 

   - [14] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [15] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” in _International conference on machine learning_ . Pmlr, 2018, pp. 1861–1870. 

   - [16] M. Deisenroth and C. E. Rasmussen, “Pilco: A model-based and data-efficient approach to policy search,” in _Proceedings of the 28th International Conference on machine learning (ICML-11)_ , 2011, pp. 465–472. 

   - [17] K. Chua, R. Calandra, R. McAllister, and S. Levine, “Deep reinforcement learning in a handful of trials using probabilistic dynamics models,” _Advances in neural information processing systems_ , vol. 31, 2018. 

   - [18] M. Janner, J. Fu, M. Zhang, and S. Levine, “When to trust your model: Model-based policy optimization,” _Advances in neural information processing systems_ , vol. 32, 2019. 

   - [19] J. Schrittwieser, I. Antonoglou, T. Hubert, K. Simonyan, L. Sifre, S. Schmitt, A. Guez, E. Lockhart, D. Hassabis, T. Graepel _et al._ , “Mastering atari, go, chess and shogi by planning with a learned model,” _Nature_ , vol. 588, no. 7839, pp. 604–609, 2020. 

   - [20] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” _arXiv preprint arXiv:2301.04104_ , 2023. 

   - [21] N. Hansen, X. Wang, and H. Su, “Temporal difference learning for model predictive control,” _arXiv preprint arXiv:2203.04955_ , 2022. 

   - [22] N. Hansen, H. Su, and X. Wang, “Td-mpc2: Scalable, robust world models for continuous control,” _arXiv preprint arXiv:2310.16828_ , 2023. 

   - [23] T. M. Moerland, J. Broekens, A. Plaat, and C. M. Jonker, “Model-based reinforcement learning: A survey,” _Foundations and Trends in Machine Learning_ , vol. 16, no. 1, pp. 1–118, 2023. 

   - [24] R. S. Sutton, A. G. Barto _et al._ , _Reinforcement learning: An introduction_ . MIT press Cambridge, 1998, vol. 1, no. 1. 

   - [25] C. Schwarke, V. Klemm, J. Bagajo, J.-P. Sleiman, I. Georgiev, J. Tordesillas, and M. Hutter, “Learning deployable locomotion control via differentiable simulation,” _arXiv preprint arXiv:2404.02887_ , 2024. 

   - [26] Y. Zhang, Y. Hu, Y. Song, D. Zou, and W. Lin, “Learning vision-based agile flight via differentiable physics,” _Nature Machine Intelligence_ , vol. 7, no. 6, pp. 954–966, 2025. 

   - [27] F. Li, F. Sun, T. Zhang, and D. Zou, “Visfly: An efficient and versatile simulator for training vision-based flight,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 11 325–11 332. 

   - [28] F. Li, S. Wang, F. Sun, S. Wu, D. Zuo, W. Yu, and D. Zou, “Stabletracker: Learning to stably track target via differentiable simulation,” _arXiv preprint arXiv:2509.14147_ , 2025. 

   - [29] L. Metz, C. D. Freeman, S. S. Schoenholz, and T. Kachman, “Gradients are not all you need,” _arXiv preprint arXiv:2111.05803_ , 2021. 

- [5] D. Hafner, T. Lillicrap, M. Norouzi, and J. Ba, “Mastering atari with discrete world models,” _arXiv preprint arXiv:2010.02193_ , 2020. 

