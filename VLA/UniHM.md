---
title: "UniHM: Unified Dexterous Hand Manipulation with Vision Language Model"
date: "2026-02-28"
authors: "Zhenhao Zhang; Jiaxin Liu; Ye Shi; Jingya Wang"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2603.00732
pdf: https://arxiv.org/pdf/2603.00732
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.00732)** / [論文ページ](https://arxiv.org/abs/2603.00732)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

# UNIHM: UNIFIED DEXTEROUS HAND MANIPULATION WITH VISION LANGUAGE MODEL 

**Zhenhao Zhang**<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> **, Jiaxin Liu**<sup>1</sup><sup>_∗_</sup> **, Ye Shi**<sup>1</sup><sup>_,_2</sup><sup>_†_</sup> **, Jingya Wang**<sup>1</sup><sup>_,_2</sup><sup>_†_</sup> 

_{_ zhangzhh2024,liujx2024,shiye,wangjingya _}_ @shanghaitech.edu.cn 1 ShanghaiTech University 2 InstAdapt 

### ABSTRACT 

Planning physically feasible dexterous hand manipulation is a central challenge in robotic manipulation and Embodied AI. Prior work typically relies on objectcentric cues or precise hand-object interaction sequences, foregoing the rich, compositional guidance of open-vocabulary instruction. We introduce UniHM, the first framework for unified dexterous hand manipulation guided by free-form language commands. We propose a Unified Hand-Dexterous Tokenizer that maps heterogeneous dexterous-hand morphologies into a single shared codebook, improving cross-dexterous hand generalization and scalability to new morphologies. Our vision language action model is trained solely on human-object interaction data, eliminating the need for massive real-world teleoperation datasets, and demonstrates strong generalizability in producing human-like manipulation sequences from open-ended language instructions. To ensure physical realism, we introduce a physics-guided dynamic refinement module that performs segmentwise joint optimization under generative and temporal priors, yielding smooth and physically feasible manipulation sequences. Across multiple datasets and realworld evaluations, UniHM attains state-of-the-art results on both seen and unseen objects and trajectories, demonstrating strong generalization and high physical feasibility. Our project page at https://unihm.github.io/. 

### 1 INTRODUCTION 

Dexterous hand manipulation involves perceiving, grasping, and reconfiguring objects in complex environments. Generating and understanding diverse, long-horizon, and physically feasible dexterous-hand manipulation sequences are critical for advancing robotic capabilities in humanoidcentric applications. Such human-like interactions are ubiquitous in the real world and underpin fine-grained, complex tasks for embodied agents. 

Real-world manipulation tasks require sequential, contact-rich control that couples semantic intent ( _what to do_ ) with precise geometry and physics ( _how to do it_ ). Conventional methods (Wang et al., 2022; Xu et al., 2023; Li et al., 2025) either take object-centric inputs and optimize static grasp pose or transfer human-object interaction (HOI) video to fixed sequences. **Lacking open-vocabulary instruction** , these pipelines cannot guide diverse and complex dexterous hand manipulation. 

Recent vision-language approaches have begun to guide static grasping and manipulation by mapping free-form language to grasp representations. SemGrasp (Li et al., 2024b) uses a languagealigned discretization of the grasp space and fine-tunes a multimodal LLM so that text, object cues, and discrete grasp tokens lie in a shared semantic space, yielding language-conditioned static human grasp poses. AffordDexGrasp (Wei et al., 2025a) targets open-set generalization by predicting affordances from language and then generating dexterous grasps, with the primary output still being static pose rather than multi-step interaction. Despite advances in semantic controllability and openvocabulary coverage, most language-guided approaches focus on generating **static grasp poses** , ignore temporal structure, and therefore fail to produce smooth and rich manipulation sequences. 

Building on these observations, we propose **UniHM** , a unified framework for generating dexterous hand-manipulation sequences for both seen and unseen objects under open-vocabulary language in- 

> _∗_ Equal contribution; _†_ The corresponding author. 

1 

Published as a conference paper at ICLR 2026 


Figure 1: **Overview.** We introduce UniHM, the first unified hand-manipulation framework conditioned on free-form language. UniHM is trained solely on closed-set HOI datasets to follow target trajectories and execute physically feasible interactions, and generalizes to open-world tasks in realworld interactions. 

structions. Our approach couples a vision-language model with a Unified Hand-Dexterous Tokenizer and physics-guided dynamic refinement, which together enable two key capabilities: **1) Dynamic language-guided manipulation.** Prior methods typically either generate only static grasp poses or lack open-vocabulary language understanding; in contrast, we progressively train both the trajectory planner and the DexHand VLM, allowing the system to perform dynamic dexterous-hand manipulation along arbitrary planned trajectories with substantially improved temporal consistency and scalability. **2) Learning from video.** We leverage diverse, scene-rich human video data that contains abundant information about both environments and interactions(Zeng et al., 2025), enabling the model to synthesize human-like grasping poses while achieving strong generalization across a wide range of manipulation scenarios. Extensive real-world cross-embodiment experiments further demonstrate the effectiveness and generalization ability of this training paradigm. By integrating these components, **UniHM** achieves state-of-the-art performance and exhibits strong generalization across hand morphologies, object categories, task horizons, and linguistic complexity. 

Our contributions summaries are as follows: 

- **Unified Dexterous Hand Manipulation.** We introduce **UniHM** , the first unified, language-conditioned framework for dynamic dexterous hand manipulation beyond static grasps directly from images and open-vocabulary instructions. 

- **Morphology-Agnostic Codebook.** We introduce a unified VQ token codebook with crosshand consistency that maps heterogeneous hand kinematics into one discrete action lattice and decodes tokens into hand-specific joint trajectories, which enables direct token reuse and transfer across robotic and anthropomorphic hands. 

- **Physics-Guided Dynamic Trajectory Optimization.** We employ a tailored energy-based refinement that fuses a generative prior shaping feasible pose manifolds, a temporal prior enforcing smooth velocity–acceleration profiles and time-aware consistency, and contactaware dynamic trajectory optimization to optimize the generation result. 

- **Generalization without Teleoperation.** Our framework eliminates the dependency on expensive teleoperation data by learning dexterous manipulation skills from human videos. This paradigm achieves robust generalization to unseen scenes and instructions, significantly lowering the barrier to developing dexterous manipulation systems. 

2 

Published as a conference paper at ICLR 2026 

### 2 RELATED WORK 

#### 2.1 DEXTEROUS GRASP GENERATION. 

Research on dexterous grasping largely follows two lines. **Language-free** pipelines advance dexterous grasping without text by exploiting geometry, simulation, or video demonstrations. UniDexGrasp (Xu et al., 2023) learns from point clouds using a two-stage scheme that first proposes diverse grasp poses and then executes a goal-conditioned policy for stable lift, thereby generalizing across many categories. DexGraspNet (Wang et al., 2022) synthesizes and validates at scale via differentiable force-closure and collision checks to supervise grasp policies. DexMV (Qin et al., 2022) builds an imitation pipeline that converts human videos into robot demonstrations through pose estimation, retargeting, and demonstration translation for dexterous manipulation. **Language-guided** dexterous grasping aligns natural language with grasp spaces using discretization or affordance cues; for example, SemGrasp (Li et al., 2024b) learns a language-aligned discrete representation and uses a VLM to produce semantically consistent static dexterous grasp poses. DexGYS (Wei et al., 2024) introduces a language-guided dataset and model that maps commands to dexterous grasp poses. AffordDexGrasp (Wei et al., 2025a) leverages a generalizable, instructive affordance representation to guide open-set dexterous grasp generation. While these methods improve semantic controllability and open-vocabulary coverage, they remain pose-centric and typically generate **static poses** rather than sequence-level hand manipulation. 

#### 2.2 VISION LANGUAGE MODEL FOR MANIPULATION 

Generative vision-language model approaches increasingly cast manipulation as sequence prediction conditioned on vision and language. MotionGPT (Zhu et al., 2025) treats human motion as a language via VQ tokenization and unified text-motion modeling for sequence generation. HOIGPT (Huang et al., 2025) extends token-based generation to long 3D hand-object interaction, learning a bidirectional mapping between text and HOI sequences. OWG (Tziafas & Kasaei, 2024) composes VLM-guided referring segmentation, grounded grasp planning, and contact-aware ranking for zero-shot grasping rather than full sequence synthesis. ReKep (Huang et al., 2024) converts language/vision into relational keypoint constraints and solves actions via hierarchical optimization instead of an autoregressive policy. DexGrasp Anything (Zhong et al., 2025b) complements VLM pipelines with a physics-aware diffusion generator and the largest dexterous-grasp dataset to date, improving feasibility through explicit physical constraints. Multi-GraspLLM (Li et al., 2024a) aligns point-cloud and text features to generate language-guided grasp poses across multiple robotic hands within a single framework. Taken together, these generative models advance instruction following but predominantly target **Digital Hand, low-DoF grippers, or static grasp poses** ; explicit sequential dexterous-hand manipulation with feasibility remains limited, motivating our hand-agnostic tokenizer and physics-guided refinement. 

