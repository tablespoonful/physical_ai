---
title: "QUAR-VLA: Vision-Language-Action Model for Quadruped Robots"
date: "2023-12-22"
authors: "Pengxiang Ding; Han Zhao; Wenjie Zhang; Wenxuan Song; Min Zhang; Siteng Huang"
venue: "ECCV 2024"
url: https://arxiv.org/abs/2312.14457
pdf: https://arxiv.org/pdf/2312.14457
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2312.14457)** / [論文ページ](https://arxiv.org/abs/2312.14457)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **QUAR-VLA: Vision-Language-Action Model for Quadruped Robots** 

Pengxiang Ding<sup>12</sup> Han Zhao<sup>12</sup> Wenxuan Song<sup>1</sup> Wenjie Zhang<sup>1</sup> Min Zhang<sup>12</sup> Siteng Huang<sup>12</sup> Ningxi Yang<sup>1</sup> Donglin Wang<sup>1</sup><sup>_⋆_</sup> 

> 1Westlake University 2Zhejiang University `{dingpengxiang,zhaohan34,wangdonglin}@westlake.edu.cn` 

**Abstract.** The important manifestation of robot intelligence is the ability to naturally interact and autonomously make decisions. Traditional quadruped robot learning typically handles language interaction and visual autonomous perception separately, which, while simplifying system design, also limits the synergy between different information streams. This separation poses challenges in achieving seamless autonomous reasoning, decision-making, and action execution. To address these limitations, a novel paradigm, named **V** ision- **L** anguage- **A** ction tasks for **QUA** druped **R** obots ( **QUAR-VLA** ), has been introduced in this paper. This approach tightly integrates visual information and instructions to generate executable actions, effectively merging perception, planning, and decision-making. The central idea is to elevate the overall intelligence of the robot. Within this framework, a notable challenge lies in aligning fine-grained instructions with visual perception information. This emphasizes the complexity involved in ensuring that the robot accurately interprets and acts upon detailed instructions in harmony with its visual observations. Consequently, we propose **QUA** druped **R** obotic **T** ransformer ( **QUART** ), a VLA model to integrate visual information and instructions from diverse modalities as input and generates executable actions for real-world robots and present **QUA** druped **R** obot **D** ataset ( **QUARD** ), a large-scale multi-task dataset including perception, navigation and advanced capability like whole-body manipulation tasks for training **QUART** model. Our extensive evaluation shows that our approach leads to performant robotic policies and enables **QUART** to obtain a range of generalization capabilities. 

**Keywords:** Robotics · Quadruped Robot Learning · Vision-LanguageAction Model 

## **1 Introduction** 

Quadruped robots, characterized by their excellent traversability on complex terrains and agile movements, have garnered significant attention in the field of robotics [14]. Researchers have extensively employed these robots to explore tasks encompassing autonomous navigation and manipulation [16, 17, 36]. 

> _⋆_ Corresponding author 

2 Authors Suppressed Due to Excessive Length 


**Fig. 1: Comparison of QUAR-VA, QUAR-LA, and QUAR-VLA. QUAR-VA** solely utilizes coarse-grained vision information, lacking explicit instructions for handling diverse tasks. In contrast, **QUAR-LA** exclusively relies on language information and lacks of vision information for autonomy. Therefore, **QUART-VLA** combines both vision information and language instructions as inputs, enabling autonomous problem-solving across a range of tasks, revealing distinct input modalities and task capabilities. 

Broadly speaking, the quadruped tasks consist of two major specifications: **V** ision- **A** ction tasks for **QUA** druped **R** obots ( **QUAR-VA** ) and **L** anguage- **A** ction tasks for **QUA** druped **R** obots ( **QUAR-LA** ). As depicted in Fig. 1, in **QUAR-VA** approaches [31], quadruped robots {receive} perception images captured from a first-person perspective and instruction images obtained from a third-person perspective to guide their actions. However, such a task specification often relies on a single (coarse-grained) goal image instruction, making it difficult to apply in many real-world combination tasks, _i.e_ . requiring combining multiple sub-instructions. In contrast, employing language as instructions [36], **QUARLA** formulation allows for executing more fine-grained and diverse tasks, suitable for expressing combinational commands ( _i.e_ . _“before / then"_ ), complex spatial relationships ( _i.e_ . _“move to the left"_ ), and many commonsense command priors ( _i.e_ . _“move fast"_ ). Nevertheless, **QUAR-LA** approaches, which lack the integration of visual modality, hinder the robots’ ability to perceive the environment, thereby impeding their autonomous navigation capabilities [36]. To enable quadruped robots to autonomously navigate and manipulate various tasks, in this paper, we propose a new paradigm: **V** ision- **L** anguage- **A** ction tasks for **QUA** druped **R** obots ( **QUAR-VLA** ), integrating visual information and instructions from diverse modalities as input and generating executable actions for real-world robots. 

This task primarily encompasses two challenges. Firstly, there is a lack of large-scale datasets in the research community for quadruped robots performing diverse tasks. Pretraining models require abundant trajectory data from a variety of tasks. However, collecting substantial amounts of real-world data often necessitates human involvement and significant time investment in manual instruction operations. Secondly, different from navigation tasks [31] for general mobile robots and manipulation tasks for fixed-base systems [7, 9, 12, 34], building a VLA model to solve complex quadruped robot tasks is considerably more challenging due to their agile locomotion behaviors. The action space needs to be 

QUAR-VLA: Vision-Language-Action Model for Quadruped Robots 

3 


**Fig. 2: Overview of QUAR-VLA** . Our tasks encompass a diverse range of perception, navigation, and other advanced capability. The Vision-Language-Action (VLA) model first undergoes training with a huge amount of simulation data (259K episodes) and a small amount of real-world data (3K episodes). In the inference phase, images and texts undergo tokenization, after which **QUART** generates 12-dimensional action tokens. These tokens are subsequently detokenized into valid robot actions and deployed on a physical quadruped robot. This methodology effectively extends the learned capabilities from a simulated environment to real-world applications. 

properly defined to strike a balance between movement flexibility and computational efficiency. The action generated by the model should not be too simplistic, akin to the planner base velocities output by 2-D navigation modules, nor should they require a high execution frequency like the low-level motion policy that directly controls the joint motors. 

To address these two problems, we collect a large-scale multi-task dataset **QUA** druped **R** obot **D** ataset ( **QUARD** ). It includes multiple tasks such as perception, navigation, and advanced capabilities like object avoidance. To the best of our knowledge, this is the first quadruped robot dataset that incorporates a significant amount of vision, language instruction, and robot command data. As collecting data on real robots is expensive and inefficient, we primarily rely on data generated in simulation, which exhibits significant differences in visual, sensor, and system dynamics. We also introduce **QUA** druped **R** obotic **T** ransformer ( **QUART** ), a VLA model for training **QUARD** . **QUART** takes images of the robot’s first-view camera and the natural language instruction as inputs and generates rich control commands that include controlling the robot’s base velocity, posture, and gait parameters. **QUART** leverages a pre-trained large-scale visual language model and fine-tunes it on our dataset to enable the generation of executable commands for quadruped robots. To address the simto-real gap caused by the data disparity, we construct a co-training pipeline to effectively distill the knowledge of simulation data for real-scene deployment. Our extensive evaluation shows that our approach leads to performant robotic policies and enables **QUART** to obtain a range of generalization capabilities. 

Our contributions are as follows: 1) To the best of our knowledge, we first propose a new paradigm: **QUAR-VLA** , integrating visual and language instructions to executable actions for more autonomous and diverse quadruped 

4 Authors Suppressed Due to Excessive Length 

robot tasks. 2) We present a large-scale multi-task dataset, **QUARD** , and a Vision-Language-Action model, **QUART** to solve the **QUAR-VLA** tasks. 3) Our extensive evaluation shows that our approach leads to performant robotic policies and enables **QUART** to obtain a range of generalization capabilities. 

