---
title: "Affordance Field Intervention: Enabling VLAs to Escape Memory Traps in Robotic Manipulation"
date: "2025-12-08"
authors: "Siyu Xu; Zijian Wang; Yunke Wang; Chenghao Xia; Tao Huang; Chang Xu"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2512.07472
pdf: https://arxiv.org/pdf/2512.07472
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.07472)** / [論文ページ](https://arxiv.org/abs/2512.07472)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Affordance Field Intervention: Enabling VLAs to Escape Memory Traps in Robotic Manipulation** 

Siyu Xu<sup>1</sup> Zijian Wang<sup>1</sup> Yunke Wang<sup>1</sup> Chenghao Xia<sup>3</sup> Tao Huang<sup>2</sup> Chang Xu<sup>1†</sup> 1The University of Sydney 2 Shanghai Jiao Tong University 3StellarEdge Robotics 

_{_ s.xu,yunke.wang,c.xu _}_ @sydney.edu.au, t.huang@sjtu.edu.cn 


Figure 1. **Memory Trap in VLAs.** VLAs often fail under distribution shifts. In such a case, they replay trajectories memorized during training instead of adapting to the updated scene. In both Case 1 and Case 2, even though the target object moves, the VLA drives the end-effector toward the original location, ignoring new spatial cues. 

## **Abstract** 

_Vision-Language-Action (VLA) models have shown great performance in robotic manipulation by mapping visual observations and language instructions directly to actions. However, they remain brittle under distribution shifts: when test scenarios change, VLAs often reproduce memorized trajectories instead of adapting to the updated scene, which is a failure mode we refer to as the “Memory Trap”. This limitation stems from the end-to-end design, which lacks explicit 3D spatial reasoning and prevents reliable identification of actionable regions in unfamiliar environments. To compensate for this missing spatial understanding, 3D Spatial Affordance Fields (SAFs) can provide a geometric representation that highlights where interactions are physically feasible, offering explicit cues about regions the robot should approach or avoid. We therefore introduce Affordance Field Intervention (AFI), a lightweight hybrid framework that uses SAFs as an on-demand plugin to guide VLA behavior. Our system detects memory traps through proprioception, repositions the robot to recent_ 

_high-affordance regions, and proposes affordance-driven waypoints that anchor VLA-generated actions. A SAFbased scorer then selects trajectories with the highest cumulative affordance. Extensive experiments demonstrate that our method achieves an average improvement of 23.5% across different VLA backbones (π_ 0 _and π_ 0 _._ 5 _) under out-ofdistribution scenarios on real-world robotic platforms, and 20.2% on the LIBERO-Pro benchmark, validating its effectiveness in enhancing VLA robustness to distribution shifts. Project page: https://vla-afi.github.io/._ 

## **1. Introduction** 

Vision-Language-Action (VLA) models [5, 8, 22] have emerged as powerful motion planners in robotic manipulation, directly mapping visual observations and linguistic instructions to executable action sequences and enabling seamless interaction with objects in diverse environments. By leveraging large-scale pre-trained vision-language foundations, these end-to-end neural architectures facilitate generalization across tasks, such as grasping and object rearrangement, without requiring extensive task-specific engi- 

> _†_ Corresponding Author 

37206 

neering [4, 15, 21]. 

Despite these advancements, VLA models encounter substantial challenges in generalization, frequently succumbing to a “Memory Trap” [6, 7, 47]. In out-ofdistribution (OOD) scenarios, such as significant perturbations in object positions, these models tend to rigidly reproduce trajectories memorized from the training data. Consequently, this suboptimal behavior leads to task failure, as the model directs the end-effector toward obsolete positions rather than the actual updated target. This limitation stems from VLA’s end-to-end design, which implicitly fits mappings from vision-language inputs to actions based on training distributions, without explicitly perceiving and reasoning over 3D regions for interaction [23, 36, 46]. As a result, VLAs lack the planning capabilities to generate actions that target the appropriate regions in unfamiliar environments. Instead, they rely on memorized trajectories from training, which fail to adapt to perturbations [11, 28]. 

Recent works have introduced the concept of affordance to guide action planning. An object’s affordance, described as “opportunities of interaction”, provides direct and intuitive guidance in robot workspace [1, 10, 20, 42]. By leveraging multimodal understanding and reconstruction techniques, these methods generate 3D spatial affordance fields (SAFs) that highlight actionable regions [12, 13]. Once the SAF identifies target endpoints, non-learningbased methods such as optimization-based trajectory planning can generate dynamically feasible action trajectories [16, 35, 44]. However, these VLM-based planning approaches [12, 13] suffer from low success rates in practice due to two critical limitations: (1) unreliable VLMgenerated motion plans that lack fine-grained geometric understanding and often produce infeasible actions [3, 34], (2) heavy reliance on task-specific prompt engineering to generate diverse constraints, which are brittle and lack transferability across different manipulation scenarios [26, 38]. 

To overcome these challenges, we propose Affordance Field Intervention (AFI), a novel hybrid framework that treats a 3D SAF as a plug-in for VLA-based action generation. The core of our method lies in how to leverage the SAF to help the VLA escape the memory trap and navigate toward high-affordance regions, thereby improving task success rates. First, we design a memory trap detection mechanism using robot proprioception. By monitoring end-effector motion patterns and goal progress, our system identifies when the VLA falls into rigid, memorized trajectories that fail to adapt to environmental changes. Second, upon detecting the memory trap, the AFI rolls back the EEF to a recent high-affordance position for safe repositioning under the guidance of the SAF. From there, it proposes intermediate waypoints as nearby high-affordance points that progressively guide toward the target region (e.g., updated object location). These waypoints act as geometric anchors, 

breaking the VLA’s rigid memorization with explicit spatial cues. 

Finally, the VLA is queried to generate action proposals conditioned on these SAF-guided waypoints.To ensure spatial optimality, the SAF acts as a scorer, evaluating and re-ranking the VLA’s action candidates based on their projected trajectories’ cumulative affordance values. The action with the highest affordance value, indicating alignment with favorable paths, is selected for execution. This closedloop modular integration allows the VLA to leverage its semantic understanding and efficiency while being softly constrained by 3D geometry through grounded interventions. It enables adaptive navigation to high-affordance regions _without parameter updates_ , effectively bridging data-driven policies with interpretable planning. 

We conduct extensive experiments on both real-world robotic platforms and simulation benchmarks to validate our proposed AFI. On real-world manipulation tasks using an AgileX Piper manipulator, our method achieves consistent improvements across four diverse tasks, with average success rate gains ranging from 17.0% to 26.0% over baseline VLA policies ( _π_ 0 and _π_ 0 _._ 5) under various OOD scenarios including position shifts, color changes, object variations, and background shifts. Our framework also demonstrates model-agnostic generalization, with ensemble integration of multiple VLA backbones achieving up to 89.0% success rate. On LIBERO-Pro [47] simulation with spatial perturbations, our method improves _π_ 0 _._ 5 by 21.7% (Spatial) and 16.8% (Object). These results validate that AFI effectively mitigates the memory trap problem and enhances VLA robustness to distribution shifts without requiring model retraining or additional demonstration data. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

Vision-Language-Action (VLA) models [5, 8, 22] have emerged as a promising approach for general-purpose robotic manipulation. These models frame robot control as a sequence modeling task, trained end-to-end via imitation learning on large datasets of camera observations, language instructions, and actions. However, a significant body of recent literature highlights that these models suffer from poor generalization and inherent fragility when faced with spatial perturbations or novel environments [6, 7, 47]. Research suggests that existing VLA models often struggle with robust action planning in unseen contexts, relying heavily instead on memorized or imitated trajectories from their training data distribution [2, 9], especially when trained on imperfect demonstrations of varying quality [39].Orthogonal efforts focus on improving VLA inference efficiency through adaptive token caching [30, 41] and visual token reduction [31, 40], which reduce compu- 

37207 

tational costs but do not address the spatial generalization limitations. 

Recent studies also explored the integration of reinforcement learning (RL) to enhance the generalization capabilities of VLA models [25, 28, 29, 43]. By incorporating RL-based fine-tuning, these approaches aim to adapt VLA policies to diverse and unseen scenarios beyond mere imitation. However, a key challenge lies in obtaining reliable reward signals for RL training [17, 24], which often requires extensive human annotation or complex simulation environments. Moreover, scaling RL to large-scale datasets and diverse environments remains a significant challenge, limiting its practicality for real-world robotic applications [29, 45]. 

### **2.2. Grounding 3D Affordance and Action Planning** 

Grounding 3D affordances plays a pivotal role in robotic manipulation by bridging language instructions with actionable spatial representations, enabling agents to infer object interactions (e.g., graspable regions or avoidance zones) directly in the 3D perceptual space [1, 14, 19]. Grounding 3D affordances explicitly encodes target object locations and interaction cues into dense spatial maps, allowing action planning to be offloaded to these affordance maps. 

Building on this, VoxPoser [12] is a novel framework that leverages large language models (LLMs) and visionlanguage models (VLMs) to compose composable 3D value maps for zero-shot manipulation tasks. Geomanip [37] uses geometric constraints as general interfaces for robot manipulation, allowing agents to reason about object interactions and plan actions in a more principled manner. GIGA [18] is a structured implicit representation that couples 3D reconstruction with an affordance field for 6-DoF grasping, grounding action cues directly in local geometry. By training the shared implicit functions on self-supervised trials, it improves occlusion-robust grasp detection and allocates representation capacity toward graspable regions, enabling more reliable action planning in clutter. 

## **3. Preliminary** 

In this section, we introduce the background knowledge of VLA models and affordance field construction. 

### **3.1. VLA Models** 

VLA models _π_ VLA take a 2D image _It_<sup>_rgb_</sup> at timestep _t_ and language instructions _τ_ as inputs to propose actions for environment interaction. These actions are executed by the controller, results in an end-effector (EEF) displacement ∆ **d** _t_ in the 3D workspace, i.e., 


VLA models are typically trained using imitation learning, memorizing direct mappings from vision-language inputs 


Figure 2. **Spatial Affordance Field (SAF) Construction.** (a) GPT-4o decomposes the task instruction into sequential stages and identifies the current target object (e.g., “carrot” or “blue pan”). (b) The target text is fed to Grounded-SAM for segmentation, and the resulting 2D mask is back-projected into 3D space to construct the SAF, where color gradients indicate affordance values. 

to actions based on the training distribution. However, in out-of-distribution (OOD) scenarios, the VLA model continues to propose actions that guide the end-effector along the memorized trajectories from the training set, rather than adapting to the perturbed environment. 

### **3.2. Affordance Field Construction** 

In this subsection, we introduce the two-stage pipeline for constructing the 3D spatial affordance field (SAF). 

#### **3.2.1. Inferring Affordance via VLM** 

To infer affordances from language instructions, we first identify task-relevant objects and then project them into the robot’s workspace. Given a high-level task instruction _τ_ (e.g., “place the mug on the table”) and the current RGB observation _It_<sup>_rgb_</sup> , we leverage a vision-language model (VLM) to parse the task into a sequence of semantic stages. Specifically, we use GPT-4o to decompose _τ_ into temporally ordered sub-goals (e.g., _pick → move → place_ ) and extract stage-wise target tokens (e.g., “mug”, “table”). These target tokens serve as text prompts for subsequent open-vocabulary object detection. 

Then for each sub-goal, we apply Grounded-SAM [33] to generate a 2D segmentation mask _M_ target _∈{_ 0 _,_ 1 _}_<sup>_H×W_</sup> corresponding to the target object. By combining _M_ target with the depth map _It_<sup>_depth_</sup> and camera intrinsic parameters, we back-project the masked region into 3D space to obtain the target point cloud _P_ target = _{_ **p** _i ∈_ R<sup>3</sup> _}_ . Notably, when 

37208 


Figure 3. **Overview of Affordance Field Intervention (AFI).** (1) _Memory Trap Detection:_ SAF evaluates VLA-predicted actions and detects memory traps by monitoring end-effector displacement and distance to target. (2) _Trajectory Rollback:_ Upon detection, the robot rolls back to the historical position with lowest SAF cost before grasping attempts. (3) _SAF-Guided Sampling:_ VLA generates trajectory candidates at SAF-sampled waypoints, and the trajectory with lowest cumulative SAF cost is selected for execution. 

the VLM detects a sub-goal transition during execution, the system automatically updates the target identification to reflect the new semantic focus, allowing the spatial affordance field to adapt dynamically throughout multi-stage manipulation tasks. 

#### **3.2.2. Grounding Affordance in 3D Space** 

We discretize the robot’s workspace into an _N × N × N_ voxel grid _V_ , where each voxel _vijk_ represents a small cuboid region in 3D space. Both the scene point cloud _P_ scene (obtained from the full RGB-D observation) and the target object point clouds _P_ target are projected onto this grid. Within this voxelized representation, we construct two complementary geometric subfields for each target object: 

**1) Target Guidance Field** _V_ target: This field encodes spatial attraction toward the target. For each voxel _vijk_ , we compute its Euclidean distance _d_ ( _vijk,_ **c** target) to the target object centroid **c** target = _|P_ target1 _|_ � **p** _∈P_ target<sup>**p**.After applying</sup> distance transform, regions farther from the target receive higher values, which contribute to higher cost in the final affordance field, encouraging the EEF to approach the goal region. 

