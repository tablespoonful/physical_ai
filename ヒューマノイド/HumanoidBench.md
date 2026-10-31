---
title: "HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation"
date: "2024-03-15"
authors: "Carmelo Sferrazza; Dun-Ming Huang; Xingyu Lin; Youngwoon Lee; Pieter Abbeel"
url: https://arxiv.org/abs/2403.10506
pdf: https://arxiv.org/pdf/2403.10506
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2403.10506)** / [論文ページ](https://arxiv.org/abs/2403.10506)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation 

Carmelo Sferrazza<sup>1</sup> Dun-Ming Huang<sup>1</sup> Xingyu Lin<sup>1</sup> Youngwoon Lee<sup>1</sup><sup>_,_2</sup> Pieter Abbeel<sup>1</sup> 1UC Berkeley 2Yonsei University 


Fig. 1: Humanoid robots equipped with dexterous hands hold immense promise for integration into real-world human environments. Nonetheless, harnessing the full potential of humanoid robots presents numerous challenges, such as the intricate control of robots with complex dynamics, sophisticated coordination among various body parts, and addressing long-horizon complex tasks envisioned for these robots. We present **HumanoidBench** , a simulated humanoid robot benchmark consisting of 15 whole-body manipulation and 12 locomotion tasks, such as shelf rearrangement, package unloading, and maze navigation. 

**_Abstract_ —Humanoid robots hold great promise in assisting humans in diverse environments and tasks, due to their flexibility and adaptability leveraging human-like morphology. However, research in humanoid robots is often bottlenecked by the costly and fragile hardware setups. To accelerate algorithmic research in humanoid robots, we present a high-dimensional, simulated robot learning benchmark, HumanoidBench, featuring a humanoid robot equipped with dexterous hands and a variety of challenging whole-body manipulation and locomotion tasks. Our findings reveal that state-of-the-art reinforcement learning algorithms struggle with most tasks, whereas a hierarchical learning approach achieves superior performance when supported by robust low-level policies, such as walking or reaching. With HumanoidBench, we provide the robotics community with a platform to identify the challenges arising when solving diverse tasks with humanoid robots, facilitating prompt verification of algorithms and ideas. The open-source code is available at https://humanoid-bench.github.io.** 

### I. INTRODUCTION 

Humanoid robots have long held promise to be seamlessly deployed in our daily lives. Despite the rapid progress in humanoid robots’ hardware (e.g., Boston Dynamics Atlas, Tesla Optimus, Unitree H1), their controllers are fully or partially hand-designed for specific tasks, which requires significant engineering efforts for each new task and environment, and often demonstrates only limited whole-body control capabilities. 

In recent years, robot learning has shown steady progress in both robotic manipulation [12, 69, 15] and locomotion [27, 71]. However, scaling learning algorithms to humanoid robots is 

still challenging and has been delayed mainly due to such robots’ costly and unsafe real-world experimental setups. 

To accelerate the progress of research for humanoid robots, we present the first-of-its-kind humanoid robot benchmark, **HumanoidBench** , with a diverse set of locomotion and manipulation tasks, providing an accessible, fast, safe, and inexpensive testbed to robot learning researchers. Our simulated humanoid benchmark demonstrates a variety of challenges in learning for autonomous humanoid robots, such as the intricate control of robots with complex dynamics, sophisticated coordination among various body parts, and long-horizon complex tasks. 

HumanoidBench provides (1) a simulation environment comprising a humanoid robot with two dexterous hands, as illustrated in Figure 1; (2) a variety of tasks, spanning locomotion, manipulation, and whole-body control, incorporating humans’ everyday tasks; (3) a standardized benchmark to evaluate the progress of the community on high-dimensional humanoid robot learning and control. In fact, HumanoidBench supports generic controller structures, including both learning and modelbased approaches [14, 26]. In this paper, we present extensive benchmarking results of the state-of-the-art reinforcement learning (RL) algorithms, which do not require extensive domain knowledge, and a hierarchical RL approach. 

The simulation environment of HumanoidBench uses the MuJoCo [60] physics engine. For the simulated humanoid robot, 

|Benchmark|Dexterous hands|Action dim.|DoF|Task horizon|# Tasks|Skills<sup>1</sup>|
|---|---|---|---|---|---|---|
|MyoHand [8]|�|39|23D|50-2000|9|PnP, R, Po, IR, H, Ro|
|Adroit [49]|�|24|24D|200|4|PnP, P, R, Po, IR, H, L, Ro|
|MyoLeg [8]|�|80|20D|1000|1|Lo, St|
|LocoMujoco [3] (Unitree-H1)|�|19|6D|100-500|27|L, Lo, St, BM|
|DMControl [58] (Humanoid)|�|24-56|22D|1000|6|Lo, St|
|FurnitureSim [22]|�|8|6D|2300|8|PnP, P, I, IR, H, L, Ro|
|robosuite [70]|�|6-24|6-7D|500|9|PnP, P, I, R, IR, H, L, Ro|
|rlbench [24]|�|6-7|6-7D|100-1000|106|PnP, P, I, R, Po, IR, H, L, Ro|
|metaworld [64]|�|6|7D|500|50|PnP, P, I, R, Po, IR, H, L, Ro|
|**HumanoidBench (Ours)**|�|61|75D|500-1000|27|PnP, P, I, R, Po, IR, H, L, Ro, Lo, BM, St|


> 1PnP: Pick-and-place / P: Push / I: Insert / R: Reach / Po: Pose / IR: In-hand re-orientation / H: Hold / L: Lift / Ro: Rotate / Lo: Locomotion / BM: Whole-body (humanoid) Manipulation / St: Stabilization 

TABLE I: **Comparison of simulated robot benchmarks.** Our humanoid robot benchmark tests a variety of complex, longhorizon task with a large action space. 

we mainly opt for a Unitree H1 humanoid robot<sup>1</sup> , which is relatively affordable and offers accurate simulation models [66], with two dexterous Shadow Hands<sup>2</sup> attached to its arms. Our environment can easily incorporate any humanoid robots and end effectors; thus, we provide other models, including Unitree G1<sup>3</sup> , Agility Robotics Digit<sup>4</sup> , the Robotiq 2F-85 gripper, and the Unitree H1 hand. 

The HumanoidBench task suite includes 15 distinct wholebody manipulation tasks involving a variety of interactions, e.g., unloading packages from a truck, wiping windows using a tool, catching and shooting a basketball. In addition, we provide 12 locomotion tasks (not requiring hands’ dexterity), which can serve as primitive skills for whole-body manipulation tasks and provide a set of easier tasks to verify algorithms. The benchmarking results on this task suite show how the state-ofthe-art RL algorithms struggle with controlling the complex humanoid robot dynamics and solving the most challenging tasks, illustrating ample opportunities for future research. 

### II. RELATED WORK 

Deep reinforcement learning (RL) has made rapid progress with the advent of standardized, simulated benchmarks, such as Atari [5] and continuous control [7, 58] benchmarks. In robotic manipulation, most existing simulated environments are limited to quasi-static, short-horizon skills, having focused on tasks like picking and placing [7, 24, 70, 64, 37], in-hand manipulation [49, 44, 8], and screwing [43]. 

Complex manipulation tasks, such as block stacking [13], kitchen tasks [17], and table-top manipulation [25, 39, 34], have been introduced but are still limited to a combination of pushing, picking, and placing. On the other hand, the IKEA furniture assembly environment [31], BEHAVIOR [55, 32], and Habitat [57] present diverse long-horizon (mobile) manipulation tasks, with their main focus being on high-level planning by abstracting complex low-level control problems, while FurnitureBench [22] introduces a simulated benchmark for complex 

> 1https://www.unitree.com/h1 

> 2https://www.shadowrobot.com/dexterous-hand-series/ 

> 3https://www.unitree.com/g1 

> 4https://agilityrobotics.com/robots 

long-horizon furniture assembly tasks with sophisticated lowlevel control. 

However, most of these benchmarks use a single-arm manipulation setup with either a parallel gripper or a dexterous hand [9, 49], limiting the types of object interactions and not addressing the challenges of coordinating multiple parts of a body [30], e.g., multiple fingers, arms, and legs. Robosuite [70] includes a handful of bimanual manipulation tasks, while more recently Chen et al. [10] and Zakka et al. [67] have introduced additional benchmarks that require coordinating two floating robot hands, i.e., not attached to any arm base. 

While bimanual manipulation is one of the key objectives of humanoid robots, most benchmarks in humanoid research have so far focused on the locomotion challenges [8, 28, 45, 3]. In this regard, such simulations have accelerated research on control algorithms [6, 46, 47, 40], ultimately leading to achieve robust humanoid locomotion in the real world [1, 50, 11]. 

Recent works have extended humanoid simulations to different domains involving a certain degree of manipulation, i.e., tennis [68], soccer [19], ball manipulation [61] and catching [38], and box moving [63]. However, all these works focus on demonstrating their approaches on specific humanoid tasks and lack a diversity of tasks. In addition, most of the previous work focuses on simplistic humanoid models [38, 61], leading to inaccurate physics and collision handling. This motivates us to implement a _comprehensive_ simulated humanoid benchmark based on real-world hardware and consisting of a diverse set of whole-body control tasks with careful design choices for diversity and usability. 

In contrast to prior robotic simulation benchmarks, HumanoidBench presents a broader set of challenges, featuring high-dimensional action spaces and DoFs, resulting from humanoid robots and dexterous hands, and a variety of longhorizon tasks, which cover a comprehensive set of robotic locomotion and manipulation skills, as summarized in Table I. 

Finally, we note how in the literature, tasks that require long-term planning with a high-dimensional action space have been addressed with hierarchical reinforcement learning (HRL), which decouples low-level and high-level planning in a reinforcement learning paradigm [33, 4, 42, 29, 17, 30, 48]. 


Fig. 2: Example egocentric visual (top-left) and whole-body tactile (right) observations when the humanoid interacts with a package in the truck environment. In the right figure, the two cameras on the robot head are highlighted in green, while continuous tactile pressure readings are indicated in shades of red (strong pressure) and yellow (mild pressure). Note that for ease of visualization, we are not showing shear forces and tactile readings on the back of the robot, which are also implemented in our environment. 

In the context of humanoids, we propose an HRL paradigm to show how a specific set of low-level skills (e.g., standing, walking) facilitates learning of higher-level tasks. 

### III. SIMULATED HUMANOID ROBOT ENVIRONMENT 

In this section, we describe our simulated environment and discuss relevant design choices for the simulated humanoid robot. As illustrated in Figure 2, we use the Unitree H1 humanoid robot<sup>1</sup> with two dexterous Shadow Hands<sup>2</sup> as the primary robotic agent of our benchmark. We simulate this humanoid robot using MuJoCo [60] adapting the Unitree H1 model provided by Unitree<sup>5</sup> and the dexterous Shadow Hand models available through MuJoCo Menagerie.<sup>6</sup> 

**Humanoid Body.** We implement Unitree H1<sup>1</sup> , Unitree G1<sup>3</sup> , and Agility Robotics Digit<sup>4</sup> , which are well-known humanoid robots with their model files freely available [66, 1]. Unitree H1 is primarily used in our benchmark as it is a full-size humanoid compared to the smaller Unitree G1, and as we observed faster learning compared to the Agility Robotics Digit, which we ascribe to a simpler mechanical design compared to Digit, which features passive joints actuated through a four-bar linkage. 

**Dexterous Hands.** We use two dexterous Shadow Hands<sup>2</sup> , which also have model files freely available<sup>6</sup> , and have shown impressive manipulation capabilities both in simulation [67] and in the real world [2]. To make the simulated robot have more human-like morphology, we remove the cumbersome 

> 5https://github.com/unitreerobotics/unitree <u>ros</u> 

> 6https://github.com/google-deepmind/mujoco <u>menagerie</u> 

||Without hand|With 2 hands|
|---|---|---|
|Observation space|51|151|
|Action space|19|61|
|DoF (body)|25|25|
|DoF (two hands)|0|50|


TABLE II: **Humanoid robot specifications with and without hands.** Both the humanoid body (including its floating base) and one Shadow Hand present action spaces (19 and 21, respectively) smaller than their DoFs (25), making them underactuated systems. In this table, the observation spaces solely comprise generalized positions and velocities of the robots and do not take into account any environment observations. We use quaternions for the robot floating base orientation, which adds an additional position coordinate compared to the velocity components, which match the DoFs. In the appendix, Table III shows an exhaustive overview of all the robot configurations available in HumanoidBench. 

forearms of the dexterous Shadow Hands in HumanoidBench. While this is not currently a realistic model, we anticipate the trend in the industry towards developing slimmer, human-like hands (e.g., Tesla Optimus, Figure 01) so that our design choice aligns better with next-generation humanoid robots. In addition, we also provide models for the Robotiq 2F-85 parallel-jaw gripper and the 13-DoF Unitree hands available in the Unitree collection<sup>5</sup> (see Appendix, Section A for more details). 

The observation and action spaces, and degrees of freedom of the robot system with or without the dexterous hands are summarized in Table II. 

**Observations.** Our simulated environment supports the following observations: 

- Proprioceptive robot state (i.e., joint angles and velocities) and task-relevant environment observations (i.e., object poses and velocities). 

- Egocentric visual observations from two cameras placed on the robot head (see Figure 2). 

- Whole-body tactile sensing using the MuJoCo tactile grid sensor (see Figure 2). We design tactile sensing at the hands with high resolution and in other body parts with low resolution, similar to humans, with a total of 448 taxels spread over the entire body, each providing threedimensional contact force readings. Similar distributed force readings have been captured on real-world systems both on humanoid bodies [41] and end-effectors [53]. The implementation of such spatially distributed contact sensing required non-trivial mesh adaptations and refinements, which we detail in Appendix, Section B-D. 

Although other sensory inputs are available from the environment, to investigate challenges in whole-body control of humanoid robots, we first focus on the state-based environment setup, where proprioceptive robot states and object states are used as the agent’s input in HumanoidBench. In our statebased environment, we maintain the robot observations the same across tasks to minimize domain knowledge, in contrast to tailoring it to the specific tasks [59]. We leave extending 


Fig. 3: **HumanoidBench manipulation task suite.** We devise 15 benchmarking whole-body manipulation tasks that cover a wide variety of interactions and difficulties. This figure illustrates an initial state for each task (left) and examples of the robot performing such tasks (right). 

our environment to benchmarking multimodal perception capabilities [65, 54] of humanoid robots as future work. 

**Actions.** In HumanoidBench, the humanoid robot is controlled via position control (i.e., specifying the target joint positions). Torque-based control is also supported but we found that position control is generally more stable and allows for lower control frequency than torque control. For both position and torque control, the action space is 61-dimensional including the two hands, and controlled at 50 Hz. 

### IV. HUMANOIDBENCH 

Humanoid robots promise to solve human-like tasks in human-tailored environments, possibly using human tools. However, their form factor and hardware challenges make real-world research challenging, making simulation a crucial tool to advance algorithmic research in the field. 

To this end, we present HumanoidBench, a humanoid benchmark for robot learning and control, which features a 


Fig. 4: **HumanoidBench locomotion task suite.** We devise 12 benchmarking locomotion tasks that cover a wide variety of interactions and difficulties. This figure illustrates an initial state for each task (left) and examples of the robot performing such tasks (right). 

high-dimensional action space (up to 61 different actuators) and enables research in complex whole-body coordination. 

We benchmark 27 tasks, consisting of 12 locomotion tasks and 15 distinct manipulation tasks, as illustrated in Figure 4 and Figure 3. A set of locomotion tasks aim to provide interesting but simpler humanoid control scenarios, bypassing intricate dexterous hand control. On the other hand, wholebody manipulation tasks render a comprehensive evaluation of the state-of-the-art algorithms on challenging tasks with unique challenges that require coordination across the entire robot body, ranging from toy examples (e.g., pushing a box on a table) to practical applications (e.g., truck unloading, shelf rearrangement). 

In this section, we briefly describe the tasks in our benchmark task suite. Further details about each of the tasks, including task initialization, reward functions, as well as different variations of the tasks, are provided in Appendix, Section B-E. 

_A. Locomotion Tasks_ 

- walk: Keep forward velocity (in the global _x_ -direction) close to 1 m _/_ s without falling to the ground. 

- stand: Maintain a standing pose throughout the provided amount of time. 

- run: Run forward at a speed of 5 m _/_ s. 

- reach: Reach a randomly initialized 3D point with the left hand. 

- hurdle: Keep forward velocity close to 5 m _/_ s while successfully overcoming hurdles. 

- crawl: Keep forward velocity close to 1 m _/_ s while passing inside a tunnel. 

- maze: Reach the goal position in a maze by taking multiple turns at the intersections. 

- sit: Sit onto a chair situated closely behind the robot. 

- balance: Stay balanced on the unstable board. 

- stair: Traverse an iterating sequence of upward and 


Fig. 5: **Learning curves of RL algorithms (locomotion).** The curves are averaged over three random seeds and the shaded regions represent the standard deviation. Returns are computed by summing the rewards at all timesteps of an episode. The dashed lines qualitatively indicate task success. We run PPO on the walk task but it is not visible in the plot since it only achieves very low returns. 

downward stairs at 1 m _/_ s. 

- slide: Walk over an iterating sequence of upward and downward slides at 1 m _/_ s. 

- pole: Travel in forward direction over a dense forest of high thin poles, without colliding with them. 

### _B. Whole-Body Manipulation Tasks_ 

- push: Move a box to a randomly initialized 3D point on a table. 

- cabinet: Open four different types of cabinet doors (e.g., hinge doors, sliding door, drawer). 

- highbar: Athletically swing while staying attached to a horizontal high bar until reaching a vertical upside-down position. 

- door: Pull a door and traverse it while keeping the door open. 

- truck: Unload packages from a truck by moving them onto a platform. 

- cube: Manipulate two cubes in-hand until they both reach a randomly initialized target orientation. 

- bookshelf: Pick and place several items across shelves in a given order. 

- basketball: Catch a ball coming from random directions and throw it into the basket. 

- window: Grab a window wiping tool and keep its tip parallel to a window by following a prescribed vertical velocity. 

- spoon: Grab a spoon and use it to follow a circular pattern inside a pot. 

- kitchen [17]: Execute a sequence of actions in a kitchen environment, namely, open a microwave door, move a kettle, and turning burner and light switches. 

- package: Move a box to a randomly initialized target position. 

- powerlift: Lift a barbell shaped object of a designated mass. 


Fig. 6: **Learning curves of RL algorithms (manipulation).** The curves are averaged over three random seeds and the shaded regions represent the standard deviation. The dashed lines qualitatively indicate task success. Note that kitchen is the only environment with a purely discrete, sparse reward, with a maximum of 4. 

- room: Organize a 5 m by 5 m space populated with randomly scattered object to minimize the variance of scattered objects’ locations in _x_ , _y_ -axis directions. 

- insert: Insert the ends of a rectangular peg into two tight target blocks. 

### V. BENCHMARKING RESULTS 

To identify the challenges in learning with humanoid robots, we benchmark reinforcement learning (RL) algorithms on HumanoidBench, which promises for robots to learn from their own experience. Remarkably, this class of algorithms 

requires limited domain expertise and does not necessarily rely on expert demonstrations, which are not only expensive but also challenging to collect for humanoid robots.<sup>7</sup> 

### _A. Baselines_ 

We evaluate all tasks in our benchmark with four RL methods (DreamerV3, TD-MPC2, SAC, PPO). Please refer to Appendix, Section C for implementation details. 

> 7While we do not benchmark classical model-based control approaches [14, 26] in this work, our environments support actions obtained by using any type of controllers. 

- **DreamerV3** [20]: the state-of-the-art model-based RL algorithm, learning from imaginary model rollouts. 

- **TD-MPC2** [21]: the state-of-the-art model-based RL algorithm with online planning. 

- **SAC** (Soft Actor-Critic [18]): the state-of-the-art off-policy model-free RL algorithm. 

- **PPO** (Proximal Policy Optimization [52]): the state-ofthe-art on-policy model-free RL algorithm. 

### _B. Results_ 

We report benchmarking results in Figure 5 and Figure 6, where we ran each of the algorithms for approximately 48 hours, resulting in the visible differences in environment steps (e.g., 2M steps for TD-MPC2, 10M steps for DreamerV3). We only run PPO on a subset of tasks (walk, kitchen, door, package), given its inferior performance without massive parallelization. Each of the environments is evaluated with a combination of dense rewards and sparse subtask completion rewards, and for each of these we provide qualitative measures of task success (see dashed lines in Figure 5 and Figure 6). A detailed description of the reward functions used for each environment is available in Appendix, Section B-E. 

All the baseline algorithms perform below the success threshold on most tasks, particularly struggling on tasks that require long-horizon planning and intricate whole-body coordination in a high-dimensional action space. Surprisingly, these state-of-the-art RL algorithms require a large number of steps to learn even simple locomotion tasks, such as walk, which has been extensively studied with a simplified humanoid agent in the DeepMind Control Suite [59]. 

This poor performance is mainly attributed to _the highdimensionality of the state and action spaces_ of our humanoid robot agent with dexterous hands. Although the hands of the humanoid robot are barely used for most locomotion tasks, the RL algorithms fail to ignore this information, which makes policy learning challenging. In addition, these high-dimensional state and action spaces result in a much larger exploration space, which makes exploration slow or infeasible with simple maximum entropy approaches. This implies the need for incorporating behavioral priors or commonsense knowledge about the world that can ease the exploration problem, when it comes to learning on more complex agents, like humanoid robots. We investigate this further in Section V-C. 

This problem becomes even more severe in manipulation tasks, resulting in particularly low rewards in all such tasks. Before learning any manipulation skills, an agent must learn locomotion skills to balance and move towards an object or the world to interact. All the policies barely learn to stabilize using the dense reward, but struggle to learn any complex manipulation skills. 

### _C. With Hands vs. Alternative Configurations_ 

**With Hands vs. Without Hands.** As discussed in Section V-B, controlling humanoid robots with dexterous hands is challenging due to their high degrees of freedom and complex dynamics. Thus, we investigate the difficulty of RL 


Fig. 7: **Performance with and without dexterous hands.** The curves are averaged over three random seeds and the shaded regions represent the standard deviation. 

training with a large action space (i.e., additional 42 dimensions with two dexterous Shadow Hands) on walk that does not necessarily require to control dexterous hands. The results in Figure 7 show that the presence of hands, with their additional joints and actuators, leads to a large decrease in performance compared to training the same task without the dexterous hands (see differences in observation and action space in Table II). 

**Reduced Action Space.** To verify whether such difficulties stem from the dimensionality of the action space, we benchmark our full robot model, but fix the actuation of the hands (42D), which we set to zero. In this way, the action dimensionality is reduced from 61D in the original model to 19D. Note that the observations and masses induced by the presence of the hands are retained (i.e., observation space remains 151D). Figure 7 shows that the RL algorithms learn significantly faster in the reduced action space setup than the ones trained with the full action space. This confirms that most of the performance drop is indeed due to the increased action dimensionality. 

We observe similar trends in the more complex manipulation task, push, which presents substantially different dynamics in the task approach (e.g., pushing with and without hands). 

### _D. Flat vs. Hierarchical Reinforcement Learning_ 

As shown in the previous subsection, flat, end-to-end RL approaches fail to learn most of the tasks in HumanoidBench. Many of such tasks require long-horizon planning and necessitate acquiring a diverse set of skills (e.g., balancing, walking, reaching). These tasks can be addressed by hierarchical RL, which introduces additional structure into the learning problem. In HRL, one or multiple low-level skill policies are provided to a high-level planning policy that outputs setpoints for the lower-level policies. In practice, such setpoints comprise the action space of the high-level policy. This framework is very general, and there are no constraints on how to obtain both low-level and high-level policies. However, here we focus on training both of these through reinforcement learning [56]. 

**Hierarchical RL Implementation.** We implement a hierarchical RL approach on two manipulation tasks, namely, the push and package tasks. As a low-level skill, push uses a _one-hand reaching policy_ , which allows the robot to reach a 3D point in space with its left hand, while package uses a _two-hand reaching policy_ , where both hands are commanded 


Fig. 8: **Our hierarchical RL pipeline (a).** (b) A robust low-level reaching policy is pretrained using PPO in a MuJoCo MJX-based reaching environment, as shown in the top snapshot in (a). (c) The high-level policy then leverages the pretrained reaching policy to move to a desired position and learns to solve a downstream task, shown in the bottom snapshot in (a). Note that the reaching policy weights are frozen during the high-level policy training. 

to reach different 3D targets. Figure 8 illustrates the overview of our hierarchical RL implementation. 

**Low-level Reaching Policy Pretraining.** We treat the lowlevel reaching policy as a pretrained frozen block that can be reused across tasks. Since this policy does not improve during training of the high-level policy, it needs to be very _robust_ to cope with the continually shifting reaching targets that the high-level policy sets during exploration. However, the results in the previous section show that even a one-hand reaching task is hard to learn. 

On the other hand, while our experiments above confirm that PPO exhibits poor sample efficiency compared to the offpolicy algorithms, it is worth noting that PPO has achieved significant success in robotic locomotion by exploiting largescale parallelization of environments on GPUs [36]. To achieve robust reaching policies, we exploit hardware acceleration by pretraining the low-level reaching policies in the recently released MuJoCo MJX<sup>8</sup> , which enables training PPO on thousands of parallel environments. 

For low-level reaching policy training, we employ a simplified H1 model that only considers collisions between feet and ground in the MuJoCo MJX environments, as in our experience the advantages stemming from parallelization are largely reduced when considering all numerous humanoid geometries (hindering training of the more complex benchmark tasks via MJX). We also remove the hands from the model to further increase training efficiency. The simplified reaching task environments for pretraining reset the target once reached. To achieve robust low-level reaching policies, we apply force perturbations at each of the links during training. We train the one-hand reaching policy for 2 billion steps (36 hours) and the two-hand reaching policy for 4 billion steps (60 hours) on 32 _,_ 768 parallel environments. The pretrained reaching policies successfully transfer to the original (non-simplified, simulated in classical MuJoCo) humanoid environments. 

**High-level Policy Training.** Then, we use the pretrained reaching policies (frozen) as low-level policies and only train a high-level policy using either DreamerV3 and TD-MPC2 on 


Fig. 9: **Comparison between flat policies and hierarchical policies.** The curves are averaged over three random seeds and the shaded regions represent the standard deviation. 

the push and package tasks. To facilitate exploration, we restrict the range of reaching targets to the robot workspace. 

**Hierarchical RL Results.** In Figure 9, our hierarchical architecture significantly outperforms the flat, end-to-end baselines on the push task, achieving very high success rates with DreamerV3. While the low-level policy has undergone additional pretraining, this can be in principle reused across tasks. On the other hand, we note a less pronounced performance improvement in the more challenging package task. While getting closer to picking up the package with our hierarchical approach, the policy struggles in lifting it (having never experienced it during training). 

These results confirm that the tasks in our benchmark present challenges that can be addressed with a more structured approach to the learning problem, and we hope this stimulates further directions for future research. 

### _E. Common Failures_ 

In this subsection, we remark on notable challenges and common failures for some representative tasks in our benchmark, which denote the challenge in learning with high-dimensional action spaces and limited planning horizon of the state-of-theart RL algorithms. 

**_Common Failure on highbar._** In the highbar task, the Unitree H1 robot conservatively learns to maintain contact with the bar to avoid episode termination, but experiences 

8https://mujoco.readthedocs.io/en/stable/mjx.html 


Fig. 10: **Failure Scenarios.** This figure presents a selection of common failures that occur while training our benchmark tasks. 

difficulties in performing the whole-body rotation trajectory. This is indicative of short horizon planning and a recurrent challenge in many of the long-horizon benchmark tasks, despite the availability of dense rewards. 

**_Common Failure on door._** In the door task, the robot is well-guided to turn the door hatch to unlock the door, but it finds it challenging to learn the precise motion required to pull the door towards its opening position. This is mainly because pulling the door requires not only pulling its arm but also moving the whole body backwards. The coordination between multiple body parts and seamless interaction between manipulation and locomotion skills are common challenges in training humanoid robots. 

**_Common Failure on hurdle._** In the hurdle environment, the robot learns to run forward with the expected velocity but does not recognize the need to surpass the hurdle by jumping, which is a hard exploration problem. Previous work has shown that in OpenAI gym Walker2d, the forward-moving reward is sufficient to learn this behavior [29]. On the other hand, the humanoid robot finds conservative poses to collide with the hurdle such that it can stabilize without terminating the episode after hitting the obstacle, without further exploring high-reward jumping behaviors. 

### VI. CONCLUSION 

We presented HumanoidBench, a high-dimensional humanoid robot control benchmark. Ours is the first example of a comprehensive humanoid environment with a diversity of locomotion and manipulation tasks, ranging from toy examples to practical humanoid applications. We set a high bar with our complex tasks, in the hope to stimulate the community to accelerate the development of whole-body algorithms for such robotic platforms. 

**Future work.** HumanoidBench already includes multimodal high-dimensional observations in the form of egocentric vision and whole-body tactile sensing. While our experiments only benchmarked the performance of state-based environments, studying the interplay between different modalities is a compelling direction for future work. 

Extensions of the humanoid environment will also eventually include more realistic objects and environments with real-world diversity and higher-quality rendering. As for dexterous manipulation tasks, we envision screwing and furniture assembly tasks 

being part of our framework, given that they are particularly tailored for bimanual manipulation. 

Here we have focused on reinforcement learning algorithms because collecting physical demonstrations with humanoid robots is particularly challenging. However, we believe that other means could be employed to bootstrap learning (e.g., learning from human videos). 

Finally, while this was not the focus of our work, the impressive results obtained via domain randomization in the newly developed MuJoCo MJX show promise to study sim-toreal transfer in more depth, following the large success of the field in quadrupedal locomotion [23]. 

### ACKNOWLEDGMENTS 

This work was supported in part by the SNSF Postdoc Mobility Fellowship 211086, ONR MURI N00014-22-1-2773, BAIR Industrial Consortium, Komatsu, InnoHK Centre for Logistics Robotics, an ONR DURIP grant, the Institute of Information & Communications Technology Planning & Evaluation (IITP) grant and the National Research Foundation of Korea (NRF) grant funded by the Korean government (MSIT) (RS-2020-II201361, Artificial Intelligence Graduate School Program (Yonsei University) and RS-2024-00333634). We also thank Google TPU Research Cloud (TRC) for granting us access to TPUs for research. 

### REFERENCES 

- [1] Alphonsus Adu-Bredu, Grant Gibson, and Jessy Grizzle. Exploring kinodynamic fabrics for reactive whole-body control of underactuated humanoid robots. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 10397–10404. IEEE, 2023. 

- [2] Ilge Akkaya, Marcin Andrychowicz, Maciek Chociej, Mateusz Litwin, Bob McGrew, Arthur Petron, Alex Paino, Matthias Plappert, Glenn Powell, Raphael Ribas, et al. Solving rubik’s cube with a robot hand. _arXiv preprint arXiv:1910.07113_ , 2019. 

- [3] Firas Al-Hafez, Guoping Zhao, Jan Peters, and Davide Tateo. Locomujoco: A comprehensive imitation learning benchmark for locomotion. _6th Robot Learning Workshop at NeurIPS_ , 2023. 

- [4] Pierre-Luc Bacon, Jean Harb, and Doina Precup. The option-critic architecture. In _Association for the Advancement of Artificial Intelligence_ , pages 1726–1734, 2017. 

- [5] M. G. Bellemare, Y. Naddaf, J. Veness, and M. Bowling. The arcade learning environment: An evaluation platform for general agents. _Journal of Artificial Intelligence Research_ , 47:253–279, jun 2013. 

- [6] Cameron H Berg, Vittorio Caggiano, and Vikash Kumar. SAR: Generalization of Physiological Dexterity via Synergistic Action Representation. In _Robotics: Science and Systems_ , 2023. 

- [7] Greg Brockman, Vicki Cheung, Ludwig Pettersson, Jonas Schneider, John Schulman, Jie Tang, and Wojciech Zaremba. Openai gym. _arXiv preprint arXiv:1606.01540_ , 2016. 

- [8] Vittorio Caggiano, Huawei Wang, Guillaume Durandau, Massimo Sartori, and Vikash Kumar. Myosuite: A contactrich simulation suite for musculoskeletal motor control. In _Learning for Dynamics and Control_ , pages 492–507. PMLR, 2022. 

- [9] Vittorio Caggiano, Sudeep Dasari, and Vikash Kumar. Myodex: a generalizable prior for dexterous manipulation. In _International Conference on Machine Learning_ , pages 3327–3346. PMLR, 2023. 

- [10] Yuanpei Chen, Yiran Geng, Fangwei Zhong, Jiaming Ji, Jiechuang Jiang, Zongqing Lu, Hao Dong, and Yaodong Yang. Bi-dexhands: Towards human-level bimanual dexterous manipulation. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2023. 

- [11] Xuxin Cheng, Yandong Ji, Junming Chen, Ruihan Yang, Ge Yang, and Xiaolong Wang. Expressive wholebody control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 

- [12] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Robotics: Science and Systems_ , 2023. 

- [13] Yan Duan, Marcin Andrychowicz, Bradly Stadie, Jonathan Ho, Jonas Schneider, Ilya Sutskever, Pieter Abbeel, and Wojciech Zaremba. One-shot imitation learning. In _Advances in Neural Information Processing Systems_ , pages 1087–1098, 2017. 

- [14] Siyuan Feng, Eric Whitman, X Xinjilefu, and Christopher G Atkeson. Optimization based full body control for the atlas robot. In _2014 IEEE-RAS International Conference on Humanoid Robots_ , pages 120–127. IEEE, 2014. 

- [15] Zipeng Fu, Tony Z Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. 

- [16] Dibya Ghosh. dibyaghosh/jaxrl <u>m,</u> 2023. URL https: //github.com/dibyaghosh/jaxrl <u>m.</u> 

- [17] Abhishek Gupta, Vikash Kumar, Corey Lynch, Sergey Levine, and Karol Hausman. Relay policy learning: Solving long-horizon tasks via imitation and reinforcement learning. _Conference on Robot Learning_ , 2019. 

- [18] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In _International Conference on Machine Learning_ , pages 1856–1865, 2018. 

- [19] Tuomas Haarnoja, Ben Moran, Guy Lever, Sandy H Huang, Dhruva Tirumala, Markus Wulfmeier, Jan Humplik, Saran Tunyasuvunakool, Noah Y Siegel, Roland Hafner, Michael Bloesch, Kristian Hartikainen, Arunkumar Byravan, Leonard Hasenclever, Yuval Tassa, Fereshteh Sadeghi, Nathan Batchelor, Federico Casarini, Stefano Saliceti, Charles Game, Neil Sreendra, Kushal Patel, Marlon Gwira, Andrea Huber, Nicole Hurley, Francesco Nori, Raia Hadsell, and Nicolas Heess. Learn- 

ing agile soccer skills for a bipedal robot with deep reinforcement learning. _arXiv preprint arXiv:2304.13653_ , 2023. 

- [20] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [21] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. In _International Conference on Learning Representations_ , 2024. 

- [22] Minho Heo, Youngwoon Lee, Doohyun Lee, and Joseph J. Lim. Furniturebench: Reproducible real-world benchmark for long-horizon complex manipulation. In _Robotics: Science and Systems_ , 2023. 

- [23] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. 

- [24] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J. Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 2020. 

- [25] Harini Kannan, Danijar Hafner, Chelsea Finn, and Dumitru Erhan. Robodesk: A multi-task reinforcement learning benchmark. https://github.com/google-research/ robodesk, 2021. 

- [26] Scott Kuindersma, Robin Deits, Maurice Fallon, Andres´ Valenzuela, Hongkai Dai, Frank Permenter, Twan Koolen, Pat Marion, and Russ Tedrake. Optimization-based locomotion planning, estimation, and control design for the atlas humanoid robot. _Autonomous robots_ , 40:429– 455, 2016. 

- [27] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. Rma: Rapid motor adaptation for legged robots. In _Robotics: Science and Systems_ , 2021. 

- [28] Seunghwan Lee, Moonseok Park, Kyoungmin Lee, and Jehee Lee. Scalable muscle-actuated human simulation and control. _ACM Transactions on Graphics_ , 38(4):1–13, 2019. 

- [29] Youngwoon Lee, Shao-Hua Sun, Sriram Somasundaram, Edward S. Hu, and Joseph J. Lim. Composing complex skills by learning transition policies. In _International Conference on Learning Representations_ , 2019. URL https://openreview.net/forum?id=rygrBhC5tQ. 

- [30] Youngwoon Lee, Jingyun Yang, and Joseph J. Lim. Learning to coordinate manipulation skills via skill behavior diversification. In _International Conference on Learning Representations_ , 2020. 

- [31] Youngwoon Lee, Edward S Hu, and Joseph J Lim. IKEA furniture assembly environment for long-horizon complex manipulation tasks. In _IEEE International Conference on Robotics and Automation_ , 2021. URL https://clvrai.com/ furniture. 

- [32] Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto Mart´ın-Mart´ın, Chen Wang, Gabrael Levine, Michael Lingelbach, Jiankai 

Sun, Mona Anvari, Minjune Hwang, Manasi Sharma, Arman Aydin, Dhruva Bansal, Samuel Hunter, Kyu-Young Kim, Alan Lou, Caleb R Matthews, Ivan Villa-Renteria, Jerry Huayang Tang, Claire Tang, Fei Xia, Silvio Savarese, Hyowon Gweon, Karen Liu, Jiajun Wu, and Li Fei-Fei. Behavior-1k: A benchmark for embodied ai with 1,000 everyday activities and realistic simulation. In _Conference on Robot Learning_ , 2022. 

- [33] L-J Lin. Hierarchical learning of robot skills by reinforcement. In _IEEE International Conference on Neural Networks_ , pages 181–186. IEEE, 1993. 

- [34] Xingyu Lin, Yufei Wang, Jake Olkin, and David Held. Softgym: Benchmarking deep reinforcement learning for deformable object manipulation. In _Conference on Robot Learning_ , 2020. 

- [35] Chris Lu, Jakub Kuba, Alistair Letcher, Luke Metz, Christian Schroeder de Witt, and Jakob Foerster. Discovered policy optimisation. _Advances in Neural Information Processing Systems_ , 35:16455–16468, 2022. 

- [36] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, and Gavriel State. Isaac gym: High performance gpu based physics simulation for robot learning. In _Neural Information Processing Systems Datasets and Benchmarks Track_ , 2021. 

- [37] Ajay Mandlekar, Danfei Xu, Josiah Wong, Soroush Nasiriany, Chen Wang, Rohun Kulkarni, Li Fei-Fei, Silvio Savarese, Yuke Zhu, and Roberto Mart´ın-Mart´ın. What matters in learning from offline human demonstrations for robot manipulation. In _Conference on Robot Learning_ , 2021. 

- [38] Dominik Mattern, Pierre Schumacher, Francisco M Lopez,´ Marcel C Raabe, Markus R Ernst, Arthur Aubret, and Jochen Triesch. Mimo: A multi-modal infant model for studying cognitive development. _IEEE Transactions on Cognitive and Developmental Systems_ , 2024. 

- [39] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 2022. 

- [40] Josh Merel, Saran Tunyasuvunakool, Arun Ahuja, Yuval Tassa, Leonard Hasenclever, Vu Pham, Tom Erez, Greg Wayne, and Nicolas Heess. Catch & carry: reusable neural controllers for vision-guided whole-body tasks. _ACM Transactions on Graphics_ , 39(4):39–1, 2020. 

- [41] Philipp Mittendorfer and Gordon Cheng. Humanoid multimodal tactile-sensing modules. _IEEE Transactions on robotics_ , 27(3):401–410, 2011. 

- [42] Ofir Nachum, Shixiang Shane Gu, Honglak Lee, and Sergey Levine. Data-efficient hierarchical reinforcement learning. In _Advances in Neural Information Processing Systems_ , pages 3303–3313, 2018. 

- [43] Yashraj Narang, Kier Storey, Iretiayo Akinola, Miles Macklin, Philipp Reist, Lukasz Wawrzyniak, Yunrong 

Guo, Adam Moravanszky, Gavriel State, Michelle Lu, Ankur Handa, and Dieter Fox. Factory: Fast contact for robotic assembly. In _Robotics: Science and Systems_ , 2022. 

- [44] OpenAI, Marcin Andrychowicz, Bowen Baker, Maciek Chociej, Rafal Jozefowicz, Bob McGrew, Jakub Pachocki, Arthur Petron, Matthias Plappert, Glenn Powell, Alex Ray, Jonas Schneider, Szymon Sidor, Josh Tobin, Peter Welinder, Lilian Weng, and Wojciech Zaremba. Learning dexterous in-hand manipulation. _The International Journal of Robotics Research_ , 39(1):3–20, 2020. 

- [45] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions on Graphics_ , 37(4):1–14, 2018. 

- [46] Xue Bin Peng, Angjoo Kanazawa, Jitendra Malik, Pieter Abbeel, and Sergey Levine. Sfv: Reinforcement learning of physical skills from videos. _ACM Transactions on Graphics_ , 37(6):1–14, 2018. 

- [47] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics_ , 40(4):1–20, 2021. 

- [48] Karl Pertsch, Youngwoon Lee, and Joseph J. Lim. Accelerating reinforcement learning with learned skill priors. In _Conference on Robot Learning_ , 2020. 

- [49] Matthias Plappert, Marcin Andrychowicz, Alex Ray, Bob McGrew, Bowen Baker, Glenn Powell, Jonas Schneider, Josh Tobin, Maciek Chociej, Peter Welinder, Vikash Kumar, and Wojciech Zaremba. Multi-goal reinforcement learning: Challenging robotics environments and request for research. _arXiv preprint arXiv:1802.09464_ , 2018. 

- [50] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Learning humanoid locomotion with transformers. _arXiv preprint arXiv:2303.03381_ , 2023. 

- [51] Antonin Raffin, Ashley Hill, Maximilian Ernestus, Adam Gleave, Anssi Kanervisto, and Noah Dormann. Stable baselines3, 2019. 

- [52] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [53] Carmelo Sferrazza and Raffaello D’Andrea. Sim-to-real for high-resolution optical tactile sensing: From images to three-dimensional contact force distributions. _Soft Robotics_ , 9(5):926–937, 2022. 

- [54] Carmelo Sferrazza, Younggyo Seo, Hao Liu, Youngwoon Lee, and Pieter Abbeel. The power of the senses: Generalizable manipulation from vision and touch through masked multimodal learning. _arXiv preprint arXiv:2311.00924_ , 2023. 

- [55] Sanjana Srivastava, Chengshu Li, Michael Lingelbach, Roberto Mart´ın-Mart´ın, Fei Xia, Kent Elliott Vainio, Zheng Lian, Cem Gokmen, Shyamal Buch, Karen Liu, Silvio Savarese, Hyowon Gweon, Jiajun Wu, and Li Fei-Fei. Behavior: Benchmark for everyday household activities in virtual, interactive, and ecological environments. In 

_Conference on Robot Learning_ , 2021. 

- [56] Richard S Sutton, Doina Precup, and Satinder Singh. Between mdps and semi-mdps: A framework for temporal abstraction in reinforcement learning. _Artificial intelligence_ , 112(1-2):181–211, 1999. 

- [57] Andrew Szot, Alex Clegg, Eric Undersander, Erik Wijmans, Yili Zhao, John Turner, Noah Maestre, Mustafa Mukadam, Devendra Chaplot, Oleksandr Maksymets, Aaron Gokaslan, Vladimir Vondrus, Sameer Dharur, Franziska Meier, Wojciech Galuba, Angel Chang, Zsolt Kira, Vladlen Koltun, Jitendra Malik, Manolis Savva, and Dhruv Batra. Habitat 2.0: Training home assistants to rearrange their habitat. In _Neural Information Processing Systems_ , 2021. 

- [58] Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, Timothy P. Lillicrap, and Martin A. Riedmiller. Deepmind control suite. _arXiv preprint arXiv:1801.00690_ , 2018. 

- [59] Yuval Tassa, Saran Tunyasuvunakool, Alistair Muldal, Yotam Doron, Siqi Liu, Steven Bohez, Josh Merel, Tom Erez, Timothy Lillicrap, and Nicolas Heess. dm <u>control:</u> Software and tasks for continuous control. _arXiv preprint arXiv:2006.12983_ , 2020. 

Pete Florence, Andy Zeng, and Pieter Abbeel. Robopianist: Dexterous piano playing with deep reinforcement learning. In _Conference on Robot Learning_ , pages 2975– 2994. PMLR, 2023. 

   - [68] Haotian Zhang, Ye Yuan, Viktor Makoviychuk, Yunrong Guo, Sanja Fidler, Xue Bin Peng, and Kayvon Fatahalian. Learning physically simulated tennis skills from broadcast videos. _ACM Transactions on Graphics_ , 42(4):1–14, 2023. 

   - [69] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _Robotics: Science and Systems_ , 2023. 

   - [70] Yuke Zhu, Josiah Wong, Ajay Mandlekar, and Roberto Mart´ın-Mart´ın. robosuite: A modular simulation framework and benchmark for robot learning. _arXiv preprint arXiv:2009.12293_ , 2020. 

   - [71] Ziwen Zhuang, Zipeng Fu, Jianren Wang, Christopher G Atkeson, Soren¨ Schwertfeger, Chelsea Finn, and Hang Zhao. Robot parkour learning. In _Conference on Robot Learning_ , 2023. 

- [60] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033, 2012. 

- [61] Yinhuai Wang, Jing Lin, Ailing Zeng, Zhengyi Luo, Jian Zhang, and Lei Zhang. Physhoi: Physics-based imitation of dynamic human-object interaction. _arXiv preprint arXiv:2312.04393_ , 2023. 

- [62] Xinyue Wei, Minghua Liu, Zhan Ling, and Hao Su. Approximate convex decomposition for 3d meshes with collision-aware concavity and tree search. _ACM Transactions on Graphics (TOG)_ , 41(4):1–18, 2022. 

- [63] Zhaoming Xie, Jonathan Tseng, Sebastian Starke, Michiel van de Panne, and C Karen Liu. Hierarchical planning and control for box loco-manipulation. _Symposium on Computer Animation_ , 2023. 

- [64] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Metaworld: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on Robot Learning_ , 2019. 

- [65] Ying Yuan, Haichuan Che, Yuzhe Qin, Binghao Huang, Zhao-Heng Yin, Kang-Won Lee, Yi Wu, Soo-Chul Lim, and Xiaolong Wang. Robot synesthesia: In-hand manipulation with visuotactile sensing. _arXiv preprint arXiv:2312.01853_ , 2023. 

- [66] Kevin Zakka, Yuval Tassa, and MuJoCo Menagerie Contributors. MuJoCo Menagerie: A collection of highquality simulation models for MuJoCo, 2022. URL http://github.com/google-deepmind/mujoco <u>menagerie.</u> 

- [67] Kevin Zakka, Philipp Wu, Laura Smith, Nimrod Gileadi, Taylor Howell, Xue Bin Peng, Sumeet Singh, Yuval Tassa, 


Fig. 11: Additional configurations available in HumanoidBench. 

## **Appendix** 

### **Table of Contents** 

|**Appendix A: **|**Additional Components**|14|
|---|---|---|
|**Appendix B: **|**Simulated Environment Details**|14|
|B-A|Observation Space . . . . . . . . . . . .|14|
|B-B|Action Space . . . . . . . . . . . . . . .|14|
|B-C|Simulation Performance . . . . . . . . .|14|
|B-D|Whole-body Tactile Sensing<br>. . . . . .|14|
|B-E|Task Specification . . . . . . . . . . . .|14|
|**Appendix C: **|**Training Details**|24|
|C-A|Baseline Implementation Details . . . .|24|
|C-B|Reaching Policy Implementation Details|24|
|C-C|Benchmarking Results . . . . . . . . . .|24|
||APPENDIXA<br>ADDITIONALCOMPONENTS||


In addition to the Unitree H1 robot, we also include model files for the Agility Robotics Digit humanoid (see Figure 11). We add a custom head, together with egocentric vision and whole-body tactile sensing, similarly to the H1. We provide a torque controlled version of this robot. We also provide a torque controlled version of the more recent Unitree G1 humanoid. 

For the broader use of HumanoidBench, we also provide two simple end-effector options for the Unitree H1 robot: a 2-DoF Robotiq 2F-45 parallel-jaw gripper (with a rotational wrist joint), and a 13-DoF dexterous Unitree hand available in the Unitree model collection.<sup>5</sup> 

Specifications for all these variants are detailed in Table III. 

### APPENDIX B 

### SIMULATED ENVIRONMENT DETAILS 

### _A. Observation Space_ 

The observation space for the benchmarked H1 robot state (joint positions and velocities) comprises 151 dimensions, with 51 dimensions representing the humanoid robot body and 50 dimensions representing each hand. Table III summarizes observation spaces for other robotic configurations supported in HumanoidBench. The observation space can also include environment states for tasks interacting with objects, as described in detail in Section B-E. 

### _B. Action Space_ 

The action space is the same across all environments. We normalize the action space to be [ _−_ 1 _,_ 1]<sup>_∥A∥_</sup> , where _∥A∥_ = 61 (19 for the humanoid body and 21 for each hand). We use position control for the benchmarking results in this paper. 

### _C. Simulation Performance_ 

HumanoidBench is based on MuJoCo [60], which provides fast and accurate physics simulation. We provide a diverse set of configurations, such as the full humanoid model with two hands, the humanoid model without hands, and the humanoid model with collision meshes only on its feet. We use the fastest model (i.e., collision meshes only on feet) to train the low-level reaching policies, described in Section C-B. 

We benchmark our HumanoidBench simulation using the Unitree H1 model and report its performance in Table IV. Even with complex humanoid body and dexterous hands, HumanoidBench can run 1000+ FPS on a single CPU with a simulation timestep of 0 _._ 002 s. 

### _D. Whole-body Tactile Sensing_ 

We implement whole-body tactile sensing by employing MuJoCo touch grid, which aggregates pressure and shear contact forces into discrete bins. Similar distributed force readings have been captured on real-world systems both on humanoid bodies [41] and end-effectors [53]. To increase the number of contact point candidates and fully exploit the spatial resolution of the touch grid, we subdivide the original meshes into many smaller meshes. Specifically, we build on top of CoACD [62], which in addition makes sure that the resulting meshes are all convex. This procedure results in finer contact resolution when the MuJoCo physics engine computes collisions. An example is depicted in Figure 12, with a larger number of contact points generally resulting in a considerably better discretization of the tactile readings. The full model with refined meshes and tactile readings runs at 550 FPS. 

### _E. Task Specification_ 

Before enumerating the environment details below, let us define auxiliary functions and variables that are employed in the reward functions of multiple environments: 

- _tol_ ( _x,_ ( _x_ lower _, x_ upper) _, m_ ) is a function provided in the DeepMind Control Suite package [59]. This is denoted 

||H1 w/o hands|H1 w/ ShadowHand|H1 w/ Robotiq gripper|H1 w/ Unitree hand|Digit w/ ShadowHand|Unitree G1|
|---|---|---|---|---|---|---|
|Observation space|51|151|55|103|221|87|
|Action space|19|61|23|45|65|37|
|DoF (body)|25|25|25|25|57|29|
|DoF (2 end-effectors)|0|50|4|26|50|14|


TABLE III: **All supported robot specifications** . Note that the observation space in this table does not take into account any observations of the surrounding environment and solely comprises generalized positions and velocities. We use quaternions for the robot floating base orientation, as well as for ball joints, which add additional position coordinates compared to the velocity components (which match the DoFs). 

|**Configuration**|**FPS**|
|---|---|
|Without hands|2450|
|Simplified body collisions|3600|
|Collisions only for feet|5100|
|**Default**|1050|


TABLE IV: **HumanoidBench Simulation Performance.** 

there as a _tolerance_ function that returns 1 when the evaluated value is within the bounds, i.e., _x ∈_ ( _x_ lower _, x_ upper), and between 0 and 1 otherwise. The margin _m_ regulates the slope of the function, i.e., how far from the bounds the function approaches 0. 

- _height_ (( _x_ lower _, x_ upper) _, m_ ) is a variable defined as _tol_ ( _z_ head _,_ ( _x_ lower _, x_ upper) _, m_ ) that rewards the head height, where _z_ head is the vertical coordinate of the robot head position. Whenever the arguments are not indicated, we assume _x_ lower = 1 _._ 65, _x_ upper = + _∞_ , and _m_ = 0 _._ 4125. 

- _d_ ( _object_ A _, object_ B) is the distance between object A and object B. 

- _upright_ (( _x_ lower _, x_ upper) _, m_ ) is a variable defined as _tol_ ( _z_ proj _,_ ( _x_ lower _, x_ upper) _, m_ ), which rewards the alignment of the robot torso with respect to the vertical axis, where _z_ proj is the unit projection of the _z_ -axis in the robot body frame onto the _z_ -axis in the global frame. Whenever the arguments are not indicated, we assume _x_ lower = 0 _._ 9, _x_ upper = + _∞_ , and _m_ = 1 _._ 9. 

- _stand_ := _height × upright_ represents a standing posture reward. 

- _e_ := 0 _._ 2 _·_ �4 + _|u_ <u>1</u> _|_ � _i_<sup>_tol_(</sup><sup>_ui,_(0</sup><sup>_,_0)</sup><sup>_,_10)</sup> � rewards small control effort, where _u_ is the vector of actuation inputs. 

- _stable_ = _stand × e_ , densely rewards stable standing configurations. 

- _vx_ is the robot velocity in the _x_ direction (positive forward) of the robot body coordinate frame. 

- _vy_ is the robot velocity in the _y_ direction (positive left) of the robot body coordinate frame. 

- _z_ item is the vertical _z_ coordinate of the indicated ‘item’ in the global frame. 

- _pos_ item is the 3D position of the indicated ‘item’ in the global frame. 

- _1) walk:_ 


