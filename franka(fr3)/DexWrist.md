---
title: "DexWrist: A Robotic Wrist for Constrained and Dynamic Manipulation"
date: "2025-07-01"
authors: "Martin Peticco; Gabriella Ulloa; John Marangola; Nitish Dashora; Pulkit Agrawal"
url: https://arxiv.org/abs/2507.01008
pdf: https://arxiv.org/pdf/2507.01008
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2507.01008)** / [論文ページ](https://arxiv.org/abs/2507.01008)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED SEPTEMBER, 2026 

1 

# DexWrist: A Robotic Wrist for Constrained and Dynamic Manipulation 

Martin Peticco, Gabriella Ulloa, John Marangola, Nitish Dashora, and Pulkit Agrawal 

**_Abstract_ —Development of dexterous manipulation hardware has primarily focused on hands and grippers. However, these endeffectors are often paired with bulky and highly stiff wrists that limit performance in human environments. More recent designs have adopted backdrivable actuation, but are still difficult to model and control due to coupled kinematics or high mechanical inertia from heavy links. We present** **_DexWrist_ , a compact robotic wrist combining quasi-direct-drive actuation with a decoupled parallel kinematic mechanism to advance manipulation in highly constrained environments and enable dynamic, contact-rich tasks. It delivers 3** **_._ 75** **_±_ 0** **_._ 05 Nm rated torque, 0** **_._ 33** **_±_ 0** **_._ 06 Nm backdrive torque, 10** **_._ 15** **_±_ 1** **_._ 34 Hz torque bandwidth,** **_±_ 40**<sup>**_◦_**</sup> **ROM in both DOFs, and a diagonal velocity-constraint Jacobian (one-to-one motor-to-DOF mapping) in a 0.97 kg package. In practice, these properties increase workspace in clutter and stabilize contact without finely tuned admittance control. We evaluate** **_DexWrist_ as a drop-in upgrade in simulation and on three robot arms across constrained and contact-rich tasks. In learned policy evaluations on the AgileX PiPER and UR3e,** **_DexWrist_ achieved 50–76% relative improvements in success rate and reduced autonomous task completion times by 3–5** _×_ **; on a torque-controlled Franka FR3, where a strong joint-impedance baseline already succeeds, it still completed the task 1.4** _×_ **faster.** 

**_Index Terms_ —Dexterous manipulation, mechanism design of manipulators, telerobotics and teleoperation.** 

## I. INTRODUCTION 

**W** HILE robotic manipulation has advanced rapidly usingmachine learning and commodity hardware, current systems perform quasi-static tasks in clutter-free environments with open workspaces (e.g., empty tables and fridges), as evidenced in large-scale manipulation datasets [1]. The real world is highly cluttered, imposing workspace constraints on robots that lack the compliance and force sensing to make safe contact, risking damage to the robot and the environment. Many tasks, such as wiping and cooking, also require high speed. Furthermore, most learning-based systems rely on expensive real-world data collection, making fast demonstration speed and high reliability critical. We posit that many of these shortcomings stem from the wrists on current robots, and can be mitigated by a drop-in hardware upgrade. 

A majority of current robotic systems, such as arms by Franka [2] and Universal Robots [3], rely on parallel-jaw 

Manuscript received: April 16, 2026; Revised: July 18, 2026; Accepted: 

September 1, 2026. 

This paper was recommended for publication by Editor Clement Gosselin upon evaluation of the Associate Editor and Reviewers’ comments. 

This work was supported by ONR MURI (grant N00014-22-1-2740), Sony, and Toyota Research Institute. 

The authors are with the Improbable AI Lab, Massachusetts Institute of Technology, Cambridge, MA 02139 USA (e-mail: _{_ mpeticco, gulloa, jmgola, dashora, pulkitag _}_ @mit.edu). 

Videos and details: martinpeticco.com/dexwrist 

grippers mounted on 6- or 7-DOF arms whose wrists present several issues: (i) rigid joints with high gear reductions are slow and hard to backdrive, resulting in poor adaptation to external forces and precluding dynamic tasks [4]; (ii) the joints are often too large for cluttered spaces [5]; (iii) the joints are connected end-to-end serially, making small end-effector (EE) reorientations require large arm motions, further preventing operation in cluttered spaces [5]; and (iv) parallel designs have coupled kinematics, producing a non-diagonal constraint Jacobian that increases modeling and control complexity [6]. Together, these factors limit the speed, workspace, and contact handling of current systems. 

Humans, in contrast, can reorient their hands extensively in tight spaces because their wrist DOFs are co-located near the hand, reducing the motion needed to accomplish tasks. Human joints are also fast and tolerant of repeated contact [7]. In fact, studies have found that wrist dexterity with a simple endeffector outperforms a highly dexterous end-effector paired with a limited wrist [8]. 

We present _DexWrist_ (Fig. 1), a compact 2-DOF robotic wrist that combines a decoupled parallel kinematic mechanism (PKM) with quasi-direct-drive (QDD) actuation. The PKM co-locates two rotational DOFs about a single point, keeping the wrist small and reducing arm motions. Its diagonal velocity-constraint Jacobian gives a one-to-one motor-to-DOF mapping that reduces modeling and control complexity. QDD actuation permits low mechanical impedance, enabling fast motions and stable contact without complex admittance control. _DexWrist_ is a drop-in pitch–yaw upgrade. Throughout this paper, pitch denotes flexion/extension (F/E), yaw denotes radial/ulnar (R/U), and roll denotes pronation/supination (P/S), the last of which is typically available upstream on all 6- and 7-DOF arms. Our contributions are: 

- A compact, robust, decoupled PKM wrist design with a co-located pitch–yaw center and one-to-one motor-toDOF mapping. 

- A requirements-driven validation of torque, backdrive torque, bandwidth, speed, ROM, size, and weight. 

- A system-level evaluation demonstrating these properties carry downstream: 88% larger workspace in simulation, **1.3–2.2** _×_ faster teleoperated demonstrations on the AgileX and UR3e, and improved autonomous policy performance: **50–76%** relative increases in success rate and **3–5** _×_ faster autonomous completion on the AgileX and UR3e, and a 1.4 _×_ speedup on a torque-controlled Franka. 

The remainder of the paper covers related work (Sec. II), design and validation (Sec. III), system-level setup and results (Secs. IV–V), and discussion (Sec. VI). 

> © 2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works. 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED SEPTEMBER, 2026 

2 


Fig. 1. _DexWrist_ , a robotic wrist for constrained and dynamic manipulation. **A:** _DexWrist_ with an AgileX gripper. **B:** Learned constrained-space task: picking from a cluttered fridge. **C:** Dynamic bottle flip (pre-planned). **D:** Learned contact-rich task: wiping a whiteboard. 

## II. PRIOR WORK 

Robotic wrists group broadly by kinematic architecture and actuation strategy; we review each category and identify the gaps that motivate our design. 

Most commercially available robot arms, including the UR series [3], Franka [2], and AgileX PiPER [9], use a serial wrist with single-DOF joints connected end-to-end along the kinematic chain. The harmonic drives common in these platforms (typically 80:1–160:1 reduction) make the wrist slow and poorly suited to contact-rich tasks due to their low backdrivability [4]. Even with highly backdrivable actuators, if the joints are spaced apart (like the AgileX) rather than co-located as in the human wrist [8], small end-effector reorientations will require large arm motions in constrained spaces [5]. 

A simple approach to co-locating DOFs is a universaljoint (U-joint) arrangement. Platforms such as the Unitree H12 [10], GALAXEA R1 [11], and OpenArm [12] mount the first motor stationary in the forearm and rotate the second motor in its entirety through a linkage. This yields a one-to-one motorto-DOF mapping, but moving motor mass raises distal inertia, reducing mechanical bandwidth and limiting dynamic tasks. 

Some works address contact stability through material compliance or stiffness modulation. Milazzo et al. [13] use four motors and nonlinear elastic elements to vary stiffness up to 3 _×_ , at the cost of weight and complexity. Sun et al. [14] achieve 232 _×_ stiffness variation in a 55 mm, 200 g module, but its sheet-type flexure limits transmissible torque. Baggetta et al. [15] use cable-driven flexural pivots with wide ROM, but cables introduce friction and hysteresis. BiFlex [16] uses a passive buckling honeycomb, but provides no active reorientation and only a 500 g payload. These designs sacrifice torque capacity, active control authority, or both. 

Parallel kinematic mechanisms (PKMs) permit tighter motions by co-locating the output DOFs through linkages. In coupled designs like the Omni-Wrist [17], Carpal wrist [18], Damerla prosthetic wrist [19], and ByteWrist [20], the constraint Jacobian is non-diagonal: actuators do not map one-to- 

### TABLE I 

REPRESENTATIVE WRIST ARCHITECTURES ACROSS THE PROPERTIES NEEDED FOR COMPACT, CONTACT-RICH, DYNAMIC MANIPULATION (✓ FAVORABLE, ✗ UNFAVORABLE). A NON-ELASTIC TRANSMISSION HAS NO SERIES-ELASTIC ELEMENT OR FLEXURE, LEAVING ENDPOINT STIFFNESS TO THE CONTROLLER. THE LAST TWO COLUMNS ARE THE INERTIAL CONTRIBUTIONS TO ENDPOINT IMPEDANCE: REFLECTED ROTOR INERTIA AND DISTAL MOVING MASS. 

|||||Endpoint|impedance:|
|---|---|---|---|---|---|
|Architecture|Co-<br>located|De-<br>coupled|Non-Elastic<br>transmission|Reflected<br>inertia|Distal<br>inertia|
|Serial (UR3e, Franka) [2], [3]|✗|✓|✓|high (✗)|high (✗)|
|U-joint (OpenArm) [12], [22]|✓|✓|✓|low (✓)|high (✗)|
|Coupled PKM (ByteWrist) [20]|✓|✗|✓|low (✓)|high (✗)|
|Compliant / VS (Milazzo) [13]|✗|✗|✗|high (✗)|low (✓)|
|Decoupled PKM (Negrello) [5]|✓|✓|✗|high (✗)|low (✓)|
|**_DexWrist_ (ours)**|✓|✓|✓|low (✓)|low (✓)|


one with output DOFs, requiring multi-input coordination and preventing direct per-axis torque attribution [6]. A decoupled parallel mechanism [21] provides one-to-one motor-to-DOF mapping with co-located rotation. The Negrello wrist [5] employs one, but relies on heavily geared (350:1) actuation, making it heavier and lower-bandwidth while limiting its use for dynamic, contact-rich tasks. 

As Table I summarizes, no existing wrist simultaneously provides a compact co-located rotation center, a one-to-one motor-to-DOF mapping, low-impedance (quasi-direct-drive) actuation, and low distal inertia. _DexWrist_ achieves this by pairing a 2-(R, RR) decoupled PKM with custom quasi-directdrive actuators housed entirely in the forearm. 

## III. DEXWRIST DESIGN AND VALIDATION 

This section defines _DexWrist_ ’s mechanical and actuation requirements, the design decisions that meet them, and the experiments validating them. Table II summarizes the results. 

## _A. Functional Requirements_ 

The human wrist serves as our design reference. It provides two orientation DOFs via a condyloid/ellipsoidal joint with ap- 

PETICCO _et al._ : DEXWRIST: A ROBOTIC WRIST FOR CONSTRAINED AND DYNAMIC MANIPULATION 

3 

TABLE II 

FUNCTIONAL REQUIREMENTS AND MEASURED PERFORMANCE. SPEC DENOTES THE DESIGN TARGET DERIVED FROM THE CITED WORK. ROM SPEC DENOTES MINIMUM COVERAGE AND CAN BE EXCEEDED. 

|Requirement<sup>_‡_</sup>|Spec|Ours|Meets|
|---|---|---|---|
|Rated torque (Nm)|_≥_3 [23]|3_._75_±_0_._05|✓|
|Backdrive torque (Nm)<br>|_≤_0_._4 [23]|0_._33_±_0_._06|✓|
|Hardstop load cap. (Nm)<sup>_†_</sup><br>|_≥_9 [24]|_≥_14|✓|
|Axial load cap. (kg)<sup>_†_</sup>|_≥_15 [24]|_≥_100|✓|
|No-load speed (rpm)|_≥_53_._3 [25]|96_._6_±_9_._4|✓|
|Torque BW (Hz) @ 3.75 Nm|_≥_10 [26]|10_._15_±_1_._34|✓|
|Angular precision (deg)|_≤_3_._47 [27]<br>|1.65<br>|✓|
|F/E ROM (deg)|[_−_40<sup>_◦_</sup>_,_40<sup>_◦_</sup>] [28]<br>|[_−_40<sup>_◦_</sup>_,_40<sup>_◦_</sup>]<br>|✓|
|R/U ROM (deg)|[_−_10<sup>_◦_</sup>_,_30<sup>_◦_</sup>] [28]|[_−_40<sup>_◦_</sup>_,_40<sup>_◦_</sup>]|✓|
|Width (mm)|_≤_61_._4 [29]|64|✗|
|Height (mm)|_≤_61_._4 [29]|66.5|✗|
|Length (mm)|_≤_195_._5 [29]|178.2|✓|
|Weight (kg)|_≤_1_._0 [30]|0.97|✓|


> _†_ Load capacities are _tested-to_ values, not failure limits. _‡ DexWrist_ provides F/E and R/U; P/S is assumed upstream. 

proximately co-located axes near the hand, while a third DOF (pronation/supination) originates upstream in the forearm [8]. We use human performance data from the literature to derive the targets below. 

_1) Torque, Load Capacity, and Backdrivability:_ 93% of activities of daily living (ADL) can be completed with a torque of 3 Nm in both the R/U and F/E directions (Fig. 2) [23]. We do not target P/S torque, as most 6- and 7-DOF robot arms provide this DOF. 