**2) Obstacle Avoidance Field** _V_ obst: This field encodes repulsion from scene obstacles. Voxels occupied by _P_ scene or near obstacles are assigned high values to discourage collision. To prevent overly conservative behavior, we apply heuristic masking: (1) we exempt the immediate vicinity of the EEF, allowing close-range manipulation, and (2) we create a buffer zone around the target object, permitting approach actions necessary for grasping. 

The final spatial affordance field _V_ SAF is obtained by fus- 

ing these subfields via weighted linear combination: 


where _w_ target and _w_ obst are hyperparameters balancing target attraction and obstacle avoidance. To ensure smooth spatial gradients suitable for trajectory evaluation, we apply Euclidean distance transform to both subfields, followed by Gaussian smoothing with kernel size _σ_ . Finally, _V_ SAF is normalized to [0 _,_ 1], yielding a continuous affordance cost field where lower values indicate more favorable regions (near targets and away from obstacles) for action selection. 

## **4. Method** 

In this section, we introduce our proposed AFI that integrates the spatial affordance field (SAF) into the VLA workflow to help the VLA model escape the memory trap in outof-distribution scenarios. We first describe how to detect whether the robot has fallen into the memory trap. Then, we explain how to integrate the SAF to intervene in the VLA workflow for escaping the memory trap. 

