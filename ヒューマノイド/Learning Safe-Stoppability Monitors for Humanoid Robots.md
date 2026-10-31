---
title: "Learning Safe-Stoppability Monitors for Humanoid Robots"
date: "2026-03-24"
authors: "Yifan Sun; Yiyuan Pan; Shangtao Li; Caiwu Ding; Tao Cui; Lingyun Wang"
url: https://arxiv.org/abs/2603.22703
pdf: https://arxiv.org/pdf/2603.22703
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.22703)** / [論文ページ](https://arxiv.org/abs/2603.22703)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Learning Safe-Stoppability Monitors for Humanoid Robots** 

Yifan Sun<sup>1</sup> , Yiyuan Pan<sup>1</sup> , Shangtao Li<sup>1</sup> , Caiwu Ding<sup>2</sup> , Tao Cui<sup>2</sup> , Lingyun Wang<sup>2</sup> , Changliu Liu<sup>1</sup> 1Robotics Institute, Carnegie Mellon University, Pittsburgh, PA, USA 

> 2Foundational Technologies, Siemens Corporation, Princeton, NJ, USA 

- _{_ yifansu2, yiyuanp, shangtal, cliu6 _}_ @andrew.cmu.edu 

   - _{_ caiwu.ding, tao.cui, max.wang _}_ @siemens.com 


Fig. 1. **Safe-stoppability monitoring for humanoid robots.** Emergency stops for humanoids cannot simply cut power; instead, a predefined fallback controller is triggered to drive the robot toward a minimum-risk condition (MRC). We simulate fallback executions from nominal states in a digital twin to label whether the robot can safely reach the terminal configuration without collision or failure. These labels are used to train a neural monitor that predicts the real-time safe-stoppability confidence of the current state. The monitor can not only discourage pre-mature execution of the fallback policy, but also enable proactive intervention by triggering the fallback policy before the robot enters states from which safe stopping is no longer possible. 

**_Abstract_ — Emergency stop (E-stop) mechanisms are the de facto standard for robot safety. However, for humanoid robots, abruptly cutting power can itself cause catastrophic failures; instead, an emergency stop must execute a predefined fallback controller that preserves balance and drives the robot toward a minimum-risk condition. This raises a critical question: from which states can a humanoid robot safely execute such a stop? In this work, we formalize emergency stopping for humanoids as a policy-dependent safe-stoppability problem and use data-driven approaches to characterize the safestoppable envelop. We introduce PRISM (Proactive Refinement of Importance-sampled Stoppability Monitor), a simulationdriven framework that learns a neural predictor for statelevel stoppability. PRISM iteratively refines the decision boundary using importance sampling, enabling targeted exploration of rare but safety-critical states. This targeted exploration significantly improves data efficiency while reducing falsesafe predictions under a fixed simulation budget. We further demonstrate sim-to-real transfer by deploying the pretrained monitor on a real humanoid platform. Results show that modeling safety as policy-dependent stoppability enables proactive safety monitoring and supports scalable certification of failsafe behaviors for humanoid robots. The project website can be found at https://intelligent-control-lab.github. io/humanoid_stoppability/.** 

## I. INTRODUCTION 

Humanoid robots are increasingly deployed in unstructured, human-centered environments where unexpected contacts, perception errors, model mismatch, or external disturbances may arise during task execution. In such settings, 

a fundamental safety layer is the emergency-stop (E-stop) mechanism. Unlike fixed-base industrial manipulators, however, a humanoid robot cannot simply cut power when an E-stop is triggered. Due to their underactuated nature and reliance on unilateral ground contacts, abrupt power loss inevitably induces catastrophic falls and secondary collisions. Instead, humanoid E-stop must execute a predefined fallback controller that preserves balance, regulates contacts, and drives the robot toward a safe terminal configuration. 

On the other hand, E-stop triggers are asynchronous and unpredictable. An emergency stop may be triggered at any time due to human intrusion, system-level anomalies, communication failures, or direct operator intervention. Given the temporal unpredictability of these interventions, the robot must maintain its state in the _safe-stoppable envelope (SSE)_ : a set of states from which the fallback controller can reliably drive the robot to a dynamically stable terminal condition, usually called _minimum risk condition_ (MRC). This requirement leads to a state-dependent fail-safe property that we call _safe-stoppablity_ . Rather than requiring invariant safety under nominal control, safe-stoppability asks a more urgent question: 

_If we press the button, would the robot survive the stop?_ 

We formalize this property as a stochastic reach-avoid condition under the fixed fallback policy. A state is _safely_ 

_stoppable_ if, when the fallback controller is triggered, the robot can reach MRC while avoiding intermediate failures such as falls, forbidden collisions, or joint-limit violations. Importantly, this definition naturally excludes states from which failure is inevitable before the fallback policy can bring the system to the MRC, as such states lie outside SSE. 

This perspective leads to a critical insight: a safestoppability monitor can serve not only as a _passive_ diagnostic tool after an external E-stop trigger, but also as a _proactive_ supervisory mechanism. By continuously evaluating whether the current state remains within SSE, the monitor can autonomously trigger E-stop behavior before catastrophic failure occurs, effectively preventing falls or collisions that would otherwise unfold under nominal control. In this way, safe-stoppability becomes a runtime assurance mechanism that bridges nominal task execution and emergency intervention. 

Nevertheless, precisely characterizing SSE for highdimensional humanoids is fundamentally challenging. First, exact reach–avoid computation under nonlinear, contact-rich hybrid dynamics is analytically intractable and numerically prohibitive. Second, directly learning the boundary from hardware data is unsafe and impractical, as failure trials are costly and potentially catastrophic. Third, failure-tostop events lie in the long tail of the state distribution, making naive data collection highly inefficient and poorly conditioned near the boundary of SSE between stoppable and non-stoppable states. 

To address these challenges, we introduce **PRISM** ( **P** roactive **R** efinement of **I** mportance-sampled **S** toppability **M** onitors), a simulation-driven framework that learns a neural safe-stoppability monitor under a predefined fallback controller for E-stop. The predefined fallback controller drives the humanoid to a MRC, defined as a stable standing posture with both feet firmly grounded and both arms raised alongside the body. This configuration provides a generalpurpose, dynamically stable posture that minimizes risk during emergency termination. On the other hand, since safety behaviors are highly context dependent, we restrict our scope to a known task and environment, focusing on the nominal state distribution induced during execution rather than the entire state space. Whether the state is inside the SSE is labeled in large-scale simulation, and an iterative importanceguided refinement strategy concentrates data collection near the predicted boundary between stoppable and non-stoppable states. By strictly targeting these high-uncertainty regions rather than exhaustive exploration, PRISM yields a highly data-efficient demarcation of SSE, enabling reliable sim-toreal deployment. The main contributions of this work are: 

- **Characterization of Safe-stoppability.** We formalize fail-safe safety for humanoid robots as a policydependent stochastic reach-avoid property under a fixed fallback controller for E-stop, and propose a data-driven method to learn the neural safe-stoppability monitor. 

- **Simulation-driven boundary refinement.** We propose an iterative, importance-guided sampling framework that dynamically reallocates sampling density toward in- 

formative boundary regions, improving boundary characterization for the safe-stoppable envelop (SSE). 

- **Sim-to-real validation.** We demonstrate real-world deployment on a Unitree G1 humanoid. Our framework enables efficient and safe verification of predefined fallback policies, making the characterization of the safe-stoppable envelop (SSE) on hardware significantly more practical and scalable. 

By establishing verifiable safe-stop capabilities for bipedal humanoid robots, this work tackles one of the most significant obstacles preventing their adoption in manufacturing environments; demonstrating fail-safe operation that meets stringent industrial safety requirements. 

## II. RELATED WORK 

## _A. Fail-Safe Safety and Minimum Risk Conditions_ 

Fail-safe operation is a foundational principle in safetycritical systems. Upon fault detection, systems are not expected to simply disable actuation; instead, they must transition to a configuration with bounded and acceptable residual risk (e.g., an autonomous vehicle safely pulling over to the roadside). In automotive safety, this requirement is formalized through the concept of _Minimum Risk Condition_ (MRC), defined in standards such as ISO 26262[1] and _Safety Of The Intended Functionality_ (SOTIF) defined by ISO 21448[2]. A similar principle should be applied in humanoid robotics. 

On the other hand, prior work in humanoid control has extensively addressed disturbance rejection and balance recovery, including capture-point methods [3], push recovery [4], step timing adjustment [5], and optimization-based whole-body control for platforms such as Atlas [6]. More recent efforts explore multi-constraint safe control [7] and safety benchmarking toolkits [8]. While these approaches improve robustness and disturbance handling, they do not explicitly characterize the state-dependent region from which a predefined emergency behavior can safely drive the robot to a minimum-risk terminal condition. 

## _B. Reach-Avoid Analysis for Fail-Safe Control_ 

Safety in control theory is often formulated as a _invariance_ problem, where the objective is to keep system trajectories within a safe set using supervisory control. Classical settheoretic approaches characterize maximal controlled invariant sets for constrained systems [9], [10], [11]. 

Fail-safe behavior, however, is inherently a _reachability_ problem: when safety cannot be guaranteed indefinitely, the system must reach a designated safe terminal condition while avoiding failure along the way. Reachability and reachavoid analysis characterize states that can reach a target set while avoiding unsafe regions [12], [13], with stochastic reachability extending these formulations to uncertain systems [14], [15]. While these methods provide strong theoretical guarantees, their computational complexity scales poorly with system dimension, making exact computation impractical for high-dimensional humanoid models. 


Fig. 2. **Data-efficient stoppability monitoring via PRISM.** Exhaustively collecting failure data to learn SSE boundaries on physical humanoids is prohibitively expensive and risks severe hardware damage. To overcome this labeling bottleneck, PRISM dynamically tracks prediction errors and allocates dense sampling to highly uncertain boundary regions (the IS Window). By focusing on critical unstoppable states rather than trivially safe regions, PRISM reduces data requirements while improving boundary characterization. Red dots denote counts, while the shaded background indicates density values. 

Recent work has therefore explored data-driven approximations of reach-avoid sets [16], [17], [18]. In many such approaches, a fixed policy is evaluated by estimating the probability of reaching a goal while avoiding failure, yielding a policy-dependent reach-avoid value function. Our formulation adopts this perspective but introduces iterative importance sampling to concentrate data collection near the predicted stoppability boundary, significantly improving data efficiency. 

## _C. Sim-to-Real Deployment for Humanoid Robots_ 

Simulation has become a standard tool for improving data efficiency in humanoid control. Large-scale parallel simulators [19] enable extensive exploration of robot dynamics and policy behavior without the cost and risk of real-world experimentation. Such simulation-driven pipelines have been widely adopted in humanoid locomotion and whole-body control [20], [21], [22], where policies are trained or evaluated using large numbers of simulated rollouts before deployment on physical systems. However, simulation-based methods must address the sim-to-real gap, arising from mismatches in friction, actuator dynamics, compliance, latency, and other physical effects. A common mitigation strategy is domain randomization, where physical parameters are randomized during simulation to encourage policies that generalize to real-world dynamics [23], [24]. 

In this work, we adopt simulation to efficiently approximate the SSE and train the stoppability monitor. To reduce sim-to-real mismatch, simulation rollouts are initialized using real-robot state logs before executing the fallback controller. This design eliminates discrepancies along the nominal trajectory and confines the remaining gap to fallback execution. The residual mismatch is then mitigated through targeted domain randomization, improving the reliability of the learned monitor during real-world deployment. 

## III. PROBLEM FORMULATION 

This paper studies whether a predefined fallback (E-stop) policy can be safely executed at states in the _nominal state space_ induced by a task policy _π_ nom. 

## _A. System Model_ 

Consider a humanoid robot with state _xt ∈X_ and control input _ut ∈U_ evolving under stochastic dynamics _xt_ +1 = _f_ ( _xt, ut, wt_ ) _,_ where _wt_ captures disturbances, contact uncertainty, and modeling mismatch. 

For a given task, the robot executes a nominal policy _ut_ = _π_ nom( _xt_ ), inducing a nominal state distribution _X_ nom _⊂X_ . 

We define a safe set _X_ safe _⊂X_ encoding admissible conditions such as no falling and no forbidden collisions. A predefined fallback (E-stop) policy _ut_ = _π_ fallback( _xt_ ) is designed to drive the robot toward MRC characterized as a terminal stopping pose _X_ terminal _⊂X_ safe as shown in fig. 1. 

It is assumed that both the nominal policy and the fallback policy are well trained with high success rates if we do not account for complex environmental interaction. 

## _B. Safe-Stoppable Envelop (SSE) and Stoppability Monitor_ 


which represents the probability that the fallback policy successfully reaches the terminal region while avoiding intermediate safety violations, given an instantaneous trigger state _x_ trig sampled during nominal execution. 

For a confidence threshold _α ∈_ (0 _,_ 1], the corresponding _α_ -safe-stoppable set is defined as the level set 


To map the probabilistic outcome _V_ stop( _x_ ) to a deterministic binary classification, we define a state _x ∈X_ as _Stoppable_ if _V_ stop( _x_ ) _≥ α_ , meaning the fallback policy succeeds with probability at least _α_ . Conversely, a state is considered _Unstoppable_ if _V_ stop( _x_ ) _< α_ . The SSE is then directly equivalent to the _α_ -level set _Xπ_<sup>_α_</sup> fallback<sup>. By adjusting the</sup> threshold _α_ , we can recover different levels of robustness for the SSE, effectively controlling the trade-off between safety conservatism and nominal task efficiency. 

The true stoppability function _V_ stop( _x_ ) and SSE are unknown. Our objective is to learn an online neural monitor _V_ ˆstop( _x_ ) to approximate the true stoppability _V_ stop( _x_ ). Specifically, we aim to train this monitor such that: 

- 1) _V_<sup>ˆ</sup> stop( _x_ ) accurately estimates the safe-stop success probability over the nominal state distribution _Xπ_ nom. 

