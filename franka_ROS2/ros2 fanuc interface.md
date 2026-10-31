---
title: "ros2 fanuc interface: Design and Evaluation of a Fanuc CRX Hardware Interface in ROS2"
date: "2025-06-17"
authors: "Paolo Franceschi; Marco Faroni; Stefano Baraldo; Anna Valente"
url: https://arxiv.org/abs/2506.14487
pdf: https://arxiv.org/pdf/2506.14487
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2506.14487)** / [論文ページ](https://arxiv.org/abs/2506.14487)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# _ros2_ _<u>fanuc interface</u>_ : Design and Evaluation of a Fanuc CRX Hardware Interface in ROS2 

Paolo Franceschi<sup>1</sup> , Marco Faroni<sup>2</sup> , Stefano Baraldo<sup>1</sup> , Anna Valente<sup>1</sup> 

**_Abstract_ —This paper introduces the ROS2 control and hardware interface integration for the Fanuc CRX robot family. It explains basic implementation details and communication protocols, and its integration with the Moveit2 motion planning library. We conducted a series of experiments to evaluate relevant performances in the robotics field. We tested the developed** **_ros2_** **_<u>fanuc interface</u>_ for four relevant robotics cases: step response, trajectory tracking, collision avoidance integrated with Moveit2, and dynamic velocity scaling, respectively. Results show that, despite a non-negligible delay between command and feedback, the robot can track the defined path with negligible errors (if it complies with joint velocity limits), ensuring collision avoidance. Full code is open source and available at https://github.com/paolofrance/ros2** **<u>fanuc interface.</u>** 

**_Index Terms_ —ROS2 control, Hardware Interface, ROS2-Fanuc Hardware Interface** 

## I. INTRODUCTION 

**T** HEde factoRobotstandardOperatingto controlSystemrobots(ROS)in ecosystemthe researchisfieldthe and is growing in interest from the industrial world. ROS and ROS2 allow for seamless integration of state-of-the-art motion planning, vision, and control algorithms, acting as a middleware for modular software development and deployment. While initially widespread mainly in academia, ROS2 has now reached a level of maturity that makes it usable in industrial applications [1]. 

In the ROS2 world, the _ros2_ _<u>control</u>_ framework [2] is a control architecture designed to standardize and simplify the development of controllers and hardware abstractions. _ros2_ _<u>control</u>_ separates high-level control logic from low-level hardware interfaces, promoting reusability and maintainability across diverse robotic systems. Central to this architecture are the _ros2_ _<u>controllers</u>_ package and the concept of _hardware interfaces_ . On the one hand, _ros2_ _<u>controllers</u>_ provides a collection of standardized controllers for common robotic functionalities (such as joint trajectory tracking, forward command execution, and state broadcasting, etc.) designed to work seamlessly with different robot configurations through welldefined interfaces. On the other hand, _hardware interface_ defines how actuator and sensor data are exchanged between ROS2 and the physical robot. In other words, it translates the standard interfaces expected by ROS2 controllers into hardware-dependent commands and data formats of a specific robot. 

Corresponding author: paolo.franceschi@supsi.ch 

> 1 Department of Innovative Technologies, University of Applied Science and Arts of Southern Switzerland (SUPSI), Lugano, Switzerland 

> 2 Dipartimento di Elettronica, Informazione e Bioingegneria, Politecnico di Milano, Milan, Italy 


Fig. 1: Real and simulated scene of the collision avoidance experiment. 

Most industrial robots are integrated, to some extent, with the _ros2_ _<u>control</u>_ framework [3]. For example, commonly used robots, such as KUKA LBR [4], [5], Universal Robots [6], ABB [7], Franka [8], have their _hardware interfaces_ freely available. Unfortunately, this is not the case for the Fanuc CRX Collaborative Robot Series. 

To the best of the authors’ knowledge, [9] is the only attempt to integrate Fanuc robots with ROS2. Such a package focuses on developing Python APIs integrated with ROS2 high-level actions. However, its Python implementation is not compatible with _ros2_ _<u>control</u>_ and hinders real-time performance. 

This work presents and validates the usage of the Fanuc CRX family within the _ros2_ _<u>control</u>_ framework. It describes the _hw_ _<u>interface</u>_ implementation based on the Ethernet IP communication protocol and its integration with ROS2 tools such as MoveIt2 [10] (see Figure 1). It also experimentally evaluates the control performance and discusses the limitations of the proposed approach. The additional material describes the open-source software packages available at https://github.com/paolofrance/ros2 <u>fanuc interface.</u> 

## II. PRELIMINARIES 

When developing a _hardware interface_ from scratch, it is essential to understand how a remote computer communicates with the robot controller. The Fanuc CRX robots are managed by the Fanuc R30iB Mini Plus controller, which allows for remote commands to the robot through two modalities, Remote Motion Interface (RMI) and Ethernet/IP (EIP). 

This work is currently under review in a IEEE journal 

2 

RMI allows control of the robot’s motion by sending commands from a remote PC to the controller in JSON format. A special teach pendant (TP) program appends and executes the instructions received from the remote PC to the TP program as soon as they are available. The TP program executes the commands sequentially, removing the ones already executed to let new ones incoming, with a buffer of eight slots. RMI communicates through TCP/IP socket messages. 

The EIP interface supports I/O exchange with the remote computer over an Ethernet network. EIP allows easy access to several Fanuc signals, including reading and writing numeric Registers (R), Position Registers (PR), and Digital Inputs (DI). 

RMI represents a powerful solution to use Fanuc functions remotely, but it is not meant for streaming position commands, and has a limited number of instructions available. Therefore, our hardware interface relies on the EIP interface. 

## III. ROS2-FANUC HARDWARE INTERFACE 

This section describes the main components of the ROS2 Fanuc interface; namely, how we use the Fanuc EIP interface to communicate with the robot and how the robot executes motion commands received from the external computer. 

## _A. Fanuc Ethernet/IP_ 

The Fanuc Ethernet/IP communication module provides a direct interface with the Fanuc R-30iB Mini Plus controller, enabling remote access to internal memory structures such as Registers (R) and Position Registers (PR). Position Registers serve as memory slots that can store either joint-space or Cartesian-space target poses. 

In the proposed control architecture, a ROS2-based driver running on an external computer communicates with the robot by writing desired target poses into PR[1], at a frequency specified by the _ros2_ _<u>control</u>_ hardware interface. The motion execution logic is implemented in a TP program on the Fanuc controller according to the value stored in PR[1]. 

The Ethernet/IP channel also continuously communicates the current robot position to the external computer and the states of digital signals. 

The Etherner/IP module also allows calling additional functionalities, such as controlling a tool-mounted gripper, that can be implemented using mapped registers. 

Examples of available ROS2 services implementing such features can be found in the _fanuc_ _<u>srvs</u>_ package described in the additional material attached to this paper. 

## _B. TP program_ 

The Hardware Interface requires a TP program running on the Fanuc controller to move the robot. The logic behind the basic TP program and hardware interface implementation is in Figure 2. 

The combination of the TP program and the ROS2 hardware interface works as follows: 

- 1) When started, the TP program resets Register R[1]. 


