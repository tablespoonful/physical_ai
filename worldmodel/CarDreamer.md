---
title: "CarDreamer: Open-Source Learning Platform for World Model based Autonomous Driving"
date: "2024-05-15"
authors: "Dechen Gao; Shuangyu Cai; Hanchu Zhou; Hang Wang; Iman Soltani; Junshan Zhang"
url: https://arxiv.org/abs/2405.09111
pdf: https://arxiv.org/pdf/2405.09111
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2405.09111)** / [論文ページ](https://arxiv.org/abs/2405.09111)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# CARDREAMER: OPEN-SOURCE LEARNING PLATFORM FOR WORLD MODEL BASED AUTONOMOUS DRIVING 

**Dechen Gao**<sup>_∗_1</sup> **, Shuangyu Cai**<sup>_∗_2,4</sup> **, Hanchu Zhou**<sup>_∗_2</sup> **, Hang Wang**<sup>_∗_2</sup> **, Iman Soltani**<sup>3</sup> **, and Junshan Zhang**<sup>2</sup> 

1Department of Computer Science, University of California, Davis 

2Department of Electrical and Computer Engineering, University of California, Davis 

3Department of Mechanical and Aerospace Engineering, University of California, Davis 

4Institute for Interdisciplinary Information Sciences, Tsinghua University, China 

```
{dcgao,hczhou,whang,isoltani,jazh}@ucdavis.edu
```

> 4 `caisy21@mails.tsinghua.edu.cn` 

> _∗_ Equal contribution. 

July 29, 2024 

## **ABSTRACT** 

To safely navigate intricate real-world scenarios, autonomous vehicles (AVs) must be able to adapt to diverse road conditions and anticipate future events. World model based reinforcement learning (RL) has emerged as a promising approach by learning and predicting the complex dynamics of various environments. Nevertheless, to the best of our knowledge, there does not exist an open-source platform for training and testing such algorithms in complicated driving environments. To fill this void, we introduce CarDreamer, the first open-source learning platform designed specifically for developing and evaluating world model based autonomous driving algorithms. It comprises a few key components, including 1) World model (WM) backbone: CarDreamer has integrated some state-of-the-art world models, which simplifies the reproduction of RL algorithms. The backbone is decoupled from the rest and communicates using the standard Gym interface, so that users can easily integrate and test their own algorithms. 2) Built-in tasks: CarDreamer offers a comprehensive set of highly configurable driving tasks which are compatible with Gym interfaces and are equipped with empirically optimized reward functions. 3) Task development suite: CarDreamer integrates a flexible task development suite to streamline the creation of driving tasks. This suite enables easy definition of traffic flows and vehicle routes, along with automatic collection of multi-modal observation data. A visualization server allows users to trace real-time agent driving videos and performance metrics through a browser. Furthermore, we conduct extensive experiments using built-in tasks to evaluate the performance and potential of WMs in autonomous driving. Thanks to the richness and flexibility of CarDreamer, we also systematically study the impact of observation modality, observability, and sharing of vehicle intentions on AV safety and efficiency. All code and documents are accessible on our GitHub page `https://github.com/ucd-dare/CarDreamer` . 

**_K_ eywords** Autonomous Driving _·_ Reinforcement Learning _·_ World Model 

## **1 Introduction** 

Autonomous vehicles (AVs) are expected to play a central role in future mobility system with many promising benefits like safety and efficiency [1]. Recent years have witnessed great achievement on the development of AVs. In the U.S. alone, millions of miles have been driven by AVs [2] on public roads. However, achieving robust AVs that are capable of navigating complex and diverse real-world scenarios remains a challenging frontier [3, 4, 5]. For instance, as calculated by the US Department of Transportation’s Federal Highway Administration, AVs experience a crash rate about two times more than the conventional vehicles per million miles traveled [6]. 

A TECHNICAL REPORT - JULY 29, 2024 

The reliability of AVs directly hinges upon the generalization capability of autonomous systems in unforeseen scenarios. World model (WM), which excels in generalization, offers a promising solution with its ability to learn the complex dynamics of environments and anticipate future scenarios. In particular, WMs learn a compact latent representation that encodes the key elements and dynamics of the environment. This learned representation facilitates strong generalization, enabling the WM to make predictions in scenarios beyond its training samples. In particular, our WM-based learning platform incorporates building blocks that mimic human-like perception and decision-making, such as vision model and memory model [7, 8]. Indeed, humans excel at handling rare or unseen events with proper actions thanks to human’s “internal world model” [9]. By emulating cognitive processes akin to human intelligence, WM based reinforcement learning (RL) has demonstrated state-of-the-art performance in domains such as Atari games and Minecraft [10]. However, WMs’ application on autonomous driving remains an exciting open field [5], partially due to the lack of easy-to-use platforms to train and test such RL algorithms. The endeavor on developing a learning platform for WM-based autonomous driving can be extremely beneficial for the research in this domain. 

