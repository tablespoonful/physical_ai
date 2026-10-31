---
title: "A ROS2-based software library for inverse dynamics computation"
date: "2025-04-08"
authors: "Vincenzo Petrone; Enrico Ferrentino; Pasquale Chiacchio"
url: https://arxiv.org/abs/2504.06106
pdf: https://arxiv.org/pdf/2504.06106
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2504.06106)** / [論文ページ](https://arxiv.org/abs/2504.06106)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE ROBOTICS AND AUTOMATION PRACTICE 

1 

# A ROS2-based software library for inverse dynamics computation 

Vincenzo Petrone, _Student Member, IEEE,_ Enrico Ferrentino, _Member, IEEE,_ and Pasquale Chiacchio 

**_Abstract_ —Inverse dynamics computation is a critical component in robot control, planning and simulation, enabling the calculation of joint torques required to achieve a desired motion. This paper presents a ROS2-based software library designed to solve the inverse dynamics problem for robotic systems. The library is built around an abstract class with three concrete implementations: one for simulated robots and two for real UR10 and Franka robots. This contribution aims to provide a flexible, extensible, robot-agnostic solution to inverse dynamics, suitable for both simulation and real-world scenarios involving planning and control applications. The related software is available at https://github.com/unisa-acg/inverse-dynamics-solver/tree/rap.** 

**_Index Terms_ —Robot Operating System, Inverse Dynamics, ROS2.** 


Fig. 1. The Inverse Dynamics Solver library and its concrete implementations 

## I. INTRODUCTION 

**M** ODELING robotic systems’ dynamics is a fundamentalaspect in the design and control of robots [1]. In this context, the computation of _inverse dynamics_ plays a critical role. Inverse dynamics involves determining the torques required at each joint of a robot to produce a specified motion, given its joint positions, velocities, and accelerations [2]. 

This calculation is essential for a wide range of applications, from optimal motion planning [3] to advanced control [4] and human-robot collaboration [5]. Accurate and efficient computation of inverse dynamics is particularly critical in applications such as high-performance control systems [6], trajectory optimization [7], and real-time simulations [8]. 

In the ROS2 framework [9] – a de-facto standard in developing robotics software [10]–[12] – a common library that exposes interfaces to such paramount components does not currently exist. Releasing and documenting a software to fill this gap is the focus of this paper. 

## _A. Background_ 

The inverse dynamics problem can be framed as the determination of the dynamics components acting on a robotic system, according to the following model [2]: 


where **_H_** is the inertia term, **_C_** accounts for Coriolis and centrifugal effects, **_f_** is the friction vector, **_g_** describes the torques due to gravity, and **_τ_** are the torques applied to the system, while **_q_** , **_q_** ˙ and **_q_** ¨ indicate joint positions, velocities and accelerations, respectively. 

The inverse dynamics model requires a detailed representation of these components to compute the torques **_τ_** 

Authors are with the Department of Information Engineering, Electrical Engineering and Applied Mathematics (DIEM), University of Salerno, 84084 Fisciano, Italy (email: _{_ vipetrone, eferrentino, pchiacchio _}_ @unisa.it). 

necessary to achieve a specified joint motion, described by the kinematic variables ( **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨). Usually, the dynamic terms in (1) are described through equations of motion (EOM), typically devised according to Newton-Euler or Lagrange formulations, as a function of joint motion variables and parametrized w.r.t. DH kinematic parameters and dynamic parameters [13]. 

## _B. Contribution_ 

The primary contribution of this paper is a _ROS2-based software library_ designed to compute inverse dynamics for robotic systems, as in (1). Our module addresses the need for a flexible, extensible, and robot-agnostic solution to the inverse dynamics problem. The library is built around an abstract class called _Inverse Dynamics Solver_ (IDS) that defines a generic interface for inverse dynamics computation, ensuring its broad applicability across various robot platforms. 

As a further contribution, we provide three concrete implementations of this abstract class, as illustrated in Fig. 1: 

- 1) **A generic implementation for simulated robots** , based on KDL, suitable for use in physics-based simulators such as Gazebo or others in the ROS ecosystem. This implementation leverages the kinematic and dynamic parameters of the simulated robot to calculate the relevant dynamics components. 

- 2) **Two implementations for real robots** , tailored for specific robotic platforms, namely the the popular UR10 and Franka manipulators. These implementations account for real-world dynamics, including nonlinear friction models, making them suitable for applications involving optimal planning, accurate control, and hardware-in-theloop testing. 

The primary goal of this library is to provide a robust and reusable tool for computing inverse dynamics in both simulated and real-world scenarios, with particular emphasis on 

