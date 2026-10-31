---
title: "Sim-to-Real Transfer for Mobile Robots with Reinforcement Learning: from NVIDIA Isaac Sim to Gazebo and Real ROS 2 Robots"
date: "2025-01-06"
authors: "Sahar Salimpour; Jorge Peña-Queralta; Diego Paez-Granados; Jukka Heikkonen; Tomi Westerlund"
url: https://arxiv.org/abs/2501.02902
pdf: https://arxiv.org/pdf/2501.02902
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2501.02902)** / [論文ページ](https://arxiv.org/abs/2501.02902)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Sim-to-Real Transfer for Mobile Robots with Reinforcement Learning: from NVIDIA Isaac Sim to Gazebo and Real ROS 2 Robots 

Sahar Salimpour, Jorge Pe˜na-Queralta, Diego Paez-Granados, Jukka Heikkonen, and Tomi Westerlund 

**Abstract** —Unprecedented agility and dexterous manipulation have been demonstrated with controllers based on deep reinforcement learning (RL), with a significant impact on legged and humanoid robots. Modern tooling and simulation platforms, such as NVIDIA Isaac Sim, have been enabling such advances. This article focuses on demonstrating the applications of Isaac in local planning and obstacle avoidance as one of the most fundamental ways in which a mobile robot interacts with its environments. Although there is extensive research on proprioception-based RL policies, the article highlights less standardized and reproducible approaches to exteroception. At the same time, the article aims to provide a base framework for end-to-end local navigation policies and how a custom robot can be trained in such simulation environment. We benchmark end-to-end policies with the state-of-the-art Nav2, navigation stack in Robot Operating System (ROS). We also cover the sim-to-real transfer process by demonstrating zero-shot transferability of policies trained in the Isaac simulator to real-world robots. This is further evidenced by the tests with different simulated robots, which show the generalization of the learned policy. Finally, the benchmarks demonstrate comparable performance to Nav2, opening the door to quick deployment of state-of-the-art end-to-end local planners for custom robot platforms, but importantly furthering the possibilities by expanding the state and action spaces or task definitions for more complex missions. Overall, with this article we introduce the most important steps, and aspects to consider, in deploying RL policies for local path planning and obstacle avoidance with Isaac Sim training, Gazebo testing, and ROS 2 for real-time inference in real robots. The code is available at https://github.com/sahars93/RL-Navigation. 

**Index Terms** —Reinforcement learning (RL); Deep reinforcement learning; Sim-to-real transfer; Mobile robotics; Local planning; Obstacle avoidance; Gazebo; ROS 2; Nav2; End-to-end control. 

✦ 

## **1 INTRODUCTION** 

Reinforcement learning (RL) stands at the forefront of enabling complex control and facilitating advanced behaviors in various types of robots. This advancement holds promise for revolutionizing robotics, empowering machines to interact with their environments. RL algorithms are widely used across classic tasks including locomotion, navigation, or manipulation, among others. Indeed, recent years have seen unprecedented improvements in the ability of quadruped robots [1], wheeledlegged robots [2], drone racing [3], humanoids [4], 

- _S. Salimpour, J. Heikkonen, and T. Westerlund were with the University of Turku, Finland. Emails: {sahars, jukhei, tovewe}@utu.fi_ 

- _J. Pe˜na-Queralta and D. Paez-Granados were with the Swiss Federal School of Technology in Zurich - ETH Zurich, 8092 Switzerland._ 

_Emails: {jorge.penaqueralta, diego.paez}@hest.ethz.ch._ 

or bipedal robot sports [2]. Also, in the automation of machinery such as hydraulic excavators [5]. 

In the majority of these problems, a policy is trained to map a control input, together with the robot sensory inputs, to join-level actuation. For example, [1] maps from body-state velocities to steps, while [4] focuses on whole-body motion planning. Throughout this large variety of use cases and robotic systems, often focused on dexterous manipulation, or motion planning with a large number of degrees of freedom and/or uncertainty [6]–[8], the field has established a range of commonly used approaches and, importantly, simulation tools. The latter include NVIDIA Isaac Sim or Orbit [9], [10], MuJoCo [2], [4], or Flightmare [3], among others. 

Beyond low-level control and motion planning from propioceptive sensory inputs, RL has also been studied within the more general perspective of mobile robotics for local or global navigation, and high- 

2 


Fig. 1: Conceptual illustration of the sim-to-real workflow described in this article. In the first step, we utilize different existing robot models, while also describing the Isaac model importer functionality in Section 3. In the second step, we describe key considerations in terms of RL policy training in Section 4, and the setup of different static and dynamic environments. In the third step, we provide template Robot Operating System (ROS 2) nodes, and guidance on Gazebo testing in Sections 4 and 5. Additionally, we benchmark the performance to the state-of-the-art Nav2 navigation and planning algorithms. Finally, in the fourth step, we also demonstrate the zero-shot sim-to-real transfer capabilities in Section 5. 

level planning and autonomy. This applies to both complex robots such as quadrupeds [1], to wheeled robots there motion planning is more straightforward. The level of standardization and the depth of the study of sim-to-real transfer for navigation task, however, is shallower [11]. Through this article, we aim to give more insight into such an a priori more rudimentary and classical problem, but where RL controllers can also play an important role as the field solidifies. Our focus is on providing an stepby-step approach to training RL policies for mobile robot navigation _from scratch_ , and describing the transition _from simulation to reality_ (see Figure 1). 

From this point forward, we constraint use cases to path planning and local navigation for mobile robots from an initial position to a target destination. The sensory focus is exterioceptive, aiming at training end-to-end policies that enable navigation without collisions in both simulated and realworld scenarios. This area, including complex static and dynamic environments, has been the subject of extensive study in recent literature [12]. Deep 

reinforcement learning algorithms have emerged as a promising solution to this challenge [13]. Such RL algorithms have shown significant potential in navigation tasks for different types of robots and sensors such as LiDAR, RGB camera, and RGB-D camera [14]. 

Some representative examples are the following. [15] proposes the usage of the Advantage ActorCritic algorithm to navigate their robot in an environment with 3D obstacle avoidance, achieved through the fusion of a 2D laser scanner with an RGB-D camera in a self-implemented simulator. In [13], a soft actor-critic algorithm has been utilized to train and test an obstacle avoidance model for a differential drive robot. Similar to most lidarbased navigation studies, factors such as relative distance to the target point, lidar scan data, and the robot’s speed are employed to determine the velocity necessary to drive toward the target point. Many of these studies have conducted their training processes within the Gazebo simulation environment [16], [17]. In [18], a model-free, on-policy 

3 

deep RL approach is employed to train the control policy within TensorFlow agents simulation. It aims to guide the drone at high speeds through gates while observing the current robot state’s estimate, the gate’s relative pose using an onboard camera, and the previous action. 

A significant portion of existing studies, illustrated by the previous examples, are confined to simulations. Additionally, approaches are often tailored or the papers concentrate on either particular robots or specific considerations of a use-case. Furthermore, the lack of standardized benchmarks and open-source implementations hinders validation and comparison [19]. In this article, we address these gaps by providing detailed implementation steps, demonstrating the process of training an RL agent from simulation to real-world deployment on a generic wheeled robot. Specifically, through this magazine article, we also aim to introduce a broader audience to utilizing the state-of-the-art NVIDIA Omniverse Isaac Sim to achieve autonomous local planning and obstacle avoidance from the ground up. We delve into the key challenges and compare different approaches to training. Through learning from robot’s interactions with the environment—specifically by evaluating the presence and proximity of nearby walls and obstacles— these algorithms enable robots to make informed decisions and adapt to new situations, thereby improving their navigation capabilities in unknown environments. This makes reinforcement learning a potentially compelling approach for advancing mobile robot navigation. 

The main contributions of this article with respect to the available literature are the following. First, we provide an in-depth description of the state-of-the-art Isaac Sim simulator for RL-based navigation of wheeled robots. Second, we discuss in detail different training strategies (e.g., curriculum learning) and the key aspects to account for when defining tasks, including reward function design. Finally, we demonstrate sim-to-real transfer of end-to-end RL policies across robots, while benchmarking to classical state-of-the-art navigation approaches. Overall, we aim to provide a more comprehensive analysis of the problem of training RL-based local planners for navigation than existing literature, making learning-based approaches to ground robot navigation accessible to a larger audience. Throughout the article, we assume familiarity with basic RL concepts. 

The rest of the manuscript is organized as follows. Section 2 covers the use of Isaac Sim as a simu- 

lator for RL policy training. Section 3 then describes in more detail the different elements required to set up a training workflow. In Section 4, we delve into specific fine-tuning aspects of the proximal policy optimization (PPO) algorithm, one of the de-facto standards in the field, including reward modeling and model and training hyperparameters. Simulation and experimental results, with a focus on describing a sim-to-real transfer based on ROS 2 and the Gazebo simulator, are introduced in Section 5. Section 6 discusses and concludes the work. 

## **2 RL WITH ISAAC SIM** 

The introduction of the NVIDIA Omniverse Isaac Gym and Orbit frameworks have arguably aided in widening of audience and applications of deep reinforcement learning research. 

### **2.1 Isaac Sim** 

Isaac Sim, a GPU-based general-purpose physics simulation platform from Nvidia, serves as an extensible robotics simulator that empowers designers, researchers, and developers to create, test, and train AI-based robots such as wheeled robots, legged robots, and drones. Leveraging the power of NVIDIA Omniverse, Isaac Sim provides scalable, photorealistic, and physically accurate virtual environments for high-fidelity simulations. It can simulate realistic sensor models such as camera, lidar, and IMU, and a variety of objects and scenes, enabling tasks such as manipulation, navigation, synthetic data generation, and various computer vision applications through Python, ROS integration, and Isaac SDK. 

### **2.2 RL in Isaac Sim / Gym** 

Omniverse Isaac Gym is an extension for reinforcement learning in robotics which is built on top of NVIDIA Isaac Sim. Isaac Gym is highly parallelized simulations by conducting both physics simulation and policy training on the GPU through an API, based on the vectorization of observations and actions. This framework offers a straightforward interface for training RL agents and supports various RL algorithms. In the latest releases of Isaac Gym, RL Games is introduced as the default library for running example environments. Whether it is training robotic agents to perform complex tasks, fine-tuning and optimizing RL policies, or evaluating their performance, Isaac Gym provides a bridge between the simulation environment and RL algorithms. 

4 

More recent RL framework, also powered by NVIDIA Isaac Sim, are Orbit and Isaac Lab. Orbit offers a comprehensive suite of features, including support for various robot platforms, sensors, teleoperation, imitation Learning, and motion planning across diverse robotic applications, while Isaac Lab provides more comprehensive environments for different types of robots and tasks<sup>1</sup> . In these new frameworks, beginners may encounter a steeper learning curve. This article, therefore, focuses on the more documented and tested Isaac Gym as the first tutorial for straightforward path planning and navigation implementation, which can be further developed in Isaac Lab for more advanced features. 

## **3 RL WORKFLOW** 

In Isaac Gym, the development and simulation of a customized RL agent navigation task needs a few basic steps for effective simulation, training, and testing. This includes defining the simulation environment and robot, crafting a Python script for the task class to specify goals, reward computation, and reset management, and utilizing two YAML configuration files—one for task parameters and another for training parameters—to complete the task. This section provides an overview of these essential core components. 

### **3.1 Robot And Environments** 

Isaac Gym offers a user-friendly API for creating and configuring scenes with custom robots and objects. Many ROS users utilize the Unified Robot Description Format (URDF), a popular format for describing the basic robot cell and geometry, and practical applications. Isaac Sim supports various file formats, including URDF, Multi-Joint dynamics with Contact (MJCF), and Universal Scene Description (USD). It is feasible to incorporate custom robots from URDF and MJCF files into tasks, or alternatively, convert them to USD format using the Isaac Sim Importer extensions. Two robot models were employed in our mobile robot navigation task, the modified Isaac built-in Jetbot robot with Lidar sensor (Figure.2a) and the USD model of the Turtlebot3-Waffle from the TurtleBot3 Simulation ROS Package, converted through the Isaac URDF Importer as shown in Figure. 2b for additional experiments. To correctly import the mobile robot from the URDF file, the ”Fixed Base Link” must be unchecked, and the ”Joint Drive Type” must be set 

1. https://isaac-sim.github.io/IsaacLab/main/index.html 

to ”Velocity”. When working on specific tasks, one can create, modify, and save custom scenes within Isaac Sim and add them as USD files into the task as shown in Figure. 2c. 

### **3.2 Task** 

A variety of reinforcement learning tasks are provided at Omniverse Isaac Gym extension, where main functionalities such as performing episode resets, applying actions, collecting observations, and computing rewards are implemented in this task class. Our _JetbotTask_ , inherits from the BaseTask class in _omni.isaac.core_ , comprises several key components. The general structure of the definition of each component of a new RL task is shown in Listing 1 The Initialization phase, the _init_ function, sets initial configurations for the environment. The initial setup for each task is detailed in its dedicated task YAML file. An overview of this file, along with a few sample parameters, is presented in 3.2. One can specify parameters related to the environment and simulation within this file. These include the number of environments, various sensors and USD configurations for the robot and objects, specifying CPU or GPU pipeline, and applying noise to observations, actions, and other properties in the domain randomization part. Action and observation space and other parameters such as the episode’s length are also defined in the init function. The _set_ _<u>up scene</u>_ function is for setting up the scene by creating ArticulationView or RigidPrimView objects. This function involves defining the scene, sensor, and robot, or loading assets from USD, URDF, and MJCF file formats. The _get_ _<u>observation</u>_ function generates the observation space using Lidar ranges, information on the target’s relative position, and the robot’s state. Computations required before stepping into the physics simulation, such as applying actions to move the robot based on policy decisions or resetting the environment, occur in the _pre_ _<u>physics step</u>_ function. The calculation of rewards, resets, and extra buffers is handled in the _calculate_ _<u>metrices</u>_ function. Finally, determining which environments need resetting is done in the last function of the task. Besides the task config file, each task is accompanied by its configuration file containing training parameters such as the model and network structures, and the PPO parameters such as the learning rate, as shown in 3. These parameters are passed through _rlgames_ _<u>train.py</u>_ . 

5 


Fig. 2: Robots and Environments 


Listing 1: General structure of a new RL task definition in OmniIsaacGym. 

### **3.3 From Isaac To Gazebo** 

Before deploying navigation policies in the real world, we evaluate the trained policy within the 


Listing 2: Core components of _task.yaml_ . 

Gazebo simulation environment. Gazebo, a widely adopted simulator in the global robotics community, directly interfaces with the ROS through userfriendly packages. This integration facilitates the creation of accurate simulations, and the outcomes obtained can be directly implemented on the real robots with only ROS installed, regardless of their software architecture. There are many Gazebo simulation packages available, featuring different dif- 

6 


Listing 3: Core components of train.yaml. 

ferential drive robots equipped with Lidar sensors. 

In order to test in the Gazebo simulator, the trained model weights are exported in the format of ONNX model and integrated into a ROS node. The ONNX model can be imported and utilized for both simulation and real-world scenarios. 

### **3.4 ROS 2 Node Deployment** 

A ROS2 node is defined to handle the ROS operations within the robots. Upon initialization, such as the target’s position, it sets up subscriptions to topics such as the Scan topic to get the Lidar ranges and the robot’s position through the Odometry topic, along with a publisher for _cmd_ _<u>vel</u>_ commands. Additionally, the class integrates an ONNX model, for inference. Various callback functions are implemented, such as _Odometry_ _<u>callback</u>_ (), and _scan_ _<u>callback</u>_ (), to process incoming messages from subscribed topics. Finally, the _send_ _<u>control</u>_ () function generates robot control commands based on the model’s outputs and publishes them via _cmd_ _<u>vel</u>_ . 


Listing 4: ROS2 Node for real-time inference. 

In our navigation task, at each time step, the observation state _ot_ comprises 2D lidar scans with 6- degree resolution (120 scans) in the range of [0.15, 3](m) shown as _Lt_ , relative goal position as a 2D vector representing the robot’s relative distance, _dt_ , and angle, _θt_ , to the goal in polar coordinates, and the linear velocity _vt−_ 1 from the previous time step, along with the angular velocity _ωt−_ 1. In (1), _at_ is the 2D action space, defined as linear velocity _vt_ and angular velocity _ωt_ , and the DRL policy, _π_ , maps the observed state _ot_ , into the updated action, as the linear velocity in the range of [0.1, 0.5](m/s) and angular velocity in the range of [-0.5, 0.5](rad), to direct the robot towards its goal while avoiding collisions. 


## **4 RL FOR NAVIGATION** 

This section covers key aspects that need to be customized based on the robot, available sensors, or the overall use-case or general optimization objectives. These include the definition of observation and action spaces, reward modeling, and hyperparameter settings for both the model and the training and environment setup. 

### **4.1 Observation State** 

The primary objective of an RL policy is to optimize the cumulative reward, by effectively navigating the interactions between the agent and its environment. 

### **4.2 Rewards** 

In the reinforcement learning framework, the reward function plays a crucial role in assessing the effectiveness of the robot’s actions. In navigation tasks, agents receive rewards based on goal achievement, collision avoidance, and time. Sparse rewards can hinder convergence, so the reward structure can be adjusted to better suit the task and enhance learning efficiency. In our navigation task, the primary aim is to ensure the robot avoids collisions and reaches its destination swiftly. The reward function, denoted as _Rt_ in (2), is designed with three main components. The robot receives rewards as 

7 

it progressively reduces its distance from the target, defined as _rdistance_ , and to avoid the collision, an exponential penalty, _rcollision_ , is applied to the robot as it gets closer to the obstacles, increasing as it approaches the threshold _Min_ , as the closest possible distance. Furthermore, to determine the shortest path, the robot is rewarded based on the time it takes to reach the target. This means that after reaching the target, the reward is calculated based on the remaining episode length. 


(2) 

In the reward function, we introduce additional conditions that signal the end of an episode. In addition to the previously discussed rewards, we define three fixed rewards that serve as reset flags. The first is awarded upon reaching the target, defined as _Goal_ , _Collision_ is a fixed negative reward for collisions when the robot gets too close to obstacles beyond the _Min_ threshold, and _Max length_ is a penalty for surpassing the maximum episode length before reaching to the target. These three conditions collectively signify the conclusion of an episode in the _is_ _<u>done</u>_ function in the Listing 1. The reward amounts can be defined based on the size and type of the robot, avoidance distance, and the environment. In our Jetbot navigation task, the _Min_ is 25 _cm_ and all fixed rewards _r_ 1, _r_ 2, and _r_ 3 are set to 30. 

In the literature, the three main components—goal, collision, and time—are essential, with their weights varying. A large penalty for collisions may limit exploration, while a high reward for the target might lead to overfitting to a specific target point, reducing generalization. Typically, training begins with equal weights, and adjustments are made based on the specific task. 

### **4.3 Model Definition** 

We set the episode length to a maximum of 1200 steps, with 64 environments running for 1500 iterations. Our implementation revolves around the Actor-Critic algorithm designed for continuous spaces. The actor-critic algorithm is a reinforcement learning technique that merges policy-driven (Actor) and value-driven (Critic) approaches. The Actor 


Fig. 3: Episodic returns during training using Isaac Sim 


Fig. 4: Illustration of the robot and lidar scan in an Isaac environment with dynamic obstacles pictured in red. 

selects actions per its policy, while the Critic assesses the Actor’s decisions. The Actor-Critic model utilizes a logarithmic standard deviation (logstd) for continuous action space, resulting in actions defined by a mean value with a fixed standard deviation. The network structure consists of a MultiLayer Perception (MLP) with 3 hidden layers of sizes [256 _,_ 128 _,_ 64]. Additionally, for training in the dynamic environment, we experimented with a Long Short-Term Memory (LSTM) layer of 128 hidden units after the input, followed by the MLP. As described earlier, these parameters are configured in the task and train config files. We train and test with two mobile robots, the Isaac built-in Jetbot, Figure 2a, and the Turtlebot3 robot imported from 

8 

its URDF format, Figure 2b. When changing the robot, certain parameters in the initialization function must be adjusted, such as the wheel and speed settings in the _DifferentialController_ class or the minimum and maximum lidar scan ranges. 

## **5 EXPERIMENTAL RESULTS** 

### **5.1 Training In Isaac** 

The training results, depicted in Figure 3, show our experiments conducted in static and dynamic environments. In the static environment, the aforementioned MLP structure achieved a maximum of 73 rewards across 1000 episodes, signifying the successful accumulation of rewards for reaching the target in the shortest possible time. We employed the same network structure but added dynamic obstacles moving within the environment, red cubes in Fig4, which inherently complicated the training process. To further capture previous observations, we extended our training to include an LSTM layer followed by the same MLP layers. The training process in the dynamic environment shows limited promise, even when utilizing an LSTM layer. In fact, the robot fails to avoid obstacles and reach the target within 1000 episodes. 

We adopted a curriculum learning approach for the dynamic environment to facilitate and accelerate the learning process, and enhance convergence. Curriculum learning is a training strategy that gradually increases the complexity of tasks or training samples. When performing an advanced navigation task, the initial step involves moving toward the target with associated rewards. Then, the environment’s complexity can be enhanced by including static obstacles, and a penalty for collisions in the reward function. Finally, dynamic obstacles are added during the training process. In our case, we initiated training with the simpler task, the static environment. This allowed the agent to learn initial policies for moving towards the target, resulting in faster convergence. After 300 initial steps, we added dynamic objects and continued the training process in a more complex environment. The staged curriculum approach enabled smoother adaptation to the dynamic obstacles, ultimately enhancing the agent’s performance and episode return. 

### **5.2 Isaac Simulations** 

Within the process of validating our model, a series of tests were conducted within the Isaac simulation environment, utilizing both Jetbot and Turtlebot3 


Fig. 5: Average and standard deviation of distance to the target as a function of time during tests using Jetbot in Isaac Sim with static and dynamic environments. 

robots. These tests involved setting various target positions to assess the model’s adaptability. Figure 6a illustrates the Jetbot navigating through a novel environment, adeptly heading towards diverse target poses while avoiding obstacles along multiple paths. For Turtlebot3, Figure 6b conveys the trajectory outcomes, where the proximity to obstacles is indicated by a gradient of colors, reflecting the robot’s distance to the nearest object. This visual representation underscores the model’s proficiency in maintaining a safe distance from obstacles, a critical aspect of autonomous navigation. Extending the assessment to dynamic settings, Figure 6c depicts robot’s successful navigation past moving objects, effectively avoiding collisions. This performance is attributed to the model’s curriculum-based training, as discussed in the preceding section. 

Finally, Figure 5 presents an aggregation of the robots’ relative distances to a specified target from Figure 6c, compiled over 30 trials. This data encompasses scenarios with and without dynamic obstacles, providing a comprehensive view of the model’s efficacy in variable environments. 

### **5.3 Gazebo Simulations** 

Prior to real-world deployment, the RL model was converted to an ONNX format and subjected to tests in various Gazebo environments using a ROS 2 node. We conducted a comparative analysis of the LSTM- and MLP-based RL models against Nav2 [20], the de facto ROS 2 navigation stack, a sophisticated control system designed for autonomous robot navigation to a goal state based on the robot’s current position, a map, and a target location. Figure 7 illustrates the comparative results in both static and dynamic settings. 

In the experiments, a mobile box was placed ahead of the robot, with its velocity adjusted be- 

9 


(a) Jetbot trajectory, different targets (static environment) 


(b) Turtlebot3 trajectory, safety spectrum (static environment). 


(c) Jetbot trajectory in dynamic environment. 

Fig. 6: Qualitative evaluation performance with minimum lidar range throughout the trajectories in Isaac Sim. 

tween 0.1 and 0.3 m/s across various trials to obstruct the robot’s trajectory toward the designated target. Over 10 iterations of the same path, the distance-to-target distribution over time was comparable across all three methods (MLP-, LSTMbased RL, and Nav2) in static environments. This outcome is expected, as the Nav2 stack relies on a precomputed cost map, which can be less effective when encountering dynamic obstacles or sudden environmental changes, potentially leading to mission failure. 

In contrast, the LSTM-based RL model, specifically trained to handle such scenarios, demonstrated superior performance. It consistently navigated around obstacles and avoided collisions, showcasing its robustness in dynamic conditions and its potential for reliable real-world applications. Meanwhile, the one-step training model using the MLP exhibited reduced performance in dynamic obstacle avoidance, underscoring its limited effectiveness for this task. 

### **5.4 Real-World Validation** 

The approach adopted in this research is adaptable to various mobile robotic systems. For the practical implementation and assessment of the RL navigation model, we employed the TurtleBot 4 Lite, which was equipped with an RPLIDAR A1M8, granting a complete 360-degree perspective, and interfaced with a Raspberry Pi 4B as the On-board Computer, Figure 8. The dimension of the TurtleBot 4 Lite is 342 x 339 x 192 mm, with wheels measuring 72 mm in diameter. Its maximum safe mode linear velocity is 0.31 m/s. The LiDAR has a minimum detection distance of 0.15 m, with its range configured up to 2 m and a resolution of 3 degrees. 

The refined model weights have been exported and integrated into a ROS2 Galactic node. The control system runs on the Raspberry Pi On-board Computer. The robot’s positioning data was captured using an Optitrack Motion Capture system. To evaluate the system in real-world static environments, we designed test scenarios with obstacles of varying sizes and shapes, ensuring these differed from those used during training to assess generalization. Additionally, the robot’s starting position was carefully chosen to align with the training setup, where it consistently began in relatively free space. This was necessary to avoid requiring additional training steps to account for diverse initial conditions. Figure 9 illustrates the robot’s navigation paths in four distinct settings 

10 


Fig. 7: Comparative performance analysis of the RL policy and Nav2 Stack in Gazebo. 

TABLE 1: Real-world performance statistics over 10 trials for 4 different experiments. 

||Task<br>time (s)|Success<br>rate|Min. lidar<br>range (m)|Avg. linear<br>vel. (m/s)|Dist. to<br>target (m)|
|---|---|---|---|---|---|
|**Exp. 1**|39|10/10|0.43|0.15|4.69|
|**Exp. 2**|41|10/10|0.39|0.15|4.70|
|**Exp. 3**|53|8/10|0.40|0.13|5|
|**Exp. 4**|52|7/10|0.25|0.14|4.73|


Fig. 8: TurtleBot 4 Lite robot with 2D lidar used for the real-world experimental evaluation. 

with varied obstacles. As shown in Figure 10, the robot’s trajectories at different timestamps illustrate 

its movement while navigating towards the target. We conducted 10 trials for each test, and the bolded average performance metrics are presented in Table 1. The results from the successful trials indicate that the robots maintained a minimum distance of 25 cm from obstacles, aligning with the training threshold. This safety margin can be adjusted to suit different robot dimensions and configurations. Similarly, the linear velocity parameter is flexible and can be tailored as required. 

We expanded our experimentation to include dynamic obstacles—specifically, people—that obstruct the robot’s path toward the target. The robot’s trajectories, both without obstacles and with dynamic obstacles, are illustrated in Figure 11. To highlight the robot’s avoidance behavior, we marked the positions of the robot and obstacle every 15 

11 


Fig. 9: Navigation in Various Real-World Environments 

seconds, showing when the robot adjusts its path. The individuals moved unpredictably in front of the robot, partially obstructing its direct path toward the target. At times, the person would suddenly appear in the robot’s trajectory, while in other instances, they moved alongside the robot, attempting to obstruct its path. This random movement pattern was designed to simulate real-world scenarios with a priori unpredictable dynamic obstacles. 

While curriculum learning improves performance in dynamic environments, models often struggle with tasks beyond their training conditions in dynamic environments. Handling diverse obstacle sizes, shapes, directions, and speeds requires carefully tuned reward functions and additional training stages to maintain robust performance. 

## **6 DISCUSSION** 

We tested the model in various static environments across simulators and the real world, achieving promising results. However, its generalization and robustness faced challenges in dynamic real-world settings. The presence of diverse conditions and noise—such as changes in the size, shape, speed, and direction of dynamic obstacles—highlighted the need for further adjustments. To improve performance in such scenarios, retraining, progressive training, and potential modifications to the reward function may be necessary. Additionally, real-world test feedback led to fine-tuning parameters, such as adjusting the LiDAR sampling process to account for narrower dynamic obstacles. These adjustments required either retraining from the baseline or more training to refine the reward function. To enable safe and effective navigation through dynamic obstacles such as humans, incorporating a specialized reward 

12 


Fig. 10: Robot trajectories with timestamps showing obstacle avoidance and navigating towards the target. 


Fig. 11: Trajectories of Turtlebot in the presence of a dynamic obstacle in real-world experiments. 

function term, such as a social-safety zone, may be essential for fostering human-aware navigation. This approach can be adapted and generalized for other specific environments requiring tailored modifications. 

## **7 CONCLUSION** 

Throughout this article, we have described the process of setting up a training workflow for a RL policy for mobile robot navigation in Isaac Sim. We covered the key steps in defining the robot model, and the training environment and RL task. Additionally, we discuss important aspects in terms of hyperparameter tuning from the perspective of 

both the training setup and the actual policy model. Finally, we describe the workflow to enable the transfer from simulation to reality, with examples and ROS 2 node templates. 

To demonstrate the effectiveness and usability of such RL policies for real-world deployments, we also analyze the performance both quantitatively and qualitatively in simulation (Isaac Sim and Gazebo) and real-world experiments. We use Nav2, the de-facto standard ROS 2 navigation stack, as a benchmark in a subset of the simulations. 

The experimental results convey that state-ofthe-art performance can be obtained by training fully in the simulation environment. This opens the 

13 

door to quick deployment of new robots with endto-end RL-based control, where both perception, trajectory planning and tracking are encapsulated in a single process. While this does not necessarily offer the best fine-tuned performance, we believe this to be a step towards, e.g., low-code applications. 

Overall, this work aims to discuss the different possible approaches to RL-based local navigation and obstacle avoidance, beyond the specific approaches and use-cases widely showcased in the literature. This has been presented in an instructional style, but also covering new experimental results. Importantly, we believe this work fills a gap in the literature in terms of the introduction of generic sim-to-real workflows and a generalizable approach to RL navigation in mobile robotics. 

## **ACKNOWLEDGMENTS** 

This work was supported by the R3Swarms project funded by the Technology Innovation Institute (TII). 

## **REFERENCES** 

- [1] S. Gangapurwala, M. Geisert, R. Orsolino, M. Fallon, and I. Havoutis, “Rloc: Terrain-aware legged locomotion using reinforcement learning and optimal control,” _IEEE Transactions on Robotics_ , vol. 38, no. 5, 2022. 

   - [12] S. Aradi, “Survey of deep reinforcement learning for motion planning of autonomous vehicles,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 23, no. 2, 2020. 

   - [13] J. Choi, G. Lee, and C. Lee, “Reinforcement learningbased dynamic obstacle avoidance and integration of path planning,” _Intelligent Service Robotics_ , vol. 14, 2021. 

   - [14] W. Li, M. Yue, J. Shangguan, and Y. Jin, “Navigation of mobile robots based on deep reinforcement learning: Reward function optimization and knowledge transfer,” _Intl. Journal of Control, Automation and Systems_ , 2023. 

   - [15] H. Surmann, C. Jestel, R. Marchel, F. Musberg, H. Elhadj, and M. Ardani, “Deep reinforcement learning for real autonomous mobile robot navigation in indoor environments,” _arXiv_ , 2020. 

   - [16] J. Gao, W. Ye, J. Guo, and Z. Li, “Deep reinforcement learning for indoor mobile robot path planning,” _MDPI Sensors_ , vol. 20, no. 19, 2020. 

   - [17] N. U.<sup>¨</sup> Akmandor, H. Li, G. Lvov, E. Dusel, and T. Padir, “Deep reinforcement learning based robot navigation in dynamic environments using occupancy values of motion primitives,” in _IEEE IROS_ , 2022. 

   - [18] E. Kaufmann, L. Bauersfeld, A. Loquercio, M. M¨uller, V. Koltun, and D. Scaramuzza, “Champion-level drone racing using deep reinforcement learning,” _Nature_ , vol. 620, no. 7976, 2023. 

   - [19] I. Kim, S. H. Nengroo, and D. Har, “Reinforcement learning for navigation of mobile robot with lidar,” in _IEEE ICECA Technology_ , IEEE, 2021. 

   - [20] S. Macenski, T. Moore, D. V. Lu, A. Merzlyakov, and M. Ferguson, “From the desks of ros maintainers: A survey of modern & capable mobile robotics algorithms in the robot operating system 2,” _Robotics and Autonomous Systems_ , vol. 168, 2023. 

- [2] J. Lee, M. Bjelonic, A. Reske, L. Wellhausen, T. Miki, and M. Hutter, “Learning robust autonomous navigation and locomotion for wheeled-legged robots,” _Science Robotics_ , vol. 9, no. 89, 2024. 

- [3] Y. Song, A. Romero, M. M¨uller, V. Koltun, and D. Scaramuzza, “Reaching the limit in autonomous racing: Optimal control versus reinforcement learning,” _Science Robotics_ , vol. 8, no. 82, 2023. 

- [4] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, 2024. 

- [5] P. Egli and M. Hutter, “Towards rl-based hydraulic excavator automation,” in _IEEE IROS_ , 2020. 

- [6] D. Han, B. Mulyana, V. Stankovic, and S. Cheng, “A survey on deep reinforcement learning algorithms for robotic manipulation,” _MDPI Sensors_ , vol. 23, no. 7, 2023. 

- [7] G. B. Margolis, G. Yang, K. Paigwar, T. Chen, and P. Agrawal, “Rapid locomotion via reinforcement learning,” _The International Journal of Robotics Research_ , 2024. 

- [8] T.-Y. Yang, T. Zhang, L. Luu, S. Ha, J. Tan, and W. Yu, “Safe reinforcement learning for legged locomotion,” in _IEEE IROS_ , 2022. 

- [9] M. Mittal, C. Yu, Q. Yu, J. Liu, N. Rudin, D. Hoeller, J. L. Yuan, R. Singh, Y. Guo, H. Mazhar, _et al._ , “Orbit: A unified simulation framework for interactive robot learning environments,” _IEEE Robotics and Automation Letters_ , 2023. 

- [10] W. Zhao, E.-A. Rantala, J. Pajarinen, and J. P. Queralta, “Less is more: Robust robot learning via partially observable multi-agent reinforcement learning,” _arXiv_ , 2023. 

- [11] W. Zhao, J. P. Queralta, and T. Westerlund, “Sim-to-real transfer in deep reinforcement learning for robotics: a survey,” in _IEEE SSCI_ , 2020. 

