---
title: "OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception"
date: "2026-03-05"
authors: "Pei Qu; Zheng Li; Yufei Jia; Ziyun Liu; Liang Zhu; Haoang Li"
url: https://arxiv.org/abs/2603.05355
pdf: https://arxiv.org/pdf/2603.05355
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.05355)** / [論文ページ](https://arxiv.org/abs/2603.05355)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **OmniDP: Beyond-FOV Large-Workspace Humanoid Manipulation with Omnidirectional 3D Perception** 

Pei Qu<sup>1</sup><sup>_∗_</sup> , Zheng Li<sup>1</sup><sup>_∗_</sup> , Yufei Jia<sup>2</sup> , Ziyun Liu<sup>1</sup> , Liang Zhu<sup>1</sup> , Haoang Li<sup>1</sup> , Jinni Zhou<sup>1</sup> , Jun Ma<sup>1</sup><sup>_,_3</sup><sup>_†_</sup> 

**_Abstract_ — The deployment of humanoid robots for dexterous manipulation in unstructured environments remains challenging due to perceptual limitations that constrain the effective workspace. In scenarios where physical constraints prevent the robot from repositioning itself, maintaining omnidirectional awareness becomes far more critical than color or semantic information. While recent advances in visuomotor policy learning have improved manipulation capabilities, conventional RGB-D solutions suffer from narrow fields of view (FOV) and self-occlusion, requiring frequent base movements that introduce motion uncertainty and safety risks. Existing approaches to expanding perception, including active vision systems and third-view cameras, introduce mechanical complexity, calibration dependencies, and latency that hinder reliable real-time performance. In this work, We propose OmniDP, an end-to-end LiDAR-driven 3D visuomotor policy that enables robust manipulation in large workspaces. Our method processes panoramic point clouds through a TimeAware Attention Pooling mechanism, efficiently encoding sparse 3D data while capturing temporal dependencies. This 360° perception allows the robot to interact with objects across wide areas without frequent repositioning. To support policy learning, we develop a whole-body teleoperation system for efficient data collection on full-body coordination. Extensive experiments in simulation and real-world environments show that OmniDP achieves robust performance in large-workspace and cluttered scenarios, outperforming baselines that rely on egocentric depth cameras.** 

## I. INTRODUCTION 

Humanoid robots capable of dexterous manipulation in unstructured environments have long been a central goal in robotics. Recent advances in visuomotor policy learning, particularly imitation learning [1]–[3] and diffusion-based action generation [4]–[6], have substantially enhanced humanoids’ ability to learn manipulation skills directly from visual observations. By learning end-to-end sensorimotor mappings, these policies bypass explicit state estimation and task-specific modeling, enabling flexible skill acquisition across embodiments [7]. This progress opens opportunities for deploying humanoid robots in service robotics [8], household assistance [9], and collaborative human–robot interaction [10]. 

Despite recent advances in visuomotor policies, perceptual limitations persist in humanoid robots operating in unstruc- 

*Equal contribution, †Corresponding Author. 

> 1The Hong Kong University of Science and Technology (Guangzhou). _{_ pqu458, zli514, zliu176, lzhu686 _}_ @connect.hkust-gz.edu.cn, _{_ haoangli, eejinni, eejma _}_ @hkust-gz.edu.cn 

> 2Tsinghua University. jyf23@mails.tsinghua.edu.cn, zhouguyue@air.tsinghua.edu.cn 

> 3The Hong Kong University of Science and Technology. jun.ma@ust.hk 


Fig. 1: **OmniDP.** (a) The narrow field of view of RGB-D cameras prevents perception of objects outside visual range, causing task failures and collisions in space-constrained environments where robot repositioning is difficult; (b) by utilizing panoramic 3D LiDAR perception, our approach empowers humanoid robots with the capability to perform manipulation tasks across a large workspace, including areas outside the camera’s visual blind spots. 

tured environments. In scenarios where the robot’s base is restricted in movement and rotation due to physical constraints, target objects may remain undetected by conventional RGBD cameras, thereby limiting the effective workspace to what is immediately visible [1], [11]. In these ”viewpoint-limited” cases imposed by standard visual sensors, omnidirectional awareness becomes more critical than color or semantic information. Mainstream RGB-D solutions rely on singleview input, which suffers from a narrow field of view (FOV) and self-occlusion [12]–[14]. Moreover, the commonly used depth-to-point-cloud approach, while providing 3D geometry, remains inherently viewpoint-constrained [15]. Even introducing third-view cameras fails to resolve this, as they depend on extrinsic calibration and struggle with camera pose generalization [16], [17]. These limitations hinder the reliable deployment of humanoid robots for large-workspace, continuous operations in unstructured environments. 

Several approaches have been explored to expand the 

effective workspace for robotic manipulation. Active vision systems, which adjust viewpoint through camera motion, can in principle extend perception range [18]–[20]. However, for humanoid robots, this often requires additional degrees of freedom in the head or neck, introducing mechanical complexity, higher costs, and control overhead. Moreover, active movements may interfere with ongoing task execution and introduce latency, limiting real-time performance. Panoramic sensors, including 360<sup>_◦_</sup> cameras and LiDAR, provide wide horizontal fields of view without mechanical motion. Although they have shown promise in autonomous driving [21], [22], navigation [23]–[25], and locomotion [26], their use in end-to-end visuomotor manipulation for humanoid robots remains under-explored, representing a gap in enabling largeworkspace manipulation tasks [25], [27], [28]. 

To overcome these challenges, we propose a novel method for robust, large-workspace humanoid manipulation. First, we introduce **OmniDP** , an end-to-end LiDAR-driven 3D visuomotor policy that processes panoramic point clouds with a Time-Aware Attention Pooling mechanism, enabling efficient encoding of sparse 3D data while capturing temporal dependencies. This design expands the effective manipulation space through 360° perception, allowing the robot to perceive and interact with objects located outside the camera’s FOV without frequent repositioning, as demonstrated in Fig. 1. Second, to support policy learning in this setting, we develop a whole-body teleoperation system tailored for humanoid robots, enabling efficient collection of largeworkspace demonstration data that captures complex fullbody coordination. Extensive experiments demonstrate that our method achieves robust performance in large-workspace scenarios requiring extended spatial coverage, as well as in cluttered environments where panoramic perception is essential for collision-free manipulation, consistently outperforming vision-based baselines. 

Our core contributions are summarized as follows: 

- We propose OmniDP, an end-to-end LiDAR-driven 3D visuomotor policy with time-aware encoding of panoramic point clouds, enabling beyond-FOV largeworkspace humanoid manipulation. 

- We develop a whole-body teleoperation system that enables efficient collection of human demonstration data involving coordinated whole-body movements. 

- We validate our method through extensive experiments in simulation and the real world, demonstrating robust large-workspace and omnidirectional collision-free manipulation in challenging environments. 

## II. RELATED WORK 

## _A. Visuomotor Policy_ 

Recent progress in robot learning has been driven by visuomotor policies that map visual observations to actions, with approaches varying by representation type: 2D RGB, 2.5D RGB-D, and 3D point clouds. 

**Approaches with 2D and 2.5D Visual Inputs.** Diffusion Policy [4] pioneered the integration of diffusion models into 

robotic policy learning, generating action sequences from RGB observations to enable multimodal behavior synthesis in complex scenarios. Beyond imitation learning, visionbased reinforcement learning has also achieved significant progress in real-world settings [29], [30]. RGB-D observations, by incorporating depth information, provide geometric perception for contact-rich dexterous manipulation tasks. For instance, monocular metric depth alignment methods [31] can recover 3D scene structure without requiring dense depth annotations. However, constrained by fixed viewpoints and limited observation ranges, these methods are typically applicable only to local manipulation areas and struggle to develop a comprehensive global 3D scene understanding. 

**Approaches with 3D Visual Inputs.** Approaches with 3D Visual Inputs. In contrast to 2D methods, point cloud representations explicitly encode 3D spatial geometry, offering richer structural information for complex manipulation tasks. 3D Diffusion Policy (DP3) [5] successfully extended diffusion models to point cloud representations, with subsequent research applying this framework to humanoid robotic manipulation [6]. Regarding robustness, notable progress has been made through techniques such as implicit scene supervision [32] and variational regularization [33]. Addressing the challenge of viewpoint sensitivity, ManiVID-3D [34] learns view-invariant representations via feature disentanglement, significantly enhancing model generalization across multiple viewpoints. Nevertheless, current mainstream methods still rely on point clouds acquired from fixed RGB-D cameras, inheriting limited fields of view and requiring accurate extrinsic calibration for reliable 3D reconstruction. 

## _B. LiDAR-based Perception_ 

LiDAR is an increasingly adopted exteroceptive modality for legged and humanoid robots due to its illumination invariance and reliable 3D geometry, supporting both reactive control and long-horizon autonomy. 

Omni-Perception [26] learns omnidirectional collision avoidance for legged locomotion by consuming temporal LiDAR point clouds and directly producing control actions, reducing reliance on hand-crafted intermediate maps and emphasizing sim-to-real transfer with LiDAR-centric simulation support. LVI-Q [35] tightly couples LiDAR with vision, inertial, and kinematic cues to obtain robust odometry on quadrupeds, mitigating drift under aggressive motion and partial observability, and providing a reliable state estimate for downstream navigation. BeamDojo [36] targets agile humanoid locomotion on sparse footholds and leverages onboard LiDAR-based elevation mapping at deployment time, demonstrating the practical utility of structured terrain maps for precise stepping. PILOT [37] uses LiDAR as the sole external sensor input for environment perception. While LiDAR-based perception has demonstrated promising applications in locomotion and navigation, its potential in humanoid manipulation remains largely unexplored, particularly in tasks that demand large workspace operation and omnidirectional obstacle avoidance during arm deployment. 

## III. METHOD 

## _A. System Overview_ 

In this section, we present a framework that enables large-workspace manipulation for humanoid robots through omnidirectional 3D perception. To overcome the viewpoint constraints of conventional visuomotor policies, our approach leverages panoramic LiDAR observations within an imitation learning pipeline. We first develop a whole-body teleoperation system for efficient collection of demonstration data. We then train OmniDP, an end-to-end visuomotor policy that processes historical sequences of panoramic point clouds using a time-aware encoding mechanism. The system overview is provided in Fig. 2. 

## _B. OmniDP_ 

**Architecture of OmniDP.** OmniDP comprises a perception encoder and an action decoder. The encoder processes panoramic point clouds using a pyramid convolutional encoder [6] enhanced with time-aware attention, producing a compact global feature that captures both spatial structure and temporal context. This feature conditions a Diffusion Policy [4] decoder, which iteratively denoises random noise into coordinated action sequences. The end-to-end framework directly maps omnidirectional observations to wholebody actions without intermediate state estimation. 

**Omnidirectional Perception for Large-Workspace Manipulation.** Most existing 3D visuomotor policies operate on third-view [5] or egocentric [6] point clouds from depth cameras, which suffer from a narrow field of view. This restricts the effective manipulation space to the camera’s immediate vicinity, forcing frequent repositioning when objects are distributed across a wider area. As illustrated in Fig. 3, which compares the visual coverage of LiDAR and RGB-D cameras, we instead adopt panoramic LiDAR to capture complete 360° point clouds at each timestep. This provides full spatial awareness of the robot’s surroundings, enabling it to reach and manipulate objects anywhere around its body without moving. It also allows collision-free bimanual coordination in cluttered environments by maintaining continuous awareness of surrounding obstacles throughout task execution. 

**Time-Aware Attention Pooling (TAP).** Point clouds generated by LiDAR sensors are often sparse and temporally flickering, making standard global max pooling over singleframe observations unstable. To enhance robustness, we introduce a time-aware attention pooling mechanism for point cloud encoding. Specifically, we aggregate point clouds over a short temporal window and augment each point with a normalized relative timestamp. Per-point spatial features are extracted using a point cloud encoder, while a small MLP predicts attention weights conditioned on the temporal offsets, encouraging the model to emphasize more recent observations. The final global feature is computed as a weighted sum over all points, yielding a temporally smoothed representation that improves stability for policy learning. 

**Point Cloud Processing.** Raw panoramic LiDAR point clouds exhibit non-uniform density, with points densely 

distributed near the sensor and sparse at a distance. To ensure sufficient point density for nearby objects within the robot’s manipulation range while maintaining real-time inference efficiency, we design a lightweight preprocessing pipeline. Specifically, we crop out points beyond 1.3 meters from the Lidar sensor based on the robot’s arm reachability prior, where the sparse sampling provides limited utility for manipulation tasks. The remaining points are then uniformly downsampled to 4096 points per frame, balancing geometric fidelity with computational efficiency for 3D encoding. 

**Learning and Deployment.** We train OmniDP using human demonstration data collected via the whole-body teleoperation system described in Sec. III-C. To achieve coordinated whole-body control, the model takes as input the 43dimensional joint states covering all joints of the humanoid as proprioceptive information, together with panoramic point clouds from the head-mounted LiDAR as visual perception. The supervision target is the 28-dimensional joint angles of the upper body, including arms and dexterous hands. During deployment, the learned policy generates commands only for the upper-body joints, while the lower body and waist are controlled by a pre-trained HOMIE [38] algorithm for stable locomotion. Notably, our point clouds are represented in the LiDAR’s egocentric frame, which eliminates the need for extrinsic calibration during deployment and enhances the adaptability of the policy across different environments. 

## _C. Whole-body Teleoperation System_ 

**Hardware Configuration.** We deploy a Unitree G1 humanoid robot featuring 29-DoF body and two 7-DoF Dex31 dexterous hands, resulting in 43 actively controlled joints. Unlike upper-body-only configurations, all joints including legs, waist, arms, and hands remain enabled during operation. This full-body actuation allows coordinated locomanipulation behaviors and natural motion execution during teleoperation. 

**Panoramic Lidar Perception.** Our perception system centers on a head-mounted Livox MID-360 LiDAR, rigidly installed to align with the operator’s egocentric viewpoint and provide panoramic 3D observations. The LiDAR provides a 360<sup>_◦_</sup> horizontal and _−_ 7<sup>_◦_</sup> to 52<sup>_◦_</sup> vertical field-ofview (FoV), generating up to 200k points per second at 10 Hz. The wide FoV and non-repetitive scanning pattern improve spatial coverage within short temporal windows, which enhances geometric consistency in cluttered indoor environments. Instead of relying on multi-camera fusion or structured-light depth sensors, we directly utilize raw LiDAR point clouds as the primary visual input modality. In simulation, the technology stack of LiDAR is based on DISCOVERSE [39], enabling realistic panoramic point cloud generation. 

**Lightweight Whole-body Teleoperation Device.** To enable large-scale data acquisition, we build upon the HOMIE [38] loco-manipulation framework, adapting it to support immersive XR-based teleoperation on the Unitree G1. Rather than using isomorphic exoskeleton hardware, our system requires only a standard head-mounted display (HMD) and 


Fig. 2: **Overview of system architecture.** Our system consists of four key components: (i) the panoramic perception hardware platform based on a Unitree G1 humanoid robot equipped with a Mid-360 LiDAR; (ii) a whole-body teleoperation system for efficient demonstration data collection; (iii) an end-to-end visuomotor policy learning method leveraging omnidirectional 3D perception with time-aware encoding; and (iv) real-world deployment enabling large-workspace manipulation and omnidirectional obstacle avoidance. 


Fig. 3: **Comparison of the field of views of LiDAR and camera.** (a) The panoramic LiDAR provides 360° horizontal coverage, significantly surpassing the narrow field of view of the head-mounted RGB-D camera. (b) This enables the robot to perceive global scene context and locate target objects even when they lie outside the camera’s visual blind spots, which is essential for large-workspace manipulation tasks. 

handheld XR (VR and AR) controllers (Meta Quest 3). This significantly simplifies deployment while retaining fullbody controllability. The operator’s head motion defines the reference frame for perception, while controller poses specify target end-effector poses. Locomotion and torso adjustments are commanded via joystick inputs, enabling simultaneous manipulation and base motion. 

**Task-Space Upper Limb Control.** Given target wrist poses from the XR interface, upper limb motion is generated through constrained inverse kinematics (IK). Each arm is modeled as a 7-DoF serial chain derived from the Unitree G1 URDF file. Instead of employing classical Jacobian pseudoinverse methods, we formulate IK as a constrained nonlinear optimization problem. The objective balances: 1) task-space position and orientation tracking, 2) joint regularization, and 3) temporal smoothness. Joint position limits are explicitly imposed as bound constraints. 

