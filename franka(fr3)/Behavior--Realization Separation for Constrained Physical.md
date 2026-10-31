---
title: "Behavior--Realization Separation for Constrained Physical Human--Robot Interaction"
date: "2026-09-01"
authors: "Yongyan Cao"
url: https://arxiv.org/abs/2609.00669
pdf: https://arxiv.org/pdf/2609.00669
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.00669)** / [論文ページ](https://arxiv.org/abs/2609.00669)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Behavior–Realization Separation for Constrained Physical Human–Robot Interaction 

Yongyan Cao 

**_Abstract_ —Physical human–robot interaction software often couples desired-behavior specification with constrained realization; we treat these as separate layers. A** **_behavior layer_ supplies a desired contact-port acceleration** _a_<sup>id</sup> _k_ = _fθ_ ( _ek, e_ ˙ _k, Fh,k_ ) **. A** **_realization layer_ converts it into constrained robot commands and reports total desired-versus-realized acceleration error instead of hiding it in saturation. A same-objective unconstrained counterfactual separates regularization from constraint intervention, while plant data expose model error. This paper implements a receding-horizon quadratic program realizing memoryless affine behaviors. Changing the behavior modifies objective coefficients through** ( _Cθ, Gθ_ ) **while the robot-command variable and feasible set remain unchanged. A planar study instantiates impedance and admittance; the same running layer accepts an impedance– admittance–impedance reassignment without reconstruction, under its existing rate limit. On a torque-controlled 7-DOF Franka FR3 in MuJoCo, the runtime freezes task-space dynamics per solve and enforces torque feasibility across its horizon. Under a sustained 20 N push, it holds a slack-relaxed workspace boundary to within approximately 0.1–0.2 mm, versus 4.4 cm (impedance) and 4.7 cm (admittance) overshoot from instantaneous clipping. A derated actuator budget then activates the torque constraint: horizon-wide enforcement keeps its frozen-model plan feasible to** 2 _._ 1 _×_ 10<sup>_−_4</sup> **N** _·_ **m, whereas a first-step-only ablation plans up to 11.329 N** _·_ **m beyond budget; on the executed nonlinear plant, where both share the same local-model error, the gap is smaller but still favors horizon-wide enforcement (0.161 vs. 0.380 N** _·_ **m). These results are a focused proof of behavior– realization separation, not a new MPC or safety-filter principle (scope in Section VI-E).** 

**_Index Terms_ —Physical human–robot interaction, behavior– realization separation, robot-control architecture, predictive realization, model predictive control, impedance control, admittance control.** 

## I. INTRODUCTION 

Interaction behavior should specify only desired interaction dynamics; physical feasibility should be realized independently by the robot. 

A pHRI software stack has two conceptually different responsibilities: 

- 1) specify the desired interaction behavior; and 

- 2) realize that behavior through commands compatible with the physical robot. 

**Architectural hypothesis.** We argue for a general softwareengineering principle, stated above, and for a specific reason it should hold: desired interaction behavior is a statement in interaction-state space — position error, velocity error, and human force — while physical feasibility is a statement in robot-constraint space — joint torque, joint limits, and 

- Y. Cao is with Voryx Robotics LLC, San Jose, CA 95136, USA (e-mail: 

- yongyancao@gmail.com). 

workspace geometry. These are different mathematical objects with different natural variables, so a representation that mixes them (as a fixed impedance or PD law does) couples two things that do not have to be coupled. Separating them into a behavior layer and a realization layer connected by an explicit interface is therefore not only a convenient software boundary but a decomposition along the actual variables each responsibility depends on. This is an architectural claim, not merely an empirical one: it also implies that a behavior specification can be authored, tested, and replaced independently of the robot, and that feasibility logic can be verified once and reused across every behavior that respects the interface (Section VII argues this directly). This paper tests the principle with one executable desired-acceleration interface, developed and validated only for its memoryless affine subclass (Sections III-B–VI); that affine QP realization layer is one instance supporting the general claim, not the claim itself, and its success does not establish that every possible behavior representation can use the same runtime unchanged. 

Conventional impedance control combines behavior specification and command realization in one mass–spring–damper feedback law. Variable-impedance methods add adaptation, and model-predictive variants can optimize impedance parameters or jointly plan motion and compliance. Those formulations are useful, but changing the behavior representation generally changes the controller that interprets it. 

A concrete consequence of that coupling is actuator saturation. A conventional impedance or PD law computes joint torque directly from the interaction error, _τ_ = _J_<sup>_⊤_</sup> ( _−Kde − Dd_ ˙ _e_ ) + _τ_ ff , where _τ_ ff includes gravity/Coriolis compensation and, on a redundant arm, orientation-hold and null-space terms. Neither term reasons about the actuator limit. A stiff impedance, large interaction force, or unfavorable configuration can therefore drive the command past _τ_ max, and clipping silently changes the delivered acceleration. 

The architecture studied here assigns this conflict to a realization layer. Its current predictive implementation constrains the _total frozen-model torque_ — feedforward, orientation, null-space, and interaction terms — at every prediction step (Section VI-A). Any deviation from the behavior specification appears in the total realization residual; a counterfactual audit distinguishes constraint intervention from secondary-objective and model terms. Because the manipulator prediction is frozen at each solve, this remains a local-model mechanism rather than a global nonlinear-plant guarantee. 

We study a different decomposition: 

The behavior layer expresses intent without choosing a robot command. The realization runtime handles feasibility, 

2 


Fig. 1. Behavior and realization as separate layers. The behavior layer (dashed) supplies _a_<sup>id</sup> ; the realization runtime (blue) converts it into a constrained command and reports _rk_ = _a − a_<sup>id</sup> ; the audit in (18) separates its causes. 

constraint enforcement, and command optimization without deciding what stiffness, damping, or force-response semantics should mean. The runtime reports total behavior error and a constraint-intervention diagnostic rather than conflating the two. 

**The current executable instance.** For memoryless affine behavior models, the predictive runtime retains one decision variable, feasible set, and objective template; the desired behavioral acceleration enters through ( _Cθ, Gθ_ ). Section IV states this limited structural property formally, and Section III-B implements impedance and admittance. Nonlinear or stateful specifications may require different prediction machinery and are not instances of the present QP by assertion. 

This separation changes the scientific question. Instead of asking whether a particular MPC formulation produces compliant tracking, we ask: 

_How should robot-control software separate desired interaction behavior from its constrained physical realization, and how should unavoidable intervention be exposed?_ 

The contributions are: 

- a behavior–realization architecture that assigns behavior semantics and physical command feasibility to separate software layers; 

- a precise desired-acceleration interface, a total realization residual, and a same-objective constrained/unconstrained audit that makes constraint intervention separately observable; 

- one predictive realization runtime for the memoryless affine subclass, with a fixed robot-command variable and feasible set across impedance and admittance behavior layers; 

- reproducible planar and FR3 simulations showing online behavior-layer replacement, anticipatory state-constraint handling, and manipulator-level realization under command and torque limits. 

We do **not** claim that architectural separation in the abstract, impedance behavior in MPC, or constrained interaction control is new. Task-space inverse dynamics, whole-body QPs, reference governors, and hierarchical robot controllers already separate related responsibilities, while model predictive impedance and interaction controllers provide important integrated formulations. The narrower contribution is the four-part combination of (i) an interaction law evaluated along predicted states and exchanged at an acceleration-level contract, (ii) one fixed robot-command runtime across generators, (iii) a same-objective constrained/unconstrained counterfactual that decomposes the realization residual, and (iv) live generator substitution without rebuilding runtime state. The executable evidence covers two affine behaviors. 

## II. RELATED WORK AND POSITIONING 

The closest literature is best distinguished by what the predictive or adaptive layer optimizes and by what quantity the robot-level controller is asked to reproduce. 

Several approaches use MPC to adapt impedance parameters or to plan impedance and motion together. Anand et al. place a learned predictive policy above a low-level variable-impedance controller [1]. Haninger et al. predict interaction and optimize trajectory and impedance online while incorporating safety constraints [2]. Recent predictive variable-impedance formulations continue this parameter-adaptation direction [3]. Their optimized behavior variables are stiffness, damping, or related trajectory parameters. 

