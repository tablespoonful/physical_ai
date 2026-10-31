---
title: "Collision-Free Humanoid Traversal in Cluttered Indoor Scenes"
date: "2026-01-22"
authors: "Han Xue; Sikai Liang; Zhikai Zhang; Zicheng Zeng; Yun Liu; Yunrui Lian"
url: https://arxiv.org/abs/2601.16035
pdf: https://arxiv.org/pdf/2601.16035
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.16035)** / [論文ページ](https://arxiv.org/abs/2601.16035)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Collision-Free Humanoid Traversal in Cluttered Indoor Scenes** 

Han Xue<sup>1</sup><sup>_,_3∗</sup> , Sikai Liang<sup>2</sup><sup>_,_3∗</sup> , Zhikai Zhang<sup>1</sup><sup>_,_3∗</sup> , Zicheng Zeng<sup>3</sup><sup>_,_5</sup> , Yun Liu<sup>1</sup><sup>_,_3</sup> , Yunrui Lian<sup>1</sup><sup>_,_3</sup> , Jilong Wang<sup>3</sup><sup>_,_6</sup> , Qingtao Liu<sup>3</sup><sup>_,_7</sup> , Xuesong Shi<sup>3</sup> , and Li Yi<sup>†</sup><sup>_,_1</sup><sup>_,_4</sup> 


Fig. 1: Using a single generalist policy, our humanoid robot achieves collision-free traversal in cluttered indoor environments, including (a) detouring through narrow passages, (b) crouching under low-hanging obstacles, (c) squeezing through tight indoor spaces, and (d) hurdling over objects scattered on the floor. 

**_Abstract_ — We study the problem of collision-free humanoid traversal in cluttered indoor scenes, such as hurdling over objects scattered on the floor, crouching under low-hanging obstacles, or squeezing through narrow passages. To achieve this goal, the humanoid needs to map its perception of surrounding obstacles with diverse spatial layouts and geometries to the corresponding traversal skills. However, the lack of an effective representation that captures humanoid–obstacle relationships during collision avoidance makes directly learning such mappings difficult. We therefore propose Humanoid Potential Field (HumanoidPF), which encodes these relationships as collision-free motion directions, significantly facilitating RLbased traversal skill learning. We also find that HumanoidPF exhibits a surprisingly negligible sim-to-real gap as a perceptual representation. To further enable generalizable traversal skills through diverse and challenging cluttered indoor scenes, we further propose a hybrid scene generation method, incorporating crops of realistic 3D indoor scenes and procedurally synthesized obstacles. We successfully transfer our policy to the real world and develop a teleoperation system where users could command** 

*Equal Contributions, †Corresponding Author 

> 1Tsinghua University, 2Tongji University, 3Galbot, 4Shanghai Qi Zhi Institute, 5South China University of Technology, 6Peking University, 

> 7Zhejiang University 

**the humanoid to traverse in cluttered indoor scenes with just a single click. Extensive experiments are conducted in both simulation and the real world to validate the effectiveness of our method. Demos and code can be found in our website: https://axian12138.github.io/CAT/.** 

## I. INTRODUCTION 

Consider a domestic humanoid robot needs to frequently traverse between the bedroom, living room, and kitchen to perform household chores. A key challenge for the robot is to avoid collisions with the surrounding environment during movement, preventing potential damage to the robot itself or the environment. In cluttered indoor scenes, the humanoid may need to hurdle over objects scattered on the floor, crouch under low-hanging obstacles, or squeeze through narrow passages. This requires the robot to perceive the environment and map obstacles with diverse spatial layouts and geometries to the corresponding traversal skills. 

While legged locomotion in complex environments has seen remarkable advances for quadrupeds [1]–[17] and humanoids [18]–[30], existing works are often limited in their 

ability to handle traversal in _cluttered indoor scenes_ (fullspatial obstacle layouts and intricate, realistic geometries), as shown in Table I. These limitations collectively point to the lack of an effective representation for humanoid–obstacle relationships during collision avoidance: (i) existing works [9]– [17], [22], [29] typically obtain penalty signals only when collisions occur, yielding sparse and delayed supervision. This forces reinforcement learning (RL) to depend on inefficient trial-and-error exploration, thus calling for a representation that can provide anticipatory and dense guidance; (ii) conventional representations expose the policy to raw, high-dimensional environmental measurement independently of humanoid–obstacle spatial relationships, forcing the policy to infer traversal decisions through implicit kinematic reasoning. 

To bridge these gaps, we introduce Humanoid Potential Field ( **HumanoidPF** ), an informative representation that encodes humanoid–obstacle relationships for collision avoidance. Inspired by classical Artificial Potential Fields (APF) [31], HumanoidPF models how the humanoid is influenced by and should react to its surrounding environment as a continuous and differentiable gradient field, inducing “virtual forces” that point toward collision-free motion directions. 

We seamlessly integrate HumanoidPF into traversal skill learning in two complementary ways. First, HumanoidPF serves as the policy observation by being queried at multiple key body parts, providing directional cues that indicate how each part should move to avoid obstacles and advance toward the goal. This allows the policy to reason directly over traversal decisions, instead of inferring collision-avoidance behavior from raw, high-dimensional visual inputs. Second, HumanoidPF streamlines collision-aware reward design. The field induces a distribution over preferred motion directions, and the policy is encouraged to align its motion with this distribution. This provides anticipatory and sufficient supervision for RL models, while exhibiting strong cross-scene generalization without manual reward tuning. Moreover, we observe that HumanoidPF yields a surprisingly negligible sim-to-real gap as a perceptual representation. Its continuous field formulation naturally functions as a low-pass perceptual filter, smoothing out isolated perception artifacts and promoting robust sim-to-real transfer. 

To learn traversal skills with HumanoidPF across diverse and challenging obstacle configurations, we propose a hybrid scene generation strategy that systematically expands the space of training scenarios. By augmenting crops of realistic 3D indoor datasets with procedurally synthesized highly constrained obstacles, we expose the robot to a curriculum of challenging clutter configurations that are rarely present in existing datasets, enabling it to acquire rich collisionavoidance experience and substantially improving robustness in near-collision and emergency scenarios. 

We further instantiate our approach into a practical teleoperation system, termed Click-and-Traverse (CAT), where the user can simply click a goal to command the humanoid to safely traverse cluttered indoor environments. Extensive experiments in both simulation and realistic real-world indoor 

|Method|Spatial layouts<br>Intricate|geometries|
|---|---|---|
|PIM [23]|_𝑆_={_𝑔_}|✗|
|HumanoidParkour [22]|_𝑆_={_𝑔_}|✗|
|BeamDojo [26]|_𝑆_={_𝑔_}|✗|
|Vb-com [24]|_𝑆_⊂{_𝑔,𝑙_}_,_ |_𝑆_|=1|✗|
|Gallant [29]|_𝑆_⊂{_𝑔,𝑙, 𝑜_}_,_ |_𝑆_|=1|✗|
|**Ours**|_𝑆_={_𝑔,𝑙, 𝑜_}|✓|


TABLE I: **Overall comparison with existing works.** _𝑆_ : Spatial layouts. _𝑔,𝑙,𝑜_ : Ground, lateral and overhead obstacles. 

scenes validate the practical applicability of HumanoidPF and its strong generalization across diverse environments. Our contributions are fourfold: 

- To the best of our knowledge, we are the first to systematically study collision-free humanoid traversal in _cluttered indoor scenes_ , advancing toward real-world domestic humanoid robot application. 

- We propose **HumanoidPF** , an informative representation that explicitly encodes humanoid–obstacle relationships for collision avoidance, thus significantly facilitating RL-based traversal skill learning. 

- We propose a hybrid scene generation strategy that exposes the policy to realistic, diverse and challenging cluttered scenarios, significantly improving robustness and generalization in complex indoor environments. 

- We successfully transfer our policy to the real world as a convenient and useful teleoperation system to command the humanoid to traverse in cluttered indoor scenes. 

## II. RELATED WORKS 

## _A. Legged locomotion in complex environments_ 

Legged robots are expected to perform stable locomotion in complex environments, including challenging terrains and obstacles. Quadruped robots have demonstrated robust parkour capabilities on highly challenging terrains [1], [2], [4], [6], [8], [16], [17] and confined or cluttered spaces [9]–[14]. Humanoids have also demonstrated the ability to navigate in height-constrained environments [18] and advanced locomotion skills against risky terrains or obstacles, such as stepping stairs, balance beams, and stepping stones [19], [20], [22]–[27], [29], [30]. 

However, existing works on humanoids often limited to obstacles with partial spatial layouts (e.g. terrains [19], [20], [22]–[27], [30], or over-hanging obstacles [18]) and simple geometries (e.g. rectangular blocks [18]–[20], [22], [25]–[27], or regular polyhedra [24], [29]). Notably, while Gallant [29] addresses ground, lateral, and overhead obstacle layouts in isolation, it does not consider scenarios where these constraints coexist. In contrast, our method constructs HumanoidPF to operate in _cluttered indoor scenes_ where full-spatial constraints are jointly present with highly intricate geometries. The comparison of existing works and our work is shown in Table I. 

## _B. Artificial potential field for obstacle avoidance_ 

Originally introduced in the late 1980s, the Artificial Potential Field (APF) [31] method generates a virtual force 


Fig. 2: **Overall pipeline.** We learn a visuomotor policy that maps diverse obstacle geometries and spatial layouts to corresponding whole-body traversal skills. **Left: HumanoidPF for whole-body traversal learning.** _(Top)_ Construction of HumanoidPF, a reformulation of APF tailored for humanoid whole-body traversal; _(Bottom)_ its use as informative perceptual representation and collision-avoidance rewards. **Right: Scalable training and deployment pipeline.** _(Top)_ Hybrid scene generation for constructing diverse and challenging training environments; _(Middle)_ parallel training of multiple specialist policies followed by distillation into a single generalist policy; _(Bottom)_ sim-to-real deployment via “Click-and-Traverse”, an intuitive loco-navigation teleoperation in cluttered indoor scenes. Sections III-A, III-B and III-C provide detailed descriptions of the HumanoidPF for traversal learning, the scalable training, and deployment pipeline, respectively. 

field to guide the motion of manipulators or mobile robots for obstacle avoidance. Inspired by physical analogies, the goal position is modeled as an attractive pole, while obstacles act as repulsive surfaces. Traditionally, APF has been widely used in 2D path planning for mobile robots [32]–[34] and robotic manipulators [35]–[37]. 

However, only a few studies have combined model-based quadruped control with APF in limited forms by abstracting the center of mass [38], [39] or foot joint [40], [41] as a single rigid body, which is insufficient to handle the complex planning and control challenges of humanoid learning. In contrast, we propose **HumanoidPF** , a principled reformulation of APF specifically tailored for informative perception and reward streamlining of humanoid skill learning. 

## III. METHOD 

We study the problem of collision-free humanoid traversal in cluttered indoor scenes. Given a target position **g** ∈ R<sup>3</sup> , and a set of indoor obstacles O = { _𝑂𝑖_ } _𝑖_<sup>_𝑁_</sup> =1<sup>,thehumanoid</sup> needs to move to **g** without any collision with O. To solve this problem, the humanoid needs to map its perception of surrounding obstacles to the corresponding traversal skills. Our method can be split into two parts. We first introduce how our **HumanoidPF** encodes humanoid–obstacle relationships to facilitate humanoid traversal learning in Section IIIA. We further introduce how to generalize our policy to 

diverse and challenging indoor scenes with our proposed hybrid scene generation method in Section III-B. For realworld deployment, we further instantiate our approach as a teleoperated loco-navigation system, which is presented in Section III-C. The overall pipeline is shown in Figure 2. 

## _A. HumanoidPF for whole-body traversal learning_ 

We substantially extend classical APF to support learningbased whole-body humanoid traversal. In APF, the target location **g** is modeled as an attractive pole and obstacles O as repulsive surfaces, forming a gradient field that indicates collision-free motion toward the goal. However, prior works directly apply APF in single-rigid-body model-based control, which is inadequate for the high-dimensional and tightly coupled planning and control demands of humanoid skill learning. We therefore propose HumanoidPF, a principled reformulation of APF tailored for humanoid, which encodes humanoid–obstacle relationships for informative perception and reward streamlining. 

## _1) HumanoidPF construction_ 

We begin by constructing the attractive field _𝑈_ att: 


where the geodesic distance ∥ **x** − **g** ∥geo represents the shortest 3D path from position **x** to the goal **g** without intersecting obstacles, and _𝜂_ is a scaling factor. The geodesic distance 


Fig. 3: (a) Construction of the APF and (b) motion prior distribution induced by the HumanoidPF. inherently accounts for obstacle geometry, providing safer guidance than a simple Euclidean distance. 

Next, the repulsive field _𝑈_ rep prevents collisions and is defined as: 


where _𝑑_ ( **x** ) is the signed distance, _𝜉_ is a scaling factor, and _𝑑_ 0 defines the influence range of obstacles. The final guidance field is the negative gradient of a combined potential, 


which is then queried at the locations of different body parts, yielding field vectors **F** ( **x** _𝑘_ ) for each body part **p** _𝑘_ . A 2D visualization of our APF is illustrated in Figure. 3 (a). 

While APF method typically models robots as a single rigid body, its direct application to multi-jointed humanoid robots could lead to conflicts between body parts. For instance, when the robot faces an obstacle directly ahead, it must decide whether to move left or right. The potential fields on the left and right sides of the body direct it toward opposite paths. In a symmetrical configuration, these vectors cancel each other out, leading to a multi-modal dilemma where the robot becomes trapped in a local minimum or exhibits oscillatory behavior. To address this challenge, we propose a priority-weighting scheme that prioritizes the influence of certain body parts over others according to their contribution to the task. 

**Priority-weighting.** Instead of treating all body parts equally, our priority-weighting scheme adjusts the influence of each body part based on its role in the overall motion. 

To establish coherent global guidance, we assign a higher priority to the root body part (e.g., pelvis) since it plays a central role in maintaining stability and direction: 


Furthermore, some body parts are more critical in avoiding obstacles, particularly those closer to potential collisions. To account for this, we define a dynamic collision-urgency weight based on the signed distance _𝑑_ ( **x** _𝑘_ ) and the Cartesian velocity **v** _𝑘_ of body part **p** _𝑘_ , with a scaling factor _𝜆_ : 


The resulting HumanoidPF is defined as **F** _𝐻_ = _𝑤_ 0 _𝑤_ 1 ∥ **<u>FF</u>** ∥<sup>.</sup> This scheme attenuates conflicting influences and promotes coordinated whole-body control. In particular, minute asymmetries in the spatial configuration are selectively amplified, thus seamlessly resolving the multi-modal dilemma. 

_2) Traversal skill learning with HumanoidPF_ 

