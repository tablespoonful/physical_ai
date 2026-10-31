---
title: "ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation"
date: "2026-05-06"
authors: "Wei Li; Jizhihui Liu; Li Yixing; Junwen Tong; Rui Shao; Liqiang Nie"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2605.05126
pdf: https://arxiv.org/pdf/2605.05126
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.05126)** / [論文ページ](https://arxiv.org/abs/2605.05126)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation** 

Wei Li<sup>1</sup> , Jizhihui Liu<sup>1</sup> , Li Yixing<sup>1</sup> , Junwen Tong<sup>2</sup> , Rui Shao<sup>1</sup><sup>_,_3*</sup> , Liqiang Nie<sup>1</sup> 1Harbin Institute of Technology, Shenzhen 2State Key Laboratory of Mobile Network and Mobile Multimedia Technology, ZTE, China 3Shenzhen Loop Area Institute 

liwei2024@stu.hit.edu.cn shaorui@hit.edu.cn 

https://github.com/JiuTian-VL/ConsisVLA-4D 

## **Abstract** 

_Current Vision-Language-Action (VLA) models primarily focus on mapping 2D observations to actions but exhibit notable limitations in spatiotemporal perception and reasoning: 1) spatial representations often rely on additional sensors, introducing substantial computational overhead; 2) visual reasoning is typically limited to future-frame prediction, lacking alignment with the instruction-grounded scene and thus compromising spatiotemporal consistency. To address these challenges, we propose_ **_ConsisVLA-4D_** _, a unified and efficient framework that enhances spatiotemporal consistency in 3D-Perception and 4D-Reasoning. Specifically, we design:_ **_1) CV-Aligner_** _, which ensures_ **_C_** _ross-_ **_V_** _iew object semantic consistency via filtering instructionrelevant regions and aligning object identities across multiple viewpoints;_ **_2) CO-Fuser_** _, which guarantees_ **_C_** _ross-_ **_O_** _bject spatial geometric consistency by eliminating spatial relation ambiguities between objects across views using compact latent representations. Building upon these, we introduce_ **_3) CS-Thinker_** _to achieve_ **_C_** _ross-_ **_S_** _cene spatiotemporal consistency as actions unfold. It learns implicit knowledge of local dynamics from object-semantic tokens of CV-Aligner and global depth from geometric tokens of CO-Fuser, thereby enhancing efficient visual reasoning under scene variations. Extensive experiments demonstrate that, benefiting from its efficient spatiotemporal consistency design, ConsisVLA-4D achieves_ **_21.6%_** _and_ **_41.5%_** _performance improvements, along with_ **_2.3_** _× and_ **_2.4_** _× inference speedups compared to OpenVLA on the LIBERO benchmark and real-world platforms, respectively._ 

## **1. Introduction** 

Vision-Language-Action (VLA) models [4, 7, 28, 29, 36, 37] have made significant progress in enabling robots to 

> *Corresponding author. 


Figure 1. **Comparison with Existing Paradigms.** Beyond conventional 2D visual inputs, **<u>Para. A</u>** employs explicit 3D/4D inputs (e.g., point clouds, depth maps, historical frames), **<u>Para. B</u>** projects 2D inputs into 3D space, and **<u>Para. C</u>** predicts 3D representations from 2D observations. In contrast, we extend the paradigm from 3D-Perception to 4D-Reasoning within a unified framework <u>(</u> **<u>Para. D</u>** <u>):</u> **1)** CV-Aligner extracts instructionrelated and cross-correlated spatial objects; **2)** CO-Fuser aggregates multi-view geometric relation; **3)** CS-Thinker infers actions based on implicit knowledge of future dynamic objects and global depth. **ConsisVLA-4D** achieves spatiotemporal consistency using only about **1/8** of the original visual inputs, enabling robust and efficient robotic manipulation, as illustrated on the right. 

perform complex tasks by integrating visual perception and language instructions. Representative works such as RT2 [6], Octo [61], OpenVLA [28], and _π_ -series [4, 15, 23, 50] highlight the potential of the VLA paradigm in bridging the gap between 2D perception and spatial manipulation, achieving impressive results across diverse benchmarks. 

6706 

However, despite these advances, current VLA models remain limited in spatiotemporal perception and reasoning. For instance, when confronted with complex object layouts or action-induced scene changes, they often struggle with these tasks, limiting their real-world effectiveness. 

The core challenges lie in two aspects. First, **3D spatial understanding** remains a significant bottleneck for VLA models. Although some methods attempt basic 2Dto-3D mapping [1, 43, 54], they fail to capture the full structural complexity of the 3D world [25, 60], often leading to object misalignment and spatial relation ambiguity. Methods [30, 59, 89] that utilize 3D representations, such as point clouds or depth maps, require additional sensors and incur substantial computational overhead, limiting their applicability in resource-constrained settings. Second, **4D spatiotemporal reasoning** remains underdeveloped [2, 8, 10, 85]. During action execution, spatial scenes evolve dynamically. Due to the lack of a comprehensive understanding of current spatial states and insufficient knowledge of evolving scene dynamics, existing methods struggle to build consistent correlations with predicted future scenes. This deficiency undermines spatiotemporal consistency, resulting in impaired visual reasoning and unstable action generation. 

In contrast, humans excel in manipulation tasks owing to their robust and efficient spatiotemporal consistency [5, 12]. Through binocular vision or movement, humans maintain accurate and consistent spatial perception (e.g., object locations and relationships) across diverse viewpoints. Simultaneously, humans perform visual reasoning (e.g., predicting future spatial states) based on this stable spatial perception, ensuring temporal stability throughout task execution. 

Motivated by human behavior and its relevance to VLA, we aim to address two key questions: **1)** How can we efficiently generate 3D representations from 2D observations without excessive computational overhead? **2)** How can we enhance spatiotemporal consistency to optimize action prediction through 4D visual reasoning? To this end, we propose **ConsisVLA-4D** , a unified and efficient framework that enhances spatiotemporal consistency in 3D-perception and 4D-reasoning, as shown in Fig. 1. Specifically, ConsisVLA4D consists of three tightly integrated and coherent core components: **1) Cross-View Aligner (CV-Aligner)** filters redundant visual representations through Explicit Semantic Object Selection, retaining only instruction-relevant objects. It then aligns object identities across viewpoints using Single-Fusion, producing efficient spatial representations ( **1/8** of the original) that ensure Cross-View object semantic consistency. **2) Cross-Object Fuser (CO-Fuser)** processes multiple viewpoints via Group-Fusion to resolve geometric ambiguities in object positions from a single view. It refines spatial relationships between objects through Implicit Geometric Relation Aggregation, yielding compact latent 

representations ( **1/12-1/8** of the original) that ensure CrossObject Spatial Geometric Consistency. **3) Cross-Scene Thinker (CS-Thinker)** learns two sets of implicit knowledge: dynamic objects in future fixed viewpoints using semantic tokens from CV-Aligner, and global depth across all viewpoints using geometric latent tokens from CO-Fuser. During inference, these pre-learned knowledge sets account for less than **10%** of the observation-instruction sequence, enabling efficient 4D visual reasoning. Through this design, ConsisVLA-4D achieves a stable and coherent understanding of dynamic scenes and maintains spatiotemporal consistency throughout action generation. 

Our contributions are summarized as follows: 

- We propose **ConsisVLA-4D** , an efficient and innovative framework that advances spatiotemporal consistency in 3D-Perception and 4D-Reasoning. 

- We introduce **CV-Aligner** and **CO-Fuser** to ensure crossview object semantic consistency and cross-object spatial geometric consistency, thereby improving the model’s understanding of complex 3D scenes. 

- We design **CS-Thinker** to enhance 4D spatiotemporal reasoning, ensuring the model generates consistent and reliable actions in dynamic environments. 

