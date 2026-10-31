---
title: "Now You See That: Learning End-to-End Humanoid Locomotion from Raw Pixels"
date: "2026-02-06"
authors: "Wandong Sun; Yongbo Su; Leoric Huang; Alex Zhang; Dwyane Wei; Mu San"
url: https://arxiv.org/abs/2602.06382
pdf: https://arxiv.org/pdf/2602.06382
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.06382)** / [論文ページ](https://arxiv.org/abs/2602.06382)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# _Now You See That:_ Learning End-to-End Humanoid Locomotion from Raw Pixels 

Wandong Sun<sup>1,2</sup> Yongbo Su<sup>1,2</sup> Leoric Huang<sup>2</sup> Alex Zhang<sup>2</sup> Dwyane Wei<sup>2</sup> Mu San<sup>2</sup> Daniel Tian<sup>2</sup> Ellie Cao<sup>2</sup> Baoshi Cao<sup>1</sup> Yang Liu<sup>1</sup> Finn Yan<sup>2</sup> Ethan Xie<sup>2</sup> Zongwu Xie<sup>1</sup> 1Harbin Institute of Technology 2HONOR Robotics Team 

https://github.com/Hellod035/Now_You_See_That 


**Fig. 1: Overview.** Our end-to-end vision-based humanoid locomotion policy enables robust traversal across diverse challenging terrains, including high stones, long staircases (both ascending and descending), debris fields, gaps with varying heights, trolleys, high platforms, grid holes, and platform-slope-gap combinations. All behaviors emerge from a single unified policy trained with raw depth images. 

**_Abstract_ —Achieving robust vision-based humanoid locomotion remains challenging due to two fundamental issues: the sim-toreal gap introduces significant perception noise that degrades performance on fine-grained tasks, and training a unified policy across diverse terrains is hindered by conflicting learning objectives. To address these challenges, we present an end-to-end framework for vision-driven humanoid locomotion. For robust sim-to-real transfer, we develop a high-fidelity depth sensor simulation that captures stereo matching artifacts and calibration uncertainties inherent in real-world sensing. We further propose a vision-aware behavior distillation approach that combines latent space alignment with noise-invariant auxiliary tasks, enabling effective knowledge transfer from privileged height maps to noisy depth observations. For versatile terrain adaptation, we introduce terrain-specific reward shaping integrated with multi-critic and multi-discriminator learning, where dedicated networks capture the distinct dynamics and motion priors of each terrain type. We** 

**validate our approach on two humanoid platforms equipped with different stereo depth cameras. The resulting policy demonstrates robust performance across diverse environments, seamlessly handling extreme challenges such as high platforms and wide gaps, as well as fine-grained tasks including bidirectional long-term staircase traversal.** 

### I. INTRODUCTION 

Vision-based humanoid locomotion provides a compelling benchmark for embodied intelligence, requiring robots to traverse diverse terrains, from extreme obstacles like high platforms and wide gaps to fine-grained challenges such as continuous staircases, using onboard visual and proprioceptive sensing. Unlike quadrupedal locomotion where static stability tolerates moderate control errors [19], humanoid robots operate in inherently unstable regimes [8, 30] that demand pre- 

|**Method**|**Representation**|**End-to-End**|**Noise Modeling**|**Long-Term Deploy**|**Fine Locomotion**|**Extreme Parkour**|
|---|---|---|---|---|---|---|
|Long et al. [26]|Elevation Map|✗|Moderate|✗|✓|✗|
|Sun et al. [47]|Elevation Map|✗|Moderate|✗|✓|✗|
|He et al. [12]|Elevation Map|✗|Moderate|✗|✓|✗|
|Ben et al. [2]|Voxel|✗|Moderate|✓|✓|✗|
|Zhuang et al. [60]|End-to-End Vision|✓|Moderate|✓|✗|✓|
|Song et al. [45]|Vision-to-Elevation|✗|Moderate|✓|✓|✗|
|**Ours**|End-to-End Vision|✓|Comprehensive|✓|✓|✓|


**TABLE I:** Comparison of perceptive humanoid locomotion methods. Representation indicates the terrain perception approach. Noise Modeling indicates the comprehensiveness of depth sensor simulation. Long-Term Deploy indicates drift-free operation capability. Fine Locomotion indicates support for precise movements like stair climbing. Extreme Parkour indicates support for dynamic maneuvers across challenging obstacles. 

cise coordination between perception and action. Vision-based humanoid locomotion faces two fundamental challenges: **(1)** perception noise from the sim-to-real gap severely degrades performance on fine-grained tasks requiring centimeter-level accuracy, and **(2)** training a single policy to handle diverse terrain scenarios remains difficult due to conflicting learning objectives across heterogeneous environments. 

Current perception approaches for legged robots can be broadly categorized into LiDAR-based and vision-based methods. Elevation map-based methods fuse LiDAR height measurements with odometry to construct terrain representations [6, 7, 32, 20], achieving success on both quadrupedal [31, 15, 23] and humanoid platforms [27, 47, 24]. Voxel-based 3D occupancy grids [2, 34, 16] explicitly represent volumetric geometry. However, both LiDAR-based approaches suffer from limited sensing frequency and inherent latency, constraining their applicability for highly dynamic maneuvers. Visionbased methods using depth cameras [1, 5, 58, 51, 28] offer higher bandwidth ego-centric perception, yet their application to humanoid platforms remains limited due to sim-to-real gaps from imperfect depth sensor modeling. 

Beyond perception, learning unified control across heterogeneous terrains poses additional challenges. Standard reinforcement learning with a single value function struggles to capture these diverse reward landscapes, leading prior work to train separate specialist policies before distillation [15, 59], incurring substantial training overhead. 

In this work, we present an end-to-end vision-driven locomotion framework addressing both challenges. For robust perception transfer, we introduce comprehensive depth augmentation operators that reproduce realistic stereo camera imperfections, combined with vision-aware behavior distillation that aligns latent spaces through noise-invariant auxiliary tasks. For unified terrain mastery, we employ terrain-specific reward shaping with multi-critic reinforcement learning [33] and multi-discriminator[11] adversarial motion priors, where dedicated networks capture distinct dynamics and terrainappropriate behaviors. We validate our approach on two humanoid platforms with different depth cameras, demonstrating robust performance across both extreme challenges (high platforms, wide gaps) and fine-grained locomotion tasks (long term staircases in both ascending and descending directions). Our contributions are: 

- **Realistic depth sensor simulation:** A comprehensive augmentation pipeline simulating stereo matching ar- 

- tifacts, depth-dependent noise, optical distortions, and calibration uncertainties for seamless sim-to-real transfer. 

- **Vision-aware behavior distillation:** A distillation framework combining latent space shaping with noise-invariant auxiliary tasks, transferring locomotion knowledge from privileged observations to noisy depth inputs. 

- **Multi-critic and Multi-discriminator terrain learning:** Terrain-specific reward shaping with dedicated value networks and discriminators capturing distinct dynamics and motion priors across diverse terrains within a single unified policy. 

- **Cross-platform validation:** Extensive real-world experiments on two humanoid robots with different stereo depth cameras, demonstrating successful traversal across both extreme and fine-grained terrains in diverse indoor and outdoor environments. 

### II. RELATED WORK 

### _A. Perceptive Legged Locomotion_ 

Early work on legged locomotion primarily focused on height-based terrain perception using LiDAR sensors combined with odometry systems [6, 7]. These methods construct elevation maps that enable quadrupedal robots to traverse challenging terrains by providing dense geometric information for foothold planning [23, 15, 32]. Recent humanoid locomotion systems have adopted similar approaches [40, 24, 27, 13]. However, the dynamic stability of bipedal locomotion significantly amplifies odometry drift issues, cumulative errors in map registration directly cause foothold misalignment and falls, particularly in high-impact scenarios such as running, jumping, or stair navigation. 

To eliminate odometry dependency, depth camera-based approaches have emerged as an alternative. Direct depth-toaction learning has demonstrated robust terrain traversal in quadrupedal systems [1, 5, 58, 59, 51, 28], where static stability provides inherent tolerance to perception noise. However, extending these methods to humanoid platforms remains challenging [46, 47]. An alternative approach reconstructs elevation maps directly from egocentric depth observations without external odometry [45], avoiding cumulative drift but introducing additional complexity compared to end-to-end approaches. 


**Fig. 2:** Diverse terrain types used during training. Each terrain type contains 20 difficulty levels for curriculum learning. 

### _B. Data Augmentation in Visual Reinforcement Learning_ 

Data augmentation (DA) has become a fundamental technique in visual reinforcement learning for improving both sample efficiency and generalization ability [22, 53, 54, 52, 50]. Early work explored various image transformations, with random cropping emerging as particularly effective for sampleefficient training [53, 54]. Beyond simple transformations, spectrum-based augmentation [18] and saliency-guided approaches [3] have been proposed to improve generalization. However, existing domain randomization techniques primarily focus on simple perturbations [48, 38, 4], lacking systematic modeling of structured sensor artifacts present in realworld depth cameras. For depth-based perception, comprehensive augmentation strategies must simulate realistic sensor imperfections, including stereo fusion artifacts, depthdependent noise patterns, optical distortions, and calibration variations [9], combined with appropriate preprocessing techniques to handle sensor-specific characteristics. 

Recent advances have shown that auxiliary training objectives are essential for improving generalization beyond visual augmentation alone [41]. Auxiliary task approaches have proven essential [41]: contrastive learning methods like CURL [21] maximize mutual information between augmented views to learn invariant representations [29, 17], while consistency regularization techniques such as DrAC [42] explicitly penalize policy differences across augmentations to enforce noise-invariant features. Pre-trained visual representations have also shown promise for improving sample efficiency and generalization [43, 37, 35, 49, 56, 10]. Masked autoencoder-based approaches [14, 55] and predictive representation learning [36, 25] offer alternative strategies for learning robust features. 

### III. METHOD 

We present an end-to-end framework for vision-based humanoid locomotion that addresses both perception transfer and unified terrain control. As illustrated in Figure 4, our approach follows a two-stage training pipeline. In the first stage, we train a privileged policy using height scan observations with multicritic and multi-discriminator reinforcement learning, where terrain-specific reward shaping and dedicated value networks enable efficient learning across diverse scenarios. In the second 

stage, we distill the privileged policy into a deployment policy that operates directly on depth images, using vision-aware behavior distillation with comprehensive depth augmentation to ensure robust sim-to-real transfer. 

### _A. Realistic Depth Sensor Simulation_ 

Real depth cameras exhibit structured imperfections that standard simulation pipelines fail to capture. We introduce a comprehensive augmentation pipeline that sequentially applies eight operators to simulate realistic sensor artifacts, bridging the sim-to-real gap for robust policy transfer. 

_1) Stereo Depth Fusion:_ Stereo cameras reconstruct depth through binocular correspondence matching, producing characteristic hole patterns in occluded and textureless regions. We simulate this process by rendering images from left and right viewpoints with baseline distance _b_ . For each pixel ( _u, v_ ) in the left image, we compute disparity-based correspondence: 


