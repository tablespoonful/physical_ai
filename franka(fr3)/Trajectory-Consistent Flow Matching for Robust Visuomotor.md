---
title: "Trajectory-Consistent Flow Matching for Robust Visuomotor Policy Learning"
date: "2026-05-08"
authors: "Riad Ahmed; Sujosh Nag; Moniruzzaman Akash; Mostafa Hussein; Momotaz Begum"
url: https://arxiv.org/abs/2605.08511
pdf: https://arxiv.org/pdf/2605.08511
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.08511)** / [論文ページ](https://arxiv.org/abs/2605.08511)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Trajectory-Consistent Flow Matching for Robust Visuomotor Policy Learning** 

Riad Ahmed<sup>_∗_</sup> , Sujosh Nag, Moniruzzaman Akash, Mostafa Hussein, and Momotaz Begum 


Fig. 1: Overview of Trajectory-Consistent Flow Matching (Traj-Consistent FM) for visuomotor policy learning. **(a)** Standard flow matching trains pointwise velocity targets, producing curved flow paths from noise _x_ 0 to expert actions _x_ 1. The resulting ODE integration drifts from the expert trajectory, leading to imprecise robot actions. **(b)** Our Traj-Consistent FM enforces trajectory-level supervision through four training losses ( _L_ rect, _L_ multistep, _L_ vel, _L_ action) built atop the base _L_ CFM, combined with RK4 inference, yielding straight, consistent flow paths that converge precisely to expert actions. **(c)** Traj-Consistent FM enables precise manipulation across four real-robot tasks on Franka FR3 and Boston Dynamics Spot, and three simulated MetaWorld tasks. 

**_Abstract_ — Flow matching policies learn continuous velocity fields that transport noise to actions, enabling fast deterministic inference for robot manipulation. However, standard training optimizes a** **_pointwise_ velocity objective while inference requires numerical** **_integration_ of that field—a mismatch that causes compounding trajectory errors. We propose four complementary remedies: (1)** **_auxiliary rectified flow velocity regression_ that provides uniform temporal supervision across the full time interval; (2)** **_multi-step trajectory consistency training_ that supervises the integrated displacement of the velocity field over trajectory segments, directly closing the train–inference gap; (3)** **_velocity field regularization_ that enforces temporal smoothness, preventing oscillations that destabilize integration; and (4)** **_fourth-order Runge-Kutta (RK4) inference_ that reduces global discretization error by orders of magnitude over Euler methods. Critically, these components are not independently sufficient—RK4 without a smooth velocity field fails, and smoothness without trajectorylevel supervision still drifts, as our ablation study confirms. We further pair these with a dual-view 3D point cloud encoder using two independent PointNet encoders for complementary spatial** 

The authors are with the University of New Hampshire, Durham, NH, USA. Emails: _{_ Riad.Ahmed, sujosh.nag, moniruzzaman.akash, Mostafa.Hussein, mbegum _}_ @unh.edu. _∗_ Corresponding author. 

**perception. On four real-robot tasks across a Franka arm and a Boston Dynamics Spot, our method achieves 70% and 60% overall success on two long-horizon multi-phase tasks where both baselines score 0%, and reaches 100% on precision tool placement. Three MetaWorld simulation tasks confirm consistent improvements, validating that trajectory-level supervision is essential for reliable policy execution.** 

# I. INTRODUCTION 

Learning precision manipulation policies that preserve multimodality—different grasp orientations, approach trajectories, and timing variations—remains a central challenge in robot learning. Standard behavior cloning with regression losses averages over multiple valid modes, producing physically unrealizable actions [1], [2]. Diffusion policies [3], [4] model the full action distribution via iterative denoising, but require 50–100 network evaluations per action query, limiting real-time deployment. Flow matching [5], [6], [7] provides a faster deterministic alternative: a learned velocity field transports noise to actions along a continuous ODE, and when the learned trajectories are straight, integration is both fast and accurate. Recent work pairing flow matching with 3D 

point cloud observations has further advanced manipulation performance [8], [9], [10]. 

Despite these advances, we identify a systematic **train– inference mismatch** that limits existing flow matching policies. During training, the velocity field is supervised at isolated, independently sampled time instances. At inference, however, the same field must be _integrated sequentially_ —each step’s output becomes the next step’s input. This gap manifests as three failure modes: (i) _collapsed paired-time supervision_ , where the schedule-based pairing collapses most samples to a single fixed endpoint, leaving the velocity field without diverse inter-step consistency constraints across the time interval; (ii) _compounding integration drift_ , where small per-step errors accumulate as the solver queries the network at states far from the training distribution; and (iii) _velocity oscillations_ that satisfy pointwise objectives but destabilize numerical integration, causing jerky motions and large positional errors. These are especially damaging for precision manipulation. 

Individually, partial remedies exist: rectified flow promotes straight trajectories, consistency training enforces local agreement, velocity regularization penalizes oscillations, and higher-order solvers reduce truncation error. However, no prior work addresses all three failure modes simultaneously in a unified framework. Critically, our ablation confirms the interaction is non-trivial: removing _L_ vel while keeping RK4 drops overall success from 70% to just 10%, demonstrating that the benefit arises from the specific combination rather than any individual component. 

We introduce **Trajectory-Consistent Flow Matching (Traj-Consistent FM)** , which combines four complementary components to close this gap: (1) rectified flow velocity regression for uniform temporal coverage across [0 _,_ 1], (2) multi-step trajectory consistency that directly supervises integrated displacement over trajectory segments, (3) velocity smoothness regularization that prevents temporal oscillations, and (4) RK4 inference that reduces global discretization error by orders of magnitude over Euler. We further design a dual-view 3D point cloud architecture with two independent PointNet encoders for complementary spatial perception. Our contributions: 

- We identify a three-part train–inference gap in flow matching policies—collapsed paired-time supervision, integration drift, and velocity oscillation—and show all three must be addressed jointly. 

- We introduce complementary training losses that produce a globally consistent, temporally smooth velocity field amenable to high-order integration. 

- We deploy RK4 inference and a dual-view 3D point cloud architecture, ablating both against alternatives. 

- On four real-robot tasks across Franka FR3 and Boston Dynamics Spot, we achieve 70% and 60% on longhorizon tasks where baselines score 0%, and 100% on precision tool placement. 

# II. RELATED WORK 

# _A. Generative Policies for Robot Manipulation_ 

Imitation learning has evolved from regression-based cloning [11], [12] and energy-based models [2] to generative formulations. Diffusion Policy [3] models action distributions as denoising processes, with extensions to 3D point clouds [4] and foundation-model scale [13]. Flow matching policies [8], [10], [14] replace stochastic diffusion with deterministic ODEs for faster inference, while ManiCM [15] and Consistency Policy [16] further compress function evaluations via consistency distillation. Both reduce inference cost but retain pointwise training and first-order solvers, addressing neither trajectory-level drift nor velocity field smoothness. 

# _B. Shortcomings of Flow Matching for Policy Learning_ 

Conditional Flow Matching [5], [17] trains velocity networks at independent time points; the composed inference trajectory is never directly supervised. Rectified Flow [6] and OT-CFM [7] promote straighter couplings but retain isolatedtime supervision. Consistency Flow Matching [18] enforces segment-boundary agreement without supervising integrated displacement. Multistep Consistency Models [19] partition the ODE into segments yet still use first-order Euler. 

TPC-FM [20] regularizes velocity oscillations through paired-time penalties, sharing motivation with our _L_ vel, but does not supervise integrated displacement or adopt higherorder solvers. CTM [21] learns anytime-to-anytime jumps via teacher distillation from a pretrained score model, which does not accommodate the changing observation conditioning of closed-loop control. We supervise integrated displacements directly via _L_ multistep without requiring a teacher. Flow Matching robotic policies [8], [14], [22] inherit all these gaps. 

# _C. Flow Matching Advances in Computer Vision_ 

InstaFlow [23] applies iterative reflow for one-step generation; Scaling Rectified Flow Transformers [24] motivate higher-order integration. DPM-Solver [25] and DPM-Solverv3 [26] replace Euler with high-order solvers, reducing truncation error by orders of magnitude. However, these solvers exploit noise-schedule structure (log-SNR reparameterization) specific to diffusion; adapting them to flow matching with observation-conditioned velocity fields would require nontrivial modifications. We use classical RK4, which assumes only smoothness of the velocity field. Our work is the first to bring trajectory-level supervision and higher-order Runge– Kutta integration together into a robot visuomotor policy. 

# III. PRELIMINARIES 

Flow matching [5], [6] learns a velocity field transporting noise to data along a deterministic ODE. In visuomotor policy learning, the target is the conditional action distribution given observations and the source is standard Gaussian noise. 

Given a noise sample _x_ 0 _∼N_ (0 _, I_ ) and an expert action _x_ 1 from the demonstration dataset, flow matching constructs a linear interpolation path: 


A neural network _vθ_ ( _xt, t, c_ ), conditioned on observation feature _c_ , predicts the velocity along this path. For the linear path the ground-truth velocity is constant: _u_<sup>_∗_</sup> ( _t_ ) = _x_ 1 _− x_ 0. At inference, actions are generated by drawing _x_ 0 _∼N_ (0 _, I_ ) and integrating the flow ODE: 


Consistency Flow Matching (Consistency-FM) [18] enforces that predictions from nearby path points agree when projected to a shared segment boundary. The interval [0 _,_ 1] is partitioned into _K_ segments with boundaries 0 = _s_ 0 _< s_ 1 _< · · · < sK_ = 1; let _τ_ ( _t_ ) = _sk_ denote the endpoint of the segment containing _t_ . Training samples _t ∼U_ [ _ε,_ 1] ( _ε_ = 5 _×_ 10<sup>_−_3</sup> ) and pairs each _t_ with _r_ = min( _t_ + _δ,_ 1) where _δ_ is a schedule parameter. The loss requires Euler-forward steps from _xt_ and _xr_ to reach the same segment endpoint with matching velocities: 


where _α_ = 0 _._ 8. Deployment uses first-order Euler steps to integrate the learned velocity field. A gap remains between this pointwise training and the trajectory-level integration required at inference. 

# IV. PROBLEM DEFINITION 

We identify three gaps between the training objective of standard flow matching policies, as described in Section III, and the behavior required at inference time. 

_a) Collapsed paired-time supervision:_ Consistency-FM pairs each _t_ with _r_ = min( _t_ + _δ,_ 1); with the default schedule parameter _δ_ = 0 _._ 7 [18], every _t >_ 0 _._ 3 has _r_ clamped to 1. Consequently, no intermediate-to-intermediate pairs exist in the upper 70% of [0 _,_ 1]—the loss only constrains agreement between each such _t_ and the fixed endpoint _t_ =1. Near _t_ = 1 the pair separation _|r − t|_ vanishes, providing negligible gradient signal. The ODE integrator, however, must traverse the entire interval at inference, including regions where interstep consistency is never directly enforced. 

