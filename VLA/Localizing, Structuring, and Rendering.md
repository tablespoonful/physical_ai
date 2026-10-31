---
title: "Localizing, Structuring, and Rendering: Bridging 3D and 2D Vision-Language-Action Models for Robotic Manipulation"
date: "2026"
venue: "CVPR 2026"
url: https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_Localizing_Structuring_and_Rendering_Bridging_3D_and_2D_Vision-Language-Action_Models_CVPR_2026_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2026/papers/Zhao_Localizing_Structuring_and_Rendering_Bridging_3D_and_2D_Vision-Language-Action_Models_CVPR_2026_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhao_Localizing_Structuring_and_Rendering_Bridging_3D_and_2D_Vision-Language-Action_Models_CVPR_2026_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_Localizing_Structuring_and_Rendering_Bridging_3D_and_2D_Vision-Language-Action_Models_CVPR_2026_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Localizing, Structuring, and Rendering: Bridging 3D and 2D Vision-Language-Action Models for Robotic Manipulation** 

Yunlong Zhao<sup>1</sup> Xiaoheng Deng<sup>1*</sup> Yichao Cao<sup>1</sup> Yi Chen<sup>2</sup> Xiangjian He<sup>7</sup> Shan You<sup>3</sup> Shuo Yang<sup>5</sup> Lei Fan<sup>6</sup> Fei Wang<sup>4</sup> Xiu Su<sup>1</sup><sup>_∗_</sup> 1Central South University 2Hong Kong University of Science 3SenseTime Research 4ACE ROBOTICS 5Harbin Institute of Technology(Shenzhen) 6University of New South Wales 7The University of Nottingham Ningbo China 

- _{_ zhaoyl741, dxh, caoyichao _}_ @csu.edu.cn, _{_ yichen _}_ @ust.hk, _{_ sean.he _}_ @nottingham.edu.cn 

   - _{_ youshan _}_ @sensetime.com, _{_ shuoyang _}_ @hit.edu.cn, _{_ lei.fan1 _}_ @unsw.edu.au, 


Figure 1. 2D VLA models (left-top) leverage intuitive semantic perception from multi-view transformers but st ~~ru~~ ggle with explicit 3D spatial reasoning. 3D VLA models (left-bottom) achieve precise spatial perception through point clouds and v ~~o~~ xe ~~l~~ s but sacrifi ~~<u>ce visual</u>~~ interpretability. Our method bridges these paradigms by embedding spatial semantics into images via different ~~iable rendering.~~ 

## **Abstract** 

_Robotic manipulation in complex 3D environments requires unifying spatial reasoning with intuitive visual perception, which is a capability that current Vision-Language-Action paradigms address separately. While 3D VLAs excel in geometric and physical reasoning, they lack intuitive, imagelevel understanding and dense visual semantics; conversely, 2D VLAs (even with depth image) provide rich visual intuition and semantic continuity but miss explicit spatial global grounding. We introduce DiffRender-VLA, a differentiable rendering–based framework that bridges 3D and 2D VisionLanguage-Action models through gradient-consistent visual mediation. It generates differentiable images by lo-_ 

_calizing the next end-effector target with a world-aligned cube marker, differentiably structuring surrounding geometry whose color encodes spatial relations to the marker, and rendering adaptive viewpoints optimized to reveal the target–environment spatial relationships. These differentiable images serve as visual bridges, embedding spatial semantics while allowing gradients from 2D VLAs to backpropagate into 3D representations, thereby coupling geometric reasoning with visual perception. This closed differentiable loop unifies reasoning and perception, substantially improving performance under occlusion, clutter, and complex spatial manipulation tasks, achieving average improvements of +12.1% over state-of-the-art methods. Codes are available at https://github.com/zyl123456aB/DIFFVLA._ 

*Corresponding author is Xiu Su and Xiaoheng Deng 

20812 

## **1. Introduction** 

Robotic manipulation in complex 3D environments remains a central challenge in artificial intelligence and robotics. Despite advances in computer vision [15], natural language processing [8], and reinforcement learning [41], robots still struggle to achieve human-level spatial understanding and visually grounded reasoning. The key difficulty lies in coupling geometric reasoning with semantic perception—robots must not only reason about 3D spatial structures but also interpret visual cues in an interpretable, image-centric manner. 

Recent research in vision-language-action (VLA) models has advanced along two complementary directions. _3D spatial VLAs_ , such as PerAct [39] and VoxPoser [17], emphasize precise geometric reasoning through point clouds or voxels, achieving physically grounded action prediction but sacrificing visual intuitiveness. Conversely, _2D visual VLAs_ , such as RT-2 [4], OpenVLA [22], RoboMamba [2], and PaLM-E [9], leverage high-level semantics from images but lack explicit 3D grounding. This dichotomy leaves a gap: 3D VLAs reason geometrically but fail to “see,” while 2D VLAs perceive richly but fail to reason spatially. 

A natural extension to enhance spatial awareness in 2D VLAs is to incorporate depth information. Recent studies such as Depth Helps [37], RoboFlamingo-Plus [26], and DepthVLA [49] adopt RGB-D fusion to provide richer geometric cues and improve manipulation accuracy. While effective to some extent, depth maps remain limited as they describe only surface geometry from a fixed viewpoint and lack explicit encoding of object-to-object spatial relationships. Moreover, most fusion strategies operate at the feature level [38], which improves performance but offers little interpretability regarding how spatial cues are integrated. Thus, despite their benefits, RGB-D approaches still struggle to convey holistic 3D scene understanding in an imageinterpretable and reasoning-compatible manner. 

We propose DiffRender-VLA, a differentiable rendering–based framework that bridges 3D spatial reasoning and 2D visual perception through continuous visual mediation. DiffRender-VLA generates differentiable images by first localizing the next end-effector target and inserting a worldaligned cube marker into the point cloud, then differentiably structuring surrounding geometry whose color encodes spatial relations to the marker, and finally rendering adaptive viewpoints optimized to reveal the spatial configuration between the target and its environment. Together, these components form a closed differentiable loop: localization defines _where to act_ , structuring encodes _what relations exist_ , and rendering determines _how to visualize them_ . This design unifies perception and reasoning, achieving substantial performance gains in occluded, cluttered, and spatially complex manipulation tasks. 

Comprehensive experiments in both simulation and 

real-world robotic systems validate the effectiveness of DiffRender-VLA. It achieves up to **11.2%** performance gain under occlusion, **17.8%** in cluttered scenes, and **13.4%** in tasks requiring intricate spatial reasoning, consistently outperforming RGB- and RGB-D-based methods. These results confirm that differentiable rendering provides an efficient pathway for transferring 3D spatial understanding into visually interpretable action policies. Our main contributions are as follows: 