- 2) The monitor maintains high reliability in rare but safety-critical regions, particularly reducing false-safe predictions (unstoppable states classified as stoppable). 

At runtime, the monitor triggers a proactive stop whenever _V_ ˆstop( _x_ ) _< α_ . The threshold _α_ acts as a tunable safety margin that determines the required confidence level. In practice, _α_ can be selected empirically to control the false-safe rate. Even within the nominal state space, two key challenges arise when learning _V_<sup>ˆ</sup> stop( _x_ ). 

_First_ , stoppable and unstoppable states are often highly imbalanced, so uniform data sampling in _X_ nom wastes most samples on easy nominal states and fails to adequately cover the rare boundary states that are most informative for learning. 

_Second_ , stoppability labels are expensive to obtain. Unlike standard safety events such as collisions or falls, which can be checked instantaneously, stoppability must be determined by executing the full fallback policy from a given state. On physical hardware, this is especially inefficient because the robot cannot generally be reset directly to arbitrary intermediate states, so each queried state must first be reached through rollout. 

To address _imbalance_ , we develop the iterative importance sampling scheme in Section V, which focuses data collection on informative states using the monitor learned in the previous iteration. To address _labeling cost_ , we use simulation as a state replay engine in Section IV, allowing direct initialization at queried states before fallback execution. The former improves where data are sampled; the latter reduces the cost of labeling each sampled state. 