_b) Trajectory integration drift:_ The loss evaluates _vθ_ at points on the ground-truth path _xt_ , but at inference the solver chains predictions sequentially: after step _n_ the state _xtn_ has drifted from the training path, and the network is queried at off-path states it was never trained on. This compounds across the trajectory and is most harmful in long-horizon tasks. 

_c) Integration instability:_ No constraint prevents _vθ_ from oscillating rapidly in _t_ while still satisfying the pairwise consistency condition. The first-order Euler integrator amplifies such oscillations, producing jerky motions and large positional errors. 

All three gaps stem from the same root cause: training at isolated time points without feedback about the integrated trajectory. We address them jointly in Section V. 

# V. METHOD 

Section III established _L_ CFM (4) and the flow ODE (2); Section IV identified three gaps that arise when the pointwisetrained velocity field is integrated at inference. We present four training losses and one inference-time change that close these gaps. 

# _A. Auxiliary Rectified Flow Velocity Regression_ 

To fill the coverage gaps left by the schedule-based Consistency-FM loss, we add a regression loss that draws _t_ uniformly from [0 _,_ 1] and supervises the velocity field against its analytical target [6]. For the linear path, (1), the target is constant: 


Any temporal variation in _vθ_ introduces curvature that increases the number of function evaluations (NFEs) required for accurate integration. We minimize: 