A related line of work is model-reference adaptive impedance control, which specifies desired impedance dynamics and designs an adaptive nonlinear controller so that the robot approaches them [4]. This establishes the value of separating a desired model from the physical robot, but it does not by itself provide horizon-wide handling of coupled state and input constraints. 

A separate class applies MPC directly to the robot or to a feedback-linearized error model, with decision variables that are robot commands rather than impedance parameters. Such a controller can generate an effective closed-loop impedance, but unless a desired interaction model appears explicitly in the prediction objective, that impedance is an induced property of the optimizer rather than the behavior it is asked to realize. This distinction separates the present formulation from our earlier double-integrator tracking MPC: the earlier controller penalizes interaction error, whereas the present controller penalizes disagreement with an independently specified interaction dynamical system. 

Task-space inverse dynamics and hierarchical whole-body QPs are a more fundamental precedent for the interface itself: they already accept desired task accelerations as modular objectives and solve for dynamically feasible robot accelerations, contact forces, or torques. Del Prete et al.’s TSID, for example, treats prioritized motion/force tasks for constrained fully actuated robots [19]. Predictive hierarchical task-space control extends acceleration-error objectives over a finite horizon for underactuated and constrained robots [20]. Thus neither “desired task acceleration” nor “QP realization 

3 

TABLE I 

POSITIONING AGAINST RELATED WORK. 

|Class|Behavior representation|Optimized robot-level variable|Role of prediction|
|---|---|---|---|
|Predictive variable<br>impedance|_Md, Dd, Kd_, often with a trajectory|Impedance parameters and/or<br>trajectory|Select compliant<br>behavior|
|Reference-model adaptive<br>impedance|_Md_¨_e_+_Dd_˙_e_+_Kde_=_Fh_|Adaptive feedback parameters|Usually absent|
|Direct robot MPC|State or tracking-error dynamics|Force, torque, velocity, or<br>acceleration|Optimize robot<br>motion directly|
|Impedance/interaction<br>MPC|Impedance, force, or coupled<br>interaction model|Robot command and sometimes<br>behavior parameters|Embed interaction<br>objectives and<br>constraints|
|Reference governor|A single reference/setpoint signal|Filtered reference fed to a fixed<br>inner-loop controller|Supervise a<br>non-predictive inner<br>loop to enforce<br>constraints|
|Predictive safety filter|Nominal controller input|Minimally modified admissible<br>input|Certify or replace a<br>proposed command|
|Constrained compliance<br>QP|Desired impedance/compliance<br>response|Torque, velocity, or acceleration|Reproduce compliant<br>behavior under robot<br>constraints|
|TSID / hierarchical<br>whole-body QP|Desired task accelerations and task<br>priorities|Joint acceleration, contact force,<br>and/or torque|Usually instantaneous<br>constrained realization|
|Predictive hierarchical<br>task-space control|Task trajectories and<br>acceleration-level errors|Robot state and command<br>trajectories|Extend hierarchical<br>task objectives over a<br>horizon|
|This work|_a_<sup>id </sup>=_Cθx_+_GθFh_|Robot command _u_|Minimize<br>dynamics-realization<br>error under constraints|


under robot constraints” is claimed as new. Relative to these frameworks, the contribution tested here is narrower: the task is an interaction dynamical law evaluated along the predicted state; the same runtime is retained across impedance and admittance generators; its residual is split using a sameobjective counterfactual; and the generator is replaced online without reconstructing the runtime state. 

Closer still is model predictive impedance and interaction control. Bednarczyk et al. formulate impedance behavior through MPC and handle practical constraints such as velocity, energy, and jerk [5]. Gold et al. formulate model predictive interaction control using robot and interaction models in the optimal-control problem and express manipulation objectives through costs and constraints [6]. Minniti et al. combine whole-body MPC with online adaptation of robot–environment interaction models for constrained mobile manipulation [7]. These papers are close precedents and make a broad “first constrained interaction-dynamics MPC” claim untenable. Alharbat et al. explicitly compare NMPC impedance, cascaded admittance, and hybrid position/force paradigms [14]; their later predictive admittance controller predicts both robot and desired impedance states, respects actuator constraints, and is validated in physical aerial interaction [15]. Kumbhar et al. pass admittance-generated plans to a constrained wholebody QP on Digit hardware [17]. These are stronger validation precedents than the present simulation-only study; the remaining distinction sought here is the fixed cross-behavior desiredacceleration contract, not predictive compliance itself. 

QP realization of compliant behavior and residual reporting also predate this work. Leboutet et al. compute robot com- 

mands under kinematic and dynamic constraints and propagate generalized-force residuals when a limb cannot realize the requested compliance [16]. More recent safety-critical adaptive impedance work filters a nominal impedance law through a QP with joint-state and torque constraints and provides formal invariance and boundedness results [18]. Accordingly, neither “QP-constrained compliance” nor “an explicit residual” is claimed independently as novel here. 

Reference governors and predictive safety filters are the closest architectural relatives to this paper’s separation, from a different literature than the parameter-adaptation and directMPC work described above. A reference governor sits upstream of a fixed, already-designed inner-loop controller and modifies the reference signal so that constraints on the resulting closed-loop trajectory are respected [8]. The parallel is direct: a reference governor also separates what is commanded from what is safe to execute. The difference is where prediction lives and what is exchanged. A reference governor typically supervises a fixed inner loop and manipulates a reference signal; the realization layer here is itself predictive, and the exchanged object is an affine desired-acceleration law evaluated over predicted interaction states. The realization residual additionally measures the difference between requested and delivered dynamics. Predictive safety filters similarly accept an arbitrary upstream command and use model-based backup optimization to certify or modify it [13]. This connection limits the novelty claim: the contribution is not separation in the abstract, but its formulation and measurement at the interaction-dynamics level. 

Control barrier function (CBF) quadratic programs are an- 

4 

other related architectural pattern from a different literature: a CBF-QP takes a nominal control input and projects it, at each tick, onto the minimal-deviation admissible set defined by a safety constraint [10]. The realization layer here is structurally similar — a minimal-deviation projection of a requested behavior onto a robot-feasible set — but the projected object is a full behavior law evaluated over a receding horizon rather than a single nominal input. The total deviation is reported, and the constrained/unconstrained counterfactual identifies its constraint-intervention component rather than treating every nonzero residual as safety action. We do not compare against a CBF-QP filter or a reference-governor instance in this paper; Section VI-E lists a matched comparison against the closest alternative architecture as open. 

Theorem 1 is a structural statement about a parametric quadratic program: for the affine generator class, the QP’s decision variable, feasible set, and constraint structure are fixed while only its cost coefficients vary with the generator parameter _θ_ . This is the object studied by the explicit MPC / multi-parametric QP literature [11], [12], which characterizes the solution map _θ �→ Uk_<sup>_⋆_(</sup><sup>_θ_)aspiecewiseaffine.Thepresent</sup> paper does not use that machinery — the QP is solved online at every tick, not precomputed offline — but Theorem 1 is best read as an instance of that established parametric-QP structure applied to the behavior–realization interface, not as a new structural fact about quadratic programs. 

Most rows above optimize a quantity tied to one behavior representation: impedance parameters, adaptive impedance gains, or robot-level tracking against a specific interaction model. The reference-governor and safety-filter rows are architecturally closest. Our narrower distinction is an interactionlevel behavior contract whose desired acceleration is separate from robot feasibility, together with a total residual and counterfactual intervention audit. The executable and theoretical evidence is limited to memoryless affine impedance and admittance behaviors. 

## III. BEHAVIOR–REALIZATION FORMULATION 

## _A. Behavior–Realization Interface_ 

Consider a rigid manipulator 


where _q ∈_ R<sup>_nq_</sup> , _τ ∈_ R<sup>_nq_</sup> , and _Fh_ is the human wrench applied at the interaction port. For a task coordinate _y_ = _h_ ( _q_ ) _∈_ R<sup>_ny_</sup> , 


Substitution of the joint dynamics gives the affine acceleration map 


where 


Let _yd_ be a nominal interaction pose and define 


