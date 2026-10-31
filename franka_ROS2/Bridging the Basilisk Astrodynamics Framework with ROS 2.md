---
title: "Bridging the Basilisk Astrodynamics Framework with ROS 2 for Modular Spacecraft Simulation and Hardware Integration"
date: "2025-12-10"
authors: "Elias Krantz; Ngai Nam Chan; Gunnar Tibert; Huina Mao; Christer Fuglesang"
url: https://arxiv.org/abs/2512.09833
pdf: https://arxiv.org/pdf/2512.09833
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.09833)** / [論文ページ](https://arxiv.org/abs/2512.09833)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Bridging the Basilisk Astrodynamics Framework with ROS 2 for Modular Spacecraft Simulation and Hardware Integration** 

E. Krantz, N. N. Chan, G. Tibert, H. Mao, and C. Fuglesang 

**_Abstract_ — Integrating high-fidelity spacecraft simulators with modular robotics frameworks remains a challenge for autonomy development. This paper presents a lightweight, open-source communication bridge between the Basilisk astrodynamics simulator and the Robot Operating System 2 (ROS 2), enabling real-time, bidirectional data exchange for spacecraft control. The bridge requires no changes to Basilisk’s core and integrates seamlessly with ROS 2 nodes. We demonstrate its use in a leader–follower formation flying scenario using nonlinear model predictive control, deployed identically in both simulation and on the ATMOS planar microgravity testbed. This setup supports rapid development, hardware-in-the-loop testing, and seamless transition from simulation to hardware. The bridge offers a flexible and scalable platform for modular spacecraft autonomy and reproducible research workflows.** 

## SOFTWARE RELEASES 

- _BSK-ROS2-Bridge_ 

https://github.com/DISCOWER/bsk-ros2-bridge 

- _Basilisk ROS 2 Messages_ 

https://github.com/DISCOWER/bsk-msgs 

- _Demo MPC using BSK-ROS2-Bridge_ 

https://github.com/DISCOWER/bsk-ros2-mpc 

with ROS 2’s distributed middleware enables a unified autonomy pipeline across simulation, software-in-the-loop (SITL), and hardware-in-the-loop (HITL), addressing the lack of native compatibility and providing orbital fidelity unavailable in general-purpose robotic simulators. 

## _Contributions_ 

This paper introduces an open-source bridge between Basilisk and ROS 2, facilitating bidirectional communication between high-fidelity spacecraft simulations and modular robotics software. Our main contributions are: 

- A lightweight and scalable communication interface connecting ROS 2 nodes with Basilisk simulations without modifying Basilisk’s internal architecture. 

- Demonstration of the proposed bridge in a leaderfollower SFF scenario using Nonlinear Model Predictive Control (NMPC), fully implemented in ROS 2. 

- Comparative validation in both simulation and hardware using the KTH ATMOS free-flyers [6], showing consistent control performance across platforms. 

This work aims to support rapid prototyping and reliable software transition across simulation and hardware systems. 

## I. INTRODUCTION 

## II. RELATED WORK 

Spacecraft formation flying (SFF) enables advanced mission architectures by coordinating multiple spacecraft as a distributed system. This paradigm supports modular assembly, distributed sensing, and in-orbit inspection, but also demands precise control and inter-agent coordination under tight dynamic constraints [1]. Demonstration missions such as PRISMA [2] and PROBA-3 [3] illustrate the increasing performance requirements, with recent efforts targeting submeter accuracy. As autonomy becomes more critical, so does the ability to validate and iterate on control architectures quickly and reliably across different test environments. 

High-fidelity simulators like Basilisk (BSK) [4] are essential for modeling spacecraft dynamics, multi-body interactions, and orbital environments in autonomy development workflows. Meanwhile, Robot Operating System 2 (ROS 2) [5] has become the standard for modular, real-time capable robotics software, supported by a broad ecosystem for autonomy development. Bridging Basilisk’s orbital dynamics and flight-software interfaces 

This work was partially supported by the Wallenberg AI, Autonomous Systems and Software Program (WASP) funded by the Knut and Alice Wallenberg Foundation. 

All authors are with the KTH Royal Institute of Technology, Stockholm, Sweden. Emails: _{_ eliaskra, channn, tibert, huina, cfug _}_ @kth.se 

The Basilisk Astrodynamics Simulation Framework provides a modular environment combining a Python scripting interface with a high-performance C/C++ backend, widely used for spacecraft flight software (FSW) development [7]. Features like accelerated time, visualization via the Vizard engine, and, recently, the integration with MuJoCo [8] extend its applicability to articulated-bodies and space robotics [9]. However, integrating external autonomy software with Basilisk remains non-trivial. Typical workflows require implementing autonomy modules within Basilisk’s internal messaging system, posing a steep learning curve. Prior bridging efforts, such as the ROS–Basilisk interface in [10], embed ROS 2 execution within Basilisk through timer-coupled operation and per-message translation, which complicates time synchronization and increases maintenance overhead as message definitions and ROS 2 versions evolve. Similar integrations, such as with NASA’s core Flight System (cFS) [11], have demonstrated feasibility but remain tightly coupled to specific software versions. In contrast, general-purpose robotic simulators like Gazebo [12] and Isaac Sim [13] offer native ROS 2 support but lack the orbital dynamics fidelity required for spacecraft scenarios. 

ROS 2 itself has become a widely adopted framework for modular, distributed autonomy, supported by its DDS 

communication layer. Its design makes it well-suited for integrating complex robotic systems, including those in space environments. NASA’s Astrobee free-flyers aboard the ISS exemplify its use for onboard navigation, control, and perception [14]. Recent initiatives such as Space ROS [15], a safety-focused fork of ROS 2 developed by NASA and collaborators, further underscore the framework’s relevance for mission-critical space robotics. 

To enable representative testing of autonomous spacecraft systems, ground-based testbeds have become essential. These platforms provide repeatable microgravity-analog conditions, enabling HITL testing of planning and control algorithms. Notable examples include NASA Ames’ granite-based facility for Astrobee [16], Caltech’s large-scale resin-floor testbed [17], and ESA’s Orbital Robotics Laboratory [18]. At KTH Royal Institute of Technology, the ATMOS platform [6] offers an open-source 2D-spacecraft analog with air-based propulsion. It uses PX4 Autopilot [19] for low-level control and ROS 2 for high-level autonomy, supporting HITL evaluation of spacecraft control and planning algorithms under realistic and repeatable conditions. 

## III. BASILISK-ROS 2 BRIDGE 

The _BSK-ROS2-Bridge_ enables modular spacecraft autonomy development by connecting Basilisk’s high-fidelity simulation environment with the ROS 2 middleware. This opensource interface allows seamless and scalable data exchange between Basilisk and ROS 2, supporting both real-time and accelerated simulation workflows. The bridge is implemented as a ROS 2 package and leverages Basilisk’s existing support for ZeroMQ (ZMQ) [20], a lightweight messaging protocol used internally by Basilisk’s visualization tool Vizard. By integrating with Basilisk’s native message infrastructure without modifying its core, the bridge enables autonomy stacks to run externally in ROS 2 while maintaining synchronized interaction with the simulation. This design lowers the barrier to entry for researchers and engineers accustomed to robotics middleware, and supports multi-agent, real-time, and HITL scenarios with minimal setup. 

## _A. Architecture_ 

The bridge architecture consists of two main components: a ROS 2 node and a Basilisk-side handler module, Fig. 1. The bridge node behaves like any other ROS 2 component, integrating naturally into launch files and workflows. It operates independently and can remain active across multiple simulations, communicating externally with Basilisk via three ZMQ ports: receive, transmit, and heartbeat (used for monitoring connection health). On the Basilisk side, the handler module follows the standard Python module structure and is imported into the simulation script like any other Basilisk module. This design allows users to extend existing scenarios with ROS 2 connectivity by simply adding the handler to their simulation configuration. The integration is designed for accessibility: message routing is defined in the Basilisk script, while the bridge node requires no manual topic configuration in ROS 2, keeping a minimal setup. 


Fig. 1: Functional overview of the Basilisk – ROS 2 bridge. The bridge interfaces with the ROS 2 network and exchanges data with a Basilisk handler module, which connects messages to internal simulation modules. 

Communication between the bridge node and the Basilisk handler occurs via JSON-formatted byte messages over ZMQ sockets, supporting low-latency and high-frequency control loops. Additionally, the bridge publishes the Basilisk simulation time to ROS 2 via the /clock topic, allowing all ROS 2 nodes to remain synchronized with the simulation time, enabling consistent behavior across nodes and supporting both real-time and accelerated simulation modes. 

## _B. Scalability and Message Configuration_ 

The bridge supports both single- and multi-spacecraft scenarios. A single bridge and handler instance can manage any number of spacecraft using namespace-aware topic conventions. Message routing is configured programmatically in the Basilisk simulation script, where users register publishers and subscribers via the handler’s Python API by specifying the ROS 2 topic name, message type, internal identifier, and namespace. Topics follow the structure /[ _ns_ ]/bsk/[ _direction_ ]/[ _topic_ ], where [ _direction_ ] is either in (for ROS 2 _→_ Basilisk) or out (for Basilisk _→_ ROS 2). This convention enables scalable, multi-agent setups and integration with HITL experiments. 

To further simplify integration, Basilisk’s native message types are systematically converted into ROS 2-compatible message definitions, maintained in a standalone Git repository ( _bsk-msgs_ ). This repository includes tools to automatically update messages, ensuring continuous compatibility with future Basilisk updates. High-throughput applications are supported by launching multiple bridge-handler pairs on separate ports, yielding parallel communication streams suitable for large-scale formations, HITL testing, and highrate simulations. 

## IV. FORMATION CONTROL DEMONSTRATION 

To benchmark the BSK-ROS2 bridge in a coordinated multi-agent setting, we implement a formation flying scenario with one _leader_ and two _follower_ spacecraft. Each is controlled via a NMPC in ROS 2, with the followers maintaining a desired relative formation as the leader moves between waypoints. 

## _A. Dynamics Modeling in Simulation_ 

The local orbital Hill frame _H_ provides a convenient reference for describing relative dynamics of spacecraft in orbit (see Fig. 2). This rotating reference frame is centered at a designated leader spacecraft in a nearly circular orbit. Defined with respect to the Earth-Centered Inertial (ECI) frame _N_ , its axes are: 


where **_p_** and **_v_** are the leader’s position and velocity in the inertial frame, and **_h_** = **_p_** _×_ **_v_** is its specific angular momentum. This frame serves as the basis for describing the relative dynamics of a follower spacecraft with respect to the leader. 

The follower’s motion relative to the leader can be approximated using the Clohessy-Wiltshire (CW) equations [21]. Expressed in _H_ , centered on the leader, the follower’s relative position evolves according to: 


where _n_ = ~~�~~ _µ/a_<sup>3</sup> is the mean motion of the leader’s orbit, _µ_ is the gravitational parameter, _a_ is the semi-major axis, _Fx, Fy, Fz_ are the external force components acting on the follower, and _m_ is the follower spacecraft’s mass. These linearized equations are valid for small relative distances and velocities, _∥_ **_p_**<sup>_H_</sup> _∥≪ a_ and _∥_ **_v_**<sup>_H_</sup> _∥≪ na_ . 

Despite their simplicity, the CW equations reveal inherent drift and coupling effects due to Coriolis and centrifugal forces, making formation maintenance non-trivial. These fictitious forces make it challenging to maintain a stable relative configuration over time. Control strategies such as Model Predictive Control (MPC) must therefore actively compensate for these effects to ensure stability, disturbance rejection, and safe separation within tight relative constraints. 

The spacecraft attitude is represented using unit quaternions **q**<sup>_H|B_</sup> and angular velocity **_ω_**<sup>_B_</sup> . The rotational motion is governed by: 


where **q** **_ω_** _B_ is the quaternion representation of **_ω_** _B_ with zero scalar part, **J** is the moment of inertia matrix, **_τ_**<sup>**_B_**</sup> is the external torque, and _⊗_ denotes quaternion multiplication. 


Fig. 2: Hill frame _H_ (red), ECI frame _N_ (black) and body frame _B_ (green) with respect to a leader’s orbit (blue) [22]. 

## _B. Spacecraft Formation Flying NMPC_ 

Each agent employs an NMPC strategy where it solves an Optimal Control Problem (OCP) over a finite prediction horizon of _N_ steps. MPC is well suited for spacecraft formation control due to its ability to handle multivariable dynamics, predict future behaviors, and enforce constraints on control effort, collision avoidance, and relative motion [23], capabilities that standard linear controllers such as linear quadratic regulator lack. The nonlinear formulation is used as large rotational maneuvers introduce significant nonlinearities that linear controllers cannot accurately capture. At each discrete time _k_ , the controller optimizes a sequence of control inputs _{_ **_u_** ( _n|k_ ) _}_<sup>_N_</sup> _n_ =0<sup>_−_1tominimizeacostfunctionsubjecttody-</sup> namic and operational constraints, yielding a corresponding sequence of predicted states _{_ **_x_** ( _n|k_ ) _}_<sup>_N_</sup> _n_ =0<sup>,startingfromthe</sup> initial condition **_x_** (0 _|k_ ) = **_x_** _k_ . Only the first control input **_u_** (0 _|k_ ) is applied, and the process is repeated. For agent _a_ at time _k_ we have the following OCP: 


Here, the function _f_ ( _·_ ) denotes the discrete-time dynamics model in a fixed timestep ∆ _t_ , where the state = vector **_x_** and control input **_u_** are defined as **_x_** � **_p_**<sup>_H_</sup> **_v_**<sup>_H_</sup> **q**<sup>_H|B_</sup> **_ω_**<sup>_B_�</sup> _∈_ R<sup>13</sup> , and **_u_** = � **_F_**<sup>_B_</sup> **_τ_**<sup>_B_�</sup> _∈_ R<sup>6</sup> . The sets X _⊂_ R<sup>13</sup> and U _⊂_ R<sup>6</sup> define admissible states and control inputs, respectively, including velocity bounds, actuation limits, and spatial constraints. The scalar _d_ min _≥_ 0 defines the minimum allowable inter-agent separation distance for collision avoidance. The stage cost is defined as: 


where **Q** , and **R** are positive semi-definite weighting matrices. The terminal cost is defined analogously as: 


with weighting matrix **P** . The quaternion term minimizes the scalar deviation from the desired orientation and remains well-conditioned even for large attitude changes. 

In this decentralized architecture, each agent independently solves its own NMPC problem. The leader agent tracks a reference trajectory, which may be updated at any time through new waypoints. Each follower constructs its own reference trajectory based on the leader’s predicted motion, which is communicated at each control step as the solution to the leader’s OCP. Specifically, the follower applies a desired relative position and attitude to the leader’s predicted state while copying the leader’s velocity and angular velocity directly: 


where ∆ **_p_** _∈_ R<sup>3</sup> and ∆ **q** _∈_ R<sup>4</sup> represent the desired relative formation configuration in position and attitude. 

To ensure decentralized coordination, all agents communicate their predicted trajectories, i.e., their OCP solutions, at each control step. These shared trajectories are used by other agents to enforce the pairwise collision avoidance constraints during optimization. In this way, each agent incorporates the shared future trajectories of others, enabling predictive conflict resolution and safe formation-keeping without requiring centralized planning. 

## V. CROSS-PLATFORM VALIDATION 

Using this NMPC, we evaluate the BSK-ROS2 bridge’s ability to support modular autonomy stacks by deploying an identical leader–follower SFF in two settings: a physical hardware experiment using the planar ATMOS spacecraft analogs, Fig. 3, and a Basilisk simulation that replicates the same conditions, Fig. 4. 


Fig. 3: Three ATMOS free-flyer platforms. Each unit uses air bearings for frictionless 2D motion and is independently controlled for the spacecraft formation experiments. 


Fig. 4: Basilisk simulation of the leader-follower scenario, visualized in Vizard. 

## _A. Simulation and Hardware Setup_ 

Both setups use the same control architecture, spacecraft parameters, and autonomy logic to ensure a consistent evaluation across environments. In each case, the full control stack operates externally as ROS 2 nodes. The control strategy builds on the SFF NMPC controller described in Section IV, with three ROS 2 nodes deployed: one for the leader, which follows a predefined waypoint sequence, and one for each follower, which maintains a fixed relative position with respect to the leader. Each controller receives state estimates and outputs force and torque commands at 5 Hz, which are then allocated to actuators by the corresponding simulation or hardware stack. 

The ATMOS free-flyer platforms provide a microgravityanalog environment for two-dimensional motion, utilizing air bearings for nearly frictionless motion over an epoxycoated flat floor. Each unit is equipped with eight solenoid thrusters, powered by compressed air and arranged for holonomic 3-degrees-of-freedom (DoF) motion control (planar **_x_** ˆ, **_y_** ˆ, and yaw **_θ_** _z_ ). The Basilisk simulation mimics this hardware configuration with three spacecraft in Low-EarthOrbit (LEO), parameterized to match the ATMOS platforms in mass, inertia, and actuation setup. Due to this shared hardware constraint, only thrusters are used for actuation, excluding alternatives such as reaction wheels. In simulation, the thruster configuration is expanded to twelve symmetrically arranged units, enabling full 6-DoF actuation in 3D space while maintaining the same thruster-based actuation principle and hardware-matched limits. Both the physical and simulated spacecraft have a mass of 17.8 kg and a moment of inertia of _Jzz_ = 0.315 kg m<sup>2</sup> , with the simulation assuming symmetry _Jxx_ = _Jyy_ = _Jzz_ for simplicity. The maximum available thrust in **_x_**<sup>_B_</sup> and **_y_**<sup>_B_</sup> is 3.0 N, and the maximum torque about **_θ_** _z_<sup>_B_is0.51 N m.</sup> 

In both the hardware and simulation scenarios, thrusters are actuated via pulse width modulation (PWM) at 10 Hz, with each thruster producing approximately 1.5 N of thrust when active. For ATMOS, the controller runs offboard and transmits desired force and torque commands to the onboard PX4 flight controller, which performs control allocation via its internal mixer. In the simulation, control commands 


(a) Position and attitude tracking in Basilisk simulation (left) and on ATMOS free-flyers (right). 


(b) Commanded force and torque in Basilisk simulation (left) and on ATMOS free-flyers (right). 

Fig. 5: Comparison of position and attitude tracking, as well as control behavior, between Basilisk simulation and ATMOS hardware in the leader–follower formation flying scenario. 

are mapped to individual thruster inputs using Basilisk’s forceTorqueThrForceMapping module, subject to a minimum on-time of 1 ms to mimic hardware limitations. 

The leader spacecraft follows a cyclic pose trajectory composed of predefined waypoints, transitioning every 20 s. Followers are tasked with maintaining fixed positions of −1.0 m in **_x_**<sup>_H_</sup> and ±0.3 m in **_y_**<sup>_H_</sup> relative to the leader, while aligning their attitude with that of the leader. In the simulation case, the spacecraft are placed in a near-circular LEO, representative of typical formation-flying mission conditions, with semi-major axis _a_ = 6778.0 km, eccentricity _e_ = 0 _._ 001, inclination _i_ = 45<sup>_◦_</sup> , right ascension of the ascending node Ω= 270<sup>_◦_</sup> , and argument of periapsis _ω_ = 90<sup>_◦_</sup> . This choice provides realistic dynamic conditions while remaining general enough for other orbital regimes, and it does not affect comparability with the ATMOS hardware results, which are constrained to planar motion. 

Both scenarios share an identical NMPC formulation, solved in real-time using the ACADOS solver [24]. The prediction horizon is set to _N_ = 30 with timestep ∆ _t_ = 0.2 s. The cost function penalizes position, velocity, attitude, and angular velocity errors using a diagonal state weighting matrix **Q** = diag(1 **I** 3 _,_ 30 **I** 3 _,_ 1000 _,_ 10 **I** 3), control effort via **R** = diag(0 _._ 2 **I** 3 _,_ 100 **I** 3), and a terminal cost via **P** = 20 **Q** chosen via iterative tuning to achieve stable waypoint tracking with balanced control effort. 

## _B. Observed Performance_ 

Fig. 5 illustrates the tracking and control behavior observed in both simulation and hardware. The followers suc- 

cessfully tracked the leader’s communicated trajectory, maintaining formation within 0.17 m in simulation and 0.35 m on hardware. On the ATMOS platforms, a steady-state offset was visible across all agents, attributed to unmodeled disturbances such as floor unevenness and actuation asymmetries. These results highlight the ability of the BSK-ROS2 bridge to support seamless integration of modular autonomy stacks across platforms. Without changes to the controller implementation or architecture, the same ROS 2-based control nodes operate reliably in both high-fidelity simulation and hardware, validating the bridge’s utility for spacecraft formation control and HITL development workflows. 

## _C. Communication Performance_ 

Stress tests were conducted with an AMD Ryzen 5 5600X running Ubuntu 24.04 to assess the bridge’s scalability and communication limits under varying simulation speeds, spacecraft counts, and topic rates. As shown in Table I, the bridge remained stable at nominal control frequencies, with saturation only under extreme loads. 

TABLE I: Bridge communication performance 

|**Sim speed**|**S/c**|**Target [Hz]**|**Achieved [Hz]**|**Std [ms]**|
|---|---|---|---|---|
|1x|1|100|100|1.3|
|1x|1|10 000|4 390|1.0|
|100x|1|10 000|4 270|1.0|
|1x|100|100|100|6.5|
|100x|100|100|100|6.6|
|100x|100|1 000|270|2.4|


It sustained 100 Hz per agent with low jitter and reached about 4.4 kHz in single-agent high-load tests. Similar limits under 100x accelerated simulation indicate CPU-bound throughput rather than timing constraints. With 100 spacecraft, it showed saturation near 270 Hz per agent. These results confirm that the bridge comfortably supports typical spacecraft control frequencies. 

## VI. DISCUSSION 

The bridge developed in this work has proven to be a practical enabler for the rapid deployment of modular autonomy stacks in both simulation and hardware environments. By decoupling the control logic from the simulation engine, the same ROS 2 nodes used in Basilisk could be deployed on the ATMOS testbed with minimal changes. Specifically, the transition required only substituting Basilisk topics with those used by PX4, demonstrating the flexibility and portability of the proposed architecture. Such topic remappings can be easily automated. A key benefit of this approach is the ability to interact with the simulator in real-time without modifying its internal setup, which significantly lowers the barrier for incorporating advanced autonomy into existing Basilisk scenarios. The current setup was executed in an open-loop configuration, with no SITL or HITL feedback between Basilisk and the hardware. However, the bridge architecture inherently supports closed-loop setups, and enabling SITL or HITL is a promising avenue for future work. 

The formation flying scenario presented here, while intentionally constrained to a planar 2D setting with one leader and two followers, demonstrates the core functionality and viability of the bridge. More advanced use cases can now be explored by leveraging Basilisk’s extensive module library, which includes high-fidelity spacecraft dynamics, FSW architectures, realistic sensors, actuator models, and environmental disturbances. This includes scenarios such as spacecraft docking, articulated manipulators, deployable structures, and flexible appendages. Combined with the ROS 2 bridge, such capabilities can be coupled with realtime autonomy stacks, making them accessible for closedloop testing, planning, and control. 

## VII. CONCLUSIONS 

This paper presents a lightweight and extensible communication bridge between the Basilisk Astrodynamics Simulation Framework and ROS 2. By enabling bidirectional data exchange without requiring modifications to Basilisk’s internal architecture, the bridge allows real-time interaction between high-fidelity orbital dynamics and modular control stacks. Its effectiveness has been demonstrated in a leader–follower formation flying scenario using decentralized NMPC, where the same ROS 2-based control system was deployed without modification in both Basilisk and the ATMOS 2D microgravity platform. The results highlight the bridge’s utility in enabling seamless simulation-to-hardware transitions and supporting reproducible autonomy development workflows. Future work includes integration into SITL and HITL pipelines, scaling to larger constellations, and 

applications involving contact dynamics. The open-source release of the bridge aims to accelerate adoption within the space robotics community and serve as a foundation for modular, scalable autonomy architectures in orbital applications. 

## REFERENCES 

- [1] R. Kristiansen and P. J. Nicklasson, “Spacecraft formation flying: A review and new results on state feedback control,” _Acta Astronautica_ , vol. 65, pp. 1537–1552, 2009. 

- [2] P. Bodin _et al._ , “The prisma formation flying demonstrator: Overview and conclusions from the nominal mission,” _Adv. Astronaut. Sci._ , vol. 144, 2012. 

- [3] T. V. Peters, J. Branco, D. Escorial, L. T. Castellani, and A. Cropp, “Mission analysis for PROBA-3 nominal operations,” _Acta Astronautica_ , vol. 102, 2014. 

- [4] AVS Laboratory, “Basilisk Astrodynamics Simulation Framework.” [Online]. Available: https://avslab.github.io/basilisk/ 

- [5] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, “Robot operating system 2: Design, architecture, and uses in the wild,” _Science Robotics_ , vol. 7, no. 66, 2022. 

- [6] P. Roque _et al._ , “Towards open-source and modular space systems with ATMOS,” 2025, arXiv:2501.16973 [cs]. 

- [7] P. W. Kenneally, S. Piggott, and H. Schaub, “Basilisk: A flexible, scalable and modular astrodynamics simulation framework,” _Journal of Aerospace Information Systems_ , vol. 17, 2020. 

- [8] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ . IEEE, 2012, pp. 5026–5033. 

- [9] J. Garcia Bonilla and H. Schaub, “A message-passing simulation framework for generally articulated spacecraft dynamics,” in _AAS/AIAA Astrodyn. Specialist Conf._ , Boston, MA, 2025. 

- [10] K. Matsuka, L. Zhang, I. Ragheb, C. Ohenzuwa, and S.-J. Chung, “High-fidelity closed-loop simulation of spacecraft vision-based relative navigation in ROS2,” in _AAS/AIAA Space Flight Mech._ , 2023. 

- [11] R. Kramlich, J. Huun, A. Garcia, A. Cohen, and T. Gaston, “Validation of the guidance, navigation, and control (GNC) architecture for RPO missions using Basilisk-CFS architecture,” in _AAS/AIAA Astrodyn. Specialist Conf._ , Big Sky, Montana, 2023. 

- [12] N. Koenig and A. Howard, “Design and use paradigms for Gazebo, an open-source multi-robot simulator,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , vol. 3, 2004, pp. 2149–2154. 

- [13] NVIDIA Corporation, “Isaac Sim.” [Online]. Available: https: //developer.nvidia.com/isaac-sim 

- [14] L. Fl¨uckiger, K. Browne, B. Coltin, J. Fusco, T. Morse, and A. Symington, “Astrobee robot software: A modern software system for space,” NASA Ames Research Center, Tech. Rep., 2018. 

- [15] A. B. Probe _et al._ , “Space ROS: An open-source framework for space robotics and flight software,” in _Proc. AIAA SciTech Forum_ , 2023. 

- [16] M. Bualat, J. Barlow, T. Fong, C. Provencher, and T. Smith, “Astrobee: Developing a free-flying robot for the International Space Station,” in _AIAA SPACE Conf._ , 2015. 

- [17] T. Barrett, S. Schultz, W. Bezouska, and M. Aherne, “Demonstration of technologies for autonomous micro-satellite assembly,” in _AIAA SPACE Conf._ , 2009. 

- [18] H. Kolvenbach and K. Wormnes, “Recent developments on ORBIT, a 3-DoF free-floating contact dynamics testbed,” in _in Proc. Int. Symp. Artif. Intell., Robot. Autom. Space (i-SAIRAS)_ , 2016. 

- [19] L. Meier, D. Honegger, and M. Pollefeys, “PX4: A node-based multithreaded open source robotics framework for deeply embedded platforms,” in _Proc. IEEE Int. Conf. Robot. Autom. (ICRA)_ , 2015, pp. 6235–6240. 

- [20] iMatix, “ZeroMQ.” [Online]. Available: https://zeromq.org/ [21] W. H. Clohessy and R. S. Wiltshire, “Terminal guidance system for satellite rendezvous,” _Journal of the Aerospace Sciences_ , vol. 27, 1960. 

- [22] N. N. Chan, “Implementation of controller schemes for multi-agent spacecraft formation flights via the basilisk simulation framework,” Master’s thesis, KTH Royal Institute of Technology, 2025. 

- [23] J. Rawlings, D. Mayne, and M. Diehl, _Model Predictive Control: Theory, Computation, and Design_ , 2nd ed. Nob Hill Publishing, 2020. 

- [24] R. Verschueren _et al._ , “Acados—A modular open-source framework for fast embedded optimal control,” _Math. Program. Comput._ , vol. 14, no. 1, pp. 147–183, 2022. 