- Extensive experiments demonstrate that ConsisVLA-4D, with its advanced spatiotemporal consistency design, significantly outperforms existing methods in both performance and computational efficiency. 

## **2. Related Work** 

**VLM-based VLA Models.** Vision-Language Models (VLMs) [18, 31, 35, 42, 45, 46, 51, 52, 73, 87] and deep learning [33, 39, 40, 53, 56, 66, 67, 75–77, 81, 83] have advanced robotic manipulation by bridging visual perception with language. RT-2 [6] introduced VLA modeling with pre-trained VLMs, and RT-X [63] scaled it for better generalization. OpenVLA [28], trained on 970K robot demonstrations, released a 7B-parameter model, while OpenVLAOFT [29] optimized inference with action chunking. These single-system models [47, 58, 71, 82, 85] sparked numerous subsequent studies. In contrast, dual-system architectures, such as GR00T N1 [3], CogACT [86], _π_ 0 [4], and SmolVLA [57], separate the VLM backbone for high-level reasoning from an action expert for low-level control, fostering structured coordination. However, most models remain limited to a 2D vision-language paradigm. 

**Spatiotemporal Modeling Approaches in VLA Models.** Recent works [22, 41, 59, 70, 72, 79, 88] like 3D-VLA [88], PointVLA [30], GeoVLA [59], and Lift3D [24] leverage 3D representations, while 4D-VLA [78] and TraceVLA [89] extend this to 4D cues, incorporating historical frames and visual traces. However, these approaches rely on specialized sensors, limiting platform flexibility and increasing computational cost. Alternatively, models like Spa- 

6707 

tialVLA [54], BridgeVLA [32], Evo-0 [43] and GeoAwareVLA [1] infer 3D structures from 2D perception but suffer from projection bias, geometric inconsistencies, and occlusion errors. Thus, an efficient framework for 3D spatial perception and spatiotemporal coherence is urgently needed. 

**World Model-based VLA Models.** These models [8– 10, 21, 62, 65, 80, 90] jointly predict future visual states and actions. WorldVLA [8] unifies action and image through autoregressive prediction, while World4Omni [10] employs a pre-trained world model for task-agnostic manipulation. V-JEPA 2 [2] builds an action-conditioned latent world model from large-scale video pretraining. However, these approaches primarily predict future images rather than achieving true 3D spatial understanding or 4D reasoning. 

## **3. Preliminary & Problem Definition** 

**Semantic, Geometric, and Spatial Perception.** For efficient and comprehensive 3D scene encoding, **z**<sup>sem</sup> , **z**<sup>geo</sup> , and **z**<sup>3D</sup> are derived from visual encoders specialized in semantics, geometry, and spatial perception. 

As shown in Fig. 2, this establishes the foundation for feature selection and fusion design: **1)** SigLIP [74] employs visual and text encoders _fv_<sup>SigLIP</sup> ( _·_ ) and _ft_<sup>SigLIP</sup> ( _·_ ), aligning modalities via sample-wise matching loss, enabling each visual token **z**<sup>sem</sup><sup>_,j_</sup> in **z**<sup>sem</sup> = _fv_<sup>SigLIP</sup> ( **x** ) to inherit linguistic semantics. **2)** DINOv2 [48] aligns augmented different views of the same image using contrastive loss, allowing **z**<sup>geo</sup> = _fv_<sup>DINOv2</sup> ( **x** ) to capture geometric consistency. **3)** VGGT [64] takes _M_ RGB images ( **x** _i_ )<sup>_M_</sup> _i_ =1<sup>fromthesame</sup> 3D scene and outputs depth maps _Di_ , point maps _Pi_ , and feature grids _Gi_ (for point tracking), as expressed below: DPT _fv_<sup>VGGT</sup> ( **x** _i_ )<sup>_M_</sup> _i_ =1 = ( _Di, Pi, Gi_ )<sup>_M_</sup> _i_ =1<sup>_,_</sup> (1) � � 

where DPT( _·_ ) refers to Dense Prediction [55] head, and _fv_<sup>VGGT</sup> ( _·_ ) extracts latent features, yielding **z**<sup>3D</sup> = _fv_<sup>VGGT</sup> ( **x** ). The latent priors of _Gi_ and _Di_ in **z**<sup>3D</sup> enable it to combine with **z**<sup>sem</sup> and **z**<sup>geo</sup> for local semantic filtering and global geometric relationship modeling in 3D space. 

**Human-Aligned Spatiotemporal Consistency Modeling.** Analogous to how the human retina captures 2D images while the brain integrates spatial cues and predicts future states during manipulation, VLA models should inherit this mechanism, as shown below: 


The construction of spatially consistent 3D representations from 2D inputs serves as the foundation for spatiotemporal consistency, encompassing: **1)** the identification and matching of object identities across multiple viewpoints; **2)** the resolution of visual ambiguities through information complementarity between viewpoints. Meanwhile, VLA models should reason about dynamic spatial scenes (rather than 


Figure 2. **Efficient 3D-Perception** ensures spatial consistency through the Cross-View Aligner (red) and Cross-Object Fuser (orange). The former employs an Explicit Semantic Object Selection combined with a frame-wise Single-Fusion strategy, while the latter utilizes Implicit Geometric Relation Aggregation with a multi-frame Group-Fusion strategy to achieve Cross-View Object Semantic Consistency and Cross-Object Spatial Geometric Consistency in the spatial domain. 

merely frames), with the inferred spatial scenes enhancing temporal stability, thereby ensuring spatiotemporal consistency for robust and efficient robotic manipulation. 

## **4. ConsisVLA-4D** 

### **4.1. Proposed Framework** 

**Efficient 3D-Perception Phase.** As shown in Fig. 2 and Fig. 3 left, multi-view observations _I_ = _{M, L, R}_ (Main, Left, Right) are encoded by SigLIP into semantic representations **z**<sup>sem</sup> _M_<sup>,</sup><sup>**z**sem</sup> _R_<sup>,and</sup><sup>**z**</sup> _L_<sup>sem.Guidedbytheinstruction</sup><sup>**t**,</sup> these representations are filtered via Explicit Semantic Object Selection _f_ ES-S( _·_ ) and fused frame-wise with the 3D features extracted by VGGT through Single-Fusion _f_ SF( _·_ ), yielding instruction-relevant object representations: 


During spatial geometric feature extraction, single-view depth estimation suffers from scale ambiguity. To address this, tri-view features are integrated for depth completion at each encoder layer. In the _l_ -th block of DINOv2 and VGGT, the unified tri-view geometric feature **z**<sup>geo</sup> _l_ is fused with the cosine-decayed weighted spatial feature **z**<sup>3D</sup> _l_ via Group-Fusion _f_ GF( _·_ ), followed by Implicit Geometric Re- 

6708 


Figure 3. **The Mechanism from 3D-Perception to 4D-Reasoning.** The Cross-View Aligner selects spatial objects with matching identities across different views, and through 4D-Reasoning, further predicts the dynamic object with the same identity from one view to another after an action occurs. The Cross-Object Fuser aggregates global geometric relations to eliminate spatial ambiguity across multiple views, and through 4D-Reasoning, further predicts global depth from the same geometric representation to different views. This progression not only enhances Spatiotemporal Consistency but also reduces visual input, significantly improving training and inference efficiency. 

