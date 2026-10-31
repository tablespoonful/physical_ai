---
title: "Cost-Matching Model Predictive Control for Efficient Reinforcement Learning in Humanoid Locomotion"
date: "2026-03-30"
authors: "Wenqi Cai; Kyriakos G. Vamvoudakis; Sébastien Gros; Anthony Tzes"
url: https://arxiv.org/abs/2603.28243
pdf: https://arxiv.org/pdf/2603.28243
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.28243)** / [論文ページ](https://arxiv.org/abs/2603.28243)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Cost-Matching Model Predictive Control for Efficient Reinforcement Learning in Humanoid Locomotion** 

Wenqi Cai<sup>1</sup> , Kyriakos G. Vamvoudakis<sup>2</sup> , S´ebastien Gros<sup>3</sup> , and Anthony Tzes<sup>1</sup> 

**_Abstract_ — In this paper, we propose a cost-matching approach for optimal humanoid locomotion within a Model Predictive Control (MPC)-based Reinforcement Learning (RL) framework. A parameterized MPC formulation with centroidal dynamics is trained to approximate the action-value function obtained from high-fidelity closed-loop data. Specifically, the MPC cost-to-go is evaluated along recorded state–action trajectories, and the parameters are updated to minimize the discrepancy between MPC-predicted values and measured returns. This formulation enables efficient gradient-based learning while avoiding the computational burden of repeatedly solving the MPC problem during training. The proposed method is validated in simulation using a commercial humanoid platform. Results demonstrate improved locomotion performance and robustness to model mismatch and external disturbances compared with manually tuned baselines.** 

## I. INTRODUCTION 

Humanoid robotics has advanced rapidly in recent years. Humanoid locomotion poses particular challenges due to intermittent contacts, high degrees of freedom, and strict safety constraints, while also requiring robustness to disturbances and modeling errors [1]. 

Model Predictive Control (MPC) has emerged as a dominant paradigm for humanoid locomotion because it provides a systematic mechanism to encode task objectives and enforce constraints through online optimization. To satisfy real-time requirements, many MPC pipelines rely on simplified or reduced-order models that enable lightweight computation and high update rates [2]. However, such simplified models may neglect important effects present during high-fidelity execution (e.g., contact realization, inertial coupling, and actuator or tracking-stack abstractions). Consequently, robust performance often relies heavily on expert tuning of cost weights and terminal penalties [3]. Alternatively, richer formulations that tighten kinematic consistency or incorporate more detailed dynamics [4] can improve fidelity but typically increase computational complexity and complicate real-time deployment [5]. In practice, this trade-off is often addressed using predictive–reactive hierarchies, where an MPC planner 

> 1Wenqi Cai and Anthony Tzes are with the Electrical Engineering Program, New York University Abu Dhabi (NYUAD), 129188, UAE. Email: wenqi.cai@nyu.edu; anthony.tzes@nyu.edu 

> 2Kyriakos G. Vamvoudakis is with the School of Aerospace Engineering, Georgia Institute of Technology, Atlanta, GA 30332, United States. Email: kyriakos@gatech.edu 

> 3Sebastien´ Gros is with the Department of Engineering Cybernetics, Norwegian University of Science and Technology (NTNU), Trondheim, Norway. Email: sebastien.gros@ntnu.no 

This work was supported in part by: a) NSF under grant Nos. SLES2415479, CPS-2227185, b) NASA ULI under grant No. 80NSSC25M7104, and c) the NYUAD Center for AI and Robotics, funded by Tamkeen under the NYUAD Research Institute Award CG010. 

generates reference trajectories that are executed by a higherrate tracking module [6]. While effective for real-time operation, this architectural separation can amplify systematic planning–execution mismatches and make performance sensitive to cost design and tuning, particularly when operating with short horizons [7]. 

Reinforcement Learning (RL) has demonstrated strong capability in learning robust locomotion behaviors directly from data with efficient runtime execution [8]. However, humanoid locomotion represents a challenging learning regime. Training from scratch is often sample-inefficient and sensitive to reward design and curriculum choices, and successful deployments typically rely on large-scale simulation pipelines with additional mechanisms to mitigate sim-to-real discrepancies (e.g., domain randomization [9] and system identification [10]). Furthermore, purely learned policies do not naturally enforce hard safety and contact constraints [11]. These limitations have motivated control– learning formulations that connect RL with adaptive optimal control concepts and provide explicit convergence or stability analyses under disturbances [12], [13]. In this direction, MPC– learning hybrids aim to retain constrained optimization for deployment while leveraging learning to improve performance under model mismatch and uncertainty [14], [15]. 

In this context, this work builds upon our prior MPC-based Reinforcement Learning (MPC-RL) framework—initiated in [16] and further developed in subsequent works (e.g., [17], [18], [19])—which treats a parameterized MPC as a structured value/action-value function approximator or policy approximator. Within this framework, the predictive model, cost function, and constraints of the MPC are parameterized, and closedloop behavior is improved by adjusting these parameters using RL signals. This approach allows learning to operate within the MPC structure, thereby preserving constraint handling and interpretability [20]. However, a key limitation arises in complex, time-critical humanoid locomotion stacks: standard gradient-based MPC-RL methods typically require repeatedly solving the MPC optimization within the learning loop, making training prohibitively expensive when the MPC itself is already operating near real-time computational limits. 

Motivated by this challenge, we propose Cost-Matching MPC (CM-MPC), an efficient learning procedure that preserves the MPC-RL perspective while avoiding solve-inthe-loop training. The central idea is to learn the MPC parameters **_θ_** by minimizing the discrepancy between an MPC surrogate cost-to-go _Q_<sup>MPC</sup> **_θ_** and a measured long-horizon return _Q_<sup>meas</sup> computed from closed-loop trajectories. Rather than differentiating through repeated MPC solves, _Q_<sup>MPC</sup> **_θ_** is 

evaluated by rolling out the parameterized predictive model along recorded action segments and accumulating parameterized stage costs, together with differentiable penalties for state-constraint violations. This formulation enables efficient gradient-based learning while maintaining deployment as a standard constrained receding-horizon MPC controller. 

