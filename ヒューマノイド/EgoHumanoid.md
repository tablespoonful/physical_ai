---
title: "EgoHumanoid: Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration"
date: "2026-02-10"
authors: "Modi Shi; Shijia Peng; Jin Chen; Haoran Jiang; Tianyu Li; Di Huang"
url: https://arxiv.org/abs/2602.10106
pdf: https://arxiv.org/pdf/2602.10106
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.10106)** / [論文ページ](https://arxiv.org/abs/2602.10106)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Unlocking In-the-Wild Loco-Manipulation with Robot-Free Egocentric Demonstration 

Modi Shi<sup>2</sup><sup>_,_3</sup><sup>_∗_</sup> Shijia Peng<sup>1</sup><sup>_∗†_</sup> Jin Chen<sup>2</sup><sup>_∗_</sup> Haoran Jiang<sup>2</sup> Tianyu Li<sup>2</sup> Di Huang<sup>3</sup> Ping Luo<sup>1</sup><sup>_†_</sup> Hongyang Li<sup>1</sup><sup>_♮_</sup> Li Chen<sup>1</sup><sup>_♮_</sup> 

> 1 The University of Hong Kong 2 Shanghai Innovation Institute 3 Beihang University https://opendrivelab.com/EgoHumanoid 


Fig. 1: Introducing **EGOHUMANOID** , the first investigation on human-to-humanoid transfer for whole-body loco-manipulation. Robot teleoperation data collection is constrained to laboratory environment due to hardware and safety limitations, while inthe-wild human demonstrations offer scalable diversity in objects, scenes, lighting, and viewpoints. Our alignment pipeline bridges the embodiment gap through view and action alignment, enabling vision-language-action (VLA) co-training on both data sources. Real-world loco-manipulation deployment validates that egocentric human demonstrations invigorate generalization _without_ scene-specific robot data, outperforming robot-only baselines by 51% with consistent scaling behavior. 

**_Abstract_ —Human demonstrations offer rich environmental diversity and scale naturally, making them an appealing alternative to robot teleoperation. While this paradigm has advanced robotarm manipulation, its potential for the more challenging, datahungry problem of humanoid loco-manipulation remains largely unexplored. We present EGOHUMANOID, the first framework to co-train a vision-language-action policy using abundant egocentric human demonstrations together with a limited amount of robot data, enabling humanoids to perform loco-manipulation across diverse real-world environments. To bridge the embodiment gap between humans and robots, including discrepancies in physical morphology and viewpoint, we introduce a systematic alignment pipeline spanning from hardware design to data processing. A portable system for scalable human data collection is developed, and we establish practical collection protocols to improve transferability. At the core of our human-to-humanoid** 

> _∗_ Equal Contribution. _♮_ Project lead. _†_ Work done while at Kinetix AI. 

**alignment pipeline lies two key components. The view alignment reduces visual domain discrepancies caused by camera height and perspective variation. The action alignment maps human motions into a unified, kinematically feasible action space for humanoid control. Extensive real-world experiments demonstrate that incorporating robot-free egocentric data significantly outperforms robot-only baselines by 51%, particularly in unseen environments. Our analysis further reveals which behaviors transfer effectively and the potential for scaling human data.** 

## I. INTRODUCTION 

Humanoid robots hold immense promise for operating across diverse human-centric environments, from household assistance to outdoor service scenarios [23]. These applications fundamentally demand _loco-manipulation_ , which involves the 

close orchestration of whole-body locomotion and dexterous manipulation [38, 54, 77]. Unlike fixed-base manipulators [31, 5, 70], robots must navigate through varied spaces, adjust their body posture for reachability, and manipulate objects, all while maintaining dynamic balance in unstructured environments. 

Despite rapid progress in model architectures and control algorithms, learning humanoid loco-manipulation remains bottlenecked by the _scarcity_ of diverse, large-scale demonstration data. Existing approaches [18, 3] primarily rely on robot teleoperation, which provides embodiment-consistent supervision but suffers from high cost, operational complexity, and hardware instability [38, 25, 73]. Moreover, it confines data collection to the laboratory environment, as transporting humanoid platforms and teleoperation equipment such as motion capture suits to diverse real-world scenarios, _e.g._ , homes, parks, stores, outdoor spaces, is often impractical [81, 74]. 

We instead provide a compelling alternative based on the simple observation: humans naturally perform locomanipulation tasks every day, exactly across the environments where robots are expected to operate. Recent advances in wearable sensing [15, 22, 50] make it possible to capture egocentric human demonstrations using lightweight, portable devices, without requiring any robot hardware. This paradigm offers scalable access to behaviorally rich and environmentally diverse data, and has induced progress in robot manipulation and navigation [32, 29, 55, 83, 49, 30, 10]. 

However, applying egocentric human demonstrations to humanoid control is far from straightforward due to the fundamental _embodiment gap_ . Humanoid robots differ substantially from humans in morphology and kinematics, including limb proportions and joint limits [78, 65]. Egocentric visual observations also differ – humans observe their own hands and body, whereas robots perceive metallic manipulators from distinct viewpoints [12, 81]. Moreover, motion dynamics diverge, as human walking patterns, body sway, and balance strategies do not directly transfer to robots with different mass distributions and actuation constraints [49, 83]. Collectively, these discrepancies are pronounced in loco-manipulation, where wholebody movement amplifies viewpoint change and introduces substantial motion variation in the egocentric observations. 

To this end, we present **EGOHUMANOID** , a systematic framework for human–humanoid co-training as described in Fig. 1. Our key insight is that while low-level actions are embodiment-specific, high-level behavioral structures ( _e.g._ , navigation routes, object approach strategies, and task decomposition) _could_ transfer reliably when observations and motions are properly aligned. Moreover, human demonstrations in diverse real-world settings expose policies to variations that robot-only data rarely covers, enabling stronger in-the-wild generalization. Accordingly, we build a data collection system that captures both robot-free human demonstrations and teleoperated humanoid robot data. The portable human setup integrates a VR headset, body trackers for pose estimation, and an egocentric camera, enabling scalable collection in varied scenarios without robot hardware. Complementary robot data, collected via VR-based teleoperation, provides embodiment- 

accurate supervision for manipulation-intensive behaviors. 

The embodiment alignment pipeline is proposed to convert human demonstrations into robot-compatible training signals. Our approach focuses on two core components. The view alignment reduces visual discrepancies by transforming human egocentric observations to approximate robot viewpoints using depth-based reprojection and inpainting. The action alignment employs a unified action space shared by humans and robots, using delta end-effector poses for upper body control and discrete commands for locomotion. Together, these mechanisms guarantee the VLA policy co-training on both data sources. 

**EGOHUMANOID** is validated on a Unitree G1 humanoid robot across four indoor and outdoor loco-manipulation tasks. Experiments demonstrate that incorporating human data significantly improves policy performance by 20% on average and enables generalization to scenes not covered by the robot data, yielding a 51% performance gain. Through extensive ablation studies, we scrutinize the transfer mechanism for sub-tasks, validate the scaling effectiveness, and identify critical design choices in our alignment pipeline. 

In summary, the contributions are: **(a) The first endorsement of human-to-humanoid transfer for whole-body locomanipulation tasks.** We show that egocentric human data effectively enhances humanoid policy through co-training, establishing the feasibility of cross-embodiment transfer with an integrated data collection and training framework. **(b) A principled embodiment alignment pipeline.** We propose practical strategies to bridge human-robot embodiment gaps, combining view alignment to mitigate visual disparities and action alignment to enforce kinematic feasibility. **(c) Comprehensive real-world evaluation and analysis.** We characterize which behaviors transfer effectively, how to scale human data, and exhibit that human data substantially boosts generalization beyond the robot-only training environment. 

We hope this study could encourage broader exploration of egocentric human data as a scalable pathway toward generalizable humanoid control, and lay the groundwork for transferring human behaviors to complex loco-manipulation skills. 

## II. RELATED WORK 

## _A. Egocentric Human Data for Robots_ 

Egocentric human data has emerged as a promising source for robot learning, offering scalable collection in diverse environments without robot hardware. Various systems enable robot-free data capture, including handheld grippers with mounted cameras [12, 80], wearable glasses [15], and VR/AR headsets such as Apple Vision Pro, Meta Quest, and PICO. Such data has been leveraged in multiple ways for embodied AI. One line of work trains vision-language models on largescale egocentric datasets [21, 22, 67, 39, 36, 76] to enhance scene understanding and spatial reasoning, with applications in embodied question answering [42] and egocentric decisionmaking [62]. For robot policy learning, prior work primarily adopts a pretraining-then-finetuning paradigm, using human data to learn visual representations [43, 41, 75], motion priors [44, 82, 66, 71], or latent action embeddings [68, 6, 27], 

discarding action information during pretraining. Co-training, in contrast, leverages actions from both human and robot demonstrations as supervision through aligned observation and action spaces, enabling more effective knowledge transfer [49, 30, 83, 72]. However, existing co-training approaches focus on fixed-base manipulation. Our work presents the first validation of human-robot co-training for humanoid loco-manipulation, addressing the unique challenges of transferring whole-body human demonstrations to mobile humanoid platforms. 

## _B. Cross-Embodiment Data Alignment_ 

In robot-to-robot transfer, Mirage [8] reduces visual mismatch by rewriting robots in images through cross-painting and inpainting, while Chen _et al._ [9] use generative models to augment robot appearances and viewpoints. For action alignment, common approaches either adopt transferable taskspace or end-effector control interfaces [8, 60, 53], or project heterogeneous state–action spaces into a shared latent representation [59, 37, 13]. Human-to-robot transfer is more challenging due to large gaps in morphology, viewpoint, and motion dynamics, but it is attractive given the scale of human data. The UMI series [12, 80, 63, 61] makes human demonstrations robot-compatible at collection time using hand-held hardware that provides accurate global positions. However, this hand-held hardware ties the collected data to a specific gripper morphology. Another line of work relies on motion retargeting, mapping human motions to robot configurations [2, 65, 19], which is usually employed for training low-level humanoid controllers [24, 11, 57]. This paradigm is further used by several concurrent manipulation or navigation-centered works, through estimating hand poses from egocentric human videos for joint training with robot data [29, 83, 30, 72]. They focus on manipulation solely or decouple these two subtasks for mobile robots to prevent base shift. Contrarily, our work targets humanoid loco-manipulation with tightly-coupled whole-body coordination. We address the larger morphological gap through dedicated view transformation, including reprojection and generation, and action retargeting to fully exploit egocentric human demonstrations. 

## _C. Humanoid Loco-Manipulation_ 

Humanoid loco-manipulation couples locomotion and manipulation, as well as task planning, where both reliable execution and scalable supervision remain challenging. Note that “whole-body” here is used at the task level rather than full joint-level actuation. Inspired by humanoid wholebody control [24, 1, 57, 48], emerging works build locomanipulation skills with reinforcement learning, typically relying on specifically modeled objects in simulation, carefully designed rewards, and learning curricula to handle the strong coupling between base motion and arm–hand interaction [25, 77, 69, 78]. However, these methods face scaling bottlenecks such as per-contact physics tuning, intractable affordance modeling, and unmodeled hardware non-idealities. In parallel, recent works explore scaling supervision through motion- or language-conditioned generation, aiming to lower 

the burden of expensive robot teleoperation needed for new tasks [17, 14, 64, 56]. VLA policies have been developed from manipulation methods as well, by extending models with lower-body robot action commands [27, 81, 46] or motion targets [40, 4, 16]. Despite this progress, most pipelines still scale primarily through robot-centered data or constrained setups, enduring the lack of environmental diversity and laborious data collection process, which prevents studying generalization in human-centric scenes. In sharp contrast, we treat robotfree egocentric human demonstrations as a scalable source of diverse whole-body behaviors to complement robot data, and we provide a starting point to co-train a humanoid VLA with two sources of data corpus through explicit view and action alignment. 

## III. EGOHUMANOID FRAMEWORK 

We present the EGOHUMANOID framework for training humanoid loco-manipulation policies by leveraging both egocentric human demonstrations and teleoperated robot data. The overview is illustrated in Fig. 1. We first formalize the problem setup (Sec. III-A), then describe our data collection system (Sec. III-B), embodiment alignment pipeline (Sec. III-C), and policy training procedure (Sec. III-D). 

## _A. Problem Setup_ 

Our goal is to train a VLA model capable of completing loco-manipulation tasks across novel real-world environments. The policy is trained on a combined dataset _D_ = _D_ robot _∪ D_ human, where _D_ robot consists of teleoperated robot demonstrations collected in constrained laboratory settings, and _D_ human comprises egocentric human demonstrations of the same tasks captured across diverse scenarios, _e.g._ , homes, stores, and outdoor environments. Each data episode in _D_ contains egocentric videos and synchronized whole-body actions. 

After training, the policy is deployed under two settings: (1) _in-domain_ evaluation in laboratory environments similar to those in _D_ robot, and (2) _generalization_ evaluation in scenes covered by _D_ human but absent from _D_ robot. This setup directly tests whether human data enables generalization beyond the limited scenes where robot teleoperation is feasible. 

We use a mid-sized (1.3m) Unitree G1 humanoid robot as our hardware platform, on account of its robust performance in low-level controller and durability. Meanwhile, the robot bares huge embodiment gap with normal teleoperators considering its size and degree of freedom (29 DoF with 3-finger Dex3 dexterous hands). Unlike prior work on tabletop bimanual manipulation, where the robot base remains stationary, we focus on tasks that require whole-body coordination—the robot must locomote to target locations while simultaneously or sequentially performing manipulation. This fundamental requirement for lower-body mobility distinguishes humanoid loco-manipulation from fixed-base settings and motivates our investigation of human-to-humanoid transfer. 

## _B. Data Collection System_ 

Crucially, robots and humans differ in practicality and embodiment. Robot data collection typically requires expensive 


Fig. 2: **Hardware setup for data collection.** Humans and the G1 humanoid robot are equipped with an integrated VR-based system for portable usage and agile development. The same camera captures egocentric recordings. The VR headset and trackers provide coarse human poses, while the VR controller is employed to teleoperate the robot. 

hardware, careful setup, and is mostly bound to laboratories, while human data can be collected cheaply and flexibly using wearable devices in diverse settings. To mitigate the embodiment and visual gap in the data collection level and support human-robot co-training, we develop a unified and portable hardware setup with a VR-based system for swift adaptation between the two collection modes, shown in Fig. 2. We intentionally drop wrist cameras as egocentric-only is a more universal setup, and the benefits of wrist views are not deterministic due to the enormous gaps, as shown in previous works [30] (See more discussion in Sec. V). The efficiency of human demonstration contrast to robot teleoperation is pronounced ( _∼_ 2 _×_ ) and detailed in Table III. 

**Human Data Collection.** We use a portable PICO VR setup that enables low-cost and unconstrained recording of human demonstrations in both indoor and outdoor settings. The subject wears the headset with five PICO Motion Trackers, while a head-mounted ZED X Mini camera captures synchronized egocentric RGB images. Using the PICO SDK [79], we record full-body human motion in real time, including 24 body keypoints and detailed hand poses with 26 keypoints per hand. **Robot Data Collection.** Robot demonstrations are collected through VR-based teleoperation. The operator wears a PICO VR headset and uses handheld controllers to issue navigation commands (forward/backward, lateral movement, turning, standing, squatting) and wrist pose commands derived from the controller-to-headset relative pose. These commands are converted to joint-level actions through inverse kinematics and executed on a Unitree G1 humanoid, while the controller trigger controls grasping of a Dex3 dexterous hand. A lowlevel locomotion policy [45] ensures stable whole-body exe- 

cution. We record navigation commands, wrist poses of the end-effector, hand grasp states, and synchronized egocentric RGB images from a head-mounted ZED X Mini camera. 

_C. Human-to-Humanoid Alignment_ 

To transform human demonstrations captured by the VR setup in Sec. III-B into robot-compatible training data, we develop an alignment pipeline consisting of two main modules, view alignment and action alignment for addressing visual domain gaps from differing camera viewpoints and action representation gaps from morphological discrepancies, respectively. The procedure is depicted in Fig. 3 and described below. More implementation details are provided in Appendix C. 

**View Alignment.** The substantial height discrepancy between humans and humanoid robots results in pronounced differences in egocentric visual observations. To bridge this visual gap, we transform human egocentric images to approximate robot camera viewpoints through a three-stage process. First, we use MoGe [58] to infer an affine-invariant per-pixel 3D point map via its reprojection-based focal/shift recovery, and derive a scale-invariant depth map. We then transform the recovered 3D points into the target robot camera frame and project them onto the target image plane. During training, random perturbations are applied to the target pose to encourage robustness to viewpoint variations. Note that the reprojection can produce missing regions due to invalid 3D predictions indicated by MoGe’s validity mask and view-dependent disocclusions introduced by the pose change, leaving target pixels with no source correspondence. Therefore, the final step involves employing latent diffusion-based inpainting [51] to hallucinate the missing regions, conditioning on the observed context and the missing region mask. Throughout this, complete RGB images are generated for better mimicking robot egocentric inputs. 

**Action Alignment.** We design a unified action space that accommodates both human and robot demonstrations while respecting their kinematic differences. 

_Upper Body._ The actions are parameterized as 6-DoF delta end-effector poses, consistent with concurrent crossembodiment works [83, 30, 72, 71]. Using deltas avoids dependence on a globally aligned base frame, which could be ill-defined between human and robot recordings, enabling direct comparability across embodiments. We also avoid jointlevel retargeting [2] as it may introduce artifacts and perturb interaction-relevant hand–object geometry [65]. Explicitly, we express human wrist poses in a pelvis-centric frame, then smooth translations with a Savitzky-Golay filter [52]. For rotations, we filter in the SO(3) tangent space using log/exp maps to prevent quaternion interpolation ambiguities. Finally, the transformed data is downsampled from 100 Hz to 20 Hz to match robot control and output the delta pose between consecutive frames as the action. 

_Lower body._ To collect robot data, the operator issues navigation commands using a discrete set of constant-velocity primitives ( _i.e._ , forward/backward, left/right, turn left/right, stand/squat) through the VR setup, following common practice in humanoid loco-manipulation [3, 27]. To align human 


Fig. 3: **Pipeline of human-to-humanoid alignment. (a) View Alignment** : Egocentric images are transformed to approximate robot viewpoints by reprojecting estimated depth points and generative inpainting to fill in blank holes. **(b) Action Alignment** : We employ relative end-effector poses to unify the upper body action space, and discrete commands for lower-body locomotion. 

demonstrations with this robot action space, we convert the human pelvis trajectory into the same discrete commands. Specifically, we apply Savitzky–Golay smoothing to suppress jitter, then estimate the instantaneous heading via centered differences with a continuity constraint to prevent direction flips. Displacements in the world frame are projected on the local frame to obtain forward and lateral velocities. Yaw rate is computed from inter-frame heading changes. We downsample these continuous commands to 20 Hz by averaging within each control window, and quantize them into discrete bins of horizontal movements. Finally, a discrete stand/squat primitive is derived by thresholding inter-frame changes in pelvis height, matching the robot teleoperation interface. 

_Gripper._ We represent the gripper action as a binary variable _at_ = _{_ 0 _,_ 1 _}_ , where 1 corresponds to the gripper being closed and 0 corresponds to the gripper being open. During robot data collection, a teleoperator controls the gripper via a handheld controller, and the resulting binary command sequence _{at}_ is recorded. Human demonstrations are captured using the VR system that tracks 26 hand joints per hand. To robustly infer the hand grasping state, we first apply low-pass filtering followed by Savitzky-Golay smoothing to the raw joint trajectories. We then compute the finger-level curvature _κf_ , defined as the curvature evaluated at the midpoint of a quadratic polynomial fitted to each finger’s joint polyline. The hand-level grasping state is obtained by averaging _κf_ across all fingers and thresholding the resulting scalar _κ_ ¯ to produce a binary open/close label. This curvature-based representation mitigates noise and enables reliable supervision extraction from human demonstrations. Similarly, all human-derived signals are downsampled to 20 Hz to align temporally with the robot data. 

## _D. Loco-Manipulation Policy Co-Training_ 

With identical visual observation formats and action dimensions owing to the alignment procedure, we co-train a single policy on both human and robot demonstrations. Explicitly, we adapt _π_ 0 _._ 5 [26], a state-of-the-art VLA model, for humanoid loco-manipulation via finetuning. The policy receives egocentric RGB observations and language instructions as input, and outputs actions in our unified action space. We intentionally omit proprioceptive states, as morphological differences between humans and humanoids yield incompatible proprioceptive distributions that would confound co-training. 

**Multi-source Data Sampling.** In this case, the amount of human demonstrations may be substantially larger and more diverse than robot data, creating a highly imbalanced dataset. Prior work has shown that balanced sampling is essential for imbalanced multi-source training in robot manipulation [20, 28]. Meanwhile, loco-manipulation tasks require both highlevel navigation or locomotion and intricate manipulation, where human and robot data may feature distinct advantages in these aspects. Thereafter, we examine the human-to-robot sampling ratio within each mini-batch, preserving sufficient exposure to robot demonstrations (See Sec. IV-D). 

## IV. EVALUATIONS 

We conduct real-world experiments to evaluate the effectiveness of leveraging egocentric human data for humanoid locomanipulation. Our evaluation addresses three key questions: 

- **Q1: Generalization.** Does egocentric human data enable humanoid policies to generalize to diverse human-centric environments beyond laboratory settings? 

- **Q2: Transfer Analysis.** What behaviors transfer effectively from human demonstrations to humanoid policies? 

- **Q3: Data Scaling.** Does policy performance scale with increasing amounts of human demonstration data? 


Fig. 4: **Humanoid loco-manipulation tasks for evaluation.** We design four tasks which span varying levels of difficulty for large-space movement and dexterous manipulation. Robots are teleoperated in laboratories as the source domain ( **Top** ). Humancentric scenes occur in human demonstrations only **(Middle)** , and set as testbeds for generalization evaluation ( **Bottom** ). 


Fig. 5: **Performance of human-robot data co-training with EGOHUMANOID.** Our pipeline achieves unanimous improvements over robot-only baselines across in-domain and generalized environments. The boost is amplified in robots’ unseen settings. 

## _A. Real-world Experimental Setup_ 

We design four loco-manipulation tasks requiring tight coordination between locomotion and manipulation, illustrated in Fig. 4. All tasks involve non-trivial locomotion (1–5 _m_ ), distinguishing them from fixed-base bimanual manipulation. Navigation accuracy subsequently impacts manipulation success: suboptimal stopping positions render subsequent manipulation infeasible. The variance in stopping positions across trials further requires policies to generalize across viewpoints and object configurations. 

The four tasks are: (1) Pillow Placement. The robot carries a pillow to a bed and places it at a target location. This task tests stable locomotion with a bulky object and placement on a deformable surface. (2) Trash Disposal. The robot carries garbage (crumpled paper or a can) to a waste container with lids, inserts it horizontally into the hole rather than 

dropping from above, requiring precise localization and endeffector control. (3) Toy Transfer. The robot approaches a toy on a surface, grasps it, reorients, walks to a distant table, and places the toy down. This task evaluates sequential coordination across approach, grasp, in-hand locomotion, and placement. (4) Cart Stowing. The robot pushes a cart to a product display, grasps a toy, places it in the cart, and pushes the cart away. This task involves sustained contact during locomotion and multi-phase manipulation. 

We conduct 20 trials per setting with position perturbations, and normalized scores are adopted to evaluate the performance of each trial. We delineate complementary experimental details in Appendix C2, and list our scoring criteria in Appendix D. 

## _B. Will human data improve humanoid loco-manipulation?_ 

We evaluate whether co-training with robot-free egocentric demonstrations enables humanoid policies to generalize 

TABLE I: **Granular performance across tasks and subtasks.** Each task is roughly categorized into sub-steps of locomotion (including high-level navigation) or manipulation, represented in blue and red, respectively, and denoted as s1, s2, _etc_ . 


Fig. 6: **Failure mode analysis.** For each setting—(a) Robot-only, (b) Human-only, and (c) Co-training—we log all failed episodes. The Sankey diagrams break failures down into locomotion vs. manipulation errors and finer causes. 

beyond laboratory environments. We compare _Robot-only_ , trained exclusively on robot data, with _Co-training_ , trained on both sources using our alignment pipeline. Policies are evaluated under two settings: _In-Domain_ (laboratory environments) and _Generalization_ (diverse scenes covered only by human data). For these experiments, robot-only models use 100 episodes per task, while co-training absorbs 300 episodes of human demonstrations additionally. 

As shown in Fig. 5, co-training consistently improves performance across both settings. For in-domain evaluation, cotraining achieves 78% average score versus 59% for robotonly. The gap widens remarkably in generalization settings: co-training reaches 82% compared to 31% for robot-only. Notably, generalization performance exceeds in-domain results, indicating that human data effectively bridges the domain gap to novel environments. These results demonstrate that humanoid robots can operate in diverse real-world settings without in-the-wild robot data collection. 

## _C. Which subskill benefits most from the data transfer?_ 

Delving deeper into the results in Fig. 5, we examine which skills are primarily learned from human demos. We train a _Human-only_ model and analyze performance separately across locomotion and manipulation stages. Table I shows consecutive success rates of sub-steps. Though dependence exists among steps leading to a not strictly aligned ‘apple-toapple’ comparison, two observations emerge. 

First, navigation transfers effectively from human data alone. Human-only achieves 100% on navigation-dominated subtasks (Pillow Placement s1, Trash Disposal s1, Toy Transfer s1, Cart Stowing s1). Even on Toy Transfer s3, requiring two consecutive turns, Human-only attains 45%, only 15% 

below Co-training. In contrast, Robot-only yields near-zero success on these stages, confirming that human demonstrations provide transferable navigation knowledge. 

Second, manipulation also transfers but effectiveness diminishes with increasing precision requirements. Human-only outperforms Robot-only on coarse manipulation subtasks (Pillow Placement s2, Trash Disposal s2, Toy Transfer s2/s4), where approximate contact suffices. However, for precision-critical phases such as Cart Stowing s2, Human-only achieves only 5% versus Robot-only’s 15%. Notably, Co-training reaches 60% on this subtask, indicating that human data provides useful priors that become effective when combined with robot demos. 

The failure analysis in Fig. 6 corroborates these findings: Human-only exhibits three times more manipulation failures than locomotion failures, whereas Robot-only failures are balanced across both phases. 

## _D. Does Performance Scale with Human Data?_ 

We investigate how human demonstration quantity and mini-batch sampling ratio jointly affect policy performance. Fig. 7 presents results across four tasks as human demonstrations scale from 0 to 300 under varying sampling ratios. The optimal ratio depends on task characteristics: tasks requiring only coarse grasping ( _e.g._ , Pillow Delivery) benefit from higher human data ratios (Robot:Human 1:2), while fine manipulation tasks ( _e.g._ , Toy Transfer, Cart Shopping) favor higher robot ratios (Robot:Human 2:1). This aligns with our subtask analysis (Sec. IV-C), confirming that the embodiment gap disproportionately impacts precision-critical manipulation. 

Across all sampling ratios, results improves consistently as human demonstrations accumulate, verifying that our method scales effectively without overfitting to dominant human data. 


Fig. 7: **Scaling human demonstrations with various training-time data sampling strategies.** More human demonstrations, from robot-only (0 Human Demos) to 3 _×_ robot data (300 Human Demos), principally yield improved loco-manipulation performance in generalized scenarios. The optimal sampling ratio depends on task characteristics: manipulation-heavy tasks favor higher robot data ratios, while navigation-dominant tasks benefit from more human data. 


Fig. 8: **View alignment ablation.** View alignment is essential for effective human-robot co-training, especially for tasks involving variable object heights such as Toy Transfer. 

## _E. View Alignment Ablation_ 

We ablate the effect of view alignment in Fig. 8. View alignment yields consistent improvements across all tasks, with the largest gains on Toy Transfer and Cart Stowing. Both tasks involve objects placed at varying heights, creating deployment viewpoints that differ from both data sources: human demonstrations are captured from a higher camera position, while robot data is collected with objects at different heights. Without view alignment, the policy encounters out-ofdistribution viewpoints from either source. Our view transformation bridges this gap by reprojecting human observations to the robot’s camera height with added pose perturbations, exposing the policy to broader viewpoint variations during training. Visualizations are provided in Appendix E. 

## _F. Scene Diversity in Human Data_ 

We further investigate how scene diversity affects cotraining. Fixing the data quantity at 100 robot and 300 human demonstrations, we vary only the number of distinct human scenes and evaluate zero-shot in a novel scene unseen during training (Table II). The score rises monotonically from 57.5% 

(robot-only) to 82.5% with three scenes, indicating that scene diversity is a key driver of generalization even at fixed data quantity. 

## _G. Data Collection Efficiency_ 

As shown in Table III, human demonstrations are roughly 2 _×_ faster than robot teleoperation across all four tasks, reducing the per-episode collection time from 62.1 s to 39.7 s on average. 

## V. DISCUSSIONS 

Our work demonstrates inspiring pioneering results of learning humanoid loco-manipulation from human data, boosting robot-only baselines by a large margin as shown in Fig. 5. Yet, the overall success rate is not satisfactory, and typical failure cases are characterized in Fig. 6. Due to the instability of the humanoid and the huge embodiment gap, we find a bunch of critical factors that affect the performance significantly, even when equipped with the proposed pipeline. We present the devil in the details below, and also incorporate practical guidelines for data collection in Appendix B. 

**Action Representation.** Two candidate action spaces exist for human-robot alignment: absolute end-effector pose in camera frame and delta end-effector pose. We adopt the latter because human and humanoid morphologies yield systematically different hand-to-camera distances—human arms are typically longer relative to torso height, resulting in different absolute position distributions even for functionally equivalent poses. Delta end-effector naturally shares an identical action space. 

However, delta end-effector poses present a fundamental limitation: the correspondence between human hand orientation and robot gripper orientation is ambiguous. While we define explicit pose correspondences, these mappings are difficult to infer from visual observations alone. Consequently, without proprioceptive input, precise rotation transfer remains challenging—the policy cannot reliably disambiguate intended end-effector orientations from egocentric images, limiting finegrained rotational control in manipulation tasks. 

**Data Scale Requirements.** Humanoid loco-manipulation presents unique data efficiency challenges compared to fixedbase manipulation. These tasks require the robot to first 

TABLE II: **Effect of human demonstration scene diversity on zero-shot generalization.** We evaluate the Trash Disposal task in a novel scene unseen during training, progressively increasing the number of distinct human demonstration scenes while keeping robot data fixed. Sub-steps s1 (locomotion) and s2 (manipulation) are reported alongside the average task score. 

|**Training Data**|**# Human Scenes**|**s1**|**s2**|**Average Score**|
|---|---|---|---|---|
|Robot-only|0|70|45|57.5|
|Co-training|1|90|60|75.0|
|Co-training|2|**100**|50|75.0|
|Co-training|3|**100**|**65**|**82.5**|


TABLE III: **Comparison of data collection efficiency.** The average time ( _s_ ) for collection of each data episode shows the preeminent efficiency ( _∼_ 2 _×_ ) of gathering human demonstrations over teleoperating robots. 

|**Method**<br>**Pillow Placement**|**Trash Disposal**|**Toy Transfer**|**Cart Stowing**|**Average**|
|---|---|---|---|---|
|Robot teleop<br>35.7|43.1|66.2|103.5|62.1|
|Human demo<br>16.2|18.3|34.5|89.9|**39.7**|


navigate to the target location before performing manipulation—yet the robot rarely stops at precisely the same position, resulting in highly diverse viewpoints during the manipulation phase. This viewpoint variability raises substantially increasing data requirements. In our experiments, achieving comparable success rates on loco-manipulation tasks requires approximately 2–3× more demonstrations than fixedbase manipulation tasks of similar difficulty, highlighting the compounded challenge of learning both robust navigation and precise manipulation from egocentric observations. 

## VI. CONCLUSION 

We introduce EGOHUMANOID, the first framework to realize human-to-humanoid transfer for loco-manipulation. By aligning egocentric human demonstrations with robot data through view transformation and unified action space, our approach enables effective VLA co-training. Experiments demonstrate substantial generalization improvements, enabling deployment in diverse environments without in-the-wild robot data. We hope this work encourages broader exploration of egocentric human data toward generalizable humanoid control. 

**Limitations and Future Work.** As an early endeavor, our method still bears limitations with respect to orientation ambiguity in delta end-effector representations, scaling laws with human data, and expressive whole-body controls. We will take scaling up this paradigm with advanced egocentric hardware as key future direction. More discussions are in Appendix A. 

## ACKNOWLEDGMENTS 

This study is supported by National Natural Science Foundation of China (62206172). This work is in part supported by the JC STEM Lab of Autonomous Intelligent Systems funded by The Hong Kong Jockey Club Charities Trust. We gratefully acknowledge our robot operators for data collection and evaluations. We also extend our thanks to Jiazhi Yang, Tianyu Li, Yixuan Pan, Junli Ren, Penglin Fu, and Kaiyang Wu for their insightful feedback and fruitful discussions. 

## REFERENCES 

- [1] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. In _CoRL_ , 2025. 3 

- [2] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting Matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 3, 4 

- [3] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. HOMIE: Humanoid locomanipulation with isomorphic exoskeleton cockpit. In _RSS_ , 2025. 2, 4 

- [4] Boston Dynamics. Large behavior models help atlas find new footing. https://bostondynamics.com/blog/ large-behavior-models-atlas-find-new-footing/, 2025. 3 

- [5] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Xindong He, Xu Huang, et al. AgiBot World Colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. In _IROS_ , 2025. 2 

- [6] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. UniVLA: Learning to act anywhere with task-centric latent actions. In _RSS_ , 2025. 2 

- [7] Xiongyi Cai, Ri-Zhao Qiu, Geng Chen, Lai Wei, Isabella Liu, Tianshu Huang, Xuxin Cheng, and Xiaolong Wang. In-N-On: Scaling egocentric manipulation with in-thewild and on-task data. _arXiv preprint arXiv:2511.15704_ , 2025. 13 

- [8] Lawrence Yunliang Chen, Kush Hari, Karthik Dharmarajan, Chenfeng Xu, Quan Vuong, and Ken Goldberg. Mirage: Cross-embodiment zero-shot policy transfer with cross-painting. In _RSS_ , 2024. 3 

- [9] Lawrence Yunliang Chen, Chenfeng Xu, Karthik Dharmarajan, Muhammad Zubair Irshad, Richard Cheng, Kurt Keutzer, Masayoshi Tomizuka, Quan Vuong, and Ken 

   - Goldberg. RoVi-Aug: Robot and viewpoint augmentation for cross-embodiment robot learning. In _CoRL_ , 2024. 3 

- [10] Li Chen, Chonghao Sima, Kashyap Chitta, Antonio Loquercio, Ping Luo, Yi Ma, and Hongyang Li. Intelligent robot manipulation requires self-directed learning. _Authorea Preprints_ , 2025. 2 

- [11] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. GMT: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 3 

- [12] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal Manipulation Interface: In-thewild robot teaching without in-the-wild robots. In _RSS_ , 2024. 2, 3 

- [13] Apan Dastider, Hao Fang, and Mingjie Lin. Crossembodiment robotic manipulation synthesis via guided demonstrations through cyclevae and human behavior transformer. _arXiv preprint arXiv:2503.08622_ , 2025. 3 

- [14] Pengxiang Ding, Jianfei Ma, Xinyang Tong, Binghong Zou, Xinxin Luo, Yiguo Fan, Ting Wang, Hongchao Lu, Panzhong Mo, Jinxin Liu, et al. Humanoid-VLA: Towards universal humanoid control with visual integration. _arXiv preprint arXiv:2502.14795_ , 2025. 3 

- [15] Jakob Engel, Kiran Somasundaram, Michael Goesele, Albert Sun, Alexander Gamino, Andrew Turner, Arjang Talattof, Arnie Yuan, Bilal Souti, Brighid Meredith, et al. Project Aria: A new tool for egocentric multi-modal ai research. _arXiv preprint arXiv:2308.13561_ , 2023. 2 

- [16] Figure. Introducing Helix 02: Full-body autonomy. https: //www.figure.ai/news/helix-02, 2026. 3 

- [17] Yuhui Fu, Feiyang Xie, Chaoyi Xu, Jing Xiong, Haoqi Yuan, and Zongqing Lu. DemoHLM: From one demonstration to generalizable humanoid loco-manipulation. _arXiv preprint arXiv:2510.11258_ , 2025. 3 

- [18] Zipeng Fu, Tony Z. Zhao, and Chelsea Finn. Mobile ALOHA: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. In _CoRL_ , 2024. 2 

- [19] Zipeng Fu, Qingqing Zhao, Qi Wu, Gordon Wetzstein, and Chelsea Finn. HumanPlus: Humanoid shadowing and imitation from humans. In _CoRL_ , 2025. 3 

- [20] Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, et al. Octo: An open-source generalist robot policy. In _RSS_ , 2024. 5 

- [21] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4D: Around the world in 3,000 hours of egocentric video. In _CVPR_ , 2022. 2 

- [22] Kristen Grauman, Andrew Westbury, Lorenzo Torresani, Kris Kitani, Jitendra Malik, Triantafyllos Afouras, Kumar Ashutosh, Vijay Baiyya, Siddhant Bansal, Bikram Boote, et al. Ego-Exo4D: Understanding skilled human activity from first- and third-person perspectives. In _CVPR_ , 2024. 2 

- [23] Zhaoyuan Gu, Junheng Li, Wenlan Shen, Wenhao Yu, Zhaoming Xie, Stephen McCrory, Xianyi Cheng, Abdulaziz Shamsah, Robert Griffin, C Karen Liu, et al. Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. _IEEE/ASME TMECH_ , 2025. 1 

- [24] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris M Kitani, Changliu Liu, and Guanya Shi. OmniH2O: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. In _CoRL_ , 2025. 3, 13 

- [25] Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando Casta˜neda, Shankar Sastry, et al. VIRAL: Visual simto-real at scale for humanoid loco-manipulation. _arXiv preprint arXiv:2511.15200_ , 2025. 2, 3 

- [26] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In _CoRL_ , 2025. 5, 14, 17 

- [27] Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, Chuang Wang, Zhihui Peng, et al. WholeBodyVLA: Towards unified latent vla for whole-body loco-manipulation control. In _ICLR_ , 2026. 2, 3, 4 

- [28] Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, Benjamin Swanson, Rico Jonschkowski, Chelsea Finn, Sergey Levine, and Karol Hausman. MT-Opt: Continuous multi-task robotic reinforcement learning at scale. _arXiv preprint arXiv:2104.08212_ , 2021. 5 

- [29] Simar Kareer, Dhruv Patel, Ryan Punamiya, Pranay Mathur, Shuo Cheng, Chen Wang, Judy Hoffman, and Danfei Xu. EgoMimic: Scaling imitation learning via egocentric video. In _ICRA_ , 2025. 2, 3 

- [30] Simar Kareer, Karl Pertsch, James Darpinian, Judy Hoffman, Danfei Xu, Sergey Levine, Chelsea Finn, and Suraj Nair. Emergence of human to robot transfer in vision-language-action models. _arXiv preprint arXiv:2512.22414_ , 2025. 2, 3, 4, 13 

- [31] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. OpenVLA: An open-source vision-language-action model. In _CoRL_ , 2024. 2 

- [32] Ashish Kumar, Saurabh Gupta, and Jitendra Malik. Learning navigation subroutines from egocentric videos. In _CoRL_ , 2019. 2 

- [33] Marion Lepert, Jiaying Fang, and Jeannette Bohg. Masquerade: Learning from in-the-wild human videos using data-editing. _arXiv preprint arXiv:2508.09976_ , 2025. 13 

- [34] Marion Lepert, Jiaying Fang, and Jeannette Bohg. Phantom: Training robots without robots using only human videos. _arXiv preprint arXiv:2503.00779_ , 2025. 13 

- [35] Guangrun Li, Yaoxu Lyu, Zhuoyang Liu, Chengkai Hou, Jieyu Zhang, and Shanghang Zhang. H2r: A human- 

to-robot data augmentation for robot pre-training from videos. _arXiv preprint arXiv:2505.11920_ , 2025. 13 

- [36] Kevin Qinghong Lin, Jinpeng Wang, Mattia Soldan, Michael Wray, Rui Yan, Eric Z Xu, Difei Gao, RongCheng Tu, Wenzhe Zhao, Weijie Kong, et al. Egocentric video-language pretraining. In _NeurIPS_ , 2022. 2 

- [37] Junjia Liu, Zhuo Li, Minghao Yu, Zhipeng Dong, Sylvain Calinon, Darwin Caldwell, and Fei Chen. Humanhumanoid robots cross-embodiment behavior-skill transfer using decomposed adversarial learning from demonstration. _RAM_ , 2025. 3 

- [38] Chenhao Lu, Xuxin Cheng, Jialong Li, Shiqi Yang, Mazeyu Ji, Chengjing Yuan, Ge Yang, Sha Yi, and Xiaolong Wang. Mobile-TeleVision: Predictive motion priors for humanoid whole-body control. In _ICRA_ , 2025. 2 

- [39] Hao Luo, Zihao Yue, Wanpeng Zhang, Yicheng Feng, Sipeng Zheng, Deheng Ye, and Zongqing Lu. OpenMMEgo: Enhancing egocentric understanding for lmms with open weights and data. In _NeurIPS_ , 2025. 2 

- [40] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Casta˜neda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. SONIC: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 3, 13 

- [41] Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. VIP: Towards universal visual reward and representation via value-implicit pre-training. In _ICLR_ , 2023. 2 

- [42] Arjun Majumdar, Anurag Ajay, Xiaohan Zhang, Pranav Putta, Sriram Yenamandra, Mikael Henaff, Sneha Silwal, Paul Mcvay, Oleksandr Maksymets, Sergio Arnaud, et al. OpenEQA: Embodied question answering in the era of foundation models. In _CVPR_ , 2024. 2 

- [43] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3M: A universal visual representation for robot manipulation. In _CoRL_ , 2022. 2 

- [44] Yaru Niu, Yunzhe Zhang, Mingyang Yu, Changyi Lin, Chenhao Li, Yikai Wang, Yuxiang Yang, Wenhao Yu, Tingnan Zhang, Zhenzhen Li, Jonathan Francis, Bingqing Chen, Jie Tan, and Ding Zhao. Human2LocoMan: Learning versatile quadrupedal manipulation with human pretraining. In _RSS_ , 2025. 2 

- [45] NVIDIA. GR00T-WholeBodyControl. https://github. com/NVlabs/GR00T-WholeBodyControl, 2025. 4, 13, 15, 17 

- [46] NVIDIA. GR00T N1.6: An improved open foundation model for generalist humanoid robots. https://research. nvidia.com/labs/gear/gr00t-n1 <u>6/,</u> 2025. 3 

- [47] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin ElNouby, et al. DINOv2: Learning robust visual features without supervision. _TMLR_ , 2024. 17 

- [48] Yixuan Pan, Ruoyi Qiao, Li Chen, Kashyap Chitta, Liang 

Pan, Haoguang Mai, Qingwen Bu, Cunyuan Zheng, Hao Zhao, Ping Luo, and Hongyang Li. Agility Meets Stability: Versatile humanoid control with heterogeneous data. In _ICRA_ , 2026. 3, 13 

- [49] Ri-Zhao Qiu, Shiqi Yang, Xuxin Cheng, Chaitanya Chawla, Jialong Li, Tairan He, Ge Yan, David J Yoon, Ryan Hoque, Lars Paulsen, et al. Humanoid policy ˜ human policy. In _CoRL_ , 2025. 2, 3 

- [50] TARS Robotics, Yuhang Zheng, Jichao Peng, Weize Li, Yupeng Zheng, Xiang Li, Yujie Jin, Julong Wei, Guanhua Zhang, Ruiling Zheng, et al. World In Your Hands: A large-scale and open-source ecosystem for learning human-centric manipulation in the wild. _arXiv preprint arXiv:2512.24310_ , 2025. 2 

- [51] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _CVPR_ , 2022. 4, 14, 17 

- [52] Ronald W. Schafer. What is a savitzky-golay filter? [lecture notes]. _IEEE SPM_ , 2011. 4 

- [53] Modi Shi, Li Chen, Jin Chen, Yuxiang Lu, Chiming Liu, Guanghui Ren, Ping Luo, Di Huang, Maoqing Yao, and Hongyang Li. Is diversity all you need for scalable robotic manipulation? _arXiv preprint arXiv:2507.06219_ , 2025. 3 

- [54] Wandong Sun, Luying Feng, Baoshi Cao, Yang Liu, Yaochu Jin, and Zongwu Xie. ULC: A unified and fine-grained controller for humanoid loco-manipulation. _arXiv preprint arXiv:2507.06905_ , 2025. 2 

- [55] Tony Tao, Mohan Kumar Srirama, Jason Jingzhou Liu, Kenneth Shaw, and Deepak Pathak. DexWild: Dexterous human interactions for in-the-wild robot policies. In _RSS_ , 2025. 2 

- [56] Ilyass Taouil, Haizhou Zhao, Angela Dai, and Majid Khadiv. Physically consistent humanoid locomanipulation using latent diffusion models. In _HUMANOIDS_ , 2025. 3 

- [57] Takara E Truong, Qiayuan Liao, Xiaoyu Huang, Guy Tevet, C Karen Liu, and Koushil Sreenath. BeyondMimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 3 

- [58] Ruicheng Wang, Sicheng Xu, Cassie Dai, Jianfeng Xiang, Yu Deng, Xin Tong, and Jiaolong Yang. MoGe: Unlocking accurate monocular geometry estimation for open-domain images with optimal training supervision. In _CVPR_ , 2025. 4, 14, 17 

- [59] Tianyu Wang, Dwait Bhatt, Xiaolong Wang, and Nikolay Atanasov. Cross-embodiment robot manipulation skill transfer using latent space alignment. _arXiv preprint arXiv:2406.01968_ , 2024. 3 

- [60] Zhenyu Wei, Zhixuan Xu, Jingxiang Guo, Yiwen Hou, Chongkai Gao, Zhehao Cai, Jiayu Luo, and Lin Shao. _D_ ( _R, O_ ) Grasp: A unified representation of robot and object interaction for cross-embodiment dexterous grasping. In _ICRA_ , 2025. 3 

- [61] Longyan Wu, Checheng Yu, Jieji Ren, Li Chen, Yufei Jiang, Ran Huang, Guoying Gu, and Hongyang Li. FreeTacMan: Robot-free visuo-tactile data collection system for contact-rich manipulation. _arXiv preprint arXiv:2506.01941_ , 2025. 3 

- [62] Boshen Xu, Yuting Mei, Xinbi Liu, Sipeng Zheng, and Qin Jin. EgoDTM: Towards 3d-aware egocentric videolanguage pretraining. In _NeurIPS_ , 2025. 2 

- [63] Mengda Xu, Han Zhang, Yifan Hou, Zhenjia Xu, Linxi Fan, Manuela Veloso, and Shuran Song. DexUMI: Using human hand as the universal manipulation interface for dexterous manipulation. In _CoRL_ , 2025. 3 

- [64] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, et al. LeVERB: Humanoid whole-body control with latent visionlanguage instruction. _arXiv preprint arXiv:2506.13751_ , 2025. 3 

- [65] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. OmniRetarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 2, 3, 4 

- [66] Ruihan Yang, Qinxi Yu, Yecheng Wu, Rui Yan, Borui Li, An-Chieh Cheng, Xueyan Zou, Yunhao Fang, Xuxin Cheng, Ri-Zhao Qiu, et al. EgoVLA: Learning visionlanguage-action models from egocentric human videos. _arXiv preprint arXiv:2507.12440_ , 2025. 2 

- [67] Hanrong Ye, Haotian Zhang, Erik Daxberger, Lin Chen, Zongyu Lin, Yanghao Li, Bowen Zhang, Haoxuan You, Dan Xu, Zhe Gan, Jiasen Lu, and Yinfei Yang. MMEgo: Towards building egocentric multimodal LLMs for video QA. In _ICLR_ , 2025. 2 

- [68] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent action pretraining from videos. In _ICLR_ , 2025. 2 

- [69] Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C Karen Liu, and Jiajun Wu. VisualMimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 3 

- [70] Checheng Yu, Chonghao Sima, Gangcheng Jiang, Hai Zhang, Haoguang Mai, Hongyang Li, Huijie Wang, Jin Chen, Kaiyang Wu, Li Chen, Lirui Zhao, Modi Shi, Ping Luo, Qingwen Bu, Shijia Peng, Tianyu Li, and Yibo Yuan. _χ_ 0: Resource-aware robust manipulation via taming distributional inconsistencies. _arXiv preprint arXiv:2602.09021_ , 2026. 2 

- [71] Justin Yu, Yide Shentu, Di Wu, Pieter Abbeel, Ken Goldberg, and Philipp Wu. EgoMI: Learning active vision and whole-body manipulation from egocentric human demonstrations. _arXiv preprint arXiv:2511.00153_ , 2025. 2, 4 

- [72] Chengbo Yuan, Rui Zhou, Mengzhen Liu, Yingdong Hu, Shengjie Wang, Li Yi, Chuan Wen, Shanghang Zhang, 

and Yang Gao. MotionTrans: Human vr data enable motion-level learning for robotic manipulation policies. _arXiv preprint arXiv:2509.17759_ , 2025. 3, 4, 13 

- [73] Yanjie Ze, Zixuan Chen, Jo˜ao Pedro Ara´ujo, Zi ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. TWIST: Teleoperated whole-body imitation system. In _CoRL_ , 2025. 2, 13 

- [74] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C Karen Liu. TWIST2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 2 

- [75] Jia Zeng, Qingwen Bu, Bangjun Wang, Wenke Xia, Li Chen, Hao Dong, Haoming Song, Dong Wang, Di Hu, Ping Luo, et al. Learning manipulation by predicting interaction. In _RSS_ , 2024. 2 

- [76] Hai Zhang, Siqi Liang, Li Chen, Yuxian Li, Yukang Xu, Yichao Zhong, Fu Zhang, and Hongyang Li. Sparse video generation propels real-world beyondthe-view vision-language navigation. _arXiv preprint arXiv:2602.05827_ , 2026. 2 

- [77] Yuanhang Zhang, Yifu Yuan, Prajwal Gurunath, Tairan He, Shayegan Omidshafiei, Ali-akbar Agha-mohammadi, Marcell Vazquez-Chanlatte, Liam Pedersen, and Guanya Shi. FALCON: Learning force-adaptive humanoid locomanipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 2, 3 

- [78] Siheng Zhao, Yanjie Ze, Yue Wang, C Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. ResMimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 2, 3 

- [79] Zhigen Zhao, Liuchuan Yu, Ke Jing, and Ning Yang. XRoboToolkit: A cross-platform framework for robot teleoperation. _arXiv preprint arXiv:2508.00097_ , 2025. 4, 17 

- [80] Zhaxizhuom Zhaxizhuoma, Kehui Liu, Chuyue Guan, Zhongjie Jia, Ziniu Wu, Xin Liu, Tianyu Wang, Shuai Liang, Pengan CHEN, Pingrui Zhang, et al. FastUMI: A scalable and hardware-independent universal manipulation interface with dataset. In _CoRL_ , 2025. 2, 3 

- [81] Rui Zhong, Yizhe Sun, Junjie Wen, Jinming Li, Chuang Cheng, Wei Dai, Zhiwen Zeng, Huimin Lu, Yichen Zhu, and Yi Xu. HumanoidExo: Scalable whole-body humanoid manipulation via wearable exoskeleton. _arXiv preprint arXiv:2510.03022_ , 2025. 2, 3 

- [82] Jiaming Zhou, Teli Ma, Kun-Yu Lin, Zifan Wang, Ronghe Qiu, and Junwei Liang. Mitigating the humanrobot domain discrepancy in visual pre-training for robotic manipulation. In _CVPR_ , 2025. 2 

- [83] Lawrence Y Zhu, Pranav Kuppili, Ryan Punamiya, Patcharapong Aphiwetsa, Dhruv Patel, Simar Kareer, Sehoon Ha, and Danfei Xu. EMMA: Scaling mobile manipulation via egocentric human data. _arXiv preprint arXiv:2509.04443_ , 2025. 2, 3, 4, 13 

## APPENDIX 

Demo recordings are provided along with this supplementary material. We will open-source our code and data to facilitate future research in learning humanoid policies with human demonstrations. 

In the appendix, we first provide a list of motivating questions in Sec. A, and practical guidelines for data collection to benefit human-to-robot transfer in Sec. B. Implementation details on EGOHUMANOID and the real-world experiments are presented in Sec. C. Sec. D outlines the scoring criteria when evaluating the experiments to get the scores in the main paper. We show qualitative results on human-to-humanoid alignment in Sec. E. Lastly, the licenses of the assets used in our work are provided in Sec. F. 

## _A. Motivating Questions_ 

To help an instinctive and thorough comprehension of our work, we present several motivating questions that might be raised and corresponding answers below. 

**Q1.** _Why co-train two sources of data in the post-training stage? How about leveraging human data in pre-training?_ 

These two research focuses are compatible and can work harmoniously. Pre-training with human data has been a hot topic in recent years [83, 7], especially in enhancing the generality of the foundation model, while effective co-training embodied policies remains puzzled. Co-training in post-training serves as an initial investigation into leveraging egocentric human data for humanoid loco-manipulation, while verifying that our alignment pipeline successfully bridges human and robot data. The successful in-the-wild deployment demonstrates that scene generalization through human data is achievable, suggesting a scalable recipe for future pre-training: collect modest robot demonstrations per task in laboratories, then augment with large-scale human demonstrations across diverse scenarios. 

## **Q2.** _How will_ EGOHUMANOID _apply to other humanoid embodiments, besides the mid-sized humanoid robot, Unitree G1?_ 

Our pipeline addresses alignment between human demonstrations and humanoid action representations, _e.g._ , delta end-effector poses and discrete locomotion commands, which can be instantiated on any humanoid with appropriate inverse kinematics and locomotion controllers. The successful deployment on the mid-sized G1 (1.3m) validates our approach under challenging conditions with a substantial embodiment gap compared to human demonstrators (1.6–1.8m). Full-sized humanoids would exhibit smaller gaps, potentially making transfer more straightforward with minimal modifications. 

**Q3.** _Can this paradigm be extended to whole-body humanoid VLA with expressive motions, beyond the presented locomanipulation tasks?_ 

Our implementation builds upon GR00T-WholeBodyControl [45], which constrains lower-body motion to coarse commands for stability. Incorporating more expressive locomotion policies would extend our framework to tasks requiring precise leg movements, such as stepping on pedal-operated trash bins or navigating narrow gaps. The human demonstration pipeline already captures full-body motion, so the data infrastructure supports such extensions, and we envision this as a natural direction for future development. The primary challenge lies in developing robust low-level controllers for expressive whole-body motions while maintaining balance [40, 24, 73, 48]. 

**Q4.** _Why use the egocentric view only, without the commonly adopted wrist cameras? Why not inpaint human hands with robot grippers?_ 

We adopt a minimalist sensor configuration to establish a clean baseline for human-to-humanoid transfer. Wrist cameras would further amplify the embodiment gap through differing hand geometry and interaction patterns, warranting dedicated investigation [30]. Hand inpainting [34, 35, 33], while potentially reducing the visual domain gap, introduces errors from imperfect detection and rendering, and is embodiment-specific rather than agnostic. Our pipeline maintains generality through viewpoint transformation and action alignment without tremendous appearance modification. Wrist camera integration and inpainting remain promising future directions. 

## **Q5.** _Limitations and future endeavors._ 

Key limitations include: (1) delta end-effector poses create rotation ambiguity without proprioceptive input, limiting finegrained rotational control; (2) loco-manipulation requires more demonstrations than fixed-base tasks due to viewpoint variability from navigation; (3) discrete locomotion commands limit achievable behaviors. Future work will focus on scaling with advanced egocentric hardware, investigating pre-training with internet-scale egocentric video, and developing expressive action representations preserving cross-embodiment transferability. Besides, similar to general methods of learning from human data [72, 30], several practical human demonstration collection guidelines are necessary for efficient co-training, which are 

listed in Sec. B. Random human motion with occluded hands or high-speed motion changes would require more advanced sensor setups, such as tactile and SLAM techniques, to compensate for the estimation error. 

## **Q6.** _Broader impact._ 

On the technical side, our alignment between human and humanoid data establishes a form of cross-embodiment adaptation, suggesting humanoid-embodiment-agnostic learning is feasible. It hints at the potential for foundation models that learn from human demonstrations and deploy across diverse platforms with minimal adaptation, besides humanoid robots, mobile manipulators, and other non-anthropomorphic platforms. For societal impact, our work could motivate large-scale human data collection, which may accelerate innovation and broaden participation across institutions and regions. It can also democratize humanoid development for groups without expensive hardware, though it raises considerations around data privacy and contributor recognition as the paradigm scales. 

## _B. Practical Guidelines for Data Collection_ 

Due to the huge embodiment gap between humans and robots, several protocols are necessary for the demonstrators to follow to realize effective and efficient co-training, especially when we are experimenting with mid-sized humanoids. Though these guidelines may limit human motions to certain extents, they do not constrain the scenario diversity or affect collection efficiency, which are the main advantages of in-the-wild human data. 

**Hand-Wrist Pose Consistency.** Demonstrators should maintain consistent hand-wrist orientation patterns throughout task execution. Since our action representation uses delta end-effector poses, small wrist rotations can produce dramatically different action labels even for visually similar manipulation scenarios. Such inconsistencies introduce significant noise into the training data, as nearly identical visual observations become paired with conflicting action targets, ultimately degrading policy learning effectiveness. 

**Base Coordinate Stability.** Our pipeline computes locomotion commands using the human waist pose as the base coordinate frame. Consequently, demonstrators should maintain a relatively stable torso posture during movement. Excessive upper body swaying, which is common during natural human walking but absent in humanoid locomotion, can introduce systematic noise in velocity estimation, creating a mismatch between demonstrated and executable locomotion commands. 

**Hand Visibility Maintenance.** Reliable hand pose estimation requires minimizing occlusion during manipulation, particularly when ego-centric (head) cameras are used only without wrist cameras. When hands are obscured by manipulated objects or environmental elements, tracking quality degrades substantially, resulting in missing or inaccurate action labels. Demonstrators should adjust their approach angles and manipulation strategies to maintain clear hand visibility throughout task execution, even when this deviates from the most natural human behavior. 

## _C. Implementation Details_ 

## _1)_ EGOHUMANOID _:_ 

_a) View Alignment:_ We employ MoGe [58] at a resolution of 720 _×_ 1280 for depth prediction, followed by bilinear upsampling to match the input image resolution. A rigid camera transformation simulates downward movement from the human to robot viewpoint, with a translation distance of 0 _._ 25 m. During training, we apply data augmentation by adding uniform noise of _±_ 0 _._ 05 m to the translation distance. The resulting warped images with occlusions are inpainted using Stable Diffusion 2.0 Inpainting [51] with 20 denoising steps and classifier-free guidance scale of 7 _._ 5. 

