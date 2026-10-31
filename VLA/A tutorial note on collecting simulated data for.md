---
title: "A tutorial note on collecting simulated data for vision-language-action models"
date: "2025-08-06"
authors: "Heran Wu; Zirun Zhou; Jingfeng Zhang"
url: https://arxiv.org/abs/2508.06547
pdf: https://arxiv.org/pdf/2508.06547
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2508.06547)** / [論文ページ](https://arxiv.org/abs/2508.06547)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

A TUTORIAL NOTE ON COLLECTING SIMULATED DATA FOR VISION-LANGUAGE-ACTION MODELS 

## **Heran Wu, Zirun Zhou, Jingfeng Zhang*** 

School of Computer Science, The University of Auckland, New Zealand 

*Contact Lecturer Jingfeng Zhang <jingfeng.zhang9660@gmail.com> for any questions 

# ABSTRACT 

Traditional robotic systems typically decompose intelligence into independent modules for computer vision, natural language processing, and motion control. Vision-Language-Action (VLA) models fundamentally transform this approach by employing a single neural network that can simultaneously process visual observations, understand human instructions, and directly output robot actions—all within a unified framework. However, these systems are highly dependent on high-quality training datasets that can capture the complex relationships between visual observations, language instructions, and robotic actions. This tutorial reviews three representative systems: the PyBullet simulation framework for flexible customized data generation, the LIBERO benchmark suite for standardized task definition and evaluation, and the RT-X dataset collection for large-scale multi-robot data acquisition. We demonstrated dataset generation approaches in PyBullet simulation and customized data collection within LIBERO, and provide an overview of the characteristics and roles of the RT-X dataset for large-scale multi-robot data acquisition. Code and data are available at https://github.com/trustmlyoungscientist/dataset ~~f~~ or ~~V~~ LA.git. 

# TABLE OF CONTENTS 

- **Vision-Language-Action Models: An Overview** 

- **Data collection with PyBullet** 

- **Data collection with Libero** 

- **RT-X Dataset: Cross-Embodiment Learning for VLA** 

- **Conclusion** 

- **References** 

# 1 VISION-LANGUAGE-ACTION MODELS: AN OVERVIEW 

Vision-Language-Action (VLA) models have emerged as a transformative paradigm in robotics research, fundamentally changing how robots understand and execute tasks. Unlike traditional robotic systems that decompose intelligence into separate perception, planning, and control modules following the classical “sense-plan-act” paradigm, which decomposes robot intelligence into separate perception, planning, and control modules (Brooks, 1986; Murphy, 2000), VLA models learn unified end-to-end policies that simultaneously process visual observations, understand natural language instructions, and generate robotic actions. 

Recent breakthroughs such as RT-1 (Robotics Transformer 1) (Brohan et al., 2023b), RT-2 (Brohan et al., 2023a), and OpenVLA (Kim et al., 2024) have demonstrated remarkable multi-task generalization capabilities, showcasing the potential of this unified approach. However, the success of these models critically depends on the quality and diversity of their training data—a challenge that distinguishes VLA research from traditional computer vision or natural language processing domains. 

At its core, a VLA model learns a policy function that maps multimodal inputs to robotic actions: 


where **_I_** represents visual observations (RGB images), **_L_** represents language instructions, _A_ represents robot actions, and _θ_ denotes learnable parameters. This formulation enables robots to respond to natural commands like “pick up the red block” by processing camera imagery and text to generate precise joint positions, gripper commands, and motor signals. 

Modern VLA systems typically consist of three interconnected components that process multimodal inputs in sequence. The **vision encoder** transforms raw camera observations into semantic representations: 


where **_I_** represents the visual observation. 

The **language encoder** converts natural language instructions into dense semantic vectors: 


where **_L_** represents the language instruction. 

Finally, the **policy network** fuses these multimodal representations to generate executable actions: 


where **_a_** _t_ represents the robot action at time step _t_ , _πθ_ represents the parameterized policy function that takes visual and language features as input. **_h_** v is the visual feature representation, **_h_** l is the language feature representation, and _A_ denotes the action space. 

Training VLA models requires specialized approaches tailored to the multimodal nature of the problem. Behavior cloning (Pomerleau, 1991) frames policy learning as supervised learning from expert demonstrations, optimizing: 


where _L_ BC( _θ_ ) is the behavior cloning loss function, _θ_ denotes the policy parameters, _D_ contains vision-language-action triplets, and _ℓ_ represents an appropriate loss function. 

Alternatively, **reinforcement learning** optimizes policies through environmental interaction: 


where _J_ ( _θ_ ) is the expected cumulative reward, _θ_ denotes the policy parameters, _τ_ represents a trajectory sampled by following policy _πθ_ to execute language instruction **_L_** , _T_ is the trajectory length (number of time steps in _τ_ ), _γ_ is the discount factor, _st_ is the state at time step _t_ (consisting of visual observations **_I_** _t_ and language instruction **_L_** ), **_a_** _t_ is the action at time step _t_ generated by _πθ_ ( _st,_ **_L_** ), and _r_ ( _st,_ **_a_** _t_ ) is the reward function. 

This tutorial addresses these challenges by examining three practical approaches: PyBullet for simulation-based data collection, RT-X for large-scale real robot data, and LIBERO for standardized benchmarks, providing concrete guidance for researchers tackling VLA dataset construction. 

# 2 DATA COLLECTION WITH PYBULLET 

## 2.1 PYBULLET AND RAVENS FRAMEWORK FOR VLA DATASET CONSTRUCTION 

PyBullet is a lightweight, Python-based physics simulation environment built on the Bullet physics engine (Coumans & Bai, 2016). Its ease of installation, straightforward API, and native support 

for URDF (Unified Robot Description Format) files make it an ideal choice for rapidly setting up manipulation scenarios in robotic learning. These features enabled us to quickly build customized manipulation tasks with fine-grained control over environment parameters, object properties, and data collection procedures. 

For VLA dataset construction, we use PyBullet as the core physics simulation platform, combined with the Ravens framework (Zeng et al., 2021) built on top of PyBullet as a structured task suite. Ravens provides predefined manipulation tasks, scripted oracle policies, and standardized evaluation metrics, while PyBullet handles the underlying physics simulation, camera rendering, and robot control mechanisms. 

This combination brings multiple advantages to VLA research: PyBullet’s flexible API allows precise control over simulation parameters and data collection procedures, while Ravens’ structured task definitions ensure consistency and reproducibility across various manipulation scenarios. The scripted oracle policies provide deterministic, high-quality demonstration data, eliminating human operational randomness and serving as reliable benchmarks for model evaluation. 

## 2.2 CORE IMPLEMENTATION FRAMEWORK 

Our VLA dataset generation pipeline leverages PyBullet’s simulation capabilities through the Ravens framework, focusing on systematic data collection across multiple task scenarios while maintaining controllability over simulation and data quality. Algorithm 1 outlines the complete data generation process, which is implemented in the ravens/demos.py file in our repository. 


Figure 1: Ravens Framework: Collected Task Data showing diverse manipulation scenarios in PyBullet simulation environment. The framework encompasses ten representative tasks including geometric alignment ( _Stack Block Pyramid_ ), perception-based sorting ( _Packing Boxes_ ), spatial reasoning ( _Align Box Corner_ ), multi-object coordination ( _Place Ball in Green_ ), sequential planning ( _Towers of Hanoi_ ), precision manipulation ( _Block Insertion_ ), assembly operations ( _Manipulating Rope_ ), and goal-directed placement tasks ( _Assembling Kits_ ). Each task provides systematic data collection for training VLA models across different manipulation skills and complexity levels. 

where assets ~~r~~ oot is the path to Ravens task assets, N is the number of episodes per task, obs represents the current observation including object poses, oracle is the scripted expert policy, and save ~~d~~ ata() is the function to store vision-language-action triplets. 

## 2.3 TASK SELECTION AND DATA CHARACTERISTICS 

We selected three representative manipulation tasks that demonstrate different types of robotic manipulation skills and task complexity levels: 

Block-insertion tests precise geometric alignment and spatial reasoning capabilities. The task requires inserting an L-shaped block into a matching slot, demanding high-precision 6-degree-offreedom (dof) pose estimation and fine control abilities. 

**Algorithm 1** PyBullet VLA Data Generation Pipeline 

- 1: env = ravens.Environment(assets ~~r~~ oot, disp=True) _{_ Initialize Ravens environment _}_ 2: tasks = [block-insertion, place-red-in-green, towers-of-hanoi] 3: p.connect(p.GUI) _{_ Initialize PyBullet physics engine _}_ 4: **for** task **in** tasks **do** 5: env.set ~~t~~ ask(task) _{_ Configure environment for current task _}_ 6: **for** episode **in** range(N) **do** 7: obs = env.reset() _{_ Reset environment and randomize scene _}_ 8: done = False 9: step = 0 

- 10: **while not** done **do** 

- 11: rgb ~~i~~ mg = p.getCameraImage(width, height, viewMatrix, projMatrix) _{_ Capture RGB observation _}_ 

- 12: action = oracle.act(obs) _{_ Oracle policy generates expert action _}_ 13: obs, reward, done = env.step(action) _{_ Execute action, get new state _}_ 14: save ~~d~~ ata(episode, step, rgb ~~i~~ mg, action, reward) _{_ Store data triplet _}_ 15: step += 1 

- 16: **end while** 17: **end for** 18: **end for** 

Place-red-in-green evaluates color recognition and goal-directed placement capabilities. The task involves identifying objects through color attributes and executing conditional placement operations based on visual features. 

Towers-of-hanoi assesses sequential reasoning and task planning capabilities. This classic puzzle requires understanding operational constraints, maintaining object ordering, and executing multistep action sequences. 

As shown in Figure 1, these tasks cover various primitive operations from pick-and-place and precise insertion to sequential object manipulation, embodying fundamental skills required for VLA models including visual perception, spatial understanding, and sequential planning. 

We successfully collected demonstration data across three manipulation tasks. Three tasks achieved 95% success rates, demonstrating the reliability of the PyBullet simulation environment and the stability of Ravens oracles. This provides a stable source of labeled data for subsequent model training and evaluation. Despite consistent success rates, tasks differ significantly in their underlying skill requirements. Block-insertion emphasizes geometric contact modeling and precise spatial alignment, place-red-in-green focuses on visual attribute understanding and object recognition, while towersof-hanoi involves long-term planning and sequential constraint execution. This diversity ensures that the collected data captures different aspects of manipulation intelligence while maintaining high quality standards. 

## 2.4 DATA ORGANIZATION AND STORAGE FORMAT 

PyBullet data collection is based on Ravens’ distributed storage structure, storing different modality data in independent directories. As shown in Figure 2, this structure is organized by episodes for efficient access during training. 

To demonstrate the actual content and structure of each data modality, Figure 3 shows the real data outputs from our stack-block-pyramid task collection. 

The color directory stores RGB visual observations captured from PyBullet’s camera system, as shown in Figure 3(c). Each file contains a (7, 3, 480, 640) numpy array with uint8 dtype, representing 7 timesteps of 480×640 RGB images. The value range [25, 239] indicates the pixel intensity distribution in the simulation environment. Action data, demonstrated in Figure 3(a), consists of lists containing 7 timesteps where each element is a dictionary with manipulation primitives and parameters computed by Ravens’ oracle policies. The reward directory stores task completion signals following the progression pattern [0, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167] as shown in Fig- 


Figure 2: PyBullet data organization structure with distributed storage format for efficient VLA training. Data modalities are separated into specialized directories (color, depth, action, reward, info) using episode ~~i~~ d-step ~~i~~ d.pkl naming convention, enabling efficient random access and supporting parallel processing for large-scale VLA dataset construction and training pipelines. 

ure 3(b), where the initial timestep starts at 0 and subsequent timesteps receive incremental rewards of 0.167 based on block stacking progress. 

Depth measurements are captured simultaneously with RGB images, containing (7, 3, 480, 640) float32 arrays that provide distance measurements ranging from 0.294 to 2.265 meters from the camera sensor to scene surfaces, as demonstrated in Figure 3(d). The info directory preserves comprehensive metadata including environment states, object poses, and task parameters, organized as lists of length 7 corresponding to the timestep sequence shown in Figure 3(e). Each file follows the naming convention episode ~~i~~ d-step ~~i~~ d.pkl, where the consistent 7-timestep structure across all modalities ensures temporal synchronization necessary for VLA training while enabling efficient random access during model development. 

# 3 DATA COLLECTION WITH LIBERO 

## 3.1 FROM STANDARD BENCHMARKS TO CUSTOMIZED DATA 

LIBERO (Qin et al., 2023) is a well-structured benchmark suite that defines standardized tasks and evaluation protocols using the robosuite (Zhu et al., 2020) framework, which is built on the MuJoCo (Todorov et al., 2012) physics simulator, providing modular environments specifically tailored for Vision-Language-Action (VLA) learning. Our work with LIBERO encompasses two main aspects: utilizing existing benchmark datasets and manually collecting new demonstrations through teleoperation. Each approach has its respective advantages and limitations. 

First, we extensively leveraged LIBERO’s existing demonstration datasets, particularly those curated in the cleaned versions released under the OpenVLA project (Kim et al., 2024). These datasets remove no-operation actions, achieving denser and more meaningful state-action transitions. The cleaned datasets (libero ~~1~~ 0 ~~n~~ o ~~n~~ oops, libero ~~g~~ oal ~~n~~ o ~~n~~ oops, etc.) improve training stability by eliminating long stretches of idle steps that provide little to no learning signal, thereby ensuring that each time step contributes relevant supervision for policy learning. 

However, relying solely on pre-collected data limits our ability to adapt tasks or enhance data diversity. Therefore, we also explored an alternative pathway: collecting customized trajectories using human teleoperation. 


(a) Action data structure 


(c) Color (RGB) data format 


(b) Reward computation results 


(d) Depth sensor data 


(e) Info metadata structure 

Figure 3: Actual data analysis results from stack-block-pyramid task showing real data structures, types, and values captured during PyBullet demonstration collection. 

To evaluate robustness and create challenging scenarios, we modified LIBERO scenes by introducing additional objects that could potentially distract or mislead the robot during task execution. Figure 4 shows the comparison between original and modified scenes. 


Figure 4: LIBERO scene modification for new data collection experiments. (Left) Original standardized scene configuration for object manipulation tasks, (Right) Modified scene with additional distractor objects. 

To implement these scene modifications, we developed custom BDDL (Behavioral Domain Definition Language) files to define new object locations, properties, and initialization logic. BDDL serves as LIBERO’s standardized task specification format, enabling precise control over object placement, spatial relationships, and goal conditions within the simulation environment. Our approach primarily focused on exploring how to add pre-registered objects from LIBERO’s built-in library, leveraging the existing object registry to create more complex and challenging scenarios. 

## 3.2 BUILT-IN OBJECT INTEGRATION 

Building on the scene modification approach shown in Figure 4, we now detail the specific BDDL file modifications required to systematically add distractor objects. LIBERO’s built-in object library contains pre-validated objects with established physics parameters, collision geometries, and visual properties, making them immediately suitable for the experimental complexity enhancement we demonstrated. 

Figure 5 shows the specific BDDL code changes that enable the scene transformation from Figure 4. The modification process involves three coordinated steps that maintain the original task structure while introducing the additional visual complexity visible in the modified scene. 

As shown in Figure 5(a-b), we added cookies ~~1~~ - cookies to the objects section to create the additional distractor visible in Figure 4(Right). This leverages LIBERO’s built-in object registry, which contains pre-validated cookies with established physics parameters and visual properties. No additional asset preparation or physics tuning is required, making this approach ideal for rapid experimental setup. 

The initialization changes in Figure 5(c-d) show the addition of (On cookies ~~1~~ floor ~~o~~ ther ~~o~~ bject ~~r~~ egion ~~5~~ ), which places the distractor in the designated region visible in our modified scene. Crucially, cookies ~~1~~ remains excluded from the (obj ~~o~~ f ~~i~~ nterest ) specification, making it a passive element that doesn’t trigger goal conditions or affect reward calculations. This design preserves the original task semantics while enabling the controlled complexity increase shown in Figure 4. 

Figure 5(e) shows the new other ~~o~~ bject ~~r~~ egion ~~5~~ definition with coordinates (0.125 -0.105 0.175 -0.055) and yaw ~~r~~ otation (0.0 0.0). This positioning strategy ensures that the distractor object enhances visual complexity without interfering with the core manipulation task, as demonstrated in the scene comparison. Careful placement is essential because LIBERO’s fixed-position cameras generate 2D projective images without inherent depth separation. When objects appear close in the camera view, vision models may perceive them as connected components even if physically separate in 3D space, leading to incorrect target identification or manipulation attempts. 


(a) Original objects section 


(b) Modified objects section 


(c) Original initialization 


(d) Modified initialization 


(e) New spatial region definition (other ~~o~~ bject ~~r~~ egion ~~5~~ ) 

Figure 5: BDDL file modifications for adding distractor objects. (a-b) Objects section showing addition of cookies ~~1~~ . (c-d) Initialization section showing placement of new object. (e) New spatial region definition for distractor positioning. 

## 3.3 DEMONSTRATION COLLECTION 

After completing scene configuration, we moved to the actual demonstration collection phase. Figure 6 illustrates our pipeline, which transforms abstract task descriptions into datasets through three interconnected stages. 


Figure 6: LIBERO demonstration collection workflow showing the complete pipeline from BDDL task specification to HDF5 dataset generation. The process includes task parsing and environment setup (left), real-time human teleoperation with device input processing and success validation (middle), and data aggregation from temporary .npz files to structured HDF5 format (right). The success detection includes a 10-step validation mechanism to prevent false positives. 

## 3.3.1 TASK INITIALIZATION AND ENVIRONMENT SETUP 

The left panel shows how we convert human-readable task descriptions into executable robot simulations. We start with BDDL files—structured text files that describe robot tasks by specifying what objects exist, where they should be placed, and what constitutes successful task completion. The BDDLUtils.get ~~p~~ roblem ~~i~~ nfo() function acts as our parser, reading these files and extracting three critical components: problem ~~n~~ ame identifies the specific manipulation task (such as “put ~~i~~ tem ~~i~~ n ~~d~~ rawer”), domain ~~n~~ ame specifies the task category for system organization, and language ~~i~~ nstruction provides the natural language description that will be paired with robot actions for training. 

TASK ~~M~~ APPING serves as LIBERO’s registry that automatically connects task names to their corresponding simulation environments. When you specify “put ~~i~~ tem ~~i~~ n ~~d~~ rawer”, it knows to load a virtual world containing a robot arm, a drawer, appropriate objects, and the correct physics settings. This automation eliminates manual scene construction for each task type. 

Environment creation includes setting control ~~f~~ req=20, which determines that the simulation updates 20 times per second. This frequency ensures smooth robot movements that feel natural to human operators—too low would create jerky motion, while too high would be computationally wasteful. Two essential wrappers are then applied: VisualizationWrapper provides the 

graphical interface that human operators see, while DataCollectionWrapper automatically captures and stores all demonstration data without requiring manual saving commands. 

## 3.3.2 REAL-TIME DATA COLLECTION LOOP 

The middle panel illustrates the core demonstration recording process. Human operators choose between keyboard or SpaceMouse input devices. Keyboard control creates discrete, step-like movements that produce jerky robot trajectories unsuitable for learning smooth manipulation. SpaceMouse is a specialized 3D device that translates physical force and torque into smooth, continuous robot movements across all six degrees of freedom, making it our preferred choice for high-quality demonstrations. 

The collect ~~h~~ uman ~~t~~ rajectory() function orchestrates the entire demonstration session, coordinating between human input, robot simulation, and data recording. Device configuration involves setting sensitivity parameters: pos ~~s~~ ensitivity determines how much the robot moves in response to translational input, while rot ~~s~~ ensitivity controls rotational responsiveness. Proper tuning ensures comfortable control without oversensitive or sluggish response. 

Each demonstration episode begins with env.reset(), which initializes a fresh task scenario by resetting the robot to its starting position and randomizing object placements within appropriate ranges. This randomization ensures dataset diversity rather than the identical scenarios of multiple trials. 

The real-time control loop operates through several synchronized steps. Human device input is processed by input2action(), which converts raw device signals into standardized robot control commands while handling coordinate transformations and safety constraints. These commands are executed through env.step(), which advances the simulation by one timestep, updating robot positions and calculating physics interactions. Simultaneously, the system records RGB camera images, executed actions, and reward signals, providing comprehensive multimodal data. 

Success detection employs env. ~~c~~ heck ~~s~~ uccess() to evaluate whether the current configuration satisfies task completion criteria defined in the BDDL file. However, to prevent false positives from brief object contact or accidental alignment, we implement 10-step validation: tasks are only considered complete when success conditions remain satisfied for 10 consecutive timesteps (0.5 seconds at 20Hz). This temporal requirement ensures genuine task completion. Successful demonstrations are saved as .npz files—a compressed format for efficiently storing numerical arrays. 

## 3.3.3 DATA AGGREGATION AND STORAGE 

The right panel shows how individual demonstration files become organized training datasets. The gather ~~d~~ emonstrations ~~a~~ s ~~h~~ df5() function processes all .npz files from temporary directories, combining them into a single structured database suitable for machine learning training. 

This aggregation process includes data validation to ensure trajectory completeness—checking that image sequences align with action sequences and filtering out demonstrations that end prematurely or contain recording errors. The HDF5 format organizes information hierarchically, with each demonstration becoming a separate group containing its complete sequence of states, actions, and model specifications. This structure enables efficient data access during training, allowing AI algorithms to quickly locate specific demonstrations. 

Comprehensive metadata preservation includes collection timestamps, environment configuration parameters, and complete BDDL task descriptions. This metadata enables researchers to analyze how collection conditions affect data quality and ensures experiment reproducibility by allowing recreation of identical conditions using the preserved parameters. 

# 4 RT-X DATASET: CROSS-EMBODIMENT LEARNING FOR VLA 

## 4.1 THE CROSS-EMBODIMENT LEARNING PARADIGM 

The RT-X dataset represents a fundamental shift from single-robot learning to cross-embodiment learning. Traditional robotic datasets typically focus on individual robot platforms, thereby limit- 

ing their applicability across different hardware configurations. RT-X addresses this limitation by aggregating data from 22 different robot embodiments across 21 institutions (Collaboration et al., 2023), creating a unified dataset of over 1 million real robot trajectories. The key insight is that with appropriate abstraction, manipulation skills can be effectively transferred across different robot modalities, enabling a single model to control multiple robot types. 

## 4.2 DATASET COMPOSITION AND REPRESENTATIVE EXAMPLES 

RT-X encompasses diverse manipulation scenarios across different robot platforms, environments, and tasks (Collaboration et al., 2023). Figure 7 shows representative data samples from the dataset, illustrating the variety of robots, scenes, and manipulation skills captured across real-world settings. 


Figure 7: Representative manipulation tasks from the RT-X dataset (Collaboration et al., 2023). Top row shows typical manipulation scenarios: moving objects to specific locations (“move red pepper to tray”), grasping operations (“pick ice cream”), and precise placement tasks (“move red pepper to A”). Figure adapted from Open X-Embodiment. 

The dataset composition has important practical implications for VLA training. The Franka Panda dominates with 40% of all trajectories, reflecting its widespread adoption in research institutions due to its versatility and research-friendly interface. This concentration provides sufficient data for robust model training on this popular platform. WidowX robots contribute 25% of the data, offering an important counterpoint with different kinematic structures and workspace constraints. Specialized platforms including xArm, Google Robot systems, and Sawyer robots provide the remaining 35%, ensuring diversity necessary for effective cross-embodiment learning. 

From a task perspective, pick-and-place operations constitute 60% of all demonstrations, making RT-X particularly well-suited for basic manipulation research. The remaining 40% includes more complex behaviors: wiping motions, assembly tasks, tool use, and container manipulation. While these advanced skills have smaller sample sizes, they provide essential coverage for developing more sophisticated manipulation capabilities. The dataset spans over 300 distinct scenes ranging from controlled laboratory environments to realistic kitchen settings, with comprehensive object diversity covering geometric shapes, containers, food items, and household appliances. 

## 4.3 DATA FORMAT AND PRACTICAL USAGE 

RT-X employs a crucial technical innovation: standardized action representation. All robot actions are stored in a unified 7-dimensional format [x, y, z, roll, pitch, yaw, gripper], representing endeffector movement and gripper state. This abstraction means that regardless of whether the original data came from a 6-joint WidowX or 7-joint Franka robot, all actions are converted to this common format that captures the essential manipulation semantics. 

This standardization eliminates a major barrier in multi-robot learning and provides RT-X’s primary advantage: unprecedented combination of scale and diversity within a consistent format. When using RT-X data, researchers receive these normalized actions along with corresponding RGB images and language instructions, enabling direct training without robot-specific preprocessing. Rather than investing months in data collection infrastructure, researchers can immediately access million-scale trajectories covering common manipulation scenarios. This accessibility is particularly valuable given that robot data collection is orders of magnitude more expensive and time-consuming than traditional curation of vision and language datasets. 

RT-X demonstrates different strengths for different research objectives. For basic manipulation research, particularly pick-and-place capabilities, the 60% task coverage provides substantial training 

data enabling vision language action model development. For specialized applications like assembly or tool use, RT-X serves as a foundation that researchers can extend with task-specific data collection. The multi-institutional nature introduces quality variations across collection sites, but this variation can actually improve model robustness by providing exposure the suboptimal demonstrations that models will encounter in real-world deployment. 

# 5 CONCLUSION 

Our analysis reveals that effective VLA dataset construction requires careful consideration of three key dimensions: data quality, scale, and diversity. Simulation-based approaches like PyBullet excel at providing controlled, high-quality demonstrations with perfect annotations, making them ideal for algorithmic development and systematic studies. Human-guided methods like LIBERO offer realistic demonstrations that better reflect real-world conditions, though with higher collection costs and variable quality. Large-scale collaborative efforts like RT-X achieve unprecedented diversity and real-world applicability through multi-institutional data collaboration, albeit with inherent quality variations across collection sites. 

Several technical considerations are crucial for successful data collection. Automated data generation requires robust oracle policies and systematic quality control, while human teleoperation demands careful validation mechanisms such as multi-step success verification to ensure demonstration authenticity. Cross-platform compatibility depends on standardized data representations that abstract away hardware differences, enabling knowledge transfer across different robot embodiments. 

# REFERENCES 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023a. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _Robotics: Science and Systems (RSS)_ , 2023b. 

- Rodney A Brooks. A robust layered control system for a mobile robot. _IEEE Journal of Robotics and Automation_ , 2(1):14–23, 1986. 

- Open X-Embodiment Collaboration, Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anikait Singh, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 

- Erwin Coumans and Yunfei Bai. Pybullet, a python module for physics simulation for games, robotics and machine learning, 2016. URL http://pybullet.org. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Sankha Sinha, Thomas Kollar, and Chelsea Finn. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Robin R Murphy. _Introduction to AI robotics_ . MIT press, 2000. 

- Dean A Pomerleau. Efficient training of artificial neural networks for autonomous navigation. _Neural computation_ , 1991. 

- Yifeng Qin, Bingyi Wang, Bo Liu, Ryan Feng, Yifan Zhang, and Yuke Zhu. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36, 2023. 

- Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pp. 5026–5033. IEEE, 2012. 

- Andy Zeng et al. Ravens: Train robotic agents to learn pick and place with deep learning for visionbased manipulation in pybullet, 2021. URL https://github.com/google-research/ ravens. 

- Yuke Zhu, Josiah Wong, Ajay Mandlekar, and Roberto Mart´ın-Mart´ın. robosuite: A modular simulation framework and benchmark for robot learning. In _arXiv preprint arXiv:2009.12293_ , 2020. 