Thus motivated, we introduce CarDreamer, the first open-source learning platform designed specifically for WM based autonomous driving. CarDreamer aims to facilitate the rapid development and evaluation of algorithms, enabling users to test their algorithms on provided tasks or quickly implement customized tasks through a comprehensive development suite. CarDreamer’s key contributions include: 

1. _Integrated WM algorithms for reproduction._ CarDreamer has integrated state-of-the-art WMs, including DreamerV2, DreamerV3, and Planning2Explore, significantly reducing the time required to reproduce the performance of existing algorithms. These algorithms are decoupled from the rest of CarDreamer and communicates through the unified Gym interface. This enables streamlined integration and testing of new algorithms without additional adaptation efforts as long as they support Gym interface. 

2. _Highly configurable built-in tasks with optimized rewards._ CarDreamer provides a comprehensive set of driving tasks, such as lane changing and overtaking. These tasks allow extensive customization in terms of difficulty, observability, observation modalities, and communication of vehicle intentions. They expose the same Gym interface for convenient use and the reward functions are meticulously designed to optimize training efficiency. 

3. _Task Development Suite and Visualization Server._ This suite not only simplifies the creation of customized driving tasks via API-driven traffic spawning and control, but also includes a modular observer for easy multimodal data collection and configuration. A visualization server enables the real-time display of agent driving videos and statistics on a web browser, which accelerates reward engineering and algorithm development by providing immediate performance insights. 

In addition to developing the CarDreamer platform, we present comprehensive experiments that evaluate the overall performance and potential of WMs in autonomous driving. We highlight its predictive accuracy on multi-modal observation inputs. Furthermore, the comparison of different levels of observability and intention sharing demonstrates that communication can clearly enhance both traffic safety and efficiency. To the best of our knowledge, these results represent the first experimental manifestation of WMs’ efficacy in autonomous driving tasks with communication of vehicle intentions. 

## **2 Related Work** 

**World Models in Reinforcement Learning.** RL usually suffers from high sample complexity [11], which significantly hinders it from being practical especially for tasks where interacting with environment can be costly and time-consuming. To remedy for the issue, model-based RL has been studied to leverage a world model that explicitly learns environment dynamics to “imagine” future trajectories, allowing agents to interact with the world model instead of the actual environment [7]. As the high-dimensional observations that evolve on intricate dynamics can be intractable, prior works typically learn dynamics on a latent space. Typical designs involve modeling dynamics with a Recurrent State-Space Model (RSSM) [12]. Dreamer provides a series of works that leverage RSSM [12, 13, 10] and train agents in world model’s imagination, and has demonstrated promising sample efficiency and generalization ability on conventional RL benchmarks. ISO-Dream [14] isolates controllable and non-controllable sources to the changes of dynamics such that agents can differentiate changes that are independent and dependent to their actions. Planning2Explore [15] promotes exploration by directing it towards states of higher uncertainty, facilitating the learning of more robust dynamics and enabling quick adaptation to new tasks in a zero or few-shot manner. LEXA [16] utilizes a learned world model to train separate explorer and achiever policies for forward-looking exploration and goal achievement. 

**World Models for Autonomous Driving.** In the field of autonomous driving, there has been mainly two approaches for studying world models [17, 18], 1) leveraging world models as neural driving simulators to synthesize realistic 

2 

A TECHNICAL REPORT - JULY 29, 2024 

driving videos, and 2) utilize world models in simulation to train and evaluate agent policies. In the first approach, GAIA-1 [19] utilizes a world model to generate realistic driving scenarios given videos, texts, and actions as inputs. DriveDreamer [20] generates driving scenarios along with the actions given prior information such as high-definition maps and 3D bounding boxes. ADriver-1 [21] eliminates the need of extensive prior information and is able to achieve “infinite driving” inside its world model by providing both scenario generation and action predictions. DriveDreamer2 [22] is built-upon large language models to make prompting more user-friendly to generate diverse traffic conditions for driving video generation. In contrast, in the second approach, MILE [9] conducts imitation learning based on a Dreamerstyle world model. It learns from offline expert data using road map and camera inputs, and predicts the transition of future Bird-Eye Views (BEVs) as an auxiliary task. SEM2 [23] conducts reinforcement learning with a Dreamer-style world model, and decodes camera and LiDAR representations into semantic BEV masks. Think2Drive [24] trains DreameV3 with BEV inputs and tests it on 39 CARLA benchmarks. Our platform aims at facilitating this line of research, providing tailored benchmarks and tools for WM based RL algorithms in autonomous driving. 