Fig. 2: Scheme of the interaction between the TP program running on the robot controller and ROS2 hardware interface developed in _ros2_ _<u>fanuc interface</u>_ . 

- 2) The TP program waits for R[1] to be set by the external computer, as a means to wait for the ROS2 hardware interface to be ready. This mechanism provides a straightforward interface for coordinating motion triggers from the external control system, ensuring that the hardware interface initializes with the current robot pose before sending commands. 

- 3) The hardware interface sets R[1]=1 at the end of the initialization procedure. Then, it continuously writes position commands to PR[1]. 

- 4) If R[1]==1, the TP program continuously commands the robot to move to the target joint position available in PR[1]. Using a CNT=100% motion instruction enables smooth trajectory execution. 

This register-based if-then-else structure of the TP program can be extended to use other registers to command other non-motion operations. For example, one may use R[2] to command the opening/closing of a gripper through a digital input signal. Several services, such as the gripper ones in the _fanuc_ _<u>srvs</u>_ , work according to this principle. 

## IV. PERFORMANCE EVALUATIONS 

To check the performance and usability of the developed hardware interface, we conducted experiments for four relevant tasks in industrial robotics: reaching a target point, tracking a trajectory, executing a collision-free trajectory, and dynamic velocity scaling. Experiments are performed with a Fanuc CRX-25iA communicating via Ethernet with a remote PC at a frequency of 25 _Hz_ . Position and velocity measurements were recorded at the ROS2 controller’s level, which means they include communication latency and ROS2’s possible computational overheads. Comparable results were observed with a CRX-10iA <u>L</u> and CRX-20iA <u>L</u> robots. 

