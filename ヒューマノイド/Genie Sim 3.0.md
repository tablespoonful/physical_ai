---
title: "Genie Sim 3.0 : A High-Fidelity Comprehensive Simulation Platform for Humanoid Robot"
date: "2026-01-05"
authors: "Chenghao Yin; Da Huang; Di Yang; Jichao Wang; Nanshu Zhao; Chen Xu"
url: https://arxiv.org/abs/2601.02078
pdf: https://arxiv.org/pdf/2601.02078
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.02078)** / [論文ページ](https://arxiv.org/abs/2601.02078)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Genie Sim 3.0 : A High-Fidelity Comprehensive Simulation Platform for Humanoid Robot** 

Chenghao Yin<sup>*</sup> , Da Huang<sup>*</sup> , Di Yang<sup>*</sup> , Jichao Wang<sup>*</sup> , Nanshu Zhao<sup>*</sup> , Chen Xu<sup>*</sup> , Wenjun Sun, Linjie Hou, Zhijun Li, Junhui Wu, Zhaobo Liu, Zhen Xiao, Sheng Zhang, Lei Bao, Rui Feng, Zhenquan Pang, Jiayu Li, Qian Wang � , Maoqing Yao � 

* Equal contribution<sup>�</sup> Corresponding authors 


**Fig. 1: Overview of Genie Sim 3.0.** Genie Sim 3.0 is a full-cycle robotic simulation platform that integrates environment reconstruction, scene generalization, data collection, and automated evaluation. We plan to open-source 5,140 object assets of simulation, more than 10,000 hours of synthetic dataset and 100,000 evaluation scenarios. 

**_Abstract_ — The development of robust and generalizable robot learning models is critically contingent upon the availability of large-scale, diverse training data and reliable evaluation benchmarks. Collecting data in the physical world poses prohibitive costs and scalability challenges, and prevailing simulation benchmarks frequently suffer from fragmentation, narrow scope, or insufficient fidelity to enable effective sim-toreal transfer. To address these challenges, we introduce Genie Sim 3.0, a unified simulation platform for robotic manipulation. We present Genie Sim Generator, a large language model** 

**(LLM)-powered tool that constructs high-fidelity scenes from natural language instructions. Its principal strength resides in rapid and multi-dimensional generalization, facilitating the synthesis of diverse environments to support scalable data collection and robust policy evaluation. We introduce the first benchmark that pioneers the application of LLM for automated evaluation. It leverages LLM to mass-generate evaluation scenarios and employs Vision-Language Model (VLM) to establish an automated assessment pipeline. We also release an open-source dataset comprising more than 10,000 hours** 

**of synthetic data across over 200 tasks. Through systematic experimentation, we validate the robust zero-shot sim-to-real transfer capability of our open-source dataset, demonstrating that synthetic data can server as an effective substitute for real-world data under controlled conditions for scalable policy training. For code and dataset details, please refer to: https: //github.com/AgibotTech/genie_sim.** 

## I. INTRODUCTION 

The advancement of robotic manipulation is increasingly supported by vision-language-action (VLA) models, which equip robots with the ability to interpret natural language instructions and execute corresponding physical actions [1] [2]. This capability allows robots to perform a wider range of tasks in unstructured environments, moving closer to humanlike adaptive operation [3]. However, the development of robust and generalizable VLA models relies heavily on access to large-scale, high-quality datasets of robot interactions, which are resource-intensive and time-consuming to collect in the real physical world [4][5]. Furthermore, systematically evaluating and iterating these models requires a consistent, reproducible and scalable testing environment, but the current evaluation approaches on real devices often fail to meet this requirement [6]. 

A high-fidelity simulation platform is a practical and efficient approach to provide large-scale, cost-effective and low sim-to-real gap synthetic dataset and benchmark for VLA training and evaluation [7][8]. A well-designed simulation platform can provide the necessary scale, diversity, and repeatability for both training and evaluation, significantly accelerating the development cycle of VLA-driven robotic systems [9][10]. However, scaling this process encounters three fundamental bottlenecks. First, creating high-fidelity simulation environments that accurately reflect the complexity of the real world traditionally requires significant manual efforts from specialists in 3D modeling and physics simulation. This process is time-consuming, labor-intensive and limits the scale and variety of training data, becoming a critical barrier to model generalization [11][12][13]. Second, while automated or procedural generation can create varied scenes, it often lacks fine-grained control. A core tension exists between generating sufficient diversity for robust learning and maintaining the ability to precisely reproduce or systematically vary specific scenarios. This makes it difficult to debug failures, conduct controlled ablation studies, or measure systematic generalization—hindering rigorous model development [14]. Third, current model evaluation relying on a fixed set of handcrafted metrics (e.g., success rate) fails to capture nuanced task completion quality[15]. Furthermore, human-in-the-loop evaluation is inefficient, subjective, and non-scalable, resulting in an incomplete assessment of policy performance and slows down the iterative training-evaluation cycle. 

To resolve above-mentioned issues, we introduce **Genie Sim 3.0** , a comprehensive open-source simulation platform for environment reconstruction, scene generalization, data collection and automated evaluation. Genie Sim 3.0 integrates the following four novel features: (1) large language 

model (LLM)-driven scene generation and generalization; (2) LLM-based task and evaluation generation; (3) high fidelity simulation via 3D reconstruction and visual generative synthesis; (4) dual-mode data collection pipeline, including teleoperation and automation. 

Developing on these innovative new features, Genie Sim 3.0 provides five new simulation modules to significantly accelerate the model development of embodied intelligence: (1) Genie Sim asset retrieval system, supporting sematic query-based search for 5,140 simulation-ready objects across 353 categories; (2) a scene generation pipeline that operates solely on natural language input and is equipped with comprehensive domain randomization capabilities; (3) more than 10,000 hours of synthetic data with multi-dimensional domain randomization across 200 tasks; (4) a comprehensive benchmark integrating close-loop evaluation with over 100,000 evaluation scenarios, designed to assess a holistic capability profile across multiple dimensions, covering semantic understanding, spatial reasoning, and operational execution, therefore clearly defining model’s performance boundaries and optimization directions. 

Contributions of Genie Sim 3.0 can be summarized into 

five key aspects: 

- 1) We develop a scene generation pipeline called Genie Sim Generator that features a natural language interface that interprets high-level semantic instructions to generate highly realistic simulation scenes in real-time. This interface supports multi-round conservation for iterative refinement, significantly improving efficiency of scene generation. 

- 2) We support rapid, multi-dimensional scene generalization from a single generated scene mentioned above. It can produce vast and varied scenarios by parameterizing factors such as lighting, background, layout, poses, trajectories, sensor noise, and robot morphology within several minutes via natural language instructions. 

- 3) We establish a scalable evaluation benchmark built upon more than 100,000 simulation scenarios. It leverages LLM to automatically generate task instructions and evaluation protocols, which are then executed and scored by VLM. This constructs a comprehensive and multi-dimensional capability profile—spanning semantic understanding, spatial reasoning, and operational execution—that clearly delineates a model’s performance boundaries and optimization pathways. 

