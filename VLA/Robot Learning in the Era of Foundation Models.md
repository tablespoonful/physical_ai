---
title: "Robot Learning in the Era of Foundation Models: A Survey"
date: "2023-11-24"
authors: "Xuan Xiao; Jiahang Liu; Zhipeng Wang; Yanmin Zhou; Yong Qi; Qian Cheng"
url: https://arxiv.org/abs/2311.14379
pdf: https://arxiv.org/pdf/2311.14379
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2311.14379)** / [論文ページ](https://arxiv.org/abs/2311.14379)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Robot Learning in the Era of Foundation Models: A Survey 

Xuan Xiao<sup>1,2,4</sup> , Jiahang Liu<sup>1,2,3</sup> , Zhipeng Wang<sup>1,2,3</sup> , Yanmin Zhou<sup>1,2,3</sup> , Yong Qi<sup>5</sup> , Qian Cheng<sup>1,2,4</sup> , Bin He<sup>1,2,3</sup> , Shuo Jiang<sup>1,2,3</sup> * 

**Abstract:** The proliferation of Large Language Models (LLMs) has s fueled a shift in robot learning from automation towards general embodied Artificial Intelligence (AI). Adopting foundation models together with traditional learning methods to robot learning has increasingly gained recent interest research community and showed potential for real-life application. However, there are few literatures comprehensively reviewing the relatively new technologies combined with robotics. The purpose of this review is to systematically assess the state-of-the-art foundation model techniques in the robot learning and to identify future potential areas. Specifically, we first summarized the technical evolution of robot learning and identified the necessary preliminary preparations for foundation models including the simulators, datasets, foundation model framework. In addition, we focused on the following four mainstream areas of robot learning including manipulation, navigation, planning, and reasoning and demonstrated how the foundation model techniques can be adopted in the above scenarios. Furthermore, critical issues which are neglected in the current literatures including robot hardware and software decoupling, dynamic data, generalization performance with the presence of human, etc. were discussed. This review highlights the state-of-the-art progress of foundation models in robot learning and future research should focus on multimodal interaction especially dynamics data, exclusive foundation models for robots, and AI alignment, etc. 

**Keywords:** Robot Learning, Foundation Models, Embodied AI 

# **1 Introduction** 

Robots have played an important role in various scenarios including industrial<sup>[1]</sup> , medical<sup>[2]</sup> , service<sup>[3]</sup> and special robot<sup>[4]</sup> industry. With the increasing task complexity and working environment variability, the demands for robot tasks have shifted from fixed automation to general artificial intelligence, where robot learning will be the core enabling techniques of the autonomous systems<sup>[5]</sup> . 

The field of robot learning lies at the junction of machine learning and robotics. Its primary focus is enabling 

robots to acquire new skills or adapt to their environment by utilizing learning algorithms. Some examples of skills that learning algorithms target include sensorimotor skills (like locomotion, grasping and active object classification), interaction skills (such as co-manipulating objects with humans) and linguistic skills (including the grounded and situated meaning of human language). Learning can be acquired through autonomous self-exploration or through demonstrated teaching. 

Extensive research studies have been performed on how to realize robot learning. Traditional robot learning techniques are generally divided into imitation learning<sup>[6-9]</sup> and reinforcement learning<sup>[10, 11]</sup> . Imitation learning enables robots to learn new skills by mimicking human behavior, while reinforcement learning allows robots to optimize the outcome of skill execution. Imitation learning is an important way to initialize and improve learning efficiency in reinforcement learning. However, they all suffer from certain limitations. Imitation learning is a straightforward and stable form of supervised learning. It requires labeled behavior data and is unable to surpass human-level performance. Although reinforcement learning has the potential to surpass human-level performance, it requires defining the reward function, addressing the policy exploration challenge, and may encounter convergence issues and instability during training. The characteristics of robot learning is that robots are physically embodied and environmentally situated. Thus, a critical challenge in robot learning is to close the perception-action loop in the practical scenarios and there are still some problems in the practical application of traditional robot learning, including insufficient generalization of tasks, insufficient environmental adaptability, low execution accuracy, and lack of planning and reasoning capabilities<sup>[12-14]</sup> . Recently, with the release of ChatGPT, foundation models, particularly multi-modal foundation models, presented both opportunities and challenges for robot learning. LLMs have demonstrated significant potential in achieving human-level intelligence, thereby leading to a surge of research in robotics based on LLMs. Leveraging multi-domain prior knowledge, LLMs have made breakthroughs in understanding complex task, engaging in 

1 National Key Laboratory of Autonomous Intelligent Unmanned Systems, Tongji University, Shanghai, China. 

2 Frontiers Science Center for Intelligent Autonomous Systems, Ministry of Education, Tongji University, Shanghai, China. 

- 3 College of Electronics and Information Engineering Tongji University, Shanghai, China. 

4 Institute of Acoustics, School of Physics Science and Engineering, Tongji University, Shanghai, China. 

5 School of Electronic Information and Artificial Intelligence, Shaanxi University of Science and Technology, Shaanxi, China. 

This work was supported by National Key Research and Development Program of China under Grant 2020AAA0108905, National Natural Science Foundation 

of China (Grant No. 62088101, 52105033), and the Shanghai Municipal Science and Technology Major Project (2021SHZDZX0100). (*Corresponding author�Shuo 

Jiang) 

continuous dialogue, and performing zero-sample reasoning. However, LLMs still lack the general perception ability of the external environment, which can be addressed by employing the multi-modal foundation model incorporating 2D&3D vision, LiDAR, voice, inertial motion unit (IMU), etc. To fully unleash the potential of the foundational model and address the current challenges in robot learning, so that robots can learn human behavior and skillfully undertake a series of tasks, researchers have developed task-specific robot learning architectures. However, these models were proposed independently and relatively recently. Upon thorough investigation, existing surveys on robot learning are primarily focused on a single task and predominantly rely on traditional methods<sup>[5, 15-19]</sup> . There are few literature reviews on multi-task robot learning based on foundation models. Therefore, it is crucial to construct an overall summary analysis of existing LLM-based robot learning work, which is of great significance for a comprehensive understanding of the field and to provide inspiration for future research<sup>[20]</sup> . 

the embodied AI need? What foundation model algorithms, strategies, and mechanisms are currently used for downstream tasks in robot learning? What are promising future research areas in robotics learning for current research questions? In this paper, we systematically survey the relatively new field of foundation model-based robot learning, establish a clear taxonomy for the existing research in the field, focusing on the four aspects of robot learning: manipulation, navigation, planning, and reasoning. We also identify several challenges in this field and discuss potential future directions. The article follows the organizational structure presented below (Fig. 1). 

We select references based on the following criteria: 1) Our primary objective is to encompass all significant milestones in robot learning during the advent of foundation models across diverse tasks. 2) the diversity and significance of subfields and research groups should be considered. 3) A valuable source entails conducting a reverse search beginning with highly influential publications<sup>[21]</sup> . 

We organize this survey according to the solutions of the following three research questions. What platforms does 


Fig.1. Overall structure of the survey. 

# **2 Overview** 

# 2.1 Technical Evolution 

In the exploration and discovery of robot learning, it has gone through different stages of historical evolution (Fig.2). 

They can be summarized as the following four categories: robot learning through teaching programming (TP) including kinesthetic teaching and teleoperation, reinforcement learning in interaction, embodied imitation learning<sup>[22, 23]</sup> and learning in AIGC-based generative models<sup>[24-26]</sup> . 


Fig.2. Technical Evolution<sup>[27-30]</sup> . 

Kinesthetic teaching<sup>[31]</sup> involves physically maneuvering the robot to perform the necessary actions, while the robot’s onboard sensors record status information, which is then used to generate training data for the machine learning model. Although this method is relatively simple, the quality of the demonstration relies heavily on the operator's ability to perform movements with flexibility and smoothness. While it proves highly effective for robotic arms, its application becomes more challenging on other platforms, such as legged robots or dexterous hands. Another demonstration method is teleoperation<sup>[32]</sup> , which enables trajectory learning, task learning, grabbing or more advanced tasks, by providing external input to the robot through handles, graphical interfaces or other methods. There are currently a variety of interactive devices (such as haptic devices or VR interactive devices). In contrast to kinesthetic teaching, teleoperation allows for remote implementation, eliminating the need for the user and the robot to be physically present at the same site. Limitations of teleoperation include the additional work required to develop input interfaces, a longer user training process, and usability risks posed by external devices. 

Reinforcement learning involves determining optimal actions in a given situation to maximize the digital revenue 

signal. Rather than being explicitly instructed on which actions to take, learners must independently identify the actions that yield the greatest benefits. Reinforcement learning focuses on finding a balance between exploring unknown territory and leveraging current knowledge. A typical framework for a reinforcement learning scenario: an agent takes an action in the environment, and the action is interpreted as a reward and state representation, which is then fed back to the agent<sup>[33]</sup> . 

Embodied imitation learning<sup>[34]</sup> mainly involves robots learning by observing the actions of the demonstrator (such as watching videos). In this method, the presenter utilizes their own body to perform the task, while an external device records their movements. This approach proves to be the most straightforward for presenters, as it does not necessitate any training in the presentation process. Furthermore, this approach can be extended to robots with multiple degrees of freedom, including non-anthropomorphic robots. However, enabling this approach involves mapping human actions to robot-executable actions, which presents challenges such as occlusion, rapid movement, and sensor noise during demonstrations. 

By integrating foundation models<sup>[25]</sup> with robots, based on their embodied intelligence, zero-sample training is 

achieved for motion planning and execution in real-world scenarios, resulting in human-like motion control logic and capabilities. This type of robot obtains general knowledge from foundation models and addresses cognitive deficiencies through perceptual intelligence, such as vision. This marks the initial steps towards the industrialization of embodied intelligent robots. 

# 2.2 Preliminary Preparations 

Developing a learning model for robots is not an easy task<sup>[35, 36]</sup> , given the challenges of technical issues<sup>[37, 38]</sup> including computing resources, algorithms and data. A feasible approach is to perform incremental development or experimental verification on the basis of existing models. In this section, we briefly organize publicly available resources<sup>[39-45]</sup> for robot learning, including simulators, datasets<sup>[46-49]</sup> , foundation models<sup>[36]</sup> . 

As developing and testing applications with real robots is expensive and time-consuming, simulation has emerged as a crucial component in the field of robotics application development. The validation of applications in simulation prior to deployment on robots can shorten iteration time by identifying potential issues at an early stage. Simulation facilitates the testing of corner cases or scenarios that could pose risks in the real world. To validate and assess the performance and effectiveness of robot learning, it is beneficial to conduct initial testing in a simulator before transitioning to the real-world environment. Several simulation frameworks<sup>[50]</sup> currently exist for training in robot learning simulations and are summarized in Appendix Table 1. 

are two types of data sets: static data and dynamic data. Static data refers to related data sets collected on the Internet, and dynamic data refers to data generated through interactions with robots in a real-world environment. Currently, the majority of existing datasets consist of static data, and the specifics of prominent datasets are summarized in Appendix Table 2. Obtaining dynamic data is challenging, and it is relatively scarce. 

Foundation models<sup>[51]</sup> are inseparable from the support of computing power, algorithms and data. The chip determines the computing power. Higher-performance chips are necessary for the training and construction of the neural network in foundation models. Research institutes currently employ diverse algorithms to implement foundation models. However, the primary difficulty lies in acquiring highquality data. High-quality data plays a crucial role in facilitating AI training and tuning. The following is a summary of notable foundation models in Appendix Table 3. 

Due to the substantial cost of model pre-training, utilizing public API<sup>[52, 53]</sup> allows for remote execution of inference tasks. 

# **3 Downstream Tasks** 

The target and output of robot learning is to help the robot tactfully fulfill a certain task via acquiring a behavior or skill. Common target tasks include robot manipulation, navigation, mission planning, and reasoning (Fig.3). This section investigates and reviews how different works combine foundation models for different downstream tasks to achieve robot learning goals<sup>[54, 55]</sup> . 

To validate the correlation performance in the simulation experiment, it is essential to have a dataset. There 


Fig.3. Downstream Tasks For Robot Learning. 

# 3.1 Manipulation 

# 3.1.1 Characteristic and Challenges 

Tasks, despite being commonly perceived as simple and routine, such as washing dishes, cutting vegetables, and packing clothes, are still challenging for robots and are at the forefront of robotics research<sup>[56]</sup> . The robot manipulation problem deals with how a robot learns to manipulate its surrounding environment<sup>[5]</sup> . It can be formulated as the ability to connect a starting state to a goal state through successive actions, during which the manipulation task is represented by a set of points denoting the starting and goal states, along with the constraints imposed on the transition states<sup>[57]</sup> . Furthermore, the ability to make physical contact is critical to the development of manipulation skills. Currently, robots can only effectively grab and release certain types of objects and perform a variety of simple manipulation actions such as throwing, sliding, pushing, and poking. Challenges emerge when these actions need to be performed in uncluttered environments or when more complex interactions are necessary<sup>[14]</sup> . Foundation models have the capability to engage in interactive dialogues with users, receive and process various types of data, including images, text, and speech. They can utilize multimodal information, such as vision, to guide the actions of the robot or generate corresponding code or action sequences. These capabilities enable robots to effectively adapt to intricate and ever-changing environments, eliminating the need for defining every single possible scenario in advance<sup>[55]</sup> . In this section, we survey the recent research results and latest progress of foundation models in the direction of robot manipulation, including learning of robotic skill primitives, learning of complex robot manipulation tasks, and robot manipulation learning with multimodal fusion. 

# 3.1.2 Methods 

# l Learning of Robotic Skill Primitives 

The approach involves breaking down the problem of robot skill learning into several easily comprehensible skill primitives or movement primitives. Subsequently, suitable and efficient learning methods are devised for these skill primitives, allowing the robot to acquire manipulation skills by combining these primitives. This enables the robot to adapt to new environments and generalize its abilities to perform novel tasks. Researchers are currently exploring the utilization of LLM guidance to facilitate the learning of action primitives for skill completion<sup>[58, 59]</sup> . 

The ActivityPrograms knowledge base<sup>[60]</sup> collected by Puig et al. has 292 different high-level tasks in the knowledge base. This work lays the foundation for further exploration by future generations. Huang et al.<sup>[61]</sup> randomly sampled 88 holdout tasks from the aforementioned knowledge base for evaluation, and the remaining 204 tasks were used as a demonstration set, from which they were used as examples for prompting language models. For supervised fine-tuning baselines, these tasks were utilized in fine-tuning the pretrained language model. Brohan et al.<sup>[62]</sup> collected a large and diverse dataset of robot trajectories, including multiple tasks, objects, and environments. The main dataset contains 130,000 robot demonstrations, which were performed by 13 robots over a 17-month period. The robot conducted large-scale data collection in a series of office and kitchen. Fu et al.<sup>[63]</sup> proposed a novel physics-based actioncentric environment, RFUniverse, for robot learning of daily 

housework tasks. RFUniverse supports 87 atomic operations and interactions between 8 primitive object types in a visually and physically plausible way. To demonstrate the usability of the simulated environment, the learned algorithm is performed on various types of tasks, namely fruit picking for manipulation, folding cloth and sponge wiping, stair chasing for locomotion, room cleaning for multi-agent collaboration, milk pouring, and hand lift for cloning behavior from VR interface. Vaucher et al.<sup>[22]</sup> extracted 28 kinds of atomic operations for synthetic operations of chemical experiments using three models, which are rule-based action extraction from Pistachio, rulebased action extraction from NLP, and a combination of the above two methods. Wu et al.<sup>[64]</sup> propose to use pick-andplace and pick-and-throw as action primitives, arguing that they are well suited for household cleaning, and thus propose a personalized robot assistance model with a large language model<sup>[58]</sup> . Gu et al. introduced the benchmark maniskill2, comprising a series of 20 operational tasks specifically designed to tackle the major challenges faced by researchers when utilizing general operational skill benchmarks<sup>[65]</sup> . Gao et al. proposed a two-stage fine-tuning strategy to further enhance the model's generalization ability based on the maniskill2 benchmark<sup>[59]</sup> . Furthermore, there are additional pertinent works that can be referenced<sup>[66-69]</sup> . 

l Learning of Complex Manipulation Tasks for Robots With the expanding scope of application scenarios and increasing performance requirements for robots, the demand for completing increasingly complex and precise manipulation tasks has risen. Therefore, the research goal is to empower robots with the capability to autonomously learn from their environment and independently accomplish complex manipulation tasks. This includes acquiring knowledge, accumulating experience, continuously updating and expanding manipulation skills in order to successfully execute complex tasks. 

Wang et al. proposed RoboGen, a method for achieving robot automation learning by generating simulated infinite data<sup>[70]</sup> . Ma et al. proposed the Eureka method, which utilizes LLMs for human-like reward design. They demonstrated, for the first time, a simulated shadow hand capable of performing pen spinning techniques<sup>[30]</sup> . Shridhar et al. propose CLIPORT, a language-conditioned imitation learning agent that combines the broad semantic understanding of CLIP with the spatial precision of Transporter, an end-to-end framework capable of solving various language-specified desktop tasks<sup>[71]</sup> . Khandelwal et al. build a simple baseline EmbCLIP without task-specific architectures, inductive biases (e.g. using semantic maps), auxiliary tasks during training, or depth maps, but the improved baseline performs remarkably well across a range of tasks and simulator<sup>[72]</sup> . Wang et al. access pre-trained visual language models in robot manipulation, using a combinatorial classification grammar that parses sentences into operational procedures in a domain-specific language, which allows visual language models to correspond category or attribute descriptions to pixels, thus opening up the learning of visual and action strategies<sup>[73]</sup> . Xiao et al. introduced Data-Driven Instructional Augmentation with Linguistic Condition Control (DIAL) and generalized it to 60 new instructions not seen in the original dataset. This effectively incorporates internet-scale knowledge into existing datasets with limited real annotations<sup>[69]</sup> . Huang et al. used LLMs to infer affordances and constraints through 

language, used its code writing ability to interact with VLM to generate 3D value maps, integrated knowledge into observation space, and used value maps to model zero-shot synthesis of closed-loop robot trajectories. Robust to perturbations, the model is used to perform a variety of manipulation tasks<sup>[74]</sup> . Mo et al. proposed SeeAsk, an openworld interactive vision-based system that can master specific goals through vague natural language instructions<sup>[75]</sup> . Ze et al. proposed GNFactor, a visual behavioral cloning agent for multi-task robot manipulation<sup>[76]</sup> . Zheng et al. designed the canonicalized manipulation space and proposed a two-stage framework for synthesizing humanlike manipulation animations covering rigid and articulated object categories<sup>[77]</sup> . Extensive research has also been conducted on dexterous manipulation<sup>[78-96]</sup> . 

l Robot Manipulation Learning with Multimodal Fusion 

While multimodality<sup>[97]</sup> addresses the challenge of agent perception, it falls short in addressing the issue of cognition. In various scenarios like an intelligent customer service, users often provide information through multiple modalities. Multimodality holds significant perceived value, but it still has substantial challenges to overcome in solving fundamental issues. Multimodality represents a prominent future trend wherein foundation models will progressively align with multimodal approaches, enabling future agents to operate within a multimodal environment<sup>[98]</sup> . 

Yang et al. proposed MOMA-Force, an imitation method for visual binding force, using perceptual representation learning, imitation learning, and admittance whole-body control to enhance the robustness and controllability of the system. MOMA-Force enables mobile manipulators to learn multiple complex contact-rich tasks with high success rate and small contact force<sup>[99]</sup> . Jiang et al. demonstrate that a wide range of robotic manipulation tasks can be expressed with multimodal prompts, and many robotic manipulation tasks can be represented as multimodal prompts interleaved with language and images or video frames. The authors design a transformer-based robotic agent, VIMA, that processes these prompts and outputs motor actions autoregressively<sup>[100]</sup> . Sferrazza et al. achieve robot generalization manipulation through multimodal learning that fuses vision and touch. AudioPaLM combines text-based and speech-based language models<sup>[101]</sup> . Brohan et al. propose to jointly fine-tune state-of-the-art visuallanguage models on robot trajectory data and Internet-scale visual-language tasks. The authors present RT-2: VisionLanguage-Action Model Transferring Network Knowledge to Robot Control<sup>[102]</sup> . RobotGPT provides the perception, cognition, decision, execution capabilities with embodied AI<sup>[103]</sup> . Luo et al. proposed a physics-based humanoid controller that enables high-fidelity motion imitation and fault-tolerant behavior in the presence of noisy inputs (e.g., pose estimates generated from videos or speech) and unexpected falls<sup>[104]</sup> . Gandhi et al. conducted the first largescale study of the interaction between sound and robot movement. The authors created the largest available soundaction-vision dataset using the robotics platform Tilt-Bot, with 15,000 interactions on 60 objects<sup>[105]</sup> . Peng introduces Kosmos-2, a multimodal large language model (MLLM) that supports perceptual object descriptions (such as bounding boxes) and new capabilities for integrating text into the visual world<sup>[106]</sup> . Radosavovic et al. proposed an RPT model, which is a Transformer that operates on a sequence of sensorimotor tokens. Given a sequence of camera images, 

proprioceptive robot states, and past actions, it is assumed that if the robot can predict what is missing, then it has acquired a good model of the physical world that allows it to act<sup>[107]</sup> . Li et al. systematically studied how visual, auditory, and tactile perception can jointly help robots solve complex operating tasks<sup>[108]</sup> . LEE et al. use graph neural networks to generate master odor maps (POMs) that preserve perceptual relationships and enable odor quality predictions for previously uncharacterized odors<sup>[109]</sup> . Guzey et al. proposed visually stimulated tactile adaptation in order to learn tactile flexibility, thereby correcting errors and adapting to changing situations<sup>[110]</sup> . 

# 3.1.3 Datasets and Metrics 

