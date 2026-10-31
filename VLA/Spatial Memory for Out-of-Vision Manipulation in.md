---
title: "Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action"
date: "2026-05-21"
authors: "Pengteng Li; Weiyu Guo; He Zhang; Tiefu Cai; Xiao He; Yandong Guo"
venue: "ICML 2026"
url: https://arxiv.org/abs/2605.22283
pdf: https://arxiv.org/pdf/2605.22283
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.22283)** / [論文ページ](https://arxiv.org/abs/2605.22283)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

**Pengteng Li**<sup>1 2</sup> **Weiyu Guo**<sup>1 2</sup> **He Zhang**<sup>1 2</sup> **Tiefu Cai**<sup>1 2</sup> **Xiao He**<sup>2</sup> **Yandong Guo**<sup>2</sup> **Hui Xiong**<sup>1 3</sup> 

## **Abstract** 

We introduce **SOMA** , the **S** patial memory framework for **O** ut-of-Vision **M** anipulation in VisionLanguage- **A** ction (VLA) models. Most existing VLAs implicitly assume that task-relevant objects are always visible, leading to brittle and reactive behaviors when targets fall outside the camera’s field of view. SOMA addresses this limitation by equipping VLAs with a persistent, spatial memory constructed from multi-view observations acquired via a movable head camera, enabling reasoning beyond the current visual frustum. The framework consists of three components: _Spatial Memory Construction_ for aggregating angular-wise observations into a unified spatial–semantic representation by scanning, _Dynamic Memory Refinement_ for maintaining global consistency over time, and _Contextual Memory Retrieval_ for activating instruction-relevant spatial cues during manipulation. We evaluate SOMA on five self-designed challenging real-world OOV manipulation tasks, including multi-step and dualarm scenarios, where target objects are initially invisible. Experiment results show that SOMA not only improves task success rates, but also induces qualitatively different manipulation behaviors, with faster target localization, reduced viewpoint search, and near one-shot grasping under partial observability. Additional experiments on RoboCasa GR1 and SimplerEnv further validate the effectiveness of SOMA’s memory design under conventional fully observable settings. Code will be released soon. 

1Thrust of Artificial Intelligence, The Hong Kong University of Science and Technology (Guangzhou), China<sup>2</sup> AI<sup>2</sup> Robotics 3Department of Computer Science and Engineering, The Hong Kong University of Science and Technology Hong Kong SAR, China. Correspondence to: Yandong Guo _<_ Yandong.guo@live.com _>_ , Hui Xiong _<_ xionghui@ust.hk _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 


_Figure 1._ Illustration of the Out-of-Vision (OOV) limitation in existing VLA models. Most VLAs rely on purely reactive perception—actions are driven only by what is visible in the current view. When the target moves outside the field of view, perception can no longer support manipulation, leading to inevitable task failure. 

## **1. Introduction** 

The development of VLAs have become a central direction in robotic action modeling research (Zhao et al., 2025; Chen et al., 2025c; Kim et al., 2024; Shukor et al., 2025; Intelligence et al., 2025). These systems typically extend large-scale pre-trained Multimodal Large Language Models (MLLMs) (Bjorck et al., 2025; Yang et al., 2025a) with an action head or specialized action module that maps multimodal inputs—such as visual observations and naturallanguage instructions—into executable robotic actions. By leveraging the strong perception and reasoning capabilities of MLLMs, VLA models demonstrate improved generalization and task versatility across diverse robotic manipulation scenarios (Jiang et al., 2025b; Bu et al., 2025). 

However, most existing VLAs are developed under fixedview tabletop manipulation setups, typically relying on a single static camera or a third-person viewpoint. Such configurations are widely adopted because they simplify camera–robot calibration, provide stable state estimation, and facilitate large-scale data collection without the need for multi-view coordination or explicit spatial fusion. As a result, these models implicitly operate under a view-bound assumption—namely, that _the object referenced in the instruction is visible within the robot’s current camera view at decision time._ This assumption fundamentally limits the 

1 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

model’s ability to reason about objects that are temporarily occluded or outside the field of view. Without a mechanism to maintain a persistent spatial representation of the scene, the perception–action loop becomes strictly viewdependent: when a target object is not observed, the model lacks the necessary context to infer its presence or spatial relation, often leading to failure. As shown in Figure 1, even when multiple fixed camera viewpoints (e.g., head- and armmounted cameras) are available, the absence of a global spatial memory prevents the system from localizing unseen targets (such as the pink cup), highlighting a core limitation of view-bound perception in current VLA models. 

To address this limitation, recent work has attempted to compensate for out-of-view perception by relying on internal spatial reasoning under static camera setups, inferring unseen targets via learned spatial priors (Team et al., 2025; Jiang et al., 2025a; Bu et al., 2025; Li et al., 2025c). However, such inference is inherently brittle: existing MLLMs can reason reliably only when partial visual evidence or object-related cues are available, and their spatial estimates deteriorate rapidly once the target is fully outside the observable field (Yang et al., 2025b). When inferred relations deviate from physical reality, errors propagate through the perception–action pipeline, leading to inaccurate localization, misaligned motion, or task failure. These observations expose a fundamental limitation of current VLA paradigms: spatial reasoning alone, without grounded perceptual evidence, is insufficient for robust manipulation. When objects have never been observed or when past observations are not retained, increasing model capacity or reasoning depth cannot compensate for missing perceptual grounding. _Addressing this gap requires mechanisms that both acquire spatial evidence beyond the current view and retain it in a persistent scene representation._ In particular, integrating angular-wise observations into a coherent spatial–semantic memory enables globally consistent reasoning and effective manipulation even when task-relevant objects are temporarily out of view. 

Based on these insights, we introduce **SOMA** , a VLA framework for out-of-vision manipulation that equips the robot with persistent spatial memory for reasoning and action. Unlike prior VLAs that rely solely on instantaneous, viewbound visual observations, SOMA explicitly models perception as a memory-centric process, enabling manipulation beyond the current camera view. SOMA is built upon two key design principles: (1) a movable head-mounted camera that provides access to diverse viewpoints of the workspace, and (2) a global spatial memory that integrates angular-wise observations into a unified, queryable spatial–semantic representation. When a task-relevant target cannot be localized within the current view, SOMA triggers its _Spatial Memory Construction_ phase, during which the camera follows a predefined scanning strategy to systemat- 

ically acquire multi-view observations and assemble a coherent spatial representation of the scene. This process employs a multi-level visual abstraction pipeline that combines category-level semantics (Cheng et al., 2024), fine-grained appearance priors (Simeoni et al.´ , 2025), and implicit 3D geometric cues (Wang et al., 2025b). By fusing these complementary signals, SOMA constructs an overview memory that serves as a structured spatial substrate for downstream manipulation. During interaction, _Dynamic Memory Refinement_ incrementally assimilates newly observed information through similarity-aware fusion, maintaining global consistency as the scene evolves. Meanwhile, _Contextual Memory Retrieval_ aligns incoming multimodal instruction and perception tokens with the spatial memory, selectively activating instruction-relevant regions to guide precise and grounded manipulation, even when target objects are temporarily outside the current field of view. Extensive realworld evaluations demonstrate that SOMA fundamentally alters manipulation behavior under OOV conditions, enabling faster target localization, reduced viewpoint search, and near one-shot grasping. Additional experiments on RoboCasa Tabletop GR1 (Nasiriany et al., 2024) and SimplerEnv (Li et al., 2024) further validate the robustness and generality of SOMA’s memory mechanism under standard observability settings. Overall, our contribution can be listed as follows: 

- We introduce **SOMA** , a spatial memory framework for Vision-Language-Action models that enables out-ofvision manipulation by inducing a memory-guided manipulation paradigm beyond the current camera view, rather than reactive view-bound exploration. 

- We propose a memory-centric perception architecture comprising _Spatial Memory Construction_ , _Dynamic Memory Refinement_ , and _Contextual Memory Retrieval_ , which together maintain a persistent, object-centric spatial representation that supports cross-view consistency and instruction-aware action selection under limited viewpoint coverage. 

- Real-world experiments show that SOMA not only improves task success rates, but also consistently yields qualitatively different manipulation behaviors under out-of-vision conditions, including earlier target fixation, reduced head exploration, and near one-shot grasping. Additional evaluations on RoboCasa GR1 and SimplerEnv further validate the effectiveness of our memory design under fully observable settings 

## **2. Related Work** 

**Policy Learning for Robotic Manipulation.** Policy learning underpins robotic manipulation, enabling data-driven control for arm and whole-body coordination (Du & Song, 2025; Sun & Song, 2025; He et al., 2025; 2024; Xie et al., 

2 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

2025; Weng et al., 2025; Fu et al., 2024; Song et al., 2025a; 2024). Recent work introduces movable cameras to improve exploration under partial observability (Xiong et al., 2025; Zeng et al., 2025), but these methods remain instructionagnostic and rely on policies ( _e.g._ , Diffusion Policy (Chi et al., 2025)) without persistent spatial memory, limiting generalization to unseen goals and spatial configurations. In contrast, our framework integrates movable perception into a VLA models, enabling instruction-aligned, memoryguided manipulation. 

**Vision-Language-Action Models.** VLA models provide a unified framework for instruction-driven robotic manipulation. Prior work spans data-driven approaches trained on large-scale multimodal datasets (Luo et al., 2025; Bu et al., 2025; Zhai et al., 2025; Jiang et al., 2025a; Zitkovich et al., 2023; Intelligence et al., 2025; Guo et al., 2026), world-model (Wan et al., 2025; Agarwal et al., 2025; Li et al., 2025d) and latent-action formulations that enhance generalization (Cen et al., 2025; Zhang et al., 2025a; Agarwal et al., 2025; Ye et al., 2024; Chen et al., 2025d), and extensions to diverse embodiments including mobile, tactile, and force-based platforms (Chen et al., 2025b; Zhang et al., 2025c; Cheng et al., 2025; Yu et al., 2025). Recent efforts also explore efficiency (Chen et al., 2025a; Wang et al., 2025a; Zhang et al., 2025b; Wang et al., 2025d; Liu et al., 2024; Song et al., 2025b; Zheng et al., 2025; Wang et al., 2025c) and spatial grounding via geometric cues for precise localization (Qu et al., 2025; Li et al., 2025a; Zhu et al., 2025; Yuan et al., 2025; Li et al., 2025b; Guo et al., 2022; Li et al., 2025e; Sun et al., 2025; Li et al., 2026). Memorycentric designs (Shi et al., 2025; Sridhar et al., 2025) further store recent observations or key frames to support shortterm reasoning. Despite this progress, most existing VLAs remain fundamentally view-dependent, lacking mechanisms to retain and reuse spatial information beyond the current camera frustum. Consequently, they struggle with manipulation when task-relevant objects are temporarily unseen. This work addresses this limitation by introducing a spatialgrounded memory that enables persistent scene understanding and reliable out-of-vision manipulation, expanding the effective operational scope of VLA systems. 

## **3. Method** 

As shown in Figure 2, SOMA addresses the challenge of out-of-vision manipulation by equipping VLA with a spatial memory that supports persistent scene understanding beyond the current camera view. Prior to manipulation, if the target object referenced in the instruction cannot be localized in the current camera observation by the perception module, the robot performs a dedicated scene observation phase using a movable head camera to initialize _Spatial Memory Construction_ . Given a multi-view scanning se- 

quence, object-level semantics and their relative spatial relationships are extracted by combining efficient visual perception and geometric modeling. These representations are aggregated into an overview scene memory _M_ 0, which encodes a unified spatial–semantic representation of all observed objects. During manipulation, the model receives the current observation _o_<sup>_t_</sup> _c_<sup>, the user instruction, robot states, and</sup> a noised action sequence, where _c ∈{l, r, h}_ denotes the left arm, right arm, and head cameras. New observations from the head view _M_ ˆ _t_ through _Dynamic Memory Refinement o_<sup>_t_</sup> _h_<sup>are incorporated to update</sup> , which performs<sup>_M_0 into</sup> similarity-aware fusion to preserve global consistency while accommodating newly observed evidence. Subsequently, _Contextual Memory Retrieval_ aligns instruction-grounded vision–language embeddings with _M_<sup>ˆ</sup> _t_ , selectively activating task-relevant spatial representations to augment the current perceptual features. The resulting memory-enhanced vision–language tokens, together with robot states and noised action embeddings, are processed by DiT blocks and an action decoder to predict the next action chunk. By maintaining a globally consistent spatial memory, SOMA enables robust reasoning and manipulation even when task-relevant objects lie outside the current field of view. 

### **3.1. Spatial Memory Construction** 

_Spatial Memory Construction_ builds a unified spatial– semantic map of the environment by integrating object-level semantics and 3D geometry from head-camera exploration, serving as a global memory foundation for subsequent perception and manipulation. Given a scanning video sequence _V_ = _{fi}_<sup>_N_</sup> _i_ =1<sup>_v_,weuniformlysampleoneframeevery</sup><sup>_N_</sup> frames to obtain a subset _V_<sup>˜</sup> , which is used to construct the overview scene memory _M_ 0. Each sampled frame _fi ∈ V_<sup>˜</sup> is processed by a unified perception pipeline consisting of: (1) a geometry prior network (VGGT (Wang et al., 2025b)) for camera pose and coarse scene geometry estimation, (2) a semantic perception module (YOLO (Cheng et al., 2024)) for object localization and categorization, and (3) a semantic encoder (DINOv3 (Simeoni et al.´ , 2025)) for highdimensional visual feature extraction. Given the per-frame feature map **F**<sup>(</sup><sup>_i_)</sup> _∈_ R<sup>_H×W ×C_</sup> , each detected 2D bounding box _b_<sup>(</sup> _j_<sup>_i_)</sup> is used to crop its corresponding region, followed by spatial average pooling to obtain an instance-level appearance embedding **f** _j_<sup>(</sup><sup>_i_)</sup> _∈_ R<sup>_C_</sup> . Each 2D detection is further lifted into the global 3D scene coordinate system using VGGT-predicted geometric priors, yielding a 3D bounding box **b**<sup>(</sup> _j_<sup>_i_)</sup> _∈_ R<sup>8</sup><sup>_×_3</sup> . VGGT predicts the camera pose of each frame in a consistent scene-level coordinate system, which we treat as a shared global reference frame. All lifted 3D bounding boxes are expressed in this global frame using the estimated camera poses, enabling direct aggregation and comparison across views. Since the head-camera scan is short-horizon and performed in a static environment, pose 

3 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 


_Figure 2._ Illustration of the proposed SOMA framework. SOMA enhances OOV manipulation via spatial memory. (A) **Spatial Memory Construction:** Before manipulation, if the specified objects are not in the current observation, the robot actively scans the scene to construct a unified spatial–semantic memory _M_ 0 by integrating object semantics (YOLO (Cheng et al., 2024), DINOv3 (Simeoni et al.´ , 2025)) with geometric cues (VGGT (Wang et al., 2025b)). (B) **Dynamic Memory Refinement:** During interaction, newly perceived information _Mt_ is adaptively fused into the initial overview scene memory _M_ 0 through similarity-weighted updates, yielding a refined current memory _M_<sup>ˆ</sup> _t_ . (C) **Contextual Memory Retrieval:** Language-guided queries selectively attend to relevant memory regions, providing contextual cues for a DiT-based Action Decoder to generate executable manipulation actions. 

drift is negligible in practice and does not affect instance association or memory construction. 

Across all sampled frames _V_<sup>˜</sup> , detected instances are associated and fused across views to form a global set of view-invariant object instances. To resolve same-class ambiguities and multi-view duplicates, we perform class-wise instance association based on a joint appearance–geometry similarity, combining cosine similarity between DINOv3 embeddings and 3D spatial consistency between lifted bounding boxes. Instances with similarity above a threshold are merged, and their appearance features and 3D geometries are aggregated by averaging. This process yields global collections _F_ = _{_ **f** _k}_<sup>_N_</sup> _k_ =1<sup>_I_,</sup><sup>_B_3D=</sup><sup>_{_</sup><sup>**b**</sup><sup>_k}_</sup> _k_<sup>_N_</sup> =1<sup>_I_,and</sup> _C_ 3D = _{ck}_<sup>_N_</sup> _k_ =1<sup>_I_,where</sup><sup>_NI_denotesthenumberoffused</sup> object instances. To improve robustness under imperfect detections or missing observations, learned placeholder embeddings and pseudo bounding boxes are injected when no objects are detected in a sampled frame. Each global instance is ultimately represented by a unified triplet ( **f** _k, ck,_ **b** _k_ ), forming the fine-grained basis for constructing the overview scene memory. 

To construct a unified scene memory that captures both semantic identity and geometric configuration, we integrate object-level appearance embeddings with their corresponding 3D spatial encodings. Each 3D bounding box **b** _k_ is embedded into a spatial positional vector **p** _k_ = Φpos( **b** _k_ ), where Φpos( _·_ ) denotes the learnable 3D positional embedding module. The object features **f** _k_ are then projected into a shared embedding space through a learnable mapping Φmem( _·_ ), and combined with their corresponding spatial descriptors to form the joint spatial–semantic embedding: **m**<sup>0</sup> _k_<sup>=Φmem(</sup><sup>**f**</sup><sup>_k_)+</sup><sup>**p**</sup><sup>_k_.Theresulting</sup><sup>**m**0</sup> _k_<sup>_∈_R</sup><sup>_C_</sup> serves as the final memory token, jointly encoding appearance semantics and 3D spatial context. Collectively, the set of all such embeddings forms the overview scene memory: _M_ 0 = _{_ **m**<sup>0</sup> _k_<sup>_}N_</sup> _k_ =1<sup>_I,_whichprovidesacompact,</sup> geometry-aware, and semantically discriminative representation of the entire scene. 

### **3.2. Dynamic Memory Refinement** 

During manipulation, the environment evolves as objects move, become occluded, or newly appear in the scene. 

4 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 


_Figure 3._ Illustration of our real world benchmark settings. We design five challenging _out-of-vision_ pick-and-place (PnP) tasks to evaluate the robot’s OOV manipulation capabilities. Tasks (1–3) require the robot to use its left arm to pick up the object located outside the current field of view and place it into the basket. Task (4) involves sequential pick-and-place of the object followed by the other object into the same basket. Task (5) requires dual-arm coordination to pick and place the object into the basket. 


_Figure 4._ Performance comparison across five real world out-of-vision tasks. “Fixed Head Camera” denotes we train SOMA under fixed head camera setting. StarVLA (Ye et al., 2026; Community, 2026), SpatialVLA (Qu et al., 2025),GR00T N1.5 (Bjorck et al., 2025) and our proposed SOMA is trained under active head camera for fair. We adopt 20 episodes and average SR (Success Rate) to evaluate the models by multi-stages. 

|**Behavioral Analy**|**sis on Real-**|**World Out-**|**of-Vision Ta**|**sks**|
|---|---|---|---|---|
|**Model**<br>**Task 1**|**Task 2**|**Task 3**|**Task 4**|**Task 5**|
|_First-Fixation Time (s) ↓_<br>GR00T-N1.5<br>7.6|21.0|14.8|10.9|11.5|
|SOMA<br>**4.2**_↓_45%|**12.7**_↓_40%|**8.2**_↓_45%|**4.9**_↓_55%|**4.7**_↓_59%|
|_Head Search Path Length_<br>GR00T-N1.5<br>50.5|_(deg) ↓_<br>51.0|83.8|109.2|164.0|
|SOMA<br>**27.8**_↓_45%|**28.1**_↓_45%|**50.3**_↓_40%|**54.6**_↓_50%|**70.4**_↓_57%|
|_Viewpoint Correction Cou_<br>GR00T-N1.5<br>1.6|_nt ↓_<br>1.9|1.4|3.4|5.3|
|SOMA<br>**0.9**_↓_44%|**1.1**_↓_42%|**0.8**_↓_43%|**1.7**_↓_50%|**2.3**_↓_57%|
|_Grasp Attempt Count ↓_<br>GR00T-N1.5<br>1.8|2.0|1.7|2.4|3.7|
|SOMA<br>**1.0**_↓_44%|**1.2**_↓_40%|**1.0**_↓_41%|**1.2**_↓_50%|**1.6**_↓_57%|
|_Time-to-Grasp (s) ↓_<br>GR00T-N1.5<br>58.0|30.0|50.0|65.5|36.5|
|SOMA<br>**32.3**_↓_44%|**16.8**_↓_44%|**29.7**_↓_41%|**30.4**_↓_54%|**14.6**_↓_60%|


_Table 1._ Behavioral comparison between GR00T-N1.5 and SOMA on five real-world OOV manipulation tasks. 

To maintain an up-to-date and globally coherent scene representation, _Dynamic Memory Refinement_ is proposed to iteratively update the scene memory initialized by the overview memory _M_ 0 using the latest observation from the robot’s head-view camera. The current observation _o_<sup>_t_</sup> _h_ is processed by the same embedding pipeline described in Section 3.1 at time _t_ , producing the current memory tokens _Mt_ = _{_ **m**<sup>_t_</sup> _j_<sup>_}N_</sup> _j_ =1<sup>_t_, where each</sup><sup>**m**</sup> _j_<sup>_t_= Φmem(</sup><sup>**f**</sup><sup>_t_</sup> _j_<sup>)+ ¯</sup><sup>**p**</sup> _c_<sup>_t_</sup> _j_<sup>jointly</sup> encodes semantic and spatial cues extracted from the current frame, and **p** ¯ _ctj_<sup>denotes the positional embedding derived</sup> from the estimated 3D location of the observed instance. 

For each observed instance **m**<sup>_t_</sup> _j_<sup>with class label</sup><sup>_ct_</sup> _j_<sup>, we per-</sup> form instance-level association against the memory entries 

of the same class in the previous memory state _Mt−_ 1. If a matching memory instance **m**<sup>_t_</sup> _k_<sup>_−_1</sup> is found using the same class-wise appearance–geometry association criterion as in _Spatial Memory Construction,_ its representation is refined through an _adaptive similarity-aware fusion mechanism_ . Each observation is associated to at most one memory instance, and each memory entry is updated by at most one observation per time step _t_ . Given the previous memory vector **m**<sup>_t_</sup> _k_<sup>_−_1</sup> and the new observation **m**<sup>_t_</sup> _j_<sup>, we compute the</sup> semantic similarity _s_<sup>_t_</sup> _kj_<sup>and a dynamic fusion score</sup><sup>_g_</sup> _kj_<sup>_t_:</sup> 


where _σ_ ( _·_ ) denotes the sigmoid activation. The two scores jointly determine an adaptive update coefficient _αkj_<sup>_t_=</sup><sup>_g_</sup> _kj_<sup>_t·_</sup> _s_<sup>_t_</sup> _kj_<sup>.Thematchedmemorytokenisthenupdatedviaa</sup> temporal exponential moving average: 


This design adaptively balances new visual evidence with historical memory, allowing the representation to remain stable under minor viewpoint changes while rapidly adapting to meaningful scene updates. Observed instances without matched counterparts are appended as new memory entries, while unmatched past memory instances are retained to handle temporary occlusions and partial observability. The updated memory is denoted as _M_ ˆ _t_ = _{_ **m** ˆ<sup>_t_</sup> _k_<sup>_}N_</sup> _k_ =1 _t_<sup>_M_,where</sup> _Nt_<sup>_M_</sup> is the number of memory entries. This instance-aware temporal refinement process ensures memory consistency across time, faithfully reflecting the evolving scene state. 

5 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

### **3.3. Contextual Memory Retrieval** 

We inject global spatial–semantic knowledge into the multimodal representation for instruction-grounded reasoning. Given the vision–language token embeddings from the VLM, **X** vl = _{_ **x** _i ∈_ R<sup>_C_</sup> _}_<sup>_N_</sup> _i_ =1<sup>_q_, where</sup><sup>_Nq_is the token num-</sup> ber and eachtreat **X** vl as the **x** _i_ queryrepresents a visual–linguistic feature.set, and the scene memory, _M_ ˆ _t_ Weas the key–value memory bank containing the structured spatial context. Each memory token **m**<sup>_t_</sup> _k_<sup>is first projected into</sup> the same latent space as the VLM features via an alignment function: **m** ˜<sup>_t_</sup> _k_<sup>=Φalign( ˆ</sup><sup>**m**</sup> _k_<sup>_t_).Theretrievalprocess</sup> is realized through a cross-attention module, where **X** vl serves as the query **Q** and _M_<sup>˜</sup> _t_ as the key–value pair **K** , **V** : **<u>QK</u>**<sup>_⊤_</sup> **X** boost = _{_ **x**<sup>_′_</sup> _i_<sup>_}N_</sup> _i_ =1<sup>_q_= softmax</sup> � _~~√~~ C_ � **V** , which **x**<sup>_′_</sup> _i_<sup>denotes</sup> the enhanced token representations enriched with spatially grounded memory cues. Through this scenario knowledge interaction, each token **x** _i_ selectively attends to relevant regions in _M_<sup>˜</sup> _t_ , retrieving geometry-aware information that bridges current perception with global scene context. 

Finally, the retrieved memory-enhanced features **X** boost are injected into the DiT blocks as a spatial–semantic prior. The original vision–language tokens, robot state, and noised action embeddings are directly fed into the DiT, where **X** boost serves as global context that modulates token interactions. Through these DiT blocks, the model fuses current observations with the structured scene memory, producing refined state and action tokens. These refined tokens are then passed to the embodiment-specific action decoder to generate the final action chunk _{a_ ˆ _t,_ ˆ _at_ +1 _, . . . ,_ ˆ _at_ + _H−_ 1 _}_ , where _H_ denotes the action chunk length. 

## **4. Experiments** 

### **4.1. Benchmarks** 

We conduct extensive real-world experiments to validate the effectiveness of SOMA in OOV manipulation. We further evaluate its memory-centric design on RoboCasa Tabletop GR1 (Bjorck et al., 2025) and SimplerEnv (Li et al., 2024). 

**Real World OOV Tasks.** As shown in Figure 3 and 5, we construct a real-world benchmark of five out-of-vision pickand-place (PnP) tasks with increasing difficulty to evaluate SOMA under partial observability. All tasks require manipulating objects outside the robot’s initial field of view, directly probing the model’s ability to operate beyond instantaneous visual input. Tasks (1)–(3) evaluate single-object manipulation under different visibility transitions, testing spatial recall and re-identification. Task (4) introduces sequential dual-object manipulation, requiring spatial memory to be preserved and reused across stages. Task (5) further involves dual-arm coordination, where success depends on maintaining a globally consistent spatial representation. These tasks 

|**OOV Task**|**Scan+GR00T**|**No-Scan SOMA**|**Scan-only SOMA**|**Full SOMA**|
|---|---|---|---|---|
|Task 1|19.0|20.0|25.0|**30.0**|
|Task 2|22.0|24.0|29.0|**35.0**|
|Task 3|16.0|17.5|22.5|**27.5**|
|Task 4|25.0|26.0|30.0|**32.5**|
|Task 5|10.5|11.7|14.2|**16.7**|
|**SR (%)**|18.5|19.8|24.1|**28.3**|


_Table 2._ Ablation study on scan-based exploration and spatial memory for real-world OOV manipulation. _Scan+GR00T_ performs head scanning and uses the detected target frame as a fixed visual input for a reactive policy, without maintaining a persistent spatial memory. _No-Scan SOMA_ initializes the memory from the first observed frame without multi-view scanning. _Scan-only SOMA_ constructs the memory from multi-view scans but disables memory refinement during manipulation. 

enable a behavior-level evaluation of spatial memory, revealing its impact on target localization, viewpoint efficiency, and manipulation under partial observability. 

**Static Simulation Tasks.** We evaluate the memory design of SOMA on RoboCasa Tabletop GR1 (Nasiriany et al., 2024; Bjorck et al., 2025) and SimplerEnv. RoboCasa Tabletop GR1 provides a large-scale tabletop manipulation suite with diverse objects, layouts, and multi-stage tasks requiring joint grounding of vision and language. SimplerEnv offers a standardized real-to-sim benchmark for evaluating policy success rates across simulated environments reflecting real-world robotic systems (Zitkovich et al., 2023). 

### **4.2. Implementation** 

**Robot Setting.** Real-world experiments are conducted on a self-designed humanoid platform equipped with two 7- DoF Realman ZM73 arms and adaptive grippers. The robot features a 2-DoF motorized head with pan–tilt control, enabling viewpoint adjustment during manipulation. For multiview perception, Intel RealSense D435 RGB-D cameras are mounted on the head and both wrists, providing synchronized visual and depth observations. We also deploy an NVIDIA Jetson AGX Orin (64 GB) on robot. 

**Training Details.** To accelerate training, _Spatial Memory Construction_ is performed offline during data preprocessing. For real-world experiments, we collect 400 expert demonstrations per task using a VR teleoperation system. Each trajectory consists of a scanning phase, used to construct the overview scene memory, and a manipulation phase, which is used for training all comparison models. For simulation experiments, the overview memory is constructed from the first frame of each trajectory. “Full” denotes training on the complete RoboCasa Tabletop dataset. We adopt GR00T N1.5 (Bjorck et al., 2025) as the real-world baseline. During training, all components are optimized except the VLM language decoder, using multi-task learning with a batch size of 60 for 30,000 steps on 32 NVIDIA H200 GPUs. 

**Inference Details.** All inference are executed on a server equipped with an NVIDIA RTX 4090 GPU. In real-world 

6 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 


_Figure 5._ Illustration of task execution examples for our five challenging out-of-vision tasks in real world using our proposed SOMA. 

experiments, the _Spatial Memory Construction_ phase is triggered by a perception-based criterion: a lightweight object detector checks whether the target specified in the instruction is visible in the current view. If the target cannot be localized, SOMA initiates an active head-scanning procedure along a predefined trajectory to construct the spatial memory. In simulation, the overview memory is constructed from the initial robot observation. 

### **4.3. Real World Results** 

In Figure 4, SOMA achieves the highest success rates across all five real-world out-of-vision (OOV) manipulation tasks. The fixed-head variant fails once either the target or the goal leaves the field of view, confirming the brittleness of view-bound policies under partial observability. Although prior VLAs with active head control (e.g., StarVLA (Ye et al., 2026; Community, 2026), SpatialVLA (Qu et al., 2025), and GR00T-N1.5 (Bjorck et al., 2025)) can partially recover visibility, their performance degrades in multi-stage and dual-arm tasks, where spatial information must be preserved and reused across stages. In contrast, SOMA maintains consistently higher success rates across both Pick and Place stages, with the performance gap widening as task complexity increases. These results indicate that persistent spatial memory, rather than reactive viewpoint adjustment, is critical for reliable manipulation beyond the current visual frustum. 

Moreover, we also investigate the different behaviour mode between out SOMA and GR00T as shown in Table 1. It demonstrates that SOMA’s advantages go beyond improved 

success rates and manifest as qualitatively different execution behavior. Across all five tasks, SOMA consistently shortens the time required to visually acquire the target, reduces head search motion, and stabilizes viewpoint alignment, achieving 40–60% improvements over GR00T-N1.5 depending on task difficulty. In particular, SOMA exhibits near one-shot grasping behavior, with significantly fewer grasp attempts and corrective head motions, indicating more decisive and spatially grounded execution. The behavioral gap becomes increasingly pronounced as task difficulty increases. On the most challenging dual-arm Task 5, SOMA substantially reduces head search effort, viewpoint corrections, and time-to-grasp, highlighting its ability to maintain a consistent global spatial representation across multi-arm coordination and staged manipulation. These results demonstrate that SOMA’s spatial memory enables stable crossstage spatial grounding, leading to both higher efficiency and greater reliability in out-of-vision manipulation. 

Finally, Table 2 disentangles the roles of scan-based exploration and explicit spatial memory in real-world out-ofvision manipulation. _Scan+GR00T_ , which performs head scanning without maintaining a persistent spatial memory, yields the lowest performance, indicating that scan-based exploration alone is insufficient for reliable OOV manipulation. _No-Scan SOMA_ slightly outperforms Scan+GR00T despite using only a single-view initialization, highlighting the benefit of an explicit memory structure even without multi-view coverage. _Scan-only SOMA_ further improves success rates by leveraging multi-view scanning to construct a more complete initial memory, but still falls short of the full model. In contrast, _Full SOMA_ consistently achieves the 

7 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

|**Task Category**|**Diffus**<br>30|**ion Po**<br>100|**licy**(Chi<br>300|et al.,2025)<br>Full|**StarV**<br>30|**LA**<sup>_∗_</sup>(<br>100|Commun<br>300|ity,2026)<br>Full|**GR00**<br>30|**T N1.5**<br>100|(Bjorck<br>300|et al.,2025)<br>Full|30|**SOMA**<br>100|**(Ours**<br>300|**)**<br>Full|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Container Interaction|35.1|49.5|54.2|-|1.4|1.1|1.8|3.0|35.3|33.7|35.7|40.3|52.3|52.0|53.3|55.6|
|Cooking Preparation|19.2|31.4|35.3|-|10.5|14.2|25.8|27.6|40.8|45.2|42.8|49.2|43.6|50.8|48.4|46.4|
|Tabletop Serving|13.2|18.4|28.4|-|15.0|18.5|24.0|25.0|41.0|47.5|48.5|39.5|44.5|46.5|54.0|47.5|
|Dish Transfer|16.9|22.3|39.0|-|11.3|15.0|21.5|22.5|44.0|58.5|51.0|50.0|58.0|58.0|55.0|49.5|
|Tray Organization|15.7|32.6|39.2|-|25.3|28.2|27.9|28.8|36.0|40.0|43.6|50.8|43.2|38.0|48.8|47.6|
|**Average**|20.0|30.8|39.2|-|12.7|15.4|20.2|21.4|39.4|44.9|44.3|45.9|**48.3**|**49.1**|**52.0**|**49.3**|


_Table 3._ Performance comparison via SR (%) across task categories on the Robocasa Tabletop GR1 benchmarks with varying numbers of demonstrations per task. Each group of four columns corresponds to one method (30 / 100 / 300 / Full demos per task). Bold numbers indicate the best result for each setting.<sup>_∗_</sup> denotes that we utilize the Qwen-GR00T setting for development. 

||**(a) Visual Ma**|**tching**|||
|---|---|---|---|---|
|**Model**|Pick Coke Can|Move Near|Open/Close Drawer|Average|
|Moto (Chen et al.,2025e)|74.0|60.4|43.1|59.2|
|RoboVLM (Liu et al.,2025)|77.3|61.7|43.5|60.6|
|TraceVLA (Zheng et al.,2024)|28.0|53.7|57.0|42.0|
|_π_0(Intelligence et al.,2025)|72.7|65.3|38.3|58.8|
|_π_0+FAST (Driess et al.,2025)|75.3|67.5|42.9|61.9|
|OpenVLA-OFT (Kim et al.,2025)|72.3|69.6|47.2|63.0|
|GR00T-N1.5 (Bjorck et al.,2025)|47.0|70.0|18.1|45.0|
|SOMA (Ours)|**85.0**|73.0|31.5|**63.2**|
||**(b) Variant Agg**|**regation**|||
|**Model**|Pick Coke Can|Move Near|Open/Close Drawer|Average|
|OpenVLA (Kim et al.,2024)|54.5|47.7|17.7|39.8|
|RoboVLM (Liu et al.,2025)|**75.6**|60.0|10.6|51.3|
|TraceVLA (Zheng et al.,2024)|60.0|56.4|**31.0**|45.0|
|OpenVLA-OFT (Kim et al.,2025)|65.3|59.0|12.2|45.5|
|GR00T-N1.5 (Bjorck et al.,2025)|46.7|62.9|17.5|42.4|
|SOMA (Ours)|55.5|**76.6**|25.4|**52.5**|


_Table 4._ SimplerEnv evaluation across different SOTAs on Google Robot tasks. We report results of all models pretrained with OXE (O’Neill et al., 2024) dataset and then fine-tuned with Fractal dataset (Brohan et al., 2022). 

best performance by continuously refining and interacting with the spatial memory during manipulation. These results demonstrate that while scanning can provide useful coverage for bootstrapping, the dominant performance gains arise from persistent spatial memory and its ongoing refinement, rather than scanning itself. 

### **4.4. Simulation Results** 

**GR1 Results.** Table 3 presents SR across five task categories under varying numbers of demonstrations. Overall, SOMA achieves the highest average performance of 52.0% with 300 demos and maintains competitive results across all data regimes, surpassing strong baselines such as Diffusion Policy (Chi et al., 2025), GR00T (Bjorck et al., 2025), and StarVLA (Community, 2026). The advantage is particularly evident in _Dish Transfer_ and _Tabletop Serving_ , where SOMA consistently outperforms diffusion-based policies by over 15%, demonstrating the effectiveness of its designed spatial memory in handling multi-stage, spatially complex manipulations. Notably, even with only 30–100 demonstrations per task, SOMA maintains high success rates, revealing strong sample efficiency and robust generalization to unseen spatial configurations. These consistent gains across all categories confirm that grounding perception and action generation in a structured spatial memory yields more coherent, globally aware manipulation in complex, multi-object environments. 

|**Ablation Setting**|**w/o Geo.**|**w/o Obj.**|**w/o Update**|**Full (Ours)**|
|---|---|---|---|---|
|Geometric cues||✓|✓|✓|
|Object Semantics|✓||✓|✓|
|Dynamic Update|✓|✓||✓|
|**Overall Success (%)**|45.1|43.7|41.5|**49.3**|


_Table 5._ Ablation study on different components of the proposed memory design. “Geo.” and “Obj.” denote Geometric cues and object semantics, respectively. 

**SimplerEnv Results.** Table 4 reports the performance comparison across multiple SOTA VLAs. In the _Visual Matching_ setting (Table 4(a)), our SOMA achieves the best SR of 63.2%, surpassing all listed SOTAs. Compared to strong baselines like RoboVLM (Liu et al., 2025) (60.6%), SOMA improves performance particularly on challenging partialobservation tasks like _Pick Coke Can_ (+7.7%), highlighting the benefit of its designed memory mechanism. In the _Variant Aggregation_ setting (Table 4(b)), SOMA also achieves the highest overall average of 52.5%, demonstrating strong robustness and spatial consistency across task variants. 

### **4.5. Ablation Study** 

We utilize GR1 benchmark for evaluation and leverage _full training version_ as the baseline model. All experiments evaluated over 50 episodes for accuracy. _More detailed results are provided in the Appendix._ 

**Overall Memory Construction.** As shown in Table 5, we conduct the ablation study on different components of the overview scene memory. Removing positional cues ( _w/o Geo._ ) or object semantics ( _w/o Obj._ ) leads to clear performance drops from 49.3% to 45.1% and 43.7%, respectively, confirming that both spatial geometry and semantic identity are indispensable for constructing a coherent global memory. Further excluding the dynamic update mechanism ( _w/o Update_ ) causes the largest degradation to 41.5%, highlighting the importance of temporal refinement in maintaining memory consistency across observations. 

## **5. Conclusion** 

We propose SOMA, a spatial memory framework for VisionLanguage-Action models that addresses the fundamental limitation of view-bound perception in out-of-vision manip- 

8 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

ulation. By constructing, refining, and retrieving a persistent spatial–semantic memory from multi-view observations, SOMA enables robots to retain and reuse spatial evidence beyond instantaneous visual input. This memory-centric design supports robust reasoning and manipulation when task-relevant objects are temporarily outside the field of view, without relying on brittle view-dependent behaviors. Extensive real-world experiments demonstrate the practical effectiveness of SOMA in challenging out-of-vision manipulation scenarios, while additional evaluations in simulation show that the proposed memory mechanism remains beneficial under conventional fully observable settings. 

## **Acknowledgements** 

This work was supported in part by the National Key R&D Program of China (Grant No.2023YFF0725001), in part by the National Natural Science Foundation of China (Grant No.92370204),in part by the guangdong Basic and Applied Basic Research Foundation (Grant No.2023B1515120057), in part by the Key-Area Special Project of Guangdong Provincial Ordinary Universities (2024ZDZX1007). 

Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. <u>arXiv preprint arXiv:2212.06817, 2022.</u> 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., Gao, S., He, X., Hu, X., Huang, X., et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. <u>arXiv preprint arXiv:2503.06669, 2025.</u> 

- Cen, J., Yu, C., Yuan, H., Jiang, Y., Huang, S., Guo, J., Li, X., Song, Y., Luo, H., Wang, F., et al. Worldvla: Towards autoregressive action world model. <u>arXiv preprint arXiv:2506.21539, 2025.</u> 

- Chen, H., Liu, J., Gu, C., Liu, Z., Zhang, R., Li, X., He, X., Guo, Y., Fu, C.-W., Zhang, S., et al. Fast-in-slow: A dual-system foundation model unifying fast manipulation within slow reasoning. <u>arXiv preprint arXiv:2506.01953,</u> 2025a. 

- Chen, S., Liu, J., Qian, S., Jiang, H., Li, L., Zhang, R., Liu, Z., Gu, C., Hou, C., Wang, P., et al. Ac-dit: Adaptive coordination diffusion transformer for mobile manipulation. <u>arXiv preprint arXiv:2507.01961, 2025b.</u> 

## **Impact Statement** 

This work addresses the challenge of manipulation under limited operational field of view by introducing a spatial memory framework that enables robots to reason about and act on objects beyond the current camera view. By integrating multi-view scene exploration, persistent spatial memory, and contextual interaction, the proposed approach improves robustness in long-horizon manipulation tasks where relevant objects cannot be directly observed at execution time. This capability is particularly relevant for real-world robotic applications such as household assistance and industrial manipulation, where sensing is often constrained by embodiment and task geometry. The framework is modular and builds on standard perception components, allowing future improvements in perception and safety-aware control to further enhance reliability. 

## **References** 

- Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al. Cosmos world foundation model platform for physical ai. <u>arXiv preprint arXiv:2501.03575, 2025.</u> 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. <u>arXiv preprint arXiv:2503.14734, 2025.</u> 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., 

- Chen, T., Kornblith, S., Norouzi, M., and Hinton, G. A simple framework for contrastive learning of visual representations. In <u>International conference on machine learning,</u> pp. 1597–1607. PmLR, 2020. 

- Chen, X., Chen, Y., Fu, Y., Gao, N., Jia, J., Jin, W., Li, H., Mu, Y., Pang, J., Qiao, Y., et al. Internvla-m1: A spatially guided vision-language-action framework for generalist robot policy. <u>arXiv preprint arXiv:2510.13778, 2025c.</u> 

- Chen, X., Wei, H., Zhang, P., Zhang, C., Wang, K., Guo, Y., Yang, R., Wang, Y., Xiao, X., Zhao, L., et al. Villax: enhancing latent action modeling in vision-languageaction models. <u>arXiv preprint arXiv:2507.23682, 2025d.</u> 

- Chen, Y., Ge, Y., Tang, W., Li, Y., Ge, Y., Ding, M., Shan, Y., and Liu, X. Moto: Latent motion token as the bridging language for learning robot manipulation from videos. In <u>Proceedings of the IEEE/CVF International Conference on Computer Vision, pp. 19752–19763, 2025e.</u> 

- Cheng, T., Song, L., Ge, Y., Liu, W., Wang, X., and Shan, Y. Yolo-world: Real-time open-vocabulary object detection. In <u>Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 16901–</u> 16911, 2024. 

- Cheng, Z., Zhang, Y., Zhang, W., Li, H., Wang, K., Song, L., and Zhang, H. Omnivtla: Vision-tactile-languageaction model with semantic-aligned tactile sensing. <u>arXiv preprint arXiv:2508.08706, 2025.</u> 

9 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. <u>The International Journal of Robotics Research,</u> 44(10-11): 1684–1704, 2025. 

- Community, S. Starvla: A lego-like codebase for visionlanguage-action model developing. <u>arXiv preprint arXiv:2604.05014, 2026.</u> 

- Driess, D., Springenberg, J. T., Ichter, B., Yu, L., Li-Bell, A., Pertsch, K., Ren, A. Z., Walke, H., Vuong, Q., Shi, L. X., et al. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. <u>arXiv preprint arXiv:2505.23705, 2025.</u> 

- Du, M. and Song, S. Dynaguide: Steering diffusion polices with active dynamic guidance. <u>arXiv preprint arXiv:2506.13922, 2025.</u> 

- Fu, Z., Zhao, Q., Wu, Q., Wetzstein, G., and Finn, C. Humanplus: Humanoid shadowing and imitation from humans. <u>arXiv preprint arXiv:2406.10454, 2024.</u> 

- Guo, W., Li, Z., Yang, Y., Wang, Z., Taylor, R. H., Unberath, M., Yuille, A., and Li, Y. Context-enhanced stereo transformer. In <u>European Conference on Computer Vision,</u> pp. 263–279. Springer, 2022. 

- Guo, W., Chen, Z., Wang, S., He, J., Xu, Y., Ye, J., Sun, Y., and Xiong, H. Logic-in-frames: Dynamic keyframe search via visual semantic-logical verification for long video understanding. <u>Advances in Neural Information Processing Systems, 38:124389–124422, 2026.</u> 

- He, T., Luo, Z., He, X., Xiao, W., Zhang, C., Zhang, W., Kitani, K., Liu, C., and Shi, G. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. <u>arXiv preprint arXiv:2406.08858, 2024.</u> 

- He, T., Gao, J., Xiao, W., Zhang, Y., Wang, Z., Wang, J., Luo, Z., He, G., Sobanbab, N., Pan, C., et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. <u>arXiv preprint arXiv:2502.01143, 2025.</u> 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: a vision-language-action model with openworld generalization. <u>arXiv preprint arXiv:2504.16054,</u> 2025. 

- Jiang, T., Yuan, T., Liu, Y., Lu, C., Cui, J., Liu, X., Cheng, S., Gao, J., Xu, H., and Zhao, H. Galaxea open-world dataset and g0 dual-system vla model. <u>arXiv preprint arXiv:2509.00576, 2025a.</u> 

- Jiang, Y., Zhang, R., Wong, J., Wang, C., Ze, Y., Yin, H., Gokmen, C., Song, S., Wu, J., and Fei-Fei, L. Behavior robot suite: Streamlining real-world whole-body manipulation for everyday household activities. <u>arXiv preprint arXiv:2503.05652, 2025b.</u> 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. <u>arXiv preprint arXiv:2406.09246, 2024.</u> 

- Kim, M. J., Finn, C., and Liang, P. Fine-tuning visionlanguage-action models: Optimizing speed and success. <u>arXiv preprint arXiv:2502.19645, 2025.</u> 

- Li, C., Wen, J., Peng, Y., Peng, Y., Feng, F., and Zhu, Y. Pointvla: Injecting the 3d world into vision-languageaction models. <u>arXiv preprint arXiv:2503.07511, 2025a.</u> 

- Li, F., Song, W., Zhao, H., Wang, J., Ding, P., Wang, D., Zeng, L., and Li, H. Spatial forcing: Implicit spatial representation alignment for vision-language-action model. <u>arXiv preprint arXiv:2510.12276, 2025b.</u> 

- Li, P., Song, P., Li, W., Guo, W., Yao, H., Xu, Y., Liu, D., and Xiong, H. See&trek: Training-free spatial prompting for multimodal large language model. <u>arXiv preprint arXiv:2509.16087, 2025c.</u> 

- Li, W., Pan, W., Luan, P.-C., Gao, Y., and Alahi, A. Stable video infinity: Infinite-length video generation with error recycling. <u>arXiv preprint arXiv:2510.09212, 2025d.</u> 

- Li, W., Zhang, R., Shao, R., Fang, Z., Zhou, K., Tian, Z., and Nie, L. Semanticvla: Semantic-aligned sparsification and enhancement for efficient robotic manipulation. <u>arXiv preprint arXiv:2511.10518, 2025e.</u> 

- Li, W., Yu, Z., and Alahi, A. Voxdet: Rethinking 3d semantic scene completion as dense object detection. <u>Advances in Neural Information Processing Systems,</u> 38:81004– 81038, 2026. 

- Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al. Evaluating real-world robot manipulation policies in simulation. <u>arXiv preprint arXiv:2405.05941, 2024.</u> 

- Liu, H., Li, X., Li, P., Liu, M., Wang, D., Liu, J., Kang, B., Ma, X., Kong, T., and Zhang, H. Towards generalist robot policies: What matters in building vision-language-action models. <u>arXiv preprint arXiv, 2025.</u> 

- Liu, J., Liu, M., Wang, Z., An, P., Li, X., Zhou, K., Yang, S., Zhang, R., Guo, Y., and Zhang, S. Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation. <u>Advances in Neural Information Processing Systems, 37:40085–40110, 2024.</u> 

10 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

- Luo, H., Feng, Y., Zhang, W., Zheng, S., Wang, Y., Yuan, H., Liu, J., Xu, C., Jin, Q., and Lu, Z. Being-h0: Vision-language-action pretraining from large-scale human videos. <u>arXiv preprint arXiv:2507.15597, 2025.</u> 

- Nasiriany, S., Maddukuri, A., Zhang, L., Parikh, A., Lo, A., Joshi, A., Mandlekar, A., and Zhu, Y. Robocasa: Largescale simulation of everyday tasks for generalist robots. <u>arXiv preprint arXiv:2406.02523, 2024.</u> 

- O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In <u>2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 6892–6903. IEEE,</u> 2024. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. <u>arXiv preprint arXiv:2501.15830, 2025.</u> 

- Shi, H., Xie, B., Liu, Y., Sun, L., Liu, F., Wang, T., Zhou, E., Fan, H., Zhang, X., and Huang, G. Memoryvla: Perceptual-cognitive memory in vision-languageaction models for robotic manipulation. <u>arXiv preprint arXiv:2508.19236, 2025.</u> 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., Aractingi, M., Pascal, C., Russi, M., Marafioti, A., et al. Smolvla: A vision-languageaction model for affordable and efficient robotics. <u>arXiv preprint arXiv:2506.01844, 2025.</u> 

- Simeoni, O., Vo, H. V., Seitzer, M., Baldassarre, F., Oquab,´ M., Jose, C., Khalidov, V., Szafraniec, M., Yi, S., Ramamonjisoa, M., et al. Dinov3. <u>arXiv preprint arXiv:2508.10104, 2025.</u> 

- Song, P., Li, P., Aertbelien, E., and Detry, R.¨ Robot trajectron: Trajectory prediction-based shared control for robot manipulation. In <u>2024 IEEE International Conference on Robotics and Automation (ICRA), pp. 5585–5591. IEEE,</u> 2024. 

- Song, P., Hu, Y., Li, P., and Detry, R. Equivariant volumetric grasping. <u>arXiv preprint arXiv:2507.18847, 2025a.</u> 

- Song, W., Chen, J., Ding, P., Huang, Y., Zhao, H., Wang, D., and Li, H. Ceed-vla: Consistency vision-languageaction model with early-exit decoding. <u>arXiv preprint arXiv:2506.13725, 2025b.</u> 

- Sridhar, A., Pan, J., Sharma, S., and Finn, C. Memer: Scaling up memory for robot control via experience retrieval. <u>arXiv preprint arXiv:2510.20328, 2025.</u> 

- Sun, L., Xie, B., Liu, Y., Shi, H., Wang, T., and Cao, J. Geovla: Empowering 3d representations in vision-language-action models. <u>arXiv preprint arXiv:2508.09071, 2025.</u> 

- Sun, Z. and Song, S. Latent policy barrier: Learning robust visuomotor policies by staying in-distribution. <u>arXiv preprint arXiv:2508.05941, 2025.</u> 

- Team, B. R., Cao, M., Tan, H., Ji, Y., Chen, X., Lin, M., Li, Z., Cao, Z., Wang, P., Zhou, E., et al. Robobrain 2.0 technical report. <u>arXiv preprint arXiv:2507.02029, 2025.</u> 

- Wan, T., Wang, A., Ai, B., Wen, B., Mao, C., Xie, C.-W., Chen, D., Yu, F., Zhao, H., Yang, J., et al. Wan: Open and advanced large-scale video generative models. <u>arXiv preprint arXiv:2503.20314, 2025.</u> 

- Wang, H., Xu, J., Pan, J., Zhou, Y., and Dai, G. Specprunevla: Accelerating vision-language-action models via action-aware self-speculative pruning. <u>arXiv preprint arXiv:2509.05614, 2025a.</u> 

- Wang, J., Chen, M., Karaev, N., Vedaldi, A., Rupprecht, C., and Novotny, D. Vggt: Visual geometry grounded transformer. In <u>Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 5294–5306, 2025b.</u> 

- Wang, Y., Ding, P., Li, L., Cui, C., Ge, Z., Tong, X., Song, W., Zhao, H., Zhao, W., Hou, P., et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. <u>arXiv preprint arXiv:2509.09372, 2025c.</u> 

- Wang, Y., Zhu, H., Liu, M., Yang, J., Fang, H.-S., and He, T. Vq-vla: Improving vision-language-action models via scaling vector-quantized action tokenizers. <u>arXiv preprint arXiv:2507.01016, 2025d.</u> 

- Weng, H., Li, Y., Sobanbabu, N., Wang, Z., Luo, Z., He, T., Ramanan, D., and Shi, G. Hdmi: Learning interactive humanoid whole-body control from human videos. <u>arXiv preprint arXiv:2509.16757, 2025.</u> 

- Wu, P., Shentu, Y., Yi, Z., Lin, X., and Abbeel, P. Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators. In <u>2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS),</u> pp. 12156–12163. IEEE, 2024. 