lation Aggregation _f_ IG-A( _·_ ) to capture spatial relations: further enhance the semantic correlation between **z**<sup>sem</sup> _i,l_<sup>ex-</sup> tracted by the SigLIP visual encoder from the _i_ -th viewpoint ( **z**<sup>geo-3D</sup> _l_ +1 _,_ **z**<sup>agg-3D</sup> _l_ +1 ) = _f_ IG-A( _f_ GF( **z**<sup>geo</sup> _l ,_ **z**<sup>3D</sup> _l_<sup>)</sup><sup>_,_</sup><sup>**z**agg-3D</sup> _l_ ) _._ (4) ( _i ∈I_ ) and **t** _∈_ R<sup>_dt_</sup> obtained from its paired text encoder: 


**Efficient 4D-Reasoning Phase.** We further extend 3DPerception to 4D-Reasoning to expand the spatial consistency into the spatiotemporal domain (Fig. 3 right and Fig. 4). On one hand, although objects with the same identity may exhibit appearance differences across different viewpoints, reasoning the object’s identity from one perspective to another is crucial for establishing cross-view identity consistency. Furthermore, we focus the reasoning on objects that change as actions unfold, resulting in: 

Subsequently, the FiLM-modulated final-layer representation **z**<sup>sem</sup> _i_ = ˜ **z**<sup>sem</sup> _i,L_<sup>is utilized to compute the semantic similar-</sup> ity _si,j_ between each visual token in **z** _i_<sup>sem</sup> and the instruction embedding **t** , which is defined as: 


where sim( _·, ·_ ) denotes cosine similarity, and **Wt** is the mapping matrix from text to viewpoint dimensions. To achieve explicit semantic object selection, we retain only the Top-K tokens most relevant to the instruction: 


On the other hand, we use the aggregated geometric relation **z**<sup>agg-3D</sup> _L_<sup>_′_</sup> to infer the depth representations of future multiview perspectives as actions unfold: 


where _Si_ represents the set of selected token indices for the _i_ -th viewpoint. The default _K_ is 32, effectively removing substantial visual redundancy. The set of tokens indexed within **z**<sup>sem</sup> _i_ is the selected object tokens **z**<sup>obj</sup> _i_<sup>:</sup> 

where **0**<sup>dyn-4D</sup> _{M,L,R}_<sup>and</sup><sup>**0**dep-4D denote initialized dynamic and</sup> depth tokens, and _L_<sup>_′_</sup> is the number of encoder layers. In comparison, **z**<sup>dyn-4D</sup> _M_ models future local dynamics through explicit object features, while **z**<sup>dep-4D</sup> _{M,L,R}_<sup>infers future global</sup> depth through implicit spatial relations. We concatenate the initialized action chunk **0**<sup>_A_</sup> at the end of the sequence and apply our proposed Spatiotemporal Consistency Attention (SC-Attn) to ultimately obtain the action output: **A** ˆ = SC-Attn( SC-Attn(( **z**<sup>obj-3D</sup> _{M,L,R}M,L,R}}_<sup>_,_</sup><sup>**z**</sup> _L_<sup>agg-3D</sup><sup>_′_</sup> _,_ **t** _,_ **0**<sup>dyn-4D</sup> _{M,L,R}M,L,R}}_<sup>_,_</sup><sup>**0**dep-4D</sup><sup>_,_</sup><sup>**0**</sup><sup>_A_)</sup><sup>_._</sup> (7) 


depth through implicit spatial relations. We concatenate the To inject 3D information into **z**<sup>obj</sup> _i_ and establish associinitialized action chunk **0**<sup>_A_</sup> at the end of the sequence and ations between objects with the same identity across difapply our proposed Spatiotemporal Consistency Attention ferent viewpoints, we introduce Single-Fusion, which per(SC-Attn) to ultimately obtain the action output: forms frame-wise integration of **z**<sup>3D</sup> _i_ extracted from VGGT. **A** ˆ = SC-Attn( SC-Attn(( **z**<sup>obj-3D</sup> _{M,L,R}M,L,R}}_<sup>_,_</sup><sup>**z**</sup> _L_<sup>agg-3D</sup><sup>_′_</sup> _,_ **t** _,_ **0**<sup>dyn-4D</sup> _{M,L,R}M,L,R}}_<sup>_,_</sup><sup>**0**dep-4D</sup><sup>_,_</sup><sup>**0**</sup><sup>_A_)</sup><sup>_._</sup> (7) We append _N_ transformer layers, where **z**<sup>obj</sup> _i_ serves as the query (Q), and **z**<sup>3D</sup> _i_ serves as both the key (K) and value (V). **4.2. Cross-View Object Semantic Consistency** The output of the final layer is taken as **z**<sup>obj-3D</sup> _i_ : In the Explicit Semantic Object Selection (ES-Selection) **z**<sup>obj-3D</sup> _i_ = �FFN(Cross-Attn( **z**<sup>obj</sup> _i_<sup>_,_</sup><sup>**z**</sup> _i_<sup>3D)) + Res(</sup><sup>**z**obj</sup> _i_<sup>)</sup> ���Layer=1,. . . ,N (13) module, layer-wise FiLM [49] modulation is applied to = _f_ SF( **z**<sup>obj</sup> _i_<sup>_,_</sup><sup>**z**</sup> _i_<sup>3D)</sup><sup>_,_</sup> 

6709 

where Res( _·_ ) denotes the residual connection. This leverages VGGT’s pre-trained ability of point tracking ( _Gi_ ) from the _i_ -th viewpoint and achieves cross-view object semantic consistency using only **1/8** of the original visual tokens. 

### **4.3. Cross-Object Spatial Geometric Consistency** 

Due to geometric ambiguity in object positions from a single viewpoint, we jointly process multiple viewpoints (M, L, and R) to abstract the spatial geometric relationships between them. We achieve concise spatial geometric relation aggregation through in-depth feature fusion within the encoder of DINOv2 and VGGT, performed block by block. For the _l_ -th block, the weighted 3D representation **z**<sup>3D</sup> _l_ is aggregated element-wise with the weight _αl_ as follows: **z**<sup>geo-3D</sup> _l_ = (1 _− αl_ ) _⊙_ **z**<sup>geo</sup> _l_ + _αl ⊙_ **z**<sup>3D</sup> _l_ = _f_ GF( **z**<sup>geo</sup> _l ,_ **z**<sup>3D</sup> _l_<sup>)</sup><sup>_._(14)</sup> 

The value of _αl_ is controlled by the layer number _l_ , decreasing cosinusoidally with increasing layer depth to maintain a deep yet stable adjustment. The formula is given by: 


At the 0-th layer, the maximum weight is achieved, _α_ 0 = _ψ_ , and at the maximum layer _L_<sup>_′_</sup> , the minimum weight is _αL_<sup>_′_</sup> = = _δ_ . After concatenating the learnable **z**<sup>agg-3D</sup> _l_ (with **z**<sup>agg-3D</sup> _l_ +1 **z**<sup>agg</sup> _l_ at _l_ = 0), the combined result is input to the Implicit Geometric Relation Aggregation (IG-Aggregation): 


where _⊕_ denotes the concatenation of two token sets, and BC-Attn( _·_ ) represents block-wise causal self-attention, where causal attention is applied between **z**<sup>geo-3D</sup> _l_ and **z**<sup>agg-3D</sup> _l_ , and bidirectional attention is applied within each. Finally, we use only the final layer output, **z**<sup>agg-3D</sup> _L_<sup>_′_</sup> . This implicit modeling avoids redundancy with semantic tokens and efficiently aggregates spatial geometric information to maintain cross-object spatial geometric consistency, using only **1/12-1/8** of the original visual tokens. 

### **4.4. Cross-Scene Spatiotemporal Consistency** 

As actions unfold, spatial scenes continuously change, extending the requirement of spatial consistency within a single scene to spatiotemporal consistency across scenes. The introduction of the temporal dimension also transforms the perception stage into a reasoning phase toward future states. 

