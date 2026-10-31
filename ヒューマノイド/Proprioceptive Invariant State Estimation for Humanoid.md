---
title: "Proprioceptive Invariant State Estimation for Humanoid Robots on Non-Inertial Ground"
date: "2026-06-17"
authors: "Falak Mandali; Zijian He; Yan Gu"
url: https://arxiv.org/abs/2606.19512
pdf: https://arxiv.org/pdf/2606.19512
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.19512)** / [論文ページ](https://arxiv.org/abs/2606.19512)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Proprioceptive Invariant State Estimation for Humanoid Robots on Non-Inertial Ground 

Falak Mandali<sup>1</sup><sup>_,∗_</sup> , Zijian He<sup>1</sup><sup>_,∗_</sup> , Yan Gu<sup>1</sup><sup>_,†_</sup> 

**_Abstract_ —This paper presents an invariant extended Kalman filtering (InEKF) approach for real-time state estimation of humanoid robots operating on non-inertial ground using only onboard proprioceptive sensing. The proposed approach estimates the robot’s base position and velocity relative to the moving ground frame without requiring direct measurements of ground motion or externally mounted sensors. By exploiting kinematic constraints at the stance foot through foot-mounted IMUs, the filter accounts for ground-induced nonlinearities in the process and measurement models while remaining fully proprioceptive. The estimator is formulated to admit a right-invariant measurement model, enabling favorable error dynamics under large initial uncertainties. Observability analysis establishes conditions under which the robot’s relative base position and velocity are observable with respect to the non-inertial ground frame. Experiments with the Digit humanoid robot standing and squatting atop a swaying and pitching ground showcase a 96% speedup in convergence rate and an 80% reduction in position estimate errors over existing InEKFs. Walking experiments on a uniaxially rotating ground achieve an average estimation error of less than 9 cm for an initial error of up to 1 m.** 

**_Index Terms_ —State estimation, legged robots, dynamic environments, loco-manipulation** 

## I. INTRODUCTION 

Accurate, real-time state estimation is a prerequisite for model-based planning and control of legged robots. Most existing estimators fuse proprioceptive and exteroceptive sensing using extended Kalman filters (EKFs) [1] or optimizationbased frameworks [2], [3], and rely on the assumption that the ground is static, implying zero stance-foot velocity in the inertial frame [1], [4]. Under this assumption, invariant EKFs (InEKFs) [5], which ensure trajectory-independent linearization under group-affine dynamics and invariant observation conditions, have significantly improved estimation accuracy and convergence rate beyond standard EKF methods [6]–[10]. In parallel, recent proprioceptive estimation methods have explored the use of multiple onboard inertial measurement units (IMUs) to mitigate drift or improve vertical-position estimation [11]–[13], all of which fundamentally rely on the static-ground assumption. 

However, the static-ground assumption limits applicability in non-inertial environments, where the supporting surface undergoes translational and rotational motion relative to the inertial frame, such as on moving trains, ships, or aircraft [14]–[17]. In these settings, ground-induced accelerations and rotations fundamentally alter both the system dynamics and the 

> 1Purdue University, West Lafayette, IN 47907, USA. E-mails: {fmandali,he348,yangu}@purdue.edu. 

> _∗_ Equal contributions. _†_ Corresponding author. This research has been supported in part by NSF CMMI-2423239 and ONR N00014-24-1-2028. 


Fig. 1: (a) Humanoid robot walking on non-inertial ground with onboard proprioceptive sensors (torso and foot IMUs and joint encoders); no ground-mounted sensors are required. (b) Reference frames and state variables used for state estimation. 

structure of the estimation problem, where ignoring ground motion introduces significant modeling errors that degrade estimation accuracy, particularly under large ground motion. 

To address state estimation on non-inertial ground, the InEKF introduced in [8] explicitly models ground motion to estimate a robot’s absolute state in the inertial world frame, but assumes direct and accurate knowledge of the moving ground’s absolute pose and velocity, which is an assumption rarely satisfied in practice. More recently, [9], [18] formulate state estimation in a non-inertial frame rigidly attached to the moving ground, enabling full observability of the robot’s relative pose and velocity under general ground motions. Yet, this approach relies on an external IMU physically mounted on the ground to measure its motion, which may be impractical in real-world deployments due to instrumentation constraints, communication delays, and potential signal loss, particularly in unstructured environments. Recent learning-based [19], [20] and hybrid model-learning [10], [21] estimators have shown promising results under contact uncertainty, slip, and complex terrain. Yet, they rely on substantial training data and estimate states in the inertial frame, so their generalization to noninertial environments remains unclear. 

To enable accurate, real-time state estimation of humanoid robots in non-inertial environments without explicit ground motion sensing, we propose an InEKF that estimates the robot’s motion state relative to a moving ground frame using only onboard proprioceptive sensors. These state estimates are directly relevant for planning and control tasks defined with 

2 

respect to the moving environment. The key contributions of this study are summarized as follows: 

- (a) An InEKF formulation for estimating a humanoid robot’s base pose and velocity relative to a non-inertial ground frame using only joint encoders and torso- and footmounted IMUs. By exploiting kinematic foot-ground contact constraints through foot-IMU measurements, the proposed InEKF enables fully proprioceptive estimation. 

- (b) Process and measurement models that explicitly account for nonlinear effects induced by ground motion, with the measurement model satisfying the right-invariant observation condition. These properties promote robust and accurate estimation under large initial errors. 

- (c) An observability analysis revealing that the base position and velocity relative to the moving ground are observable under general ground motions. The analysis further shows that simple augmentation of the sensing configuration enables recovery of base orientation observability. 

- (d) Hardware experiments on the Digit humanoid robot under various ground motions, demonstrating improved estimation accuracy and faster convergence of the proposed InEKF compared to baseline estimators, and validating the theoretical observability results. 

II. PRELIMINARIES 

We consider a matrix Lie group _G ⊂_ GL( _n,_ R), where GL( _n,_ R) denotes the set of invertible _n × n_ real matrices. Its associated Lie algebra, denoted by g with dimension dim(g), acts as the tangent space of _G_ at the identity element **I** _∈G_ . We define the wedge operator ( _·_ )<sup>_∧_</sup> : R<sup>dim(g)</sup> _→_ g as the isomorphism that maps a vector **_ξ_** _∈_ R<sup>dim(g)</sup> to the corresponding element in the Lie algebra. The exponential map exp : R<sup>dim(g)</sup> _→G_ is defined as exp ( **_ξ_** ) = exp _m_ ( **_ξ_**<sup>_∧_</sup> ), where exp _m_ ( _·_ ) is the matrix exponential. The Adjoint map **AdX** : g _→_ g at **X** _∈G_ is defined as ( **AdX** **_ξ_** )<sup>_∧_</sup> = **X** **_ξ_**<sup>_∧_</sup> **X**<sup>_−_1</sup> . 

Throughout this paper, we denote **I** _n_ and **0** _m,n_ as the _n × n_ identity matrix and the _m × n_ zero matrix, respectively. The skew-symmetric matrix associated with a vector ( _·_ ) _∈_ R<sup>3</sup> is denoted by [ _·_ ] _×_ . We distinguish between the true values of a variable ( _·_ ), its measured value (<sup>˜</sup> _·_ ), and its estimated value (<sup>¯</sup> _·_ ). ( _·_ ) _t_ denotes the value of a variable ( _·_ ) at time _t_ . 

We define four primary reference frames: the robot’s base (e.g., torso) link _{B}_ , the stance foot _{F }_ , the dynamic ground _{D}_ , and the inertial world _{W }_ , as illustrated in Fig. 1(a). 

We adopt the convention that the left superscript denotes the frame in which a quantity is expressed, while the right superscript specifies the frame relationship. A single-letter right superscript indicates the frame whose configuration is being expressed (e.g.,<sup>_D_</sup> **R**<sup>_B_</sup> is the orientation of _B_ relative to _D_ ), whereas in a two-letter right superscript, the first denotes the reference origin and the second denotes the target frame (e.g.,<sup>_W_</sup> **p**<sup>_DB_</sup> is the position of the origin of _B_ relative to _D_ , expressed in the world frame _W_ ). The reference frames and variables are illustrated in Fig. 1(b). Table I in the supplementary material summarizes the main notations. 

III. PROBLEM FORMULATION 

## _A. State Representation_ 

For reliable navigation in non-inertial environments, planners and controllers require the robot’s motion state relative to 

the moving environment rather than an inertial world frame, since task objectives such as obstacle avoidance and goal reaching are naturally defined relative to the moving support. Accordingly, the proposed filter estimates the robot’s velocity and pose with respect to the dynamic ground frame _{D}_ . 

Following the reference frame conventions in Sec. II, the robot base pose and velocity in the inertial frame _{W }_ are denoted by<sup>_W_</sup> **R**<sup>_B_</sup> _t_<sup>,</sup><sup>_W_</sup><sup>**p**</sup> _t_<sup>_W B_</sup> , and<sup>_W_</sup> **v** _t_<sup>_W B_</sup> , with the stance-foot position given by<sup>_W_</sup> **p**<sup>_W F_</sup> _t_ . The ground motion relative to _{W }_ is parameterized by<sup>_W_</sup> **R**<sup>_D_</sup> _t_<sup>,</sup><sup>_W_</sup><sup>**v**</sup> _t_<sup>_W D_</sup> , and<sup>_W_</sup> **p**<sup>_W D_</sup> _t_ . The robot’s motion relative to the moving ground is described by<sup>_D_</sup> **R**<sup>_B_</sup> _t_<sup>and</sup> _D_ **p** _DBt_ , together with the stance-foot pose<sup>_D_</sup> **R**<sup>_F_</sup> _t_<sup>and</sup><sup>_D_</sup><sup>**p**</sup><sup>_DF_</sup> _t_ , as illustrated in Fig. 1(b). 

_1) State variables:_ To estimate the robot’s motion relative to the dynamic ground frame _{D}_ , we define the relative base orientation, position, and velocity as: 


