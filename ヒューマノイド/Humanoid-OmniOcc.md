---
title: "Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI"
date: "2026-06-22"
authors: "Xianda Guo; Bohao Zhang; Chenwei Huang; Shiyuan Chen; Ruilin Wang; Yiqun Duan"
url: https://arxiv.org/abs/2606.22971
pdf: https://arxiv.org/pdf/2606.22971
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.22971)** / [論文ページ](https://arxiv.org/abs/2606.22971)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Humanoid-OmniOcc: Stereo-Based Full-View Occupancy Dataset for Embodied AI** 

**Xianda Guo**<sup>**1,**</sup><sup>_∗†_</sup> **Bohao Zhang**<sup>**2,**</sup><sup>_∗_</sup> **Chenwei Huang**<sup>**2,**</sup><sup>_∗_</sup> **Shiyuan Chen**<sup>**2,3**</sup> **Ruilin Wang**<sup>**2**</sup> **Yiqun Duan**<sup>**4**</sup> **Cong Yang**<sup>**3**</sup> **Qin Zou**<sup>**1,**�</sup> **Wei Sui**<sup>**2,**�</sup> 

> 1 School of Computer Science, Wuhan University 2 D-Robotics 3 Soochow University 4 UTS xianda_guo@163.com, {bohao.zhang, chenwei.huang, wei.sui}@d-robotics.cc 

> _∗_ Equal Contributions � Corresponding Author 

## **Abstract** 

Occupancy prediction at voxel-level granularity is essential for safe robotic navigation and interaction in complex environments. Existing occupancy datasets, however, are predominantly designed for autonomous driving with vehicle-centric biases—forward-facing cameras, far-field geometry, and static road priors— limiting their applicability to embodied humanoid perception. We present **Humanoid-OmniOcc** , a large-scale panoramic stereo-based occupancy dataset tailored for humanoid robots. The dataset encompasses 15 diverse simulated indoor scenes and 5 real-world environments, yielding over 155K samples with broad scene and style diversity. Importantly, the dataset is designed around a **Real2Sim2Real** closed-loop paradigm: real sensor specifications drive physically accurate simulation, simulation produces large-scale annotated training data, and models trained in simulation are directly evaluated on real-world captures— enabling iterative refinement of the sim-to-real pipeline. We further propose **H** umanoid **S** urround **S** tereo-guided **Occ** upancy model ( **HS**<sup>**2**</sup> **Occ** ) that exploits robust depth priors for accurate 2D-to-3D lifting. Extensive experiments show that HS<sup>2</sup> Occ consistently outperforms monocular baselines and generalizes well to both unseen simulated test scenes and real-world environments, validating the effectiveness of the Real2Sim2Real design. Code and data will be available upon acceptance at `https://d-robotics-ai-lab.github.io/humanoid-omniocc` . 

## **1 Introduction** 

Reliable near-field 3D occupancy perception is essential for humanoid robots to navigate, manipulate, and interact safely within human-centered spaces. Among scene representations, occupancy grids strike a practical balance between fidelity and computability by estimating the free/occupied state of each voxel. This geometry-centric abstraction supports collision-aware planning, integrates naturally with semantics, and scales to real-time control loops. 

Most existing 3D occupancy datasets target _autonomous driving_ Behley et al. (2019); Wei et al. (2023); Wang et al. (2023a), emphasizing forward-facing views, long-range geometry, and largely static road scenes—assumptions that misalign with humanoid operation. Humanoids work _indoors_ , with _egocentric_ viewpoints, frequent occlusions, and _dynamic_ human activity; consequently, existing benchmarks underspecify the near-field, omnidirectional conditions where safety-critical interaction occurs. 

More recently, _embodied/indoor_ occupancy datasets have begun to emerge ( _e.g._ , HumanoidOcc Cui et al. (2025)), yet they are predominantly _monocular_ —prone to depth ambiguity and weak crossdomain generalization—or rely on _LiDAR_ , which is accurate but costly and cumbersome for headmounted humanoid platforms. As illustrated in Fig. 2, these existing perception paradigms either 

> †Work was done during an internship at D-Robotics. 

Preprint. 


Figure 1: Illustration of the proposed **Humanoid-OmniOcc** dataset. **Left:** Six representative scenes rendered in high photorealistic quality, covering diverse spatial layouts and material textures. **Right:** Visualization of one scene with four stereo RGB pairs ( _Front, Rear, Left, Right_ ), their corresponding depth maps, and voxelized occupancy labels. 

struggle with geometric reliability or incur prohibitive hardware costs. To break this bottleneck at both the data and algorithmic levels, we advocate for a stereo-centric approach. For near-field perception, _stereo_ offers a pragmatic middle ground: metrically grounded dense depth at arm’s reach with lower cost and easier deployment. Meanwhile, stereo depth estimation Guo et al. (2023, 2024, 2025a) has matured to a degree that makes it a strong source of depth priors. However, to our knowledge, _no_ surround-stereo occupancy dataset exists that aligns with humanoid robots’ 360<sup>_◦_</sup> egocentric sensing in indoor environments. 

We introduce **Humanoid-OmniOcc** , a _stereobased panoramic occupancy_ dataset tailored for humanoid perception, designed around a **Real2Sim2Real** closed-loop paradigm. Built on NVIDIA Isaac Sim, a head-like rig of _four synchronized stereo cameras_ provides fullsurround RGB. The Real2Sim2Real pipeline operates as follows: (i) _Real→Sim_ —physical sensor parameters (intrinsics, extrinsics, FoV, baseline) from the Unitree G1 robot are faithfully replicated in the simulator with photorealistic PBR and sensor-accurate camera models (Fig. 3); (ii) _Sim_ —large-scale training data with centimeter-level occupancy ground truth is generated via multi-view geometric verification across 15 globally diverse indoor styles; and (iii) _Sim→Real_ —models trained purely on simulated data are directly evaluated on real-world captures, with real-world performance feeding back to guide simulator refinement. **Fifteen** simulated scenes and **five** real-world environments are released in this paper, providing broad scene diversity. The configurable sensor stack enables seamless retargeting to specific hardware configurations. 


Figure 2: Comparison of different 3D perception paradigms. Top: Monocular-based model. Middle: Multi-sensor fusion model. Bottom: Our proposed stereo-based model. 

Along with the dataset, we propose the **HS**<sup>**2**</sup> **Occ** model family, which achieves state-of-the-art occupancy prediction by leveraging stereo-derived depth priors for robust 3D understanding in egocentric scenes. As shown in Tab. 2, our stereo-based model substantially outperforms monocular baselines on unseen test scenes while maintaining competitive results on the validation set, demonstrating stronger robustness. Furthermore, we evaluate all methods on real-world scenes to validate sim-toreal generalization. Comprehensive visualizations and ablation studies are provided to elucidate the properties of the proposed benchmark. 

**Contributions.** Our main contributions are as follows: 

2 

Table 1: **Dataset comparison.** Comparing our **OmniOcc** Datasets with other occupancy datasets. Surround refers to surround-view image inputs. C, D, L and R denote camera and depth, LiDAR and Radar. 

|**Dataset**|Publication|**Type**|**Surround**|**Modality**|**#Scenes**|**#Frames**|**Volume Size**|**Resolution(m)**|
|---|---|---|---|---|---|---|---|---|
|SemanticKITTIBehley et al.(2019)|ICCV2019|Outdoor|✗|C & L|22|9K|[32, 256, 256]|-|
|KITTI-360Liao et al.(2022)|TPAMI2022|Outdoor|✓|C & L|11|91K|[32, 256, 256]|[0.2, 0.2, 0.2]|
|SurroundOccWei et al.(2023)|ICCV2023|Outdoor|✓|C & L|-|-|[16, 200, 200]|[0.5, 0.5, 0.5]|
|OpenOccupancyWang et al.(2023a)|ICCV2023|Outdoor|✓|C & L|-|200K|[40, 512, 512]|-|
|Occ3D-nuScenesTian et al.(2023)|ArXiv2023|Outdoor|✓|C & L|16|40K|[16, 200, 200]|[0.4, 0.4, 0.4]|
|Occ3D-WaymoTian et al.(2023)|ArXiv2023|Outdoor|✓|C & L|14|200K|[128, 3200, 3200]|[0.05, 0.05, 0.05]|
|StereoVoxelNetLi et al.(2023a)|ICRA2023|Indoor&Outdoor|✗|Stereo & L|-|-|-|-|
|WildOccZhai et al.(2024)|ArXiv2024|Outdoor|✗|C & L|5|10K|[40, 100, 100]|[0.2, 0.2, 0.2]|
|OmniHD-ScenesZheng et al.(2025)|ArXiv2024|Outdoor|✓|C & L& R|200|60K|-|-|
|Co3SOPWu et al.(2025a)|ArXiv2025|Outdoor|✗|C & L|-|-|[70, 1000, 1000]|[0.1, 0.1, 0.1]|
|DSEC-SSCGuo et al.(2025b)|ArXiv2025|Outdoor|✗|S & L|6|3K|[16, 128, 128]|[0.4, 0.4, 0.4]|
|ORAD-3DMin et al.(2025)|ArXiv2025|Outdoor|✓|C & L|145|58K|[100, 100, 100]|-|
|SUNCGSong et al.(2017)|CVPR2017|Indoor|✗|C & D|46K|140K|[144, 240, 240]|-|
|Occ-ScanNetYu et al.(2024)|ECCV2024|Indoor|✗|C & L|-|65K|[36, 60, 60]|[0.08, 0.08, 0.08]|
|EmbodiedScanWang et al.(2023b)|CVPR2024|Indoor|✓|C & D|5,185|890K|[16, 40, 40]|-|
|<br>EmbodiedOccWu et al.(2025b)|ICCV2025|Indoor|✗|C & L|-|674|[36, 60, 60]|[0.08, 0.08, 0.08]|
|HumanoidOccCui et al.(2025)|ArXiv2025|Indoor|✓|C & L|-|40K|[24, 200, 200]|[0.1, 0.1, 0.1]|
|**Humanoid-OmniOcc**|**Ours**|Indoor|✓|**Stereo & D**|15|155K|[44, 384, 384]|[0.04, 0.04, 0.04]|


- We present **Humanoid-OmniOcc** , the first panoramic stereo-based occupancy dataset for humanoid robots, offering full 360<sup>_◦_</sup> visual coverage with dense semantic labels over 15 indoor categories, spanning 15 simulated scenes and 5 real-world environments, without relying on LiDAR. 

- We develop a physically grounded data generation pipeline on Isaac Sim following a Real2Sim2Real paradigm: sensor specifications drive simulation, simulation produces centimeter-level occupancy ground truth via multi-view stereo and geometric verification, and real-world evaluation closes the loop. 

- We propose **HS**<sup>**2**</sup> **Occ** , leveraging stereo-based depth priors to achieve state-of-the-art occupancy prediction and demonstrating strong robustness on both simulated test sets and real-world environments over monocular baselines. 

## **2 Related Work** 

### **2.1 Occupancy Perception Datasets** 

Recent progress in 3D occupancy prediction has been largely driven by large-scale benchmarks Wang et al. (2023a); Wei et al. (2023); Tian et al. (2023). OpenOccupancy Wang et al. (2023a) improves voxel completeness through an Augmenting and Purifying (AAP) pipeline, supported by roughly 4000 hours of human annotation and verification to ensure high-fidelity occupancy reconstruction. SurroundOcc Wei et al. (2023) fuses multi-frame LiDAR sweeps via Poisson reconstruction to obtain dense occupancy maps of dynamic and static scenes. Occ3D Tian et al. (2023) introduces two large-scale benchmarks—Occ3D-Waymo and Occ3D-nuScenes—featuring an automated annotation pipeline composed of voxel densification, occlusion reasoning, and image-guided refinement. These efforts collectively establish strong baselines for occupancy-based 3D scene understanding, yet most remain designed for autonomous driving scenarios with meter-level resolution, limiting their direct applicability to humanoid robotics where near-field accuracy and fine-grained articulation reasoning are required. For indoor scenes, EmbodiedScan Wang et al. (2024a) introduces a multimodal, egocentric 3D perception dataset and benchmark designed for comprehensive 3D scene understanding in embodied environments. HumanoidOcc Cui et al. (2025) provides a panoramic occupancy benchmark tailored to humanoid robots, which integrates six monocular cameras and one LiDAR sensor mounted around the robot’s head to achieve full-surround visual coverage with accurate spatial alignment. 

### **2.2 3D Occupancy Prediction** 

3D occupancy prediction has emerged as a key direction in scene understanding and embodied perception. MonoScene Cao and De Charette (2022) pioneered camera-based occupancy perception. TPVFormer Huang et al. (2023) introduces a tri-perspective view representation framework that reconstructs 3D geometry from 2D visual cues through three orthogonal projections. FB-Occ Li et al. (2023b) refines geometric reasoning through a bidirectional projection mechanism, allowing improved 

3 

visibility modeling in occlusion-prone regions. FlashOcc Yu et al. (2023) focuses on computational efficiency, compressing voxel features to achieve real-time inference without significant accuracy degradation. More recently, GaussianFormer Huang et al. (2024) and GaussianFormerV2 Huang et al. (2025) introduce 3D semantic Gaussians to represent scene geometry and semantics. EmbodiedOcc Wu et al. (2025c) utilizes 3D Gaussian to represent indoor scenes in a continuous volumetric form. Beyond pure camera-based systems, multimodal fusion frameworks have been widely explored to overcome the inherent limitations of single-sensor perception. OccFusion Ming et al. (2024) introduces voxel-level cross-modal attention, allowing asynchronous RGB and LiDAR inputs to collaboratively predict high-density occupancy maps. Despite notable progress, monocular-based methods often struggle with depth ambiguity and occlusion sensitivity, while LiDAR-based solutions, though accurate, are costly and difficult to deploy at scale. 

### **2.3 Stereo Matching** 

Deep learning-based stereo matching frameworks typically **comprise** four key stages: feature extraction, cost volume construction, cost aggregation, and disparity regression. Existing methods **are** broadly categorized into two families—accuracy-oriented and efficiency-oriented approaches. Accuracy-focused networks Chang and Chen (2018); Guo et al. (2019); Cheng et al. (2020); Xu et al. (2022); Guo et al. (2023) substantially improve disparity estimation precision by constructing high-dimensional cost volumes and performing 3D convolutional aggregation to refine matching consistency. Meanwhile, iterative optimization-based methods Xu et al. (2023a, 2025, 2023b); Guo et al. (2023); Wang et al. (2024b) achieve state-of-the-art accuracy through recurrent optimization within the disparity space, further improving depth continuity and geometric fidelity. In contrast, efficiency-oriented methods Guo et al. (2025a); Bangunharcana et al. (2021); Wang et al. (2020); Duggal et al. (2019); Shamsafar et al. (2022); Khamis et al. (2018) seek to reduce computational complexity by constructing compact or downsampled cost volumes, while maintaining reasonable accuracy for real-time deployment. In addition, several recent approaches have been designed specifically to improve temporal coherence in stereo video processing Jing et al. (2024a,b, 2025), ensuring that disparities remain stable over time. Recent foundation models such as FoundationStereo Wen et al. (2025), and StereoAnything Guo et al. (2024) further extend stereo generalization by leveraging tens of millions of diverse training pairs Guo et al. (2024) and pretraining with depth-aware priors like DepthAnything Yang et al. (2024a,b). OccDepth Miao et al. (2023), StereoScene Li et al. (2024), and Stereovoxelnet Li et al. (2023a) incorporate stereo matching into occupancy prediction and achieve promising results. Furthermore, Cvt-Occ Ye et al. (2024) introduces a temporal cost volume framework tailored for multi-view and multi-frame occupancy prediction. However, these methods are limited to front-view stereo settings, and no surround-stereo occupancy prediction framework has been explored due to the lack of corresponding datasets. 

## **3 Humanoid-OmniOcc Dataset** 

### **3.1 Real2Sim2Real Design Philosophy** 

Humanoid-OmniOcc is built around a **Real2Sim2Real** closed-loop paradigm that tightly couples simulation with real-world deployment, as illustrated below. 

**Real** **_→_ Sim.** The physical sensor configuration of the Unitree G1 robot—including stereo camera intrinsics, extrinsics, baseline (6 cm), field of view, and mounting geometry—is precisely replicated in NVIDIA Isaac Sim. Photorealistic physically-based rendering (PBR) with calibrated material properties and lighting further minimizes the visual domain gap, ensuring that the simulated observations closely match real sensor outputs. 

**Sim (Data Generation).** With the sensor-accurate digital twin in place, we generate large-scale training data with pixel-accurate dense annotations that would be prohibitively expensive to obtain in the real world. The simulator produces centimeter-level occupancy ground truth, per-voxel semantic labels across 15 categories, and metrically calibrated depth maps—all automatically and at scale (155K+ samples across 15 diverse indoor scenes). 

**Sim** **_→_ Real.** Models trained exclusively on simulated data are deployed and evaluated on real-world captures from the same Unitree G1 platform in five distinct indoor environments (Bar, Corridor, Office, Apartment). The real-world evaluation quantitatively measures the sim-to-real transfer gap and 

4 

reveals domain-specific failure modes ( _e.g._ , lighting discrepancies, material reflectance mismatch), which in turn inform iterative refinement of the simulation parameters—closing the Real2Sim2Real loop. 

This closed-loop design ensures that the benchmark is not a one-off simulation artifact but a continuously improvable pipeline tightly coupled with real-world deployment requirements. 

### **3.2 Virtual Scene Setup** 

We construct diverse virtual indoor environments using _Isaac Sim_ to emulate realistic object layouts, illumination conditions, and physical interactions, providing a controllable and reproducible foundation for data collection. The scenes span a wide range of global interior styles—including Scandinavian minimalism, Baroque luxury, and modern industrial design—capturing the diversity of real-world indoor environments across different cultural and aesthetic contexts. Each environment contains static objects ( _e.g._ , tables, chairs, cabinets, walls), all assigned physically accurate attributes including material reflectivity, collision dynamics, and lighting parameters, ensuring faithful simulation of real-world photometric and geometric behavior. 

**Data quality, diversity, and scalability.** We prioritize sim-to-real fidelity via photorealistic physically-based rendering (PBR) and sensor-accurate camera emulation (intrinsics/extrinsics, noise, FoV, baseline), enabling direct retargeting to specific hardware. Ground-truth occupancy is produced at centimeter-level precision via multi-view geometric verification, yielding high-accuracy labels at low cost with high collection throughput. 

### **3.3 Omnidirectional Stereo Configuration** 

As shown in Fig. 3, four stereo camera modules are mounted on the Unitree G1’s head facing the _front_ , _rear_ , _left_ , and _right_ directions, forming a panoramic stereo perception system. Each stereo pair performs depth estimation through disparity computation, ensuring 360<sup>_◦_</sup> spatial coverage. In our setup, we employ stereo cameras with a resolution of 1280 _×_ 1080, a baseline of 6 cm, and a focal length of 596 _._ 81 pixels. The field of view (FOV) of the raw distorted images is approximately 106<sup>_◦_</sup> horizontally and 86<sup>_◦_</sup> vertically ( _±_ 3<sup>_◦_</sup> ), which becomes 93<sup>_◦_</sup> (H) and 83<sup>_◦_</sup> (V) ( _±_ 3<sup>_◦_</sup> ) after stereo rectification. Intrinsic and extrinsic parameters of all cameras are calibrated and recorded to support precise spatial alignment. 


Figure 3: The data collection setup, featuring the CAD model of the stereo head (left) alongside its integration into the physical humanoid robot (right). 

### **3.4 Autonomous Data Collection via Dynamic Window Approach** 

To capture realistic motion and viewpoint diversity, an autonomous navigation policy based on the Dynamic Window Approach (DWA) is integrated into the robot control system. DWA samples feasible linear and angular velocity commands under velocity and acceleration constraints, predicts short-term trajectories, and scores them according to goal alignment, obstacle clearance, and motion smoothness. The optimal velocity command is executed to ensure safe, collision-free navigation. During navigation, synchronized stereo image pairs and robot poses are continuously recorded for subsequent ground-truth generation. 

An overview of the Humanoid-OmniOcc dataset, ground truth generation in both simulation and the real world, as well as additional analyses of the dataset, are provided in the _Supplementary Material_ . 

5 


Figure 4: **The pipeline of our proposed HS**<sup>**2**</sup> **Occ framework.** 

## **4 HS**<sup>**2**</sup> **OccModel** 

### **4.1 Task Definition** 

As shown in Figure 4, given synchronized multi-view stereo inputs, the objective of our task is to infer the 3D occupancy state of each voxel within the surrounding environment. Specifically, the model receives frames captured from four stereo pairs positioned at the front, back, left, and right of the humanoid platform, denoted as _{Ii_<sup>_l, I_</sup> _i_<sup>_r} ⊂_R</sup><sup>_Hi×Wi×_3, where</sup><sup>_i_= 1</sup><sup>_, ...,_4.Each stereo pair is</sup> calibrated with known intrinsics _{_ **K**<sup>_l_</sup> _i_<sup>_,_</sup><sup>**K**</sup><sup>_r_</sup> _i_<sup>_}_and extrinsics</sup><sup>_{_</sup><sup>**T**</sup> _i_<sup>_l,_</sup><sup>**T**</sup><sup>_r_</sup> _i_<sup>_}_relative to the robot frame.The</sup> network predicts a volumetric occupancy grid _O_<sup>ˆ</sup> _∈{_ 0 _,_ 1 _}_<sup>_X×Y ×Z_</sup> , where each voxel represents an _occupancy state_ (free, occupied). 

### **4.2 Feature Extraction** 

**Multi-view encoding.** Eight synchronized RGB images from four stereo pairs ( _front_ , _back_ , _left_ , and _right_ ) are encoded by a shared 2D backbone _E_ into multi-scale feature maps _{Fi_<sup>_l, F_</sup> _i_<sup>_r}_, where</sup> _i ∈{_ 1 _,_ 2 _,_ 3 _,_ 4 _}_ corresponds to the four viewing directions, and the superscripts _l_ and _r_ denote the left and right images of each stereo pair, respectively. 

### **4.3 Stereo Depth Network** 

To model pixel correspondences along potential disparities, a differentiable cost volume _Ci_<sup>disp</sup> is constructed over disparity hypotheses _d ∈_ [0 _, D_ max] as: 


where _Ci_<sup>disp</sup> ( _u, v, d,_ :) encodes the similarity between left and right feature embeddings. 

Disparity-based cost volumes suffer from non-uniform depth sensitivity, as the same disparity shift corresponds to larger depth variations at greater distances. To alleviate this issue, we transform _Ci_<sup>disp</sup> into a depth-oriented cost representation _Ci_<sup>depth</sup> using bilinear interpolation guided by the depth-todisparity relation. This reformulation aligns the convolutional operations with actual geometric depth, ensuring equal treatment across different distance ranges. 

The depth cost volume _Ci_<sup>depth</sup> is processed by a series of 3D convolutions to generate the aggregated depth feature volume _Si_<sup>depth</sup> . _Si_<sup>depth</sup> is then used to regress pixel-wise depth via a softmax-weighted expectation: 


where _Zi_<sup>_l_(</sup><sup>_u, v_) denotes the predicted metric depth of the left image.This depth-based formulation</sup> leads to smoother and more stable predictions, particularly for far-range regions. 

6 

### **4.4 2D-to-3D Transformer** 

We lift only _left-view_ features into a robot-centric voxel grid _V_ using depth-discretized splatting guided by the left camera’s stereo-derived depth posterior. 

Let _I_ = _{_ 1 _,_ 2 _,_ 3 _,_ 4 _}_ index the four stereo rigs (front/back/left/right). For the left camera of rig _i_ , denote its intrinsics and extrinsics by **K**<sup>_l_</sup> _i_<sup>and</sup><sup>**T**</sup><sup>_l_</sup> _i_<sup>(robot frame), and the left-view feature map by</sup><sup>_F l_</sup> _i_<sup>.</sup> For a pixel **x** = ( _u, v_ ) and discretized depth bins _{zk}_<sup>_K_</sup> _k_ =1<sup>, the back-projected 3D point in the robot</sup> frame is 


With trilinear splatting _ϕ_ ( _·→ v_ ) and a feature projector _P_ , the camera-to-voxel aggregation becomes 


where _qi_ ( **x** _, k_ ) is the _left-view_ stereo depth posterior from Sec. 4.3. A lightweight transformer refines _V_ cam by aggregating multi-view context along camera rays. 

### **4.5 Occupancy Head and Loss** 

The occupancy head consumes the lifted voxel feature map _V_ cam _∈_ R<sup>_X×Y ×Z×D_</sup> and predicts pervoxel logits **o** ( _v_ ) _∈_ R<sup>_C_occ</sup> using a lightweight 3D decoder composed of sparse convolution and trilinear upsampling layers. A softmax classifier converts logits to occupancy probabilities. Following FB-Occ Li et al. (2023b), we supervise the predicted occupancy map _O_<sup>ˆ</sup> with a weighted composite loss: 


In parallel, the stereo depth prediction (Sec. 4.3) is supervised with binary cross-entropy over discretized depth bins. The full objective function couples voxel occupancy and stereo depth supervision: 


This joint optimization framework aligns appearance, depth, and volumetric reasoning. Notably, the stereo posterior _qi_ ( **x** _, k_ ) (Eq. 5) guides voxel lifting, while occupancy gradients implicitly regularize depth prediction by enforcing geometric consistency within 3D space. 

## **5 Experiments** 

### **5.1 Implementation Details.** 

All experiments are conducted on a cluster equipped with 16 NVIDIA H20 GPUs. The network is trained for 10 epochs using the AdamW optimizer with a learning rate of 4 _×_ 10<sup>_−_4</sup> . We set the batch size to 32. All input images are resized to 544 _×_ 640 before training and inference. For LightStereo Guo et al. (2025a), COEX Bangunharcana et al. (2021), and IGEV Xu et al. (2023a) stereo models, we initialize the models with StereoAnything Guo et al. (2024) pretrained weights to leverage large-scale stereo correspondence priors. For FoundationStereo Wen et al. (2025), we adopt the official pretrained weights released by the authors. We adapt FB-Occ Li et al. (2023b), FlashOcc Yu et al. (2023), and SurroundOcc Wei et al. (2023) (originally designed for nuScenes with 6 surround-view cameras) to a 4-view input setting using the left images from each stereo pair. 

### **5.2 Evaluation Metrics** 

Following SurroundOcc Wei et al. (2023), we evaluate semantic occupancy using the per-class intersection-over-union (IoU) and the mean IoU over valid classes (mIoU), which jointly measure geometric consistency and fine-grained semantic recognition. 

7 

Table 2: Semantic occupancy prediction results on the **test** sets and in the real world. We report per-class IoU and mIoU (%). 

|Method|Input|IoU|mIoU|■floor|■partitions|■door|■chair|■table|■sofa|■bed|■appliance|■cabinet|■carpet|■plant|■objects|■suspended|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||_Test Se_|_t_||||||||||
|FB-OccLi et al.(2023b)|Mono|28.59|5.11|36.76|6.07|4.44|2.24|2.32|0.82|1.43|0.00|4.27|2.31|4.13|1.68|0.01|
|FlashOccYu et al.(2023)|Mono|18.05|1.71|16.69|1.87|1.72|0.08|0.09|0.05|0.00|0.02|0.56|0.06|0.01|1.14|0.00|
|SurroundOccWei et al.(2023)|Mono|24.71|6.86|28.22|8.10|2.17|4.62|14.65|7.96|5.93|0.01|7.81|2.34|2.88|4.53|0.01|
|GaussianFormerHuang et al.(20<br>|24)<br>Mono|26.15|5.84|33.43|5.03|1.20|4.47|6.54|2.38|5.19|0.09|6.11|5.31|3.09|3.11|0.00|
|HS<sup>2</sup>Occ (Ours)|Stereo|29.67|11.69|50.85|4.50|12.97|5.17|6.95|9.57|9.77|7.05|16.71|8.02|10.58|9.70|0.12|
|||||||_Real Wor_|_ld_||||||||||
|FB-OccLi et al.(2023b)|Mono|12.22|2.42|8.30|3.92|0.00|3.90|4.54|4.88|0.00|0.00|2.41|1.61|0.23|1.59|0.04|
|FlashOccYu et al.(2023)|Mono|15.39|2.42|18.21|4.58|0.00|1.58|0.82|1.63|0.00|0.00|0.91|0.26|1.29|0.88|1.36|
|SurroundOcWei et al.(2023)|Mono|20.35|8.89|26.76|10.18|1.48|10.72|10.63|16.21|18.23|0.06|4.81|0.09|1.44|4.45|10.47|
|GaussianFormerHuang et al.(20<br>|24)<br>Mono|17.11|5.30|21.55|7.22|0.86|9.32|6.98|6.51|1.90|0.00|2.75|1.40|2.14|6.25|2.01|
|HS<sup>2</sup>Occ (Ours)|Stereo|35.45|19.26|51.31|14.29|7.77|22.31|22.43|34.74|34.93|1.64|13.52|11.40|11.57|12.12|12.34|


### **5.3 Main Results** 

Table 2 summarizes voxel-level semantic occupancy prediction on the Humanoid-OmniOcc **test** set and real-world captures. We compare our proposed **HS**<sup>**2**</sup> **Occ** with four SOTA monocular occupancy prediction models: FB-Occ Li et al. (2023b) (CVPR’23 3D occupancy prediction champion method), FlashOcc Yu et al. (2023), SurroundOcc Wei et al. (2023) and GaussianFormer Huang et al. (2024). On the test set, our stereo-based **HS**<sup>2</sup> **Occ** achieves the best overall performance with 29.67 IoU and 11.69 mIoU, outperforming the strongest monocular baseline (FB-Occ: 28.59 IoU / 5.11 mIoU), indicating notably better semantic completeness on indoor long-tail categories. More importantly, HS<sup>2</sup> Occ generalizes strongly to real-world scenes under the Real2Sim2Real protocol, reaching 35.45 IoU and 19.26 mIoU, which exceeds the best monocular results (best IoU: 15.39, best mIoU: 5.34). Per-class results further show that stereo depth priors substantially improve interaction-relevant semantics and thin structures: on the test set, HS<sup>2</sup> Occ boosts _floor_ (50.85), _door_ (12.97), and _cabinet_ (16.71), while maintaining non-trivial IoUs for object-centric classes where monocular methods often collapse; in real-world evaluation, HS<sup>2</sup> Occ achieves strong recognition for _chair/table/sofa/bed_ (22.31/22.43/34.74/34.93), validating robust 2D-to-3D lifting under domain shift. 

### **5.4 Ablation study** 

Our dataset and model primarily focus on the stereo-based setting, aiming to explore how binocular perception contributes to accurate and stable occupancy prediction. Therefore, we keep the occupancy head and training protocol fixed, and ablate the stereo component by plugging in different stereo backbones while using the same surround stereo inputs and 2D-to-3D lifting pipeline. 

**Ablation study on Stereo module.** As shown in Tab. 3, FoundationStereo Wen et al. (2025) achieves the best overall semantic occupancy performance, particularly on real-world data, demonstrating that stronger and more robust disparity estimation can substantially improve downstream occupancy prediction quality. Overall, these results confirm that occupancy quality is highly sensitive to stereo depth reliability: a stronger stereo model can significantly enhance semantic completeness and real-world generalization, motivating our use of FoundationStereo Wen et al. (2025) as the default stereo backbone. 

**Ablation Study on Disparity-to-Depth Formulation.** As shown in Tab. 4, compared with DDVM, SDN consistently improves occupancy on both the test set (IoU/mIoU: 28.04/10.07 _→_ 29.67/11.69) and real-world data (32.80/17.03 _→_ 35.45/19.26). 

### **5.5 Qualitative Comparisons** 

As shown in Figure 5, our stereo-based model ( **HS**<sup>**2**</sup> **Occ** ) generates more complete and geometrically consistent occupancy reconstructions than the monocular baseline Flash-Occ, FB-Occ, and SurroundOcc. Across both test scenes and real-world environments, **HS**<sup>**2**</sup> **Occ** preserves stable geometric structures and clear spatial layouts, highlighting its strong robustness and superior sim-to-real generalization capability. 

8 

Table 3: Ablation Study on Stereo module. 

|Stereo|IoU|mIoU|■floor|■partitions|■door|■chair|■table|■sofa|■bed|■appliance|■cabinet|■carpet|■plant|■objects|■suspended|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||_T_|_est Set_||||||||||
|LStereo-SGuo et al.(2025a)|33.46|6.55|39.33|6.06|0.00|6.31|12.37|3.40|6.44|0.21|5.37|0.14|1.64|3.87|0.00|
|LStereo-LGuo et al.(2025a)|35.11|8.09|42.73|6.62|0.08|7.26|15.21|4.49|9.25|0.03|6.51|0.88|8.54|3.57|0.00|
|<br>COEXBangunharcana et al.(202|1)<br>31.17|5.20|43.24|2.49|0.01|5.14|7.40|0.54|1.88|0.02|3.46|0.31|0.57|2.51|0.00|
|<br>IGEVXu et al.(2023a)|27.59|5.59|36.01|2.98|0.02|6.56|10.88|2.52|0.47|0.07|2.97|0.09|6.58|3.57|0.00|
|<br>FDSWen et al.(2025)|29.67|11.69|50.85|4.50|12.97|5.17|6.95|9.57|9.77|7.05|16.71|8.02|10.58|9.70|0.12|
||||||_Rea_|_l World_||||||||||
|LStereo-SGuo et al.(2025a)|33.69|9.00|44.86|13.61|3.81|5.33|14.88|16.08|0.86|0.17|5.43|2.62|0.99|7.54|0.76|
|LStereo-LGuo et al.(2025a)|33.66|9.78|43.52|18.51|0.18|11.32|13.88|15.73|2.87|0.05|6.00|0.33|7.01|7.37|0.36|
|<br>COEXBangunharcana et al.(202|1)<br>30.07|6.96|43.48|11.78|0.06|6.30|12.94|5.90|0.44|0.04|1.82|0.00|1.65|5.95|0.07|
|<br>IGEVXu et al.(2023a)|28.22|9.32|42.41|9.55|0.65|10.70|13.20|27.65|0.00|0.98|4.34|0.19|4.66|6.89|0.00|
|FDSWen et al.(2025)|35.45|19.26|51.31|14.29|7.77|22.31|22.43|34.74|34.93|1.64|13.52|11.40|11.57|12.12|12.34|


Table 4: Ablation Study on Disparity-to-Depth: DDVM Chen et al. <u>(2025) vs.</u> SDN. 

|Stereo<br>Di|sp2Depth|IoU<br>mIoU|■floor<br>■partitions<br>■door<br>_Test_|■chair<br>■table<br>■sofa<br>■bed<br>■appliance<br>_Set_|■cabinet<br>■carpet|■plant<br>■objects<br>■suspended|
|---|---|---|---|---|---|---|
|FDSWen et al.(2025)<br><br>FDSWen et al.(2025)|DDVM<br>SDN|28.04<br>10.07<br>29.67<br>11.69|50.87<br>6.55<br>4.85<br>50.85<br>4.50<br>12.97<br>_Real_|6.39<br>13.95<br>7.31<br>3.29<br>0.18<br>5.17<br>6.95<br>9.57<br>9.77<br>7.05<br>_World_|6.65<br>17.74<br>16.71<br>8.02|6.36<br>6.80<br>0.00<br>10.58<br>9.70<br>0.12|
|FDSWen et al.(2025)<br><br>FDSWen et al.(2025)|DDVM<br>SDN|32.80<br>17.03<br>35.45<br>19.26|47.92<br>18.06<br>5.95<br>51.31<br>14.29<br>7.77|24.84<br>22.29<br>29.58<br>31.15<br>0.82<br>22.31<br>22.43<br>34.74<br>34.93<br>1.64|5.56<br>4.21<br>13.52<br>11.40|14.53<br>10.99<br>5.45<br>11.57<br>12.12<br>12.34|
|Testset|||||||
|Office|||||||
|ppartment|||||||
|A<br>Images|Fla|sh-Occ|FB-Occ|SurrOcc<br>HS<sup>2</sup>Oc|c(Ours)|GT|


Figure 5: **Qualitative comparisons on the test set (first row) and real-world scenes (rows 2–3).** The first column shows the left images from the four stereo pairs ( _front_ , _back_ , _left_ , and _right_ ). 

## **6 Conclusion** 

In this work, we presented Humanoid-OmniOcc, a panoramic stereo-based occupancy benchmark for embodied humanoid perception, featuring high-quality voxel-level annotations across diverse simulated and real-world indoor environments. By aligning simulation with real sensor configurations under a Real2Sim2Real paradigm, the benchmark enables scalable training while preserving strong sim-to-real consistency. Based on this dataset, we introduced HS<sup>2</sup> Occ, a stereo-guided occupancy network that exploits reliable depth priors for improved 2D-to-3D lifting. Experimental results show that stereo cues significantly enhance geometric fidelity and generalization ability over monocular baselines, especially under real-world domain shifts. Overall, our results highlight the importance of stereo-aware perception and realistic simulation design for embodied 3D understanding. We hope Humanoid-OmniOcc can serve as a foundation for future research in omnidirectional perception, humanoid navigation, and interactive embodied intelligence. 

9 

## **References** 

- J. Behley, M. Garbade, A. Milioto, J. Quenzel, S. Behnke, C. Stachniss, and J. Gall. SemanticKITTI: A Dataset for Semantic Scene Understanding of LiDAR Sequences. In _ICCV_ , 2019. 1, 3 

- Yi Wei, Linqing Zhao, Wenzhao Zheng, Zheng Zhu, Jie Zhou, and Jiwen Lu. Surroundocc: Multicamera 3d occupancy prediction for autonomous driving. In _ICCV_ , 2023. 1, 3, 7, 8 

- Xiaofeng Wang, Zheng Zhu, Wenbo Xu, Yunpeng Zhang, Yi Wei, Xu Chi, Yun Ye, Dalong Du, Jiwen Lu, and Xingang Wang. Openoccupancy: A large scale benchmark for surrounding semantic occupancy perception. In _ICCV_ , 2023a. 1, 3 

- Wei Cui, Haoyu Wang, Wenkang Qin, Yijie Guo, Gang Han, Wen Zhao, Jiahang Cao, Zhang Zhang, Jiaru Zhong, Jingkai Sun, Pihai Sun, Shuai Shi, Botuo Jiang, Jiahao Ma, Jiaxu Wang, Hao Cheng, Zhichao Liu, Yang Wang, Zheng Zhu, Guan Huang, Jian Tang, and Qiang Zhang. Humanoid occupancy: Enabling a generalized multimodal occupancy perception system on humanoid robots, 2025. URL `https://arxiv.org/abs/2507.20217` . 1, 3 

- Xianda Guo, Juntao Lu, Chenming Zhang, Yiqi Wang, Yiqun Duan, Tian Yang, Zheng Zhu, and Long Chen. Openstereo: A comprehensive benchmark for stereo matching and strong baseline. _arXiv preprint arXiv:2312.00343_ , 2023. 2, 4 

- Xianda Guo, Chenming Zhang, Youmin Zhang, Dujun Nie, Ruilin Wang, Wenzhao Zheng, Matteo Poggi, and Long Chen. Stereo anything: Unifying stereo matching with large-scale mixed data. _arXiv preprint arXiv:2411.14053_ , 2024. 2, 4, 7 

- Xianda Guo, Chenming Zhang, Youmin Zhang, Wenzhao Zheng, Dujun Nie, Matteo Poggi, and Long Chen. Lightstereo: Channel boost is all you need for efficient 2d cost aggregation. In _ICRA_ , 2025a. 2, 4, 7, 9 

- Yiyi Liao, Jun Xie, and Andreas Geiger. Kitti-360: A novel dataset and benchmarks for urban scene understanding in 2d and 3d. _TPAMI_ , 2022. 3 

- Xiaoyu Tian, Tao Jiang, Longfei Yun, Yucheng Mao, Huitong Yang, Yue Wang, Yilun Wang, and Hang Zhao. Occ3d: A large-scale 3d occupancy prediction benchmark for autonomous driving, 2023. URL `https://arxiv.org/abs/2304.14365` . 3 

- Hongyu Li, Zhengang Li, Neset Unver Akmandor, Huaizu Jiang, Yanzhi Wang, and Taskin Padir. Stereovoxelnet: Real-time obstacle detection based on occupancy voxels from a stereo camera using deep neural networks. In _ICRA_ , 2023a. 3, 4 

- Heng Zhai, Jilin Mei, Chen Min, Liang Chen, Fangzhou Zhao, and Yu Hu. Wildocc: A benchmark for off-road 3d semantic occupancy prediction, 2024. URL `https://arxiv.org/abs/2410.15792` . 3 

- Lianqing Zheng, Long Yang, Qunshu Lin, Wenjin Ai, Minghao Liu, Shouyi Lu, Jianan Liu, Hongze Ren, Jingyue Mo, Xiaokai Bai, Jie Bai, Zhixiong Ma, and Xichan Zhu. Omnihd-scenes: A next-generation multimodal dataset for autonomous driving, 2025. URL `https://arxiv.org/ abs/2412.10734` . 3 

- Hanlin Wu, Pengfei Lin, Ehsan Javanmardi, Naren Bao, Bo Qian, Hao Si, and Manabu Tsukada. A synthetic benchmark for collaborative 3d semantic occupancy prediction in v2x autonomous driving, 2025a. URL `https://arxiv.org/abs/2506.17004` . 3 

- Shangwei Guo, Hao Shi, Song Wang, Xiaoting Yin, Kailun Yang, and Kaiwei Wang. Event-aided semantic scene completion, 2025b. URL `https://arxiv.org/abs/2502.02334` . 3 

- Chen Min, Jilin Mei, Heng Zhai, Shuai Wang, Tong Sun, Fanjie Kong, Haoyang Li, Fangyuan Mao, Fuyang Liu, Shuo Wang, Yiming Nie, Qi Zhu, Liang Xiao, Dawei Zhao, and Yu Hu. Advancing off-road autonomous driving: The large-scale orad-3d dataset and comprehensive benchmarks, 2025. URL `https://arxiv.org/abs/2510.16500` . 3 

- Shuran Song, Fisher Yu, Andy Zeng, Angel X. Chang, Manolis Savva, and Thomas Funkhouser. Semantic scene completion from a single depth image. In _CVPR_ , 2017. 3 

10 

- Hongxiao Yu, Yuqi Wang, Yuntao Chen, and Zhaoxiang Zhang. Monocular occupancy prediction for scalable indoor scenes. In _ECCV_ , 2024. 3 

- Tai Wang, Xiaohan Mao, Chenming Zhu, Runsen Xu, Ruiyuan Lyu, Peisen Li, Xiao Chen, Wenwei Zhang, Kai Chen, Tianfan Xue, Xihui Liu, Cewu Lu, Dahua Lin, and Jiangmiao Pang. Embodiedscan: A holistic multi-modal 3d perception suite towards embodied ai, 2023b. URL `https://arxiv.org/abs/2312.16170` . 3 

- Yuqi Wu, Wenzhao Zheng, Sicheng Zuo, Yuanhui Huang, Jie Zhou, and Jiwen Lu. Embodiedocc: Embodied 3d occupancy prediction for vision-based online scene understanding. In _ICCV_ , 2025b. 3 

- Tai Wang, Xiaohan Mao, Chenming Zhu, Runsen Xu, Ruiyuan Lyu, Peisen Li, Xiao Chen, Wenwei Zhang, Kai Chen, Tianfan Xue, et al. Embodiedscan: A holistic multi-modal 3d perception suite towards embodied ai. In _CVPR_ , 2024a. 3 

- Anh-Quan Cao and Raoul De Charette. Monoscene: Monocular 3d semantic scene completion. In _CVPR_ , 2022. 3 

- Yuanhui Huang, Wenzhao Zheng, Yunpeng Zhang, Jie Zhou, and Jiwen Lu. Tri-perspective view for vision-based 3d semantic occupancy prediction. In _CVPR_ , 2023. 3 

- Zhiqi Li, Zhiding Yu, David Austin, Mingsheng Fang, Shiyi Lan, Jan Kautz, and Jose M Alvarez. Fb-occ: 3d occupancy prediction based on forward-backward view transformation. _arXiv preprint arXiv:2307.01492_ , 2023b. 3, 7, 8 

- Zichen Yu, Changyong Shu, Jiajun Deng, Kangjie Lu, Zongdai Liu, Jiangyong Yu, Dawei Yang, Hui Li, and Yan Chen. Flashocc: Fast and memory-efficient occupancy prediction via channel-to-height plugin. _arXiv preprint arXiv:2311.12058_ , 2023. 4, 7, 8 

- Yuanhui Huang, Wenzhao Zheng, Yunpeng Zhang, Jie Zhou, and Jiwen Lu. Gaussianformer: Scene as gaussians for vision-based 3d semantic occupancy prediction. In _ECCV_ , 2024. 4, 8 

- Yuanhui Huang, Amonnut Thammatadatrakoon, Wenzhao Zheng, Yunpeng Zhang, Dalong Du, and Jiwen Lu. Gaussianformer-2: Probabilistic gaussian superposition for efficient 3d occupancy prediction. In _CVPR_ , 2025. 4 

- Yuqi Wu, Wenzhao Zheng, Sicheng Zuo, Yuanhui Huang, Jie Zhou, and Jiwen Lu. Embodiedocc: Embodied 3d occupancy prediction for vision-based online scene understanding. In _ICCV_ , 2025c. 4 

- Zhenxing Ming, Julie Stephany Berrio, Mao Shan, and Stewart Worrall. Occfusion: Multi-sensor fusion framework for 3d semantic occupancy prediction. _TIV_ , 2024. 4 

- Jia-Ren Chang and Yong-Sheng Chen. Pyramid stereo matching network. In _CVPR_ , 2018. 4 

- Xiaoyang Guo, Kai Yang, Wukui Yang, Xiaogang Wang, and Hongsheng Li. Group-wise correlation stereo network. In _CVPR_ , 2019. 4 

- Xuelian Cheng, Yiran Zhong, Mehrtash Harandi, Yuchao Dai, Xiaojun Chang, Hongdong Li, Tom Drummond, and Zongyuan Ge. Hierarchical neural architecture search for deep stereo matching. In _NeurIPS_ , 2020. 4 

- Gangwei Xu, Junda Cheng, Peng Guo, and Xin Yang. Attention concatenation volume for accurate and efficient stereo matching. In _CVPR_ , 2022. 4 

- Gangwei Xu, Xianqi Wang, Xiaohuan Ding, and Xin Yang. Iterative geometry encoding volume for stereo matching. In _CVPR_ , 2023a. 4, 7, 9 

- Gangwei Xu, Xianqi Wang, Zhaoxing Zhang, Junda Cheng, Chunyuan Liao, and Xin Yang. Igev++: iterative multi-range geometry encoding volumes for stereo matching. _TPAMI_ , 2025. 4 

- Gangwei Xu, Yun Wang, Junda Cheng, Jinhui Tang, and Xin Yang. Accurate and efficient stereo matching via attention concatenation volume. _TPAMI_ , 2023b. 4 

11 

- Xianqi Wang, Gangwei Xu, Hao Jia, and Xin Yang. Selective-stereo: Adaptive frequency information selection for stereo matching. In _CVPR_ , 2024b. 4 

- Antyanta Bangunharcana, Jae Won Cho, Seokju Lee, In So Kweon, Kyung-Soo Kim, and Soohyun Kim. Correlate-and-excite: Real-time stereo matching via guided cost volume excitation. In _IROS_ , 2021. 4, 7, 9 

- Qiang Wang, Shaohuai Shi, Shizhen Zheng, Kaiyong Zhao, and Xiaowen Chu. FADNet: A fast and accurate network for disparity estimation. In _ICRA_ , 2020. 4 

- Shivam Duggal, Shenlong Wang, Wei-Chiu Ma, Rui Hu, and Raquel Urtasun. Deeppruner: Learning efficient stereo matching via differentiable patchmatch. In _ICCV_ , 2019. 4 

- Faranak Shamsafar, Samuel Woerz, Rafia Rahim, and Andreas Zell. Mobilestereonet: Towards lightweight deep networks for stereo matching. In _WACV_ , 2022. 4 

- Sameh Khamis, Sean Fanello, Christoph Rhemann, Adarsh Kowdle, Julien Valentin, and Shahram Izadi. Stereonet: Guided hierarchical refinement for real-time edge-aware depth prediction. In _ECCV_ , 2018. 4 

- Junpeng Jing, Ye Mao, and Krystian Mikolajczyk. Match-stereo-videos: Bidirectional alignment for consistent dynamic stereo matching. In _ECCV_ , 2024a. 4 

- Junpeng Jing, Ye Mao, Anlan Qiu, and Krystian Mikolajczyk. Match stereo videos via bidirectional alignment. _arXiv preprint arXiv:2409.20283_ , 2024b. 4 

- Junpeng Jing, Weixun Luo, Ye Mao, and Krystian Mikolajczyk. Stereo any video: Temporally consistent stereo matching. _arXiv preprint arXiv:2503.05549_ , 2025. 4 

- Bowen Wen, Matthew Trepte, Joseph Aribido, Jan Kautz, Orazio Gallo, and Stan Birchfield. Foundationstereo: Zero-shot stereo matching. In _CVPR_ , 2025. 4, 7, 8, 9 

- Lihe Yang, Bingyi Kang, Zilong Huang, Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao. Depth anything: Unleashing the power of large-scale unlabeled data. In _CVPR_ , 2024a. 4 

- Lihe Yang, Bingyi Kang, Zilong Huang, Zhen Zhao, Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao. Depth anything v2. _arXiv preprint arXiv:2406.09414_ , 2024b. 4 

- Ruihang Miao, Weizhou Liu, Mingrui Chen, Zheng Gong, Weixin Xu, Chen Hu, and Shuchang Zhou. Occdepth: A depth-aware method for 3d semantic scene completion. _arXiv preprint arXiv:2302.13540_ , 2023. 4 

- Bohan Li, Yasheng Sun, Xin Jin, Wenjun Zeng, Zheng Zhu, Xiaoefeng Wang, Yunpeng Zhang, James Okae, Hang Xiao, and Dalong Du. Stereoscene: Bev-assisted stereo matching empowers 3d semantic scene completion. In _IJCAI_ , 2024. 4 

- Zhangchen Ye, Tao Jiang, Chenfeng Xu, Yiming Li, and Hang Zhao. Cvt-occ: Cost volume temporal fusion for 3d occupancy prediction. In _ECCV_ , 2024. 4 

- Shiyuan Chen, Wei Sui, Bohao Zhang, Zeyd Boukhers, John See, and Cong Yang. Unleashing semantic and geometric priors for 3d scene completion. _arXiv preprint arXiv:2508.13601_ , 2025. 9 

12 

## **Appendix** 

### **.1 Overview of the Humanoid-OmniOcc Dataset** 

As summarized in Table 5, **Humanoid-OmniOcc** dataset comprises a total of 155,753 samples, each containing four stereo pairs captured from omnidirectional viewpoints. The data are collected from **fifteen** simulated indoor environments, each featuring distinct spatial layouts and aesthetic styles, covering diverse room types including apartments, studios, bedrooms, dining rooms, kitchens, lounges, living rooms, offices, and patios. In addition, five real-world indoor environments (Bar, Corridor, Office, and Apartment) are captured to enable sim-to-real evaluation. The entire dataset construction and physically-based rendering process consumed approximately **4,000 GPU hours** on NVIDIA L20 clusters, encompassing global illumination simulation, stereo rendering, and voxel-level occupancy ground-truth generation. 

### **.2 Ground Truth Generation in Simulation** 

At each frame, Isaac Sim provides RGB-D images for all stereo cameras, the robot’s pose _Tw_<sup>_r_</sup> in the world coordinate system, and each camera’s pose _Tw_<sup>_ci_.Thelocalenvironmentwithin</sup> [bev _w,_ bev _d,_ bev _h_ ] is exported as a mesh and voxelized with a voxel size of voxel_size. For each camera, the extrinsic matrix is computed as Extrinsic _ci_ = ( _Tw_<sup>_ci_)</sup><sup>_−_1</sup><sup>_T r_</sup> _w_<sup>.Occupancyvox-</sup> els in the world coordinates _Pw_ are transformed into the robot base frame _Pb_ = ( _Tw_<sup>_r_)</sup><sup>_−_1</sup><sup>_Pw_,</sup> and further into each camera coordinate frame _Pc_ = Extrinsic _ciPb_ . Valid points are filtered by _Pc_ ( _z_ ) _>_ 0 _._ 15 and projected to the image plane using intrinsic parameters to obtain pixel coordinates and depth _dpt_ . Each voxel is labeled following the depth consistency rule: 

Table 5: **Dataset samples distribution.** 

|**Scene**|**Frames**|**Scene**|**Frames**|
|---|---|---|---|
|ApartM1|10,766|Abode|4,951|
|Studio|14,860|Loft|15,694|
|BedR1|8,912|Nooks|19,851|
|Patio|5,705|BedR2|5,300|
|DiningR|9,909|Kitchen|6,116|
|Lounge|4,706|LivingR|10,206|
|ApartM2|10,860|Work|13,351|
|Office|14,566|Sum|155,753|


All voxel grids are projected back to the image plane for visual inspection. The projection visualization allows intuitive verification of occupancy accuracy and alignment consistency. 

To support fine-grained scene understanding, we annotate every occupied voxel with one of 15 semantic categories: _free, floor, partitions_ (wall, railings, window), _door, chair, table, sofa, bed, appliance_ (large household items), _cabinet, carpet, plant, objects_ (miscellaneous small items), _suspended objects_ (curtains, hanging fixtures), and _other_ . Categories are defined by merging simulator object labels into coherent groups that align with common indoor object taxonomies. The label distribution across scenes shows balanced coverage of structural ( _floor, partitions, door_ ) and furniture ( _chair, table, sofa, bed_ ) categories. 

### **.3 Ground Truth Generation in the Real World** 

We generate 3D occupancy supervision ground truth based on LiDAR point clouds. First, the fused dense point clouds undergo a preprocessing stage to eliminate invalid points, extreme outliers, and significant noise, thereby mitigating the impact of artifacts on voxel labeling. Subsequently, the point clouds are transformed into a unified baselink coordinate system using sensor calibration parameters, and a predefined 3D voxel space is constructed around the robotic. Each point coordinate is discretized into its corresponding voxel unit, where voxels containing LiDAR points are labeled as occupied, representing the regions supported by actual physical observations. To prevent unobserved or occluded regions from being erroneously categorized as free space, we further incorporate a visibility assessment based on viewing frustum constraints. Specifically, camera intrinsic and extrinsic 

13 

parameters are utilized to determine whether each voxel resides within the effective field of view (FoV) of the surround-view cameras. For voxels within the FoV that lack LiDAR point occupancy, we employ the 3D Bresenham ray-tracing algorithm to cast rays from the sensor center toward the target voxels. By traversing the voxels along the ray path and checking for the presence of occupied voxels, we determine the visibility status: if a ray is intercepted by an occupied voxel before reaching its destination, the target voxel is considered to be in an occluded region—meaning its true state cannot be resolved by current observations—and is thus marked as unknown; otherwise, it is classified as free space. Through this pipeline, the generated occupancy ground truth simultaneously characterizes the occupied space directly observed by LiDAR, the free space within the visible range, and the unknown space resulting from occlusions, providing a more physically consistent 3D spatial supervision signal for model training. Finally, semantic labels are manually annotated to obtain semantic occupancy supervision. 


Figure 6: **Performance scaling of HS**<sup>**2**</sup> **Occ with training and testing data.** 

### **.4 More Analysis on the Humanoid-OmniOcc Dataset** 

Figure 6 (Left) illustrates the influence of training data scale on occupancy prediction performance. As the number of training frames increases from 15K to 59K, all three metrics—IoU, Precision, and Recall—consistently improve, indicating that larger scene coverage leads to better spatial generalization and completeness. We also analyze the robustness of HS<sup>2</sup> Occ under varying testing frame scales, as shown in Figure 6 (Right). When the number of testing frames increases from 1K to 9K, all three metrics—IoU, Precision, and Recall—remain nearly constant, with fluctuations within only 1–2%. This consistency demonstrates that the learned representation generalizes well across different test scenes, confirming that the model does not rely on scene-specific priors or temporal bias. 

14 

