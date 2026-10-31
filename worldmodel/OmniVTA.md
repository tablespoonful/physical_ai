---
title: "OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation"
date: "2026-03-19"
authors: "Yuhang Zheng; Songen Gu; Yupeng Zheng; Weize Li; Yujie Zang; Shuai Tian"
url: https://arxiv.org/abs/2603.19201
pdf: https://arxiv.org/pdf/2603.19201
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.19201)** / [論文ページ](https://arxiv.org/abs/2603.19201)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# OmniVTA: Visuo-Tactile World Modeling for Contact-Rich Robotic Manipulation 

Yuhang Zheng<sup>1</sup><sup>_∗_</sup> , Songen Gu<sup>3</sup><sup>_∗_</sup> , Yupeng Zheng<sup>2</sup><sup>_†_</sup> , Weize Li<sup>1</sup> , Yujie Zang<sup>1</sup> , Shuai Tian<sup>2</sup> , Xiang Li<sup>4</sup><sup>_,_5</sup> , Ce Hao<sup>6</sup> , Chen Gao<sup>1</sup><sup>_,_7</sup> , Si Liu<sup>7</sup> , Haoran Li<sup>2</sup> , Yilun Chen<sup>4</sup> , Shuicheng Yan<sup>1</sup><sup>_†_</sup> , Wenchao Ding<sup>4</sup><sup>_†_</sup> 

- 1National University of Singapore, 2CASIA, 3Fudan University, 4TARS Robotics, 

   - 5Tsinghua University, 6Zhongguancun Academy, 7Beihang University 

      - Corresponding Author, * Equal Contribution 


Fig. 1: **Overview of the proposed visuo-tactile manipulation system.** (Left) We introduce OmniViTac, a large-scale visuotactile-action aligned dataset for contact-rich manipulation. (Center) We propose OmniVTA, a world model-based visuo-tactileaction framework that predicts future contact states. It seamlessly unifies tactile representation learning, predictive multimodal modeling, adaptive fusion, and reflexive tactile control. (Right) Extensive real-world experiments demonstrate that OmniVTA outperforms prior methods, exhibiting strong robustness and generalization. 

**_Abstract_ —Contact-rich manipulation tasks, such as wiping and assembly, require accurate perception of contact forces, friction changes, and state transitions that cannot be reliably inferred from vision alone. Despite growing interest in visuotactile manipulation, progress is constrained by two persistent limitations: existing datasets are small in scale and narrow in task coverage, and current methods treat tactile signals as passive observations rather than using them to model contact dynamics or enable closed-loop control explicitly. In this paper, we present OmniViTac, a large-scale visuo-tactile-action dataset comprising** 21 _,_ 000+ **trajectories across** 86 **tasks and** 100+ **objects, organized into six physics-grounded interaction patterns. Building on this dataset, we propose OmniVTA, a world-model-based visuo-tactile manipulation framework that integrates four tightly coupled modules: a self-supervised tactile encoder, a two-stream visuo-tactile world model for predicting short-horizon contact evolution, a contact-aware fusion policy for action generation, and a 60Hz reflexive controller that corrects deviations between predicted and observed tactile signals in a closed loop. Realrobot experiments across all six interaction categories show that OmniVTA outperforms existing methods and generalizes well to unseen objects and geometric configurations, confirming the value of combining predictive contact modeling with high-** 

**frequency tactile feedback for contact-rich manipulation. To advance research in visuo-tactile manipulation, all data, models, and code will be made publicly available to the community.** 

**_Index Terms_ —Visuo-Tactile Manipulation, Visuo-Tactile World Models, Contact-Rich Manipulation** 

## I. INTRODUCTION 

Contact-rich manipulation tasks, such as wiping and assembly, are ubiquitous in daily human activities. Their successful execution requires not only precise geometric alignment, but also accurate perception and fine-grained control of contact forces, frictional changes, and subtle transitions in contact state [1], [2], [3]. Since such information is difficult to infer reliably from vision alone, recent studies [4], [5], [6] have incorporated tactile sensing into imitation learning frameworks to improve visuomotor policies for contact-rich manipulation. 

However, despite the growing adoption of tactile sensing in contact-rich manipulation, the broader visuo-tactile manipulation community still faces substantial limitations in both data 

2 

and methodology. (1) On the data side, existing public visuotactile manipulation datasets [4], [7], [8] remain limited in both the scale of fully aligned vision-tactile-action demonstrations and the diversity of contact-rich tasks. In particular, the amount of synchronized visual and high-frequency tactile data is still insufficient for learning generalizable visuo-tactile representations and modeling contact dynamics. In addition, the covered scenarios, tasks, and interaction patterns are narrow, making it difficult to capture the broad spectrum of contact mechanisms required in real-world manipulation. (2) On the methodology side, existing visuo-tactile manipulation approaches remain limited in both representation and control. In most prior works [9], [10], tactile signals are incorporated merely as auxiliary observations to the policy network, primarily for contactstate recognition or compensating for visual occlusion, rather than being used to model the evolution of contact dynamics explicitly. At the control level, these methods typically rely on action chunking to generate short action sequences that are then executed in an open-loop manner. Such a design makes it difficult to react promptly to rapid contact changes, including slippage, misalignment, and external disturbances, which are pervasive in contact-rich manipulation. 

In contrast, humans perform such tasks with remarkable dexterity and robustness. Neuroscience studies [11], [12], [13], [14] suggest that this ability relies on tightly coupled multimodal perception, predictive internal models, and rapid tactile feedback control. This combination of predictive modeling and reflexive correction is still largely missing from current visuotactile policies. 

In this paper, we address these limitations from both the data and methodology perspectives. Concretely, we introduce OmniViTac, a large-scale visuo-tactile-action aligned dataset. Building on this dataset, we further propose OmniVTA, a world-model-based visuo-tactile manipulation framework. 

Specifically, OmniViTac is a large-scale visuo-tactile-action aligned dataset for contact-rich manipulation, comprising 21 _,_ 879 trajectories spanning 86 tasks and 100+ manipulated objects in diverse real-world scenarios. To capture the broad spectrum of contact-rich behaviors encountered in manipulation, we organize the dataset into six physics-grounded visuotactile interaction patterns: wiping, peeling, cutting, grasping, assembly, and in-hand adjustment. To ensure data fidelity, OmniViTac is collected using a unified cross-embodiment platform and processed through a rigorous pipeline that preserves native sensor frequencies, performs precise temporal synchronization across vision, touch, and action streams, and incorporates automated trimming together with human-in-theloop verification. Beyond scale and data quality, our analysis further shows that OmniViTac captures structured, patternspecific contact dynamics and reveals two key properties of tactile signals in manipulation, namely spatial locality and contact-driven dynamics. These properties make OmniViTac a strong benchmark for learning visuo-tactile representations, predictive contact models, and robust manipulation policies. 

Inspired by human sensorimotor control in contact-rich manipulation, an effective robotic system should possess two key capabilities [12]: (1) forming feedforward anticipations of contact evolution through predictive modeling, and (2) exploit- 

ing tactile feedback for high-frequency closed-loop correction. 

To this end, we propose OmniVTA, a world-model-based visuo-tactile manipulation framework composed of four tightly coupled modules. First, TactileVAE learns compact, lowdimensional tactile representations through spatio-temporal encoding and reconstructs continuous tactile deformation fields with an implicit neural decoder, providing structured tactile features for downstream prediction and policy learning. Second, the Visuo-Tactile World Model adopts a two-stream conditional generative architecture to model the temporal evolution of visual observations and tactile signals, thereby forming short-horizon feedforward predictions of contact dynamics. Third, the Adaptive Visuo-Tactile Fusion Policy leverages a Latent Tactile Differential (LTD) Encoder to capture the relationship between current tactile observations and predicted future tactile features, and adaptively fuses visual and tactile information through a contact-aware gating mechanism for action generation. Finally, the Reflexive Latent Tactile Controller uses predicted and observed tactile features to produce finegrained corrective actions at 60,Hz, enabling rapid closed-loop correction during manipulation. 

Extensive real-robot experiments across six tactile interaction pattern categories validate the effectiveness of OmniVTA from three perspectives. First, OmniVTA achieves state-of-theart performance on diverse contact-rich manipulation tasks, with strong advantages in object diversity, geometric generalization, and disturbance robustness. The full framework further outperforms its open-loop variant, highlighting the importance of high-frequency tactile feedback for stable contact control. Second, mechanistic analyses show that the policy adaptively reweights vision and touch according to the predicted contact state, and that accurate tactile prediction is crucial for reliable action generation. Third, OmniVTA maintains stable performance under unseen geometric configurations and unseen tools, suggesting that it learns transferable contact-relevant structure and dynamics rather than memorizing task-specific trajectories. Together, these results demonstrate the benefit of predictive visuo-tactile world modeling combined with rapid tactile-feedback-based correction. 

The main contributions of this paper are three-fold: (1) We present OmniViTac, a large-scale visuo-tactile-action aligned dataset for contact-rich manipulation spanning six tactile interaction pattern categories, and reveal two key properties of tactile signals: spatial locality and contact-driven dynamics. (2) We propose OmniVTA, a world-model-based visuo-tactile manipulation framework that integrates tactile representation learning, predictive visuo-tactile world modeling, contactaware fusion, and high-frequency closed-loop tactile control. (3) Extensive real-world experiments show that OmniVTA outperforms state-of-the-art baselines across diverse contact-rich manipulation tasks, with strong robustness to perturbations and effective generalization to novel configurations and objects. 

## II. RELATED WORKS 

## _A. Tactile Sensing and Tactile Representation Learning_ 

Robotic fine-grained interaction relies on advances in both tactile hardware and representation learning. Existing tactile 

3 


Fig. 2: **Overview of OmniViTac dataset. Left:** The Cross-Embodiment Data Collection Platform features UNFactory 7- DoF xArm and the TacUMI manipulation interface, both supporting identical end-effectors and diverse tactile sensors (Xense, GelSight Mini, Tac3D, Daimon). **Middle:** The dataset covers 6 visuo-tactile manipulation patterns, instantiated across 5 semantic scenarios. **Top-Right:** A scale comparison demonstrates that OmniViTac (21,879 trajectories) significantly exceeds existing visuo-tactile manipulation datasets in tactile-rich data volume. **Bottom-Right:** The High-quality Data Pipeline ensures reliability through timestamp alignment, visualization, and human-in-the-loop verification. 

sensors span multiple physical principles, including capacitive arrays [15], [16], piezoresistive sensors [17], [18], and magnetic sensors [19]. Among them, visuo-tactile sensors such as GelSight [20] and DIGIT [21] have attracted particular attention because they provide high-resolution and robust measurements. By tracking gel deformation with a camera, they reconstruct fine contact geometry and, with marker dots, estimate force and torque. 

With such signals available, the focus has shifted from taskspecific features to transferable tactile representations. A major line of work learns from paired vision-tactile data through self-supervision or contrastive learning. Sparsh [22] adopts a masked autoencoder, Anytouch [23] uses contrastive learning, and UniT [24] introduces a VQGAN-like architecture [25] for compact latent modeling. More recently, tactile sensing has been integrated into MLLMs to align tactile, visual, and textual representations. Representative examples include Binding touch to everything [26], Octopi [27], and VTV-LLM [28]. Octopi-1.5 [7] further adds retrieval augmentation to improve predictions for unseen object-tactile pairs. Our study builds on this trend by examining unified visuo-tactile representation learning across four visuo-tactile sensors: GelSight Mini [20], Tac3D [29], Xense [30], and Daimon [31]. 

## _B. Visuo-Tactile Robotic Manipulation Policies_ 

Findings from human motor control highlight the importance of tactile feedback for stable manipulation. Prior studies show that cutaneous feedback is essential for maintaining grip stability [14] and that the brain uses a unified internal model to predict tactile feedback for both limbs and tools [13], [12]. 

These results suggest that tactile sensing is fundamental to contact-rich manipulation, where it complements vision under occlusion and provides direct force-related feedback. 

Inspired by these insights, robotic manipulation policies increasingly incorporate non-visual inputs. Early visuo-tactile systems such as See-to-Touch [32] and RoboPack [33] showed that local tactile observations can resolve ambiguities and support fine-grained control when vision is unreliable. Recent work extends this idea to end-to-end manipulation models, including vision-action models such as 3D-ViTac [9] and RDP [5], as well as vision-language-action models such as VLA-Touch [4], Tactile-VLA [34], and TA-VLA [35]. However, effectively fusing tactile and visual signals for highfrequency closed-loop control remains difficult. Existing methods often suffer from weak tactile integration or temporal mismatch. Beyond direct policy learning, recent generative visuotactile modeling approaches predict interaction outcomes: VTWM [36] learns action-conditioned visuo-tactile latent dynamics for model-based planning, whereas FlowTouch [37] generates view-invariant static tactile observations from local 3D geometry. Different from these standalone generative or predictive models, our framework adopts a predictive–reactive slow–fast design, in which predicted future tactile latents support adaptive multimodal fusion and slow action generation, while real-time tactile feedback drives high-frequency residual correction for robust contact-rich manipulation. 

## _C. Visuo-tactile Manipulation Datasets and Systems_ 

Early visuo-tactile datasets [26], [38], [27], [23], [28], [7] mainly collected static paired observations by pressing 

4 

handheld tactile sensors against objects, surfaces, or textures. Although useful for multimodal representation learning, they do not provide action trajectories for manipulation. More recent datasets [39], [40], [41], [4], [42], [43], [44] mount tactile sensors on robotic grippers and record manipulation through UMI [45], teleoperation, or kinesthetic teaching. These systems capture synchronized vision, touch, and proprioception, enabling visuo-tactile policy learning for contact-rich tasks. Nevertheless, current datasets remain limited in scale, sensor and platform diversity, and temporal alignment between highfrequency tactile streams and visual observations. 

Our work addresses these limitations with a multi-platform visuo-tactile manipulation dataset that offers diverse tasks and fully aligned vision, touch, and action sequences, supporting large-scale world-model training for unified visuo-tactile policy learning. 

## III. THE OMNIVITAC DATASET 

To support data-driven visuo-tactile learning for contact-rich manipulation, we introduce OmniViTac, a large-scale visuotactile-action dataset that addresses two key limitations of existing datasets: insufficient scale of fully aligned demonstrations and limited coverage of contact-rich tasks. 

OmniViTac contains 21 _,_ 879 synchronized trajectories spanning 86 tasks and 100+ objects in diverse real-world environments, with RGB-D observations, high-frequency tactile sensing, and action streams recorded in a temporally aligned manner. Compared with prior visuo-tactile-action datasets in Tab. I, OmniViTac substantially expands both task coverage and data scale, while also increasing sensor and collection diversity. Beyond scale alone, OmniViTac is organized around six physics-grounded visuo-tactile interaction patterns, enabling the dataset to capture a broad spectrum of contact dynamics rather than a narrow set of task-specific behaviors. These properties make OmniViTac a comprehensive benchmark for learning generalizable visuo-tactile representations, predictive contact models, and manipulation policies. 

In the following, we describe OmniViTac in terms of its system design, task organization, and dataset scale. Sec. III-A presents the hardware setup and synchronized data collection pipeline, which enables temporally aligned acquisition of RGB-D observations, tactile signals, and actions under diverse embodiments and sensing configurations. Sec. III-B introduces the task taxonomy and representative visuo-tactile interaction patterns, revealing the contact-rich structure underlying the dataset. Sec. III-C summarizes the dataset statistics and comparisons with prior work, highlighting the scale, diversity, and breadth of OmniViTac. 

## _A. Hardware Setup and Data Collection System_ 

_1) System Overview:_ To efficiently collect large-scale visuo-tactile manipulation data, we develop a unified multimodal data acquisition system that can be operated by a single human operator. The system records synchronized multimodal observations during manipulation, including RGB-D visual observations, tactile signals from fingertip sensors, manipulation trajectories, and continuous gripper aperture states. 