**Contributions.** The contributions of this work are twofold. First, we introduce a cost-matching learning framework that extends our prior MPC-RL formulation while substantially reducing the computational burden during training by eliminating the need for repeated MPC solves in the learning loop. The proposed framework is generic and can be applied to systems formulated as Optimal Control Problems (OCPs). Second, we demonstrate the approach on humanoid locomotion by developing a constrained OCP formulation based on centroidal dynamics and validating the learning procedure in highfidelity simulation. An open-source implementation of the framework is also provided at https://github.com/R ISC-NYUAD/humanoid_mpc_cost_matching. 

## II. PROBLEM FORMULATION 

Consider humanoid locomotion control within a hierarchical control architecture [21]. In this architecture, an upperlevel nonlinear MPC planner operates at a lower frequency and generates reference commands, while a high-frequency Proportional Derivative (PD)-type tracking controller maps the MPC commands to joint torques (from **_u_** to **_u_** ˜), as shown in Fig. 1. 


Fig. 1: Cost-Matching MPC-RL framework for humanoids. 

In this work, we shall focus on the learning-based parame- 

terization of the MPC layer, while the low-level tracking controller is treated as a fixed module. Fig. 1 provides an overview of the proposed CM-MPC framework for humanoids, and the remaining components are introduced in the subsequent sections. 

## _A. Centroidal Dynamics_ 

A complete _centroidal dynamics_ model is adopted in this work, building on the OCS2 centroidal formulation [22], [21]. Let _I_ denote the inertial (world) frame and _B_ the base frame attached to the robot trunk. The generalized coordinates of the robot are defined as **_q_** = [ **_p_**<sup>_⊤_</sup> _b_<sup>_,_</sup><sup>**_θ_**</sup> _b_<sup>_⊤,_</sup><sup>**_q_**</sup><sup>_⊤_</sup> _j_<sup>]</sup><sup>_⊤∈_R6+</sup><sup>_nj_,where</sup> **_p_** _b ∈_ R<sup>3</sup> denotes the base position in _I_ , **_θ_** _b ∈_ R<sup>3</sup> represents the base orientation (ZYX Euler angles), and **_q_** _j ∈_ R<sup>_nj_</sup> denotes the joint angles. 

The state **_x_** _∈_ R<sup>12+</sup><sup>_nj_</sup> := � **_h_**<sup>_⊤_</sup> lin **_h_**<sup>_⊤_</sup> ang **_q_**<sup>_⊤_�</sup><sup>_⊤_</sup> concatenates the centroidal momentum **_h_** and the configuration **_q_** , where **_h_** lin _,_ **_h_** ang _∈_ R<sup>3</sup> denote the linear and angular momenta expressed in _I_ . The control input **_u_** _∈_ R<sup>12+</sup><sup>_nj_</sup> consists of the contact wrenches for the left ( _L_ ) and right ( _R_ ) feet together with the joint velocities **_u_** := � **_w_** _⊤c,L_ **_w_**<sup>_⊤_</sup> _c,R_ **_v_**<sup>_⊤_</sup> _j_ � _⊤ ,_ where **_w_** _c,i_ = [ **_f_**<sup>_⊤_</sup> _c,i_<sup>_,_</sup><sup>**_m_**</sup><sup>_⊤_</sup> _c,i_<sup>]</sup><sup>_⊤∈_R6representsthecontactforceand</sup> moment exerted at the _i_ -th foot ( _i ∈{L, R}_ ), and **_v_** _j ∈_ R<sup>_nj_</sup> denotes the commanded joint velocity. 

The system dynamics **_x_** ˙ = **_f_** dyn( **_x_** _,_ **_u_** ) is 


where _M_ denotes the total mass and **_g_** is the gravitational acceleration. The vector **_r_** _c,i_ denotes the moment arm from the Center of Mass (CoM) to the contact point of foot _i_ , expressed in the inertial frame _I_ . The matrix **Ξ** ( **_q_** ) maps generalized velocities to the configuration derivative **_q_** ˙ . These transformationrelated quantities can be efficiently computed using rigidbody algorithms provided by the Pinocchio library [23]. The base velocity variables ( **_v_** _b,_ **_ω_** _b_ ) are determined by the centroidal momentum **_h_** and the joint velocities **_v_** _j_ through 


is the Centroidal Momentum Matrix (CMM) [24], which captures the inertial coupling between base and limb motions. The matrices **_A_** _b_ and **_A_** _j_ denote the corresponding block partitions of the CMM. The base velocity can therefore be obtained as = **_A_** _b_ ( **_q_** )<sup>_−_1</sup> ( **_h_** _−_ **_A_** _j_ ( **_q_** ) **_v_** _j_ ), ensuring that � **_ωv_** _bb_ � the kinematic evolution remains consistent with the centroidal momentum dynamics. 

## _B. Constraints_ 

The feasible state–input set is defined through equality and inequality constraints. To distinguish phase-dependent constraints, let _P_ st and _P_ sw denote the sets of stance and swing phases, respectively. 

_1) Inequality Constraints:_ 

- Joint Limits. The joint configurations are restricted by mechanical limits: **_q_**<sup>min</sup> _j ≤_ **_q_** _j ≤_ **_q_**<sup>max</sup> _j ._ 

- Foot Collision. To prevent self-collision, the minimum distance between the left and right feet, computed using Signed Distance Fields (SDF) Φsdf, must maintain a safety margin _d_ safe: Φsdf( **_q_** ) _≥ d_ safe _._ 

- Friction Cone. To avoid foot slippage, the contact force for any active foot must lie within the friction cone: ~~�~~ <u>�</u> _fc,i_<sup>_x_</sup> <u>�2 + �</u> _fc,i_<sup>_y_</sup> <u>�2</u> _≤ µfc,i z_<sup>_,∀i ∈Pst._</sup> 

- _•_ Center of Pressure (CoP). To maintain contact stability with foot dimensions ( _dx, dy_ ), the CoP must remain within the support region: _|m_<sup>_x_</sup> _c,i_<sup>_|≤dyf_</sup> _c,i_<sup>_z,|my_</sup> _c,i_<sup>_|≤dxf_</sup> _c,i_<sup>_z,∀i ∈Pst._</sup> _2) Equality Constraints:_ 

- Zero Velocity. During stance, the foot maintains rigid ground contact and the linear velocity of the foot contact frame is constrained to zero: **_v_** _c,i_ = **_J_** _c,i_ ( **_q_** ) ˙ **_q_** = **0** _, ∀i ∈ P_ st _,_ where **_J_** _c,i_ ( **_q_** ) denotes the contact Jacobian. 