The optimization is solved using interior point optimizer, 

yielding stable and physically consistent joint configurations even under redundant and multi-objective settings. The optimized configuration _q_<sup>_∗_</sup> is forwarded to the low-level joint controller for execution. 

**Motion Mapping.** Controller poses relative to the HMD frame are mapped to robot end-effector targets through rigidbody transformations in _SE_ (3): 


Locomotion commands are defined as 


where _vx,k_ and _vy,k_ denote planar velocities, ∆ _θk_ denotes the yaw increment, and _hk_ denotes the torso height adjustment. This formulation enables coordinated base motion during manipulation. 

TABLE I: **Performance comparison.** Our method consistently outperforms existing RGB-based and depth-to-point-cloud baselines across all simulated and real-world tasks, with particularly significant advantages in scenarios where target objects lie outside the camera’s field of view. 

|Simulation<br><br><br>||Real World<br><br><br><br>|
|---|---|---|
|Method<br>Pick & Place<br>Pour (OV)|Pick & Place|Hand Over (OV)<br>Pour (OV)<br>Wipe (OV)<br>Total|
|DP<br>10/20<br>0/20<br>DP3<br>13/20<br>0/20<br>iDP3<br>14/20<br>0/20|8/20<br>9/20<br>11/20|0/20<br>0/20<br>0/20<br>18/120<br>0/20<br>0/20<br>0/20<br>22/120<br>0/20<br>0/20<br>0/20<br>25/120|
|**Ours**<br>**16/20**<br>**12/20**|**15/20**|**12/20**<br>**11/20**<br>**16/20**<br>**82/120**|
|Pick and Plac||Ou~~t~~o~~f~~ <br>Vie<br>Pick and Plac|
|Pou||Handove|
|Fig. 4: **Simulation experiments and sna**<br>uate OmniDP on two simulated tasks, <br>effectiveness in large-workspace manipulat<br>panoramic perception.<br>**Data Collection.** During teleoperation<br>chronizedobservation–actiontrajectories|**pshots.** We eval-<br>demonstrating its<br>ion scenarios with<br>, we record syn-<br>Observationscon-|Pou<br>Wip|


