---
title: "A Survey: Learning Embodied Intelligence from Physical Simulators and World Models"
date: "2025-07-01"
authors: "Xiaoxiao Long; Qingrui Zhao; Kaiwen Zhang; Zihao Zhang; Dingrui Wang; Yumeng Liu"
url: https://arxiv.org/abs/2507.00917
pdf: https://arxiv.org/pdf/2507.00917
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2507.00917)** / [論文ページ](https://arxiv.org/abs/2507.00917)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# A Survey: Learning Embodied Intelligence from Physical Simulators and World Models 

Xiaoxiao Long<sup>_∗_</sup> , Qingrui Zhao<sup>_∗_</sup> , Kaiwen Zhang<sup>_∗_</sup> , Zihao Zhang<sup>_∗_</sup> , Dingrui Wang<sup>_∗_</sup> , Yumeng Liu<sup>_∗_</sup> , Zhengjie Shu<sup>_∗_</sup> , Yi Lu<sup>_∗_</sup> , Shouzheng Wang<sup>_∗_</sup> , Xinzhe Wei<sup>_∗_</sup> , Wei Li, Wei Yin, Yao Yao, Jia Pan, Qiu Shen, Ruigang Yang, Xun Cao<sup>_†_</sup> , Qionghai Dai 

**Abstract** —The pursuit of artificial general intelligence (AGI) has placed embodied intelligence at the forefront of robotics research. Embodied intelligence focuses on agents capable of perceiving, reasoning, and acting within the physical world. Achieving robust embodied intelligence requires not only advanced perception and control, but also the ability to ground abstract cognition in real-world interactions. Two foundational technologies, physical simulators and world models, have emerged as critical enablers in this quest. Physical simulators provide controlled, high-fidelity environments for training and evaluating robotic agents, allowing safe and efficient development of complex behaviors. In contrast, world models empower robots with internal representations of their surroundings, enabling predictive planning and adaptive decision-making beyond direct sensory input. This survey systematically reviews recent advances in learning embodied AI through the integration of physical simulators and world models. We analyze their complementary roles in enhancing autonomy, adaptability, and generalization in intelligent robots, and discuss the interplay between external simulation and internal modeling in bridging the gap between simulated training and real-world deployment. By synthesizing current progress and identifying open challenges, this survey aims to provide a comprehensive perspective on the path toward more capable and generalizable embodied AI systems. We also maintain an active repository that contains up-to-date literature and open-source projects at https://github.com/NJU3DV-LoongGroup/Embodied-World-Models-Survey. 

**Index Terms** —Embodied Intelligence, World Model, Physical Simulator, Autonomous Driving, Robotic Learning 

✦ 

## **1 INTRODUCTION** 

### **1.1 Overview** 

With the rapid advancement of artificial intelligence [1], [2] and robotics technology [3], [4], the interaction between intelligent agents and the physical world has increasingly become a central focus of research. The pursuit of artificial general intelligence (AGI), systems that can match or exceed human cognitive abilities across diverse domains, faces a key question: _how to ground abstract reasoning in real-world understanding and action?_ 

Intelligent robots have emerged as essential embodied agents paving the way toward AGI by providing the physical medium that bridges computational intelligence with interaction in real-world environments. Unlike disembodied intelligence systems that operate purely on symbolic or digital data, embodied intelligence emphasizes the importance of perception, action, and cognition through physical interaction with the environment. This paradigm allows 

> _• ∗ indicates equal contributions. † indicates corresponding authors. • Xiaoxiao Long, Qingrui Zhao, Yi Lu, Yao Yao, Qiu Shen, Wei Li and Xun Cao are with the Nanjing University (e-mail: caoxun@nju.edu.cn)._ 


Fig. 1: Physical simulator and world model play vital roles for embodied intelligence. Simulator provides an explicit modeling of the real world, offering a controlled environment where robots can train, test, and refine their behaviors. World model offers internal representations of the environment, enabling robots to autonomously simulate, predict, and plan actions within their cognitive framework. 

- _Yumeng Liu, Zhengjie Shu and Jia Pan are with the University of Hong Kong._ 

> _• Shouzheng Wang is with the Central South University._ 

- _Wei Yin is with the Horizon Robotics._ 

- _Zihao Zhang and Xinzhe Wei are with the Institute of Computing Technology, Chinese Academy of Sciences (ICT). Xinzhe Wei is also with the University of Chinese Academy of Sciences._ 

- _Ruigang Yang and Zhengjie Shu are with the Shanghai Jiao Tong University._ 

- _Dingrui Wang is with the Technical University of Munich._ 

- _Kaiwen Zhang and Qionghai Dai are with the Tsinghua University._ 

robots to adjust their behavior and cognition continuously based on feedback from the physical world while executing tasks, making robotics not merely an application of AI, but a essential component of the path toward general intelligence. 

The significance of embodied intelligence extends beyond the execution of physical tasks. By acting and perceiving within a physical body [5], robots can robustly learn 

2 


Fig. 2: Survey outline: We categorize intelligent robot development into five levels (IR-L0 to IR-L4) and review progress and key techniques in robotic mobility, manipulation, and interaction (§3), the use of physical simulators for learning and control algorithm verification (§4), and the design and use of world models as internal representations for learning, planning, and decision-making (§5–§6), emphasizing both explicit and implicit learning pathways. 

from experience, test hypotheses, and refine their strategies through ongoing interaction. This closed-loop integration of sensory input, motor control, and cognitive processing forms the foundation for true autonomy and adaptability, allowing robots to reason about and respond to the world in a more human-like manner [6]. 

As intelligent robots are increasingly deployed in realworld scenarios, such as elderly care [7], medical assistance [8], disaster rescue [9] and education [10]. Their ability to operate autonomously and safely in dynamic, uncertain environments becomes paramount. However, the diversity of applications and the rapid pace of technological progress have created a pressing need for a systematic framework to evaluate and compare robot capabilities. Establishing a scientifically sound grading system for robot intelligence not only clarifies the technological development roadmap, but also provides essential guidance for regulation, safety assessment, and ethical deployment. 

To address this need, recent research has explored various frameworks for quantifying robot capabilities, such as the DARPA Robotics Challenge evaluation scheme [11], the ISO 13482 standard for service robot safety [12], and reviews on autonomy levels [13], [14]. Nevertheless, a comprehensive grading system that integrates the dimensions of intelligent cognition, autonomous behavior, and social interaction remains lacking. 

In this work, we propose a capability grading model for intelligent robots, systematically outlining five progressive levels (IR-L0 to IR-L4) from basic mechanical execution to advanced, fully autonomous social intelligence. This classification encompasses key dimensions such as autonomy, task handling ability, environmental adaptability, and societal cognition, providing a unified framework to assess and guide the development of intelligent robots across the full spectrum of technological evolution. 

Central to enabling intelligent behavior in robots are two key technologies: physical simulators and world models. Both play vital roles in improving the robot’s control capabilities and extending its potential. Simulators, such as Gazebo [15] or MuJoCo [16], provide an explicit modeling of the physical world, offering a controlled environment where 

robots can train, test, and refine their behaviors before being deployed in real-world scenarios. These simulators serve as training grounds where the robot’s actions can be predicted, tested, and fine-tuned without the high costs and risks of real-world experimentation. 

Unlike simulators, world models offer internal representations of the environment, enabling robots to autonomously simulate, predict, and plan actions within their cognitive framework. Following NVIDIA’s definition, world models are ”generative AI models that understand the dynamics of the real world, including physics and spatial properties” [17]. This concept gained significant attention with Ha and Schmidhuber’s seminal work [18], which demonstrated how agents could learn compact environmental representations for internal planning. 

The synergy between simulators and world models enhances robots’ autonomy, adaptability, and task performance across diverse scenarios. This paper will explore the interplay between robot control algorithms, simulators, and world models. By examining how simulators provide a structured, external environment for training and how world models create internal representations for more adaptive decision-making, we aim to provide a comprehensive understanding of how these components work together to enhance the capabilities of intelligent robots. 

### **1.2 Scope and Contributions** 

**Scope.** This survey offers a comprehensive analysis of the interplay among robot control algorithms, simulators, and world models, mainly focusing on developments from 2018 to 2025. Our coverage includes both traditional physicsbased simulators and emerging world models, emphasizing their impact on autonomous driving and robots. 

This survey distinguishes itself from existing literature by providing a comprehensive examination of the synergistic relationship between physical simulators and world models in advancing embodied intelligence. While previous surveys have typically focused on individual components (such as robotics simulators [19]–[21] and world models [22]–[24]) our work bridges these domains to reveal their complementary roles in intelligent robot development. 

3 

**Contribution.** The main contributions of this survey are: 

- **Levels of intelligent robots:** Propose a comprehensive five-level grading standard (IR-L0 to IR-L4) for humanoid robot autonomy evaluation across four key dimensions: autonomy, task handling ability, environmental adaptability, and societal cognition ability. 

- **Analysis of recent techniques of robot learning:** Systematically review recent developments in intelligent robotics across legged locomotion (bipedal walking, fall recovery), manipulation (dexterous control, bimanual coordination), and human-robot interaction (cognitive collaboration, social embeddedness). 

- **Analysis of current physical simulators:** Provide comprehensive comparative analysis of mainstream simulators (Webots, Gazebo, MuJoCo, Isaac Gym/Sim/Lab etc.) covering physical simulation capabilities, rendering quality, and sensor support. 

- **Recent advancements of World Models:** We first revisit the main architectures of world models and their potential roles, for example, serve as controllable simulators, dynamic models, and reward models for embodied intelligence. Furthermore, we comprehensively discuss the recent world models designed for specific applications such as autonomous driving and articulated robots. 

### **1.3 Structure** 

A summary of the paper structure is illustrated in Fig. 2, which is presented as follows: 

- Sec. 1 introduces the importance of embodied AI and outlines how physical simulators and world models contribute to the development of embodied AI. 

- Sec. 2 provides a comprehending grading system for intelligent robots in five levels. 

- Sec. 2.1 Level Criteria. 

- Sec. 2.2 Level Factors. 

- Sec. 2.3 Classification Levels. 

- Sec. 3 reviews current progresses in intelligent robotic tasks in terms of mobility, dexterity and human-robot interaction. 

- Sec. 3.1 Related Robotic Techniques. 

- Sec. 3.2 Robotic Locomotion. 

- Sec. 3.3 Robotic Manipulation. 

- Sec. 3.4 Human-Robot Interaction. 

- Sec. 4 discusses pros and cons of mainstream simulators in contemporary robotics research. **–** Sec. 4.1 Main stream Simulators. 

- Sec. 4.2 Physical Properties of Simulators. 

- Sec. 4.3 Rendering Capabilities. 

- Sec. 4.4 Sensor and Joint Component Types. 

- Sec. 4.5 Discussions and Future Perspectives. 

- Sec. 5 introduces the representative architectures and core roles of world models. 

- Sec. 5.1 Representative Architectures of World Models. 

- Sec. 5.2 Core Roles of World Models. 

- Sec. 6 further reviews applications and challenges of world models for intelligent agents including autonomous driving and articulated robots. 

- Sec. 6.1 World Models for Autonomous Driving. 

- Sec. 6.2 World Models for Articulated Robots. 

- Sec. 6.3 Challenges and Future Perspectives. 

## **2 LEVELS OF INTELLIGENT ROBOT** 

With the rapid development in fields such as artificial intelligence, mechanical engineering, sensor fusion, and humancomputer interaction, intelligent robots are gradually transitioning from laboratories to real-world scenarios, including elderly care [7], medical assistance [8], disaster rescue [9] and education [10]. Unlike traditional industrial robots, intelligent robots emphasize the completion of complex cognition, perception, and execution tasks based on human-like structures. The dynamic nature and uncertainty they face in real environments make capability assessment a critical issue. Therefore, establishing a scientifically sound capability grading system not only helps clarify the technological development roadmap but also provides guidance for robot regulation and safety assessment. 

Currently, several studies have attempted to quantify robot capabilities, such as the DARPA Robotics Challenge framework for evaluating the ability to perform complex tasks [11], the ISO 13482 standard for service robot safety grading [12], and reviews on robot levels of autonomy [13], [14]. However, a comprehensive grading system that combines the dimensions of ”intelligent cognition” and ”autonomous behavior” is still lacking. To address this, this paper proposes and systematically outlines a capability grading model for intelligent robots from IR-L0 to IR-L4, covering the full technological evolution path from mechanical operation levels to advanced social interaction levels. 

### **2.1 Level Criteria** 

This standard classifies robots based on: their ability to perform tasks in various environments, the depth of autonomous decision-making, interaction complexity, and ethical cognition. The following core dimensions are covered: 

- The robot’s ability to complete tasks independently, ranging from full reliance on human control to full autonomy. 

- The difficulty of tasks the robot can handle, from simple repetitive labor to innovative problem-solving. 

- The robot’s ability to work in dynamic or extreme environments. 

- The robot’s capacity to understand, interact with, and respond to social situations within human society. 

### **2.2 Level Factors** 

The intelligent level of robots is graded based on the following five factors. 

- **Autonomy** : This factor is based on the robot’s ability to autonomously make decisions across various tasks. 

- **Task Handling Ability** : This factor is based on the complexity of the tasks the robot can perform. 

- **Environmental Adaptability** : This factor is based on the robot’s performance in different environments. 

- **Societal Cognition Ability** : This factor is based on the level of intelligence exhibited by robots in social scenarios. 

4 


Fig. 3: Levels of Intelligent Robotics: From Basic Execution to Full Autonomy. 

|**Level**|**Autonomy**|**Task Handling Ability**|**Environmental Adaptability**|**Societal Cognition Ability**|
|---|---|---|---|---|
|**IR-L0**|Human Control|Basic Tasks|Controlled Only|No Social Cognition|
|**IR-L1**|Human Supervised|Complex Navigation|Predictable Environments|Basic Recognition|
|**IR-L2**|Human Assisted|Dynamic Collaboration|Adaptive Learning|Simple Interaction|
|**IR-L3**|Conditional<br>Autonomy|Multitasking|Dynamic Adaptation|Emotional Intelligence|
|**IR-L4**|Full Autonomy|Innovation|Universal Flexibility|Advanced Social Intelligence|


TABLE 1: Relationship between graded levels and level factors. 

The relationship between graded levels and level factors are listed in table 1. 

- **Human-Robot Interaction:** None, or limited to simple buttons/teleoperation. 

### **2.3 Classification Levels** 

### _2.3.1_ **_IR-L0:_** _Basic Execution Level_ 

IR-L0 represents the foundational execution level in this system, characterized by a completely non-intelligent, program-driven attribute. Robots at this level are focused on executing highly repetitive, mechanized, deterministic tasks, such as industrial welding and fixed-path material handling. The ”low perception - high execution” operational mode makes the robot entirely relies on predefined programmatic instructions or real-time teleoperation. It lacks environmental perception, state feedback, or autonomous decision-making capability, forming a unidirectional closedloop system with ”command input - mechanical execution” [25]. The potential technical requirements are summarized as follows: 

- **Hardware:** High-precision servomotors and rigid mechanical structures, with motion controllers based on PLC or MCU. 

- **Perception:** Extremely limited, typically involving only limit switches, encoders, etc. 

- **Control Algorithms:** Mainly based on predefined scripts, action sequences, or teleoperation, without realtime feedback loops. 

### _2.3.2_ **_IR-L1:_** _Programmatic Response Level_ 

IR-L1 robots feature limited rule-based reactive capabilities, enabling them to execute predefined task sequences such as those performed by cleaning and reception robots. These systems utilize fundamental sensors, including infrared, ultrasonic, and pressure sensors, to trigger specific behavioral patterns. They cannot process complex or unforeseen events and can demonstrate operational stability only in closedtask environments with clearly defined rules. They embody a ”limited perception–limited execution” paradigm, representing the beginning of basic robotic intelligence [26]. The potential technical requirements are summarized as follows: 

- **Hardware:** Integration of basic sensors (infrared, ultrasonic, pressure) with moderately enhanced processor capabilities. 

- **Perception:** Detection of obstacles, boundaries, and simple human movements. 

- **Control Algorithms:** Rule engines and finite state machines (FSM), supplemented by basic SLAM or random walk algorithms. 

- **Human-Robot Interaction:** Basic voice and touch interfaces supporting simple command-response protocols. 

- **Software Architecture:** Embedded real-time operating systems with elementary task scheduling capabilities. 

5 

### _2.3.3_ **_IR-L2:_** _Basic Perception and Adaptation Level_ 

IR-L2 robots introduce preliminary environmental awareness and autonomous capabilities, representing a significant advancement in robotic intelligence. Their characteristics include fundamental responsiveness to environmental changes and the ability to transition between multiple task modes. For instance, a service robot at this level can execute distinct tasks such as ”water delivery” or ”navigation guidance” based on voice commands while simultaneously avoiding obstacles during path execution. These systems require integrated perception modules (cameras, microphone arrays, LiDAR) and basic behavior-decision frameworks, such as Finite State Machines (FSM) or Behavior Trees [27]. 

While human supervision remains essential, IR-L2 robots demonstrate substantially greater execution flexibility compared to IR-L1 systems, signifying their progression toward genuine ”contextual understanding.” The potential technical requirements are summarized as follows: _•_ **Hardware:** Multimodal sensor arrays (cameras, LiDAR, microphone arrays) coupled with enhanced computational resources. 

- **Perception:** Visual processing, auditory recognition, and spatial localization capabilities enabling basic object identification and environmental mapping. 

- **Control Algorithms:** Finite state machines, behavior trees, SLAM implementations, path planning, and obstacle avoidance systems. 

- **Human-Robot Interaction:** Speech recognition and synthesis capabilities supporting comprehension and execution of basic commands. 

- **Software Architecture:** Modular design framework facilitating parallel task execution with preliminary priority management systems. 

### _2.3.4_ **_IR-L3:_** _Humanoid Cognition and Collaboration Level_ 

IR-L3 robots demonstrate autonomous decision-making capabilities in complex, dynamic environments while supporting sophisticated multimodal human-robot interaction. These systems can infer user intent, adapt their behavior accordingly, and operate within established ethical constraints. For example, in eldercare application, IR-L3 robots analyze speech patterns and facial expressions to detect emotional state changes in elderly patients, responding with appropriate comforting actions or emergency alerts. The potential technical requirements are summarized as follows: 

- **Hardware:** High-performance computing platforms integrated with comprehensive multimodal sensor suites (depth cameras, electromyography sensors, forcesensing arrays). 

- **Perception:** Multimodal fusion of vision, speech, and tactile inputs; affective computing for emotion recognition and dynamic user modeling. 

- **Control Algorithms:** Deep learning architectures (CNNs, Transformers) for perception and language understanding; reinforcement learning for adaptive policy optimization; planning and reasoning modules for complex task workflow management. 

- **Human-Robot Interaction:** Multi-turn natural language dialogue support; facial expression recognition and feedback; foundational empathy and emotion regulation capabilities. 

- **Software Architecture:** Service-oriented, distributed frameworks enabling task decomposition and collaborative execution; integrated learning and adaptation mechanisms. 

- **Safety and Ethics:** Embedded ethical governance systems to prevent unsafe or non-compliant behaviors. 

### _2.3.5_ **_IR-L4:_** _Fully Autonomous Level_ 

IR-L4 represents the pinnacle of intelligent robotics: systems with complete autonomy in perception, decision-making, and execution, capable of independent operation in any environment without human intervention. These robots possess self-evolving ethical reasoning, advanced cognition, empathy, and long-term adaptive learning capabilities. Beyond handling open-ended tasks, they engage in sophisticated social interactions, including multi-turn natural language dialogue, emotional understanding, cultural adaptation, and multi-agent collaboration. The potential technical requirements are summarized as follows: 

- **Hardware:** Highly biomimetic structures featuring fullbody, multi-degree-of-freedom articulation; distributed high-performance computing platforms. 

- **Perception:** Omnidirectional, multi-scale, multimodal sensing systems; real-time environment modeling and intent inference. 

- **Control Algorithms:** General Artificial Intelligence (AGI) frameworks integrating meta-learning, generative AI, and embodied intelligence; autonomous task generation and advanced reasoning capabilities. 

- **Human-Robot Interaction:** Natural language understanding and generation; complex social context adaptation; empathy and ethical deliberation. 

- **Software Architecture:** Cloud-edge-client collaborative systems; distributed agent architectures supporting self-evolution and knowledge transfer. 

- **Safety and Ethics:** Embedded dynamic ethical decision systems constraining behavior and enabling morally sound choices in ethical dilemmas. 

## **3 ROBOTIC MOBILITY, DEXTERITY AND INTERACTION** 

Among the various embodiments of intelligent robots, humanoid robots—characterized by their human-like appearance—stand out for their ability to seamlessly integrate into human-centered environments and provide meaningful assistance. As such, they serve as crucial physical representations of embodied intelligence. 

Recently, the rapid advancement of machine learning technologies has led to significant breakthroughs in robot whole-body control and general manipulation. This chapter begin by outlining fundamental technical approaches in intelligent robotics, then review the latest developments in robot locomotion and manipulation, and finally, examine ongoing research aimed at enabling natural and intuitive human-robot interactions. 

### **3.1 Related Robotic Techniques** 

### _3.1.1 Model Predictive Control, MPC_ 

Model Predictive Control (MPC) [28] is a powerful control strategy that has gained significant traction in the field 

6 

of humanoid robotics over the past two decades. At its core, MPC is an optimization-based approach that predicts the future behavior of a system using a dynamic model, and computes control actions by solving an optimization problem at each time step. This allows the controller to explicitly handle constraints on inputs and states, making it particularly suitable for complex, high-dimensional systems like humanoid robots [29]. 

Tom Erez et al. introduced a comprehensive real-time MPC system that applied MPC to the full dynamics of a humanoid robot, enabling it to perform complex tasks such as standing, walking, and recovering from disturbances [30]. Building upon this foundation, in 2015, Jonas Koenemann, Andrea Del Prete, Yuval Tassa, Emanuel Todorov et al. implemented a complete MPC and applied it in real-time on the physical HRP-2 robot, marking the first time such a whole-body model predictive controller was applied in realtime on a complex dynamic robot [31]. 

### _3.1.2 Whole-Body Control, WBC_ 

Whole body control (WBC) in humanoid robotics is a comprehensive framework that enables robots to coordinate all of their joints and limbs simultaneously to achieve different motions. The basic methods of whole body control typically involve formulating the robot’s motion and force objectives as a set of prioritized tasks, such as maintaining balance, following a desired trajectory, or applying a specific force with the hand. These tasks are then translated into mathematical constraints and objectives, which are solved using optimization techniques or hierarchical control frameworks [32]. 

During implementation, WBC typically employs techniques such as dynamic modeling, inverse kinematics solving, and optimization algorithms to ensure that the robot achieves desired motion behaviors while satisfying physical constraints. In the early 2000s, Oussama Khatib and his collaborators introduced the operational space formulation for controlling redundant manipulators and later extended it to humanoid robots [33]. Optimization-based WBC offers strong flexibility, allowing for modular addition or removal of constraints and resolving conflicting constraints by setting different task hierarchies or soft task weightings [34]– [36]. In recent years, with the development of artificial intelligence such as reinforcement learning, researchers have proposed frameworks like ExBody2 [37] and HugWBC [38], which train control policies in simulated environments and transfer them to actual robots, achieving more natural and expressive whole-body motion control. 

### _3.1.3 Reinforcement Learning_ 

Reinforcement learning (RL) [39] is a branch of machine learning that has become increasingly influential in the field of humanoid robotics. The core insight of RL is that an agent—such as a humanoid robot—can learn to perform complex tasks by interacting with its environment and receiving feedback in the form of rewards or penalties. Unlike traditional control methods [40], [41] that require explicit programming or modeling of behaviors, RL enables robots to autonomously discover optimal actions through trial and error, making it particularly well-suited for high- 

dimensional, dynamic, and uncertain environments that humanoid robots often encounter [42]. 

The application of reinforcement learning to humanoid robotics dates back to the late 1990s and early 2000s. In 1998, Masahiro Morimoto and Kenji Doya introduced a reinforcement learning (RL) approach enabling a simulated two-joint, three-link robot to autonomously learn a dynamic standing-up motion from a lying position [43]. Since then, RL has been used to achieve complex behaviors for humanoid robots, DeepLoco [44] and other works [45], [46] did an extensive exploration of the ability of deep RL in bipedal tasks, but they have not shown to be be suitable for physical robots. In 2019, Xie et al. used iterative reinforcement learning and Deterministic Action Stochastic State (DASS) tuples to progressively refine the reward function and policy architecture, enabling robust dynamic walking for a physical Cassie bipedal robot [47]. 

### _3.1.4 Imitation Learning_ 

Imitation learning (IL) is a paradigm in robotics where robots learn to perform tasks by observing and mimicking demonstrations, typically provided by humans or other agents. The core insight behind imitation learning is that it bypasses the need for explicit programming or handcrafted reward functions, allowing humanoid robots to acquire complex behaviors more efficiently and intuitively. By leveraging demonstrations, robots can learn skills such as walking, manipulation, or social interaction, which are otherwise difficult to specify through traditional control or reinforcement learning methods [3], [48]–[50]. 

In humanoid robot motion control, IL often utilizes human motion capture data that has been re-targeted (Retargeting), or reference gaits generated from model-based trajectory planning (such as natural walking, running, etc.), and encourages the robot to follow these reference trajectories in simulation to achieve more natural and stable motion gaits [51]–[53]. 

While IL effectively utilizes existing knowledge for learning, it faces challenges such as high costs for obtaining expert demonstration data, insufficient data diversity, quality concerns, and time-consuming processes. Moreover, strategies trained on limited demonstration data often suffer from poor generalization, making them difficult to adapt to new environments or tasks. The operational skills learned may also be relatively narrow. To address these challenges, researchers and companies are focusing on developing more efficient data collection hardware platforms or teleoperation technologies to expand data [49], [54], [55], while also exploring new types of training data, such as extracting human actions from video data [56]. 

### _3.1.5 Visual-Language-Action Models, VLA_ 

Visual-Language-Action (VLA) models represent a crossmodal artificial intelligence framework that integrates visual perception, language understanding, and action generation. The core concept involves leveraging the reasoning capabilities of Large Language Models (LLMs) to directly map natural language instructions to actions of physical robotic. 

In 2023, Google DeepMind introduced RT-2, which first applied this paradigm to robot control by discretizing robot control instructions into language-like tokens, achieving 

7 


Fig. 4: Timeline of advancements in unstructured environment adaption of humanoid robot. 

end-to-end visual-language-action mapping [65]. By leveraging internet-scale visual-language data for pre-training, robots could understand previously unseen semantic concepts and generate reasonable action sequences through chain-of-thought reasoning. Subsequently, numerous endto-end VLA models emerged [4] [66] [67] [68] [69] [70] [71], further advancing the application and development of VLA models in robotics. 

Although current VLA models have made significant progress, several critical challenges still remain. These models often struggle to reliably handle tasks or environments they have not encountered before. Additionally, real-time inference constraints limit their responsiveness in dynamic situations. Furthermore, biases within training datasets, difficulties in semantic grounding across modalities, and the high computational complexity of system integration continue to hinder further development [72]. 

### **3.2 Robotic Locomotion** 

The goal of robotic locomotion is to achieve natural movement patterns, including walking, running, and jumping. By integrating multiple domains such as perception, planning, and control, robots with locomotion abilities could be categorized within our IR-L2 level. This integration enables robots to adapt dynamically to varying terrain, external disturbances, and unforeseen events, promoting robust and fluent bipedal motion. Moreover, the ability to autonomously recover from unexpected incidents reduces dependence on human intervention, paving the way toward greater intelligence and autonomy. This section will explore recent advancements in legged locomotion and discuss strategies for protecting and recovering from falls. 

### _3.2.1 Legged Locomotion_ 

Bipedal robots exhibit unique advantages in navigating complex terrains, emulating human behaviors, and seamlessly integrating into human-centric environments. Research in the field of bipedal locomotion control can be divided into two tasks: **Unstructured Environment Adaption** , which emphasizes the ability to maintain stable walking 

in complex, unknown or dynamic environments, and **High Dynamic Movements** , which focuses on achieving a balance between stability and agility in high-speed, dynamic movements such as running and jumping. 

**Unstructured Environment Adaption.** “Unstructured environments” typically refer to complex natural or manmade terrains, such as rugged mountain trails, gravelstrewn ground, slippery grass, staircases, and other unpredictable obstacles. Early efforts in bipedal walking stabilization mainly used position-controlled humanoid robots. In 2008, Sang-Ho Hyon [57] introduced a passivity-based contact force control framework, enabling the SARCOS humanoid robot [73] to actively balance on indoor terrains with varying heights and time-varying inclinations. Subsequent advancements explored diverse strategies to improve locomotion stability, including online learning for terrain adaptation [74], compliance control with terrain estimation [58], and the integration of Linear Inverted Pendulum Model (LIPM) with foot force control [75], as demonstrated by Kajita et al. in 2010 on the HRP-4C humanoid robot. 

Above mentioned methods only enabled humanoid robots with limited terrain adaptability, such as walking on thin beams, pavement, or flat but inclined ramp. This is due to the high gear-ratio of position controlled robot joints. These joints suffers from high impedance, which could easily cause damage under large impact applied to the output shaft or end-effector (hand and foot) [76]. To achieve better adaptability in unknown environments, modern humanoid and quadruped robots use force-controlled joints with low gear ratios, offering improved compliance and smoother responses under large impacts [77], [78]. 

With development of force-controlled humanoid robots and increased computational power, researchers are able to develop and implement more sophisticated control algorithms [85]. This further enhanced robots’ adaptability to diverse environments. Jacob Reher et al. introduced a comprehensive full-body dynamic controller that explicitly accounts for the passive spring mechanisms in the Cassie bipedal robot [59]. Their approach successfully achieved stable bipedal walking on various terrains, including outdoor grass. George Mesesan et al. combines Divergent Compo- 

8 


Fig. 5: Timeline of advancements in high dynamic movements of humanoid robot. 

nent of Motion (DCM) for center of mass trajectory planning with a passivity-based whole-body controller (WBC) to compute joint torques [60]. Demonstrated dynamic walking over soft gym mats with the TORO robot. 

Apart from proprioceptive blind walk, researchers also explored integrating exteroceptive sensing and path planning modules to tackle more complex environments. JiunnKai Huang et al. integrates a low-frequency path planner with a high-frequency reactive controller that generates smooth, feedback-driven motion commands [62]. This enables the Cassie Blue robot to autonomously traverse more complex terrains, such as the University of Michigan’s Wave Field. 

Learning-based methods also performed promising stability under outdoor complex environments. In 2020, Joonho Lee et al. [86] demonstrated the first successful real-world application of reinforcement learning to legged locomotion, outperforming traditional approaches in outdoor environments [87]. Jonah Siekmann et al. achieved blind stair traverse with the Cassie robot [61]. They used domain randomization methods to vary stair dimensions and robot dynamics, which enabled the learned policy to transfer successfully to real-world scenarios. Researchers also leveraged depth cameras and LiDAR to construct height maps [63], Perceptive Internal Models (PIM) [88], or end-to-end policy [64], significantly enhancing robot mobility across diverse terrains. Now robots can traverse stairs, overcome hurdles, and even jump across gaps up to 0.8 meters wide. 

**High Dynamic Movements.** Highly dynamic movements such as running and jumping impose greater demands on the control systems of bipedal robots. During rapid motion, robots must manage quick support transitions, posture adjustments, and precise force control within very short duration. 

Early studies employed simplified dynamic models, such as the Spring-Loaded Inverted Pendulum (SLIP) [89], Linear Inverted Pendulum Model (LIPM) [90], and Single Rigid Body Model (SRBM) [91], to reduce computational complexity and enable real-time control. Xiaobin Xiong and Aaron D. Ames developed a simplified spring-mass model controlled via a Control Lyapunov Function-based Quadratic Program (CLF-QP) [79], successfully achieving an 18 cm vertical jump with the Cassie robot. Qi et al. [80] proposed a Center of Pressure (CoP)-guided angular momentum controller based on LIPM, enabling vertical jumps of up to 0.5 meters by stabilizing angular momentum during flight. More recently, He et al. [83] introduced a Centroidal Dynamics Model (CDM) coupled with a MPC framework, termed CDM-MPC, to achieve continuous jumping motions 

on the KUAVO humanoid robot. 

RL-based methods have also been applied to dynamic tasks. Learned implicit robot dynamics have shown promising results in activities such as running [81], jumping [82], and parkour on discrete terrain [92], significantly broadening the capabilities of bipedal locomotion. 

Training highly dynamic motions from scratch often requires tedious reward function design and parameter tuning. Imitation learning, leveraging extensive human motion datasets [93], has been employed to achieve expressive and dynamic robot behaviors. Adversarial Motion Priors (AMP) [94] derive style-based rewards from motion capture data, enhancing the naturalness of robot movements. Frameworks such as Exbody [37], [95], OmniH2O [96], and ASAP [84] realized natural and agile whole-body movements. ASAP specifically addressing simulation-to-reality gaps, enabled sophisticated movements like the Fadeaway Jump-Shot. 

### _3.2.2 Fall Protection and Recovery_ 

Humanoid robots are prone to instability and falls which could cause hardware damage or interrupt operation. Therefore, fall protection for humanoid robots and efficient recovery to standing posture after falls have become major research topics in humanoid robotics. 

**Model-based Methods.** Early model-based fall protection and recovery control for humanoid robots largely drew inspiration from biomechanics, mimicking the biomechanical features of human falling processes combined with optimization control methods to generate motion trajectories that reduce damage during falls and achieve stable standing recovery. 

UKEMI [97] controlled the robot’s posture during falls to distribute impact forces and reduce damage to critical components. They also designed specific joint movement patterns and control strategies to enable robot fall recovery [98]. Libo Meng et al. proposed a falling motion control method through biomechanical analysis of human falls, achieving impact protection control adaptable to different falling directions [99]. Dong et al. proposed a compliant control framework that allows the robot to adjust its stiffness and damping characteristics in response to external disturbances, similar to how humans modulate muscle stiffness to maintain balance [100]. 

**Learning-based Methods.** Learning-based methods, with their insensitivity to high-precision models and strong generalization capabilities, can better address this task. HiFAR [102] trained humanoid robots to recover from falls through a multi-stage curriculum learning method that gradually increased scenario difficulty, achieving high success rates 

9 


Fig. 6: The HOST, proposed by Tao Huang et al. [101], enables the Unitree G1 robot to stand-up from diverse postures in complex environments. 

in fall recovery across various scenarios with real robots. HoST [101] enabled robust and natural standing actions on the Unitree G1 robot across various environments with smoothing regularization and implicit action velocity limits. Embrace Collisions [103] expanded the robot’s ability to interact with environment through whole-body contacts, rather than being restricted to hands and feet alone. By imitating human actions such as roll-and-stand, side-lying, and other multi-contact behaviors, this approach extended the range of motion and adaptability of humanoid robots in real-world scenarios. 

### **3.3 Robotic Manipulation** 

Robotic manipulation tasks encompass a wide range of activities, from simple actions like picking up objects to complex sequences involving assembly or cooking. 

This section will review research progress in robot manipulation, focusing on the increasing complexity of coordination required for different tasks. We will begin with manipulation using a single end effector, such as a hand or gripper, progress to bimanual coordination involving two arms, and finally address whole-body manipulation tasks that require the integrated control of the entire robot. 

### _3.3.1 Unimanual Manipulation Task_ 

Unimanual manipulation refers to the use of a single end effector to interact with and manipulate objects, such as a parallel gripper or a dexterous robotic hand. Tasks in this category range from basic pick-and-place operations to more complex actions such as pushing, inserting, tool usage, and manipulating deformable or articulated objects. The complexity of these tasks depends on the capabilities of the end effector and the environment it interacts with. **Gripper-based manipulation.** The parallel two-finger gripper [104] is the most common end effector for manipulation tasks like grasping, placing, and tool use, relying on simple opening and closing actions. Early research focused on precise physical models and pre-programming [105], effective in structured settings like industrial automation with predetermined trajectories or Visual Servoing [106] for feedback. These methods struggled with adaptability in unstructured environments, object diversity, and complex interactions (e.g., friction, deformation). 


Fig. 7: DexCap [54] is a portable motion capture system that collects human hand movements, enabling robots to complete tasks from simple picks to complex operations like Tea preparing. 

Learning-based approaches overcame these limitations. In perception, PoseCNN [107] enabled instance-level 6D pose estimation, while NOCS [108] advanced category-level estimation for generalization. Functional affordance learning progressed with AffordanceNet [109] identifying manipulable regions via supervised learning and Where2Act [110] using self-supervised simulation interactions. Imitation learning evolved with Neural Descriptor Fields (NDFs) [111] enhancing policy generalization, Diffusion Policy [3] leveraging diffusion models for multimodal actions, and RT2 [112] integrating foundation models to interpret complex instructions. 

Task-oriented manipulation expanded with these advances. Beyond basic grasping [3], robots handle cluttered environments with collision avoidance (e.g., CollisionNet [113], PerAct [114]), manipulate deformable and articulated objects [115]–[118], and perform bimanual coordination [49], dexterous hand manipulation [54], and whole-body control [119]. This evolution underscores gripper-based manipulation’s growing capability for diverse, complex tasks. **Dexterous hand manipulation.** Dexterous manipulation aims to enable robots to interact with the physical world in complex, precise ways akin to human hands, which is a core challenge in robotics for decades [120]. This field seeks to achieve human-like versatility and precision, addressing tasks that require intricate control and adaptability. 

Early work in dexterous manipulation concentrated on hardware design and theoretical foundations. Pioneering designs like the Utah/MIT Hand [121] and Shadow Hand [122] explored high degrees of freedom and biomimetic structures (e.g., tendon-driven mechanisms), while the BarrettHand [123] showcased underactuated designs for adaptive grasping. Concurrently, theoretical contributions [124] from Napier, classifying human grasp patterns, and Salisbury and Craig, analyzing multi-fingered force control and kinematics [125], established the groundwork for future research. Traditional model-based control methods struggled with high-dimensional state spaces and complex contact 

10 

dynamics, limiting their real-world effectiveness. Learningbased methods, including two-stage and end-to-end approaches, have since become the mainstream, using machine learning to tackle these challenges. 

Two-stage methods begin by generating grasping poses, followed by controlling the dexterous hand to achieve them. The key challenge lies in producing highquality poses from visual observations, tackled through optimization-based [126]–[128], regression-based [129], [130] or generation-based [131]–[140] strategies, often paired with motion planning. For instance, UGG [136] uses a diffusion model to unify pose and object geometry generation, while SpringGrasp [141] models uncertainty in partial observations to improve pose quality. Though these methods benefit from decoupled perception and control and simulation data, they remain sensitive to disturbances and calibration errors due to the absence of closed-loop feedback. 

End-to-end methods directly model grasping trajectories using reinforcement learning or imitation learning. Reinforcement learning trains policies in simulation for realworld transfer [142]–[144], with examples like DexVIP [145] and GRAFF [146] integrating visual affordance cues with reinforcement learning. DextrAH-G [147] and DextrAHRGB [148] achieve real-world generalization via largescale simulation, though sim-to-real gaps and sample efficiency pose challenges. Imitation learning, driven by human demonstrations [54], [146], [149], excels in complex tasks but struggles with generalization. Innovations like SparseDFF [150] and Neural Attention Field [151] enhance generalization using three-dimensional feature fields, while DexGraspVLA [152] employs a vision-languageaction framework: combining pre-trained vision-language models with diffusion-based action controllers. It achieves a 90.8% success rate across 1,287 unseen object, lighting, and background combinations in zero-shot settings. 

### _3.3.2 Bimanual Manipulation Task_ 

Bimanual manipulation refers to robotic tasks that require the coordinated use of two arms, enabling robots to perform complex operations such as cooperative transport, precise assembly, and the handling of flexible or deformable objects [155]. These bimanual tasks inherently present greater challenges compared to single-arm manipulation, including high-dimensional state-action spaces, potential for inter-arm and environmental collisions, and the necessity for effective bimanual coordination and dynamic role assignment. 

Early research in this area addressed these challenges by introducing inductive biases or structural decompositions to simplify learning and control. For instance, BUDS [156] decomposes bimanual manipulation tasks into stabilizer and executor functional roles, which not only reduces the complexity of the dual-arm action space but also enables effective collaboration between arms. This framework has demonstrated robust performance on tasks such as cutting vegetables, pulling zippers, and capping markers. In parallel, SIMPLe [157] utilizes Graph Gaussian Processes (GGP) to represent motion primitives for bimanual manipulation, ensuring trajectory stability and enabling the system to learn dual-arm coordination from single-arm demonstrations with the aid of kinematic feedback. 


Fig. 8: (1)The ALOHA series [49], [153] feature a low-cost, open-source hardware system that enables the learning of fine-grained, complex, and long-horizon mobile bimanual manipulation tasks, such as slot battery and cooking shrimp. This provides a robotic platform foundation for subsequent research. (2)RoboTwin 2.0 [154] enhances dual-arm manipulation by generating simulated data in simulator. It offers 50 dual-arm tasks, 731 diverse objects, and 5 embodiments for comprehensive research and development. 

With advances in large-scale data collection and imitation learning, end-to-end approaches have become increasingly prominent in bimanual manipulation research. The ALOHA series [49], [153], [158] exemplifies this trend by leveraging off-the-shelf hardware and custom 3D-printed components to enable efficient collection of diverse, largescale demonstration data for high-precision bimanual tasks. These datasets have facilitated the training of end-to-end neural networks with strong generalization capabilities. In particular, ACT [49] combines action chunking with a Conditional Variational Autoencoder (CVAE) framework, allowing robots to learn effective policies from as little as 10 minutes of demonstration data and achieving high success rates in challenging tasks such as battery insertion and cup lid opening. Building on this, Mobile ALOHA [153] introduces a mobile base and further simplifies the ACT pipeline, enabling efficient completion of mobile bimanual tasks. Furthermore, RDT-1B [50] proposes a foundation model for bimanual manipulation based on the diffusion DiT architecture, unifying action representations across heterogeneous multi-robot systems. This approach addresses data scarcity by enabling zero-shot generalization to new tasks and platforms. 

While these works have significantly advanced the field of bimanual manipulation, their focus has predominantly been on systems equipped with parallel-jaw grippers. In contrast, bimanual manipulation with dexterous robotic hands introduces additional challenges, particularly in terms of fine-grained coordination and high-dimensional control. Recently, several studies [140], [159], [160] have investigated RL-based methods to transfer human bimanual manipulation skills to robotic dexterous hands, thereby enabling more sophisticated manipulation capabilities. 

In summary, bimanual manipulation research has evolved from approaches reliant on strong task-specific pri- 

11 


Fig. 9: The BRS, introduced by Yunfan Jiang et al. [119], enables a humanoid robot to perform a wide range of complex household chores that require Whole-Body Manipulation Control, such as cleaning a toilet, taking out trash, and organizing shelves. 

ors and structural simplifications to data-driven, end-to-end frameworks that leverage large-scale demonstrations. These advances have significantly improved the robustness, generality, and versatility of bimanual robotic systems, enabling them to tackle an increasingly diverse array of complex manipulation tasks. In addition, ongoing research aimed at adapting these approaches to dexterous robotic hands is expanding the capabilities of bimanual manipulation, enabling robots to perform increasingly intricate and humanlike tasks. 

### _3.3.3 Whole-Body Manipulation Control_ 

Whole-body manipulation refers to the ability of humanoid robots to interact with and manipulate objects using their entire body, including dual arms [155], torso [161], wheeled or legged base [162], and/or other components [163]. 

In recent years, significant progress has been made in learning-based whole-body manipulation for humanoid robots, focusing on enhancing robots’ autonomy, adaptability, and interaction capabilities in complex environments. One of the trends involves leveraging large pre-trained models (such as LLMs, VLMs, and generative models) to enhance semantic understanding and generalization capabilities. For instance, TidyBot [164] utilizes the inductive capabilities of LLMs to learn personalized household tidying preferences from a small number of examples. MOO [165] maps object descriptions from language instructions to visual observations through VLMs, achieving zero-shot operational generalization to unseen object categories. HARMON [166] combines human motion generation priors with VLM editing to generate diverse and expressive humanoid movements from natural language. 

Visual demonstrations also guide learning manipulation skills. OKAMI [167] proposes an object-aware redirection method, enabling humanoid robots to imitate skills from a single human RGB-D video and adapt to different object layouts. iDP3 [168] achieves multi-scene task execution policies trained from single-scene teleoperation data through an improved 3D diffusion strategy. To achieve robust and dexterous whole-body control, OmniH2O [96] adopts a reinforcement learning Sim-to-Real approach, training whole- 

body control policies that coordinate movement and manipulation, and designs a universal kinematic interface compatible with both VR teleoperation and autonomous agents. The HumanPlus [6] system combines a Transformerbased low-level control policy with visual imitation strategies, enabling whole-body action demonstration and autonomous learning of complex skills for humanoid robots using only a monocular RGB camera. This system can learn whole-body manipulation and locomotion skills in the real world, such as putting on shoes, standing up, and walking. WB-VIMA [119] models the hierarchical structure of whole-body actions and the interdependencies between components within specific humanoid robot morphologies through autoregressive action denoising, predicting coordinated whole-body actions and effectively learning wholebody manipulation for completing challenging real-world household tasks. 

_3.3.4 Foundation Models in Humanoid Robot Manipulation_ Foundation Models (FMs) refer to large-scale models pretrained on internet-scale data, including Large Language Models (LLMs), Vision Models (VMs), and Vision-Language Models (VLMs). With their powerful capabilities in semantic understanding, world knowledge integration, logical reasoning, task planning, and cross-modal representation, these models can be directly deployed or fine-tuned for a wide range of downstream tasks. 

Foundation Models enable humanoid robots to perform operational tasks in complex, dynamic, and unstructured environments, typically involving complex environmental perception and modeling, abstract task understanding, and autonomous planning for long-sequence and multi-step tasks. Figure 10 illustrates two main technical paradigms for leveraging foundation models to drive humanoid robot operations. 

**Hierarchical Approach** utilizes pretrained language or vision-language foundation models as high-level task planning and reasoning engines to understand user instructions, parse scene information, and decompose complex tasks into sequences of sub-goals. These high-level outputs (typically actionable knowledge or image-language tokens) are then passed to low-level action policies (usually expert policies trained through imitation learning or reinforcement learning) to execute physical interaction actions. Transformer have become a common choice for such low-level policies due to their scalability. 

This hierarchical architecture leverages the powerful semantic and logical reasoning capabilities of foundation models while combining the efficiency of lower-level policies in specific action execution, enabling robots to excel in multi-task processing and cross-scenario generalization [169]–[173]. The advantages of this approach lie in its modularity and interpretability, but it also faces challenges related to information bottlenecks and semantic gaps between high and low levels. For example, Figure AI demonstrated Helix, a hierarchical VLA model for dexterous manipulation and collaboration between two humanoid robots [174], while NVIDIA developed GR00T N1, a general foundation model for humanoid robots [175]. The _π_ 0 model [176] integrates pretrained vision-language models with flow matching architecture to achieve universal control across various robotic 

12 


Fig. 10: Illustration of three common humanoid robot manipulation frameworks: Traditional, Hierarchical and End-to-End, which shows **input** _−→_ **action** data flows and structural differences. 

platforms, efficiently executing complex dexterous tasks such as laundry folding and object classification. **End-to-End Approach** directly incorporates robot operation data into the training or fine-tuning process of foundation models, constructing end-to-end Vision-Language-Action (VLA) models [4], [68], [177], [178]. These models directly learn the mapping from multimodal inputs (such as images and language instructions) to robot action outputs. Through pretraining or fine-tuning on large amounts of robot interaction data, VLA models can implicitly learn task planning, scene understanding, and action generation without explicit hierarchy. This end-to-end approach allows models to be holistically optimized for downstream deployment tasks, potentially achieving superior performance and faster response times, but typically requires substantial robot-specific data and offers relatively weaker model interpretability. For instance, Google DeepMind’s RT (Robotics Transformer) series [112], [177] represents typical VLA models for manipulation. 

### **3.4 Human-Robot Interaction** 

Human-Robot Interaction (HRI) focuses on enabling robots to understand and respond to human needs and emotions, fostering efficient cooperation, companionship, and personalized services from robots, with broad applications in home, healthcare, education, and entertainment [179]. To accurately interpret and adapt to diverse human behaviors, robots need to possess human-like abilities such as multimodal perception, natural language processing, and coordinated control. 

Research in human-robot interaction can be categorized into three primary dimensions: **Cognitive Collaboration** , **Physical Reliability** , and **Social Embeddedness** . These dimensions respectively focus on how robots perceive and understand human cognitive patterns, coordinate physical actions, and integrate effectively into human social contexts. 

Taking a robot navigating through a crowded environment as an example, Cognitive Collaboration involves the robot recognizing pedestrians’ potential urgency; Physical Reliability is demonstrated through the robot’s adjustments 


Fig. 11: Cognitive interaction analysis enables effective human–robot collaboration in assembly tasks [180]. 

in speed and trajectory to avoid collisions; and Social Embeddedness is exemplified by the robot actively negotiating passage rights using linguistic cues or body language to establish temporary social protocols. Such comprehensive capabilities enable robots to integrate seamlessly into daily human activities, enhancing interaction naturalness and efficiency. The subsequent sections will elaborate on the theoretical foundations, current research advancements, major research directions, and representative literature associated with each dimension. 

### _3.4.1_ **_Cognitive Collaboration:_** _Understanding and Aligning with Human Cognition_ 

Cognitive Collaboration in Human-Robot Interaction refers to the bidirectional cognitive alignment between robots and humans, achieving natural and intuitive communication and cooperation. This collaboration emphasizes not only the robot’s passive response to human behavior but also deep cognitive understanding and dynamic adaptation, forming a pattern similar to efficient collaboration among humans. Its core objective is to enable robots to understand not only explicit instructions from humans, such as voice commands and sign language instructions [181], but also implicit intentions (such as emotions and context), dynamically adjusting their behavior to match human cognitive patterns 

13 

and expectations. The realization of this capability is crucial for improving robots’ adaptability in complex scenarios and natural interaction experiences. 

Research shows that achieving cognitive collaboration depends on complex cognitive architectures and multimodal information processing capabilities. For example, Lemaignan et al. [182] explored key skills required for robot cognition in social human-robot interaction, including geometric reasoning, contextual assessment, and multimodal dialogue. Robots need to understand human intentions and collaborate with humans to complete joint tasks through these skills [180]. 

Additionally, multimodal intention learning has been identified as a key factor for achieving cognitive collaboration [183]. For example, integrating facial expressions and body movements to interpret the emotional tone and underlying intentions of spoken instructions can greatly reduce misunderstandings and enhance the naturalness of human-robot interactions [184]. 

Furthermore, cognitive collaboration requires robots to have a deep semantic understanding of the environment and interaction context. Laplaza et al.’s research demonstrates how to infer interaction intentions through contextual semantic analysis of human actions [185]. They proposed a model based on dynamic semantic analysis that can parse the potential goals of human actions in realtime and make predictions combined with environmental information, enabling robots to more accurately collaborate in completing tasks. 

In interaction tasks without direct human participation, cognitive collaboration also plays an important role. For example, in home service robot scenarios, robots can solve goal-oriented navigation tasks through semantic understanding of the environment. This task requires robots to locate specific target objects (such as cups, sofas, or televisions) or designated areas (such as bedrooms and bathrooms) in unknown environments. Works like L3mvn [186], Sg-Nav [187], Trihelper [188], CogNav [189] and UniGoal [190] have improved robot performance in goal-oriented navigation tasks by leveraging large language models (LLMs) to simulate various human cognitive states, such as broad search and contextual search. 

In summary, the advancement of cognitive collaboration in human-robot interaction relies on interdisciplinary efforts that encompass cognitive science, semantic understanding, and the development of large multimodal models involving language, vision, and audio perception. As cognitive collaboration capabilities continue to improve, robots will become increasingly adept at supporting various tasks in real-world scenarios. 

### _3.4.2_ **_Physical Reliability:_** _Coordination and Safety of Physical Actions_ 

Physical reliability in human-robot interaction refers to the effective coordination of force, timing, and distance between humans and robots to ensure safe, efficient, and humancompatible task execution. Its core objective is to enable robots to dynamically respond to real-time changes in human actions, including adjust movement strategies, avoid physical conflicts, and ensure human safety during interaction. To achieve this, research focuses on two main di- 


Fig. 12: Physical Reliability are ensured through perception and planning [191]. 

rections: real-time control in physical interaction and largescale generative dataset construction based on simulation platforms. 

Ensuring physical reliability in human-robot interaction relies on advanced motion planning and control strategies that address both coordination and safety between humans and robots [192]. Sampling-based planners such as Probabilistic Road Map (PRM) [193] and Rapidly-exploring Random Tree (RRT) [194], as well as their extensions, have been widely used to generate collision-free and human-aware trajectories in shared workspaces [195]–[199]. Optimizationbased planners including CHOMP [200], STOMP [201], ITOMP [202], TrajOpt [203], [204] and GPMP [205] further improve trajectory quality by minimizing costs related to feasibility and smoothness in dynamic scenarios. These methods are well-suited for application in human-robot collaborative settings to ensure physical reliability [206], [207]. 

On the control side, impedance control and admittance control provide compliant and safe responses to physical contacts, while adaptive and hybrid controllers further enhance robustness against disturbances and uncertainties [208]–[211]. These approaches ensure that robots act reliably and predictably, reducing the risk of injury and discomfort for human collaborators. 

However, as robots are increasingly deployed in diverse and unstructured environments, achieving safe and robust physical collaboration requires more than just traditional control strategies. The integration of perception, intention prediction, and real-time adaptation has become essential to enable robots to respond to dynamic changes and complex human behaviors [212], [213]. Building upon these advances, recent research has explored imitation learning and reinforcement learning methods, enabling robots to acquire adaptive motion policies directly from data and experience [214]–[216]. However, the effectiveness of these learning-based approaches depends heavily on the availability of high-quality interaction data. As a result, largescale generative datasets produced through physical simulation have become a vital resource for enhancing the reliability and safety of robotic actions. For instance, Handover- 

14 

Sim [217] provides a simulation and benchmarking platform for human-robot object handover, leveraging physics engines and trajectory optimization to ensure collisionfree and standardized safety evaluation. Building on this, GenH2R [218] introduces a simulation environment with extensive 3D models and dexterous grasp generation, enabling the training of generalized handover strategies through imitation learning. Further, MobileH2R [191] integrates expert demonstrations generated by CHOMP [200] to tackle the challenges of safe and efficient object transfer for mobile robots in dynamic scenarios. 

Despite promising progress in current research, ensuring physical reliability in HRI still faces challenges such as high computational cost and limited robustness in complex scenarios. Future exploration is needed to develop more efficient algorithms and enhance adaptability, enabling reliable human-robot interaction in diverse and dynamic environments. 

### _3.4.3_ **_Social Embeddedness:_** _Integration with Social Rules and Cultural Norms_ 

Social embeddedness in human-robot interaction refers to a robot’s ability to recognize and adapt to social norms, cultural expectations, and group dynamics, enabling seamless integration into human environments. This extends beyond task completion to include behaviors such as negotiation, etiquette, and emotional expression. As illustrated in Fig. 13, the robot is shown engaging in negotiation with a human partner. To facilitate the seamless integration of robots into social scenarios, recent research has explored a range of strategies that address both social space understanding and behavior understanding. These two complementary aspects are fundamental for achieving effective social embeddedness in human-robot interaction. 

On one hand, social space understanding enables robots to interpret and adapt to the spatial dynamics of human groups. Through the application of spatial understanding in social scenarios, robots can better interpret collaborative or defensive behaviors through concepts such as peripersonal space [219], [220]. A typical application is enabling robots to navigate and interact more effectively within social environments, thereby providing individuals with visual impairments more appropriate and natural assistance [221]– [223]. 

On the other hand, behavior understanding focuses on decoding the intricacies of human communication from both linguistic and non-linguistic perspectives. Linguistic research explores aspects such as dialogue modeling, conversational structure, and discourse analysis [224]–[228], while non-linguistic studies focus on the interpretation of gestures, gaze, and emotional expressions [229], [230]. To capture these diverse social signals, a range of methods have been proposed for modeling and recognizing nonverbal behaviors, spanning from individual gesture analysis to multi-party, real-world interactions [231]–[236]. 

Despite these advances, robust social embeddedness remains challenging. Robots must accurately balance task efficiency with social appropriateness, requiring improvements in multimodal perception, long-term adaptation, and the integration of social knowledge into decision-making. 


Fig. 13: A social navigation scenario where the robot communicates its intent to a human via a wearable haptic interface [237]. 

Future research should also address lifelong learning, crosscultural adaptation, and the ethical implications of socially embedded robots, paving the way toward IR-L4 autonomy. 

## **4 GENERAL PHYSICAL SIMULATORS** 

As the traditional robots evolve toward embodied intelligence, their application demands are gradually shifting from structured industrial settings to open and dynamic human living environments. However, algorithmic research on intelligent robots continues to face significant data bottlenecks, which severely limit the generalization capability and applicability of related algorithms. 

Specifically, current data collection for intelligent robots still faces the following challenges: 1) **_Cost and Safety problem_** : Data collection strategies based on teleoperation [55], [153] or universal manipulation interfaces (UMI) [238] impose hardware requirements and demand a certain level of operator proficiency, bringing financial problems to the data collection process. Moreover, the physical experiments also raise the safety problem related to hazardous and dangerous scenarios or robotic actions. 2) **_Control and Repeatability problem_** : The data collection process is influenced by numerous factors such as lighting, background, and sensor noise, which affect data quality. To control all these factors, the collection scenario must be carefully designed. Additionally, because the scene cannot be fully controlled, it becomes challenging to replicate experiments with identical settings for verification. 