## IV. SIMULATION-BASED STOPPABILITY ESTIMATION 

## _A. Efficient Safe-Stop Outcome Labeling_ 

We generate binary supervisory labels via simulated rollouts of _π_ fallback. Specifically, we sample instantaneous trigger states, denoted as _x_ trig, from a nominal trajectory distribution _q_ ( _x_ ) (initially approximating _Xπ_ nom), execute the fallback policy _π_ fallback for a maximum horizon _T_ max, and assign the 

label. 


Fundamentally, the outcome of any single fallback rollout is a stochastic realization _y ∈{_ 0 _,_ 1 _}_ , drawn from a Bernoulli distribution parameterized by the true safety probability: _y ∼_ Bernoulli( _V_ stop( _x_ )). Although each training sample provides only a deterministic binary label, optimizing the neural network via a binary cross-entropy objective drives the model to recover the conditional expectation E[ _y|x_ ]. Consequently, the optimal predictor converges precisely to the true probability Pr( _y_ = 1 _|x_ ) = _V_ stop( _x_ ). This statistical equivalence mathematically bridges the conceptual gap between single-rollout deterministic labels and stochastic reachability. 

## _B. Learning the Stoppability Monitor_ 

Given the dataset _D_ = _{_ ( _x_<sup>_i_</sup> _t_<sup>_, y_</sup> _t_<sup>_i_)</sup><sup>_}t_</sup> _t_<sup>=</sup> =0<sup>_T_</sup> _,i_<sup>_i,i_</sup> =1<sup>=</sup><sup>_N_,wetrain</sup> the _θ_ -parameterized neural network monitor _V_<sup>ˆ</sup> stop( _x_ ; _θ_ ) by minimizing a weighted binary cross-entropy loss 


