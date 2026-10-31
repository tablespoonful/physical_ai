---
title: "Simplifying ROS2 controllers with a modular architecture for robot-agnostic reference generation"
date: "2026-01-13"
authors: "Davide Risi; Vincenzo Petrone; Antonio Langella; Lorenzo Pagliara; Enrico Ferrentino; Pasquale Chiacchio"
url: https://arxiv.org/abs/2601.08514
pdf: https://arxiv.org/pdf/2601.08514
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.08514)** / [論文ページ](https://arxiv.org/abs/2601.08514)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/RAP.2026.3732617 — IEEE ROBOTICS AND AUTOMATION PRACTICE 

1 

# Simplifying ROS2 controllers with a modular architecture for robot-agnostic reference generation 

Davide Risi, Vincenzo Petrone, _Member, IEEE,_ Antonio Langella, Lorenzo Pagliara, _Student Member, IEEE,_ Enrico Ferrentino, _Member, IEEE,_ Pasquale Chiacchio 

**_Abstract_ —This paper introduces a novel modular architecture for ROS2 that decouples the logic required to acquire, validate, and interpolate references from the control laws that track them. The design includes a dedicated component, named** **_Reference Generator_ , that receives references, in the form of either single points or trajectories, from external nodes (e.g., planners), and writes single-point references at the controller’s sampling period via the existing ros2_control chaining mechanism to downstream controllers. This separation removes duplicated referencehandling code from controllers and improves reusability across robot platforms. We implement two reference generators: one for handling joint-space references and one for Cartesian references, along with a set of new controllers (PD with gravity compensation, Cartesian pose, and admittance controllers) and validate the approach on simulated and real Universal Robots and Franka Emika manipulators. Results show that (i) references are tracked reliably in all tested scenarios, (ii) reference generators reduce duplicated reference-handling code across chained controllers to favor the construction and reuse of complex controller pipelines, and (iii) controller implementations remain focused only on control laws.** 

**_Index Terms_ —Robot Operating System, Software Tools for Robot Programming, Compliance and Impedance Control, Control Architectures and Programming, ROS2.** 

## I. INTRODUCTION 

**T** HEwhereROS2researchersframeworkand aimsindustriesto supportcan rapidlyan ecosystemset up robotic systems by reusing and composing open-source community-developed components [1]. Sharing this vision, the ros2_control framework adopts design principles such as hardware-interface abstraction and modular design promoting controller reusability across robots and applications [2], [3]. Notably, the controller chaining mechanism has been introduced to enable users to build complex behaviors from reusable components [4]. Its modular design enables interoperability among control modules developed by different actors. It also simplifies controller development by moving resource and lifecycle management out of individual controllers. 

While this design successfully decouples controllers from hardware, it is less successful in decoupling 

Authors are with the Department of Information Engineering, Electrical Engineering and Applied Mathematics (DIEM), University of Salerno, 84084 Fisciano, Italy (email: _{_ drisi, vipetrone, alangella, lpagliara, eferrentino, pchiacchio _}_ @unisa.it). 

©2026 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works. 

control logic from input processing. In contrast to the Single Responsibility Principle (SRP) [5], standard controllers like the AdmittanceController and JointTrajectoryController [6] act as monolithic entities that handle both reference processing and loop closure. This leads to code duplication and undermines reusability. In turn, it increases development time and maintenance costs, with a steeper learning curve for new developers. Potentially, this could hinder the adoption of ros2_control in educational and research contexts, e.g., when interested practitioners are specialized in control theory, but not in software engineering. 

## _A. Contributions_ 

To address the monolithic nature of current controllers, we analyze the common responsibilities that are frequently duplicated across implementations: 

- _Reference acquisition and validation._ Controllers often accept references via ROS2 topics [7] and actions [8] and verify that they are dimensionally consistent, numerically valid, and within expected limits. 

- _Real-time-safe handling._ Many controllers receive external references asynchronously but must compute a reference at the controller loop rate. This requires handling the communication between non-real-time and real-time contexts. 

- _Interpolation._ Planners typically produce waypoints at rates differing from the low-level controller frequency, necessitating internal interpolation logic. 

Decoupling those from control law calculation is possible and would make new controllers easier to implement and more reusable across different applications. 

To reach this goal, we propose a ros2_control software module called _Reference Generator_ (RG) that encapsulates all of the responsibilities cited above. RGs handle reference acquisition via standard ROS2 communication primitives and produce single-point references at the controller’s sampling period. A key design choice is to exclusively use the controller chaining mechanism as the communication interface between RGs and downstream controllers [4]. By leveraging ROS2 interfaces, this mechanism promotes cross-compatibility among modules developed by different organizations while keeping the design extensible for future needs. Consequently, new controllers developed within this framework are agnostic to how references are acquired, making the implementation 

0000–0000/00$00.00 © 2021 IEEE 

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/RAP.2026.3732617 — IEEE ROBOTICS AND AUTOMATION PRACTICE 

2 

of the control law their sole responsibility. This design also makes RGs backward-compatible with any ROS2 controller that supports chaining. 

Specifically, this paper makes the following contributions: 

- 1) We design a novel architecture that separates reference processing (acquisition, validation, and interpolation) from the control law algorithm within the ros2_control ecosystem. 