Fig. 4: **Simulation experiments and snapshots.** We evaluate OmniDP on two simulated tasks, demonstrating its effectiveness in large-workspace manipulation scenarios with panoramic perception. 

**Data Collection.** During teleoperation, we record synchronized observation–action trajectories. Observations consist of real-time processed LiDAR point clouds (distancebased cropping and uniform downsampling) and the 43DoF proprioceptive joint positions. We utilize the TeleVuer open-source framework to establish real-time communication between the XR device and the controlled robot, supporting interactive teleoperation under high-throughput visual data streams, such as high-density 3D point clouds. Unlike image-centric pipelines, our dataset preserves full 3D spatial structure, enabling downstream policy learning directly in geometric space. 

Fig. 5: **Real-world experiments and snapshots.** We further validate OmniDP on four real-world tasks, confirming its robust performance in real-world environments and out-ofview manipulation scenarios. 

backbone but differ in their visual observation modalities and encoder architectures. By benchmarking under a unified diffusion framework, we aim to systematically examine how variations in visual input representation and feature encoding influence policy performance, particularly in scenarios requiring panoramic or large-scale spatial perception. Task success rate is adopted as the primary evaluation metric. It is important to note that the comparison with DP / DP3 / iDP3 is not intended to demonstrate the superiority of our algorithm, but rather to validate the impact of the ‘FOV limitation’. 

