---
title: "Predicting What Matters: Robust Generalist Robot Policy Learning via Future Semantic Mask"
date: "2026"
venue: "ICML 2026"
url: https://proceedings.mlr.press/v306/lou26a.html
pdf: https://raw.githubusercontent.com/mlresearch/v306/main/assets/lou26a/lou26a.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://raw.githubusercontent.com/mlresearch/v306/main/assets/lou26a/lou26a.pdf)** / [論文ページ](https://proceedings.mlr.press/v306/lou26a.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Predicting What Matters: Robust Generalist Robot Policy Learning via Future Semantic Mask** 

**Yunfan Lou**<sup>* 1 2</sup> **Xiaowei Chi**<sup>* 3</sup> **Xiaojie Zhang**<sup>*</sup><sup>_†_2 4</sup> **Zezhong Qian**<sup>4</sup> **Chengxuan Li**<sup>4</sup> **Rongyu Zhang** _†_ 5 6 **Yaoxu Lyu**<sup>2 4</sup> **Guoyu Song**<sup>5</sup> **Chuyao Fu**<sup>2</sup> **Haoxuan Xu**<sup>3</sup> **Pengwei Wang**<sup>2</sup> **Shanghang Zhang**<sup>�2 4</sup> 

## **Abstract** 

## **1. Introduction** 

World models derived from large-scale video generative pre-training have emerged as a promising paradigm for generalist robot policy learning. However, standard approaches often focus on high-fidelity RGB video prediction, this can result in overfitting to irrelevant factors, such as dynamic backgrounds and illumination changes. These distractions reduce the model’s ability to generalize, ultimately leading to unreliable and fragile control policies. To address this, we introduce the **Mask World Model (MWM)** , which leverages video diffusion architectures to predict the evolution of semantic masks instead of pixels. This shift imposes a geometric information bottleneck, forcing the model to capture essential physical dynamics and contact relations while filtering out visual noise. We seamlessly integrate this mask dynamics backbone with a diffusion-based policy head to enable robust end-to-end control. Extensive evaluations demonstrate the superiority of MWM on the LIBERO and RLBench simulation benchmarks, significantly outperforming the state-of-the-art RGB-based world models. Furthermore, real-world experiments and robustness evaluation (via random token pruning) reveal that MWM exhibits superior generalization capabilities and robust resilience to texture information loss. 

*Equal contribution _†_ Project leaders � Corresponding author 1National University of Singapore, Singapore 2Beijing Academy of Artificial Intelligence, Beijing, China<sup>3</sup> The Hong Kong University of Science and Technology, Hong Kong, China<sup>4</sup> State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University<sup>5</sup> Peking University, Beijing, China<sup>6</sup> Nanjing University, Nanjing, China. Correspondence to: Shanghang Zhang _<_ shanghang@pku.edu.cn _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

Learning generalist robot manipulation policies that remain reliable under real-world visual variability remains a central challenge. A promising direction is to learn a predictive world model and use its internal features to guide action generation (Hu et al., 2025; Assran et al., 2025; Ha & Schmidhuber, 2018; Hafner et al., 2020; Chi et al., 2025c), offering long-horizon foresight and improved data efficiency (Pai et al., 2025). However, most video world models are optimized to predict RGB pixels, and this photometric objective is often misaligned with control. 

RGB frames contain substantial nuisance variation, including texture, lighting, reflections, and dynamic backgrounds, which is weakly related to action selection (Wang et al., 2023). Pixel prediction compels a model to allocate capacity to these factors and to entangle appearance with dynamics, treating changes in illumination or background as comparable to contact-relevant motion (Grooten et al., 2023; Wang et al., 2025). In closed-loop execution, this misallocation becomes more damaging: small appearance-driven errors can compound over time, causing predictive drift and brittle policies under modest distribution shifts (Liu et al., 2025). 

We argue that robust control benefits from predicting decision-relevant dynamics rather than photometric realism (Chi et al., 2024; Ze et al., 2024). To this end, we introduce the MWM (Figure 1), which shifts the prediction space from future RGB frames to future semantic masks. Semantic masks impose a geometric bottleneck that preserves object identity, spatial layout, and interaction-relevant structure while discarding redundant appearance (Seo et al., 2023; Berg et al., 2025). Crucially, MWM does not require an external segmentation model at inference: semantic labels are used only offline during training, while deployment uses only raw multi-view RGB (Zhu et al., 2025). 

The training pipeline of the proposed MWM adopts a twostage strategy, as illustrated in Figure 1. First, we learn a mask-centric predictive model by forecasting future semantic masks with a conditional diffusion objective, so the predictor models the evolution of semantic structure instead of reconstructing pixels. Second, we train a diffusion policy 

1 

**Mask World Model** 


_Figure 1._ **MWM overview.** MWM learns a mask-centric predictive world model from semantic supervision during training, but runs purely on raw multi-view RGB at test time. Training proceeds in two stages: we first learn to forecast future semantic masks via conditional diffusion, then train a diffusion policy that conditions on mask-centric predictive features for action generation. This semantic bottleneck prioritizes decision-relevant geometry and interaction dynamics over photometric realism. 

that conditions on intermediate features produced by the mask-centric model to generate actions. This coupling is essential: _the policy is explicitly optimized to extract controlutility from mask-centric predictions, rather than treating masks as an auxiliary visualization._ Empirically, we find that the semantic bottleneck improves both representation quality and control. This is because mask-centric predictive features focus on capturing motion and contact geometry while filtering out irrelevant photometric variations, providing stronger and more reliable action guidance compared to RGB-centric features (He et al., 2021). 

Extensive experiments demonstrate that MWM yields consistent gains across multiple domains with 98.3% average success rate on LIBERO, 68.3% on RLBench, and 67.5% average success on a real Franka robot across four tasks, substantially outperforming strong RGB-centric baselines. In addition, we observe improved robustness and generalization under controlled real-robot appearance shifts (background, lighting, object color), as well as under compute/observability stress tests such as random visual token pruning. Our main contributions can be concluded as: 

1. We propose **Mask World Model** , a world model that forecasts future semantic masks internally and runs purely on raw RGB at inference, using semantic supervision only during training to eliminate reliance on external segmenters at deployment. 

2. We design a **mask-guided diffusion policy** that conditions action generation on mask-centric predictive 

features, and show that these representations provide stronger control utility than RGB-centric prediction by emphasizing dynamics-relevant structure. 

3. We investigate several approaches to extracting and utilizing mask information and observe that mask-centric designs consistently outperform future RGB prediction, which highlights that the performance gains primarily arise from the shift in representation and objectives, rather than reliance on a specific architectural design. 

## **2. Related Work** 

### **2.1. Video world models for robot policy learning** 

World models have long been used to learn compact predictive dynamics for control, often in latent spaces to avoid direct pixel prediction (e.g., Dreamer-style agents) (Hafner et al., 2024; 2025). More recently, diffusion/transformer video generators have been repurposed as predictive backbones for robotics and physical simulation (NVIDIA et al., 2025; Brooks et al., 2024), and some systems couple multiview video diffusion with action heads for manipulation (Liao et al., 2025; Chi et al., 2025b;a; Li et al., 2025c; Mi et al., 2026; Jia et al., 2026). Despite strong results, these methods typically optimize prediction in an appearancecentric space (RGB reconstruction or closely related latents), which encourages modeling nuisance variation (texture, lighting, background) and can entangle appearance with interaction dynamics. Concurrent diffusion worldmodel variants improve scalability or handle multi-modality 

2 

**Mask World Model** 

(Huang et al., 2025b; Shang et al., 2025; Bu et al., 2025; Qian et al., 2025; Li et al., 2025b), but their predictive targets remain primarily photometric. In contrast, MWM predicts future semantic mask dynamics, using semantic supervision only during training and requiring no external segmenter at test time. 

