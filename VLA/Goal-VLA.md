---
title: "Goal-VLA: Image-Generative VLMs as Object-Centric World Models Empowering Zero-shot Robot Manipulation"
date: "2025-06-30"
authors: "Haonan Chen; Jingxiang Guo; Bangjun Wang; Tianrui Zhang; Xuchuan Huang; Boren Zheng"
venue: "ICRA 2026"
url: https://arxiv.org/abs/2506.23919
pdf: https://arxiv.org/pdf/2506.23919
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2506.23919)** / [論文ページ](https://arxiv.org/abs/2506.23919)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Goal-VLA: Image-Generative VLMs as Object-Centric World Models Empowering Zero-shot Robot Manipulation** 

Haonan Chen<sup>_∗_1</sup> , Jingxiang Guo<sup>_∗_1</sup> , Bangjun Wang<sup>2</sup> , Tianrui Zhang<sup>1</sup> , Xuchuan Huang<sup>3</sup> , Boren Zheng<sup>4</sup> , Yiwen Hou<sup>1</sup> , Chenrui Tie<sup>1</sup> , Jiajun Deng<sup>1</sup> , Lin Shao<sup>_†_1</sup> 


Fig. 1: **Goal-VLA** maps a single-view RGB-D image and a language instruction to executable manipulation actions. Our approach employs an object-centric world model to generate a goal image, from which the corresponding object transformation is subsequently computed, enabling zero-shot manipulation. This overcomes key limitations of previous methods, which often either rely on paired action data for training or lack precise spatial reasoning. We demonstrate our framework’s strong performance and generalization capabilities across both simulated and real-world experiments. 

**_Abstract_ — Generalization remains a fundamental challenge in robotic manipulation. To tackle this challenge, recent VisionLanguage-Action (VLA) models build policies on top of VisionLanguage Models (VLMs), seeking to transfer their openworld semantic knowledge. However, their zero-shot capability lags significantly behind the base VLMs, as the instructionvision-action data is too limited to cover diverse scenarios, tasks, and robot embodiments. In this work, we present GoalVLA, a zero-shot framework that leverages Image-Generative VLMs as world models to generate desired goal states, from which the target object pose is derived to enable generalizable manipulation. The key insight is that object state representation is the golden interface, naturally separating a manipulation system into high-level and low-level policies. This representation abstracts away explicit action annotations, allowing the use of highly generalizable VLMs while simultaneously providing spatial cues for training-free low-level control. To further improve robustness, we introduce a Reflection-through-Synthesis process that iteratively validates and refines the generated goal image before execution. Both simulated and real-world experiments demonstrate that our Goal-VLA achieves strong performance and inspiring generalizability in manipulation tasks. Supplementary materials are available at https://nus-linslab.github.io/goalvlaweb/.** 

* denotes equal contribution; _†_ denotes the corresponding author. 

> 1School of Computing, National University of Singapore; 2The HKU Musketeers Foundation Institute of Data Science, The University of Hong Kong;<sup>3</sup> Yuanpei College, Peking University;<sup>4</sup> Department of Automation, Tsinghua University. 

## I. INTRODUCTION 

Robotic manipulation is a long-standing topic for robotics and embodied AI [1]–[3]. It serves as a cornerstone for a wide range of applications in robotics, from household assistance and healthcare to manufacturing and logistics. Despite recent progress [4], methods that perform exceptionally well in specific settings often collapse under minor distributional shifts [5], [6] across environments, tasks, object categories, and robot embodiments. This fact makes robust generalization a valid problem and draws increasing research interest from the community. This generalization gap is the primary barrier hindering the practical deployment of autonomous robots in unstructured environments. 

Foundation models, pre-trained on vast datasets, have emerged as a promising direction to address this challenge. This progress has catalyzed the development of VisionLanguage-Action (VLA) models, a broad paradigm aiming to connect multimodal perception with robotic action. Two primary architectural approaches have emerged within the VLA paradigm: end-to-end and hierarchical. 

The end-to-end VLA approach is to train a single, largescale policy to map visual and language inputs to low-level robot actions directly. These models are either developed by finetuning existing Vision-Language Models (VLMs) [7]–[9] 

or by training high-capacity policies from the ground up on robotics data [10], [11]. While their architectures differ, both approaches share a common and significant challenge: their performance is contingent on massive paired instructionvision-action data. This data type is exceptionally costly and time-consuming to acquire in sufficient diversity [12], [13], which limits its generalization to novel tasks and scenarios. 

The hierarchical VLA approach, in contrast, aims to mitigate this intense data dependency. It decouples the problem using a VLM for high-level planning to generate an intermediate representation, guiding a separate lowlevel policy [14]–[16]. Yet, the design of the intermediate representation presents a critical dilemma. Sparse or symbolic representations, such as language descriptions and keypoints [14], [17]–[19], lack the precise geometric detail required for complex manipulation. In contrast, while dense visual representations like goal images provide rich information [20]–[23], they typically require the low-level policy to be explicitly trained on paired action data to interpret them, thus forfeiting the zero-shot objective. Other VLMgenerated guidance, like value maps, constraints, or reward functions [15], [16], [24], often suffers from significant inaccuracies, stemming from the inherent weakness of current VLMs in precise spatial reasoning. 

To ameliorate this problem, we develop our approach based on this key insight: Effective zero-shot generalization in a low-level policy requires explicit spatial guidance. However, the powerful VLMs serving as our high-level goal generator excel at semantic reasoning but perform worse at precise spatial reasoning. To this end, we propose a decoupled architecture that leverages the VLM as an objectcentric world model. Unlike traditional agent-centric world models [22], [25]–[27] that are tied to specific robot kinematics and thus limit cross-embodiment generalization, our world model focuses exclusively on the semantic goal in the image space. This allows a separate, dedicated spatial grounding module to handle the translation of this semantic goal into explicit spatial guidance of the object, playing to the strengths of each component. 

Formally, we introduce Goal-VLA, a zero-shot manipulation framework that employs an Image-Generative VLM to produce a goal image depicting the desired task outcome, functioning as an object-centric world model. This visual representation is translated into a precise target pose to direct a low-level policy. To evaluate and optimize the generated goal image, we incorporate a Reflection-through-Synthesis mechanism that assesses and iteratively refines the visual output. The target object state is then extracted from the refined goal image, and the goal pose is computed using feature matching and point cloud registration. This objectcentric representation is inherently generalizable across various tasks, environments, object categories, and robot embodiments. By providing an explicit object pose rich in spatial information, our framework effectively guides a low-level policy to perform manipulation tasks in a zero-shot manner. 

Our framework operates solely on a user’s task description and a single-view RGB-D input, requiring no prior scene 

knowledge such as pre-scanned maps or object meshes. We demonstrate its effectiveness on tasks in simulated and realworld settings, including _Pick and Place, Table Sweeping, Bottle Stand-Up, and Box Closing_ . Our approach consistently outperforms baseline methods, such as MOKA [19], VoxPoser [15], and MolmoAct [9], achieving higher success rates. Moreover, our pipeline does not require task-specific fine-tuning, highlighting its zero-shot generalization. 

To summarize, our key contributions are: 

- We introduce Goal-VLA, a decoupled hierarchical framework that leverages an Image-Generative VLM as a world model to generate goal object states, serving as the bridge between high-level semantic reasoning and low-level action control. 

- We propose an iterative refinement process, termed Reflection-through-Synthesis, where the generated goal is improved by synthesizing and overlaying a virtual image of the target object onto the current observation for visual inspection and improvement. 

- We demonstrate that Goal-VLA achieves inspiring zeroshot generalizability across diverse manipulation tasks, environments, object categories, and robot embodiments in both simulation and the real world, without requiring any task-specific finetuning. 

II. RELATED WORK 

TABLE I: Comparison of VLA Paradigms 

|**Category**|**Method**|**Future**<br>**State**<br>**Awareness**|**Inter-**<br>**mediate**<br>**Type**|**Training-**<br>**Free**<br>**Policy**|**Precise 3D**<br>**Spatial**<br>**Grounding**|
|---|---|---|---|---|---|
|**End-to-End**<br>**VLA**|RT-1/2 [10], [11],<br>OpenVLA [7],<br>_π_0 [28],<br>RDT-1B [8]|_×_|N/A|_×_|_×_|
||MolmoAct [9]|_×_|Depth &<br>Trajectory|_×_|✓|
||SayCan [14],<br>PaLM-E [18]|_×_|Symbolic<br>Skills|_×_|_×_|
|**Hierarchical**|Code as<br>Policies [17]|_×_|Code|_×_|_×_|
|**VLA**|ProgPrompt [29]|_×_|Programmatic<br>Plan|_×_|_×_|
||MOKA [19]|✓|Keypoints|✓|_×_|
||Rekep [16]|_×_|Keypoints|✓|_×_|
||IKER [24]|✓|Rewards|_×_|_×_|
||SUSIE [20]|✓|Subgoal<br>Images|_×_|_×_|
||VoxPoser [15]|_×_|3D Value<br>Maps|✓|_×_|
||3D-VLA [21]|✓|3D Scene|_×_|✓|
||**Goal-VLA**<br>**(Ours)**|✓|Object State|✓|✓|


_A. Foundation Models Paradigms for Robotic Manipulation_ 

Recent advances in foundation models have significantly influenced robotics, especially in robotic manipulation tasks, by leveraging LLMs and VLMs for high-level planning and decision-making [30]–[33]. A key development in this area is the Vision-Language-Action (VLA) model: a class of frameworks that maps multimodal inputs, typically visual observations and language instructions, to executable robot 

actions [31], [33]. Current research building on this concept can be broadly categorized into several main paradigms, which we compare in detail in Table I. 

**End-to-End Vision-Language-Action Models.** The first paradigm aims to build monolithic, end-to-end models that directly map visual and linguistic inputs to low-level robot actions. This approach includes methods that train large models from scratch, such as RT-1 [10] and RT-2 [11], as well as those that finetune pre-trained VLMs, like OpenVLA [7], RDT-1B [8], and MolmoAct [9]. While these models have impressive capabilities, their performance is fundamentally bottlenecked by the need for massive datasets of paired instruction-vision-action data. The high cost and complexity of collecting such data severely constrain their diversity, limiting the models’ zero-shot generalization. 

**Hierarchical Models with Intermediate Representations.** A second representative paradigm employs foundation models in a hierarchical structure. A high-level VLM is a planner in this setup, generating an intermediate representation to guide a separate low-level policy [34]. Therefore, the design of this intermediate representation is critical, defining the primary trade-offs within this paradigm. One line of work utilizes symbolic or sparse geometric representations. This includes selecting from a library of predefined skills [14], [18], generating executable code [17], [29], or defining tasks through a set of keypoints [19], [35]. While effective for structured tasks, the generalizability of these methods is often constrained by the limited scope of discrete skill sets or the insufficiency of sparse keypoints to capture complex object interactions. Other methods generate more explicit, dense visual guidance to provide richer context, such as subgoal images [20], [21] or videos [22], [36]. A significant drawback, however, is that the low-level policy typically needs to be trained to interpret these visual goals, which reintroduces a data dependency and undermines the objective of a truly zero-shot, training-free system. A third approach involves the VLM generating implicit spatial guidance, like value maps [15], constraints [16], or reward functions [24]. These methods require the VLM to ground its reasoning in 3D space, a capability that is often imprecise due to the inherent limitations of its spatial understanding. 

## _B. Reflection in Foundation Models_ 

Reflection mechanisms, which enable generative models to iteratively critique and refine their outputs, have recently attracted growing attention as a promising approach for enhancing robotic manipulation capabilities. In generative modeling, recent studies demonstrate that incorporating selffeedback or iterative critiques substantially improves the quality and coherence of generated outputs [37]–[39]. Notable examples include CritiqueLLM [40] and Idea2Img [41], which showcase how reflective feedback loops facilitate progressive refinement and correction of initial predictions. Extending these reflective approaches into robotics, several recent frameworks [42]–[44] integrate self-reflection into robotic task planning and action execution, enabling robotic agents to dynamically identify and correct errors, 

thereby progressively enhancing their performance during tasks. Moreover, additional studies have advanced this concept by incorporating multimodal reflection mechanisms, effectively bridging high-level cognitive reasoning with lowlevel motor control adjustments. This multimodal integration significantly improves robot robustness and adaptability, enabling robots to manage uncertainties better and effectively generalize across diverse manipulation scenarios and realworld conditions [45]–[47]. 

## III. METHOD 

The overall workflow of our framework is illustrated conceptually in Figure 2 and detailed procedurally in Algorithm 1. This section begins by formulating the problem and defining the inputs and outputs for each module of our hierarchical pipeline (Sec. III-A). We then detail the core components, starting with the Goal State Reasoning module, which interprets the user’s instruction to generate a visual goal state (Sec. III-B). Subsequently, the Spatial Grounding module takes this visual representation and computes a precise 3D transformation (Sec. III-C). Finally, we describe how the Low-level Policy uses this transformation to plan and execute the physical manipulation task (Sec. III-D). 

## _A. Problem Formulation_ 

Given a single-view RGBD image observation _O_ = ( _I ∈_ R<sup>_H×W ×_3</sup> _, D ∈_ R<sup>_H×W ×_1</sup> ), and a natural language task description _L_ , the objective is to generate an action sequence _{_ **_a_** _}i_ that completes the manipulation task described in _L_ . 

## **Algorithm 1** Goal-VLA Execution Framework 

**Require:** Initial observation _O_ = ( _I, D_ ), Language instruction _L_ , Initial End-effector pose _Pinit_ 

**Ensure:** Action sequence _{_ **_a_** _}i_ 

- 1: **procedure** GOAL-VLA( _O, L_ ) 

## **Stage 1: Goal State Reasoning** 

- 2: _Le ←_ EnhancePrompt( _I, L_ ) 

- # _— Reflection-through-Synthesis Loop —_ 

- 3: **for** _i_ = 1 **to** max ~~i~~ terations **do** 

- 4: _Icand_<sup>_′←_GenerateImage(</sup><sup>_I, Le_)</sup> 5: _Isynth ←_ SynthesizeOverlay( _I, Icand_<sup>_′_)</sup> 6: is ~~v~~ alid, _Lrevised ←_ Reflector( _Isynth, Le_ ) 7: **if** is ~~v~~ alid **then break** 8: **end if** 

- 9: _Le ←Lrevised_ 

- 10: **end for** 11: _I_<sup>_′_</sup> _, M, M_<sup>_′_</sup> _, D_<sup>_′_</sup> _←_ GenMask&Depth( _I, Icand_<sup>_′_)</sup> 

## **Stage 2: Spatial Grounding** 

- 12: ( _R, t_ ) _←_ ComputeTransform( _I, I_<sup>_′_</sup> _, D, D_<sup>_′_</sup> _, M, M_<sup>_′_</sup> ) 

## **Stage 3: Low-level Policy** 

- 13: _Pcontact ←_ DetermineContactPose( _O, M_ ) 

- 14: _Pgoal ←_ ApplyTransform(( _R, t_ ) _, Pcontact_ ) 15: _{_ **_a_** _}i ←_ MotionPlan( _Pinit, Pcontact, Pgoal_ ) 

- 16: **return** _{_ **_a_** _}i_ 

- 17: **end procedure** 


Fig. 2: Overview of the **Goal-VLA** framework, which decouples the manipulation pipeline into three stages: **(a) Goal State Reasoning:** A VLM generates a goal image from instructions and refines it for task feasibility, yielding a validated goal with image, mask, and depth. **(b) Spatial Grounding:** The object’s transformation is computed by feature matching and point cloud registration between the initial and goal states. **(c) Low-level Policy:** The gripper’s goal pose is derived by applying the object’s transformation to a contact pose, after which a motion planner generates the final trajectory for robot execution. 

The **Goal State Reasoning** receives an RGB image _I_ and a task description _L_ to produce a goal image _I_<sup>_′_</sup> _∈_ R<sup>_H×W ×_3</sup> and a goal metric depth map _D_<sup>_′_</sup> _∈_ R<sup>_H×W ×_1</sup> . The Goal State Reasoning module also generates the object masks for the initial and goal images, denoted as _M_ and _M_<sup>_′_</sup> . 

The **Spatial Grounding** is given with the initial and goal RGB images _I, I_<sup>_′_</sup> , real depth maps _D_ and goal metric depth _D_<sup>_′_</sup> , and object masks _M, M_<sup>_′_</sup> . The objective of this module is to compute the rotation _R ∈ SO_ (3) and translation _t ∈_ R<sup>3</sup> that maps the object from its initial pose to its goal pose. 

The **Low-level Policy** takes the current observation _O_ = ( _I, D_ ) and the mask _M_ as input, then outputs a sequence of actions _{_ **_a_** _}i_ to drive the system from _O_ to _O_<sup>_′_</sup> = ( _I_<sup>_′_</sup> _, D_<sup>_′_</sup> ). 

_B. Goal State Reasoning_ 

The Goal State Reasoning module is responsible for translating the user’s abstract language instruction ( _L_ ) into a concrete and plausible visual goal, represented by a goal image ( _I_<sup>_′_</sup> ) and a goal depth map ( _D_<sup>_′_</sup> ). This is achieved through an initial prompt enhancement step and an iterative refinement loop we term Reflection-through-Synthesis. 

Before the image generation process, we enhance the user’s raw instruction to make it more descriptive for the image generation model. The initial image _I_ and the raw task description _L_ are fed into a text-output VLM (e.g., Gemini 2.5 Pro). This model enriches the concise instruction with critical details inferred from the visual context, producing a more descriptive enhanced prompt. 

**The Reflection-through-Synthesis Loop:** This enhanced prompt then seeds our iterative refinement loop, which 

generates and validates candidate goals until one is deemed successful. Each iteration involves the following steps: 

- **Goal Image Generation:** The current prompt and the initial image _I_ are passed to a pre-trained image generation VLM (Gemini 2.5 Flash-image, also known as Nano Banana) to produce a candidate goal image. 

- **Synthesis for Inspection:** We construct a synthesized image to provide the Reflector VLM with a clear basis for evaluation. Using Grounded SAM [48], we segment the target object from the candidate goal and overlay this “virtual image” onto the initial scene with partial transparency. This overlay is crucial as it provides an in-context visualization of the goal, which mitigates the semantic gap and enables a more robust evaluation. 

- **Reflection and Refinement:** The synthesized image, along with the original instruction and the current enhanced prompt, is fed to a **Reflector VLM** (Gemini 2.5 Pro). The Reflector assesses if the synthesized outcome aligns with the task’s semantic requirements. If successful, the loop terminates. If not, the Reflector generates a revised prompt containing corrective feedback, which is used for the next generation iteration. 

This process continues until the Reflector validates a goal image or a pre-set maximum number of attempts is reached. Once a goal image is accepted, the final outputs for the next module are generated: a depth estimation model (DepthAnything V2 [49]) produces the goal’s relative depth map. At the same time, Grounded SAM [48] extracts the target object masks for both the initial and final goal images. 

## _C. Spatial Grounding_ 

The Spatial Grounding module consists of two main stages: **semantic matching** and **point-cloud registration** . 

**Semantic Matching.** Given the initial observation _I ∈_ R<sup>_H×W ×_3</sup> and the goal image _I_<sup>_′_</sup> _∈_ R<sup>_H×W ×_3</sup> , our goal is to obtain a pixel matching _F_ : ( _x, y_ ) _→_ ( _x_<sup>_′_</sup> _, y_<sup>_′_</sup> ), which maps pixel in the initial image _I_ to the corresponding pixel in the goal image _I_<sup>_′_</sup> . Since the goal image synthesized by the generative VLM is semantically correct but may not preserve the instance-level appearance of the original object, traditional methods like optical flow estimation or 2D pixel tracking yield unreliable results. Therefore, we utilize semantic features to generate robust pixel matching. Based on the existing semantic matching model Geo-Aware [50], we extract pixel-wise semantic features **f** _,_ **f**<sup>_′_</sup> from _I_ , _I_<sup>_′_</sup> , respectively. Furthermore, we match pixels between the two frames by pairing the pixel in _I_ with the pixel yielding the highest cosine similarity among all pixels in _I_<sup>_′_</sup> , i.e. 


**Point-cloud Registration.** Following the establishment of 2D correspondences, this stage computes the 3D spatial transformation. The process involves lifting the 2D images to 3D point clouds using depth information. While a groundtruth depth map _D_ is available for the initial frame, the depth map for the generated goal, _D_<sup>_′_</sup> , is estimated using the DepthAnythingV2 model. 

To align these different scales, we first perform depth alignment. A linear transformation, characterized by a scale factor _s_ 1 and a bias _b_ , is calibrated to map the predicted depth scale of _D_<sup>_′_</sup> to the metric scale of _D_ . This transformation is determined via the method of least squares: 


The regression is performed exclusively on background pixels, denoted by the complement set ( _M ∪M_<sup>_′_</sup> )<sup>_c_</sup> , to ensure manipulated foreground objects do not skew the alignment. The learned parameters are then applied to the entire predicted depth map to yield a correctly scaled version, 


Subsequently, object-specific point clouds, _P_ and _P_<sup>_′_</sup> , are extracted from the initial and goal frames by applying object masks _M_ and _M_<sup>_′_</sup> to the depth maps _D_ and _D_ rescaled<sup>_′_,</sup> respectively. Specifically, we use the pixel matching _F_ to establish a set of corresponding point pairs, which are then filtered to remove those with negligible changes in distance. To robustly account for scale differences in the generated goal, we solve for a similarity transformation between the two point clouds: 


where _R_ stands for the rotation; _t_ stands for translation and _s_ 2 is the scale factor of the transformation, respectively. The optimal scale _s_ 2, rotation _R_ and translation _t_ are 

computed using the Umeyama algorithm [51]. These final parameters, representing the precise spatial transformation, are then utilized by a low-level policy module to guide robot actions. 

## _D. Low-level Policy_ 

The **Low-level Policy** translates the object goal pose, provided by the high-level modules, into executable robot actions. This process involves three stages: determining an initial contact point on the object, computing the gripper’s final goal pose, and planning a valid trajectory. A key advantage of our framework’s object-centric representation is its flexibility; it provides an explicit geometric target and is compatible with various low-level controllers operating on different input modalities (e.g., RGB images or point clouds). 

**Contact Module.** The Contact Module determines a feasible contact pose using a multi-stage, sample-based method on the object’s point cloud. First, a large set of contact pose candidates is generated on the object’s surface, oriented along local surface normals. This set is then pruned through filters that check for valid orientation and perform collision checks using a robot’s end-effector geometry against the scene. Finally, the remaining collision-free candidates are scored based on task-relevant geometric heuristics, and the top-scoring pose is selected as the initial contact pose for subsequent planning. 

**Goal Pose Computing.** We assume that the relative pose between the gripper and the object remains constant after contact. This assumption holds for most prehensile actions and a subset of non-prehensile tasks. Based on this, we calculate the gripper’s goal pose by applying the object’s transformation, as determined by the Spatial Grounding module, to the gripper’s initial pose. This provides the target configuration for motion planning. 

**Motion Planning Module.** Finally, the Motion Planning Module generates a collision-free trajectory for the manipulator from its current configuration to the target pose. In our simulated experiments, we leverage a built-in samplebased planner [52] to interpolate the trajectory. We utilized a sample-based motion planner in the real-world experiment to generate a feasible path in the robot’s configuration space. 

## IV. EXPERIMENT 

In this section, we conduct comprehensive experiments and analyses to answer the following key questions: 

- Q1: How well does our proposed method perform compared to existing baselines? 

- Q2: How effective is the Reflection-through-Synthesis process in refining the outputs of the high-level reasoning? 

- Q3: Can our framework generalize across diverse environments, tasks, object categories, and robot embodiments? 

## _A. Experimental Setup_ 

**Simulation.** Our simulation experiments are conducted in RLBench [52], utilizing a Franka Emika Panda 7-DoF arm with attached RGB-D cameras. The robot arm is fixed to a tabletop, and for each task, objects are placed in randomized 

TABLE II: Results of Simulation Experiments. All methods are evaluated in a zero-shot setting. 

|Method|Pick Up<br>Cup|Open Wine<br>Bottle|Put Shoe<br>On Box|Take Plate<br>Off Dish Rack|Take Frame<br>Off Hanger|Plug Charger<br>In Supply|Place Cup<br>on Cabinet|Close<br>Box|Average<br>Success Rate|
|---|---|---|---|---|---|---|---|---|---|
|OpenVLA|0/100|2/100|0/100|0/100|0/100|0/100|0/100|0/100|0.2%|
|Pi0|0/100|0/100|0/100|0/100|0/100|0/100|0/100|0/100|0.0%|
|SUSIE|0/100|0/100|0/100|0/100|0/100|0/100|0/100|0/100|0.0%|
|MOKA|62/100|55/100|33/100|21/100|17/100|8/100|0/100|24/100|26.0%|
|VoxPoser|20/100|24/100|0/100|0/100|2/100|0/100|0/100|0/100|5.8%|
|MomolAct|20/100|10/100|40/100|0/100|0/100|20/100|0/100|0/100|11.3%|
|**Ours**|93/100|100/100|70/100|55/100|67/100|33/100|25/100|36/100|59.9%|


initial configurations determined by a random seed. We select eight representative tasks from the RLBench benchmark to evaluate a range of manipulation skills, with the complete list and setup details provided in Table II. In all experiments, the robot starts without holding any object at the beginning of each trial. 

To robustly assess performance and account for variations in object placement, each task is evaluated across 10 random seeds. For each seed, which defines a unique initial scene arrangement, we conduct 10 independent trials of each method, resulting in 100 evaluation runs per task for calculating the success rate. 

**Real World.** Our real-world experimental setup comprises a 7-DoF UFACTORY X-ARM 7 and an Orbbec Femto Bolt RGB-D camera. We design four distinct real-world tasks to evaluate a range of core manipulation capabilities: _Place Tomato in Pan_ , a foundational pick-and-place task requiring reasoning about object containment; _Table Sweeping_ , which involves tool use and non-prehensile manipulation; _Weigh the Duck_ , a task demanding precise placement onto a small target; and _Stand a Bottle Upright_ , which tests object reorientation. We conduct 10 trials for each task, with detailed results presented in Table III and Figure 5. 

For detailed descriptions of our simulation and real-world tasks, please refer to the Appendix B and C. 

## _B. Baselines_ 

We evaluate our method against representative baselines from the two primary paradigms discussed in our related work: end-to-end and hierarchical. Our selection is designed to rigorously test our approach against the main competing strategies in robotic manipulation. 

For the end-to-end paradigm, we select OpenVLA [7], Pi0 [28], and MolmoAct [9]. These models are typical examples of the end-to-end VLA approach that directly maps multimodal inputs to robot actions. 

We choose a diverse set of methods for the hierarchical paradigm to evaluate the efficacy of different intermediate representations. Our selection includes: VoxPoser [15] (value maps), SUSIE [20] (subgoal images), and MOKA [19] (keypoints), covering a broad spectrum of representations, from implicit spatial guidance to explicit visual targets. 

All of our comparative evaluations are conducted under a strict zero-shot protocol, which means neither our method nor the baselines undergo any task-specific fine-tuning. 

## _C. Simulation Experiments (Q1)_ 

The results of our simulation experiments are presented in Table II. Our method, **Goal-VLA** , achieves a remarkable average success rate of 59.9%, significantly outperforming all baselines across a diverse set of eight manipulation tasks. 

The end-to-end baselines, OpenVLA and Pi0, fail almost completely (0.2% and 0% success rates, respectively), highlighting their brittleness in this zero-shot setting due to a strong dependency on large-scale, in-domain action data. Performance within the hierarchical paradigm was varied but limited by the intermediate representation. While methods using keypoints (MOKA, 26.0%) or trajectories (MomolAct, 11.3%) show some capability, their performance lags significantly behind that of our approach. This suggests a fundamental weakness in the baselines’ intermediate representations. Unlike our explicit 3D pose, their representations either lack sufficient spatial precision or necessitate taskspecific training for the low-level policy. 

These findings decisively answer our first research question (Q1). While other methods falter due to data dependency or imprecise goals, Goal-VLA’s explicit goal object state provides the necessary precision and robustness for a lowlevel policy to succeed. 

## _D. Ablation Study (Q2)_ 

We perform an ablation study to validate the contributions of our two key components: Input Enhancement and the Reflection-through-Synthesis process. 

**Reflection’s Necessary:** Figure 3 highlights a typical failure mode of image generation. Image-Generative VLM may 


Fig. 3: An example of our **Reflection-through-Synthesis** process, which corrects a semantically correct but infeasible goal by refining the generation prompt. 


Fig. 4: Ablation Study. The performance of our full model (”World Model w/ Instruction & max 3 Reflection”), shown by the purple line, surpasses all ablated variants. 

alter non-target elements (e.g., moving the pan along with the tomato), creating a semantically plausible but physically incorrect goal. Our **synthesis** step, overlaying the segmented target object onto the original scene, grounds the reflection in the world context. This allows our Reflector VLM to identify such errors and provide corrective feedback effectively. 

**Analysis:** The results in Figure 4 quantify the impact of each component. Starting from a 40.0% success rate for the baseline model, adding Input Enhancement provides the most significant single improvement (+27.5pp), while the Reflector alone yields a substantial gain (+11.2pp). Our complete model, which combines both, performs best, and its success can be further boosted from 83.8% to 88.8% by increasing the maximum reflection iterations from 1 to 3. 

These results demonstrate that both components are critical and complementary, confirming their effectiveness and answering our second research question (Q2). 

## _E. Real World Experiments (Q3)_ 

Our framework is tested on four diverse real-world manipulation tasks to validate its practical applicability. As shown in Table III, our method achieves a 60% average success rate, significantly outperforming baselines like MOKA (22.5%) and MolmoAct (27.5%). Consistent with the simulation findings, the end-to-end model OpenVLA fails (0%). These results further highlighting our generalization ability. 

TABLE III: Real World Experiments 

|Mhd|Tomato|Table|Weighing|Bottle|Average|
|---|---|---|---|---|---|
|eto|Placement|Sweeping|Duck|Stand-Up|Success Rate|
|OpenVLA|0/10|0/10|0/10|0/10|0%|
|MOKA|5/10|1/10|3/10|0/10|22.5%|
|MolmoAct|5/10|0/10|6/10|0/10|27.5%|
|**Ours**|9/10|4/10|7/10|4/10|60%|


Figure 5 provides qualitative evidence for these findings. The visualizations illustrate how the generated goal image captures the task’s intent, and the subsequent transformation provides a precise spatial target, enabling the robot to execute complex tasks in a robust, zero-shot manner. 

The framework’s success across diverse tasks, objects, and environments (simulated and real), combined with its zeroshot deployment on different robot embodiments, demonstrates strong generalization, providing a clear answer to Q3. 

## _F. Failure Cases Analysis_ 

In our real-world experiments, we observe several typical failure modes as different tasks place varying demands on each module of our framework. 

Failures originating from the Spatial Grounding module are the primary obstacle in several precision-demanding tasks. For _Tomato Placement_ and _Weighing Duck_ , this manifests as inaccuracies in the estimated depth, with the latter task being sensitive to minor height errors. Similarly, the _Bottle Stand-Up_ task’s success is contingent on orientation precision, where even minor inaccuracies in the computed orientation from this module may lead to failure. 

In contrast, the primary difficulty in the _Table Sweeping_ task shifts to the High-level Reasoning module. Generating a goal image representing a practical and feasible sweeping motion demands a sophisticated semantic understanding, and occasional failures occur at this reasoning stage. 

## V. CONCLUSION 

In this work, we introduce **Goal-VLA** , a hierarchical manipulation framework designed to address the critical challenge of zero-shot generalization. Our key contribution is a decoupled architecture where a high-level generative VLM, acting as an object-centric world model, envisions a visual goal state. This visual goal is iteratively refined for plausibility and accuracy through our novel Reflection-throughSynthesis mechanism. Crucially, this visual representation is 

translated into a precise 3D object pose, which serves as an explicit, training-free guide for a separate low-level policy. This design ensures the entire manipulation process, from semantic reasoning to physical execution, is performed in a zero-shot setting, eliminating any requirement for action data or task-specific finetuning. Our extensive evaluations in both simulation and the real world demonstrate that Goal-VLA significantly surpasses existing end-to-end and hierarchical baselines across various manipulation tasks, highlighting its strong generalization and cross-embodiment capabilities. 

## REFERENCES 

- [1] Z. Xu, K. Wu, J. Wen, J. Li, N. Liu, Z. Che, and J. Tang, “A survey on robotics with foundation models: toward embodied ai,” _arXiv preprint arXiv:2402.02385_ , 2024. 1 

- [2] Y. Liu, W. Chen, Y. Bai, X. Liang, G. Li, W. Gao, and L. Lin, “Aligning cyber space with physical world: A comprehensive survey on embodied ai,” _arXiv preprint arXiv:2407.06886_ , 2024. 1 

- [3] Z. Xian, T. Gervet, Z. Xu, Y.-L. Qiao, T.-H. Wang, and Y. Wang, “Towards generalist robots: A promising paradigm via generative simulation,” _arXiv preprint arXiv:2305.10455_ , 2023. 1 

- [4] R. Shao, W. Li, L. Zhang, R. Zhang, Z. Liu, R. Chen, and L. Nie, “Large vlm-based vision-language-action models for robotic manipulation: A survey,” _arXiv preprint arXiv:2508.13073_ , 2025. 1 

- [5] N. Roy, I. Posner, T. Barfoot, _et al._ , “From machine learning to robotics: Challenges and opportunities for embodied intelligence,” _arXiv preprint arXiv:2110.15245_ , 2021. 1 

- [6] O. Kroemer, S. Niekum, and G. Konidaris, “A review of robot learning for manipulation: Challenges,” _Found. Trends Mach. Learn._ , 2019. 1 

- [7] M. J. Kim, K. Pertsch, S. Karamcheti, _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 3, 6 

- [8] S. Liu, L. Wu, B. Li, _et al._ , “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _arXiv:2410.07864_ , 2024. 1, 2, 3 

- [9] J. Lee, J. Duan, H. Fang, _et al._ , “Molmoact: Action reasoning models that can reason in space,” _arXiv:2508.07917_ , 2025. 1, 2, 3, 6 

- [10] A. Brohan, N. Brown, J. Carbajal, _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 2, 3 

- [11] B. Zitkovich, T. Yu, S. Xu, _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 2, 3 

- [12] J. Yang, W. Tan, C. Jin, _et al._ , “Transferring foundation models for generalizable robotic manipulation,” in _WACV_ . IEEE, 2025. 2 

- [13] A. O’Neill, A. Rehman, A. Maddukuri, _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0,” in _ICRA_ , 2024, pp. 6892–6903. 2 

- [14] M. Ahn, A. Brohan, N. Brown, _et al._ , “Do as i can, not as i say: Grounding language in robotic affordances,” _arXiv preprint arXiv:2204.01691_ , 2022. 2, 3 

- [15] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language models,” _arXiv preprint arXiv:2307.05973_ , 2023. 2, 3, 6 

- [16] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation,” _arXiv preprint arXiv:2409.01652_ , 2024. 2, 3 

- [17] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence, and A. Zeng, “Code as policies: Language model programs for embodied control,” in _ICRA_ . IEEE, 2023, pp. 9493–9500. 2, 3 

- [18] D. Driess, F. Xia, and M. S. M. o. Sajjadi, “Palm-e: An embodied multimodal language model,” in _ICML_ , vol. 202. PMLR, 2023, pp. 8469–8488. 2, 3 

- [19] F. Liu, K. Fang, P. Abbeel, and S. Levine, “Moka: Open-vocabulary robotic manipulation through mark-based visual prompting,” in _ICRA Workshop_ , 2024. 2, 3, 6 

- [20] K. Black, M. Nakamoto, P. Atreya, H. Walke, C. Finn, A. Kumar, and S. Levine, “Zero-shot robotic manipulation with pretrained imageediting diffusion models,” _arXiv:2310.10639_ , 2023. 2, 3, 6 

- [21] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: A 3d vision-language-action generative world model,” _arXiv preprint arXiv:2403.09631_ , 2024. 2, 3 

- [22] J. Wu, S. Yin, N. Feng, X. He, D. Li, J. Hao, and M. Long, “ivideogpt: Interactive videogpts are scalable world models,” _NeurIPS_ , vol. 37, pp. 68 082–68 119, 2024. 2, 3 

- [23] A. Stone, T. Xiao, Y. Lu, _et al._ , “Open-world object manipulation using pre-trained vision-language models,” _arXiv preprint arXiv:2303.00905_ , 2023. 2 

- [24] S. Patel, X. Yin, W. Huang, S. Garg, H. Nayyeri, L. Fei-Fei, S. Lazebnik, and Y. Li, “A real-to-sim-to-real approach to robotic manipulation with vlm-generated iterative keypoint rewards,” _arXiv preprint arXiv:2502.08643_ , 2025. 2, 3 

- [25] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” _arXiv preprint arXiv:1912.01603_ , 2019. 2 

- [26] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg, “Daydreamer: World models for physical robot learning,” in _CoRL_ . PMLR, 2023, pp. 2226–2240. 2 

- [27] C. Zhu, R. Yu, S. Feng, B. Burchfiel, P. Shah, and A. Gupta, “Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets,” _arXiv preprint arXiv:2504.02792_ , 2025. 2 

- [28] K. Black, N. Brown, D. Driess, _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” 2024. [Online]. Available: https://arxiv.org/abs/2410.24164 2, 6 

- [29] I. Singh, V. Blukis, A. Mousavian, A. Goyal, D. Xu, J. Tremblay, D. Fox, J. Thomason, and A. Garg, “Progprompt: Generating situated robot task plans using large language models,” _arXiv preprint arXiv:2209.11302_ , 2022. 2, 3 

- [30] R. Firoozi, J. Tucker, S. Tian, _et al._ , “Foundation models in robotics: Applications, challenges, and the future,” _IJRR_ , vol. 44, no. 5, pp. 701–739, 2025. 2 

- [31] Y. Ma, Z. Song, Y. Zhuang, J. Hao, and I. King, “A survey on vision-language-action models for embodied ai,” _arXiv preprint arXiv:2405.14093_ , 2024. 2, 3 

- [32] C. Tie, S. Sun, J. Zhu, _et al._ , “Manual2skill: Learning to read manuals and acquire robotic skills for furniture assembly using vision-language models,” _arXiv preprint arXiv:2502.10090_ , 2025. 2 

- [33] Y. Zhong, F. Bai, S. Cai, _et al._ , “A survey on vision-languageaction models: An action tokenization perspective,” _arXiv preprint arXiv:2507.01925_ , 2025. 2, 3 

- [34] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao, “React: Synergizing reasoning and acting in language models,” in _ICLR_ , 2023. 3 

- [35] Y. Mikami, A. Melnik, J. Miura, and V. Hautam¨aki, “Natural language as policies: Reasoning for coordinate-level embodied control with llms,” _arXiv preprint arXiv:2403.13801_ , 2024. 3 

- [36] H. Bharadhwaj, D. Dwibedi, A. Gupta, _et al._ , “Gen2act: Human video generation in novel scenarios enables generalizable robot manipulation,” _arXiv preprint arXiv:2409.16283_ , 2024. 3 

- [37] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Reflexion: Language agents with verbal reinforcement learning,” _NeurIPS_ , vol. 36, pp. 8634–8652, 2023. 3 

- [38] A. Madaan, N. Tandon, P. Gupta, _et al._ , “Self-refine: Iterative refinement with self-feedback,” _NeurIPS_ , vol. 36, 2023. 3 

- [39] S. S. Raman, V. Cohen, I. Idrees, E. Rosen, R. Mooney, S. Tellex, and D. Paulius, “Cape: Corrective actions from precondition errors using large language models,” in _ICRA_ . IEEE, 2024, pp. 14 070–14 077. 3 

- [40] P. Ke, B. Wen, Z. Feng, _et al._ , “Critiquellm: Towards an informative critique generation model for evaluation of large language model generation,” _arXiv preprint arXiv:2311.18702_ , 2023. 3 

- [41] Z. Yang, J. Wang, L. Li, K. Lin, C.-C. Lin, Z. Liu, and L. Wang, “Idea2img: Iterative self-refinement with gpt-4v for automatic image design and generation,” in _ECCV_ . Springer, 2024, pp. 167–184. 3 

- [42] Z. Wang, S. Cai, G. Chen, A. Liu, X. Ma, and Y. Liang, “Describe, explain, plan and select: Interactive planning with large language models enables open-world multi-task agents,” _arXiv preprint arXiv:2302.01560_ , 2023. 3 

- [43] Y. Feng, J. Han, Z. Yang, X. Yue, S. Levine, and J. Luo, “Reflective planning: Vision-language models for multi-stage long-horizon robotic manipulation,” _arXiv preprint arXiv:2502.16707_ , 2025. 3 

- [44] Z. Yang, C. Garrett, D. Fox, T. Lozano-P´erez, and L. P. Kaelbling, “Guiding long-horizon task and motion planning with vision language models,” _arXiv preprint arXiv:2410.02193_ , 2024. 3 

- [45] C. Li, J. Liu, G. Wang, _et al._ , “A self-correcting vision-languageaction model for fast and slow system manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2405.17418 3 

- [46] C. Xiong, C. Shen, X. Li, K. Zhou, J. Liu, R. Wang, and H. Dong, “Aic mllm: Autonomous interactive correction mllm for robust robotic manipulation,” _arXiv preprint arXiv:2406.11548_ , 2024. 3 

- [47] W. Xia, R. Feng, D. Wang, and D. Hu, “Phoenix: A motion-based self-reflection framework for fine-grained robotic action correction,” _arXiv preprint arXiv:2504.14588_ , 2025. 3 

- [48] T. Ren, S. Liu, A. Zeng, _et al._ , “Grounded sam: Assembling open-world models for diverse visual tasks,” _arXiv preprint arXiv:2401.14159_ , 2024. 4 

- [49] L. Yang, B. Kang, Z. Huang, X. Xu, J. Feng, and H. Zhao, “Depth anything: Unleashing the power of large-scale unlabeled data,” in _CVPR_ , 2024, pp. 10 371–10 381. 4 

- [50] J. Zhang, C. Herrmann, J. Hur, E. Chen, V. Jampani, D. Sun, and M.H. Yang, “Telling left from right: Identifying geometry-aware semantic correspondence,” in _CVPR_ , 2024. 5 

- [51] S. Umeyama, “Least-squares estimation of transformation parameters between two point patterns,” _IEEE Transactions on pattern analysis and machine intelligence_ , vol. 13, no. 4, pp. 376–380, 2002. 5 

- [52] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _IEEE RA-L_ , vol. 5, no. 2, pp. 3019–3026, 2020. 5 

## APPENDIX 

## _A. Acknowledgements of the Use of AI_ 

The research presented in this paper incorporates several publicly available foundation models as components within our framework. These models are utilized for various functions, including generative image synthesis, semantic evaluation, object segmentation, and depth generation. 

In addition to their role as research components, AIpowered tools assist in the preparation of this manuscript and its associated code. We use a large language model (Gemini, Google; accessed Aug–Sep 2025) for grammar correction and to improve text clarity. AI-assisted coding tools, such as Cursor, are employed during development. All code generated with AI assistance is manually reviewed and rigorously tested by the authors. 

The authors take full responsibility for the content and conclusions of this work. 

## _B. Simulation Task Description_ 

The simulation experiments are conducted on a suite of eight challenging manipulation tasks from RLBench. These tasks include: _Pick Up Cup_ , which involves grasping a cup and lifting it; _Open Wine Bottle_ , which requires the gripper to directly grasp the bottle cap and pull it off the bottle’s opening; _Put Shoe On Box_ , picking up a shoe and placing it onto a box; _Take Plate Off Dish Rack_ , lifting a plate from a rack; _Take Frame Off Hanger_ , lifting the picture frame along the contour of the hanger to disengage it; _Plug Charger In Supply_ , plugging a charger into a power socket; _Place Cup on Cabinet_ , picking up a cup and setting it onto a cabinet; and _Close Box_ , manipulating a lid to close a box. For the ”Pick Up” and ”Take...Off” tasks, success is achieved as soon as the object is lifted clear from its supporting surface (e.g., the table or rack). In contrast, the ”Put...On” and ”Place...on” tasks require the robot to first successfully grasp the target object and then transport it to the specified goal location before releasing it. 

## _C. Real World Task Description_ 

The _Tomato Placement_ task requires the robot to pick up a tomato from its initial location and place it inside a pan, where the tomato must rest stably within the pan without rolling out. In the _Table Sweeping_ task, the robot should utilize a brush to sweep several screws scattered on a tabletop into a designated dustpan. The _Weighing Duck_ task requires the robot to pick up a toy duck and place it accurately onto a weighing scale’s platform such that it remains stable for a consistent weight reading. _Bottle Stand-Up_ is a re-orientation task where the robot must grasp a bottle lying horizontally and set it in a stable, upright position. 