where _ω_ ( _·_ ) addresses class imbalance and _ℓ_ ( _·, ·_ ) is the crossentropy loss. _Ts_<sup>_i_denotethespecificsubsetofsampledtime</sup> steps for the _i_ -th trajectory. At runtime, the monitor produces a scalar estimate _V_<sup>ˆ</sup> stop( _x_ ) and a binary stoppability decision: 


During robust nominal execution, catastrophic failures under the fallback policy are inherently rare, as the system state predominantly resides within SSE. Uniformly sampling states _x ∈X_ nom therefore produces predominantly successful rollouts, yielding limited information about the boundary of SSE. This severe class imbalance makes accurate learning of a stoppability monitor particularly challenging. 

A na¨ıve strategy would continually augment the dataset with additional nominal trajectories and corresponding safestop labels. However, this approach is highly data-inefficient: most nominal states are trivially stoppable and contribute little new information, while only a small subset of boundary or contact-critical states are informative. 

To overcome these limitations, we adopt a progressive refinement strategy that simultaneously (i) expands nominal state coverage across iterations and (ii) concentrates labeling effort on regions where the current monitor exhibits systematic error. Instead of balancing data post hoc, PRISM performs importance-guided resampling that prioritizes SSE boundary-proximal or high-uncertainty states. Because identifying such states requires a trained model, the framework alternates between monitor training and targeted resampling, yielding an iterative boundary-refinement procedure. 

**Algorithm 1** PRISM: **P** roactive **R** efinement of **I** mportancesampled **S** toppability **M** onitors 

- 1: Collect _N_ 0 nominal trajectories under _π_ nom from initial state set _X_ 0. 

- 2: Uniformly sample states and label via _π_ fallback rollouts. 3: Train initial monitor _V_<sup>ˆ(0)</sup> stop<sup>.</sup> 

- 4: Initialize dataset _D_<sup>(0)</sup> and validation set _D_ val. 

- 5: **for** _k_ = 0 _,_ 1 _, . . . , K −_ 1 **do** 

- 6: Generate new nominal trajectories with _π_ nom from _X_ 0 inducing _p_<sup>(</sup> nom<sup>_k_)(</sup><sup>_x_).</sup> 

- 7: Compute residuals on validation set: 


- 12: **for** each sampled state _x_ **do** 

- 13: Roll out safe-stop under _π_ fallback and obtain label _y_ . 

- 14: Add ( _x, y_ ) to _D_<sup>(</sup><sup>_k_+1)</sup> . 15: **end for** 16: Retrain monitor _V_<sup>ˆ(</sup><sup>_k_+1)</sup> with _D_<sup>(</sup><sup>_k_+1)</sup> . stop 

- 17: **end for** 18: **return** _V_<sup>ˆ(</sup><sup>_K_)</sup> stop<sup>.</sup> 

## _A. Initial Dataset Construction_ 

We begin by collecting _N_ 0 nominal trajectories under the nominal task policy _π_ nom, inducing a state distribution _p_<sup>(0)</sup> nom<sup>(</sup><sup>_x_). States are uniformly sampled along the time dimen-</sup> sion and labeled via e-stop rollouts under _π_ fallback, yielding an initial dataset _D_<sup>(0)</sup> = _{_ ( _x_<sup>_i_</sup> _t_<sup>_, y_</sup> _t_<sup>_i_)</sup><sup>_}t_</sup> _t_<sup>=</sup> =0<sup>_T_</sup> _,i_<sup>_i,i_</sup> =1<sup>=</sup><sup>_N−_0</sup> . We train the initial stoppability monitor _V_<sup>ˆ</sup> stop<sup>(0)on</sup><sup>_D_(0).</sup> 

## _B. Data Refinement via Importance Sampling_ 

At iteration _k_ , we generate a new batch of nominal trajectories (fixed number _NI_ ), inducing distribution _p_<sup>(</sup> nom<sup>_k_)(</sup><sup>_x_).To</sup> identify informative regions, we maintain a fixed validation set _D_ val = _{_ ( _x_<sup>_i_</sup> _t_<sup>_, y_</sup> _t_<sup>_ii_)</sup><sup>_}t_</sup> _t_<sup>=</sup> =0<sup>_T_</sup> _,i_<sup>_i,i_</sup> =1<sup>=</sup><sup>_N_val</sup> to compute the residuals of the current monitor: _ri_<sup>(</sup><sup>_k_)</sup> = _ℓ_ � _x_<sup>_i_</sup> _, y_<sup>_i_�</sup> _,_ ( _x_<sup>_i_</sup> _, y_<sup>_i_</sup> ) _∈D_ val (for simplicity, we use _x_<sup>_i_</sup> _, y_<sup>_i_</sup> to denote the _i_ -th trajectory and its corresponding labels; see eq. (4)). Let _q_ 1<sup>(</sup><sup>_k_</sup> _−_<sup>)</sup> _δ_<sup>denotethe</sup> empirical (1 _− δ_ ) quantile of _{ri_<sup>(</sup><sup>_k_)</sup> _}_ . Inspired by conformal prediction [25], [26], this quantile provides a finite-sample calibration threshold to define the importance region as: 


