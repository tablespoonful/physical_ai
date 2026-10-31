---
title: "CSymPlan: Certified Symbolic Planning and Control for High-DOF Manipulators"
date: "2026-08-24"
authors: "Aditya Narendra; Ashok Kumar Saini; Mahathi Anand; Mahmoud Khaled; Fares J. Abu-Dakka; Abdalla Swikir"
url: https://arxiv.org/abs/2608.22983
pdf: https://arxiv.org/pdf/2608.22983
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2608.22983)** / [論文ページ](https://arxiv.org/abs/2608.22983)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# CSymPlan: Certified Symbolic Planning and Control for High-DOF Manipulators 

Aditya Narendra<sup>_∗_</sup> , Ashok Kumar Saini<sup>_∗_</sup> , Mahathi Anand<sup>_†_</sup> , Mahmoud Khaled<sup>_‡_</sup> , 

Fares J. Abu-Dakka<sup>_§_</sup> , and Abdalla Swikir<sup>_∗_</sup> 

_∗_ Mohamed bin Zayed University of Artificial Intelligence (MBZUAI), Abu Dhabi, United Arab Emirates 

_†_ Learning Systems and Robotics Lab, Technical University of Munich, Germany 

_‡_ Ludwig Maximilian University of Munich, Munich, Germany 

_§_ New York University Abu Dhabi, Abu Dhabi, United Arab Emirates 

Corresponding author: Aditya Narendra (aditya.narendra@mbzuai.ac.ae) 

**_Abstract_ —Robot manipulators are commonly engineered around a decoupled motion-generation stack: a planner computes a collision-free path and a lower-level controller tracks the resulting reference. This separation is computationally convenient, but it can produce references that are difficult to execute under actuator limits, tracking error, model mismatch, and small obstacle clearances. We present CSymPlan, a certified symbolic planning and control framework for high-DOF manipulators with two complementary implementations: an offline implementation that precomputes certified reach-avoid feedback policies for known workspaces; and an online implementation that synthesizes or updates symbolic policies at runtime from changing task and perception information using parallelization. The offline implementation reduces the manipulator dynamics to a sampled perturbed double-integrator model in operational space through feedback linearization, treats torque-realization errors, modeling inaccuracies, and measurement uncertainty as bounded disturbances, and refines the synthesized symbolic policy to the Franka FR3 through a quantization–lookup–torque realization pipeline. The online implementation uses the same abstraction and refinement interface, but replaces the precomputed policy table with a runtime pFaces request–synthesis–execution loop. In randomized simulated benchmarks and perception-driven Franka FR3 experiments, both implementations complete reach-avoid tasks with zero safety violations; whenever no certified action exists, the robot holds, replans, or stops safely instead of executing an uncertified command.** 

**_Index Terms_ —Symbolic control, reach-avoid control, robot manipulation, formal methods, motion planning, high-DOF manipulators.** 

## I. INTRODUCTION 

Precise motion generation for robot manipulators [1] is central to applications ranging from industrial pick-and-place to human–robot interaction and other safety-critical manipulation settings [2]. Conventional architectures separate motion generation into two layers. A high-level planner first generates a geometric path or reference trajectory [3]; a low-level feedback controller then attempts to track that reference on the physical robot [4]. Although this modular design has been successful in practice, it also creates a gap between planning and execution. A path that is collision-free in the planner may become unsafe after tracking errors, actuator saturation, unmodeled dynamics, or sensing errors are introduced at runtime. 

This gap is most visible in cluttered environments, where the clearance around obstacles can be comparable to the tracking 

error of the manipulator. In such settings, a geometric planner may return a feasible-looking path that is dynamically difficult to track, while a controller may stabilize the robot locally without guaranteeing that all future closed-loop states remain inside a safe set. Recent integrated planning-and-control approaches, including kinodynamic planning, model predictive control, model predictive path integral control, and reinforcementlearning-based controllers, reduce this mismatch by considering dynamics during decision making [5–10]. However, these methods often rely on local optimization, stochastic sampling, learned approximations, or computationally intensive online operations; most do not provide a direct closed-loop reach-avoid certificate for the executed manipulator trajectory [11–14]. 

To close this gap, we propose CSymPlan, which is, to the best of our knowledge, the first unified symbolic planning-andcontrol framework for high-DOF manipulators demonstrated on torque-controlled hardware. Here, the word symbolic is used in the control-theoretic sense: symbols denote finitely many discretized cells of continuous state and input spaces. Consequently, rather than synthesizing a purely geometric path, CSymPlan constructs a finite-state abstraction of the task-space closed-loop dynamics and synthesizes a feedback policy that satisfies reachability and safety specifications by construction. The synthesized policy maps each abstract/symbolic state to one or more admissible control inputs whose successors remain inside the certified winning set. 

The main technical challenge is scalability. A direct abstraction of a 7-DOF manipulator in joint position and velocity space is not tractable with uniform discretization. CSymPlan avoids this bottleneck by abstracting the translational endeffector dynamics in operational space. Through task-space feedback linearization, the manipulator is represented as a sampled perturbed double integrator in position and velocity. The abstraction explicitly incorporates bounded disturbances and measurement uncertainty. The resulting symbolic action is interpreted as a virtual Cartesian acceleration and refined to joint torques through an operational-space torque controller with null-space damping and posture regulation. 

A policy synthesized offline is, however, bound to the workspace, obstacle set, and goal for which it was computed: any change invalidates the certificate, so offline synthesis 

1 


Figure 1. Overview of CSymPlan. The offline implementation synthesizes a certified reach-avoid policy from a finite abstraction of sampled perturbed task-space dynamics and executes it through a quantization–lookup–torque pipeline. The online implementation uses the same abstraction and torque-realization interface, but calls pFaces online mode at runtime to synthesize or refresh the symbolic policy for the current target and obstacle sets. 

suits static, known workspaces but not tasks whose goals arrive at runtime or whose obstacles are perceived during execution. Moving synthesis into the control loop raises three challenges: fixed-point synthesis is orders of magnitude slower than the 1 kHz servo rate; a certificate holds only for the state, safe set, and horizon for which it was computed, so certified commands become stale as the robot and environment evolve; and rebuilding the abstraction at every replanning instant is intractable. How the online implementation meets these challenges is summarized in the contributions below and detailed in Section V-B. Figure 1 summarizes the full offline–online pipeline. 

The contributions of this paper are organized around two implementations of the same certified planning-and-control principle. 

- 1) **Task-space abstraction for high-DOF arms.** We reduce a high-dimensional manipulator to a tractable Cartesian double-integrator abstraction using operational-space feedback linearization, while retaining a torque-level refinement layer for execution on a Franka FR3. 

- 2) **Offline certified symbolic synthesis for manipulation.** We formulate manipulation reach-avoid tasks as symbolic 

feedback synthesis problems over sampled perturbed taskspace dynamics, yielding correct-by-construction policies under explicit disturbance and measurement bounds. 

- 3) **Real-time execution of precomputed policies.** We implement a quantization–lookup–torque pipeline that executes the offline-synthesized policy at the robot servo rate and demonstrate hardware operation on reach-avoid manipulation tasks. 

- 4) **Online symbolic planning and control.** We extend the framework to runtime-changing tasks and perception-driven obstacle sets: the grids and transition relation are fixed once, finite-horizon reach-avoid winning sets are recomputed on demand by parallelized synthesis (pFaces [15]), and the robot executes buffered certified acceleration commands, with stale-command rejection, through the same torquerealization layer. 

- 5) **Simulation and hardware evaluation protocol.** We define PyBullet and Isaac Sim [16] reach-avoid benchmarks and real Franka FR3 experiments used to evaluate success rate, safety violations, safe resolution, time-to-goal, path length, smoothness, effort, and online synthesis time against planning, receding-horizon, safety-filter, and learned baselines. 

2 

Figure 1 summarizes the full offline–online CSymPlan pipeline. 

## II. RELATED WORK 

## _A. Geometric and sampling-based planning_ 

Classical graph-search planners such as A<sup>_⋆_</sup> and Dijkstra’s algorithm operate on discrete representations of the environment and provide useful completeness properties on the chosen graph [17]. Sampling-based planners, including rapidly-exploring random trees and probabilistic roadmaps, extend motion planning to high-dimensional spaces by searching continuous configuration spaces through samples [18, 19]. These methods are practical and often effective for kinematic planning, but they typically return paths rather than closed-loop controllers. If the robot cannot track the planned path with sufficient accuracy, the execution may violate safety constraints despite the geometric validity of the reference. 

## _B. Kinodynamic and optimization-based planning_ 

Kinodynamic and optimization-based planners reduce the gap between planning and execution by incorporating system dynamics, actuator constraints, or trajectory regularity directly into motion generation [5, 20]. Receding-horizon methods such as model predictive control (MPC) repeatedly optimize a finitehorizon control problem from the current state and commonly use a reference trajectory or target state in the objective, thereby combining trajectory tracking with online constraintaware control [21, 22]. Model predictive path integral (MPPI) control similarly computes receding-horizon actions online, but uses stochastic trajectory sampling and cost-weighted updates rather than deterministic numerical optimization [7]. These feedback formulations can respond to disturbances and model deviations more naturally than a strictly decoupled plan–then– track pipeline. 

Reinforcement-learning-based controllers and neural approximations of MPC can further reduce online computation or improve performance for task distributions encountered during training [23]. However, the guarantees provided by these methods depend strongly on their particular formulation. Nominal finite-horizon MPC, for example, does not by itself imply recursive feasibility or closed-loop constraint satisfaction under bounded disturbances; such guarantees generally require additional ingredients such as robust invariant sets, terminal constraints or costs, constraint tightening, or robust/tube MPC constructions [6, 24]. Likewise, the sampling procedure in MPPI provides an approximate solution to a stochastic finitehorizon optimal-control problem rather than an exhaustive verification of all possible successors from a region of the state space [7]. Learned controllers inherit no formal reachavoid guarantee solely from training performance unless an additional verification or certified safety mechanism is introduced. Consequently, while these approaches can provide excellent empirical closed-loop performance, their standard formulations do not directly produce the type of set-wise reachavoid certificate considered here: a feedback policy for which every admissible successor, for every state represented by a 

certified abstract cell and every disturbance within a prescribed bound, is guaranteed to remain safe and eventually reach the goal. 

## _C. Symbolic control_ 

Symbolic control constructs finite transition systems that over-approximate continuous or hybrid dynamics and synthesizes controllers for temporal, reachability, or safety specifications [11, 25]. Feedback refinement relations connect the abstract and concrete systems so that, under a sound abstraction, the refined controller inherits the abstract guarantees [14, 26]. 

Although the term “symbolic” is also used in task and motion planning (TAMP), it has a different meaning. TAMP typically uses symbols to represent semantic predicates, objects, and high-level actions, while continuous planners determine configurations or trajectories that realize those actions [27–29]. In contrast, symbolic control uses symbols to represent regions of the continuous state and input spaces and synthesizes a feedback policy over these regions. Thus, TAMP primarily addresses task-level sequencing and continuous feasibility, whereas symbolic control focuses on certifying closed-loop dynamical behavior. The two approaches are complementary: a TAMP layer could provide high-level manipulation goals that are executed by certified symbolic controllers. 

Symbolic-control methods have been applied to systems such as mobile robots and autonomous vehicles [30, 31], but their main limitation is state-space explosion. CSymPlan addresses this challenge for high-DOF manipulators by synthesizing over a lower-dimensional operational-space model rather than the full joint-space state. 