**Simulators.** Collecting data for autonomous driving in the real world is costly and time-consuming. To this end, various simulators, such as CARLA [25], SUMO [26], and Flow [27], have been developed. CARLA is distinguished by its realistic environmental modeling and image rendering capabilities. These simulators are generally designed for general traffic simulation rather than for RL applications. Our platform is specifically tailored for WM-based RL, offering meticulously crafted RL rewards, interfaces, and automating training data requirements. 

## **3 Background** 

We give a brief introduction in this section to the two cornerstones that CarDreamer involves: CARLA, [25] a high-fidelity and flexible simulator, and Gym [28], a standard interface for RL training and evaluation. 

**CARLA.** CARLA is an open-source simulator that aims at simulating real-world traffic scenarios. CARLA is based on Unreal Engine which provides realistic physics and high-quality rendering. It provides digital assets including maps, buildings, vehicles, and various landmarks. It supports various sensors such as RGB camera, LiDAR, RADAR. Users can create vehicles or pedestrians and take full control of these actors. It is a general tool, and one main challenge of its application in RL algorithms also originates from its generality: As stated in Section 2, obtaining the BEV in CARLA involves a cumbersome process, thus impeding its fast deployment in training RL algorithms. 

**Gym.** Gym is a standard interface defined by OpenAI to formalize the interplays between agents and environments. Two functions `reset()` and `step(action)` constitute the core part of this interface. The former initializes the environment to its start state. The latter takes an action input from the agents, simulates the evolution of the environment, and returns observation data, reward signals, a terminal indicator, and some extra information. In this way, an RL algorithm can be easily tested on various environments with minor adaptation as long as they both support the Gym interface. There have been extensive efforts in developing diverse Gym benchmarks, such as Atari games and DMC suites. To the best of our knowledge, in the field of WM based RL algorithms for autonomous driving in CARLA, CarDreamer is the first platform that provides diverse urban driving tasks through the Gym interface to facilitate training and evaluation. 

## **4 CarDreamer Architecture and Implementation** 

### **4.1 Overview of CarDreamer** 

As depicted in Figure 1, CarDreamer comprises three principal components: _world model backbone_ , _built-in tasks_ , and _task development suite_ . In particular, the task development suite facilitates a variety of API functionalities, including vehicle spawning, traffic flow control, and route planning within CARLA. An observer module automates the collection of multi-modal observation data, such as sensor data and BEVs, managed by independent and customizable data handlers. This data serves dual purposes: it is utilized by the task and a training visualization server. The visualization server displays real-time driving videos and environment feedback via an HTTP server and integrates seamlessly with the world model algorithm through the gym interface. Upon receiving an action as the agent’s response, the observer collects data from data handlers at the subsequent frame, thus continuing this operational cycle. We will now explore each module in detail. 

### **4.2 World Model Backbone** 

The World Model Backbone in CarDreamer seamlessly integrates state-of-the-art approaches such as DreamerV2 [13], DreamerV3 [10], and Planning2Explore [15], facilitating rapid reproduction of these models. This backbone architecture is strategically designed to decouple the world model implementation from task-specific components, thereby enhancing 

3 

A TECHNICAL REPORT - JULY 29, 2024 


Figure 1: CarDreamer Architecture. Three key components are highlighted: Built-In Tasks, Task Development Suite, World Model Backbone. 

modularity and extensibility. Communication between these components is efficiently managed through the standard Gym interface, which allows for extensive customization. 

This decoupling enables users to easily adapt or replace the default world models with their own implementations, supporting rapid prototyping, benchmarking, and comparative analysis against established baselines. CarDreamer thus provides a comprehensive testbed for world model-based algorithms, fostering an ecosystem conducive to accelerated research and development within this field. The platform encourages users to explore innovative architectures, loss functions, and training strategies, all within a consistent and standardized evaluation framework characterized by diverse driving tasks and performance metrics. 

### **4.3 Built-In Tasks** 

We have meticulously crafted a wide array of realistic tasks, ranging from simple skills such as lane following and left turning to more complex challenges like random roaming across mixed road conditions that include crossroads, roundabouts, and varying traffic flows. These tasks are highly configurable, offering numerous options that present fundamental questions in autonomous driving. 