## **2 Related Work** 

**Quadruped Robot Learning.** Previous research [2,4,10,13,16,17,19,26,30,36, 39] has delved into single-model policies. As to vision-based methods ( **QUARVA** ), Kareer _et al_ . [16] utilizes vision perception to predict a privileged terrain map, enabling the robot to perform specific locomotion based on the terrain characteristics. Karnan [17] leverages ego-motion estimates obtained through vision perception, allowing the robot to understand its relative position and direction to avoid collisions and navigate toward a goal location. While some works have succeeded in these tasks through vision perception, relying solely on vision limits the capability to handle only a specific type of task. In response to this limitation, Tang _et al_ . [36] have started exploring language-conditioned tasks ( **QUAR-LA** ). However, the absence of vision perception in their approach results in a lack of autonomy for the robot to interact with its environment. Therefore, this paper proposes a new **QUAR-VLA** paradigm to integrate visual information and instructions to generate executable actions, effectively ensuring that the robot accurately interprets and acts upon detailed instructions in harmony with its visual observations. 

**Vision-language-action models.** Visual-language-action models [1, 5, 20, 24, 28, 33, 35]integrates visual information and instructions to generate executable actions, effectively merging perception, planning, and decision-making and elevating the overall intelligence of the robot. As a result, vision-language-action models have been a popular area of research in robotics. In the realm of visuallanguage-action models, Shridhar _et al_ . [33] have made significant strides by leveraging CLIP to encode text inputs, thereby enhancing the vision model’s semantic comprehension and action execution capabilities. Further advancing the field, Brohan _et al_ . [8] and Li _et al_ . [20] have innovatively applied large language models to craft manipulation policies specifically for robotic applications. This paper delves into the domain of embodied agents, focusing on the quadruped robot as a case study. It explores the challenges and opportunities in enabling quadruped robots to autonomously navigate and perform a variety of tasks as directed by human instructions, contributing to the broader discourse on robotic autonomy and intelligence. 

**Robot Dataset.** The realm of robotic learning has been at the forefront of advancing open-source datasets tailored explicitly for robot learning [6, 15, 17, 32, 36,38,40]. Within the domain of quadrupedal robots, previous works on datasets primarily focused on algorithms and leg controllers. Eckert _et al._ [11] introduced a grading system and an online dataset for the collection and distribution of agility scores. Caluwaerts _et al._ [10] sought to address the lack of a standardized and scalable environment and inductive metrics. Tang _et al._ [36] pioneered the 

QUAR-VLA: Vision-Language-Action Model for Quadruped Robots 5 

generation of desired joint position control using LLM. Nevertheless, common limitations persist among these quadruped robot datasets: the quantity is insufficient and the tasks are limited in diversity. Hence, our data repository aims to complement these endeavors. We curate and process an extensive array of skills on various objects, across diverse scenes in both the real world and virtual environments. The dataset includes image data, robot action data, and point cloud data, providing quadruped robots with rich perceptual information to tackle increasingly intricate and demanding tasks. 

## **3 Method** 

This section provides a detailed exposition of our proposed methodology. Initially, we present the definition of our proposed **QUAR-VLA** in Section 3.1. Following that, Section 3.2 outlines the collecting process of **QUARD** . Lastly, we delve into the overarching architecture of **QUART** in Section 3.3. 

### **3.1 Problem Setup** 

The objective of **QUAR-VLA** is to construct a vision-language-action model learned from large-scale demonstration data and generate actions for closed-loop robot control. 

An overview of our **QUAR-VLA** is shown in Fig. 2. Our goal is to train a conditional policy **QUART** that can interpret RGB image(s), denoted _s ∈ S_ , together with a task instruction _w ∈W_ , which correspond to a language string. The policy is a mapping from images and instructions to actions, and can be written as _µ_ : _S × W →A_ , where the action space _A_ consists of the 11-dimensional high-level commands as well as a terminate signal. 


Here, _vx_ , _vy_ , and _ωz_ represent the velocities along the x-axis, y-axis, and z-axis respectively. _θ_ 1, _θ_ 2, and _θ_ 3 indicate the gait pattern, _f_ denotes the frequency, _hz_ represents the height of the robot, _ϕ_ denotes the pitch angle, _sy_ corresponds to the foot width, _h_<sup>_f_</sup> _z_<sup>representsthefootheight,and</sup><sup>_t_indicatesthetermination</sup> signal of the action. 

Notably, in this study, we employ the discretization method proposed by [9] to discretize all continuous dimensions into 256 uniformly sized bins. This choice of discretization is motivated by the desire to reduce the complexity of action search and improve the stability and convergence of algorithms. 

### **3.2 Large-scale Quadruped Robot Datasets** 

To enable an imitation learning system to generalize to new tasks with zero demonstrations of said task, we must be able to easily collect a diverse dataset, provide corrective feedback, and evaluate many tasks at scale. Therefore, we collect a large-scale multi-task dataset, **QUA** druped **R** obot **D** ataset ( **QUARD** ), 

6 Authors Suppressed Due to Excessive Length 

**Table 1: Tasks Definition.** The "Type" means different capabilities of robots. The "Level" devides the difficulty into 3 levels. The "Skill" means different skill/task categories. The "Episode" signifies the number of experiments conducted for each task, which also corresponds to the number of trajectories. The "Description" is the illustration of the tasks. 

|**Type**|**Level**|**Skill**|**Episode**|**Description**|
|---|---|---|---|---|
|Perception|Easy|Distinguish<br>_Letter_<br>(sim)|10K|Identify the correct one from multiple boxes with differ-<br>ent printed letters|
|Basic|Medium|Go to _Object_ (sim)|72K|Navigate to the object and stop in front of it|
|Navigation|Medium|Go to Object (real)|3K|Navigate to the object and stop in front of it|
||Hard|Go<br>through<br>_Tunnel_<br>(sim)|48K|**Spatial**<br>**Navigation**: Go through the correct tunnel<br>from two tunnels with different colors and shapes|
|Advanced<br>Capability|Hard|Go to _Object_ and avoid<br>the obstacle (sim)|63K|**Obstacle Avoidance**: Navigate to the object without<br>colliding with the obstacle|
||Hard|Crawl under _Bar_ (sim)|1K|**Environment Adaptation**: Crawl under a bar with a<br>low height|
||Hard|Unload _Object_ into _Re-_<br>_ceptacle_ (sim)|52K|**Object Manipulation**: Move with a ball on the back<br>and unload it into a receptacle|
|||Total|259K|The total number of episodes|


**Fig. 3:** The left figure illustrates the trajectory lengths corresponding to different tasks and the right figure illustrates the relationships between tasks. As the difficulty of the skill increases, it can be observed that the average trajectory length gradually increases. The right figure demonstrates the relationship between the types of tasks: perception as foundational capability; basic navigation ability is built on perception; object manipulation, obstacle avoidance, spatial navigation, and environment adaption extend from perception and navigation. 

which includes multiple tasks such as perception, basic navigation, and advanced capability like object manipulation. 

**Task Definition.** As is shown in Table 1, there are seven tasks distributed across three levels of difficulty: easy, medium, and hard. The easy and medium tasks are designed such that the robot can accomplish them using fundamental skills. For instance, the “Go to” task is a basic action integral to all navigation tasks, while the “Distinguish” task serves as the foundational action for all perception tasks. Hard tasks necessitate the robot to execute tasks using more advanced skills. A case in point is the “Unload object” task, which involves the robot distinguishing the target container, navigating to the target position, adjusting body position, and considering potential collisions to successfully unload the object. This process integrates perception, navigation, and whole-body manipulation. The complexity of tasks is reflected in the average trajectory length, with more challenging tasks requiring a greater number of steps and consequently taking 