**HumanoidPF for policy observation.** To better inform RL policies about humanoid-obstacle relationships, we leverage HumanoidPF to construct a compact, task-relevant visual observation. It is sampled at _𝐾_ = 13 body parts, 


where each **F** _𝐻_ ( **x** _𝑘_ ) encodes the local directional guidance induced by obstacles and the target at body part _𝑘_ , indicating collision-free motion. Sampling these fields at key body parts specifies how the humanoid should steer its body through the environment, allowing the policy to reason about traversal decisions rather than implicit inference from raw visual data. We empirically validate this in Section IV-A. 

HumanoidPF for observation further mitigates the perceptual sim-to-real gap by representing the environment as a continuous, spatially aggregated field, which functions like a low-pass perceptual filter. Unlike raw sensor representations that retain fine-grained geometric details and are sensitive to small local perturbations, the field formulation suppresses isolated noise while preserving the dominant spatial gradients relevant to the traversal task. This ensures that minor geometric variations do not significantly affect control during realworld deployment, as is empirically validated in Section IV-C 

**HumanoidPF for policy reward.** To streamline reward engineering, we employ HumanoidPF to induce anticipatory and dense guidance that generalizes across diverse environments. At each time step, HumanoidPF encodes a distribution of preferred motion directions, and the policy is optimized to produce actions that align with this distribution, thus fostering safe and dexterous collision-avoidance behaviors. 