All sensory streams are recorded asynchronously at their native frequencies. A post-processing synchronization pipeline then aligns different modalities using timestamps to ensure consistent temporal correspondence across all observations. 

_2) Dual-Embodiment Data Collection:_ To balance _robotaligned demonstrations_ and _data collection scalability_ , our dataset is collected using two complementary hardware embodiments: a 7-DoF robotic manipulator (xArm-7) and a TacUMI handheld data collection device. The robotic platform captures demonstrations that closely match the kinematic and dynamic distributions of robot execution, while TacUMI enables flexible and efficient human manipulation for largescale data collection. 

**Robot Demonstrations (7DoF Robot Arm).** We employ a UFACTORY xArm-7 manipulator to collect robot-aligned demonstrations. Two control modes are used: 

- **Kinesthetic Teaching.** The operator directly guides the robot under gravity compensation mode, allowing precise control of contact interactions. This mode is particularly suitable for tasks requiring fine force perception, such as wiping surfaces or inserting connectors. 

- **GELLO Teleoperation.** For tasks involving larger spatial motions and less reliance on direct force perception, we adopt the GELLO teleoperation system [46]. This master–follower interface enables efficient collection of pickand-place style demonstrations while preserving realistic robot motion trajectories. 

**Human Demonstrations (TacUMI).** To improve data collection efficiency and flexibility, we develop TacUMI, a handheld visuo-tactile data collection device inspired by FastUMI [49]. TacUMI enables natural manipulation motions while recording multimodal sensory observations that are consistent with the robotic platform. Following FastUMI, we use a RealSense T265 tracking camera, which outputs 6-DoF poses at 200 Hz to estimate trajectories. After each trajectory is collected, an automatic verification step checks for tracking drift, and trajectories with position errors larger than 8 mm are discarded. **Isomorphic End-Effector.** To minimize embodiment-induced domain gaps, both the robotic arm and TacUMI employ identical parallel-jaw grippers. This shared end-effector design ensures consistent grasp geometry and contact mechanics across both data collection embodiments. Each gripper records _continuous motor states_ , which are normalized to a [0 _,_ 1] range to represent the gripper width. The fingertip structure is modular and supports interchangeable tactile sensor modules. 

_3) Sensor Suite:_ To capture the diverse perceptual cues required in contact-rich manipulation, we combine RGB-D sensing with multiple tactile sensors that provide complementary observations of object geometry, surface interaction, and contact dynamics. 

**Visual Observation.** We record both _wrist-view_ and _thirdperson-view_ RGB-D observations. Wrist-view images are captured using an Intel RealSense D435 camera, while thirdperson observations are captured using either a D435 or an L515 camera. All cameras record RGB-D streams at 30 Hz. The D435 provides images at 640 _×_ 480 resolution, while the L515 provides 1280 _×_ 720 resolution. TacUMI additionally 

5 


Fig. 3: **Example visualization of the** 6 **visuo-tactile manipulation patterns in OmniViTac.** The dataset captures diverse, contact-rich behaviors across various scenarios, including Assembly, Cutting, Adjustment, Peeling, Grasping, and Wiping. Each panel illustrates the global third-person workspace view overlaid with the end-effector’s trajectory, alongside synchronized, highfrequency tactile maps (bottom) that continuously record the complex tool-object contact dynamics during task execution. 

TABLE I: **Comparison of OmniViTac with existing vision-tactile-action datasets.** _Note:_ * indicates that the statistics count only the visuo-tactile trajectories in the corresponding dataset. “–” denotes not applicable. 

|**Dataset**|**#Task**|**#Traj.**|**#Object**|**Vision**|**Tactile**|||**Action**|**Collection**|
|---|---|---|---|---|---|---|---|---|---|
||||||**Sensors**|**Force Dim.**|**Frequency**|||
|ObjectFolder2.0 [47]|3|–|1,000|Rendered|GelSight|3|–|✗|Simulated|
|AnyTouch [23]|1|–|124|–|GelSight Mini/DIGIT/DuraGel/Tac3D|3|30|✗|Handheld|
|VTV150k [28]|–|–|100|–|GelSight Mini/DIGIT/Tac3D|–|–|✗|Handheld|
|Octopi-1.5 [7]|3|–|–|GoPro|GelSight Mini/TAC-02|–|50_∼_1000|✓|TMI|
|See, Hear, and Feel [39]|2|60|4|RealSense|GelSight|–|30|✓|Teleop|
|RH20T* [40]|55|917|–|RealSense|uSkin|–|200|✓|Teleop|
|FreeTacMan [41]|50|10,000|50|Fisheye|FreeTacMan|–|30|✓|Fingertips|
|VLA-Touch [4]|3|–|–|RealSense|GelSight Mini|–|10|✓|Kinesthetic Teaching|
|OmniVTLA [42]|2|240|56|RealSense|GelSight/Paxini Gen 2|–|30|✗|Handheld|
|exUMI [43]|9|1,665|8|GoPro|9DTact|6|–|✓|UMI-style|
|MLA [44]|6|1,200|14|RealSense|Tashan TS-E-A|6|–|✗|Gello-teleop|
|Hoi! [48]|6|_∼_3,000|381|Zed Mini/Aria|DIGIT|6|30_∼_60|✓|Gello-teleop|
|AgiBot World* [8]|7|5,337|–|–|Xense|3|–|✓|Teleop|
|**OmniViTac (Ours)**|86|21,879|126|RealSense/Fisheye|Xense/Gelsight Mini/DM-Tac/Tac3D|3|30_∼_60|✓|UMI-style/Kinesthetic Teaching|


integrates a wide-angle RGB camera to capture broader environmental context. 

**Tactile Sensing.** Tactile sensors are mounted on the gripper fingertips to capture detailed contact information during manipulation. Our platform supports four types of tactile sensors with different sensing principles and resolutions: 

- **Xense (Quark N1):** records RGB tactile images with a resolution of 700 _×_ 400 at 30 Hz and 3D displacement fields with a spatial resolution of 35 _×_ 20 at 60 Hz. 

- **Daimon (Tac-WL):** records grayscale tactile images at 640 _×_ 480 resolution at 30 Hz and 3D displacement measurements with resolution 320 _×_ 240 at 60 Hz. 

- **Tac3D-A1:** provides dense 3D displacement sensing with spatial resolution 20 _×_ 20 at 30 Hz. 

- **GelSight Mini:** records RGB tactile images with resolution 320 _×_ 240 and 3D displacement fields with spatial resolution 9 _×_ 7, both captured at 25 Hz. 

These sensors provide multiple tactile signal modalities for 

the same manipulation tasks. The Xense sensor is used for the majority of data collection due to its robustness in large-scale manipulation datasets. Consequently, demonstrations collected with Xense are primarily used for analysis and real-robot evaluation, while the additional tactile sensors are included to support research on tactile representation learning and crosssensor generalization. 

**Proprioceptive Signals.** The system also records proprioceptive states, including robot joint states (only for xArm demonstrations), end-effector poses, and continuous gripper aperture values. During data collection, the average tactile displacement is visualized in real time to provide operators with an intuitive estimate of contact forces. 

_4) Data Collection and Processing Pipeline:_ We describe how visuo-tactile-action trajectories are recorded and how the raw data are collected, validated, and processed. **Data Acquisition.** To enable single-operator data collection, we design a foot-pedal control interface for managing the entire recording process. The interface provides three functions: 

6 

starting the system, recording trajectories, and stopping it. During recording, all sensors continuously publish timestamped observations, which are subscribed and stored by the host computer. To prevent sensor drift from extended operation, the system automatically restarts after every 25 trajectories. **Data Validation.** We perform both online and offline quality checks. During collection, every 50 trajectories the system randomly selects three trajectories and visualizes synchronized sensor streams, including camera observations, tactile signals, trajectory curves, and gripper width signals. After data collection, all trajectories can be inspected offline using visualization tools, and abnormal samples are removed. 