# _B. Multi-Step Trajectory Consistency_ 

Even a pointwise-accurate velocity field can drift when integrated, because errors shift the state off the training distribution. We supervise the _outcome of integration_ over trajectory segments. For a randomly sampled pair _t_ 0 _< t_ 1 drawn from [0 _,_ 1], the ground-truth displacement along path (1) from _t_ 0 to _t_ 1 is: 


Starting from the on-path point _x_<sup>(0)</sup> = (1 _− t_ 0) _x_ 0 + _t_ 0 _x_ 1, we roll out the learned velocity field using _S_ = 4 Euler steps with step size _h_ = ( _t_ 1 _− t_ 0) _/S_ : 


We sample _K_ = 3 independent segments per training step and average their losses. The gradient backpropagates through all _S_ steps, training _vθ_ to produce mutually consistent sequences—unlike _L_ CFM and _L_ rect, which see each time step in isolation. The multi-step rollout (8) is a composition _x_<sup>(</sup><sup>_S_)</sup> = _gS ◦· · · ◦ g_ 1( _x_<sup>(0)</sup> ), where _gs_ ( _x_ ) ≜ _x_ + _vθ_ ( _x, t_ 0 + _Ss_<sup>(</sup><sup>_t_1</sup><sup>_−t_0)</sup><sup>_,c_)</sup><sup>_<u>t</u>_</sup><sup><u>1</u></sup><sup>_−_</sup> _S_<sup>_<u>t</u>_</sup><sup><u>0</u></sup> is a single Euler step and _c_ is produced by the observation encoder. By the chain rule, _∂L_ multistep _/∂c_ accumulates gradient contributions from all _S_ steps. Concretely, if the encoder confuses two visually similar objects (e.g., two cups differing only by a thin stripe), the conditioning vector _c_ shifts by _δc_ ; each step then produces a velocity error _δv ∝ ∂vθ/∂c · δc_ , and after _S_ steps the displacement error grows as _∥_ ∆<sup>ˆ</sup> _x−_ ∆ _x_<sup>_∗_</sup> _∥∝ S ·∥δv∥·_ ∆ _t_ . By contrast, _L_ CFM and _L_ rect evaluate a single network call per sample, so the encoder gradient reflects only a one-step velocity deviation—too weak to penalize subtle encoding errors. The _S_ -step amplification 


Fig. 2: **Train–inference gap in flow policies and our remedy.** (a) Pointwise flow matching trains _vθ_ ( _xt, t_ ) at independently sampled times, without enforcing consistency along an integrated trajectory. (b) During inference, the solver composes predictions sequentially; small per-step errors _ϵi_ move the state off the training path and compound, yielding _x_ ˆ1 _̸_ = _x_ 1. (c) Our trajectory-consistency objectives supervise integrated displacements over short multi-step segments and through rollouts, encouraging a self-correcting velocity field. **Bottom:** supervision coverage over _t ∈_ [0 _,_ 1] for each loss component. 

in _L_ multistep thus produces a gradient signal proportional to the _integrated_ cost of misidentification, making the encoder sensitive to fine-grained visual distinctions that single-step losses ignore. 

# _C. Velocity Smoothness Regularization_ 

The Consistency-FM loss places no constraint on how _vθ_ varies between paired times, allowing temporally irregular fields that degrade RK4’s four intermediate evaluations. We penalize consecutive velocity differences along _S_ = 5 uniformly spaced times on a random path: 


We omit a magnitude penalty _∥vθ∥_<sup>2</sup> since the target _u_<sup>_∗_</sup> = _x_ 1 _− x_ 0 has non-trivial magnitude. _L_ rect anchors the field to the correct constant target; _L_ vel penalizes variation around it. 