### **2.2. Vision-Language-Action models** 

Generalist Vision-Language-Action (VLA) policies leverage large pretrained vision-language representations to map instructions and observations to actions (Brohan et al., 2023; Team et al., 2024; Zhang et al., 2025b;a). When tasks require precise spatial relations and contact-sensitive control, policies can benefit from representations that more explicitly expose object state and interaction geometry and are less coupled to photometric variation. A growing line of work injects semantics to reduce perceptual redundancy or improve grounding, e.g., instruction-aligned token pruning (Li et al., 2025a), auxiliary reconstruction to emphasize task-relevant regions (Song et al., 2025), or externally produced grounding masks as intermediate cues (Huang et al., 2025a). MWM differs in both mechanism and deployment: rather than using semantics as an input cue on the current observation, it provides semantic lookahead by learning predictive mask dynamics and trains a policy head to consume mask-centric predictive features for action generation, while retaining a pure-RGB interface at test time. 

### **2.3. Structured representations under masking** 

Object-centric representations and scene factorization aim to discover structured entities and dynamics (Locatello et al., 2020; Burgess et al., 2019; Greff et al., 2020; Engelcke et al., 2022), while masked modeling and token dropping are widely used to learn robust and efficient visual representations (He et al., 2021; Tong et al., 2022). These lines support the broader intuition that compact, structure-biased representations can improve stability over raw pixels. MWM instantiates this idea for manipulation by making semantic structure the predictive space of a diffusion world model and coupling it to a diffusion policy head. We further adopt random visual token pruning as an evaluation stress test (not a modeling contribution) to probe control robustness under severe partial observability. 

## **3. Method** 

We present the **MWM** , a mask-centric world-model for language-conditioned manipulation. As shown in Figure 2, MWM consists of a mask-dynamics backbone and a diffusion policy head. Training follows two stages: (i) pretrain the backbone to forecast future semantic mask latents using offline semantic supervision, and (ii) train the action diffusion head for control, where gradients from _L_ act also 

update the backbone to make predictive features maximally action-relevant. At test time, MWM takes only multi-view RGB as input without external segmentation model. 

### **3.1. Motivation: Geometric Information Bottleneck** 

Robust manipulation relies on object identity, spatial layout, and contact-relevant dynamics, while RGB factors such as texture, illumination, and background often act as nuisance variables. By predicting future semantic masks, MWM introduces a geometric bottleneck that preserves decisioncritical structure while filtering out irrelevant photometric variation. 

### **3.2. Problem Setup** 

At time _t_ , the agent receives multi-view RGB observations **o** _t_ = _{_ **o**<sup>(</sup> _t_<sup>_v_)</sup><sup>_}V_</sup> _v_ =1<sup>and a language instruction</sup><sup>**p**, and outputs</sup> a continuous action **a** _t_ (end-effector motion and gripper command). We learn a closed-loop policy robust to appearance variations (e.g., background, lighting, and object color), where such photometric changes should not dominate learned dynamics. 

### **3.3. Mask Dynamics Backbone** 

**Offline semantic supervision; RGB-only at deployment.** During training, each frame is paired with a semantic mask **m** _t ∈{_ 0 _,_ 1 _}_<sup>_H×W ×C_</sup> for task-relevant entities (robot arm/gripper and manipulated objects). These masks are used _only_ to supervise the backbone predictor; at deployment, the model takes only raw RGB as input. 

**Discrete-to-continuous mask encoding with a shared VAE.** Semantic masks are discrete, while video diffusion backbones typically operate on continuous latents. MWM reuses the _same pretrained video VAE_ (Kingma & Welling, 2022) for RGB and mask targets by rendering masks into an RGB-compatible image **m** ˜ _t ∈_ [0 _,_ 1]<sup>_H×W ×_3</sup> using a fixed color palette (each semantic region mapped to a distinct color). We then encode both RGB frames and rendered masks with the same encoder _E_ : 


This design avoids modifying the pretrained VAE and yields a consistent latent interface for context (RGB) and targets (masks). 

**Latent normalization, Interpolate and Stack.** Let **z** _∈_ R<sup>_T ×H′×W ′×D_</sup> denote VAE latents. We apply channel-wise normalization using VAE statistics: 


To obtain a fixed-length token sequence, we temporally resample (interpolate) latents to a canonical latent frame rate 

3 

**Mask World Model** 


_Figure 2._ **Mask World Model (MWM) architecture.** Given multi-view RGB memory frames and a language prompt, MWM encodes observations with a shared video VAE, then applies _Normalize & Interpolate & Stack_ to form a fixed-length latent token sequence. A DiT-style backbone with AdaIN timestep conditioning and text cross-attention processes these tokens for _N_ =28 transformer blocks. In Stage 1, a mask decoder supervises future mask latent prediction with _L_ mask. In Stage 2, an action diffusion head (action expert + action decoder) attends to the backbone predictive features via cross-attention and is trained with _L_ act only. 

and stack multi-view latents into a unified sequence before flattening into tokens. Concretely, for view _v_ we resample **z** ¯<sup>(</sup><sup>_v_)</sup> along time to **z** ˆ<sup>(</sup><sup>_v_)</sup> _∈_ R<sup>_T_ˆ</sup><sup>_×H′×W ′×D_</sup> , then stack over _v_ and flatten spatially into tokens for a transformer backbone. This step replaces the conventional pixel-space 3D patchification, enabling more stable training even with varying temporal subsampling rates and compression artifacts brought by the VAE module. 

**Conditional flow matching with fixed memory slots.** Given a memory window of RGB latents ˆ **z**<sup>_o_</sup> _t−n_ +1: _t_<sup>and target</sup> future mask latents **z** ˆ<sup>_m_</sup> _t_ +1: _t_ + _τ_<sup>,thebackbonelearnstogen-</sup> erate future mask latents conditioned on the memory and language. We use flow matching(Lipman et al., 2023) with a linear interpolation path between clean target latents and noise. Let **z** 0 be clean future mask latents and **z** 1 _∼N_ ( **0** _,_ **I** ). For _s ∈_ [0 _,_ 1], 


Crucially, conditioning enters through the _velocity field_ , not the path: the transformer predicts **v** _θ_ ( **z** _s, s,_ **c** _t_ ) where **c** _t_ encodes the RGB memory and text instruction and is injected via cross-attention. The loss is 


**Conditioning mask (memory clean; future denoised).** We represent the latent sequence as [ˆ **z**<sup>_o_</sup> _t−n_ +1: _t_<sup>_,_</sup><sup>**z**ˆ</sup><sup>_m_</sup> _t_ +1: _t_ + _τ_<sup>]</sup> 

and use a binary mask **b** _∈{_ 0 _,_ 1 _}_<sup>_n_+</sup><sup>_τ_</sup> indicating memory slots. Memory slots are treated as clean inputs by forcing their diffusion time to zero, and the mask loss is applied only on future slots. Specifically, we define ˜ **z** _s_ as the noised version of the future latent at diffusion level _s_ . A compact way to write the noising operation is: 


**3D RoPE with interpolation scale (compression-aware).** We apply 3D RoPE(Ma et al., 2024) over ( _t, h, w_ ) token coordinates. Because tokens live in VAE-compressed latent grids, we use an interpolation scale **_γ_** = ( _γt, γh, γw_ ) derived from the VAE temporal/spatial compression to keep positional phases consistent across resolutions: 


**Timestep conditioning via AdaIN-style modulation.** Instead of standard adaptive normalization, MWM applies timestep-dependent scale and shift modulation after normalization(Huang & Belongie, 2017). 

4 

**Mask World Model** 

For a hidden activation **x** , we first normalize using RMSNorm, then modulate: 


Here, _α_ ( _s_ ) and _β_ ( _s_ ) are functions of the timestep embedding _s_ , learned through a combination of a trainable scaleshift table and timestep projection. The operator _⊙_ represents element-wise multiplication. 