where _fx_ is the focal length and _ϵ_ = 10<sup>_−_6</sup> prevents division by zero. The fused depth applies a consistency check: 


where _τ ∈_ [0 _._ 05 _,_ 0 _._ 20] controls matching sensitivity. Pixels failing the consistency check are marked invalid, reproducing the hole patterns caused by occlusions and texture-poor surfaces. 

_2) Depth-Dependent Noise:_ Real depth measurements exhibit noise profiles that grow nonlinearly with distance due to the inverse relationship between disparity and depth. We model this effect with quadratic scaling: 


where _c_ 0 _, c_ 1 _, c_ 2 _∼U_ ( _−_ 0 _._ 03 _,_ 0 _._ 03) are randomly sampled per environment to capture inter-device variations. The absolute value ensures non-negative noise amplitude while preserving the randomization of noise characteristics across different simulated sensors. 

_3) Structured Noise Patterns:_ Environmental interference and sensor artifacts manifest as spatially correlated noise. We generate multi-octave Perlin noise to simulate these structured patterns: 


where _P_ ( _·, ·_ ) denotes the standard Perlin noise function that generates smooth, continuous pseudo-random values through gradient interpolation. We use 5 octaves with persistence 0.5 to balance between large-scale intensity variations and fine-grained texture, matching the multi-scale nature of real sensor interference patterns. The noise is applied with depthdependent amplitude: _d_<sup>˜</sup> = _d_ + _σ_ p( _d_ ) _· n_ perlin, where _σ_ p( _d_ ) = 

|**Order**|**Operation**|**Schedule**|**Parameters**|**Description**|
|---|---|---|---|---|
|_Prepara_<br>1<br>2<br>3|_tion Stage_<br>Camera intrinsics<br>Camera extrinsics<br>Observation delay|Once at startup<br>Once at startup<br>Once at startup|_s_h_, s_v _∼U_(0_._90_,_1_._10)<br>∆**p**_∼U_(_−_0_._05_,_0_._05)<sup>3 </sup>m<br>∆**_θ_** _∼U_(_−_0_._10_,_0_._10)<sup>3 </sup>rad<br>_d_frame _∼U_[2_,_4] frames|Focal length variations<br>Mounting position offset<br>Mounting orientation offset<br>Processing pipeline latency|
|_Processi_|_ng Pipeline_||||
|1|Stereo fusion|Per frame|_τ ∼U_[0_._05_,_0_._20]|Disparity consistency check|
|2|Random convolution|Per frame|_wi,j,k,l ∼U_(_−_0_._05_,_0_._05)|Optical aberrations|
|3|Gaussian noise|Per frame|_c_0_, c_1_, c_2 _∼U_(_−_0_._03_,_0_._03)<br><br><br>|Distance-dependent noise|
|4|Perlin noise|Per frame|_c_<sup>p</sup><br>0<sup>_, c_p</sup><br>1<sup>_, c_p</sup><br>2 <sup>_∼U_(</sup><sup>_−_0</sup><sup>_._02</sup><sup>_,_ 0</sup><sup>_._02)</sup>|Time-dependent noise|
|5|Scale randomization|Per frame|_si ∼U_(0_._90_,_1_._10)|Calibration errors|
|6|Pixel failures|Per frame|_p_zero =_p_max = 0_._001|Dead/saturated pixels|
|7|Depth clipping|Per frame|[_d_min_, d_max] = [0_._3_,_2_._0] m<br>|Valid sensing range|
|8|Spatial cropping|Per frame|(_t, b, l, r_) = (3_,_3_,_4_,_4) pixels|Edge distortion removal|


**TABLE II:** Vision Augmentation Pipeline: Operations, Schedule, Parameters and Descriptions 


**Fig. 3:** Visualization of the depth augmentation pipeline. Starting from clean left and right depth images, the pipeline sequentially applies: (1) stereo fusion, (2) random convolution, (3) Gaussian noise, (4) Perlin noise, (5) scale randomization, (6) zero pixel failures, (7) max pixel failures, (8) depth clipping and spatial cropping to produce realistic depth observations for sim-to-real transfer. 

_|c_<sup>p</sup> 0<sup>+</sup><sup>_c_</sup> 1<sup>p</sup><sup>_d_+</sup><sup>_c_</sup> 2<sup>p</sup><sup>_d_2</sup><sup>_|_followsthesamequadraticscalingwith</sup> absolute value to ensure non-negative amplitude. 

_4) Optical Distortions:_ Lens aberrations introduce local geometric distortions that vary across the image plane. We model these effects through randomized convolution: 


where _W ∈_ R<sup>3</sup><sup>_×_3</sup> with _wij ∼U_ ( _−_ 0 _._ 05 _,_ 0 _._ 05) and _I_ is the identity kernel, ensuring the distortion remains centered around the original measurement. 

_5) Calibration Uncertainties:_ Manufacturing variations and imperfect calibration cause systematic measurement errors. We randomize depth scaling _s ∼U_ (0 _._ 90 _,_ 1 _._ 10) to simulate factory calibration drift, perturb camera intrinsics through aperture scaling, and add extrinsic offsets to camera position and orientation. Additionally, we model pixel failures through random masking with probability _p_ zero = _p_ max = 0 _._ 001. 

