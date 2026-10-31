---
title: "A ROS2 Interface for Universal Robots Collaborative Manipulators Based on ur_rtde"
date: "2025-11-21"
authors: "Alessio Saccuti; Riccardo Monica; Jacopo Aleotti"
url: https://arxiv.org/abs/2511.17237
pdf: https://arxiv.org/pdf/2511.17237
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.17237)** / [論文ページ](https://arxiv.org/abs/2511.17237)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# A ROS2 Interface for Universal Robots Collaborative Manipulators Based on ur <u>rtde</u> 

Alessio Saccuti, Riccardo Monica, Jacopo Aleotti _Department of Engineering and Architecture, University of Parma, Parma, Italy {_ alessio.saccuti,riccardo.monica,jacopo.aleotti _}_ @unipr.it 

**_Abstract_ —In this paper a novel ROS2 driver for UR robot manipulators is presented, based on the ur_rtde C++ library. The proposed driver aims to be a flexible solution, adaptable to a wide range of applications. The driver exposes the high-level commands of Universal Robots URScripts, and custom commands can be added using a plugin system. Several commands have been implemented, including motion execution along a waypoint-based path. The driver is published as open source.** 

**_Index Terms_ —Software Architecture for Robotic and Automation, Collaborative Robots in Manufacturing.** 

additional commands can be added to the driver, if needed, by leveraging a plugin system. The proposed solution aims at providing a flexible driver, designed for easy adaptation to a wide range of applications, including academic research. 

In summary, the contributions of this work are: 

- a ROS2 interface for Universal Robot cobots based on ur_rtde that exposes high-level URScript commands 

- the proposed driver is a more flexible alternative to ur_robot_driver thanks to a plugin system 

- the source code is published as open source<sup>1</sup> 

## I. INTRODUCTION 

Collaborative robots have become widely adopted due to their flexibility and safety in human-robot interactions. Universal Robots (UR) is one of the leading manufacturers of collaborative manipulators. UR robots can be programmed using URScript, a custom language developed by Universal Robots and executed on the robot controller. URScript provides several high-level commands like, for example, linear motion to a point ( _moveL_ ). UR robots can also be controlled remotely with various communication interfaces like the RealTime Data Exchange interface (RTDE) [1], which allows external applications to communicate with the robot controller over a TCP/IP connection. Real-time communication is achieved using a message exchange protocol where the robot sends its status at each control cycle (up to 500 Hz) and the external application can change the value of robot controller registers. 

As RTDE is a low level communication protocol, high-level software libraries have been developed to enable advanced robot commands, such as executing trajectories. The official library published by Universal Robot supporting RTDE is ur_client_library [2], which was used to develop the official ROS2 driver for UR robots: ur_robot_driver [3]. The ur_client_library, and in turn ur_robot_driver, offer a rather low level of abstraction where highlevel URScript commands (like _moveL_ ) are not exposed. Those commands are accessible only by sending custom URScript snippets to the robot. 

This paper proposes ur_ros_rtde, a novel ROS 2 driver for Universal Robots. Unlike the official ROS2 driver, the proposed solution is built on the ur_rtde C++ library [4], a RTDE interface that operates at a higher level of abstraction than ur_client_library. By leveraging ur_rtde, ur_ros_rtde exposes the high-level URScript commands as ROS2 action servers. Other commands have been implemented as a composition of URScript instructions. Moreover, 

## II. RELATED WORK 

The Universal Robots RTDE communication interface is well-known in literature and it was used in several works. In [5] and [6] RTDE was adopted to control UR cobots. In [7], [8], and [9], the RTDE interface was used only for data acquisition. 

To facilitate the development of external applications for UR cobots, various higher-level software interfaces and drivers have been proposed based on RTDE. In addition to the official software interface by Universal Robots (ur_client_library), a few alternatives have been developed by thirdparties. One of these software interfaces is ur_rtde [4] by SDU Robotics, which was used in this work. Another similar interface is python-urx [10], which is a Python interface for tasks that do not require high control frequency. A C# software interface is provided in _UnderAutomation_ [11]. 

To the best of our knowledge, the only ROS2 driver currently available is the official Universal Robot driver ur_robot_driver. Unlike the driver proposed in this work, in ur_robot_driver most high-level URScript commands are accessible only through the low-level transmission of custom URScript snippets to the robot. Also, there is no mechanism to verify the correctness of the snippet or to obtain feedback after execution. Indeed, in previous works [12] [13] [14] [15] [16] only default functionalities of the driver were used like accessing robot state or executing trajectories. Another disadvantage of ur_robot_driver is that it requires a program running on the robot controller. In particular, the _External Control URCap_ package must be installed and running to control the robot. 

In this work ur_rtde was preferred over ur_client_library and python-urx due to its ease of use and the 

1https://github.com/SuperDiodo/ur_ros_rtde.git 

2 


Fig. 1: Diagram of ur_ros_rtde. 

native availability of high-level URScript commands. Moreover, the ur_rtde software interface does not depend on the _External Control URCap_ , even if it is compatible with it. The ease of use of ur_rtde and its usefulness are evident given the number of works where it has been employed [17] [18] [19] [20] [21] [22] [23]. However, no ROS2 interface for ur_rtde is currently available, other than the one proposed in this paper. 

## III. SOFTWARE DESCRIPTION 

The proposed software architecture is summarized in Fig. 1. The proposed driver includes three ROS2 nodes: _RobotStateReceiver_ , _CommandServer_ , and _DashBoardServer_ . All three nodes (summarized in Section III-A) use the ur_rtde interface for communication with the robot. The _RobotStateReceiver_ node retrieves the robot state (Section III-B). The _CommandServer_ and _DashBoardServer_ nodes expose ROS2 actions to send high-level commands to the robot, and they can be extended using the plugin system of ur_ros_rtde (Section III-C). More advanced plugins which extend the robot control script can also be created (Section III-D). 

## _A. Overview of ur_rtde_ 

The ur_rtde interface by SDU Robotics is a C++ library with Python bindings for controlling UR cobots over RTDE. The library has a modular structure where each module (called “interface” by the developers) exposes a subset of the robot functionalities. Four modules of ur_rtde are used in this work: the _RTDE Control_ interface, which sends motion commands; the _RTDE Receive_ interface, which is used for retrieving the current robot state; the _RTDE IO_ interface, which handles the robot I/O pins; and the _Dashboard Client_ interface, which can be used to send commands to the teach pendant GUI remotely. Each module is represented by a main class, which can be instantiated independently from the others. 

Among the listed modules, only the _RTDE Control_ interface requires a control script running on the robot. The control script is automatically uploaded to the robot controller when the _RTDE Control_ class is instantiated, without requiring any installation on the robot, unlike the official ur_robot_driver. Nonetheless, the _RTDE Control_ interface is still compatible with the official _External Control URCap_ control 

TABLE I: Topics and services advertised by the _RobotStateReceiver_ . 

|**Type**|**Topic**|**Service**|
|---|---|---|
|Joint state|/joint_states|/get_joint_state|
|TCP pose|/tcp_pose|/get_tcp_pose|
|Wrench|/wrench|/get_wrench|
|IO state|/io_state|/get_io_state|


script if it is already running on the robot. To prevent conflicts, at any time only one instance of the _RTDE Control_ interface can be connected to the robot, unlike the other interfaces. 

The RTDE protocol is a real-time protocol which operates on a TCP connection, synchronized with the internal robot control loop. The RTDE protocol defines input and output registers, which correspond to variables residing in the robot controller memory. Registers are used by the _RTDE Control_ interface for communication with the script running on the robot controller. At each control loop, the current value of the output registers is sent by the robot controller to the connected client. Some output registers have pre-defined meaning and they contain information about the current robot state (e.g., joint angles). Other output registers can be configured, and can be used for custom communication from the script running on the controller to the client. Similarly, the client can send messages through the TCP connection to change the value of the configurable input registers. 

In order to execute a command on the robot, _RTDE Control_ sets a specific input register to the index of that command. At each control loop iteration, in the process_cmd function, the control script uses the value of the input register to select the command to be executed on that iteration. Command parameters are passed using other input registers, and results are returned using output registers. 

## _B. Retrieving the robot state_ 

The ROS2 interface to access the current robot state is provided by the _RobotStateReceiver_ node of ur_ros_rtde. The node was designed to depend only on the _RTDE Receive_ interface of ur_rtde. Hence, it does not require a control script running on the robot controller, and it does not interfere with other operations on the robot. Any number of _RobotStateReceiver_ nodes may be running to monitor the robot state, potentially on different physical machines. 

The _RobotStateReceiver_ node uses the _RTDE Receive_ interface to iteratively read the robot state with a configurable frequency. The robot state includes data such as joint positions, forces and torques. At each iteration, each component of the robot state is published to a ROS2 topic, in the standard format, if available. Moreover, the last robot state is also stored in the node. The stored robot state can be accessed at any time by calling a service (Table I). 

The joints’ positions and velocities are published to the joint_states topic, following the naming convention adopted in software such as MoveIt! [24] and RViz [25]. The tcp_pose topic contains the current pose of the tool contact point (TCP), which is defined using the teach pendant in the 

3 

Fig. 2: Digital twin of a UR cobot. 

installation phase of the robot. The wrench topic provides information about the force and the torque read by the robot force-torque sensor. The io_state topic reports the state of the robot and controller I/O digital pins. 

The joint_states topic can be provided as input to a standard robot_state_publisher ROS2 node. Hence, a digital twin simulation of the robot can be displayed in RViz (Figure 2). The robot_state_publisher node must be configured using the UR cobot URDF (Unified Robot Description Format) description. However, unlike the official ur_robot_driver, ur_ros_rtde by itself does not depend directly on an URDF for accessing the robot state. The _RobotStateReceiver_ provides a service for pausing the retrieval of the actual robot joints’ positions to temporarily display a custom robot configuration. In this case, the last joint positions are published to the joint_states topic and the joints’ positions can be updated externally by sending a message to the fake_joint_states topic. 

## _C. Robot commands and plugin system_ 

The _CommandServer_ and _DashBoardServer_ nodes expose ROS2 actions to send high-level commands to the robot. The _CommandServer_ is designed to implement high-level commands. Instead, the _DashBoardServer_ implements commands which only use the _Dashboard Client_ interface. The two nodes leverage a flexible plugin system where each plugin exposes different action servers. All plugins are loaded using the ROS2 plugin system. The plugins share the same instance of the ur_rtde interface, hence only one connection (for each node) is created. 

Three types of plugins were defined: the _command_ and _extension_ plugins extend the _CommandServer_ node, and the _dashboard_ plugins extends the _DashBoardServer_ . Each plugin must implement the _start_ _<u>action server</u>_ method, where the plugin should initialize itself, for example by creating an action server. To speed-up the definition of many action servers, a simplified templated C++ action server implementation is also provided within ur_ros_rtde. Plugins with the _command_ interface can access the common instance of the _RTDE Receive_ , _RTDE Control_ , _RTDE IO_ and _Dashboard Client_ interfaces of ur_rtde. The _dashboard_ plugins can only access the _Dashboard Client_ interface. The _extension_ plugins extend the robot control script (Section III-D). 

More than 40 plugins have already been implemented in ur_ros_rtde. Each plugin instantiates a single ROS2 action server, with a custom action type with the command input parameters and output values. In most plugins, the action 

Fig. 3: Snippet for OnRobot _sg_ _<u>grip</u>_ method (yellow background) and corresponding C++ code (blue background). 

callback simply calls a high-level command by ur_rtde and returns the results. Examples are the _moveJ_ command, which allows linear movement of the robot in joint space, and the _moveUntilContact_ command, which moves the robot at constant speed until a collision is detected. 

A notable plugin is _ExecuteTrajectory_ , which allows the execution of a motion along a path described by a sequence of waypoints. To accomplish this, the _ExecuteTrajectory_ integrates a trajectory planner and a control loop based on the _servoJ_ function of ur_rtde. Execution of a motion given a path is not present in ur_robot_driver, where a timeparameterized trajectory must always be provided instead. 

## _D. Extending the ur_rtde control script_ 

Plugins of the _extension_ type are used to extend the control script running on the robot, so that custom instructions can be called by ur_ros_rtde. For example, add-on devices such as robot grippers often require software extensions, called URCaps, to be installed on the robot controller. URCaps typically provide custom instructions which are not part of standard URScript. The interface of _extension_ -type plugins requires the implementation of a method which returns the changes to be applied to the control script. The changes should include a URScript code snippet with the custom instructions to be executed. Also, the changes may include a preamble to be added to the URScript header. 

The ur_ros_rtde _CommandServer_ assigns a non-zero unique ID to each _extension_ plugin. The code snippet of each plugin is added in the control script process_cmd function so that, when input register 18 contains one of the unique IDs, the corresponding snippet is executed. The input float register 18 was chosen for this purpose, as it is not used by the unmodified ur_rtde interface. The output float register 18 is used to signal the completion of the snippet execution. Hence, C++ code in the plugin can trigger the snippet by setting input register 18 to its own unique ID. Then, the code can wait for end of execution by monitoring output register 18. 

Fig. 3 illustrates an example URScript snippet to close an OnRobot soft gripper, and the corresponding C++ code to trigger the snippet. The C++ code first sets the target gripper width in integer input register 19, and then triggers the snippet by setting register 18 to its unique ID (256 in this case). The snippet uses the _sg_ _<u>grip</u>_ command provided by the OnRobot 

4 


Fig. 4: Forces (top) and joints’ velocities (bottom) in the experiment with the _MoveDownUntilForce_ plugin. Blue and red dots highlight the instants in which the force exceeded the threshold. At the first two instants (blue dots) the force was ignored since the force direction is not along the flange Z-axis. 

URCap to close the gripper to the value in input register 19. After the execution of the command, the snippet stores the reached gripper width into output register 19 and signals end of execution using output register 18. Hence, the C++ code can wait for end of execution using register 18 and then retrieve the gripper width from register 19. 

## IV. EXAMPLE OF A CUSTOM PLUGIN 

The plugin system of ur_ros_rtde can be leveraged to create custom commands for specific use cases. As an example, the _MoveDownUntilForce_ plugin provides an action which moves the end-effector vertically until a force above a threshold is detected along the flange Z-axis. The action is useful, for example, when placing an object on a surface. The plugin overcomes a limitation of the similar _moveUntilContact_ function of ur_rtde, where the threshold is not configurable. 

Listing 1 shows the content of the action callback. First, the force-torque sensor is reset (Line 1). In Line 2, the _RTDE Receive_ interface is used to obtain the robot current pose, which is then used to compute the target pose by adding a vertical offset of 1 meter. The command _moveL_ (Line 4) starts the linear movement of the robot to the target point. During the movement a loop retrieves the current force measured by the robot force-torque sensor (Lines 5-10). When a force of 20 N is detected along the flange Z-axis (Line 7), the robot is stopped using the _stopJ_ command (Line 8). The example is provided in the driver repository within the ur_ros_rtde_tutorials package. 


Fig. 4 displays the force detected by the robot and the joints’ velocities in a test experiment of the plugin. As expected, the robot continued the motion until a force along the flange Z-axis exceeded the threshold. Then, the joint velocities dropped to zero, stopping the robot. Horizontal forces along the X and Y axes, applied by hand to interfere with the robot, were ignored. 

For comparison, the same task was implemented in a separate ROS2 node using the ur_robot_driver. Due to the verbosity of ROS2, only a pseudocode of the implementation is shown in Listing 2. 

At Line 2, the force-torque sensor is reset by calling a service. At Lines 3 and 4, topics are subscribed to update the force_z and speed variables, which represent the vertical force measured by the robot force-torque sensor and the actual joint speeds, respectively. As the high-level _moveL_ and _stopJ_ commands are not available in ur_robot_driver, code snippets containing the commands are defined at Lines 5–10. The robot starts moving at Line 13, when the URScript snippet containing _moveL_ is sent. The process then waits until a vertical force of 20 N is detected (Line 14). When the vertical force read by the robot exceeds the threshold the robot is stopped by sending the snippet containing the _stopJ_ command (Line 15). As there is no mechanism to wait for the end of a snippet, the node cannot determine when the stop command ends. Hence, at Line 16, the process waits until the robot joint velocities drop below a given threshold. Finally, the _External Control URCap_ must be restarted (Line 17) due to a further limitation of ur_robot_driver where URScript snippets stop programs running on the robot controller. 


Listing 2: Implementation of a custom command similar to _MoveDownUntilForce_ , using ur_robot_driver. 

The implementation of Listing 2 shows that several workarounds are needed to use the ur_robot_driver. Indeed, high-level commands are accessible only through URScript snippets and also do not provide feedback after execution. Instead, a plugin on ur_ros_rtde can access the high-level commands of the ur_rtde directly. Moreover, access to ur_robot_driver is done through messages and services, which have higher overhead than the ur_rtde interface. Hence, the implementation of critical control tasks as ur_ros_rtde plugins may be preferable. 

## V. CONCLUSION 

This paper presented ur_ros_rtde, a novel ROS2 driver for Universal Robots. Unlike the official ur_robot_driver, the proposed driver exposes high-level URScript 

Listing 1: Action callback of the _MoveDownUntilForce_ plugin. 

5 

commands, and custom commands can be added by leveraging a plugin system. The driver is published as open source, with several plugins already implemented, including motion along a sequence of waypoints. A comparison against the implementation of custom commands using ur_robot_driver was also reported. 

## REFERENCES 

- [1] U. Robot, “Rtde,” https://www.universal-robots.com/articles/ur/ interface-communication/real-time-data-exchange-rtde-guide. 

- [2] U. Robots, “ur <u>client library,”</u> https://github.com/UniversalRobots/ Universal <u>Robots Client Library.</u> 

- [3] ——, “ur <u>ros2 driver,”</u> https://github.com/UniversalRobots/Universal Robots <u>ROS2 Driver.</u> 

- [4] A. P. Lindvig, I. Iturrate, U. Kindler, and C. Sloth, “ur <u>rtde: An interface</u> for controlling universal robots (ur) using the real-time data exchange (rtde),” in _IEEE/SICE International Symposium on System Integration (SII)_ , 2025, pp. 1118–1123. 

- [5] U. M. U. Zakaria, S. M. Mustaza, M. H. M. Zaman, and A. A. A. Rahni, “Development of real-time contact force control of a collaborative robot for automated ultrasound scanning,” in _IEEE-EMBS Conference on Biomedical Engineering and Sciences (IECBES)_ , 2022, pp. 334–337. 

- [6] S. Kumar, S. Arora, and F. Sahin, “Speed and separation monitoring using on-robot time-of-flight laser-ranging sensor arrays,” in _IEEE 15th International Conference on Automation Science and Engineering (CASE)_ , 2019, pp. 1684–1691. 

   - [19] Y. Shi, Z. Chen, Y. Wu, D. Henkel, S. Riedel, H. Liu, Q. Feng, and J. Zhang, “Combining learning from demonstration with learning by exploration to facilitate contact-rich tasks,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2021, pp. 1062– 1069. 

   - [20] Y. Shi, C. Yuan, A. Tsitos, L. Cong, H. Hadjar, Z. Chen, and J. Zhang, “A sim-to-real learning-based framework for contact-rich assembly by utilizing cyclegan and force control,” _IEEE Transactions on Cognitive and Developmental Systems_ , vol. 15, no. 4, pp. 2144–2155, 2023. 

   - [21] Z. Cheng, A. S. Zeltner, A. T. Arsvold,<sup>˚</sup> K. L. Schwaner, P. T. Jensen, and T. R. Savarimuthu, “Active search of subsurface lymph nodes using robot-assisted electrical impedance scanning,” _IEEE Transactions on Instrumentation and Measurement_ , vol. 71, pp. 1–11, 2022. 

   - [22] D. Wu, J. Jiang, J. Pan, K. Qian, and Z. Xue, “Root Canal Preparation Robot Based on Guiding Strategy for Safe Remote Therapy: System Design and Feasibility Study (2023),” _IEEE/ASME Transactions on Mechatronics_ , vol. 30, no. 1, pp. 84–95, 2025. 

   - [23] J. Lee, E. Quist, S. German, M. Kim, and N. Fisher, “Neural network model of efast target prediction for robotic ultrasound diagnostics in austere environments,” in _19th International Conference on Ubiquitous Robots (UR)_ , 2022, pp. 153–158. 

   - [24] Ioan A. Sucan and Sachin Chitta, “Moveit.” [Online]. Available: moveit.ros.org 

   - [25] H. R. Kam, S.-H. Lee, T. Park, and C.-H. Kim, “Rviz: a toolkit for real domain data visualization,” _Telecommunication Systems_ , vol. 60, pp. 337–345, 2015. 

- [7] E. S. Kolvig-Raun, M. B. Kjærgaard, and R. Brorsen, “Joint stress estimation and remaining useful life prediction for collaborative robots to support predictive maintenance,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 4, pp. 3554–3561, 2024. 

- [8] ——, “Edde: An event-driven data exchange to accurately introspect cobot applications,” in _IEEE/ACM 5th International Workshop on Robotics Software Engineering (RoSE)_ , 2023, pp. 25–30. 

- [9] R. J. Kirschner, A. Kurdas, K. Karacan, P. Junge, S. A. Baradaran Birjandi, N. Mansfeld, S. Abdolshah, and S. Haddadin, “Towards a reference framework for tactile robot performance and safety benchmarking,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2021, pp. 4290–4297. 

- [10] O. Roulet-Dubonnet, “python-urx,” https://github.com/ SintefManufacturing/python-urx. 

- [11] UnderAutomation, “Underautomation,” https://github.com/ underautomation/UniversalRobots.NET. 

- [12] B. Cosmin, A. Alexandru, and T. Sorin, “Controlling industrial robots with simulink,” in _15th International Conference on Electronics, Computers and Artificial Intelligence (ECAI)_ , 2023, pp. 1–4. 

- [13] K. T. T. Moyo, J. V. S. Luces, A. A. Ravankar, Y. Hirata, and M. Shota, “Enhancing manipulator flexibility: Real-time positional control for variable assembly environments using apriltag markers and edge detection,” in _IEEE 20th International Conference on Automation Science and Engineering (CASE)_ , 2024, pp. 3932–3939. 

- [14] S. Ryu, J. Jung, B. Song, and J. Shin, “Development of robot applications utilizing asset administration shell for integrated robotics processes,” in _IEEE 29th International Conference on Emerging Technologies and Factory Automation (ETFA)_ , 2024, pp. 1–4. 

- [15] F. H. N. Nascimento, S. A. Cardoso, A. M. N. Lima, and D. F. S. Santos, “Synchronizing a collaborative arm’s digital twin in real-time,” in _Latin American Robotics Symposium (LARS), Brazilian Symposium on Robotics (SBR), and Workshop on Robotics in Education (WRE)_ , 2023, pp. 230–235. 

- [16] C. Fernando, D. Olds, S. I. Campbell, and P. M. Maffettone, “Facile integration of robots into experimental orchestration at scientific user facilities,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2024, pp. 9578–9584. 

- [17] J. Halim, P. Eichler, S. Krusche, M. Bdiwi, and S. Ihlenfeldt, “A hybrid approach of no-code robot programming for agile production: Integrating finger-gesture and point cloud,” in _33rd IEEE International Conference on Robot and Human Interactive Communication (ROMAN)_ , 2024, pp. 732–739. 

- [18] S. Hosseini and I. Hahn, “On Experimental Energy Consumption Estimation of a 6-DoF Industrial UR3e Robot Arm Manipulator in Trajectory Planning,” in _33rd IEEE International Conference on Robot and Human Interactive Communication (ROMAN)_ , 2024, pp. 1430– 1435. 