- 4) Through systematic experiments, we validate the effective sim-to-real transfer capability of the proposed benchmark framework and synthetic data. Empirical results demonstrate that, under certain conditions, the generated synthetic data can serve as a viable substitute for real-world robotic data, thereby providing scalable support for model training. Furthermore, the benchmark enables the effective prediction and extrapolation of a model’s performance boundaries in real-world scenarios based on its performance in simulation, offering stable and reproducible guidance for model iteration. 

- 5) We open-source Genie Sim 3.0 simulation platform 

which integrates scene generation, evaluation synthesis, data acquisition, and closed-loop model assessment. To foster community progress, we opensource 5,140 assets, 10,000+ hours dataset, 100,000+ evaluation scenarios, and the complete codebase. By providing massive-scale synthetic dataset and evaluation scenes for insightful capability diagnostics and panoramic evaluation to accelerate model iteration, Genie Sim 3.0 reduces reliance on physical hardware, enhances research and development efficiency, and propels the development of practical embodied AI applications. 

is a benchmark consisting of 30 kitchen scenes, over 150 object categories, with defined training, validation and test splits and evaluation metrics. Although seminal benchmarks such as _HomeRobot_ [30], _DaXBench_ [31], _SoftGym_ [32], _PlasticineLab_ [33], _INT-ACT_ [34], _ManiFeel_ [35], _AGNOSTOS_ [36], _RoboTwin 2_ [23], _VLABench_ [37] contribute valuable evaluations, the field remains constrained by several persistent challenges, including narrow evaluation scope, notable sim-to-real gaps in both physical dynamics and visual rendering, and insufficient transfer efficacy to real-world deployments. 

## III. METHOD 

## II. RELATED WORK 

## _A. Robotics Dataset_ 

Numerous open-source datasets are available in robotics, encompassing data collected from both physical robotic platforms and simluation environments. _DROID_ [16] dataset provides over 70,000 real-world robotic manipulation demonstrations; _RoboNet_ [17] integrated 160,000 trajectory data from 7 different robot systems; _RH20T_ [18] includes 100,000 demonstrations spanning 147 different tasks, reflecting a high degree of task diversity; _Open X-Embodiment_ [19] integrates vast amounts of heterogeneous data from laboratories worldwide, comprising over 1 million trajectories, 160,266 tasks, and 22 distinct robot embodiments; _Agibot World_ [20] comprises millions of real-robot data trajectories, covering five core scenarios and encompassing over 80 skills. Despite the extensive scale, real-world datasets impose two fundamental limitations: prohibitively high acquisition costs and narrow generalization capability. 

Synthetic datasets provide cost-effective, large-scale, diverse data with controlled domain randomization to promote robust policy generalization. _RoboCasa_ [21] offers more than 100,000 trajectories, yet its scenes are predominantly confined to kitchen settings; _DexGraspNet 2_ [22] contains over 400 million demonstrations but focuses solely on grasping actions without dynamic scene variations or more complex manipulation skills; _RoboTwin 2.0_ [23] encompasses over 100,000 bimanual manipulation trajectories across 50 tasks, but the physical and visual fidelity of its simulation environment remains notably constrained. 

## _B. Robotics Benchmark_ 

Benchmarks are essential for assessing model performance, yet creating high-quality benchmarks continues to be a significant challenge with the field. _Meta-World_ [24] provides a benchmark designed for multi-task and metareinforcement learning. _HumanoidGen_ [25] establishes a dedicated benchmark comprising 20 tabletop manipulation tasks. _HumanoidBench_ [26] contains 27 whole-body control tasks designed to evaluate reinforcement learning and hierarchical control methods. _Bigym_ [27] introduces a benchmark comprising 40 manipulation tasks set in household kitchen scenarios. _BEHAVIOR-1K_ [28] provides a comprehensive benchmark that includes 50 diverse scenes, over 9,000 object models spanning 1,900+ categories. _ManipulaTHOR_ [29] 

## _A. Scene Generation_ 

With the proliferation of LLM and VLM, scalable, generalizable and conversational data creation has become an emerging paradigm. 

We implement **Genie Sim Generator** , an LLM-driven toolchain that jointly creates simulation scenes and produces _Scene Graph_ for downstream task evaluations. It consists of two tightly-coupled modules. The first is Assets Index, a managed repository of Isaac Sim-ready assets augmented with LLM, VLM and retrieval-augmented generation (RAG) agents, which offers structured Application Programming Interface (API) to facilitate scene composition. The second is Scene Generator, inspired by the scene language [37], this module captures user intent via multi-round conversation, translates it into executable Python code, and compiles the final scene graph with assets for Isaac Sim. 

The entire scene generation process has four stages: intention interpret, assets retrieve, domain specific language (DSL) code generation and results assemble, all within the same chat window sharing the same context. 

**Intention Interpreter** translates user’s open-ended natural language prompt into a structured, machine-interpretable task request. A chain-of-thought (CoT)–enabled LLM first parses and decomposes the natural language prompt into a structured decomposition comprising spatial scene descriptors, object attribute constraints and task-level intents (e.g., “stack-up”, “tidy”, “random”). Ambiguous or underspecified phrases (e.g., “some blocks”, “randomly arranged”) are resolved through a reasoning process grounded in a pre-trained world-knowledge memory. The resulting specification is formulated as a JavaScript Object Notation (JSON) schema containing required semantic object classes (with optional geometric constraints such as size, color and shape) and pairwise spatial relations (e.g., “on”, “adjacent”, “aligned”). The resulting schema is forwarded to the Assets Index to initiate retrieval process. If constraints contradict predefined system rules, the interpreter engages an explicit feedback loop with the user for clarification. 

**Assets Index** is a RAG-powered asset retrieval module. Semantic descriptions are first extracted for all 5,140 objects based on their appearance, geometry, and usage. Subsequently, these descriptions are encoded into 2048dimensional vectors via the QWEN: text-embedding-v4 


Fig. 2: **The Automated Workflow of Genie Sim Generator** . This module captures user intent via multi-round conversation, translates it into executable Python code, and compiles the final scene graph with assets for Isaac Sim. 

model and stored in a ChromaDB vector database. At runtime, the planner extracts keywords (e.g., “yellow cube”) from scene description and encodes them into the same embedding space using the identical model. The resulting query vector is compared against the stored asset embeddings via cosine similarity, and the top-k most similar candidates are retrieved along with their metadata—including Universal Scene Description (USD) paths, collision hulls, mass properties, and texture variants. These assets are seamlessly integrated into the LLM context, ensuring that subsequent code generation references only pre-validated, available assets. This retrieval step is fully transparent to the user and typically completes within 200 milliseconds. 

**DSL Code Generater** draws upon the syntactic structure defined in the scene language [37], but extends it with a back-end adaptation for seamless interoperability with Genie Sim Assets Library. Integrating the contexts from Intention Interpreter, Assets Index and DSL definition, our system synthesizes a precise scene specification via pre-trained LLM. This representation exhibits fine-grained controllability, double float precision and enhanced generalization capability. We maintain the chat context within our engine to support iterative task editing. The output can also be manually adjusted to address limitations of LLM. By embedding our asset library into the LLM context, we achieve joint generalization over categories, poses, lighting, and textures without any fine-tuning. Rich semantic annotations and geometric properties within assets library enables scene-level generalization. Complicated layouts which extend beyond basic tabletop scenarios are also supported such as shelves and storage racks. 

