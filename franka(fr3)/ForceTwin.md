---
title: "ForceTwin: Physics-informed Digital Twins for Robotic Manipulation from Instrumented Human Interaction"
date: "2026-09-18"
authors: "Tim Engelbracht; René Zurbrügg; Mayank Mittal; Marco Hutter; Marc Pollefeys; Hermann Blum"
url: https://arxiv.org/abs/2609.21751
pdf: https://arxiv.org/pdf/2609.21751
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2609.21751)** / [論文ページ](https://arxiv.org/abs/2609.21751)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ForceTwin: Physics-informed Digital Twins for Robotic Manipulation from Instrumented Human Interaction** 

Tim Engelbracht<sup>1</sup><sup>_,_†</sup> René Zurbrügg<sup>1</sup> Mayank Mittal<sup>1</sup><sup>_,_2</sup> Marco Hutter<sup>1</sup> Marc Pollefeys<sup>1</sup><sup>_,_3</sup> Hermann Blum<sup>4</sup> Zuria Bauer<sup>1</sup> 

> 1ETH Zurich 2NVIDIA 3Microsoft 4University of Bonn 


**Fig. 1. FORCETWIN builds a physics-informed digital twin from instrumented human interaction.** Interaction trajectories estimate object kinematics, while measured wrenches identify dynamics and mechanism behavior. Combined with semantic 3D scene reconstruction, FORCETWIN supports dynamicsaware robot control and high-fidelity simulation parameters for reinforcement learning. 

**_Abstract_ — Manipulating objects requires understanding not only their motion, but also the physical properties that determine it. For articulated objects, these include inertia, friction, and mechanisms such as springs or door closers, whose effects can vary with configuration and velocity. Such properties are not directly observable from appearance: visually identical doors may require very different effort to manipulate. Existing digital-twin pipelines recover primarily kinematics or assign static physical parameters from visual and language priors, which can yield physically implausible estimates. As a result, state-dependent mechanism dynamics remain unidentified and are not represented in standard asset formats. We present FORCETWIN, a system for identifying physics-informed digital twins of articulated objects from instrumented human interaction. A person probes an object using a handheld forcesensing gripper, providing synchronized poses and interaction forces from which we estimate the articulation, parametric dynamics including inertia, Coulomb friction, viscous damping, and a structured neural residual capturing state-dependent mechanism forces. FORCETWIN nearly halves the inertialparameter error of a VLM prior. As a feedforward dynamics model for impedance control on a Spot and a Franka FR3, FORCETWIN achieves 87% goal completion across nine objectembodiment pairs, compared with 60% using VLM-prior and 57% using kinematics-only twins, with the largest gains on** 

**objects whose strong mechanisms cause both baselines to stall. We further use the identified twins to train whole-body doortraversal policies and deploy them in the real world. Project page: timengelbracht.github.io/forcetwin-website** 

## I. INTRODUCTION 

Robotic manipulation requires more than knowing how an object can move. To open a drawer, a dishwasher, or a door with a closer, a robot must also account for the forces induced by inertia, friction, and internal mechanisms. These dynamics can vary substantially between visually similar objects and are often impossible to infer from appearance alone: the same drawer may be empty or heavily loaded, while a concealed closer can make an otherwise ordinary door strongly resist motion. A digital twin for manipulation must therefore capture not only an object’s geometry and articulation, but also the instance-specific dynamics that govern its interaction. 

These dynamics have to be measured. Appearance provides at best a prior, while motion alone identifies inertia, friction, and mechanism torque only up to a common scale that the contact wrench resolves. Feedback cannot simply replace the missing model: strong resistance may indicate that a drawer is stuck and the robot should stop, or be 

> †Corresponding author: tengelbracht@ethz.ch 

the expected behavior of a spring-loaded door that requires additional effort. 

Existing twin pipelines neither measure this effort nor model its state-dependent component. Reconstruction methods recover kinematic structure [1]–[4], while recent methods assign physical parameters from visual and language priors [5], [6]. Robot-probing approaches [7]–[9] measure interaction, but recover at most constant friction models and require robot deployment. None identify the nonlinear, statedependent response of mechanisms such as door closers or spring-loaded catches, which no set of constant parameters can describe, and standard asset formats provide no representation for this response. 

We take a different route (Fig. 2): a person measures the object. Handheld force-sensing grippers have made in-thewild interaction capture practical [10], [11]; we repurpose them for system identification. With FORCETWIN, a person probes an articulated object, and from the tool trajectory and contact wrenches we identify the object’s kinematics and dynamics (Fig. 1), decoupling identification from robot deployment. Humans can reach objects without a robot present, safely excite their full range across varied speeds, and do so faster than contact-based robot exploration. We model joint effort semi-parametrically. Inertia, Coulomb friction, and viscous damping are estimated under nonnegativity constraints, yielding physically valid parameters that map directly to simulators and controllers. A structured neural residual captures the remaining statedependent mechanism response. The resulting twin can be used directly for model-based control or exported as a simulation asset. 

In summary, our contributions are: 

- We introduce FORCETWIN, which identifies instancespecific articulated-object dynamics from instrumented human interaction, including nonlinear, state-dependent mechanism responses. 

- We formulate identification as a semi-parametric partially linear model, combining physically constrained inertia and friction parameters with a structured neural residual, yielding simulation-compatible parameters and a predictive model of joint effort. 

- We show that one identified twin serves both control and simulation. As the feedforward model of an impedance controller, it reaches 87% goal completion across nine object–embodiment pairs, where prior-based and kinematics-only twins reach 60% and 57% and stall entirely on objects with strong mechanisms; incorporated into simulation assets, the identified dynamics support policy learning, where we train whole-body door-traversal policies and deploy them in the real world. 

## II. RELATED WORK 

**Articulated Object Perception and Kinematics.** Estimating articulation models by acting on the world is a classic instance of interactive perception [12]: a robot pushes an 

object and infers its kinematic model from the observed motion [7], [13]. Later work removes the interaction, estimating articulation from a single RGB-D frame [14], from two observed object states [15], with learned categoryindependent models [16], or from in-the-wild video [17], and scene-graph pipelines lift such estimates to scene scale for robotic manipulation [1], [2], [4], [18]. All of these methods estimate kinematic structure, i.e., joint types and axes, but not the dynamic parameters that govern interaction forces; our kinematics stage builds on this line of work, adopting the twist formulation of works such as [16], [19] and interactive BIC-based model selection of [13], but treats the kinematic model as the input to dynamic identification rather than the final result. 

**Instrumented Interaction and Physical Model Identification.** Closest to our setting are methods that identify physical parameters from forceful interaction. Door inertia and a velocity-dependent deceleration profile have been identified from robot interaction and released-door trajectories [20], and human opening forces on doors and drawers have been captured with an instrumented hook, yielding force-versus-angle profiles used for haptic recognition and monitoring [21]. We share their premise that dynamics must be measured, but differ in what is recovered and for what: our semiparametric formulation yields interpretable, simulationready parameters plus a nonlinear mechanism model, rather than a per-object regression, and our capture requires only a handheld gripper rather than a robot. Robot-mounted estimators also go beyond kinematics: coupled recursive filters over vision, wrist forces, and proprioception additionally estimate a quasi-static Coulomb friction model, i.e., stiction and constant kinetic friction, while deliberately neglecting inertial and viscous effects [8], and factor-graph estimators use force factors to disambiguate the articulation but identify no dynamic parameters [9]. Our identification retains all of these terms, inertia, Coulomb and viscous damping, under physical constraints, and adds the nonlinear mechanism response. Ditto [22] builds “digital twins of articulated objects from interaction,” but its twins carry default physical parameters, while the dynamics parameters are not identified. Finally, handheld instrumented grippers [10], [11], [23] have made in-the-wild interaction capture practical, so far primarily to record demonstrations for policy learning; we repurpose this hardware for system identification. 

**Real-to-Sim and Simulation Asset Creation.** A complementary line of work turns real scenes into simulationready articulated assets: from images alone [24], from a robot push [25], through human-in-the-loop annotation [26], or by retrieving similar “digital cousins” from an asset database [27]. In all four, the resulting physics is defaulted, annotated, or inherited from the retrieved asset. A parallel thread assigns physical parameters from visual and language priors [3], [5], [6], fits them to visual tracking [28], or tunes simulator distributions against real task rollouts [29]. None of these approaches measure the interaction forces of the specific instance being modeled. FORCETWIN complements this line of work with per-instance dynamics, identified from 

force measurements and exported in a format such pipelines can consume. 

III. METHOD 

## _A. Problem Formulation_ 

We consider a rigid articulated part with a single degree of freedom and identify its kinematics and interaction dynamics from instrumented human probing. The observations consist of two synchronized streams, 


where<sup>_W_</sup> _T_ TCP _,i_ is the pose of the tool center point (TCP) in a world frame _W_ , and<sup>_W_</sup> _Fi ∈_ R<sup>6</sup> is the contact wrench applied by the tool to the object after compensating for the weight and inertial loading of the instrumented gripper. We assume that the tool maintains a rigid, non-slip grasp and that the articulated part follows an ideal revolute or prismatic joint during the retained measurements. Unless marked otherwise, all quantities are expressed in _W_ , and bold denotes a stacked multi-component quantity. From _D_ , we estimate the articulation class _κ ∈{_ revolute _,_ prismatic _}_ , the joint twist<sup>_W_</sup> _ξ_ , the observed range _Q_ = [ _q_ min _, q_ max], and a generalized-effort model _τ_ ˆ = _τ_ ˆ( _q,_ ˙ _q,_ ¨ _q_ ) _._ We represent the latter by simulator-compatible effective parametric coefficients _β_ = [ _µ, b, I_ ]<sup>_⊤_</sup> and a structured mechanism residual _M_ mech = _{gθ , cφ }_ . Together, these quantities form the physical model 


The model is estimated independently of a particular geometric reconstruction. A physics-informed digital twin is obtained afterwards by registering and associating _M_ phys with a geometric asset or a robot’s object representation. 

## _B. Kinematics Estimation_ 

Under the rigid-grasp assumption, the tracked TCP positions _{pi}_<sup>_N_</sup> _i_ =1<sup>followtheone-dimensionalmotionofthe</sup> articulated part. We represent this motion using a screw in product-of-exponentials form [13], [16], [30], 


where _p_ ¯ _i ∈_ R<sup>4</sup> denotes the homogeneous TCP position, _qi_ is the scalar joint coordinate, and<sup>_W_</sup> _ξ_ = [ _ω_<sup>_⊤_</sup> _, v_<sup>_⊤_</sup> ]<sup>_⊤_</sup> _∈_ R<sup>6</sup> is the joint twist, and [ _·_ ]<sup>_∧_</sup> maps a twist to its 4 _×_ 4 matrix form in se(3). We remove the scale ambiguity between _W ξ_ and _q_ by imposing _∥ω∥_ 2 = 1 for revolute joints and _∥v∥_ 2 = 1 for prismatic joints. We set the coordinate origin at the first retained configuration and orient the axis so that the first sustained displacement has positive _q_ . These conventions fix the units and signs of the subsequently identified dynamic parameters. A revolute candidate satisfies _ω̸_ = 0 and _ω_<sup>_⊤_</sup> _v_ = 0, while a prismatic candidate satisfies _ω_ = 0. We fit both candidates and select the articulation class using the Bayesian information criterion [13], [31]. We then refine the selected model in a factor graph, similar to [9], jointly estimating the joint geometry and the per-sample states _{qi}_ . For revolute joints, the refinement enforces zero screw pitch. The observed extrema of the refined states define _Q_ = [ _q_ min _, q_ max]. 

## _C. Dynamics Identification_ 

**Wrench Compensation and Generalized Effort.** The force-torque sensor measures both the contact wrench and the wrench generated by the instrumented gripper itself. We transform the measured wrench into the world frame and subtract the calibrated gravitational and inertial wrench of the gripper, yielding the estimated contact wrench<sup>_W_</sup> _Fi_ applied by the tool to the object. We order spatial twists as angular followed by linear velocity and wrenches as moment followed by force. The kinematic estimate then defines the object Jacobian at the TCP, 


where _o_ is a point on the revolute axis, and _Jp_ denotes the linear block of _J_ obj, the three rows that map _q_ ˙ to the TCP velocity. By virtual work, the generalized effort applied by the tool is _τi_ = _J_ obj( _qi_ )<sup>_⊤W_</sup> _Fi._ Under the rigidgrasp and ideal-joint assumptions, wrench components that perform no virtual work along the permitted articulation lie in the null space of _J_ obj<sup>_⊤_anddonotcontributeto</sup><sup>_τi_.</sup> The projection does not remove errors caused by wrench calibration, joint-axis estimation, grasp compliance, or slip; these effects remain part of the measurement residual. We obtain _q_ ˙ _i_ and _q_ ¨ _i_ by differentiating a smoothed joint-state trajectory. Samples near joint limits, with negligible velocity, or with implausibly large differentiated accelerations are removed using excitation gates. 

**Generalized-Effort Model.** We define _τi_ as the generalized effort applied to the object and model the effort required to realize the observed motion as 


The sign convention in Eq. (5) describes the effort that must be applied to move the object. Consequently, the compensating damping effort is + _cφ_ ˙ _q_ . The corresponding damping effort exerted by the object is _−cφ_ ˙ _q_ , whose mechanical power is 


when _cφ ≥_ 0. The function _gθ_ ( _q_ ) captures configurationdependent generalized loads. For joints whose motion is orthogonal to gravity, this term primarily represents mechanisms such as door closers and spring-loaded elements. For a horizontal revolute axis, it may also contain gravitational torque unless gravity is compensated using an independently available mass and center-of-mass estimate. We therefore interpret _gθ_ as a configuration-dependent load rather than claiming that it uniquely isolates a mechanical spring. **Residual Fitting.** We first estimate the effective parametric coefficients using samples with sufficient motion and force 


Fig. 2: **The FORCETWIN pipeline.** Instrumented human interaction provides synchronized tool poses and contact wrenches from which we identify an articulation model and its generalized-effort dynamics. Geometry is reconstructed from the same recording or supplied independently, and the physical model is registered to it to produce a twin for robot control or simulation. 

excitation. For sample _i_ , define 


Stacking the retained regressors into _Z_ gives 


The elementwise nonnegativity constraint enforces nonnegative effective inertia, Coulomb friction, and viscous damping. These quantities correspond to properties commonly supported by rigid-body simulators, although their exact interpretation and implementation remain backend-dependent. We next fit the structured nonlinear model to the residual 


using _r_ ˆ _i_ = _τ_ mech( _qi,_ ˙ _qi_ ) _, cφ ≥_ 0 _._ The configurationdependent head _gθ_ is sign-unconstrained and takes only _q_ as input. The damping coefficient is produced by softplus outputs, with separate heads for positive and negative motion, allowing directional asymmetry while preserving nonnegative damping. The resulting model is partially linear, but its decomposition is not generally unique. In particular, a constant component of _cφ_ is indistinguishable from the linear damping coefficient _b_ , and configuration-dependent gravity is indistinguishable from a mechanical load represented by _gθ_ . Correlations between _q_ , _q_ ˙, and _q_ ¨ can introduce further coupling between the fitted terms. We therefore interpret _β_<sup>ˆ</sup> as effective simulator-compatible parameters and evaluate the predictive fidelity of the complete effort model. The structured residual and probing protocol regularize the decomposition, but do not make every component uniquely identifiable. We fit the model sequentially: nonnegative least squares followed by residual-network training. Training minimizes residual MSE using full-batch AdamW (learning rate and weight decay 10<sup>_−_3</sup> ), with a random 75/25 training/validation split, at most 1200 epochs, and early stopping after 120 epochs without validation improvement; we retain the bestvalidation weights for the mechanism term. 

_D. Twin Assembly_ 

The identified physical model is expressed in the probing frame _W_ and joint coordinate defined above. To attach it to a target geometric representation with frame _A_ , we first register the probing frame using<sup>_A_</sup> _TW_ . The joint twist transforms according to<sup>_A_</sup> _ξ_ = Ad _ATW W ξ ._ Rigid frame changes preserve the scalar joint coordinate and generalized effort. If the target asset instead uses a different coordinate convention 


we transform the valid range and reparameterize the mechanism model. For the complete mechanism effort _τ_ mech( _q,_ ˙ _q_ ), the target convention uses _τ_ mech<sup>_A_(</sup><sup>_qA,_˙</sup><sup>_qA_)=</sup><sup>_sτ_mech</sup> � _s_ ( _qA − q_ off) _, sq_ ˙ _A_ � . The nonnegative magnitudes _I_ , _µ_ , and _b_ are unchanged under the sign reversal, while their associated signed efforts follow the transformed joint coordinate. We then associate the registered model with the corresponding articulated instance, as illustrated in Fig. 3. The parametric dynamics are mapped to the corresponding joint or actuator properties provided by the target backend. When the backend supports runtime joint-effort evaluation, the nonlinear model is evaluated directly. For backends that cannot execute the learned network, we approximate it with a backendsupported spring-damper representation during export. This conversion is distinct from physical identification and may introduce an additional approximation. In our experiments, the geometric representation is reconstructed from the same recording, so it already shares the probing frame. We associate the manipulated handle with the tracked TCP and use the reconstructed functional relation to identify the corresponding panel. Other geometric backends or existing assets require only a registration and an instance-association procedure. The resulting twin can be consumed either as a feedforward dynamics model for robot control or as an articulated simulation asset. 


Fig. 3: **Construction of a physics-informed twin.** (a) Reconstructed panel instance, associated handle, and registered joint axis. (b) Exported articulated twin. The physical model is transformed into the asset frame, reparameterized to match its joint-coordinate convention, and attached to the corresponding articulated instance. 

## IV. EXPERIMENTS 

Evaluation proceeds along two axes. First, we ask whether the estimated parameters are accurate and whether that accuracy justifies the model’s complexity: Section IV-B measures fidelity against ground truth inertia measurements and realworld behavior, and Section IV-C investigates the contribution of each model component. Second, we investigate the utility of ForceTwin: Section IV-D deploys the twin as a feedforward dynamics model on two physical robots, and Section IV-E exports it as a simulation asset for policy learning. All experiments follow the capture protocol of Section IV-A. 

## _A. Capture Protocol and Implementation_ 

We capture all interactions with the handheld Hoi! gripper [10], which provides posed RGB-D observations, the tool trajectory from Project Aria MPS [32], and the contact wrench from a wrist-mounted force-torque sensor. Once a part is grasped, we open and close it over a range of speeds and accelerations chosen to excite the individual regressor axes: slow, low-acceleration motion for Coulomb friction, a wide speed spectrum for viscous damping, high accelerations for inertia, and passive following for the mechanism. Fig. 4(b) shows an example probing sequence. In our implementation, FunFact [18] reconstructs panels, handles and functional relations from the same recording and therefore already shares the probing frame; we identify the manipulated handle by proximity to the tracked TCP, use FunFact’s handle-to-panel relation to select the associated door or drawer panel, attach the recovered model to that pair, process the instance meshes, and export the articulated asset to USD. Because _M_ phys is independent of the geometric representation, it can equally be registered onto an existing asset: the real-to-sim free-swing experiments of Section IVB use the exported asset, while the policy-learning experiments of Section IV-E attach the identified dynamics and mechanism to the door asset of the training pipeline, leaving its geometry unchanged. In both cases the identified _β_<sup>ˆ</sup> is written directly to the joint’s inertia, friction and damping fields, so the parametric half of the twin is native to the 


Fig. 4: **Dynamics model fit for the wood door.** (a) Measured generalized effort (gray) against the parametric model alone (dashed) and with the structured mechanism added (green); (b) the probing trajectory. The parametric model tracks the shape of the effort but is offset from it by a configuration-dependent amount, which the learned mechanism recovers. Shaded bands mark the probing regimes for inertia (yellow), viscous damping (purple), and the mechanism (blue). 

simulator, while the mechanism term is evaluated per step as a state-dependent joint effort. An independently obtained representation has to be registered to the probing frame first. 

## _B. Estimation Fidelity_ 

We evaluate estimation accuracy at three levels: kinematic parameters, compared against annotated ground-truth axes on the real-world test rig; inertial parameters, whose ground truth can be independently measured (unlike friction parameters, for which no such reference exists); and finally aggregate system fidelity, where kinematic and dynamic terms are evaluated jointly. 

**Kinematics Estimation.** We evaluate articulation types and axes on our real-world test bench against ground truth annotated in a Leica RTC360 laser scan [10], [17]. After registering estimates to the scan, we measure axisangle errors for both joint types and axis-position errors for revolute joints [2], [17]. We compare against MoMaSG [2], which tracks object points during non-instrumented human interaction and is run on our interactions, and OPDMulti [14], which estimates articulation from visual input without interaction. Interaction-based methods outperform the visual baseline (Table I). OPDMulti estimates prismatic directions reasonably well (4 _._ 8<sup>_◦_</sup> ), but yields large revoluteaxis errors (34 _._ 9<sup>_◦_</sup> ) and only 54 _._ 1% revolute type accuracy; both interaction-based methods classify all joints correctly. Compared with MoMa-SG, our method slightly improves revolute-axis orientation (1 _._ 5<sup>_◦_</sup> vs. 1 _._ 7<sup>_◦_</sup> ) and halves position error (23 vs. 46 mm). We attribute this improvement to directly measured tool poses, avoiding reliance on surfacepoint tracking susceptible to low texture and motion blur. **Dynamics and Mechanism Estimation.** We next assess the fidelity of our estimated dynamics parameters against a prior-based paradigm such as [5]. We focus on the inertial parameters, since ground truth is readily obtainable for them. 

TABLE I: **ARTICULATION AXIS ESTIMATION.** Evaluated on the real-world test bench against 12 axes annotated in a Leica RTC360 laser scan. Metrics follow ArtiPoint [17]: _θ_ err is the angle between axis lines, folded to [0 _,_ 90]<sup>_◦_</sup> , and _dL_ 2 the distance between revolute axis lines along their common perpendicular. Errors accumulate only over predictions with the correct joint type. Values are means with the sample standard deviation in smaller type;<sup>†</sup> no deviation available. **Bold** indicates best performance, <u>underline</u> second best; tied entries are all marked best. 

||**Prismatic**|**Re**|**volut**|**e**|**Type acc.**|[%] _↑_|
|---|---|---|---|---|---|---|
|**Method**|_θ_err [<sup>_◦_</sup>] _↓_|_θ_err [<sup>_◦_</sup>] _↓_|_dL_2|[mm] _↓_|**Pris.**|**Rev.**|
|FORCETWIN (Ours)|**1.4**_±_0.2|**1.5**_±_0.8||**23**_±_26|**100.0**|**100.0**|
|MoMa-SG [2]|1.6<br>_±_0.8|1.7<br>_±_0.0||46<br>_±_20|**100.0**|**100.0**|
|OPDMulti [14]|4.8<sup>†</sup>|34.9_±_29.1||143_±_117|**100.0**|54.1|


Fig. 5: **Inertial-parameter fidelity on the four objects for which ground truth is available:** estimate against ground truth on logarithmic axes, so an estimate on the diagonal is exact and vertical distance from it is the error. Marker shape distinguishes revolute (circle) from prismatic (square) joints, whose parameters carry the two units given on the axes. Nested shaded bands mark agreement to within _±_ 25% (inner) and to within a factor of two (outer). The macro mean of the absolute relative errors is 29 _._ 5% for FORCETWIN and 53 _._ 0% for the VLM prior. 

For prismatic joints this is the mass, measured with a scale. For revolute panels, the hinge inertia follows from mass and geometry as _I_ =<sup><u>1</u></sup> 3<sup>_mℓ_2undertheassumptionofconstant</sup> density, while compact parts such as locks and handles are treated as point masses with _I_ = _mℓ_<sup>2</sup> . Here _ℓ_ is the distance from the hinge axis: the panel’s extent from the hinge in the first case, and the radial offset of the part in the second. No ground truth is available for the parametric friction parameters or for the nonlinear MLP. To still evaluate these terms, we assess the aggregate fit at the system level: the real-to-sim free-swing experiment below compares the closing behavior of the real object with that of its simulated twin. Fig. 4 shows a qualitative example of the fit. The parametric model tracks the measured effort qualitatively, but with a non-constant offset that reveals the mechanism it cannot represent. Aggregated over all objects (Fig. 5), the interaction-based estimate is more accurate than the priorbased one (29 _._ 5% vs. 53 _._ 0% macro mean absolute relative error), and it is the better estimate on three of the four objects for which ground truth is available. Our accuracy improves systematically with the magnitude of the inertial parameter: the two heaviest parts are estimated to within 

10 _._ 4% and 13 _._ 7%, whereas the lightest ones reach 63 _._ 8% and 30 _._ 2%. We attribute this to the signal-to-noise ratio of the measurement rather than to the estimator itself, as light parts excite only small interaction forces, so that the force-torque noise band occupies a larger fraction of the measured signal. Consistently, the sole case in which the prior-based baseline is more accurate is the smallest object in the set. The prior-based baseline underestimates the inertial parameter for every object, despite being provided with scale information and prompted to reason about material. The largest error occurs for the heavy drawer (83 _._ 5%), whose effective mass is dominated by its contents, hidden state that cannot be inferred from appearance. Our estimator, in turn, overestimates on all four objects. The bias is consistent in sign, which suggests that residual unmodeled effort is partially absorbed into the inertial term during the parametric fit. This reflects a structural property of the decomposition rather than insufficient optimization: both the parametric terms and the mechanism response depend on the articulation velocity, so the split between them is only partially identifiable from torque observations, and the fit objective is predictive accuracy rather than parameter recovery. The downstream uses of the twin consume the full torque model, whose aggregate fidelity is assessed at system level by the free-swing experiment below. 

**System-Level Fidelity: Real-to-Sim Free Swing.** The preceding experiment evaluates individual parameters, but only the inertial ones admit ground truth. We therefore assess the twin at the system level, where inertia, friction and mechanism act jointly. We release the metal door and the wood door from 45<sup>_◦_</sup> and 90<sup>_◦_</sup> and compare the measured closing time against simulations parameterized either by our interaction-derived estimates or by the VLM-prior baseline. Our estimates yield the lower error in all four conditions (Table III), reducing the macro mean from 57 _._ 7% to 16 _._ 3%. The VLM-prior baseline closes every door in roughly 2 s regardless of door or release angle, indicating that it does not match the damped dynamics closely. Note that this measure is aggregate and not injective: a large mismatch proves the dynamics are wrong, but a close match does not uniquely identify the individual parameters, since compensating errors could in principle yield the same closing time. It therefore complements the parameter-wise evaluation above. 

## _C. Model-Class Ablations_ 

We evaluate the benefit of added model complexity. Adding viscous damping to the Coulomb-inertia model reduces in-sample effort RMSE by up to 12%. Adding the structured mechanism reduces it by a further 67 _−_ 73% on mechanism-dominated parts such as the doors and the oven, against 12% on the sliding door, which has no mechanism. We fit the two stages sequentially, the parametric coefficients first and the mechanism on their residual. Alternating between them changes the fit RMSE by less than 5% of the parametric baseline while redistributing effort between overlapping terms, so we do not iterate. 

TABLE II: **REAL-ROBOT ARTICULATION.** Spot and Franka FR3 track robot-specific opening goals within 6 s using a fixed controller. FORCETWIN uses interaction-identified dynamics; VLM prior uses visual and language estimates [5], [6]; Kinematics only omits dynamics compensation [2], [3]. _Complete_ : maximum goal completion (capped at 100%). _Track_ : goal-normalized tracking RMSE (%). Values are means with sample SD; the overall mean equally weights nine object–robot pairs. _Mechanism_ rates the contribution of built-in mechanisms to articulation force. Objects are ordered by FORCETWIN tracking error within each robot panel. **Bold** <u>/underline:</u> best/second best per object and metric, with ties marked best. 

TABLE III: **REAL-TO-SIM FREESWING FIDELITY.** Closing times of the physical door and of twins parameterized by our interaction-derived estimates and by the VLM prior, released from two initial opening angles _q_ 0. Times are in seconds and the absolute relative error (ARE) is a percentage. The final row is the equal-weight macro mean. Only two estimates are compared, so **bold** marks the lower ARE and no second rank is reported. 

||||**FORCETWI**|**N (Ours)**|**VLM p**|**rior**|**Kinematic**|**s only**|
|---|---|---|---|---|---|---|---|---|
||**Object**|**Mechanism **|**Complete** _↑_|**Track** _↓_|**Complete** _↑_|**Track** _↓_|**Complete** _↑_|**Track** _↓_|
||Drawer|Weak|88.0_±_1.8|**9.2**_±_2.9|**95.2**_±_4.0|34.1<br>_±_3.1|90.6<br>_±_3.7|38.0_±_2.6|
|**t**|Sliding door|None|**100.0**_±_0.0|**10.5**_±_1.9|**100.0**_±_0.0|15.4<br>_±_1.9|**100.0**_±_0.0|18.5_±_2.6|
|**po**|Wood door|Medium|**100.0**_±_0.0|**14.0**_±_1.5|91.2<br>_±_0.9|24.3<br>_±_0.0|88.3_±_4.7|27.3_±_1.6|
|**S**|Oven|Strong|**100.0**_±_0.0|**33.3**_±_3.1|4.0<br>_±_0.7|91.1<br>_±_0.4|2.2_±_0.1|91.9_±_0.2|
||Metal door|Strong|N/A|(object f|orces exceed|Spot’s actu|ation limits)||
||Sliding door|None|93.7_±_0.7|**10.5**_±_0.4|98.7<br>_±_1.0|17.2<br>_±_0.9|**99.3**_±_1.0|26.9_±_12.2|
|**ka**|Drawer|Weak|85.6<br>_±_9.6|**17.6**_±_3.2|**93.1**_±_3.2|37.0_±_0.4|85.1_±_11.2|22.4<br>_±_4.2|
|**an**|Metal door|Strong|**81.2**_±_3.5|**24.4**_±_5.5|1.6<br>_±_0.0|91.0<br>_±_0.0|1.5_±_0.0|91.0<br>_±_0.0|
|**Fr**|Wood door|Medium|**69.8**_±_19.4|**30.3**_±_11.0|51.7<br>_±_4.0|47.7<br>_±_2.8|44.0_±_21.3|56.0_±_16.6|
||Oven|Strong|**67.6**_±_0.0|**49.7**_±_0.0|1.8<br>_±_1.0|90.8<br>_±_0.9|0.9_±_0.1|91.6_±_0.1|
|**O**|**verall mean**||**87.3**|**22.2**|59.7|49.8|56.9|51.5|


||||**For**|**ceTwin**|**VLM**|**prior**|
|---|---|---|---|---|---|---|
|**Object**|_q_0 [<sup>_◦_</sup>]|**Real** [s]|_t_ [s]|**ARE** _↓_|_t_ [s]|**ARE** _↓_|
|Metal door|45|5.6|5.9|**5.4**|2.1|62.5|
|Metal door|90|8.4|8.8|**4.8**|2.5|70.2|
|Wood door|45|3.7|5.0|**35.1**|2.0|45.9|
|Wood door|90|5.0|6.0|**20.0**|2.4|52.0|
|Macro mean|–|–|–|**16.3**|–|57.7|


We report goal completion and goal-normalized tracking RMSE. Table II reports goal completion and tracking error on five objects across Spot and Franka FR3 under a common 6 s goal. FORCETWIN yields the lowest tracking error on every object and the highest macro mean completion (87 _._ 3%, against 59 _._ 7% for the VLM prior and 56 _._ 9% for kinematics only), and the margin scales with the dynamic load. On the drawers and sliding doors all three models complete the goal, and the identified model improves tracking error by factors of 1 _._ 3 to 4. On the strong-mechanism objects, the oven on both robots and the metal door on the Franka, both baselines stall below 5% completion because their feedforward supplies only a fraction of the required force, while the identified model reaches 67–100%. The wood door lies between these regimes on both embodiments, where the baselines lose 9–26 percentage points and roughly double the tracking error. 

Fig. 6: **Real-world experiments of zero-shot model-based articulation** (Table II) across two embodiments: Spot and Franka FR3. We visualize the initial and final articulation states as blended overlays for both embodiments. The recovered quasi-static mechanism torque for each object is plotted over the opening trajectory, highlighting the variation in mechanism behavior across objects. 

## _D. Does Dynamics Fidelity Change Manipulation?_ 

This experiment evaluates whether the fidelity of a twin’s dynamics influences manipulation performance: We use ForceTwin’s object dynamics as a feedforward term of a Cartesian impedance controller, 

## _E. The Twin as a Training Asset_ 

Beyond the feedforward evaluations above, we show that the identified models can be used directly for reinforcement learning. We register the identified wood- and metal-door dynamics, including the recovered nonlinear closing mechanism, onto the door asset in Isaac Lab [34]. Using the motion-imitation pipeline from [35], we train whole-body door-traversal policies. That pipeline randomizes the door parameters during training; here we replace that randomization with the identified dynamics, leaving the policy architecture and training procedure unchanged. We deploy both policies on an ANYmal quadruped with an arm and evaluate them on the two real doors. The wood-door policy succeeds on the wood door in all five trials. The metal-door policy also succeeds on this door, but exhibits a stop-and-go motion: it advances the door and then pauses while the imitation phase catches up (Fig. 7). On the metal door, the metal-door policy succeeds, whereas the wood-door policy fails its initial opening attempt. These experiments demonstrate that the identified models integrate into an existing policy-learning pipeline and support real-world deployment on contact-rich whole-body tasks. Whether training with identified dynamics 

**f** cmd = _Kx_ ( _xd − x_ )+ _Dx_ ( _x_ ˙ _d − x_ ˙)+ **f** ff _,_ 


where the bracket sums the generalized effort of the identified inertia, Coulomb and viscous damping, and mechanism response along the reference articulation trajectory _qd_ ( _t_ ), and the transposed pseudoinverse of the object Jacobian’s linear block _Jp_ maps them to an end-effector force added to the impedance feedback. The twin enters only through **f** ff, so we vary its source across the two prevalent twin-construction paradigms and ours, keeping robot, controller, and task fixed: kinematics-only twins [2], [3], [14], [33] provide _Jp_ but no dynamics ( **f** ff = **0** ), VLM-prior twins [5], [6] supply prior-based parameter estimates to the same feedforward, and FORCETWIN supplies the parameters identified from instrumented interaction. In each trial, the robot starts with the handle grasped and tracks _qd_ ( _t_ ) from the closed configuration to an embodiment-specific goal within 6 s (Fig. 6); 


Fig. 7: **Policy learning with identified door models. Left:** We use the identified wood- and metal-door models (real-to-sim) to train whole-body policies, which we then deploy on ANYmal (sim-toreal). **Right:** Both policies on the real wood door; shaded regions show the average over five trials. The wood-door policy moves the end-effector smoothly, while the metal-door policy stops and starts, pulling hard and then pausing, which gives it higher jerk (bottom) due to the worse sim-to-real calibration. 

consistently improves performance over domain randomization requires a controlled comparison, which we leave to future work. 

## V. LIMITATIONS 

Our decomposition of the effort model is not unique: a constant mechanism damping is absorbed by _b_ , and any configuration-dependent load by _gθ_ , including gravity when the joint axis is not vertical. The model is memoryless in ( _q,_ ˙ _q_ ), so hysteresis, backlash, stiction at rest, and latch states lie outside its class, and both _gθ_ and the joint range hold only where the object was probed. Further, identification is per instance and needs physical interaction: each part is probed individually, and the probing has to excite the individual regressor axes, so passive demonstration recordings do not suffice. Priors scale across a scene where probing does not, so the two are complementary, and transferring identified dynamics to parts that were not probed is left to future work. Identification is also one-shot: a loaded drawer or a readjusted closer changes the object, and refining a twin online from the robot’s own interaction forces remains open. 

## VI. CONCLUSION 

FORCETWIN identifies physics-informed digital twins of articulated objects from instrumented human interaction. A person probes the object with a handheld force-sensing gripper, and from the tool trajectory and contact wrenches we recover the articulation, effective inertia, Coulomb and viscous terms under nonnegativity constraints, and a residual for the nonlinear mechanism. The identified parameters nearly halve the inertial error of a prior-based estimate and reproduce measured door-closing times. A single twin then serves two uses: as the feedforward model of an impedance controller, it operates objects on which kinematics-only and prior-based twins stall, and exported to simulation it is used to train whole-body door-traversal policies transferring to the real objects. 

### ACKNOWLEDGEMENTS 

This work was supported by SNSF Advanced Grant 216260, the Lamarr Institute, and Google. The authors used generative AI to assist with drafting and editing the manuscript, cleaning up figures and coding; all content was reviewed by the authors, who take full responsibility for it. 

## REFERENCES 

- [1] Q. Gu _et al._ , “ArtiSG: Functional 3D Scene Graph Construction via Human-demonstrated Articulated Objects Manipulation,” _arXiv:2512.24845_ , 2026. 

- [2] M. Büchner _et al._ , “Articulated 3D Scene Graphs for Open-World Mobile Manipulation,” _arXiv:2602.16356_ , 2026. 

- [3] Z. Huang _et al._ , “REACT3D: Recovering Articulations for Interactive Physical 3D Scenes,” _IEEE RA-L_ , 2026. 

- [4] A. Yu _et al._ , “Pandora: Articulated 3D Scene Graphs from Egocentric Vision,” _arXiv:2603.28732_ , 2026. 

- [5] D. Iliash _et al._ , “Artiverse: A Diverse and Physically Grounded Dataset for Articulated Objects,” in _CVPR_ , 2026. 

- [6] H. Li _et al._ , “PhysGraph: A Physics-aware 3D Scene Graph for Perception and Reasoning,” _arXiv:2606.08655_ , 2026. 

- [7] D. Katz and O. Brock, “Manipulating Articulated Objects with Interactive Perception,” in _ICRA_ , 2008. 

- [8] R. Martín-Martín and O. Brock, “Coupled Recursive Estimation for Online Interactive Perception of Articulated Objects,” _IJRR_ , 2022. 

- [9] R. Buchanan _et al._ , “Online Estimation and Manipulation of Articulated Objects,” _Auton. Robots_ , 2026. 

- [10] T. Engelbracht _et al._ , “Hoi! - A Multimodal Dataset for ForceGrounded, Cross-View Articulated Manipulation,” in _CVPR_ , 2026. 

- [11] H. Choi _et al._ , “In-the-Wild Compliant Manipulation with UMI-FT,” _arXiv:2601.09988_ , 2026. 

- [12] J. Bohg _et al._ , “Interactive Perception: Leveraging Action in Perception and Perception in Action,” _IEEE T-RO_ , 2017. 

- [13] J. Sturm _et al._ , “A Probabilistic Framework for Learning Kinematic Models of Articulated Objects,” _JAIR_ , 2011. 

- [14] X. Sun _et al._ , “OPDMulti: Openable Part Detection for Multiple Objects,” _arXiv:2303.14087_ , 2023. 

- [15] J. Liu _et al._ , “PARIS: Part-level Reconstruction and Motion Analysis for Articulated Objects,” _arXiv:2308.07391_ , 2023. 

- [16] A. Jain _et al._ , “ScrewNet: Category-Independent Articulation Model Estimation From Depth Images Using Screw Theory,” _arXiv:2008.10518_ , 2021. 

- [17] A. Werby _et al._ , “Articulated Object Estimation in the Wild,” _arXiv:2509.01708_ , 2025. 

- [18] Z. Fu _et al._ , “FunFact: Building Probabilistic Functional 3D Scene Graphs via Factor-Graph Reasoning,” _arXiv:2604.03696_ , 2026. 

- [19] R. Buchanan _et al._ , “Online Estimation of Articulated Objects with Factor Graphs using Vision and Proprioceptive Sensing,” _arXiv:2309.16343_ , 2023. 

- [20] F. Endres _et al._ , “Learning the Dynamics of Doors for Robotic Manipulation,” in _IROS_ , 2013. 

- [21] A. Jain _et al._ , “Improving Robot Manipulation with Data-Driven Object-Centric Models of Everyday Forces,” _Auton. Robots_ , 2013. 

- [22] Z. Jiang _et al._ , “Ditto: Building Digital Twins of Articulated Objects from Interaction,” in _CVPR_ , 2022. 

- [23] C. Chi _et al._ , “Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots,” _arXiv:2402.10329_ , 2024. 

- [24] Q. Chen _et al._ , “URDFormer: A Pipeline for Constructing Articulated Simulation Environments from Real-World Images,” in _RSS_ , 2024. 

- [25] L. Ma _et al._ , “Sim2Real<sup>2</sup> : Actively Building Explicit Physics Model for Precise Articulated Object Manipulation,” in _ICRA_ , 2023. 

- [26] M. Villasevil _et al._ , “Reconciling Reality through Simulation: A Realto-Sim-to-Real Approach for Robust Manipulation,” in _RSS_ , 2024. 

- [27] T. Dai _et al._ , “Automated Creation of Digital Cousins for Robust Policy Learning,” _arXiv:2410.07408_ , 2024. 

- [28] H. Jiang _et al._ , “PhysTwin: Physics-Informed Reconstruction and Simulation of Deformable Objects from Videos,” in _ICCV_ , 2025. 

- [29] Y. Chebotar _et al._ , “Closing the Sim-to-Real Loop: Adapting Simulation Randomization with Real World Experience,” in _ICRA_ , 2019. 

- [30] K. M. Lynch and F. C. Park, _Modern Robotics: Mechanics, Planning, and Control_ . Cambridge University Press, 2017. 

- [31] G. Schwarz, “Estimating the Dimension of a Model,” _The Annals of Statistics_ , 1978. 

- [32] J. Engel _et al._ , “Project Aria: A New Tool for Egocentric Multi-Modal AI Research,” _arXiv:2308.13561_ , 2023. 

- [33] A. Delitzas _et al._ , “FunRec: Reconstructing Functional 3D Scenes from Egocentric Interaction Videos,” in _CVPR_ , 2026. 

- [34] M. Mittal _et al._ , “Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning,” _arXiv:2511.04831_ , 2025. 

- [35] J.-P. Sleiman _et al._ , “Guided Reinforcement Learning for Robust Multi-Contact Loco-Manipulation,” _arXiv:2410.13817_ , 2024. 