Intuitively, _T_<sup>(</sup><sup>_k_)</sup> captures states where the monitor’s prediction error exceeds the calibrated tolerance level, focusing refinement on systematically mispredicted regions. 

Then, We define the importance-refined distribution and the effective sampling distribution at iteration _k_ as follows: 


where _β ∈_ [0 _,_ 1) balances global coverage and boundary refinement. 

In practice, sampling from this high-dimensional mixture _p_<sup>(</sup> mix<sup>_k_)isphysicallyinstantiatedbydynamicallyadjusting</sup> the temporal stride along each newly collected nominal trajectory. Specifically, we construct the trajectory-specific index set _Ts_<sup>_i_(introducedineq.(4))byapplyingadense</sup> temporal sampling stride to segments where states enter the importance region, and a sparse uniform stride elsewhere. 

The aggregated training buffer is then updated as _D_<sup>(</sup><sup>_k_+1)</sup> = _D_<sup>(</sup><sup>_k_)</sup> _∪D_ imp<sup>(</sup><sup>_k_).Themonitor</sup><sup>_V_ˆ</sup> stop<sup>(</sup><sup>_k_+1)</sup> is subsequently retrained on _D_<sup>(</sup><sup>_k_+1)</sup> . This iterative process progressively expands nominal coverage while concentrating sample density near the critical stoppability boundary, as summarized in Algorithm 1. 

## VI. EXPERIMENTS 

## _A. System Setup._ 

Experiments are conducted on the 29-DoF Unitree G1 humanoid performing a fixed loco-manipulation task: grasping an object from a MagneMotion Conveyor cart, navigating to a designated area, and releasing it. The nominal controller _π_ nom is a pretrained whole-body policy executing in closedloop via onboard proprioception and a three-camera global localization system. The safe set _X_ safe includes states where the robot is balanced, collision free, and meets joint-limit constraints. Its subset, the terminal MRC _X_ terminal _⊂X_ safe, designates a predefined upright stance with both arms in a default posture. We train the task policy _π_ nom to perform loco-manipulation in the task area; and the task-agnostic fallback policy _π_ fallback to drive the robot toward _X_ terminal from arbitrary initial states without considering environmental interaction (hence having no knowledge of the task-dependent _X_ safe). 

## _B. Data Collection._ 

Stoppability labeling is conducted in the SPARK simulator [8] using the identical nominal and fallback policies. During real-world trials, which are monitored and reconstructed via an Apple Vision Pro AR headset, we record proprioceptive and global camera states. These states are subsequently replayed in simulation to execute importance-guided E-stop rollouts. The rollouts yield binary labels: Unsafe if any collision occurs or the robot falls down, and Safe if the robot reaches the terminal set without incident. We collect 40 real-world trajectories and 400 simulated seeds, which are used to generate safety labels and to train the models for real-world and simulation experiments, respectively. For simulation evaluation, we use single rollouts for labeling, as Unsafe labels in our task typically occur when the lower body remains stationary while the upper body collides during 


Fig. 3. **Experimental platforms used** : ( **Left** ) Real humanoid deployment. ( **Middle** ) AR based of data collection. ( **Right** ) Simulation-based fallback policy rollouts. AR-based data collection improves safety during real-robot experiments by projecting the virtual environment onto the real robot, enabling realistic data collection while performing collision checking in simulation to avoid physical collisions. 

TABLE I 

PROGRESSIVE STOPPABILITY MONITOR REFINEMENT (SIM). 

|**Sampling**|**Iter**|**Total**<br>|**Unsafe**<br>|**Num.**<br>|**Pred A**<br>|**cc.** (%) _↑_<br>|
|---|---|---|---|---|---|---|
|||**Data**|**Ratio**|**Traj.**|**Safe**|**Unsafe**|
|_- Importance _|_Samp_|_ling (PRIS_|_M)_||||
||0|715|29_._7%<br>|3|93_._8|70_._0|
||1|1127|28_._4%|6|92_._7|72_._3|
|PRISM|5|2754|27_._6%<br>|18|92_._9|74_._2|
||9|4332|26_._9%<br>|30|93_._2|73_._5|
||13|5801|27_._3%|42|95_._0|77_._2|
||17|7339|27_._4%|54|94_._3|87_._9|
|_- Full-Buffer _|_Unifo_|_rm Trainin_|_g_||||
|30 Traj.|–|7212|28_._2%|30|96_._4|78_._3|
|54 Traj.|–|12564|28_._7%|54|94_._8|89_._2|


Fig. 4. **Safety score over a full loco-manipulation trajectory.** The monitor exhibits precise temporal alignment with the ground truth and identifies elevated risks during manipulation phases ( _Pick_ , _Place_ ) while ensuring high confidence during steady-state locomotion ( _Transfer_ , _Leave_ ). 

the safe stop, resulting in quite deterministic labels even under domain randomization. 

## _C. Data-Efficient Iterative Monitor Learning_ 