**Results Assembler** finally collects the output from chat context and instantiates the DSL program generated by LLM. To achieve randomization, the DSL program employs random functions that introduce variability in object poses, layout patterns, and choice of objects. During instantiation, a hierarchical Scene Graph with two major parts is created: nodes (objectes encoded with asset id, semantic, size, pose 

and task tag) and edges (spatial relations such as on, in, adjacent, aligned and stacked). Finally assembler utilizes the OpenUSD Schema and Isaac Sim APIs to synthesize simulation-ready USD files. Our Results Assembler generates thousands of diverse scenes within minutes, leveraging the power of LLM and advanced algorithms to produce massive scene layouts with high efficiency. 


Fig. 3: **VLM-Driven Evaluation** . 

## _B. Evaluation Generation_ 

Current open-source simulation benchmarks typically rely on predefined instructions, manually annotated success criteria and repeated trial executions to evaluate VLA models. This paradigm yields a largely unidimensional instruction space, limits the scalability of evaluations, and entails high costs for new task creation. LLM exhibits strong natural language understanding and therefore can be introduced for automated instruction generation, task decomposition and prompt expansion, enabling more diverse, scalable, and cost-effective evaluation pipelines. 

Given a certain simulation scenario, Genie Sim Benchmark leverages the capabilities of the LLM by combining it with Action Domain Evaluation Rule (ADER) system to automatically generate numerous reasonable instructions and executable evaluation configuration files, which are then integrated with the simulator for automated evaluation. 

VLM demonstrates strong visual and semantic understanding. Given formalized task specifications alongside the temporal sequence of visual observations recorded during task execution, VLM can efficiently determine whether task requirements have been satisfied and generate evidence-based justifications (see Fig. 3) . This evaluation paradigm is applicable to the majority of simulation benchmark tasks, markedly reducing human annotation effort and allowing the creation of large-scale evaluation instances at low cost. 

## _C. Environment Reconstruction_ 

To provide large-scale, high-fidelity interactive simulation environment, we utilize 3DGS [38] neural rendering technology for photorealistic image rendering and surface reconstruction, generating high-precision meshes for interactive physical simulation. We collect data using SkylandX Innovation’s MetaCam handheld 3D laser scanner. The collected data contains fisheye images, the corresponding poses for each frame, and the dense point cloud data of the entire scene. 

However, 3D Gaussian Splatting (3DGS) imposes relatively stringent requirements on camera pose accuracy; deviations of even a few pixels can result in blurred rendering, artifacts, and geometric bulges. In complex indoor environments, LiDAR-based SLAM often cannot achieve pixel-level positioning precision, leading to insufficient pose accuracy for high-quality 3DGS reconstruction. In the camera pose optimization module, we first utilize SuperPoint [39] and LightGLue [40] to replace the DSP-SIFT [41] and feature extraction module in COLMAP-PCD [42], which reduces noise in 2D feature points and enhances the ability to extract features in weak textures. Then, we perform triangulation directly using the prior poses of the camera obtained by LiDAR SLAM, and search the 2D feature points corresponding to the lidar 3D points for association and the sparse 3D points to implement BA optimization together. After obtaining the camera pose and 3D point data output using COLMAP-PCD, we train 3DGS using the open-source gsplat [43]framework. During the process of large-scale scene reconstruction, it is always inevitable to collect sufficient coverage of the views. 

To compensate for the insufficient number of views during the collection process and improve the rendering quality, we utilize generative models to extrapolate sufficient views. We use the pretrained model from Difix3D+ [44] to render extrapolated views and obtain high-quality images. Finally, we conducte 3DGS training based on surface reconstruction using a large number of new perspective images produced by the diffusion model and the corresponding pose data, as well as the lidar point cloud data obtained during data collection. We use PGSR [45] for surface reconstruction and obtained a high-precision mesh. 

## _D. Data Generation_ 

The data collection framework integrates two complementary paradigms: teleoperation and automation. Teleoperation is utilized for complex long-horizon tasks to produce high quality human-like demonstrations. In contrast, automated collection excels in efficiency and cost-effectiveness, facilitating the rapid generation of extensive synthetic data for robot imitation learning. 

**Teleoperation:** Our teleoperation framework utilizes a PICO VR Head-Mounted Display (PICO) device to bridge human input with a simulated robotic environment. Functioning as the primary input apparatus, the PICO sends action signals representing the target end-effector pose to a central host. A benchmark module processes these signals, and a motion controller executes the planned trajectory, driving the virtual motion of the robot in simulation environment. 

The simulation system incorporates physical effects in real world, including collisions and friction, which enables the robot to manipulate and interactive with simulated objects. The entire interaction sequence, encompassing robot joint states, visual observations, and object poses, is fully logged to constitute the synthetic dataset. Consequently, this approach generates anthropomorphic motion data and leverages human expertise to tackle intricate tasks that are difficult to automate. 

**Automated Collection:** Leveraging _cuRobo_ [46]—a GPUaccelerated motion planner—as the core trajectory planning module, the fully automated data collection pipeline consists 


Fig. 4: **Automated Data Collection** . A complete task parsing and execution pipeline, which improves task success rate through waypoint filtering and a robust retry mechanism. 

of two parts: task generation and data collection (Figure 4). Task generation is facilitated by an LLM-based asset retrieval system, through which required simulation assets can be efficiently queried and assembled using predefined atomic skills. 

During task parsing, candidate key waypoints—derived from pre-annotated asset configurations, such as grasping poses labeled by _GraspNet_ [47]—are evaluated based on kinematic reachability, collision avoidance, and anthropomorphic feasibility. To improve robustness, multiple candidate waypoints are generated per action, forming several alternative action sequences. Each sequence is executed in simulation and subsequently assessed by a dedicated trajectory evaluation module. In case of execution failure, a state rollback is performed before the next candidate sequence is attempted. 

Unlike most previous approaches that simplify the planning environment—for example, objects not directly related to the task are excluded, which can lead to collisions in cluttered scenes—our system retains environmental completeness. In order to balance completeness and efficiency, mesh simplification is applied to object geometries during scene initialization, maintaining trajectory reliability while significantly improving computational efficiency during planning. 

## _E. Closed-loop Evaluation_ 

For model closed-loop evaluation, the simulation and the model inference environment are decoupled and communicate over the Hypertext Transfer Protocol (HTTP) protocol. The simulator transmits the robot’s observation images and proprioceptive states to the inference service and the model returns control commands, which are then executed in the simulation environment. During simulation execution, task completion is periodically evaluated; if the task is completed, the simulation terminates, otherwise a predefined timeout procedure is invoked to terminate the run. Genie Sim 3.0 benchmark supports the following evaluation features: 