- 2) We provide two implementations for _Reference Generator_ : a _Joint-Space Reference Generator_ (JRG) and a _TaskSpace Reference Generator_ (TRG) for handling jointspace and Cartesian references, respectively. 

- 3) Additionally, we deliver a set of new controllers, to further demonstrate how our reference generators favor the creation of control chains: (i) PD with gravity compensation, (ii) Cartesian pose [9], and (iii) admittance controllers. The latter is tailored to work with Cartesian references instead of joint-space ones, differently from the original AdmittanceController proposed in ros2_controllers [6]. 

The proposed _Reference Generator_ and the new controllers are successfully demonstrated in various pipeline configurations on simulated and real Universal Robots [10] UR10 and Franka Emika Robot [11], [12] (FER) manipulators. 

## _B. Control laws_ 

Consider the robot dynamics [13]: 


where **_B_** is the inertia matrix, **_C_** collects Coriolis and centrifugal terms, **_f_** models friction, **_g_** the gravitational effects, and **_τ_** are the actuation torques. Vectors **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨ denote joint positions, velocities, and accelerations. The end-effector pose, twist and accelerations are denoted with **_x_** _,_ **_v_** _,_ **_v_** ˙ , respectively. Here we recall the control laws used in the pipelines of Section III. 

- **PD control with gravity compensation (PDGC):** 


where **_K_** _P ,_ **_K_** _D ≻_ 0 are symmetric positive-definite gain matrices, and **_q_** _d_ is the desired joint position profile [14]. 

- **PID control:** 


with integral gain matrix **_K_** _I ≻_ 0 and desired joint velocities **_q_** ˙ _d_ [15]. 

- **Admittance control (AC):** The desired relationship between the commanded and measured wrenches is defined in task space as a mass-spring-damper system acting on the task error **_x_** ˜ = **_x_** _d −_ **_x_** _c_ , with **_x_** _d_ and **_x_** _c_ denoting the desired and commanded end-effector poses, respectively: 


where **_M_** _d,_ **_K_** _D,_ **_K_** _P ≻_ 0 are diagonal positive-definite matrices specifying the desired dynamics, **_h_** _e_ is the measured external wrench, and **_h_** _d_ is the commanded 


Fig. 1. Component diagram. The _Reference Generator_ validates and interpolates incoming references, producing single, chainable references for the downstream controller. 

feedforward wrench. The vectors **_x_** ˜<sup>˙</sup> and **_x_**<sup>¨</sup> ˜ denote the first and second time derivatives of **_x_** ˜. The resulting control law providing the commanded task motion is 


whose integration yields the commanded pose **_x_** _c_ = **_x_** _d −_ **_x_** ˜ tracked by the downstream controller [16], [17]. 

- **Cartesian pose control (CPC):** 