### 3 METHOD 

We propose **UniHM** , a unified framework for dexterous hand manipulation. UniHM first annotates large-scale hand-object interaction data, then employs a vision language model coupled with a Unified Hand-Dexterous Tokenizer to synthesize manipulation sequences, and finally applies physicsbased optimization to ensure physical feasibility. 

#### 3.1 AUTO DATA ANNOTATION 

**Open-vocabulary Language Annotation.** We annotated dexterous hand manipulation sequences with GPT-4o (Hurst et al., 2024). For each sequence, we provide keyframes as visual context, specifically the first and last frames and the three frames preceding first contact, and the model returns five distinct open-vocabulary natural language instructions. 

**Dexterous Hand Retargeting.** For HOI sequences to dexterous hand manipulation sequences transfer, we first apply Dex-Retargeting (Qin et al., 2023) to map MANO poses onto five dexterous robot hands (Shadow hand, Allegro hand, SVH hand, Leap hand and Panda hand). We then perform 

3 

Published as a conference paper at ICLR 2026 


Figure 2: **Pipeline.** UniHM converts open-vocabulary instructions and RGB-D inputs into executable dexterous-hand trajectories via three stages: (1) morphology-agnostic motion tokenization; (2) language-guided generation that fuses text, perception, and token history to produce manipulation token sequences; and (3) physics-aware decoding with smoothness/contact priors for feasible, stable execution. 

energy-based physical optimization to enforce feasibility, yielding physically consistent dexterous hand manipulation sequences. 

#### 3.2 UNIFIED HAND-DEXTEROUS TOKENIZER 

**Morphology-Agnostic Codebook.** We discretize dexterous hand poses and short motion segments across heterogeneous hand morphologies with a shared VQ-VAE (Van Den Oord et al., 2017) codebook. Let _Eh_ and _Dh_ denote the encoder and decoder for hand type _h_ (e.g., MANO or a specific robot hand), and let the global codebook be _Z_ = _{_ **e** _k}_<sup>_K_</sup> _k_ =1<sup>with</sup><sup>**e**</sup><sup>_k∈_R</sup><sup>_dz_.Given a sequence chunk</sup> **x**<sup>(</sup><sup>_h_)</sup> , we define the encoder output **z** _e_<sup>(</sup><sup>_h_)</sup> = _Eh_ ( **x**<sup>(</sup><sup>_h_)</sup> ) and the vector-quantization operator _Q_ ( _·_ ) that returns an index _c ∈{_ 1 _, . . . , K}_ : 


and the quantized representation is **z**<sup>(</sup> _q_<sup>_h_)</sup> = **e** _c_ . The reconstructed sequence chunk **x** ˆ<sup>(</sup><sup>_h_)</sup> is then 


So that every encoder _Eh_ maps to the same discrete index space and every decoder _Dh_ realizes the token within its own morphology. 

**Scalable Cross-Morphology Training.** To align representations across diverse hand types, we train our model in a staged, scalable manner. We first establish a reference encoder-decoder pair ( _E_ ref, _D_ ref) for a specific hand morphology, along with the shared codebook _Z_ . 

When integrating a new hand morphology, instead of direct non-differentiable token alignment, we first align the new encoder’s latent space with the reference encoder via knowledge distillation. This bypasses the gradient discontinuity of the quantization step. The distillation objective is: 


where _E_ new is the new encoder and _E_ ref is the pre-trained reference encoder. **x** new and **x** ref are corresponding hand sequences for the new and reference hands, respectively, obtained through retargeting. 

4 

Published as a conference paper at ICLR 2026 

After the new encoder is aligned, it is integrated into the full VQ-VAE training pipeline. The new encoder and its corresponding decoder are then fine-tuned with a combined objective that includes reconstruction and codebook-related terms. For a new hand type _h_ , the training objectives are: 


where sg[ _·_ ] denotes the stop-gradient operator and _β >_ 0 is a commitment weight. The total training objective for a new morphology is a combination of these terms, as well as the distillation loss for encoder alignment. 

**Unified Hand Pose Translation.** Because the encoders are aligned to a shared latent space and the decoders are mapped to the unified codebook, translating a pose from hand _i_ to hand _j_ is straightforward. We simply encode the source pose and decode using the target hand’s decoder: 


where **x**<sup>(</sup><sup>_i_)</sup> is the source hand pose and **x** ˆ<sup>(</sup><sup>_j_)</sup> is the retargeted pose for the target hand. 

#### 3.3 DEXTEROUS-HAND MANIPULATION WITH VLM 

**Network structure of VLM.** Given the scarcity of HOI and dynamic dexterous-hand data and the high cost of collecting it, training large multimodal language models (e.g., 7B or 13B parameters) is data-inefficient and yields limited performance in this regime(Zeng et al., 2026; Wang et al., 2026; He et al., 2025; Zhong et al., 2025a). We therefore adopt **Qwen3-0.6B** as the base model, whose scale enables stable convergence on HOI and dexterous-hand datasets. To compensate for the lack of dynamic manipulation data while retaining strong visual grounding, We adopt a decoupled architecture that separates scene perception from HOI sequence generation. A CLIPort-style vision module consumes RGB-D images and language to infer target trajectories, and an MLP-based trajectory encoder serializes these targets for the VLM. The main VLM focuses on instruction-conditioned token generation with a progressive masking curriculum, and the unified tokenizer maps tokens to hand-specific poses across different robotic hands. At inference time, only the CLIPort perception head is adapted to distribution shifts, which improves data efficiency and robustness while keeping the HOI generator unchanged. 

**Unified Dexterous Manipulation.** We first use a CLIPort model to take an RGB-D image and its corresponding instruction (e.g., “grasp the bottle into the box”) as input. The model then decodes a target execution trajectory _T_ tar. This process can be formally described as 


The target trajectory is denoted by _T_ tar = _{T_ tar<sup>1</sup><sup>_, . . . , T_</sup> tar<sup>_K},_</sup> _T_ tar<sup>_i∈_SE(3)</sup><sup>_,_where</sup><sup>_K_is the length of</sup> the total sequence. 

We leverage RGB-D data to reconstruct the scene point cloud and then use Point-SAM to segment the object point cloud _P_ obj with the corresponding semantics. 


_P_ obj denotes the point cloud of the target object. Specifically, _P_ obj _∈_ R<sup>3</sup><sup>_×l_</sup> is a set of _l_ 3D coordinates ( _x, y, z_ ), where _l_ is the number of points in the point cloud. 

Next, the initial hand pose is encoded by _Ej_ ( _·_ ) and concatenated with _T_ tar, _P_ obj, and text token _T_ . This combined input is then fed into a Vision Language Model (VLM) to obtain a code sequence in the VQ-VAE latent space. Finally, we use the decoder of the target hand, _Dh_ ( _·_ ), to decode the corresponding q-positions: 


**Training Stage.** When fine-tuning the main model, we input the real object sequence trajectory as a target trajectory into the large model. To enable the model to understand the spatial continuity of 

5 

Published as a conference paper at ICLR 2026 

hand poses, we initially input the ground truth hand poses and the VQ-VAE as an encoder into the model. As training progresses, we use masking to randomly occlude a portion of the hand poses, replacing the masked poses with a unified, learnable token, until all hand poses are masked (Liu et al., 2019; Oquab et al., 2023). 

The masking process can be expressed as: 


where _Q_ is the ground truth hand pose sequence, _E_ is the VQ-VAE encoder, _M_ is a binary mask, and _T_ mask is the learnable token. 

**Inference Stage.** Our training and inference pipelines differ by design. During training, we condition the model on ground-truth target trajectories and object point clouds, enabling it to reliably generate physically feasible dexterous-hand manipulation sequences that follow the specified targets. At inference, a separate CLIPort module estimates these quantities from RGB-D observations, decoupling spatial perception from hand–object interaction. This modularization allows the main model to focus solely on HOI sequence generation. A practical advantage is robustness to environmental shift: when the scene distribution changes, we fine-tune only CLIPort, which is smaller and less data-hungry, rather than the entire model. 

#### 3.4 PHYSICAL-GUIDED DYNAMIC REFINEMENT 

To bridge the gap between the generated grasping trajectory _Q_ gen and the object point cloud _P_ obj under the target pose trajectory _T_ tar( _t_ ), we formulate a posterior optimization. We solve a spatiotemporally regularized, frame-by-frame Gauss–Newton problem that enforces physical plausibility while preserving the semantic intent of the generated actions. We proceed frame-by-frame: at time _t_ , we optimize _qt_ while treating _qt_<sup>opt</sup> _−_ 1<sup>and</sup><sup>_q_</sup> _t_<sup>opt</sup> _−_ 2<sup>as fixed from previous steps.</sup> 