# _D. RK4 Integration at Inference_ 

At inference we replace the standard Euler method with fourth-order Runge-Kutta (RK4) [27] as the numerical ODE solver for integrating the flow ODE (2). RK4 queries the conditional vector field at four evaluation points within the current time step [ _tn, tn_ + ∆ _t_ ]: 


RK4 achieves _O_ (∆ _t_<sup>4</sup> ) global truncation error versus _O_ (∆ _t_ ) for Euler, where each RK4 step requires 4 NFEs (network forward passes). We deploy _N_ =30 RK4 steps (120 NFEs); Fig. 2 visualizes the improvement. 

At a fixed NFE budget _M_ , Euler takes _M_ steps at ∆ _tE_ = 1 _/M_ while RK4 takes _M/_ 4 steps at ∆ _tR_ = 4 _/M_ , both using exactly _Mτ_ wall-clock time ( _τ_ = one forward pass). Global 


Fig. 3: Vector fields visualize the learned velocity _vθ_ ( _t, x_ ) in a 1D toy ( _t, x_ ) setting; color encodes _∥vθ − u_<sup>_∗_</sup> _∥_ . (a) _LCF M_ alone provides sparse supervision and induces bias. (b) _Lrect_ adds dense pointwise constraints but does not eliminate compounding drift. (c) _Lmultistep_ constrains integrated _S_ =4 step displacements, reducing drift. (d) _Lvel_ penalizes temporal variation in _vθ_ , yielding smoother, more uniform fields. (e) At inference, RK4 benefits from the smoother field and exhibits lower discretization error than Euler. 

truncation error scales as _ε_ Euler = _C_ 1∆ _tE_ and _ε_ RK4 = _C_ 4∆ _tR_<sup>4, where</sup><sup>_C_1</sup><sup>_, C_4 depend on the regularity of the velocity</sup> field. Their ratio is _ε_ Euler _/ε_ RK4 = _C_ 1 ∆ _tE /_ ( _C_ 4 ∆ _tR_<sup>4).With</sup> ∆ _tR_ = 4 ∆ _tE_ this becomes ( _C_ 1 _/C_ 4) _·_ ∆ _t_<sup>_−_</sup> _E_<sup>3</sup><sup>_/_256,i.e.the</sup> advantage grows as _O_ (∆ _t_<sup>_−_</sup> _E_<sup>3)withthebudget.Assuming</sup> comparable constants ( _C_ 1 _≈ C_ 4), our budget _M_ =120 gives _ε_ Euler _/ε_ RK4 _≈_ 6 _,_ 750; Euler would need _∼_ 810 _,_ 000 steps to match—far exceeding any real-time budget at 20 Hz. Critically, RK4’s advantage requires a smooth velocity field: the four evaluations _k_ 1– _k_ 4 per step must return consistent estimates, which oscillatory fields violate. Dedicated diffusion solvers such as DPM-Solver [25] exploit log-SNR reparameterization specific to score-based models and do not directly apply to observation-conditioned flow matching ODEs. 

# _E. Full Training Objective_ 

The complete training objective is: 

_L_ = _L_ CFM + _λ_ r _L_ rect + _λ_ c _L_ multistep + _λ_ v _L_ vel + _λ_ a _L_ action _,_ 


where _L_ action = E[ _∥x_ ˆ1 _− x_ 1 _∥_<sup>2</sup> ] runs a _S_ act=5-step Euler rollout from _x_ 0 _∼N_ (0 _, I_ ) to _t_ =1 and penalizes endpoint error. This uses fewer steps and a simpler solver than the 30-step RK4 at deployment; back-propagating through 120 NFEs would be memory-prohibitive. The mismatch is benign: _L_ action acts as a coarse end-to-end sanity check ( _λ_ a=0 _._ 1), while the gap-closing losses _L_ multistep and _L_ vel supervise the velocity field directly and are solver-agnostic. 

The five losses provide complementary supervision at different levels: _L_ CFM enforces local pairwise consistency, _L_ rect anchors each prediction to the ground-truth velocity, _L_ multistep supervises the integrated trajectory, _L_ vel regularizes temporal smoothness, and _L_ action checks the final output. We set _λ_ r = 1 _._ 0, _λ_ c = 0 _._ 5, _λ_ v = 0 _._ 1, _λ_ a = 0 _._ 1. The higher weights on _L_ CFM and _L_ rect reflect their role as primary accuracy-driving losses, while the lower weights keep the regularizers subordinate. Figure 3 shows the convergence dynamics of each component. 

# _F. Observation Encoding_ 

Each observation consists of an agent-view point cloud _Pa ∈_ R<sup>_N×_6</sup> (XYZ+RGB) (where _N_ is the pointcloud number) an eye-in-hand point cloud _Pe ∈_ R<sup>_N×_6</sup> , and proprioception _s ∈_ R<sup>21</sup> . Two independent PointNet encoders [28] with identical architecture but separate weights produce: 


The proprioceptive state gives _fs_ = MLP( _s_ ) _∈_ R<sup>64</sup> ; the full observation vector is _c_ = [ _fa_ ; _fe_ ; _fs_ ] _∈_ R<sup>192</sup> . Separate encoders let each view specialize: the agent-view encoder for object identity and global position, the eye-in-hand encoder for contact geometry and local detail. The policy receives _n_ obs = 2 consecutive steps; the conditioning signal is _C_ = [ _c_ 1; _c_ 2] _∈_ R<sup>384</sup> . 

