---
title: "PCHC: Enabling Preference Conditioned Humanoid Control via Multi-Objective Reinforcement Learning"
date: "2026-03-25"
authors: "Huanyu Li; Dewei Wang; Xinmiao Wang; Xinzhe Liu; Peng Liu; Chenjia Bai"
url: https://arxiv.org/abs/2603.24047
pdf: https://arxiv.org/pdf/2603.24047
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.24047)** / [論文ページ](https://arxiv.org/abs/2603.24047)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **PCHC: Enabling Preference Conditioned Humanoid Control via Multi-Objective Reinforcement Learning** 

Huanyu Li<sup>1</sup> , Dewei Wang<sup>2</sup> , Xinmiao Wang<sup>3</sup> , Xinzhe Liu<sup>4</sup> , Peng Liu<sup>1</sup><sup>_†_</sup> , Chenjia Bai<sup>5</sup><sup>_†_</sup> , Xuelong Li<sup>5</sup> 

**_Abstract_ — Humanoid robots often need to balance competing objectives, such as maximizing speed while minimizing energy consumption. While current reinforcement learning (RL) methods can master complex skills like fall recovery and perceptive locomotion, they are constrained by fixed weighting strategies that produce a single suboptimal policy, rather than providing a diverse set of solutions for sophisticated multiobjective control. In this paper, we propose a novel framework leveraging Multi-Objective Reinforcement Learning (MORL) to achieve Preference-Conditioned Humanoid Control (PCHC). Unlike conventional methods that require training a series of policies to approximate the Pareto front, our framework enables a single, preference-conditioned policy to exhibit a wide spectrum of diverse behaviors. To effectively integrate these requirements, we introduce a Beta distribution-based alignment mechanism based on preference vectors modulating a Mixtureof-Experts (MoE) module. We validated our approach on two representative humanoid tasks. Extensive simulations and realworld experiments demonstrate that the proposed framework allows the robot to adaptively shift its objective priorities in real-time based on the input preference condition.** 

## I. INTRODUCTION 

Humanoid robots represent a premier embodied platform for replacing humans in hazardous environments and laborintensive tasks. While Model Predictive Control (MPC) has traditionally enabled locomotion across diverse terrains [1], [2], Reinforcement Learning (RL) [3], empowered by high-performance parallel simulators [4], [5], has recently achieved unprecedented robustness in complex control scenarios. Current RL frameworks, particularly those utilizing policy gradient methods [6], [7], have successfully addressed challenging tasks including fall recovery [8], [9], blind locomotion over uneven ground [10]–[12], vision-based locomotion [13]–[16]. Despite these advancements, these methods typically rely on predefined weights to scalarize competing reward objectives, ultimately collapsing the multi-faceted nature of the task into a rigid, single-objective policy. 

In the real world, many complex control problems, such as humanoid robot locomotion [17], intrinsically involve multiple conflicting objectives that cannot be optimized simultaneously. Single-objective RL approaches typically rely on manually tuned, fixed reward weights to balance these competing objectives, yielding static behaviors that cannot dynamically adapt to changing environmental demands or shifting user priorities during deployment. Multi-objective 

> 1Harbin Institute of Technology 

> 2University of Science and Technology of China 

> 3Harbin Engineering University 

> 4ShanghaiTech University 

> 5Institute of Artificial Intelligence (TeleAI), China Telecom 

> _†_ Corresponding authors 


Fig. 1: _PCHC_ integrates MORL with humanoid control tasks which enables the robot perform different multi-objective preference-aligned behaviors given preference vector **_λ_** . For example, _PCHC_ enables the robot to balance stride length and disturbance resistance in the humanoid walking task. 

reinforcement learning (MORL) [18], [19], which aims to approximate the Pareto front [20], provides a highly suitable solution. While many existing Q-learning [21]–[23] and policy gradient [24]–[26] methods have been developed, extending these paradigms to high-dimensional continuous humanoid control remains a formidable challenge, as it requires balancing the explosion of the state-action space with the intricate, multi-objective trade-offs inherent in complex dynamics. This dynamic adaptability is especially critical for humanoid robots, which must reconcile competing priorities ranging from speed and energy efficiency in industrial logistics to stability and agility in search-and-rescue operations. Despite its potential, the application of MORL to humanoid locomotion remains non-trivial. Unlike standard MORL benchmarks that rely on simplified environments [27], humanoid control involves high-dimensional dynamics and a multitude of dense, manually crafted reward functions [9], [10], [13]. Consequently, developing a unified multiobjective humanoid control policy capable of navigating these complex Pareto trade-offs in real-time remains an unresolved challenge. 

In this paper, we propose _PCHC_ , a novel framework that enables a single, unified policy to achieve versatile humanoid control while satisfying multiple preferenceconditioned objectives. We formulate preference-conditioned humanoid control as a Multi-Objective Reinforcement Learning (MORL) problem, aiming to approximate the Paretooptimal front. To eliminate the overhead of policy switching, 

PCHC trains a preference-conditioned policy that employs linear scalarization across diverse objectives. Given that RL-based humanoid control typically involves an extensive array of reward functions, we distinguish between objectivespecific rewards and auxiliary rewards. Specifically, only the rewards directly relevant to target-specific objectives are subjected to preference-based scalarization during training, while auxiliary rewards remain invariant to ensure fundamental stability. To effectively map preference vectors to robot behaviors, we introduce a multi-expert network architecture where expert routing is governed not by a gating network, but by a Beta distribution parameterized by the preference vector. Each expert implicitly acquires preference-aligned knowledge, and the entire ensemble is trained to approximate the Pareto front through a guided, weighted aggregation. 

We evaluate _PCHC_ on two humanoid tasks: walking and fall recovery, both characterized by intrinsically conflicting objectives. Specifically, we investigate the trade-offs between disturbance resistance versus stride length in walking, and disturbance resistance versus energy efficiency in fall recovery. Experimental results demonstrate that _PCHC_ can dynamically shift its behavioral priorities across the Pareto front based on the input preference vector. Our primary contributions are summarized as follows: 

- We propose _PCHC_ that integrates MORL with humanoid control to obtain distinct policy outputs conditioned on different preferences over objectives. 

- We design a multi-expert module combined with a preference-parameterized Beta distribution to perform preference injection. 

- We validate the proposed framework on two humanoid robot tasks and demonstrate its effectiveness across multiple metrics through extensive simulation and realworld experiments. 

## II. RELATED WORK 

## _A. Humanoid Control with Reinforcement Learning_ 

RL algorithms [3], [6] are now widely applied to humanoid robot control, greatly unlocking the potential of humanoid robots [10]–[16], [28]–[30]. Humanoid robots are capable of walking on uneven terrains [10], [11], while the use of external sensors such as LiDAR or depth cameras enables them to handle more complex scenarios with improved stability [13]– [15]. By training policies to track human motion, humanoid robots can perform tasks such as dancing through real-time tracking of human body poses [29], [31], [32]. Fall recovery [8], [9] and walking [28], [33] are fundamental and essential skills for humanoid robots, Host [9] employs multi-critic RL [34] and a multi-stage framework to achieve recovery to standing from various falling postures and terrains. Walking on complex terrains has been addressed through reward function design, policy distillation, and privileged information reconstruction [10], [13], [14], [16]. Most of these approaches rely on training in simulation [4], [5] and employ techniques such as domain randomization to mitigate the sim-to-real gap. However, existing works fail to accommodate multiple, 

and often conflicting, objectives under varying preference conditions which would enable policies to achieve better adaptability across different situations. 

## _B. Multi-Objective Reinforcement Learning_ 

Existing MORL algorithms can be classified as multipolicy and single policy. Multi-policy approaches [21], [23] seek to learn a collection of policies that collectively approximate the Pareto front. In contrast, single-policy methods [22], [25], [35] convert a multi-objective problem into a single-objective one by aggregating multiple rewards into a scalar value using a scalarization function. In addition, early works [21]–[23] primarily follow the Q-learning paradigm, where the agent learns to approximate the value function for different preference weights. Recently, with the success of policy-gradient algorithms in continuous control, some studies have extended them to MORL by incorporating objective weights [25], [26] or distributional value function into the policy optimization process [24]. Meanwhile, MORL has gradually been adopted in fine-tuning of large language models (LLMs) [36], [37] to balance multiple reward signals. This also offering insights into preference-conditioned optimization strategies applicable to robotics. Existing works on MORL for robot control have remained in toy scenarios like MO-Gym [27]. In this work, we extend MORL to complex humanoid control tasks and validate our approach through both simulation and real-world experiments. 

## III. METHOD 

## _A. Preliminaries_ 

We formulate the humanoid control problem as an RL problem, which can be modeled as a Markov Decision Process (MDP) formally described by a tuple ( _S, A, P, R, γ, ρ_ 0). Here, _S_ denotes the state space, _A_ represents the action space, _P_ is the state transition probability, _R_ is the reward function, _γ_ is the discount factor, and _ρ_ 0 is the initial state distribution. While standard RL focuses on a single reward signal, many real-world tasks involve multiple, often conflicting objectives. This motivates MORL, which extends the standard MDP to a multi-objective MDP (MOMDP). 

In MOMDPs, the reward function _R_ : _S×A →_ R<sup>_m_</sup> returns a reward vector **r** = ( _r_ 1 _, r_ 2 _, . . . , rm_ ), where _m_ denotes the number of objectives. The value function of a policy _π_ is defined as 


To compare two policies in a multi-objective setting, their values are evaluated across all objectives. A policy _π_ 1 is said to dominate another policy _π_ 2 if and only if it improves at least one objective without reducing the values of the others. As a result, the set of undominated policies forms the Pareto front: 


where _≻P_ is the Pareto dominance relation: 


Fig. 2: Overview of the proposed _PCHC_ framework. _PCHC_ adopts multiple critics and employs a _Preference Condition Injection_ module based on a preference-parameterized Beta distribution achieving multi-objective control on two humanoid control tasks. 

## and Π is the set of all possible policies. 

For complex humanoid control tasks, obtaining the exact Pareto front is practically infeasible. Therefore, the goal of multi-objective optimization is to approximate the Pareto front as closely as possible. To evaluate the approximated Pareto front, two commonly used metrics are considered: hypervolume, which reflects the coverage of the objective space, and sparsity, which indicates the diversity of solutions. Let _P_ = _{p_ 1 _, p_ 2 _, . . . , pn} ⊂_ R<sup>_m_</sup> denote an approximation of Pareto front containing _n_ solutions, where each solution _pi_ corresponds to the values of _m_ objectives. The hypervolume indicator quantifies the volume of the objective space dominated by the Pareto front. Formally, it is defined as 


where _r ∈_ R<sup>_m_</sup> is a reference point, [ _p, r_ ] denotes the hyperrectangle spanning from _p_ to _r_ across all dimensions, and Λ( _·_ ) represents the Lebesgue measure (i.e., the volume). For the same P, sparsity is defined as: 


where _Pi_ is the _i_<sup>th</sup> solution in _P_ and _Pij_ means the value _j_<sup>th</sup> objective. It is evident that a larger hypervolume indicates a 


Fig. 3: In two-objective space: (a) Hypervolume is represented with the shaded area bounded by the Pareto points and the reference point. (b) Sparsity measures the average square distance between consecutive points. 

better approximation of the Pareto front, while lower sparsity values reflect a denser distribution of solutions. 

## _B. Preference-Conditioned Humanoid Control_ 

An overview of the proposed framework and conflicting objectives of two humanoid control tasks are shown in Fig. 2. Unlike multi-policy approaches that train a set of policies to approximate the Pareto front, we adopt a single-policy formulation in order to dynamically adapt the policy. To achieve this, we condition the policy on a preference vector that specifies the relative importance of multiple objectives. Formally, we define a preference vector **_λ_** _∈_ R<sup>_m_</sup> , where each entry _λi ≥_ 0 corresponds to the weight of objective _i_ , and the vector lies on the probability simplex, i.e.,<sup>�</sup><sup>_m_</sup> _i_ =1<sup>_λi_= 1.</sup> During training, **_λ_** is sampled from a Dirichlet distribution and concatenated with the other observation of the robot. 

A key challenge in preference-conditioned training is accurate value estimation under dynamic preference vector. Inspired by previous methods [9], [34], we adopt multiple critics to estimate returns, where one critic is assigned to evaluate the task-related return and additional critics are assigned to estimate each objective-specific return. We employ GAE [38] to estimate the advantage for each critic, and then compute a weighted sum to obtain the overall advantage. The final preference-conditioned advantage is thus obtained as 


where _A_<sup>ˆobj</sup> _i_ and _A_<sup>ˆtask</sup> denote the normalized advantage for objective-related and task-related rewards, respectively. This formulation enables the policy update to dynamically reflect the user-specified trade-off among conflicting objectives while consistently enforcing essential task constraints. The preference-conditioned policy is optimized using Proximal Policy Optimization (PPO) [6]. Specifically, with a mimibatch _{_ ( _sk, ak, A_<sup>ˆ</sup><sup>_λ_</sup> _k_<sup>)</sup><sup>_}k_,thelossoftheactorisdefinedas:</sup> 


where _rk_ ( _θ_ ) = _ππ_ ref _<u>θ</u>_ <u>((</u> _aakk||sskk,,_ **_λλ_** <u>))</u><sup>,</sup><sup>_π_refisthepolicydirectlyafter</sup> sampling the trajectory. 

## _C. Preference Condition Injection_ 

Directly concatenating the preference vector **_λ_** with other observation as policy input is often insufficient, since the mapping from preference condition to low-level motor behaviors in humanoid control is highly non-linear and complex. To address this, we propose a _Preference Condition Injection_ module, which consists of multiple experts and a Beta distribution parameterized by the preference vector. Instead of relying on a gating network to determine expert routing, we parameterize a Beta distribution using the preference vector, and sample routing weights from this distribution. For two conflicting objectives, the preference vector _λ_ lies on a 1D probability simplex. The Beta distribution is uniquely suited for this architecture as the equivalent of a two-dimensional Dirichlet distribution. Its domain naturally aligns with the [0 _,_ 1] interval of interpolating between two conflicting objectives, providing mathematically bounded and smooth density curves that enforce a structured interpolation between experts along the Pareto front. Given a preference vector **_λ_** = [ _λ_ 1 _, λ_ 2], we define the Beta distribution parameters as _α_ = _α_ 0 + _λ_ 1 _· s, β_ = _β_ 0 + _λ_ 2 _· s,_ where _α_ 0 _, β_ 0 _>_ 0 are base offsets and _s_ is a scaling factor. For each expert branch _j ∈{_ 1 _, . . . , NB}_ with fixed position _xj ∈_ [0 _,_ 1], the unnormalized weight is computed by evaluating the Beta density: 


where _B_ ( _α, β_ ) = �01<sup>_tα−_1(1</sup><sup>_−t_)</sup><sup>_β−_1</sup><sup>_dt_istheBetafunction.</sup> The final routing weights are first normalized. Each expert network receives the current observation as well as the output from the history encoder as shown in Fig. 2. Their outputs are aggregated through a weighted sum according to the routing weights _w_ ˜ _j_ . Each expert in the multi-expert actor network implicitly learns a distinct solution on the Pareto front. By determining their routing weights through a preferenceparameterized Beta distribution, the framework can leverage the interpolation of these expert network outputs to better generate solutions at other points on the Pareto front. To ensure a comprehensive representation of the Pareto front without introducing excessive complexity, we set the number of experts to _NB_ = 5 in our implementation. Their fixed positions _xj_ are evenly distributed at 0.0, 0.25, 0.5, 0.75, and 1.0 along the objective space. 

positions and velocities, _at−_ 1 is the previous action, _η ∈_ (0 _,_ 1] is a action scaling factor. For policy learning, both the actor and critic receive as input a combination of five history states and current state, which provides temporal context for decision making in both tasks. The predicted action _at_ is mapped to target joint positions through _qt_<sup>target</sup> = _q_<sup>default</sup> + _ηat_ , where _q_<sup>default</sup> is the nominal joint configuration. The corresponding motor torques are then computed by a jointlevel PD controller as 


with _Kp_ and _Kd_ denoting the stiffness and damping gains, respectively. 

For the reward function design of the two tasks, we referred to prior work [9], [13], [39] and additionally incorporated reward terms related to multiple objectives, which are described in §III-D.1 and §III-D.2. To encourage natural behaviors, we also adopt the Adversarial Motion Prior (AMP) [40]-based reward during the training process. AMP provides a style reward _r_<sup>style</sup> by training a discriminator _Dϕ_ to distinguish between reference motion data and policygenerated trajectories. The discriminator operates on an AMP state sequence _τt_ = [ _s_<sup>amp</sup> _t−_ 4<sup>_, s_amp</sup> _t−_ 3<sup>_, . . . , s_</sup> _t_<sup>amp</sup> ], where each AMP state _s_<sup>amp</sup> _t ∈_ R<sup>20</sup> is constructed from the 20 joint positions. The discriminator is trained with the following objective: 

arg max E _τ ∼M_ [( _Dϕ_ ( _τ_ ) _−_ 1)<sup>2</sup> ] + E _τ ∼P_ [( _Dϕ_ ( _τ_ ) + 1)<sup>2</sup> ] _ϕ_ +<sup>_α_</sup> 2<sup>_d_E</sup><sup>_τ∼M_[</sup><sup>_∥∇ϕDϕ_(</sup><sup>_τ_)</sup><sup>_∥_2]</sup><sup>_,_</sup> (11) 

where _M_ is the reference dataset, _P_ contains policy rollouts, and _α_<sup>_d_</sup> is a regularization coefficient. The discriminator output _Dϕ_ ( _τt_ ) _∈_ R is then converted into a smooth reward: 


where _c_ is a manually specified scaling factor. In our setup, each task employs a separate discriminator trained on its corresponding reference motion dataset: for _Walking_ , we adopt the motions from the LAFAN1 Retargeting Dataset, while for _Fall Recovery_ task, we use motions captured and retargeted by ourselves. 

_1) Humanoid Walking:_ In this task, the policy controls 20 actuated joints of the humanoid. Besides the proprioceptive information and preference vector, the velocity commands **v** cmd _∈_ R<sup>3</sup> are also provided as part of the observation input. We define two conflicting objectives for this task: **stride length** and **disturbance resistance** , which are quantified by their corresponding reward functions as follows: 

