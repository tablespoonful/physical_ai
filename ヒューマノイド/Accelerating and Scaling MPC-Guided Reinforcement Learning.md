---
title: "Accelerating and Scaling MPC-Guided Reinforcement Learning for Humanoid Locomotion and Manipulation"
date: "2026-06-04"
authors: "Junheng Li; Liang Wu; Sergio A. Esteban; Lizhi Yang; Ján Drgoňa; Aaron D. Ames"
url: https://arxiv.org/abs/2606.05687
pdf: https://arxiv.org/pdf/2606.05687
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.05687)** / [論文ページ](https://arxiv.org/abs/2606.05687)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Accelerating and Scaling MPC-Guided Reinforcement Learning for Humanoid Locomotion and Manipulation** 

Junheng Li<sup>_∗_1</sup> , Liang Wu<sup>_∗_2</sup> , Sergio A. Esteban<sup>1</sup> , Lizhi Yang<sup>1</sup> , J´an Drgoˇna<sup>2</sup> , and Aaron D. Ames<sup>1</sup> 

**_Abstract_ — In humanoid motion control, model predictive control (MPC) offers physically grounded prediction and constraint handling, while reinforcement learning (RL) enables robust whole-body skills through large-scale simulation. However, using MPC inside RL often requires time-consuming problem construction or excessive training overhead, making such frameworks difficult to justify in practice. This work studies efficient training-time MPC guidance for humanoid locomotion and manipulation, termed** **_MPC-RL_ . We introduce a centroidal-dynamics MPC reward formulation that leverages guidance from MPC trajectories in training time. To make this practical in massively parallel RL, we develop** _π_<sup>_n_</sup> **MPC, a** **<u>parallel-in-horizon</u> and construction-free batched GPU MPC solver that operates directly on time-varying dynamics to avoid high memory usage and pre-compilation. Through a variety of comparative studies and hardware validations, we have found that MPC-RL achieves superior performance in locomotion and manipulation skills. The code base is available at https: //github.com/junhengl/mpc-rl** 

## I. INTRODUCTION 

Recent advances in humanoid locomotion and manipulation control and learning have opened broad opportunities for operation in human-centered environments [1]. Model predictive control (MPC) and reinforcement learning (RL) represent two complementary paradigms for humanoid motion control. MPC provides explicit dynamics modeling, constraint handling, and predictive reasoning [2]–[4], while RL has recently demonstrated impressive robustness and agility [5]–[7]. Therefore, combining MPC and RL has emerged as a promising direction for humanoid control [8]–[10]. 

Recent work has explored RL-augmented MPC for legged and humanoid control, [8], [10], [11] train residual policies and greatly enhance the capability of MPC in deployment. However, such frameworks require efficient test-time MPC solutions and still rely on real-time state estimation. Parallelly, offline optimized trajectory libraries also provide dynamically consistent guidance for RL [7], [12] and avoid excessive computation during training. These frameworks allow dynamic and interactive motion control; however, the exploration is limited to the motion encoded offline. Additionally, there is an increasing interest in the direction of physics-based structure and guidance in RL. For example, 

> _∗_ Equal contribution; 1California Institute of Technology, CA 91106, USA;<sup>2</sup> Johns Hopkins University, MD 21218, USA. Corresponding author email:junhengl@caltech.edu. This work is in part supported by Technology Innovation Institute, The Dow Chemical Company project #227027AW, Westwood Robotics, the Ralph O’Connor Sustainable Energy Institute at Johns Hopkins University, and by the U.S. DOE, Office of Science, ASCR program under the Scientific Discovery through Advanced Computing (SciDAC) Institute “LEADS: LEarningAccelerated Domain Science”. 


Fig. 1: **MPC-RL Experiment Snapshots.** a). Walking on treadmill; b). Wearing an unknown 10 kg vest while walking; c). Push-recovery; d). Carrying an unknown 10 kg payload while walking; e). Pushing a 290kg cart. Full video: https://youtu.be/PrcbXkA1kYg 

Dai _et al._ [13] leverages analytical gait synthesis with CLFbased reward structure for future foot placement guidance in highly unstructured terrain. Krishna _et al._ [14] uses interpolated oracle guidance for multi-modal locomotion. In short, predictive guidance can provide dynamically consistent motion targets, contact-aware structure, and long-horizon task information that are often difficult to recover from reward design alone. 

In the aerial robotics community, training-time MPCguided learning has shown strong promise, where MPC can provide physically structured supervision for learned policies [15], [16]. Zhang _et al._ [17] used MPC-guided policy search to train quadrotor policies from full-state MPC rollouts, enabling lower-cost onboard execution at test time. 

Extending long-horizon MPC guidance to humanoid RL remains challenging: repeated batched MPC solves force a tradeoff between prediction length, update rate, and training time [18], [19]. Recent GPU-based MPC solvers reduce the cost of running many MPC instances in parallel during RL training [20], [21]. However, existing approaches often parallelize across environments more naturally than across the prediction horizon, leaving horizon-wise recursions or sequential optimization steps as a bottleneck. Traditionally, forming MPC as sparse QP problems scales poorly with problem size in VRAM usage and in symbolic compilation resources, requiring time-consuming problem construction [8]. Therefore, a _construction-free_ and _memory-efficient_ batched solver is highly needed. Additionally, most prior 


Fig. 2: MPC-Guided Reinforcement Learning (MPC-RL) Architecture. During training, MPC generates per-environment predictive references through _π_<sup>_n_</sup> MPC batched solver, which are converted into prediction landmark rewards for PPO; at deployment, the learned policy deploys without MPC. 

studies incorporating this MPC _↔_ RL hybrid approach focus primarily on locomotion [22], while MPC-guided RL for loco-manipulation remains under-explored, where physical and interactive models are higly valuable [7]. 