## III. BACKGROUND AND PROBLEM FORMULATION 

## _A. Notation_ 

Let R, R _≥_ 0, and N denote the sets of real numbers, nonnegative real numbers, and natural numbers, respectively. For _x,_ ˆ _x ∈_ R<sup>_n_</sup> , dist( _x,_ ˆ _x_ ) = _∥x − x_ ˆ _∥_ denotes Euclidean distance. For _x ∈_ R<sup>_n_</sup> and _A ⊂_ R<sup>_n_</sup> , dist( _x, A_ ) = inf _a∈A ∥x − a∥_ . A set-valued map from _A_ to _B_ is denoted _f_ : _A_ ⇒ _B_ . Infinite sequences are written in bold, for example **_x_** = ( _x_ 0 _, x_ 1 _, . . ._ ), and finite truncations are denoted by a subscript such as **_x_** _T_ . 

## _B. Manipulator dynamics in operational space_ 

Consider an _nq_ -DOF manipulator with joint configuration _q ∈_ R<sup>_nq_</sup> . Its rigid-body dynamics are 


where _M_ ( _q_ ) is the inertia matrix, _C_ ( _q, q_ ˙) ˙ _q_ contains Coriolis and centrifugal terms, _g_ ( _q_ ) is gravity, _τ_ is the commanded joint torque, and _τ_ ext represents external torques. Let the translational end-effector position be _x_ = _h_ ( _q_ ) _∈_ R<sup>_d_</sup> , with _d ∈{_ 2 _,_ 3 _}_ , and let _J_ ( _q_ ) = _∂h/∂q_ be the corresponding Jacobian. Then 


The operational-space dynamics can be written as [32] 


3 


Figure 2. Offline CSymPlan architecture. The upper row shows the one-time synthesis pipeline: task-space discretization, finite symbolic model construction, reach-avoid task specification, SCOTS-based policy synthesis, and export of a policy table for runtime query. The lower row shows the real-time execution pipeline: the robot state is measured and quantized, the precomputed policy is queried, the selected abstract input is refined through operational-space torque realization, and the resulting torque command is applied to the robot. 

where Λ( _q_ ) = ( _JM_<sup>_−_1</sup> _J_<sup>_⊤_</sup> )<sup>_−_1</sup> is the operational-space inertia, _η_ ( _q, q_ ˙) groups task-space bias terms, _F ∈_ R<sup>_d_</sup> is the commanded task-space wrench for the translational task, and _F_ ext collects external task-space effects. 

## _C. Sampled perturbed control systems_ 

A sampled perturbed control system is described by a tuple _S_ = ( _X, U, F_ ), where _X ⊆_ R<sup>_n_</sup> is the state set, _U ⊆_ R<sup>_m_</sup> is the input set, and _F_ : _X × U_ ⇒ _X_ is a set-valued transition map. For sampling period _s >_ 0, _F_ is induced by the sampled behavior of the perturbed continuous-time differential inclusion 


where _ξ ∈ X_ , _u ∈ U_ , and _w ∈_ R<sup>_n_</sup> _≥_ 0<sup>boundsthecomponent-</sup> wise disturbance set 


Measurement uncertainty is represented by (4): 


with _z ∈_ R<sup>_n_</sup> _≥_ 0<sup>. A behavior of</sup><sup>_S_is an infinite sequence (</sup><sup>**_x_**</sup><sup>_,_</sup><sup>**_u_**) =</sup> ( _x_ 0 _, u_ 0 _, x_ 1 _, u_ 1 _, . . ._ ) such that _xk_ +1 _∈F_ ( _xk, uk_ ) for all _k ∈_ N. 

## _D. Reachability, invariance, and reach-avoid specifications_ 

A specification is a desired subset of possible state sequences. In this work we consider invariance, reachability, and reachavoid specifications. Given a safe set _X_ safe, invariance requires the system to remain safe for all time: 


Given an initial set _X_ 0, goal set _X_ goal, and horizon _T_ , reachability requires the system to reach the goal within the horizon: 


The reach-avoid specification in (7) combines the invariance and reachability specifications in (5) and (6): 


A controller satisfies a specification if the closed-loop behaviors of the system under that controller are contained in the specification set. 

## _E. Symbolic controller synthesis_ 

Symbolic synthesis proceeds by constructing a finite abstraction _S_ abs = ( _X_ abs _, U_ abs _, F_ abs) that over-approximates the sampled perturbed system _S_ . In the implementation, the abstraction is connected to the concrete system by a quantizer _Q_ : _X → X_ abs. Equivalently, the graph of the quantizer, 


can be viewed as the feedback-refinement relation. Assuming _U_ abs _⊆ U_ , refinement requires that every admissible symbolic input is admissible for the concrete plant and that all quantized concrete successors are included among the abstract successors. In particular, for every ( _x,_ ˆ _x_ ) _∈ RQ_ , 1) _U_ abs(ˆ _x_ ) _⊆ U_ ( _x_ ); and 

4 

2) for all _u ∈ U_ abs(ˆ _x_ ), _Q_ ( _F_ ( _x, u_ )) _⊆F_ abs(ˆ _x, u_ ), where _Q_ ( _F_ ( _x, u_ )) = _{Q_ ( _x_<sup>+</sup> ) _| x_<sup>+</sup> _∈F_ ( _x, u_ ) _}_ . 

The abstract controller is then computed by fixed-point algorithms for reachability and invariance [14]. If the abstraction is sound and the safe and goal sets are approximated conservatively, the refined controller inherits the abstract guarantee. 

## IV. METHODOLOGY 

This section presents the common mathematical model used by both the offline and online versions of CSymPlan. The offline implementation precomputes a fixed symbolic controller for a given workspace, obstacle set, and goal. The online implementation retains the same symbolic state and input grids and transition relation, but recomputes the finite-horizon reachavoid winning set and corresponding admissible control actions at runtime from the current measured state, target set, and obstacle set. In our implementation, these online fixed-point computations are executed in parallel using pFaces [15]. 

_A. Manipulator reduction to a sampled perturbed double integrator_ 

CSymPlan begins with the operational-space model in (2). We choose the task-space command 


where _u ∈_ R<sup>_d_</sup> is a virtual input interpreted as desired endeffector acceleration. Substituting (8) into (2) gives 


The residual term in (9), Λ( _q_ )<sup>_−_1</sup> _F_ ext, together with modeling error, discretization error, measurement error, and torquerealization error, is modeled as a bounded additive disturbance. Defining the task-space state _ξ_ = [ _x_<sup>_⊤_</sup> _, v_<sup>_⊤_</sup> ]<sup>_⊤_</sup> , with _v_ = _x_ ˙ , yields the perturbed double-integrator model 


This is an instance of the perturbed differential inclusion (3) with linear drift. The input set _u ∈U ⊂_ R<sup>_d_</sup> is compact and is selected to respect actuation limits after torque realization. The system is sampled with period _s_ under zero-order-hold inputs. In practice, the disturbance bound _w_ and measurement bound _z_ are calibrated conservatively from residual-acceleration and state-estimation error data recorded while running the torquerealization layer of Section V on representative motions. 

## _B. Safe and goal sets_ 

Let _X_ ws _⊂_ R<sup>_d_</sup> denote the admissible Cartesian workspace and let _O ⊂ X_ ws be the union of obstacle regions. For a safety distance _d_ safe _>_ 0, define the inflated obstacle set 


Using the inflated obstacle set in (11), the position-level safe set is 


Lifting this set to the full task-space state gives 


where _V ⊂_ R<sup>_d_</sup> is a compact velocity set. The safe set is stated over the translational end-effector position; accordingly, the margin _d_ safe is chosen to cover the end-effector and tool geometry in addition to the tracking and measurement uncertainty already captured by _w_ and _z_ . Certification of whole-arm collision avoidance is outside the scope of the present abstraction; extensions beyond translational task-space certification are discussed in Section VII-B4. For a target position _xT ∈ X_ safe<sup>_x_andpositiontolerance</sup><sup>_d_tol,define</sup> 


Because the robot should come to rest at the goal, the full target set is 


Sequential waypoint tasks are handled by synthesizing a separate reach-avoid policy for each waypoint and switching to the next policy once the current goal set has been reached and held for a specified number of control ticks. 

**Problem 1** (Certified reach-avoid manipulation) **.** _Given the manipulator dynamics_ (1) _with translational end-effector output x_ = _h_ ( _q_ ) _, workspace X_ ws _, obstacle set O, disturbance and measurement bounds w and z, an initial set X_ 0 _⊆ X_ safe _, and the safe and goal sets_ (12) _and_ (13) _, synthesize a joint-torque feedback controller such that every closed-loop behavior of the sampled perturbed task-space system_ (10) _satisfies the reach-avoid specification_ (7) _._ 

The offline implementation of Section V-A solves Problem 1 once per scene by precomputing a policy over the full abstraction; the online implementation of Section V-B solves a finite-horizon instance of Problem 1 at each replanning step for the currently perceived sets. 

## V. IMPLEMENTATION 

## _A. Offline implementation_ 

Figure 2 shows the offline architecture: a one-time synthesis pipeline that discretizes the task space, builds the finite symbolic model, and exports a reach-avoid policy table, followed by a real-time execution pipeline that queries the table at the robot servo rate. 

_1) Offline symbolic synthesis:_ For a fixed workspace, obstacle set, and goal set, CSymPlan first constructs a finite abstraction of (10). The continuous set _X_ = _X_ ws _× V_ is discretized into a uniform grid _X_ abs, and the admissible acceleration set _U_ is discretized into a finite input set _U_ abs. For every abstract state–input pair, the transition relation _F_ abs is computed by over-approximating all reachable sampled successors under the disturbance and measurement bounds. The abstract safe set is selected conservatively so that each represented concrete cell lies in _X_ safe, and the abstract goal 

5 

## **Algorithm 1** CSymPlan offline synthesis 

**Require:** Workspace bounds _X_ ws, obstacles _O_ , safety margin _d_ safe, velocity bounds _V_ 

**Require:** Sampling time _s_ , disturbance and measurement bounds _w, z_ , grid parameters, input grid _U_ abs _⊆U_ 

**Require:** Task specification: initial set _X_ 0, goals _{X_ goal<sup>(</sup><sup>_j_)</sup><sup>_}_</sup> _j_<sup>_p_</sup> =1<sup>,</sup> with _p_ = 1 for a single goal **Ensure:** Policies _{π_<sup>(</sup><sup>_j_)</sup> _}_<sup>_p_</sup> _j_ =1 

- 1: Compute _X_ safe using (12) 

- 2: Discretize _X_ = _X_ ws _× V_ into uniform cells to obtain _X_ abs 

- 3: Compute _F_ abs by over-approximating reachable sets of (10) 

- 4: Build the quantizer _Q_ : _X → X_ abs 

- 5: **for** _j_ = 1 to _p_ **do** 

- 6: Construct abstract sets _X_<sup>ˆ</sup> 0<sup>(</sup><sup>_j_),</sup><sup>_X_ˆ</sup> safe<sup>(</sup><sup>_j_),and</sup><sup>_X_ˆ</sup> goal<sup>(</sup><sup>_j_)</sup> 

- 7: Synthesize reach-avoid controller Π<sup>(</sup><sup>_j_)</sup> : _X_ abs ⇒ _U_ abs by fixed-point computation 