_b) Action Alignment:_ The Savitzky–Golay filter for upper-body translation smoothing uses a window size of 11 and polynomial order 3. The same configuration is applied for rotation smoothing in the SO(3) tangent space and for lower-body pelvis trajectory smoothing. For lower-body command quantization, forward/backward velocity is discretized into 3 bins, lateral velocity into 3 bins, and yaw rate into 3 bins. The pelvis height change (delta <u>height) is computed as the inter-frame difference</u> of the downsampled z-coordinates, where the first frame is set to 0 and subsequent frames represent the change relative to the previous frame. 

## _2) Experiments:_ 

_a) Policy Architecture and Training:_ We finetune _π_ 0 _._ 5 [26] with the following configuration. The input RGB image is resized to 224 _×_ 224. The output action space is 18-dimensional, consisting of 12-DoF delta end-effector pose (6-DoF _×_ 2 arms), 3-dimensional discrete locomotion commands (navigation in x, y, and yaw), 2-dimensional binary gripper commands (one per hand), and 1-dimensional delta height command. The action chunk size is 50 steps. 

Training is conducted on 8 _×_ NVIDIA A100 GPUs with a per-GPU batch size of 32, yielding an effective batch size of 256. We use the AdamW optimizer with a learning rate of 5 _×_ 10<sup>_−_5</sup> , weight decay of 1 _×_ 10<sup>_−_10</sup> (effectively negligible), gradient clipping norm of 1.0, and a cosine decay learning rate schedule with 10,000 warmup steps. Training runs for 20,000 steps. We use mixed-precision (bfloat16) training throughout. No proprioceptive inputs are used for either data source. 

