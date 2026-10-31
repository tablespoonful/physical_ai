---
title: "Synchronizing Machine Learning Algorithms, Realtime Robotic Control and Simulated Environment with o80"
date: "2023-06-16"
authors: "Vincent Berenz; Felix Widmaier; Simon Guist; Bernhard Schölkopf; Dieter Büchler"
url: https://arxiv.org/abs/2306.09764
pdf: https://arxiv.org/pdf/2306.09764
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2306.09764)** / [論文ページ](https://arxiv.org/abs/2306.09764)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Synchronizing Machine Learning Algorithms, Realtime Robotic Control and Simulated Environment with o80 

Vincent Berenz, Felix Widmaier, Simon Guist, Bernhard Sch¨olkopf and Dieter B¨uchler Max Planck Institute for Intelligent Systems, T¨ubingen, Germany 


(work presented at the Robot Software Architectures Workshop - RSA 2023, ICRA) 

**_Abstract_ —Robotic applications require the integration of various modalities, encompassing perception, control of real robots and possibly the control of simulated environments. While the state-of-the-art robotic software solutions such as ROS 2 provide most of the required features, flexible synchronization between algorithms, data streams and control loops can be tedious. o80 is a versatile C++ framework for robotics which provides a shared memory model and a command framework for real-time critical systems. It enables expert users to set up complex robotic systems and generate Python bindings for scientists. o80’s unique feature is its flexible synchronization between processes, including the traditional blocking commands and the novel “bursting mode”, which allows user code to control the execution of the lower process control loop. This makes it particularly useful for setups that mix real and simulated environments.** 

# I. INTRODUCTION 

o80<sup>1</sup> is an open-source C++ toolbox that allows expert users to create custom Python API suitable for interacting with complex robotic setup [1]. o80 provides functions for: 

- the spawning realtime processes (e.g., running on RTPreempt, low latency kernel or Xenomai) 

- the synchronization of these processes 

- the asynchronous access to a shared memory hosting the history of all sensor data 

- the sending of custom commands, including blocking and not blocking commands (see section II-B) 

- the automated generation of customized Python bindings 

While o80 shares similarities with ROS (spawning of processes and C++/Python interoperability) and actionlib (management of commands) [2][3], it has differences to them: it relies on a shared memory model rather than a publishsubscribe model. But the core difference, and novelty of 

1‘o80’ is a monogram representing two running processes (‘o’ and ‘0’) and the communication between them (‘8’) 

o80, is its flexibility regarding synchronization. When using o80, users may either synchronize their higher level code with the lower level control process via blocking commands (see section II-B). Alternatively, it is possible to synchronize the lower level control process to the higher level code via the new ‘bursting mode’. In bursting mode, the low-level control process blocks until the user process sends a request to run one or more iterations. This unique feature is useful when interacting with a simulated robot or even, as shown in section III, an experimental setup involving a real robot and a simulated environment. 

However, as opposed to ROS, o80 does not support network communication, as it requires the processes it orchestrates to run on the same computer. 

The o80 framework is a two-levels system. The first level involves the expert user, who is responsible for implementing the C++ driver classes that are specific to the hardware used in the experiment. During compilation, o80 utilizes these classes as templates to generate executables that create the real-time control processes. In addition to implementing the driver classes, the expert user is responsible for generating a Python API tailored to the needs of the users. o80 allows for automated generation of Python bindings. As a result, the users will have access to a simple Python interface. These users can focus on designing experiments without being burdened by the implementation details of the robotic setup. 

# II. OVERVIEW 

# _A. Backend, frontend and shared memory_ 

o80 is based on the interaction between: 

- a backend, i.e., a process which communicates in realtime with a hardware device. It is responsible for sending commands to the device and receiving observations from 

it. Upon spawning, a backend creates a dedicated shared memory. It uses this shared memory to 1) read user commands and 2) write sensor and/or state related data. 

- a frontend provides methods for connecting to a related backend’s shared memory for 1) writing user commands and 2) for reading data. 

# _B. Realtime control and commands_ 

Stable control on realtime critical systems requires highfrequency software loops. o80 backend processes are developed in C++ to comply with real-time constraints, calculating the desired state for each actuator at each iteration. Frontends provide Python methods that send higher-level, non-realtime commands to the backend’s shared memory. These commands specify implicit desired state trajectories that rely on interpolation (based on specified durations, speeds, or numbers of server iterations). For instance, if a user command specifies that a robot should reach a desired state over a specified duration, the backend will generate the higher-frequency low-level commands that interpolate from the robot’s current state to the desired state. By translating the frontend’s commands into low-level commands that operate the system at the required frequency, the backend ensures stable control of the real-time critical systems. The frontend’s API is flexible and allows for queuing or interrupting commands, as well as issuing both blocking and non-blocking commands. 

# _C. Reading observation_ 

The backend writes current actuator state and custom sensor information to shared memory at each control iteration, which can be retrieved using various methods provided by the frontend API. Users can request the latest information, information from past server iterations, or wait for future data using a blocking method (which can be used for synchronizing user processes with backend, see section II-E). Multiple instances of the frontend can read asynchronously from shared memory. For example, this enables users to run logging scripts for the robot’s state in parallel with control scripts. 

