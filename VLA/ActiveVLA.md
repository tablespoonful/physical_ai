---
title: "ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation"
date: "2026-01-13"
authors: "Zhenyang Liu; Yongchong Gu; Yikai Wang; Xiangyang Xue; Yanwei Fu"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2601.08325
pdf: https://arxiv.org/pdf/2601.08325
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.08325)** / [論文ページ](https://arxiv.org/abs/2601.08325)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation** 

Zhenyang Liu<sup>1</sup><sup>_,_2</sup> , Yongchong Gu<sup>1</sup> , Yikai Wang<sup>3*</sup> , Xiangyang Xue<sup>1†</sup> , Yanwei Fu<sup>1</sup><sup>_,_2†</sup> 1Fudan University 2Shanghai Innovation Institute 3Nanyang Technological University 

liuzy24@m.fudan.edu.cn, yongchonggu22@m.fudan.edu.cn, yikai.wang@ntu.edu.sg, xyxue@fudan.edu.cn, yanweifu@fudan.edu.cn Project Page: ZhenyangLiu.github.io/ActiveVLA 


Figure 1. **Comparison between previous VLA methods and ActiveVLA.** Traditional VLA systems often fail in tasks like “bring the apples on the table” because their fixed cameras miss critical details or become occluded. In contrast, **ActiveVLA** leverages 3D scene understanding to freely place virtual cameras and synthesize optimal viewpoints, enabling robots to adjust their view for clearer, more informative observations and thus achieve more reliable manipulation performance even under occlusion. 

## **Abstract** 

_Recent advances in robot manipulation have leveraged pretrained vision-language models (VLMs) and explored integrating 3D spatial signals into these models for effective action prediction, giving rise to the promising visionlanguage-action (VLA) paradigm. However, most existing approaches overlook the importance of active percep-_ 

_tion: they typically rely on static, wrist-mounted cameras that provide an end-effector-centric viewpoint. As a result, these models are unable to adaptively select optimal viewpoints or resolutions during task execution, which significantly limits their performance in long-horizon tasks and fine-grained manipulation scenarios. To address these limitations, we propose_ **_ActiveVLA_** _, a novel vision-languageaction framework that empowers robots with active percep-_ 

_tion capabilities for high-precision, fine-grained manipulation. ActiveVLA adopts a coarse-to-fine paradigm, dividing the process into two stages: (1) Critical region localization. ActiveVLA projects 3D inputs onto multi-view 2D projections, identifies critical 3D regions, and supports dynamic spatial awareness. (2) Active perception optimization. Drawing on the localized critical regions, ActiveVLA uses an active view selection strategy to choose optimal viewpoints. These viewpoints aim to maximize amodal relevance and diversity while minimizing occlusions. Additionally, ActiveVLA applies a 3D zoom-in to improve resolution in key areas. Together, these steps enable finer-grained active perception for precise manipulation. Extensive experiments demonstrate that ActiveVLA achieves precise 3D manipulation and outperforms state-of-the-art baselines on three simulation benchmarks. Moreover, ActiveVLA transfers seamlessly to real-world scenarios, enabling robots to learn high-precision tasks in complex environments._ 

## **1. Introduction** 

_“Perception is not a passive process. It’s an active process of hypothesis testing.”_ – Richard Gregory 

Pretrained vision-language models (VLMs) [2, 3, 27, 55] have become a highly effective approach for building largescale vision-language-action (VLA) architectures. Such models have demonstrated impressive generalization and robustness in robotic manipulation [4, 6, 21, 31, 34, 38]. However, most current VLA approaches primarily process 2D visual inputs, requiring massive datasets to bridge the gap between perception and action. In contrast, 3Daware robotic policies leverage structural cues from 3D data, achieving better sample efficiency and spatial reasoning for complex manipulation tasks [16–18, 28, 52]. 

Gregory’s insight captures a core challenge in embodied intelligence: perception must not remain a passive receiver of sensory input but instead become an active hypothesistesting process—seeking, selecting, and verifying information relevant to the task at hand. However, existing VLA models [31, 38, 50, 66] largely rely on static or wristmounted cameras, constraining observations to a fixed, endeffector-centric viewpoint. Such a setup inherently limits perceptual flexibility: the agent cannot adaptively and dynamically adjust its viewpoint or camera resolution according to the task context. As a result, the absence of adaptive viewpoint selection during long-horizon or fine-grained manipulation prevents current systems from acquiring essential contextual information, thereby undermining the robustness and generalizability of learned policies [16–18, 28, 38, 52]. Addressing this limitation is crucial for developing embodied agents capable of adaptive and reliable interaction in complex, real-world environments. 

To address this limitation, we propose **ActiveVLA** , a novel vision-language-action framework that explicitly integrates active perception into robotic manipulation. ActiveVLA enables robots to adaptively and dynamically adjust their viewpoint and camera resolution according to the task context, allowing more informative observations to be acquired on demand. The framework equips robots with two complementary capabilities: (1) **Active viewpoint selection** , which autonomously determines optimal camera perspectives during task execution to maximize visibility and task relevance while minimizing occlusions; and (2) **Active 3D zoom-in** , which identifies and selectively enhances high-resolution views of task-critical regions within the 3D scene. By dynamically refining its perceptual input through these mechanisms, ActiveVLA enables more precise, context-aware, and reliable action prediction, ultimately achieving superior adaptability and performance in complex, long-horizon manipulation scenarios. 

As illustrated in Figure 1, ActiveVLA adopts a coarseto-fine active perception design that integrates 3D spatial reasoning with vision-language understanding. In the _coarse stage_ , ActiveVLA projects the 3D point-cloud observations into multiple 2D orthographic views [17, 18], aligning them with the pretrained VLM backbone. By leveraging structural priors from the 3D inputs, the model effectively localizes salient and task-relevant regions in 3D space. In the _fine stage_ , ActiveVLA performs active view selection to determine optimal camera poses centered on these key regions, maximizing amodal relevance and spatial diversity while reducing occlusions. It then applies an active 3D zoom-in strategy to enhance the spatial resolution of these areas, enabling precise manipulation of fine-grained details. This closed-loop, coarse-to-fine perception-action pipeline allows ActiveVLA to dynamically adapt its sensory inputs and maintain high effectiveness across complex, multi-step, and long-horizon manipulation tasks. 

Comprehensive experiments validate the advantages of ActiveVLA. On RLBench [23], it achieves an average success rate of 91.8%, with some tasks reaching a perfect success rate of 100%. On COLOSSEUM [48], it achieves the highest success rate of 78.3% in challenging generalization scenarios. ActiveVLA consistently outperforms all baselines on GemBench [14], demonstrating superior adaptability across diverse tasks. Real-world evaluations further confirm its robustness and strong generalization to previously unseen configurations. These results demonstrate that integrating active perception into vision-language-action learning is a key step toward adaptive embodied intelligence. 

The contributions of this paper are summarized: 

- **_Active Perception for Vision-Language-Action Models_** : We propose ActiveVLA, a novel vision-language-action framework that equips robots with active perception capabilities, enabling adaptive viewpoint selection and zoom- 

in mechanisms for precise, fine-grained manipulation. 

- **_A Novel ActiveVLA Framework_** : ActiveVLA designs a novel coarse-to-fine pipeline that projects 3D point clouds into multi-view 2D representations, predicts key regions via heatmaps, and selectively refines observations for precise, fine-grained manipulation. 

- **_State-of-the-Art Performance and Real-World Generalization_** : Extensive experiments on RLBench, COLOSSEUM, and GemBench demonstrate that ActiveVLA outperforms state-of-the-art baselines. Real-world robot evaluations show strong generalization and high success rates, highlighting the practical impact of active perception in long-horizon and precision-critical tasks. 

merging their features in a downstream action predictor to inform decision-making. SpatialVLA [50] introduces a specialized position encoding (Ego3D) to inject spatial information into 2D observations. However, most existing methods lack perceptual flexibility because the models cannot dynamically adjust their viewpoint or camera resolution. As a result, they fail to leverage the advantages of active, egocentric perception in robotic manipulation. In contrast, ActiveVLA uses an active camera selection strategy to choose optimal viewpoints and an active 3D zoom-in mechanism to enhance point cloud resolution in key regions, leading to better performance in complex, long-horizon tasks. 

## **3. Our Proposed ActiveVLA** 

## **2. Related Work** 

**Vision-Language-Action Models.** Recent research has increasingly focused on developing generalist robot policies trained on large-scale robotic learning datasets [10, 13, 29, 35, 45]. Vision-Language-Action (VLA) models have emerged as a promising approach for training such policies [5, 9, 11, 12, 30, 39, 44, 47, 54, 57, 58, 62, 65, 67]. VLAs extend vision-language models (VLMs), which are pre-trained on massive internet-scale image and text datasets [1, 8, 27, 36, 37, 42, 55, 64, 68, 69], to the domain of robotic control [56]. This approach provides several key advantages: leveraging large-scale vision-language model backbones with billions of parameters enables effective learning from vast robotic datasets, while reusing pretrained weights from internet-scale data enhances VLAs’ ability to interpret diverse language commands and generalize to novel objects and environments, making them adaptable for real-world robotic applications. ActiveVLA is a vision-language-action (VLA) framework that employs large-scale vision-language model backbones. Unlike previous methods, ActiveVLA further leverages the spatial structure of 3D inputs and utilizes active perception through novel view synthesis of 3D representations, resulting in greater adaptability and improved performance in manipulation tasks. 

**3D Modalities in Robotic Learning.** Although VLA models with 2D inputs have been extensively explored, incorporating 3D modalities into robot learning is still an emerging area of research [26, 32, 40, 41, 60, 66]. Recent studies have started leveraging richer spatial information to enhance robot perception and manipulation capabilities. Some approaches, such as 3DVLA [20], present holistic models for unified 3D tasks like generalization, visual question answering, 3D perception, and control. Other methods aim to improve the performance of foundational 2D models by integrating three-dimensional features. Lift3D [26] augments 2D vision backbones like DINOv2 [46] with both implicit and explicit 3D representations. PointVLA [32] utilizes separate encoders for 2D images and 3D point clouds, 

**VLA Setup.** Vision-Language-Action models aim to learn a generalizable and robust multi-task robot manipulation policy _π_ . _π_ that maps an observation **o** and a language instruction _l_ to an action **a** : 


The action **a** consists of a 6-DoF end-effector pose _T ∈ SE_ (3), a gripper state _g ∈{_ 0 _,_ 1 _}_ , and a collision flag _c ∈{_ 0 _,_ 1 _}_ of the next key frame. This setting assumes access to expert demonstrations _D_ = _{τ_<sup>_i_</sup> _}_<sup>_N_</sup> _i_ =1<sup>containing</sup> _N_ trajectories, where each trajectory contains a language instruction and a sequence of observation-action pairs, _i.e._ , _τ_<sup>_i_</sup> = _{l_<sup>_i_</sup> _,_ ( **o** 1<sup>_i,_</sup><sup>**a**</sup><sup>_i_</sup> 1<sup>)</sup><sup>_, ...,_(</sup><sup>**o**</sup><sup>_i_</sup> _H_<sup>_,_</sup><sup>**a**</sup><sup>_i_</sup> _H_<sup>)</sup><sup>_}_.Theobservation</sup><sup>**o**con-</sup> tains RGB-D images captured from one or multiple fixed, end-effector-centric viewpoints. However, this setup limits perceptual flexibility by preventing dynamic viewpoint or resolution adjustment, hindering context acquisition and policy generalization. 

**ActiveVLA.** As shown in Figure 2, ActiveVLA addresses the limitation of perceptual flexibility through a coarseto-fine active perception framework that adaptively adjusts the camera’s viewpoint and zoom-in level according to the task context, thereby enhancing scene exploration and facilitating fine-grained interaction. By integrating 3D spatial reasoning with vision-language understanding, our approach progressively refines perceptual focus from a broad overview to task-critical regions, enhancing both contextual awareness and generalization. ActiveVLA enables robots to attend to critical 3D regions and actively sense the environment, allowing adaptive viewpoints and zoom-in for fine-grained manipulation. 

### **3.1. 3D Crucial Area Perception** 

During each task, ActiveVLA first identifies the core region in the 3D scene to serve as the focus for active perception. **Multi-View Rendering.** Given RGB-D images as visual input, ActiveVLA reconstructs a point cloud of the scene using images captured by calibrated cameras. To match the 


Figure 2. **The pipeline of ActiveVLA. ActiveVLA** is a 3D vision-language-action framework that adopts a two-stage, coarse-to-fine strategy. In the _coarse stage_ , three orthographic projections of the 3D scene and a language instruction are processed by the PaliGemma backbone to generate 2D heatmaps, which are then back-projected to locate the most relevant 3D region. In the _fine stage_ , an active perception module selects new views and performs a 3D zoom-in on this region. The refined PaliGemma then predicts heatmaps for key end-effector positions, while an action decoder outputs the final 3D action. 

2D image input required by the VLM backbone, we render three orthographic projection images of the point cloud from top, front, and right viewpoints. Specifically, for each view, we render three image maps with a total of 7 channels: RGB, depth, and the coordinates of the points in the world frame (3 channels). The coordinates help establish the correspondence of pixels across views, _i.e._ , if pixels from different views share the same ( _x, y, z_ ), they correspond to the same point in 3D. We use PyTorch3D [51] for rendering. The rendered image at viewpoint _v_ is given by: 


where _π_<sup>(</sup><sup>_v_)</sup> ( _·_ ) denotes the orthographic projection. The rendered color at each pixel is taken from the point with the minimal depth _zi_<sup>(</sup><sup>_v_)</sup> among all points projecting to that pixel, ensuring correct occlusion handling. 

**3D Crucial Area Extraction.** These images are then used as input for the VLM backbone, which is designed to process images along with accompanying text prompts. Since the VLM’s global representations are not sufficient for precise spatial localization, we introduce a heatmap prediction module to recover fine-grained spatial attention and identify object positions within each view. To predict the heatmap, we first rearrange the output patch tokens _{_ **t** _i}_<sup>_M_</sup> _i_ =1<sup>accord-</sup> ing to their spatial positions to form a feature grid. A convex upsampling block is then applied to the feature grid to obtain a heatmap that matches the resolution of the input image. This process can be expressed as: 


where _U_ ( _·_ ) denotes the convex upsampling block, and Rearrange( _·_ ) rearranges the tokens into a feature grid of size _Hp × Wp_ . Unlike fixed interpolation methods, the upsampling module learns pixel-wise weights for finer spatial detail recovery. The pipeline is trained with cross-entropy loss to predict heatmaps, which are then back-projected from all views to identify the crucial 3D region. 

### **3.2. 3D Active Perception** 

ActiveVLA enables active perception, allowing robots to perform fine-grained manipulation. It includes two components: Active Viewpoint Selection and Active 3D Zoom-in. **Active Viewpoint Selection.** To improve perceptual completeness in complex scenes, ActiveVLA proposes a hypothesis testing strategy for selecting active views that focuses on optimal camera viewpoints centered on key regions identified during the coarse stage. The goal is to maximize amodal relevance by ensuring full visibility of target objects and increasing view diversity. Together, these objectives help reduce occlusion and perceptual ambiguity through complementary observations. Given the 3D key region of interest _pf ∈_ R<sup>3</sup> (e.g., the centroid of a partially observed object), we generate a set of candidate camera positions uniformly distributed around a sphere centered at _pf_ . To achieve isotropic coverage, we employ a geodesic sampling strategy based on recursive subdivision of a regular icosahedron, producing a near-uniform point distribution on the spherical surface. This avoids sampling biases inherent in latitude-longitude parameterizations and provides scalable control over viewpoint density via subdivision level. The total number of sampling points _V_ ( _k_ ) after _k_ -level re- 

cursive subdivision (where _k ∈_ N, a non-negative integer) is quantitatively described as: 


where _k_ = 0 corresponds to the original icosahedron (12 vertices), and higher _k_ indicates successive subdivisions. Each candidate camera position _ci_ is evaluated using a multi-objective scoring function that balances three criteria: 

- **Visibility** : ActiveVLA determines whether the line of sight from _ci_ to _pf_ is occluded by scene geometry. Using a KDTree-based nearest-neighbor search on the observed point cloud _S_ , it samples _N_ uniformly spaced points _{qk}_ along the ray and computes their nearestsurface distances: 


- If all distances exceed a threshold _r_ ( _dk ≥ r, ∀k_ ), the view is marked unoccluded with _v_ ( _ci, pf_ ) = 1; otherwise, _v_ ( _ci, pf_ ) = 0. 

- **Distance** : We normalize the distance _∥ci − pf ∥_ and standardize it across candidates to prefer moderate viewing ranges that balance field-of-view and detail resolution. 

- **Diversity** : To ensure geometric diversity among selected viewpoints, we compute the total angular separation between the viewing direction of _ci_ and all other candidates. Given candidate set _C_ = _{c_ 1 _, . . . , cM }_ and unit viewing vectors **v** _i ∈_ S<sup>2</sup> , the diversity score is defined as: 


A larger _S_ div( _ci_ ) indicates greater angular diversity and more spatially distributed views. 

These scores are Z-normalized and combined into a unified score: 


where _w_ vis + _w_ dis + _w_ div = 1 are the weighting coefficients, _s_ vis denotes the visibility score, _s_ dis denotes the distance score, and _s_ div denotes the diversity score. The top- _K_ highest-scoring views are selected as the next observation poses. Each camera is configured using the look-at formulation with eye _ci_ , target _pf_ , and a dynamically adjusted up vector. These views enable informative, unoccluded observations that support robust multi-view reasoning and precise manipulation, with the most informative view serving as the basis for active 3D zoom-in. 

**Active 3D Zoom-in.** Previous VLA models rely on fixed camera views around the robot, which often fail to capture sufficient detail for fine-grained tasks involving small objects (e.g., _welding a hole using a welding gun_ ). 

To overcome this limitation, ActiveVLA introduces an active 3D zoom-in mechanism that adaptively refines visual perception around key interaction regions. After selecting the optimal viewpoint, the system re-renders the scene from the same camera pose with a narrowed field of view, effectively magnifying the local region while maintaining high pixel resolution for precise gripper pose prediction. This simulates an optical zoom effect in virtual rendering space, enabling detailed observation of small-scale structures without loss of visual fidelity. Let _α_ denote the original FoV (in radians), _z >_ 1 the zoom-in factor, and _d_ the distance from the camera to the region of interest. The spatial coverage width _W_ of the rendered image (perpendicular to the viewing direction) is given by: 


where _W_ ( _z_ ) decreases with increasing _z_ , while pixel resolution _R_ is preserved as _R_ = image width _W_ ( _z_ )(pixels) , ensuring higher detail in the magnified region. 

The zoom-in process leverages the 3D point cloud for scale-invariant view synthesis without geometric loss. Unlike fixed physical cameras, the virtual renderer produces high-resolution close-ups based on local 3D structure, enhancing gripper pose accuracy. By separating exploration (view selection) from exploitation (zoom-in), ActiveVLA forms a hierarchical perception strategy that improves precision manipulation and underscores the benefits of adaptive observation in simulation-to-real VLA systems. 

### **3.3. 3D Action Prediction** 

After obtaining the actively selected and zoom-in views, we feed them into the VLM to generate attention heatmaps. For translational prediction, these 2D heatmaps are backprojected into the 3D workspace and accumulated on a discretized grid _G_ = _{_ **g** 1 _, . . . ,_ **g** _N }_ to form a multi-view score volume: 


where _hv_ is the attention heatmap of view _v_ , _πv_ ( **g** ) is the 2D projection of grid point **g** , and _wv_ denotes the view weight. The translation target is determined as **t**<sup>_∗_</sup> = arg max **g** _∈G S_ ( **g** ). For rotation prediction, ActiveVLA represents orientation using Euler angles ( _ϕ, θ, ψ_ ), each discretized into 72 bins. A hierarchical feature fusion module then integrates global and local context to predict rotation, gripper state, and a binary collision flag. 

- **Global Context Encoding** : We perform max-pooling over the vision encoder outputs of each orthographic projection to obtain a global feature vector per view, yielding three global tokens that capture overall scene semantics. 

Table 1. **Results on RLBench.** “Avg. Rank” denotes the average rank across all 18 tasks, where a lower value signifies better overall performance. ActiveVLA attains first place in 10 tasks, highlighting its dominance in the benchmark. 

|**Models**|**Avg.**<br>**SR (%)**_↑_|**Avg.**<br>**Rank**_↓_|Close<br>Jar|Drag<br>Stick|Insert<br>Peg|Meat off<br>Grill|Open<br>Drawer|Place<br>Cups|Place<br>Wine|Push<br>Buttons|
|---|---|---|---|---|---|---|---|---|---|---|
|Image-BC (CNN) [25,52]|1.3|11.56|0.0|0.0|0.0|0.0|0.0|4.0|0.0|0.0|
|Image-BC (ViT) [25,52]|1.3|11.61|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|
|C2F-ARM-BC [24,52]|20.1|9.89|24.0|24.0|4.0|20.0|20.0|0.0|8.0|72.0|
|HiveFormer [19]|45.3|8.22|52.0|76.0|0.0|100.0|52.0|0.0|80.0|84.0|
|PolarNet [7]|46.4|7.78|36.0|92.0|4.0|100.0|84.0|0.0|40.0|96.0|
|PerAct [22]|49.4|7.33|55.2_±_4.7|89.6_±_4.1|5.6_±_4.1|70.4_±_2.0|88.0_±_5.7|2.4_±_3.2|44.8_±_7.8|92.8_±_3.0|
|Act3D [16]|65.0|5.28|92.0|92.0|27.0|94.0|93.0|3.0|80.0|99.0|
|RVT [17]|62.9|5.39|52.0_±_2.5|99.2_±_1.6|11.2_±_3.0|88.0_±_2.5|71.2_±_6.9|4.0_±_2.5|91.0_±_5.2|100.0_±_0.0|
|3D Diffuser Actor [28]|81.3|3.39|96.0_±_2.5|100.0_±_0.0|65.6_±_4.1|96.8_±_1.6|89.6_±_4.1|24.0_±_7.6|93.6_±_4.8|98.4_±_2.0|
|RVT-2 [18]|81.4|3.00|100.0_±_0.0|99.0_±_1.7|40.0_±_0.0|99.0_±_1.7|74.0_±_11.8|38.0_±_4.5|95.0_±_3.3|100.0_±_0.0|
|BridgeVLA [33]|88.2|2.44|100.0_±_0.0|100.0_±_0.0|88.0_±_2.8|100.0_±_0.0|100.0_±_0.0|58.4_±_10.0|88.0_±_2.8|98.4_±_2.2|
|**ActiveVLA (Ours)**|**91.8**|**1.22**|**100.0**_±_**0.0**|**100.0**_±_**0.0**|**92.4**_±_**1.9**|**100.0**_±_**0.0**|**100.0**_±_**0.0**|**65.6**_±_**3.2**|**96.2**_±_**1.4**|**100.0**_±_**0.0**|
||Put in|Put in|Put in|Screw|Slide|Sort|Stack|Stack|Sweep to|Turn|
|**Models**|Cupboard|Drawer|Safe|Bulb|Block|Shape|Blocks|Cups|Dustpan|Tap|
|Image-BC (CNN) [25,52]|0.0|8.0|4.0|0.0|0.0|0.0|0.0|0.0|0.0|8.0|
|Image-BC (ViT) [25,52]|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|0.0|16.0|
|C2F-ARM-BC [24,52]|0.0|4.0|12.0|8.0|16.0|8.0|0.0|0.0|0.0|68.0|
|HiveFormer [19]|32.0|68.0|76.0|8.0|64.0|8.0|8.0|0.0|28.0|80.0|
|PolarNet [7]|12.0|32.0|84.0|44.0|56.0|12.0|4.0|8.0|52.0|80.0|
|PerAct [22]|28.0_±_4.4|51.2_±_4.7|84.0_±_3.6|17.6_±_2.0|74.0_±_13.0|16.8_±_4.7|26.4_±_3.2|2.4_±_2.0|52.0_±_0.0|88.0_±_4.4|
|Act3D [16]|51.0|90.0|95.0|47.0|93.0|8.0|12.0|9.0|92.0|94.0|
|RVT [17]|49.6_±_3.2|88.0_±_5.7|91.2_±_3.0|48.0_±_5.7|81.6_±_5.4|36.0_±_2.5|28.8_±_3.9|26.4_±_8.2|72.0_±_0.0|93.6_±_4.1|
|3D Diffuser Actor [28]|85.6_±_4.1|96.0_±_3.6|97.6_±_2.0|82.4_±_2.0|97.6_±_3.2|44.0_±_4.4|68.3_±_3.3|47.2_±_8.5|84.0_±_4.4|99.2_±_1.6|
|RVT-2 [18]|66.0_±_4.5|96.0_±_0.0|96.0_±_2.8|88.0_±_4.9|92.0_±_2.8|35.0_±_7.1|80.0_±_2.8|69.0_±_5.9|100.0_±_0.0|99.0_±_1.7|
|BridgeVLA [33]|73.6_±_4.6|99.2_±_1.8|99.2_±_1.8|87.2_±_6.6|96.0_±_2.8|60.8_±_7.7|76.8_±_8.7|81.6_±_3.6|87.2_±_1.8|92.8_±_3.3|
|**ActiveVLA (Ours)**|**87.4**_±_**3.4**|**99.5**_±_**2.1**|**99.4**_±_**1.6**|**89.3**_±_**5.4**|**98.5**_±_**3.7**|**63.3**_±_**5.3**|**82.2**_±_**4.7**|**84.8**_±_**2.1**|**100.0**_±_**0.0**|**95.3**_±_**2.8**|


- **Local Context Encoding** : For fine-grained reasoning, we use an ROI-aware sampler to extract local tokens, encoding detailed appearance and geometry. 

All tokens are concatenated and passed through an MLP head to predict rotation, gripper, and collision actions. This global-local fusion allows the model to combine overall scene understanding with fine spatial precision, enabling accurate and safe manipulation in complex environments. 

## **4. Experiments** 

**Simulation Benchmarks.** We evaluate ActiveVLA on three simulation benchmarks for long-horizon and finegrained manipulation. RLBench [23] features 18 tasks using a Franka Panda robot with RGB-D inputs from four calibrated cameras and 100 demonstrations per task. COLOSSEUM [48] extends RLBench with 12 perturbation types involving object, scene, and camera variations for robustness evaluation. GemBench [14] further builds on RLBench as a hierarchical benchmark with 16 training and 44 testing tasks across seven core action primitives, assessing compositionality and generalization. 

**Implementation Details.** Our ActiveVLA adopts the pretrained VLM backbone from BridgeVLA [33], built on PaliGemma [3] with a SigLIP encoder [63] and Gemma decoder [53], pre-trained on a 120K-image RoboPoint subset [61]. Real-world experiments are conducted on a KINOVA GEN2 robot with a RealSense D455 camera in 

an eye-to-hand setup, covering occlusion-rich manipulation tasks. All experiments run on eight NVIDIA H100 GPUs and a 192-vCPU Intel Xeon Platinum 8468 system. 

**Baselines.** We compare ActiveVLA with state-of-the-art baselines. Image-BC (CNN/ViT) [25] performs 2D behavior cloning with convolutional or transformer backbones. C2F-ARM-BC [24] and PerAct [52] adopt voxelbased coarse-to-fine and Perceiver Transformer policies, respectively. HiveFormer integrates historical observations via a multimodal transformer, while PolarNet [49] encodes 3D scenes to predict heatmaps and offsets. Act3D [16] samples and ranks 3D points for action selection, and 3D Diffuser Actor [28] models 3D trajectories via diffusion. RVT [17] and RVT-2 [18] aggregate multi-view projections in a coarse-to-fine transformer framework, whereas BridgeVLA [33] aligns 2D heatmaps for efficient 3D vision-language-action learning. 

### **4.1. Experimental Results** 

**Results on RLBench.** We evaluate ActiveVLA over five trials for statistical reliability, with results shown in Table 1. ActiveVLA achieves a new state of the art on RLBench with a 91.8% average success rate and an average rank of 1.22. It performs exceptionally well in precision-demanding and contact-rich tasks such as _Insert Peg_ and _Open Drawer_ , and remains robust even under occlusions (e.g., _Place Cups_ , 65.6%). Across diverse task types including placement, assembly, and cleaning, ActiveVLA maintains consistent high 

Table 2. **Results on the COLOSSEUM Benchmark.** The table presents performance across 14 generalization scenarios. ”Avg. Rank” indicates the mean ranking of each method over all perturbations, with lower values reflecting stronger overall performance. ActiveVLA surpasses the current best method by 1.9 percentage points in average success rate, demonstrating improved robustness and generalization. 

|**Models**|**Avg. SR (%)**_↑_|**Avg. Rank**_↓_|All Perturbations|MO-COLOR|RO-COLOR|MO-TEXTURE|RO-TEXTURE|MO-SIZE|
|---|---|---|---|---|---|---|---|---|
|R3M-MLP [43]|0.8|6.57|0.6|0.4|0.0|0.0|0.0|1.8|
|MVP-MLP [59]|1.6|6.36|0.8|1.2|0.0|0.4|0.0|4.44|
|PerAct [22]|27.9|4.79|7.2|24.0|29.2|28.8|17.71|35.6|
|RVT [17]|35.4|4.36|6.4|26.0|31.3|44.8|41.1|35.3|
|RVT-2 [18]|56.7|2.86|15.6_±_0.8|53.0_±_0.9|54.6_±_0.6|59.7_±_0.7|56.7_±_1.4|60.9_±_0.9|
|BridgeVLA [33]|64.0|2.07|18.7_±_2.2|60.5_±_1.1|63.8_±_0.1|63.5_±_1.5|68.4_±_3.3|69.3_±_1.0|
|**ActiveVLA (Ours)**|**65.9**|**1.07**|**21.4**_±_**1.8**|**64.2**_±_**1.5**|**64.4**_±_**1.2**|**65.7**_±_**2.1**|**69.3**_±_**2.6**|**72.4**_±_**0.8**|
|**Models**|RO-SIZE|Light Color|Table Color|Table Texture|Distractor|Background Texture|RLBench|Camera Pose|
|R3M-MLP [43]|0.0|1.0|1.4|0.2|1.6|1.2|2.0|0.8|
|MVP-MLP [59]|0.0|1.6|1.6|1.0|3.8|2.2|2.0|2.6|
|PerAct [22]|29.3|29.1|30.4|23.2|27.1|33.5|39.4|36.3|
|RVT [17]|40.5|34.0|30.0|45.2|18.8|46.4|53.4|42.2|
|RVT-2 [18]|53.4_±_1.5|58.0_±_1.1|62.6_±_0.9|56.6_±_0.9|**60.8**_±_**0.5**|68.7_±_1.1|68.8_±_1.3|64.4_±_0.5|
|BridgeVLA [33]|61.7_±_0.8|69.7_±_1.2|75.7_±_0.9|71.3_±_0.7|51.8_±_1.5|74.8_±_1.0|73.1_±_0.2|73.8_±_0.3|
|**ActiveVLA (Ours)**|**64.4**_±_**1.3**|**70.4**_±_**1.4**|**78.3**_±_**1.1**|**72.5**_±_**0.9**|54.3_±_1.2|**75.2**_±_**0.6**|**74.4**_±_**0.6**|**76.3**_±_**1.1**|


Figure 3. **Qualitative results of fine-grained manipulation tasks.** Left of the dotted line (coarse stage): (a) project 3D modalities onto orthographic images, then (b) predict heatmaps to mark critical regions. Right of the dotted line (fine stage): using these regions, perform (c) active view selection and (d) active 3D zoom-in for fine-grained manipulation in complex scenes. 

performance, demonstrating strong generalization in visionbased robotic manipulation. The qualitative results for each stage of active perception are presented in Figure 3. 

**Results on COLOSSEUM.** Results in Table 2 show that ActiveVLA achieves a new state of the art on COLOSSEUM, with an average success rate of 65.9% and an average rank of 1.07, outperforming all previous methods. It remains robust to variations in object size, color, lighting, and texture, obtaining 72.4% on MO-SIZE and 64.4% on RO-SIZE. The best performance is observed on Table Color (78.3%) and Camera Pose (76.3%), where it maintains high accuracy despite clutter, distractors, and viewpoint changes. Overall, ActiveVLA surpasses BridgeVLA in most categories, confirming its stronger visual generalization and in- 

Table 3. **Performance on the GemBench benchmark.** Results are reported as mean success rates without confidence intervals. 

|**Method**|**Average**|**L1**|**L2**|**L3**|**L4**|
|---|---|---|---|---|---|
|Hiveformer [19]|30.4|60.3|26.1|35.1|0.0|
|PolarNet [7]|38.4|77.7|37.1|38.5|0.1|
|3D Diffuser Actor [28]|44.0|91.9|43.4|37.0|0.0|
|RVT-2 [18]|44.0|89.1|51.0|36.0|0.0|
|3D-LOTUS [15]|45.7|**94.3**|49.9|38.1|0.3|
|3D-LOTUS++[15]|48.0|68.7|64.5|41.5|**17.4**|
|BridgeVLA [33]|50.0|91.1|65.0|43.8|0.0|
|**ActiveVLA (Ours)**|**51.3**|**92.4**|**66.3**|**45.1**|1.2|


variant representation learning capability. **Results on GemBench.** As shown in Table 3, ActiveVLA 


Figure 4. **Visualization of ActiveVLA in complex manipulation tasks** . It actively perceives and precisely completes tasks despite severe occlusions and complex spatial structures. 

achieves the best performance across core levels L1–L3, with success rates of 92.4%, 66.3%, and 45.1%, surpassing baselines such as 3D-LOTUS++ and BridgeVLA. It attains an overall average of 51.3%, improving upon the previous state of the art by 1.3 percentage points. Although performance decreases on the most difficult L4 tasks (1.2%), ActiveVLA still demonstrates promising long-horizon reasoning and strong 3D perception for precise manipulation. **Real-Robot Analysis.** To evaluate the real-world performance of ActiveVLA, we conduct a series of real-world manipulation experiments under complex and highly occluded scenarios. The tasks involve diverse spatial configurations, such as picking objects from cluttered scenes, retrieving partially hidden items, and manipulating objects with intricate occlusion relationships. As illustrated in Figure 4, ActiveVLA demonstrates strong active perception and precise manipulation capabilities. It effectively infers object geometry and spatial relations through 3D perception, actively selects informative viewpoints, and executes fine-grained actions to complete the tasks successfully. Even when key targets are heavily occluded by other objects or environmental structures, ActiveVLA maintains high accuracy and stability, reflecting its robust spatial understanding and adaptive control in real-world conditions. 

Table 4. **Ablation study on key components.** We report the success rate (%) and inference time (s) over 100 trials. A-VS (Active View Selection) dynamically acquires informative views, while A- 3Z (Active 3D Zoom-in) refines local focus. 


Figure 5. **Success rates of ActiveVLA under different hyperparameters** : (a) Number of selected views; (b) Active 3D zoom-in factor. Experiments are evaluated on the RLBench benchmark. 

fixed-view baseline achieves 87.6% success in 0.26 s per trial. Adding A-VS dynamically selects informative views, raising performance to 89.4% at 0.45 s by improving scene coverage and reducing occlusion. Further introducing A- 3Z enables virtual optical zoom for high-resolution closeups, achieving 91.8% success at 0.53 s. These consistent gains confirm that A-VS guides _where_ to look and A-3Z _how closely_ to observe, forming a hierarchical perception strategy for precise manipulation. 

**Hyperparameter Analysis.** We analyze the effects of the _Number of Views_ and _Zoom-in Factor_ on ActiveVLA. As shown in Figure 5, increasing the number of views improves the success rate from 82.2% (one view) to 91.8% (three views), confirming that multi-view observation enhances spatial understanding and mitigates occlusion. Beyond three views, the performance saturates while computational cost increases. Similarly, increasing the zoomin factor from 1 to 4 boosts precision by enabling finergrained perception, whereas excessive zoom reduces contextual awareness. Therefore, we set the number of views to 3 and the zoom-in factor to 4 for all experiments, striking a balance between global context and local detail. 

## **5. Conclusion** 

### **4.2. Ablation Study** 

**Component Analysis.** We ablate the core active perception modules of ActiveVLA, Active View Selection (A-VS) and Active 3D Zoom-in (A-3Z), on an NVIDIA H100 GPU across RLBench, COLOSSEUM, and GemBench. The 

This paper presents ActiveVLA, a vision-language-action framework that integrates active perception into robotic manipulation. By incorporating Active View Selection and Active 3D Zoom-in within a coarse-to-fine architecture, ActiveVLA enables robots to dynamically adapt their obser- 

vation strategies for enhanced spatial reasoning and finegrained control. By leveraging multi-view 3D perception aligned with VLMs, ActiveVLA effectively balances global context and fine-grained local detail during manipulation. Experiments in both simulated and real-world environments demonstrate its superior performance across diverse tasks. 

## **References** 

- [1] Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed Awadallah, Ammar Ahmad Awan, Nguyen Bach, Amit Bahree, Arash Bakhtiari, Jianmin Bao, Harkirat Behl, et al. Phi-3 technical report: A highly capable language model locally on your phone. _arXiv preprint arXiv:2404.14219_ , 2024. 3 

- [2] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 2 

- [3] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 2, 6 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control, 2024. _URL https://arxiv. org/abs/2410.24164_ . 2 

- [5] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2024. 3 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 2 

- [7] Shizhe Chen, Ricardo Garcia Pinel, Cordelia Schmid, and Ivan Laptev. Polarnet: 3d point clouds for language-guided robotic manipulation. In _Conference on Robot Learning_ , pages 1761–1781. PMLR, 2023. 6, 7 

- [8] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 24185–24198, 2024. 3 

- [9] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ , 2023. 3 

- [10] Sudeep Dasari, Oier Mees, Sebastian Zhao, Mohan Kumar Srirama, and Sergey Levine. The ingredients for robotic dif- 

fusion transformers. _arXiv preprint arXiv:2410.10088_ , 2024. 

3 

- [11] Pengxiang Ding, Han Zhao, Wenjie Zhang, Wenxuan Song, Min Zhang, Siteng Huang, Ningxi Yang, and Donglin Wang. Quar-vla: Vision-language-action model for quadruped robots. pages 352–367. Springer, 2024. 3 

- [12] Pengxiang Ding, Jianfei Ma, Xinyang Tong, Binghong Zou, Xinxin Luo, Yiguo Fan, Ting Wang, Hongchao Lu, Panzhong Mo, Jinxin Liu, et al. Humanoid-vla: Towards universal humanoid control with visual integration. _arXiv preprint arXiv:2502.14795_ , 2025. 3 

- [13] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Chenxi Wang, Junbo Wang, Haoyi Zhu, and Cewu Lu. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot. _arXiv preprint arXiv:2307.00595_ , 2023. 3 

- [14] Ricardo Garcia, Shizhe Chen, and Cordelia Schmid. Towards generalizable vision-language robotic manipulation: A benchmark and llm-guided 3d policy. _arXiv preprint arXiv:2410.01345_ , 2024. 2, 6 

- [15] Ricardo Garcia, Shizhe Chen, and Cordelia Schmid. Towards generalizable vision-language robotic manipulation: A benchmark and llm-guided 3d policy. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 7 

- [16] Theophile Gervet, Zhou Xian, Nikolaos Gkanatsios, and Katerina Fragkiadaki. Act3d: 3d feature field transformers for multi-task robotic manipulation. In _Conference on Robot Learning_ , pages 3949–3965. PMLR, 2023. 2, 6 

- [17] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. Rvt: Robotic view transformer for 3d object manipulation. In _Conference on Robot Learning_ , pages 694– 710. PMLR, 2023. 2, 6, 7 

- [18] Ankit Goyal, Valts Blukis, Jie Xu, Yijie Guo, Yu-Wei Chao, and Dieter Fox. Rvt-2: Learning precise manipulation from few demonstrations. In _RSS 2024 Workshop: Data Generation for Robotics_ , 2024. 2, 6, 7 

- [19] Pierre-Louis Guhur, Shizhe Chen, Ricardo Garcia Pinel, Makarand Tapaswi, Ivan Laptev, and Cordelia Schmid. Instruction-driven history-aware policies for robotic manipulations. In _Conference on Robot Learning_ , pages 175–187. PMLR, 2023. 6, 7 

- [20] Jiangyong Huang, Silong Yong, Xiaojian Ma, Xiongkun Linghu, Puhao Li, Yan Wang, Qing Li, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. An embodied generalist agent in 3d world. In _ICLR 2024 Workshop: How Far Are We From AGI_ . 3 

- [21] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0.5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 2 

- [22] Andrew Jaegle, Sebastian Borgeaud, Jean-Baptiste Alayrac, Carl Doersch, Catalin Ionescu, David Ding, Skanda Koppula, Daniel Zoran, Andrew Brock, Evan Shelhamer, et al. Perceiver io: A general architecture for structured inputs & outputs. In _International Conference on Learning Representations_ . 6, 7 

- [23] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 2, 6 

- [24] Stephen James, Kentaro Wada, Tristan Laidlow, and Andrew J Davison. Coarse-to-fine q-attention: Efficient learning for visual robotic manipulation via discretisation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13739–13748, 2022. 6 

- [25] Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991– 1002. PMLR, 2022. 6 

- [26] Yueru Jia, Jiaming Liu, Sixiang Chen, Chenyang Gu, Zhilue Wang, Longzan Luo, Lily Lee, Pengwei Wang, Zhongyuan Wang, Renrui Zhang, et al. Lift3d foundation policy: Lifting 2d large-scale pretrained models for robust 3d robotic manipulation. _arXiv preprint arXiv:2411.18623_ , 2024. 3 

- [27] Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 2, 3 

- [28] Tsung-Wei Ke, Nikolaos Gkanatsios, and Katerina Fragkiadaki. 3d diffuser actor: Policy diffusion with 3d scene representations. In _8th Annual Conference on Robot Learning_ , 2024. 2, 6, 7 

- [29] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 3 

- [30] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 3 

- [31] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al. Openvla: An open-source vision-language-action model. In _8th Annual Conference on Robot Learning_ . 2 

- [32] Chengmeng Li, Junjie Wen, Yan Peng, Yaxin Peng, Feifei Feng, and Yichen Zhu. Pointvla: Injecting the 3d world into vision-language-action models. _arXiv preprint arXiv:2503.07511_ , 2025. 3 

- [33] Peiyan Li, Yixiang Chen, Hongtao Wu, Xiao Ma, Xiangnan Wu, Yan Huang, Liang Wang, Tao Kong, and Tieniu Tan. Bridgevla: Input-output alignment for efficient 3d manipulation learning with vision-language models. _arXiv preprint arXiv:2506.07961_ , 2025. 6, 7 

- [34] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, 

   - Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 2 

- [35] Fanqi Lin, Yingdong Hu, Pingyue Sheng, Chuan Wen, Jiacheng You, and Yang Gao. Data scaling laws in imitation learning for robotic manipulation, 2024. 3 

- [36] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. _arXiv preprint arXiv:2310.03744_ , 2023. 3 

- [37] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. 3 

- [38] Zhenyang Liu, Yongchong Gu, Sixiao Zheng, Xiangyang Xue, and Yanwei Fu. Trivla: A unified triple-system-based unified vision-language-action model for general robot control. _arXiv preprint arXiv:2507.01424_ , 2025. 2 

- [39] Zhenyang Liu, Yikai Wang, Kuanning Wang, Longfei Liang, Xiangyang Xue, and Yanwei Fu. Spatial-temporal aware visuomotor diffusion policy learning. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 7122–7131, 2025. 3 

- [40] Zhenyang Liu, Yikai Wang, Sixiao Zheng, Tongying Pan, Longfei Liang, Yanwei Fu, and Xiangyang Xue. Reasongrounder: Lvlm-guided hierarchical feature splatting for open-vocabulary 3d visual grounding and reasoning. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 3718–3727, 2025. 3 

- [41] Zhenyang Liu, Sixiao Zheng, Siyu Chen, Cairong Zhao, Longfei Liang, Xiangyang Xue, and Yanwei Fu. A neural representation framework with llm-driven spatial reasoning for open-vocabulary 3d visual grounding. In _Proceedings of the 33rd ACM International Conference on Multimedia_ , pages 1042–1051, 2025. 3 

- [42] Haoyu Lu, Wen Liu, Bo Zhang, Bingxuan Wang, Kai Dong, Bo Liu, Jingxiang Sun, Tongzheng Ren, Zhuoshu Li, Hao Yang, et al. Deepseek-vl: towards real-world visionlanguage understanding. _arXiv preprint arXiv:2403.05525_ , 2024. 3 

- [43] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ , 2022. 7 

- [44] Dantong Niu, Yuvan Sharma, Giscard Biamby, Jerome Quenum, Yutong Bai, Baifeng Shi, Trevor Darrell, and Roei Herzig. Llarva: Vision-action instruction tuning enhances robot learning. _arXiv preprint arXiv:2406.11815_ , 2024. 3 

- [45] Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, et al. Open x-embodiment: Robotic learning datasets and rt-x models. 2024. 3 

- [46] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 3 

- [47] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and 

Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 3 

- [48] Wilbert Pumacay, Ishika Singh, Jiafei Duan, Ranjay Krishna, Jesse Thomason, and Dieter Fox. The colosseum: A benchmark for evaluating generalization for robotic manipulation. _arXiv preprint arXiv:2402.08191_ , 2024. 2, 6 

- [49] Guocheng Qian, Yuchen Li, Houwen Peng, Jinjie Mai, Hasan Hammoud, Mohamed Elhoseiny, and Bernard Ghanem. Pointnext: Revisiting pointnet++ with improved training and scaling strategies. _Advances in neural information processing systems_ , 35:23192–23204, 2022. 6 

- [50] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 2, 3 

- [51] Nikhila Ravi, Jeremy Reizenstein, David Novotny, Taylor Gordon, Wan-Yen Lo, Justin Johnson, and Georgia Gkioxari. Accelerating 3d deep learning with pytorch3d. _arXiv:2007.08501_ , 2020. 4 

- [52] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiveractor: A multi-task transformer for robotic manipulation. In _Conference on Robot Learning_ , pages 785–799. PMLR, 2023. 2, 6 

- [53] Gemma Team, Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju, Shreya Pathak, Laurent Sifre, Morgane Rivi`ere, Mihir Sanjay Kale, Juliette Love, et al. Gemma: Open models based on gemini research and technology. _arXiv preprint arXiv:2403.08295_ , 2024. 6 

- [54] Xinyang Tong, Pengxiang Ding, Donglin Wang, Wenjie Zhang, Can Cui, Mingyang Sun, Yiguo Fan, Han Zhao, Hongyin Zhang, Yonghao Dang, et al. Quartonline: Latency-free large multimodal language model for quadruped robot learning. _arXiv preprint arXiv:2412.15576_ , 2024. 3 

- [55] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 2, 3 

- [56] Taiyi Wang, Zhihao Wu, Jianheng Liu, Jianye Hao, Jun Wang, and Kun Shao. Distrl: An asynchronous distributed reinforcement learning framework for on-device control agents. _arXiv preprint arXiv:2410.14803_ , 2024. 3 

   - [60] Rujia Yang, Geng Chen, Chuan Wen, and Yang Gao. Fp3: A 3d foundation policy for robotic manipulation. _arXiv preprint arXiv:2503.08950_ , 2025. 3 

   - [61] Wentao Yuan, Jiafei Duan, Valts Blukis, Wilbert Pumacay, Ranjay Krishna, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. Robopoint: A vision-language model for spatial affordance prediction for robotics. _arXiv preprint arXiv:2406.10721_ , 2024. 6 

   - [62] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 3 

   - [63] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11975–11986, 2023. 6 

   - [64] Han Zhao, Min Zhang, Wei Zhao, Pengxiang Ding, Siteng Huang, and Donglin Wang. Cobra: Extending mamba to multi-modal large language model for efficient inference. 2025. 3 

   - [65] Wei Zhao, Pengxiang Ding, Min Zhang, Zhefei Gong, Shuanghao Bai, Han Zhao, and Donglin Wang. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. _arXiv preprint arXiv:2502.13508_ , 2025. 3 

   - [66] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 2, 3 

   - [67] Zhongyi Zhou, Yichen Zhu, Minjie Zhu, Junjie Wen, Ning Liu, Zhiyuan Xu, Weibin Meng, Ran Cheng, Yaxin Peng, Chaomin Shen, et al. Chatvla: Unified multimodal understanding and robot control with vision-language-action model. _arXiv preprint arXiv:2502.14420_ , 2025. 3 

   - [68] Minjie Zhu, Yichen Zhu, Xin Liu, Ning Liu, Zhiyuan Xu, Chaomin Shen, Yaxin Peng, Zhicai Ou, Feifei Feng, and Jian Tang. Mipha: A comprehensive overhaul of multimodal assistant with small language models. _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2025. 3 

   - [69] Yichen Zhu, Minjie Zhu, Ning Liu, Zhiyuan Xu, and Yaxin Peng. Llava-phi: Efficient multi-modal assistant with small language model. In _Proceedings of the 1st International Workshop on Efficient Multimedia Computing under Limited_ , pages 18–22, 2024. 3 

- [57] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _arXiv preprint arXiv:2409.12514_ , 2024. 3 

- [58] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 3 

- [59] Tete Xiao, Ilija Radosavovic, Trevor Darrell, and Jitendra Malik. Masked visual pre-training for motor control. _arXiv preprint arXiv:2203.06173_ , 2022. 7 

# **ActiveVLA: Injecting Active Perception into Vision-Language-Action Models for Precise 3D Robotic Manipulation** 

# Supplementary Material 

## **1. Video** 

The attached video demonstrates the capabilities of our proposed **ActiveVLA** , a vision–language–action framework that transforms perception from a passive sensing mechanism into an active, hypothesis-driven process. Unlike prior VLA systems that rely on static or wrist-mounted cameras and thus fail under severe occlusion, ActiveVLA explicitly integrates **active viewpoint selection** and **active 3D zoomin** to dynamically acquire high-quality visual information. 

The video consists of four manipulation scenarios intentionally designed with **complex occlusion patterns, challenging spatial relationships, and fine-grained geometric constraints** . In each scenario, the robot must actively decide both _where to look_ and _what region to zoom into_ before determining _how to act_ . Below, we provide a technically detailed explanation of each task. 

**Task 1: “Retrieving a Towel from Layered Drawers”** _Technical challenge summary:_ This task contains **selfinduced structural occlusion** caused by multi-layer drawer geometry, where the target towel is partially or fully hidden behind drawer faces, internal shadows, and nested surfaces. The occlusion pattern is depth-dependent and viewpointsensitive, making monocular observation insufficient. 

In this scenario, the towel resides inside a stack of layered drawers, where only a small portion of its surface is visible from most viewpoints. The nested geometric layout creates severe internal occlusion, preventing accurate state estimation from a single view. 

- ActiveVLA performs **active viewpoint probing** , selecting camera poses that maximize visibility of internal drawer regions and break geometric occlusion cycles. 

- After obtaining partial exposure of the towel surface, ActiveVLA triggers **active 3D zoom-in** to construct a highresolution local representation, enabling precise localization of edges, depth discontinuities, and graspable regions despite the heavy geometric occlusion. 

This scenario demonstrates ActiveVLA’s ability to resolve internal structural occlusion and extract fine-grained geometry for accurate picking. 

**Task 2: “Picking a Red Block and Placing It onto a Green Block”** _Technical challenge summary:_ This scene features **multi-object mutual occlusion** and **long-horizon relational constraints** . The red block is obscured by clutter objects, while the placement target (green block) is itself partially occluded and requires long-range spatial reasoning to ensure stable stacking. 

In this cluttered tabletop setting, the red block is heavily obscured by surrounding objects, and its visible surface varies drastically across viewpoints. The task further requires placing the block onto a target that is also occluded. 

- Through **occlusion-aware viewpoint planning** , ActiveVLA obtains a sequence of camera poses that reveal the red block’s true geometry and reduce ambiguity arising from clutter-induced occlusion. 

- With the red and green blocks exposed, ActiveVLA applies **targeted 3D zoom-in** to build a high-resolution geometric representation of both objects, enabling accurate grasping and stable long-horizon placement. This task highlights ActiveVLA’s capability to jointly re- 

- solve clutter occlusion and plan fine-grained manipulation over extended horizons. 

**Task 3: “Grasping an Occluded Banana Among Multiple Fruits”** _Technical challenge summary:_ This scenario presents **dense, heterogeneous occlusion** where the target (banana) is partially surrounded and occluded by fruits of irregular shapes. The occlusion is non-convex, multi-body, and view-dependent, making it challenging for any passive perception system to identify graspable surface regions. 

The banana is deeply embedded within a bowl of multiple fruits, with only tiny fragments of its surface visible from typical camera views. The non-uniform shapes of the surrounding objects produce occlusion boundaries. 

- ActiveVLA performs **viewpoint sweeps** to uncover minimal exposed areas of the banana, actively reducing multiobject occlusion by selecting informative perspectives. 

- Upon identifying a candidate grasp region, ActiveVLA uses **active 3D zoom-in** to extract high-resolution local geometry, ensuring a stable and collision-free grasp while preserving the arrangement of surrounding fruits. This task demonstrates ActiveVLA’s ability to handle 

- dense, irregular occlusion structures and perform precision manipulation in cluttered environments. 

**Task 4: “Retrieving an Occluded Purple Cup from a Hanging Rack”** _Technical challenge summary:_ This task involves **relational occlusion among articulated or suspended objects** . The purple cup is occluded by other hanging cups whose curved geometries create highly viewdependent visibility, requiring multi-view reasoning to identify graspable handles and collision-safe approach trajectories. 

The target purple cup is positioned behind multiple hanging cups on a rack. From several viewpoints, its handle and 

Table 5. **Success rates (%) on the Real-World Experiment.** We compare our **ActiveVLA** with more baselines on real-world tasks. The tasks involve complex spatial occlusion and manipulation. 

|**Method**|_Retrieving Towel_|_Red to Green Block_|_Occluded Banana_|_Occluded Purple Cup_|**Overall**|
|---|---|---|---|---|---|
|Diffusion Policy|26_±_2|38_±_4|42_±_2|35_±_2|35.3|
|VPP|52_±_2|48_±_7|58_±_2|64_±_3|55.5|
|TriVLA|68_±_4|54_±_3|62_±_2|72_±_2|64.0|
|RVT-2|77_±_4|63_±_2|72_±_4|78_±_5|72.5|
|**ActiveVLA (ours)**|**92**_±_**2**|**95**_±_**3**|**91**_±_**5**|**89**_±_**2**|91.8|


graspable regions are entirely invisible due to occlusion. 

- ActiveVLA evaluates the occlusion graph of the hanging rack and selects **optimal exploratory viewpoints** that maximally expose the occluded cup without disturbing neighboring objects. 

- After isolating the purple cup visually, **3D zoom-in** is applied to recover detailed geometry around the handle region, enabling precise grasping and safe extraction. 

This scenario showcases ActiveVLA’s strength in reasoning about occlusion in relational object structures, and performing grasping under strict collision constraints. 

## **2. Additional Quantitative Results** 

We conduct further quantitative evaluations on real-world manipulation tasks that involve complex spatial arrangements and occlusions. The selected tasks include: 1) _Retrieving a Towel from Layered Drawers_ , which requires reasoning about objects partially hidden in layered drawer configurations; 2) _Picking a Red Block and Placing It onto a Green Block_ , requiring precise spatial alignment under cluttered conditions; 3) _Grasping an Occluded Banana Among Multiple Fruits_ , which tests the model’s ability to identify and manipulate partially obstructed objects; 4) _Retrieving an Occluded Purple Cup from a Hanging Rack_ , which involves fine-grained spatial reasoning. 

Table 5 presents the success rates of baselines, including Diffusion Policy, VPP, TriVLA, and RVT-2, as well as our proposed ActiveVLA. Across all tasks, TriVLA demonstrates strong performance, highlighting its capability to reason over spatial structures and handle occlusions. RVT2 improves on certain tasks, particularly in aligning and grasping objects under partial visibility. 

ActiveVLA further advances performance by leveraging _active perception_ , enabling the agent to autonomously select informative viewpoints, dynamically adjust camera zoom, and focus on regions of interest. This proactive sensing reduces uncertainty in partially observed environments, disambiguates occluded objects, and allows manipulation actions to be executed more precisely. Quantitatively, ActiveVLA improves the success rate over TriVLA by 24% on _Retrieving a Towel_ , 41% on _Red to Green Block_ , 29% on _Occluded Banana_ , and 17% on _Occluded Purple Cup_ , 

achieving an overall success rate of 96.3%. 

These results demonstrate that integrating active perception with high-level policy reasoning is crucial for realworld robotic manipulation, particularly in cluttered and occluded environments. Beyond overall success rates, ActiveVLA’s ability to strategically explore and adapt its observations provides a generalizable framework for robust manipulation in partially observable and dynamically structured scenarios. 

## **3. Additional Implementation Details** 

**Training Stages.** ActiveVLA is optimized through sequential stages: training on RLBench, COLOSSEUM, GemBench, and finally real-world robot data. All stages share an identical optimization pipeline. Throughout the entire training process, we keep both the SigLIP vision encoder and the language token embeddings frozen to avoid representation drift and to maintain a stable perceptual backbone under actively changing viewpoints. 

**RLBench Training.** For RLBench, we adopt a learning rate of 8 _×_ 10<sup>_−_5</sup> with AdamW and a batch size of 192, without warmup. Fine-tuning is performed for 90,000 steps on 16 NVIDIA H100 GPUs (approximately 20 hours). This stage instills strong visuomotor priors and teaches the model to resolve structured manipulation tasks involving partial occlusions, multi-object interactions, and geometricallyconstrained contact dynamics. 

**COLOSSEUM Training.** The COLOSSEUM stage uses the same optimization configuration as RLBench: a learning rate of 8 _×_ 10<sup>_−_5</sup> , AdamW, batch size 192, and no warmup. Training spans 90,000 steps on 16 NVIDIA H100 GPUs (about 20 hours). Compared to RLBench, COLOSSEUM introduces procedurally generated spatial layouts and high-frequency viewpoint perturbations, enabling ActiveVLA to acquire stronger invariance to transient selfocclusion, clutter-induced ambiguity, and large-scale geometric variations. 

**GemBench Training.** For GemBench, we maintain the learning rate of 8 _×_ 10<sup>_−_5</sup> and AdamW while adjusting the batch size to 160 to accommodate longer trajectories and higher per-sample memory cost. Training is conducted for 50 epochs on 32 NVIDIA H100 GPUs (roughly 8 hours). 

Table 6. **Success rates (%) of ActiveVLA under different perturbations in COLOSSEUM.** We report mean and standard deviation over multiple trials for tasks with diverse visual and spatial perturbations. ActiveVLA achieves consistently high performance, demonstrating robustness to environmental variations and the benefit of active perception for precise manipulation. 

|Task Name|Original|All Perturbations|MO-COLOR|RO-COLOR|MO-TEXTURE|RO-TEXTURE|MO-SIZE|RO-SIZE|Light Color|Table Color|Table Texture|Distractor|Background Texture|RLBench|Camera Pose|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|basketball<br>~~i~~n<br>~~h~~oop|100.0_±_0.0|6.2_±_3.1|96.3_±_1.5|96.7_±_0.0|86.5_±_5.0|-|100.0_±_0.0|69.5_±_0.0|100.0_±_0.0|100.0_±_0.0|100.0_±_0.0|38.7_±_2.0|<br>100.0_±_0.0|100.0_±_0.0|100.0_±_0.0|
|close<br>~~b~~ox|100.0_±_0.0|73.5_±_1.8|95.9_±_1.2|-|-|-|94.8_±_1.7|-|100.0_±_0.0|100.0_±_0.0|99.3_±_1.2|99.0_±_1.3|100.0_±_0.0|98.5_±_1.4|100.0_±_0.0|
|close<br>~~l~~aptop<br>~~l~~id|100.0_±_0.0|12.3_±_14.5|84.0_±_3.5|-|-|-|69.5_±_14.0|-|90.7_±_7.8|93.2_±_0.0|98.5_±_3.5|84.3_±_6.5|97.5_±_3.0|100.0_±_0.0|97.5_±_0.0|
|empty<br>~~d~~ishwasher|0.0_±_0.0|0.5_±_1.5|2.5_±_1.2|1.7_±_1.8|-|2.0_±_1.5|4.5_±_3.0|0.0_±_0.0|0.0_±_0.0|0.0_±_0.0|0.5_±_0.8|0.5_±_1.5|1.5_±_1.2|1.7_±_1.0|0.0_±_0.0|
|get<br>~~i~~ce<br>~~f~~rom<br>~~f~~ridge|95.5_±_1.5|6.2_±_2.0|88.5_±_1.5|91.2_±_6.8|92.0_±_4.8|-|85.3_±_3.0|74.5_±_1.5|97.5_±_3.0|99.5_±_1.5|90.7_±_7.0|57.5_±_8.0|95.5_±_1.2|97.2_±_3.0|99.0_±_1.5|
|hockey|59.5_±_4.5|10.5_±_3.5|46.7_±_6.0|52.0_±_7.5|-|52.5_±_12.0|48.3_±_7.8|66.0_±_4.8|46.7_±_1.5|65.5_±_8.0|54.0_±_1.5|21.5_±_3.0|57.5_±_5.0|51.5_±_5.0|52.3_±_5.0|
|insert<br>~~o~~nto<br>~~s~~quare<br>~~p~~eg|94.7_±_3.0|24.5_±_2.0|53.5_±_3.0|95.2_±_1.5|-|77.5_±_8.0|86.7_±_3.5|71.5_±_3.0|85.0_±_0.0|89.5_±_3.0|89.2_±_3.0|45.5_±_11.0|87.5_±_1.5|78.5_±_5.0|96.0_±_0.0|
|meat<br>~~o~~n<br>~~g~~rill|96.5_±_0.0|10.5_±_1.5|33.5_±_0.0|89.5_±_5.0|-|-|100.0_±_0.0|-|100.0_±_0.0|93.5_±_6.0|92.0_±_1.5|99.5_±_1.5|98.7_±_1.5|100.0_±_0.0|100.0_±_0.0|
|move<br>~~h~~anger|38.7_±_3.0|3.8_±_3.0|27.5_±_3.0|48.5_±_3.0|-|-|-|-|53.5_±_0.0|85.0_±_0.0|53.7_±_5.0|53.0_±_5.0|34.5_±_5.0|44.0_±_1.5|25.0_±_0.0|
|open<br>~~d~~rawer|97.0_±_0.0|61.5_±_3.0|98.0_±_1.5|-|-|-|91.5_±_1.5|-|89.5_±_3.0|94.5_±_1.5|100.0_±_0.0|91.5_±_1.5|100.0_±_0.0|95.0_±_1.5|96.5_±_0.0|
|place<br>~~w~~ine<br>~~a~~t<br>~~r~~ack<br>~~l~~ocation|89.5_±_5.0|18.5_±_13.0|84.5_±_5.0|90.7_±_7.0|-|93.5_±_6.0|94.5_±_3.5|91.5_±_3.5|91.5_±_5.0|98.5_±_1.5|89.5_±_3.0|75.5_±_3.5|91.5_±_6.0|93.5_±_3.0|93.5_±_8.0|
|put<br>~~m~~oney<br>~~i~~n<br>~~s~~afe|95.5_±_1.5|7.5_±_4.8|80.0_±_1.5|76.5_±_1.5|82.5_±_6.5|90.5_±_5.0|93.5_±_3.0|-|38.5_±_12.0|85.5_±_3.0|85.5_±_3.0|85.5_±_3.0|90.5_±_1.5|87.5_±_8.0|87.5_±_1.5|
|reach<br>~~a~~nd<br>~~d~~rag|100.0_±_0.0|0.5_±_0.0|90.5_±_3.5|96.0_±_0.0|96.0_±_5.0|85.5_±_5.0|95.5_±_1.5|39.5_±_5.0|93.5_±_3.0|89.5_±_5.5|79.5_±_3.5|29.5_±_8.0|100.0_±_0.0|100.0_±_0.0|95.5_±_3.5|
|scoop<br>~~w~~ith<br>~~s~~patula|96.5_±_3.0|7.5_±_1.5|95.5_±_1.5|94.5_±_1.5|86.5_±_3.5|86.5_±_3.5|79.5_±_3.5|87.5_±_5.0|91.5_±_1.5|89.5_±_6.0|78.5_±_1.5|21.5_±_5.0|91.5_±_6.0|90.5_±_1.5|94.5_±_1.5|
|setup<br>~~c~~hess|11.5_±_1.5|0.5_±_0.0|2.5_±_1.5|8.5_±_0.0|9.0_±_3.0|-|14.5_±_1.5|-|13.5_±_5.0|22.5_±_8.0|14.5_±_3.5|6.5_±_1.5|21.5_±_5.0|17.5_±_5.0|5.5_±_3.0|
|slide<br>~~b~~lock<br>~~t~~o<br>~~t~~arget|100.0_±_0.0|25.5_±_3.0|75.5_±_1.5|-|93.5_±_3.0|-|-|-|100.0_±_0.0|100.0_±_0.0|99.5_±_1.5|85.5_±_9.5|100.0_±_0.0|100.0_±_0.0|100.0_±_0.0|
|stack<br>~~c~~ups|60.5_±_3.5|30.5_±_1.5|68.5_±_1.5|-|52.0_±_1.5|-|45.5_±_3.0|-|64.0_±_1.5|65.5_±_3.0|66.5_±_8.0|28.5_±_7.0|74.5_±_8.0|65.5_±_14.0|73.5_±_8.0|
|straighten<br>~~r~~ope|63.0_±_6.5|9.5_±_5.0|17.5_±_5.0|-|49.5_±_3.0|-|-|-|63.5_±_9.0|66.5_±_1.5|55.5_±_8.0|38.5_±_5.0|71.5_±_8.0|67.5_±_7.5|73.5_±_6.5|
|turn<br>~~o~~ven<br>~~o~~n|94.5_±_1.5|86.5_±_3.5|95.5_±_3.5|-|-|-|91.5_±_1.5|-|94.5_±_3.5|95.5_±_7.0|97.0_±_3.0|97.0_±_3.0|97.0_±_0.0|89.5_±_3.0|100.0_±_0.0|
|wipe<br>~~d~~esk|0.0_±_0.0|0.5_±_0.0|0.5_±_0.0|0.5_±_0.0|0.5_±_0.0|-|0.5_±_0.0|-|0.0_±_0.0|0.0_±_0.0|0.0_±_0.0|0.0_±_0.0|0.0_±_0.0|0.0_±_0.0|0.0_±_0.0|
|Task Mean|74.5_±_0.7|20.0_±_2.0|62.0_±_1.0|65.0_±_0.1|65.0_±_1.5|70.0_±_3.0|71.0_±_1.0|63.0_±_0.8|71.0_±_1.2|77.0_±_0.9|73.0_±_0.7|53.0_±_1.5|76.0_±_1.0|74.0_±_0.2|75.0_±_0.3|


This dataset emphasizes precise, fine-grained manipulation with dense clutter, demanding accurate feature localization and precise 3D reasoning under persistent occlusions. **Real-robot Fine-tuning.** In the final stage, we adapt the model to real-world data using a smaller learning rate of 2 _×_ 10<sup>_−_5</sup> with AdamW and a batch size of 192. Realrobot fine-tuning is performed on 8 NVIDIA H100 GPUs for 400 epochs (approximately 2 hours). This step calibrates ActiveVLA’s viewpoint selection and 3D zoom-in modules to real sensor noise, illumination variations, and complex, non-procedural occlusion patterns encountered during physical execution. 

**Training Stability and Optimization Notes.** Across all stages, we apply gradient clipping at a maximum norm of 1.0 and use cosine learning rate decay. Freezing the vision and language encoders ensures that active viewpoint shifts do not destabilize the multimodal embedding space. Only the action head, viewpoint selection module, and 3D zoomin module are updated during training. 

## **4. Details of Simulation Tasks** 

For the simulation, ActiveVLA is evaluated across three major benchmarks, covering a broad distribution of manipulation difficulty, task compositionality, and robustness challenges. As shown in Figure 6, these benchmarks include structured multi-step manipulation, perturbation-heavy robustness evaluation, and hierarchical skill composition, collectively forming a comprehensive simulation suite. This section provides a detailed overview of these simulation do- 

mains. The experimental results are shown in Table 6. 

**RLBench.** RLBench serves as the foundational simulation benchmark for ActiveVLA, consisting of 18 visually and physically diverse manipulation tasks executed using a 7-DoF Franka Panda manipulator. Each task is equipped with 100 expert demonstrations generated in the RLBench pipeline. The robot receives synchronized RGB-D observations from four extrinsically calibrated cameras, providing multi-view coverage that enables ActiveVLA to reason about occluded objects and viewpoint-dependent geometry. RLBench tasks span fine-grained pick-and-place operations, articulated-object interactions, and multi-stage routines requiring precise control of contact transitions. The benchmark is built on PyRep and CoppeliaSim, offering deterministic physics, contact modeling, and scene-level randomization. These characteristics make RLBench a controlled yet sufficiently diverse domain for learning structured visuomotor policies. 

**COLOSSEUM.** COLOSSEUM extends RLBench into a perturbation-rich robustness benchmark by introducing 12 systematic variation types across object geometry, material, scene layout, kinematics, lighting, and camera configuration. These perturbations include distribution shifts in object shape and mass, pose-domain noise, distractor injection, background and lighting alterations, and adversarial camera placement changes that severely affect visibility. Each perturbation type is procedurally generated with controlled parameter ranges, enabling a quantitative evaluation of robustness under viewpoint changes and occlusion- 


Figure 6. **Visualization of 18 RLBench tasks.** The tasks cover a diverse set of manipulation challenges, including object grasping, tool use, and complex spatial interactions, illustrating the range of scenarios used for evaluation. 

induced ambiguity. We evaluate ActiveVLA on the same set of tasks as RLBench, but under these structured disturbances. Because COLOSSEUM preserves task semantics while altering environmental statistics, it serves as a stress test for generalization, viewpoint invariance, and policy stability under heavy covariate shift. 

**GemBench.** GemBench is a hierarchical generalization benchmark built upon RLBench. It decomposes manipulation into seven core action primitives (e.g., reaching, grasping, placing, pushing, rotation, alignment), and constructs 16 training tasks and 44 held-out evaluation tasks by composing these primitives in novel combinations. Tasks differ not only in object types and spatial arrangements but also in primitive ordering, interaction dependencies, and multi-step causal structure. Unlike RLBench and COLOSSEUM, where each task follows a predefined demonstration distribution, GemBench requires learning from primitivelevel structure and recombining them to solve previously unseen compositions. This setting challenges the model’s ability to perform long-horizon reasoning, adapt to un- 


Figure 7. **Visualization of direct manipulation tasks.** These tasks evaluate baseline visuomotor skills and include cloth manipulation, highlighting varying physical and spatial challenges. 

familiar task graphs, and maintain consistent visuomotor grounding across compositional variations. The benchmark uses the Franka Panda robot under RLBench physics, with 


Figure 8. **Visualization of occlusion-heavy and spatially complex tasks.** These tasks challenge ActiveVLA’s active viewpoint selection and 3D zoom-in capabilities. They include multi-layered drawer retrieval ( _towel_ ), high-precision stacking with partial occlusion ( _red to green block_ ), collision-aware grasping in clutter ( _occluded banana_ ), and narrow-grasp extraction from a hanging rack ( _purple cup_ ), highlighting severe occlusions, complex geometry, and fine-grained 6D pose reasoning. 

additional environment-induced occlusions and clutter not present in the base tasks. Evaluating on GemBench allows us to measure ActiveVLA’s capacity for skill recomposition, cross-task transfer, and manipulation generalization at the structural level. 

## **5. Details of Real-Robot Tasks** 

We evaluate ActiveVLA on a diverse set of real-robot manipulation tasks that span basic object handling, articulatedobject interaction, non-prehensile control, and complex occlusion-heavy scenarios. All experiments are conducted on a Franka Panda robot equipped with an eye-in-hand RGB-D sensor and two auxiliary static cameras, enabling multi-view observations under natural occlusion. 

**Direct Manipulation Tasks.** As shown in Figure 7, the first group consists of relatively straightforward manipulation tasks designed to assess baseline visuomotor competence: 

- _Wiping the table with a towel_ : The robot grasps a deformable pink towel and wipes a specified region of a black tabletop. Mild uncertainties arise due to cloth deformation and contact variability. 

- _Picking up an orange and placing it into a basket_ : The robot must reliably grasp a spherical object and place it into a confined container, requiring stable grasp synthesis and precise placement. 

- _Opening an orange drawer and placing a mouse inside_ : This sequential task requires articulated-object manipulation, followed by object retrieval and placement within a restricted drawer volume. 

- _Pushing a blue bowl in front of a green plate_ : A nonprehensile manipulation task that relies on continuous contact and collision-free motion in a cluttered planar environment. 

- _Pressing a red button on the desk_ : A reach-and-interact task requiring accurate end-effector pose control but minimal physical complexity. 

**Occlusion-Heavy and Spatially Complex Tasks.** As shown in Figure 8, The second group contains tasks explicitly designed to challenge ActiveVLA’s active viewpoint selection and 3D zoom-in mechanisms. These tasks include severe occlusion, multi-layer geometry, and fine-grained 6D pose reasoning: 

- _Retrieving a towel from layered drawers_ : The robot must identify the correct drawer, reason about partial occlusions, actuate the drawer, and extract the towel from a tightly constrained multi-layer structure. 

- _Picking a red block and placing it onto a green block_ : A high-precision stacking task where the target object is partially occluded or surrounded by distractors, demanding fine-grained localization and vertical alignment. 

- _Grasping an occluded banana among multiple fruits_ : The banana is frequently hidden beneath or between other fruits, requiring collision-aware grasp planning and viewpoint selection in dense clutter. 

- _Retrieving an occluded purple cup from a hanging rack_ : The rack geometry induces persistent occlusions and narrow allowable grasp regions. The robot must infer the 3D pose of the cup and extract it without contacting objects. These occlusion-heavy tasks pose substantially greater 

- challenges due to compounded visibility constraints, irregular geometry, and the need for precise 6D pose inference. 