- We propose DiffRender-VLA, a unified framework that bridges 3D spatial reasoning and 2D visual perception to transfer geometric understanding into imageinterpretable action policies. 

- We introduce a three-stage pipeline (localization, structuring, and rendering) that transforms point-cloud geometry into 2D representations embedding spatial semantics. 

- We demonstrate that differentiable rendering provides a closed gradient loop where 2D VLA losses backpropagate into 3D representations. 

- We achieve state-of-the-art performance with **+12.1%** average improvement over existing methods, validated across both simulation and real-world robotic systems. 

## **2. Related Work** 

**3D VLA Models.** 3D VLA models [5, 21, 24]reason directly in 3D space through explicit geometric representations such as voxels or point clouds. PerAct [39] voxelizes the workspace with Perceiver transformers, C2F-ARM [20] performs coarse-to-fine voxelization, and Act3D [12] applies adaptive point sampling. RVT [13, 14] leverages multi-view transformers, DP3 [52] and 3D Diffuser Actor [21] introduce diffusion-based 3D reasoning, while GNFactor [51] and ManiGaussian [30] employ neural fields and Gaussian splatting for continuous 3D understanding. VoxPoser [17] and Spatial-VLM [6] incorporate languagegrounded 3D reasoning. These spatial approaches excel in geometric precision but sacrifice visual intuitiveness and scalability. Comprehensive reviews [32, 45] emphasize that bridging 3D reasoning with image-based interpretability remains a major problem. 

**2D VLA Models.** 2D VLA models [7, 25, 27] predict actions from visual-language observations, leveraging large-scale pretraining to achieve semantic generalization. Notable systems include RT-1/RT-2 [4], OpenVLA [22], RoboMamba [2], PaLM-E [9], and Pi0 [3]. While offering strong visual understanding, these models lack explicit spatial grounding, leading to errors in fine-grained manipulation. To enrich spatial cues, several works augment RGB inputs with depth or multimodal fusion. Depth Helps [37], RoboFlamingo-Plus [1], and DepthVLA [49] show that depth improves local geometry perception but remains view-dependent and feature-level, offering limited 3D interpretability. Video- and latent-action pretraining ap- 

20813 


Figure 2. Overview of DiffRender-VLA. The framework bridges spatial and 2D VLA paradigms through differentiable rendering: localizing anchors the next manipulation target, structuring encodes surrounding geometry as color-encoded differentiable features, and rendering optimizes viewpoints to project spatial semantics as interpretable, differentiable images. 

proaches such as LAPA [46] introduce temporal groundi <mark>ng</mark> but still operate within 2D projections. Overall, 2D VLAs and their RGB-D variants enhance perceptual richness but lack explicit geometric structure, motivating the need for differentiable mechanisms that embed 3D reasoning into visual representations. 

**Rendering-based Representations.** Rendering provides a natural interface between spatial geometry and visual perception. Voxel or point re-rendering (RVT [13]), neural radiance fields [48], and Gaussian splatting [28, 29, 54, 57, 58] enable view synthesis and cross-view learning, while OmniManip [36] and Goal-VLA [7] exploit rendering for self-correction and goal conditioning. 

We use point-cloud as basic rendering for its efficiency and geometric transparency. Unlike NeRFs or Gaussian splatting, which require scene-specific optimization and complex modeling. Our method offers a lightweight, interpretable bridge between 3D reasoning and 2D perception which fits gradient-based robotic learning. 

## **3. Method** 

We present **DiffRender-VLA** , which, instead of choosing between image-based and 3D reasoning, enables gradient flow to transfer the 3D perception capabilities into 2D VLA models. Figure 2 illustrates the overall framework. 

### **3.1. Localizing Coarse Target Region** 

Given a natural langua <mark>ge instruction</mark> _<mark>I</mark>_ <mark>which is trans</mark> formed to **e** lang by VLM, like [43], and multi-view RGB-D observations _O_ = _{_ **o** _i}_<sup>_M_</sup> _i_ =1<sup>obs,our final goal is to predict a 6-DoF</sup> end-effector action **a** = ( **p** _,_ **r** _, g_ ) where **p** _∈_ R<sup>3</sup> is the target end-effector position, **r** _∈_ R<sup>3</sup> is the rotation (Euler angles), and _g ∈{_ 0 _,_ 1 _}_ is the gripper state. 

We reconstruct a point cloud _P_ and voxelize it into **V** _∈_ R<sup>_D×H×W_</sup> for coarse spatial reasoning [39]. The coarse stage establishes spatial understanding by predicting world-axes–aligned cubic regions containing target endeffector locations. A Perceiver IO encoder [18] jointly processes voxels and language embeddings: 


where **Q** coarse _∈_ R<sup>_D×H×W_</sup> predicts coarse target voxel probabilities over the entire workspace (initial spatial localization), **Z** coarse encodes coarse spatial features for subsequent fusion, and **_θ_** view parameterizes dynamic viewpoints—enabling joint reasoning about target end-effector locations and optimal observation perspectives within a unified encoder. The highest confidence coarse location **p** coarse _∈_ R<sup>3</sup> is computed via a differentiable spatial expectation over **Q** coarse. 

We define a cube _B_ centered at **p** coarse with side length _ℓ_ cube, critically aligned with world axes rather than camera axes. This alignment ensures rendered 2D projections encode spatial information through pure geometry: square 

20814 

projections indicate perpendicular camera views, rectangular distortions reveal oblique angles, and projection sizes inversely correlate with distance. These geometric cues provide implicit depth and orientation interpretable by imagebased models without explicit 3D reasoning. 

### **3.2. Structuring Differential Spatial Information** 

While cube projections reveal camera–target relationships, they lack information about surrounding objects relative to the target end-effector location. Our Structuring module addresses this limitation by transforming abstract 3D relationships into perceptible visual features through colored depth–gradient encoding. 

For each point **x** _∈P_ , we compute the signed distance _dj_ ( **x** ) to cube face _j ∈{_ 1 _, . . . ,_ 6 _}_ , normalized by half-size along the face normal. Each face has a characteristic color **c** _j_ encoding axis direction: red/cyan for _±X_ , green/magenta for _±Y_ , blue/yellow for _±Z_ . Colors follow world axes rather than camera axes, ensuring consistent directional semantics across viewpoints—crucial for generalizable spatial reasoning. Final point color blends original appearance with directional cues: 