- Zero Wrench. Feet in the swing phase are contact-free, and their contact wrench must vanish: **_w_** _c,i_ = **0** _, ∀i ∈P_ sw _._ 

- Normal Velocity Tracking. The normal ( _z_ -axis) velocity of the swing foot is constrained to follow a reference profile _v_ ref<sup>_z_toensureaccuratelanding:</sup><sup>_v_</sup> _c,i_<sup>_z_=</sup><sup>_v_</sup> ref<sup>_z_(</sup><sup>_t_)</sup><sup>_,∀i ∈P_sw</sup><sup>_._</sup> 

## _C. Optimal Control Objective_ 

Humanoid locomotion is formulated as a constrained OCP over a finite prediction horizon _N_ . Given the centroidal dynamics and feasibility constraints, the planner seeks an optimal control sequence that minimizes 


where _L_ ( _·_ ) and _T_ ( _·_ ) denote the stage and terminal costs, respectively. The stage cost is composed of 

_L_ = _L_ trac + _L_ base + _L_ com + _L_ swin + _L_ torq _,_ (3) capturing reference tracking, dynamic stability, and physical plausibility. Specifically: 

- We enforce tracking of the reference state trajectory **x** ref while regularizing the control effort: _L_ trac = _∥_ **_x_** _−_ **_x_** ref _∥_<sup>2</sup> **_Q_**<sup>+</sup><sup>_∥_</sup><sup>**_u_**</sup><sup>_−_</sup><sup>**_u_**ref</sup><sup>_∥_</sup> **_R_**<sup>2</sup><sup>_._</sup> 

- A task-space kinematic penalty is imposed on a baseattached frame to regularize upper-body motion: _L_ base = _∥_ **_e_** base( **_x_** _,_ **_u_** ) _∥_<sup>2</sup> **_Q_** base<sup>,where</sup><sup>**_e_**base</sup><sup>_∈_R18collectsthetask-</sup> space tracking errors. This term mitigates upper-body oscillations and promotes an upright posture during locomotion. 

- To improve balance robustness, the horizontal CoM position is regularized toward the midpoint of the active foot contacts: _L_ com = _∥_ **_p_**<sup>_xy_</sup> com<sup>(</sup><sup>**_q_**)</sup><sup>_−_</sup><sup>**_p_**</sup><sup>_xy_</sup> mid<sup>(</sup><sup>**_q_**)</sup><sup>_∥_2</sup> **_Q_** com<sup>,where</sup><sup>**_p_**</sup> com<sup>_xy_</sup> denotes the CoM position projected onto the horizontal plane, and **_p_**<sup>_xy_</sup> mid<sup>:=1</sup> 2<sup>(</sup><sup>**_p_**</sup> _c,L_<sup>_xy_(</sup><sup>**_q_**)+</sup><sup>**_p_**</sup><sup>_xy_</sup> _c,R_<sup>(</sup><sup>**_q_**))denotesthe</sup> midpoint between the left and right foot contacts. 

- To regulate foot clearance and landing orientation, deviations of the swing-foot pose and twist from their references are penalized: _L_ swin =<sup>�</sup> _i∈P_ sw<sup>_∥_</sup><sup>**_e_**sw</sup><sup>_,i_(</sup><sup>**_x_**</sup><sup>_,_</sup><sup>**_u_**)</sup><sup>_∥_2</sup> **_Q_** sw<sup>,where</sup> **_e_** sw _,i ∈_ R<sup>18</sup> denotes the task-space tracking error of the swing-foot frame relative to its reference trajectory. 

- To discourage contact force distributions that generate large joint torques, the contact wrench is regularized through the induced generalized torques: _L_ torq = � _i∈P_ st �� **_J_** _c,i_ ( **_q_** ) _⊤_ **_w_** _c,i_ ��2 **_Q_** torq<sup>,where</sup><sup>**_J_**</sup><sup>_c,i_(</sup><sup>**_q_**)denotesthe</sup> contact Jacobian. 

The terminal cost is defined as a quadratic penalty on the terminal state, 


The above OCP provides a structured mechanism for generating feasible locomotion behaviors. Nevertheless, model mismatch and unmodeled effects can lead to suboptimal MPC policies and degraded closed-loop performance. To address this issue, the next section introduces a data-driven adaptation of the MPC parameterization using rollout data collected during execution. 

## III. COST-MATCHING MPC-BASED REINFORCEMENT LEARNING 

We present the cost-matching method using the general Markov decision process (MDP) notation in order to emphasize that the proposed approach applies to any problem that can be formulated as a constrained OCP and for which real-world data is available. 

## _A. Parameterized MPC as a Q Function_ 

Consider a discounted infinite-horizon MDP with state **_s_** _∈S_ , action **_a_** _∈A_ , stage cost _L_ ( **_s_** _,_ **_a_** ), and discount factor _γ ∈_ (0 _,_ 1]. The objective is to minimize the expected discounted cumulative cost. To obtain a structured and differentiable approximation of the optimal policy and its associated action-value function, we employ a finite-horizon parameterized model predictive control (MPC) scheme as a function approximator. The parameter vector **_θ_** _∈_ R<sup>_p_</sup> jointly parameterizes the predictive model and cost functions of the MPC, enabling data-driven adaptation in the presence of model mismatch and uncertainties. 

_a) Parameterized MPC scheme:_ Given a measured state **_s_** , the horizon- _N_ parameterized MPC problem is 


The predictive model **_f θ_** , stage cost _L_ **_θ_** , and terminal cost _T_ **_θ_** are parameterized and adapted through learning. 

_b) MPC-induced action-value function:_ To enable learning without repeatedly solving the optimization problem, we define the MPC-induced action-value along given actions recorded from the real system. For a length- _N_ action segment **_a_** 0: _N −_ 1 := _{_ **_a_** 0 _, . . . ,_ **_a_** _N −_ 1 _}_ , the predicted rollout is 

- **_x_** 0 = **_s_** _,_ **_x_** _i_ +1 = **_f θ_** ( **_x_** _i,_ **_a_** _i_ ) _, i_ = 0 _, . . . , N −_ 1 _._ (6) 

Note that even when the recorded actions are feasible on the real system, the predicted trajectory generated by (6) may violate state-related constraints due to model mismatch. Consequently, constraint-violation penalties are incorporated directly into the rollout-based value evaluation. Define the per-stage and terminal violation residuals 