**Datasets.** In order to improve the generalization ability of robot manipulation learning, researchers collected multitask, multi-scenario data sets so that the robot can be trained to quickly generalize various scenarios. At the same time, the test datasets evaluate the manipulation capabilities of these robots guided by the foundation model. There are several datasets available for testing, as presented in Appendix Table 4. 

**Metrics** . In order to improve robot performance and manipulation level, the key is to continuously optimize the performance of the robot learning system. Then the core issue is to reasonably evaluate the performance of the robot. Issues encountered in the comprehensive evaluation process: improvement of single evaluation indicators, integration of multiple evaluation indicators, weight distribution of each indicator, and reliability of evaluation results. 

Manipulation performance is evaluated by: (1) Plan success rate, which measures whether the skills selected by the model are correct for the instructions, regardless of whether they are actually successfully executed. (2) Execution success rate, which measures whether the entire system actually successfully executed the required instructions<sup>[62, 102]</sup> . 

# 3.1.4 Problems 

Despite making considerable progress, significant problems still exist. Robot movements are continuous and complex, with more physical interactions and manipulation causality. 

A comprehensive library of skills and actions needs to be built. In order to complete downstream target tasks, a skill library needs to be built. High-level instructions are broken down into atomic actions. The existing skill action library suffers from a long-tail distribution problem. A more comprehensive skill action library needs to be established to assist robot skill learning. Robots can manipulate objects of any size, shape, and material in any scene. For example, a robot can pour a specified volume of any liquid and complete specified tasks in a dynamically changing environment. Objects that are difficult to manipulate in the 3D world, such as articulated, deformable and transparent objects, can be manipulated. The robot can solve the problems of occlusion and obstacle avoidance when grasping. The robot can reason about spatial relationships and contact dynamics, accurately drive high-degree-of-freedom arms, and apply the appropriate force to stably grasp objects without breaking them. 

Current robotic object manipulation applications rely heavily on human programming and have poor autonomy, which is unrealistic in the long run. Vision-based intuitive 

physics, open set grasping with semantic representation, and planning under partial observability and uncertainty will be the future trends of robot grasping<sup>[15]</sup> . 

# 3.2 Navigation 

# 3.2.1 Characteristic and Challenges 

Several research projects focus on developing autonomous robots capable of navigating in different environments. However, little research has specifically addressed the navigation challenges faced by legged robots in indoor environments, especially when relying on singlecamera vision. The legged robot is able to traverse uneven surfaces and overcome obstacles, such as stairs, that traditional wheeled robots typically cannot reach. In order to realize the autonomous navigation of mobile robots in unknown dynamic environments, mobile robots need to solve three basic problems, namely "Where am I?", "What is my surrounding?", and "What should I do next?". In order to solve these three core basic problems, a series of core technologies such as environmental perception, map creation, autonomous positioning, and motion planning are required<sup>[111, 112]</sup> . Foundation models have reasoning and decision-making capabilities, and multi-modal foundation models can handle rich information modalities, and encode information of different modalities into the same vector space, which is conducive to cross-modal information processing. Benefiting from these considerations, foundation models help to deal with problems such as motion planning and environment perception of robots. In this section, we survey recent research results and state-ofthe-art advances in the direction of robotic navigation with foundation models, including robotic environment perception, map creation, autonomous localization, and motion planning. 

# 3.2.2 Methods 

# l Environment Perception 

Environmental perception refers to the process in which a robot, during its movement, perceives the surrounding environment through various devices. It can collect real-time environmental information and adjust its position and pose accordingly based on the actual situation. 

Lynch et al. proposed a robot framework for real-time natural language interaction in a real environment. The relevant resources are open source (datasets, environments, benchmarks, and policies). Behavioral cloning training is performed on the dataset of annotated trajectories, and the generated Policies proficiently execute orders of magnitude more commands than previous work<sup>[113]</sup> . Methods that align the embedding space of different modalities (in this case, IMU data) with the visual embedding space enable the VLM to understand and reason about these additional modalities without the need for retraining. The results show that using multiple modalities as input can improve VLM's scene understanding and enhance its overall performance in various tasks<sup>[114]</sup> . The agent follows real-life navigation instructions, then recognizes the location described in natural language and finds the object at the target location<sup>[115]</sup> . Hong et al. proposed a predictor to generate a set of candidate waypoints during navigation, bridging the gap between learning in discrete and continuous environments for visual and language navigation<sup>[116]</sup> . Tan et al. use environment dropout for back-translation to learn unseen 

environments in navigation<sup>[117]</sup> . Qi et al. propose an object and action perception model that can flexibly match objectcentered or action-centered instructions with their corresponding visual perception or action direction in the process<sup>[118]</sup> . Various other studies can serve as references<sup>[119-</sup> 121]. 

# l Map Creation 

Map construction can be accomplished either through the utilization of metric maps or by employing symbols that represent the robot's position in its reference frame. 

Gervet et al. proposed a semantic visual navigation method, compared six typical approaches of classical, modular and end-to-end learning methods without any experience, maps or instruments, through large-scale empirical research, found that modular learning is a reliable way to navigate to objects<sup>[122]</sup> . To address the lack of spatial accuracy of classical geometric maps, Huang et al. proposed spatial map representation VLMaps, which fuses pretrained visual-linguistic features with 3D reconstructions of the physical world. VLMaps can be autonomously constructed from the robot's video sources using standard exploration methods and can support natural language indexing of maps without labeled data<sup>[123]</sup> . An et al. proposed a multi-modal map pre-training paradigm BEVbert for language-guided navigation, which has spatial awareness capabilities<sup>[124]</sup> . Jia et al. proposed a neural SLAM method that for the first time exploits multiple modes to explore, predict perceptible semantic maps, and plan them simultaneously<sup>[125]</sup> . Zhang et al. propose a hierarchical object-to-region (HOZ) environment map to guide the agent in a coarse-to-fine manner. Additionally, an online learning method is proposed to update the HOZ new environment based on real-time observations. 

# l Autonomous Localization 

Robot localization refers to a robot's ability to accurately determine its position and orientation within a predefined reference frame. Inspired by the recent success of open-vocabulary models for image classification, Gadre et al. investigate a simple framework, CLIP on Wheels (CoW), to adapt open-vocabulary models to language-driven zeroshot object navigation without fine-tuning (L-ZSON)<sup>[126]</sup> . Keetha et al. have developed a universal VPR solution - a technology that works across a variety of structured and unstructured environments without the need for any retraining or fine-tuning<sup>[127]</sup> . Based on the WAY dialogue dataset, Hahn et al. focus on the LED task (locating the observer from the dialogue history)<sup>[128]</sup> . Two agents (tourist and tour guide) interact through natural language to allow tourists to navigate to the correct location<sup>[129]</sup> . 

# l Motion Planning 

Motion planning is the process by which a robot intelligently selects an optimal sequence of actions to move towards a target location based on its current position within a reference frame, considering changes in the environment. Hong et al. proposed a time-aware recurrent bert model to maintain cross-modal state information in order to solve the problem that the bert architecture in visual language navigation is difficult to use for partially observable Markov decision-making processes, which need to rely on historical attention and decision-making<sup>[130]</sup> . Manglani studies the development of visual segmentation and path planning algorithms for autonomous navigation and obstacle avoidance systems in domestic environments<sup>[111]</sup> . Lin et al. propose to provide action prompts for VLN agents to enable 

explicit learning of action-level modality alignment for navigation. Specifically, action prompts are defined as a pair of modality-aligned image sub-prompts and text subprompts, and when navigation starts, a set of action prompts related to an instruction is retrieved from a pre-built library of action prompts and passed through a prompt encoder to get hint features. Then, the prompt features are concatenated with raw instruction features and fed to a multi-layer transformer for action prediction. Using a contrastive language-image pre-training (CLIP) model, a modality alignment loss and a sequential consistency loss are introduced to enhance the alignment of action prompts and force the agent to sequentially attend to related prompts<sup>[131]</sup> . Traditional path planning algorithms focus only on collisionfree paths, limiting their applicability in contact-rich tasks. To address this limitation, Xie et al. proposed Linguistically Conditional Collision Function (LACO), a novel method to learn collision functions using only single-view images, language cues, and robot configurations<sup>[132]</sup> . Zhou et al. introduce NavGPT, an LLM-based instruction tracking navigation agent, to demonstrate the reasoning ability of large language models in complex scenes by performing zero-shot sequential action prediction for visual and language navigation<sup>[133]</sup> . Qian et al. propose the March-InChat model, which allows communication with LLMs in real time and perform dynamic planning based on room-and - object aware scene perceiver. The model outperforms previous models on the REVERIE benchmark<sup>[134]</sup> . Fried et al. experimentally demonstrated that the three parts of the proposed method (speaker-driven data augmentation, pragmatic reasoning, and panoramic action space) greatly improved the performance of the baseline instruction follower<sup>[135]</sup> . Wang et al. proposed enhanced cross-modal matching and self-supervised imitation learning methods to solve cross-modal grounding, ill-posed feedback and generalization problems<sup>[136]</sup> . Nguyen et al.<sup>[137]</sup> develop a memory-enhanced neural agent. Imitation learning algorithms teach agents to avoid repeating past mistakes. The agent also completes object finding tasks by requesting and interpreting natural language and visual assistance. 

# 3.2.3 Datasets and Metrics 

**Datasets.** In order to promote the development of robot navigation tasks, researchers have collected a large amount of data from multiple aspects such as instructions, scenes, objects, etc. This plays a very important role in the development of navigation and also lays the foundation for the transfer from virtual to real environments. There are many datasets that can be used for navigation. See Appendix Table 5 below. 

**Metrics.** Navigation performance is evaluated by: (1) Success / Oracle Success Rate (%). (2) Navigation Error (m). (3) SPL (Success weighted by Path Length). (4) CLS (Coverage weighted by Length Score), measuring fidelity to the reference path. (5) nDTW (normalized Dynamic Time). (6) SDTW (Success weighted by normalized Dynamic Time Warping)<sup>[138-140]</sup> . 

# 3.2.4 Problems 

To solve the problem of high obstacles, it is worth considering investigating partially observable search methods. Potential solutions would involve broadening the scope of the study to cover a wider range of domestic environments (including stairs and uneven surfaces), 

outdoor environments and complex unknown environments. In addition, a more general large-scale navigation model can be designed that can be widely applied to any robot, similar to LLMs and VLMs for processing any text or image. 

In addition, the efficiency of multi-target navigation needs to be improved, scene knowledge needs to be better applied in navigation, and the efficiency of unknown scene navigation needs to be improved. Techniques for optimizing system efficiency in real-time scenarios will also be explored, taking into account factors such as robot stability, dynamic obstacle avoidance, and resource constraints. 

Path planning in unknown scenarios faces the following problems: lack of global map, generalization of unknown environments, and sensor noise in real-life applications. The lack of global map includes the following aspects: lack of global SLAM map, how to learn prior knowledge of layout, and in what form to store knowledge. The generalization of unknown environments includes the following aspects: limited training rooms and infinite unknown environments, transfer and generalization of knowledge. Sensor noise in real-life applications includes the following aspects: depth loss, RGB blur, and detection and segmentation errors. 

# 3.3 Task Planning 

# 3.3.1 Characteristic and Challenges 

Depending on the difficulty of the task, the task can be completed by a single robot or by multiple robots. Many of these problems require multiple robots to work together in multi-robot systems. Long-term tasks for a single robot need to be broken down into smaller tasks that can be accomplished with simple operations. Task planning for multiple robots working together needs to consider the relationship between tasks, robot capabilities and cooperation, and other challenges. In addition, the agent cannot hallucinate when planning tasks. Within the bounds of common sense, agents can learn from previous tasks, selfcorrect and improve, and continue to learn. This is a challenging task. The true realization of intelligent robots will be based on the perception of the environment, dynamic learning, and continuous updating. In this section, we survey the recent research results and the latest progress of foundation models in the direction of robot task planning, including single-robot task decomposition, multi-robot task planning, and self-correction, self-improvement, and continuous learning of agents. 

# 3.3.2 Methods 

# l Single-Robot Task Decomposition 

Task planning. For complex tasks, the best solution is to split it into several simple tasks, and then solve them one by one. Generally, the effect will be good. LLMs have shown good zero-shot generalization ability. State-of-the-art chatbots can provide plausible answers to many common questions that arise in everyday life. However, so far, LLMs cannot reliably solve long-term planning problems<sup>[141]</sup> . 

Liu et al. introduce LLM+P, the first framework to incorporate the strengths of the classical planner into LLM<sup>[142]</sup> . Wu et al. aligned the LLM with the visual perception model, and generated executable action sequences based on the objects existing in the real scene<sup>[143]</sup> . Lin et al. proposed a language-based planning framework, Text2Motion, based on which robots can solve sequential manipulation tasks for long-horizon reasoning. This 

framework uses the feasibility heuristic encoded in the skill library Q function to guide the task planning of LLMs, and Geometric dependencies among skills are resolved by performing geometric feasibility planning during the search process<sup>[144]</sup> . Wake et al. use ChatGPT to convert natural language instructions into executable robotic actions in longstep scenarios<sup>[145]</sup> . EmbodiedGPT introduces an efficient training method to generate high-quality plans. The paradigm of extracting task-relevant features from LLMgenerated planning queries is introduced to form a closed loop between high-level planning and low-level control<sup>[146]</sup> . Ruan et al. proposed a structured framework customized for LLM-based artificial intelligence agents, within which two different types of agents were designed: one-step agents and sequential agents, to perform the reasoning process. The framework is then instantiated using LLMs and evaluated on their task planning and tool usage abilities on typical tasks<sup>[147]</sup> . Zhen et al. propose a task planning method that combines human expertise with LLMs. And the LLM prompt template is designed, which has stronger expressive ability to represent structured professional knowledge. Further, a method of gradually decomposing tasks to generate task trees is proposed. And a strategy for decoupling robot task planning is designed<sup>[148]</sup> . Gu et al. studied a modular approach to handle the long-view movement operation task for object rearrangement, decomposing the complete task into a series of subtasks<sup>[149]</sup> . Obinata et al. describe a strategy for implementing a robotic system capable of performing general service robot (GPSR) tasks in robocup@home<sup>[150]</sup> . Shi et al. developed RoboCook, an intelligent robotic system that can use multiple tools for long-horizon elastoplastic object manipulation<sup>[151]</sup> . There are some other works that can be referenced<sup>[61]</sup> . 

l Multi-Robot Task Planning 

For multiple robots, relationships between tasks needs to be considered during task planning, robot capabilities and cooperation, and other challenges. Task planning for multirobot teams usually involves three sub-problems: task decomposition, task allocation and task scheduling, which are introduced here to consider situations where robots sequence their own tasks to satisfy various constraints. While each of these problems can be solved individually, the interdependencies between these subproblems are often considered in the context of integrated tasks to provide solutions that are often better than solving each subproblem independently<sup>[18, 152, 153]</sup> . 

LLMs have shown impressive planning capabilities in single-agent specific tasks across domains, yet their planning and communication capabilities in multi-agent cooperation remain unclear. A novel framework for multi-agent cooperation using LLMs is proposed, which enables agents to plan, communicate and cooperate with other agents or humans to effectively complete long-horizon tasks<sup>[154]</sup> . RoCo is a unified approach for multi-robot collaboration that leverages pre-trained LLMs for high-level communication and low-level path planning. The authors introduce the RoCoBench benchmark, which includes various challenges in collaborative task scenarios. The method demonstrates its utility on RoCoBench<sup>[155]</sup> . Qian et al. carefully divided the development process into four different chronological stages: design, coding, testing and recording. Each stage involves a team of agents, such as programmers, code reviewers, and test engineers, facilitating collaborative conversations and facilitating a seamless workflow. The chat chain acts as a 

facilitator, breaking down each stage into atomic subtasks<sup>[156]</sup> . Using multi-agent competition, the simple goal of hide-and-seek, and large-scale standard reinforcement learning algorithms, Bowen Baker et al. found that the agent created a self-supervised automated course, triggering multiple rounds of different emergent strategies, many of which required complex tool use and coordination<sup>[157]</sup> . Zhang et al. proposed a framework for multi-agent cooperation using LLMs. Experiments have proven that LLM-based agents that communicate verbally can win more trust and cooperate more effectively with humans<sup>[154]</sup> . 

l Self-Correction and Self-Improvement 

The ability to automatically detect and analyze failed executions is critical for explainable and robust robotic systems. This requires the agent to self-criticize and continuously learn from previous tasks. Correct behavior within the bounds of common sense. Based on the large language model, directional error correction and directional improvement can be done. In task planning, it is necessary not only to have the current state, but also to have memory, experience, reflection and summary, and world knowledge. Agents can get feedback based on actions. For large language models, reinforcement learning from human feedback is an extremely simple environment. 

Pan et al. analyzed and categorized a series of work of LLM's self-correction, including training time, generation time and post-correction<sup>[158]</sup> . Sharma et al. show how language can be used to update the latent cost of the planner to improve task performance. This method can use the language to correct the plan in two ways: adding constraints or specifying intermediate subgoals for the planner<sup>[159]</sup> . Liu et al. introduced a framework, REFLECT, to leverage the power of LLMs to explain robot failures. According to the explanation, the mission planner will generate an executable plan for the robot to correct the fault and complete the mission. Evaluating the framework on the RoBoFail dataset of failure scenarios, experiments demonstrate that the LLMbased framework is capable of generating informative failure explanations to aid in successful corrective planning<sup>[160]</sup> . Shinn et al. proposed a novel framework, reflexion, to learn from trial and error through dynamic memory and self-reflection to make better decisions in subsequent experiments<sup>[161]</sup> . Bousmalis et al. proposed RoboCat, a foundational agent for robotic manipulation, as a visual goal-conditional decision transformer. The authors demonstrate the ability to generalize to new tasks and robots. It also demonstrates the use of the trained model to generate data for subsequent training iterations, providing the basic building blocks for autonomous improvement loops<sup>[162]</sup> . Ning et al. explore whether LLMs has the ability to identify its own mistakes without resorting to external resources. In particular, the research focuses on whether they can be used to identify individual errors in step-by-step reasoning. The authors propose a zero-shot verification scheme to identify such errors. This verification scheme is then used to perform weighted voting on different generated answers, improving question answering performance<sup>[163]</sup> . Olausson et al. analyzed the ability of GPT3.5 and GPT4 to perform selfrepair on APPS. The approach is to self- repair with separate code and feedback models. APPS is a dataset consisting of various coding challenges. By evaluating the strategy, it was found that the effectiveness of self- repair was only seen in GPT4. It was also observed that self- repair is bottlenecked by the feedback phase<sup>[164]</sup> . Continual learning serves as a 

means to consistently foster self-improvement and selfoptimization<sup>[165]</sup> . Guo et al. proposed DoReMi, a novel language model base framework that can instantly detect and recover from inconsistencies between planning and execution<sup>[166]</sup> . In order to enable LLMs to integrate into the environment autonomously, Peng et al. proposed the selfdriven grounding framework to automatically and gradually lay the foundation for LLMs through self-driven skill learning<sup>[167]</sup> . 

There are some other works that can be referenced<sup>[168-</sup> 175], such as WebShop[176], InterCode[177], Collie[178]. 

# 3.3.3 Datasets and Metrics 

**Datasets.** Researchers in the field of robot task planning rely on datasets to develop, validate, and test their planning algorithms and systems. These datasets may include real-world data collected from robots or simulated data generated within robot environments<sup>[179]</sup> . Here is an example list in Appendix Table 6. 

**Metrics** . Task planning performance is evaluated by: (1) Task Success Rate. (2) Task Durations. (3) Task Diversity. (4) Task Difficulty. (5) Task Dependencies. 

# 3.3.4 Problems 

More effective strategies for self-improvement and enhancement need to be explored<sup>[180]</sup> . LLMs automatically detects when and how to apply the planner; LLMs reduces reliance on human information during planning<sup>[142]</sup> . In addition, the planning time efficiency of the model needs to be improved. The correctness and executability of generated plans need to be significantly improved. Multimodal models are explored for mission planning, which can naturally support extending the planning system to higherdimensional observation spaces. 

A significant advantage of utilizing the latest LLMs is their ability to adapt to various operating environments through several learnings and user feedback. These capabilities not only eliminate the need for extensive data collection or model retraining, but also allow users to make adjustments that promote safe and robust mission planning. The ability to effectively adapt to user feedback may be due in part to learning methods that combine model behavior with human intent. Additionally, the output of large models can be adjusted with a reasonable amount of feedback. The ability of LLMs to reflect the semantic content of user feedback provides means for users to communicate their intentions to the system. Therefore, this aspect helps lay the foundation for a user-friendly system. Delving into this ability to adjust contributes to the user-friendliness of the system<sup>[145]</sup> . 

# 3.4 Reasoning 

# 3.4.1 Characteristic and Challenges 

Reasoning requires the reasoner (robot) to have an explicit representation of various parts or aspects of its environment in order to reason. Robots are increasingly transitioning from specialized single-task machines to general-purpose systems operating in diverse and dynamic environments. To solve the challenges associated with realworld interactions, robots must effectively generalize knowledge, learn, and remain transparent in their decisionmaking processes. However, there are few studies that specifically address the reasoning challenges faced by robots 

in interactive environments. This survey aims to investigate reasoning robot system technologies that enable robots to encode and use knowledge, including concepts, facts, ideas, and beliefs about the world. Continuously sensing, understanding, and generalizing knowledge enables robots to identify meaningful patterns shared across problems and environments to perform a variety of real-world tasks more efficiently<sup>[19]</sup> . LLMs provide promising tools for robots to perform complex reasoning tasks<sup>[181]</sup> . In this section, we survey the recent research results and latest progress of foundation models in the direction of robot reasoning, including robot logical reasoning, common sense reasoning, affordance reasoning, and personalized reasoning<sup>[182-185]</sup> . 

# 3.4.2 Methods 

# l Logical Reasoning 