For static loads at the output flange, we follow NASA hardstop guidance [24] with a 3.0 factor of safety over rated torque, giving 9 Nm at the hardstops, and target a 15 kg axial load for UR5e-class payloads. 

Low-impedance actuation lets the wrist conform to the environment while sustaining unexpected impacts. We interpret this as a 5 N maximum backdrive force [23] at 70 mm from the wrist center, i.e., _≤_ 0 _._ 35 Nm, rounded to 0.4 Nm. 

_2) Speed, Bandwidth, Range, and Precision:_ Human studies report wrist speeds of 10–53.3 RPM [25]. Conscious and involuntary reflexes span 50–100 ms, giving bandwidth frequencies of 10–20 Hz [26]. Minimum wrist angular precision is 3.47° [27]. 

ADL studies show that _±_ 40<sup>_◦_</sup> F/E and [ _−_ 10<sup>_◦_</sup> _,_ 30<sup>_◦_</sup> ] R/U allow completion of 22 of the 24 tasks [28]. We align _DexWrist_ joint coordinates such that the pitch–yaw output DOFs correspond to F/E and R/U. 

_3) Size and Weight:_ NASA anthropometric data give a 95th-percentile male wrist width and height of 61.4 mm, and a forearm length of 349 mm [29], which we shorten by 2 _._ 5 _×_ 61 _._ 4 mm to 195.5 mm to leave ample room for an elbow joint and a P/S DOF upstream, as most robot arms include this DOF. As a drop-in module, we target the _∼_ 1 kg weight of common grippers such as the Robotiq 2F series [30]. 