_b) Robot Platform:_ The ZED X Mini camera is mounted on the robot head and captures egocentric RGB images at 20 Hz with a resolution of 960 _×_ 540, which are later downsampled to 224 _×_ 224 for model input. The low-level wholebody controller [45] converts high-level delta end-effector commands to joint-level motor targets. Robot demonstration data is collected at 100 Hz and downsampled to 20 Hz (factor of 5) for training, with Savitzky-Golay filtering applied to smooth end-effector trajectories. 

_c) Policy Inference:_ The policy generates 50-step action chunks at each inference. The inference client runs on RTX 4090, with each forward pass taking approximately 130 ms. We employ a temporal smoothing mechanism based on linear blending of action chunks. When a new chunk arrives, we drop the first _k_ actions that has been executed during inference for latency compensation, then linearly blend the overlapping region with the remaining actions from the previous chunk using weights _w_ old( _i_ ) = 1 _− i/_ ( _m −_ 1) and _w_ new( _i_ ) = _i/_ ( _m −_ 1) for _i ∈_ [0 _, m_ ), where _m_ is the overlap length. This ensures smooth transitions between chunks while maintaining responsiveness. 

## _D. Scoring Criteria for Real-world Experiments_ 

In this section, we introduce four real-world loco–manipulation tasks and the criteria for determining success or failure. Each task is decomposed into an ordered sequence of stages _{Sk}_ , where each stage is labeled as either locomotion-dominant or manipulation-dominant. A trial is considered **successful** only if **all** stages succeed in order; otherwise, it is a **failure** . We evaluate each task in both in-domain and generalized environments. We additionally record **stage-wise success/failure** to enable fine-grained analysis. 

