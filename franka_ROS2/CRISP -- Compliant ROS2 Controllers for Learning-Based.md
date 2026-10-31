---
title: "CRISP -- Compliant ROS2 Controllers for Learning-Based Manipulation Policies and Teleoperation"
date: "2025-09-08"
authors: "Daniel San José Pro; Oliver Hausdörfer; Ralf Römer; Maximilian Dösch; Martin Schuck; Angela P. Schoellig"
url: https://arxiv.org/abs/2509.06819
pdf: https://arxiv.org/pdf/2509.06819
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.06819)** / [論文ページ](https://arxiv.org/abs/2509.06819)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# CRISP - <u>Compliant ROS2</u> Controllers for Learning-Based Manipulation <u>Policies</u> and Teleoperation 

Daniel San Jos´e Pro, Oliver Hausd¨orfer, Ralf R¨omer, Maximilian D¨osch, Martin Schuck and Angela P. Schoellig 

**_Abstract_ — Learning-based controllers, such as diffusion policies and vision-language action models, often generate lowfrequency or discontinuous robot state changes. Achieving smooth reference tracking requires a low-level controller that converts high-level targets commands into joint torques, enabling compliant behavior during contact interactions. We present CRISP, a lightweight C++ implementation of compliant Cartesian and joint-space controllers for the ROS2 control standard, designed for seamless integration with high-level learningbased policies as well as teleoperation. The controllers are compatible with any manipulator that exposes a joint-torque interface. Through our Python and Gymnasium interfaces, CRISP provides a unified pipeline for recording data from hardware and simulation and deploying high-level learningbased policies seamlessly, facilitating rapid experimentation. The system has been validated on hardware with the Franka Robotics FR3 and in simulation with the Kuka IIWA14 and Kinova Gen3. Designed for rapid integration, flexible deployment, and real-time performance, our implementation provides a unified pipeline for data collection and policy execution, lowering the barrier to applying learning-based methods on ROS2compatible manipulators. Detailed documentation is available at the project website.** 

**_Index Terms_ — Compliance and Impedance Control, Telerobotics and Teleoperation, Software-Hardware Integration for Robot Systems Deep Learning in Grasping and Manipulation, Reinforcement Learning, Imitation Learning,** 

ronment. While ROS and ROS2 have generally simplified robotics software development, current ROS2 tooling for such tasks often introduces significant overhead. At the same time, several robot manufacturers, including Franka Robotics, Kinova, Duatic, and ROBOTIS, together with the broader ROS2 community, have contributed high-quality ros2 ~~c~~ ontrol [9] hardware interfaces that are actively maintained and support direct torque control for a wide range of manipulators. This convergence creates an opportunity to implement modular, low-level controllers that integrate directly with the ROS2 control interface and are well suited to the requirements of high-level learning-based policies. 

**Contributions.** We present CRISP, a C++ implementation with Python interfaces of compliant Cartesian and joint-space controllers for robotic manipulators compatible with the ROS2 and ros2 ~~c~~ ontrol frameworks. Our main contributions are: 

- **Robot-agnostic, compliant Cartesian and joint-space controllers** that leverage ROS2 standard interfaces to ensure broad compatibility. 

- **A unified pipeline for data collection and deployment of learning-based policies** through our Python interface CRISP PY and Gymnasium interface CRISP GYM. 

## I. INTRODUCTION 

In recent years, learning-based policies for robotic manipulation have become increasingly prevalent. These approaches commonly command changes in the robot state as small trajectories over a short horizon, also called action chunks, or low-frequent targets, often at around 5 to 10 Hz, without requiring a traditional perception and path planning stack [2]–[6]. Such paradigms require low-level controllers that can respond to command changes during deployment rather than following precomputed smooth trajectories, which has been the typical mode of operation in manipulation in the past [7], [8]. Moreover, many challenging manipulation tasks often involve interaction with the environment, including contact-rich behaviors. 

Learning-based applications demand responsive, lowlatency controllers capable of reacting to both user or highlevel policy input and to a dynamically changing envi- 

The authors are with the Technical University of Munich (TUM), Germany; the TUM School of Computation, Information and Technology, Department of Computer Engineering, Learning Systems and Robotics Lab and the TUM Munich Institute of Robotics and Machine Intelligence (MIRMI). Email: _{_ daniel.sanjose.pro; oliver.hausdoerfer; maximilian.doesch; martin.schuck; angela.schoellig _}_ @tum.de. 

## II. RELATED WORK 

Traditionally, executing complex robot manipulation tasks relies on a path planning and perception pipeline. Established frameworks such as MoveIt [10] provide comprehensive planning capabilities; however, they often depend on extensive software stacks that require users to have in-depth knowledge for effective integration into their systems. In contrast, recent learning-based approaches focus on producing small chunks or low-frequency target poses rather than full trajectories, which reduces system complexity and necessitates a fundamentally different architectural framework. 

Several existing efforts address discontinuous Cartesian control within ROS. Table I compares our implementation with other available options. The Cartesian controllers developed by the FZI Research Center for Information Technology (FZI CC) [11] support position and velocity control but do not provide torque-based control. Other controllers, such as the Cartesian Impedance Controller (CIC) [12], compliant ~~c~~ ontrollers [13], or serl ~~f~~ ranka ~~c~~ ontrollers [14], implement Cartesian impedance control but are only available for ROS1 or 


Fig. 1. CRISP architecture overview and integration with robots using ROS2. We provide CRISP ~~P~~ Y, an easy-to-use Python interface to the CRISP controllers, as well as Gymnasium [1] environments we use for data collection and policy deployment in CRISP ~~G~~ YM. The user can publish any of the available target commands at arbitrary frequencies via ROS2 topics, and the robot will track the most recent target. High-level learning-based policies such as vision-language-action (VLA) models typically use the target ~~p~~ ose topic. We run the CRISP controllers on a real-time enabled Linux workstation at 1 kHz, while CRISP ~~G~~ YM with the VLA model runs on a separate workstation in the same network, communicating via ROS2 topics. CRISP ~~G~~ YM further easily integrates robotic grippers, cameras, and additional sensors required for the task via ROS2 topics. 

||FZI CC|CIC|Ours|
|---|---|---|---|
|ROS1|x|x||
|ROS2|x||x|
|Torque/effort interface||x|x|
|Robot agnostic|x|x|x|
|Highly Configurable|(x)|x|x|
|Cartesian Impedance||x|x|
|Nullspace Biasing||x|x|
|Force control||x|x|
|Joint limits barrier|||x|
|Friction Compensation|||x|
|Operation Space Control|||x|
|Built with pinocchio<sup>1</sup>|||x|
|Gymnasium Wrapper|||x|


### TABLE I 

COMPARISON TO THE CLOSEST AVAILABLE CONTROLLER IMPLEMENTATIONS 

are specific to a single manipulator type. Additional userdeveloped tools have also emerged [15]–[17], but these are typically robot specific or lack ros2 ~~c~~ ontrol integration. The emerging LeRobot framework [18] improves accessibility for learning-based manipulation, but does not yet support a wide range of manipulators and lacks full integration with ROS2. 

In contrast to existing frameworks, we present robotagnostic controllers that integrate seamlessly with the ROS2 standard and support both data collection and deployment of learning-based policies. 

## III. IMPLEMENTATION 

To ensure robot agnosticism, we implement compliant controllers in C++ for the ros2 ~~c~~ ontrol interface, capable of running at 1 kHz on a joint-torque interface. These controllers are designed to be responsive and robust to the discontinuous command updates typically generated by highlevel learning-based policies. As shown in the overview in Figure 1, users can publish target commands at any frequency using CRISP PY and CRISP GYM, and the controller will continuously track the most recent command. 

> 1ROS native, well-tested kinematics and rigid-body dynamics library based on Lie groups. 

The controllers implement joint limit barriers and include friction compensation for smooth teleoperation. All required rigid-body computations, as well as parsing of the robot structure from the standard Universal Robot Description File (URDF), are handled by pinocchio [19]. The pinocchio library efficiently implements rigid-body dynamics, is distributed with ROS2 binaries, and supports modern automatic differentiation in addition to other features required for advanced control algorithms. 

To enable configurability and ease of integration into other software stacks, all controller parameters are dynamically configurable via standard ROS2 parameter services. Examples of configurable parameters include stiffness, damping, nullspace stiffness, torque rate limits, and error limits. Several default configurations are provided in our repositories. 

## _A. Task Torque_ 

The task torque **_τ_** task refers to the desired torques to be applied to solve the task of following a target pose ( **x** target _,_ **R** target) _∈_ R<sup>3</sup> _× SO_ (3) which is represented with respect to the base frame. It attempts to minimize the error **e** = ( **e** pos _,_ **e** rot) _∈_ R<sup>6</sup> with respect to the current pose ( **x** current( **q** ) _,_ **R** current( **q** )) computed using forward kinematics. The error can computed with respect to the base as 


or with respect to the end effector-frame as 


where Log is the logarithmic map used to map a rotation difference to the tangent space of _SO_ (3). This can be seen as an angular velocity that turns the end-effector rotation towards the target rotation [20]. Defining the error in different frames allows the user to define anisotropic stiffness and damping behavior of the controller with respect to the endeffector or base frame. 

_1) Cartesian Impedance (CI) Controller:_ This controller implements a virtual spring between the end-effector and the reference pose and is well suited for contact-rich, compliant 