where<sup>_W_</sup> **v** _t_<sup>_W B_</sup> = _dtd_<sup>(</sup><sup>_W_</sup><sup>**p**</sup> _t_<sup>_W B_</sup> ) and<sup>_W_</sup> **v** _t_<sup>_W D_</sup> = _dtd_<sup>(</sup><sup>_W_</sup><sup>**p**</sup> _t_<sup>_W D_</sup> ) are time derivatives taken in the inertial world frame _{W }_ . Note that **v** _t_ is not equal to _dtd_<sup>**p**</sup><sup>_t_when</sup><sup>_{D}_isrotatingrelativeto</sup> _{W }_ , as the latter additionally includes terms induced by the angular motion of _{D}_ . 

To exploit stance-contact kinematic constraints and eliminate direct ground-motion sensing, we further introduce the stance-foot orientation and position relative to _{D}_ as: 


_2) State representation on a Lie group:_ The state variables in (1) and (2) are embedded in a matrix Lie group _G_ as: 


where _G_ is composed of a double spatial isometry _SE_ 3(3) and the special orthogonal group _SO_ (3). 

_3) Right-invariant and logarithmic errors:_ By the general InEKF methodology [5], both the propagation and update steps are formulated in terms of the right-invariant error **_η_** _t ∈G_ and its associated logarithmic error **_ξ_** _t ∈_ R<sup>dimg</sup> . The right-invariant error, defined as **_η_** _t_ := **X**<sup>¯</sup> _t_ **X**<sup>_−_</sup> _t_<sup>1,captures</sup> the discrepancy between the true state **X** _t_ and its estimate = **X** ¯ _t_ . The logarithmic error satisfies **_η_** _t_ exp( **_ξ_** _t_ ), with �( **_ξ_**<sup>_R_</sup> _t_<sup>_F_</sup> )<sup>T</sup> _,_ ( **_ξ_**<sup>_v_</sup> _t_<sup>)T</sup><sup>_,_(</sup><sup>**_ξ_**</sup> _t_<sup>_p_)T</sup><sup>_,_(</sup><sup>**_ξ_**</sup><sup>_d_</sup> _t_<sup>)T</sup><sup>_,_(</sup><sup>**_ξ_**</sup><sup>_R_</sup> _t_<sup>_B_</sup> )<sup>T</sup> �T := **_ξ_** _t_ . 

## _B. Sensors Considered_ 

To ensure practical deployability, the proposed filter relies exclusively on onboard proprioceptive sensing and does not require external instrumentation (e.g., ground-mounted IMUs) or exteroceptive sensors such as GPS, LiDAR, or cameras. Specifically, the filter utilizes onboard IMUs and joint encoders commonly available on legged robots. 

3 

_1) Proprioceptive sensor selection:_ Encoders measure all joint angles, and each IMU provides linear acceleration and angular velocity measurements expressed in the IMU frame. We consider three IMUs mounted on the robot: one on the base (torso) and one on each footpad, as illustrated in Fig. 1(a). 

_2) Reference frame assignment:_ For simplicity and without loss of generality, we assume that (i) during double-support or standing phases, the stance-foot IMU data from either foot may be used, and (ii) the robot base frame _{B}_ and stancefoot frame _{F }_ coincide with the frames of the base IMU and stance-foot IMU, respectively. 