**_Objective._** Keep forward velocity close to 1 m _/_ s without falling to the ground. 

**_Observation._** Joint positions and velocities of the robot. **_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 2. 

### **_Reward Implementation._** 

_R_ ( _s, a_ ) = _stable × tol_ ( _vx,_ (1 _,_ + _∞_ ) _,_ 1) _._ 

- _2) stand:_ 


**_Objective._** Maintain a standing pose. **_Observation._** Joint positions and velocities of the robot. **_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** Let: 

- _stillx_ = _tol_ ( _vx,_ (0 _,_ 0) _,_ 2) 

- _stilly_ = _tol_ ( _vy,_ (0 _,_ 0) _,_ 2), 

Then: 

- _R_ ( _s, a_ ) = _stable × mean_ ( _stillx, stilly_ ) 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 2. 

with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** 

_R_ ( _s, a_ ) = _stable × tol_ ( _vx,_ (5 _, ∞_ ) _,_ 5) 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 2. 

_4) sit:_ 


(a) Refined meshes 


(b) Contact before refinement 

(c) Contact after refinement 

Fig. 12: **Refinement of collision meshes.** As a result of the mesh refinement (see (a), where each colored section indicates a different collision mesh), our model can detect a higher number of contact points, as shown by the yellow disks in the figure. This results in a better spatial discretization of the tactile readings. 