## _A. Step response_ 

We measured the position step response of the robot controller. For this experiment, we requested the robot to move 

3 

TABLE I: Step responses (in degrees). 

|**Set Point [**°**]**|_tr_|_Ts_|%_OS_|_errss_|_tp_|
|---|---|---|---|---|---|
|30|0.51|0.90|0.00|0.00|1.15|
|45|0.64|1.10|0.00|0.00|1.35|
|90|1.22|1.79|0.00|0.00|2.12|


only the first joint _J_ 1 from a fixed nominal position, to three different setpoints, _sp_ = 30° _,_ 45° _,_ 90°. 

We evaluate standard performance indicators such as rise time _tr_ , settling time _Ts_ , overshoot percentage % _OS_ , steady state error _errss_ , and peak time _tp_ . Results are in Table I and Figures 3a, 3b, and 3c. 

As expected, _tr_ and _Ts_ depend on the step amplitude. Moreover, _Ts_ is also influenced by the joint velocity limits enforced by the Fanuc controller. This is visible in Figures 3b and 3c, where the measured velocity (dotted black line) saturates at about 60°, increasing the rise time. Interestingly, the robot does not present any overshoots and shows negligible steadystate error. Therefore, _tp_ coincides with the time required to reach the set point. 

TABLE II: Path and trajectory tracking error results. 

||**_f_ [Hz]**|**MAE**|**RMSE**|**Max Error**|
|---|---|---|---|---|
|trajectory|0.1|3.72|4.34|6.67|
|trkin|0.25|7.77|9.96|17.03|
|acg|0.5|18.26|22.57|36.70|
|path|0.1|0.36|0.42|0.87|
|flli|0.25|0.41|0.49|1.91|
|oowng|0.5|5.22|5.68|8.78|


measured when the command changes from zero to _ref_ ( _t_ ). In this case, the robot should have a non-zero velocity and must adhere to physical constraints. The path errors are in the bottom rows of Table II and in Figure 3g, 3h, and 3i. 

_3) Time delay:_ We measured the time delay between the command and feedback, as well as the allowed control frequency. Relying on the sinusoidal commands, we computed the cross-correlation to obtain the lag, for the first two cases ( _f_ = _{_ 0 _._ 1 _,_ 0 _._ 25 _}Hz_ ). Then we measured the average cycle time to obtain the time delay and control frequency. The time delay varies a little between the cases, with an average value of about 0 _._ 31 _s_ , and a control frequency of about 24 _Hz_ , which is in line with Fanuc’s EIP specifications. 

## _B. Trajectory tracking_ 

To measure the tracking capabilities of the hardware interface, we streamed sinusoidal reference trajectories, _ref_ ( _t_ ) = _A_ sin(2 _πft_ ), with amplitude _A_ = 30° and frequencies _f ∈ {_ 0 _._ 1 _,_ 0 _._ 25 _,_ 0 _._ 5 _} Hz_ . Also, for this experiment, we requested the robot to move only the first joint. We evaluate the tracking error and the path following error. 