- Xie, W., Han, J., Zheng, J., Li, H., Liu, X., Shi, J., Zhang, W., Bai, C., and Li, X. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. <u>arXiv preprint arXiv:2506.12851, 2025.</u> 

- Xiong, H., Xu, X., Wu, J., Hou, Y., Bohg, J., and Song, S. Vision in action: Learning active perception from human demonstrations. <u>arXiv preprint arXiv:2506.15666, 2025.</u> 

11 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

- Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., et al. Qwen3 technical report. <u>arXiv preprint arXiv:2505.09388, 2025a.</u> 

- Yang, J., Yang, S., Gupta, A. W., Han, R., Fei-Fei, L., and Xie, S. Thinking in space: How multimodal large language models see, remember, and recall spaces. In <u>Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 10632–10643, 2025b.</u> 

- Ye, J., Gao, N., Yang, S., Zheng, J., Wang, Z., Chen, Y., Chen, P., Chen, Y., Liu, S., and Jia, J. Starvla- _alpha_ : Reducing complexity in vision-language-action systems. <u>arXiv preprint arXiv:2604.11757, 2026.</u> 

- Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., et al. Latent action pretraining from videos. <u>arXiv preprint arXiv:2410.11758, 2024.</u> 

- Yu, J., Liu, H., Yu, Q., Ren, J., Hao, C., Ding, H., Huang, G., Huang, G., Song, Y., Cai, P., et al. Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation. <u>arXiv preprint arXiv:2505.22159, 2025.</u> 