_6) Preprocessing:_ We clip depth values to the valid sensing range [0 _._ 3 _,_ 2 _._ 0] m, normalize to [0 _,_ 1], and crop from 30 _×_ 40 to 24 _×_ 32 pixels to reduce peripheral distortion artifacts. Observation delay sampled from _U_ [2 _,_ 4] frames simulates processing pipeline latency. Table II summarizes the complete augmentation pipeline with parameter ranges. 

### _B. Privileged Reinforcement Learning_ 

Parkour terrains exhibit fundamentally different dynamics, and a single value function struggles to capture these diverse reward landscapes. We address this challenge through terrainspecific reward shaping with dedicated critic and discriminator networks. 

_1) Height Scan Observations:_ The privileged policy receives dense geometric information via ray casting over a 1.6 m _×_ 1.0 m ego-centric window with 0.05 m resolution, yielding a grid of 21 _×_ 33 = 693 height samples. This terrain representation is subsequently transferred to depthbased perception through distillation. The architecture of the depth encoder is detailed in Appendix A. 

_2) Terrain-Specific Reward Shaping:_ We partition terrains into _K_ = 3 categories with specialized reward components: (1) _stairs and platforms_ , encompassing stair ascending, stair descending, platform ascending, and platform descending; (2) _gap crossing_ ; and (3) _rough terrain_ locomotion. Detailed reward formulations are provided in Appendix D. 

_3) Multi-Critic and Multi-Discriminator Architecture:_ We maintain _K_ = 3 critic networks _{Vk}_<sup>_K_</sup> _k_ =1<sup>and</sup><sup>_K_</sup> = 3 discriminator networks _{Dk}_<sup>_K_</sup> _k_ =1<sup>, each specialized for a terrain</sup> category: (1) stairs and platforms, (2) gap crossing, and (3) 


## 2. Distillation with Vision Augmentation 


**Fig. 4: Method Overview.** Our framework consists of two stages: (1) _Privileged RL Training_ : A teacher policy is trained with height scan observations using multi-critic and multi-discriminator learning, where terrain-specific reward shaping and dedicated value networks handle diverse terrain categories (stairs/platforms, gaps, rough terrain). (2) _Vision-Aware Distillation_ : The privileged policy is distilled into a deployment policy operating on augmented depth images, combining behavior cloning with denoising objectives for robust sim-to-real transfer. 

rough terrain. The critics share a common backbone while maintaining separate output heads, enabling efficient parameter sharing while preserving terrain-specific value estimation. During training, the appropriate critic and discriminator are selected based on terrain labels: 


where _k_ ( _st_ ) _∈{_ 1 _,_ 2 _,_ 3 _}_ identifies the current terrain category. Each critic learns the value landscape for its specific dynamics, while the actor receives policy gradients from the terrainappropriate critic. Similarly, each discriminator provides style rewards tailored to the motion characteristics required for its terrain type. 

|**Parameter**|**Range**|
|---|---|
|_Contact Properties_||
|Static/Dynamic friction|(0_._4_,_1_._2)|
|Restitution|(0_._0_,_0_._4)|
|_Body Properties_||
|Mass scaling|(0_._8_,_1_._2)|
|COM offset|_±_0_._03 m|
|Default joint offset|_±_0_._03 rad|
|_Actuator Dynamics_||
|Armature scaling|(0_._5_,_1_._5)|
|Stiffness/Damping scaling|(0_._9_,_1_._1)|
|_External Disturbances_||
|Push velocity|_±_1_._2 m/s|
|IMU bias|_±_0_._04 rad/s|


**TABLE III:** Robot Dynamics Domain Randomization 

_4) Motion Priors:_ We incorporate Adversarial Motion Priors [39] to guide natural locomotion. The discriminator operates on torso-centric observations: 


We collect separate motion datasets for each terrain category to provide appropriate style guidance. 

_5) Advanced Domain Randomization:_ We apply comprehensive randomization to robot dynamics to ensure robust simto-real transfer. Table III details the complete randomization schedule covering contact properties, body parameters, actuator dynamics, and external disturbances. 

### _C. Vision-Aware Behavior Distillation_ 

We transfer the privileged policy to a deployment policy operating on depth images through DAgger-style distillation. The student policy interacts with the environment while the teacher provides supervision, enabling learning from its own state distribution. 

_1) Behavior Cloning:_ The deployment policy minimizes the action discrepancy with the privileged policy: 


where the student receives augmented depth images with proprioceptive observations, while the teacher receives clean height scans. 

_2) Denoising Objective:_ To ensure robust feature extraction under sensor noise, we enforce consistency between clean and augmented depth representations: 


where _E_ ( _·_ ) is the depth encoder, _d_ is clean depth, and _d_<sup>˜</sup> is its augmented counterpart. 

_3) Feature Regularization:_ We regularize the depth encoder features to avoid collapse by matching the _batch-wise feature distribution_ to a standard normal prior. Let _z_ = _E_ ( _d_ ) _∈_ R<sup>_N×D_</sup> 

|**Method**|SR|**Stairs Up**<br>P_↓_|PDR_↓_|SR|**Stairs Down**<br>P_↓_|PDR_↓_|SR|**Gaps**<br>P_↓_|PDR_↓_|SR|**Platform**<br>P_↓_|PDR_↓_|SR|**Average**<br>P_↓_|PDR_↓_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|No Augmentation<br>Partial Aug.<br>Standard DR<br>Humanoid Parkour|45.3_±_1_._8<br>61.2_±_1_._5<br>65.4_±_1_._3<br>74.2_±_1_._1|52.3_±_1_._2<br>43.8_±_0_._9<br>41.5_±_0_._8<br>38.2_±_0_._7|68.4_±_2_._1<br>42.6_±_1_._4<br>38.2_±_1_._2<br>28.5_±_1_._0|42.1_±_2_._0<br>57.4_±_1_._6<br>62.1_±_1_._4<br>71.5_±_1_._2|48.7_±_1_._1<br>41.2_±_0_._8<br>39.4_±_0_._7<br>36.5_±_0_._6|71.2_±_2_._3<br>45.3_±_1_._5<br>40.6_±_1_._3<br>30.2_±_1_._1|44.8_±_1_._7<br>59.8_±_1_._4<br>63.7_±_1_._2<br>72.8_±_1_._0|51.2_±_1_._0<br>42.5_±_0_._7<br>40.2_±_0_._6<br>37.1_±_0_._5|69.5_±_1_._9<br>43.8_±_1_._3<br>39.1_±_1_._1<br>29.4_±_0_._9|39.7_±_2_._2<br>53.6_±_1_._8<br>56.8_±_1_._6<br>65.5_±_1_._4|54.6_±_1_._3<br>46.1_±_1_._0<br>44.3_±_0_._9<br>40.8_±_0_._8|74.3_±_2_._5<br>48.7_±_1_._6<br>45.2_±_1_._4<br>35.6_±_1_._2|43.0_±_1_._9<br>58.0_±_1_._6<br>62.0_±_1_._4<br>71.0_±_1_._2|51.7_±_1_._2<br>43.4_±_0_._9<br>41.4_±_0_._8<br>38.2_±_0_._7|70.9_±_2_._2<br>45.1_±_1_._5<br>40.8_±_1_._3<br>30.9_±_1_._1|
|Direct RL<br>Single Critic/Disc.<br>BC Only|57.3_±_1_._9<br>85.6_±_0_._8<br>89.2<br>_±_0_._7|48.6_±_1_._1<br>34.6_±_0_._5<br>32.4<br>_±_0_._4|55.2_±_1_._8<br>18.3_±_0_._6<br>15.6<br>_±_0_._5|53.8_±_2_._1<br>82.3_±_0_._9<br>86.5<br>_±_0_._8|45.8_±_1_._0<br>32.8_±_0_._4<br>30.6<br>_±_0_._4|58.4_±_2_._0<br>20.1_±_0_._7<br>17.2<br>_±_0_._6|55.6_±_1_._8<br>83.8_±_0_._7<br>87.8<br>_±_0_._6|47.2_±_0_._9<br>33.5_±_0_._4<br>31.2<br>_±_0_._3|56.8_±_1_._7<br>19.2_±_0_._5<br>16.3<br>_±_0_._4|49.3_±_2_._3<br>76.3_±_1_._1<br>80.5<br>_±_0_._9|51.4_±_1_._2<br>37.8_±_0_._6<br>35.2<br>_±_0_._5|62.1_±_2_._2<br>25.4_±_0_._8<br>21.8<br>_±_0_._7|54.0_±_2_._0<br>82.0_±_0_._9<br>86.0<br>_±_0_._8|48.3_±_1_._1<br>34.7_±_0_._5<br>32.4<br>_±_0_._4|58.1_±_1_._9<br>20.8_±_0_._7<br>17.7<br>_±_0_._6|
|**Ours**|**99.2**_±_0_._3|**28.5**_±_0_._3|**5.2**_±_0_._2|**98.6**_±_0_._4|**27.2**_±_0_._3|**6.1**_±_0_._3|**99.3**_±_0_._2|**25.8**_±_0_._2|**4.5**_±_0_._2|**98.4**_±_0_._5|**29.4**_±_0_._4|**7.2**_±_0_._3|**98.9**_±_0_._4|**27.7**_±_0_._3|**5.8**_±_0_._3|