To address the aforementioned bottlenecks, simulationto-reality (Sim2Real) transfer has emerged as a key approach to overcome data limitations. This paradigm constructs high-fidelity virtual environments to generate multimodal synthetic data, offering several key advantages: 1) **_Significantly improved data generation efficiency_** : The use of GPU-accelerated physics engines and distributed rendering in simulators enables the rapid generation of large volumes of simulated data, which makes the data collection process cost-effective and safe; 2) **_Automated annotation and controllable semantic labeling_** : Simulators can directly output pixel-level ground truth, including semantic segmentation maps, depth maps, and 6D object poses, allowing precise control of the simulated environments. Furthermore, simulators also provide an efficient, safe, and reproducible testing ground for debugging, validating, and optimizing robot 

15 


Fig. 14: Mainstream Simulators for robotic research. 

perception, control, and planning algorithms, enhancing their robustness and reliability during actual deployment. 

This chapter focuses on mainstream simulators in contemporary robotics research. We first introduce the widely adopted simulation platforms, followed by an introduction of their diverse capabilities, encompassing physical simulation properties, rendering capabilities, and sensor/joint component support abilities. Finally, we summarize the current development of robotic simulators and discuss prospective research direction. 

### **4.1 Mainstream Simulators** 

**Webots** [239], introduced by Cyberbotics Ltd. in 1998, provides an integrated framework for robot modeling, programming, and simulation, and has been widely adopted in education, industry, and academia. It was open-sourced in 2018, significantly enhancing its accessibility for research and education worldwide. Webots offers a rich set of prebuilt robot models, supports various sensor modalities, is cross-platform, and provides multi-language APIs, making it a versatile and user-friendly tool. However, it lacks support for deformable bodies and fluid dynamics, and shows limitations in advanced physics and large-scale learning tasks. 

**Gazebo** [15], developed in 2002 by Andrew Howard and Nate Koenig at the University of Southern California, is a widely adopted open-source simulator known for its extensibility and integration with robotic middleware. In addition to supporting a broad range of sensors and robot models, Gazebo features a modular plugin system that enables users to customize simulation components, including models, controllers and sensors. The system also allows users to interface with various physics and rendering engines. However, it shares similar limitations with Webots in terms of advanced physical interaction, lacking support for suction-based grasping, deformable objects, and fluid dynamics. Both Webots and Gazebo are tightly integrated with the Robot Operating System (ROS), enabling seamless testing and validation of robotic algorithms within the ROS ecosystem. Nonetheless, they do not offer native support for parallel execution or reinforcement learning workflows. 

**MuJoCo** (Multi-Joint dynamics with Contact) [16] is a physics engine developed in 2012 by Professor Emo Todorov’s group at the University of Washington, and was 

later acquired by Google DeepMind in 2021. Designed specifically for simulating contact-rich dynamics in articulated systems, MuJoCo offers high-precision physical computation, an optimized generalized-coordinate formulation, and native support for biomechanical modeling. MuJoCo formulates contact constraints as convex optimization problems. This approach enables accurate simulation of complex interactions. These interactions include soft contacts, frictional behavior and tendon-actuated motion. At the same time, it mitigates common limitations of traditional engines, such as interpenetration and instability. It maintains both numerical accuracy and computational efficiency even under large simulation time steps. The engine supports a lightweight XML-based modeling format (MJCF/URDF) and provides multi-language APIs (Python, C++), enabling rapid model construction and iteration. These features have led to its widespread adoption in robotics and reinforcement learning research. Overall, MuJoCo excels in contact dynamics and RL applications with ROS integration support, but is limited in rendering capabilities due to its OpenGL backend and lacks support for fluid, discrete element (DEM), or LiDAR simulation. 

With the rapid advancement of robotics and artificial intelligence, the demand for efficient simulation tools has increased. In response, Erwin Coumans, the original developer of the Bullet physics engine, introduced **PyBullet** in 2017 [240]. PyBullet wraps the powerful capabilities of Bullet in a Python interface, aiming to provide researchers and developers with a lightweight and easy-to-integrate simulation platform. Although PyBullet falls slightly short of some mainstream simulators in terms of simulation fidelity and feature richness, it has gained widespread adoption in academia due to its open-source nature, lightweight design, user-friendly Python interface, and ease of use. Over time, it has fostered a large and active user community. 

**CoppeliaSim** [241], formerly known as V-REP (Virtual Robot Experimentation Platform), was initially released around 2010 by Toshiba Corporation as a general-purpose robot simulation software aimed at developers, researchers, and educators. Since 2019, it has been further developed and maintained by the Swiss company Coppelia Robotics. The core strength of CoppeliaSim lies in its distributed control architecture, which allows Python and Lua scripts or C/C++ plugins to function as individual synchronous controllers. Additional asynchronous controllers can be executed via 

16 

various middleware solutions (e.g., ROS, remote APIs) and support integration with C/C++, Python, Java, and MATLAB across separate processes, threads, or even machines. The educational edition of CoppeliaSim is open-source and freely available, making it widely adopted in academic and educational settings. 

With the growing convergence of robotics, reinforcement learning, and photorealistic simulation, the demand for scalable, GPU-accelerated simulation platforms has surged. The NVIDIA Isaac series addresses this need by establishing a closed-loop technological ecosystem for robotics development and embodied AI research. Its evolution reflects a shift from isolated acceleration tools to a comprehensive, fullstack simulation infrastructure. **Isaac Gym** [242], introduced in 2021, pioneered large-scale GPU-accelerated physics simulation by enabling the parallel training of thousands of environments simultaneously. Built upon NVIDIA’s PhysX engine, it significantly improves sample efficiency in tasks such as locomotion control and policy learning for legged robots. However, Isaac Gym is limited in rendering fidelity due to its lack of ray tracing support, and does not offer fluid or LiDAR simulation capabilities. 

**Isaac Sim** [243] is subsequently introduced by NVIDIA with integration of the Omniverse platform [244], a fullfeatured digital twin simulator built on Omniverse. It incorporates the PhysX 5 physics engine and RTX-based real-time ray tracing, enabling high-fidelity LiDAR simulation with millimeter-level precision. By adopting the USD (Universal Scene Description) [245] standard, Isaac Sim supports physically accurate simulation of multimodal sensors, including RGB-D cameras and IMUs. The 2025 release of Isaac Sim 5.0 further improved rigid-body momentum conservation, added joint visualization tools, and introduced simulation data analytics modules, achieving robotic arm grasping precision within 0.1 mm. 

**Isaac Lab** [246] is a modular reinforcement learning framework built on top of Isaac Sim, designed to streamline and optimize the robot learning pipeline. It employs a tiled rendering technique to efficiently process multicamera inputs, improving training throughput by approximately 1.2×. Isaac Lab supports both imitation learning and reinforcement learning paradigms, enabling rapid policy construction from demonstration datasets in HDF5 format. Isaac Gym’s parallel computing capabilities are now deeply integrated into Isaac Sim’s underlying architecture. Built upon Isaac Sim, Isaac Lab employs modular design to abstract simulation environments into configurable task units. This evolving software stack is advancing toward support for heterogeneous physics engines (including both rigid and soft-body dynamics), sim-to-real transfer, and generative AI-driven scene synthesis (e.g., the Cosmos world model), thereby providing a unified infrastructure for embodied intelligence research—from low-level physics to high-level behavior learning. However, it inherits the high hardware requirements of Isaac Sim, which may limit accessibility for resource-constrained users. Both Isaac Sim and Isaac Lab have released early developer preview versions and are expected to be gradually open-sourced. 

**SAPIEN** (SimulAted Part-based Interactive ENvironment), introduced in 2020 by researchers from the University of California, San Diego and collaborating institu- 

tions [247], is a simulation platform designed for physically realistic modeling of complex, part-level interactive objects, extending beyond traditional rigid-body dynamics. To support research in articulated object manipulation, the authors released PartNet-Mobility [247], a comprehensive dataset featuring motion-annotated, articulated 3D objects. Building on the SAPIEN engine, the research team later introduced the ManiSkill [248] and ManiSkill3 [249] benchmarks, which provide diverse manipulation tasks, highquality demonstrations, and efficient, parallelized data collection pipelines. This ecosystem has become a widely used benchmark suite for evaluating manipulation policies and embodied intelligence algorithms in realistic physics-based environments. SAPIEN offers interactive visualization, supports RGB and IMU sensors, and is tightly coupled with the ManiSkill benchmark. However, it lacks support for softbody and fluid dynamics, ray tracing, LiDAR, GPS, and ROS integration, which limits its applicability in broader robotic simulation scenarios. 