The von Mises–Fisher (vMF) distribution is used to model directional preferences _𝝁_ ( **x** ) ∈ R<sup>3</sup> on the unit sphere and allows the strength of this preference to be controlled by a single concentration parameter _𝜅_ ( **x** ) ∈ R: 


where **v** ˆ is the motion direction of a humanoid body part, _𝐶𝑑_ ( _𝜅_ ) is the normalization function. _𝝁_ ( **x** ) and _𝜅_ ( **x** ) is directly derived from HumanoidPF: 


where _𝜅_ max is a scaling factor. The body part with higher priority receives a field vector **F** _𝐻_ ( **x** ) with larger magnitude; accordingly, _𝜅_ ( **x** ) increases to enforce stricter alignment with _𝝁_ ( **x** ) , and vice versa for lower-priority parts. This priorityaware concentration design promotes coordinated wholebody motion while improving collision-avoidance behavior, as illustrated in Figure 3 (b). 

During policy training, let the motion direction of the _𝑘_ -th body part be **v** ˆ _𝑘_ = **v** _𝑘_ /∥ **v** _𝑘_ ∥, the associated prior direction be 


Fig. 4: **Collision-free humanoid traversal in both simulation and the real world.** (a) Humanoid traversal behaviors on eight representative test scene types; (b) traversal behaviors in procedurally generated cluttered environments; (c) realworld “hurdle-crouch” scenario, validating sim-to-real transfer in a cluttered indoor setting; (d) robustness under dynamic disturbances, where simple object movements (blue arrows) are introduced during traversal. 