This design enhances stability when operating on normalized VAE latents by effectively handling their inherent variability, while simultaneously preserving accurate timestepdependent conditioning for improved performance. 

**Predictive feature bank for control.** During mask forecasting, we cache the hidden states from transformer blocks to form a multi-level predictive feature bank **H** _t_ = _{_ **h**<sup>(1)</sup> _t_<sup>_, . . . ,_</sup><sup>**h**(</sup> _t_<sup>_L_)</sup> _}_ . These features preserve view-/space/time-indexed structure and are later exposed to the policy head as cross-attention keys/values. We use all blocks by default; aggregation details are deferred to the appendix. 

**Multi-view handling (minimal reproducible description).** Multi-view tokens are processed mostly with shared spatiotemporal self-attention, and we periodically apply crossview mixing layers so that information can flow between views while retaining view-specific structure. The exact cross-view frequency is reported in the appendix. 

latents using the flow matching objective ( _L_ mask) defined in Eq. (4), with memory slots fixed by Eq. (5). A memory window of _n_ =4 RGB frames is used to predict _τ_ =5 future latent frames, covering a total of 9 video frames. To enhance robustness, caption dropout ( _p_ =0 _._ 06) and slight noise injection (0 _._ 1) are applied to the conditioning frames. 

**Stage 2: policy learning (no video/mask loss).** Starting from the Stage-1 checkpoint, we optimize the model end-toend using only the action loss, _L_ stage2 = _L_ act. The VAE is frozen, while the DiT backbone and action expert are jointly trained to denoise action chunks ( _Ha_ =36) from backbone features. The action space is 15-dimensional, including a 7-DoF pose, a 1-DoF gripper command, and a 7-DoF state vector. No mask or video reconstruction loss is used in this stage; instead, gradients from _L_ act update the backbone so that its predictive features become more control-aligned. We keep the Stage-1 optimizer settings, but use a lower learning rate and disable text dropout. The appendix compares this design against adding an auxiliary mask loss in Stage 2 and against training from scratch without Stage-1 initialization. 

**Inference.** During deployment, Receding Horizon Control (RHC) is used to predict a 36-step action chunk via 10-step Euler discrete diffusion sampling. After generating the action chunk, the first action is executed, and the model replans at the next timestep, ensuring adaptive and responsive control. 

## **4. Experiments** 

### **3.4. Mask-Guided Diffusion Policy** 

**Action-state tokens.** The policy predicts actions in short chunks. At each step, we form an input vector **u** _t_ = [ **a** _t,_ **s** _t_ ] by concatenating the action parameterization with a lowdimensional proprioceptive state **s** _t_ . **u** _t_ is linearly projected into action tokens before entering the action transformer. 

**Diffusion objective in action space.** We train the policy as a conditional denoiser in action space. Given an action chunk **u** , sample _σ_ and add noise **u** ˜ = **u** + _σ_ **_ϵ_** with **_ϵ_** _∼N_ ( **0** _,_ **I** ). The denoiser _ϕξ_ is conditioned on **H** _t_ (and optionally text embeddings) and trained with a weighted score-matching objective: 


At test time, we sample an action chunk by iterative denoising and execute in a receding-horizon closed loop. 

### **3.5. Two-Stage Training Protocol** 

**Stage 1: mask dynamics pretraining.** In the first stage, the backbone is trained to predict future semantic mask 

### **4.1. Simulation Experiments** 

**Benchmarks.** We evaluate on two standard languageconditioned manipulation benchmarks. LIBERO(Liu et al., 2023) consists of 130 simulated manipulation tasks with templated language instructions; following common practice, we report results on four evaluation suites: LIBEROSpatial, LIBERO-Object, and LIBERO-Goal (10 tasks each), plus LIBERO-10, a 10-task long-horizon subset derived from LIBERO-100 (Table 1). RLBench(James et al., 2019) contains 100 tabletop manipulation tasks with standardized multi-view observations and natural-language goals; following prior work, we report success rates (SR) on six representative tasks (Table 2). On RLBench, we run 20 evaluation episodes per task with randomized seeds/initializations. 

**Baselines and our instantiations.** On LIBERO, we compare against representative RGB-centric generalist policies and world-model pipelines: OpenVLA(Kim et al., 2024), CogACT(Li et al., 2024), _π_ 0(Black et al., 2026), Cosmos+IDM, Cosmos+LatentIDM, and GE-ACT (Table 1). We additionally evaluate three mask-based instantiations introduced in Section 3 under the _same training data and_ 

5 

**Mask World Model** 

_Table 1._ LIBERO benchmark success rates (SR). For each suite, we select the checkpoint with the best validation performance and evaluate it over 500 episodes. Cell colors indicate camera setups: green for 3rd, yellow for 3rd+wrist, and red for our method. 

|Modality|Cameras|Method|Spatial|Object|Goal|Libero-10|Avg.|
|---|---|---|---|---|---|---|---|
||3rd|CogACT|0.972|0.980|0.902|0.888|0.936|
||3rd|OpenVLA|0.847|0.884|0.792|0.537|0.765|
|RGB|3rd|Cosmos w/ IDM|0.768|0.750|0.694|0.488|0.675|
||3rd|Cosmos w/ Latent IDM|0.948|0.992|0.892|0.842|0.919|
||3rd+wrist|_π_0|0.968|0.988|0.958|0.852|0.942|
||3rd+wrist|GE-ACT|0.982|0.976|0.958|0.944|0.965|
||3rd|MWM-C1|0.866|0.842|0.828|0.704|0.810|
|Mask|3rd|MWM-C2|0.948|0.988|0.922|0.812|0.918|
||3rd+wrist|**MWM (ours)**|**0.988**|**1.000**|**0.982**|**0.960**|**0.983**|


_recipe_ (detailed architectures are provided in Section C): 

- **MWM-C1** explicit future-mask decoding with an IDM 

- **MWM-C2** predictive latent features with an action diffusion head, without explicit mask decoding 

- **MWM** end-to-end mask world model with thirdperson + wrist-view inputs 

On RLBench, we compare to OpenVLA, CogACT, _π_ 0, FiSVLA, and GE-ACT. 

performance (0.965 _→_ 0.983 over GE-ACT) while remaining strong on LIBERO-10, approaching saturation on Spatial/Object/Goal. 

On RLBench (Table 2), MWM achieves 68.3% average SR, outperforming both the RGB world-model baseline GEACT (30.8%) and the stronger generalist baseline FiS-VLA (50.0%). The largest gains appear on tasks requiring precise object interaction and goal satisfaction (e.g., _Umbrella Out_ , _Frame off Hanger_ , _Wine at Rack_ ), supporting the claim that a semantic bottleneck improves robustness to appearance variation and strengthens decision-relevant generalization. 

**Evaluation protocol.** We select checkpoints using a held-out validation split to avoid test-time tuning. For LIBERO, we perform suite-wise selection and evaluate the selected checkpoint over 500 episodes with randomized seeds/initializations. For RLBench, we select the best validation checkpoint per task and evaluate it over 20 episodes. SR is the fraction of successful episodes. 

**Results and analysis.** As shown in Table 1, replacing RGB-centric prediction with future semantic structure improves performance consistently across all LIBERO suites. A direct comparison to RGB world-model counterparts shows that mask prediction is particularly beneficial when errors compound over longer horizons: MWM-C1 outperforms Cosmos w/ IDM in average SR (0.675 _→_ 0.810), with the largest gain on the long-horizon LIBERO-10 suite (0.488 _→_ 0.704), suggesting reduced rollout drift from appearance-related nuisance variables. Similarly, MWM-C2 improves over Cosmos w/ Latent IDM (0.873 _→_ 0.918), with clear gains on Goal and LIBERO-10, indicating that learning predictive representations in a semantic space yields more decision-relevant features. Notably, MWM-C2 also surpasses MWM-C1 (0.810 _→_ 0.918), consistent with the hypothesis that leveraging predictive latent features avoids error propagation introduced by explicitly decoded mask rollouts and a separately trained IDM. With additional wrist-view observations, MWM achieves the best overall 