_3) Sensor data expression:_ Sensor measurements are modeled as true values corrupted by additive white Gaussian noise. Although real sensors may exhibit colored noise and slowly varying bias drift, these effects are not explicitly modeled here and are instead mitigated through offline calibration and covariance tuning. Accordingly, the joint angle measurements satisfy **q** ˜ _t_ = **q** _t_ + **w** _t_<sup>_q_,where</sup><sup>**w**</sup> _t_<sup>_q_denotesencodernoise.</sup> Let<sup>_i_</sup> **_ω_** ˜<sup>_W i_</sup> _t_ and<sup>_i_</sup> **a** ˜<sup>_W i_</sup> _t_ denote the measured angular velocity and linear acceleration of frame _{i}_ with respect to the initial world _{W }_ , expressed in frame _{i}_ , where _i ∈{B, F }_ . For brevity, we define<sup>_i_</sup> **_ω_** ˜ _t_ :=<sup>_i_</sup> **_ω_** ˜<sup>_W i_</sup> _t_ and<sup>_i_</sup> **a** ˜ _t_ :=<sup>_i_</sup> **a** ˜<sup>_W i_</sup> _t_ , and model the measurements as<sup>_i_</sup> **_ω_** ˜ _t_ =<sup>_i_</sup> **_ω_**<sup>_W i_</sup> _t_ +<sup>_i_</sup> **w** _t_<sup>_ω_and</sup><sup>_i_</sup><sup>**a**˜</sup><sup>_t_=</sup> _i_ **a** _W it_ +<sup>_i_</sup> **w** _t_<sup>_a,_where</sup><sup>_i_</sup><sup>**_ω_**</sup><sup>_W i_</sup> _t_ and<sup>_i_</sup> **a**<sup>_W i_</sup> _t_ are the true angular velocity and linear acceleration, and<sup>_i_</sup> **w** _t_<sup>_ω_and</sup><sup>_i_</sup><sup>**w**</sup> _t_<sup>_a_arewhite</sup> Gaussian noise. 

## IV. SYSTEM MODELING 

This section derives the process and measurement models of the proposed filter. The process model governs the time evolution of the system state and forms the prediction step of the InEKF (Sec. V-A), while the measurement model maps available proprioceptive sensor readings to the state for correction during the update step (Sec. V-B). 

As legged locomotion involves intermittent ground contact, the models account for both continuous swing phases and discrete contact events. Also, the translational and rotational motion of the non-inertial ground introduces nonlinearities, which are explicitly captured in the proposed modeling. 

## _A. Process Model during a Continuous Phase_ 

During continuous phases, the process model is constructed from IMU motion dynamics and stance-foot contact kinematics, which is simple yet accurate. 

_1) Relative IMU motion dynamics:_ We derive the relative IMU motion dynamics by expressing the robot’s motion in the dynamic ground frame _{D}_ . Building on prior extensions of IMU dynamics from inertial frames to non-inertial frames [9], the continuous-time evolution of the relative base orientation **R**<sup>_B_</sup> _t_<sup>,velocity</sup><sup>**v**</sup><sup>_t_,andposition</sup><sup>**p**</sup><sup>_t_isgivenby:</sup> 


Equation (4) depends on the dynamic ground acceleration _D_ **a** _t_ and angular velocity _D_ **_ω_** _t_ , which are assumed to be directly measured by a ground-mounted IMU in prior works [9]. Since such measurements are generally unavailable without 

external instrumentation, we eliminate this dependency by exploiting stance-foot kinematic constraints. 

As described in Sec. III-B, the robot feet are equipped with IMUs measuring<sup>_F_</sup> **a** ˜ _t_ and<sup>_F_</sup> **_ω_** ˜ _t_ . Our objective is to express the ground-frame inertial quantities using only onboard proprioceptive sensing. 


whose detailed derivations are in the supplementary file. 


where the vector **J** _hR_ ( ˜ **q** _t,_ **w** _t_<sup>_q_)isdefinedas</sup><sup>**J**</sup><sup>_h_</sup> _R_<sup>( ˜</sup><sup>**q**</sup><sup>_t,_</sup><sup>**w**</sup> _t_<sup>_q_):=</sup> � _∂∂_ **hq** _Rt,_ 1<sup>(˜</sup><sup>**q**</sup><sup>_t_)</sup><sup>**w**</sup> _t_<sup>_q,_</sup> _∂∂_ **hq** _Rt,_ 2<sup>(˜</sup><sup>**q**</sup><sup>_t_)</sup><sup>**w**</sup> _t_<sup>_q,_</sup> _∂∂_ **hq** _Rt,_ 3<sup>(˜</sup><sup>**q**</sup><sup>_t_)</sup><sup>**w**</sup> _t_<sup>_q_</sup> �, which is obtained using the Jacobian of each column of **h** _R_ =: � **h** _R,_ 1 _,_ **h** _R,_ 2 _,_ **h** _R,_ 3�. The physical interpretation of Eq. (7) is provided in the supplementary material. _2) Stance-foot contact dynamics:_ To model slippage, the foot velocity in _{D}_ is treated as white Gaussian noise. Then, the foot position **d** _t_ and orientation **R** _t_<sup>_F_evolveas:</sup> 


where **u** _t_ := [(<sup>_B_</sup> **a** ˜ _t_ )<sup>T</sup> _,_ (<sup>_F_</sup> **a** ˜ _t_ )<sup>T</sup> _,_ (<sup>_B_</sup> **_ω_** ˜ _t_ )<sup>T</sup> _,_ (<sup>_F_</sup> **_ω_** ˜ _t_ )<sup>T</sup> ]<sup>T</sup> collects the IMU measurements and **w** _t_ aggregates sensor noise and contact uncertainties as **w** _t_ := [(<sup>_B_</sup> **w** _t_<sup>_a_)T</sup><sup>_,_(</sup><sup>_F_</sup><sup>**w**</sup> _t_<sup>_a_)T</sup><sup>_,_(</sup><sup>_B_</sup><sup>**w**</sup> _t_<sup>_ω_)T</sup><sup>_,_</sup> (<sup>_F_</sup> **w** _t_<sup>_ω_)T</sup><sup>_,_(</sup><sup>**w**</sup> _t_<sup>_q_)T</sup><sup>_,_(</sup><sup>_F_</sup><sup>**w**</sup> _t_<sup>_v_)T</sup><sup>_,_(</sup><sup>_F_</sup><sup>**w**</sup> _t_<sup>_ωc_)T]T.Theexpressionsof</sup><sup>_f_</sup> _ut_ and **W** _t_ are given in the supplementary file. _B. Measurement Model_ 

During continuous phases, we employ leg odometry as the measurement model. Based on the relative position between the base and stance-foot frames, the leg-odometry measurement is given by: **h** _p_ ( **q** ) = ( **R**<sup>_B_</sup> _t_<sup>)T(</sup><sup>**d**</sup> _t_<sup>_−_</sup><sup>**p**</sup> _t_<sup>).Toexpressthis</sup> measurement in the stance-foot frame used in the process model, we left-multiply by **h**<sup>T</sup> _R_<sup>,yielding:</sup> 


Due to encoder noise, the true measurement is approximated via first-order Taylor expansion as: **h**<sup>T</sup> _R_<sup>(</sup><sup>**q**</sup><sup>_t_)</sup><sup>**h**</sup><sup>_p_(</sup><sup>**q**</sup><sup>_t_)</sup><sup>_≈_</sup> 

4 