## _B. Wrist Design_ 

_DexWrist_ is a 2-DOF robotic wrist meeting the requirements of Sec. III-A. Two custom QDD actuators in the forearm each drive one leg of a decoupled 2-(R,RR) parallel kinematic mechanism (PKM), whose output axes intersect at a fixed wrist center with output angles _q_ 1 (yaw), _q_ 2 (pitch). Roll is assumed upstream, but can be easily added with our modular actuators. 


Fig. 2. **Left:** Human wrists have 3 DOFs: F/E, R/U, and P/S. **Middle:** _DexWrist_ provides pitch (F/E) and yaw (R/U); with the arm’s upstream roll (P/S), all three axes intersect at a point. **Right:** The UR3e’s wrist axes do not intersect at a point. 

_1) 2-(R, RR) Decoupled Parallel Kinematic Mechanism:_ 

_a) Architecture and motion:_ We implement a 2-(R,RR) spherical parallel mechanism similar to the Agile Eye [21], where ”spherical” denotes pure rotation about the fixed wrist center. Both actuators stay in the forearm rather than rotating with the output flange, reducing distal mass versus U-joint layouts and raising bandwidth. The wrist center is 48.75 mm from the output and 70 mm from the Sec. III-A load point. 

_b) Geometry selection and structural checks:_ We selected link lengths and joint offsets to satisfy the required ROM without self-collision inside the size envelope, and checked strength under four load cases: 5 kg applied along each base axis (X, Y, Z independently) and simultaneous 3 Nm actuation about both DOFs (Fig. 3). 

_c) Forward and inverse kinematics:_ The joint axes **e** 1 _, . . . ,_ **e** 5 and output axis **v** are defined in Fig. 3, in a base frame with **e** 1 = **x** ˆ (yaw axis), **e** 2 = ˆ **z** (pitch axis), and home output **v** 0 = **y** ˆ. The yaw leg rotates **e** 3 about **e** 1 by _θ_ 1, and the pitch leg rotates **e** 4 about **e** 2 by _θ_ 2. All link twists are 90<sup>_◦_</sup> except _α_ 2 = ∠( **e** 2 _,_ **e** 4) = 95<sup>_◦_</sup> ; this 5<sup>_◦_</sup> offset, _α_ ≜ _α_ 2 _−_ 90<sup>_◦_</sup> , provides clearance for the yaw axis to reach the full _±_ 40<sup>_◦_</sup> . The output orientation follows from the two loop-closure constraints **e**<sup>_⊤_</sup> 3<sup>**v**=0and</sup><sup>**e**</sup> 4<sup>_⊤_</sup><sup>**e**5=0.Writingtheoutputas</sup> _R_ = _Rx_ ( _q_ 1) _Rz_ ( _q_ 2), the yaw constraint is satisfied directly by _q_ 1 = _θ_ 1, and the pitch constraint yields the closed form (abbreviating _cx_ =cos _x_ , _sx_ =sin _x_ ): _q_ 2 = atan2( _cαsθ_ 2 _, cαcθ_ 1 _cθ_ 2 _− sαsθ_ 1) _,_ (1) with output axis **v** = ( _−_ sin _q_ 2 _,_ cos _q_ 2 cos _q_ 1 _,_ cos _q_ 2 sin _q_ 1). In the orthogonal limit _α →_ 0 this reduces to tan _q_ 2 = tan _θ_ 2 _/_ cos _q_ 1. Inverting, _θ_ 1 = _q_ 1 and _θ_ 2 solves _A_ cos _θ_ 2 + _B_ sin _θ_ 2 = _C_ with _A_ = _−_ tan _q_ 2 cos _α_ cos _q_ 1, _B_ = cos _α_ , _C_ = _−_ tan _q_ 2 sin _α_ sin _q_ 1, taking the root in _|θi| <_ _<u>π</u>_ 2<sup>.The</sup> complete derivation is on the project website, and the mapping was verified in CAD. 

_d) Decoupling and diagonal constraint Jacobian:_ We use the standard parallel-robot differential kinematics form _K_ ( _·_ ) **_θ_**<sup>˙</sup> = _J_ 0( _·_ ) **_ω_** , where **_θ_**<sup>˙</sup> = [ _θ_<sup>˙</sup> 1 _θ_<sup>˙</sup> 2]<sup>_⊤_</sup> are the actuated joint angle rates and **_ω_** is the output flange’s angular velocity. _θ_<sup>˙</sup> 1 actuates the yaw leg (R) via **e** 1, and _θ_<sup>˙</sup> 2 the pitch leg (RR) via **e** 2. The mechanism imposes two constant-angle constraints: **e**<sup>_⊤_</sup> 3<sup>**v**=cos</sup><sup>_α_3and</sup><sup>**e**</sup> 4<sup>_⊤_</sup><sup>**e**5=cos</sup><sup>_α_4,with</sup><sup>_α_3</sup><sup>_, α_4fixedby</sup> the wrist geometry. Here _α_ 3 = _α_ 4 = _π/_ 2, so **e**<sup>_⊤_</sup> 3<sup>**v**=0</sup> and **e**<sup>_⊤_</sup> 4<sup>**e**5=0.Differentiatingandusing</sup><sup>**e**˙3=</sup><sup>_θ_˙1(</sup><sup>**e**1</sup><sup>_×_</sup><sup>**e**3),</sup> 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED SEPTEMBER, 2026 

4 

**e** ˙ 4 = _θ_<sup>˙</sup> 2( **e** 2 _×_ **e** 4), **v** ˙ = **_ω_** _×_ **v** , and **e** ˙ 5 = **_ω_** _×_ **e** 5 yields: 