### **4.2. Real-World Experiments** 

**Setup and tasks.** We evaluate on a Franka Emika Panda robot in a tabletop environment with two synchronized Intel RealSense D435i cameras: a fixed third-person view and an eye-in-hand wrist view. Detailed hardware specifications, sensor layout, and task visualizations are provided in Appendix B. We consider four language-conditioned manipulation tasks: (1) place bread and a hotdog into a basket, (2) open a drawer and place a pen inside, (3) pour water from a bottle into a bowl, and (4) place a book onto a shelf. In Table 4, Task1–Task4 correspond to tasks (1)–(4). 

**Data collection, mask annotation, and post-training.** For each task, we collect 50 task-specific demonstrations and perform per-task post-training across all methods to ensure consistent evaluation. To provide semantic supervision for MWM, we utilize RoboEngine (Yuan et al., 2025) to annotate the demonstration videos with pixel-wise semantic masks, covering the robot arm (including the gripper) and task-relevant objects. Notably, RoboEngine is employed only offline to generate training labels, while at test time, MWM operates directly on raw multi-view RGB observations, leveraging its learned mask-centric dynamics for control. For a fair comparison, both GE-ACT and _π_ 0 are post-trained using the same 50 demonstrations per task under identical training settings. 

6 

**Mask World Model** 

_Table 2._ RLBench success rates. We evaluate the best checkpoint selected on validation over 20 episodes with randomized seeds. 

|Method|Sweep to Dustpan|Phone on Base|Umbrella Out|Frame off Hanger|Wine at Rack|Water Plants|Avg.|
|---|---|---|---|---|---|---|---|
|CogACT|50.0%|50.0%|55.0%|45.0%|30.0%|25.0%|42.5%|
|FiS-VLA|55.0%|50.0%|50.0%|70.0%|55.0%|20.0%|50.0%|
|OpenVLA|50.0%|20.0%|35.0%|15.0%|10.0%|10.0%|23.3%|
|_π_0|30.0%|30.0%|30.0%|70.0%|10.0%|30.0%|33.3%|
|GE-ACT|10.0%|15.0%|40.0%|35.0%|40.0%|45.0%|30.8%|
|**MWM (ours)**|**55.0%**|**55.0%**|**85.0%**|**75.0%**|**90.0%**|**50.0%**|**68.3%**|


_Table 3._ Visual generalization on real-world tasks (Tasks (1)–(4)). Each entry is averaged over four tasks, with 20 trials per task per condition. We report in-distribution SR (SRID), SR under each appearance shift, and the summary metrics OOD-SR and Retain. 

|Method|SRID|BG|Light|Color|OOD-SR|Retain|
|---|---|---|---|---|---|---|
|GE-ACT|23.8%|3.8%|18.8%|15.0%|12.5%|0.53|
|_π_0|38.8%|13.8%|17.5%|26.3%|19.2%|0.49|
|**MWM (ours)**|**67.5%**|**27.5%**|**56.3%**|**42.5%**|**42.1%**|**0.62**|


_Table 4._ Real-world success rates (SR) on a Franka robot. Each method is post-trained per task using 50 demonstrations. 

|Method|Task1|Task2|Task3|Task4|Avg.|
|---|---|---|---|---|---|
|GE-ACT|35%|20%|10%|30%|23.8%|
|_π_0|50%|30%|5%|70%|38.8%|
|**MWM (ours)**|**75%**|**55%**|**60%**|**80%**|**67.5%**|


_Table 5._ Robustness to random token pruning on LIBERO (multiview). We report normalized pruning AUC (nPAUC; higher is better), averaged over pruning ratios _r ∈{_ 0 _._ 1 _, . . . ,_ 0 _._ 9 _}_ and the four LIBERO suites. Full detailed are provided in Section D. 

|Method|nPAUC_↑_|
|---|---|
|GE-ACT|0.629|
|**MWM (ours)**|**0.648**|


**Evaluation protocol.** After post-training, each method is evaluated for 20 real-robot trials per task with randomized initializations/seeds, and we report success rate (SR) as the fraction of successful executions. 

**Results and analysis.** Figure 3 visualizes representative real-robot rollouts, and Table 4 reports success rates. Table 4 shows that **MWM** consistently outperforms RGB-centric baselines across all four tasks, achieving 67.5% average SR versus 23.8% for GE-ACT and 38.8% for _π_ 0. The largest improvements appear on tasks with tighter goal constraints and higher sensitivity to compounding errors, such as drawer manipulation (Task2) and pouring (Task3), where RGB-based policies are more prone to appearance-driven drift. Overall, these results indicate that enforcing a semantic bottleneck together with multi-view observations yields more decision-relevant representations and improves robustness under real-world visual variability, even with only 50 demonstrations per task. 

### **4.3. Analysis: Robustness and Generalization** 

### 4.3.1. ROBUSTNESS TO RANDOM TOKEN PRUNING 

Token pruning/merging is a common way to reduce transformer inference cost by decreasing the number of visual tokens processed by attention. To evaluate robustness under compute-constrained inference, we randomly prune a fraction _r_ of _visual_ tokens (uniformly at random) _before_ feeding 

them into the Video-DiT backbone, while keeping language tokens unchanged. We sweep _r ∈ R_ = _{_ 0 _._ 1 _,_ 0 _._ 2 _, . . . ,_ 0 _._ 9 _}_ and report suite-wise success rates SR _s_ ( _r_ ) on LIBERO (500 episodes per suite, following the standard protocol). 

**Metric.** To summarize robustness with a single scalar (main paper), we measure the normalized pruning AUC (nPAUC), defined as the average success retention relative to the no-pruning performance: nPAUC = _|S||_ <u>1</u> _R|_ � _s∈S_ � _r∈R_ SRSR _ss_ (0)( _r_ <u>)</u><sup>,where</sup><sup>_S_denotesthefour</sup> LIBERO suites and SR _s_ (0) is the success rate without pruning. The full SR _s_ ( _r_ ) curves are reported in the appendix. 

**Results.** As shown in Table 5, **MWM** achieves a higher nPAUC than **GE-ACT** (0.648 vs. 0.629), indicating slightly better robustness to random token removal. We attribute the gain to the semantic bottleneck: mask-centric tokens concentrate capacity on object geometry and relations, making the policy less sensitive to missing visual tokens than RGB-centric representations. 

### 4.3.2. VISUAL GENERALIZATION 

**Protocol.** We evaluate visual generalization on the four real-world tasks in Section 4.2 (Tasks (1)–(4)). All policies are post-trained on 50 demonstrations per task under a _nominal_ visual condition, and are then evaluated _without any further adaptation_ under controlled appearance shifts. For 

7 

**Mask World Model** 


_Figure 3._ **Real-robot qualitative rollouts.** We visualize representative third-person executions for the four real-world tasks: bread+hotdog _→_ basket, pour water _→_ bowl, book _→_ shelf, and open drawer _→_ put pen. Each row shows frames ordered left-to-right. 

each task and each shift, we run 20 real-robot trials with randomized initializations and report success rate (SR). 

**Appearance shifts.** We consider three appearance factors that commonly induce failures under real-world visual variability: (i) **Background** (BG): replacing the tablecloth with unseen textures/patterns; (ii) **Lighting** (Light): changing illumination intensity (dimmer/brighter) while keeping geometry unchanged; (iii) **Object color** (Color): swapping task objects to unseen colors while preserving shape and size. These shifts primarily perturb visual nuisance variables (texture, illumination, and color) rather than task geometry. 