To this end, we design the Cross-Scene Thinker (as shown in Fig. 4) with Spatiotemporal Consistency Attention (SC-Attn), which **1)** learns implicit semantic and geometric knowledge during training to enable efficient visual reasoning at inference, and **2)** extends both semantic and geometric consistency into the spatiotemporal domain, thereby enhancing the temporal stability of 3D perception. 


Figure 4. **Efficient 4D-Reasoning.** IK (implicit knowledge). Cross-Scene Thinker with Spatiotemporal Consistency Attention (SC-Attn) ensures: **1)** Three sets of initialized dynamic tokens decode dynamic object representations for one view (CoTracker [26, 27] supervision), guided by object features from different views; **2)** One set of initialized depth tokens decodes global depth for three views (Depth-Anything [68, 69] supervision), guided by multi-view geometric relations; **3)** These predictions serve as intermediate visual reasoning for parallel action decoding. 

**Multi-View Objects to Single-View Dynamic Objects.** For each viewpoint _i ∈I_ , a corresponding learnable token set **0**<sup>dyn-4D</sup> _i_ is initialized, forming _|I|_ groups in total. In the SC-Attn module, each dynamic token **0**<sup>dyn-4D</sup> _i_ is independently guided by its corresponding object representation **z**<sup>obj-3D</sup> _i_ and the instruction embedding **t** : 


To enhance spatiotemporal consistency of object dynamics across scenes, the model predicts the dynamic object ˆ **z**<sup>dyn-4D</sup> _i_<sup>_∗_</sup> corresponding to a fixed viewpoint _i_<sup>_∗_</sup> _∈I_ after the action occurs. The dynamic-object loss is formulated as: 

_L_ dyn-4D = ��(ˆ **z** _i_ dyn-4D<sup>_∗_</sup> _⊙_ **m**<sup>obj-3D</sup> _i_<sup>_∗_</sup> ) _−_ ( **z**<sup>dyn-4D</sup> _i_<sup>_∗_</sup> _⊙_ **m**<sup>obj-3D</sup> _i_<sup>_∗_</sup> )��22<sup>_,_(18)</sup> where _⊙_ denotes element-wise multiplication, and **m**<sup>obj-3D</sup> _i_<sup>_∗_</sup> is the mask that localizes the object position in **z**<sup>obj-3D</sup> _i_<sup>_∗_</sup> . 

**Abstract Relation to Concrete Global Depths. z**<sup>agg-3D</sup> _L_<sup>_′_</sup> aggregates implicit abstract geometric relations across multiple views. In the SC-Attn module, we initialize a set of learnable tokens **0**<sup>dep-4D</sup> and these tokens are guided jointly 

6710 

Table 1. **Simulation Results on LIBERO Benchmark.** Task success rates across four suites and their overall average. 

|**Method**|**Spatial **|**Object **|**Goal **|**Long**|**Avg.**|
|---|---|---|---|---|---|
|Diffusion Policy_[RSS’23]_[14]|78.3|92.5|68.3|50.5|72.4|
|Octo_[RSS’24]_[61]|78.9|85.7|84.6|51.1|75.1|
|OpenVLA_[CoRL’24]_[28]|84.7|88.4|79.2|83.7|76.5|
|OpenVLA-OFT_[RSS’25]_[29]|97.6|98.4|97.9|94.5|97.1|
|_π_0 _[RSS’25]_[4]|96.8|98.8|95.8|85.2|94.2|
|_π_0-Fast_[RSS’25]_[50]|96.4|96.8|88.6|60.2|85.5|
|_π_0_._5 _[arXiv’25]_[23]|98.8|98.2|98.0|92.4|96.9|
|TraceVLA_[ICLR’25]_[89]|84.6|85.2|75.1|54.1|74.8|
|CoT-VLA_[CVPR’25]_[85]|87.5|91.6|87.6|69.0|83.9|
|SpatialVLA_[RSS’25]_[54]|88.2|89.9|78.6|55.5|78.1|
|ConsisVLA-4D|**98.8**|**99.8**|**98.0**|**95.6**|**98.1**|


Table 2. **Simulation Results on ManiSkill2 Benchmark.** “†” denotes results reproduced under identical settings as ConsisVLA4D. The results are averaged over 20 or 100 trials. 

|**Method**|**PickC.**|**StackC.**|**PushC.**|**Avg.**|
|---|---|---|---|---|
|Octo_[RSS’24]_[61]|86/100|76/100|-|81.0%|
|OpenVLA_[CoRL’24]_† [28]|67/100|64/100|71/100|67.3%|
|CogACT_[arXiv’24]_[34]|19/20|18/20|-|92.5%|
|GeoVLA_[arXiv’25]_[59]|18/20|18/20|-|90.0%|
|Dita_[ICCV’25]_[20]|79/100|80/100|-|79.5%|
|OpenVLA-OFT_[RSS’25]_† [29]|85/100|93/100|88/100|88.7%|
|ConsisVLA-4D|**93/100**|**95/100**|**95/100**|**94.3%**|


by **z**<sup>agg-3D</sup> _L_<sup>_′_</sup> and the instruction embedding **t** , while remaining isolated from the learning processes of **z**<sup>obj-3D</sup> _I_ and **0**<sup>dyn-4D</sup> _I_ : 


Given the spatial ambiguities inherent to single-view perception, the aggregated cross-view geometric relations are decoded into global depth features **z** ˆ<sup>dep-4D</sup> _I_ for each viewpoint. The global-depth loss is defined as: 


During training, CS-Thinker learns the complete processes from Eq. 17 to Eq. 20 to enhance spatiotemporal consistency understanding. During inference, it operates without explicitly generating dynamic objects or global depth, relying instead on the learned implicit semantic and geometric knowledge for efficient and stable action generation. 

**Parallel Decoding of Action Chunks in SC-Attn.** The predictions of **z** ˆ<sup>dyn-4D</sup> _i_<sup>_∗_</sup> and **z** ˆ<sup>dep-4D</sup> _I_ occur within the same contextual window as action prediction, serving as comprehensive intermediate visual reasoning for action generation. During this process, the initialized action tokens **0**<sup>_A_</sup> are decoded in parallel to yield **A**<sup>ˆ</sup> , optimized using the L1 loss _L_ action. The overall training objective is formulated as: 


Table 3. **Efficiency Optimization Results.** “†” denotes results reproduced under identical settings as ConsisVLA-4D. _Latency_ and _Throughput (T-put)_ represent the inference delay and the number of predicted actions per second, while _Cost_ indicates the time required for every 10k training steps. The results show that despite the addition of 3D representation input and 4D reasoning processes, ConsisVLA-4D outperforms the most efficient 7B VLA model (OpenVLA-OFT). Ablation on E3D (Efficient 3DPerception phase) validates its contribution to overall efficiency. 

|**Method**|**Latency** _↓_|**T-put** _↑_|**FLOPs** _↓_|**Cost** _↓_|
|---|---|---|---|---|
|_Simulation_<br>|_: Unimanual_<br>|_tasks_<br>|||
|RT-2-X_[PMLR’23]_[6]|0.200 s|5.0 Hz|-|-|
|ManipLLM_[CVPR’24]_[38]|-|2.2 Hz|-|-|
|CogACT_[arXiv’24]_[34]|-|9.8 Hz|-|-|
|OpenVLA_[CoRL’24]_† [28]|0.254 s|3.9 Hz|8.48 T|11.7 h|
|TraceVLA_[ICLR’25]_[89]|0.192 s|5.2 Hz|-|-|
|SpatialVLA_[RSS’25]_[54]|0.199 s|20.1 Hz|-|-|
|OpenVLA-OFT_[RSS’25]_† [29]|0.137 s|58.4 Hz|8.45 T|12.3 h|
|FiS-VLA_[NeurIPS’25]_[29]|-|21.9 Hz|-|-|
|ConsisVLA-4D|**0.110 s**|**72.7 Hz**|**4.59 T**|**8.6 h**|
|w/o E3D|0.204 s|39.2 Hz|16.83 T|22.3 h|
|_Real Worl_|_d: Bimanual_|_tasks_|||
|OpenVLA_[CoRL’24]_† [28]|0.552 s|1.8 Hz|16.30 T|12.8 h|
|OpenVLA-OFT_[RSS’25]_† [29]|0.334 s|74.8 Hz|14.95 T|13.7 h|
|ConsisVLA-4D|**0.231 s**|**108.2 Hz**|**9.68 T**|**10.1 h**|
|w/o E3D|0.398 s|62.8 Hz|25.70 T|22.0 h|