In this work, we study the role of training-time MPC guidance in RL for humanoid locomotion and loco-manipulation. The core architecture is shown in Figure 2. In this work, we make three main contributions. (1) We present a structured MPC-based reward for RL, using prediction-confidence weighting to extract long-horizon motion and dynamics guidance from centroidal MPC trajectories, and we provide a systematic empirical study of its effect through ablations on horizon length, update rate, and reward structure. (2) We introduce _π_<sup>_n_</sup> MPC, a <u>parallel-in-horizon,</u> constructionfree batched MPC solver that extends the original monolithic and time-invariant _π_ MPC structure [23] to legged robots with time-varying dynamics matrices, enabling compilationfree and memory-efficient batched solves over long horizons. (3) We extend the MPC-guided RL architecture beyond locomotion to humanoid loco-manipulation, demonstrating box-pushing on hardware with up to 290 kg (639 lbs) cart payload, corresponding to 829% of the robot body mass. Together, these results show how powerful predictive optimization can serve both as a practical training tool and as a source of structure for learning humanoid behaviors with competitive training efficiency. 

## II. CENTROIDAL-DYNAMICS MPC GUIDANCE 

This section describes the centroidal-dynamics [24] MPC (CD-MPC) module used to provide predictive guidance during RL. The purpose of CD-MPC is not to directly control the humanoid at deployment, but to generate CoM, momentum, ground reaction force (GRF), and footstep references during massive-parallel training as structured rewards. 

## _A. Centroidal Dynamics Model_ 

Let _q ∈_ R<sup>_nq_</sup> and _q_ ˙ _∈_ R<sup>_nq_</sup> denote the full-order humanoid configuration and velocity. We define the centroidal state as 


where _c ∈_ R<sup>3</sup> is the center-of-mass (CoM) position, _lG ∈_ R<sup>3</sup> is the centroidal linear momentum, and _kG ∈_ R<sup>3</sup> is the centroidal angular momentum about the CoM. 

Based on the continuous-time CD [24], using timestep ∆ _t_ , the discrete CD are 


where _m_ is the total robot mass, _g_ is the gravity vector, _Ck_ is the active contact set at step _k_ , _pi,k_ is the position of contact _i_ , and ( _fi,k, τi,k_ ) are the corresponding contact force and moment. For locomotion, _Ck_ contains the foot contacts planned by Raibert heuristics; for loco-manipulation, it can additionally include hand contacts to reason external interaction forces with environment. 

## _B. CD-MPC Formulation_ 

At planning time _t_ , CD-MPC solves a finite-horizon optimal control problem over _N_ steps, with horizon length 


The decision variables are the centroidal states and contact wrenches 


The initial centroidal state is obtained from the current fullorder simulation state, _ξ_ 0 = _ϕ_ ( _qt, q_ ˙ _t_ ), where _ϕ_ maps the full-order state to the centroidal state. 

The CD-MPC problem is formulated as 


where _uk_ := _{fi,k, τi,k}i∈Ck_ and _f_ ∆ _t_ denotes the discrete CD from (2)–(4). _Fi,k_ and _Ti,k_ denote the constraint sets based on contact wrench cone (CWC) [25] and friction pyramid. 

The stage and terminal cost contains velocity tracking, CoM tracking, angular momentum regulation, and control input regularization: 


where _vk_<sup>_c_=</sup> _m_ <u>1</u><sup>_lG,k_.Fornominallocomotion,</sup><sup>_k_</sup> _G,k_<sup>refand</sup><sup>_c_</sup> _k_<sup>ref</sup> are chosen based on the reference structure proposed in [26]. 

## _C. MPC Landmark Guidance Reward_ 


A naive use of this trajectory is to track only the next MPC prediction. However, this discards the longer-horizon structure of MPC. We instead extract a small set of predictive landmarks from the full trajectory. Let 

_δℓ_ = _nℓ_ ∆ _t, nℓ_ = 1+ _⌊sℓ_ ( _N −_ 1) _⌋, sℓ ∈_ [0 _,_ 1] _,_ (10) where _ℓ_ = 0 _, . . . , NL −_ 1, _s_ 0 = 0, and _sNL−_ 1 = 1. Thus, _δ_ 0 corresponds to the next MPC step and _δNL−_ 1 = _H_ corresponds to the end of the horizon. 

For each MPC solve at time _t_ , we store the landmarks 


When the rollout reaches time _t_ , the realized CoM can be compared against the landmarks predicted for this same time from previous MPC solves. We define 


where unavailable landmarks at the beginning of an episode are omitted. The CoM MPC-guidance reward is then 


The weights follow a horizon-monotone schedule 


which we refer to as _prediction-confidence weighting_ . The schedule encodes a prediction-confidence prior: near-horizon landmarks are weighted more heavily because they are less affected by centroidal model mismatch and integration error, while far-horizon landmarks are down-weighted. 

**Remark 1.** _The single exponential form in_ (13) _fuses all landmark residuals into one bounded reward rt_<sup>mpc</sup><sup>_,c_</sup> _∈_ (0 _,_ 1] _. Two limiting cases recover familiar designs: if α_ 0 = 1 _and αℓ>_ 0 = 0 _, the reward reduces to strict next-step MPC supervision; if αℓ_ = 1 _/NL, it becomes a time-averaged trajectorytracking objective. In all of our MPC-RL experiments, we set the confidence-weighted schedule to a horizon-tapered profile α_ = _{_ 0 _._ 5 _,_ 0 _._ 25 _,_ 0 _._ 15 _,_ 0 _._ 07 _,_ 0 _._ 03 _}, allowing the policy to_ 

_exploit long-horizon MPC structure while keeping the nearterm tracking signal sharp._ 

The same landmark construction is used for other MPCguided quantities, including CoM velocity and angular momentum references. The total PPO reward is 


where _rt_<sup>reg</sup> contains the standard regularization rewards and _rt_<sup>mpc</sup> collects the CD-MPC landmark guidance terms, which is covered in more detail in Section IV. 

## III. _π_<sup>_n_</sup> MPC: PARALLE-IN-HORIZON AND CONSTRUCTION-FREE BATCHED MPC SOLVER 