_1) Trajectory tracking error:_ For each frequency, we measured the Mean Absolute Error MAE = _n_ <u>1</u> � _ni_ =1<sup>_|q_fb</sup><sup>_,i −_</sup><sup>_<u>q</u>_cmd</sup><sup>_<u>,i|</u>_,</sup> the Root Mean Squared Error RMSE = ~~�~~ _n_ <u>1 �</u> _ni_ =1<sup>(</sup><sup>_q_fb</sup><sup>_,i −q_cmd</sup><sup>_,i_)2,andtheMaximum</sup> Error = max _i∈{_ 1 _,...,n} |q_ fb _,i − q_ cmd _,i|_ , where _q_ cmd and _q_ fb are the position command and feedback signals for the selected joint, and _n_ is the number of measurements. 

The results are in Table II and Figures 3d, 3e, and 3f 

The upper rows of Table II highlight that the average and maximum errors increase with frequency. In particular, in the case of high frequency, this is due to the joint velocity limits intrinsic in the Fanuc robots. This is visible in Figure 3f, where the velocity profile (dotted line) saturates around _±_ 60°. 

_2) Path following error:_ Tracking errors are mainly caused by the communication latency between the controller command and the robot movement. It is meaningful to measure path following performance, i.e., the control error between the command and feedback signals after time synchronization. 

The sinchronized signals are obtained by computing the cross-correlation, _Rq_ cmd _,q_ fb[ _τ_ ] =<sup>�</sup><sup>_n_</sup> _i_ =0<sup>_−_1</sup><sup>_q_cmd[</sup><sup>_i_]</sup><sup>_·q_fb[</sup><sup>_i_+</sup><sup>_τ_],</sup> between the command and feedback signals. We then find the lag _τ_<sup>_∗_</sup> that maximizes cross-correlation between the two signals. We apply the same metrics of the trajectory tracking case to the error signal given by _q_ cmd[ _i_ ] and _q_ fb[ _i_ + _τ_<sup>_∗_</sup> ]. In this case, for the low-frequency cases ( _f_ = _{_ 0 _._ 1 _,_ 0 _._ 25 _}Hz_ ), the errors dramatically decrease, with averages below 1°. As for the higher frequency, _f_ = 0 _._ 5 _Hz_ , the velocity of the joint saturates, and the resulting error remains large, leading to poor path following. The maximum error is 

## _C. Obstacle avoidance_ 

We assessed the correct execution of collision-free trajectories via Moveit2 [10] through the experiment shown in Figure 1. The robot has to move from an initial to a goal configuration by avoiding a box-shaped obstacle. The trajectory is computed with the BiTRRT motion planner, with a velocity scaling of 0.1. The executed trajectory is in Figure 4. The plots confirm the results obtained in the previous experiments in terms of trajectory tracking and path following. 

## _D. Dynamic velocity scaling_ 

We used the proposed hardware interface to implement online velocity scaling during trajectory execution. In the proposed experiment, a trajectory is computed with Moveit2 to move the first joint from _−_ 45° to 45°, maintaining the other joints fixed. The speed override is manually set to 10% _,_ 50% _,_ 100%. Figure 5 shows the command and feedback signals, as well as the override values. This experiment used a custom ROS2 controller, named _scaled_ _<u>fjt controller</u>_ , based on [11], [12] and available here [13]. 

We used this feature for safe human-robot interaction and human-robot collaborative transport applications. Detailed experiments of human-robot collaborative transport can be found in [14], where the proposed _ros2_ _<u>fanuc interface</u>_ is used in combination with the _scaled_ _<u>fjt controller</u>_ to adapt trajectory execution based on interaction forces. 

## _E. Limitations_ 

Closed-loop control is limited by the latency. We attempted to implement force and admittance control, but achieved unsatisfactory results, as the delay led to unstable behaviors. To implement feedback control on an external computer, we performed preliminary tests exploiting the Dynamic Path Modification (DPM) function of the Fanuc robots, but its 

4 


Fig. 3: Results of the step responses (top), trajectory tracking (middle), and path following (bottom). 