where **_J_**<sup>_†_</sup> denotes a damped least-squares pseudoinverse of the geometric Jacobian **_J_** , and **_q_** ˙ _c_ is the resulting jointspace command [9]. When only a position controller is available, **_q_** ˙ _c_ is integrated to obtain target joint positions. 

## II. DESIGN 

This section describes the proposed architecture and its behavior. An implementation is available in our repository<sup>1</sup> . 

Fig. 1 shows the main components and their interfaces. In particular, we distinguish between two main components with complementary functionalities: the _Reference Generator_ and the _Controller_ . The former: 

- receives single-point references or trajectories from external nodes; 

- validates incoming references to ensure dimensional consistency, numerical correctness, and compliance with expected limits, and rejects invalid external references with appropriate error codes; 

- performs interpolation of references to match the controller frequency; 

- writes a single-point reference to the downstream controller via ros2_control’s chaining mechanisms. 

The latter, instead: 

- exposes a chainable controller interface according to ros2_control’s chaining mechanisms; 

- reads a preprocessed reference input from the chainable interfaces; 

- executes the control law and performs hardware-interface or downstream-controller-reference writes; 

- 1https://github.com/unisa-acg/reference-generators-demo/tree/rap 

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/RAP.2026.3732617 — IEEE ROBOTICS AND AUTOMATION PRACTICE 

3 


Fig. 2. Finite state machine of the _Reference Generator_ . 

In this novel design, controllers are responsible only for executing control laws and interacting with hardware/downstream controllers, while reference acquisition, validation, and interpolation are delegated to the RG. This separation avoids code duplication and enhances reusability within the ros2_control framework. 

The RG operates in two complementary modes: forwarding online point references received on a topic, and executing trajectories received via actions. As shown in Fig. 2, its behavior is governed by a finite state machine (FSM) with two states: ONLINE_REFERENCE and TRAJECTORY_EXECUTION. On startup, if no reference has been published on the topic yet, the RG reads the current robot state and computes an initial reference. In ONLINE_REFERENCE, the generator forwards the most recent reference retrieved from the topic at the controller’s sampling period, keeping it constant until a new message or trajectory arrives. When a trajectory is received, the FSM switches to TRAJECTORY_EXECUTION and the RG produces interpolated points at each control period according to trajectory timestamps. When the trajectory is completed, aborted, or a new reference is received from the topic, the FSM returns to ONLINE_REFERENCE. If a new trajectory arrives while another is being executed, the RG aborts the current trajectory and starts the new one, providing action feedback and result codes accordingly. Importantly, all nonreal-time processing (action/subscriber handling, parsing and validation) occurs outside the real-time controller path (thanks to the decoupling offered by the RGs), while writing to the chainable interface remains deterministic. 

## III. EXPERIMENTAL VALIDATION 

## _A. Experimental setup and results_ 

The experiments validate the design presented in Section II. In particular, across all experiments, the goal is to demonstrate three key properties of the proposed architecture: 

- 1) **Controller-agnosticity** : RGs can easily be configured to work with downstream controllers. 

- 2) **Robot-agnosticity** : the same control pipeline can be exercised on different hardware platforms and Gazebo [18] simulations. 

- 3) **Reference interpolation** : the JRG and TRG preprocess incoming references and reliably deliver single-point references at the controller’s sampling period. 

Each experiment pairs a RG with one or more downstream controllers. Since the single-point reference functionality of the RG trivially consists of forwarding the received topic reference to the downstream controller, the experiments focus on trajectory tracking via actions. The effectiveness of the 


Fig. 3. Experiments on real robots: (left) FER executing an excitation trajectory in the JRG → PDGC experiment; (center) control points defining the square Cartesian trajectory in the TRG → CPC experiment on the UR10; (right) UR10 drawing on a blackboard with the TRG → AC → CPC pipeline. 


Fig. 4. Reference (dashed) and measured (solid) joint positions on the real FER under PD control with gravity compensation. 

design and of the controller pipelines is qualitatively demonstrated through trajectory-tracking results. The following control pipelines are tested: 