**_Objective._** Sit onto a chair situated closely behind the robot. **_Observation._** In sit_simple, the observation is a vector containing all joint positions on the robot unit. In sit_hard, we allow the chair to be moved, and the robot initial position is randomized, so the observation includes position and orientation of the chair as well. 

**_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. Note that in sit_hard, the robot is rotated at a random angle _α ∈_ [ _−_ 1 _._ 8 rad _,_ 1 _._ 8 rad] with position initialized at random values _x ∈_ [0 _._ 2 _,_ 0 _._ 4] _, y ∈_ [ _−_ 0 _._ 15 _,_ 0 _._ 15] 

**_Reward Implementation._** Let 

- _sittingx_ = _tol_ ( _xrobot − xchair,_ ( _−_ 0 _._ 19 _,_ 0 _._ 19) _,_ 0 _._ 2 

- _sittingy_ = _tol_ ( _yrobot − ychair,_ (0 _,_ 0) _,_ 0 _._ 1 

- _sittingz_ = _tol_ ( _zrobot,_ (0 _._ 68 _,_ 0 _._ 72) _,_ 0 _._ 2) 

- _posture_ = _tol_ ( _z_ head _− z_ IMU _,_ (0 _._ 35 _,_ 0 _._ 45) _,_ 0 _._ 3) 

- _stillx_ = _tol_ ( _vx,_ (0 _,_ 0) _,_ 2) 

- _stilly_ = _tol_ ( _vy,_ (0 _,_ 0) _,_ 2) 

then, the reward of this task is 

- _R_ ( _s, a_ ) = ((0 _._ 5 _· sittingz_ + 0 _._ 5 _· sittingx × sittingy_ ) 

   - _× upright × posture_ ) 

   - _× e × mean_ ( _stillx, stilly_ ) 

_3) run:_ 


**_Objective._** Keep forward velocity close to 5 m _/_ s without falling to the ground. 

**_Observation._** Joint positions and velocities of the robot. **_Initialization._** The robot is initialized to a standing position, 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 5. 

- _5) balance:_ 