Machine logical reasoning refers to the ability of a machine to draw new conclusions through the derivation of known facts and reasoning rules. In logical reasoning, the machine needs to take into account the logical relationship between facts, such as If A is true, then B is also true, One of A and B must be chosen, etc. In addition, machines need to be able to understand fuzzy information and take into account the possibilities of different situations and choose the most reasonable conclusion from them<sup>[186]</sup> . Chain of thoughts can significantly improve the complex reasoning capabilities of large language models<sup>[187]</sup> . Tree of thoughts can be used for tasks that require exploration, strategic foresight, or where initial decision-making play a key role<sup>[188]</sup> . 

Driess et al. implemented a PaLM-E multimodal model that plugs real-world continuous sensor modalities into a LLM to establish a link between words and perception. The inputs to the specific LLM are multimodal sentences that interweave visual, continuous state estimation, and textual input encodings. These encodings are trained end-to-end in conjunction with a pre-trained LLM to perform a variety of specific tasks, including sequential robot operation planning, visual questioning and answering, and captioning<sup>[189]</sup> . Brohan et al. argue that one of the keys to the success of general robotics models lies in combining high-performance architectures that learn a large variety of robotics data for training on open tasks<sup>[62]</sup> . Liang et al. proposed a method to generate policies based on LLMs. By inputting natural language instructions, the LLM trained by code completion can write robot policy codes. These policies are reactive policies and waypoint-based policies. Features include exhibiting spatial-geometric reasoning, generalizing new instructions, and assigning exact values to ambiguous descriptions based on context<sup>[168]</sup> . Yao et al. explore that with the support of chain of thoughts prompting and external knowledge bases, LLMs generates reasoning trajectories and task-specific actions in an interactive manner, thereby exerting greater synergy between the two<sup>[190]</sup> . 

There are still some valuable methods for reasoning that are worth studying, including accumulative reasoning<sup>[191]</sup> , context learning<sup>[192]</sup> and causal reinforcement learning<sup>[193]</sup> . l Commonsense Reasoning 

LLMs combined with knowledge graphs or langchain is a way to try common sense reasoning. LLMs are blackbox models that typically fail to acquire and capture factual knowledge. In contrast, knowledge graphs etc. are structured knowledge models that explicitly store rich factual knowledge. Knowledge graphs can enhance LLMs by 

providing external knowledge for reasoning and interpretability. At the same time, knowledge graphs are inherently difficult to construct and evolve, posing challenges to existing methods for generating new knowledge and representing unseen knowledge in knowledge graphs. Therefore, it is complementary to combine LLMs and knowledge graphs to play their respective advantages at the same time<sup>[194]</sup> . LLMs and knowledge graphs (KGs) can complement each other, such that LLMs can be used for KG construction or completion, while existing KGs can be used for different tasks, such as making LLMs outputs interpretable or fact-checking in a neural-symbolic manner. Text2KGBench is a benchmark that evaluates the ability of language models to generate knowledge graphs from ontology-guided natural language text<sup>[195]</sup> . Kim et al. proposed KG-GPT, a general framework that utilizes LLM for knowledge graph reasoning<sup>[196]</sup> . Zhu et al proposed AutoKG, a method based on multi-agents, using LLM for knowledge graph construction and reasoning<sup>[197]</sup> . Yang et al. proposed to enhance the large language model KGLLM by developing knowledge graphs, and provided a solution to enhance the factual reasoning ability of LLMs<sup>[198]</sup> . Ren et al. propose KNOWNO, a framework for measuring and adjusting uncertainty in LLM planners so that they know when they don't know and seek help when needed. KNOWNO builds on conformal prediction theory to provide statistical guarantees for task completion. At the same time human assistance in complex multi-step planning setups is minimized<sup>[199]</sup> . Zellers et al. proposed QLeT: a model that learns physical commonsense knowledge through interaction and then uses this knowledge to construct language. Authors decompose QLeT into a physical dynamics model and a separate language model. Using a dynamics model as an interface to a language model, QLeT can read a sentence, neurally simulate what might happen next, and then communicate that result through a textsymbolic representation or natural language<sup>[200]</sup> . Zhu et al. proposed 3D-VisTA, a LLM with 3D world recognition capability, capable of answering questions based on a 3D world model. The project team also released the ScanScribe dataset, a 3D model-text dataset<sup>[201]</sup> . One approach to address inference problems is by incorporating vector databases. Both LlamaIndex and Langchain are working diligently to develop a data-augmented retrieval system, which could be further enhanced with a contextual agent. Yohei introduces the concept of incorporating relevant contextual information (task context), which may have nuances differing from those of the conventional semantic similarity algorithm offered by vector databases. Tang et al. proposed GraphGPT, which utilizes LLMs for graph instruction tuning<sup>[202]</sup> . 

l Affordance Reasoning 

The ability to reason about affordances enables robots to choose actions that are appropriate for a given object and produce a desired effect. The Dreamer algorithm has recently shown great promise for learning from a small number of interactions by planning in a learned world model, outperforming pure reinforcement learning in video games. Learning world models to predict the outcomes of potential actions can be planned in imagination, reducing the amount of trial and error required in real settings<sup>[203]</sup> . Robots need primary knowledge of the world in which to act. LLMs can be used to score potential subsequent actions during task planning, or even directly generate action sequences without 

natural language instructions from additional domain information. Singh et al. propose a procedural LLM hint structure that enables plan generation to work across environments, robot functions, and tasks. LLMs are prompted by program-like specifications of operations and objects available in the environment, as well as example programs that can be executed. Situational awareness is introduced in LLM-based robot task planning<sup>[204]</sup> . Ahn et al. proposed SayCan, the value function of pre-trained skills to obtain the results of interaction with the environment, based on the real world. SayCan incorporates real-world experience into LLMs through the value function of pretrained skills, enabling LLMs to execute real-world abstract, long-term commands on robots. This method implements language models to provide high-level semantic knowledge and provide pre-trained low-level skills to constrain the model to propose natural language actions that are both feasible and appropriate to the context<sup>[205]</sup> . Yoneda et al. published the Statler framework, which enables LLMs to have representations of world states that change over time while maintaining memory. The framework has two generic LLM instances: a world model reader and a world model writer. These two parts interact with and maintain the world state. With access to this world-state memory, the Statler framework improves the ability of existing LLMs to reason over longer periods of time, independent of context length constraints. Experiments on simulated domains and real robots show that the proposed method improves the state-ofthe-art in LLM-based robot inference<sup>[206]</sup> . Gao et al. finetuned VLM on PhysObjects to improve its understanding of physical object concepts by capturing human priors on these concepts from visual appearance. Combining this physicsbased VLM with a large language model-based robot planner into an interactive framework improves mission success rates<sup>[207]</sup> . Tang et al. proposed a knowledge condition detection framework CoTDet for affordance knowledge prompts for task-driven object detection<sup>[208]</sup> . Strategic robotic pursuit-avoidance requires exploiting the dynamics of interactions and planning through uncertainty in physical states and underlying intentions<sup>[209]</sup> . 

# l Personalized Reasoning 

The emergence of large language models marks a revolutionary breakthrough in artificial intelligence. A major leap forward in the capabilities of general artificial intelligence will change how personalization is implemented. On one hand, it will change the way humans interact with personalized systems. On the other hand, it will also greatly expand the scope of personalization<sup>[210]</sup> . The growing use of LLMs in conversational agents has sparked interest in the personality exhibited by data-trained models, as personality significantly influences communication effectiveness. Therefore, Safdari et al. proposed a comprehensive approach to test the personality traits expressed in the text generated by LLMs. Experiments find the reliability and validity of LLMs for simulating personality for larger and fine-tuned models. The personalities in the LLM output can be shaped in desired dimensions to mimic specific personality traits<sup>[211]</sup> . Huang et al. proposed to assess the empathic ability of LLMs, that is, how their feelings change when they encounter a specific situation. After experimental evaluation, LLMs can usually respond appropriately to some situations, although there are some biases. Still, they don't match human emotional behavior to make connections between similar situations. This paper expects to contribute to the 

advancement of LLMs to better adapt to human emotional behavior, thereby enhancing the practicality and applicability of intelligent assistants<sup>[212]</sup> . Wu et al. used TidyBot, a robot to learn personal preferences to personalize the cleaning of a room, where the robot used the planning and perception of language combined with the summarization capabilities of a LLM to pick up objects, determine where to place them, and organize the room<sup>[64]</sup> . Ding et al. Learn universal human priors for dexterous manipulation from human preferences<sup>[213]</sup> . Deng et al. present Socratis, a social response benchmark that tests the ability of state-of-the-art multimodal large language models to generate emotional reasons for a given IC pair<sup>[214]</sup> . Lian et al. proposed the first multimodal LLM in affective computing, called AffectGPT. The goal is to address the long-standing challenge of label ambiguity and chart a path toward more reliable technology<sup>[215]</sup> . 

# 3.4.3 Datasets and Metrics 

**Datasets.** Robot reasoning datasets typically involve tasks that require problem-solving abilities such as logical reasoning and common-sense reasoning. These datasets are designed to evaluate the robot's ability to make inferences in various scenarios. Here are some examples of robot reasoning datasets in Appendix Table 7. 

**Metrics** . The evaluation indicators for robot reasoning datasets typically depend on the specific dataset and task. However, common evaluation metrics and indicators for many reasoning datasets. 

Reasoning performance is evaluated by: (1) Accuracy. (2) F1 Score: F1 score is calculated based on the overlap between predicted answers and ground truth answers. (3) Exact Match (EM): Calculates the percentage of questions answered exactly correctly. (4) Top-k Accuracy. (5) Mean Reciprocal Rank (MRR): Measures the quality of the topranked answer. It calculates the average reciprocal rank of the first correct answer in the ranked list of answers. (6) BLEU (Bilingual Evaluation Understudy): Commonly used in machine translation tasks, BLEU measures the similarity between predicted and reference answers. 

# 3.4.4 Problems 

Robot learning goals are to master how to learn, combine advanced pattern recognition with model-based reasoning, and develop common sense intelligence. With the advancement of learning and the improvement of intelligence<sup>[216]</sup> , research on robot reasoning has gradually deepened. Reasoning is an abstract, advanced form of thinking. The objective basis of reasoning is the relationship between objective things. At present, the reasoning capabilities of robots are weak (including causal reasoning<sup>[217]</sup> , spatiotemporal reasoning, real-time reasoning, geometric reasoning, world model, world knowledge, common sense reasoning, understanding of physical constraints, etc.). One very important point is that the robot lacks reverse reasoning, and the basic model may reason from left to right. The current model is based on text-visual speech, so it does not directly reason about information such as touch, and more powerful multi-modal models are needed when available. 

Solutions that can be tried are as follows: Beyond statistical correlation, reasoning about system dynamics and causality; meta-learning with limited data; rapid learning to adapt to dynamic, uncertain environments; learning across 

heterogeneous tasks and domains ; Developing systems that know their limitations and know how to ask for help; Developing systems that can deeply understand and synthesize complex textual and narrative information; Conducting deep moral and social reasoning about realworld problems. 

# **4 Discussion** 

Despite the significant progress made in robot learning based on LLMs techniques, the field still faces numerous challenges in terms of both technical aspects and ethic aspects. In the following section, we will outline the major challenges, potential solutions as well as potential future directions. We hope that the highlight aspects can serve as inspiration for future research investigations in the robot learning area. 

# 4.1 Robot Hardware and Software Decoupling 

The basic requirement for a foundation model is a unified architectural framework. However, there is significant variation in robot hardware, making it crucial to achieve bottom-level uniformity or decoupling. To facilitate the advancement of robot technology, it is crucial to ensure the synchronization of form with function<sup>[218]</sup> , which implies that software and hardware must evolve simultaneously. Nevertheless, numerous challenges persist in the development of software and hardware. On one hand, due to the diversity of manufacturers' specifications and private parameters, it becomes challenging to individually program and manage robots when (re)configuring them to achieve desired tasks or formations. This dilemma often occurs in industrial and operational fields. On the other hand, the construction of current robot models and databases largely depends on the hardware structure of the robots. The majority of robot databases are constructed by collecting specific data pertaining to individual robots. Consequently, trained robot models exhibit optimal performance solely on the particular robot they are trained for. Put simply, existing robot models are limited by the hardware structure of the robots and software algorithms. 

Ideally, there is a need to decouple robot software and hardware, and concurrently, collect databases encompassing various robot models. The separation of the logical and physical components would foster increased software innovations and facilitate a potentially more accessible robot market, inevitably resulting in reduced non-recurring engineering costs. In a decoupled architecture, robot hardware and software can be developed and updated independently, without restrictions. Additionally, the most recent high-performance software algorithms can be efficiently implemented across various robot models. Confronted with diverse hardware configurations and unpredictable operating environments, users can develop and program robots of different types without the need for a comprehensive understanding of the specific hardware employed by each robot. Compatible APIs, predefined libraries, and programming software can be developed and enhanced. The abstraction level of robot software needs to be improved to increase the efficiency and effectiveness of robot operations, enabling robot applications to run robustly in dynamic environments<sup>[219]</sup> . 

# 4.2 Dynamic Data for Interaction with the Environment 

When establishing a specialized large-scale robot model, it is necessary to utilize dynamic and diverse data<sup>[220]</sup> , including dynamics data, during the training or fine-tuning process. Meanwhile, robots are anticipated to embody key attributes including agility, cost-effectiveness, diversity, environmental adaptability, and plasticity, which empower them to execute tasks like fastening garments and tying shoelaces. Interactive environments<sup>[221]</sup> and abundant dynamic data are imperative for sufficiently training and assessing robots possessing these aforementioned attributes. However, the realization of authentic robot scenarios and the acquisition of real-time data present formidable challenges. Therefore, collaboration and resource sharing among laboratories worldwide assume paramount importance in propelling responsible and open advancements in robotics research. Data collection methods may encompass several approaches, including action library aggregation, teleoperation, and imitation learning. The crux of the challenge lies in dissociating the collected data from the specific robot model employed, thus ensuring its perpetual validity. Additionally, the existing training process in robot learning suffers from an inadequacy of effective and abundant data. Establishing multimodal databases that can be utilized for robot learning training is of paramount importance. In order to better understand the environment, recognize objects, and perform tasks, current robot models often only focus on the fusion of top-level data such as vision and language in multimodal fusion, while neglecting bottom-level data such as dynamics data related to interaction with the environment. In real-world environments, there is no doubt that mechanics directly determine the stability of grasping. To improve the accuracy, generalization, robustness, and address issues related to force perception in robot models, it is necessary to construct large-scale dynamics data during training. Dynamics data includes information such as position (XYZ, rotation angles), acceleration, and forces (magnitude and torque), etc. Based on this information, robots can easily manipulate objects of different materials and weights accurately. Understanding the robot's dynamics model allows the model to comprehend the robot from a bottom-up approach during the training process of existing robot learning. Incorporating dynamics data into the robot's foundation model also enables the model to generate more realistic and physically meaningful data. 

# 4.3 Robot Generalization 

Robot models need to demonstrate better generalization ability, surpassing the semantic, visual, and other multimodal understanding of the robot data they encounter. It requires robots to perform operational tasks on objects or scenes in the robot data that they have never seen before. This necessitates the utilization of knowledge derived from network data for operation. Robot models should not only maintain performance on the original tasks in robot data but also improve performance in previously unseen scenarios. Accordingly, we present the following key elements. 

Currently, the advancements in robotic research have yet to reach optimal levels of efficacy. A clear divergence is evident between human intelligence and that of robots, especially when evaluating areas such as image recognition and the competency of platforms like ChatGPT in question- 

answering scenarios. The enhancement of both the precision and efficiency of robotic learning stands as a critical imperative. While modern robotic learning methodologies have attained certain milestones, the scope for refining execution success rates remains substantial. 

The environment is expected to become increasingly complex. Robots need to adapt to various scenarios to perform a variety of tasks. It is difficult to achieve long-term autonomy in complex environments, so lifelong learning is required. Currently, robots are only capable of performing a limited number of skilled tasks and are not generalizable across a variety of tasks<sup>[222]</sup> . On the one hand, Robots will adapt to different scenarios including layout configuration, visual texture, light source changes, time simulation, low cost, data enhancement, demand personalization, and program automation. In virtual-real transfer, methods that may be used include domain adaptation, meta-learning, transfer learning, knowledge distillation, and world models. Legged robots have made a lot of progress in traditional methods, but they are lacking in combining with foundation models. On the other hand, Robots can observe, understand, practice in interaction with their environment, and thus selfexam, diagnose, and repair. The robot can not only collect data by itself, analyze the data, and then analyze the cause of the failure and then solve the problem. Robots can have selfdriven learning awareness and can continue to learn<sup>[165]</sup> . 

Currently, foundation models are developed and trained in unmanned environments. In the future, when they are utilized in environments with human presence, interactions between robots and humans will need to take human factors into consideration. It requires human-robot alignment and considers emotional factors. It also considers biomimetic learning, cross-learning, and the co-development of the brain and the body. 

AI alignment is worthy of in-depth research. The goals of AI systems are required to be consistent with human values and interests. If the values of AI and humans cannot be aligned, the following problems will arise. Behaviors that do not meet the goals of human intentions, out of control, harming human interests, and making wrong choices in the conflict of multiple setting goals<sup>[157, 223]</sup> . 

Researchers can combine functionality with expressive capabilities and explore methods to improve robots from this perspective. Functionality is manifested in mobility, dexterity, perception, and intelligence. Considering the relationship between individuals and occupations, we can liberate people from dangerous situations and enhance the technological level of humanity. 

While current foundation models are capable of engaging in high-level semantic conversations, they fall short of humans in low-level control aspects such as movement and operation. Consequently, bionics is deemed significant. Biomimetic learning is a highly worthwhile field of research in order to design and develop more powerful robots. It draws inspiration from biological systems, especially animals and organisms. By observing how animals and organisms move, perceive their environment, and interact with it, researchers attempt to replicate these mechanisms in robots. They utilize biomimetic materials, such as artificial muscles and soft robot components, to enable robots to imitate the adaptability and flexibility of living organisms. The objective of researchers is not only to replicate the physical characteristics of animals but also to understand their behavioral patterns. This includes 

understanding how animals make decisions, solve problems, and exhibit intelligent behavior. Overall, the aim of biomimetic learning in robotics is to push the limits of robot capabilities by harnessing natural wisdom and integrating biological principles into the design and control of robots, making them more versatile and adaptable to various tasks and environments. 

Robots can achieve dexterous movement and manipulation. It has been found through research that the perception-action circuit is the center of cognition, and the body uses the perception-motor system to generate intelligence in the interaction with the environment. Intelligent robots span multiple directions in intelligent disciplines, such as cognitive science, psychology, brain science, and sociology. Therefore, the focus is on interdisciplinary integration, analogous to the developmental process of human intelligence. In multimodal environmental interaction, by opening up the links and loops between morphology, perception, behavior and learning, robots can realize active perception and autonomous learning. 

Being conscious is hard, but the body and brain of robot should develop together<sup>[218, 224]</sup> . In robot learning, the robot lacks common sense and lacks the physical constraints of learning real scenes from the environment. Robot learning is to make robots intelligent. In addition to perceptual and motor capabilities, which have been studied in the past, cognitive abilities are also very significant. Referring to the development process of human intelligence, the brain and body develop simultaneously. Intelligent robots not only have perception and motor intelligence, but also cognitive intelligence with autonomous consciousness. In addition, robots lack the ability to learn actively. For example, in completing the specified target tasks, it can actively ask what it needs to do next in order to achieve a certain task. Active learning may regain favor as autonomous contextual agents actively reveal what they don't know in order to prioritize<sup>[225]</sup> . 

# 4.4 Multimodal Interaction 

Currently, the interaction data of robots mainly relies on visual and textual information, lacking diversity. In order to enhance the robot's perception of the environment and its interaction with it, it is necessary to integrate multimodal data from various sensory modalities, including visual, auditory, tactile, olfactory, gustatory, and other sensory inputs. Although multimodal data brings great hopes for advancing robot technology, it also comes with some problems and challenges. Specifically, different modalities have different data formats, structures, and features, posing challenges for the collaborative interaction among different modalities. The main issues involved are multimodal representation, multimodal mapping, multimodal alignment, and multimodal fusion. 

To address these problems, several considerations can be taken into account. Research can be conducted to tackle challenges related to large-scale environments, multitasking, and strong interaction. Tasks with higher interactivity can be verified and demonstrated in more open and complex environments, such as simulators and multi-platform settings. Various fusion strategies can be explored to effectively combine information from different modalities, including hierarchical and multilingual fusion, as well as scalable fusion. Advanced deep learning models, such as multimodal transformers, can be developed to efficiently 

fuse and extract meaningful information from different sensory modalities. Cross-modal learning techniques can be explored to enable robots to learn meaningful correlations between different modalities, thereby improving their understanding of the environment. Transparent and interpretable multimodal fusion models can be developed to facilitate human understanding and trust in robot decisions. The capability of robots to understand the semantic of multimodal data, including scene understanding<sup>[15]</sup> and context comprehension, can also be enhanced. Additionally, during the process of converting multimodal content, foundation models may lose information or generate errors, leading to biased results. This requires foundation models to achieve strong multimodal understanding, addressing the current issues of unreliability in intelligent agents, as well as information loss and biases. 

# 4.5 Exclusive Foundation Models for Robots 

Foundation models have achieved many gratifying results in text, language, etc., but in the field of robotics, the development of foundation models is slow. There is an urgent need to develop usable and effective general-purpose foundation models and special-purpose foundation models of robots. In order for robots to reach human-like levels of capability, it is necessary to collect robot data for every object, environment, task, and situation. In addition to the issue of robot data, the following problems and challenges also need to be overcome. 