**Definition 1** (Behavior-layer interface) **.** _In the present architecture, the behavior layer is a causal map_ 


_where z denotes optional internal behavior state and θ denotes behavior parameters. Its output is a desired contact-port acceleration — termed the_ desired behavioral acceleration _throughout this paper — not a robot command. The behavior layer is deliberately unaware of robot torque limits, joint limits, or workspace geometry; those belong to the realization layer. The general map defines the interface boundary; the theorem and experiments below cover only its memoryless affine specialization._ 

The architecture does not ask the behavior layer to compute _τ_ . It supplies _e_ ¨<sup>id</sup> , and the realization layer selects _τ_ so that the physical _e_ ¨ approaches _e_ ¨<sup>id</sup> while satisfying robot constraints. The predictive QP developed below is one realization-layer implementation, not the definition of the layer itself. 

The full manipulator formulation is the target architecture. The planar study below uses the following exactly discretized specialization so that behavior–realization separation can be isolated without kinematic or inverse-dynamics confounds: a planar point mass, 


where _p ∈_ R<sup>2</sup> is displacement from a nominal interaction pose, _u ∈_ R<sup>2</sup> is commanded robot force, _Fh ∈_ R<sup>2</sup> is measured human force, and _mr >_ 0 is the realized robot mass. Define 


Under zero-order hold with period ∆ _t_ , 


The actual acceleration is 

_ak_ =<sup>_uk_+</sup><sup>_Fh,k_</sup> _._ (12) _mr_ For this planar plant, Definition 1 specializes with _xk_ = [ _p_<sup>_⊤_</sup> _k_<sup>_v_</sup> _k_<sup>_⊤_]</sup><sup>_⊤_inplaceof(</sup><sup>_e,e_˙):</sup> 


For the affine class considered throughout this paper, 


The gap between what a behavior specifies and what the robot delivers is the _total realization residual_ , 


If _rk_ = 0, the robot exactly realizes the desired behavioral acceleration at that sample. Nonzero _rk_ alone, however, does not prove that a constraint caused the deviation: the finite force and force-rate weights can already shift the unconstrained optimum, and a physical plant can differ from the prediction model. 

5 

We therefore audit three terms. Let _Uk_<sup>_c⋆_</sup> be the deployed constrained optimum and _Uk_<sup>0</sup><sup>_⋆_</sup> the counterfactual optimum of the _same_ horizon objective at the same state, force forecast, and previous command after removing physical constraints. Let _a_<sup>_c_</sup> _k_<sup>and</sup><sup>_a_0</sup> _k_<sup>betheirfirst-stepmodelaccelerations,andlet</sup> _a_<sup>emp</sup> _k_ be the acceleration measured from the plant. Define 


Then the empirical total error closes exactly as 


Here _r_<sup>reg</sup> contains secondary-objective compromise, _r_<sup>con</sup> is the joint intervention of all enforced constraints, and _r_<sup>mod</sup> contains frozen-model and acceleration-measurement error. The split does not attribute _r_<sup>con</sup> to one individual active row; that would require a multiplier- or leave-one-constraint-out analysis. For the exact planar model _r_<sup>mod</sup> = 0. The FR3 audit evaluates the first two terms at 50 Hz manager updates and obtains _r_<sup>mod</sup> from the following 1 kHz plant sample. 

All four quantities retain physical acceleration units. They are logging and causal-diagnostic signals, not normalized cross-generator scores; a generator-relative or energynormalized metric would answer a different comparison question. 

This definition is intentionally stronger than commanding a nominal impedance force and penalizing 


The latter is controller-output tracking: it penalizes deviation from a nominal force command. _∥rk∥_<sup>2</sup> _W_<sup>istrackingtoo,but</sup> of a categorically different target — the _desired behavioral acceleration_ the generator specifies, not a prior controller’s output — so it compares two physical accelerations directly. In this paper that distinction is demonstrated for impedance and admittance, neither of which requires the QP to track a prior controller output. 

## _B. Implemented Behavior Layers_ 

The two behavior layers implemented below use the same QP template developed in Section III-C and differ only in ( _Cθ, Gθ_ ), as formalized by Theorem 1. The first is an impedance generator, whose desired impedance is 


For isotropic parameters, 


Unlike variable-impedance MPC (Section II), _Md, Dd, Kd_ are not decision variables in the present formulation; they describe the requested behavior. 

The second is a force-guided admittance generator, which requests a force-dependent velocity: 


or 


It has no position-restoring term. After force release, velocity decays and the displaced position is retained. This provides a qualitatively different behavior through the same acceleration interface. 

## _C. Predictive Realization Runtime_ 

Section III-B supplies _a_<sup>id</sup> . For a memoryless affine generator it is represented by _Cθ, Gθ_ , producing one condensed-QP template whose numerical cost coefficients change with the generator while its decision variable and feasible set do not. At time _k_ , let 


The controller solves 


Only _u_<sup>_⋆_</sup> 0 _|k_<sup>isexecuted.</sup><sup>_u−_1</sup><sup>_|k_inthe</sup><sup>_i_=0ratepenaltyand</sup> rate constraint denotes the command actually applied at the previous solve, carried by the controller between calls (zero before the first solve), so both are well-defined from the very first call. The implementation uses the measured force held constant across the horizon, _F_<sup>ˆ</sup> _h,i|k_ = _Fh,k_ , rather than oracle knowledge of the scripted force. A learned or physicsbased force predictor can be substituted without changing the generator interface. 

The objective _∥ai|k − a_<sup>id</sup> _i|k_<sup>_∥_</sup> _W_<sup>2istracking—ofacategor-</sup> ically different target than a position or velocity trajectory. No desired position trajectory is constructed; the optimizer instead compares two accelerations evaluated at the predicted interaction state: the acceleration the constrained robot will produce and the desired behavioral acceleration the generator specifies. Position and velocity enter as generator states and as safety-constrained quantities, never as tracked references in their own right. 

The optimization variable is the robot command sequence _Uk_ , not the generator’s parameters. The generator parameters _θ_ are fixed during each experiment. Switching from impedance to admittance changes _Cθ, Gθ_ , not the QP constraints or the 

6 

command variable — stated formally as Theorem 1 (Section IV). 

## IV. PROPERTIES OF THE AFFINE RUNTIME INSTANCE 

The architecture does not depend on the following QP property; rather, the property shows how cleanly the separation is realized for the present affine subclass. This section establishes template invariance, convexity, exact realization under idealized conditions, and one-step constraint inheritance, while Proposition 3 states explicitly what the runtime does not guarantee. 

**Theorem 1** (Affine-Generator Template-Invariance Property) **.** _Fix the plant_ ( _A, B, mr_ ) _, horizon N , weights_ ( _W, λu, λ_ ∆ _u_ ) _, and bounds_ ( _u_ max _, u_ ˙ max _, p_ max _, v_ max) _. There is a single map_ ( _C, G_ ) _�→ Q_ ( _C, G_ ) _— a quadratic-program template depending only on the plant, horizon, weights, and bounds above, never on θ — such that, for every generator θ with affine law_ ( _Cθ, Gθ_ ) _, the realization QP of Section III-C is exactly Q_ ( _Cθ, Gθ_ ) _. Consequently, for any two generators θ_ 1 _, θ_ 2 _, the instances Q_ ( _Cθ_ 1 _, Gθ_ 1) _and Q_ ( _Cθ_ 2 _, Gθ_ 2) _share the same decision variable Uk and the same feasible set, and differ only in the numerical objective coefficients contributed by_ ( _Cθ, Gθ_ ) _, not in the decision-variable dimensions, constraint set, or objective template. Realizing a different affine generator therefore changes only the supplied_ ( _Cθ, Gθ_ ) _. A nonlinear generator can make a_<sup>id</sup> _i|k_<sup>_nonlinearinUk,sotheresidualcost_</sup> _is no longer guaranteed convex quadratic and the template Q does not apply without linearization._ 