Since _K_ is diagonal, each constraint equation depends on only one actuated rate [21]: the velocity constraint Jacobian is decoupled. This is the one-to-one motor-to-DOF mapping in the velocity-constraint sense: each actuator appears in exactly one constraint, paired with one output-link axis, in contrast to coupled parallel wrists, whose non-diagonal constraint Jacobian requires coordinated multi-motor actuation. In projective coordinates the displacement map of this mechanism family is fully decoupled [31], though this does not extend to the velocity or torque level. The torque-level consequences are derived next. Within the restricted configuration space _Q_<sup>_′_</sup> = _{_ ( _θ_ 1 _, θ_ 2) : _|θi| <_ _<u>π</u>_ 2<sup>_}_setbythemechanicaljoint</sup> limits, **e** 1 _×_ **e** 3 is nonzero by construction and cannot be orthogonal to **v** , and the rotational constraint on _θ_ 2 keeps **e**<sup>_⊤_</sup> 5<sup>(</sup><sup>**e**2</sup><sup>_×_</sup><sup>**e**4)</sup><sup>_̸_=0,sodet(</sup><sup>_K_)=</sup><sup>_K_11</sup><sup>_K_22</sup> _̸_<sup>=0on</sup><sup>_Q′_.Over</sup> the mechanical range _|θi| ≤_ 40<sup>_◦_</sup> the mechanism also stays far from degeneracy: _∂q_ 2 _/∂θ_ 2 _≥_ 0 _._ 98 and the output Jacobian’s condition number never exceeds 1.7. The same bound gives existence and uniqueness of the inverse-kinematics root, since _q_ 2 is strictly monotone in _θ_ 2. 

_e) Statics and torque attribution:_ By virtual work, an external moment **m** reflects onto the actuators as **_τ_** = _J_<sup>_⊤_</sup> **m** , where _J_ is the output Jacobian ( **_ω_** = _J_ **_θ_**<sup>˙</sup> , with _J_ 0 _J_ = _K_ ). Because _q_ 1 = _θ_ 1 exactly while _q_ 2 depends on both actuator angles, _J_<sup>_⊤_</sup> is upper triangular in ( _M_ 1 _, M_ 2): 


where _M_ 1 = **m** _·_ **e** 1 and _M_ 2 = **m** _·_ **u** are the moment components about the yaw and pitch output axes ( **u** = _Rx_ ( _θ_ 1)ˆ **z** = **e** 3). The remaining component is reacted by the structure. A yaw moment never reaches the pitch actuator at any configuration, while a pitch moment reflects onto the yaw actuator in the ratio ( _∂q_ 2 _/∂θ_ 1) _/_ ( _∂q_ 2 _/∂θ_ 2): zero on _θ_ 2 = 0, at most 6% along _θ_ 1 = 0 where only the 5<sup>_◦_</sup> twist contributes, growing from 15% at (20<sup>_◦_</sup> _,_ 20<sup>_◦_</sup> ) to 31% at (30<sup>_◦_</sup> _,_ 30<sup>_◦_</sup> ) and 50% at the (40<sup>_◦_</sup> _,_ 40<sup>_◦_</sup> ) motor corner. Setting _α_ = 0 still leaves 25% at (30<sup>_◦_</sup> _,_ 30<sup>_◦_</sup> ), so the coupling is driven by the yaw deflection, not the twist. As a closed form of the kinematics, (2) can be compensated exactly. We verified (2) on a bench rig by quasistatically loading each output axis in turn with known masses and reading the opposite actuator over a 2-D pose grid: the yaw-loaded pitch torque is zero as predicted (2 _._ 2 percentage points RMS, at the fixture noise floor), the pitch-loaded yaw torque matches the predicted coupling in sign and _θ_ 2-parity at every pose (0 _._ 96 _×_ aggregate), and the worst residual is 0 _._ 044 N _·_ m, 1 _._ 2% of rated torque and 7 _._ 5 _×_ below the backdrive friction that remains the practical limit on torque attribution (protocol and data on the website). 

_2) Quasi-Direct-Drive Actuator Modules:_ Quasi-directdrive (QDD) actuation [4] meets our torque, speed, backdrivetorque, and bandwidth requirements: a high-torque-density motor with a low-ratio transmission reduces friction/hysteresis and reflected motor inertia, enabling high-bandwidth torque 


Fig. 3. The 2-(R, RR) decoupled PKM. **Left:** Embodiment. The actuated axes **e** 1 _,_ **e** 2 (red) are forearm-fixed; the yaw (R, gray) and pitch (RR, blue) legs connect them to the output link (green). All joint axes intersect at the wrist center. **Right:** Kinematic schematic in the base frame ( _x ∥_ **e** 1, _z ∥_ **e** 2, _y ∥_ **v** 0), deflected at ( _θ_ 1 _, θ_ 2) = (22<sup>_◦_</sup> _,_ 25<sup>_◦_</sup> ). Gray cylinders mark the passive bearings on **e** 3 _,_ **e** 4 _,_ **e** 5; **v** 0 (dashed) is the home output axis. The shaded triangle is the rigid output link, with **e** 3, **e** 5, and **v** mutually fixed. Arcs denote 90<sup>_◦_</sup> except the 95<sup>_◦_</sup> between **e** 2 and **e** 4. 


Fig. 4. Our custom 13:1 quasi-direct-drive (QDD) actuator. 

control and far lower commanded stiffness through the PD gains than in the high-reduction harmonic-drive wrists of commodity arms (e.g., Franka and UR). 

The actuators use a CubeMars GL40 brushless DC gimbal motor paired with a custom single-stage compound planetary gearbox (Fig. 4), since commercial gearboxes did not meet our packaging requirements. A low ratio of 13:1 multiplies the motor rated torque ( _∼_ 0.25 Nm) past the 3 Nm-class joint target. Reflected rotor inertia is _J_ ref = _N_<sup>2</sup> _Jm_ , and using GL40 inertia ( _Jm_ = 74 g cm<sup>2</sup> ) and a worst-case payload inertia ( _JL ≈ mr_<sup>2</sup> with _m_ = 5 kg at _r_ = 70 mm), we obtain _J_ ref _/JL ≈_ 5 _×_ 10<sup>_−_2</sup> _≪_ 1, consistent with QDD-style lowimpedance actuation [4]. Gear tooth bending stress is checked with the Lewis equation (including dynamic factors) using 1045-steel gears, targeting _≥_ 3 factor of safety. 

An AS5047P encoder measures motor position; a moteusn1 controller, mounted in the actuator and daisy-chained over CAN at 16 V, runs a 1 kHz torque/current loop. 

## _C. Mechanical Validation_ 

Experiments were performed to validate the functional requirements in Table II. Results are in this table as well. 