- 8: Export a selector _π_<sup>(</sup><sup>_j_)</sup> ( _ξ_<sup>ˆ</sup> ) _∈_ Π<sup>(</sup><sup>_j_)</sup> ( _ξ_<sup>ˆ</sup> ) as a BDD or lookup table 

- 9: _X_ 0<sup>(</sup><sup>_j_+1)</sup> _← X_ goal<sup>(</sup><sup>_j_)if</sup><sup>_j< p_</sup> 

- 10: **end for** 

set is selected conservatively so that each represented concrete cell lies in _X_ goal. 

A fixed-point computation then yields a winning set and a symbolic controller. The resulting controller is exported as a binary decision diagram or lookup table. At runtime, policy evaluation is therefore constant time: the measured state is quantized, the symbolic action is looked up, and the corresponding Cartesian acceleration is refined to torques. Algorithm 1 summarizes this offline synthesis procedure. 

_2) Real-time policy execution:_ At runtime, the offlinesynthesized symbolic policy is executed in a high-frequency control loop. At servo tick _k_ , the robot provides joint feedback ( _qk, q_ ˙ _k_ ). The task-space state is computed as 


The quantizer maps _ξk_ to an abstract state _ξ_<sup>ˆ</sup> _k_ = _Q_ ( _ξk_ ), and the active symbolic policy returns a virtual acceleration _uk_ = _π_ ( _ξ_<sup>ˆ</sup> _k_ ). 

The abstract acceleration is realized through the operationalspace wrench command in (14), 


and the joint torque command 


The additional term _τ_ 0 _,k_ handles secondary objectives such as posture regulation, damping, and joint-limit avoidance. In our implementation, it is a fixed null-space PD term, 


where _q_ ns is a nominal posture, _N_ ( _qk_ ) is a null-space projector, and _Kp, Kd ≻_ 0 are fixed gains. These gains are tuned before 

**Algorithm 2** CSymPlan offline-policy runtime execution 

**Require:** Joint feedback ( _q, q_ ˙); policies _{π_<sup>(</sup><sup>_j_)</sup> _}_<sup>_p_</sup> _j_ =1<sup>;quantizer</sup> _Q_ ; goal sets _{X_ goal<sup>(</sup><sup>_j_)</sup><sup>_}_</sup> _j_<sup>_p_</sup> =1 **Ensure:** Torque commands _τk_ at the robot control rate 

- 1: Set active task index _j ←_ 1 

- 2: **while** robot is running and _j ≤ p_ **do** 3: Read ( _qk, q_ ˙ _k_ ) 

- 4: Compute _ξk ←_ � _h_ ( _qk_ )<sup>_⊤_</sup> _,_ � _J_ ( _qk_ ) ˙ _qk_ � _⊤_ � _⊤_ 5: Quantize _ξ_<sup>ˆ</sup> _k ← Q_ ( _ξk_ ) 6: Lookup symbolic input _uk ← π_<sup>(</sup><sup>_j_)</sup> ( _ξ_<sup>ˆ</sup> _k_ ) 7: Compute _Fk ← η_ ( _qk, q_ ˙ _k_ ) + Λ( _qk_ ) _uk_ 8: Compute _τk ← J_ ( _qk_ )<sup>_⊤_</sup> _Fk_ + _τ_ 0 _,k_ 9: Apply _τk_ subject to torque and safety limits 

- 10: **if** _ξk ∈ X_ goal<sup>(</sup><sup>_j_)for</sup><sup>_N_holdconsecutiveticks</sup><sup>**then**</sup> 11: _j ← j_ + 1 

- 12: **end if** 

- 13: **end while** 

the experiments and kept constant across trials. Algorithm 2 gives the offline runtime loop. 

_3) Offline guarantee boundary:_ The guarantee provided by CSymPlan is conditional on the abstraction and refinement assumptions, which we state explicitly so that the boundary of the certificate is unambiguous. 

**Assumption 1** (Soundness of abstraction and refinement) **.** (i) The abstract transition relation _F_ abs over-approximates all sampled perturbed task-space successors of (10); (ii) the abstract safe and goal sets are linear (conservative) approximations of the continuous sets (12) and (13); (iii) the difference between the intended virtual acceleration and the acceleration realized by (15) remains within the disturbance bound _w_ used during synthesis; (iv) the workspace and obstacle model match the physical environment after the configured safety inflation; and (v) the margin _d_ safe covers the end-effector and tool geometry, since the safe set is stated for the translational end-effector position. 

**Proposition 1** (Guarantee transfer) **.** _Under Assumption 1, if the quantized initial state lies in the winning set computed by Algorithm 1, then every closed-loop execution of Algorithm 2 satisfies the reach-avoid specification_ (7) _with respect to the sets_ (12) _–_ (13) _. This follows from the feedback-refinement construction of Section III-E: conditions (i) and (iii) make the quantizer graph RQ a feedback refinement relation from the sampled perturbed system to S_ abs _, so the refined controller inherits the abstract reach-avoid guarantee [14, 26], while conditions (ii), (iv), and (v) ensure that satisfaction of the abstract specification implies satisfaction of the continuous one._ 

Hardware experiments therefore demonstrate real-time executability together with empirical evidence that the calibrated bounds are conservative enough for Assumption 1 to hold in the reported setup. 

6 

_Remark_ 1 (Joint-space instantiation) _._ The same symboliccontrol principle can be instantiated in joint space by defining the abstraction over joint positions and velocities and synthesizing discrete joint-space commands. Such an abstraction would provide joint-level correctness guarantees but would be substantially higher-dimensional for a 7-DOF manipulator. The task-space formulation used in CSymPlan is chosen to make synthesis tractable for reach-avoid manipulation tasks defined by end-effector position. 

## _B. Online implementation_ 

The online implementation keeps the same sampled perturbed task-space model (10), but moves the symbolic synthesis call into the robot runtime. Instead of exporting a policy once for a fixed scene, an online server maintains the symbolic grid, input grid, sampled post operator, and growth-bound computation. A separate robot process sends the current task data to the server, requests a finite-horizon reach-avoid controller, receives one or more admissible symbolic accelerations, and executes the resulting command segment through the same operational-space torque layer used by the offline implementation. Figure 3 shows the resulting architecture and its receding-horizon request– synthesis–execution loop, where the online server calls are implemented through pFaces [15], a tool enabling parallelized computation of reach-avoids synthesis sets as well as the corresponding policies. 

_1) Online task and set representation:_ At replanning instant _r_ , the online controller receives the measured task-space state in (17), 


a target region _G_<sup>_x_</sup> _r_<sup>_⊂X_ws,andaruntimeobstacleset</sup><sup>_Or⊂_</sup> _X_ ws from the current task or perception module. The positionlevel safe set is updated as 


and lifted to the state space by 


Equations (18)–(19) define the online safe set. The online goal set is represented as a target tube 


where _v_ tol _,r_ may be chosen strictly for stop-at-goal tasks or relaxed for intermediate waypoints. These sets are received by the online server as interval unions. For a collection of axis-aligned boxes _B_ = _{_ [ _ℓi, ui_ ] _}_<sup>_N_</sup> _i_ =1<sup>_B_,theserializationusedby</sup> the online server is 


with obstacle boxes written to obst_set, target boxes written to target_set, and the measured state written to current_state. Position-only obstacles are lifted by assigning the velocity coordinates the full bounds _V_ . 

Let _ηx, ηu_ denote the state and input grid widths. The online abstraction uses the same finite state and input grids as the offline implementation, 


Only the symbolic safe and target subsets change across replanning calls: 


Thus the abstract sets in (23) allow the online implementation to avoid rebuilding the grid at every servo tick; it recomputes the winning set for the current symbolic safe and target sets. 

_2) Online reach-avoid synthesis:_ For each online request, a finite-horizon reach-avoid fixed point is computed over the abstract transition relation _F_ abs. Given horizon _H_ , the terminal set is initialized as 


The associated time-indexed symbolic controller is the setvalued map 


The condition in (25) is the online analogue of the offline controller lookup: every admissible action keeps all abstract successors inside the remaining winning set. If _Q_ ( _ξr_ ) _∈/ Wr,_ 0, the online engine returns no certified action for the requested sets and horizon. The implementation then holds the robot at the last certified reference and may submit a modified request, for example by widening the target tube within configured limits. 

When several admissible actions are returned, the controller selects one action for execution. Let 


be the nominal sampled double-integrator matrices. The implementation ranks candidate actions by a one-step cost 


where _Px_ and _Pv_ project onto position and velocity, _xT,r_ is the target center, and 

7 


Figure 3. Online CSymPlan architecture. At each replanning instant, the robot senses the environment, updates the obstacle model and uncertainty bounds, maps the measured task-space state to an abstract cell, and sends the current state, target set, unsafe set, and horizon to the pFaces server. pFaces performs finite-horizon reach-avoid synthesis over the symbolic abstraction, returns a certified policy or command segment for the current state, and the robot refines the selected abstract input through operational-space torque realization. The lower loop illustrates the receding-horizon update: changes in the environment trigger map updates, new pFaces requests, and replacement of stale command segments. 

and uses the same operational-space torque refinement as the offline controller, 


The term (27) rewards predicted progress of the nominal successor toward the target. Since the minimization is over Π _r,i_ ( _ξ_<sup>ˆ</sup> ), the heuristic only chooses among actions already certified by the symbolic fixed point. Algorithm 3 summarizes one online pFaces synthesis request. 

This makes the online synthesis server the decision layer, while the Cartesian or joint impedance behavior remains the torquerealization layer. 

Before activating a buffered command, the runtime checks that the current measured state is still close to the state for which the command was certified: 

_3) Online buffered execution:_ The robot process separates online synthesis from real-time torque control. A background planning thread communicates with the online server at a lower rate _f_ plan, while the Franka torque callback runs at the servo period. The planner submits a new request when the remaining certified buffer time falls below a threshold _T_ buf : 


Commands that fail (34) are discarded and a new online request is issued. If the buffer is empty, the controller holds the last certified reference using the same impedance layer while waiting for the online synthesis server to generate a new winning set and corresponding symbolic actions. An optional proportional–derivative fallback can be enabled for debugging, but actions generated by that fallback are not part of the certified online controller. Algorithm 4 describes the buffered execution loop. 


Each buffered symbolic action _ur,i_ is interpreted as a constant acceleration over one symbolic sampling interval using the reference in (30). For local time _t ∈_ [0 _, s_ ] inside that interval, the desired task-space reference is 


_4) Online guarantee boundary:_ The online guarantee is the same reach-avoid guarantee as in the offline case, but it is local to the sets, horizon, and state used in each online server request. Formally, Proposition 1 applies per request, with _X_ safe _,r_ , _X_ goal _,r_ , and the finite horizon _H_ in place of the fixed offline sets. If _Q_ ( _ξr_ ) _∈ Wr,_ 0, then any command selected from (25) keeps the sampled perturbed system inside _X_ safe _,r_ and 


At servo tick _k_ , the online implementation forms the realized acceleration command 

_u_<sup>rt</sup> _k_<sup>= sat</sup><sup>_U_(</sup><sup>_ur,i_+</sup><sup>_Kx_(</sup><sup>_xd_(</sup><sup>_tk_)</sup><sup>_−xk_) +</sup><sup>_Dx_(</sup><sup>_vd_(</sup><sup>_tk_)</sup><sup>_−vk_))</sup><sup>_,_</sup> (31) 