**Observability & Intention Sharing:** Partial observability presents a significant challenge in RL, where incomplete state information can exponentially increase the complexity of the input space for the sake of encompassing historical steps [29]. To address the lack of tools tailored to these challenges in autonomous driving, we initially offer three observability settings in CarDreamer: 1) Field-of-View (FOV) includes only the vehicles within the camera’s FOV; 2) Shared-FOV (SFOV) enables a vehicle to communicate with and collect FOV data from other vehicles within its own FOV; 3) Full Observability (FULL) assumes complete environment and background traffic information. Furthermore, users have control over whether the vehicles share their intention, and whom the vehicles share with. These configurations aligns with the fundamental questions of “what information to communicate” and “whom to communicate with” [30]. 

**Observation Modality:** Users can configure the observation space to include various modalities, from sensor data such as RGB cameras and LiDAR to synthetic data such as BEVs. This flexibility supports the development of end-to-end models that are capable of making decisions directly from multi-modal raw sensor data [5] or planning with BEV perception [31]. 

**Difficulty:** Difficulty settings primarily affect the density of traffic, posing significant collision avoidance challenges. As safety-critical events of AVs are rare [32], it is inherently nontrivial to validate the robustness of AVs due to the infrequent nature of such events [33]. CarDreamer is specifically designed to enable a comprehensive evaluation of safety and efficiency in scenarios that mimic these infrequent but critical events. 

4 

A TECHNICAL REPORT - JULY 29, 2024 

_Reward function._ Each task within CarDreamer is equipped with an ‘optimized’ reward function, which has been experimentally shown to enable DreamerV3 to successfully navigate through waypoints within just 10,000 training steps (see Section 5 for details). Notably, our empirical findings indicate that rewarding the agent based on its speed or incremental position changes leads to superior performance compared to rewarding absolute position. This is because when be rewarded solely for position, the agent can exploit the reward function by making a small initial movement and then remaining stationary, as any further movement risks incurring collision penalties. In practice, we do observe such sub-optimal behavior, where the learned policy converges to a local optimum to avoid collision by remaining stationary with a constant position reward. Conversely, rewarding speed encourages the agent to keep moving and accumulate rewards, mitigating the risk of premature convergence to sub-optimal policies. 

Our reward design carefully addresses crucial requirements for driving tasks, such as trajectory smoothness, which are often overlooked in conventional RL algorithms. Typically, these algorithms include an entropy term in their loss function or value estimation to encourage exploration and prevent premature convergence. However, in autonomous driving contexts, this entropy term can incentivize vehicles to follow a zigzag trajectory, as such erratic motion generates higher entropy rewards compared to smoother paths, even though both trajectories might achieve similar progress towards the goal. To counteract this effect, we introduce a penalty term specifically designed to discourage motion perpendicular to the goal direction. As a result, we have developed a reward function that effectively balances goal progression and trajectory smoothness, structured as follows 


Here, _v_ parallel and _v_ perp represent the speed parallel and perpendicular to the goal direction, respectively. Icollision is the indicator for collision. _α_ , _β_ , _γ_ are scaling factors. For tasks like waypoint following, additional reward terms are included for reaching each waypoint. 

_Interface and Usage._ All built-in tasks in CarDreamer utilize a unified Gym interface, allowing simple-to-use training and testing of RL algorithms without additional adaptations. Beyond direct usage, CarDreamer supports a variety of algorithms, including those for curriculum learning, which can leverage the progression from simpler to more complex tasks; or continual learning, which aims at addressing catastrophic forgetting when learning a new task. Additionally, for imitation learning, CarDreamer simplifies the collection of observational data in the simulator. Although initially designed for WM-based RL algorithms, the gym interface enables diverse applications across various algorithmic strategies. 

### **4.4 Task Development Suite** 

For users requiring customized tasks, CarDreamer offers a highly modular Task Development Suite. This suite is adaptable to various levels of customization to satisfy diverse user requirements. 

The initial module, _World Manager_ , caters to basic needs such as varying driving scenarios with different maps, routes, spawning locations, or background traffic flows. The World Manager is responsible for managing ‘actors,’ a term from CARLA [25], which encompasses all entities including vehicles, pedestrians, traffic lights, and sensors. It provides API calls to spawn various actors, particularly vehicles at different locations with either a default or a customized blueprint. These vehicles can be controlled by the user or by an Autopilot, a simple rule-based autonomous driving algorithm. Upon reset, it transparently destroys and releases resources. 