_𝝁𝑘_ = _𝝁_ ( **x** _𝑘_ ) and concentration parameter be _𝜅𝑘_ = _𝜅_ ( **x** _𝑘_ ). Assuming independence among joints, the whole-body motion prior and log-likelihood reward are expressed as: 


This reward formulation exhibits strong cross-scene generalization without requiring manual tuning, thereby enabling an automated training pipeline that scales effectively across diverse environments. 

## _B. Scalable training in diverse and challenging scenes_ 

For general practical use, the humanoid needs to handle diverse scenes within a single unified policy. It needs the policy trained with a sufficiently large and challenging indoor scene dataset to enable generalization in real-world cluttered scenes. Therefore, we propose a hybrid scene generation method in Section III-B.1. It incorporates crops of realistic 3D indoor scenes for structural realism, and procedurally synthesized obstacles to enrich highly challenging clutter configurations. In addition, even with HumanoidPF, directly learning a single policy across all scenes remains challenging due to the low sample efficiency of RL. We therefore adopt a specialist-to-generalist training strategy inspired by [42], [43], described in Section III-B.2. 

## _1) Hybrid scene generation_ 

We observe that highly challenging obstacle layouts constitute merely a long-tail subset in most existing datasets [44]–[46], since typical indoor scenes feature orderly object arrangements and clearly delineated walkable regions. Simply scaling up the dataset does not alleviate this problem. Therefore, we propose a novel hybrid scene generation scheme that enriches realistic 3D indoor datasets with procedurally synthesized ”extreme” obstacles, where full-spatial constraints are jointly present. 

**Crops of realistic 3D indoor scenes.** For generalization to intricate and realistic indoor environments, we adopt the 3DFRONT [44] dataset, containing structurally realistic scenes with large-scale high-quality furniture objects. We selectively crop and filter scene blocks for policy training. 

Specifically, we first project all furniture onto the ground and erode the resulting planar walkable regions with a radius of 0.1 m to account for clearance. Within the remaining walkable regions, we randomly sample a start location and crop a 5 m × 5 m block centered at this position. During training, the goal location will be randomly sampled on a circle with a radius of 2 m around the start. 

We initially train specialist policies on all such cropped scenes and subsequently identify scenes with low traversal success rates. Scenes that are empirically found to be nontraversable are manually filtered out. 

**Procedurally generated obstacles.** To supplement crops of 3D-FRONT with more challenging and cluttered environments, we procedurally generate obstacles that impose full-spatial (simultaneous ground, lateral, and overhead) constraints, deliberately targeting highly restrictive scenarios. Specifically, we place boxes with varying positions, dimensions, and orientations that may extend upward from the floor, descend from the ceiling, and be placed in close proximity to form narrow traversal passages. 

To break structural regularity and enhance geometric realism, we apply random SO(3) rotations and 2D Perlin noise to each box. The resulting artifacts, such as spiky surfaces or non-manifold regions, are mitigated via 3D morphological closing and opening at the voxel level before mesh conversion. Visualizations of the robot traversing generated obstacles are shown in Figure 2 and Figure 4 (b). 

To support curriculum learning during policy training, we use a layout-agnostic difficulty factor to control obstacle complexity, such as the number and size of boxes. As the difficulty increases, the policy progressively acquires robust traversal skills under increasingly challenging configurations. 

