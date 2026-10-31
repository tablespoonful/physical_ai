---
title: "CulinaryCut-VLAP: A Vision-Language-Action-Physics Framework for Food Cutting via a Force-Aware Material Point Method"
date: "2026-01-10"
authors: "Hyunseo Koh; Chang-Yong Song; Youngjae Choi; Misa Viveiros; David Hyde; Heewon Kim"
url: https://arxiv.org/abs/2601.06451
pdf: https://arxiv.org/pdf/2601.06451
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.06451)** / [論文ページ](https://arxiv.org/abs/2601.06451)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CulinaryCut-VLAP: A Vision–Language–Action–Physics Framework for Food Cutting via a Force-Aware Material Point Method** 

Hyunseo Koh<sup>1</sup> Chang-Yong Song<sup>2</sup> Youngjae Choi<sup>1</sup> Misa Viveriros<sup>2</sup> 

David H <mark>yde</mark><sup>2</sup> Heewon Kim<sup>1</sup> 

1Soongsil University 2Vanderbilt University 

_{_ deepvelop, yj951118, hwkim _}_ @soongsil.ac.kr 

_{_ chang-yong.song, misa.h.viveiros, david.hyde.1 _}_ @vanderbilt.edu 

## **Abstract** 

_Food cutting is a highly practical yet underexplored application at the intersection of vision and robotic manipulation. The task remains challenging because interactions between the knife and deformable materials are highly nonlinear and often entail large deformations, frequent contact, and topological change, which in turn hinder stable and safe large-scale data collection. To address these challenges, we propose a unified framework that couples a vision-language-action (VLA) dataset with a physically realistic cutting simulator built on the material point method (MPM). Our simulator adopts MLS-MPM_ _<mark>as its compu-</mark> tational core, reducing numerical dissipation and energy drift while preserving rotational and shear responses even under topology-changing cuts. During cutting, forces and stress distributions are estimated from impulse exchanges between particles and the grid, enabling stable tracking of transient contact forces and energy transfer. We also provide a benchmark dataset that integrates diverse cutting trajectories, multi-view visual observations, and fine-grained language instructions, together with force–torque and tool– pose labels to provide physically consistent training signals. These components realize a learning–evaluation loop that respects the core physics of cutting and establishes a safe, reproducible, and scalable foundation for advancing VLA models in deformable object manipulation._ 

## **1. Introduction** 

Interest in vision-based robotic manipulation [27, 34] has grown rapidly with advances in low-cost vision sensors, sim-to-real learning [64], and the integration of perception [61], language [40], and control [39]. Recent VLA models [4, 27, 69] unify these components into a single lan- 


Figure 1. Concept of the Vision–Language–Action-Physics (VLAP) framework. The framework interacts between the robot and physics simulation to construct a physically grounded VLA dataset and model for food cutting. 

guage→perception→action <mark>pipe</mark> line trained under physical constraints [66], enabling operation in grounded environments. 

Despite this progress, food cutting remains largely unexplored in VLA research. Cutting tasks involve deformation, fracture, and force-mediated contact—phenomena [14] that rigid-body manipulation datasets fail to capture. Existing approaches rely either on real robot data, which ensures physical realism but limits scale, or on geometry-focused simulations [55] that do not directly leverage forces and impulses, which can potentially limit physical accuracy. 

Constructing a dataset suitable for VLA-based food cut- 

1 

|**Dataset**|**Physics**<br>**Sim**|**Robot**<br>**Sim**|**Data**<br>**Origin**|**Multi**<br>**Camera**|**Language**<br>**Intruction**|**Continuous**<br>**Action**|**Cutting**<br>**Flexibility**|**Cutting**<br>**Task**|**Multiple cut**<br>**Style**|**Force**<br>**Data**|
|---|---|---|---|---|---|---|---|---|---|---|
|DROID [25]|N/A|N/A|Real|✓|✓|✓|✗|✗|✗|✗|
|FMB [36]|N/A|N/A|Real|✓|✗|✗|✗|✗|✗|✗|
|Playing with Food [45]|N/A|N/A|Real|✓|✗|✗|✗|✗|✗|✗|
|MimicPlay [54]|N/A|MuJoCo|Real|✓|✗|✓|✗|✗|✗|✗|
|Mutex [46]|N/A|N/A|Real|✓|✗|✓|✗|✗|✗|✗|
|FurnitureBench [15]|N/A|IsaacGym [38]|Real|✓|✗|✗|✗|✗|✗|✗|
|Arnold [13]|N/A|IssacSim|Synthetic|✓|✗|✓|✗|✗|✗|✗|
|Robomind[59]|N/A|IssacSim|Synthetic|✓|✗|✓|✗|✗|✗|✗|
|RoboChop [9]|N/A|N/A|Real|✗|✗|✗|✓|✓|✗|✗|
|RoboCook [47]|MPM|N/A|Hybrid|✓|✗|✗|✓|✓|✓|✗|
|Foo et al. [21]|FEM|N/A|Synthetic|✗|✗|✗|✓|✓|✗|✗|
|SliceIt [2]|FEM|Gazebo|Synthetic|✗|✗|✗|✓|✓|✗|✗|
|DiSECt [14]|FEM|N/A|Synthetic|✓|✗|✗|✓|✓|✗|✗|
|TopoCut [55]|MPM|N/A|Synthetic|✓|✗|✗|✓|✓|✓|✗|
|Ours|MPM|Maniskill[50]|Synthetic|✓|✓|✓|✓|✓|✓|✓|


Table 1. **Comparison of cutting benchmark datasets for embodied agents. Physics Sim:** Realistic physical simulation using a physicsbased simulator. **Robot Sim:** Ability to perform actions interactively within a robot simulator. **Data Origin:** Source of collected data (real-world, synthetic, or hybrid). “Hybrid” indicates a combination of real and synthetic data. **Multi Camera:** Robot is equipped with multiple cameras for perception. **Language:** Task goals are specified using human language instructions. **Continuous Action:** Actions are defined in a continuous control space rather than discrete steps. **Cutting Flexibility:** Support for diverse geometric and topological deformations from cutting. **Cutting Task:** Inclusion of cutting-related tasks. **Multiple Cut Style:** Support for multiple cutting styles or multi-step cutting sequences. **Force Data:** Availability of force-sensing data. 

ting introduces three challenges: (1) existing robot simulators used in VLA frameworks are limited in modeling topology changes and force/velocity variations during deformable interactions. (2) cutting outcomes are continuous in size, ratio, and orientation, requiring large-scale diverse data, and (3) multi-step interactions tend to generate a wide semantic gap between language instructions and quantitative outcomes; and (4) ensuring safety-aware control in cutting, where force constraints must be respected to prevent unstable or unsafe trajectories. 

Concurrently, advances in robot hardware and highfidelity simulation (e.g., MPM/FEM) enable large-scale, physically consistent deformable-manipulation data [63] for policy learning and sim-to-real transfer. In particular, MLS-MPM[16] handles contact-rich, topologychanging phenomena while reducing numerical diffusion and energy drift and preserving rotational and shear responses—properties that are crucial for cutting. 

Nevertheless, large-scale multimodal datasets suitable for VLA training remain scarce, especially for cutting[7], where safety and data-collection constraints make realworld scaling impractical [10]. These challenges are compounded by the nature of cutting, which demands precise goal specification via quantitative spatial instructions (exact positions, orientations, division ratios). Commands such as “cut through the apple’s center,” “slice the cucumber into three equal parts,” require tight coupling of perception, spatial reasoning, and force control, posing a quantitative grounding challenge: mapping language, with numeric precision, into executable trajectories. 

To bridge these gaps, we present a unified benchmark that couples a VLA dataset for precise grounding of quantitative instructions with an MPM-based cutting simula- 

tor. The simulator uses MPM to stably reproduce contactrich, topology-changing cutting interactions and to estimate force/stress distributions from impulse exchanges between particles. It includes a fracture criterion with particle/mesh updates, frictional knife–material contact via CPIC for stable momentum exchange, and safety controllers (force/velocity caps, entry-angle guards) to regularize contact transients. Sim-to-real consistency is validated via force–time curves and cutting-surface quality metrics. 

The dataset encodes both qualitative intent and quantitative cutting goals (position, orientation, division ratio), enabling large-scale multimodal learning and sim-to-real transfer for deformable-object cutting within a physically consistent framework. 

In summary, the present work contributes: 

- A **large-scale food cutting dataset** providing diverse food categories and cutting styles with multimodal annotations for quantitative instruction grounding. 

- A **hybrid simulation framework** combining ManiSkill and MPM to model deformation, contact forces, and topology changes under realistic visual and physical conditions. 

- A **scalable data generation pipeline** using LLM-based instruction synthesis and simulation-driven augmentation for efficient large-scale dataset construction. 

- A **comprehensive benchmark and analysis** of multiple VLA models, revealing challenges in quantitative grounding, continuous action control, and generalization. 

## **2. Related Work** 

**Large multimodal models (LMMs).** Recent advances in LMMs extend text-only LLM reasoning to visual and 

2 


Figure 2. Overview of CulinaryCut data generation pipeline. (a) Teleoperation generates initial cutting demonstrations for each cut style. (b) Physics simulation updates material deformation and cutting geometry. (c) Language instructions are augmented using LLMs with continuous cut state variations. (d, e) Trajectories are augmented via motion <mark>planning with object and</mark> cutting randomization. 

temporal domains by aligning frozen vision encoders with open-weight LLMs through lightweight adapters, enabling multimodal instruction-following and dialogue [33, 40, 42, 71]. Region- and video-aware variants enhance spatial and temporal grounding via RoI features and interleaved visual– text tokens [6, 11, 30, 43], while benchmarks such as MMBench and SEED-Bench systematically evaluate these multimodal capabilities [28, 35]. Building on such perceptionaligned foundations, reasoning-oriented frameworks incorporate interactive correction, memory, and deliberative intermediates to support long-horizon task understanding and multi-step decision making [19, 37, 60, 68]. Recent systems elevate LLMs into full perception–planning–control orchestrators [51, 65], while multimodal reasoning extends beyond language to speech and haptics for fine-grained embodied control [18, 24], pointing toward unified, adaptive, and deployable generalist agents. 

**Vision-language-action (VLA) for robotics.** VLA models unify perception, language, and action generation into a single policy backbone, progressing from early generalist tokenization to large-scale real-world transformers and open cross-embodiment architectures [3, 26, 44]. Reasoning-augmented VLAs build upon LMMs by integrating self-talk, VLM _→_ VLA transfer, and platformlevel orchestration for long-horizon tasks [20, 31, 51]. Trajectory-centric designs map language to motion/control tokens and leverage video-pretrained world models for predictive control [5, 23, 58]. Applications span bimanual/mobile manipulation and driving/aerial domains with 3D sensing enriching spatial grounding [12, 29, 70]. Efficiency and scalability are achieved through hierarchical decomposition, token-efficient actionization, and heterogeneous-robot pretraining with model–expert collaboration [1, 41, 62, 67]. 

**Large-scale robot learning datasets.** Community efforts have established broad open datasets for imitation and VLA-style policies, yet few directly address deformable cutting. Open X-Embodiment (RT-X) unifies over one million real-robot trajectories from 60 datasets across 34 labs and 22 embodiments [7], while RoboNet [8], BridgeData V2 [53], DROID [25], and LIBERO [32] provide large-scale manipulation datasets but exclud <mark>e deformable</mark> interactions. Cutting-specific resources remain simulationonly [2, 14, 55], and force–deformation datasets [66] are still lacking, as summarized in Table 1. Our dataset bridges this gap by introducing Set-of-Mark (SoM) and Trace-ofMark (ToM) supervision, explicitly encoding where to cut and how the tool evolves over time to enable fine-grained spatial–temporal reasoning for deformable cutting. 

**Material point method (MPM).** The material point method (MPM) [49] excels at simulating solid mechanics involving large deformations and fractures [48, 56, 57]. As a hybrid method coupling Lagrangian particles with an Eulerian grid, MPM effectively handles material deformation and topological change. Standard PIC/FLIP transfer methods used in early MPM, however suffered from severe numerical dissipation, failing to conserve rotational momentum. To address this dissipation problem, the Affine Particle-in-Cell (APIC) technique [22] was proposed, which effectively preserves rotational and shear stress via the affine velocity term **C** . Our work adopts MLS-MPM (moving least-squares MPM) [16], which incorporates the benefits of APIC, as our computational core to ensure a stable simulation foundation for synthetic data generation. 

## **3. CulinaryCut Benchmark** 

To evaluate the robot’s food cutting performance under text instructions, we introduce a cutting task benchmark in a hy- 

3 

brid simulation for the robot and physics. 

### **3.1. Robot Simulation Environment** 

**Simulation Platform.** We adopt ManiSkill [50], for robot simulation, which provides accurate robot movement and a visually realistic environment with three viewpoints of front, left, and right. It detects the moment when the knife first contacts the object surface and marks it as the contact phase. We integrate the topology change from the physics simulation during the contact phase into ManiSkill. 

**Robotic Manipulation.** For task execution, we utilize a 7-DoF Franka Emika Panda robot, equipped with a cutting knife as the end effector. The agent directly controls all joints and the gripper using ManiSkill’s built-in controller for stable and precise manipulation. End-effector actions are represented in 3D translation and quaternion rotation, with optional proportional derivative (PD) joint representations for different types of action model training. 

### **3.2. Physics Simulation Environment** 

**Simulation Platform.** We employ the moving leastsquares material point method (MLS-MPM) [16], which is known to be effective for cutting simulation [16]. The knife and cutting board are modeled as signed distance fields (SDFs), enabling efficient contact detection with MPMbased deformable objects. Full simulation method details are in the supplementary material (Section A). 

**Topology Change.** Each particle is associated with a continuum damage scalar _D ∈_ [0 _,_ 1]. At each time step, particles near the knife blade receive increased values of _D_ , which linearly reduce their effective moduli of Lam´e and promote crack formation. 

**Force and Velocity Calculation.** After resolving contact interactions on the grid, we compute the impulse of the knife during the time step by comparing the velocities before and after contact, from which the applied cutting force is derived. We additionally track the blade velocity and adopt a quadratic speed-resistance model to ensure that cutting occurs only when the blade moves sufficiently fast. 

### **3.3. Task Definition** 

**Cut Styles.** We define four primary **cut styles** ( _ℓs_ ) that characterize how the robot interacts with the object during cutting: _Normal Cut_ , _Bias Cut_ , _Guillotine Cut_ , and _Saw Cut_ . Normal Cut represents a straight cut with a perpendicular slicing motion. Bias Cut introduces an angled cutting trajectory, commonly used to increase contact area or create oblique slices. Guillotine Cut represents a downward slicing motion with the knife tip fixed, moving straight down 

along a single, controlled path. Saw Cut involves repeated back-and-forth motions along the cutting direction, capturing more realistic interactions with more fibrous materials. 

**Continuous Cut States.** We describe the progress and goal of each cutting operation using **continuous cut states** : _Middle Cut_ , _Split Cut_ , and _Ratio Cut_ . Middle Cut denotes cuts targeting the geometric center or midpoint of the object. Split Cut corresponds to **multi-cut** operations that divide the object into multiple segments ( _e.g._ , slicing a cucumber into several pieces). Ratio Cut specifies cuts at a desired proportion of the object, such as “cut at one-third from the left” or “slice at 70% of the length.” 

**Cutting Tasks.** Each cutting task in our dataset is defined by a combination of a _cut style_ and a _continuous cut state_ . In addition, the language instruction explicitly specifies both the target state ( _e.g._ , numerical ratio or number of segments) and the target object, ensuring that the robot receives precise, goal-directed commands. For example, a task may require a Saw Cut with a Split Cut state (multi-step slicing into several pieces), or a Normal Cut with a Ratio Cut state (single slice at a specified ratio). This formulation enables the VLA model to jointly reason about _how_ to cut (style) and _where/how much_ to cut (state), allowing for fine-grained control over realistic food cutting behaviors. 

**Success Criteria.** A trial is considered successful if the resulting cut position lies within a positional tolerance of one-tenth of the object’s total length. In addition to positional accuracy, the cutting motion must preserve a correct blade orientation, ensuring that the contact angle between the knife and the target plane remains within the same tolerance range. This criterion guarantees that the robot not only cuts at the correct location but also performs a spatially aligned and directionally consistent motion, while allowing minor variations from simulation dynamics. 

### **3.4. Data Collection** 

**Human Demonstration.** For each cut style, a human operator provides teleoperated demonstrations within the simulation environment. During teleoperation, the relative pose of the knife with respect to the target object is recorded and later used for trajectory augmentation. 

**Trajectory Augmentation.** A motion planner adapts each human-provided demonstration to various object conditions, including position ( _Op_ ), scale ( _Os_ ), rotation ( _Or_ ), object type ( _Ot_ ), and cutting parameters of height ( _⟨_ ) and velocity ( _⊑_ ). These conditions and parameters are randomly sampled for data augmentation. The planner generates realistic trajectories by computing the object’s Axis-Aligned 

4 

Bounding Box (AABB) to estimate its spatial extent and determining the appropriate cutting position based on the given cut style ( _ℓs_ ) and state. 

**Topology and Physics Data.** During trajectory execution, the physics simulation engine continuously updates the tool–object interaction by applying realistic physical forces and handling state transitions. The engine also updates the object’s topology to reflect deformation and separation as cutting progresses. By incorporating these physics-driven topology changes, the system maintains coherent alignment between visual observations and manipulation actions, enabling physically grounded supervision. 

**Language Instructions.** For each trajectory, we utilized a template-based language generator to create diverse text instructions that described the same manipulation. Each cut state included 5+ templates with placeholders for object and continuous state terms, filled with varied lexical candidates ( _e.g._ , “cut the banana at 0.5 ratio from the right side”, “slice the banana halfway along its length”). A pool of equivalent expressions ( _e.g._ , “50%”, “half”, “two quarters”) was randomly substituted to enhance linguistic diversity. Since the instruction omits the initial state, the agent must infer the current scene from visual input to execute the command correctly. All templates and lexical variations are listed in the supplementary material. 


Figure 3. Overall pipeline of the **Vision-Language-ActionPhysics (VLAP)** model during inference on the **CulinaryCut** dataset. 

novel object positions and scales not used during training. (2) multi-object evaluation where multiple objects coexist within the same workspace, and (3) evaluation using unseen language instructions specifically reserved for testing. Additionally, user-defined cross-domain evaluation is supported, where models only trained on a specific object category (e.g., apple) can be evaluated on unseen categories (e.g., banana) to measure compositional generalization. 

## **4. CulinaryCut-VLAP** 

### **4.1. Vision-Language-Action Model** 

**Data Statistics.** The CulinaryCut dataset consists of 325,000 simulation-based manipulation trajectories, where each task is defined as a unique combination of a _cut style_ ( _ℓs_ ) and a _cut state_ . We include five representative cut styles and thirteen cut states, composed of nine ratio cuts ranging from 0.1 to 0.9, one middle cut, and three split cuts (3-way, 4-way, and 5-way splits). For every cutting task, the system generates 500 augmented trajectories using a motion planner, and the remaining elements of the scene are randomly sampled. The dataset comprises seven food categories (Ø _t_ ): orange, strawberry, melon, cucumber, banana, apple, and peach. All trajectories are collected across two distinct scenes, a realistic kitchen environment and a standard table setting, reflecting common everyday cutting contexts. Each trajectory is paired with more than five language instructions generated and augmented by large language models that cover a broad spectrum of numerical expressions, ratio descriptions, spatial directives, and phrasing styles. We allocate 20 trials per cutting task for testing, and the remaining are used for training. 

**Evaluation Setting.** We design three evaluation environment settings to comprehensively assess model generalization: (1) evaluation under unseen random seeds involving 

Our baseline follows the sequence-level Vision-LanguageAction (VLA) formulation adopted in large-scale models such as OpenVLA [27], Octo [52], and RDT-1B [34]. Given a language instruction _ℓ_ and a multimodal observation sequence _o_ 1: _T_ = _{_ ( _It, xt_ ) _}_<sup>_T_</sup> _t_ =1<sup>, where</sup><sup>_It_denotes multi-view</sup> RGB images and _xt_ represents proprioceptive states, the VLA model _πθ_ generates an entire action sequence, 


### **4.2. Manipulation Safety Module** 

To prevent excessive forces beyond the robot’s mechanical limits, we introduce a manipulation safety module that regulates knife velocity based on force predictions from the physics simulator. In the Franka robot, the contact force parameter ( _F_ max) above 100 N may cause hardware damage, making velocity control critical for safe manipulation. From the simulation, we construct a dataset _D_ = _{_ ( _vi,_ **m** _i, Fi_ ) _}_<sup>_N_</sup> _i_ =1<sup>, where</sup><sup>_vi_is the velocity of the knife,</sup><sup>**m**</sup><sup>_i_</sup> denotes the properties of the material ( _e.g._ , _E_ , _σy_ ), and _Fi_ is the resulting contact force. A regression model _R_ predicts expected maximum force: 


5 


Figure 4. **Object Variation Results.** The bar chart shows the inference performance of each model when trained on individual object–instruction pairs. 

and the safe velocity threshold is defined by 


ensuring that the forces remain within the safety limits. This data-driven limiter integrates with the compliance controller, allowing a material-aware adaptive cutting motion. 

### **4.3. Cutting Style Transfer Module (CSTM)** 

CSTM transforms the action generated by VLA into the action generated by auxiliary networks. 

A ViT-based binary classifier _C_ predicts the contact state between the knife and objects from observation images _It_ . 

Then, a cut-style generator _f_ converts the predicted trajectory **a** ˆ1: _T_ into a style-specific trajectory. Built upon behavior cloning, the module uses the contact segments of normal cutting trajectories **a** and their style-specific counterparts **a**<sup>_s_</sup> as supervision, enabling VLA outputs to be adapted to different styles. Finally, the style-conditioned policy is defined as: 


where the generated stylized trajectory **a**<sup>s</sup> 1: _T_<sup>reflectsboth</sup> the linguistic intent _ℓ_ and the cut style instruction _ℓs_ . 

## **5. Experiments** 

**Experimental Setup.** All cutting experiments are conducted in a simulated tabletop environment with randomized object placements to evaluate each model’s robustness and spatial generalization. Before each episode, the target object (e.g., banana, cucumber, apple, melon) is randomly initialized within the workspace boundary on the table. The robot executes the instructed cutting motion according to either a language-based or numerical command. Each task is evaluated over 20 randomized trials (excluding the training seed), varying the object’s initial pose and position to determine success. 


Figure 5. **Multi-Object Results:** Comparison of RDT, Octo, and OpenVLA in single- and multi-object scenes. The presence of additional objects significantly impairs target identification and reduces cutting success rates. 

### **5.1. Experiment Results** 

**General Task.** As shown in Figure 4, models achieve stable performance when cutting normal-sized objects (e.g., _banana_ , _cucumber_ ) at the half-cut ratio, but success rates drop sharply for smaller objects such as _berry_ , revealing limited precision and contact generalization at small scales. 

**Multi-object Target Identification.** To evaluate whether the model can correctly identify and cut the instructed object when multiple objects are present, we conduct a multiobject scene experiment as illustrated in Figure 5. Each scene contains multiple fruits placed randomly on the table, and the model receives an instruction referring to one specific target (e.g., “cut the banana at the center”). The results, summarized in Figure 5, show a consistent performance drop across all models when transitioning from single-object (Original) to multi-object scenarios. Specifically, the success rate of RDT decreases from 68.57% to 31.42%, Octo from 42.28% to 17.00%, and OpenVLA from 50.57% to 27.85%. This indicates that while the models possess moderate visual grounding ability, their reasoning and spatial grounding for precise target selection remain limited under complex, cluttered multi-object conditions. 

**Cross-object Generalization.** We evaluate the baseline models’ ability to generalize to unseen objects when trained on a single-object dataset and tested on different, untrained categories. As shown in Figure 8, the performance exhibits a moderate drop when transferring to new objects: RDT1B decreases from 59.28% to 48.14%, and OpenVLA from 48.14% to 45.00%. Although the success rates decline, both models still maintain reasonable performance on unseen objects, indicating that our dataset effectively promotes transferable cutting behavior beyond the trained object category. This result suggests that the proposed dataset provides sufficient geometric and visual diversity to support generalizable cutting policies across object types. 

6 


Figure 6. **Transfer Performance Results.** (a), (b), and (c) illustrate ratio-based cutting tasks, while the bar chart on the right compares model performance between training and testing conditions, highlighting a clear performance drop on unseen ratio configurations. 


Figure 7. **Evaluation of Continuous Cut.** Success rates (%) of RDT, Octo, and OpenVLA under continuous ratio-based cutting instructions. The radar charts show model performance across cut ratios (0.1–0.9) for banana and cucumber. 


Figure 8. **Generalization to Unseen Objects.** Evaluation of model generalization to unseen objects and novel language instructions. The bar chart presents success rates of RDT, Octo, and OpenVLA, showing a clear performance drop on unseen objects. 

**Directional and Ratio-based Generalization.** We further evaluate the RDT model, which achieved the highest overall performance, to analyze its ability to generalize across directional flips and cutting ratios. As summarized in Figure 6, the model shows a significant degradation when trained on one configuration and evaluated on its directional or proportional counterpart. When the model is trained on 0.25-ratio cuts from the right side and then evaluated on the mirrored left-side instruction (e.g., ‘cut the banana at a 0.25 ratio from the left’), its success rate drops from 55% to 20%. Similarly, in the reverse direction (0.75 _→_ 0.25), the success rate decreases from 35% to 0%, and when transferring from the 0.5-ratio to 0.25-ratio instruction, performance drops from 60% to 25%. These findings demonstrate that even strong diffusion-based policies fail to generalize symmetrically across directional and ratio-based instructions. To bridge this gap, we introduce the ContinuousCut dataset, which provides dense ratio supervision (0.1–0.9) with explicit left/right labels. This enables continuous grounding of cutting geometry and fosters robust generalization across spatial and linguistic variations. 

**Numeric Ratio Grounding Failure in Continuous-Cut.** As shown in Figure 7, our continuous-ratio benchmark exposes a systematic weakness of current VLA-style policies in grounding percentage-based ratios to spatial geometry. Even the large diffusion-based baseline ( **RDT-1B** ) behaves inconsistently across nearby targets: on _banana_ , success 

rate is 60% at ratio 0 _._ 40 cut but drops to 35% at 0 _._ 70 and 0 _._ 75; on _cucumber_ , 60% at ratio 0 _._ 25 falls to 25% at 0 _._ 75. **OpenVLA** and **Octo** likewise fluctuate sharply and often collapse at mid-range ratios, as seen on banana at ratio 0 _._ 40 where OpenVLA5% and Octo 0%. Thus, to correctly execute instructions such as “cut at 40% from the right,” the model must accurately link linguistic quantities to objectcentric coordinates and correctly perceive the object’s size and spatial proportions. 

### **5.2. Ablation Study** 

**Effect of Fine-Grained Motion Styles and CSTM Module.** As shown in Figure 9, training on fine-grained, repetitive motions such as sawcut drastically reduces task success (59.28% _→_ 5.00%) on RDT-1B model, as dense oscillatory trajectories distort motion feature distributions and destabilize policy learning. To address this, we propose the **Cutting Style Transfer Module (CSTM)** , which preserves the global trajectory structure while adaptively transferring local style cues. Rather than replicating high-frequency motions, CSTM regularizes trajectory dynamics to maintain temporal smoothness and consistency. Detailed qualitative results, including visualizations of predicted trajectory coordinates, are provided in the Supplementary Material. 

**Assessing the Physical Realism of MPM-Based Cutting Simulation** To evaluate the physical realism of the MPMbased Cutting Simulation, the Young’s Modulus _E_ was sys- 

7 


Figure 9. Visualization of task success rate for different trajectory styles. **Case 1** represents the normal trajectory with the proposed Cutting Style Transfer Module (CSTM) applied, while **Case 2** corresponds to training on sawcut trajectories. 


Figure 10. Temporal progression of knife force magnitude for all tested Young’s moduli. 


Figure 11. Temporal progression of knife velocity for all tested Young’s moduli. 

tematically varied between 0 _._ 1 _×_ 10<sup>6</sup> Pa and 0 _._ 9 _×_ 10<sup>6</sup> Pa, in increments of 0 _._ 1 _×_ 10<sup>6</sup> Pa. This parameter sweep was designed to assess how material stiffness influences the peak cutting force and post-impact velocity during a single cutting cycle (downward stroke and retraction). 


Figure 12. Comparison of peak cutting force and post-impact velocity across all tested Young’s moduli. 

force magnitude throughout the simulation for all nine tested Young’s moduli. Each curve is color-coded from purple (lowest _E_ ) to yellow (highest _E_ ), illustrating that as stiffness increases, the knife experiences higher cutting forces. Figure 11 similarly plots the knife velocity over time, using the same color scheme. The velocities reveal the opposite trend, demonstrating that stiffer materials lead to lower knife velocities. 

The force magnitudes were directly obtained from the simulation output, while velocities were estimated via a finite-difference approximation of the time derivative of position, computed from the simulation output. 

Figure 12 summarizes the results by comparing the recorded peak cutting force (N) and post-impact velocity (m _/_ s) for each tested modulus. The peak force, defined as the maximum knife force across time for a given _E_ , consistently occurs at the fifth timestep for all simulations. Peak cutting force increases approximately linearly with _E_ , from 69 _._ 96 N at _E_ = 0 _._ 1 _×_ 10<sup>6</sup> Pa to 77 _._ 34 N at _E_ = 0 _._ 9 _×_ 10<sup>6</sup> Pa. The post-impact velocity, defined as the minimum knife velocity following impact (occurring at the sixth timestep), shows a corresponding linear decrease, from 0 _._ 22 m _/_ s at _E_ = 0 _._ 1 _×_ 10<sup>6</sup> Pa to 0 _._ 02 m _/_ s at _E_ = 0 _._ 9 _×_ 10<sup>6</sup> Pa. These results are physically consistent: stiffer materials (larger _E_ ) resist deformation more, requiring greater cutting forces and storing more elastic energy, which slows the blade after impact. The observed forcevelocity relationship validates that our MPM simulation realistically captures the interplay between elastic stiffness, cutting resistance, and energy dissipation. 

## **6. Conclusion** 

We propose a unified framework for vision-languageaction-physics (VLAP) in deformable object manipulation, centered on food cutting. By combining a physically realistic MLS-MPM simulator with a large-scale multimodal dataset, our approach enables quantitative evaluation of geometric and physical reasoning in cutting tasks. The **CulinaryCut** benchmark further enhances cutting performance through physically grounded learning. 

Figure 10 shows the temporal progression of the knife 

8 

## **A. Details on MLS-MPM Simulation Method for Cutting** 

Our simulation methodology is based on MPM. MPM represents materials as collections of particles, or point clouds. Each particle carries physical quantities such as mass, volume, position, and velocity. On a given timestep of the simulation, the particle-based quantities are interpolated or rasterized to a background grid, often a uniform square/cubic Cartesian grid. Then, governing equations such as conservation of momentum are solved on the grid, predicting updated values at the next time step. These updated quantities are interpolated back to the particles, and the particles’ positions are updated for the next time step. 

In addition to each particle carrying position **x** , velocity **v** , and deformation gradient **F** , in MLS-MPM, an affine velocity term **C** is also stored on each particle. This increases the fidelity of velocities transferred between particles and the background grid—and hence, the fidelity of the overall simulation. In our case, to simulate cutting, we also store on each particle an accumulated plasticity _α_ and a continuum damage scalar _D ∈_ [0 _,_ 1]. Our background grid is a uniform lattice with spacing ∆ _x_ . 

**Governing equations.** At the continuum level, we enforce mass and linear momentum balance together with the kinematic relation for **F** ; the Cauchy stress **_σ_** is closed by a constitutive law: 


We adopt corotated elasticity as the elastic backbone and couple it with (optional) J2 plasticity via radial return. Around the blade we accumulate a scalar damage _D_ that linearly reduces the effective Lam´e moduli, which promotes controlled crack opening. 

**P2G: particle-to-grid transfer.** Each particle distributes mass and momentum to its 3 _×_ 3 _×_ 3 stencil using quadratic B- spline weights; the APIC/MLS affine term **C** is transferred to better preserve rotation/shear modes and reduce numerical diffusion. Stress is computed from the corotated model by polar decomposition **F** = **RS** (rotation **R** ; stretch **S** ). Damage acts by scaling the Lam´e parameters, and when yielding occurs we apply J2 radial return (optionally with a small viscoplastic parameter) to tame overstress during abrupt contact transients. The Cauchy stress and the corotated first Piola stress are 


**Grid update.** Grid node velocities are obtained by dividing momentum by mass, followed by gravity, boundary, and mild damping. Knife and board are represented as signed distance fields (SDFs). For nodes inside blade/board AABBs, we sample SDFs and resolve contact by decomposing relative velocity into normal/tangential components, applying non-penetration (normal restitution) and Coulomb friction; a CPIC-style conservative mix can be used to strengthen momentum consistency with the tool. We accumulate the impulse from pre- and post-contact velocities and convert it to an average force over the outputaccumulation window ∆ _t_ acc: 


This force directly underpins the force–time curves reported in Section 5. In parallel, we build a contact-strength scalar _c_ ˆ _∈_ [0 _,_ 1] by normalizing the accumulated approach speed near the blade with _c_ norm = 0 _._ 35 ∆ _x/_ ∆ _t_ ; _c_ ˆ gates cutting (damage updates occur only when contact is sufficient) and drives a quadratic speed-resistance model for the knife: with normalized speed _u_ = _s/s_ 0, we update _u ← u/_ (1 + _k_ 2 ˆ _c u_ ∆ _t_ ), scaling _k_ 2 by material ( _E, σy_ ) so harder materials decelerate faster. Here, _E_ denotes the Young’s modulus. 

**G2P: grid-to-particle transfer.** Updated grid velocities are interpolated back to particles to form the new particle velocity and affine term. We apply gravity, particle-level damping, and a small “tip force” to particles within a narrow band around the blade edge to gently separate the two sides and mitigate stick–slip oscillations. The deformation gradient is advanced with the affine field and clamped isotropically when _J_ leaves a safe interval: 


**Damage-gated cutting and resolution-invariant scaling.** Damage accumulation is enabled only within a blade SDF band _|ϕ| <_ band when three conditions hold simultaneously: sufficient contact strength ( _c_ ˆ _≥ c_ ˆmin), sufficiently fast approach ( _vn ≤−v_ th), and a downward stroke. As _D_ grows, effective stiffness decreases, and cracks open 

1 

|**Cut Style**_ℓs_|**Cut State**|**Representative Language Instruction**|
|---|---|---|
|**Normal Cut**|Ratio Cut|Normal Cut the_Ot_at 0.3 ratio from the right side.|
|**Normal Cut**|Middle Cut|Normal Cut the_Ot_at the midpoint along its length.|
|**Normal Cut**|Split Cut|Normal Cut the_Ot_at the first split boundary from the right side.|
|**Bias Cut**|Ratio Cut|Bias cut the_Ot_at 0.4 ratio toward the right end.|
|**Bias Cut**|Middle Cut|Bias cut the_Ot_at the midpoint from the left side.|
|**Bias Cut**|Split Cut|Bias cut the_Ot_at the first split boundary along its length.|
|**Guillotine Cut**|Ratio Cut|Guillotine cut the_Ot_at 0.5 ratio from the left side.|
|**Guillotine Cut**|Middle Cut|Guillotine cut the_Ot_at the center from the top direction.|
|**Guillotine Cut**|Split Cut|Guillotine cut the_Ot_at the first split boundary from the top.|
|**Saw Cut**|Ratio Cut|Saw cut the_Ot_at 0.6 ratio along its length.|
|**Saw Cut**|Middle Cut|Saw cut the_Ot_at the midpoint from the right side.|
|**Saw Cut**|Split Cut|Saw cut the_Ot_at the third boundary toward the right end.|


Table S1. Representative language instructions for all combinations of Cut Style (Normal, Bias, Guillotine, Saw) and Continuous Cut State (Ratio, Middle, Split). 

progressively; visual/topological separation is stabilized by connectivity-/color-based post-processing of particles. To preserve behavior across resolutions we define resolutioninvariant thresholds via band = band0(∆ _x_ ref _/_ ∆ _x_ )<sup>_γ_</sup> and _v_ th = (∆ _x/_ ∆ _t_ ) ˆ _v_ . 

**Stabilization, efficiency, and reproducibility.** We use a CFL-limited step (∆ _t ≤_ 0 _._ 2 ∆ _x/_ ~~�~~ ( _λ_ + 2 _µ_ ) _/ρ_ ), cap particle/grid speeds, clamp _J_ , and apply AABB culling of blade/board SDF queries. Implementation is on Taichi[17] GPU kernels with atomic impulse reductions and tuned block sizes. For reproducibility we avoid logging full deformation fields and instead record a lightweight set of summaries: (i) force–time curves with a momentum-change check<sup>�</sup> _i_<sup>_mi_∆</sup><sup>**v**</sup><sup>_i≈_</sup> � **F** _dt_ , (ii) _J_ statistics (min/max and clamp counts), (iii) contact-strength _c_ ˆ traces and blade/handle/board impulses, and (iv) configuration metadata (∆ _x,_ ∆ _t_ , material parameters, knife/EEF states). When ∆ _x,_ ∆ _t_ change we rescale band, _v_ th, and _c_ norm as specified; when materials change we scale _k_ 2 with ( _E, σy_ ). 

## **B. Language Instruction Design.** 

This section outlines the design of the language instructions used in the CulinaryCut dataset. Each instruction is paired with a single trajectory and corresponds to a specific Cutting Specification, defined as a combination of a _Cut Style_ and a _Continuous Cut State_ . 

**Default Settings.** When an instruction specifies only a Continuous Cut State (Ratio, Middle, Split) and does not specify the Cut Style, we default to using the **Normal Cut** style. Conversely, when only the Cut Style (Bias, Guillotine, Saw) is provided without a Continuous Cut State, we assign the **Middle Cut** state. These default rules ensure that every instruction is complete and consistently resolves to a single, unambiguous Cutting Specification. 

**Design Objectives.** Instructions are constructed to convey the information required for the Cutting Specification. 

For Continuous Cut States, we include numerical terms, geometric references, or count-based expressions as needed. We augment each template with additional paraphrases generated by large language models to increase linguistic diversity while preserving the intended semantics. 

**Instruction Structure.** Each instruction consists of four components: 

- **Target Object** _Ot_ **:** banana, cucumber, apple, peach, melon, orange, strawberry 

- **Cut Style** _ℓs_ **:** Normal, Bias, Guillotine, Saw 

- **Continuous Cut State:** Ratio, Middle, Split 

- **Directional Reference:** from the left/right side, from the top, along its length 

**Instruction Samples.** Table S1 provides representative instruction examples for all combinations of Cut Style and Continuous Cut State. Each entry illustrates how an instruction encodes both the cutting motion and the target position. When an instruction omits either component, we apply the default rules described above. 

## **C. Trajectory Visualization.** 

To highlight the structural differences among cutting strategies, Figure S1 presents representative end-effector (EE) trajectories extracted from the dataset. All trajectories are plotted in the world coordinate frame and temporally aligned, enabling direct comparison across different Cut Style _×_ Continuous Cut State combinations. 

**Normal Cut.** Normal Cutting exhibits a straight downward motion pattern, characterized by a monotonic decrease along the Z-axis with minimal lateral movement. In the Middle Cut case (Figure S1 (A)), the EE performs a single descent toward the geometric center of the object. For Split Cuts (Figure S1 (B–D)), the trajectory contains multiple vertical segments, each corresponding to a distinct slicing operation in the multi-cut sequence. Despite the increased number of cuts, the vertical descent profile remains consistent, reflecting the stable and non-oscillatory nature of Normal Cutting. In the Split Cut settings, increasing the number of cuts simply adds additional vertical descent segments, each executed at a new target location. In practice, the 2- cut, 3-cut, and 4-cut trajectories differ only in the number of repeated descending motions, while the underlying slicing dynamics remain identical across all cases. 

**Saw Cut.** Saw Cutting introduces periodic lateral oscillations superimposed on the downward motion (Figure S1 (E)). These oscillations appear as sinusoidal variations along the X-axis and represent the forward–backward 

2 


Figure S1. **Trajectory visualization.** End-effector (EE) trajectory visualizations for different Cut Style + Continuous Cut State combination. (A) Normal Cut + Middle produces a single vertical descent toward the object’s midpoint. (B)–(D) Normal Cut + Split show multi-cut trajectories with 2-cut, 3-cut, and 4-cut sequences, each consisting of repeated vertical slicing motions at distinct target locations. (E) Saw Cut introduces periodic lateral oscillations characteristic of sawing actions. (F) Bias Cut exhibits a diagonally slanted descent produced by a continuous lateral shift during cutting. 

micro-motions characteristic of sawing. The oscillation frequency is randomly sampled at the start of each demonstration, resulting in diverse but consistently periodic patterns while maintaining the overall sawing behavior. 

**Bias Cut.** Bias Cutting exhibits a diagonal slicing motion produced by a continuous lateral drift during descent. As shown in Figure S1, the EE trajectory deviates steadily from the straight-line profile of the Normal Cut, forming an oblique motion path. This lateral shift results in an angled contact geometry, aligning with the definition of Bias Cutting in Sec. 3.3. 

## **D. Additional Experiment Result** 

### **D.1. Additional Result** 

**Split Cut Evaluation.** To analyze how VLA policies behave in multi-segment cutting, we consider the Split Cut setting, where the agent must place multiple cuts so that an object is divided into equal-length pieces. We treat an episode as _successful_ only if all required cuts fall within a _±_ 10% tolerance around their ideal boundaries. Under this strict criterion, the overall Split Cut success rate is **0%** for all baselines (RDT-1B, Octo, and OpenVLA), indicating that none of the models can complete a full cutting sequence reliably. 

Table S2 provides a finer-grained view of partial success 

3 

Table S2. **Distribution of successfully placed cuts in Split Cut evaluation with RDT-1B.** Each cell shows the percentage of episodes in which exactly _k_ cuts were placed within the _±_ 10% tolerance among all required cuts for that Split Cut configuration. 

|Object|Split Cut|1|2|3|4|
|---|---|---|---|---|---|
||1/3|20%|0%|–|–|
|Banana|1/4|10%|5%|0%|–|
||1/5|5%|0%|0%|0%|
||1/3|30%|0%|–|–|
|Cucumber|1/4|10%|0%|0%|–|
||1/5|0%|0%|0%|0%|


Table S3. Average Cut Completion by Object with RDT–1B Models 

|Case|Train Topology|Evaluation Topology|Success Rate|
|---|---|---|---|
|Case 1|update✗|update✗|55%|
|Case 2|update✗|update✓|50%|
|Case 3|update✓|update✗|45%|
|Case 4(ours)|update✓|update✓|60%|


for RDT-1B. For each object and Split Cut configuration (1/3, 1/4, 1/5), the columns labeled 1–4 report the percentage of episodes in which exactly that many cuts were placed correctly among all required cuts. For example, in the 1/3 Split Cut task (which requires two cuts), the entry **20%** in the “1” column for banana indicates that 20% of episodes achieved exactly one correct cut and never both; the “2” column remains at 0%, showing that no episode successfully placed both boundaries. In the more challenging 1/4 setting (three required cuts), banana still reaches a small number of partially successful episodes: 10% of episodes achieve exactly one correct cut, and 5% manage to place two correct cuts, but no episode reaches all three. Cucumber generally shows slightly higher rates of obtaining at least one correct cut (e.g., 30% for the 1/3 setting), yet still fails to complete the full sequence under any configuration. 

These distributions reveal a characteristic failure mode of long-horizon cutting. Once the first cut is misplaced, the policy rarely reorganizes the remaining cuts to recover the global pattern. Instead, the controller tends to hover around a local region and repeatedly issue similar cutting motions, producing strange, oscillatory trajectories rather than progressing to new boundaries. In other words, the models can sometimes “hit” one boundary, or occasionally two in the 1/4 setting, but they do not learn stable multi-step cutting programs. This helps explain why partial statistics in Table S2 are non-zero, while the strict all-cuts-complete success remains 0% for RDT-1B, Octo, and OpenVLA alike. 


Figure S2. **Predicted 3D end-effector trajectories from RDT under different topology-update conditions.** (A) Without topology update (Case 3), the predicted trajectories show larger axiswise deviations. (B) With topology update (Case 4), the trajectories become more stable as cutting progresses, demonstrating the importance of modeling topology changes. 

**Ablation Study of Topology Update.** Table S3 reports an ablation on Train Topology and Evaluation Topology, where we independently control whether the object mesh is allowed to update its connectivity after a cut. Here, “update ✓” denotes that the mesh connectivity is updated once the cut is completed, so that the rendered observations explicitly show separated parts, visible gaps, and other topology changes. In contrast, “update ✗” corresponds to a topologyfree setting in which the mesh connectivity is kept fixed even after the knife passes through the object, and only the surface geometry is deformed. The four rows in Table S3 correspond to all combinations of training and evaluation conditions. Quantitatively, the average success rates vary only moderately across these settings: the matched regimes in Case 1 and Case 4 achieve 55% and 60%, while the mismatched regimes in Case 2 and Case 3 drop to 50% and 45%, respectively. However, these relatively small differences in average cut completion mask systematic qualitative changes in the behavior of the RDT–1B. 

When the model is trained on topology-aware data but evaluated in an environment where the topology is not updated (Case 3), it cannot reliably perceive that a cut has already succeeded. As a result, the policy frequently returns 

4 


Figure S3. **Visualization of the end-effector (EEF) trajectory and contact force during the cutting motion.** The top plot illustrates the EEF position along the cutting direction, while the bottom plot shows the corresponding contact force profiles. **Case 1** denotes the model _without_ the Safety Module, and **Case 2** represents the model _with_ the proposed Safety Module enabled. For clarity, regions where Case 1 exhibits excessive force (exceeding 60 N) are highlighted in red, indicating unsafe spikes that the Safety Module successfully suppresses. 

Table S4. Average maximum cutting speed before and after applying the proposed safety module. 

|Safety Module|Maximum cutting speed|Maximum force|
|---|---|---|
|Safety Module✗|3.63 m/s|129.31N|
|Safety Module✓|0.89 m/s|37.78N|


Figure S3, the baseline model without the safety module exhibits an excessively aggressive motion pattern: across 20 trials, the predicted average maximum cutting velocity reaches 3.63 m/s, and the corresponding peak contact force in the physics simulation increases to 129.31 N, surpassing the Franka robot’s safe operational limit of 100 N. 

In contrast, when the proposed safety module is enabled, the commanded velocity is adaptively regulated according to contact conditions. As visualized in Table S4, the resulting execution reduces the average maximum cutting speed to 0.89 m/s, while the simulated peak contact force remains safely contained at 37.78 N. 

These results indicate that the proposed safety module effectively suppresses force spikes that may otherwise cause hardware damage, producing material-aware and stable cutting trajectories. Even under challenging contact interactions, the module ensures physically safe manipulation without compromising task feasibility. 

to nearly the same 3D pose and executes a second, redundant cutting motion along an almost identical trajectory, as visualized in Figure S2 (A). 

In contrast, when the same model is deployed in an environment that updates the object topology after each successful cut (Case 4), the change in geometry is clearly reflected in the visual input, and the policy typically performs a single decisive cut and then terminates or moves on to the next instruction, as shown in Figure S2 (B). A similar form of distribution shift also appears in Case 2, where the model is trained without topology updates but evaluated with them, leading to slightly degraded average performance compared to the fully topology-aware configuration in Case 4. 

Although these experiments are conducted in simulation, where we can artificially switch topology updates on or off, real-world cutting inevitably changes the object topology and this change is immediately visible to the robot’s camera. Therefore, even though the numerical differences in Table S3 are modest, we regard topology-aware data generation and evaluation (Case 4) as an important design choice for obtaining stable, non-redundant cutting behavior in real robotic systems. 

**Ablation Study of Safety module.** To validate the effectiveness of our manipulation safety module, we compare the maximum cutting velocity and contact force before and after applying the proposed limiter. As shown in Table S4 and 

5 

## **References** 

- [1] Anurag Ajay, Seungwook Han, Yilun Du, Shuang Li, Abhi Gupta, Tommi Jaakkola, Josh Tenenbaum, Leslie Kaelbling, Akash Srivastava, and Pulkit Agrawal. Compositional foundation models for hierarchical planning, 2023. 3 

- [2] Carlos C. Beltran-Hernandez et al. A dual simulator framework for learning robot food slicing. _arXiv preprint arXiv:2404.02569_ , 2024. 2, 3 

- [3] Anthony Brohan. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. 3 

- [4] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 1 

- [5] Arthur Bucker, Luis Figueredo, Sami Haddadin, Ashish Kapoor, Shuang Ma, Sai Vemprala, and Rogerio Bonatti. Latte: Language trajectory transformer, 2022. 3 

- [6] Mu Cai, Haotian Liu, Dennis Park, Siva Karthik Mustikovela, Gregory P. Meyer, Yuning Chai, and Yong Jae Lee. Vip-llava: Making large multimodal models understand arbitrary visual prompts. _arXiv preprint arXiv:2312.00784_ , 2023. 3 

- [7] Open X-Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, and et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 2, 3 

- [8] Sudeep Dasari, Frederik Ebert, Stephen Tian, Suraj Nair, Ben Bucher, Karl Schmeckpeper, Siddharth Singh, Sergey Levine, and Chelsea Finn. Robonet: Large-scale multi-robot learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2019. 3 

- [9] Atharva Dikshit, Alison Bartsch, Abraham George, and Amir Barati Farimani. Robochop: Autonomous framework for fruit and vegetable chopping leveraging foundational models. _arXiv preprint arXiv:2307.13159_ , 2023. 2 

- [10] Alexander Khazatsky et al. Droid: A large-scale in-the-wild robot manipulation dataset, 2024. 2 

- [11] Xinyu Fang, Kangrui Mao, Haodong Duan, Xiangyu Zhao, Yining Li, Dahua Lin, and Kai Chen. Mmbench-video: A long-form multi-shot benchmark for holistic video understanding. _arXiv preprint arXiv:2406.14515_ , 2024. 3 

- [12] Koffivi Fid`ele Gbagbe, Miguel Altamirano Cabrera, Ali Alabbas, Oussama Alyunes, Artem Lykov, and Dzmitry Tsetserukou. Bi-vla: Vision-language-action model-based system for bimanual robotic dexterous manipulations, 2024. 3 

- [13] Ran Gong, Jiangyong Huang, Yizhou Zhao, Haoran Geng, Xiaofeng Gao, Qingyang Wu, Wensi Ai, Ziheng Zhou, Demetri Terzopoulos, Song-Chun Zhu, et al. Arnold: A benchmark for language-grounded task learning with continuous states in realistic 3d scenes. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 2 

- [14] Eric Heiden, Miles Macklin, Yashraj Narang, Dieter Fox, Animesh Garg, and Fabio Ramos. Disect: A differentiable simulator for parameter inference and control in robotic cutting. _arXiv preprint arXiv:2203.10263_ , 2022. 1, 2, 3 

- [15] Minho Heo, Youngwoon Lee, Doohyun Lee, and Joseph J Lim. Furniturebench: Reproducible real-world benchmark for long-horizon complex manipulation. _The International Journal of Robotics Research_ , 44(10-11):1863–1891, 2025. 2 

- [16] Yuanming Hu, Yu Fang, Ziheng Ge, Ziyin Qu, Yixin Zhu, Andre Pradhana, and Chenfanfu Jiang. A Moving Least Squares Material Point Method with Displacement Discontinuity and Two-way Rigid Body Coupling. _ACM Trans. Graph._ , 37(4), 2018. 2, 3, 4 

- [17] Yuanming Hu, Tzu-Mao Li, Luke Anderson, Jonathan Ragan-Kelley, and Fr´edo Durand. Taichi: a language for high-performance computation on spatially sparse data structures. _ACM Trans. Graph._ , 38(6), 2019. 2 

- [18] Jialei Huang, Shuo Wang, Fanqi Lin, Yihang Hu, Chuan Wen, and Yang Gao. Tactile-vla: Unlocking visionlanguage-action model’s physical knowledge for tactile generalization, 2025. 3 

- [19] Siyuan Huang, Zhengkai Jiang, Hao Dong, Yu Qiao, Peng Gao, and Hongsheng Li. Instruct2act: Mapping multimodality instructions to robotic actions with large language model, 2023. 3 

- [20] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Tomas Jackson, Linda Luu, Sergey Levine, Karol Hausman, and Brian Ichter. Inner monologue: Embodied reasoning through planning with language models, 2022. 3 

- [21] Prajjwal Jamdagni and Yan-Bin Jia. Robotic slicing of fruits and vegetables: modeling the effects of fracture toughness and knife geometry. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6607–6613. IEEE, 2021. 2 

- [22] Chenfanfu Jiang, Craig Schroeder, and Joseph Teran. An Angular Momentum Conserving Affine-Particle-in-Cell Method. _Journal of Computational Physics_ , 338:137–164, 2017. 3 

- [23] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. Vima: General robot manipulation with multimodal prompts, 2023. 3 

- [24] Muhamamd Haris Khan, Selamawit Asfaw, Dmitrii Iarchuk, Miguel Altamirano Cabrera, Luis Moreno, Issatay Tokmurziyev, and Dzmitry Tsetserukou. Shake-vla: Visionlanguage-action model-based system for bimanual robotic manipulations and liquid mixing, 2025. 3 

- [25] Alexander Khazatsky and et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 2, 3 

- [26] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An opensource vision-language-action model, 2024. 3 

- [27] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Fos- 

6 

ter, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 5 

- [28] Bohao Li, Yuying Ge, Yixiao Ge, Guangzhi Wang, Rui Wang, Ruimao Zhang, and Ying Shan. Seed-bench-2: Benchmarking multimodal large language models. _arXiv preprint arXiv:2311.17092_ , 2023. 3 

- [29] Chengmeng Li, Junjie Wen, Yan Peng, Yaxin Peng, Feifei Feng, and Yichen Zhu. Pointvla: Injecting the 3d world into vision-language-action models, 2025. 3 

- [30] Feng Li, Renrui Zhang, Hao Zhang, Yuanhan Zhang, Bo Li, Wei Li, Zejun Ma, and Chunyuan Li. Llava-next-interleave: Tackling multi-image, video, and 3d in large multimodal models. _arXiv preprint arXiv:2407.07895_ , 2024. 3 

- [31] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, Hang Li, and Tao Kong. Vision-language foundation models as effective robot imitators. In _The Twelfth International Conference on Learning Representations_ , 2024. 3 

- [32] Bang Liu, Zhe Wang, Zhi Ding, et al. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems (NeurIPS) — Datasets and Benchmarks Track_ , 2023. 3 

- [33] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Visual instruction tuning. _arXiv preprint arXiv:2304.08485_ , 2023. 3 

- [34] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation, 2025. 1, 5 

- [35] Yulin Liu, Bo Li, Chunyuan Li, et al. Mmbench: Is your multi-modal model an all-around player? In _Proceedings of the European Conference on Computer Vision (ECCV)_ , 2024. 3 

- [36] Jianlan Luo, Charles Xu, Fangchen Liu, Liam Tan, Zipeng Lin, Jeffrey Wu, Pieter Abbeel, and Sergey Levine. Fmb: a functional manipulation benchmark for generalizable robotic learning. _The International Journal of Robotics Research_ , 44 (4):592–606, 2025. 2 

- [37] Corey Lynch, Ayzaan Wahid, Jonathan Tompson, Tianli Ding, James Betker, Robert Baruch, Travis Armstrong, and Pete Florence. Interactive language: Talking to robots in real time, 2022. 3 

- [38] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, and Gavriel State. Isaac gym: High performance gpu-based physics simulation for robot learning, 2021. 2 

- [39] Runliang Niu, Jindong Li, Shiqi Wang, Yali Fu, Xiyu Hu, Xueyuan Leng, He Kong, Yi Chang, and Qi Wang. Screenagent: A vision language model-driven computer control agent, 2024. 1 

- [40] OpenAI. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 1, 3 

- [41] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models, 2025. 3 

- [42] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision. In _Proceedings of the 38th International Conference on Machine Learning (ICML)_ , pages 8748–8763, 2021. 3 

- [43] Hanoona Rasheed, Muhammad Maaz, Sahal Shaji Mullappilly, Abdelrahman Shaker, Salman Khan, Hisham Cholakkal, Rao M. Anwer, Eric Xing, Ming-Hsuan Yang, and Fahad Shahbaz Khan. Glamm: Pixel grounding large multimodal model. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 3 

- [44] Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, Tom Eccles, Jake Bruce, Ali Razavi, Ashley Edwards, Nicolas Heess, Yutian Chen, Raia Hadsell, Oriol Vinyals, Mahyar Bordbar, and Nando de Freitas. A generalist agent, 2022. 3 

- [45] Amrita Sawhney, Steven Lee, Kevin Zhang, Manuela Veloso, and Oliver Kroemer. Playing with food: Learning food item representations through interactive exploration. In _International Symposium on Experimental Robotics_ , pages 309– 322. Springer, 2020. 2 

- [46] Rutav Shah, Roberto Mart´ın-Mart´ın, and Yuke Zhu. Mutex: Learning unified policies from multimodal task specifications. _arXiv preprint arXiv:2309.14320_ , 2023. 2 

- [47] Haochen Shi, Huazhe Xu, Samuel Clarke, Yunzhu Li, and Jiajun Wu. Robocook: Long-horizon elasto-plastic object manipulation with diverse tools. _arXiv preprint arXiv:2306.14447_ , 2023. 2 

- [48] Alexey Stomakhin, Craig Schroeder, Lawrence Chai, Joseph Teran, and Andrew Selle. A Material Point Method for Snow Simulation. _ACM Trans. Graph._ , 32(4), 2013. 3 

- [49] D. Sulsky, Z. Chen, and H.L. Schreyer. A Particle Method for History-Dependent Materials. _Computer Methods in Applied Mechanics and Engineering_ , 118(1):179–196, 1994. 3 

- [50] Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse kai Chan, Yuan Gao, Xuanlin Li, Tongzhou Mu, Nan Xiao, Arnav Gurha, Viswesh Nagaswamy Rajesh, Yong Woo Choi, Yen-Ru Chen, Zhiao Huang, Roberto Calandra, Rui Chen, Shan Luo, and Hao Su. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai, 2025. 2, 4 

- [51] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, et al. Gemini robotics: Bringing ai into the physical world, 2025. 3 

- [52] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey 

7 

Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy, 2024. 

   - 5 

- [53] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe HansenEstruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale. _arXiv preprint arXiv:2308.12952_ , 2023. 3 

- [54] Chen Wang, Linxi Fan, Jiankai Sun, Ruohan Zhang, Li FeiFei, Danfei Xu, Yuke Zhu, and Anima Anandkumar. Mimicplay: Long-horizon imitation learning by watching human play. _arXiv preprint arXiv:2302.12422_ , 2023. 2 

- [55] Liquan Wang, Jiangjie Bian, Eric Heiden, and Animesh Garg. Topocut: Learning multi-step cutting with spectral rewards and discrete diffusion policies. _arXiv preprint arXiv:2509.19712_ , 2025. 1, 2, 3 

- [56] Stephanie Wang, Mengyuan Ding, Theodore F. Gast, Leyi Zhu, Steven Gagniere, Chenfanfu Jiang, and Joseph M. Teran. Simulation and visualization of ductile fracture with the material point method. _Proc. ACM Comput. Graph. Interact. Tech._ , 2(2), 2019. 3 

- [57] Joshuah Wolper, Yu Fang, Minchen Li, Jiecong Lu, Ming Gao, and Chenfanfu Jiang. CD-MPM: Continuum Damage Material Point Methods for Dynamic Fracture Animation. _ACM Trans. Graph._ , 38(4), 2019. 3 

- [58] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _The Twelfth International Conference on Learning Representations_ , 2024. 3 

- [59] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, Shichao Fan, Xinhua Wang, Fei Liao, Zhen Zhao, Guangyu Li, Zhao Jin, Lecheng Wang, Jilei Mao, Ning Liu, Pei Ren, Qiang Zhang, Yaoxu Lyu, Mengzhen Liu, Jingyang He, Yulin Luo, Zeyu Gao, Chenxuan Li, Chenyang Gu, Yankai Fu, Di Wu, Xingyu Wang, Sixiang Chen, Zhenyu Wang, Pengju An, Siyuan Qian, Shanghang Zhang, and Jian Tang. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation, 2025. 2 

shape morphing. _IEEE Transactions on Visualization and Computer Graphics_ , 31(10):9140–9153, 2025. 2 

   - [64] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ , 2023. 1 

   - [65] Zhejian Yang, Yongchao Chen, Xueyang Zhou, Jiangyue Yan, Dingjie Song, Yinuo Liu, Yuting Li, Yu Zhang, Pan Zhou, Hechang Chen, and Lichao Sun. Agentic robot: A brain-inspired framework for vision-language-action models in embodied agents, 2025. 3 

   - [66] Jiawen Yu, Hairuo Liu, Qiaojun Yu, Jieji Ren, Ce Hao, Haitong Ding, Guangyu Huang, Guofan Huang, Yan Song, Panpan Cai, et al. ForceVLA: Enhancing VLA models with a force-aware MoE for contact-rich manipulation. _arXiv preprint arXiv:2505.22159_ , 2025. 1, 3 

   - [67] Jianke Zhang, Yanjiang Guo, Yucheng Hu, Xiaoyu Chen, Xiang Zhu, and Jianyu Chen. Up-vla: A unified understanding and prediction model for embodied agent, 2025. 3 

   - [68] Ji Zhang, Shihan Wu, Xu Luo, Hao Wu, Lianli Gao, Heng Tao Shen, and Jingkuan Song. Inspire: Visionlanguage-action models with intrinsic spatial reasoning. _arXiv preprint arXiv:2505.13888_ , 2025. 3 

   - [69] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, He Wang, Zhizheng Zhang, Li Yi, Wenjun Zeng, and Xin Jin. Dreamvla: A vision-language-action model dreamed with comprehensive world knowledge. _CoRR_ , abs/2507.04447, 2025. 1 

   - [70] Xingcheng Zhou, Xuyuan Han, Feng Yang, Yunpu Ma, and Alois C. Knoll. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model, 2025. 3 

   - [71] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. _arXiv preprint arXiv:2304.10592_ , 2023. 3 

- [60] Yilin Wu, Ran Tian, Gokul Swamy, and Andrea Bajcsy. From foresight to forethought: Vlm-in-the-loop policy steering via latent alignment, 2025. 3 

- [61] Fei Xia, Amir R Zamir, Zhiyang He, Alexander Sax, Jitendra Malik, and Silvio Savarese. Gibson env: Real-world perception for embodied agents. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 9068–9079, 2018. 1 

- [62] Tian-Yu Xiang, Ao-Qun Jin, Xiao-Hu Zhou, Mei-Jiang Gui, Xiao-Liang Xie, Shi-Qi Liu, Shuang-Yi Wang, Sheng-Bin Duang, Si-Cheng Wang, Zheng Lei, and Zeng-Guang Hou. Vla model-expert collaboration for bi-directional manipulation learning, 2025. 3 

- [63] Michael Xu, Chang-Yong Song, David Levin, and David Hyde. A differentiable material point method framework for 

8 