**Genesis** [250], released in 2024, is a general-purpose physical simulation platform developed by a global consortium of researchers. Its core objective is to unify a wide array of physics solvers—including rigid body dynamics, Material Point Method (MPM), Smoothed Particle Hydrodynamics (SPH), Finite Element Method (FEM), Position-Based Dynamics (PBD), and stable fluid solvers—within a highfidelity framework capable of capturing complex physical phenomena with maximal realism. A key innovation in Genesis is its generative data engine, which enables users to specify simulation scenarios and generate multimodal datasets from natural language prompts. Built with differentiability as a fundamental design principle, Genesis is well-suited for applications in embodied intelligence, physical reasoning, and differentiable simulation. According to public benchmarks, Genesis demonstrates a 2.70× to 11.79× throughput advantage over Isaac Gym across batch sizes ranging from 512 to 32,768 environments. The platform is currently undergoing staged open-source release. Despite its strengths, Genesis does not yet support LiDAR or GPS simulation, nor does it provide ROS integration. 

In addition, NVIDIA **Newton** [251] is an open-source physics engine jointly developed by NVIDIA, Google DeepMind, and Disney Research in 2025. Targeting at highfidelity simulation and robot learning, Newton provides a full-stack framework spanning from basic physical modeling to complex multiphysics interactions. Built on top of the NVIDIA Warp framework, it achieves over 70 _×_ simulation speedup via GPU acceleration and supports rigid/softbody dynamics, contact and friction modeling, as well as custom solver integration. Newton is designed to be deeply compatible with existing robot learning platforms such as MuJoCo Playground and Isaac Lab, allowing seamless reuse of existing robot models and training pipelines. With its differentiable physics engine, Newton enables backpropagation of gradients through simulation, offering a solid mathematical foundation for learning-based control optimization. Additionally, its OpenUSD-based scene construction capability aligns physical laws with virtual environments at a fine-grained level. Although still in its early development stage, the Newton ecosystem is rapidly evolving and aims to bridge the sim-to-real gap in domains such as industrial 

17 

manipulation and humanoid motion planning. 

### _4.2.3 Deformable objects_ 

### **4.2 Physical Properties of Simulators** 

Intelligent robots are required to perform human-like behaviors such as grasping, walking, and collaboration in complex and dynamic environments. In this context, the physical modeling capabilities of the simulator directly determine the realism of the generated data and the effectiveness of policy transfer. High-fidelity physical property simulation not only enhances the realism of environmental interactions (e.g., soft body deformation, center-of-mass shifts caused by fluid dynamics), but also improves algorithm generalization by introducing stochastic perturbations that prevent policy overfitting to the simulated environment. This, in turn, broadens the applicability of humanoid robot algorithms across a wider range of scenarios. This section provides a comparative analysis of the simulators discussed above, focusing on their capabilities in simulating various physical properties. Following the categorization in [21], this subsection selects physical attributes that are especially important for humanoid robots and world model, and compares how different simulators support them. Table 2 summarizes the support of different simulators for various types of physical simulation. 

### _4.2.1 Suction_ 

In robotic simulation, suction modeling primarily refers to the non-rigid attachment behavior at contact interfaces, such as simulating vacuum suction for object grasping. This function is widely used in industrial automation and warehouse picking. 

Currently, mainstream robotic simulation platforms vary in implementation of suction effects. MuJoCo relies on userdefined logic to simulate suction by detecting contact and applying external forces or creating virtual links, offering limited accuracy and control. Gazebo implements suction via plugins that dynamically create joints based on contact, enabling more flexible control of mechanical behavior. In contrast, Webots, CoppeliaSim and Isaac Sim provide native module support for suction, offering greater ease of use. 

### _4.2.2 Random external forces_ 

Random external forces aim to simulate uncertainties in the environment, such as object collisions, wind forces, and so on. Applying random external forces to humanoid robots can better enhance their balance capabilities and resistance to disturbances, thus preventing overfitting of training strategies in stable environments. 

Most mainstream robot simulation platforms support the simulation of random external forces, though their implementations vary. MuJoCo, PyBullet, SAPIEN, CoppeliaSim, and Isaac Gym primarily rely on user-defined methods through scripting or APIs to apply such perturbations. Notably, Isaac Gym offers parallel control interfaces, enabling efficient addition of random disturbances in large-scale scenarios. In contrast,Webots, Gazebo, Isaac Sim, and Isaac Lab provide well-developed interfaces that allow direct application of random forces or disturbances via random velocities. 

Deformable objects refer to materials that undergo shape changes under external forces and are widely used to simulate the physical behavior of flexible materials such as cloth, ropes, and soft robots. Support for deformable object simulation across mainstream robotic simulators ranges from basic to high fidelity. Platforms like MuJoCo and PyBullet provide foundational soft body capabilities for simple deformable entities such as cloth or elastic materials. In contrast, Isaac Gym, Isaac Sim, and Isaac Lab offer more advanced solutions. They leverage GPU acceleration or PhysXbased [252] finite element methods for finer control and higher realism. Genesis further extends these capabilities by integrating state-of-the-art physics solvers, enabling detailed and high-precision simulation of complex deformable materials. 

### _4.2.4 Soft-body contacts_ 

Unlike deformable objects, Soft-body contacts refer to the simulation of interactions between soft materials—such as cloth, rubber and other objects. These simulations involve complex deformation responses and force transmission processes, and are widely used in the study of manipulation, collision, and contact mechanics of deformable materials. 

Current mainstream simulators support soft-body contact simulation at two main levels: basic support and high-precision modeling. Webots, Gazebo, MuJoCo, CoppeliaSim, and PyBullet offer basic simulation capabilities through soft-contact parameters, simplified contact models, or articulated body structures, which are suitable for general-purpose applications. In contrast, Isaac Gym, Isaac Sim, Isaac Lab, and Genesis provide more advanced and accurate simulations using GPU acceleration or methods such as finite element modeling (FEM), making them better suited for complex physical interaction scenarios. 

### _4.2.5 Fluid mechanism_ 

Fluid mechanism simulation refers to the computational modeling of the motion and interaction of fluids such as liquids and gases. This type of simulation is widely used in engineering and robotics, enabling researchers and engineers to predict and analyze fluid behavior under various conditions, optimize system designs, improve efficiency, and reduce costs. 

Mainstream simulators differ significantly in their support for fluid mechanisms. Webots and Gazebo offer basic fluid simulation capabilities, suitable for modeling simple interactions such as buoyancy and drag, though with limited accuracy. Isaac Sim, built on Omniverse and PhysX, supports more complex fluid behaviors through particle-based methods. Genesis integrates advanced physical solvers, offering native support for high-fidelity fluid simulation and ranking among the most comprehensive and accurate platforms currently available. Other mainstream simulators currently lack native support for fluid mechanisms, though limited community-driven extensions exist—for example, in Isaac Lab. 

### _4.2.6 DEM(Discrete Element Method) simulation_ 

The Discrete Element Method (DEM) is a numerical simulation technique that models objects as assemblies of rigid par- 

18 

|Simulator|Physics Engine|Suction|Random<br>external forces|Deformable<br>objects|Soft-body<br>contacts|Fluid<br>mechanism|DEM<br>simulation|Differentiable<br>physics|
|---|---|---|---|---|---|---|---|---|
|Webots|ODE(default)|✓|✓|✗|✓|✓|✗|✗|
|Gazebo|DART(default)|✓|✓|✗|✓|✓|✓|✗|
|MuJoCo|MuJoCo|✓|✓|✓|✓|✗|✗|✓|
|CoppeliaSim|Bullet, ODE, Vortex, Newton|✓|✓|✗|✓|✗|✗|✗|
|PyBullet|Bullet|✗|✓|✓|✓|✗|✗|✓|
|Isaac Gym|PhysX, FleX(GPU)|✗|✓|✓|✓|✗|✗|✗|
|Isaac Sim|PhysX(GPU)|✓|✓|✓|✓|✓|✗|✗|
|Isaac Lab|PhysX(GPU)|✗|✓|✓|✓|✗|✗|✗|
|SAPIEN|PhysX|✗|✓|✗|✓|✗|✗|✗|
|Genesis|Custom-designed|✗|✓|✓|✓|✓|✗|✓|


TABLE 2: Comparison of physical simulation across different simulators. ✓: support, ✗: lack of support. 

|Simulator<br>|RenderingEngine<br>|RayTracing|Physically-Based Rendering|Scalable Parallel Rendering|
|---|---|---|---|---|
|Webots<br>|WREN (OpenGL-based)<br>|✗|✓|✗|
|Gazebo|Ogre (OpenGL-based)<br>|✗|✓|✗|
|Mujoco|OpenGL-based|✗|✗|✗|
|CoppeliaSim|OpenGL-based|✗|✗|✗|
|PyBullet|OpenGL-based (GPU)<br>TinyRender (CPU)|✗|✗|✗|
|Isaac Gym|Vulkan-based|✗|✗|✓|
|Isaac Sim|Omniverse RTX Renderer|✓|✓|✓|
|Isaac Lab|Omniverse RTX Renderer<br>|✓|✓|✓|
|SAPIEN|SapienRenderer<br>(Vulkan-based)|✓|✓|✓|
|Genesis|PyRender+LuisaRender|✓|✓|✓|


TABLE 3: Rendering Features Across Various Simulators. ✓: support, ✗: lack of support. 

ticles, simulating interactions such as contact, collision, and friction between particles. It is widely used to simulate the physical behavior of granular materials and powders. DEM accurately captures the microscopic mechanical properties of particle systems but involves high computational cost, often mitigated by parallel computing or GPU acceleration. In robotic simulations, DEM can be employed to model interactions between robots and granular materials, such as grasping and manipulation. 

However, current mainstream simulators do not natively support DEM. Although platforms such as MuJoCo and the Isaac series can simulate granular materials, their contact models are not specifically optimized for the microscopic interactions of particulate matter. Notably, Gazebo supports functionality extension through plugins, and NASA’s OceanWATERS project [253] integrates DEM simulation with Gazebo to enable indirect simulation of granular material behavior. This approach primarily supports force feedback in tasks like excavation rather than real-time particlelevel simulation. 

### _4.2.7 Differentiable physics_ 

In the field of simulation, differentiable physics refers to a simulator’s ability to compute gradients of physical states with respect to input parameters, such as control signals, object poses, and physical properties. This capability enables end-to-end optimization and learning, allowing seamless integration with machine learning models, particularly reinforcement learning and optimization algorithms, to achieve efficient self-learning and task performance improvement. 

Several simulation platforms have recently made rapid advancements in supporting differentiable physics. The XLA branch of MuJoCo (MuJoCo XLA) enables differentiable simulation via JAX, allowing gradient computation 

and optimization tasks. PyBullet offers a differentiable interface through its subproject, the Tiny Differentiable Simulator, which is suitable for gradient-based learning and optimization. Genesis incorporates differentiability from the ground up, having already implemented differentiable physics in its MPM solver and planning to extend it to rigid body and articulated system solvers. Overall, these platforms are increasingly integrating high-fidelity physical modeling with automatic differentiation, accelerating the deployment of differentiable simulation in embodied intelligence and robot learning. 

### **4.3 Rendering Capabilities** 

Simulation rendering capabilities are pivotal in modern robotics research and development. They not only provide researchers with an efficient virtual experimentation environment but also ensure that the appearance and behavior of the robot are more realistic and accurate in predictions. High-fidelity rendering plays a crucial role in diminishing the simulation-to-reality (sim-to-real) gap. This is essential for various stages of robot development, including design, validation, and optimization, and it significantly bolsters the robustness and reliability of perception, control, and Simultaneous Localization and Mapping (SLAM) algorithms during their transition to real-world deployment. 

This subsection presents a comparative analysis of the rendering capabilities of the aforementioned simulators, focusing on four key technological aspects: the underlying rendering engines, support for ray tracing, implementation of Physically Based Rendering (PBR), and capabilities for parallel rendering. The results are shown in Table 3. 

19 

|Simulator|Sensor<br>IMU/Force contact/<br>RGB Camera|LiDAR|GPS|Joint type<br>Floating/Fixed/Hinge<br>Spherical/Prismatic|Helical|
|---|---|---|---|---|---|
|Webots|✓|✓|✓|✓|✗|
|Gazebo|✓|✓|✓|✓|✓|
|Mujoco|✓|✓|✗|✓|✗|
|CoppeliaSim|✓|✓|✓|✓|✓|
|PyBullet|✓|✓|✗|✓|✗|
|Isaac Gym|✓|✗|✓|✓|✗|
|<br>Isaac Sim|✓|✓|✓|✓|✗|
|Isaac Lab|✓|✓|✓|✓|✗|
|SAPIEN|✓|✗|✗|✓|✗|
|Genesis|✓|✓|✓|✓|✗|


TABLE 4: Sensor and Joint Component Support Across Various Simulators. ✓: support, ✗: lack of support. 

### _4.3.1 Rendering Engine_ 

A rendering engine is the core software used to create 2D images from 3D scene descriptions. Its tasks include processing geometric data, applying textures, calculating illumination from various light sources, and executing shading models to determine the final appearance of surfaces. 

OpenGL [254], a long-standing cross-platform graphics API, is widely adopted. Webots employs its proprietary Webots Rendering Engine (WREN), architected upon OpenGL 3.3. WREN is specifically optimized for GPU hardware and tailored to the Webots simulation platform, incorporating features such as anti-aliasing, resolution enhancement, ambient occlusion, and a full PBR pipeline. MuJoCo features an integrated renderer implemented using fixedfunction OpenGL, prioritizing efficiency by preloading GPU resources but limited to basic visual effects. CoppeliaSim leverages a built-in OpenGL-based rendering engine for real-time rasterization. PyBullet offers basic rendering via OpenGL on the GPU and includes TinyRender, a CPU-based software renderer, for headless or non-GPU scenarios. 

As OpenGL’s capabilities have gradually fallen short of real-world demands, subsequent rendering engines have adopted more versatile graphics APIs to better leverage GPU resources and achieve higher rendering performance. Isaac Gym utilizes Vulkan [255] for its lightweight GUI visualization. This Vulkan-powered viewer does not aim for high-fidelity rendering but provides efficient, real-time visual feedback for debugging and simulation workflows. The subsequent NVIDIA Isaac suite presents a more advanced approach. Isaac Sim and Isaac Lab are deeply integrated with the NVIDIA Omniverse ecosystem. They employ the Omniverse RTX renderer with the Hydra rendering delegate [256], leveraging NVIDIA’s RTX technology for high-fidelity graphics. SAPIEN employs a custom, high-performance rendering engine built upon the Vulkan graphics API, known as SapienRenderer. Genesis utilizes a native rendering pipeline, integrating cutting-edge frameworks such as PyRender [257] and LuisaRender [258]. 

### _4.3.2 Ray Tracing_ 

Ray tracing is a rendering technique that simulates the physical behavior of light by tracing paths of light rays as they interact with surfaces in a 3D scene. Its primary advantage over traditional rasterization in robotics is the ability to produce highly accurate shadows, reflections, refractions, global illumination, and, critically, more physically realis- 

tic simulation of sensors like LiDAR and depth cameras. Rasterization often struggles with non-linear optical sensors and complex light interactions. 

Among the reviewed simulators, Webots, MuJoCo, and PyBullet do not offer native real-time ray tracing, relying on rasterization for their primary visual output. CoppeliaSim integrates the POV-Ray tracer, enabling high-quality static image generation with ray tracing, but it does not support real-time ray tracing for dynamic simulations. Rendering in Isaac Gym is also relatively basic, and does not support either ray tracing or the more sophisticated synthetic data sensors provided in Omniverse. In contrast, simulators built for high-fidelity visual output increasingly incorporate ray tracing. Isaac Sim and Isaac Lab, through the Omniverse RTX renderer, provide robust real-time ray tracing, enabling effects like global illumination, reflections, and refractions. SAPIEN also offers significant ray tracing support; its SapienRenderer (Vulkan-based) supports both rasterization and ray tracing pipelines, selectable via shader packs. Gazebo, while primarily rasterization-based, shows a path towards ray tracing through experimental NVIDIA OptiX [259] support in its gz-rendering library. Genesis, aiming for photorealism, utilizes a state-of-the-art high-performance renderer “LuisaRender”. 

### _4.3.3 Physically-based Rendering_ 

PBR is an approach that models how light interacts with materials based on their physical properties, such as roughness and metallicity. This results in more realistic and consistent visuals across different lighting conditions, leading to better material definition and improved visual fidelity, which is crucial for training vision-based robotic learning methods. 

Webots’ WREN engine implements a PBR pipeline, incorporating advanced lighting models and non-color textures for realism comparable to modern game engines. Modern Gazebo, through Ignition Rendering, also supports PBR, and its Ogre backend has PBR capabilities. In contrast, MuJoCo, CoppeliaSim and PyBullet, with their focus on basic visual effects and rudimentary rendering respectively, lack PBR support. Isaac Gym, using a basic Vulkan-based pipeline, also does not implement PBR. 

High-fidelity simulators embrace PBR. Isaac Sim and Isaac Lab, built on NVIDIA Omniverse, inherently support PBR through the Omniverse RTX renderer and leverage the Material Definition Language (MDL) for defining realistic, physically-based materials. SAPIEN and Genesis also sup- 

20 


Fig. 15: Main joint types in simulators. [260] 

port PBR. Their advanced rendering capabilities, including ray tracing and accurate material property representation, are integral to PBR systems. 

### _4.3.4 Parallel Rendering_ 

Parallel rendering in robotics simulation encompasses rendering multiple independent simulation environments simultaneously for large-scale RL or data collection. Its utility lies in significantly speeding up RL agent training, enabling efficient generation of large synthetic datasets. 

Simulators like Isaac Gym, Isaac Sim/Lab, SAPIEN (especially with ManiSkill), and Genesis are designed with strong parallel rendering capabilities as a core architectural feature. Isaac Gym can simulate and render thousands of environments in parallel on a single GPU, including camera sensors. Isaac Sim and Isaac Lab extend this to multiGPU training, where each process can run on a dedicated GPU with its own Isaac Sim instance, and Isaac Sim itself supports multi-GPU rendering for complex scenes or multiple cameras. SAPIEN, particularly with ManiSkill3, offers a GPU-parallelized visual data collection system achieving very high FPS (e.g., 30,000+ FPS with rendering on a highend GPU) and supports heterogeneous simulation where each parallel environment can differ. 

Older or more general-purpose simulators like Webots, Gazebo, MuJoCo, CoppeliaSim, and PyBullet may support running multiple instances or have some form of physics parallelization but generally lack the integrated, highthroughput parallel visual rendering pipelines of the specialized platforms. Webots allows multiple instances (e.g., via Docker) and disabling rendering for speed, but parallel visual output is not a primary strength. Gazebo parallelizes its physics engine but is not designed for massive parallel visual output for RL. MuJoCo can run parallel simulation threads with basic or offscreen rendering per instance. CoppeliaSim allows multiple scenes but renders only the active one, not suited for parallel data collection. PyBullet supports multiple physics servers and headless image capture via a CPU renderer, with some multi-threading in Bullet physics, but lacks high-throughput GPU parallel visual rendering. 

### **4.4 Sensor and Joint Component Types** 

Sensors are essential components in robot perception, providing the foundation for motion control and environmental understanding by capturing multimodal information such 

as vision, force, and inertia. In simulation platforms, realistic and reliable sensor models offer an efficient, safe, and repeatable testing basis for debugging, validating, and collecting data for robot perception algorithms. We surveyed the support for various sensors across mainstream simulation platforms. Specifically, the sensors considered include inertial measurement unit (IMU), force contact, RGB camera, LiDAR, and GPS. 

As shown in Table 4, most mainstream simulation platforms provide standard support for commonly used sensors, including vision (RGB), IMU, and contact force sensing. For example, Isaac Sim and Isaac Lab offer comprehensive high-fidelity sensor simulation. Isaac Gym supports IMU state and contact information output, but its vision capabilities are relatively limited in terms of runtime efficiency and parallel processing. In practice, it is often used in conjunction with Isaac Sim or Omniverse to enable highquality visual sensing and processing. Genesis provides comprehensive multimodal sensor support, making it suitable for complex perception tasks. Beyond these, support for other sensors varies across platforms. Specifically, Isaac Gym and SAPIEN do not provide native support for LiDAR sensors, while MuJoCo, PyBullet, and SAPIEN lack support for GPS. 

Besides sensor modeling, accurately simulating various joint types (such as floating, hinge, spherical, prismatic, fixed and helical) is crucial for reproducing the robot’s structure and motion characteristics in simulation platforms. The combination of these joints determines the robot’s degrees of freedom (DOF) and flexibility, which in turn affects its performance in complex tasks. By precisely modeling these joints in the simulation, developers can test and optimize robot designs and control strategies in a virtual environment, thereby improving system performance and reliability. 

As shown in Fig. 15, the simulation of joint components in these platforms is typically based on motion constraint mechanisms provided by physics engines, with the DOF between two rigid bodies defined to achieve the joint’s movement. Floating joints enable free movement and rotation in all directions. Fixed joints completely constrain the relative motion of two rigid bodies, hinge (revolute) joints allow rotation around a specific axis, prismatic joints allow linear motion along a specific axis, and spherical joints provide three rotational degrees of freedom. Simulation platforms often allow users to set parameters such as range limits, damping, and spring stiffness for joints to simulate the physical characteristics of actual mechanical systems. Some platforms also support more complex joint types, such as helical joints (which enable coupled rotational and translational motion). A helical joint allows two connected rigid bodies to perform synchronized rotation and linear movement along the same axis, similar to the advancement of a screw within a nut, with a single DOF and a helical motion trajectory. Table 4 also summarizes the support for various joint types across mainstream simulation platforms. Most simulators support common joint types such as floating, fixed, hinge, spherical, and prismatic. However, helical joints are less commonly supported and are natively implemented only in Gazebo and CoppeliaSim. 

21 

### **4.5 Discussions and Future Perspectives** 

Simulators are computational models designed to replicate real-world processes or systems, and they have become indispensable tools across various scientific and engineering disciplines. Their primary purpose is to provide a controlled environment for experimentation, analysis, and prediction without the need for costly or risky physical trials. Despite their widespread use, simulators possess both significant advantages and notable limitations, which highlight the need for more advanced modeling approaches such as world models. 

### _4.5.1 Advantages of Simulators_ 

Simulators offer several key benefits that make them valuable in research and practical applications: 

**Cost-effectiveness** : By reducing or eliminating the need for physical experiments, simulators can significantly lower the financial burden associated with testing and development. 

**Safety** : They enable the simulation of hazardous or dangerous scenarios (e.g., nuclear reactor failures or extreme weather conditions) without posing real-world risks. 

**Control** : Simulators provide precise control over variables and experimental conditions, allowing researchers to isolate specific factors and study their effects. 

**Repeatability** : Experiments conducted in simulators can be repeated exactly, ensuring consistency and facilitating the verification of results. 

### _4.5.2 Challenges of Simulators_ 

However, simulators are not without their challenges, and these limitations often constrain their effectiveness: 

**Accuracy** : Simulators may fail to fully capture the complexity of real-world systems, leading to inaccuracies in their predictions. Simplifications or approximations made during model design can result in discrepancies between simulated and actual outcomes. 

**Complexity** : Real-world systems are often highly intricate, with numerous interacting components and variables. Creating a simulator that accurately reflects this complexity is computationally demanding and, in some cases, infeasible. 

**Data dependency** : Effective simulators typically require large amounts of high-quality data to calibrate and validate their models. In scenarios where data is scarce or difficult to obtain, the performance of simulators can be severely compromised. 

**Overfitting** : There is a risk that simulators may become overly tailored to specific scenarios or datasets, reducing their ability to generalize to new or unseen conditions. This limits their applicability in dynamic or evolving environments. 

### _4.5.3 Future Perspectives_ 

Limitations in accuracy, complexity, and data dependency highlight the need for more sophisticated, adaptable modeling frameworks. This has motivated the development of world models, which aim to provide a more comprehensive and flexible approach to understanding and predicting real-world dynamics. Unlike traditional simulators, world 

models leverage advances in machine learning and artificial intelligence to create representations that can adapt to new data, handle complex systems more efficiently, and reduce reliance on extensive datasets. As such, the study of world models represents a natural evolution in the pursuit of more robust and versatile tools for modeling real-world phenomena. 

## **5 WORLD MODELS** 

“World models are **generative** AI models that understand the **dynamics** of the real world, including physics and spatial properties.” 

### – _NVIDIA’s World Foundation Models_ [17] 

Inspired by the human brain’s ability to form internal representations of the world, world models has emerged as a pivotal framework in artificial intelligence. These models enable agents to predict future states and plan actions, mimicking the cognitive processes that allow humans to navigate and interact with their environment. In 2018, David Ha and J¨urgen Schmidhuber introduced the idea of world models [18], demonstrating that an AI could learn a compressed, generative model of its environment and use it to simulate experiences, thereby facilitating reinforcement learning without direct interaction with the real world. 

As the field progressed, advancements in video generation models have significantly enhanced the capabilities of world models. Since early 2024, video generation models, such as Sora [263] and Kling [264] have garnered considerable attention from both academia and industry due to their high-fidelity video synthesis and realistic modeling of the physical world. The technical report on Sora, titled ”Video Generation Models as World Simulators” [263], emphasizes the potential of employing video generation models as robust engines for simulating the physical world. The Navigation World Model (NWM) [265] employed a Conditional Diffusion Transformer (CDiT) to predict future visual observations based on past experiences and navigation actions, which enables agents to plan navigation trajectories by simulating potential paths and evaluating their outcomes. 

Yann LeCun also emphasized the importance of videobased world models, stating that humans develop internal models of the world through visual experiences, particularly through binocular vision. He argues that for artificial intelligence to achieve human-level cognition, it must learn in a manner similar to humans, primarily through visual perception. This perspective underscores the significance of integrating video data into world models to capture the richness of spatial and temporal information. He further proposed the Video Joint Embedding Predictive Architecture (V-JEPA) model [266], which aims to learn abstract representations of videos by predicting missing parts of videos, thus providing new ideas for building a more powerful visual world model. 

Building upon these insights, recent developments in video generation models aim to create more sophisticated world models that can represent and understand dynamic environments. By leveraging large-scale video datasets and advanced neural architectures, these models strive to replicate the way humans perceive and interact with the world, paving the way for more advanced and adaptable artificial intelligence systems. 

22 


(a) World model in the AI system proposed by Lecun [261]. 


(b) Learn World model in a self-supervised manner [262]. 

Fig. 16: Illustration of the role and training of world models in AI systems. 

This section begins by reviewing the architectural evolution of video generation models, tracing their technological advancements to establish a foundation for subsequent discussions on their role as world models. It then highlights key developments in the application of generative models as world models across various domains, including their function as controllable data generators and their use in model-based reinforcement learning (model-based RL) for dynamic and reward modeling. 

### **5.1 Representative Architectures of World Models** 

To effectively capture the dynamics of complex environments, world models have evolved into a diverse set of architectural paradigms, each reflecting a different perspective on how to represent and predict the world. From early _compact latent dynamics models_ to recent powerful _generative architectures_ , these models differ in how they encode states, handle temporal dependencies, and model future observations. Some approaches prioritize _efficient state abstraction and predictive learning in latent space_ , while others focus on _high-fidelity generation of future sensory inputs such as video or 3D scenes_ . Meanwhile, advances in sequence modeling, selfsupervised learning, and generative modeling, particularly with transformers and diffusion models, have profoundly shaped the design of modern world models. In this section, we review representative architectural families that have been widely adopted or recently proposed, highlighting their core modeling principles. An overview of the architecture evolution is shown in Fig. 17. 

**Recurrent State Space Model.** Recurrent State Space Models (RSSMs) are among the earliest and most widely adopted architectures for learning world models. The core 

idea is to use a compact latent space to encode the evolving state of the environment, and to model its temporal dynamics using a recurrent structure. This design enables long-horizon prediction and decision-making by simulating possible futures in the latent space, rather than directly predicting raw observations. The RSSM framework was popularized by the Dreamer series [267]–[271], which demonstrated that planning and reinforcement learning can be effectively conducted within the learned latent dynamics. The recurrent modeling of latent transitions remains a central mechanism for learning predictive and decision-aware representations in continuous environments. 

**Joint-Embedding Predictive Architecture.** Like RSSMs, Joint-Embedding Predictive Architectures (JEPAs) also model the world in an abstract latent space, but differ in learning objective. Instead of reconstructing visual observations, JEPA models are trained to predict abstractlevel representations of missing content in a purely selfsupervised manner. Originally proposed by Yann Lecun as part of a broader framework for autonomous machine intelligence [272], JEPA eliminates the need for explicit generative decoders by framing prediction as a representation matching problem. I-JEPA (Image JEPA) [273] and V-JEPA (Video JEPA) [274], [275] instantiate this idea in static and temporal domains respectively. I-JEPA learns to predict masked image regions directly in latent space, while V-JEPA extends this to spatiotemporal structures, enabling representation learning from videos without frame-level reconstruction. This architecture is particularly appealing for large-scale pretraining, where semantic abstraction and data efficiency are prioritized over exact observation synthesis. 

**Transformer-based State Space Models.** As world models scale to more complex environments and longer horizons, the limitations of recurrent architectures in modeling long-range dependencies have become more evident. Transformer-based models address this by replacing RNNs with attention-based sequence modeling, offering greater expressiveness and parallelism. In latent dynamics modeling, this shift is exemplified by works such as TransDreamer [276], TWM [277], and Google Deepmind’s Genie [278], where Transformers are used to model transitions in latent state spaces over extended temporal windows. These models retain the latent-space prediction philosophy of RSSMs, but benefit from the Transformer’s ability to capture global context across time, improving long-horizon consistency and planning performance. 

**Autoregressive Generative World Models.** Inspired by recent breakthrough in natural language processing, autoregressive generative models treat world modeling as a sequential prediction task over tokenized visual observations. These models leverage Transformer architectures to generate future observations conditioned on past context, often integrating multimodal inputs such as actions or language. Early video generation frameworks like CogVideo [279], NUWA [280], and VideoPoet [281] laid the groundwork by demonstrating scalable autoregressive synthesis of realistic videos. Building on this, recent generative world models for autonomous driving and 3D scene generation, such as GAIA-1 [282], OccWorld [283], incorporate autoregressive Transformers to model complex environment dynamics with multimodal inputs and outputs. However, discrete 

23 


Fig. 18: Comparison of autoregressive transformer-based world models and video diffusion-based world models. 

token quantization frequently results in the loss of highfrequency details, adversely affecting the visual quality of generated videos. 

**Diffusion-based Generative World Models.** In recent years, diffusion models have rapidly become a cornerstone of video generation, offering stable training and superior fidelity in synthesizing temporally consistent visual sequences. By iteratively denoising from noise, these models capture complex data distributions with high expressiveness. To reduce computational cost, recent works shift from pixel-space diffusion (e.g., VDM [284]) to latent-space modeling using pretrained autoencoders, enabling efficient cascaded generation of long and high-resolution videos (e.g., Imagen Video [285], VideoLDM [286], SVD [287]). With the emergence of large-scale pretrained models such as OpenAI’s Sora [263] and Google Deepmind’s Veo3 [288], diffusion has demonstrated not only visual realism but also the ability to model 3D structure and physical dynamics—qualities aligning closely with the goals of world models. 

As a result, diffusion-based architectures are now increasingly adopted in generative world models, where the goal is to simulate future observations grounded in realistic and controllable environments. Models like DriveDreamer [289], Vista [290] and GAIA-2 [291] apply diffusion 

model to generate video or 3D scenes conditioned on actions or other modalities. Compared to autoregressive models, diffusion models offer stronger spatiotemporal coherence and higher visual quality, making them a compelling foundation for building high-fidelity, predictive neural simulators of the world. 

Despite substantial progress in video diffusion-based world models, challenges persist in sampling speed, longduration generation, and the ability to model causal temporal dynamics. Consequently, emerging research such as Vid2World [292] and Epona [293] is investigating the integration of diffusion models’ visual expressiveness with the temporal modeling strengths of autoregressive models, aiming to achieve realistic and interactive video-based world modeling. 

### **5.2 Core Roles of World Models** 

Beyond architectural designs, it is equally important to understand the roles world models play in intelligent systems. As general-purpose representations of the environment, world models serve as crucial enablers across various domains. Their capacity to abstract and predict environmental dynamics allows them to support downstream applications far beyond simple reconstruction tasks. In this section, we 

24 

highlight three core roles that world models fulfill: 1) as _neural simulators_ that generate controllable, high-fidelity synthetic experiences. 2) as _dynamic models_ that enable planning and decision-making in model-based reinforcement learning; and 3) as _reward models_ that help extract meaningful training signals in the absence of dense or well-defined rewards. These perspectives not only reflect the practical utility of world models but also guide future research directions in leveraging world modeling for intelligent agents. 

### _5.2.1 World Models as Neural Simulator_ 

The rise of generative world models has unlocked the potential to simulate complex, controllable environments across vision and action domains. These models synthesize temporally coherent and semantically grounded videos conditioned on diverse inputs, such as text, images, and trajectories, enabling scalable training and evaluation for autonomous driving, robotics, and virtual agents. 

**NVIDIA’s Cosmos series** exemplifies this direction. Cosmos [294] proposes a unified platform for building foundation video models as general-purpose world simulators, adaptable via fine-tuning for domains such as robotics and autonomous driving. It offers a full-stack pipeline: from video filtering and tokenization to pretraining and downstream adaptation, designed for efficient, open-source world model development. 

Extending this foundation, Cosmos-Transfer1 [295] introduces a spatially conditioned, multi-modal video generator. Through adaptive fusion control, it incorporates structured inputs such as segmentation maps, depth, and edges to guide video synthesis. Its spatial weighting mechanism enhances generation controllability and diversity, supporting applications like sim-to-real transfer, data augmentation, and robot perception with fine-grained control. 