## _D. Humanoid Control Task_ 

We focus on two humanoid control tasks in this paper: _Fall Recovery_ and _Walking_ . Both tasks rely solely on proprioceptive information. At timestep _t_ , the state is defined as 


where _ωt ∈_ R<sup>3</sup> is the base angular velocity, _gt ∈_ R<sup>3</sup> denotes the gravity vector in the base frame, _qt_ and _q_ ˙ _t_ are the joint 


where Icontact and Iafter-disturb are indicator functions used to determine whether a foot is in contact and whether the current step is within a period of time after a disturbance, **p** current and **p** last ~~c~~ ontact<sup>isthefootpos,</sup><sup>**x**</sup> base<sup>and</sup> **x** last denote the horizontal base positions before and after 

TABLE I: Performance evaluation on the fall recovery task. 

|**Objective**|||**Energ**|**y Efficiency**|||**Disturbanc**|**e Robustness**|
|---|---|---|---|---|---|---|---|---|
|Preference<br>Metrics|Avg. Energy<br>Overall (J)|Avg. Energy<br>Fall Recovery (J)|Avg. Energy<br>Recovery (J)|Avg. Torque<br>Overall (Nm)|Avg. Torque<br>Fall Recovery (Nm)|Avg. Torque<br>Recovery (Nm)|COM<br>displacement|(m)<br>Success<br>rate (%)|
||||**P**|**CHC (ours)**|||||
|(1.00, 0.00)|**463.45**|**743.14**|**416.96**|**223.90**|**223.01**|**224.17**|1.82|62.24|
|(0.75, 0.25)|480.58|747.43|435.15|241.31|227.86|245.31|1.73|67.95|
|(0.50, 0.50)|517.90|787.09|476.94|243.04|227.26|246.00|1.62|75.73|
|(0.25, 0.75)|583.31|807.77|550.13|249.08|229.82|251.93|1.12|91.95|
|(0.00, 1.00)|666.24|790.43|646.83|256.23|232.33|260.55|**0.75**|**96.56**|
|||||**HoST**|||||
||550.15|745.25|467.67|235.65|224.02|240.18|1.69|69.22|