Multimodal large language models suffer from the catastrophic forgetting problem. Fine-tuning of a model can improve specific performance, but as fine-tuning proceeds, the model begins to exhibit hallucinations, resulting in a significant loss of generality<sup>[226]</sup> . The hallucination problem of foundation models, that is, when the text generated by the model does not follow the original text (Faithfulness) or does not conform to the facts (Factualness)<sup>[227]</sup> . As a result, the robot gives wrong judgments or operations in the process of performing tasks in combination with the foundation model<sup>[228]</sup> . Currently, in order to obtain reasonable answers in multi-turn dialogues with foundation models, multiple prompts need to be provided. Therefore, it is necessary to design foundation models that do not rely on human prompts. Furthermore, foundation models need to have better contextual understanding and causal understanding<sup>[229, 230]</sup> . 

Combining large models and small models is also a method that can be tried<sup>[231]</sup> . Large models are well suited to handle Corner Cases, while small models trained by modeling and for scenarios cannot exhaustively cover the whole scenario, and this part of the work can be handled by the general understanding and strong generalization and inference capabilities of large models. The combination of large model and small model can improve the inference efficiency without reducing the inference ability. 

Foundation models for low level control need to be designed. Due to the lack of data for low-level controllers in the training corpora, most of the existing robot foundation models have been applied to robots as either a semantic planner or to interact with robots using human-designed action primitives<sup>[232]</sup> . Having a large embodied model enables one-step control of the lowest level. 

The evaluation of embodied intelligent agents should shift from task-oriented evaluation to capability-value evaluation. Human discrimination tests evaluate AI based on human observations, as represented by the classic Turing test. 

Qualitative testing can only be done through human observation and there is no quantitative testing<sup>[233-239]</sup> . 

# 4.6 Computation Efficiency 

Computing efficiency<sup>[240]</sup> requires continuous evolution and improvement. Optimization aspects while ensuring high performance mainly include the following three aspects: computing costs need to be reduced, computing resources need to be reduced, and computing time needs to be reduced. 

There has been a staggering increase in computational power requirements. However, storage performance significantly falls behind that of processors. These two factors contribute to the problems of the computational wall and the storage wall. In response to the above challenges, researchers are committed to addressing issues related to novel AI storage and computing technologies. These technologies aim to break through the storage and computational bottlenecks of AI calculations, improve computational efficiency, and mainly include new applications, computing frameworks, storage-computing architectures, and cloud infrastructure technologies. In terms of hardware architecture, there are two aspects: von Neumann architecture and novel storage-computing architecture. The novel storage-computing architecture can focus on integrated storage-computing chips, neuromorphic chips, and so on. 

The models involved in the robot system require efficient computing, including the following aspects: cloudedge-device integration and smart chips. Cloud-edge-device integration requires unified management, cloud-edge collaboration, and resource allocation. Smart chips need to be small in size, low in power consumption, and high in performance. 

The existing foundation models have a huge amount of parameters, and the training of parameters requires the support of many high-performance graphics cards, which requires a huge cost. In order to reduce the cost and the amount of parameters of the model, a lightweight foundation model is designed while ensuring the performance<sup>[241]</sup> . Additionally, further compression can be performed on the network structure of large-scale models. In addition to adjusting the parameter size, extraction methods such as knowledge distillation, network pruning, low-rank parameter decomposition, and quantization can also be employed. 

# 4.7 Robot Safety and Ethics 

Robot security includes two aspects: physical security and data security. Physical safety refers to the fact that some misunderstandings when combining LLMs with robots may lead to unexpected chain reactions. For example, the robot received instructions to cook Western food in the oven, but it cooked Chinese food. As a result, it turned on the gas and accidentally caught fire. The specificity of robot tasks lies in the constant interaction with the environment during task execution, and robot safety becomes particularly crucial when humans are present in the environment. In the process of completing the specified target tasks, the robot lacks safety guarantee due to physical constraints and other real environment restrictions, and there may be accidents such as collisions, extrusions, and damage to mechanical parts, potentially causing harm to humans. 

There is also data security, which involves data privacy. Privacy risks in robot foundation model development and application primarily come from the information contained in the original training data and the powerful inference capabilities of the models. Developers need to ensure that robot foundation models do not cause privacy breaches and carefully evaluate the potential ethical issues they may bring about. In addition to the data bias in the LLMs being trained, every user will also have information security concerns when training the foundation model and uploading the data to the cloud. The intellectual property rights and data security cannot be guaranteed. This requires the use of data desensitization. In addition to the risks of sensitive information leakage and content infringement, the following risks also exist: model denial of service, model theft, training data poisoning, model hallucination, and attacker prompt injection. Therefore, it is necessary to establish a comprehensive and multi-faceted security evaluation, detection, and defense system. 

Ethically, the behavior of robots should comply with social and legal norms. Developing autonomous robots with self-awareness is also a promising direction. There is growing concern about ethical and safety aspects of robotic learning, including fairness, transparency, and robustness. It is important to pay attention to biases and toxicity in the training samples of robot foundation models to ensure that robots' behavior does not lead to discrimination or unfairness. 

# **5 Conclusion** 

This paper provides an overview of the key challenges of robot learning and the types of algorithms that combine robot learning with foundation models developed to address these challenges. We outline the development and evolution of related technologies for robot learning, as well as the prerequisites such as datasets and computing resources required. We divide these key robot learning challenges into four categories according to downstream tasks, namely manipulation, navigation, planning, and reasoning. With the development of foundational models, they have demonstrated significant progress in robot applications and promising humanoid intelligence<sup>[242]</sup> . These findings present a bright future for foundational models in robot applications. Last but not least, discussions were conducted, which explained the current problems and challenges of robot learning, and proposed research directions in the future, including robot hardware and software decoupling, dynamic data for interaction with the environment, exclusive foundation models for robots, and so on. 

# **References** 

- [1] Yang G-Z, Full R J, Jacobstein N, et al. Ten robotics technologies of the year [M]. American Association for the Advancement of Science. 2019: eaaw1826. 

- [2] Dupont P E, Nelson B J, Goldfarb M, et al. A decade retrospective of medical robotics research from 2010 to 2020[J]. Science Robotics, 2021, 6(60): eabi8017. 

- [3] Clabaugh C, Matarić M. Robots for the people, by the people: Personalizing human-machine interaction[J]. Science Robotics, 2018, 3(21): eaat7451. 

- [4] Tsitsimpelis I, Taylor C J, Lennox B, et al. A review of ground-based robotic systems for the characterization of nuclear environments[J]. Progress in nuclear energy, 2019, 111: 109-124. 

- [5] Kroemer O, Niekum S, Konidaris G. A review of robot learning for manipulation: Challenges, representations, and algorithms[J]. The Journal of Machine Learning Research, 2021, 22(1): 13951476. 

- [6] Yu T, Abbeel P, Levine S, et al. One-shot hierarchical imitation learning of compound visuomotor tasks[J]. arXiv preprint arXiv:1810.11043, 2018. 

- [7] Huang D-A, Xu D, Zhu Y, et al. Continuous relaxation of symbolic planner for one-shot imitation learning[C]//2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2019, 2635-2642. 

- [8] Pauly L, Agboh W C, Hogg D C, et al. O2a: oneshot observational learning with action vectors[J]. Frontiers in Robotics and AI, 2021, 8: 686368. 

- [9] Hussein A, Gaber M M, Elyan E, et al. Imitation learning: A survey of learning methods[J]. ACM Computing Surveys (CSUR), 2017, 50(2): 1-35. 

- [10] Li A, Boots B, Cheng C-A. MAHALO: Unifying Offline Reinforcement Learning and Imitation Learning from Observations[J]. arXiv preprint arXiv:2303.17156, 2023. 

- [11] Pateria S, Subagdja B, Tan A-h, et al. Hierarchical reinforcement learning: A comprehensive survey[J]. ACM Computing Surveys (CSUR), 2021, 54(5): 1- 35. 

- [12] Platt R. Grasp learning: Models, methods, and performance[J]. Annual Review of Control, Robotics, and Autonomous Systems, 2023, 6: 363389. 

- [13] Yang G-Z. Robot learning—Beyond imitation [M]. American Association for the Advancement of Science. 2019: eaaw3520. 

- [14] Billard A, Kragic D. Trends and challenges in robot manipulation[J]. Science, 2019, 364(6446): eaat8414. 

- [15] Zhang H, Tang J, Sun S, et al. Robotic grasping from classical to modern: A survey[J]. arXiv preprint arXiv:2202.03631, 2022. 

- [16] Mavrogiannis C, Baldini F, Wang A, et al. Core challenges of social robot navigation: A survey[J]. ACM Transactions on Human-Robot Interaction, 2023, 12(3): 1-39. 

- [17] Guo H, Wu F, Qin Y, et al. Recent trends in task and motion planning for robotics: A Survey[J]. ACM Computing Surveys, 2023. 

- [18] Antonyshyn L, Silveira J, Givigi S, et al. Multiple mobile robot task and motion planning: A survey[J]. ACM Computing Surveys, 2023, 55(10): 1-35. 

- [19] Liu W, Daruna A, Patel M, et al. A survey of Semantic Reasoning frameworks for robotic systems[J]. Robotics and Autonomous Systems, 2023, 159: 104294. 

- [20] Wang L, Ma C, Feng X, et al. A Survey on Large Language Model based Autonomous Agents[J]. arXiv preprint arXiv:2308.11432, 2023. 

- [21] Muratore F, Ramos F, Turk G, et al. Robot learning from randomized simulations: A review[J]. Frontiers in Robotics and AI, 2022: 31. 

- [22] Vaucher A C, Zipoli F, Geluykens J, et al. Automated extraction of chemical synthesis actions from experimental procedures[J]. Nature communications, 2020, 11(1): 3601. 

- [23] Boiko D A, MacKnight R, Gomes G. Emergent autonomous scientific research capabilities of large language models[J]. arXiv preprint arXiv:2304.05332, 2023. 

- [24] Awais M, Naseer M, Khan S, et al. Foundational Models Defining a New Era in Vision: A Survey and Outlook[J]. arXiv preprint arXiv:2307.13721, 2023. 

- [25] Zhao W X, Zhou K, Li J, et al. A survey of large language models[J]. arXiv preprint arXiv:2303.18223, 2023. 

- [26] Graves A, Srivastava R K, Atkinson T, et al. Bayesian Flow Networks[J]. arXiv preprint arXiv:2308.07037, 2023. 

- [27] Akgun B, Subramanian K. Robot learning from demonstration: kinesthetic teaching vs. teleoperation[J]. Unpublished manuscript, 2011: 26. 

- [28] Agarwal A. Deep Reinforcement Learning with Skill Library : Exploring with Temporal Abstractions and coarse approximate Dynamics Models[C]. 2018. 

- [29] Finn C, Yu T, Zhang T, et al. One-shot visual imitation learning via metalearning[C]//Conference on robot learning. PMLR, 2017, 357-368. 

- [30] Ma Y J, Liang W, Wang G, et al. Eureka: HumanLevel Reward Design via Coding Large Language Models[J]. arXiv preprint arXiv:2310.12931, 2023. 

- [31] Akgun B, Cakmak M, Yoo J W, et al. Trajectories and keyframes for kinesthetic teaching: A humanrobot interaction perspective[C]//Proceedings of the seventh annual ACM/IEEE international conference on Human-Robot Interaction. 2012, 391-398. 

- [32] Kazanzides P, Vagvolgyi B P, Pryor W, et al. Teleoperation and Visualization Interfaces for Remote Intervention in Space[J]. Frontiers in Robotics and AI, 2021, 8: 747917. 

- [33] Sutton R S, Barto A G. Reinforcement learning: An introduction[M]. MIT press, 2018. 

- [34] Ho J, Ermon S. Generative adversarial imitation learning[J]. Advances in neural information processing systems, 2016, 29. 

- [35] Meng F, Shao W, Peng Z, et al. Foundation Model is Efficient Multimodal Multitask Model Selector[J]. arXiv preprint arXiv:2308.06262, 2023. 

- [36] Yin S, Fu C, Zhao S, et al. A Survey on Multimodal Large Language Models[J]. arXiv preprint arXiv:2306.13549, 2023. 

- [37] Wang J, Liu Z, Zhao L, et al. Review of large vision models and visual prompt engineering[J]. arXiv preprint arXiv:2307.00855, 2023. 

- [38] Kaddour J, Harris J, Mozes M, et al. Challenges and Applications of Large Language Models[J]. arXiv preprint arXiv:2307.10169, 2023. 

- [39] Zhou S, Xu F F, Zhu H, et al. WebArena: A Realistic Web Environment for Building Autonomous Agents[J]. arXiv preprint arXiv:2307.13854, 2023. 

- [40] Gan Z, Li L, Li C, et al. Vision-language pretraining: Basics, recent advances, and future trends[J]. Foundations and Trends® in Computer Graphics and Vision, 2022, 14(3–4): 163-352. 

- [41] Shen L, Shen E, Luo Y, et al. Towards natural language interfaces for data visualization: A survey[J]. IEEE transactions on visualization and computer graphics, 2022. 

- [42] Narayanan D, Shoeybi M, Casper J, et al. Efficient large-scale language model training on gpu clusters using megatron-lm[C]//Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis. 2021, 1-15. 

- [43] Duan J, Yu S, Tan H L, et al. A survey of embodied ai: From simulators to research tasks[J]. IEEE Transactions on Emerging Topics in Computational Intelligence, 2022, 6(2): 230-244. 

- [44] Chen K, Hoque R, Dharmarajan K, et al. FogROS2SGC: A ROS2 Cloud Robotics Platform for Secure Global Connectivity[J]. arXiv preprint arXiv:2306.17157, 2023. 

- [45] Awadalla A, Gao I, Gardner J, et al. OpenFlamingo: An Open-Source Framework for Training Large Autoregressive Vision-Language Models[J]. arXiv preprint arXiv:2308.01390, 2023. 

- [46] Zhou G, Dean V, Srirama M K, et al. Train Offline, Test Online: A Real Robot Learning Benchmark[J]. arXiv preprint arXiv:2306.00942, 2023. 

- [47] Liang X, Ma L, Guo S, et al. MO-VLN: A MultiTask Benchmark for Open-set Zero-Shot Visionand-Language Navigation[J]. arXiv preprint arXiv:2306.10322, 2023. 

- [48] Guo A, Wen B, Yuan J, et al. HANDAL: A Dataset of Real-World Manipulable Object Categories with Pose Annotations, Affordances, and Reconstructions[J]. arXiv preprint arXiv:2308.01477, 2023. 

- [49] Elangovan N, Godoy R V, Sanches F, et al. On Human Grasping and Manipulation in Kitchens: Automated Annotation, Insights, and Metrics for Effective Data Collection[C]//2023 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2023, 11329-11335. 

- [50] Shridhar M, Yuan X, Côté M-A, et al. Alfworld: Aligning text and embodied environments for interactive learning[J]. arXiv preprint arXiv:2010.03768, 2020. 

- [51] Yang J, Jin H, Tang R, et al. Harnessing the power of llms in practice: A survey on chatgpt and beyond[J]. arXiv preprint arXiv:2304.13712, 2023. 

- [52] Liang Y, Wu C, Song T, et al. Taskmatrix. ai: Completing tasks by connecting foundation models with millions of apis[J]. arXiv preprint arXiv:2303.16434, 2023. 

- [53] Qin Y, Liang S, Ye Y, et al. ToolLLM: Facilitating Large Language Models to Master 16000+ Realworld APIs[J]. arXiv preprint arXiv:2307.16789, 2023. 

- [54] Wei J, Tay Y, Bommasani R, et al. Emergent abilities of large language models[J]. arXiv preprint arXiv:2206.07682, 2022. 

- [55] Vemprala S, Bonatti R, Bucker A, et al. Chatgpt for robotics: Design principles and model abilities[J]. Microsoft Auton. Syst. Robot. Res, 2023, 2: 20. 

- [56] Tedrake R. Robot manipulation: Perception, planning, and control[J]. Downloaded on March, 2021. 

- [57] Cui J, Trinkle J. Toward next-generation learned robot manipulation[J]. Science Robotics, 2021, 6(54): eabd9461. 

- [58] Kim M J, Wu J, Finn C. Giving Robots a Hand: Learning Generalizable Manipulation with Eye-inHand Human Video Demonstrations[J]. arXiv preprint arXiv:2307.05959, 2023. 

- [59] Gao F, Li X, Yu J, et al. A Two-stage Fine-tuning Strategy for Generalizable Manipulation Skill of Embodied AI[J]. arXiv preprint arXiv:2307.11343, 2023. 

- [60] Puig X, Ra K, Boben M, et al. Virtualhome: Simulating household activities via programs[C]//Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 2018, 8494-8502. 

- [61] Huang W, Abbeel P, Pathak D, et al. Language models as zero-shot planners: Extracting actionable knowledge for embodied agents[C]//International Conference on Machine Learning. PMLR, 2022, 9118-9147. 

- [62] Brohan A, Brown N, Carbajal J, et al. Rt-1: Robotics transformer for real-world control at scale[J]. arXiv preprint arXiv:2212.06817, 2022. 

- [63] Fu H, Xu W, Xue H, et al. Rfuniverse: A physicsbased action-centric interactive environment for everyday household tasks[J]. arXiv preprint arXiv:2202.00199, 2022. 

- [64] Wu J, Antonova R, Kan A, et al. Tidybot: Personalized robot assistance with large language models[J]. arXiv preprint arXiv:2305.05658, 2023. 

- [65] Gu J, Xiang F, Li X, et al. Maniskill2: A unified benchmark for generalizable manipulation skills[J]. arXiv preprint arXiv:2302.04659, 2023. 

- [66] Jia Z, Liu F, Thumuluri V, et al. Chain-of-Thought Predictive Control[J]. arXiv preprint arXiv:2304.00776, 2023. 

- [67] Wang H, Zhang H, Li L, et al. Task-Driven Reinforcement Learning With Action Primitives for Long-Horizon Manipulation Skills[J]. IEEE Transactions on Cybernetics, 2023. 

- [68] Ha H, Florence P, Song S. Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition[J]. arXiv preprint arXiv:2307.14535, 2023. 

- [69] Xiao T, Chan H, Sermanet P, et al. Robotic skill acquisition via instruction augmentation with vision-language models[J]. arXiv preprint arXiv:2211.11736, 2022. 

- [70] Wang Y, Xian Z, Chen F, et al. RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation[J]. arXiv preprint arXiv:2311.01455, 2023. 

- [71] Shridhar M, Manuelli L, Fox D. Cliport: What and where pathways for robotic 

manipulation[C]//Conference on Robot Learning. PMLR, 2022, 894-906. 