# _G. Velocity Network Architecture_ 

The velocity network _vθ_ is a 1D conditional UNet [3] that operates along the temporal dimension of the action sequence _xt ∈_ R<sup>_H×Da_</sup> , where _H_ = 16 is the prediction horizon (number of future action steps) and _Da_ = 7 is the action dimension (3D position delta, 3D orientation delta, gripper command). The network receives three inputs: the noisy action sequence _xt_ , a sinusoidal time embedding (dim 128) encoding the flow time _t_ , and the observation conditioning vector _C_ , and outputs a velocity field of the same shape R<sup>_H×Da_</sup> . The UNet has three resolution levels with channel dimensions (256 _,_ 512 _,_ 1024), kernel size 5, and FiLM conditioning [29] that modulates intermediate features based on the time embedding and observation at each level. All parameters—both PointNet encoders and the UNet—are trained jointly end-to-end. We maintain an exponential moving average (EMA) of network weights with decay 0 _._ 9999 and use the EMA model at deployment. Figure 4 illustrates the full pipeline from point cloud observations to velocity field prediction. 

# _H. Training Configuration_ 

All four auxiliary losses operate exclusively during training; the deployed inference pipeline differs from the baseline only by replacing Euler with RK4, adding zero architectural overhead (Section V-D). The main training cost is _L_ multistep, requiring _S_ =4 extra forward passes per segment with backpropagation through the solver, increasing per-epoch time by _∼_ 35% and GPU memory by _∼_ 20% (RTX 4090, batch 64; total: _∼_ 5 _._ 5h vs. _∼_ 4h for 400 epochs on Bell Pepper). 

# VI. EXPERIMENTS 

# _A. Robot Platforms and Setup_ 

We evaluate on a **Franka Emika FR3** 7-DOF arm with parallel gripper and a **Boston Dynamics Spot** mobile manipulator (6-DOF arm). Both use calibrated RGBD sensing from agent-view and wrist-view perspectives (Intel RealSense cameras on Franka; RealSense + onboard hand camera on Spot). Observations consist of two 8,192point clouds (XYZ+RGB) and 21-d proprioception; actions are 7-d end-effector delta commands. Demonstrations are collected at 20 Hz via SpaceMouse (Franka) and Meta Quest 3 teleoperation (Spot). 

# _B. Tasks_ 

We evaluate on four real-robot manipulation tasks across two platforms (Fig. 5). We group tasks into _short-horizon_ settings with a single continuous manipulation phase and _longhorizon_ settings that require executing multiple sequential subtasks with distinct phases. 

_1) Short-Horizon Tasks:_ **Cereal Pouring (Franka, 30 demos).** The robot grasps a bowl containing cereal, moves above a target plate, and pours. Due to high friction and granular jamming, success often requires a smooth tilting motion combined with small shaking perturbations to reliably empty the bowl. 

**Screwdriver Placement (Spot, 32 demos).** Spot grasps a screwdriver and brings its tip into contact with a small target cube. Poses are randomized, emphasizing precise tool-tip alignment on a mobile manipulator. 

_2) Long-Horizon Tasks:_ **Bell Pepper Placing (Franka, 70 demos).** Two subtasks: (1) grasp a bell pepper and place it into a pot, then (2) grasp the lid and place it onto the pot with rim alignment. Demonstrations are collected across widely varying initial configurations—pepper, pot, and lid poses are randomized each episode—producing a broad action distribution that the policy must generalize over. **Cup Stacking (Franka, 101 demos).** Two subtasks with three cups at randomized poses: (1) insert the plain blue cup into the gray cup, then (2) insert the black-striped blue cup into the assembled stack. The 101 demonstrations cover diverse spatial arrangements. This task couples precise sequential insertions with fine-grained visual discrimination between two nearly identical cups differing only by a thin black stripe. 


Fig. 4: Dual-view 3D point cloud observation encoder. A fixed **agent-view** camera captures global object positions and workspace layout; a wrist-mounted **eye-in-hand** camera captures contact geometry around the gripper. Independent PointNet encoders PN _θa_ , PN _θe_ extract 64-d features from each cloud. Features are concatenated with a 64-d proprioceptive embedding to form the 192-d conditioning vector _c_ , stacked across two timesteps into the 384-d input _g_ for the velocity network. 


Fig. 5: Real-robot task setups and execution sequences. **Top two rows:** Cup Stacking and Bell Pepper Placing on the Franka FR3 arm. **Bottom two rows:** Cereal Pouring on the Franka FR3 and Screwdriver Placement on the Boston Dynamics Spot. Each sequence shows key phases of the manipulation trajectory from approach to task completion. 

_3) Simulation Tasks:_ We additionally evaluate on three MetaWorld [30] tasks— **Drawer Open** , **Assembly** (peg insertion), and **Bin Picking** —which provide deterministic dynamics and noise-free observations. Since all methods reach near-perfect success, we use these tasks primarily to compare trajectory quality via the MetaWorld reward signal, which penalizes inefficient or jerky motions. 

# _C. Baselines_ 

To ensure a fair comparison, all three methods share the same dual-view PointNet observation encoder (Section V-F) and the same 1D conditional UNet architecture (Section V- G); only the training objective and inference solver differ. 