For consistency with Figs. 5, 7, 8 in the main paper, we also report an _Average Score_ for each task, defined as the average stage completion rate. Specifically, for a task with _K_ ordered stages, each stage is assigned a binary indicator _sk ∈{_ 0 _,_ 1 _}_ , where _sk_ = 1 if stage _Sk_ succeeds and _sk_ = 0 otherwise. The per-trial task score is defined as 


The _Average Score_ reported in Figs. 5, 7, 8 is obtained by averaging Score over trials, which is equivalent to the mean of the per-stage success rates within the task. 

- **Pillow Placement.** 

_Task description:_ the robot starts while grasping a pillow and facing a bed. It must keep holding the pillow, walk to the bed, squat to an appropriate height, and place the pillow onto the target area near the head of the bed. This task is naturally split into a locomotion stage (carrying without dropping) and a placement stage. 

_Experimental setup:_ the in-domain environment is a laboratory setting, where the bed is a portable camp bed. In the generalized environment, we recreate a home-like bedroom scene with a standard household bed and consistent background furniture and decor, matching everyday living conditions. 

_Stage-wise success/failure:_ 

## **– S1 (Locomotion).** 

- _∗_ **Success:** the robot reaches a position in front of the bed suitable for subsequent placement _while continuously holding_ the pillow (no drop, no unintended release). 