where **c** orig( **x** ) is the original RGB color from the point cloud, _dj_ ( **x** ) = sign( **n** _j ·_ ( **x** _−_ **p** _c_ )) _·∥_ **x** _−_ Π _j_ ( **x** ) _∥_ is the signed distance from point **x** to cube face _j_ (where **n** _j_ is the face normal, **p** _c_ is cube center, and Π _j_ denotes projection onto face _j_ ), and **c** _j_ encodes the face’s axis-aligned color. The _r_ target _−∥_ **x** _−_ **<u>p</u>** _c∥_ blending weight _α_ ( **x** ) = _σ_ sig� _σ_ blend � controls color mixing based on distance to the cube, where _σ_ sig( _·_ ) is the sigmoid function, _r_ target and _σ_ blendcm yield peak blending. _k_ beam controls gradient sharpness, creating ”beam” effects where intensity encodes distance and hue encodes direction. 

As shown in Figure 3, our method creates differentiable point clouds with key properties: hue indicates spatial direction aligned with world axes; intensity encodes relative distance to the target location; encoding remains viewpointconsistent. In scenes with vibrant multi-colored objects (e.g., colorful toys), the adaptive blending via _α_ ( **x** ) ensures target-relevant beams remain perceptually dominant. 

Critically, the entire process is differentiable with respect to **p** coarse: when action prediction improves, gradients backpropagate through rendered images to refine cube place- _<u>∂</u>_ **<u>I</u>** _<u>∂</u>_ **<u>c</u>** <u>beam</u> ment and beam encoding (<sup>_<u>∂L</u>_</sup> _∂_ **I**<sup><u>task</u></sup> _→ ∂_ **c** beam<sup>_→_</sup> _∂_ **p** coarse<sup>),en-</sup> abling the encoder to learn optimal spatial representations that transfer 3D understanding into 2D VLA. 

### **3.3. Rendering Adaptive Viewpoint** 

Suboptimal viewpoints severely degrade spatial information—occlusions hide cube faces, unfavorable angles obscure gradients, or cubes appear too small for meaningful cues [33]. Our mechanism learns camera positioning that maximizes spatial visibility in 2D projections. 

We learn viewpoint parameters **_θ_** view (predicted alongside **Q** coarse and **Z** coarse by Φenc above) through action-loss backpropagation. This enables joint reasoning about the target location and observation perspective as a coupling that is difficult to achieve through separate optimization. 

For each dynamic camera _i ∈{_ 1 _, . . . , N_ dyn _}_ , we decode valid parameters ( **R** _i,_ **t** _i, ϕi_ ) = _D_ view( **_θ_** _i_ ) where **R** _i ∈ SO_ (3) is rotation, **t** _i ∈_ R<sup>3</sup> is translation, and _ϕi ∈_ R<sup>+</sup> is field-of-view. Decoder _D_ view ensures plausible configurations through bounded transformations and a 6D rotation representation [56] for stable gradients. 

By learning viewpoints end-to-end through task loss, the model discovers task-relevant perspectives: clearly revealing color gradients from multiple faces (maximizing directional information), minimizing occlusions of the target end-effector region (preserving spatial context), and adjusting field-of-view for sufficient cube size (enhancing perceptibility). Differentiable camera poses enable gradient flow from rendered images back to viewpoint parameters _<u>∂</u>_ **<u>I</u>** _<u>i</u>_ (<sup>_<u>∂</u>_</sup> _∂_<sup>_<u>L</u>_</sup> **I**<sup><u>task</u></sup> _i → ∂_ ( **R** _i,_ **t** _i,ϕi_ )<sup>_→∂_</sup><sup><u>(</u></sup><sup>**R**</sup> _∂_<sup>_i_</sup> **_θ_**<sup>_<u>,</u>_</sup> view<sup>**t**</sup><sup>_i,ϕi_</sup><sup><u>)</u></sup> ), completing the gradient pathway that transfers spatial understanding into imagebased manipulation without expensive viewpoint search. 

### **3.4. Fine-Grained Action Prediction** 

DiffRender-VLA leverages pretrained VLA models [22] as powerful semantic feature extractors while adapting them for spatially aware manipulation. We bridge pretrained visual–language capabilities with 3D manipulation by presenting spatially enriched observations and training the VLA backbone jointly with our spatial embeddings. 

For each viewpoint _i ∈{_ 1 _, . . . , N_ cam _}_ (where _N_ cam = _N_ fix + _N_ dyn includes both fixed baseline and adaptive cameras), we render scenes with spatial markers to obtain views **I** _i_ containing original appearance overlaid with colored beams—making invisible 3D relationships perceptually explicit. The pretrained VLA backbone (e.g., initialized from OpenVLA [22]) processes these views: 


where _ψ_ VLA is the VLA backbone and **Z**<sup>_i_</sup> VLA<sup>areextracted</sup> semantic features. Critically, the VLA backbone is trainable, allowing it to adapt its visual understanding to interpret spatial beam markers and cube projections while preserving semantic knowledge from pretraining, to learn spatial semantics from enriched visual inputs end-to-end. 

20815 


Figure 3. Visualization of differentiable point cloud rendered image. We use RLbench [19] and RH20T [10] dataset for display. 


Figure 4. Visualization of our real-world tasks. For each task, we show several steps to understand the task process. 

We fuse VLA features with coarse spatial context through bidirectional cross-attention: 

**Z** fused = CrossAttn( **Z** coarse _,_ **Z** VLA)+CrossAttn( **Z** VLA _,_ **Z** coarse) 

(4) 

The first term guides VLA features toward spatially relevant regions; the second refines coarse estimates with semantic understanding. This creates complementary synergy: the coarse stage provides explicit 3D scaffolding from voxel 

reasoning; the VLA contributes semantic understanding learned from pretraining and adapted through fine-tuning. Neither alone suffices—spatial context without semantics yields brittle predictions; semantics without spatial grounding cannot achieve precise manipulation. The bidirectional fusion enables both components to co-adapt during training. 

Following standard VLA practice [12, 39], from the fused guided features **Z** fused, we predict the 6-DoF end- 

20816 

Table 1. Simulation results on RLBench. Success rates (%) with standard deviation. Best results in **bold** <u>, second best underlined.</u> 