TABLE II: Performance evaluation on the locomotion task. 

|Preference<br>Metrics|Avg. Stride<br>Traj.|Deviation|
|---|---|---|
|(0.00, 1.00)|**0.79**|0.85|
|(0.25, 0.75)|0.72|0.51|
|(0.50, 0.50)|0.67|0.33|
|(0.75, 0.25)|0.55|0.29|
|(0.10, 0.00)|0.42|**0.23**|
|Baseline|0.59|0.46|


an external disturbance, **v** base is linear velocity of the base, **d** ˆ is unit vector in the disturbance direction. The stride length objective encourages the policy to take larger steps. In contrast, disturbance resistance emphasizes stability and robustness against disturbance, often resulting in shorter and more conservative steps. Through preference-conditioned optimization, our framework enables the humanoid to modulate its gait to favor either longer strides or stronger robustness. 

_2) Humanoid Fall Recovery:_ The _Fall Recovery_ task trains the humanoid to rise from a prone posture. Here, the policy controls 23 actuated joints. Similar to the walking task, we consider **disturbance resistance** and **energy efficiency** as the multi-objective setting. The energy efficiency reward function is designed as follows: 


where _N_ dof is the number of actuated joints, _q_ ˙ _j_ and _τj_ are the velocity and torque of joint _j_ , and _κτ , κp >_ 0 are scaling coefficients. The disturbance resistance reward function is same as the walking task. Disturbance resistance requires the policy to maintain robustness against external disturbance applied during both the recovery phase and the subsequent standing posture. Energy efficiency, on the other hand, encourages the policy to minimize torque consumption through the whole process. These two objectives are inherently conflicting since stronger disturbance resistance typically demands higher torque expenditure. Note that excessive coefficients in _r_ energy may hinder the robot from standing. 