**h**<sup>T</sup> _R_<sup>(˜</sup><sup>**q**</sup><sup>_t_)</sup><sup>**h**</sup><sup>_p_(˜</sup><sup>**q**</sup><sup>_t_)</sup><sup>_−_</sup><sup>**h**</sup> _R_<sup>T</sup> � **J** _hp_ (˜ **q** _t_ ) + [ **h** _p_ (˜ **q** _t_ )] _×_ **J** _θ_ (˜ **q** _t_ )� **w** _t_<sup>_q_,</sup> where **J** _hp_ (˜ **q** _t_ ) =<sup>_∂_</sup> _∂_<sup>**h**</sup> **q**<sup>_<u>p</u>_(˜</sup><sup>**q**</sup><sup>_t_)isthelinearJacobianand</sup><sup>**J**</sup><sup>_θ_(˜</sup><sup>**q**</sup><sup>_t_)</sup><sup>_∈_R3</sup><sup>_×n_</sup> is the angular component of the geometric Jacobian [22] mapping the joint velocities to the relative angular velocity of the foot. Derivations are included in the supplementary file. 

Following invariant filtering theory, the measurement in (10) admits the right-invariant observation form [5]: 

**Y** _t_ = **X**<sup>_−_</sup> _t_<sup>1</sup><sup>**b**+</sup><sup>**n**</sup><sup>_t,_</sup> (11) where **Y** _t_ = �( **h**<sup>T</sup> _R_<sup>(˜</sup><sup>**q**</sup><sup>_t_)</sup><sup>**h**</sup><sup>_p_(˜</sup><sup>**q**</sup><sup>_t_))T</sup><sup>_,_</sup> 0 _,_ 1 _, −_ 1 _,_ **0** 1 _,_ 3�T, **n** _t_ = �( **h**<sup>T</sup> _R_<sup>(˜</sup><sup>**q**</sup><sup>_t_)</sup> � **J** _hp_ ( ˜ **q** _t_ ) + [ **h** _p_ (˜ **q** _t_ )] _×_ **J** _θ_ ( ˜ **q** _t_ )� **w** _t_<sup>_q_)T</sup><sup>_,_</sup> **0** 1 _,_ 6�T, and **b** = � **0** 1 _,_ 3 _,_ 0 _,_ 1 _, −_ 1 _,_ **0** 1 _,_ 3�T. The derivations of **Y** _t_ , **b** , and **n** _t_ are given in the supplementary file. 

This invariant structure yields a log-error dynamics that is exactly linear and trajectory-independent in the deterministic case, enabling consistent covariance propagation, fast convergence, and high accuracy even under large initial errors [5]. 

_C. Process Model at a Discrete Contact-Switch Event_ 

While (8) governs the stance-foot evolution during continuous phases, the stance-foot pose undergoes a discrete jump at foot-landing events. At a contact switch occurring at _t_ = _t_<sup>_−_</sup> _K_ ( _K ∈_ N+), the change in the stance-foot orientation and position are computed using the forward-kinematics chain between the outgoing and incoming stance feet: 


where ( _·_ ) _K−_ and ( _·_ ) _K_ + denote the values of ( _·_ ) _t_ immediately before and after the switch, respectively. Here, **h** _RF_ ( **q** _t_ ) = _B_ **R** _Ft_ and **h** _pF_ ( **q** ) = _B_ **p** _tBF_ are the forwardkinematics mappings of foot orientation and position relative to the base, and the subscripts “old” and “new” indicate the previous and incoming stance feet. **n** _RF_ and **n** _d_ capture additive uncertainty due to encoder noise, expressed as: **n** _RF_ := _−_ **h**<sup>T</sup> _RF,_ old<sup>(˜</sup><sup>**q**</sup> _K_<sup>_−_)</sup><sup>**J**</sup><sup>_h_</sup> _RF,_ new<sup>(˜</sup><sup>**q**</sup> _K_<sup>+</sup><sup>_,_</sup><sup>**w**</sup> _K_<sup>_q_+)</sup><sup>_−_</sup> **J**<sup>T</sup> _hRF,_ old<sup>(˜</sup><sup>**q**</sup> _K_<sup>_−,_</sup><sup>**w**</sup> _K_<sup>_q−_)</sup><sup>**h**</sup><sup>_RF,_new(˜</sup><sup>**q**</sup><sup>_K_+)and</sup><sup>**n**</sup><sup>_d_</sup> := _−_ **h**<sup>T</sup> _RF,_ old<sup>(˜</sup><sup>**q**</sup> _K_<sup>_−_)</sup> **J** _hpF,_ new (˜ **q** _K_ + ) **w** _K_<sup>_q_+</sup><sup>_−_</sup><sup>**J**T</sup> _hRF,_ old<sup>(˜</sup><sup>**q**</sup> _K_<sup>_−,_</sup><sup>**w**</sup> _K_<sup>_q−_)</sup><sup>**h**</sup><sup>_pF,_new(˜</sup><sup>**q**</sup><sup>_K_+).</sup> Since the robot’s base pose and velocity relative to the dynamic ground do not change across foot-switch events, **R** _t_<sup>_B_,</sup> **p** _t_ , and **v** _t_ remain continuous from _t_ = _t_<sup>_−_</sup> _K_<sup>to</sup><sup>_t_=</sup><sup>_t_+</sup> _K_<sup>.</sup> 

## V. FILTER DESIGN 

This section presents the design of the proposed InEKF based on the process and measurement models developed in Sec. IV, including the propagation and update steps. 

_A. Propagation Step during a Continuous Phase_ 

During propagation, the InEKF predicts the estimate **X**<sup>¯</sup> _t_ and the error covariance **P** _t_ using the process model. The corresponding measurement update, which incorporates sensor data to correct these predictions, is described later. 

_1) State estimate propagation:_ The state estimate **X**<sup>¯</sup> _t_ is propagated using the deterministic component of the process models described in Sec. IV. 

_2) Covariance estimate propagation:_ By the general InEKF methodology, the estimation-error covariance **P** _t_ is propagated using the linearized log-error dynamics derived from the process model. Taking the time derivative of the right-invariant 

error in (3) and applying the first-order approximations **_η_** _t ≈_ **I** + **_ξ_**<sup>_∧_</sup> _t_<sup>and</sup> _dtd_<sup>**_η_**</sup><sup>_t≈_</sup> _dtd_<sup>(</sup><sup>**_ξ_**</sup> _t_<sup>_∧_)yields:</sup> _dtd_<sup>**_ξ_**</sup><sup>_t_=</sup><sup>**A**</sup><sup>_t_</sup><sup>**_ξ_**</sup><sup>_t_+</sup><sup>**w**</sup><sup>_At,_</sup> (13) 

where **A** _t_ is the Jacobian of the error dynamics and **w** _At_ is the process noise. Their expressions are provided in the supplementary file. Since (13) is linear, the covariance evolves according to the associated Riccati equation [23]: 


where **Q**<sup>¯</sup> _t_ = **Q** _At_ Cov( **w** _At_ ) **Q**<sup>T</sup> _At_<sup>is constructed from the covari-</sup> ance of the IMU white noise Cov(<sup>_i_</sup> **w** _t_ ) for _{i ∈ B, F }_ . 

_B. Measurement Update Step during a Continuous Phase_ 