To enable MPC solving effort and guidance lightweight during RL training, we build on top of the parallel-in-horizon ADMM structure of previous work _π_ MPC [23]. Unlike the native Julia implementation _π_ MPC with time-invariant state matrices for monolithic MPC solve, we adapt to the timevarying nature of the legged locomotion dynamics and allow storage of time-varying state matrices along the horizon for massive-parallel evaluations. The implementation is migrated and realized in both PyTorch and JAX, termed _π_<sup>_n_</sup> _MPC_ . At every MPC step, we solve a linearized CD-MPC in the standard form following eqn. (7), 


where _ξk_ is the centroidal state defined in Sec. II and _uk_ denotes contact wrenches. The state matrices _{Ak, Bk, ek}_<sup>_N_</sup> _k_ =0<sup>_−_1</sup> are obtained along the input periodic contact sequence. 

Unlike previous ADMM-based MPC approaches, _π_<sup>_n_</sup> MPC achieves parallel-in-horizon and construction-free while maintaining simple, low-cost operation at each iteration by employing a velocity-form MPC and a novel variablesplitting scheme. **(1) The velocity-form MPC scheme:** we optimize over input increments. Define the lifted state 


The lifted constraints are written compactly as _ξ_<sup>¯</sup> _k_ +1 _∈ X_<sup>¯</sup> _k_ , where _X_<sup>¯</sup> _k_ = _Xk × Uk_ . **(2) The proposed variable-splitting scheme:** we introduce auxiliary variables _zk_ +1 = _ξ_<sup>¯</sup> _k_ +1 and _vk_ = _B_<sup>¯</sup> _k_ ∆ _uk_ , yielding the following optimization problem, 


straintwhere theset indicator _zk_ +1 _∈_ function _X_ ¯ _k_ +1. _Note_ Π _X_ ¯ _k_ +1 _that_<sup>(</sup><sup>_zk_+1</sup> _the_<sup>)denotes</sup> _above_<sup>the</sup> _splitting_<sup>con-</sup> _scheme is the key to achieving linear parallel-in-horizon and construction-free features, such as making a copy of vk_ = _B_<sup>¯</sup> _k_ ∆ _uk instead of vk_ = ∆ _uk, and incorporating zk_ +1 _, rather than ξ_<sup>¯</sup> _k_ +1 _, into the dynamical equation._ 

_batch dimension, so the local ADMM updates at all horizon indices can be executed in parallel on the GPU rather than through a sequential Riccati-style recursion. In addition, the solver is construction-free: it operates directly on the timevarying dynamics {Ak, Bk, ek}_<sup>_N_</sup> _k_ =0<sup>_−_1</sup><sup>_and avoids assembling a_</sup> _sparse MPC-QP at every update. This is particularly useful for RL training to avoid high VRAM usage or problemspecific compilation or symbolic code generation ahead of time (e.g., [20]), π_<sup>_n_</sup> _MPC is implemented with standard batched operations and can adapt online._ 

The augmented Lagrangian (with the scaled-form Lagrangian variable) of Problem (20) is given by 


**Remark 3.** _Furthermore, to accelerate the convergence speed, the π_<sup>_n_</sup> _MPC implementation inherits Nesterov’s acceleration scheme with the restart option, whose details can be found in previous work [23], [27]._ 

## IV. MPC-GUIDED REINFORCEMENT LEARNING 

This section presents the implementation details of the MPC-RL training and deployment infrastructure. 

where ( _θk, βk, λk_ ) denotes the scaled dual variables for equality constraints (20b), (20c), and (20d), respectively; _ρ_ denotes the ADMM parameter. In our variable-splitting scheme, the three block variable ADMM updates are 

## _A. Training Setup_ 

We train the policy with PPO using rsl-rl on top of mjlab [28], running _N_ env = 4096 environments. Physics is integrated at 200 Hz with with a control rate of 50 Hz. Episodes last at most _T_ max = 20 s (1000 control steps). The action _at ∈_ R<sup>29</sup> is a joint-position delta around the default pose _q_<sup>_⋆_</sup> , with action scale 0 _._ 5 and tracked by perjoint PD controllers; the actor’s policy is therefore directly deployable on hardware _without_ the MPC in the loop at the test time. The actor and critic are independent MLPs of width (512 _,_ 256 _,_ 128) with ELU activations and a Gaussian action distribution with a learnable scalar standard deviation. 


before ADMM iterations, the above updates (21) result in the following closed-form horizon-parallel updates at ( _m_ +1)-th ADMM iteration: 

## _B. Policy Observations_ 


The complete reward structure is listed in Table I. The locomotion-driving signal is the MPC stack that collectively replaces the base-RL velocity-command-tracking rewards and the angular-momentum regularizer by supervising the centroidal-MPC’s predicted CoM trajectory under 

The proof and the detailed derivations (such as the update of _zk_ +1) can be found in our previous work [23]. 

**Remark 2.** _π_<sup>_n_</sup> _MPC exposes the prediction horizon as a_ 

TABLE I: Locomotion Training Reward Structure. 