- _∗_ **Failure:** the pillow is dropped/released or the robot stops in a pose/location that makes the next stage infeasible ( _e.g._ , too far to reach the target placement region). 

## **– S2 (Manipulation).** 

   - _∗_ **Success:** after squatting, the robot places the pillow onto the designated head-area region of the bed. 

   - _∗_ **Failure:** the pillow is placed outside the target region, slips/falls off the bed, is released prematurely, or the robot cannot complete the squat-and-place motion. 

- **Trash Disposal.** 

_Task description:_ the robot starts while grasping a piece of trash and facing a waste container. It must keep holding the trash, walk to the container, and dispose the trash into the container opening. 

_Experimental setup:_ in-domain trials are conducted in the laboratory. For generalized trials, we relocate the waste container to an outdoor garden setting and evaluate the same disposal procedure under the resulting scene and background changes. _Stage-wise success/failure:_ 

## **– S1 (Locomotion).** 

- _∗_ **Success:** the robot approaches the waste container to a feasible disposal pose while maintaining a stable grasp on the trash. 

- _∗_ **Failure:** the trash is dropped/released, the robot falls/becomes unstable, or the final approach pose is not suitable for the disposal motion. 

## **– S2 (Manipulation).** 

   - _∗_ **Success:** the trash ends up inside the waste container after the disposal attempt (successful insertion through the opening) and does not remain outside or get stuck at the rim as an external object. 

   - _∗_ **Failure:** the trash misses the opening, stays outside the container, gets stuck externally at the rim region, or the robot cannot execute the disposal motion stably. 