ruptive: GE-ACT nearly collapses (3.8% BG-SR), while MWM remains substantially more reliable (27.5%), suggesting reduced sensitivity to background texture cues. Under lighting and color perturbations, MWM maintains strong success (56.3% and 42.5%), indicating improved robustness to illumination and appearance changes. Finally, MWM also attains the best retention of in-distribution performance (0.62), supporting our hypothesis that enforcing a semantic bottleneck yields more decision-relevant representations under real-world visual variability. 

## **5. Conclusion** 

**Metrics.** Let SRID denote the in-distribution success rate under the nominal condition, and SR _c_ denote the success rate under shift condition _c ∈{_ BG _,_ LIGHT _,_ COLOR _}_ . We summarize the visual robustness using: OOD-SR = _|C_ <u>1</u> _|_ � _c∈C_<sup>SR</sup><sup>_c,_</sup> Retain =<sup><u>OOD</u></sup> SRID<sup>-SR.OOD-SR evaluates</sup> SR under appearance shifts, while Retain measures the preservation of nominal performance. 

**Results.** Table 3 summarizes OOD performance averaged over the four tasks (20 trials per task per condition; detailed per-task breakdowns are provided in Section E). MWM achieves the highest average performance under appearance shifts (OOD-SR 42.1%), outperforming GE-ACT (12.5%) and _π_ 0 (19.2%). Across shift types, BG is the most dis- 

We presented **Mask World Model (MWM)** , a mask-centric world-model framework that mitigates the mismatch between photometric RGB prediction and control utility by forecasting _future semantic masks_ . MWM uses semantic supervision only offline during training, while operating purely on raw multi-view RGB at test time, and couples maskcentric predictive features with a diffusion policy head for closed-loop control. Across LIBERO, RLBench, and realrobot evaluations, MWM consistently outperforms strong RGB-centric baselines, demonstrating improved robustness and generalization under real-world visual variability. These results suggest that semantic prediction provides a practical information bottleneck for learning more decision-relevant dynamics representations for generalist robot manipulation. 

8 

**Mask World Model** 

## **Acknowledgements** 

This work was supported by the National Natural Science Foundation of China (62476011) and (625B2090). 

## **Impact Statement** 

This work aims to improve the robustness and reliability of generalist robot manipulation policies by using semantic mask prediction to reduce sensitivity to irrelevant visual variations. The potential positive impacts include more reliable robotic systems in real-world environments and reduced dependence on brittle appearance-based prediction. At the same time, deploying generalist robots may raise broader societal concerns, including safety, labor displacement, and biases introduced by upstream perception or annotation systems. We encourage careful evaluation, transparent reporting, and responsible deployment in safety-critical settings. 

## **References** 

- Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Mojtaba, Komeili, Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., Arnaud, S., Gejji, A., Martin, A., Hogan, F. R., Dugas, D., Bojanowski, P., Khalidov, V., Labatut, P., Massa, F., Szafraniec, M., Krishnakumar, K., Li, Y., Ma, X., Chandar, S., Meier, F., LeCun, Y., Rabbat, M., and Ballas, N. V-jepa 2: Self-supervised video models enable understanding, prediction and planning, 2025. URL https://arxiv.org/abs/2506.09985. 

- Berg, J., Zhu, C., Bao, Y., Durugkar, I., and Gupta, A. Semantic world models, 2025. URL https://arxiv. org/abs/2510.19818. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Shi, L. X., Tanner, J., Vuong, Q., Walling, A., Wang, H., and Zhilinsky, U. _π_ 0: A vision-language-action flow model for general robot control, 2026. URL https://arxiv.org/abs/24 10.24164. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., Florence, P., Fu, C., Arenas, M. G., Gopalakrishnan, K., Han, K., Hausman, K., Herzog, A., Hsu, J., Ichter, B., Irpan, A., Joshi, N., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, L., Lee, T.-W. E., Levine, S., Lu, Y., Michalewski, H., Mordatch, I., Pertsch, K., Rao, K., Reymann, K., Ryoo, M., Salazar, G., Sanketi, P., Sermanet, P., Singh, J., Singh, A., Soricut, R., Tran, H., Vanhoucke, V., Vuong, Q., Wahid, A., Welker, S., Wohlhart, P., Wu, J., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., and Zitkovich, B. Rt-2: Vision-language-action 

models transfer web knowledge to robotic control, 2023. URL https://arxiv.org/abs/2307.15818. 

- Brooks, T., Peebles, B., Holmes, C., DePue, W., Guo, Y., Jing, L., Schnurr, D., Taylor, J., Luhman, T., Luhman, E., Ng, C., Wang, R., and Ramesh, A. Video generation models as world simulators. 2024. URL https:// openai.com/research/video-generationmodels-as-world-simulators. 

- Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. Univla: Learning to act anywhere with task-centric latent actions, 2025. URL https://arxi v.org/abs/2505.06111. 

- Burgess, C. P., Matthey, L., Watters, N., Kabra, R., Higgins, I., Botvinick, M., and Lerchner, A. Monet: Unsupervised scene decomposition and representation, 2019. URL https://arxiv.org/abs/1901.11390. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., and Song, S. Diffusion policy: Visuomotor policy learning via action diffusion, 2024. URL https://arxiv.org/abs/2303.04137. 

- Chi, X., Fan, C.-K., Zhang, H., Qi, X., Zhang, R., Chen, A., min Chan, C., Xue, W., Liu, Q., Zhang, S., and Guo, Y. Eva: An embodied world model for future video anticipation, 2025a. URL https://arxiv.org/ab s/2410.15461. 

- Chi, X., Ge, K., Liu, J., Zhou, S., Jia, P., He, Z., Liu, Y., Li, T., Han, L., Han, S., Zhang, S., and Guo, Y. Mind: Learning a dual-system world model for realtime planning and implicit risk analysis, 2025b. URL https://arxiv.org/abs/2506.18897. 

- Chi, X., Jia, P., Fan, C.-K., Ju, X., Mi, W., Zhang, K., Qin, Z., Tian, W., Ge, K., Li, H., Qian, Z., Chen, A., Zhou, Q., Jia, Y., Liu, J., Dai, Y., Wuwu, Q., Bai, C., Wang, Y.-K., Li, Y., Chen, L., Bao, Y., Jiang, Z., Zhu, J., Tang, K., An, R., Luo, Y., Feng, Q., Zhou, S., min Chan, C., Hou, C., Xue, W., Han, S., Guo, Y., Zhang, S., and Tang, J. Wow: Towards a world omniscient world model through embodied interaction, 2025c. URL https://arxiv.org/abs/2509.22642. 

- Engelcke, M., Jones, O. P., and Posner, I. Genesis-v2: Inferring unordered object representations without iterative refinement, 2022. URL https://arxiv.org/abs/ 2104.09958. 

- Greff, K., Kaufman, R. L., Kabra, R., Watters, N., Burgess, C., Zoran, D., Matthey, L., Botvinick, M., and Lerchner, A. Multi-object representation learning with iterative variational inference, 2020. URL https://arxiv. org/abs/1903.00450. 

9 

**Mask World Model** 

- Grooten, B., Tomilin, T., Vasan, G., Taylor, M. E., Mahmood, A. R., Fang, M., Pechenizkiy, M., and Mocanu, D. C. Madi: Learning to mask distractions for generalization in visual deep reinforcement learning, 2023. URL https://arxiv.org/abs/2312.15339. 

- Ha, D. and Schmidhuber, J. World models. 2018. doi: 10.5281/ZENODO.1207631. URL https://zenodo .org/record/1207631. 

- Hafner, D., Lillicrap, T., Ba, J., and Norouzi, M. Dream to control: Learning behaviors by latent imagination, 2020. URL https://arxiv.org/abs/1912.01603. 

- Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. Mastering diverse domains through world models, 2024. URL ht tps://arxiv.org/abs/2301.04104. 