|Term|Expression|Weight|
|---|---|---|
|**Base-RL rewar**|**ds** (Only appear in MPC-free baseline training)<br>||
|lin<br>~~v~~el|exp(_−∥ev∥_<sup>2</sup>_/_0_._25)<br><br>|+2_._0|
|ang<br>~~v~~el<br>ang<br>~~v~~el<br>~~r~~eg <br>ang<br>~~m~~om<br>~~r~~eg|exp(_−_(_e_<sup>2</sup><br>_ω_ <sup>+</sup><sup>_∥ωxy∥_2)</sup><sup>_/_0</sup><sup>_._5)</sup><br> _−∥ωxy∥_<sup>2</sup><br><br> _−∥k∥_<sup>2</sup><br>|+2_._0<br>_−_5_×_10<sup>_−_2</sup><br>_−_2_×_10<sup>_−_2</sup>|
|foot<br>~~s~~lip|_−_<sup>�</sup><br>_i _<sup>_∥_˙</sup><sup>_pxy_</sup><br>_i _<sup>_∥_2 1[ctc</sup><sup>_i_]</sup><sup>_g_</sup>|_−_0_._10|
|**MPC rewards** (|Only appear in MPC-RL training)<br>||
|mpc<br>~~c~~om|exp(_−_<sup>�</sup><br>_j _<sup>_αj∥ej_</sup><br>_c_<sup>_∥_2)</sup><sup>_, j_ = 1</sup><sup>_,_ 2</sup><sup>_, . . ._ 5</sup><br>|+2_._0|
|mpc<br>~~l~~in<br>~~v~~el|exp(_−_<sup>�</sup><br>_j _<sup>_αj∥e j_</sup><br>˙_c _<sup>_∥_2</sup><sup>_/_0</sup><sup>_._25)</sup><sup>_, j_ = 1</sup><sup>_,_ 2</sup><sup>_, . . ._ 5</sup><br><br>|+2_._0|
|mpc<br>~~a~~ng<br>~~m~~om|_−_<sup>�</sup><br>_j _<sup>_αj_(</sup><sup>_∥ej_</sup><br>_k_<sup>_∥_2</sup><sup>_/_0</sup><sup>_._5 + 0</sup><sup>_._01</sup><sup>_∥_˙</sup><sup>_ej_</sup><br>_k_<sup>_∥_2)</sup><br><br>|+5_×_10<sup>_−_2</sup>|
|mpc<br>~~f~~oot|mean_i∈S_exp(_−∥p_<sup>_xy_</sup><br>_i_<br>_−p_<sup>_m_</sup><br>_i _<sup>_∥_2</sup><sup>_/_0</sup><sup>_._04)</sup><br>|+1_._0|
|mpc<br>~~g~~rf|_−_<br>~~�~~<br>1<br>6<br>�<br>_j_<sup>(</sup><sup>_fj −fm_</sup><br>_j_ <sup>)2</sup><br>|+2_×_10<sup>_−_3</sup>|
|**Regularization **|**rewards** (Appear in all trainings)||
|pose|exp(_−_<br>(_q −q_<sup>_∗_</sup>)<sup>2</sup>_/σ_<sup>2</sup>(_v_<sup>_c_</sup>)_−∥g_<sup>_b_</sup><br>_xy_<sup>_∥_2</sup><sup>_/_0</sup><sup>_._2)</sup>|+1_._0|
|gait|mean_i_1[ctc_i_ =_si_(_ϕ_)]|+1_._0|
|foot<br>~~c~~lear<br>|_−_<sup>�</sup><br>_i _<sup>_|hi −h∗| ∥_˙</sup><sup>_pxy_</sup><br>_i _<sup>_∥g_</sup><br>|_−_4_._0|
|stand<br>~~s~~till <br>|_−∥q −q_<sup>_∗_</sup>_∥_<sup>2 </sup>1[_∥v_<sup>_c_</sup>_∥<_0_._1]<br>|_−_4_._0|
|action<br>~~r~~ate|_−∥at −at−_1_∥_<sup>2</sup><br>|_−_0_._25|
|foot<br>~~h~~eight|_−_<sup>�</sup><br>_i_<sup>(</sup><sup>_h_pk</sup><br>_i _<sup>_/h∗−_1)2 1</sup><sup>_i_</sup>|_−_0_._25|
|joint<br>~~l~~im|_−_<sup>�</sup><br>_j_<sup>([</sup><sup>_qj −q_max</sup><br>_j_<br>]++ [_q_<sup>min</sup><br>_j_<br>_−qj_]+)|_−_1_._0|
|self<br>~~c~~oll.|_−_<sup>�</sup><br>_c∈g_ <sup>1[</sup><sup>_∥fc∥>_ 10 N]</sup>|_−_1_._0<sup>_†_</sup><br>|
|soft<br>~~l~~and|_−_<sup>�</sup><br>_i _<sup>_∥fi∥_1[land</sup><sup>_i_]</sup>|_−_10<sup>_−_5</sup>|


> _†_ feet–feet, hip–abad, hip–hand, foot–leg. 

the prediction-confidence weighting schedule of Eq. (13); mpc ~~a~~ ng ~~m~~ om regulates angular momentum against the MPC reference; mpc ~~f~~ oot adds a spatial signal for foot placement against the Raibert-heuristic landing targets; and a small mpc ~~g~~ rf coefficient softly aligns the foot groundreaction forces with the MPC’s optimal solution, bridging the centroidal abstraction and the full-body dynamics. The shared regularization block is held identical to the baseRL configuration, so that any locomotion-quality difference between the two reward stacks is attributable to the MPCguided block alone. 

## _D. Effective-Inertia-Based Joint PD Gain Selection_ 

For training and hardware deployment on Themis, we select joint PD gains based on the effective inertia observed at each joint. Around a nominal configuration _q_<sup>_⋆_</sup> , the local joint dynamics are approximated as 


Here, _Mii_ ( _q_<sup>_⋆_</sup> ) is the diagonal rigid-body inertia seen at joint _i_ , including downstream link effects, and _Ai_ denotes the joint armature, including motor-reflected inertia and actuator-side effects. Matching (23) to a second-order system gives 


where _ωn,i_ is the desired natural frequency and _ζi_ is the damping ratio. 

Unlike reflected-inertia-only heuristics [29] that set gains from _Ai_ alone with a fixed high natural frequency, we include the downstream inertia term _Mii_ ( _q_<sup>_⋆_</sup> ) and intentionally 


Fig. 3: Scalability of Batched GPU MPC Solvers. ( _×_ means CUDA out of memory; Number of max iteration is 200 for consensus ADMM and _π_<sup>_n_</sup> MPC, 20 for qpth, 30 for qpax, and 5 PDIPM iterations for CusADi. Note CusADi compilation takes 1.5 hr and requires 150 GB RAM for _N_ = 10.) 