- **Toy Transfer.** 

_Task description:_ a toy is placed on a small elevated stand in front of the robot, and a table is located at a distance. The robot must walk to the stand, grasp the toy with both hands, turn and walk to the table while holding the toy, and finally place the toy onto the table. 

_Experimental setup:_ in-domain trials are conducted in the laboratory. For generalized trials, we replace the lab desk with household counterparts—using a secretaire as the table and a home cabinet as the stand—and evaluate the task in a home-like setting with consistent background furniture and decor. 

_Stage-wise success/failure:_ 

## **– S1 (Locomotion).** 

   - _∗_ **Success:** the robot reaches a pose where the toy is reachable for a two-hand grasp attempt. 

   - _∗_ **Failure:** the robot stops too far / in a poor pose that makes grasping infeasible. 

- **S2 (Manipulation).** 

   - _∗_ **Success:** the robot lifts and secures the toy with both hands, and the toy remains firmly held (no drop) at the end of the grasp stage. 

   - _∗_ **Failure:** failure to establish a stable grasp, dropping the toy during/after lift, or grasping in a way that prevents carrying to the next stage. 

## **– S3 (Locomotion).** 

   - _∗_ **Success:** the robot turns and walks to the table while constantly holding the toy, ending at a pose suitable for placement. 

   - _∗_ **Failure:** dropping/releasing the toy or arriving at an infeasible placement pose. 