**_Objective._** Balance on the unstable board. There are two variants to this environment: the balance_simple variant’s 

spherical pivot beneath the board does not move, while the balance_hard variant’s pivot does. 

**_Observation._** The observation comprises the joint positions and velocities of the robot and those of the board. 

**_Initialization._** The robot is initialized to a standing position on the unstable board, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

- _stillx_ = _tol_ ( _vx,_ (0 _,_ 0) _,_ 2) 

- _stilly_ = _tol_ ( _vy,_ (0 _,_ 0) _,_ 2) 

- _still_ =<sup><u>1</u></sup> 2<sup>(</sup><sup>_stillx_+</sup><sup>_stilly_)</sup> 

- _height_ robot = _height_ ((2 _._ 15 _,_ + _∞_ )) 

Then: 

_R_ ( _s, a_ ) = ( _e × still_ ) _×_ ( _height_ robot _× upright_ ) 


**_Objective._** Walk over an iterating sequence of upward and downward slides at 1 m _/_ s. 

**_Observation._** Joint positions and velocities of the robot. 

**_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

- _vertical_ foot,left = _tol_ ( _z_ head _− z_ foot,left _,_ (1 _._ 2 _,_ + _∞_ ) _,_ 0 _._ 45) 

**_Termination._** The episode terminates after 1000 steps, or when one of the following condition satisfies: 