- Integration with common VLA models ( _π_ 0 _._ 5 [48], _GO1_ [20], GR00T, _UniVLA_ [49], _RDT_ [50], _X-VLA_ [51], etc.) 

- Multiple robot types (Genie G1, Genie G2) 

- Multiple end effectors (omnipicker, omnihands, INSPIRE skillhands, zhixing gripper, etc.) 

- Local/distributed inference framework 

- Automated and multi-dimensional evaluation 

## IV. DATASET 

## _A. Task Distribution_ 

To accommodate developers at different stages who may prioritize varying levels of data complexity and focus, our dataset is designed to provide comprehensive coverage of the core competencies required by contemporary VLA models for embodied intelligence. The complexity of the tasks is hierarchically organized, facilitating a structured progression from simple to complex scenarios. A key design principle is composability: long-horizon tasks can be decomposed into 


Fig. 5: **Task Distribution Matrix** . The dataset is constructed along three dimensions: Manipulation skill, Cognitive comprehension, and Task complexity. 

sequences of fundamental sub-tasks contained within the dataset. 

To this end, we structure the task taxonomy along three primary axes (Figure 5): manipulation skill, cognitive comprehension, and task complexity. 

- **Atomic Skills** encompass the model’s fundamental motor actions, such as _pick_ , _place_ , _pull_ , _push_ , _open_ , and _close_ . 

- **Cognitive Comprehension** pertain to the model’s ability to interpret tasks, scenes, and instructions. This includes competencies like _spatial reasoning_ (e.g., size relationships), _attribute understanding_ (e.g., color), _logical inference_ , and _commonsense reasoning_ . 

- **Task Complexity** is defined along metrics such as planning horizon and the need for coordinated control. For instance, the sequence from “single-arm removal of a trash item” to “bimanual coordinated removal of a trash item” and finally to “cleaning all trash from a desktop” illustrates a graduated increase in complexity. 

## _B. Data Distribution_ 

Building upon the aforementioned principles of task distribution, we introduce Genie Sim 3.0 synthetic dataset. This dataset encompasses 200 representative tasks for embodied intelligence, providing over 10,000 hours of simulated interaction that reflects its substantial scale. The data is generated using two robotic platforms, Agibot’s G1 and G2, and incorporates systematic variations across multiple dimensions—including task layout, initial robot pose, environmental lighting, scene configuration, camera noise, and semantic instruction phrasing—ensuring broad coverage and strong generalization capability. The resulting dataset thus supports the training and evaluation of embodied intelligence models with high-quality, diverse, and robust simulated experiences. 

## V. EXPERIMENT 

To systematically assess the validity and utility of GenieSim as a simulation benchmark and data generation platform, we introduce five closed-loop evaluation suites. 

**GenieSim-Sim2Real** is designed to validate the data quality of GenieSim and the fidelity of its simulated environments: it examines whether large-scale synthetic data can match or exceed real-world data in model training, and whether benchmark evaluations in simulation yield conclusions consistent with physical deployment. **GenieSim-Instruction** focuses on language-conditioned manipulation, probing how well policies can follow diverse and compositional natural language instructions. **GenieSim-Robust** systematically evaluates policy robustness by introducing controlled perturbations spanning language instruction rephrasing, robot initial pose, scene background and lighting, camera image quality, and camera position. **GenieSim-Manipulation** covers a broad set of challenging manipulation tasks that require precise motor skills, long-horizon planning, and dexterous object interactions. **GenieSim-Spatial** probes spatial understanding and reasoning, requiring policies to resolve absolute and relative spatial references, perform relational placement, order objects by attribute, and construct vertical structures. Together, these five suites provide complementary perspectives on policy capabilities and benchmark reliability. 


Fig. 6: **GenieSim-Sim2Real Task Setups** . Comparison of initial task configurations between real and simulated testing environments across all evaluated tasks. 

## _A. Experimental Setup_ 

**GenieSim-Sim2Real.** All experiments within this suite use the _π_ 0 _._ 5 model [48] as the base policy, post-trained on varying amounts of real-world or synthetic data. The Agibot G1 robot is deployed for physical task execution. Each training configuration is evaluated over 50 trials in real-world environments and in simulation, ensuring direct comparability between the two evaluation modalities. 

**GenieSim-Instruction, GenieSim-Robust, GenieSimManipulation, and GenieSim-Spatial.** For these four benchmark suites, four state-of-the-art vision-languageaction models are compared: _π_ 0 _._ 5 [48], ACoT-VLA [52], GR00T-N1.7 [53], and _π_ 0 [54]. Each model is fine-tuned with task-specific synthetic data generated by GenieSim 

and evaluated on the Agibot G2 robot using GenieSim’s automated closed-loop evaluation pipeline. 

## _B. GenieSim-Sim2Real_ 

_1) Synthetic Data Scaling:_ We conduct 32 groups of experiments across four representative tasks: Select Color, Recognize Size, Grasp Targets, and Organize Items. These tasks span a range of complexities—from atomic manipulation skills to language-conditioned cognitive reasoning— while avoiding floor or ceiling effects that would obscure performance differences. For each task, _π_ 0 _._ 5 is fine-tuned under four data configurations: 200 and 500 episodes of realworld data, and 500 and 1500 episodes of synthetic data. Results are reported in Tab. I. 

**Effectiveness of Synthetic Data.** Scores improve monotonically with increasing data volume for both real and synthetic sources, consistent with scaling laws in robot learning. At equivalent scale (500 eps), models trained on real-world data outperform those trained on synthetic data, reflecting the higher physical fidelity of real demonstrations. However, scaling synthetic data to 1500 episodes enables the model to surpass all real-data baselines across all four tasks in zero-shot real-world evaluation. This demonstrates that GenieSim’s systematic domain randomization—spanning object textures, lighting conditions, physics parameters, and task variations—effectively bridges the domain gap at scale, offering a practical and scalable alternative to real-world data collection. 

**Consistency between Sim and Real Environments.** Model performance across simulated and physical environments is compared. Despite minor discrepancies attributable to imperfect simulation of contact dynamics and stochastic real-world perturbations, overall performance trends remain consistent across environments. A quantitative correlation analysis (Fig. 7) yields _R_<sup>2</sup> = 0 _._ 931 with a slope _≈_ 1 _._ 023, indicating that GenieSim evaluations reliably predict realworld performance trends and can serve as a cost-efficient substitute for physical benchmarking. 


Fig. 7: **Correlation Analysis of Sim and Real Performance** . All 16 model configurations show a strong linear relationship between simulated and real-world scores ( _R_<sup>2</sup> = 0 _._ 931). 

TABLE I: **Synthetic Data Scaling Results.** Task scores of _π_ 0 _._ 5 fine-tuned with varying amounts of real and synthetic data, evaluated in both simulated and real environments. 

||Select|Color|Recogn|ize Size|Grasp|Targets|Organiz|e Objects|
|---|---|---|---|---|---|---|---|---|
||sim env|real env|sim env|real env|sim env|real env|sim env|real env|
|200 eps real|0.45|0.53|0.50|0.56|0.34|0.39|0.25|0.30|
|500 eps real|0.75|0.73|0.75|0.75|0.54|0.58|0.45|0.40|
|500 eps sim|0.53|0.60|0.50|0.63|0.29|0.33|0.39|0.35|
|1500 eps sim|**0.86**|**0.85**|**0.93**|**0.94**|**0.72**|**0.71**|**0.48**|**0.60**|