||**Hurdle**|**-Crouch**|**Side-Hur**|**dle-Crouch**|**Side-**|**Hurdle**|**Side-**|**Crouch**|
|---|---|---|---|---|---|---|---|---|
||_SR(%)_ ↑|_DE(m)_ ↓|_SR(%)_ ↑|_DE(m)_ ↓|_SR(%)_ ↑|_DE(m)_ ↓|_SR(%)_ ↑|_DE(m)_ ↓|
|ASTraversal|28.1 ±10.4|1.11 ±0.78|0.5 ±0.5|1.06 ±0.39|37.1 ±3.1|0.54 ±0.32|56.0 ±9.9|0.48 ±0.05|
|Humanoid Parkour|33.3 ±6.1|1.16 ±0.63|0.4 ±0.3|1.49 ±0.04|45.1 ±4.5|0.62 ±0.39|64.4 ±19.3|0.56 ±0.16|
|Ours w/o _𝑂𝐵𝑆𝐹𝑖𝑒𝑙𝑑_|77.8 ±5.4|0.33 ±0.23|53.7 ±9.9|0.59 ±0.08|60.4 ±9.6|0.53 ±0.68|90.1 ±5.3|0.19 ±0.35|
|Ours w/o _𝑅𝐹𝑖𝑒𝑙𝑑_|21.9 ±15.8|1.27 ±0.71|0.0 ±0.0|1.57 ±0.003|71.4 ±9.9|0.5 ±0.34|80.3 ±15.4|0.23 ±0.06|
|Ours|**93.9** ±**2.7**|**0.08** ±**0.16**|**86.6** ±**5.2**|**0.2** ±**0.32**|**95.4** ±**3.9**|**0.06** ±**0.34**|**96.9** ±**2.1**|**0.05** ±**0.09**|
||**Hurdl**|**e-Pass**|**Crou**|**ch-Pass**|**Side**|**-Pass**|**Multi-**|**Hurdle**|
||_SR(%)_ ↑|_DE(m)_ ↓|_SR(%)_ ↑|_DE(m)_ ↓|_SR(%)_ ↑|_DE(m)_ ↓|_SR(%)_ ↑|_DE(m)_ ↓|
|ASTraversal|75.9 ±6.8|0.66 ±0.3|41.3 ±5.3|0.9 ±1.04|55.2 ±8.5|0.78 ±0.87|82.1 ±8.7|0.26 ±0.43|
|Humanoid Parkour|84.3 ±8.0|0.32 ±0.18|48.1 ±3.3|1.34 ±0.18|41.3 ±2.5|0.91 ±0.34|88.7 ±2.6|0.23 ±0.35|
|Ours w/o _𝑂𝐵𝑆𝐹𝑖𝑒𝑙𝑑_|92.3 ±4.9|0.1 ±0.15|96.8 ±5.0|0.07 ±0.3|95.2 ±4.4|0.07 ±0.22|90.5 ±3.5|0.09 ±0.11|
|Ours w/o _𝑅𝐹𝑖𝑒𝑙𝑑_|90.7 ±7.5|0.12 ±0.37|95.9 ±5.0|0.08 ±0.24|28.0 ±18.3|1.07 ±0.56|88.3 ±14.1|0.23 ±0.5|
|Ours|**96.9** ±**5.5**|**0.06** ±**0.15**|**97.5** ±**4.3**|**0.05** ±**0.09**|**97.3** ±**3.2**|**0.04** ±**0.15**|**95.0** ±**4.9**|**0.06** ±**0.1**|


TABLE II: **Validation of HumanoidPF for skill learning.** To better characterize the performance of our method under diverse obstacle layouts, we design 8 distinct scene types for evaluation and ablation studies. 

## _2) Specialist-to-generalist training_ 

We construct an automated and parallel specialist-togeneralist training pipeline. We first conduct large-scale training of specialist policies across diverse scenes via PPO [47]. The reward derived from HumanoidPF is scenegeneral, enabling scalable training on 139 cropped 3DFRONT scenes and 216 procedurally generated scenes. Each specialist is trained with 32,768 parallel environments and 5,000,000 episodes, with start and goal locations randomly sampled for each episode. 

Subsequently, a generalist policy is distilled using DAgger [42] from multiple specialists as teacher policies. Dedicated specialists provide expert actions conditioned on current obstacle, enabling the generalist to acquire strong generalization capability across varying scenarios. 

To learn robust and stable traversal skills, both specialist and generalist policies are trained with sensor noise and force perturbations to simulate realistic collision-avoidance conditions. In addition, a curriculum with progressively increasing scene difficulty is employed to gradually enhance traversal performance and explore the limits of the policy’s obstacleavoidance capability. 

## _C. Real-world deployment: Click-and-Traverse_ 

For real-world deployment, we instantiate our method as a teleoperated loco-navigation system, termed Click-andTraverse (CAT). The system integrates a LiDAR–inertial SLAM pipeline based on Fast-LIO2 [48] and OctoMap [49]. It maintains an up-to-date environment mapping and field construction, both operating at a frequency of 10 Hz. The policy queries the HumanoidPF at different body parts via self-localization and forward-kinematics. 

Users could specify a desired goal by simply clicking on a grid map, after which the humanoid autonomously navigates to the target while avoiding collisions. This interface removes the need for labor-intensive control modalities such as joysticks or motion capture, providing a lightweight and highly automated teleoperation solution. 

## IV. EXPERIMENT 

In this section, we provide extensive experimental results in both the MuJoCo [50] simulator and the real world on Unitree G1 humanoid robot. The experiments aim to address the following three questions: 

- **Q1** : Can **HumanoidPF** improve the performance of traversal in cluttered indoor scenes compared to existing methods? 

- **Q2** : Can our hybrid scene generation method help the policy generalize to unseen and challenging scenes? 

- **Q3** : Can the HumanoidPF for observation _𝑂𝐵𝑆𝐹𝑖𝑒𝑙𝑑_ help the sim-to-real transfer? 

## _A. Validation of HumanoidPF for skill learning_ 

To address **Q1** ( _Can HumanoidPF improve the performance of traversal in cluttered indoor scenes compared to existing methods?_ ), we compare the performance of our method against existing ones on traversing cluttered scenes. 

**Experiment Setting.** To systematically analyze performance under different obstacle layouts and geometric configurations, we design eight distinct types of cluttered scenes for evaluation. All scenes used in this experiment are manually generated, each type exhibiting distinct characteristics and collectively covering a broad range of challenging obstacle configurations, with 10 scenes per type. We train and evaluate all methods on these generated scenes to compare their ability to traverse cluttered environments. Representative visualizations of the robot traversing each scene type are shown in Figure 4 (a). 

**Experiment Metrics.** We use the following metrics to evaluate the performance on traversing cluttered scenes: 

- **Success Rate (SR, %)** records the percentage of successful traversal trials. A trial is considered successful if the robot reaches within 0.1 meters of the target location in 5 seconds without colliding with any obstacle. 

- **Distance Error (DE, m)** is the averaged closest horizontal distance between the humanoid root and the target location in a traversal. 