Fig. 4: Command and feedback signals during execution of Moveit2 computed trajectory with obstacle avoidance. 

integration in the _ros_ _<u>control</u>_ is not straightforward and left as a future work. 

The _ros2_ _<u>fanuc interface</u>_ does not enforce joint velocity limits. This means that large velocity commands may be clamped by the Fanuc controller. For this reason, careful attention must be paid to the robot controller’s settings, as the Fanuc controller may enforce Cartesian speed limits of around 250 mm/s in the collaborative mode. This may lead to unexpected joint speed clamping during execution. 


Fig. 5: Command and feedback signals with dynamic velocity scaling during trajectory execution. The speed override is set dynamically via ros topic. 

## V. CONCLUSIONS 

We presented the implementation and performance evaluation of the ROS2 Fanuc CRX hardware interface. We experimentally highlighted the strengths and limitations of the real-time control and communication framework based on the Fanuc Ethernet-IP module. Despite the limited applicability to high-frequency closed-loop control, experiments show good results in setpoint reaching, path following, collision avoidance, and dynamic velocity modification. Future works will explore other Fanuc control functions, such as the Dynamic Path Modification (DPM), to reduce communication latency. 

5 

## REFERENCES 

- [1] A. Bonci, F. Gaudeni, M. C. Giannini, and S. Longhi, “Robot operating system 2 (ros2)-based frameworks for increasing robot autonomy: A survey,” _applied sciences_ , vol. 13, no. 23, p. 12796, 2023. 

- [2] S. Chitta, E. Marder-Eppstein, W. Meeussen, V. Pradeep, A. R. Tsouroukdissian, J. Bohren, D. Coleman, B. Magyar, G. Raiola, M. L¨udtke, and E. F. Perdomo, “ros <u>control:</u> A generic and simple control framework for ros,” _Journal of Open Source Software_ , vol. 2, no. 20, p. 456, 2017. [Online]. Available: https://doi.org/10.21105/joss.00456 

- [3] S. Macenski, T. Foote, B. Gerkey, C. Lalancette, and W. Woodall, “Robot operating system 2: Design, architecture, and uses in the wild,” _Science Robotics_ , vol. 7, no. 66, p. eabm6074, 2022. [Online]. Available: https://www.science.org/doi/abs/10.1126/scirobotics.abm6074 

- [4] M. Huber, C. E. Mower, S. Ourselin, T. Vercauteren, and C. Bergeles, “Lbr-stack: Ros 2 and python integration of kuka fri for med and iiwa robots,” _Journal of Open Source Software_ , vol. 9, no. 103, p. 6138, 2024. [Online]. Available: https://doi.org/10.21105/joss.06138 

- [5] ICube-Robotics, “Iiwa <u>ros2,”</u> https://github.com/ICube-Robotics/iiwa ros2, accessed: 2025-06-06. 

- [6] UniversalRobots, “Universal <u>robots ros2 driver,”</u> https://github.com/ UniversalRobots/Universal <u>Robots ROS2 Driver,</u> accessed: 2025-0606. 

- [7] PickNikRobotics, “abb <u>ros2,”</u> https://github.com/PickNikRobotics/abb ros2, accessed: 2025-06-06. 

- [8] frankaemika, “franka <u>ros2,”</u> https://github.com/frankaemika/franka ros2, accessed: 2025-06-06. 

- [9] UofI-CDACS, “fanuc <u>ros2 drivers,”</u> https://github.com/UofI-CDACS/ fanuc <u>ros2 drivers,</u> accessed: 2025-06-06. 

- [10] D. Coleman, I. Sucan, S. Chitta, and N. Correll, “Reducing the barrier to entry of complex robotic software: a moveit! case study,” _ournal of Software Engineering for Robotics_ , 2014. 

- [11] M. Faroni, M. Beschi, N. Pedrocchi, and A. Visioli, “Predictive inverse kinematics for redundant manipulators with task scaling and kinematic constraints,” _IEEE Transactions on Robotics_ , vol. 35, no. 1, pp. 278–285, 2019. 