**Contact Energy.** Let _si_ ( _qt_ ) be the _i_ -th fingertip position from forward kinematics in the world frame. We transform it into the object frame using _T_ tar( _t_ )<sup>_−_1</sup> and query the nearest neighbor ( **p** _i,_ **n** _i_ ) on _P_ obj, where **n** _i_ is the local surface normal. We define a signed point-to-plane distance (Grant et al., 2012): 


and an asymmetric, smooth penalty that is continuous and slope-matched at _d_ = 0, which is essential during the optimization: 


where _α >_ 0 and _k >_ 0 are scale parameters. Stacking per-fingertip residuals yields: 


with _λc >_ 0 controlling the contact strength. 

**Generative HOI Prior.** To preserve the intent of the generative model, we penalize deviations from the generated configuration _qt_<sup>gen:</sup> 


where **W** gen _≻_ **0** is a symmetric positive-definite weighting matrix. We use the weighted norm shorthand _∥x∥_<sup>2</sup> **W**<sup>≜</sup><sup>_x_T</sup><sup>**W**</sup><sup>_x_below.</sup> 

**Temporal Prior.** We regularize first- and second-order temporal differences to ensure smooth, coherent motion: 


6 

Published as a conference paper at ICLR 2026 

Table 1: Main Result on DexYCB. The arrow pointing to the right means closer to the GT. 

||Method|MPJPE_↓_|FOL_↓_|FPL_↓_|FID _↓_|Diversity_→_|
|---|---|---|---|---|---|---|
||GT|-<br>|-<br>|-<br>|-<br>|125.53<br>|
||TM2T(Guo et al.,2022)|85.33<sup>_±_3.41</sup>|36.57<sup>_±_1.46</sup>|24.10<sup>_±_0.96</sup>|54.83<sup>_±_2.19</sup>|37.12<sup>_±_1.48</sup>|
|**en**|MDM(Tevet et al.,2023)|88.06<sup>_±_3.52</sup><br>|33.40<sup>_±_1.34</sup><br>|23.06<sup>_±_0.92</sup><br>|52.33<sup>_±_2.09</sup><br>|33.95<sup>_±_1.36</sup><br>|
|**Se**|FlowMDM(Barquero et al.,2024)|82.75<sup>_±_3.31</sup><br>|31.24<sup>_±_1.25</sup><br>|21.55<sup>_±_0.86</sup><br>|48.05<sup>_±_1.92</sup><br>|61.25<sup>_±_2.45</sup><br>|
||MotionGPT3(Zhu et al.,2025)|74.80<sup>_±_2.99</sup>|28.76<sup>_±_1.15</sup>|19.32<sup>_±_0.77</sup>|43.35<sup>_±_1.73</sup>|**72.51**<sup>_±_2.90</sup>|
||**Ours**|**61.40**<sup>_±_1.93</sup>|**23.14**<sup>_±_0.65</sup>|**12.15**<sup>_±_0.24</sup>|**31.24**<sup>_±_1.02</sup>|39.62<sup>_±_0.66</sup>|
||TM2T(Guo et al.,2022)|94.22<sup>_±_3.77</sup>|37.25<sup>_±_1.49</sup>|27.03<sup>_±_1.08</sup>|55.94<sup>_±_2.24</sup>|31.25<sup>_±_1.25</sup>|
|**en**|MDM(Tevet et al.,2023)|93.05<sup>_±_3.72</sup>|39.04<sup>_±_1.56</sup>|25.89<sup>_±_1.04</sup>|55.13<sup>_±_2.21</sup>|29.0<sup>_±_1.16</sup>|
|**se**|FlowMDM(Barquero et al.,2024)|86.13<sup>_±_3.45</sup><br>|32.67<sup>_±_1.31</sup><br>|24.09<sup>_±_0.96</sup><br>|51.33<sup>_±_2.05</sup><br>|58.21<sup>_±_2.33</sup><br>|
|**Un**|MotionGPT3(Zhu et al.,2025)|77.93<sup>_±_3.12</sup><br>|30.55<sup>_±_1.22</sup><br>|21.48<sup>_±_0.86</sup><br>|46.14<sup>_±_1.85</sup><br>|**75.84**<sup>_±_3.03</sup><br>|
||**Ours**|**63.56**<sup>_±_2.08</sup>|**27.29**<sup>_±_0.43</sup>|**13.06**<sup>_±_0.43</sup>|**41.03**<sup>_±_1.65</sup>|42.70<sup>_±_1.19</sup>|


The per-frame objective is the sum of all terms: 


Here the prior terms enter both as quadratic regularizers on the left and as linear gradients on the right, stabilizing the optimization while respecting the generated intent and temporal smoothness under the object’s target pose trajectory _T_ tar( _t_ ). 

### 4 EXPERIMENTS 

Our framework comprises three components: (1) we annotate hand-object interaction (HOI) sequences with a vision language model (VLM) and, via retargeting plus physics-based refinement, obtain manipulation sequences for multiple dexterous hands; (2) we train a Unified Hand-Dexterous Tokenizer together with an VLM for text-to-hand manipulation sequence generation; and (3) we apply an energy-based physical refinement and validate feasibility in simulation. Comparative experiments and ablations demonstrate the effectiveness of our approach. All experiments are conducted on NVIDIA A100 GPUs. 

#### 4.1 DATASET 

In our experiments, we evaluate on two of the most widely used datasets. **DexYCB** (Chao et al., 2021) is a multi-view RGB-D dataset of human grasps on YCB objects with precise 3D labels: 582K frames, 1,000 sequences, 10 subjects, 20 objects, and 8 views; benchmarks include 2D/6D object pose, 3D hand pose, and handover. **OakInk** (Yang et al., 2022) A large-scale hand-object interaction repository integrating OakInk-Image (230K multi-view frames from 12 subjects manipulating 100 objects across 32 categories) and OakInk-Shape (3D grasp-pose meshes with affordance labels), plus 50K affordance-aware interactions transferred via Tink. For both **DexYCB** and **OakInk** , we adopt an 80/20 split: 80% for training/validation (seen) and 20% held out as an unseen test set. This protocol enables a rigorous assessment of generalization across seen and unseen objects, trajectories, and interaction patterns for UniHM. 

#### 4.2 EVALUATION METRIC 

To assess the quality, diversity, realism, and physical plausibility of our generated dexterous-hand manipulation sequences, we adopt a multi-pronged evaluation protocol that follows prior work (Wei 

7 

Published as a conference paper at ICLR 2026 

Table 2: Main Result on OakInk. The arrow pointing to the right means closer to the GT. 

||Method|MPJPE_↓_|FOL_↓_|FPL_↓_|FID _↓_|Diversity_→_|
|---|---|---|---|---|---|---|
||GT|-<br>|-<br>|-<br>|-<br>|147.40<br>|
||TM2T(Guo et al.,2022)|71.08<sup>_±_2.84</sup>|91.25<sup>_±_3.65</sup>|34.51<sup>_±_1.38</sup>|311.90<sup>_±_12.48</sup>|277.38<sup>_±_11.10</sup>|
|**en**|MDM(Tevet et al.,2023)|67.55<sup>_±_2.70</sup>|93.8<sup>_±_3.75</sup>|30.06<sup>_±_1.20</sup>|285.22<sup>_±_11.41</sup>|275.42<sup>_±_11.02</sup>|
|**Se**|FlowMDM(Barquero et al.,2024)|60.74<sup>_±_2.43</sup>|85.43<sup>_±_3.42</sup>|26.47<sup>_±_1.06</sup>|249.08<sup>_±_9.96</sup>|189.54<sup>_±_7.58</sup>|
||MotionGPT3(Zhu et al.,2025)|56.29<sup>_±_2.25</sup>|79.24<sup>_±_3.17</sup>|23.98<sup>_±_0.96</sup>|221.10<sup>_±_8.84</sup>|247.10<sup>_±_9.88</sup>|
||**Ours**|**52.73**<sup>_±_2.08</sup>|**72.32**<sup>_±_0.55</sup>|**19.86**<sup>_±_1.38</sup>|**204.91**<sup>_±_7.64</sup>|**165.47**<sup>_±_6.30</sup>|
||TM2T(Guo et al.,2022)|75.34<sup>_±_3.01</sup>|125.33<sup>_±_5.01</sup>|45.51<sup>_±_1.82</sup>|337.08<sup>_±_13.48</sup>|362.08<sup>_±_14.48</sup>|
|**en**|MDM(Tevet et al.,2023)|72.90<sup>_±_2.92</sup>|112.94<sup>_±_4.52</sup>|42.93<sup>_±_1.72</sup>|325.58<sup>_±_13.02</sup>|354.93<sup>_±_14.20</sup>|
|**se**|FlowMDM(Barquero et al.,2024)|65.39<sup>_±_2.62</sup>|101.25<sup>_±_4.05</sup>|36.14<sup>_±_1.45</sup>|298.04<sup>_±_11.92</sup>|224.67<sup>_±_8.99</sup>|
|**Un**|MotionGPT3(Zhu et al.,2025)|61.95<sup>_±_2.48</sup>|93.65<sup>_±_3.75</sup>|28.25<sup>_±_1.13</sup>|272.69<sup>_±_10.91</sup>|316.58<sup>_±_12.66</sup>|
||**Ours**|**58.62**<sup>_±_2.35</sup>|**83.27**<sup>_±_1.17</sup>|**22.87**<sup>_±_0.52</sup>|**253.41**<sup>_±_13.05</sup>|**153.28**<sup>_±_9.48</sup>|


Table 3: Real-World Experiments 

||||Su|ccess Rate||
|---|---|---|---|---|---|
|Split|Method|Grab|Pick&Place|Pull&Push|Open&Close|
|**n**|MDM+Dex-Retargeting|20%|10%|0%|5%|
|**ee**|MotionGPT3+Dex-Retargeting|30%|15%|25%|25%|
|**S**|**Ours**|**65%**|**50%**|**60%**|**55%**|
|**en**|MDM+Dex-Retargeting|5%|0%|0%|5%|
|**nse**|MotionGPT3+Dex-Retargeting|45%|25%|15%|20%|
|**U**|**Ours**|**60%**|**35%**|**55%**|**45%**|


et al., 2025a; Zhang et al., 2025; Deng et al., 2025; Ji et al., 2025; Liu et al., 2025; Wang et al., 2025b; Jian et al., 2025; Wei et al., 2025b) and combines quantitative and qualitative measures across five metrics. 