0000–0000/00$00.00 © 2021 IEEE 

IEEE ROBOTICS AND AUTOMATION PRACTICE 

2 


Fig. 2. Sequence diagram: the user can instantiate the IDS library with pluginlib, by specifying the parameter plugin_name via launch file; concrete solvers call external libraries (e.g., robot-specific models [14], [15] or other software modules, such as KDL) to retrieve dynamic components. 

ease of integration within ROS2-based systems. By adopting a modular approach with neat abstractions, our library aims to simplify the integration of inverse dynamics solvers into a wide range of contexts involving robotic applications. 

## II. INVERSE DYNAMICS SOLVER 

This section presents the functionality and architecture of the library, so as to provide a structural and behavioral description to the community. The readers can refer to our public repository for further details<sup>1</sup> . 

files. This critical design choice favors the robot-agnosticism required by off-the-shelf ROS libraries. 

At instance time, the robot description is required, which can be easily retrieved by parsing the URDF file with xacro<sup>3</sup> . Furthermore, the solver can be configured by choosing the root and the tip of the chain to solve the dynamics for, as well as the gravity vector, which influences the **_g_** ( **_q_** ) component. The functioning of the IDS library and its communication mechanisms with external entities in the ROS2 framework are schematized in Fig. 2 with a sequence diagram. 

## _A. Functionality_ 

The IDS library exposes functions to allow the user to extract **_H_** ( **_q_** ), **_C_** ( **_q_** _,_ **_q_** ˙) ˙ **_q_** , **_f_** ( ˙ **_q_** ), **_g_** ( **_q_** ) or **_τ_** . By default, **_τ_** is computed as in (1) by setting **_f_** ( ˙ **_q_** ) _≡_ 0. This choice is driven by the fact that, differently from the other components, it usually does not depend on linear dynamic parameters (typically estimated via identification techniques [14], [15]), and its formulation might follow various linear or nonlinear models [5]. Furthermore, some modern robot controllers compensate friction internally [16], [17], relieving the user from accounting for it in the design of the control software [18]. 

The library follows the pluginlib paradigm<sup>2</sup> , i.e., the software does not strictly depend on the concrete implementation, which can be chosen via configuration, e.g. via launch 

## _B. Architecture_ 

As shown in Fig. 3, the software architecture is composed by an abstract class, named InverseDynamicsSolver, providing the functionalities mentioned in Section II-A: this class represents a generic solver, and the particular implementation of the methods returning dynamic components is a responsibility of the concrete classes. 

_1) Abstract class:_ The interface exposes the following public methods, all inherited by the concrete implementations: 

- initialize: initializes the solver with the robot description and the root, tip and gravity parameters through the node parameters interface; 

- getInertiaMatrix: returns **_H_** ( **_q_** ); 

- getCoriolisVector: returns **_C_** ( **_q_** _,_ **_q_** ˙) ˙ **_q_** ; 

- getFrictionVector: returns **_f_** ( ˙ **_q_** ); 

> 1https://github.com/unisa-acg/inverse-dynamics-solver/tree/rap 

> 2https://github.com/ros/pluginlib/tree/ros2 

> 3http://wiki.ros.org/urdf 

IEEE ROBOTICS AND AUTOMATION PRACTICE 

3 


Fig. 3. Class diagram: methods inherited by the concrete implementations from the interface are omitted for brevity 


Fig. 4. Measured and computed torques on the simulated UR10 robot 

- getGravityVector: returns **_g_** ( **_q_** ); 

- getDynamicComponents: returns ( **_H_** _,_ **_Cq_** ˙ _,_ **_g_** ) 

_•_ getTorques: returns **_τ_** = **_H_** ( **_q_** )¨ **_q_** + **_C_** ( **_q_** _,_ **_q_** ˙) ˙ **_q_** + **_g_** ( **_q_** ). As mentioned in Section I-B, this class is derived by three solvers we provide. The KDL-based one is tailored for simulated robots, and discussed in Section II-B2. Two solvers for real robots, specifically UR10 and Franka, are presented in Section II-B3. It is worth highlighting that users in the ROS2 community are allowed to inherit the base class with their own implementations, possibly including the estimated models of other manipulators. 

_2) KDL-based solver:_ By exploiting the KDL library<sup>4</sup> , the InverseDynamicsSolverKDL concrete class computes the dynamic components, acting as a bridge between KDL’s and our IDS’ interfaces. Specializing the initialize method, it parses the robot description to build the kinematic chain via KDL. This class is useful when a complete kinematic and dynamic description is available, e.g. in the case both the DH and dynamic parameters are provided by the manufacturer, to be specified in the URDF file. However, it disregards the friction term **_f_** since, as mentioned in Section I-A, it does not depend on the inertial parameters. Therefore, the users are invited to adopt this library in simulation only, where joint friction can be disregarded. 