## **5. Experiments** 

### **5.1. Experimental Setup** 

**Implementation Details.** Training uses 4× A800 GPUs, and real-world inference runs on a single RTX 5090. 

**Simulation Benchmark.** We conduct evaluations across multiple simulation benchmarks, including: **1)** the four task suites of LIBERO [44]—Spatial, Object, Goal, and Long; **2)** three pick-and-place tasks emphasizing spatial scene perception in ManiSkill2 [19]; and **3)** diverse ALOHAbased [16] bimanual tasks within RoboTwin 2.0 [13]. 

**Real-World Platforms and Tasks.** ConsisVLA-4D is deployed on both the AgileX Cobot Magic [16] and Galaxea R1 Lite [17] platforms for real-world evaluations, covering four categories of long-horizon tasks: **1)** Microwave Operation, **2)** Banana Peeling, **3)** Drawer Arrangement, and **4)** T-shirt Folding. Each task includes 60, 60, 60, and 45 human-teleoperated demonstrations across both platforms. 

**Baselines.** In simulation, ConsisVLA-4D is compared with multiple SOTA methods, including OpenVLA [28], SpatialVLA [54], _π_ 0 [4], CoT-VLA [85], and OpenVLAOFT [29]. In real-world, we reproduce three representative models, including OpenVLA (base model), and OpenVLAOFT (the best 7B baseline in performance and efficiency), with training and deployment settings identical. For efficiency, we conduct fair comparisons between these three baselines with ConsisVLA-4D on the LIBERO and Galaxea R1 Lite platforms. 

6711 


Figure 5. **Simulation Results on RoboTwin 2.0 Benchmark.** The tasks cover diverse scenarios, with each task conducted in 100 trials. Table 4. **Real-World Task Results.** “†” denotes results reproduced under identical settings as ConsisVLA-4D. The table reports subtask (progressive stage) success rates for four long-horizon tasks on the Galaxea R1 Lite and AgileX Cobot Magic platforms. Decimal values indicate averages over 15 trials, and the average success rate reflects complete task completion. 

|**Method**|**Micro**<br>**Put**|**wave Ope**<br>**+Place**|**ration**<br>**+Close**|**Ba**<br>**Pick**|**nana Pee**<br>**+Peel**|**ling**<br>**+Place**|**Draw**<br>**Pull**|**er Arran**<br>**+Place**|**gement**<br>**+Push**|**T**<br>**Step 1**|**-shirt Fold**<br>**+Step 2**|**ing**<br>**+Step 3**|**Avg.**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||_Galaxea_|_R1 Litepl_|_atform_|||||||
|OpenVLA† [28]|6.7/10|5.3/10|4.7/10|8.0/10|0.7/10|0.7/10|5.3/10|3.3/10|2.0/10|4.7/10|4.0/10|4.0/10|28.5%|
|SpatialVLA† [54]|6.0/10|5.3/10|4.7/10|-|-|-|6.0/10|3.3/10|2.7/10|-|-|-|36.7%|
|OpenVLA-OFT† [29]|8.0/10|6.7/10|6.7/10|9.3/10|4.0/10|3.3/10|7.3/10|6.7/10|6.0/10|6.7/10|6.0/10|4.7/10|51.8%|
|ConsisVLA-4D|**9.3/10**|**8.7/10**|**8.0/10**|**10/10**|**6.0/10**|**6.0/10**|**8.7/10**|**8.0/10**|**6.7/10**|**9.3/10**|**8.7/10**|**7.3/10**|**70.0%**|
||||||_AgileX Co_|_bot Magic_|_platform_|||||||
|OpenVLA† [28]|6.0/10|5.3/10|4.7/10|8.0/10|1.3/10|0.7/10|5.3/10|3.3/10|2.7/10|4.7/10|4.7/10|4.0/10|30.0%|
|OpenVLA-OFT† [29]|8.0/10|6.7/10|6.0/10|9.3/10|3.3/10|2.7/10|7.3/10|6.7/10|6.7/10|6.7/10|5.3/10|4.7/10|50.3%|
|ConsisVLA-4D|**9.3/10**|**8.7/10**|**8.0/10**|**9.3/10**|**6.0/10**|**6.0/10**|**8.7/10**|**7.3/10**|**6.0/10**|**9.3/10**|**8.7/10**|**7.3/10**|**68.3%**|


Table 5. **Ablation Study on CV-Aligner and CO-Fuser.** Ablation components include ES-Selection, Single-Fusion from CVAligner, and Group-Fusion, IG-Aggregation from CO-Fuser. 

|**CV-Al**|**igner**|**CO-**|**Fuser**|**LIBERO SR**_↑_|**Real-World SR**_↑_|
|---|---|---|---|---|---|
|ES-Sel.|S-Fus.|G-Fus.|IG-Agg.|Four Suites|Two Tasks|
||✓|✓|✓|93.9(-4.2)|71.7(-6.6)|
|✓||✓|✓|95.5(-2.6)|73.3(-5.0)|
|✓|✓||✓|95.6(-2.5)|70.0(-8.3)|
|✓|✓|✓||91.7(-6.4)|68.3(-10.0)|
|✓|✓|✓|✓|**98.1**|**78.3**|


### **5.2. Overall Performance & Efficiency** 

**Simulation Performance. 1)** As illustrated in Tab. 1, ConsisVLA-4D outperforms all methods across the four LIBERO suites. Particularly, it achieves exceptional success rates of **98.8%** and **99.8%** in the Spatial and Object suites, which assess spatial perception and object recognition, respectively. The average success rate exceeds that of comparative methods SpatialVLA (specialized in spatial modeling) and CoT-VLA (specialized in visual reasoning) by **20%** and **14.2%** , highlighting the advantages of our 3D spatial representation and 4D visual reasoning. **2)** As shown in Tab. 2 and Fig. 5, ConsisVLA-4D demonstrates stable superiority across the three classic tasks in ManiSkill2 (PickCube, StackCube, PushCube) and seven diverse tasks in RoboTwin 2.0, testing fine spatial perception and robust bimanual manipulation, respectively. 

**Simulation Efficiency.** As illustrated in Tab. 3, despite adding approximately 2B parameters (mainly from VGGT), ConsisVLA-4D achieves **2.31** _×_ and **1.25** _×_ speedups in inference latency and **1.36** _×_ and **1.43** _×_ speedups in training cost compared to the base 7B baseline (OpenVLA) and the most efficient 7B baseline (OpenVLA-OFT), respectively. 

**Real-World Performance.** As shown in Tab. 4, 15-trial results are normalized to a 10-trial equivalent for intuitiveness. ConsisVLA-4D leads significantly in both phased and final success rates across 4 diverse long-horizon bimanual tasks, with strong performance stably maintained across deployment platforms ( **±1.7%** ). Enhanced spatiotemporal consistency gives ConsisVLA-4D greater advantages in these 4 real-world tasks, where spatial understanding and scenario variations are more emphasized. Notably, its realworld results are nearly consistent with those on RoboTwin 2.0 (ALOHA manipulator), demonstrating robust sim-toreal transfer capability. 