In our importance sampling setting, the PRISM is initialized with _N_ 0 = 3 trajectories, Then, _NI_ = 3 more novel trajectories are incorporated per iteration. Critical boundary regions identified by importance weights are sampled densely ( _fine stride_ ), whereas trivial safe regions are sampled sparsely ( _coarse stride_ ). 

We benchmark PRISM against two full-buffer uniform training baselines (Table I). The 30-trajectory baseline matches the strict data volume of PRISM at Iteration 17, while the 54-trajectory baseline matches PRISM’s total trajectory exposure. In Table I, under an equivalent data budget (30-Traj baseline), PRISM improves the prediction accuracy for critical unsafe states. Furthermore, PRISM achieves comparable performance with the 54-trajectory baseline, yet reduces the total data collection footprint by over 40%. This clearly demonstrates PRISM’s capability to disentangle monitor accuracy from sheer data volume. 

## _D. Qualitative Study_ 

**Safety Confidence Profiling.** Figure 4 visualizes the continuous output logits of the trained stoppability monitor _V_ ˆsafe across a complete _∼_ 7500-step nominal trajectory. During steady-state walking (e.g., _Transfer_ , _Leave_ ), the confidence heavily fluctuates in the deep negative (Safe) 


Fig. 5. **Spatial projection of the stoppability boundaries.** For both (a) Real-World and (b) Simulation, the scatter plots (left panels) display the Cartesian ( _x, y_ ) state distributions colored by ground-truth labels. The contour maps (right panels) illustrate the interpolated predictive safety regions overlaid with state density. 

region, reflecting the high stability margin of the nominal limit cycle. Conversely, severe probability spikes into the positive (Unsafe) domain correlate precisely with the _Pick_ and _Place_ phases. Our monitor successfully captures these complex, state-dependent dynamic vulnerabilities. 

**Spatial State-Space Profiling.** Complementary to the temporal analysis, Figure 5 visualizes the spatial distribution of the monitor’s predictions using 2D Cartesian coordination ( _x, y_ ). Crucially, the contour density maps demonstrate that the decision boundaries (the red/blue interfaces) in both the real-world deployment and the simulation environment 

TABLE II 

TABLE III 

SINGLE-FACTOR DOMAIN RANDOMIZATION ABLATION (SIM). 

|**DRID**|**Perturbation**|**Test**<br>|**Unsafe**<br>|**Pred A**<br>|**cc.** (%) _↑_<br>|
|---|---|---|---|---|---|
|||**Data**|**Ratio**|**Safe**|**Unsafe**|
|_- Default _|_Configuration_|||||
|Default|None|8428|30.5|91.9|88.8|
|_- Single-F_|_actor Variations_|||||
|0|Damping _↓_|7995|30_._1%|92_._0|88_._2|
|1|Damping _↑_|7998|30_._1%|92_._0|88_._2|
|2|Gains _↓_|7998|30_._2%|92_._1|88_._0|
|3|Gains _↑_|8004|30_._3%|92_._2|88_._0|
|4|Friction _↓_|8021|30_._7%|92_._0|86_._5|
|5|Friction _↑_|8383|36_._8%|91_._5|74_._7|


exhibit highly consistent topological structures. This structural isomorphism strongly validates the monitor’s sim-toreal transferability and its physical grounding in identifying spatially-induced failures. 

ABLATION ANALYSIS OF STRIDE VARIATION SENSITIVITY (SIM). 

|**MthdID**|**Strid**|**Train**|**Unsafe**|**Pred Ac**|**c.** (%) _↑_|
|---|---|---|---|---|---|
|**eo **|**e**|**Data**|**Ratio**|**Safe**|**Unsafe**|
|_- Stride Varia_|_tions (Bal_|_anced Tra_|_ining)_|||
|0|60|2624|50_._0%|91_._00|82_._45|
|1|50|3130|50_._0%|92_._16|81_._79|
|2|40|3866|50_._0%|91_._57|79_._81|
|3|30|5334|50_._0%|92_._20|84_._63|
|4|20|7864|50_._0%|**92**_._**35**|**84**_._**55**|


TABLE IV 

ABLATION ANALYSIS OF DECISION THRESHOLD _α_ (SIM). 

|**Param** _α_|**Pred A**|**cc.** (%) _↑_|**Param** _α_|**Pred A**|**cc.** (%) _↑_|
|---|---|---|---|---|---|
||**Safe**|**Unsafe**||**Safe**|**Unsafe**|
|0_._47|62_._05|99_._38|0_._53|93_._58|94_._05|
|0_._49|78_._56|98_._44|0_._55|96_._82|89_._14|
|0_._51|88_._32|96_._46|0_._57|98_._86|81_._52|


## _E. Robustness to Dynamics Perturbations_ 

Table II evaluates the zero-shot generalization of a single monitor (trained on 40 nominal trajectories) against domain randomizations. Joint damping and geometry friction are randomized within [0 _._ 5 _,_ 1 _._ 6] and [0 _._ 4 _,_ 2 _._ 0] (default [0 _._ 7 _,_ 1 _._ 3]). Motor gains are tested under _kp ∈_ [0 _._ 75 _,_ 1 _._ 25] _, kd ∈_ [0 _._ 85 _,_ 1 _._ 15] and _kp ∈_ [0 _._ 6 _,_ 1 _._ 4] _, kd ∈_ [0 _._ 75 _,_ 1 _._ 25], with default _kp, kd ∈_ [0 _._ 8 _,_ 1 _._ 2]. The monitor remains highly robust to internal joint parameters (damping and PD gains). Theoretically, these variations merely alter high-frequency transient control responses without fundamentally distorting the global wholebody kinematic envelope. 