## IV. EXPERIMENTS 

**Tasks.** In simulation, we design two simulation tasks using the MuJoCo [40] physics engine: (1) Pick & Place, and (2) Pour (OV), as shown in Fig. 4. These tasks are constructed to require large-scale spatial awareness, where critical objects and interactions frequently occur outside the field of view of a fixed camera, leading to partial observability. To further validate our approach in real-world settings, we additionally introduce two tasks, (3) Hand Over (OV), and (4) Wipe (OV), as shown in Fig. 5. Tasks marked with “OV” (Out of View) require panoramic spatial awareness, where key objects may lie outside the field of view of a fixed camera. 

**Robot Setup.** All experiments are conducted on a Unitree G1 humanoid platform equipped with Unitree Dex3-1 powercontrolled dexterous hands. A Livox MID-360 LiDAR and an Intel RealSense D435i camera are rigidly mounted on the robot head for exteroceptive perception. Point clouds are obtained either directly from the LiDAR or converted from depth images via camera intrinsics. During policy deployment, all 29 DoFs of the robot are fully actuated, 

**Baselines.** We evaluate our approach against three diffusion-based manipulation policies: DP [4], DP3 [5], and iDP3 [6]. These methods share a common diffusion-policy 

TABLE II: **Collision-free manipulation evaluation.** Results demonstrate that OmniDP achieves robust omnidirectional obstacle avoidance in cluttered environments. 