QUAR-VLA: Vision-Language-Action Model for Quadruped Robots 

7 


**Fig. 4:** Statistic analysis of **QUARD** . 1) Simulation data accounts for a larger proportion compared to real data. 2) Trotting occupied most of the share of gait. 3) Most tasks own similar episodes while Distinguish Letter and Go to Object (in reality) owns much less. 4) 3 types of speed occupied 1/3 separately. 

longer to complete. The specific trajectory lengths and task distribution for each task are detailed in Fig. 4 and Fig. 3. 

**System Setup.** The robot used to collect the trajectory data is WR-2, which is a quadruped robot with 12 joints. WR-2 has around 25cm in standing height and 40cm body length. The command output is sent to the low-level command tracking controller (pre-trained command-conditioned policy in [23]) to generate the actual joint action of the robot. The simulation data was collected in Nvidia’s Isaac Gym [22], a powerful simulator that allows us to collect massive robot trajectories in parallel. The real data was collected by manually manipulating a quadruped robot in the lab setting. The perception data is provided by a RealSense d435 camera installed in the front of the robot. 

**Data Collection.** As to simulation data, A* and D* algorithms are used to plot optimal paths for a dog navigating through various objects and obstacles. The A* algorithm seeks the most cost-effective path, while the D* algorithm adapts to changes in real time. A Proportional-Derivative controller then converts these paths into target velocities for the dog, ensuring smooth movement. The combination of both algorithms provides a flexible and efficient method for path planning in various environments. For real data, The real data set is obtained in a laboratory environment using remote control. 

**Consistency constraints.** To maintain consistency between simulation and reality, we’ve established constraints for data collection. The robot starts at the origin, with the target randomly positioned within [2.7,3.3] meters on the x-axis and [0.9,1.1] meters on the y-axis. In obstacle scenarios, obstacles are placed 1.5 meters from the target’s x-coordinate, with the same y-coordinate. Task termination criteria vary. For "go to object", "go to the object and avoid obstacle", and "crawl under bar" tasks, success is when the robot is less than one meter from the target. Other task success criteria are: 1) “Unload object”: successful when the object is in the target container. 2) “Go through tunnel” and “Crawl under bar”: successful when the robot reaches a specific position behind the tunnel or bar. 3) “Distinguish letter”: successful when the robot correctly orients towards the visual target. 

**More Statistics.** The data collection setup adheres to a predefined language template as depicted in Fig. 4, where the task, target object, speed, and gait 

- 8 Authors Suppressed Due to Excessive Length 


**Fig. 5: Architecture of QUART** . It is designed to leverage the scene comprehension capability of a pretrained MLLM. It receives visual information as observation, and outputs an action representing the actual action taken by the robot based on text-form instructions, and de-tokenizes it into specific action values. **QUART** can generate a complete action sequence at a processing rate of 2Hz in actual scenarios, and hand it over to the underlying low-level strategy for execution. 

are explicitly defined. To enhance diversity and generalization capabilities, the dataset includes a variety of common indoor furniture and outdoor facilities, in addition to basic shapes. The basic shapes come in four color variations: green, red, blue, and yellow. Examples of indoor furniture include bookshelves, ovens, and vases, while outdoor facilities encompass trashcans and benches. Recognizing the distinct nature of motion robots as compared to manipulation robots, we also require robots to perform the same task with varying gaits and speeds to adapt to different instructions and environments. The corresponding ratios of gaits and speeds are presented in Fig. 4. More details about the datasets can be found in the supplementary material. 

### **3.3 Vision-Language-Action Model** 

In comparison to VLA models [7, 9, 12, 31, 34] in other field, our research stands out due to the abundance of kinematics information available in this domain. This allows the robot to not only excel at goal-oriented navigation tasks but also perform a diverse range of whole-body manipulation operations with enhanced flexibility in gaits and body control. Next, we will present our **QUA** druped **R** obotic **T** ransformers **(QUART)** . 

**QUART** relies on a pre-trained vision-language-model [3] to associate tokens from the model’s existing tokenization with the discrete action bins. It is worth noting that training MLLMs to override existing tokens with action tokens is a form of symbol tuning [37], which has been shown to work well in prior work. For [3], integers up to 1000 each have a unique token, so we simply 

QUAR-VLA: Vision-Language-Action Model for Quadruped Robots 9 

associate the action bins with the token representing the corresponding integer. Notably, **QUART** model takes a single image _s_ and a natural language instruction _w_ as input, which are first converted into corresponding tokens _t_ through a tokenizer _τ_ ( _t|s, w_ ) and fed into a decoder-only transformer module to obtain discretized action tokens _p_ ( _ad|t_ ). 

The policy **QUART** could be shown as follow: 


where _w, s_ are the input images and language instruction and _τ_ represents the tokenizer and _p_ indicates the vision-language model to output action _ad_ . **Action Detokenize.** To directly convert models’ output to valid robot actions for downstream control, we need detokenize the discrete action token _ad_ into continuous representation _ac_ (except for the discrete termination command). 


**Loss.** We use a standard categorical cross-entropy objective and causal masking that was utilized in prior Transformer-based controllers [18, 29]. **Inference Speed.** In contrast to many applications of large models, such as natural language or image generation, one of the unique requirements for a model that needs to run on real robots in real-time is fast and consistent inference speed. It is important to highlight that our research specifically emphasizes the command control of quadruped robots. In contrast to low-level motor control, the command control outputs alleviate the strict control frequency requirements, enabling smooth integration of larger models and unlocking improved reasoning capabilities. For **QUART** , the inference time could get 2Hz. More details about the deployment could be found in the supplementary material. 

## **4 Experiments** 

We concentrate our experiments on the multi-task ability, generalization, and sim2real scaling. and try to address the following questions: 1. How effective is the vision-language-action architecture for multi-task quadruped task compared to previous VLM baselines? 2. How well do these models generalize to unseen semantic attributes like object shape, color, and unseen verbal information? 3. How do these simulation data contribute to real-scene performance? More details about the model architecture and training strategy can be found in the supplementary material. 

### **4.1 Implementation Details** 

**Training Details.** We train a specific instantiation of **QUART** , derived from 8B pre-trained VLM models [3] for superior performance. And we use learning rate 2e-5 and batch size 256 to fine-tune the model for 100K gradient steps. Both 

10 Authors Suppressed Due to Excessive Length 


**Fig. 6: Tasks Successful Rate.** R3M lacks alignment with text, which means that although it has some recognition capabilities, it struggles to understand actions through instructions. CLIP and the VC-1 possess the ability to align text and images, enabling them to generate and execute actions based on instructions and observations.As shown above, while R3M may have a slight advantage in easy seen tasks (distinguish), it performs poorly in more complex tasks requiring action execution, significantly lagging behind CLIP and VC-1. **QUART** fully leverages the advantages of large models, enabling semantic understanding of images and alignment with textual information. 

models are trained with the next token prediction objective, which corresponds to the behavior cloning loss in robot learning. 

**Evaluation Details.** We follow the standard robot evaluation metrics [7, 9], success rate (SR), to evaluate the overall performance. The signal we used for robot control is the 11-dimensional command information with the action space outlined in Section 3.1 and 1 stop terminal command means the end of action. More details for each experiment can be seen in the supplementary material. **Baselines.** Considering the absence of VLA models work on quadruped robots at present, we have taken the following baselines into account for a fair comparison: **CLIP** [27], **R3M** [25], and **VC-1** [21]. 