||||**Occlusio**|**n Tasks**||||**C**|**lutter & Pre**|**cision Ta**|**sks**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|Put<br>Cupboard|Close<br>Jar|Open<br>Drawer|Put<br>Safe|Turn<br>Tap|Sort<br>Shape|Stack<br>Blocks<br>|Put<br>Drawer|Sweep<br>Dustpan|Stack<br>Cups|Insert<br>Peg|Place<br>Wine|**Avg**|
||||||_2D VL_|_A Models_||||||||
|RT-2 [4]|61.5|55.7|75.1|52.3|68.9|58.4|32.4|21.6|56.3|13.2|14.8|60.2|47.5|
|UniVLA [44]|74.2|68.3|88.4|65.8|82.5|71.7|46.1|34.3|69.7|26.3|27.2|73.5|60.7|
|OpenVLA-OFT [23]|67.8|61.2|80.1|58.4|74.8|64.3|39.4|27.5|62.4|18.7|19.8|66.8|53.4|
|VLA-adapter [11]|79.6|72.5|87.9|71.3|83.4|77.8|43.8|31.6|76.4|24.1|33.7|85.2|63.9|
|<br>SmolVLA [40]|71.3|65.7|83.5|62.8|77.2|70.6|40.5|28.3|67.4|21.5|24.8|72.9|57.2|
|Pi0 [3]|73.8|68.4|85.3|65.2|79.7|71.5|42.3|30.1|70.8|23.8|26.4|75.6|59.4|
|TraceVLA [55]|75.9|69.3|84.8|67.1|80.5|74.3|41.2|29.5|72.6|22.7|30.4|79.5|60.6|
||||||_3D VL_|_A Models_||||||||
|PerAct [39]|72.8|63.2|88.0|61.5|78.4|69.2|26.4|16.8|52.0|2.4|5.6|44.8|48.4|
|DP3 [52]|81.5|74.3|88.9|73.2|84.7|79.4|41.8|29.7|76.5|20.3|31.5|86.2|64.0|
|ManiGaussian [30]|83.4|76.1|90.2|75.3|86.5|81.3|43.7|30.5|78.8|22.4|32.7|87.9|65.7|
|Act3D [12]|82.9|75.6|89.8|74.8|85.9|80.8|44.3|31.4|79.2|23.1|33.9|88.4|65.8|
|3D Diffuser [21]|84.3|76.8|89.5|76.1|87.2|82.4|42.1|28.6|78.4|18.9|32.4|87.3|65.3|
|<br>FVP [16]|83.7|76.8|90.5|75.8|86.4|81.9|43.2|30.8|80.3|21.6|32.8|89.5|66.1|
|GWM [31]|85.2|78.3|91.8|77.5|88.6|83.7|46.5|33.8|82.1|25.7|36.4|90.8|68.4|
|**DiffRender-VLA (Ou**|**rs)**<br>**92.8**_±_1_._9|**87.5**_±_1_._6|**95.3**_±_1_._3|**88.4**_±_2_._1|**94.7**_±_1_._5|**91.6**_±_1_._8|**69.3**_±_2_._4<br>**5**|**7.8**_±_2_._7|**96.5**_±_1_._2|**48.6**_±_3_._1|**46.8**_±_2_._|9<br>**97.2**_±_1_._4|**80.5**|
|ffector action th<br>anslation, we rei<br>ggregating sema|rough inde<br>fine the coa<br>ntically inf|penden<br>i  rse spat<br>ormed|t predicti<br>i   ial cube<br>multi-vie|on head<br>i     localiza<br>w pred|s. For<br>i     tion by<br>ictions.|**plac**|**e_shape_in_sorte**|**open**<br>**r**|**_drawer**|**stack**|**i**<br>**_cups**|**nsert_onto_sq**|**uare_peg**|
|or each view_i_o<br>roduce refined tr|f cube, the<br>i anslation s|guided<br>i  cores:|features|are dec|oded to|**p**|**ut_in_cupboard**|**tu**|**rn_tap**|**clos**|**e_jar**|**place_wine**|**_at_rack**|
|**Q**<sup>_i_</sup><br>trans <sup>=</sup><br>**p**<sup>(</sup><sup>_i_) </sup>= <br>here _h_trans is th<br>|<sup>_h_trans(</sup><sup>**Z**</sup><sup>_i_</sup><br>fus<br>Proj<br>~~t~~o<br>~~S~~pa<br>e translatio<br>|ed<sup>)</sup><sup>_∈_R</sup><br>tial<br>�<br>ar<br>n head <br>|<sup>_D×H×W_</sup><br>g max<br>_x,y,z_ <sup>**Q**</sup><br> that refi<br>|<sup>_,_</sup><br><sup>_i_</sup><br>trans<br>�<br>ines the <br>|(5)<br> coarse<br>|**put_**|**item_in_drawer**|**put_m**|**oney_in_safe**|**stack_**|**blocks**|**sweep_to_d**|**ustpan**|


effector action through independent prediction heads. For translation, we refine the coarse spatial cube localization by aggregating semantically informed multi-view predictions. For each view _i_ of cube, the guided features are decoded to produce refined translation scores: 

where _h_ trans is the translation head that refines the coarse prediction **p** coarse (the coarse cube) by incorporating semantic understanding from the VLA backbone. Specifically, **Q**<sup>_i_</sup> trans<sup>represents a refined plane probability distribution fo-</sup> cusing on the surface of the predicted cube _B_ , enhanced by view-specific semantic features from spatially marked images. This refinement transforms the initial workspacewide coarse localization into precise, semantically aware position estimates. **p**<sup>(</sup><sup>_i_)</sup> is the transofrmed location of arg max _x,y,z_ **Q** trans<sup>_i_basedontheworldaxis.Thefinalnext</sup> best end-effector location averages across the cube’s surfaces: **p** = 6<sup><u>1</u></sup> �6 _i_ =1<sup>**p**(</sup><sup>_i_).</sup> For rotation, we follow standard discretization into Euler-angle bins [39]. The guided features are max-pooled spatially and decoded to rotation logits: 


Figure 5. Simulation Tasks for Occlusion and Clutter enviroments. 

## **4. Experiments** 

**Simulation Platform & Tasks.** We evaluate on 12 representative tasks from RLBench [19] with Franka Panda. The tasks is shown in Figure 5. These tasks cover diverse challenges including multi-step planning, fine-grained spatial reasoning, and cluttered scene. 

**Real-World Platform & Tasks.** We deploy on an AgileX PIPER with Robotic 2F-85 gripper. As shown in Figure 4, six tasks test key capabilities. Each task runs 20 trials across varied poses and lighting. 


where rotation is discretized into 5<sup>_◦_</sup> bins for three Euler angles. For gripper state, we use a binary classification head: 