_Proof._ Every constraint in Section III-C’s QP — the dynamics recursion, the acceleration definition, and the four box constraints — is written in terms of _A_ , _B_ , _mr_ , _u_ max, _u_ ˙ max, _p_ max, _v_ max, _Uk_ , and the resulting state/acceleration sequence; none references _θ_ , _Cθ_ , or _Gθ_ . The feasible set is therefore a fixed polyhedron, identical for every generator. The only appearance of ( _Cθ, Gθ_ ) anywhere in the problem is the term _a_<sup>id</sup> _i|k_<sup>=</sup><sup>_Cθxi|k_+</sup><sup>_Gθ_ˆ</sup><sup>_Fh,i|k_insidetheprimarycost,entering</sup> exactly once per horizon step as an affine substitution into _ri|k_ = _ai|k − a_<sup>id</sup> _i|k_<sup>.Because</sup><sup>_xi|k_isitselfindependentof</sup> ( _Cθ, Gθ_ ) and affine in _Uk_ (established in Proposition 1’s proof below), _a_<sup>id</sup> _i|k_<sup>isaffinein</sup><sup>_Uk_with(</sup><sup>_Cθ, Gθ_)-dependent</sup> coefficients only, so _∥ri|k∥W_<sup>2isaconvexquadraticin</sup><sup>_Uk_</sup> whose Hessian and gradient contributions are determined entirely by ( _Cθ, Gθ_ ); the secondary terms _λu∥ui|k∥_ 2<sup>2and</sup> _λ_ ∆ _u∥ui|k −ui−_ 1 _|k∥_ 2<sup>2do not involve (</sup><sup>_Cθ, Gθ_) at all. Collecting</sup> these pieces defines _Q_ ( _C, G_ ) as a function of ( _C, G_ ) alone — the plant, horizon, weights, and bounds enter _Q_ as fixed parameters, not arguments — and by construction _Q_ ( _Cθ, Gθ_ ) is exactly the QP Section III-C poses for generator _θ_ . This is why Section III-B’s two implemented generators are checkable rather than aspirational: each supplies a different ( _Cθ, Gθ_ ) to the same template _Q_ . Without linearization, a nonlinear or stateful _fθ_ does not factor through a fixed ( _C, G_ ) pair and lies outside the theorem. 

**Proposition 1** (Convexity for affine generators) **.** _If W ⪰_ 0 _, λu ≥_ 0 _, and λ_ ∆ _u ≥_ 0 _, then the finite-horizon problem in_ 

_Section III-C is a convex quadratic program. It is strictly convex if the assembled Hessian is positive definite, including the common case λu >_ 0 _._ 

_Proof._ The lifted state _xi|k_ is affine in _Uk_ by the recursion _xi_ +1 _|k_ = _Axi|k_ + _B_ ( _ui|k_ + _F_<sup>ˆ</sup> _h,i|k_ ) unrolled from _x_ 0 _|k_ . Hence _ai|k_ = ( _ui|k_ + _F_<sup>ˆ</sup> _h,i|k_ ) _/mr_ and _a_<sup>id</sup> _i|k_<sup>=</sup><sup>_Cθxi|k_+</sup><sup>_Gθ_ˆ</sup><sup>_Fh,i|k_are</sup> affine in _Uk_ , so _ri|k_ = _ai|k − a_<sup>id</sup> _i|k_<sup>isaffinein</sup><sup>_Uk_and</sup><sup>_∥ri|k∥_</sup> _W_<sup>2</sup> is convex quadratic since _W ⪰_ 0. The regularization terms _λu∥ui|k∥_<sup>2</sup> 2<sup>and</sup><sup>_λ_∆</sup><sup>_u∥u_</sup> _i|k_<sup>_−u_</sup> _i−_ 1 _|k_<sup>_∥_</sup> 2<sup>2areconvexquadraticin</sup> _Uk_ for _λu, λ_ ∆ _u ≥_ 0, and a sum of convex functions is convex. Every listed constraint bounds an affine function of _Uk_ in absolute value, so the feasible set is an intersection of halfspaces, hence a convex polyhedron. 

**Proposition 2** (Exact unconstrained realization) **.** _Assume additionally that W ≻_ 0 _(strictly positive definite — a stronger hypothesis than Proposition 1’s W ⪰_ 0 _). Suppose an input sequence exists for which ri|k_ = 0 _over the horizon and no constraint is active. If the realization residual is optimized lexicographically before secondary effort objectives—or equivalently the secondary weights are zero—then every optimal primary solution realizes the reference dynamics exactly._ 

_Proof._ The primary objective<sup>�</sup> _i_<sup>_∥ri|k∥_</sup> _W_<sup>2isnonnegativeand</sup> attains the value zero at the assumed feasible sequence, so its minimum over the horizon is zero. Under lexicographic priority (or zero secondary weights), any optimal solution must attain this minimum, so<sup>�</sup> _i_<sup>_∥ri|k∥_</sup> _W_<sup>2= 0, and since each term</sup> is nonnegative, _∥ri|k∥W_<sup>2=0forevery</sup><sup>_i_.Because</sup><sup>_W≻_0,</sup> a quadratic form _∥r∥_<sup>2</sup> _W_<sup>vanishesonlyat</sup><sup>_r_=0;if</sup><sup>_W_were</sup> only positive semi-definite, this step would give _ri|k ∈_ ker _W_ rather than _ri|k_ = 0, which is why the stronger hypothesis is needed here but not in Proposition 1. 

With finite (not zero) secondary weights, predictive realization’s measured residual is not exactly zero even during unconstrained intervals (Table II), consistent with Proposition 2’s zero-weight idealization. The reactive comparator instead solves a different, unconstrained algebraic inversion of the generator’s instantaneous law, so its residual sits at numerical-solver tolerance (Table II) — a check that the underlying generator and dynamics model are implemented correctly, not itself an instance of Proposition 2. 

**Proposition 3** (One-step constraint inheritance) **.** _Assume the model and current human force are exact over the executed sample and the QP is feasible. Then u_<sup>_⋆_</sup> 0 _|k_<sup>_, p_1</sup><sup>_|k, and v_1</sup><sup>_|ksatisfy_</sup> _their corresponding QP bounds. Re-solving at every sample yields constraint satisfaction by induction while feasibility is retained._ 

This proposition is not a recursive-feasibility theorem. A deployable version requires a terminal invariant set, soft constraints with a quantified fallback, or a backup safe controller. Sudden force changes inside one sample and model error must also be covered by robust constraint tightening. 

## V. PLANAR ARCHITECTURE VALIDATION 

Section IV establishes what the QP guarantees in principle — convexity, exact realization when unconstrained, one-step 

7 


Fig. 2. Planar validation: impedance (left) and admittance (right). Dotted lines are state limits. Reactive clipping tracks the behavior but ignores the limits; predictive realization departs from it near the bound (final row). 

constraint satisfaction, and what it does not guarantee (recursive feasibility). This section tests those properties empirically on the planar plant of Section III-A, comparing predictive realization against the reactive comparator under identical command and rate limits. 

## _A. Reproducible Setup_ 

The simulation uses a 2.5 kg planar point mass, ∆ _t_ = 0 _._ 02 s, and a 20-step (0.4 s) horizon. A smooth 12 N force is applied along + _y_ from 1 s to 3 s. Limits are 


with _|u_ ˙ _j| ≤_ 180 N/s. The realization, force, and force-rate weights are 1, 2 _×_ 10<sup>_−_4</sup> , and 10<sup>_−_3</sup> , respectively. The impedance generator (Section III-B) uses 


The admittance generator (Section III-B) uses _Ta_ = 0 _._ 25 s and _Y_ = 0 _._ 025 m/(Ns). 

The comparator computes the instantaneous reference acceleration, converts it to robot force, and applies the same 18 N force and 180 N/s slew limits. It has no prediction of position or speed constraints. This comparator is intentionally minimal: it isolates what horizon-wide state constraints change; it is not presented as a survey-complete baseline. 

## _B. Results_ 

The impedance reference has a static displacement _Fh/Kd_ = 12 _/_ 45 = 0 _._ 267 m, matching the 0.266 m simulated peak after the smooth force ramp. Because this behavior is incompatible with the 0.10 m workspace, the predictive controller increases the realization residual while the bound is active. After release, it returns to the impedance equilibrium at the origin. 