|**Group**|**Easy (SR%)**|**Hard (SR%)**|
|---|---|---|
|Base|62.0 ±23.4|1.2 ±2.9|
|Base + Syn-Partial-Easy|78.6 ±12.2|12.3 ±10.3|
|Base + Syn-Full-Easy|83.1 ±19.0|26.4 ±5.8|
|Base + Syn-Full-Hard|95.2 ±6.1|66.7 ±17.9|


TABLE III: **Validation of hybrid scene generation.** Mean success rate (%) on easy and hard subsets for the four experiment groups (mean ± std). 

**Baselines.** We choose the following methods and adapt them to fit our problem setting for a fair comparison: 

- **ASTraversal** [14]: ASTraversal was originally proposed for quadrupeds. We re-implement its core multi-layer elevation maps and obstacle-avoidance reward for our humanoid framework. 

- **Humanoid Parkour** [22]: The method enhances collision penalties to better guide locomotion, but is limited to terrain modeling below the feet. To adapt it to our full-space traversal setting, we additionally provide overhead obstacle perception for fair comparison. 

- **Ours w/o** _𝑂𝐵𝑆𝐹𝑖𝑒𝑙𝑑_ **:** We replace the HumanoidPF in observation with multi-layer elevation maps as used in ASTraversal [14]. We adopt this baseline to evaluate the effectiveness of HumanoidPF for observation. 

- **Ours w/o** _𝑅𝐹𝑖𝑒𝑙𝑑_ **:** We remove the HumanoidPF-guided reward. Instead, we use a basic collision-penalty reward commonly used in collision-avoidance tasks [22]. We adopt this baseline to validate HumanoidPF for reward. 

**Experiment Results.** Results are summarized in Table II. Our method consistently achieves the best performance across all types of test cases, demonstrating its strong traversal capability in cluttered scenes. In contrast, both Humanoid Parkour and ASTraversal only achieve competitive performance in relatively simple terrains. Nevertheless, our approach exhibits low variance over multiple trials, indicating high robustness and stability of the learned policy. 

## _B. Validation of hybrid scene generation_ 

To address **Q2** ( _Can our hybrid scene generation method help the policy generalize to unseen and challenging scenes?_ ), We evaluate and compare the zero-shot scene generalization ability of the traversal policies trained with different scene datasets. 

**Experiment Setting.** We collect 30 artist-designed indoor scenes that were not included in the training dataset. These scenes are categorized according to obstacle density into 15 easy and 15 hard cases. We test the policies trained with different datasets in these unseen scenes and compare their zero-shot transfer performance. 

**Experiment Metrics.** We use the **Success Rate (SR, %)** metric as mentioned in Section IV-A. 

**Baselines.** We choose the following methods as baselines: 

- **Base:** We use 3D-FRONT scenes only. 

- **Base + Syn-Partial-Easy: Base** combined with a subset of moderate-difficulty (≤ 0 _._ 6) synthesized scenes. 

- **Base + Syn-Full-Easy: Base** combined with the full set of moderate-difficulty (≤ 0 _._ 6) synthesized scenes. 

|**Real-world**<br>**Exteroception**|**Crouch-**<br>**Pass**|**Hurdle-**<br>**Pass**|**Side-**<br>**Pass**|**Crouch-**<br>**Hurdle**|
|---|---|---|---|---|
|Voxel Grids|1/5|3/5|2/5|2/5|
|Elevation Maps|3/5|3/5|1/5|2/5|
|HumanoidPF (Ours)|**4/5**|**5/5**|**5/5**|**4/5**|


TABLE IV: **Validation of HumanoidPF for real world transfer.** Success rate on four challenging real-world scenes. 

- **Base + Syn-Full-Hard: Base** combined with the full set of high-difficulty (0 _._ 4 ∼ 1 _._ 0) synthesized scenes. 

**Experiment Results** The results shown in Table III confirm that procedural obstacle generation is crucial to enhance generalization, as it systematically scales both the volume and the difficulty of training data. Despite significant performance improvement from the expansion of obstacle diversity, saturation in gains can be observed once common layout patterns are sufficiently learned. The key breakthrough emerges from training in scenes with novel complexities and tighter constraints, which induce the policy to develop the superior capabilities necessary for complex terrains. 

## _C. Validation of HumanoidPF for real world transfer_ 

To address **Q3** ( _Can the HumanoidPF for observation 𝑂𝐵𝑆𝐹𝑖𝑒𝑙𝑑 help the sim-to-real transfer?_ ), we compare the traversal capability of our method with other perceptual representations under real-world conditions. 

**Experiment Setting.** We construct a set of representative cluttered indoor traversal scenarios in the real world, covering crouching under low-hanging obstacles, hurdling over ground objects, and negotiating narrow-side passages. These scenarios are deliberately designed to stress perceptual reliability by evaluating whether the learned policy could remain collision-free traversal under real-world conditions. 

**Experiment Metrics.** We use the **Success Rate (SR)** metric as mentioned in Section IV-A. 

**Baselines.** We distill the same specialists to two different perceptual representation as baselines: 

- **Voxel Grids:** Distilling to voxel-based visuomotor policy. 

- **Multi-layer Elevation Maps:** Distilling to two-layerelevation visuomotor policy. 

**Experiment Results.** Results are summarized in Table IV. Our HumanoidPF consistently outperforms voxelbased approaches across diverse environments. For example, on hurdle terrains, the voxel-based method often exhibits instability because it is sensitive to fine-grained geometric details of obstacles and to noise in task-irrelevant regions. In contrast, HumanoidPF remains largely unaffected by such disturbances and shows behavior that aligns more closely with simulation, further confirming its robustness in sim-toreal transfer. Qualitative results of our method are shown in Figure 1 and Figure 4. 