**TABLE IV:** Performance on RDT-Bench across four terrain configurations. SR: Success Rate (%), P: Average Power ( _×_ 10<sup>1</sup> W), PDR: Power Degradation Ratio (%). All methods are evaluated under CycleGAN-augmented realistic depth noise. Results report mean _±_ std over 5 random seeds. Best results are in **bold** , second best are <u>underlined.</u> _↓_ indicates lower is better. 

denote the encoder outputs. We estimate a diagonal Gaussian _q_ ( _z_ ) = _N_ ( **_µ_** _,_ diag( **_σ_**<sup>2</sup> )) using empirical statistics: 


where _ϵ_ is a small constant for numerical stability. We then minimize the KL divergence between this estimated distribution and the standard normal prior: 


_4) Combined Objective:_ The total distillation loss balances all components: 


where _λ_ denoise = _λ_ kl = 0 _._ 1. The depth encoder output replaces the height scan embedding, enabling vision-based deployment. 


We evaluate our approach through comprehensive simulation benchmarks and real-world deployment on a custom humanoid robot equipped with an Orbbec Gemini 336L depth camera. Our experiments address the following questions: (1) Does realistic depth augmentation improve sim-to-real transfer compared to standard domain randomization? (2) How does multi-critic learning contribute to performance across diverse terrains? (3) Do the distillation objectives improve policy robustness? 

### _A. Experimental Setup_ 

_1) Real-World Depth Transfer Benchmark:_ Standard simulation benchmarks fail to capture the perception challenges of real-world deployment. We construct the RealWorld Depth Transfer Benchmark (RDT-Bench) by training a CycleGAN [57] model on unpaired depth observations from simulation and real-world deployment. During evaluation, policies receive CycleGAN-augmented depth images while operating in the physics simulator, enabling large-scale quantitative comparison under realistic perception conditions. Importantly, CycleGAN is used _exclusively for evaluation_ , each method employs its own augmentation strategy during training, ensuring fair comparison that reveals true sim-to-real transfer capability. 

_2) Evaluation Terrains:_ We evaluate on four representative terrain configurations spanning three categories: 

- **Stairs:** 15 cm step height and 30 cm step depth, both ascending and descending 

- **Gap:** 0.45 m width requiring accurate depth perception for crossing 

- **Platform:** 0.40 m height requiring precise stepping up and down 

Each configuration is tested across 1024 parallel environments for 100 episodes, providing statistically robust performance estimates. 

- _3) Baselines:_ We compare against the following methods: 

- **Humanoid Parkour Learning** [60]: State-of-the-art vision-based humanoid locomotion using standard domain randomization with Gaussian noise and random dropout. 

- **No Augmentation** : Depth images with only simple Gaussian noise ( _σ_ = 0 _._ 01) and random pixel dropout ( _p_ = 0 _._ 001). 

- **Partial Augmentation** : Depth-dependent noise and preprocessing only, without stereo fusion, structured noise, or optical distortion. 

- **Standard DR** : Domain randomization following [60] with hole filling and random masking. 

- **Single Critic/Disc.** : Our method with a single shared critic and discriminator for all terrains, instead of terrainspecific ones. 

- **Direct RL** : End-to-end reinforcement learning directly from depth images without privileged distillation. 

- **BC Only** : Behavior cloning with only _L_ behavior, removing denoising and KL regularization losses. 

- _4) Metrics:_ We evaluate methods using three complemen- 

- tary metrics: 

- **Success Rate (SR):** Percentage of episodes where the robot traverses the terrain without falling. 

- **Average Power (P):** Average mechanical power consumption computed as _P_ = _T_ <u>1</u> � _t_<sup>_∥τt⊙q_˙</sup><sup>_t∥_2,where</sup> _τt_ denotes joint torques and _q_ ˙ _t_ denotes joint velocities. Lower values indicate more efficient locomotion. 

- **Power Degradation Ratio (PDR):** Relative power increase under realistic noise, defined as PDR = ( _P_ RDT _− P_ clean) _/P_ clean _×_ 100%. Lower PDR indicates greater robustness to sensor artifacts. 


**Fig. 5:** Real-world deployment sequences demonstrating stair traversal. Top row: ascending stairs with anticipatory leg lifting. Bottom row: descending stairs with controlled foot placement. The policy executes smooth gait patterns without any real-world fine-tuning. 

### _B. Main Results_ 

Table IV presents comprehensive results on RDT-Bench. Our method achieves 98.9% average success rate with the lowest power consumption (27.7 _×_ 10<sup>1</sup> W) and minimal power degradation (5.8% PDR), substantially outperforming all baselines across every terrain and metric. 

**Perception Transfer.** The comparison between augmentation strategies reveals the critical importance of realistic depth simulation. No Augmentation achieves only 43.0% success with severe power degradation (70.9% PDR), demonstrating that policies trained with simple Gaussian noise fail catastrophically under realistic sensor artifacts. Our full augmentation pipeline achieves 98.9% success with only 5.8% PDR, indicating consistent, efficient control despite perception noise. 

**Comparison with Prior Work.** Humanoid Parkour Learning [60] achieves 71.0% success with 30.9% PDR. Our method outperforms this baseline by 27.9% in success rate while reducing PDR by 25.1%, demonstrating that our approach not only improves task completion but also maintains powerefficient locomotion under realistic perception conditions. 

**Architecture Contributions.** Single Critic/Disc. achieves 82.0% success with 20.8% PDR, while our multi-critic and multi-discriminator approach achieves 98.9% success with 5.8% PDR. The terrain-specific value functions and discriminators enable more stable policy optimization by learning distinct motion priors for each terrain type. Direct RL without privileged distillation shows the highest PDR (58.1%), confirming that the two-stage training pipeline is essential for efficient vision-based control. 

### _C. Ablation Studies_ 

_1) Augmentation Pipeline Analysis:_ Table V analyzes the contribution of each augmentation component. Stereo Fusion 

provides the largest improvement by simulating characteristic hole patterns that cause significant perception failures on real hardware. Depth-Dependent Noise and Calibration Uncertainties offer moderate gains by modeling distance-varying uncertainty and device variations. Even components with smaller SR impact contribute to control smoothness, validating the importance of comprehensive sensor modeling. 

|**Configuration**|**SR (%)**|**P (**_×_10<sup>1</sup> **W)**_↓_|**PDR (%)**_↓_|
|---|---|---|---|
|Full Pipeline|**98.9**_±_0_._4|**27.7**_±_0_._3|**5.8**_±_0_._2|
|w/o Stereo Fusion|90.4_±_0_._6|34.1_±_0_._5|17.5_±_0_._4|
|w/o Depth-Dependent Noise|92.1_±_0_._5|32.5_±_0_._4|14.9_±_0_._3|
|w/o Structured Noise (Perlin)|96.2<br>_±_0_._3|29.4<br>_±_0_._3|8.3<br>_±_0_._2|
|w/o Optical Distortions|96.9_±_0_._3|28.7_±_0_._3|7.2_±_0_._2|
|w/o Calibration Uncertainties|94.5_±_0_._4|31.0_±_0_._4|11.7_±_0_._3|
|w/o Preprocessing|95.6_±_0_._4|30.1_±_0_._3|9.9_±_0_._3|


**TABLE V:** Ablation study on depth augmentation components. Each row removes one component from the full pipeline. Results report mean _±_ std over 5 random seeds. 