During the measurement update, the predicted state and covariance are corrected using the leg-odometry measurement model in (10) with newly available sensor data. 

_1) State estimate update:_ Since the measurement model admits a right-invariant observation form, the updated state estimate **X**<sup>¯+</sup> _t_<sup>isgivenby[5]:</sup> 


where **K** _t_ denotes the Kalman gain. 

_2) Covariance estimate update:_ To update the covariance, we use the right-invariant InEKF property **H** _t_ **_ξ_** _t_ = _−_ **_ξ_**<sup>_∧_</sup> _t_<sup>**b**</sup><sup>_t_[5],</sup> and apply a first-order approximation of the right-invariant error, **_η_** _t ≈_ **I** + **_ξ_**<sup>_∧_</sup> _t_<sup>.Thisyieldsthelinearizedupdateequation</sup> for the logarithmic error: 


Derivation of (16) and (17) is given in the supplementary file. 

Since (16) is linear, the Kalman gain follows from standard Kalman filtering as: **K** _t_ = **P** _t_ **H** _t_<sup>T</sup><sup>**S**</sup><sup>_−_</sup> _t_<sup>1,where</sup><sup>**S**</sup><sup>_t_=</sup><sup>**H**</sup><sup>_t_</sup><sup>**P**</sup><sup>_t_</sup><sup>**H**</sup> _t_<sup>T+</sup> **N** ¯ _t_ . Here the measurement noise covariance **¯N** _t_ is given by: **N**<sup>**¯**</sup> _t_ = **N**<sup>¯</sup> _R_ Cov( **w** _t_<sup>_q_) ¯</sup><sup>**N**</sup> _R_<sup>T,with</sup><sup>**N**¯</sup><sup>_R_:=</sup><sup>**R**¯</sup> _t_<sup>_F_</sup><sup>**h**T</sup> _R_<sup>( ˜</sup><sup>**q**</sup><sup>_t_)(</sup><sup>**J**</sup><sup>_p_(˜</sup><sup>**q**</sup><sup>_t_)+</sup> [ **h** _p_ ( ˜ **q** _t_ )] _×_ **J** _θ_ ( ˜ **q** _t_ )), with derivations in the supplementary file. Finally, the updated covariance estimate is: 


_C. Propagation Step at a Discrete Contact Switch_ 

_1) State estimate propagation:_ At a discrete foot-landing event occurring at _t_ = _t_<sup>_−_</sup> _K_<sup>(</sup><sup>_K∈_N+),thestateundergoes</sup> a jump due to the change of stance foot. This discrete propagation can be approximated as: 


where **r** 1 := **h**<sup>T</sup> _RF,_ old<sup>(˜</sup><sup>**q**</sup> _K_<sup>_−_)</sup><sup>**h**</sup><sup>_R_</sup> _F,_ new<sup>(˜</sup><sup>**q**</sup> _K_<sup>+)and</sup><sup>**r**2:=</sup><sup>**h**T</sup> _RF,_ old<sup>(˜</sup><sup>**q**</sup> _K_<sup>_−_)</sup> **h** _pF,_ new (˜ **q** _K_ + ). Thus, the state can be propagated deterministically through ∆ _ut_ ( **X** _K− ,_ ˜ **q** _K−_ ). _2) Covariance estimate propagation:_ At a contact switch, the covariance is propagated through a linear transformation that removes the previous stance-foot state and introduces the new contact point. Accounting for foot impact and slippage, the covariance update follows [6]: **P** _t_ = **F** _t_ **P** _t_ **F** _t_<sup>T+</sup><sup>**¯Q**</sup> _t_<sup>_c_,with</sup> derivations of **F** _t_ and **Q**<sup>**¯**</sup><sup>_c_</sup> _t_<sup>giveninthesupplementaryfile.</sup> 

5 

TABLE I: Observability analysis. 

|**Obs.**<br>**type**|**Foot-IMU reading**<br>|**Observable**<br>**pos. and vel.**|
|---|---|---|
|**O1**|_F_ ˜_ωx_ = _F_ ˜_ωy_ = _F_ ˜_ωz_ = 0 _∀t_<br>|**v**_t_|
|**O2.1**|_F_ ˜_ωx̸ ≡_0_, F_ ˜_ωy_ = 0, _F_ ˜_ωz_ = 0 _∀t_|**v**_t_, _py_, _pz_|
|**O2.2**|_F_ ˜_ωx_ = 0, _F_ ˜_ωy̸ ≡_0, _F_ ˜_ωz_ = 0 _∀t_<br>|**v**_t_, _px_, _pz_|
|**O2.3**|_F_ ˜_ωx_ = 0_, F_ ˜_ωy_ = 0, _F_ ˜_ωz̸ ≡_0 _∀t_<br>|**v**_t_, _px_, _py_|
|**O3.1**|_F_ ˜_ωx̸ ≡_0, _F_ ˜_ωy̸ ≡_0, _F_ ˜_ωz_ = 0 _∀t_<br>||
|**O3.2**|_F_ ˜_ωx̸ ≡_0, _F_ ˜_ωy_ = 0, _F_ ˜_ωz̸ ≡_0 _∀t_<br>|**v**|
|**O3.3**|_F_ ˜_ωx_ = 0_, F_ ˜_ωy̸ ≡_0, _F_ ˜_ωz̸ ≡_0 _∀t_<br>|_t_, **p**_t_|
|**O3.4**|_F_ ˜_ωx̸ ≡_0_, F_ ˜_ωy̸ ≡_0, _F_ ˜_ωz̸ ≡_0 _∀t_||


VI. OBSERVABILITY ANALYSIS _1) Observability matrix:_ We perform a local observability analysis on the linearized log-error dynamics in (13). Since the filter operates in discrete time with discrete measurements, a discrete-time observability analysis is adopted. 

The local observability between adjacent measurement update steps (i.e., over [ _tk_ , _tk_ +1] with _k ∈_ N+) depends on both the state-transition matrix **Φ** ( _tk, tk_ +1), and the output matrix **H** _t_ in (17). The state-transition matrix satisfies **Φ**<sup>˙</sup> ( _tk, tk_ +1) = **A** _k_ **Φ** ( _tk, tk_ +1) with **Φ** ( _tk, tk_ ) = **I** 15, and admits the closed-form solution **Φ** ( _tk, tk_ +1) = exp _m_ ( **A** _k_ ∆ _t_ ): 


where the expressions of **Φ** _k,_ 22, **Φ** _k,_ 24, **Φ** _k,_ 32, **Φ** _k,_ 33, and **Φ** _k,_ 34 are derived in the supplementary file. 

The discrete-time local observability matrix at **X**<sup>¯</sup> _t_ is [24]: 


