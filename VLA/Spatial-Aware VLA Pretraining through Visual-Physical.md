---
title: "Spatial-Aware VLA Pretraining through Visual-Physical Alignment from Human Videos"
date: "2025-12-15"
authors: "Yicheng Feng; Wanpeng Zhang; Ye Wang; Hao Luo; Haoqi Yuan; Sipeng Zheng"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2512.13080
pdf: https://arxiv.org/pdf/2512.13080
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.13080)** / [論文ページ](https://arxiv.org/abs/2512.13080)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Spatial-Aware VLA Pretraining through Visual-Physical Alignment from Human Videos** 

Yicheng Feng<sup>1</sup><sup>_,_3</sup> Wanpeng Zhang<sup>1</sup><sup>_,_3</sup> Ye Wang<sup>2</sup><sup>_,_3</sup> Hao Luo<sup>1</sup><sup>_,_3</sup> Haoqi Yuan<sup>1</sup><sup>_,_3</sup> Sipeng Zheng<sup>3</sup> Zongqing Lu<sup>1</sup><sup>_,_3†</sup> 1School of Computer Science, Peking University 2Renmin University of China 3BeingBeyond 

## **Abstract** 

_Vision-Language-Action (VLA) models provide a promising paradigm for robot learning by integrating visual perception with language-guided policy learning. However, most existing approaches rely on 2D visual inputs to perform actions in 3D physical environments, creating a significant gap between perception and action grounding. To bridge this gap, we propose a_ **_SpatialAware VLA Pretraining_** _paradigm that enables models to acquire 3D spatial understanding before robot policy learning. Starting from pretrained vision-language models, we leverage large-scale human demonstration videos to extract 3D visual and 3D action annotations, forming a new source of supervision that aligns 2D visual observations with 3D spatial reasoning. We instantiate this paradigm with VIPA-VLA, a dual-encoder architecture that incorporates a 3D visual encoder to augment semantic visual representations with 3D-aware features, and aligns the two through visual-physical alignment pretraining. When adapted to downstream robot tasks, VIPA-VLA achieves significantly improved grounding between 2D vision and 3D action, resulting in more robust and generalizable robotic policies. The project website: https://beingbeyond.github.io/VIPA-VLA._ 

## **1. Introduction** 

The rapid progress of large-scale vision-language models (VLMs) has showcased remarkable capabilities in learning joint representations across modalities[1, 3, 22, 41, 50, 66, 77, 86, 87, 94, 95, 98]. This progress has opened up new opportunities for robot policy learning, where VLMs offer a solid foundation for understanding both visual observations and language instructions, thereby guiding robot interaction with the physical world. Building on this foundation, the vision-language-action (VLA) paradigm has recently 

> †Corresponding to _<_ zongqing.lu@pku.edu.cn _>_ . 

demonstrated the potential to develop generalist robot policies across a wide range of tasks[5, 6, 8, 9, 38]. 

Nevertheless, current VLA models typically rely on 2D visual inputs to perceive the world while performing actions in a 3D physical environment, leaving a substantial gap between visual perception and embodied action. This weak correspondence limits their ability to ground actions in physical space. For effective policy learning, an agent must not only interpret pixels but also understand how these visual cues map to 3D geometry and how physical actions interact with the surrounding environment. While humans can infer 3D space from 2D visual signals, existing VLA models largely overlook this aspect, resulting in poor spatial grounding and limited generalization. 

To bridge this gap, we introduce a new **Spatial-Aware VLA Pretraining** paradigm that enables models to acquire 3D spatial awareness before learning robotic policies. Starting from pretrained VLMs, we leverage large-scale human demonstration videos as a rich source of supervision, where implicit correspondences between 2D visual observations and 3D physical actions naturally exist. Compared to robot data, human demonstrations are easier to obtain across diverse environments and naturally provide rich evidence of how actions are carried out in the physical world under diverse visual contexts. By extracting 3D cues such as hand-object relationships and motion trajectories from these videos, we construct pretraining tasks that teach the model to align 2D vision with 3D spatial understanding—forming what we term _visual-physical alignment_ . This spatially grounded pretraining provides a strong foundation for subsequent VLA post-training, allowing the model to learn and generalize more effectively in robot manipulation tasks. 

To instantiate this paradigm, we present VIPA-VLA ( **Vi** sual- **P** hysical- **A** lignment- **VLA** ), a dual-encoder architecture that augments semantic visual representations with explicit 3D spatial features. Alignment between vision, language, and 3D action is achieved through Spatial-Aware VLA Pretraining on our dataset Hand3D, which is constructed from diverse human manipulation recordings with annotated hand poses. From these videos, we derive two 

712 


Figure 1. Overview of the proposed _Visual-Physical Alignment_ framework. We start from diverse human demonstration videos to extract 3D visual annotations and 3D action annotations, capturing how humans interact with the physical world with corresponding visual observations. These annotations enable the two-stage **Spatial-Aware VLA Pretraining** , which teaches VLA models to ground 2D visual inputs in 3D spatial understanding. Then in the third stage, the pretrained model, VIPA-VLA, is adapted to robot manipulation tasks, resulting in robust and generalizable policies in simulation and real-world settings. 

forms of spatial supervision: **3D visual annotations** , providing coarse-grained spatial grounding between visual inputs and physical configurations, and **3D action annotations** , offering fine-grained motion supervision through 3D trajectories that encode human manipulation dynamics. The pretrained model is then adapted to robotic tasks via posttraining, transferring the learned spatial reasoning capability to robotic control.In summary, this work makes the following contributions: 

- We propose a new Spatial-Aware VLA Pretraining paradigm that bridges 2D visual perception and 3D physical action through large-scale human video data. 

- We construct Hand3D, a dataset of human manipulation videos with 3D visual and action annotations enabling visual–physical alignment supervision. 

- We present VIPA-VLA, a dual-encoder VLA architecture pretrained with our paradigm, which significantly enhances spatial grounding and generalization in downstream robot tasks. 

## **2. Related Work** 

### **2.1. VLA models** 

Vision-Language-Action (VLA) models aim to leverage joint representations of visual observations and language instructions to enable action execution in physical environments[8, 16, 19, 26, 27, 33, 42, 49, 51, 52, 67, 74, 79, 80, 82, 89, 96]. Some prior works tokenize robot actions and finetune pretrained VLMs on robot datasets[9, 38]. To support this pretraining paradigm, large-scale robot datasets have been introduced[10, 37, 58]. Other works incorporate additional action experts to improve the quality of action generation[5, 6, 45, 57]. Some approaches leverage demonstration videos for representation learning[54, 62, 69] or future state prediction to enhance action learning[10, 75, 

88]. More recently, models such as GR00T-N1[5] and _π_ 0 _._ 5[34] combine massive multimodal internet data with robot datasets for large-scale VLA pretraining, significantly improving generalization. In contrast, our work focuses on understanding the 3D physical space to better ground actions in environments with Spatial-Aware VLA Pretraining from human videos. 

### **2.2. 3D Aware Models** 

Recent advances in 3D vision-language models (3D VLMs) aim to extend the perceptual capacity of multimodal models beyond 2D images by incorporating 3D spatial information[12, 15, 23, 28, 32, 76, 97]. Some approaches leverage datasets with explicit 3D annotations[2, 13, 18], while others rely on geometric priors or depth estimation models to infer 3D structure from monocular visual inputs[4, 68, 70, 71, 78]. These methods have improved the ability of VLMs to reason about spatial relationships, object geometry, and scene structure. However, the focus of existing 3D VLMs is primarily on perception rather than action. They enhance spatial understanding of static observations but do not explicitly establish the correspondence between 3D perception and the physical action space required for robot policy learning. Consequently, their utility in training VLA models remains limited. 

Recent works have also explored enhancing VLAs with 3D spatial reasoning[32]. For instance, 3D-VLA[92] introduces a generative world model with diffusion-based rendering of future images and point clouds, GeoVLA[65] leverages RGBD inputs together with tailored architectures for explicit 3D modeling, while SpatialVLA[61] improves policy learning through ego-centric position encoding and adaptive action grids. Our work differs in that we aim to endow VLAs with 3D spatial understanding through a pretraining stage, by leveraging 3D-aware annotations ex- 

713 

tracted from human videos and incorporating a 3D encoder to explicitly align 2D visual observations with 3D physical space. This Spatial-Aware Pretraining equips VLAs with stronger 3D grounding prior to downstream policy learning. 

### **2.3. Learning from human videos** 

A line of research has explored leveraging human demonstration videos to facilitate robot policy learning. Some efforts adopt representation learning approaches to extract latent features from human activities[10, 54, 76], yet such representations are typically implicit and provide limited guidance for explicit action grounding. Other methods attempt to directly align the human action space with the robot action space[36, 56, 60, 64, 81]. However, these approaches suffer from embodiment mismatch, as the physical capabilities and kinematics of humans and robots differ significantly. In addition, several works explore extracting interaction-related knowledge from human videos, such as affordances or grasping strategies[14, 25, 53], which provide helpful cues but still stop short of explicitly bridging perception and action in 3D physical space. Beyond these, Being-H0[49] also leverages human videos for VLA pretraining, but its primary focus lies in learning manipulation motion sequences. In contrast, we highlight that, despite the embodiment gap, human videos contain rich information about how actions are executed in the 3D physical world across diverse visual contexts. Our work leverages this information as supervision for Spatial-Aware Pretraining, enabling VLA models to acquire grounded correspondences between 2D visual observations and 3D action space before downstream policy learning. 

## **3. Method** 

In this section, we first provide preliminaries on visionlanguage models (VLMs) and vision-language-action models (VLAs) (Sec. 3.1). Then we illustrate the _Visual Phisical Alignment_ in Sec. 3.2, including the spatialaware dataset Hand3D (Sec. 3.2.1), the model architecture VIPA-VLA (Sec. 3.2.2) and the Spatial-Aware VLA Pretraining (Sec. 3.2.3). In Sec. 3.3 we describe the posttraining procedure for adapting the model to robot tasks. 

### **3.1. Preliminaries** 

We begin by briefly formulating the setting of visionlanguage models (VLMs) and vision-language-action models (VLAs). A VLM is designed to map a set of visual inputs _v_ = _{v_ 1 _, . . . , vT }_ (e.g., images or video frames) and a language instruction _l_ (e.g., a question or command) into an aligned embedding space, producing a textual output _y_ such as an answer or a caption: 


Figure 2. Overview of the Hand3D-visual. By integrating point cloud estimation, object localization, and hand pose annotations from human manipulation videos, we bridge 2D visual observations with 3D physical action space to provide visual-physical aligment supervision for VLA models. 

In contrast, a VLA extends this formulation to the action domain, where the model must not only capture the semantic alignment between vision and language but also generate executable actions in a 3D physical environment. Given visual observations _v_ and an instruction _l_ , the VLA predicts an action chunk **a** _t_ = _{_ **a**<sup>1</sup> _t_<sup>_, . . . ,_</sup><sup>**a**</sup><sup>_H_</sup> _t_<sup>_}_:</sup> 


This distinction highlights the central challenge addressed in this work: while VLMs excel at visual–semantic reasoning, VLAs additionally require grounding visual perception in 3D physical action space, which motivates our proposed Spatial-Aware VLA Pretraining paradigm. 

### **3.2. Visual-Physical Alignment** 

#### **3.2.1.** Hand3D 

Existing 3D VLMs typically obtain 3D supervision either from datasets with explicit 3D annotations or by estimating depth from 2D inputs. We follow their principles, but we focus on human demonstration videos, which inherently reveal how actions unfold in 3D space. These videos naturally provide rich source of visual-physical correspondences, allowing us to construct annotations that align 2D visual observations with action-relevant 3D information, forming the foundation for visual–physical alignment in VLA models. 

**Human video collection.** We start from the collection of human manipulation videos covering diverse tasks and interaction scenarios. Following UniHand[49], we aggregate data from a wide range of different sources: **(1) Motion capture datasets** : Arctic[20], HOI4D[46], FPHA[24], H2O[39], OAKINK2[83], TACO[47], DexYCB[11], **(2) VR-recorded datasets** : EgoDex[29] and **(3) Pseudo-annotated datasets** : Taste-Rob[90], each providing recordings of humans performing object-centric manipulations and the corresponding hand motion sequences. To ensure consistency across heterogeneous datasets, we align all hand annotations to the unified MANO[63] representation, which serves as a standard parametric model of human hand pose and shape. This alignment enables us to obtain high-quality, normalized annotations of hand trajec- 

714 

tories that can be directly associated with the corresponding visual frames. 

**3D aware annotations.** While prior works have explored learning from human videos, they largely remain confined to the 2D visual space, which restricts their ability to capture the physical grounding required for 3D action execution in robotic manipulation. We address this by extracting **3D visual annotations** and **3D action annotations** from human demonstrations. 

As shown in Figure 2, we construct **3D visual annotations** from human manipulation videos by combining point cloud estimation, object proposals, and hand pose information. Specifically, we first employ the Cut3R[70] model to obtain a dense per-frame point cloud estimation _P_ = _{_ ( _xi, yi, zi_ ) _}_<sup>_N_</sup> _i_ =1<sup>,whichprovides3Dcoordinatesforeach</sup> image pixel. Cut3R is chosen for its robustness in dynamic scenes and pretraining on human–object interaction data. For object localization, we apply Gemini-2.5-flash[17] to generate object proposals and GroundingDINO[44] to obtain 2D bounding boxes _Bo_ , which approximate the spatial extent of each object in the image. By combining these bounding boxes with the depth estimation from _P_ , we localize each object in the 3D space and obtain its approximate spatial position. 

In parallel, we utilize MANO-based hand pose annotations **m** = _{θ, r, τ, β}_ , provided in the dataset, together with camera extrinsics [ _R | t_ ] and intrinsics _K_ . The MANO parameters are transformed into the camera coordinate system to yield 3D joint locations _Jh_ = _{_ ( _xj, yj, zj_ ) _}_<sup>21</sup> _j_ =1<sup>.</sup> These joint coordinates are projected onto the image plane, 


By checking the visibility of the projected joints, we filter out frames where the hand is outside the view. Previous works have often relied on depth estimation models to introduce 3D information; however, the relative scale provided by such models typically does not match the actual physical space and may introduce misalignment. This mismatch can be problematic for action learning, since actions are executed at real-world physical scales. To unify scales between the relative point cloud estimation _P_ and the physical space, we perform **scale calibration** by matching hand joint positions _Jh_ , which are absolute spatial positions, with corresponding point cloud coordinates. 

To formalize this process, let _Jh_<sup>_z_=</sup><sup>_{j_</sup> _k_<sup>_z}_denotethe</sup> set _J_ ˜ _h_<sup>_z_</sup> of<sup>=</sup> hand<sup>_{_˜</sup><sup>_j_</sup> _k_<sup>_z}_</sup> joint<sup>thecorresponding</sup> depths in absolute<sup>depths</sup> physical<sup>obtained</sup> space,<sup>from</sup> and<sup>the</sup> point cloud estimation _P_ . We estimate a scale factor _s_ as 


where Ω is the set of valid joints determined by visibility and valid depth estimations. Applying _s_ to the point cloud 

_P_ yields the calibrated representation _sP_ which ensures that both hands and objects are represented in a consistent 3D physical coordinate system. Consequently, we obtain spatially aligned annotations that encode the 3D geometry of hands and objects in consecutive frames. 

**Instructional data curation.** Building on the spatial annotations derived from human manipulation videos, we construct a set of vision–question–answering style labels that explicitly encode the relationship between 2D visual observations and 3D action information. This step is crucial for grounding visual inputs to physical actions, enabling VLA models to understand how 3D movements are manifested in visual space. To achieve this, we leverage Gemini-2.5-flash[17] to generate four complementary categories of question–answer pairs: (1) **Spatial Relationship:** Given information about a hand and an object within several consecutive frames, we generate natural language questions and answers that describe their 3D spatial relations in the last frame (e.g., relative position, distance, or contact state). (2) **Task Completion:** Conditioned on a task description and corresponding video frames, we formulate instructions about how the hand should move in 3D to interact with the target object. (3) **Hand Movement:** Given two frames, we annotate the hand’s 3D trajectory between them, including movement direction and distance. (4) **Camera Movement:** The relative 3D transformation of the camera for pairs of frames, expressed in terms of rotation direction and degree. For the 3D spatial relationships or movements used in Category 1–3 we represent each by the pair (direction _,_ distance). Let **v** = ( _x, y, z_ ) _∈_ R<sup>3</sup> denote the displacement vector that characterizes the relative 3D offset between two entities (e.g., object and hand, or hand positions across frames). The distance is defined as the Euclidean norm dist( **v** ) = _∥_ **v** _∥_ 2 _._ The direction is derived from the unit vector **v** ˆ = **v** _/∥_ **v** _∥_ 2 and discretized into axis-aligned language tokens with a component-wise threshold _γ_ to filter out negligible components: 


For camera movement, we consider the relative transformation between two camera poses ( _R_ 1 _, t_ 1) and ( _R_ 2 _, t_ 2), and decompose it into a rotation, represented by an axisangle description ( **u** _, ϕ_ ), where **u** is the rotation axis and _ϕ_ the rotation degree; and the translation, expressed as a direction vector and magnitude. 

Through this process, dense 3D geometry are transformed into compact, linguistically grounded labels directly used to produce VQA-style supervisory pairs, linking human visual demonstrations to physically grounded actions. Importantly, this formulation allows the model not only to perceive spatial configurations but also to reason about 

715 


Figure 3. Model architecture of VIPA-VLA. A dual-encoder including a semantic vision encoder and a 3D encoder produces fused spatial–semantic features through a cross-attention fusion layer. During pre-training, the vision tokens are aligned with text and motion tokens using 3D visual and 3D action annotations. During post-training, action queries interact with fused visual–language features to produce conditions, which is combined with the robot state and processed by a flow-matching action head to predict actions for robotic manipulation. 

dynamic changes—hand motions, task-oriented manipulations, and even camera movements—thereby strengthening the bridge between 2D visual observations and 3D action policies. With large-scale human data from nine heterogeneous human manipulation video sources, we uniformly sampled approximately 4K clips for annotation, ensuring coverage across diverse scenes, task types, and object interactions, and our pipeline produced around 300K instruction–answer pairs, which we denote as Hand3D-visual. 

To complement the 3D visual annotations, we further construct **3D action annotations** that capture the dynamic aspect of human manipulation in physical space. From hand motion sequences in human videos, we extract wrist trajectories as ( _xt, yt, zt_ ) spatial coordinate series, which are discretized via uniform binning into motion tokens ( _m_ 1<sup>_x, my_</sup> 1<sup>_, m_</sup> 1<sup>_z, ..., mx_</sup> _t_<sup>_, m_</sup> _t_<sup>_y, mz_</sup> _t_<sup>).Following</sup> UniHand[49], we obtain text instructions for videos, yielding 4M video–instruction–motion pairs. We further filter out samples with insignificant 3D hand movement, resulting in a 1M curated dataset Hand3D-action, providing fine-grained 3D motion patterns and spatial trajectories, as well as higher-level physical reasoning knowledge such as object affordance and task decomposition. 

#### **3.2.2.** VIPA-VLA 

Previous VLA models typically employ a semantic vision encoder to extract high-level visual semantics. However, such encoders lack the ability to provide features of 3D spatial structures. To address this limitation, we propose VIPA-VLA, a dual-encoder architecture that integrates both semantic and spatial visual representations (Figure 3 left). Specifically, in addition to a semantic vision encoder, we incorporate a 3D vision encoder Cut3R [70], which provides explicit geometric understanding of the scene. The semantic encoder produces visual embeddings **V** _sem_ , while the 3D encoder outputs spatial embed- 

dings **V** _spa_ . To effectively combine these complementary features, we introduce a fusion layer implemented as a cross-attention module, where the semantic features serve as queries and the 3D spatial features act as keys and values, yielding fused visual representations **V** _f_ . To further enable the model to to understand fine-grained 3D motion trajectories extracted from human demonstrations, we extend the LLM’s token embedding space by introducing a set of motion tokens which discretize the 3D physical space. 

#### **3.2.3. Spatial-Aware VLA Pretraining** 

To effectively align semantic perception with physical understanding, we design a _Spatial-Aware VLA Pretraining_ strategy composed of two stages, enabling progressive learning of visual–physical alignment (Figure 1). We first initialize our model using a pretrained VLM to inherit semantic understanding, while incorporating the pretrained 3D vision encoder and a randomly initialized fusion layer. In Stage 1, we freeze all pretrained parameters and train only the fusion layer using the 3D visual annotation VQA data. The objective is to align the semantic embeddings **V** _sem_ and spatial embeddings **V** _spa_ through the fusion layer, encouraging reasoning about 3D spatial relations. 

In Stage 2, we extend the LLM vocabulary to include a set of motion tokens and then train the model on 3D action annotations. In this stage, the semantic and spatial encoders are frozen, and the LLM is trained to predict motion tokens conditioned on fused visual and textual inputs. This phase enables the model to acquire fine-grained spatial reasoning and action-level understanding, learning how visual cues correspond to physically grounded motion patterns. Through the Spatial-Aware VLA Pretraining, VIPA-VLA progressively aligns 2D semantic perception, 3D spatial understanding, and action reasoning — achieving comprehensive visual–physical alignment for downstream robotic policy learning. 

### **3.3. Post-Training** 

After pretraining, VIPA-VLA has acquired alignment between 2D observations and 3D physical/action representations. In the post-training stage, we fine-tune this initialization on downstream robot tasks by attaching an _action head_ and training it to produce executable action chunks. For implementation, we use a diffusion transformer (DiT) model, parameterized with _θ_ . 

Let _v_ and _l_ denote visual frames and language instruction, and let _Qa_ be a fixed set of action queries. We extract conditional context from the pretrained VLM backbone as _h_ cond = VLM _ϕ_ ( _v, l, Qa_ ) _,_ where the hidden states corresponding to _Qa_ are used as the DiT conditioning. The ground-truth action chunk for timestep _t_ is denoted by **a** _t_ , and the robot state embedding by _st_ . Following flow matching[43], we generate a noisy action trajectory by linearly interpolating between a random noise vector **_ϵ_** and the 

716 

Table 1. **Success rates (%) on the LIBERO benchmark.** Results are reported for four task suites, with each suite evaluated across 500 trials. Experiments are conducted under both single-view and two-view input settings. All results are from public reports, except for GR00T N1.5<sup>_∗_</sup> , which we reproduce using the released model. The results of MaIL<sup>_†_</sup> is from the ED-Ma version. 

|Model|Robo-PT|LIBERO-S (%)|LIBERO-O (%)|LIBERO-G (%)|LIBERO-L (%)|Avg. (%)|
|---|---|---|---|---|---|---|
|_Models with single_|_-view input_<br>||||||
|TraceVLA[93]|�<br>|84.6|85.2|75.1|54.1|74.8|
|OpenVLA[38]|�|84.7|88.4|79.2|53.7|76.5|
|SpatialVLA[61]|�|88.2|89.9|78.6|55.5|78.1|
|DiT Policy[30]|�|84.2|96.3|85.4|63.8|82.4|
|CoT-VLA[91]|�|87.5|91.6|87.6|69.0|83.9|
|ThinkAct[31]|�|88.3|91.4|87.1|70.9|84.4|
|TriVLA[48]|�|91.2|93.8|89.8|73.2|87.0|
|4D-VLA[84]|�|88.9|95.2|90.9|79.1|88.6|
|GR00T N1.5<sup>_∗_</sup>[5]|�|91.4|**97.6**|94.0|**85.6**|92.1|
|**VIPA-VLA**|�|**92.6**|97.2|**94.2**|**85.6**|**92.4**|
|_Models with two-vi_|_ew input_||||||
|MaIL<sup>_†_</sup>[35]|�|74.3|90.1|81.8|78.6|83.5|
|_π_0-FAST [59]|�|96.4|96.8|88.6|60.2|85.5|
|MolmoAct[40]|�|87.0|95.4|87.6|77.2|86.6|
|GR00T N1[5]|�|94.4|97.6|93.0|90.6|93.9|
|_π_0 [6]|�|98.0|96.8|94.4|88.4|94.4|
|UniVLA[73]|�|95.4|**98.8**|93.6|94.0|95.5|
|_π_0_._5[7]|�<br>|**98.8**|98.2|**98.0**|92.4|**96.9**|
|**VIPA-VLA**|�|96.6|98.6|97.0|**95.0**|96.8|


ground-truth action: 


The DiT receives the concatenation of **a** ˜<sup>(</sup> _t_<sup>_τ_)</sup> and the state embedding _st_ as its input representation: _h_ DiT = concat� **a** ˜ _t_ ( _τ_ ) _, st_ � _._ Conditioned on _h_ cond, the DiT predicts the instantaneous flow vector **v** _θ_ . The training objective minimizes the deviation between this prediction and the oracle transport direction given by **a** _t −_ **_ϵ_** : 


During training, only the LLM backbone and the action head _fθ_ are updated to adapt the model to action execution. The illustration is shown in Figure 3 (right). 

## **4. Experiment** 

### **4.1. Implementation Details** 

VIPA-VLA is initialized from InternVL3.5-2B[72]. During the first pre-training stage, for the _spatial relationship_ and _task completion_ tasks, the model is given 1–4 randomly sampled consecutive frames as input, while for the _hand movement_ and _camera movement_ tasks, two frames are provided. All video frames are sampled at 1 fps. In the second pre-training stage and the post-training stage, we use single frame as visual input. We use a learning rate of 1 _e −_ 5 for pre-training and 5 _e−_ 5 for post-training, and all experiments are conducted on 8 _×_ A800 GPUs. 

### **4.2. Simulation Robot Tasks** 

**Benchmarks.** We first evaluate VIPA-VLA’s performance for robotic manipulation in simulation environments, which assesses how well the model can generalize spatially grounded reasoning from human demonstrations to robotic scenarios. Specifically, we adopt **LIBERO** , which is a standard benchmark for evaluating robot manipulation capabilities, emphasizing robustness and generalization. **LIBERO** consists of four task suites: _Spatial_ , _Object_ , _Goal_ and _Long_ , covering different task settings and scene layouts. 

**Results** We report the average success rates across 500 trials for each task suite in Table 1. VIPA-VLA achieves strong performance across all LIBERO task suites under both single-view and two-view input settings. This demonstrates that the Spatial-Aware VLA Pretraining learned from human videos generalizes effectively to simulated robotic environments. Notably, our model does not rely on any robot data during pretraining, yet it surpasses a number of previous methods and achieves results comparable to _π_ - series and GR00T models, which are strong baselines pretrained on large-scale robot datasets. This indicates that the spatial reasoning ability acquired from human demonstrations—bridging 2D visual cues with 3D spatial understanding—can significantly help robotic manipulation even in simulation. Among baselines that explicitly model spatial reasoning, such as SpatialVLA[61], TraceVLA[93], and MolmoAct[40], our approach consistently performs better, 

717 

highlighting the effectiveness of learning visual–physical alignment from diverse human demonstrations. 

### **4.3. Real Robot Tasks** 

We further evaluate our model in real-world robotic manipulation tasks, which provide a more realistic 3D physical setting and require more accurate spatial perception and action grounding, making them ideal for assessing the benefits of our Spatial-Aware VLA Pretraining with human videos. The experiments are conducted with a 7-DoF Franka Research 3 arm, a 6-DoF Inspire hand, and two RealSense L515 cameras for visual observation. 


Figure 4. Real Robot Task Settings. 

We design three manipulation tasks to test different aspects of spatial perception and reasoning: (1) **Put-ThreeObj** – sequentially place three fruits into a drawer, assessing the ability to localize and manipulate multiple objects; (2) **Wipe-Board** – use a cloth to remove all pen marks from a whiteboard, requiring flexible spatial reasoning over irregularly shaped target regions; (3) **Water-Plant** – pick up a watering can and water a plant, demanding precise spatial localization and control of fine-grained 3D motion. The illustration of the tasks are shown in Figure 4. For each task, we collect 50 teleoperated trajectories for post-training and conduct 10 evaluation trials to measure task success rates. Besides the success rates of the whole tasks, each task is decomposed into a sequence of sub-tasks, and we also report the success rates computed by the proportion of completed sub-tasks, averaged across all trials. There are 5 sub-tasks for Put-Three-Obj, and 3 for the other two tasks. Details of the sub-task configurations are provided in the Appendix. 

Table 2. Success rates (%) of VIPA-VLA v.s. baseline models on real robot tasks. Results are shown as sub-task / whole-task success rates. 

|Task|Put-Three-Obj|Wipe-Board|Water-Plant|
|---|---|---|---|
|GR00T N1.5 [5]|48% /**40%**|57% / 30%|53% / 30%|
|Being-H0[49]|38% / 20%|40% / 10%|37% / 20%|
|InternVL3.5 [72]|34% / 10%|43% / 10%|37% / 20%|
|**VIPA-VLA**|**52%**/ 10%|**83%**/**60%**|**57%**/**50%**|


As shown in Table 2, VIPA-VLA achieves the best overall performance across all real-world manipulation tasks, demonstrating that the spatial understanding acquired during pretraining effectively helps real robotic manipulations, leading to more robust and generalizable behavior in real- 

world manipulation scenarios. Compared with the ablation baseline InternVL3.5, our model achieves substantial improvements on all tasks, confirming the effectiveness of our proposed Spatial-Aware Pretraining and dual-encoder architecture in enhancing spatial grounding and generalization. Although VIPA-VLA achieves lower complete-task success rate on Put-Three-Obj, it attains higher sub-task success rate. This is because baseline models often fail early in the sequence—sometimes unable to complete even the first step—indicating less stable spatial reasoning and control. In contrast, VIPA-VLA exhibits more consistent progress across task stages, reflecting stronger robustness in real-world execution. 

Table 3. Success rates (%) of VIPA-VLA v.s. baseline models on real robot tasks with unseen environments. Results are shown as sub-task / whole-task success rates. 

|Task|Put-Three-Obj-Unseen|Wipe-Board-Unseen|
|---|---|---|
|GR00T N1.5 [5]|28% / 0%|43% / 10%|
|Being-H0[49]|16% / 0%|33% / 10%|
|InternVL3.5 [72]|42% / 10%|40% / 10%|
|**VIPA-VLA**|**44%**/**20%**|**83%**/**50%**|


We further evaluate the models in unseen environments. As shown in Table 3, VIPA-VLA maintains strong performance when evaluated in unseen visual environments, significantly outperforming all baselines. While other models often exhibit a sharp degradation in performance—often failing to complete even the initial steps—VIPA-VLA retains high sub-task and whole-task success rates, demonstrating enhanced robustness and generalization. These results highlight that the Spatial-Aware Pretraining effectively equips the model with transferable 3D spatial understanding learned from human videos. By grounding 2D visual observations into 3D physical representations, our model generalizes more reliably to new scenes. 

### **4.4. Ablation Studies** 

**Architecture and the Spatial-Aware VLA Pretraining.** We conduct ablation studies on the **LIBERO** benchmark to evaluate the effectiveness of our model architecture and the proposed Spatial-Aware VLA Pretraining. This analysis isolates the contributions of the dual-encoder design and the pretraining strategy with visual-physical alignment. 

As shown in Table 4, both the Spatial-Aware Pretraining on human videos and the proposed dual-encoder architecture contribute to overall performance improvements. Removing either component leads to a consistent performance drop across all task suites. The pretraining provides the model with rich 3D motion and perception priors learned from human demonstrations, while the dual encoder enables more effective fusion of 3D visual representations. When combined, these two designs further enhance 

718 

Table 4. Ablations (%) on the LIBERO benchmark. 

|Model<br>Spa.|Obj. Goal|Long|Avg.|
|---|---|---|---|
|**VIPA-VLA**<br>**92.6**|**97.2**<br>**94.2**|**85.6**|**92.4**|
|– Pretraining<br>90.8|97.0 93.0|84.0|91.2 (-1.2%)|
|– Dual Encoder<br>90.0|**97.2** 92.4|81.8|90.4 (-2.0%)|
|– Both<br>89.2|95.2 90.0|80.4|88.7 (-3.7%)|


the model’s spatial reasoning and generalization, resulting in the strongest performance. 

**Effect of Spatial-Aware VLA Pretraining.** Here we first evaluate the effectiveness of the first stage pretraining on **3D visual annotations** in improving spatial understanding capabilities. Specifically, we assess how well the model can reason about spatial relations and 3D geometry in visual scenes. We report results on the Hand3D-test, which consists of 2K VQA pairs from unseen videos not included in the training corpus. The evaluation focuses on two aspects: _distance accuracy_ and _direction accuracy_ . Direction accuracy is measured by assessing the correctness of predictions along the three principal axes; each axis contributes a binary score of 0 or 1. Distance accuracy is quantified by the average prediction error in meters. 

We compare VIPA-VLA-PT against two ablations: (1) **InternVL3.5** : the backbone VLM without additional pretraining. (2) **InternVL3.5** +Hand3D: The backbone model pretrained with Hand3D, without the proposed dual encoder architecture. This setup allows us to disentangle the contribution of Hand3D pretraining and the architecture of VIPA-VLA. For InternVL3.5, we provide an example answer in the prompt for valid answering format. 

Table 5. Evaluation of 3D spatial understanding. 

|**Model**|**Dist. Err. (m)**_↓_|**Dir. Scr.** _↑_|
|---|---|---|
|InternVL3.5|0.18|1.22/3|
|InternVL3.5 +Hand3D|0.14|1.75/3|
|VIPA-VLA-PT|**0.12**|**1.82/3**|


ships. Pretraining on Hand3D notably improves performance, confirming that 3D visual annotations effectively enhance the model’s spatial grounding through visualphysical alignment. Our proposed VIPA-VLA further achieves a consistent performance gain, demonstrating that introducing the 3D visual encoder and the fusion mechanism brings additional benefits beyond data-level supervision. Notably, only the fusion layer is trained at this stage, showing that aligning semantic and spatial visual features alone already yields substantial gains. 

We further show detailed comparison between VIPA-VLA-PT and InternVL3.5 in Figure 5. After Spatial-Aware Pretraining on **3D visual annotations** , our model makes substantially fewer severe errors and attains highly accurate predictions in about 30% of the cases, reflecting precise and reliable 3D spatial grounding ability obtained in this stage. 


Figure 6. Visualization of the predicted motion trajectories from VIPA-VLA after second stage pretraining (blue lines) and the ground-truth trajectories (red lines). 

We then show qualitative results of the second stage pretraining on **3D action annotations** in Figure 6. The predicted trajectories closely align with the instructions, showing that the model effectively understands the mapping between visual observations and physical space. Compared to the ground-truth trajectories, which often exhibit noisy and redundant motion due to natural human variability, our model produces smoother and more goal-directed trajectories. Moreover, the predictions reflect learned affordance knowledge — for example, when manipulating a wooden spoon, the model grasps it near the handle end. 

## **5. Conclusion** 


Figure 5. Comparison between VIPA-VLA-PT and InternVL3.5 on Hand3D-test. Left: histogram of direction scores; Right: histogram of distance errors 

From the results shown in Table 5, the backbone InternVL3.5 performs poorly on the spatial reasoning tasks, indicating its limited understanding of spatial relation- 

In this work, we address the critical 2D–3D gap in VLA models through _visual-physical alignment_ pretraining from large-scale human videos. We introduce Hand3D, a dataset providing 3D visual and action annotations derived from human manipulation, and propose VIPA-VLA, a dualencoder architecture designed for Spatial-Aware VLA Pretraining. The proposed paradigm effectively aligns 2D perception with 3D physical understanding, yielding strong improvements in spatial reasoning and downstream robotic manipulation. Our results validate the effectiveness of Spatial-Aware Pretraining from human demonstrations. In future, this pretraining paradigm can be combined with robot data pretraining to achieve a more comprehensive and effective overall pretraining strategy. 

719 

### **Acknowledgments** 

This work was supported by NSFC in part under Grant 62450001 and 62476008. The authors would like to thank the anonymous reviewers for their valuable comments and advice. 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 1 

- [2] Panos Achlioptas, Ahmed Abdelreheem, Fei Xia, Mohamed Elhoseiny, and Leonidas Guibas. Referit3d: Neural listeners for fine-grained 3d object identification in real-world scenes. In _ECCV_ , 2020. 2 

- [3] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 1 

- [4] Shariq Farooq Bhat, Reiner Birkl, Diana Wofk, Peter Wonka, and Matthias Muller. Zoedepth: Zero-shot transfer by combining relative and metric depth. _arXiv preprint arXiv:2302.12288_ , 2023. 2 

- [5] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 2, 6, 7 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ , 2024. 1, 2, 6 

- [7] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y Galliker, et al. _π_ 0.5: a vision-language-action model with open-world generalization. In _CoRL_ , 2025. 6 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1, 2 

- [9] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 1, 

2 

- [10] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xu Huang, Shu Jiang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 2, 3 

- [11] Yu-Wei Chao, Wei Yang, Yu Xiang, Pavlo Molchanov, Ankur Handa, Jonathan Tremblay, Yashraj S Narang, Karl Van Wyk, Umar Iqbal, Stan Birchfield, et al. Dexycb: A benchmark for capturing hand grasping of objects. In _CVPR_ , 2021. 3, 1 

- [12] Boyuan Chen, Zhuo Xu, Sean Kirmani, Brain Ichter, Dorsa Sadigh, Leonidas Guibas, and Fei Xia. Spatialvlm: Endowing vision-language models with spatial reasoning capabilities. In _CVPR_ , 2024. 2 

- [13] Dave Zhenyu Chen, Angel X Chang, and Matthias Nießner. Scanrefer: 3d object localization in rgb-d scans using natural language. In _ECCV_ , 2020. 2 

- [14] Hanzhi Chen, Boyang Sun, Anran Zhang, Marc Pollefeys, and Stefan Leutenegger. Vidbot: Learning generalizable 3d actions from in-the-wild 2d human videos for zero-shot robotic manipulation. In _CVPR_ , 2025. 3 

- [15] Sijin Chen, Xin Chen, Chi Zhang, Mingsheng Li, Gang Yu, Hao Fei, Hongyuan Zhu, Jiayuan Fan, and Tao Chen. Ll3da: Visual interactive instruction tuning for omni-3d understanding, reasoning, and planning. In _CVPR_ , 2024. 2 

- [16] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ , 2023. 2 

- [17] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 4, 1 

- [18] Angela Dai, Angel X. Chang, Manolis Savva, Maciej Halber, Thomas Funkhouser, and Matthias Nießner. Scannet: Richly-annotated 3d reconstructions of indoor scenes. In _CVPR_ , 2017. 2 

- [19] Shengliang Deng, Mi Yan, Songlin Wei, Haixin Ma, Yuxin Yang, Jiayi Chen, Zhiqi Zhang, Taoyu Yang, Xuheng Zhang, Heming Cui, et al. Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data. _arXiv preprint arXiv:2505.03233_ , 2025. 2 

- [20] Zicong Fan, Omid Taheri, Dimitrios Tzionas, Muhammed Kocabas, Manuel Kaufmann, Michael J Black, and Otmar Hilliges. Arctic: A dataset for dexterous bimanual handobject manipulation. In _CVPR_ , 2023. 3, 1 

- [21] Zhiwen Fan, Jian Zhang, Renjie Li, Junge Zhang, Runjin Chen, Hezhen Hu, Kevin Wang, Huaizhi Qu, Dilin Wang, Zhicheng Yan, et al. Vlm-3r: Vision-language models augmented with instruction-aligned 3d reconstruction. _arXiv preprint arXiv:2505.20279_ , 2025. 1 

- [22] Yicheng Feng, Yijiang Li, Wanpeng Zhang, Sipeng Zheng, Hao Luo, Zihao Yue, and Zongqing Lu. Videoorion: Tokenizing object dynamics in videos. In _ICCV_ , 2025. 1 

- [23] Rao Fu, Jingyu Liu, Xilun Chen, Yixin Nie, and Wenhan Xiong. Scene-llm: Extending language model for 3d visual understanding and reasoning. _arXiv preprint arXiv:2403.11401_ , 2024. 2 

720 

- [24] Guillermo Garcia-Hernando, Shanxin Yuan, Seungryul Baek, and Tae-Kyun Kim. First-person hand action benchmark with rgb-d videos and 3d hand pose annotations. In _CVPR_ , 2018. 3, 1 

- [25] Alexey Gavryushin, Xi Wang, Robert JS Malate, Chenyu Yang, Xiangyi Jia, Shubh Goel, Davide Liconti, Ren´e Zurbr¨ugg, Robert K Katzschmann, and Marc Pollefeys. Maple: Encoding dexterous robotic manipulation priors learned from egocentric videos. _arXiv preprint arXiv:2504.06084_ , 2025. 3 

- [26] Ankit Goyal, Valts Blukis, Jie Xu, Yijie Guo, Yu-Wei Chao, and Dieter Fox. Rvt2: Learning precise manipulation from few demonstrations. In _RSS_ , 2024. 2 

- [27] Jiawei He, Danshi Li, Xinqiang Yu, Zekun Qi, Wenyao Zhang, Jiayi Chen, Zhaoxiang Zhang, Zhizheng Zhang, Li Yi, and He Wang. Dexvlg: Dexterous vision-language-grasp model at scale. _arXiv preprint arXiv:2507.02747_ , 2025. 2 

- [28] Yining Hong, Haoyu Zhen, Peihao Chen, Shuhong Zheng, Yilun Du, Zhenfang Chen, and Chuang Gan. 3d-llm: Injecting the 3d world into large language models. In _NeurIPS_ , 2023. 2 

- [29] Ryan Hoque, Peide Huang, David J Yoon, Mouli Sivapurapu, and Jian Zhang. Egodex: Learning dexterous manipulation from large-scale egocentric video. _arXiv preprint arXiv:2505.11709_ , 2025. 3, 1 

- [30] Zhi Hou, Tianyi Zhang, Yuwen Xiong, Hengjun Pu, Chengyang Zhao, Ronglei Tong, Yu Qiao, Jifeng Dai, and Yuntao Chen. Diffusion transformer policy. _arXiv preprint arXiv:2410.15959_ , 2024. 6 

- [31] Chi-Pin Huang, Yueh-Hua Wu, Min-Hung Chen, YuChiang Frank Wang, and Fu-En Yang. Thinkact: Visionlanguage-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025. 6 

- [32] Jiangyong Huang, Silong Yong, Xiaojian Ma, Xiongkun Linghu, Puhao Li, Yan Wang, Qing Li, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. An embodied generalist agent in 3d world. In _ICML_ , 2024. 2 

- [33] Ziye Huang, Haoqi Yuan, Yuhui Fu, and Zongqing Lu. Efficient residual learning with mixture-of-experts for universal dexterous grasping. In _ICLR_ , 2025. 2 

- [34] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Rich Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0.5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 2 

- [35] Xiaogang Jia, Qian Wang, Atalay Donat, Bowen Xing, Ge Li, Hongyi Zhou, Onur Celik, Denis Blessing, Rudolf Lioutikov, and Gerhard Neumann. MaIL: Improving imitation learning with selective state space models. In _CoRL_ , 2024. 6 

- [36] Simar Kareer, Dhruv Patel, Ryan Punamiya, Pranay Mathur, Shuo Cheng, Chen Wang, Judy Hoffman, and Danfei Xu. 

   - Egomimic: Scaling imitation learning via egocentric video. _arXiv preprint arXiv:2410.24221_ , 2024. 3 

- [37] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 2 

- [38] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 6 

- [39] Taein Kwon, Bugra Tekin, Jan St¨uhmer, Federica Bogo, and Marc Pollefeys. H2o: Two hands manipulating objects for first person interaction recognition. In _ICCV_ , 2021. 3, 1 

- [40] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, et al. Molmoact: Action reasoning models that can reason in space. _arXiv preprint arXiv:2508.07917_ , 2025. 6 

- [41] Junnan Li, Dongxu Li, Silvio Savarese, and Steven C. H. Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _ICML_ , 2023. 1 

- [42] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 2 

- [43] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _ICLR_ , 2023. 5 

- [44] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. _arXiv preprint arXiv:2303.05499_ , 2023. 4 

- [45] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 2 

- [46] Yunze Liu, Yun Liu, Che Jiang, Kangbo Lyu, Weikang Wan, Hao Shen, Boqiang Liang, Zhoujie Fu, He Wang, and Li Yi. Hoi4d: A 4d egocentric dataset for category-level humanobject interaction. In _CVPR_ , 2022. 3, 1 

- [47] Yun Liu, Haolin Yang, Xu Si, Ling Liu, Zipeng Li, Yuxiang Zhang, Yebin Liu, and Li Yi. Taco: Benchmarking generalizable bimanual tool-action-object understanding. In _CVPR_ , 2024. 3, 1 

- [48] Zhenyang Liu, Yongchong Gu, Sixiao Zheng, Xiangyang Xue, and Yanwei Fu. Trivla: A unified triple-system-based unified vision-language-action model for general robot control. _arXiv preprint arXiv:2507.01424_ , 2025. 6 

- [49] Hao Luo, Yicheng Feng, Wanpeng Zhang, Sipeng Zheng, Ye Wang, Haoqi Yuan, Jiazheng Liu, Chaoyi Xu, Qin Jin, 

721 

and Zongqing Lu. Being-h0: Vision-language-action pretraining from large-scale human videos. _arXiv preprint arXiv:2507.15597_ , 2025. 2, 3, 5, 7, 1 

- [50] Hao Luo, Zihao Yue, Wanpeng Zhang, Yicheng Feng, Sipeng Zheng, Deheng Ye, and Zongqing Lu. Openmmego: Enhancing egocentric understanding for lmms with open weights and data. In _NIPS_ , 2025. 1 

- [51] Hao Luo, Ye Wang, Wanpeng Zhang, Haoqi Yuan, Yicheng Feng, Haiweng Xu, Sipeng Zheng, and Zongqing Lu. Jointaligned latent action: Towards scalable vla pretraining in the wild. _arXiv preprint arXiv:2602.21736_ , 2026. 2 

- [52] Hao Luo, Ye Wang, Wanpeng Zhang, Sipeng Zheng, Ziheng Xi, Chaoyi Xu, Haiweng Xu, Haoqi Yuan, Chi Zhang, Yiqing Wang, Yicheng Feng, and Zongqing Lu. Being-h0.5: Scaling human-centric robot learning for cross-embodiment generalization. _arXiv preprint arXiv:2601.12993_ , 2026. 2 

- [53] Teli Ma, Jia Zheng, Zifan Wang, Ziyao Gao, Jiaming Zhou, and Junwei Liang. Glover++: Unleashing the potential of affordance learning from human behaviors for robotic manipulation. _arXiv preprint arXiv:2505.11865_ , 2025. 3 

- [54] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ , 2022. 2, 3 

- [55] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ , 2024. 2 

- [56] Yaru Niu, Yunzhe Zhang, Mingyang Yu, Changyi Lin, Chenhao Li, Yikai Wang, Yuxiang Yang, Wenhao Yu, Tingnan Zhang, Bingqing Chen, et al. Human2locoman: Learning versatile quadrupedal manipulation with human pretraining. _arXiv preprint arXiv:2506.16475_ , 2025. 3 

- [57] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _RSS_ , 2024. 2 

- [58] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _ICRA_ , 2024. 2 

- [59] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 6 

- [60] Ri-Zhao Qiu, Shiqi Yang, Xuxin Cheng, Chaitanya Chawla, Jialong Li, Tairan He, Ge Yan, David J Yoon, Ryan Hoque, Lars Paulsen, et al. Humanoid policy˜ human policy. _arXiv preprint arXiv:2503.13441_ , 2025. 3 

- [61] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial represen- 

tations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 2, 6 

- [62] Ilija Radosavovic, Tete Xiao, Stephen James, Pieter Abbeel, Jitendra Malik, and Trevor Darrell. Real-world robot learning with masked visual pre-training. In _CoRL_ , 2023. 2 

- [63] Javier Romero, Dimitrios Tzionas, and Michael J. Black. Embodied hands: Modeling and capturing hands and bodies together. _ACM Transactions on Graphics, (Proc. SIGGRAPH Asia)_ , 2017. 3, 1 

- [64] Himanshu Gaurav Singh, Antonio Loquercio, Carmelo Sferrazza, Jane Wu, Haozhi Qi, Pieter Abbeel, and Jitendra Malik. Hand-object interaction pretraining from videos. _arXiv preprint arXiv:2409.08273_ , 2024. 3 

- [65] Lin Sun, Bin Xie, Yingfei Liu, Hao Shi, Tiancai Wang, and Jiale Cao. Geovla: Empowering 3d representations in visionlanguage-action models. _arXiv preprint arXiv:2508.09071_ , 2025. 2 

- [66] Gemini Team, Rohan Anil, Sebastian Borgeaud, JeanBaptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ , 2023. 1 

- [67] Weikang Wan, Haoran Geng, Yun Liu, Zikang Shan, Yaodong Yang, Li Yi, and He Wang. Unidexgrasp++: Improving dexterous grasping policy learning via geometryaware curriculum and iterative generalist-specialist learning. In _ICCV_ , 2023. 2 

- [68] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. Vggt: Visual geometry grounded transformer. In _CVPR_ , 2025. 2 

- [69] Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. In _Neurips_ , 2024. 2 

- [70] Qianqian Wang, Yifei Zhang, Aleksander Holynski, Alexei A Efros, and Angjoo Kanazawa. Continuous 3d perception model with persistent state. _arXiv preprint arXiv:2501.12387_ , 2025. 2, 4, 5 

- [71] Shuzhe Wang, Vincent Leroy, Yohann Cabon, Boris Chidlovskii, and Jerome Revaud. Dust3r: Geometric 3d vision made easy. In _CVPR_ , 2024. 2 

- [72] Weiyun Wang, Zhangwei Gao, Lixin Gu, Hengjun Pu, Long Cui, Xingguang Wei, Zhaoyang Liu, Linglin Jing, Shenglong Ye, Jie Shao, et al. Internvl3.5: Advancing open-source multimodal models in versatility, reasoning, and efficiency. _arXiv preprint arXiv:2508.18265_ , 2025. 6, 7 

- [73] Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025. 6 

- [74] Ye Wang, Sipeng Zheng, Hao Luo, Wanpeng Zhang, Haoqi Yuan, Chaoyi Xu, Haiweng Xu, Yicheng Feng, Mingyang Yu, Zhiyu Kang, et al. Rethinking visual-language-action model scaling: Alignment, mixture, and regularization. _arXiv preprint arXiv:2602.09722_ , 2026. 2 

- [75] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _ICLR_ , 2024. 2 

722 

- [76] Boshen Xu, Yuting Mei, Xinbi Liu, Sipeng Zheng, and Qin Jin. Egodtm: Towards 3d-aware egocentric video-language pretraining. _arXiv preprint arXiv:2503.15470_ , 2025. 2, 3 

- [77] Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, et al. Magma: A foundation model for multimodal ai agents. In _CVPR_ , 2025. 1 

- [78] Lihe Yang, Bingyi Kang, Zilong Huang, Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao. Depth anything: Unleashing the power of large-scale unlabeled data. In _CVPR_ , 2024. 2 

- [79] Jianglong Ye, Keyi Wang, Chengjing Yuan, Ruihan Yang, Yiquan Li, Jiyue Zhu, Yuzhe Qin, Xueyan Zou, and Xiaolong Wang. Dex1b: Learning with 1b demonstrations for dexterous manipulation. _arXiv preprint arXiv:2506.17198_ , 2025. 2 

- [80] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Se June Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, Lars Liden, Kimin Lee, Jianfeng Gao, Luke Zettlemoyer, Dieter Fox, and Minjoon Seo. Latent action pretraining from videos. In _ICLR_ , 2025. 2 

- [81] Haoqi Yuan, Bohan Zhou, Yuhui Fu, and Zongqing Lu. Cross-embodiment dexterous grasping with reinforcement learning. In _ICLR_ , 2025. 3 

- [82] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 2 

- [83] Xinyu Zhan, Lixin Yang, Yifei Zhao, Kangrui Mao, Hanlin Xu, Zenan Lin, Kailin Li, and Cewu Lu. Oakink2: A dataset of bimanual hands-object manipulation in complex task completion. In _CVPR_ , 2024. 3, 1 

- [84] Jiahui Zhang, Yurui Chen, Yueming Xu, Ze Huang, Yanpeng Zhou, Yu-Jie Yuan, Xinyue Cai, Guowei Huang, Xingyue Quan, Hang Xu, et al. 4d-vla: Spatiotemporal vision-language-action pretraining with cross-scene calibration. _arXiv preprint arXiv:2506.22242_ , 2025. 6 

- [85] Jinglei Zhang, Jiankang Deng, Chao Ma, and Rolandos Alexandros Potamias. Hawor: World-space hand motion reconstruction from egocentric videos. In _CVPR_ , 2025. 1 

   - [90] Hongxiang Zhao, Xingchen Liu, Mutian Xu, Yiming Hao, Weikai Chen, and Xiaoguang Han. Taste-rob: Advancing video generation of task-oriented hand-object interaction for generalizable robotic manipulation. In _CVPR_ , 2025. 3, 1 

   - [91] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, Ankur Handa, Ming-Yu Liu, Donglai Xiang, Gordon Wetzstein, and Tsung-Yi Lin. Cot-vla: Visual chainof-thought reasoning for vision-language-action models. In _CVPR_ , 2025. 6 

   - [92] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 2 

   - [93] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. TraceVLA: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. In _ICLR_ , 2025. 6 

   - [94] Sipeng Zheng, jiazheng liu, Yicheng Feng, and Zongqing Lu. Steve-eye: Equipping LLM-based embodied agents with visual perception in open worlds. In _ICLR_ , 2024. 1 

   - [95] Sipeng Zheng, Bohan Zhou, Yicheng Feng, Ye Wang, and Zongqing Lu. Unicode: Learning a unified codebook for multimodal large language models. In _ECCV_ , 2024. 1 

   - [96] Yifan Zhong, Xuchuan Huang, Ruochong Li, Ceyao Zhang, Yitao Liang, Yaodong Yang, and Yuanpei Chen. Dexgraspvla: A vision-language-action framework towards general dexterous grasping. _arXiv preprint arXiv:2502.20900_ , 2025. 2 

   - [97] Chenming Zhu, Tai Wang, Wenwei Zhang, Jiangmiao Pang, and Xihui Liu. Llava-3d: A simple yet effective pathway to empowering lmms with 3d-awareness. _arXiv preprint arXiv:2409.18125_ , 2024. 2 

   - [98] Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen Duan, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. _arXiv preprint arXiv:2504.10479_ , 2025. 1 

- [86] Wanpeng Zhang, Zilong Xie, Yicheng Feng, Yijiang Li, Xingrun Xing, Sipeng Zheng, and Zongqing Lu. From pixels to tokens: Byte-pair encoding on quantized visual modalities. _arXiv preprint arXiv:2410.02155_ , 2024. 1 

- [87] Wanpeng Zhang, Yicheng Feng, Hao Luo, Yijiang Li, Zihao Yue, Sipeng Zheng, and Zongqing Lu. Unified multimodal understanding via byte-pair visual encoding. In _ICCV_ , 2025. 1 

- [88] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, He Wang, Zhizheng Zhang, Li Yi, Wenjun Zeng, and Xin Jin. Dreamvla: A vision-language-action model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025. 2 

- [89] Wanpeng Zhang, Ye Wang, Hao Luo, Haoqi Yuan, Yicheng Feng, Sipeng Zheng, Qin Jin, and Zongqing Lu. Dig-flow: Discrepancy-guided flow matching for robust vla models. _arXiv preprint arXiv:2512.01715_ , 2025. 2 

723 

