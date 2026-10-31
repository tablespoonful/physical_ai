---
title: "InstaDrive: Instance-Aware Driving World Models for Realistic and Consistent Video Generation"
date: "2026-02-03"
authors: "Zhuoran Yang; Xi Guo; Chenjing Ding; Chiyu Wang; Wei Wu; Yanyong Zhang"
url: https://arxiv.org/abs/2602.03242
pdf: https://arxiv.org/pdf/2602.03242
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.03242)** / [論文ページ](https://arxiv.org/abs/2602.03242)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **InstaDrive: Instance-Aware Driving World Models for Realistic and Consistent Video Generation** 

Zhuoran Yang<sup>1</sup> Xi Guo<sup>2</sup> Chenjing Ding<sup>2</sup> Chiyu Wang<sup>2</sup> Wei Wu<sup>2</sup><sup>_,_3</sup> Yanyong Zhang<sup>1*</sup> 

1University of Science and Technology of China 2SenseAuto 3Tsinghua University 

shanpoyang@mail.ustc.edu.cn, _{_ guoxi,dingchenjing _}_ @sensetime.com 

_{_ wangchiyu, wuwei _}_ @senseauto.com 

_{_ yanyongz _}_ @ustc.edu.cn 

## **Abstract** 

_Autonomous driving relies on robust models trained on high-quality, large-scale multi-view driving videos. While world models offer a cost-effective solution for generating realistic driving videos, they struggle to maintain instance-level temporal consistency and spatial geometric fidelity. To address these challenges, we propose_ **_InstaDrive_** _, a novel framework that enhances driving video realism through two key advancements: (1) Instance Flow Guider, which extracts and propagates instance features across frames to enforce temporal consistency, preserving instance identity over time. (2) Spatial Geometric Aligner, which improves spatial reasoning, ensures precise instance positioning, and explicitly models occlusion hierarchies. By incorporating these instance-aware mechanisms,_ **_InstaDrive_** _achieves state-of-the-art video generation quality and enhances downstream autonomous driving tasks on the nuScenes dataset. Additionally, we utilize CARLA’s autopilot to procedurally and stochastically simulate rare but safety-critical driving scenarios across diverse maps and regions, enabling rigorous safety evaluation for autonomous systems. Our project page_<sup>1</sup> _._ 

## **1. Introduction** 

Autonomous driving has attracted extensive attention from both industry and academia for decades [7, 26, 33, 56]. To enhance the performance and reliability of autonomous systems, high-quality, large-scale multi-view driving videos with precise annotations are essential for training models on downstream tasks such as perception, object tracking, and planning. However, acquiring and labeling real-world driving data is both costly and labor-intensive. To address this, 

*Corresponding Author 

> 1https : / / shanpoyang654 . github . io / InstaDrive / page.html 

benefiting from the rapid advancements in video generation models [2, 4, 9, 16, 17, 22, 23, 27, 41, 42, 46, 49, 58, 60], driving world models [10, 25, 45, 47, 55] have emerged as a promising solution, capable of generating diverse and realistic driving scenarios while significantly reducing data collection and annotation costs. 

Instance-level temporal consistency and spatial geometric fidelity are critical for generating realistic driving videos, as they affect video quality [40] and directly impact their applicability in autonomous driving tasks. Multi-object Tracking [43] and planning [24] require generated driving videos with temporally stable instance appearances to enhance temporal context understanding. This necessitates that the world model accurately maintains instance identities across frames, ensuring continuity in the motion and behavior of surrounding objects. On the other hand, perception tasks [43] require generated driving videos where instance positioning strictly adheres to spatial constraints imposed by bounding box control signals, ensuring accurate spatial context comprehension. This requires the world model to accurately capture instance spatial locations and occlusion hierarchy, ensuring geometric consistency within the scene. These two factors are essential for enabling world models to effectively learn the underlying dynamics of realworld environments. From a technical standpoint, ensuring strong temporal consistency and precise spatial alignment enhances the reliability of autonomous driving models trained on synthetic data, ultimately improving their realworld performance. 

However, generating driving videos that maintain instance-level temporal consistency and spatial geometric fidelity remains two significant challenges, primarily due to the large sampling space in diffusion-based models and the limited control signals. First, maintaining fine-grained temporal consistency is particularly difficult. While prior works [10, 11, 28, 45, 47, 55] have incorporated various techniques to improve _global_ coherence, they still struggle 

1 


Figure 1. **Limitations of Prior Works. (a)** Temporal Consistency: In MagicDrive-V2 [10], the car’s color changes inconsistently over time. **(b)** Spatial Localization: In MagicDrive-V2, the car deviates from the bounding box control signal. **(c)** Occlusion Hierarchy: In Panacea [47], the distant bus incorrectly occludes the nearby pedestrian, violating natural occlusion rules. Our method excels in temporal consistency, spatial localization, and occlusion hierarchy, addressing these issues effectively. 

with _instance-level_ temporal inconsistencies. For instance, DriveDreamer [45], MagicDrive-V2 [10], and Panacea [47] integrate temporal attention layers to enhance inter-frame consistency. However, without explicit control mechanisms to enforce instance-level consistency, these methods struggle to maintain stable instance attributes across frames, often resulting in color shifts or texture inconsistencies in Fig.1 (a). This highlights the need for explicit instance-level control signals to improve temporal consistency. Second, achieving spatial geometric fidelity presents another challenge. Existing methods often suffer from spatial misalignment of instances, as seen in MagicDrive-V2 [10], where instance locations exhibit noticeable deviations in Fig.1 (b). This issue arises because these methods lack explicit view transformation from BEV to the camera’s First-Person View (FPV). Furthermore, existing methods struggle to capture the occlusion hierarchy among instances in Fig. 1 (c), where the lack of explicit depth order prevents correct occlusion reasoning. This highlights the need for an improved spatial control mechanism that ensures accurate instance positioning and explicitly models the occlusion hierarchy. 

In this paper, to address the above challenges, we propose **_InstaDrive_** , a driving world model that effectively adheres to instance-level temporal consistency and spatial geometric fidelity. **_InstaDrive_** achieves state-of-the-art performance in both video quality and validation in downstream autonomous driving tasks. To ensure instance-level temporal consistency, we introduce **I** nstance **F** low **G** uider ( **IFG** ), a lightweight module to extract and propagate instance features across frames. We propose a simple but effective instance flow for mapping the object motion to the RGB domain, then inject the flow to DiT backbone. IFG provides an instance-aware motion cue, which serves as a reference for tracking the position of the corresponding instances in the previous frame. Once the position is determined, we retrieve the semantic features of the instance, such as object category and color. These features 

are then propagated forward to ensure instance-level visual consistency across frames. This mechanism significantly improves instance-level temporal consistency. 

To ensure instance-level spatial geometric fidelity, we introduce **S** patial **G** eometric **A** ligner ( **SGA** ), which enables the model to accurately capture the spatial locations of the instance and the occlusion hierarchy. To enable accurate spatial localization, we transform 3D bounding boxes into the camera’s perspective view, extracting projected instance bounding boxes as control elements. This transformation leverages the camera’s intrinsic and extrinsic parameters, ensuring spatial consistency between the world coordinate system and the image plane. To establish a consistent occlusion hierarchy, we explicitly resolve the relative depth order of instances using the distance from each corner point to the camera’s optical center, measured along the optical axis. We encode each corner point’s location and depth via Fourier embedding, followed by an MLP, to derive an explicit depth order representation. Through this mechanism, the model effectively learns to capture spatial locations and occlusion relationships between instances. 

**_InstaDrive_** establishes a fine-grained and robust world model which ensures instance-level temporal consistency and geometric fidelity in generated driving videos. Our approach achieves state-of-the-art performance in both video generation quality and downstream autonomous driving task validation, outperforming previous works [10, 28, 47, 55]. Our contributions are as follows. 

- To maintain stable instance attributes over time, we propose the Instance Flow Guider, which extracts and propagates instance features across frames, enabling instancelevel temporal consistency. 

- To enable accurate spatial location and establish a consistent occlusion hierarchy, we introduce the Spatial Geometric Aligner, which integrates the 3D bounding boxes and their occlusion relationships, and aligns these details with the pixel space. 

2 

- Our model achieves SOTA video generation quality with high FID and FVD on the nuScenes benchmark, surpassing previous methods. For autonomous driving applications, the generated videos are validated on downstream perception, tracking, and planning tasks, with performance competitive to real-world sensor data. 

- We designed a pipeline that generates virtual layouts based on CARLA and employs our model as a renderer for video synthesis, demonstrating the immense potential of **_InstaDrive_** in generating long-tail driving scenarios. 

## **2. Related Works** 

**Controllable Generation.** The emergence of diffusion models [52] has significantly advanced text-to-video generation [1, 3, 4, 14, 15, 19, 21, 35, 44, 51, 59]. Video LDM [4] accelerates generation by denoising in the latent space, but text prompts alone lack precision. Recent methods combine image blocks with text for better control [52]. Our work focuses on generating realistic street-view videos, addressing challenges like complex layouts and dynamic vehicles. We enhance control by integrating road maps, 3D bounding boxes, and BEV keyframes. 

**Street-View Generation.** Street-view generation methods typically use 2D layouts like BEV maps, 2D bounding boxes, and semantic segmentation. BEVGen [36] encodes semantic data in BEV layouts, while BEVControl [50] uses a two-stage pipeline for multi-view urban scenes, ensuring cross-view consistency. However, projecting 3D information into 2D layouts loses geometric details, causing temporal inconsistencies in videos. To address this, we use 3D bounding boxes to maintain geometric fidelity. Unlike DrivingDiffusion [28], which relies on a complex multi-stage pipeline, our method simplifies the process with an efficient, end-to-end framework, ensuring temporal coherence and computational efficiency. 

**Multi-View Video Generation.** Multi-view video generation faces challenges in achieving both multi-view and temporal consistency. MVDiffusion [37] uses a correspondence-aware attention module to align views, while Tseng et al. [39] apply epipolar geometry for viewto-view regularization. DriveScape [48], MagicDrive [11], and MagicDrive V2 [10] incorporate advanced control signals, high-definition rendering, and long-duration training but struggle with instance-level temporal consistency and precise positional control. 

**Simulation-to-Real Visual Translation.** Recent advances in synthetic data for real-world visual tasks have shown significant progress. GAN-based translation [12] and domain randomization [38] bridge synthetic and real-world data distributions, while datasets like Synthia [32] and Virtual KITTI [5] provide scalable benchmarks for semantic segmentation and autonomous driving. Adversarial training [34, 54] reduces distribution gaps, and human motion rep- 

resentation learning [13] highlights synthetic data’s utility in video understanding. Unlike these methods, we extract proxy data like 3D bounding boxes and road maps from graphics systems, leveraging the InstaDrive model to generate more realistic and diverse videos. 

## **3. Method** 

We introduce **_InstaDrive_** in Sec. 3.1, a novel framework for generating realistic driving videos that adhere to instancelevel temporal consistency and spatial geometric fidelity. Furthermore, we leverage CARLA’s autopilot to procedurally and stochastically simulate rare yet safety-critical driving scenarios across diverse maps and regions in Sec. 3.4. 

### **3.1. Overview** 

The overall architecture of our model is illustrated in Fig. 2. Building on OpenSora V1.1 [57], we employ a Variational Auto-Encoder (VAE) for video encoding, T5 [31] for text encoding, and Spatial-Temporal Diffusion Transformer (ST-DiT) as foundational model for the denoising process. 

To achieve fine-grained control over both foreground and background elements, we introduce a comprehensive set of control conditions, including bounding box projection, road maps, camera poses, and scene descriptions, integrating them into the conditioned video generation process. Moreover, we introduce instance tracking IDs to facilitate the tracking and propagation of instance features across frames, a key mechanism within our proposed Instance Flow Guider module, detailed in Sec. 3.2. Additionally, we leverage box coordinate and bounding box projection to enforce instance-level spatial geometric fidelity, as elaborated in Sec. 3.3. 

Given the need for handling multiple control elements, we employ ControlNet [53] to inject control signals into the video generation process. Practically, a set of encoders, including _Edepth_ , _Evae_ , and _Etext_ , extract latent features from diverse control conditions. To incorporate these control-aware representations, we integrate 13 duplicated blocks into the first 13 base blocks of the ST-DiT architecture. Each control block modulates the feature flow by fusing condition features with the corresponding base block outputs, thereby ensuring effective control signal conditioning throughout the generation pipeline. 

To guarantee the multi-view consistency during generation, we use a parameter-free view-inflated attention mechanism to replace the commonly used cross-view attention modules [11]. Specifically, we reshape the input from R<sup>_v×t×h×w×c_</sup> to R<sup>_t×h×_(</sup><sup>_wv_)</sup><sup>_×c_</sup> and treat _wv_ as the frame width. Our proposed approach improves the multi-view coherence without compensating with additional parameters. 

3 


Figure 2. **Overview.** (a) Instance Flow Guider, which utilizes the instance flow to improve instance-level temporal consistency. (b) Spatial Geometric Aligner, which uses perspective projection and depth order to capture instance spatial locations and occlusion hierarchy. (c) Controlled Denoising Process, enabled by ST-DiT with ControlNet for unified condition control. 


Figure 3. Illustration of the extraction process for motion map in Instance Flow Guider. We calculate the motion vector _F_ offset for each instance, and render the projected box using _F_ offset. 

### **3.2. Instance Flow Guider** 

To ensure instance-level temporal consistency, we introduce a lightweight **I** nstance **F** low **G** uider ( **IFG** ) module, which enables the model to track, retrieve, and propagate instance features over time, preserving instance attributes such as color and texture. Fig. 3 provides an overview of Instance Flow Guider module. 

**Tracking Instance Position.** We leverage track IDs to capture motion trajectories of surrounding instances, termed as _instance flow_ , which supports both continuous and non- 

continuous trajectories: 


where ( _x_<sup>_i_</sup> _j_<sup>_, y_</sup> _j_<sup>_i, z_</sup> _j_<sup>_i_) denotes the position of instance</sup><sup>_i_at frame</sup> _t_ , and _vi_<sup>_t∈{_0</sup><sup>_,_1</sup><sup>_}_indicates whether instance</sup><sup>_i_is visible at</sup> frame _t_ . We define the most recent visible frame as: 


If _i_ was never visible before _t_ , _τ_ ( _i, t_ ) is undefined. To encode the positional displacement of an instance from previous frame to current frame, we define _instance flow offset_ : 


which propagates features from _τ_ ( _i, t_ ) to _t_ , effectively reassociating reappearing instances with their pre-occlusion states. The full offset map for all _N_ instances at frame _t_ is: 


which serves as a motion condition for tracking the corresponding instance’s position in the previous frame. **Visualizing Motion Conditions.** To ensure alignment between the motion condition and the corresponding instance’s geometric position, we transform _F_ offset<sup>_t_into a mo-</sup> tion map _h_<sup>_t_</sup> _∈_ R<sup>_H×W ×_3</sup> , which belongs to the same latent space of video patches. The 3D bounding box of instance _i_ is projected onto the camera’s First-Person View to obtain its 2D projection region. Each pixel within this region at 

4 

frame _t_ is assigned the positional displacement of the corresponding instance: 


The positional displacements of all instances _F_ offset<sup>_t_are col-</sup> lectively encoded into the motion map _h_<sup>_t_</sup> . Notably, the first frame employs a fully-zero map: _h_<sup>_t_=0</sup> = 0. Afterward, to visualize the motion map _h ∈_ R<sup>_T ×H×W ×_3</sup> , we transform _h_ into the RGB color space, generating _h_<sup>_vis_</sup> _∈_ R<sup>_T ×H×W ×_3</sup> through a flow visualization technique: _x_ - offset is mapped to the red ( _R_ ) channel, _y_ -offset is mapped to the green ( _G_ ) channel, and _z_ -offset is mapped to the blue ( _B_ ) channel. To efficiently encode motion information, we leverage the same VAE encoder _E_ vae to compress the motion maps _h_<sup>_vis_</sup> , achieving an 8× spatial downsampling, yielding a compact motion latent representation: _hm ∈_ R<sup>_T ×h×w×_4</sup> . 

**Retrieving and Propagating Instance Features.** Once the motion vector is encoded, we fuse instance motion condition features with the corresponding base block outputs using ControlNet [53]. These fused representations are then passed through temporal attention layers in ST-DiT blocks. The encoded motion map, which comprises instance flow and instance mask, enables the temporal attention layers to selectively incorporate instance information from adjacent frames. As a result, the semantic attributes of each instance (e.g., instance category, color, and texture) are retrieved from the past frame and efficiently propagated forward. By conditioning the ST-DiT model _Dθ_ on both the spatial location and feature tokens of each instance, we explicitly control where and how each instance should appear in the generated video. This approach significantly enhances instance-level temporal consistency in driving video synthesis, effectively addressing issues such as color shifts and texture inconsistencies. 

Unlike methods such as GEM [18], which rely on external feature-extraction models (e.g., DINOv2 [30]) to obtain instance features, IFG directly derives instance motion and semantic attributes from the generated video itself. This eliminates the need for additional deep feature extractors, making IFG computationally efficient while still ensuring strong instance-level temporal consistency. 

### **3.3. Spatial Geometric Aligner** 

To ensure spatial geometric fidelity, we introduce a lightweight **S** patial **G** eometric **A** ligner ( **SGA** ) module, which enables the model accurately capture instance spatial locations and occlusion hierarchy. Fig. 2(c) provides an overview of the SGA module. 

To enable accurate spatial localization, we transform 3D bounding boxes into the camera’s perspective view, extract- 

ing instance bounding box projections as control elements. This transformation uses the camera’s intrinsic and extrinsic parameters, ensuring spatial consistency between the world coordinate system and the image plane. 

A 3D bounding box ( _c, b_ ) consists of a class label _c_ and box position _b_ . The 3D coordinates _bw_ in the world coordinate system, representing one of the eight corner points of _b_ , are first converted into the ego vehicle coordinate system using the inverse ego rotation _Re_ and translation _Te_ : 


Next, the coordinates are transformed into the camera coordinate system using the calibrated sensor extrinsic matrix: 


where _Rs_ and _Ts_ represent the camera’s rotation and translation relative to the vehicle. The 3D points _bc_ = [ _xc, yc, zc_ ] are then projected onto the 2D image plane using the camera’s intrinsic matrix _K_ . The 2D pixel coordinates are computed as: 


The resulting 2D pixel coordinates render instance-aware spatial constraints in the RGB domain, with distinct colors representing different classes _c_ . These constraints are encoded by the _E_ layout encoder into the projected bounding box condition embedding _h_ box. This explicit transformation pipeline ensures precise instance localization. 

To establish a consistent occlusion hierarchy, we explicitly resolve the relative depth order of instances. During the transformation from the camera coordinate system to the image plane, the depth component _zc_ represents the distance from an instance’s corner point to the camera optical center along the optical axis. We use this depth information as a control condition, helping the model understand occlusion relationships and ensuring closer instances correctly occlude farther ones. 

For each instance, the 3D bounding box is defined by eight corner points in the camera coordinate system, denoted as _b_<sup>_i_</sup> _t_<sup>_∈_R8</sup><sup>_×_3,whereeachrow</sup><sup>_bc_=[</sup><sup>_u, v, zc_]en-</sup> codes the position and depth of a corner point in the 2D image plane. We apply Fourier embedding to each corner point and pass it through an MLP to obtain the depth order representation: 


The hidden states for all bounding boxes in frame _t_ are rep- _bNt_ resented as _hdepth_ = [ _ht_<sup>_b_1</sup><sup>_, . . . , h_</sup> _t_ ], where _Nt_ is the number of instances. To integrate depth-based spatial information, we fuse _hdepth_ with the projected bounding box condition embedding _h_ box using cross-attention: 


5 

This enables the model to effectively capture spatial locations and occlusion relationships, ensuring geometric fidelity in generated driving videos. 

### **3.4. CARLA based Procedural Scenario Simulation** 

We used CARLA’s autopilot and map system to define obstacle interaction behaviors (e.g., cut-in, braking) and extracted intermediate 3D bounding boxes, lane markings, and drivable areas. Leveraging nuScenes’ ego vehicle coordinate system and camera parameters, we projected this data into multiple viewpoints, converting it into model control conditions. This enabled scene generation. The system efficiently utilizes CARLA’s waypoint mechanism to randomly generate diverse events across maps, providing a rich set of control conditions. 

## **4. Experiment** 

### **4.1. Setups** 

**Datasets and Baselines.** We train and evaluate our model on the nuScenes dataset [6]. To benchmark our approach, we compare it with state-of-the-art driving world models, including BEVControl [50], DriveDiffusion [28], DriveDreamer2 [55], Panacea [47], and MagicDrive-V2 [10]. 

**Metrics.** For realism assessment, we use FID [20] and FVD [40] to measure video quality. To evaluate instance-level temporal consistency, we test our model in real-world autonomous driving scenarios using the multi-object tracking (MOT) task. MOT ensures consistent object tracking across frames, minimizing ID switches (IDSW) and drift. Following Panacea [47], we employ the StreamPETR model [43] and evaluate performance using standard MOT metrics: AMOTA, AMOTP, RECALL, MOTA, and IDS. Additionally, we evaluate spatial geometric fidelity by measuring the alignment between generated videos and their conditioned sequences, ensuring accurate preservation of geometric structures. This is assessed through perception tasks, as precise detection and localization are fundamental to perception. Thus, perception performance directly indicates the accuracy of object localization and occlusion relationships. Using the StreamPETR model [43], we employ metrics such as the nuScenes Detection Score (NDS), mean Average Precision (mAP), mean Average Orientation Error (mAOE), and mean Average Velocity Error (mAVE). We note that Bevfusion [29] has also been used for perception metric evaluation [11], but it is based on an image model, performs worse than the video-based model StreamPETR, and cannot provide object tracking metrics. Therefore, we still choose StreamPETR for evaluation. 

For metrics and results on the planning task using pretrained UniAD [33] model, please refer to Appendix. 

|Method|Multi-View|Multi-Frame|FVD_↓_|FID_↓_|
|---|---|---|---|---|
|BEVControl [50]|✓||-|24.85|
|DrivingDiffusion [28]|✓|✓|332|15.83|
|Panacea [47]|✓|✓|139|16.96|
|MagicDrive-V2 [10]|✓|✓|94.84|20.91|
|DriveScape [48]|✓|✓|76.39|8.34|
|DriveDreamer2[55]|✓|✓|55.7|11.2|
|**_InstaDrive_**|✓|✓|38.06|3.96|


Table 1. Comparing with SoTA methods on the validation set of the nuScenes dataset. We generate the entire validation set without applying any post-processing strategies to select specific samples. 

|Method|Real|Generated|AMOTA_↑_|AMOTP_↓_|IDS_↓_|
|---|---|---|---|---|---|
|Oracle|✓|-|0.289|1.419|687|
|DriveDreamer2|✓|✓|0.313|1.387|593(-94)|
|**_InstaDrive_** (Ours)|✓|✓|0.496|1.376|532(-155)|


Table 2. Comparison on multi-object tracking task with MagicDrive-V2 [10] based on a pre-trained StreamPETR model. 

### **4.2. Training Details** 

Our method is implemented based on OpenSora [57]. All training inputs were set to 16x256x448 and conducted on 8 A100 GPUs. Experimental results show that our method can stably generate over 200 frames. For more implementation details, please refer to Appendix. 

### **4.3. Main Results** 

#### **4.3.1. Quantitative Analysis** 

To verify the high fidelity of our generated videos, we compare our approach with various state-of-the-art driving world models. We generate training and validation data using the nuScenes dataset’s labels as conditions. For fairness, we generate the entire dataset without applying any post-processing strategies to select specific samples. **Realism of Images.** Our generated videos exhibit higher visual quality, achieving an FID of 3 _._ 96, as shown in Tab. 1. It substantially outperforms those of all counterparts, including both video-based methods like DriveDreamer2 [55] and image-based solutions such as BEVControl [50]. 

**Instance-Level Temporal Consistency.** Our method significantly reduces FVD to 38 _._ 06 in Tab. 1, due to the Instance Flow Guider module preserving instance attributes over frames and therefore enhancing instance-level temporal consistency. Additionally, we also assess our model in real-world autonomous driving applications using the multi-object tracking (MOT) task in Tab. 2, as MOT requires consistent tracking of the same object across frames while minimizing ID switches, making it a strong indicator of instance-level temporal consistency. Specifically, we generate data using the nuScenes validation set’s labels as conditions. We then re-train the object tracking model StreamPETR [43] by integrating the generated data with real data. The MOT model’s performance improves sig- 

6 


Figure 4. **Text control** . By adding ”Rainy,” ”Sunny,” and ”Night” to the original text prompt, while keeping other conditions unchanged, our model represents strong ability to edit videos effectively. 


Figure 5. **Long-tail scenarios simulation.** Using CARLA’s highly configurable simulation environment, we create synthetic control conditions which represent complex driving scenarios (e.g., sudden braking), and then utilize InstaDrive to generate corresponding videos. 

nificantly, achieving a lower IDS of 532 compared to the originally pre-trained StreamPETR, indicating our framework’s effectiveness in producing instance-level temporally consistent synthetic data. 

|Method|Real|Generated|NDS_↑_|
|---|---|---|---|
|Oracle|✓|-|46.90|
|Panacea|-|✓|32.10 (68.00%)|
|MagicDrive-V2|-|✓|36.82 (78.51%)|
|**_InstaDrive_**|-|✓|40.51 (86.38%)|


Table 3. Comparison on perception task using the generated nuScenes validation set in (T+I)2V scenarios. We use pre-trained perception model StreamPETR [43] to evaluate. Our model outperformed most baseline models across the board without any post-refine process, underscoring a better capability of spatial localization and occlusion hierarchy understanding. 

**Spatial Geometric Fidelity.** _Data Augmentation Performance._ We assess our model in real-world autonomous driving applications using the perception task, as the perception task fundamentally relies on precise detection and localization. Thus, perception performance directly reflects the accuracy of object localization and occlusion relationships. In Tab. 4, we first train StreamPETR exclusively on 

our generated training dataset, and it achieves a mAP of 35 _._ 5%, equivalent to 92 _._ 69% of the performance obtained by models trained solely on the real nuScenes training dataset. These results highlight that the generated dataset is not only a viable substitute for real data but also highly effective in training perception models independently. Moreover, we re-train StreamPETR by integrating the generated data with real data; the perception model’s performance improves significantly, achieving a NDS of 51 _._ 9, marking a 3 _._ 6-point increase over the model trained exclusively on real data. This underscores the substantial value of incorporating generated data into the training pipeline. 

**Perception Validation Performance.** Additionally, we use the pre-trained StreamPETR model to evaluate the generated validation set of the nuScenes. In Tab. 3, our model achieves a relative performance of 86 _._ 38% on the nuScenes Detection Score (NDS), underscoring a better alignment with the control conditions. Additional results on planning task can refer to Appendix. 

#### **4.3.2. Qualitative Analysis** 

We conduct a qualitative comparison of **_InstaDrive_** with other SOTA models using the generated videos. 

7 

**Instance-Level Temporal Consistency.** In Fig.1(a), MagicDrive-V2 exhibits an inconsistency where the car’s color changes over time. In contrast, our model maintains the car’s attributes consistently across all frames, showcasing superior instance-level temporal consistency. **Spatial Localization.** In Fig.1(b), MagicDrive-V2 fails to adhere to the bounding box control signal, resulting in spatial deviation. In contrast, our model ensures precise spatial localization, accurately following the control signal. **Occlusion Hierarchy.** In Fig.1(c), for the video generated by Panacea, the distant bus incorrectly occludes the nearby pedestrian, violating natural occlusion rules. In contrast, our model accurately preserves the occlusion hierarchy, ensuring a realistic representation of scene depth. 

#### **4.3.3. Long-tail Scenarios Simulation.** 

Our method can simulate diverse long-tail driving scenarios. By modifying text prompts, we can change the weather and time of scenes, as shown in Fig. 4. We can also generate critical long-tail events, such as sudden braking and lane cutting, using control conditions provided by the **Carla** simulator [8]. Carla supplies conditions like 3D bounding box projections, lane line projections, and text descriptions for scenes. Leveraging Carla’s highly configurable environment, we create synthetic control conditions for complex and diverse scenarios, such as multi-vehicle intersections, narrow streets, or sudden obstacles, which are challenging to capture in real-world data. In Fig. 5, we demonstrate our model’s ability to generate long-tail videos corresponding to these conditions. The results show that our method not only replicates realistic conditions but also seamlessly adapts to complex scenarios generated by Carla, enhancing its applicability in autonomous driving research. For more visualization details, please refer to the Appendix. 

|Method|Real|Gen.|mAP_↑_|mAOE_↓_|mAVE_↓_|NDS_↑_|
|---|---|---|---|---|---|---|
|Panacea|✓|-|34.5|59.4|29.1|46.9|
|Panacea|-|✓|22.5|72.7|46.9|36.1|
|Panacea|✓|✓|37.1 (+2.6%)|54.2|27.3|49.2 (+2.3%)|
|**_InstaDrive_** (Re-Impl.)|✓|-|38.3|62.1|28.8|48.3|
|**_InstaDrive_** (Ours)|-|✓|35.5|59.7|29.4|43.67|
|**_InstaDrive_** (Ours)|✓|✓|42.0(+3.7%)|53.2|26.8|51.9(+3.6%)|


Table 4. Comparison on perception task with Panacea. We involve data augmentation using synthetic training data to train StreamPETR. The perception model’s performance improves significantly, showing the substantial value of incorporating generated data into the training pipeline. 

### **4.4. Ablation Study** 

We validate two key modules through qualitative and quantitative analyses, demonstrating their effectiveness and robustness. The qualitative comparison is in Fig. 6. **Instance Flow Guider.** To evaluate the impact of the IFG module, we conduct an ablation study by removing the instance flow injection. In Tab. 5, the absence of instance flow 

|Settings|FVD_↓_|FID_↓_|NDS_↑_|IDS_↓_|
|---|---|---|---|---|
|**_InstaDrive_**|38.06|3.96|40.51|532|
|w/o IFG|58.86(+20.8)|6.28(+2.32)|40.23(-0.28)|1189(+653)|
|w/o SGA|41.21(+3.15)|4.22(+0.26)|37.31(-3.20)|723(+187)|
|w/o SGA(Box)|39.27(+1.21)|4.07(+0.11)|38.22(-2.29)|628(+92)|
|w/o SGA(Depth)|40.46(+2.40)|4.15(+0.19)|39.13(-1.38)|669(+133)|


Table 5. Ablation study results in (T+I)2V scenarios on the generated nuScenes validation set. 


Figure 6. Ablation study of two key modules. **Zoom for better view. (a)** Removing the IFG causes the car’s color to change over time, breaking temporal consistency. **(b)** Replacing box projection with box coordinates in the Spatial Geometric Aligner module causes misalignment between the passenger and the control box, resulting in failed spatial localization. **(c)** Removing depth cues in the Spatial Geometric Aligner results in the nearby car A failing to occlude the distant car B, disrupting occlusion hierarchy. 

leads to a significant drop of 20 _._ 8 in FVD and an increase of 653 in IDS (ID Switch) for the multi-object tracking task. These results underscore the critical role of the IFG module in preserving instance-level temporal consistency. 

**Spatial Geometric Aligner.** To evaluate the influence of the SGA module, we remove the injection of depth cues and replace the box projection with box coordinates as the control signal, seperately. As shown in Tab. 5, the absence of SGA module results in a significant degradation of **3.20** in NDS, highlighting its critical role in understanding spatial localization and occlusion hierarchy. 

Our method can also generate videos without the initial frame as condition. To evaluate the impact of two key modules in the T2V scenario, please refer to Appendix. 

## **5. Conclusion** 

We propose **_InstaDrive_** , a driving world model that enhances instance-level temporal consistency and spatial geometric fidelity. Our approach introduces two key advancements: the Instance Flow Guider module, which extracts and propagates instance features across frames to preserve instance identity over time, and the Spatial Geometric Aligner module, which ensures precise instance positioning and explicitly models occlusion hierarchies. By incorporating these instance-aware mechanisms, **_InstaDrive_** achieves SOTA generation quality and significantly improves downstream autonomous driving tasks. Finally, we leverage CARLA’s autopilot to generate rare yet safety-critical driving scenarios, demonstrating the immense potential of **_InstaDrive_** in long-tail simulation. 

8 

## **Acknowledgements** 

This work was supported by the National Natural Science Foundation of China (No. 62332016) and the Key Research Program of Frontier Sciences, CAS (No. ZDBS-LYJSC001). 

## **References** 

- [1] Jie An, Songyang Zhang, Harry Yang, Sonal Gupta, Jia-Bin Huang, Jiebo Luo, and Xi Yin. Latent-shift: Latent diffusion with temporal shift for efficient text-to-video generation. _arXiv preprint arXiv:2304.08477_ , 2023. 3 

- [2] Omer Bar-Tal, Hila Chefer, Omer Tov, Charles Herrmann, Roni Paiss, Shiran Zada, Ariel Ephrat, Junhwa Hur, Guanghui Liu, Amit Raj, et al. Lumiere: A space-time diffusion model for video generation. In _SIGGRAPH Asia 2024 Conference Papers_ , pages 1–11, 2024. 1 

- [3] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 3 

- [4] Andreas Blattmann, Robin Rombach, Huan Ling, Tim Dockhorn, Seung Wook Kim, Sanja Fidler, and Karsten Kreis. Align your latents: High-resolution video synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 22563–22575, 2023. 1, 3 

- [5] Yohann Cabon, Naila Murray, and Martin Humenberger. Virtual kitti 2. _arXiv preprint arXiv:2001.10773_ , 2020. 3 

- [6] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11621–11631, 2020. 6 

- [7] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 1 

- [8] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. CARLA: An open urban driving simulator. In _Proceedings of the 1st Annual Conference on Robot Learning_ , pages 1–16, 2017. 8 

- [9] Kaifeng Gao, Jiaxin Shi, Hanwang Zhang, Chunping Wang, Jun Xiao, and Long Chen. Ca2-vdm: Efficient autoregressive video diffusion model with causal generation and cache sharing. _arXiv preprint arXiv:2411.16375_ , 2024. 1 

- [10] Ruiyuan Gao, Kai Chen, Bo Xiao, Lanqing Hong, Zhenguo Li, and Qiang Xu. Magicdrivedit: High-resolution long video generation for autonomous driving with adaptive control, 2024. 1, 2, 3, 6 

- [11] Ruiyuan Gao, Kai Chen, Enze Xie, Hong Lanqing, Zhenguo Li, Dit-Yan Yeung, and Qiang Xu. Magicdrive: Street view generation with diverse 3d geometry control. In _ICLR_ , 2024. 1, 3, 6 

- [12] Xi Guo, Zhicheng Wang, Qin Yang, Weifeng Lv, Xianglong Liu, Qiong Wu, and Jian Huang. Gan-based virtualto-real image translation for urban scene semantic segmentation. _Neurocomputing_ , 394:127–135, 2020. 3 

- [13] Xi Guo, Wei Wu, Dongliang Wang, Jing Su, Haisheng Su, Weihao Gan, Jian Huang, and Qin Yang. Learning video representations of human motion from synthetic data. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 20197–20207, 2022. 3 

- [14] Xi Guo, Chenjing Ding, Haoxuan Dou, Xin Zhang, Weixuan Tang, and Wei Wu. Infinitydrive: Breaking time limits in driving world models. _arXiv preprint arXiv:2412.01522_ , 2024. 3 

- [15] Yuwei Guo, Ceyuan Yang, Anyi Rao, Yaohui Wang, Yu Qiao, Dahua Lin, and Bo Dai. Animatediff: Animate your personalized text-to-image diffusion models without specific tuning. _arXiv preprint arXiv:2307.04725_ , 2023. 3 

- [16] Agrim Gupta, Lijun Yu, Kihyuk Sohn, Xiuye Gu, Meera Hahn, Fei-Fei Li, Irfan Essa, Lu Jiang, and Jos´e Lezama. Photorealistic video generation with diffusion models. In _European Conference on Computer Vision_ , pages 393–411. Springer, 2024. 1 

- [17] Yoav HaCohen, Nisan Chiprut, Benny Brazowski, Daniel Shalem, Dudu Moshe, Eitan Richardson, Eran Levin, Guy Shiran, Nir Zabari, Ori Gordon, et al. Ltx-video: Realtime video latent diffusion. _arXiv preprint arXiv:2501.00103_ , 2024. 1 

- [18] Mariam Hassan, Sebastian Stapf, Ahmad Rahimi, Pedro M B Rezende, Yasaman Haghighi, David Br¨uggemann, Isinsu Katircioglu, Lin Zhang, Xiaoran Chen, Suman Saha, Marco Cannici, Elie Aljalbout, Botao Ye, Xi Wang, Aram Davtyan, Mathieu Salzmann, Davide Scaramuzza, Marc Pollefeys, Paolo Favaro, and Alexandre Alahi. Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control, 2024. 5 

- [19] Yingqing He, Tianyu Yang, Yong Zhang, Ying Shan, and Qifeng Chen. Latent video diffusion models for high-fidelity video generation with arbitrary lengths. _arXiv preprint arXiv:2211.13221_ , 2022. 3 

- [20] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium. In _Proceedings of the 31st International Conference on Neural Information Processing Systems_ , page 6629–6640, Red Hook, NY, USA, 2017. Curran Associates Inc. 6 

- [21] Jonathan Ho, William Chan, Chitwan Saharia, Jay Whang, Ruiqi Gao, Alexey Gritsenko, Diederik P Kingma, Ben Poole, Mohammad Norouzi, David J Fleet, et al. Imagen video: High definition video generation with diffusion models. _arXiv preprint arXiv:2210.02303_ , 2022. 3 

- [22] Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, and David J Fleet. Video diffusion models. _Advances in Neural Information Processing Systems_ , 35:8633–8646, 2022. 1 

- [23] Li Hu. Animate anyone: Consistent and controllable imageto-video synthesis for character animation. In _Proceedings of_ 

9 

_the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 8153–8163, 2024. 1 

- [24] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, Lewei Lu, Xiaosong Jia, Qiang Liu, Jifeng Dai, Yu Qiao, and Hongyang Li. Planning-oriented autonomous driving, 2023. 1 

- [25] Fan Jia, Weixin Mao, Yingfei Liu, Yucheng Zhao, Yuqing Wen, Chi Zhang, Xiangyu Zhang, and Tiancai Wang. Adriver-i: A general world model for autonomous driving. _arXiv preprint arXiv:2311.13549_ , 2023. 1 

- [26] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 8340–8350, 2023. 1 

- [27] Jiarui Lei, Xiaobo Hu, Yue Wang, and Dong Liu. Pyramidflow: High-resolution defect contrastive localization using pyramid normalizing flow. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 14143–14152, 2023. 1 

- [28] Xiaofan Li, Yifu Zhang, and Xiaoqing Ye. Drivingdiffusion: Layout-guided multi-view driving scene video generation with latent diffusion model, 2023. 1, 2, 3, 6 

- [29] Zhijian Liu, Haotian Tang, Alexander Amini, Xinyu Yang, Huizi Mao, Daniela L Rus, and Song Han. Bevfusion: Multitask multi-sensor fusion with unified bird’s-eye view representation. In _2023 IEEE international conference on robotics and automation (ICRA)_ , pages 2774–2781. IEEE, 2023. 6 

- [30] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herv´e Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. Dinov2: Learning robust visual features without supervision, 2024. 5 

- [31] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, et al. Exploring the limits of transfer learning with a unified text-to-text transformer. _Journal of machine learning research_ , 21(140):1–67, 2020. 3 

- [32] German Ros, Laura Sellart, Joanna Materzynska, David Vazquez, and Antonio M Lopez. The synthia dataset: A large collection of synthetic images for semantic segmentation of urban scenes. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 3234–3243, 2016. 3 

- [33] Xiaogang Shi, Bin Cui, Gillian Dobbie, and Beng Chin Ooi. Uniad: A unified ad hoc data processing system. _ACM Transactions on Database Systems (TODS)_ , 42(1):1–42, 2016. 1, 6 

- [34] Ashish Shrivastava, Tomas Pfister, Oncel Tuzel, Joshua Susskind, Wenda Wang, and Russell Webb. Learning from simulated and unsupervised images through adversarial training. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 2107–2116, 2017. 3 

- [35] Uriel Singer, Adam Polyak, Thomas Hayes, Xi Yin, Jie An, Songyang Zhang, Qiyuan Hu, Harry Yang, Oron Ashual, Oran Gafni, et al. Make-a-video: Text-to-video generation without text-video data. _arXiv preprint arXiv:2209.14792_ , 2022. 3 

- [36] Alexander Swerdlow, Runsheng Xu, and Bolei Zhou. Streetview image generation from a bird’s-eye view layout. _arXiv preprint arXiv:2301.04634_ , 2023. 3 

- [37] Shitao Tang, Fuyang Zhang, Jiacheng Chen, Peng Wang, and Yasutaka Furukawa. Mvdiffusion: Enabling holistic multiview image generation with correspondence-aware diffusion. _arXiv preprint arXiv:2307.01097_ , 2023. 3 

- [38] Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, and Pieter Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pages 23–30. IEEE, 2017. 3 

- [39] Hung-Yu Tseng, Qinbo Li, Changil Kim, Suhib Alsisan, JiaBin Huang, and Johannes Kopf. Consistent view synthesis with pose-guided diffusion models. In _CVPR_ , 2023. 3 

- [40] Thomas Unterthiner, Sjoerd van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric challenges. _arXiv:1812.01717_ , 2018. 1, 6 

- [41] Jiuniu Wang, Hangjie Yuan, Dayou Chen, Yingya Zhang, Xiang Wang, and Shiwei Zhang. Modelscope text-to-video technical report. _arXiv preprint arXiv:2308.06571_ , 2023. 1 

- [42] Jing Wang, Ao Ma, Jiasong Feng, Dawei Leng, Yuhui Yin, and Xiaodan Liang. Qihoo-t2x: An efficient proxy-tokenized diffusion transformer for text-to-any-task. _arXiv preprint arXiv:2409.04005_ , 2024. 1 

- [43] Shihao Wang, Yingfei Liu, Tiancai Wang, Ying Li, and Xiangyu Zhang. Exploring object-centric temporal modeling for efficient multi-view 3d object detection. In _CVPR_ , pages 3621–3631, 2023. 1, 6, 7 

- [44] Wenjing Wang, Huan Yang, Zixi Tuo, Huiguo He, Junchen Zhu, Jianlong Fu, and Jiaying Liu. Videofactory: Swap attention in spatiotemporal diffusions for text-to-video generation, 2023. 3 

- [45] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-worlddriven world models for autonomous driving. _arXiv preprint arXiv:2309.09777_ , 2023. 1, 2 

- [46] Yaohui Wang, Xinyuan Chen, Xin Ma, Shangchen Zhou, Ziqi Huang, Yi Wang, Ceyuan Yang, Yinan He, Jiashuo Yu, Peiqing Yang, et al. Lavie: High-quality video generation with cascaded latent diffusion models. _International Journal of Computer Vision_ , pages 1–20, 2024. 1 

- [47] Yuqing Wen, Yucheng Zhao, Yingfei Liu, Fan Jia, Yanhui Wang, Chong Luo, Chi Zhang, Tiancai Wang, Xiaoyan Sun, and Xiangyu Zhang. Panacea: Panoramic and controllable video generation for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 6902–6912, 2024. 1, 2, 6 

- [48] Wei Wu, Xi Guo, Weixuan Tang, Tingxuan Huang, Chiyu Wang, Dongyue Chen, and Chenjing Ding. Drivescape: To- 

10 

   - wards high-resolution controllable multi-view driving video generation. _arXiv preprint arXiv:2409.05463_ , 2024. 3, 6 

- [49] Haocheng Xi, Shuo Yang, Yilong Zhao, Chenfeng Xu, Muyang Li, Xiuyu Li, Yujun Lin, Han Cai, Jintao Zhang, Dacheng Li, et al. Sparse videogen: Accelerating video diffusion transformers with spatial-temporal sparsity. _arXiv preprint arXiv:2502.01776_ , 2025. 1 

- [50] Kairui Yang, Enhui Ma, Jibin Peng, Qing Guo, Di Lin, and Kaicheng Yu. Bevcontrol: Accurately controlling streetview elements with multi-perspective consistency via bev sketch layout. _arXiv preprint arXiv:2308.01661_ , 2023. 3, 6 

- [51] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, et al. Cogvideox: Text-to-video diffusion models with an expert transformer. _arXiv preprint arXiv:2408.06072_ , 2024. 3 

- [52] David Junhao Zhang, Dongxu Li, Hung Le, Mike Zheng Shou, Caiming Xiong, and Doyen Sahoo. Moonshot: Towards controllable video generation and editing with multimodal conditions, 2024. 3 

- [53] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding conditional control to text-to-image diffusion models. In _ICCV_ , 2023. 3, 5 

- [54] Weichen Zhang, Wanli Ouyang, Wen Li, and Dong Xu. Collaborative and adversarial network for unsupervised domain adaptation. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 3801–3809, 2018. 3 

- [55] Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Xinze Chen, Guan Huang, Xiaoyi Bao, and Xingang Wang. Drivedreamer-2: Llm-enhanced world models for diverse driving video generation. _arXiv preprint arXiv:2403.06845_ , 2024. 1, 2, 6 

- [56] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. _arXiv preprint arXiv:2402.11502_ , 2024. 1 

- [57] Zangwei Zheng, Xiangyu Peng, Tianji Yang, Chenhui Shen, Shenggui Li, Hongxin Liu, Yukun Zhou, Tianyi Li, and Yang You. Open-sora: Democratizing efficient video production for all, 2024. 3, 6 

- [58] Zangwei Zheng, Xiangyu Peng, Tianji Yang, Chenhui Shen, Shenggui Li, Hongxin Liu, Yukun Zhou, Tianyi Li, and Yang You. Open-sora: Democratizing efficient video production for all. _arXiv preprint arXiv:2412.20404_ , 2024. 1 

- [59] Daquan Zhou, Weimin Wang, Hanshu Yan, Weiwei Lv, Yizhe Zhu, and Jiashi Feng. Magicvideo: Efficient video generation with latent diffusion models, 2023. 3 

- [60] Yuan Zhou, Qiuyue Wang, Yuxuan Cai, and Huan Yang. Allegro: Open the black box of commercial-level video generation model. _arXiv preprint arXiv:2410.15458_ , 2024. 1 

11 