### **4.1. Memory Trap Detection** 

We monitor the robot’s execution status at each timestep to detect potential memory traps. A memory trap is triggered when two conditions are simultaneously met: (1) the endeffector displacement _∥_ **p** _t −_ **p** _t−_ ∆ _t∥_ falls below a threshold _ϵ_ stuck over a time window ∆ _t_ , and (2) the distance to the target _∥_ **p** _t −_ **c** target _∥_ exceeds a threshold _ϵ_ far. The first condition detects when the robot enters a quasi-static state, which typically indicates either fine-grained manipulation 

37209 

near the target (e.g., grasping) or getting stuck in an undesired configuration. The second condition disambiguates these two scenarios: if the end-effector becomes stationary while still far from the target, it suggests the robot is stuck or performing incorrect actions (e.g., grasping the wrong object), rather than executing the intended fine manipulation. This dual-criterion detection ensures we intervene only when genuine memory traps occur, avoiding false positives during legitimate stationary behaviors near the goal. 

### **4.2. Affordance Field Intervention** 

Upon detecting a memory trap, the spatial affordance field (SAF) immediately comes into play through a targeted intervention mechanism, guiding the escape from the trap and steering the VLA model away from its memorized trajectories. This intervention begins with a guided rollback to a safer historical position, followed by a tree-based, SAFguided search that samples intermediate waypoints toward high-affordance regions and integrates VLA-generated trajectories for task-directed refinement. 

#### **4.2.1. Historical Rollback via Affordance** 

We maintain a history buffer of length _M_ over recent endeffector positions: **P** hist = _{_ **p** _t−M , . . . ,_ **p** _t−_ 1 _}_ . The rollback target is selected as the historical point with the lowest affordance cost: 


where _V_ SAF( **p** ) queries the SAF at position **p** , with lower values indicating lower cost (safer and more task-relevant regions). The robot executes a short rollback trajectory to return to this configuration **p** rollback, which serves as the root node for subsequent tree-based trajectory extension. This step repositions the robot to a safer, low-cost state, mitigating the immediate effects of the memory trap. 

#### **4.2.2. Hierarchical Exploration for Optimal Trajectories** 

Starting from the rollback position **p** rollback, we construct a two-stage tree-based exploration process to sample intermediate waypoints toward high-affordance regions and integrate VLA-generated trajectories for task-directed refinement. 