|Method|Success Rate _↑_|Collision Rate _↓_|
|---|---|---|
|DP|0/20|20/20|
|DP3|0/20|18/20|
|iDP3|0/20|18/20|
|**Ours**|**14/20**|**5/20**|


comprising 14 DoFs in the arms, 3 DoFs in the waist, and 12 DoFs in the legs. 

**Evaluation Metrics.** We evaluate all methods primarily by task success rate. For each task, we run each model 20 times under consistent initial conditions and report the number of successful trials. For collision-free manipulation tasks conducted in cluttered environments, we additionally report the collision rate, defined as the proportion of trials where the robot makes physical contact with surrounding obstacles during execution. This metric captures the robot’s ability to leverage environmental awareness for safe wholebody coordination, complementing the success rate which focuses on task completion. 

## _A. Effectiveness of OmniDP_ 

We evaluate the effectiveness of OmniDP by comparing it with three diffusion-based visuomotor baselines: Diffusion Policy (DP) [4] operating on 240 × 424 RGB images, DP3 [5] and iDP3 [6], both using point clouds derived from depth cameras (camera-frame coordinates, downsampled to 4096 points). All methods are tested on two simulated tasks and four real-world tasks, with success rates reported in Table I. For tasks where target objects are located outside the camera’s field of view (denoted OV), all baselines largely fail due to their limited perceptual coverage. In contrast, OmniDP leverages its omnidirectional 360° perception to achieve robust large-workspace manipulation, reaching objects anywhere in the surroundings while maintaining full environmental awareness. For in-view tasks such as Pick & Place, OmniDP also outperforms the baselines, benefiting from panoramic perception that provides comprehensive scene context for better obstacle avoidance and spatial reasoning, while the time-aware encoding mechanism enhances temporal stability by mitigating transient sensor noise. 

## _B. Collision-Free Manipulation Evaluation_ 

We further evaluate the obstacle avoidance capability of each method during task execution. In this experiment, we place a physical obstacle along the robot’s manipulation path, positioned outside the field of view of the head-mounted RGB-D camera, as illustrated in Fig. 6(a). This setup challenges the policy to perceive and avoid obstacles that are not visible to standard egocentric vision but are captured by panoramic LiDAR. We compare OmniDP against the three baselines in terms of success rate and collision rate, 