Beyond general-purpose models, domain-specific simulators like **Wayve’s GAIA series** focus on realistic and controllable traffic simulation. GAIA-1 [282] formulates unsupervised sequence modeling of driving videos using multi-modal inputs, such as language, vision, and action, to generate discrete video tokens. GAIA-2 [291] improves generation fidelity and control by combining structured priors (vehicle states, road layout, scene semantics) with a latent diffusion backbone, enabling high-resolution, multi-cameraconsistent video synthesis across diverse traffic settings. 

In addition to image-based models, emerging work explores 3D-structured neural simulators that explicitly model physical occupancy or scene geometry. DriveWorld [296] builds a city-scale traffic simulator with causal interactions between agents, offering a richly structured environment for embodied planning. Similarly, DOME [297] proposes a diffusion-based world model that predicts future 3D occupancy frames instead of RGB pixels, achieving high-fidelity and long-horizon predictions with fine-grained controllability. AETHER [298] introduces a single geometry-aware framework, simultaneously preserving scene geometric consistency and ensuring the inferability of generated content, thereby establishing a geometric foundation for a unified world model. Complementarily, DeepVerse [299] recasts world modeling as a 4D autoregressive video-generation task, produces future predictions that are both coherent and 


Fig. 19: The general framework of Model-based RL. The agent learns a dynamic model _f_ : ( _st, at_ ) _→ st_ +1 and a reward model _r_ : ( _st, at_ ) _→ rt_ , which are used to simulate interactions and improve policy learning. 

controllable. These approaches highlight that neural simulators need not produce RGB videos: structured 3D/4D world representations can equally serve as simulation backbones in control-intensive domains. 

Overall, video and 3D generative models as neural simulators enable controllable, high-fidelity, and richly structured world synthesis, serving as scalable alternatives to traditional simulators for training intelligent agents. As model expressivity and control improve, their role in simulation, rare event synthesis, and data-driven decision-making is expected to grow across domains such as autonomous driving, humanoid robotics, and beyond. 

### _5.2.2 World Models as Dynamic Models_ 

In model-based reinforcement learning (MBRL), the agent builds an internal model of the environment. This model usually includes _dynamic model_ , _reward model_ , and _policy model_ . The agent uses this model to simulate interactions with the environment, which helps the agent to make better decisions, as shown in Fig. 19. Instead of relying solely on real-world interactions, the agent learns a dynamic model and a reward model from collected experience, and subsequently performs planning or policy learning within the simulated environment. This decoupling of environment modeling and policy optimization significantly enhances sample efficiency, which is especially valuable in scenarios with costly, slow, or high-risk data collection. 

World models can serve as general-purpose dynamic models in MBRL by learning to predict future states or observations conditioned on past interactions. Rather than relying on handcrafted symbolic rules or low-dimensional physics simulators, world models learn internal representations of environment dynamics directly from data. These models enable the agent to simulate hypothetical futures, perform rollouts for planning, and optimize behavior through imagined experiences. Depending on the design, world models may operate in pixel space, latent space, or structured representations, but their shared objective is to capture the temporal evolution of the environment in a way that supports efficient policy learning. This modeling flexibility allows world models to generalize across tasks, 

25 


Fig. 20: Core idea of the Dreamer series [300]: learn a latent world model as a dynamics model and optimize policies through model-based RL 

incorporate rich perceptual inputs, and serve as a scalable foundation for decision-making in complex domains. 

**The Dreamer series** systematically explores latent-space modeling of environment dynamics from visual input. As shown in Fig. 20, its central idea is to encode highdimensional observations into compact, predictive latent trajectories using variational autoencoding and state-space modeling, enabling efficient policy learning through imagined rollouts. DreamerV1 [268] introduced the Recurrent State-Space Model (RSSM), demonstrating strong performance on pixel-based control benchmarks such as DMC. DreamerV2 [269] extended this framework with discrete latent variables to improve modeling capacity and generalization, achieving human-level scores on Atari. DreamerV3 [270] further incorporated normalization and training stabilization mechanisms, becoming the first general world model to reach state-of-the-art performance across a broad range of visual control tasks. DayDreamer [271] validated the real-world applicability of this approach by deploying a Dreamer-style model on physical robots. 

To improve model generalization and transfer, recent work explores pretraining world models on real-world video data. ContextWM [301] uses natural videos to learn generalizable visual dynamics in an unsupervised manner. By introducing a context modulation mechanism, the model selectively attends to predictable spatial-temporal regions, enabling more sample-efficient fine-tuning in downstream robotics and driving tasks. These results suggest that highquality visual pretraining can endow world models with transferrable priors across domains. 

Beyond latent modeling, token-based approaches directly model visual dynamics in discrete video space. iVideoGPT [302] exemplifies this line of work, using VQVAE [303] to tokenize videos, actions, and rewards into multi-modal sequences. A Transformer is then trained to autoregressively predict future tokens conditioned on past context. Unlike Dreamer-style methods, iVideoGPT bypasses explicit state construction and instead samples full video rollouts to augment offline policy learning via standard actor-critic methods [304]. This direct modeling 

approach offers greater flexibility and demonstrates strong generalization in complex, multi-step planning tasks. 

In conclusion, world models serve as dynamic models by enabling agents to learn, simulate, and plan based on environment dynamics. Whether implemented in latent space or high-dimensional visual space, they form the backbone of modern MBRL systems by unifying perception, prediction, and decision-making in a single generative framework. 

### _5.2.3 World Models as Reward Models_ 

Designing effective reward signals remains a fundamental challenge in reinforcement learning (RL), particularly in open-ended or complex environments. Traditional methods often rely on manually crafted reward functions, which are expensive to define and may fail to capture meaningful behavioral cues. This limitation has motivated the development of methods that automatically infer rewards from weakly supervised or unlabeled data, such as raw videos. 

Recent advances in generative world models, especially those trained for video prediction, offer a promising direction for reward inference. These models learn to capture the underlying dynamics and structure of expert demonstrations, enabling them to serve as implicit reward models. The key insight is that if an agent’s behavior leads to trajectories that are easier for the model to predict, it likely aligns with the implicit preferences embedded in the training data. Thus, the model’s prediction confidence can be interpreted as a learned reward signal. 

VIPER [305] exemplifies this approach. It trains an autoregressive video world model on expert demonstrations, and then uses the model’s prediction likelihood during online agent behavior as the reward. When the agent acts in a way that produces highly predictable trajectories, it receives higher rewards. This enables learning high-quality policies without manually defined rewards. VIPER demonstrates strong performance on visual control benchmarks such as DMC, Atari, and RLBench. Additionally, due to the generalization ability of the learned world model, it can transfer reward inference across different embodiments and environments, such as variations in robotic arms or scene layouts. 

26 

Looking ahead, with continued progress in long-horizon modeling and multi-modal conditional generation, generative world models are poised to play a central role in reward modeling, such as humanoid control, multi-agent collaboration, and embodied interaction. Unifying dynamic modeling and reward inference within a single generative framework holds the potential to advance general-purpose agents that learn directly from raw visual experience. 

## **6 WORLD MODELS FOR INTELLIGENT AGENTS** 

Autonomous driving and articulated robots (including robotic arms, quadruped robots, and humanoid robots) are two critical applications of artificial intelligence and embodied intelligence. Autonomous driving vehicles, can be seen as an intelligent robot with four wheels together with a smaller action space comparing to humanoid robots. Also, autonomous driving is a critical application of artificial intelligence, imposes stringent requirements on world modeling. Further, autonomous driving systems require real-time comprehension and forecasting of complex and dynamic road environments. As discussed in the previous section, video generation models as world models have demonstrated capacity for capturing physics and dynamic interactions, making them well-suited for the highly dynamic, high-stakes context of autonomous driving. Articulated robots (including robotic arms, quadruped robots, and humanoid robots), as the core carriers of Embodied Intelligence, pose unique and stringent requirements for world modeling. Similar to autonomous driving, robot systems also need to predict and understand its surroundings to conduct complex locomanipulation tasks in human-centered environment. 

Both autonomous driving and articulated robots require rich, long-term, and safe interactions with the real world during their applications, which places high demands on the precise and predictable modeling of the real world. This section explores the applications and challenges of world models in autonomous drive and articulated robots, particularly in the context of video generation-based models. 

### **6.1 World Models for Autonomous Driving** 

Traditional autonomous driving architectures employ a modular design with independent modules for perception, prediction, planning, and control [306], [307]. While facilitating development and testing, this design exhibits critical limitations: errors in perception modules compound and amplify during processing [308], temporal modeling of long-term dependencies remains challenging [309], and performance deteriorates significantly in unfamiliar scenarios, as demonstrated by the 2018 Uber autonomous vehicle accident where the system repeatedly failed to correctly identify a pedestrian despite detecting them 5.6 seconds before impact [310]. 

Tesla share similar visual encoding architectures in the research and development of autonomous driving and robots [311], reflecting the commonality of perception technology. Video generation-based world models have become a key area of research in autonomous driving, progressing from early foundational models to sophisticated systems that have achieved significant advancements in scene generation, multi-view consistency, closed-loop simulation, and 

reasoning. Unlike general video generation world models discussed previously, those designed for autonomous driving prioritize the unique characteristics and safety demands of traffic scenarios, leading to the development of several notable technical approaches and application paradigms. 

We follow the previous categorization in section 5.2, and categorize autonomous driving world models into three main types as shown in Fig. 21: Neural Simulator, Dynamic Model, and Reward Model. Three representative pipelines of autonomous driving world models are illustrated in Fig. 22. 

### _6.1.1 WMs as Neural Simulators for Autonomous Driving_ 

Neural simulators focus on generating realistic driving scenarios for training and testing autonomous systems. These models typically take multi-modal inputs (images, text, actions, trajectories) and produce high-fidelity video sequences that simulate diverse driving conditions for data augmentation and safety validation. 

**GAIA-1** [282] pioneered treating world modeling as sequence prediction in autonomous driving, integrating video, text, and action inputs through an autoregressive transformer architecture to generate realistic driving scenarios. The model leverages a 9-billion parameter transformer trained on 4,700 hours of proprietary driving data, demonstrating emergent behaviors such as predicting diverse future scenarios from the same context and reasoning about interactions with dynamic agents. A key innovation is its ability to generate long, diverse driving scenes purely from learned understanding, with controllable generation through action conditioning and text prompts that can influence environmental aspects like weather and time of day. 

Building upon this foundation, and also transitioning from autoregressive to diffusion-based approaches, **GAIA2** [312] advanced controllable generation with structured conditioning for ego-vehicle dynamics, multi-agent interactions, and environmental factors. The model integrates both structured conditioning inputs and external latent embeddings from proprietary driving models, enabling finegrained control over weather, lighting, and scene geometry across diverse geographical environments including the UK, US, and Germany. This enhanced controllability facilitates scalable simulation of both common and rare safety-critical driving scenarios through high-resolution, spatiotemporally consistent multi-camera video generation. 

**DriveDreamer** [313] also introduced diffusion-based generation with structured traffic constraints, representing a major advancement in driving scenario generation. The model demonstrates superior performance on real-world data by learning from actual driving scenarios rather than simulated environments, employing a two-stage training pipeline where the first stage learns structured traffic constraints and the second stage enables future state anticipation. This approach allows for generating precise and controllable videos that faithfully capture the structural constraints of real-world traffic. **DriveDreamer-2** [314] enhanced the DriveDreamer framework by integrating Large Language Models (LLMs) to enable natural language-driven scenario generation. The system operates through an LLM interface that converts textual user queries into agent trajectories, followed by HDMap generation that adheres to 

27 


Fig. 21: Illustration of the world model’s three roles in autonomous driving: Neural Simulator, Dynamics Model and Reward Model. 

traffic regulations, and finally employs a Unified MultiView Model (UniMVM) to generate driving videos with enhanced temporal and spatial coherence. This represents the first world model capable of generating customized driving videos based on user descriptions, achieving improvements in quality while enabling generation of diverse and uncommon driving scenarios crucial for robust autonomous driving training. **DriveDreamer4D** [315] further enhanced 4D driving scene representation by leveraging world model priors to synthesize novel trajectory videos with explicit spatiotemporal consistency control. The framework uses existing world models as ”data machines” to synthesize novel trajectory videos with structured conditions that explicitly control the spatiotemporal consistency of traffic elements. A key innovation is the ”cousin data training strategy” that effectively merges real and synthetic data for optimizing 4D Gaussian Splatting-based reconstruction, significantly improving generation quality for novel trajectory views and spatial temporal coherence. 

Aiming to address the challenge of 3D geometry control, **MagicDrive** [316] introduced a novel street view generation framework that accepts diverse inputs including camera poses, road maps, 3D bounding boxes, and textual descriptions. The system employs tailored encoding strategies for varied inputs and incorporates a cross-view attention module to ensure consistency across multiple camera views, enabling high-fidelity street-view synthesis that accurately captures nuanced 3D geometry and diverse scene characteristics such as lighting and weather. **MagicDrive3D** [317] extended this capability to enable controllable 3D generation for any-view rendering through a novel two-step ”generation-first, reconstruction-later” pipeline. The framework first trains a conditional multi-view video generation model, then reconstructs 3D scenes from generated video 

data using Deformable Gaussian Splatting with monocular depth initialization and appearance modeling. This approach represents the first framework to effectively integrate geometry-free view synthesis with geometry-focused reconstruction for controllable 3D street scene generation using common driving datasets. **MagicDrive-V2** [318] scaled the framework to high-resolution, long-duration videos using Diffusion Transformer architecture integrated with 3D Variational Autoencoders. The system incorporates an MVDiT block for multi-view video generation, novel spatial-temporal conditional encoding for precise geometric control, and a three-stage progressive bootstrapping training strategy that enables synthesis of videos up to 848×1600 resolution and 241 frames. This represents a significant advancement in output resolution, frame count, and control fidelity for autonomous driving applications. **Panacea** [319] focused on panoramic video generation with multi-view consistency mechanisms and super-resolution capabilities. The framework employs a two-stage video generation model that first synthesizes multi-view images, then constructs multi-view videos from these images, incorporating multi-view appearance noise prior mechanisms and super-resolution modules to enable generation of highquality, high-resolution 360-degree videos. 

Focusing on multi-camera consistency, **WoVoGen** [320] introduced explicit 4D world volumes as foundational elements, operating in two phases to envision future 4D temporal world volumes and generate multi-camera videos with sensor interconnectivity. The model addresses the challenge of maintaining intra-world consistency and inter-sensor coherence by incorporating 4D world volumes that adeptly integrate time with spatial data. The generated 4D world feature is geometrically transformed to sample 3D image volumes for each camera, enabling high-quality street-view 

28 


Fig. 22: Illustration of the world model’s representative pipelines: GAIA-2 [312], MagicDrive [316], and DriveDreamer [313] 

video generation that responds to vehicle control inputs while maintaining consistency across sensors. 

Recent works have also explored occupancy representations for more structured scene understanding. **OccSora** [321] employed a diffusion-based 4D occupancy generation model to simulate 3D world development, generating 16-second videos with authentic 3D layouts and temporal consistency. The framework uses a 4D scene tokenizer to obtain compact, discrete spatio-temporal representations from 4D occupancy input, followed by a diffusion transformer trained on these representations for trajectory-conditioned 4D occupancy generation. **DriveWorld** [322] used occupancy-based Memory State-Space Models (MSSM) for 4D scene understanding by learning from multi-camera driving videos. The framework comprises a Dynamic Memory Bank for temporal-aware latent dynamics and a Static Scene Propagation module for spatialaware latent statics. This approach enables comprehensive 4D scene understanding that benefits diverse vision-centric perception, prediction, and planning tasks, demonstrating improvements across multiple autonomous driving benchmarks. **Drive-OccWorld** [323] combined occupancy forecasting with end-to-end planning through semantic and motion-conditional normalization techniques. The framework features a memory module that accumulates semantic and dynamic information from historical BEV embeddings, enabling controllable generation of future states through flexible action conditions. This integration of forecasting capabilities with end-to-end planning opens new avenues for driving world generation and integrated planning systems. 

Targeting at address time horizon challenges of generated result, **InfinityDrive** [324] enabled generation of indefinitely long driving sequences through generative mod- 

els that maintain coherence over extended periods. The framework addresses challenges in sampling speed, longduration generation, and temporal consistency, representing efforts to achieve controllable, efficient, and realistic videobased world modeling for autonomous driving applications. 

**ReconDreamer** [325] enhanced driving scene reconstruction for closed-loop simulation through online restoration and progressive data update strategies. The framework introduces ”DriveRestorer,” a world model-based component that mitigates ghosting artifacts through online restoration, coupled with progressive data updates to ensure highquality rendering especially for large and complex maneuvers. This represents the first method to effectively render large maneuvers such as multi-lane shifts spanning up to 6 meters. 

### _6.1.2 WMs as Dynamic Models for Autonomous Driving_ 

Dynamic models focus on learning the underlying physics and motion patterns in driving environments, primarily serving perception, prediction, and planning tasks rather than high-fidelity generation. These models learn environment dynamics to enable better decision-making and longterm planning. 

**MILE** [350] pioneered model-based imitation learning for urban driving by jointly learning a predictive world model and driving policy from expert demonstrations. The framework achieves significant improvements in driving scores through high-resolution video inputs and 3D geometry as inductive bias, demonstrating how world models can serve as effective foundations for policy learning in complex urban environments. The joint learning approach enables the model to capture both environmental dynamics and appropriate driving behaviors simultaneously. 

29 

TABLE 5: Comparison of **Key Research** for World Models in Autonomous Driving 

|**Category**|**Paper**|e|**In**<br>on|**put**<br>**Output**<br>ctory<br>metry<br>|**World Model**<br>**Architecture**|**Dataset**<br>**Code**<sup>2</sup>|
|---|---|---|---|---|---|---|
|||Imag|Text<br>Acti|Traje<br>Geo<br>1<br>Map|||
||GAIA-1 [282]|✓|✓<br>✓|Image|Transformer|In-house|
||DriveDreamer [313]|✓|✓<br>✓|✓<br>✓<br>Image|Diffusion|nuScenes<br>✓|
||ADriver-I [326]|✓|✓|Image|Diffusion|nuScenes [327] & In-house|
||GAIA-2 [312]|✓|✓<br>✓|✓<br>✓<br>Image|Diffussion|In-house|
||DriveDreamer-2 [314]|✓|✓<br>✓|✓<br>✓<br>✓<br>Image|Diffusion|nuScenes|
||DriveDreamer4D [315]|✓|✓|✓<br>✓<br>Image|Diffusion|Waymo Open dataset (WOD) [328]<br>✓|
||DrivingWorld [329]|✓||✓<br>Image|Transformer|NuPlan [330] & In-house|
||MagicDrive [316]|✓|✓|✓<br>✓<br>Image|DiT|nuScenes<br>✓|
||MagicDrive3D [317]||✓|✓<br>✓<br>✓<br>Image|DiT|nuScenes|
||MagicDrive-V2 [318]|✓|✓|✓<br>✓<br>✓<br>Image|DiT|nuScenes|
||WoVoGen [320]|✓|✓|✓<br>✓<br>Image|Diffusion|nuScenes, Occ3d [331], nuScenes-lidarseg|
||ReconDreamer [325]|✓||✓<br>✓<br>✓<br>Image|Diffusion|Waymo Open dataset (WOD)<br>✓|
||DualDiff+ [332]|✓|✓|✓<br>✓<br>Image|Transformer|nuScenes|
|**Neural**<br>|Panacea [319]|✓|✓|✓<br>✓<br>Image|Diffusion|nuScenes|
|**Simulator**|Cosmos-Transfer1 [295]|✓|✓|✓<br>Image|DiT|Cosmos [294]<br>✓|
||GeoDrive [333]|✓||✓<br>✓<br>Image|Diffusion|nuScenes|
||DriveWorld [322]|✓|✓<br>✓|Occupancy|Transformer|nuScenes, Openscene [334]|
||OccSora [321]|||✓<br>Occupancy|Diffusion|nuScenes<br>✓|
||Drive-OccWorld [323]|✓|✓<br>✓|✓<br>Occupancy|Transformer|nuScenes, Lyft-Level5 [335]|
||DOME [297]|||✓<br>✓<br>Occupancy|Diffusion|nuScenes<br>✓|
||RenderWorld [336]|||✓<br>Occupancy|Transformer|nuScenes|
||OccLLama [337]||✓|✓<br>✓<br>Occupancy|Transformer|NuScenes, Occ3D, NuScenes-QA [338]|
||BEVWorld [339]|✓|✓|✓<br>Image, point cloud|Diffusion|nuScenes, Carla simulation [340]|
||HoloDrive [341]|✓|✓|✓<br>✓<br>Image, point cloud|Transformer|NuScenes|
||GEM [342]|✓||✓<br>✓<br>Image, depth|Diffusion|BDD [343], etc [344], [345]<br>✓|
||DriveArena [346]|✓|✓|✓<br>✓<br>Image|Diffusion|nuScenes<br>✓|
||ACT-Bench [347]|✓|✓<br>✓|✓<br>Image|Transformer|nuScenes, ACT-Bench|
||InfinityDrive [324]|✓|✓<br>✓|Image|Transformer|nuScenes|
||Epona [293]|✓||✓<br>Image|Transformer|NuPlan<br>✓|
||DrivePhysica [348]|✓|✓<br>✓|✓<br>✓<br>Image|Diffusion|nuScenes|
||Cosmos-Drive [349]|✓|✓<br>✓|✓<br>✓<br>✓<br>Image|DiT|In-house, WOD<br>✓|
||MILE [350]|✓|✓|Image, BEV Semantics|RNN|Carla simulation<br>✓|
||Cosmos-Reason1 [351]|✓|✓<br>✓|Text|Transformer|Cosmos-Reason-1-Dataset|
||TrafficBots [352]||✓|✓<br>✓<br>✓<br>Trajectory|Transformer|Waymo Open Motion Dataset<br>✓|
||Uniworld [353]|✓||Occupancy|Transformer|nuScenes|
||Copilot4D [354]|||✓<br>Point cloud|Diffusion|nuScenes, KITTI [355]|
||MUVO [356]|✓|✓|✓<br>Image, Occupancy, Point cloud|RNN|Carla simulation|
||OccWorld [283]|||✓<br>✓<br>Occupancy|Transformer|nuScenes, Occ3D<br>✓|
||ViDAR [357]|✓|✓|Point cloud|Transformer|nuScenes|
||Think2Drive [358]|||✓<br>✓<br>BEV Semantics|RNN|CARLA simulation|
||LidarDM [359]|||✓<br>Point cloud|Diffusion|KITTI-360, WOD|
||LAW [360]|✓|✓|BEV Semantics|Transformer|nuScenes, NAVSIM [361], CARLA simulation<br>✓|
|**Dynamic**|UnO [362]|||✓<br>Occupancy|Transformer|nuScenes, Argoverse 2, KITTI Odometry|
|**Model**|CarFormer [363]||✓|✓<br>✓<br>✓<br>Trajectory|Transformer|CARLA simulation<br>✓|
||NeMo [364]|✓||Image, Occupancy|Transformer|nuScenes|
||Covariate Shift [365]|✓|✓|Image, BEV Semantics|Transformer|CARLA simulation|
||Imagine-2-Drive [366]|✓||✓<br>Image|Diffusion|CARLA simulation|
||Doe-1 [367]|✓|✓|✓<br>Image|Transformer|nuScenes<br>✓|
||GaussianWorld [368]|✓|✓|✓<br>Occupancy|TransFormer|nuScenes|
||DFIT-OccWorld [369]|✓||✓<br>✓<br>Image, Occupancy|Transformer|Occ3D, nuScenes, OpenScene|
||DrivingGPT [370]|✓|✓|Image|Transformer|nuPlan|
||AdaWM [371]||✓|✓<br>Trajectory|RNN|CARLA simulation|
||AD-L-JEPA [372]|||✓<br>Point cloud|JEPA|KITTI3D, WOD|
||HERMES [373]|✓|✓<br>✓|Point cloud|Transformer|nuScenes, OmniDrive-nuScenes|
||SEM2 [374]|✓|✓|✓<br>Image Point cloud|RNN|nuScenes|
||<br>Iso-Dream [375]|✓|✓|,<br>Image|RNN|nuScenes<br>✓|
|**Reward**<br>**Model**|Vista [376]|✓|✓<br>✓|✓<br>Image|Diffusion|nuScenes, etc [328], [344], [377].|
||Drive-WM [378]<br>WoTE [379]|✓|✓<br>✓|✓<br>✓<br>Image<br>✓<br>✓<br>BEV Semantics|Diffusion<br>Transformer|nuScenes<br>NAVSIM<br>✓|
||<br>IRL-VLA [380]|✓|✓<br>✓|<br>✓<br>Trajectory, Action Sequence|Diffusion|NAVSIM|


> 1 Geometry mean 3D geomtric representation which includes: 3D voxel occupancy, 3D bounding box, 3D depth, 3D segmentation and 3D point cloud. 

> 2 Code availability: ” ” means code is not announced to be released in the paper or is announced to be released in the paper, but the full code (training and inference) is still no available yet, ”✓” means code is released. 

30 

**TrafficBots** [352] addressed multi-agent traffic simulation with configurable agent personalities through conditional variational autoencoders, enabling scalable simulation of diverse driving behaviors. The system introduces destination-based navigation and time-invariant personality latents to control agent behavior styles from aggressive to cautious, providing a comprehensive framework for simulating realistic multi-agent interactions in traffic scenarios. 

Building on occupancy-based representations for better 3D understanding, **UniWorld** [353] employed 4D geometric occupancy prediction as a foundational pre-training task, achieving notable improvements in motion prediction, 3D object detection, and semantic scene completion. The framework demonstrates how 4D occupancy prediction can serve as a unified pre-training objective that benefits multiple downstream autonomous driving tasks through comprehensive spatiotemporal scene understanding. **OccWorld** [283] used vector-quantized variational autoencoders to learn discrete scene tokens from 3D occupancy data, enabling GPT-like spatial-temporal generative modeling. This approach reformulates scene understanding as a sequence modeling problem, allowing for efficient autoregressive prediction of future occupancy states while maintaining spatial and temporal coherence across extended horizons. **GaussianWorld** [368] reformulated 3D occupancy prediction as 4D occupancy forecasting, using Gaussian world models to infer scene evolution considering ego motion, dynamic objects, and newly-observed areas. The framework leverages Gaussian representations to model uncertainty and temporal dynamics, enabling more robust forecasting in complex driving scenarios with multiple moving agents and changing environmental conditions. 

**DFIT-OccWorld** [369] introduced an efficient occupancy world model through decoupled dynamic flow, reformulating occupancy forecasting as voxel warping processes with image-assisted training paradigms. This approach improves computational efficiency while maintaining prediction accuracy by separating static and dynamic scene elements, enabling more scalable deployment in real-time autonomous driving systems. 

Addressing sensor fusion and geometric understanding, **MUVO** [356] incorporated spatial voxel representations to learn sensor-agnostic geometric understanding from both camera and LiDAR data. The framework addresses the neglect of physical and geometric attributes in existing world models by integrating multi-modal sensor inputs into unified 3D representations, enabling more comprehensive scene understanding that bridges the gap between different sensor modalities. **ViDAR** [357] introduced visual point cloud forecasting as a pre-training task, predicting future LiDAR point clouds based solely on historical visual input to foster synergic learning of semantics, 3D structures, and temporal dynamics. This cross-modal approach demonstrates how world models can learn to translate between different sensor modalities while maintaining spatiotemporal consistency and semantic understanding. 

**LAW** [360] proposed self-supervised learning without perception labels by predicting future latent features based on current observations and ego-vehicle actions. This approach significantly reduces reliance on expensive manual annotations while enabling effective learning of 

environment dynamics through latent feature prediction. The framework demonstrates how world models can be trained efficiently without requiring dense supervision, making them more practical for large-scale deployment. **Think2Drive** [358] demonstrated efficient reinforcement learning in latent space by training a neural planner within a compact latent world model, achieving expert-level proficiency in complex urban scenarios. The framework shows how latent world models can enable efficient planning and decision-making by abstracting complex high-dimensional observations into manageable latent representations that preserve essential information for control. **HERMES** [373] unified 3D scene understanding and generation within a single framework using Bird’s-Eye View representations and ”world queries” that incorporate world knowledge through causal attention mechanisms. The framework demonstrates how world models can integrate understanding and generation capabilities, enabling both perception and simulation within a unified architecture that leverages causal attention for improved temporal modeling. 

**Cosmos-Reason1** [351] represents cutting-edge exploration in incorporating physical common sense and embodied reasoning, generating scenes that conform more closely to physical laws while reasoning about possible physical interactions. This work advances the field by integrating physical reasoning capabilities into world models, enabling more realistic simulation of complex physical interactions in driving scenarios. **Doe-1** [367] formulated autonomous driving as a next-token generation problem using multi-modal tokens (observation, description, and action), enabling unified perception, prediction, and planning through autoregressive generation. This approach demonstrates how language model architectures can be adapted for autonomous driving by treating all modalities as tokens in a unified sequence, enabling end-to-end learning across perception and control tasks. **DrivingGPT** [370] combined driving world modeling and trajectory planning using multi-modal autoregressive transformers, treating interleaved discrete visual and action tokens as a unified ”driving language.” The framework demonstrates how driving can be formulated as a language modeling problem, enabling the application of large-scale language model techniques to autonomous driving while maintaining the ability to reason about both visual inputs and control outputs. 

### _6.1.3 WMs as Reward Models for Autonomous Driving_ 

Reward models evaluate the quality and safety of driving behaviors, often integrated with reinforcement learning for policy optimization. These models use world model predictions to assess trajectory safety and guide decision-making without requiring manually engineered reward functions. 

**Vista** [376] demonstrated generalizable reward functions using the model’s own simulation capabilities, establishing a novel approach where the world model itself assesses the quality or safety of potential driving maneuvers by simulating their outcomes. The system supports versatile action controllability from high-level intentions to low-level maneuvers. This self-assessment capability enables the model to provide intrinsic motivation for safe driving behaviors without requiring manual reward engineering. 

31 

**WoTE** [379] focused on trajectory evaluation using Bird’s-Eye View world models for real-time safety assessment in end-to-end autonomous driving systems. The framework leverages BEV world models to predict future states and evaluate trajectory safety more efficiently than image-level approaches, demonstrating state-of-the-art performance on NAVSIM and Bench2Drive benchmarks. This approach enables continuous safety monitoring and trajectory assessment in real-time autonomous driving applications. 

**Drive-WM** [378] enabled multi-future trajectory exploration with image-based reward evaluation through joint spatial-temporal modeling and view factorization. The system can simulate multiple possible futures based on distinct driving maneuvers and determine optimal trajectories by evaluating imagined futures using image-based rewards. This capability supports safe driving planning through world model-based ”what-if” reasoning, enabling the system to explore and evaluate multiple potential actions before execution. 

**Iso-Dream** [375] addressed the challenge of controllable versus non-controllable dynamics separation in driving environments. The approach enhances model-based reinforcement learning by isolating controllable dynamics (egovehicle actions) from non-controllable dynamics (other vehicles, environmental changes), enabling more effective longhorizon planning and decision-making in complex traffic scenarios. This separation enables more focused learning on controllable aspects while properly modeling environmental uncertainty. 

### _6.1.4 Technical Trends and Implications_ 

The evolution of autonomous driving world models reveals four major technological trends that are reshaping how we approach vehicle simulation and testing: 

**Generative Architecture Evolution from Autoregressive to Diffusion Models:** Early autonomous driving world models like GAIA-1 employed autoregressive transformer architectures that predicted future driving scenarios through sequential token generation. While these approaches demonstrated strong capabilities in learning high-level scene structures, they faced significant computational challenges when generating long-duration, high-fidelity driving videos due to the sequential nature of token prediction. The field has since witnessed a paradigm shift toward diffusion-based models, exemplified by the DriveDreamer series, GAIA-2, and WoVoGen, which offer superior control over generation quality. Modern hybrid architectures are beginning to emerge that combine autoregression with diffusion-based scene generation. The integration of diffusion transformers (DiT) in models like MagicDrive-V2 represents the latest evolution, combining the strengths of transformer attention mechanisms with diffusion-based generation. 

**Multi-Modal Integration and Controllable Scenario Generation:** Recent autonomous driving world models have evolved from simple image-to-image generation to sophisticated multi-modal systems that integrate diverse input types including camera images, LiDAR point clouds, textual descriptions, vehicle trajectories, and high-definition maps. This evolution addresses the fundamental challenge in autonomous vehicle testing: the need to generate specific, 

controllable driving scenarios that can stress-test different aspects of the driving system under precisely defined conditions. Models like GAIA-2 and DriveDreamer-2 exemplify this trend by accepting structured inputs such as ego-vehicle dynamics, multi-agent configurations, environmental factors (weather, time of day), and road semantics to enable fine-grained control over generated scenarios. This multimodal approach also facilitates the generation of synchronized multi-camera views can cover 360-degree. These advances have transformed world models into active simulation tools that can explore the vast space of possible driving scenarios, enabling more efficient validation of autonomous driving systems. 