**Data Processing.** Before policy training, we preprocess all trajectories to improve data quality and temporal consistency. This pipeline removes redundant static frames at the beginning and end of each trajectory, aligns RGB-D, tactile, and action streams through timestamp synchronization (with temporal error below 10 ms), and segments trajectories into training-ready clips according to downstream policy learning requirements. 

## _B. Task Taxonomy and Tactile Pattern Analysis_ 

_1) Environmental Diversity:_ To facilitate robust generalization of visuo-tactile policies to real-world environments, OmniViTac is deliberately designed with high environmental diversity. As illustrated in the inner ring of Fig. 2 and the examples in Fig. 3, the dataset encompasses over 70 distinct manipulation tasks, systematically distributed across five semantic scenarios: _Kitchen, Fruit Shop, Industrial Workspace, Chemistry Laboratory,_ and _Office_ . Diverse scene selection ensures broad coverage of visual distractors, varying illumination conditions, and a wide range of object properties, including rigid, deformable, transparent, and articulated types, thereby posing fundamental challenges to the robustness of policies. 

_2) Task Taxonomy:_ To move beyond task classification based purely on visual kinematics, we introduce a physicsgrounded taxonomy that categorizes the collected behaviors into six representative visuo-tactile patterns. This taxonomy is defined by the dominant tactile features and contact mechanics underlying successful execution: 

- **Assembly:** Involves precise coordination of contact geometry and multi-directional forces to perceive tight tolerances and detect successful mating of intricate parts. 

- **Cutting:** Predominantly relies on the progressive magnitude of normal forces to penetrate objects, using sudden force drops to judge the completion of the severing action. 

- **Adjustment:** Characterized by torsional and shear forces, which are crucial for sensing slip and reorienting in-hand objects until the desired stable pose is achieved. 

- **Peeling:** Involves a dynamic and continuous coupling of both shear and normal forces to maintain constant toolsurface contact while stripping object exteriors. 

- **Wiping:** Another canonical contact-rich task demanding the simultaneous regulation of normal pressure (to maintain surface adherence) and planar shear force (to overcome friction during sweeping motions). 

- **Grasping:** A highly versatile category encompassing a broad spectrum of force profiles. It utilizes precise normal 

force control to safely handle fragile items, leverages contact feedback to verify secure holds on visually challenging (e.g., transparent) objects, and exploits combined normal-shear dynamics to optimize the manipulation of complex articulated mechanisms. 

_3) Tactile Pattern Analysis:_ To quantitatively validate the proposed task taxonomy and analyze the underlying data distribution, we embed the high-dimensional tactile signals from all six pattern categories into a two-dimensional latent space using t-SNE, as shown in Fig. 4(f). The embedding reveals a highly structured and physically interpretable distribution. Notably, tasks dominated by continuous, high-frequency shear and dynamic normal forces, such as _Wiping_ and _Peeling_ , form overlapping or closely adjacent clusters, reflecting their shared underlying contact mechanics. In contrast, tasks governed primarily by static normal pressure and localized geometric contacts, such as _Assembly_ , yield distinct and well-separated manifolds. The _Grasping_ category occupies a broad and expansive region in the feature space, consistent with its inherent intra-class diversity spanning delicate handling of fragile objects to manipulation of complex articulated mechanisms. This clear semantic separability within the tactile latent space underscores that OmniViTac captures rich, pattern-specific contact dynamics rather than redundant or noisy signals. 

## _C. Dataset Statistics and Scale_ 

_1) Overview Statistics:_ To rigorously benchmark the scale, diversity, and fidelity of OmniViTac, we provide a comprehensive statistical analysis of all collected trajectories, with an emphasis on task distributions and their associated spatiotemporal tactile properties. As illustrated in Fig. 4(e), the dataset captures a broad range of visuo-tactile patterns commonly encountered in daily manipulation tasks. The “grasping” category constitutes the largest subset, comprising 9,200 trajectories. Other manipulation categories also account for a significant portion of the dataset, each comprising approximately 3,000 or 1,000 trajectories, with all categories remaining within the same order of magnitude. This balanced composition ensures sufficient data density for both generalpurpose pre-training and task-specific fine-tuning. 

_2) Tactile Active Ratio:_ A key metric for evaluating contact-rich datasets is the Effective Contact Ratio, defined as the proportion of a trajectory during which the tactile sensors register meaningful tactile interaction. As shown in Fig. 4(d), _Adjustment_ exhibits the highest active ratio (0.67) with relatively low variance, primarily because in-hand reorientation demands continuous contact with the tool or object to monitor slip and state changes. Similarly, tasks such as _Wiping_ (0.49) and _Peeling_ (0.41) require prolonged frictional interaction. In contrast, _Cutting_ yields the lowest active ratio (0.27) and exhibits high variance, as these patterns typically involve an extended phase of visual alignment and pre-contact approach before the brief, high-force severing event. 

_3) Pattern-level Contact Area and Force Intensity:_ The heatmaps in Fig. 4(a) and (b) reveal a clear and physically intuitive distinction in how tactile sensors are spatially and dynamically engaged across different manipulation patterns. 

7 


Fig. 4: **Comprehensive statistical analysis of the OmniViTac. (a)** Pattern-level contact area distribution, highlighting the distinct dichotomy between precision-dominant tasks (concentrated in the 0-10% range) and surface-dominant tasks (peaking at 70-90%). **(b)** Force intensity distribution, showcasing the wide spectrum of force magnitudes required across different manipulation modes. **(c)** Hierarchical distribution illustrating the rich diversity of 86 instantiated tasks. **(d)** Effective contact ratio with variance across patterns, demonstrating the temporal dependency on tactile feedback (e.g., _Adjustment_ exhibits the highest continuous engagement). **(e)** Total trajectory counts per category, demonstrating the massive scale and balanced composition of the benchmark. **(f)** t-SNE projection of the high-dimensional tactile signals, revealing physically intuitive and semantically separable latent clusters that strictly align with the underlying contact mechanics of each interaction pattern. 

- **Precision-oriented tasks** (e.g., _Assembly, Grasping, Adjustment_ ): These manipulations are predominantly associated with the lowest deciles in both contact area (with 66% of occurrences in the 0 _−_ 10% range) and force intensity. This distribution reflects the underlying nature of these tasks, which rely on delicate, localized fingertip contacts and sensitive low-magnitude force feedback to adjust object poses or prevent damage precisely. 

- **Power-oriented or surface-oriented tasks** (e.g., _Cutting, Peeling, Wiping_ ): In contrast, these tasks exhibit extensive sensory activation. Their contact area distributions peak prominently in the 70% _−_ 90% range, indicating full-patch engagement of the sensor surface to maintain frictional contact. Moreover, _Cutting_ shows a marked shift toward higher force intensities (peaking in the 40% _−_ 50% range of sensor capacity), which is necessary for penetrating 

## materials and overcoming physical resistance. 

Together, these multi-dimensional statistics demonstrate that OmniViTac is not merely a collection of random contacts, but a highly structured and physically grounded benchmark, wellsuited to support advanced research in visuo-tactile perception and contact-rich policy learning. 

## IV. METHODOLOGY 

## _A. System Overview_ 

To achieve stable and robust contact-rich manipulation, we introduce OmniVTA, a hierarchical slow-fast manipulation policy built upon a visuo-tactile world model, as illustrated in Fig. 5. OmniVTA explicitly decomposes manipulation into _slow planning_ and _fast reflexive control_ . The _Slow Policy_ integrates the Visuo-Tactile World Model (VTWM) and the 

8 


Fig. 5: **System Overview** . OmniVTA is a hierarchical slow–fast policy for contact-rich manipulation. The slow policy contains a visuo-tactile world model and an adaptive fusion policy to generate long-horizon action chunks from multi-modal inputs. The fast policy outputs high-frequency refinements at 60 Hz using tactile feedback. Final actions are a weighted summation of slow-planned and fast-refined outputs, enabling both long-horizon planning and reactive control for robust manipulation. 

Adaptive Visuo-Tactile Fusion Policy (AFP) to perform longhorizon action chunk planning from low-frequency visual observations, high-frequency tactile signals, and proprioceptive states. To improve efficiency, the world model predicts future tactile signals without generating visual observations during inference, enabling higher-frequency rollout while preserving contact-relevant dynamics. The _Fast Policy_ is implemented as a Reflexive Latent Tactile Controller (RLTC), inspired by the reflexive control paradigm [50], [51], which outputs finegrained corrective actions at 60 Hz based on both predicted and observed tactile signals. This controller refines the action sequences generated by the slow policy by combining the planned actions with the controller outputs through a weighted summation, where the controller contribution is scaled by a predefined coefficient before execution on the robot. This slow-fast decomposition enables both long-horizon planning and high-frequency reflexive control, which are critical for contact-rich manipulation. 

In the following, we detail the components of OmniVTA. Sec. IV-B introduces the TactileVAE for tactile feature extraction. Sec. IV-C presents the Visuo-Tactile World Model, which captures contact dynamics via joint visual-tactile prediction. Sec. IV-D describes the adaptive fusion policy with a gated mechanism [52] for integrating visual and tactile features. Sec. IV-E details the Reflexive Latent Tactile Controller. 

## _B. TactileVAE_ 

TactileVAE aims to rapidly extract low-dimensional, continuous, and task-agnostic tactile representations for downstream prediction and policy learning. For optical tactile sensors, instead of using high-resolution tactile images, we adopt _3D marker displacement_ as tactile input. This representation captures contact-induced surface deformation while maintaining significantly lower resolution, enabling efficient feature extraction and higher-frequency inference. The structure of the TactileVAE is shown in Fig. 6, which contains a spatialtemporal encoder and an implicit deformation decoder. 

_1) Encoder:_ We construct a spatio-temporal encoder to extract compact tactile token representations. Since the markers on the tactile surface are uniformly distributed, a singleframe tactile observation can be represented as a tensor of size _H × W ×_ 3 where _H_ and _W_ denote the number of markers along the _y_ - and _x_ -axes, respectively, and the channel dimension corresponds to the marker displacement along the _x_ , _y_ , and _z_ directions. 

As tactile sensing typically operates at a higher frequency than vision, we perform joint temporal and spatial compression to reduce the number of tactile tokens and align them with visual tokens in time. To this end, we adopt a _3D convolutionbased variational autoencoder (VAE)_ and pretrain it on a large corpus of real tactile data to learn low-dimensional, taskagnostic latent features. 

As illustrated in Fig. 6, the encoder consists of a projectionin layer (causal 3D convolution), _M_ downsampling modules, and a projection-out layer (causal 3D convolution). The input is encoded into a latent feature map of size _<u>Hs</u>_<sup>_×_</sup><sup>_<u>W</u>_</sup> _s_<sup>_×C_,</sup> where _s_ = 2<sup>_M_</sup> is the spatial downsampling factor and _C_ is the latent dimension. We adopt _causal 3D convolutions_ along the temporal axis so that the latent representation at time _t_ depends only on current and past observations, ensuring consistency between training and real-time deployment. 

_2) Decoder:_ Instead of reconstructing pixels as in conventional VAEs, we employ an _implicit neural representation (INR)_ [53] decoder to model a continuous tactile deformation field conditioned on spatial coordinates. Implicit representations are well-suited for modeling continuous signals and have been widely used in computer vision tasks such as geometric reconstruction [54], [55] and dense prediction [56], [57]. Since marker displacement arises from the continuous deformation of the elastomer surface under contact, we model the deformation field as a continuous function: 


where **x** _∈_ R<sup>2</sup> denotes the spatial coordinate, **z** _t_ is the latent feature map, _γ_ ( _·_ ) represents positional encoding, Φ( **z** _t,_ **x** ) 

9 


Fig. 6: **Overview of TactileVAE.** The model encodes 3D marker displacements into spatio-temporal features, and reconstructs the deformation via an implicit decoder that represents the deformation as a continuous field. 

retrieves local features from **z** _t_ via spatial interpolation, and _Dθ_ is an MLP decoder that predicts the 3D deformation **d** ( **x** ) _∈_ R<sup>3</sup> . During training, we uniformly sample query points in the latent feature map and extract their local features, which, together with the corresponding positional encodings, are fed into the decoder to predict the corresponding _3D deformation vector_ . This yields a continuous reconstruction of the tactile surface deformation field. 