## IV. RESULT AND DISCUSSION 

We conduct parallel training using the Isaac Gym simulator. Each training iteration aggregates experience from 4096 parallel environments, with each episode lasting 10 seconds. The entire training process was performed on a single NVIDIA GeForce RTX 4090 GPU. For both the walking and fall recovery tasks, each policy was trained for a total of 12000 iterations. The control policy operates at 50 Hz and outputs target joint positions, which are tracked by a PD controller running at 500 Hz to compute the corresponding joint torques. The policy is trained and deployed specifically for the Unitree G1 humanoid robot. To ensure efficient realtime inference, the model is converted to the Open Neural Network Exchange (ONNX) format and executed on the robot’s onboard computer. 

## _A. Simulation Result_ 

_a) Fall Recovery task:_ We first evaluate _PCHC_ on the humanoid fall recovery task, where the robot starts from a prone posture. To study how preferences affect the learned behaviors, we vary the preference vector **_λ_** = ( _λ_ 1 _, λ_ 2) across five settings, ranging from _λ_ = (1 _._ 0 _,_ 0 _._ 0), which prioritizes energy efficiency, to **_λ_** = (0 _._ 0 _,_ 1 _._ 0), which emphasizes robustness against disturbance. Each policy is evaluated in 1000 parallel environments. We report results across multiple metrics: (1) **Average energy consumption** , reported in Joules (J), including both the overall value across the entire process and the decomposed values for the recovery phase and the standing phase; (2) **Average joint torque** , measured in Newton–meters (Nm), also reported as an overall value and further separated into the recovery and standing phases; (3) Disturbance robustness under small disturbance, measured by the **COM displacement** in meters(m) after mild pushes; and (4) **Success rate** defined as the percentage (%) of trials in which the robot remains standing without falling when subjected to strong external disturbances. Baseline is HoST [8] augmented with AMP motion priors. 