TABLE I: Simulation results on three MetaWorld tasks (50 episodes each). Columns per task: _S_ (%) = Success Rate and _R_ = Reward. Best per task in **bold** . 

||Drawer|Open|Asse|mbly|Bin|Picking|
|---|---|---|---|---|---|---|
|Method|_S_|_R_|_S_|_R_|_S_|_R_|
|DP3 [4]|98.0<br>|376.3|88.0|241.6|96.0|88.3|
|Consistency FM [8]|100.0<br>|386.6|98.0|259.3|96.0|88.5|
|**Traj-Consistent FM (Ours) **|**100.0**<br>|**446.3**|**98.0 **|**281.2 **|**96.0**|**89.5**|


This isolates the effect of our proposed losses and integration method from architectural choices. 

**DP3** [4]: A DDPM-based diffusion policy using 20-step DDIM denoising, representing the state-of-the-art diffusion paradigm for 3D point cloud policies. 

**Consistency FM** [8]: The FlowPolicy baseline with _L_ CFM and first-order Euler integration—the base upon which TrajConsistent FM is built, without our additional losses or RK4. This directly measures the contribution of our improvements. 

# _D. Simulation Results_ 

Table I reports success rate and mean trajectory reward across three MetaWorld simulation tasks [30], evaluated over 50 episodes per method. 

All three methods achieve near-perfect success rates, as expected with deterministic dynamics and noise-free observations. However, trajectory reward—penalizing inefficient or jerky motions—reveals meaningful quality differences. TrajConsistent FM achieves the highest rewards across all tasks (e.g., 446.3 vs. 386.6 on Drawer Open, 15% improvement), indicating smoother, more direct trajectories. This quality gap becomes performance-critical on physical robots, where noisy observations amplify integration errors. 

# _E. Short-Horizon Real-Robot Results_ 

Table II reports success rates on the two short-horizon real-robot tasks, evaluated over 20 trials per method. 

Traj-Consistent FM outperforms both baselines on both tasks. On Cereal Pouring (80% vs. 65%/55%), _L_ vel is the key differentiator: pouring requires a smooth tilting arc, and 

TABLE II: Short-horizon real-robot results (success rate %). Best per task in **bold** . Evaluated over 20 trials. 

|Method|Cereal Pouring|Screwdriver|
|---|---|---|
|DP3 [4]|55|70|
|Consistency FM [8]|65|60|
|**Traj-Consistent FM (Ours)**|**80**|**100**|


TABLE III: Long-horizon real-robot results (success rate %). S1 and S2 denote subtask 1 and subtask 2 success. Overall requires both subtasks to succeed. Best per column in **bold** . Evaluated over 20 trials. 

||Bell|Pep|per Placing|Cu|p S|tacking|
|---|---|---|---|---|---|---|
|Method|S1|S2|Overall|S1|S2|Overall|
|DP3 [4]|60|0|0|55|0|0|
|Consistency FM [8]|50|0|0|40|0|0|
|**Traj-Consistent FM (Ours) **|**95 **|**70**|**70**|**90 **|**60**|**60**|


baseline failures involve abrupt wrist rotations that scatter cereal or fail to initiate pouring. On Screwdriver Placement (100% vs. 60%/70%), _L_ rect + RK4 delivers the endpoint precision needed for tool-tip contact with the small target cube; baseline failures stem from accumulated integration drift causing the tip to miss by several millimeters. 

# _F. Long-Horizon Real-Robot Results_ 

Table III reports subtask-level and overall success rates on the two long-horizon real-robot tasks. Each task consists of two sequential subtasks; the trial proceeds to the second subtask only if the first succeeds. Evaluation uses 20 trials per method. 

Neither baseline completed a single full trial (0% overall) on either task, despite achieving 40–60% S1 success— demonstrating that the baselines learn competent single-phase policies but cannot sustain accuracy through multi-phase rollouts. The broad configuration diversity in demonstrations amplifies this effect: the velocity field must remain accurate across a wide observation distribution, and pointwise-trained fields inevitably drift when queried at states accumulated over extended integration. Traj-Consistent FM achieves 95%/70% (S1/Overall) on Bell Pepper and 90%/60% on Cup Stacking because _L_ multistep directly supervises integrated displacements across this configuration space, while _L_ vel ensures the smooth field that RK4 requires for its theoretical accuracy advantage. 

_a) Bell Pepper Placing:_ Baselines fail through three recurring modes (Fig. 5): (a) the policy confuses the pepper with the lid (object discrimination error), (b) the arm drifts toward the wrong receptacle after grasping (placement target confusion), and (c) the policy stalls after subtask 1 and hovers instead of transitioning to lid grasping. These failures are characteristic of accumulated integration drift: the velocity field produces reasonable per-step actions, but compounded errors shift the state to regions where the observation conditioning no longer specifies the correct subtask. Traj-Consistent FM’s trajectory-level supervision prevents this by training the velocity network to maintain accurate displacements over 

TABLE IV: Ablation study on Bell Pepper Placing (success rate %). Each row removes one component from the full TrajConsistent FM model. Best per column in **bold** . Evaluated over 20 trials. 