_3) Real UR10 and Franka solvers:_ We provide a solver for the UR10 industrial manipulator: the InverseDynamicsSolverUR10 class returns the torques for this robot, according to the model estimated by [15], including the nonlinear friction vector, and a regressive form for other terms. In [15], the robot is identified at current level, hence this class exposes methods to retrieve the joint currents, while the torquebased methods exploit the getDriveGainsMatrix function to convert currents to torques (see Fig. 3). Additionally, we share a solver for the Franka research robot: the InverseDynamicsSolverFrankaInria class implements the model estimated by [14] which, differently from the libfranka [19] implementation provided by the manufacturer, also provides a formulation for the nonlinear friction. Given the presence of **_f_** , both these solvers use (1) to compute **_τ_** , hence overloading the default getTorques 

method defined in the parent class, differently from the KDL solver discussed in Section II-B2. 

## _C. Implementation details_ 

The IDS defines the input/output types of the implemented methods using Eigen<sup>5</sup> , a popular C++ linear algebra library, widely used in ROS2. This way, users can easily manipulate the computed matrices for model-based applications, such as writing control schemes or evaluating planning algorithms [7]. 

## III. RESULTS 

This section reports the results obtained by employing the IDS. To demonstrate its robot-agnosticism, we adopt the same interface to retrieve the dynamic components of 4 robots, namely simulated and real UR10 and Franka manipulators. It is worth remarking that providing accurate dynamic models falls outside the scope of this article, as the correctness of the computed torques relies on the underlying estimations [14], [15]. Thus, the goal of this section is demonstrating the application of our IDS in different scenarios across various robotic platforms. Indeed, the results in terms of computed torques are _all_ obtained with the _same_ demo, exclusively re-configured with different plugins. The readers are invited to replicate the results with the reproducible CodeOcean capsule<sup>6</sup> . 

## _A. Simulations_ 

We exercise the KDL-based solver described in Section II-B2 in a Gazebo simulation: we command a trajectory to a simulated UR10 robot via a ros2_control joint trajectory controller, and compute the torques corresponding to each joint state with the IDS’ getTorques method, which computes all the dynamics components in (1), as explained in Section II-B1. Fig. 4 shows the joint torques returned by the IDS along the trajectory. Similarly, we command a trajectory to the Franka robot, and evaluate the same solver to retrieve the results displayed in Fig. 5. Notably, in both cases measured and computed torque signals showcase a perfect match, as Gazebo itself uses KDL to simulate the system dynamics. 

> 5https://eigen.tuxfamily.org/dox 

> 6https://doi.org/10.24433/CO.2265930.v1 

> 4https://github.com/orocos/orocos <u>kinematics dynamics</u> 

IEEE ROBOTICS AND AUTOMATION PRACTICE 

4 


Fig. 5. Measured and computed torques on the simulated Franka robot 


Fig. 6. Measured and computed torques on the real UR10 robot 

Consequently, the InverseDynamicsSolverKDL can be easily plugged in a robot-agnostic torque-based controller, to reliably compensate the dynamics of any simulated robot. 

## _B. Experiments_ 

_1) UR10:_ Commanding an excitation trajectory to the real UR10 robot through the ROS2 driver<sup>7</sup> , we measure the actual joint configurations and currents via a utility provided by the manufacturer<sup>8</sup> , and obtain the corresponding torques with the getDriveGainsMatrix method (see Section II-B3). Comparing them with the torques computed through our InverseDynamicsSolverUR10 library, Fig. 6 shows that they closely match the ones retrieved from actual currents, demonstrating the correctness of the model in [15] and of our software. 

_2) Franka:_ Similarly to what described in Section III-B1 for the UR10 manipulator, we command an excitation trajectory to the real Franka robot, and evaluate the InverseDynamicsSolverFrankaInria library on each measured joint configuration. Fig. 7 shows the measured torques, obtained via libfranka [19], against the ones computed with our IDS library. We remark that, as demonstrated in [14], the model we chose to implement in our software provides an explicit estimation of the friction contribution, differently from the manufacturer interface. The advantage 

> 7https://github.com/UniversalRobots/Universal <u>Robots ROS2 Driver</u> 

> 8https://github.com/UniversalRobots/RTDE <u>Python Client Library</u> 


Fig. 7. Measured and computed torques on the real Franka robot 