The second module, the _Observer_ , automates the collection of observation data across various modalities. While it allows users to easily access pre-defined observation modalities without manual interaction, it also supports extensive customization for data specifications. This is achieved through a series of data handlers, each delivering data for a particular modality, such as a RGB camera handler and a BEV handler. Each data handler is highly modular and independently manages the entire lifecycle of a specific type of data. Users can enhance the observer by registering a new data handler tailored to their own requirements. 

The third module comprises _Route Planners_ that accommodate diverse needs for task routes. CarDreamer includes several planners: a random planner for exploratory roaming across the entire map, a fixed path planner that creates waypoints connecting user-defined locations, and a fixed ending planner that generates routes using the classical A* algorithm from the current position to a designated endpoint. For additional customization, a base class is available for users to develop their own planners by overriding the `init_route()` and `extend_route()` methods, which define the initialization and extension of routes per time step, respectively. 

Additionally, the suite features a visualization server that seamlessly integrates the output from the Observer and other statistical data from environment feedback, displaying via an HTTP server. This automation facilitates rapid feedback, enhancing the process of reward engineering and algorithm development without extra coding efforts. 

5 

A TECHNICAL REPORT - JULY 29, 2024 


Figure 2: Reward curves of different tasks. 

## **5 CarDreamer Task Experiments** 

This section showcases the versatility and capabilities of CarDreamer through a comprehensive set of experiments across a wide range of settings. We use DreamerV3 [10] as the model backbone. Section 5.1 focuses on task training and evaluation, where we evaluate the performance of WMs in diverse driving tasks within CarDreamer. In Section 5.2, we assess the prediction accuracy of WMs to accurately imagine future states in different observation modality settings. Furthermore, Section 5.3 systematically evaluates the significant impact of observability and intention sharing on traffic safety and efficiency. 

### **5.1 World Model Training & Evaluation** 

We use a small DreamerV3 model with only 18M parameters as the model backbone. A small DreamerV3 has 32 CNN multipliers, 512 GRU and MLP units, and the MLP has only two layers within its RSSM [10]. The small memory overhead is around 22GB which allows us to train on a single NVIDIA 4090 GPU alongside running CARLA simulator. 

We train the agent on each task. The change in reward curves with respect to time steps is shown in Figure 2. All the tasks here are trained with intention sharing and full observability. Simpler tasks with less traffic, such as ‘right turn simple’ and ‘lane merge’, typically converge within 50k steps (about 1 hour), whereas tasks involving denser, aggressive traffic flows, which require collision avoidance, take approximately 150k-200k steps to converge (about 3 to 4 hours). 

In our evaluation, we employ several metrics to rigorously assess the performance of autonomous driving agents executed within the CarDreamer tasks, detailed in Table 1. These metrics include: 

- **Success Rate:** This metric measures the percentage of episodes in which the ego vehicle successfully completes the task by reaching a destination point or traveling a predetermined distance without incident or out of lanes. 

- **Collision Rate (%):** Calculates the percentage of episodes where the ego vehicle is involved in a collision. 

- **Average Speed (m/s):** Measures the average speed maintained by the ego vehicle throughout the task. This metric is indicative of how efficiently the vehicle navigates the environment, balancing speed with safety. 

It is worth noting that several tasks, such as ‘right turn’ and ‘left turn’, are notably challenging in environments with background traffic, where traffic flows aggressively and always disregards traffic rules and signs. This behavior increases the potential for collisions with the ego vehicle. Consequently, the AV must accurately predict future maneuvering of other vehicles to successfully navigate through the task. 

6 

A TECHNICAL REPORT - JULY 29, 2024 


Figure 3: Sampled images during one episode in different tasks. 

Table 1: Performance metrics in different tasks. 

|Tasks|Success Rate|Collision Rate|Avg. Speed (m/s)|
|---|---|---|---|
|Right turn simple|99.21%_±_0.49%|0.00 %_±_0.00%|3.19_±_0.01|
|Right turn medium|98.11 %_±_0.22%|1.89 %_±_0.22%|2.99_±_0.02|
|Right turn hard|99.58 %_±_0.42%|0.42 %_±_0.42%|2.92_±_0.02|
|Left turn simple|100.00%_±_0.00%|0.00%_±_0.00%|3.21_±_0.01|
|Left turn medium|97.58%_±_0.61%|2.42%_±_0.61%|3.04_±_0.03|
|Left turn hard|92.36%_±_3.03%|7.64 %_±_3.03%|2.97_±_0.01|
|Overtake|100.00%_±_0.00%|0.00%_±_0.00%|3.12_±_0.03|
|Four lane|96.83%_±_3.17%|3.17%_±_3.17%|3.47_±_0.00|
|Navigation|80.95%_±_6.41%|7.58%_±_4.01%|3.97_±_0.08|
|Lane merge|90.61%_±_1.17%|9.39%_±_1.17%|5.17_±_0.01|
|Roundabout|96.00%_±_2.31%|4.00%_±_2.31%|3.58_±_0.00|
|Traffic lights|92.65%_±_0.85%|0.00%_±_0.00%|2.26_±_0.03|
|Stop sign|97.94%_±_1.09%|0.00%_±_0.00%|1.80_±_0.01|