= where [ _·_ ]+ denotes the element-wise operator [ _y_ ]+ max( _y,_ 0). Let the weights **_W_** _,_ **_W_** _f ≻_ **0** , and define _ϕ_ ( **_r_** _i_ ) := _∥_ **_r_** _i∥_<sup>2</sup> **_W_**<sup>_,_</sup> _ϕf_ ( **_r_** _N_ ) := _∥_ **_r_** _N ∥_<sup>2</sup> **_W_** _f_<sup>_._</sup> (8) The MPC-induced action-value function is then defined as 


where _{_ **_x_** _i}_ and _{_ **_r_** _i}_ are generated by (6) and (7). Importantly, (9) can be evaluated through forward rollout and cost accumulation, and is differentiable with respect to **_θ_** , without requiring the solution of (5) during training. 

## _B. Action-Value Evaluation via Data Rollouts_ 

Consider a dataset of trajectories collected from the real environment _D_ = _{_ ( **_s_** _k,_ **_a_** _k, ℓk_ ) _}_<sup>_M_</sup> _k_ =0<sup>_−_1,where(</sup><sup>_M≫N_)</sup> denotes the trajectory length and _ℓk_ = _L_ ( **_s_** _k,_ **_a_** _k_ ) is the observed stage cost. The trajectories need not be optimal. For each time index _k_ , we define the measured discounted return-to-go along the recorded trajectory as 


This quantity represents the long-term cost accumulated by the system under the executed actions. In the proposed framework, _Q_<sup>meas</sup> serves as the learning target, while _Q_<sup>MPC</sup> **_θ_** provides a finite-horizon, model-based approximation evaluated along the same recorded action segment. The discrepancy between these quantities primarily reflects a systematic mismatch between the real system and the parameterized predictive model. 

Given an index _k_ , we compute _Q_<sup>MPC</sup> **_θ_** by initializing (6) at **_x_** 0 = **_s_** _k_ and rolling out the parameterized model over the recorded action segment ( **_a_** _k, . . . ,_ **_a_** _k_ + _N −_ 1). This estimate is compared with _Q_<sup>meas</sup> , which accumulates the discounted costs along the measured trajectory from _k_ to _M −_ 1. 

From an RL perspective, _Q_<sup>MPC</sup> **_θ_** and _Q_<sup>meas</sup> represent two evaluations of the action-value at the same anchor state **_s_** _k_ for the executed action segment: a finite-horizon modelbased surrogate and the measured rollout return. While typically _M ≫ N_ , the discount factor _γ_ in _Q_<sup>meas</sup> and the terminal shaping _T_ **_θ_** ( **_x_** _N_ ) in _Q_<sup>MPC</sup> compensate for the horizon mismatch. Discounting attenuates far-future costs, while the terminal term summarizes the residual cost-to-go beyond the prediction horizon. This observation highlights the importance of terminal cost design in short-horizon MPC and motivates learning its relative weight to align the surrogate with long-term performance. 

## _C. Cost-Matching Objective and Gradient_ 

The key idea behind the learning objective is to adjust **_θ_** such that the MPC-induced value _Q_<sup>MPC</sup> **_θ_** evaluated along recorded action segments matches the long-term return _Q_<sup>meas</sup> observed on the real system. 

Given the dataset _D_ and the measured returns (10), the cost-matching objective is 


The expectation in (11) is approximated using empirical averages over mini-batches. For a fixed recorded action segment, _Q_<sup>MPC</sup> **_θ_** is obtained via the forward rollout (6) and accumulation of the cost and penalty terms in (9). Therefore, _∇_ **_θ_** _Q_<sup>MPC</sup> **_θ_** can be computed by differentiating through the rollout recursion and the corresponding cost and penalty evaluations. The loss gradient is 


Since training does not require solving (5), gradient evaluation reduces to differentiating a length- _N_ rollout and scales linearly with the horizon length _N_ . The parameters are updated using a first-order optimization method, 


with step size _α >_ 0. After convergence, the learned parameters **_θ_**<sup>_⋆_</sup> define a structured MPC controller deployed online by solving (5) in a receding-horizon fashion. 

## _D. Convergence of Cost Matching_ 

The cost-matching update (13) is a stochastic optimization of (11). The following theorem establishes convergence to a first-order stationary point under standard smoothness and bounded-variance assumptions. 

**Assumption 1.** _For each sample ξ_ = ( **_s_** _,_ **_a_** 0: _N −_ 1 _, Q_<sup>meas</sup> ) _, define qξ_ ( **_θ_** ) := _Q_ **_θ_**<sup>MPC</sup> ( **_s_** _,_ **_a_** 0: _N −_ 1) _. Assume that qξ_ ( **_θ_** ) _is continuously differentiable in_ **_θ_** _, and that there exist constants BQ, GQ, LQ >_ 0 _such that, for all samples ξ and all_ **_θ_** _,_ **_θ_**<sup>_′_</sup> _,_ 


_Moreover, the mini-batch gradient estimator ∇L_<sup>�</sup> ( **_θ_** ) _used in_ (13) _is unbiased and has bounded variance, i.e.,_ 


**Theorem 1** (Convergence of cost matching) **.** _Suppose that Assumption 1 holds and the loss L in_ (11) _has Lipschitzcontinuous gradient with constant LL_ = 2( _G_<sup>2</sup> _Q_<sup>+</sup><sup>_BQLQ_)</sup><sup>_._</sup> _Let the parameter sequence {_ **_θ_** _j} be generated by_ **_θ_** _j_ +1 = **_θ_** _j − α∇L_<sup>�</sup> ( **_θ_** _j_ ) _, with a constant step size_ 0 _< α ≤_ 1 _/LL. Then, for any K ≥_ 1 _,_ 


_where L_ inf := inf **_θ_** _L_ ( **_θ_** ) _. In the full-batch case (σ_ = 0 _), L_ ( **_θ_** _j_ ) _is monotonically nonincreasing and ∇L_ ( **_θ_** _j_ ) _→_ **0** _as j →∞._ 

_Proof._ For a single sample _ξ_ , the gradient of the squared matching error is 


By Assumption 1, this gradient is Lipschitz with constant 2( _G_<sup>2</sup> _Q_<sup>+</sup><sup>_BQLQ_),hence</sup><sup>_∇L_isalsoLipschitzwiththesame</sup> constant. Using the standard descent lemma [25] for smooth objectives, we have 


Taking the conditional expectation and using the unbiased and bounded-variance assumptions yields 