**Implementation.** We initialize from OpenVLA [22] (SigLIP [53] + DinoV2 [35], Llama-2-7B [42] backbone) pretrained on Open X-Embodiment [34] and RH20T [10]. 


_Architecture:_ Our spatial reasoning module augments the VLA backbone with a voxel-based encoder: (1) Multiview RGB-D observations are fused into point clouds and voxelized into a 50<sup>3</sup> grid; (2) A Perceiver IO [18] with 2048 latents (dim=512, 6 layers) jointly predicts coarse trans- 

The complete action is **a** = ( **p** _,_ **r** _, g_ ), where each component is predicted independently from the fused features, combining coarse spatial understanding with fine-grained semantic reasoning from the VLA backbone. 

20817 


Figure 6. Real-World Deployment Situation. 

lation heatmaps **Q** coarse, world-aligned cube markers with adaptive sizing ( _ℓ_ cube = 10-15cm, scaled to 0.8 _×_ object size for small targets); (3) We render spatially-enriched images via differentiable beam encoding with axis-aligned RGB gradients, using 300 sampling points per beam, 3-5px thickness, and 0.5-0.7 alpha transparency, then rasterize from learned poses plus 2 fixed cameras 

_Training:_ Simulation uses 100 demos/task, 220 _×_ 220 RGB-D, LAMB optimizer [47] (lr=2 _._ 4 _×_ 10<sup>_−_4</sup> , batch=32, 100k steps). Real-world uses 50 demos/task with identical hyperparameters. Loss weights: _λ_ trans = 1 _._ 0, _λ_ rot = 0 _._ 8, _λ_ grip = 0 _._ 5. The VLA backbone is initialized from OpenVLA; the spatial module trains from scratch. **methods.** We compare against state-of-the-art methods: 

- _2D VLA models_ : Pi0[3], OpenVLA-OFT[23], RT2[4], TraceVLA[55], UniVLA[44], VLA-Adapter[11], SmolVLA [40]; 

- _3D VLA models_ : RVT-2 [14], Peract [39], DP3 [52], Act3D [12], ManiGaussian [30], GWM [31], PerAct [39], 3D Diffuser [21], FVP [16]. 

**Metrics.** Simulation: position error _<_ 2cm, rotation error _<_ 10°, 50 trials/task. Real-world: success rate, translation/rotation error, 20 trials/task. Significance: Bonferroni correction ( _p <_ 0 _._ 05). 

### **4.1. Simulation Results** 

Table 1 presents simulation results on RLBench, where DiffRender-VLA achieves 80.5% average success 

Table 2. Real-world results on AgileX PIPER. Success rates (%) across 20 trials per task. 

|**Method**|Place<br>Cup|Place<br>Plate|Place<br>Stamp|Place<br>Banana|Press<br>Button|Block<br>Stacking|**Avg**|
|---|---|---|---|---|---|---|---|
|DP3 [52]|55.0|50.0|15.0|35.0|25.0|20.0|33.3|
|rvt-2 [14]|75.0|70.0|40.0|55.0|50.0|45.0|55.8|
|OpenVLA-OFT [23]|78.0|73.0|42.0|58.0|52.0|48.0|58.5|
|VLA-Adapter [11]|80.0|75.0|45.0|60.0|55.0|50.0|60.8|
|TraceVLA [55]|65.0|60.0|25.0|45.0|35.0|30.0|43.3|
|Pi0 [3]|77.0|72.0|43.0|57.0|53.0|47.0|58.2|
|**DiffRender-VLA**|**90.0**|**85.0**|**70.0**|**80.0**|**75.0**|**70.0**|**78.3**|
|vs. Best Baseline|+10.0|+10.0|+25.0|+20.0|+20.0|+20.0|+17.5|
|(a) Camera Pose|Densit|y|(b|) Visibili|ty impro|vements||


Figure 7. Adaptive viewpoint analysis validates differentiable camera poses enable task-specific optimization. 

rate.Among 3D methods, DiffRender-VLA outperforms explicit 3D representations while preserving interpretability: DP3 (+16.5%), ManiGaussian (+14.8%), and Act3D (+14.7%). This demonstrates that our differentiable rendering pipeline more effectively embeds 3D spatial semantics into 2D visual representations than direct 3D processing. DiffRender-VLA significantly outperforms 2D visual prompting approaches: TraceVLA (63.9%, +16.6%) and VLA-adapter (60.6%, +19.9%). Unlike temporal history or semantic cues, our spatial beams explicitly encode 3D geometry through color intensity gradients (distance) and world-aligned hues (direction: RGB → XYZ), enabling 2D VLAs to perform physically grounded spatial reasoning. 

Task-specific improvements highlight spatial understanding capabilities: **Occlusion Tasks** : Average 91.7% success (+7.6% over GWM). Adaptive viewpoint optimization reveals occluded targets by rendering perspectives where cube markers and beams remain visible despite obstacles. **Clutter & Precision Tasks** : Average 69.4% success (+24.0% over GWM). Color-encoded beams disambiguate densely packed objects, while cube marker distortions convey fine-grained orientation—compressed cubes indicate approaching angles, elongated projections reveal alignment directions. 

### **4.2. Real-World Deployment Results** 

Table 2 demonstrates that DiffRender-VLA successfully transfers to physical robotic systems, achieving 78.3% average success rate on the AgileX PIPER manipulator. This represents a **+17.5%** improvement over the best baseline (VLA-Adapter: 60.8%), validating real-world applicability. The consistent gains across simulation and physical 

20818 

Table 3. Component ablation. Trans./Rot. Error in cm/degrees. 

|**Variant**|Stack<br>Blk|Insert<br>Peg|Sort<br>Shape|Open<br>Draw|**Avg**|Trans.<br>Err|Rot.<br>Err|
|---|---|---|---|---|---|---|---|
|_w/o_Adaptive View|42.8|26.4|39.7|84.9|71.6|2.3|11.4|
|_w/o_Spatial Beams|45.6|25.9|40.8|85.7|72.5|2.2|10.8|
|_w/o_Coarse Cube|39.9|22.1|35.6|82.1|68.4|2.5|12.6|
||_Gra_|_dient Flo_|_w Valida_|_tion_||||
|Non-Diff. Beams|51.3|31.7|44.2|88.5|74.8|2.0|10.1|
|Non-Diff. Viewpoint|48.7|29.3|42.6|87.2|73.6|2.1|10.5|
|Two-Stage Training<sup>_†_</sup>|55.8|36.4|48.9|90.6|76.2|1.9|9.4|
||_Altern_|_ative Sp_|_atial Enc_|_oding_||||
|Trajectory Traces|52.4|33.8|45.6|89.2|75.3|2.0|9.8|
|<br>Keypoint Markers|49.7|31.2|43.8|87.6|74.1|2.1|10.3|
|Fixed Multi-View|58.3|38.9|50.2|91.5|77.4|1.8|8.9|
|**Full Method**|**69.3**|**46.8**|**57.8**|**95.3**|**80.5**|**1.7**|**8.2**|