_3) Training Loss:_ For supervision, the ground-truth deformation **d**<sup>ˆ</sup> ( **x** ) at each query point **x** is obtained by interpolating the original 3D deformation. The TactileVAE is trained with a reconstruction loss and a KL regularization term [58]: 


## _C. Visuo-Tactile World Model_ 

In this section, we present the Visuo-Tactile World Model, which adopts a two-stream conditional generative framework and explicitly models the temporal evolution of visual observations and tactile signals, thereby learning a dynamic prior for multimodal interactions. Overall, it consists of three key modules. The two-stream world model separately characterizes the dynamic generation process of the visual and tactile modalities while performing coordinated prediction under a shared condition. The multimodal observation conditioner jointly encodes vision, tactile, and actions, providing consistent conditioning for the generation process. The dynamic-aware weighted loss further emphasizes regions with high-frequency tactile variations and salient contact responses, improving the modeling of fine-grained tactile dynamics. 

_1) Two-stream World Model:_ To model the evolution of visual observations and tactile states during policy execution, we build a two-stream visuo-tactile world model, as shown in Fig. 7 (a). Both branches employ a spatial-temporal diffusion transformer [59], which stacks transformer blocks along temporal and spatial axes. Specifically, the model takes the past _c_ frames as conditioning and iteratively denoises to generate multiple future frames, yielding a probabilistic model of future dynamics. The diffusion objective is defined as 


where **z** _o_ = � **z**<sup>1</sup> _o_<sup>_, . . . ,_</sup><sup>**z**</sup><sup>_K_</sup> _o_ � denotes a sequence of observation latents (including tactile latent **z** _t_ and visual latent **z** _v_ ), and **_ϵ_** _θ_ ( **z** _o, t_ ) predicts the noise for the entire sequence. Each **z**<sup>_i_</sup> _o_<sup>correspondstotheencodedobservationattimestep</sup><sup>_i_.</sup> The mask _m_ provides temporal conditioning, encouraging the model to leverage historical observations for predicting future states. At the modality encoding layer, the visual branch uses an SD-VAE [60] to extract image latents, while the tactile branch employs the TactileVAE pretrained in the previous stage to compress tactile signals. After obtaining the latent representations of vision and touch, the two modalities are fed into their corresponding spatial-temporal diffusion models, enabling parallel modeling and joint generation. 

_2) Multi-modal Observation Conditioner:_ To model joint visual-tactile dynamics effectively, we design a multi-modal conditional encoder for visual-tactile-action interactions. This module first performs feature extraction and temporal aggregation separately for visual observations, tactile embeddings, and historical action sequences, where each action is represented as the 2D image-plane projection of the 3D end-effector position. Specifically, each historical 3D end-effector position is transformed from the robot base frame into the current camera frame and then projected onto the current image plane using the camera intrinsics. We observe that this representation improves robustness to variations in manipulation locations. The modalities are then fused in a shared linear projection space to produce a fixed-dimensional conditioning vector. This vector is injected as a shared prior into both the tactile and visual world models, aligning the two branches and improving cross-modal consistency during dynamic prediction. 

_3) Dynamic-aware Weighted Loss:_ To supervise highfrequency dynamic changes in tactile signals more effectively, we introduce a Dynamic-Aware Weighted Loss. Specifically, the loss constructs a dynamic weight map based on local temporal differences of the tactile sequence to capture timevarying activity at different spatial locations: 


where _Xk_ denotes the tactile frame at the _k_ -th timestep, and resize( _·_ ) resizes the weight map from the raw tactile resolution to the latent resolution. The dynamic-aware loss is defined as the weighted simple diffusion loss: 


In addition, an amplitude weight map is constructed from the response magnitude of the tactile signal to represent the distribution of local contact intensity: 


10 


Fig. 7: **Overview of the Slow Policy. (a):** The proposed Visuo-Tactile World Model takes noisy tactile and visual latent sequences as input and jointly generates both modalities via a two-stream spatio-temporal diffusion transformer. **(b):** The Adaptive Visuo-Tactile Fusion Policy employs a Latent Tactile Differential Encoder to effectively encode the observed and predicted tactile and a gating mechanism to adaptively balance tactile and visual information for robust action planning. The amplitude loss is defined as Inspired by the human feedforward prediction mechanism, 

Inspired by the human feedforward prediction mechanism, we introduce a _Latent Tactile Differential (LTD) Encoder_ that captures potential contact states and interaction dynamics by modeling the difference between predicted future tactile features and the current tactile observation. Specifically, the current tactile feature map is spatially aggregated using 2D convolution and max pooling to obtain a global representation _ft_<sup>_c_.Predictedmulti-frametactilefeaturesarefirstaggregated</sup> spatially for each frame and then temporally using 1D convolution and max pooling to produce _ft_<sup>_p_.Thefinaltactilerepre-</sup> sentation is constructed through channel-wise concatenation of the current feature, the predicted feature, and their difference: 


The two weight maps are then aligned to the spatial resolution of the tactile latent representation and jointly used to modulate the reconstruction loss during training. This weighting strategy explicitly highlights regions with rapid dynamics and strong contact responses during optimization, thereby improving the modeling of high-frequency tactile patterns, local contact changes, and fine-grained temporal structure. Finally, the overall objective is a weighted sum of the diffusion loss and the dynamic-aware weighted loss: 


where _ft_<sup>_c_isextractedfromthetactileobservation,while</sup><sup>_f_</sup> _t_<sup>_p_</sup> denotes the tactile latent predicted by the visuo-tactile world model. The differential term highlights discrepancies between predicted and current tactile signals, providing informative cues for potential contact events and interaction dynamics. 


where _λ_ 1 and _λ_ 2 are the loss weights for the dynamic and amplitude terms, respectively. 

_2) Adaptive Visuo-Tactile Fusion:_ To effectively integrate visual and tactile information, we design a gating-based adaptive fusion module that modulates modality contributions according to the interaction state. 

## _D. Adaptive Visuo-Tactile Fusion Policy_ 

We propose the Adaptive Visuo-Tactile Fusion Policy, which adaptively balances visual and tactile information based on the predicted contact state for stable action planning. The policy comprises three components: a Latent Tactile Differential (LTD) Encoder for tactile representation, an Adaptive VisuoTactile Fusion module for modality weighting, and a VisuoTactile Diffusion Policy for action generation. 

Inspired by FoAR [61], we first construct a contact probability prediction module to estimate the likelihood of physical contact occurring within a future time window. The predicted contact probability serves as a modulation signal for modality fusion. This module takes the tactile representation _ft_ as input and predicts the contact probability using an MLP followed by a sigmoid activation. Contact labels are automatically generated by thresholding the tactile deformation magnitude: values exceeding a predefined threshold are labeled as contact, while others are treated as non-contact. The module is trained using BCE loss _Lbce_ . 

_1) Latent Tactile Differential (LTD) Encoder:_ Tactile signals exhibit strong spatial locality and remain largely inactive before contact, becoming informative only when physical interaction occurs. Previous approaches typically concatenate historical tactile observations with visual features as policy inputs, which cannot explicitly capture potential contact dynamics and their consequences, limiting performance in contact-rich manipulation. 

Based on the predicted interaction state, we further construct a gating network consisting of two fully connected layers. The 

11 

network takes the concatenation of the contact logit and tactile feature _ft_ as input and outputs normalized modality weights _Wt_ and _Wv_ , which modulate the tactile and visual features, respectively. _Wt_ and _Wv_ are per-channel weights normalized such that _Wt_ + _Wv_ = 1. Since the tactile representation already encodes future tactile dynamics through the world model, the gating network does not require visual inputs, reducing model complexity and improving computational efficiency. Before fusion, the tactile feature _ft_ is projected to the same dimensionality as the visual feature using a linear layer, producing the projected tactile feature _f_<sup>˜</sup> _t_ . The fused visuotactile representation is therefore computed as 


where _fv_ denotes the visual feature extracted by a ResNet-18 encoder. Notably, we use only the current and historical visual observations without incorporating future visual prediction, since the current image already provides sufficient global context for action planning, while the predicted tactile features capture potential contact dynamics, making visual prediction unnecessary and reducing model complexity. 

_3) Visuo-Tactile Diffusion Policy:_ We model the visuotactile manipulation policy as a conditional denoising diffusion model [62] conditioned on the fused visuo-tactile representation _fvt_ and robot proprioception _s_ . The policy generates a short-horizon action chunk by progressively denoising Gaussian noise. Specifically, the diffusion model predicts a sequence of coarse actions _Ac_ = ( _a_<sup>1</sup> _c_<sup>_, a_2</sup> _c_<sup>_, . . . , aH_</sup> _c_<sup>),where</sup><sup>_Ac_</sup> denotes an action chunk consisting of _H_ coarse actions. 

Starting from Gaussian noise _Ac,T_ , the denoising network _ϵθ_ iteratively refines the action chunk through _T_ steps to obtain the clean action sequence _Ac,_ 0: 


where _N_ (0 _, I_ ) denotes Gaussian noise and _αt_ , _γt_ , and _σt_ are scheduler-dependent coefficients. This reverse diffusion update resembles Stochastic Langevin Dynamics [63], where the noise predictor implicitly parameterizes the score function. During training, the model is conditioned on _fc_ = concat( _fvt, s_ ) and optimized using the DDPM objective 


To incorporate the conditional information, we adopt a CNN-based diffusion architecture where the conditioning feature _fc_ is injected through FiLM modulation [64]. 

_4) Training Loss:_ The Adaptive Visuo-Tactile Fusion Policy is jointly optimized with an action loss _L_ act and a contact prediction loss _L_ bce. The overall objective is defined as: 


Since the action chunk generated by the Visuo-Tactile Diffusion Policy is executed in an open-loop manner, we introduce a Reflexive Latent Tactile Controller to provide highfrequency tactile feedback and enable closed-loop control. 


Fig. 8: **Overview of the Reflexive Latent Tactile Controller (RLTC).** It takes single-frame tactile feedback, chunk-aligned predicted tactile latents, and robot/gripper delta states as input to produce high-frequency (60 Hz) refined single-step corrective actions. 

_1) Model Design:_ The RLTC takes single-frame tactile feedback, predicted tactile features, and robot states as input and outputs a high-frequency refined action. Specifically, since the TactileVAE compresses tactile observations along the temporal dimension by a factor of _M_ = 4, the current singleframe tactile observation is temporally repeated four times to form a short sequence compatible with the encoder and is then encoded into a current tactile latent feature using the TactileVAE. Similarly, the tactile predictions generated by the world model have a lower temporal resolution of 15 Hz due to latent compression. We upsample the predicted tactile latent sequence using nearest-neighbor interpolation, such that each predicted latent is repeated and shared by four consecutive 60 Hz control steps, establishing an explicit 4-to-1 chunk-level temporal correspondence between the 15 Hz predicted tactile latents and the 60 Hz tactile feedback. The LTD Encoder is then applied to jointly encode the current tactile feature and the corresponding predicted future tactile feature at each time step, producing a tactile representation. Meanwhile, the robot’s historical delta actions over the past _h_ steps are transformed into the TCP coordinate frame and concatenated with the corresponding delta gripper states to form a trajectory feature. Finally, the tactile representation and trajectory feature are concatenated and fed into a three-layer MLP to output a singlestep refined action _ar_ . 

_2) Training Loss:_ To train the Reflexive Latent Tactile Controller, we jointly use abnormal recovery samples and normalcontact samples. For each task category, we first estimate a valid tactile distribution using the mean and standard deviation of human-collected expert trajectories. Tactile observations outside this distribution, such as those exhibiting excessively large or small contact forces, are identified as abnormal states. 

12 

TABLE II: Objects used for training and manipulation across different robotic tasks. Each object is associated with 150 manipulation trajectories in the dataset for training world models and manipulation policies. 