- **Physically Feasible.** Mean Per-Joint Position Error **(MPJPE)** for hand joints, Final Position Location Error **(FPL)** and Final Orientation Location Error **(FOL)** for dexterous hand placement and orientation. **Success Rate** means the Real-world grasping success rate. 

- **Generation Realism.** Fr´echet Inception Distance **(FID)** between real and synthesized. **Diversity,** which measures the variability across different prompts and within outputs from the same prompt 

Lower MPJPE, FPL, FOL, and FID indicate higher accuracy and fidelity. Diversity closer to the ground truth indicates a more reasonable generation. 

#### 4.3 MAIN RESULT 

**Comparison with SOTA Methods.** We conduct extensive comparisons against prior state-of-theart methods(i.e.,TM2T (Guo et al., 2022), MDM (Tevet et al., 2023), FlowMDM (Barquero et al., 2024), MotionGPT3 (Zhu et al., 2025)) on both DexYCB (Chao et al., 2021) and OakInk (Yang et al., 2022). Because prior action-generation baselines lack explicit physical-feasibility guarantees, we post-process their outputs with our physics-guided refinement to ensure a fair comparison. As shown in Table 1 and Table 2, our method consistently outperforms all baselines across both seen and unseen objects. 

These results unequivocally affirm our method as cutting-edge, showcasing the robust generalization capability of our VLM framework and physical refinement, thereby substantiating the efficacy of our UniHM synthesis framework in producing sequential hand manipulation sequences for both seen and unseen objects and trajectories guided by open-vocabulary instructions. 

**Visualization in Real-world Results.** We conduct real-world evaluations on a dexterous hand across both seen and unseen objects and trajectories. Results show improvements in grasp success rate and grasp quality. As summarized in Table 3, **UniHM** achieves a higher success rate than prior methods, and Fig.D2 presents qualitative visualizations of our real-world grasps. 

8 

Published as a conference paper at ICLR 2026 


Figure 3: **Real-World Results.** UniHM achieves higher success rates than prior methods on both seen and unseen objects, producing physically consistent and executable real-world manipulations. 

Table 4: Ablation Result on DexYCB. The arrow pointing to the right means closer to the GT. 

||Method|MPJPE_↓_|FOL_↓_|FPL_↓_|FID _↓_|Diversity_→_|
|---|---|---|---|---|---|---|
||GT|-|-|-|-|125.53|
|**n**|w/o Depth Input|85.47<sup>_±_3.42</sup><br>|33.41<sup>_±_1.34</sup><br>|20.97<sup>_±_0.84</sup><br>|56.36<sup>_±_2.25</sup><br>|66.40<sup>_±_2.66</sup><br>|
|**ee**|w/o Masked Training|73.41<sup>_±_2.94</sup><br>|28.22<sup>_±_1.13</sup><br>|14.42<sup>_±_0.58</sup><br>|44.87<sup>_±_1.79</sup><br>|**73.09**<sup>_±_2.92</sup><br>|
|**S**|w/o Physical Refinement|65.78<sup>_±_2.63</sup><br>|25.06<sup>_±_1.00</sup><br>|15.35<sup>_±_0.61</sup><br>|33.57<sup>_±_1.34</sup><br>|38.06<sup>_±_1.52</sup><br>|
||**Ours**|**61.40**<sup>_±_1.93</sup><br>|**23.14**<sup>_±_0.65</sup><br>|**12.15**<sup>_±_0.24</sup><br>|**31.24**<sup>_±_1.02</sup><br>|39.62<sup>_±_0.66</sup><br>|
|**n**|w/o Depth Input|90.12<sup>_±_3.60</sup><br>|39.77<sup>_±_1.59</sup><br>|21.70<sup>_±_0.87</sup><br>|77.38<sup>_±_3.10</sup><br>|67.53<sup>_±_2.70</sup><br>|
|**ee**|w/o Masked Training|74.63<sup>_±_2.99</sup><br>|28.08<sup>_±_1.12</sup><br>|17.25<sup>_±_0.69</sup><br>|43.09<sup>_±_1.72</sup><br>|**74.88**<sup>_±_3.00</sup><br>|
|**ns**|w/o Physical Refinement|65.39<sup>_±_2.62</sup>|28.55<sup>_±_1.14</sup>|16.05<sup>_±_0.64</sup>|45.06<sup>_±_1.80</sup>|41.03<sup>_±_1.64</sup>|
|**U**|**Ours**|**63.56**<sup>_±_2.08</sup>|**27.29**<sup>_±_0.43</sup>|**13.06**<sup>_±_0.43</sup>|**41.03**<sup>_±_1.65</sup>|42.70<sup>_±_1.19</sup>|


#### 4.4 ABLATION STUDY 

We conduct controlled ablation studies on **DexYCB** (Chao et al., 2021) to verify the necessity of each module. Each component is essential for **UniHM** to synthesize realistic and physically feasible dexterous hand manipulation sequences; the details can be found in Table 4. 

**Masked Training (w/o Masked Training).** We adopt a progressive masking curriculum for language-conditioned sequence generation. Training starts with the teacher forcing the use of both language and ground-truth sequences, then gradually replaces a fraction _pt_ of ground truth with [MASK]. As _pt_ increases from 0 to 1, the model relies on language and its autoregressive history; the final stage uses language only, matching inference. This reduces exposure bias and improves sequential stability while retaining strong supervision early on. 

**RGB-D or RGB Input (w/o Depth Input).** To better estimate object poses and reconstruct scene point clouds, we adopt RGB-D inputs and infer scene trajectories with a language-conditioned visuomotor module. When RGB-D is replaced by RGB-only, pose estimation and 3D reconstruction degrade substantially. 

**Physical Refinement (w/o Physical Refinement).** Physical refinement is a postprocessing step that makes a plausible plan physically valid for dexterous hands. We run a lightweight simulation-based optimization that adjusts poses, contacts, and timing to reduce collisions and slips, enforce joint and torque limits, and improve stability. The objective penalizes penetration, excessive contact forces, and abrupt accelerations while staying close to the original. 

9 

Published as a conference paper at ICLR 2026 

### 5 CONCLUSION 

We present **UniHM** , a unified framework for synthesizing sequential dexterous hand-manipulation sequences guided by open-vocabulary instructions. UniHM couples a Unified Hand-Dexterous Tokenizer, which utilizes a shared codebook with cross-hand code distillation to form a common discrete action space, with a vision language model for instruction-grounded token generation. It applies a physical-guided dynamic refinement, yielding semantically aligned and physically consistent trajectories across heterogeneous robotic hands. Extensive evaluations of DexYCB and OakInk, along with simulation checks and real-world trials, demonstrate strong generalization to unseen objects and trajectories, and validate the contribution of each component through ablations. While UniHM advances language-conditioned dexterous manipulation beyond pose-centric grasp generation, several challenges remain: reliance on RGB-D perception without tactile or force sensing, simplified energy terms for contact and friction, and limited coverage of bimanual or tool-use scenarios. Future work will incorporate richer contact priors and feedback, scale the unified codebook to more hand morphologies, and close the loop with online adaptation to better handle sequential, contact-rich tasks. 

### ACKNOWLEDGEMENT 

This work was supported by National Natural Science Foundation of China (62406195, 62303319), ShanghaiTech AI4S Initiative SHTAI4S202404, HPC Platform of ShanghaiTech University, and MoE Key Laboratory of Intelligent Perception and Human-Machine Collaboration (ShanghaiTech University), and Shanghai Engineering Research Center of Intelligent Vision and Imaging. This work was also supported in part by computational resources provided by Fcloud CO., LTD. 