Fig. 3. One controller instance; only .generator is reassigned at _t_ = 2 s and _t_ = 4 s. Position converges to the impedance equilibrium in both impedance segments, drifts under admittance in between, and re-converges after re-entry from a different state. 

The admittance reference requests approximately 0.30 m/s under 12 N and has no restoring spring. Reactive realization therefore accumulates 0.525 m displacement and retains it after release. The constrained controller begins departing from the requested velocity dynamics before reaching the workspace boundary and settles at 0.091 m. The generator remains unchanged. Table III shows that the observed modification is predominantly constraint intervention rather than secondary regularization; the stronger “entirely constraintinduced” wording would be false because the regularization term is small but nonzero. 

## _C. Online Generator Switching_ 

The preceding two subsections validate the generator interface by running two separate simulations, one per generator — informative, but not yet a demonstration that a single running controller accepts a different generator without redesign. This section tests that directly. One InteractionDynamicsMPC instance is constructed once, with the impedance generator; a small constant lateral force (1 N, well inside every bound) is applied for the entire 6 s run, with no release. At _t_ = 2 s and _t_ = 4 s, exactly one attribute is reassigned on the live controller — controller.generator — switching impedance _→_ admittance _→_ impedance; nothing else (the QP weights, constraints, decision variable, or the previous_command state carried between solves) is touched or reconstructed. 

Both switches are rate-bounded: the largest command-force jump at a switch instant is 3.02 N at _t_ = 4 s, 84% of the QP’s 3.6 N per-tick limit. This is a material command change, not evidence of mathematical smoothness; it simply satisfies the same discrete rate constraint that bounds every other step. Position and speed stay within 0.067 m and 0.083 m of the origin throughout, well inside the 0.10 m / 0.22 m/s bounds. The experiment therefore validates the software-level 

8 

TABLE II 

PLANAR VALIDATION. 

|Generator|Controller|RMSE<sup>_∗_</sup><br>(m/s<sup>2</sup>)|Peak _|pj|_<br>(m)|Peak spd.<br>(m/s)|Peak _|uj|_<br>(N)|Violation|
|---|---|---|---|---|---|---|
|Impedance|Predictive|1.351|0.100002|0.220|14.16|2_×_10<sup>_−_6 </sup>m|
|Impedance|Reactive|_<_10<sup>_−_6</sup>|0.2663|0.480|14.24|0.1663 m, 0.260 m/s|
|Admittance|Predictive|0.405|0.0912|0.169|12.88|none|
|Admittance|Reactive|_<_10<sup>_−_6</sup>|0.5250|0.300|12.00|0.4250 m, 0.080 m/s|


> _∗_ Realization RMSE, componentwise. State-limit violation reports the amount by which the 0.10 m / 0.22 m/s workspace/speed bound is exceeded. Realization RMSE for the reactive comparator is at numerical-solver tolerance because it directly inverts the generator’s instantaneous law; predictive realization’s nonzero residual reflects finite secondary weights and constraint-driven deviation, aggregated over the whole run (Proposition 2, Section IV). As in Table IV, RMSE is _component-wise_ : all residual components and time samples are pooled into one mean before the square root. 

TABLE III 

PLANAR RESIDUAL DECOMPOSITION (M/S<sup>2</sup> ). 

|Generator|Total|_r_<sup>reg</sup>|_r_<sup>con</sup>|Closure|
|---|---|---|---|---|
|Impedance|1.351|0.0113|1.339|_<_9_×_10<sup>_−_16</sup>|
|Admittance|0.405|0.00261|0.403|_<_3_×_10<sup>_−_16</sup>|


The first three numerical columns are component-wise RMSE and need not add as scalars; (18) closes samplewise. “Closure” is its maximum absolute component error. The planar model is exact, so _r_<sup>mod</sup> = 0. 

generator interface and feasibility of an online swap under the existing rate constraint; it does not establish optimal switching, hybrid stability, or continuity of the generator law. The second impedance segment additionally shows re-convergence from the different position and nonzero velocity left by the admittance segment without special-casing on re-entry. 

## _D. What the Experiments Establish_ 

The results support four limited claims: 

- 1) two qualitatively different affine interaction models use the same constrained predictive implementation; 

- 2) a constrained/unconstrained counterfactual separates constraint intervention from the small regularization component of total behavior error; 

- 3) horizon-wide state constraints prevent violations that command clipping alone cannot prevent in this deterministic model; 

- 4) a single controller instance accepts a different generator online, mid-run, by reassigning one attribute, with its command change bounded by the existing rate constraint. 

They do not establish manipulator-level feasibility, coupled human–robot stability, passivity, robustness to force-estimation delay, or real-time performance on embedded hardware. 

## VI. FR3 RUNTIME VALIDATION 

Section V isolates behavior–realization separation from kinematic and inverse-dynamics confounds by using a point mass. This section deploys the same interface on a torquecontrolled 7-DOF Franka FR3 simulated in MuJoCo, replacing the exact double-integrator plant with the nonlinear, configuration-dependent manipulator dynamics of Section III-A. 

## _A. Architecture_ 

At each solve, let _Jv_ ( _q_ ) _∈_ R<sup>3</sup><sup>_×_7</sup> be the translational Jacobian and Λ( _q_ )<sup>_−_1</sup> = _JvM_ ( _q_ )<sup>_−_1</sup> _Jv_<sup>_⊤_the(regularized)inverse</sup> operational-space inertia for the position coordinate. **Full closed-loop law.** Let _Rd_ be the held reference orientation, _eR_ ( _q_ ) _∈_ R<sup>3</sup> the corresponding orientation error, _Jw_ ( _q_ ) _∈_ R<sup>3</sup><sup>_×_7</sup> the rotational Jacobian, and _q_ 0 a fixed neutral configuration. The commanded joint torque is assembled from a feedforward term _τ_ ff , a raw orientation-hold term _τ_ orient, a raw null-space centering term _τ_ null, and their projection _τ_ aux through the null-space projector _N_<sup>¯</sup> _v_ : 


_τ_ base( _q, q_ ˙) = _τ_ ff ( _q, q_ ˙) + _τ_ aux( _q, q_ ˙) _,_ 

and the executed torque is 


Task acceleration obeys _y_ ¨ = _Jvq_ ¨ + _J_<sup>˙</sup> _v_ ˙ _q_ . Consequently, define 


which contains both the projected auxiliary-torque contribution and the task-kinematic term. The residual translational dynamics used by the QP are 


where the realized acceleration is _positive_ in the commanded force, matching the point-mass convention of Section III-A. _F_ cmd _∈_ R<sup>3</sup> , the QP’s Cartesian correction force, is supplied by whichever controller is active. The predictive controller sets _F_ cmd = _F_ 0<sup>_⋆_</sup> _|k_<sup>, the first element of the receding-horizon solution</sup> (Section III-C, condensed later in this section). The reactive comparator instead sets 


rate- and magnitude-limited to the same bounds as the predictive controller, with _a_<sup>id</sup> = _Cθx_ + _GθFh_ the instantaneous desired behavioral acceleration (Section III-B). Both controllers share the identical _τ_ base and torque-assembly step; they differ 

9 

only in how _F_ cmd is chosen. Thus the manipulator realization map changes, but the generator interface does not. 

_N_ ¯ _v_ ( _q_ ) is a dynamically consistent projector for the translation task [9]. Projecting both the orientation and null-space auxiliary torques through _N_<sup>¯</sup> _v_ ( _q_ ), rather than leaving either unprojected, prevents them from leaking into _e_ ¨ and inflating joint drift and the compensating Cartesian command. Because Λ uses Tikhonov regularization, _JvM_<sup>_−_1</sup> _N_<sup>¯</sup> _v_<sup>_⊤_=0holdsonly</sup> approximately; the remaining leakage and _J_<sup>˙</sup> _v_ ˙ _q_ are therefore retained in _d_ known. 