|**Task**|**Object Used for Training**|**Object Used for Manipulation**|
|---|---|---|
|**Wipe**|vases in 4 different colors and shapes, plate, and whiteboard|vases in 4 different colors and shapes|
|**Peel**|cucumber, Chinese yam, radish, carrot, and white daikon|cucumber, Chinese yam, radish|
|**Cut**|cucumber, Chinese yam, carrot, pepper, and banana|cucumber, Chinese yam, pepper, banana|
|**Assembly**|3 colors of USB stick and 3 types of charging adapters|red USB stick and silver USB stick|
|**Grasp**|blueberry, strawberry, grape, cherry, and cherry tomato|blueberry, strawberry, grape, and cherry tomato|
|**Adjustment**|test tube, pencil, cuboid, cylinder, and triangular prism|cuboid, cylinder|


We then extract recovery segments in which a human operator drives the system from an abnormal tactile state back to the valid distribution, as well as normal-contact segments whose tactile observations remain within the valid range. For each abnormal recovery sample, the target corrective action ˆ _ar_ is defined as the residual between the expert recovery action and the action generated by the slow policy, whereas the target residual for each normal-contact sample is set to zero. The controller is trained to predict the corrective action _ar_ using a mean squared error (MSE) loss: 


which encourages the controller to output near-zero residuals during normal execution while producing high-frequency tactile-driven corrections under abnormal contact conditions. 

## V. EXPERIMENTAL EVALUATION 

Our experiments are organized into three parts. First, we describe the experimental setup and implementation details. Second, we evaluate the overall performance of OmniVTA on manipulation tasks involving diverse tactile interaction patterns. Then, we conduct comprehensive ablation studies to analyze the contribution of each module in the proposed policy. Specifically, we investigate the following questions: (1) whether the TactileVAE can effectively encode tactile signals; (2) whether the proposed visuo-tactile world model can predict future tactile signals more accurately than alternative tactile prediction approaches; (3) whether incorporating predicted future tactile signals improves policy performance and whether the proposed usage of predicted tactile information in OmniVTA is effective; and (4) whether the Reflexive Latent Tactile Controller can generate reasonable fine-grained corrective actions and how much it improves policy execution. We further analyze the contribution of each design component through detailed ablation studies. 

## _A. Experimental Setup_ 

_1) Training Details:_ Our OmniVTA framework is trained in four stages: training the TactileVAE, training the Visuo-Tactile World Model, training the Adaptive Visuo-Tactile Fusion Policy, and training the Reflexive Latent Tactile Controller. **Training of TactileVAE.** For training the TactileVAE, we use tactile data from 20% of the manipulation trajectories, together with additional tactile interaction data collected from 

interactions between 10 extra objects and the tactile sensors. The resulting dataset contains approximately 1.2M tactile samples. Both TactileVAE and the VAE baselines are trained for 50 epochs using 8 NVIDIA A100 GPUs. The loss weights are set to _λ_ KL = 1 _e −_ 6. 

**Training of Visuo-Tactile World Model.** We first construct a dataset to train the Visuo-Tactile World Model, comprising six categories of tactile interaction patterns. For each category, 5–6 objects are selected, and 150 manipulation trajectories per object are collected using TacUMI and the xArm7. The data are split into training and test sets with a 90%/10% ratio. A detailed breakdown of the dataset is provided in Table II. 

For training the Visuo-Tactile World Model, we use AdamW with a learning rate of 1 _×_ 10<sup>_−_4</sup> and weight decay 0. The perGPU batch size is 5, and the total number of training steps is 100 _,_ 000. The gradient norm threshold is set to 0 _._ 1, with gradient clipping enabled after 20 _,_ 000 steps. The loss weights are set to _λ_ dyn = 1 _._ 0 and _λ_ amp = 1 _._ 0. 

**Training of Adaptive Visuo-Tactile Fusion Policy.** We used the same training set to train the Adaptive Visuo-Tactile Fusion Policy. For each interaction category, the data are combined to train a unified visuo-tactile generation and manipulation model (OmniVTA), as well as other policy baselines. The Adaptive Visuo-Tactile Fusion Policy is trained for 250k steps. Other manipulation baselines are trained for 350k steps to compensate for the absence of additional perception modules. The loss weights are set to _λct_ = 0 _._ 2. 

**Parameter settings.** Following prior work, we adopt _relative actions_ as the action representation. During training, visual observations are sampled at 15 Hz, tactile signals at 60 Hz, and robot proprioception at 60 Hz. The policy outputs action chunks at 15 FPS. For observations, both OmniVTA and all baselines use the current and previous visual frames (2 frames in total), the corresponding 8 tactile frames within the same temporal window, and 2 proprioceptive observations as policy inputs. Each action chunk predicts the next 6 actions, which are interpolated to 60 Hz during execution. 

**Details about the model size.** Table III shows the parameter counts of the major components of OmniVTA, including the TactileVAE, the visuo-tactile world model, and the RLTC. 

13 

TABLE III: Model sizes of the main OmniVTA components. 

|**Component**|**Parameters**|
|---|---|
|TactileVAE|1.96 M|
|Visuo–Tactile World Model|271.57 M|
|Adaptive Visuo–Tactile Fusion Policy|326.89 M|
|RLTC|0.10 M|
|**Total**|**600.52 M**|


_2) Hardware Setup:_ The experimental platform consists of a UFactory xArm7 robotic arm equipped with a parallel two-finger gripper and two fingertip tactile sensors. An Intel RealSense D435 camera mounted on the robot wrist provides RGB observations at 15 Hz, while the tactile sensors capture tactile signals at 60 Hz. For the TactileVAE validation experiments, three types of tactile sensors are used: GelSight Mini, Tac3D, and Xense. The resolutions of their reconstructed 3D displacement fields are 7 _×_ 9, 20 _×_ 20, and 35 _×_ 20, respectively. In the real-world manipulation experiments, we use only the Xense sensors. 

_3) Baselines:_ We select representative baseline methods to evaluate the effectiveness of the proposed TactileVAE, VisuoTactile World Model, and the overall OmniVTA framework. **TactileVAE baselines.** We compare the proposed TactileVAE with two representative tactile encoding methods: PCA-based features and a point cloud-based autoencoder [65]. 

**Tactile prediction baselines.** We compare our Visuo-Tactile World Model against three representative paradigms for multimodal generative modeling. 

- **Unified multimodal generation** : UVA [66] models video frames and actions as a unified token sequence and jointly generates them using a single generative model. We extend this formulation by injecting tactile tokens. 

- **Joint trajectory diffusion** : ForceMimic [67] and KineDex [68] concatenate interaction forces with actions and learn diffusion-based policies conditioned on visual observations. In our implementation, we replace force inputs with tactile feature embeddings extracted using a lightweight MLP autoencoder. 

- **Conditional modality prediction** : exUMI [43] generates future tactile signals using a latent diffusion model (LDM) conditioned on visual observation and action. Since our method assumes only historical observations are available at inference, future action inputs are replaced with historical action sequences. 

**Contact-rich policy baselines.** We compare against several state-of-the-art imitation learning policies: 

- **DP** [62]: Diffusion Policy using wrist-view RGB observations and open-loop action chunk execution. 

- **DP+tactile** : Diffusion Policy augmented with tactile features encoded by PCA. 

- **KineDex** [68]: a diffusion policy that jointly predicts actions and forces from visual observations. 

- **ForceMimic** [67]: a diffusion policy conditioned on 3D observations that jointly predicts actions and forces. 

- **RDP** [5]: a reactive diffusion policy with a slow diffusion planner and a fast tactile-based reactive controller. 

- **OmniVTA (ours)** : our method with a visuo-tactile world model and a dual-system manipulation policy consisting of a diffusion planner and a reflexive tactile controller. 

- **OmniVTA w/o RLTC** : our method without the reflexive controller, executing diffusion-planned action chunks in a open-loop manner. 


Fig. 9: **Objects used in the manipulation tasks.** 

_B. Overall Performance_ 

We evaluate the real-world manipulation performance of OmniVTA from three perspectives: object diversity, generalization, and perturbation robustness. 

**Object diversity.** For each category, we evaluate the policy on 2–4 different objects, as summarized in Table II and Fig. 9. Before each trial, the object is placed at a random position and fixed during manipulation. For each object, we perform 10 trials and report the average success rate. 

**Generalization.** We evaluate two types of generalization. 

(1) _Position generalization._ For the wipe, peel, assembly, and adjustment tasks, objects are placed at two additional unseen heights during evaluation. For each object and each height, we conduct 5 trials and report the average success rate. 

(2) _Tool generalization._ For the cut task, we replace the training knife with a previously unseen knife (shown in Fig. 9). Each object is tested 10 times using the new tool. 

**Perturbation robustness.** For the wipe, peel, cut, and assembly tasks, we introduce controlled perturbations during execution to disrupt the current contact state. Specifically, the target object is suddenly displaced upward or downward along the vertical direction during the interaction phase. This perturbation breaks the existing contact state and requires the policy to re-establish stable contact. For each task, one representative object is selected and evaluated over 10 trials. **Evaluation metric.** The primary evaluation metric is task success rate. A trial is considered successful if the task objective is completed and no damage occurs to the tactile sensors during execution. For wiping, peeling, and cutting tasks, we measure task completion using the ratio of the successfully processed length (e.g., the proportion of removed peel, erased marks, or completed cuts). For assembly and grasping tasks, a trial is considered successful only if the object is fully inserted or grasped without damage. For adjustment tasks, success is 

14 


Fig. 10: **Real-robot manipulation results.** We visualize the manipulation process across six task categories. 

TABLE IV: Performance comparison of OmniVTA and baseline methods across six tasks under three evaluation settings: object diversity (O), generalization (G), and perturbation robustness (P). Results are reported in terms of success rate. 

|**Task**||**Wipe**|||**Peel**|||**Cut**||**A**|**ssembl**|**y**|**Grasp **|**Adjus**|**tment**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method / Eval. setting**|**O**|**G**|**P**|**O**|**G**|**P**|**O**|**G**|**P**|**O**|**G**|**P**|**O**|**O**|**G**|
|DP|0.12|0.05|0|0.06|0|0|0.28|0.10|0|0.10|0|0.05|0.20|0|0|
|DP+tactile|0.36|0.28|0|0.32|0.20|0.08|0.33|0.15|0.13|0.30|0.10|0.10|0.48|0.25|0.15|
|KineDex|0.40|0.25|0|0.24|0.13|0.05|0.38|0.30|0.20|0.30|0.15|0.15|0.65|0.30|0.20|
|ForceMimic|0.33|0.20|0|0.27|0.18|0|0.50|0.25|0.05|0.35|0.15|0.10|0.60|0.10|0|
|RDP|0.50|0.38|0.42|0.48|0.36|0.45|0.65|0.50|0.43|**0.60**|**0.50**|0.35|0.88|0.50|0.50|
|OmniVTA w/o RLTC|0.66|0.40|0.25|0.40|0.30|0.20|0.50|0.50|0.20|0.40|0.35|0.20|0.70|0.40|0.30|
|**OmniVTA**|**0.80**|**0.58**|**0.60**|**0.55**|**0.48**|**0.63**|**0.85**|**0.83**|**0.60**|**0.60**|**0.50**|**0.40**|**0.90**|**0.65**|**0.65**|


defined as achieving a pose change that exceeds a predefined angular threshold (60°). 

**Results.** The overall real-robot manipulation results are visualized in Fig. 10, and the corresponding overall success rates are reported in Table IV. In the object diversity evaluation, OmniVTA achieves the best performance across all six tasks, demonstrating the effectiveness of the proposed framework. Adding the closed-loop controller further improves performance compared with the open-loop variant (OmniVTA w/o RLTC), highlighting the importance of feedback control in contact-rich manipulation. 

We also observe that, for contact-rich tasks involving strong physical interactions (e.g., wiping, peeling, cutting), the performance gain from the reactive policy in RDP (compared with DP+tactile) is smaller than the improvement brought by our reflexive controller. This is because our controller leverages predicted tactile signals as targets to regulate the robot’s motion, enabling reliable contact while preventing excessive contact forces. During the contact phase, the average tangential deformation measured by our tactile sensors is 0.35 with a maximum of 0.72. In contrast, the reactive policy in RDP often 