**Real-World Efficiency.** Compared to simulation, the real-world setup adds a new viewpoint input, increases the action chunk size from 8 to 25, and reduces the training batch size from 64 to 32. As shown in Tab. 3, ConsisVLA4D maintains similar efficiency gains in inference latency and training cost as in simulation. The significant throughput improvement by **33.4** Hz enables real-time, smooth operation of large VLA models on real hardware. When **E3D** is ablated, the large spatial information representation leads to a significant drop in model efficiency. 

### **5.3. Ablation Studies** 

We conduct ablation experiments in simulation (LIBERO) and real-world (Galaxea R1 Lite). Two tasks (Microwave Operation, T-shirt Folding) are selected, with 15 trials per task extended to 30 to ensure stable ablation results. 

**CV-Aligner and CO-Fuser.** As shown in Tab. 5, for both simulation and real-world results: **1)** Removing ES-Sel. and S-Fus. from CV-Aligner prevents the filtering of redundant visual inputs and fails to align object identities across different viewpoints, leading to success rate drops of **7.0%** and 

6712 


Figure 6. Visualization of ConsisVLA-4D performing four long-horizon real-world manipulation tasks on the Galaxea R1 Lite platform, illustrating key execution-stage observations. Red circles highlight fine-grained gripper operations, including _grasping bowl edge_ , _peeling banana_ , _holding drawer handle_ , and _pinching cloth corner_ . 


Figure 7. Visualization of **1)** LIBERO observation examples, where _M_ and _W_ denote main and wrist views; **2)** instruction-relevant object tokens extracted by CV-Aligner, identifying objects such as bowl on/next to the cookie box, bowl in the top drawer of the wooden cabinet, stove, and plate; and **3)** aggregated spatial geometry tokens from CO-Fuser capturing geometric relations across multiple views. 

Table 6. **Ablation Study on CS-Thinker.** Dyn. O. and Glob. D. represent the training-only dynamic objects and global depth representations in 4D-Reasoning, respectively. 

|**Dyn. O. **|**Glob. D.**|**Attention**|**LIBERO SR**_↑_|**Real-World SR**_↑_|
|---|---|---|---|---|
|||SC-Attn|93.3(-4.8)|66.7(-11.6)|
||✓|SC-Attn|95.4(-2.7)|73.3(-5.0)|
|✓||SC-Attn|94.7(-3.4)|71.6(-6.7)|
|✓|✓|Causal|90.9(-7.2)|66.7(-11.6)|
|✓|✓|Bidirectional|92.2(-5.9)|68.3(-10.0)|
|✓|✓|SC-Attn|**98.1**|**78.3**|


Table 7. **Ablation Study on sparsification ratio (Spf.Ratio).** “†” denotes reproduced results of FastV and SliME. **0**<sup>4D</sup> represents the sum of **0**<sup>dyn-4D</sup> _I_ and **0**<sup>dep-4D</sup> token counts. 

|**Spf.Ratio**|**z**<sup>obj-3D</sup><br>_I_|**z**<sup>agg-3D</sup><br>_L_<sup>_′_</sup>|**0**<sup>4D</sup>|**LIBERO SR**_↑_|**Real-World SR**_↑_|
|---|---|---|---|---|---|
|_≈_1/4|128|128|30|98.0(-0.1)|80.0(+0.7)|
|_≈_1/8|64|64|18|**98.1**|**78.3**|
|_≈_1/16|32|32|12|94.9(-3.2)|68.3(-10.0)|
|_≈_1/8||FastV† [11]||88.8(-9.3)|50.0(-28.3)|
|_≈_1/8||SliME† [84]||85.6(-12.5)|46.7(-31.6)|


**10.0%** . **2)** Removing G-Fus. and IG-Agg. from CO-Fuser causes visual ambiguities in spatial relationships between objects, resulting in success rate drops of **8.2%** and **13.3%** . These results demonstrate that the consistency modeling of each module plays a crucial role in ensuring the model’s efficient understanding of complex 3D scenes. Moreover, all modules are adaptively designed, and swapping them with counterparts in SigLIP and DINOv2 degrades performance. 

**CS-Thinker.** As shown in Tab. 6, removing Dyn. O. and Glob. D. from SC-Attn causes success rate drops of **2.7%4.8%** in simulation and **5.7%-11.6%** in the real world. These results highlight the importance of local object and global depth in 4D-Reasoning and action prediction. Moreover, comparison with causal and bidirectional attention shows that SC-Attn’s targeted modulation enhances the role of each visual element in spatiotemporal consistency modeling, thus improving action execution success rates. **Sparsification Ratio.** Tab. 7 presents results under varying sparsification ratios _R ∈{_ 1 _/_ 4 _,_ 1 _/_ 8 _,_ 1 _/_ 16 _}_ . The _R_ = 1 _/_ 8 setting achieves a favorable balance between performance and efficiency. Furthermore, compared to other general sparsification methods, such as FastV [11] and 

SliME [84], at the same 8× compression level, ConsisVLA4D demonstrates significant advantages. 

### **5.4. Qualitative Analysis** 

Fig. 6 illustrates the model’s ability to execute manipulation tasks smoothly and accurately across four long-horizon real-world scenarios. Fig. 7 visualizes: **1)** selected local object tokens from patch tokens at different viewpoints; and **2)** the correlation of a global spatial relation aggregation token with all patch tokens across viewpoints. Based on this correlation, ConsisVLA-4D achieves state-of-the-art performance with only 1 **/8** of the visual tokens (see Tab. 7). 

## **6. Conclusion** 

ConsisVLA-4D advances spatiotemporal reasoning for robotic manipulation by unifying efficient 3D perception and 4D visual reasoning. Through the integration of CVAligner, CO-Fuser, and CS-Thinker, it achieves cross-view, cross-object, and cross-scene consistency, enabling robust and efficient understanding of dynamic environments. Experiments demonstrate substantial improvements in both performance and efficiency over prior VLAs. We expect this work to provide useful insights for embodied research. 

6713 

## **Acknowledgement** 

This study is supported by National Natural Science Foundation of China (Grant No. 62306090) , Natural Science Foundation of Guangdong Province of China (Grant No. 2024A1515010147) , Natural Science Foundation of Shenzhen City of China (Grant No. JCYJ20250604145700001), Shenzhen Science and Technology Program (KQTD20240729102207002) and Beijing Natural Science Foundation (L254018). 

## **References** 

- [1] Ali Abouzeid, Malak Mansour, Zezhou Sun, and Dezhen Song. Geoaware-vla: Implicit geometry aware visionlanguage-action model. _arXiv preprint arXiv:2509.14117_ , 2025. 2, 3 

- [2] Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, et al. V-jepa 2: Selfsupervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 2, 3 

- [3] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 2 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-languageaction flow model for general robot control, 2024. _URL https://arxiv. org/abs/2410.24164_ , 2024. 1, 2, 6 

- [5] Randolph Blake and Hugh Wilson. Binocular vision. _Vision research_ , 51(7):754–770, 2011. 2 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 1, 2, 6 

- [7] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 1 

- [8] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 2, 3 

- [9] Delong Chen, Mustafa Shukor, Theo Moutakanni, Willy Chung, Jade Yu, Tejaswi Kasarla, Yejin Bang, Allen Bolourchi, Yann LeCun, and Pascale Fung. Vl-jepa: Joint embedding predictive architecture for vision-language. _arXiv preprint arXiv:2512.10942_ , 2025. 

- [10] Haonan Chen, Bangjun Wang, Jingxiang Guo, Tianrui Zhang, Yiwen Hou, Xuchuan Huang, Chenrui Tie, and Lin Shao. World4omni: A zero-shot framework from image gen- 