8 

**Algorithmgorithmorithm 3** CSymPlanymPlanmPlan online <u>pFacesFaces</u> synthesisynthesisnthesis requestquestuest 

**Algorithmgorithmorithm 3** CSymPlanymPlanmPlan online <u>pFacesFaces</u> synthesisynthesisnthesis requestquestuest **Algorithm 4** CSymPlan online-policy execution **Require:** Measured state _ξr_ , target tube _X_ goal _,r_ , obstacle set **Require:** pFaces, _Q_ , targets _{G_<sup>_x_</sup> _r_<sup>_}_,obstacles</sup><sup>_Or_,</sup><sup>_T_buf</sup> _Or_ , horizon _H_ **Ensure:** Torque commands _τk_ **Require:** Fixed grids _X_ abs, _U_ abs, transition relation _F_ abs, 1: _r ←_ 1, _C_ buf _←∅_ , _c_ act _←∅_ quantizer _Q_ 2: Start asynchronous online worker (via pFaces) **Ensure:** Certified command segment _Cr_ or failure 3: **while** robot is running **do** 1: Build _X_ safe _,r_ and _X_ goal _,r_ using (19)–(20) 4: _ξk ←_ Sense( _qk, q_ ˙ _k_ ) 2: Serialize target and obstacle intervals to pFaces using (21) 5: **if** LowBuffer( _C_ buf _, T_ buf ) and Idle() **then** 3: Compute conservative abstract sets _X_<sup>ˆ</sup> safe _,r_ and _X_<sup>ˆ</sup> goal _,r_ 6: PlanAsync( _ξk, G_<sup>_x_</sup> _r_<sup>_, Or_)</sup> 4: Compute _Wr,H ← X_<sup>ˆ</sup> goal _,r_ 7: **end if** 5: **for** _i_ = _H −_ 1 down to 0 **do** 8: _C_ buf _←_ AppendCertified( _C_ buf ) 6: Compute _Wr,i_ by the predecessor update (24) 9: **if** _c_ act = _∅_ **then** 7: Store admissible actions Π _r,i_ using (25) 10: _c_ act _←_ PopValid( _C_ buf _, ξk_ ) 8: **end for** 11: **end if** 9: _ξ_<sup>ˆ</sup> _r,_ 0 _← Q_ ( _ξr_ ) 12: **if** _c_ act _̸_ = _∅_ **then** 10: **if** _ξ_<sup>ˆ</sup> _r,_ 0 _∈/ Wr,_ 0 **then** 13: ( _xd, vd_ ) _←_ SampleReference( _c_ act) 11: **return** failure 14: _u_<sup>rt</sup> _k_<sup>_←_TrackCertified(</sup><sup>_ξk, xd, vd_)</sup> 12: **end if** 15: **else** 13: **for** _i_ = 0 to _H −_ 1 **do** 16: _u_<sup>rt</sup> _k_<sup>_←_HoldReference(</sup><sup>_ξk_)</sup> 14: Select _ur,i ∈_ Π _r,i_ ( _ξ_<sup>ˆ</sup> _r,i_ ) using (26) 17: **end if** 15: Predict _ξ_<sup>ˆ</sup> _r,i_ +1 _← Q_ ( _Asξ_<sup>ˆ</sup> _r,i_ + _Bsur,i_ ) 18: _τk ←_ RealizeTorque( _u_<sup>rt</sup> _k_<sup>_, qk,q_˙</sup><sup>_k_)</sup> 16: Append ( _ξ_<sup>ˆ</sup> _r,i, ur,i, ξ_<sup>ˆ</sup> _r,i_ +1) to _Cr_ 19: Apply _τk_ with torque, rate, and safety limits 17: **if** _ξ_<sup>ˆ</sup> _r,i_ +1 _∈ X_<sup>ˆ</sup> goal _,r_ **then** 20: **if** GoalReached( _ξk, G_<sup>_x_</sup> _r_<sup>)</sup><sup>**then**</sup> 18: **break** 21: _r ← r_ + 1, _c_ act _←∅_ , _C_ buf _←∅_ 19: **end if** 22: **end if** 20: **end for** 23: **end while** 21: **return** _Cr_ 

## _A. Offline evaluation_ 

reaches _X_ goal _,r_ within the requested horizon, provided that the disturbance, measurement, and torque-refinement bounds used by _F_ abs contain the physical realization error. The guarantee is preserved across replanning calls when each accepted buffered command satisfies the state-matching condition (34) and the runtime obstacle model remains valid until the next certified update. 

The guarantee does not cover three cases: no winning action returned by the online server, execution of an explicitly enabled uncertified fallback, or environment changes that invalidate _X_ safe _,r_ before a new certified request has been accepted. In these cases the implementation either holds the last certified reference, widens the target tube within configured bounds, submits a new request to compute another winning action, or stops the task if the state leaves the symbolic domain. 

## VI. EXPERIMENTAL EVALUATION 

The experimental evaluation mirrors the implementation structure. The offline evaluation tests the precomputedcontroller pipeline in static workspaces, including real Franka FR3 deployment and PyBullet benchmarking against planning and receding-horizon baselines. The online evaluation tests the request–synthesis–execution loop under changing task geometry, including Isaac Sim/Isaac Lab [16] task families and real Franka experiments with perception-driven obstacle updates. 

The offline evaluation studies the precomputed-policy version of CSymPlan in fixed workspaces. The aim is to verify that the quantization–lookup–torque pipeline can be executed on hardware and to compare the offline symbolic feedback policy against representative planning-and-control baselines in simulation. In contrast to the online implementation in Section V-B, the obstacle set, workspace, and goal sequence are fixed during each offline synthesis run, and the resulting policy is exported before execution. 

_1) Offline real-world Franka experiments:_ 

_Offline hardware and control stack.:_ The offline synthesized policy is deployed on a Franka FR3 using the architecture in Figure 4. The system has two stages. The offline stage uses SCOTS [14] to construct the finite abstraction and synthesize a reach-avoid controller for a fixed workspace and task. The resulting controller is exported as a lookup structure. The runtime stage performs state estimation, quantization, policy lookup, and torque realization at the robot control rate. The control loop runs at 1 kHz, and the low-level gains in (16) are fixed across all trials. 

_Offline tasks and procedure.:_ The real-robot task is a taskspace reach-avoid problem defined by the safe and goal sets in (12)–(13). The initial set is a neighborhood around a nominal start pose. A trial is counted as successful if the end-effector enters the goal set and remains there for _N_ hold consecutive control ticks while staying in the safe set for the entire execution. We test five static scenes with increasing obstacle 

9 

Table I 

OFFLINE SIMULATED REACH-AVOID BENCHMARKING IN PYBULLET ACROSS RANDOMIZED TRIALS AND SCENES. METRICS SUMMARIZE RELIABILITY, EFFICIENCY, CONTROL QUALITY, AND ONLINE COMPUTATION TIME. 

|**Method**|**Success (%)**|**Violation (%)**|_t_goal **(s)**|_L_ **(m)**|**Smoothness**|**Effort**|**CPU/step (ms)**|
|---|---|---|---|---|---|---|---|
|CSymPlan|**100**|**0.0**|**2.3**|1.25|0.90|1.05|**0.05 / 0.08**|
|RRT + tracker|76|10.0|3.9|1.42|1.25|1.18|120 / 240|
|LQR-RRT<sup>_⋆_</sup>+ tracker|83|6.0|3.6|1.33|0.62|1.02|170 / 340|
|MPPI|95|4.5|2.5|1.17|0.52|0.98|18.1 / 19.0|
|Neural MPC|93|3.5|2.6|**1.14**|**0.38**|**0.92**|3.6 / 4.4|


**Notes:** _N_ denotes the number of trials and ∆ _t_ the control period. Success = 100 _N_ succ _/N_ ; violation = 100 _N_ viol _/N_ , where a violation means _∃k_ : _xk ∈/ X_ safe<sup>_x_;</sup><sup>_t_goal=min</sup><sup>_{k_∆</sup><sup>_t_:</sup><sup>_ξk∈X_goal</sup><sup>_}_;</sup><sup>_L_=�</sup> _k_<sup>_∥xk_+1</sup><sup>_−xk∥_</sup> 2<sup>;smoothness=�</sup> _k_<sup>_∥uk_+1</sup><sup>_−uk∥_2</sup> 2<sup>;effort=�</sup> _k_<sup>_∥τk∥_</sup> 2<sup>2.CPU/step</sup> reports the mean and 95th percentile over the execution loop. 


Figure 4. Offline real-time execution architecture on the Franka FR3. Joint feedback is converted to task-space position and velocity, quantized, queried through the precomputed symbolic policy, and refined to joint torques at the control rate. 


Figure 5. Offline hardware experiment procedure and control-loop execution order. 

complexity. Obstacles are represented by boxes, cylinders, and mesh primitives, and the same execution stack and actuation limits are used across scenes. 

Each hardware trial follows the procedure in Figure 5: initialize the robot to the start configuration, verify that the measured state lies in the winning set, execute the 1 kHz 

quantization–lookup–torque loop, and terminate on success, timeout, or safety stop. We repeat five trials per scene with fixed initial states and fixed goals. 

_Offline real-world metrics.:_ We report aggregate hardware metrics over _N_ = 5 trials per scene. Curves show the mean and one-standard-deviation band over normalized execution time. Figure 6 shows the end-effector position tracking error, 


where _pd_ ( _t_ ) is the desired end-effector position command and _p_ ( _t_ ) is the measured end-effector position from forward kinematics. The same figure also reports the commanded jointtorque norm _∥τ_ ( _t_ ) _∥_ 2 and the measured joint-velocity norm _∥q_ ˙( _t_ ) _∥_ 2. 

_2) Offline simulated benchmarking:_ We also evaluate the offline version of CSymPlan in simulation against representative planning-and-control baselines. The simulated study uses 

a Franka-family manipulator model in PyBullet with the same task-space bounds, obstacle definitions, safety margins, actuation limits, and torque-realization interface across all methods. Figure 7 shows a representative simulated scene. Each method outputs a task-space command or reference that is executed through the same low-level realization layer. Thus, the comparison isolates the decision layer while keeping collision checking, limits, and dynamics consistent. 

_Offline task setup.:_ We consider five reach-avoid tasks in environments with randomized starts, goals, and obstacle placements sampled from fixed configuration sets. A trial terminates on success, safety violation, or timeout. Success requires reaching _X_ goal while remaining in _X_ safe for the entire trajectory. Safety violation is registered if the end-effector position leaves the position-level safe set, intersects the inflated obstacle set, or violates configured velocity or torque limits. All simulated experiments are run on a workstation with an NVIDIA RTX 5070 Ti GPU with 16 GB VRAM and 64 GB RAM. 

_Offline baselines.:_ We compare against four representative baselines for the offline setting: 

10 


Figure 6. Offline Franka FR3 real-robot execution metrics across hardware trials. The panels show (a) end-effector position tracking error, (b) commanded joint-torque norm, and (c) measured joint-velocity norm. Curves show the mean and one-standard-deviation band over _N_ = 5 trials per scene. 


Figure 7. Representative offline simulation scene. The robot starts at the blue marker and aims to reach the red marker. Green markers indicate a trajectory produced by CSymPlan through the certified safe set. 

- **RRT + tracker.** A geometric RRT computes a collision-free path that is executed by the shared tracking and torquerealization layer. 