- [72] Khandelwal A, Weihs L, Mottaghi R, et al. Simple but effective: Clip embeddings for embodied ai[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2022, 14829-14838. 

- [73] Wang R, Mao J, Hsu J, et al. Programmatically Grounded, Compositionally Generalizable Robotic Manipulation[J]. arXiv preprint arXiv:2304.13826, 2023. 

- [74] Huang W, Wang C, Zhang R, et al. VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models[J]. arXiv preprint arXiv:2307.05973, 2023. 

- [75] Mo Y, Zhang H, Kong T. Towards Open-World Interactive Disambiguation for Robotic Grasping[C]//2023 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2023, 8061-8067. 

- [76] Ze Y, Yan G, Wu Y-H, et al. GNFactor: Multi-Task Real Robot Learning with Generalizable Neural Feature Fields[J]. arXiv preprint arXiv:2308.16891, 2023. 

- [77] Zheng J, Zheng Q, Fang L, et al. CAMS: CAnonicalized Manipulation Spaces for CategoryLevel Functional Hand-Object Manipulation Synthesis[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2023, 585-594. 

- [78] Yenamandra S, Ramachandran A, Yadav K, et al. HomeRobot: Open-Vocabulary Mobile Manipulation[J]. arXiv preprint arXiv:2306.11565, 2023. 

- [79] Tam A, Rabinowitz N, Lampinen A, et al. Semantic exploration from language abstractions and pretrained representations[J]. Advances in neural information processing systems, 2022, 35: 2537725389. 

- [80] Wan W, Geng H, Liu Y, et al. UniDexGrasp++: Improving Dexterous Grasping Policy Learning via Geometry-aware Curriculum and Iterative Generalist-Specialist Learning[J]. arXiv preprint arXiv:2304.00464, 2023. 

- [81] Gordon E K, Zarrin R S. Online augmentation of learned grasp sequence policies for more adaptable and data-efficient in-hand manipulation[J]. arXiv preprint arXiv:2304.02052, 2023. 

- [82] Haldar S, Pari J, Rai A, et al. Teach a Robot to FISH: Versatile Imitation from One Minute of Demonstrations[J]. arXiv preprint arXiv:2303.01497, 2023. 

- [83] Wang R, Zhang J, Chen J, et al. Dexgraspnet: A large-scale robotic dexterous grasp dataset for general objects based on simulation[C]//2023 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2023, 11359-11366. 

- [84] Guzey I, Evans B, Chintala S, et al. Dexterity from Touch: Self-Supervised Pre-Training of Tactile Representations with Robotic Play[J]. arXiv preprint arXiv:2303.12076, 2023. 

- [85] Bao C, Xu H, Qin Y, et al. DexArt: Benchmarking Generalizable Dexterous Manipulation with Articulated Objects[C]//Proceedings of the 

IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2023, 21190-21200. 

- [86] Ota K, Jain S, Zhang M, et al. Tactile Pose Feedback for Closed-loop Manipulation Tasks[J]. 

- [87] Shaw K, Pathak D. Leap hand: Low-cost, efficient, and anthropomorphic hand for robot learning[J]. Submission, ICRA, 2023. 

- [88] Kannan A, Shaw K, Bahl S, et al. DEFT: Dexterous Fine-Tuning for Real-World Hand Policies[C]//7th Annual Conference on Robot Learning. 2023. 

- [89] Han Y, Xie M, Zhao Y, et al. On the Utility of Koopman Operator Theory in Learning Dexterous Manipulation Skills[J]. arXiv preprint arXiv:2303.13446, 2023. 

- [90] Lin X, So J, Mahalingam S, et al. SpawnNet: Learning Generalizable Visuomotor Skills from Pre-trained Networks[J]. arXiv preprint arXiv:2307.03567, 2023. 

- [91] Huang B, Chen Y, Wang T, et al. Dynamic Handover: Throw and Catch with Bimanual Hands[C]//7th Annual Conference on Robot Learning. 2023. 

- [92] Seo M, Han S, Sim K, et al. Deep Imitation Learning for Humanoid Loco-manipulation through Human Teleoperation[J]. arXiv preprint arXiv:2309.01952, 2023. 

- [93] Chen T, Xu J, Agrawal P. A system for general inhand object re-orientation[C]//Conference on Robot Learning. PMLR, 2022, 297-307. 

- [94] Radosavovic I, Xiao T, Zhang B, et al. Learning Humanoid Locomotion with Transformers[J]. arXiv preprint arXiv:2303.03381, 2023. 

- [95] Stella F, Della Santina C, Hughes J. How can LLMs transform the robotic design process?[J]. Nature Machine Intelligence, 2023: 1-4. 

- [96] Yin Z-H, Huang B, Qin Y, et al. Rotating without Seeing: Towards In-hand Dexterity through Touch[J]. arXiv preprint arXiv:2303.10880, 2023. 

- [97] Wu S, Fei H, Qu L, et al. Next-gpt: Any-to-any multimodal llm[J]. arXiv preprint arXiv:2309.05519, 2023. 

- [98] Li C, Gan Z, Yang Z, et al. Multimodal Foundation Models: From Specialists to General-Purpose Assistants[J]. arXiv preprint arXiv:2309.10020, 2023. 

- [99] Yang T, Jing Y, Wu H, et al. MOMA-Force: VisualForce Imitation for Real-World Mobile Manipulation[J]. arXiv preprint arXiv:2308.03624, 2023. 

- [100] Jiang Y, Gupta A, Zhang Z, et al. VIMA: Robot Manipulation with Multimodal Prompts[J]. 2023. 

- [101] Rubenstein P K, Asawaroengchai C, Nguyen D D, et al. AudioPaLM: A Large Language Model That Can Speak and Listen[J]. arXiv preprint arXiv:2306.12925, 2023. 

- [102] Brohan A, Brown N, Carbajal J, et al. RT-2: VisionLanguage-Action Models Transfer Web Knowledge to Robotic Control[J]. arXiv preprint arXiv:2307.15818, 2023. 

- [103] He H M. Robotgpt: From chatgpt to robot intelligence[J]. 2023. 

- [104] Luo Z, Cao J, Winkler A, et al. Perpetual Humanoid Control for Real-time Simulated Avatars[J]. arXiv preprint arXiv:2305.06456, 2023. 

- [105] Gandhi D, Gupta A, Pinto L. Swoosh! Rattle! Thump!--Actions that Sound[J]. arXiv preprint arXiv:2007.01851, 2020. 

- [106] Peng Z, Wang W, Dong L, et al. Kosmos-2: Grounding Multimodal Large Language Models to the World[J]. arXiv preprint arXiv:2306.14824, 2023. 

- [107] Radosavovic I, Shi B, Fu L, et al. Robot Learning with Sensorimotor Pre-training[J]. arXiv preprint arXiv:2306.10007, 2023. 

- [108] Li H, Zhang Y, Zhu J, et al. See, Hear, and Feel: Smart Sensory Fusion for Robotic Manipulation (Supplementary Materials)[J]. 

- [109] Lee B K, Mayhew E J, Sanchez-Lengeling B, et al. A principal odor map unifies diverse tasks in olfactory perception[J]. Science, 2023, 381(6661): 999-1006. 

- [110] Guzey I, Dai Y, Evans B, et al. See to Touch: Learning Tactile Dexterity through Visual Incentives[J]. arXiv preprint arXiv:2309.12300, 2023. 

- [111] Manglani S. Real-time Vision-based Navigation for a Robot in an Indoor Environment[J]. arXiv preprint arXiv:2307.00666, 2023. 

- [112] Wolbers T, Hegarty M. What determines our navigational abilities?[J]. Trends in cognitive sciences, 2010, 14(3): 138-146. 

- [113] Lynch C, Wahid A, Tompson J, et al. Interactive language: Talking to robots in real time[J]. IEEE Robotics and Automation Letters, 2023. 

- [114] Tavassoli R, Amani M, Akhavian R. Expanding Frozen Vision-Language Models without Retraining: Towards Improved Robot Perception[J]. arXiv preprint arXiv:2308.16493, 2023. 

- [115] Chen H, Suhr A, Misra D, et al. Touchdown: Natural language navigation and spatial reasoning in visual street environments[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2019, 12538-12547. 

- [116] Hong Y, Wang Z, Wu Q, et al. Bridging the gap between learning in discrete and continuous environments for vision-and-language navigation[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2022, 15439-15449. 

- [117] Tan H, Yu L, Bansal M. Learning to navigate unseen environments: Back translation with environmental dropout[J]. arXiv preprint arXiv:1904.04195, 2019. 

- [118] Qi Y, Pan Z, Zhang S, et al. Object-and-action aware model for visual language navigation[C]//European Conference on Computer Vision. Springer, 2020, 303-317. 

- [119] Yang W, Wang X, Farhadi A, et al. Visual semantic navigation using scene priors[J]. arXiv preprint arXiv:1810.06543, 2018. 

- [120] Du H, Yu X, Zheng L. Learning object relation graph and tentative policy for visual navigation[C]//Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part VII 16. Springer, 2020, 19-34. 

- [121] Zhang S, Song X, Li W, et al. Layout-Based Causal Inference for Object Navigation[C]//Proceedings 

- of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2023, 10792-10802. 

- [122] Gervet T, Chintala S, Batra D, et al. Navigating to objects in the real world[J]. Science Robotics, 2023, 8(79): eadf6991. 

- [123] Huang C, Mees O, Zeng A, et al. Visual language maps for robot navigation[C]//2023 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2023, 10608-10615. 

- [124] An D, Qi Y, Li Y, et al. BEVBert: Topo-Metric Map Pre-training for Language-guided Navigation[J]. arXiv preprint arXiv:2212.04385, 2022. 

- [125] Jia Z, Lin K, Zhao Y, et al. Learning to act with affordance-aware multimodal neural slam[C]//2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2022, 5877-5884. 

- [126] Gadre S Y, Wortsman M, Ilharco G, et al. Cows on pasture: Baselines and benchmarks for languagedriven zero-shot object navigation[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2023, 23171-23181. 

- [127] Keetha N, Mishra A, Karhade J, et al. AnyLoc: Towards Universal Visual Place Recognition[J]. arXiv preprint arXiv:2308.00688, 2023. 

- [128] Hahn M, Krantz J, Batra D, et al. Where are you? localization from embodied dialog[J]. arXiv preprint arXiv:2011.08277, 2020. 

- [129] De Vries H, Shuster K, Batra D, et al. Talk the walk: Navigating new york city through grounded dialogue[J]. arXiv preprint arXiv:1807.03367, 2018. 

- [130] Hong Y, Wu Q, Qi Y, et al. Vln bert: A recurrent vision-and-language bert for navigation[C]//Proceedings of the IEEE/CVF conference on Computer Vision and Pattern Recognition. 2021, 1643-1653. 

- [131] Lin B, Zhu Y, Chen Z, et al. Adapt: Vision-language navigation with modality-aligned action prompts[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2022, 15396-15406. 

- [132] Xie A, Lee Y, Abbeel P, et al. LanguageConditioned Path Planning[J]. arXiv preprint arXiv:2308.16893, 2023. 

- [133] Zhou G, Hong Y, Wu Q. NavGPT: Explicit Reasoning in Vision-and-Language Navigation with Large Language Models[J]. arXiv preprint arXiv:2305.16986, 2023. 

- [134] Qiao Y, Qi Y, Yu Z, et al. March in Chat: Interactive Prompting for Remote Embodied Referring Expression[J]. arXiv preprint arXiv:2308.10141, 2023. 

- [135] Fried D, Hu R, Cirik V, et al. Speaker-follower models for vision-and-language navigation[J]. Advances in neural information processing systems, 2018, 31. 

- [136] Wang X, Huang Q, Celikyilmaz A, et al. Reinforced cross-modal matching and self-supervised imitation learning for vision-language navigation[C]//Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2019, 6629-6638. 

- [137] Nguyen K, Daumé III H. Help, anna! visual navigation with natural multimodal assistance via retrospective curiosity-encouraging imitation learning[J]. arXiv preprint arXiv:1909.01871, 2019. 

- [138] Shridhar M, Thomason J, Gordon D, et al. Alfred: A benchmark for interpreting grounded instructions for everyday tasks[C]//Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2020, 10740-10749. 

- [139] Anderson P, Wu Q, Teney D, et al. Vision-andlanguage navigation: Interpreting visuallygrounded navigation instructions in real environments[C]//Proceedings of the IEEE conference on computer vision and pattern recognition. 2018, 3674-3683. 

- [140] Qi Y, Wu Q, Anderson P, et al. Reverie: Remote embodied visual referring expression in real indoor environments[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2020, 9982-9991. 

- [141] Yang S, Nachum O, Du Y, et al. Foundation models for decision making: Problems, methods, and opportunities[J]. arXiv preprint arXiv:2303.04129, 2023. 

- [142] Liu B, Jiang Y, Zhang X, et al. Llm+ p: Empowering large language models with optimal planning proficiency[J]. arXiv preprint arXiv:2304.11477, 2023. 

- [143] Wu Z, Wang Z, Xu X, et al. Embodied Task Planning with Large Language Models[J]. arXiv preprint arXiv:2307.01848, 2023. 

- [144] Lin K, Agia C, Migimatsu T, et al. Text2motion: From natural language instructions to feasible plans[J]. arXiv preprint arXiv:2303.12153, 2023. 

- [145] Wake N, Kanehira A, Sasabuchi K, et al. Chatgpt empowered long-step robot control in various environments: A case application[J]. arXiv preprint arXiv:2304.03893, 2023. 

- [146] Mu Y, Zhang Q, Hu M, et al. Embodiedgpt: Visionlanguage pre-training via embodied chain of thought[J]. arXiv preprint arXiv:2305.15021, 2023. 

- [147] Ruan J, Chen Y, Zhang B, et al. TPTU: Task Planning and Tool Usage of Large Language Model-based AI Agents[J]. arXiv preprint arXiv:2308.03427, 2023. 

- [148] Zhen Y, Bi S, Xing-tong L, et al. Robot Task Planning Based on Large Language Model Representing Knowledge with Directed Graph Structures[J]. arXiv preprint arXiv:2306.05171, 2023. 

- [149] Gu J, Chaplot D S, Su H, et al. Multi-skill mobile manipulation for object rearrangement[J]. arXiv preprint arXiv:2209.02778, 2022. 

- [150] Obinata Y, Kanazawa N, Kawaharazuka K, et al. Foundation Model based Open Vocabulary Task Planning and Executive System for General Purpose Service Robots[J]. arXiv preprint arXiv:2308.03357, 2023. 

- [151] Shi H, Xu H, Clarke S, et al. RoboCook: LongHorizon Elasto-Plastic Object Manipulation with Diverse Tools[J]. arXiv preprint arXiv:2306.14447, 2023. 

- [152] Sun X, Cheng H, Li J, et al. All in One: Multi-Task Prompting for Graph Neural Networks[J]. 2023. 

- [153] Xu Y, Wang S, Li P, et al. Exploring Large Language Models for Communication Games: An Empirical Study on Werewolf[J]. arXiv preprint arXiv:2309.04658, 2023. 

- [154] Zhang H, Du W, Shan J, et al. Building Cooperative Embodied Agents Modularly with Large Language Models[J]. arXiv preprint arXiv:2307.02485, 2023. 

- [155] Mandi Z, Jain S, Song S. RoCo: Dialectic MultiRobot Collaboration with Large Language Models[J]. arXiv preprint arXiv:2307.04738, 2023. 

- [156] Qian C, Cong X, Yang C, et al. Communicative agents for software development[J]. arXiv preprint arXiv:2307.07924, 2023. 

- [157] Baker B, Kanitscheider I, Markov T, et al. Emergent tool use from multi-agent autocurricula[J]. arXiv preprint arXiv:1909.07528, 2019. 

- [158] Pan L, Saxon M, Xu W, et al. Automatically Correcting Large Language Models: Surveying the landscape of diverse self-correction strategies[J]. arXiv preprint arXiv:2308.03188, 2023. 

- [159] Sharma P, Sundaralingam B, Blukis V, et al. Correcting robot plans with natural language feedback[J]. arXiv preprint arXiv:2204.05186, 2022. 

- [160] Liu Z, Bahety A, Song S. Reflect: Summarizing robot experiences for failure explanation and correction[J]. arXiv preprint arXiv:2306.15724, 2023. 

- [161] Shinn N, Labash B, Gopinath A. Reflexion: an autonomous agent with dynamic memory and selfreflection[J]. arXiv preprint arXiv:2303.11366, 2023. 

- [162] Bousmalis K, Vezzani G, Rao D, et al. RoboCat: A Self-Improving Foundation Agent for Robotic Manipulation[J]. arXiv preprint arXiv:2306.11706, 2023. 

- [163] Miao N, Teh Y W, Rainforth T. SelfCheck: Using LLMs to Zero-Shot Check Their Own Step-by-Step Reasoning[J]. arXiv preprint arXiv:2308.00436, 2023. 

- [164] Olausson T X, Inala J P, Wang C, et al. Demystifying GPT Self-Repair for Code Generation[J]. arXiv preprint arXiv:2306.09896, 2023. 

- [165] Wang L, Zhang X, Su H, et al. A comprehensive survey of continual learning: Theory, method and application[J]. arXiv preprint arXiv:2302.00487, 2023. 

- [166] Guo Y, Wang Y-J, Zha L, et al. DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment[J]. arXiv preprint arXiv:2307.00329, 2023. 

- [167] Peng S, Hu X, Yi Q, et al. Self-driven Grounding: Large Language Model Agents with Automatical Language-aligned Skill Learning[J]. arXiv preprint arXiv:2309.01352, 2023. 

- [168] Liang J, Huang W, Xia F, et al. Code as policies: Language model programs for embodied control[C]//2023 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2023, 9493-9500. 

- [169] Guha N, Chen M F, Bhatia K, et al. Embroid: Unsupervised Prediction Smoothing Can Improve 

- Few-Shot Classification[J]. arXiv preprint arXiv:2307.11031, 2023. 

- [170] Dou S, Shan J, Jia H, et al. Towards Understanding the Capability of Large Language Models on Code Clone Detection: A Survey[J]. arXiv preprint arXiv:2308.01191, 2023. 

- [171] Jiang D, Ren X, Lin B Y. LLM-Blender: Ensembling Large Language Models with Pairwise Ranking and Generative Fusion[J]. arXiv preprint arXiv:2306.02561, 2023. 

- [172] Zheng Q, Xia X, Zou X, et al. Codegeex: A pretrained model for code generation with multilingual evaluations on humaneval-x[J]. arXiv preprint arXiv:2303.17568, 2023. 

- [173] Yang C, Wang X, Lu Y, et al. Large Language Models as Optimizers[J]. arXiv preprint arXiv:2309.03409, 2023. 

- [174] Yang H, Yue S, He Y. Auto-GPT for Online Decision Making: Benchmarks and Additional Opinions[J]. arXiv preprint arXiv:2306.02224, 2023. 

- [175] Chen B, Zhang F, Nguyen A, et al. Codet: Code generation with generated tests[J]. arXiv preprint arXiv:2207.10397, 2022. 

- [176] Yao S, Chen H, Yang J, et al. Webshop: Towards scalable real-world web interaction with grounded language agents[J]. Advances in neural information processing systems, 2022, 35: 20744-20757. 

- [177] Yang J, Prabhakar A, Narasimhan K, et al. InterCode: Standardizing and Benchmarking Interactive Coding with Execution Feedback[J]. arXiv preprint arXiv:2306.14898, 2023. 

- [178] Yao S, Chen H, Hanjie A W, et al. COLLIE: Systematic Construction of Constrained Text Generation Tasks[J]. arXiv preprint arXiv:2307.08689, 2023. 

- [179] Mandlekar A, Nasiriany S, Wen B, et al. MimicGen: A Data Generation System for Scalable Robot Learning using Human Demonstrations[J]. arXiv preprint arXiv:2310.17596, 2023. 

- [180] Triantafyllidis E, Acero F, Liu Z, et al. Hybrid hierarchical learning for solving complex sequential tasks using the robotic manipulation network ROMAN[J]. Nature Machine Intelligence, 2023: 1-15. 

- [181] Sumers T, Yao S, Narasimhan K, et al. Cognitive Architectures for Language Agents[J]. arXiv preprint arXiv:2309.02427, 2023. 

- [182] Huang J, Chang K C-C. Towards reasoning in large language models: A survey[J]. arXiv preprint arXiv:2212.10403, 2022. 

- [183] Lai X, Tian Z, Chen Y, et al. LISA: Reasoning Segmentation via Large Language Model[J]. arXiv preprint arXiv:2308.00692, 2023. 

- [184] Qiao S, Ou Y, Zhang N, et al. Reasoning with language model prompting: A survey[J]. arXiv preprint arXiv:2212.09597, 2022. 

- [185] Wang R, Zelikman E, Poesia G, et al. Hypothesis Search: Inductive Reasoning with Language Models[J]. arXiv preprint arXiv:2309.05660, 2023. 

- [186] Cheng G, Ramirez-Amaro K, Beetz M, et al. Purposive learning: Robot reasoning about the meanings of human activities[J]. Science Robotics, 2019, 4(26): eaav1530. 

- [187] Wei J, Wang X, Schuurmans D, et al. Chain-ofthought prompting elicits reasoning in large language models[J]. Advances in neural information processing systems, 2022, 35: 2482424837. 

- [188] Yao S, Yu D, Zhao J, et al. Tree of thoughts: Deliberate problem solving with large language models[J]. arXiv preprint arXiv:2305.10601, 2023. 

- [189] Driess D, Xia F, Sajjadi M S, et al. Palm-e: An embodied multimodal language model[J]. arXiv preprint arXiv:2303.03378, 2023. 

- [190] Yao S, Zhao J, Yu D, et al. React: Synergizing reasoning and acting in language models[J]. arXiv preprint arXiv:2210.03629, 2022. 

- [191] Zhang Y, Yang J, Yuan Y, et al. Cumulative Reasoning With Large Language Models[J]. arXiv preprint arXiv:2308.04371, 2023. 

- [192] Ding N, Levinboim T, Wu J, et al. CausalLM is not optimal for in-context learning[J]. arXiv preprint arXiv:2308.06912, 2023. 

- [193] Deng Z, Jiang J, Long G, et al. Causal Reinforcement Learning: A Survey[J]. arXiv preprint arXiv:2307.01452, 2023. 

- [194] Pan S, Luo L, Wang Y, et al. Unifying Large Language Models and Knowledge Graphs: A Roadmap[J]. arXiv preprint arXiv:2306.08302, 2023. 

- [195] Mihindukulasooriya N, Tiwari S, Enguix C F, et al. Text2KGBench: A Benchmark for OntologyDriven Knowledge Graph Generation from Text[J]. arXiv preprint arXiv:2308.02357, 2023. 

- [196] Kim J, Kwon Y, Jo Y, et al. KG-GPT: A General Framework for Reasoning on Knowledge Graphs Using Large Language Models[J]. arXiv preprint arXiv:2310.11220, 2023. 

- [197] Zhu Y, Wang X, Chen J, et al. LLMs for Knowledge Graph Construction and Reasoning: Recent Capabilities and Future Opportunities[J]. arXiv preprint arXiv:2305.13168, 2023. 

- [198] Yang L, Chen H, Li Z, et al. ChatGPT is not Enough: Enhancing Large Language Models with Knowledge Graphs for Fact-aware Language Modeling[J]. arXiv preprint arXiv:2306.11489, 2023. 

- [199] Ren A Z, Dixit A, Bodrova A, et al. Robots that ask for help: Uncertainty alignment for large language model planners[J]. arXiv preprint arXiv:2307.01928, 2023. 

- [200] Zellers R, Holtzman A, Peters M, et al. PIGLeT: Language grounding through neuro-symbolic interaction in a 3D world[J]. arXiv preprint arXiv:2106.00188, 2021. 

- [201] Zhu Z, Ma X, Chen Y, et al. 3D-VisTA: Pre-trained Transformer for 3D Vision and Text Alignment[J]. arXiv preprint arXiv:2308.04352, 2023. 

- [202] Tang J, Yang Y, Wei W, et al. GraphGPT: Graph Instruction Tuning for Large Language Models[J]. arXiv preprint arXiv:2310.13023, 2023. 

- [203] Wu P, Escontrela A, Hafner D, et al. Daydreamer: World models for physical robot learning[C]//Conference on Robot Learning. PMLR, 2023, 2226-2240. 

- [204] Singh I, Blukis V, Mousavian A, et al. Progprompt: Generating situated robot task plans using large 

|language models[C]//2023 IEEE International|
|---|
|Conference on Robotics and Automation (ICRA).|
|IEEE, 2023, 11523-11530.|


- [205] Ahn M, Brohan A, Brown N, et al. Do as i can, not as i say: Grounding language in robotic affordances[J]. arXiv preprint arXiv:2204.01691, 2022. 

- [206] Yoneda T, Fang J, Li P, et al. Statler: Statemaintaining language models for embodied reasoning[J]. arXiv preprint arXiv:2306.17840, 2023. 

- [207] Gao J, Sarkar B, Xia F, et al. Physically Grounded Vision-Language Models for Robotic Manipulation[J]. arXiv preprint arXiv:2309.02561, 2023. 

- [208] Tang J, Zheng G, Yu J, et al. CoTDet: Affordance Knowledge Prompting for Task Driven Object Detection[J]. arXiv preprint arXiv:2309.01093, 2023. 

- [209] Bajcsy A, Loquercio A, Kumar A, et al. Learning Vision-based Pursuit-Evasion Robot Policies[J]. arXiv preprint arXiv:2308.16185, 2023. 

- [210] Chen J, Liu Z, Huang X, et al. When large language models meet personalization: Perspectives of challenges and opportunities[J]. arXiv preprint arXiv:2307.16376, 2023. 

- [211] Safdari M, Serapio-García G, Crepy C, et al. Personality traits in large language models[J]. arXiv preprint arXiv:2307.00184, 2023. 

- [212] Huang J-t, Lam M H, Li E J, et al. Emotionally Numb or Empathetic? Evaluating How LLMs Feel Using EmotionBench[J]. arXiv preprint arXiv:2308.03656, 2023. 

- [213] Ding Z, Chen Y, Ren A Z, et al. Learning a Universal Human Prior for Dexterous Manipulation from Human Preference[J]. arXiv preprint arXiv:2304.04602, 2023. 

- [214] Deng K, Ray A, Tan R, et al. Socratis: Are large multimodal models emotionally aware?[J]. arXiv preprint arXiv:2308.16741, 2023. 

- [215] Lian Z, Sun L, Xu M, et al. Explainable Multimodal Emotion Reasoning[J]. arXiv preprint arXiv:2306.15401, 2023. 

- [216] Achtibat R, Dreyer M, Eisenbraun I, et al. From attribution maps to human-understandable explanations through Concept Relevance Propagation[J]. Nature Machine Intelligence, 2023, 5(9): 1006-1019. 

- [217] Nilforoshan H, Moor M, Roohani Y, et al. Zero-shot causal learning[J]. arXiv preprint arXiv:2301.12292, 2023. 

- [218] Mengüç Y, Correll N, Kramer R, et al. Will robots be bodies with brains or brains with bodies?[J]. Science Robotics, 2017, 2(12): eaar4527. 

- [219] García S, Strüber D, Brugali D, et al. Software variability in service robotics[J]. Empirical Software Engineering, 2023, 28(2): 24. 

- [220] Jiang S, Kang P, Song X, et al. Emerging wearable interfaces and algorithms for hand gesture recognition: A survey[J]. IEEE Reviews in Biomedical Engineering, 2021, 15: 85-102. 

- [221] Jiang S, Strout Z, He B, et al. Dual Stream Meta Learning for Road Surface Classification and Riding Event Detection on Shared Bikes[J]. IEEE 

   - Transactions on Systems, Man, and Cybernetics: Systems, 2023. 

- [222] Jin Z, Si W, Liu A, et al. Learning a Flexible Neural Energy Function With a Unique Minimum for Globally Stable and Accurate Demonstration Learning[J]. IEEE Transactions on Robotics, 2023. 

- [223] Christiano P, Shlegeris B, Amodei D. Supervising strong learners by amplifying weak experts[J]. arXiv preprint arXiv:1810.08575, 2018. 

- [224] Aru J, Larkum M, Shine J M. The feasibility of artificial consciousness through the lens of neuroscience[J]. arXiv preprint arXiv:2306.00915, 2023. 

- [225] Ren P, Xiao Y, Chang X, et al. A survey of deep active learning[J]. ACM Computing Surveys (CSUR), 2021, 54(9): 1-40. 

- [226] Zhai Y, Tong S, Li X, et al. Investigating the Catastrophic Forgetting in Multimodal Large Language Models[J]. arXiv preprint arXiv:2309.10313, 2023. 

- [227] Ji Z, Lee N, Frieske R, et al. Survey of hallucination in natural language generation[J]. ACM Computing Surveys, 2023, 55(12): 1-38. 

- [228] Gunjal A, Yin J, Bas E. Detecting and Preventing Hallucinations in Large Vision Language Models[J]. arXiv preprint arXiv:2308.06394, 2023. 

- [229] Xi Z, Chen W, Guo X, et al. The Rise and Potential of Large Language Model Based Agents: A Survey[J]. arXiv preprint arXiv:2309.07864v2, 2023. 

- [230] Yang Z, Li L, Lin K, et al. The Dawn of LMMs: Preliminary Explorations with GPT-4V(ision)[C]. 2023. 

- [231] Xu C, Xu Y, Wang S, et al. Small models are valuable plug-ins for large language models[J]. arXiv preprint arXiv:2305.08848, 2023. 

- [232] Yu W, Gileadi N, Fu C, et al. Language to Rewards for Robotic Skill Synthesis[J]. arXiv preprint arXiv:2306.08647, 2023. 

- [233] Peng Y, Han J, Zhang Z, et al. The Tong Test: Evaluating Artificial General Intelligence Through Dynamic Embodied Physical and Social Interactions[J]. Engineering, 2023. 

- [234] Zhuang Z, Chen Q, Ma L, et al. Through the Lens of Core Competency: Survey on Evaluation of Large Language Models[J]. arXiv preprint arXiv:2308.07902, 2023. 

- [235] Liu X, Yu H, Zhang H, et al. AgentBench: Evaluating LLMs as Agents[J]. arXiv preprint arXiv:2308.03688, 2023. 

- [236] Dalvi F, Hasanain M, Boughorbel S, et al. LLMeBench: A Flexible Framework for Accelerating LLMs Benchmarking[J]. arXiv preprint arXiv:2308.04945, 2023. 

- [237] Chang Y, Wang X, Wang J, et al. A survey on evaluation of large language models[J]. arXiv preprint arXiv:2307.03109, 2023. 

- [238] Bang Y, Cahyawijaya S, Lee N, et al. A multitask, multilingual, multimodal evaluation of chatgpt on reasoning, hallucination, and interactivity[J]. arXiv preprint arXiv:2302.04023, 2023. 

- [239] Srivastava A, Rastogi A, Rao A, et al. Beyond the imitation game: Quantifying and extrapolating the 

capabilities of language models[J]. arXiv preprint arXiv:2206.04615, 2022. 

- [240] Dong Q, Dong L, Xu K, et al. Large Language Model for Science: A Study on P vs. NP[J]. arXiv preprint arXiv:2309.05689, 2023. 

- [241] Zhu X, Li J, Liu Y, et al. A Survey on Model Compression for Large Language Models[J]. arXiv preprint arXiv:2308.07633, 2023. 

- [242] Lake B M, Baroni M. Human-like systematic generalization through a meta-learning neural network[J]. Nature, 2023: 1-7. 

- [243] Fan L, Wang G, Jiang Y, et al. Minedojo: Building open-ended embodied agents with internet-scale knowledge[J]. Advances in neural information processing systems, 2022, 35: 18343-18362. 

- [244] Szot A, Clegg A, Undersander E, et al. Habitat 2.0: Training home assistants to rearrange their habitat[J]. Advances in neural information processing systems, 2021, 34: 251-266. 

- [245] Puig X, Undersander E, Szot A, et al. HABITAT 3.0: A CO-HABITAT FOR HUMANS, AVATARS AND ROBOTS [M]. 2023. 

- [246] Srivastava S, Li C, Lingelbach M, et al. Behavior: Benchmark for everyday household activities in virtual, interactive, and ecological environments[C]//Conference on Robot Learning. PMLR, 2022, 477-490. 

- [247] Li C, Zhang R, Wong J, et al. Behavior-1k: A benchmark for embodied ai with 1,000 everyday activities and realistic simulation[C]//Conference on Robot Learning. PMLR, 2023, 80-93. 

- [248] Shen B, Xia F, Li C, et al. iGibson 1.0: A simulation environment for interactive tasks in large realistic scenes[C]//2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2021, 7520-7527. 

- [249] Kolve E, Mottaghi R, Han W, et al. Ai2-thor: An interactive 3d environment for visual ai[J]. arXiv preprint arXiv:1712.05474, 2017. 

- [250] Chevalier-Boisvert M, Bahdanau D, Lahlou S, et al. Babyai: A platform to study the sample efficiency of grounded language learning[J]. arXiv preprint arXiv:1810.08272, 2018. 

- [251] Murali A, Chen T, Alwala K V, et al. Pyrobot: An open-source robotics framework for research and benchmarking[J]. arXiv preprint arXiv:1906.08236, 2019. 

- [252] Makoviychuk V, Wawrzyniak L, Guo Y, et al. Isaac gym: High performance gpu-based physics simulation for robot learning[J]. arXiv preprint arXiv:2108.10470, 2021. 

- [253] Fu H, Xu W, Ye R, et al. Demonstrating RFUniverse: A Multiphysics Simulation Platform for Embodied AI[J]. 

- [254] Yang M, Du Y, Ghasemipour K, et al. Learning Interactive Real-World Simulators[J]. arXiv preprint arXiv:2310.06114, 2023. 

- [255] Padalkar A, Pooley A, Jain A, et al. Open X- Embodiment: Robotic learning datasets and RT-X models[J]. arXiv preprint arXiv:2310.08864, 2023. 

- [256] Wang X, Kwon T, Rad M, et al. HoloAssist: an Egocentric Human Interaction Dataset for Interactive AI Assistants in the Real World[C]//Proceedings of the IEEE/CVF 

International Conference on Computer Vision. 2023, 20270-20281. 

- [257] Mitash C, Wang F, Lu S, et al. ARMBench: An object-centric benchmark dataset for robotic manipulation[J]. arXiv preprint arXiv:2303.16382, 2023. 

- [258] Mandlekar A, Zhu Y, Garg A, et al. Roboturk: A crowdsourcing platform for robotic skill learning through imitation[C]//Conference on Robot Learning. PMLR, 2018, 879-893. 

- [259] Zhang C, Gao F, Jia B, et al. Raven: A dataset for relational and analogical visual reasoning[C]//Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2019, 5317-5327. 

- [260] Dasari S, Ebert F, Tian S, et al. Robonet: Largescale multi-robot learning[J]. arXiv preprint arXiv:1910.11215, 2019. 

- [261] Downs L, Francis A, Koenig N, et al. Google scanned objects: A high-quality dataset of 3d scanned household items[C]//2022 International Conference on Robotics and Automation (ICRA). IEEE, 2022, 2553-2560. 

- [262] Yu T, Quillen D, He Z, et al. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning[C]//Conference on robot learning. PMLR, 2020, 1094-1100. 

- [263] James S, Ma Z, Arrojo D R, et al. Rlbench: The robot learning benchmark & learning environment[J]. IEEE Robotics and Automation Letters, 2020, 5(2): 3019-3026. 

- [264] Yin J, Li A, Li T, et al. M2dgr: A multi-sensor and multi-scenario slam dataset for ground robots[J]. IEEE Robotics and Automation Letters, 2021, 7(2): 2266-2273. 

- [265] Gao R, Si Z, Chang Y-Y, et al. Objectfolder 2.0: A multisensory object dataset for sim2real transfer[C]//Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2022, 10598-10608. 

- [266] Levine S, Pastor P, Krizhevsky A, et al. Learning hand-eye coordination for robotic grasping with deep learning and large-scale data collection[J]. The International journal of robotics research, 2018, 37(4-5): 421-436. 

- [267] Mahler J, Liang J, Niyaz S, et al. Dex-net 2.0: Deep learning to plan robust grasps with synthetic point clouds and analytic grasp metrics[J]. arXiv preprint arXiv:1703.09312, 2017. 

- [268] Ebert F, Yang Y, Schmeckpeper K, et al. Bridge data: Boosting generalization of robotic skills with crossdomain datasets[J]. arXiv preprint arXiv:2109.13396, 2021. 

- [269] Fang H-S, Fang H, Tang Z, et al. RH20T: A Robotic Dataset for Learning Diverse Skills in One-Shot[J]. arXiv preprint arXiv:2307.00595, 2023. 

- [270] Huang Y, Sun Y. A dataset of daily interactive manipulation[J]. The International journal of robotics research, 2019, 38(8): 879-886. 

- [271] Ruiz-Sarmiento J R, Galindo C, González-Jiménez J. Robot@ home, a robotic dataset for semantic mapping of home environments[J]. The International journal of robotics research, 2017, 36(2): 131-141. 

- [272] Padmakumar A, Thomason J, Shrivastava A, et al. Teach: Task-driven embodied agents that chat[C]//Proceedings of the AAAI Conference on Artificial Intelligence. 2022, 36: 2017-2025. 

- [273] Jing Y, Zhu X, Liu X, et al. Exploring Visual Pretraining for Robot Manipulation: Datasets, Models and Methods[J]. arXiv preprint arXiv:2308.03620, 2023. 

- [274] Yang L, Li K, Zhan X, et al. OakInk: A large-scale knowledge repository for understanding handobject interaction[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2022, 20953-20962. 

- [275] Zeng A, Liu X, Du Z, et al. Glm-130b: An open bilingual pre-trained model[J]. arXiv preprint arXiv:2210.02414, 2022. 

- [276] Raffel C, Shazeer N, Roberts A, et al. Exploring the limits of transfer learning with a unified text-to-text transformer[J]. The Journal of Machine Learning Research, 2020, 21(1): 5485-5551. 

- [277] Brown T, Mann B, Ryder N, et al. Language models are few-shot learners[J]. Advances in neural information processing systems, 2020, 33: 18771901. 

- [278] Thoppilan R, De Freitas D, Hall J, et al. Lamda: Language models for dialog applications[J]. arXiv preprint arXiv:2201.08239, 2022. 

- [279] Touvron H, Lavril T, Izacard G, et al. Llama: Open and efficient foundation language models[J]. arXiv preprint arXiv:2302.13971, 2023. 

- [280] Sun T, Zhang X, He Z, et al. Moss: Training conversational language models from synthetic data[J]. arXiv preprint arXiv:2307.15020, 2023, 7. 

- [281] Team I. Internlm: A multilingual language model with progressively enhanced capabilities [M]. 2023. 

- [282] Yang A, Xiao B, Wang B, et al. Baichuan 2: Open large-scale language models[J]. arXiv preprint arXiv:2309.10305, 2023. 

- [283] Bai J, Bai S, Chu Y, et al. Qwen technical report[J]. arXiv preprint arXiv:2309.16609, 2023. 

- [284] Ren X, Zhou P, Meng X, et al. PanGu-{\Sigma}: Towards Trillion Parameter Language Model with Sparse Heterogeneous Computing[J]. arXiv preprint arXiv:2303.10845, 2023. 

- [285] Li S, Liu H, Bian Z, et al. Colossal-ai: A unified deep learning system for large-scale parallel training[C]//Proceedings of the 52nd International Conference on Parallel Processing. 2023, 766-775. 

- [286] Taori R, Gulrajani I, Zhang T, et al. Stanford alpaca: An instruction-following llama model [M]. 2023. 

- [287] Kirillov A, Mintun E, Ravi N, et al. Segment anything[J]. arXiv preprint arXiv:2304.02643, 2023. 

- [288] Zhang C, Liu L, Cui Y, et al. A Comprehensive Survey on Segment Anything Model for Vision and Beyond[J]. arXiv preprint arXiv:2305.08196, 2023. 

- [289] Oquab M, Darcet T, Moutakanni T, et al. Dinov2: Learning robust visual features without supervision[J]. arXiv preprint arXiv:2304.07193, 2023. 

- [290] Dosovitskiy A, Beyer L, Kolesnikov A, et al. An image is worth 16x16 words: Transformers for image recognition at scale[J]. arXiv preprint arXiv:2010.11929, 2020. 

- [291] Wang L, Huang B, Zhao Z, et al. Videomae v2: Scaling video masked autoencoders with dual masking[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2023, 14549-14560. 

- [292] Scao T L, Fan A, Akiki C, et al. Bloom: A 176bparameter open-access multilingual language model[J]. arXiv preprint arXiv:2211.05100, 2022. 

- [293] Chiang W-L, Li Z, Lin Z, et al. Vicuna: An opensource chatbot impressing gpt-4 with 90%* chatgpt quality[J]. See https://vicuna. lmsys. org (accessed 14 April 2023), 2023. 

- [294] OpenAI. GPT-4 Technical Report[J]. arXiv preprint arXiv:2303.08774v3, 2023. 

- [295] Yang Z, Li L, Lin K, et al. The dawn of lmms: Preliminary explorations with gpt-4v (ision)[J]. arXiv preprint arXiv:2309.17421, 2023. 

- [296] Zheng K, He X, Wang X E. MiniGPT-5: Interleaved Vision-and-Language Generation via Generative Vokens[J]. arXiv preprint arXiv:2310.02239, 2023. 

- [297] Wang S, Sun Y, Xiang Y, et al. Ernie 3.0 titan: Exploring larger-scale knowledge enhanced pretraining for language understanding and generation[J]. arXiv preprint arXiv:2112.12731, 2021. 

- [298] Radford A, Kim J W, Hallacy C, et al. Learning transferable visual models from natural language supervision[C]//International conference on machine learning. PMLR, 2021, 8748-8763. 

- [299] Ramesh A, Pavlov M, Goh G, et al. Zero-shot textto-image generation[C]//International Conference on Machine Learning. PMLR, 2021, 8821-8831. 

- [300] Kim W, Son B, Kim I. Vilt: Vision-and-language transformer without convolution or region supervision[C]//International Conference on Machine Learning. PMLR, 2021, 5583-5594. 

- [301] Wang W, Chen Z, Chen X, et al. Visionllm: Large language model is also an open-ended decoder for vision-centric tasks[J]. arXiv preprint arXiv:2305.11175, 2023. 

- [302] Liu S, Fan L, Johns E, et al. Prismer: A visionlanguage model with an ensemble of experts[J]. arXiv preprint arXiv:2303.02506, 2023. 

- [303] Wang W, Bao H, Dong L, et al. Image as a foreign language: Beit pretraining for all vision and visionlanguage tasks[J]. arXiv preprint arXiv:2208.10442, 2022. 

- [304] Liu H, Li C, Wu Q, et al. Visual instruction tuning[J]. arXiv preprint arXiv:2304.08485, 2023. 

- [305] Zhang Y, Han W, Qin J, et al. Google usm: Scaling automatic speech recognition beyond 100 languages[J]. arXiv preprint arXiv:2303.01037, 2023. 

- [306] Radford A, Kim J W, Xu T, et al. Robust speech recognition via large-scale weak supervision[C]//International Conference on Machine Learning. PMLR, 2023, 28492-28518. 

- [307] Pratap V, Tjandra A, Shi B, et al. Scaling speech technology to 1,000+ languages[J]. arXiv preprint arXiv:2305.13516, 2023. 

- [308] Betker J, Goh G, Jing L, et al. Improving Image Generation with Better Captions [M]. https://cdn.openai.com/papers/dall-e-3.pdf. 2023. 

- [309] Zhang Y, Gong K, Zhang K, et al. Meta-transformer: A unified framework for multimodal learning[J]. arXiv preprint arXiv:2307.10802, 2023. 

- [310] Jiang Y, Gupta A, Zhang Z, et al. Vima: General robot manipulation with multimodal prompts[J]. arXiv preprint arXiv:2210.03094, 2022. 

- [311] Shah D, Osiński B, Levine S. Lm-nav: Robotic navigation with large pre-trained models of language, vision, and action[C]//Conference on Robot Learning. PMLR, 2023, 492-504. 

- [312] Huang W, Wang C, Zhang R, et al. VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models[J]. arXiv preprint arXiv:2307.05973, 2023. 

- [313] Wang G, Xie Y, Jiang Y, et al. Voyager: An openended embodied agent with large language models[J]. arXiv preprint arXiv:2305.16291, 2023. 

- [314] Reed S, Zolna K, Parisotto E, et al. A generalist agent[J]. arXiv preprint arXiv:2205.06175, 2022. 

- [315] Huang S, Jiang Z, Dong H, et al. Instruct2Act: Mapping Multi-modality Instructions to Robotic Actions with Large Language Model[J]. arXiv preprint arXiv:2305.11176, 2023. 

- [316] Yang J, Tan W, Jin C, et al. Pave the Way to Grasp Anything: Transferring Foundation Models for Universal Pick-Place Robots[J]. arXiv preprint arXiv:2306.05716, 2023. 

- [317] Saxena A, Driemeyer J, Ng A Y. Robotic grasping of novel objects using vision[J]. The International journal of robotics research, 2008, 27(2): 157-173. 

- [318] Jiang Y, Moseson S, Saxena A. Efficient grasping from rgbd images: Learning using a new rectangle representation[C]//2011 IEEE International conference on robotics and automation. IEEE, 2011, 3304-3311. 

- [319] Calli B, Walsman A, Singh A, et al. Benchmarking in manipulation research: Using the Yale-CMUBerkeley object and model set[J]. IEEE Robotics & Automation Magazine, 2015, 22(3): 36-52. 

- [320] Pinto L, Gupta A. Supersizing self-supervision: Learning to grasp from 50k tries and 700 robot hours[C]//2016 IEEE international conference on robotics and automation (ICRA). IEEE, 2016, 3406-3413. 

- [321] Mahler J, Matl M, Satish V, et al. Learning ambidextrous robot grasping policies[J]. Science Robotics, 2019, 4(26): eaau4984. 

- [322] Depierre A, Dellandréa E, Chen L. Jacquard: A large scale dataset for robotic grasp detection[C]//2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2018, 3511-3516. 

- [323] Fang H-S, Wang C, Gou M, et al. Graspnet-1billion: A large-scale benchmark for general object grasping[C]//Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2020, 11444-11453. 

- [324] Gao W, Tedrake R. kpam-sc: Generalizable manipulation planning using keypoint affordance and shape completion[C]//2021 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2021, 6527-6533. 

- [325] Liu M, Pan Z, Xu K, et al. Generating grasp poses for a high-dof gripper using neural 

networks[C]//2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2019, 1518-1525. 

- [326] Liu Y, Liu Y, Jiang C, et al. HOI4D: A 4D egocentric dataset for category-level human-object interaction[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2022, 21013-21022. 

- [327] Vuong A D, Vu M N, Le H, et al. Grasp-Anything: Large-scale Grasp Dataset from Foundation Models[J]. arXiv preprint arXiv:2309.09818, 2023. 

- [328] Huang H, Shen Y, Sun J, et al. NavigationNet: A large-scale interactive indoor navigation dataset[J]. arXiv preprint arXiv:1808.08374, 2018. 

- [329] Kirsanov P, Gaskarov A, Konokhov F, et al. DISCOMAN: Dataset of Indoor SCenes for Odometry[J]. Mapping And Navigation, 2019. 

- [330] Wang H, Liang W, Gool L V, et al. Towards versatile embodied navigation[J]. Advances in neural information processing systems, 2022, 35: 36858-36874. 

- [331] Karnan H, Nair A, Xiao X, et al. Socially compliant navigation dataset (scand): A large-scale dataset of demonstrations for social navigation[J]. IEEE Robotics and Automation Letters, 2022, 7(4): 11807-11814. 

- [332] Nguyen D M, Nazeri M, Payandeh A, et al. Toward Human-Like Social Robot Navigation: A LargeScale, Multi-Modal, Social Human Navigation Dataset[J]. arXiv preprint arXiv:2303.14880, 2023. 

- [333] Guhur P-L, Tapaswi M, Chen S, et al. Airbert: Indomain pretraining for vision-and-language navigation[C]//Proceedings of the IEEE/CVF International Conference on Computer Vision. 2021, 1634-1643. 

- [334] Goyal A, Deng J. Packit: A virtual environment for geometric planning[C]//International Conference on Machine Learning. PMLR, 2020, 3700-3710. 

- [335] Li H, Su J, Chen Y, et al. SheetCopilot: Bringing Software Productivity to the Next Level through Large Language Models[J]. arXiv preprint arXiv:2305.19308, 2023. 

- [336] Šegota S B, Anđelić N, Mrzljak V, et al. Utilization of multilayer perceptron for determining the inverse kinematics of an industrial robotic manipulator[J]. International Journal of Advanced Robotic Systems, 2021, 18(4): 1729881420925283. 

- [337] Kuehne H, Jhuang H, Garrote E, et al. HMDB: a large video database for human motion recognition[C]//2011 International conference on computer vision. IEEE, 2011, 2556-2563. 

- [338] Soomro K, Zamir A R, Shah M. UCF101: A dataset of 101 human actions classes from videos in the wild[J]. arXiv preprint arXiv:1212.0402, 2012. 

- [339] Mees O, Hermann L, Rosete-Beas E, et al. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks[J]. IEEE Robotics and Automation Letters, 2022, 7(3): 7327-7334. 

- [340] Ben-Shabat Y, Yu X, Saleh F, et al. The ikea asm dataset: Understanding people assembling furniture through actions, objects and pose[C]//Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision. 2021, 847-859. 

- [341] Damen D, Doughty H, Farinella G M, et al. Scaling egocentric vision: The epic-kitchens dataset[C]//Proceedings of the European conference on computer vision (ECCV). 2018, 720736. 

- [342] Tenorth M, Bandouch J, Beetz M. The TUM kitchen data set of everyday manipulation activities for motion tracking and action recognition[C]//2009 IEEE 12th International Conference on Computer Vision Workshops, ICCV Workshops. IEEE, 2009, 1089-1096. 

- [343] Rohrbach M, Amin S, Andriluka M, et al. A database for fine grained activity detection of cooking activities[C]//2012 IEEE conference on computer vision and pattern recognition. IEEE, 2012, 1194-1201. 

- [344] Tang Y, Ding D, Rao Y, et al. Coin: A large-scale dataset for comprehensive instructional video analysis[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2019, 1207-1216. 

- [345] Zhou L, Xu C, Corso J. Towards automatic learning of procedures from web instructional videos[C]//Proceedings of the AAAI Conference on Artificial Intelligence. 2018, 32. 

- [346] De la Torre F, Hodgins J, Bargteil A, et al. Guide to the carnegie mellon university multimodal activity (cmu-mmac) database[J]. 2009. 

- [347] Kong Q, Wu Z, Deng Z, et al. Mmact: A large-scale dataset for cross modal human action understanding[C]//Proceedings of the IEEE/CVF International Conference on Computer Vision. 2019, 8658-8667. 

- [348] Yan Z, Schreiberhuber S, Halmetschlager G, et al. Robot perception of static and dynamic objects with an autonomous floor scrubber[J]. Intelligent Service Robotics, 2020, 13(3): 403-417. 

- [349] Weihs L, Yuile A, Baillargeon R, et al. Benchmarking progress to infant-Level physical reasoning in AI[J]. Transactions on Machine Learning Research, 2022. 

- [350] Lourie N, Le Bras R, Bhagavatula C, et al. Unicorn on rainbow: A universal commonsense reasoning 

- model on a new multitask benchmark[C]//Proceedings of the AAAI Conference on Artificial Intelligence. 2021, 35: 13480-13488. 

- [351] Shu T, Bhandwaldar A, Gan C, et al. Agent: A benchmark for core psychological reasoning[C]//International Conference on Machine Learning. PMLR, 2021, 9614-9625. 

- [352] Levesque H, Davis E, Morgenstern L. The winograd schema challenge[C]//Thirteenth international conference on the principles of knowledge representation and reasoning. 2012. 

- [353] Zellers R, Bisk Y, Schwartz R, et al. Swag: A largescale adversarial dataset for grounded commonsense inference[J]. arXiv preprint arXiv:1808.05326, 2018. 

- [354] Johnson J, Hariharan B, Van Der Maaten L, et al. Clevr: A diagnostic dataset for compositional language and elementary visual reasoning[C]//Proceedings of the IEEE conference on computer vision and pattern recognition. 2017, 2901-2910. 

- [355] Dua D, Wang Y, Dasigi P, et al. DROP: A reading comprehension benchmark requiring discrete reasoning over paragraphs[J]. arXiv preprint arXiv:1903.00161, 2019. 

- [356] Rajpurkar P, Jia R, Liang P. Know what you don't know: Unanswerable questions for SQuAD[J]. arXiv preprint arXiv:1806.03822, 2018. 

- [357] Clark P, Cowhey I, Etzioni O, et al. Think you have solved question answering? try arc, the ai2 reasoning challenge[J]. arXiv preprint arXiv:1803.05457, 2018. 

- [358] Zellers R, Holtzman A, Bisk Y, et al. Hellaswag: Can a machine really finish your sentence?[J]. arXiv preprint arXiv:1905.07830, 2019. 

- [359] Choi E, He H, Iyyer M, et al. QuAC: Question answering in context[J]. arXiv preprint arXiv:1808.07036, 2018. 

- [360] Mihaylov T, Clark P, Khot T, et al. Can a suit of armor conduct electricity? a new dataset for open book question answering[J]. arXiv preprint arXiv:1809.02789, 2018. 

# **Appendix** 

<u>Table 1. Simulation Framework</u> 

||Mine<br>Dojo<br>[243]|Habi<br>tat<br>2.0<sup>[2</sup><br>44]|Habi<br>tat3.<br>0<sup>[245]</sup>|BEH<br>AVIO<br>R-<br>100<sup>[246</sup><br>]|BEH<br>AVIO<br>R-<br>1K<sup>[247]</sup>|iGibson<br>1.0<sup>[248]</sup>|AI2-<br>THO<br>R<br>2.0<sup>[24</sup><br>9]|BabyAI<br>[250]|PyBulle<br>t|PyR<br>obot<sup>[</sup><br>251]|Isaac<br>Sim<sup>[25</sup><br>2]|RFUn<br>iverse<br>[253]|Uni<br>sim<sup>[</sup><br>254]|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Simu<br>lator|Mine<br>Dojo|Habi<br>tat<br>Sim|Habi<br>tat<br>Sim|iGibso<br>n 2.0|OMNI<br>GIBS<br>ON|iGibson|AI2-<br>THO<br>R 2.0|MiniGr<br>id|PyBulle<br>t|Gaze<br>bo|Omni<br>verse|RFUn<br>iverse|Uni<br>sim|
|Datas<br>et|Mine<br>Dojo|Repl<br>icaC<br>AD|Habi<br>tat<br>Synt<br>hetic<br>Scen<br>es|Huma<br>n VR<br>demos|BEH<br>AVIO<br>R-1K|iGibson<br>dataset|iTHO<br>R,<br>Robo<br>THO<br>R,<br>Proc|||||||


||||Data<br>set||||THO<br>R-<br>10K,<br>Archi<br>tecT<br>HOR|||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Sens<br>ors/S<br>ensor<br>Signa<br>ls|Vide<br>o|RGB<br>-D<br>Cam<br>eras,<br>Joint<br>-<br>posit<br>ion<br>sens<br>ors,<br>Ego<br>moti<br>on<br>sens<br>ors|RGB<br>-D<br>Cam<br>eras,<br>GPS|On-<br>board<br>virtual<br>sensor<br>s<br>(RGB,<br>Depth<br>image<br>s,<br>LiDA<br>R,<br>Norm<br>als,<br>Flow<br>(Optic<br>al,<br>Spatia<br>l), and<br>Sema<br>ntic<br>and<br>instan<br>ce<br>segme<br>ntatio<br>|On-<br>board<br>virtual<br>sensor<br>s<br>(RGB,<br>Depth<br>image<br>s,<br>LiDA<br>R)|RGB<br>images,<br>Renderi<br>ng<br>of<br>normals<br>,<br>Depth,<br>Point<br>clouds,<br>Virtual<br>LiDAR<br>signals,<br>and<br>Optical<br>scene<br>flow|<br>Came<br>ras<br>and<br>the<br>envir<br>onme<br>nt<br>meta<br>data|||Cam<br>era,<br>Dist<br>ance<br>,<br>Prox<br>imit<br>y<br>sens<br>ors,<br>Lase<br>r,<br>force<br>sens<br>ors|RGB-<br>D,<br>Lidar,<br>and<br>IMU|Visio<br>n, IR,<br>DIGT|Ca<br>mer<br>as,<br>LiD<br>AR|
|Lang<br>uage|JAV<br>A,<br>Pyth<br>on|C++,<br>Pyth<br>on|C++,<br>Pyth<br>on|n)<br>Pytho<br>n|Pytho<br>n|Python,<br>C|C#,<br>Pytho<br>n|Python|Python|C++,<br>Pyth<br>on|Pytho<br>n|C#||
|Supp<br>orted<br>OS|<br>Linu<br>x/Ma<br>c<br>OS/<br>Win<br>dows|Linu<br>x/M<br>ac<br>OS/<br>Win<br>dow<br>|Linu<br>x/Ma<br>c<br>OS/<br>Win<br>dows|Windo<br>ws/Ub<br>untu|Windo<br>ws/Ub<br>untu|Windo<br>ws/Lin<br>ux/Mac|Mac<br>OS,<br>Ubun<br>tu|Windo<br>ws/Lin<br>ux/Mac|Windo<br>ws/Lin<br>ux/Mac<br>OS|GN<br>U/Li<br>nux<br>(Ubu<br>ntu)|Wind<br>ows/<br>Linux|Wind<br>ows/<br>Linux||
|Supp<br>orted<br>Task|Mine<br>craft<br>Gam<br>e|s<br>Navi<br>gatio<br>n,<br>Man<br>ipula<br>tion|Navi<br>gatio<br>n,<br>Mani<br>pulat<br>ion|Navig<br>ation,<br>Manip<br>ulatio<br>n|House<br>hold<br>Activi<br>ties|Navigat<br>ion,<br>Manipu<br>lation|Navi<br>gatio<br>n,<br>Mani<br>pulati<br>on|Navigat<br>ion,<br>Manipu<br>lation|Manipu<br>lation,<br>Locom<br>otion,<br>Control|Navi<br>gatio<br>n,<br>Man<br>ipula<br>tion|Navig<br>ation,<br>Mani<br>pulati<br>on|Comp<br>lex<br>Dyna<br>mics<br>Tasks|Self<br>-<br>Dri<br>vin<br>g|
|Open<br>Sourc<br>|Ope<br>n|<br>Ope<br>n|<br>Ope<br>n|Open|Open|Open|<br>Open|Open|Open|<br>Ope<br>n|No|Open|No|
|e<br>Back<br>end|Pyto<br>rch|||||||Pytorch||||||
|<br>Scen<br>||105|211|15|50|15|120|19|9||||103|
|es<br>Obje<br>cts||92|18k|391|5000+|570|84|||||||
|<br>Agen<br>t/Wor<br>ld<br>Intera<br>ction||||Mass,<br>Center<br>of<br>Mass,||Force||||||||


|||||Frictio<br>n||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Envir<br>onme<br>nt|3D|3D|3D|<br>3D|3D|3D|3D|2D<br>Gridwo<br>rld||3D|3D|3D|3D|
|Physi<br>cs<br>Engi<br>ne|Mine<br>craft<br>gam<br>e|Bull<br>et|Bull<br>et|PyBul<br>let|PhysX<br>5|PyBulle<br>t|Unity||Bullet<br>Physics<br>SDK|ODE<br>,<br>Bull<br>et,<br>Sim<br>body<br>,<br>DA<br>RT|Phys<br>X|Unity||
|3D<br>Rend<br>ering<br>Engi<br>ne|Mine<br>craft<br>gam<br>e|Mag<br>num|Mag<br>num|Physic<br>s-<br>Based<br>Rende<br>ring|Nvidi<br>a<br>Omni<br>verse|Physics<br>-Based<br>Renderi<br>ng|Unity||OpenG<br>L|<br>OG<br>RE|RTX|Unity||
|Spee<br>d||1400<br>steps<br>/s|140-<br>250<br>steps<br>/s|||100<br>steps/s|90-<br>180<br>steps/<br>s||Each<br>time<br>step in<br>PyBulle<br>t<br>is<br>1/240<br>seconds|||||
|Robo<br>t<br>Famil<br>y||Artic<br>ulate<br>d<br>Rob<br>ots|Spot<br>Rob<br>ot|A<br>Biman<br>ual<br>Huma<br>noid<br>Avatar<br>,<br>A<br>Fetch<br>Robot||Articul<br>ated<br>Robots,<br>Fetch<br>Robot|||R2d2<br>Robot|Mob<br>ile,<br>Hum<br>anoi<br>d,<br>Indu<br>strial|A<br>Whee<br>led<br>Robot<br>and A<br>Frank<br>,<br>a<br>Emik,<br>a<br>Robot<br>ic|||
||||||||||||Arm|||
|Supp<br>orted<br>Tools||Grip<br>pers,<br>Arm<br>Man<br>ipula<br>tor||||Gripper<br>s,<br>Locobo<br>t||||Grip<br>pers|Mani<br>pulat<br>ors|||
|Com<br>putin<br>g<br>Reso<br>urce|8×<br>V10<br>0<br>GPU<br>s|8GP<br>U||||||20~50G<br>PU|A high-<br>end<br>desktop<br>GPU|||||


<u>Table 2. Comprehensive Robot Datasets</u> 

||Data Type|Objects|Scenes|Data Volume|Task|Skills|
|---|---|---|---|---|---|---|
|Open X-Embodiment<sup>[255]</sup>|Demonstrations|||4435.41GB|Manipulation|527|
|HoloAssist<sup>[256]</sup>|RGB, depth, head<br>pose,<br>3D<br>hand<br>pose, eye gaze,<br>audio, and IMU,<br>text|||166h|Collaboratively<br>manipulation|20|
|UniMoCap|Text-motion<br>mocap|||34K<br>motions<br>and<br>66K<br>annotations|Describing the actions<br>being<br>performed<br>in<br>mocap sequences||


|ARMBench<sup>[257]</sup>|Images and videos|190K|1|235K|Object<br>segmentation,<br>Object Identification, and<br>Defect Detection||
|---|---|---|---|---|---|---|
|RT-1<sup>[62]</sup>|Instruction<br>and<br>image<br>tokenization||3|130K|<br>Manipulation|744|
|RoboTurk<sup>[258]</sup>|Demonstrations||2|137h|Block Lifting (lifting),<br>Bin Picking (picking),<br>and Nut-andpeg<br>Assembly (assembly)||
|Raven<sup>[259]</sup>|Images and RPM|||1120000<br>images<br>and<br>70000 RPM|<br>Reasoning, VQA||
|RoboNet<sup>[260]</sup>|Video frames||4|15<br>million<br>video frames|Manipulation||
|GSO<sup>[261]</sup>|3D images|1030||13G|Manipulation, Navigation<br>and so on||
|Meta-world<sup>[262]</sup>|Video, trajectory||50||Manipulation|50|
|RLBench<sup>[263]</sup>|<br>RGB, depth, and<br>segmentation<br>masks||||<br>Manipulation|100|
|M2DGR<sup>[264]</sup>|RGB image, 3D<br>point<br>cloud,<br>inertial<br>data,<br>GNSS signals|||36<br>sequences<br>(about 1TB)|SLAM||
|OBJECTFOLDER 2.0<sup>[265]</sup>|<br>Object<br>files<br>(containing<br>the<br>complete<br>multisensory<br>profile)|1000||1000<br>object<br>files|Object scale estimation,<br>Contact localization, and<br>Shape reconstruction||
|Google<br>Brain<br>Robot<br>Data<sup>[266]</sup>|<br>Images|||~800k<br>grasp<br>attempts|Manipulation||
|Dex-Net 2.0<sup>[267]</sup>|Point cloud|1500||<br>6.7<br>million<br>point clouds|Manipulation||
|Bridge Data<sup>[268]</sup>|Demonstrations<br>(video)||10|<br>7200<br>demonstrations|Household kitchen tasks|71|
|RH20T<sup>[269]</sup>|<br>RGB<br>image,<br>Depth<br>image,<br>Binocular<br>IR<br>images,<br>Robot<br>joint angle, Robot<br>joint<br>torque,<br>Gripper Cartesian<br>pose,<br>Gripper<br>width,<br>6-DoF<br>Force/Torque,<br>Fingertip tactile|||~110K|Learning task and<br>motion planning|147|
|Radish|<br>Odometry, laser<br>and sonar data,<br>sensor data,<br>Environment<br>maps|||Multi datasets<br>(Usc<br>Sal200<br>Synthetic,<br>Robonaut<br>Sensor)|Robotics<br>dataset<br>community||
|Daily<br>Interactive<br>Manipulation<sup>[270]</sup>|<br>Position,<br>orientation, force,<br>and<br>torque<br>of<br>objects|||<br>3354 trails|Manipulation|33|
|Robot @ Home<sup>[271]</sup>|Intensity images,<br>depth images, and<br>3D point clouds|||9.6G|Object/room instance<br>recognition, object<br>segmentation, data||


||,<br>laser<br>scanner<br>data,<br>topological<br>information||||compression/transmission|
|---|---|---|---|---|---|
|TEACh<sup>[272]</sup>|Language|||3047 sessions|Navigation, Dialogue|
|Robotic<br>3D<br>Scan<br>Repository|3D point clouds|||Multi datasets<br>(FHG Campus,<br>FireAcademy)|SLAM (navigation)|
|MRPT|Sensors from 2D<br>laser scanners up<br>to<br>RTK<br>GPS,<br>stereo cameras or<br>3D ToF cameras|||Multi datasets<br>(Kenmore,<br>Edmonton<br>2002)|Mobile<br>robotics<br>and<br>computer vision|
|ImageNet<sup>[273]</sup>|Image|||1.4<br>million+<br>images|Computer vision|
|EgoNet<sup>[273]</sup>|Image||100+|1.5<br>million<br>video frames|Manipulation|
|OakInk-Image<sup>[274]</sup>|Image|100||230K<br>image<br>frames|Hand Mesh Recovery and<br>Hand-Object<br>Pose<br>Estimation|
|OakInk-Shape<sup>[274]</sup>|Obj models|||62K<br>hand-<br>object<br>poses<br>and models|Grasp Generation, Intent-<br>based<br>Interaction<br>Generation,<br>and<br>Handover Generation|
|HANDAL<sup>[48]</sup>|Image frames|210||306K<br>image<br>frames|Manipulation|
|ScanScribe<sup>[201]</sup>|3D scan and text|56.1k|1,185|2995 RGB-D<br>scans|3D<br>vision-language<br>grounding|
|Sound-Action-Vision<br>Dataset<sup>[105]</sup>|Sound,<br>RGBD,<br>tracking location|60||15000<br>interactions|Interplay of action and<br>sound|


<u>Table 3. Foundation Models</u> 

||Foundational<br>Model|Data<br>Type|Data<br>Size|Parameters<br>Scale|Tokens<br>Scale|Open<br>Source<br>|Training<br>Time|GPU<br>Numbers|Publisher|
|---|---|---|---|---|---|---|---|---|---|
|Language<br>Models|ChatGLM<sup>[275]</sup>|Text|1.2T<br>Engli<br>sh,<br>1.25T<br>Chine<br>se<br>(130<br>B)|6B-130B|400B-<br>1T|ü|60 days|96 DGX-<br>A100<br>GPU<br>(8×40G)|Tsinghua|
||T5<sup>[276]</sup>|Text||60M-11B|1T|ü|||Google|
||GPT3<sup>[277]</sup>|Text||175B|300B|û|||OpenAI|
||LaMDA<sup>[278]</sup>|Text|1.56T<br>words|2B-137B|2.81T|û|57.7 days|1024<br>TPU-v3<br>chips|Google|
||LLaMA<sup>[279]</sup>|Text|4.7T|7B-65B|1.4T|ü|21 days|2048<br>A100<br>GPU|Meta|
||MOSS<sup>[280]</sup>|Text|700B<br>words|16B||ü|||Fudan<br>Universit<br>y|
||InternLM<sup>[281]</sup>|Text|1.6T|7B,<br>20B,<br>104B|1.6T|ü|||Shanghai<br>AI<br>Laborato<br>ry,<br>SenseTi<br>me|


||Baichuan 2<sup>[282]</sup>|Text|127M<br>vocab<br>size|7B, 13B|2.6T|ü||8<br>A800<br>GPUs|Baichuan<br>Inc.|
|---|---|---|---|---|---|---|---|---|---|
||Qwen<sup>[283]</sup><br>|Text<br>|3T<br>|7B, 14B<br>|3T|ü<br>|||Alibaba<br>|
||OpenChatKit|Text|43M<br>instru<br>ctions|20B||ü|||Eleuther<br>AI|
||PANGU-Σ<sup>[284]</sup>|Text|2158<br>GB|1.085T|329B|û|100 days|512<br>Ascend<br>910<br>NPUs|Huawei|
||ColossalChat<sup>[2</sup><br>85]|Text|104K<br>Chine<br>se and<br>Engli<br>sh.|7B|54M|ü||8 A100-<br>40G<br>GPUs|UC<br>Berkeley|
||Alpaca<sup>[286]</sup>|Text|<br>52K<br>instru<br>ctions|7B||ü|3 hours|8 80GB<br>A100s|Stanford<br>Universit<br>y|
|Vision<br>Models|SAM<sup>[287, 288]</sup>|Imag<br>e|<br>11M<br>image<br>s,<br>1.1B<br>mask<br>|91M-<br>636M||ü|68 hours|256<br>GPUs|<br>Meta|
||DINOv2<sup>[289]</sup>|Imag<br>e|s<br>1.2B<br>image<br>s|~1B||ü|2 days|8 V100-<br>32GB<br>GPUs|Meta|
||ViT<sup>[290]</sup>|Imag<br>e|317M<br>image<br>s|86M||ü|||Google|
||VideoMAE<br>V2<sup>[291]</sup>|Video|<br>1.35<br>M<br>clips|1B||ü|14 days|64 A100<br>GPUs|Nanjing<br>Universit<br>y|
|Multilingual<br>Models|BLOOM<sup>[292]</sup>|Text|<br>341B<br>token<br>s<br>of<br>text|176B|366B|ü|3.5<br>months|48 nodes<br>with<br>8<br>NVIDIA<br>A100<br>80GB<br>GPUs|<br>Google|
||Vicuna<sup>[293]</sup>|Text|70K<br>sampl<br>es|13B||ü|1 day|8<br>A100<br>GPUs|UC<br>Berkeley,<br>etc.|
||Claude|||||û|||Anthropi<br>c|
|Multimodal<br>Models|GPT-4<sup>[294]</sup>|Text,<br>Imag<br>||175B|13000B|û|||<br>OpenAI|
||GPT-4V<sup>[295]</sup>|e<br>Text,<br>Imag<br>e||||û|||OpenAI|
||MiniGPT-5<sup>[296]</sup>|<br>Text,<br>Imag<br>e||7B||ü||4 A6000<br>GPUs|Universit<br>y<br>of<br>Californi<br>a, Santa<br>Cruz|
||ERNIE Bot<sup>[297]</sup>|Text,<br>Imag<br>e|4TB<br>Chine<br>se<br>text<br>corpo<br>ra|100B-<br>260B||û|||<br>Baidu|


|CLIP<sup>[298]</sup>|Text,<br>Imag<br>e|400M<br>(imag<br>e,<br>text)<br>pairs|~1.6B|ü|||OpenAI|
|---|---|---|---|---|---|---|---|
|DALL-E<sup>[299]</sup>|Text,<br>Imag<br>e|<br>250M<br>text-<br>image<br>s|12B|ü|||OpenAI|
|ViLT<sup>[300]</sup>|Text,<br>Imag<br>e|<br>4M<br>image<br>s and<br>9.8M<br>captio<br>ns|87.4M|ü||64<br>NVIDIA<br>V100<br>GPUs|NAVER<br>AI Lab|
|VisionLLM<sup>[301</sup><br>]|Text,<br>Imag<br>e|<br>238K<br>image<br>s|7B|ü||4<br>×<br>8<br>NVIDIA<br>A100|Shanghai<br>AI<br>Laborato<br>ry|
|Prismer<sup>[302]</sup>|Text,<br>Imag<br>e|11M<br>image<br>s,<br>12.7<br>M(im<br>ages,<br>text)|275M-<br>1.6B|ü|||<br>Imp<br>erial<br>College<br>London,<br>|
||||||||etc.|
|BEiT-3<sup>[303]</sup>|Text,<br>Imag<br>e|15M<br>image<br>s and<br>21M<br>image<br>-text<br>airs|1.9B|ü|||Microsof<br>t|
|LLaVA<sup>[304]</sup>|Text,<br>Imag<br>e|p<br>∼80K<br>image<br>s|13B|ü|||Universit<br>y<br>of<br>Wisconsi<br>n–<br>Madison|
|USM<sup>[305]</sup>|Text,<br>Audi<br>o|12M<br>hours<br>of<br>speec<br>h,<br>28B<br>sente<br>nces<br>of<br>tt|2B|û|||Google|
|AudioPaLM<sup>[10</sup><br>1]|Text,<br>Audi<br>|ex|600M, 2B|û|||Google|
|Whisper<sup>[306]</sup>|o<br>Text,<br>Audi<br>o|680,0<br>00<br>hours<br>of<br>audio|39M-<br>1550M|ü|||OpenAI|
|MMS<sup>[307]</sup>|Text,<br>Audi<br>o|<br>107.4<br>h|0.3B, 1B|ü|2.3h(0.3<br>B)<br>or<br>3.5h(1B)|48(0.3B)<br>or 64(1B)<br>A100<br>GPU|Meta|


||DALL·E3<sup>[308]</sup>|Text,<br>Imag<br>e|1B<br>image<br>s|||û|||OpenAI|
|---|---|---|---|---|---|---|---|---|---|
||Meta-<br>transformer<sup>[309</sup><br>]|<br>12<br>Types<br>(Text,<br>Imag<br>es,<br>Point<br>Clou<br>ds,<br>Audi<br>o,<br>Video<br>etc.)|<br>Total<br>~<br>449M|85M,<br>302M||ü|||Chinese<br>Universit<br>y<br>of<br>Hong<br>Kong,<br>etc.|
|Embodied<br>Agents|Palm-E<sup>[189]</sup>|,<br>Text,<br>Imag<br>e||12B, 84B,<br>562B||û|||Google|
||VIMA<sup>[310]</sup>|<br>Text,<br>Imag<br>e,<br>Video|650K<br>trajec<br>tories|2M-200M||ü|1 days|8<br>NVIDIA<br>V100<br>GPUs|Stanford<br>Universit<br>y|
||RT-2<sup>[102]</sup>|Text,<br>Imag<br>e,<br>Actio<br>n|10B<br>image<br>-text<br>pairs|5B, 55B||û|||Google<br>DeepMin<br>d|
||RT-X<sup>[255]</sup>|<br>Text,<br>Imag<br>e,<br>Actio<br>||35M, 5B,<br>55B||ü|||Google<br>DeepMin<br>d|
||LM-Nav<sup>[311]</sup>|n<br>Text,<br>Imag<br>e,<br>Actio<br>n||(Based on<br>GPT3,<br>ViNG,<br>CLIP)||ü|||UC<br>Berkeley|
||VoxPoser<sup>[312]</sup>|<br>Text,<br>Imag<br>e||(Based on<br>GPT4)||ü|||Stanford<br>Universit<br>y|
||VOYAGER<sup>[313</sup><br>]|<br>Text,<br>Imag<br>e||(Based on<br>GPT4)||ü|||<br>NVIDIA|
||DIAL<sup>[69]</sup>|<br>Text,<br>Imag<br>e|80k<br>trajec<br>tories|(Based on<br>CLIP)||û|||Google|
||Gato<sup>[314]</sup>|Text,<br>Imag<br>e, etc.|63M<br>Episo<br>des|1.2B|1.5T|û|||DeepMin<br>d|
||RoboCat<sup>[162]</sup>|<br>Text,<br>Imag<br>e, etc.||1.2B||ü|||DeepMin<br>d|
||MOMA-<br>Force<sup>[99]</sup>|Visio<br>n,<br>Force||||û|||ByteDan<br>ce|
||Co-LLM-<br>Agents<sup>[154]</sup>|Text||(Based on<br>GPT4)||ü|||Universit<br>y<br>of<br>Massach<br>usetts<br>Amherst|


|CLIPORT<sup>[71]</sup>|Text,<br>Imag<br>e|200K<br>iterati<br>ons|(Based on<br>CLIP)|ü|1 day|6<br>GPU|UW&NV<br>IDIA|
|---|---|---|---|---|---|---|---|
|Instruct2Act<sup>[31</sup><br>5]|Text,<br>Imag<br>e||(Based on<br>SAM and<br>CLIP)|ü|||Shanghai<br>Jiao Tong<br>Universit<br>y|


<u>Table 4. Manipulation Datasets</u> 

||Objects|Scene|RGB-D<br>Images|Depth<br>Images|3D<br>point<br>cloud<br>s|Size|Num<br>of<br>grasp|6<br>Do<br>F|Multi<br>-cam|Real<br>Image|Shape<br>comp<br>letion|Human<br>oid<br>gripper|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|DailyGras<br>p<sup>[316]</sup>|26||26005|26005||26K<br>mot<br>ion<br>step<br>s||7Do<br>F|ü|ü||û|
|Standford<br>Grasping<sup>[31</sup><br>7]|10||13747|13747||||ü|||||
|Cornell<br>Grasping<sup>[31</sup><br>8]|240||885|885||720<br>0<br>gras<br>ps||ü||ü||û|
|YCB<br>Benchmar<br>ks<sup>[319]</sup>|77||46200|46200|ü|||ü|ü|ü||û|
|CMU<br>dataset<sup>[320]</sup>|150+||50567|||Abo<br>ut<br>1G|50K|7Do<br>F|ü|ü||û|
|Google<br>grasping<br>dataset<sup>[266]</sup>|||800000|||650<br>K||7Do<br>F|ü|ü||û|
|Dex-Net<br>4.0<sup>[321]</sup>|25||5M|5M|ü|103.<br>16G|||û|û||û|
|JACQUA<br>RD<sup>[322]</sup>|11k||54485|108970|||1.1M||û|û||û|
|GraspNet-<br>1Billion<sup>[323</sup><br>]|88|190+|97280|||2.1<br>B|1B+|ü|ü|ü||û|
|kPAM-<br>SC<sup>[324]</sup>|33|125|111k+||ü|111<br>k||7Do<br>F|û|ü|ü|û|
|Min Liu et<br>al.<sup>[325]</sup>|324|||||||25D<br>oF|û|û||ü|
|HOI4D<sup>[326]</sup>|800|610|2.4M|2.4M|ü||||ü|ü||ü|
|DexGrasp<br>Net<sup>[83]</sup>|5355||||||1.32<br>M|||û||ü|
|Grasping-<br>anything<sup>[32</sup><br>7]|∼3M|||1M||1M<br>sam<br>ples|∼600<br>M|||û|||


|||Table 5 Visual Langu|age Navig|ation Datasets||||
|---|---|---|---|---|---|---|---|
||Data type|Size|Scenes|Annotation|Objects|Instructions|Buildings|
|NavigationNet<sup>[328]</sup>|Image|Hundreds of<br>thousands of|15||||Each<br>scene|
|||images|||||with 1-3<br>rooms|


|M2DGR<sup>[264]</sup>|Image, IMU, VI<br>sensor,<br>LiDAR,<br>GNSS|1220.6GB|36|||||
|---|---|---|---|---|---|---|---|
|DISCOMAN<sup>[329]</sup>|Image,<br>depth,<br>IMU, grid|200<br>long<br>sequences||||||
|ALFRED<sup>[138]</sup>|Images,<br>instructions|8055<br>expert<br>demonstration<br>episodes|120|25k||ü||
|VXN<sup>[330]</sup>|Image, text, audio|9.6M<br>episodes|58||21<br>(category)|||
|SCAND<sup>[331]</sup>|Rosbags, LiDAR,<br>Images,<br>Visual<br>Odometry, Wheel<br>odometry|8.7hour/138<br>trajectories||1656||||
|MuSoHu<sup>[332]</sup>|Image,<br>LiDAR,<br>IMU, audio, depth|300<br>trajectories||17 labels||||
|R2R<sup>[139]</sup>|Image, text|7189<br>trajectories|90|||22k||
|BnB<sup>[333]</sup>|Image, text|1.4M|140k|0.7M||||
|REVERIE<sup>[140]</sup>|Image, text|10318<br>panoramas|132||4140|21702|86|


# <u>Table 6 Long Horizon Task Planning Datasets</u> 

|Dataset Name|Description|Data Format|Number<br>of Tasks|Task<br>Descriptions|Task Duration<br>Range|Dataset<br>Size (GB)|
|---|---|---|---|---|---|---|
|TaPA<sup>[143]</sup>|Grounded<br>planning<br>with<br>physical<br>scene<br>constraint|Image, text||Daily tasks||15k<br>instructions|
|RoboCook<sup>[151]</sup>|Complex long-horizon<br>soft body manipulation<br>tasks|Point clouds||Complex<br>long-horizon<br>soft<br>body<br>manipulation<br>tasks||19.73GB|
|RLBench<sup>[263]</sup>|An ambitious large-<br>scale benchmark and<br>learning environment|Image, depth,<br>joint angles,<br>velocities and<br>forces|100|Manipulation<br>tasks|||
|PackIt<sup>[334]</sup>|A<br>dataset<br>of<br>hard<br>packing<br>problems|Point cloud||The geometry<br>of objects and<br>plan<br>actions<br>for<br>manipulating||7.7GB|
|SheetCopilot<sup>[335]</sup>|A<br>dataset<br>as<br>a<br>foundation<br>for<br>assessing<br>the<br>spreadsheet<br>control<br>capabilities|Text|221|Spreadsheet<br>control tasks|||
|Kinetics<sup>[336]</sup>|A dataset for inverse<br>kinematics of robotic<br>manipulators|Coordinates<br>of the robotic<br>manipulator<br>end effector||Inverse<br>kinematics||15k data|
|HMDB<sup>[337]</sup>|A large human motion<br>database|Video||Human action<br>tasks||2GB|
|UCF<sup>[338]</sup>|An action recognition<br>data set of realistic<br>action videos|Video|101|Action<br>recognition<br>tasks||6.5GB|
|CALVIN<sup>[339]</sup>|A benchmark to learn<br>long-horizon language-<br>conditioned tasks|Image, depth,<br>tactile image|34|Language-<br>conditioned<br>continuous<br>control tasks||1.3GB|


|IKEA<br>assembly<br>dataset<sup>[340]</sup>|A<br>multi-modal<br>and<br>multi-view<br>video<br>dataset<br>of<br>assembly<br>tasks|3 RGB views,<br>one<br>depth<br>stream,<br>atomic<br>actions,<br>human poses,<br>object<br>segments,<br>object<br>tracking, and<br>extrinsic<br>camera<br>calibration||Assembly<br>tasks||406GB|
|---|---|---|---|---|---|---|
|Epic-Kitchens<sup>[341]</sup>|A large-scale dataset in<br>first-person<br>(egocentric) vision|Image, audio|700|Daily<br>activities<br>in<br>the kitchen||1.1TB|
|TUM<br>Kitchen<br>DataSet<sup>[342]</sup>|<br>A dataset of everyday<br>manipulation activities<br>for motion tracking and<br>action recognition|Image,<br>motion<br>capture data,<br>RFID<br>tag<br>readings||Action<br>recognition<br>tasks|||
|MPII<br>Cooking<br>Activities<br>Dataset<sup>[343]</sup>|A<br>dataset<br>which<br>distinguishes 65 fine-<br>grained activities|<br>Image, video|65|Cooking<br>activities||141.7GB|
|Coin-Dataset<sup>[344]</sup>|<br>A large-scale dataset for<br>comprehensive<br>instruction<br>video<br>analysis|Video|180|Video<br>analysis tasks|12<br>domains<br>as: nursing &<br>caring,<br>vehicles,<br>leisure<br>&<br>performance,<br>gadgets,<br>electric<br>appliances,<br>household<br>items, science<br>& craft, plants<br>&<br>fruits,<br>snacks<br>&<br>drinks dishes,<br>sports,<br>and<br>housework|476 hours<br>video|
|Youcook2<sup>[345]</sup>|A large task-oriented,<br>instructional<br>video<br>dataset|Video|2000|Cooking<br>tasks||35.1GB|
|Kitchen(CMU)<sup>[346</sup><br>]|A<br>dataset<br>contains<br>multimodal<br>measures<br>of the human activity of<br>subjects performing the<br>tasks<br>involved<br>in<br>cooking<br>and<br>food<br>preparation.|Video, audio,<br>IMU|5|The<br>human<br>activity<br>of<br>subjects<br>performing<br>the<br>tasks<br>involved<br>in<br>cooking and<br>food<br>preparation|||
|MMACT<sup>[347]</sup>|A large-scale dataset for<br>cross modal learning on<br>human<br>action<br>understanding|RGB,<br>Keypoints,<br>Acceleration,<br>Gyroscope,<br>Orientation,<br>Wi-Fi,<br>Pressure|37|<br>3<br>major<br>groups:<br>complex<br>actions,<br>simple action,<br>desk actions||40K+<br>instances|
|FLOBOT<br>Perception<sup>[348]</sup>|A real-world dataset for<br>robotic<br>cleaning<br>in<br>public spaces|<br>Image, depth,<br>LiDAR|3(scenes)|Robotic<br>cleaning tasks||12.5GB|


|Fusion360Gallery|A dataset contains rich|B-Rep,|mesh,|Design tasks|
|---|---|---|---|---|
|Dataset|2D and 3D geometry|and|point||
||data<br>derived<br>from|cloud|||
||parametric<br>CAD<br>models||||


Table 7 Reasoning Datasets 

|Dataset Name|Description|Publisher|Domain/Applicatio<br>n|Data Type|Task Type|Size (Number<br>of Samples)|
|---|---|---|---|---|---|---|
|InfLevel<sup>[349]</sup>|A benchmark<br>designed<br>to<br>evaluate<br>AI<br>systems’<br>understanding<br>of<br>core<br>physical<br>principles|AI2|Evaluate<br>AI<br>systems’<br>understanding<br>of<br>core<br>physical<br>principles|Video|Manipulatio<br>n|80k videos|
|Socratis<sup>[214]</sup>|A benchmark<br>of<br>diverse<br>open-ended<br>emotional<br>reactions<br>to<br>image-caption<br>pairs|Boston<br>University|Predict<br>human<br>emotion at an image<br>and caption pair|Image, text|Reasoning|18,378<br>annotations|
|RoboTurk<sup>[258]</sup>|A<br>crowdsourced<br>teleoperated<br>robot<br>manipulation<br>dataset|Stanford<br>University|Challenging<br>manipulation tasks|Video|Manipulatio<br>n|2144<br>demonstration<br>s|
|Rainbow<sup>[350]</sup>|A<br>universal<br>commonsense<br>reasoning<br>benchmark<br>spanning both<br>social<br>and<br>physical<br>common sense|AI2|Commonsense<br>reasoning tasks|Question-<br>answering|Reasoning||
|PhysObjects<sup>[207</sup><br>]|An<br>object-<br>centric dataset<br>of<br>common<br>household<br>objects|Stanford<br>University<br>etc.|Help<br>VLMs<br>understand<br>the<br>physical<br>concepts<br>(e.g.,<br>material,<br>fragility)<br>of<br>common objects|Image, text|Manipulatio<br>n|39.6K crowd-<br>sourced<br>and<br>417K<br>annotations|
|AGENT<sup>[351]</sup>|A benchmark<br>for<br>core<br>psychological<br>reasoning|MIT etc.|Core psychological<br>reasoning|RGB-D<br>frames,<br>segmentatio<br>n maps, GT<br>states|Reasoning|3360 trials|
|Winograd<br>Schema<br>Challenge<sup>[352]</sup>|A dataset for<br>commonsense|University<br>of Toronto|Commonsense<br>reasoning|Text|Multiple<br>Choice<br>Questions|150 schemas|


||reasoning and<br>AI.||||||
|---|---|---|---|---|---|---|
|SWAG<sup>[353]</sup><br>(Situation With<br>Adversarial<br>Generations)|A dataset for<br>grounded<br>commonsense<br>inference.|University<br>of<br>Washingto<br>n|Commonsense<br>reasoning|Text|Multiple<br>Choice<br>Questions|113k examples|
|CLEVR<br>(Compositional<br>Language and<br>Elementary<br>Visual<br>Reasoning)<sup>[354]</sup>|A dataset for<br>visual<br>reasoning and<br>logic.|Stanford<br>University|Visual reasoning|Images, Text|Multiple<br>Choice<br>Questions|100k images,<br>100k questions|
|DROP<sup>[355]</sup>|A dataset for<br>reading<br>comprehensio<br>n<br>and<br>reasoning.|AI2|Reading<br>comprehension|Text|Question<br>Answering|96k questions|
|SQuAD(The<br>Stanford<br>Question<br>Answering<br>Dataset)<sup>[356]</sup>|A<br>reading<br>comprehensio<br>n dataset|Stanford<br>University|Reading<br>comprehension|Text|Question<br>Answering|150k questions|
|ARC<sup>[357]</sup>(AI2<br>Reasoning<br>Challenge)|A<br>set<br>of<br>science<br>questions that<br>require various<br>forms<br>of<br>reasoning.|AI2|Science reasoning|Text|Multiple<br>Choice<br>Questions|7k questions|
|HellaSwag<sup>[358]</sup>|A<br>dataset<br>designed<br>for<br>commonsense<br>reasoning with<br>unconventiona<br>l questions.|AI2|Commonsense<br>reasoning|Text|Multiple<br>Choice<br>Questions|70k questions|
|QuAC<sup>[359]</sup><br>(Question<br>Answering<br>in<br>Context)|A dataset for<br>reasoning<br>about<br>questions<br>posed<br>in<br>a<br>dialogue<br>context.|University<br>of<br>Washingto<br>n|Dialog-based<br>reasoning|Text|Question<br>Answering|14k dialogues|
|OBQA<sup>[360]</sup><br>(OpenBookQA<br>)|A dataset for<br>open-domain<br>question<br>answering that<br>requires<br>reasoning over<br>a<br>large<br>collection<br>of<br>texts.|AI2<br>and<br>University<br>of<br>Washingto<br>n|Question answering|Text|Multiple<br>Choice<br>Questions|6k questions|