- Yuan, T., Liu, Y., Lu, C., Chen, Z., Jiang, T., and Zhao, H. Depthvla: Enhancing vision-language-action models with depth-aware spatial reasoning. <u>arXiv preprint arXiv:2510.13375, 2025.</u> 

   - chain-of-thought reasoning for vision-language-action models. In <u>Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 1702–1713, 2025.</u> 

   - Zheng, J., Li, J., Wang, Z., Liu, D., Kang, X., Feng, Y., Zheng, Y., Zou, J., Chen, Y., Zeng, J., et al. X-vla: Soft-prompted transformer as scalable crossembodiment vision-language-action model. <u>arXiv preprint arXiv:2510.10274, 2025.</u> 

   - Zheng, R., Liang, Y., Huang, S., Gao, J., Daume´ III, H., Kolobov, A., Huang, F., and Yang, J. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. <u>arXiv preprint arXiv:2412.10345, 2024.</u> 

   - Zhu, M., Zhu, Y., Li, J., Zhou, Z., Wen, J., Liu, X., Shen, C., Peng, Y., and Feng, F. Objectvla: End-to-end openworld object manipulation without demonstration. <u>arXiv preprint arXiv:2502.19250, 2025.</u> 

   - Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In <u>Conference on Robot Learning, pp.</u> 2165–2183. PMLR, 2023. 