_2) Multi-Critic Architecture:_ Table VI compares singlecritic/discriminator and multi-critic/discriminator architectures. The multi-critic/discriminator approach provides consistent improvements across all terrain categories in both success rate (+15.1% to +22.5%) and power degradation (-13.5% to - 18.2% PDR), indicating that terrain-specific value functions and discriminators enable more stable gradient estimation during training. 

|**Method**|**Sta**<br>SR|**irs**<br>PDR_↓_|**G**<br>SR|**aps**<br>PDR_↓_|**Pla**<br>SR|**tforms**<br>PDR_↓_|
|---|---|---|---|---|---|---|
|Single Critic/Disc.|84.0_±_0_._5|19.2_±_0_._3|83.8_±_0_._4|19.2_±_0_._3|76.3_±_0_._6|25.4_±_0_._4|
|Multi-Critic/Disc. (Ours)|**98.9**_±_0_._4|**5.7**_±_0_._2|**99.3**_±_0_._2|**4.5**_±_0_._2|**98.4**_±_0_._5|**7.2**_±_0_._3|
|∆|+14.9|-13.5|+15.5|-14.7|+22.1|-18.2|


**TABLE VI:** Ablation study on multi-critic and multi-discriminator architecture. Stairs column reports the average of ascending (99.2%) and descending (98.6%) configurations. Results report mean _±_ std over 5 random seeds. 


**Fig. 6:** t-SNE visualization of the depth encoder’s latent space across six terrain types. Each terrain forms a distinct cluster, demonstrating effective terrain-specific representation learning despite realistic sensor noise. 

_3) Distillation Objectives:_ Table VII evaluates the distillation loss components. The denoising objective _L_ denoise contributes 5.5% SR improvement by enforcing consistent latent representations between clean and augmented depth inputs. KL regularization _L_ kl provides 2.8% SR improvement by preventing representation collapse. Using behavior cloning alone achieves only 86.0% SR with 17.7% PDR, demonstrating that auxiliary objectives are essential for robust visionbased deployment. 

|**Configuration**|**SR (%)**|**P (**_×_10<sup>1</sup> **W)**_↓_|**PDR (%)**_↓_|
|---|---|---|---|
|Full|**98.9**_±_0_._4|**27.7**_±_0_._3|**5.8**_±_0_._2|
|w/o _L_denoise|93.4_±_0_._5|32.3_±_0_._4|13.3_±_0_._3|
|w/o _L_kl|96.1<br>_±_0_._4|29.5<br>_±_0_._3|8.9<br>_±_0_._3|
|BC Only|86.0_±_0_._6|32.4_±_0_._4|17.7_±_0_._4|


**TABLE VII:** Ablation study on distillation loss components. Results report mean _±_ std over 5 random seeds. 

### _D. Latent Space Analysis_ 

To understand how our depth encoder represents different terrains, we visualize the learned latent space using t-SNE dimensionality reduction. Figure 6 shows the latent embeddings of augmented depth observations across six terrain types. 

The visualization reveals that each terrain type, stair ascending, stair descending, gap, platform ascending, platform descending, and rough terrain, forms a distinct, well-separated cluster. This clear separation indicates that our encoder learns to extract terrain-specific geometric features despite realistic sensor noise, providing the policy with discriminative information for appropriate locomotion strategies. 

### _E. Real-World Deployment_ 

We validate our approach on a full-sized humanoid robot equipped with a stereo depth camera. The policy runs entirely onboard at 50 Hz without any fine-tuning from simulation training. 

_1) Test Scenarios:_ We evaluate four real-world scenarios: (1) outdoor stairs with 15 cm step height (ascending and descending), (2) outdoor platforms with approximately 40 cm height, (3) extended staircases with 30+ consecutive steps, and (4) wide gaps exceeding 45 cm width. 

_2) Quantitative Results:_ Table VIII reports results from real-world deployment. The policy achieves 97.8% overall success rate (88/90 trials), with perfect performance on five out of six test conditions. The extended staircase test validates long-horizon stability over 30+ consecutive steps without accumulated drift. 

_3) Failure Analysis:_ The performance gap between stair ascending (100%) and descending (86.7%) reveals an inherent asymmetry in bipedal locomotion: during descent, gravitational acceleration amplifies minor errors into irreversible forward momentum, whereas similar misjudgments during ascent remain recoverable. Additionally, the target foot placement is partially occluded by the current step edge, precisely where stereo matching artifacts are most pronounced. These observations suggest that robust stair descent demands higherresolution near-field depth sensing or predictive foot placement strategies. 

|**Scenario**|**Success**|**Rate (%)**|
|---|---|---|
|Outdoor Stairs (up)|15/15|100.0|
|Outdoor Stairs (down)|13/15|86.7|
|Outdoor Platform (up)|15/15|100.0|
|Outdoor Platform (down)|15/15|100.0|
|Extended Staircase|15/15|100.0|
|Wide Gap Crossing|15/15|100.0|
|**Overall**|**88/90**|**97.8**|


**TABLE VIII:** Real-world deployment success rates across 15 trials per scenario. 

_4) Cross-Platform Generalization:_ To assess whether our training pipeline generalizes beyond the primary platform, we apply the same methodology to a Unitree G1 humanoid robot equipped with an Intel RealSense D435i depth camera, a different robot morphology and sensor modality. Preliminary results are provided in Appendix E, suggesting that our depth augmentation and multi-critic framework can be effectively transferred to new hardware configurations. 

### V. CONCLUSION AND LIMITATIONS 

We presented a framework for vision-based humanoid locomotion that combines realistic depth sensor simulation, multicritic reinforcement learning, and vision-aware behavior distillation. Our depth augmentation pipeline models stereo fusion artifacts, depth-dependent noise, and calibration uncertainties, while terrain-specific critics and discriminators enable unified control across diverse scenarios. Experiments on RDT-Bench and real-world deployment demonstrate strong performance across diverse terrains without fine-tuning. However, stair descent remains less robust than ascent due to gravitational amplification of minor errors and occlusion of target footholds by step edges, which motivates future work on higher resolution near-field depth sensing and predictive foot placement strategies. 

REFERENCES 

locomotion. _Science Robotics_ , 10(105):eadv3604, 2025. 

- [1] Ananye Agarwal, Ashish Kumar, Jitendra Malik, and Deepak Pathak. Legged locomotion in challenging terrains using egocentric vision. In _Conference on robot learning_ , pages 403–415. PMLR, 2023. 

- [2] Qingwei Ben, Botian Xu, Kailin Li, Feiyu Jia, Wentao Zhang, Jingping Wang, Jingbo Wang, Dahua Lin, and Jiangmiao Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains, 2025. URL https://arxiv.org/abs/2511.14625. 

- [3] David Bertoin, Adil Zouitine, Mehdi Zouitine, and Emmanuel Rachelson. Look where you look! saliencyguided q-networks for generalization in visual reinforcement learning. _Advances in Neural Information Processing Systems_ , 35:30693–30706, 2022. 

- [4] Xiaoyu Chen, Jiachen Hu, Chi Jin, Lihong Li, and Liwei Wang. Understanding domain randomization for sim-toreal transfer. _arXiv preprint arXiv:2110.03239_ , 2021. 

- [5] Xuxin Cheng, Kexin Shi, Ananye Agarwal, and Deepak Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450. IEEE, 2024. 

- [6] P´eter Fankhauser, Michael Bloesch, Christian Gehring, Marco Hutter, and Roland Siegwart. Robot-centric elevation mapping with uncertainty estimates. In _International Conference on Climbing and Walking Robots (CLAWAR)_ , 2014. 

- [7] P´eter Fankhauser, Michael Bloesch, and Marco Hutter. Probabilistic terrain mapping for mobile robots with uncertain localization. _IEEE Robotics and Automation Letters (RA-L)_ , 3(4):3019–3026, 2018. doi: 10.1109/ LRA.2018.2849506. 

- [8] Ambarish Goswami and Vinutha Kallem. Rate of change of angular momentum and balance maintenance of biped robots. In _International Conference on Robotics and Automation (ICRA)_ , 2004. 

- [9] Nicklas Hansen, Hao Su, and Xiaolong Wang. Stabilizing deep q-learning with convnets and vision transformers under data augmentation. _Advances in Neural Information Processing Systems_ , 34, 2021. 