10 

Published as a conference paper at ICLR 2026 

### REFERENCES 

- German Barquero, Sergio Escalera, and Cristina Palmero. Seamless human motion composition with blended positional encodings. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 457–469, 2024. 

- Yu-Wei Chao, Wei Yang, Yu Xiang, Pavlo Molchanov, Ankur Handa, Jonathan Tremblay, Yashraj S. Narang, Karl Van Wyk, Umar Iqbal, Stan Birchfield, Jan Kautz, and Dieter Fox. DexYCB: A benchmark for capturing hand grasping of objects. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2021. 

- Zekai Deng, Ye Shi, Kaiyang Ji, Lan Xu, Shaoli Huang, and Jingya Wang. Human-object interaction via automatically designed vlm-guided motion policy, 2025. URL https://arxiv.org/ abs/2503.18349. 

- Darion Grant, James Bethel, and Melba Crawford. Point-to-plane registration of terrestrial laser scans. _ISPRS Journal of Photogrammetry and Remote Sensing_ , 72:16–26, 2012. 

- Chuan Guo, Xinxin Zuo, Sen Wang, and Li Cheng. Tm2t: Stochastic and tokenized modeling for the reciprocal generation of 3d human motions and texts. In _European Conference on Computer Vision_ , pp. 580–597. Springer, 2022. 

- Peiqi He, Zhenhao Zhang, Yixiang Zhang, Xiongjun Zhao, and Shaoliang Peng. Spatial-ormllm: Improve spatial relation understanding in the operating room with multimodal large language model, 2025. URL https://arxiv.org/abs/2508.08199. 

- Mingzhen Huang, Fu-Jen Chu, Bugra Tekin, Kevin J Liang, Haoyu Ma, Weiyao Wang, Xingyu Chen, Pierre Gleize, Hongfei Xue, Siwei Lyu, Kris Kitani, Matt Feiszli, and Hao Tang. Hoigpt: Learning long sequence hand-object interaction with language models, 2025. 

- Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Li Fei-Fei. Rekep: Spatiotemporal reasoning of relational keypoint constraints for robotic manipulation. _arXiv preprint arXiv:2409.01652_ , 2024. 

- Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. _arXiv preprint arXiv:2410.21276_ , 2024. 

- Kaiyang Ji, Ye Shi, Zichen Jin, Kangyi Chen, Lan Xu, Yuexin Ma, Jingyi Yu, and Jingya Wang. Towards immersive human-x interaction: A real-time framework for physically plausible motion synthesis, 2025. URL https://arxiv.org/abs/2508.02106. 

- Juntao Jian, Yi-Lin Wei, Chengjie Mou, Yuhao Lin, Xing Zhu, Yujun Shen, Wei-Shi Zheng, and Ruizhen Hu. Zerodexgrasp: Zero-shot task-oriented dexterous grasp synthesis with prompt-based multi-stage semantic reasoning, 2025. URL https://arxiv.org/abs/2511.13327. 

- Haosheng Li, Weixin Mao, Weipeng Deng, Chenyu Meng, Haoqiang Fan, Tiancai Wang, Yoshie Osamu, Ping Tan, Hongan Wang, and Xiaoming Deng. Multi-graspllm: A multimodal llm for multi-hand semantic guided grasp generation. _arXiv preprint arXiv:2412.08468_ , 2024a. 

- Kailin Li, Jingbo Wang, Lixin Yang, Cewu Lu, and Bo Dai. Semgrasp: Semantic grasp generation via language aligned discretization. In _European Conference on Computer Vision_ , pp. 109–127. Springer, 2024b. 

- Kailin Li, Puhao Li, Tengyu Liu, Yuyang Li, and Siyuan Huang. Maniptrans: Efficient dexterous bimanual manipulation transfer via residual learning. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025. 

- Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. Roberta: A robustly optimized bert pretraining approach. _arXiv preprint arXiv:1907.11692_ , 2019. 

- Zhirui Liu, Kaiyang Ji, Ke Yang, Jingyi Yu, Ye Shi, and Jingya Wang. Commanding humanoid by free-form language: A large language action model with unified motion vocabulary, 2025. URL https://arxiv.org/abs/2511.22963. 

11 

Published as a conference paper at ICLR 2026 

- Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J Black. Smpl: A skinned multi-person linear model. In _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ , pp. 851–866. 2023. 

- Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- Charles R Qi, Hao Su, Kaichun Mo, and Leonidas J Guibas. Pointnet: Deep learning on point sets for 3d classification and segmentation. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 652–660, 2017a. 

- Charles Ruizhongtai Qi, Li Yi, Hao Su, and Leonidas J Guibas. Pointnet++: Deep hierarchical feature learning on point sets in a metric space. _Advances in neural information processing systems_ , 30, 2017b. 

- Yuzhe Qin, Yueh-Hua Wu, Shaowei Liu, Hanwen Jiang, Ruihan Yang, Yang Fu, and Xiaolong Wang. Dexmv: Imitation learning for dexterous manipulation from human videos. In _European Conference on Computer Vision_ , pp. 570–587. Springer, 2022. 

- Yuzhe Qin, Wei Yang, Binghao Huang, Karl Van Wyk, Hao Su, Xiaolong Wang, Yu-Wei Chao, and Dieter Fox. Anyteleop: A general vision-based dexterous robot arm-hand teleoperation system. In _Robotics: Science and Systems_ , 2023. 

- Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words with subword units. _arXiv preprint arXiv:1508.07909_ , 2015. 

- Guy Tevet, Sigal Raab, Brian Gordon, Yoni Shafir, Daniel Cohen-or, and Amit Haim Bermano. Human motion diffusion model. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Georgios Tziafas and Hamidreza Kasaei. Towards open-world grasping with large vision-language models. _arXiv preprint arXiv:2406.18722_ , 2024. 

- Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

- Hanqing Wang, Shaoyang Wang, Yiming Zhong, Zemin Yang, Jiamin Wang, Zhiqing Cui, Jiahao Yuan, Yifan Han, Mingyu Liu, and Yuexin Ma. Affordance-r1: Reinforcement learning for generalizable affordance reasoning in multimodal large language model, 2025a. URL https://arxiv.org/abs/2508.06206. 

- Hanqing Wang, Zhenhao Zhang, Kaiyang Ji, Mingyu Liu, Wenti Yin, Yuchao Chen, Zhirui Liu, Xiangyu Zeng, Tianxiang Gui, and Hangxing Zhang. Dag: Unleash the potential of diffusion model for open-vocabulary 3d affordance grounding, 2025b. URL https://arxiv.org/ abs/2508.01651. 

- Hanqing Wang, Yuan Tian, Mingyu Liu, Zhenhao Zhang, and Xiangyang Zhu. Sdeval: Safety dynamic evaluation for multimodal large language models, 2026. URL https://arxiv. org/abs/2508.06142. 

- Ruicheng Wang, Jialiang Zhang, Jiayi Chen, Yinzhen Xu, Puhao Li, Tengyu Liu, and He Wang. Dexgraspnet: A large-scale robotic dexterous grasp dataset for general objects based on simulation. _arXiv preprint arXiv:2210.02697_ , 2022. 

- Zifan Wang, Junyu Chen, Ziqing Chen, Pengwei Xie, Rui Chen, and Li Yi. Genh2r: learning generalizable human-to-robot handover via scalable simulation demonstration and imitation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 16362– 16372, 2024. 

- Yi-Lin Wei, Jian-Jian Jiang, Chengyi Xing, Xian-Tuo Tan, Xiao-Ming Wu, Hao Li, Mark Cutkosky, and Wei-Shi Zheng. Grasp as you say: Language-guided dexterous grasp generation. _Advances in Neural Information Processing Systems_ , 37:46881–46907, 2024. 

12 

Published as a conference paper at ICLR 2026 

- Yi-Lin Wei, Mu Lin, Yuhao Lin, Jian-Jian Jiang, Xiao-Ming Wu, Ling-An Zeng, and Wei-Shi Zheng. Afforddexgrasp: Open-set language-guided dexterous grasp with generalizable-instructive affordance. _arXiv preprint arXiv:2503.07360_ , 2025a. 

- Yi-Lin Wei, Zhexi Luo, Yuhao Lin, Mu Lin, Zhizhao Liang, Shuoyu Chen, and Wei-Shi Zheng. Omnidexgrasp: Generalizable dexterous grasping via foundation model and force feedback, 2025b. URL https://arxiv.org/abs/2510.23119. 

- Shijie Wu, Yihang Zhu, Yunao Huang, Kaizhen Zhu, Jiayuan Gu, Jingyi Yu, Ye Shi, and Jingya Wang. Afforddp: Generalizable diffusion policy with transferable affordance, 2025. URL https://arxiv.org/abs/2412.03142. 