- _zrobot <_ 0 _._ 8 

- The sphere collides with anything other than the floor and the standing board. 

- _vertical_ foot,right = _tol_ ( _z_ head _− z_ foot,right _,_ (1 _._ 2 _,_ + _∞_ ) _,_ 0 _._ 45) 

- Then: 

_R_ ( _s, a_ ) = _e × tol_ ( _vx,_ (1 _,_ + _∞_ ) _,_ 1) _× upright_ ((0 _._ 5 _,_ 1) _,_ 1 _._ 9) 

   - _×_ ( _vertical_ foot,left _× vertical_ foot,right) 

- The standing board collides with the floor. 

### _6) stair:_ 


**_Objective._** Traverse an iterating sequence of upward and downward stairs at 1 m _/_ s. 

**_Observation._** Joint positions and velocities of the robot. **_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

- _vertical_ foot,left = _tol_ ( _z_ head _− z_ foot,left _,_ (1 _._ 2 _,_ + _∞_ ) _,_ 0 _._ 45) 

- _vertical_ foot,right = _tol_ ( _z_ head _− z_ foot,right _,_ (1 _._ 2 _,_ + _∞_ ) _,_ 0 _._ 45) 

Then: 

_R_ ( _s, a_ ) = _e × tol_ ( _vx,_ (1 _,_ + _∞_ ) _,_ 1) _× upright_ ((0 _._ 5 _,_ 1) _,_ 1 _._ 9) _×_ ( _vertical_ foot,left _× vertical_ foot,right) 