## V. CONCLUSION 

In this work, we address collision-free humanoid traversal in cluttered indoor scenes. We introduce HumanoidPF, an informative representation to encode humanoid–obstacle 

relationships for RL-based traversal skill learning, advancing toward real-world domestic humanoid robot application. Despite these advances, several limitations remain. Our current framework does not yet exploit contact-rich interactions, such as leaning on obstacles or stepping onto support surfaces, and generalization to entirely unseen, highly unstructured, and extremely cluttered scenes remains an open challenge. 

## REFERENCES 

- [1] R. Grandia, F. Jenelten, S. Yang, F. Farshidian, and M. Hutter, “Perceptive locomotion through nonlinear model-predictive control,” _IEEE Transactions on Robotics_ , vol. 39, no. 5, pp. 3402–3421, 2023. 

- [2] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning quadrupedal locomotion over challenging terrain,” _Science robotics_ , vol. 5, no. 47, p. eabc5986, 2020. 

- [3] G. Gagn´e-Labelle, V. Atanassov, and I. Havoutis, “Acrobotics: A generalist approach to quadrupedal robots’ parkour,” in _Annual Conference Towards Autonomous Robotic Systems_ . Springer, 2025, pp. 124–137. 

- [4] C. Zhang, N. Rudin, D. Hoeller, and M. Hutter, “Learning agile locomotion on risky terrains,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 11 864– 11 871. 

- [5] Q. Liao, Z. Li, A. Thirugnanam, J. Zeng, and K. Sreenath, “Walking in narrow spaces: Safety-critical locomotion control for quadrupedal robots with duality-based optimization,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2023, pp. 2723–2730. 

- [6] J. Lee, M. Bjelonic, A. Reske, L. Wellhausen, T. Miki, and M. Hutter, “Learning robust autonomous navigation and locomotion for wheeledlegged robots,” _Science Robotics_ , vol. 9, no. 89, p. eadi9641, 2024. 

- [7] R. Yang, G. Yang, and X. Wang, “Neural volumetric memory for visual locomotion control,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2023, pp. 1430–1440. 

- [8] N. Rudin, D. Hoeller, M. Bjelonic, and M. Hutter, “Advanced skills by learning locomotion and local navigation end-to-end,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2022, pp. 2497–2503. 

- [9] Z. Wang, T. Ma, Y. Jia, X. Yang, J. Zhou, W. Ouyang, Q. Zhang, and J. Liang, “Omni-perception: Omnidirectional collision avoidance for legged locomotion in dynamic environments,” _arXiv preprint arXiv:2505.19214_ , 2025. 

- [10] D. Hoeller, N. Rudin, D. Sako, and M. Hutter, “Anymal parkour: Learning agile navigation for quadrupedal robots,” _Science Robotics_ , vol. 9, no. 88, p. eadi7566, 2024. 

- [11] T. Miki, J. Lee, L. Wellhausen, and M. Hutter, “Learning to walk in confined spaces using 3d representation,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 8649–8656. 

- [12] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao, “Robot parkour learning,” _arXiv preprint arXiv:2309.05665_ , 2023. 

- [13] N. Rudin, J. He, J. Aurand, and M. Hutter, “Parkour in the wild: Learning a general and extensible agile locomotion policy using multi-expert distillation and rl fine-tuning,” _arXiv preprint arXiv:2505.11164_ , 2025. 

- [14] Y. Chen, J. Ma, Z. Luo, Y. Han, Y. Dong, B. Xu, and P. Lu, “Learning autonomous and safe quadruped traversal of complex terrains using multi-layer elevation maps,” _IEEE Robotics and Automation Letters_ , 2025. 

- [15] T. He, C. Zhang, W. Xiao, G. He, C. Liu, and G. Shi, “Agile but safe: Learning collision-free high-speed legged locomotion,” _arXiv preprint arXiv:2401.17583_ , 2024. 

- [16] X. Cheng, K. Shi, A. Agarwal, and D. Pathak, “Extreme parkour with legged robots,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 11 443–11 450. 

- [17] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning robust perceptive locomotion for quadrupedal robots in the wild,” _Science robotics_ , vol. 7, no. 62, p. eabk2822, 2022. 

- [18] Z. Li, J. Zeng, S. Chen, and K. Sreenath, “Autonomous navigation of underactuated bipedal robots in height-constrained environments,” _The International Journal of Robotics Research_ , vol. 42, no. 8, pp. 565–585, 2023. 

- [19] J. He, C. Zhang, F. Jenelten, R. Grandia, M. B¨acher, and M. Hutter, “Attention-based map encoding for learning generalized legged locomotion,” _Science Robotics_ , vol. 10, no. 105, p. eadv3604, 2025. 

- [20] J. Sun, G. Han, P. Sun, W. Zhao, J. Cao, J. Wang, Y. Guo, and Q. Zhang, “Dpl: Depth-only perceptive humanoid locomotion via realistic depth synthesis and cross-attention terrain reconstruction,” _arXiv preprint arXiv:2510.07152_ , 2025. 

- [21] H. Duan, B. Pandit, M. S. Gadde, B. Van Marum, J. Dao, C. Kim, and A. Fern, “Learning vision-based bipedal locomotion for challenging terrain,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 56–62. 

- [22] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” _arXiv preprint arXiv:2406.10759_ , 2024. 

- [23] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9997–10 003. 

- [24] J. Ren, T. Huang, H. Wang, Z. Wang, Q. Ben, J. Long, Y. Yang, J. Pang, and P. Luo, “Vb-com: Learning vision-blind composite humanoid locomotion against deficient perception,” _arXiv preprint arXiv:2502.14814_ , 2025. 