choose a low _ωn,i_ . This is necessary for Themis because its high-inertia, low gear-ratio actuators do not perform as stiff servo-like motors ( _e.g.,_ G1), and can excite unmodeled actuator compliance when high-bandwidth gains are used. Therefore, carefully selecting a favorable actuator natural frequency based on actuator behavior is key (1-2 Hz for our case). The resulting lower-bandwidth impedance improves hardware stability and avoids severe chatter at the hip and knee joints. A motor gain comparison is shown in Table IV. 

## V. RESULTS 

This section evaluates the proposed MPC-guided Reinforcement Learning (MPC-RL for short) framework from three perspectives. We first characterize the computational scalability of _π_<sup>_n_</sup> MPC inside massively parallel training. We then study the effect of MPC guidance on humanoid locomotion through empirical comparisons. Finally, we extend to a loco-manipulation task involving payload pushing. 

## _A. Experimental Setup_ 

The desktop setup for training and evaluation consists of an Intel Ultra 9 285k CPU, an Nvidia RTX 5090 GPU (32GB VRAM), and 64 GB of RAM. The trained policy receives the same observation space across all ablations; only the reward guidance or MPC configuration is varied. We evaluate the locomotion and loco-manipulation policies on the Westwood Robotics Themis V2 humanoid robot with custom Pythonbased deployment infrastructure. 

## _B. Acceleration and Scalability of π_<sup>_n_</sup> _MPC_ 

We first evaluate the efficiency and scalability of _π_<sup>_n_</sup> MPC on the same CD-MPC problem used during training with SOTA methods, including qpax, a JAX-based batch QP solver [30], qpth, a PyTorch-based batch QP solver [31], CusADi, a symbolic GPU solver [20], and consensus ADMM, a custom batched implementation of [32], with 

TABLE II: Time-varying velocity tracking, push-recovery, and constraint-satisfaction comparison between Pure RL and MPC-RL under different MPC horizons and update rates. ( _↑_ high is better, _↓_ lower is better.) 

|Method|Training-time MPC|Time-var|ying velocity tracking RMSE _↓_||Max recoverable push force (|N) _↑_||Constr|aint satisf|action _↑_|
|---|---|---|---|---|---|---|---|---|---|---|
||_N_<br>Rate|_vx_<br>_vy_|_ωz_<br>_v_<sup>OOD</sup><br>_x_<br>_v_<sup>OOD</sup><br>_y_<br>_ω_<sup>OOD</sup><br>_z_|0<sup>_◦_</sup>|45<sup>_◦_</sup>90<sup>_◦_</sup>135<sup>_◦_</sup>180<sup>_◦_</sup>225<sup>_◦_</sup>|270<sup>_◦_</sup>|315<sup>_◦_</sup>|Friction|CWC-_y_|CWC-_x_|
|Pure RL|–<br>–|0.1609 0.1566|0.0912<br>0.2310 0.1975 **0.1113**|300|350 100<br>300<br>350<br>225|125|275|100%|57.2%|92.0%|
||10<br>5 Hz|0.1374 0.1342|0.1060<br>0.2052 0.1851 0.1138|325|375<br>75<br>325<br>425<br>325|75|125|100%|69.8%|98.2%|
||10<br>10 Hz|**0.1280**<br>**0.1326**|0.0928<br>**0.1949**<br>**0.1761**<br>0.1171|375|375<br>125<br>**400**<br>**450**<br>**375**|100|350|100%|**91.8**%|94.0%|
|MPC-RL|10<br>25 Hz|0.1340 0.1455|0.1058<br>0.1977 0.1868 0.1399|**425**|375 175<br>250<br>350<br>300|200|375|100%|84.8%|94.8%|
||10<br>50 Hz|0.1464 0.1375|0.1050<br>0.2049 0.1811 0.1411|400|375 150<br>350<br>400<br>325|200|**400**|100%|82.0%|98.2%|
||30<br>10 Hz|0.1438 0.1337|**0.0873**<br>0.2109 0.1834 0.1374|325|**400** 175<br>275<br>400<br>350|125|300|100%|87.8%|**99.0**%|
||50<br>10 Hz|0.1316 0.1511|0.0923<br>0.1985 0.1842 0.1259|325|350 **200**<br>350<br>375<br>325|**300**|350|100%|81.0%|96.0%|
|The highli|ghted row is the de|fault MPC-RL coi|nfiguration, _N_ = 10 at 10 Hz. OOD|comma|nd bounds are 50% higher than|the|in-distrib|ution com|mands.||
||Linear Veloci|ty Tracking Score (|Horizon length Comparison)||Linear Velocity Tracking Sco|re (M|PC Updat|e Rate Com|parison)||
|0.0<br>0.2<br>0.4<br>0.6<br>_s_vel<br>_t_|<br> <br> <br>|Pure RL baseline<br>MPC-RL (N=10)<br>MPC-RL (N=30)<br>MPC-RL(N=50)||0.0<br>0.2<br>0.4<br>0.6<br>_s_vel<br>_t_|Pure RL baseline<br>MPC-RL (5 Hz)<br>MPC-RL (10 Hz<br>MPC-RL (25 Hz<br>MPC-RL(50 Hz|<br>)<br>)<br> )|||||
||0<br>2000<br>4000<br>Training ite|6000<br>ration<br>|0<br>1<br>2<br>3<br>Wall-clock time (hours)|0|2000<br>4000<br>6000<br>Training iteration|0|W|1<br>all-clock tim|2<br>e (hours)|3|
|(a)|Varying MPC trainin|g-time horizon le|ngth (all runs are at 10 Hz rate).|(b)|Varying MPC training-time updat|e rate|(all run|s have fixe|id _N_ = 1|0).|


Fig. 4: Comparison of locomotion velocity-tracking score metric vs. training steps and wall-clock time under different MPC-RL settings. 