- **S4 (Manipulation).** 

   - _∗_ **Success:** the robot places the toy onto the table surface and the toy remains stably on the table after release. 

   - _∗_ **Failure:** the toy is dropped off the table, placed unstably (immediately falls), or the robot cannot complete the placement. 

- **Cart Stowing.** 

_Task description:_ a toy is placed on a table, and a cart is located nearby. The robot must first hold the cart handle and move the cart to a position beside the table such that the toy becomes reachable by the left hand; then it releases the handle, grasps the toy with the left hand, moves the toy over the cart basket and releases it into the cart; finally it pushes the cart forward. This task includes sustained cart contact during locomotion and multi-phase manipulation. 

_Experimental setup:_ in-domain trials are conducted in the laboratory. For generalized trials, we replace the table with a retail-style shelf and place the toy on the shelf to better match a shopping scenario. The generalized evaluation is performed in a real convenience store with natural background clutter and layout. 

_Stage-wise success/failure:_ 

## **– S1 (Locomotion).** 

- _∗_ **Success:** the robot maintains a stable grasp on the cart handle and pushes/moves the cart to a position where the toy on the table is reachable by the left hand. 

- _∗_ **Failure:** stopping in a pose that makes toy grasping infeasible. 

## **– S2 (Manipulation).** 