where elements of **_O_** are provided in the supplementary file. _2) Observability of base position, velocity, and foot position:_ From the expanded expression of **_O_** in the supplementary file, the observability of the base position **p** _t_ , base velocity **v** _t_ , and stance-foot position **d** _t_ depends solely on the stance-foot gyroscope measurement<sup>_F_</sup> **_ω_** ˜ _t_ =: [<sup>_F_</sup> _ω_ ˜ _x,_<sup>_F_</sup> _ω_ ˜ _y,_<sup>_F_</sup> _ω_ ˜ _z_ ]<sup>T</sup> . Given the fast sampling of IMUs, the gyroscope readings can be assumed constant over [ _tk, tk_ +1], enabling analytical observability characterization (see supplementary material). 

As summarized in Tab. I, the relative base velocity **v** _t_ is always observable, regardless of whether the ground is stationary or moving (observability type **O1** ). If only one principal axis of the stance-foot frame _{F }_ exhibits nontrivial angular-motion readings, the base position **p** _t_ = [ _px, py, pz_ ]<sup>T</sup> is observable except along that axis (types **O2.1** - **O2.3** ). When at least two axes of _{F }_ have nonzero angular-motion readings, the full base position becomes observable (types **O3.1** - **O3.4** ). 

_3) Reconstruction of base orientation via base IMU augmentation:_ The observability matrix **_O_** further indicates that the base orientation **R**<sup>_B_</sup> _t_ and stance-foot orientation **R**<sup>_F_</sup> _t_<sup>are</sup> unobservable under the nominal sensing configuration. Here, the nominal sensing configuration refers to the proposed FRS filter using a single torso IMU together with the IMU on the current stance foot during a given stance phase. Yet, since 


Fig. 2: Experimental setup for performance validation on Digit using torso and foot IMUs, encoders, and motion-capture ground truth on a dynamic treadmill. 


Fig. 3: Snapshots of Digit operating on a moving treadmill under five representative test cases: (a) Case **T1** : standing with a 90° heading relative to the treadmill; (b) Case **T2** : standing with a 45° heading; (c) Case **T3** : box picking and placing; (d) Case **T4** : squatting; and (e) Case **T5** : walking. 

the relative base position **p** _t_ is fully observable under general ground motions (Tab. I), this property can be used to recover base-orientation observability through sensor augmentation. 

Specifically, we consider an augmented sensing configuration with three non-collinear IMUs rigidly mounted on the torso, so the filter can estimate the position of each IMU using the proposed formulation. These three position estimates define a plane fixed to the torso, which uniquely determines the base orientation, thereby enabling full-state observability through torso-IMU augmentation, rather than under the nominal sensing configuration alone. An example of this reconstruction is demonstrated experimentally in Sec. VII. 

VII. EXPERIMENTAL VALIDATION 

This section reports the experimental setup and validation results, including comparison to baseline filters. An experiment movie is provided in the supplementary material and available at: https://youtu.be/3AsKlwrB1ag. 

## _A. Experimental Setup_ 

_1) Robot and sensors:_ Experiments are conducted on the Agility Robotics Digit humanoid robot. The proprietary torsomounted IMU is used as the base-frame IMU while onboard IMU and joint encoder data are sampled at 500 Hz. Two external IMUs (WT901C-232, WitMotion Co., Ltd.) are mounted on the footpads and record data at 200 Hz. All onboard sensors are time-synchronized through a single computation platform. The 200 Hz foot-end IMU measurements are then linearly interpolated to 500 Hz before filter fusion. The sensor specifications are summarized in the supplementary material. A Vicon mo-cap system provides ground-truth state values. 

6 

TABLE II: Summary of the test cases under various robot and ground motions and different observability types. 

|**Test**<br>**case**|**Digit**<br>**motion**|**Digit**<br>**heading**|**Ground**<br>**motion**|**Predicted**<br>**obs. type**|
|---|---|---|---|---|
|**T1**|Standing|90<sup>_◦_</sup>|**GM2**+**GM4**|**O2.1**|
|**T2**|Standing|45<sup>_◦_</sup>|**GM1**+**GM3**|**O3.1**|
|**T3**|Squatting|0<sup>_◦_</sup>|**GM3**|**O2.2**|
|**T4**|Squatting|45<sup>_◦_</sup>|**GM3**|**O3.1**|
|**T5**|Walking|0<sup>_◦_</sup>|**GM5**|**O2.2**|


TABLE III: Maximum steady-state absolute position error for FRS/DRS under varying initial errors. The steady-state periods are as specified in Figs. 4, 5, and 6. 

|**Test case**|_px_[m]|_py_[m]|_pz_[m]|
|---|---|---|---|
|**T1**|0.007<br>/ 0.148|0.006<br>/ 0.199|0.003<br>/ 0.170|
|**T2**|0.011<br>/ 0.138|0.012<br>/ 0.087|0.009<br>/ 0.128|
|**T3**|0.018<br>/ 0.194|0.039 / 0.029|0.013<br>/ 0.149|
|**T4**|0.013<br>/ 0.240|0.011<br>/ 0.112|0.007<br>/ 0.115|
|**T5**|0.113<br>/ 0.136|0.067<br>/ 0.115|0.057 / 0.025|


_2) Dynamic ground:_ Dynamic ground motion is emulated using a Motek M-Gait treadmill (Fig. 2) programmed with the following sway and pitch trajectories: ( **GM1** ) 4 cos � <u>26</u> _<u>π</u>_<sup>_t_</sup> � cm; ( **GM2** ) 4 cos � <u>25</u> _<u>π</u>_<sup>_t_</sup> � cm; ( **GM3** ) 4<sup>_◦_</sup> sin � <u>26</u> _<u>π</u>_<sup>_t_</sup> �; ( **GM4** ) 4<sup>_◦_</sup> sin � <u>28</u> _<u>π</u>_<sup>_t_</sup> �; and ( **GM5** ) 4<sup>_◦_</sup> sin � <u>27</u> _<u>π</u>_<sup>_t_</sup> �. 

_3) Test cases:_ Five experimental cases are designed to assess filter performance under diverse robot and ground motions: two standing trials, two squatting trials (with and without lifting a box), and one walking trial, each conducted under different ground motions. The test cases are illustrated in Fig. 3 and summarized in Tab. II. Guided by the observability analysis, Digit is oriented with different headings, inducing distinct stance-foot angular motions and enabling evaluation under varying observability conditions. 

_4) Baseline estimators:_ The proposed estimator, termed “FRS”, is compared against two InEKF-based baselines [6], [9], both of which propagate the state using IMU motion dynamics and perform measurement updates via leg odometry. 

The first baseline, “SRS” [6], is designed for legged robots operating on static terrain. In the absence of IMU noise and bias, its process model satisfies the group-affine property and its measurement model is right-invariant. However, the staticground assumption restricts its applicability to stationary environments and results in unobservable base yaw and position. 

The second baseline, “DRS” [9], estimates the robot’s pose and velocity relative to a dynamic ground frame by explicitly modeling ground motion. While the filter achieves full state observability, its main limitation is the reliance on an external ground-mounted IMU, which may be impractical in real-world deployments. Results from an additional baseline, DogLegs [11], are provided in the supplementary material. 