_1) Output Torque, Bandwidth, and Backdrive Torque:_ We measured torque with a Vernier Go force sensor at 70 mm from the wrist center, past the PKM rather than at the actuator: continuous 60 s measurements gave 3.75 Nm on both axes. Rigidly fixing the flange and converting the 10–90% torque rise time by the first-order relation _B_ = 0 _._ 35 _/tr_ gives 10.15 Hz. Backdrive torque with PD gains set to 0 and no feedforward torque is 0.33 Nm. 

_2) Structural Load Capacity:_ Rigidly mounted to an 8020 testbed, we loaded the output flange (48.75 mm from the wrist center) directly with a crane scale and ratchet straps: axial 

5 

PETICCO _et al._ : DEXWRIST: A ROBOTIC WRIST FOR CONSTRAINED AND DYNAMIC MANIPULATION 

loading reached 100 kg in both directions, and converting output force to torque about the wrist center gave 14 Nm in both directions about both axes at the hardstops. These are tested-to values, not failure limits. 

_3) Speed, Angular Precision, and Range of Motion:_ Tracking the flange from center to both endstops with Vernier Video Analysis gave a maximum of 96.6 RPM per axis and a 1.65<sup>_◦_</sup> SD of start/end position differences over 10 trials. ROM was [ _−_ 40<sup>_◦_</sup> _,_ 40<sup>_◦_</sup> ] in pitch–yaw. 

_4) Size and Weight: DexWrist_ ’s length is 178.2 mm, meeting the requirement. Width and height (64 mm and 66.5 mm, set by the driving links) exceed the 61.4 mm target by only 4% and 8%, respectively. The assembly weighs 0.97 kg, below our 1.0 kg target mass. 

## IV. SYSTEM-LEVEL EVALUATION 

We evaluate how _DexWrist_ ’s mechanical properties (Sec. III) translate to system-level gains through three experiments: a simulated workspace comparison, a teleoperated user study, and autonomous task completion on two representative tasks. The latter two use behavior cloning (BC). A human teleoperates the robot to perform a task, and each successful example becomes a _demonstration_ : per-timestep _observations_ (RGB image and proprioceptive state) paired with the operator’s commanded _actions_ . From a dataset of demonstrations we train a _policy πθ_ ( _at_ : _t_ + _c | ot−k_ : _t_ ) via supervised learning to model a distribution over action chunks given a history of observations, with performance measured by success rate and task completion time. 

## _A. System Integration_ 

We tested _DexWrist_ on two primary platforms, each stressing one design property: (i) the AgileX PiPER, whose spacedapart serial wrist joints limit constrained-space kinematics (testing the PKM), and (ii) the UR3e, whose stiff harmonic drives limit contact-rich manipulation (testing the QDD actuation). For the wiping task we additionally test on the Franka FR3, whose joint-torque sensing supports high-quality jointimpedance control, to isolate the wrist’s contribution from the low-level controller. All platforms use the AgileX PiPER parallel-jaw (ALOHA-style) gripper. 

_1) Manipulation in Constrained Spaces:_ We study how _DexWrist_ ’s co-located DOFs and small size affect manipulation in constrained spaces. 

- **AgileX + stock wrist** : Uses backdrivable QDD actuators for contact-rich tasks, but its wrist joints are not colocated, complicating reorientation in tight spaces. 

- **AgileX + DexWrist** : We replace the AgileX’s last two joints with _DexWrist_ , maintaining 6-DOF. 

_2) Dynamic and Contact-Rich Manipulation:_ We study how _DexWrist_ ’s QDD actuation and one-to-one mapping affect proprioception, speed, and simple compliant control. 

- **UR3e + stock wrist** : Uses stiff, high-reduction harmonic drives that fault the robot upon rigid contact in position control. A closed-loop Cartesian admittance controller [32] allows contact by adjusting motor commands from sensed force, but restricts us to EE pose commands, as the UR3e’s only F-T sensor is at the EE. 

TABLE III 

SENSING AND ACTION INTERFACES FOR EACH SETUP (EE = END-EFFECTOR). EACH COLUMN COVERS THE ARM’S STOCK-WRIST AND _DexWrist_ ; WHERE THEY DIFFER, CELLS LIST STOCK / _DexWrist_ . 

||AgileX|UR3e|Franka|
|---|---|---|---|
|**Controller**|SpaceMouse|Lead–follow|Lead–follow|
|**Camera**|Intel D405|OAK-1 W|RealSense D435|
|**Obs**|Wrist RGB<br>+ EE Pose|Overhead RGB<br>+ Joint Pos.|RGB<br>+ Joint Pos.|
|**Action**|EE Pose|EE Pose /<br>Joint Pos.|Joint Pos.|


Fig. 5. Teleoperation tasks, from left to right: picking from a cluttered fridge, cable unplugging, picking from a deep drawer, and wiping a whiteboard on the UR3e and on the Franka. The fridge and wiping tasks also serve as the BC testbeds (constrained and dynamic+contact-rich, respectively). 

- **UR3e + DexWrist** : We lock the UR3e’s Wrist1 and Wrist2 joints and attach _DexWrist_ at the end of the chain to maintain 6-DOF. Its backdrivable, low-inertia actuation supports joint position control without faulting the robot, while allowing stiffness modulation. 

- **Franka + stock wrist** : A torque-controlled arm under a joint-impedance controller, among the best generalpurpose compliant control on commercial arms. 

- **Franka + DexWrist** : We lock the Franka’s J5 and J6 joints and attach _DexWrist_ , keeping the same jointimpedance controller and joint-space action so only the wrist hardware differs between the conditions. 

Observation and teleoperation interfaces for demonstration collection and policy learning are summarized in Table III. The UR3e’s leader arm is a second UR3e, and the Franka’s is a GELLO [33]. We keep end-effector actions on the AgileX and joint-position actions on the UR3e + _DexWrist_ to test whether _DexWrist_ ’s benefits hold across both action representations. On the stock UR3e, the Cartesian admittance controller needed for wiping requires EE actions. AgileX policies run at 30 Hz (200 Hz low-level) and UR3e policies at 50 Hz (500 Hz). Inverse kinematics (IK) converts between EE pose and joint space as needed. 

## _B. Experiments_ 

_1) Workspace Comparison:_ We quantify the workspace benefit of _DexWrist_ ’s co-located pitch–yaw center by comparing the AgileX PiPER with its stock wrist and with _DexWrist_ in a simulated confined-space task. In a PyBullet environment with a deep cabinet model, we sample target points uniformly inside the volume and solve IK for a fixed end-effector orientation from a fixed nominal start configuration. A point is reachable if a collision-free IK solution exists at the goal pose 

6 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED SEPTEMBER, 2026 


Fig. 6. **Left:** Serial wrist baseline (AgileX). **Middle:** _DexWrist_ . **Right:** Workspace comparison by reaching through the narrow opening of a kitchen cabinet, with _DexWrist_ achieving an 88% improvement over the AgileX. 

(checking self- and cabinet collisions). We do not collisioncheck a full motion trajectory. 