|Configuration|S1|S2|Overall|
|---|---|---|---|
|Full model (Traj-Consistent FM)|**95**|**70**|**70**|
|w/o multi-step consistency loss|60|20|20|
|w/o velocity regularization|50|10|10|
|w/o RK4 (Euler inference)|80|40|40|
|w/o dual-view (shared PointNet)|85|45|45|


extended horizons, keeping the integrated state within the learned distribution. 

_b) Cup Stacking:_ The two blue cups differ only by a thin black strip, making this task a direct test of the visual encoding mechanism described in Section V-B: a single-step loss penalizes only the instantaneous velocity deviation from confusing the cups, whereas _L_ multistep’s _S_ - step rollout amplifies that encoding error into a displacement loss proportional to the segment length. Baselines, trained with only pointwise losses, frequently pick the wrong cup first or produce jerky insertions that knock over the stack. Traj-Consistent FM makes zero cup-discrimination errors across all 20 evaluation trials, consistent with the _S×_ gradient amplification driving the encoder to resolve fine-grained visual differences. Remaining failures occur only when cups are placed very close together, causing point cloud overlap. The 30-point S1-to-Overall drop reflects the compounding difficulty of the second insertion, where the target receptacle (the gray cup with first blue cup inside) presents a narrower opening. 

# _G. Ablation Study_ 

We ablate on Bell Pepper Placing—the longest-horizon task, where compounding errors are most visible. Table IV reports success rates when individual components are removed. 

Every component contributes independently, and the magnitudes of the drops are informative. Removing _L_ vel causes the largest drop (S1: 95% _→_ 50%, Overall: 70% _→_ 10%): without smoothness, the velocity field oscillates between solver evaluations and even short-horizon grasps fail due to imprecise gripper positioning. This confirms that _L_ vel is the most critical single component. Removing _L_ multistep has a more targeted effect (Overall: 70% _→_ 20%): S1 remains moderate (60%) since the first subtask is shorter, but without trajectory-level feedback the drift becomes fatal for the longer second phase. Replacing RK4 with Euler reduces overall to 40%; S1 remains relatively high (80%), confirming that Euler’s _O_ (∆ _t_ ) error compounds primarily over the longer second phase. A shared PointNet drops overall to 45%: a single encoder must simultaneously parse near-field contact geometry and far-field object positions from a merged cloud, degrading both. 

# _H. Discussion_ 

The performance gap scales with task difficulty: nearsaturated in simulation, 15–40 percentage points on shorthorizon tasks, and decisive on long-horizon tasks (70% 

vs. 0%). This progression follows directly from the train– inference gap analysis in Section IV: velocity-field drift is manageable over short horizons but compounds to fatal errors for multi-phase tasks where the integration path is much longer. As an indirect consequence, the _S_ -step gradient amplification of _L_ multistep (analyzed in Section V- B) forces the PointNet encoder to resolve visual details that pointwise losses are insensitive to—an effect validated by Traj-Consistent FM’s zero cup-discrimination errors on Cup Stacking. DP3 and Consistency FM represent the diffusion and flow matching paradigms for 3D point cloud policies. We exclude ManiCM [15] and Consistency Policy [16] because consistency distillation is orthogonal—it compresses inference steps, while we address training and integration of the velocity field. The 0% overall baseline success on longhorizon tasks directly manifests compounding integration drift, not weak tuning. Both DP3 and Consistency FM are heavily optimized state-of-the-art methods, evidenced by their competitive short-horizon performance (Table II) and DP3’s 55% S1 success on Cup Stacking (Table III). Because these baselines rely on pointwise supervision, small per-step errors accumulate across long horizons, physically manifesting as phase-transition failures—stalling after a successful grasp or drifting toward incorrect receptacles (Table III). TrajConsistent FM’s trajectory-level supervision directly arrests this compounding error. 

# VII. CONCLUSION 

We presented Trajectory-Consistent Flow Matching, addressing the train–inference gap in flow matching policies through auxiliary rectified flow velocity regression, multistep trajectory consistency training, velocity smoothness regularization, and RK4 inference. On four real-robot tasks across two platforms, our method achieves 70% and 60% overall success on long-horizon multi-phase tasks where both baselines score 0%, and reaches 100% on precision tool placement. Our ablation confirms that no single component is sufficient: the interaction between trajectory-level supervision, smooth velocity fields, and higher-order integration is what enables reliable long-horizon execution. The core insight— that trajectory-level supervision is essential when pointwisetrained velocity fields are integrated as ODEs—applies broadly to any iterative generative policy, including diffusionbased formulations. Future work includes learning segment endpoints and step counts adaptively, incorporating optimal transport couplings for improved noise-data pairings, and extension to bimanual and deformable-object manipulation tasks. 

# REFERENCES 

- [1] D. A. Pomerleau, “Alvinn: An autonomous land vehicle in a neural network,” in _Advances in Neural Information Processing Systems_ , 1989. 

- [2] P. Florence, C. Lynch, A. Zeng, O. A. Ramirez, A. Wahid, L. Downs, A. Wong, J. Lee, I. Mordatch, and J. Tompson, “Implicit behavioral cloning,” in _Conference on Robot Learning_ , 2021, pp. 158–168. 

- [3] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Robotics: Science and Systems_ , 2023. 

- [4] Y. Ze, G. Zhang, K. Zhang, C. Hu, M. Wang, and H. Xu, “3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- [5] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _International Conference on Learning Representations_ , 2023. 