A six-second gain sweep over all four conditions (sweep_null_space_gains.py) exposed the remaining slow drift. With _k_ null = 10 _, d_ null = 2, configuration deviation reaches 1.32–1.85 rad and the reactive impedance condition exceeds a joint limit by about 1.6 N _·_ m. Gains 40/8 are the gentlest tested values that remove this violation and keep deviation below 0.29 rad; they are used in the benchmark. They also alter reactive task-space peaks (admittance 0.474 m to 0.107 m; impedance 0.158 m to 0.104 m), whereas predictive peaks stay near the 0.06 m workspace bound. Gains 100/20 reduce drift below 0.19 rad but suppress admittance further, including its predictive peak to 0.044 m. The selected gains therefore control drift but are not claimed to leave task-space behavior unchanged. 

The realization QP freezes Λ( _q_ )<sup>_−_1</sup> , _d_ known( _q, q_ ˙), _τ_ base( _q, q_ ˙), and _Jv_ ( _q_ ) at the current solve and holds them across the horizon. In compact form, its decision vector contains the Cartesian command sequence and nonnegative state slacks, 


This per-solve model is a convex QP but only a local predictor of the nonlinear MuJoCo plant. The hard torque constraint is imposed at every predicted step, rather than only _i_ = 0. It guarantees feasibility of the frozen-model command sequence returned by a successful solve; it is not a horizonwide guarantee for the future nonlinear trajectory. Executed torque is therefore recomputed and monitored at 1 kHz. 

The torque bound applies to the _total frozen-model torque τ_ base + _Jv_<sup>_⊤Fi_,becausethebasetermcanconsumeactuator</sup> budget before the interaction correction is added. A successful solve therefore satisfies the frozen-model limit by construction. If the desired behavioral acceleration requires more torque, the QP returns the closest feasible command and exposes the trade-off through _rk_ . 

The workspace and speed boxes use nonnegative slacks with _ρ_ = 10<sup>8</sup> , because the frozen-Jacobian model cannot guarantee recursive feasibility for the nonlinear plant. Nontrivial slack 

occurs in 110 impedance and 186 admittance solves, with peak position slack of 0.077 mm (impedance) and 0.027 mm (admittance) and peak speed slack below 10<sup>_−_6</sup> m/s in both conditions. This slack is smaller than Table IV’s executed peak _|ez|_ violation (0.0001 m impedance, 0.0001 m admittance) because the two measure different objects: slack is the QP’s own relaxation of its frozen-model prediction, while the executed violation is measured against the real nonlinear MuJoCo trajectory, which the frozen model only approximates. The separate reactive fallback for solver infeasibility is implemented but is not exercised: every reported solve is feasible. 

The fast control loop recomputes _τ_ base, the orientation term, and the null-space term from the current ( _q, q_ ˙) at 1 kHz; the QP is re-solved only every 20 ms (a 50 Hz outer loop), holding _F_ cmd between solves. Caching the full joint torque at the outerloop rate, rather than only the slow correction term, would confound any comparison of predictive against reactive control at a common inner-loop rate. 

## _B. Benchmark Scenario_ 

Mirroring the planar prototype’s own story rather than a separate benchmark design: the EE holds a fixed nominal pose and orientation while a sustained human push toward a workspace/speed boundary is applied, and predictive realization is compared against a command/rate-limited reactive controller with no predictive workspace handling, under an identical command/rate box. Neither controller has oracle knowledge of the scripted force; both receive a zero-order-hold forecast of the currently measured force, as in Section V. 

The push is a 20 N force along _−z_ with a raised-cosine ramp from _t_ = 1 _._ 0 s to 1 _._ 25 s, a hold to _t_ = 3 _._ 25 s, and a symmetric ramp-down to _t_ = 3 _._ 5 s. It is applied physically to the MuJoCo end-effector body, not only supplied to the controller’s model. 

The 2 s hold gives the admittance velocity time to approach steady state ( _Ta_ = 0 _._ 3 s), which is needed for the reactive comparator to approach the workspace bound and so yield a predictive-versus-reactive contrast for admittance. The impedance peak, determined by its equilibrium, is reached within 0.5 s regardless of hold length. 

The workspace/speed bound is 


the QP horizon is 15 steps (0.3 s) at ∆ _t_ = 0 _._ 02 s, and perjoint torque limits match the FR3 ( _±_ 87 N _·_ m for joints 1–4, _±_ 12 N _·_ m for joints 5–7). 

The impedance generator (Section III-B) uses _Md_ = 2 _._ 0 kg, _Dd_ = 28 Ns/m, _Kd_ = 200 N/m. The admittance generator (Section III-B) uses _Ta_ = 0 _._ 3 s and _Y_ = 0 _._ 01 m/(Ns). Each condition runs for 6 s of simulated time. 

## _C. Results_ 

No condition violates a per-joint torque limit at the executed sample, no solve is reported infeasible, and the torque constraint never binds in this primary benchmark: maximum 

10 

TABLE IV 

FR3 BENCHMARK. 

|Generator|Controller<br>R|MSE<sup>_∗_</sup><br>(m/s<sup>2</sup>)|Peak _|ez|_<br>(m)|Peak spd.<br>(m/s)|Torque util.|Violation|
|---|---|---|---|---|---|---|
|Impedance|Predictive<br>1.39|/ 1.45|0.0601|0.300|37.0%|0.0001 m|
|Impedance|Reactive<br>0.223|/ 0.062|0.1044|0.415|37.2%|0.0444 m, 0.065 m/s|
|Admittance|Predictive<br>0.212|/ 0.289|0.0601|0.070|34.4%|0.0001 m|
|Admittance|Reactive<br>0.200|/ 0.034|0.1066|0.041|31.7%|0.0466 m|


> _∗_ Residual RMSE, empirical / predicted. The _predicted_ residual uses the frozen local model of Section VI-A. The _empirical_ residual instead finite-differences the 1 kHz MuJoCo end-effector velocity and compares that acceleration with the generator request; it is the appropriate measure of behavior delivered by the simulated nonlinear plant. Their gap measures local-model and differentiation error, so the predicted residual must not be interpreted as an exact plant residual. As in Table II, both use component-wise RMSE: all three residual components and all time samples are pooled into one mean before the square root. This harmonizes the aggregation convention but does not make cross-plant values direct performance rankings. Speed is reported component-wise to match the box constraint. Maximum torque utilization is the largest ratio _|τj |/τ_ max _,j_ , which avoids comparing unlike 87 N _·_ m and 12 N _·_ m joint limits. Predictive solve times are reported in the text below because the reactive comparator does not solve a QP. 

TABLE V 

FR3 MANAGER-UPDATE RESIDUAL AUDIT (COMPONENT-WISE RMSE, M/S<sup>2</sup> ). 

|Generator|Model total|_r_<sup>reg</sup>|_r_<sup>con</sup>|_r_<sup>mod</sup>|Empirical total|Model closure|
|---|---|---|---|---|---|---|
|Impedance|1.448|0.285|1.205|0.199|1.395|_<_5_×_10<sup>_−_16</sup>|
|Admittance|0.283|0.0958|0.356|0.153|0.211|_<_3_×_10<sup>_−_16</sup>|


All columns use the 50 Hz manager-update instants; RMSE columns need not add because the vector terms can cancel. Model closure is the maximum absolute component error in _r_<sup>model</sup> = _r_<sup>reg</sup> + _r_<sup>con</sup> . _r_<sup>mod</sup> then closes (18) against the finite-difference plant acceleration. 


Fig. 4. FR3 benchmark: impedance (left) and admittance (right), predictive realization (solid) vs. the command/rate-limited reactive controller without predictive workspace handling (dashed). Dotted lines are workspace/speed bounds; bottom row is the empirical residual; torque does not clip in this primary benchmark. Predictive realization tracks the bound; the reactive controller overshoots and, for admittance, never recovers. 

utilization stays below 38%. This benchmark therefore evaluates behavior realization at a workspace boundary, not torque intervention. Section VI-D introduces a deliberately derated torque-budget stress case in which the constraint activates. 

An end-to-end unit test also tightens one joint limit until the horizon-wide constraint activates. 