**Stage 1: Local SAF-Guided Sampling of Intermediate Waypoints.** We perform a local spatial search to identify _N_ promising intermediate waypoints in the vicinity. Specifically, we sample candidate positions from a local neighborhood _N_ ( **p** rollback _, r_ ) with radius _r_ and select those with the lowest cost values: 


where arg min<sup>_N_</sup> selects the _N_ positions with minimum cost values. These waypoints form the first-level child nodes 

in the trajectory extension tree, representing spatially favorable intermediate targets that prioritize low-cost regions near targets and away from obstacles. 

**Stage 2: Trajectory Generation via VLA at Sampled Waypoints.** The robot sequentially navigates to each waypoint **p**<sup>way</sup> _i_ and queries the VLA policy _π_ VLA to produce _K_ diverse action candidates _{_ **a** _i,k}_<sup>_K_</sup> _k_ =1<sup>basedontheupdated</sup> observation _It_<sup>rgb</sup> and task instruction _τ_ . For stochastic policies (e.g., diffusion-based), candidates are sampled with different noise temperature or seeds. 

Each action candidate **a** _i,k_ represents an action chunk consisting of a sequence of joint states over horizon _H_ . We apply forward kinematics to convert these joint states into the corresponding end-effector trajectory **_ξ_** _i,k_ = _{_ **p**<sup>_i,k_</sup> _j_<sup>_}_</sup> _j_<sup>_H_</sup> =1<sup>,</sup> where **p**<sup>_i,k_</sup> _j_ denotes the end-effector position at timestep _j_ . The cumulative affordance cost is: 


This yields _N × K_ evaluated candidates forming the leaf nodes of the trajectory tree. We then select the globally optimal trajectory by minimizing the cumulative cost: 


The robot executes **_ξ_**<sup>_∗_</sup> by navigating to its corresponding waypoint and following the associated VLA actions. This hierarchical, exploration-driven approach effectively combines the spatial reasoning of SAF (for waypoint selection) with the task-specific capabilities of VLA (for trajectory completion), enabling robust recovery from diverse failure modes while incorporating real-world perceptual feedback. 

## **5. Experiments** 

### **5.1. Experimental Settings** 

**Environments.** We evaluate our framework on both realworld robotic platforms and simulated environments. For real-world experiments, we employ an AgileX Piper manipulator equipped with two Intel RealSense D435 cameras. For simulation experiments, we utilize the LIBERO benchmark [27] with spatial perturbations following LIBEROPro [47] to assess OOD generalization. Detailed hardware configuration, SAF construction procedures, and training details are provided in Appendix A. **Baselines.** We compare our method against pre-trained VLA models without 3D SAF guidance: _π_ 0 [4] and _π_ 0 _._ 5 [15] in real-world experiments, and the officially released _π_ 0 _._ 5-LIBERO checkpoint in simulation. We also evaluate on OpenVLA-OFT [22] and SpatialVLA [32] (3Daware VLA backbone that incorporates depth features) to verify backbone-agnostic effectiveness. We also compare 

37210 

Table 1. Real-world experimental results on AgileX Piper manipulator across four manipulation tasks. We report success rates over 20 trials for each scenario. Our AFI framework achieves consistent improvements across all distribution shifts and VLA backbones. See Appendix B for detailed task descriptions. 

|**Task**|**Method**|**In Dist.**|**Position**|**Color**|**Task**|**Background**|**Average SR.**|
|---|---|---|---|---|---|---|---|
||ReKep [13]|8/20|7/20|9/20|5/20|7/20|36.0%|
|**Place Carrot**|_π_0|17/20|6/20|13/20|15/20|10/20|61.0%|
||_π_0-AFI(Ours)|**20/20**|**13/20**|**17/20**|**18/20**|**19/20**|**87.0%** (_↑_26.0%)|
|**R Lid**|_π_0|20/20|8/20|17/20|5/20|13/20|63.0%|
|**emove**|_π_0-AFI(Ours)|**20/20**|**12/20**|**19/20**|**11/20**|**18/20**|**80.0%** (_↑_17.0%)|
|**Slt P**|_π_0|16/20|11/20|13/20|15/20|5/20|60.0%|
|**o en**|_π_0-AFI(Ours)|**19/20**|**16/20**|**16/20**|**19/20**|**12/20**|**82.0%** (_↑_22.0%)|
||_π_0|18/20|9/20|16/20|13/20|8/20|64.0%|
||_π_0-AFI(Ours)|**20/20**|**15/20**|**20/20**|**17/20**|**14/20**|**86.0%** (_↑_22.0%)|
|**Stack Tape**|_π_0_._5|20/20|7/20|17/20|10/20|7/20|61.0%|
||_π_0_._5-AFI (Ours)|**20/20**|**14/20**|**19/20**|**15/20**|**14/20**|**82.0%**(_↑_21.0%)|
||_π_0+_π_0_._5-AFI(Ours)|**20/20**|**16/20**|**20/20**|**16/20**|**17/20**|**89.0%** (_↑_25.0%)|


Figure 4. **Real-world AFI execution rollout.** Top: Memory trap detected at _t_ = 50 when approaching wrong location, followed by rollback to low-cost historical position. Bottom: SAF-guided sampling ( _t_ = 70-79) generates trajectory candidates; optimal trajectory (green) is selected and executed ( _t_ = 80-90) for successful completion. 

with ReKep [13], a training-free VLM-based planner based on 3D waypoints, to demonstrate the advantages of our hybrid VLA+SAF approach. 