1. **CLIP** [27]uniquely encodes both textual and visual data, fusing these embeddings to create feature sets that integrate textual and visual information. 

2. **R3M** [25]is a visual representation model derived from the Ego4D dataset, which acts as a unified, static perception module for policy learning applications. 

3. **VC-1** [21]pushes the boundaries of visual representation learning by amalgamating data from multiple datasets and assessing performance across a diverse range of tasks via the implementation of CortexBench. 

Since the aforementioned models do not include language conditioning, we include this aspect by separately embedding the language command, allowing us to compare it to our method. Specifically, we concatenate the resulting language embedding tokens with the image tokens generated by the vision model and pass the combined token sequences through a policy head to produce action outputs. 

### **4.2 Overall Performance** 

**Multi-task Performance.** To assess the overall capabilities of VLA models on multiple tasks, we conduct evaluations using instructions randomly selected 

QUAR-VLA: Vision-Language-Action Model for Quadruped Robots 11 

**Table 2: Overall performance. QUART** has achieved success rates far exceeding those of the baselines in tasks of all difficulty levels, especially in the most challenging crawl and unload tasks, where the baselines have no record of success. 

||||Seen||||Uns|een|
|---|---|---|---|---|---|---|---|---|
||Easy|Medium||Hard|||||
||Distinguish|Go to|Go avoid G|o through|Crawl|Unload|Object|Verbal|
|CLIP [27]|0.44|0.43|0.45|0.19|0|0|0.11|0.14|
|R3M [25]|0.58|0|0|0|0|0|0|0|
|VC-1 [21]|0.46|0.43|0.45|0.31|0|0|0.29|0.19|
|**QUART**|**0.66**|**0.60**|**0.53**|**0.41**|**0.32**|**0.12**|**0.35**|**0.33**|


from the training set. It’s important to note that this evaluation introduces variations in the placement of objects and other setup factors (such as robot position). This variation demands the system’s ability to generalize effectively to realistic environmental variability. In total, over 1500 episodes are tested in this evaluation, comprising 425 episodes for going to objects, 500 for going to objects without colliding with the obstacle. 150 for going through the tunnel, 100 for unloading objects, 100 for distinguishing objects, and 75 for crawling under the bar. 

**1. Comparison within VLM baselines.** The experiment results reveal that R3M has poor performances on tasks except distinguish. The primary reason appears to be the lack of alignment with language semantics, which hinders its ability to comprehend tasks beyond basic discrimination. In contrast, CLIP and VC-1 demonstrate satisfactory performance on fundamental perceptual tasks, such as navigation (e.g., "go to" commands). However, their efficacy diminishes significantly when tasks require complex mechanical movements. This observation suggests that while visual language models (VLMs) can grasp abstract principles of the world, directly applying VLMs does not readily translate to the execution of intricate physical tasks. 

**2. VLM baselines vs QUART.** As is shown in Table 2, Our model has achieved optimal performance on nearly all the baseline models. In our study, we have achieved a decoder-only VLA framework. This approach diverges from the traditional single-layer MLP policy head by leveraging the sequential nature of action generation. This allows for the implicit learning of interdependencies between different action dimensions through the use of a transformer. Consequently, while the performance gains may be marginal in simple tasks, there is a noticeable enhancement in tasks that involve complex mechanical movements. significantly improved its perceptual capabilities by incorporating commonsense from the multi-modal large model (MLLM). 

**Generalization capabilities.** To examine the adaptability in unanticipated scenarios, we orchestrated two primary examinations: one concentrated on unfamiliar objects, and the other on unprecedented linguistic directives. For the unfamiliar objects, we cast our gaze upon an array of circumstances: objects belonging to an identical category but exhibiting divergent textures and colors; 

12 Authors Suppressed Due to Excessive Length 


**Fig. 7: Cases with unseen verbal.** Here are 3 verbal instructions. The words below represent the names of instructions in the training data, with the words above in bold indicating verbal instruction. When confronted with unseen instructions, the alighment between the existing language and the integration of vision and action cues within the baselines is compromised, resulting in task failure. This failure manifests in behaviors such as repetitive motion, misdirection, wrong terminate commands. Conversely, **QUART** , leveraging the language prowess inherited from large language models, adeptly achieves generalization under novel instructions, thereby effectuating the harmonization of vision, language, and action. 

**Table 3: Scaling experiments on real-world execution of QUART. QUART** was trained on three training schemes that mix simulated and real data. The experimental results show that as the amount of simulated data increases, the success rate of **QUART** also rises, demonstrating well scaling capabilities. 

|Sim Data : Real|Data<br>0K|:3K|25.6K: 3K|256K: 3K|
|---|---|---|---|---|
|**QUART**|3/|20|7/20|13/20|


objects from the same category but of disparate shapes; and objects with differences in shapes and textures, absent from current datasets. Turning towards the unprecedented linguistic instructions, we characterized unfamiliar instances as linguistic directives that bear the same semantics but vary in expression. For example, within the " _go to the object_ " task, we gauged the directive’s adaptability by employing " _navigate to target_ " as the testing instruction. 

**1. Unseen Object.** As depicted in Fig. 6, we can observe the enhanced generalization ability of our **QUART** model. For unseen objects, both **QUART** and VC-1 perform well, thanks to the advantages of the pre-trained VLM model. However, when it comes to unseen verbal descriptions, apart from **QUART** , all other models essentially failed. This is attributed to the inherent advantage provided by the pre-trained Multimodal Large Language Model (MLLM), enabling the recognition of distinct variations in object types and the comprehension of subtle semantic nuances. Consequently, the model exhibits exceptional generalization performance. 

**2. Unseen Verbal instruction.** The training directives utilized were relatively monotonous, demonstrating that minor alterations in instruction can often perplex the model, thereby revealing an imperative for generalization across lan- 

QUAR-VLA: Vision-Language-Action Model for Quadruped Robots 

13 


**Fig. 8: QUART** can extend basic skills to accommodate complex customized skills with commonsense. It shows example performances of combinational command and spatial understanding towards customized command. 


**Fig. 9: Visualization of seen and unseen tasks.** This figure demonstrates the excellent performance of **QUART** for seen tasks in both simulated and real-world environments. The left part shows 4 instances of seen tasks in both simulation environment and real-world. The right part shows performances on unseen tasks, which contain unseen verbal, object, and background. 

guage directives. Initially, the difficulties introduced by merely replacing descriptions of skill for task generalization were investigated. Evident from Table 2 and Fig. 7 is that **QUART** surpasses other baseline methods, an innate advantage of large-scale multimodal models. In addition, to explore more intriguing linguistic directives and fully harness the universal capabilities of the Large Language Model (LLM), Fig. 8 presents instances where the model demonstrates a clear comprehension and application of combined directives constructed via "first" and "then". It was further noted that even in the absence of explicit directional information within the dataset, the model reliably interpreted linguistic directives which, in turn, influenced task execution accuracy. The ability to utilize language for precise control of quadruped robots facilitated by scene perception, as showcased in Fig. 8, is of immense significance. More intriguing examples and analyses can be found in the supplementary materials. 

**Sim2Real Transferring.** Due to the scarcity of authentic data, a considerable amount of simulated data has emerged as a reliable resource for training 

14 Authors Suppressed Due to Excessive Length 