- Zeng, Q., Li, C., John, J. S., Zhou, Z., Wen, J., Feng, G., Zhu, Y., and Xu, Y. Activeumi: Robotic manipulation with active perception from robot-free human demonstrations. <u>arXiv preprint arXiv:2510.01607, 2025.</u> 

- Zhai, A., Liu, B., Fang, B., Cai, C., Ma, E., Yin, E., Wang, H., Zhou, H., Wang, J., Shi, L., et al. Igniting vlms toward the embodied space. <u>arXiv preprint arXiv:2509.11766,</u> 2025. 

- Zhang, J., Guo, Y., Hu, Y., Chen, X., Zhu, X., and Chen, J. Up-vla: A unified understanding and prediction model for embodied agent. <u>arXiv preprint arXiv:2501.18867,</u> 2025a. 

- Zhang, R., Dong, M., Zhang, Y., Heng, L., Chi, X., Dai, G., Du, L., Du, Y., and Zhang, S. Mole-vla: Dynamic layer-skipping vision language action model via mixtureof-layers for efficient robot manipulation. <u>arXiv preprint arXiv:2503.20384, 2025b.</u> 

- Zhang, Z., Xu, H., Yang, Z., Yue, C., Lin, Z., Gao, H.a., Wang, Z., and Zhao, H. Ta-vla: Elucidating the design space of torque-aware vision-language-action models. <u>arXiv preprint arXiv:2509.07962, 2025c.</u> 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual 