- [10] Nicklas Hansen, Zhecheng Yuan, Yanjie Ze, Tongzhou Mu, Aravind Rajeswaran, Hao Su, Huazhe Xu, and Xiaolong Wang. On pre-training for visuo-motor control: Revisiting a learning-from-scratch baseline. _arXiv preprint arXiv:2212.05749_ , 2022. 

- [11] Corentin Hardy, Erwan Le Merrer, and Bruno Sericola. Md-gan: Multi-discriminator generative adversarial networks for distributed datasets. In _2019 IEEE International Parallel and Distributed Processing Symposium (IPDPS)_ , page 866–877. IEEE, May 2019. doi: 10. 1109/ipdps.2019.00095. URL http://dx.doi.org/10.1109/ IPDPS.2019.00095. 

- [12] Junzhe He, Chong Zhang, Fabian Jenelten, Ruben Grandia, Moritz B¨acher, and Marco Hutter. Attentionbased map encoding for learning generalized legged 

- [13] Junzhe He, Chong Zhang, Fabian Jenelten, Ruben Grandia, Moritz B Acher,<sup>¨</sup> and Marco Hutter. Attentionbased map encoding for learning generalized legged locomotion, 2025. URL https://arxiv.org/abs/2506.09588. 

- [14] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Doll´ar, and Ross Girshick. Masked autoencoders are scalable vision learners. _arXiv preprint arXiv:2111.06377_ , 2021. 

- [15] David Hoeller, Nikita Rudin, Dhionis Sako, and Marco Hutter. Anymal parkour: Learning agile navigation for quadrupedal robots. _Science Robotics_ , 9(88):eadi7566, 2024. 

- [16] Armin Hornung, Kai M. Wurm, Maren Bennewitz, Cyrill Stachniss, and Wolfram Burgard. OctoMap: An efficient probabilistic 3D mapping framework based on octrees. _Autonomous Robots_ , 2013. doi: 10.1007/ s10514-012-9321-0. URL https://octomap.github.io. Software available at https://octomap.github.io. 

- [17] Weiran Huang, Mingyang Yi, and Xuyang Zhao. Towards the generalization of contrastive self-supervised learning. _arXiv preprint arXiv:2111.00743_ , 2021. 

- [18] Yangru Huang, Peixi Peng, Yifan Zhao, Guangyao Chen, and Yonghong Tian. Spectrum random masking for generalization in image-based reinforcement learning. _Advances in Neural Information Processing Systems_ , 35: 20393–20406, 2022. 

- [19] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 2019. 

- [20] R.E. Kalman. A new approach to linear filtering and prediction problems. _Journal of Basic Engineering_ , 82 (1):35–45, 1960. 

- [21] Michael Laskin, Aravind Srinivas, and Pieter Abbeel. Curl: Contrastive unsupervised representations for reinforcement learning. In _International Conference on Machine Learning_ , pages 5639–5650. PMLR, 2020. 

- [22] Misha Laskin, Kimin Lee, Adam Stooke, Lerrel Pinto, Pieter Abbeel, and Aravind Srinivas. Reinforcement learning with augmented data. _Advances in neural information processing systems_ , 33:19884–19895, 2020. 

- [23] Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning quadrupedal locomotion over challenging terrain. _Science robotics_ , 2020. 

- [24] Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control. _The International Journal of Robotics Research (IJRR)_ , 2024. 

- [25] Minsong Liu, Yuanheng Zhu, Yaran Chen, and Dongbin Zhao. Enhancing reinforcement learning via transformerbased state predictive representations. _IEEE Transactions on Artificial Intelligence_ , 2024. 

- [26] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao 

Huang, Ping Luo, and Jiangmiao Pang. Learning humanoid locomotion with perceptive internal model. _arXiv preprint arXiv:2411.14386_ , 2024. 

- [27] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao Huang, Ping Luo, and Jiangmiao Pang. Learning humanoid locomotion with perceptive internal model. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9997–10003. IEEE, 2025. 

- [28] Antonio Loquercio, Ashish Kumar, and Jitendra Malik. Learning visual locomotion with cross-modal supervision. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7295–7302. IEEE, 2023. 

- [29] Bogdan Mazoure, Remi Tachet des Combes, Thang Long Doan, Philip Bachman, and R Devon Hjelm. Deep reinforcement and infomax learning. In _Advances in Neural Information Processing Systems_ , 2020. 

- [30] Tad McGeer. Passive Dynamic Walking. _The International Journal of Robotics Research_ , 9(2):62–82, 1990. doi: 10.1177/027836499000900206. URL http: //ijr.sagepub.com/content/9/2/62.abstract. 

- [31] Takahiro Miki, Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning robust perceptive locomotion for quadrupedal robots in the wild. _Science Robotics_ , 7(62), January 2022. ISSN 2470-9476. doi: 10.1126/scirobotics.abk2822. URL http://dx.doi.org/10.1126/scirobotics.abk2822. 

- [32] Takahiro Miki, Lorenz Wellhausen, Ruben Grandia, Fabian Jenelten, Timon Homberger, and Marco Hutter. Elevation mapping for locomotion and navigation using gpu. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2273–2280. IEEE, 2022. 

- [33] Siddharth Mysore, George Cheng, Yunqi Zhao, Kate Saenko, and Meng Wu. Multi-critic actor learning: Teaching rl policies to act with style. In _International Conference on Learning Representations (ICLR)_ , 2022. 

- [34] I Made Aswin Nahrendra, Byeongho Yu, Minho Oh, Dongkyu Lee, Seunghyun Lee, Hyeonwoo Lee, Hyungtae Lim, and Hyun Myung. Obstacle-aware quadrupedal locomotion with resilient multi-modal reinforcement learning, 2024. URL https://arxiv.org/abs/2409.19709. 

- [35] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ , 2022. 

- [36] Tianwei Ni, Benjamin Eysenbach, Erfan Seyedsalehi, Michel Ma, Clement Gehring, Aditya Mahajan, and Pierre-Luc Bacon. Bridging state and history representations: Understanding self-predictive rl. _arXiv preprint arXiv:2401.08898_ , 2024. 

- [37] Simone Parisi, Aravind Rajeswaran, Senthil Purushwalkam, and Abhinav Gupta. The unsurprising effectiveness of pre-trained vision models for control. In _International Conference on Machine Learning_ , pages 17359–17371. PMLR, 2022. 

- [38] Xue Bin Peng, Marcin Andrychowicz, Wojciech 

Zaremba, and Pieter Abbeel. Sim-to-real transfer of robotic control with dynamics randomization. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 3803–3810. IEEE, 2018. 

- [39] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics_ , 40(4):1–20, July 2021. ISSN 1557-7368. doi: 10.1145/3450626.3459670. URL http: //dx.doi.org/10.1145/3450626.3459670. 

- [40] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 2024. 

- [41] Banafsheh Rafiee, Jun Jin, Jun Luo, and Adam White. What makes useful auxiliary tasks in reinforcement learning: investigating the effect of the target policy. _arXiv preprint arXiv:2204.00565_ , 2022. 

- [42] Roberta Raileanu, Maxwell Goldstein, Denis Yarats, Ilya Kostrikov, and Rob Fergus. Automatic data augmentation for generalization in reinforcement learning. _Advances in Neural Information Processing Systems_ , 34:5402–5415, 2021. 

- [43] Rutav M Shah and Vikash Kumar. Rrl: Resnet as representation for reinforcement learning. In _International Conference on Machine Learning_ , pages 9465–9476. PMLR, 2021. 

- [44] Leslie N. Smith and Nicholay Topin. Super-convergence: Very fast training of neural networks using large learning rates, 2018. URL https://arxiv.org/abs/1708.07120. 

- [45] Haolin Song, Hongbo Zhu, Tao Yu, Yan Liu, Mingqi Yuan, Wengang Zhou, Hua Chen, and Houqiang Li. Gait-adaptive perceptive humanoid locomotion with realtime under-base terrain reconstruction, 2025. URL https: //arxiv.org/abs/2512.07464. 