of this choice is that, although this manipulator compensates for friction internally in control applications [16], having an explicit model is crucial for, e.g., offline planning purposes [3], [7]. 

## IV. CONCLUSIONS 

This paper presented a ROS2-based robot-agnostic library to solve the inverse dynamics problem. Given joint positions, velocities and accelerations, the developed software can be used to compute the torques acting on the manipulator’s joints, along with the dynamic terms influencing the EOM. 

We released and documented a codebase including an interface, exposing methods to retrieve the aforementioned dynamic components, and three concrete implementations, implementing the estimated models of two popular real manipulators, and adopting the KDL library for simulated robots. With the abstract class we shared, other users in the ROS2 community can specialize the library with new concrete classes, implementing the solvers for different robotic platforms. 

The off-the-shelf library can be used in planning algorithms, control schemes, and simulations, enriching the community with a useful tool to adopt in various applications requiring the estimation or compensation of the robot dynamics. The software is validated in both simulated and real scenarios, to demonstrate its functioning in devising the torques of the manipulators we exercised our library on. 

In the future, we intend to extend our codebase by including the information about the robot’s payload, which might influence the dynamics [20], or implementing an additional concrete solver based on the Pinocchio library [1]. Furthermore, we plan to include the solver in model-based controllers, e.g. inverse dynamics or gravity compensation controllers, to be released as separate packages. 

## APPENDIX 

## DESCRIPTION OF SUPPLEMENTARY MATERIALS 

This work is supported by the following supplementary materials, detailed in the next sections: 

- a video, showing our validation setup and animating the obtained results: https://youtu.be/p5ITcvoozGc; 

- a CodeOcean capsule, to reproduce our results: https:// doi.org/10.24433/CO.2265930.v1; 

5 

IEEE ROBOTICS AND AUTOMATION PRACTICE 


Fig. 8. Robots involved in the experiments: (top) UR10; (bottom) Franka; (left) simulated in Gazebo; (right) real laboratory setup 

- a GitHub repository, containing the ROS2 packages: https://github.com/unisa-acg/inverse-dynamics-solver/ tree/rap. 

## _A. Video_ 

The attached video shows the execution of 4 excitation trajectories on simulated and real robots, namely Franka and UR10 manipulators (see Fig. 8). The plots included in Fig. 4– 7 are animated, to show the measured and computed torque signals along the robots’ movements. 

## _B. Code_ 

_1) CodeOcean capsule:_ By accessing our capsule on CodeOcean, users can execute the IDS software via formal unit tests and demos. On the one hand, tests are developed to validate the main functionalities of the library (see Sect. II), e.g. parameter-based initialization and correctness of the computed torques. On the other hand, demos replicate the results displayed in Fig 4–7. It is worth stressing that the CodeOcean capsule does not merely plot the _same_ data again, but actually builds and runs the concrete solvers from scratch, producing _new_ data (i.e., torque predictions) that, eventually, are plotted to reproduce the aforementioned graphs. 

_2) GitHub repository:_ To strengthen the impact of our work, we opened a Pull Request (PR) from our GitHub repository, so that the developed packages will be subject to code review from other members of the ROS2 community, and eventually released as part of ROS2 distributions. The PR towards rosdistro, to index our package under the humble distribution, is reachable at https://github.com/ros/ rosdistro/pull/44979. Furthermore, we opened an issue to ask 

to release our packages under ROS2 Git Built Package (GBP), reachable at https://github.com/ros2-gbp/ros2-gbp-github-org/ issues/732. Upon acceptance, our packages will be distributed via rosdep. 

## REFERENCES 

- [1] J. Carpentier, G. Saurel, G. Buondonno, J. Mirabel, F. Lamiraux, O. Stasse, and N. Mansard, “The Pinocchio C++ library : A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives,” in _IEEE/SICE International Symposium on System Integration (SII)_ , Jan. 2019, pp. 614–619. 

- [2] R. Featherstone and D. E. Orin, “Dynamics,” in _Springer Handbook of Robotics_ , 2nd ed., B. Siciliano and O. Khatib, Eds. Cham: Springer, 2016, vol. 3, pp. 195–211. [Online]. Available: https: //link.springer.com/10.1007/978-3-319-32552-1 

- [3] E. Ferrentino, H. J. Savino, A. Franchi, and P. Chiacchio, “A Dynamic Programming Framework for Optimal Planning of Redundant Robots Along Prescribed Paths With Kineto-Dynamic Constraints,” _IEEE Transactions on Automation Science and Engineering_ , vol. 21, no. 4, pp. 6744–6757, Oct. 2024. 