As shown in Table I, _PCHC_ effectively adapts its behavior according to the preference vector. When prioritizing energy efficiency, the policy exhibits reduced robustness and success rate under perturbations. Conversely, when robustness is emphasized, the policy maintains stable standing under large disturbances with increased energy consumption. Intermediate preferences yield smooth trade-offs between these 


preference vector **_λ_** on _Fall Recovery_ and _Walking_ task. 

Fig. 4: The performance of our policy with different 


Similar to the fall recovery task, to examine how preference conditioning influences gait behavior, we vary the preference vector **_λ_** = [ _λ_ 1 _, λ_ 2] across five setting for comparison. Each trained policy is tested in 1000 parallel rollouts, and we record the average **stride length** and **trajectory deviation** both expressed in meters (m). For reference, we include a baseline policy that follows the design of prior approaches [9], [10], [13]. 

As summarized in Table II, different preferences lead to different locomotion styles. When stride length is prioritized ( **_λ_** = [0 _._ 0 _,_ 1 _._ 0]), the robot takes larger steps but suffers from increased trajectory deviation. Conversely, when stability is emphasized ( **_λ_** = [1 _._ 0 _,_ 0 _._ 0]), the policy achieves minimal trajectory deviation but at the cost of shorter strides. Besides, the results showing that intermediate preferences produce gradual transitions, indicating that the policy flexibly balances the two objectives. Similarly, Fig. 4(b) illustrates representative simulation results under three preference settings, providing a direct visualization of how preferences modulate the trade-off between stride length and stability. 