> _†_ Training spatial module first, then fine-tuning VLA backbone separately. 


Figure 8. Beam parameters improvement for small objects. 

deployment confirm that color-encoded spatial beams and world-aligned cube markers generalize beyond synthetic environments. DiffRender-VLA substantially outperforms recent approaches: DP3 (33.3%, +45.0%), OpenVLA-OFT (58.5%, +19.8%), Pi0 (58.2%, +20.1%), and TraceVLA (43.3%, +35.0%). These results underscore that our differentiable rendering approach. As shown in Figure 6, Our method encodes spatial relationships through visual beams. providing more reliable spatial cues than implicit 3D representations or temporal visual prompts. 

### **4.3. Ablation Studies** 

Table 3 validates each component and our core hypothesis. **Gradient Flow Validation.** (1) Non-differentiable beams: 74.8% (-5.7%)—beams provide visual cues but cannot optimize placement. (2) Non-differentiable viewpoint: 73.6% (-6.9%)—random views lack task-specific optimization. (3) Two-stage training: 76.2% (-4.3%)—without end-to-end gradient flow, stages cannot co-adapt. These demonstrate differentiability enables spatial knowledge transfer. 

**Alternative Spatial Encoding.** Trajectory traces (inspired by TraceVLA [55]): 75.3% (-5.2%)—temporal history lacks instantaneous 3D geometry. Keypoint markers (inspired by RoboPoint [50]): 74.1% (-6.4%)—lacks directional relationships. Fixed multi-view (inspired by RVT2 [14]): 77.4% (-3.1%)—static views cannot optimize for marker manifestation. Our differentiable spatial beams with adaptive viewpoints provide superior encoding. 

Table 4. Zero-shot generalization. Success (%) and degradation from in-domain. 

|**Condition**|**DiffRender-VLA**|**RVT-2 [14]**|**OpenVLA-OFT [23**|**]**<br>**Gap**|
|---|---|---|---|---|
|In-Domain|80.5|68.4|53.4|12.1/27.1|
|Novel Objects|74.2 (-6.3)|60.1 (-8.3)|43.7 (-9.7)|14.1/30.5|
|Novel Scenes|71.8 (-8.7)|58.6 (-9.8)|41.2 (-12.2)|13.2/30.6|
|Novel Lighting|76.3 (-4.2)|63.9 (-4.5)|48.9 (-4.5)|12.4/27.4|
|Distractors|73.5 (-7.0)|61.2 (-7.2)|46.3 (-7.1)|12.3/27.2|
|Random Views|67.9 (-12.6)|56.3 (-12.1)|47.8 (-5.6)|11.6/20.1|
|**Avg.**|**73.6**|**61.0**|**46.5**|**12.6/27.1**|


### **4.4. Parameter & Viewpoint Analysis** 

**Beam Appearance Optimization.** Figure 8 analyzes spatial beam design choices. (a) The performance heatmap reveals an optimal region at 3-5px thickness and 0.5-0.7 transparency, achieving 99% peak performance. This sweet spot balances visual perceptibility of directional cues, (b) The 3D surface visualization confirms this trade-off, showing performance degradation (85%) when either parameter deviates significantly from the optimal range. 

**Adaptive Viewpoint Discovery.** Figure 7 demonstrates task-specific camera positioning learned through gradient flow. (a) The polar density plot shows clear angular preferences: picking tasks concentrate at 0°-45° (overhead views, density _>_ 0.03), enabling top-down grasp planning, This autonomous specialization emerges without task labels, validating end-to-end differentiability. (b) The 3D spatial visualization illustrates visibility optimization—adaptive cameras (blue/red points) position themselves to maximize target visibility while avoiding occlusions. contrasting with fixed cameras (gray markers) that may suffer occlusion. 

### **4.5. Generalization** 

Table 4 evaluates zero-shot transfer to out-of-distribution conditions. DiffRender-VLA maintains 73.6% average success under distribution shifts, degrading only 6.9% from indomain performance. Critically, our advantage over methods widens in generalization scenarios: 12.6% over RVT-2 and 27.1% over OpenVLA (vs. 12.1%/27.1% in-domain), indicating world-aligned beam encoding provides more robust appearance-invariant spatial features. 

## **5. Conclusion** 

DiffRender-VLA bridges 3D and 2D VLA paradigms through differentiable rendering, enabling gradient flow to transfer spatial 3D perception into interpretable image representations. Our pipeline—coarse cube prediction, spatial beam markers, adaptive viewpoint generation—channels spatial understanding into image-based manipulation without requiring explicit 3D inputs or abandoning visual interpretability. By rendering axis-aligned colored beams that encode directional distances, we create visual semantics interpretable by standard vision encoders while preserving 3D geometric precision. Experiments demonstrate 80.5% simulation success and 78.3% real-world success. 

20819 

## **6. Acknowledgments** 

This work was supported by the National Natural Science Foundation of China Project (62172441, 62406347, 62172449), the Joint Funds for Railway Fundamental Research of National Natural Science Foundation of China (Grant No. U2368201), special fund of National Key Laboratory of Ni&Co Associated Minerals Resources Development and Comprehensive Utilization(GZSYSKY-2022-018, GZSYSKY-2022-024), Key Project of Shenzhen City Special Fund for Fundamental Research(JCYJ20220818103200002), the Postgraduate Innovative Project of Central South University under Grant 2023XQLH008, the National Natural Science Foundation of Hunan Province(2023JJ30696), and the High Performance Computing Center of Central South University. 

## **References** 

- [1] Jean-Baptiste Alayrac, Iain Barr, Ricardo Barreira, Mikolaj Binkowski, Sebastian Borgeaud, Andy Brock, Serkan Cabi, Jeff Donahue, Zhitao Gong, Tengda Han, Yana Hasson, Karel Lenc, Pauline Luc, Jacob L Menick, Arthur Mensch, Antoine Miech, Katherine Millican, Marianne Monteiro, Aida Nematzadeh, Malcolm Reynolds, Roman Ring, Eliza Rutherford, Sina Samangooei, Sahand Sharifzadeh, Kar´en Simonyan, Oriol Vinyals, and Andrew Zisserman. Flamingo: A visual language model for few-shot learning. _Advances in Neural Information Processing Systems 35_ , 2022. 2 