- Fanbo Xiang, Yuzhe Qin, Kaichun Mo, Yikuan Xia, Hao Zhu, Fangchen Liu, Minghua Liu, Hanxiao Jiang, Yifu Yuan, He Wang, et al. Sapien: A simulated part-based interactive environment. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 11097– 11107, 2020. 

- Peng Xiang, Xin Wen, Yu-Shen Liu, Yan-Pei Cao, Pengfei Wan, Wen Zheng, and Zhizhong Han. SnowflakeNet: Point cloud completion by snowflake point deconvolution with skip-transformer. In _Proceedings of the IEEE International Conference on Computer Vision (ICCV)_ , 2021. 

- Peng Xiang, Xin Wen, Yu-Shen Liu, Yan-Pei Cao, Pengfei Wan, Wen Zheng, and Zhizhong Han. Snowflake point deconvolution for point cloud completion and generation with skip-transformer. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 45(5):6320–6338, 2023. doi: 10.1109/TPAMI.2022.3217161. 

- Yinzhen Xu, Weikang Wan, Jialiang Zhang, Haoran Liu, Zikang Shan, Hao Shen, Ruicheng Wang, Haoran Geng, Yijia Weng, Jiayi Chen, et al. Unidexgrasp: Universal robotic dexterous grasping via learning diverse proposal generation and goal-conditioned policy. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 4737–4746, 2023. 

- Lixin Yang, Kailin Li, Xinyu Zhan, Fei Wu, Anran Xu, Liu Liu, and Cewu Lu. Oakink: A large-scale knowledge repository for understanding hand-object interaction. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 20953–20962, 2022. 

- Zuyao You and Zuxuan Wu. Seg-r1: Segmentation can be surprisingly simple with reinforcement learning, 2025. URL https://arxiv.org/abs/2506.22624. 

- Hao Yu and Bogdan M Wilamowski. Levenberg–marquardt training. In _Intelligent systems_ , pp. 12–1. CRC Press, 2018. 

- Xiangyu Zeng, Kefan Qiu, Qingyu Zhang, Xinhao Li, Jing Wang, Jiaxin Li, Ziang Yan, Kun Tian, Meng Tian, Xinhai Zhao, Yi Wang, and Limin Wang. Streamforest: Efficient online video understanding with persistent event memory, 2025. URL https://arxiv.org/abs/2509. 24871. 

- Xiangyu Zeng, Zhiqiu Zhang, Yuhan Zhu, Xinhao Li, Zikang Wang, Changlian Ma, Qingyu Zhang, Zizheng Huang, Kun Ouyang, Tianxiang Jiang, Ziang Yan, Yi Wang, Hongjie Zhang, Yali Wang, and Limin Wang. Video-o3: Native interleaved clue seeking for long video multi-hop reasoning, 2026. URL https://arxiv.org/abs/2601.23224. 

- Zhenhao Zhang, Ye Shi, Lingxiao Yang, Suting Ni, Qi Ye, and Jingya Wang. Openhoi: Openworld hand-object interaction synthesis with multimodal large language model. _arXiv preprint arXiv:2505.18947_ , 2025. 

- Ming Zhong, Yuanlei Wang, Liuzhou Zhang, Arctanx An, Renrui Zhang, Hao Liang, Ming Lu, Ying Shen, and Wentao Zhang. Vcu-bridge: Hierarchical visual connotation understanding via semantic bridging, 2025a. URL https://arxiv.org/abs/2511.18121. 

- Yiming Zhong, Qi Jiang, Jingyi Yu, and Yuexin Ma. Dexgrasp anything: Towards universal robotic dexterous grasping with physics awareness. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 22584–22594, 2025b. 

- Bingfan Zhu, Biao Jiang, Sunyi Wang, Shixiang Tang, Tao Chen, Linjie Luo, Youyi Zheng, and Xin Chen. Motiongpt3: Human motion as a second modality. _arXiv preprint arXiv:2506.24086_ , 2025. 

13 

Published as a conference paper at ICLR 2026 

## **UniHM: Unified Dexterous Hand Manipulation with Vision Language Model Appendix** 

A USE OF LLMS 

We used an GPT to polish the experiments and introduction sections. We also use the Nano to generate the icon in Figure 1. 

### B IMPLEMENTATION DETAILS 

#### B.1 RETARGETING 

**Hand Pose Retargeting.** The DexYCB (Chao et al., 2021) and OakInk (Yang et al., 2022) datasets provide MANO pose sequences (Loper et al., 2023), object point clouds, and associated object trajectories. We employ Dex-Retargeting (Qin et al., 2023) to map MANO joint configurations to multiple robotic hands via a differentiable inverse-kinematics objective with joint limits and devicespecific kinematic calibration. Given a MANO pose _q_ MANO( _t_ ), the device configuration is: 


where _fk_ denote forward-kinematics constraints on fingertip/phalange keypoints, _ϕ_ dev aligns MANO and device frames and scales link lengths, and _q_ prev is the previous solution for temporal smoothness. We generate retargeted sequences for Allegro, Shadow, Schunk, LEAP, and Ability hands, and for the Panda gripper (mapping the thumb-index aperture to a scalar opening width via linear scaling with clamping). 

**Target Trajectory Generation.** Let _M_ ext _∈ SE_ (3) denote the camera extrinsics that map world coordinates to the camera frame, and let _T_ obj<sup>cam(</sup><sup>_t_)</sup><sup>_∈SE_(3) be the object pose in the camera frame</sup> at time _t_ . The object target trajectory in the world frame used during training is 


We time-align _T_ tar( _t_ ) with the retargeted hand poses using the dataset timestamps. 

#### B.2 UNIFIED HAND TOKENIZER 

**Unified Codebook Training.** We adopt a shared VQ-VAE codebook _Z_ = _{_ **e** _k}_<sup>_K_</sup> _k_ =1<sup>initialized with</sup> Shadow Hand due to its data availability and wildly used. For any hand type _h_ , denote its encoder and decoder by _Eh_ and _Dh_ . Given an input sequence chunk **x**<sup>(</sup><sup>_h_)</sup> , the encoder output, quantization, and reconstruction follow the main text: 


where _Q_ ( _·_ ) performs a nearest neighbor lookup in the codebook, finding the code vector with the minimum squared Euclidean distance. We train with the standard reconstruction and VQ losses: 


where sg[ _·_ ] is the stop-gradient operator and _β >_ 0 is the commitment weight. 

1 

Published as a conference paper at ICLR 2026 

To avoid codebook collapse with a purely statistical procedure, we maintain a “cold-code” table based on per-epoch usage counts. Let _n_<sup>(</sup> _k_<sup>_t_)</sup> be the usage of code _k_ during epoch _t_ , computed from token indices _{c_<sup>(</sup> _b_<sup>_t_)</sup><sup>_}_</sup> _b_<sup>_B_</sup> =1<sup>(</sup><sup>_t_):</sup> 


where 1 ( _·_ ) denotes the indicator function that evaluates to 1 if the condition inside its brackets is true, and 0 otherwise. Define the cold set at epoch _t_ by a count threshold _τc_ : 


At scheduled refresh epochs _t ∈E_ reset, we selectively update only the codes belonging to the cold set. Collect a buffer _B_<sup>(</sup><sup>_t_)</sup> of encoder outputs since the previous refresh and run K-Means with _R_ = �� _S_ ( _t_ )�� to obtain centroids _{_ **_µ_** _r}rR_ =1<sup>.Wedirectlyreplacethecoldcodeswiththenewly</sup> computed centroids. With an injective assignment _π_ : _S_<sup>(</sup><sup>_t_)</sup> _→{_ 1 _, . . . , R}_ : 


Thus, only the codes in the cold-code table are refreshed at those epochs, while frequently used codes remain unchanged. The objective for this stage is: 


**Multi-Encoder and Decoder Training.** To integrate a new hand morphology, we first align the new encoder to the reference encoder via retargeted pairs. Let _E_ ref be the reference (Shadow Hand) encoder and ( **x** new _,_ **x** ref ) be a retargeted pair: 


After encoder alignment, we train the new encoder–decoder pair within the shared VQ-VAE using the same reconstruction and VQ losses: 


, where _λ_ distill _≥_ 0 controls the contribution of the distillation term during the encoder alignment stage. 

**Training Details.** We train a unified codebook with capacity _K_ = 8192 on DexYCB sequences. Since the inputs are 1D pose and short-motion signals, we instantiate encoders/decoders with either MLP or 1D convolutional backbones and ablate both choices, as shown in Table B1. When training the reference encoder, we set the _β_ = 0 _._ 25 and train the network with a learning rate 1 _e −_ 4. We also update the codebook at epochs 50 _,_ 100 _,_ 150 _, ..._ . For the multi-encoder and multi-decoder training, the cold-code threshold _τc_ is set to 1, and the distillation weight _λ_ distill is set to 0.1. 

Table B1: A comparison of the validation set performance for the MLP and 1D-Conv models. 