QP-splitting structure following OSQP [33]. As shown in Fig. 3, in the _N_ = 10 case, _π_<sup>_n_</sup> MPC scales more favorably on GPU than consensus ADMM, qpth, and qpax as the number of parallel environments increases. CusADi shares comparable solve speed, but its symbolic compilation takes around 1.5 hours for our MPC problem. Our advantage is especially clear for longer horizons, where qpth and qpax are unable to provide competitive solve time for comparison here; CusADi requires substantially longer compilation time ( _>_ 5 hrs) and high RAM usage, and thus are omitted from the rest of the plots. Consensus ADMM either becomes substantially slower or runs out of VRAM, while _π_<sup>_n_</sup> MPC remains feasible by parallelizing over both environments and horizon steps even to _N_ = 400. 

Note that _π_<sup>_n_</sup> MPC’s JAX implementation is generally more computationally efficient than the PyTorch implementation; however, in RL training, _π_<sup>_n_</sup> MPC-JAX’s memory overhead is sizably larger than the PyTorch variant due to the memory splitting and pre-allocation. 

## _C. Humanoid Locomotion with MPC-RL_ 

Having established that long-horizon CD-MPC can be computed at training scale, we next study how this predictive guidance can improve humanoid locomotion learning. Here, we set MPC ∆ _t_ = 0 _._ 7s, such that 5∆ _t_ makes up one stride. 

_1) Choosing the right MPC setup:_ First, we study how the training-time MPC update rate and prediction horizon affect the final locomotion policy. Table II shows that MPCRL consistently improves translational velocity tracking over Pure RL across velocity command tracking tests, includ- 

ing out-of-distribution commands. MPC-RL variants also outperform the RL baseline in all tested directions under push-recovery experiments. We additionally evaluate the contact constraint satisfaction during deployment, training-time MPC’s friction cone and CWC constraints, and their shaping to GRF guidance leads to improved constraint satisfaction over base RL’s foot ~~s~~ lip penalty alone. 

We compare the effects of training-time MPC horizon number with a fixed 10 Hz update rate. Although longer horizons provide more lookahead, Table II and Fig. 4a show that performance does not improve monotonically with horizon length; the _N_ = 10 setting (one complete gait cycle lookahead) gives the strongest overall velocity-tracking and push-recovery behavior, while maintaining a very competitive training efficiency compared to baseline RL. We further compare training-time MPC update rates at a fixed horizon _N_ = 10. The 10 Hz setting achieves the best overall tracking performance with good training efficiency, while higher-rate guidance does not further improve the learned policy. This trend is also reflected in Fig. 4b, where increasing the MPC rate exhibits diminishing returns on policy performance. 

_Therefore, we use N=10, 10 Hz training-time MPC setup for the following experiments in this paper. The locomotion policy is trained to 15k iterations under 6 hours._ 

_2) Comparison of Model-based Guidance Reward Design:_ Finally, we compare the model-free baseline and modelbased reward structures seen in the current literature. Comparing (i) baseline pure RL reward, (ii) constructing MPC landmarks as CLF-based reward [34], (iii) interpolated oracle guidance reward [14], and (iv) the proposed MPC-guided 

TABLE III: Performance comparison of model/trajectoryguided RL methods for humanoid locomotion. 

|Reward<br>|Tracking|RMSE _↓_|Max|reco|very for|ce (N) _↑_|_s_<sup>vel</sup><br>_t _<sup>_/s_</sup><br>|<sup>vel</sup><br>max<br>_†_ (|%) _↑_|
|---|---|---|---|---|---|---|---|---|---|
|Method|_vx_|_vy_|0<sup>_◦_</sup>|90<sup>_◦_</sup>|180<sup>_◦_</sup>|270<sup>_◦_</sup>|30min|45min|1hr|
|Baseline RL|0.161|0.157|300|100|350|125|**24.3**|52.6|63.7|
|CLF-RL [34]|0.151|0.139|375|125|350|150|11.8|18.9|54.9|
|OGMP [14]|0.148|0.161|375|**200**|375|150|22.9|26.7|33.0|
|MPC-RL||||||||||
|Next-step|0.190|0.170|325|125|350|100|18.7|25.0|68.7|
|Averaged|0.134|0.136|**425**|150|350|150|21.9|28.2|71.5|
|**Tapered**|**0.128**|**0.132**|400|150|**450**|**250**|16.7|**60.0**|**77.7**|


_↑_ high is better, _↓_ lower is better. _†_ % progress of a unified linear velocity tracking score metric during training. 

reward. We additionally compare the choice of _α_ in the MPC landmark schedule, including “next-step” _{_ 1 _,_ 0 _,_ 0 _,_ 0 _,_ 0 _}_ , “averaged” _{_ 0 _._ 2 _,_ 0 _._ 2 _,_ 0 _._ 2 _,_ 0 _._ 2 _,_ 0 _._ 2 _}_ , and the proposed “tapered” _{_ 0 _._ 5 _,_ 0 _._ 25 _,_ 0 _._ 15 _,_ 0 _._ 07 _,_ 0 _._ 03 _}_ . 

As Table III suggests, the proposed MPC-guided reward structure with tapered landmark weighting has clear advantages in locomotion velocity and push recovery performance against the other model-guided reward design approaches. We compare the progress of the linear velocity tracking score during training, and the MPC-RL achieves faster progress (higher % in unit time) even compared to the pure RL approach, despite parallel MPCs adding slightly more training iteration time. The proposed horizon-wise tapered tracking schedule works more favorably than the immediate next-step or average-weighted tracking schedule. 

We validate the proposed MPC-RL policy on hardware – as Figure 1(a-e) presents, we demonstrate MPC-RL’s hardware transferability and robustness via unknown disturbances, including external weights and pushes. 

## _D. Humnoid Loco-Manipulation with MPC-RL_ 

We further evaluate the proposed MPC-RL framework on a humanoid box-pushing task, using a loco-manipulation MPC at training time to generate additional hand-pushing force references and box state references. Compared with the pure RL baseline, the structured MPC rewards provide more informative exploration signals by guiding the policy toward dynamically consistent CoM, momentum, and contact-force behaviors during pushing. 