TABLE II: **Sim-to-Real Transfer Results.** _π_ 0 _._ 5 scores for models trained on synthetic or real data, evaluated in both simulated and real environments across 8 tasks.<sup>†</sup> 

|**Tk**|Sim <br>|Env<br>|Real <br>|Env<br>|
|---|---|---|---|---|
|**ass**|_Sim Data_<br>(sim-to-sim)|_Real Data_<br>(real-to-sim)|_Sim Data_<br>(sim-to-real)|_Real Data_<br>(real-to-real)|
|Select Color|**0.86**|0.75|**0.85**|0.73|
|Recognize Size|**0.93**|0.75|**0.94**|0.75|
|Grasp Targets|**0.72**|0.54|**0.71**|0.58|
|Organize Items|**0.48**|0.45|**0.60**|0.40|
|Pack in Supermarket|0.94|**1.00**|**0.95**|**0.95**|
|Sort Fruit|**0.90**|**0.90**|**1.00**|**1.00**|
|Place Block into Drawer|0.80|**0.90**|0.85|**0.90**|
|Bimanual Chip Handover|**0.80**|0.70|**0.73**|0.71|
|**Avg.**|**0.80**|0.75|**0.83**|0.75|


> † _Sim Data:_ 500 _∼_ 1500 _episodes of simulation data. Real Data:_ 500 _episodes of real-world data. All models are post-trained from the π_ 0 _._ 5 _baseline._ 

_2) Sim-to-Real Transfer:_ To further validate the crossdomain transfer capability of GenieSim, we extend the evaluation to 8 tasks in Tab. II, adding four newly introduced tasks—Pack in Supermarket, Sort Fruit, Place Block into Drawer, and Bimanual Chip Handover—to the original four. For each task, models trained on synthetic data (500– 1500 episodes) are compared against models trained on 500 episodes of real-world data, with both evaluated in simulated and physical environments. 

**Sim-to-Real.** Across all 8 tasks, models trained solely on synthetic data achieve competitive or superior real-world performance relative to models trained on real data, with an average sim-to-real score of 0.83 versus 0.75 for real-to-real. This confirms that GenieSim-generated data is of sufficient fidelity for direct real-world deployment. 

**Real-to-Sim.** Conversely, models trained on real-world data also transfer well to simulated evaluation, achieving an average of 0.75. This bidirectional transferability demonstrates that the GenieSim environment faithfully captures the physical structures and task dynamics of real-world settings, establishing it as a reliable evaluation platform. 

Taken together, the 32-group scaling experiments and the 8-task transfer study demonstrate that GenieSim provides both high-quality synthetic data and a reliable simulation benchmark—the two foundational properties required for the credible cross-model evaluations conducted in the following suites. 

## _C. GenieSim Benchmark Evaluation_ 

Grounded in the validated reliability of GenieSim, we present a systematic comparison of _π_ 0 _._ 5, ACoT-VLA, GR00T-N1.7, and _π_ 0 across four complementary benchmark 

suites. Each suite targets a distinct capability dimension— instruction following, perturbation robustness, manipulation dexterity, and spatial reasoning—and the high sim-to-real consistency established in Sec. V-B ensures that simulationbased rankings are predictive of real-world policy performance. 

**GenieSim-Instruction.** This suite comprises 10 tasks that require policies to interpret and execute diverse natural language instructions, including directives based on object number, shape, type, color, size, and commonsense or logical reasoning. The tasks are designed to stress-test the language grounding capabilities of VLA models beyond simple keyword matching. As shown in Tab. III, ACoT-VLA and _π_ 0 _._ 5 attain the top average scores of 0.76 and 0.75, substantially outperforming GR00T-N1.7 (0.65) and _π_ 0 (0.37). The two leaders are separated by only 0.01 on average yet differ systematically by task type: ACoT-VLA leads on perception-intensive attribute-matching tasks such as pick_block_color (0.96), pick_billiards_color (0.91), pick_specific_object (0.83), and pick_block_size (0.83), whereas _π_ 0 _._ 5 holds an edge on tasks requiring counting, geometric abstraction, or symbolic composition—pick_block_number (0.82), pick_block_shape (0.55), pick_follow_logic_or (0.81), and straighten_object (0.59). GR00T-N1.7 tops the field on pick_common_sense (0.68), the single task that most depends on world knowledge rather than on visual attribute grounding. Two tasks remain difficult for every model: pick_block_shape (0.44–0.55 for the three strong policies) requires abstracting geometry from appearance, and pick_common_sense (0.59–0.68) requires knowledge that cannot be read off the scene. The consistently low scores of _π_ 0 (0.19 on pick_common_sense, 0.20 on pick_block_shape) confirm that a stronger language- 

TABLE III: **Experimental results on GenieSim-Instruction.** Scores across 10 language-conditioned manipulation tasks. 

|**Tasks**|_π_0_._5|ACoT-VLA|GR00T-N1.7|_π_0|
|---|---|---|---|---|
|pick_billiards_color|0.83|**0.91**|0.73|0.50|
|pick_block_color|0.87|**0.96**|0.80|0.49|
|pick_block_number|**0.82**|0.76|0.61|0.40|
|pick_block_shape|**0.55**|0.52|0.44|0.20|
|pick_block_size|0.79|**0.83**|0.62|0.34|
|pick_common_sense|0.59|0.66|**0.68**|0.19|
|pick_follow_logic_or|**0.81**|0.79|0.72|0.39|
|pick_object_type|**0.80**|**0.80**|0.72|0.42|
|pick_specific_object|0.81|**0.83**|0.69|0.37|
|straighten_object|**0.59**|0.51|0.45|0.38|
|**Avg.**|0.75|**0.76**|0.65|0.37|


TABLE IV: **Experimental results on GenieSim-Robust.** Task scores under 5 categories of perturbations applied to a reference pick-and-place task, anchored by the unperturbed Reference score. ∆ is the signed change relative to Reference, where a negative value marks degradation and a positive value an improvement. 

||_π_|0_._5|ACo|T-VLA|GR00|T-N1.7||_π_0|
|---|---|---|---|---|---|---|---|---|
|**Perturbation**|Score|∆|Score|∆|Score|∆|Score|∆|
|Reference|0.750|–|**0.760**|–|0.650|–|0.370|–|
|Instruction|0.689|_−_0_._061|**0.739**|_−_0_._021|0.678|+0_._028|0.332|_−_0_._038|
|Robot Pose|0.492|_−_0_._258|**0.543**|_−_0_._217|0.429|_−_0_._221|0.240|_−_0_._130|
|Background|0.709|_−_0_._041|**0.737**|_−_0_._023|0.646|_−_0_._004|0.381|+0_._011|
|Image Quality|**0.599**|_−_0_._151|0.589|_−_0_._171|0.489|_−_0_._161|0.307|_−_0_._063|
|Camera Position|**0.575**|_−_0_._175|0.504|_−_0_._256|0.449|_−_0_._201|0.303|_−_0_._067|
|**Avg.**|0.613|_−_0_._137|**0.622**|_−_0_._138|0.538|_−_0_._112|0.313|_−_0_._057|