- **LQR-RRT**<sup>_⋆_</sup> **+ tracker.** LQR-RRT<sup>_⋆_</sup> grows a state-space tree using an LQR-based steering metric and then executes the resulting trajectory through a tracking controller [33]. 

- **MPPI.** Model predictive path integral control samples control sequences over a finite horizon, rolls them out through the dynamics model, and applies the first action using pathintegral reweighting [7]. 

- **Neural MPC.** Neural MPC computes receding-horizon actions under constraints, using a learned approximation to reduce latency while retaining a constraint-aware formulation [34]. 

_Offline metrics and results.:_ Table I summarizes reliability, motion quality, and deployability metrics. Reliability is measured by success and violation rates. Motion quality is measured by time-to-goal, path length, smoothness, and effort. Deployability is measured by mean and 95th-percentile online computation time per control step. 

Across the randomized trials, CSymPlan achieves 100% success with no recorded safety violations. Figure 8 shows 

representative executed trajectories for CSymPlan and the baselines. The receding-horizon baselines produce competitive time-to-goal and path-length values but have nonzero violation rates in tight scenes. LQR-RRT<sup>_⋆_</sup> improves over geometric RRT by incorporating dynamics into the planning stage, but it still inherits failure modes from the plan–then–track separation. The main computational trade-off is offline synthesis: CSymPlan incurs a larger one-time cost to build the abstraction and solve the fixed point, but the resulting runtime policy query is a constant-time lookup. 

**Offline compute cost.** In the reported simulated setup, CSymPlan required _T_ offline = 290 s in total, comprising _T_ abs = 75 s for abstraction construction and _T_ syn = 215 s for fixed-point synthesis. As a reference, the average offline planning time for RRT was 6 _._ 2 s. This difference is expected because CSymPlan performs conservative abstraction construction and fixed-point synthesis, which is substantially heavier than incremental sampling. The benefit is that this cost is paid once per scene and model; after synthesis, online execution is a predictable quantize–lookup–apply operation. When tasks share the same workspace and dynamics, the abstraction phase can be reused and only re-synthesis is required for new goals, partially amortizing the offline burden. 

## _B. Online evaluation_ 

- _1) Online simulated Isaac Sim experiments:_ 

_Online simulation stack.:_ The simulated experiments use the CSymIsaac environment, which runs a Franka-family manipulator in Isaac Sim through Isaac Lab. The symbolic state and input grids and the transition relation _F_ abs are constructed once before execution and reused across replanning calls. At runtime, only the current safe and target sets are updated from the robot state and scene geometry. 

We use pFaces [15] as an online synthesis server over this fixed abstraction. At each replanning step, the measured state, target set, obstacle-derived safe set, and horizon are sent to pFaces, which computes the finite-horizon winning set and corresponding admissible symbolic actions. The returned action is interpreted as a Cartesian acceleration, checked for staleness, and executed through the task-space realization layer in (31)– (33). This closes the state/perception–synthesis–realization loop used in both simulation and hardware. 

11 


(a) CSymPlan 


(b) RRT 


(c) LQR-RRT<sup>_⋆_</sup> (d) MPPI (e) Neural MPC 

Figure 8. Representative maze trajectories for offline CSymPlan and baselines. Dashed curves show reference paths where applicable and solid curves show executed end-effector trajectories from the same start to the same goal. Black regions are obstacles; a collision is counted when the end-effector footprint intersects an obstacle cell. 

_Online simulated task families.:_ We evaluate three families of reach-avoid tasks, illustrated in Figure 9. 

- **Shelf reach-avoid.** The robot moves between targets placed at different parts of a shelf or rack, including top-shelf approach, shelf insertion, retreat, and lower-shelf placement motions. This task stresses three-dimensional motion because the feasible path must coordinate lateral, depth, and vertical movement while avoiding shelf surfaces, posts, and the shelf lip. 

- **Three-dimensional maze.** The robot moves a probe-like end-effector through a generated tabletop maze. The safe set is the corridor volume, and the obstacle set is formed by the maze walls and baffles. This task evaluates whether the online symbolic controller can keep the executed trajectory inside a narrow connected safe region rather than simply moving around isolated convex obstacles. 

- **Moving obstacle reach-avoid.** The robot moves between two Cartesian goal regions while a voxelized cube obstacle changes occupancy over time. The obstacle can sweep laterally, switch between high and low states, or require over-under behavior. This task evaluates online replanning when the safe set changes during execution. 

_Online simulated procedure.:_ Each simulated trial begins by resetting the Franka model, loading the task geometry, and selecting a start state, target tube, and obstacle set. For shelf and maze tasks, the target sequence is known at the start of the episode, but the controller still solves each segment online from the current measured state. For moving-obstacle tasks, the obstacle set is updated whenever the voxel state changes, and a new online request via pFaces is issued when the certified command buffer falls below the replanning threshold in (28). A trial terminates when the final target has been held for the required dwell time, when the end-effector leaves the safe set, when a robot or scene collision is detected, or when the episode reaches a timeout. 

The main simulated measurements are success or failure, safety violation, time-to-goal, path length, minimum obstacle clearance, command smoothness, joint-torque effort, number of pFaces replanning calls, and pFaces synthesis latency. These metrics and benchmark results are summarized in Section VI-B4. 

- _2) Online real-world Franka experiments:_ 

_Online hardware and control stack.:_ The hardware experiments use the CSymFranka stack on a Franka FR3. The robot reports joint position and velocity through libfranka at the servo rate, and similar to the simulated case, a pFaces controller takes synthesis requests. In particular, the controller computes the measured end-effector state in the Franka base frame, submits online pFaces synthesis requests in a background thread, buffers the returned symbolic accelerations, and realizes the active command as a Cartesian impedance or joint-impedance torque command. The torque layer is kept fixed across real experiments so that differences between tasks are attributed to the online symbolic decision layer and the task geometry rather than to retuning the low-level controller. 

Real-time obstacle tracking is provided by DNVblox [35], which fuses depth observations into a voxel map and publishes the occupied obstacle set used by the online pFaces request; Figure 10 shows the perception and simulation correspondence. In the real-robot experiments, the DNVblox obstacle map is updated at 10 Hz, while the libfranka torque callback remains at the robot servo rate. Each pFaces replanning request therefore uses the most recent DNVblox obstacle snapshot, inflated by the configured safety margin _d_ safe before being serialized into obst_set. 

_Online real-world task families.:_ We evaluate three realrobot task families, shown in Figure 11. 

- **High-speed reach.** The robot executes a sequence of measured Cartesian targets in the Franka base frame. The targets are chosen to exercise fast three-dimensional endeffector motion while remaining inside the calibrated symbolic workspace. This task measures whether online pFaces commands can be generated and consumed quickly enough for aggressive but bounded reaching. 

- **Dynamic-obstacle reach-avoid.** The robot moves between Cartesian targets while the obstacle description changes during execution. The obstacle description is obtained from the 10 Hz DNVblox voxel map, the pFaces target and obstacle intervals are updated online, and stale buffered commands are discarded if the measured state no longer matches the certified command start state. This task evaluates closed-loop behavior under a changing safe set. 

- **Dynamic maze.** The robot executes a maze-like reach-avoid sequence in which the allowed corridor or active target 

12 


Figure 9. Representative Isaac Sim benchmark environments used for online evaluation: shelf/rack reach-avoid, point reach, 3D maze, and moving-obstacle under tasks. 

changes over time. The task is intended to test repeated online synthesis in narrow passages, where holding the last certified reference, rejecting stale commands, and stopping outside the symbolic domain are all safety-critical behaviors. 

_Online real-world procedure.:_ Each hardware trial starts from a checked home configuration. Before motion is enabled, the system verifies that the initial end-effector position and velocity lie inside the configured symbolic domain and that the first target is within the allowed distance bound. The pFaces worker is then asked to produce an initial certified segment. Once a segment is available, the torque callback starts tracking buffered symbolic commands at the robot servo rate. During execution, the controller monitors workspacedomain membership, target distance, command staleness, DNVblox obstacle-map updates, torque limits, and timeout conditions. Whenever DNVblox publishes a new obstacle map, the occupied voxels are converted to inflated Cartesian obstacle intervals and used in the next pFaces synthesis request. A trial is successful when the robot reaches the final target set and remains there for the configured hold time without leaving the safe set or triggering a stop condition. 

Hardware measurements include success or failure, safetystop reason, time-to-goal, maximum and mean tracking error, minimum obstacle clearance when available, command-buffer underruns, pFaces synthesis latency, commanded torque norm, torque-rate saturation count, and measured joint-velocity norm. 

These metrics and representative hardware values are summarized in Section VI-B4. 

_3) Online benchmark baselines:_ We compare CSymPlan against five representative baselines spanning deterministic optimal control, sampling-based receding-horizon control, classical plan–then–track motion generation, reactive safety filtering, and learned predictive control. All baselines are evaluated using the same task definitions, workspace bounds, obstacle sets, safety inflation, velocity and input limits, termination conditions, and success criteria as CSymPlan. Whenever possible, the baseline decision variable is chosen to be the same Cartesian acceleration input _u ∈U_ used in (10). The resulting command is then executed through the same operational-space torquerealization layer used by CSymPlan, so that the comparison isolates the decision-making layer rather than differences in low-level tracking. 

_Nonlinear model predictive control.:_ The first baseline is nonlinear model predictive control (NMPC) [6, 24] over the same sampled task-space double-integrator model used by CSymPlan. At each replanning step, NMPC solves a finitehorizon optimal-control problem from the current measured state. The optimization variables are a sequence of Cartesian accelerations 


13 


Figure 10. Real-world online perception and simulation correspondence. Left: Franka FR3 hardware setup used for the online reach-avoid experiments. Middle: DNVblox voxel reconstruction obtained from depth sensing and used to form the runtime obstacle set. Right: corresponding Isaac Sim scene used for controlled online benchmarking. 

and the predicted states evolve according to the nominal sampled double-integrator dynamics 


The objective penalizes terminal distance to the target, intermediate distance to the target, velocity magnitude, control effort, and input variation. Obstacle avoidance is handled either through hard nonlinear constraints when feasible or through signed-distance penalties with a large collision cost. The first optimized acceleration is applied to the robot and the problem is solved again at the next replanning step. This baseline represents a deterministic optimization-based online plannercontroller with the same task-space model and torque interface as CSymPlan, but without a discrete reach-avoid winning-set certificate. 

_Model predictive path integral control.:_ The second baseline is model predictive path integral control (MPPI) [7]. MPPI also uses the sampled task-space double-integrator model, but replaces deterministic trajectory optimization with stochastic sampling over candidate acceleration sequences. At each replanning step, the controller samples candidate control sequences, rolls them out over the prediction horizon, evaluates them using a cost composed of target-reaching error, obstacleavoidance cost, velocity regularization, command smoothness, and control-effort regularization, and then computes a weighted control update. The first acceleration of the selected sequence is executed through the shared torque-realization layer. This baseline represents a sampling-based receding-horizon controller that can naturally handle nonlinear costs and changing obstacles, but does not provide a closed-loop reach-avoid certificate for all states in a symbolic cell. 

_RRT-Connect with trajectory tracking.:_ The third baseline is a classical decoupled motion-generation stack based on RRTConnect [36]. The planner computes a collision-free geometric path in configuration space or task space using the same obstacle model and safety inflation as the other methods. The resulting path is time-parameterized and then tracked using the same impedance or operational-space tracking controller used in the robot experiments. For dynamic-obstacle tasks, the current path is invalidated when it intersects the updated obstacle set, and RRT-Connect is called again from the current 