Fig. 5: Demonstration of dynamic preference switching during task execution. The preference vector **_λ_** is instantaneously adjusted from [0.0, 1.0] to [1.0, 0.0]. 

two extremes, producing balanced solutions. In addition, we record the **step-wise energy consumption** throughout the entire fall recovery process (Fig. 4(a)), comparing three representative preferences. The curves show how different preference settings modulate energy usage, further validating the role of preference conditioning in shaping task behaviors. 

From the perspective of Pareto front (PF) analysis, HoST corresponds to a single fixed solution, which is strictly dominated by multiple solutions obtained through _PCHC_ . In other words, for the same or lower energy consumption, _PCHC_ achieves higher robustness, while for the same robustness, it yields lower energy consumption. This shows that the baseline solution lies inside the dominated region, whereas _PCHC_ spans a broader set of non-dominated points approximating the Pareto front.These results show that preference conditioning enables _PCHC_ to flexibly navigate the tradeoff between energy consumption and disturbance resistance in the fall recovery task. By adjusting the preference vector, the policy smoothly interpolates between behaviors, showing that the baseline lies within the dominated region. 

Compared to the baseline, which remains confined to a single operating point, _PCHC_ covers a much broader portion of the stride–stability spectrum. Instead of being restricted to a fixed compromise, the preference-conditioned policies provide a continuous set of solutions: some achieve longer strides with larger deviations, while others ensure highly stable trajectories at the cost of reduced stride length. This diversity demonstrates that preference conditioning enables the locomotion policy to adapt flexibly to different requirements, whereas the baseline remains dominated by multiple solutions obtained through _PCHC_ . 

To evaluate the robustness of our framework under changing requirements, we further tested the policy’s ability to handle dynamic preference switching during task execution. As shown in Fig. 5, the preference vector **_λ_** is instanta- 

_b) Walking task.:_ We further evaluate the locomotion performance of _PCHC_ on the walking task, where the humanoid is commanded to walk forward on flat terrain. 


Fig. 6: Ablation study comparing our PCI module (w/ PCI) against a standard trainable gating network (w/o PCI). 


Fig. 7: Real world experiments results of fall recovery task on a Unitree G1 robot. 

neously altered while the humanoid is executing the task. The policy demonstrates the capability to seamlessly transition its behavior in real-time without any instability or failure. This confirms that the PCHC framework is not limited to static preference settings, but can dynamically and safely adapt to evolving objective priorities in complex environments. 

_c) Ablation on Preference Condition Injection:_ To evaluate the effectiveness of the proposed Preference Condition Injection (PCI) module, we compare it against a standard trainable gating network. As illustrated by the Pareto front (PF) curves in Fig. 6, removing the PCI module leads to a noticeable contraction of the front both in the fall recovery task and walking task. To quantify these differences, we compute the **hypervolume** and **sparsity** of the obtained PFs. On the fall recovery task, the PCI-enabled policy achieves a hypervolume of 313.78 compared to 306.02 without PCI, with sparsity reduced from 3493.85 to 3210.61. On the walking task, the hypervolume increases from 0.14 to 0.20, while sparsity shows little change. These results confirm that our Beta-distribution based routing provides superior coverage of the objective space and a more faithful approximation of the Pareto front than a conventional gating architecture. 

_d) Compared with fixed preference:_ During training, _PCHC_ randomly samples a preference vector **_λ_** and concatenates it with the robot’s observation, so that a single policy 


Fig. 8: Objective space evaluation of PCHC, Fixed **_λ_** policies, and Baseline. 