|||Allegro|Shadow|Schunk|LEAP|Ability|Panda Gripper|Overall|
|---|---|---|---|---|---|---|---|---|
||MLP|0.0268|0.0450|0.0293|0.0348|0.0432|0.0221|0.0350|
|MAE|1D-Conv|**0.0216**|**0.0297**|**0.0221**|**0.0257**|**0.0327**|**0.0182**|**0.0256**|
||MLP|0.0545|0.0886|0.0656|0.0656|0.0913|0.0630|0.0736|
|RMSE|1D-Conv|**0.0465**|**0.0654**|**0.0551**|**0.0531**|**0.0705**|**0.0519**|**0.0581**|


#### B.3 PHYSICAL OPTIMIZATION 

**Physical Model.** We expand the contact term used in the per-frame objective. Let _si_ ( _qt_ ) denote the _i_ -th fingertip position (forward kinematics) in the world frame and _T_ tar( _t_ )<sup>_−_1</sup> be the object-frame transform at time _t_ . Query the nearest neighbor ( **p** _i,_ **n** _i_ ) on _P_ obj in the object frame, and define the signed point-to-plane distance: 


2 

Published as a conference paper at ICLR 2026 

We adopt an asymmetric, smooth penalty _f_ ( _d_ ) that is continuous and slope-matched at _d_ = 0: 


At _d_ = 0, _f_ is continuous and has matched first derivatives: 

_d_ lim _→_ 0<sup>_± f_(</sup><sup>_d_) = 0</sup><sup>_,_</sup> _d_ lim _→_ 0<sup>+</sup><sup>_f ′_(</sup><sup>_d_) = 0</sup><sup>_,_</sup> _d_ lim _→_ 0<sup>_−f ′_(</sup><sup>_d_) =</sup><sup>_α_</sup> _k_<sup>(1</sup><sup>_−e−k·_0) = 0</sup><sup>_._</sup> (B17) 

Moreover, _f_<sup>_′′_</sup> (0<sup>_−_</sup> ) = _f_<sup>_′′_</sup> (0<sup>+</sup> ) = _αe_<sup>_−k·_0</sup> _≥_ 0, so _f_ is twice-differentiable and convex. Stacking per-fingertip residuals gives: 


with _λc >_ 0. For Gauss–Newton, we linearize the residuals at the current iterate. Let _xi_ ( _qt_ ) = _T_ tar( _t_ )<sup>_−_1</sup> _si_ ( _qt_ ) and _Jx,i_ ( _qt_ ) = _∂xi/∂qt_ (the kinematic Jacobian in the object frame). Treating ( **p** _i,_ **n** _i_ ) as fixed within an inner iteration: 


which yields the contact Jacobian rows that form _Jt_ = _∂r_ contact( _qt_ ) _/∂qt_ with a small _ϵ >_ 0. 

**Generative Prior and Temporal Prior.** We keep the generative and temporal priors from the main text and unify their roles as dynamic smoothers from two information sources—semantic intent (generator) and history (velocity/acceleration). The generative prior anchors _qt_ to _qt_<sup>gen:</sup> 


The temporal prior penalizes first- and second-order differences: 

_E_ time( _qt, qt_<sup>opt</sup> _−_ 1<sup>_, q_</sup> _t_<sup>opt</sup> _−_ 2<sup>) =</sup><sup><u>1</u></sup> 2<sup>_∥qt −q_</sup> _t_<sup>opt</sup> _−_ 1<sup>_∥_2</sup> **W** vel<sup>+</sup> 2<sup><u>1</u></sup><sup>_∥_(</sup><sup>_qt −q_</sup> _t_<sup>opt</sup> _−_ 1<sup>)</sup><sup>_−_(</sup><sup>_q_</sup> _t_<sup>opt</sup> _−_ 1<sup>_−q_</sup> _t_<sup>opt</sup> _−_ 2<sup>)</sup><sup>_∥_2</sup> **W** acc<sup>_,_</sup> (B21) 

where **W** vel _≻_ **0** and **W** acc _≻_ **0** (often **W** vel = _λ_ vel _I_ , **W** acc = _λ_ acc _I_ ). Define the per-frame objective: 

_Et_ ( _qt, qt_<sup>gen</sup><sup>_, q_</sup> _t_<sup>opt</sup> _−_ 1<sup>_, q_</sup> _t_<sup>opt</sup> _−_ 2<sup>) =</sup><sup>_E_contact(</sup><sup>_qt_) +</sup><sup>_E_gen(</sup><sup>_qt, q_</sup> _t_<sup>gen) +</sup><sup>_E_time(</sup><sup>_qt, q_</sup> _t_<sup>opt</sup> _−_ 1<sup>_, q_</sup> _t_<sup>opt</sup> _−_ 2<sup>)</sup><sup>_._</sup> (B22) 

Let _r_ contact( _qt_ ) denote the stacked contact residuals. Linearizing _r_ contact( _qt_ + ∆ _qt_ ) _≈ r_ contact( _qt_ ) + _Jt_ ∆ _qt_ and expanding the two quadratic priors around _qt_ give: 

_Et_ ( _qt_ + ∆ _qt_ ) _≈_<sup><u>1</u></sup> 2<sup>_∥r_contact(</sup><sup>_qt_) +</sup><sup>_Jt_∆</sup><sup>_qt∥_</sup> 2<sup>2+</sup><sup><u>1</u></sup> 2<sup>∆</sup><sup>_q_</sup> _t_<sup>T(</sup><sup>**W**gen+</sup><sup>**W**vel+</sup><sup>**W**acc)∆</sup><sup>_qt_+ ∆</sup><sup>_q_</sup> _t_<sup>T</sup> **W**<sup>˜</sup> _,_ (B23) where: 

**W** ˜ ≜ **W** gen( _qt − qt_<sup>gen) +</sup><sup>**W**vel(</sup><sup>_qt−q_</sup> _t_<sup>opt</sup> _−_ 1<sup>) +</sup><sup>**W**acc((</sup><sup>_qt −q_</sup> _t_<sup>opt</sup> _−_ 1<sup>)</sup><sup>_−_(</sup><sup>_q_</sup> _t_<sup>opt</sup> _−_ 1<sup>_−q_</sup> _t_<sup>opt</sup> _−_ 2<sup>))</sup><sup>_._</sup> (B24) 

Setting the gradient w.r.t. ∆ _qt_ to zero and adding Levenberg–Marquardt damping _λ ≥_ 0 yields the normal equations: 


**Optimization Procedure.** Given the decoded grasping trajectory _Q_ gen, the object point cloud _P_ obj, and the target pose trajectory _T_ tar( _t_ ), we refine each frame by Gauss–Newton with LM damping while freezing nearest-neighbor correspondences inside each inner iteration. In our implementation, we set _α_ = _k_ = 1 and use a small positive constant _ϵ_ to handle cases where _f_ ( _d_ ) approaches zero. 

In practical environments, obtaining precise point clouds is often challenging. A significant advantage of employing the kernel function _f_ ( _d_ ) is the inherent robustness it provides to the segmentation process. 

As shown in Fig. B1, the kernel function is relatively flat in a neighborhood of _d_ = 0, which implies that, even when the segmented point cloud is contaminated with noise, the resulting cost term does not deviate substantially from that constructed from the ground-truth point cloud, and thus the optimization still converges to the correct solution in the presence of noisy inputs. We further demonstrate the optimization results under noisy conditions (for a clearer illustration of the grasp point, we have omitted the remaining structure of the dexterous hand, plotting only the object point cloud and the positions of the hand’s fingers), as shown in Fig. B2. 

3 

Published as a conference paper at ICLR 2026 

**Algorithm 1** Physical-guided dynamic refinement **Require:** Generated sequence _Q_ gen = _{qt_<sup>gen</sup><sup>_}T_</sup> _t_ =0<sup>,pointcloud</sup><sup>_P_obj,targetposes</sup><sup>_{T_tar(</sup><sup>_t_)</sup><sup>_}_</sup> _t_<sup>_T_</sup> =0<sup>,</sup> weights _λc_ , **W** gen, **W** vel, **W** acc, damping _λ ≥_ 0 **Ensure:** Refined sequence _Q_ opt = _{qt_<sup>opt</sup><sup>_}T_</sup> _t_ =0 1: Set boundary priors _q−_<sup>opt</sup> 2<sup>=</sup><sup>_q_</sup> _−_<sup>opt</sup> 1<sup>=</sup><sup>_q_</sup> 0<sup>gen</sup> 2: **for** _t_ = 0 to _T_ **do** 3: Initialize _qt ← qt_<sup>gen</sup> 4: **repeat** 5: Transform fingertips _xi_ ( _qt_ ) = _T_ tar( _t_ )<sup>_−_1</sup> _si_ ( _qt_ ) 6: For each fingertip _i_ , find ( **p** _i,_ **n** _i_ ) = NN( _xi_ ( _qt_ ) _, P_ obj) and determine inside/outside sign 7: Compute _di_ ( _qt_ ), _r_ contact( _qt_ ), and _Jt_ = _∂r_ contact _/∂qt_ with correspondences fixed 8: Form **W**<sup>˜</sup> using _qt_ , _qt_<sup>opt</sup> _−_ 1<sup>,</sup><sup>_q_</sup> _t_<sup>opt</sup> _−_ 2 9: Solve ( _Jt_<sup>T</sup><sup>_Jt_+</sup><sup>**W**gen+</sup><sup>**W**vel+</sup><sup>**W**acc+</sup><sup>_λI_)∆</sup><sup>_qt_=</sup><sup>_−J_</sup> _t_<sup>T</sup><sup>_r_contact(</sup><sup>_qt_)</sup><sup>_−_</sup> **W**<sup>˜</sup> 10: Update: _qt ← qt_ + ∆ _qt_ ; adjust _λ_ by decrease/increase of _Et_ 11: **until** converged or max iters 12: _qt_<sup>opt</sup> _← qt_ 13: **end for** 