- [2] Pengju An, Yandong Guo, Xiaoqi Li, Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Senqiao Yang, Renrui Zhang, Shanghang Zhang, and Kaichen Zhou. Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation. _Advances in Neural Information Processing Systems 37_ , 2024. 2 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 2, 6, 7 

- [4] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choroma´nski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alexander Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael S. Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv (Cornell University)_ , 2023. 2, 6, 7 

- [5] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, Deli Zhao, and Hao Chen. Worldvla: Towards autoregressive action world model. _arXiv.org_ , 2025. 2 

- [6] Boyuan Chen, Zhuo Xu, Sean Kirmani, Brian Ichter, Dorsa Sadigh, Leonidas Guibas, and Fei Xia. Spatialvlm: Endowing vision-language models with spatial reasoning capabilities. _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 2 

- [7] Haonan Chen, Jingxiang Guo, Bangjun Wang, Tian-Rui Zhang, Xieyining Huang, Boren Zheng, Yiwen Hou, Chenrui Tie, Jiajun Deng, and Lin Shao. Goal-vla: Imagegenerative vlms as object-centric world models empowering zero-shot robot manipulation. _ArXiv.org_ , 2025. 2, 3 

- [8] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. _North American Chapter of the Association for Computational Linguistics_ , 2019. 2 

- [9] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence. Palm-e: An embodied multimodal language model. _arXiv (Cornell University)_ , 2023. 2 

- [10] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Chenxi Wang, Junbo Wang, Haoyi Zhu, and Cewu Lu. A comprehensive robotic dataset for learning diverse skills in one-shot. _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 5, 6 

- [11] Association for Artificial Intelligence 2026, Can Cui, Pengxiang Ding, Zirui Ge, Pengxu Hou, Siteng Huang, Lingxiao Li, Jianyi Liu, Wenxuan Song, Yifan Tang, Xinyang Tong, Wenhui Wang, Yihao Wang, Donglin Wang, Ru Zhang, Wei Zhao, and Han Zhao. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _Underline Science Inc._ , 2026. 6, 7 

- [12] Th´eophile Gervet, Xian Zhou, Nikolaos Gkanatsios, and Katerina Fragkiadaki. Act3d: 3d feature field transformers for multi-task robotic manipulation. _arXiv (Cornell University)_ , 2023. 2, 5, 6, 7 

- [13] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. Rvt: Robotic view transformer for 3d object manipulation. _arXiv (Cornell University)_ , 2023. 2, 3 

- [14] Ankit Goyal, Valts Blukis, Jie Xu, Yijie Guo, Yu-Wei Chao, and Dieter Fox. Rvt-2: Learning precise manipulation from few demonstrations. _Robotics: Science and Systems XX_ , 2024. 2, 7, 8 

- [15] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. _2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2016. 2 

- [16] Chengkai Hou, Yanjie Ze, Yankai Fu, Zeyu Gao, Songbo Hu, Yue Yu, Shanghang Zhang, and Huazhe Xu. 4d visual pretraining for robot learning. In _Proceedings of the IEEE/CVF_ 

20820 

_International Conference on Computer Vision_ , pages 8451– 8461, 2025. 6, 7 

- [17] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv (Cornell University)_ , 2023. 2 

- [18] Andrew Jaegle, Felix Gimeno, Andrew Brock, Andrew Zisserman, Oriol Vinyals, and Jo˜ao Carreira. Perceiver: General perception with iterative attention. _arXiv (Cornell University)_ , 2021. 3, 6 

- [19] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J. Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 2020. 5, 6 

- [20] Stephen James, Kentaro Wada, Tristan Laidlow, and Andrew J. Davison. Coarse-to-fine q-attention: Efficient learning for visual robotic manipulation via discretisation. _2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 2 

- [21] Tsung-Wei Ke, Nikolaos Gkanatsios, and Katerina Fragkiadaki. Policy diffusion with 3d scene representations. _arXiv (Cornell University)_ , 2024. 2, 6, 7 

- [22] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 2, 4, 6 

- [23] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 6, 7, 8 

- [24] Peiyan Li, Yixiang Chen, Hongtao Wu, Xiao Ma, Xinhai Wu, Yan Huang, Liang Wang, Tao Kong, and Tieniu Tan. Bridgevla: Input-output alignment for efficient 3d manipulation learning with vision-language models. _arXiv (Cornell University)_ , 2025. 2 

- [25] Puhao Li, Yingying Wu, Ziheng Xi, Wanlin Li, Yuzhe Huang, Zhiyuan Zhang, Yinghan Chen, Jianan Wang, SongChun Zhu, Tengyu Liu, and Siyuan Huang. Controlvla: Few-shot object-centric adaptation for pre-trained visionlanguage-action models. _ArXiv.org_ , 2025. 2 

- [26] Xiaojian Li, Sheng Wang, Chao Chen, Hailong Wei, Yudong Shi, and Hangjie Mo. Roboflamingo-plus: Fusion of depth and rgb perception with vision-language models for enhanced robotic manipulation. _2025 IEEE International Conference on Real-time Computing and Robotics (RCAR)_ , 2025. 2 

- [27] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified visionlanguage-action model with adaptive reasoning. _arXiv (Cornell University)_ , 2025. 2 

- [28] Hengyu Liu, Yifan Liu, Chenxin Li, Wuyang Li, and Yixuan Yuan. Lgs: A light-weight 4d gaussian splatting for efficient surgical scene reconstruction. _Lecture Notes in Computer Science_ , 2024. 3 

- [29] Yu Liu, Baoxiong Jia, Ruijie Lu, Junfeng Ni, Song-Chun Zhu, and Siyuan Huang. Artgs: Building interactable replicas of complex articulated objects via gaussian splatting. _arXiv (Cornell University)_ , 2025. 3 

- [30] Guanxing Lu, Shiyi Zhang, Ziwei Wang, Changliu Liu, Jiwen Lu, and Yansong Tang. Manigaussian: Dynamic gaussian splatting for multi-task robotic manipulation. _Lecture Notes in Computer Science_ , 2024. 2, 6, 7 

- [31] Guanxing Lu, Baoxiong Jia, Puhao Li, Yixin Chen, Ziwei Wang, Yansong Tang, and Siyuan Huang. Gwm: Towards scalable gaussian world models for robotic manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9263–9274, 2025. 6, 7 

- [32] Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, and Irwin King. A survey on vision-language-action models for embodied ai. _arXiv preprint arXiv:2405.14093_ , 2024. 2 