machine learning models. This has been particularly beneficial in the field of robotics, where real-world data can be challenging and costly to collect. Simulated data, generated from physics engines and computer graphics, can provide diverse and scalable environments for robots to learn from. In this context, we evaluate the performance of joint training using both simulated and real data in real-world scenarios. This approach, often referred to as sim-to-real transfer, leverages the strengths of both types of data. Simulated data provides a wide range of scenarios for initial training, while real-world data ensures the model’s applicability to authentic environments. As illustrated in Table 3, our experiments show that the performance of the **QUART** model improves consistently with the incorporation of simulated data. This demonstrates the effectiveness of simulated data in enhancing the model’s ability to handle real-world tasks. The joint training approach, which combines broad simulation data with narrow real-world data, enables **QUART** to work effectively in real-world environments. The broad simulation data provides a comprehensive training ground, while the narrow real-world data ensures the model’s robustness and adaptability to realworld scenarios. For more detailed experimental results and further insights, please refer to the supplementary materials provided. 

## **5 Conclusion & Future Work** 

This paper emphasizes the significance of deploying Vision-Language-Action models on quadruped robots. We introduce the concept of **V** ision- **L** anguage- **A** ction tasks for **QUA** druped **R** obots **(QUAR-VLA)** , which seamlessly integrates visual information and instructions from diverse modalities to generate executable actions. Specifically, **QUAR-VLA** focuses on two main aspects of deploying VLA models for quadruped robots: defining the action space to balance flexibility and efficiency, and addressing the scarcity of large-scale training datasets. To tackle these two questions, we present the **QUART** models tailored for quadruped robots and the **QUARD** dataset, which includes diverse tasks such as navigation and manipulation. Our extensive evaluation shows that our approach leads to performant robotic policies and enables **QUART** to obtain a range of emergent capabilities. This includes generalization to novel objects, the ability to interpret commands not present in the robot training data, and the ability to perform rudimentary reasoning in response to user commands. 

Furthermore, this work has these areas requiring further enhancements: **1) Automated Data Collection for Larger Datasets.** Future work can explore automated processes for data collection, involving techniques such as active learning and data augmentation can be employed to further expand the dataset size and diversity. **2) Better solution for sim2Real gap.** Integrating domain adaptation methods like domain randomization, data augmentation, and more accurate modeling of physics engines will be a better solution compared with direct co-training. **3) Improving Inference Speed for Real-time Control.** Future works will explore hardware acceleration techniques and model compression techniques to enable faster and more efficient execution of the models. 

# **Supplementary material: QUAR-VLA: Vision-Language-Action Model for Quadruped Robots** 

Pengxian Ding<sup>12</sup> Han Zhao<sup>1</sup> Wenxuan Song<sup>1</sup> Wenjie Zhang<sup>1</sup> Ningxi Yang<sup>1</sup> Donglin Wang<sup>1</sup><sup>_⋆_</sup> 

> 1Westlake University 2Zhejiang University `{dingpengxiang,zhaohan34,wangdonglin}@westlake.edu.cn` 

## **1 Abstract** 

In this supplementary material, we will provide the following supplementary information: 

**Extended Data Collection Details** : We will present additional details regarding the data collection process, including information about the specific environments used and the criteria for determining successful data acquisition for different tasks. 

**Enhanced Experimental Results** : We will provide more comprehensive information about the experimental setup, including a comparative analysis of the results obtained in both seen and unseen environments. Furthermore, we will compare the performance of different model architectures to provide a more thorough evaluation. 

**Expanded Deployment Results** : To facilitate real-world deployment, we will present additional experimental results showcasing the model’s performance across a broader range of tasks and scenarios. 

**Extended Visualizations** : We will include supplementary visual results that highlight various failure cases observed in both real-world and simulation settings, offering a more comprehensive understanding of the model’s limitations and areas for improvement. 

## **2 Details of data collection** 

**Environment** : We prioritize the richness of tasks. In terms of environmental setup, our current tasks are all carried out in relatively simple scenarios without complex visual background information for data collection and model evaluation. At the same time, all experiments are conducted on flat terrains, and we have not yet conducted experiments on complex terrains. Our next goal is to use simulation environments with higher visual fidelity, and add some backgrounds that are more in line with real-world scenarios and more varied terrains for data collection. 

> _⋆_ Corresponding author 

16 Authors Suppressed Due to Excessive Length 

**Planning Algorithm** : In simulation scenarios, we adopted a large-scale parallel simulation environment for the need of rapid automated data collection. During data collection, we used traditional path search algorithms to implement the robot’s route selection. In the early stage of data collection, we adopted the D* algorithm. After evaluating the quality of the early data, we found that the paths planned by D* tend to generate curves with larger turning angles. This could potentially lead to the robot frequently losing sight of the target object, thus affecting the quality of the strategy obtained by imitation learning. Therefore, we changed the navigation algorithm to A*. Taking the go_avoid task as an example, we directly access the positions of the robot, the target object, and obstacles through the simulator. The initial centroid coordinates of the robot on the x-y plane are used as the starting point of the path, and the centroid coordinates of the target object are used as the endpoint. We then add the areas of obstacles on the map. After the path planning is completed, a PD controller is used to convert the path into current velocity and direction. Since we set the speed of the path collection to three levels (fast, normal, slow), the obtained speed needs to be processed to roughly satisfy the speed range set by the levels. 

**Excution Details** : In control systems, the combination of high-frequency and low-frequency control is a strategic approach to achieve finer control and optimize system performance. This integration can be described by a simple mathematical relationship: _N_ = _fhigh/flow_ , where _fhigh_ represents the highfrequency control rate, _flow_ represents the low-frequency control rate, and N is the ratio between the two. In this equation, N indicates the number of times the high-frequency control needs to be executed within a given low-frequency period. The advantage of this combination is that it allows the system to achieve rapid responses and finer adjustments while maintaining the stability and efficiency of the low-frequency control. High-frequency control is typically used to address the rapid changes in system states, while low-frequency control focuses more on long-term system stability and energy management. 

## **3 More experiments** 

### **3.1 Detailed results on seen tasks** 

Firstly, we supplement two additional frameworks: **VLA(LLaVa)** (which uses LLaVa as the backbone for multi-modal large models) and **Aligned VLM+P (Transformer)** (policy head is a decoder-only transformer) to validate the rationality of our VLA model framework design; Next, we provide the results trained on a single task to verify the performance advantages on multi-task; Then, we present more granular results for each task. 

**Two additional frameworks** : 

### **1. Experiment Setting:** 

1) **VLM baseline** : In the main paper, we reproduced previous baselines based on VLM by utilizing features extracted from VLM in conjunction with 

Title Suppressed Due to Excessive Length 

17 

**Table 1: Detailed performance on different architecture.** 

|||Distinguish|Go to|Go avoid|Go through|Crawl|Unload|
|---|---|---|---|---|---|---|---|
|Unaligned VLM+P(MLP)|CLIP [27]|0.44|0.43|0.45|0.19|0|0|
|Aligned VLM+P(MLP)|VC-1 [21]|0.46|0.43|0.45|0.31|0|0|
|Aligned VLM+P(Transformer)|RT-1 [21]|0.22|0.15|0.4|-|0|0|
|VLA(Fuyu)|**QUART**|**0.66**|**0.60**|**0.53**|**0.41**|**0.32**|**0.12**|
|VLA(LLaVa)|**QUART**|**0.66**|**0.52**|**0.40**|**0.32**|**0.18**|**0.16**|


a policy head to generate actions. However, the policy head at that time was merely in the form of an MLP, called **VLM+P(MLP)** , and we did not explore the differences between various types of policy heads, particularly the decoder-only transformer ( **VLM+P(Transformer)** ).Therefore, we have additionally supplemented this study with different policy-head layers to ascertain whether the limitations of the VLM+Policy approach are related to the design of the policy head. 