E[ _L_ ( **_θ_** _j_ +1)] _≤_ E[ _L_ ( **_θ_** _j_ )] _−_<sup>_α_</sup> _σ_<sup>2</sup> _,_ 2<sup>E[</sup><sup>_∥∇L_(</sup><sup>**_θ_**</sup><sup>_j_)</sup><sup>_∥_2] +</sup><sup>_LL_</sup> 2<sup>_α_2</sup> where the factor 1 _/_ 2 follows from _α ≤_ 1 _/LL_ . Summing this inequality from _j_ = 0 to _K −_ 1 gives the stated bound. The full-batch case follows by setting _σ_ = 0. ■ 

Theorem 1 shows that the proposed cost-matching update converges to a first-order stationary set of (11) under Assumption 1, which is compatible with our setting since training is performed over a bounded rollout buffer. 

## _E. Constraints and Feasibility_ 

The treatment of constraints differs between the learning and deployment phases. During training, the MPC-induced action-value function (9) incorporates state-related constraints through differentiable penalty terms based on the violation measures defined in (8). This soft-penalty formulation allows constraint violations to be evaluated along data-driven rollouts without requiring the predicted trajectory to remain feasible, which is essential when the parameterized model does not perfectly capture the true system dynamics. 

After training, the learned parameters **_θ_**<sup>_⋆_</sup> define a structured MPC controller that is deployed by solving the constrained optimization problem (5) in a receding-horizon manner. In this phase, input and state constraints are enforced as hard constraints, thereby ensuring feasibility and safety in closedloop operation. Because the learning process shapes the MPC model and cost to match the long-term performance of the real system, the resulting controller benefits from both data-driven adaptation and the constraint-handling guarantees inherent to MPC. This separation—soft constraint handling during learning and hard constraint enforcement during online MPC execution—enables efficient gradient-based training while preserving the safety and feasibility guarantees of MPC at runtime. 

## IV. INSTANTIATION ON HUMANOID LOCOMOTION 

This section instantiates the general cost-matching framework introduced in Section III for the humanoid locomotion OCP described in Section II. Rollouts are collected from realworld execution, and the MPC-induced value is evaluated by replaying the logged MPC commands in the parameterized 

predictive model initialized at the measured state. We next describe the model and cost parameterizations adopted in this locomotion setting. 

## _A. Parameterized Model and Objective_ 

The predictive model **_f θ_** used in (6) is obtained by discretizing the centroidal dynamics (1). To account for systematic mismatch between the predictive model and the real system, we parameterize the centroidal momentum propagation using learnable gains: 


where **_θ_** _hl ∈_ R<sup>3</sup> _>_ 0<sup>and</sup><sup>**_θ_**</sup><sup>_ha∈_R3</sup> _>_ 0<sup>areincludedin</sup><sup>**_θ_**.</sup> This parameterization preserves the centroidal dynamics structure while absorbing systematic discrepancies caused by imperfect contact wrench realization, unmodeled compliance, and abstraction effects introduced by the low-level tracking controller. The parameterized stage cost retains the decomposition in (3) as _L_ **_θ_** = _L_ trac( **_θ_** ) + _L_ base( **_θ_** ) + _L_ com( **_θ_** ) + _L_ swin( **_θ_** ) + _L_ torq( **_θ_** ) _,_ and the terminal cost is defined = as _T_ **_θ_** ( **_x_** _N_ ) _∥_ **_x_** _N −_ **_x_**<sup>ref</sup> _N_<sup>_∥_2</sup> **_Q_** _f_ ( **_θ_** )<sup>.Quadraticweights</sup> = are parameterized through diagonal scalings as **_Qθ_** = = diag( **_θ_** _q_ ) _,_ **_Rθ_** diag( **_θ_** _r_ ) _,_ **_Qf θ_** diag( **_θ_** _qf_ ) _,_ where **_θ_** _q,_ **_θ_** _r,_ **_θ_** _qf ∈_ R _≥_<sup>12+</sup> 0<sup>_nj_</sup> are learnable vectors. The weight matrices **_Q_** base( **_θ_** ), **_Q_** com( **_θ_** ), **_Q_** sw( **_θ_** ), and **_Q_** torq( **_θ_** ) are parameterized analogously. 

## _B. Cost-Matching Training Loop_ 

Training is performed _on-policy_ using the parameterized MPC controller. At iteration _j_ , the parameter vector **_θ_** _j_ defines a closed-loop locomotion policy obtained by solving (5) in a receding-horizon manner. Trajectories are collected by executing the resulting commands through the fixed lowlevel tracking module within a high-fidelity simulator. From the recorded trajectories, and for each sampled index _k_ , we compute the measured return _Q_<sup>meas</sup> _k_ (data length _M_ ) and the rollout-based surrogate _Q_<sup>MPC</sup> **_θ_** _j ,k_<sup>(datalength</sup><sup>_N_).The</sup> parameters are then updated by minimizing the squared discrepancy between these quantities, as summarized in Algorithm 1. 

## _C. Implications for Locomotion Control_ 

For bipedal locomotion, this instantiation yields several practical benefits. 

**(i) Mitigating short-horizon bias.** By matching _Q_<sup>MPC</sup> **_θ_** to long-horizon returns, the learned stage and terminal shaping terms effectively act as a tail-cost approximation, mitigating the short-horizon bias inherent in real-time humanoid MPC. **(ii) Compensating model mismatch.** The learned parameters adapt both the prediction model and the objective to systematic discrepancies between the planning model and high-fidelity execution, including modeling inaccuracies and abstraction effects introduced by the tracking controller. 

**Algorithm 1** On-policy Cost-Matching Training for Hu- <u>manoid Locomotion.</u> 

