---
title: "XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations"
date: "2025-11-04"
authors: "Shichao Fan; Kun Wu; Zhengping Che; Xinhua Wang; Di Wu; Fei Liao"
venue: "Submitted to ICLR 2026 / ICML 2026"
url: https://arxiv.org/abs/2511.02776
pdf: https://arxiv.org/pdf/2511.02776
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.02776)** / [論文ページ](https://arxiv.org/abs/2511.02776)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

**Shichao Fan**<sup>* 1</sup> **Kun Wu**<sup>* 1</sup> **Zhengping Che**<sup>* † 1</sup> **Xinhua Wang**<sup>1</sup> **Di Wu**<sup>1 2</sup> **Fei Liao**<sup>1</sup> **Ning Liu**<sup>1</sup> **Yixue Zhang**<sup>1</sup> **Zhen Zhao**<sup>1</sup> **Zhiyuan Xu**<sup>1</sup> **Meng Li**<sup>1</sup> **Qingjie Liu**<sup>3</sup> **Shanghang Zhang**<sup>2</sup> **Min Wan**<sup>4</sup> **Jian Tang**<sup>�1</sup> 


_Figure 1._ We introduce **X Robotic Model 1 (XR-1)** , a versatile and scalable vision-language-action framework. XR-1 supports robust multi-task learning across diverse robot embodiments and environments. 

# **Abstract** 

Recent progress in large-scale robotic datasets and vision-language models (VLMs) has advanced research on vision-language-action (VLA) models. However, existing VLA models still face two fundamental challenges: ( _i_ ) producing precise low-level actions from high-dimensional ob- 

*Equal contribution. †Project leader. � Corresponding author. 1Beijing Innovation Center of Humanoid Robotics, Beijing, China 2State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University, Beijing, China 3State Key Laboratory of Virtual Reality Technology and Systems, SCSE, Beihang University, Beijing, China<sup>4</sup> School of Mechanical Engineering and Automation, Beihang University, Beijing, China. Correspondence to: Jian Tang _<_ jian.tang@x-humanoid.com _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

servations, ( _ii_ ) bridging domain gaps across heterogeneous data sources, including diverse robot embodiments and human demonstrations. Existing methods often encode latent variables from either visual dynamics or robotic actions to guide policy learning, but they fail to fully exploit the complementary multi-modal knowledge present in large-scale, heterogeneous datasets. In this work, we present **X Robotic Model 1 (XR-1)** , a novel framework for versatile and scalable VLA learning across diverse robots, tasks, and environments. At its core, XR-1 introduces the _Unified Vision-Motion Codes (UVMC)_ , a discrete latent representation learned via a dual-branch VQ-VAE that jointly encodes visual dynamics and robotic motion. UVMC addresses these challenges by ( _i_ ) serving as an intermediate representation between the observations and actions, and ( _ii_ ) aligning mul- 

1 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

timodal dynamic information from heterogeneous data sources to capture complementary knowledge. To effectively exploit UVMC, we propose a _three-stage training paradigm_ : ( _i_ ) self-supervised UVMC learning, ( _ii_ ) UVMC-guided pretraining on large-scale cross-embodiment robotic datasets, and ( _iii_ ) task-specific post-training. We validate XR-1 through extensive real-world experiments with more than 14,000 rollouts on six different robot embodiments, spanning over 120 diverse manipulation tasks. XR-1 consistently outperforms state-of-the-art baselines such as _π_ 0 _._ 5, _π_ 0, RDT, UniVLA, and GR00T-N1.5 while demonstrating strong generalization to novel objects, background variations, distractors, and illumination changes. Our project is at https://xr-1vla.github.io/. 

# **1. Introduction** 

The long-term goal of Embodied AI (Pfeifer & Iida, 2004) is to develop generalist agents capable of executing diverse natural language instructions across real-world settings, such as households, factories, and hospitals. Recent advancements in Vision-Language Models (VLMs) (Bai et al., 2023; Gao et al., 2024; Li et al., 2023; Liu et al., 2023; Zhang et al., 2024; Beyer et al., 2024; Wang et al., 2024b) demonstrate that large-scale pre-training on internet data provides robust visual-semantic understanding. Building on this, VisionLanguage-Action (VLA) models (Zitkovich et al., 2023; Kim et al., 2024; Black et al., 2025; Liu et al., 2025; Wen et al., 2025a; Cheang et al., 2025a; Liu et al., 2026a; Lee et al., 2025; Intelligence et al., 2025; Bu et al., 2025b) incorporate action heads to ground perception and language into executable motor commands. 

VLA training typically follows a two-stage pipeline: ( _i_ ) large-scale pre-training on cross-embodiment datasets (Walke et al., 2023; O’Neill et al., 2024; Wu et al., 2025a) to learn general priors, and ( _ii_ ) task-specific post-training. Despite VLM advancements, two challenges persist: ( _i_ ) Precision Gap: Mapping high-dimensional observations to precise low-level actions is difficult due to multimodal uncertainty; even centimeter-level errors lead to failure in dexterous or contact-rich tasks. ( _ii_ ) Data Heterogeneity: Cross-embodiment transfer is hindered by morphological differences (hardware and DoF) and the lack of explicit action labels or visual alignment in human demonstration videos. 

To address these challenges, prior research (Cui et al., 2023; Shafiullah et al., 2022; Lee et al., 2024; Xie et al., 2025; Zheng et al., 2025) has explored latent representations as intermediate abstractions. Current directions either encode ac- 

tion sequences for motion modeling (Shafiullah et al., 2022; Wu et al., 2025b; Bauer et al., 2025), which requires costly labeled data, or encode visual dynamics from videos (Cui et al., 2023; Hu et al., 2025; Bu et al., 2025a), which lacks explicit action grounding. Both approaches treat vision and action in isolation, failing to capture the multimodal alignment necessary for task-relevant correspondences. In contrast, humans fuse heterogeneous sensory inputs into _supramodal codes_ (Park et al., 2025), abstracting embodiment-specific details while preserving task semantics. Inspired by this, we argue that robotic representation learning must move beyond unimodal abstractions toward a joint encoding of visual dynamics and motor control. 

Addressing the limitations of unimodal representations and inspired by human supramodal cognition, we propose X Robotic Model 1 (XR-1) to achieve cross-data exploitation and cross-embodiment control. Central to our framework is Unified Vision-Motion Codes (UVMC), a discrete latent representation that jointly captures visual dynamics and robotic motion. UVMC is learned via a dual-branch VQ-VAE where vision and motion branches share a unified latent space to enforce cross-modal consistency. To suppress task-irrelevant visual noise and ensure the extraction of motion-centric features, we introduce a vision-motion alignment loss that regularizes visual codes to align with their corresponding motion counterparts. Building upon UVMC, XR-1 employs a three-stage paradigm: ( _i_ ) selfsupervised UVMC learning on large-scale robot and human video datasets; ( _ii_ ) cross-embodiment pre-training that injects UVMC knowledge into a VLM via learnable tokens; and ( _iii_ ) task-specific post-training for refinement. This architecture allows XR-1 to leverage heterogeneous data while ensuring embodiment-agnostic consistency. 

We extensively evaluate XR-1 through more than 14k rollouts across six distinct robot embodiments, including Tien Kung 1.0/2.0, Single-/Dual-Arm UR-5e, Dual-Arm Franka, and AgileX Cobot Magic 2.0, covering over 120 manipulation tasks. XR-1 outperforms state-of-the-art baselines such as _π_ 0 _._ 5, _π_ 0, RDT, UniVLA, and GR00T-N1.5 across challenging scenarios involving bimanual collaboration, dexterous manipulation, deformable objects, contact-rich interactions, dynamic settings, and long-horizon manipulation. Our main contributions are summarized as follows: 

- We propose **X Robotic Model 1 (XR-1)** , a scalable three-stage framework for VLA learning that effectively leverages heterogeneous data sources, including Internet-scale human videos and diverse robot datasets, and integrates with diverse VLA architectures. 

- We introduce the _Unified Vision-Motion Codes (UVMC)_ , a discrete latent representation that encodes both environmental dynamics and robotic motion, 

2 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

while an alignment loss enforces consistent multimodal embeddings across embodiments via UVMC. 

- We validate XR-1 with over 14 _,_ 000 real-world rollouts on six robot embodiments across 123 tasks, and demonstrate that it consistently outperforms strong baselines such as _π_ 0 _._ 5, _π_ 0, RDT, UniVLA, and GR00T-N1.5. 

# **2. Related Work** 

## **2.1. Vision-Language-Action Models** 

Modern robotics aims to develop robust, general-purpose Vision-Language-Action (VLA) policies capable of zeroshot cross-embodiment transfer. While early Imitation Learning (IL) methods relied on narrow demonstrations (Cui et al., 2023; Zhao et al., 2023; Chi et al., 2023; Ze et al., 2024; Fu et al., 2024; Bharadhwaj et al., 2024; Ze et al., 2024; Cao et al., 2025; Su et al., 2025; Fan et al., 2025), scalability and generalization remained limited. This bottleneck has been addressed by large-scale datasets, such as BridgeData (Ebert et al., 2022; Walke et al., 2023), DROID (Khazatsky et al., 2024), Open X-Embodiment (O’Neill et al., 2024), RoboMIND (Wu et al., 2025a), and AgiBot World (Bu et al., 2025a), which catalyzed the transition to generalist policies. Key advancements include RT-1 (Brohan et al., 2023) and RT2 (Zitkovich et al., 2023), which unified vision-language pretraining with action generation. Subsequent frameworks like RT-X (O’Neill et al., 2024) and Octo (Team et al., 2024b) further embraced data heterogeneity, while PaLM-E (Driess et al., 2023) utilized visual-conditioned LLMs to enhance complex task planning and semantic grounding. 

Beyond core training paradigms, research has focused on augmenting VLA models with extensive world knowledge and diverse capabilities through internet-scale representations. Recent advancements include CrossFormer (Zhang & Yan, 2023), OpenVLA (Kim et al., 2024), HPT (Wang et al., 2024a), _π_ 0 (Black et al., 2025), RDT (Liu et al., 2025), TinyVLA (Wen et al., 2025b), GR00T (Bjorck et al., 2025), HybridVLA (Liu et al., 2026a), SwitchVLA (Li et al., 2025a), MLA (Liu et al., 2026b), and X-VLA (Zheng et al., 2026). Specifically, _π_ 0 _._ 5 (Intelligence et al., 2025) and FSD (Yuan et al., 2026) leverage image-text pre-training for grounding, while CoT-VLA (Zhao et al., 2025) and InstructVLA (Yang et al., 2026) enhance reasoning and instruction following. Additionally, SpatialVLA (Qu et al., 2025) improves spatial awareness, and Diffusion-VLA (Wen et al., 2025c) utilizes generative modeling for action generation. Our framework, XR-1, introduces a novel three-stage process that synergizes human and robot data, departing from traditional two-stage paradigms. Its core is an initial self-supervised stage that learns unified vision-motion representations, which serve as auxiliary features to optimize sub- 

sequent large-scale VLA pre-training. This model-agnostic approach ensures flexibility, which we validate by building upon base models like _π_ 0 and SwitchVLA to develop the high-performing XR-1 and efficient XR-1-Light. 

## **2.2. Latent Representation Learning** 

A primary bottleneck in learning robust visuomotor policies is the gap between high-dimensional pixel observations and low-dimensional motor commands. To bridge this, prior research (Cui et al., 2023; Shafiullah et al., 2022; Lee et al., 2024; Zheng et al., 2025; Xie et al., 2025) utilizes latent representations as a critical intermediary layer. Current methodologies generally fall into two unimodal categories, with the first focusing on modeling low-level motor dynamics by discretizing continuous actions into latent tokens. This tokenization approach, pioneered by Behavior Transformers (BeT) (Shafiullah et al., 2022) and refined by QueST (Mete et al., 2024), transforms continuous control into a sequencegeneration task. Recent advancements have further optimized this direction: (Bauer et al., 2025) introduced discrete latent actions for data efficiency, while ATE (Zhang et al., 2026) improved alignment between visual inputs and discretized action spaces. Similarly, Moto (Chen et al., 2025) and Discrete Policy (Wu et al., 2025b) demonstrate that action tokenization scales effectively for generalized control. However, these action-centric methods are fundamentally limited by dependence on vast quantities of labeled robotic data, which is prohibitively expensive to acquire at scale. Alternatively, the second category exploits unlabeled video data (Cui et al., 2023; Du et al., 2023; Hu et al., 2025; He et al., 2024; Ye et al., 2025; Cheang et al., 2025b) to encode visual flow and state transitions. While models like C-BeT (Cui et al., 2023) and UniPi (Du et al., 2023) utilize ”play” data or video generation, more recent works—including VPP (Hu et al., 2025), LAPA (Ye et al., 2025), GR-2 (Cheang et al., 2025b), VPDD (He et al., 2024), and GO-1 (Bu et al., 2025a)—pre-train on actionless human and web videos to capture task semantics. However, these approaches, alongside UVA (Li et al., 2025b), often isolate vision from action during representation learning. This reliance on action-free data lacks explicit grounding, creating a critical alignment gap between understanding visual changes and executing the fine-grained motor control required to achieve them. 

Crucially, by treating vision and action in isolation, existing unimodal paradigms miss the causal link between observation and execution. We address this limitation with XR-1, which introduces Unified Vision-Motion Codes (UVMC), a discrete latent representation learned jointly from visual dynamics and robotic motion. By constructing a bimodal latent space, UVMC encodes the cause-and-effect relationship between seeing and acting, abstracting away embodimentspecific details while preserving task semantics. 

3 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 2._ Overview of **X Robotic Model 1 (XR-1)** . In XR-1, we introduce the _Unified Vision-Motion Codes (UVMC)_ , a discrete latent representation that jointly encodes visual dynamics and robotic motion. XR-1 adopts a three-stage training paradigm to enable precise low-level control across diverse robots and tasks. 

# **3. Methodology** 

## **3.1. Overview** 

Our goal is to build a versatile and generalist VisionLanguage-Action (VLA) model that controls diverse robotic embodiments across tasks. At each inference step _t_ , the policy _π_ receives a language instruction **_l_** and multimodal observations **_o_** = _⟨_ **_c_** _,_ **_m_** _⟩_ , where **_c_** _∈_ R<sup>_K×_3</sup><sup>_×H×W_</sup> denotes _K_ RGB images from external or robot-mounted cameras, and **_m_** represents proprioceptive states. The model then predicts the next action **_a_** ˆ = _π_ ( **_l_** _,_ **_o_** ) in terms of joint positions and gripper commands. 

We introduce **XR-1** , a scalable framework for cross-robot VLA learning (Figure 2), structured in three stages. First, we learn a dual-branch VQ-VAE to encode visual dynamics and robot motion into a unified discrete latent space, yielding _Unified Vision-Motion Codes (UVMC)_ . In the second stage, these codes supervise large-scale pre-training on cross-embodiment datasets for broad generalization. Finally, the policy is fine-tuned on target embodiment data to adapt to specific dynamics and improve success rates. By progressing from the unified representation to task-specific refinement, this design ensures scalability and adaptability. 

## **3.2. Stage-1: Learning Unified Vision-Motion Codes** 

We design a dual-branch VQ-VAE (Van Den Oord et al., 2017) to learn Unified Vision-Motion Codes (UVMC) via self-supervision. Unlike prior works focusing exclusively on visual dynamics (Cui et al., 2023; Hu et al., 2025; Bu 

et al., 2025a; He et al., 2024; Ye et al., 2025; Cheang et al., 2025b; Du et al., 2023) or action sequences (Shafiullah et al., 2022; Wu et al., 2025b; Bauer et al., 2025; Zhang et al., 2026; Mete et al., 2024; Chen et al., 2025), our approach explicitly unifies both modalities in a discrete latent space. By employing an alignment regularization loss, our design provides complementary guidance for action prediction and enables learning from heterogeneous sources, such as actionless human demonstrations. 

**Visual Dynamic Code Extraction** . Vision captures universal dynamics across robots and environments. To encode temporal visual variations in the vision branch, we adopt an asymmetric VQ-VAE (Zhu et al., 2023c) structure tailored for future-frame prediction. Given two frames **_c_** _t_ and **_c_** _t_ + _h_ , the vision encoder _E_ vis( _·_ ) produces a latent code **_z_** vis = _E_ vis( **_c_** _t,_ **_c_** _t_ + _h_ ), which compresses temporal changes over _h_ steps. The decoder then predicts the future frame via **_c_** ˆ _t_ + _h_ = _D_ vis( **_c_** _t,_ **_z_** vis). Thus, **_z_** vis captures the essential visual dynamics. 

**Robotic Motion Extraction** . The second branch encodes low-level actions and proprioceptive states. Specifically, the motion encoder _E_ mo( _·_ ) takes ( **_a_** _t_ : _t_ + _h,_ **_m_** _t_ : _t_ + _h_ ) as input and outputs **_z_** mo = _E_ mo( **_a_** _t_ : _t_ + _h,_ **_m_** _t_ : _t_ + _h_ ). Unlike the vision branch, no raw images or instructions are used here to ensure that the representation focuses purely on robotic dynamics. The motion decoder _D_ mo( _·_ ) then takes the latent motion embedding **_z_** _mo_ and optional conditions **_cd_** as input, such as the language instruction **_l_** , proprioceptive states **_m_** , and the observations **_o_** . The decoder reconstructs actions as 

4 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

**_a_** ˆ _t_ : _t_ + _h_ = _D_ mo( **_z_** _mo,_ **_cd_** ). In our implementation, we use the proprioceptive states **_m_** as the condition input. 

**Unified Vision-Motion Codes** . To unify both modalities, we introduce a VQ-VAE codebook **_e_** _∈_ R<sup>_d×f_</sup> with _d_ discrete entries of dimension _f_ . Encoder outputs **_z_** vis and **_z_** mo are quantized by nearest-neighbor lookup: **_z_** vis<sup>**_e_**=</sup> _S_ ( **_z_** vis) = **_e_** _j_ , where _j_ = arg min _i ∥_ **_z_** vis _−_ **_e_** _i∥_ 2, and **_z_** mo<sup>**_e_**=</sup><sup>_S_(</sup><sup>**_z_**mo)=</sup><sup>**_e_**</sup><sup>_j_,where</sup><sup>_j_=arg min</sup> _i_<sup>_∥_</sup><sup>**_z_**mo</sup><sup>_−_</sup><sup>**_e_**</sup><sup>_i∥_2.</sup> Both decoders then condition on these quantized codes for reconstruction. Training follows standard VQ-VAE objectives (Van Den Oord et al., 2017), combining reconstruction losses with codebook and commitment regularization terms: 


where _sg_ ( _·_ ) denotes stop-gradient. We set _β_ = 0 _._ 25 in all experiments. To capture both the vision and motion signals, we concatenate the robotic motion codes **_z_** mo<sup>**_e_**andvisual</sup> dynamics codes **_z_** vis<sup>**_e_**toobtaintheUnifiedVision-Motion</sup> Codes **_z_** uvmc<sup>**_e_**for subsequent policy learning.</sup> 

**Cross-Modality Alignment** . While motion codes provide precise control signals, visual embeddings may capture irrelevant factors (e.g., camera jitter). To mitigate this gap, we introduce an alignment loss that constrains visual codes to remain consistent with their motion counterparts: 


where _q_ ( _·_ ) denotes the posterior distribution in the codebook space. This grounding of perception in motor dynamics improves robustness and allows human-only demonstrations to be effectively mapped into the robot’s action space. 

**Final Training Objective** . The overall objective integrates reconstruction and alignment losses from different data sources. For robotic demonstrations, we jointly optimize _L_<sup>robot</sup> total<sup>=</sup><sup>_L_vis+</sup><sup>_L_mo+</sup><sup>_L_align,where</sup><sup>_L_visand</sup><sup>_L_moarethe</sup> VQ-VAE losses for visual and motion branches, and _L_ align enforces cross-modal consistency. For human demonstrations, where low-level actions are unavailable, the objective naturally reduces to _L_<sup>human</sup> total = _L_ vis. This design allows training on both robot rollouts and purely visual human data. Further architectural details are provided in Appendix B. 

## **3.3. Stage-2: UVMC-Guided Generalist Pretraining** 

After learning the Unified Vision-Motion Codes (UVMC) with the dual-branch VQ-VAE, we integrate it into policy learning to enhance low-level control. The policy _π_ ( _·_ ) follows a standard VLA design with a VLM _F_ ( _·_ ) and an action 

head _H_ ( _·_ ). Learnable tokens **_t_** are introduced into the VLM input, enabling _F_ ( _·_ ) to predict the UVMC. The prediction loss is defined as _L_ uvmc = _∥F_ ( **_l_** _,_ **_o_** _,_ **_t_** ) _−_ **_z_** uvmc<sup>**_e_**</sup><sup>_∥_</sup> 2<sup>2.In paral-</sup> lel, the action head is pretrained on robot datasets using an action loss _L_ act, which may be generative or autoregressive depending on the model variant. The overall objective is _L_ = _L_ uvmc + _L_ act. This joint training encourages the backbone to internalize structured vision-motion representations while ensuring effective large-scale action pretraining. 

## **3.4. Stage-3: Post-training for Deployment** 

Following large-scale UVMC-guided pre-training, the model effectively extracts unified vision-motion knowledge to produce foundation-level actions. To refine performance on downstream tasks, we introduce a post-training stage where the VLA policy is fine-tuned on task-specific datasets using an action loss _L_ act. A primary advantage of our framework is its model-agnostic design, making it directly compatible with various VLA architectures. This flexibility allows for the integration of diverse backbones while consistently leveraging the benefits of our pre-trained representations. 

## **3.5. Data Collection and Implementation Details** 

**Dataset Collection** . To support large-scale pretraining, we curate a comprehensive dataset by integrating four complementary sources: Open-X (O’Neill et al., 2024), RoboMIND (Wu et al., 2025a), Ego4D (first-person human activity videos) (Grauman et al., 2022), and XR-D (a subset of RoboMIND 2.0 (Hou et al., 2025) primarily comprising in-house collected data across multiple robot embodiments). 

Table 1 summarizes the distribution of episodes and frames across these datasets, together with their relative proportions. Since the number of episodes and frames varies significantly among different sources, we assign dataset-specific sampling weights during training to balance contributions and prevent overfitting to dominant datasets. We provide more details of the datasets in Appendix C. 

## **Implementation De-** 

|**tails**.|The framework|_Table_|_1._ Dataset|Statist|ics.|
|---|---|---|---|---|---|
|is|model-agnostic.|||||
|Our|main<br>instanti-|Dataset|Episodes|Frames<br>|Weight|
|ation|follows<br>the|OXE<br>RoboMIND|978k<br>69k|59.3M<br>21.4M|40%<br>15%|
|desig|n of _π_0 (Black|XR-D|158k|69.1M|35%|
|et al|<br>., 2025),<br>built|Ego4D|59k|14.3M|10%|


on PaliGemma (Beyer et al., 2024) with a SigLIP visual encoder (Zhai et al., 2023), Gemma backbone (Team et al., 2024a), and action head. We also provide a lightweight variant, XR-1-Light, built upon SwitchVLA (Li et al., 2025a), which uses Florence-2 (Xiao et al., 2024) to reduce computational cost with minimal performance degradation. Further details on training settings and model configurations are provided in Appendix B. 

5 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 3._ Experimental Setup. We evaluate XR-1 across six robot embodiments (Tien Kung 1.0/2.0, Single-/Dual-Arm UR-5e, Dual-Arm Franka, and AgileX Cobot Magic 2.0), covering more than 120 manipulation tasks with over 14k rollouts. 


_Figure 4._ Success rate results across 20 tasks on Dual-Arm UR-5e. 

# **4. Experiments** 

We evaluate XR-1 across six robotic embodiments and over 120 tasks, including bimanual collaboration, dexterous manipulation, and long-horizon tasks, to address four key questions: ( _i_ ) performance compared to SOTA VLA models; ( _ii_ ) the impact of large-scale pre-training on rapid adaptation; ( _iii_ ) generalization to novel objects and environmental shifts; and ( _iv_ ) the efficacy of specific components and training strategies. By benchmarking against multiple strong baselines, we demonstrate the robustness and scalability of our approach in diverse, challenging scenarios. 

## **4.1. Experiment Setup** 

**Real-World Robotic Setup.** We evaluate XR-1 on six heterogeneous embodiments (Figure 3): Tien Kung 1.0/2.0, single/dual-arm UR-5e, dual-arm Franka, and AgileX Cobot Magic 2.0. Each platform is equipped with parallel grippers 

and calibrated multi-view cameras. For each embodiment, 20 tasks were designed and expert demonstrations were collected via teleoperation, recording synchronized RGB and proprioceptive streams (e.g., joint positions and gripper commands). Representative tasks for the Dual-Arm UR-5e and Tien Kung 2.0 are shown in Figure 3, with full task details provided in Appendix K. 

**Training and Evaluation Protocol.** We employ a threestage pipeline: ( _i_ ) UVMC Pre-training: learning representations from large-scale heterogeneous datasets, including RoboMIND (Wu et al., 2025a), Open-X (O’Neill et al., 2024), XR-D, and Ego4D (Grauman et al., 2022); ( _ii_ ) Policy Pre-training: integrating cross-embodiment knowledge on XR-D; and ( _iii_ ) Task Fine-tuning: refining performance on target tasks. This staged training progressively transfers vision-motion abstractions to downstream robotic policies. For evaluation, we conduct 20 rollouts per task and report success rates based on human evaluation. 

6 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

_Table 2._ Success rate results across 20 tasks on Tien Kung 2.0. 

|Method|TK2-Press<br>Button|TK2-Assemble<br>Valve|TK2-Stack<br>Brake|TK2-Place<br>Circuit|TK2-Press<br>ControlBox|TK2-Close<br>DoorKnob|TK2-Gather<br>Tools|TK2-Close<br>Laptop|TK2-Open<br>PotLid|TK2-Hang<br>CupHolder|-|
|---|---|---|---|---|---|---|---|---|---|---|---|
|UniVLA|25|0|25|50|10|0|0|20|35|0|-|
|RDT|15|0|0|65|20|0|0|0|90|0|-|
|GR00T-N1.5|85|20|85|90|0|0|20|0|75|0|-|
|_π_0|85|10|55|70|85|0|20|85|85|20|-|
|_π_0_._5|80|0|65|60|40|25|20|90|80|35|-|
|XR-1 (ours)|90|15|90|90|90|85|25|90|85|75|-|
||TK2-Move<br>CupSauce|TK2-Stack<br>Cup|TK2-Insert<br>ToyBlock|TK2-Find<br>Capacitor|TK2-Move<br>MilkMug|TK2-Pour<br>GearOil|TK2-Place<br>BiscuitBox|TK2-Collect<br>Screws|TK2-Move<br>Tape|TK2-Take<br>BasketTea|Avg.|
|UniVLA|45|30|0|25|35|35|0|0|20|0|17.8|
|RDT|50|25|0|0|0|75|0|0|0|0|17.0|
|GR00T-N1.5|50|55|0|60|55|70|25|0|70|0|38.0|
|_π_0|60|20|10|0|80|55|0|0|0|75|40.8|
|_π_0_._5|70|25|20|0|75|75|0|0|0|60|41.0|
|XR-1 (ours)|70|85|55|75|90|85|75|15|70|85|72.0|


_Table 3._ Ablation study of XR-1. In Stage-1 and Stage-2, “DT” indicates training directly on the downstream task data. 

|Exp.|Instantiation|Stage-1|Stage-2|Stage-3|DUR-Clean<br>Table|DUR-Find<br>TapeBasket|DUR-Move<br>CupMilk|DUR-Stack<br>Bowls|DUR-Sweep<br>Trash|DUR-Trans<br>CupHolder|Avg|
|---|---|---|---|---|---|---|---|---|---|---|---|
|1|XR-1-Light|_×_|_×_|✓|0|70|0|75|60|50|42.5|
|2|XR-1-Light|DT|DT|✓|40|90|10|90|60|55|57.5|
|3|XR-1|_×_|_×_|✓|0|50|20|55|0|45|28.3|
|4|XR-1 w/o KL|DT|DT|✓|45|55|35|60|30|65|48.3|
|5|XR-1 motion-only|DT|DT|✓|25|70|35|60|5|15|35.0|
|6|XR-1 vision-only|DT|DT|✓|10|70|65|70|15|65|50.0|
|7|XR-1|DT|DT|✓|50|75|65|80|60|70|66.7|
|8|XR-1|1%|DT|✓|15|60|10|55|15|20|29.2|
|9|XR-1|10%|DT|✓|25|60|25|60|20|40|38.3|
|10|XR-1|50%|DT|✓|25|80|65|80|20|50|53.3|
|11|XR-1|100%|DT|✓|60|80|70|85|40|55|65.0|
|12|XR-1|100%|XR-D|✓|70|85|80|90|85|80|81.6|
|13|XR-1 w/o Ego4D|10%|DT|✓|20|60|10|55|15|35|32.5|
|14|XR-1 w/ Ego4D|10%|DT|✓|25|60|25|60|20|40|38.3|


## **4.2. Results on Real-World Robotic Tasks** 

**Baseline Methods** . We compare XR-1 with strong VLA models, including _π_ 0 _._ 5 (Intelligence et al., 2025), _π_ 0 (Black et al., 2025), RDT (Liu et al., 2025), UniVLA (Bu et al., 2025b), and GR00T-N1.5 (Bjorck et al., 2025). We note a performance degradation with the Lerobot implementation of _π_ 0. The results of _π_ 0 reported in this paper are based on the original JAX implementation. 

**Results on Dual-Arm UR-5e** . Figure 4 shows success rates on 20 Dual-Arm UR-5e tasks. XR-1 outperforms all baselines by a wide margin (e.g., _DUR-FindTapeBasket_ : 85% vs. 50% for _π_ 0), while several baselines drop to 0% on harder tasks. We attribute this to limited auxiliary supervision and optimization conflicts in multi-task training. XR-1 mitigates these issues with UVMC, producing stronger representations and more stable optimization. Tabular results are in Appendix Table 13. 

**Results on Tien Kung 2.0 (Unseen during Pretraining)** . We further evaluate transferability on Tien Kung 2.0 over another 20 tasks in Table 2. Unlike the UR-5e, this robot is _unseen during pretraining_ (e.g., Stages 1 and 2 for XR1), making the evaluation a stringent embodiment-transfer 

benchmark. Despite this challenge, XR-1 again outperforms all baselines; e.g., in _TK2-MoveCupSauce_ , it reaches 70% versus 60% for _π_ 0. These results indicate that UVMC effectively encodes embodiment-agnostic dynamics into a shared latent space, enabling efficient transfer of prior knowledge to novel robotic platforms. 

**Results on Other Robots** . XR-1 consistently outperforms all other methods across four diverse robotic arm configurations, achieving a significant relative gain over the strongest baseline. Additional experimental results for Tien Kung 1.0 in Table 9, Dual-Arm Franka in Table 10, AgileX Cobot Magic V2.0 in Table 11, and Single-Arm UR-5e in Table 12 are provided in Appendix D. 

## **4.3. Ablation Study** 

To disentangle the contribution of each component in XR1, we conduct ablations on six manipulation tasks using the Dual-Arm UR-5e. Table 3 summarizes success rates under different configurations, covering model capacity, UVMC learning, cross-modal alignment, and dataset scaling. Additional experimental results and analysis for the UVMC ablation study, as well as for Ego4D and crossembodied knowledge transfer ablations on enhanced single- 

7 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

_Table 4._ Generalization results of XR-1 on unseen scenarios. 


_Figure 5._ Unseen scenario task setup on Dual-Arm Franka. 

embodiment performance, are provided in Appendix E. 

**Lightweight Models.** To validate the applicability of our methods in resource-constrained environments, we extend our evaluation to a compact variant, XR-1-Light, which comprises only 230M trainable parameters. When this model is trained without our proposed UVMC-based fine-tuning stage (Exp. 1), it achieves a respectable baseline performance of 42.5%. However, the integration of the UVMC module during its training phase (Exp. 2) elevates the average success rate to 57.5%. _This significant +15% absolute improvement confirms that our training methodology is not merely an artifact of large model capacity but provides substantial and consistent benefits even for highly efficient, lightweight architectures, thereby highlighting its broad applicability and practical value._ 

**UVMC and Cross-Modal Alignment.** Exps. 3–5 examine the role of UVMC together with a cross-modal alignment loss between vision and motion. Performance consistently improves as these components are added, confirming their complementary importance for feature learning across tasks. 

**Scaling with Pretraining Data.** Having established the profound impact of our core training objectives, we now turn our attention to the role of large-scale pretraining. We first analyze the scaling behavior with respect to the volume of Stage-1 pretraining data, using the full XR-1 model without any subsequent fine-tuning. The results from Exps. 6–9 reveal a clear and compelling monotonic scaling law: as the pretraining dataset size systematically increases from 1% to 10%, 50%, and finally 100%, the average success rate consistently climbs from 29.2% to 38.3%, 53.3%, and ultimately 65.0%. _This trend unequivocally demonstrates the foundational importance of leveraging large and diverse datasets to learn generalizable robotic policies._ Intriguingly, the performance achieved with 100% of the Stage-1 pretraining data (65.0%) is already on par with the model that was exclusively fine-tuned on downstream tasks (Exp. 5, 66.7%), indicating that task-agnostic pretraining can effectively instill a powerful inductive bias. 

## **4.4. Generalization Analysis** 

**Generalization to Unseen Scenarios** . We further evaluate XR-1 on unseen conditions to assess its out-of-distribution generalization. As shown in Figure 5, we test on ( _i_ ) novel objects (e.g., unseen rubbish or dustpans), ( _ii_ ) dynamic and static distractors, ( _iii_ ) illumination changes, and ( _iv_ ) background variations. As shown in Table 4, XR-1 consistently outperforms the strong VLA method _π_ 0 across all settings. It demonstrates clear gains on novel objects, improved robustness under distractor interference, and stable performance when background and lighting variations are introduced. _These results highlight XR-1’s strong generalization not only across embodiments and tasks but also under diverse environmental shifts never encountered during pretraining or fine-tuning, underscoring its potential for real-world deployment._ 

**Out-of-Box Evaluation.** We assess the foundational capabilities of XR-1 after Stage-2, bypassing Stage-3 posttraining. We evaluate on 7 tasks from the Dual-Arm Franka setup, which comprises only 0 _._ 45% of the XR-D dataset. For a fair comparison, baselines without XR-D pre-training are fine-tuned on these specific tasks. As shown in Figure 6, the pre-trained XR-1-oob model, despite no adaptation, achieves performance comparable to GR00T-N1.5 and _π_ 0, while outperforming RDT and UniVLA. _This robustness highlights the efficacy of UVMC in aligning multimodal dynamics across embodiments, enabling strong generalization with minimal task-specific supervision._ Additional results for the Dual-Arm UR-5e are in Appendix F. 

**Fast Adaptation to New Tasks** . We further evaluate whether XR-1 can rapidly adapt to unseen tasks with limited demonstrations. Specifically, we collect 15 new tasks on Tien Kung 2.0 (unseen in XR-D), each with 20 trajectories. XR-1 is trained jointly across these tasks, while single-task baselines, ACT (Zhao et al., 2023) and Diffusion Policy (DP) (Chi et al., 2023), are trained independently per task. As shown in Figure 7, XR-1 achieves significantly higher success rates than ACT and DP, despite the setting favoring 

8 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 6._ Out-of-box evaluation results of 7 tasks on Dual-Arm Franka. 

the baselines. _This advantage stems from large-scale pretraining and UVMC supervision, enabling XR-1 to extract transferable features from few-shot data and adapt across diverse embodiments._ Additional results and analysis on the Dual-Arm UR-5e are provided in Appendix F. 

## **4.5. Additional Analyses** 

Additional simulation results are provided in Appendix G. To assess semantic alignment between visual codes (VC) and motion codes (MC), we perform cross-modal nearestneighbor retrieval and t-SNE visualization. These analyses validate UVMC’s ability to capture embodiment-agnostic action semantics: nearest-neighbor retrieval shows that MCs retrieve visually consistent action phases across tasks and embodiments, while t-SNE reveals coherent clustering by task dynamics rather than robot morphology. Failure analyses for baselines and XR-1 are provided in Appendix I and Appendix J, respectively, showing that XR-1 reduces baseline failures such as optimization collapse, conflicting gradients, and coordination errors, though high-precision manipulation remains challenging. We further categorize the 120 real-world tasks into seven types in Appendix K. The full benchmark specification, including task images, language instructions, and collected demonstration counts for all 120 tasks, is provided in Appendix K.1. 

# **5. Conclusion** 

We presented **X Robotic Model 1 (XR-1)** , a unified framework for versatile and scalable vision-language-action learning that addresses the key limitations of existing approaches: precise low-level action generation and crossdomain multimodal knowledge exploitation across heterogeneous data sources. Central to our approach is the _Unified Vision-Motion Codes (UVMC)_ , which serve as embodiment- 

agnostic abstractions aligning visual dynamics with motor control through a shared discrete latent space. By utilizing a three-stage training paradigm, XR-1 achieves robust performance across diverse robots, environments, and tasks while significantly outperforming state-of-the-art baselines such as _π_ 0 _._ 5, _π_ 0, RDT, UniVLA, and GR00T-N1.5. Our results highlight the importance of multimodal alignment for embodied AI and suggest promising directions toward general-purpose robotic agents capable of interacting with the physical world and adapting seamlessly to new environments and task demands. 

# **Acknowledgments** 

This work was supported by the New Generation Artificial Intelligence-National Science and Technology Major Project (2025ZD0122603). 

Developing large-scale Vision-Language-Action (VLA) models is a monumental task that required extensive collaboration among numerous researchers across multiple domains. The development of this work would not have been possible without the dedication and expertise of many individuals who contributed their time and knowledge throughout various stages of the project. 

We would like to extend our deepest gratitude to the following individuals for their invaluable help in this work: Guang Yang, Haonan Liu, Heng Zhou, Huijuan Ma, Jianwei Guo, Jianwei Sun, Jianyu Dong, Junjie Ji, Mingxuan Guo, Panpan Chen, Pei Ren, Pengwei Zhang, Qiang Zhang, Qichun Liu, Shuguang Qiao, Shiwei Jiao, Yaowen Xu, Yang Pan, Yi Zhang, Yulin Luo, and Zhifei Xiang. We also sincerely appreciate the dedication and effort of numerous contributors who assisted with data collection, quality assurance, and testing procedures. Their collective efforts and expertise have been instrumental in making this research possible. 

9 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 7._ Fast adaptation on Tien Kung 2.0. Tien Kung 2.0 is an unseen embodiment in XR-D. In this setup, XR-1 adapts to 15 novel tasks with one model using only 20-shot demonstrations per task, while baselines (ACT and DP) are trained per task. 

We sincerely appreciate their commitment to advancing the field of robotic manipulation through this collaborative endeavor. 

# **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

# **References** 

- Bahl, S., Mendonca, R., Chen, L., Jain, U., and Pathak, D. Affordances from human videos as a versatile representation for robotics. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 13778–13790, 2023. 

- Bai, J., Bai, S., Chu, Y., Cui, Z., Dang, K., Deng, X., Fan, Y., Ge, W., Han, Y., Huang, F., et al. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 

- Bauer, E., Nava, E., and Katzschmann, R. K. Latent action diffusion for cross-embodiment manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- Belkhale, S., Cui, Y., and Sadigh, D. Hydra: Hybrid robot actions for imitation learning. In _Conference on Robot Learning_ , pp. 2113–2133. PMLR, 2023. 

- Beyer, L., Steiner, A., Pinto, A. S., Kolesnikov, A., Wang, X., Salz, D., Neumann, M., Alabdulmohsin, I., Tschannen, M., Bugliarello, E., et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Bharadhwaj, H., Vakil, J., Sharma, M., Gupta, A., Tulsiani, S., and Kumar, V. Roboagent: Generalization and effi- 

ciency in robot manipulation via semantic augmentations and action chunking. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 4788–4795. IEEE, 2024. 

- Bjorck, J., Castaneda, F., Cherniadev, N., Da, X., Ding, R.,˜ Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A vision-language-action flow model for general robot control. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., Gao, S., He, X., Hu, X., Huang, X., et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025a. 

- Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. Univla: Learning to act anywhere with task-centric latent actions. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025b. 

- Cao, J., Zhang, Q., Sun, J., Wang, J., Cheng, H., Li, Y., Ma, J., Wu, K., Xu, Z., Shao, Y., et al. Mamba policy: Towards efficient 3d diffusion policy with hybrid selective state models. In _Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025. 

10 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

- Cheang, C., Chen, S., Cui, Z., Hu, Y., Huang, L., Kong, T., Li, H., Li, Y., Liu, Y., Ma, X., et al. Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ , 2025a. 

- Cheang, C.-L., Chen, G., Jing, Y., Kong, T., Li, H., Li, Y., Liu, Y., Wu, H., Xu, J., Yang, Y., et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2025b. 

- Chen, L., Bahl, S., and Pathak, D. Playfusion: Skill acquisition via diffusion from language-annotated play. In _Conference on Robot Learning_ , pp. 2012–2029. PMLR, 2023. 

- Chen, L. Y., Adebola, S., and Goldberg, K. Berkeley UR5 demonstration dataset. https://sites.google.com/view/berkeley-ur5/home. 

- Chen, Y., Ge, Y., Li, Y., Ge, Y., Ding, M., Shan, Y., and Liu, X. Moto: Latent motion token as the bridging language for robot manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ . IEEE, 2025. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , pp. 02783649241273668, 2023. 

- Cui, Z. J., Wang, Y., Shafiullah, N. M. M., and Pinto, L. From play to policy: Conditional behavior generation from uncurated robot data. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2023. 

- Dass, S., Yapeter, J., Zhang, J., Zhang, J., Pertsch, K., Nikolaidis, S., and Lim, J. J. Clvr jaco play dataset, 2023. URL https://github.com/ clvrai/clvr_jaco_play_dataset. 

- Driess, D., Xia, F., Sajjadi, M. S. M., Lynch, C., Chowdhery, A., Ichter, B., Wahid, A., Tompson, J., Vuong, Q., Yu, T., Huang, W., Chebotar, Y., Sermanet, P., Duckworth, D., Levine, S., Vanhoucke, V., Hausman, K., Toussaint, M., Greff, K., Zeng, A., Mordatch, I., and Florence, P. PaLM-e: An embodied multimodal language model. In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pp. 8469–8488. PMLR, 23–29 Jul 2023. URL https://proceedings.mlr.press/ v202/driess23a.html. 

- Du, Y., Yang, S., Dai, B., Dai, H., Nachum, O., Tenenbaum, J., Schuurmans, D., and Abbeel, P. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

- Ebert, F., Yang, Y., Schmeckpeper, K., Bucher, B., Georgakis, G., Daniilidis, K., Finn, C., and Levine, S. Bridge data: Boosting generalization of robotic skills with crossdomain datasets. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2022. 

- Fan, S., Yang, Q., Liu, Y., Wu, K., Che, Z., Liu, Q., and Wan, M. Diffusion trajectory-guided policy for long-horizon robot manipulation. _IEEE Robotics and Automation Letters_ , 10(12):12788–12795, 2025. doi: 10.1109/LRA.2025.3619794. 

- Feng, Y., Hansen, N., Xiong, Z., Rajagopalan, C., and Wang, X. Finetuning offline world models in the real world. In _Conference on Robot Learning (CoRL)_ , 2023. 

- Fu, Z., Zhao, T. Z., and Finn, C. Mobile aloha: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. In _Conference on Robot Learning (CoRL)_ , 2024. 

- Gao, P., Han, J., Zhang, R., Lin, Z., Geng, S., Zhou, A., Zhang, W., Lu, P., He, C., Yue, X., et al. Llama-adapter v2: Parameter-efficient visual instruction model. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2024. 

- Grauman, K., Westbury, A., Byrne, E., Chavis, Z., Furnari, A., Girdhar, R., Hamburger, J., Jiang, H., Liu, M., Liu, X., et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 18995–19012, 2022. 

- Haldar, S., Mathur, V., Yarats, D., and Pinto, L. Watch and match: Supercharging imitation with regularized optimal transport. In _Conference on Robot Learning_ , pp. 32–43. PMLR, 2023. 

- He, H., Bai, C., Pan, L., Zhang, W., Zhao, B., and Li, X. Learning an actionable discrete diffusion policy via largescale actionless video pre-training. _Advances in Neural Information Processing Systems_ , 37:31124–31153, 2024. 

- He, K., Chen, X., Xie, S., Li, Y., Dollar, P., and Girshick,´ R. Masked autoencoders are scalable vision learners. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 16000–16009, 2022. 

- Heo, M., Lee, Y., Lee, D., and Lim, J. J. Furniturebench: Reproducible real-world benchmark for long-horizon complex manipulation. _The International Journal of Robotics Research_ , pp. 02783649241304789, 2023. 

11 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

- Hirose, N., Shah, D., Sridhar, A., and Levine, S. Sacson: Scalable autonomous control for social navigation. _IEEE Robotics and Automation Letters_ , 9(1):49–56, 2023. 

- Hou, C., Wu, K., Liu, J., Che, Z., Wu, D., Liao, F., Li, G., He, J., Feng, Q., Jin, Z., et al. Robomind 2.0: A multimodal, bimanual mobile manipulation dataset for generalizable embodied intelligence. _arXiv preprint arXiv:2512.24653_ , 2025. 

- Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.-J., Zhang, J., Sreenath, K., Lu, C., and Chen, J. Video prediction policy: A generalist robot policy with predictive visual representations. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2025. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In _Proceedings of the Conference on Robot Learning (CoRL)_ , volume 305, pp. 17–40. PMLR, 2025. 

- Jang, E., Irpan, A., Khansari, M., Kappler, D., Ebert, F., Lynch, C., Levine, S., and Finn, C. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pp. 991–1002. PMLR, 2022. 

- Kahn, G., Villaflor, A., Ding, B., Abbeel, P., and Levine, S. Self-supervised deep reinforcement learning with generalized computation graphs for robot navigation. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pp. 5129–5136. IEEE, 2018. 

- Kalashnikov, D., Irpan, A., Pastor, P., Ibarz, J., Herzog, A., Jang, E., Quillen, D., Holly, E., Kalakrishnan, M., Vanhoucke, V., et al. Scalable deep reinforcement learning for vision-based robotic manipulation. In _Conference on robot learning_ , pp. 651–673. PMLR, 2018. 

- Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., Nasiriany, S., Srirama, M. K., Chen, L. Y., Ellis, K., et al. Droid: A large-scale in-the-wild robot manipulation dataset. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- Kim, M., Han, J., Kim, J., and Kim, B. Pre-and post-contact policy decomposition for non-prehensile manipulation with zero-shot sim-to-real transfer. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 10644–10651. IEEE, 2023. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. In _Conference on Robot Learning (CoRL)_ , 2024. 

- Lee, J., Duan, J., Fang, H., Deng, Y., Liu, S., Li, B., Fang, B., Zhang, J., Wang, Y. R., Lee, S., et al. Molmoact: Action reasoning models that can reason in space. In _CoRL 2025 Robot Data Workshop_ , 2025. 

- Lee, S., Wang, Y., Etukuru, H., Kim, H. J., Shafiullah, N. M. M., and Pinto, L. Behavior generation with latent actions. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2024. 

- Li, J., Li, D., Savarese, S., and Hoi, S. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _International conference on machine learning_ , pp. 19730–19742. PMLR, 2023. 

- Li, M., Zhao, Z., Che, Z., Liao, F., Wu, K., Xu, Z., Ren, P., Jin, Z., Liu, N., and Tang, J. Switchvla: Executionaware task switching for vision-language-action models. In _Workshop at the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025a. 

- Li, S., Gao, Y., Sadigh, D., and Song, S. Unified video action model. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025b. 

- Liu, H., Nasiriany, S., Zhang, L., Bao, Z., and Zhu, Y. Robot learning on the job: Human-in-the-loop autonomy and learning during deployment. _The International Journal of Robotics Research_ , pp. 02783649241273901, 2022. 

- Liu, H., Li, C., Wu, Q., and Lee, Y. J. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 

- Liu, J., Chen, H., An, P., Liu, Z., Zhang, R., Gu, C., Li, X., Guo, Z., Chen, S., Liu, M., et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-languageaction model. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2026a. 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., and Zhu, J. Rdt-1b: a diffusion foundation model for bimanual manipulation. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2025. 

- Liu, Z., Liu, J., Xu, J., Han, N., Gu, C., Chen, H., Zhou, K., Zhang, R., Hsieh, K. C., Wu, K., et al. Mla: A multisensory language-action model for multimodal understanding and forecasting in robotic manipulation. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2026b. 

- Luo, J., Xu, C., Geng, X., Feng, G., Fang, K., Tan, L., Schaal, S., and Levine, S. Multistage cable routing through hierarchical imitation learning. _IEEE Transactions on Robotics_ , 40:1476–1491, 2024. 

12 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

- Luo, J., Xu, C., Liu, F., Tan, L., Lin, Z., Wu, J., Abbeel, P., and Levine, S. Fmb: a functional manipulation benchmark for generalizable robotic learning. _The International Journal of Robotics Research_ , 44(4):592–606, 2025. 

- Lynch, C., Wahid, A., Tompson, J., Ding, T., Betker, J., Baruch, R., Armstrong, T., and Florence, P. Interactive language: Talking to robots in real time. _IEEE Robotics and Automation Letters_ , 2023. 

- Mandlekar, A., Booher, J., Spero, M., Tung, A., Gupta, A., Zhu, Y., Garg, A., Savarese, S., and Fei-Fei, L. Scaling robot supervision to hundreds of hours with roboturk: Robotic manipulation dataset through human reasoning and dexterity. In _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 1048– 1055. IEEE, 2019. 

- Mees, O., Hermann, L., Rosete-Beas, E., and Burgard, W. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- Mees, O., Borja-Diaz, J., and Burgard, W. Grounding language with visual affordances over unstructured data. In _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- Mendonca, R., Bahl, S., and Pathak, D. Structured world models from human videos. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- Mete, A., Xue, H., Wilcox, A., Chen, Y., and Garg, A. Quest: Self-supervised skill abstractions for learning continuous control. _Advances in Neural Information Processing Systems_ , 37:4062–4089, 2024. 

- Nasiriany, S., Gao, T., Mandlekar, A., and Zhu, Y. Learning and retrieval from prior data for skill-based imitation learning. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2022. 

- Oh, J., Kanazawa, N., and Kawaharazuka, K. X- embodiment u-tokyo pr2 datasets. _URL https://github. com/ojh6404/rlds_ _~~d~~ ataset_ _~~b~~ uilder_ , 22, 2023. 

- Osa, T. Motion planning by learning the solution manifold in trajectory optimization. _The International Journal of Robotics Research_ , 41(3):281–311, 2022. 

- O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903. IEEE, 2024. 

- Padalkar, A., Quere, G., Raffin, A., Silverio, J., and Stulp, F.´ A guided reinforcement learning approach using shared control templates for learning manipulation skills in the real world. 2023a. 

- Padalkar, A., Quere, G., Steinmetz, F., Raffin, A., Nieuwenhuisen, M., Silverio, J., and Stulp, F.´ Guiding reinforcement learning with shared control templates. In _ICRA_ , pp. 11531–11537, 2023b. 

- Pari, J., Shafiullah, N. M., Arunachalam, S. P., and Pinto, L. The surprising effectiveness of representation learning for visual imitation. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2022. 

- Park, D., Hwang, S.-H., Lee, K., Ryoo, Y., Kim, H. F., and Lee, S.-H. Supramodal and cross-modal representations of working memory in higher-order cortex. _Nature Communications_ , 16(1):4497, 2025. 

- Pfeifer, R. and Iida, F. Embodied artificial intelligence: Trends and challenges. _Lecture notes in computer science_ , pp. 1–26, 2004. 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- Quere, G., Hagengruber, A., Iskandar, M., Bustamante, S., Leidner, D., Stulp, F., and Vogel, J. Shared control templates for assistive robotics. In _2020 IEEE international conference on robotics and automation (ICRA)_ , pp. 1956– 1962. IEEE, 2020. 

- Radosavovic, I., Shi, B., Fu, L., Goldberg, K., Darrell, T., and Malik, J. Robot learning with sensorimotor pretraining. In _Conference on Robot Learning_ , pp. 683–693. PMLR, 2023a. 

- Radosavovic, I., Xiao, T., James, S., Abbeel, P., Malik, J., and Darrell, T. Real-world robot learning with masked visual pre-training. In _Conference on Robot Learning_ , pp. 416–426. PMLR, 2023b. 

- Rosete-Beas, E., Mees, O., Kalweit, G., Boedecker, J., and Burgard, W. Latent plans for task-agnostic offline reinforcement learning. In _Conference on Robot Learning_ , pp. 1838–1849. PMLR, 2023. 

- Saxena, S., Sharma, M., and Kroemer, O. Multi-resolution sensing for real-time control with vision-language models. In _2nd Workshop on Language and Robot Learning: Language as Grounding_ , 2023. 

- Shafiullah, N. M., Cui, Z., Altanzaya, A. A., and Pinto, L. Behavior transformers: Cloning _k_ modes with one stone. 

13 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

_Advances in neural information processing systems_ , 35: 22955–22968, 2022. 

- Shafiullah, N. M. M., Rai, A., Etukuru, H., Liu, Y., Misra, I., Chintala, S., and Pinto, L. On bringing robots home. _arXiv preprint arXiv:2311.16098_ , 2023. 

- Shah, D., Eysenbach, B., Kahn, G., Rhinehart, N., and Levine, S. Rapid exploration for open-world navigation with latent goal models. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2021. 

- Shah, R., Mart´ın-Mart´ın, R., and Zhu, Y. Mutex: Learning unified policies from multimodal task specifications. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2023. 

- Su, Y., Zhan, X., Fang, H., Xue, H., Fang, H.-S., Li, Y.L., Lu, C., and Yang, L. Dense policy: Bidirectional autoregressive learning of actions. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2025. 

- Team, G., Mesnard, T., Hardin, C., Dadashi, R., Bhupatiraju, S., Pathak, S., Sifre, L., Riviere, M., Kale, M. S., Love,` J., et al. Gemma: Open models based on gemini research and technology. _arXiv preprint arXiv:2403.08295_ , 2024a. 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , 2024b. 

- Van Den Oord, A., Dieleman, S., Zen, H., Simonyan, K., Vinyals, O., Graves, A., Kalchbrenner, N., Senior, A., Kavukcuoglu, K., et al. Wavenet: A generative model for raw audio. _arXiv preprint arXiv:1609.03499_ , 12:1, 2016. 

- Van Den Oord, A., Vinyals, O., et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

- Vogel, J., Hagengruber, A., Iskandar, M., Quere, G., Leipscher, U., Bustamante, S., Dietrich, A., Hoppner, H., Lei-¨ dner, D., and Albu-Schaffer, A.¨ Edan: An emg-controlled daily assistant to help people with physical disabilities. In _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 4183–4190. IEEE, 2020. 

- Walke, H. R., Black, K., Zhao, T. Z., Vuong, Q., Zheng, C., Hansen-Estruch, P., He, A. W., Myers, V., Kim, M. J., Du, M., et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pp. 1723–1736. PMLR, 2023. 

- Wang, L., Chen, X., Zhao, J., and He, K. Scaling proprioceptive-visual learning with heterogeneous pretrained transformers. _Advances in neural information processing systems_ , 37:124420–124450, 2024a. 

- Wang, P., Bai, S., Tan, S., Wang, S., Fan, Z., Bai, J., Chen, K., Liu, X., Wang, J., Ge, W., et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024b. 

- Wen, J., Zhu, Y., Li, J., Tang, Z., Shen, C., and Feng, F. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025a. 

- Wen, J., Zhu, Y., Li, J., Zhu, M., Tang, Z., Wu, K., Xu, Z., Liu, N., Cheng, R., Shen, C., et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025b. 

- Wen, J., Zhu, Y., Zhu, M., Tang, Z., Li, J., Zhou, Z., Liu, X., Shen, C., Peng, Y., and Feng, F. Diffusionvla: Scaling robot foundation models via unified diffusion and autoregression. In _Forty-second International Conference on Machine Learning_ , 2025c. 

- Wu, K., Hou, C., Liu, J., Che, Z., Ju, X., Yang, Z., Li, M., Zhao, Y., Xu, Z., Yang, G., et al. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025a. 

- Wu, K., Zhu, Y., Li, J., Wen, J., Liu, N., Xu, Z., and Tang, J. Discrete policy: Learning disentangled action space for multi-task robotic manipulation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 8811–8818. IEEE, 2025b. 

- Xiao, B., Wu, H., Xu, W., Dai, X., Hu, H., Lu, Y., Zeng, M., Liu, C., and Yuan, L. Florence-2: Advancing a unified representation for a variety of vision tasks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 4818–4829, 2024. 

- Xie, A., Rybkin, O., Sadigh, D., and Finn, C. Latent diffusion planning for imitation learning. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2025. 

- Yan, W. and Wang, X. ucsd kitchens Dataset. August 2023. 

- Yang, S., Li, H., Chen, Y., Wang, B., Tian, Y., Wang, T., Wang, H., Zhao, F., Liao, Y., and Pang, J. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2026. 

- Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., et al. Latent action pretraining from videos. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2025. 

14 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

- Yuan, Y., Cui, H., Chen, Y., Dong, Z., Ni, F., Kou, L., Liu, J., Li, P., Zheng, Y., and Hao, J. From seeing to doing: Bridging reasoning and decision for robotic manipulation. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2026. 

- Ze, Y., Zhang, G., Zhang, K., Hu, C., Wang, M., and Xu, H. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- Zhai, X., Mustafa, B., Kolesnikov, A., and Beyer, L. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 11975–11986, 2023. 

- Zhang, R., Jiang, D., Zhang, Y., Lin, H., Guo, Z., Qiu, P., Zhou, A., Lu, P., Chang, K.-W., Qiao, Y., et al. Mathverse: Does your multi-modal llm truly see the diagrams in visual math problems? In _European Conference on Computer Vision_ , pp. 169–186. Springer, 2024. 

- Zhang, Y. and Yan, J. Crossformer: Transformer utilizing cross-dimension dependency for multivariate time series forecasting. In _The eleventh international conference on learning representations_ , 2023. 

- Zhang, Y., Wang, C., Lu, O., Zhao, Y., Ge, Y., Sun, Z., Li, X., Zhang, C., Bai, C., and Li, X. Align-then-steer: Adapting the vision-language action models through unified latent guidance. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2026. 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 1702–1713, 2025. 

- Zhao, T. Z., Kumar, V., Levine, S., and Finn, C. Learning fine-grained bimanual manipulation with low-cost hardware. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

   - Zhou, G., Dean, V., Srirama, M. K., Rajeswaran, A., Pari, J., Hatch, K., Jain, A., Yu, T., Abbeel, P., Pinto, L., et al. Train offline, test online: A real robot learning benchmark. In _Proceedings of the Conference on Robot Learning workshop_ , 2022a. 

   - Zhou, Y., Sonawani, S., Phielipp, M., Stepputtis, S., and Amor, H. B. Modularity through attention: Efficient training and transfer of language-conditioned policies for robot manipulation. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2022b. 

   - Zhou, Y., Sonawani, S., Phielipp, M., Ben Amor, H., and Stepputtis, S. Learning modular language-conditioned robot policies through attention. _Autonomous Robots_ , 47 (8):1013–1033, 2023. 

   - Zhu, X., Tian, R., Xu, C., Huo, M., Zhan, W., Tomizuka, M., and Ding, M. Fanuc manipulation: A dataset for learning-based manipulation with fanuc mate 200id robot. https://sites.google.com/ berkeley.edu/fanuc-manipulation, 2023a. 

   - Zhu, Y., Stone, P., and Zhu, Y. Bottom-up skill discovery from unsegmented demonstrations for long-horizon robot manipulation. _IEEE Robotics and Automation Letters_ , 7 (2):4126–4133, 2022. 

   - Zhu, Y., Joshi, A., Stone, P., and Zhu, Y. Viola: Imitation learning for vision-based manipulation with object proposal priors. In _Conference on Robot Learning_ , pp. 1199–1210. PMLR, 2023b. 

   - Zhu, Z., Feng, X., Chen, D., Bao, J., Wang, L., Chen, Y., Yuan, L., and Hua, G. Designing a better asymmetric vqgan for stablediffusion. _arXiv preprint arXiv:2306.04632_ , 2023c. 

   - Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pp. 2165–2183. PMLR, 2023. 

- Zheng, J., Li, J., Liu, D., Zheng, Y., Wang, Z., Ou, Z., Liu, Y., Liu, J., Zhang, Y.-Q., and Zhan, X. Universal actions for enhanced embodied foundation models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 22508–22519, 2025. 

- Zheng, J., Li, J., Wang, Z., Liu, D., Kang, X., Feng, Y., Zheng, Y., Zou, J., Chen, Y., Zeng, J., et al. X-vla: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. In _Proceedings of the International Conference on Learning Representations (ICLR)_ , 2026. 

15 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

# **A. Open-Source Resources** 

- Code Repository: https://github.com/Open-X-Humanoid/XR-1. 

- Model Weights (HuggingFace): https://huggingface.co/collections/X-Humanoid/xr-1. 

- Model Weights (ModelScope): https://modelscope.cn/collections/X-Humanoid/XR-1. 

# **B. Implementation Details** 

In this section, we provide a detailed description of the XR-1 framework, focusing on the architecture and training of the dual-branch VQ-VAE. The model is designed to encode both vision dynamics and robotic motion into a shared discrete latent space, thereby enabling seamless integration of perception and control. 

## **B.1. Dual-Branch VQ-VAE** 

To achieve a unified latent representation, we introduce a dual-branch VQ-VAE consisting of two complementary encoders, a vision encoder and a motion encoder, that map their respective modalities into a common discrete codebook. Each branch is paired with a decoder to facilitate reconstruction during pretraining. The overall design ensures that the majority of representational capacity resides in the encoders, while the decoders primarily serve as auxiliary components for reconstruction. 

**Vision Branch.** The vision branch processes raw image observations _{ot, ot_ + _h}_ and encodes them into compact latent tokens. 

**Vision Branch Encoder.** We adopt SigLIP (Zhai et al., 2023) as the backbone vision encoder, comprising approximately 400M parameters. This encoder extracts high-level features from visual inputs. To capture temporal dynamics beyond static representations, we incorporate a visual dynamic module inspired by (Chen et al., 2025). This module is implemented as a four-layer transformer (ViT (He et al., 2022)) with 32M parameters, which compresses vision dynamic information into a fixed number of latent tokens by querying dynamic features. 

**Vision Branch Decoder.** For reconstruction, we employ a ViT-based decoder with 12 transformer layers (94M parameters). Importantly, the encoder contains roughly five times more parameters than the decoder. This asymmetry is intentional: by allocating more capacity to encoding, we encourage the model to produce informative latent tokens that simplify downstream decoding. Consequently, the decoder remains lightweight since its role is auxiliary rather than representationally dominant. 

During training, all parameters in both the SigLIP backbone and the dynamic module remain fully trainable. Additional details regarding training hyperparameters are provided in Table 5. 

**Motion Branch.** The motion branch encodes action sequences _{at_ : _t_ + _h}_ into discrete motion codes. 

**Motion Branch Encoder.** To capture temporal dependencies across actions, we employ 1D causal strided convolutions (Van Den Oord et al., 2016), which progressively reduce sequence length _h_ while preserving causality. The stride configuration determines the degree of temporal abstraction achieved at each stage. Following this convolutional compression, an 8-layer transformer encoder (34M parameters) further contextualizes action embeddings before quantization into discrete tokens. 

**Motion Branch Decoder.** For action reconstruction, we leverage Gemma (Beyer et al., 2024), an autoregressive language model with approximately 300M parameters. The design closely follows the action expert structure in _π_ 0 (Black et al., 2025), integrating diffusion-based supervision for reconstructing low-level actions from motion codes. Pretraining this decoder equips it with strong generative priors over action sequences, thereby providing an effective initialization for downstream policy learning. Additional details regarding training hyperparameters are provided in Table 5 

Overall, this dual-branch architecture ensures that both perception and motion are represented in a unified tokenized space via vector quantization (VQ), enabling scalable pretraining across multimodal data sources. 

## **B.2. XR-1 Models** 

**XR-1** . The proposed framework is designed to be model-agnostic, making it compatible with a wide range of visionlanguage-action (VLA) architectures. In this work, we instantiate XR-1 using a configuration inspired by the baseline policy 

16 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

_Table 5._ Implementation Details of Dual-Branch VQ-VAE. 

||Hyperparameter|Value||Hyperparameter|Type|Params.|
|---|---|---|---|---|---|---|
|Hyper-<br>parameter|Batch Size<br>Learning Rate<br>Optimizer<br>Trainable Parameters<br>Motion/Vision Codebook Category<br>Motion/Vision Codebook Embed. Dim<br>Motion/Vision Code Num.<br>Action Sequence|960<br>1e-4<br>AdamW<br>0.9B<br>256<br>256<br>13<br>50|Network<br>Architectures|Vision Encoder<br>Vision Dynamic Encoder<br>Vision Decoder<br>Vision Recons. Loss<br>Action Encoder<br>Action Decoder<br>Action Recons. Loss<br>-|SigLIP<br>ViT<br>ViT<br>MSE<br>Convolution and Transfomer<br>Transformer Decoder<br>Flow Matching<br>-|400M<br>32M<br>94M<br>-<br>33M<br>300M<br>-|
||Vision Interval|50||-|-||
||Training Step|275K||-|-||


_π_ 0 (Black et al., 2025) while introducing several key modifications that enable more structured representation learning. Specifically, XR-1 builds upon the PaliGemma architecture (Beyer et al., 2024), which integrates a SigLIP-based visual encoder (Zhai et al., 2023) with approximately 400 million parameters and a Gemma transformer backbone (Team et al., 2024a) with an action prediction head containing around 2.6 billion parameters. This design largely mirrors _π_ 0 in terms of scale and backbone selection, but diverges in how supervision is introduced. 

Instead of directly optimizing for action prediction as in _π_ 0, XR-1 leverages the UVMC produced by a Dual-Branch VQ-VAE as intermediate supervisory signals. The joint representation _zuvmc_ encodes both motion and visual dynamics information, which serves as guidance for training. To incorporate this signal effectively, we introduce two learnable tokens, [ _ZMO_ ] and [ _ZV IS_ ], that are responsible for predicting the robotic motion codes and the visual dynamics codes. These predictions are optimized using mean squared error loss against their respective targets. By enforcing this disentangled supervision on both motor control and perceptual dynamics, XR-1 encourages stronger alignment between perception and action. 

To ensure fairness in evaluation, XR-1 is initialized from PaliGemma’s publicly available pretrained checkpoint rather than directly adopting the released weights of _π_ 0. This avoids potential confounding effects due to differences in pretraining objectives or data exposure. Overall, XR-1 extends beyond _π_ 0 by introducing structured supervision through VQ-VAE latent codes and dedicated learnable tokens for motion and visual prediction, while maintaining compatibility with large-scale pretrained models such as PaliGemma. Additional details regarding training hyperparameters are provided in Table 6. 

_Table 6._ Implementation Details of XR-1. 

||Hyperparameter|Value||Hyperparameter|Value|
|---|---|---|---|---|---|
||Batch size|640||Decoder layer|18|
||Learning rate|1e-4||Transformer hidden dim|2048|
|Hyper-|Optimizer|AdamW|Network<br>|Heads num|8|
|parameter|[_ZMO_]Number|13|Architectures|Action Decoder layer|18|
||[_ZV IS_]Number|13*_viewnum_||Action Transformer hidden dim|1024|
||Action sequence|50||Action Heads num|8|
||Training step|300k||Action loss|flow matching|


**XR-1-Light** . To further highlight the flexibility of our approach, we introduce **XR-1-Light** , a lightweight variant of XR-1 that significantly reduces computational cost while maintaining competitive performance. The motivation behind XR-1-Light is to replace the large-scale PaliGemma backbone, which contains nearly 3 billion parameters, with a more efficient vision-language model (VLM) without sacrificing the ability to capture rich multimodal representations. For this purpose, we adopt Florence-2 (Xiao et al., 2024), a transformer-based model with approximately 230 million parameters, as the backbone within the SwitchVLA framework (Li et al., 2025a). This substitution enables faster training and inference while lowering memory requirements, making XR-1-Light more suitable for resource-constrained scenarios. 

Despite its reduced scale, XR-1-Light preserves the core design principles of XR-1. In particular, it continues to leverage the supervisory signal UVMC from the Dual-Branch VQ-VAE, which encodes both robotic motion and visual dynamics. To integrate this supervision effectively, we employ two learnable tokens, [ _ZMO_ ] and [ _ZV IS_ ], that are responsible for predicting the motion codes and the visual dynamics codes. Unlike in XR-1 where these tokens are attached to a decoder-only 

17 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

transformer backbone, in Florence-2 they are inserted between the encoder and decoder layers. This design allows the encoder to specialize in extracting structured latent representations aligned with UVMC, while enabling the decoder to function as an action expert that generates task-specific predictions conditioned on these learned codes. 

A notable difference between XR-1 and XR-1-Light lies in their training strategies. While XR-1 benefits from pretraining on XR-D before fine-tuning on downstream tasks, XR-1-Light omits this stage due to its lightweight architecture. Instead, it is directly fine-tuned on task-specific datasets. This choice reflects a trade-off: although pretraining could potentially enhance generalization, direct fine-tuning allows us to fully exploit Florence-2’s efficiency without incurring additional computational overhead. 

In summary, XR-1-Light demonstrates that our framework can be instantiated not only with large-scale backbones such as PaliGemma but also with compact VLMs like Florence-2. By maintaining structured supervision through _zuvmc_ while reducing parameter count by more than an order of magnitude, XR-1-Light provides a practical alternative that balances performance with efficiency. Additional details regarding training hyperparameters are provided in Table 7. 

_Table 7._ Implementation Details of XR-1-Light 

||Hyperparameter|Value||Hyperparameter|Value|
|---|---|---|---|---|---|
||Batch Size|160||Encoder Layer|6|
||Learning Rate|5e-5||Transformer Hidden Dim.|768|
|Hyper-|Optimizer|AdamW|Network<br>|Heads Num.|12|
|parameter|[_ZMO_]Number|13|Architectures|Action Decoder Layer|6|
||[_ZV IS_]Number|13*_viewnum_||Action Transformer Hidden Dim.|768|
||Action Sequence|50||Action Heads Num.|12|
||Training Step|50K||Action Loss|Flow Matching|


## **B.3. Training and Inference** 

The training of our framework is organized into three stages: UVMC learning, UVMC-guided pretraining, and policy fine-tuning. Each stage progressively aligns perception, representation, and control while balancing computational efficiency. 

In the first stage, the UVMC module, containing approximately 0.9B parameters, is pretrained on large-scale multimodal data. This process consumed roughly 38 _,_ 400 GPU hours on a cluster of 80 NVIDIA A100 GPUs (80GB each), enabling the model to capture both motion and visual dynamics representations. 

The second stage involves policy pretraining, where the complete model scales up to about 4B parameters. This step also required around 38 _,_ 400 GPU hours on the same hardware configuration. The objective here is to integrate the pretrained UVMC representations into a unified vision-language-action policy. 

In the final stage, policy fine-tuning is performed for embodiment-specific adaptation. Each embodiment configuration is fine-tuned across 20 downstream tasks using 8 A100 GPUs (80GB), requiring approximately 576 GPU hours per embodiment. This ensures that XR-1 and its variants generalize effectively to diverse robotic environments while remaining computationally practical. 

For inference, we emphasize both responsiveness and throughput. The system operates with an action chunk inference frequency of about 5 Hz while maintaining an average action-level inference rate close to 200 Hz (actions per second). These frequencies are achieved on a single commercially available RTX 4090 GPU (24GB), demonstrating that despite large-scale pretraining costs, deployment remains efficient without reliance on massive compute resources. 

# **C. Dataset Curation** 

Large-scale pretraining has consistently been shown to enhance both generalization and rapid adaptation in multimodal learning systems. Motivated by these findings, we curate a comprehensive dataset tailored for robotic manipulation, integrating diverse sources of visual, linguistic, and action-centric data. Our dataset construction draws from four complementary resources: _Open-X_ (O’Neill et al., 2024), which provides large-scale open-world manipulation trajectories; _RoboMIND_ (Wu et al., 2025a), a benchmark emphasizing reasoning-driven robotic tasks; _Ego4D_ (Grauman et al., 2022), a first-person human activity dataset offering rich egocentric perspectives; and _XR-D_ , our in-house collection spanning multiple robotic 

18 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 8._ Overview of the pretraining datasets used for XR-1. We combine Open-X, RoboMIND, Ego4D, and our dataset XR-D, with a total of _∼_ 1,264k episodes and 110M frames. 

embodiments and task domains. Together, these sources cover a wide spectrum of sensory modalities, embodiment variations, and task complexities, forming a foundation for scalable pretraining. 

The training procedure is organized into three progressive stages. In **Stage-1** , we pretrain a dual-branch VQ-VAE on the combined datasets to learn disentangled latent representations of motion and visual dynamics. In **Stage-2** , we leverage XR-D to pretrain the vision-language-action (VLA) backbone, aligning multimodal perception with action generation across diverse embodiments. Finally, in **Stage-3** , we fine-tune on novel scenes and previously unseen tasks outside XR-D in order to rigorously assess transferability and generalization beyond the pretraining distribution. 

A detailed breakdown of dataset statistics, including scale, modality coverage, and embodiment diversity across all sources used for UVMC pretraining, is provided in Figure 8 and Table 8. 

_Table 8._ Pretraining Dataset Details. 

|**Dataset**|**Episode**|**Frames**|**Weight**|
|---|---|---|---|
|**OXE (O’Neill et al., 2024)**|**978,582**|**59.3M**|**40%**|
|FMB Dataset (Luo et al.,2025)|8611|1137340|0.88%|
|DROID (Khazatsky et al.,2024)|92233|27044326|9.43%|
|Language Table (Lynch et al.,2023)|442226|7045476|45.19%|
|Berkeley Autolab UR5 (Chen et al.)|896|87783|0.09%|
|Berkeley Fanuc Manipulation (Zhu et al.,2023a)|415|62613|0.04%|
|Berkeley Cable Routing (Luo et al.,2024)|1482|38240|0.15%|
|Berkeley Gnm Cory Hall (Kahn et al.,2018)|7331|156012|0.75%|
|Berkeley Gnm Recon (Shah et al.,2021)|11834|610907|1.21%|
|Berkeley Gnm Sac Son (Hirose et al.,2023)|2955|241059|0.30%|
|Berkeley MVP (Radosavovic et al.,2023b)|480|45308|0.05%|
|Berkeley RPT (Radosavovic et al.,2023a)|908|392578|0.10%|
|Bridge (Ebert et al.,2022;Walke et al.,2023)|25460|813372|2.60%|
|BC-Z (Jang et al.,2022)|43264|6015535|4.42%|
|Taco Play (Rosete-Beas et al.,2023;Mees et al.,2023)|3242|213972|0.33%|
|NYU Franka Play Dataset (Cui et al.,2023)|365|34448|0.04%|
|Asu Table Top (Zhou et al.,2022b;2023)|110|26113|0.01%|
|Austin Buds Dataset (Zhu et al.,2022)|50|34112|0.01%|
|Austin Sailor Dataset (Nasiriany et al.,2022)|240|353094|0.02%|
|Austin Sirius Dataset (Liu et al.,2022)|559|279939|0.05%|
|CMU Play Fusion (Chen et al.,2023)|576|235922|0.05%|
|CMU Stretch (Bahl et al.,2023;Mendonca et al.,2023)|135|25016|0.01%|
|Columbia Cairlab Pusht Real (Chi et al.,2023)|122|24924|0.01%|


Continued on next page 

19 

### **XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|**Dataset**|**Episode**|**Frames**|**Weight**|
|---|---|---|---|
|DLR EDAN Shared Control (Vogel et al.,2020;Quere et al.,2020)|104|8928|0.01%|
|DLR Sara Grid Clamp (Padalkar et al.,2023a)|107|7622|0.01%|
|DLR Sara Pour (Padalkar et al.,2023b)|100|12971|0.01%|
|DobbE (Shafiullah et al.,2023)|5208|1139911|0.52%|
|Stanford Hydra Dataset (Belkhale et al.,2023)|570|358234|0.06%|
|Tokyo U Lsmo (Osa,2022)|50|11925|0.01%|
|Toto (Zhou et al.,2022a)|902|294139|0.10%|
|UCSD Kitchen Dataset (Yan & Wang,2023)|150|3970|0.02%|
|UCSD Pick and Place Dataset (Feng et al.,2023)|1355|67750|0.14%|
|UTAustin Mutex (Shah et al.,2023)|1500|361883|0.15%|
|U-Tokyo PR2 Opening Fridge (Oh et al.,2023)|64|9140|0.01%|
|U-Tokyo PR2 Tabletop Manipulation (Oh et al.,2023)|192|26346|0.02%|
|U-Tokyo xArm Bimanual (Oh et al.,2023)|64|1388|0.01%|
|<br>U-Tokyo xArm Pick and Place (Oh et al.,2023)|92|6789|0.01%|
|<br>Viola (Zhu et al.,2023b)|135|68913|0.01%|
|Fractal (Brohan et al.,2023)|87212|3786400|8.91 %|
|Furniture Bench Dataset (Heo et al.,2023)|5100|3948057|0.51%|
|<br>IAMLab CMU Pickup Insert (Saxena et al.,2023)|631|146241|0.06%|
|<br>Jaco Play (Dass et al.,2023)|976|70127|0.10%|
|Kaist Non-prehensile (Kim et al.,2023)|201|32429|0.02%|
|<br>Kuka (Kalashnikov et al.,2018)|209880|2455879|21.45%|
|NYU Door Opening Surprising Effectiveness (Pari et al.,2022)|435|18196|0.04%|
|NYU ROT Dataset (Haldar et al.,2023)|14|440|0.01%|
|RoboSet (Bharadhwaj et al.,2024)|18250|1419999|1.86%|
|<br>Roboturk (Mandlekar et al.,2019)|1796|168423|0.18%|
|**RoboMIND (Wu et al., 2025a)**|**69274**|**21.4M**|**15%**|
|Single-Arm Franka|16018|2268033|23.12%|
|<br>Dual-Arm Franka|1774|375807|2.56%|
|Single-Arm UR-5e|25721|2643322|37.13%|
|AgileX Cobot Magic V2.0|10059|6477564|14.52%|
|Tien Kung 1.0|15702|9683213|22.67%|
|**XR-D**|**158639**|**69.1M**|**35%**|
|Single-Arm Franka|16933|5240845|10.67%|
|Dual-Arm Franka|56800|17140497|35.80%|
|Single-Arm UR-5e|21954|3218116|13.84%|
|<br>Dual-Arm UR-5e|33916|5463729|21.38%|
|AgileX Cobot Magic V2.0|8004|16576019|5.05%|
|<br>ARX LIFT|11866|15845836|7.48%|
|Tien Kung 1.0|9166|5605573|5.78%|
|**Ego4D (Grauman et al., 2022)**|**59427**|**14.3M**|**10%**|


20 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

# **D. Additional Real-World Experiments** 

_Table 9._ Success rate results across 20 tasks on Tien Kung 1.0. 

|Method|TK1-Close<br>Drawer|TK1-Flip<br>TennisTube|TK1-Press<br>CookerButton|TK1-Move<br>ChopstickCup|TK1-Stack<br>Cubes|TK1-Stack<br>Cups|TK1-Stack<br>Plates|TK1-Pick<br>WipeTowel|TK1-Hang<br>Towel|TK1-Open<br>PotLid|-|
|---|---|---|---|---|---|---|---|---|---|---|---|
|UniVLA|25|0|25|10|0|0|35|0|0|0|-|
|RDT|45|0|65|0|0|0|70|0|0|0|-|
|GR00T-N1.5|75|20|85|20|0|0|70|0|0|0|-|
|_π_0|75|40|45|25|0|0|80|0|0|0|-|
|_π_0_._5|75|35|55|60|0|0|75|0|0|0|-|
|XR-1 (ours)|80|50|90|65|65|20|85|55|65|20|-|
||TK1-Open<br>Oven|TK1-Pack<br>EggBox|TK1-Close<br>Laptop|TK1-Insert<br>Toaster|TK1-Flip<br>Cup|TK1-Place<br>FlipButton|TK1-Open<br>TrashBin|TK1-Press<br>Machine|TK1-Find<br>Tape|TK1-Stack<br>Bowls|Avg.|
|UniVLA|30|0|0|30|0|0|25|20|20|30|12.5|
|RDT|0|0|90|0|0|0|85|55|0|0|20.5|
|GR00T-N1.5|55|0|15|40|0|0|70|45|45|45|29.3|
|_π_0|75|10|90|65|10|15|75|70|70|80|41.3|
|_π_0_._5|80|20|95|65|30|25|65|75|75|80|45.5|
|XR-1 (ours)|80|65|95|70|65|65|85|75|75|90|68.0|


**Results on Tien Kung 1.0** . Table 9 reports success rates across 20 tasks on Tien Kung 1.0. XR-1 again outperforms all baselines by a clear margin. For example, in _TK1-HangTowel_ , it achieves 65% success while all baselines fail (0%). Overall, XR-1 attains an average success rate of 68 _._ 0%, substantially higher than _π_ 0 (41 _._ 3%) and more than double RDT (20 _._ 5%) and UniVLA (12 _._ 5%). These results highlight the effectiveness of UVMC supervision in providing robust representations and stable optimization across diverse manipulation skills. 

_Table 10._ Success rate results across 20 tasks on Dual-Arm Franka. 

|Method|DFR-Move<br>CupMilk|DFR-Stack<br>Bowls|DFR-Sweep<br>Trash|DFR-Transfer<br>Cup|DFR-Move<br>Chopstick|DFR-Stack<br>Cubes|DFR-Stack<br>Plates|DFR-Clean<br>Table|DFR-Hang<br>CupHolder|DFR-Hang<br>TowelRack|-|
|---|---|---|---|---|---|---|---|---|---|---|---|
|UniVLA|15|20|0|30|0|5|25|35|0|20|-|
|RDT|55|40|0|0|15|60|90|65|0|0|-|
|GR00T-N1.5|80|85|35|55|0|15|45|90|25|50|-|
|_π_0|0|75|35|60|0|75|80|80|0|25|-|
|_π_0_._5|15|85|60|40|0|55|90|85|45|20|-|
|XR-1 (ours)|80|85|75|90|55|60|90|90|65|60|-|
||DFR-Find|DFR-Pick|DFR-Sweep|DFR-Close|DFR-Collect|DFR-Place|DFR-Get|DFR-Place|DFR-Open|DFR-Place|A|
||TapeBox|ButtonPress|Rubbish|Toolbox|BasketTea|Tools|Blocks|RagWipe|Toolbox|Screws|vg.|
|UniVLA|25|0|0|15|10|0|25|20|0|0|12.3|
|RDT|0|20|0|25|0|0|5|55|0|0|21.5|
|GR00T-N1.5|80|0|0|85|35|0|70|0|0|0|37.5|
|_π_0|90|30|0|0|0|0|75|70|50|0|37.3|
|_π_0_._5|65|25|30|0|0|60|75|70|0|0|41.0|
|XR-1 (ours)|90|75|60|90|75|60|85|70|60|55|73.5|


**Results on Dual-Arm Franka** . Table 10 reports success rates across 20 tasks on the Dual-Arm Franka. XR-1 achieves the highest average performance (73 _._ 5%), substantially outperforming _π_ 0 (37 _._ 3%) and other baselines. For example, in _DFR-TransferCup_ it reaches 90% success, while all alternatives fall below 60%. It is because XR-1 leverages UVMC for richer supervision, yielding robust representations and stable learning across diverse objectives. 

21 

### **XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

_Table 11._ Success rate results across 20 tasks on AgileX Cobot Magic V2.0. 

|Method|AGX-Open<br>DrawerButton|AGX-Move<br>ButtonDrawer|AGX-Stack<br>Boxes|AGX-Find<br>TapeBox|AGX-Sweep<br>Rubbish|AGX-Arrange<br>Valves|AGX-Hang<br>Scissors|AGX-Place<br>Button|AGX-Close<br>Toolbox|AGX-Gather<br>Screws|-|
|---|---|---|---|---|---|---|---|---|---|---|---|
|UniVLA|25|15|0|0|0|0|25|25|20|0|-|
|RDT|70|75|20|60|0|30|0|60|0|0|-|
|GR00T-N1.5|85|75|20|75|0|45|0|80|0|0|-|
|_π_0|85|85|0|60|0|45|0|0|0|0|-|
|_π_0_._5|35|70|40|80|15|35|0|70|35|30|-|
|XR-1 (ours)|90|80|45|75|25|45|80|85|90|30|-|
||AGX-Find<br>Circuit|AGX-Place<br>BiscuitBox|AGX-Collect<br>BasketTea|AGX-Place<br>Screwdriver|AGX-Pour<br>GearOil|AGX-Stack<br>BrakePads|AGX-Mesh<br>StackCup|AGX-Pour<br>Wine|AGX-Hang<br>WipeRag|AGX-Stack<br>Bowls|Avg.|
|UniVLA|0|0|0|0|10|10|25|0|0|20|8.8|
|RDT|0|0|0|0|0|55|0|0|65|85|28.5|
|GR00T-N1.5|0|50|45|0|0|0|0|0|20|70|24.0|
|_π_0|0|40|45|55|40|0|55|0|50|90|32.5|
|_π_0_._5|20|60|25|30|55|40|15|20|60|90|41.3|
|XR-1 (ours)|15|60|35|35|75|85|90|20|55|85|60.0|


**Results on AgileX Cobot Magic V2.0** . Table 11 reports success rates on 20 tasks with the AgileX Cobot Magic V2.0. XR-1 achieves an average of 60 _._ 0%, nearly doubling _π_ 0 (32 _._ 5%) and far surpassing UniVLA (8 _._ 8%). On challenging tasks such as _AGX-StackBrakePads_ and _AGX-CloseToolbox_ , it reaches 85 _−_ 90%, while other methods collapse to near 0%. We attribute these gains to UVMC-driven representations, which provide richer supervision and stabilize multi-task optimization. 

_Table 12._ Success rate results across 20 tasks on Single-Arm UR-5e. 

|Method|SUR-Find<br>Tape|SUR-Move<br>MilkCup|SUR-Stack<br>Bowls|SUR-Open<br>Drawer|SUR-Close<br>Drawer|SUR-Insert<br>ToyBlock|SUR-Place<br>Chopstick|SUR-Stack<br>Cubes|SUR-Stack<br>Cup|SUR-Stack<br>Plates|-|
|---|---|---|---|---|---|---|---|---|---|---|---|
|UniVLA|35|25|50|20|35|0|0|0|0|0|-|
|RDT|80|35|20|35|45|0|0|0|0|0|-|
|GR00T-N1.5|85|70|80|25|70|0|0|0|25|0|-|
|_π_0|25|55|90|50|85|0|0|80|0|55|-|
|_π_0_._5|55|30|95|85|95|0|35|90|90|85|-|
|XR-1 (ours)|95|85|95|90|90|15|20|90|85|85|-|
||SUR-Slide<br>Drawer|SUR-Open<br>UpperDrawer|SUR-Open<br>Oven|SUR-Pack<br>EggBox|SUR-Close<br>Laptop|SUR-Insert<br>Bread|SUR-Assemble<br>Valve|SUR-Pour<br>TubeBeaker|SUR-Pour<br>GearOil|SUR-Wipe<br>HangRag|Avg.|
|UniVLA|30|30|35|0|35|0|30|0|20|30|18.8|
|RDT|40|35|55|15|50|0|15|10|35|30|25.0|
|GR00T-N1.5|45|65|80|0|90|0|80|0|10|30|37.8|
|_π_0|75|90|55|20|85|30|20|10|45|75|47.3|
|_π_0_._5|90|90|95|80|90|85|25|10|50|75|67.5|
|XR-1 (ours)|80|90|90|70|90|65|90|20|85|75|75.3|


**Results on Single-Arm UR-5e** . Table 12 summarizes success rates over 20 tasks on the Single-Arm UR-5e. XR-1 achieves the highest average success of 75 _._ 3%, clearly surpassing _π_ 0 (47 _._ 3%) and all other baselines. XR-1 maintains strong performance (65% and 85%) on hard tasks like _SUR-InsertBread_ and _SUR-StackPlates_ where baselines often collapse to near 0%. These results highlight the robustness and generalization ability of XR-1 enabled by UVMC. 

22 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

_Table 13._ Success rate results across 20 tasks Dual-Arm UR-5e. 

|Method|DUR-Find<br>TapeBasket|DUR-Move<br>CupMilk|DUR-Stack<br>Bowls|DUR-Sweep<br>Trash|DUR-Trans<br>CupHolder|DUR-Stack<br>Cubes|DUR-Hang<br>CupHolder|DUR-Stack<br>Brake|DUR-Sweep<br>Rubbish|DUR-Press<br>Button|-|
|---|---|---|---|---|---|---|---|---|---|---|---|
|UniVLA|30|35|35|20|0|0|0|0|0|10|-|
|RDT|45|65|50|0|30|0|60|15|10|20|-|
|GR00T-N1.5|25|60|80|0|0|0|0|0|0|0|-|
|_π_0|70|55|80|55|15|15|10|0|0|35|-|
|_π_0_._5|45|65|90|60|55|20|10|85|70|80|-|
|XR-1 (ours)|85|65|85|60|65|20|85|65|80|85|-|
||DUR-Pick<br>PlaceTape|DUR-Close<br>Toolbox|DUR-Assemble<br>Valve|DUR-Flip<br>TennisTube|DUR-Place<br>Tools|DUR-Close<br>DoorKnob|DUR-Take<br>BasketTea|DUR-Pick<br>Toolbox|DUR-Open<br>TrashBin|DUR-Trans<br>Buttons|Avg.|
|UniVLA|35|30|25|20|30|40|25|30|30|0|19.8|
|RDT|85|10|0|35|0|20|85|0|0|0|26.5|
|GR00T-N1.5|55|0|50|45|65|80|90|55|85|0|34.5|
|_π_0|20|85|0|70|35|85|80|70|55|20|42.8|
|_π_0_._5|65|90|45|70|65|50|90|75|75|35|62.0|
|XR-1 (ours)|85|90|55|80|65|90|90|75|85|30|72.0|


**Results on Dual-Arm UR-5e** . In addition to the bar plot reported in Figure 4, we provide the corresponding numerical results in Table 13. The table summarizes success rates across 20 tasks on the Dual-Arm UR-5e, offering a more detailed comparison among different methods. 

# **E. Additional Ablation Study** 

**Ablation study of UVMC.** To obtain deeper insights into the UVMC architecture and its key hyperparameter choices, we conduct 10 ablation experiments, as summarized in Table 14, with Exp.10 serving as the baseline. By comparing Exp.1–6 against Exp.10, we analyze the influence of different codebook category numbers and code dimensions on the final performance. For the code dimension, Exp.1–3 adopt 64, 128, and 512, respectively, and are compared with the baseline setting of 256 in Exp.10. The results show that when the dimension is below 256, policy performance consistently improves as the dimension increases from 64 to 128 and 256, while further increasing it to 512 yields no clear additional gains, suggesting that a dimension of 256 is already near-optimal. Using a similar protocol in Exp.4–6 for the category number, we finally adopt 256 categories and a 256-dimensional codebook as our default configuration. Next, by comparing Exp.7–8 with Exp.10, we evaluate the difference between using only motion codes, only vision codes, and the unified vision–motion code (UVMC). The results indicate that both motion-only and vision-only variants underperform the unified UVMC. Moreover, vision-only codes outperform motion-only codes, while combining both modalities within UVMC leads to complementary effects and improved overall performance. Finally, by comparing Exp.9 and Exp.10, we investigate whether a combined or separate codebook is more effective. The results show that both designs achieve comparable performance, which we attribute to the alignment loss imposed during training: although a separate codebook increases the number of learnable codes, the alignment constraint effectively regulates cross-modal relationships, leading to similar execution capabilities for both schemes. 

_Table 14._ Ablation study of UVMC. 

|E|Cdbk|Ct_×_EbdDi|UVMC Tk|St1&2&3|DUR-Clean|DUR-Find|DUR-Move|DUR-Stack|DUR-Sweep|DUR-Trans|A|
|---|---|---|---|---|---|---|---|---|---|---|---|
|xp.|oeoo|aegoryme.m|oen|age-|Table|TapeBasket|CupMilk|Bowls|Trash|CupHolder|vg|
|1|combine|256_×_64|both|DT|35|55|50|60|35|45|46.7|
|2|combine|256_×_128|both|DT|45|65|60|70|55|65|60.0|
|3|combine|256_×_512|both|DT|55|75|50|85|65|55|64.2|
|4|combine|64_×_256|both|DT|45|60|55|65|35|50|51.7|
|5|combine|128_×_256|both|DT|50|65|55|65|60|60|59.2|
|6|combine|512_×_256|both|DT|40|80|60|80|55|65|63.3|
|7|combine|256_×_256|motion-only|DT|25|70|35|60|5|15|35.0|
|8|combine|256_×_256|vision-only|DT|10|70|65|70|15|65|50.0|
|9|separate|256_×_256|both|DT|55|75|55|85|40|80|65.0|
|10|combine|256_×_256|both|DT|50|75|65|80|60|70|66.7|


**Ablation study of Ego4d.** To further examine the contribution of human video data (Ego4D) in the pre-training stage, we conduct a set of ablation experiments, as summarized in Table 15. To balance computational cost and the reliability of the conclusions, we use 10% of the full pre-training dataset for these comparisons. Under this setting, we evaluate two variants: one with Ego4D included in the pre-training data and one without Ego4D (w/o Ego4D). As shown in Table 15, 

23 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

removing Ego4D leads to a 5.8% drop in average success rate compared to the setting that includes Ego4D. These results quantitatively suggest that incorporating Ego4D into the pre-training data can effectively improve performance. 

_Table 15._ Ablation study of Ego4d. 

|Exp.|Instantiation|Stage-1|Stage-2|Stage-3|DUR-Clean<br>Table|DUR-Find<br>TapeBasket|DUR-Move<br>CupMilk|DUR-Stack<br>Bowls|DUR-Sweep<br>Trash|DUR-Trans<br>CupHolder|Avg|
|---|---|---|---|---|---|---|---|---|---|---|---|
|1|XR-1 w/o Ego4D|10%|DT|✓|20|60|10|55|15|35|32.5|
|2|XR-1 w/ Ego4D|10%|DT|✓|25|60|25|60|20|40|38.3|


**Cross-Embodied Knowledge Transfer for Enhanced Single Embodiment Performance** . This setup is designed to verify whether similar tasks across different embodiments can mutually benefit each other. Since the UVMC counterpart of XR-1 learns an embodiment-agnostic feature, this setup serves to validate that capability. Specifically, we selected two identical tasks (FindTape and SweepRubbish) across three different embodiments (Dual-Arm Franka, Dual-Arm UR5e, and Tien Kung 2.0). The detailed results are shown in Table 16. Exp. 2 represents the results of training these two skills across three different embodiments, resulting in six tasks. In the comparative experiment setup, training two skills for a specific embodiment typically results in only two tasks. Therefore, to ensure fairness, in Exp. 1, we added four additional tasks for the same embodiment, ensuring that the data volume is equivalent. _The final results indicate that learning the same skills across different embodiments can enhance the success rate of each embodiment’s skills, increasing the average success rate by approximately 15%._ This demonstrates that the UVMC module has learned an embodiment-agnostic beneficial feature. 

_Table 16._ Ablation study of XR-1 on cross-embodiment knowledge transfer. 

|Exp.|Instantiation|Stage-1|Stage-2|Stage-3|DFR-Find<br>TapeBox|DFR-Sweep<br>Rubbish|DUR-Pick<br>PlaceTape|DUR-Sweep<br>Rubbish|TK2-Take<br>Tape|TK2-Sweep<br>Rubbish|Avg.|
|---|---|---|---|---|---|---|---|---|---|---|---|
|1|XR-1|100%|XR-D|SelfRobot|50|20|70|50|60|30|47|
|2|XR-1|100%|XR-D|CrossRobot|70|30|70|60|70|70|62|


# **F. Additional Generalization Analysis** 


_Figure 9._ Out-of-box evaluation results of 7 tasks on Dual-Arm UR-5e. 

**Out-of-Box Evaluation** . In addition to the evaluation on the Dual-Arm Franka, we also conduct an out-of-box evaluation of XR-1 on the Dual-Arm UR-5e. Specifically, we select 7 representative tasks from XR-D, covering only 0 _._ 45% of the dataset. To ensure a fair comparison, baselines without XR-D pretraining are fine-tuned on data from these tasks prior to evaluation. As shown in Figure 9, the pretrained **XR-1-oob** model, even without Stage-3 task-specific adaptation, achieves performance comparable to _π_ 0, while consistently outperforming GR00T-N1.5, RDT, and UniVLA. This result highlights XR-1’s strong generalization ability in low-data regimes. 

24 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 10._ Fast adaption on Dual-Arm UR5e. Dual-Arm UR5e is an embodiment included in XR-D. In this setup, Here, XR-1 adapts to 15 novel tasks with one model using only 20-shot demonstrations per task, while baselines (ACT and DP) are trained per task. 

**Fast Adaptation to New Tasks** . Beyond the experiments on Tien Kung 2.0, we also evaluate fast adaptation on the Dual-Arm UR-5e. Specifically, we collect 15 new tasks that are unseen in XR-D, each with 20 trajectories for training. XR-1 is trained jointly across these tasks, while single-task baselines, ACT (Zhao et al., 2023) and Diffusion Policy (DP) (Chi et al., 2023), are trained independently per task. As shown in Figure 10, XR-1 achieves substantially higher success rates than ACT and DP, even though the evaluation setting is more favorable to the baselines. This performance gain can be attributed to large-scale pretraining combined with UVMC supervision, which enables XR-1 to extract transferable representations from few-shot data and adapt effectively across diverse manipulation tasks. 

# **G. Simulation Results on CALVIN** 

**Simulation Benchmark** . CALVIN (Mees et al., 2022) is a comprehensive simulated benchmark for evaluating languageconditioned policies in long-horizon robotic manipulation. It consists of four distinct yet closely related environments, denoted A, B, C, and D, which differ in desk textures and object layouts, as shown in Figure 11. The benchmark contains 34 manipulation tasks with unconstrained language instructions. Each environment features a Franka Emika Panda robot equipped with a parallel-jaw gripper, along with a tabletop scene containing a sliding door, a drawer, colored blocks, an LED, and a light bulb, all of which can be interacted with or manipulated. 

**Results** . We report results on the challenging CALVIN benchmark under the D _→_ D setting. This setting is particularly sensitive to error accumulation and the resulting distribution drift. As shown in Table 17, XR-1 achieves a new state-of-the-art success score of 4.256, outperforming strong baselines such as _π_ 0 _._ 5 (3.885) and Qwen-GR00T (3.786). Notably, XR-1 maintains a success rate of 0.741 on the fifth sub-task, demonstrating stronger long-horizon robustness and improved resistance to distribution drift. 

# **H. Visualization of Unified Vision-Motion Codes** 

## **H.1. Frame-to-Frame Nearest-Neighbor Retrieval between Motion and Vision Codes** 

To further evaluate whether the vision code (VC) and motion code (MC) are semantically aligned in the latent space, we design a nearest-neighbor retrieval experiment, as shown in Figure 12. We select 7 tasks, each with 10 trajectory episodes, and compute the VC and MC for all frames in each episode. At the current time step _T_ , we extract the MCs corresponding to the actions GRASP and MOVE, as illustrated in the first column of Figure 12, and visualize the image of the current frame to better interpret the motion code semantics. We then compute VC features from different tasks and embodiments and, using cosine similarity, identify for each MC feature at time _T_ its nearest-neighbor and farthest-neighbor VC feature. Columns two through five of Figure 12 report the cosine distances between MC and VC features under four settings: Same Embodiment with a Similar Task (SE.ST.), Same Embodiment with a Different Task (SE.DT.), Different Embodiment with a Similar Task (DE.ST.), and Different Embodiment with a Different Task (DE.DT.). For the different-embodiment setting, we use a dual-arm Franka robot. To standardize the notion of left and right across embodiments, we define them with respect to 

25 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Table 17._ Comparison of XR-1 with baselines on CALVIN D _→_ D. 

|Method|1|2|3|4|5|Success Rate|
|---|---|---|---|---|---|---|
|OpenVLA|0.716|0.385|0.180|0.088|0.041|1.411|
|RDT-1B|0.757|0.495|0.359|0.243|0.184|2.038|
|_π_0|0.848|0.704|0.559|0.466|0.377|2.954|
|Qwen-_π_0|0.909|0.795|0.696|0.622|0.554|3.576|
|Qwen-GR00T|0.925|0.839|0.744|0.679|0.599|3.786|
|_π_0_._5|0.925|0.840|0.766|0.710|0.644|3.885|
|**XR-1 (ours)**|**0.964**|**0.908**|**0.845**|**0.798**|**0.741**|**4.256**|


_Figure 11._ The upper four environments correspond to the CALVIN ABCD settings. The bottom section shows a sequence of five longhorizon tasks, each guided by a specific instruction. 

the outward-facing direction of the embodiment. 

Comparing SE.ST. with GRASP and MOVE shows that, under the same embodiment and a similar task, the nearest-neighbor VC for a given MC consistently reflects the same action semantics, whereas the farthest-neighbor images display clearly different motions. Under the SE.DT. setting, despite task changes, the nearest-neighbor VCs still capture the semantics of grasp or move, while the farthest-neighbor images correspond to distinct motions. In the DE.ST. setting, even with different embodiments, the nearest-neighbor frames for a similar task consistently depict similar actions, in contrast to the clearly different motions in the farthest-neighbor images. Likewise, in the DE.DT. setting, nearest-neighbor retrieval continues to select frames whose semantics are closest to grasp or move, despite differences in both embodiment and task, whereas the farthest-neighbor images represent dissimilar actions. Together, these visualizations demonstrate that UVMC successfully learns semantic representations of different actions, and that these representations become embodiment-agnostic. 

## **H.2. Task-to-Task Nearest-Neighbor Retrieval between Motion and Vision Codes** 

In the preceding analysis (Appendix H.1), we primarily evaluate nearest-neighbor retrieval performance at the frame-to-frame level for representative skills (e.g., grasp, move) under different experimental settings (SE.ST., SE.DT., DE.ST., DE.DT.). To further investigate cross-task similarity from an episode-to-episode perspective, we construct the nearest-neighbor similarity distribution as illustrated in Figure 13. Specifically, we select four distinct tasks and perform pairwise comparisons among them, following the same experimental configurations as before (SE.ST., SE.DT., DE.ST., DE.DT.). Specifically, let the motion code of the _i_ -th frame in the source task be denoted by MC _i_ , and the vision code of the _j_ -th frame in the target task be denoted by VC _j_ . We first compute the similarity between each MC _i_ in the source task and all VC _j_ in the target task: 


where _Ts_ and _Tt_ denote the number of frames in the source and target tasks, respectively. Based on this matrix **S** , we perform a column-wise maximization, i.e., for each target frame _j_ , we select from all source frames the motion-vision pair that attains the highest similarity: 


In this way, we reduce the original two-dimensional similarity matrix to a similarity vector: 


which characterizes, for each target frame, its nearest-neighbor similarity with the source task. Finally, we normalize the elements of **s** to obtain a normalized nearest-neighbor similarity vector ˜ **s** , whose values are constrained to lie within [0 _,_ 1], enabling comparable and stable statistical analysis across different tasks. 

In Table 18, we report pairwise comparison results across different tasks. We take task 1 as the reference and use cosine similarity to quantify representational similarity between tasks. Under the SE.ST. setting, the mode of the similarity distribution is close to 1, indicating that for identical embodiments and tasks, the model learns highly consistent representations between MC and VC. Among the remaining three settings, DE.ST. has the highest mode, suggesting that UVMC learns features that 

26 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 12._ **Frame-to-Frame Nearest-neighbor Retrieval between motion and vision codes.** In the first column, we select two representative skill actions, grasp and move, and compute their Motion Codes (MC). Columns two through five report the cosine distances between Motion Code (MC) and Vision Code (VC) features and their nearest and farthest neighbors under four settings: Same Embodiment with a Similar Task (SE.ST.), Same Embodiment with a Different Task (SE.DT.), Different Embodiment with a Similar Task (DE.ST.), and Different Embodiment with a Different Task (DE.DT.). For the different-embodiment setting, we use a dual-arm Franka robot. To standardize the notion of left and right across embodiments, we define them with respect to the outward-facing direction of the embodiment. 

are largely independent of embodiment and instead capture action-centric skills. Comparing DE.ST. with SE.DT. further supports this: different-embodiment but similar-task pairs exhibit higher overall similarity than same-embodiment but different-task pairs, implying stronger semantic alignment for shared skills than for shared morphology alone. Although DE.DT. has the lowest mode, it still retains non-trivial similarity, indicating that shared low-level skills (such as pick, handover, and place) give rise to stable cross-task, cross-embodiment similarity in the learned representations. We also compute the average nearest-neighbor similarity under these settings and observe consistent conclusions. Consequently, these analyzes demonstrate that UVMC learns semantically meaningful action representations that are largely invariant to embodiment. 

## **H.3. Visualizing UVMC with t-SNE** 

To qualitatively validate whether UVMC effectively captures intrinsic task dynamics and abstracts away physical embodiment details, we employ t-SNE to project the high-dimensional latent embeddings into a two-dimensional manifold. We conduct this analysis on two distinct subsets: (1) a single-robot scenario involving 6 tasks performed by a dual-arm UR robot (Figure 14), and (2) a mixed-embodiment scenario comprising both dual-arm Franka and dual-arm UR robots (Figure 15). 

27 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 13._ **Task-to-task nearest-neighbor retrieval between motion and vision codes.** It illustrates four different tasks and annotates the corresponding process phase at each timestep. For each task, the annotations correspond one-to-one to the four experimental settings in Table 18, representing the actual procedure used to compute nearest-neighbor retrieval across different tasks. 

The visualization reveals two critical properties of the representation learned by UVMC. 

**Semantic Consistency of Dynamics.** As shown in Figure 14, the embedding space exhibits a structured organization where tasks characterized by similar motion primitives form cohesive, proximal clusters. Specifically, in the lower-right corner, tasks sharing the ”left-arm pick” primitive—namely DUR-CleanTable, DUR-StackBowls, and DUR-SweepTrash—are grouped closely together. This suggests the model successfully encodes the shared underlying semantics of the grasping motion. Conversely, the model effectively isolates distinct behaviors. Observing the upper region of the plot, a cluster of brown points forms a distinct island separate from other task embeddings. This cluster corresponds to the sweeping and translational motions unique to the DUR-SweepTrash task. This separation demonstrates that UVMC can effectively disentangle common dynamical patterns (e.g., picking) from task-specific nuances (e.g., sweeping). 

**Cross-Embodiment Alignment.** A central hypothesis of our approach is that the learned representation should be embodiment-agnostic. Figure 15 substantiates this by illustrating the embedding space for identical tasks executed by morphologically distinct robots. Notably, the embeddings for DFR-CleanTable (represented in red) and DUR-CleanTable (represented in yellow) share a common support and overlap significantly within the latent manifold. Despite the kinematic and appearance discrepancies between the Franka and UR robots, UVMC projects their state-action trajectories onto a unified manifold. This result indicates that the model has learned a robust, embodiment-invariant representation that prioritizes high-level task semantics over low-level proprioceptive differences. 

28 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

_Table 18._ Task-to-task Nearest-neighbor similarity statistics 

|Exp.|The mode of similarity distribution|Average|
|---|---|---|
|SE.ST. (Task1.MC vs Task1.VC)|0.97|0.75|
|DE.ST. (Task1.MC vs Task2.VC)|0.82|0.67|
|SE.DT. (Task1.MC vs Task3.VC)|0.60|0.56|
|DE.DT. (Task1.MC vs Task4.VC)|0.46|0.48|


_Figure 14._ Visualizing UVMC on 6 dual-arm UR tasks using t-SNE. 

# **I. Failure Case Analysis on Baseline Methods** 

We conducted a qualitative analysis of the rollout videos to investigate why baselines struggle compared to XR-1. We categorize the observed failures into two primary modes: 

**Optimization Collapse and Conflicting Gradients** . In some distinct scenarios, baselines fail to capture the correct motion trend entirely. The models exhibit ”hesitation” or revert to the mean pose, suggesting that the optimization objective is torn between conflicting gradients from different tasks. Example: In the ‘DFR-CloseToolbox‘ task, the _π_ 0 policy initiates a downward movement with the right arm but immediately retracts to the initial position. The robot appears indecisive and fails to commit to the task trajectory. We attribute this to the difficulty of fitting a single policy distribution to 20 diverse tasks without task-distinguishing representations. 

**Precision Deficiency and Coordination Failure** . The most common failure mode involves the robot attempting the correct action but failing in execution precision or bimanual coordination. Example: In the ‘DUR-HangCupHolder‘ task, GR00T-N1.5 successfully grasps the cup with the right arm. However, it drops the cup during the handover to the left arm. This indicates that while the model learns the general policy distribution, it lacks the fine-grained control and temporal consistency required for complex, multi-stage manipulation. 

XR-1 addresses these issues through the Unified Vision-Motion Condition (UVMC) introduced in Stage 1. The UVMC serves as a compact representation of visual dynamics and motion patterns. By conditioning the policy on UVMC, XR-1 can explicitly distinguish between different task modes, thereby reducing gradient conflicts during multi-task optimization. As 

29 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 15._ Visualizing UVMC across different embodiments (Dual-Arm Franka and Dual-Arm UR) using t-SNE. 

an intermediate feature supervision signal, UVMC guides the model to generate smoother and more physically consistent actions. This additional supervision is critical for tasks requiring high precision (e.g., dual-arm handover), preventing the coordination failures observed in baselines like GR00T. 

# **J. Failure Case Analysis on XR-1** 

**Precision Deficiency** . The most common failure mode involves the robot attempting the correct action but failing in execution precision or bimanual coordination. Example: In the ‘TK2-CollectScrews‘ task, the robot may fail to grasp a tiny screw or drop it mid-motion due to slight localization errors. This reflects the inherent difficulty of learning precise bimanual coordination for dexterous manipulation tasks. 

# **K. Representative Tasks** 

As illustrated in Figure 18, we select a set of representative tasks from real-world experiments to provide detailed descriptions of the evaluation scenarios. These tasks are designed to cover a broad spectrum of challenges, including bimanual collaboration, dexterous manipulation, fluid/deformable object handling, contact-rich interactions, dynamic environments, and long-horizon manipulation. Together, they demonstrate the versatility and robustness of **XR-1** across diverse manipulation settings. 

- **Bimanual Collaboration:** _DUR-TransCupHolder_ . This task involves a coordinated bimanual operation: the right arm initially grasps a cup, performs an aerial handover to the left arm, which subsequently places the cup into a cup rack. 

- **Dexterous Manipulation:** _DUR-CloseDoorKnob_ . The robot performs a dexterous operation to close and lock the control box door. The right arm first manipulates the door to a closed position. Subsequently, the left arm rotates the door handle by 90 degrees and presses it inward to engage the locking mechanism. 

- **Fluid Object Handling:** _SUR-PourTubeBeaker_ . The task consists of three phases: removing a test tube from the rack, pouring its liquid into a measuring cup, and returning the test tube to the rack. 

30 

### **XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 16._ Failure cases of baseline methods. 


_Figure 17._ Failure Cases of XR-1. 

- **Deformable Object Handling:** _DFR-HangTowelRack_ . The robot performs a bimanual manipulation task involving deformable object handling: the right arm first picks up a towel from a surface and transfers it to the left arm via an aerial handover; the left arm then manipulates the towel to drape it over a towel rack, completing the hanging motion. 

- **Contact-Rich Interactions:** _DFR-SweepRubbish_ . A dual-arm cleaning task is executed where the right arm operates a broom and the left arm stabilizes a dustpan. The robot systematically sweeps food remnants and a crumpled paper ball into the dustpan, followed by transporting and emptying the dustpan into a waste bin after each collection. 

- **Dynamic Environments:** _DUR-TransButtons_ . The robot’s left arm loads colored button workpieces onto a moving conveyor belt, while the right arm autonomously identifies each part’s color upon arrival and places it into the respective color-matched container. 

- **Long-Horizon Manipulation:** _AGX-StoreButton_ . This task entails a sequential dual-arm interaction: the left arm opens a drawer and holds it open, enabling the right arm to place a button workpiece inside; the left arm then closes the drawer after object deposition. 

## **K.1. Dataset for Evaluation** 

The dataset is primarily employed for the final fine-tuning stage of XR-1, and for training and evaluation of multiple baselines on this benchmark. 

31 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 


_Figure 18._ Diverse task settings in evaluation: bimanual collaboration, dexterous manipulation, deformable object handling, contact-rich interactions, dynamic environments, and long-horizon tasks. 

32 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

_Table 19._ The tasks summary of our real-world experiments. 

|#|Task|Tr<br>Num.|ajectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|||||**Dual-Arm UR5e**||
|T1|DUR-<br>FindTapeBasket|160|155|Find the packaging tape and put it into<br>the other basket||
|T2|DUR-<br>MoveCupMilk|198|149|Place the cup in the middle of the table<br>and pick up the milk and place it next to<br>the cup.||
|T3|DUR-StackBowls|158|147|Put the blue bowl in the middle of the<br>table and stack the green bowl on top of<br>it||
|T4|DUR-SweepTrash|192|293|Sweep up the rubbish and take out the<br>trash||
|T5|DUR-<br>TransCupHolder|167|170|Pick up the cup with the right arm, hand<br>it over to the left arm, and hang it on the<br>holder with the left arm||
|T6|DUR-StackCubes|158|153|Put the blue cube in the middle of the<br>desk and stack it on top of the other blue<br>cube||
|T7|DUR-<br>HangCupHolder|167|223|Hang the cup on the holder||
|T8|DUR-StackBrake|200|81|Use the left arm to place Brake Pad Type<br>A in the middle, then use the right arm to<br>pick up Brake Pad Type B and stack it on<br>top of Brake Pad Type A||
|T9|DUR-<br>SweepRubbish|185|157|Sweep up the rubbish||


Continued on next page 

33 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T10|DUR-PressButton|183|121|Pick up and place the green button, then<br>press it||
|T11|DUR-<br>PickPlaceTape|192|111|Pick up and place the adhesive tape||
|T12|DUR-<br>CloseToolbox|114|190|Use both arms to close the toolbox||
|T13|DUR-<br>AssembleValve|253|108|Assemble the valve||
|T14|DUR-<br>FlipTennisTube|123|127|Put the tennis tube upright||
|T15|DUR-PlaceTools|198|102|Use the left arm to place the screwdriver<br>on the left side of the toolbox, and use the<br>right arm to place the wrench on the right<br>side of the toolbox||
|T16|DUR-<br>CloseDoorKnob|201|147|The right arm closes the distribution box<br>door, and the left arm turns and presses<br>the closing knob||
|T17|DUR-<br>TakeBasketTea|198|147|The right arm places the shopping basket<br>in the middle, while the left arm takes tea<br>drinks from the shelf and puts them inside||
|T18|DUR-PickToolbox|200|117|Use both arms to pick up the toolbox||
|T19|DUR-<br>OpenTrashBin|28|45|Open the trash bin||


Continued on next page 

34 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T20|DUR-<br>TransButtons|146|184|Transport the buttons from left to right<br>and place them in the corresponding<br>plates||
|T21|DUR-CleanTable|197|183|Move the buttons from left to right and<br>place them on the corresponding plates||
|||||**Tien Kung 2.0**||
|T1|TK2-PressButton|291|292|The left arm picks up the green button and<br>places it in the middle, while the right arm<br>presses it||
|T2|TK2-<br>AssembleValve|162|382|Assemble the valve||
|T3|TK2-StackBrake|178|261|Use the left arm to place Brake Pad Type<br>A in the middle, and use the right arm to<br>pick up Brake Pad Type B and stack it on<br>top of Brake Pad Type A||
|T4|TK2-PlaceCircuit|209|359|The left arm picks up the circuit breaker<br>from the red tray and places it in the mid-<br>dle of the table. Then the right arm picks<br>up the circuit breaker and puts it into the<br>blue tray on the right.||
|T5|TK2-<br>PressControlBox|256|292|The left arm places the control box in the<br>middle, while the right arm presses the<br>red emergency stop button on it||
|T6|TK2-<br>CloseDoorKnob|197|271|The right arm closes the door of the dis-<br>tribution box, and the left arm rotates and<br>presses the closing knob.||
|T7|TK2-GatherTools|177|452|Use the left arm to place the screwdriver<br>on the left side of the toolbox, and use the<br>right arm to place the wrench on the right<br>side||
|T8|TK2-CloseLaptop|189|186|Close the laptop||


Continued on next page 

35 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T9|TK2-OpenPotLid|190|304|Open the blue pot lid||
|T10|TK2-<br>HangCupHolder|144|277|Hang the oval-bottom cup on the holder||
|T11|TK2-<br>MoveCupSauce|129|312|Move the blue cup, pick up the yellow<br>sauce bottle, and pour it into the blue cup||
|T12|TK2-StackCup|161|291|Stack the blue cups||
|T13|TK2-<br>InsertToyBlock|152|521|Insert the blue toy into the square-bottom<br>slot of the grey block||
|T14|TK2-<br>FindCapacitor|232|370|The left arm picks up the red electrolytic<br>capacitor from the blue tray and places it<br>in the middle of the table. Then the right<br>arm picks it up and puts it into the red<br>tray on the right||
|T15|TK2-<br>MoveMilkMug|279|284|Pick up and place the milk, then move the<br>white mug||
|T16|TK2-PourGearOil|152|503|The left arm places the gear on the mid-<br>dle metal tray, while the right arm pours<br>lubricating oil on it||
|T17|TK2-<br>PlaceBiscuitBox|133|447|Pick up the biscuit box from the blue bas-<br>ket with the right arm and place it in the<br>middle of the table. Then, use the left arm<br>to place it on the middle shelf of the black<br>rack||
|T18|TK2-<br>CollectScrews|192|620|The right arm places the two long screws<br>into the slot at the very right end of the<br>storage box, while the left arm places the<br>two short screws into the slot at the very<br>left end of the storage box||


Continued on next page 

36 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T19|TK2-MoveTape|182|547|Pick up and place the rattan basket||
|T20|TK2-<br>TakeBasketTea|197|497|The right arm places the shopping basket<br>in the middle, while the left arm takes tea<br>drinks from the shelf and puts them inside||
|T21|TK2-TakeTape|297|357|Pick up and place the adhesive tape||
|T22|TK2-<br>SweepRubbish|239|421|Sweep up the rubbish||
|||||**Tien Kung 1.0**||
|T1|TK1-FindTape|446|793|Find the packaging tape, pick it up, and<br>place it into another basket||
|T2|TK1-StackBowls|260|497|Put the blue bowl in the middle of the<br>table, then stack the green bowl on top of<br>it||
|T3|TK1-CloseDrawer|231|223|Slide the drawer closed||
|T4|TK1-<br>FlipTennisTube|300|535|Put the tennis tube upright||
|T5|TK1-<br>PressCookerButton|98|187|Press the rice cooker’s off button||
|T6|TK1-<br>MoveChopstickCup|274|574|Move the blue cup to the middle, then<br>place one chopstick from the bamboo<br>holder into it||


Continued on next page 

37 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T7|TK1-StackCubes|200|520|Stack the two blue cubes||
|T8|TK1-StackCups|200|487|Move the blue cup and stack it with the<br>other blue cup||
|T9|TK1-StackPlates|200|449|Place the pink plate into the beige plate<br>in the middle, then stack the blue plate on<br>top of the pink plate||
|T10|TK1-<br>PickWipeTowel|222|643|Pick up a towel and wipe the water with<br>it||
|T11|TK1-HangTowel|242|620|Pick up the towel with the right arm, hand<br>it over to the left arm, and hang it on the<br>rack with the left arm||
|T12|TK1-OpenPotLid|104|486|Open the pot lid||
|T13|TK1-OpenOven|21|228|Open the oven||
|T14|TK1-PackEggBox|192|315|Put the egg into the box and close the lid||
|T15|TK1-CloseLaptop|174|188|Close the laptop screen||
|T16|TK1-InserToaster|174|254|Insert the bread into the toaster||
|T17|TK1-FlipCup|153|578|Flip the cup upright||


Continued on next page 

38 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T18|TK1-<br>PlaceFlipButton|125|616|Pick up the button with the right arm and<br>place it in the middle. Then use the left<br>arm to flip the button upright||
|T19|TK1-<br>OpenTrashBin|177|206|Open the trash bin||
|T20|TK1-<br>PressMachine|181|213|Press down the bread machine with the<br>right arm||
|||||**Dual-Arm Franka**||
|T1|DFR-<br>MoveCupMilk|293|254|Place the cup in the middle of the table,<br>then pick up the milk and put it next to<br>the cup||
|T2|DFR-StackBowls|298|245|Put the blue bowl in the middle of the<br>table and stack the green bowl on top of<br>it||
|T3|DFR-SweepTrash|248|350|Sweep up the rubbish and take out the<br>trash||
|T4|DFR-TransferCup|244|196|Pick up the cup with the right arm, hand<br>it over to the left arm, and hang it on the<br>holder with the left arm||
|T5|DFR-<br>MoveChopstick|277|299|The left arm moves the blue cup from the<br>left side of the robot to the middle, while<br>the right arm takes a chopstick from the<br>bamboo holder on the right side and puts<br>it into the blue cup||
|T6|DFR-StackCubes|245|166|Put the blue cube in the middle of the<br>desk and stack it on top of the other blue<br>one||
|T7|DFR-StackPlates|360|230|Use the left arm to place the pink plate<br>into the beige plate in the middle, then<br>use the right arm to stack the blue plate<br>on top of the pink plate||


Continued on next page 

39 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T8|DFR-CleanTable|284|201|Put the trash into the trash can, and put<br>the items back in the box||
|T9|DFR-<br>HangCupHolder|206|199|Hang the cup on the cup holder||
|T10|DFR-<br>HangTowelRack|232|195|Pick up the towel with the right arm, hand<br>it over to the left arm, and hang it on the<br>rack with the left arm||
|T11|DFR-<br>FindTapeBox|194|245|Find the packaging tape and put it into<br>the other box||
|T12|DFR-<br>PickButtonPress|200|206|The left arm picks up the green button and<br>places it in the middle, while the right arm<br>presses it||
|T13|DFR-<br>SweepRubbish|196|288|Sweep up the rubbish||
|T14|DFR-<br>CloseToolbox|201|220|Use both arms to close the toolbox||
|T15|DFR-<br>CollectBasketTea|200|186|The right arm places the shopping basket<br>in the middle, while the left arm takes tea<br>drinks from the shelf and puts them inside||
|T16|DFR-PlaceTools|199|159|Use the right arm to place the wrench on<br>the right side of the toolbox, and use the<br>left arm to place the screwdriver on the<br>left side||
|T17|DFR-GetBlocks|94|255|The right arm grabs the storage box and<br>opens the lid, while the left arm places<br>the red building blocks inside, ensuring<br>they do not fall off||


Continued on next page 

40 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T18|DFR-<br>PlaceRagWipe|196|301|Use the right arm to place the rag in the<br>middle of the table, and use the left arm to<br>wipe the remaining liquid on the middle<br>of the table with the rag||
|T19|DFR-<br>OpenToolbox|199|244|Use both arms to open the toolbox||
|T20|DFR-PlaceScrews|189|301|The right arm places the two long screws<br>into the slot at the very right end of the<br>storage box, while the left arm places the<br>two short screws into the slot at the very<br>left end of the storage box||
|||||**AgileX Cobot Magic V2.0**||
|T1|AGX-<br>OpenDrawerButton|272|1418|Slide open the drawer and place the yel-<br>low button inside||
|T2|AGX-<br>MoveButtonDrawer|387|1612|Place the yellow button in the drawer and<br>close it||
|T3|AGX-StackBoxes|169|1514|Put the left box in the middle, then stack<br>the right box on top of it||
|T4|AGX-<br>FindTapeBox|182|1058|Find the packaging tape and put it into<br>the other box||
|T5|AGX-<br>SweepRubbish|112|2370|Sweep up the rubbish||
|T6|AGX-<br>ArrangeValves|194|1411|Arrange the valves in a row||


Continued on next page 

41 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T7|AGX-<br>HangScissors|48|3124|Hang the scissors on the holder||
|T8|AGX-PlaceButton|184|1794|Take the blue tray and place a button on<br>it||
|T9|AGX-<br>CloseToolbox|184|2003|Use both arms to close the toolbox||
|T10|AGX-<br>GatherScrews|152|2918|The right arm places the two long screws<br>into the slot at the very right end of the<br>storage box, while the left arm places the<br>two short screws into the slot at the very<br>left end of the storage box||
|T11|AGX-FindCircuit|476|2880|The left arm picks up the circuit breaker<br>from the red tray and places it in the mid-<br>dle of the table. Then the right arm picks<br>up the circuit breaker and puts it into the<br>blue tray on the right||
|T12|AGX-<br>PlaceBiscuitBox|188|1983|Pick up the biscuit box from the blue bas-<br>ket with the right arm and place it in the<br>middle of the table. Then, use the left arm<br>to place it on the middle shelf of the black<br>rack||
|T13|AGX-<br>CollectBasketTea|190|3078|The right arm places the shopping basket<br>in the middle, while the left arm takes tea<br>drinks from the shelf and puts them inside||
|T14|AGX-<br>PlaceScrewdriver|177|3079|The right arm picks up the Phillips screw-<br>driver and places it in the middle of the<br>table. Then, the left arm picks it up again<br>and puts it into the groove in the toolbox||
|T15|AGX-PourGearOil|192|3144|The left arm takes the gear and places it<br>on the middle metal tray, and the right<br>arm pours lubricating oil on the gear||


Continued on next page 

42 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T16|AGX-<br>StackBrakePads|188|1650|Use the left arm to place Brake Pad Type<br>A in the middle, and use the right arm to<br>pick up Brake Pad Type B and stack it on<br>top of Brake Pad Type A||
|T17|AGX-<br>MeshStackCup|117|1765|Place the mesh and stack the cup on it||
|T18|AGX-PourWine|162|1644|Pour the wine with the right arm and<br>place the cup on the tray with the left<br>arm||
|T19|AGX-<br>HangWipeRag|199|2257|Use the right arm to place the rag in the<br>middle of the table, and use the left arm<br>to wipe the remaining liquid with it||
|T20|AGX-StackBowls|185|1314|Stack the blue bowl on top of the green<br>bowl||
|||||**Single-Arm UR5e**||
|T1|SUR-FindTape|134|104|Find the packaging tape and put it into<br>the other basket||
|T2|SUR-<br>MoveMilkCup|292|116|Pick up the milk and place it next to the<br>cup||
|T3|SUR-StackBowls|300|118|Stack the blue bowl on top of the green<br>bowl||
|T4|SUR-OpenDrawer|212|168|Slide open the drawer||


Continued on next page 

43 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T5|SUR-CloseDrawer|190|191|Slide the drawer closed||
|T6|SUR-<br>InsertToyBlock|150|198|Insert the blue toy into the square-bottom<br>slot of the grey block||
|T7|SUR-<br>PlaceChopstick|297|109|Place one chopstick from the bamboo<br>chopstick holder into the blue cup||
|T8|SUR-StackCubes|308|92|Stack the two blue cubes on top of each<br>other||
|T9|SUR-StackCup|284|192|Stack the cups||
|T10|SUR-StackPlates|291|194|Stack the plates in the middle||
|T11|SUR-SlideDrawer|56|181|Slide open the drawer||
|T12|SUR-<br>OpenUpperDrawer|182|132|Open the upper drawer||


Continued on next page 

44 

**XR-1: Towards Versatile Vision-Language-Action Models via Learning Unified Vision-Motion Representations** 

|#|Task|Tra<br>Num.|jectory<br>Avg. Len.|Task Instruction|Task Setting|
|---|---|---|---|---|---|
|T13|SUR-OpenOven|141|70|Open the oven||
|T14|SUR-PackEggBox|183|151|Put the egg into the box and close the lid||
|T15|SUR-CloseLaptop|196|107|Close the laptop screen||
|T16|SUR-InsertBread|193|156|Insert the bread into the toaster||
|T17|SUR-<br>AssembleValve|182|166|Assemble the valve||
|T18|SUR-<br>PourTubeBeaker|152|270|Pick up the test tube and pour water into<br>a 50 ml glass beaker||
|T19|SUR-PourGearOil|172|214|Take the gear and place it on the middle<br>metal tray, then pour lubricating oil on it||
|T20|SUR-<br>WipeHangRag|209|134|After using the rag to wipe the water in<br>the middle of the table, hang the rag on<br>the rag rack||


45 