2) **VLA architecture** : Furthermore, in the paper, we experimented with a multi-modal large model based on the fuyu-8b model( **VLA(Fuyu)** ) to verify whether the effectiveness of VLA is related to the choice of multi-modal large model foundations. To this end, we have also presented experiments based on the LLaVa( **VLA(LLaVa)** ) to validate the benefits of a VLA approach grounded in multi-modal large models. 

### **2. Experiment Analysis:** 

**1) Unaligned VLM + Policy(MLP)** : For the R3M model, the visual backbone employed is a ResNet-50, which has not been aligned with textual features. Consequently, this model is only capable of performing the most rudimentary tasks within its scope. 

**2) Aligned VLM + Policy(MLP)** : In the case of CLIP and VC-1, the visual and textual features have been aligned, enabling the models to comprehend and execute simple tasks. They perform reasonably well on tasks such as "go to," "go through," and "go avoid," which do not involve manipulation of the robot’s body. The primary reason for this adequate performance is that these tasks only require changes in velocity along the x-axis and yaw orientat. 

**3) Aligned VLM + Policy(Transformer)** : As is shown in Table 1, we have also referred to the RT-1 paradigm, employing different policy heads ( **VLM +P(Transformer)** ) to ascertain whether the limitations are inherent to the MLP architecture. We can observe that even when the policy is switched to a Decoder-only Transformer, the trend of the RT-1 method remains consistent with the previous VLM+P (MLP) approach. Only tasks that involve simple distinction and those related to the velocity of the aircraft’s center of mass have success rates; tasks such as crawl and unload are still not achievable. This demonstrates that the choice of different policy heads does not affect the performance of the VLM+policy paradigm. 

**4)Vision + Language + Action (VLA)** : Within the VLA framework, we have utilized the entire decoder-only VLM backbone. However, we directly map action instructions to the language space. During inference, each dimension of 

18 Authors Suppressed Due to Excessive Length 

**Table 2: Multi-task performance vs Single-task performance.** 

||Distinguish|Go to|Go avoid|Go through|Crawl|Unload|
|---|---|---|---|---|---|---|
|CLIP-Multi [27]|0.44|**0.43**|**0.45**|**0.19**|0|0|
|CLIP-Single [27]|**0.52**|0.34|0.37|0.04|0|0|
|VC-1-Multi [21]|0.46|**0.43**|**0.45**|0.31|0|0|
|VC-1-Single [21]|**0.70**|0.37|0.40|**0.34**|0|0|
|**QUART-Multi**|**0.66**|**0.60**|**0.53**|**0.41**|**0.32**|**0.12**|
|**QUART-Single**|0.30|0.36|0.19|0.30|0.25|0.08|


our action (e.g., leg width) engages in joint reasoning with previously inferred information (e.g., robot height). This approach allows for the implicit learning of associations between different action dimensions, thereby effectively grasping the coordinated relationships between multiple parts of the robot and performing well on more complex tasks (e.g., crawling). 

To investigate whether different multi-modal large models (MMLMs) affect our model’s performance, we introduce two variants: Fuyu-8B(used in main paper) and LLaVa-7B. The primary distinction between the two lies in the fact that the former encodes the original image directly, while the latter employs the widely used visual CLIP feature extraction module. From the results, we can see that there is not much difference in performance corresponding to which base model is used. This indicates the importance of the VLA paradigm. 

**Multi-task vs Single-task Performance:** To validate the performance of our multi-task learning approach, we conducted separate training on each individual task to ascertain the benefits that multi-task learning confers on the interrelated tasks. As is shown in Table 2, It has been observed that, for both single and multitask scenarios, the performance of multi-task training has yielded superior results in all but the simplest tasks(distinguish). This indicates that the paradigm of joint training in multi-task settings has enabled the learning of commonalities between different tasks, thereby underscoring the necessity of multi-task cotraining. 

**Detailed Performance:** As is shown in Table 3, we present detailed results for the seen tasks. 

### **3.2 Detailed results on unseen tasks** 

In the context of unseen tasks, we conducted experiments to assess the model’s performance on novel objects and unseen language instructions. The novel objects are categorized into three types: objects of the same category but with different shapes; objects of the same shape but with different colors; and entirely different objects. The unseen language instructions involve paraphrasing existing descriptions with synonymous terms to test the robustness of the model’s performance. 

**Detailed Performance on unseen objects:** In the experiments, we use the yellow, red, green and blue as four base color in the seen tasks, and use the gold, pink, orange, purple as the unseen color. For each objects appear in the seen 

Title Suppressed Due to Excessive Length 19 

**Table 3: Detailed results on seen tasks.** 

||Distinguish letter c|Distinguish letter d|Go to cooker|
|---|---|---|---|
|CLIP [27]|0.36|0.52|0.36|
|VC-1 [21]|0.48|0.44|0.36|
|**QUART**|**0.76**|**0.56**|**0.72**|
||Go to ball|Go to cube|Go to oven|
|CLIP [27]|0.56|0.24|**0.56**|
|VC-1 [21]|**0.64**|0.40|0.32|
|**QUART**|0.60|**0.64**|0.44|
||Go avoid cooker|Go avoid drawers|Go avoid fan|
|CLIP [27]|0.44|**0.52**|0.28|
|VC-1 [21]|0.44|**0.52**|0.20|
|**QUART**|**0.44**|0.48|**0.36**|
||Go avoid sofa|Go through triangle tunnel|Go through rectangle tunnel|
|CLIP [27]|0.56|0.04|0.24|
|VC-1 [21]|0.64|**0.40**|0.28|
|**QUART**|**0.84**|0.24|**0.47**|
||Crawl gate|Unload traybox|Average|
|CLIP [27]|0|0|0.25|
|VC-1 [21]|0|0|0.28|
|**QUART**|**0.32**|**0.04**|**0.44**|


**Table 4: Detailed results on unseen objects.** 

||Go to|Go avoid|Go through|Crawl|Unload|
|---|---|---|---|---|---|
|CLIP [27]|0.4|0.46|0.19|0.04|0|
|VC-1 [21]|0.38|0.41|0.36|0|0|
|**QUART**|**0.4**|**0.73**|**0.41**|**0.35**|**0.01**|


**Table 5: Detailed results on unseen verbal information.** 

||Identify Letter|Navigate to target|
|---|---|---|
|CLIP [27]|0.40|0.44|
|VC-1 [21]|0.28|0.48|
|**QUART**|0.40|**0.52**|
||Move under barrier|Deposit object into container|
|CLIP [27]|0.12|0|
|VC-1 [21]|0|0|
|**QUART**|**0.28**|**0.04**|


tasks, we all test another object which is the same type but with different shape. We also test on objects which do not appear in the seen tasks: pillow, computer and window. As is shown in Table 4, we present detailed results for the unseen objects. We can see that our method have more generalization ability in unseen objects. 

**Detailed Performance on unseen verbal instruction:** Here are alternative expressions for the tasks while maintaining the same meaning. Within the 

20 Authors Suppressed Due to Excessive Length 


**Fig. 1:** Mission _go to the left corner of the object_ . The left picture is produced by model CLIP. The middle picture is produced by model VC-1. The right picture is produced by **QUART** . 


**Fig. 2:** Mission _go to the back of the object_ . The left picture is produced by model CLIP. The middle picture is produced by model VC-1. The right picture is produced by **QUART** . 

parentheses are the instructions for the seen tasks, followed by the modified instructions. 1. (Distinguish Letter) Identify Letter 2. (Go to the object) Navigate to target 3. (Crawl under the barrier) Move under barrier 4. (Unload the object) Deposit Object into container As is shown is Table 5, We can observe that with instructions that carry the same semantics but different expressions, the performance of QUART significantly surpasses that of the baseline. 