|1:|**Input:** initial parameters **_θ_**0, discount _γ_, stepsize _α_|
|---|---|
|2:|**for** _j_ = 0_,_1_,_2_, . . ._ **do**|
|3:|**Data collection.** Run the closed-loop controller induced by<br>(5) with **_θ_**_j_ for _M_ steps through the full execution stack,<br>|
||and log_Dj_ =_{_(**_s_**_k,_**_a_**_k, ℓk_)_}_<sup>_M−_1</sup><br>_k_=0 <sup>with</sup><sup>**_a_**</sup><sup>_k_ :=</sup><sup>**_u_**</sup><sup>_k_ and</sup><sup>_ℓk_ :=</sup><br>_L_(**_s_**_k,_**_a_**_k_).|
|4:|Sample a mini-batch of indices _B ⊂{_0_, . . . , M −_1_}_.|
|5:|**for** each _k ∈B_ **do**|
|6:|**Measured return.** Compute _Q_<sup>meas</sup><br>_k_<br>=<br>�_M−k−_1<br>_i_=0<br>_γ_<sup>_i _</sup>_L_(**_s_**_k_+_i,_**_a_**_k_+_i_) via (10).|
|7:|**MPC-side rollout.** Set **_x_**0 :=**_s_**_k_ and propagate for _i_=<br>|
||0_, . . . , N −_1: **_x_**_i_+1 =**_f θ_**_j_(**_x_**_i,_**_a_**_k_+_i_).<br>|
|8:|**Surrogate value.** Evaluate _Q_<sup>MPC</sup><br>**_θ_**_j,k_ <sup>:=</sup><br>_Q_<sup>MPC</sup><br>**_θ_**_j_<br>(**_s_**_k,_**_a_**_k_:_k_+_N−_1) via (9).<br>|
|9:|**end for**|
|10:|Form _L_(**_θ_**_j_) =<br>1<br>_|B|_<br>�<br>_k∈B_ <sup>(</sup><sup>_Q_MPC</sup><br>**_θ_**_j,k _<sup>_−Q_meas</sup><br>_k_<br>)<sup>2</sup>.|
|11:<br>12:|Update **_θ_**_j_+1 _←_**_θ_**_j −α∇_**_θ_**_L_(**_θ_**_j_).<br> **end for**|


**(iii) Robustness to disturbances.** When trajectories are collected under external disturbances, the measured returns reflect the recovery behaviors of the system. Consequently, the learned MPC objective is implicitly tuned toward policies that improve disturbance rejection under the same constrained MPC structure. 

**(iv) Policy improvement.** Although the update minimizes a value discrepancy rather than directly maximizing return, improving the fidelity of the MPC internal cost-to-go makes the receding-horizon minimizer of the surrogate objective more consistent with the true long-term performance, thereby yielding improved closed-loop policies. 

**(v) Training efficiency.** Each update differentiates through a length- _N_ rollout without repeatedly solving the MPC optimization problem within the learning loop, resulting in a computational cost that scales linearly with _N_ . 

## V. SIMULATION STUDIES AND ANALYSIS 

This section evaluates the proposed cost-matching MPC (CM-MPC) on a commercial humanoid platform (Unitree G1) using the locomotion stack described in Section II. In the following experiments, we compare two controllers operating under identical MPC horizon length, constraints, and tracking stack: (i) a manually tuned baseline using the initial parameters **_θ_** 0, and (ii) the learned CM-MPC controller using the converged parameters **_θ_**<sup>_⋆_</sup> . 

## _A. Cost-Matching Diagnostics_ 

The learning objective is to reduce the discrepancy between the MPC-induced surrogate cost-to-go _Q_<sup>MPC</sup> **_θ_** and the measured long-horizon return _Q_<sup>meas</sup> collected from closedloop executions. Figure 2 reports the validation mean squared error (MSE) of this value mismatch across training rounds. The mismatch decreases rapidly during the early training iterations and gradually converges as learning progresses. 

The block-wise evolution of **_θ_** provides insights into the mechanisms underlying this improvement. In particular, the terminal cost weights ( **_Q_** _f_ ) increase significantly throughout 

training, effectively acting as an implicit tail-cost approximation that compensates for the inherent myopia of the finitehorizon MPC formulation. Concurrently, torque-regularization parameters increase, which suppresses impulsive control actions, while swing-foot tracking weights decrease slightly. This reshaping of the cost landscape prevents overly strict kinematic tracking and instead allows the solver greater flexibility to prioritize whole-body balance and compliant behavior under uncertainties. 


Fig. 2: Closed-loop validation of the value mismatch MSE� _Q_<sup>MPC</sup> **_θ_** _− Q_<sup>meas�</sup> across training rounds (shaded region: 10 _−_ 90% across seeds). At each training round, 50 trajectories are collected (600 steps per trajectory), and the cost-matching objective is optimized using 2000 gradient updates with discount factor _γ_ = 0 _._ 985. The inset summarizes the normalized block-wise evolution of **_θ_** , illustrating how learning reshapes the MPC objective. 

Figure 3 provides complementary diagnostics at the sample level. The figure shows the density of _Q_<sup>MPC</sup> **_θ_** versus _Q_<sup>meas</sup> before training and after convergence. After learning, the root-mean-square error (RMSE) between the two values decreases and the residual distribution tightens, indicating improved consistency between the MPC surrogate value and the measured return. Together, these diagnostics confirm that the learned parameters significantly improve the fidelity of the MPC internal cost-to-go approximation. 


Fig. 3: Value-matching diagnostics on a fixed evaluation set: density plot of _Q_<sup>MPC</sup> **_θ_** versus _Q_<sup>meas</sup> . 

## _B. Robustness Evaluation under Disturbances_ 

To assess whether the improved surrogate value representation translates into better closed-loop behavior, we evaluate 

both the baseline MPC and the learned CM-MPC under a scripted disturbance benchmark applied to the Unitree G1 humanoid. 

As illustrated in Figure 4, the disturbance profile consists of three lateral force pulses _f_ ext _,y_ = 18 N with duration 0 _._ 10 s applied at _t_ = _{_ 12 _._ 00 _,_ 12 _._ 75 _,_ 13 _._ 55 _}_ s (P1/2/4), and one yaw torque pulse _m_ ext _,z_ = 8 N m with duration 0 _._ 06 s at _t_ = 13 _._ 05 s (P3). This mixed force–torque sequence excites both linear and angular momentum channels without modifying the nominal reference trajectories. Consequently, differences in post-disturbance recovery can be attributed to the objective and model reshaping induced by the learned parameters **_θ_** . 


Fig. 4: Simulation snapshots of the humanoid during locomotion under a time-scheduled disturbance benchmark consisting of lateral force pulses _f_ ext _,y_ and a yaw-torque pulse _m_ ext _,z_ . 

Figure 5 shows a representative rollout comparing the baseline controller and CM-MPC. From top to bottom, the plots report the tracking error _∥x − x_ ref _∥_ , control effort _∥u∥_ , control jitter _∥u_ ˙ _∥_ (discrete-time input difference), linear momentum error _∥h_ lin _− h_ lin _,_ ref _∥_ , and angular momentum error _∥h_ ang _− h_ ang _,_ ref _∥_ . 