TABLE V: **Experimental results on GenieSim-Manipulation.** Scores across 10 complex manipulation tasks. 

|**Tasks**|_π_0_._5|ACoT-VLA|GR00T-N1.7|_π_0|
|---|---|---|---|---|
|Open Door|**0.95**|0.55|0.90|0.90|
|Hold Pot|**0.55**|0.45|0.11|0.20|
|Pour Workpiece|**0.93**|**0.93**|0.87|0.07|
|Stock and Straighten Shelf|**0.40**|0.18|0.24|0.18|
|Take Wrong Item Shelf|**0.85**|**0.85**|0.77|0.65|
|Scoop Popcorn|**0.95**|**0.95**|0.77|0.87|
|Clean the Desktop|0.00|0.00|**0.02**|0.00|
|Place Block into Box|**0.58**|**0.58**|0.50|0.45|
|Sorting Packages|**0.51**|0.28|0.20|0.15|
|Sorting Packages Continuous|**0.10**|0.00|0.00|0.00|
|**Avg.**|**0.58**|0.48|0.44|0.35|


TABLE VI: **Experimental results on GenieSim-Spatial.** Scores across 8 spatial-reasoning tasks. 

|**Tasks**|_π_0_._5|ACoT-VLA|GR00T-N1.7|_π_0|
|---|---|---|---|---|
|Pick Object Absolute Position|0.80|**0.81**|0.55|0.46|
|Pick Object Relative Position|**0.65**|0.60|0.43|0.20|
|Place Beverage to Another’s Position|0.40|**0.53**|0.35|0.11|
|Place Object Relative Position|0.50|**0.51**|0.43|0.21|
|Sort Cubes by Size|0.00|**0.30**|0.10|0.00|
|Sort Number|0.00|**0.13**|**0.13**|0.06|
|Stack Bowls|**0.20**|0.00|0.00|0.00|
|Stack Three Building Blocks|**0.30**|**0.30**|0.00|0.00|
|**Avg.**|0.36|**0.40**|0.25|0.13|


model backbone provides a decisive advantage in instructionfollowing scenarios. 

**GenieSim-Robust.** This suite systematically evaluates policy robustness by introducing 5 categories of controlled perturbations to a reference pick-and-place task, spanning language instruction rephrasing, robot initial pose, scene background 

and lighting, camera image quality, and camera position. These conditions model realistic deployment variabilities that are difficult to enumerate exhaustively in physical experiments but are readily programmable in simulation. 

As reported in Tab. IV, we anchor each model against its unperturbed Reference score and report the signed change 

∆ under every perturbation. ACoT-VLA and _π_ 0 _._ 5 are nearly tied at the top (0.622 and 0.613 on average), well ahead of GR00T-N1.7 (0.538) and _π_ 0 (0.313); ACoT-VLA is strongest under Instruction, Robot Pose, and Background, and _π_ 0 _._ 5 under Image Quality and Camera Position. The ∆ columns split sharply by perturbation type: language- and appearancelevel shifts are essentially free—Instruction and Background cost at most 0.061 and are even mildly beneficial for GR00T-N1.7 (+0 _._ 028) and _π_ 0 (+0 _._ 011)—whereas geometric and embodiment-level shifts dominate the degradation, with Robot Pose and Camera Position each removing up to _∼_ 0.26 and Image Quality remaining intermediate. Crucially, ∆ must be read jointly with the absolute score: _π_ 0 exhibits the _smallest_ average degradation (0.057), yet this reflects a floor effect from its low Reference of 0.370 rather than genuine robustness, since its perturbed scores remain the worst of all models. Strong clean-task competence—not a small relative drop—is the decisive driver of deployable robustness. **GenieSim-Manipulation.** This suite consists of 10 tasks that target diverse and challenging manipulation skills, including articulated object interaction (Open Door), bimanual collaboration (Hold Pot), granular material handling (Scoop Popcorn), precise placement and sorting (Place Block into Box, Sorting Packages), desktop cleaning, and multi-step shelf organization. These tasks collectively probe the breadth and depth of a policy’s physical manipulation capabilities in realistic scenarios. As shown in Tab. V, _π_ 0 _._ 5 achieves the highest average score of 0.58, ahead of ACoT-VLA (0.48), GR00T-N1.7 (0.44), and _π_ 0 (0.35). High-performance tasks such as Pour Workpiece, Take Wrong Item Shelf, and Scoop Popcorn are handled competitively by multiple models, reflecting the robustness of large pretrained VLA backbones on well-structured manipulation primitives. In contrast, long-horizon sequential tasks—Sorting Packages Continuous (0.10 / 0.00 / 0.00 / 0.00) and Clean the Desktop (0.00 / 0.00 / 0.02 / 0.00)—remain near-unsolved for all models, highlighting the frontier of current policy capabilities and the discriminative value of this suite. 

**GenieSim-Spatial.** This newly introduced suite comprises 8 tasks that probe spatial understanding and reasoning, spanning absolute and relative spatial reference (Pick Object Absolute / Relative Position), relational placement (Place Beverage to Another’s Position, Place Object Relative Position), attribute-based ordering (Sort Cubes by Size, Sort Number), and vertical construction (Stack Bowls, Stack Three Building Blocks). As shown in Tab. VI, ACoT-VLA achieves the highest average of 0.40, followed by _π_ 0 _._ 5 (0.36), GR00T-N1.7 (0.25), and _π_ 0 (0.13). The suite separates cleanly into two regimes. _Referential_ tasks—resolving a spatial expression to a target or goal pose—are largely tractable, with the two leaders reaching 0.80 and 0.81 on Pick Object Absolute Position. _Constructive_ tasks—ordering objects by attribute or stacking them into a stable structure— collapse for every model: no policy exceeds 0.30 on Sort Cubes by Size, Sort Number, Stack Bowls, or Stack Three Building Blocks. The split holds even at the bottom of the ranking, where _π_ 0 reaches 0.46 on absolute-position 

grounding yet stays at or below 0.06 on all four constructive tasks. The leaders remain complementary—ACoT-VLA tops both attribute-ordering tasks, while _π_ 0 _._ 5 is alone in making progress on Stack Bowls (0.20)—but the 0.38 – 0.46 mean gap between the two regimes for the three strong policies identifies sequential spatial construction, rather than spatial reference resolution, as the binding constraint on current VLA policies. 