- [46] Jingkai Sun, Gang Han, Pihai Sun, Wen Zhao, Jiahang Cao, Jiaxu Wang, Yijie Guo, and Qiang Zhang. Dpl: Depth-only perceptive humanoid locomotion via realistic depth synthesis and cross-attention terrain reconstruction. _arXiv preprint arXiv:2510.07152_ , 2025. 

- [47] Wandong Sun, Baoshi Cao, Long Chen, Yongbo Su, Yang Liu, Zongwu Xie, and Hong Liu. Learning perceptive humanoid locomotion over challenging terrain. _arXiv preprint arXiv:2503.00692_ , 2025. 

- [48] Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, and Pieter Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ . IEEE, 2017. 

- [49] Tete Xiao, Ilija Radosavovic, Trevor Darrell, and Jitendra Malik. Masked visual pre-training for motor control. _arXiv preprint arXiv:2203.06173_ , 2022. 

- [50] Mingle Xu, Sook Yoon, Alvaro Fuentes, and Dong Sun Park. A comprehensive survey of image augmentation techniques for deep learning. _arXiv preprint_ 

_arXiv:2205.01491_ , 2022. 

- [51] Ruihan Yang, Minghao Zhang, Nicklas Hansen, Huazhe Xu, and Xiaolong Wang. Learning vision-guided quadrupedal locomotion end-to-end with cross-modal transformers. _arXiv preprint arXiv:2107.03996_ , 2021. 

- [52] Suorong Yang, Weikang Xiao, Mengcheng Zhang, Suhan Guo, Jian Zhao, and Furao Shen. Image data augmentation for deep learning: A survey. _arXiv preprint arXiv:2204.08610_ , 2022. 

- [53] Denis Yarats, Ilya Kostrikov, and Rob Fergus. Image augmentation is all you need: Regularizing deep reinforcement learning from pixels. In _International Conference on Learning Representations_ , 2020. 

- [54] Denis Yarats, Rob Fergus, Alessandro Lazaric, and Lerrel Pinto. Mastering visual continuous control: Improved data-augmented reinforcement learning. In _International Conference on Learning Representations_ , 2021. 

- [55] Tao Yu, Zhizheng Zhang, Cuiling Lan, Zhibo Chen, and Yan Lu. Mask-based latent reconstruction for reinforcement learning. _arXiv preprint arXiv:2201.12096_ , 2022. 

- [56] Zhecheng Yuan, Zhengrong Xue, Bo Yuan, Xueqian Wang, Yi Wu, Yang Gao, and Huazhe Xu. Pre-trained image encoder for generalizable visual reinforcement learning. In _First Workshop on Pre-training: Perspectives, Pitfalls, and Paths Forward at ICML 2022_ , 2022. 

- [57] Jun-Yan Zhu, Taesung Park, Phillip Isola, and Alexei A Efros. Unpaired image-to-image translation using cycleconsistent adversarial networkss. In _Computer Vision (ICCV), 2017 IEEE International Conference on_ , 2017. 

- [58] Ziwen Zhuang, Zipeng Fu, Jianren Wang, Christopher Atkeson, Soeren Schwertfeger, Chelsea Finn, and Hang Zhao. Robot parkour learning. _arXiv preprint arXiv:2309.05665_ , 2023. 

- [59] Ziwen Zhuang, Zipeng Fu, Jianren Wang, Christopher Atkeson, Soeren Schwertfeger, Chelsea Finn, and Hang Zhao. Robot parkour learning, 2023. URL https://arxiv. org/abs/2309.05665. 

- [60] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. In _Conference on Robot Learning (CoRL)_ , 2024. 

APPENDIX 

### _A. Network Architectures_ 

We present the detailed network architectures for the teacher policy, student policy, and multi-critic networks used in our framework. The teacher and student policies share identical architectures except for their exteroceptive encoders: the teacher uses an MLP to process privileged height scan observations, while the student uses a CNN to process depth images. During distillation, the student’s CNN encoder learns to produce latent representations that match the teacher’s MLP encoder output, enabling seamless transfer of the learned locomotion policy from privileged to vision-based observations. 

|Component|Configuration|
|---|---|
||_Height Scan Encoder_|
|Input Layer<br>Hidden Layer 1|Height Scan (21 × 33 = 693)<br>Linear(693 →512) + SiLU|
|Hidden Layer 2<br>Output Layer|Linear(512 →256) + SiLU<br>Linear(256 →128)|
||_Recurrent Module_|
|Input<br>RNN Type<br>Hidden Dimension|Concat(Proprio[96], Encoder[128]) = 224<br>GRU (1 layer)<br>256|
||_Actor MLP_|
|Input Layer|GRU Output (256)|
|Hidden Layer 1|Linear(256 →512) + SiLU|
|Hidden Layer 2|Linear(512 →256) + SiLU|
|Hidden Layer 3|Linear(256 →128) + SiLU|
|Output Layer|Linear(128 →29)|
||_Policy Distribution_|
|Distribution Type<br>Initial Noise Std|Gaussian<br>1.0|


**TABLE IX:** Teacher Policy Network Architecture 

|Component|Configuration|
|---|---|
|_De_|_pth Image Encoder (CNN)_|
|Input Layer|Depth Image (1 × 24 × 32)|
|Conv Layer 1|Conv2d(1 →32, k=3, s=2, p=1) + SiLU|
|Conv Layer 2|Conv2d(32 →64, k=3, s=2, p=1) + SiLU|
|Conv Layer 3<br>Flatten|Conv2d(64 →128, k=3, s=2, p=1) + SiLU<br>128 × 3 × 4 = 1536|
|Output Layer|Linear(1536 →128)|
||_Recurrent Module_|
|Input<br>RNN Type<br>Hidden Dimension|Concat(Proprio[96], Encoder[128]) = 224<br>GRU (1 layer)<br>256|
||_Actor MLP_|
|Input Layer<br>Hidden Layer 1|GRU Output (256)<br>Linear(256 →512) + SiLU|
|Hidden Layer 2|Linear(512 →256) + SiLU|
|Hidden Layer 3<br>Output Layer|Linear(256 →128) + SiLU<br>Linear(128 →29)|
||_Policy Distribution_|
|Distribution Type|Gaussian|
|Constant Noise Std|0.1|


**TABLE X:** Student Policy Network Architecture 

|Component|Configuration|
|---|---|
||_Height Scan Encoder (Shared)_|
|Input Layer<br>Hidden Layer|Height Scan (21 × 33 = 693)<br> 1<br>Linear(693 →512) + SiLU|
|Hidden Layer|2<br>Linear(512 →256) + SiLU|
|Output Layer|Linear(256 →128)|
||_Recurrent Module (Shared)_|
|Input|Concat(Proprio[96], Encoder[128]) = 224|
|RNN Type<br>Hidden Dimen|GRU (1 layer)<br>sion<br>256|
||_Critic MLP (Shared Backbone)_|
|Input Layer<br>Hidden Layer|GRU Output (256)<br> 1<br>Linear(256 →512) + SiLU|
|Hidden Layer|2<br>Linear(512 →256) + SiLU|
|Hidden Layer|3<br>Linear(256 →128) + SiLU|
||_Terrain-Specific Output Heads_|
|Stair Head|Linear(128 →1)|
|Gap Head|Linear(128 →1)|
|General Head|Linear(128 →1)|


**TABLE XI:** Multi-Critic Network Architecture 

### _B. Implementation Details_ 

We provide the detailed hyperparameters for our policy distillation framework in Table XII. The distillation process transfers the learned locomotion policy from the teacher (which operates on privileged height scan observations) to the student (which operates on depth images). We employ a cosine annealing learning rate schedule with warm-up to ensure stable training dynamics. The loss coefficients are carefully balanced to ensure that behavior cloning provides the primary learning signal while the denoising and KL regularization objectives contribute to robustness against sensor noise and prevent representation collapse, respectively. We use gradient accumulation to stabilize training with large effective batch sizes and apply gradient clipping to prevent training instabilities. 

|**Parameter**|**Value**|
|---|---|
|_(a) Training Hyperparameters_<br>Steps per environment per iteration|800|
|Total training iterations|4000|
|Learning rate schedule|One Cycle [44]<br>|
|Initial learning rate|1_×_10<sup>_−_3</sup>|
|Div factor (peak/init)|10.0|
|Final div factor (final/init)|50.0|
|Gradient accumulation steps|10|
|Max gradient norm|1.0|
|_(b) Loss Coefficients_<br>Behavior loss weight|1_._0|
|Denoising loss coeff. _λ_denoise|0_._1|
|KL loss coeff. _λ_kl|0_._1|
|EMA decay|0_._997|