7 

A TECHNICAL REPORT - JULY 29, 2024 


Figure 4: Comparison of the ground-truth observations and the ones imagined by WM in different modality settings 

8 

A TECHNICAL REPORT - JULY 29, 2024 


Figure 5: Reward curves in different observability settings. 

### **5.2 Predictions in Different Observation Modalities** 

WM’s imagination capability allows it to effectively predict future scenarios and manage potential events. To evaluate the WM’s imagination performance with observations of different modalities, we conduct the experiments on the “right turn hard” task. We choose three different modalities: BEV, camera, and LiDAR. For each one, the WM is required to imagine the observations in a few future steps given the start state and a series of actions. 

The results, illustrated in Figure 4, compare the ground-truth images with the imagined ones across three modalities. The first row displays the ground truth observation images, the second row the WM’s imagined outcomes, and the third row the differences between them. We selected frames within an imagination horizon of up to 64 time steps. 

The findings demonstrate the WM’s proficiency in accurately predicting the future despite the different modalities. In the BEV experiment (a), the WM precisely predicted the positions and trajectories of vehicles moving straight and making right turns, as well as the rotation and translation of the BEV with respect to the ego vehicle. Similarly, in camera and LiDAR settings, WM successfully predicts a vehicle driving in front of the ego vehicle. 

### **5.3 Benefits of V2V Communication** 

A distinctive feature of CarDreamer is its ability to facilitate easy customization of the level to which vehicles communicate. Vehicles can share FOV views, leading to different observability. Besides, they can even share intentions (represented by vehicles’ planned waypoints) for better planning. We utilize this feature to evaluate the impact of communication. An agent is trained and tested on the “right turn hard” task under different settings, i.e., different observability and whether it has access to others’ intentions. The “right turn hard” task is particularly suitable for testing observability and intention communication due to the dense traffic and frequent potential for collisions from vehicles outside the FOV. 

The reward curves are shown in Figure 5 and the performance metrics are shown in Table 2 and Table 3. Note that the successful right turn is approximately indicated by the rewards exceeding 300. The results show that limited observability or lack of intention sharing impedes the agent from completing the task. The success rates of tasks with the above limits are significant lower than the task with full information. The evenly sampled images during one episode (shown in Figure 6) provides a good explanation: the agent adopts a conservative and sub-optimal policy. For example, in the ’FOV’ and ’SFOV’ setting in Figure 6, the agent hesitates to move on since they have insufficient information about coming vehicles. In the ’No intention sharing’ setting, the agent cuts in at an inappropriate timing that leads to a collision without shared intentions. In contrast, the complete information enables the ego vehicle to successfully execute the right turn. 

9 

A TECHNICAL REPORT - JULY 29, 2024 

Table 2: Metrics in different observability settings (with intention sharing). 

|Settings|Success Rate|Collision Rate|Avg. Speed (m/s)|
|---|---|---|---|
|Full Observability|99.58 %_±_0.42%|0.42 %_±_0.42%|2.92_±_0.02|
|FOV Observability|12.44 %_±_1.79%|87.56 %_±_1.79%|2.78_±_0.01|
|SFOV Observability|29.52 %_±_3.46%|70.48 %_±_3.46%|2.86_±_0.09|


Table 3: Metrics in different intention sharing settings (with full observability). 

|Settings|Success Rate|Collision Rate|Avg. Speed (m/s)|
|---|---|---|---|
|Intention Sharing|99.58 %_±_0.42%|0.42 %_±_0.42%|2.92_±_0.02|
|No Intention Sharing|90.71 %_±_0.61%|8.94 %_±_0.58%|3.08_±_0.00|


## **6 Conclusion** 