We compare the standard pure RL training vs. MPC-RL in this setting. Both trainings involve boxes with random masses in the training environment. Pure RL adds box and body velocity tracking rewards, body-box velocity matching rewards, and contact sticking rewards to incentivize pushing, whereas MPC bundles centroidal state and reaction force predictions into a structured MPC reward. As a result, as shown in Figure 5, the MPC-guided policy achieves better velocity tracking and stronger pushing capability over the baseline, which stalls from the beginning. The locomanipulation policy uses the same observation space as the locomotion MPC-RL policy and does not require runtime feedback of object states or parameters, unlike pure MPC approaches. 


Fig. 5: Velocity tracking comparison in box-pushing simulation. The robot is commanded to push a 20kg, 1m _×_ 1m _×_ 1m box with a contact friction coefficient of 0.2. 

We validate this loco-manipulation policy on hardware, as shown in Figure 1(f), the robot is capable of pushing up to 290 kg (639 lbs) payload, which is equivalent to 829% body mass. The measured pushing force required for this cart is about 180 N. These results suggest that training-time MPC guidance is not limited to locomotion tracking but can also provide useful physical structure for discovering forceful loco-manipulation, where pure RL suffers from excessive exploration. 

## VI. CONCLUSION AND FUTURE PERSPECTIVES 

This work presented an efficient MPC-guided reinforcement learning framework for humanoid locomotion and locomanipulation. By combining prediction-confidence weighting with _π_<sup>_n_</sup> MPC, the proposed method provides structured centroidal-dynamics guidance during training while avoiding test-time MPC. The results show improved velocity tracking, push-recovery robustness, and reward progression over pure RL and model-guided baselines, with practical training overhead. We further demonstrated that the same framework can guide forceful loco-manipulation, enabling hardware pushing of heavy payloads over 600 lbs on a cart. 

We intend to use this work as a first step to showcase the validity and significance of structured MPC guidance in RL. There are still limitations in the reliance on reducedorder centroidal dynamics with prescribed contact schedules. Additionally, the inherent limitation of numerical solvers still presents scaling limitations regardless. Future work will extend the framework to richer contact modes with 

nonlinear MPC to account for the robot model and contact interaction with more fidelity. We will investigate using neural-network-augmented batch MPC solvers to enable very efficient training-time nonlinear MPC guidance in humanoid reinforcement learning. 

## REFERENCES 

- [1] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu, _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _IEEE/ASME Transactions on Mechatronics_ , vol. 31, no. 2, pp. 2300–2330, 2026. 

- [2] C. Khazoom, S. Hong, M. Chignoli, E. Stanger-Jones, and S. Kim, “Tailoring Solution Accuracy for Fast Whole-body Model Predictive Control of Legged Robots,” _arXiv preprint arXiv:2407.10789_ , 2024. 

- [3] G. Romualdi, S. Dafarra, G. L’Erario, I. Sorrentino, S. Traversaro, and D. Pucci, “Online non-linear centroidal mpc for humanoid robot locomotion with step adjustment,” in _2022 International Conference on Robotics and Automation (ICRA)_ , pp. 10412–10419, IEEE, 2022. 

- [4] P. M. Wensing, M. Posa, Y. Hu, A. Escande, N. Mansard, and A. Del Prete, “Optimization-based control for dynamic legged robots,” _IEEE Transactions on Robotics_ , vol. 40, pp. 43–63, 2023. 

- [5] Z. Li, X. Cheng, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for robust parameterized locomotion control of bipedal robots,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 2811–2817, IEEE, 2021. 

- [6] J. Dao, H. Duan, and A. Fern, “Sim-to-real learning for humanoid box loco-manipulation,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 16930–16936, IEEE, 2024. 

- [7] F. Liu, Z. Gu, Y. Cai, Z. Zhou, H. Jung, J. Jang, S. Zhao, S. Ha, Y. Chen, D. Xu, _et al._ , “Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid loco-manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [8] J. Kamohara, F. Wu, C. Wamorkar, S. Hutchinson, and Y. Zhao, “RL-augmented Adaptive Model Predictive Control for Bipedal Locomotion over Challenging Terrain,” _arXiv preprint arXiv:2509.18466_ , 2025. 

- [9] S. H. Bang, C. A. Jov´e, and L. Sentis, “Rl-augmented mpc framework for agile and robust bipedal footstep locomotion planning and control,” in _2024 IEEE-RAS 23rd International Conference on Humanoid Robots (Humanoids)_ , pp. 607–614, IEEE, 2024. 

- [10] S. H. Jeon, H. J. Lee, S. Hong, and S. Kim, “Residual MPC: Blending Reinforcement Learning with GPU-Parallelized Model Predictive Control,” _arXiv preprint arXiv:2510.12717_ , 2025. 

- [11] Y. Chen and Q. Nguyen, “Learning agile locomotion and adaptive behaviors via rl-augmented mpc,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 11436–11442, IEEE, 2024. 

- [12] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang, “Amo: Adaptive motion optimization for hyper-dexterous humanoid wholebody control,” _arXiv preprint arXiv:2505.03738_ , 2025. 

- [13] M. Dai, W. D. Compton, J. Li, L. Yang, and A. D. Ames, “Walk the PLANC: Physics-Guided RL for Agile Humanoid Locomotion on Constrained Footholds,” _arXiv preprint arXiv:2601.06286_ , 2026. 

- [14] L. Krishna, N. Sobanbabu, and Q. Nguyen, “Ogmp: Oracle guided multi-mode policies for agile and versatile robot control,” _arXiv preprint arXiv:2403.04205_ , 2024. 

- [15] A. Romero, Y. Song, and D. Scaramuzza, “Actor-critic model predictive control,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 14777–14784, IEEE, 2024. 

- [16] C. Greatwood and A. G. Richards, “Reinforcement learning and model predictive control for robust embedded quadrotor guidance and control,” _Autonomous Robots_ , vol. 43, no. 7, pp. 1681–1693, 2019. 