12 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

## **A. Data Collection** 

### **A.1. VR Teleoperation System** 

Our robot is as shown in Figure. 6. To collect high-quality human demonstration data, we develop a VR-driven fullbody teleoperation system using the Meta Oculus Quest 3 as the unified interface for controlling both robot arms and the active head as shown in Figure 7. The Quest 3 provides precise 6-DoF tracking and responsive controller input, enabling natural and coordinated bimanual operation. For arm manipulation, the operator wears a full-scale bimanual exoskeleton, inspired by GELLO (Wu et al., 2024), which establishes a joint-to-joint kinematic mapping from the operator to the robot’s dual 7-DoF humanoid arms. The Quest 3 tracks the operator’s global pose and controller actions, which are fused with exoskeleton data in the control workstation to generate smooth and human-like trajectories. For head control, the Quest 3 is likewise used as the main interaction device. Instead of streaming head pose or performing inside-VR rendering (Xiong et al., 2025; Zeng et al., 2025), we map the robot head’s pan–tilt actions to designated Quest 3 controller buttons, allowing the operator to adjust the robot’s viewpoint in a stable, discrete, and lowlatency manner. Crucially, to ensure minimal latency, high stability, and accurate visual alignment, we do not stream any robot camera views or rendered UI into the VR headset (Zeng et al., 2025; Xiong et al., 2025). All visual feedback—including wrist-mounted and head-mounted RGB-D camera feeds—is displayed exclusively on a monitor connected to an external teleoperation workstation. During demonstration collection, both the robot and the Quest 3 connect directly to this workstation, which acts as a unified hub for sensor fusion, control synchronization, and real-time visualization. This design avoids the additional encoding, wireless streaming, and rendering delays that VR-inheadset display would introduce, resulting in a significantly more responsive teleoperation loop. This VR-assisted but monitor-viewed teleoperation architecture provides a stable, low-latency, and highly controllable setup for collecting precise, human-aligned manipulation demonstrations. 


_Figure 6._ Illustration of our self-designed robot construction. 


_Figure 7._ Illustration of the designed VR teleoperation System using Meta Oculus Quest 3. 

### **A.2. Real World Data Quality Review** 

To ensure the reliability of teleoperated demonstrations collected in real-world settings, we conduct a frame-by-frame, trajectory-level data quality review. This manual inspection is designed to filter out sequences affected by latency, sensor artifacts, operator mistakes, or camera capture inconsistencies. We define a set of deterministic rules to evaluate each trajectory: 

_1) Excessive Actuation Latency._ Both gripper and joints commands are monitored for temporal alignment. Any sequence exhibiting _≥_ 300 ms delay between user input and recorded robot actuation is marked invalid, as such latency typically arises from communication bottlenecks or onboard processing delays and leads to distorted motion supervision. 

_2) Unintentional Gripper Oscillation._ Gripper trajectories containing rapid, continuous open–close toggling are flagged as operator mis-triggers and discarded, as these patterns do not reflect meaningful manipulation intent. 

_3) Gripper Value Spikes._ The gripper sensor normally outputs values within the 0–1000 range. We label as corrupted any trajectory containing systematic spiking ( _e.g._ , 1001–1010) caused by low-level hardware protocol noise or overflow. Such discontinuities compromise the smoothness required for imitation learning. 

_4) Camera View Contamination._ Demonstrations are rejected if the robot cameras capture large human-body intrusions, missing robot arms, or severe motion blur from aggressive operator movement. These issues hinder visual–kinematic alignment and degrade learning. 

_5) Invalid Reach Strategy._ For humanoid-arm grasping, we enforce a consistent approach strategy. Specifically, trajectories employing top-down, table-type grasping are filtered 

13 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

out, as such motions contradict the intended horizontal, inhand-level grasping typical for humanoid robots and lead to inconsistent action patterns. 

_6) Video–Joint Stream Misalignment (Frame Dropping)._ Raw RGB-D recordings are capped at 25 FPS. Any sequence with _≥_ 2.5 dropped frames is removed to avoid misalignment between visual frames and joint trajectories, which is critical for paired multimodal supervision. 

Across all criteria, the review ensures that only temporally aligned, semantically valid, and visually consistent demonstrations enter the training set, forming a stable foundation for robust real-world robot learning. 

### **A.3. Real-World Data Statistics** 

The real-world evaluation benchmark comprises five challenging _out-of-vision_ Pick-and-Place (PnP) tasks, designed to systematically evaluate manipulation under partial observability. The five tasks include _Invisible-to-Invisible PnP_ , _Visible-to-Invisible PnP_ , _Invisible-to-Visible PnP_ , _Sequential Dual-Object PnP_ , and _Dual-Arm Coordination PnP_ , each emphasizing a different form of spatial memory usage. 

_1) Invisible-to-Invisible PnP_ requires the robot to grasp a target object that is outside the current field of view and place it at a target location that is also outside the field of view, testing the ability to operate entirely beyond direct visual observation. 

_2) Visible-to-Invisible PnP_ involves grasping a target object that is initially visible and placing it at a target location outside the current view, evaluating whether spatial information about unseen goal locations can be recalled and utilized. 

_3) Invisible-to-Visible PnP_ requires the robot to grasp an object that is initially outside the field of view and place it at a visible target location, testing spatial recall of unseen objects followed by precise execution. 

_4) Sequential Dual-Object PnP_ extends the setting to multistage manipulation: the robot first performs pick-and-place for a visible object, and subsequently grasps and places a second object located outside the field of view, stressing memory persistence across sequential task stages. 

_5) Dual-Arm Coordination PnP_ represents the most challenging scenario, where both the target object and target placement location are outside the field of view, and successful execution requires coordinated dual-arm handover followed by accurate placement based on a globally consistent spatial representation. 

Each task involves three distinct objects and was collected with 400 expert demonstrations. The raw data is downsampled by a factor of two, resulting in 711 _,_ 524 frames at an average frame rate of 12 _._ 74 Hz, corresponding to approxi- 

mately 15 _._ 52 hours of expert demonstrations. It provides a structured real-world benchmark for evaluating spatial memory and manipulation behavior when both objects and goals may lie outside the robot’s immediate field of view. 

## **B. Methods** 

### **B.1. Data Preprocess** 

As we mentioned in Section 4.2, we accelerate the whole training process by abstract the pipeline of semantics processing by utilizing the series of external powerful perception models (Wang et al., 2025b; Cheng et al., 2024; Simeoni´ et al., 2025) as shown in Algorithm 1. In detailed, To efficiently construct the overview scene memory used by **_SOMA_** , we adopt an offline preprocessing pipeline that extracts spatial–semantic evidence from both the scanning phase and the manipulation phase of each trajectory. For each trajectory _τ_ , the process begins by generating the overview memory from the head-camera scanning video. Given a scanning sequence _V_<sup>(</sup><sup>_τ_)</sup> , we uniformly sample frames every ( _N/_ 3) steps to obtain a reduced subset _V_ ˜<sup>(</sup><sup>_τ_)</sup> = _{fi | i_ mod ( _N/_ 3) = 0 _}_ that balances spatial coverage with computational efficiency. Each sampled frame is then processed through a unified perception stack—the geometry prior Φgeo, the object detector _Y_ , and the semantic encoder Φsem, which extract instance-level embeddings **f** _j_<sup>(</sup><sup>_i_),</sup> categorical labels _c_<sup>(</sup> _j_<sup>_i_), and their corresponding 3D bound-</sup> ing boxes **b**<sup>(</sup> _j_<sup>_i_).These multi-view instances are aggregated</sup> across the entire scanning sequence and fused into the initial overview instance record _R_<sup>(</sup> sparse<sup>_τ_)[0],which provides a</sup> compact yet globally consistent summary of the scene. 

After establishing the overview memory, we process the manipulation segment of each trajectory. Instead of extracting features at every timestep—which would incur excessive computational overhead—we again apply uniform subsampling, selecting only frames whose manipulation step index satisfies _t_ mod _N_ = 0. For each such sampled frame _ft_ , we run the same perception pipeline to obtain the triplet ( **f**<sup>(</sup><sup>_t_)</sup> _, c_<sup>(</sup><sup>_t_)</sup> _,_ **b**<sup>(</sup><sup>_t_)</sup> ), storing it in the sparse record _R_<sup>(</sup> sparse<sup>_τ_)[</sup><sup>_t_].This strategy captures the temporal evolution of</sup> key task-relevant objects while significantly reducing preprocessing cost, and empirically preserves all information needed for effective memory refinement during policy execution. 