**3D Spatial-Temporal Understanding and OccupancyBased Representations:** A fundamental branch that has occurred in autonomous driving world models is to have a comprehensive 3D spatial-temporal modeling that better captures the true nature of driving environments. Early models focused primarily on generating realistic camera images, but this approach failed to provide the geometric consistency and 3D understanding necessary for training robust perception systems that must reason about object depths, occlusions, and spatial relationships in real driving scenarios. The transition to 3D-aware modeling is exemplified by frameworks like OccSora, Drive-OccWorld, and OccWorld, which represent driving scenes through 4D occupancy grids that encode both spatial structure and temporal dynamics in a unified representation. This 3D-aware modeling capability enables world models to serve not just as data generators but as comprehensive simulators that can predict how driving scenes evolve in response to ego-vehicle actions. The integration of techniques like Gaussian Splatting in models such as GaussianWorld and MagicDrive3D further enhances the geometric fidelity of generated scenes, enabling novel view synthesis and supporting the development of more robust perception algorithms. 

**End-to-End Integration with Autonomous Driving Pipelines:** Modern autonomous driving world models are increasingly designed not as standalone simulation tools but as a prediction component of modular End-to-End autonomous driving. Models like MILE, LAW, Think2Drive and WoTE exemplify this integrated approach by jointly learning world dynamics and driving policies, enabling end-to-end optimization that can minimize the accumulation of errors across different system components. The integration extends to reward modeling capabilities, where frameworks like Vista and Drive-WM use their own simulation capabilities to evaluate trajectory safety and guide policy learning without requiring manually engineered reward functions. Advanced integrated systems like Doe1 and DrivingGPT demonstrate how world models can unify perception (scene understanding), prediction (future state forecasting), and planning (action generation) within a single neural architecture that treats all modalities as tokens in a unified sequence modeling problem. The ultimate goal of this integration trend is to create autonomous driving systems that can reason about their environment, predict future states, and plan safe actions within a unified learned representation. 

32 

### **6.2 World Models for Articulated Robots** 

Articulated robots (including robotic arms, quadruped robots, and humanoid robots), as the core carriers of Embodied Intelligence, pose unique and stringent requirements for world modeling. This section systematically explores the applications and challenges of world models in the field of articulated robot control, focusing on how methods based on robot simulation and multi-modal learning are driving a paradigm shift in robot technology. 

### _6.2.1 WMs as Neural Simulators for Articulated Robots_ 

World models serve as neural simulators by learning to generate temporally coherent and semantically rich representations of physical environments from multimodal inputs (e.g., text, images, trajectories). These generative models provide a scalable, data-driven alternative to traditional physics-based simulators, enabling efficient training and evaluation of autonomous agents. 

A prominent example is NVIDIA’s **Cosmos** World Foundation Model Platform [294], which establishes a unified framework for building foundation world models capable of producing physics-accurate 3D video predictions through diffusion and autoregressive architectures. By synthesizing realistic, controllable environments from structured inputs (e.g., segmentation maps, depth), Cosmos facilitates sim-toreal transfer, data augmentation, and perception training for robotics. Fig. 23 shows the **Cosmos-Predict** World Foundation Model. The platform’s modular design supports taskspecific fine-tuning via post-training on specialized datasets, significantly reducing data requirements through transfer learning from large-scale pretraining. This approach bridges the gap between simulation and reality, enhancing robot learning in dynamic environments such as autonomous driving and robotic manipulation. Future advancements in neural simulation fidelity and control will further expand their role in embodied AI systems. 

**WHALE** [381] proposes a generalizable world model framework with behavior-conditioning and retracingrollout for OOD generalization and uncertainty estimation. Whale-ST (spatial-temporal transformer) and Whale-X [428] (414 M-parameter model) demonstrate enhanced scalability and performance in simulation and real-world manipulation tasks. 

**RoboDreamer** [382] introduces a compositional world model for robotic decision-making by factorizing video generation into primitives. It leverages language compositionality to generalize to unseen object-action combinations and multimodal goals, synthesizing plans for novel tasks in RT-X and outperforming monolithic baselines in simulation. 

**DreMa** [383] introduces a compositional world model combining Gaussian Splatting and physics simulation to explicitly replicate real-world dynamics, enabling photorealistic future prediction and data-efficient imitation learning via equivariant transformations, achieving one-shot policy learning on a Franka robot with improved accuracy and generalization. 

**DreamGen** [384] introduces a 4-stage pipeline for training generalizable robot policies via neural trajectories, leveraging video world models to synthesize photorealistic data across behaviors and environments. It recovers pseudo- 


Fig. 23: The Cosmos-Predict World Foundation Model processes input videos through Cosmos-Tokenize1-CV8×8×8720p, encoding them into latent representations perturbed with Gaussian noise. A 3D patchification step structures these latents, followed by iterative self-attention, crossattention (conditioned on text), and MLP blocks, modulated by adaptive layer normalization. Finally, the decoder reconstructs high-fidelity video output from the refined latent space. This architecture enables robust spatiotemporal modeling for diverse Physical AI applications [294]. 

actions from generated videos, achieving zero-shot generalization with minimal real-world data, validated by DreamGen Bench benchmark. 

**EnerVerse** [385] introduces a generative foundation model for robotics manipulation, employing autoregressive video diffusion and Free Anchor Views (FAVs) for 3D world modeling. The framework integrates 4D Gaussian Splatting in EnerVerse-D to reduce sim-to-real gaps, while EnerVerseA translates 4D representations into actions, achieving stateof-the-art performance in simulated and real-world tasks. 

**WorldEval** [386] introduces a world model-based pipeline for online robot policy evaluation, using Policy2Vec to generate action-following videos via latent action conditioning. It enables scalable, reproducible ranking of policies and safety detection, demonstrating strong real-world cor- 

33 

TABLE 6: Comparison of Researches for World Models in Robotics (Part I) 

||||**In**<br>|**put**|||
|---|---|---|---|---|---|---|
|**Category**|**Paper**|**Year**|ption|**Architecture**<sup>2</sup>|**Experiments**<sup>3</sup>|**Code**<br>**Availability**<br>4|
||||Image<br>Proprioce<br>Text|Action<br>Geometry<br>1<br>Tactile|||
||WhALE [381]|2024|✓|✓<br>Transformer|Robotic arm|✗|
||RoboDreamr [382]|2024|✓<br>✓|Diffusion|Robotic arm|✓|
||DreMa [383]<br>|2024<br>|✓<br><br>|GS reconstruction<br>|Robotic arm<br>|✓|
||DreamGen [384]|2025|✓<br>✓|DiT|Dual robotic arm|_◦_|
||EnerVerse [385]|2025|✓<br>✓|✓<br>Diffusion|Robotic arm|✓|
|**Neural**|WorldEval [386]|2025|✓<br>✓|DiT|Robotic arm|✓|
|**Simulators**|Cosmos (NVIDIA) [294]|2025|✓<br>✓|Diffusion + Autoregressive|Robots|✓|
||Pangu [387]|2025|✓<br>✓|/|/|✗|
||RoboTransfer [388]|2025|✓<br>✓|✓<br>Diffusion|Robotic arm|_◦_|
||TesserAct [389]|2025|✓<br>✓|DiT|Robotic arm|✓|
||3DPEWM [390]|2025|✓|✓<br>DiT|Mobile robot|✗|
||SGImageNav [391]|2025|✓<br>✓<br>✓|LLM|Quadroped robot|✗|
||EmbodieDreamer [392]|2025|✓<br>✓|Diffusion + ACT|Robotic arm|_◦_|
||PlaNet [267]|2018|✓|RSSM|DMC|✓|
||Plan2Explore [262]|2020|✓|RSSM|DMC|✓|
||Dreamer [393]|2020|✓|RSSM|DMC|✓|
||DreamerV2 [394]|2021|✓|RSSM|DMC|✓|
||DreamerV3 [270]|2023|✓|RSSM|DMC|✓|
||DayDreamer [271]|2024|✓<br>✓|✓<br>RSSM|Robotic arm|✓|
||Dreaming [395]|2021|✓|RSSM|DMC|✓|
||Dreaming V2 [396]|2021|✓|RSSM|DMC + RoboSuite|✓|
||DreamerPro [397]|2022|✓<br>✓|RSSM|DMC|✓|
||TransDreamer [276]|2024||✓<br>TSSM|2D Simulation|✓|
||LEXA [398]|2021|✓|✓<br>RSSM|Simulated robotic arm|✓|
||FOWM [399]|2023|✓<br>✓|TD-MPC|Robotic arm|✓|
|**Dnamics**|SWIM [400]|2023|✓|RSSM|Robotic arm|✗|
|**y**<br>**Models**|ContextWM [301]|2023|✓|RSSM|DMC + CARLA + Meta-world|✓|
||iVideoGPT [302]|2023|✓<br>✓<br>✓|✓<br>✓<br>AutoreGressive Transformer|Robotic arm|✓|
||DWL [401]|2024|✓|Recurrent encoder|Humanoid robot|✗|
||Surfer [402]|2024|✓<br>✓<br>✓|Transformer|Robotic arm|✓|
||GAS [403]|2024|✓|RSSM|Surgical robot|✓|
||Puppeteer [404]|2024|✓<br>✓|TD-MPC2|Simulation (56-DoF humanoid)|✓|
||TWIST [405]|2024|✓|RSSM|Robotic arm|✗|
||PIVOT-R [406]|2024|✓<br>✓<br>✓|Transformer|Robotic arm|✓|
||HarmonyDream [407]|2024|✓|RSSM|Robotic arm|✓|
||SafeDreamer [408]|2024|✓|✓<br>OSRP|simulation (Safety-Gymnasium)|✓|
||WMP [409]|2024|✓|✓<br>RSSM|Quadruped robot|✓|
||RWM [410]|2025|✓|✓<br>GRU+MLP|Quadruped robot|✗|
||RWM-O [411]|2025|✓|GRU+MLP|Robotic arm|✗|
||SSWM [412]|2025|✓|SSM|Quadrotor|✗|
||WMR [413]|2025|✓|LSTM|Humanoid robot|✗|
||PIN-WM [414]|2025|✓|GS reconstruction|Robotic arm|_◦_|
||LUMOS [415]|2025|✓<br>✓|RSSM|Robotic arm|✓|
||OSVI-WM [416]|2025|✓|Transformer|Robotic arm|✗|
||FOCUS [417]|2025|✓<br>✓|RSSM|Robotic arm|✓|
||FLIP [418]|2025|✓<br>✓|DiT|Robotic arm|✓|
||EnerVerse-AC [419]|2025|✓<br>✓|✓<br>Diffusion|Robotic arm|✓|
||FlowDreamer [420]|2025|✓|✓<br>✓<br>Diffusion|Robotic arm|_◦_|
||HWM [421]|2025|✓|MVM + FM|Humanoid robot|✗|
||MoDemV2 [422]|2023|✓<br>✓|RSSM|Robotic arm|✓|
||V-JEPA 2 [275]|2025|✓<br>✓|✓<br>JEPA|Robotic arm|✓|
||<br>AdaWorld [423]|2025|✓|DiT|Robotic arm|✓|


> 1 Geometry means 3D geometric representation, which includes: 3D voxel occupancy, 3D bounding box, 3D depth, 3D segmentation and 3D point cloud. 

> 2 DiT = Diffusion Transformers; RSSM = Recurrent State-Space Model; TSSM = Transformer State-Space Model; SSM = State-Space Model; TD-MPC = Temporal Difference learning for Model Predictive Control; OSRP = online safety-reward planning; GRU = Gated Recurrent Unit; MLP = Multilayer Perceptron; LSTM = Long Short-Term Memory; GS = Gaussian Splatting; MVM = Masked Video Modelling; FM = Flow Matching; JEPA = Joint Embedding-Predictive Architecture. 

> 3 DMC = DeepMind Control suite (Simulation). 

> 4 Code availability: ”✗” means code is not announced to be released in the paper, ”✓” means code is released, ” _◦_ ” means code is announced to be released in the paper, but the full code (training and inference) is not yet available. 

34 

TABLE 7: Comparison of Researches for World Models in Robotics (Part II) 

|||||**Input**||||
|---|---|---|---|---|---|---|---|
|**Category**|**Paper**|**Year**|Image<br>Proprioception|Text<br>Action|**Architecture**<sup>2</sup><br>Geometry<br>1<br>Tactile|**Experiments**<sup>3</sup>|**Code**<br>**Availability**<br>4|
|**Di**|MoSim [424]|2025|✓|✓|rigid-body dynamics + ODE|Robotic arm|✓|
|**ynamcs**<br>**Models**|DALI [425]|2025|✓<br>✓|✓|RSSM|DMC|✓|
||GWM [426]|2025|✓|✓|DiT|Robotic arm|✓|
|**Reward**<br>|VIPER [427]|2023|✓<br>✓|✓|Autoregressive Transformer|DMC + RLBench + Atari|✓|
|**Models**|PlaNet [267]|2018|✓||RSSM|DMC|✓|


> 1 Geometry means 3D geometric representation, which includes: 3D voxel occupancy, 3D bounding box, 3D depth, 3D segmentation and 3D point cloud. 

> 2 DiT = Diffusion Transformers; RSSM = Recurrent State-Space Model; TSSM = Transformer State-Space Model; SSM = State-Space Model; TD-MPC = Temporal Difference learning for Model Predictive Control; OSRP = online safety-reward planning; GRU = Gated Recurrent Unit; MLP = Multilayer Percentron; LSTM = Long Short-Term Memory; GS = Gaussian Splatting; MVM = Masked Video Modelling; FM = Flow Matching; JEPA = Joint Embedding-Predictive Architecture. 

> 3 DMC = DeepMind Control suite (Simulation). 

> 4 Code availability: ”✗” means code is not announced to be released in the paper, ”✓” means code is released, ” _◦_ ” means code is announced to be released in the paper, but the full code (training and inference) is not yet available. 

relation and outperforming real-to-sim methods. 

Huawei Cloud’s **Pangu** World Model [387] is a neural simulator that synthesizes high-fidelity digital environments (e.g., camera videos, LiDAR point clouds) for training intelligent driving and embodied AI systems. By modeling physical dynamics and multimodal sensor data, it bypasses costly real-world data collection. Integrated with GAC Group, it enables rapid corner-case generation and 2Dto-3D pixel mapping. The CloudRobo Platform extends this with embodied AI models (generation, planning, execution) and R2C Protocol standardization, aiming to unify robotics development via cloud-based simulation and deployment. 

**RoboTransfer** [388] proposes a geometry-consistent video diffusion framework for robotic visual policy transfer, integrating multi-view geometry with explicit scene control. By enforcing cross-view feature interactions and depth/normal conditions, it synthesizes geometrically consistent multi-view videos, improving sim-to-real policy performance. The method enables fine-grained scene editing while maintaining visual fidelity. 

### _6.2.2 WMs as Dynamic Models for Articulated Robots_ 

World models serve as dynamic models in model-based reinforcement learning (MBRL) by learning predictive representations of environmental dynamics from observed data. Instead of relying on handcrafted physics engines or sparse reward signals, these models enable agents to simulate future states and plan actions through imagined rollouts. PlaNet was one of the earliest to use the RSSM architecture, as shown in Fig. 24. The Dreamer series exemplifies this approach by learning latent-state dynamics from highdimensional observations using variational autoencoders and RSSM. Extensions like TransDreamer replace RNNs with Transformers to better capture long-range dependencies, while ContextWM and iVideoGPT explore pretraining on real-world videos and discrete token-based modeling, respectively. These advancements enhance generalization, long-horizon prediction, and transferability across tasks. By decoupling perception and planning, world models reduce sample complexity and improve decision-making in complex, high-dimensional environments. Recent work further 

demonstrates their real-world applicability, validating their potential for robotics and autonomous systems. 

**PlaNet** [429] presents a latent dynamic model for pixelbased planning, combining deterministic and stochastic transitions with latent overshooting for multi-step prediction. It solves complex continuous control tasks with fewer episodes than model-free methods, demonstrating high sample efficiency in unknown environments. 

**Plan2Explore** [262] introduces a self-supervised reinforcement learning agent that leverages model-based planning to actively seek future novelty during exploration, enabling zero or few-shot adaptation to unseen tasks. It outperforms prior methods in high-dimensional image-based control tasks without task-specific supervision, approaching oracle-level performance. 

The **Dreamer series** does a lot in world model and has discussed it in Chapter. 5.2.2. For example, **DreamerV3** [300] presents a generalist reinforcement learning algorithm that learns a world model to imagine future scenarios, achieving state-of-the-art performance across 150+ diverse tasks with a single configuration. Its robustness techniques enable stable cross-domain learning, demonstrated by first achieving diamond collection in Minecraft without human data or curricula. 

**Dreaming** [395] eliminates Dreamer’s decoder to mitigate object vanishing, employing a likelihood-free InfoMax contrastive objective with linear dynamics and data augmentation, achieving top performance on 5 robotics tasks. **DreamingV2** [396] advances this by fusing DreamerV2’s discrete latent states with Dreaming’s reconstruction-free learning, creating a hybrid world model that leverages categorical state representation for complex environments and contrastive vision modeling, excelling in 3D robotic arm tasks without reconstruction. 

**DreamerPro** [397] enhances MBRL robustness to visual distractions by integrating prototypical representations into Dreamer’s world model, distilling temporal structures from recurrent states. This approach improves performance on DeepMind Control tasks with complex backgrounds, outperforming contrastive methods in both standard and dis- 

35 


Fig. 24: Latent dynamic models employ distinct transition mechanisms for temporal prediction. (a) RNN-based models use deterministic transitions, limiting multi-modal future prediction and enabling planner exploitation. (b) State-space models (SSM) rely solely on stochastic transitions, hindering long-term memory retention. (c) RSSM combines stochastic and deterministic state components, balancing multi-future prediction with temporal coherence. This hybrid approach enhances robustness in learning diverse futures while maintaining sequential consistency, as demonstrated in [429]. 

### traction settings. 

**LEXA** [398] introduces a unified framework for unsupervised goal-reaching, combining world model-based imagined rollouts with foresight-driven exploration to discover novel states and achieve diverse tasks. It outperforms prior methods on 40 challenging robotic tasks, demonstrating zero-shot generalization and scalability across multiple environments. 

**FOWM** [399] proposes a framework combining offline world model pretraining with online finetuning, using epistemic uncertainty regularization to mitigate extrapolation errors. It enables few-shot adaptation to seen/unseen visuomotor tasks with limited offline data, validated on simulation and real-world robotic control benchmarks. 

**SWIM** [400] proposes an affordance-space world model for robotic manipulation, trained on human videos and finetuned with minimal robot data. The model learns structured action representations from human-object interactions, enabling rapid skill acquisition (¡30min) across diverse tasks and robots without task-specific supervision. 

**DWL** [401] is an end-to-end RL framework for humanoid locomotion. The world model enables zero-shot sim-to-real transfer, mastering diverse challenging terrains (snow, stairs, uneven ground) with a single policy. The approach demonstrates robustness and generalization without environment-specific tuning. 

**Surfer** [402] introduces a world model-based framework for robot manipulation, decoupling action and scene prediction to enhance generalization in multi-modal tasks. It incorporates explicit world knowledge modeling and is evaluated on SeaWave benchmark, achieving 54.74 % success rate, outperforming baselines by modeling physicsbased state transitions. 

**GAS** [403] proposes a world-model-based deep reinforcement learning framework tailored for surgical robotic manipulation, employing pixel-level visuomotor policies with uncertainty-aware depth estimation and compact 3- channel image encoding. It achieves a 69% success rate in handling unseen objects and disturbances within real-world surgical environments, demonstrating superior robustness 

and generalization compared to prior methods in clinical settings. 

**Puppeteer** [404] presents a hierarchical world model for visual whole-body humanoid control, where a highlevel visual policy generates commands for a low-level execution policy, both trained via reinforcement learning. The approach achieves high-performance motion synthesis across 8 tasks for a 56-DoF humanoid without simplifying assumptions or reward engineering. 

**TWIST** [405] proposes a teacher-student world model distillation framework for efficient sim-to-real transfer in vision-based model-based RL. It leverages state-privileged teacher models to supervise image-based student models, accelerating adaptation while bridging the sim-to-real gap through domain-randomized distillation, outperforming naive methods in sample efficiency and task performance. 

**PIVOT-R** [406] proposes a primitive-driven waypointaware world model (WAWM) for language-guided robotic manipulation, decoupling waypoint prediction from action execution with an asynchronous hierarchical executor (AHE). It achieves 19.45% relative improvement on SeaWave benchmark while improving efficiency by 28× with minimal performance trade-off. 

**HarmonyDream** [407] proposes a task harmonization framework for world models, dynamically balancing observation and reward modeling losses to enhance sampleefficient MBRL. It achieves 10%-69% performance gains on visual robotic tasks and sets a new Atari 100K benchmark record by resolving task dominance issues in world model learning. 

**SafeDreamer** [408] integrates Lagrangian-based methods with world model planning in the Dreamer framework to enhance safe reinforcement learning. The approach achieves near-zero-cost performance on Safety-Gymnasium tasks, demonstrating effective balance between performance and safety for both low-dimensional and vision-only inputs through improved model accuracy and sample efficiency. 

**WMP** [409] proposes a world model-based perception framework for legged locomotion, eliminating privileged 

36 

information reliance by learning policies from simulated world model predictions. It achieves state-of-the-art realworld traversability and robustness through cross-domain generalization, validated in simulation and physical environments. 

**RWM** [410] introduces a neural network-based robotic world model with dual-autoregressive mechanisms for long-horizon dynamics prediction. The framework enables self-supervised training and robust policy optimization through imagined environments, addressing challenges in partial observability and sim-to-real transfer without domain-specific biases. 

**RWM-O** [411] introduces an offline robotic world model with explicit epistemic uncertainty estimation, penalizing unreliable transitions to enhance policy stability and generalization. Validated in real-world data settings, it reduces sim-to-real gaps and improves safety without physics simulators, outperforming conventional MBRL methods. 

**SSWM** [430], state-space world models, was used to accelerate model-based reinforcement learning (MBRL). The approach parallelizes dynamic model training and utilizes privileged information, achieving up to 10 times faster world model training and 4 times overall MBRL speedup while maintaining performance in complex quadrotor flight tasks with partial observability. 

**WMR** [413] proposes an end-to-end world model reconstruction framework for blind humanoid locomotion, explicitly reconstructing world states to enhance policy robustness. Gradient cutoff ensures independent state reconstruction, enabling adaptive locomotion on complex terrains, validated by 3.2 km hikes across ice, snow, and deformable surfaces. 

**PIN-WM** [414] presents a physics-informed world model for non-prehensile manipulation, enabling end-toend 3D rigid body dynamics learning from few-shot visual trajectories via differentiable simulation. It eliminates state estimation with Gaussian Splatting-based observational loss and bridges Sim2Real gaps through physics-aware digital cousins, achieving robust policy transfer. 

**LUMOS** [415] introduces a language-conditioned imitation learning framework leveraging world models for latent-space skill practice. The approach combines latent planning with hindsight goal relabeling and intrinsic rewards, enabling zero-shot transfer to real robots. It demonstrates superior performance on long-horizon tasks while mitigating policy-induced distribution shift in offline settings. 

**OSVI-WM** [432] proposes a one-shot visual imitation learning framework using world-model-guided trajectory generation. A learned world model predicts latent states and actions from demonstrations, decoded into physical waypoints for execution. Evaluated across simulated and real robotic platforms, the method achieves over 30% improvement compared to prior approaches. 

**FOCUS** [417] introduces an object-centric world model for robotic manipulation, representing scenes through structured object interactions. The framework enables object-centric exploration and improves manipulation skills through more accurate scene predictions. Evaluated on robotic tasks, it demonstrates efficient learning and adapta- 

tion to sparse-reward scenarios using a Franka Emika robot arm. 

**FLIP** [418] presents a flow-centric model-based planning framework for language-vision manipulation, integrating multi-modal flow generation, flow-conditioned video dynamics, and vision-language representation modules. It synthesizes long-horizon plans via image flows, guiding lowlevel policy training with interactive world model properties, validated on diverse benchmarks. 

**EnerVerse-AC** [419] proposes an action-conditional world model for robotic evaluation, featuring multi-level action-conditioning and ray map encoding to generate dynamic multi-view observations. The model serves as both data engine and evaluator, synthesizing realistic actionconditioned videos from human-collected trajectories to enable cost-effective policy testing without physical robots or complex simulations. 

**FlowDreamer** [420] proposes an RGB-D world model using explicit 3D scene flow representations for visual prediction and planning. It decouples motion estimation (UNet) and frame synthesis (diffusion model) while maintaining end-to-end training, outperforming baselines by 7-11% in semantic quality and success rate across manipulation benchmarks. 

**HWM** [421] introduces lightweight video-based world models for humanoid robotics, employing Masked Transformers and FlowMatching to forecast action-conditioned egocentric observations. The framework demonstrates efficient parameter sharing strategies, reducing model size by 33%-53% while maintaining performance, enabling practical deployment in resource-constrained academic settings. 

**MoDem-V2** [422] enables real-world contact-rich manipulation learning via a model-based reinforcement learning framework that integrates demonstration bootstrapping and safety-aware exploration strategies (exploration centering, agency handover, actor-critic ensembles), achieving the first successful direct real-world training of vision-based MBRL systems without instrumentation. 

**V-JEPA 2** [275] is a 1.2B-parameter world model employing joint-embedding predictive architecture for videobased understanding, prediction and zero-shot planning. The model undergoes two-stage training: actionless pretraining on 1M+ video hours for physical intuition, followed by action-conditioned fine-tuning with minimal robot data (62 hours). Demonstrating state-of-the-art performance on action recognition and anticipation tasks, V-JEPA 2 enables model-predictive control for robotic tasks (65%-80% success in novel environments) through visual subgoal planning. The framework includes three new benchmarks for evaluating physical reasoning capabilities. 

### _6.2.3 WMs as Reward models for Articulated Robots_ 

A world model as a reward model leverages its learned dynamics to implicitly infer rewards by measuring how well an agent’s behavior aligns with the model’s predictions. For instance, if trajectories are highly predictable (i.e., match the world model’s expectations), they are assigned higher rewards, eliminating manual reward engineering. 

Unlike Dreamer, which implicitly replaces the reward signal through the value function, **PlaNet** uses an explicitly learned reward predictor. Its Reward Predictor, as part of 

37 


Fig. 25: Self-supervised learning architectures employ distinct approaches to model input compatibility: (a) JointEmbedding aligns embeddings of compatible inputs; (b) Generative reconstructs signals via latent-conditioned decoders; (c) Joint-Embedding Predictive forecasts embeddings using latent-conditioned predictors. Each framework optimizes energy assignments—low for compatible, high for incompatible inputs [431]. 

the dynamics model, is responsible for predicting environmental rewards from compressed latent states, training by minimizing the error between the predicted reward and the true reward, and providing immediate reward signals for multi-step trajectory rolling in the latent space during the online planning stage, thereby replacing the hand-designed reward function. 

Such approaches unify environment simulation and reward generation, enabling scalable RL from raw observations. This paradigm is particularly powerful for transfer learning, as seen in VIPER’s cross-embodiment generalization. 

**VIPER** [427] proposes using pretrained video prediction models as reward signals for reinforcement learning. The method trains an autoregressive transformer on expert videos and utilizes prediction likelihoods as rewards, enabling expert-level control without task-specific rewards across DMC, Atari and RLBench tasks, while supporting cross-embodiment generalization in tabletop manipulation scenarios. 

Key directions include: Modular architectures with shared physical priors for transferable dynamics learning; Metareinforcement learning for rapid adaptation to new hardware/task combinations; Object-centric representations enabling skill reuse across scenarios; and Sim-to-real bridges via residual physics modeling. These advances aim to create ”one model fits all” solutions for scalable robotic intelligence. 

**Hierarchical World Models for Long-Horizon Task** . Future robotics world models will focus on hierarchical planning and temporal abstraction to handle complex, multistage tasks. Key advancements include: Goal-conditioned latent spaces for dynamic sub-task chaining; Memoryaugmented transformers to capture long-term dependencies; Self-supervised skill discovery for reusable primitives; and Interactive human feedback for real-time plan adaptation. These innovations aim to bridge high-level reasoning with low-level control, enabling robust autonomy in openended environments. 

### **6.3 Challenges and Future Perspectives** 

### _6.2.4 Technical Trends_ 

The world model has broad development prospects in the future, but in the field of robotics, it may have the following development potential: 

**Tactile-Enhanced World Models for Dexterous Manipulation** . The evolution of tactile-integrated world models is enabling breakthroughs in robotic dexterity, particularly for multi-fingered hands. Cutting-edge approaches now combine high-resolution contact modeling with visuotactile fusion, using neural networks to predict slip, deformation, and optimal grip forces in real time. Selfsupervised tactile encoders eliminate manual labeling by autonomously learning material and shape representations, while graph/transformer architectures process dynamic spatiotemporal touch signals. These innovations allow robots to handle novel objects with human-like adaptability, overcoming traditional sim-to-real challenges in delicate manipulation tasks. 

**Unified World Models for Cross-Hardware and CrossTask Generalization** . Future robotics world models will focus on hardware-agnostic dynamics encoding and taskadaptive latent spaces to generalize across diverse embodiments (e.g., single/double arms, legged/wheeled robots) and tasks (e.g., gripper vs. dexterous-hand manipulation). 

**High-Dimensionality and Partial Observability** . Autonomous systems operate on high-dimensional sensory inputs, such as camera images, LiDAR point clouds, and radar signals. Modeling the world from this data imposes significant computational demands. Furthermore, these observations are inherently partial; the agent never perceives the complete state of the environment. This partial observability introduces uncertainty, necessitating robust state estimation techniques or the maintenance of a belief state over possible world states to inform decision-making. 

**Causal Reasoning versus Correlation Learning** . A fundamental limitation of many current world models is their proficiency at learning correlations rather than causal relationships. For instance, a model can learn that brake lights correlate with deceleration but may lack a deeper understanding of the underlying physics and driver intent. This deficiency hinders true generalization, as it prevents the model from performing counterfactual reasoning—evaluating ”what if” scenarios that deviate from the training distribution. Achieving robust performance in novel situations requires a transition from correlational pattern matching to a genuine causal understanding of the environment. 

38 

**Abstract and Semantic Understanding** . Effective world models must transcend low-level signal prediction and operate on a higher level of semantic and abstract understanding. A robust model should not merely predict future pixels or LiDAR points but also reason about abstract concepts. A major open problem lies in the fusion of fine-grained physical predictions with abstract reasoning about concepts such as traffic laws, pedestrian intent, and object affordances (e.g., that a chair is for sitting). Integrating these different levels of abstraction is crucial for intelligent and contextaware behavior. 

**Systematic Evaluation and Benchmarking** . The objective evaluation and comparison of world models present a significant research challenge. Conventional metrics like Mean Squared Error on future predictions are often insufficient, as they may not correlate with the performance of downstream tasks. A model generating visually sharper predictions might not necessarily enable a safer or more efficient control policy. The development of new evaluation frameworks is needed, with metrics that assess the model’s utility for planning, its robustness in safety-critical scenarios, and its ability to capture causally relevant aspects of the environment. 

**Memory Architecture and Long-Term Dependencies** . Accurate long-term forecasting is notoriously difficult due to the compounding of prediction errors and the stochastic nature of the real world. A critical challenge is the design of memory architectures capable of retaining and retrieving relevant information over extended timescales, such as remembering a ”Road Work Ahead” sign seen several minutes prior. The development of efficient and effective memory systems, leveraging architectures like Transformers or StateSpace Models (SSMs), to manage these long-term dependencies remains an active and contested area of research. 

**Human Interaction and Predictability** . For agents operating in human-centric environments, a world model’s role extends beyond mere environmental prediction. It must also facilitate agent behavior that is legible, predictable, and socially compliant to humans. Actions that are technically optimal but appear erratic or counter-intuitive can confuse human counterparts, such as other drivers or pedestrians, potentially leading to unsafe interactions. This social intelligence layer is a subtle but critical component of a functional world model. 

**Interpretability and Verifiability** . Deep learning-based world models are often opaque ”black boxes,” making it difficult to discern the rationale behind their predictions. For safety-critical applications like autonomous driving, the ability to audit and understand the model’s internal decision-making process is non-negotiable, especially during post-incident analysis. Furthermore, a formidable theoretical and engineering challenge is the formal verification of these models—mathematically proving that they satisfy crucial safety properties (e.g., never hallucinating hazardous obstacles) across the vast space of possible inputs. 

**Compositional Generalization and Abstraction** . While the sim-to-real gap is a well-known generalization problem, a deeper challenge is compositional generalization. Humans can learn discrete concepts like ”cup” and ”table” and immediately generalize to novel compositions, such as ”a cup on a table.” In contrast, current models often require 

extensive exposure to specific compositional examples. An ideal world model should learn disentangled, abstract representations of entities, their relations, and their physical properties. This would enable it to understand and predict novel scenarios by composing known concepts, rather than relying on end-to-end pattern matching of entire scenes. 

**Data Curation and Bias** . The performance of a world model is fundamentally contingent on the quality and composition of its training data. Models inevitably inherit and may even amplify biases present in the dataset. For instance, a model trained predominantly on data from one geographical region may underperform in another with different road conventions or environmental conditions. A critical aspect of data curation is addressing the ”long tail” of rare but safety-critical events. Systematically identifying, collecting, and ensuring the model learns effectively from these infrequent scenarios is essential for building robust and reliable systems. 

## **7 CONCLUSION** 

