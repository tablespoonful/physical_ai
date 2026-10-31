---
title: "Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising"
date: "2026-04-29"
authors: "Jun Guo; Qiwei Li; Peiyan Li; Zilong Chen; Nan Sun; Yifei Su"
url: https://arxiv.org/abs/2604.26694
pdf: https://arxiv.org/pdf/2604.26694
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.26694)** / [論文ページ](https://arxiv.org/abs/2604.26694)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising** 

**Jun Guo**<sup>1</sup><sup>_,_2</sup> **Qiwei Li**<sup>2</sup><sup>_,_3</sup> **Peiyan Li**<sup>2</sup><sup>_,_4</sup> **Zilong Chen**<sup>1</sup> **Nan Sun**<sup>1</sup><sup>_,_2</sup> **Yifei Su**<sup>2</sup> **Heyun Wang**<sup>2</sup> **Yuan Zhang**<sup>2</sup> **Xinghang Li**<sup>2</sup><sup>_†_</sup> **Huaping Liu**<sup>1</sup><sup>_†_</sup> 

1Tsinghua University 2Xiaomi Robotics 3 Peking University 4 CASIA 

```
https://sharinka0715.github.io/X-WAM/
```

## **Abstract** 

We propose X-WAM, a Unified 4D World Model that unifies real-time robotic action execution and high-fidelity 4D world synthesis (video + 3D reconstruction) in a single framework, addressing the critical limitations of prior unified world models ( _e.g._ , UWM) that only model 2D pixel-space and fail to balance action efficiency and world modeling quality. To leverage the strong visual priors of pretrained video diffusion models, X-WAM imagines the future world by predicting multi-view RGB-D videos, and obtains spatial information efficiently through a lightweight structural adaptation: replicating the final few blocks of the pretrained Diffusion Transformer into a dedicated depth prediction branch for the reconstruction of future spatial information. Moreover, we propose Asynchronous Noise Sampling (ANS) to jointly optimize generation quality and action decoding efficiency. ANS applies a specialized asynchronous denoising schedule during inference, which rapidly decodes actions with fewer steps to enable efficient real-time execution, while dedicating the full sequence of steps to generate high-fidelity video. Rather than entirely decoupling the timesteps during training, ANS samples from their joint distribution to align with the inference distribution. Pretrained on over 5,800 hours of robotic data, X-WAM achieves 79.2% and 90.7% average success rate on RoboCasa and RoboTwin 2.0 benchmarks, while producing high-fidelity 4D reconstruction and generation surpassing existing methods in both visual and geometric metrics. 

## **1 Introduction** 

The pursuit of general-purpose Embodied AI has been significantly accelerated by the advent of robotic foundation models. Current approaches in this space can be broadly categorized into two paradigms, each targeting a single objective. On the one hand, _policy models_ focus on predicting executable actions for robot control. Vision-Language-Action (VLA) models [1–7] fine-tune pretrained Vision-Language Models (VLMs) to output motor commands, excelling at instruction following and semantic reasoning but lacking the geometric intuition and physical awareness of how actions continuously unfold in the real world [8]. World Action Models (WAMs) [8–12] further leverage video generation models to jointly predict future observations and actions, harnessing video priors for stronger physical understanding and generalization. On the other hand, World Models [13–18] focus on simulating future observations: text-conditioned and action-conditioned world models excel at generating realistic visual predictions of physical dynamics, but do not directly produce executable actions for robot control. These separate paradigms each address a single task, limiting cross-task synergy and representational efficiency. 

Preprint. 


Figure 1: **Overview of X-WAM.** _Top:_ X-WAM is a unified 4D World Action Model that jointly predicts future multi-view RGB-D videos and robot actions from video priors, featuring a lightweight depth adaptation module for spatial reconstruction and Asynchronous Noise Sampling (ANS) for efficient action decoding. _Bottom:_ X-WAM surpasses existing methods in policy success rate on RoboCasa and RoboTwin 2.0, produces high-fidelity 4D reconstruction and generation, and enables real-time execution deployment on physical robots. 

Recently, a line of work has begun to bridge this divide by constructing unified world action models [19–22] that jointly model video generation and action prediction within a single framework. By sharing representations across modalities, these approaches achieve encouraging results in both future prediction quality and policy execution, demonstrating the significant potential of multi-task unified modeling. However, they remain confined to 2D pixel-space observation, lacking explicit spatial awareness and 3D geometric grounding. Since the physical world is fundamentally threedimensional, this confinement strips away critical geometric structures, causing models to hallucinate physically implausible futures and preventing geometrically faithful 3D reconstruction. To unlock the full potential of unified world action models, it is imperative to elevate them from 2D pixel predictors to spatially aware 4D dynamics simulators that jointly address generation, reconstruction, and policy execution. 

Building upon these initial unification efforts, we take a further step by incorporating explicit spatial information into the unified modeling paradigm. We propose X-WAM (Figure 1), a unified 4D World Action Model that simultaneously targets four objectives within a single architecture: high-fidelity video generation, 3D spatial reconstruction, high policy success rate, and efficient action execution. Built on the powerful visual priors of the pretrained video foundation model, X-WAM takes multiview RGB observations and current robot states as inputs to jointly generate future 4D observations alongside the robot’s future states and actions. However, seamlessly integrating 4D spatial awareness and policy execution into such a unified framework presents two fundamental technical challenges. 

The first challenge lies in effectively injecting 3D perception into the model without destroying its pretrained knowledge or introducing prohibitive computational overhead. Naive approaches to spatial modeling face distinct drawbacks: concatenating depth maps as additional tokens along the sequence dimension doubles the sequence length, incurring quadratic growth in attention cost; alternatively, fusing depth along the channel dimension shifts the input distribution away from the pretrained manifold, substantially increasing learning difficulty. To circumvent these bottlenecks, we introduce a lightweight structural adaptation. Rather than expanding the denoising sequence, X-WAM explicitly models the 4D world by simply replicating the final few blocks of the pretrained Diffusion Transformer (DiT) [23] to construct a dedicated depth prediction branch. This elegant design successfully extracts 3D spatial information without altering the original model’s core structure, bypassing the sequence length explosion while strictly preserving the integrity of the pretrained visual priors. As shown in our experiments, this depth supervision not only enables high-quality 3D reconstruction but also consistently improves policy success rates, confirming that explicit spatial modeling benefits multiple objectives of the unified framework simultaneously. 

2 

The second challenge stems from the inherent modality mismatch when jointly generating highdimensional video trajectories and low-dimensional robotic actions. While synthesizing high-fidelity video necessitates numerous denoising steps [24, 25], low-dimensional actions require far fewer steps [4, 26], and can be accurately recovered even from highly noisy video latents [9, 10, 20, 27, 28]. Motivated by this insight, we propose Asynchronous Noise Sampling (ANS). ANS introduces a specialized asynchronous denoising schedule for inference: it rapidly decodes precise actions using only a fraction of the initial steps to allow them to be immediately executed by the policy, and subsequently completes the remaining steps to render high-fidelity future videos. Driven by this asynchronous inference characteristic, ANS accordingly reformulates the training-stage sampling strategy. Instead of completely decoupling the noise timesteps of these modalities via independent random sampling, ANS systematically samples from a joint distribution of video and actions that strictly matches the test-time distribution. This elegantly eliminates the inefficiencies of decoupled sampling, maximizing both action inference speed and visual generation quality. 

In summary, our primary contributions are threefold: 

- We propose X-WAM, a unified 4D World Action Model that incorporates explicit 3D spatial awareness into the joint video-action modeling paradigm. By introducing a lightweight structural adaptation, replicating the final blocks of the pretrained DiT as a dedicated depth branch, we achieve high-quality spatial modeling without doubling sequence lengths or disrupting pretrained visual priors. 

- We introduce Asynchronous Noise Sampling (ANS) to enhance the joint generation of videos and actions. By sampling from their joint distribution and employing an asynchronous denoising schedule, ANS improves the training efficiency while maximizing both action decoding speed and video generation quality. 

- We demonstrate that X-WAM consistently outperforms all baselines on RoboCasa and RoboTwin 2.0 benchmarks and real-world earphone packing experiments, while producing superior 4D reconstruction and generation across both visual and geometric metrics, validating that a single unified framework can jointly optimize policy execution, visual generation, and spatial reconstruction. 

## **2 Related Work** 

### **2.1 Unified World Action Modeling** 

Current general embodied models fall into two complementary paradigms. _Policy models_ , predominantly Vision-Language-Action (VLA) models [1–7, 29–31], map observations directly to executable robot actions for real-time control. _World models_ [13–18] aim to model environmental dynamics and learn to imagine future observations. Although naturally complementary, the two paradigms have largely evolved in isolation. Some works bridge the gap from the world model side by attaching inverse dynamics models or extracting intermediate representations to convert world models into planners [22, 32–35]. Others augment VLAs with auxiliary future prediction objectives to inject dynamics awareness [36–41]. While both directions yield improvements, they remain loosely coupled rather than truly unified. 

Recently, a line of work has sought to build end-to-end World Action Models (WAMs) from video foundation models. UWM [19] and Motus [20] formulate the problem as a Unified World Model, enabling flexible conditioning and multi-task generation. VideoVLA [21] and Cosmos Policy [11] directly append action tokens into video sequences for joint prediction. Other works [10, 27, 28] employ a Mixture of Transformer architecture with independent parameters and denoising timesteps for each modality. DreamZero [9], LingBot-VA [8], and GigaWorld-Policy [12] leverage causal attention masks and KV caching to reduce inference latency. Surveys [42] have shown that such unified approaches generalize better than traditional VLAs. Despite this progress, two limitations persist. First, existing unified models remain confined to 2D pixel-space, lacking explicit 3D spatial awareness. Second, although several recent WAMs [9, 19, 20] have begun to address the balance between video generation quality and action decoding efficiency by decoupling their sampling timesteps, these approaches rely on independent noise sampling for each modality during training, which introduces a mismatch between the training and inference distributions and thus limits the effectiveness of asynchronous denoising. 

3 


Figure 2: **Overview of X-WAM.** (a) Model architecture: multi-view RGB observations, proprioceptive states, and noisy actions are encoded and jointly denoised by a Diffusion Transformer initialized from Wan2.2-5B, with a lightweight interleaved depth branch for spatial modeling. (b) Asynchronous Noise Sampling (ANS): (i) standard decoupled sampling wastes training on configurations where _tO < ta_ ; (ii) our coupled joint sampling ensures _tO ≥ ta_ , faithfully matching the inference distribution; (iii) during inference, actions are decoded in _Ta_ steps and immediately dispatched, while video denoising continues for _TO_ steps. 

### **2.2 3D Modeling in Embodied Models** 

Owing to the abundance and accessibility of 2D data, contemporary mainstream embodied models primarily operate within a 2D space for perception, modeling, and prediction. However, the lack of explicit spatial awareness and modeling capabilities, coupled with an over-reliance on purely data-driven fitting, creates a significant bottleneck in tasks that demand spatial comprehension and out-of-distribution generalization. To address this issue, numerous studies have incorporated 3D information into the training pipeline to further enhance the capabilities of embodied models. Within the VLA framework, one category of research [38, 43–47] encodes 3D features to serve as predictive targets or supervisory signals within the model’s sequence. Another category [48–50] directly utilizes explicit 3D representations as inputs, performing predictions natively within the 3D space. 

In the context of world models and world action models, several approaches [51–57] introduce 3D supervisory signals during the video generation process, endowing the models with multi-view consistency and superior spatial reasoning. ManiGaussian [58] and GWM [59] construct world models entirely within 3D representations, utilizing the neural rendering technique of 3D Gaussian Splatting [60] to build high-fidelity 3D world models. Given that current open-source robotic datasets are predominantly composed of 2D videos, existing 3D modeling methods frequently rely on pretrained feed-forward 3D reconstruction models [61–64] to extract spatial information from robotic data. This strategy effectively transfers the spatial reasoning capabilities of reconstruction models to the video generation pipelines. To the best of our knowledge, no existing work has incorporated explicit spatial information into the unified world action modeling paradigm, nor has any unified model demonstrated the ability to simultaneously serve as a high-fidelity video generator, a 3D reconstruction system, and an efficient policy model within a single framework. 

## **3 Methodology** 

Building upon recent advances in unified world action modeling, we propose X-WAM as a unified framework that simultaneously addresses video generation, 3D spatial reconstruction, policy success 

4 

rate, and efficient action execution. This is achieved through two core designs: a lightweight depth adaptation module (Section 3.2) that enables spatial reconstruction, and Asynchronous Noise Sampling (Section 3.3) that jointly optimizes generation quality and action decoding efficiency. We begin by presenting the overall model architecture (Section 3.1), and then detail the training procedure including data processing and the training pipeline (Section 3.4). 

### **3.1 Model Architecture** 

X-WAM takes a language instruction _c_ , the initial proprioceptive state _s_ 0, and multi-view initial RGB observations _O_ 0 as conditions, and jointly predicts future RGB videos _O_ 1: _H_ , depth videos _D_ 1: _H_ , proprioceptive states _s_ 1: _H_ , and actions _a_ 1: _K_ , where _H_ and _K_ denote the prediction horizons for video/state and actions, respectively. Following [9, 21], X-WAM is fine-tuned from a pretrained video generation Diffusion Transformer [23], specifically Wan2.2-TI2V-5B [65] in this work. RGB videos are encoded into latent representations via the original causal VAE encoder _E_ , _i.e_ ., **z** _O_ = _E_ ( _O_ ), while proprioceptive states and robot actions are projected into the latent space via learnable MLPs: **z** _s_ = MLP _s_ ( _s_ ) and **z** _a_ = MLP _a_ ( _a_ ). After denoising, the clean latents are decoded back to the original physical spaces via symmetric MLPs: _s_ ˆ = MLP<sup>dec</sup> _s_<sup>(</sup><sup>**z**</sup><sup>_s_) and ˆ</sup><sup>_a_=MLPdec</sup> _a_<sup>(</sup><sup>**z**</sup><sup>_a_).The three</sup> modalities are concatenated into a unified denoising sequence: 


which is processed with bidirectional full attention, with depth reconstructed from the generated RGB video sequence. The initial observation **z** _O_ 0 and state **z** _s_ 0 remain fixed throughout the denoising process with their noise timestep set to _t_ = 0 ( _i.e_ ., treated as clean samples). 

Concretely, given 1 conditioning RGB frame and 1 initial state, X-WAM predicts _H_ = 8 future RGB frames, _H_ = 8 future states, and _K_ = 32 future actions. This asymmetric design reflects the different temporal requirements of each modality: actions demand a higher control frequency for smooth and responsive robot execution, while RGB frames and states can be predicted at a lower frequency sufficient for visual generation and 4D reconstruction. The states are temporally aligned with the video frames to enable frame-wise multi-view RGB-D fusion for 3D reconstruction, whereas the actions are uniformly distributed across the same time span at _K/H_ = 4 _×_ the video frame rate. 

The original video diffusion model is designed for single-view 2D generation, employing 3D Rotary Position Embeddings (RoPE) [66] to encode temporal and spatial positions within the sequence. To enable multi-view compatibility without disrupting the pretrained positional encodings, we augment the tokens of each viewpoint with learnable view embeddings to indicate the view index. For proprioceptive states and actions, we apply the same temporal RoPE as the video tokens along the time dimension, allowing the model to infer the temporal correspondence between states/actions and video frames through positional proximity. 

X-WAM is designed to simultaneously reconstruct and generate the future world. Reconstructing 3D representations ( _e.g_ ., point clouds) from multi-view RGB-D outputs requires camera poses for each viewpoint. Unlike prior works [53] that explicitly encode camera extrinsics or ray direction maps as tokens, we adopt a more principled approach grounded in the structure of robotic systems. We observe that cameras in robotic manipulation setups can be categorized into two types: _static_ cameras (first-person and third-person views), whose poses remain constant throughout task execution, and _dynamic_ cameras (wrist-mounted), which are rigidly attached to the robot arm with a fixed hand-eye calibration matrix that depends solely on the robot model. Therefore, instead of predicting explicit camera extrinsics, X-WAM predicts the end-effector pose **T** ee _∈ SE_ (3) and derives the wrist camera pose via the fixed hand-to-eye calibration matrix **T** h2e: 


This conversion enables the fusion of 3D information across all viewpoints to reconstruct a unified 3D representation. 

### **3.2 Lightweight Depth Adaptation** 

In X-WAM, depth maps are predicted in the same VAE latent space as RGB frames: each singlechannel depth map is replicated three times along the channel dimension to form a pseudo-RGB image, encoded by the same causal VAE _E_ , and decoded back via the symmetric VAE decoder after 

5 

denoising. Rather than concatenating depth tokens along the sequence dimension (which doubles attention cost) or fusing along the channel dimension (which shifts the input distribution away from the pretrained manifold), we propose a lightweight depth adaptation module that modifies the pretrained DiT architecture. Specifically, given a model with _N_ DiT blocks, we replicate the final _M_ blocks ( _M < N_ ) to construct an auxiliary depth prediction branch. After the shared first _N −M_ blocks produce hidden states **H** , the depth branch and the main branch are initialized as **Z**<sup>(0)</sup> _D_<sup>=</sup><sup>**Z**</sup> m<sup>(0)</sup> = **H** and executed in an _interleaved_ fashion. At each layer _j ∈{_ 1 _, . . . , M }_ : 


where DepthBlock _j_ attends to the main branch’s input **Z** m<sup>(</sup><sup>_j−_1)</sup> at the same layer via cross-attention, while the main branch remains unaffected by depth tokens. We term this asymmetric connectivity _unilateral attention_ : the depth branch can read from the main branch, but not vice versa, thereby strictly preserving the integrity of the pretrained weights. The depth branch is trained to regress the inverse depth of the current video frame using mean squared error (MSE) loss, consistent with established depth estimation models [63, 64]. 

This design rests on the fundamental assumption that depth information can be inferred from RGB features without requiring fully independent generation. The detailed single-step procedure is presented in Algorithm 1 (Appendix A). Depth supervision during training enhances the model’s spatial structure perception. During inference, this auxiliary depth branch does not need to participate in every denoising step and can be flexibly toggled on or off, substantially reducing rollout overhead. 

### **3.3 Asynchronous Noise Sampling** 

Prior works [9, 10, 20, 27, 28] decouple the noise timesteps of video and actions to allow faster action decoding during inference. However, independently sampling each modality’s timestep introduces training configurations that never arise at test time ( _e.g_ ., _tO < ta_ ), degrading training efficiency. To align the training and inference noise distributions, X-WAM adopts Asynchronous Noise Sampling (ANS). The complete procedure is detailed in Algorithm 2 (Appendix A). 

**Asynchronous inference.** During inference, ANS applies asynchronous denoising timesteps for video and actions, as illustrated in Figure 2(b-iii). We allocate _Ta_ denoising steps for proprioceptive states and actions, and _TO_ denoising steps for video ( _Ta < TO_ ). Both modalities start from pure noise and are denoised with step sizes of _T_ <u>1</u> _a_<sup>and</sup> _T_ <u>1</u> _O_<sup>, respectively.After</sup><sup>_Ta_forward passes, the noise-free</sup> actions are obtained and can be immediately dispatched to the downstream robot for execution. If a clear, complete video is desired, the remaining _TO − Ta_ steps are continued, during which the actions serve as a clean modality and undergo no further denoising. In this regime, the inference process naturally becomes an action-conditioned world model. 

**Coupled noise sampling during training.** To realize this asynchronous inference behavior, we also apply different noise timesteps to video and actions during training. However, unlike prior works that sample from two independent distributions, we place the video and action noise levels into a joint distribution and perform coupled sampling. Formally, the joint noise level ( _tO, ta_ ) is drawn from the following mixture: 


where the first case corresponds to action-conditioned video generation with noise-free actions, and the second case represents asynchronous joint generation. The Beta(1 _._ 5 _,_ 1) distribution, rescaled to [ _ta,_ 1], biases _tO_ toward higher noise levels, reflecting the fact that video typically requires more denoising steps than actions. Crucially, _tO_ is sampled _conditioned on ta_ , making them dependent rather than independent random variables. This coupled sampling strategy more faithfully reflects the inference-time distribution, enabling more efficient training of the WAM. 

### **3.4 Training Details** 

Consistent with the pretrained Wan2.2-5B model [65], we fine-tune X-WAM using the flow matching framework [67]. The model _fθ_ is trained to predict the velocity field **v** = **_ϵ_** _−_ **z**<sup>0</sup> given noisy inputs 

6 

at timestep _t_ . For a modality _m ∈{O, s, a}_ with corresponding timestep _tm_ , the velocity prediction loss is: 


where _tO_ and _ta_ denote the video and action noise timesteps sampled via ANS (Eq. 4), with _ts_ = _ta_ . The depth branch is supervised with a direct MSE regression loss on inverse depth: 2 _L_ depth = , where _D_<sup>_∗_</sup> denotes the ground-truth inverse depth. The total training objective ��� _D_ ˆ _− D∗_ ��� is: 


where _λs_ , _λa_ , and _λD_ are weighting coefficients. 

To build a unified 4D model capable of generation, reconstruction, and manipulation, we train the model on over 5,800 hours of data, encompassing both real-robot and simulated datasets spanning diverse manipulation tasks. All datasets undergo preprocessing and filtering, and are unified into a consistent coordinate system and representation. We define a universal interface to represent robot states and actions across heterogeneous datasets. The state is defined as the poses and gripper positions of a dual-arm end-effector, while the action is defined as the corresponding changes in end-effector poses and gripper positions. For single-arm robots, we treat the single arm as the left arm and do not supervise the right-arm output. During inference, we employ the UniPC [68] multistep scheduler recommended by Wan2.2, maintaining separate scheduler instances with different step sizes for video and state/action modalities, following the asynchronous inference procedure described in Section 3.3. Full details on pretraining data, implementation, and baselines are provided in Appendix B. 

## **4 Experiments** 

We evaluate X-WAM across three complementary dimensions: policy execution (Section 4.1), 4D reconstruction and generation (Section 4.2), and ablation studies that jointly analyze both objectives (Section 4.3). We additionally deploy X-WAM on a real-world dual-arm platform for earphone packing tasks (Appendix D). This comprehensive evaluation validates that X-WAM’s unified framework simultaneously achieves strong performance across all dimensions. 

### **4.1 Policy Evaluation** 

We first evaluate the policy execution capability of X-WAM by deploying it in closed-loop simulation and measuring task success rates on two representative robotic manipulation benchmarks. 

**RoboCasa** [69] is a large-scale simulation benchmark featuring diverse kitchen manipulation tasks with realistic scenes and object variations. We report the average success rate (SR) across 24 manipulation tasks. We compare against two VLA baselines: _π_ 0 [4] and GR00T-N1.5 [6], and three WAM baselines: UWM [19], DreamZero [9], and Cosmos Policy [11]. 

**RoboTwin 2.0** [70] is a dual-arm manipulation benchmark that evaluates policy generalization under two settings: _Clean_ , where the environment matches a certain distribution, and _Randomized_ , where object poses, appearances, and distractors are randomized to test robustness. Following [20], we train X-WAM on all trajectories of AgileX arms, including 50 clean and 500 randomized trajectories on 50 tasks. We compare against two VLA baselines: _π_ 0 [4] and _π_ 0 _._ 5 [5], and three WAM baselines: UWM [19], GigaWorld-Policy [12], and Motus [20]. 

Results on RoboCasa and RoboTwin 2.0 are presented in Table 1 and Table 2, respectively. As shown in Table 1 and Table 2, X-WAM consistently outperforms all baselines on both benchmarks. On RoboCasa, X-WAM attains 79.2% average SR, surpassing the strongest baseline Cosmos Policy (67.1%) by 12.1 percentage points. On RoboTwin 2.0, X-WAM achieves 89.8% and 90.7% under the Clean and Randomized settings, respectively, outperforming the prior method Motus (88.7% / 87.0%) across both protocols. These results validate that incorporating explicit 3D spatial awareness and large-scale pretraining into the unified world action modeling framework yields substantial performance gains. Per-task breakdowns are provided in Appendix C. 

7 

Table 1: Average success rate (%) on 24 manipulation tasks of RoboCasa benchmark. 

Table 2: Average success rate (%) on 50 tasks of RoboTwin 2.0 benchmark. 

|Method|Avg SR|Method|Clean|Randomized|
|---|---|---|---|---|
|_VLA-based methods_||_VLA-based methods_|||
|_π_0 [4]|62.5|_π_0 [4]|65.9|58.4|
|GR00T-N1.5 [6]|64.1|_π_0_._5 [5]|82.7|76.8|
|_WAM-based methods_||_WAM-based methods_|||
|UWM [19]|60.8|UWM [19]|81.7|78.6|
|DreamZero [9]|62.4|GigaWorld-Policy [12]|87.0|85.0|
|Cosmos Policy [11]|67.1|Motus [20]|88.7|87.0|
|X-WAM (Ours)|**79.2**|X-WAM (Ours)|**89.8**|**90.7**|


Table 3: 4D reconstruction quality on RoboCasa. _↑_ indicates higher is better; _↓_ indicates lower is better. 

|Method||RGB||Dep|th|Point Cloud|
|---|---|---|---|---|---|---|
||PSNR_↑_|SSIM_↑_|LPIPS_↓_|AbsRel_↓_|_δ_1_↑_|CD_↓_|
|DreamZero [9] + DA3 [64]|21.12|0.7788|0.1580|0.1362|0.8594|0.0680|
|Robot4DGen [54]|22.67|0.8207|0.1026|0.0736|0.9443|0.0134|
|X-WAM w/o depth + DA3 [64]|23.09|0.8916|0.0548|0.1045|0.9089|0.0401|
|X-WAM (Ours)|**23.46**|**0.8942**|**0.0513**|**0.0349**|**0.9738**|**0.0049**|


### **4.2 4D Reconstruction and Generation** 

We next evaluate the 4D reconstruction and generation capabilities of X-WAM on the RoboCasa environment. Specifically, we execute the policy in simulation and compare the predicted multi-view RGB-D observations against the ground-truth observations rendered by the simulator. We adopt three groups of metrics: PSNR, SSIM, and LPIPS for visual fidelity, absolute relative error (AbsRel) and _δ_ 1 accuracy for depth quality, and Chamfer Distance (CD) for the quality of the reconstructed point clouds. The depth metrics (AbsRel, _δ_ 1) evaluate single-view reconstruction capability, measuring how accurately the model predicts per-pixel geometry from each individual viewpoint. In contrast, Chamfer Distance evaluates multi-view consistency and the accuracy of camera extrinsic estimation (for static cameras) and robot proprioceptive state prediction (for wrist cameras), as it requires lifting per-view depth maps into a shared 3D coordinate frame and fusing them into a unified point cloud. Note that pixel-level metrics (PSNR, SSIM, LPIPS, AbsRel, _δ_ 1) are computed only on the two static cameras (first-person and third-person views), as the wrist camera suffers from pixel misalignment due to minor errors in the predicted end-effector pose, rendering per-pixel comparison unreliable. The quality of wrist-camera predictions can instead be assessed through Chamfer Distance and qualitative visualizations. As baselines, we consider a two-stage approach that combines DreamZero [9] for RGB video generation with Depth Anything 3 [64] for post-hoc depth estimation, and Robot4DGen [54], a geometry-aware 4D video generation method. We also include an ablative variant, X-WAM w/o depth + DA3, which removes our depth branch and instead relies on Depth Anything 3 for depth estimation. 

As shown in Table 3, X-WAM achieves the best performance across all metrics. Compared with the two-stage pipeline of DreamZero + DA3, X-WAM improves PSNR by 2.34 dB and reduces Chamfer Distance from 0.0680 to 0.0049, demonstrating that end-to-end joint modeling produces substantially more accurate spatial reconstructions than post-hoc depth estimation applied to independently generated videos. Robot4DGen, which incorporates geometric priors during generation, achieves competitive depth metrics but falls short on visual fidelity (LPIPS 0.1026 vs. 0.0513). Notably, replacing our depth branch with Depth Anything 3 (X-WAM w/o depth + DA3) preserves strong RGB quality but degrades depth accuracy (AbsRel 0.1045 vs. 0.0349) and point cloud quality (CD 0.0401 vs. 0.0049), confirming that the integrated depth branch produces more geometrically consistent predictions than a general-purpose monocular estimator. 

8 

Table 4: Ablation studies on the RoboCasa benchmark. **Bold** : best; underline: second best. 

|Variant|SR_↑_|Latency||RGB||Dep|th|Point Cloud|
|---|---|---|---|---|---|---|---|---|
|||(ms)_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|AbsRel_↓_|_δ_1_↑_|CD_↓_|
|_(a) Depth architecture design_|||||||||
|No depth|63.0|**1033**|23.09|0.8916|0.0548|–|–|–|
|Sequence concatenation|**68.7**|1888|**23.60**|**0.8987**|**0.0488**|**0.0332**|**0.9774**|**0.0037**|
|Channel concatenation|64.2|1266|23.20|0.8933|0.0522|0.0377|0.9728|0.0052|
|Interleaved branch (Ours)|67.8|**1033**|23.46|0.8942|0.0513|0.0349|0.9738|0.0049|
|_(b) Noise scheduling strategy_|||||||||
|Sync train + Sync infer|66.4|4665|**23.48**|**0.8963**|**0.0502**|0.0375|0.9725|**0.0041**|
|Decoupled train + Sync infer|66.3|4665|23.17|0.8937|0.0529|0.0397|0.9701|0.0050|
|Decoupled train + Async infer|67.2|**1033**|22.60|0.8878|0.0561|0.0430|0.9680|0.0061|
|ANS train + Async infer (Ours)|**67.8**|**1033**|23.46|0.8942|0.0513|**0.0349**|**0.9738**|0.0049|


### **4.3 Ablation Studies** 

We conduct ablation studies on the RoboCasa benchmark to validate the key design choices of X-WAM. Due to computational constraints, all ablation variants are fine-tuned directly from the Wan2.2-TI2V-5B weights on the benchmark data without the large-scale pretraining stage described in Section 3.4. Unless otherwise stated, all variants share the same data, hyperparameters, and training schedule. Action latency is measured on a single NVIDIA RTX 3090 GPU. 

**Depth architecture design.** We compare four depth incorporation strategies (Table 4(a)). The Latency column reports the action generation latency during policy execution. Sequence concatenation achieves the best quality metrics by treating depth as explicit tokens, but nearly doubles the action latency to 1888 ms due to the expanded sequence length. Channel concatenation also introduces noticeable overhead (1266 ms). In contrast, our interleaved branch matches the latency of the no-depth variant (1033 ms), since the depth branch can be toggled off during action decoding, while delivering clearly superior quality over both the no-depth and channel-concatenation variants. Notably, removing depth supervision entirely causes the policy success rate to drop from 67.8% to 63.0%, confirming that explicit spatial modeling is essential for robust manipulation. Channel concatenation also underperforms in success rate (64.2%), as fusing depth along the channel dimension shifts the input distribution away from the pretrained manifold. 

**Effect of ANS.** We compare four noise scheduling configurations (Table 4(b)), where synchronous variants use 25 joint steps and asynchronous variants decode actions in only 5 steps. The synchronous baselines yield strong RGB metrics but force the policy to wait for all 25 denoising steps, resulting in an action latency of 4665 ms. Asynchronous inference reduces this to 1033 ms, a 4 _._ 5 _×_ speedup, by decoding actions in only the first 5 steps. Among the asynchronous variants, Decoupled-Async achieves a competitive success rate (67.2%) but its reconstruction quality degrades significantly (PSNR 22.60, AbsRel 0.0430), because the video branch must continue denoising conditioned on clean actions, a regime never seen during independently sampled training. Our ANS closes this gap by coupling the training noise distribution to faithfully cover the asynchronous inference regime. As a result, ANS achieves the highest success rate (67.8%) and the best depth metrics at the same 1033 ms latency, while maintaining RGB quality competitive with the synchronous baseline. 

## **5 Conclusion** 

In this work, we presented X-WAM, a unified 4D World Action Model that extends unified world action modeling into spatially aware 4D dynamics simulation. Through a lightweight depth adaptation module that replicates the final DiT blocks as an interleaved depth branch, X-WAM achieves highquality spatial reconstruction without increasing sequence length or compromising pretrained visual priors. Asynchronous Noise Sampling further aligns training and inference noise distributions across modalities, enabling rapid action decoding while preserving video generation quality. Experiments on RoboCasa and RoboTwin 2.0 demonstrate that X-WAM consistently outperforms all baselines in both policy success rate and 4D reconstruction quality, confirming that a single framework can jointly optimize policy execution, visual generation, and spatial reconstruction. 

9 

## **References** 

- [1] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong T. Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. RT-2: vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183, 2023. 

- [2] Dibya Ghosh, Homer Rich Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, You Liang Tan, Lawrence Yunliang Chen, Quan Vuong, Ted Xiao, Pannag R. Sanketi, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Robotics: Science and Systems_ , 2024. 

- [3] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Paul Foster, Pannag R. Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning_ , pages 2679–2713, 2024. 

- [4] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. _CoRR_ , abs/2410.24164, 2024. 

- [5] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0.5: a vision-language-action model with open-world generalization. _CoRR_ , abs/2504.16054, 2025. 

- [6] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, Joel Jang, Zhenyu Jiang, Jan Kautz, Kaushil Kundalia, Lawrence Lao, Zhiqi Li, Zongyu Lin, Kevin Lin, Guilin Liu, Edith LLontop, Loic Magne, Ajay Mandlekar, Avnish Narayan, Soroush Nasiriany, Scott Reed, You Liang Tan, Guanzhi Wang, Zu Wang, Jing Wang, Qi Wang, Jiannan Xiang, Yuqi Xie, Yinzhen Xu, Zhenjia Xu, Seonghyeon Ye, Zhiding Yu, Ao Zhang, Hao Zhang, Yizhou Zhao, Ruijie Zheng, and Yuke Zhu. GR00T N1: an open foundation model for generalist humanoid robots. _CoRR_ , abs/2503.14734, 2025. 

- [7] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- [8] Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, Yujun Shen, and Yinghao Xu. Causal world modeling for robot control. _CoRR_ , abs/2601.21998, 2026. 

- [9] Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, Ayaan Malik, Kyungmin Lee, William Liang, Nadun Ranawaka, Jiasheng Gu, Yinzhen Xu, Guanzhi Wang, Fengyuan Hu, Avnish Narayan, Johan Bjorck, Jing Wang, Gwanghyun Kim, Dantong Niu, Ruijie Zheng, Yuqi Xie, 

10 

Jimmy Wu, Qi Wang, Ryan Julian, Danfei Xu, Yilun Du, Yevgen Chebotar, Scott Reed, Jan Kautz, Yuke Zhu, Linxi "Jim" Fan, and Joel Jang. World action models are zero-shot policies. _CoRR_ , abs/2602.15922, 2026. 

- [10] Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-wam: Do world action models need test-time future imagination? _CoRR_ , abs/2603.16666, 2026. 

- [11] Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, and Jinwei Gu. Cosmos policy: Fine-tuning video models for visuomotor control and planning. _CoRR_ , abs/2601.16163, 2026. 

- [12] Angen Ye, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, Hao Li, Hengtao Li, Jie Li, Jindi Lv, Jingyu Liu, Min Cao, Peng Li, Qiuping Deng, Wenjun Mei, Xiaofeng Wang, Xinze Chen, Xinyu Zhou, Yang Wang, Yifan Chang, Yifan Li, Yukun Zhou, Yun Ye, Zhichao Liu, and Zheng Zhu. Gigaworld-policy: An efficient action-centered world-action model. _CoRR_ , abs/2603.17240, 2026. 

- [13] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse control tasks through world models. _Nature_ , 640(8059):647–653, 2025. 

- [14] Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. Irasim: A fine-grained world model for robot manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9834–9844, 2025. 

- [15] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- [16] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- [17] GigaWorld Team, Angen Ye, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, Haoyun Li, Jiagang Zhu, Kerui Li, Mengyuan Xu, et al. Gigaworld-0: World models as data engine to empower embodied ai. _arXiv preprint arXiv:2511.19861_ , 2025. 

- [18] Yufeng Cui, Honghao Chen, Haoge Deng, Xu Huang, Xinghang Li, Jirong Liu, Yang Liu, Zhuoyan Luo, Jinsheng Wang, Wenxuan Wang, et al. Emu3.5: Native multimodal models are world learners. _arXiv preprint arXiv:2510.26583_ , 2025. 

- [19] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _CoRR_ , abs/2504.02792, 2025. 

- [20] Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, Hongyan Zhao, Hanyu Liu, Zhizhong Su, Lei Ma, Hang Su, and Jun Zhu. Motus: A unified latent action world model. _CoRR_ , abs/2512.13030, 2025. 

- [21] Yichao Shen, Fangyun Wei, Zhiying Du, Yaobo Liang, Yan Lu, Jiaolong Yang, Nanning Zheng, and Baining Guo. Videovla: Video generators can be generalizable robot manipulators. _CoRR_ , abs/2512.06963, 2025. 

- [22] Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Hu Yue, Jingbin Cai, Si Liu, Jianlan Luo, Liliang Chen, Shuicheng Yan, Maoqing Yao, and Guanghui Ren. Genie envisioner: A unified world foundation platform for robotic manipulation. _CoRR_ , abs/2508.05635, 2025. 

- [23] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 

- [24] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. In _International Conference on Learning Representations_ , 2021. 

11 

- [25] Tero Karras, Miika Aittala, Timo Aila, and Samuli Laine. Elucidating the design space of diffusion-based generative models. In _Advances in neural information processing systems_ , volume 35, pages 26565–26577, 2022. 

- [26] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44(10-11):1684–1704, 2025. 

- [27] Jonas Pai, Liam Achenbach, Victoriano Montesinos, Benedek Forrai, Oier Mees, and Elvis Nava. mimic-video: Video-action models for generalizable robot control beyond vlas. _CoRR_ , abs/2512.15692, 2025. 

- [28] Teli Ma, Jia Zheng, Zifan Wang, Chunli Jiang, Andy Cui, Junwei Liang, and Shuo Yang. Dit4dit: Jointly modeling video dynamics and actions for generalizable robot control. _CoRR_ , abs/2603.10448, 2026. 

- [29] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, Hang Li, and Tao Kong. Vision-language foundation models as effective robot imitators. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- [30] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. RDT-1B: a diffusion foundation model for bimanual manipulation. In _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [31] Rui Cai, Jun Guo, Xinze He, Piaopiao Jin, Jie Li, Bingxuan Lin, Futeng Liu, Wei Liu, Fei Ma, Kun Ma, Feng Qiu, Heng Qu, Yifei Su, Qiao Sun, Dong Wang, Donghao Wang, Yunhong Wang, Rujie Wu, Diyun Xiang, Yu Yang, Hangjun Ye, Yuan Zhang, and Quanyun Zhou. Xiaomirobotics-0: An open-sourced vision-language-action model with real-time execution. _CoRR_ , abs/2602.12684, 2026. 

- [32] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. In _Advances in Neural Information Processing Systems_ , 2023. 

- [33] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. In _Forty-second International Conference on Machine Learning_ , 2025. 

- [34] Qian Long, Yueze Wang, Jiaxi Song, Junbo Zhang, Peiyan Li, Wenxuan Wang, Yuqi Wang, Haoyang Li, Shaoxuan Xie, Guocai Yao, Hanbo Zhang, Xinlong Wang, Zhongyuan Wang, Xuguang Lan, Huaping Liu, and Xinghang Li. Scaling world model for hierarchical manipulation policies. _CoRR_ , abs/2602.10983, 2026. 

- [35] Physical Intelligence, Bo Ai, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Greg Balke, Kevin Black, George Bokinsky, Shihao Cao, Thomas Charbonnier, et al. _π_ 0 _._ 7: a steerable generalist robotic foundation model with emergent capabilities. _arXiv preprint arXiv:2604.15483_ , 2026. 

- [36] Yi Chen, Yuying Ge, Yizhuo Li, Yixiao Ge, Mingyu Ding, Ying Shan, and Xihui Liu. Moto: Latent motion token as the bridging language for robot manipulation. _CoRR_ , abs/2412.04445, 2024. 

- [37] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, Deli Zhao, and Hao Chen. Worldvla: Towards autoregressive action world model. _CoRR_ , abs/2506.21539, 2025. 

- [38] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, He Wang, Zhizheng Zhang, Li Yi, Wenjun Zeng, and Xin Jin. Dreamvla: A vision-language-action model dreamed with comprehensive world knowledge. _CoRR_ , abs/2507.04447, 2025. 

12 

- [39] Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _CoRR_ , abs/2506.19850, 2025. 

- [40] Jingwen Sun, Wenyao Zhang, Zekun Qi, Shaojie Ren, Zezhi Liu, Hanxin Zhu, Guangzhong Sun, Xin Jin, and Zhibo Chen. VLA-JEPA: enhancing vision-language-action model with latent world model. _CoRR_ , abs/2602.10098, 2026. 

- [41] Yucheng Hu, Jianke Zhang, Yuanfei Luo, Yanjiang Guo, Xiaoyu Chen, Xinshu Sun, Kun Feng, Qingzhou Lu, Sheng Chen, Yangang Zhang, Wei Li, and Jianyu Chen. Bagelvla: Enhancing long-horizon manipulation via interleaved vision-language-action generation. _CoRR_ , abs/2602.09849, 2026. 

- [42] Zhanguang Zhang, Zhiyuan Li, Behnam Rahmati, Rui Heng Yang, Yintao Ma, Amir Rasouli, Sajjad Pakdamansavoji, Yangzheng Wu, Lingfeng Zhang, Tongtong Cao, Feng Wen, Xinyu Wang, Xingyue Quan, and Yingxue Zhang. Do world action models generalize better than vlas? A robustness study. _CoRR_ , abs/2603.22078, 2026. 

- [43] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. In _Forty-first International Conference on Machine Learning_ , pages 61229–61245, 2024. 

- [44] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, and Xuelong Li. Spatialvla: Exploring spatial representations for visual-language-action model. _CoRR_ , abs/2501.15830, 2025. 

- [45] Tao Lin, Gen Li, Yilei Zhong, Yanwen Zou, and Bo Zhao. Evo-0: Vision-language-action model with implicit spatial understanding. _CoRR_ , abs/2507.00416, 2025. 

- [46] Fuhao Li, Wenxuan Song, Han Zhao, Jingbo Wang, Pengxiang Ding, Donglin Wang, Long Zeng, and Haoang Li. Spatial forcing: Implicit spatial representation alignment for visionlanguage-action model. _CoRR_ , abs/2510.12276, 2025. 

- [47] Zhengshen Zhang, Hao Li, Yalun Dai, Zhengbang Zhu, Lei Zhou, Chenchen Liu, Dong Wang, Francis E. H. Tay, Sijin Chen, Ziwei Liu, Yuxiao Liu, Xinghang Li, and Pan Zhou. From spatial to actions: Grounding vision-language-action model in spatial foundation priors. _CoRR_ , abs/2510.17439, 2025. 

- [48] Chengmeng Li, Junjie Wen, Yaxin Peng, Yan Peng, and Yichen Zhu. Pointvla: Injecting the 3d world into vision-language-action models. _IEEE Robotics Autom. Lett._ , 11(3):2506–2513, 2026. 

- [49] Lin Sun, Bin Xie, Yingfei Liu, Hao Shi, Tiancai Wang, and Jiale Cao. Geovla: Empowering 3d representations in vision-language-action models. _CoRR_ , abs/2508.09071, 2025. 

- [50] Peiyan Li, Yixiang Chen, Hongtao Wu, Xiao Ma, Xiangnan Wu, Yan Huang, Liang Wang, Tao Kong, and Tieniu Tan. Bridgevla: Input-output alignment for efficient 3d manipulation learning with vision-language models. _CoRR_ , abs/2506.07961, 2025. 

- [51] Haoyu Zhen, Qiao Sun, Hongxin Zhang, Junyan Li, Siyuan Zhou, Yilun Du, and Chuang Gan. Tesseract: Learning 4d embodied world models. _CoRR_ , abs/2504.20995, 2025. 

- [52] Jun Guo, Xiaojian Ma, Yikai Wang, Min Yang, Huaping Liu, and Qing Li. Flowdreamer: A RGB-D world model with flow-based motion representations for robot manipulation. _IEEE Robotics Automation Letters_ , 11(3):2466–2473, 2026. 

- [53] Siyuan Huang, Liliang Chen, Pengfei Zhou, Shengcong Chen, Zhengkai Jiang, Yutao Hu, Peng Gao, Hongsheng Li, Maoqing Yao, and Guanghui Ren. Enerverse: Envisioning embodied future space for robotics manipulation. _CoRR_ , abs/2501.01895, 2025. 

- [54] Zeyi Liu, Shuang Li, Eric Cousineau, Siyuan Feng, Benjamin Burchfiel, and Shuran Song. Geometry-aware 4d video generation for robot manipulation. _CoRR_ , abs/2507.01099, 2025. 

- [55] Wenbing Huang, Yu-Wei Chao, Arsalan Mousavian, Ming-Yu Liu, Dieter Fox, Kaichun Mo, and Li Fei-Fei. Pointworld: Scaling 3d world models for in-the-wild robotic manipulation. _CoRR_ , abs/2601.03782, 2026. 

13 

- [56] Zezhong Qian, Xiaowei Chi, Yuming Li, Shizun Wang, Zhiyuan Qin, Xiaozhu Ju, Sirui Han, and Shanghang Zhang. Wristworld: Generating wrist-views via 4d world models for robotic manipulation. _CoRR_ , abs/2510.07313, 2025. 

- [57] Jiaxu Wang, Yicheng Jiang, Tianlun He, Jingkai Sun, Qiang Zhang, Junhao He, Jiahang Cao, Zesen Gan, Mingyuan Sun, Qiming Shao, and Xiangyu Yue. MVISTA-4D: view-consistent 4d world model with test-time action inference for robotic manipulation. _CoRR_ , abs/2602.09878, 2026. 

- [58] Guanxing Lu, Shiyi Zhang, Ziwei Wang, Changliu Liu, Jiwen Lu, and Yansong Tang. Manigaussian: Dynamic gaussian splatting for multi-task robotic manipulation. In _18th European Conference on Computer Vision_ , pages 349–366, 2024. 

- [59] Guanxing Lu, Baoxiong Jia, Puhao Li, Yixin Chen, Ziwei Wang, Yansong Tang, and Siyuan Huang. GWM: towards scalable gaussian world models for robotic manipulation. _CoRR_ , abs/2508.17600, 2025. 

- [60] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM Trans. Graph._ , 42(4):139:1–139:14, 2023. 

- [61] Shuzhe Wang, Vincent Leroy, Yohann Cabon, Boris Chidlovskii, and Jérôme Revaud. Dust3r: Geometric 3d vision made easy. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 20697–20709, 2024. 

- [62] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotný. VGGT: visual geometry grounded transformer. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 5294–5306, 2025. 

- [63] Sili Chen, Hengkai Guo, Shengnan Zhu, Feihu Zhang, Zilong Huang, Jiashi Feng, and Bingyi Kang. Video depth anything: Consistent depth estimation for super-long videos. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 22831–22840, 2025. 

- [64] Haotong Lin, Sili Chen, Junhao Liew, Donny Y. Chen, Zhenyu Li, Guang Shi, Jiashi Feng, and Bingyi Kang. Depth anything 3: Recovering the visual space from any views. _CoRR_ , abs/2511.10647, 2025. 

- [65] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [66] Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu. Roformer: Enhanced transformer with rotary position embedding. _Neurocomputing_ , 568:127063, 2024. 

- [67] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- [68] Wenliang Zhao, Lujia Bai, Yongming Rao, Jie Zhou, and Jiwen Lu. Unipc: A unified predictorcorrector framework for fast sampling of diffusion models. In _Advances in Neural Information Processing Systems_ , volume 36, pages 49842–49869, 2023. 

- [69] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. In _RSS Workshop: Data Generation for Robotics_ , 2024. 

- [70] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [71] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

14 

- [72] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- [73] Yang Tian, Yuyin Yang, Yiman Xie, Zetao Cai, Xu Shi, Ning Gao, Hangxu Liu, Xuekun Jiang, Zherui Qiu, Feng Yuan, et al. Interndata-a1: Pioneering high-fidelity synthetic data for pre-training generalist policy. _arXiv preprint arXiv:2511.16651_ , 2025. 

- [74] Ajay Mandlekar, Soroush Nasiriany, Bowen Wen, Iretiayo Akinola, Yashraj Narang, Linxi Fan, Yuke Zhu, and Dieter Fox. Mimicgen: A data generation system for scalable robot learning using human demonstrations. _arXiv preprint arXiv:2310.17596_ , 2023. 

- [75] Kevin Black, Manuel Y Galliker, and Sergey Levine. Real-time execution of action chunking flow policies. _arXiv preprint arXiv:2506.07339_ , 2025. 

15 

## **A Detailed Algorithms** 

We provide the complete algorithmic procedures for X-WAM. Algorithm 1 details the single denoising step, which jointly processes the multi-modal sequence through the shared DiT trunk and the interleaved depth branch to produce velocity predictions and depth estimates. Algorithm 2 presents the full Asynchronous Noise Sampling (ANS) procedure for both training and inference, illustrating how coupled noise sampling during training aligns with the asynchronous denoising schedule at inference time. 

**Algorithm 1** DENOISE: Single Denoising Step of X-WAM **Require:** Noisy video latent **z**<sup>_t_</sup> _O_<sup>_O_, noisy state</sup><sup>**z**</sup> _s_<sup>_ta_, noisy action</sup><sup>**z**</sup><sup>_t_</sup> _a_<sup>_a_, video timestep</sup><sup>_tO_, action timestep</sup> _ta_ , initial observation _O_ 0, initial state _s_ 0, language instruction _c_ **Ensure:** Predicted velocities **v** ˆ _O,_ ˆ **v** _s,_ ˆ **v** _a_ ; predicted inverse depth _D_<sup>ˆ</sup> 1: **z** _O_ 0 _←_ CausalVAE( _O_ 0); **z** _s_ 0 _←_ MLP _s_ ( _s_ 0) _▷_ Encode conditions with _t_ = 0 2: **Z** _←_ Concat( **z** _O_ 0 _,_ **z**<sup>_t_</sup> _O_<sup>_O,_</sup><sup>**z**</sup><sup>_s_</sup> 0<sup>_,_</sup><sup>**z**</sup> _s_<sup>_ta,_</sup><sup>**z**</sup> _a_<sup>_ta_)</sup> 3: Add learnable view embeddings to **Z** 4: **for** _i_ = 1 **to** _N − M_ **do** _▷_ Shared trunk 5: **Z** _←_ DiTBlock _i_ ( **Z** ) 6: **end for** 7: **Z** m _←_ **Z** ; **Z** _D ←_ **Z** _▷_ Initialize main and depth branches 8: **for** _j_ = 1 **to** _M_ **do** _▷_ Interleaved main-depth processing 9: **Z** _D ←_ DepthBlock _j_ ( **Z** _D |_ **Z** m) _▷_ Depth attends to main branch’s input 10: **Z** m _←_ DiTBlock _N −M_ + _j_ ( **Z** m) _▷_ Main branch 11: **end for** 12: **v** ˆ _O,_ **v** ˆ _s,_ **v** ˆ _a ←_ Headmain( **Z** m) 13: _D_<sup>ˆ</sup> _←_ Headdepth( **Z** _D_ ) _▷_ Regress inverse depth 14: **return v** ˆ _O,_ **v** ˆ _s,_ **v** ˆ _a, D_<sup>ˆ</sup> 

## **B Training Details** 

### **B.1 Pretraining Data** 

Table 5 summarizes the pretraining datasets used in X-WAM. The data spans both real-robot and simulated environments, totaling over 1.49 million episodes and approximately 5,874 hours. All datasets undergo careful preprocessing and filtering: we remove episodes containing base locomotion, dexterous manipulation, and failed executions. Following [4], we additionally filter out stationary frames from the DROID dataset. All videos are uniformly downsampled to 3.75 FPS and resized to a resolution of 320 _×_ 256. Since most pretraining datasets lack depth annotations, we extract depth maps from all training videos using Video Depth Anything [63]. 

Table 5: Summary of pretraining datasets used in X-WAM. 

|Dataset|Source|Episodes|Duration (h)|
|---|---|---|---|
|AgibotWorld-Beta [71]|Real|866,562|2,221.5|
|DROID [72]|Real|74,734|280.3|
|InternA1-Aloha [73]|Sim|184,803|1,337.3|
|InternA1-Genie1 [73]|Sim|50,638|174.0|
|InternA1-Lift2 [73]|Sim|231,018|1,464.7|
|RoboCasa MimicGen [69, 74]|Sim|56,771|282.4|
|RoboTwin 2.0 [70]|Sim|27,500|113.7|
|Total|–|1,492,026|5,873.9|


### **B.2 Implementation Details** 

**State and action representation.** To unify heterogeneous single-arm and dual-arm robots across datasets, we define a universal state and action interface based on end-effector poses. The state is 

16 

**Algorithm 2** Asynchronous Noise Sampling (ANS): Training and Inference **— Training: Coupled Noise Sampling — Require:** Clean video latent **z**<sup>0</sup> _O_<sup>, clean state</sup><sup>**z**</sup> _s_<sup>0, clean action</sup><sup>**z**0</sup> _a_<sup>, probability</sup><sup>_p_</sup> **Ensure:** Noisy samples **z**<sup>_t_</sup> _O_<sup>_O,_</sup><sup>**z**</sup> _s_<sup>_ta,_</sup><sup>**z**</sup> _a_<sup>_ta_with coupled timesteps</sup><sup>_tO, ta_</sup> 1: Draw _u ∼_ U(0 _,_ 1) 2: **if** _u < p_ **then** _▷_ Action-conditioned video generation 3: _ta ←_ 0; _tO ∼_ U(0 _,_ 1) 4: **else** _▷_ Asynchronous joint generation 5: _ta ∼_ U(0 _,_ 1); _b ∼_ Beta(1 _._ 5 _,_ 1) 6: _tO ← ta_ + (1 _− ta_ ) _· b ▷_ Rescale to [ _ta,_ 1], ensuring _tO ≥ ta_ 7: **end if** 8: **_ϵ_** _O,_ **_ϵ_** _s,_ **_ϵ_** _a ∼N_ ( **0** _,_ **I** ) 9: **z**<sup>_t_</sup> _O_<sup>_O←_(1</sup><sup>_−tO_)</sup><sup>**z**</sup> _O_<sup>0+</sup><sup>_tO_</sup><sup>**_ϵ_**</sup><sup>_O_;</sup><sup>**z**</sup> _s_<sup>_ta←_(1</sup><sup>_−ta_)</sup><sup>**z**0</sup> _s_<sup>+</sup><sup>_ta_</sup><sup>**_ϵ_**</sup><sup>_s_;</sup><sup>**z**</sup> _a_<sup>_ta←_(1</sup><sup>_−ta_)</sup><sup>**z**0</sup> _a_<sup>+</sup><sup>_ta_</sup><sup>**_ϵ_**</sup><sup>_a_</sup> _▷_ Flow matching interpolation 10: Compute _L_ total via DENOISE (Algorithm 1) and backpropagate **— Inference: Asynchronous Denoising — Require:** Conditions ( _O_ 0 _, s_ 0 _, c_ ), video steps _TO_ , action steps _Ta_ ( _Ta < TO_ ) **Ensure:** Denoised video **z** _O_ , state **z** _s_ , action **z** _a_ 11: **z** _O,_ **z** _s,_ **z** _a ∼N_ ( **0** _,_ **I** ) _▷_ Initialize from pure noise 12: Initialize schedulers: _SO_ with _TO_ steps, _Sa_ with _Ta_ steps 13: **for** _k_ = 1 **to** _TO_ **do** 14: Get current timestep _tO_ from _SO_ 15: **if** _k ≤ Ta_ **then** _▷_ Joint denoising phase 16: Get current timestep _ta_ from _Sa_ 17: **v** ˆ _O,_ **v** ˆ _s,_ **v** ˆ _a,_  ←_ DENOISE( **z** _O,_ **z** _s,_ **z** _a, tO, ta, O_ 0 _, s_ 0 _, c_ ) 18: **z** _O ←SO_ .step( **z** _O,_ ˆ **v** _O_ ); **z** _s ←Sa_ .step( **z** _s,_ ˆ **v** _s_ ); **z** _a ←Sa_ .step( **z** _a,_ ˆ **v** _a_ ) 19: **else** _▷_ Video-only denoising phase (action-conditioned) 20: **v** ˆ _O,_  ,_  ,_  ←_ DENOISE( **z** _O,_ **z** _s,_ **z** _a, tO,_ 0 _, O_ 0 _, s_ 0 _, c_ ) 21: **z** _O ←SO_ .step( **z** _O,_ ˆ **v** _O_ ) 22: **end if** 23: **end for** 24: **return z** _O,_ **z** _s,_ **z** _a ▷_ Actions available after step _Ta_ ; video after step _TO_ 

represented as a 16-dimensional absolute vector: (position3 + quaternion4 + gripper1) _×_ 2 arms. The action is represented as a 14-dimensional relative vector: (∆position3 + ∆axis-angle3 + gripper action1) _×_ 2 arms. For single-arm robots, only the first 8 dimensions of the state and the first 7 dimensions of the action are supervised. We compute per-dataset quantile statistics ( _q_ 0 _._ 01, _q_ 0 _._ 99) for normalization. Notably, the action normalization applies only scaling without bias, preserving the semantics that a zero action corresponds to no movement across all datasets. 

**Large-scale pretraining.** We pretrain X-WAM on 256 NVIDIA H20 GPUs with a per-GPU batch size of 8 (total batch size 2,048). We use the AdamW optimizer with a peak learning rate of 1 _×_ 10<sup>_−_4</sup> , 1,000 steps of linear warmup followed by cosine decay to 0, and train for 40,000 steps. The prediction horizon is set to _H_ = `8` . The loss weighting coefficients are _λs_ = `1.0` , _λa_ = `1.0` , and _λD_ = `1.0` . The number of replicated depth blocks is _M_ = `10` , and the ANS action-conditioned probability is _p_ = `0.5` . 

**Benchmark fine-tuning.** For RoboCasa and RoboTwin 2.0, we further fine-tune the pretrained model on the respective benchmark data using 32 NVIDIA H20 GPUs with a per-GPU batch size of 4 (total batch size 128), a learning rate of 3 _×_ 10<sup>_−_5</sup> , and the same warmup and cosine decay schedule. Fine-tuning proceeds for 20,000 steps. To obtain ground-truth depth maps for fine-tuning, we replay the official demonstration data in the simulator, ensuring that the total data volume and initial configurations remain unchanged and that the replay random seeds do not overlap with those used at test time. For RoboCasa, we directly use the raw actions provided in the dataset as supervision signals. For RoboTwin 2.0, we use relative actions that are converted to absolute end-effector poses 

17 

based on the state of the first frame in each action chunk before being sent to the simulator for execution. 

**Inference.** We use asynchronous denoising with _Ta_ = 10 action denoising steps and _TO_ = 50 video denoising steps, following the UniPC [68] scheduler. The classifier-free guidance scale is set to 1.0, as we empirically find that larger guidance scales do not improve action quality but increase inference cost. For both benchmarks, each task is evaluated over 100 episodes and the success rate is averaged. All other evaluation settings follow the official benchmark protocols. 

### **B.3 Baseline Details** 

**RoboCasa.** The results of _π_ 0 [4], GR00T-N1.5 [6], UWM [19], and Cosmos Policy [11] are directly taken from [11]. DreamZero [9] is reproduced using the official codebase, with the backbone replaced by Wan2.2-5B [65] for fair comparison. 

**RoboTwin 2.0.** The results of _π_ 0 [4] and _π_ 0 _._ 5 [5] are taken from [8]. The results of Motus [20] and GigaWorld-Policy [12] are taken from their respective papers. We reimplement UWM [19] with the backbone replaced by Wan2.2-5B [65] for fair comparison. 

**Pretraining data parity.** We note that among all baselines, only DreamZero is fine-tuned from a general-purpose video generation model without prior exposure to robotic data. All other baselines ( _π_ 0, _π_ 0 _._ 5, GR00T-N1.5, UWM, Cosmos Policy, GigaWorld-Policy, and Motus) incorporate large-scale robotic datasets in their pretraining pipelines. Therefore, the comparison is conducted under broadly comparable data regimes. 

## **C Detailed Results** 

We report per-task success rates for X-WAM on the RoboCasa and RoboTwin 2.0 benchmarks. 

### **C.1 Per-Task Results on RoboCasa** 

Table 6 presents the success rate of X-WAM on each of the 24 manipulation tasks in the RoboCasa benchmark. 

### **C.2 Per-Task Results on RoboTwin 2.0** 

Table 7 presents the per-task success rate under both Clean and Randomized settings on RoboTwin 2.0. 

## **D Real Robot Experiments** 

To validate the practical applicability of X-WAM, we deploy the model on a real-world dual-arm robotic platform and evaluate it on an earphone packing task. We select this task because it is a challenging long-horizon manipulation scenario that places stringent demands on 3D spatial reasoning: the robot must estimate the precise 6-DoF pose of the earphone case, localize the narrow slot openings whose geometry varies across orientations, and execute insertion trajectories that satisfy subcentimeter clearance constraints in all three spatial dimensions. These requirements make earphone packing a compelling testbed for evaluating whether the explicit 4D spatial awareness provided by X-WAM translates into tangible manipulation benefits compared to methods that operate purely in 2D pixel space. Beyond spatial precision, the task further requires robust bimanual coordination across four sequential stages, testing both long-horizon reliability and real-time execution efficiency. 

**Setup.** All experiments are conducted on an AC One dual-arm platform equipped with one main camera and two wrist-mounted cameras, all operating at a resolution of 320 _×_ 256, as illustrated in Figure 3. We collect approximately 20 hours of demonstration data for the earphone packing task. The model is fine-tuned on 64 NVIDIA H20 GPUs with a per-GPU batch size of 4 for 40,000 steps. We employ asynchronous inference with 8 denoising steps on an NVIDIA RTX 5090 D 

18 

Table 6: Per-task success rate (%) of X-WAM on the RoboCasa benchmark (24 tasks). 

|#|Task|SR|
|---|---|---|
|1|`CloseDoubleDoor`|87.0|
|2|`CloseDrawer`|100.0|
|3|`CloseSingleDoor`|96.0|
|4|`CoffeePressButton`|96.0|
|5|`CoffeeServeMug`|82.0|
|6|`CoffeeSetupMug`|45.0|
|7|`OpenDoubleDoor`|94.0|
|8|`OpenDrawer`|85.0|
|9|`OpenSingleDoor`|96.0|
|10|`PnPCabToCounter`|73.0|
|11|`PnPCounterToCab`|67.0|
|12|`PnPCounterToMicrowave`|62.0|
|13|`PnPCounterToSink`|79.0|
|14|`PnPCounterToStove`|83.0|
|15|`PnPMicrowaveToCounter`|57.0|
|16|`PnPSinkToCounter`|71.0|
|17|`PnPStoveToCounter`|80.0|
|18|`TurnOffMicrowave`|93.0|
|19|`TurnOffSinkFaucet`|86.0|
|20|`TurnOffStove`|35.0|
|21|`TurnOnMicrowave`|82.0|
|22|`TurnOnSinkFaucet`|92.0|
|23|`TurnOnStove`|80.0|
|24|`TurnSinkSpout`|80.0|
||Average|79.2|


GPU, yielding a single-pass latency of approximately 300 ms per action chunk. We further adopt the Real-Time Chunking (RTC) method [75] to overlap denoising computation with action execution. The robot operates at a control frequency of 15 Hz, executing 15 actions (1 second) per chunk with an RTC inference delay of 6 actions, enabling seamless real-time deployment. 


(a) Scalability Settings 

(b) Generalization Settings 

Figure 3: Real-world experimental setup. The AC One dual-arm platform is equipped with one main camera providing a global view and two wrist-mounted cameras for close-up observations. The earphone packing task requires precise bimanual coordination and robust insertion under tight geometric tolerances. 

**Task design.** Since earphone packing is a multi-step long-horizon task, we decompose it into four sequential stages, each contributing 25% of the total progress: 

1. Grasp the empty earphone case and open the lid. 

2. Pick up one earphone and correctly place it into the case. 

3. Pick up the other earphone and correctly place it into the case. 

4. Close the lid and return the case to the table. 

Successfully completing all four stages constitutes 100% progress. We evaluate under six settings designed to test both scalability and generalization: 

- **Scalability** : consecutively packing 1, 2, or 3 earphones in a single episode, testing the model’s ability to handle increasing task length. 

19 

Table 7: Per-task success rate (%) of X-WAM on the RoboTwin 2.0 benchmark (50 tasks). 

|#|Task|Clean|Rand.|#|Task|Clean|Rand.|
|---|---|---|---|---|---|---|---|
|||||26|`place_can_basket`|84.0|82.0|
|1<br>|`adjust_bottle`|100.0<br>|99.0<br>|27|`place_cans_plasticbox`|99.0|98.0|
|2<br>|`beat_block_hammer`|98.0<br>|96.0<br>|28|`place_container_plate`|98.0|100.0|
|3|`blocks_ranking_rgb`|99.0|95.0|29|`place_dual_shoes`|83.0|81.0|
|4|`blocks_ranking_size`|76.0|82.0|30|`place_empty_cup`|98.0|99.0|
|5|`click_alarmclock`|98.0|99.0|31|`place_fan`|84.0|92.0|
|6<br>|`click_bell`|100.0<br>|100.0<br>|32|`place_mouse_pad`|84.0|86.0|
|7<br>|`dump_bin_bigbin`|90.0<br>|96.0<br>|33|`place_object_basket`|85.0|87.0|
|8|`grab_roller`|100.0|100.0|34|`place_object_scale`|93.0|89.0|
|9|`handover_block`|88.0|79.0|35|`place_object_stand`|97.0|96.0|
|10|`handover_mic`|88.0|89.0|36|`place_phone_stand`|75.0|80.0|
|11|`hanging_mug`|46.0|55.0|37|`place_shoe`|97.0|99.0|
|12<br>|`lift_pot`|100.0<br>|99.0<br>|38|`press_stapler`|94.0|90.0|
|13|`move_can_pot`|80.0|84.0|39|`put_bottles_dustbin`|85.0|95.0|
|14<br>|`move_pillbottle_pad`|96.0<br>|98.0<br>|40|`put_object_cabinet`|66.0|76.0|
|15|`move_playingcard_away`|100.0|98.0|41|`rotate_qrcode`|84.0|83.0|
|16<br>|`move_stapler_pad`|67.0<br>|70.0<br>|42|`scan_object`|86.0|79.0|
|17|`open_laptop`|96.0|97.0|43|`shake_bottle`|99.0|99.0|
|18|`open_microwave`|89.0|92.0|44|`shake_bottle_horiz.`|100.0|99.0|
|19|`pick_diverse_bottles`|91.0|92.0|45|`stack_blocks_three`|97.0|95.0|
|20|`pick_dual_bottles`|99.0|100.0|46|`stack_blocks_two`|100.0|100.0|
|21|`place_a2b_left`|90.0|87.0|47|`stack_bowls_three`|88.0|82.0|
|22|`place_a2b_right`|92.0|89.0|48|`stack_bowls_two`|98.0|98.0|
|23|`place_bread_basket`|90.0|91.0|49|`stamp_seal`|93.0|95.0|
|24|`place_bread_skillet`|90.0|96.0|50|`turn_switch`|61.0|72.0|
|25|`place_burger_fries`|97.0|99.0||Average|89.8|90.7|


- **Generalization** : packing 1 earphone under three out-of-distribution conditions not seen during training: (i) novel object placements, (ii) unseen tablecloth colors, and (iii) unseen distractor objects. 

For each setting, we conduct 6 trials: for single-earphone tasks, each of 3 earphone colors is tested twice; for multi-earphone tasks, 6 trials are run with varying color orderings. We report two metrics: average progress (%) across all episodes, and average completion time (seconds) computed only over episodes that achieve 100% progress. 

**Quantitative results.** Table 8 summarizes the real-robot evaluation results. We compare against Xiaomi-Robotics-0 [31], a recent VLA model featuring strong performance and low inference latency. We also attempted to train _π_ 0 _._ 5 [5] using the openpi<sup>1</sup> codebase under the same data and training setup; however, it failed to complete a single full earphone packing episode across all settings, achieving only 25%–50% progress on the single-earphone task (corresponding to grasping the case but failing at earphone insertion). We therefore omit _π_ 0 _._ 5 from the table and only report XR-0 as the baseline. 

**Analysis.** As shown in Table 8, X-WAM consistently outperforms XR-0 across both scalability and generalization settings. In the scalability evaluation, both methods achieve perfect progress on the single-earphone task, but as the number of earphones increases, X-WAM demonstrates superior long-horizon reliability: achieving 93.8% progress on packing 2 earphones compared to 79.1% for XR-0, and 68.0% vs. 63.9% on packing 3 earphones. We attribute this to the explicit 3D spatial awareness of X-WAM, which provides more accurate geometric reasoning for the precise insertion operations required across successive packing stages. In the generalization evaluation, X-WAM shows stronger robustness under novel placements (70.8% vs. 58.3%) and unseen distractors (75.0% vs. 66.7%), while matching XR-0 on unseen tablecloths (66.7%). The improvement on novel placements is particularly notable, as it requires the model to generalize its spatial reasoning to unseen object configurations. Furthermore, X-WAM consistently achieves lower completion times across all settings, indicating that asynchronous denoising with real-time chunking enables not only faster inference but also more efficient trajectories with fewer corrective motions. 

> 1 `https://github.com/Physical-Intelligence/openpi` 

20 

Table 8: Real-robot earphone packing results. Progress (%) is averaged over all 6 episodes; completion time (s) is averaged over episodes reaching 100% progress. 

|Setting|XR-0 [3|1]|X-WAM (O|urs)|
|---|---|---|---|---|
||Prog. (%)|Time (s)|Prog. (%)|Time (s)|
|_Scalability_|||||
|Pack 1 earphone|100.0 (24/24)|54.66|**100.0 (24/24)**|**41.63**|
|Pack 2 earphones|79.1 (38/48)|115.44|**93.8 (45/48)**|**113.25**|
|Pack 3 earphones|63.9 (46/72)|195.66|**68.0 (49/72)**|**160.72**|
|_Generalization_|||||
|Novel placements|58.3 (14/24)|89.63|**70.8 (17/24)**|**46.68**|
|Unseen tablecloth|**66.7 (16/24)**|65.73|**66.7 (16/24)**|**62.01**|
|Unseen distractors|66.7 (16/24)|76.32|**75.0 (18/24)**|**51.53**|


**Qualitative results.** Figure 4 presents a representative rollout sequence of X-WAM on the earphone packing task. For more qualitative results, please visit our project website. 


Figure 4: Qualitative results of X-WAM deployed on a real AC One dual-arm robot for the earphone packing task. Each image shows keyframes from a representative execution rollout. 

## **E Limitations and Future Work** 

While X-WAM demonstrates strong performance across simulation benchmarks and real-robot deployment, two primary limitations remain. 

First, the current framework processes only a fixed-length context window of observations without incorporating historical information or autoregressive rollout, unlike approaches such as DreamZero [9] that leverage KV caching for extended temporal context. This limited context horizon may hinder the model’s ability to fully comprehend task progress in long-horizon manipulation scenarios, potentially leading to suboptimal decisions when the current observation alone is insufficient to disambiguate the task stage. 

Second, as a unified model that jointly generates high-dimensional videos and low-dimensional actions, X-WAM incurs higher inference latency compared to dedicated policy models. Specialized VLAs and lightweight WAMs such as Fast-WAM [10] achieve substantially lower per-step latency, whereas X-WAM requires approximately 300 ms per action chunk with 8 denoising steps. Although real-time chunking [75] enables seamless deployment on physical robots by overlapping computation with execution, the additional inference delay can degrade policy performance, as the robot must act on predictions computed several frames in the past. 

Both limitations point to promising directions for future work. Our proposed architecture and noise scheduling strategy are orthogonal to long-context mechanisms, and X-WAM can be readily extended with history conditioning, KV caching, or autoregressive inference to support longer temporal horizons. Similarly, advances in inference acceleration, such as model distillation, consistency models, and more aggressive asynchronous scheduling, could further narrow the latency gap with dedicated policy models while preserving the benefits of unified 4D modeling. 

21 