In this work, we introduced CarDreamer, an open-source learning platform tailored for the development and evaluation of WM based RL algorithms in autonomous driving. CarDreamer offers a comprehensive set of built-in tasks, a flexible task development suite, and an integrated world model backbone, all aimed at facilitating rapid prototyping of driving tasks and algorithm testing within this specialized domain. With its modular design and diverse task configurations, CarDreamer establishes itself as a flexible and challenging testbed for assessing the performance of WM based autonomous driving systems. The experiments we conduct using our platform gives a comprehensive evaluation of the performance of DreamerV3 different driving tasks. We emphasize its predictive accuracy across different observation modalities and the significant impact of communication on performance. 

Looking to the future, a promising avenue for further development involves the integration of curriculum learning [34] and continual learning [35] strategies. These approaches aim to systematically enhance the learning process by gradually increasing task complexity or continuously integrating new knowledge without forgetting previously acquired information. Furthermore, exploring advanced techniques such as transfer learning [36] and meta-learning [37] could significantly improve the platform’s capabilities for few-shot adaptation to new environments. This would further augment CarDreamer’s utility in developing more generalized and robust autonomous driving approaches. 

## **References** 

- [1] Sorin Grigorescu, Bogdan Trasnea, Tiberiu Cocias, and Gigel Macesanu. A survey of deep learning techniques for autonomous driving. _Journal of field robotics_ , 37(3):362–386, 2020. 

- [2] Matthew Schwall, Tom Daniel, Trent Victor, Francesca Favaro, and Henning Hohnhold. Waymo public road safety performance data. _arXiv preprint arXiv:2011.00038_ , 2020. 

- [3] Ekim Yurtsever, Jacob Lambert, Alexander Carballo, and Kazuya Takeda. A survey of autonomous driving: Common practices and emerging technologies. _IEEE access_ , 8:58443–58469, 2020. 

- [4] Siyu Teng, Xuemin Hu, Peng Deng, Bai Li, Yuchen Li, Yunfeng Ai, Dongsheng Yang, Lingxi Li, Zhe Xuanyuan, Fenghua Zhu, et al. Motion planning for autonomous driving: The state of the art and future perspectives. _IEEE Transactions on Intelligent Vehicles_ , 2023. 

- [5] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. _arXiv preprint arXiv:2306.16927_ , 2023. 

- [6] Crash rate calculations by US department of transportation federal highway administration. `https://safety. fhwa.dot.gov/local_rural/training/fhwasa1109/app_c.cfm` . [Accessed 07-05-2024]. 

- [7] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- [8] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 

- [9] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, Zachary Murez, Corina Gurau, Hudson Yeo, Alex Kendall, Roberto Cipolla, and Jamie Shotton. Model-based imitation learning for urban driving. _Advances in Neural Information Processing Systems_ , 35:20703–20716, 2022. 

- [10] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

10 

A TECHNICAL REPORT - JULY 29, 2024 


Figure 6: Sampled images during one episode in different communication and observability settings. 

- [11] Yang Yu. Towards sample efficient reinforcement learning. In _IJCAI_ , pages 5739–5743, 2018. 

- [12] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _International conference on machine learning_ , pages 2555–2565. PMLR, 2019. 

- [13] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. _arXiv preprint arXiv:2010.02193_ , 2020. 

- [14] Minting Pan, Xiangming Zhu, Yunbo Wang, and Xiaokang Yang. Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models. _Advances in Neural Information Processing Systems_ , 35:23178–23191, 2022. 

- [15] Ramanan Sekar, Oleh Rybkin, Kostas Daniilidis, Pieter Abbeel, Danijar Hafner, and Deepak Pathak. Planning to explore via self-supervised world models. In _International conference on machine learning_ , pages 8583–8592. PMLR, 2020. 

- [16] Russell Mendonca, Oleh Rybkin, Kostas Daniilidis, Danijar Hafner, and Deepak Pathak. Discovering and achieving goals via world models. _Advances in Neural Information Processing Systems_ , 34:24379–24391, 2021. 

- [17] Yanchen Guan, Haicheng Liao, Zhenning Li, Guohui Zhang, and Chengzhong Xu. World models for autonomous driving: An initial survey. _arXiv preprint arXiv:2403.02622_ , 2024. 

- [18] Zheng Zhu, Xiaofeng Wang, Wangbo Zhao, Chen Min, Nianchen Deng, Min Dou, Yuqi Wang, Botian Shi, Kai Wang, Chi Zhang, et al. Is sora a world simulator? a comprehensive survey on general world models and beyond. _arXiv preprint arXiv:2405.03520_ , 2024. 

- [19] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [20] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, and Jiwen Lu. Drivedreamer: Towards real-world-driven world models for autonomous driving. _arXiv preprint arXiv:2309.09777_ , 2023. 