For fair comparison under large initial errors, all filters are evaluated on the same experimental data, with initial base velocity and position errors uniformly sampled from [ _−_ 1 _,_ 1] m/s and [ _−_ 1 _,_ 1] m, respectively. Covariance matrices are tuned based on nominal sensor noise characteristics and refined empirically to achieve best performance. The estimation results are shown in Figs. 4, 5, and 6 and summarized in Tab. III, where the baseline performance is consistent with previously reported results [9]. 

_B. Results Analysis and Comparison_ 

_1) Observability of base position and velocity:_ Based on the theoretical observability analysis in Tab. I and the predicted observability for each test case in Tab. II, the relative base velocity is expected to be observable in all experiments. The relative base position is predicted to be partially observable in Cases **T1** ( _px_ unobservable) and **T3** and **T5** ( _py_ unobservable), and fully observable in Cases **T2** and **T4** . 

Experimentally, a state is considered observable if its estimate converges sufficiently close to the ground truth [6]. Under this criterion, the theoretical predictions are largely confirmed by the results in Figs. 4a, 5a, and 6. The only discrepancies occur for _px_ in Case **T1** , and _py_ in Cases **T3** and **T5** . 

Notably, these position components also converge to small neighborhoods around the ground truth, indicating practical observability under experimental conditions. This behavior is likely due to non-ideal experimental conditions (e.g., slight treadmill motion errors and small misalignment between Digit and the treadmill), which induce additional foot IMU excitation and effectively restore full positional observability. Yet, this does not alter the theoretical observability result or provide a formal guarantee. Thus, when full position observability is required, deployment should avoid this degenerate single-axis condition rather than rely on incidental non-idealities. 

In contrast, the base position estimates under the baseline SRS filter fail to converge, consistent with its known observability limitations [6]. The baseline DRS filter exhibits observability behavior similar to FRS, confirming previous observability results [6]. 

_2) Real-time computation:_ Owing to their closed-form formulations, all three filters support real-time implementation, with average computation times of less than 3 ms per cycle on a laptop with a 13th-Gen Intel Core i7-13620H processor and 16 GB RAM. 

_3) Error convergence rate:_ For base velocity estimation, all three filters ensure convergence to a small neighborhood of the ground truth within approximately 1 sec for all test cases, with the proposed FRS filter being consistently the fastest. With respect to base position estimation across all cases, the proposed FRS converges within 0.1 sec whereas the baseline DRS takes 3-5 sec on average. 

The significantly faster convergence of FRS is likely due to its measurement model incorporating both positional and rotational forward kinematics between the base and the foot, whereas DRS and SRS rely only on positional kinematics. 

_4) Steady-state accuracy:_ As shown in Figs. 4 and 5, all three filters achieve comparable steady-state accuracy in base velocity estimation for Cases **T1** - **T4** . In Case **T5** (Fig. 6), the proposed FRS exhibits noticeably larger steady-state velocity errors than in the standing and squatting cases. This degradation is primarily attributed to impact-induced noise in the foot-mounted IMUs during walking, an effect further amplified by the moving ground. 

For base position estimation, the proposed FRS consistently outperforms the SRS baseline and achieves the best overall performance among the three filters in Cases **T1** - **T4** , in terms of both transient response and steady-state accuracy. As discussed earlier, SRS fails to ensure position observability on 

7 


Fig. 4: Estimation results of the <u>proposed FRS and the baseline DRS and SRS filters during Digit</u> balancing on a swaying and pitching ground for test cases **<u>T1</u>** and **T2** under significant initial errors. For FRS and DRS, the base velocity **v** =: [ _vx, vy, vz_ ]<sup>T</sup> and position **p** =: [ _px, py, pz_ ]<sup><u>T</u></sup> relative to the dynamic ground are shown. For SRS, the ab ~~s~~ olute base velocity<sup>_W_</sup> **v**<sup>_W B_</sup> =: [<sup>_W_</sup> _vx_<sup>_W B_</sup> _,_<sup>_W_</sup> _vy_<sup>_W B_</sup> _,_<sup>_W_</sup> _vz_<sup>_W B_</sup> ]<sup>T</sup> and position<sup>_W_</sup> **p**<sup>_W B_</sup> =: [<sup>_W_</sup> _p_<sup>_W B_</sup> _x ,_<sup>_W_</sup> _p_<sup>_W B_</sup> _y ,_<sup>_W_</sup> _p_<sup>_W B_</sup> _z_ ]<sup>T</sup> in the inertial <u>world</u> frame are shown. 


Fig. 5: Estimation results of the <u>proposed FRS and the baseline DRS and SRS filters during</u> Digit squatting on a pitching ground (i.e., under test cases **<u>T3</u>** and **T4** ) under significant initial errors. The notational convention follows Fig. 4. 

non-inertial ground and theref ~~or~~ e does not converge, resulting in significantly larger positio ~~n~~ errors. In contrast, both FRS and DRS render the base position observable. 

As summarized in Tab. I ~~II~~ , FRS achieves steady-state position errors below 4 cm in <u>Cases</u> **<u>T1</u>** - **<u>T4</u>** <u>, compared to</u> approximately 10 cm for DRS. In Case **T5** , FRS maintains good performance through contact-noise mitigation, including mechanical impact absorption at the feet, stable contact switching during double support, and low-pass filtering of IMU data. These measures are detailed in the supplementary file, which also compares the results with an unmitigated experiment. As a result, FRS outperforms SRS and, despite residual jumps in the velocity estimates, achieves better _x_ - and _y_ -position estimates than DRS using only onboard sensing. 

_5) Reconstruction of base orientation with filter augmentation:_ To validate the proposed IMU augmentation strategy for recovering base-orientation observability, three IMUs are 

mounted at distinct, non-colli ~~ne~~ ar locations on the robot torso, as illustrated in Fig. 7. Thes ~~e~~ IMU positions define a plane rigidly attached to the torso, from which an effective base frame _{B}_ can be reconstruc ~~te~~ d. 

~~Experimental data are colle~~ cted while Digit stands on the treadmill undergoing pitching motion **GM3** , with the robot oriented at 15<sup>_◦_</sup> . Under this test condition, the relative base position is fully observable, enabling reconstruction of the base orientation as described in Sec. VI. The reconstructed base orientation closely matches the motion-capture-based ground truth, as shown in Fig. 7. The mean absolute errors are 0.3904°, 0.2709°, 0.3241° in roll, pitch, and yaw, respectively. The small residual discrepancies (below 2<sup>_◦_</sup> ) are primarily attributed to curved mounting surfaces on the torso and limited precision in relative IMU placement. Still, the results confirm that augmenting the proposed FRS framework with multiple torso-mounted IMUs enables reliable recovery of base orien- 

8 


Fig. 6: Estimation results of the proposed FRS and the baseline DRS and SRS filters during Digit walking on a pitching ground for test case **T5** under significant initial errors. The notational co ~~n~~ version follows Fig. 4. 

tat ~~io~~ n, thereby achieving full state observability in practic ~~e.~~ 

## VIII. CONCLUSION 