- Hafner, D., Yan, W., and Lillicrap, T. Training agents inside of scalable world models, 2025. URL https://arxi v.org/abs/2509.24527. 

- He, K., Chen, X., Xie, S., Li, Y., Dollar, P., and Girshick, R.´ Masked autoencoders are scalable vision learners, 2021. URL https://arxiv.org/abs/2111.06377. 

- Hu, Y., Guo, Y., Wang, P., Chen, X., Wang, Y.-J., Zhang, J., Sreenath, K., Lu, C., and Chen, J. Video prediction policy: A generalist robot policy with predictive visual representations, 2025. URL https://arxiv.org/ abs/2412.14803. 

- Huang, H., Chen, X., Chen, Y., Li, H., Han, X., Wang, Z., Wang, T., Pang, J., and Zhao, Z. Roboground: Robotic manipulation with grounded vision-language priors, 2025a. URL https://arxiv.org/abs/2504 .21530. 

- Huang, X. and Belongie, S. Arbitrary style transfer in realtime with adaptive instance normalization, 2017. URL https://arxiv.org/abs/1703.06868. 

- Huang, Y., Zhang, J., Zou, S., Liu, X., Hu, R., and Xu, K. Ladi-wm: A latent diffusion-based world model for predictive manipulation, 2025b. URL https://arxi v.org/abs/2505.11528. 

- James, S., Ma, Z., Arrojo, D. R., and Davison, A. J. Rlbench: The robot learning benchmark & learning environment, 2019. URL https://arxiv.org/abs/1909.1 2271. 

- Jia, Y., Liu, J., Liu, S., Zhou, R., Yu, W., Yan, Y., Chi, X., Guo, Y., Shi, B., and Zhang, S. Video2act: A dual-system video diffusion policy with robotic spatio-motional modeling, 2026. URL https://arxiv.org/abs/25 12.03044. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., Vuong, Q., Kollar, T., Burchfiel, B., Tedrake, R., Sadigh, D., Levine, S., Liang, P., and Finn, C. Openvla: An open-source vision-language-action model, 2024. URL https://arxiv.org/abs/2406.09246. 

- Kingma, D. P. and Welling, M. Auto-encoding variational bayes, 2022. URL https://arxiv.org/abs/13 12.6114. 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., Wang, X., Liu, B., Fu, J., Bao, J., Chen, D., Shi, Y., Yang, J., and Guo, B. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation, 2024. URL https://arxiv.org/abs/2411.1 9650. 

- Li, W., Zhang, R., Shao, R., Fang, Z., Zhou, K., Tian, Z., and Nie, L. Semanticvla: Semantic-aligned sparsification and enhancement for efficient robotic manipulation, 2025a. URL https://arxiv.org/abs/2511.10518. 

- Li, Y., Wei, X., Chi, X., Li, Y., Zhao, Z., Wang, H., Ma, N., Lu, M., Han, S., and Zhang, S. Manipdreamer3d : Synthesizing plausible robotic manipulation video with occupancy-aware 3d trajectory, 2025b. URL https: //arxiv.org/abs/2509.05314. 

- Li, Y., Wei, X., Chi, X., Li, Y., Zhao, Z., Wang, H., Ma, N., Lu, M., and Zhang, S. Manipdreamer: Boosting robotic manipulation world model with action tree and visual guidance, 2025c. URL https://arxiv.org/abs/ 2504.16464. 

- Liao, Y., Zhou, P., Huang, S., Yang, D., Chen, S., Jiang, Y., Hu, Y., Cai, J., Liu, S., Luo, J., Chen, L., Yan, S., Yao, M., and Ren, G. Genie envisioner: A unified world foundation platform for robotic manipulation, 2025. URL https://arxiv.org/abs/2508.05635. 

- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M., and Le, M. Flow matching for generative modeling, 2023. URL https://arxiv.org/abs/2210.02747. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning, 2023. URL https://arxiv. org/abs/2306.03310. 

- Liu, C., Zhang, J., Li, C., Zhou, Z., Wu, S., Huang, S., and Duan, H. Ttf-vla: Temporal token fusion via pixelattention integration for vision-language-action models, 2025. URL https://arxiv.org/abs/2508.1 9257. 

10 

**Mask World Model** 

- Locatello, F., Weissenborn, D., Unterthiner, T., Mahendran, A., Heigold, G., Uszkoreit, J., Dosovitskiy, A., and Kipf, T. Object-centric learning with slot attention, 2020. URL https://arxiv.org/abs/2006.15055. 

- Ma, X., Liu, W., Zhang, P., and Xu, N. 3d-rpe: Enhancing long-context modeling through 3d rotary position encoding, 2024. URL https://arxiv.org/abs/2406 .09897. 

- Mi, W., Bao, Y., Chi, X., Ju, X., Qin, Z., Ge, K., Tang, K., Jia, P., Zhang, S., and Tang, J. Tc-idm: Grounding video generation for executable zero-shot robot motion, 2026. URL https://arxiv.org/abs/2601.18323. 

- NVIDIA, :, Ali, A., Bai, J., Bala, M., Balaji, Y., Blakeman, A., Cai, T., Cao, J., Cao, T., Cha, E., Chao, Y.-W., Chattopadhyay, P., Chen, M., Chen, Y., Chen, Y., Cheng, S., Cui, Y., Diamond, J., Ding, Y., Fan, J., Fan, L., Feng, L., Ferroni, F., Fidler, S., Fu, X., Gao, R., Ge, Y., Gu, J., Gupta, A., Gururani, S., Hanafi, I. E., Hassani, A., Hao, Z., Huffman, J., Jang, J., Jannaty, P., Kautz, J., Lam, G., Li, X., Li, Z., Liao, M., Lin, C.-H., Lin, T.-Y., Lin, Y.-C., Ling, H., Liu, M.-Y., Liu, X., Lu, Y., Luo, A., Ma, Q., Mao, H., Mo, K., Nah, S., Narang, Y., Panaskar, A., Pavao, L., Pham, T., Ramezanali, M., Reda, F., Reed, S., Ren, X., Shao, H., Shen, Y., Shi, S., Song, S., Stefaniak, B., Sun, S., Tang, S., Tasmeen, S., Tchapmi, L., Tseng, W.-C., Varghese, J., Wang, A. Z., Wang, H., Wang, H., Wang, H., Wang, T.-C., Wei, F., Xu, J., Yang, D., Yang, X., Ye, H., Ye, S., Zeng, X., Zhang, J., Zhang, Q., Zheng, K., Zhu, A., and Zhu, Y. World simulation with video foundation models for physical ai, 2025. URL https://arxiv.org/abs/2511.00062. 

- Pai, J., Achenbach, L., Montesinos, V., Forrai, B., Mees, O., and Nava, E. mimic-video: Video-action models for generalizable robot control beyond vlas, 2025. URL https://arxiv.org/abs/2512.15692. 

- Qian, Z., Chi, X., Li, Y., Wang, S., Qin, Z., Ju, X., Han, S., and Zhang, S. Wristworld: Generating wrist-views via 4d world models for robotic manipulation, 2025. URL https://arxiv.org/abs/2510.07313. 

- Seo, Y., Hafner, D., Liu, H., Liu, F., James, S., Lee, K., and Abbeel, P. Masked world models for visual control. In _Conference on Robot Learning_ , pp. 1332–1344. PMLR, 2023. 

- Shang, Y., Yu, Y., Zhang, X., Jin, X., Su, H., Wu, W., and Li, Y. Mowm: Mixture-of-world-models for embodied planning via latent-to-pixel feature modulation, 2025. URL https://arxiv.org/abs/2509.21797. 