_2) Teleoperated Task User Study:_ Collecting numerous high-quality demonstrations quickly is critical to training highperforming policies. Under BC, errors accumulate as _O_ ( _ϵT_<sup>2</sup> ) (worst case) for trajectories with _T_ time steps [34], where _ϵ_ is the per-step error rate, so shorter demonstrations tighten the worst-case compounding bound. Through a user study covering four real-world, confined and contact-rich tasks (Fig. 5), we record task completion time, environment resets, and total operator time, collecting at least 35 demos per setup (100+ for the two policy-learning tasks), more than 500 in total. For the wiping task, we record the same measurements on both Franka conditions under a strong impedance-control baseline. 

- **Picking From a Cluttered Fridge (AgileX)** : Pick a highly occluded can without disturbing its surroundings. 

- **Whiteboard Wiping (UR3e, Franka)** : Wipe scribbles and dots off a whiteboard. 

- **Cable Unplugging (AgileX)** : Unplug a cable through the narrow gap between a monitor and a computer. 

- **Picking From a Drawer (AgileX)** : Pick up a cup from deep inside a drawer. 

_3) Autonomous Task Completion using Behavior Cloning:_ We train diffusion policies [35] on the fridge task (constrained, AgileX) and the wiping task (contact-rich, UR3e) to test whether _DexWrist_ ’s design benefits translate to gains in realworld autonomous performance. For each of the four configurations, we evaluated policies at six training checkpoints (epochs 75, 150, 225, 300, 375, 750). Success rates plateaued across these checkpoints rather than degrading. Because offline validation loss poorly predicts closed-loop success, we select and report the best-performing checkpoint by closedloop rollout, following standard practice [35], [36]. The same checkpoint grid and selection rule apply to every configuration. Initial object poses and task parameters (e.g., scribble location and size, object placement) are randomized every reset. We formally define the autonomous tasks below. 

_a)_ **_Constrained Pick-and-Place (AgileX)_** _:_ The task is to retrieve an occluded, flattened soda can from deep within a cluttered refrigerator and place it on the table. Failure occurs if any object is knocked over, the camera disconnects, or the refrigerator is displaced. The can sits directly beneath a shelf, so there is no top-down access: the end-effector must bend sharply and compactly to one side to reach it. Object poses are randomized every reset, with greater variation for the target. 

We use the same control method on both robots: each policy predicts a chunk of 16 consecutive actions ˆ **a** _t_ : _t_ +15, where each 


Fig. 7. Durations of successful demonstrations. _DexWrist_ reduces durations across constrained and dynamic tasks; the two whiteboard-erase groups compare the same task on the stiff UR3e and the torque-controlled Franka. Error bars: SEM. Lower is better. 

10D action **a** ˆ _k_ = [<sup>_B_</sup> **r**<sup>_TCP_</sup> _k_ ;<sup>_B_</sup> _R_<sup>_TCP_</sup> _k_ ; _gk_ ] _∈_ R<sup>3</sup> _×_ R<sup>6</sup> _× {−_ 1 _,_ 0 _,_ 1 _}_ stacks a target end-effector position in the robot base frame, a continuous 6D rotation [37], and a discrete gripper command. The first 8 actions are executed before re-planning; pose targets stream at 30 Hz to a 200 Hz low-level joint controller. 

_b)_ **_Dynamic Wiping_** _:_ The robot wipes scribbles of various sizes and shapes, and dots 2–6 cm in diameter, drawn at random locations on a whiteboard. Success is erasing more than 50% of a scribble. A failure occurs if an emergency stop triggers. We run the same task on the Franka FR3 to compare _DexWrist_ against a strong compliant-control baseline. 

The stock-wrist policy predicts end-effector pose targets tracked by the Cartesian admittance controller (Sec. IV-A); the _DexWrist_ policy outputs joint position targets (Table III). Both policies condition on 2 steps of history and predict a 96-action horizon, executing the first 32 before re-planning. 

## V. RESULTS 

## _A. Workspace Comparison_ 

Collision-free reachable targets increase by 88% with _DexWrist_ relative to the stock AgileX wrist (Fig. 6). The stock wrist fails primarily at targets deep in the cabinet and near its walls, where the serial joint layout forces the arm into self- or cabinet collisions to reach the required orientation. 

## _B. Teleoperation User Study Results_ 

As shown in Fig. 7, _DexWrist_ reduced the average duration of successful trajectories by 1.3–2.2 _×_ relative to the stock AgileX and UR3e arms. It also cut collection effort on those tasks, requiring 39.0–69.3% less operator time and fewer resets (Table IV). On the Franka wiping comparison, where the strong baseline leaves less to improve, the reductions are smaller, with demonstrations 1.2 _×_ shorter. 

## _C. Autonomous Task Results_ 

**Constrained Pick-and-Place (AgileX):** The bestperforming policy trained for AgileX + _DexWrist_ achieved a 50% relative improvement in success rate over the policy trained for the default AgileX. Qualitatively, the policy trained for the stock wrist was observed to violently disrupt the environment more frequently (e.g., displacing the fridge, knocking shelves out). On average, the AgileX + _DexWrist_ completed the task **3.24** _×_ faster than the stock system. 

**Dynamic Wiping (UR3e, Franka):** We evaluate wiping on two arms at opposite ends of the actuation spectrum. 

PETICCO _et al._ : DEXWRIST: A ROBOTIC WRIST FOR CONSTRAINED AND DYNAMIC MANIPULATION 

7 

TABLE IV 

_DexWrist_ DECREASES TOTAL OPERATOR TIME (INCLUDING RESETS AND FAILED ATTEMPTS) AND THE RESETS NEEDED TO OBTAIN SUCCESSFUL DEMONSTRATIONS. RESETS FOLLOW A SEVERE COLLISION, A KNOCKED-OVER OBJECT, OR A FAILED GRASP. 