can adapt to different trade-offs. An important concern is whether introducing preference conditioning would compromise the performance at individual trade-off points compared to policies trained with fixed preference vector. To verify this, we trained fixed-preference policies for both tasks, each with a specific preference vector **_λ_** . As shown in Fig. 8, the results demonstrate that _PCHC_ achieves comparable performance at the corresponding preferences. This indicates that Preference conditioning retains fixed-preference training effectiveness and extends it to a continuous solution set in a single policy. 

## _B. Real-world Result_ 

We deploy the trained _PCHC_ policies onto a Unitree G1 humanoid robot to directly examine their sim-to-real transfer under different preferences. 

_a) fall recovery task:_ This task involves a trade-off between energy efficiency and robustness to external pushes. As illustrated in Fig. 7, with **_λ_** = [1 _._ 0 _,_ 0 _._ 0] the robot rises with relatively low torque effort but quickly loses balance when disturbed. In contrast, with **_λ_** = [0 _._ 0 _,_ 1 _._ 0] the robot generates stronger and more stable motions that enable it to withstand the same perturbations, though at the cost of higher joint effort. 

_b) Walking task:_ For locomotion, the objectives are stride length and stability. As shown in Fig. 1, under **_λ_** = [0 _._ 0 _,_ 1 _._ 0] the robot achieves longer strides but shows larger trajectory deviation when external forces are applied. Conversely, with **_λ_** = [1 _._ 0 _,_ 0 _._ 0] the robot maintains better disturbance resistance, albeit with shorter steps. 

## V. CONCLUSION 

In this paper, we propose _PCHC_ framework which enables a single policy to perform preference-aligned humanoid behaviors. By leveraging the Beta distribution parameterized by the preference vector, the _PCI_ module efficiently enables the policy to satisfy specified objective trade-offs. However, our framework is primarily applicable to tasks with two objectives, whereas many conflicting objectives in humanoid tasks require scenario-dependent consideration. Moreover, our approach has been applied only to blind humanoid control tasks, without integrating external sensors. Future work will consider a broader range of objectives requiring trade-offs and vision-based tasks. 

REFERENCES 

- [1] Y. Gao, V. Paredes, Y. Gong, Z. He, A. Hereid, and Y. Gu, “Time-varying foot-placement control for underactuated humanoid walking on swaying rigid surfaces,” 2024. [Online]. Available: https://arxiv.org/abs/2409.08371 

- [2] J.-Y. Kim, I.-W. Park, and J.-H. Oh, “Walking control algorithm of biped humanoid robot on uneven and inclined floor,” _Journal of intelligent and robotic systems_ , vol. 48, no. 4, pp. 457–484, 2007. 

- [3] L. P. Kaelbling, M. L. Littman, and A. W. Moore, “Reinforcement learning: A survey,” _Journal of artificial intelligence research_ , vol. 4, pp. 237–285, 1996. 

- [4] K. Zakka, B. Tabanpour, Q. Liao, M. Haiderbhai, S. Holt, J. Y. Luo, A. Allshire, E. Frey, K. Sreenath, L. A. Kahrs, _et al._ , “Mujoco playground,” _arXiv preprint arXiv:2502.08844_ , 2025. 

- [5] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [6] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [7] L. Engstrom, A. Ilyas, S. Santurkar, D. Tsipras, F. Janoos, L. Rudolph, and A. Madry, “Implementation matters in deep rl: A case study on ppo and trpo,” in _ICLR_ , 2019. 

- [8] X. He, R. Dong, Z. Chen, and S. Gupta, “Learning getting-up policies for real-world humanoid robots,” in _Robotics: Science and Systems_ , 2025. 

- [9] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning humanoid standing-up control across diverse postures,” _arXiv preprint arXiv:2502.08378_ , 2025. 

- [10] X. Gu, Y.-J. Wang, X. Zhu, C. Shi, Y. Guo, Y. Liu, and J. Chen, “Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning,” _arXiv preprint arXiv:2408.14472_ , 2024. 

- [11] W. Cui, S. Li, H. Huang, B. Qin, T. Zhang, L. Zheng, Z. Tang, C. Hu, N. Yan, J. Chen, _et al._ , “Adapting humanoid locomotion over challenging terrain via two-phase training,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [12] Y. Xue, W. Dong, M. Liuˆ, W. Zhang, and J. Pang, “A unified and general humanoid whole-body controller for versatile locomotion,” _arXiv preprint arXiv:2502.03206_ , 2025. 

- [13] D. Wang, X. Wang, X. Liu, J. Shi, Y. Zhao, C. Bai, and X. Li, “More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains,” _arXiv preprint arXiv:2506.08840_ , 2025. 

- [14] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9997–10 003. 

- [15] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv preprint arXiv:2502.10363_ , 2025. 

- [16] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” _arXiv preprint arXiv:2406.10759_ , 2024. 

- [17] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu, _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _arXiv preprint arXiv:2501.02116_ , 2025. 

- [18] K. Van Moffaert and A. Now´e, “Multi-objective reinforcement learning using sets of pareto dominating policies,” _The Journal of Machine Learning Research_ , vol. 15, no. 1, pp. 3483–3512, 2014. 