**Tasks.** We evaluate on four real-world manipulation tasks covering diverse primitives: (1) _Place Carrot_ : picking up a carrot and placing it in a pot; (2) _Remove Lid_ : removing a lid from a pot and placing it on a platter; (3) _Slot Pen_ : inserting a pen into a holder; (4) _Stack Tape_ : stacking one tape roll on top of another; (5) _Remove Lid and Place Carrot_ (long-horizon task): remove the pot lid and place the carrot inside the pot. 

Each task is evaluated over 20 trials under five test conditions: in-distribution (ID) and four OOD scenarios involving position shifts ( _±_ 5-15cm), color/appearance changes, object property variations, and background shifts. Taskspecific descriptions, training data details, and OOD scenario definitions are provided in Appendix B and Figure 7 & 8. 

### **5.2. Main Results in Real World** 

Table 1 presents comprehensive results across four manipulation tasks and various distribution shift scenarios. Our AFI framework achieves consistent improvements across all tasks and VLA backbones, with average success rate gains ranging from 17.0% to 26.0% over baseline policies. 

**Consistent Improvements Across Tasks.** Our method demonstrates robust performance gains across all manipulation primitives. For _Place Carrot_ , _π_ 0-AFI achieves 87.0% average success rate versus 61.0% baseline, with particularly strong improvements in Position shift (65% vs 30%) and Background shift (95% vs 50%) scenarios. For _Stack Tape_ , we observe 86.0% success rate with _π_ 0-AFI compared to 64.0% baseline, achieving perfect success (100%) in Color shift scenarios. The _Slot Pen_ task shows 82.0% success (22.0% gain), while _Remove Lid_ achieves 80.0% (17.0% gain). 

Beyond single-stage tasks, our method also generalizes to long-horizon manipulation: on the two-stage _Remove Lid and Place Carrot_ task (Table 8), AFI achieves +20% and +16.2% average improvement for _π_ 0 and _π_ 0 _._ 5 respectively, with detailed analysis in Appendix C.3. These results validate that our SAF-guided intervention effectively handles diverse manipulation primitives as well as their sequential compositions. Figure 4 visualizes a typical AFI execution rollout. 

**Robustness to Challenging Distribution Shifts.** The Task shift scenarios present the most challenging OOD conditions, involving physical property variations and distractors. Our method shows substantial improvements: 30.0% gain for _Remove Lid_ with distractor avoidance (from 25% to 55%), 20.0% gain for _Slot Pen_ with thinner pen insertion (from 75% to 95%), and 20.0% gain for _Stack Tape_ with different tape types (from 65% to 85%). Position shift scenarios also benefit significantly, with average improve- 

37211 


Figure 5. Visualization of object position perturbations in LIBERO simulation, where the target object “black bowl on the cookie box” is displaced to significantly deviated positions. 

ments of 25.0% across tasks, demonstrating that our SAF provides effective 3D spatial reasoning to locate displaced objects. We further evaluate under cluttered scenes with 3–5 distractors on the Long-horizon task (Figure 8), where AFI improves both _π_ 0 and _π_ 0 _._ 5 by _∼_ 25%, confirming effectiveness in distractor-rich environments (see Appendix C.3). **Comparison with Zero-Shot VLM Planner.** ReKep [13], a training-free VLM-based planner, achieves only 36.0% average success rate on the _Place Carrot_ task. While VLMs excel at semantic understanding, they lack fine-grained motion planning capabilities required for precise manipulation. In contrast, our hybrid approach achieves 87.0% by leveraging VLMs’ zero-shot grounding abilities to construct SAFs as guidance while relying on VLA models for robust action generation, combining their complementary strengths. **Generalization Across VLA Backbones.** We evaluate both _π_ 0 and _π_ 0 _._ 5 on the _Stack Tape_ task. Both achieve similar baseline performance (64.0% and 61.0%), and our AFI improves them to comparable levels (86.0% and 82.0%). Beyond flow-matching VLAs, we further evaluate on OpenVLA-OFT [22] (auto-regressive) and SpatialVLA [32] (3D-aware with depth features), achieving +20% and +25% average improvements respectively (Table 7). These results validate the model-agnostic nature of our approach; detailed per-condition analysis is provided in Appendix C.2. 

**Ensemble Integration for Enhanced Performance.** We further explore ensemble integration by combining action proposals from both _π_ 0 and _π_ 0 _._ 5 backbones, where our SAF-based scorer selects the optimal trajectory from the combined candidate pool. As shown in Table 1, the ensemble approach ( _π_ 0+ _π_ 0 _._ 5-AFI) achieves 89.0% average success rate on _Stack Tape_ , outperforming both individual backbones ( _π_ 0-AFI: 86.0%, _π_ 0 _._ 5-AFI: 82.0%) and representing a 25.0% improvement over baseline _π_ 0 (64.0%). This demonstrates a key advantage of our framework: its model-agnostic design naturally supports multi-policy integration, leveraging complementary strengths from different VLA architectures without complex fusion mechanisms. 

Table 2. Success rates of _π_ 0 _._ 5-AFI and _π_ 0 _._ 5 on the LIBEROSpatial and LIBERO-Object, with object position perturbations introduced to subtask following the LIBERO-Pro protocol. 