TABLE III: **Generalization capability evaluation.** Results demonstrate that OmniDP maintains consistently high success rates across varying object instances, lighting conditions, and cluttered scenes. 

|Method|Instance|Lighting|Scene|
|---|---|---|---|
|DP|3/20|4/20|2/20|
|DP3|7/20|8/20|7/20|
|iDP3|12/20|12/20|10/20|
|**Ours**|**13/20**|**15/20**|**12/20**|


with results reported in Table II. OmniDP demonstrates robust performance and effective omnidirectional obstacle avoidance, successfully completing tasks while avoiding collisions in most trials. In contrast, all baselines largely fail to complete the task, frequently colliding with the obstacle due to their inability to perceive objects outside the limited camera field of view. These results highlight the importance of panoramic perception for safe whole-body manipulation in cluttered environments. 

## _C. Generalization Capability Evaluation_ 

We also assess the generalization ability of OmniDP under varying environmental conditions. Specifically, we test on the Pick & Place task, the setting where all baselines achieve reasonable performance under nominal conditions, and introduce three types of variations: (1) different object instances with diverse shapes and sizes, (2) changing lighting conditions, and (3) cluttered scenes with distractor objects placed around the workspace, as depicted in Fig. 6(b)-(d). Success rates for each variant are reported in Table III. While baseline methods experience noticeable performance drops due to their reliance on narrow-view RGB-D inputs and sensitivity to visual perturbations, OmniDP maintains consistently high success rates across all variations. This robustness stems from its panoramic scene understanding, which provides comprehensive spatial context and is inherently less affected by lighting changes or local clutter, enabling reliable operation in diverse real-world scenarios. 

## _D. Ablation Study_ 

We conduct ablation studies to validate the key components of OmniDP: omnidirectional perception and the timeaware attention pooling (TAP) mechanism. Experiments are performed on the Hand Over task, which demands largeworkspace coordination and spatial awareness. As reported in Table IV, removing the panoramic LiDAR input (i.e., relying solely on egocentric depth-based point clouds) leads to complete task failure, highlighting the critical role of 360° scene understanding for such tasks. Furthermore, disabling TAP results in a noticeable decrease in success rate, indicating that temporal smoothing via attention over historical point clouds contributes to more stable policy execution. These results confirm that both panoramic perception and temporal encoding are essential for reliable large-workspace manipulation. 


Fig. 6: **Capabilities evaluation.** We test OmniDP under diverse challenging conditions: (a) omnidirectional obstacle avoidance, where obstacles are placed outside the camera’s field of view; (b) varying object instances with different shapes and sizes; (c) changing lighting conditions, including low-light and complex lighting; and (d) cluttered environments with multiple distractor objects. 

TABLE IV: **Ablation study.** The results confirm the necessity of the designed components. 

|Ablation|Success Rate|
|---|---|
|OmniDP|12/20|
|w/o Omni. Obs.|0/20|
|w/o TAP|9/20|


## V. CONCLUSION 

In this paper, we present OmniDP, an end-to-end LiDARdriven visuomotor policy for large-workspace humanoid dexterous manipulation on humanoid robots. By leveraging panoramic LiDAR observations with a time-aware attention pooling mechanism, our approach overcomes the fundamental perceptual limitations of conventional RGB-D based policies, enabling 360° scene awareness and collision-free manipulation in cluttered environments. We also introduce a whole-body teleoperation system for efficient collection of demonstration data involving complex full-body motions. 

Extensive experiments in both simulation and real-world settings demonstrate that OmniDP achieves robust performance across large-workspace tasks and out-of-view manipulation scenarios, significantly outperforming vision-based baselines. Ablation studies further validate the importance of panoramic perception and temporal encoding for reliable deployment. We believe that integrating omnidirectional 3D perception into visuomotor policy learning offers a promising direction toward humanoid robots capable of operating safely and dexterously in unstructured real-world environments. 

**Future Work.** Future work will extend the system toward whole-body autonomy, leveraging LiDAR to perceive targets beyond the camera’s field of view and using locomotion for active viewpoint acquisition. We also plan to incorporate multi-modal sensing by integrating LiDAR geometry, RGB semantics, and tactile feedback. On the control side, augmenting diffusion policy with reinforcement learning represents a promising direction to improve action refinement and adaptability. Strengthening the policy’s generalization and zero-shot performance on unseen objects, layouts, and tasks will be another key step toward reliable deployment in real-world environments. 

## REFERENCES 

- [1] Z. Fu, T. Z. Zhao, and C. Finn, “Mobile Aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation,” _arXiv preprint arXiv:2401.02117_ , 2024. 

- [2] J. Liang, R. Liu, E. Ozguroglu, S. Sudhakar, A. Dave, P. Tokmakov, S. Song, and C. Vondrick, “Dreamitate: Real-world visuomotor policy learning via video generation,” _arXiv preprint arXiv:2406.16862_ , 2024. 