**_Termination._** The episode terminates after 1000 steps, or when _z_ proj _<_ 0 _._ 1. 

_7) slide:_ 

**_Termination._** The episode terminates after 1000 steps, or when _z_ proj _<_ 0 _._ 6. 

### _8) pole:_ 


**_Objective._** Travel in forward direction over a dense forest of high thin poles, without colliding with them. 

**_Observation._** Joint positions and velocities of the robot. **_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 


Then, 

_R_ ( _s, a_ ) = _γ_ collision _×_ (0 _._ 5 _· stable_ + 0 _._ 5 _· tol_ ( _vx,_ (1 _,_ + _∞_ ) _,_ 1)) _._ 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 6. 

- _9) reach:_ 

_11) crawl:_ 


**_Objective._** Reach a randomly initialized 3D point with the left hand. 

**_Observation._** Joint positions and velocities of the robot, left hand position of robot, and reaching target position. 

**_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

- _d_ hand = _d_ ( _hand_ left _, goal_ ) 

- _health_ = 5 _· zpelvis,proj_ 


Then, 

_R_ ( _s, a_ ) = _−_ 10<sup>_−_4</sup> _· penaltymotion_ + _health_ + _close_ + _success_ 

**_Termination._** The episode terminates after 1000 steps. _10) hurdle:_ 


**_Objective._** Keep forward velocity close to 5 m _/_ s without falling to the ground. 

**_Observation._** Joint positions and velocities of the robot. 

**_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 


Then, we formulate the reward of this task as: 


**_Objective._** Keep forward velocity close to 1 m _/_ s while passing inside a tunnel. 

**_Observation._** Joint positions and velocities of the robot. **_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** Let: 

- _height_ crawl = _height_ ((0 _._ 6 _,_ 1) _,_ 1) 

- _height_ IMU = _tol_ ( _z_ IMU _,_ (0 _._ 6 _,_ 1) _,_ 1) 

- _quat_ crawl = �0 _._ 75 0 0 _._ 65 0<sup>�</sup> is the expected quaternion expected when the robot is crawling. 

- _orientation_ = _tol_ ( _∥quat_ pelvis _− quat_ crawl _∥,_ (0 _,_ 0) _,_ 1) rewards correct robot body orientation. 

- _tunnel_ = _tol_ ( _y_ IMU _,_ ( _−_ 1 _,_ 1) _,_ 0) rewards the robot when its _y_ coordinate is inside the tunnel. 

- _speed_ = _tol_ ( _vx,_ (1 _,_ + _∞_ ) _,_ 1) 

Then, the reward is formulated as: 

_R_ = _tunnel ×_ (0 _._ 1 _· e_ + 0 _._ 25 _·_ min( _height_ crawl _, height_ IMU) + 0 _._ 25 _· orientation_ + 0 _._ 4 _· speed_ ) 

**_Termination._** The episode terminates after 1000 steps. _12) maze:_ 


**_Objective._** Reach the goal position in a maze by taking multiple turns at the intersections. 

**_Observation._** Joint positions and velocities of the robot. 

**_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** For each checkpoint in the maze, we assign _vtarget_ to be the velocity prescribed to travel from the previous checkpoint towards next one. Then, let 

_• move_ = 


**_Termination._** The episode terminates after 1000 steps. 


We formulate the reward as 


We also provide a sparse reward of _i ×_ 100 for arriving at the _i_<sup>_th_</sup> checkpoint. 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 2. 

_13) push:_ 


**_Objective._** Move a box to a randomly initialized 3D point on a table. 

**_Observation._** Joint positions and velocities of the robot, left hand position of the robot, box destination, box position, and box velocity. 

**_Initialization._** The robot is initialized to a standing position. The box and its destination are initialized at a random location on the table. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** Let: 

- _d_ goal = _d_ ( _box, destination_ ) 

- _success_ = 1 _d_ goal _<_ 0 _._ 05 

**_Observation._** Positions and velocities of the robot’s joints, the cabinets’ joints, and the objects situated inside the cabinets. 

**_Initialization._** The robot is initialized to a standing position, with random noise added to all joint positions during each episode reset. 

**_Reward Implementation._** The reward of this task changes based on the occurring subtask. 

Subtask 1 is to open the sliding door (second highest one), with reward 


where the cabinet joint position _l_ cabinet is a value in [0 _,_ 0 _._ 4]. Subtask 2 is to open the drawer (the lowest one), with reward 


where the drawer joint position _l_ drawer is a value in [0 _,_ 0 _._ 45]. Subtask 3 is to put the cube from the drawer into the hingebased cabinet (the third highest one). Both the left and right hinge-based cabinet doors’ joint positions _α_ door,left _, α_ door,right are values in [0 _,_ 1 _._ 57]. Let 

- _open_ door,left = min(1 _, |α_ door,left _|_ ) 

- _open_ door,right = min(1 _, |α_ door,right _|_ ) 

- _d_ destination,x = _tol_ ( _xcube −_ 0 _._ 9 _,_ ( _−_ 0 _._ 3 _,_ 0 _._ 3) _,_ 0 _._ 3) 

- _d_ destination,y = _tol_ ( _ycube,_ ( _−_ 0 _._ 6 _,_ 0 _._ 6) _,_ 0 _._ 3) 

- _d_ destination,z = _tol_ ( _zcube −_ 0 _._ 94 _,_ ( _−_ 0 _._ 15 _,_ 0 _._ 15) _,_ 0 _._ 3) 

- _r_ destination = 0 _._ 3 _· mean_ ( _d_ destination,x _, d_ destination,y) + 0 _._ 7 _· d_ destination,z 

Then the reward of this subtask, _R_ 3, is formulated as follows 

_r_ 3 = 0 _._ 5 _·_ max( _open_ door,left _, open_ door,right) + 0 _._ 5 _· r_ destination _R_ 3 = 0 _._ 2 _· stable_ + 0 _._ 8 _· r_ 3 

- _d_ hand = _d_ ( _box, hand_ left) 

Then the reward is 


where by default _αs_ = 1000 _, αt_ = 1 _, αh_ = 0 _._ 1. 

**_Termination._** The episode terminates after 500 steps, or when _d_ goal _<_ 0 _._ 05. 

_14) cabinets:_ 


**_Objective._** Open four different types of cabinet doors (e.g., hinge door, sliding door, drawer) and perform different manipulations (see subtasks below) for objects inside the cabinet. 

Subtask 4 is to put the original cube from the hinge-based leftright cabinet (third highest) into the pull-up cabinet (highest). The pull-up door has a joint position _α_ pull in [0 _,_ 1 _._ 57]. Let 

- _open_ pull = min(1 _, |α_ pull _|_ ) 

- _d_ destination,x = _tol_ ( _xcube −_ 0 _._ 9 _,_ ( _−_ 0 _._ 3 _,_ 0 _._ 3) _,_ 0 _._ 3) 

- _d_ destination,y = _tol_ ( _ycube,_ ( _−_ 0 _._ 6 _,_ 0 _._ 6) _,_ 0 _._ 3) 

- _d_ destination,z = _tol_ ( _zcube −_ 1 _._ 54 _,_ ( _−_ 0 _._ 15 _,_ 0 _._ 15) _,_ 0 _._ 3) 

- _r_ destination = 0 _._ 3 _· mean_ ( _d_ destination,x _, d_ destination,y) + 0 _._ 7 _· d_ destination,z 