|**LIBERO-Spatial(OOD)**|||
|---|---|---|
|Task|_π_0_._5|_π_0_._5-AFI|
|Pick(between(plate, ramekin), plate)|70.0%|**82.0**%|
|Pick(next<br>~~t~~o(ramekin), plate)|22.0%|**54.0**%|
|Pick(table<br>~~c~~enter, plate)|96.0%|**98.0**%|
|Pick(on(cookie<br>~~b~~ox), plate)|74.0%|**88.0**%|
|Pick(on(ramekin), plate)|26.0%|**54.0**%|
|Pick(next<br>~~t~~o(cookie<br>~~b~~ox), plate)|36.0%|**72.0**%|
|Pick(next<br>~~t~~o(plate), plate)|54.0%|**82.0**%|
|Average|54.0%|**75.7**%|
|**LIBERO-Object(OOD)**|||
|Task|_π_0_._5|_π_0_._5-AFI|
|Place(alphabet<br>~~s~~oup, basket)|42.0%|**64.0**%|
|Place(bbq<br>~~s~~auce, basket)|54.0%|**72.0**%|
|Place(butter, basket)|78.0%|**82.0**%|
|Place(chocolate<br>~~p~~udding, basket)|88.0%|**90.0**%|
|Place(cream<br>~~c~~heese, basket)|42.0%|**56.0**%|
|Place(ketchup, basket)|46.0%|**66.0**%|
|Place(milk, basket)|88.0%|**92.0**%|
|Place(orange<br>~~j~~uice, basket)|70.0%|**80.0**%|
|Place(salad<br>~~d~~ressing, basket)|16.0%|**64.0**%|
|Place(tomato<br>~~s~~auce,basket)|40.0%|**66.0**%|
|Average|56.4%|**73.2**%|


### **5.3. Main Results in Simulation** 

For LIBERO simulation experiments, we evaluate our method on the LIBERO-Pro [47] benchmark by introducing spatial perturbations to target object positions in each subtask, following the OOD evaluation protocol from LIBERO-Pro. 

Table 2 reports the success rates of our method compared to the baseline _π_ 0 _._ 5 model on the LIBERO-Spatial and LIBERO-Object suites, broken down by each subtask. Our SAF-guided framework demonstrates substantial improvements across most subtasks, particularly in scenarios involving spatial perturbations, achieving an average success rate of 78.2% on LIBERO-Spatial (vs. 52.4% for _π_ 0 _._ 5) and 82.5% on LIBERO-Object (vs. 67.3% for _π_ 0 _._ 5). These results underscore the effectiveness of affordance-guided interventions in enhancing VLA generalization to out-ofdistribution object configurations and positional shifts in simulation environments. 

**Computational Efficiency.** Our framework introduces minimal overhead to the baseline VLA inference. SAF reconstruction takes 120 ms per frame using Grounded-SAM and point cloud processing on an NVIDIA RTX 4090, while waypoint generation and action re-ranking add 15 ms total. This results in an end-to-end latency of 185 ms, suitable for 5 Hz control rates in real-world deployment. In contrast, pure optimization-based methods like MPC require 500+ 

37212 


Figure 6. **SAF value evolution across manipulation tasks.** Lower cost values indicate higher affordance. Costs decrease when approaching targets and update dynamically during stage transitions (e.g., picking to placing). 

ms per planning step, limiting their applicability to highfrequency manipulation. 

### **5.4. Ablations** 

**SAF adaptation throughout task execution.** To validate that our SAF accurately reflects task-relevant spatial information, we analyze its cost evolution throughout complete trajectories (Figure 6). The curves demonstrate that SAF cost decreases as the end-effector approaches target objects, validating that our affordance field accurately reflects spatial proximity to manipulation goals. Notably, the cost values exhibit dynamic updates when transitioning between manipulation stages (e.g., from picking the lid to placing it in the platter), showing that our system adaptively adjusts the affordance field based on current task semantics. **Ablation on key components.** Table 3 validates the importance of individual components on the position shift scenario. Removing rollback degrades performance from 65% to 40%, demonstrating its critical role. Without it, the VLA deviates too far from viable trajectories, and SAF-guided waypoints cannot recover from failed positions. Rollback repositions the end-effector to a recent high-affordance state, providing a safe starting point for effective redirection. Fixed-step interventions achieve at most 60% (Step 30), underperforming our adaptive detection (65%). This validates that real-time proprioceptive monitoring enables 

Table 3. Ablation study on key components: (1) rollback mechanism and (2) adaptive detection vs. fixed-step intervention. All experiments on position shift scenario over 20 trials. 

|Method|Success|Failure|
|---|---|---|
|_π_0|6/20|14/20|
|_π_0-AFI|**13/20**|7/20|
|w/o Rollback|8/20|12/20|
|Fixed-step at 30|12/20|8/20|
|Fixed-step at 60|11/20|9/20|
|Fixed-stepat 90|9/20|11/20|
|Table 4. Ablation on way|point count with|different numbers of|
|SAF-sampled candidates.|||
|Num of Waypoints|3<br>8|10<br>13|
|Success Rate<br>3|5.0%<br>50.0%|65.0%<br>60.0%|


flexible intervention precisely when memory traps occur, optimizing both efficiency and success rate. **Impact of waypoint proposal count.** Table 4 examines how the number of waypoint proposals affects performance. With only 3 proposals, success rate remains low at 35%, barely improving over the baseline. Optimal performance is achieved at 10 proposals (65%), balancing spatial exploration and computational efficiency. Further increasing to 13 proposals shows marginal degradation (60%). This is because SAF waypoints form a straight-line path toward the target centroid, designed for spatial guidance rather than grasp planning. When too many waypoints are used, the VLA becomes over-constrained along this straight path, which scores highest under our SAF metric but is often suboptimal for actual grasping. We find that 10 waypoints strike a good balance between providing sufficient guidance to escape memory traps and preserving VLA autonomy for flexible grasp execution. 

## **6. Conclusion** 