produces overly strong contacts that damage the sensors, with an average deformation of 0.56 and a maximum of 1.1. In the unseen-height evaluation, the performance of RDP drops moderately, while other baselines degrade significantly. In contrast, OmniVTA without the closed-loop controller already surpasses RDP, indicating stronger robustness to geometric variations. In the tool generalization experiment, replacing the knife with a smaller, unseen tool has little impact on our performance in the cut task. This suggests that the policy relies on tactile feedback rather than memorizing demonstration trajectories. Finally, in the perturbation experiments, OmniVTA consistently achieves the highest success rates. Moreover, the closed-loop controller significantly improves performance compared with the openloop variant, demonstrating its ability to quickly recover stable contact during perturbations. 

## _C. Component Analysis_ 

_1) TactileVAE:_ We evaluate TactileVAE from two aspects: reconstruction accuracy and latent representation quality. **Reconstruction evaluation.** We compare TactileVAE with baseline methods across six categories of tactile interaction patterns. Reconstruction performance is evaluated using the 

15 

TABLE V: Performance comparison of different methods across robotic tasks using L2 and cosine similarity metrics. Lower L2 ( _↓_ ) and higher cos ( _↑_ ) indicate better performance. 

|**Method**|**Wi**|**pe**|**Pe**|**el**|**C**|**ut**|**Asse**|**mbly**|**Gr**|**asp**|**Adjus**|**tment**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||L2 _↓_|cos _↑_|L2 _↓_|cos _↑_|L2 _↓_|cos _↑_|L2 _↓_|cos _↑_|L2 _↓_|cos _↑_|L2 _↓_|cos _↑_|
|PCA|0.091|0.810|0.085|0.430|0.109|0.400|0.071|0.720|0.036|0.600|0.069|0.560|
|PointNet-AE|0.059|0.910|0.067|0.850|0.062|0.840|0.058|0.900|0.028|**0.750**|0.047|0.760|
|**Ours**|**0.038**|**0.930**|**0.033**|**0.880**|**0.031**|**0.940**|**0.022**|**0.910**|**0.011**|0.720|**0.017**|**0.850**|


_L_ 2 distance and cosine similarity, which measure the magnitude and directional consistency of the reconstructed 3D deformation, respectively. The _L_ 2 metric is computed over the entire deformation field, while cosine similarity is computed over non-zero deformation regions only. As shown in Table V, the proposed TactileVAE consistently achieves the best performance across all six categories, demonstrating its effectiveness in modeling tactile deformation. 

**Latent representation analysis.** To further evaluate the learned tactile representations, we conduct experiments on three unseen objects under three types of force patterns (press, twist, and slide) using three tactile sensors, two of which are unseen during training, as shown in Fig. 11(a) and (b). We record the tactile signals and extract their features using several variants of TactileVAE, including: 

- **w/o implicit decoder:** decodes the latent feature map without query-based sampling and query points input. 

- **w/ position embedding:** incorporates positional encoding during decoding. 

- **w/o spatial feature map:** represents the latent as a single token and decodes it with an implicit decoder. 

- **w/ implicit decoder:** decodes the latent feature map via an implicit decoder. 

All models are trained using only 5% of the tactile dataset. 

For visualization, the spatio-temporal tactile features are aggregated via max pooling to obtain sequence-level embeddings, which are then visualized using t-SNE. As shown in Fig. 11(c), the learned representations exhibit clear clustering across different force patterns, even under cross-sensor settings. In contrast, marker-based encoding and variants without positional information fail to produce well-separated clusters, highlighting the importance of implicit neural representations for learning discriminative tactile features. 

Finally, we compare two forms of tactile feature representations: local feature maps (patch-based features) and a global token obtained via max pooling. As shown in Fig. 11(c) and Table VI, local feature maps achieve better reconstruction accuracy and yield more informative tactile embeddings than the global token representation. 

_2) Visuo-Tactile World Model:_ In this section, we evaluate the proposed Visuo-Tactile World Model in terms of prediction accuracy, module effectiveness, and robustness to observation perturbations. We measure tactile prediction accuracy using the _L_ 2 distance and cosine similarity between the predicted and ground-truth tactile signals, following the evaluation protocol of TactileVAE. To better illustrate prediction performance over different horizons, we report both the _L_ 2 distance 

TABLE VI: Ablation study on the design of TactileVAE. We evaluate reconstruction performance using the _L_ 2 metric. 

|**Method**|**GelSight-Mini **|**Tac3D-A1 **|**Xense-QN1**|
|---|---|---|---|
|w/o implicit decoder|0_._126|0_._098|0_._038|
|w/ position embed.|0_._102|0_._085|0_._035|
|w/o spatial feature map|0_._107|0_._084|0_._071|
|w/ implicit decoder|**0.047**|**0.058**|**0.034**|


Fig. 11: **Ablation study of TactileVAE.(a)** shows the sensors and objects for testing. **(b)** represents the three types of force loaded on the sensors. **(c)** visualizes the t-SNE of the tactile latent feature maps extracted by different models. 

and cosine similarity at the 2nd, 4th, and 6th prediction latent frames, corresponding to the 8th, 16th, and 24th decoded tactile frames, respectively, as well as the metrics averaged over all 24 predicted frames. 

**Prediction accuracy.** We first compare our method with four baselines from three representative paradigms: unified multimodal generation, joint trajectory diffusion, and conditional tactile prediction. As shown in Table VII and Fig. 12, our model consistently outperforms all baselines in both short-term and long-term tactile prediction. These results demonstrate that our method effectively models the cross-modal dynamics between vision and tactile signals, enabling accurate and consistent generation across both modalities. **Ablation study.** We further analyze the contribution of several key components in the proposed model. 

(1) _Joint visual–tactile generation._ Table VIII shows that jointly generating future visual features together with tactile features improves tactile prediction accuracy. This indicates 

16 


Fig. 12: **Visuo-tactile generation visualization across six task categories.** Red arrows indicate predicted tangential deformation, while blue arrows denote ground truth. Normal deformation in the grasp task is visualized using heatmaps. 

TABLE VII: Prediction performance. We report the _L_ 2 distance and cosine similarity at the 2nd, 4th, and 6th latent prediction steps (denoted as _L_ 21 _, L_ 22 _, L_ 23 and _C_ 1 _, C_ 2 _, C_ 3), corresponding to the 8th, 16th, and 24th decoded tactile frames, respectively. We also report the average performance over all 24 predicted frames ( _L_ 2avg, _C_ avg). Top: Wipe/Peel/Cut. Bottom: Adjustment/Assembly/Grasp. “–” denotes not applicable. 

|||**Wipe**|||||**Peel**||||||**Cut**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|_L_21<br>_L_22|_L_23<br>_L_2avg|_C_1<br>_C_2|_C_3<br>_C_avg|_L_21<br>_L_22|_L_23|_L_2avg|_C_1<br>_C_2<br>_C_3|_C_avg|_L_21|_L_22|_L_23|_L_2avg|_C_1|_C_2<br>_C_3<br>_C_avg|
|**UVA**|0.084 0.091|0.088 0.088|0.68 0.65|0.64 0.66|0.090 0.097|0.102|0.097|0.62 0.60 0.60|0.61|0.075|0.076|0.078|0.077|0.72|0.71 0.71 0.71|
|**exUMI**|0.097 0.098|0.103 0.101|0.59 0.58|0.58 0.58|0.093 0.099|0.102|0.097|0.63 0.62 0.62|0.62|0.083|0.086|0.088|0.086|0.73|0.72 0.71 0.72|
|**Kinedex**|0.081 0.084|0.085 0.082|0.82 0.80|0.81 0.81|0.064 0.066|0.068|0.066|0.77 0.79 0.80|0.79|0.091|0.100|0.104|0.096|0.74|0.73 0.72 0.73|
|**Forcemimic**<br>**Ours**|0.089 0.091 <br>**0.052 0.062 **|0.094 0.091 <br> **0.072 0.059 **|0.70 0.68 <br> **0.93 0.92 **|0.68 0.68<br>**0.91 0.93**|0.077 0.077 <br>**0.033 0.037 **|0.078 <br> **0.041 **|0.077 <br> **0.036 **|0.76 0.76 0.73 <br> **0.88 0.88 0.87 **|0.76<br> **0.87**|0.089 <br>**0.048 **|0.091 <br> **0.052 **|0.091 <br> **0.057 **|0.090 <br> **0.050 **|0.71 <br> **0.89 **|0.71 0.72 0.71<br> **0.89 0.88 0.88**|
|||**Adjustm**|**ent**||||**Assem**|**bly**|||||**Gras**|**p**||
|**Method**|_L_21<br>_L_22|_L_23<br>_L_2avg|_C_1<br>_C_2|_C_3<br>_C_avg|_L_21<br>_L_22|_L_23|_L_2avg|_C_1<br>_C_2<br>_C_3|_C_avg|_L_21|_L_22|_L_23|_L_2avg|_C_1|_C_2<br>_C_3<br>_C_avg|
|**UVA**|0.080 0.085|0.084 0.083|0.73 0.68|0.67 0.69|0.072 0.074|0.078|0.074|0.74 0.69 0.68|0.68|0.079|0.080|0.085|0.080|0.67|0.64 0.64 0.65|
|**exUMI**|0.080 0.087|0.083 0.083|0.64 0.60|0.60 0.61|0.096 0.096|0.103|0.096|0.59 0.53 0.52|0.53|0.076|0.081|0.085|0.081|0.66|0.65 0.63 0.65|
|**Kinedex**|0.052 0.053|0.055 0.053|0.70 0.70|0.69 0.70|0.045 0.048|0.052|0.047|0.80 0.77 0.75|0.78|0.017|0.017|0.017|0.017|0.60|0.60 0.58 0.59|
|**Forcemimic**<br>**Ours**|0.082 0.081 <br>**0.022 0.025 **|0.082 0.082 <br> **0.028 0.025 **|0.66 0.65 <br> **0.85 0.84 **|0.65 0.65<br>**0.84 0.85**|0.071 0.071 <br>**0.028 0.032 **|0.071 <br> **0.036 **|0.071 <br> **0.030 **|0.69 0.68 0.67 <br> **0.90 0.89 0.88 **|0.68<br> **0.89**|–<br>**0.010 **|–<br> **0.010 **|–<br> **0.010 **|–<br> **0.010 **|–<br> **0.70 **|–<br>–<br>–<br> **0.67 0.67 0.68**|


that visual prediction provides complementary global dynamic cues that help the model better capture interaction dynamics. 

(2) _Action representation._ We compare three types of action conditioning in the world model: projected 2D actions, 3D absolute actions, and 3D relative actions. As shown in Table VIII, the 2D action representation achieves the best generalization performance on unseen object positions, followed by relative actions. This result suggests that the action condition primarily conveys motion intent and that 2D actions align more naturally with visual observations. 

(3) _Dynamic weighting._ The results in Table VIII show 

that the proposed dynamic weighting strategy improves tactile prediction performance. This weighting mechanism explicitly emphasizes regions with rapid dynamics and strong contact responses during optimization, enabling the model to better capture high-frequency tactile patterns, local contact variations, and fine-grained temporal structures. 

**Perturbation robustness.** Finally, we evaluate the robustness of the Visuo-Tactile World Model in the wipe-vase task. After contact occurs, the visual and tactile observations are replaced with non-contact observations corresponding to the object being moved downward. As shown in Fig. 13, the 

17 


Fig. 13: **Perturbation and recovery.** The first row shows a contact break due to downward perturbation, with tactile signals transitioning to a no-contact state. The second row shows recovery to the contact state within one generation chunk. In tactile visualization, red arrows denote tactile prediction while blue arrows denote ground truth. 

TABLE VIII: Performance evaluation under different test cases, action spaces, and dynamic weight settings. Lower _L_ 2 and higher cosines indicate better performance. 

