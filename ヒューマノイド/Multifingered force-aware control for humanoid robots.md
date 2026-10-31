---
title: "Multifingered force-aware control for humanoid robots"
date: "2026-03-09"
authors: "Pasquale Marra; Gabriele M. Caddeo; Ugo Pattacini; Lorenzo Natale"
url: https://arxiv.org/abs/2603.08142
pdf: https://arxiv.org/pdf/2603.08142
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.08142)** / [論文ページ](https://arxiv.org/abs/2603.08142)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

_© 2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works._ Preprint version (Mar. 2026). This work has been accepted for publication in ICRA 2026. 

# **Multifingered force-aware control for humanoid robots** 

Pasquale Marra<sup>1</sup><sup>_,_2</sup> , Gabriele M. Caddeo<sup>1</sup> , Ugo Pattacini<sup>3</sup> and Lorenzo Natale<sup>1</sup> 


Fig. 1: Real robot (left) and its virtual counterpart [1] (right). ergoCub, equipped with tactile sensors, balances a tray with an unknown object by minimizing the distance between the supporting polygon center and the estimated Center of Pressure (cyan sphere), computed from normal forces (orange arrows). 

**_Abstract_ — In this paper, we address force-aware control and force distribution in robotic platforms with multi-fingered hands. Given a target goal and force estimates from tactile sensors, we design a controller that adapts the motion of the torso, arm, wrist, and fingers, redistributing forces to maintain stable contact with objects of varying mass distribution or unstable contacts. To estimate forces, we collect a dataset of tactile signals and ground-truth force measurements using five Xela magnetic sensors interacting with indenters, and train force estimators. We then introduce a model-based control scheme that minimizes the distance between the Center of Pressure (CoP) and the centroid of the fingertips contact polygon. Since our method relies on estimated forces rather than raw tactile signals, it has the potential to be applied to any sensor capable of force estimation. We validate our framework on a balancing task with five objects, achieving a** 82 _._ 7% **success rate, and further evaluate it in multi-object scenarios, achieving** 80% **accuracy. Code and data can be found here https://github.com/hsp-iit/multifingered-force-aware-control.** 

## I. INTRODUCTION 

Robots meant to live alongside and assist humans must continuously refine their actions through sensory feedback [2]. While computer vision has advanced dramatically—reaching or surpassing human-level performance in 

This work was supported by the National Institute for Insurance against Accidents at Work (INAIL) project ergoCub-core. 

> 1Humanoid Sensing and Perception, Istituto Italiano di Tecnologia, Genoa, Italy. Acknowledge financial support from the PNRR MUR project PE0000013-FAIR. 

> 2DIBRIS, Universit`a di Genova, Via All’Opera Pia, 13, Genoa, Italy., Genoa, Italy. 

> 3 MESH Facility, Istituto Italiano di Tecnologia, Genoa, Italy 

some domains—tactile sensing still lags behind. Vision can substitute for some perceptual aspects of touch, but it poorly captures contact dynamics: the interaction forces are difficult to measure reliably with external cameras. Humans routinely exploit touch for prehensile and non-prehensile manipulation: when holding a box with unknown contents or serving a tray, shifts in mass distribution are compensated by posture and hand adjustments driven by subtle force variations. Accordingly, many tactile sensors have been proposed, including finger-like, flat, and all-around designs based on magnetic [3], [4], capacitive [5], or vision-based principles [6], [7]. Their multimodal capabilities have enabled pose [8], [9], shape/curvature [10], [11], dynamic control [12], and texture estimation [13]. However, outputs differ substantially across technologies, and even within the same sensor family; therefore, manipulation methods that consume raw tactile signals often do not transfer across sensor types. A promising alternative is to map tactile outputs into the force domain: estimating 3D contact forces yields a sensor-agnostic representation that generalizes more robustly across devices [14], [15]. Yet, although force feedback is widely used in manipulation, multifingered strategies are typically limited to prehensile tasks, whereas non-prehensile approaches often rely on single-finger feedback [16]. In this work, we introduce a model-based indirect control strategy to balance in-hand objects with varying mass distribution by distributing contact forces across a multi-fingered hand. We maximize stability by minimizing the distance between the Center of Pressure (CoP), estimated from fingertip force measurements, and the geometric center of the fingertip contact polygon.To enable force feedback, we train a lightweight network to estimate 

3D forces from custom magnetic Xela sensors [17] using a calibrated testbed with 3D-printed indenters. The model is deployed on the ergoCub [18] hand equipped with these fingertip sensors. A 3D-printed tray is placed on the hand and an object of unknown mass is positioned arbitrarily on it. Estimated fingertip forces are processed by a controller that computes the CoP and the desired plane rotation, then moves the fingertips to minimize the error between the CoP and the geometric center of the contact polygon, while keeping the fingertip positions on the plane. In parallel, a secondary controller supports finger control to maintain continuous contact with the tray and compensate for sources of error. This layered structure enables stable balancing while remaining agnostic to the tactile sensor type. The approach can serve as a robust low-level primitive within hierarchical frameworks or as a standalone solution for force-based inhand balancing. We validate it by balancing an unknown object on the tray and preventing it from falling; an example is shown in Fig. 1. In summary, the contributions of this work are threefold: 

- We present a dataset containing calibrated 3D forces, relative poses, and tactile outputs for our custom fingerlike Xela sensors, collected with a dedicated testbed. 

- We provide a comprehensive characterization of the sensor performance and limitations, offering insights into its applicability for force estimation in manipulation. 

- We propose a multifingered control algorithm for balancing in-hand objects by acting on force distribution. The controller operates directly in the force domain, making it conceptually applicable across different tactile sensors. 

## II. RELATED WORKS 

Our work is closely related to manipulation control frameworks using tactile sensing. While there remains interest in solving manipulation tasks without tactile feedback [19], there is a growing focus on integrating tactile sensors into robotic hands control [20], [21]. Early works primarily relied on single-finger feedback. For instance, in [16], the structural similarity index measure (SSIM) computed from TacTip images was used to control the closure of a Pisa/IIT SoftHand [22]. Similarly, in [23], Xela uSkin sensors were calibrated for force estimation using an on-hand method, and validated by controlling a single Allegro hand finger [24]. More recent works explore multi-finger control for prehensile tasks. In [25], a joint-level adaptive torque controller tracked desired finger velocities, while BioTac sensors [26] were used to estimate the contact frame orientation. In [27], grasp forces of the Allegro hand were modulated based on shear measurements from five MicroTac sensors. Other approaches estimate pseudo-forces from tactile signals: e.g., [28] employed pseudo-forces reconstructed from Xela uSkin outputs for force direction control, while [29] used pseudo-forces derived from BioTac sensors for grasp force regulation. In [30], fingertip forces were obtained by averaging raw outputs of magnetic tactile sensors to roll a cylinder with two fingers. Whole-body controllers have been proposed for humanoid 

balancing and locomotion tasks [31], [32]. These approaches similarly exploit a large number of joints and degrees of freedom to achieve stability. However, they do not control the fingers explicitly, and therefore cannot address multifingered in-hand manipulation. In [33], a tray is fixed at the end of a robotic manipulator to perform non-prehensile transportation. However, it is assumed that the object’s shape and dynamical properties are known. In contrast, we develop an upper-body controller that extends the multi-joint reasoning of wholebody approaches to also include multicontact control of the fingers of a robotic hand, while making no assumption about the object. To the best of our knowledge, this is the first work to combine an upper-body controller with multifingered force distribution for non-prehensile manipulation. 

## III. METHOD 

In our scenario, a humanoid robot equipped with a multifingered hand and fingertip force sensors must balance an object with varying mass distribution, using fingertip force feedback to adjust its hand pose. 

Let _F_ Π = ( _O_ Π _, R_ Π) be the orthonormal frame with origin in _O_ Π _∈_ R<sup>3</sup> and orientation _R_ Π = [ _b, t, n_ ] _∈ SO_ (3), with _O_<sup>˙</sup> Π _, O_<sup>¨</sup> Π denoting its linear velocity and acceleration, and _ω_ Π _, ω_ ˙ Π its angular velocity and angular acceleration, respectively. Let Π be the plane passing through the origin _O_ Π with unit normal vector _n ∈_ R<sup>3</sup> . Our objective is to design a control architecture that: 

- controls the finger positions so as to establish contact with a planar base coincident with the plane Π; 

- employs finger force measurements to adapt the pose of the frame _F_ Π, and consequently the pose of the plane Π. 

In this configuration, a planar object can be placed on the fingertips, establishing a correspondence with the virtual plane Π. This correspondence need not be exact, since the controller ensures fingertip contact with the object to compensate for misalignment. Moreover, we do not attempt to directly control the forces measured at the fingertips, as no assumptions are made about the object’s inertial properties. Fig. 2 shows our pipeline. This section proceeds as follow: in III-A we detail the characterization of the sensors and the dataset collection for force estimation; in III-B we define the finger positions control; then in III-C we show how the fingertip force measurements are used to affect the plane Π pose, leveraging the concept of Center of Pressure (CoP). 

## _A. Sensor characterization and Dataset collection_ 

_1) Setup:_ To characterize the sensor and collect the dataset, we use the setup shown in Fig. 3a. A 3D-printed base secures the fingertip, while 3D-printed indenters (similar to those in [34], Fig. 3b) are mounted on the end effector of the Omega3 robot [35]. An ATI Nano17 force/torque sensor is placed between the robot and the indenter to measure applied forces, which are then projected onto the fingertip frame using the known transformation between the F/T sensor and the fingertip. For all experiments, we subtract an offset 


Fig. 2: Overview of the control pipeline. Finger positions (magenta spheres) are projected onto the plane (yellow rectangle), and normal force components (orange arrows) are used to compute the CoP (cyan sphere) in the plane frame. From this, a new target pose for the plane is generated, and finger and joint positions are updated with a corrective term for inaccuracies. 

for each tactile sensor, estimated by averaging a thousand readings when the sensor is not in contact. 

_2) Sensor characterization:_ We employ a custom version of the Xela sensors specifically designed for the ErgoCub hand (called uSCu). Each fingertip consists of five magnetic taxels that can displace in three directions (x, y, z) under applied force. Before collecting the dataset, we first characterize the sensor behavior with respect to three aspects most relevant to our scenario: **repeatability** of the measurements, **consistency** across different sensors, and the effect of **gravity** on tactile readings. 

To assess repeatability, we repeatedly press an indenter on the fingertip by controlling the robot’s position with 0 _._ 01 _mm_ precision. The robot maintains contact for five seconds, rests for another five seconds, and repeats the motion. This experiment is conducted three times at reference positions corresponding to contact forces of approximately 2 _N_ , 4 _N_ , and 6 _N_ . Higher forces are not considered, since the fingertips are mechanically tested only up to 5 _N_ . While the sensor produces consistent outputs at 2 _N_ , performance deteriorates at higher forces due to hysteresis. Fig. 3c illustrates this effect: the top plot shows the sequence of applied forces, while the bottom plot reports the output of one taxel, highlighting the growing influence of hysteresis with repeated touches. 

To validate consistency, we perform a similar test across different fingertips. The robot is controlled in position along the z-axis, with the reference incremented by 0 _._ 2 _mm_ at each step, producing gradually increasing contact forces. Fig. 4 shows the results: despite identical inputs, the taxels of different sensors produce different outputs, confirming variability across sensors. 

Finally, we mount the fingers on the ErgoCub hand and perform random 6D movements. We observe that tactile readings vary significantly with orientation. More critically, the displacement of the taxels follows gravity, producing opposite responses w.r.t. to contact cases. For instance, when the fingertip is inverted, multiple taxels move outward due to gravity, a behavior that never occurs under actual contact. 

_3) Data collection:_ To estimate forces, we train a neural network to predict the 3D fingertip force vector from raw sensor readings. To collect data, we define contact points 

with Poisson sampling on the sensor surface, and for each point we generate random indentation trajectories. These are constrained within a cylinder centered at the contact point (radius 1 _mm_ to prevent tangential slip, height 5 _mm_ to avoid excessive forces). Data are collected by controlling the robot probe in position, ensuring contact across a wide variety of fingertip poses. During collection, the fingertip is fixed facing upward. To mitigate the gravity effect described in Sec. III-A.2, we augment the dataset with additional nocontact samples acquired by mounting the sensors on the robot and applying random wrist and finger motions, to avoid out-of-distribution inputs during experiments. In total, we collect about 200k force–tactile pairs using all indenters, which are then balanced and reduced to 20k per sensor. Results of the calibration are reported in Section IV. 

## _B. Finger positions control_ 

We now describe how we control the fingers. Consider _d_ fingers and let _Di ∈_ R<sup>3</sup> _, D_ ˙ _i ∈_ R<sup>3</sup> _, D_ ¨ _i ∈_ R<sup>3</sup> _, i_ = 1 _, . . . , d_ be the position, linear velocity, and linear acceleration of the i-th finger, respectively. Notice that the kinematic chain up to the hand palm is shared by all the fingers. Therefore, the joint positions vector for the i-th finger can be expressed as: _qi_ = [ _qc_<sup>_Tq_</sup> _fi_<sup>_T_]</sup><sup>_T_,where</sup><sup>_qc∈_R</sup><sup>_nC_arethejointscommonto</sup> the finger kinematic chains ( _nC_ = 10, that is torso-shoulderelbow-wrist) and _qfi ∈_ R<sup>_nF i_</sup> are those specific of the i-th finger ( _nF_ = 2 for thumb and index, _nF_ = 1 for the others). We can construct a joint position vector: 


The joint velocities _q_ ˙ and accelerations _q_ ¨ are related to the finger linear acceleration as follows: 


where _JP,i ∈_ R<sup>3</sup><sup>_×_(</sup><sup>_nC_+</sup><sup>_nF_1+</sup><sup>_···_+</sup><sup>_nFd_)</sup> is the positional part of the geometric Jacobian and _J_<sup>˙</sup> _P,i_ its time derivative. For each finger position, we are interested in calculating its 


Fig. 3: a) Data collection setup. b) Indenters. c) Effect of hysteresis on the tactile readings. The graphic above shows the indented force (N) over time (s), while the bottom graphic shows the output of the sensor’s taxel over time. 

orthonormal projection _Di_<sup>Π</sup><sup>_∈_R3ontheplaneΠ:</sup> 


where _Pn_<sup>Π≜</sup><sup>_n · nT_istheorthogonalprojectorontothe</sup> line spanned by _n_ ; _Dt,i_<sup>Πisthedisplacement,thatliesonΠ,</sup> between the projection _Di_<sup>Πandtheorigin</sup><sup>_O_Π;</sup><sup>_D_</sup> _n,i_<sup>Πisthe</sup> displacement, parallel to the unit normal vector _n_ , between the projection _Di_<sup>Π</sup> and the finger position _Di_ . Using the previously defined quantities, in the following we define the two modules composing the finger positions control: the QP problem, whose unknowns are the joint accelerations _q_ ¨, and the _Keep in Touch_ module. 

_1)_ **_QP formulation_** _:_ we cast the finger positions control as: 


where the joint acceleration constraints are defined as ( [36]): 


with _kl ∈_ (0 _,_ 1], _δt_ is the control period and [ _q_<sup>_L_</sup> _, q_<sup>_U_</sup> ] is the joint range. 

_2)_ **_Bring the fingers on the plane_** _:_ we start by defining the terms of the QP. We want each fingertip position to lie on the plane Π, so as to arrange the fingers on a planar support. We do so by imposing the following dynamics: 


Fig. 4: Consistency validation across sensors shows variability in tactile outputs under identical applied forces. 

with _D_<sup>˙</sup> _n,i_<sup>Πand</sup><sup>_D_¨</sup> _n,i_<sup>Πfirst and second order time derivative of</sup> (3c), _Kn,d_ and _Kn,p_ positive scalars. This is an asymptotically stable dynamics and converges to _Dn,i_<sup>Π=0,meaning</sup> that the i-th finger position converges to its projection on the plane Π. Substituting (2) and the second-order time derivative of (3c) in (6), we obtain: 


with: 


for _i_ = 1 _, . . . , d_ . We define the relative cost function term as follows: 


where _W_ 1 _>_ 0 and _||x||_<sup>2</sup> _W_<sup>=</sup><sup>_xT Wx_.</sup> 

_3)_ **_Align the centroid of the finger projections to the origin of the plane frame_** _:_ we want the position of the fingertips centroid projection to correspond to the origin of the plane frame, because this point is also the target for the CoP control (III-C). We define the error: 


and impose the error dynamics: 


with _e_ ˙ _t_ and _e_ ¨ _t_ first and second order time derivative of _et_ , _Kt,d_ and _Kt,p_ positive scalars. The dynamics (11) ensures that the geometric center of the fingertips converges to the origin _O_ Π. Substituting (2) and the second-order time 

derivative of (3b) in (11), we obtain: 


and define the relative cost function term: 


with _W_ 2 _>_ 0. 

_4)_ **_Joint positions control_** _:_ we further add a postural term to keep the robot joint positions close to the initial configuration _q_<sup>0</sup> : 


and define: 


with: _b_ 3 = _−Kd,q · q_ ˙ + _Kp,q ·_ ( _q − q_<sup>0</sup> ) and _W_ 3 _>_ 0. _5)_ **_Bound Joint Accelerations_** _:_ this term bounds the required joint accelerations for the task and helps the solver convergence. 


_6)_ **_Keep in touch_** _:_ in addition to the QP generated references _q_ Π, we introduce a contribution _δq_ Π to compensate for small inaccuracies in the model, and mechanical imprecision due to finger tendon actuations. We call this module the _Keep in Touch_ controller. This contribution is added only to the finger joints _qfi_ and it is evaluated from the finger force _Fi_ . Given a force threshold _Fth_ , if _Fth > Fi_ , then we update the offset so as to close the finger: 


where _qu_<sup>_fi_istheupperboundfortherangeof</sup><sup>_qfi_and</sup><sup>_q_</sup> _m_<sup>_fi_</sup> is the measured joint position, and _Kp,f_ positive scalar. On the other hand, when _Fth < Fi_ and the finger is closing, if necessary, we only update this offset in order to guarantee that _δq_ Π _< qu_<sup>_fi−q_Π.Thethresholdissettoaccountfor</sup> hysteresis effects. 

_C. Plane pose evolution under the effect of the finger force measurements_ 

Based on the knowledge of the measured forces at the fingertips, we want to implement an **indirect** control of the CoP by adjusting the pose of the plane Π. The idea is to move the CoP towards the plane frame origin, which is also the target position of the fingers centroid control (see III-B.3). We define _Fi_ as the force measured by the i-th fingertip. 

_1)_ **_CoP calculation_** _:_ for each _Fi_ , we calculate the magnitude of the normal component _Rn,i ∈_ R and the resultant _Rn ∈_ R as: 


Notice that _Rn,i ≥_ 0 because the fingertips can only push on the plane. Then, assuming that the force _Fi_ is applied at the finger projection _Di_<sup>Π,wecalculatetheCoPpositionrelative</sup> to the origin _O_ Π as [37]: 


_2)_ **_Plane trajectory_** _:_ We introduce the rotation matrix _Re_ as: 


where _Rotation_ ( _·_ ) calculates the rotation matrix from an axis-angle representation, _Kp,e_ and _Ki,e_ are positive scalars, and _s_ is the cross product between (19) and the plane normal. The rotation matrix _Re_ is interpreted as the rotation that, applied to the initial plane orientation _R_ Π<sup>_i_,couldbring</sup> the CoP towards the origin _O_ Π. Note that the integral action in (20b) is introduced because the rotation due to the proportional action alone may be insufficient to cause the object to slide on the plane. We generate the plane trajectory as in the following: 


with _O_ Π<sup>_i_isthe(desired)initialplaneposition.</sup> 

## IV. EXPERIMENTAL RESULTS 

We evaluate our method in two stages: first, by validating the precision of the force estimation network, and second, by testing the controller on balancing performance on a set of objects. The task consists in balancing an object on top of a 3D-printed tray held by the ergoCub hand. Because the hand is equipped with four Xela sensors, only four fingers are used. The tray weighs 250 _g_ , measures 27 _cm_ x 17 _cm_ , and includes 2 _cm_ -high barriers (0 _._ 5 _cm_ thick) along the edges. These barriers prevent small objects from falling but still allow objects of higher mass to fall, ensuring the task remains non-trivial. The tray dimensions are constrained by the robot’s hand span, with the thumb–little finger distance being 25 _cm_ . We test five objects spanning different shapes, materials, and internal dynamics: 

- Object 1–3: a paper tea box, filled with varying amounts of small plastic balls containing modeling clay of different weights (122 _._ 7 _g_ , 152 _._ 6 _g_ , 216 _._ 2 _g_ ), producing different mass distributions. 

TABLE I: Results of the experiments. Force estimation uses different networks for each finger (first five rows) and one network for all the fingers (last row). Each metric is evaluated at different positions (1–5) and on average. 

||||**Time **|**(s)**||||**Dist**|**ance C**|**oP (cm**|**)**|||**S**|**uccess r**|**ate (%)**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|_Position_|_1_|_2_|_3_|_4_|_5_|_Mean_|_1_|_2_|_3_|_4_|_5_|_Mean_|_1_|_2_|_3_|_4_|_5_|_Mean_|
|**Object 1**|9_._2|6_._5|6_._4|42_._1|40_._5|20_._9|35_._0|13_._2|13_._6|33_._4|31_._9|25_._4|66_._7|100_._0|100_._0|100_._0|100_._0|93_._3|
|**Object 2**|8_._8|9_._5|5_._2|24_._6|28_._9|15_._4|14_._1|6_._4|3_._1|12_._6|15_._0|10_._2|100_._0|100_._0|66_._7|100_._0|66_._7|86_._7|
|**Object 3**|9_._0|7_._4|5_._1|29_._3|/|12_._7|9_._3|2_._3|6_._7|21_._7|/|10_._0|100_._0|100_._0|100_._0|66_._7|0_._0|73_._3|
|**Object 4**|12_._3|28_._4|11_._9|22_._2|22_._8|19_._52|44_._0|168_._0|15_._2|93_._2|25_._0|69_._1|66_._7|66_._7|33_._3|100_._0|66_._7|66_._7|
|**Object 5**|42_._3|20_._94|39_._7|5_._7|43_._0|30_._3|34_._6|21_._7|10_._3|21_._0|33_._2|24_._2|66_._7|100_._0|100_._0|100_._0|100_._0|93_._3|
|‘**Object 3 (SN)**|/|/|26_._8|5_._1|11_._7|11_._5|/|/|5_._8|1_._2|2_._7|2_._9|0|0|67|100|67|47|


Fig. 5: Starting position on the tray. The superimposed hand shows the position of the hand under the tray. 

- Object 4: a fabric ball filled with sand (98 _._ 6 _g_ ). 

- Object 5: an aluminum box filled with modeling clay (125 _._ 6 _g_ ). 

Objects are chosen to weigh between 100 _g_ and 300 _g_ , so that they could be reliably sensed by the Xela sensors, and they remain below the tested fingertip limit of 5 _N_ of sustainable load. 

Each fingertip uses a dedicated force estimation network trained on its own calibration dataset to maximize accuracy. To assess the necessity of this choice, we conduct an ablation in which a single shared network is used across all fingers (evaluated on Object 3). We perform all the experiments with the following parameters: _W_ 1 = _W_ 2 = 10 _._ 0, _W_ 3 = 0 _._ 01, _W_ 4 = 2 _._ 5, _Kp,q_ = 15 _._ 0, _Kd,q_ = 5 _._ 0, _Kt,p_ = _Kn,p_ = 140 _._ 0, _Kt,d_ = _Kn,d_ = 10 _._ 0, _kl_ = 0 _._ 9, _δt_ = 0 _._ 01, _Kp,ω_ = 100, _Kp,e_ = 8000 _∗_ ( _π/_ 180), _Ki,e_ = 25 _∗_ ( _π/_ 180), _Kp,f_ = 50 _._ 0 _∗_ ( _π/_ 180 _._ 0), _Fth_ = 0 _._ 15 _N_ . We limit the maximum plane orientation to 30<sup>_◦_</sup> along all three axes to constraint the speed of the object while moving on the tray. In the following we report results of the force estimation, of the balancing task employing single and multiple objects. 

_1) Force estimation:_ We train a regressor using the dataset described in Sec. III-A.3. The regressor is a multilayer perceptron (MLP) with four linear layers, interleaved with LayerNorm and GELU activation functions. Following the 

characterization study in Sec. III-A.2, we address sensorto-sensor variability by training a separate regressor for each sensor. We validate these regressors on test datasets collected by touching the sensors in poses different from those used for training. For comparison, we also train the same architecture on the combined data from all sensors and evaluate it on all test sets. On average, the single-sensor regressors achieve a normalized MAE of 9%, while the multi-sensor regressor reaches 13%. 

_2) Single object balancing experiments:_ For each object, we perform 15 trials by placing it in five different positions on the tray, with three repetitions per position. The positions are chosen by uniformly dividing the tray along its major axis. Fig. 5 shows the positions on the tray. We evaluate performance using three metrics. First, the time to convergence. Second, the distance traveled by the CoP, indicating how many corrections are required to balance the object (movements under 5 mm are ignored to filter sensor noise). Third, the success rate, when convergence is reached within 120 _s_ , also accounting for those cases in which the object falls. Converges is obtained by maintaining the distance between the CoP and the plate centroid under 3 cm threshold for at least 5 s. This threshold ensures the CoP remains inside the fingertip contact polygon, while accounting for sensor noise and static friction effects, which prevent motions from small rotations of the plane, thus not allowing small corrections. Only successful runs are included in the Time and CoP Distance metrics. The first five rows of Table I summarize the results. The best performance is obtained with the lightest objects (Object 1 and 5), since their lower friction and small momentum when contacting the barriers are insufficient to lead to failure cases. In contrast, Objects 3 and 4 show the lowest performance. Balancing Object 3 is difficult because higher friction requires larger plane inclinations to induce motion, often leading to unrecoverable situations. Object 4, instead, can roll easily; even small rotations generate high momentum, causing strong impacts against the barriers and eventual falls. Regarding object position, _Position 4_ is the easiest to balance, being closest to the center of the support polygon (around the index/middle finger), whereas _Positions 1, 2, and 3_ are farther away and therefore harder to control. Small plane inclinations, needed to correct minor unbalances, strongly affect Object 4, while Object 3 demands larger inclinations due to static friction. When the CoP is near the support polygon center, the controller also reacts more 


Fig. 6: CoP error for a success (top) and a failure (bottom) episode. In the failure case, the error drops below the threshold but is highly unstable. 

slowly. This behavior is reflected in the _CoP Distance_ metric: Object 4 exhibits much larger CoP movements, while Object 3 remains comparable to the others. Finally, to validate our choice of training a separate force estimator for each finger, we conduct an ablation using a single shared network ( **SN** ) on Object 3, shown in the last row of Table I. Results show a 26% performance drop, confirming the benefit of fingerspecific estimators: when force estimation is unreliable, the system struggles to converge. This outcome is consistent with the findings in Section IV-.1. 

Next, we analyze the primary reasons for failure for each object. Object 3 and 4 consistently fail because of strong momentum that impacts the barrier. Object 2 fails once because of the momentum and once because of exceeding convergence time, Object 5 for strong impact with barriers; in the _SN_ case, Object 3 fails seven times because of exceeding convergence time, while one time it fails because its speed generates a large impact with the border of the table. In general, potential inaccuracies in the force estimation may affect the outcome of the experiment. The results are expected, as the heavier object (Object 3) and the object with less static friction (Object 5) tends to accumulate more momentum. Fig. 6 shows the CoP error over time for a failure and for a success episode. The accompanying video provides a visual demonstration of the objects and experiments. 

_3) Multiple objects balancing experiments:_ To further check the robustness of our approach, we conduct experiments with multiple objects simultaneously. In particular, we use two aluminum boxes filled with modeling clay (as in Object 5), for a total weight of 299 _g_ . We randomly place the boxes on the tray, varying their position. The boxes are placed in three predefined configurations (opposite sides, same side, and center), with exact positions randomized 

across five trials each, obtaining 80%, 60%, and 100% success rate respectively. All failures result from excessive plane tilting caused by strong impacts with the objects. In successful trials, the average convergence time is 11 _._ 3 _s_ , and the CoP travels 13 _cm_ on average. These outcomes are consistent with the single-object experiments reported in Section IV-.2. When the objects are placed on the same side, the CoP error increases, requiring larger plane inclinations; this amplifies object momentum and leads to strong barrier impacts. Such failures occur primarily when the objects move simultaneously, behaving as a single mass. Failures with objects set apart arise for a similar reason: the plane inclines to reduce the error, one object slides rapidly toward the other, and the impact with the plane border causes failure. These outcomes are expected, as they mirror the dynamics observed in the single-object case. 

_4) Ablation on control frequency:_ To assess the importance of the controller reactivity when dealing with object with varying mass, we repeat the same tests for single objects reported in Section IV-.2, lowering the control frequency to 50 _Hz_ . The lower frequency reduces the system reactivity and hinders proper recovery, especially for fast-moving or rolling objects (e.g., Objects 3 and 4): on average, we experience a 9% drop in success rate. 

## V. LIMITATIONS 

In this section, we discuss the limitations of our work. The first concerns discrepancies between the 3D hand model and tendon friction, which cause misalignment between desired and actual finger motion. Nevertheless, the approach is still able to drive the CoP in most cases, showing robustness to modeling errors. Furthermore, the _Keep in Touch_ control is currently implemented as a separate module: a more systematic approach would integrate this compensation directly into the QP. The second limitation is the plane trajectory module: the trajectory generation in (21) only accounts for the angular position of the plane Π, while its linear position remains constant. Exploiting the full pose of the plane could enhance the balancing performance and also enable the execution of more complex tasks, such as trajectory tracking with the arm while balancing an object. Finally, contact with the palm represent an additional source of error: in some trials, the plane tilts and touches the unsensorized palm, breaking the assumption of fully sensorized contact surfaces. A sensorized palm would mitigate this issue. 

## VI. CONCLUSION 

In this paper, we presented a model-based force-aware control strategy for multifingered robotic hands. By operating in the force domain, our method adapts the motion of the torso, arm, wrist, and fingers to maintain stable contact with objects of varying mass, under the assumption of planar contact; we validated the approach on single-object and multi-object balancing tasks involving diverse shapes and weights, demonstrating robust performance across all scenarios. As future works, we plan to integrate the proposed 

algorithm as a low-level policy within hierarchical manipulation frameworks, particularly for tasks involving bimanual manipulation. 

## REFERENCES 

- [1] Rerun Development Team, “Rerun: A visualization sdk for multimodal data,” Online, 2024, available from https://www.rerun.io/ and https://github.com/rerun-io/rerun. [Online]. Available: https: //www.rerun.io 

- [2] A. G. Billard, “Robots that share our spaces require proprioception and a sense of touch,” _Science_ , vol. 389, no. 6761, p. eaea2492, 2025. [Online]. Available: https://www.science.org/doi/abs/10.1126/science. aea2492 

- [3] L. Jamone, L. Natale, G. Metta, and G. Sandini, “Highly sensitive soft tactile sensors for an anthropomorphic robotic hand,” _IEEE Sensors Journal_ , vol. 15, no. 8, pp. 4226–4233, 2015. 

- [4] J. Li, H. Qin, Z. Song, L. Hou, and H. Li, “A tactile sensor based on magnetic sensing: Design and mechanism,” _IEEE Transactions on Instrumentation and Measurement_ , vol. 73, pp. 1–9, 2024. 

- [5] N. Jamali, M. Maggiali, F. Giovannini, G. Metta, and L. Natale, “A new design of a fingertip for the icub hand,” in _2015 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2015, pp. 2705–2710. 

- [6] A. Sipos, W. van den Bogert, and N. Fazeli, “Gelslim 4.0: Focusing on touch and reproducibility,” 2024. [Online]. Available: https://arxiv.org/abs/2409.19770 

- [7] M. Lambeta, P.-W. Chou, S. Tian, B. Yang, B. Maloon, V. R. Most, D. Stroud, R. Santos, A. Byagowi, G. Kammerer, D. Jayaraman, and R. Calandra, “DIGIT: A novel design for a low-cost compact highresolution tactile sensor with application to in-hand manipulation,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 3, pp. 3838–3845, jul 2020. 

- [8] G. M. Caddeo, N. A. Piga, F. Bottarel, and L. Natale, “Collision-aware in-hand 6d object pose estimation using multiple vision-based tactile sensors,” 2023. [Online]. Available: https://arxiv.org/abs/2301.13667 

- [9] M. Bauza, A. Bronars, and A. Rodriguez, “Tac2pose: Tactile object pose estimation from the first touch,” _The International Journal of Robotics Research_ , vol. 42, no. 13, p. 1185–1209, Sep. 2023. [Online]. Available: http://dx.doi.org/10.1177/02783649231196925 

- [10] G. M. Caddeo, A. Maracani, P. D. Alfano, N. A. Piga, L. Rosasco, and L. Natale, “Sim2real bilevel adaptation for object surface classification using vision-based tactile sensors,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 15 128– 15 134. 

- [11] A.-H. Shahidzadeh, S. J. Yoo, P. Mantripragada, C. D. Singh, C. Ferm¨uller, and Y. Aloimonos, “Actexplore: Active tactile exploration of unknown objects,” 2024. [Online]. Available: https: //arxiv.org/abs/2310.08745 

- [12] M. Oller, D. Berenson, and N. Fazeli, “Tactile-driven non-prehensile object manipulation via extrinsic contact mode control,” 2024. [Online]. Available: https://arxiv.org/abs/2405.18214 

- [13] A. B¨ohm, T. Schneider, B. Belousov, A. Kshirsagar, L. Lin, K. Doerschner, K. Drewing, C. A. Rothkopf, and J. Peters, “What matters for active texture recognition with vision-based tactile sensors,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 15 099–15 105. 

- [14] A. H. Shahidzadeh, G. Caddeo, K. Alapati, L. Natale, C. Ferm¨uller, and Y. Aloimonos, “Feelanyforce: Estimating contact force feedback from tactile sensation for vision-based tactile sensors,” _ArXiv_ , vol. abs/2410.02048, 2024. [Online]. Available: https://api.semanticscholar. org/CorpusID:273097993 

- [15] Z. Chen, N. Ou, X. Zhang, Z. Wu, Y. Zhao, Y. Wang, N. Lepora, L. Jamone, J. Deng, and S. Luo, “General force sensation for tactile robot,” 2025. [Online]. Available: https://arxiv.org/abs/2503.01058 

- [16] N. F. Lepora, C. Ford, A. Stinchcombe, A. Brown, J. Lloyd, M. G. Catalano, M. Bianchi, and B. Ward-Cherrier, “Towards integrated tactile sensorimotor control in anthropomorphic soft robotic hands,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , 2021, pp. 1622–1628. 

   - [19] G. Khandate, C. P. Mehlman, X. Wei, and M. Ciocarlie, “Dexterous in-hand manipulation by guiding exploration with simple sub-skill controllers,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 6551–6557. 

   - [20] J. Egli, B. Forrai, T. Buchner, J. Su, X. Chen, and R. K. Katzschmann, “Sensorized soft skin for dexterous robotic hands,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 18 127–18 133. 

   - [21] Y. Li, P. Wang, R. Li, M. Tao, Z. Liu, and H. Qiao, “A survey of multifingered robotic manipulation: Biological results, structural evolvements, and learning methods,” _Frontiers in Neurorobotics_ , vol. Volume 16 - 2022, 2022. [Online]. Available: https://www.frontiersin. org/journals/neurorobotics/articles/10.3389/fnbot.2022.843267 

   - [22] M. Catalano, G. Grioli, E. Farnioli, A. Serio, C. Piazza, and A. Bicchi, “Adaptive synergies for the design and control of the pisa/iit softhand,” _The International Journal of Robotics Research_ , vol. 33, no. 5, pp. 768–782, 2014. [Online]. Available: https://doi.org/10.1177/0278364913518998 

   - [23] E. Chelly, A. Cherubini, P. Fraisse, F. B. Amar, and M. Khoramshahi, “Tactile-based force estimation for interaction control with robot fingers,” 2025. [Online]. Available: https://arxiv.org/abs/2411.13335 

   - [24] W. Robotics, “Allegro hand,” 2024, accessed: 2025-04-27. [Online]. Available: https://www.allegrohand.com/ 

   - [25] F. Khadivar and A. Billard, “Adaptive fingers coordination for robust grasp and in-hand manipulation under disturbances and unknown dynamics,” _IEEE Transactions on Robotics_ , vol. 39, no. 5, pp. 3350– 3367, 2023. 

   - [26] N. Wettels, J. A. Fishel, and G. E. Loeb, “Multimodal tactile sensor,” in _The Human Hand as an Inspiration for Robot Hand Development_ , ser. Springer Tracts in Advanced Robotics, R. Balasubramanian and V. J. Santos, Eds. Springer International Publishing, 2014, vol. 95, pp. 405–429. [Online]. Available: https://doi.org/10.1007/978-3-319-03017-3 ~~1~~ 9 

   - [27] C. Ford, H. Li, M. Catalano, M. Bianchi, E. Psomopoulou, and N. Lepora, “Shear-based grasp control for multi-fingered underactuated tactile robotic hands,” 03 2025. 

   - [28] D. Kitouni, E. Chelly, M. Khoramshahi, and V. Perdereau, “Fingertip contact force direction control using tactile feedback,” 2024. [Online]. Available: https://arxiv.org/abs/2406.11545 

   - [29] Z. Deng, Y. Jonetzko, L. Zhang, and J. Zhang, “Grasping force control of multi-fingered robotic hands through tactile sensing for object stabilization,” _Sensors_ , vol. 20, no. 4, p. 1050, 2020. 

   - [30] H. Lee, Y. Kim, V. M. Staven, and C. Sloth, “Trajectory optimization for in-hand manipulation with tactile force control,” 2025. [Online]. Available: https://arxiv.org/abs/2503.08222 

   - [31] R. Calandra, S. Ivaldi, M. P. Deisenroth, and Peters, “Learning torque control in presence of contacts using tactile sensing from robot skin,” in _2015 IEEE-RAS 15th International Conference on Humanoid Robots (Humanoids)_ , 2015, pp. 690–695. 

   - [32] J. Rozlivek, A. Roncone, U. Pattacini, and M. Hoffmann, “Harmonious—human-like reactive motion control and multimodal perception for humanoid robots,” _IEEE Transactions on Robotics_ , vol. 41, pp. 378–393, 2025. 

   - [33] M. Selvaggio, A. Garg, F. Ruggiero, G. Oriolo, and B. Siciliano, “Non-prehensile object transportation via model predictive non-sliding manipulation control,” _IEEE Transactions on Control Systems Technology_ , vol. 31, no. 5, pp. 2231–2244, 2023. 

   - [34] D. F. Gomes, P. Paoletti, and S. Luo, “Generation of gelsight tactile images for sim2real learning,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 2, pp. 4177–4184, 2021. 

   - [35] Force Dimension, “Force dimension omega3,” https://www. forcedimension.com/products/omega. 

   - [36] H. Durrant-Whyte, N. Roy, and P. Abbeel, _Real-Time Prioritized Kinematic Control under Inequality Constraints for Redundant Manipulators_ . MIT Press, 2012, pp. 145–152. [Online]. Available: https://ieeexplore.ieee.org/document/6301071 

   - [37] P. Sardain and G. Bessonnet, “Forces acting on a biped robot. center of pressure-zero moment point,” _IEEE Transactions on Systems, Man, and Cybernetics - Part A: Systems and Humans_ , vol. 34, no. 5, pp. 630–637, 2004. 

- [17] Xela Robotics, “uscu & alha - tactile sensors,” https://www. xelarobotics.com/sensor-collection/uscu-alha, 2025, accessed: 202504-23. 

[18] ErgoCub team, “Project ergocub,,” https://ergocub.eu/, 2023. 