We identified the “Memory Trap” problem where VLAs rigidly reproduce memorized trajectories under distribution shifts. To address this, we proposed Affordance Field Intervention (AFI), which augments VLA models with explicit 3D spatial reasoning via Spatial Affordance Fields. AFI operates through proprioceptive memory trap detection, guided rollback to high-affordance positions, and hierarchical trajectory exploration via SAF-guided waypoint sampling. By treating SAF as an on-demand plug-in without modifying VLA parameters, our method is model-agnostic and applicable to any pre-trained VLA backbone. Extensive experiments demonstrate significant improvements: 23.5% average gain on real-world OOD scenarios and 20.2% on LIBERO-Pro benchmark. The training-free nature makes it practical for deployment without additional data or finetuning. Our work shows that combining VLA policies with interpretable 3D spatial affordance fields offers a promising path toward more robust and generalizable robotic manipulation systems. 

37213 

## **Acknowledgments** 

This work was supported in part by the Australian Research Council under Projects DP240101848 and FT230100549, and by Australia’s Economic Accelerator Ignite Program under Project IG250200386. This research was supported by the resources and services provided by the National Computational Infrastructure (NCI), Australia. We would also like to thank the anonymous reviewers and area chair for their constructive feedback, which helped improve the clarity and quality of this paper. 

## **References** 

- [1] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 2, 3 

- [2] Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh. Data quality in imitation learning. _ArXiv_ , abs/2306.02437, 2023. 2 

- [3] Marc G Bellemare, Salvatore Candido, Pablo Samuel Castro, Jun Gong, Marlos C Machado, Subhodeep Moitra, Sameera S Ponda, and Ziyu Wang. Autonomous navigation of stratospheric balloons using reinforcement learning. _Nature_ , 588(7836):77–82, 2020. 2 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 2, 5 

- [5] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. _URL https://arxiv. org/abs/2307.15818_ , 2024. 1, 2 

- [6] Irving Fang, Juexiao Zhang, Shengbang Tong, and Chen Feng. From intention to execution: Probing the generalization boundaries of vision-language-action models. _arXiv preprint arXiv:2506.09930_ , 2025. 2 

- [7] Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, et al. Libero-plus: In-depth robustness analysis of visionlanguage-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 2 

- [8] Roya Firoozi, Johnathan Tucker, Stephen Tian, Anirudha Majumdar, Jiankai Sun, Weiyu Liu, Yuke Zhu, Shuran Song, Ashish Kapoor, Karol Hausman, et al. Foundation models in robotics: Applications, challenges, and the future. _The International Journal of Robotics Research_ , 44(5):701–739, 2025. 1, 2 

- [9] Dylan J. Foster, Adam Block, and Dipendra Kumar Misra. Is behavior cloning all you need? understanding horizon in imitation learning. _ArXiv_ , abs/2407.15007, 2024. 2 

- [10] James J Gibson. The ecological approach to the visual perception of pictures. _Leonardo_ , 11(3):227–235, 1978. 2 

- [11] Shresth Grover, Akshay Gopalkrishnan, Bo Ai, Henrik I Christensen, Hao Su, and Xuanlin Li. Enhancing generalization in vision-language-action models by preserving pretrained representations. _arXiv preprint arXiv:2509.11417_ , 2025. 2 

- [12] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 2, 3 

- [13] Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Li Fei-Fei. Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. _arXiv preprint arXiv:2409.01652_ , 2024. 2, 6, 7 

- [14] Wei-Jin Huang, Yue-Yi Zhang, Yi-Lin Wei, Zhi-Wei Xia, Juantao Tan, Yuan-Ming Li, Zhilin Zhao, and Wei-Shi Zheng. Learning whole-body human-humanoid interaction from human-human demonstrations. _arXiv preprint arXiv:2601.09518_ , 2026. 3 

- [15] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 2, 5 

- [16] Mazeyu Ji, Ri-Zhao Qiu, Xueyan Zou, and Xiaolong Wang. Graspsplats: Efficient manipulation with 3d feature splatting. _arXiv preprint arXiv:2409.02084_ , 2024. 2 

- [17] Anqing Jiang, Yu Gao, Yiru Wang, Zhigang Sun, Shuo Wang, Yuwen Heng, Hao Sun, Shichen Tang, Lijuan Zhu, Jinhao Chai, et al. Irl-vla: Training an vision-languageaction policy via reward world model. _arXiv preprint arXiv:2508.06571_ , 2025. 3 

- [18] Zhenyu Jiang, Yifeng Zhu, Maxwell Svetlik, Kuan Fang, and Yuke Zhu. Synergies between affordance and geometry: 6-dof grasp detection via implicit representations. _arXiv preprint arXiv:2104.01542_ , 2021. 3 

- [19] Zhenyu Jiang, Cheng-Chun Hsu, and Yuke Zhu. Ditto: Building digital twins of articulated objects from interaction. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 5616–5626, 2022. 3 

- [20] Yuanchen Ju, Kaizhe Hu, Guowei Zhang, Gu Zhang, Mingrun Jiang, and Huazhe Xu. Robo-abc: Affordance generalization beyond categories via semantic correspondence for robot manipulation. In _European Conference on Computer Vision_ , pages 222–239. Springer, 2024. 2 

- [21] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 2 

- [22] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 5, 7, 13 

- [23] Chengmeng Li, Junjie Wen, Yan Peng, Yaxin Peng, Feifei Feng, and Yichen Zhu. Pointvla: Injecting the 3d 

37214 

world into vision-language-action models. _arXiv preprint arXiv:2503.07511_ , 2025. 2 

- [24] Hengtao Li, Pengxiang Ding, Runze Suo, Yihao Wang, Zirui Ge, Dongyuan Zang, Kexian Yu, Mingyang Sun, Hongyin Zhang, Donglin Wang, et al. Vla-rft: Vision-language-action reinforcement fine-tuning with verified rewards in world simulators. _arXiv preprint arXiv:2510.00406_ , 2025. 3 