- **JRG → PDGC → simulated FER.** The JRG provides **_q_** _d_ to the PDGC (2) at frequency _f_ = 1 kHz, which issues torque commands to the simulated FER. 

- **JRG → PDGC → real FER.** The same pipeline is deployed on the real FER. Fig. 3 shows the robot executing the trajectory, with tracking results reported in Fig. 4. In this experiment, the user provides joint-space waypoints at the same rate as the controller ( _f_ = 1 kHz), so the interpolation functionality of the JRG is not exercised. 

- **JRG → PID → simulated UR10.** The user provides a few sparse joint-space waypoints to the JRG via action, which interpolates them at the controller rate ( _f_ = 1 kHz) and sends them to the PID controller (3) in simulation. Tracking results are shown in Fig. 5. 

- **TRG → CPC → simulated UR10.** The user sends sparse Cartesian waypoints to the TRG via action; the TRG provides Cartesian pose setpoints to the CPC at _f_ = 1 kHz, which computes joint targets via inverse kinematics (6) and sends them to the simulated UR10. 

- **TRG → CPC → real UR10.** Similar pipeline on the real UR10, but the frequency is reduced to _f_ = 125 Hz to accommodate hardware limitations. An illustration of the trajectory waypoints given by the user is shown in Fig. 3. Tracking results (after interpolation) are in Fig. 6. 

- **TRG → AC → CPC → real UR10.** The user sends a few Cartesian waypoints to perform an interaction experiment with the real UR10, consisting of sliding a piece of 

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/RAP.2026.3732617 — IEEE ROBOTICS AND AUTOMATION PRACTICE 

4 


Fig. 5. Reference (circles) and measured (lines) joint positions on the simulated UR10 under PID control. 

chalk on a blackboard, as shown in Fig. 3. The TRG provides Cartesian setpoints at _f_ = 125 Hz, which the AC modulates according to the measured end-effector wrench, as explained in (4) and (5); the modulated setpoints are executed by the CPC on the real UR10. The actual robot behavior is shown in Fig. 7 in terms of position errors. 

- **TRG → AC → CPC → PID → simulated UR10.** A composite pipeline consisting of TRG, AC, CPC, and PID controllers is executed on the simulated UR10 in an interaction scenario. The trajectory consists of a few Cartesian waypoints for a wall-sliding motion. In this experiment, the TRG provides Cartesian setpoints at _f_ = 1 kHz, which the AC modulates according to the measured end-effector wrench; the modulated setpoints are converted to joint targets by the CPC and finally into effort commands by the PID controller before being sent to the simulated UR10. Fig. 7 shows the position error between the TRG references and the actual end-effector position over time. 

## _B. Discussion_ 

The experiments confirm the three key properties stated in Section III-A. The same implementations of the RGs were paired with different downstream controllers (PDGC, PID, CPC, AC) without modifying the code of any components. All controllers successfully received the preprocessed references and executed their control laws. Identical control pipelines were executed on both simulation and real hardware (FER and UR10) without architectural changes, demonstrating that the design separates reference generation and controller logic from robot-specific details. 

Both TRG and JRG correctly preprocessed sparse, timestamped waypoints and produced single-point references at the controller sampling period (see Fig. 5 and 6). Larger errors observed in the admittance experiments are expected, since interaction forces intentionally modulate the motion during contact, yielding compliant behavior. 

The results also confirm that multi-layer pipelines (e.g., TRG → AC → CPC → PID) can be assembled without specialized architectural design, demonstrating the framework’s flexibility and support for hierarchical control. Finally, both 


Fig. 6. Reference (circles) and measured (lines) end-effector position (left) and orientation (right) signals on the real UR10 under Cartesian pose control. 


Fig. 7. End-effector position errors on the real (left) and simulated (right) UR10 under admittance control. X and Y axes are contact directions in base frame, respectively. 

ROS2-native (PID) and new proposed controllers (PDGC, CPC, and AC) were successfully validated, confirming their compatibility with the proposed design. 