Finally, to ensure that every timestep in the trajectory is paired with a valid memory observation during training, we perform a back-mapping procedure that expands the sparse record into a dense per-step memory sequence. For each timestep _t_ in the full trajectory, we identify the nearest sampled index _t_<sup>_′_</sup> = _⌊t/N ⌋· N_ and assign its stored evidence to the current step, i.e., _R_<sup>(</sup> _t_<sup>_τ_)</sup> _←R_<sup>(</sup> sparse<sup>_τ_)[</sup><sup>_t′_].This</sup> 

14 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

**Algorithm 1** MEMORYPREPROCESS: Offline Extraction of Spatial–Semantic Evidence 

**Input:** Dataset _D_ , sampling interval _N_ , batch size _B_ , geometry prior Φgeo, detector _Y_ , semantic encoder Φsem **Output:** Per-step memory evidence _{R_<sup>(</sup> _t_<sup>_τ_)</sup> _}_ for all trajectories 

**for** each trajectory _τ_ in _D_ **do** Initialize sparse record _R_<sup>(</sup> sparse<sup>_τ_)</sup><sup>_←∅_</sup> **(1) Overview Memory from Scanning Video (** _t_ =0 **)** Sample overview frames _V_<sup>˜(</sup><sup>_τ_)</sup> = _{fi | i_ mod ( _N/_ 3) = 0 _}_ **for** each batch _{fi}_ of size _B_ in _V_<sup>˜(</sup><sup>_τ_)</sup> **do** Extract object features ( **F** _, C_ obj) _←_ Φsem _, Y_ ( _fi_ ) Lift boxes to 3D _B_ 3 _D ←_ Φgeo( _fi_ ) Accumulate instance triplets ( **f** _j_<sup>(</sup><sup>_i_)</sup><sup>_, c_(</sup> _j_<sup>_i_)</sup><sup>_,_</sup><sup>**b**(</sup> _j_<sup>_i_))</sup> **end for** Fuse all instances _R_<sup>(</sup> sparse<sup>_τ_)[0]</sup><sup>_←_FUSE(</sup><sup>_{_</sup><sup>**f**(</sup> _j_<sup>_i_)</sup><sup>_}_)</sup> **(2) Per-step Frame Sampling (Manipulation)** Sample manipulation steps _S_<sup>˜(</sup><sup>_τ_)</sup> = _{t | t_ mod _N_ = 0 _}_ **for** each _t ∈ S_<sup>˜(</sup><sup>_τ_)</sup> with _t >_ 0 **do** Process frame _ft_ ( **f**<sup>(</sup><sup>_t_)</sup> _, c_<sup>(</sup><sup>_t_)</sup> _,_ **b**<sup>(</sup><sup>_t_)</sup> ) _←_ Φsem _, Y,_ Φgeo( _ft_ ) Store sparse evidence _R_<sup>(</sup> sparse<sup>_τ_)[</sup><sup>_t_]</sup><sup>_←_(</sup><sup>**f**(</sup><sup>_t_)</sup><sup>_, c_(</sup><sup>_t_)</sup><sup>_,_</sup><sup>**b**(</sup><sup>_t_))</sup> **end for (3) Back-mapping to All Steps for** each step _t_ in trajectory _τ_ **do** Find closest sampled step _t_<sup>_′_</sup> = _⌊t/N ⌋· N R_<sup>(</sup> _t_<sup>_τ_)</sup> _←R_<sup>(</sup> sparse<sup>_τ_)[</sup><sup>_t′_]</sup> **end for end for Return:** _{R_<sup>(</sup> _t_<sup>_τ_)</sup> _}_ for all trajectories 

back-mapping guarantees temporal consistency and avoids missing-memory cases, while keeping the computational load tied only to the sampled frames. The resulting dense instance record _{R_<sup>(</sup> _t_<sup>_τ_)</sup> _}_ serves as the input for _Spatial Memory Construction_ during training, enabling **_SOMA_** to learn manipulation policies grounded on structured, geometry-aware, and temporally coherent environmental context. 

### **B.2. Framework Details** 

We employs a set of purpose-built neural modules that support geometric encoding, semantic abstraction, temporal fusion, and memory–VLM interaction, all of which are essential for enabling SOMA’s spatial memory–driven OOV manipulation pipeline, as summarized in Table 6. 

**3D BBox Embedding MLP.** This module transforms each 

|**3D BBox Embedding MLP (**Φ**pos)**|
|---|
|LayerNorm(8_×_3), Linear(24_→_768)→GELU<br>Linear(768_→_768)→GELU, Linear(768_→_384)→GELU, LayerNorm384|
|**Spatial Positional Refinement**|
|LayerNorm384, Linear(384_→_768)→GELU<br>Linear(768_→_768)→GELU, Linear(768_→_384)→GELU, LayerNorm384|
|**Memory Feature Projection (**Φ**mem)**|
|LayerNorm384, Linear(384_→_768)→GELU<br>Linear(768_→_384)→GELU, LayerNorm384|
|**Similarity Network (**Φ**sim)**|
|LayerNorm(3_×_384), Linear(1152_→_768)→GELU<br>Linear(768_→_384)→GELU LayerNorm384|
|, <br>**Fusion Network (**Φ**fuse)**|
|LayerNorm(2_×_384), Linear(768_→_384)→GELU<br>Linear(384_→_384)→GELU, LayerNorm384|
|**Memory–VLM Alignment MLP (**Φ**align)**|
|LayerNorm384, Linear(384_→_768)→GELU<br>Linear(768_→d_VLM)→GELU, LayerNorm_d_VLM|
|**Memory–Token Transformer (3 Layers)**|
|Self-Attention Transformer (3 layers)<br>32 Heads, Head Dim = 64<br>Dropout = 0.2, Final Dropout = True|


_Table 6._ Architectures of the modules used for spatial–semantic embedding, memory refinement, and contextual retrieval. 


_Figure 8._ Analysis about time and gpu cost per demo of different component choice in _the memory preprocess stage_ . 

raw 3D bounding box **b** _k ∈_ R<sup>8</sup><sup>_×_3</sup> into a stable spatial descriptor **p** _k_ = Φpos( **b** _k_ ). It is used in _Spatial Memory Construction_ to encode viewpoint-invariant geometry, ensuring that all instances are anchored in a consistent spatial reference frame. 

**Spatial Positional Refinement.** A second-stage MLP refines **p** _k_ to suppress geometric noise from multi-view lifting. This step increases the reliability of positional embeddings before they are fused into the memory tokens. 

**Memory Feature Projection.** The projection module Φmem maps visual embeddings **f** _k_ into the memory space and combines them with **p** _k_ to form the unified memory tokens **m**<sup>0</sup> _k_<sup>.Thismoduleestablishesaconsistentrepresentation</sup> format for _Spatial Memory Construction_ and ensures that semantics and geometry are jointly encoded. 

**Similarity and Fusion MLP.** During _Dynamic Memory Refinement_ , two compact MLPs compute a semantic similarity score _s_<sup>_t_</sup> _kj_<sup>and a fusion confidence score</sup><sup>_g_</sup> _kj_<sup>_t_between histor-</sup> ical memory and new observations. Their product defines an adaptive update weight _αkj_<sup>_t_, enabling selective memory</sup> 

15 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

|**Category**|**Details**|
|---|---|
|**Container Interaction**|**Tasks:** Cup→Drawer, Potato/Milk→Microwave, Bottle/Wine/Can→Cabinet.<br>**Summary:** Multi-stage pick–place–close interactions with drawers, cabinets, or mi-<br>crowaves, evaluating sequential manipulation and spatial planning.|
|**Cooking Preparation**|**Tasks:** Cuttingboard→Basket/Pan/Pot/Tieredbasket.<br>**Summary:** Transfers ingredients from a cutting board into cookware, testing grasp<br>stability and pre-cooking preparation skills.|
|**Tabletop Serving**|**Tasks:** Placemat→Bowl/Plate/Tieredshelf.<br>**Summary:** Serving-like actions placing items from a placemat to tableware; empha-<br>sizes precise placement and tabletop spatial reasoning.|
|**Dish Transfer**|**Tasks:** Plate→Bowl/Box/Pan/Plate.<br>**Summary:** Transfers items between dishware during dining or cleanup, evaluating<br>fine-grained control and container-to-container reasoning.|
|**Tray Organization**|**Tasks:** Tray→Plate/Pot/Tieredbasket/Tieredshelf.<br>**Summary:** Organizes items from a tray into various structured storages, testing multi-<br>target placement and organization planning.|


_Table 7._ Summary of task categories in the Robocasa Tabletop GR1 benchmark. 

||**Task Name**|**# Variations**|
|---|---|---|
||Spoon On Tower|1|
|_Bridge_|Carrot On Plate<br>Stack Cube|1<br>1|
||Eggplant In Basket|1|
||Pick Coke Can|VM: 12 / VA: 33|
|_Ftl_|Move Near|VM: 4 / VA: 10|
|_raca_|Open/Close Drawer|VM: 216 / VA: 42|


_Table 8._ SimplerEnv task details. “VM” denotes visual-matching and “VA“ denotes variant-aggregation. Bridge tasks use a single configuration; Fractal tasks report VM and VA separately. 

refinement that is stable under minor viewpoint change yet responsive to true scene updates. 

**Memory–VLM Alignment MLP.** This module projects memory tokens into the VLM backbone’s feature space. It provides the key–value representation for _Contextual Memory Retrieval_ , ensuring that the memory can be directly queried by instruction-conditioned visual–linguistic tokens. 

**Memory–Token Transformer.** A lightweight attention transformer performs cross-modal interaction between the aligned memory and VLM tokens. This component injects global spatial–semantic structure into the VLM representation, producing the memory-boosted feature **X** boost that conditions the downstream DiT action predictor. 

## **C. Realworld Evaluation** 

As shown in Figure 9, we add more example with different object manipulation on our self-designed out-of-vision tasks including (1) Sequential Dual-Object and (2) Dual-Arm Coordination. 

## **D. Simulation Experiments** 

### **D.1. Benchmarks** 

**Robocasa Tabletop GR1.** This dataset provides a digital analogue to real-world humanoid demonstrations, enabling systematic evaluation prior to deployment on physical robots (Bjorck et al., 2025; Nasiriany et al., 2024). It features tabletop rearrangement tasks executed by the GR-1 humanoid robot equipped with Fourier dexterous hands, emphasizing dexterous hand–arm coordination under diverse tabletop settings. The GR-1 benchmark contains a substantially broader variety of objects, receptacles, and spatial configurations. As shown in Table 7, the dataset consists of 24 manipulation tasks, which can be organized into the following categories based on the underlying interaction structure: 

_1) Container Interaction Tasks_ (e.g., placing items into cabinets, drawers, or microwaves and subsequently closing them), testing multi-stage pick–place–close behaviors with articulated receptacles. 

_2) Cooking Preparation Tasks_ (e.g., transferring objects from a cutting board into pans, pots, or baskets), simulating preparatory cooking steps that require stable grasping and reliable object placement. 

_3) Tabletop Serving Tasks_ (e.g., moving items from a placemat to bowls or plates), capturing serving-style behaviors that depend on precise spatial reasoning. 

_4) Dish Transfer Tasks_ (e.g., moving objects between dishware such as plate→bowl), evaluating fine-grained coordination during mid-meal or cleanup scenarios. 

_5) Tray Organization Tasks_ (e.g., transporting items from a tray to multi-level shelves or containers), assessing multitarget placement and organized spatial planning. 

16 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