- [33] A. Mandlekar, Danfei Xu, Josiah Wong, Soroush Nasiriany, Chen Wang, Rohun Kulkarni, Li Fei-Fei, S. Savarese, Yuke Zhu, and Roberto Mart’in-Mart’in. What matters in learning from offline human demonstrations for robot manipulation. _Conference on Robot Learning_ , 2021. 4 

- [34] A. O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, L. Abraham, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, A. Rai, Anchit Gupta, Andrew Wang, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Sch¨olkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine W. Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guanzhi Wang, Hao Su, Haoshu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I. Christensen, Hiroki Furuta, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad AbouChakra, Jae-Hyung Kim, Jaimyn Drake, Jan Peters, Jochen Schneider, Jasmine Hsu, Jeannette Bohg, Jeffrey Bingham, Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, and Jialin Wu. Open x-embodiment: Robotic learning datasets and rtx models : Open x-embodiment collaboration¡sup¿0¡/sup¿. 2024. 6 

- [35] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, Po-Yao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herv´e Je´gou, Julien Mairal, Patrick Labatut, Armand Joulin, and Piotr Bojanowski. Dinov2: Learning robust visual features without supervision. _arXiv (Cornell University)_ , 2023. 6 

- [36] Mingjie Pan, Jiyao Zhang, Tianshu Wu, Yinghao Zhao, Wenlong Gao, and Hao Dong. Omnimanip: Towards general robotic manipulation via object-centric interaction primitives 

20821 

   - as spatial constraints. _2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 3 

- [37] Xincheng Pang, Wenke Xia, Zhigang Wang, Bin Zhao, Di Hu, Dong Wang, and Xuelong Li. Depth helps: Improving pre-trained rgb-based policy with depth information injection. _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2024. 2 

- [38] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 2 

- [39] M.H Shridhar, Lucas Manuelli, and Dieter Fox. Perceiveractor: A multi-task transformer for robotic manipulation. _arXiv (Cornell University)_ , 2022. 2, 3, 5, 6, 7 

- [40] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, P Kooijmans, Susana Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, M. Gonzalez Russi, Andr´es Marafioti, Simon Alibert, Matthieu Cord, Thomas Wolf, and R´emi Cad`ene. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv (Cornell University)_ , 2025. 6, 7 

- [41] Richard S Sutton, Andrew G Barto, et al. _Reinforcement learning: An introduction_ . MIT press Cambridge, 1998. 2 

- [42] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timoth´ee Lacroix, Baptiste Rozi`ere, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard<sup>´</sup> Grave, and Guillaume Lample. Llama: Open and efficient foundation language models. _arXiv (Cornell University)_ , 2023. 6 

- [43] Michael Tschannen, Alexey Gritsenko, Xiao Wang, Muhammad Ferjad Naeem, Ibrahim Alabdulmohsin, Nikhil Parthasarathy, Talfan Evans, Lucas Beyer, Ye Xia, Basil Mustafa, et al. Siglip 2: Multilingual vision-language encoders with improved semantic understanding, localization, and dense features. _arXiv preprint arXiv:2502.14786_ , 2025. 3 

- [44] Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025. 6, 7 

- [45] Zhijie Wang, Zhehua Zhou, Jiayang Song, Yuheng Huang, Zhan Shu, and Lei Ma. Vlatest: Testing and evaluating vision-language-action models for robotic manipulation. _Proceedings of the ACM on Software Engineering_ , 2025. 2 

- [46] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Se June Joo, Jianwei Yang, Baolin Peng, A. Mandlekar, Reuben Tan, YuWei Chao, Bill Yuchen Lin, Lars Lid´en, Kimin Lee, Jianfeng Gao, Luke S. Zettlemoyer, Dieter Fox, and Minjoon Seo. Latent action pretraining from videos. _International Conference on Learning Representations_ , 2024. 3 

_2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2021. 3 

   - [49] Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Zhuoguang Chen, Tao Jiang, and Hang Zhao. Depthvla: Enhancing vision-language-action models with depth-aware spatial reasoning. _arXiv preprint arXiv:2510.13375_ , 2025. 2 

   - [50] Wentao Yuan, Jiafei Duan, Valts Blukis, Wilbert Pumacay, Ranjay Krishna, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. Robopoint: A vision-language model for spatial affordance prediction for robotics. _arXiv (Cornell University)_ , 2024. 8 

   - [51] Yanjie Ze, Ge Yan, Yueh-Hua Wu, Annabella Macaluso, Yuying Ge, Jianglong Ye, Nicklas Hansen, Li Erran Li, and Xiaolong Wang. Gnfactor: Multi-task real robot learning with generalizable neural feature fields. _arXiv (Cornell University)_ , 2023. 2 

   - [52] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. _Robotics: Science and Systems XX_ , 2024. 2, 6, 7 

   - [53] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. _2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 6 

   - [54] Yunlong Zhao, Xiaoheng Deng, Zhuohua Qiu, Feng Yang, Chang Xu, Xiangjian He, Shan You, and Xiu Su. Cadgs: Modeling inter-gaussian mutual information for dynamic novel view synthesis. _Proceedings of the 33rd ACM International Conference on Multimedia_ , 2025. 3 

   - [55] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv (Cornell University)_ , 2024. 6, 7, 8 

   - [56] Yi Zhou, Connelly Barnes, Jingwan Lu, Jimei Yang, and Hao Li. On the continuity of rotation representations in neural networks. _2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2019. 4 

   - [57] Lingting Zhu, Zhao Wang, Jiahao Cui, Zhenchao Jin, Guying Lin, and Lequan Yu. Endogs: Deformable endoscopic tissues reconstruction with gaussian splatting. _Lecture Notes in Computer Science_ , 2025. 3 

   - [58] Xingxing Zuo, Pouya Samangouei, Yunwen Zhou, Yan Di, and Mingyang Li. Fmgs: Foundation model embedded 3d gaussian splatting for holistic 3d scene understanding. _International Journal of Computer Vision_ , 2024. 3 

- [47] Yang You, Jing Li, Sashank J. Reddi, Jonathan Hseu, Sanjiv Kumar, Srinadh Bhojanapalli, Xiaodan Song, James Demmel, Kurt Keutzer, and Cho-Jui Hsieh. Large batch optimization for deep learning: Training bert in 76 minutes. _arXiv (Cornell University)_ , 2019. 7 

- [48] Alex Yu, Vickie Ye, Matthew Tancik, and Angjoo Kanazawa. pixelnerf: Neural radiance fields from one or few images. 

20822 