tasks, as it adapts well to contacts [21]: 


where **J** denotes the geometric Jacobian with respect to the base or end-effector frame computed from the provided URDF and **K** p, **K** d are the stiffness and damping matrices respectively chosen by the user. 

_2) Operational Space Controller (OSC):_ Compared to the CI controller, OSC accounts for the dynamics, in particular the inertia, in the control law [22]. The OSC tends to be more precise but less compliant in the presence of contact. The task torque is given by 


where **Λ** ( **q** _,_ **q** ˙ ) = ( **J**<sup>_†⊤_</sup> **M**<sup>_−_1</sup> **J**<sup>_†_</sup> )<sup>_−_1</sup> denotes the task-space mass matrix computed using the mass matrix **M** . The mass matrix is determined with the provided URDF using pinocchio. OSC does not compensate for the Coriolis and gravity terms in the task space. Instead, these are dynamically decoupled and directly compensated in joint-space, since it makes computations easier and the performance is similar to the original OSC [23]. 

## _B. Null Space Control_ 

For redundant manipulators, we provide the option to control in the null space of the task, which is useful to limit unnecessary motions, avoid singularities, and stabilize the joints to the resting position. This can be achieved by projecting a secondary control law **_τ_** secondary with a null space projector **N** _∈_ R<sup>_n×n_</sup> to a subspace that does not interfere with the primary task [24]. The secondary task in our control law is a joint impedance controller computed as 