- _∗_ **Success:** the robot releases the handle and establishes a stable left-hand grasp on the toy. 

- _∗_ **Failure:** failed grasp, dropping the toy, or grasping in a way that prevents transporting it over the cart. 

## **– S3 (Manipulation).** 

- _∗_ **Success:** while holding the toy, the robot moves the left hand above the cart basket and releases the toy such that it lands inside the cart. 

- _∗_ **Failure:** the toy lands outside the cart, gets stuck on the rim/edge externally, is dropped prematurely, or the robot cannot execute the transfer motion stably. 

## **– S4 (Locomotion).** 

- _∗_ **Success:** the robot pushes/moves the cart forward in a controlled and stable manner after the toy has been stowed. 

- _∗_ **Failure:** unstable pushing leading to loss of control or fall, or requiring human intervention. 


Fig. 9: **Qualitative results of the view alignment pipeline.** For each task, we show the original human egocentric image, the MoGe-estimated depth map, the reprojected image after point cloud transformation to the robot camera frame, and the final inpainted result. The pipeline produces a consistent downward viewpoint shift that approximates the robot’s lower camera height, with inpainting filling disoccluded regions to yield complete RGB observations. 

## _E. Qualitative Results on Human-to-Humanoid Alignment_ 

Fig. 9 visualizes the view alignment pipeline across all four tasks. For each example, we show the original human egocentric image, the estimated depth map from MoGe [58], the reprojected image after point cloud transformation to the robot camera frame, and the final image after diffusion-based inpainting. The reprojected images exhibit a noticeable downward viewpoint shift consistent with the lower robot camera height, introducing black regions from disocclusions and invalid depth predictions. The inpainting step faithfully fills these missing regions while preserving scene structure and object appearance, producing complete RGB images that closely approximate what the robot would observe from its egocentric viewpoint. Notably, the pipeline handles diverse scenes including indoor bedrooms, outdoor gardens, cluttered tabletops, and retail environments, demonstrating its generality across the tasks and scenarios used in our experiments. 

## _F. License of Assets_ 

This work builds upon several open-source projects with permissive licenses. Our implementation incorporates PICO XRoboToolkit [79], MoGe [58], and latent diffusion [51], all released under the MIT License. The MoGe codebase additionally includes components from DINOv2 [47], which are released by Meta AI under the Apache 2.0 License. We also make use of openpi [26], which is distributed under the Apache 2.0 License. Finally, our system integrates GR00T-WholeBodyControl [45], which is released under the NVIDIA non-commercial license. We will open-source our assets, including code and models, under the Apache 2.0 License. 