The impedance reference has an unconstrained static displacement _Fh/Kd_ = 20 _/_ 200 = 0 _._ 10 m, which by itself already exceeds the 0.06 m bound. Reactive clipping tracks toward that equilibrium and peaks at 0.104 m (slightly above 

the static value, from the same ramp-overshoot effect as the planar case in Section V-B), overshooting the bound by 4.4 cm. Predictive realization instead departs from the desired behavioral acceleration while the bound is active, holding displacement to 0.0601 m. 

The admittance reference has no equilibrium displacement to compare against, only a steady-state velocity _Y Fh_ = 0 _._ 01 _×_ 20 = 0 _._ 2 m/s while the force is held, with no restoring term to pull it back after release. Reactive clipping accumulates displacement through the hold and continues briefly after force release before the velocity decays (time constant _Ta_ = 0 _._ 3 s), peaking at 0.1066 m — a 4.7 cm overshoot — and never recovers it, since the generator itself has no position-restoring term (Section III-B) and the reactive comparator has no lookahead to anticipate the boundary. Predictive realization begins departing from the requested velocity before the bound is reached and stays within 0.0601 m. 

Table V prevents the raw FR3 residual from being misread as constraint intervention alone. Constraint intervention is the largest component for both generators at manager updates, but finite regularization and plant/model terms are material, particularly for the admittance condition where vector cancellation makes the empirical total smaller than the individual component RMSE values. 

The deployed QP uses the exact variable change _z_ = 10<sup>3</sup> _s_ for each physical state slack _s_ . Constraint coefficients use _z/_ 10<sup>3</sup> , the slack Hessian weight becomes _ρ/_ 10<sup>6</sup> , and reported values decode _s_ = _z/_ 10<sup>3</sup> ; hence the physical objective and feasible set are unchanged. A unit test verifies this matrix transformation directly. It reduces the condensed Hessian condition number from 4 _._ 3 _×_ 10<sup>9</sup> to 4 _._ 34 _×_ 10<sup>3</sup> for impedance and from 3 _._ 8 _×_ 10<sup>9</sup> to 3 _._ 77 _×_ 10<sup>3</sup> for admittance. The deployed 50 Hz configuration also warm-starts OSQP from 

11 

the preceding primal/dual solution. 

A dedicated timing study (run_fr3_timing_study.py, five full 6 s repetitions and 1500 actual solves per generator/condition) then measures the complete QP construction and solve. In the deployed warm-started configuration, impedance has 3.45 ms mean, 6.89 ms 99th-percentile, and 8.67 ms maximum solve time; admittance has 3.68, 7.28, and 9.73 ms, respectively. Thus all 3000 measured warm-started solves meet the 20 ms manager period on the development machine. The matched cold-start ablation has means of 4.24 and 4.02 ms, 99th percentiles of 7.25 and 8.33 ms, and maxima of 17.73 and 14.92 ms; all 3000 cold solves also meet 20 ms in the saved scaled-formulation study. Warm-starting is therefore retained for additional margin, rather than being credited as the sole deadline fix. 

These wall-clock measurements are evidence for the tested machine, not a hard real-time or hardware-independent guarantee. They include QP construction and OSQP but exclude the post-solve unconstrained counterfactual used only for the residual audit. The simulator invokes the solve synchronously and does not implement asynchronous late-result discard; deployment on a different processor must re-run the timing test and, if overruns occur, hold the last applied command and reject stale solutions explicitly. 

## _D. Torque-Active Runtime Intervention_ 

The primary benchmark uses the nominal FR3 torque limits and does not activate them. To exercise runtime intervention without changing the behavior layer, we repeat the impedance condition with joint 4’s available budget deliberately derated from its nominal 87 N _·_ m to 31.5 N _·_ m. This is an artificial actuator-budget stress test, not a claim about the FR3’s physical rating. The 20 N force profile, impedance behavior, 0.3 s prediction horizon, QP weights, workspace/speed bounds, and 50 Hz solve rate remain unchanged. 

Two predictive runtimes are compared. The proposed runtime constrains total frozen-model torque at all 15 predicted steps. The ablation constrains the same torque only at _i_ = 0; its QP dimensions, behavior objective, state constraints, and command/rate bounds are otherwise identical. 

This experiment is not offered as another controller comparison. It tests the architectural responsibility assigned to the realization runtime: when a fixed behavior specification conflicts with an actuator budget, the runtime changes the command, exposes the resulting behavioral deviation, and avoids relying on an actuator-infeasible internal plan. The behavior layer itself is unchanged. 

## _E. Scope and What Remains_ 

This is a focused architecture validation, not a complete manipulator evaluation. The implemented behavior layers are impedance and admittance only; the scenario is a sustained push rather than a sweep over delay, sensor noise, or mass mismatch; and there is no collision constraint. The command/ratelimited reactive controller is a mechanism ablation, not a survey-complete baseline. The online behavior-layer switching 


Fig. 5. Torque-active intervention under a derated joint-4 budget. Horizonwide enforcement (blue) keeps the plan feasible; the first-step-only ablation (orange) satisfies only _i_ = 0 and plans an infeasible future during the ramp. Dotted lines are the derated budget and workspace bound. 

demonstration (Section V-C) is planar only; an FR3 counterpart remains future work. 

Human-participant and hardware validation remain future work, as do a faithful matched implementation of a predictive safety filter, predictive admittance controller, or MPIC baseline. Hardware timing and an explicit stale-solution policy must also be revalidated for deployment even though the warm-started development-machine study meets 20 ms. 

## VII. WHY BEHAVIOR–REALIZATION SEPARATION? 

Interaction behavior should specify only desired interaction dynamics; physical feasibility should be realized independently by the robot. Section I argued this from the different variables each side depends on; Sections III-B–VI tested it through one affine executable instance. This section defends the separation directly, against three natural alternatives. 

One alternative is to optimize behavior and robot commands jointly. Joint optimization is appropriate when behavior parameters are themselves task decisions, but separation instead makes a specification independently testable and replaceable while assigning feasibility to a stable downstream contract, at the cost that a fixed behavior layer may be suboptimal compared with a fully coupled design. This is an argument for a useful boundary, not a universal dominance claim. 

A second alternative is direct robot MPC or trajectory tracking, which chooses commands to minimize a task objective or evaluates success against a position/velocity reference. The runtime here instead receives a law evaluated at the predicted interaction state and measures whether the robot reproduces the requested response to contact, with no trajectory generated; MPC is only the current mechanism, while the architectural 

12 

TABLE VI 

TORQUE-ACTIVATION ABLATION. 

|Enforcement|Planned|Executed|RMSE<sup>_∗_</sup>|Peak|
|---|---|---|---|---|
||viol. (N_·_m)|viol. (N_·_m)|(m/s<sup>2</sup>)|_|ez|_ (m)|
|All 15 steps|0.0002|0.161|1.398|0.0603|
|First step only|11.329|0.380|1.466|0.0619|


> _∗_ Empirical residual RMSE. The planned violation is evaluated against the frozen model used by each QP. The all-step value is numerical solver tolerance, whereas the first-step-only runtime plans future torque up to 11.329 N _·_ m beyond the derated budget. Executed-sample torque is recomputed from the nonlinear MuJoCo state at 1 kHz; its smaller nonzero excess in both cases quantifies the local-model gap rather than a claimed hard nonlinear-plant guarantee. Horizon-wide enforcement reduces, but does not eliminate, that mismatch. The residual uses the component-wise convention of Tables II and IV. 

choice is what the optimizer receives and what discrepancy it reports. 

A third alternative is a reference governor, which modifies a reference upstream of an already-designed fixed controller. The realization layer here is instead itself the command optimizer, and its input is a desired-acceleration law rather than a setpoint for a separate inner loop. Both separate intent from constraint handling, so separation alone is not the novelty; the distinction is the interface boundary, online cross-behavior substitution, and the decomposition of desired-versus-realized acceleration. 

What separation buys, concretely, is controlled substitutability: Section V-C changes the behavior layer while preserving the realization object and its carried state, and Section VI-D changes the actuator budget while preserving the behavior — complementary tests of the same boundary, in which semantics can change without rebuilding feasibility logic, and feasibility can intervene without rewriting parameters. 

## VIII. LIMITATIONS AND OPEN THEORY 