We provide different projectors to compute the null space torque **_τ_** ns = **N** **_τ_** secondary: (1) a static null space projector **N** = **I** _−_ **J**<sup>_⊤_</sup> ( **J**<sup>_†_</sup> )<sup>_⊤_</sup> , (2) a dynamic null space projector **N** = **I** _−_ **J**<sup>_⊤_</sup> **J**<sup>**¯**</sup><sup>_⊤_</sup> , where **J**<sup>**¯**</sup> = **M**<sup>_−_1</sup> **J**<sup>_⊤_</sup> ( **JM**<sup>_−_1</sup> **J**<sup>_⊤_</sup> )<sup>_−_1</sup> is the generalized inverse Jacobian [22], and (3) an identity null space projector **N** = **I** that can be used to directly control the manipulator with joint commands if the task stiffness **K** p and damping **K** d have been set to 0. The dynamic null space projector leads to better primary task tracking compared to the static null space projector, provided that a sufficiently accurate model (URDF) of the robot is available [25]. 

## _C. Joint Barrier_ 

In order to avoid reaching the joint limits of the robot and prevent damage, we add joint barriers that apply an increasing torque as the joint gets close to the limits by _ϵ_ : 


## _D. Gravity and Coriolis Compensation_ 

We efficiently compute the gravity compensation and coriolis term using pinocchio, which uses the Recursive Newton Euler Algorithm (RNEA) to solve the Inverse Dynamics problem _τ_ = _RNEA_ ( **q** _,_ **˙q** _,_ **¨q** _,_ **_F_** ext) to determine **_τ_** gravity = **g** ( **q** ) = _RNEA_ ( **q** _,_ **0** _,_ **0** _,_ **0** ) and **_τ_** coriolis = **C** ( **q** _,_ **˙q** ) **˙q** . For the user, it is therefore important to provide the inertial parameters in the URDF file if these are not included by default. In case a manipulator already provides gravity compensation, it can be removed from the control law. 