This survey has provided a comprehensive examination of the critical role that physical simulators and world models play in advancing embodied artificial intelligence, revealing a transformative paradigm shift toward truly intelligent robotic systems. Through our analysis, we introduced a five-level classification framework (IR-L0 to IR-L4) for evaluating robot autonomy, conducted extensive comparative studies of mainstream simulation platforms, and explored the evolution of world models from simple recurrent architectures to sophisticated foundation-scale systems. Our investigation demonstrates how modern simulators like Isaac Gym, Genesis, and the emerging Newton platform have revolutionized robot learning through GPU-accelerated physics and photorealistic rendering, while advanced world models have enabled unprecedented capabilities in both autonomous driving and articulated robotics. 

These technologies has not only mitigated the sim-toreal gap but has also unlocked new possibilities for sampleefficient learning, long-horizon planning, and robust generalization across diverse environments. As we advance toward the realization of IR-L4 fully autonomous systems, the integration of physical simulators and world models represents the foundation upon which the next generation of embodied intelligence will be built, promising to transform robotics from task-specific automation to general-purpose intelligence capable of seamless integration into human society. 

## **REFERENCES** 

- [1] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat _et al._ , “Gpt-4 technical report,” _arXiv preprint arXiv:2303.08774_ , 2023. 

- [2] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan _et al._ , “Deepseek-v3 technical report,” _arXiv preprint arXiv:2412.19437_ , 2024. 

- [3] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , p. 02783649241273668, 2023. 

39 

- [4] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [5] Y. Tong, H. Liu, and Z. Zhang, “Advancements in humanoid robots: A comprehensive review and future prospects,” _IEEE/CAA Journal of Automatica Sinica_ , vol. 11, no. 2, pp. 301–328, 2024. 

- [6] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

- [7] J. Broekens, M. Heerink, H. Rosendal _et al._ , “Assistive social robots in elderly care: a review,” _Gerontechnology_ , vol. 8, no. 2, pp. 94–103, 2009. 

- [8] P. E. Dupont, B. J. Nelson, M. Goldfarb, B. Hannaford, A. Menciassi, M. K. O’Malley, N. Simaan, P. Valdastri, and G.-Z. Yang, “A decade retrospective of medical robotics research from 2010 to 2020,” _Science robotics_ , vol. 6, no. 60, p. eabi8017, 2021. 

- [9] R. R. Murphy, S. Tadokoro, and A. Kleiner, “Disaster robotics,” in _Springer handbook of robotics_ . Springer, 2016, pp. 1577–1604. 

- [10] T. Belpaeme, J. Kennedy, A. Ramachandran, B. Scassellati, and F. Tanaka, “Social robots for education: A review,” _Science robotics_ , vol. 3, no. 21, p. eaat5954, 2018. 

- [11] E. Krotkov, D. Hackett, L. Jackel, M. Perschbacher, J. Pippine, J. Strauss, G. Pratt, and C. Orlowski, “The darpa robotics challenge finals: Results and perspectives,” _Journal of Field Robotics_ , vol. 34, no. 2, pp. 229–240, 2016. 

- [12] _Robots and robotic devices—Safety requirements for personal care robots_ , ISO Std. 13 482, 2014. 

- [13] H.-M. Huang, K. Pavek, B. Novak, J. Albus, and E. Messin, “A framework for autonomy levels for unmanned systems (alfus),” _Proceedings of the AUVSI’s unmanned systems North America_ , pp. 849–863, 2005. 

- [14] J. M. Beer, A. D. Fisk, and W. A. Rogers, “Toward a framework for levels of robot autonomy in human-robot interaction,” _Journal of human-robot interaction_ , vol. 3, no. 2, p. 74, 2014. 

- [15] N. Koenig and A. Howard, “Design and use paradigms for gazebo, an open-source multi-robot simulator,” in _2004 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) (IEEE Cat. No.04CH37566)_ , vol. 3, 2004, pp. 2149–2154 vol.3. 

- [16] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2012, pp. 5026–5033. 

- [17] NVIDIA. (n.d.) World models. Accessed: 2025-05-24. [Online]. Available: https://www.nvidia.com/en-us/glossary/world-m odels/ 

- [18] D. Ha and J. Schmidhuber, “World models,” _arXiv preprint arXiv:1803.10122_ , 2018. 

- [19] J. Duan, S. Yu, H. L. Tan, H. Zhu, and C. Tan, “A survey of embodied ai: From simulators to research tasks,” _IEEE Transactions on Emerging Topics in Computational Intelligence_ , vol. 6, no. 2, pp. 230–244, 2022. 

- [20] Y. Liu, W. Chen, Y. Bai, X. Liang, G. Li, W. Gao, and L. Lin, “Aligning cyber space with physical world: A comprehensive survey on embodied ai,” _arXiv preprint arXiv:2407.06886_ , 2024. 

- [21] J. Collins, S. Chand, A. Vanderkop, and D. Howard, “A review of physics simulators for robotic applications,” _IEEE Access_ , vol. 9, pp. 51 416–51 431, 2021. 

- [22] Z. Zhu, X. Wang, W. Zhao, C. Min, N. Deng, M. Dou, Y. Wang, B. Shi, K. Wang, C. Zhang _et al._ , “Is sora a world simulator? a comprehensive survey on general world models and beyond,” _arXiv preprint arXiv:2405.03520_ , 2024. 

- [23] J. Ding, Y. Zhang, Y. Shang, Y. Zhang, Z. Zong, J. Feng, Y. Yuan, H. Su, N. Li, N. Sukiennik _et al._ , “Understanding world or predicting future? a comprehensive survey of world models,” _arXiv preprint arXiv:2411.14499_ , 2024. 

- [24] X. Mai, Z. Tao, J. Lin, H. Wang, Y. Chang, Y. Kang, Y. Wang, and W. Zhang, “From efficient multimodal models to world models: A survey,” _arXiv preprint arXiv:2407.00118_ , 2024. 

- [25] B. Siciliano and O. Khatib, _Robotics: Modelling, Planning and Control_ . Springer, 2010. 

- [26] R. R. Murphy, _Introduction to AI robotics_ . MIT press, 2019. [27] M. Colledanchise and P. Ogren,<sup>¨</sup> “Behavior trees in robotics and ai: An introduction,” _arXiv preprint arXiv:1709.00084_ , 2017. 

- [28] J. B. Rawlings, D. Q. Mayne, M. Diehl _et al._ , _Model predictive control: theory, computation, and design_ . Nob Hill Publishing Madison, WI, 2017, vol. 2. 

- [29] S. Katayama, M. Murooka, and Y. Tazaki, “Model predictive control of legged and humanoid robots: models and algorithms,” _Advanced Robotics_ , vol. 37, no. 5, pp. 298–315, 2023. 

- [30] T. Erez, K. Lowrey, Y. Tassa, V. Kumar, S. Kolev, and E. Todorov, “An integrated system for real-time model predictive control of humanoid robots,” in _2013 13th IEEE-RAS International conference on humanoid robots (Humanoids)_ . IEEE, 2013, pp. 292–299. 

- [31] J. Koenemann, A. Del Prete, Y. Tassa, E. Todorov, O. Stasse, M. Bennewitz, and N. Mansard, “Whole-body model-predictive control applied to the hrp-2 humanoid,” in _2015 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2015, pp. 3346–3351. 

- [32] A. Goswami and P. Vadakkepat, _Humanoid robotics: a reference_ . Springer Dordrecht, 2019. 

- [33] L. Sentis and O. Khatib, “A whole-body control framework for humanoids operating in human environments,” in _Proceedings 2006 IEEE International Conference on Robotics and Automation, 2006. ICRA 2006._ IEEE, 2006, pp. 2641–2648. 

- [34] A. Escande, N. Mansard, and P.-B. Wieber, “Hierarchical quadratic programming: Fast online humanoid-robot motion generation,” _The International Journal of Robotics Research_ , vol. 33, no. 7, pp. 1006–1028, 2014. 

- [35] S. Kuindersma, R. Deits, M. Fallon, A. Valenzuela, H. Dai, F. Permenter, T. Koolen, P. Marion, and R. Tedrake, “Optimizationbased locomotion planning, estimation, and control design for the atlas humanoid robot,” _Autonomous robots_ , vol. 40, pp. 429– 455, 2016. 

- [36] M. A. Hopkins, D. W. Hong, and A. Leonessa, “Compliant locomotion using whole-body control and divergent component of motion tracking,” in _2015 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2015, pp. 5726–5733. 

- [37] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [38] Y. Xue, W. Dong, M. Liu, W. Zhang, and J. Pang, “A unified and general humanoid whole-body controller for fine-grained locomotion,” _arXiv preprint arXiv:2502.03206_ , 2025. 

- [39] J. Kober, J. A. Bagnell, and J. Peters, “Reinforcement learning in robotics: A survey,” _The International Journal of Robotics Research_ , vol. 32, no. 11, pp. 1238–1274, 2013. 

- [40] D. Nguyen-Tuong and J. Peters, “Model learning for robot control: a survey,” _Cognitive processing_ , vol. 12, pp. 319–340, 2011. 

- [41] J. Yamaguchi, E. Soga, S. Inoue, and A. Takanishi, “Development of a bipedal humanoid robot-control method of whole body cooperative dynamic biped walking,” in _Proceedings 1999 IEEE International Conference on Robotics and Automation (Cat. No. 99CH36288C)_ , vol. 1. IEEE, 1999, pp. 368–374. 

- [42] S. Ha, J. Lee, M. van de Panne, Z. Xie, W. Yu, and M. Khadiv, “Learning-based legged locomotion: State of the art and future perspectives,” _The International Journal of Robotics Research_ , p. 02783649241312698, 2024. 

- [43] J. Morimoto and K. Doya, “Reinforcement learning of dynamic motor sequence: Learning to stand up,” in _Proceedings. 1998 IEEE/RSJ International Conference on Intelligent Robots and Systems. Innovations in Theory, Practice and Applications (Cat. No. 98CH36190)_ , vol. 3. IEEE, 1998, pp. 1721–1726. 

- [44] X. B. Peng, G. Berseth, K. Yin, and M. Van De Panne, “Deeploco: Dynamic locomotion skills using hierarchical deep reinforcement learning,” _Acm transactions on graphics (tog)_ , vol. 36, no. 4, pp. 1– 13, 2017. 

- [45] W. Yu, G. Turk, and C. K. Liu, “Learning symmetric and lowenergy locomotion,” _ACM Transactions on Graphics (TOG)_ , vol. 37, no. 4, pp. 1–12, 2018. 

- [46] N. Heess, D. Tb, S. Sriram, J. Lemmon, J. Merel, G. Wayne, Y. Tassa, T. Erez, Z. Wang, S. Eslami _et al._ , “Emergence of locomotion behaviours in rich environments,” _arXiv preprint arXiv:1707.02286_ , 2017. 

- [47] Z. Xie, P. Clary, J. Dao, P. Morais, J. Hurst, and M. van de Panne, “Iterative reinforcement learning based design of dynamic locomotion skills for cassie,” _arXiv preprint arXiv:1903.09537_ , 2019. 

- [48] Y. Ze, G. Zhang, K. Zhang, C. Hu, M. Wang, and H. Xu, “3d diffusion policy,” _arXiv e-prints_ , pp. arXiv–2403, 2024. 

- [49] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning finegrained bimanual manipulation with low-cost hardware,” _arXiv preprint arXiv:2304.13705_ , 2023. 

40 

- [50] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _arXiv preprint arXiv:2410.07864_ , 2024. 

- [51] X. Huang, Y. Chi, R. Wang, Z. Li, X. B. Peng, S. Shao, B. Nikolic, and K. Sreenath, “Diffuseloco: Real-time legged locomotion control with diffusion from offline datasets,” _arXiv preprint arXiv:2404.19264_ , 2024. 

- [52] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [53] Q. Zhang, P. Cui, D. Yan, J. Sun, Y. Duan, G. Han, W. Zhao, W. Zhang, Y. Guo, A. Zhang _et al._ , “Whole-body humanoid robot locomotion with human reference,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 225–11 231. 

- [54] C. Wang, H. Shi, W. Wang, R. Zhang, L. Fei-Fei, and C. K. Liu, “Dexcap: Scalable and portable mocap data collection system for dexterous manipulation,” _arXiv preprint arXiv:2403.07788_ , 2024. 

- [55] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang, “Open-television: Teleoperation with immersive active visual feedback,” _arXiv preprint arXiv:2407.01512_ , 2024. 

- [56] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa, “Visual imitation enables contextual humanoid control,” _arXiv preprint arXiv:2505.03729_ , 2025. 

- [57] S.-H. Hyon, “Compliant terrain adaptation for biped humanoids without measuring ground surface and contact forces,” _IEEE Transactions on Robotics_ , vol. 25, no. 1, pp. 171–178, 2008. 

- [58] S.-J. Yi, B.-T. Zhang, D. Hong, and D. D. Lee, “Practical bipedal walking control on uneven terrain using surface learning and push recovery,” in _2011 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2011, pp. 3963–3968. 

- [59] J. Reher, W.-L. Ma, and A. D. Ames, “Dynamic walking with compliance on a cassie bipedal robot,” in _2019 18th European Control Conference (ECC)_ . IEEE, 2019, pp. 2589–2595. 

- [60] G. Mesesan, J. Englsberger, G. Garofalo, C. Ott, and A. AlbuSch¨affer, “Dynamic walking on compliant and uneven terrain using dcm and passivity-based whole-body control,” in _2019 IEEERAS 19th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2019, pp. 25–32. 

- [61] J. Siekmann, K. Green, J. Warila, A. Fern, and J. Hurst, “Blind bipedal stair traversal via sim-to-real reinforcement learning,” in _Robotics: Science and Systems_ , 2021. 

- [62] J.-K. Huang and J. W. Grizzle, “Efficient anytime clf reactive planning system for a bipedal robot on undulating terrain,” _IEEE Transactions on Robotics_ , vol. 39, no. 3, pp. 2093–2110, 2023. 

- [63] H. Duan, B. Pandit, M. S. Gadde, B. Van Marum, J. Dao, C. Kim, and A. Fern, “Learning vision-based bipedal locomotion for challenging terrain,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 56–62. 

- [64] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” _arXiv preprint arXiv:2406.10759_ , 2024. 

- [65] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [66] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: A 3d vision-language-action generative world model,” _arXiv preprint arXiv:2403.09631_ , 2024. 

- [67] J. Yang, R. Tan, Q. Wu, R. Zheng, B. Peng, Y. Liang, Y. Gu, M. Cai, S. Ye, J. Jang _et al._ , “Magma: A foundation model for multimodal ai agents,” _arXiv preprint arXiv:2502.13130_ , 2025. 

- [68] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control, 2024,” _URL https://arxiv. org/abs/2410.24164_ . 

- [69] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

- [70] L. X. Shi, B. Ichter, M. Equi, L. Ke, K. Pertsch, Q. Vuong, J. Tanner, A. Walling, H. Wang, N. Fusai _et al._ , “Hi robot: Open-ended instruction following with hierarchical vision-language-action models,” _arXiv preprint arXiv:2502.19417_ , 2025. 

- [71] J. Wen, Y. Zhu, J. Li, M. Zhu, K. Wu, Z. Xu, R. Cheng, C. Shen, Y. Peng, F. Feng _et al._ , “Tinyvla: Towards fast, data-efficient 

   - vision-language-action models for robotic manipulation,” _arXiv preprint arXiv:2409.12514_ , 2024. 

- [72] R. Sapkota, Y. Cao, K. I. Roumeliotis, and M. Karkee, “Visionlanguage-action models: Concepts, progress, applications and challenges,” _arXiv preprint arXiv:2505.04769_ , 2025. 

- [73] A. Safonova, N. Pollard, and J. K. Hodgins, “Optimizing human motion for the control of a humanoid robot,” _Proc. Applied Mathematics and Applications of Mathematics_ , vol. 78, pp. 18–55, 2003. 

- [74] S. J. Yi, B. T. Zhang, and D. Lee, “Online learning of uneven terrain for humanoid bipedal walking,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 24, no. 1, 2010, pp. 1639– 1644. 

- [75] S. Kajita, M. Morisawa, K. Miura, S. Nakaoka, K. Harada, K. Kaneko, F. Kanehiro, and K. Yokoi, “Biped walking stabilization based on linear inverted pendulum tracking,” in _2010 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2010, pp. 4489–4496. 

- [76] B. J. Stephens and C. G. Atkeson, “Dynamic balance force control for compliant humanoid robots,” in _2010 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2010, pp. 1248– 1255. 

- [77] M. Sombolestan, Y. Chen, and Q. Nguyen, “Adaptive forcebased control for legged robots,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2021, pp. 7440–7447. 

- [78] B. Henze, M. A. Roa, and C. Ott, “Passivity-based whole-body balancing for torque-controlled humanoid robots in multi-contact scenarios,” _The International Journal of Robotics Research_ , vol. 35, no. 12, pp. 1522–1543, 2016. 

- [79] X. Xiong and A. D. Ames, “Bipedal hopping: Reduced-order model embedding via optimization-based control,” in _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2018, pp. 3821–3828. 

- [80] H. Qi, X. Chen, Z. Yu, G. Huang, Y. Liu, L. Meng, and Q. Huang, “Vertical jump of a humanoid robot with cop-guided angular momentum control and impact absorption,” _IEEE Transactions on Robotics_ , vol. 39, no. 4, pp. 3154–3166, 2023. 

- [81] D. Crowley, J. Dao, H. Duan, K. Green, J. Hurst, and A. Fern, “Optimizing bipedal locomotion for the 100m dash with comparison to human running,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 12 205–12 211. 

- [82] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _The International Journal of Robotics Research_ , p. 02783649241285161, 2024. 

- [83] Z. He, J. Wu, J. Zhang, S. Zhang, Y. Shi, H. Liu, L. Sun, Y. Su, and X. Leng, “Cdm-mpc: An integrated dynamic planning and control framework for bipedal robots jumping,” _IEEE Robotics and Automation Letters_ , 2024. 

- [84] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan _et al._ , “Asap: Aligning simulation and realworld physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [85] S. Le Cleac’h, T. A. Howell, S. Yang, C.-Y. Lee, J. Zhang, A. Bishop, M. Schwager, and Z. Manchester, “Fast contact-implicit model predictive control,” _IEEE Transactions on Robotics_ , vol. 40, pp. 1617–1629, 2024. 

- [86] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

- [87] J. Carpentier and P.-B. Wieber, “Recent progress in legged robots locomotion control,” _Current Robotics Reports_ , vol. 2, no. 3, pp. 231–238, 2021. 

- [88] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” _arXiv preprint arXiv:2411.14386_ , 2024. 

- [89] M. Shahbazi, R. Babuˇska, and G. A. Lopes, “Unified modeling and control of walking and running on the spring-loaded inverted pendulum,” _IEEE Transactions on Robotics_ , vol. 32, no. 5, pp. 1178–1195, 2016. 

- [90] J. Pratt, T. Koolen, T. De Boer, J. Rebula, S. Cotton, J. Carff, M. Johnson, and P. Neuhaus, “Capturability-based analysis and control of legged locomotion, part 2: Application to m2v2, a lower-body humanoid,” _The international journal of robotics research_ , vol. 31, no. 10, pp. 1117–1133, 2012. 

- [91] J. Shen and D. Hong, “Convex model predictive control of single rigid body model on so (3) for versatile dynamic legged mo- 

41 

- tions,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 6586–6592. 

- [92] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” in _8th Annual Conference on Robot Learning_ . 

- [93] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “AMASS: Archive of motion capture as surface shapes,” in _International Conference on Computer Vision_ , Oct. 2019, pp. 5442– 5451. 

- [94] A. Escontrela, X. B. Peng, W. Yu, T. Zhang, A. Iscen, K. Goldberg, and P. Abbeel, “Adversarial motion priors make good substitutes for complex reward functions,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2022, pp. 25– 32. 

- [95] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive Whole-Body Control for Humanoid Robots,” in _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, July 2024. 

- [96] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. M. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning,” in _8th Annual Conference on Robot Learning_ . 

- [97] K. Fujiwara, F. Kanehiro, S. Kajita, K. Kaneko, K. Yokoi, and H. Hirukawa, “Ukemi: Falling motion control to minimize damage to biped humanoid robot,” in _IEEE/RSJ international conference on Intelligent robots and systems_ , vol. 3. IEEE, 2002, pp. 2521–2526. 

- [98] K. Fujiwara, F. Kanehiro, S. Kajita, K. Yokoi, H. Saito, K. Harada, K. Kaneko, and H. Hirukawa, “The first human-size humanoid that can fall over safely and stand-up again,” in _Proceedings 2003 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2003)(Cat. No. 03CH37453)_ , vol. 2. IEEE, 2003, pp. 1920– 1926. 

- [99] L. Meng, Z. Yu, X. Chen, W. Zhang, M. Ceccarelli, K. Hashimoto, A. Takanishi, Q. Huang, W. Guo, L. Xie _et al._ , “A falling motion control of humanoid robots based on biomechanical evaluation of falling down of humans,” in _2015 IEEE-RAS 15th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2015, pp. 441– 446. 

- [100] Q. Huang, C. Dong, Z. Yu, X. Chen, Q. Li, H. Chen, and H. Liu, “Resistant compliance control for biped robot inspired by humanlike behavior,” _IEEE/ASME Transactions on Mechatronics_ , vol. 27, no. 5, pp. 3463–3473, 2022. 

- [101] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning humanoid standing-up control across diverse postures,” _arXiv preprint arXiv:2502.08378_ , 2025. 

- [102] P. Chen, Y. Wang, C. Luo, W. Cai, and M. Zhao, “Hifar: Multistage curriculum learning for high-dynamics humanoid fall recovery,” _arXiv preprint arXiv:2502.20061_ , 2025. 

- [103] Z. Zhuang and H. Zhao, “Embrace collisions: Humanoid shadowing for deployable contact-agnostics motions,” _arXiv preprint arXiv:2502.01465_ , 2025. 

- [104] S. An, Z. Meng, C. Tang, Y. Zhou, T. Liu, F. Ding, S. Zhang, Y. Mu, R. Song, W. Zhang _et al._ , “Dexterous manipulation through imitation learning: A survey,” _arXiv preprint arXiv:2504.03515_ , 2025. 

- [105] M. Zare, P. M. Kebria, A. Khosravi, and S. Nahavandi, “A survey of imitation learning: Algorithms, recent developments, and challenges,” _IEEE Transactions on Cybernetics_ , 2024. 

- [106] D. Kragic, H. I. Christensen _et al._ , “Survey on visual servoing for manipulation,” _Computational Vision and Active Perception Laboratory, Fiskartorpsv_ , vol. 15, p. 2002, 2002. 

- [107] Y. Xiang, T. Schmidt, V. Narayanan, and D. Fox, “Posecnn: A convolutional neural network for 6d object pose estimation in cluttered scenes,” _arXiv preprint arXiv:1711.00199_ , 2017. 

- [108] H. Wang, S. Sridhar, J. Huang, J. Valentin, S. Song, and L. J. Guibas, “Normalized object coordinate space for category-level 6d object pose and size estimation,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2019, pp. 2642–2651. 

- [109] T.-T. Do, A. Nguyen, and I. Reid, “Affordancenet: An end-to-end deep learning approach for object affordance detection,” in _2018 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2018, pp. 5882–5889. 

- [110] K. Mo, L. J. Guibas, M. Mukadam, A. Gupta, and S. Tulsiani, “Where2act: From pixels to actions for articulated 3d objects,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2021, pp. 6813–6823. 

- [111] A. Simeonov, Y. Du, A. Tagliasacchi, J. B. Tenenbaum, A. Rodriguez, P. Agrawal, and V. Sitzmann, “Neural descriptor fields: 

Se (3)-equivariant object representations for manipulation,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 6394–6400. 

- [112] A. Brohan _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” _arXiv preprint arXiv:2307.15818_ , 2023. 

- [113] A. Murali, A. Mousavian, C. Eppner, C. Paxton, and D. Fox, “6dof grasping for target-driven object manipulation in clutter,” in _2020 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2020, pp. 6232–6238. 

- [114] M. Shridhar, L. Manuelli, and D. Fox, “Perceiver-actor: A multitask transformer for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 785–799. 

- [115] V. E. Arriola-Rios, P. Guler, F. Ficuciello, D. Kragic, B. Siciliano, and J. L. Wyatt, “Modeling of deformable objects for robotic manipulation: A tutorial and review,” _Frontiers in Robotics and AI_ , vol. 7, p. 82, 2020. 

- [116] F. Gu, Y. Zhou, Z. Wang, S. Jiang, and B. He, “A survey on robotic manipulation of deformable objects: Recent advances, open challenges and new frontiers,” _arXiv preprint arXiv:2312.10419_ , 2023. 

- [117] Y. She, S. Wang, S. Dong, N. Sunil, A. Rodriguez, and E. Adelson, “Cable manipulation with a tactile-reactive gripper,” _The International Journal of Robotics Research_ , vol. 40, no. 12-14, pp. 1385–1401, 2021. 

- [118] C. Yang, K. Wang, Y. Wang, X. Yang, and W. Shen, “Neural lerplane representations for fast 4d reconstruction of deformable tissues,” in _International Conference on Medical Image Computing and Computer-Assisted Intervention_ . Springer, 2023, pp. 46–56. 

- [119] Y. Jiang, R. Zhang, J. Wong, C. Wang, Y. Ze, H. Yin, C. Gokmen, S. Song, J. Wu, and L. Fei-Fei, “Behavior robot suite: Streamlining real-world whole-body manipulation for everyday household activities,” _arXiv preprint arXiv:2503.05652_ , 2025. 

- [120] A. M. Okamura, N. Smaby, and M. R. Cutkosky, “An overview of dexterous manipulation,” in _Proceedings 2000 ICRA. Millennium Conference. IEEE International Conference on Robotics and Automation. Symposia Proceedings (Cat. No. 00CH37065)_ , vol. 1. IEEE, 2000, pp. 255–262. 

- [121] S. Jacobsen, E. Iversen, D. Knutti, R. Johnson, and K. Biggers, “Design of the utah/mit dextrous hand,” in _Proceedings. 1986 IEEE International Conference on Robotics and Automation_ , vol. 3. IEEE, 1986, pp. 1520–1532. 

- [122] Shadow Robot Company. Dexterous hand series. Accessed on June 26, 2025. [Online]. Available: https://shadowrobot.com/ dexterous-hand-series/ 

- [123] W. Townsend, “The barretthand grasper–programmably flexible part handling and assembly,” _Industrial Robot: an international journal_ , vol. 27, no. 3, pp. 181–188, 2000. 

- [124] J. R. Napier, “The prehensile movements of the human hand,” _The Journal of Bone & Joint Surgery British Volume_ , vol. 38, no. 4, pp. 902–913, 1956. 

- [125] J. K. Salisbury and J. J. Craig, “Articulated hands: Force control and kinematic issues,” _The International journal of Robotics research_ , vol. 1, no. 1, pp. 4–17, 1982. 

- [126] A. T. Miller and P. K. Allen, “Graspit! a versatile simulator for robotic grasping,” _IEEE Robotics & Automation Magazine_ , vol. 11, no. 4, pp. 110–122, 2004. 

- [127] D. Turpin, T. Zhong, S. Zhang, G. Zhu, E. Heiden, M. Macklin, S. Tsogkas, S. Dickinson, and A. Garg, “Fast-grasp’d: Dexterous multi-finger grasp generation through differentiable simulation,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 8082–8089. 

- [128] J. Zhang, H. Liu, D. Li, X. Yu, H. Geng, Y. Ding, J. Chen, and H. Wang, “Dexgraspnet 2.0: Learning generative dexterous grasping in large-scale synthetic cluttered scenes,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [129] Y. Li, W. Wei, D. Li, P. Wang, W. Li, and J. Zhong, “Hgc-net: Deep anthropomorphic hand grasping in clutter,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 714–720. 

- [130] M. Liu, Z. Pan, K. Xu, K. Ganguly, and D. Manocha, “Deep differentiable grasp planner for high-dof grippers,” _arXiv preprint arXiv:2002.01530_ , 2020. 

- [131] S. Huang, Z. Wang, P. Li, B. Jia, T. Liu, Y. Zhu, W. Liang, and S.-C. Zhu, “Diffusion-based generation, optimization, and planning in 3d scenes,” in _CVPR_ , 2023, pp. 16 750–16 761. 

42 

- [132] H. Jiang, S. Liu, J. Wang, and X. Wang, “Hand-object contact consistency reasoning for human grasps generation,” in _ICCV_ , 2021, pp. 11 107–11 116. 

- [133] J. Lundell, E. Corona, T. N. Le, F. Verdoja, P. Weinzaepfel, G. Rogez, F. Moreno-Noguer, and V. Kyrki, “Multi-fingan: Generative coarse-to-fine sampling of multi-finger grasps,” in _IEEE International Conference on Robotics and Automation_ . IEEE, 2021, pp. 4495–4501. 

- [134] J. Lundell, F. Verdoja, and V. Kyrki, “Ddgc: Generative deep dexterous grasping in clutter,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 4, pp. 6899–6906, 2021. 

- [135] W. Wei, D. Li, P. Wang, Y. Li, W. Li, Y. Luo, and J. Zhong, “Dvgg: Deep variational grasp generation for dextrous manipulation,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 2, pp. 1659–1666, 2022. 

- [136] J. Lu, H. Kang, H. Li, B. Liu, Y. Yang, Q. Huang, and G. Hua, “Ugg: Unified generative grasping,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 414–433. 

- [137] Y.-L. Wei, J.-J. Jiang, C. Xing, X.-T. Tan, X.-M. Wu, H. Li, M. Cutkosky, and W.-S. Zheng, “Grasp as you say: Language-guided dexterous grasp generation,” _arXiv preprint arXiv:2405.19291_ , 2024. 

- [138] Y. Liu, Y. Yang, Y. Wang, X. Wu, J. Wang, Y. Yao, S. Schwertfeger, S. Yang, W. Wang, J. Yu, X. He, and Y. Ma, “Realdex: Towards human-like grasping for robotic dexterous hand,” in _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI-24_ , K. Larson, Ed. International Joint Conferences on Artificial Intelligence Organization, 8 2024, pp. 6859–6867, main Track. [Online]. Available: https://doi.org/10.24963/ijcai.2024/758 

- [139] Y. Zhong, Q. Jiang, J. Yu, and Y. Ma, “Dexgrasp anything: Towards universal robotic dexterous grasping with physics awareness,” _arXiv preprint arXiv:2503.08257_ , 2025. 

- [140] Z. Wei, Z. Xu, J. Guo, Y. Hou, C. Gao, Z. Cai, J. Luo, and L. Shao, “D(r,o) grasp: A unified representation of robot and object interaction for cross-embodiment dexterous grasping,” _arXiv preprint arXiv:2410.01702_ , 2024. 

- [141] S. Chen, J. Bohg, and C. K. Liu, “Springgrasp: Synthesizing compliant, dexterous grasps under shape uncertainty,” _arXiv preprint arXiv:2404.13532_ , 2024. 

- [142] T. Chen, J. Xu, and P. Agrawal, “A system for general in-hand object re-orientation,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 297–307. 

- [143] T. Chen, M. Tippur, S. Wu, V. Kumar, E. Adelson, and P. Agrawal, “Visual dexterity: In-hand dexterous manipulation from depth,” in _Icml workshop on new frontiers in learning, control, and dynamical systems_ , 2023. 

- [144] Z.-H. Yin, B. Huang, Y. Qin, Q. Chen, and X. Wang, “Rotating without seeing: Towards in-hand dexterity through touch,” _arXiv preprint arXiv:2303.10880_ , 2023. 

- [145] P. Mandikal and K. Grauman, “Dexvip: Learning dexterous grasping with human hand pose priors from video,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 651–661. 

- [146] ——, “Learning dexterous grasping with object-centric visual affordances,” in _2021 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2021, pp. 6169–6176. 

- [147] T. G. W. Lum, M. Matak, V. Makoviychuk, A. Handa, A. Allshire, T. Hermans, N. D. Ratliff, and K. Van Wyk, “Dextrah-g: Pixelsto-action dexterous arm-hand grasping with geometric fabrics,” _arXiv preprint arXiv:2407.02274_ , 2024. 

- [148] R. Singh, A. Allshire, A. Handa, N. Ratliff, and K. Van Wyk, “Dextrah-rgb: Visuomotor policies to grasp anything with dexterous hands,” _arXiv preprint arXiv:2412.01791_ , 2024. 

- [149] Z. Q. Chen, K. Van Wyk, Y.-W. Chao, W. Yang, A. Mousavian, A. Gupta, and D. Fox, “Learning robust real-world dexterous grasping policies via implicit shape augmentation,” _arXiv preprint arXiv:2210.13638_ , 2022. 

- [150] Q. Wang, H. Zhang, C. Deng, Y. You, H. Dong, Y. Zhu, and L. Guibas, “Sparsedff: Sparse-view feature distillation for oneshot dexterous manipulation,” _arXiv preprint arXiv:2310.16838_ , 2023. 

- [151] Q. Wang, C. Deng, T. G. W. Lum, Y. Chen, Y. Yang, J. Bohg, Y. Zhu, and L. Guibas, “Neural attention field: Emerging point relevance in 3d scenes for one-shot dexterous grasping,” _arXiv preprint arXiv:2410.23039_ , 2024. 