- [4] G. Antonelli, F. Caccavale, and P. Chiacchio, “A systematic procedure for the identification of dynamic parameters of robot manipulators,” _Robotica_ , vol. 17, no. 4, pp. 427–435, Jul. 1999. 

- [5] C. Gaz, E. Magrini, and A. De Luca, “A model-based residual approach for human-robot collaboration during manual polishing operations,” _Mechatronics_ , vol. 55, pp. 234–247, Nov. 2018. 

- [6] M. Adam, E. E. Hartmark, T. Andersen, D. A. Anisi, and A. Cavalcanti, “Safety assurance of autonomous agricultural robots: from offline modelchecking to runtime verification,” in _2024 IEEE 20th International Conference on Automation Science and Engineering (CASE)_ , Aug. 2024, pp. 2511–2516. 

- [7] V. Petrone, E. Ferrentino, and P. Chiacchio, “Time-Optimal Trajectory Planning With Interaction With the Environment,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 4, pp. 10 399–10 405, Oct. 2022. 

- [8] L. Puck, P. Keller, T. Schnell, C. Plasberg, A. Tanev, G. Heppner, A. Roennau, and R. Dillmann, “Performance Evaluation of Real-Time ROS2 Robotic Control in a Time-Synchronized Distributed Network,” in _2021 IEEE 17th International Conference on Automation Science and Engineering (CASE)_ , Aug. 2021, pp. 1670–1676. 

- [9] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, “Robot Operating System 2: Design, architecture, and uses in the wild,” _Science Robotics_ , vol. 7, no. 66, 2022, art. no. eabm6074. 

- [10] S. Dehnavi, M. Koedam, A. Nelson, D. Goswami, and K. Goossens, “CompROS: A composable ROS2 based architecture for real-time embedded robotic development,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , Sep. 2021, pp. 6449– 6455. 

- [11] C. Fernando, D. Olds, S. I. Campbell, and P. M. Maffettone, “Facile Integration of Robots into Experimental Orchestration at Scientific User Facilities,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , May 2024, pp. 9578–9584. 

- [12] A. Richard, J. Kamohara, K. Uno, S. Santra, D. van der Meer, M. Olivares-Mendez, and K. Yoshida, “OmniLRS: A Photorealistic Simulator for Lunar Robotics,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , May 2024, pp. 16 901–16 907. 

- [13] J. M. Hollerbach, W. Khalil, and M. Gautier, “Model Identification,” in _Springer Handbook of Robotics_ , 2nd ed., ser. Springer Handbooks, B. Siciliano, O. Khatib, B. Roth, G. Giralt, and H. Inoue, Eds. Springer International Publishing, 2016, vol. 6, pp. 113–138. [Online]. Available: http://dx.doi.org/10.1007/978-3-319-32552-1 

- [14] C. Gaz, M. Cognetti, A. Oliva, P. Robuffo Giordano, and A. De Luca, “Dynamic Identification of the Franka Emika Panda Robot With Retrieval of Feasible Parameters Using Penalty-Based Optimization,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 4, pp. 4147–4154, Oct. 2019. 

- [15] V. Petrone, E. Ferrentino, and P. Chiacchio, “The Dynamic Model of the UR10 Robot and Its ROS2 Integration,” _IEEE Transactions on Industrial Informatics_ , Feb. 2025, Accepted for publication, DOI: 10.1109/TII.2025.3534415. 

- [16] Franka Robotics, “Franka Control Interface (FCI),” 2023. [Online]. Available: https://frankaemika.github.io/docs/overview.html 

- [17] V. Chawda and G. Niemeyer, “Toward Torque Control of a KUKA LBR IIWA for Physical Human-Robot Interaction,” in _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , Sep. 2017, pp. 6387–6392. 

6 

IEEE ROBOTICS AND AUTOMATION PRACTICE 

- [18] L. Le Tien, A. Albu-Sch¨affer, A. De Luca, and G. Hirzinger, “Friction Observer and Compensation for Control of Robots with Joint Torque Measurement,” in _2008 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , Sep. 2008, pp. 3789–3795. 

- [19] S. Haddadin, S. Parusel, L. Johannsmeier, S. Golz, S. Gabl, F. Walch, M. Sabaghian, C. J¨ahne, L. Hausperger, and S. Haddadin, “The Franka Emika Robot: A Reference Platform for Robotics Research and Education,” _IEEE Robotics & Automation Magazine_ , vol. 29, no. 2, pp. 46–64, Jun. 2022. 

- [20] C. Gaz and A. De Luca, “Payload estimation based on identified coefficients of robot dynamics — With an application to collision detection,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , Vancouver, BC, Canada, Sep. 2017, pp. 3033–3040. 