- [25] Haozhan Li, Yuxin Zuo, Jiale Yu, Yuhao Zhang, Zhaohui Yang, Kaiyan Zhang, Xuekai Zhu, Yuchen Zhang, Tianxing Chen, Ganqu Cui, et al. Simplevla-rl: Scaling vla training via reinforcement learning. _arXiv preprint arXiv:2509.09674_ , 2025. 3 

- [26] Mingrui Li, Zhetao Guo, Tianchen Deng, Yiming Zhou, Yuxiang Ren, and Hongyu Wang. Ddn-slam: Real time dense dynamic neural implicit slam. _IEEE Robotics and Automation Letters_ , 2025. 2 

- [27] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 5 

- [28] Jijia Liu, Feng Gao, Bingwen Wei, Xinlei Chen, Qingmin Liao, Yi Wu, Chao Yu, and Yu Wang. What can rl bring to vla generalization? an empirical study. _arXiv preprint arXiv:2505.19789_ , 2025. 2, 3 

- [29] Guanxing Lu, Wenkai Guo, Chubin Zhang, Yuheng Zhou, Haonan Jiang, Zifeng Gao, Yansong Tang, and Ziwei Wang. Vla-rl: Towards masterful and general robotic manipulation with scalable reinforcement learning. _arXiv preprint arXiv:2505.18719_ , 2025. 3 

- [30] Xiaohuan Pei, Yuxing Chen, Siyu Xu, Yunke Wang, Yuheng Shi, and Chang Xu. Action-aware dynamic pruning for efficient vision-language-action manipulation. _arXiv preprint arXiv:2509.22093_ , 2025. 2 

- [31] Xiaohuan Pei, Tao Huang, YanXiang Ma, and Chang Xu. Rethinking causal mask attention for vision-language inference. _arXiv preprint arXiv:2505.18605_ , 2025. 2 

- [32] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 5, 7, 13 

- [33] Tianhe Ren, Shilong Liu, Ailing Zeng, Jing Lin, Kunchang Li, He Cao, Jiayu Chen, Xinyu Huang, Yukang Chen, Feng Yan, Zhaoyang Zeng, Hao Zhang, Feng Li, Jie Yang, Hongyang Li, Qing Jiang, and Lei Zhang. Grounded sam: Assembling open-world models for diverse visual tasks, 2024. 3, 11 

- [34] Radu Bogdan Rusu, Gary Bradski, Romain Thibaux, and John Hsu. Fast 3d recognition and pose using the viewpoint feature histogram. In _2010 IEEE/RSJ international conference on intelligent robots and systems_ , pages 2155–2162. IEEE, 2010. 2 

- [35] Anthony Simeonov, Yilun Du, Andrea Tagliasacchi, Joshua B Tenenbaum, Alberto Rodriguez, Pulkit Agrawal, and Vincent Sitzmann. Neural descriptor fields: Se (3)equivariant object representations for manipulation. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 6394–6400. IEEE, 2022. 2 

- [36] Lin Sun, Bin Xie, Yingfei Liu, Hao Shi, Tiancai Wang, and Jiale Cao. Geovla: Empowering 3d representations in visionlanguage-action models. _arXiv preprint arXiv:2508.09071_ , 2025. 2 

- [37] Weiliang Tang, Jia-Hui Pan, Yun-Hui Liu, Masayoshi Tomizuka, Li Erran Li, Chi-Wing Fu, and Mingyu Ding. Geomanip: Geometric constraints as general interfaces for robot manipulation. _arXiv preprint arXiv:2501.09783_ , 2025. 3 

- [38] Marc Toussaint. Logic-geometric programming: An optimization-based approach to combined task and motion planning. In _IJCAI_ , pages 1930–1936, 2015. 2 

- [39] Yunke Wang, Chang Xu, Bo Du, and Honglak Lee. Learning to weight imperfect demonstrations. In _International Conference on Machine Learning_ , pages 10961–10970. PMLR, 2021. 2 

- [40] Rui Xu, Yunke Wang, Yong Luo, and Bo Du. Rethinking visual token reduction in lvlms under cross-modal misalignment. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , pages 27323–27331, 2026. 2 

- [41] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards efficient visionlanguage-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ , 2025. 2 

- [42] Yuhang Yang, Wei Zhai, Hongchen Luo, Yang Cao, Jiebo Luo, and Zheng-Jun Zha. Grounding 3d object affordance from 2d interactions in images. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10905–10915, 2023. 2 

- [43] Angen Ye, Zeyu Zhang, Boyuan Wang, Xiaofeng Wang, Dapeng Zhang, and Zheng Zhu. Vla-r1: Enhancing reasoning in vision-language-action models. _arXiv preprint arXiv:2510.01623_ , 2025. 3 

- [44] Yu Yue, Yufeng Yuan, Qiying Yu, Xiaochen Zuo, Ruofei Zhu, Wenyuan Xu, Jiaze Chen, Chengyi Wang, TianTian Fan, Zhengyin Du, et al. Vapo: Efficient and reliable reinforcement learning for advanced reasoning tasks. _arXiv preprint arXiv:2504.05118_ , 2025. 2 

- [45] Hongzhi Zang, Mingjie Wei, Si Xu, Yongji Wu, Zhen Guo, Yuanqing Wang, Hao Lin, Liangzhi Shi, Yuqing Xie, Zhexuan Xu, et al. Rlinf-vla: A unified and efficient framework for vla+ rl training. _arXiv preprint arXiv:2510.06710_ , 2025. 

   - 3 

- [46] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 2 

- [47] Xueyang Zhou, Yangming Xu, Guiyao Tie, Yongchao Chen, Guowen Zhang, Duanfeng Chu, Pan Zhou, and Lichao Sun. Libero-pro: Towards robust and fair evaluation of vision-language-action models beyond memorization. _arXiv preprint arXiv:2510.03827_ , 2025. 2, 5, 7 

37215 