robot state. This baseline evaluates the conventional plan–then– track architecture discussed in Section I. It tests whether a fast geometric planner combined with a common tracking layer can provide the same reliability as a closed-loop symbolic reach-avoid controller. 

_Control-barrier-function quadratic program.:_ The fourth baseline is a control-barrier-function quadratic program (CBFQP) [37, 38]. A nominal task-space controller first generates a desired acceleration or velocity command that drives the endeffector toward the target. A quadratic program then minimally modifies this nominal command so that the resulting action satisfies workspace and obstacle-safety constraints. For an obstacle described by a safety function _hj_ ( _x_ ), where _hj_ ( _x_ ) _≥_ 0 denotes the safe side of the constraint, the CBF-QP imposes inequalities of the form 


or the corresponding exponential or high-order barrier constraint for acceleration-level control [39, 40]. The optimized command is executed through the shared torque layer. This baseline represents a reactive safety-filter approach. It is expected to perform well for simple obstacle-avoidance tasks, but it may become conservative, infeasible, or trapped in narrow passages and maze-like environments because it enforces local safety constraints without explicitly solving the global reachability problem. 

_Neural MPC.:_ The fifth baseline is Neural MPC, a learned approximation or learned extension of receding-horizon model predictive control [41–43]. The neural controller receives the current task-space state, target description, and obstacle representation, and predicts a Cartesian acceleration command or a short horizon of acceleration commands. The network is trained on the same task distribution used in the simulated benchmarks, using trajectories generated by the optimizationbased controller or by successful expert rollouts. At runtime, the neural prediction is executed through the same operationalspace torque-realization layer as the other methods. When enabled, the predicted command is clipped to the admissible input set _U_ and checked against the configured velocity and workspace limits before execution. This baseline evaluates whether a learned controller can reproduce the performance of 

14 


Figure 11. Representative online real-world Franka FR3 task scenes. Left: dynamic-obstacle reach-avoid, where the robot moves from the red start region to the green goal region while avoiding a moving rod obstacle. Middle: maze traversal with dynamic walls, where the wall configuration is changed during execution and the controller replans from the updated obstacle set. Right: smooth static-maze traversal, where the robot follows a continuous path through fixed curved maze corridors from start to goal. 

online optimization with lower computation time, and whether that improvement in speed comes at the cost of safety violations or poor generalization to new obstacle layouts. 

_Fairness of comparison.:_ All baselines use the same initial states, target sets, obstacle sets, control periods, actuation limits, and termination logic. For methods that operate in task space, the commanded Cartesian acceleration is passed directly to the shared operational-space torque controller. For methods that output a geometric path or a desired pose trajectory, the trajectory is time-parameterized and tracked by the same lowlevel controller used for CSymPlan hardware execution. In the simulated experiments, every method is evaluated across the same randomized scene seeds. In the hardware experiments, only baselines that satisfy the configured safety checks in simulation are deployed on the Franka FR3. 

_4) Online metrics and certification outcomes:_ The online experiments measure two different outcomes: task completion and certified safe resolution. A certified controller is not expected to solve every requested online instance. Certification means that, when the current abstract state lies in the finitehorizon winning set, the selected action is guaranteed by the abstraction to satisfy the reach-avoid condition for the current safe set, goal set, horizon, and disturbance bounds. If 

timeouts. We report 


Table II lists the metrics used in the online evaluation. We also report the safe-resolution rate 


When every trial ends in success, safe stop, timeout, or violation, (35) implies _R_ safe = 100 _− R_ viol. This metric separates the safety behavior of the online controller from the feasibility of a particular dynamic task instance. 

Motion efficiency is measured by the time-to-goal _t_ goal and the executed path length 


Obstacle separation is measured by the minimum observed clearance 


then pFaces correctly returns no certified action for that request. Such a trial is counted as a safe stop or timeout rather than a safety violation. Thus, the main online safety claim is not 100% task success; it is that the robot executes certified command segments when a winning action exists and otherwise holds, replans, or stops. 

Let _N_ be the number of trials. Let _N_ succ be the number of trials that reach and hold the final goal, _N_ viol the number of safety violations, and _N_ stop the number of certified stops or 

where _Ok_ is the current obstacle set. Runtime performance is measured by pFaces synthesis latency, the number of online replanning requests, command buffer underruns, stale segment rejections, and the age of the DNVblox obstacle map at the time of each pFaces request. Tracking quality is measured by 


Figure 12 summarizes the normalized-time hardware tracking-error and obstacle-clearance profiles used to evaluate the online torque-realization layer and dynamic-task safety margin. 

15 

Table II 

ONLINE EVALUATION METRICS. THE SAFE-RESOLUTION METRIC SEPARATES CERTIFIED TASK FAILURE FROM UNSAFE EXECUTION. 

|**Metric**|**Definition**|**Interpretation**|
|---|---|---|
|Success|100_N_succ_/N_|Trials that reach and hold the final target without leaving the safe set.|
|Violation|100_N_viol_/N_|Trials with collision, inflated-obstacle entry, workspace exit, or limit violation.|
|Safe stop / timeout|100_N_stop_/N_|Trials that terminate without collision because no certified action is available, a<br>command becomes stale, or the task times out.|
|Safe resolution|100(_N_succ+_N_stop)_/N_|Trials that either succeed or terminate conservatively without a safety violation.|
|Time to goal|_t_goal|Elapsed time from motion start to final target hold.|
|Path length|�<br>_k _<sup>_∥xk_+1</sup><sup>_−xk∥_</sup>2|Length of the executed end-effector trajectory.|
|Minimum clearance|min_k_dist(_xk, Ok_)|Closest distance to the current obstacle set.|
|pFaces solve time|mean / 95th percentile|Wall-clock time for one online reach-avoid synthesis request.|
|Replans / trial|_N_req per trial|Number of online synthesis requests sent to pFaces.|
|Buffer underruns / trial|count / trial|Number of times no certified buffered action is available at execution time.|
|Stale rejects / trial|count / trial|Returned or buffered segments rejected by the state-matching condition.|
|Tracking error|mean / max _∥xd −x∥_2|Accuracy of the torque-realization layer while executing symbolic acceleration<br>commands.|
|DNVblox age|mean / 95th percentile|Time between the obstacle-map timestamp and the corresponding pFaces request.|
|(a) End|-effector tracking error|(b) Minimum obstacle clearance|


Figure 12. Online hardware stability profiles over normalized execution time. (a) Mean end-effector tracking error with one-standard-deviation bands for the evaluated task families. (b) Mean obstacle clearance with one-standard-deviation bands for the dynamic tasks; the dashed horizontal line is the configured safety margin used to inflate the runtime obstacle set before pFaces synthesis. 

_5) Online simulation task outcomes:_ Tables III and IV summarize representative Isaac Sim results over 50 trials per task family. Across the three task families, CSymPlan achieves a 94% aggregate success rate with no safety violations and a 100% safe-resolution rate. The remaining trials terminate as safe stops or timeouts, primarily in the narrow maze and moving-obstacle settings where the updated safe set removes all currently winning actions or a buffered command segment becomes stale. 

_6) Online hardware task outcomes:_ Tables V and VI summarize representative Franka FR3 results with DNVblox perception. The hardware results are slightly more conservative than simulation because the obstacle set is generated from depth fusion and a returned command segment can be rejected if the measured state no longer matches the certified segment start state. Across 30 trials, CSymPlan succeeds in 27 trials with no observed safety violations and a 100% safe-resolution rate. The three non-successful trials terminate as certified stops: 

one dynamic-obstacle trial returns no winning action after a DNVblox map update, and two dynamic-maze trials reject stale segments or fail to find a certified continuation in a narrow passage. 

_7) Online baseline comparison:_ Table VII compares online CSymPlan against representative online planning and control baselines in simulation. All methods use the same task-space dynamics, obstacle inflation, state limits, and torque-realization layer whenever possible. The baselines can produce shorter or faster motions in open scenes, but they do not provide the same cell-wise reach-avoid certificate. CSymPlan is therefore evaluated not only by task completion, but also by whether non-successful trials are resolved as safe stops rather than safety violations. 

_8) Online result summary:_ Across the representative online Isaac Sim benchmark, CSymPlan achieves 94% task success, 0% safety violations, and 100% safe resolution. The hardest cases are the three-dimensional maze and moving-obstacle 

16 

### Table III 

REPRESENTATIVE ONLINE ISAAC SIM TASK OUTCOMES. VALUES ARE MEAN _±_ STANDARD DEVIATION WHERE APPLICABLE. 

|**Task family**|**Trials **|<sup>**Success**</sup><br>**(%)**|**Safe stop**<br>**/ timeout (%)**|**Violation**<br>**(%)**|**Safe**<br>**resolution **|**(%)**<br>_t_goal<br>**(s)**|_L_<br>**(m)**|_d_min<br>**(cm)**|**pFaces**<br>**mean / 95p (ms)**|
|---|---|---|---|---|---|---|---|---|---|
|Shelf reach-avoid|50|98|2|0.0|100|3_._2_±_0_._5|1_._31_±_0_._16|5_._8_±_1_._4|84 / 190|
|3D maze|50|94|6|0.0|100|6_._1_±_1_._1|2_._12_±_0_._29|3_._4_±_0_._8|210 / 510|
|Moving obstacle|50|90|10|0.0|100|4_._8_±_1_._0|1_._76_±_0_._25|4_._6_±_1_._2|170 / 430|
|**All online simulation**|150|**94**|**6**|**0.0**|**100**|4_._7_±_1_._5|1_._73_±_0_._41|4_._6_±_1_._6|155 / 430|


<u>Safe stop / timeout includes trials in which pFaces returned no winning action, the command buffer became stale, or the final goal was not reached before</u> the episode timeout. 

### Table IV 

REPRESENTATIVE ONLINE ISAAC SIM REPLANNING AND BUFFER STATISTICS. 

|**Task family**|**Replans**<br>**/ trial**|**Buffer**<br>**underruns / trial**|**Stale rejects**<br>**/ trial**|**Dominant safe-stop cause**|
|---|---|---|---|---|
|Shelf reach-avoid|5_._8_±_1_._6|0.1|0.2|Timeout near shelf lip or conservative grid<br>boundary.|
|3D maze|13_._5_±_3_._7|0.8|1.1|No winning action in a narrow passage for the<br>requested horizon.|
|Moving obstacle|16_._2_±_4_._5|1.2|1.6|Obstacle update invalidates the currently<br>buffered segment.|
|**All online simulation**|11_._8_±_5_._8|0.7|1.0|Certified hold, re-request, or timeout without<br>collision.|


### Table V 

REPRESENTATIVE ONLINE FRANKA FR3 TASK OUTCOMES WITH DNVBLOX PERCEPTION. VALUES ARE MEAN _±_ STANDARD DEVIATION WHERE APPLICABLE. 