# _D. Embedding backends_ 

In addition to generating executables that spawn backend processes, o80’s API also supports embedding instances of C++ or Python backends in other processes. This feature can be utilized to extend o80’s functionality to simulations. Section III provides an example of o80 backends being used to control the movement of bodies in a Mujoco environment. 

# _E. Synchronization and bursting mode_ 

o80 provides two synchronization modes: ”normal” and ”bursting”. In normal mode, the backend process runs in real-time at its required frequency, while the user Python process can synchronize with it through the blocking waiting methods mentioned earlier. However, in bursting mode, the backend process blocks until the frontend requires it to run one or more iterations. Bursting mode is typically used when interacting with a simulator. The frontend allows users to 

create commands that require several backend iterations to execute, which can then be executed as fast as the simulator allows. 

# III. HYSR TRAINING OF TABLE TENNIS PLAYING ROBOT 

A team of researchers from the Max Planck Institute for Intelligent Systems is exploring the potential of reinforcement learning for teaching a robotic arm, actuated by a pneumatic artificial muscle (PAM), to play table tennis [4]. The scientists are using a hybrid simulation and real training (HYSR) technique that involves mirroring the movements of a real robotic arm with a Mujoco simulated arm. This approach allows the real robot to interact with a single or multiple simulated balls that are being replayed from recorded ball trajectories, facilitating practical long-term learning of table tennis<sup>2</sup> . Additionally, virtual environments can be adapted for data-efficient training by, for instance, playing with multiple virtual balls [5]. 

To set up the experiment, the researchers required: 

- A real-time control process that sends pressure commands to the PAM controllers of the real robot at a fixed frequency of 500Hz. 

- A Mujoco simulated robot that mirrors the movements of the real robot and replays recorded ball trajectories. Each iteration of the Mujoco simulator takes 0.02 seconds. 

- A GYM reinforcement learning environment with a step function running at 100Hz. 

- Control of other hardware for real ball experiments, including a Vicon system for localizing the robot and table, a ball launcher, and an RGB-based ball detection system. 

o80 allowed to solve all the synchronization issues related to this setup. A backend process runs at 500Hz and controls the real pneumatic muscles while reading related robot states. A backend instance, running in bursting mode, is embedded in the Mujoco simulated environment. Frontends, connected to both backends, are embedded in the learning environment, asynchronously sending pressure actions and reading states to/from the real robot, sending mirroring states to the simulated robot, and sending bursting commands to the Mujoco simulated environment. 

In addition, o80 simplified the process of spawning new processes that create additional frontends, which can easily access the shared memory history to log data, visualize the robot state in real-time, and monitor both the simulated and real robot state. 

The code and documentation of this project are available as open source online [6]. 

# IV. CONCLUSION 

o80 is a versatile middleware system that offers flexible control of robotic systems. It allows expert users to develop a user-friendly Python API that makes it easier for machine learning scientists to use complex robotic setups. Its 

> 2Video of HYSR training. 

shared memory model, different synchronization modes, and interpolation-based command framework distinguish it from ROS. For more information and code examples, we refer to o80’s comprehensive documentation [7]. 

# REFERENCES 

- [1] V. Berenz, M. Naveau, F. Widmaier, M. W¨uthrich, J.-C. Passy, S. Guist, and D. B¨uchler, “The o80 c++ templated toolbox: Designing customized python apis for synchronizing realtime processes,” _Journal of Open Source Software_ , vol. 6, no. 66, p. 2752, 2021. [Online]. Available: https://doi.org/10.21105/joss.02752 

- [2] Stanford Artificial Intelligence Laboratory et al., “Robotic operating system.” [Online]. Available: https://www.ros.org 

- [3] M. Carroll, J. Perron, E. Marder-Eppstein, V. Pradeep, and M. Arguedas, “actionlib,” 2009. [Online]. Available: http://wiki.ros.org/actionlib 

- [4] D. B¨uchler, S. Guist, R. Calandra, V. Berenz, B. Sch¨olkopf, and J. Peters, “Learning to play table tennis from scratch using muscular robots,” _IEEE Transactions on Robotics (T-RO)_ , vol. 38, no. 6, pp. 3850–3860, 2022. 

- [5] S. Guist, J. Schneider, A. Dittrich, V. Berenz, B. Sch¨olkopf, and D. B¨uchler, “Hindsight states: Blending sim and real task elements for efficient reinforcement learning,” _arXiv preprint arXiv:2303.02234_ , 2023. 

- [6] V. Berenz, F. Widmaier, S. Guist, and D. B¨uchler, “PAM robot software documentation,” 2020. [Online]. Available: https://intelligent-soft-robots. github.io/pam <u>documentation/</u> 

- [7] V. Berenz, S. Guist, and D. B¨uchler, “o80 robot software documentation,” 2020. [Online]. Available: http://people.tuebingen. mpg.de/mpi-is-software/o80/docs/o80/index.html 

