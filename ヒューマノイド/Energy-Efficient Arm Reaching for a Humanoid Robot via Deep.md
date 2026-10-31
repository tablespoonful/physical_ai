---
title: "Energy-Efficient Arm Reaching for a Humanoid Robot via Deep Reinforcement Learning with Identified Power Models"
date: "2026-06-14"
authors: "Nestor N. Deniz; Simon Parsons; Fernando Auat Cheein"
url: https://arxiv.org/abs/2606.15918
pdf: https://arxiv.org/pdf/2606.15918
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.15918)** / [論文ページ](https://arxiv.org/abs/2606.15918)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Energy-Efficient Arm Reaching for a Humanoid Robot via Deep Reinforcement Learning with Identified Power Models 

Nestor N. Deniz<sup>1</sup> , Simon Parsons<sup>2</sup> and Fernando A. Auat Cheein<sup>1</sup> 

**_Abstract_ —Humanoid robots performing in-field manipulation tasks, such as robotic apple harvesting, face severe energy constraints that directly limit the number of reaching motions that can be executed per battery charge. This paper presents an endto-end, energy-aware reinforcement learning framework for the 7-degree-of-freedom left arm of the Unitree G1 humanoid robot, combining a physics-based, experimentally identified electrical power model with a Soft Actor-Critic (SAC) policy trained in a Pinocchio-based rigid-body dynamics simulator. The RL policy operates on an incremental joint-position action space and is trained with a Hybrid Constellation Reward that combines a four-point end-effector constellation distance with a torque-norm energy proxy; after training it reaches a** 69 _._ 9% **success rate over** 1 000 **random targets in kinematic simulation, at a mean energy of** 98 _._ 16 J **on successful episodes. Finally, on the physical Unitree G1, the policy is validated over three independent 10target batches, achieving a mean energy of** 71 _._ 5 _±_ 48 _._ 3 **J, an endeffector position error of** 2 _._ 64 _±_ 1 _._ 04 **cm, and an orientation error of** 6 _._ 92 _±_ 1 _._ 33<sup>_◦_</sup> **—within the** 4 cm **/** 8 _._ 6<sup>_◦_</sup> **training tolerance. These results constitute a first step toward energy-aware reinforcementlearning-based arm reaching for humanoid robots.** 

**_Index Terms_ —reinforcement learning, energy-efficient motion planning, humanoid robots, soft actor-critic, power model identification, Pinocchio, sim-to-real transfer, agricultural robotics, apple harvesting, MuJoCo** 

## I. INTRODUCTION 

**H** UMANOIDployment in field environments—inspection, agriculture,robots are increasingly considered for dedisaster response—where operation time is dictated by a fixed battery capacity [1]–[3]. A particularly demanding instance of this class of tasks is robotic fruit harvesting: an autonomous apple-picking humanoid must repeatedly reach toward, align with, and grasp fruit distributed throughout a tree canopy, executing hundreds of arm-reaching motions per working session on a single battery charge. Unlike wheeled platforms, whose locomotion cost is relatively predictable, the arm joints of a humanoid can account for a highly variable fraction of total power depending on task speed, payload, and trajectory shape, and this variability is compounded over the large number of repetitive reaches required for harvesting. Reducing arm energy consumption per reach is therefore critical for extending the productive working time of a humanoid harvesting platform. 

Classical motion-planning methods minimise a surrogate for energy, such as joint torques [4] or joint velocities, but they 

require an explicit, accurate dynamics model and solve an optimisation problem online, incurring substantial computational overhead. Model Predictive Control (MPC) can incorporate energy objectives within a receding-horizon framework [5], [6], yet the quality of MPC solutions is bounded by the fidelity of its internal model, and real-time re-optimisation at control rates of 100 Hz demands dedicated solvers and often constrains the problem horizon to only a few steps. 

Deep Reinforcement Learning (RL) offers a complementary paradigm: the policy is trained offline in simulation and executes online as a fixed feedforward network, adding negligible computation at inference time. Recent work has demonstrated RL policies for dexterous manipulation [7], [8], whole-body locomotion [9], [10], and energy-aware quadruped gaits [11], but energy-efficient reaching for a physical humanoid arm— where an experimentally identified power model is embedded directly into the RL reward, and where the resulting policy is validated end-to-end from kinematic simulation through dynamics-level simulation to physical hardware—has received little attention, particularly in the context of agricultural manipulation. 

This paper makes the following contributions: 

- 1) An experimentally identified electrical power model for the 7-DOF Unitree G1 left arm, used both as an evaluation metric and as an energy proxy inside a Gymnasium RL environment (Section II). 

- 2) A Soft Actor-Critic (SAC) [12] policy, combining an incremental joint-position action space with a Hybrid Constellation Reward, that achieves a 69 _._ 9% success rate over 1 000 random targets in kinematic simulation (Section III). 

- 3) A dynamics-level sim-to-real validation in MuJoCo— including a frozen-policy PD-gain sweep of the lowlevel controller and a workspace-reachability analysis— that quantifies and explains the gap between kinematic training performance and physically realisable performance (Sections IV and V). 

- 4) A real-hardware validation campaign on the physical Unitree G1 (30 independent reaching trials across three batches), reporting the end-effector position and orientation error achieved on every trial and showing that the learned policy transfers to a restricted but representative apple-picking task envelope (Section V). 

> 1Nestor N. Deniz, Sebastian Vega and Fernando Auat Cheein are with the Engineering Department at Harper Adams University, Newport, Shropshire TF10 8NB, UK. ndeniz@harper-adams.ac.uk 

> 2Simon Parsons is with Lincoln Institute for Agri-Food Technology and Lincoln Centre for Autonomous Systems. 

## II. ROBOT PLATFORM AND POWER MODEL 

## _A. Unitree G1 Left Arm_ 

The Unitree G1 is a full-size humanoid robot weighing approximately 35 kg. Its left arm consists of seven revolute 

2 

TABLE I: Left-arm joint limits and maximum velocity 

|Joint|Index|Lower (rad)|Upper (rad)|˙_q_max (rad/s)|
|---|---|---|---|---|
|Shoulder pitch|0|_−_3_._089|2_._670|2.5|
|Shoulder roll|1|_−_1_._588|2_._252|2.5|
|Shoulder yaw|2|_−_2_._618|2_._618|2.5|
|Elbow|3|_−_1_._047|2_._094|2.5|
|Wrist roll|4|_−_1_._972|1_._972|2.5|
|Wrist pitch|5|_−_1_._614|1_._614|2.5|
|Wrist yaw|6|_−_1_._614|1_._614|2.5|


joints: shoulder pitch ( _q_ 0), shoulder roll ( _q_ 1), shoulder yaw ( _q_ 2), elbow ( _q_ 3), wrist roll ( _q_ 4), wrist pitch ( _q_ 5), and wrist yaw ( _q_ 6). Joint angles, velocities, and motor currents are broadcast via the Unitree DDS middleware at 500 Hz; mainboard power is reported by an onboard sensor at 1 Hz. Joint limits, expressed in radians, are listed in Table I. 

TABLE II: Identified power model parameters for all 7 leftarm joints ( _R_<sup>2</sup> = 0 _._ 933, RMSE = 1 _._ 07 W, hold-out _R_<sup>2</sup> = 0 _._ 965 [13]). Shoulder/elbow joints: copper loss ( _bi_ ) dominant. Wrist joints: viscous friction ( _di_ ) dominant. 

|Joint||_i_|_ai_|_bi_|_ci_|_di_|
|---|---|---|---|---|---|---|
|Shoulder|pitch|0|1.0|0.4184|0.0000|0.6467|
|Shoulder|roll|1|1.0|0.3563|1.2767|0.0000|
|Shoulder|yaw|2|1.0|0.2799|0.0000|0.2749|
|Elbow||3|1.0|0.3942|0.0324|0.0000|
|Wrist rol|l|4|1.0|0.0000|0.0000|1.0282|
|Wrist pit|ch|5|1.0|0.3768|0.3464|1.2004|
|Wrist ya|w|6|1.0|0.0000|0.0000|1.7848|
|Units: _bi_ in|W m<sup>2</sup>_/_|N<sup>2</sup>,|_ci_ in|W s_/_ra|d, _di_ in|W s<sup>2</sup>_/_rad<sup>2</sup>.|
||Pair (_i_|_, j_)|_eij_|Pai|r (_i, j_)||
||(0_,_3)<br>||0.90|9<br>(1_,_6<br>|): 0.511<br>||
||(1_,_3)<br>||1.10|5<br>(2_,_6<br>|): 0.861<br>||
||(0_,_6)||0.43|7<br>(2_,_3|): 0.405||
||All oth|er _e_|_ij <_|0_._12 (se|e [13]).||


## _B. Physics-Based Power Model_ 

We model the net electrical power of the arm as a sum of per-joint terms and pairwise joint-speed interaction terms [13]: 


where _n_ = 7, **_τ_** _∈_ R<sup>7</sup> is the joint torque vector, **_q_** ˙ _∈_ R<sup>7</sup> is the joint velocity vector, and 


is the change in copper loss relative to the static baseline torque _τ_ 0 _,i_ required to hold the arm at the neutral configuration ( **_q_** = **0** ). 

The four per-joint terms model, respectively: 

- _Mechanical power_ ( _aiτi_ ˙ _qi_ ): net work done by joint _i_ , scaled by the reciprocal of gear efficiency. 

- _Copper losses_ ( _bi_ ∆ _τi_<sup>2):resistiveheatinginthemotor</sup> windings, proportional to the change in squared torque relative to the baseline. 

- _Coulomb friction_ ( _ci|_ ˙ _qi|_ ): constant friction dissipation, direction-independent and velocity-sign dependent in magnitude. 

- _Viscous friction_ ( _di_ ˙ _qi_<sup>2):velocity-dependentfriction.</sup> 

The _eij_ terms capture electromagnetic and mechanical coupling between simultaneously moving joints, which is not accounted for by the single-joint model alone. The identified parameter values for all joints are listed in Table II. For more details, the reader is referred to [13]. 

## III. REINFORCEMENT LEARNING FORMULATION 

## _A. Markov Decision Process_ 

We model the arm reaching task as a discrete-time Markov Decision Process (MDP) _M_ = ( _S, A, T , r, γ_ ), with a fixed time step ∆ _t_ = 0 _._ 01 s and episode length _T_ = 300 steps (3 _._ 0 s). 

_State Space:_ The state **_s_** _t ∈_ R<sup>21</sup> is 


where: 

_•_ **_q_** ˜ _t ∈_ [ _−_ 1 _,_ 1]<sup>7</sup> are joint angles normalised by their range: _q_ ˜ _i_ = 2( _qi − q_ ¯ _i_ ) _/_ ∆ _qi_ , with _q_ ¯ _i_ = ( _qi_<sup>max</sup> + _qi_<sup>min</sup> ) _/_ 2 and ∆ _qi_ = _qi_<sup>max</sup> _− qi_<sup>min</sup> . _•_ **_q_**<sup>˜</sup> ˙ _t_ = **_q_** ˙ _t/_ ˙ _q_ max _∈_ R<sup>7</sup> . 

- **_e_**<sup>_t_</sup> _p_<sup>=</sup><sup>**_p_**</sup><sup>_∗−_</sup><sup>**_p_**</sup><sup>_t∈_R3istheCartesianpositionerrorof</sup> the end-effector (m), and **_e_** ˆ<sup>_t_</sup> _p_<sup>=</sup><sup>**_e_**</sup><sup>_t_</sup> _p_<sup>_/d_normwith</sup><sup>_d_norm=</sup> 0 _._ 5 m. 

- **_e_**<sup>_t_</sup> _o_<sup>_∈_so(3) is the orientation error expressed as a rotation</sup> vector (axis _×_ angle): 


where **_R_**<sup>_∗_</sup> and **_R_** _t ∈_ SO(3) are the target and current endeffector rotation matrices, respectively, and **_e_** ˆ<sup>_t_</sup> _o_<sup>=</sup><sup>**_e_**</sup><sup>_t_</sup> _o_<sup>_/π_.</sup> _• t_ rem = 1 _− k/T ∈_ [0 _,_ 1] is the fraction of time remaining in the episode. 

End-effector pose ( **_p_** _t,_ **_R_** _t_ ) is obtained from forward kinematics. 

_Action Space: Incremental Joint-Position Targets:_ We use an _incremental joint-position_ action space, in which the action **_a_** _t ∈_ [ _−_ 1 _,_ 1]<sup>7</sup> specifies a displacement of a position target that is then tracked by a proportional joint controller: 


where ∆ _q_ max = _q_ ˙max _/kp ≈_ 0 _._ 1667 rad is the maximum per-step position increment, _kp_ = 15 _._ 0 is the position gain, and _kd_ = 0. Bounding the position increment by _q_ ˙max _/kp_ guarantees that the desired velocity (6) cannot exceed the joint speed limit even before clipping in (7), which removes the persistent saturation observed with direct velocity actions. 

3 

_Transition Dynamics:_ Joint positions are integrated with the Euler scheme subject to joint limits: 


and the realised velocity is **_q_** ˙ _t_ +1 = ( **_q_** _t_ +1 _−_ **_q_** _t_ ) _/_ ∆ _t_ . Joint torques are computed via the Recursive Newton-Euler Algorithm (RNEA) [14] as implemented in Pinocchio [15], evaluated at the _pre_ -update state ( **_q_** _t,_ **_q_** ˙ _t_ ) with the realised acceleration: 


A reduced 7-DOF Pinocchio model is built from the full 29DOF URDF by locking all non-arm joints at their neutral configuration, so RNEA runs at the arm level without the computational cost of the full-body model. 

## _B. Hybrid Constellation Reward_ 

We define a _constellation distance_ that combines position and orientation error into a single geometric quantity by tracking a small set of virtual points rigidly attached to the end-effector frame. 

_Constellation Distance:_ Let _Nc_ = 4 constellation points be placed at angles _θk_ = 2 _πk/Nc_ , _k_ = 0 _, . . . , Nc −_ 1, on a circle of radius _rc_ = 0 _._ 12 m in the end-effector’s local _xy_ -plane: 


At step _t_ , the current and target positions of constellation point _k_ are 


and the constellation distance is their mean squared separation, 


Because the constellation points are offset from the endeffector origin, _d_<sup>_t_</sup> con<sup>issensitiveto</sup><sup>_both_thetranslationalerror</sup> **_e_**<sup>_t_</sup> _p_<sup>and the rotational misalignment between</sup><sup>**_R_**</sup><sup>_t_and</sup><sup>**_R_**</sup><sup>_∗_: a pure</sup> rotation about **_p_** _t_ with **_p_** _t_ = **_p_**<sup>_∗_</sup> still displaces the constellation points and increases _d_<sup>_t_</sup> con<sup>.Asingleexponentialorquadratic</sup> term in _d_<sup>_t_</sup> con<sup>thereforeshapesposition</sup><sup>_and_orientationjointly,</sup> without separately tuned weights for each. 

_Reward:_ The reward at step _t_ is the sum of six terms, 


where success ≜ ��� **_e_** _tp_ �� _< dp_ � _∧_ ( _∥_ **_e_**<sup>_t_</sup> _o_<sup>_∥< do_)terminatesthe</sup> episode. Term by term: 

- (14): _progress shaping_ —a dense reward proportional to the reduction in constellation distance since the previous step, weight _δ_ con = 5 _._ 0. 

- (15): _residual position penalty_ —a small linear penalty = 

- on the remaining Cartesian distance, weight _β_ res 0 _._ 1, which breaks ties between trajectories with similar progress but different absolute distance to the target. 

- (16): _exponential constellation reward_ —a bounded, strictly positive term in (0 _,_ 1] that grows sharply as _d_<sup>_t_</sup> con<sup>_→_0,withsharpness</sup><sup>_w_con= 40</sup><sup>_._0.Unlike(14),this</sup> term rewards _proximity_ regardless of the path taken to get there, preventing the agent from exploiting the progress term through oscillatory motion. 

- (17): a constant per-step cost _c_ step = 0 _._ 001 that encourages the agent to terminate (reach the goal) as early as possible. 

- (18): a _velocity-smoothness_ penalty (active for _t >_ 0), weight _λ_ smooth = 0 _._ 005, discouraging abrupt changes in realised velocity between consecutive steps. 

- (19): a _torque-norm energy proxy_ , weight _λτ_ = 5 _×_ 10<sup>_−_5</sup> (see Remark 1). 

- (20): a sparse terminal bonus _R_ success = 700 _._ 0, awarded when the end-effector is simultaneously within _dp_ = 4 cm position and _do_ = 0 _._ 15 rad _≈_ 8 _._ 6<sup>_◦_</sup> orientation tolerance of the target. 

_Remark 1 (Energy term: reward proxy vs. evaluation metric):_ The full electrical power model _P_ net( **_τ_** _t,_ **_q_** ˙ _t_ ) (1) is evaluated and logged at every training step, but it does _not_ appear in the reward: the corresponding weight _α_ is set to 0. The only energy-related term that shapes the policy during training is the torque-norm proxy (19), _λτ ∥_ **_τ_** _t∥_<sup>2</sup> , which is cheap to compute, smooth in **_τ_** _t_ , and penalises the large inertial torques produced by abrupt accelerations without requiring the full nonlinear power model inside the training loop. The physically grounded power model (1) is instead applied _post hoc_ to the realised ( **_τ_** _t,_ **_q_** ˙ _t_ ) trajectory of every evaluation episode—in kinematic simulation, in MuJoCo, and on the physical robot—and is the metric reported throughout Section V. This separation keeps the reward landscape smooth and inexpensive during the training run while preserving the experimentally calibrated power model as the common basis for all energy comparisons. 

## _C. Soft Actor-Critic_ 


where _H_ is the policy entropy and _α_ ent is an automatically tuned temperature parameter [16]. The entropy bonus plays a critical role here: because the success region defined by ( _dp, do_ ) in (20) is a small volume in joint space, the agent must maintain broad exploration even near the goal to discover terminal states that satisfy both the position and orientation 

4 

**Algorithm 1** SAC training step with incremental positiontarget action and RNEA-based torque evaluation 

- 1: **Input:** policy _πθ_ ; critics _Qϕ_ 1 _, Qϕ_ 2 and targets _Qϕ_<sup>_′_</sup> 1<sup>_, Qϕ′_</sup> 2<sup>;</sup> replay buffer _D_ 

- 2: **for** environment step _t_ = 0 _,_ 1 _, . . ._ **do** 3: Observe state **_s_** _t_ (3) 4: Sample action **_a_** _t ∼ πθ_ ( _·|_ **_s_** _t_ ) 5: Compute position target **_q_** _t_<sup>tgt</sup> (5) 6: Compute commanded velocity **_q_** ˙ _t_<sup>cmd</sup> via (6)–(7) 7: Integrate **_q_** _t_ +1 (8); **_q_** ˙ _t_ +1 _←_ ( **_q_** _t_ +1 _−_ **_q_** _t_ ) _/_ ∆ _t_ 8: Evaluate **_τ_** _t ←_ RNEA( **_q_** _t,_ **_q_** ˙ _t,_ **_q_** ¨ _t_ ) (9) 9: Compute _d_<sup>_t_</sup> con<sup>(13)andreward</sup><sup>_rt_via(14)–(20)</sup> 

- 10: Log _P_ net( **_τ_** _t,_ **_q_** ˙ _t_ ) ∆ _t_ (1) (evaluation only, not part of _rt_ ) 11: Store ( **_s_** _t,_ **_a_** _t, rt,_ **_s_** _t_ +1 _,_ done) in _D_ 12: **if** _t ≥_ learning_starts **then** 13: **for** _g_ = 1 **to** gradient_steps **do** 14: Sample minibatch from _D_ 15: Update _Qϕ_ 1 _, Qϕ_ 2 by minimising the soft Bellman residual using _Qϕ_<sup>_′_</sup> 1<sup>_, Qϕ′_</sup> 2 

- 16: Update _πθ_ by maximising E[min _i Qϕi_ ( **_s_** _,_ **_a_** ) _− α_ ent log _πθ_ ( **_a_** _|_ **_s_** )] 

- 17: Update _α_ ent toward the target entropy 18: Soft-update targets: _ϕ_<sup>_′_</sup> _i_<sup>_←τ_soft</sup><sup>_ϕi_+ (1</sup><sup>_−τ_soft)</sup><sup>_ϕ′_</sup> _i_ 19: **end for** 20: **end if** 21: **end for** 

already normalised to approximately [ _−_ 1 _,_ 1] by construction (Section III-A). 

## _B. Target Sampling and Initial State_ 

At each episode reset, a target pose ( **_p_**<sup>_∗_</sup> _,_ **_R_**<sup>_∗_</sup> ) is sampled by drawing a random joint configuration **_q_**<sup>_∗_</sup> _∼U_ ( **_q_**<sup>min</sup> _,_ **_q_**<sup>max</sup> ) and computing its forward kinematics; the sample is rejected and redrawn if _∥_ **_p_**<sup>_∗_</sup> _∥≤_ 0 _._ 15 m, which excludes degenerate target poses close to the shoulder. No further bias toward any workspace region is applied: **_q_**<sup>_∗_</sup> is accepted as soon as the distance check passes. 

The initial joint configuration is drawn from a band around the neutral pose, 


with **_q_** _c_ = ( **_q_**<sup>max</sup> + **_q_**<sup>min</sup> ) _/_ 2 and ∆ **_q_** = **_q_**<sup>max</sup> _−_ **_q_**<sup>min</sup> , and **_q_** ˙0 = **0** . 

## _C. Training Lineage and Protocol_ 

The agent is trained for a total of 5 _×_ 10<sup>6</sup> environment steps. An EvalCallback evaluates the deterministic policy on held-out episodes periodically and saves the checkpoint achieving the highest mean reward; a CheckpointCallback additionally saves snapshots every 10<sup>5</sup> steps. Each fresh run discards the replay buffer to avoid distributional shift when the MDP or reward changes. 

TABLE III: SAC hyperparameters 

|Hyperparameter|Value|
|---|---|
|Learning rate|3_×_10<sup>_−_4</sup>|
|Discount factor _γ_|0.99|
|Soft update _τ_soft|0.005<br>|
|Replay buffer size|5_×_10<sup>5</sup>|
|Batch size|256|
|Learning starts|25 000|
|Train frequency|1 step|
|Gradient steps per update|4|
|Temperature _α_ent|auto<br>|
|Network architecture (policy & critics)|[256_,_256]|


tolerances simultaneously, rather than committing prematurely to a suboptimal approach direction. 

The policy and both critics are multi-layer perceptrons (MLPs) with architecture [256 _,_ 256]. Algorithm 1 summarises one environment step of the training loop, combining the incremental action-to-torque mapping of Section III-A with the standard SAC update. Table III lists all hyperparameters. 

## _D. Baseline: Minimum-Jerk Trajectory_ 

As a reference for simulation evaluation, we use a jointspace minimum-jerk trajectory [18]: a 5th-order polynomial applied directly between the initial joint configuration and the sampled target configuration **_q_**<sup>_∗_</sup> (see Appendix A). No inverse kinematics is needed because the target is defined in joint space via forward kinematics sampling, so the same target is available to both the RL policy (as a Cartesian pose) and the min-jerk planner (as a joint configuration). The trajectory duration is set to satisfy the velocity limit _q_ ˙max = 2 _._ 5 rad _/_ s for the largest joint displacement, giving a planned duration of 1 _._ 519 _±_ 0 _._ 342 s (Appendix A)—well within the 3 _._ 0 s RL episode budget. The realised episode duration (Table V) is shorter on average (1 _._ 276 _±_ 0 _._ 357 s) because episodes terminate as soon as the success tolerance is reached, before the planned trajectory completes. The min-jerk baseline is energy-unaware; energy consumption is computed after the fact by passing the resulting trajectory through the same RNEA and identified power model used to evaluate the RL policy. 

## IV. TRAINING SETUP 

## _A. Simulation Environment_ 

Training runs entirely in the kinematic Pinocchio environment of Section III-A. Environments are instantiated with the Stable-Baselines3 [17] SubprocVecEnv wrapper using _N_ env = 8 parallel processes, yielding an effective wall-clock throughput of approximately 1 000–1 700 steps per second on a desktop GPU (NVIDIA RTX series). A VecNormalize layer is intentionally omitted because the observation terms are 

## _E. MuJoCo Dynamics Validation_ 

The kinematic environment of Section III-A assumes a _perfect tracker_ : the commanded velocity **_q_** ˙ _t_<sup>cmd</sup> is realised exactly within one step (8). Before any hardware trial, we therefore validate the frozen 69 _._ 9% policy (no further training) in MuJoCo [19] using the full Unitree G1 MJCF model (29 DOF, floating base). At every ∆ _t_ = 10 ms RL step, the simulator advances 5 physics substeps of 2 ms; the floating 

5 

TABLE IV: MuJoCo frozen-policy PD-gain sweep ( _n_ = 100 unless noted). “Sat.” is the fraction of action-clipped steps; “ori. err.” is the mean final orientation error. 


Fig. 2: Validation arc summary. (a) Success rate in simulation: the kinematic-simulation rate (69 _._ 9%, _n_ =1000) drops to 46% under MuJoCo dynamics over the full nominal workspace ( _n_ =200, Section IV-E), and recovers to 95% ( _n_ =20) once evaluation is restricted to the reachable apple-picking task envelope (Section V-B). (b) On the physical Unitree G1 ( _n_ =30, same task envelope), we report the achieved endeffector position error directly: every trial lands below the 4 cm tolerance (dashed line), with mean 2 _._ 64 _±_ 1 _._ 04 cm and worst case 3 _._ 94 cm. 


Fig. 1: Frozen-policy MuJoCo validation across the PD-gain sweep. (a) Success rate vs. _kp_<sup>mj:thekinematic-environment</sup> rate (dashed) is gain-independent by construction, while the MuJoCo dynamics rate is consistently 20–25 percentage points lower. (b) Actuator saturation and mean episode energy both grow sharply with _kp_<sup>mj.</sup> 

controller introduces a residual tracking lag that the policy never experienced. Second, actuator saturation and energy consumption are highly sensitive to _kp_<sup>mj,growingroughly8</sup><sup>_×_</sup> from _kp_<sup>mj</sup> = 30 to 400. We therefore deploy with a soft PD configuration ( _kp_<sup>mj</sup> = 50, _kd_<sup>mj</sup> = 1 _._ 5) together with the torque safety clamp above, which keeps saturation and energy near the lower end of the sweep without sacrificing the success rate achievable at higher gains. The remaining _∼_ 20-point gap is addressed in Section V-B through a workspace-reachability analysis that identifies _where_ in the workspace this gap is concentrated. 

base and the 36 non-arm joints are teleport-locked to their default configuration **_q_** 0<sup>mj</sup> after every substep, isolating the 7-DOF left arm under realistic actuator dynamics without requiring a balance controller. At each RL step the policy’s position target (5) and commanded velocity (7) are passed to a low-level PD torque controller, 

## V. EXPERIMENTAL RESULTS 


The RL formulation of Section III and the training/validation pipeline of Section IV are evaluated along a four-stage arc, summarised in Fig. 2: (i) kinematic-simulation evaluation of the frozen 69 _._ 9% policy at _n_ = 1 000 (Section V-A); (ii) a workspace-reachability analysis that identifies a restricted task envelope in which the policy can be expected to transfer, together with an _n_ = 20 MuJoCo screening on that envelope (Section V-B); and (iii) real-hardware validation on the physical Unitree G1 over _n_ = 30 independent trials (Section V-C). The MuJoCo dynamics-validation methodology and the PD-gain sweep that motivate stages (ii)–(iii) were already presented in Section IV-E. For the first three, simulationbased stages, a binary success rate over a fixed tolerance is a meaningful summary statistic because _n_ is large (1 000, 200, and 20, respectively); for the real-robot stage, _n_ = 30 is too small for a binary rate to be statistically informative, so we instead report the full distribution of end-effector position errors achieved. 

clipped to the MJCF actuator ctrlrange ( _±_ 25 N m for shoulder/elbow/wrist-roll, _±_ 5 N m for wrist-pitch/yaw)— tighter than the RNEA-evaluation torque limits used in Section III. _PD-Gain Sweep:_ Because _kp_<sup>mj</sup> and _kd_<sup>mj</sup> are deployment choices not seen during training, we sweep _kp_<sup>mj</sup> _∈ {_ 30 _,_ 50 _,_ 100 _,_ 400 _}_ (with _kd_<sup>mj</sup> = _kp_<sup>mj</sup><sup>_/_20)over</sup><sup>_n_= 100targets</sup> and report the kinematic-environment success rate on the same targets as a reference. Table IV and Fig. 1 summarise the results; an additional _n_ = 200 run at _kp_<sup>mj</sup> = 400 confirms the trend at larger sample size. 

Two findings drive the deployment choices used in Section V. First, the success-rate gap between the kinematic environment and MuJoCo is 20–25 percentage points across _all_ tested gains—i.e., it is largely _gain-independent_ —and the mean final orientation error is consistently 11–13<sup>_◦_</sup> , roughly 3–5<sup>_◦_</sup> above the 8 _._ 6<sup>_◦_</sup> training tolerance, regardless of _kp_<sup>mj.</sup> This indicates that the gap is not primarily a controller-tuning problem but an intrinsic consequence of the perfect-tracker assumption in Section III-A: the policy was trained assuming instantaneous, exact velocity tracking, and any finite-gain PD 

## _A. Kinematic Simulation Evaluation (n_ = 1 000 _)_ 

The frozen reference policy (Section IV-C) is evaluated deterministically over _n_ = 1 000 targets sampled as in Section IV-B, against the minimum-jerk baseline of Section IV-D 

6 

TABLE V: Kinematic-simulation evaluation, _n_ = 1 000 targets, deterministic policy (checkpoint at 5 _×_ 10<sup>6</sup> steps). Tolerances: _dp_ = 4 cm, _do_ = 8 _._ 6<sup>_◦_</sup> . 

|Metric|RL (SAC)|Min-jerk|
|---|---|---|
|Success rate (%)|69_._9|100_._0|
|Energy, all episodes (J)|163_._7_±_838_._3|22_._0_±_9_._6|
|Energy, successes only (J)|98_._16 (_n_=699)|21_._95 (_n_=1000)|
|Episode duration (s)|1_._542_±_1_._049|1_._276_±_0_._357|
|Final pos. error, all (cm)|6_._08_±_7_._32|2_._50_±_0_._96|
|Final ori. error, all (<sup>_◦_</sup>)<br>|16_._49_±_24_._47<br>|7_._88_±_0_._93<br>|
|Smoothness MSJ (rad<sup>2 </sup>s<sup>_−_6</sup>)|1_._31_×_10<sup>7</sup>|2_._00_×_10<sup>2</sup>|
|Action saturation (% steps)|24_._6|12_._1|


on the same targets. Table V reports overall metrics; Table VI reports the per-joint kinematic/torque statistics and the breakdown of the post-hoc energy model (1) for the RL policy. 

_Remark 2:_ The minimum-jerk baseline succeeds on 100% of episodes (Table V), with final errors clustered just inside the tolerance band (2 _._ 50 _±_ 0 _._ 96 cm, 7 _._ 88 _±_ 0 _._ 93<sup>_◦_</sup> vs. _dp_ = 4 cm/ _do_ = 8 _._ 6<sup>_◦_</sup> ). Because the closed-form trajectory (24) approaches **_q_**<sup>_∗_</sup> monotonically with vanishing velocity and acceleration at _ξ_ = 1, the success criterion is met at _ξ <_ 1 on average, so episodes terminate early (mean 1 _._ 276 _±_ 0 _._ 357 s vs. the planned 1 _._ 519 _±_ 0 _._ 342 s, Appendix A). Note that the planner is constructed with full knowledge of **_q_**<sup>_∗_</sup> —effectively a privileged inverse-kinematics solution unavailable to the RL policy, which observes only the Cartesian target pose—so Table V should be read as a smooth, energy-efficient _oracle_ reference rather than a directly comparable control strategy. 

On the RL policy, the energy breakdown in Table VI mirrors the pattern of the power model itself (Table II): copper losses dominate (87 _._ 6%), consistent with the large peak torques (up to 199 N m on the shoulder pitch joint) generated by RNEA (9) during the fast, large-amplitude motions that the kinematic environment’s perfect-tracker assumption permits. Action saturation occurs on 24 _._ 6% of steps, concentrated on the shoulder joints (up to 7 _._ 7% per joint), reflecting the incremental action space’s displacement ceiling (5) being reached during the most aggressive phases of a reach. 

## _B. Workspace Reachability and Restricted Task Envelope_ 

Section IV-E showed that the kinematic-to-MuJoCo success gap is approximately 20–25 percentage points and largely gain-independent. To determine how much of this gap is explained by targets that are simply not reachable by the arm— independent of any controller—we sample _n_ = 80 random points inside the nominal apple-picking workspace bounding box and solve unregularised position inverse kinematics (IK, 30 random restarts) for each. Table VII (top) summarises the result: only 24 _/_ 80 (30%) of points are reachable within 2 cm; the remaining points miss by a median of _∼_ 10 cm (90th percentile _∼_ 31 cm, max _∼_ 41 cm), regardless of the IK initialisation or controller—no feedback law can close a 10+ cm kinematic gap. A second, qualitatively distinct failure mode occurs for targets close to the torso ( _x <_ 0 _._ 1 m in the robot’s forward direction): the arm can become physically stuck in a history-dependent configuration up to _∼_ 54<sup>_◦_</sup> from 

the commanded target, a mode not present in the kinematic training environment. 

Restricting evaluation to the subset of the apple-picking workspace that is (a) at least 0 _._ 1 m from the torso along _x_ and (b) IK-reachable within 2 cm—i.e., the _task envelope_ that a real apple-picking deployment would target—and rerunning the frozen policy in MuJoCo with the deployment PD gains ( _kp_<sup>mj</sup> = 50, _kd_<sup>mj</sup> = 1 _._ 5) over _n_ = 20 targets recovers a 95% success rate (Table VII, bottom), with median final errors of 3 _._ 0 cm/7 _._ 0<sup>_◦_</sup> , both within tolerance, and mean motor excitation in [0 _._ 05 _,_ 0 _._ 26]—a substantially tighter, lowereffort regime than the full-workspace sweep of Table IV. The single failure ( _x_ = 0 _._ 105 m, near the lower edge of the envelope) timed out at 6 _._ 1 cm/11 _._ 8<sup>_◦_</sup> , just outside tolerance. This restricted task envelope is the target distribution used for the real-hardware validation in Section V-C. 

## _C. Real-Robot Hardware Validation (n_ = 30 _)_ 

_1) Deployment:_ The frozen policy is deployed on the physical Unitree G1 via a Python node that reads joint state from a ROS2 topic at 100 Hz, assembles the 21-dimensional observation **_s_** _t_ (3), passes it through the frozen network (forward pass _<_ 1 ms on CPU), and publishes the resulting position target and commanded velocity (5)–(7) to the lowlevel joint controller via a ROS2 topic, using the deployment PD gains identified in Section IV-E ( _kp_<sup>mj</sup> = 50, _kd_<sup>mj</sup> = 1 _._ 5) and the same torque safety clamp. No additional sim-to-real adaptation (domain randomisation, friction identification, or fine-tuning) is applied. 

_2) Protocol:_ Targets are drawn from the restricted task envelope of Section V-B: for each trial, a Cartesian target ( **_p_**<sup>_∗_</sup> _,_ **_R_**<sup>_∗_</sup> ) is generated within the apple-picking bounding box with _x ≥_ 0 _._ 1 m, position IK is solved (residual reported as “IK residual” below), and—only if the residual is below 2 cm—the trial proceeds; otherwise the target is re-sampled. This single check operationalises the reachability analysis of Section V-B for hardware use. Three independent batches of 10 targets each ( _n_ = 30 total) were executed. Given the small sample size, we report the achieved end-effector position and orientation error for every trial rather than a binary success rate: the position error is 2 _._ 64 _±_ 1 _._ 04 cm (worst case 3 _._ 94 cm) and the orientation error is 6 _._ 92 _±_ 1 _._ 33<sup>_◦_</sup> (worst case 8 _._ 58<sup>_◦_</sup> ), i.e., every one of the 30 trials lands within the 4 cm _/_ 8 _._ 6<sup>_◦_</sup> tolerance used during training, with a margin of at least 0 _._ 06 cm even in the worst-case trial (Fig. 2b, Fig. 3). Joint angles, velocities, and commanded torques are logged at 100 Hz and passed through the identified power model (1) to obtain the energy figures below, exactly as for the simulation evaluation of Section V-A. 

Across the _n_ = 30 hardware trials, energy consumption (mean 71 _._ 5 _±_ 48 _._ 3 J, median 54 _._ 9 J) is markedly lower than the kinematic-simulation mean for successful episodes (98 _._ 16 J, Table V), and its distribution is shifted toward lower values at every percentile (Fig. 5), reflecting the smaller realised torques (up to 20 _._ 9 N m, Table IX, vs. up to 199 N m in kinematic simulation, Table VI) imposed by the soft PD controller and torque clamp of Section IV-E. Correspondingly, the energy breakdown shifts away from copper-dominated: copper losses 

7 

TABLE VI: RL policy, _n_ = 1 000: per-joint kinematics/torques (mean over all episodes) and post-hoc energy breakdown (1) (mean over all episodes). 

|Join|t|_|_˙_q|_|mean (r|ad/s)<br>_|_˙_q|_ max|Satur|ation (%)|_|τ|_ mean (N|m)<br>_|τ|_ max (N m)|
|---|---|---|---|---|---|---|---|---|
|Sh.|pitch||1.17|2.50||7.7|4.62|199.46|
|Sh.|roll||0.93|2.50||4.1|4.23|159.31|
|Sh.|yaw||1.10|2.50||5.5|2.04|64.24|
|Elb|ow||0.94|2.50||2.6|2.62|99.94|
|Wr.|roll||1.09|2.50||5.1|0.59|27.75|
|Wr.|pitch||1.01|2.50||2.7|0.85|43.37|
|Wr.|yaw||1.03|2.50||3.9|0.66|22.10|
|||Energ|y term|Mechanical|Copper|Coulomb|Viscous|Interaction|
|||Mean|(J)|11.66|143.46|2.42|14.60|11.05|
|||Share|(%)|7.1|87.6|1.5|8.9|6.8|


TABLE VII: Workspace reachability ( _n_ = 80 random points in the apple-picking bounding box, position IK with 30 restarts) and MuJoCo screening on the restricted reachable task envelope ( _x ≥_ 0 _._ 1 m, IK residual _<_ 2 cm, _n_ = 20, default policy rollout, _kp_<sup>mj</sup> = 50, _kd_<sup>mj</sup> = 1 _._ 5). 

|_Workspace reachability (n_= 80_)_||
|---|---|
|Reachable within 2 cm|24_/_80 (30%)|
|Median miss (unreachable points)|_∼_10 cm|
|90th percentile miss|_∼_31 cm|
|Maximum miss|_∼_41 cm|
|_Restricted-envelope MuJoCo screen_|_ing (n_= 20_)_|
|Success rate|19_/_20 (95%)|
|Pos. error, median (range)|3_._0 (1_._3–6_._1) cm|
|Ori. error, median (range)|7_._0 (2_._3–11_._8)<sup>_◦_</sup>|
|Mean motor excitation, range|0_._05–0_._26|


TABLE VIII: Real-robot validation, _n_ = 30 (3 batches _×_ 10 targets); all trials land within the 4 cm _/_ 8 _._ 6<sup>_◦_</sup> tolerance (Fig. 2b). “Exc.” is the normalised joint excursion _|q − q_ ¯ _|/_ (∆ _q/_ 2). 

|Metric|Mean _±_ std|Median|Range|
|---|---|---|---|
|Pos. error (cm)|2_._64_±_1_._04|2_._77|[0_._70_,_3_._94]<br>|
|Ori. error (<sup>_◦_</sup>)|6_._92_±_1_._33|7_._16|[3_._79_,_8_._58]<br>|
|IK residual (cm)|0_._69_±_0_._45|0_._59|[0_._14_,_1_._49]<br>|
|Energy (J)|71_._5_±_48_._3|54_._9|[11_._6_,_165_._2]<br>|
|Duration (s)|0_._545_±_0_._381|0_._374|[0_._10_,_1_._31]<br>|
|Mean power (W)<br>|131_._5_±_18_._1|130_._7|[95_._0_,_162_._1]<br>|
|Mean _|_˙_q|_ (rad/s)<br>|1_._85_±_0_._27|1_._87|[1_._20_,_2_._47]|
|Max _|_˙_q|_ (rad/s)|6_._26_±_1_._27|6_._28|up to 8_._79|
|Mean _|τ|_ (N m)|3_._99_±_0_._41|4_._01|[2_._91_,_4_._94]|
|Max _|τ|_ (N m)|15_._2_±_3_._1|15_._7|up to 20_._9|
|Steps per episode|45_._2_±_30_._4|33|[8_,_105]|
|Mean excursion|0_._157_±_0_._068|0_._186|[0_._05_,_0_._24]|


fall from 87 _._ 6% (kinematic sim) to 46 _._ 1 _±_ 8 _._ 4% on hardware, with viscous friction (20 _._ 4 _±_ 4 _._ 3%) and mechanical work (17 _._ 5 _±_ 5 _._ 6%) accounting for a larger share. Final orientation error (mean 6 _._ 92 _±_ 1 _._ 33<sup>_◦_</sup> , Fig. 3) sits close to, but consistently within, the 8 _._ 6<sup>_◦_</sup> tolerance—the orientation channel is the tighter of the two success criteria on hardware, consistent with the MuJoCo finding (Section IV-E) that orientation tracking carries most of the residual sim-to-real error. 

## VI. DISCUSSION 

_Reward design: energy proxy vs. post-hoc evaluation:_ Section III-B deliberately separates the quantity that _shapes_ 


Fig. 3: Final end-effector position and orientation error on hardware ( _n_ = 30), normalised by the success tolerance ( _dp_ = 4 cm, _do_ = 8 _._ 6<sup>_◦_</sup> ). Boxes show the interquartile range and mean (triangle); points are individual trials. All trials fall below the tolerance line (dashed, = 1). 

the policy from the quantity used to _evaluate_ it. The torquenorm proxy _λτ ∥_ **_τ_** _t∥_<sup>2</sup> is cheap, smooth, and correlates with the copper-loss term of (1) (both scale with _τ_<sup>2</sup> ), but it omits the viscous, Coulomb, and interaction terms and the signdependent mechanical-work term. With _α_ = 0, the full power model (1) never enters the gradient; it is computed purely for post-hoc evaluation (Remark 1). A notable consequence, visible in Sections V-A and V-C, is that the _realised_ energy reduction on hardware (median 54 _._ 9 J vs. a kinematic-simulation mean of 98 _._ 16 J on successful episodes) is driven less by the reward’s energy term than by the deployment PD-gain choice ( _kp_<sup>mj</sup> = 50) and the restricted, lower-effort task envelope of Section V-B. This suggests that enabling _α >_ 0, or increasing _λτ_ , would act as an additional, currently unused lever for further energy reduction, at the cost of a fresh training run (Section IV-C). 

_Sim-to-real gap: mechanism:_ The kinematic environment of Section III-A assumes that the commanded velocity is realised exactly within one step. The MuJoCo PD-gain sweep (Table IV) shows that this assumption is the dominant source 

8 

TABLE IX: Real-robot validation, _n_ = 30: per-joint kinematics/torques (mean over all episodes, max over all steps) and post-hoc energy breakdown (1) (mean over all episodes). 

|Join|t|_|_˙_q|_ mean (ra|d/s)<br>_|_˙_q|_ max|_|τ|_ mean (|N m)|_|τ|_ max (N m)|Exc. mean|Exc. max|
|---|---|---|---|---|---|---|---|---|
|Sh.|pitch|1.46|5.45|7.69||20.25|0.119|0.626|
|Sh.|roll|1.63|7.19|6.03||20.88|0.122|0.534|
|Sh.|yaw|2.41|7.60|4.04||17.06|0.094|0.286|
|Elbo|w|1.78|6.60|5.36||15.50|0.193|0.597|
|Wr.|roll|2.11|8.79|1.16||14.69|0.097|0.503|
|Wr.|pitch|1.77|8.59|2.14||6.96|0.137|0.554|
|Wr.|yaw|1.80|6.15|1.53||6.95|0.148|0.519|
|||Energy term|Mechanical|Copper|Coul|omb<br>Viscous|Interaction||
|||Share (%)|17_._5_±_5_._6|46_._1_±_8_._4|2_._1_±_|0_._3<br>20_._4_±_4_._3|13_._9_±_3_._5||


Fig. 4: Representative hardware trial (101 steps, _∼_ 1 s). (a) Perjoint excursion ( _q−q_ ¯) _/_ (∆ _q/_ 2), with _±_ 1 marking the joint limits. (b) Joint velocities. (c) Measured motor torques. (d) Endeffector position error (left axis) and cumulative energy via the power model (1) (right axis). 

of the sim-to-real gap: the success-rate drop (20–25 percentage points) and the orientation-tracking inflation (11–13<sup>_◦_</sup> above the 8 _._ 6<sup>_◦_</sup> training tolerance) are both largely _independent_ of the PD gain, which is the signature of a structural mismatch between the training assumption and any finite-bandwidth controller, rather than a tuning deficiency. Unlike the generic mitigations suggested for this class of gap—domain randomisation of inertial parameters, or fine-tuning on real-robot data—the PD-gain sweep allowed us to _quantify_ the gap and choose deployment gains ( _kp_<sup>mj</sup> = 50, _kd_<sup>mj</sup> = 1 _._ 5) that keep saturation and energy near the low end of the sweep (Fig. 1) without additional training. 

_Workspace reachability as the dominant factor in the success gap:_ A second, largely independent contributor to the gap between the 69 _._ 9% kinematic rate and the 46% full-workspace MuJoCo rate is geometric, not dynamic: the kinematic environment samples targets in _joint space_ (Section IV-B), which guarantees reachability by construction, 


Fig. 5: Episode-energy percentiles: kinematic simulation ( _n_ =1000, all episodes) vs. real hardware ( _n_ =30, all successful). The hardware distribution is both lower and narrower than the kinematic-simulation distribution at every percentile, consistent with the lower torques and shorter episodes (Table VIII) observed under the restricted task envelope of Section V-B. 

whereas a deployment-style sampling of Cartesian targets within the nominal apple-picking bounding box is reachable in only _∼_ 30% of cases (Table VII). The remaining _∼_ 70% miss by a median of _∼_ 10 cm—an order of magnitude larger than the 4 cm tolerance—which no controller, however well tuned, can close. Once this geometric mismatch is removed by restricting to the reachable task envelope, the MuJoCo screening recovers a 95% success rate ( _n_ = 20), at or above the kinematic reference; on the real robot ( _n_ = 30), every trial lands within tolerance, with end-effector position errors (Fig. 2b) comparable to or tighter than the kinematic reference. This indicates that, for a deployed system, target selection (or a perception/grasp-planning stage that proposes only reachable grasp poses) is at least as important as policy or controller tuning for overall task success. 

_Energy: simulation vs. hardware:_ The energy breakdown shifts substantially between kinematic simulation and hardware (Tables VI and IX). In simulation, copper losses dominate (87 _._ 6%), driven by RNEA torques up to 199 N m on 

9 

the shoulder-pitch joint—torques that arise from the large accelerations a perfect-tracker policy can command. On hardware, the soft PD controller and torque clamp (Section IV-E) limit realised torques to at most 20 _._ 9 N m, and the energy mix becomes more balanced (copper 46 _._ 1%, viscous 20 _._ 4%, mechanical 17 _._ 5%, interaction 13 _._ 9%, Coulomb 2 _._ 1%). The identified power model (1) correctly captures both regimes because all five terms remain active; only their relative shares change with the torque/velocity operating point, which is a useful sanity check on the model’s generality beyond the identification data. 

_Orientation tracking:_ On hardware, the mean final orientation error (6 _._ 92 _±_ 1 _._ 33<sup>_◦_</sup> , Fig. 3) sits close to, but consistently below, the 8 _._ 6<sup>_◦_</sup> tolerance, mirroring the MuJoCo finding that orientation tracking absorbs most of the residual sim-toreal error (Section IV-E). The Hybrid Constellation Reward (Section III-B) couples position and orientation into a single geometric quantity _d_<sup>_t_</sup> con<sup>, which removes the need to separately</sup> tune a position/orientation weight ratio (a known difficulty in the earlier, separable reward, Section IV-C); nonetheless, orientation remains the tighter of the two success criteria in practice, and is the most likely margin to be lost if the task envelope were widened further. 

_Limitations:_ The kinematic-simulation result (69 _._ 9%, _n_ = 1 000, fixed seed) follows the _n ≥_ 1000 protocol adopted after the training lineage of Section IV-C showed that smaller- _n_ improvements did not reproduce at scale. The MuJoCo restrictedenvelope screening ( _n_ = 20) and the real-robot validation ( _n_ = 30) are, by contrast, feasibility-level demonstrations on a single fixed target set within the reachable task envelope; they establish that the policy _can_ operate reliably in this envelope, but do not constitute a formal _n ≥_ 1000 successrate estimate for hardware. Likewise, the reward’s torquenorm energy proxy (Remark 1) was not directly compared, at training scale, against training with _α >_ 0 using the full power model; the lineage of Section IV-C indicates that such changes require a fresh 5 _×_ 10<sup>6</sup> -step run and were outside the project’s remaining compute budget. 

A workspace-reachability analysis attributed most of the remaining gap to geometry rather than dynamics: only _∼_ 30% of a nominal apple-picking bounding box is reachable within 2 cm. Restricting evaluation to this reachable task envelope recovered 95% success in MuJoCo ( _n_ = 20) and, on the physical Unitree G1 over three independent batches ( _n_ = 30), end-effector position/orientation errors of 2 _._ 64 _±_ 1 _._ 04 cm / 6 _._ 92 _±_ 1 _._ 33<sup>_◦_</sup> (worst case 3 _._ 94 cm / 8 _._ 58<sup>_◦_</sup> )—inside the 4 cm _/_ 8 _._ 6<sup>_◦_</sup> training tolerance in every trial—at a median energy of 54 _._ 9 J. 

We emphasise that this work constitutes a _first approach_ in the context of robotic apple harvesting using humanoid robots. The reaching task studied here—moving the end-effector to a target pose within an energy budget—is the core repeated motion of an autonomous picking cycle, but a deployed harvesting system additionally requires perception and fruit localisation, grasp planning and execution, and coordination with locomotion or torso positioning to bring the target within the reachable task envelope identified in Section V-B. The validation arc presented here—moving from a kinematic training assumption, through a dynamics-level sim-to-real gap analysis, to a geometrically restricted but physically validated task envelope—is intended as a template for how such energyaware arm policies can be progressively hardened toward field deployment on a harvesting platform, rather than as a complete harvesting system. 

Future work will focus on: (i) training with _α >_ 0 (full power-model reward) from the current checkpoint, now that the torque-proxy formulation has established a working baseline; (ii) expanding the reachable task envelope through torso or base repositioning, so that a larger fraction of the nominal workspace becomes usable without violating the reachability constraints of Section V-B; (iii) integrating fruit-detection and grasp-pose estimation so that target poses are generated from perception rather than sampled synthetically; and (iv) scaling the real-robot validation toward the _n ≥_ 1000 protocol used in simulation, as compute and operator time allow. 

## APPENDIX 

## VII. CONCLUSION 

This paper presented an end-to-end, energy-aware reinforcement learning framework for the 7-DOF left arm of the Unitree G1 humanoid, validated along a four-stage arc from kinematic simulation to physical hardware. An experimentally identified electrical power model ( _R_<sup>2</sup> = 0 _._ 933, RMSE= 1 _._ 07 W, hold-out _R_<sup>2</sup> = 0 _._ 965) decomposes perjoint power into mechanical, copper, Coulomb, and viscous terms plus pairwise interactions, and serves both as a trainingtime energy proxy ( _λτ ∥_ **_τ_** _∥_<sup>2</sup> ) and as the common evaluation metric for every experiment in this paper. A SAC policy combining an incremental joint-position action space with a Hybrid Constellation Reward reaches 69 _._ 9% success over _n_ = 1 000 kinematic-simulation targets. A frozen-policy MuJoCo validation with a PD-gain sweep showed that this rate drops to 46% under realistic actuator dynamics ( _n_ = 200), with an intrinsic 11–13<sup>_◦_</sup> orientation-tracking penalty arising from the kinematic environment’s perfect-tracker assumption. 

Given start position _x_ 0 _∈_ R<sup>_m_</sup> with zero velocity and acceleration, and a target _x_<sup>_∗_</sup> to be reached at time _T_ , the minimum-jerk trajectory minimises �0 _T_<sup>_∥_...</sup><sup>_x ∥_2</sup><sup>_dt_andhasthe</sup> closed form [18]: 


For evaluation, _x_ is replaced by the joint configuration vector **_q_** _∈_ R<sup>7</sup> and the duration is set automatically as _T_ = (15 _/_ 8) ∆ _q_ max _/_ ˙ _q_ max, where ∆ _q_ max = max _i |qi_<sup>_∗−q_0</sup><sup>_,i|_, so that</sup> the maximum joint velocity never exceeds _q_ ˙max = 2 _._ 5 rad _/_ s. This gives a trajectory duration of 1 _._ 519 _±_ 0 _._ 342 s on average across the target-sampling distribution of Section IV-B, compared to the RL episode budget of 3 _._ 0 s. 

## REFERENCES 

> [1] M. Neunert, M. St¨auble, M. Giftthaler, C. D. Bellicoso, J. Carius, C. Gehring, M. Hutter, and J. Buchli, “Whole-body nonlinear model predictive control through contacts for quadrupeds,” _IEEE Robotics and Automation Letters_ , vol. 3, no. 3, pp. 1458–1465, 2018. 

10 

- [2] M. V. Minniti, F. Farshidian, R. Grandia, and M. Hutter, “Whole-body MPC for a dynamically stable mobile manipulator,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 4, pp. 3687–3694, 2019. 

- [3] J. Pankert and M. Hutter, “Perceptive model predictive control for continuous mobile manipulation,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 6177–6184, 2020. 

- [4] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, _Robotics: Modelling, Planning and Control_ , ser. Advanced Textbooks in Control and Signal Processing. London: Springer, 2010. 

- [5] J. B. Rawlings, D. Q. Mayne, and M. M. Diehl, _Model Predictive Control: Theory, Computation, and Design_ , 2nd ed. Madison, WI: Nob Hill Publishing, 2020. 

- [6] S. Kleff, A. Meduri, R. Budhiraja, N. Mansard, and L. Righetti, “Highfrequency nonlinear model predictive control of a manipulator,” in _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2021, pp. 7330–7336. 

- [7] OpenAI, M. Andrychowicz, B. Baker, M. Chociej, R. J´ozefowicz, B. McGrew, J. Pachocki, A. Petron, M. Plappert, G. Powell, A. Ray, J. Schneider, S. Sidor, J. Tobin, P. Welinder, D. Wierstra, and W. Zaremba, “Solving Rubik’s Cube with a robot hand,” _arXiv preprint arXiv:1910.07113_ , 2019. 

- [8] O. M. Andrychowicz, B. Baker, M. Chociej, R. J´ozefowicz, B. McGrew, J. Pachocki, A. Petron, M. Plappert, G. Powell, A. Ray, J. Schneider, S. Sidor, J. Tobin, P. Welinder, D. Wierstra, and W. Zaremba, “Learning dexterous in-hand manipulation,” in _Proceedings of the International Journal of Robotics Research_ , vol. 39, no. 1, 2020, pp. 3–20. 

- [9] V. Kumar, A. Gupta, E. Todorov, and S. Levine, “Learning dexterous manipulation with episodic reinforcement learning,” in _arXiv preprint arXiv:1611.09318_ , 2021. 

- [10] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Proceedings of the Conference on Robot Learning (CoRL)_ , ser. Proceedings of Machine Learning Research, vol. 164. PMLR, 2022, pp. 91–100. 

- [11] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [12] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” in _Proceedings of the International Conference on Machine Learning (ICML)_ , ser. Proceedings of Machine Learning Research, vol. 80. PMLR, 2018, pp. 1861–1870. 

- [13] N. Deniz, “Physics-based identification of an electrical power consumption model for a 7-DoF humanoid robot arm,” _TODO: journal/conference name_ , 2025, under preparation. 

- [14] R. Featherstone, _Rigid Body Dynamics Algorithms_ . New York, NY: Springer, 2008. 

- [15] J. Carpentier, G. Saurel, G. Buondonno, J. Mirabel, F. Lamiraux, O. Stasse, and N. Mansard, “The Pinocchio C++ library: A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives,” in _Proceedings of the IEEE International Symposium on System Integration (SII)_ , 2019, pp. 614–619. 

- [16] T. Haarnoja, A. Zhou, K. Hartikainen, G. Tucker, S. Ha, J. Tan, V. Kumar, H. Zhu, A. Gupta, P. Abbeel, and S. Levine, “Soft actor-critic algorithms and applications,” _arXiv preprint arXiv:1812.05905_ , 2018. 

- [17] A. Raffin, A. Hill, A. Gleave, A. Kanervisto, M. Ernestus, and N. Dormann, “Stable-Baselines3: Reliable reinforcement learning implementations,” _Journal of Machine Learning Research_ , vol. 22, no. 268, pp. 1–8, 2021. 

- [18] T. Flash and N. Hogan, “The coordination of arm movements: An experimentally confirmed mathematical model,” _Journal of Neuroscience_ , vol. 5, no. 7, pp. 1688–1703, 1985. 

- [19] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2012, pp. 5026– 5033. 