||**Diffu**|**sion Po**|**licy**(Chi|et al.,2025)|**GR00**|**T N1.**|**5**(Bjorck|et al.,2025)||**SOMA**|**(Ours)**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Task Category**|30|100|300|Full|30|100|300|Full|30|100|300|Full|
|CupToDrawerClose|24.5|32.4|36.3|–|34.0|44.0|44.0|44.0|60.0|46.0|46.0|60.0|
|PotatoToMicrowaveClose|17.7|30.4|41.2|–|24.0|26.0|32.0|28.0|36.0|44.0|54.0|34.0|
|MilkToMicrowaveClose|37.3|41.2|51.0|–|58.0|46.0|54.0|44.0|54.0|44.0|55.0|64.0|
|BottleToCabinetClose|40.2|62.8|60.8|–|44.0|22.0|32.0|40.0|62.0|72.0|80.0|64.0|
|WineToCabinetClose|43.1|55.9|60.8|–|28.0|34.0|34.0|44.0|52.0|52.0|56.0|64.0|
|CanToDrawerClose|48.0|74.5|75.5|–|24.0|33.0|36.0|42.0|50.0|54.0|58.0|54.0|
|**Container Interaction**|35.1|49.5|54.3|–|35.3|33.7|35.7|40.3|52.3|52.0|53.3|55.7|
|CuttingboardToBasket|19.6|42.2|29.4|–|38.0|42.0|50.0|42.0|32.0|56.0|56.0|38.0|
|CuttingboardToCardboardbox|11.8|15.7|22.6|–|36.0|40.0|50.0|36.0|48.0|40.0|32.0|44.0|
|CuttingboardToPan|28.4|48.0|57.8|–|62.0|68.0|46.0|74.0|56.0|50.0|52.0|62.0|
|CuttingboardToPot|22.6|37.3|48.0|–|48.0|40.0|46.0|74.0|46.0|46.0|52.0|42.0|
|CuttingboardToTieredbasket|13.7|13.7|18.6|–|20.0|36.0|28.0|52.0|36.0|62.0|50.0|48.0|
|**Cooking Preparation**|19.2|31.4|35.3|–|40.8|45.2|42.8|49.2|43.6|50.8|48.4|46.4|
|PlacematToBasket|15.7|25.5|41.2|–|38.0|46.0|42.0|34.0|36.0|48.0|44.0|42.0|
|PlacematToBowl|14.7|18.6|23.5|–|52.0|54.0|62.0|28.0|64.0|50.0|58.0|54.0|
|PlacematToPlate|15.7|23.5|37.3|–|54.0|52.0|52.0|56.0|54.0|54.0|56.0|72.0|
|PlacematToTieredshelf|6.9|5.9|11.8|–|20.0|28.0|38.0|56.0|24.0|34.0|58.0|22.0|
|**Tabletop Serving**|13.2|18.4|28.4|–|41.0|47.5|48.5|39.5|44.5|46.5|54.0|47.5|
|<br>PlateToBowl|15.7|18.6|31.4|–|48.0|50.0|44.0|26.0|62.0|56.0|52.0|48.0|
|PlateToCardboardbox|12.8|13.7|27.5|–|32.0|52.0|52.0|54.0|46.0|52.0|54.0|34.0|
|PlateToPan|13.7|17.7|35.3|–|48.0|60.0|38.0|46.0|54.0|58.0|46.0|68.0|
|FromPlateToPlate|25.5|39.2|61.8|–|50.0|72.0|38.0|74.0|70.0|66.0|68.0|48.0|
|**Dish Transfer**|16.9|22.3|39.0|–|44.0|58.5|51.0|50.0|58.0|58.0|55.0|49.5|
|TrayToCardboardbox|21.6|37.3|40.2|–|32.0|40.0|44.0|66.0|46.0|34.0|56.0|60.0|
|TrayToPlate|26.5|41.2|49.0|–|54.0|58.0|46.0|44.0|52.0|52.0|58.0|68.0|
|TrayToPot|21.6|48.0|52.9|–|42.0|44.0|46.0|52.0|52.0|32.0|56.0|40.0|
|TrayToTieredbasket|12.8|34.3|39.2|–|30.0|34.0|56.0|46.0|50.0|50.0|52.0|48.0|
|TrayToTieredshelf|2.0|6.9|15.7|–|22.0|24.0|26.0|30.0|16.0|22.0|22.0|32.0|
|**Tray Organization**|15.7|32.6|39.2|–|36.0|40.0|43.6|50.8|43.2|38.0|48.8|47.6|
|**Average**|**20.1**|**30.8**|**39.2**|**–**|**39.4**|**45.0**|**44.3**|**46.0**|**48.3**|**49.1**|**51.9**|**49.3**|


_Table 9._ Performance comparison via success rate (%) across task categories on the Robocasa Tabletop GR-1 benchmark with varying numbers of demonstrations per task. Diffusion Policy is only evaluated under 30/100/300 settings. 

Most tasks involve distractor objects and unseen combinations of source–target receptacles, requiring the policy to interpret task language and adapt to novel rearrangement structures. The tasks closely follow the rearrangement pattern introduced in pre-training—moving objects from a source region to a target receptacle—yet deployment settings and object pairings are deliberately held out to test generalization. The observation space consists of a single egocentric RGB view obtained from the robot’s head-mounted camera. The state space includes the 3D joint positions and orientations of both arms and dexterous hands, as well as waist and neck control. End-effector–based actions are also provided as an alternative control interface for whole-body IK. 

**SimplerEnv.** As shown in Table 8, the SimplerEnv benchmark comprises two complementary suites: Bridge and Fractal. The Bridge suite contains four tabletop manipulation tasks executed on a WidowX robot— _Spoon on Towel, Carrot on Plate, Stack Cube, and Eggplant in Basket._ Each task is associated with a single language instruction template and centers on core object-placement and stacking primitives, offering a clean, controlled evaluation setup. The Fractal suite builds on the RT-1 dataset collected with the Google 

robot and defines three additional tasks: _Pick Coke Can, Move Near, Open/Close Drawer._ Each task is evaluated under two protocols. Visual Matching (VM) approximates real-world deployment by varying object configurations and URDF assets to ensure consistency between simulation and physical execution. Variant Aggregation (VA) introduces extensive visual perturbations—spanning background changes, texture shifts, lighting variations, distractors, and camera viewpoint alterations—to rigorously stress-test robustness and generalization. _In this paper, we utilize the Fractal suite to assess our memory design._ 

### **D.2. Behavioral Metric Definitions** 

To better understand how spatial memory influences manipulation behavior under partial observability, we report a set of behavioral metrics in Table 1. All metrics are computed per episode and then averaged over 20 evaluation episodes for each task. 

_1) First-Fixation Time._ First-Fixation Time measures the temporal latency between the moment the target object first enters the head camera’s field of view and the initiation of the robot’s grasping motion. Specifically, it is defined as the 

17 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

||**Up**|**date Strate**|**gy**||**Retrieva**|**l Modul**|**e**|**Mem**|**ory Rep**|**resentation**||
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Task Category**|SimEMA|Only_s_<sup>_t_</sup><br>_kj_|Only_g_<sup>_t_</sup><br>_kj_|Concat|Light|Heavy|Middle|Obj.|Geo.|NoUpd|**Full**|
|CupToDrawerClose|25.0|25.0|25.0|50.0|42.0|43.0|60.0|35.0|45.0|45.0|60.0|
|PotatoToMicrowaveClose|25.0|50.0|20.0|20.0|25.0|25.0|34.0|30.0|20.0|25.0|34.0|
|MilkToMicrowaveClose|60.0|45.0|50.0|35.0|30.0|30.0|64.0|60.0|40.0|45.0|64.0|
|BottleToCabinetClose|20.0|45.0|20.0|40.0|50.0|40.0|64.0|30.0|40.0|30.0|64.0|
|WineToCabinetClose|45.0|25.0|35.0|35.0|35.0|35.0|54.0|45.0|25.0|20.0|54.0|
|CanToDrawerClose|15.0|25.0|25.0|25.0|40.0|30.0|58.0|25.0|30.0|25.0|58.0|
|**Container Interaction**|31.7|35.8|29.2|34.2|37.0|33.8|55.7|37.5|33.3|31.7|55.7|
|CuttingboardToBasket|55.0|50.0|50.0|25.0|35.0|45.0|38.0|45.0|35.0|40.0|38.0|
|CuttingboardToCardboardbox|60.0|40.0|40.0|45.0|50.0|60.0|44.0|35.0|55.0|25.0|44.0|
|CuttingboardToPan|65.0|65.0|50.0|55.0|60.0|45.0|60.0|70.0|75.0|60.0|60.0|
|CuttingboardToPot|55.0|50.0|50.0|65.0|40.0|60.0|42.0|55.0|60.0|65.0|42.0|
|CuttingboardToTieredbasket|25.0|40.0|45.0|30.0|30.0|30.0|48.0|15.0|25.0|40.0|48.0|
|**Cooking Preparation**|52.0|49.0|47.0|44.0|43.0|48.0|46.4|44.0|50.0|46.0|46.4|
|PlacematToBasket|50.0|15.0|50.0|45.0|35.0|40.0|42.0|40.0|45.0|45.0|42.0|
|PlacematToBowl|35.0|55.0|60.0|70.0|65.0|70.0|54.0|45.0|50.0|45.0|54.0|
|PlacematToPlate|35.0|55.0|80.0|60.0|50.0|60.0|72.0|65.0|50.0|40.0|72.0|
|PlacematToTieredshelf|10.0|10.0|25.0|40.0|10.0|25.0|22.0|20.0|35.0|25.0|22.0|
|**Tabletop Serving**|32.5|33.8|53.8|53.8|40.0|48.8|47.5|42.5|45.0|38.8|47.5|
|PlateToBowl|35.0|55.0|50.0|55.0|40.0|55.0|48.0|60.0|45.0|45.0|48.0|
|PlateToCardboardbox|35.0|25.0|55.0|40.0|55.0|55.0|34.0|45.0|50.0|35.0|34.0|
|PlateToPan|30.0|50.0|50.0|50.0|40.0|55.0|58.0|50.0|35.0|50.0|58.0|
|FromPlateToPlate|65.0|50.0|60.0|60.0|60.0|65.0|58.0|70.0|45.0|70.0|58.0|
|**Dish Transfer**|41.2|45.0|53.8|51.2|48.8|57.5|49.5|56.2|43.7|50.0|49.5|
|TrayToCardboardbox|40.0|35.0|55.0|50.0|50.0|40.0|60.0|55.0|35.0|40.0|60.0|
|TrayToPlate|55.0|60.0|45.0|65.0|50.0|50.0|68.0|55.0|70.0|50.0|68.0|
|TrayToPot|55.0|35.0|60.0|55.0|45.0|50.0|40.0|45.0|50.0|40.0|40.0|
|TrayToTieredbasket|45.0|45.0|40.0|35.0|60.0|20.0|48.0|40.0|45.0|40.0|48.0|
|TrayToTieredshelf|35.0|20.0|5.0|25.0|25.0|15.0|22.0|40.0|20.0|35.0|22.0|
|**Tray Organization**|47.5|40.0|37.5|45.0|45.0|33.7|47.6|45.0|46.2|41.2|47.6|
|**Average**|**41.0**|**40.7**|**44.2**|**45.6**|**42.8**|**44.4**|**49.3**|**45.1**|**43.7**|**41.5**|**49.3**|


_Table 10._ Detailed Ablation studies on Robocasa Tabletop GR-1 benchmark. We compare different Update Strategies, Retrieval Modules, and Memory Representations. Reported values are success rates (%). “SimEMA” denotes the normal EMA update (Chen et al., 2020), _s_<sup>_t_</sup> _kj_ denotes semantic similarity, _gkj_<sup>_t_denotes dynamic fusion scores, ”Concat” denotes naive fusion of perception tokens and memory features</sup> ”Light/Middle/Heavy” use 2/3/4 cross-attention layers. ”Geo.” and ”Obj.” denote Geometric cues and object semantics, respectively. “NoUpd” denotes the memory representation without updating with latest observations. 

|**Task Category**|**Fram**|**e Samp**|**ling In**|**terval**|
|---|---|---|---|---|
||10|20|30|40|
|Container Interaction|41.7|**55.7**|38.7|35.7|
|Cuttingboard-Origin|45.6|**46.4**|45.2|45.2|
|Placemat-Origin|45.5|**47.5**|44.5|44.0|
|Plate-Origin|50.5|49.5|50.0|**52.0**|
|Tray-Origin|41.0|**47.6**|46.0|45.2|
|**Average**|44.9|**49.3**|44.9|44.4|


_Table 11._ Ablation Study of different processing interval choices in _Spatial Memory Construction_ . The interval controls the frame sampling frequency from scanning sequences. 

duration (in seconds) from the first frame in which the target becomes visually observable to the timestamp at which the arm begins the grasp execution. This value is determined through offline human annotation of recorded trajectories to ensure high-fidelity temporal accuracy independent of the robot’s control frequency. Lower values indicate a faster transition from visual acquisition to physical manipulation, 

reflecting more decisive and well-grounded behavior. 

_2) Head Search Path Length._ Head Search Path Length measures the total amount of head motion required to bring the target object into view. Let _t ∈{_ 0 _,_ 1 _, . . . , T −_ 1 _}_ index environment steps in an episode, and let ( _ψt, ϕt_ ) denote the head pan (yaw) and tilt (pitch) angles at step _t_ , measured in degrees. Let _t_ vis denote the step at which the target object first becomes visible in the head camera view, as determined by offline annotation. The Head Search Path Length is defined as the cumulative angular displacement of the head prior to target visibility: 


Smaller values indicate more efficient viewpoint search with less unnecessary head motion. 

_3)Viewpoint Correction Count._ Viewpoint Correction Count counts the number of discrete head reorientation events performed after the target object has already been observed 

18 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

at least once. Each correction corresponds to a change in head motion direction intended to re-center or re-acquire the target. This metric captures the stability of target localization, where fewer corrections imply more consistent spatial grounding. 

_4) Grasp Attempt Count._ Grasp Attempt Count measures the number of grasp executions issued by the controller until a successful grasp is achieved. Each grasp attempt is defined as a completed gripper closing action. Lower values indicate more reliable target localization and manipulation, with values close to one corresponding to near one-shot grasping behavior. 

_5) Time-to-Grasp._ Time-to-Grasp measures the total number of environment steps from episode start until a successful grasp is completed. This metric aggregates both perception and manipulation efficiency, reflecting the overall speed of task execution under partial observability. 

### **D.3. Quantitative Results** 