|**Task**<br>**Trials **|**Success**|**Safe**<br>**stop**|**Violation**|**Safe**<br>**resolution**|_t_goal<br>**(s)**|_d_min<br>**(cm)**|**Stop cause**|
|---|---|---|---|---|---|---|---|
|High-speed reach<br>10|10 / 10|0 / 10|0 / 10|10 / 10|2_._3_±_0_._3|–|none|
|Dynamic-obstacle reach-avoid<br>10|9 / 10|1 / 10|0 / 10|10 / 10|4_._4_±_0_._8|5_._1_±_1_._6|no certified action|
|Dynamic maze<br>10|8 / 10|2 / 10|0 / 10|10 / 10|7_._0_±_1_._5|3_._5_±_0_._9|stale / no solution|
|**All hardware**<br>30|**27 / 30**|**3 / 30**|**0 / 30**|**30 / 30**|4_._6_±_2_._1|4_._3_±_1_._5|certified stops|
|Minimum clearance is omitted for high-speed reach because no dynamic<br>executing an uncertified goal-reaching action.|obstacle|is presen|t. A safe s|top means t|hat the robo|t holds or t|erminates without|


### Table VI 

REPRESENTATIVE ONLINE FRANKA FR3 RUNTIME STATISTICS. 

|**Task**|**Tracking error**<br>**mean / max (cm)**|**pFaces**<br>**mean / 95p (ms)**|**DNVblox age**<br>**mean / 95p (ms)**|**Replans**<br>**/ trial**|**Underruns**<br>**/ trial**|**Stale rejects**<br>**/ trial**|
|---|---|---|---|---|---|---|
|High-speed reach|1.1 / 3.2|65 / 150|–|4_._1_±_1_._0|0.0|0.0|
|Dynamic-obstacle reach-avoid|1.6 / 4.8|135 / 330|70 / 125|11_._8_±_3_._2|0.4|0.8|
|Dynamic maze|2.1 / 6.0|260 / 680|85 / 150|18_._7_±_5_._0|1.7|2.1|
|**All hardware**|1.6 / 6.0|153 / 410|78 / 139|11_._5_±_6_._4|0.7|1.0|
|DNVblox map age is the elapsed time bet|ween the most recent voxel-map|update and the pFa|ces request using t|hat map.|||


tasks, where the online safe set can change while a command segment is being executed. In these cases, the runtime statematching check rejects stale commands and triggers replanning. If pFaces cannot certify a continuation, the controller holds the last certified reference or terminates the task safely. 

On the Franka FR3, CSymPlan succeeds in 27 of 30 representative trials, with 0 observed safety violations and 30 

of 30 trials ending in either success or certified safe stop. The mean pFaces latency is 153 ms and the 95th-percentile latency is 410 ms, which remains below the command-buffer duration in most trials. The real-robot non-successes are certified stops caused by no winning action or stale-command rejection, not collisions. Thus, the robot never executes an uncertified command. 

17 

Table VII 

REPRESENTATIVE ONLINE SIMULATION BASELINE COMPARISON AGGREGATED ACROSS SHELF, MAZE, AND MOVING-OBSTACLE TASKS. 

|**Method**|**Success**<br>**(%)**|**Violation**<br>**(%)**|**Safe stop**<br>**/ timeout (%)**|**Safe**<br>**resolution (%)**|**Solve**<br>**mean / 95p (ms)**|**Comment**|
|---|---|---|---|---|---|---|
|CSymPlan online|**94**|**0.0**|6.0|**100.0**|155 / 430|Certified actions; no-solution cases become safe<br>stops.|
|NMPC|91|3.3|5.7|96.7|38 / 74|Fast deterministic optimization, but no symbolic<br>winning-set certificate.|
|MPPI|88|5.3|6.7|94.7|22 / 31|Aggressive sampling-based behavior with lower<br>clearance near obstacles.|
|RRT-Connect + tracker|74|9.3|16.7|90.7|210 / 460|Plan–then–track mismatch in dynamic scenes.|
|CBF-QP|83|1.3|15.7|98.7|**3.1 / 6.5**|Very fast local safety filter, but can get stuck in<br>maze-like tasks.|
|Neural MPC|86|6.0|8.0|94.0|1.4 / 2.2|Fastest runtime, but weaker safety under<br>distribution shift.|


VII. CONCLUSION AND FUTURE WORK 

## _A. Conclusion_ 

This paper presented CSymPlan, a certified symbolic planning and control framework for high-DOF robot manipulators. The central idea is to replace the standard plan–then–track pipeline with a feedback policy synthesized over a finite abstraction of the closed-loop task-space dynamics. By reducing the manipulator to a sampled perturbed double-integrator model in operational space, CSymPlan makes symbolic synthesis tractable for reach-avoid manipulation tasks while still executing the resulting action through a torque-level controller on the Franka FR3. 

The offline implementation precomputes a reach-avoid controller for a fixed workspace, obstacle set, and goal set. At runtime, the measured end-effector state is quantized, the symbolic policy is queried, and the selected virtual Cartesian acceleration is refined into joint torques. This produces a constanttime control loop after synthesis, shifting the computational burden to an offline abstraction and fixed-point computation stage. 

The online implementation extends the same abstraction and refinement interface to changing tasks and perception-driven obstacle maps. Instead of using a fixed precomputed policy, the robot sends the current quantized state, target set, obstacle set, and horizon to pFaces. The pFaces server computes a finitehorizon winning set and returns certified command segments that are buffered and executed by the real-time torque controller. This design separates slow symbolic synthesis from the highfrequency robot servo loop and allows the controller to react to new goals and changing safe sets without rebuilding the full abstraction. 

The experiments evaluate CSymPlan in both offline and online settings. In the offline setting, the symbolic controller achieves predictable real-time execution after synthesis and avoids the tracking mismatch that can occur in decoupled planning and control. In the online setting, the key metric is not only task success, but safe resolution: when a winning action exists, the robot executes a certified segment; when no certified continuation exists, the robot rejects the segment, 

holds the last certified reference, replans, or stops safely. Thus, the safety claim is not that every requested task is feasible, but that the executed actions remain inside the certified reach-avoid interface under the stated abstraction, disturbance, perception, and refinement assumptions. 

Overall, CSymPlan demonstrates that symbolic control can be made practical for high-DOF manipulation by combining task-space abstraction, conservative disturbance modeling, pFaces-accelerated synthesis, and torque-level refinement. The resulting framework provides a bridge between formal reachavoid guarantees and real robotic execution in cluttered and changing workspaces. 

## _B. Future Work_ 

_1) Scalable and structure-aware abstractions:_ The main computational bottleneck of CSymPlan is the construction and solution of the finite abstraction. Although the task-space reduction avoids a direct grid over the full 7-DOF joint state, the number of symbolic states still grows quickly with workspace dimension, velocity bounds, and grid resolution. Future work will therefore investigate adaptive, nonuniform, and structure-aware abstractions. Instead of using a uniform grid over the full workspace, the abstraction could allocate fine cells near obstacles, goal boundaries, narrow passages, and high-uncertainty regions, while using coarser cells in open regions. This direction is closely related to approximate simulation and abstraction metrics for continuous systems [44], symbolic models for nonlinear systems [13], and compositional abstraction techniques for large interconnected systems [45]. 

A complementary direction is to use pFaces-style parallelism more aggressively during abstraction construction and fixedpoint computation. The current online implementation already separates synthesis from the 1 kHz robot torque loop, but further acceleration could be obtained by parallelizing the predecessor operator, pruning unreachable symbolic regions, and caching local winning sets across related goals and obstacle maps [15]. This would make online synthesis practical for larger workspaces and finer grids without increasing the real-time burden on the robot controller. 

18 

_2) Hybridization with sampling, optimization, and learning:_ Another promising direction is to combine CSymPlan with fast non-symbolic motion-generation methods. Sampling-based planners, trajectory optimization, MPC, MPPI, or learned motion priors could first propose a candidate path, tube, or sequence of intermediate goals. Symbolic synthesis would then be used only to certify a local region around that candidate rather than the entire workspace. This hybrid design could reduce the number of symbols considered by the fixed-point computation while preserving the reach-avoid guarantee for the executed segment. 

This idea is related to feedback motion-planning methods that combine planning with verified regions of attraction, such as LQR-trees [46] and funnel libraries [47]. In the context of CSymPlan, such methods could provide local dynamically feasible funnels or motion tubes, while the symbolic layer would certify that the selected tube remains inside the current safe set and reaches the target set under the configured disturbance and measurement bounds. 

_3) Temporal-logic and STL task specifications:_ The current formulation focuses on reach-avoid tasks. This is sufficient for many point-to-point manipulation problems, but it does not capture the full structure of long-horizon manipulation. Future work will extend the specification layer to richer temporal objectives, including linear temporal logic and signal temporal logic. This would allow CSymPlan to encode tasks such as visiting regions in a specified order, avoiding a region until a condition becomes true, maintaining clearance while tracking a moving object, or satisfying time-bounded dwell constraints. 

Temporal-logic planning has been widely used for robot motion planning [30, 48], while signal temporal logic provides a natural language for continuous-time and real-valued trajectories [49]. In future versions of CSymPlan, STL formulas could be compiled into finite-horizon symbolic objectives, or combined with receding-horizon synthesis in a way similar to STL-constrained MPC [50]. This would make the online pFaces loop more expressive than repeated reach-avoid calls while retaining a formal task-level semantics. 

_4) Extending certification beyond translational task space:_ The present abstraction is defined over translational endeffector position and velocity. This choice is deliberate: it makes symbolic synthesis tractable and matches the reach-avoid tasks considered in this work. However, many manipulation problems require constraints on orientation, joint limits, selfcollision, payload-dependent dynamics, or contact modes. A direct uniform grid over joint position and velocity is not practical for a 7-DOF arm, so a joint-space extension will require more structured representations. 

Future work will investigate decomposed and hierarchical joint-space certification. One approach is to combine the current task-space certificate with lower-dimensional jointspace safety filters for joint limits, self-collision, and singularity avoidance. Another approach is to construct local reachable sets using zonotopes, polytopes, or other set representations, as in continuous reachability tools such as CORA [51]. These reachable sets could be used to certify local joint-space motion 

segments without constructing a single global grid over all joint variables. 

A third direction is to use local feedback funnels or controlinvariant tubes around nominal joint-space trajectories. Funnelbased and sums-of-squares methods provide a way to certify local regions of attraction around nonlinear robot trajectories [46, 47]. In CSymPlan, these local certificates could act as intermediate abstractions: the high-level symbolic controller would reason over certified motion primitives, while each primitive would provide its own joint-space validity certificate. This would move the framework toward whole-arm certified manipulation without requiring a monolithic full-dimensional symbolic grid. 

_5) Perception-aware certification:_ The online experiments use perception-driven obstacle sets, where depth observations are converted into occupied voxels and then inflated before being sent to pFaces. Future work will make this perception interface more explicit in the certificate. Rather than treating the obstacle map as fixed between updates, the abstraction could include map age, voxel confidence, occlusion, and depth uncertainty when constructing the safe set. This would allow the online controller to distinguish between free, occupied, and unknown regions and to synthesize policies that are robust not only to dynamics and tracking error, but also to perception uncertainty. 

Together, these extensions would make CSymPlan more scalable, more expressive, and more directly applicable to whole-arm manipulation in changing and partially observed environments. 

## REFERENCES 

- [1] B. Sundaralingam, S. K. S. Hari, A. Fishman, C. Garrett, K. V. Wyk, V. Blukis, A. Millane, H. Oleynikova, A. Handa, F. Ramos, N. Ratliff, and D. Fox, “curobo: Parallelized collision-free minimum-jerk robot motion generation,” 2023. [Online]. Available: https://arxiv.org/abs/2310.17274 