Compared with the baseline controller, CM-MPC settles earlier to the pre-disturbance error band and produces smoother corrective actions, as evidenced by reduced control effort _∥u∥_ and lower control jitter _∥u_ ˙ _∥_ during the recovery phase. At the same time, the momentum tracking errors do not consistently decrease: _∥h_ lin _− h_ lin _,_ ref _∥_ remains broadly comparable, and _∥h_ ang _− h_ ang _,_ ref _∥_ may increase during parts of the transient. This behavior reflects a deliberate trade-off induced by the learned parameters **_θ_**<sup>_⋆_</sup> . By relaxing strict tracking penalties (e.g., reduced swing-foot tracking weights) while increasing actuation regularization (larger _R_ / torque-related weights), CM-MPC allocates its limited control authority under constraints toward stabilizing whole-body motion and rejecting disturbances, rather than enforcing exact momentum reference tracking at every instant. 

## _C. Comprehensive Statistical Analysis_ 

To validate the observed improvements statistically, Table I summarizes results over six disturbance trials (mean _±_ std). The learned CM-MPC improves nominal tracking while 

reducing high-percentile control effort, indicating that the learned parameters **_θ_** produce a better trade-off between tracking accuracy and control smoothness under the same constrained MPC structure. More importantly, the postpush recovery metrics show consistent improvements. The Post-Push RMS decreases, while the Post-Push Peak and IAE (Integral Absolute Error) are reduced by 4 _._ 80% and 6 _._ 82%, respectively, indicating smaller overshoot and less accumulated deviation following the disturbance. The Settling Time improves by 31 _._ 25% under the same threshold-and-hold criterion, reflecting faster return to the predisturbance performance band. Momentum metrics remain largely comparable, with a minor trade-off in linear momentum error ( _−_ 0 _._ 99%). This observation is consistent with the qualitative analysis in Figure 5, where the learned controller prioritizes faster stabilization and smoother actuation during transient recovery rather than enforcing strict reference momentum tracking. 

TABLE I: Comprehensive Evaluation of Metrics (Mean _±_ Std) over Six Trials. 

|**Metric**|**Baseline**|**CM-MPC**|**Impr. (%)**|
|---|---|---|---|
|**_Overall Tracking_**||||
|RMS Error (_∥_**_e_**_∥_2)|1.022 _±_ 0.012|1.009 _±_ 0.016|+1.29|
|Peak Error (_∥_**_e_**_∥∞_)|1.620 _±_ 0.021|1.597 _±_ 0.045|+1.41|
|**_Control Effort & Smoothness_**||||
|Max Effort (_∥_**_u_**_∥_99%)<br>|472.7 _±_ 4.3|447.8 _±_ 7.1|+**5.26**|
|Max Jitter (_∥_˙**_u_**_∥_99%) [10<sup>4</sup>]|5.66 _±_ 0.00|5.60 _±_ 0.03|+1.10|
|**_Momentum Analysis_**||||
|Lin. Mom. (_∥_**_h_**lin_∥_2)|0.468 _±_ 0.011|0.467 _±_ 0.011|+0.35|
|Ang. Mom. (_∥_**_h_**ang_∥_2)<br>|0.048 _±_ 0.001|0.048 _±_ 0.001|+1.18|
|Lin. Mom. Err. (_∥_**_h_**lin_−_**_h_**<sup>ref</sup><br>lin<sup>_∥_2)</sup><br>|0.372 _±_ 0.010|0.376 _±_ 0.010|-0.99|
|Ang. Mom. Err. (_∥_**_h_**ang _−_**_h_**<sup>ref</sup><br>ang<sup>_∥_2) </sup>|<sup>0.048</sup> <sup>_±_ 0.001 </sup>|<sup>0.048</sup> <sup>_±_ 0.001</sup>|+1.18|
|**_Post-Push Recovery_**||||
|Post-Push RMS (_∥_**_e_**<sup>post</sup>_∥_2)<br>|1.026 _±_ 0.010|1.014 _±_ 0.015|+1.17|
|Post-Push Peak (_∥_**_e_**<sup>post</sup>_∥∞_)|1.539 _±_ 0.030|1.465 _±_ 0.020|+**4.80**|
|Integral Abs. Err. (IAE)|0.547 _±_ 0.033|0.510 _±_ 0.030|+**6.82**|
|Settling Time (_ts_)|0.053 _±_ 0.010|0.037 _±_ 0.010|+**31.25**|
|⋇_Post-push recovery metrics._ Let <br>over the post-push window _t ∈_<br>|**_e_**<sup>post</sup>(_t_)≜_∥_**_x_**<br>[_t_push<br>~~e~~nd<sup>_, t_</sup>p<br>|(_t_)_−_**_x_**ref(_t_)_∥_<br>ush<br>~~e~~nd <sup>+</sup> <sup>_T_</sup>pos<br>|evaluated<br>t<sup>]. Define</sup><br>|
|Post-Push RMS = _∥_**_e_**<sup>post</sup>_∥_2, <br>IAE=<br>�<br>max(**_e_**<sup>post</sup> _−_¯**_e_**pre_,_0)_d_|Post-Push <br>_t_ (where ¯**_e_**pre <br>|Peak = _∥_**_e_**<sup>pos</sup><br> is the pre-push <br>|<sup>t</sup>_∥∞_, and<br> baseline).<br>|
|Settling Time_ts_ is the first ti<br>within a pre-push threshold for a i|i me after_t_push<br><br>fixed hold dura|~~e~~nd <sup>that</sup><sup>**_e_**post(</sup><br>tion.|<sup>_t_) remains</sup>|


Overall, the simulation results demonstrate that the costmatching procedure effectively minimizes the discrepancy between _Q_<sup>MPC</sup> **_θ_** and _Q_<sup>meas</sup> throughout training. The optimized parameters **_θ_**<sup>_⋆_</sup> lead to improved disturbance rejection characterized by faster recovery, reduced control effort, and smoother actuation, while simultaneously compensating for modeling discrepancies in the simplified centroidal dynamics through data-driven adaptation. 

## VI. CONCLUSION 

This paper presents a cost-matching framework for learning the parameters of a constrained centroidal MPC controller for humanoid locomotion. By matching the MPC surrogate 