eration world model to robotic manipulation. _arXiv preprint arXiv:2506.23919_ , 2025. 2, 3 

- [11] Liang Chen, Haozhe Zhao, Tianyu Liu, Shuai Bai, Junyang Lin, Chang Zhou, and Baobao Chang. An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large vision-language models. In _European Conference on Computer Vision_ , pages 19–35. Springer, 2024. 8 

- [12] Shijie Chen, Ning Cheng, Xiaojing Chen, and Cheng Wang. Integration and competition between space and time in the hippocampus. _Neuron_ , 112(21):3651–3664, 2024. 2 

- [13] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 6 

- [14] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 2023. 6 

- [15] Danny Driess, Jost Tobias Springenberg, Brian Ichter, Lili Yu, Adrian Li-Bell, Karl Pertsch, Allen Z Ren, Homer Walke, Quan Vuong, Lucy Xiaoyang Shi, et al. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. _arXiv preprint arXiv:2505.23705_ , 2025. 1 

- [16] Zipeng Fu, Tony Z. Zhao, and Chelsea Finn. Mobile aloha: Learning bimanual mobile manipulation with lowcost whole-body teleoperation. In _Conference on Robot Learning (CoRL)_ , 2024. 6 

- [17] Galaxea. Galaxea r1 lite. _https://galaxea-dynamics.com/_ , 2025. 6 

- [18] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models. _arXiv preprint arXiv:2407.21783_ , 2024. 2 

- [19] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, et al. Maniskill2: A unified benchmark for generalizable manipulation skills. _arXiv preprint arXiv:2302.04659_ , 2023. 6 

- [20] Zhi Hou, Tianyi Zhang, Yuwen Xiong, Haonan Duan, Hengjun Pu, Ronglei Tong, Chengyang Zhao, Xizhou Zhu, Yu Qiao, Jifeng Dai, et al. Dita: Scaling diffusion transformer for generalist vision-language-action policy. _arXiv preprint arXiv:2503.19757_ , 2025. 6 

- [21] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. _arXiv preprint arXiv:2412.14803_ , 2024. 3 

- [22] Jiangyong Huang, Silong Yong, Xiaojian Ma, Xiongkun Linghu, Puhao Li, Yan Wang, Qing Li, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. An embodied generalist agent in 3d world. _arXiv preprint arXiv:2311.12871_ , 2023. 2 

6714 

- [23] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 1, 6 

- [24] Yueru Jia, Jiaming Liu, Sixiang Chen, Chenyang Gu, Zhilue Wang, Longzan Luo, Lily Lee, Pengwei Wang, Zhongyuan Wang, Renrui Zhang, et al. Lift3d foundation policy: Lifting 2d large-scale pretrained models for robust 3d robotic manipulation. _arXiv preprint arXiv:2411.18623_ , 2024. 2 

- [25] Guangan Jiang, Tianzi Zhang, Dong Li, Zhenjun Zhao, Haoang Li, Mingrui Li, and Hongyu Wang. Stg-avatar: Animatable human avatars via spacetime gaussian. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 20058–20065. IEEE, 2025. 2 

- [26] Nikita Karaev, Iurii Makarov, Jianyuan Wang, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker3: Simpler and better point tracking by pseudolabelling real videos. In _Proc. arXiv:2410.11831_ , 2024. 5 

- [27] Nikita Karaev, Ignacio Rocco, Benjamin Graham, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker: It is better to track together. In _European conference on computer vision_ , pages 18–35. Springer, 2024. 5 

- [28] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 6, 7 

- [29] Moo Jin Kim, Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 1, 2, 6, 7 

- [30] Chengmeng Li, Junjie Wen, Yan Peng, Yaxin Peng, Feifei Feng, and Yichen Zhu. Pointvla: Injecting the 3d world into vision-language-action models. _arXiv preprint arXiv:2503.07511_ , 2025. 2 

- [31] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _International conference on machine learning_ , pages 19730– 19742. PMLR, 2023. 2 

- [32] Peiyan Li, Yixiang Chen, Hongtao Wu, Xiao Ma, Xiangnan Wu, Yan Huang, Liang Wang, Tao Kong, and Tieniu Tan. Bridgevla: Input-output alignment for efficient 3d manipulation learning with vision-language models. _arXiv preprint arXiv:2506.07961_ , 2025. 3 

- [33] Peizheng Li, Zhenghao Zhang, David Holtz, Hang Yu, Yutong Yang, Yuzhi Lai, Rui Song, Andreas Geiger, and Andreas Zell. Spacedrive: Infusing spatial awareness into vlm-based autonomous driving. _arXiv preprint arXiv:2512.10719_ , 2, 2025. 2 

- [34] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 6 

- [35] Wei Li, Bing Hu, Rui Shao, Leyang Shen, and Liqiang Nie. Lion-fs: Fast & slow video-language thinker as online video assistant. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 3240–3251, 2025. 2 

- [36] Wei Li, Renshan Zhang, Rui Shao, Zhijian Fang, Kaiwen Zhou, Zhuotao Tian, and Liqiang Nie. Semanticvla: Semantic-aligned sparsification and enhancement for efficient robotic manipulation. _arXiv preprint arXiv:2511.10518_ , 2025. 1 

- [37] Wei Li, Renshan Zhang, Rui Shao, Jie He, and Liqiang Nie. Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification. _arXiv preprint arXiv:2508.21046_ , 2025. 1 

- [38] Xiaoqi Li, Mingxu Zhang, Yiran Geng, Haoran Geng, Yuxing Long, Yan Shen, Renrui Zhang, Jiaming Liu, and Hao Dong. Manipllm: Embodied multimodal large language model for object-centric robotic manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18061–18070, 2024. 6 

- [39] Bangyan Liao, Zhenjun Zhao, Lu Chen, Haoang Li, Daniel Cremers, and Peidong Liu. Globalpointer: Large-scale plane adjustment with bi-convex relaxation. In _European Conference on Computer Vision_ , pages 360–376. Springer, 2024. 2 

- [40] Bangyan Liao, Zhenjun Zhao, Haoang Li, Yi Zhou, Yingping Zeng, Hao Li, and Peidong Liu. Convex relaxation for robust vanishing point estimation in manhattan world. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 15823–15832, 2025. 2 

- [41] Jiakai Lin, Jinchang Zhang, Ge Jin, Wenzhan Song, Tianming Liu, and Guoyu Lu. 3d plant root skeleton detection and extraction. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3011–3017. IEEE, 2025. 2 

- [42] Jiakai Lin, Jinchang Zhang, and Guoyu Lu. Keypoint detection and description for raw bayer images. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11736–11742. IEEE, 2025. 2 

- [43] Tao Lin, Gen Li, Yilei Zhong, Yanwen Zou, Yuxin Du, Jiting Liu, Encheng Gu, and Bo Zhao. Evo-0: Vision-languageaction model with implicit spatial understanding. _arXiv preprint arXiv:2507.00416_ , 2025. 2, 3 

- [44] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 6 

- [45] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 2 

- [46] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 26296–26306, 2024. 2 

- [47] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffu- 

6715 

sion and autoregression in a unified vision-language-action model. _arXiv preprint arXiv:2503.10631_ , 2025. 2 

- [48] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 3 

- [49] Ethan Perez, Florian Strub, Harm De Vries, Vincent Dumoulin, and Aaron Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , 2018. 4 

- [50] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 1, 6 

- [51] Xiaozhen Qiao, Peng Huang, Jiakang Yuan, Xianda Guo, Bowen Ye, Chaocan Xue, Ye Zheng, Zhe Sun, and Xuelong Li. Bidirectional prototype-reward co-evolution for testtime adaptation of vision-language models. _arXiv preprint arXiv:2503.09394_ , 2025. 2 