### **3.3 More results of customized skills** 

In the manuscript, we demonstrate the capability of our model to generalize to customized skills that were not present in the training tasks, such as complex spatial perception and the ability to combine tasks. Herein, we will present additional case studies to illustrate this skill further. 

**Case1: Go the left corner of the object. Figure 1 Case2: Go the the back of object. Figure 2 Case3: Go the the left and the to the right. Figure 3** 

In these cases, we could find our model could understand the spatial relationships and have the ability to excute combinational skills. 

## **4 More analysis on real robot excution** 

In the main paper, we previously conducted 20 trials on the "Go to" task and compiled the results, which indicated an enhancement in sim2real performance. 

Title Suppressed Due to Excessive Length 21 


**Fig. 3:** Mission _go to the right and the left_ . The left picture is produced by model CLIP. The middle picture is produced by model VC-1. The right picture is produced by **QUART** . 

In this section, we present further experimental outcomes of the model as the size of the simulation dataset increases, as well as results across a broader range of tasks, in order to substantiate the efficacy of our methodology. 

We show the real robot experiments from the following 5 aspects: 1. Effectiveness in seen scenes 2. Sim2Real transfer capabilities 3. Rubustness in different localization 4. Rubustness in different workspace 5. Rubustness in unseen scenes 

More results can be found in https://sites.google.com/view/quar-vla/quarvla-eccv24. 

## **5 Limitation and future work** 

From the perspective of dataset composition, the current magnitude of data and the diversity of trajectories are insufficient. A potential direction for future work is to leverage GPT-based automation to generate more varied and enriched datasets. Additionally, the existing datasets lack complex terrains and long-horizon tasks; enhancing the complexity of the dataset is a crucial method for advancing quadrupedal tasks. 

In terms of task formulation, the current input modalities are limited to visual and textual components. Exploring how to utilize additional modalities (e.g., LiDAR point clouds) to address issues that visual information alone cannot resolve, such as occlusion problems, is a direction worthy of investigation. Furthermore, the existing models are not yet capable of more flexible control in terms of frequency. Although the high-level command action frequency can complete some tasks, more challenging tasks, such as pole crossing, require higher frequency control to achieve higher success rates. Therefore, accelerating the base model’s speed and designing a reasonable sampling mechanism for high-frequency output is an essential component. 

Of course, addressing the sim2real gap is key to effectively utilizing realworld data. The co-training approach adopted in this paper is based on the premise that the sim2real gap for large models is not significant. However, how to more efficiently employ various sim2real methods, such as domain adaptation and randomization, to solve the domain gap between the real and simulated domains is also a line of thought worth exploring. Lastly, given the substantial 

- 22 Authors Suppressed Due to Excessive Length 

amount of sub-optimal data present in the data collection process, how to utilize this data and enable the large model to learn valuable knowledge from failures through reinforcement learning is an important future direction. 

In summary, this is the inaugural work in extending multi-modal large models to quadrupedal robots. In response to the existing challenges of quadrupedal robots, we have designed a dataset that combines extensive simulated data with a small amount of real data for quadrupedal robot VLA and developed a framework based on large models to implement this task. This work has a certain catalytic effect on the development of the robotics community, and we hope for more suggestions to further refine this work in the future, thereby advancing the progress of mobile robotics. 

## **References** 

1. Ahn, M., Dwibedi, D., Finn, C., Arenas, M.G., Gopalakrishnan, K., Hausman, K., Ichter, B., Irpan, A., Joshi, N., Julian, R., Kirmani, S., Leal, I., Lee, E., Levine, S., Lu, Y., Leal, I., Maddineni, S., Rao, K., Sadigh, D., Sanketi, P., Sermanet, P., Vuong, Q., Welker, S., Xia, F., Xiao, T., Xu, P., Xu, S., Xu, Z.: Autort: Embodied foundation models for large scale orchestration of robotic agents (2024) 

2. Bahl, S., Mendonca, R., Chen, L., Jain, U., Pathak, D.: Affordances from human videos as a versatile representation for robotics (2023) 

3. Bavishi, R., Elsen, E., Hawthorne, C., Nye, M., Odena, A., Somani, A., Taşırlar, S.: Introducing our multimodal models (2023), `https://www.adept.ai/blog/fuyu-8b` 

4. Belkhale, S., Cui, Y., Sadigh, D.: Hydra: Hybrid robot actions for imitation learning. In: Proceedings of the 7th Conference on Robot Learning (CoRL) (2023) 

5. Bharadhwaj, H., Vakil, J., Sharma, M., Gupta, A., Tulsiani, S., Kumar, V.: Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking (2023) 

6. Bousmalis, K., Irpan, A., Wohlhart, P., Bai, Y., Kelcey, M., Kalakrishnan, M., Downs, L., Ibarz, J., Pastor, P., Konolige, K., et al.: Using simulation and domain adaptation to improve efficiency of deep robotic grasping. In: 2018 IEEE international conference on robotics and automation (ICRA). pp. 4243–4250. IEEE (2018) 

7. Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., Florence, P., Fu, C., Arenas, M.G., Gopalakrishnan, K., Han, K., Hausman, K., Herzog, A., Hsu, J., Ichter, B., Irpan, A., Joshi, N., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, L., Lee, T.W.E., Levine, S., Lu, Y., Michalewski, H., Mordatch, I., Pertsch, K., Rao, K., Reymann, K., Ryoo, M., Salazar, G., Sanketi, P., Sermanet, P., Singh, J., Singh, A., Soricut, R., Tran, H., Vanhoucke, V., Vuong, Q., Wahid, A., Welker, S., Wohlhart, P., Wu, J., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., Zitkovich, B.: Rt-2: Vision-languageaction models transfer web knowledge to robotic control (2023) 

8. Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., et al.: Rt-2: Vision-language-action models transfer web knowledge to robotic control. arXiv preprint arXiv:2307.15818 (2023) 

9. Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., Ibarz, J., Ichter, B., Irpan, A., 

Title Suppressed Due to Excessive Length 23 

- Jackson, T., Jesmonth, S., Joshi, N.J., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, K.H., Levine, S., Lu, Y., Malla, U., Manjunath, D., Mordatch, I., Nachum, O., Parada, C., Peralta, J., Perez, E., Pertsch, K., Quiambao, J., Rao, K., Ryoo, M., Salazar, G., Sanketi, P., Sayed, K., Singh, J., Sontakke, S., Stone, A., Tan, C., Tran, H., Vanhoucke, V., Vega, S., Vuong, Q., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., Zitkovich, B.: Rt-1: Robotics transformer for real-world control at scale (2023) 

- 10. Caluwaerts, K., Iscen, A., Kew, J.C., Yu, W., Zhang, T., Freeman, D., Lee, K.H., Lee, L., Saliceti, S., Zhuang, V., et al.: Barkour: Benchmarking animal-level agility with quadruped robots. arXiv preprint arXiv:2305.14654 (2023) 

- 11. Eckert, P., Ijspeert, A.J.: Benchmarking agility for multilegged terrestrial robots. IEEE Transactions on Robotics **35** (2), 529–535 (2019) 

- 12. Gu, J., Kirmani, S., Wohlhart, P., Lu, Y., Arenas, M.G., Rao, K., Yu, W., Fu, C., Gopalakrishnan, K., Xu, Z., Sundaresan, P., Xu, P., Su, H., Hausman, K., Finn, C., Vuong, Q., Xiao, T.: Rt-trajectory: Robotic task generalization via hindsight trajectory sketches (2023) 

- 13. Haldar, S., Mathur, V., Yarats, D., Pinto, L.: Watch and match: Supercharging imitation with regularized optimal transport. CoRL (2022) 