- [152] Y. Zhong, X. Huang, R. Li, C. Zhang, Y. Liang, Y. Yang, and Y. Chen, “Dexgraspvla: A vision-language-action frame- 

   - work towards general dexterous grasping,” _arXiv preprint arXiv:2502.20900_ , 2025. 

- [153] Z. Fu, T. Z. Zhao, and C. Finn, “Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation,” _arXiv preprint arXiv:2401.02117_ , 2024. 

- [154] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Q. Liang, Z. Li, X. Lin, Y. Ge, Z. Gu, W. Deng, Y. Guo, T. Nian, X. Xie, Q. Chen, K. Su, T. Xu, G. Liu, M. Hu, H. ang Gao, K. Wang, Z. Liang, Y. Qin, X. Yang, P. Luo, and Y. Mu, “Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2506.18088 

- [155] C. Smith, Y. Karayiannidis, L. Nalpantidis, X. Gratal, P. Qi, D. V. Dimarogonas, and D. Kragic, “Dual arm manipulation—a survey,” _Robotics and Autonomous systems_ , vol. 60, no. 10, pp. 1340–1353, 2012. 

- [156] J. Grannen, Y. Wu, B. Vu, and D. Sadigh, “Stabilize to act: Learning to coordinate for bimanual manipulation,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 563–576. 

- [157] G. Franzese, L. de Souza Rosa, T. Verburg, L. Peternel, and J. Kober, “Interactive imitation learning of bimanual movement primitives,” _IEEE/ASME Transactions on Mechatronics_ , 2023. 

- [158] T. Z. Zhao, J. Tompson, D. Driess, P. Florence, K. Ghasemipour, C. Finn, and A. Wahid, “Aloha unleashed: A simple recipe for robot dexterity,” _arXiv preprint arXiv:2410.13126_ , 2024. 

- [159] K. Li, P. Li, T. Liu, Y. Li, and S. Huang, “Maniptrans: Efficient dexterous bimanual manipulation transfer via residual learning,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025. 

- [160] Z. Mandi, Y. Hou, D. Fox, Y. Narang, A. Mandlekar, and S. Song, “Dexmachina: Functional retargeting for bimanual dexterous manipulation,” 2025. [Online]. Available: https: //arxiv.org/abs/2505.24853 

- [161] K. Harada and M. Kaneko, “Whole body manipulation,” in _IEEE International Conference on Robotics, Intelligent Systems and Signal Processing, 2003. Proceedings. 2003_ , vol. 1. IEEE, 2003, pp. 190– 195. 

- [162] H. Xiong, R. Mendonca, K. Shaw, and D. Pathak, “Adaptive mobile manipulation for articulated objects in the open world,” _arXiv preprint arXiv:2401.14403_ , 2024. 

- [163] X. Cheng, A. Kumar, and D. Pathak, “Legs as manipulator: Pushing quadrupedal agility beyond locomotion,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 5106–5112. 

- [164] J. Wu, R. Antonova, A. Kan, M. Lepert, A. Zeng, S. Song, J. Bohg, S. Rusinkiewicz, and T. Funkhouser, “Tidybot: Personalized robot assistance with large language models,” _Autonomous Robots_ , vol. 47, no. 8, pp. 1087–1102, 2023. 

- [165] A. Stone, T. Xiao, Y. Lu, K. Gopalakrishnan, K.-H. Lee, Q. Vuong, P. Wohlhart, S. Kirmani, B. Zitkovich, F. Xia _et al._ , “Open-world object manipulation using pre-trained vision-language models,” _arXiv preprint arXiv:2303.00905_ , 2023. 

- [166] Z. Jiang, Y. Xie, J. Li, Y. Yuan, Y. Zhu, and Y. Zhu, “Harmon: Whole-body motion generation of humanoid robots from language descriptions,” _arXiv preprint arXiv:2410.12773_ , 2024. 

- [167] J. Li, Y. Zhu, Y. Xie, Z. Jiang, M. Seo, G. Pavlakos, and Y. Zhu, “Okami: Teaching humanoid robots manipulation skills through single video imitation,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [168] Y. Ze, Z. Chen, W. Wang, T. Chen, X. He, Y. Yuan, X. B. Peng, and J. Wu, “Generalizable humanoid manipulation with improved 3d diffusion policies,” _arXiv preprint arXiv:2410.10803_ , 2024. 

- [169] M. Ahn, A. Brohan _et al._ , “Can foundation models ground language in robotics?” _arXiv preprint arXiv:2204.01691_ , 2022. 

- [170] D. Driess, F. Xia, M. S. Sajjadi, C. Lynch, A. Chowdhery, A. Wahid, J. Tompson, Q. Vuong, T. Yu, W. Huang _et al._ , “Palm-e: An embodied multimodal language model,” 2023. 

- [171] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng, J. Tompson, I. Mordatch, Y. Chebotar _et al._ , “Inner monologue: Embodied reasoning through planning with language models,” _arXiv preprint arXiv:2207.05608_ , 2022. 

- [172] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence, and A. Zeng, “Code as policies: Language model programs for embodied control,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 9493–9500. 

43 

- [173] Z. Lin, W. Liu, C. Chen, J. Lu, W. Hu, T.-J. Fu, J. Allardice, Z. Lai, L. Song, B. Zhang _et al._ , “Stiv: Scalable text and image conditioned video generation,” _arXiv preprint arXiv:2412.07730_ , 2024. 

- [174] Figure AI, “Introducing helix,” 2025, accessed: 2025-05-10. [Online]. Available: https://www.figure.ai/news/helix 

- [175] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [176] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [177] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [178] C.-L. Cheang, G. Chen, Y. Jing, T. Kong, H. Li, Y. Li, Y. Liu, H. Wu, J. Xu, Y. Yang _et al._ , “Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation,” _arXiv preprint arXiv:2410.06158_ , 2024. 

- [179] W. Zhang, E. L. Slade, and E. Pantano, “Humanlike service robots: A systematic literature review and research agenda,” _Psychology & Marketing_ , vol. 41, no. 12, pp. 3157–3181, 2024. 

- [180] A. Chac´on, P. Ponsa, and C. Angulo, “Cognitive interaction analysis in human–robot collaboration using an assembly task,” _Electronics_ , vol. 10, no. 11, p. 1317, 2021. 

- [181] H. Liang, C. Huang, Y. Xu, C. Tang, W. Ye, J. Zhang, X. Chen, J. Yu, and L. Xu, “Llava-slt: Visual language tuning for sign language translation,” _arXiv preprint arXiv:2412.16524_ , 2024. 

- [182] S. Lemaignan, M. Warnier, E. A. Sisbot, A. Clodic, and R. Alami, “Artificial cognition for social human–robot interaction: An implementation,” _Artificial Intelligence_ , vol. 247, pp. 45–69, 2017. 

- [183] F. Semeraro, A. Griffiths, and A. Cangelosi, “Human–robot collaboration and machine learning: A systematic review of recent research,” _Robotics and Computer-Integrated Manufacturing_ , vol. 79, p. 102432, 2023. 

- [184] M. Spezialetti, G. Placidi, and S. Rossi, “Emotion recognition for human-robot interaction: Recent advances and future perspectives,” _Frontiers in Robotics and AI_ , vol. 7, p. 532279, 2020. 

- [185] J. Laplaza, F. Moreno, and A. Sanfeliu, “Enhancing robotic collaborative tasks through contextual human motion prediction and intention inference,” _International Journal of Social Robotics_ , pp. 1– 20, 2024. 

- [186] B. Yu, H. Kasaei, and M. Cao, “L3mvn: Leveraging large language models for visual target navigation,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023, pp. 3554–3560. 

- [187] H. Yin, X. Xu, Z. Wu, J. Zhou, and J. L. Sg-nav, “Online 3d scene graph prompting for llm-based zero-shot object navigation,” _Advances in Neural Information Processing Systems_ , vol. 7, 2024. 

- [188] L. Zhang, Q. Zhang, H. Wang, E. Xiao, Z. Jiang, H. Chen, and R. Xu, “Trihelper: Zero-shot object navigation with dynamic assistance,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 10 035–10 042. 

- [189] Y. Cao, J. Zhang, Z. Yu, S. Liu, Z. Qin, Q. Zou, B. Du, and K. Xu, “Cognav: Cognitive process modeling for object goal navigation with llms,” _arXiv preprint arXiv:2412.10439_ , 2024. 

- [190] H. Yin, X. Xu, L. Zhao, Z. Wang, J. Zhou, and J. Lu, “Unigoal: Towards universal zero-shot goal-oriented navigation,” _arXiv preprint arXiv:2503.10630_ , 2025. 

- [191] Z. Wang, Z. Chen, J. Chen, J. Wang, Y. Yang, Y. Liu, X. Liu, H. Wang, and L. Yi, “Mobileh2r: Learning generalizable human to mobile robot handover exclusively from scalable and diverse synthetic data,” _arXiv preprint arXiv:2501.04595_ , 2025. 

- [192] L. Liu, F. Guo, Z. Zou, and V. G. Duffy, “Application, development and future opportunities of collaborative robots (cobots) in manufacturing: A literature review,” _International Journal of Human–Computer Interaction_ , vol. 40, no. 4, pp. 915–932, 2024. 

- [193] R. Geraerts and M. H. Overmars, “A comparative study of probabilistic roadmap planners,” in _Algorithmic foundations of robotics V_ . Springer, 2004, pp. 43–57. 

- [194] S. LaValle, “Rapidly-exploring random trees: A new tool for path planning,” _Research Report 9811_ , 1998. 

- [195] G. Chen, N. Luo, D. Liu, Z. Zhao, and C. Liang, “Path planning for manipulators based on an improved probabilistic roadmap 

   - method,” _Robotics and Computer-Integrated Manufacturing_ , vol. 72, p. 102196, 2021. 

- [196] S. Karaman and E. Frazzoli, “Sampling-based algorithms for optimal motion planning,” _The international journal of robotics research_ , vol. 30, no. 7, pp. 846–894, 2011. 

- [197] J. J. Kuffner and S. M. LaValle, “Rrt-connect: An efficient approach to single-query path planning,” in _Proceedings 2000 ICRA. Millennium conference. IEEE international conference on robotics and automation. Symposia proceedings (Cat. No. 00CH37065)_ , vol. 2. IEEE, 2000, pp. 995–1001. 

- [198] D. Yi, M. A. Goodrich, and K. D. Seppi, “Homotopy-aware rrt*: Toward human-robot topological path-planning,” in _2016 11th ACM/IEEE International Conference on Human-Robot Interaction (HRI)_ . IEEE, 2016, pp. 279–286. 

- [199] M. Raessa, J. C. Y. Chen, W. Wan, and K. Harada, “Human-in-theloop robotic manipulation planning for collaborative assembly,” _IEEE Transactions on Automation Science and Engineering_ , vol. 17, no. 4, pp. 1800–1813, 2020. 

- [200] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, “Chomp: Gradient optimization techniques for efficient motion planning,” in _2009 IEEE international conference on robotics and automation_ . IEEE, 2009, pp. 489–494. 

- [201] M. Kalakrishnan, S. Chitta, E. Theodorou, P. Pastor, and S. Schaal, “Stomp: Stochastic trajectory optimization for motion planning,” in _2011 IEEE international conference on robotics and automation_ . IEEE, 2011, pp. 4569–4574. 

- [202] C. Park, J. Pan, and D. Manocha, “Itomp: Incremental trajectory optimization for real-time replanning in dynamic environments,” in _Proceedings of the international conference on automated planning and scheduling_ , vol. 22, 2012, pp. 207–215. 

- [203] J. Schulman, Y. Duan, J. Ho, A. Lee, I. Awwal, H. Bradlow, J. Pan, S. Patil, K. Goldberg, and P. Abbeel, “Motion planning with sequential convex optimization and convex collision checking,” _The International Journal of Robotics Research_ , vol. 33, no. 9, pp. 1251–1270, 2014. 

- [204] R. Hayne, R. Luo, and D. Berenson, “Considering avoidance and consistency in motion planning for human-robot manipulation in a shared workspace,” in _2016 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2016, pp. 3948–3954. 

- [205] M. Mukadam, J. Dong, X. Yan, F. Dellaert, and B. Boots, “Continuous-time gaussian process motion planning via probabilistic inference,” _The International Journal of Robotics Research_ , vol. 37, no. 11, pp. 1319–1340, 2018. 

- [206] X. Zhao and J. Pan, “Considering human behavior in motion planning for smooth human-robot collaboration in close proximity,” in _2018 27th IEEE international symposium on robot and human interactive communication (RO-MAN)_ . IEEE, 2018, pp. 985–990. 

- [207] M. N. Finean, W. Merkt, and I. Havoutis, “Simultaneous scene reconstruction and whole-body motion planning for safe operation in dynamic environments,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2021, pp. 3710–3717. 

- [208] S. Tarbouriech, B. Navarro, P. Fraisse, A. Crosnier, A. Cherubini, and D. Sall´e, “Admittance control for collaborative dual-arm manipulation,” in _2019 19th International Conference on Advanced Robotics (ICAR)_ . IEEE, 2019, pp. 198–204. 

- [209] X. Yu, S. Zhang, L. Sun, Y. Wang, C. Xue, and B. Li, “Cooperative control of dual-arm robots in different human-robot collaborative tasks,” _Assembly Automation_ , vol. 40, no. 1, pp. 95–104, 2020. 

- [210] A. Hameed, A. Ordys, J. Mo˙zaryn, and A. Sibilska-Mroziewicz, “Control system design and methods for collaborative robots,” _Applied Sciences_ , vol. 13, no. 1, p. 675, 2023. 

- [211] A.-N. Sharkawy and P. N. Koustoumpardis, “Human–robot interaction: A review and analysis on variable admittance control, safety, and perspectives,” _Machines_ , vol. 10, no. 7, p. 591, 2022. 

- [212] Z. Ji, Q. Liu, W. Xu, Z. Liu, B. Yao, B. Xiong, and Z. Zhou, “Towards shared autonomy framework for human-aware motion planning in industrial human-robot collaboration,” in _2020 IEEE 16th International Conference on Automation Science and Engineering (CASE)_ . IEEE, 2020, pp. 411–417. 

- [213] A. Bonci, P. D. Cen Cheng, M. Indri, G. Nabissi, and F. Sibona, “Human-robot perception in industrial environments: A survey,” _Sensors_ , vol. 21, no. 5, p. 1571, 2021. 

- [214] X. Zhao, T. Fan, D. Wang, Z. Hu, T. Han, and J. Pan, “An actorcritic approach for legible robot motion planner,” in _2020 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2020, pp. 5949–5955. 

44 

- [215] Y. Cui, Z. Xu, L. Zhong, P. Xu, Y. Shen, and Q. Tang, “A taskadaptive deep reinforcement learning framework for dual-arm robot manipulation,” _IEEE Transactions on Automation Science and Engineering_ , vol. 22, pp. 466–479, 2024. 

- [216] Y. Fan, X. Li, K. Zhang, C. Qian, F. Zhou, T. Li, and Z. Huang, “Learning robust skills for tightly coordinated arms in contactrich tasks,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 3, pp. 2973–2980, 2024. 

- [217] Y.-W. Chao, C. Paxton, Y. Xiang, W. Yang, B. Sundaralingam, T. Chen, A. Murali, M. Cakmak, and D. Fox, “Handoversim: A simulation framework and benchmark for human-to-robot object handovers,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 6941–6947. 

- [218] Z. Wang, J. Chen, Z. Chen, P. Xie, R. Chen, and L. Yi, “Genh2r: Learning generalizable human-to-robot handover via scalable simulation demonstration and imitation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 16 362–16 372. 

- [219] D. M. Lloyd, “The space between us: A neurophilosophical framework for the investigation of human interpersonal space,” _Neuroscience & Biobehavioral Reviews_ , vol. 33, no. 3, pp. 297–304, 2009. 

- [220] Y. Coello and A. Cartaud, “The interrelation between peripersonal action space and interpersonal social space: psychophysiological evidence and clinical implications,” _Frontiers in Human Neuroscience_ , vol. 15, p. 636124, 2021. 

- [221] C. P. Gharpure and V. A. Kulyukin, “Robot-assisted shopping for the blind: issues in spatial cognition and product selection,” _Intelligent Service Robotics_ , vol. 1, pp. 237–251, 2008. 

- [222] H. Fernandes, P. Costa, V. Filipe, H. Paredes, and J. Barroso, “A review of assistive spatial orientation and navigation technologies for the visually impaired,” _Universal Access in the Information Society_ , vol. 18, pp. 155–168, 2019. 

- [223] S. Agrawal, S. Nayak, A. Naik, and B. Hayes, “Shelfhelp: Empowering humans to perform vision-independent manipulation tasks with a socially assistive robotic cane,” _arXiv preprint arXiv:2405.20501_ , 2024. 

- [224] D. Hazarika, S. Poria, A. Zadeh, E. Cambria, L.-P. Morency, and R. Zimmermann, “Conversational memory network for emotion recognition in dyadic dialogue videos,” in _Proceedings of the conference. Association for Computational Linguistics. North American Chapter. Meeting_ , vol. 2018. NIH Public Access, 2018, p. 2122. 

- [225] B. Lee and Y. S. Choi, “Graph based network with contextualized representations of turns in dialogue,” _arXiv preprint arXiv:2109.04008_ , 2021. 

- [226] D. Ghosal, N. Majumder, S. Poria, N. Chhaya, and A. Gelbukh, “Dialoguegcn: A graph convolutional neural network for emotion recognition in conversation,” _arXiv preprint arXiv:1908.11540_ , 2019. 

- [227] A. Stolcke, K. Ries, N. Coccaro, E. Shriberg, R. Bates, D. Jurafsky, P. Taylor, R. Martin, C. V. Ess-Dykema, and M. Meteer, “Dialogue act modeling for automatic tagging and recognition of conversational speech,” _Computational linguistics_ , vol. 26, no. 3, pp. 339– 373, 2000. 

- [228] B. Lai, H. Zhang, M. Liu, A. Pariani, F. Ryan, W. Jia, S. A. Hayati, J. Rehg, and D. Yang, “Werewolf among us: Multimodal resources for modeling persuasion behaviors in social deduction games,” _Association for Computational Linguistics: ACL 2023_ , 2023. 

- [229] S. Lee, M. Li, B. Lai, W. Jia, F. Ryan, X. Cao, O. Kara, B. Boote, W. Shi, D. Yang _et al._ , “Towards social ai: A survey on understanding social interactions,” _arXiv preprint arXiv:2409.15316_ , 2024. 

- [230] D. Yang, D. Hovy, D. Jurgens, and B. Plank, “The call for socially aware language technologies,” 2024. 

- [231] D. Liu, L. Zhang, and Y. Wu, “Ld-congr: A large rgb-d video dataset for long-distance continuous gesture recognition,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022, pp. 3304–3312. 

- [232] W. Jia, M. Liu, H. Jiang, I. Ananthabhotla, J. M. Rehg, V. K. Ithapu, and R. Gao, “The audio-visual conversational graph: From an egocentric-exocentric perspective,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 26 396–26 405. 

- [233] S. Jahangard, Z. Cai, S. Wen, and H. Rezatofighi, “Jrdb-social: A multifaceted robotic dataset for understanding of context and dynamics of human interactions within social groups,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 22 087–22 097. 

- [234] S. Ghosh, Z. Cai, A. Dhall, D. Kollias, R. Goecke, and T. Gedeon, “Mrac track 1: 2nd workshop on multimodal, generative and responsible affective computing,” _arXiv preprint arXiv:2409.07256_ , 2024. 

- [235] Y. Peng, J. Han, Z. Zhang, L. Fan, T. Liu, S. Qi, X. Feng, Y. Ma, Y. Wang, and S.-C. Zhu, “The tong test: Evaluating artificial general intelligence through dynamic embodied physical and social interactions,” _Engineering_ , vol. 34, pp. 12–22, 2024. 

- [236] X. Cao, P. Virupaksha, W. Jia, B. Lai, F. Ryan, S. Lee, and J. M. Rehg, “Socialgesture: Delving into multi-person gesture understanding,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 

- [237] Y. Che, A. M. Okamura, and D. Sadigh, “Efficient and trustworthy social navigation via explicit and implicit robot–human communication,” _IEEE Transactions on Robotics_ , vol. 36, no. 3, pp. 692–707, 2020. 

- [238] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, and S. Song, “Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots,” _arXiv preprint arXiv:2402.10329_ , 2024. 

- [239] O. Michel, “Webots: Professional mobile robot simulation,” _Journal of Advanced Robotics Systems_ , vol. 1, no. 1, pp. 39–42, 2004. [Online]. Available: http://www.ars-journal.com/International -Journal-of-Advanced-Robotic-Systems/Volume-1/39-42.pdf 

- [240] E. Coumans and Y. Bai, “Pybullet, a python module for physics simulation for games, robotics and machine learning,” http:// pybullet.org, 2016–2019. 

- [241] E. Rohmer, S. P. N. Singh, and M. Freese, “Coppeliasim (formerly v-rep): a versatile and scalable robot simulation framework,” in _Proc. of The International Conference on Intelligent Robots and Systems (IROS)_ , 2013, www.coppeliarobotics.com. 

- [242] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [243] NVIDIA Corporation, “Isaac Sim,” 2025, accessed: 2025-04-18. [Online]. Available: https://developer.nvidia.com/isaac/sim 

- [244] ——, “NVIDIA Omniverse,” 2025, accessed: 2025-06-28. [Online]. Available: https://www.nvidia.com/en-us/omniverse/ 

- [245] “The alliance for openusd,” https://aousd.org/, Alliance for OpenUSD (AOUSD), 2023, accessed: 2025-06-28. [Online]. Available: https://aousd.org/ 

- [246] Isaac Lab Contributors, “Isaac Lab Documentation,” 2025, accessed: 2025-04-18. [Online]. Available: https://isaac-sim.git hub.io/IsaacLab/main/index.html 

- [247] F. Xiang, Y. Qin, K. Mo, Y. Xia, H. Zhu, F. Liu, M. Liu, H. Jiang, Y. Yuan, H. Wang _et al._ , “Sapien: A simulated part-based interactive environment,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 11 097–11 107. 

- [248] J. Gu, F. Xiang, X. Li, Z. Ling, X. Liu, T. Mu, Y. Tang, S. Tao, X. Wei, Y. Yao, X. Yuan, P. Xie, Z. Huang, R. Chen, and H. Su, “Maniskill2: A unified benchmark for generalizable manipulation skills,” in _International Conference on Learning Representations_ , 2023. 

- [249] S. Tao, F. Xiang, A. Shukla, Y. Qin, X. Hinrichsen, X. Yuan, C. Bao, X. Lin, Y. Liu, T. kai Chan, Y. Gao, X. Li, T. Mu, N. Xiao, A. Gurha, Z. Huang, R. Calandra, R. Chen, S. Luo, and H. Su, “Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai,” _arXiv preprint arXiv:2410.00425_ , 2024. 

- [250] G. Authors, “Genesis: A universal and generative physics engine for robotics and beyond,” December 2024. [Online]. Available: https://github.com/Genesis-Embodied-AI/Genesis 

- [251] S. Huang, M. Macklin, and G. State, “Announcing newton, an open-source physics engine for robotics simulation,” March 2025, accessed: 2025-04-18. [Online]. Available: https://developer.nvidia.com/blog/announcing-newton-an-o 

- pen-source-physics-engine-for-robotics-simulation/ 

- [252] NVIDIA Corporation, “NVIDIA PhysX System Software,” Official driver download page, Oct. 2021, release Date: 2021-10-15; Accessed: 2025-06-28. [Online]. Available: https: //www.nvidia.cn/drivers/physx/physx-9-21-0713-driver/ 

- [253] D. Catanoso, T. Stucky, J. Case, and A. Rogg, “Analysis of sample acquisition dynamics using discrete element method,” in _2020 IEEE Aerospace Conference_ . IEEE, 2020, pp. 1–11. 

- [254] Khronos Group, “OpenGL: The Industry Standard for High-Performance Graphics,” https://www.opengl.org/, 1992, released June 30, 1992; Accessed: 2025-06-28. 

45 

- [255] ——, “Vulkan: A royalty-free cross-platform 3D graphics and compute API,” https://www.vulkan.org/, 2016, first released February 16, 2016; Accessed: 2025-06-28. 

- [256] Ray-Tracing-Systems, “HydraRendererInfo: Informational page about Hydra Renderer,” https://github.com/Ray-Tracing-Sys tems/HydraRendererInfo, 2019, gitHub repository, MIT license. 

- [257] M. Matl, “Pyrender,” https://github.com/mmatl/pyrender, 2019, gitHub repository. 

- [258] S. Zheng, Z. Zhou, X. Chen, D. Yan, C. Zhang, Y. Geng, Y. Gu, and K. Xu, “Luisarender: A high-performance rendering framework with layered and unified interfaces on stream architectures,” _ACM Trans. Graph._ , vol. 41, no. 6, Nov. 2022. 

- [259] NVIDIA Corporation, “NVIDIA OptiX™Ray Tracing Engine,” https://developer.nvidia.com/rtx/ray-tracing/optix, 2024, ac- 

- cessed: 2025-06-28. 

- [260] LS Group, “Interact documentation: Kinematics,” https:// documentation.ls-group.fr/interact/kinematics/, 2025, accessed: 2025-06-26. 

- [261] A. Dawid and Y. LeCun, “Introduction to latent variable energybased models: a path toward autonomous machine intelligence,” _Journal of Statistical Mechanics: Theory and Experiment_ , vol. 2024, no. 10, p. 104011, 2024. 

- [262] R. Sekar, O. Rybkin, K. Daniilidis, P. Abbeel, D. Hafner, and D. Pathak, “Planning to explore via self-supervised world models,” in _International conference on machine learning_ . PMLR, 2020, pp. 8583–8592. 

- [263] T. Brooks, B. Peebles, C. Holmes, W. DePue, Y. Guo, L. Jing, D. Schnurr, J. Taylor, T. Luhman, E. Luhman, C. Ng, R. Wang, and A. Ramesh, “Video generation models as world simulators,” 2024. [Online]. Available: https://openai.com/research/vide o-generation-models-as-world-simulators 

- [264] klingai.com, “KlingAI,” 2025, accessed: 2025-04-18. [Online]. Available: https://klingai.com/cn/ 

- [265] A. Bar, G. Zhou, D. Tran, T. Darrell, and Y. LeCun, “Navigation world models,” _arXiv preprint arXiv:2412.03572_ , 2024. 

- [266] K. Drozdov, R. Shwartz-Ziv, and Y. LeCun, “Video representation learning with joint-embedding predictive architectures,” _arXiv preprint arXiv:2412.10925_ , 2024. 

- [267] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson, “Learning latent dynamics for planning from pixels,” _arXiv preprint arXiv:1811.04551_ , 2018. 

- [268] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” _arXiv preprint arXiv:1912.01603_ , 2019. 

- [269] D. Hafner, T. Lillicrap, M. Norouzi, and J. Ba, “Mastering atari with discrete world models,” _arXiv preprint arXiv:2010.02193_ , 2020. 

- [270] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” _arXiv preprint arXiv:2301.04104_ , 2023. 

- [271] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg, “Daydreamer: World models for physical robot learning,” in _Conference on robot learning_ . PMLR, 2023, pp. 2226–2240. 

- [272] Y. LeCun, “A Path Towards Autonomous Machine Intelligence,” OpenReview, 2022, version 0.9.2, June 27. [Online]. Available: https://openreview.net/pdf?id=BZ5a1r-kVsf 

- [273] M. Assran, Q. Duval, I. Misra, P. Bojanowski, P. Vincent, M. Rabbat, Y. LeCun, and N. Ballas, “Self-supervised learning from images with a joint-embedding predictive architecture,” _arXiv preprint arXiv:2301.08243_ , 2023. 

- [274] A. Bardes, Q. Garrido, J. Ponce, M. Rabbat, Y. LeCun, M. Assran, and N. Ballas, “Revisiting feature prediction for learning visual representations from video,” _arXiv:2404.08471_ , 2024. 

- [275] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Komeili, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus, S. Arnaud, A. Gejji, A. Martin, F. Robert Hogan, D. Dugas, P. Bojanowski, V. Khalidov, P. Labatut, F. Massa, M. Szafraniec, K. Krishnakumar, Y. Li, X. Ma, S. Chandar, F. Meier, Y. LeCun, M. Rabbat, and N. Ballas, “V-jepa 2: Self-supervised video models enable understanding, prediction and planning,” _arXiv preprint arXiv:2506.09985_ , 2025. 

- [276] C. Chen, Y.-F. Wu, J. Yoon, and S. Ahn, “Transdreamer: Reinforcement learning with transformer world models,” _arXiv preprint arXiv:2202.09481_ , 2022. 

- [277] J. Robine, M. H¨oftmann, T. Uelwer, and S. Harmeling, “Transformer-based world models are happy with 100k 

   - interactions,” in _ICLR_ , 2023. [Online]. Available: https: //openreview.net/forum?id=TdBaDGCpjly 

- [278] J. Bruce, M. Dennis, A. Edwards, J. Parker-Holder, Y. Shi, E. Hughes, M. Lai, A. Mavalankar, R. Steigerwald, C. Apps, Y. Aytar, S. Bechtle, F. M. P. Behbahani, S. Chan, N. M. O. Heess, L. Gonzalez, S. Osindero, S. Ozair, S. Reed, J. Zhang, K. Zolna, J. Clune, N. de Freitas, S. Singh, and T. Rocktaschel, “Genie: Generative interactive environments,” _ArXiv_ , vol. abs/2402.15391, 2024. [Online]. Available: https://api.semantic scholar.org/CorpusID:267897982 

- [279] W. Hong, M. Ding, W. Zheng, X. Liu, and J. Tang, “Cogvideo: Large-scale pretraining for text-to-video generation via transformers,” _arXiv preprint arXiv:2205.15868_ , 2022. 

- [280] C. Wu, J. Liang, L. Ji, F. Yang, Y. Fang, D. Jiang, and N. Duan, “N¨uwa: Visual synthesis pre-training for neural visual world creation,” in _European conference on computer vision_ . Springer, 2022, pp. 720–736. 

- [281] D. Kondratyuk, L. Yu, X. Gu, J. Lezama, J. Huang, G. Schindler, R. Hornung, V. Birodkar, J. Yan, M.-C. Chiu _et al._ , “Videopoet: A large language model for zero-shot video generation,” _arXiv preprint arXiv:2312.14125_ , 2023. 

- [282] A. Hu, L. Russell, H. Yeo, Z. Murez, G. Fedoseev, A. Kendall, J. Shotton, and G. Corrado, “Gaia-1: A generative world model for autonomous driving,” _arXiv preprint arXiv:2309.17080_ , 2023. 

- [283] W. Zheng, W. Chen, Y. Huang, B. Zhang, Y. Duan, and J. Lu, “Occworld: Learning a 3d occupancy world model for autonomous driving,” in _European conference on computer vision_ . Springer, 2024, pp. 55–72. 

- [284] J. Ho, T. Salimans, A. Gritsenko, W. Chan, M. Norouzi, and D. J. Fleet, “Video diffusion models,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 8633–8646, 2022. 

- [285] J. Ho, W. Chan, C. Saharia, J. Whang, R. Gao, A. Gritsenko, D. P. Kingma, B. Poole, M. Norouzi, D. J. Fleet, and T. Salimans, “Imagen video: High definition video generation with diffusion models,” 2022. [Online]. Available: https: //arxiv.org/abs/2210.02303 

- [286] A. Blattmann, R. Rombach, H. Ling, T. Dockhorn, S. W. Kim, S. Fidler, and K. Kreis, “Align your latents: High-resolution video synthesis with latent diffusion models,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2023, pp. 22 563–22 575. 

- [287] A. Blattmann, T. Dockhorn, S. Kulal, D. Mendelevitch, M. Kilian, D. Lorenz, Y. Levi, Z. English, V. Voleti, A. Letts _et al._ , “Stable video diffusion: Scaling latent video diffusion models to large datasets,” _arXiv preprint arXiv:2311.15127_ , 2023. 

- [288] DeepMind, “Veo: a text-to-video generation system,” Google DeepMind, Tech. Rep., 2025, https://deepmind.google/models /veo/. [Online]. Available: https://storage.googleapis.com/dee pmind-media/veo/Veo-3-Tech-Report.pdf 

- [289] X. Wang, Z. Zhu, G. Huang, X. Chen, J. Zhu, and J. Lu, “Drivedreamer: Towards real-world-drive world models for autonomous driving,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 55–72. 

- [290] S. Gao, J. Yang, L. Chen, K. Chitta, Y. Qiu, A. Geiger, J. Zhang, and H. Li, “Vista: A generalizable driving world model with high fidelity and versatile controllability,” _ArXiv_ , vol. abs/2405.17398, 2024. [Online]. Available: https: //api.semanticscholar.org/CorpusID:270062607 

- [291] L. Russell, A. Hu, L. Bertoni, G. Fedoseev, J. Shotton, E. Arani, and G. Corrado, “Gaia-2: A controllable multi-view generative world model for autonomous driving,” _arXiv preprint arXiv:2503.20523_ , 2025. 

- [292] S. Huang, J. Wu, Q. Zhou, S. Miao, and M. Long, “Vid2world: Crafting video diffusion models to interactive world models,” _arXiv preprint arXiv: 2505.14357_ , 2025. 

- [293] K. Zhang, Z. Tang, X. Hu, X. Pan, X. Guo, Y. Liu, J. Huang, L. Yuan, Q. Zhang, X. Long, X. Cao, and W. Yin, “Epona: Autoregressive diffusion world model for autonomous driving,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 