Conversely, the monitor is notably sensitive to external ground friction. Dynamically, excessively high friction prevents natural kinetic energy dissipation via micro-slipping. Consequently, the aggressive deceleration induced by _π_ fallback abruptly converts linear momentum into angular tipping momentum around the foot edges. These novel tripping failure modes act as out-of-distribution (OOD) states. 

## _F. Sample Stride Sensitivity_ 

To investigate the inherent trade-off between temporal sampling resolution and data collection cost, we perform an ablation study on the trigger stride using a class-balanced dataset (Table III). As intuitively expected, decreasing the temporal stride yields denser state coverage, which steadily improves the overall prediction accuracy. Notably, the denser sampling also reduces false-safe errors by improving coverage near the stoppability boundary. However, this accuracy improvement incurs a steep empirical cost, proportionally inflating the expensive data collection time. This fundamental conflict between blanket dense sampling and hardware safety directly substantiates the necessity of our PRISM framework. 

## _G. Effect of Threshold Margin α_ 

To investigate the inherent trade-off between operational conservatism and task efficiency, we perform an ablation 

study on the decision threshold _α_ (Table IV, we used stride10 sampling and balanced the Unsafe and Safe labels.). As empirically demonstrated, tuning _α_ directly governs the monitor’s bias towards safety versus nominal utility. A lower threshold yields a highly conservative monitor, drastically elevating the Unsafe prediction accuracy to 99 _._ 73%. However, this extreme safety margin incurs a utility penalty. 

## _H. Real-World Experiments_ 

To validate empirical efficacy and sample efficiency, we evaluate the trained monitor on the physical Unitree G1 humanoid using a hold-out test set of 5 unseen nominal trajectories. In safety-critical hardware deployments, the cost of a false negative exponentially outweighs a false positive. Notably, PRISM inherently learns a more conservative decision boundary, reflected by a lower Safe accuracy (70 _._ 0%). Given the severe asymmetric penalty between false alarms and hardware destruction, this conservative prediction margin is highly desirable for physical robotic systems, definitively validating PRISM’s capacity to maximize operational safety while minimizing hazardous real-world data collection. 

## VII. DISCUSSION 

**Safety Integrity Level Analysis.** To assess deployment readiness against industrial benchmarks, we evaluate our framework’s performance contextually within Safety Integrity Levels (SIL). By strategically tuning the decision threshold _α_ to enforce a conservative safety bias, the monitor consistently elevates the prediction accuracy of critical Unsafe states above 99% (e.g., see _α_ = 0 _._ 47 in table IV). In the domain of functional safety, an automated hazard detection and intervention reliability exceeding 99% fundamentally satisfies the stringent risk-reduction requirements of SIL 2. Consequently, our tunable safe-stoppability monitor can fullfill the rigorous prerequisites essential for the practical production and real-world deployment of bipedal humanoids. 

TABLE V 

PROGRESSIVE STOPPABILITY MONITOR REFINEMENT (REAL). 

|**Sampling**|**Iter**|**Total**<br>**Data**|**Unsafe**<br>**Ratio**|**Num.**<br>**Traj.**|**Pred **<br>**Safe**|**Acc.** (%) _↑_<br>**Unsafe**|
|---|---|---|---|---|---|---|
|_- Importance _|_Samp_|_ling (PRI_|_SM)_||||
|PRISM|11|4099|35_._3%|33|70_._0|**94**_._**1**|
|_- Full-Buffer _|_Unifo_|_rm Traini_|_ng_<br>||||
|20 Traj.|–|4169|34_._9%|20|82_._2|88_._7|
|33 Traj.|–|6820|35_._1%|33|77_._3|93_._3|


**Sim-to-Real Considerations.** Two sources of sim-to-real discrepancy arise: (1) the distribution gap of triggering states and (2) dynamics mismatch during fallback execution. The first is mitigated by collecting nominal trajectories on the real robot to initialize fallback rollouts in simulation, ensuring realistic triggering states. The second is mitigated by domain randomization during fallback rollouts in simulation. These enable robust approximation of the safe-stoppable envelope (SSE). Finally, the decision threshold _α_ can be tuned to adjust the conservatism of the learned SSE, helping to compensate for residual sim-to-real mismatch introduced by domain randomization. 

**Limitations.** The approach depends on the fidelity of simulation and the representativeness of sampled scenarios. Conservative thresholding improves safety at the cost of frequent interventions. Future work includes integrating monitor outputs into runtime switching logic and extending the method to multi-stage emergency behaviors. 

## VIII. CONCLUSION 

We presented a simulation-driven framework for fail-safe safety in humanoid robots by modeling safety as policydependent stoppability under a predefined safe-stop controller. We learn a neural monitor from large-scale simulation labels and introduced an iterative importance sampling strategy to refine performance in safety-critical failure regions. Experiments across humanoid scenarios demonstrate improved failure-case prediction and reduced false-safe errors under a fixed simulation budget. 

Beyond monitoring, the characterized safe-stoppable envelope naturally enables a closed-loop improvement process. Insights from identified failure modes and boundary states can be used to systematically refine the fallback controller, progressively enlarging the safe-stoppable, and therefore operational envelope. Such iterative co-design between monitoring and control holds significant promise for scalable industrial deployment, and will be explored in future work. In addition, for states that currently lie outside the safe-stoppable envelop, one may design secondary recovery policies that first steer the system back into the envelope before executing the stop. This layered fallback architecture offers a principled pathway toward broader recoverability and enhanced runtime safety. 