## _E. Friction Compensation_ 

We provide a term to compensate for friction effects that are unmodeled terms in the equations of motion for rigid bodies. The friction can be modeled as a combination of static Coulomb friction, viscous friction, and a friction offset. We provide a simplified model as used in [26] to estimate the Franka Emika Robot friction term: 


with _σ_ ( _u_ ) = 1+exp (1 _−u_ )<sup>.Thismodeloffrictionneglects</sup> viscous terms and uses a sigmoidal function instead of a sign function to avoid sudden discontinuities around zero velocities. 

While we provide friction parameters for the Franka Robotics FR3 [26], these parameters must be determined for each robot by the user or the term omitted entirely. In practice, this term is particularly useful for teleoperation, as it makes the operator feel less unnatural resistance when moving the robot. 

## _F. Target Wrench_ 

Using our implementations, it is possible to command a wrench at the end-effector to apply external forces and torques. The term is computed as **_τ_** wrench = **J**<sup>_⊤_</sup> **_F_** target, where **_F_** _∈_ R<sup>6</sup> denotes the desired wrench. Wrench control is useful for tasks that demand careful interaction with the environment, require specific torques to be applied such as in screw driving [8], compensate for the weight of end-effector extensions, or simply drive the robot with a wrench instead of Cartesian poses. 

## _G. Final Control Law_ 

Our final control law is a sum of all the previous terms: 


In our implementation, each term can be switched on and off depending on the task, giving full flexibility to the user. 

## _H. Additional Features_ 

We provide additional safety features including joint torque and rate limits, exponential filtering of targets to avoid fast movements, and tracking error clipping for precise yet safe control when targets are distant [14]. For teleoperation, we implement force-torque feedback controllers where follower forces are reflected to the leader as **_τ_** fb = _−k_ p,fb **J**<sup>_⊤_</sup> _F_ follower _− k_ d,fb ˙ **q** leader. 


Fig. 2. **Robot-agnostic Cartesian control [I]:** Error evolution for tracking a discontinuous target pose using a Franka Emika FR3 on hardware with CRISP. We set a new target pose at _t_ = 1 s. For reproducibility, the controller parameters used are available on our website. Note that exact tracking performance depends on controller parameterization, which should be chosen based on the specific task. **Left:** Position error evolution with steady-state errors of 5.54 mm, 4.73 mm, and 0.81 mm for OSC, CI, and CI-clipped, respectively. **Right:** Rotational error evolution with steady-state errors of 0.0998 rad, 0.0532 rad, and 0.0029 rad for OSC, CI, and CIclipped, respectively. 


Fig. 3. **Robot agnostic Cartesian control [II]:** We demonstrate our controllers on a Franka FR3 on hardware, and on multiple manipulators in simulation. **Left:** Franka Robotics FR3. **Middle:** Kinova Gen3. **Right** : Kuka IIWA 14. 

## IV. EVALUATION 

The controllers have been validated on hardware using the Franka Robotics FR3 and in simulation with the Kuka IIWA14 and Kinova Gen3, as shown in Figure 3. Videos of these experiments are available on the project website. In this section, we present results for three representative tasks performed with our controllers. All experiments were conducted on a real Franka Robotics FR3. The exact tracking performance depends on the parameters selected by the user for the specific task as well as the manipulator used. 

First, we evaluate the tracking capabilities by issuing a randomly generated target pose within a safe motion range and monitoring the evolution of the tracking error over time, as shown in Figure 2. This experiment illustrates the tracking performance for a fixed target pose under different parameter configurations available to the user. 