|**Metric (Mean)**|**Task**|**Base Robot**|**w/** **_DexWrist_ (ours)**|
|---|---|---|---|
||Fridge|63.5|**38.7**|
||Cable|76.3|**28.0**|
|Operator Time (s)|Drawer|57.2|**29.6**|
||Wipe (UR3e)|21.5|**6.6**|
||Wipe (Franka)|24.2|**22.4**|
||Fridge|1.7|**1.0**|
||Cable|0.6|**0.4**|
|Operator Resets|Drawer|0.6|**0.3**|
||Wipe (UR3e)|0.2|**0.0**|
||Wipe (Franka)|0.2|**0.0**|


Fig. 8. Comparison of policy success rates across baseline arms and their _DexWrist_ versions. _DexWrist_ substantially improves success on the UR3e and AgileX; on the Franka, whose strong joint-impedance baseline already succeeds, it matches the baseline. Error bars: SEM, with at least 15 trials each (Table V). Higher is better. 

On the stiff, harmonic-drive UR3e, the UR3e + _DexWrist_ achieved a 76% relative improvement in success rate over the stock UR3e (Fig. 8) and completed the task **4.92** _×_ faster (Table V); the baseline often failed to erase even half of a scribble, while the UR3e + _DexWrist_ consistently erased nearly all of it. To confirm this gap is not an artifact of the stock UR3e’s admittance controller, a separate teleoperated study on a dot-wiping variant ( _n_ =42 trials per condition) verified that our controller performs comparably to UR’s native force-mode controller (completion time _p_ = 0 _._ 70, success _p_ = 0 _._ 78; details on the project website). On the Franka FR3, whose high-quality joint-impedance controller already succeeds, adding _DexWrist_ left success statistically unchanged (stock 19/20, _DexWrist_ 20/20); with success saturated for both conditions, the informative metric is completion time, where _DexWrist_ was **1.43** _×_ faster with the same controller and action space (one-sided Mann–Whitney _p ≈_ 9 _×_ 10<sup>_−_5</sup> ). 

## VI. DISCUSSION 

_DexWrist_ ’s novel combination of quasi-direct-drive actuation and a decoupled parallel kinematic mechanism addresses many shortcomings of current wrist designs. The design was validated in Sec. III, and co-location produced an 88% workspace increase in simulation. 

At the system level, these properties translate to more efficient teleoperation. _DexWrist_ reduced data collection time by 39.0–69.3% on the AgileX and UR3e tasks while reducing 

TABLE V 

AUTONOMOUS TASK COMPLETION TIME STATISTICS FOR SUCCESSFUL TRIALS AT EACH SYSTEM’S BEST CHECKPOINT (AT LEAST _N_ = 15 PER SYSTEM). _DexWrist_ SUBSTANTIALLY INCREASES COMPLETION SPEED. 

|**System**|**Policy T**|**ask Co**|**mpletion **|**Time (s)**|
|---|---|---|---|---|
||Mean _±_|SD|Min|Max|
|AgileX + stock wrist|91.0 _±_|7.9|55.2|134.2|
|AgileX +**DexWrist (Ours)**|**28.1** _±_|**2.2**|**20.5**|**49.0**|
|UR3e + stock wrist|21.2 _±_|10.5|12.7|40.6|
|UR3e +**DexWrist (Ours)**|**4.3** _±_|**1.2**|**1.9**|**6.5**|
|Franka + stock wrist|6.1 _±_|1.4|4.3|9.0|
|Franka +**DexWrist (Ours)**|**4.3** _±_|**1.3**|**2.9**|**7.8**|


resets, with 1.3–2.2 _×_ shorter demonstrations. We attribute these results to _DexWrist_ ’s (1) co-located DOFs reorienting the end-effector by moving only the short distal links, requiring less arm articulation in confined spaces; (2) task workspace staying far from the near-singular configurations where small end-effector adjustments demand large joint velocities; and (3) quasi-direct-drive actuation stabilizing contact without an admittance controller. Lower operator time and reset count yield more data per unit time, and shorter demonstrations tighten the compounding-error bound (Sec. IV-B2); both carried over to policy performance. 

Under diffusion-policy evaluation, these mechanisms produced the 50–76% success-rate and 3–5 _×_ completion-time gains on the AgileX and UR3e. In the constrained pick-andplace task, _DexWrist_ reorients the gripper inside the fridge by moving only the distal, co-located pitch/yaw links, requiring little motion from the arm. The stock wrist, whose final two DOFs sit further upstream, must instead articulate the whole arm, bringing its links closer to surrounding objects and increasing the chance of collisions. The learned policy imitates these more compact demonstrations and contacts objects less often, consistent with the lower teleoperation reset counts (Table IV). The AgileX’s kinematic chain also passes through a near-singular configuration as it enters the fridge, where IK becomes poorly conditioned and unreliable. The autonomous speedup exceeds the 1.3–2.2 _×_ demonstrationlength ratio because recovery behavior inflates the baseline’s rollout times (Table V). 

In the wiping task, the stock UR3e’s stiff harmonic drives resisted backdriving, producing contact forces beyond what the F-T sensor and admittance controller could absorb and sometimes faulting the robot even on its least restrictive safety settings. At contact, peak force scales with the endpoint mechanical impedance and approach speed ( _F ∼ Zv_ ), and the reflected rotor inertia that dominates _Z_ scales as _N_<sup>2</sup> _Jm_ : between our 13:1 reduction and the 80–160:1 of harmonic drives, this factor alone is 40–150 _×_ , so _DexWrist_ bounds contact force passively, before any control loop can react. Because the backdrivable joints are PD-controlled, contact also produces a steady-state tracking error _e ≈ τ_ ext _/Kp_ on the pitch axis (an observable contact signal in the policy’s joint-position inputs, where a stiff harmonic joint deflects negligibly), which may have allowed the policy to learn when to wipe. This benefit is largest where the arm’s own contact capability is weakest: on the stiff, force-sensing-limited UR3e, 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED SEPTEMBER, 2026 

8 

_DexWrist_ yields large success and speed gains, whereas on the torque-controlled Franka it preserves success and still improves speed with the same controller in both conditions, isolating the improvement to the wrist hardware rather than the control loop. Across both tasks, we hypothesize that shorter demonstrations, compact motions from co-located DOFs, and transparent proprioception from decoupled QDD actuation make expert behavior more learnable through BC. 

## VII. LIMITATIONS AND FUTURE WORK 

Being a parallel wrist, _DexWrist_ is mechanically more complex than a serial wrist. Its parallel linkages also introduce some backlash, making it better suited to contact-rich manipulation than high-precision positioning. The decoupled mapping gives no load sharing, so each actuator must be sized for its axis’s full torque. The decoupling holds exactly at the velocity-constraint level (Sec. III-B1); at the torque level, a pitch moment reflects onto the yaw actuator by the closed-form ratio in (2), reaching 50% at the corners, and the measured unmodelled residual is 1 _._ 2% of rated torque under quasi-static loading, leaving dynamic cross-axis coupling to future work. The _±_ 40<sup>_◦_</sup> range of motion per axis meets the ADL targets we adopt (Sec. III-A) but not the full human wrist flexionextension range. Width and height exceed the target by 4% and 8%, respectively. A cover over the linkages and a cable management solution would add polish to the design. 

Future work includes adding the roll (P/S) DOF, switching to frameless BLDC motors for higher torque and lower inertia, exploring reinforcement learning via torque control, and studying human demonstration transfer given _DexWrist_ ’s kinematic similarity to the human wrist. 

## ACKNOWLEDGMENTS 

We thank the members of the Improbable AI lab, especially Nolan Fey and Branden Romero, for the helpful discussions and feedback on the paper. We are grateful to MIT Supercloud and the Lincoln Laboratory Supercomputing Center for providing HPC resources. We acknowledge AgileX for providing us a custom version of their PiPER firmware. 

## REFERENCES 

- [1] OX-Embodiment Collab., “Open X-Embodiment: Robotic learning datasets and RT-X models,” _arXiv preprint arXiv:2310.08864_ , 2023. 

- [2] “Franka Emika Panda robot - RoboDK.” [Online]. Available: https://robodk.com/robot/Franka/Emika-Panda 

- [3] Universal Robots, “Collaborative Robots from Universal Robots.” [Online]. Available: https://www.universal-robots.com/products/ 

- [4] P. M. Wensing, _et al._ , “Proprioceptive actuator design in the MIT Cheetah: Impact mitigation and high-bandwidth physical interaction for dynamic legged robots,” _IEEE Trans. Robot._ , vol. 33, no. 3, pp. 509–522, 2017. 

- [5] F. Negrello, _et al._ , “A Compact Soft Articulated Parallel Wrist for Grasping in Narrow Spaces,” _IEEE Robot. Autom. Lett._ , vol. 4, no. 4, pp. 3161–3168, 2019. 

- [6] N. M. Bajaj and A. M. Dollar, “Kinematic optimization of a 2-dof u, 2pss parallel wrist device,” in _Proc. ASME Int. Design Eng. Tech. Conf. (IDETC-CIE)_ , vol. 5A, 2019, p. V05AT07A027. 

- [7] T. Petriˇc, _et al._ , “Hammering does not fit Fitts’ law,” _Front. Comput. Neurosci._ , vol. 11, p. 45, 2017. 

- [8] N. M. Bajaj, _et al._ , “State of the Art in Artificial Wrists: A Review of Prosthetic and Robotic Wrist Design,” _IEEE Trans. Robot._ , vol. 35, no. 1, pp. 261–277, 2019. 

- [9] “PiPER.” [Online]. Available: https://global.agilex.ai/products/piper 

- [10] Unitree Robotics, “Unitree H1-2 Full-size Universal Humanoid Robot,” 2024. [Online]. Available: https://www.unitree.com/h1 

- [11] Galaxea Dynamics, “Galaxea R1 Hardware Guide,” 2024. [Online]. Available: https://docs.galaxea-ai.com/Guide/R1/Hardware <u>Guide/</u> 

- [12] Enactic, Inc., “OpenArm: A fully open-source humanoid arm for physical AI research,” 2024. [Online]. Available: https://openarm.dev/ 

- [13] G. Milazzo, _et al._ , “Modeling and control of a novel variable stiffness three dofs wrist,” _Int. J. Robot. Res._ , vol. 43, no. 12, pp. 1898–1915, 2024. 

- [14] H. Sun, _et al._ , “Compact modular robotic wrist with variable stiffness capability,” _IEEE Trans. Robot._ , vol. 41, pp. 141–158, 2025. 

- [15] M. Baggetta, _et al._ , “Virtual and physical prototyping of a cable-driven compliant robotic wrist,” _IEEE/ASME Trans. Mechatron._ , vol. 30, no. 5, pp. 4000–4010, 2025. 

- [16] G.-C. Jeong, _et al._ , “BiFlex: A passive bimodal stiffness flexible wrist for manipulation in unstructured environments,” _IEEE Robot. Autom. Lett._ , vol. 10, no. 10, pp. 10 783–10 790, 2025. 

- [17] J. Sofka, _et al._ , “Omni-Wrist III - a new generation of pointing devices. Part II. Gimbals systems - control,” _IEEE Trans. Aerosp. Electron. Syst._ , vol. 42, no. 2, pp. 726–734, 2006. 

- [18] J. B. R. Alvarez, _et al._ , “Design and Development of a Carpal Wrist Robotic Manipulator,” in _Proc. IEEE Int. Conf. Humanoid, Nanotechnol., Inf. Technol., Commun. Control, Environ., Manag. (HNICEM)_ , 2019, pp. 1–5. 

- [19] R. Damerla, _et al._ , “Design and Testing of a Novel, High-Performance Two DoF Prosthetic Wrist,” _IEEE Trans. Med. Robot. Bionics_ , vol. 4, no. 2, pp. 502–519, 2022. 

- [20] J. Tian, _et al._ , “ByteWrist: A parallel robotic wrist enabling flexible and anthropomorphic motion for confined spaces,” _arXiv preprint arXiv:2509.18084_ , 2025. 

- [21] F. Caron, “Analyse et conception d’un manipulateur parall`ele sph´erique `a deux degr´es de libert´e pour l’orientation d’une cam´era,” Master’s thesis, Laval University, Quebec, Canada, 1997. 

- [22] Shenzhen Damiao Technology Co., Ltd., “DM-J4310-2EC V1.1 Gear Motor User Manual,” 2023. [Online]. Available: https://files.seeedstudio. com/products/Damiao/DM-J4310-en.pdf 

- [23] A. Pando and S. Charles, “Characterization of wrist kinetics during activities of daily living,” _J. Undergrad. Res._ , vol. 2013, no. 1, 2013, art. no. 1966. 

- [24] _NASA-STD-5017B: Design and Development Requirements for Mechanisms_ , National Aeronautics and Space Administration (NASA) NASA Standard NASA-STD-5017B, 2022. 

- [25] L. Vaisman, _et al._ , “A Comparative Analysis of Speed Profile Models for Wrist Pointing Movements,” _IEEE Trans. Neural Syst. Rehabil. Eng._ , vol. 21, no. 5, pp. 756–766, 2013. 

- [26] C. J. Forgaard, _et al._ , “Voluntary reaction time and long-latency reflex modulation,” _J. Neurophysiol._ , vol. 114, no. 6, pp. 3386–3399, 2015. 

- [27] M. E. Holman, _et al._ , “Accuracy and precision of a wrist movement when vibrotactile prompts inform movement speed,” _Somatosens. Mot. Res._ , vol. 37, no. 3, pp. 165–171, 2020. 

- [28] J. Ryu, _et al._ , “Functional ranges of motion of the wrist joint,” _J. Hand Surg._ , vol. 16, no. 3, pp. 409–419, 1991. 

- [29] “ANTHROPOMETRY AND BIOMECHANICS.” [Online]. Available: https://msis.jsc.nasa.gov/sections/section03.htm 

- [30] “2F-85 and 2F-140 Robot Grippers from Robotiq _|_ Electromate Inc.” [Online]. Available: https://www.electromate.com/ 2f-85-and-2f-140-grippers/ 

- [31] C.-H. Kuo, _et al._ , “A non-overconstrained variant of the Agile Eye with a special decoupled kinematics,” _Robotica_ , vol. 32, pp. 889–905, 2014. 

- [32] C. Ott, _et al._ , “Unified impedance and admittance control,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2010, pp. 554–561. 

- [33] P. Wu, _et al._ , “GELLO: A general, low-cost, and intuitive teleoperation framework for robot manipulators,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , 2024. 

- [34] S. Ross, _et al._ , “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proc. Int. Conf. Artif. Intell. Stat. (AISTATS)_ , 2011, pp. 627–635. 

- [35] C. Chi, _et al._ , “Diffusion policy: Visuomotor policy learning via action diffusion,” _Int. J. Robot. Res._ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

- [36] A. Mandlekar, _et al._ , “What matters in learning from offline human demonstrations for robot manipulation,” in _Proc. Conf. Robot Learn. (CoRL)_ , 2021. 

- [37] Y. Zhou, _et al._ , “On the continuity of rotation representations in neural networks,” _arXiv preprint arXiv:1812.07035_ , 2020. 