- [17] T. Zhang, G. Kahn, S. Levine, and P. Abbeel, “Learning deep control policies for autonomous aerial vehicles with mpc-guided policy search,” in _2016 IEEE international conference on robotics and automation (ICRA)_ , pp. 528–535, IEEE, 2016. 

- [18] F. Jenelten, J. He, F. Farshidian, and M. Hutter, “Dtc: Deep tracking control,” _Science Robotics_ , vol. 9, no. 86, p. eadh5401, 2024. 

- [19] R. Reiter, J. Hoffmann, D. Reinhardt, F. Messerer, K. Baumg¨artner, S. Sawant, J. Boedecker, M. Diehl, and S. Gros, “Synthesis of model predictive control and reinforcement learning: Survey and classification,” _Annual Reviews in Control_ , vol. 61, p. 101045, 2026. 

- [20] S. H. Jeon, S. Hong, H. J. Lee, C. Khazoom, and S. Kim, “Cusadi: A gpu parallelization framework for symbolic expressions and optimal control,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 2, pp. 899–906, 2024. 

- [21] A. L. Bishop, J. Z. Zhang, S. Gurumurthy, K. Tracy, and Z. Manchester, “Relu-qp: A gpu-accelerated quadratic programming solver for model-predictive control,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 13285–13292, IEEE, 2024. 

- [22] W. Cai, K. G. Vamvoudakis, S. Gros, and A. Tzes, “Cost-Matching Model Predictive Control for Efficient Reinforcement Learning in Humanoid Locomotion,” _arXiv preprint arXiv:2603.28243_ , 2026. 

- [23] L. Wu, B. Yang, J. Li, X. Yang, Y. Mo, Y. Shi, A. D. Ames, and J. Drgoˇna, “ _π_ MPC: A Parallel-in-horizon and Construction-free NMPC Solver,” _arXiv preprint arXiv:2601.14414v2_ , 2026. 

- [24] D. E. Orin, A. Goswami, and S.-H. Lee, “Centroidal dynamics of a humanoid robot,” _Autonomous robots_ , vol. 35, no. 2, pp. 161–176, 2013. 

- [25] S. Caron, Q.-C. Pham, and Y. Nakamura, “Stability of surface contacts for humanoid robots: Closed-form formulae of the contact wrench cone for rectangular support areas,” in _2015 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 5107–5112, IEEE, 2015. 

- [26] J. Li, Z. Duan, J. Ma, and Q. Nguyen, “Gait-Net-augmented Implicit Kino-dynamic MPC for Dynamic Variable-frequency Humanoid Locomotion over Discrete Terrains,” in _Proceedings of Robotics: Science and Systems_ , (LosAngeles, CA, USA), June 2025. 

- [27] T. Goldstein, B. O’Donoghue, S. Setzer, and R. Baraniuk, “Fast alternating direction optimization methods,” _SIAM Journal on Imaging Sciences_ , vol. 7, no. 3, pp. 1588–1623, 2014. 

- [28] K. Zakka, Q. Liao, B. Yi, L. L. Lay, K. Sreenath, and P. Abbeel, “mjlab: A Lightweight Framework for GPU-Accelerated Robot Learning,” _arXiv preprint arXiv:2601.22074_ , 2026. 

- [29] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [30] J. Arrizabalaga, K. Tracy, and Z. Manchester, “A Differentiable Interior-Point Method in Single Precision,” _arXiv preprint arXiv:2605.17913_ , 2026. 

- [31] B. Amos and J. Z. Kolter, “OptNet: Differentiable Optimization as a Layer in Neural Networks,” _arXiv preprint arXiv:1703.00443_ , 2017. 

- [32] S. Boyd, N. Parikh, E. Chu, B. Peleato, and J. Eckstein, “Distributed Optimization and Statistical Learning via the Alternating Direction Method of Multipliers,” _Foundations and Trends in Machine Learning_ , vol. 3, no. 1, pp. 1–122, 2011. 

- [33] B. Stellato, G. Banjac, P. Goulart, A. Bemporad, and S. Boyd, “OSQP: An operator splitting solver for quadratic programs,” in _2018 UKACC 12th international conference on control (CONTROL)_ , pp. 339–339, IEEE, 2018. 

- [34] K. Li, Z. Olkin, Y. Yue, and A. D. Ames, “Clf-rl: Control lyapunov function guided reinforcement learning,” _IEEE Robotics and Automation Letters_ , 2026. 

## APPENDIX 

TABLE IV: Comparison of inertia-based gain selection for THEMIS v2. Here _kg_ is the gear ratio, _I_ rotor = _Ai/kg_<sup>2is the</sup> rotor inertia, and _ωn_ = 2 _πfn_ . 

|Joint|Method|_kg_|_I_rotor<br>(kg m<sup>2</sup>)|_Ai_<br>(kg m<sup>2</sup>)|_J_eff<br>(kg m<sup>2</sup>)|_fn_<br>(Hz)|_ζ_|_Kp/Kd_|
|---|---|---|---|---|---|---|---|---|
|Ab/Ad|[29]<br>Ours|9_._00|9_._15_×_10<sup>_−_4</sup>|0_._074|0_._074<br>0_._46|10_._0 <br>1_._4|2_._0 <br>0_._6|292_._5_/_18_._6<br>35_._6_/_4_._8|
|Hip|[29]<br>Ours|7_._78|1_._90_×_10<sup>_−_3</sup>|0_._1153|0_._115<br>0_._45|10_._0 <br>1_._4|2_._0 <br>0_._9|455_._2_/_29_._0<br>34_._8_/_7_._1|
|Knee|[29]<br>Ours|7_._78|1_._90_×_10<sup>_−_3</sup>|0_._1153|0_._115<br>0_._25|10_._0 <br>1_._9|2_._0 <br>1_._2|455_._2_/_29_._0<br>35_._6_/_7_._2|