Second, we demonstrate our teleoperation setup for a Lego stacking task in Figure 4. During teleoperation, the end effector poses from the leader robot are streamed to the follower at roughly 30 Hz, where they are tracked using the CRISP CI controller. The torque-based controllers allow for force feedback as well as compliant behavior. 

Third, we evaluate our controllers deployed with two imitation learning policies, namely Diffusion Policy [4] and SmolVLA [27], running at different inference frequencies on a GPU. The policies are deployed with the same Python interface as used for the previously described data collection with teleoperation. The results are shown in Figure 5. 

Our experiments demonstrate that the proposed controllers are suitable to track poses commanded by learning-based policies or by a human operator through teleoperation. 


Fig. 4. **Unified data collection and policy deployment [I]:** Recording a block-stacking task with Lego using teleoperation and force-torque feedback for the operator. **Upper left:** Plot of the follower’s target and end-effector positions. **Lower left:** Feedback wrenches applied at the leader manipulator. **Upper right:** Image of the recording on the follower manipulator at the current time. **Lower right:** Image of the operator guiding the leader robot to record data on the follower at the current time. 


Fig. 5. **Unified data collection and policy deployment [II]:** Using the same recorded data in the CRISP GYM interface, different learned policies can be successfully deployed in hardware. **Left:** Diffusion Policy [4] operating at approximately 30 Hz. **Right:** SmolVLA [27] operating at approximately 10 Hz. Both policies provide end-effector target pose updates that are tracked by our CRISP controllers. Note the different timescales shown in the plots. For policy deployment, we used the CI controllers with CRISP GYM. 

## V. CONCLUSION 

In this work, we present CRISP - an implementation of controllers for robotic manipulators designed for the deployment of learning-based policies that require tracking of small action chunks or low-frequency, discontinuous target joints or poses. The robot-agnostic implementation in ROS2 enables broad applicability across platforms, while its lightweight software design facilitates easy integration in new software stacks. Our framework can be used for both data collection and policy deployment across different manipulators, thereby accelerating research in learning-based manipulation. 

REFERENCES 

- [1] M. Towers, A. Kwiatkowski, J. Terry, J. U. Balis, G. De Cola, T. Deleu, M. Goul˜ao, A. Kallinteris, M. Krimmel, A. KG _et al._ , “Gymnasium: A Standard Interface for Reinforcement Learning Environments,” _arXiv preprint arXiv:2407.17032_ , 2024. 

- [2] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choromanski, T. Ding, D. Driess, A. Dubey, C. Finn, P. Florence, C. Fu, M. G. Arenas, K. Gopalakrishnan, K. Han, K. Hausman, A. Herzog, J. Hsu, B. Ichter, A. Irpan, N. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, L. Lee, T.-W. E. Lee, S. Levine, Y. Lu, H. Michalewski, I. Mordatch, K. Pertsch, K. Rao, K. Reymann, M. Ryoo, G. Salazar, P. Sanketi, P. Sermanet, J. Singh, A. Singh, R. Soricut, H. Tran, V. Vanhoucke, Q. Vuong, A. Wahid, S. Welker, P. Wohlhart, J. Wu, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich, “RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control,” in _Proceedings of the 7th Conference on Robot Learning_ , vol. 229, 2023, pp. 2165–2183. 

- [3] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware,” in _Proceedings of Robotics: Science and Systems (RSS XIX)_ , 2023. 

- [4] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion Policy: Visuomotor Policy Learning via Action Diffusion,” _The International Journal of Robotics Research_ , 2024. 