- [3] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa, “Visual imitation enables contextual humanoid control,” _arXiv preprint arXiv:2505.03729_ , 2025. 

- [4] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion Policy: Visuomotor policy learning via action diffusion,” _The International Journal of Robotics Research_ , vol. 44, no. 10-11, pp. 1684–1704, 2025. 

- [5] Y. Ze, G. Zhang, K. Zhang, C. Hu, M. Wang, and H. Xu, “3D Diffusion Policy: Generalizable visuomotor policy learning via simple 3d representations,” _arXiv preprint arXiv:2403.03954_ , 2024. 

- [6] Y. Ze, Z. Chen, W. Wang, T. Chen, X. He, Y. Yuan, X. B. Peng, and J. Wu, “Generalizable humanoid manipulation with 3D diffusion policies,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 2873–2880, 2025. 

- [7] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, _et al._ , “Octo: An open-source generalist robot policy,” _arXiv preprint arXiv:2405.12213_ , 2024. 

- [8] H. Lef`evre, T. Chaki, T. Kawakami, A. Tanguy, T. Yoshiike, and A. Kheddar, “Humanoid-human sit-to-stand-to-sit assistance,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 2, pp. 1521–1528, 2024. 

- [9] Y. Jiang, R. Zhang, J. Wong, C. Wang, Y. Ze, H. Yin, C. Gokmen, S. Song, J. Wu, and L. Fei-Fei, “Behavior robot suite: Streamlining real-world whole-body manipulation for everyday household activities,” _arXiv preprint arXiv:2503.05652_ , 2025. 

- [10] Y. Du, Y. Li, B. Jia, Y. Lin, P. Zhou, W. Liang, Y. Yang, and S. Huang, “Learning human-humanoid coordination for collaborative object carrying,” _arXiv preprint arXiv:2510.14293_ , 2025. 

- [11] X. Xu, D. Bauer, and S. Song, “Robopanoptes: The all-seeing robot with whole-body dexterity,” _arXiv preprint arXiv:2501.05420_ , 2025. 

- [12] Y. Tian, J. Zhang, Z. Yin, and H. Dong, “Robot structure prior guided temporal attention for camera-to-robot pose estimation from image sequence,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 8917–8926, 2023. 

- [13] S. Tian, B. Wulfe, K. Sargent, K. Liu, S. Zakharov, V. Guizilini, and J. Wu, “View-invariant policy learning via zero-shot novel view synthesis,” _arXiv preprint arXiv:2409.03685_ , 2024. 

- [14] J. Kerr, C. M. Kim, M. Wu, B. Yi, Q. Wang, K. Goldberg, and A. Kanazawa, “Robot see robot do: Imitating articulated object manipulation with monocular 4D reconstruction,” _arXiv preprint arXiv:2409.18121_ , 2024. 

- [15] S. Peri, I. Lee, C. Kim, L. Fuxin, T. Hermans, and S. Lee, “Point cloud models improve visual robustness in robotic learners,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 17529–17536, 2024. 

- [16] C. Acar, K. Binici, A. Tekirda˘g, and Y. Wu, “Visual-policy learning through multi-camera view to single-camera view knowledge distillation for robot manipulation tasks,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 1, pp. 691–698, 2023. 

- [17] Y. Zhang, J. Xu, and W. Ren, “PLK-Calib: Single-shot and targetless LiDAR-camera extrinsic calibration using pl¨ucker lines,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 16091–16097, 2025. 

- [18] H. Xiong, X. Xu, J. Wu, Y. Hou, J. Bohg, and S. Song, “Vision in action: Learning active perception from human demonstrations,” _arXiv preprint arXiv:2506.15666_ , 2025. 

- [19] J. Yu, Y. Shentu, D. Wu, P. Abbeel, K. Goldberg, and P. Wu, “Egomi: Learning active vision and whole-body manipulation from egocentric human demonstrations,” _arXiv preprint arXiv:2511.00153_ , 2025. 

- [20] I. Chuang, A. Lee, D. Gao, M.-M. Naddaf-Sh, and I. Soltani, “Active vision might be all you need: Exploring active vision in bimanual robotic manipulation,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 7952–7959, 2025. 

- [21] E. Wenke, C. Yuan, L. Li, Y. Sun, Y. F. A. Gaus, A. AtapourAbarghouei, and T. P. Breckon, “Dur360BEV: A real-world 360degree single camera dataset and benchmark for bird-eye view mapping in autonomous driving,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 3737–3744, 2025. 

- [22] S. Yogamani, D. Unger, V. Narayanan, and V. R. Kumar, “Fisheyebevseg: Surround view fisheye cameras based bird’s-eye view segmentation for autonomous driving,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 1331– 1334, 2024. 

- [23] W. Xie, G. Chu, Q. Qian, Y. Yu, S. Zhai, D. Chen, N. Wang, H. Bao, and G. Zhangv, “Omnidirectional dense slam for back-to-back fisheye cameras,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 1653–1660, 2024. 

- [24] Y. Zhang, S. Ahmadi, J. Kang, Z. Arjmandi, and G. Sohn, “YUTO MMS: A comprehensive slam dataset for urban mobile mapping with tilted lidar and panoramic camera integration,” _The International Journal of Robotics Research_ , vol. 44, no. 1, pp. 3–21, 2025. 

- [25] J. Lee, M. Bjelonic, A. Reske, L. Wellhausen, T. Miki, and M. Hutter, “Learning robust autonomous navigation and locomotion for wheeledlegged robots,” _Science Robotics_ , vol. 9, no. 89, p. eadi9641, 2024. 

- [26] Z. Wang, T. Ma, Y. Jia, X. Yang, J. Zhou, W. Ouyang, Q. Zhang, and J. Liang, “Omni-Perception: Omnidirectional collision avoidance 

for legged locomotion in dynamic environments,” _arXiv preprint arXiv:2505.19214_ , 2025. 

- [27] A.-C. Cheng, Y. Ji, Z. Yang, Z. Gongye, X. Zou, J. Kautz, E. Bıyık, H. Yin, S. Liu, and X. Wang, “Navila: Legged robot vision-languageaction model for navigation,” _arXiv preprint arXiv:2412.04453_ , 2024. 

- [28] Z. Wang, X. Yang, J. Zhao, J. Zhou, T. Ma, Z. Gao, A. Ajoudani, and J. Liang, “End-to-end humanoid robot safe and comfortable locomotion policy,” _arXiv preprint arXiv:2508.07611_ , 2025. 

- [29] T. Lin, K. Sachdev, L. Fan, J. Malik, and Y. Zhu, “Sim-to-real reinforcement learning for vision-based dexterous manipulation on humanoids,” _arXiv preprint arXiv:2502.20396_ , 2025. 

- [30] A. Maddukuri, Z. Jiang, L. Y. Chen, S. Nasiriany, Y. Xie, Y. Fang, W. Huang, Z. Wang, Z. Xu, N. Chernyadev, _et al._ , “Sim-and-real cotraining: A simple recipe for vision-based robotic manipulation,” _arXiv preprint arXiv:2503.24361_ , 2025. 

- [31] T. Guo, B. Huang, and J. Yu, “Monocular one-shot metric-depth alignment for rgb-based robot grasping,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 642–649, 2025. 

- [32] W. Xia, J. Zhang, C. Zhang, Y. Wang, Y. Gong, and J. Mei, “ISS Policy: Scalable diffusion policy with implicit scene supervision,” _arXiv preprint arXiv:2512.15020_ , 2025. 

- [33] J. Zhang, W. Xia, Y. Wang, Z. Zhou, H. Li, Y. Lai, H. Song, Y. Gong, and J. Me, “Information filtering via variational regularization for robot manipulation,” _arXiv preprint arXiv:2601.21926_ , 2026. 

- [34] Z. Li, P. Qu, Y. Jia, S. Zhou, H. Ge, J. Cao, J. Zhou, G. Zhou, and J. Ma, “ManiVID-3D: Generalizable view-invariant reinforcement learning for robotic manipulation via disentangled 3D representations,” _arXiv preprint arXiv:2509.11125_ , 2025. 

- [35] K. C. Marsim, M. Oh, B. Yu, S. Lee, I. M. A. Nahrendra, H. Lim, and H. Myung, “LVI-Q: Robust lidar-visual-inertial-kinematic odometry for quadruped robots using tightly-coupled and efficient alternating optimization,” _IEEE Robotics and Automation Letters_ , 2025. 

- [36] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “BeamDojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv preprint arXiv:2502.10363_ , 2025. 

- [37] X. Cui, L. Feng, Y. Zhou, H. Han, Z. Liu, and H. Wang, “PILOT: A perceptive integrated low-level controller for loco-manipulation over unstructured scenes,” _arXiv preprint arXiv:2601.17440_ , 2026. 

- [38] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “HOMIE: Humanoid loco-manipulation with isomorphic exoskeleton cockpit,” _arXiv preprint arXiv:2502.13013_ , 2025. 

- [39] Y. Jia, G. Wang, Y. Dong, J. Wu, Y. Zeng, H. Lin, Z. Wang, H. Ge, W. Gu, K. Ding, _et al._ , “DISCOVERSE: Efficient robot simulation in complex high-fidelity environments,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 6272–6279, 2025. 

- [40] E. Todorov, T. Erez, and Y. Tassa, “MuJoCo: A physics engine for model-based control,” in _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pp. 5026–5033, 2012. 