This paper has presented a proprioceptive invariant extended Kalman filter for state estimation of humanoid robots operating on accelerating ground. By exploiting foot-mounted inertial measurement units (IMUs), the filter explicitly accounts for ground-induced nonlinearities without requiring direct groundmotion measurements or external instrumentation. Observability analysis showed that the robot’s base position and velocity relative to the moving ground are observable under general ground motions and that base orientation can be recovered in practice through simple torso-IMU augmentation. Experiments on the Digit humanoid robot during standing, squatting, and walking on a moving treadmill validated the proposed approach and demonstrated fast convergence, high accuracy, and robustness to impact-induced foot-IMU noise, even under large initial errors. Compared with existing InEKF baselines for static and instrumented dynamic ground, the proposed filter achieves comparable or superior performance using solely onboard sensing. Our future work will explore the integration of the proposed filter with locomotion planners and controllers formulated directly in the dynamic ground frame. 

## REFERENCES 

- [1] M. Bloesch, M. Hutter, M. Hoepflinger, S. Leutenegger, C. Gehring, C. David Remy, and R. Siegwart, “State estimation for legged robots: Consistent fusion of leg kinematics and imu,” in _Rob.: Sci. Syst. VIII_ , Jul. 2012. 

- [2] M. Camurri, M. Ramezani, S. Nobili, and M. Fallon, “Pronto: A multisensor state estimator for legged robots in real-world scenarios,” _Front. Rob. AI_ , vol. 7, Jun. 2020. 

- [3] D. Cheng, J. Kang, and X. Xiong, “Simultaneous calibration of noise covariance and kinematics for state estimation of legged robots via bilevel optimization,” _arXiv:2510.11539_ , 2025. 

- [4] V. Agrawal, S. Bertrand, R. Griffin, and F. Dellaert, “Proprioceptive state estimation of legged robots with kinematic chain modeling,” in _IEEE Int. Conf. Humanoid Rob._ , Nov. 2022, pp. 178–185. 

- [5] A. Barrau and S. Bonnabel, “The invariant extended kalman filter as a stable observer,” _IEEE Trans. Autom. Contr._ , vol. 62, no. 4, pp. 1797– 1812, 2016. 


Fig. 7: (a) Experimental setup for base-orientation reconstruction using three torso-mounted IMUs under the FRS framework. (b) Reconstructed relative base orientation **R**<sup>_B_</sup> _t_ compared with ground truth, validating accurate orientation recovery through IMU augmentation. 

- [6] R. Hartley, M. Ghaffari, R. M. Eustice, and J. W. Grizzle, “Contactaided invariant extended kalman filtering for robot state estimation,” _Int. J. Rob. Res._ , vol. 39, no. 4, pp. 402–430, 2020. 

- [7] S. Teng, M. W. Mueller, and K. Sreenath, “Legged robot state estimation in slippery environments using invariant extended kalman filter with velocity update,” in _IEEE Int. Conf. on Robotics and Automation_ , May 2021, pp. 3104–3110. 

- [8] Y. Gao, C. Yuan, and Y. Gu, “Invariant Filtering for Legged Humanoid Locomotion on a Dynamic Rigid Surface,” _IEEE/ASME Trans. Mechatron._ , vol. 27, no. 4, pp. 1900–1909, Aug. 2022. 

- [9] Z. He, S. Teng, T.-Y. Lin, M. Ghaffari, and Y. Gu, “Invariant filtering for full-state estimation of ground robots in non-inertial environments,” _IEEE/ASME Trans. Mechatron._ , pp. 1–10, 2025. 

- [10] T.-Y. Lin, R. Zhang, J. Yu, and M. Ghaffari, “Legged robot state estimation using invariant kalman filtering and learned contact events,” in _Conf. Rob. Learn._ , 2021. 

- [11] Y. Wu, J. Kuang, S. Khorshidi, X. Niu, L. Klingbeil, M. Bennewitz, and H. Kuhlmann, “Doglegs: Robust proprioceptive state estimation for legged robots using multiple leg-mounted imus,” in _IEEE Int. Conf. Int. Rob. Syst._ , 2025, pp. 8856–8863. 

- [12] S. Yang, Z. Zhang, J. Z. Zhang, I. S. Sow, and Z. Manchester, “Multiimu sensor fusion for legged robots,” _arXiv:2507.11447_ , 2025. 

- [13] F. E. Xavier, G. Burger, M. Pétriaux, J.-E. Deschaud, and F. Goulette, “Multi-IMU proprioceptive state estimator for humanoid robots,” in _IEEE Int. Conf. Int. Rob. Syst._ , 2023. 

- [14] Y. Gao, V. Paredes, Y. Gong, Z. He, A. Hereid, and Y. Gu, “Timevarying foot placement control for humanoid walking on swaying rigid surface,” _IEEE Trans. Rob._ , vol. 41, pp. 5740–5760, 2025. 

- [15] A. Iqbal, Y. Gao, and Y. Gu, “Provably stabilizing controllers for quadrupedal robot locomotion on dynamic rigid platforms,” _IEEE/ASME Trans. Mechatron._ , vol. 25, no. 4, pp. 2035–2044, 2020. 

- [16] J. Stewart, I.-C. Chang, and Y. Gu, “Adaptive ankle torque control for bipedal humanoid walking on surfaces with unknown horizontal and vertical motion,” in _Amer. Contr. Conf._ , 2025, pp. 4647–4652. 

- [17] A. Iqbal, S. Veer, and Y. Gu, “Analytical solution to a time-varying LIP model for quadrupedal walking on a vertically oscillating surface,” _Mechatron._ , vol. 96, p. 103073, 2023. 

- [18] Z. He, S. Teng, T.-Y. Lin, M. Ghaffari, and Y. Gu, “Legged robot state estimation within non-inertial environments,” in _IEEE Conf. Dec. Contr._ , Dec. 2024, pp. 2469–2474. 

- [19] S. Lee and K.-S. Kim, “Attention-based neural-augmented kalman filter for legged robot state estimation,” _IEEE Rob. Autom. Lett._ , vol. 11, no. 4, pp. 4122–4129, 2026. 

- [20] C. Yu, Y. Yang, T. Liu, Y. You, M. Zhou, and D. Xiang, “State estimation transformers for agile legged locomotion,” in _IEEE Int. Conf. Intel. Rob. Syst._ , 2024, pp. 6810–6817. 

- [21] D. Youm, H. Oh, H. Kim, and J. Hwangbo, “Legged robot state estimation with invariant extended kalman filter using neural measurement network,” in _IEEE Int. Conf. Rob. Autom._ , 2025, pp. 670–676. 

- [22] K. M. Lynch and F. C. Park, _Mod. Rob._ Cambridge Univ. Press, 2017. 

- [23] R. E. Kalman, “A new approach to linear filtering and prediction problems,” _ASME. J. Basic Eng. March_ , 1960. 

- [24] Z. Chen, K. Jiang, and J. C. Hung, “Local observability matrix and its application to observability analyses,” in _Ann. Conf. IEEE Ind. Electron. Soc._ , 1990, pp. 100–103. 