- [52] Xiaozhen Qiao, Jingkai Zhao, Yuqiu Jiang, Xianda Guo, Zhe Sun, Hongyuan Zhang, and Xuelong Li. Classaware prototype learning with negative contrast for testtime adaptation of vision-language models. _arXiv preprint arXiv:2510.19802_ , 2025. 2 

- [53] Xinchi Qiu, Lei Yu, Yuchen Zhang, Aobo Yang, Narine Kokhlikyan, Nicola Cancedda, Diego Garcia-Olano, et al. Hallucination reduction with casal: Contrastive activation steering for amortized learning. _arXiv preprint arXiv:2510.02324_ , 2025. 2 

- [54] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 2, 3, 6, 7 

- [55] Ren´e Ranftl, Alexey Bochkovskiy, and Vladlen Koltun. Vision transformers for dense prediction. _ArXiv preprint_ , 2021. 3 

- [56] Erfan Shayegani, GM Shahariar, Sara Abdali, Lei Yu, Nael Abu-Ghazaleh, and Yue Dong. Misaligned roles, misplaced images: Structural input perturbations expose multimodal alignment blind spots. _arXiv preprint arXiv:2504.03735_ , 2025. 2 

- [57] Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 2 

- [58] Wenxuan Song, Jiayi Chen, Pengxiang Ding, Han Zhao, Wei Zhao, Zhide Zhong, Zongyuan Ge, Jun Ma, and Haoang Li. Accelerating vision-language-action model integrated with action chunking via parallel decoding. _arXiv preprint arXiv:2503.02310_ , 2025. 2 

- [59] Lin Sun, Bin Xie, Yingfei Liu, Hao Shi, Tiancai Wang, and Jiale Cao. Geovla: Empowering 3d representations in vision- 

language-action models. _arXiv preprint arXiv:2508.09071_ , 2025. 2, 6 

- [60] Idris O Sunmola, Zhenjun Zhao, Samuel Schmidgall, Yumeng Wang, Paul Maria Scheikl, and Axel Krieger. Surgical gaussian surfels: Highly accurate real-time surgical scene rendering. _arXiv preprint arXiv:2503.04079_ , 2025. 2 

- [61] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 1, 6 

- [62] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. _arXiv preprint arXiv:2412.15109_ , 2024. 3 

- [63] Quan Vuong, Sergey Levine, Homer Rich Walke, Karl Pertsch, Anikait Singh, Ria Doshi, Charles Xu, Jianlan Luo, Liam Tan, Dhruv Shah, et al. Open x-embodiment: Robotic learning datasets and rt-x models. In _Towards Generalist Robots: Learning Paradigms for Scalable Skill Acquisition@ CoRL2023_ , 2023. 2 

- [64] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. Vggt: Visual geometry grounded transformer. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 3 

- [65] Mengwei Xie, Shuang Zeng, Xinyuan Chang, Xinran Liu, Zheng Pan, Mu Xu, and Xing Wei. Seqgrowgraph: Learning lane topology as a chain of graph expansions. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 27166–27175, 2025. 3 

- [66] Zhipei Xu, Xuanyu Zhang, Runyi Li, Zecheng Tang, Qing Huang, and Jian Zhang. Fakeshield: Explainable image forgery detection and localization via multi-modal large language models. In _International Conference on Learning Representations_ , 2025. 2 

- [67] Shaocheng Yan, Pengcheng Shi, Zhenjun Zhao, Kaixin Wang, Kuang Cao, Ji Wu, and Jiayuan Li. Turboreg: Turboclique for robust and efficient point cloud registration. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 26371–26381, 2025. 2 

- [68] Lihe Yang, Bingyi Kang, Zilong Huang, Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao. Depth anything: Unleashing the power of large-scale unlabeled data. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10371–10381, 2024. 5 

- [69] Lihe Yang, Bingyi Kang, Zilong Huang, Zhen Zhao, Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao. Depth anything v2. _Advances in Neural Information Processing Systems_ , 37:21875–21911, 2024. 5 

- [70] Rujia Yang, Geng Chen, Chuan Wen, and Yang Gao. Fp3: A 3d foundation policy for robotic manipulation. _arXiv preprint arXiv:2503.08950_ , 2025. 2 

- [71] Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024. 2 

6716 

- [72] Shuang Zeng, Xinyuan Chang, Mengwei Xie, Xinran Liu, Yifan Bai, Zheng Pan, Mu Xu, and Xing Wei. Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving. _arXiv preprint arXiv:2505.17685_ , 2025. 2 

- [73] Shuang Zeng, Dekang Qi, Xinyuan Chang, Feng Xiong, Shichao Xie, Xiaolong Wu, Shiyi Liang, Mu Xu, and Xing Wei. Janusvln: Decoupling semantics and spatiality with dual implicit memory for vision-language navigation. _arXiv preprint arXiv:2509.22548_ , 2025. 2 

- [74] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 11975–11986, 2023. 3 

- [75] Jinchang Zhang and Guoyu Lu. Underground mapping and localization based on ground-penetrating radar. In _Proceedings of the Asian Conference on Computer Vision_ , pages 2018–2033, 2024. 2 

- [76] Jinchang Zhang and Guoyu Lu. Vision-language embodiment for monocular depth estimation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 29479–29489, 2025. 

- [77] Jinchang Zhang, Praveen Kumar Reddy, Xue-Iuan Wong, Yiannis Aloimonos, and Guoyu Lu. Embodiment: Selfsupervised depth estimation based on camera models. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 7809–7816. IEEE, 2024. 2 

- [78] Jiahui Zhang, Yurui Chen, Yueming Xu, Ze Huang, Yanpeng Zhou, Yu-Jie Yuan, Xinyue Cai, Guowei Huang, Xingyue Quan, Hang Xu, et al. 4d-vla: Spatiotemporal vision-language-action pretraining with cross-scene calibration. _arXiv preprint arXiv:2506.22242_ , 2025. 2 

      - Diving into high-resolution large multimodal models. _arXiv preprint arXiv:2406.08487_ , 2024. 8 

   - [85] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 2, 6 

   - [86] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 2 

   - [87] Zhenjun Zhao. Balf: Simple and efficient blur aware local feature detector. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , pages 3362–3372, 2024. 2 

   - [88] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 2 

   - [89] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 2, 6 

   - [90] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _arXiv preprint arXiv:2504.02792_ , 2025. 3 

- [79] Jinchang Zhang, Zijun Li, Jiakai Lin, and Guoyu Lu. Adaptive event stream slicing for open-vocabulary event-based object detection via vision-language knowledge distillation. _arXiv preprint arXiv:2510.00681_ , 2025. 2 

- [80] Kaidong Zhang, Pengzhen Ren, Bingqian Lin, Junfan Lin, Shikui Ma, Hang Xu, and Xiaodan Liang. Pivot-r: Primitivedriven waypoint-aware world model for robotic manipulation. _Advances in Neural Information Processing Systems_ , 37:54105–54136, 2024. 3 

- [81] Rongchao Zhang, Weiping Ding, Hongbin Han, Yongzhi Cao, Hanpin Wang, and Yu Huang. Strfilter: Multi-modal medical image fusion via structure-oriented adaptive filtering. _Information Fusion_ , page 103888, 2025. 2 

- [82] Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Dan Wang, Yuan Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025. 2 

- [83] Rongchao Zhang, Yu Huang, Yongzhi Cao, and Hanpin Wang. Molebridge: Synthetic space projecting with discrete markov bridges. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 2 

- [84] Yi-Fan Zhang, Qingsong Wen, Chaoyou Fu, Xue Wang, Zhang Zhang, Liang Wang, and Rong Jin. Beyond llava-hd: 

6717 