The results above establish the architectural distinction on two plants, not everything a mature behavior-realization framework needs. Five gaps are worth stating plainly. 

First, the implemented behavior class is affine and memoryless; a stateful or learned model would need augmented prediction and explicit treatment of model uncertainty. 

Second, the realization cost does not itself imply passivity — a passive reference generator can be rendered non-passive by constraint-induced deviation or secondary optimization. A dissipativity constraint on the realized port variables, paired with an energy tank or passivity observer, is a natural extension. 

Third, hard state constraints can become infeasible after an unpredicted impulse (Proposition 3 flags this as a gap, not a guarantee). The FR3 study handles it operationally with slackrelaxed workspace/speed boxes and a reactive fallback on solver infeasibility; only the slack relaxation is exercised, and it stays small in the tested scenario. This does not establish a terminal invariant set, quantify soft-constraint risk, or validate the untriggered fallback — a deployable system would need all three. 

Fourth, the total realization residual has physical units and depends on the chosen output coordinates. Equation (18) now separates regularization, joint constraint intervention, and model error, but does not allocate intervention among individual constraint rows or provide a normalized severity score. The 

FR3 study exercises translation only; orientation is held by a fixed PD law, not a generator, so extending the interface needs a principled or energy-weighted normalization across coordinates. Raw RMSE across generators with different scales is not a direct performance ranking, and Table IV’s empirical and frozen-model residuals differ materially in several conditions — evidence of model-adequacy and estimation gaps, not a violation of Theorem 1. 

Finally, the architectural novelty must be assessed against the full literature of Section II, not only its closest precedents. The strongest eventual claim rests on implemented behaviorlayer substitutability, formal residual guarantees, and matched experiments, not terminology alone. 

## IX. CONCLUSION 

This paper’s contribution is architectural, not another interaction controller: desired-behavior specification and constrained robot realization are different responsibilities of robot-control software, made executable through a desiredacceleration interface and one predictive realization runtime for its memoryless affine subclass. The planar study swaps impedance for admittance and back while preserving the running realization object and its command state. The FR3 study instead changes the actuator budget while preserving the behavior layer: horizon-wide torque enforcement modifies the command, exposes the intervention through the constrained/unconstrained audit, and avoids the infeasible future plan a first-step-only ablation produces. Together these test both directions of the software boundary. The evidence is a reproducible proof of concept, scoped in Sections VI-E and VIII; future behavior layers may be physics-based, optimizationbased, or learned only once they expose a compatible realization contract. Interaction behavior should specify only desired interaction dynamics; physical feasibility should be realized independently by the robot. 

## REPRODUCIBILITY 

All experiments are driven by fixed, deterministic scenarios and are verified by an accompanying test suite that runs each scripted benchmark end to end and asserts its headline claims directly (torque-limit compliance, solver feasibility, workspace-bound margins, and the horizon-wide-versus-firststep-only comparison of Section VI-D). It also asserts samplewise closure of the residual decomposition on the planar and frozen FR3 models rather than relying on inspection of a saved 

13 

figure. Physical quantities (position, torque, and violation counts) are bit-for-bit reproducible from the fixed scenarios; solve times are wall-clock and are only ever bounded, never asserted exactly. The warm-start/Hessian-conditioning solvetime diagnosis of Section VI-C is produced by a dedicated script (run_fr3_timing_study.py) separate from the main benchmark, with unit tests checking the exact slackvariable matrix transformation, confirming that warm-starting converges to the same command as a cold solve, and verifying that resetting a controller clears its carried warm-start state. Code, configuration, and saved numerical artifacts backing every figure and table in this paper are available in the project repository. 

## REFERENCES 

- [1] A. Anand et al., “Deep Model Predictive Variable Impedance Control,” arXiv:2209.09614, 2022. 

- [2] K. Haninger, C. Hegeler, and L. Peternel, “Model Predictive Impedance Control with Gaussian Processes for Human and Environment Interaction,” _Robotics and Autonomous Systems_ , vol. 165, 104431, 2023. 

- [3] S. Xue et al., “Model predictive variable impedance control towards safe robotic interaction in unknown disturbance-rich environments,” _Robotics and Autonomous Systems_ , 2025. 

- [4] M. Sharifi, S. Behzadipour, and G. Vossoughi, “Nonlinear model reference adaptive impedance control for human–robot interactions,” _Control Engineering Practice_ , 2014. 

- [5] M. Bednarczyk et al., “Model Predictive Impedance Control,” in _Proc. IEEE Int. Conf. Robotics and Automation (ICRA)_ , 2020. 

   - [11] A. Bemporad, M. Morari, V. Dua, and E. N. Pistikopoulos, “The explicit linear quadratic regulator for constrained systems,” _Automatica_ , vol. 38, no. 1, pp. 3–20, 2002. 

   - [12] P. Tondel, T. A. Johansen, and A. Bemporad, “An algorithm for multi-parametric quadratic programming and explicit MPC solutions,” _Automatica_ , vol. 39, no. 3, pp. 489–497, 2003. 

   - [13] K. P. Wabersich and M. N. Zeilinger, “A predictive safety filter for learning-based control of constrained nonlinear dynamical systems,” _Automatica_ , vol. 129, Art. no. 109597, 2021. 

   - [14] A. Alharbat, H. Esmaeeli, D. Bicego, A. Mersha, and A. Franchi, “Three fundamental paradigms for aerial physical interaction using nonlinear model predictive control,” in _Proc. Int. Conf. Unmanned Aircraft Systems (ICUAS)_ , 2022, pp. 39–48. 

   - [15] A. Alharbat, C. Gabellieri, A. Mersha, and A. Franchi, “Predictive admittance control for aerial physical interaction,” _IEEE Robot. Autom. Lett._ , vol. 10, no. 11, pp. 11235–11242, 2025. 

   - [16] Q. Leboutet, E. Dean-Leon, F. Bergner, and G. Cheng, “Tactile-based whole-body compliance with force propagation for mobile manipulators,” _IEEE Trans. Robotics_ , vol. 35, no. 2, pp. 330–342, 2019. 

   - [17] S. S. Kumbhar, A. M. Kulkarni, and P. Artemiadis, “Efficient and compliant control framework for versatile human–humanoid collaborative transportation,” arXiv:2512.07819, 2025. 

   - [18] F. Lawan, X. Han, J. Carrasco, B. Lennox, and X. Cheng, “Safety-critical adaptive impedance control via nonsmooth control barrier functions under state and input constraints,” arXiv:2605.28367, 2026. 

   - [19] A. Del Prete, F. Nori, G. Metta, and L. Natale, “Prioritized motion– force control of constrained fully-actuated robots: Task Space Inverse Dynamics,” _Robotics and Autonomous Systems_ , 2014, doi: 10.1016/j.robot.2014.08.016. 

   - [20] J. Lee, S. H. Bang, E. Bakolas, and L. Sentis, “MPC-based hierarchical task space control of underactuated and constrained robots for execution of multiple tasks,” arXiv:2009.05891, 2020. 

- [6] T. Gold, A. Völz, and K. Graichen, “Model Predictive Interaction Control for Robotic Manipulation Tasks,” _IEEE Trans. Robotics_ , 2023. 

- [7] M. V. Minniti, R. Grandia, K. Fäh, F. Farshidian, and M. Hutter, “Model Predictive Robot-Environment Interaction Control for Mobile Manipulation Tasks,” in _Proc. IEEE Int. Conf. Robotics and Automation (ICRA)_ , 2021. 

- [8] E. Garone, S. Di Cairano, and I. Kolmanovsky, “Reference and command governors for systems with constraints: A survey on theory and applications,” _Automatica_ , vol. 75, pp. 306–328, 2017. 

- [9] O. Khatib, “A Unified Approach for Motion and Force Control of Robot Manipulators: The Operational Space Formulation,” _IEEE J. Robotics and Automation_ , vol. 3, no. 1, pp. 43–53, 1987. 

- [10] A. D. Ames, S. Coogan, M. Egerstedt, G. Notomista, K. Sreenath, and P. Tabuada, “Control Barrier Functions: Theory and Applications,” in _Proc. European Control Conference (ECC)_ , 2019. 