## ACKNOWLEDGMENT 

This project was supported in part by Siemens and in part by the National Science Foundation under Grant 

## No. 2144489. 

## REFERENCES 

- [1] ISO, “Road vehicles – functional safety,” International Organization for Standardization, Geneva, Switzerland, Tech. Rep. ISO 26262:2018, 2018. [Online]. Available: https://www.iso.org/standard/68383.html 

- [2] “Road vehicles — safety of the intended functionality,” International Organization for Standardization, Geneva, CH, Standard ISO 21448:2022, 06 2022. [Online]. Available: https://www.iso.org/ standard/77490.html 

- [3] J. Pratt, J. Carff, S. Drakunov, and A. Goswami, “Capture point: A step toward humanoid push recovery,” in _2006 6th IEEE-RAS international conference on humanoid robots_ . Ieee, 2006, pp. 200–207. 

- [4] B. Stephens, _Push recovery control for force-controlled humanoid robots_ . Carnegie Mellon University, 2011. 

- [5] R. J. Griffin, G. Wiedebach, S. Bertrand, A. Leonessa, and J. Pratt, “Walking stabilization using step timing and location adjustment on the humanoid robot, atlas,” in _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2017, pp. 667–673. 

- [6] S. Feng, E. Whitman, X. Xinjilefu, and C. G. Atkeson, “Optimization based full body control for the atlas robot,” in _2014 IEEE-RAS International Conference on Humanoid Robots_ . IEEE, 2014, pp. 120–127. 

- [7] R. Chen, Y. Sun, and C. Liu, “Dexterous safe control for humanoids in cluttered environments via projected safe set algorithm,” _arXiv preprint arXiv:2502.02858_ , 2025. 

- [8] Y. Sun, R. Chen, K. S. Yun, Y. Fang, S. Jung, F. Li, B. Li, W. Zhao, and C. Liu, “SPARK: Safe protective and assistive robot kit,” in _IFAC Symposium on Robotics_ , 2025. [Online]. Available: https://intelligent-control-lab.github.io/spark/ 

- [9] F. Blanchini, “Set invariance in control,” _Automatica_ , vol. 35, no. 11, pp. 1747–1767, 1999. 

- [10] C. Liu and M. Tomizuka, “Control in a safe set: Addressing safety in human-robot interactions,” in _2014 ASME Dynamic Systems and Control Conference_ . ASME, 2014. 

- [11] A. D. Ames, S. Coogan, M. Egerstedt, G. Notomista, K. Sreenath, and P. Tabuada, “Control barrier functions: Theory and applications,” in _2019 18th European control conference (ECC)_ . IEEE, 2019, pp. 3420–3431. 

- [12] I. M. Mitchell, A. M. Bayen, and C. J. Tomlin, “A time-dependent hamilton-jacobi formulation of reachable sets for continuous dynamic games,” _IEEE Transactions on automatic control_ , vol. 50, no. 7, pp. 947–957, 2005. 

- [13] J. F. Fisac, M. Chen, C. J. Tomlin, and S. S. Sastry, “Reach-avoid problems with time-varying dynamics, targets and constraints,” in _Proceedings of the 18th international conference on hybrid systems: computation and control_ , 2015, pp. 11–20. 

- [14] S. E. Z. Soudjani and A. Abate, “Probabilistic reach-avoid computation for partially degenerate stochastic processes,” _IEEE Transactions on Automatic Control_ , vol. 59, no. 2, pp. 528–534, 2013. 

- [15] M. Prandini and J. Hu, “Stochastic reachability: Theory and numerical approximation,” _Stochastic hybrid systems, Automation and Control Engineering Series_ , vol. 24, pp. 107–138, 2006. 

- [16] J. F. Fisac, A. K. Akametalu, M. N. Zeilinger, S. Kaynama, J. Gillula, and C. J. Tomlin, “A general safety framework for learning-based control in uncertain robotic systems,” _IEEE Transactions on Automatic Control_ , vol. 64, no. 7, pp. 2737–2752, 2018. 

- [17] K. Nakamura, L. Peters, and A. Bajcsy, “Generalizing safety beyond collision-avoidance via latent-space reachability analysis,” _arXiv preprint arXiv:2502.00935_ , 2025. 

- [18] R. Pandya, C. Liu, and A. Bajcsy, “Robots that learn to safely influence via prediction-informed reach-avoid dynamic games,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 14 330–14 337. 

- [19] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [20] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [21] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [22] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu, “Twist2: Scalable, portable, and holistic humanoid data collection system,” _arXiv preprint arXiv:2511.02832_ , 2025. 

- [23] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel, “Domain randomization for transferring deep neural networks from simulation to the real world,” in _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ . IEEE, 2017, pp. 23–30. 

- [24] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Sim-toreal transfer of robotic control with dynamics randomization,” in _2018 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2018, pp. 3803–3810. 

- [25] G. Shafer and V. Vovk, “A tutorial on conformal prediction.” _Journal of machine learning research_ , vol. 9, no. 3, 2008. 

- [26] Y. Pan, Y. Xu, Z. Liu, and H. Wang, “Seeing through uncertainty: Robust task-oriented optimization in visual navigation,” _arXiv preprint arXiv:2510.00441_ , 2025. 