- [294] N. Agarwal, A. Ali, M. Bala, Y. Balaji, E. Barker, T. Cai, P. Chattopadhyay, Y. Chen, Y. Cui, Y. Ding _et al._ , “Cosmos world foundation model platform for physical ai,” _arXiv preprint arXiv:2501.03575_ , 2025. 

- [295] H. A. Alhaija, J. Alvarez, M. Bala, T. Cai, T. Cao, L. Cha, J. Chen, M. Chen, F. Ferroni, S. Fidler _et al._ , “Cosmos-transfer1: Con- 

46 

ditional world generation with adaptive multimodal control,” _arXiv preprint arXiv:2503.14492_ , 2025. 

- [296] C. Min, D. Zhao, L. Xiao, J. Zhao, X. Xu, Z. Zhu, L. Jin, J. Li, Y. Guo, J. Xing, L. Jing, Y. Nie, and B. Dai, “Driveworld: 4d pretrained scene understanding via world models for autonomous driving,” _CVPR_ , pp. 15 522–15 533, 2024. [Online]. Available: https://api.semanticscholar.org/CorpusID:269614067 

- [297] S. Gu, W. Yin, B. Jin, X. Guo, J. Wang, H. Li, Q. Zhang, and X. Long, “Dome: Taming diffusion model into highfidelity controllable occupancy world model,” _arXiv preprint arXiv:2410.10429_ , 2024. 

- [298] A. Team, H. Zhu, Y. Wang, J. Zhou, W. Chang, Y. Zhou, Z. Li, J. Chen, C. Shen, J. Pang _et al._ , “Aether: Geometric-aware unified world modeling,” _arXiv preprint arXiv:2503.18945_ , 2025. 

- [299] J. Chen, H. Zhu, X. He, Y. Wang, J. Zhou, W. Chang, Y. Zhou, Z. Li, Z. Fu, J. Pang _et al._ , “Deepverse: 4d autoregressive video generation as a world model,” _arXiv preprint arXiv:2506.01103_ , 2025. 

- [300] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” _arXiv preprint arXiv:2301.04104_ , 2023. 

- [301] J. Wu, H. Ma, C. Deng, and M. Long, “Pre-training contextualized world models with in-the-wild videos for reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 39 719–39 743, 2023. 

- [302] J. Wu, S. Yin, N. Feng, X. He, D. Li, J. Hao, and M. Long, “ivideogpt: Interactive videogpts are scalable world models,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 68 082–68 119, 2024. 

- [303] A. Van Den Oord, O. Vinyals _et al._ , “Neural discrete representation learning,” _Advances in neural information processing systems_ , vol. 30, 2017. 

- [304] V. Konda and J. Tsitsiklis, “Actor-critic algorithms,” _Advances in neural information processing systems_ , vol. 12, 1999. 

- [305] A. Escontrela, A. Adeniji, W. Yan, A. Jain, X. B. Peng, K. Goldberg, Y. Lee, D. Hafner, and P. Abbeel, “Video prediction models as rewards for reinforcement learning,” 2023. [Online]. Available: https://arxiv.org/abs/2305.14343 

- [306] R. T. McAllister, Y. Gal, A. Kendall, M. Van Der Wilk, A. Shah, R. Cipolla, and A. Weller, “Concrete problems for autonomous vehicle safety: Advantages of bayesian deep learning.” International Joint Conferences on Artificial Intelligence, Inc., 2017. 

- [307] E. Yurtsever, J. Lambert, A. Carballo, and K. Takeda, “A survey of autonomous driving: Common practices and emerging technologies,” _IEEE Access_ , vol. 8, pp. 58 443–58 469, 2020. 

- [308] Y. Zhang, A. Carballo, H. Yang, and K. Takeda, “Perception and sensing for autonomous vehicles under adverse weather conditions: A survey,” _ISPRS Journal of Photogrammetry and Remote Sensing_ , vol. 196, pp. 146–177, 2023. 

- [309] Z. Peng, H. Zhang, Y. Wang, C. Luo, Z. Hu, Y. Jiang, and L. Fan, “Baidu apollo em motion planner,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2019, pp. 3993–4001. 

- [310] National Transportation Safety Board, “Preliminary report highway: Hwy18mh010,” National Transportation Safety Board, Washington, DC, Tech. Rep., 2018. 

- [311] Tesla, Inc., “Tesla ai day 2022,” Tesla, Inc., Tech. Rep., 2022. 

- [312] L. Russell, A. Hu, L. Bertoni, G. Fedoseev, J. Shotton, E. Arani, and G. Corrado, “Gaia-2: A controllable multi-view generative world model for autonomous driving,” _arXiv preprint arXiv:2503.20523_ , 2025. 

- [313] X. Wang, Z. Zhu, G. Huang, X. Chen, J. Zhu, and J. Lu, “Drivedreamer: Towards real-world-drive world models for autonomous driving,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 55–72. 

- [314] G. Zhao, X. Wang, Z. Zhu, X. Chen, G. Huang, X. Bao, and X. Wang, “Drivedreamer-2: Llm-enhanced world models for diverse driving video generation,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 39, no. 10, 2025, pp. 10 412– 10 420. 

- [315] G. Zhao, C. Ni, X. Wang, Z. Zhu, X. Zhang, Y. Wang, G. Huang, X. Chen, B. Wang, Y. Zhang _et al._ , “Drivedreamer4d: World models are effective data machines for 4d driving scene representation,” _arXiv preprint arXiv:2410.13571_ , 2024. 

- [316] R. Gao, K. Chen, E. Xie, L. Hong, Z. Li, D.-Y. Yeung, and Q. Xu, “Magicdrive: Street view generation with diverse 3d geometry control,” _arXiv preprint arXiv:2310.02601_ , 2023. 

- [317] R. Gao, K. Chen, Z. Li, L. Hong, Z. Li, and Q. Xu, “Magicdrive3d: Controllable 3d generation for any-view rendering in street scenes,” _arXiv preprint arXiv:2405.14475_ , 2024. 

- [318] R. Gao, K. Chen, B. Xiao, L. Hong, Z. Li, and Q. Xu, “Magicdrivedit: High-resolution long video generation for autonomous driving with adaptive control,” _arXiv preprint arXiv:2411.13807_ , 2024. 

- [319] Y. Wen, Y. Zhao, Y. Liu, F. Jia, Y. Wang, C. Luo, C. Zhang, T. Wang, X. Sun, and X. Zhang, “Panacea: Panoramic and controllable video generation for autonomous driving,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 6902–6912. 

- [320] J. Lu, Z. Huang, Z. Yang, J. Zhang, and L. Zhang, “Wovogen: World volume-aware diffusion for controllable multi-camera driving scene generation,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 329–345. 

- [321] L. Wang, W. Zheng, Y. Ren, H. Jiang, Z. Cui, H. Yu, and J. Lu, “Occsora: 4d occupancy generation models as world simulators for autonomous driving,” _arXiv preprint arXiv:2405.20337_ , 2024. 

- [322] C. Min, D. Zhao, L. Xiao, J. Zhao, X. Xu, Z. Zhu, L. Jin, J. Li, Y. Guo, J. Xing _et al._ , “Driveworld: 4d pre-trained scene understanding via world models for autonomous driving,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 15 522–15 533. 

- [323] Y. Yang, J. Mei, Y. Ma, S. Du, W. Chen, Y. Qian, Y. Feng, and Y. Liu, “Driving in the occupancy world: Vision-centric 4d occupancy forecasting and planning via world models for autonomous driving,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 39, no. 9, 2025, pp. 9327–9335. 

- [324] X. Guo, C. Ding, H. Dou, X. Zhang, W. Tang, and W. Wu, “Infinitydrive: Breaking time limits in driving world models,” _arXiv preprint arXiv:2412.01522_ , 2024. 

- [325] C. Ni, G. Zhao, X. Wang, Z. Zhu, W. Qin, G. Huang, C. Liu, Y. Chen, Y. Wang, X. Zhang _et al._ , “Recondreamer: Crafting world models for driving scene reconstruction via online restoration,” _arXiv preprint arXiv:2411.19548_ , 2024. 

- [326] F. Jia, W. Mao, Y. Liu, Y. Zhao, Y. Wen, C. Zhang, X. Zhang, and T. Wang, “Adriver-i: A general world model for autonomous driving,” _arXiv preprint arXiv:2311.13549_ , 2023. 

- [327] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu, A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom, “nuscenes: A multimodal dataset for autonomous driving,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 11 621–11 631. 

- [328] P. Sun, H. Kretzschmar, X. Dotiwalla, A. Chouard, V. Patnaik, P. Tsui, J. Guo, Y. Zhou, Y. Chai, B. Caine _et al._ , “Scalability in perception for autonomous driving: Waymo open dataset,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 2446–2454. 

- [329] X. Hu, W. Yin, M. Jia, J. Deng, X. Guo, Q. Zhang, X. Long, and P. Tan, “Drivingworld: Constructingworld model for autonomous driving via video gpt,” _arXiv preprint arXiv:2412.19505_ , 2024. 

- [330] N. Karnchanachari, D. Geromichalos, K. S. Tan, N. Li, C. Eriksen, S. Yaghoubi, N. Mehdipour, G. Bernasconi, W. K. Fong, Y. Guo _et al._ , “Towards learning-based planning: The nuplan benchmark for real-world autonomous driving,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 629–636. 

- [331] X. Tian, T. Jiang, L. Yun, Y. Mao, H. Yang, Y. Wang, Y. Wang, and H. Zhao, “Occ3d: A large-scale 3d occupancy prediction benchmark for autonomous driving,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 64 318–64 330, 2023. 

- [332] Z. Yang, Z. Qian, X. Li, W. Xu, G. Zhao, R. Yu, L. Zhu, and L. Liu, “Dualdiff+: Dual-branch diffusion for high-fidelity video generation with reward guidance,” _arXiv preprint arXiv:2503.03689_ , 2025. 

- [333] A. Chen, W. Zheng, Y. Wang, X. Zhang, K. Zhan, P. Jia, K. Keutzer, and S. Zhang, “Geodrive: 3d geometry-informed driving world model with precise action control,” _arXiv preprint arXiv:2505.22421_ , 2025. 

- [334] O. Contributors, “Openscene: The largest up-to-date 3d occupancy prediction benchmark in autonomous driving,” https: //github.com/OpenDriveLab/OpenScene, 2023. 

- [335] J. Houston, G. Zuidhof, L. Bergamini, Y. Ye, L. Chen, A. Jain, S. Omari, V. Iglovikov, and P. Ondruska, “One thousand and one hours: Self-driving motion prediction dataset,” in _Conference on Robot Learning_ . PMLR, 2021, pp. 409–418. 

47 

- [336] Z. Yan, W. Dong, Y. Shao, Y. Lu, L. Haiyang, J. Liu, H. Wang, Z. Wang, Y. Wang, F. Remondino _et al._ , “Renderworld: World model with self-supervised 3d label,” _arXiv preprint arXiv:2409.11356_ , 2024. 

- [337] J. Wei, S. Yuan, P. Li, Q. Hu, Z. Gan, and W. Ding, “Occllama: An occupancy-language-action generative world model for autonomous driving,” _arXiv preprint arXiv:2409.03272_ , 2024. 

- [338] T. Qian, J. Chen, L. Zhuo, Y. Jiao, and Y.-G. Jiang, “Nuscenesqa: A multi-modal visual question answering benchmark for autonomous driving scenario,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 38, no. 5, 2024, pp. 4542–4550. 

- [339] Y. Zhang, S. Gong, K. Xiong, X. Ye, X. Tan, F. Wang, J. Huang, H. Wu, and H. Wang, “Bevworld: A multimodal world model for autonomous driving via unified bev latent space,” _arXiv preprint arXiv:2407.05679_ , 2024. 

- [340] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun, “Carla: An open urban driving simulator,” in _Conference on robot learning_ . PMLR, 2017, pp. 1–16. 

- [341] Z. Wu, J. Ni, X. Wang, Y. Guo, R. Chen, L. Lu, J. Dai, and Y. Xiong, “Holodrive: Holistic 2d-3d multi-modal street scene generation for autonomous driving,” _arXiv preprint arXiv:2412.01407_ , 2024. 

- [342] M. Hassan, S. Stapf, A. Rahimi, P. Rezende, Y. Haghighi, D. Br¨uggemann, I. Katircioglu, L. Zhang, X. Chen, S. Saha _et al._ , “Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control,” _arXiv preprint arXiv:2412.11198_ , 2024. 

- [343] H. Xu, Y. Gao, F. Yu, and T. Darrell, “End-to-end learning of driving models from large-scale video datasets,” in _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 2017, pp. 2174–2182. 

- [344] J. Yang, S. Gao, Y. Qiu, L. Chen, T. Li, B. Dai, K. Chitta, P. Wu, J. Zeng, P. Luo _et al._ , “Generalized predictive model for autonomous driving,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 14 662–14 672. 

- [345] K. Grauman, A. Westbury, L. Torresani, K. Kitani, J. Malik, T. Afouras, K. Ashutosh, V. Baiyya, S. Bansal, B. Boote _et al._ , “Ego-exo4d: Understanding skilled human activity from firstand third-person perspectives,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 19 383–19 400. 

- [346] X. Yang, L. Wen, Y. Ma, J. Mei, X. Li, T. Wei, W. Lei, D. Fu, P. Cai, M. Dou _et al._ , “Drivearena: A closed-loop generative simulation platform for autonomous driving,” _arXiv preprint arXiv:2408.00415_ , 2024. 

- [347] H. Arai, K. Ishihara, T. Takahashi, and Y. Yamaguchi, “Act-bench: Towards action controllable world models for autonomous driving,” _arXiv preprint arXiv:2412.05337_ , 2024. 

- [348] Z. Yang, X. Guo, C. Ding, C. Wang, and W. Wu, “Pysical informed driving world model,” _arXiv preprint arXiv:2412.08410_ , 2024. 

- [349] X. Ren, Y. Lu, T. Cao, R. Gao, S. Huang, A. Sabour, T. Shen, T. Pfaff, J. Z. Wu, R. Chen _et al._ , “Cosmos-drive-dreams: Scalable synthetic driving data generation with world foundation models,” _arXiv preprint arXiv:2506.09042_ , 2025. 

- [350] A. Hu, G. Corrado, N. Griffiths, Z. Murez, C. Gurau, H. Yeo, A. Kendall, R. Cipolla, and J. Shotton, “Model-based imitation learning for urban driving,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 20 703–20 716, 2022. 

- [351] A. Azzolini, H. Brandon, P. Chattopadhyay, H. Chen, J. Chu, Y. Cui, J. Diamond, Y. Ding, F. Ferroni, R. Govindaraju _et al._ , “Cosmos-reason1: From physical common sense to embodied reasoning,” _arXiv preprint arXiv:2503.15558_ , 2025. 

- [352] Z. Zhang, A. Liniger, D. Dai, F. Yu, and L. Van Gool, “Trafficbots: Towards world models for autonomous driving simulation and motion prediction,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 1522–1529. 

- [353] C. Min, D. Zhao, L. Xiao, Y. Nie, and B. Dai, “Uniworld: Autonomous driving pre-training via world models,” _arXiv preprint arXiv:2308.07234_ , 2023. 

- [354] L. Zhang, Y. Xiong, Z. Yang, S. Casas, R. Hu, and R. Urtasun, “Copilot4d: Learning unsupervised world models for autonomous driving via discrete diffusion,” _arXiv preprint arXiv:2311.01017_ , 2023. 

- [355] A. Geiger, P. Lenz, C. Stiller, and R. Urtasun, “Vision meets robotics: The kitti dataset,” _The international journal of robotics research_ , vol. 32, no. 11, pp. 1231–1237, 2013. 

- [356] D. Bogdoll, Y. Yang, T. Joseph, and J. M. Z¨ollner, “Muvo: A multi- 

   - modal world model with spatial representations for autonomous driving,” _arXiv preprint arXiv:2311.11762_ , 2023. 

- [357] Z. Yang, L. Chen, Y. Sun, and H. Li, “Visual point cloud forecasting enables scalable autonomous driving,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 14 673–14 684. 

- [358] Q. Li, X. Jia, S. Wang, and J. Yan, “Think2drive: Efficient reinforcement learning by thinking with latent world model for autonomous driving (in carla-v2),” in _European Conference on Computer Vision_ . Springer, 2024, pp. 142–158. 

- [359] V. Zyrianov, H. Che, Z. Liu, and S. Wang, “Lidardm: Generative lidar simulation in a generated world,” _arXiv preprint arXiv:2404.02903_ , 2024. 

- [360] Y. Li, L. Fan, J. He, Y. Wang, Y. Chen, Z. Zhang, and T. Tan, “Enhancing end-to-end autonomous driving with latent world model,” _arXiv preprint arXiv:2406.08481_ , 2024. 

- [361] D. Dauner, M. Hallgarten, T. Li, X. Weng, Z. Huang, Z. Yang, H. Li, I. Gilitschenski, B. Ivanovic, M. Pavone _et al._ , “Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 28 706–28 719, 2024. 

- [362] B. Agro, Q. Sykora, S. Casas, T. Gilles, and R. Urtasun, “Uno: Unsupervised occupancy fields for perception and forecasting,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 14 487–14 496. 

- [363] S. Hamdan and F. G¨uney, “Carformer: Self-driving with learned object-centric representations,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 177–193. 

- [364] Z. Huang, J. Zhang, and E. Ohn-Bar, “Neural volumetric world models for autonomous driving,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 195–213. 

- [365] A. Popov, A. Degirmenci, D. Wehr, S. Hegde, R. Oldja, A. Kamenev, B. Douillard, D. Nist´er, U. Muller, R. Bhargava _et al._ , “Mitigating covariate shift in imitation learning for autonomous vehicles using latent space generative world models,” _arXiv preprint arXiv:2409.16663_ , 2024. 

- [366] A. Garg and K. M. Krishna, “Imagine-2-drive: High-fidelity world modeling in carla for autonomous vehicles,” _arXiv preprint arXiv:2411.10171_ , 2024. 

- [367] W. Zheng, Z. Xia, Y. Huang, S. Zuo, J. Zhou, and J. Lu, “Doe-1: Closed-loop autonomous driving with large world model,” _arXiv preprint arXiv:2412.09627_ , 2024. 

- [368] S. Zuo, W. Zheng, Y. Huang, J. Zhou, and J. Lu, “Gaussianworld: Gaussian world model for streaming 3d occupancy prediction,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 6772–6781. 

- [369] H. Zhang, Y. Xue, X. Yan, J. Zhang, W. Qiu, D. Bai, B. Liu, S. Cui, and Z. Li, “An efficient occupancy world model via decoupled dynamic flow and image-assisted training,” _arXiv preprint arXiv:2412.13772_ , 2024. 

- [370] Y. Chen, Y. Wang, and Z. Zhang, “Drivinggpt: Unifying driving world modeling and planning with multi-modal autoregressive transformers,” _arXiv preprint arXiv:2412.18607_ , 2024. 

- [371] H. Wang, X. Ye, F. Tao, C. Pan, A. Mallik, B. Yaman, L. Ren, and J. Zhang, “Adawm: Adaptive world model based planning for autonomous driving,” _arXiv preprint arXiv:2501.13072_ , 2025. 

- [372] H. Zhu, Z. Dong, K. Topollai, and A. Choromanska, “Ad-ljepa: Self-supervised spatial world models with joint embedding predictive architecture for autonomous driving with lidar data,” _arXiv preprint arXiv:2501.04969_ , 2025. 

- [373] X. Zhou, D. Liang, S. Tu, X. Chen, Y. Ding, D. Zhang, F. Tan, H. Zhao, and X. Bai, “Hermes: A unified self-driving world model for simultaneous 3d scene understanding and generation,” _arXiv preprint arXiv:2501.14729_ , 2025. 

- [374] Z. Gao, Y. Mu, C. Chen, J. Duan, P. Luo, Y. Lu, and S. E. Li, “Enhance sample efficiency and robustness of end-to-end urban autonomous driving via semantic masked world model,” _IEEE Transactions on Intelligent Transportation Systems_ , 2024. 

- [375] M. Pan, X. Zhu, Y. Wang, and X. Yang, “Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models,” _Advances in neural information processing systems_ , vol. 35, pp. 23 178–23 191, 2022. 

- [376] S. Gao, J. Yang, L. Chen, K. Chitta, Y. Qiu, A. Geiger, J. Zhang, and H. Li, “Vista: A generalizable driving world model with high fidelity and versatile controllability,” _arXiv preprint arXiv:2405.17398_ , 2024. 

48 

- [377] K. Li, K. Chen, H. Wang, L. Hong, C. Ye, J. Han, Y. Chen, W. Zhang, C. Xu, D.-Y. Yeung _et al._ , “Coda: A real-world road corner case dataset for object detection in autonomous driving,” in _European Conference on Computer Vision_ . Springer, 2022, pp. 406–423. 

- [378] Y. Wang, J. He, L. Fan, H. Li, Y. Chen, and Z. Zhang, “Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 14 749–14 759. 

- [379] Y. Li, Y. Wang, Y. Liu, J. He, L. Fan, and Z. Zhang, “End-to-end driving with online trajectory evaluation via bev world model,” _arXiv preprint arXiv:2504.01941_ , 2025. 

- [380] A. Jiang, Y. Gao, Y. Wang, Z. Sun, S. Wang, Y. Heng, H. Sun, S. Tang, L. Zhu, J. Chai _et al._ , “Irl-vla: Training an visionlanguage-action policy via reward world model,” _arXiv preprint arXiv:2508.06571_ , 2025. 

- [381] Z. Zhang, R. Chen, J. Ye, Y. Sun, P. Wang, J. Pang, K. Li, T. Liu, H. Lin, Y. Yu _et al._ , “Whale: Towards generalizable and scalable world models for embodied decision-making,” _arXiv preprint arXiv:2411.05619_ , 2024. 

- [382] S. Zhou, Y. Du, J. Chen, Y. Li, D.-Y. Yeung, and C. Gan, “Robodreamer: Learning compositional world models for robot imagination,” _arXiv preprint arXiv:2404.12377_ , 2024. 

- [383] L. Barcellona, A. Zadaianchuk, D. Allegro, S. Papa, S. Ghidoni, and E. Gavves, “Dream to manipulate: Compositional world models empowering robot imitation learning with imagination,” _arXiv preprint arXiv:2412.14957_ , 2024. 

- [384] J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y.-C. Lin _et al._ , “Dreamgen: Unlocking generalization in robot learning through neural trajectories,” _arXiv preprint arXiv:2505.12705_ , 2025. 

- [385] S. Huang, L. Chen, P. Zhou, S. Chen, Z. Jiang, Y. Hu, Y. Liao, P. Gao, H. Li, M. Yao _et al._ , “Enerverse: Envisioning embodied future space for robotics manipulation,” _arXiv preprint arXiv:2501.01895_ , 2025. 

- [386] Y. Li, Y. Zhu, J. Wen, C. Shen, and Y. Xu, “Worldeval: World model as real-world robot policies evaluator,” _arXiv preprint arXiv:2505.19017_ , 2025. 

- [387] “Pangu multimodal model,” 2025. [Online]. Available: https: //www.huaweicloud.com/product/pangu/multimodal.html 

- [388] L. Liu, X. Wang, G. Zhao, K. Li, W. Qin, J. Qiu, Z. Zhu, G. Huang, and Z. Su, “Robotransfer: Geometry-consistent video diffusion for robotic visual policy transfer,” _arXiv preprint arXiv:2505.23171_ , 2025. 

- [389] H. Zhen, Q. Sun, H. Zhang, J. Li, S. Zhou, Y. Du, and C. Gan, “Tesseract: learning 4d embodied world models,” _arXiv preprint arXiv:2504.20995_ , 2025. 

- [390] S. Zhou, Y. Du, Y. Yang, L. Han, P. Chen, D.-Y. Yeung, and C. Gan, “Learning 3d persistent embodied world models,” _arXiv preprint arXiv:2505.05495_ , 2025. 

- [391] Y. Hu, J. Wu, R. Xu, H. Liu, A. Xi, H. X. Liu, R. Vasudevan, and M. Ghaffari, “Imaginative world modeling with scene graphs for embodied agent navigation,” _arXiv preprint arXiv:2508.06990_ , 2025. 

- [392] B. Wang, X. Meng, X. Wang, Z. Zhu, A. Ye, Y. Wang, Z. Yang, C. Ni, G. Huang, and X. Wang, “Embodiedreamer: Advancing real2sim2real transfer for policy training via embodied world modeling,” _arXiv preprint arXiv:2507.05198_ , 2025. 

- [393] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” _arXiv preprint arXiv:1912.01603_ , 2019. 

- [394] M. Okada and T. Taniguchi, “Dreamingv2: Reinforcement learning with discrete world models without reconstruction,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 985–991. 

- [395] ——, “Dreaming: Model-based reinforcement learning by latent imagination without reconstruction,” in _2021 ieee international conference on robotics and automation (icra)_ . IEEE, 2021, pp. 4209– 4215. 

- [396] ——, “Dreamingv2: Reinforcement learning with discrete world models without reconstruction. in 2022 ieee,” in _RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 985–991. 

- [397] F. Deng, I. Jang, and S. Ahn, “Dreamerpro: Reconstruction-free model-based reinforcement learning with prototypical representations,” in _International Conference on Machine Learning_ . PMLR, 2022, pp. 4956–4975. 

- [398] R. Mendonca, O. Rybkin, K. Daniilidis, D. Hafner, and D. Pathak, “Discovering and achieving goals via world models,” _Advances in Neural Information Processing Systems_ , vol. 34, pp. 24 379–24 391, 2021. 

- [399] Y. Feng, N. Hansen, Z. Xiong, C. Rajagopalan, and X. Wang, “Finetuning offline world models in the real world,” _arXiv preprint arXiv:2310.16029_ , 2023. 

- [400] R. Mendonca, S. Bahl, and D. Pathak, “Structured world models from human videos,” _arXiv preprint arXiv:2308.10901_ , 2023. 

- [401] X. Gu, Y.-J. Wang, X. Zhu, C. Shi, Y. Guo, Y. Liu, and J. Chen, “Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning,” _arXiv preprint arXiv:2408.14472_ , 2024. 

- [402] P. Ren, K. Zhang, H. Zheng, Z. Li, Y. Wen, F. Zhu, M. Ma, and X. Liang, “Surfer: Progressive reasoning with world models for robotic manipulation,” _arXiv preprint arXiv:2306.11335_ , 2023. 

- [403] H. Lin, B. Li, C. W. Wong, J. Rojas, X. Chu, and K. W. S. Au, “World models for general surgical grasping,” _arXiv preprint arXiv:2405.17940_ , 2024. 

- [404] N. Hansen, J. SV, V. Sobal, Y. LeCun, X. Wang, and H. Su, “Hierarchical world models as visual whole-body humanoid controllers,” _arXiv preprint arXiv:2405.18418_ , 2024. 

- [405] J. Yamada, M. Rigter, J. Collins, and I. Posner, “Twist: Teacherstudent world model distillation for efficient sim-to-real transfer,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 9190–9196. 

- [406] K. Zhang, P. Ren, B. Lin, J. Lin, S. Ma, H. Xu, and X. Liang, “Pivotr: Primitive-driven waypoint-aware world model for robotic manipulation,” _arXiv preprint arXiv:2410.10394_ , 2024. 

- [407] H. Ma, J. Wu, N. Feng, C. Xiao, D. Li, J. Hao, J. Wang, and M. Long, “Harmonydream: Task harmonization inside world models,” _arXiv preprint arXiv:2310.00344_ , 2023. 

- [408] W. Huang, J. Ji, C. Xia, B. Zhang, and Y. Yang, “Safedreamer: Safe reinforcement learning with world models,” _arXiv preprint arXiv:2307.07176_ , 2023. 

- [409] H. Lai, J. Cao, J. Xu, H. Wu, Y. Lin, T. Kong, Y. Yu, and W. Zhang, “World model-based perception for visual legged locomotion,” _arXiv preprint arXiv:2409.16784_ , 2024. 

- [410] C. Li, A. Krause, and M. Hutter, “Robotic world model: A neural network simulator for robust policy optimization in robotics,” _arXiv preprint arXiv:2501.10100_ , 2025. 

- [411] ——, “Offline robotic world model: Learning robotic policies without a physics simulator,” _arXiv preprint arXiv:2504.16680_ , 2025. 

- [412] E. Aljalbout, M. Krinner, A. Romero, and D. Scaramuzza, “Accelerating model-based reinforcement learning with state-space world models,” in _ICLR 2025 Workshop on World Models: Understanding, Modelling and Scaling_ . 

- [413] W. Sun, L. Chen, Y. Su, B. Cao, Y. Liu, and Z. Xie, “Learning humanoid locomotion with world model reconstruction,” _arXiv preprint arXiv:2502.16230_ , 2025. 

- [414] W. Li, H. Zhao, Z. Yu, Y. Du, Q. Zou, R. Hu, and K. Xu, “Pin-wm: Learning physics-informed world models for non-prehensile manipulation,” _arXiv preprint arXiv:2504.16693_ , 2025. 

- [415] I. Nematollahi, B. DeMoss, A. L. Chandra, N. Hawes, W. Burgard, and I. Posner, “Lumos: Language-conditioned imitation learning with world models,” _arXiv preprint arXiv:2503.10370_ , 2025. 

- [416] R. G. Goswami, P. Krishnamurthy, Y. LeCun, and F. Khorrami, “Osvi-wm: One-shot visual imitation for unseen tasks using world-model-guided trajectory generation,” _arXiv preprint arXiv:2505.20425_ , 2025. 

- [417] S. Ferraro, P. Mazzaglia, T. Verbelen, and B. Dhoedt, “Focus: Object-centric world models for robotic manipulation,” _Frontiers in Neurorobotics_ , vol. 19, p. 1585386, 2025. 

- [418] C. Gao, H. Zhang, Z. Xu, C. Zhehao, and L. Shao, “Flip: Flowcentric generative planning as general-purpose manipulation world model,” in _The Thirteenth International Conference on Learning Representations_ . 

- [419] Y. Jiang, S. Chen, S. Huang, L. Chen, P. Zhou, Y. Liao, X. He, C. Liu, H. Li, M. Yao _et al._ , “Enerverse-ac: Envisioning embodied environments with action condition,” _arXiv preprint arXiv:2505.09723_ , 2025. 

- [420] J. Guo, X. Ma, Y. Wang, M. Yang, H. Liu, and Q. Li, “Flowdreamer: A rgb-d world model with flow-based motion representations for robot manipulation,” _arXiv preprint arXiv:2505.10075_ , 2025. 

49 

- [421] M. Q. Ali, A. Sridhar, S. Matiana, A. Wong, and M. Al-Sharman, “Humanoid world models: Open world foundation models for humanoid robotics,” _arXiv preprint arXiv:2506.01182_ , 2025. 

- [422] P. Lancaster, N. Hansen, A. Rajeswaran, and V. Kumar, “Modemv2: Visuo-motor world models for real-world robot manipulation,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 7530–7537. 

- [423] S. Gao, S. Zhou, Y. Du, J. Zhang, and C. Gan, “Adaworld: Learning adaptable world models with latent actions,” _arXiv preprint arXiv:2503.18938_ , 2025. 

- [424] C. Hao, W. Lu, Y. Xu, and Y. Chen, “Neural motion simulator pushing the limit of world models in reinforcement learning,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 27 608–27 617. 

- [425] F. R¨oder, J. Benad, M. Eppe, and P. K. Banerjee, “Dynamicsaligned latent imagination in contextual world models for zeroshot generalization,” _arXiv preprint arXiv:2508.20294_ , 2025. 

- [426] G. Lu, B. Jia, P. Li, Y. Chen, Z. Wang, Y. Tang, and S. Huang, “Gwm: Towards scalable gaussian world models for robotic manipulation,” _Proceedings of International Conference on Computer Vision (ICCV)_ , 2025. 

- [427] A. Escontrela, A. Adeniji, W. Yan, A. Jain, X. B. Peng, K. Goldberg, Y. Lee, D. Hafner, and P. Abbeel, “Video prediction models as rewards for reinforcement learning,” _Neural Information Processing Systems_ , 2023. 

- [428] Z. Zhang, R. Chen, J. Ye, Y. Sun, P. Wang, J.-C. Pang, K. Li, T.S. Liu, H. Lin, and Y. Yu, “Whale-x: Learning scalable embodied world models with enhanced generalizability.” 

- [429] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson, “Learning latent dynamics for planning from pixels,” in _International conference on machine learning_ . PMLR, 2019, pp. 2555–2565. 

- [430] M. Krinner, E. Aljalbout, A. Romero, and D. Scaramuzza, “Accelerating model-based reinforcement learning with state-space world models,” _arXiv preprint arXiv:2502.20168_ , 2025. 

- [431] M. Assran, Q. Duval, I. Misra, P. Bojanowski, P. Vincent, M. Rabbat, Y. LeCun, and N. Ballas, “Self-supervised learning from images with a joint-embedding predictive architecture,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 15 619–15 629. 

- [432] R. Gautam Goswami, P. Krishnamurthy, Y. LeCun, and F. Khorrami, “Osvi-wm: One-shot visual imitation for unseen tasks using world-model-guided trajectory generation,” _arXiv e-prints_ , pp. arXiv–2505, 2025. 