**TABLE XII:** Policy Distillation Configuration 

### _C. CycleGAN Hyperparameters_ 

We train a CycleGAN model to translate between simulated and real-world depth images for evaluation purposes. The real-world dataset consists of approximately 2 hours of depth recordings from the humanoid robot traversing various terrains, yielding approximately 200,000 depth frames. The CycleGAN is used _exclusively for evaluation_ to inject realistic depth artifacts into simulation, enabling fair comparison of sim-to-real transfer capabilities across different training augmentation strategies. 

_1) Translation Quality Evaluation:_ To validate that our CycleGAN produces realistic depth translations, we evaluate the model using standard image-to-image translation metrics on a held-out test set comprising 10% of the data (approximately 20,000 frames). 

|**Metric**|**Sim**_→_**Real**<br>**Real**_→_**Sim**|
|---|---|
|_Translation Quality_<br>FID _↓_(no translation baseline)|67.2|
|FID _↓_(after CycleGAN)|23.4<br>21.7|
|KID (_×_10<sup>_−_3</sup>) _↓_|8.2<br>7.6|
|_Cycle Consistency_||
|SSIM _↑_|0.89<br>0.91|
|PSNR _↑_|28.3 dB<br>29.1 dB|
|LPIPS _↓_|0.12<br>0.11|


**TABLE XIII:** CycleGAN Translation Quality Metrics. **Translation Quality** : FID and KID measure distributional distance between translated images _G_ ( _x_ source) and real target domain images _x_ target. The baseline FID (67.2) is computed between raw simulation and real depth images without translation. **Cycle Consistency** : SSIM, PSNR, and LPIPS evaluate reconstruction quality of _F_ ( _G_ ( _x_ )) _≈ x_ , measuring how well geometric structure is preserved through the translation cycle. Images are resized to 128 _×_ 128 before FID computation using bilinear interpolation. 

The FID score of 23.4 for Sim _→_ Real translation indicates that the generated depth images closely match the statistical properties of real sensor outputs. The high cycle-consistency metrics (SSIM = 0.89, PSNR = 28.3 dB) confirm that the translation preserves geometric structure while introducing realistic sensor artifacts. 

|**Parameter**|**Value**|
|---|---|
|_(a) Dataset Statistics_<br>Total real-world recording time|_∼_2 hours|
|Total depth frames|_∼_200,000|
|Frame resolution|24 _×_ 32|
|Train/Val split|90% / 10%|
|_(b) Network Architecture_||
|Generator architecture|ResNet (9 blocks)|
|Discriminator architecture|PatchGAN (70 _×_ 70)|
|Number of filters (first layer)|64|
|Normalization|Instance Normalization|
|_(c) Training Hyperparameters_||
|Batch size|64|
|Total epochs|200|
|Optimizer|Adam|
|Learning rate|2_×_10<sup>_−_4</sup>|
|_β_1, _β_2|0.5, 0.999|
|Learning rate decay|Linear (after epoch 100)|
|_(d) Loss Weights_||
|Adversarial loss weight|1.0|
|Cycle consistency loss weight _λcyc_|10.0|
|Identity loss weight _λidt_|0.5|


**TABLE XIV:** CycleGAN Training Configuration 

### _D. Terrain Specific Rewards_ 

Our multi-critic framework employs terrain-specific reward functions to encourage appropriate locomotion strategies for different obstacle types. We detail the key terrain-specific rewards below. 

_1) Velocity Tracking Rewards:_ We employ two distinct velocity tracking formulations depending on terrain requirements: **Exponential Velocity Tracking** ( _r_ vel<sup>exp)isusedforstairs,platforms,androughterrain,whereprecisevelocityregulation</sup> ensures stable foot placement: 


where **v** _xy_<sup>cmd</sup> denotes the commanded velocity, **v** _xy_<sup>robot</sup> denotes the robot’s base linear velocity in the body frame, and _σ_ is a temperature parameter controlling tracking precision. This exponential kernel provides smooth gradients that encourage accurate velocity following, which is critical for controlled stepping on elevated surfaces. 

**Directional Velocity Tracking** ( _r_ vel<sup>dir) is used for gap terrain, where the robot benefits from moving faster than the commanded</sup> 

velocity to execute dynamic crossing motions: 


where **d**<sup>ˆ</sup> cmd = **v** _xy_<sup>cmd</sup><sup>_/∥_</sup><sup>**v**</sup> _xy_<sup>cmd</sup><sup>_∥_istheunitdirectionofthecommandedvelocity,and</sup><sup>_ϵ_isasmallconstantfornumericalstability.</sup> This formulation rewards movement in the commanded direction without penalizing speeds exceeding the command magnitude, enabling the robot to build momentum for successful gap traversal. 

_2) Feet Contact Height Reward:_ For stairs and platform terrains, we introduce a feet contact height reward ( _r_ contact) that encourages the robot to place its feet on flat, stable surfaces: 


where _h_<sup>scan</sup> _f_ denotes the height scan measurements around foot _f_ relative to the foot position, ⊮<sup>_f_</sup> contact<sup>isanindicatorfunction</sup> that equals 1 when foot _f_ is in contact with the ground, and _h_ max is a clipping threshold. The standard deviation of clipped height values around each foot serves as a measure of surface irregularity, lower values indicate flatter contact surfaces. This reward is applied as a penalty (with negative weight) to discourage foot placement on edges or uneven surfaces, which is particularly important for stair and platform traversal where precise foot placement determines stability. This reward is _not_ applied to gap and rough terrains: gap crossing requires dynamic leaping motions where contact surface analysis is less relevant, while rough terrain inherently features irregular surfaces where penalizing height variation would be counterproductive. 

|**Reward**|**Stairs/Platforms**|**Gaps**|**Rough**|
|---|---|---|---|
|_r_<sup>exp</sup><br>vel<br>_r_<sup>dir</sup><br>vel|✓<br>–|–<br>✓|✓<br>–|
|_r_contact|✓|–|–|


**TABLE XV:** Terrain-Specific Reward Configuration 

### _E. Cross-Platform Validation_ 

We conduct a preliminary cross-platform validation to assess whether the learned policy generalizes beyond the primary training platform. We deploy our policy on a Unitree G1 humanoid robot, which differs from our primary platform in both kinematic structure and sensor configuration (Intel RealSense D435i vs. Orbbec Gemini 336L). 

|**Scenario**|**Success**|**Rate (%)**|
|---|---|---|
|Stair Ascending|15/15|100.0|


**TABLE XVI:** Cross-Platform Validation on Unitree G1 

As shown in Table XVI and Figure 7, the policy achieves perfect success rate on the stair ascending task without any platformspecific adaptation. This result provides initial evidence that our depth augmentation strategy learns transferable geometric representations rather than sensor-specific artifacts. However, we note that this validation is limited to a single terrain type; comprehensive cross-platform benchmarking across gaps, platforms, and descending scenarios remains an important direction for future work. 


**Fig. 7:** Cross-platform deployment on Unitree G1 humanoid robot ascending outdoor stairs. The policy transfers zero-shot from training on a different platform with different depth sensor, demonstrating the generality of the learned depth representations. 

### _F. Additional Augmentation Results_ 

We provide additional visualization examples of our depth augmentation pipeline in Figure 8. Each row shows a triplet consisting of: (1) the left camera depth image, (2) the right camera depth image, and (3) the augmented depth output before spatial cropping. All depth values are normalized to the range [0 _,_ 2] meters and converted to color maps for intuitive visualization, where cooler colors (blue/purple) indicate closer surfaces and warmer colors (red/yellow) represent farther distances. 


**Fig. 8:** Additional depth augmentation examples across diverse terrains. Each triplet shows (left to right): left camera depth, right camera depth, and augmented output before spatial cropping. Depth values are normalized to [0 _,_ 2] m and rendered as color maps (cool = near, warm = far). The augmented images exhibit realistic stereo fusion holes (black regions), depth-dependent noise, and structured Perlin patterns while preserving terrain geometry essential for locomotion control. 