Reconstructive vision-language-action model as effective robot perceiver, 2025. URL https://arxiv.org/ abs/2508.10333. 

   - Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., Luo, J., Tan, Y. L., Chen, L. Y., Sanketi, P., Vuong, Q., Xiao, T., Sadigh, D., Finn, C., and Levine, S. Octo: An open-source generalist robot policy, 2024. URL https: //arxiv.org/abs/2405.12213. 

   - Tong, Z., Song, Y., Wang, J., and Wang, L. Videomae: Masked autoencoders are data-efficient learners for selfsupervised video pre-training, 2022. URL https:// arxiv.org/abs/2203.12602. 

   - Wang, Q., Zhang, Z., Xie, B., Jin, X., Wang, Y., Wang, S., Zheng, L., Yang, X., and Zeng, W. Disentangled world models: Learning to transfer semantic knowledge from distracting videos for reinforcement learning, 2025. URL https://arxiv.org/abs/2503.08751. 

   - Wang, T., Du, S. S., Torralba, A., Isola, P., Zhang, A., and Tian, Y. Denoised mdps: Learning world models better than the world itself, 2023. URL https://arxiv. org/abs/2206.15477. 

   - Yuan, C., Joshi, S., Zhu, S., Su, H., Zhao, H., and Gao, Y. Roboengine: Plug-and-play robot data augmentation with semantic robot segmentation and background generation, 2025. URL https://arxiv.org/abs/2503.1 8738. 

   - Ze, Y., Zhang, G., Zhang, K., Hu, C., Wang, M., and Xu, H. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

   - Zhang, K., Ge, K., Chi, X., Zhang, R., Shi, S., Dong, Z., Han, S., and Zhang, S. Can world models benefit vlms for world dynamics?, 2025a. URL https://arxiv. org/abs/2510.00855. 

   - Zhang, R., Dong, M., Zhang, Y., Heng, L., Chi, X., Dai, G., Du, L., Du, Y., and Zhang, S. Mole-vla: Dynamic layer-skipping vision language action model via mixtureof-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025b. 

   - Zhu, C., Yu, R., Feng, S., Burchfiel, B., Shah, P., and Gupta, A. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025. 

- Song, W., Zhou, Z., Zhao, H., Chen, J., Ding, P., Yan, H., Huang, Y., Tang, F., Wang, D., and Li, H. Reconvla: 

11 

**Mask World Model** 

## **A. Implementation Details** 

We provide a structured overview of the MWM architecture, training protocol, and reproducibility settings. Detailed hyperparameters are summarized in Table 6. 

### **A.1. Network Architecture** 

**Video VAE & Tokenization.** We utilize a fixed, pretrained 3D VAE to compress 256 _×_ 256 RGB frames into 8 _×_ 8 latent patches with channel dimension _D_ =128. The compression ratios are _fs_ =32 (spatial) and _ft_ =8 (temporal). To align positional embeddings with this compression, we apply 3D Rotary Positional Embeddings (RoPE) with scaling factors **_γ_** = ( _γt ≈_ 0 _._ 267 _, γh_ =32 _, γw_ =32), compensating for the resolution shift between video and latent space. 

**Mask Dynamics Backbone.** The backbone is a 28-layer Diffusion Transformer (DiT) with a hidden dimension of 2048 and 32 attention heads. It processes multi-view inputs (third-person and wrist) via shared spatiotemporal attention. To maintain view consistency while allowing information flow, we insert cross-view attention layers at every 3<sup>rd</sup> block (indices 0 _,_ 3 _, . . . ,_ 27). Text conditioning is injected via a T5-base encoder projecting to 2048 dimensions. 

**Action Expert Head.** The policy head is a 28-layer transformer (512 hidden dim, 16 heads) that parallels the backbone. It uses a _Predictive Feature Bank_ mechanism: the _l_ -th layer of the action transformer attends specifically to the spatial-temporal features extracted from the _l_ -th layer of the frozen DiT backbone via cross-attention. This design directly leverages the hierarchical semantic representations learned during mask pretraining. 

### **A.2. Infrastructure and Reproducibility** 

**Compute.** Training is performed on a cluster of 8 _×_ NVIDIA A100 (80GB) GPUs using DeepSpeed ZeRO-2. Stage 1 takes _∼_ 3.5 days (30k steps), and Stage 2 takes _∼_ 1.5 days (18k steps) per task suite. 

**Data Processing.** Images are resized to 256 _×_ 256 and normalized to [ _−_ 1 _,_ 1]. Semantic masks are rendered with a consistent color palette before VAE encoding. All experiments use a fixed random seed of 42. 

_Table 6._ **Detailed Hyperparameters for MWM.** 

|**Configuration**|**Stage 1 (Dynamics)**|**Stage 2 (Policy)**|
|---|---|---|
|_Optimization (AdamW)_|||
|Learning Rate|3_×_10<sup>_−_4</sup>|5_×_10<sup>_−_5</sup>|
|Batch Size|128 (global)<br>|128 (global)<br>|
|Weight Decay|1_×_10<sup>_−_5</sup>|1_×_10<sup>_−_5</sup>|
|Warmup Steps|1000|1000|
|Gradient Clip|1.0|1.0|
|Precision|bfloat16|bfloat16|
|_Model Architecture_|||
|Layers|28|28|
|Hidden Dimension|2048|512|
|Attention Heads|32|16|
|Cross-Attn Dim|2048|2048|
|VAE|Trainable|Frozen|
|Backbone / Policy|Trainable|Trainable|
|_Sequence & Data_|||
|Context / Horizon|4 frames / 5 latents|4 frames / 36 actions|
|Spatial Compression|_fs_ = 32|-|
|Temporal Compression|_ft_ = 8|-|
|Resolution|256_×_256|-|


## **B. Real-World Experimental Setup** 

To supplement the experimental results presented in Section 4.2, we provide a detailed visualization of our real-world hardware setup and task environments in Figure 4. 

12 

**Mask World Model** 


_Figure 4._ **Real-world experimental environment.** (Left) The hardware setup features a Franka Emika Panda robot arm equipped with a parallel gripper. Perception is provided by two synchronized Intel RealSense D435i cameras: a fixed third-person view capturing the global workspace and a wrist-mounted eye-in-hand view for fine-grained interaction. (Right) Snapshots of the four manipulation tasks used for evaluation: (1) Placing food items into a basket, (2) Opening a drawer to insert a pen, (3) Pouring water into a bowl, and (4) Shelving a book. All policies run on raw RGB streams at 10Hz during deployment. 

**Hardware Configuration.** Our physical testbed consists of a 7-DoF Franka Emika Panda robot. The RGB-D streams from the two RealSense D435i cameras are resized to 256 _×_ 256 resolution. The third-person camera is mounted on a tripod facing the table to cover the entire workspace, while the wrist camera provides ego-centric visual feedback crucial for contact-rich stages of the manipulation tasks. 

**Semantic Annotation Process.** For the training of the Mask World Model (Stage 1), we require semantic segmentation masks corresponding to the video demonstrations. We utilize **RoboEngine** (Yuan et al., 2025) to automatically generate pixel-wise semantic annotations for the robot arm, gripper, and task-relevant objects (e.g., bread, drawer handle, cup) offline. These masks serve strictly as supervision targets during the pre-training phase; at inference time, MWM relies solely on the raw multi-view RGB inputs. 

## **C. Detailed Algorithms of MWM Variants** 

We provide the detailed training and inference procedures for MWM-C1 and MWM-C2 in Algorithm 1 and Algorithm 2, respectively. 

## **D. Detailed Random Token Pruning Results** 

In this section, we report the detailed success rates for the Random Token Pruning (RTP) stress test on LIBERO. We compare **MWM (Ours)** and **GE-ACT** across pruning ratios _r ∈{_ 0 _._ 1 _, . . . ,_ 0 _._ 9 _}_ on four evaluation suites: Spatial, Object, Goal, and Libero-10. 

## **E. Detailed Visual Generalization Results** 