- [2] O. Khatib, S. Quinlan, and D. Williams, “Robot planning and control,” _Robotics and Autonomous Systems_ , vol. 21, no. 3, pp. 249–261, Sep. 1997. 

- [3] S. M. LaValle, _Planning Algorithms_ . Cambridge University Press, 2006. 

- [4] S. A. Ajwad, J. Iqbal, M. I. Ullah, and A. Mehmood, “A systematic review of current and emergent manipulator control approaches,” _Frontiers of Mechanical Engineering_ , vol. 10, no. 2, pp. 198–210, 2015. 

- [5] S. M. LaValle and J. J. Kuffner, “Randomized kinodynamic planning,” _The International Journal of Robotics Research_ , vol. 20, no. 5, pp. 378–400, 2001. 

- [6] D. Q. Mayne, J. B. Rawlings, C. V. Rao, and P. O. M. Scokaert, “Constrained model predictive control: Stability and optimality,” _Automatica_ , vol. 36, no. 6, pp. 789–814, 2000. 

- [7] G. Williams, A. Aldrich, and E. A. Theodorou, “Model predictive path integral control: From theory to parallel computation,” _Journal of Guidance, Control, and Dynamics_ , vol. 40, no. 2, pp. 344–357, 2017. 

- [8] J. Kober, J. A. Bagnell, and J. Peters, “Reinforcement learning in robotics: A survey,” _The International Journal of Robotics Research_ , vol. 32, no. 11, pp. 1238–1274, 2013. 

- [9] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

19 

- [10] T. Haarnoja, A. Zhou, K. Hartikainen, G. Tucker, S. Ha, J. Tan, V. Kumar, H. Zhu, A. Gupta, P. Abbeel, and S. Levine, “Soft actor-critic algorithms and applications,” _arXiv preprint arXiv:1812.05905_ , 2018. 

- [11] P. Tabuada, _Verification and Control of Hybrid Systems: A Symbolic Approach_ . Springer, 2009. 

- [12] G. Pola, A. Girard, and P. Tabuada, “Approximately bisimilar symbolic models for nonlinear control systems,” _Automatica_ , vol. 44, no. 10, pp. 2508–2516, 2008. 

- [13] M. Zamani, G. Pola, M. Mazo, and P. Tabuada, “Symbolic models for nonlinear control systems without stability assumptions,” _IEEE Transactions on Automatic Control_ , vol. 57, no. 7, pp. 1804–1809, 2012. 

- [14] M. Rungger and M. Zamani, “SCOTS: A Tool for the Synthesis of Symbolic Controllers,” in _International Conference on Hybrid Systems: Computation and Control_ , Vienna Austria, 2016, pp. 99–104. 

- [15] M. Khaled and M. Zamani, “pfaces: An acceleration ecosystem for symbolic control,” in _International Conference on Hybrid Systems: Computation and Control_ , ser. HSCC ’19. New York, NY, USA: Association for Computing Machinery, 2019, pp. 252–257. 

- [16] NVIDIA, “Isaac sim,” 2026, available at: https://github.com/ isaac-sim/IsaacSim (accessed 10 August 2026). [Online]. Available: https://github.com/isaac-sim/IsaacSim 

- [17] A. Candra, M. A. Budiman, and K. Hartanto, “Dijkstra’s and A-Star in Finding the Shortest Path: a Tutorial,” in _International Conference on Data Science, Artificial Intelligence, and Business Analytics_ , 2020, pp. 28–32. 

- [18] V. Varricchio, P. Chaudhari, and E. Frazzoli, “Sampling-based algorithms for optimal motion planning using process algebra specifications,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2014, pp. 5326–5332. 

- [19] A. Orthey, C. Chamzas, and L. E. Kavraki, “Sampling-Based Motion Planning: A Comparative Review,” _Annual Review of Control, Robotics, and Autonomous Systems_ , vol. 7, no. Volume 7, pp. 285–310, Jul. 2024. 

- [20] Z. Zhao, S. Cheng, Y. Ding, Z. Zhou, S. Zhang, D. Xu, and Y. Zhao, “A survey of optimization-based task and motion planning: From classical to learning approaches,” _IEEE/ASME Transactions on Mechatronics_ , vol. 30, no. 4, pp. 2799–2825, 2025. 

- [21] A. Tika, N. Gafur, V. Yfantis, and N. Bajcinca, “Optimal Scheduling and Model Predictive Control for Trajectory Planning of Cooperative Robot Manipulators,” _IFAC-PapersOnLine_ , vol. 53, no. 2, pp. 9080–9086, 2020. 

- [22] A. Mavrommati, C. Osorio, R. G. Valenti, A. Rajhans, and P. J. Mosterman, “An application of model predictive control to reactive motion planning of robot manipulators,” in _IEEE International Conference on Automation Science and Engineering (CASE)_ , 2021, pp. 915–920. 

- [23] M. Everett, Y. F. Chen, and J. P. How, “Motion planning among dynamic, decision-making agents with deep reinforcement learning,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2018, pp. 3052–3059. 

- [24] J. B. Rawlings, D. Q. Mayne, and M. M. Diehl, _Model Predictive Control: Theory, Computation, and Design_ , 2nd ed. Madison, WI: Nob Hill Publishing, 2017. 

- [25] C. Belta, A. Bicchi, M. Egerstedt, E. Frazzoli, E. Klavins, and G. J. Pappas, “Symbolic planning and control of robot motion [Grand Challenges of Robotics],” _IEEE Robotics & Automation Magazine_ , vol. 14, no. 1, pp. 61–70, 2007. 

- [26] G. Reissig and M. Rungger, “Feedback refinement relations for symbolic controller synthesis,” in _IEEE Conference on Decision and Control_ , 2014, pp. 88–94. 

- [27] J. Wolfe, B. Marthi, and S. Russell, “Combined task and motion planning for mobile manipulation,” in _ICAPS_ , 2010. 

- [28] L. P. Kaelbling and T. Lozano-Perez,´ “Hierarchical task and motion planning in the now,” in _ICRA_ , 2011. 

- [29] S. Srivastava, E. Fang, L. Riano, R. Chitnis, S. Russell, and P. Abbeel, “Combined task and motion planning through an extensible planner-independent interface layer,” in _ICRA_ , 2014. 

- [30] G. E. Fainekos, A. Girard, H. Kress-Gazit, and G. J. Pappas, “Temporal logic motion planning for dynamic robots,” _Automatica_ , vol. 45, no. 2, pp. 343–352, 2009. 

- [31] L. Shamgah, T. G. Tadewos, A. Karimoddini, and A. Homaifar, “A symbolic approach for multi-target dynamic reach-avoid problem,” in _IEEE International Conference on Control and Automation (ICCA)_ , 2018, pp. 1022–1027. 

- [32] O. Khatib, “A unified approach for motion and force control of robot manipulators: The operational space formulation,” _IEEE Journal on Robotics and Automation_ , vol. 3, no. 1, pp. 43–53, 1987. 

- [33] A. Perez, R. Platt, G. Konidaris, L. Kaelbling, and T. LozanoPerez, “Lqr-rrt*: Optimal sampling-based motion planning with automatically derived extension heuristics,” in _IEEE International Conference on Robotics and Automation_ , 2012, pp. 2537– 2542. 

- [34] J. Nubert, J. Kohler, V. Berenz, F. Allgower, and S. Trimpe, “Safe and fast tracking on a robot manipulator: Robust mpc and neural network control,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 3050–3057, 2020. 

- [35] A. Millane, H. Oleynikova, E. Wirbel, R. Steiner, V. Ramasamy, D. Tingdahl, and R. Siegwart, “nvblox: Gpu-accelerated incremental signed distance field mapping,” 2024. [Online]. Available: https://arxiv.org/abs/2311.00626 

- [36] J. J. Kuffner and S. M. LaValle, “RRT-connect: An efficient approach to single-query path planning,” in _International Conference on Robotics and Automation_ , 2000, pp. 995–1001. 

- [37] A. D. Ames, X. Xu, J. W. Grizzle, and P. Tabuada, “Control barrier function based quadratic programs for safety critical systems,” _IEEE Transactions on Automatic Control_ , vol. 62, no. 8, pp. 3861–3876, 2017. 

- [38] A. D. Ames, S. Coogan, M. Egerstedt, G. Notomista, K. Sreenath, and P. Tabuada, “Control barrier functions: Theory and applications,” in _European Control Conference_ , 2019, pp. 3420–3431. 

- [39] Q. Nguyen and K. Sreenath, “Exponential control barrier functions for enforcing high relative-degree safety-critical constraints,” in _American Control Conference_ , 2016, pp. 322–328. 

- [40] W. Xiao and C. Belta, “High-order control barrier functions,” _IEEE Transactions on Automatic Control_ , vol. 67, no. 7, pp. 3655–3662, 2022. 

- [41] M. Hertneck, J. Kohler,¨ S. Trimpe, and F. Allgower,¨ “Learning an approximate model predictive controller with guarantees,” _IEEE Control Systems Letters_ , vol. 2, no. 3, pp. 543–548, 2018. 

- [42] B. Karg and S. Lucia, “Efficient representation and approximation of model predictive control laws via deep learning,” _IEEE Transactions on Cybernetics_ , 2020. 

- [43] T. Salzmann, E. Kaufmann, J. Arrizabalaga, M. Pavone, D. Scaramuzza, and M. Ryll, “Real-time neural MPC: Deep learning model predictive control for quadrotors and agile robotic platforms,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 4, pp. 2397–2404, 2023. 

- [44] A. Girard and G. J. Pappas, “Approximation metrics for discrete and continuous systems,” _IEEE Transactions on Automatic Control_ , vol. 52, no. 5, pp. 782–798, 2007. 

- [45] M. Rungger and M. Zamani, “Compositional construction of approximate abstractions of interconnected control systems,” _IEEE Transactions on Control of Network Systems_ , vol. 5, no. 1, pp. 116–127, 2018. 

- [46] R. Tedrake, I. R. Manchester, M. M. Tobenkin, and J. W. Roberts, “LQR-trees: Feedback motion planning via sums-of-squares verification,” _The International Journal of Robotics Research_ , 

20 

vol. 29, no. 8, pp. 1038–1052, 2010. 

- [47] A. Majumdar and R. Tedrake, “Funnel libraries for real-time robust feedback motion planning,” _The International Journal of Robotics Research_ , vol. 36, no. 8, pp. 947–982, 2017. 

- [48] H. Kress-Gazit, G. E. Fainekos, and G. J. Pappas, “Temporallogic-based reactive mission and motion planning,” _IEEE Transactions on Robotics_ , vol. 25, no. 6, pp. 1370–1381, 2009. 

- [49] O. Maler and D. Nickovic, “Monitoring temporal properties of continuous signals,” in _Formal Techniques, Modelling and_ 

- _Analysis of Timed and Fault-Tolerant Systems_ , ser. Lecture Notes in Computer Science, vol. 3253. Springer, 2004, pp. 152–166. 

- [50] V. Raman, A. Donze,´ M. Maasoumy, R. M. Murray, A. Sangiovanni-Vincentelli, and S. A. Seshia, “Model predictive control with signal temporal logic specifications,” in _Conference on Decision and Control_ , 2014, pp. 81–87. 

- [51] M. Althoff, “An introduction to CORA 2015,” in _Workshop on Applied Verification for Continuous and Hybrid Systems_ . EasyChair, 2015, pp. 120–151. 

21 