As shown in Table 9, SOMA achieves SOTA performance on the RoboCasa Tabletop GR-1 benchmark across all data regimes. Importantly, this benchmark operates under static observability, where all task-relevant objects are visible, allowing us to isolate the effect of the spatial memory design independent of viewpoint acquisition. SOMA attains the highest overall average success rate, reaching 49.3% under the full-data setting, outperforming both GR00T-N1.5 (46.0%) and Diffusion Policy (39.2% under 300-shot). Beyond absolute performance, SOMA exhibits markedly improved sample efficiency. With only 30 demonstrations per task, SOMA already achieves an average success rate of 48.3%, surpassing GR00T-N1.5 trained on the full dataset. This advantage is consistent across task categories, with particularly strong gains in _Container Interaction_ (55.7% vs. 40.3% for GR00T-N1.5 under full data), which involves multi-step manipulation and structured object–receptacle relationships. These results indicate that SOMA’s spatial memory—through explicit scene representation and instructionconditioned retrieval—provides a more structured inductive bias for manipulation. Even when all objects are directly observable, maintaining and querying a global spatial–semantic memory leads to more stable learning and better generalization than purely reactive policies. 

### **D.4. Qualitative Results** 

The qualitative results of _GR1 benchmark_ (Bjorck et al., 2025; Nasiriany et al., 2024) and _SimplerEnv Fractal_ (Li et al., 2024; Zitkovich et al., 2023) are as shown in Figure (10,11). 

### **D.5. Detailed Ablation Study** 

We further expand our ablation analysis from the coarse summary in Table (5) to a fine-grained breakdown in Table 10, complemented by the efficiency study in Fig. 8 and the sampling-interval analysis in Table 11. Together, these results substantiate the effectiveness of SOMA by isolating the gains from its key designs— _Dynamic Memory Refinement_ , _Contextual Memory Retrieval_ , and the spatial–semantic memory representation—while also clarifying the associated computational trade-offs and the impact of memory construction frequency. 

**Dynamic Memory Refinement.** Comparing the _Update Strategy_ variants, the _Full_ method (Average: 49.3%) significantly outperforms the baselines (SimEMA: 41 _._ 0%, Only _s_<sup>_t_</sup> _kj_<sup>:40</sup><sup>_._7%,Only</sup><sup>_g_</sup> _kj_<sup>_t_:44</sup><sup>_._2%).Thisdemonstrates</sup> that the complete adaptive similarity-aware fusion mechanism—which leverages the product of semantic similarity ( _s_<sup>_t_</sup> _kj_<sup>)andlearneddynamicfusionscore(</sup><sup>_g_</sup> _kj_<sup>_t_),</sup><sup>_α_</sup> _kj_<sup>_t_=</sup> _gkj_<sup>_t· st_</sup> _kj_<sup>—is essential for maintaining global memory con-</sup> sistency and temporal coherence. Specifically, relying solely on semantic similarity ( _s_<sup>_t_</sup> _kj_<sup>) or dynamic confidence (</sup><sup>_g_</sup> _kj_<sup>_t_) re-</sup> sults in a performance drop of approximately 8 _._ 6% _∼_ 8 _._ 3% in average success rate, confirming that the _joint, adaptive update coefficient_ is the most effective strategy for stabilizing the memory under continuous visual changes. 

**Contextual Memory Retrieval.** The performance of the _Retrieval Module_ shows a strong correlation with model capacity. The final _Full_ (Average: 49.3%) utilizes the _Middle_ module which employs a sufficient number of crossattention layers. The simpler _Light_ module (42 _._ 8%) and the naive _Concat_ fusion (45 _._ 6%) perform substantially worse. Although _Heavy_ achieves a competitive 44 _._ 4%, the _Middle_ config achieves the optimal balance between performance and architectural complexity, suggesting that three crossattention layers are adequate for effectively integrating the queried scene memory ( _M_<sup>ˆ</sup> _t_ ) into the VLM’s perception tokens to achieve instruction-grounded spatial reasoning. 

**Memory Representation.** Analysis of the _Memory Representation_ confirms the necessity of integrating both geometric and semantic priors. The full representation (Full: 49.3%)—which couples appearance features ( **f** _k_ ) with 3D spatial encodings ( **p** _k_ )—significantly outperforms variants that omit critical information: _Geo._ (43 _._ 7%): Omitting object semantics (relying only on geometry/VLM features) leads to a 5 _._ 6% performance drop, highlighting that discriminative semantics (from YOLO/DINOv3) are crucial for robust object identification. _Obj._ (45 _._ 1%): Omitting 3D geometric cues (relying only on object features) results in a 4 _._ 2% drop, emphasizing that _geometric grounding_ (from VGGT) is indispensable for precise spatial reasoning and action generation in 3D space. Finally, _NoUpd_ (41 _._ 5%): Using the initial memory _M_ 0 without the _Dynamic Mem-_ 

19 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

|Method|Inference Latency (s / chunk)|
|---|---|
|StarVLA (Community,2026)|_∼_1.26|
|SpatialVLA (Qu et al.,2025)|_∼_1.45|
|GR00T-N1.5 (Bjorck et al.,2025)|_∼_1.30|
|SOMA (Ours)|_∼_1.58|


_Table 12._ Comparison of online inference latency across diverse VLA methods on real-world experiments. 

|**Geometry Source**|**OOV SR (%)**_↑_|**Latency (s)**_↓_|
|---|---|---|
|RGB-D + OpenCV fusion|22.6|0.18|
|VGGT geometry + pose|27.3|0.21|


_Table 13._ Ablation on geometry source and alignment strategy. We compare RGB-D based point cloud fusion with VGGT-predicted geometry in terms of OOV task performance and computational overhead. 

_ory Refinement_ process severely limits the agent’s ability to adapt to scene changes, resulting in the worst performance and confirming that _Dynamic Memory Refinement_ is necessary for dynamic environments. 

**Processing Intervals.** We analyzes the impact of different frame sampling intervals from _Spatial Memory Construction_ as shown in Table 11. Shorter intervals (10) result in redundant and noisy memory updates with a lower average success rate of 44.9%, while excessively large intervals (30/40) lead to sparse scene representations and degraded performance (44.9%/44.4%). An interval of 20 achieves the best balance between information density and temporal diversity, yielding the highest average SR of 49.3%, which confirms that moderate sampling facilitates more stable and informative spatial memory construction. We chose 20 as the sampling interval to obtain the superiority performance. 

**Memory Preprocess.** We further assess the cost of each module in the _memory preprocessing stage_ outlined in Section 4.2. As shown in Figure 8, removing VGGT (Wang et al., 2025b) (lacking geometric cues) reduces the runtime and GPU cost most significantly but causes a 4.2% performance drop, confirming geometry modeling as the dominant yet essential cost. Excluding DINOv3 (Simeoni et al.´ , 2025) (lacking object semantics) offers a smaller speedup but a larger accuracy loss (-5.6%), showing that semantic encoding is critical for maintaining spatial–semantic consistency despite moderate overhead. 

|**Failure Mode**|**Count**|**Prop.**|**Description**|
|---|---|---|---|
|Inaccurate Grasp Pose<br>Under Dynamic Viewpoint|12/25|48.0%|Shifting head-camera views during visual search degrade grasp<br>estimation, causing misaligned approach or gripper slippage<br>(most pronounced in Tasks 1, 3, 5 with extended head movement).|
|Placement Timing and<br>Precision Errors|8/25|32.0%|Policy misjudges release timing during memory-guided navigation;<br>memory-to-reality offsets accumulate for narrow receptacles.|
|Head–Arm Coordination|5/25|20.0%|Head orients toward one arm’s workspace while the other lacks|
|Mismatch|||visual guidance, causing failed handovers in dual-arm tasks (Task 5).|


_Table 14._ Failure mode analysis on real-world OOV tasks (25 sampled failed episodes, 5 per task). Failures predominantly arise when translating reliable spatial localization into accurate motor execution under dynamic viewpoints. 

|**Failure Mode**|**Count**|**Prop.**|**Description**|
|---|---|---|---|
|Noisy Spatial Tokens from|22/50|44.0%|VGGT geometry noise on thin/textureless objects propagates|
|Imperfect 3D Estimation|||through retrieval, misleading action prediction.|
|Irrelevant Memory|16/50|32.0%|Cross-attention activates task-irrelevant memory entries in|
|Activation During Retrieval|||multi-object scenes, diluting the action signal.|
|Lack of Task-Phase|12/50|24.0%|Object-level memory refinement cannot distinguish meaningful|
|Awareness in Memory|||state changes (e.g., drawer open vs. closed) from minor visual<br>variations, yielding no phase-transition signal in multi-stage tasks.|


_Table 15._ Failure mode analysis on the fully observable RoboCasa Tabletop GR1 simulation (50 sampled failures, 10 per category). Under full observability, failures reflect limitations of the memory mechanism itself rather than OOV conditions. 

magnitude as StarVLA (Community, 2026), SpatialVLA (Qu et al., 2025), and GR00T-N1.5 (Bjorck et al., 2025), indicating that the proposed spatial memory design does not impose prohibitive computational overhead during online execution. This allows SOMA to achieve improved manipulation performance without sacrificing practical inference efficiency. 

**Geometry Source and Alignment.** Table 13 compares RGB-D based point cloud fusion with VGGT-predicted geometry for spatial memory construction. Although RGB-D fusion leverages depth sensors, its end-to-end latency remains non-trivial due to multi-view point cloud registration and alignment, resulting in comparable preprocessing cost to VGGT-based geometry. More importantly, real-world depth measurements are subject to sensor noise, missing depth, and misalignment across viewpoints, which accumulate during fusion and degrade the geometric consistency of the global memory. This noisy and unstable geometry leads to less reliable spatial tokens and ultimately lower OOV success rates. In contrast, VGGT provides more stable cross-view geometry and pose estimates under active head motion, yielding higher task success despite similar preprocessing latency. These results suggest that, for OOV manipulation, geometric consistency is more critical than raw depth fidelity, motivating our choice of VGGT-based geometry for spatial memory construction. 

### **D.6. Latency Evaluation** 

Table 12 reports the online inference latency per action chunk for diverse VLA methods in real-world settings. Despite introducing additional parameters for spatial memory modeling and geometry-aware perception, SOMA operates at a comparable inference speed to prior VLA baselines. The measured latency remains within the same order of 

### **D.7. Failure Case Analysis** 

To better understand the limitations of our approach, we collected 25 representative failed trajectories from real-world OOV tasks (5 per task) and 50 from the fully observable RoboCasa Tabletop GR1 simulation (10 per category), each with full recordings and memory states. As summarized in 

20 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 

Table 14, the dominant real-world failures stem from executing precise manipulation during active visual search: while the spatial memory provides reliable localization, translating it into accurate motor execution under dynamic viewpoints remains a key challenge, accounting for 48.0% of failures via inaccurate grasp pose estimation alone. In the fully observable simulation setting (Table 15), where OOV conditions are absent, failures instead expose limitations of the memory mechanism itself—primarily noisy spatial tokens from imperfect 3D estimation (44.0%) and irrelevant memory activation during retrieval (32.0%). These observations suggest that future improvements should focus on viewpoint-robust grasp estimation and task-phase-aware memory refinement. 

view confidence scoring, re-scan triggers, memory expiration, on-device storage, and human-in-the-loop confirmation as practical mitigations. 

### **D.8. Limitations and Future Directions** 

SOMA establishes out-of-vision manipulation under controlled tabletop conditions, and three limitations point to natural directions for future work. 

**Robustness in dynamic and parameter-sensitive settings.** Spatial Memory Construction relies on a short-horizon scan in a quasi-static scene with globally fixed thresholds for instance association and similarity-aware fusion. While Dynamic Memory Refinement handles objects that move and re-enter the head camera, fully dynamic scenes, noisier egomotion, and dense clutter would benefit from real-time tracking, confidence-based re-scanning, and per-token geometric confidence; learning these matching criteria, rather than hand-tuning them, is a promising direction. Residual failures further stem less from memory localization than from translating reliable spatial cues into precise motor execution while the head camera is still moving, motivating tighter head–arm coordination and viewpoint-stabilized action decoding. 

**Scope, scalability, and semantic granularity.** Memory refinement currently operates at object-level granularity (position and appearance) and cannot distinguish semantically meaningful state transitions—e.g., a drawer open vs. closed—from minor visual variations, limiting performance on multi-stage tasks; augmenting spatial tokens with explicit phase-transition signals is a natural extension. Scaling beyond tabletop settings—to mobile manipulation or room-scale environments—will require hierarchical memory structures operating across spatial and temporal scales, together with loop closure or SLAM-based alignment to control drift, while preserving the core principle of memorygrounded perception and action. 

**Safety and societal considerations.** Persistent spatial memory introduces risks that warrant attention in deployment: stale or incorrect memory can compromise physical safety in human-shared environments, and memory-grounded embodied systems raise privacy and potential-misuse concerns. We 

21 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 


_Figure 9._ Illustration of more execution examples including (1) _Sequential Dual-Object_ and (2) _Dual-Arm Coordination_ using our **_SOMA_** . 

22 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 


_Figure 10._ Qualitative results of the proposed SOMA framework on the _Robocasa Tabletop GR1_ benchmark (Bjorck et al., 2025; Nasiriany et al., 2024). The environment’s high-DOF control (arms, hands, waist) generates dynamic and highly variable head camera viewpoints, demonstrating SOMA’s robust capability in utilizing its designed spatial memory amidst complex visual instability. 

23 

**Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action** 


_Figure 11._ Qualitative Results of SimplerEnv Fractal suite (Li et al., 2024; Zitkovich et al., 2023) using our proposed SOMA. 

24 