- [5] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky, “ _π_ 0: A Vision-Language-Action Flow Model for General Robot Control,” 2024. 

   - [20] J. Sol`a, J. Deray, and D. Atchuthan, “A micro Lie theory for state estimation in robotics,” 2021. 

   - [21] N. Hogan, “Impedance Control: An Approach to Manipulation,” in _1984 American Control Conference_ , 1984, pp. 304–313. 

   - [22] O. Khatib, “A unified approach for motion and force control of robot manipulators: The operational space formulation,” _IEEE Journal on Robotics and Automation_ , vol. 3, no. 1, pp. 43–53, 1987. 

   - [23] J. Nakanishi, R. Cory, M. Mistry, J. Peters, and S. Schaal, “Operational Space Control: A Theoretical and Empirical Comparison,” _The International Journal of Robotics Research_ , vol. 27, no. 6, pp. 737–757, 2008. 

   - [24] A. Dietrich, C. Ott, and A. Albu-Sch¨affer, “An overview of null space projections for redundant, torque-controlled robots,” _The International Journal of Robotics Research_ , vol. 34, no. 11, pp. 1385–1400, 2015. 

   - [25] A. Albu-Schaffer, C. Ott, U. Frese, and G. Hirzinger, “Cartesian impedance control of redundant robots: Recent results with the DLRlight-weight-arms,” in _IEEE International Conference on Robotics and Automation_ , vol. 3. IEEE, 2003, pp. 3704–3709. 

   - [26] C. Gaz, M. Cognetti, A. Oliva, P. Robuffo Giordano, and A. De Luca, “Dynamic Identification of the Franka Emika Panda Robot With Retrieval of Feasible Parameters Using Penalty-Based Optimization,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 4, pp. 4147–4154, 2019. 

   - [27] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti _et al._ , “SmolVLA: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [6] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “OpenVLA: An Open-Source Vision-Language-Action Model,” in _Proceedings of the 8th Conference on Robot Learning_ , vol. 270, 2025, pp. 2679–2713. 

- [7] M. Brady, J. M. Hollerbach, T. Johnson, T. Lozano-Perez, and M. T. Mason, _Robot Motion: Planning and Control_ , 1982. 

- [8] K. M. Lynch and F. C. Park, _Modern Robotics: Mechanics, Planning, and Control_ . New York: Cambridge University Press, 2017. 

- [9] “ROS2 control,” https://control.ros.org/rolling/index.html, accessed: 2024-05-03. 

- [10] D. Coleman, I. A. Sucan, S. Chitta, and N. Correll, “Reducing the Barrier to Entry of Complex Robotic Software: a MoveIt! Case Study,” _Journal of Software Engineering for Robotics_ , vol. 5, no. 1, pp. 3–16, 2014. 

- [11] S. Scherzinger, A. Roennau, and R. Dillmann, “Forward Dynamics Compliance Control (FDCC): A new approach to cartesian compliance for robotic manipulators,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2017, pp. 4568–4575. 

- [12] M. Mayr and J. M. Salt-Ducaju, “A C++ Implementation of a Cartesian Impedance Controller for Robotic Manipulators,” _Journal of Open Source Software_ , vol. 9, no. 93, p. 5194, 2024. 

- [13] A. L. Mitchell, T. Flatscher, and I. Posner, “Task and Joint Space Dual-Arm Compliant Control,” 2025. 

- [14] “serl ~~f~~ ranka ~~c~~ ontrollers,” https://github.com/rail-berkeley/serl ~~f~~ ranka controllers, accessed: 2025-05-05. 

- [15] Y. Zhu, A. Joshi, P. Stone, and Y. Zhu, “VIOLA: Imitation Learning for Vision-Based Manipulation with Object Proposal Priors,” _6th Annual Conference on Robot Learning (CoRL)_ , 2022. 

- [16] J. Elsner, “Taming the Panda with Python: A powerful duo for seamless robotics programming and integration,” _SoftwareX_ , vol. 24, p. 101532, 2023. 

- [17] T. Schneider, “franky,” https://github.com/TimSchneider42/franky, accessed: 2025-08-04. 

- [18] R. Cadene, S. Alibert, A. Soare, Q. Gallouedec, A. Zouitine, S. Palma, P. Kooijmans, M. Aractingi, M. Shukor, D. Aubakirova, M. Russi, F. Capuano, C. Pascale, J. Choghari, J. Moss, and T. Wolf, “LeRobot: State-of-the-art Machine Learning for Real-World Robotics in Pytorch,” https://github.com/huggingface/lerobot, 2024. 

- [19] J. Carpentier, G. Saurel, G. Buondonno, J. Mirabel, F. Lamiraux, O. Stasse, and N. Mansard, “The Pinocchio C++ library – A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives,” in _IEEE International Symposium on System Integrations (SII)_ , 2019. 