Across the four task suites, _π_ 0 _._ 5 and ACoT-VLA emerge as the two strongest policies under complementary profiles. ACoT-VLA holds a narrow lead on the three cognition-oriented suites—GenieSim-Instruction (0.76 vs. 0.75), GenieSim-Robust (0.622 vs. 0.613), and GenieSimSpatial (0.40 vs. 0.36)—while _π_ 0 _._ 5 is decisively ahead on GenieSim-Manipulation (0.58 vs. 0.48), the suite that most heavily weights long-horizon motor execution over language and spatial grounding. The margins on the first three suites (0.01 – 0.04) are far smaller than the 0.10 gap on the fourth, indicating that action-chain-of-thought supervision buys reasoning quality rather than manipulation dexterity. GR00T-N1.7 follows as a competitive third policy, staying within reach of the leaders on several suites (0.65 on GenieSim-Instruction and 0.538 on GenieSim-Robust) and topping individual tasks such as pick_common_sense (0.68) and Clean the Desktop, while _π_ 0 trails by a clear margin throughout (0.37 / 0.313 / 0.35 / 0.13). Read jointly, the four suites also localize where the frontier lies: instruction following is largely solved for strong backbones (leaders at or above 0.75), whereas long-horizon sequential execution— Sorting Packages Continuous, Clean the Desktop, and the four spatial construction tasks—remains at or below 0.30 for every model. The credibility of these cross-model comparisons rests on the reliability of GenieSim as a benchmark platform, which has been rigorously validated through the sim-to-real experiments in Sec. V-B. 

## VI. CONCLUSIONS 

We present Genie Sim 3.0, a unified platform that addresses key bottlenecks in robot learning through these integrated contributions: Genie Sim Generator that uses LLM to create generalized, high-fidelity scenes from natural language instructions; a pioneering LLM-VLM benchmark for automated, scalable task generation and evaluation; and a largescale open-source dataset validated for effective zero-shot sim-to-real transfer. Together, these components constitute a cohesive foundation for advancing scalable data generation, robust policy assessment, and reproducible research toward more generalizable robotic manipulation. 

## APPENDIX 

## ACKNOWLEDGMENT 

We would like to express our sincere gratitude to Linqing Zhong, Sukai Wang and Xiaowei Cai for their assistance with model inference and training; to Haowen Yin, Yanping Zhou, Jiahao Yu, Zengcheng Zhou, and Cheng Ruan for their support with experiment testing; to Chengyue Zhao, Xinke Yu, and Jialu Li for their work on publicity and design; and 

to Cheng Jing, Haoyu Cao, Chi Zhang, Guangte Xiang, Jun Dai, Jia Zeng for their help with data processing. 

## REFERENCES 

- [1] Cheng Chi et al. “Diffusion Policy: Visuomotor Policy Learning via Action Diffusion”. In: _Proceedings of Robotics: Science and Systems_ . Daegu, Republic of Korea, July 2023. DOI: 10.15607/RSS.2023. XIX.026. 

- [2] Moo Jin Kim et al. “OpenVLA: An Open-Source Vision-Language-Action Model”. In: _arXiv preprint arXiv:2406.09246_ (2024). 

- [3] Modi Shi et al. “Is Diversity All You Need for Scalable Robotic Manipulation?” In: _arXiv preprint arXiv:2507.06219_ (2025). 

- [4] Zhenyu Jiang et al. “DexMimicGen: Automated Data Generation for Bimanual Dexterous Manipulation via Imitation Learning”. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . 2025. 

- [5] Yuanpei Chen et al. “Object-Centric Dexterous Manipulation from Human Motion Data”. In: _8th Annual Conference on Robot Learning_ . 2024. 

- [6] Jiangran Lyu et al. _ScissorBot: Learning Generalizable Scissor Skill for Paper Cutting via Simulation, Imitation, and Sim2Real_ . 2024. arXiv: 2409.13966 [cs.RO]. URL: https://arxiv.org/abs/ 

   - 2409.13966. 

- [7] Abhishek Kadian et al. “Sim2Real Predictivity: Does Evaluation in Simulation Predict Real-World Performance?” In: _IEEE Robotics and Automation Letters_ 5.4 (2020), pp. 6670–6677. DOI: 10.1109/LRA. 2020.3013848. 

- [8] Pushkal Katara, Zhou Xian, and Katerina Fragkiadaki. “Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models”. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . 2024, pp. 6672–6679. DOI: 10 . 1109 / ICRA57147.2024.10610566. 

- [9] Yufei Jia et al. _DISCOVERSE: Efficient Robot Simulation in Complex High-Fidelity Environments_ . 2025. arXiv: 2507.21981 [cs.RO]. URL: https:// arxiv.org/abs/2507.21981. 

- [10] Shengliang Deng et al. “GraspVLA: a Grasping Foundation Model Pre-trained on Billion-scale Synthetic Action Data”. In: (2025). arXiv: 2505 . 03233 [cs.RO]. URL: https://arxiv.org/abs/ 2505.03233. 

- [11] Arhan Jain et al. _PolaRiS: Scalable Real-to-Sim Evaluations for Generalist Robot Policies_ . 2025. arXiv: 2512.16881 [cs.RO]. URL: https://arxiv. org/abs/2512.16881. 

- [12] Kejun Hu, Peng Yu, and Ning Tan. “Learning high-fidelity robot self-model with articulated 3D Gaussian splatting”. In: _The International Journal of Robotics Research_ 0.0 (2025). DOI: 10 . 1177/02783649251396980. eprint: https:// 

doi . org / 10 . 1177 / 02783649251396980. 

URL: https : / / doi . org / 10 . 1177 / 

02783649251396980. 

- [13] Xuanlin Li et al. _Evaluating Real-World Robot Manipulation Policies in Simulation_ . 2024. arXiv: 2405. 05941 [cs.RO]. URL: https://arxiv.org/ abs/2405.05941. 

- [14] Yanjiang Guo et al. “Ctrl-world: A controllable generative world model for robot manipulation”. In: _arXiv preprint arXiv:2510.10125_ (2025). 

- [15] Haoran Geng et al. _RoboVerse: Towards a Unified Platform, Dataset and Benchmark for Scalable and Generalizable Robot Learning_ . 2025. arXiv: 2504. 18904 [cs.RO]. URL: https://arxiv.org/ 

   - abs/2504.18904. 

- [16] Alexander Khazatsky et al. _DROID: A Large-Scale InThe-Wild Robot Manipulation Dataset_ . 2025. arXiv: 2403.12945 [cs.RO]. URL: https://arxiv. 

   - org/abs/2403.12945. 

- [17] Sudeep Dasari et al. _RoboNet: Large-Scale MultiRobot Learning_ . 2020. arXiv: 1910 . 11215 [cs.RO]. URL: https://arxiv.org/abs/ 1910.11215. 

- [18] Hao-Shu Fang et al. “RH20T: A Comprehensive Robotic Dataset for Learning Diverse Skills in One-Shot”. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE. 2024, pp. 653–660. 

- [19] Embodiment Collaboration et al. _Open X- Embodiment: Robotic Learning Datasets and RT-X Models_ . 2025. arXiv: 2310.08864 [cs.RO]. URL: https://arxiv.org/abs/2310.08864. 

- [20] Qingwen Bu et al. “Agibot world colosseo: A largescale manipulation platform for scalable and intelligent embodied systems”. In: _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE. 2025. 

- [21] Soroush Nasiriany et al. “RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots”. In: _Robotics: Science and Systems_ . 2024. 