- [21] Fan Jia, Weixin Mao, Yingfei Liu, Yucheng Zhao, Yuqing Wen, Chi Zhang, Xiangyu Zhang, and Tiancai Wang. Adriver-i: A general world model for autonomous driving. _arXiv preprint arXiv:2311.13549_ , 2023. 

- [22] Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Xinze Chen, Guan Huang, Xiaoyi Bao, and Xingang Wang. Drivedreamer-2: Llm-enhanced world models for diverse driving video generation. _arXiv preprint arXiv:2403.06845_ , 2024. 

11 

A TECHNICAL REPORT - JULY 29, 2024 

- [23] Zeyu Gao, Yao Mu, Ruoyan Shen, Chen Chen, Yangang Ren, Jianyu Chen, Shengbo Eben Li, Ping Luo, and Yanfeng Lu. Enhance sample efficiency and robustness of end-to-end urban autonomous driving via semantic masked world model. _arXiv preprint arXiv:2210.04017_ , 2022. 

- [24] Qifeng Li, Xiaosong Jia, Shaobo Wang, and Junchi Yan. Think2drive: Efficient reinforcement learning by thinking in latent world model for quasi-realistic autonomous driving (in carla-v2). _arXiv preprint arXiv:2402.16720_ , 2024. 

- [25] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In _Conference on robot learning_ , pages 1–16. PMLR, 2017. 

- [26] Pablo Alvarez Lopez, Michael Behrisch, Laura Bieker-Walz, Jakob Erdmann, Yun-Pang Flötteröd, Robert Hilbrich, Leonhard Lücken, Johannes Rummel, Peter Wagner, and Evamarie Wiessner. Microscopic traffic simulation using sumo. In _2018 21st International Conference on Intelligent Transportation Systems (ITSC)_ , pages 2575–2582, 2018. 

- [27] Cathy Wu, Abdul Rahman Kreidieh, Kanaad Parvate, Eugene Vinitsky, and Alexandre Bayen. Flow: Architecture and benchmarking for reinforcement learning in traffic control. 10 2017. 

- [28] Greg Brockman, Vicki Cheung, Ludwig Pettersson, Jonas Schneider, John Schulman, Jie Tang, and Wojciech Zaremba. Openai gym. _arXiv preprint arXiv:1606.01540_ , 2016. 

- [29] Jakob Foerster, Ioannis Alexandros Assael, Nando De Freitas, and Shimon Whiteson. Learning to communicate with deep multi-agent reinforcement learning. _Advances in neural information processing systems_ , 29, 2016. 

- [30] Changxi Zhu, Mehdi Dastani, and Shihan Wang. A survey of multi-agent reinforcement learning with communication. _arXiv preprint arXiv:2203.08975_ , 2022. 

- [31] Dian Chen, Brady Zhou, Vladlen Koltun, and Philipp Krähenbühl. Learning by cheating. In _Conference on Robot Learning_ , pages 66–75. PMLR, 2020. 

- [32] Shuo Feng, Haowei Sun, Xintao Yan, Haojie Zhu, Zhengxia Zou, Shengyin Shen, and Henry X Liu. Dense reinforcement learning for safety validation of autonomous vehicles. _Nature_ , 615(7953):620–627, 2023. 

- [33] Nidhi Kalra and Susan M. Paddock. Driving to safety: How many miles of driving would it take to demonstrate autonomous vehicle reliability? _Transportation Research Part A: Policy and Practice_ , 94:182–193, 2016. 

- [34] Yoshua Bengio, Jérôme Louradour, Ronan Collobert, and Jason Weston. Curriculum learning. In _Proceedings of the 26th annual international conference on machine learning_ , pages 41–48, 2009. 

- [35] Matthias De Lange, Rahaf Aljundi, Marc Masana, Sarah Parisot, Xu Jia, Aleš Leonardis, Gregory Slabaugh, and Tinne Tuytelaars. A continual learning survey: Defying forgetting in classification tasks. _IEEE transactions on pattern analysis and machine intelligence_ , 44(7):3366–3385, 2021. 

- [36] Karl Weiss, Taghi M Khoshgoftaar, and DingDing Wang. A survey of transfer learning. _Journal of Big data_ , 3:1–40, 2016. 

- [37] Timothy Hospedales, Antreas Antoniou, Paul Micaelli, and Amos Storkey. Meta-learning in neural networks: A survey. _IEEE transactions on pattern analysis and machine intelligence_ , 44(9):5149–5169, 2021. 

12 

