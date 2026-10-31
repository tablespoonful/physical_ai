---
title: "Building Explicit World Model for Zero-Shot Open-World Object Manipulation"
date: "2026-03-14"
authors: "Xiaotong Li; Gang Chen; Javier Alonso-Mora"
url: https://arxiv.org/abs/2603.13825
pdf: https://arxiv.org/pdf/2603.13825
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.13825)** / [論文ページ](https://arxiv.org/abs/2603.13825)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Building Explicit World Model for Zero-Shot Open-World Object Manipulation** 

Xiaotong Li, Gang Chen, and Javier Alonso-Mora 

**_Abstract_ — Open-world object manipulation remains a fundamental challenge in robotics. While Vision–Language–Action (VLA) models have demonstrated promising results, they rely heavily on large-scale robot action demonstrations, which are costly to collect and can hinder out-of-distribution generalization. In this paper, we propose an explicit-world-modelbased framework for open-world manipulation that achieves zero-shot generalization by constructing a physically grounded digital twin of the environment. The framework integrates open-set perception, digital-twin reconstruction, sampling and evaluation of interaction strategies. By constructing a digital twin of the environment, our approach efficiently explores and evaluates manipulation strategies in physic-enabled simulator and reliably deploys the chosen strategy to the real world. Experimentally, the proposed framework is able to perform multiple open-set manipulation tasks without any task-specific action demonstrations, proving strong zero-shot generalization on both the task and object levels. Project Page: https://bojackbj.github.io/projects/thesis/** 

## I. INTRODUCTION 

Open-world manipulation has recently become a popular research frontier in robotics, aiming to enable robots to perform diverse tasks commanded by humans in unstructured environments. In such settings, robots must have the ability to infer task goals from natural language, perceive and interact physically with previously unseen objects. This open-ended nature introduces fundamental challenges in semantic and physical understanding. 

Recent works have explored Vision–Language–Action (VLA) models [1]–[4], which leverage large-scale vision–language backbones plus an action head to predict robot actions for diverse tasks. Despite strong performance on manipulation benchmarks, VLAs often struggle to generalize beyond the training distribution and rely on large amounts of costly robot demonstration data for supervision. Another line of research investigates world models, which predict the consequences of actions rather than directly imitating demonstrations, either through implicit dynamics modeling [5] or explicit world construction [6]. By reasoning over action outcomes, world-model-based approaches offer improved generalization to unseen objects and tasks. 

Most existing world models are imageor videobased [7]–[9]. While these 2D models can generate visually compelling predictions, they typically lack explicit 3D structure and physical constraints, which limits their ability to faithfully capture real-world dynamics and physical laws. 

All authors are with the Department of Cognitive Robotics (CoR), Delft University of Technology, 2628CD Delft, The Netherlands. X.Li-89@student.tudelft.nl; _{_ g.chen-5; j.alonsomora _}_ @tudelft.nl 

In contrast, explicit world models represent the environment with geometrically and physically meaningful digital-twin assets [10]. However, prior explicit-world-model approaches either target specialized problem settings, such as articulatedobject manipulation toward desired joint configurations [6], or still rely on task-specific demonstrations to train policies [10]. As a result, a method that can generalize zero-shot to both novel objects and novel tasks remains needed. 

In this paper, we propose an explicit world-model-based framework for object manipulation in open-world environments. In such settings, target objects are not predefined, and the robot must operate on previously unseen, openset objects. A central challenge is therefore to accurately reconstruct a digital twin from onboard 2D observations, which are inherently partial and can be further degraded by occlusions, e.g., from the gripper during grasping. To address this challenge, our framework combines modern generative and visual foundation models with classical pointcloud registration techniques to reconstruct digital twins that are both geometrically accurate and semantically consistent. Given a high-level task specification, we then sample diverse interaction strategies within the reconstructed world model. A physics engine is used to simulate the outcomes of these candidate strategies, and a large vision–language model (VLM) evaluates their consistency with the task prompts to select the most promising action sequence. The entire pipeline operates without any task-specific training and is independent of robot embodiment, enabling zero-shot generalization to novel objects and tasks. 

The contributions of this work are listed as follows: 

- An explicit world model based manipulation framework that achieves zero-shot generalization to novel rigid objects and task specifications, without task-specific training or demonstrations. 

- A dynamic digital twin construction pipeline that reconstructs object meshes from onboard observation, and aligns scales and poses to real objects for simulationconsistent transfer. 

- A VLM-based evaluation module that evaluates the success probabilities of simulated outcomes of sampled action candidates. 

We validate our system by evaluating digital-twin construction accuracy and conducting real-robot experiments on multiple open-set, semantically subtle manipulation tasks with previously unseen objects, reporting both qualitative and quantitative results. 

## II. RELATED WORKS 

## _A. Open-world manipulation_ 

Manipulation has long been a popular topic in robotics due to its substantial practical value. Traditional reinforcement learning [11] and imitation learning [12], [13] methods have achieved good performance in this domain, but they typically require training a separate policy for each task, and thus exhibit limited generalization. In contrast, open-world manipulation demands a system that can generate policies for a broad, open-ended set of tasks. 

In the early stage, researchers explored leveraging pretrained vision–language foundation models to achieve strong generalization. A common paradigm is to use a foundation model to infer task-specific affordances [14] or a coarse trajectory/keypoints [15] for open-ended instructions. In [16], [17], the authors both choose to use VLM to predict 2D keypoints, and lift to 3D trajectories. While this approach can generalize well, the task success depends heavily on the accuracy of the model predictions. It typically lacks closed-loop verification and real-time reaction to ensure that the desired outcome is achieved. Thus, in more complete scenarios, this purely feedforward fashion can break down. 

Motivated by these limitations, subsequent work has moved toward Vision–Language–Action (VLA) models. VLA models typically adopt a pretrained VLM as the backbone to encode observations and natural-language task instructions, with additionally an action head to produce executable control commands or policies. This design is architecturally concise and can directly inherit strong semantic priors from large pretrained VLMs. However, action data is a fundamentally different modality from language and vision, and a backbone pretrained primarily on discrete tokens of 2D vision and language does not naturally handle this continuous data representation. As a result, VLA performance and robustness remain strongly bottlenecked by the scale and quality of action supervision. 

Recently, the emergence of models such as Pi [4] and the release of large-scale Open X-Embodiment [18] datasets have signaled a community-wide effort to scale up VLA training data and push toward an actionable scaling law. Nevertheless, collecting diverse, high-quality robot action trajectories remains expensive and difficult to standardize across embodiments and sensing configurations. Fully realizing the benefits of scaling-up will likely take time. 

## _B. World Models_ 

World models were originally introduced in reinforcement learning to improve sample efficiency by enabling agents to _imagine_ the consequences of interactions in a learned latent space [7], [19], [20]. By encapsulating the environment dynamics, a world model allows an agent to roll out hypothetical futures, support planning, and make informed decisions without executing every action in the real world. 

With the recent surge of video diffusion models, much of the progress has focused on image- or video-based world models [8], [9]. Despite producing visually compelling predictions, such 2D world models often struggle to provide 

explicit 3D structure and physical consistency, due to their 2D training data and underlying 2D representations. This limitation makes it difficult to faithfully reason about geometry, contact, and dynamics required for manipulation. 

In parallel, another line of research constructs _explicit_ world models by leveraging 3D reconstruction or generation techniques, typically focusing on object-centric reconstructions of the entities involved in the task. In [10], authors propose an explicit-world-model framework that reconstructs a sim-ready digital twin from visual observations and leverages physics-based simulation to train imitation learning policy. Jiang et al. [6] construct explicit world models for articulated objects and plan trajectories via sampling-based model predictive control within a physics simulator, without requiring demonstrations or reinforcement learning. 

Although these approaches also leverage explicit world models, our focus is different. Compared with [6], which focuses on articulated-object manipulation toward target joint configurations, our framework supports a wider range of open-set manipulation tasks beyond articulated joint-angle goals. In contrast to [10], which still relies on task demonstrations to train imitation-learning policies, our method enables zero-shot generalization to previously unseen tasks, without requiring any task-specific demonstrations. 

## III. METHODS 

## _A. Problem Statement_ 

Formally, given the visual observations _I_ of the scene (e.g., RGB-D images), and a natural language task instruction _C_ , the objective is to build a world model _W_ , and find an _a_ that successfully achieves the goal described by _C_ in the real world. That is, we first build a world model _W_ 


where _τ_ = ( _s, o_ ) is the future states and observations generated by world model _W_ , given the current observation _I_ and sampled action _a_ . Then, 


where _A_ denotes the space of sampled candidate actions from a sample policy _π_ ( _· | I, C_ ), parameterized by endeffector poses, _a_<sup>_∗_</sup> is the selected best action and _R_ ( _C, τ_ ) is a score function that measures the score of _τ_ given the natural language task instruction _C_ . 

In this paper, we aim to build an explicit world model that can generate plausible future states and observations _τ_ . We also designed a prior-based sample policy _π_ and a VLMbased result checker to measure the success score of _τ_ . We focus on rigid objects. Handling deformable and articulated objects would require incorporating elasticity modeling, joint constraints, and contact deformation into the world model. We leave these extensions to future research. 


Fig. 1. Overview of our manipulation task framework with explicit world model construction. The system takes an RGB-D observation _I_ and a natural language task instruction _C_ as input and proceeds through four main stages: (A) _Open-set segmentation_ , (B) _Open-set object grasping_ , (C) _Digital twin reconstruction_ , (D) _Manipulation strategy sampling_ . The outcome is the most promising manipulation strategy, which is then executed on the real robot. 

## _B. System Overview_ 

An overview of the full framework is illustrated in Figure 1. Given an RGB-D image of the scene and a text instruction (e.g., “put the blue cup standing with its opening upside on the right wooden block”), the system outputs a complete manipulation plan and executes it on a real-world manipulator. To achieve our goal, the framework consists of four main components: _Open-set Segmentation and Grasping_ (Section III-C), _Digital Twin Construction_ (Section III-D), and _Manipulation Strategy Sampling_ (Section III-E). 

## _C. Open-set Segmentation and Grasping_ 

In this module, we first employ GPT-4o [21] and Grounded-SAM [22] to segment any objects related to the given task prompt. Specifically, we query the GPT-4o with the RGB image and a prompt question (e.g., “What objects in the picture are involved in the task ‘put the blue cup standing with its opening upside on the right wooden block’? Return their names in two categories as directly manipulated objects and other interactive objects.”). The VLM here allows our method to generalize to arbitrary objects beyond a closed set of predefined classes. Once the object are identified, we use Grounded-SAM to segment the target objects from the input _M_ ˜ obj forimage.bothThisdirectlygives manipulatedus accurate 2Dobjectssegmentation(e.g., cup)masksand other interactive objects involved in interaction (e.g., right wooden block). 

For object grasping, we adopt AnyGrasp [23] as our grasp pose prediction module, which is trained on a large number of real-world grasping data and has demonstrated strong 

robustness in open-set, general-purpose grasping tasks. The grasp pose predictor, denoted as _fg_ ( _·_ ), takes an input RGBD image _I_ and outputs a set of grasp pose candidates _g_ ˜ = _fg_ ( _I_ ). The predicted grasp candidates _g_ ˜ are densely distributed among all graspable objects in the scene. To reduce computational overhead, we first retain only the top 1000grasping,predictionswe reuserankedthe masksby confidence. _M_ ˜ obj of theFor targetinstance-levelobjects obtained from the open-set segmentation module, retaining only _M_ ˜ obj thoseof theassociatedtarget objects,with thewe objectperformof back-projectioninterest. Given theon the masked RGB-D image _Iobj_ to obtain the corresponding partial 3D point cloud _P_ obj. Each grasp candidate in _g_ ˜ is then evaluated based on its spatial proximity to the surface of _P_ obj. Specifically, we retain only those grasp poses which lie within a predefined distance threshold from the segmented object’s surface points, 


To improve the robustness of the grasping, we also add a grasp result checker. After the execution of grasping, we inquire the GPT-4o with the observation from the bottom camera if the gripper successfully grasped the target object, and if the answer is no (the grasping fails or someone deliberately takes the object off), the system will keep trying to find the object and grasp it. 


Fig. 2. The proposed digital twin construction module, containing the mesh generation and two-stage pose alignment. We first generate a textured mesh from the masked RGB image via Hunyuan3D 2.0 [24]. During coarse alignment, we render RGB and depth images from a set of hypopaper poses and compare their similarities with real-world observation in DINO [25] feature space, and select the one that best matches the real-world observation. The resulting coarse pose is then refined using RANSAC and ICP on the partial point cloud back-projected from the depth image. 

## _D. Digital Twin Construction_ 

The objective of this module is to construct accurate 3D meshes of the target objects, align them with real-world observations, and predict their material properties, enabling reliable use in simulation-based interaction and planning. 

This project adopts Hunyuan 3D 2.0 [24] as the 3D generation module. However, the mesh generated by the 3D generation module is in unit scale and canonical pose. Therefore, it is necessary to align the generated mesh with the real-world observation by estimating the appropriate scale and 6-DoF pose. Since only partial object geometry is observed (often limited to a single visible side) and additional occlusions may be introduced by the gripper, classical point cloud based alignment methods tend to perform poorly in this scenario. To address this, we proposed two-stage pose alignment pipeline, performs mesh-observation matching in a coarse-to-fine manner, as shown in Fig 2. 

Let _P_<sup>˜</sup> denote the set of hypothesized coarse object poses sampled in 6D space (translation and rotation). For each hypothesized pose _p_ ˜ _∈ P_<sup>˜</sup> , the corresponding textured 3D mesh is rendered to obtain both the RGB image _I_<sup>˜</sup> rgb and the depth image _I_<sup>˜</sup> depth. The following equation describes this rendering process: 


Then, we compare the similarities of these rendered views with the real-world observation _Iobs_ to select the most promising hypothesis as an initial coarse pose estimate. Here we use DINOv2 [25] as the feature extractor and compute the cosine similarities, 


We then select the hypothesized pose with the highest similarity to the real-world observation as the coarse pose estimate. Using this pose, we render a depth image of the generated mesh and back-project it to obtain a partial point cloud that corresponds to the observed view. This transformation effectively converts the challenging partialto-complete alignment problem into a partial-to-partial alignment problem, thereby enabling the use of conventional point cloud registration methods, such as RANSAC and ICP, for further fine alignment. 

The coarse alignment produces two roughly aligned point clouds that still differ in scale. To estimate the scale factor, we compare the dimensions of the 3D bounding boxes derived from the partial point clouds of both the rendered mesh and the real observation, and adjust the mesh dimensions to match the real-world object. Following this, we refine the transformation using a combination of RANSAC and ICP, yielding an accurate alignment between the generated mesh and the real object. We examined our mesh alignment pipeline and the results are in Sec. IV-B. 

Moreover, Inspired by Xu et al. [26], who leveraged an LLM together with a curated material library to infer the material and physical properties of an object from its masked image, we utilize the reasoning capability of GPT-4o to predict the material of the object. The predicted material can then be used to assign corresponding physical properties in the simulation environment. 

## _E. Manipulation Strategy Sampling_ 

Once the digital twin of the environment is constructed, we integrate it into a physics-enabled simulation environment to perform manipulation strategy sampling. In this work, we adopt NVIDIA Isaac Sim as the simulation platform. We then sample 6-DoF poses for the grasped object, representing candidate manipulation goals. The simulated outcome of each sample is then evaluated to determine whether the 


Fig. 3. Our manipulation strategy sampling module. (a) _Interaction area segmentation_ : We use GPT-4o and Grounded-SAM to segment the interaction area to constrain the sample space of translation. (b) _Interaction strategy sampling_ : Different rotations of the dynamic object are sampled. The outcomes are simulated in the Isaac Sim. (c) _Result checking_ : The results are rendered in the simulator. We query the GPT-4o again to check which samples fulfill the task requirements, and feed the results to a Gaussian Process classifier to get the success probabilities. 

manipulation strategy successfully completes the task. This process allows us to test diverse candidate strategies without executing them on the real robot. 

To improve sampling efficiency and reduce the size of the search space, the translation component of the dynamic object’s pose is constrained to be near the most probable interaction region, which is predicted by GPT-4o plus Grounded-SAM, as illustrated in Fig. 3a. The segmented region is back-projected into 3D space to obtain a point cloud, from which we compute the centroid as reference for the initial estimate of the translation component. 

After constraining the translation around the interaction area, we sample different rotation angles, which are reachable by the robot arm, to generate diverse 6-DoF pose hypotheses. For each sample, we spawn the non-directly manipulated object at its real-world pose and the grasped object at the sampled pose, and the Kinova arm with proper joint values computed by an inverse kinematics solver. 

For each simulated strategy sample, we render an RGB image as the observation for each candidate from a fixed, front-facing viewpoint with a _−_ 60<sup>_◦_</sup> tilt, shown in Fig 3 b on the left. We then query GPT-4o with the rendered image and the natural language task instruction to determine whether the observed outcome satisfies the instruction. This yields weak binary labels _yi ∈{_ 0 _,_ 1 _}_ for each end-effector pose ( **t** _i,_ **q** _i_ ), where **t** _i ∈_ R<sup>3</sup> is translation and **q** _i_ = [ _w x y z_ ]<sup>_⊤_</sup> is 

a unit quaternion. The strategies deemed successful by the GPT-4o are prioritized for real-robot execution. 

To obtain calibrated success probabilities, we train a Gaussian Process (GP) classifier over SE(3) on the LLM-provided labels _{_ ( **t** _i,_ **q** _i_ ) _, yi}_ . At test time, the GP outputs calibrated success probabilities. We use the predicted probabilities to rank all candidate strategies and select the one with the highest likelihood of success for real-robot execution. 

## IV. RESULTS 

## _A. Experiments Setup_ 

Our experiments contain two parts. First, we tested the digital twin alignment accuracy. The second part was nine different real-world manipulation tasks. The selected tasks are designed to validate the system’s ability to understand both semantic instructions and spatial relations, and also the ability to complete various open-world manipulation tasks without seeing the objects or demonstrations before. 

We used the 7-DoF Kinova Gen3 Lite robotic arm.Two Intel RealSense D405 stereo cameras were mounted on the gripper and the front bottom on the mobile base, respectively. The bottom camera has a 25 degree elevation angle to better observe the grasped object. For computational resources, we have an NVIDIA RTX 2070 GPU with 6GB RAM on a laptop for Isaac Sim simulation, and an NVIDIA RTX 

TABLE I 

COMPARISON OF MESH ALIGNMENT PERFORMANCE BETWEEN OUR TWO-STAGE ALIGNMENT PIPELINE AND DIRECT ALIGNMENT. 

|**bjt**|**lidl**|**our m**|**ethod**|**direct a**|**lignment**|
|---|---|---|---|---|---|
|**oecs**|**va sampe**|success rate ↑|RMSE ↓|success rate|RMSE|
|**without grasp in the **|**gripper**|||||
|mug|11|**90.91%**|0.00457|27.27%|**0.00390**|
|box|5|**100.00%**|**0.00564**|**100.00%**|0.00684|
|foam box container|5|**40.00%**|**0.00665**|20.00%|0.00745|
|bottle|8|**100.00%**|0.00432|62.50%|**0.00367**|
|laptop|11|**90.91%**|**0.00408**|45.45%|0.00453|
|**grasped in the gripp**|**er**|||||
|mug|9|**88.89%**|**0.00443**|11.11%|0.00450|
|banana|8|**100.00%**|0.00505|**100.00%**|**0.00460**|
|fish|4|**100.00%**|0.00400|**100.00%**|**0.00317**|
|cup|3|**66.67%**|**0.00412**|33.33%|0.00474|


Fig. 4. Qualitative results of the proposed two-stage mesh alignment method. The left image shows the aligned meshes overlaid with the RGB-D observation. The right image illustrates the corresponding real-world setup. 

3090 GPU workstation with 24GB RAM for computer vision models like Grounded-SAM and Hunyuan 3D 2.0. 

## _B. Digital Twin Alignment Accuracy_ 

In this experiment, we compare our proposed two-stage mesh alignment pipeline with a direct alignment baseline, which applies RANSAC and ICP directly to the generated mesh. Ideally, the pose error of each object would serve as a more informative metric for evaluating alignment performance; however, ground-truth object poses are unavailable in the real-world setup, and coordinate frames are not consistently fixed for each generated mesh. Therefore, we evaluate alignment performance using two complementary metrics: 

alignment success rate, which measures the correctness of the estimated object pose, and root mean square error (RMSE), which assesses the geometric precision of the alignment. 

We conduct experiments across multiple object categories, both being placed freely and under grasping scenarios. Since ground-truth meshes are also unavailable, we use Hunyuan 3D to generate meshes for all samples. Both the proposed and baseline alignment pipelines use the same generated meshes for a fair comparison. The qualitative results are shown in Fig. 4, and quantitative results are summarized in Table I. 

The results demonstrate that our proposed two-stage mesh alignment method substantially improves the alignment success rate compared with direct alignment using RANSAC and ICP. The direct alignment baseline relies solely on minimizing point-to-point distances without a reliable initialization, which often leads to convergence to local minima or incorrect correspondences. In contrast, our method leverages an initial coarse alignment stage guided by appearance similarity, effectively narrowing the search space for fine alignment and improving robustness to noise and scale differences. Overall, our method achieves a much higher alignment success rate while maintaining comparable geometric accuracy, validating the effectiveness of the twostage pipeline for robust and generalizable mesh-to-scene alignment. 

## _C. Real Robot Task Performance_ 

We performed 9 real robot experiments for a total 96 attempts on our system, as shown in Fig. 5. The selected tasks are designed to validate the system’s ability to understand both semantic instructions and spatial relations, and also the ability to complete various open-world tasks without seeing the objects before or fine-tuning on these tasks. Relying on these properties, our system shows the potential to tackle the open-world object manipulation problem in a novel way. 

The success rates for the selected tasks are reported in Table II. We observe that six of the nine tasks reach a success rate of at least 75%. The other three tasks perform less reliably, and we discuss possible reasons in the later failure analysis. 

To provide a comprehensive evaluation of the entire system, we record the success/failure results of all major compo- 


Fig. 5. Representative tasks used for experimental validation. Frames with the same color represent the same task, where the top one denotes the initial scene and the bottom one denotes the final scene. 

TABLE II 

TASK SUCCESS RATE OF DIFFERENT MANIPULATION SCENARIOS. 

|**Task**|**Success Rate**|
|---|---|
|Put the banana into the basket|83.3% (10/12)|
|Put the lemon into the white cup|75.0% (9/12)|
|Put the yellow cube into the white box|91.7% (11/12)|
|Put the yellow cube into the blue can|75.0% (9/12)|
|Stack the green cube onto the yellow cube|50.0% (6/12)|
|Put the long cutlery box on the two boxes, like a bridge|75.0% (9/12)|
|Put the long cutlery box into the gap between two boxes|83.3% (10/12)|
|Put the blue cup upside on the wooden box|33.3% (2/6)|
|Put the blue cup upside down on the wooden box|33.3% (2/6)|


Fig. 6. Sankey diagram illustrating the stage-wise success and failure flow across all 96 real-world trials. Each block represents one functional module in the proposed framework. 

nents, including object grasping, mesh alignment, interaction area segmentation, strategy sampling in simulation, sampling result checking, and real robot execution. The results are visualized as a Sankey diagram as shown in Fig 6. 

Most of the failures came up from the result checker and final execution stage. The result checker failure denotes that the visual information were not clear enough, at least for 

an LLM, to make correct judgments. We also conducted a task-level failure analysis as illustrated in Fig.7, and it shows that most of the result checker failures happened in the ”cup on/upside down on the boxes”, since the visual features of a cup standing upside and upside down were ambiguous. Overall, the LLM-based checker did demonstrate strong generalization and semantic understanding across different object configurations. However, its sensitivity to visual ambiguity suggests that incorporating multimodal feedback (e.g., depth or contact information) could further improve its robustness. 


Fig. 7. Failure type distribution across all 9 tasks. Each cell represents the number of occurrences of a specific failure type for a given task. 

The real robot execution failure means that although the action candidates were successful in the simulator, the real robot execution still failed, indicating the sim-to-real gap 

was nontrivial. Several factors contribute to this discrepancy. First, the physics engine of Isaac Sim, though highly realistic, cannot perfectly replicate real-world contact dynamics. In an attempt to mitigate this gap, we incorporated material property estimation to better parameterize physical attributes in Isaac Sim. However, the range of adjustable parameters remains limited for rigid body objects. In particular, hollow or deformable structures, such as plastic cubes in the ’Stack cubes’ task, cannot yet be accurately modeled or detected based solely on visual appearance, leading to further inconsistencies between simulated and real interactions. Second, the robot hardware precision and control latency introduce minor pose and timing errors that can accumulate during execution, especially for tasks with tight spatial constraints. Third, sensor noise and calibration errors (e.g., camera extrinsics and depth inaccuracies) can cause small misalignment between the reconstructed scene and the actual setup. 

## V. CONCLUSION 

This work presented a novel framework that constructs a mesh-based explicit world model to enable action sampling and evaluation for open-world manipulation tasks. Our approach leverages VLMs and a simulator to reason about object dynamics and choose successful actions without any demonstrations. Experimental results demonstrate that the proposed two-stage mesh alignment pipeline is able to support the accuracy and robustness of digital twin reconstruction, providing more reliable object pose estimation. With the constructed explicit world model, the system is capable of performing dynamic reasoning and strategy evaluation across diverse manipulation tasks, and achieves successful transfer from simulation to real-world execution, proven by real robot experiments. 

While the proposed framework demonstrates promising results, the simulation-based strategy sampling process remains computationally demanding, which currently prevents real-time deployment. Future work will focus on improving computational efficiency to facilitate efficient real-world deployment. 

## REFERENCES 

- [1] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” 2024. [Online]. Available: https://arxiv.org/abs/2406.09246 

- [2] D. Ghosh, H. R. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo _et al._ , “Octo: An open-source generalist robot policy,” in _Robotics: Science and Systems_ , 2024. 

- [3] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning (CoRL)_ . PMLR, 2023. 

- [4] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky, “ _π_ : A vision-language-action flow model for general robot control,” _CoRR_ , 2024. 

- [5] Y. Liao, P. Zhou, S. Huang, D. Yang, S. Chen, Y. Jiang, Y. Hu, J. Cai, S. Liu, J. Luo _et al._ , “Genie envisioner: A unified world foundation platform for robotic manipulation,” _arXiv preprint arXiv:2508.05635_ , 2025. 

- [6] T. Jiang, Y. Guan, L. Ma, J. Xu, J. Meng, W. Chen, Z. Zeng, L. Li, D. Wu, and R. Chen, “Dexsim2real<sup>2</sup> : Building explicit world model for precise articulated object dexterous manipulation,” _IEEE Transactions on Robotics_ , 2025. 

- [7] D. Hafner, T. P. Lillicrap, M. Norouzi, and J. Ba, “Mastering atari with discrete world models,” in _International Conference on Learning Representations (ICLR)_ , 2021. 

- [8] M. Yang, Y. Du, K. Ghasemipour, J. Tompson, D. Schuurmans, and P. Abbeel, “Learning interactive real-world simulators,” _CoRR_ , 2023. 

- [9] J. Bruce, M. D. Dennis, A. Edwards, J. Parker-Holder, Y. Shi, E. Hughes, M. Lai, A. Mavalankar, R. Steigerwald, C. Apps, Y. Aytar, S. M. E. Bechtle, F. Behbahani, S. C. Chan, N. Heess, L. Gonzalez, S. Osindero, S. Ozair, S. Reed, J. Zhang, K. Zolna, J. Clune, N. de Freitas, S. Singh, and T. Rockt¨aschel, “Genie: Generative interactive environments,” in _Forty-first International Conference on Machine Learning (ICML)_ , 2024. 

- [10] L. Barcellona, A. Zadaianchuk, D. Allegro, S. Papa, S. Ghidoni, and E. Gavves, “Dream to manipulate: Compositional world models empowering robot imitation learning with imagination,” _arXiv preprint arXiv:2412.14957_ , 2024. 

- [11] S. Levine, C. Finn, T. Darrell, and P. Abbeel, “End-to-end training of deep visuomotor policies,” _Journal of Machine Learning Research_ , vol. 17, no. 39, pp. 1–40, 2016. 

- [12] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

- [13] T. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” _Robotics: Science and Systems XIX_ , 2023. 

- [14] Y. Tang, W. Huang, Y. Wang, C. Li, R. Yuan, R. Zhang, J. Wu, and L. Fei-Fei, “Uad: Unsupervised affordance distillation for generalization in robotic manipulation,” in _CoRL 2024 Workshop on Mastering Robot Manipulation in a World of Abundant Data_ , 2025. 

- [15] W. Yuan, J. Duan, V. Blukis, W. Pumacay, R. Krishna, A. Murali, A. Mousavian, and D. Fox, “Robopoint: A vision-language model for spatial affordance prediction in robotics,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 4005–4020. 

- [16] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 4573–4602. 

- [17] F. Liu, K. Fang, P. Abbeel, and S. Levine, “Moka: Open-vocabulary robotic manipulation through mark-based visual prompting,” _Robotics: Science and Systems XIX_ , 2024. 

- [18] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x- embodiment collaboration 0,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 6892–6903. 

- [19] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” in _International Conference on Learning Representations (ICLR)_ , 2020. 

- [20] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg, “Daydreamer: World models for physical robot learning,” in _Conference on robot learning (CoRL)_ . PMLR, 2023. 

- [21] OpenAI, “Gpt-4o system card,” 2024. 

- [22] T. Ren, S. Liu, A. Zeng, J. Lin, K. Li, H. Cao, J. Chen, X. Huang, Y. Chen, F. Yan, Z. Zeng, H. Zhang, F. Li, J. Yang, H. Li, Q. Jiang, and L. Zhang, “Grounded sam: Assembling open-world models for diverse visual tasks,” 2024. 

- [23] H. Fang, C. Wang, H. Fang, M. Gou, J. Liu, H. Yan, W. Liu, Y. Xie, and C. Lu, “Anygrasp: Robust and efficient grasp perception in spatial and temporal domains,” _IEEE Trans. Robotics_ , October 2023. 

- [24] Z. Zhao, Z. Lai, Q. Lin, Y. Zhao, H. Liu, S. Yang, Y. Feng, M. Yang, S. Zhang, X. Yang _et al._ , “Hunyuan3d 2.0: Scaling diffusion models for high resolution textured 3d assets generation,” _CoRR_ , 2025. 

- [25] M. Oquab, T. Darcet, T. Moutakanni, H. V. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. HAZIZA, F. Massa, A. El-Nouby, M. Assran, N. Ballas, W. Galuba, R. Howes, P.-Y. Huang, S.-W. Li, I. Misra, M. Rabbat, V. Sharma, G. Synnaeve, H. Xu, H. Je- 

gou, J. Mairal, P. Labatut, A. Joulin, and P. Bojanowski, “DINOv2: Learning robust visual features without supervision,” _Transactions on Machine Learning Research_ , 2024. 

- [26] X. Xu, W. Ge, D. Qiu, Z. Chen, D. Yan, Z. Liu, H. Zhao, H. Zhao, S. Zhang, J. Liang, and Y.-C. Chen, “Gaussianproperty: Integrating physical properties to 3d gaussians with lmms,” _arXiv preprint arXiv:2412.11258_ , 2024. 