- [22] Jialiang Zhang et al. “DexGraspNet 2.0: Learning Generative Dexterous Grasping in Large-scale Synthetic Cluttered Scenes”. In: _8th Annual Conference on Robot Learning_ . 2024. 

- [23] Tianxing Chen et al. “Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation”. In: _arXiv preprint arXiv:2506.18088_ (2025). 

- [24] Tianhe Yu et al. “Meta-World: A Benchmark and Evaluation for Multi-Task and Meta Reinforcement Learning”. In: _Conference on Robot Learning (CoRL)_ . 2019. arXiv: 1910.10897 [cs.LG]. URL: https:// 

   - arxiv.org/abs/1910.10897. 

- [25] Zhi Jing et al. “HumanoidGen: Data Generation for Bimanual Dexterous Manipulation via LLM Reasoning”. In: _arXiv preprint arXiv:2507.00833_ (2025). 

- [26] Carmelo Sferrazza et al. _HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation_ . 2024. 

- [27] Nikita Chernyadev et al. “BiGym: A Demo-Driven Mobile Bi-Manual Manipulation Benchmark”. In: _arXiv preprint arXiv:2407.07788_ (2024). 

- [28] Chengshu Li et al. “BEHAVIOR-1K: A HumanCentered, Embodied AI Benchmark with 1,000 Everyday Activities and Realistic Simulation”. In: _arXiv preprint arXiv:2403.09227_ (2024). 

- [29] Kiana Ehsani et al. “ManipulaTHOR: A Framework for Visual Object Manipulation”. In: _CVPR_ . 2021. 

- [30] Sriram Yenamandra et al. _HomeRobot: OpenVocabulary Mobile Manipulation_ . 2024. arXiv: 2306.11565 [cs.RO]. URL: https://arxiv. org/abs/2306.11565. 

- [31] Siwei Chen* et al. “DaXBench: Benchmarking Deformable Object Manipulation with Differentiable Physics”. In: _ICLR_ . 2023. 

- [32] Xingyu Lin et al. “SoftGym: Benchmarking Deep Reinforcement Learning for Deformable Object Manipulation”. In: _Conference on Robot Learning_ . 2020. 

- [33] Zhiao Huang et al. _PlasticineLab: A Soft-Body Manipulation Benchmark with Differentiable Physics_ . 2021. arXiv: 2104.03311 [cs.LG]. URL: https:// arxiv.org/abs/2104.03311. 

- [34] Irving Fang et al. _From Intention to Execution: Probing the Generalization Boundaries of VisionLanguage-Action Models_ . 2025. arXiv: 2506.09930 [cs.RO]. URL: https://arxiv.org/abs/ 

   - 2506.09930. 

- [35] Quan Khanh Luu et al. _ManiFeel: Benchmarking and Understanding Visuotactile Manipulation Policy Learning_ . 2025. arXiv: 2505 . 18472 [cs.RO]. URL: https://arxiv.org/abs/2505.18472. 

- [36] Jiaming Zhou et al. “Exploring the Limits of VisionLanguage-Action Manipulation in Cross-task Generalization”. In: _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ . 2025. URL: https : / / openreview . net / forum ? id = 

   - h6xQClTm4W. 

- [37] Yunzhi Zhang et al. _The Scene Language: Representing Scenes with Programs, Words, and Embeddings_ . 2025. arXiv: 2410.16770 [cs.CV]. URL: https://arxiv.org/abs/2410.16770. 

- [38] Bernhard Kerbl et al. “3D Gaussian splatting for realtime radiance field rendering.” In: _ACM Trans. Graph._ 42.4 (2023), pp. 139–1. 

- [39] Daniel DeTone, Tomasz Malisiewicz, and Andrew Rabinovich. “Superpoint: Self-supervised interest point detection and description”. In: _Proceedings of the IEEE conference on computer vision and pattern recognition workshops_ . 2018, pp. 224–236. 

- [40] Philipp Lindenberger, Paul-Edouard Sarlin, and Marc Pollefeys. “Lightglue: Local feature matching at light speed”. In: _Proceedings of the IEEE/CVF in-_ 

_ternational conference on computer vision_ . 2023, pp. 17627–17638. 

- [41] Jingming Dong and Stefano Soatto. “Domain-size pooling in local descriptors: DSP-SIFT”. In: _Proceedings of the IEEE conference on computer vision and pattern recognition_ . 2015, pp. 5097–5106. 

- [42] Chunge Bai, Ruijie Fu, and Xiang Gao. “Colmappcd: An open-source tool for fine image-to-point cloud registration”. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE. 2024, pp. 1723–1729. 

- [43] Vickie Ye et al. “gsplat: An open-source library for Gaussian splatting”. In: _Journal of Machine Learning Research_ 26.34 (2025), pp. 1–17. 

- [44] Jay Zhangjie Wu et al. “DIFIX3D+: Improving 3D Reconstructions with Single-Step Diffusion Models”. In: _Proceedings of the Computer Vision and Pattern Recognition Conference_ . 2025, pp. 26024–26035. 

- [45] Danpeng Chen et al. “PGSR: Planar-based Gaussian Splatting for Efficient and High-Fidelity Surface Reconstruction”. In: _arXiv preprint arXiv:2406.06521_ (2024). 

- [46] Balakumar Sundaralingam et al. “curobo: Parallelized collision-free minimum-jerk robot motion generation”. In: _arXiv preprint arXiv:2310.17274_ (2023). 

- [47] Haoshu Fang et al. “GraspNet: A Large-Scale Clustered and Densely Annotated Datase for Object Grasping”. In: _CoRR_ abs/1912.13470 (2019). arXiv: 1912. 13470. URL: http://arxiv.org/abs/1912. 

   13470. 

- [48] Physical Intelligence et al. _π_ 0 _._ 5 _: a Vision-LanguageAction Model with Open-World Generalization_ . 2025. arXiv: 2504.16054 [cs.LG]. URL: https:// arxiv.org/abs/2504.16054. 

- [49] Qingwen Bu et al. “Univla: Learning to act anywhere with task-centric latent actions”. In: _arXiv preprint arXiv:2505.06111_ (2025). 

- [50] Songming Liu et al. “RDT-1B: a Diffusion Foundation Model for Bimanual Manipulation”. In: _arXiv preprint arXiv:2410.07864_ (2024). 

- [51] Jinliang Zheng et al. “X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model”. In: _arXiv preprint arXiv:2510.10274_ (2025). 

- [52] Linqing Zhong et al. _ACoT-VLA: Action Chain-ofThought for Vision-Language-Action Models_ . 2026. arXiv: 2601.11404 [cs.RO]. URL: https:// arxiv.org/abs/2601.11404. 

- [53] NVIDIA et al. “GR00T N1: An Open Foundation Model for Generalist Humanoid Robots”. In: _ArXiv Preprint_ . Mar. 2025. arXiv: 2503.14734. 

- [54] Kevin Black et al. _π_ 0 _: A Vision-Language-Action Flow Model for General Robot Control_ . 2026. arXiv: 2410.24164 [cs.LG]. URL: https://arxiv. org/abs/2410.24164. 