- [12] M. Faroni, M. Beschi, and N. Pedrocchi, “An mpc framework for online motion planning in human-robot collaborative tasks,” in _2019 24th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA)_ , 2019, pp. 1555–1558. 

- [13] paolofrance, “scaled <u>fjt controller,”</u> https://github.com/paolofrance/ scaled <u>fjt controller,</u> accessed: 2025-06-06. 

- [14] P. Franceschi, A. Bussolan, V. Pomponi, O. Avram, S. Baraldo, and A. Valente, “Human-robot collaborative transport personalization via dynamic movement primitives and velocity scaling,” 2025. [Online]. Available: https://arxiv.org/abs/2506.09697 

1 

## Description of Supplementary Materials 

|**File / Resource**|**Description**|
|---|---|
|**Core Folders**||
|TP_programs/|Basic TP programs enabling communication and motion of the real Fanuc robot. Must be running before<br>launching the hardware interface.|
|crx_description/|Contains URDF, XACRO, and mesh files for the robot model. Easily customizable for different cell layouts.|
|crx_moveit_config/|MoveIt2 configuration package for planning and execution. It should be adjusted for new scenes.|
|fanuc_control/|Core hardware interface logic implementation for robot communication and control.|
|fanuc_eth_ip/|Implements Ethernet/IP communication between PC and Fanuc controller.|
|fanuc_rmi/|RMI communication alternative (EXPERIMENTAL). Limited testing; included for advanced users.|
|fanuc_srvs/<br>experiments/|ROS2 service examples for I/O control (e.g., Robotiq gripper). Requires additional robot-side logic.<br>Python scripts to reproduce the experiments:<br>step_response.py – step response<br>sinusoidal_traj.py – sinusoidal trajectory<br>add_obstacle.py – add obstacle in MoveIt2 scene|
|**Launch Parameters**||
|robot_type|One of [crx5ia, ..., crx30ia]; model of the CRX robot.|
|use_mock_hardware|true/false – Enables virtual vs. real robot control. If true, it integrates a fake hardware interface with<br>MoveIt2/RViz.|
|controllers_file|Path to the YAML configuration file for ROS2 controllers.|
|robot_ip|IP address of the physical robot (required if not using mock hardware).|
|read_only|true/false – Enables passive state monitoring without running a TP program.|
|use_rmi|true/false – EXPERIMENTAL; enables RMI instead of Ethernet/IP.|
|**Available Topics**||
|/cmd_j_pos|Joint command input topic fromros2_controllers. Converts radians to degrees and accounts for J2/J3<br>coupling.|
|/fb_j_pos|Joint state feedback including positions and velocities (same conversion as above).|
|/fb_c_pos|Cartesian feedback from the Fanuc controller. Format: _{_x, y, z, Rx, Ry, Rz_}_; units: mm and degrees.|
|**System Requirements**||
|Ubuntu 22.04|Target operating system.|
|ROS 2 Humble|Target ROS version.|
|ROS packages|ros-humble-ros2-control, ros-humble-moveit.|
|EIPScanner|Library required for Ethernet/IP communication with the Fanuc controller.|
|ros2<br>fanuc<br>interface|Main ROS2 package containing robot interface code.|
|scaled<br>fjt<br>controller|Velocity-scaled controller used during experiments.|
|**Reproducing the Experiments**||
|Launch robot|ros2 launch fanuc_control robot_bringup.launch.py<br>robot_ip:=your.robot.ip.address<br>robot_type:=crx25ia<br>controllers_file:=scaled_velocity_controller.yaml|
|Step response|python experiments/scripts/step_response.py|
|Trajectory following|python experiments/scripts/sinusoidal_traj.py|
|Obstacle avoidance|python experiments/scripts/add_obstacle.py, then move robot in GUI|
|Velocity scaling|ros2 topic pub /speed_ovr std_msgs/msg/Int16 "_{_data: vel_scale_}_"<br>where<br>vel_scale_∈_[0_,_100]|