- [25] T. Huang, R. Xu, Y. Wang, W. Gao, and S. Zhang, “Traversing narrow paths: A two-stage reinforcement learning framework for robust and safe humanoid walking,” _arXiv preprint arXiv:2508.20661_ , 2025. 

- [26] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv preprint arXiv:2502.10363_ , 2025. 

- [27] W. Sun, B. Cao, L. Chen, Y. Su, Y. Liu, Z. Xie, and H. Liu, “Learning perceptive humanoid locomotion over challenging terrain,” _arXiv preprint arXiv:2503.00692_ , 2025. 

- [28] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa, “Visual imitation enables contextual humanoid control,” _arXiv preprint arXiv:2505.03729_ , 2025. 

- [29] Q. Ben, B. Xu, K. Li, F. Jia, W. Zhang, J. Wang, J. Wang, D. Lin, and J. Pang, “Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains,” _arXiv preprint arXiv:2511.14625_ , 2025. 

- [30] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu, _et al._ , “Track any motions under any disturbances,” _arXiv preprint arXiv:2509.13833_ , 2025. 

- [31] O. Khatib, “Real-time obstacle avoidance for manipulators and mobile robots,” _The international journal of robotics research_ , vol. 5, no. 1, pp. 90–98, 1986. 

- [32] Z. Wu, J. Dai, B. Jiang, and H. R. Karimi, “Robot path planning based on artificial potential field with deterministic annealing,” _ISA transactions_ , vol. 138, pp. 74–87, 2023. 

- [33] Y. K. Hwang, N. Ahuja, _et al._ , “A potential field approach to path planning.” _IEEE transactions on robotics and automation_ , vol. 8, no. 1, pp. 23–32, 1992. 

- [34] S. S. Ge and Y. J. Cui, “Dynamic motion planning for mobile robots using potential field method,” _Autonomous robots_ , vol. 13, no. 3, pp. 207–222, 2002. 

- [35] Y. Gong, R. Laha, and L. Figueredo, “Geopf: Infusing geometry into potential fields for reactive planning in non-trivial environments,” _arXiv preprint arXiv:2505.19688_ , 2025. 

- [36] M. Ginesi, D. Meli, A. Roberti, N. Sansonetto, and P. Fiorini, “Dynamic movement primitives: Volumetric obstacle avoidance using dynamic potential functions,” _Journal of Intelligent & Robotic Systems_ , vol. 101, no. 4, p. 79, 2021. 

- [37] Y. Chen, L. Chen, J. Ding, and Y. Liu, “Research on real-time obstacle avoidance motion planning of industrial robotic arm based on artificial potential field method in joint space,” _Applied Sciences_ , vol. 13, no. 12, p. 6973, 2023. 

- [38] H. Igarashi, T. Machida, F. Harashima, and M. Kakikura, “Free gait for quadruped robots with posture control,” in _9th IEEE International Workshop on Advanced Motion Control, 2006._ IEEE, 2006, pp. 433– 438. 

- [39] H. Igarashi and M. Kakikura, “Path and posture planning for walking robots by artificial potential field method,” in _IEEE International_ 

   - _Conference on Robotics and Automation, 2004. Proceedings. ICRA’04. 2004_ , vol. 3. IEEE, 2004, pp. 2165–2170. 

- [40] F. Zhuo, W. Jia, S. Ma, J. Yuan, and Y. Sun, “A variable artificial potential field method for gait generation of quadruped robot,” in _2021 IEEE International Conference on Mechatronics and Automation (ICMA)_ . IEEE, 2021, pp. 1176–1181. 

- [41] Y. A. Voeurn and M. I. Raza, “Motion planning of quadruped robot using potential field,” in _2021 International Conference” Nonlinearity, Information and Robotics”(NIR)_ . IEEE, 2021, pp. 1–6. 

- [42] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 

- [43] Z. Zhang, C. Chen, H. Xue, J. Wang, S. Liang, Y. Liu, Z. Zhang, H. Wang, and L. Yi, “Unleashing humanoid reaching potential via real-world-ready skill space,” _arXiv preprint arXiv:2505.10918_ , 2025. 

- [44] H. Fu, B. Cai, L. Gao, L.-X. Zhang, J. Wang, C. Li, Q. Zeng, C. Sun, R. Jia, B. Zhao, _et al._ , “3d-front: 3d furnished rooms with layouts and semantics,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2021, pp. 10 933–10 942. 

- [45] M. Deitke, E. VanderBilt, A. Herrasti, L. Weihs, K. Ehsani, J. Salvador, W. Han, E. Kolve, A. Kembhavi, and R. Mottaghi, “Procthor: Largescale embodied ai using procedural generation,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 5982–5994, 2022. 

- [46] S. K. Ramakrishnan, A. Gokaslan, E. Wijmans, O. Maksymets, A. Clegg, J. Turner, E. Undersander, W. Galuba, A. Westbury, A. X. Chang, _et al._ , “Habitat-matterport 3d dataset (hm3d): 1000 large-scale 3d environments for embodied ai,” _arXiv preprint arXiv:2109.08238_ , 2021. 

- [47] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [48] W. Xu, Y. Cai, D. He, J. Lin, and F. Zhang, “Fast-lio2: Fast direct lidar-inertial odometry,” 2021. [Online]. Available: https://arxiv.org/abs/2107.06829 

- [49] A. Hornung, K. M. Wurm, M. Bennewitz, C. Stachniss, and W. Burgard, “OctoMap: An efficient probabilistic 3D mapping framework based on octrees,” _Autonomous Robots_ , 2013, software available at https://octomap.github.io. [Online]. Available: https: //octomap.github.io 

- [50] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2012, pp. 5026–5033. 