TABLE IX: Ablation study on Adaptive Visuo-Tactile Fusion Policy and the components’ impact on task success rate. 

||||||||**Com**|**ponen**|**t**||**Suc**|**cess R**|**ate**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Settings**|**Action**|**Dyn. Weight**|**Joint Gen.**|**L2** _↓_|**Cos** _↑_|Pred.|Used as<br>|<sup>LTD</sup>|<sup>Gti </sup>|<sup>Visual</sup>|Wi|Pl|A|
||3D absolute|✓|✓|0.075|0.72|Len.|Contact State||<sup>ang </sup>|<br>Gen.|pe|ee|vg.|
|Unseen<br>Position|3D relative|✓|✓|0.056|0.88|0|_×_|_×_|_×_|_×_|0.12|0.06|0.09|
||2D|✓|✓|**0.042**|**0.91**|2|_×_|_×_|_×_|_×_|0.40|0.26|0.33|
|||||||4|_×_|_×_|_×_|_×_|0.45|0.30|0.38|
|S|2D|_×_|_×_|0.041|0.90|6|_×_|_×_|_×_|_×_|0.50|0.30|0.40|
|een<br>Position|2D|_×_<br>|✓<br>|0.038|0.92|6|✓|_×_|_×_|_×_|0.46|0.28|0.37|
||2D|✓|✓|**0.035**|**0.93**|6|_×_|✓|_×_|_×_|0.57|0.36|0.47|
|||||||6|_×_|✓|✓|_×_|0.66|**0.40**|0.53|
|||||||6|_×_|✓|✓|✓|**0.70**|0.38|**0.54**|


model exhibits a certain level of recovery capability under observation perturbations. 

_3) Adaptive Visuo-Tactile Fusion Policy:_ In this section, we analyze the key components of the proposed Adaptive VisuoTactile Fusion Policy through a series of experiments and address the following questions: (1) Does predicted future tactile information improve action planning? (2) Is the proposed Latent Tactile Differential (LTD) Encoder more effective than simple feature concatenation? (3) Is the gating mechanism necessary for adaptive visuo-tactile fusion, and do modality weights correlate with contact states? (4) Does the VisuoTactile Diffusion Policy depend on the accuracy of tactile prediction? (5) Do generated visual features further improve policy performance? (6) What role does the Reflexive Latent Tactile Controller play during execution? 

**Effect of predicted tactile signals.** We first investigate whether predicted tactile information improves action planning. As shown in Table IX, we compare two tactile representations: (1) using only the current tactile observation, and (2) concatenating the current tactile observation with predicted tactile features at future horizons of 2, 4, and 6 steps. To eliminate the influence of feature dimensionality, 

TABLE X: Inference time of each component on RTX 4090D. 

|Slow Policy|Slow Policy w/ Visual Gen.|Fast Policy|
|---|---|---|
|230 ms|480 ms|3.5 ms|


the concatenated tactile features are projected to the same dimension as the current tactile representation through a linear layer, ensuring consistent policy input size across settings. In this experiment, the gating mechanism is retained while the controller is disabled. Results show that incorporating predicted tactile information consistently improves policy success rates, and longer prediction horizons (6 steps) outperform shorter ones (4 steps and 2 steps). This indicates that future tactile prediction provides richer contact dynamics that benefit action planning. 

**Comparison of tactile representations.** We further compare different tactile representation strategies: (1) direct concatenation of current and predicted tactile features, and (2) the proposed LTD Encoder applied to both signals. For fair comparison, the resulting tactile features are projected to the 

18 


Fig. 14: **Gating Fusion Mechanism.** We visualize the temporal evolution of the predicted contact probability (purple), together with the corresponding visual (blue) and tactile (red) weights over the course of task execution. 


Fig. 15: **Perturbation experiments.** We break contact by abruptly lowering the object and demonstrate how the policy rapidly restores contact via the RLTC. 

same dimensionality before being fed into the policy network. As shown in Table IX, the LTD-based representation achieves higher success rates across multiple tasks. This suggests that the LTD Encoder effectively captures the dynamic relationship between current and predicted tactile, producing a more informative tactile representation for policy learning. 

**Necessity of the gating fusion mechanism.** Next, we evaluate the effectiveness of the gating mechanism for visuo-tactile fusion by comparing two input configurations: (1) direct concatenation of visual features and LTD-encoded tactile features, and (2) adaptive fusion using the proposed gating mechanism. As shown in Table IX, the gating mechanism improves the average task success rate by approximately 7% compared to direct concatenation. We further visualize the predicted contact probability and the modality weights in Fig. 14. The results show a strong correlation between modality weights 

and contact states: when no contact occurs, the tactile weight remains close to zero, while it increases significantly as the predicted contact probability rises, indicating that action planning increasingly relies on tactile information during contact. 

**Effect of tactile prediction.** To evaluate how policy performance depends on tactile prediction quality, we introduce controlled prediction errors by using world model checkpoints with varying tactile prediction accuracies, corresponding to 80%, 60%, 40%, and 20% of the performance of the bestperforming model. As shown in Fig. 17, as prediction accuracy decreases, the policy gradually loses its ability to correctly infer contact states and adjust modality weights, leading to degraded action planning performance. This proves that accurate tactile prediction plays a critical role in our policy. Besides, using a lighter alternative that predicts only future contact state instead of using tactile prediction will result in a significant 

19 


Fig. 16: **Recovery time of OmniVTA w/ RLTC and w/o RLTC.** 

decrease of success rate, as shown in Table IX. 


Fig. 17: **Effect of tactile prediction accuracy. Left:** At 60% prediction performance, the model fails to estimate future contact probability, resulting in improper modality weighting. **Right:** Lower prediction performance leads to a significant drop in success rate. 

**Effect of generated visual features.** We also investigate whether incorporating generated visual features improves policy performance. Experimental results show that adding generated visual features to the policy input does not yield significant performance gains, as shown in Table IX. Moreover, introducing a visual generation branch significantly reduces inference frequency, as shown in Table X. Therefore, the final policy design relies only on current visual observations rather than on the generation. 

**Effectiveness of the Reflexive Latent Tactile Controller.** Finally, we evaluate the contribution of the Reflexive Latent Tactile Controller. The controller enables high-frequency closed-loop control, allowing the robot to execute actions more stably and improving overall task success rates. In perturbation experiments, shown in Table IV and Fig. 15, the controller rapidly responds to environmental perturbations. When perturbations disrupt the current contact state, the highfrequency controller adjusts robot actions to re-establish stable contact. In tasks requiring strong interaction forces, the controller also adaptively modulates the action magnitude to prevent excessive contact forces. Besides, Fig. 16 shows the effectiveness of the RLTC. With RLTC, the policy can recover from the perturbation quickly. 

## VI. CONCLUSION 

In this work, we address two persistent bottlenecks in visuotactile manipulation: the scarcity of large-scale, task-diverse training data and the lack of methods that model contact dynamics explicitly while supporting closed-loop tactile control. On the data side, OmniViTac comprises 21 _,_ 000+ temporally aligned trajectories spanning 86 contact-rich tasks organized 

into six physics-grounded interaction patterns. Systematic analysis of the dataset identifies two structural properties of tactile signals in manipulation, spatial locality, and contactdriven dynamics, which guided the architectural design of OmniVTA. On the methodology side, OmniVTA integrates self-supervised implicit tactile representation learning, shorthorizon visuo-tactile world modeling, contact-aware multimodal fusion, and high-frequency reflexive control within a unified framework. Real-robot experiments across all six interaction categories demonstrate that OmniVTA consistently outperforms existing baselines, with clear advantages in generalization to unseen objects and geometric configurations and robustness to external disturbances. 

## REFERENCES 

- [1] Z. Zhao, Y. Li, W. Li, Z. Qi, L. Ruan, Y. Zhu, K. Althoefer, Tac-man: Tactile-informed prior-free manipulation of articulated objects, IEEE Transactions on Robotics 41 (2024) 538–557. 

- [2] L. Cui, Z. Zhao, S. Xie, W. Zhang, Z. Han, Y. Zhu, Vi-tacman: Articulated object manipulation via vision and touch, arXiv preprint arXiv:2510.06339 (2025). 

- [3] Z. Zhao, Z. Qi, Y. Li, L. Cui, Z. Han, L. Ruan, Y. Zhu, Tacmanturbo: Proactive tactile control for robust and efficient articulated object manipulation, arXiv preprint arXiv:2508.02204 (2025). 

- [4] J. Bi, K. Y. Ma, C. Hao, M. Z. Shou, H. Soh, Vla-touch: Enhancing vision-language-action models with dual-level tactile feedback, arXiv preprint arXiv:2507.17294 (2025). 

- [5] H. Xue, J. Ren, W. Chen, G. Zhang, Y. Fang, G. Gu, H. Xu, C. Lu, Reactive diffusion policy: Slow-fast visual-tactile policy learning for contact-rich manipulation, arXiv preprint arXiv:2503.02881 (2025). 

- [6] H. Chen, J. Xu, H. Chen, K. Hong, B. Huang, C. Liu, J. Mao, Y. Li, Y. Du, K. Driggs-Campbell, Multi-modal manipulation via multi-modal policy consensus, arXiv preprint arXiv:2509.23468 (2025). 

- [7] S. Yu, K. Lin, H. Soh, Demonstrating the octopi-1.5 visual-tactilelanguage model, arXiv preprint arXiv:2507.09985 (2025). 

- [8] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang, et al., Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems, arXiv preprint arXiv:2503.06669 (2025). 

- [9] B. Huang, Y. Wang, X. Yang, Y. Luo, Y. Li, 3d-vitac: Learning fine-grained manipulation with visuo-tactile sensing, arXiv preprint arXiv:2410.24091 (2024). 

- [10] T. Wu, J. Li, J. Zhang, M. Wu, H. Dong, Canonical representation and force-based pretraining of 3d tactile for dexterous visuo-tactile policy learning, in: 2025 IEEE International Conference on Robotics and Automation (ICRA), IEEE, 2025, pp. 6786–6792. 

- [11] J. Monz´ee, Y. Lamarre, A. M. Smith, The effects of digital anesthesia on force control using a precision grip, Journal of neurophysiology 89 (2) (2003) 672–683. 

- [12] D. M. Wolpert, J. R. Flanagan, Motor prediction, Current biology 11 (18) (2001) R729–R732. 

- [13] K. Kilteni, H. H. Ehrsson, Sensorimotor predictions and tool use: Handheld tools attenuate self-touch, Cognition 165 (2017) 1–9. 

- [14] A.-S. Augurelle, A. M. Smith, T. Lejeune, J.-L. Thonnard, Importance of cutaneous feedback in maintaining a secure grip during manipulation of hand-held objects, Journal of neurophysiology 89 (2) (2003) 665–671. 

20 

- [15] B. Xu, L. Zhong, G. Zhang, X. Liang, D. Virtue, R. Madan, T. Bhattacharjee, Cushsense: Soft, stretchable, and comfortable tactile-sensing skin for physical human-robot interaction, in: IEEE International Conference on Robotics and Automation (ICRA), IEEE, 2024, pp. 5694–5701. 

- [16] D. Xu, A. Tairych, I. A. Anderson, Stretch not flex: programmable rubber keyboard, Smart Materials and Structures 25 (1) (2016) 015012. 

- [17] S. Stassi, V. Cauda, G. Canavese, C. F. Pirri, Flexible tactile sensing based on piezoresistive composites: A review, Sensors 14 (3) (2014) 5296–5332. 

- [18] S. Sundaram, P. Kellnhofer, Y. Li, J.-Y. Zhu, A. Torralba, W. Matusik, Learning the signatures of the human grasp using a scalable tactile glove, Nature 569 (7758) (2019) 698–702. 

- [19] Y. Yan, Z. Hu, Z. Yang, W. Yuan, C. Song, J. Pan, Y. Shen, Soft magnetic skin for super-resolution tactile sensing with force self-decoupling, Science Robotics 6 (51) (2021) eabc8801. 