Then the reward of this subtask, _R_ 4, is formulated as follows 


The reward during the occurrence of subtask _i_ is _Ri_ . Upon the completion of subtask _i_ , a sparse reward of _i ∗_ 100 is offered. At the timestep where all subtasks are completed, a sparse reward of 1000 is added to the total reward. 

**_Termination._** The episode terminates after 1000 steps or whenever all subtasks are complete. 

_15) highbar:_ 


**_Objective._** Athletically swing while staying attached to a horizontal high bar until reaching a vertical upside-down position. 

**_Observation._** Joint positions and velocities of the robot. 

**_Initialization._** The robot is initialized such that its hand is gripping the high bar, and its body is hanging from it. 

**_Reward Implementation._** Let 

- _uprighthighbar_ = _upright_ (( _−∞, −_ 0 _._ 9) _,_ 1 _._ 9) 

- _feet_ = _tol_ (( _z_ foot,left + _z_ foot,right) _/_ 2 _,_ (4 _._ 8 _,_ + _∞_ ) _,_ 2) 

Then, 

_R_ ( _s, a_ ) = _uprighthighbar × feet × e_ 

**_Termination._** The episode terminates after 1000 steps, or when _z_ head _<_ 2. 

_16) door:_ 


**_Objective._** Pull a door open using its doorknob, and traverse through the doorpath while keeping the door open. 

**_Observation._** Joint positions and velocities of the robot, door hinge, and door hatch. 

**_Initialization._** The robot is initialized to a standing position. The door hinge joint and door latch are initialized such that the door is completely closed. For the current implementation, the door can only be pulled towards the robot, limiting its hinge joint position to be within [0 _,_ 1 _._ 4]. The door latch has a joint range of [0 _,_ 2] (being pulled downwards until 2 radians from positive x-axis, clockwise). Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

- _open_ door = min(1 _, q_ door<sup>2)</sup> 

- _open_ hatch = _tol_ ( _q_ hatch _,_ (0 _._ 75 _,_ 2) _,_ 0 _._ 75) 

- _proximity_ door = 

   - _tol_ ( min( _d_ ( _hand_ left _, door_ ) _, d_ ( _hand_ right _, door_ )) _,_ (0 _,_ 0 _._ 25) _,_ 1) 

- _passage_ = _tol_ ( _x_ IMU _,_ (1 _._ 2 _,_ + _∞_ ) _,_ 1) 

Then, the reward of this task is: 

_R_ = 0 _._ 1 _· stable_ + 0 _._ 45 _· open_ door + 0 _._ 05 _· open_ hatch 

- + 0 _._ 05 _· proximity_ door + 0 _._ 35 _· passage_ 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 58. 

_17) truck:_ 


**_Objective._** Unload packages from a truck by moving them onto a platform. 

**_Observation._** Joint positions and velocities of the robot, and positions and velocities of packages. 

**_Initialization._** The robot is initialized to a standing position. Packages are initialized to be on the truck. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** The reward of this task relies on the subsets of packages based on three categories: (1) being on truck ( _p_ truck), (2) being picked up ( _p_ picked), and (3) being on table ( _p_ table). Let 

   - _truck_ = _tol_ (min _p∈p_ truck _∥posp − pos_ pelvis _∥,_ (0 _,_ 0 _._ 2) _,_ 4) 

   - _picked_ = _tol_ (min _p∈p_ picked _∥posp − pos_ pelvis _∥,_ (0 _,_ 0 _._ 2) _,_ 4) 

   - _table_ = _tol_ (min _p∈p_ table _∥posp − pos_ table _∥,_ (0 _,_ 0 _._ 2) _,_ 4) 

- _rlocation_ = 100 _·_ ( _ptable_ + _ppicked − ptruck_ ) 

- Then, the reward is: 

_R_ ( _s, a_ ) = _rlocation_ + _upright ×_ (1 + _truck_ + _picked_ + _table_ ) 

If all packages are picked up, an additional sparse reward of 1000 is provided, and the episode terminates thereafter. 

**_Termination._** The episode terminates after 1000 steps, or when all packages are delivered onto the table. _18) cube:_ 


**_Objective._** Manipulate two cubes, each cube in one hand, until they both correspond with a specific, randomly initialized target orientation. 

**_Observation._** Joint positions and velocities of the robot and the two cubes to be manipulated on hand. The transparent cube 

in front of the robot is an indication of the target orientation for in-hand cubes, and its orientation is also in the state. 

**_Initialization._** The robot is initialized to a standing position. The cubes are initialized at a random orientation right above the robot hands. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

- _stillx_ = _tol_ ( _vx,_ (0 _,_ 0) _,_ 2) 

- _stilly_ = _tol_ ( _vy,_ (0 _,_ 0) _,_ 2) 

- _still_ = _mean_ ( _stillx, stilly_ ) 

- _quat_ target denotes the target orientation for both in-hand cubes. 

- _orientation_ = 


- _proximity_ cube = 


Then the reward of this task is: 


**_Termination._** The episode terminates after 500 steps, or when _z_ pelvis _<_ 0 _._ 5, _z_ cube,left _<_ 0 _._ 5, or _z_ cube,right _<_ 0 _._ 5. 

_19) bookshelf:_ 


**_Objective._** The bookshelf environment mainly concerns relocating five objects across the various shelves. There are five designated subtasks, resembling five different relocations (each for a different item and destination location). The items involved in the subtasks are colored from brightest to darkest in a red shade, where the brighter shade of red shows that the object’s relocation is an earlier subtask to complete. The subtasks must be completed in order. The order is always the same in bookshelf_simple, while it is randomized at every episode in bookshelf_hard. 

**_Observation._** Positions and velocities of the robot’s joints and all objects on the bookshelf, including those that are not associated with any subtasks, as well as an index representing the next object to be relocated. 

**_Initialization._** The robot is initialized to a standing position. All objects on the bookshelf are currently initialized at a default position. Random noise is added to all joint positions during each episode reset. In the simple version of this environment, the objects to move on the bookshelf and their destinations are 

fixed; in the hard version, both of them are randomized at the beginning of every episode instead. 

**_Reward Implementation._** For each subtask _ti_ where _i ∈ {_ 1 _,_ 2 _, . . . ,_ 5 _}_ , its reward _ri_ is formulated as follows. First, let 

_• proximity_ destination = 


Then, the subtask reward is 


and the reward for that step is the subtask reward per se. The current subtask is considered complete when the distance between the destination and object of current subtask is less than 0 _._ 15. 

An additional sparse reward of 100 _∗i_ is added to the timestep of subtask _i_ ’s completion. 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 58, _z_ object _<_ 0 _._ 5, or all subtasks succceeded. 

_20) basketball:_ 


**_Objective._** Catch a ball coming from random direction and throw it into the basket. 

**_Observation._** Positions and velocities of the robot’s joints and the basketball. 

**_Initialization._** The robot is initialized to a standing position. The basketball is initialized such that it will be randomly spawned at a radius of 1 _._ 5 m from the robot, at a random angle _ω ∈_ [ _−_ 1 _._ 45 rad _,_ 1 _._ 45 rad] from positive x-axis, and arrive right in front of the robot after 0 _._ 2 s. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** The task is divided into two stages: 

- catch : before the basketball collides with anything 

- �throw : after the basketball experiences one collision 

The rewards at different stages are formulated differently. Let 

- _proximity_ hand = 


_• aim_ = _tol_ ( _d_ ( _ball, basket_ ) _,_ (0 _,_ 0) _,_ 7). 

Then, the reward at each stage of the task is formulated as follows: 

_R_ catch( _x, u_ ) = 0 _._ 5 _· proximity_ hand + 0 _._ 5 _· stable_ 


At the earliest timestep where _d_ ( _ball, basket_ ) _≤_ 0 _._ 05, the episode terminates, and a large sparse reward of 1000 is given. **_Termination._** The episode terminates after 500 steps, or when _z_ pelvis _<_ 0 _._ 5, _z_ ball _<_ 0 _._ 5, or when success has been achieved. 

_21) window:_ 


**_Objective._** Grab a window wiping tool and keep its tip parallel to a window by following a prescribed vertical speed (in absolute value). 

**_Observation._** Joint positions and velocities of the robot and the window wiping tool (position and velocities of the entire tool, in addition to those of the rotational joint attached between the wipe and the rod of the tool). 

**_Initialization._** The robot is initialized to a standing position. The window wiping tool is initialized above the robot unit’s hand in a parallel direction to the window frames. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

- _proximity_ tool = 


_• move_ wipe = _tol_ ( _|v_ wipe,z _|,_ (0 _._ 5 _,_ 0 _._ 5) _,_ 0 _._ 5) 

The manipulation reward is defined as: 


Meanwhile, five sites are put on the four corners and center of the wipe to detect coverage of contact. Let these sites be _s_ 1 _, s_ 2 _, . . . , s_ 5, then the reward for contact between the tool and window is defined as: 


Then, the reward of this task is: 


**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 58 or _z_ tool _<_ 0 _._ 58. 

_22) spoon:_ 


**_Objective._** Grab a spoon and use it to follow a circular pattern inside a pot. 

**_Observation._** Joint positions and velocities of the robot and the position and velocity of the spoon, as well as the target position that the spoon should be at the current timestep. 

**_Initialization._** The robot is initialized to a standing position. The spoon is initialized at a specified position on the table, leftwards of the pot. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

- _t_ := current timestep 

- _proximity_ tool = 


Then: 


**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 58. 

_23) kitchen:_ 


**_Objective._** Execute a sequence of actions in a kitchen environment, namely, open a microwave door, move a kettle, and turn burner and light switches. 

**_Observation._** Joint positions and velocities of the robot, and positions and velocities of kitchenware. 

**_Initialization._** The robot is initialized to a standing position. Kitchenware is initialized at specified positions. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** A subtask in kitchen is considered complete if the distance between an object and its goal position is lower than a specified threshold. The sparse reward is the number of subtasks completed. 

**_Termination._** The episode terminates after 500 steps. 

_24) package:_ 


**_Objective._** Move a box to a randomly initialized target position, also tested in the ablation in Figure 9. 

**_Observation._** Joint positions and velocities of the robot, both hand positions of the robot, package destination, package position, and package velocity. 

**_Initialization._** The robot is initialized to a standing position. The package position and its destination are randomly initialized within a specific area. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

   - _height_ package = min(1 _, z_ package) 

   - _success_ = 1 _d_ ( _package,destination_ ) _<_ 0 _._ 1 

- _d_ hand = _d_ ( _package, hand_ left) + _d_ ( _package, hand_ right). 

- Then, the reward is: 


+ _stable_ + _height_ package + 1000 _· success_ 

**_Termination._** The episode terminates after 1000 steps, or when _d_ ( _package, destination_ ) _<_ 0 _._ 1. 

_25) powerlift:_ 


**_Objective._** Lift a barbell of a designated mass. **_Observation._** Joint positions and velocities of the robot and barbell. 

**_Initialization._** The robot is initialized to a standing position. The barbell is initialized on the ground. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

_• heightbarbell_ = _tol_ ( _zbarbell,_ (1 _._ 9 _,_ 2 _._ 1) _,_ 2). 

Then, 

_R_ ( _s, a_ ) = 0 _._ 2 _· stable_ + 0 _._ 8 _· heightbarbell._ 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 2. 

_26) room:_ 


**_Objective._** Organize a 5 m by 5 m space populated with randomly scattered object to minimize the variance of scattered objects’ locations in _x_ , _y_ -axis directions. 