Figure B1: The function plots under varying values of _α_ and _k_ are displayed. Note that _α_ and _k_ control the curve behavior for _x >_ 0 and _x <_ 0, respectively. For comparison, the curve of _y_ = _|x|_ is plotted using a dashed line. 

4 

Published as a conference paper at ICLR 2026 


Figure B2: Optimization results when the point cloud includes noise. Here, the black points represent the object point cloud, and the red/green points denote the positions of the dexterous hand’s fingertips. (A) Optimization using the _f_ ( _d_ ) kernel, visualized on the noisy input. (B) Optimization using the Euclidean distance, visualized on the noisy input. (C) The _f_ ( _d_ ) kernel optimization result projected onto the clean noise-free point cloud. (D) The Euclidean distance optimization result projected onto the noise-free point cloud. 

### C MODEL INSTRUCTION 

#### C.1 TEXT TOKENIZER 

We employ a pretrained language model from the Qwen series, specifically Qwen3, as the core component for our language input pipeline. This choice is motivated by its strong performance across a wide range of natural language tasks and its robust, efficient tokenizer. 

The Qwen3 tokenizer operates on a byte-level Byte-Pair Encoding algorithm (Sennrich et al., 2015). This method ensures that all possible input characters are representable, and it is particularly effective at handling diverse linguistic inputs, including code and technical terms, without resorting to unknown tokens. The tokenizer’s vocabulary size is _Vtok_ , and each input sequence _S_ is tokenized into a sequence of tokens _T_ = ( _t_ 1 _, t_ 2 _, . . . , tN_ ), where _N_ is the sequence length. The tokenization process can be formally expressed as: 


This token sequence _T_ is then converted into a sequence of token embeddings, which serve as the input to the subsequent layers of our model. We utilize the tokenizer’s built-in padding and truncation functionalities to handle variable-length sequences, ensuring a consistent input shape for the model. 

#### C.2 POINT CLOUD ENCODER 

We use a PointNet-based architecture (Qi et al., 2017a;b) as our point cloud feature extractor, which is a key component of our model. The network directly consumes raw point cloud data, which is an unordered set of _n_ points, with each point represented by its ( _x, y, z_ ) coordinates. The PointNet architecture addresses the permutation invariance of point clouds by using a symmetric function to aggregate information from each point. 

5 

Published as a conference paper at ICLR 2026 

Specifically, the network first applies a shared multi-layer perceptron to each point individually to transform the input features. This is followed by a max-pooling layer, which acts as a symmetric function to aggregate the point-wise features into a global feature vector. This process can be concisely described as: 


where _X_ = _{x_ 1 _, . . . , xn}_ is the input point cloud, _h_ represents the shared MLP, and _f_ ( _X_ ) is the resulting global feature vector. The network is configured to output several feature vectors, which are then concatenated and fed into the subsequent main model for further processing. 

#### C.3 TRAJECTORY ENCODER 

Our model takes the target trajectory _T_ tar as input. We encode this trajectory using a two-layer MLP to obtain a feature representation **z** ( _t_ ). The MLP processes the pose **p** tar( _t_ ) at each timestep _t_ and is defined as: 


where _σ_ 1 and _σ_ 2 are non-linear activation functions. The hidden layer dimension is set to 512 during training. 

#### C.4 MASKED TRAINING 

During training, we progressively mask the ground truth hand poses to encourage the model to learn the temporal relationships within a sequence. This approach, which has been shown to be highly effective in fields like language modeling (e.g., BERT (Liu et al., 2019)) and computer vision (e.g., DINOv2 (Oquab et al., 2023)), allows the model to generate hand poses from a given context. 

Specifically, we feed the ground truth trajectory into the VQ-VAE encoder and then use a mask to conceal the corresponding hand poses. The masked hand pose tokens are replaced with a single, learnable token. This masking process can be formalized as: 


where _Q_ is the ground truth hand pose sequence, _E_ is the VQ-VAE encoder, _M_ is a binary mask, and _T_ mask is the learnable token. 

We implement this masking strategy with a progressive curriculum across training epochs. For the first 20% of epochs, we do not mask any hand poses. From 20% to 80% of the epochs, we linearly increase the masking ratio until it reaches 100%. Finally, during the last 20% of epochs, all hand poses are consistently masked, forcing the network to perform full generation. We train the model for 100 epochs using the AdamW optimizer with a learning rate of 1e-4. 

#### C.5 TARGET TRAJECTORY PLANER 

We use CLiPort to plan the target trajectory _Ttar_ . Specifically, we take RGB-D and instructions as input data. Then, based on GenH2R (Wang et al., 2024), we generate a smooth trajectory in the output space, which is then encoded using the aforementioned trajectory encoder and fed into the model. 

### D ADDITIONAL VISUALIZATION 

We employ Sapien (Xiang et al., 2020) as a visualization engine for observing and validating the generated results. We also present some additional visualizations here. 

### E REAL-WORLD SETUP 

The experimental setup utilizes a Franka manipulator arm equipped with Panda Hand, an XHand dexterous hand, and Inspire Hand in Fig.E1. The 7-degree-of-freedom (DoF) Franka provides a 

6 

Published as a conference paper at ICLR 2026 


Figure D1: The visualization results of our grasping sequence in Sapien. More real world examples could be found in the video. 


Figure D2: The visualization results of our grasping sequence in Sapien. More real world examples could be found in the video. 

7 

Published as a conference paper at ICLR 2026 

workspace comparable to that of a human arm. The 2-DOF Panda Hand, 12-DOF XHand, and 6-DOF Inspire Hand, with overall dimensions similar to a human hand, feature a proportionally elongated pinky finger. This specific design requires an adaptive scaling heuristic to ensure natural and fluid motion. 

We employ a Zed camera to acquire RGB-D observations, apply PointSAM(You & Wu, 2025; Wang et al., 2025a; Wu et al., 2025) to segment the target point cloud, and subsequently leverage SnowflakeNet (Xiang et al., 2023; 2021) to reconstruct a complete point cloud that serves as input to our model. 


Figure E1: Real-World Cross-embodiment Set up 

F EVALUATION METRIC 

**MPJPE (Mean Per-Joint Position Error).** For each sequence, we compute the Euclidean error of every hand joint in every frame, Then average over joints and time: 


The final MPJPE reported 


where _N_ is the number of test sequences. **FPL (Final Position Location Error)** FPL measures how close the final hand placement is to the ground truth. Let _c_<sup>(</sup> _T_<sup>_i_)and ˆ</sup><sup>_c_(</sup> _T_<sup>_i_)be the 3D positions of the</sup> hand root / palm center at the last frame _Ti_ of sequence _i_ : 


**FOL (Final Orientation Location Error).** FOL measures the orientation error of the hand at the final frame. Let _RT_<sup>(</sup><sup>_i_</sup> _i_<sup>)and</sup><sup>_R_ˆ</sup> _T_<sup>(</sup><sup>_i_</sup> _i_<sup>)be the ground-truth and predicted rotation matrices of the hand root;</sup> 

8 

Published as a conference paper at ICLR 2026 

the orientation error is 


converted to degrees. We report 


**Feature extractor.** We first embed every hand-object interaction sequence _x_ (either real or generated) using a pretrained motion encoder _f_ ( _·_ ) that consumes the full temporal joint trajectory (and object pose) and outputs a fixed-dimensional feature vector _z_ = _f_ ( _x_ ) _∈_ R<sup>_d_</sup> . We use the same encoder for all methods and compute all distributional metrics in this learned feature space. 

**FID (Fr´echet Inception Distance).** Let _{zk_<sup>real</sup><sup>_}M_</sup> _k_ =1<sup>_r_bethefeaturesofrealtestsequencesand</sup> _{zk_<sup>gen</sup><sup>_}M_</sup> _k_ =1<sup>_g_the features of generated sequences.We estimate the empirical means and covariances:</sup> 


and compute 


**Diversity.** Diversity measures how varied the generated sequences are in the same feature space. Given the set of features _{zk}_<sup>_M_</sup> _k_ =1<sup>for a method, we compute</sup> 


9 