- [20] W. Yuan, S. Dong, E. A. GelSight, High-resolution robot tactile sensors for estimating geometry and force., 2017, 17, 2762, DOI: https://doi. org/10.3390/s17122762. PMID: https://www. ncbi. nlm. nih. gov/pubmed/29186053. 

- [21] M. Lambeta, P.-W. Chou, S. Tian, B. Yang, B. Maloon, V. R. Most, D. Stroud, R. Santos, A. Byagowi, G. Kammerer, et al., Digit: A novel design for a low-cost compact high-resolution tactile sensor with application to in-hand manipulation, IEEE Robotics and Automation Letters 5 (3) (2020) 3838–3845. 

- [22] C. Higuera, A. Sharma, C. K. Bodduluri, T. Fan, P. Lancaster, M. Kalakrishnan, M. Kaess, B. Boots, M. Lambeta, T. Wu, et al., Sparsh: Selfsupervised touch representations for vision-based tactile sensing, arXiv preprint arXiv:2410.24090 (2024). 

- [23] R. Feng, J. Hu, W. Xia, T. Gao, A. Shen, Y. Sun, B. Fang, D. Hu, Anytouch: Learning unified static-dynamic representation across multiple visuo-tactile sensors, arXiv preprint arXiv:2502.12191 (2025). 

- [24] Z. Xu, R. Uppuluri, X. Zhang, C. Fitch, P. G. Crandall, W. Shou, D. Wang, Y. She, Unit: Data efficient tactile representation with generalization to unseen objects, IEEE Robotics and Automation Letters (2025). 

- [25] P. Esser, R. Rombach, B. Ommer, Taming transformers for highresolution image synthesis, in: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2021, pp. 12873–12883. 

- [26] F. Yang, C. Feng, Z. Chen, H. Park, D. Wang, Y. Dou, Z. Zeng, X. Chen, R. Gangopadhyay, A. Owens, et al., Binding touch to everything: Learning unified multimodal tactile representations, in: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2024, pp. 26340–26353. 

- [27] S. Yu, K. Lin, A. Xiao, J. Duan, H. Soh, Octopi: Object property reasoning with large tactile-language models, arXiv preprint arXiv:2405.02794 (2024). 

- [28] Y. Xie, M. Li, S. Li, X. Li, G. Chen, F. Ma, F. R. Yu, W. Ding, Universal visuo-tactile video understanding for embodied interaction, arXiv preprint arXiv:2505.22566 (2025). 

- [29] L. Zhang, Y. Wang, Y. Jiang, Tac3d: A novel vision-based tactile sensor for measuring forces distribution and estimating friction coefficient distribution, arXiv preprint arXiv:2202.06211 (2022). 

- [30] https://www.xenserobotics.com/product/367/detail/9 (2025). [31] https://www.dmrobot.com/en/product/p1/dm-tac-w.html (2025). [32] I. Guzey, Y. Dai, B. Evans, S. Chintala, L. Pinto, See to touch: Learning tactile dexterity through visual incentives, in: 2024 IEEE International Conference on Robotics and Automation (ICRA), IEEE, 2024, pp. 13825–13832. 

- [33] B. Ai, S. Tian, H. Shi, Y. Wang, C. Tan, Y. Li, J. Wu, Robopack: Learning tactile-informed dynamics models for dense packing, arXiv preprint arXiv:2407.01418 (2024). 

- [34] J. Huang, S. Wang, F. Lin, Y. Hu, C. Wen, Y. Gao, Tactile-vla: unlocking vision-language-action model’s physical knowledge for tactile generalization, arXiv preprint arXiv:2507.09160 (2025). 

- [35] Z. Zhang, H. Xu, Z. Yang, C. Yue, Z. Lin, H.-a. Gao, Z. Wang, H. Zhao, Ta-vla: Elucidating the design space of torque-aware vision-languageaction models, arXiv preprint arXiv:2509.07962 (2025). 

- [36] C. Higuera, S. Arnaud, B. Boots, M. Mukadam, F. Hogan, F. Meier, Visuo-tactile world models, ArXiv abs/2602.06001 (2026). URL https://api.semanticscholar.org/CorpusID:285303883 

- [37] S. Bien, C. Kneissl, T. J¨ulg, F. Fundel, T. Ressler-Antal, F. Walter, B. Ommer, G. Kutyniok, W. Burgard, Flowtouch: View-invariant visuotactile prediction, ArXiv abs/2603.08255 (2026). URL https://api.semanticscholar.org/CorpusID:286376577 

- [38] L. Fu, G. Datta, H. Huang, W. C.-H. Panitch, J. Drake, J. Ortiz, M. Mukadam, M. Lambeta, R. Calandra, K. Goldberg, A touch, vi- 

sion, and language dataset for multimodal alignment, arXiv preprint arXiv:2402.13232 (2024). 

- [39] H. Li, Y. Zhang, J. Zhu, S. Wang, M. A. Lee, H. Xu, E. Adelson, L. FeiFei, R. Gao, J. Wu, See, hear, and feel: Smart sensory fusion for robotic manipulation, arXiv preprint arXiv:2212.03858 (2022). 

- [40] H.-S. Fang, H. Fang, Z. Tang, J. Liu, C. Wang, J. Wang, H. Zhu, C. Lu, Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot, arXiv preprint arXiv:2307.00595 (2023). 

- [41] L. Wu, C. Yu, J. Ren, L. Chen, Y. Jiang, R. Huang, G. Gu, H. Li, Freetacman: Robot-free visuo-tactile data collection system for contactrich manipulation, arXiv preprint arXiv:2506.01941 (2025). 

- [42] Z. Cheng, Y. Zhang, W. Zhang, H. Li, K. Wang, L. Song, H. Zhang, Omnivtla: Vision-tactile-language-action model with semantic-aligned tactile sensing, arXiv preprint arXiv:2508.08706 (2025). 

- [43] Y. Xu, L. Wei, P. An, Q. Zhang, Y.-L. Li, exumi: Extensible robot teaching system with action-aware task-agnostic tactile representation, arXiv preprint arXiv:2509.14688 (2025). 

- [44] Z. Liu, J. Liu, J. Xu, N. Han, C. Gu, H. Chen, K. Zhou, R. Zhang, K. C. Hsieh, K. Wu, et al., Mla: A multisensory language-action model for multimodal understanding and forecasting in robotic manipulation, arXiv preprint arXiv:2509.26642 (2025). 

- [45] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, S. Song, Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots, arXiv preprint arXiv:2402.10329 (2024). 

- [46] P. Wu, Y. Shentu, Z. Yi, X. Lin, P. Abbeel, Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators, in: 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), IEEE, 2024, pp. 12156–12163. 

- [47] R. Gao, Z. Si, Y.-Y. Chang, S. Clarke, J. Bohg, L. Fei-Fei, W. Yuan, J. Wu, Objectfolder 2.0: A multisensory object dataset for sim2real transfer, in: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2022, pp. 10598–10608. 

- [48] T. Engelbracht, R. Zurbr¨ugg, M. Wohlrapp, M. B¨uchner, A. Valada, M. Pollefeys, H. Blum, Z. Bauer, Hoi!-a multimodal dataset for force-grounded, cross-view articulated manipulation, arXiv preprint arXiv:2512.04884 (2025). 

- [49] Z. Zhaxizhuoma, K. Liu, C. Guan, Z. Jia, Z. Wu, X. Liu, T. Wang, S. Liang, P. Chen, P. Zhang, et al., Fastumi: A scalable and hardwareindependent universal manipulation interface with dataset, in: Conference on Robot Learning, PMLR, 2025, pp. 3069–3093. 

- [50] Z. Xu, K. Sima, J. Deng, Z. Zhuang, C. Wang, C. Hao, J. S. Dong, Aprebot: Active perception system for reflexive evasion robot, arXiv preprint arXiv:2509.24733 (2025). 

- [51] Z. Xu, C. Hao, C. Wang, K. Sima, F. Shi, J. S. Dong, Rebot: Reflexive evasion robot for instantaneous dynamic obstacle avoidance, IEEE Robotics and Automation Letters 11 (2) (2025) 1746–1753. 

- [52] B. Cao, Y. Sun, P. Zhu, Q. Hu, Multi-modal gated mixture of localto-global experts for dynamic image fusion, in: Proceedings of the IEEE/CVF international conference on computer vision, 2023, pp. 23555–23564. 

- [53] V. Sitzmann, J. Martel, A. Bergman, D. Lindell, G. Wetzstein, Implicit neural representations with periodic activation functions, Advances in neural information processing systems 33 (2020) 7462–7473. 

- [54] C. Zhong, Y. Zheng, Y. Zheng, H. Zhao, L. Yi, X. Mu, L. Wang, P. Li, G. Zhou, C. Yang, et al., 3d implicit transporter for temporally consistent keypoint discovery, in: Proceedings of the IEEE/CVF international conference on computer vision, 2023, pp. 3869–3880. 

- [55] J. J. Park, P. Florence, J. Straub, R. Newcombe, S. Lovegrove, Deepsdf: Learning continuous signed distance functions for shape representation, in: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2019, pp. 165–174. 

- [56] X. Chen, Y. Zheng, Y. Zheng, Q. Zhou, H. Zhao, G. Zhou, Y.-Q. Zhang, Dpf: Learning dense prediction fields with weak supervision, in: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2023, pp. 15347–15357. 

- [57] H. Yu, H. Lin, J. Wang, J. Li, Y. Wang, X. Zhang, Y. Wang, X. Zhou, R. Hu, S. Peng, Infinidepth: Arbitrary-resolution and fine-grained depth estimation with neural implicit fields, arXiv preprint arXiv:2601.03252 (2026). 

- [58] D. P. Kingma, M. Welling, Auto-encoding variational bayes, arXiv preprint arXiv:1312.6114 (2013). 

- [59] W. Peebles, S. Xie, Scalable diffusion models with transformers, in: Proceedings of the IEEE/CVF international conference on computer vision, 2023, pp. 4195–4205. 

- [60] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, B. Ommer, Highresolution image synthesis with latent diffusion models, in: Proceedings 

21 

of the IEEE/CVF conference on computer vision and pattern recognition, 2022, pp. 10684–10695. 

- [61] Z. He, H. Fang, J. Chen, H.-S. Fang, C. Lu, Foar: Force-aware reactive policy for contact-rich robotic manipulation, IEEE Robotics and Automation Letters (2025). 

- [62] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, S. Song, Diffusion policy: Visuomotor policy learning via action diffusion, The International Journal of Robotics Research 44 (10-11) (2025) 1684–1704. 

- [63] M. Welling, Y. W. Teh, Bayesian learning via stochastic gradient langevin dynamics, in: Proceedings of the 28th international conference on machine learning (ICML-11), 2011, pp. 681–688. 

- [64] E. Perez, F. Strub, H. De Vries, V. Dumoulin, A. Courville, Film: Visual reasoning with a general conditioning layer, in: Proceedings of the AAAI conference on artificial intelligence, Vol. 32, 2018. 

- [65] W. Chen, J. Xu, F. Xiang, X. Yuan, H. Su, R. Chen, General-purpose sim2real protocol for learning contact-rich manipulation with markerbased visuotactile sensors, IEEE Transactions on Robotics 40 (2024) 1509–1526. 

- [66] S. Li, Y. Gao, D. Sadigh, S. Song, Unified video action model, arXiv preprint arXiv:2503.00200 (2025). 

- [67] W. Liu, J. Wang, Y. Wang, W. Wang, C. Lu, Forcemimic: Force-centric imitation learning with force-motion capture system for contact-rich manipulation, in: 2025 IEEE International Conference on Robotics and Automation (ICRA), IEEE, 2025, pp. 1105–1112. 

- [68] D. Zhang, C. Yuan, C. Wen, H. Zhang, J. Zhao, Y. Gao, Kinedex: Learning tactile-informed visuomotor policies via kinesthetic teaching for dexterous manipulation, arXiv preprint arXiv:2505.01974 (2025). 