- [19] C. F. Hayes, R. R˘adulescu, E. Bargiacchi, J. K¨allstr¨om, M. Macfarlane, M. Reymond, T. Verstraeten, L. M. Zintgraf, R. Dazeley, F. Heintz, _et al._ , “A practical guide to multi-objective reinforcement learning and planning,” _arXiv preprint arXiv:2103.09568_ , 2021. 

   - [24] X.-Q. Cai, P. Zhang, L. Zhao, J. Bian, M. Sugiyama, and A. Llorens, “Distributional pareto-optimal multi-objective reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 15 593–15 613, 2023. 

   - [25] M. Terekhov and C. Gulcehre, “In search for architectures and loss functions in multi-objective reinforcement learning,” _arXiv preprint arXiv:2407.16807_ , 2024. 

   - [26] J. Xu, Y. Tian, P. Ma, D. Rus, S. Sueda, and W. Matusik, “Predictionguided multi-objective reinforcement learning for continuous robot control,” in _International conference on machine learning_ . PMLR, 2020, pp. 10 607–10 616. 

   - [27] L. N. Alegre, F. Felten, E.-G. Talbi, G. Danoy, A. Now´e, A. L. Bazzan, and B. C. da Silva, “Mo-gym: A library of multi-objective reinforcement learning environments,” in _Proceedings of the 34th Benelux Conference on Artificial Intelligence BNAIC/Benelearn_ , vol. 2022, 2022, p. 2. 

   - [28] J. Shi, X. Liu, D. Wang, O. Lu, S. Schwertfeger, F. Sun, C. Bai, and X. Li, “Adversarial locomotion and motion imitation for humanoid policy learning,” _arXiv preprint arXiv:2504.14305_ , 2025. 

   - [29] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

   - [30] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit,” _arXiv preprint arXiv:2502.13013_ , 2025. 

   - [31] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbabu, C. Pan, Z. Yi, G. Qu, K. Kitani, J. Hodgins, L. J. Fan, Y. Zhu, C. Liu, and G. Shi, “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

   - [32] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li, “Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills,” _arXiv preprint arXiv:2506.12851_ , 2025. 

   - [33] X. Gu, Y.-J. Wang, and J. Chen, “Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer,” _arXiv preprint arXiv:2404.05695_ , 2024. 

   - [34] S. Mysore, G. Cheng, Y. Zhao, K. Saenko, and M. Wu, “Multi-critic actor learning: Teaching rl policies to act with style,” in _International Conference on Learning Representations_ , 2022. 

   - [35] K. Van Moffaert, M. M. Drugan, and A. Nowe, “Scalarized multiobjective reinforcement learning: Novel design techniques,” in _2013 IEEE Symposium on Adaptive Dynamic Programming and Reinforcement Learning (ADPRL)_ . Singapore, Singapore: IEEE, 2013. 

   - [36] A. Rame, G. Couairon, C. Dancette, J.-B. Gaya, M. Shukor, L. Soulier, and M. Cord, “Rewarded soups: towards pareto-optimal alignment by interpolating weights fine-tuned on diverse rewards,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 71 095–71 134, 2023. 

   - [37] J. Jang, S. Kim, B. Y. Lin, Y. Wang, J. Hessel, L. Zettlemoyer, H. Hajishirzi, Y. Choi, and P. Ammanabrolu, “Personalized soups: Personalized large language model alignment via post-hoc parameter merging,” _arXiv preprint arXiv:2310.11564_ , 2023. 

   - [38] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel, “Highdimensional continuous control using generalized advantage estimation,” _arXiv preprint arXiv:1506.02438_ , 2015. 

   - [39] J. Ren, T. Huang, H. Wang, Z. Wang, Q. Ben, J. Long, Y. Yang, J. Pang, and P. Luo, “Vb-com: Learning vision-blind composite humanoid locomotion against deficient perception,” _arXiv preprint arXiv:2502.14814_ , 2025. 

   - [40] A. Escontrela, X. B. Peng, W. Yu, T. Zhang, A. Iscen, K. Goldberg, and P. Abbeel, “Adversarial motion priors make good substitutes for complex reward functions,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 25–32. 

- [20] A. Navon, A. Shamsian, G. Chechik, and E. Fetaya, “Learning the pareto front with hypernetworks,” _arXiv preprint arXiv:2010.04104_ , 2020. 

- [21] M. Reymond, E. Bargiacchi, and A. Now´e, “Pareto conditioned networks,” _arXiv preprint arXiv:2204.05036_ , 2022. 

- [22] T. Basaklar, S. Gumussoy, and U. Y. Ogras, “Pd-morl: Preferencedriven multi-objective reinforcement learning algorithm,” _arXiv preprint arXiv:2208.07914_ , 2022. 

- [23] R. Yang, X. Sun, and K. Narasimhan, “A generalized algorithm for multi-objective reinforcement learning and policy adaptation,” _Advances in neural information processing systems_ , vol. 32, 2019. 