To quantify the reduction in code complexity enabled by the proposed architecture, we compare against the JointTrajectoryController<sup>2</sup> . This controller can be regarded as a monolithic coupling of a JRG with a PID control law, which is precisely the design this work proposes to separate by delegating reference management to the RGs, leaving the controllers with only control-law code. We counted approximately 905 of 1,745 source lines (52%) dedicated to reference handling features: trajectory validation, actionserver and subscriber callbacks, goal management, trajectorypoint processing, and real-time safe buffering. By following the SRP [5], the RGs are a one-time investment shared across all downstream controllers: any new controller does not need to re-implement the aforementioned features, yielding compounding savings as the number of controllers grows. 

## IV. CONCLUSIONS 

This paper presented a modular architecture for ROS2 that separates reference processing from control-law execution, realized through two RGs (JRG and TRG). The work demonstrated that this separation improves reusability, simplifies controller design, and enables modular construction of flexible control pipelines through chaining. 

The JRG and TRG were shown to be compatible not only with the custom controllers introduced in this work, but also with the ros2_control PID controller, showing that the same RGs can be used with controllers developed by the community as long as they adhere to the ros2_control’s chaining mechanisms. 

The pipelines defined in Section III were configured by only changing the parameters in the configuration file (e.g., 

> 2https://github.com/ros-controls/ros2 <u>controllers/tree/humble</u> 

5 

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/RAP.2026.3732617 — IEEE ROBOTICS AND AUTOMATION PRACTICE 

TABLE I 

DESCRIPTION OF SUPPLEMENTARY MATERIALS 

|**Material**|**Description**|
|---|---|
|Video<br>(rap-rg-video.mp4)|The video shows the three experiments executed on the real robots: 1) PDGC on the real FER; 2) CPC on the real UR10 robot;<br>3) AC _→_CPC pipeline on the real UR10 robot. The video can be viewed on YouTube at https://youtu.be/qpMYzO2Cpx8|
|Source code<br>(online)|The source code is hosted in a GitHub repository, containing the ROS2 packages implementing the reference generators<br>(JRG and TRG) described in the paper, together with documentation and launch files to use them. The readers can directly<br>access the GitHub repository at https://github.com/unisa-acg/reference-generators-demo/tree/rap.|
|UML Class Diagram<br>(rap-rg-class-diagram.png)|The Class Diagram better illustrates the main _Reference Generators_ classes (ReferenceGenerator, JointSpace<br>ReferenceGenerator, and TaskSpaceReferenceGenerator), their methods, and their relationships.|


interface names, control period, and gains), demonstrating the limited effort required for reconfiguration. In addition, the successful development of new control laws based on the same RGs shows that they provide a stable abstraction for extending and prototyping additional control strategies. 

The architecture naturally allows for extensions at the reference generation level; while linear interpolation was sufficient for our demonstrations, the modular design easily accommodates higher-order interpolation (e.g., quintic splines) strategies to implement in future works, to improve smoothness and reference fidelity without affecting downstream controllers. 

Furthermore, extending the TRG to produce velocity commands would also benefit mobile-base controllers — e.g., the DiffDriveController — by decoupling its subscriber logic and introducing trajectory-handling capabilities. 

## APPENDIX 

## DESCRIPTION OF SUPPLEMENTARY MATERIALS 

This work is supported by the supplementary materials detailed in Table I. 

## REFERENCES 

- [1] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, “Robot Operating System 2: Design, architecture, and uses in the wild,” _Science Robotics_ , vol. 7, no. 66, 2022, art. no. eabm6074. 