- 14. Hutter, M., Gehring, C., Jud, D., Lauber, A., Bellicoso, C.D., Tsounis, V., Hwangbo, J., Bodie, K., Fankhauser, P., Bloesch, M., Diethelm, R., Bachmann, S., Melzer, A., Hoepflinger, M.: Anymal - a highly mobile and dynamic quadrupedal robot. In: 2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). pp. 38–44 (2016). `https://doi.org/10.1109/IROS.2016.7758092` 

- 15. Jiang, Y., Moseson, S., Saxena, A.: Efficient grasping from rgbd images: Learning using a new rectangle representation. In: 2011 IEEE International conference on robotics and automation. pp. 3304–3311. IEEE (2011) 

- 16. Kareer, S., Yokoyama, N., Batra, D., Ha, S., Truong, J.: Vinl: Visual navigation and locomotion over obstacles. 2023 IEEE International Conference on Robotics and Automation (ICRA) pp. 2018–2024 (2022), `https://api.semanticscholar. org/CorpusID:253117178` 

- 17. Karnan, H., Nair, A., Xiao, X., Warnell, G., Pirk, S., Toshev, A., Hart, J., Biswas, J., Stone, P.: Socially compliant navigation dataset (scand): A large-scale dataset of demonstrations for social navigation. IEEE Robotics and Automation Letters **7** (4), 11807–11814 (2022) 

18. Lee, K.H., Nachum, O., Yang, M.S., Lee, L., Freeman, D., Guadarrama, S., Fischer, I., Xu, W., Jang, E., Michalewski, H., et al.: Multi-game decision transformers. Advances in Neural Information Processing Systems **35** , 27921–27936 (2022) 

19. Lee, M.A., Zhu, Y., Srinivasan, K., Shah, P., Savarese, S., Fei-Fei, L., Garg, A., Bohg, J.: Making sense of vision and touch: Self-supervised learning of multimodal representations for contact-rich tasks. In: 2019 IEEE International Conference on Robotics and Automation (ICRA) (2019), `https://arxiv.org/abs/1810.10191` 

20. Li, X., Liu, M., Zhang, H., Yu, C., Xu, J., Wu, H., Cheang, C., Jing, Y., Zhang, W., Liu, H., et al.: Vision-language foundation models as effective robot imitators. arXiv preprint arXiv:2311.01378 (2023) 

21. Majumdar, A., Yadav, K., Arnaud, S., Ma, Y.J., Chen, C., Silwal, S., Jain, A., Berges, V.P., Abbeel, P., Malik, J., Batra, D., Lin, Y., Maksymets, O., Rajeswaran, A., Meier, F.: Where are we in the search for an artificial visual cortex for embodied intelligence? (2023) 

22. Makoviychuk, V., Wawrzyniak, L., Guo, Y., Lu, M., Storey, K., Macklin, M., Hoeller, D., Rudin, N., Allshire, A., Handa, A., State, G.: Isaac gym: High performance gpu-based physics simulation for robot learning (2021) 

- 24 Authors Suppressed Due to Excessive Length 

23. Margolis, G.B., Agrawal, P.: Walk these ways: Tuning robot control for generalization with multiplicity of behavior. In: Liu, K., Kulic, D., Ichnowski, J. (eds.) Proceedings of The 6th Conference on Robot Learning. Proceedings of Machine Learning Research, vol. 205, pp. 22–31. PMLR (14–18 Dec 2023) 

24. Nair, S., Rajeswaran, A., Kumar, V., Finn, C., Gupta, A.: R3m: A universal visual representation for robot manipulation. In: Conference on Robot Learning (2022), `https://api.semanticscholar.org/CorpusID:247618840` 

25. Nair, S., Rajeswaran, A., Kumar, V., Finn, C., Gupta, A.: R3m: A universal visual representation for robot manipulation (2022) 

26. Pari, J., Shafiullah, N.M., Arunachalam, S.P., Pinto, L.: The surprising effectiveness of representation learning for visual imitation (2021) 

27. Radford, A., Kim, J.W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G., Sutskever, I.: Learning transferable visual models from natural language supervision (2021) 

28. Reed, S., Zolna, K., Parisotto, E., Colmenarejo, S.G., Novikov, A., Barth-Maron, G., Gimenez, M., Sulsky, Y., Kay, J., Springenberg, J.T., et al.: A generalist agent. arXiv preprint arXiv:2205.06175 (2022) 

29. Reed, S., Zolna, K., Parisotto, E., Colmenarejo, S.G., Novikov, A., Barth-Maron, G., Gimenez, M., Sulsky, Y., Kay, J., Springenberg, J.T., et al.: A generalist agent. arXiv preprint arXiv:2205.06175 (2022) 

30. Schiavi, G., Wulkop, P., Rizzi, G., Ott, L., Siegwart, R., Chung, J.J.: Learning agent-aware affordances for closed-loop interaction with articulated objects. In: 2023 IEEE International Conference on Robotics and Automation (ICRA). pp. 5916–5922 (2023). `https://doi.org/10.1109/ICRA48891.2023.10160747` 

31. Shah, D., Sridhar, A., Dashora, N., Stachowicz, K., Black, K., Hirose, N., Levine, S.: Vint: A foundation model for visual navigation (2023) 

32. Shilane, P., Min, P., Kazhdan, M., Funkhouser, T.: The princeton shape benchmark. In: Proceedings Shape Modeling Applications, 2004. pp. 167–178 (2004) 

33. Shridhar, M., Manuelli, L., Fox, D.: Cliport: What and where pathways for robotic manipulation. In: Conference on Robot Learning. pp. 894–906. PMLR (2022) 

34. Stone, A., Xiao, T., Lu, Y., Gopalakrishnan, K., Lee, K.H., Vuong, Q., Wohlhart, P., Kirmani, S., Zitkovich, B., Xia, F., Finn, C., Hausman, K.: Open-world object manipulation using pre-trained vision-language models (2023) 

35. Szot, A., Schwarzer, M., Agrawal, H., Mazoure, B., Talbott, W., Metcalf, K., Mackraz, N., Hjelm, D., Toshev, A.: Large language models as generalizable policies for embodied tasks. arXiv preprint arXiv:2310.17722 (2023) 

36. Tang, Y., Yu, W., Tan, J., Zen, H., Faust, A., Harada, T.: Saytap: Language to quadrupedal locomotion. arXiv preprint arXiv:2306.07580 (2023) 

37. Wei, J., Hou, L., Lampinen, A., Chen, X., Huang, D., Tay, Y., Chen, X., Lu, Y., Zhou, D., Ma, T., et al.: Symbol tuning improves in-context learning in language models. arXiv preprint arXiv:2305.08298 (2023) 

38. Wu, Z., Song, S., Khosla, A., Yu, F., Zhang, L., Tang, X., Xiao, J.: 3d shapenets: A deep representation for volumetric shapes. In: Proceedings of the IEEE conference on computer vision and pattern recognition. pp. 1912–1920 (2015) 

39. Yang, R., Zhang, M., Hansen, N., Xu, H., Wang, X.: Learning visionguided quadrupedal locomotion end-to-end with cross-modal transformers. ArXiv **abs/2107.03996** (2021), `https://api.semanticscholar.org/CorpusID: 235765481` 

40. Yu, K.T., Bauza, M., Fazeli, N., Rodriguez, A.: More than a million ways to be pushed. a high-fidelity experimental dataset of planar pushing. In: 2016 IEEE/RSJ 

Title Suppressed Due to Excessive Length 25 

international conference on intelligent robots and systems (IROS). pp. 30–37. IEEE (2016) 