Fig. 5: Representative closed-loop response under the disturbance benchmark. Left: full-horizon signals. Right: zoom around the push interval. The gray bands indicate push windows. The dashed horizontal line indicates the settle threshold computed from pre-disturbance statistics, and the “settled” marker indicates the first time the error remains below this threshold. 

cost-to-go to measured long-horizon returns from closedloop rollouts, the method avoids repeated MPC solves in the learning loop. Simulations show improved value consistency and enhanced robustness to model mismatch and external disturbances, suggesting that cost matching is a practical and computationally efficient way to shape long-horizon locomotion behavior while retaining standard constrained MPC deployment. 

## REFERENCES 

- [1] W. Li, G. Yang, J. Wu, C. Pan, L. Sheng, and Q. Zhang, “A comprehensive review on humanoid robots: perspectives from academia and industry,” _Engineering Information Technology & Electronic Engineering_ , vol. 27, no. 2, p. 250105, 2026. 

- [2] Y.-M. Chen, J. Hu, and M. Posa, “Beyond inverted pendulums: Taskoptimal simple models of legged locomotion,” _IEEE Transactions on Robotics_ , vol. 40, pp. 2582–2601, 2024. 

- [3] S. Katayama, M. Murooka, and Y. Tazaki, “Model predictive control of legged and humanoid robots: models and algorithms,” _Advanced Robotics_ , vol. 37, no. 5, pp. 298–315, 2023. 

- [4] M. Y. Galliker, N. Csomay-Shanklin, R. Grandia, A. J. Taylor, F. Farshidian, M. Hutter, and A. D. Ames, “Planar bipedal locomotion with nonlinear model predictive control: Online gait generation using whole-body dynamics,” in _2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids)_ , 2022, pp. 622–629. 

- [5] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _arXiv preprint arXiv:2501.02116_ , 2025. 

- [6] K. Zhang, Y. Yin, J. Wu, L. Jiang, and Y.-a. Yao, “Gravity-compensated model predictive control and whole-body optimization for humanoid locomotion,” _Journal of Mechanisms and Robotics_ , vol. 18, no. 3, p. 031007, 2026. 

- [7] J. Carpentier and P.-B. Wieber, “Recent progress in legged robots locomotion control,” _Current Robotics Reports_ , vol. 2, no. 3, pp. 231– 238, 2021. 

- [8] J. Peters, S. Vijayakumar, and S. Schaal, “Reinforcement learning for humanoid robotics,” in _Proceedings of the third IEEE-RAS international conference on humanoid robots_ , 2003, pp. 1–20. 

- [9] T. Haarnoja, B. Moran, G. Lever, S. H. Huang, D. Tirumala, J. Humplik, M. Wulfmeier, S. Tunyasuvunakool, N. Y. Siegel, R. Hafner _et al._ , “Learning agile soccer skills for a bipedal robot with deep reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, p. eadi8022, 2024. 

- [10] Y. Li, J. Li, W. Fu, and Y. Wu, “Learning agile bipedal motions on a quadrupedal robot,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 9735–9742. 

- [11] H. Zhang, L. He, and D. Wang, “Deep reinforcement learning for realworld quadrupedal locomotion: a comprehensive review,” _Intelligence & Robotics_ , vol. 2, no. 3, pp. 275–297, 2022. 

- [12] A. S. Chen and K. G. Vamvoudakis, “Robot learning optimal control via an adaptive critic reservoir,” in _2025 IEEE 64th Conference on Decision and Control (CDC)_ , 2025, pp. 3842–3847. 

- [13] W. Gao, Y. Wang, and K. G. Vamvoudakis, “Output-feedback learningbased adaptive optimal control of nonlinear systems,” _Automatica_ , vol. 187, p. 112875, 2026. 

- [14] Z. Zhang, X. Chang, H. Ma, H. An, and L. Lang, “Model predictive control of quadruped robot based on reinforcement learning,” _Applied Sciences_ , vol. 13, no. 1, p. 154, 2022. 

- [15] K. G. Vamvoudakis, Y. Wan, F. L. Lewis, and D. Cansever, _Handbook of reinforcement learning and control_ . Springer, 2021. 

- [16] S. Gros and M. Zanon, “Data-driven economic NMPC using reinforcement learning,” _IEEE Transactions on Automatic Control_ , vol. 65, no. 2, pp. 636–648, 2019. 

- [17] M. Zanon and S. Gros, “Safe reinforcement learning using robust MPC,” _IEEE Transactions on Automatic Control_ , vol. 66, no. 8, pp. 3638–3652, 2020. 

- [18] W. Cai, A. B. Kordabad, and S. Gros, “Energy management in residential microgrid using model predictive control-based reinforcement learning and shapley value,” _Engineering Applications of Artificial Intelligence_ , vol. 119, p. 105793, 2023. 

- [19] W. Cai, A. B. Kordabad, H. N. Esfahani, A. M. Lekkas, and S. Gros, “MPC-based reinforcement learning for a simplified freight mission of autonomous surface vehicles,” in _2021 60th IEEE Conference on Decision and Control (CDC)_ , 2021, pp. 2990–2995. 

- [20] W. Cai, S. Sawant, D. Reinhardt, S. Rastegarpour, and S. Gros, “A learning-based model predictive control strategy for home energy management systems,” _IEEE Access_ , vol. 11, pp. 145 264–145 280, 2023. 

- [21] J.-P. Sleiman, F. Farshidian, M. V. Minniti, and M. Hutter, “A unified MPC framework for whole-body dynamic locomotion and manipulation,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 3, pp. 4688–4695, 2021. 

- [22] F. Farshidian _et al._ , “OCS2: An open source library for optimal control of switched systems,” [Online]. Available: https://github.com/leggedr obotics/ocs2. 

- [23] J. Carpentier, G. Saurel, G. Buondonno, J. Mirabel, F. Lamiraux, O. Stasse, and N. Mansard, “The Pinocchio C++ library – A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives,” in _IEEE International Symposium on System Integrations (SII)_ , 2019. 

- [24] D. E. Orin, A. Goswami, and S.-H. Lee, “Centroidal dynamics of a humanoid robot,” _Autonomous robots_ , vol. 35, no. 2, pp. 161–176, 2013. 

- [25] Y. Nesterov, _Introductory lectures on convex optimization: A basic course_ . Springer Science & Business Media, 2013, vol. 87. 