In this section, we provide the per-task success rates for the visual generalization experiments discussed in Section 4.3.2. We evaluated three methods (GE-ACT, _π_ 0, and our MWM) across four real-world tasks under three distinct appearance shifts: Background (BG), Lighting (Light), and Object Color (Color). 

To provide qualitative context for these quantitative results, we visualize the specific environmental variations in Figure 5. These shifts serve as stress tests to determine whether the models are overfitting to visual nuisance variables (e.g., table texture or illumination) rather than learning the underlying manipulation geometry. 

**Quantitative Results.** The detailed success rates for each shift type are presented below. Table 9 details the performance under background changes, Table 10 covers lighting variations, and Table 11 reports robustness to object color swaps. 

13 

**Mask World Model** 

_Table 7._ **MWM (Ours) Robustness Profile.** Success rates at varying visual token pruning ratios. 

|Pruning Ratio (_r_)|LIBERO-Spatial|LIBERO-Object|LIBERO-Goal|LIBERO-10|
|---|---|---|---|---|
|0.1|0.98|1.00|0.98|0.96|
|0.2|0.97|1.00|0.97|0.96|
|0.3|0.96|0.99|0.94|0.95|
|0.4|0.95|0.97|0.89|0.79|
|0.5|0.90|0.94|0.84|0.69|
|0.6|0.85|0.80|0.65|0.37|
|0.7|0.50|0.49|0.40|0.03|
|0.8|0.05|0.10|0.07|0.00|
|0.9|0.00|0.00|0.00|0.00|


_Table 8._ **GE-ACT Robustness Profile.** Success rates at varying visual token pruning ratios. 

|Pruning Ratio (_r_)|LIBERO-Spatial|LIBERO-Object|LIBERO-Goal|LIBERO-10|
|---|---|---|---|---|
|0.1|0.96|0.99|0.95|0.94|
|0.2|0.96|0.98|0.94|0.95|
|0.3|0.96|0.97|0.94|0.86|
|0.4|0.96|0.96|0.89|0.77|
|0.5|0.90|0.85|0.84|0.59|
|0.6|0.83|0.47|0.67|0.39|
|0.7|0.51|0.09|0.42|0.03|
|0.8|0.11|0.00|0.21|0.00|
|0.9|0.00|0.00|0.00|0.00|


_Table 9._ **Detailed success rates under Background (BG) shift.** The tablecloth texture was replaced with unseen patterns. Reported values are success rates (%) over 20 trials per task. 

|METHOD|TASK1|TASK2|TASK3|TASK4|AVG.|
|---|---|---|---|---|---|
|GE-ACT|0%|0%|10%|5%|3.8%|
|_π_0|10%|20%|15%|10%|13.8%|
|**MWM (OURS)**|**35%**|**25%**|**20%**|**30%**|**27.5%**|


_Table 10._ **Detailed success rates under Lighting (Light) shift.** Illumination intensity was significantly altered (dimmer/brighter). Reported values are success rates (%) over 20 trials per task. 

|METHOD|TASK1|TASK2|TASK3|TASK4|AVG.|
|---|---|---|---|---|---|
|GE-ACT|30%|15%|10%|20%|18.8%|
|_π_0|30%|20%|0%|20%|17.5%|
|**MWM (OURS)**|**65%**|**50%**|**50%**|**60%**|**56.3%**|


_Table 11._ **Detailed success rates under Object Color (Color) shift.** Task objects were swapped with instances of unseen colors. Reported values are success rates (%) over 20 trials per task. 

|METHOD|TASK1|TASK2|TASK3|TASK4|AVG.|
|---|---|---|---|---|---|
|GE-ACT|25%|5%|10%|20%|15.0%|
|_π_0|30%|10%|0%|65%|26.3%|
|**MWM (OURS)**|**45%**|**25%**|**50%**|**50%**|**42.5%**|


14 

**Mask World Model** 

|**Alg**|**orithm 1**MWM-C1: Cosmos-Predict2 with Inverse Dynamics|
|---|---|
|1: <br>2:|**Input:** Observation_ot_, language instruction_l_, ground truth masks_m_, actions_a_<br> **Output:** Trained models_Wθ, ϕψ_ and inference resultˆ_a_|
|3: <br>4:|**Step 1: Train Mask World Model**_Wθ_<br> **while**not converged**do**|
|5:|Sample video batch: _v ←_Sample(_D_);<br>|
|6:|Convert to mask latents: _zm ←E_(_vmask_);<br>|
|7:|Compute diffusion loss: _L_cosmos _←∥ϵθ_(_zm_+_σϵ, t, c_)_−ϵ∥_<sup>2</sup>;|
|8:|Update_θ ←θ −η∇θL_cosmos;|
|9:|**end while**|
|10:|**Step 2: Train Inverse Dynamics Model (IDM)**_ϕψ_|
|11:|**while**not converged**do**|
|12:|Sample adjacent masks: (_mt, mt_+1_, at_)_∼D_;|
|13:|Predict action: ˆ_at ←ϕψ_(_mt, mt_+1);<br>|
|14:|Update_ψ ←ψ −η∇ψ∥_ˆ_at −at∥_<sup>2</sup>;|
|15:|**end while**|
|16:|**Step 3: Inference Pipeline**|
|17:|Given current observation_ot_and instruction_l_:|
|18:|Generate future mask rollout: ˆ_mt_+1:_t_+_τ ←_Denoise(_Wθ, ot, l_);|
|19:|**for**_k_ = 0to_τ −_1**do**|
|20:|Infer action: ˆ_at_+_k ←ϕψ_( ˆ_mt_+_k,_ ˆ_mt_+_k_+1);|
|21:|**end for**|
|22:|**Return**Action sequenceˆ_at_:_t_+_τ_|


|**Alg**|**orithm 2**MWM-C2: Predictive Feature Policy|
|---|---|
|1:|**Input:** Observation_ot_, language instruction_l_, ground truth actions_a_|
|2:|**Output:** Trained policy_πξ_ and inference resultˆ_a_|
|3:|**Step 1: Pretrain and Freeze Backbone**|
|4:|Pretrain World Model_Wθ_ on mask prediction (same as C1, Step 1);|
|5:|Freeze weights: _θ ←_StopGradient(_θ_);|
|6:|**Step 2: Train Diffusion Policy Head**_πξ_|
|7:|**while**not converged**do**|
|8:|Extract predictive features: **F**_←Wθ_(_ot, l_);|
|9:|//**F**contains semantic-aware spatio-temporal tokens|
|10:|Sample noise_ϵ_and timestep_k_;|
|11:|Noised action: ˜_a ←a_+_σkϵ_;|
|12:|Predict noise: ˆ_ϵ ←πξ_(˜_a, k,_**F**);|
|13:|Update_ξ ←ξ −η∇ξ∥_ˆ_ϵ −ϵ∥_<sup>2</sup>;|
|14:|**end while**|
|15:|**Step 3: Inference Pipeline**|
|16:|Given current observation_ot_:|
|17:|Extract features (single forward pass): **F**_←Wθ_(_ot, l_);|
|18:|Initialize noise action: ˆ_aK ∼N_(0_, I_);|
|19:|**for**_k_ =_K_ down to1**do**|
|20:|Denoise action: ˆ_ak−_1 _←_Sampler(_πξ,_ˆ_ak,_**F**);|
|21:|**end for**|
|22:|**Return**Denoised actionˆ_a_0|


15 

**Mask World Model** 


_Figure 5._ **Visual generalization stress tests.** We evaluate policy robustness under three distinct distribution shifts relative to the nominal condition (Top-Left). The shifts include: (Top-Right) **Object Color Shift** , where task objects are swapped with unseen colors while retaining geometry; (Bottom-Left) **Lighting Shift** , involving significant changes in illumination intensity; and (Bottom-Right) **Background (BG) Shift** , where the table surface is replaced with unseen textures. These setups correspond to the quantitative results reported in Tables 9–11. 

16 