- [6] X. Liu, C. Gong, and Q. Liu, “Flow straight and fast: Learning to generate and transfer data with rectified flow,” in _International Conference on Learning Representations_ , 2023. 

- [7] A. Tong, N. Malkin, K. Fatras, L. Atanackovic, Y. Zhang, G. Huguet, G. Wolf, and Y. Bengio, “Improving and generalizing flow-matching for conditional generation,” _arXiv preprint arXiv:2302.00482_ , 2023. 

- [8] Q. Zhang, Z. Liu, H. Fan, G. Liu, B. Zeng, and S. Liu, “Flowpolicy: Enabling fast and robust 3d flow-based policy via consistency flow matching for robot manipulation,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 39, no. 14, 2025, pp. 14 754–14 762. 

- [9] S. Noh, D. Nam, K. Kim, G. Lee, Y. Yu, R. Kang, and K. Lee, “3d flow diffusion policy: Visuomotor policy learning via generating flow in 3d space,” _arXiv preprint arXiv:2509.18676_ , 2025. 

- [10] E. Chisari, N. Heppert, M. Argus, T. Welschehold, T. Brox, and A. Valada, “Learning robotic manipulation policies from point clouds with conditional flow matching,” _arXiv preprint arXiv:2409.07343_ , 2024. 

- [11] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics_ , 2011, pp. 627–635. 

- [12] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _Robotics: Science and Systems_ , 2023. 

- [13] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [14] X. Hu, Q. Liu, X. Liu, and B. Liu, “Adaflow: Imitation learning with variance-adaptive flow-based policies,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 138 836–138 858, 2024. 

- [15] G. Lu, Z. Gao, T. Chen, W. Ding, J. Zhang, and Z. Wang, “ManiCM: Real-time 3d diffusion policy via consistency model for robotic manipulation,” _arXiv preprint arXiv:2406.01586_ , 2024. 

- [16] A. Prasad, K. Lin, J. Wu, L. Zhou, and J. Bohg, “Consistency policy: Accelerated visuomotor policies via consistency distillation,” in _Robotics: Science and Systems_ , 2024. 

- [17] M. S. Albergo and E. Vanden-Eijnden, “Building normalizing flows with stochastic interpolants,” in _International Conference on Learning Representations_ , 2023. 

- [18] L. Yang, Z. Zhu, Z. Hong, M. Xu, W. Zhao, H. Li, W. Zhang, Z. Zhang, B. Cui, and G. Huang, “Consistency flow matching: Defining straight flows with velocity consistency,” _arXiv preprint arXiv:2407.02398_ , 2024. 

- [19] J. Heek, E. Hoogeboom, and T. Salimans, “Multistep consistency models,” _arXiv preprint arXiv:2403.06807_ , 2024. 

- [20] G. Li, P. Zhang, C.-C. Liu, and C.-G. Wu, “Temporal pair consistency guided rectified flow,” _arXiv preprint arXiv:2501.12540_ , 2025. 

- [21] D. Kim, C.-H. Lai, W.-H. Liao, N. Murata, Y. Takida, T. Uesaka, Y. He, Y. Mitsufuji, and S. Ermon, “Consistency trajectory models: Learning probability flow ode trajectory of diffusion,” _arXiv preprint arXiv:2310.02279_ , 2024. 

- [22] A. Rouxel, S. Rohou, and A. Kheddar, “Flow matching imitation learning for multi-support manipulation,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2024. 

- [23] X. Liu, X. Zhang, J. Ma, J. Peng, and Q. Liu, “InstaFlow: One step is enough for high-quality diffusion-based text-to-image generation,” in _International Conference on Learning Representations_ , 2024. 

- [24] P. Esser, S. Kulal, A. Blattmann, R. Entezari, J. Muller, H. Saini, Y. Levi,¨ D. Lorenz, A. Sauer, F. Boesel, D. Podell, T. Dockhorn, Z. English, and R. Rombach, “Scaling rectified flow transformers for high-resolution image synthesis,” in _Proceedings of the 41st International Conference on Machine Learning_ , 2024. 

- [25] C. Lu, Y. Zhou, F. Bao, J. Chen, C. Li, and J. Zhu, “DPM-Solver: A fast ODE solver for diffusion probabilistic model sampling in around 10 steps,” in _Advances in Neural Information Processing Systems_ , vol. 35, 2022. 

- [26] K. Zheng, C. Lu, J. Chen, and J. Zhu, “DPM-Solver-v3: Improved diffusion ODE solver with empirical model statistics,” _Advances in Neural Information Processing Systems_ , vol. 36, 2024. 

- [27] J. C. Butcher, “Numerical methods for ordinary differential equations.” John Wiley & Sons, 2016. 

- [28] C. R. Qi, H. Su, K. Mo, and L. J. Guibas, “Pointnet: Deep learning on point sets for 3d classification and segmentation,” in _IEEE Conference on Computer Vision and Pattern Recognition_ , 2017, pp. 652–660. 

- [29] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville, “FiLM: 

   - Visual reasoning with a general conditioning layer,” in _AAAI Conference on Artificial Intelligence_ , 2018. 

- [30] T. Yu, D. Quillen, Z. He, R. Julian, K. Hausman, C. Finn, and S. Levine, “Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning,” in _Conference on Robot Learning_ . PMLR, 2020, pp. 1094–1100. 