**_Observation._** Joint positions and velocities of the robot and scattered objects. 

**_Initialization._** The robot is initialized to a standing position. The scattered objects’ positions are randomly initialized within a specific area. Random noise is added to all joint positions during each episode reset. 

**_Reward Implementation._** Let 

- _X_ be a matrix containing the location of all scattered objects in 3D coordinates. 

- _cleanness_ = _tol_ (max( _V ar_ ( _X_ : _,_ 0) _, V ar_ ( _X_ : _,_ 1)) _,_ (0 _,_ 0) _,_ 3), where _V ar_ ( _X_ : _,_ 0) is the variance of x-coordinates of all objects’ locations, and _V ar_ ( _X_ : _,_ 1) is such variance for y-coordinates. 

Then, 

_R_ ( _s, a_ ) = 0 _._ 2 _· stable_ + 0 _._ 8 _· cleanness_ 

**_Termination._** The episode terminates after 1000 steps, or when _z_ pelvis _<_ 0 _._ 3. 

_27) insert:_ 


**_Objective._** Insert the ends of a rectangular block into two small pegs. Two versions, insert_small and insert_normal present different object sizes. 

**_Observation._** Joint positions and velocities of the robot, rectangular block to insert, and two provided small pegs. 

**_Initialization._** The robot is initialized to a standing position. The rectangular block and two pegs are initialized on the table at specific orientation and position. 

**_Reward Implementation._** Let the rectangular blocks be formualted to have two ends _enda_ , _endb_ , which must be respectively inserted to the pegs _pega_ , _pegb_ . 

- _proximitypeg,site_ = _tol_ ( _d_ ( _peg, site_ ) _,_ (0 _,_ 0) _,_ 0 _._ 5) 

- _proximityblock_ = 

_mean_ ( _proximity_ ( _pega, enda_ ) _, proximity_ ( _pegb, endb_ )) 

- _height_ ( _peg_ ) = _tol_ ( _zpeg −_ 1 _._ 1 _,_ (0 _,_ 0) _,_ 0 _._ 15) 

- _heightpegs_ = _mean_ ( _height_ ( _pega_ ) _, height_ ( _pegb_ )) 

- _proximityhands_ = 


The reward of this task is phrased as: 


**_Termination._** The episode terminates after 1000 steps, or when any of the blocks or pegs are at a height lower than 0 _._ 5 from floor. 

### APPENDIX C TRAINING DETAILS 

||DreamerV3|TD-MPC2|SAC|Target|
|---|---|---|---|---|
|walk|800_._2_±_158_._7|782_._0_±_109_._2|31_._7_±_24_._0|700_._0|
|stand|622_._7_±_404_._8|809_._0_±_137_._1|208_._3_±_105_._6|800_._0|
|run|633_._8_±_222_._4|93_._3_±_14_._3|5_._0_±_2_._1|700_._0|
|reach|7580_._9_±_1951_._0|7316_._1_±_2112_._1|4565_._1_±_212_._8|12000_._0|
|hurdle|126_._2_±_59_._4|46_._4_±_10_._8|13_._2_±_8_._8|700_._0|
|crawl|878_._8_±_122_._7|957_._4_±_17_._5|330_._0_±_111_._9|700_._0|
|maze|272_._3_±_116_._6|244_._3_±_97_._7|144_._8_±_17_._8|1200_._0|
|sit_simple|891_._4_±_38_._4|411_._1_±_368_._0|148_._3_±_103_._8|750_._0|
|sit_hard|433_._4_±_355_._9|343_._0_±_381_._7|55_._0_±_18_._2|750_._0|
|balance_simple|19_._8_±_7_._0|40_._5_±_23_._9|61_._5_±_1_._1|800_._0|
|balance_hard|45_._9_±_27_._4|48_._2_±_28_._5|42_._5_±_22_._6|800_._0|
|stair|131_._1_±_43_._6|70_._4_±_7_._1|14_._1_±_6_._8|700_._0|
|slide|436_._5_±_200_._1|119_._0_±_35_._9|6_._3_±_2_._8|700_._0|
|pole|658_._3_±_343_._3|226_._3_±_116_._1|46_._3_±_26_._4|700_._0|
|push|_−_1251_._9_±_659_._8|_−_258_._7_±_66_._5|_−_97_._9_±_147_._0|700_._0|
|cabinet|57_._3_±_66_._3|112_._8_±_142_._9|211_._8_±_33_._8|2500_._0|
|highbar|8_._9_±_5_._8|0_._3_±_0_._0|9_._4_±_3_._7|750_._0|
|door|213_._0_±_149_._3|274_._7_±_12_._5|39_._4_±_25_._2|600_._0|
|truck|1103_._8_±_232_._9|1132_._6_±_72_._1|1077_._5_±_95_._0|3000_._0|
|cube|111_._2_±_59_._9|54_._7_±_33_._1|130_._7_±_30_._5|370_._0|
|bookshelf_simple|840_._4_±_5_._6|136_._2_±_71_._6|346_._9_±_231_._5|2000_._0|
|bookshelf_hard|530_._2_±_302_._5|37_._0_±_1_._3|293_._9_±_121_._6|2000_._0|
|basketball|19_._3_±_2_._5|42_._0_±_14_._8|22_._1_±_3_._2|1200_._0|
|window|461_._0_±_252_._8|87_._1_±_37_._5|62_._9_±_83_._8|650_._0|
|spoon|349_._7_±_46_._2|77_._9_±_80_._6|87_._7_±_80_._5|650_._0|
|kitchen|0_._0_±_0_._0|0_._0_±_0_._0|0_._0_±_0_._0|4_._0|
|package|_−_18015_._2_±_9477_._7|_−_3655_._6_±_1055_._0|_−_6718_._3_±_607_._0|1500_._0|
|powerlift|315_._9_±_16_._9|99_._1_±_47_._3|81_._8_±_46_._7|800_._0|
|room|120_._5_±_71_._4|131_._4_±_56_._7|12_._0_±_4_._9|400_._0|
|insert_small|184_._8_±_26_._3|129_._8_±_51_._9|10_._8_±_13_._4|350_._0|
|insert_normal|171_._5_±_33_._2|237_._6_±_9_._1|46_._3_±_63_._1|350_._0|


TABLE V: **Average returns for HumanoidBench.** Each number represents average return@10M (return@2M) with the standard deviation for DreamerV3 and SAC (TD-MPC2). 

### _A. Baseline Implementation Details_ 

For SAC, we use the implementation from JaxRL Minimal [16]. For PPO, we use the Stable-Baselines3 [51] implementation with 4 parallel environments. For DreamerV3 and TD-MPC2, we use their official code. For DreamerV3, we use the ‘medium’ configuration, with an update-to-data ratio of 64. For TD-MPC2, we use the 5M configuration. Unless specified, we use their default hyperparameters. 

### _B. Reaching Policy Implementation Details_ 

We train the low-level reaching policies described in Section V-D using PPO, largely parallelized on GPU using MuJoCo MJX. We employ the PureJaxRL [35] implementation, using their default parameters, except a higher number of environments as detailed in Section V-D, 16 steps per environment, and an entropy coefficient of 0.001. 

### _C. Benchmarking Results_ 

We summarize our benchmarking results in Table V and Table VI. We report the mean and standard deviation of maximum episode returns over three seeds. DreamerV3 and SAC are trained for 10M, while TD-MPC2 is trained for 2M environment steps, which roughly corresponds to 48 h. 

||DreamerV3|TD-MPC2|SAC|Target|
|---|---|---|---|---|
|walk|932_._4_±_0_._3|900_._3_±_47_._6|68_._7_±_27_._0|700_._0|
|stand|932_._9_±_1_._1|925_._7_±_2_._5|809_._9_±_194_._5|800_._0|
|run|895_._9_±_6_._0|226_._7_±_23_._3|104_._8_±_7_._4|700_._0|
|reach|9831_._6_±_115_._9|9727_._6_±_48_._9|7169_._9_±_874_._1|12000_._0|
|hurdle|396_._8_±_39_._7|196_._7_±_30_._5|78_._6_±_32_._8|700_._0|
|crawl|985_._3_±_0_._6|985_._2_±_0_._4|626_._5_±_29_._1|700_._0|
|maze|592_._5_±_49_._0|444_._9_±_22_._1|269_._9_±_37_._8|1200_._0|
|sit_simple|935_._7_±_5_._5|928_._4_±_1_._5|842_._7_±_50_._8|750_._0|
|sit_hard|914_._6_±_1_._5|906_._3_±_6_._0|214_._0_±_47_._9|750_._0|
|balance_simple|95_._4_±_8_._3|95_._3_±_3_._1|80_._7_±_3_._7|800_._0|
|balance_hard|114_._0_±_12_._3|122_._2_±_13_._1|71_._0_±_7_._9|800_._0|
|stair|411_._4_±_9_._7|251_._9_±_9_._1|42_._8_±_0_._7|700_._0|
|slide|928_._4_±_2_._0|311_._9_±_15_._1|41_._4_±_2_._4|700_._0|
|pole|952_._2_±_10_._3|644_._9_±_21_._2|440_._0_±_88_._4|700_._0|
|push|1000_._0_±_0_._0|1000_._0_±_0_._0|352_._8_±_31_._5|700_._0|
|cabinet|722_._6_±_7_._3|721_._6_±_25_._9|485_._9_±_137_._2|2500_._0|
|highbar|83_._1_±_4_._6|0_._9_±_0_._4|40_._8_±_41_._7|750_._0|
|door|335_._7_±_14_._8|310_._6_±_10_._6|251_._2_±_9_._0|600_._0|
|truck|1674_._3_±_52_._6|1457_._2_±_24_._3|1387_._5_±_10_._0|3000_._0|
|cube|237_._9_±_3_._4|241_._1_±_1_._2|203_._5_±_27_._2|370_._0|
|bookshelf_simple|849_._6_±_0_._3|825_._0_±_9_._6|766_._5_±_10_._3|2000_._0|
|bookshelf_hard|867_._8_±_8_._4|320_._4_±_58_._9|681_._5_±_10_._3|2000_._0|
|basketball|808_._8_±_340_._5|1055_._3_±_4_._1|192_._3_±_45_._6|1200_._0|
|window|765_._6_±_38_._4|201_._1_±_91_._5|128_._6_±_170_._8|650_._0|
|spoon|421_._5_±_2_._5|403_._5_±_3_._2|297_._5_±_26_._5|650_._0|
|kitchen|0_._0_±_0_._0|0_._0_±_0_._0|0_._0_±_0_._0|4_._0|
|package|1009_._2_±_4_._1|1003_._3_±_3_._4|_−_3552_._8_±_361_._3|1500_._0|
|powerlift|338_._6_±_0_._1|264_._7_±_23_._9|171_._2_±_3_._6|800_._0|
|room|420_._8_±_51_._1|353_._3_±_41_._5|52_._2_±_3_._9|400_._0|
|insert_small|239_._8_±_4_._6|226_._4_±_10_._8|72_._7_±_21_._9|350_._0|
|insert_normal|279_._9_±_9_._9|273_._0_±_5_._7|135_._3_±_51_._5|350_._0|


TABLE VI: **Maximum returns for HumanoidBench.** Each number represents maximum return@10M (return@2M) with the standard deviation for DreamerV3 and SAC (TD-MPC2). 