- [2] S. Chitta, E. Marder-Eppstein, W. Meeussen, V. Pradeep, A. R. Tsouroukdissian, J. Bohren, D. Coleman, B. Magyar, G. Raiola, M. L¨udtke, and E. F. Perdomo, “ros <u>control:</u> A generic and simple control framework for ROS,” _Journal of Open Source Software_ , vol. 2, no. 20, p. 456, 2017. [Online]. Available: https://doi.org/10.21105/joss.00456 

   - [10] Universal Robots A/S, “Universal Robots,” 2025. [Online]. Available: https://www.universal-robots.com/ 

   - [11] S. Haddadin, S. Parusel, L. Johannsmeier, S. Golz, S. Gabl, F. Walch, M. Sabaghian, C. J¨ahne, L. Hausperger, and S. Haddadin, “The Franka Emika Robot: A Reference Platform for Robotics Research and Education,” _IEEE Robotics & Automation Magazine_ , vol. 29, no. 2, pp. 46–64, Jun. 2022. 

   - [12] Franka Robotics GmbH, “Franka Robotics,” 2025. [Online]. Available: https://franka.de/products-overview 

   - [13] R. Featherstone and D. E. Orin, “Dynamics,” in _Springer Handbook of Robotics_ , 2nd ed., B. Siciliano and O. Khatib, Eds. Cham: Springer, 2016, vol. 3, pp. 195–211. [Online]. Available: https: //link.springer.com/10.1007/978-3-319-32552-1 

   - [14] R. Kelly, V. Santib´a˜nez Davila, and A. Lor´ıa, “PD Control with Gravity Compensation,” in _Control of Robot Manipulators in Joint Space_ . London: Springer London, 2005, pp. 157–169. [Online]. Available: https://doi.org/10.1007/1-85233-999-3 <u>9</u> 

   - [15] ——, “PID control,” in _Control of Robot Manipulators in Joint Space_ . London: Springer London, 2005, pp. 201–220. [Online]. Available: https://doi.org/10.1007/1-85233-999-3 <u>11</u> 

   - [16] W. S. Newman, “Stability and Performance Limits of Interaction Controllers,” _Journal of Dynamic Systems, Measurement, and Control_ , vol. 114, no. 4, pp. 563–570, 12 1992. [Online]. Available: https://doi.org/10.1115/1.2897725 

   - [17] L. Villani and J. De Schutter, “Force control,” in _Springer Handbook of Robotics_ , B. Siciliano and O. Khatib, Eds. Cham: Springer International Publishing, 2016, pp. 195–220. [Online]. Available: https://doi.org/10.1007/978-3-319-32552-1 <u>9</u> 

   - [18] N. Koenig and A. Howard, “Design and use paradigms for Gazebo, an open-source multi-robot simulator,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , ser. IROS04, vol. 3. IEEE, 2004, pp. 2149–2154. [Online]. Available: http://dx.doi.org/10.1109/iros.2004.1389727 

- [3] ros2 <u>control</u> Development Team, “ROS2 Control,” 2025. [Online]. Available: https://control.ros.org/rolling/index.html 

- [4] ——, “Controller Chaining / Cascade Control,” 2025. [Online]. Available: https://control.ros.org/rolling/doc/ros2 <u>control/</u> controller <u>manager/doc/controller chaining.html</u> 

- [5] R. C. Martin, _Clean Code: A Handbook of Agile Software Craftsmanship_ , 1st ed. USA: Prentice Hall PTR, 2008. 

- [6] ros2 <u>control</u> Development Team, “ROS2 Controllers,” 2025. [Online]. Available: https://control.ros.org/rolling/doc/ros2 <u>controllers/</u> doc/controllers <u>index.html</u> 

- [7] Open Robotics, “Understanding Topics,” 2025. [Online]. Available: https://docs.ros.org/en/rolling/Tutorials/Beginner-CLI-Tools/ Understanding-ROS2-Topics/Understanding-ROS2-Topics.html 

- [8] ——, “Understanding Actions,” 2025. [Online]. Available: https://docs.ros.org/en/rolling/Tutorials/Beginner-CLI-Tools/ Understanding-ROS2-Actions/Understanding-ROS2-Actions.html 

- [9] P. Chiacchio, S. Chiaverini, L. Sciavicco, and B. Siciliano, “Closed-Loop Inverse Kinematics Schemes for Constrained Redundant Manipulators with Task Space Augmentation and Task Priority Strategy,” _The International Journal of Robotics Research_ , vol. 10, no. 4, pp. 410–425, 1991. [Online]. Available: https://doi.org/10.1177/027836499101000409 

